# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T01:02:55.942Z

```
你是 SandboxWorld 项目(泰拉瑞亚 1.4.5.6 的 TypeScript 复刻,实现代码在 ~/Project/GLM/SandboxWorld/game/src/)的机制审计员。你的域是:**光标与方块交互链(交互距离/放置对齐/智能光标/快捷键)**。

参照资源:
- 官方 wiki 离线镜像:~/Project/GLM/SandboxWorld/terraria-wiki-md/(Smart_cursor.md、Controls.md、Builder 相关、Tile_range?)
- 反编译源码:~/Project/GLM/SandboxWorld/Terarria1456/Terrarria 之外——正确路径是 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/(Player.cs tileRangeX/Y 段、SmartCursor;先 grep -n 定位再精读)
- 本仓库实现:game/src/player/SmartCursor.ts、game/src/core/Game.ts(grep "tileRange\|smartCursor\|blockRange")

审计规则:
- 只读审计,禁止修改/创建任何文件,报告作为最终回复返回
- wiki 与实现冲突时以源码裁决;wiki 与源码不符要标注
- 每条结论给实现侧 file:line 证据(grep 到并读过;纯推断标 ❓)

必核清单:
1. 交互距离:tileRangeX=5/Y=3 默认+加成链(工具腰带?建筑药水/建筑背包+1/2?砖层放置范围)、放置 vs 挖掘 vs 使用物品的距离差异、联机距离
2. 智能光标:开启规则(按住 Ctrl?设置常开?)、每种方块的吸附行为(挖矿吸附边框/砍树整体/放置对齐)、智能光标对平台/门/轨道的特殊逻辑、开采优先级
3. 放置对齐:放置物 1×1/2×2/多格的锚点(左上/中心?)、放置时与现有格重叠的拒绝条件、斜坡上放置
4. 方块拾取(选取同型/Pick 行为)、中键选取
5. 快捷键链:H 快速治疗/J 快速魔力/B 快速增益(喝全部增益药水)/数字键武器槽——若未实装标注
6. 光标样式切换(智能光标开启时光标变化)
7. 多格物放置辅助(如长墙连续放置时连成片、路径放置)
8. 开门/交互物件右键链(门/宝箱/雕像/床/旗帜的右键优先级,同格多物件冲突时)

实现侧入口:grep -rn "tileRange\|smartCursor\|blockReach\|quickHeal\|quickMana\|quickBuff" game/src/ | head -50

输出格式(markdown):
## 域:光标与方块交互
### 差异清单
| # | 机制项 | 原版设定(wiki页+数值) | 本仓库实现(file:line) | 状态 | 差异细节 |
状态:✅对齐(一行) / ⚠️数值偏差(两侧数值) / ❌未实现 / 🔀逻辑不同 / ❓存疑 / 📄wiki与源码不符
### 覆盖清单
### 最需修复 TOP N
```

---

## 📎 Attachment · skill_listing · 2026-08-13T01:02:55.945Z

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

## 🤖 Assistant · 2026-08-13T01:02:57.713Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the codebase to understand the current implementation of cursor and block interaction mechanisms. I'll do parallel searches first.

Let me plan:
1. Grep implementation side for tileRange, smartCursor, quickHeal, quickMana, quickBuff, etc.
2. Read game/src/player/SmartCursor.ts
3. Grep Game.ts for interaction range
4. Look at decompiled source Player.cs for tileRangeX/Y, SmartCursor logic
5. Check wiki mirror for Smart_cursor.md, Controls.md, Builder

Let me start with parallel greps.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:02:58.307Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"tileRange\\|smartCursor\\|blockRange\\|quickHeal\\|quickMana\\|quickBuff\\|SmartCursor\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" -l | head -30",
 "description": "Find files with cursor/interaction keywords"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:02:58.328Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts
~/Project/GLM/SandboxWorld/game/src/core/Options.ts
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
~/Project/GLM/SandboxWorld/game/src/vui/VUI.ts
~/Project/GLM/SandboxWorld/game/src/data/vanillaAccFx.ts
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts
~/Project/GLM/SandboxWorld/game/src/player/SmartSelect.ts
~/Project/GLM/SandboxWorld/game/src/player/SmartCursor.ts
~/Project/GLM/SandboxWorld/game/src/debug/DebugReport.ts

```


---

## 🤖 Assistant · 2026-08-13T01:21:51.309Z · <synthetic>

```
API Error: Response stalled mid-stream. The response above may be incomplete.
```


---

## 👤 User(sidechain) · 2026-08-13T01:21:51.312Z

```
[Request interrupted by user]
```


---

## 👤 User(meta)(sidechain) · 2026-08-13T01:25:24.543Z

```
The coordinator sent a message while you were working:
继续你的「光标与方块交互链」审计——继续核对交互距离/智能光标/放置对齐/快捷键(H/J/B)/多格放置辅助/右键优先级并输出最终 markdown 报告(差异清单表+覆盖清单+TOP N)。只读审计禁改文件,每条结论带 file:line。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-13T01:25:27.124Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The coordinator wants me to continue the audit of cursor and block interaction chain. Let me continue with parallel searches to gather evidence. I need to:

1. Check implementation side: SmartCursor.ts, SmartSelect.ts, Game.ts, Player.ts, Options.ts, Renderer.ts
2. Check decompiled source: Player.cs tileRangeX/Y, SmartCursor logic
3. Check wiki mirror: Smart_cursor.md, Controls.md

Let me read the key implementation files first.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:27.244Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/player/SmartCursor.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:27.425Z

**📎 ToolResult**

```
1	// 智能光标（Smart Cursor）——原版 1.4.5.6 Terraria.GameContent/SmartCursorHelper.cs 全量移植。
2	//
3	// 权威源码对照（行号 = Terarria1456 反编译）：
4	//   - 策略链总调度 SmartCursorLookup            SmartCursorHelper.cs:61-165
5	//   - 让位集判定 IsHoveringOverAnInteractableTileThatBlocksSmartCursor :183-199
6	//   - 镐射线  Step_Pickaxe_MineSolids            :2350-2580（Collision.HitLine Collision.cs:782）
7	//   - 锤      Step_Hammers                       :1536-1723
8	//   - 斧      Step_Axe                           :2582-2690
9	//   - 方向锁  GetDesiredDirectionFrom/AllowedForContinuity :1403-1443
10	//   - 状态机  Main.cs:2074-2084 + Player.cs:28344-28374（TryToToggleSmartCursor）
11	//   - 渲染    Main.cs:46016-46066（DrawSmartCursor）
12	//
13	// 我们的 tile id 与原版 tile id 通过 TILE_DEFS[t].vanilla.sheet 桥接（sheet = 原版 Tiles_N 表 id）；
14	// 物品原版 id 通过 ITEM_DEFS[i].vid 或 key 前缀 vi_(\d+)_ 反解。
15	import type { ItemDef } from '../data/items';
16	import { TILE_DEFS, TILE_BY_KEY } from '../data/tiles';
17	import type { TileStore } from '../world/TileStore';
18	import { TileStore as TS } from '../world/TileStore';
19	import { WALL_HOUSE } from '../world/Housing';
20	
21	// ===================== 原版 TileID.Sets / ItemID.Sets 集合（TileID.cs / ItemID.cs 行号注释） =====================
22	
23	/** TileID.cs:205 DisableSmartCursor（57 项）——鼠标悬停即让位，交给直接交互 */
24	const VANILLA_DISABLE_SMART_CURSOR_IDS = [4, 104, 79, 209, 511, 510, 216, 335, 338, 219, 212, 21, 467, 13, 29, 463,
25	  491, 97, 33, 49, 174, 50, 707, 139, 207, 55, 85, 237, 88, 10, 11, 125, 621, 354, 699, 287, 132, 136, 144, 334,
26	  386, 387, 411, 389, 388, 425, 441, 468, 494, 573, 464, 642];
27	
28	/** TileID.cs:201 SmartCursorPickaxePriorityOverride（int 表：12/639/665 → 优先级 1） */
29	const PICKAXE_PRIORITY_OVERRIDE: Record<number, number> = { 12: 1, 639: 1, 665: 1 };
30	
31	/** TileID.cs:203 IgnoreSmartCursorPriorityAxe */
32	const IGNORE_SMART_AXE = new Set([488]);
33	
34	/** TileID.cs:161 IsATreeTrunk（多格树干族：橡树 5 / 棕榈 72 / 各宝石树 583-589 / 樱花 596 / 柳树 616 / 灰烬树 634） */
35	const IS_A_TREE_TRUNK = new Set([5, 72, 583, 584, 585, 586, 587, 588, 589, 596, 616, 634]);
36	
37	/** TileID.cs:173 CommonSapling（树苗族：普通 20 / 宝石 590 / 樱花 595 / 柳树 615） */
38	const COMMON_SAPLING = new Set([20, 590, 595, 615]);
39	
40	/** TileID.cs:195 Boulders（巨石族） */
41	const BOULDERS = new Set([138, 484, 664, 665, 711, 712, 713, 714, 715, 716]);
42	
43	/** TileID.cs:239 IsBeam（梁族：火把侧锚允许） */
44	const IS_BEAM = new Set([124, 561, 574, 575, 576, 577, 578]);
45	
46	/** TileID.cs:243 Platforms（平台族 = tileSolidTop） */
47	const PLATFORMS = new Set([19, 427, 435, 436, 437, 438, 439]);
48	
49	/** TileID.cs:401 Torches（tile 级：只有 4） */
50	const TORCH_TILES = new Set([4]);
51	
52	/** Main.tileNoAttach 全表（Main.cs `tileNoAttach[n] = true` 逐条赋值提取：
53	 *  :7260-7305 植物盆景族 / :7717-7771 树苗 / :7812-7838 火把与开着的门 / :7939-8007
54	 *  可割植物与家具 / :8323-8331 高门 / :9890-9900 平台族（427 + 循环 435-439）/ :10258 岩浆石） */
55	export const TILE_NO_ATTACH_SHEETS: ReadonlySet<number> = new Set([
56	  568, 569, 570, 580, 620, 572, 564, 565, 593, 594,
57	  590, 595, 615, 110, 3, 4, 10, 50, 707,
58	  20, 19, 13, 14, 469, 486, 488, 704, 487, 489, 490, 15, 497, 16, 134, 17, 18, 21, 467, 441,
59	  468, 27, 114, 86, 87, 88, 89, 90, 101, 102, 94, 95, 96, 97, 98, 99, 91, 92, 93,
60	  387, 388, 427, 435, 436, 437, 438, 439, 390,
61	]);
62	
63	/** TileID.Sets.BreakableWhenPlacing（TileID.cs:379）——放置时自动顶掉的方块族 */
64	const BREAKABLE_WHEN_PLACING = new Set([324, 186, 187, 185, 165, 530, 233, 227, 485, 81, 624]);
65	
66	/** TileID.cs:355 NotReallySolid（高门 387/388 与开着的门 10——"看着实心其实能穿"） */
67	const NOT_REALLY_SOLID = new Set([387, 388, 10]);
68	
69	/** ItemID.cs:80 GrassSeeds（草地种子：草 2/丛林 59/猩红 194? 详见策略内 switch） */
70	const GRASS_SEED_ITEMS = new Set([62, 59, 2171, 369, 195, 194, 5214]);
71	
72	/** ItemID.cs:82 Moss（苔藓物品族） */
73	const MOSS_ITEMS = new Set([4349, 4350, 4351, 4352, 4353, 4354, 4377, 4378, 4389, 5127, 5128]);
74	
75	/** ItemID.cs:1192 Torches / :1194 WaterTorches（物品级火把族） */
76	const TORCH_ITEMS = new Set([8, 427, 3004, 523, 433, 429, 974, 1333, 1245, 3114, 430, 3045, 428, 2274, 431, 432,
77	  4383, 4384, 4385, 4386, 4387, 4388, 5293, 5353]);
78	const WATER_TORCH_ITEMS = new Set([523, 1333, 4384]);
79	
80	/** ItemID.cs:254 IsPaintScraper（油漆刮刀）——油漆系统未建，策略 no-op 但集合保留 */
81	const PAINT_SCRAPER_ITEMS = new Set([1100, 1545]);
82	const PAINT_BRUSH_ITEMS = new Set([1071, 1543]);
83	const PAINT_ROLLER_ITEMS = new Set([1072, 1544]);
84	
85	/** WorldGen.cs:3789 GrowTreeSettings.Profiles（GemCorns 策略档案：全部 TreeHeightMax=12 / SaplingTileType=590） */
86	const GEM_TREE_PROFILES: Record<number, { treeHeightMax: number; saplingTile: number }> = {
87	  4851: { treeHeightMax: 12, saplingTile: 590 },
88	  4852: { treeHeightMax: 12, saplingTile: 590 },
89	  4853: { treeHeightMax: 12, saplingTile: 590 },
90	  4854: { treeHeightMax: 12, saplingTile: 590 },
91	  4855: { treeHeightMax: 12, saplingTile: 590 },
92	  4856: { treeHeightMax: 12, saplingTile: 590 },
93	  4857: { treeHeightMax: 12, saplingTile: 590 },
94	};
95	/** WorldGen.cs:30461 GemTreeGroundTest = Conversion.Stone(TileID.cs:26) || Conversion.Moss(TileID.cs:38) */
96	const GEM_TREE_GROUND = new Set([1, 25, 117, 203, 182, 180, 179, 381, 183, 181, 534, 536, 539, 625, 627]);
97	
98	/** 让位集（导出供测试）：原版 57 项 ∩ 我方已注册 sheet——未注册的 tile 不可能出现在世界里，
99	 *  即等价于"按我方已实现的交互裁剪"（门 10/11、宝箱 21/467、床 79、拉杆/开关/计时器、
100	 *  起爆器 411、生命水晶 29、药草 82/83、训练假人、火把 4 等都在原版集内）。 */
101	export const DISABLE_SMART_CURSOR_SHEETS: ReadonlySet<number> = (() => {
102	  const registered = new Set<number>();
103	  for (const d of TILE_DEFS) if (d?.vanilla?.sheet != null) registered.add(d.vanilla.sheet);
104	  return new Set(VANILLA_DISABLE_SMART_CURSOR_IDS.filter((s) => registered.has(s)));
105	})();
106	
107	/** Main.cs:66188 SmartCursorDirectionLocks（上起顺时针 8 方向；箭头帧索引 = 下标） */
108	export const SMART_CURSOR_DIRECTION_LOCKS: ReadonlyArray<readonly [number, number]> = [
109	  [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1],
110	];
111	
112	// ===================== tile sheet 桥 =====================
113	
114	const SHEET_OF: number[] = new Array(TILE_DEFS.length).fill(-1);
115	for (let i = 0; i < TILE_DEFS.length; i++) SHEET_OF[i] = TILE_DEFS[i]?.vanilla?.sheet ?? -1;
116	
117	/** 我方 tile id → 原版 sheet（无映射 -1） */
118	export function sheetOf(t: number): number {
119	  return t >= 0 && t < SHEET_OF.length ? SHEET_OF[t] : -1;
120	}
121	
122	// ===================== 设置（对齐原版 Player.SmartCursorSettings :320-329 + Main.cs:49705） =====================
123	
124	export interface SmartCursorSettings {
125	  /** 模式：true=Toggle（默认，Main.cs:66090 cSmartCursorModeIsToggleAndNotHold 默认 true） */
126	  toggleMode: boolean;
127	  /** 斧优先级排后（默认 false：斧在镐之前） */
128	  smartAxeAfterPickaxe: boolean;
129	  /** 方块智能填充/铺线（默认 true） */
130	  smartBlocksEnabled: boolean;
131	  /** Hold 模式下使用中松开即关（默认 true） */
132	  holdCanReleaseMidUse: boolean;
133	}
134	
135	export const DEFAULT_SMART_CURSOR_SETTINGS: SmartCursorSettings = {
136	  toggleMode: true,
137	  smartAxeAfterPickaxe: false,
138	  smartBlocksEnabled: true,
139	  holdCanReleaseMidUse: true,
140	};
141	
142	// ===================== 输入上下文 =====================
143	
144	export interface SmartCursorHeld {
145	  def: ItemDef | null;
146	  /** Game 侧工具判定结果（镐/斧/锤，含 vi_ 桥接） */
147	  tool: { type: 'pick' | 'axe' | 'hammer' | 'sword'; power: number } | null;
148	}
149	
150	export interface SmartCursorActor {
151	  x: number; y: number; w: number; h: number;   // position / width / height（px）
152	  cx: number; cy: number;                        // Center
153	  facing: number;                                // direction
154	}
155	
156	export interface SmartCursorEnv {
157	  st: TileStore;
158	  /** MouseWorld（世界 px） */
159	  mouse: { x: number; y: number };
160	  actor: SmartCursorActor;
161	  held: SmartCursorHeld;
162	  settings: SmartCursorSettings;
163	  /** tileBoost（放置物加 blockRange；Game 侧与 inTileRange 同公式） */
164	  tileBoost: number;
165	  /** 多彩扳手/宏伟蓝图当前模式位（TOOL_*；仅 MulticolorWrench 策略用） */
166	  wireToolMode: number;
167	  /** EmptyTile 判定的占位实体（玩家 + NPC，px 盒） */
168	  occupants: Array<{ x: number; y: number; w: number; h: number }>;
169	  /** 是否正在按住使用键（controlUseItem）——锁清理与 Hold 模式语义用 */
170	  controlUseItem: boolean;
171	  /** WorldGen.IsAlchemyPlantHarvestable（WorldGen.cs:66198-66225）所需世界态。
172	   *  仅 Step_AlchemySeeds 的"成熟药草可覆盖"判定用；缺省按"未到收获期"处理
173	   *  （等价语义 = 仅 type 84 直接可收）。time 为原版 Main.time 口径：
174	   *  白天 (timeOfDay-0.25)*54000 / 夜晚 (timeOfDay-0.75 或 +0.25)*32400。 */
175	  alchemy?: {
176	    dayTime: boolean; bloodMoon: boolean; moonPhase: number;
177	    raining: boolean; cloudAlpha: number; time: number;
178	    worldSurface: number; remixWorld: boolean; maxTilesY: number;
179	  };
180	}
181	
182	interface Pt { x: number; y: number }
183	
184	// ===================== 格级谓词（Tile.cs / Main.tile* 语义） =====================
185	
186	const tileSolidType = (t: number): boolean => !!TILE_DEFS[t]?.solid;            // Main.tileSolid
187	const tileSolidTopType = (t: number): boolean => !!TILE_DEFS[t]?.platform;      // Main.tileSolidTop
188	const tileAxeType = (t: number): boolean => (TILE_DEFS[t]?.axe ?? -1) >= 0;     // Main.tileAxe
189	/** WorldGen.CanKillTile 子集（SmartCursorHelper 用法：不查镐力，只看"不可破坏"） */
190	const canKillTile = (t: number): boolean => (TILE_DEFS[t]?.pick ?? -1) >= 0;
191	const tileFrameImportantType = (t: number): boolean => !!TILE_DEFS[t]?.framed;  // Main.tileFrameImportant
192	const tileCutType = (t: number): boolean => !!TILE_DEFS[t]?.decor;              // Main.tileCut（可割植物）
193	
194	/** Main.cs:46058-46065 方向箭头显示门：锁向下一格须 !active 或可替换块才画
195	 *  SmartCursorArrow。"可替换" = PlaceThing_IsReplaceableBlock（Player.cs:39094-
196	 *  39103），本作沿用 tileCutType（Main.tileCut 可割植物）口径；锁向格为实心/家具
197	 *  等不可覆盖块时返回 false → 调用方传 null，渲染层不画箭头。
198	 *  越界按"未激活"处理（原版越界 Tile 为空 → !active() → 画；SmartCursor 已钳到
199	 *  [10, w-10]，锁向 ±1 实际不会越界）。 */
200	export function smartCursorArrowAllowed(st: TileStore, x: number, y: number, dir: Pt): boolean {
201	  const nx = x + dir.x, ny = y + dir.y;
202	  if (!st.inBounds(nx, ny)) return true;
203	  if (!activeAt(st, nx, ny)) return true;
204	  return tileCutType(st.type[st.idx(nx, ny)]);
205	}
206	
207	const activeAt = (st: TileStore, x: number, y: number): boolean => st.isActive(x, y);
208	const inActiveAt = (st: TileStore, x: number, y: number): boolean => st.isActuated(x, y);
209	/** Main.tileNoAttach（Main.cs:7260-10258 全表，见 TILE_NO_ATTACH_SHEETS）：该方块不可作为附着锚 */
210	const tileNoAttachType = (sheet: number): boolean => TILE_NO_ATTACH_SHEETS.has(sheet);
211	
212	/** TileID.Sets.BreakableWhenPlacing（TileID.cs:379）：放置时被自动顶掉的方块 */
213	const breakableWhenPlacing = (sheet: number): boolean => BREAKABLE_WHEN_PLACING.has(sheet);
214	
215	/** WorldGen.SolidTile（WorldGen.cs SolidTile(Tile)）:nactive && tileSolid && !tileSolidTop && !half && slope==0 */
216	function solidTile(st: TileStore, x: number, y: number): boolean {
217	  if (!st.inBounds(x, y)) return false;
218	  const i = st.idx(x, y);
219	  if (!activeAt(st, x, y) || tileSolidTopType(st.type[i])) return false;
220	  return tileSolidType(st.type[i]) && st.half[i] === 0 && st.slope[i] === 0;
221	}
222	
223	/** WorldGen.SolidTile2（Acorns/GemCorns 用）:active && tileSolid && slope==0 && !half && !inActive */
224	function solidTile2(st: TileStore, x: number, y: number): boolean {
225	  if (!st.inBounds(x, y)) return false;
226	  const i = st.idx(x, y);
227	  if (!activeAt(st, x, y)) return false;
228	  return tileSolidType(st.type[i]) && st.slope[i] === 0 && st.half[i] === 0;
229	}
230	
231	/** Collision.EmptyTile（Collision.cs:1361-1376）：ignoreTiles=false 时还要求本格 !active
232	 *  （:1364-1367）；随后逐占位实体（玩家/NPC）求交。 */
233	function emptyTile(env: SmartCursorEnv, x: number, y: number, ignoreTiles = false): boolean {
234	  const st = env.st;
235	  if (!ignoreTiles && st.inBounds(x, y) && activeAt(st, x, y)) return false;
236	  const rx = x * 16, ry = y * 16;
237	  for (const o of env.occupants) {
238	    if (o.x < rx + 16 && o.x + o.w > rx && o.y < ry + 16 && o.y + o.h > ry) return false;
239	  }
240	  return true;
241	}
242	
243	/** WorldGen.EmptyTileCheck：矩形内全部为空，或恰为 ignoreType 的树苗 */
244	function emptyTileCheck(st: TileStore, x1: number, x2: number, y1: number, y2: number, ignoreType: number): boolean {
245	  for (let x = x1; x <= x2; x++) {
246	    for (let y = y1; y <= y2; y++) {
247	      if (!st.inBounds(x, y)) return false;
248	      const i = st.idx(x, y);
249	      if (st.type[i] !== 0 && sheetOf(st.type[i]) !== ignoreType) return false;
250	    }
251	  }
252	  return true;
253	}
254	
255	/** Collision.InTileBounds */
256	function inTileBounds(x: number, y: number, x0: number, y0: number, x1: number, y1: number): boolean {
257	  return x >= x0 && x <= x1 && y >= y0 && y <= y1;
258	}
259	
260	const toWorld = (p: Pt): { x: number; y: number } => ({ x: p.x * 16 + 8, y: p.y * 16 + 8 });
261	const dist = (ax: number, ay: number, bx: number, by: number): number => Math.hypot(ax - bx, ay - by);
262	
263	/** 扫描型策略公共收尾：取离鼠标最近的候选（SmartCursorHelper 各策略统一模式） */
264	function nearestOf(targets: Pt[], mouse: { x: number; y: number }): Pt | null {
265	  if (targets.length === 0) return null;
266	  let best = -1;
267	  let point = targets[0];
268	  for (const t of targets) {
269	    const w = toWorld(t);
270	    const d = dist(w.x, w.y, mouse.x, mouse.y);
271	    if (best === -1 || d < best) { best = d; point = t; }
272	  }
273	  return point;
274	}
275	
276	// ===================== Collision.HitLine 1:1（Collision.cs:782-979） =====================
277	
278	export interface HitLineResult { hit: boolean; col: Pt }
279	
280	/**
281	 * 镐射线：DDA 从 (x1,y1) 走到 (x2,y2)，返回首个 `tileSolid && !tileSolidTop && !inActive` 的格。
282	 * ignoreX/ignoreY 是 MineSolids 传入的 `signX*gravDir / -signY*gravDir`（起点一侧的邻居不判）。
283	 * 返回 hit=false 表示线路上出现越界格；hit=true 且 col==终点表示一路畅通。
284	 */
285	export function hitLine(
286	  st: TileStore, x1: number, y1: number, x2: number, y2: number,
287	  ignoreX: number, ignoreY: number, ignoreTargets: ReadonlyArray<Pt>,
288	): HitLineResult {
289	  let value = Math.max(1, Math.min(x1, st.w - 1));
290	  let value2 = Math.max(1, Math.min(y1, Math.max(2, st.h - 40)));
291	  let value3 = Math.max(1, Math.min(x2, st.w - 1));
292	  let value4 = Math.max(1, Math.min(y2, Math.max(2, st.h - 40)));
293	  const blocked = (x: number, y: number): boolean => {
294	    if (!st.inBounds(x, y)) return false;
295	    const i = st.idx(x, y);
296	    return !inActiveAt(st, x, y) && activeAt(st, x, y)
297	      && tileSolidType(st.type[i]) && !tileSolidTopType(st.type[i]);
298	  };
299	  const ignored = (x: number, y: number): boolean =>
300	    ignoreTargets.some((t) => t.x === x && t.y === y);
301	  const num = Math.abs(value - value3);
302	  const num2 = Math.abs(value2 - value4);
303	  if (num === 0 && num2 === 0) return { hit: true, col: { x: value, y: value2 } };
304	  let num3 = 1, num4 = 1;
305	  if (num === 0 || num2 === 0) {
306	    if (num === 0) num3 = 0;
307	    if (num2 === 0) num4 = 0;
308	  } else if (num > num2) num3 = num / num2;
309	  else num4 = num2 / num;
310	  let num5 = 0, num6 = 0;
311	  let num7 = value2 < value4 ? 2 : 1;
312	  let num8 = Math.floor(num), num9 = Math.floor(num2);
313	  const num10 = Math.sign(value3 - value);
314	  const num11 = Math.sign(value4 - value2);
315	  let flag = false, flag2 = false;
316	  do {
317	    if (num7 === 2) {
318	      // 纵向步进（先走 Y）
319	      num5 += num3;
320	      let num13 = Math.floor(num5);
321	      num5 -= num13;
322	      for (let j = 0; j < num13; j++) {
323	        if (!ignored(value, value2) && !ignored(value, value2 - 1) && !ignored(value, value2 + 1)) {
324	          if (ignoreY !== -1 && num11 < 0 && blocked(value, value2 - 1)) return { hit: true, col: { x: value, y: value2 - 1 } };
325	          if (ignoreY !== 1 && num11 > 0 && blocked(value, value2 + 1)) return { hit: true, col: { x: value, y: value2 + 1 } };
326	          if (blocked(value, value2)) return { hit: true, col: { x: value, y: value2 } };
327	        }
328	        if (num8 === 0 && num9 === 0) { flag = true; break; }
329	        value += num10; num8--;
330	        if (num8 === 0 && num9 === 0 && num13 === 1) flag2 = true;
331	      }
332	      if (num9 !== 0) num7 = 1;
333	    } else {
334	      // 横向步进（先走 X）
335	      num6 += num4;
336	      let num12 = Math.floor(num6);
337	      num6 -= num12;
338	      for (let i = 0; i < num12; i++) {
339	        if (!ignored(value, value2) && !ignored(value - 1, value2) && !ignored(value + 1, value2)) {
340	          if (ignoreX !== -1 && num10 < 0 && blocked(value - 1, value2)) return { hit: true, col: { x: value - 1, y: value2 } };
341	          if (ignoreX !== 1 && num10 > 0 && blocked(value + 1, value2)) return { hit: true, col: { x: value + 1, y: value2 } };
342	          if (blocked(value, value2)) return { hit: true, col: { x: value, y: value2 } };
343	        }
344	        if (num8 === 0 && num9 === 0) { flag = true; break; }
345	        value2 += num11; num9--;
346	        if (num8 === 0 && num9 === 0 && num12 === 1) flag2 = true;
347	      }
348	      if (num8 !== 0) num7 = 2;
349	    }
350	    if (blocked(value, value2) && !ignored(value, value2)) return { hit: true, col: { x: value, y: value2 } };
351	  } while (!(flag || flag2));
352	  return { hit: true, col: { x: value, y: value2 } };
353	}
354	
355	// ===================== 手持物语义解析 =====================
356	
357	/** 物品原版 id（def.vid 优先，vi_NNNN_ key 前缀兜底） */
358	export function vanillaItemIdOf(def: ItemDef | null | undefined): number | null {
359	  if (!def) return null;
360	  if (def.vid != null) return def.vid;
361	  const m = /^vi_(\d+)_/.exec(def.key);
362	  return m ? Number(m[1]) : null;
363	}
364	
365	interface HeldSemantics {
366	  vid: number | null;
367	  pick: number; axe: number; hammer: number;
368	  createTileSheet: number | null;
369	  createWall: number | null;
370	  placeStyle: number;
371	}
372	
373	function heldSemantics(held: SmartCursorHeld): HeldSemantics {
374	  const def = held.def;
375	  const tool = held.tool;
376	  return {
377	    vid: vanillaItemIdOf(def),
378	    pick: tool?.type === 'pick' ? tool.power : 0,
379	    // 副斧力（Drax 579 等镐+斧双工具 / Hamaxe 锤+斧）：主工具之外再取 def.axePower
380	    axe: tool?.type === 'axe' ? tool.power : (def?.axePower ?? 0),
381	    hammer: tool?.type === 'hammer' ? tool.power : 0,
382	    createTileSheet: def?.tile != null ? sheetOf(TILE_BY_KEY[def.tile] ?? -1) : null,
383	    createWall: def?.wallId != null ? def.wallId : null,
384	    placeStyle: def?.placeStyle ?? 0,
385	  };
386	}
387	
388	// ===================== SmartCursor 状态机 + 策略链 =====================
389	
390	export class SmartCursor {
391	  // Main.cs:2074-2084
392	  wanted = false;        // SmartCursorWanted_Mouse
393	  showing = false;       // SmartCursorShowing
394	  x = -1; y = -1;        // SmartCursorX/Y
395	  /** SmartCursorHelper.cs:55-57 方向锁/连通锁（仅 Platforms 写入 :1382-1383） */
396	  lockedDirection: Pt | null = null;
397	  lockedContinuity: Pt | null = null;
398	  private prevSmart = false;
399	
400	  /** Player.cs:28344-28374 TryToToggleSmartCursor 1:1。
401	   *  返回 true = 发生按下沿（调用方播音效 12 / menuTick）。 */
402	  updateWanted(controlSmart: boolean, controlUseItem: boolean, s: SmartCursorSettings): boolean {
403	    const edge = controlSmart && !this.prevSmart;
404	    this.prevSmart = controlSmart;
405	    if (s.toggleMode) {
406	      if (edge) this.wanted = !this.wanted;
407	      return edge;
408	    }
409	    if (s.holdCanReleaseMidUse) {
410	      this.wanted = controlSmart;
411	    } else if (this.wanted) {
412	      if (!controlSmart && !controlUseItem) this.wanted = false;
413	    } else {
414	      this.wanted = controlSmart;
415	    }
416	    return edge;
417	  }
418	
419	  /** SmartCursorLookup（SmartCursorHelper.cs:61-165）1:1。 */
420	  lookup(env: SmartCursorEnv): void {
421	    this.showing = false; // :63
422	    const used = this.wanted; // Main.SmartCursorIsUsed = SmartCursorWanted（Main.cs:2962）
423	    if (!env.controlUseItem || !used) { // :64-68
424	      this.lockedDirection = null;
425	      this.lockedContinuity = null;
426	    }
427	    if (!used) return; // :69-72
428	
429	    const st = env.st;
430	    const sem = heldSemantics(env.held);
431	    const s = env.settings;
432	    // :82-87 tileTarget 钳到世界 [10, max-10]
433	    const raw = { x: Math.floor(env.mouse.x / 16), y: Math.floor(env.mouse.y / 16) };
434	    const screenX = Math.max(10, Math.min(raw.x, st.w - 10));
435	    const screenY = Math.max(10, Math.min(raw.y, st.h - 10));
436	    if (!st.inBounds(screenX, screenY)) return; // :88-91
437	    // :92 让位集
438	    const blocks = isHoveringOverAnInteractableTile(st, screenX, screenY);
439	    // :94-103 可达区 = GetTileRegion(tileBoost)（TileReachCheckSettings.cs:53）。
440	    // blockRange（放置物额外射程）已由 Game 侧并入 env.tileBoost（Builder 药水/配饰同公式）
441	    const reach = tileRegion(env.actor, env.tileBoost, st);
442	    // :104 让位集命中且鼠标格在可达区内 → 本次不查找
443	    if (blocks
444	      && inTileBounds(screenX, screenY, reach.x0, reach.y0, reach.x1, reach.y1)) {
445	      return;
446	    }
447	    let fX = -1, fY = -1;
448	    // :118-128 斧的插入位置由 SmartAxeAfterPickaxe 决定（默认 false = 斧最优先）
449	    const steps: Array<() => void> = [];
450	    if (!s.smartAxeAfterPickaxe) steps.push(() => this.stepAxe(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1));
451	    steps.push(
452	      () => this.stepForceCursor(env, sem, reach, screenX, screenY, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
453	      () => this.stepMineShinies(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
454	      () => this.stepMineSolids(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
455	    );
456	    if (s.smartAxeAfterPickaxe) steps.push(() => this.stepAxe(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1));
457	    steps.push(
458	      () => this.stepColoredWrenches(env, sem, reach, screenX, screenY, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
459	      () => this.stepMulticolorWrench(env, sem, reach, screenX, screenY, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
460	      () => this.stepHammers(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
461	      () => this.stepActuationRod(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
462	      () => this.stepWireCutter(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
463	      () => this.stepPlatforms(env, sem, reach, screenX, screenY, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
464	      () => this.stepMinecartTracks(env, sem, reach, screenX, screenY, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
465	      () => this.stepWalls(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
466	      () => this.stepPumpkinSeeds(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
467	      () => this.stepGrassSeeds(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
468	      () => this.stepMoss(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
469	      () => this.stepPigronata(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
470	      () => this.stepBoulders(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
471	      () => this.stepTorch(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
472	      () => this.stepLawnMower(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
473	      () => this.stepBlocksFilling(env, sem, reach, screenX, screenY, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
474	      () => this.stepBlocksLines(env, sem, reach, screenX, screenY, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
475	      () => this.stepPaintRoller(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
476	      () => this.stepPaintBrush(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
477	      () => this.stepPaintScrapper(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
478	      () => this.stepAcorns(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
479	      () => this.stepGemCorns(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
480	      () => this.stepEmptyBuckets(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
481	      () => this.stepActuators(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
482	      () => this.stepAlchemySeeds(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
483	      () => this.stepPlanterBox(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
484	      () => this.stepClayPots(env, sem, reach, screenX, screenY, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
485	      () => this.stepStaffOfRegrowth(env, sem, reach, (x, y) => { fX = x; fY = y; }, () => fX !== -1),
486	    );
487	    for (const step of steps) {
488	      if (fX !== -1 && fY !== -1) break; // 首个命中独占（:118-156 顺序执行）
489	      step();
490	    }
491	    if (fX !== -1 && fY !== -1) { // :157-162
492	      this.x = fX;
493	      this.y = fY;
494	      this.showing = true;
495	    }
496	  }
497	
498	  // ===================== 各策略 =====================
499	
500	  /** :2582-2690 斧：扫 tileAxe → 树干帧校正 → 沿 Y 走到根 → 离鼠标最近 */
501	  private stepAxe(
502	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
503	    set: (x: number, y: number) => void, taken: () => boolean,
504	  ): void {
505	    if (sem.axe <= 0 || taken()) return; // :2590
506	    const st = env.st;
507	    let best = -1;
508	    let bx = -1, by = -1;
509	    for (let i = reach.x0; i <= reach.x1; i++) {
510	      for (let j = reach.y0; j <= reach.y1; j++) {
511	        if (!activeAt(st, i, j)) continue;
512	        const type = st.get(i, j);
513	        const sheet = sheetOf(type);
514	        if (!tileAxeType(type) || IGNORE_SMART_AXE.has(sheet)) continue; // :2604
515	        let num2 = i, k = j;
516	        if (IS_A_TREE_TRUNK.has(sheet)) {
517	          // :2611-2646 多格树干帧校正（左右子块归位到主干列）+ 沿 Y 下到底（树根）
518	          if (inTileBounds(num2 + 1, k, reach.x0, reach.y0, reach.x1, reach.y1)) {
519	            const i2 = st.idx(num2, k);
520	            if (st.frameY[i2] >= 198 && st.frameX[i2] === 44) num2++;
521	            if (st.frameX[i2] === 66 && st.frameY[i2] <= 44) num2++;
522	            if (st.frameX[i2] === 44 && st.frameY[i2] >= 132 && st.frameY[i2] <= 176) num2++;
523	          }
524	          if (inTileBounds(num2 - 1, k, reach.x0, reach.y0, reach.x1, reach.y1)) {
525	            const i2 = st.idx(num2, k);
526	            if (st.frameY[i2] >= 198 && st.frameX[i2] === 66) num2--;
527	            if (st.frameX[i2] === 88 && st.frameY[i2] >= 66 && st.frameY[i2] <= 110) num2--;
528	            if (st.frameX[i2] === 22 && st.frameY[i2] >= 132 && st.frameY[i2] <= 176) num2--;
529	          }
530	          for (; activeAt(st, num2, k) && sheetOf(st.get(num2, k)) === sheet
531	            && sheetOf(st.get(num2, k + 1)) === sheet
532	            && inTileBounds(num2, k + 1, reach.x0, reach.y0, reach.x1, reach.y1); k++) { /* 下到底 */ }
533	        }
534	        if (sheet === 80) {
535	          // :2647-2674 仙人掌帧校正 + 下到底
536	          if (inTileBounds(num2 + 1, k, reach.x0, reach.y0, reach.x1, reach.y1)) {
537	            const i2 = st.idx(num2, k);
538	            if (st.frameX[i2] === 54) num2++;
539	            if (st.frameX[i2] === 108 && st.frameY[i2] === 36) num2++;
540	          }
541	          if (inTileBounds(num2 - 1, k, reach.x0, reach.y0, reach.x1, reach.y1)) {
542	            const i2 = st.idx(num2, k);
543	            if (st.frameX[i2] === 36) num2--;
544	            if (st.frameX[i2] === 108 && st.frameY[i2] === 18) num2--;
545	          }
546	          for (; activeAt(st, num2, k) && sheetOf(st.get(num2, k)) === 80
547	            && sheetOf(st.get(num2, k + 1)) === 80
548	            && inTileBounds(num2, k + 1, reach.x0, reach.y0, reach.x1, reach.y1); k++) { /* 下到底 */ }
549	        }
550	        if (sheet === 323 || sheet === 72) {
551	          // :2675-2680 竹 / 棕榈干下到底
552	          for (; activeAt(st, num2, k)
553	            && ((sheetOf(st.get(num2, k)) === 323 && sheetOf(st.get(num2, k + 1)) === 323)
554	              || (sheetOf(st.get(num2, k)) === 72 && sheetOf(st.get(num2, k + 1)) === 72))
555	            && inTileBounds(num2, k + 1, reach.x0, reach.y0, reach.x1, reach.y1); k++) { /* 下到底 */ }
556	        }
557	        const w = toWorld({ x: num2, y: k });
558	        const d = dist(w.x, w.y, env.mouse.x, env.mouse.y);
559	        if (best === -1 || d < best) { best = d; bx = num2; by = k; } // :2681-2687
560	      }
561	    }
562	    if (bx !== -1) set(bx, by);
563	  }
564	
565	  /** :2229-2268 ForceCursor：鼠标格自身可挖（非实心/平台）且工具门通过 → 钉鼠标格 */
566	  private stepForceCursor(
567	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region, screenX: number, screenY: number,
568	    set: (x: number, y: number) => void, taken: () => boolean,
569	  ): void {
570	    if (taken()) return;
571	    const st = env.st;
572	    const x = Math.floor(env.mouse.x / 16), y = Math.floor(env.mouse.y / 16);
573	    if (!inTileBounds(x, y, reach.x0, reach.y0, reach.x1, reach.y1)) return;
574	    const t = st.get(x, y);
575	    const sheet = sheetOf(t);
576	    let flag = activeAt(st, x, y) && canKillTile(t) && (!tileSolidType(t) || tileSolidTopType(t)); // :2249
577	    if (flag && tileAxeType(t) && sem.axe < 1) flag = false;      // :2250-2253
578	    if (flag && isHammerTile(sheet) && sem.hammer < 1) flag = false; // :2254-2257
579	    if (flag && !isHammerTile(sheet) && !tileAxeType(t) && sem.pick < 1) flag = false; // :2258-2261
580	    if (flag) set(x, y);
581	  }
582	
583	  /** :2270-2348 MineShinies：优先级表（12 火把 / 639 / 665）全扫取离鼠标最近 */
584	  private stepMineShinies(
585	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
586	    set: (x: number, y: number) => void, taken: () => boolean,
587	  ): void {
588	    if (sem.pick <= 0 || taken()) return; // :2280
589	    const st = env.st;
590	    const targets: Pt[] = [];
591	    for (let i = reach.x0; i <= reach.x1; i++) {
592	      for (let j = reach.y0; j <= reach.y1; j++) {
593	        if (!activeAt(st, i, j)) continue;
594	        const sheet = sheetOf(st.get(i, j));
595	        if ((PICKAXE_PRIORITY_OVERRIDE[sheet] ?? 0) > 0) targets.push({ x: i, y: j }); // :2304-2312
596	      }
597	    }
598	    // :2315-2327（反编译此处 _targets2 为空集——保留最高优先级过滤语义：本表全为 1，无过滤）
599	    let maxPri = 0;
600	    for (const t of targets) maxPri = Math.max(maxPri, PICKAXE_PRIORITY_OVERRIDE[sheetOf(st.get(t.x, t.y))] ?? 0);
601	    const filtered = targets.filter((t) => (PICKAXE_PRIORITY_OVERRIDE[sheetOf(st.get(t.x, t.y))] ?? 0) >= maxPri);
602	    const point = nearestOf(filtered, env.mouse);
603	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
604	      set(point.x, point.y); // :2341-2345
605	    }
606	  }
607	
608	  /** :2350-2580 MineSolids：3:1 方向归约 → 玩家前缘列 ↔ 鼠标端点逐对射线 → 择近 */
609	  private stepMineSolids(
610	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
611	    set: (x: number, y: number) => void, taken: () => boolean,
612	  ): void {
613	    if (sem.pick <= 0 || taken()) return; // :2355
614	    const st = env.st;
615	    const p = env.actor;
616	    const gravDir = 1;
617	    let mouse = { ...env.mouse };
618	    // :2369-2381 3:1 方向归约（|vx|>3|vy| 纯水平等）
619	    let vector = { x: mouse.x - p.cx, y: mouse.y - p.cy };
620	    let signX = Math.sign(vector.x);
621	    let signY = Math.sign(vector.y);
622	    if (Math.abs(vector.x) > Math.abs(vector.y) * 3) { signY = 0; mouse.y = p.cy; }
623	    if (Math.abs(vector.y) > Math.abs(vector.x) * 3) { signX = 0; mouse.x = p.cx; }
624	    void vector;
625	    const points: Pt[] = [];
626	    const endpoints: Pt[] = [];
627	    const num3 = (signY === -1 && signX !== 0) ? -1 : 1; // :2386-2390
628	    // :2391-2396 玩家前缘列 / 起始行
629	    const num4 = Math.floor((p.x + (p.w / 2) + ((p.w / 2 - 1) * signX)) / 16);
630	    let num5 = Math.floor((p.y + 0.1) / 16);
631	    if (num3 === -1) num5 = Math.floor((p.y + p.h - 1) / 16);
632	    const num6 = Math.floor(p.w / 16) + (p.w % 16 !== 0 ? 1 : 0);
633	    const num7 = Math.floor(p.h / 16) + (p.h % 16 !== 0 ? 1 : 0);
634	    // :2399-2418 起点集（前缘列 + 必要时底/顶行展开）
635	    if (signX !== 0) {
636	      for (let i = 0; i < num7; i++) {
637	        if (st.inBounds(num4, num5 + i * num3)) points.push({ x: num4, y: num5 + i * num3 });
638	      }
639	    }
640	    if (signY !== 0) {
641	      for (let j = 0; j < num6; j++) {
642	        const x = Math.floor(p.x / 16) + j;
643	        if (st.inBounds(x, num5)) points.push({ x, y: num5 });
644	      }
645	    }
646	    // :2419-2432 鼠标端点（假想玩家前缘/边缘展开）
647	    const num8 = Math.floor((mouse.x + ((p.w / 2 - 1) * signX)) / 16);
648	    let num9 = Math.floor((mouse.y + 0.1 - (p.h / 2 + 1)) / 16);
649	    if (num3 === -1) num9 = Math.floor((mouse.y + (p.h / 2) - 1) / 16);
650	    if (gravDir === 1 && signX === 0) num9++;
651	    if (num9 < 10) num9 = 10;
652	    if (num9 > st.h - 10) num9 = st.h - 10;
653	    const num10 = Math.floor(p.w / 16) + (p.w % 16 !== 0 ? 1 : 0);
654	    const num11 = Math.floor(p.h / 16) + (p.h % 16 !== 0 ? 1 : 0);
655	    if (num8 >= 40 && num9 >= 40 && num8 < st.w - 40 && num9 < st.h - 40) { // WorldGen.InWorld(,40)
656	      if (signX !== 0) {
657	        for (let k = 0; k < num11; k++) {
658	          if (st.inBounds(num8, num9 + k * num3)) endpoints.push({ x: num8, y: num9 + k * num3 });
659	        }
660	      }
661	      if (signY !== 0) {
662	        for (let l = 0; l < num10; l++) {
663	          const x = Math.floor((mouse.x - p.w / 2) / 16) + l;
664	          if (st.inBounds(x, num9)) endpoints.push({ x, y: num9 });
665	        }
666	      }
667	    }
668	    // :2466-2488 逐对射线。钩爪锚点集合（SmartCursorHelper.cs:61-165 顶部 _grappleTargets，
669	    // 由 SmartCursorLookup :73-80 从 player 现役钩爪弹幕收集）依赖钩爪系统未实装——
670	    // 等价语义 = 空集（原版无钩爪时同样为空，行为一致；实装后补收集即可）。
671	    const grappleTargets: Pt[] = [];
672	    const targets: Pt[] = [];
673	    let pi = 0;
674	    while (pi < points.length && endpoints.length > 0) {
675	      const item = points[pi];
676	      const item2 = endpoints[0];
677	      const r = hitLine(st, item.x, item.y, item2.x, item2.y, signX * gravDir, -signY * gravDir, grappleTargets);
678	      if (!r.hit) { pi++; endpoints.shift(); continue; }
679	      if (r.col.x !== item2.x || r.col.y !== item2.y) targets.push(r.col);
680	      const t = st.get(r.col.x, r.col.y);
681	      if (!inActiveAt(st, r.col.x, r.col.y) && activeAt(st, r.col.x, r.col.y)
682	        && tileSolidType(t) && !tileSolidTopType(t)) {
683	        targets.push(r.col); // :2482-2485
684	      }
685	      pi++;
686	      endpoints.shift();
687	    }
688	    // :2489-2501 CanKillTile 过滤（不查镐力）
689	    const killable = targets.filter((t) => canKillTile(st.get(t.x, t.y)));
690	    if (killable.length > 0) {
691	      // :2502-2576 择近 = 格中心+8px 到玩家 Center（单人无联机偏移）
692	      let best = -1;
693	      let point = killable[0];
694	      for (const t of killable) {
695	        const w = toWorld(t);
696	        const d = dist(w.x, w.y, p.cx, p.cy);
697	        if (best === -1 || d < best) { best = d; point = t; }
698	      }
699	      if (inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
700	        set(point.x, point.y);
701	      }
702	    }
703	  }
704	
705	  /** :1879-2030 彩色扳手（红 509/蓝 850/绿 851/黄 3612）：延伸已有同色导线断点一格 */
706	  private stepColoredWrenches(
707	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region, screenX: number, screenY: number,
708	    set: (x: number, y: number) => void, taken: () => boolean,
709	  ): void {
710	    const vid = sem.vid;
711	    if (vid == null || ![509, 850, 851, 3612].includes(vid) || taken()) return; // :1881
712	    const st = env.st;
713	    // :1886-1902 颜色档：509红(1)/850蓝(2)/851绿(3)/3612黄(4)
714	    const num = vid === 509 ? 1 : vid === 850 ? 2 : vid === 851 ? 3 : 4;
715	    const wireBit = num === 1 ? TS.WIRE_RED : num === 2 ? TS.WIRE_BLUE : num === 3 ? TS.WIRE_GREEN : TS.WIRE_YELLOW;
716	    // :1903-1919 鼠标格已有同色线 → 让位（原版 flag=true 时不产生目标）
717	    const hoverWire = st.inBounds(screenX, screenY) ? st.wire[st.idx(screenX, screenY)] : 0;
718	    if ((hoverWire & wireBit) !== 0) return;
719	    const targets: Pt[] = [];
720	    for (let i = reach.x0; i <= reach.x1; i++) {
721	      for (let j = reach.y0; j <= reach.y1; j++) {
722	        if (!st.inBounds(i, j)) continue;
723	        if ((st.wire[st.idx(i, j)] & wireBit) === 0) continue;
724	        // :1931-2006 四向断点延伸
725	        for (const [ox, oy] of [[-1, 0], [1, 0], [0, -1], [0, 1]] as const) {
726	          const nx = i + ox, ny = j + oy;
727	          if (!st.inBounds(nx, ny)) continue;
728	          if ((st.wire[st.idx(nx, ny)] & wireBit) === 0) targets.push({ x: nx, y: ny });
729	        }
730	      }
731	    }
732	    const point = nearestOf(targets, env.mouse);
733	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
734	      set(point.x, point.y);
735	    }
736	  }
737	
738	  /** :1724-1877 多彩扳手（3625）：按当前工具模式延伸/剪除 */
739	  private stepMulticolorWrench(
740	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region, screenX: number, screenY: number,
741	    set: (x: number, y: number) => void, taken: () => boolean,
742	  ): void {
743	    if (sem.vid !== 3625 || taken()) return; // :1726
744	    const st = env.st;
745	    const toolMode = env.wireToolMode; // WiresUI.Settings.ToolMode（Game.wireToolMode）
746	    const bits: Array<[boolean, number]> = [
747	      [(toolMode & 1) !== 0, TS.WIRE_RED],
748	      [(toolMode & 2) !== 0, TS.WIRE_BLUE],
749	      [(toolMode & 4) !== 0, TS.WIRE_GREEN],
750	      [(toolMode & 8) !== 0, TS.WIRE_YELLOW],
751	    ];
752	    const cutter = (toolMode & 32) !== 0;
753	    // :1733-1750 鼠标格已有线组合 == 工具模式（去 Cutter 位）→ 让位
754	    const hoverWire = st.inBounds(screenX, screenY) ? st.wire[st.idx(screenX, screenY)] : 0;
755	    let mouseMode = 0;
756	    if (hoverWire & TS.WIRE_RED) mouseMode |= 1;
757	    if (hoverWire & TS.WIRE_BLUE) mouseMode |= 2;
758	    if (hoverWire & TS.WIRE_GREEN) mouseMode |= 4;
759	    if (hoverWire & TS.WIRE_YELLOW) mouseMode |= 8;
760	    if ((toolMode & ~32) === mouseMode) return;
761	    const targets: Pt[] = [];
762	    for (let i = reach.x0; i <= reach.x1; i++) {
763	      for (let j = reach.y0; j <= reach.y1; j++) {
764	        if (!st.inBounds(i, j)) continue;
765	        const w = st.wire[st.idx(i, j)];
766	        if (cutter) {
767	          // :1764-1770 剪线模式：已选色有线的格都是目标
768	          for (const [on, bit] of bits) if (on && (w & bit) !== 0) { targets.push({ x: i, y: j }); break; }
769	        } else {
770	          // :1772-1853 铺线模式：延伸每色断点一格
771	          let any = false;
772	          for (const [on, bit] of bits) if (on && (w & bit) !== 0) { any = true; break; }
773	          if (!any) continue;
774	          for (const [on, bit] of bits) {
775	            if (!on) continue;
776	            for (const [ox, oy] of [[-1, 0], [1, 0], [0, -1], [0, 1]] as const) {
777	              const nx = i + ox, ny = j + oy;
778	              if (!st.inBounds(nx, ny)) continue;
779	              if ((st.wire[st.idx(nx, ny)] & bit) === 0) targets.push({ x: nx, y: ny });
780	            }
781	          }
782	        }
783	      }
784	    }
785	    const point = nearestOf(targets, env.mouse);
786	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
787	      set(point.x, point.y);
788	    }
789	  }
790	
791	  /** :1536-1723 锤：两段。第一段 :1587-1677 逐对 HitLineWall 射线取离玩家 Center 最近
792	   *  （剔除祭坛 26，:1657-1672）；第二段 :1683-1721 射线无果时全扫可达区内可锤墙
793	   *  （HitWallSubstep），取离鼠标最近——这是原版既定回退，不是近似。
794	   *  player.poundRelease=false 的副作用（:1674/:1717）属 Player 锤击状态机，
795	   *  本类不承载，由挖掘路径按 poundRelease 语义自理。 */
796	  private stepHammers(
797	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
798	    set: (x: number, y: number) => void, taken: () => boolean,
799	  ): void {
800	    if (sem.hammer <= 0 || taken()) return; // :1540/:1683
801	    const st = env.st;
802	    const p = env.actor;
803	    let mouse = { ...env.mouse };
804	    // :1542-1554 3:1 方向归约（同 MineSolids）
805	    const vector = { x: mouse.x - p.cx, y: mouse.y - p.cy };
806	    let signX = Math.sign(vector.x);
807	    let signY = Math.sign(vector.y);
808	    if (Math.abs(vector.x) > Math.abs(vector.y) * 3) { signY = 0; mouse.y = p.cy; }
809	    if (Math.abs(vector.y) > Math.abs(vector.x) * 3) { signX = 0; mouse.x = p.cx; }
810	    const num3 = (signY === -1 && signX !== 0) ? -1 : 1;
811	    const points: Pt[] = [], endpoints: Pt[] = [];
812	    const num4 = Math.floor((p.x + (p.w / 2) + ((p.w / 2 - 1) * signX)) / 16);
813	    let num5 = Math.floor((p.y + 0.1) / 16);
814	    if (num3 === -1) num5 = Math.floor((p.y + p.h - 1) / 16);
815	    const num6 = Math.floor(p.w / 16) + (p.w % 16 !== 0 ? 1 : 0);
816	    const num7 = Math.floor(p.h / 16) + (p.h % 16 !== 0 ? 1 : 0);
817	    if (signX !== 0) for (let i = 0; i < num7; i++) if (st.inBounds(num4, num5 + i * num3)) points.push({ x: num4, y: num5 + i * num3 });
818	    if (signY !== 0) for (let j = 0; j < num6; j++) { const x = Math.floor(p.x / 16) + j; if (st.inBounds(x, num5)) points.push({ x, y: num5 }); }
819	    const num8 = Math.floor((mouse.x + ((p.w / 2 - 1) * signX)) / 16);
820	    let num9 = Math.floor((mouse.y + 0.1 - (p.h / 2 + 1)) / 16);
821	    if (num3 === -1) num9 = Math.floor((mouse.y + (p.h / 2) - 1) / 16);
822	    num9 = Math.max(10, Math.min(num9, st.h - 10));
823	    const num10 = Math.floor(p.w / 16) + (p.w % 16 !== 0 ? 1 : 0);
824	    const num11 = Math.floor(p.h / 16) + (p.h % 16 !== 0 ? 1 : 0);
825	    if (signX !== 0) for (let k = 0; k < num11; k++) if (st.inBounds(num8, num9 + k * num3)) endpoints.push({ x: num8, y: num9 + k * num3 });
826	    if (signY !== 0) for (let l = 0; l < num10; l++) { const x = Math.floor((mouse.x - p.w / 2) / 16) + l; if (st.inBounds(x, num9)) endpoints.push({ x, y: num9 }); }
827	    // :1632-1655 逐对 HitLineWall（Collision.cs:1148）：(-1,-1) 双端出队续下一对；
828	    //  非终点命中先入 targets，再经 HitWallSubstep 复核入 targets（:1649-1652）
829	    const targets: Pt[] = [];
830	    let pi = 0;
831	    while (pi < points.length && endpoints.length > 0) {
832	      const a = points[pi], b = endpoints[0];
833	      const col = hitLineWall(st, a.x, a.y, b.x, b.y);
834	      if (col.x !== -1) {
835	        if (col.x !== b.x || col.y !== b.y) targets.push(col);
836	        if (hitWallSubstep(st, col.x, col.y)) targets.push(col);
837	      }
838	      pi++;
839	      endpoints.shift();
840	    }
841	    const pick = pickNonAltar(st, targets, (t) => toWorld(t), { x: p.cx, y: p.cy });
842	    if (pick && inTileBounds(pick.x, pick.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
843	      set(pick.x, pick.y);
844	      return;
845	    }
846	    // :1683-1721 原版回退段：全扫可达区可锤墙，取离鼠标最近（剔除祭坛 26）
847	    const targets2: Pt[] = [];
848	    for (let i = reach.x0; i <= reach.x1; i++) {
849	      for (let j = reach.y0; j <= reach.y1; j++) {
850	        if (!st.inBounds(i, j)) continue;
851	        if (st.wall[st.idx(i, j)] > 0 && hitWallSubstep(st, i, j)) targets2.push({ x: i, y: j });
852	      }
853	    }
854	    const pick2 = pickNonAltar(st, targets2, (t) => toWorld(t), env.mouse);
855	    if (pick2 && inTileBounds(pick2.x, pick2.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
856	      set(pick2.x, pick2.y);
857	    }
858	  }
859	
860	  /** :1494-1534 致动魔杖（3620）：已装致动器的实心格取最近 */
861	  private stepActuationRod(
862	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
863	    set: (x: number, y: number) => void, taken: () => boolean,
864	  ): void {
865	    if (sem.vid !== 3620 || taken()) return;
866	    const st = env.st;
867	    const targets: Pt[] = [];
868	    for (let i = reach.x0; i <= reach.x1; i++) {
869	      for (let j = reach.y0; j <= reach.y1; j++) {
870	        if (!st.inBounds(i, j)) continue;
871	        const w = st.wire[st.idx(i, j)];
872	        if (activeAt(st, i, j) && (w & TS.WIRE_ACTUATOR) !== 0) targets.push({ x: i, y: j }); // :1508
873	      }
874	    }
875	    const point = nearestOf(targets, env.mouse);
876	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
877	  }
878	
879	  /** :1454-1492 剪线钳（510）：任何导线/致动器格取最近 */
880	  private stepWireCutter(
881	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
882	    set: (x: number, y: number) => void, taken: () => boolean,
883	  ): void {
884	    if (sem.vid !== 510 || taken()) return;
885	    const st = env.st;
886	    const targets: Pt[] = [];
887	    for (let i = reach.x0; i <= reach.x1; i++) {
888	      for (let j = reach.y0; j <= reach.y1; j++) {
889	        if (!st.inBounds(i, j)) continue;
890	        if (st.wire[st.idx(i, j)] & 31) targets.push({ x: i, y: j }); // :1466 四色线或致动器
891	      }
892	    }
893	    const point = nearestOf(targets, env.mouse);
894	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
895	  }
896	
897	  /** :1323-1388 平台：已有平台边缘沿八方向续一格；写方向锁/连通锁 */
898	  private stepPlatforms(
899	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region, screenX: number, screenY: number,
900	    set: (x: number, y: number) => void, taken: () => boolean,
901	  ): void {
902	    const createSheet = sem.createTileSheet;
903	    if (createSheet == null || !PLATFORMS.has(createSheet) || taken()) return; // :1325
904	    const st = env.st;
905	    if (isPlatformSheet(st, screenX, screenY)) return; // 鼠标已在平台上不动
906	    const targets: Pt[] = [];
907	    const points: Pt[] = [];
908	    for (let i = reach.x0; i <= reach.x1; i++) {
909	      for (let j = reach.y0; j <= reach.y1; j++) {
910	        if (!st.inBounds(i, j)) continue;
911	        // :1335 鼠标指向该格的八方向量化
912	        const dir = this.getDesiredDirectionFrom({ x: env.mouse.x - (i * 16 + 8), y: env.mouse.y - (j * 16 + 8) });
913	        let flag = !isPlatformSheet(st, i, j); // :1336
914	        // :1337-1340 该格非实心且左右已有平台 → 不作为续铺源
915	        if (!flag && dir.y === 0 && activeAt(st, i, j) && !solidTile(st, i, j)
916	          && (isPlatformSheet(st, i - 1, j) || isPlatformSheet(st, i + 1, j))) {
917	          flag = false;
918	        }
919	        if (flag) continue;
920	        // :1345 对角规则映射 slope（1=右上 2=右下 等：dx==dy→2、dx==-dy→1）
921	        const slopeKind = dir.x === dir.y ? 2 : dir.x === -dir.y ? 1 : 0;
922	        if ((slopeKind === 0 || st.slope[st.idx(i, j)] !== slopeKind)
923	          && (dir.x !== 0 || (!isPlatformSheet(st, i - 1, j + dir.y) && !isPlatformSheet(st, i + 1, j + dir.y)))) {
924	          const nx = i + dir.x, ny = j + dir.y;
925	          if (!st.inBounds(nx, ny)) continue;
926	          const nt = st.get(nx, ny);
927	          if ((!activeAt(st, nx, ny) || tileCutType(nt)) && this.allowedForContinuity(nx, ny, 2)) { // :1349
928	            targets.push({ x: nx, y: ny });
929	            points.push({ x: dir.x, y: dir.y });
930	          }
931	        }
932	      }
933	    }
934	    if (targets.length === 0) return;
935	    // :1359-1377 离鼠标最近，并列时取"沿锁定方向投影更大"
936	    let num2 = -1, num3 = -1;
937	    let point = targets[0], point2 = points[0];
938	    for (let k = 0; k < targets.length; k++) {
939	      const t = targets[k], d = points[k];
940	      const vx = env.mouse.x - (t.x * 16 + 8), vy = env.mouse.y - (t.y * 16 + 8);
941	      const len = Math.hypot(vx, vy);
942	      const dot = vx * d.x + vy * d.y;
943	      if (num2 === -1 || len < num2 || (len === num2 && dot > num3)) {
944	        num2 = len; num3 = dot; point = t; point2 = d;
945	      }
946	    }
947	    if (inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
948	      set(point.x, point.y);
949	      this.lockedDirection = { x: point2.x, y: point2.y };   // :1382
950	      this.lockedContinuity = { x: point.x, y: point.y };    // :1383
951	    }
952	  }
953	
954	  /** :1403-1428 AllowedForContinuity：目标须与连通锁重合或在锁方向步进可达 */
955	  private allowedForContinuity(x: number, y: number, skipsAllowed: number): boolean {
956	    const lock = this.lockedContinuity;
957	    if (!lock) return true;
958	    let cx = lock.x, cy = lock.y;
959	    if (x === cx && y === cy) return true;
960	    const dir = this.lockedDirection;
961	    if (!dir) return false;
962	    for (let i = 0; i < skipsAllowed; i++) {
963	      cx += dir.x; cy += dir.y;
964	      if (x === cx && y === cy) return true;
965	    }
966	    return false;
967	  }
968	
969	  /** :1430-1443 八方向量化（锁定方向优先） */
970	  getDesiredDirectionFrom(offset: { x: number; y: number }): Pt {
971	    if (this.lockedDirection) return this.lockedDirection;
972	    let num = Math.atan2(offset.y, offset.x);
973	    if (num < 0) num += Math.PI * 2;
974	    const step = Math.PI / 4;
975	    const ang = Math.floor(((num + step / 2) % (Math.PI * 2)) / step) * step;
976	    // || 0 归一化 -0（cos(π/2) 浮点残尾 trunc 后会是 -0）
977	    return { x: Math.trunc(Math.cos(ang) * 1.5) || 0, y: Math.trunc(Math.sin(ang) * 1.5) || 0 };
978	  }
979	
980	  /** :1165-1321 矿车轨道（2340/2739 主 + 2492 压力轨道段） */
981	  private stepMinecartTracks(
982	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region, screenX: number, screenY: number,
983	    set: (x: number, y: number) => void, taken: () => boolean,
984	  ): void {
985	    const st = env.st;
986	    const p = env.actor;
987	    // 原版按物品 id 2340/2739 门；我方轨道放置物（place_v_314_*）无 vid → 以 createTile sheet==314 认定
988	    const isTrackItem = sem.createTileSheet === 314 || sem.vid === 2340 || sem.vid === 2739 || sem.vid === 2492;
989	    if (isTrackItem && !taken()) {
990	      // :1170-1196 主方向判定（±0.5 阈值；斜向组合时水平让位）
991	      const dx = env.mouse.x - p.cx, dy = env.mouse.y - p.cy;
992	      const len = Math.hypot(dx, dy) || 1;
993	      const upDot = -dy / len;
994	      const up = upDot >= 0.5, down = upDot <= -0.5;
995	      const rightDot = dx / len;
996	      let right = rightDot >= 0.5, left = rightDot <= -0.5;
997	      const upLeft = up && left, upRight = up && right, downLeft = down && left, downRight = down && right;
998	      if (upLeft || downLeft) left = false;
999	      if (upRight || downRight) right = false;
1000	      // :1197-1201 鼠标格已在轨道上 → 不动
1001	      const hoverSheet = sheetOf(st.get(screenX, screenY));
1002	      if (hoverSheet !== 314) {
1003	        const targets: Pt[] = [];
1004	        for (let i = reach.x0; i <= reach.x1; i++) {
1005	          for (let j = reach.y0; j <= reach.y1; j++) {
1006	            if (!st.inBounds(i, j) || sheetOf(st.get(i, j)) !== 314) continue;
1007	            const diag = (ox: number, oy: number): boolean => st.inBounds(i + ox, j + oy) && sheetOf(st.get(i + ox, j + oy)) === 314;
1008	            const open = (x: number, y: number): boolean => {
1009	              if (!st.inBounds(x, y)) return false;
1010	              const t = st.get(x, y);
1011	              return !activeAt(st, x, y) || tileCutType(t);
1012	            };
1013	            // :1215-1238 六方向延伸（斜向带让位规则）
1014	            if (upLeft && open(i - 1, j - 1) && !(!diag(1, 1) && diag(1, -1)) && !diag(-1, 1)) targets.push({ x: i - 1, y: j - 1 });
1015	            if (left && open(i - 1, j)) targets.push({ x: i - 1, y: j });
1016	            if (downLeft && open(i - 1, j + 1) && !(!diag(1, -1) && diag(1, 1)) && !diag(-1, -1)) targets.push({ x: i - 1, y: j + 1 });
1017	            if (upRight && open(i + 1, j - 1) && !(!diag(-1, 1) && diag(-1, -1)) && !diag(1, 1)) targets.push({ x: i + 1, y: j - 1 });
1018	            if (right && open(i + 1, j)) targets.push({ x: i + 1, y: j });
1019	            if (downRight && open(i + 1, j + 1) && !(!diag(-1, -1) && diag(-1, 1)) && !diag(1, -1)) targets.push({ x: i + 1, y: j + 1 });
1020	          }
1021	        }
1022	        // :1243-1258 目标上下不可再连轨道（端点）才入选，取离鼠标最近
1023	        const ends = targets.filter((t) => {
1024	          const above = st.inBounds(t.x, t.y - 1) && sheetOf(st.get(t.x, t.y - 1)) === 314;
1025	          const below = st.inBounds(t.x, t.y + 1) && sheetOf(st.get(t.x, t.y + 1)) === 314;
1026	          return !above && !below;
1027	        });
1028	        const point = nearestOf(ends, env.mouse);
1029	        if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
1030	          set(point.x, point.y);
1031	          return;
1032	        }
1033	      }
1034	    }
1035	    // :1267-1321 压力轨道（2492）：左右各续一格——我方无该物品的独立数据段，
1036	    // 已并入上面 sheet==314 的通用延伸（2492 命中 isTrackItem 同走主段）
1037	  }
1038	
1039	  /** :1099-1163 铺墙：可铺墙格四向有依附，取最近 */
1040	  private stepWalls(
1041	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1042	    set: (x: number, y: number) => void, taken: () => boolean,
1043	  ): void {
1044	    if ((sem.createWall ?? 0) <= 0 || taken()) return; // :1103
1045	    const st = env.st;
1046	    const targets: Pt[] = [];
1047	    for (let i = reach.x0; i <= reach.x1; i++) {
1048	      for (let j = reach.y0; j <= reach.y1; j++) {
1049	        if (!st.inBounds(i, j)) continue;
1050	        const ii = st.idx(i, j);
1051	        const t = st.type[ii];
1052	        // :1113 本格无墙且（空 / 非实心 / 平台）且与玩家视线可通
1053	        //  （Collision.CanHitWithCheck + NotDoorStand，Collision.cs:492-589 / DelegateMethods.cs:858-869）
1054	        if (st.wall[ii] === 0 && (!activeAt(st, i, j) || !tileSolidType(t) || tileSolidTopType(t))
1055	          && canHitWithCheck(st, env.actor, env.actor.w, env.actor.h,
1056	            { x: i * 16, y: j * 16 }, 16, 16, (x, y) => notDoorStand(st, x, y))) {
1057	          let flag = false;
1058	          // :1115-1131 四向有 active tile 或已有墙 → 可依附
1059	          for (const [ox, oy] of [[-1, 0], [1, 0], [0, -1], [0, 1]] as const) {
1060	            const nx = i + ox, ny = j + oy;
1061	            if (!st.inBounds(nx, ny)) continue;
1062	            const ni = st.idx(nx, ny);
1063	            if (activeAt(st, nx, ny) || st.wall[ni] > 0) { flag = true; break; }
1064	          }
1065	          // :1137-1140 开门锚帧格（WorldGen.IsOpenDoorAnchorFrame）不可铺墙
1066	          if (isOpenDoorAnchorFrame(st, i, j)) flag = false;
1067	          if (flag) targets.push({ x: i, y: j });
1068	        }
1069	      }
1070	    }
1071	    const point = nearestOf(targets, env.mouse);
1072	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1073	  }
1074	
1075	  /** :1026-1097 南瓜种子（createTile 254） */
1076	  private stepPumpkinSeeds(
1077	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1078	    set: (x: number, y: number) => void, taken: () => boolean,
1079	  ): void {
1080	    if (sem.createTileSheet !== 254 || taken()) return;
1081	    pumpkinOrBoulderScan(env, reach, set, (st, i, j) => {
1082	      // :1043-1070 草面 2 格宽、无坡无半砖、上方 2×2 无阻挡
1083	      const a = st.inBounds(i, j + 1) ? st.get(i, j + 1) : 0;
1084	      const b = st.inBounds(i + 1, j + 1) ? st.get(i + 1, j + 1) : 0;
1085	      if (!activeAt(st, i, j + 1) || !activeAt(st, i + 1, j + 1)) return false;
1086	      const grassOk = (t: number): boolean => [2, 477, 109, 492].includes(sheetOf(t));
1087	      if (!grassOk(a) || !grassOk(b)) return false;
1088	      for (let k = i; k <= i + 1; k++) {
1089	        for (let l = j - 1; l <= j; l++) {
1090	          if (!st.inBounds(k, l)) return false;
1091	          const t = st.get(k, l);
1092	          if (activeAt(st, k, l) && (tileSolidType(t) || !tileCutType(t))) return false;
1093	        }
1094	      }
1095	      return true;
1096	    });
1097	  }
1098	
1099	  /** :256-322 草地种子（ItemID.Sets.GrassSeeds） */
1100	  private stepGrassSeeds(
1101	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1102	    set: (x: number, y: number) => void, taken: () => boolean,
1103	  ): void {
1104	    const vid = sem.vid;
1105	    if (vid == null || !GRASS_SEED_ITEMS.has(vid) || taken()) return;
1106	    const st = env.st;
1107	    const targets: Pt[] = [];
1108	    for (let i = reach.x0; i <= reach.x1; i++) {
1109	      for (let j = reach.y0; j <= reach.y1; j++) {
1110	        if (!st.inBounds(i, j)) continue;
1111	        // :273-274 八向至少一格暴露；:323 须 active 且未被致动（nactive）
1112	        if (!activeAt(st, i, j) || inActiveAt(st, i, j) || !exposed8(st, i, j)) continue;
1113	        const sheet = sheetOf(st.get(i, j));
1114	        // :278-294 各种子适配的基底
1115	        let ok = false;
1116	        switch (vid) {
1117	          default: ok = sheet === 0; break;                      // 普通草种：泥土
1118	          case 59: case 2171: ok = sheet === 0 || sheet === 59; break; // 丛林草种
1119	          case 194: case 195: ok = sheet === 59; break;
1120	          case 5214: ok = sheet === 57; break;
1121	        }
1122	        if (ok) targets.push({ x: i, y: j });
1123	      }
1124	    }
1125	    const point = nearestOf(targets, env.mouse);
1126	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1127	  }
1128	
1129	  /** :324-369 苔藓（ItemID.Sets.Moss）：暴露的石/泥灰岩面 */
1130	  private stepMoss(
1131	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1132	    set: (x: number, y: number) => void, taken: () => boolean,
1133	  ): void {
1134	    const vid = sem.vid;
1135	    if (vid == null || !MOSS_ITEMS.has(vid) || taken()) return;
1136	    const st = env.st;
1137	    const targets: Pt[] = [];
1138	    for (let i = reach.x0; i <= reach.x1; i++) {
1139	      for (let j = reach.y0; j <= reach.y1; j++) {
1140	        if (!st.inBounds(i, j)) continue;
1141	        const sheet = sheetOf(st.get(i, j));
1142	        if (!activeAt(st, i, j) || inActiveAt(st, i, j)) continue;
1143	        if (!exposed8(st, i, j)) continue; // :341-342
1144	        // :343 原版谓词 `tile.type == 1 || tile.type == 38`（石 / 苔石）照搬
1145	        if (sheet === 1 || sheet === 38) targets.push({ x: i, y: j });
1146	      }
1147	    }
1148	    const point = nearestOf(targets, env.mouse);
1149	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1150	  }
1151	
1152	  /** :968-1024 皮纳塔（createTile 454） */
1153	  private stepPigronata(
1154	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1155	    set: (x: number, y: number) => void, taken: () => boolean,
1156	  ): void {
1157	    if (sem.createTileSheet !== 454 || taken()) return;
1158	    const st = env.st;
1159	    const targets: Pt[] = [];
1160	    for (let i = reach.x0; i <= reach.x1; i++) {
1161	      for (let j = reach.y0; j <= reach.y1; j++) {
1162	        if (!st.inBounds(i, j)) continue;
1163	        // :979-1002 顶部一行实心 + 下方 4×3 空
1164	        let flag = true;
1165	        for (let k = i - 2; k <= i + 1; k++) {
1166	          for (let l = j - 1; l <= j + 2; l++) {
1167	            if (!st.inBounds(k, l)) { flag = false; continue; }
1168	            const t = st.get(k, l);
1169	            if (l === j - 1) {
1170	              if (!solidTile(st, k, l)) flag = false;
1171	            } else if (activeAt(st, k, l) && (!tileCutType(t) || sheetOf(t) === 454)) {
1172	              flag = false;
1173	            }
1174	          }
1175	        }
1176	        if (flag) targets.push({ x: i, y: j });
1177	      }
1178	    }
1179	    const point = nearestOf(targets, env.mouse);
1180	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1181	  }
1182	
1183	  /** :885-966 巨石（TileID.Sets.Boulders） */
1184	  private stepBoulders(
1185	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1186	    set: (x: number, y: number) => void, taken: () => boolean,
1187	  ): void {
1188	    const cs = sem.createTileSheet;
1189	    if (cs == null || !BOULDERS.has(cs) || taken()) return;
1190	    pumpkinOrBoulderScan(env, reach, set, (st, i, j) => {
1191	      // :898-925 下方两格 nactive 无坡无半砖、可承重、上方 2×2 无阻挡
1192	      for (const ox of [0, 1]) {
1193	        const bx = i + ox, by = j + 1;
1194	        if (!st.inBounds(bx, by) || !activeAt(st, bx, by)) return false;
1195	        const t = st.get(bx, by);
1196	        if (st.slope[st.idx(bx, by)] > 0 || st.half[st.idx(bx, by)] > 0) return false;
1197	        if (!tileSolidType(t) && !TILE_DEFS[t]) return false;
1198	      }
1199	      for (let k = i; k <= i + 1; k++) {
1200	        for (let l = j - 1; l <= j; l++) {
1201	          if (!st.inBounds(k, l)) return false;
1202	          const t = st.get(k, l);
1203	          if (activeAt(st, k, l) && !tileCutType(t)) return false;
1204	        }
1205	      }
1206	      return true;
1207	    });
1208	  }
1209	
1210	  /** :2795-2865 火把：合法锚位 + 17×17 去重 + 非水火把避液体，取离鼠标最近 */
1211	  private stepTorch(
1212	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1213	    set: (x: number, y: number) => void, taken: () => boolean,
1214	  ): void {
1215	    const vid = sem.vid;
1216	    const isTorch = (vid != null && TORCH_ITEMS.has(vid)) || sem.createTileSheet === 4; // 本地 'torch' 支已随退役移除(vi_8 走 vid)
1217	    if (!isTorch || taken()) return; // :2804
1218	    const st = env.st;
1219	    const notWaterTorch = vid == null || !WATER_TORCH_ITEMS.has(vid); // :2809
1220	    const targets: Pt[] = [];
1221	    for (let i = reach.x0; i <= reach.x1; i++) {
1222	      for (let j = reach.y0; j <= reach.y1; j++) {
1223	        if (!st.inBounds(i, j)) continue;
1224	        const ii = st.idx(i, j);
1225	        const t = st.type[ii];
1226	        // :2815 非水火把避液体；占位格须可替换：非 active、BreakableWhenPlacing、
1227	        //  或可割植物（82/83 药草除外）——TileID.cs:379 表
1228	        if (notWaterTorch && st.liquid[ii] > 0) continue;
1229	        if (activeAt(st, i, j) && !breakableWhenPlacing(sheetOf(t))
1230	          && (!tileCutType(t) || sheetOf(t) === 82 || sheetOf(t) === 83)) continue;
1231	        // :2819-2838 17×17 内已有火把 → 排除
1232	        let near = false;
1233	        outer: for (let k = i - 8; k <= i + 8; k++) {
1234	          for (let l = j - 8; l <= j + 8; l++) {
1235	            if (st.inBounds(k, l) && TORCH_TILES.has(sheetOf(st.get(k, l)))) { near = true; break outer; }
1236	          }
1237	        }
1238	        if (!near && isValidSpotForTorch(st, i, j)) targets.push({ x: i, y: j });
1239	      }
1240	    }
1241	    const point = nearestOf(targets, env.mouse);
1242	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1243	  }
1244	
1245	  /** :2895-2938 割草机（4049）：草/神圣草格取最近 */
1246	  private stepLawnMower(
1247	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1248	    set: (x: number, y: number) => void, taken: () => boolean,
1249	  ): void {
1250	    if (sem.vid !== 4049 || taken()) return;
1251	    const st = env.st;
1252	    const targets: Pt[] = [];
1253	    for (let i = reach.x0; i <= reach.x1; i++) {
1254	      for (let j = reach.y0; j <= reach.y1; j++) {
1255	        if (!st.inBounds(i, j)) continue;
1256	        const sheet = sheetOf(st.get(i, j));
1257	        if (activeAt(st, i, j) && (sheet === 2 || sheet === 109)) targets.push({ x: i, y: j });
1258	      }
1259	    }
1260	    const point = nearestOf(targets, env.mouse);
1261	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1262	  }
1263	
1264	  /** :2692-2793 方块填充（补洞）。注意原版门是"死代码"：第一道 :2694-2697
1265	   *  `if (!SmartBlocksEnabled) return;` 之后，第二道 :2714 的条件首项竟是
1266	   *  `SmartBlocksEnabled ||`（1.4.0.5/1.4.5.6 两个反编译口径一致）——即开关打开时
1267	   *  本策略恒不产生目标，只有 BlocksLines 生效。此处按 1:1 保留该门。 */
1268	  private stepBlocksFilling(
1269	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region, screenX: number, screenY: number,
1270	    set: (x: number, y: number) => void, taken: () => boolean,
1271	  ): void {
1272	    if (!env.settings.smartBlocksEnabled) return; // :2694-2697
1273	    if (taken()) return;
1274	    const cs = sem.createTileSheet;
1275	    // :2714 原版死门（见上）：SmartBlocksEnabled 为真即返回
1276	    if (env.settings.smartBlocksEnabled
1277	      || cs == null || !allowNormalBlockPlacement(sem) || !isSolidBlockSheet(cs)) return;
1278	    const st = env.st;
1279	    // :2716-2722 鼠标格已占用/不可达 → 停用
1280	    if (activeAt(st, screenX, screenY)) return;
1281	    if (!inTileBounds(screenX, screenY, reach.x0, reach.y0, reach.x1, reach.y1)) return;
1282	    const targets: Pt[] = [];
1283	    for (let i = reach.x0; i <= reach.x1; i++) {
1284	      for (let j = reach.y0; j <= reach.y1; j++) {
1285	        if (!st.inBounds(i, j)) continue;
1286	        const t = st.get(i, j);
1287	        if (!activeAt(st, i, j) || tileCutType(t) || breakableWhenPlacing(sheetOf(t))) {
1288	          // :2732-2749 四邻实心（非平台）计数 ≥2
1289	          let n = 0;
1290	          for (const [ox, oy] of [[-1, 0], [1, 0], [0, -1], [0, 1]] as const) {
1291	            const nx = i + ox, ny = j + oy;
1292	            if (!st.inBounds(nx, ny)) continue;
1293	            const nt = st.get(nx, ny);
1294	            if (activeAt(st, nx, ny) && tileSolidType(nt) && !tileSolidTopType(nt)) n++;
1295	          }
1296	          if (n >= 2) targets.push({ x: i, y: j });
1297	        }
1298	      }
1299	    }
1300	    if (targets.length === 0) return;
1301	    // :2759-2784 排序：先 |dx| 最小，并列取距离小（Collision.EmptyTile(ignoreTiles:true) 门）
1302	    let num2 = -1;
1303	    let num3 = Infinity;
1304	    let point = targets[0];
1305	    for (const t of targets) {
1306	      if (!emptyTile(env, t.x, t.y, true)) continue;
1307	      const vx = (t.x * 16 + 8) - env.mouse.x;
1308	      const vy = (t.y * 16 + 8) - env.mouse.y;
1309	      const adx = Math.abs(vx);
1310	      const len = Math.hypot(vx, vy);
1311	      let better = false;
1312	      if (adx < num3) better = true;
1313	      if (adx === num3 && (num2 === -1 || len < num2)) better = true;
1314	      if (better) { num2 = len; num3 = adx; point = t; }
1315	    }
1316	    if (num2 !== -1 && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
1317	      set(point.x, point.y); // :2786-2790
1318	    }
1319	  }
1320	
1321	  /** :809-883 方块铺线：四邻实心 ≥1，纯取最近 */
1322	  private stepBlocksLines(
1323	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region, screenX: number, screenY: number,
1324	    set: (x: number, y: number) => void, taken: () => boolean,
1325	  ): void {
1326	    if (!env.settings.smartBlocksEnabled) return; // :812
1327	    if (taken()) return;
1328	    const cs = sem.createTileSheet;
1329	    if (cs == null || !allowNormalBlockPlacement(sem) || !isSolidBlockSheet(cs)) return;
1330	    const st = env.st;
1331	    // :817-825 鼠标格已占用/不可达 → 停用
1332	    if (activeAt(st, screenX, screenY)) return;
1333	    if (!inTileBounds(screenX, screenY, reach.x0, reach.y0, reach.x1, reach.y1)) return;
1334	    const targets: Pt[] = [];
1335	    for (let i = reach.x0; i <= reach.x1; i++) {
1336	      for (let j = reach.y0; j <= reach.y1; j++) {
1337	        if (!st.inBounds(i, j)) continue;
1338	        const t = st.get(i, j);
1339	        if (!activeAt(st, i, j) || tileCutType(t) || breakableWhenPlacing(sheetOf(t))) {
1340	          // :835-851 四邻任一实心（非平台）
1341	          let ok = false;
1342	          for (const [ox, oy] of [[-1, 0], [1, 0], [0, -1], [0, 1]] as const) {
1343	            const nx = i + ox, ny = j + oy;
1344	            if (!st.inBounds(nx, ny)) continue;
1345	            const nt = st.get(nx, ny);
1346	            if (activeAt(st, nx, ny) && tileSolidType(nt) && !tileSolidTopType(nt)) { ok = true; break; }
1347	          }
1348	          if (ok) targets.push({ x: i, y: j });
1349	        }
1350	      }
1351	    }
1352	    // :860-876 EmptyTile 过滤后取最近
1353	    const open = targets.filter((t) => emptyTile(env, t.x, t.y));
1354	    const point = nearestOf(open, env.mouse);
1355	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1356	  }
1357	
1358	  // ---- 油漆三策略：依赖油漆系统（Tile.color / Tile.paintCoating / Main.tileColor）未建，
1359	  //      等价语义 = 目标集恒空（原版各策略以 tile.color != selectedColor 为扫描主条件，
1360	  //      无 color 数据则无候选）。恢复时机：接入 tile paint 通道后按下列行号补全 ----
1361	  //      Step_PaintRoller  :767-807（item 1072/1544，扫描 paint != 0）
1362	  //      Step_PaintBrush   :722-765（item 1071/1543，扫描 paint == 0）
1363	  //      Step_PaintScrapper:668-720（item 1100/1545，扫描 paint != 0）
1364	
1365	  /** :767-807 PaintRoller——no-op（见上：油漆系统依赖） */
1366	  private stepPaintRoller(
1367	    _env: SmartCursorEnv, sem: HeldSemantics, _reach: Region,
1368	    _set: (x: number, y: number) => void, _taken: () => boolean,
1369	  ): void {
1370	    void sem; void PAINT_ROLLER_ITEMS;
1371	  }
1372	
1373	  /** :722-765 PaintBrush——no-op（见上：油漆系统依赖） */
1374	  private stepPaintBrush(
1375	    _env: SmartCursorEnv, sem: HeldSemantics, _reach: Region,
1376	    _set: (x: number, y: number) => void, _taken: () => boolean,
1377	  ): void {
1378	    void sem; void PAINT_BRUSH_ITEMS;
1379	  }
1380	
1381	  /** :668-720 PaintScrapper——no-op（见上：油漆系统依赖） */
1382	  private stepPaintScrapper(
1383	    _env: SmartCursorEnv, sem: HeldSemantics, _reach: Region,
1384	    _set: (x: number, y: number) => void, _taken: () => boolean,
1385	  ): void {
1386	    void sem; void PAINT_SCRAPER_ITEMS;
1387	  }
1388	
1389	  /** :2032-2157 橡实（item 27）：草面 + 上方净空 + 相邻同类地面 */
1390	  private stepAcorns(
1391	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1392	    set: (x: number, y: number) => void, taken: () => boolean,
1393	  ): void {
1394	    if (sem.vid !== 27 || taken()) return; // :2037（reachableStartY<=20 的地表门由 reach 决定）
1395	    const st = env.st;
1396	    if (reach.y0 <= 20) return;
1397	    const NUM1 = 9, NUM2 = 14, NUM3 = 20; // :2034-2036
1398	    const targets: Pt[] = [];
1399	    for (let i = reach.x0; i <= reach.x1; i++) {
1400	      for (let j = reach.y0; j <= reach.y1; j++) {
1401	        if (!st.inBounds(i, j) || !st.inBounds(i, j - 1) || !st.inBounds(i, j + 1)) continue;
1402	        const t = st.get(i, j);
1403	        const below = st.get(i, j + 1);
1404	        // :2055 自身/上方须空（可割植物放行），下方须实心
1405	        if ((activeAt(st, i, j) && !tileCutType(t))
1406	          || (activeAt(st, i, j - 1) && !tileCutType(st.get(i, j - 1)))
1407	          || !activeAt(st, i, j + 1) || !solidTile2(st, i, j + 1)) continue;
1408	        // :2059-2060 ±1/±3 内已有树苗 → 间距门
1409	        const saplingAt = (x: number, y: number): boolean =>
1410	          st.inBounds(x, y) && activeAt(st, x, y) && COMMON_SAPLING.has(sheetOf(st.get(x, y)));
1411	        const flag = saplingAt(i - 1, j) || saplingAt(i + 1, j);
1412	        const flag2 = flag || saplingAt(i - 2, j) || saplingAt(i + 2, j) || saplingAt(i - 3, j) || saplingAt(i + 3, j);
1413	        const groundSheet = sheetOf(below);
1414	        let ok = false;
1415	        switch (groundSheet) {
1416	          case 60: // 丛林草：5×14 净空
1417	            if (!flag2 && emptyTileCheck(st, i - 2, i + 2, j - NUM2 + 1, j, 20)) ok = true;
1418	            break;
1419	          case 2: case 23: case 109: case 147: case 199: case 477: case 492: case 633: case 661: case 662:
1420	            if (!flag2 && st.liquid[st.idx(i - 1, j)] === 0 && st.liquid[st.idx(i, j)] === 0
1421	              && st.liquid[st.idx(i + 1, j)] === 0 && emptyTileCheck(st, i - 2, i + 2, j - NUM1 + 1, j, 20)) ok = true;
1422	            break;
1423	          case 53: case 112: case 116: case 234: // 沙族：棕榈
1424	            if (!flag && st.liquid[st.idx(i, j)] === 0 && emptyTileCheck(st, i, i, j - NUM3, j, 20)) ok = true;
1425	            break;
1426	        }
1427	        if (ok) targets.push({ x: i, y: j });
1428	      }
1429	    }
1430	    // :2096-2136 目标下方相邻列必须有同类地面（防孤点）
1431	    const kept = targets.filter((p) => {
1432	      let ok = false;
1433	      for (const l of [-1, 1]) {
1434	        const x = p.x + l, y = p.y + 1;
1435	        if (!st.inBounds(x, y) || !activeAt(st, x, y)) continue;
1436	        if ([2, 23, 53, 60, 109, 112, 116, 147, 199, 234, 477, 492, 633, 661, 662].includes(sheetOf(st.get(x, y)))) ok = true;
1437	      }
1438	      return ok;
1439	    });
1440	    const point = nearestOf(kept, env.mouse);
1441	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1442	  }
1443	
1444	  /** :2159-2226 宝石橡实（GrowTreeSettings 档案）：石/苔面 + 5×12 净空 */
1445	  private stepGemCorns(
1446	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1447	    set: (x: number, y: number) => void, taken: () => boolean,
1448	  ): void {
1449	    const profile = sem.vid != null ? GEM_TREE_PROFILES[sem.vid] : undefined;
1450	    if (!profile || taken()) return; // :2161
1451	    const st = env.st;
1452	    if (reach.y0 <= 20) return;
1453	    const targets: Pt[] = [];
1454	    const groundOk = (t: number): boolean => GEM_TREE_GROUND.has(sheetOf(t));
1455	    for (let i = reach.x0; i <= reach.x1; i++) {
1456	      for (let j = reach.y0; j <= reach.y1; j++) {
1457	        if (!st.inBounds(i, j)) continue;
1458	        const t = st.get(i, j);
1459	        const below = st.get(i, j + 1);
1460	        if (!groundOk(below) || !activeAt(st, i, j + 1) || !solidTile2(st, i, j + 1)) continue;
1461	        if (activeAt(st, i, j) && !tileCutType(t)) continue;
1462	        if (activeAt(st, i, j - 1) && !tileCutType(st.get(i, j - 1))) continue;
1463	        // :2179 ±3 内无树苗、无液体、5×TreeHeightMax 净空
1464	        let sapling = false;
1465	        for (const dx of [-3, -2, -1, 1, 2, 3]) {
1466	          const x = i + dx;
1467	          if (st.inBounds(x, j) && activeAt(st, x, j) && COMMON_SAPLING.has(sheetOf(st.get(x, j)))) sapling = true;
1468	        }
1469	        if (sapling) continue;
1470	        if (st.liquid[st.idx(i - 1, j)] !== 0 || st.liquid[st.idx(i, j)] !== 0 || st.liquid[st.idx(i + 1, j)] !== 0) continue;
1471	        if (!emptyTileCheck(st, i - 2, i + 2, j - profile.treeHeightMax, j, profile.saplingTile)) continue;
1472	        targets.push({ x: i, y: j });
1473	      }
1474	    }
1475	    // :2185-2205 相邻列须有同类地面
1476	    const kept = targets.filter((p) => {
1477	      for (const l of [-1, 1]) {
1478	        const x = p.x + l, y = p.y + 1;
1479	        if (st.inBounds(x, y) && activeAt(st, x, y) && groundOk(st.get(x, y))) return true;
1480	      }
1481	      return false;
1482	    });
1483	    const point = nearestOf(kept, env.mouse);
1484	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1485	  }
1486	
1487	  /** :612-666 空桶（205）：液体连通量 >100 的格（我方键 empty_bucket，vid 缺 → 键名兜底） */
1488	  private stepEmptyBuckets(
1489	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1490	    set: (x: number, y: number) => void, taken: () => boolean,
1491	  ): void {
1492	    const vid = sem.vid;
1493	    const isBucket = vid === 205;
1494	    if (!isBucket || taken()) return;
1495	    const st = env.st;
1496	    const targets: Pt[] = [];
1497	    for (let i = reach.x0; i <= reach.x1; i++) {
1498	      for (let j = reach.y0; j <= reach.y1; j++) {
1499	        if (!st.inBounds(i, j)) continue;
1500	        const ii = st.idx(i, j);
1501	        if (st.liquid[ii] <= 0) continue;
1502	        // :628-640 3×3 同类液体总量 >100
1503	        let sum = 0;
1504	        for (let k = i - 1; k <= i + 1; k++) {
1505	          for (let l = j - 1; l <= j + 1; l++) {
1506	            if (!st.inBounds(k, l)) continue;
1507	            const ni = st.idx(k, l);
1508	            if (st.liquidType[ni] === st.liquidType[ii]) sum += st.liquid[ni];
1509	          }
1510	        }
1511	        if (sum > 100) targets.push({ x: i, y: j });
1512	      }
1513	    }
1514	    const point = nearestOf(targets, env.mouse);
1515	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1516	  }
1517	
1518	  /** :572-610 致动器（849）：有导线未装致动器的格取最近 */
1519	  private stepActuators(
1520	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1521	    set: (x: number, y: number) => void, taken: () => boolean,
1522	  ): void {
1523	    const isActuatorItem = sem.vid === 849;
1524	    if (!isActuatorItem || taken()) return;
1525	    const st = env.st;
1526	    const targets: Pt[] = [];
1527	    for (let i = reach.x0; i <= reach.x1; i++) {
1528	      for (let j = reach.y0; j <= reach.y1; j++) {
1529	        if (!st.inBounds(i, j)) continue;
1530	        const w = st.wire[st.idx(i, j)];
1531	        // :584 四色任一导线 + 未装致动器 + active
1532	        if ((w & TS.WIRE_COLORS) !== 0 && (w & TS.WIRE_ACTUATOR) === 0 && activeAt(st, i, j)) {
1533	          targets.push({ x: i, y: j });
1534	        }
1535	      }
1536	    }
1537	    const point = nearestOf(targets, env.mouse);
1538	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1539	  }
1540	
1541	  /** :482-570 炼金种子（createTile 82）：各药草适配的盆/土/沙面。
1542	   *  我方药草种子物品放置 sheet 83（v_83_herbs_mature）——82/83 均为我方注册的药草格，
1543	   *  门取两档并集以兼容数据现状（原版仅 82）。 */
1544	  private stepAlchemySeeds(
1545	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1546	    set: (x: number, y: number) => void, taken: () => boolean,
1547	  ): void {
1548	    if (sem.createTileSheet !== 82 && sem.createTileSheet !== 83 || taken()) return;
1549	    const st = env.st;
1550	    const style = sem.placeStyle;
1551	    const targets: Pt[] = [];
1552	    for (let i = reach.x0; i <= reach.x1; i++) {
1553	      for (let j = reach.y0; j <= reach.y1; j++) {
1554	        if (!st.inBounds(i, j)) continue;
1555	        const t = st.get(i, j);
1556	        const below = st.get(i, j + 1);
1557	        // :496 可替换 = 非 active / BreakableWhenPlacing（TileID.cs:379）/
1558	        //  可割植物（82/83 药草除外）/ 成熟药草可收（WorldGen.cs:66173）
1559	        const replaceable = !activeAt(st, i, j)
1560	          || breakableWhenPlacing(sheetOf(t))
1561	          || (tileCutType(t) && sheetOf(t) !== 82 && sheetOf(t) !== 83)
1562	          || isHarvestableHerbWithSeed(st, i, j, env);
1563	        if (!replaceable) continue;
1564	        // :497 下方 nactive（active 且 !inActive）+ 平顶无坡
1565	        if (!activeAt(st, i, j + 1) || inActiveAt(st, i, j + 1)
1566	          || st.half[st.idx(i, j + 1)] !== 0 || st.slope[st.idx(i, j + 1)] !== 0) continue;
1567	        const belowSheet = sheetOf(below);
1568	        const ii = st.idx(i, j);
1569	        const liq = st.liquid[ii];
1570	        const lava = liq > 0 && st.liquidType[ii] === 2; // Tile.lava()
1571	        // :502-546 各样式（草药）适配基质与液体门（原版逐 case 条件照搬）
1572	        const ok = (() => {
1573	          switch (style) {
1574	            case 0: return [78, 380, 2, 477, 109, 492].includes(belowSheet) && liq === 0;
1575	            case 1: return [78, 380, 60].includes(belowSheet) && liq === 0;
1576	            case 2: return [78, 380, 0, 59].includes(belowSheet) && liq === 0;
1577	            case 3: return [78, 380, 203, 199, 23, 25].includes(belowSheet) && liq === 0;
1578	            case 4: return [78, 380, 53, 116].includes(belowSheet) && !(liq > 0 && lava);
1579	            case 5: return [78, 380, 57, 633].includes(belowSheet) && !(liq > 0 && !lava);
1580	            case 6: return [78, 380, 147, 161, 163, 164, 200].includes(belowSheet) && !(liq > 0 && lava);
1581	            default: return false;
1582	          }
1583	        })();
1584	        if (ok) targets.push({ x: i, y: j });
1585	      }
1586	    }
1587	    const point = nearestOf(targets, env.mouse);
1588	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1589	  }
1590	
1591	  /** :427-480 种植盆（createTile 380）：已有盆的左右空位 */
1592	  private stepPlanterBox(
1593	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1594	    set: (x: number, y: number) => void, taken: () => boolean,
1595	  ): void {
1596	    if (sem.createTileSheet !== 380 || taken()) return;
1597	    const st = env.st;
1598	    // :431-435 鼠标正悬在已有种植盆上 → 让位（原版不是"鼠标格占用即停"，只认盆本身）
1599	    if (st.inBounds(screenX, screenY) && activeAt(st, screenX, screenY)
1600	      && sheetOf(st.get(screenX, screenY)) === 380) return;
1601	    const targets: Pt[] = [];
1602	    for (let i = reach.x0; i <= reach.x1; i++) {
1603	      for (let j = reach.y0; j <= reach.y1; j++) {
1604	        if (!st.inBounds(i, j) || sheetOf(st.get(i, j)) !== 380) continue;
1605	        // :448-455 盆左右为空/可割/BreakableWhenPlacing → 续放
1606	        for (const ox of [-1, 1]) {
1607	          const nx = i + ox;
1608	          if (!st.inBounds(nx, j)) continue;
1609	          const nt = st.get(nx, j);
1610	          if (!activeAt(st, nx, j) || tileCutType(nt) || breakableWhenPlacing(sheetOf(nt))) {
1611	            targets.push({ x: nx, y: j });
1612	          }
1613	        }
1614	      }
1615	    }
1616	    const point = nearestOf(targets, env.mouse);
1617	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1618	  }
1619	
1620	  /** :371-425 陶盆（createTile 78）：空位 + 下方平实心顶 */
1621	  private stepClayPots(
1622	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region, screenX: number, screenY: number,
1623	    set: (x: number, y: number) => void, taken: () => boolean,
1624	  ): void {
1625	    if (sem.createTileSheet !== 78 || taken()) return;
1626	    const st = env.st;
1627	    // :378-386 鼠标格占用/不可达 → 停用
1628	    if (activeAt(st, screenX, screenY)) return;
1629	    if (!inTileBounds(screenX, screenY, reach.x0, reach.y0, reach.x1, reach.y1)) return;
1630	    const targets: Pt[] = [];
1631	    for (let i = reach.x0; i <= reach.x1; i++) {
1632	      for (let j = reach.y0; j <= reach.y1; j++) {
1633	        if (!st.inBounds(i, j)) continue;
1634	        const t = st.get(i, j);
1635	        const below = st.get(i, j + 1);
1636	        // :395 自身空/可割/BreakableWhenPlacing，下方 nactive 无坡无半砖且实心
1637	        if ((!activeAt(st, i, j) || tileCutType(t) || breakableWhenPlacing(sheetOf(t)))
1638	          && activeAt(st, i, j + 1) && !inActiveAt(st, i, j + 1)
1639	          && st.half[st.idx(i, j + 1)] === 0 && st.slope[st.idx(i, j + 1)] === 0
1640	          && tileSolidType(below)) {
1641	          targets.push({ x: i, y: j });
1642	        }
1643	      }
1644	    }
1645	    // :409-417 EmptyTile(ignoreTiles:true)（只查占位实体）后取最近
1646	    const open = targets.filter((p) => emptyTile(env, p.x, p.y, true));
1647	    const point = nearestOf(open, env.mouse);
1648	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1649	  }
1650	
1651	  /** :214-254 再生法杖（213/5295）：暴露泥土格取最近 */
1652	  private stepStaffOfRegrowth(
1653	    env: SmartCursorEnv, sem: HeldSemantics, reach: Region,
1654	    set: (x: number, y: number) => void, taken: () => boolean,
1655	  ): void {
1656	    if (sem.vid !== 213 && sem.vid !== 5295 || taken()) return;
1657	    const st = env.st;
1658	    const targets: Pt[] = [];
1659	    for (let i = reach.x0; i <= reach.x1; i++) {
1660	      for (let j = reach.y0; j <= reach.y1; j++) {
1661	        if (!st.inBounds(i, j)) continue;
1662	        // :228 泥土(0) 且暴露（四邻或四角有空）
1663	        if (activeAt(st, i, j) && !inActiveAt(st, i, j) && sheetOf(st.get(i, j)) === 0 && exposed8(st, i, j)) {
1664	          targets.push({ x: i, y: j });
1665	        }
1666	      }
1667	    }
1668	    const point = nearestOf(targets, env.mouse);
1669	    if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) set(point.x, point.y);
1670	  }
1671	}
1672	
1673	// ===================== 模块级工具 =====================
1674	
1675	interface Region { x0: number; y0: number; x1: number; y1: number }
1676	
1677	/** TileReachCheckSettings.GetTileRegion（TileReachCheckSettings.cs:53）+ clamp 世界 [10,max-10]（:100-103） */
1678	function tileRegion(p: SmartCursorActor, tb: number, st: TileStore): Region {
1679	  const x = Math.min(20, 5) + tb;
1680	  const y = Math.min(20, 3) + tb;
1681	  const LX = Math.floor(p.x / 16) - x;
1682	  const HX = Math.ceil((p.x + p.w) / 16) - 1 + x;
1683	  const LY = Math.floor(p.y / 16) - y;
1684	  const HY = Math.ceil((p.y + p.h) / 16) - 1 + y;
1685	  return {
1686	    x0: Math.max(10, Math.min(LX, st.w - 10)),
1687	    x1: Math.max(10, Math.min(HX, st.w - 10)),
1688	    y0: Math.max(10, Math.min(LY, st.h - 10)),
1689	    y1: Math.max(10, Math.min(HY, st.h - 10)),
1690	  };
1691	}
1692	
1693	/** :183-199 让位集（DisableSmartCursor / 轨道 314 且 gravDir=1） */
1694	function isHoveringOverAnInteractableTile(st: TileStore, x: number, y: number): boolean {
1695	  if (!st.inBounds(x, y) || !activeAt(st, x, y)) return false;
1696	  const sheet = sheetOf(st.get(x, y));
1697	  if (DISABLE_SMART_CURSOR_SHEETS.has(sheet)) return true;
1698	  if (sheet === 314) return true; // gravDir 恒 1（反重力未实装）
1699	  return false;
1700	}
1701	
1702	/** Main.tileHammer 全表（Main.cs:7153-7156 共 4 条赋值，全仓再无他处写）：
1703	 *  26 祭坛 / 31 音符块 / 695 / 696 */
1704	const HAMMER_TILES = new Set([26, 31, 695, 696]);
1705	function isHammerTile(sheet: number): boolean {
1706	  return HAMMER_TILES.has(sheet);
1707	}
1708	
1709	/** Step_Platforms 辅助：格上是平台族 sheet（:1445-1452） */
1710	function isPlatformSheet(st: TileStore, x: number, y: number): boolean {
1711	  if (!st.inBounds(x, y) || !activeAt(st, x, y)) return false;
1712	  return PLATFORMS.has(sheetOf(st.get(x, y)));
1713	}
1714	
1715	/** :201-212 AllowNormalBlockPlacementBehaviourForItemType（草种/苔藓物品不参与方块策略） */
1716	function allowNormalBlockPlacement(sem: HeldSemantics): boolean {
1717	  const vid = sem.vid;
1718	  if (vid == null) return true;
1719	  return !(vid === 213 || vid === 5295 || GRASS_SEED_ITEMS.has(vid) || MOSS_ITEMS.has(vid));
1720	}
1721	
1722	/** 放置物为实心非平台非框架方块（BlocksFilling/Lines 门 :812/:2709） */
1723	function isSolidBlockSheet(sheet: number): boolean {
1724	  const tileId = sheetToTileId(sheet);
1725	  if (tileId == null) return false;
1726	  const d = TILE_DEFS[tileId];
1727	  return !!d && d.solid && !d.platform && !d.framed;
1728	}
1729	
1730	function sheetToTileId(sheet: number): number | null {
1731	  if (sheet < 0) return null;
1732	  const hit = TILE_DEFS.findIndex((d) => d?.vanilla?.sheet === sheet);
1733	  return hit >= 0 ? hit : null;
1734	}
1735	
1736	/** WorldGen.IsHarvestableHerbWithSeed（WorldGen.cs:66173-66196）：
1737	 *  type 82 → false；type 84 → true；type 83 → IsAlchemyPlantHarvestable(style=frameX/18, y)。
1738	 *  env.alchemy 缺省（未接世界态）时 83/84 均按不可收——等价语义 = 只认"非药草"分支，
1739	 *  Game 侧已传入 clock/weather/groundLevel 实况，正常对局不触发该缺省。 */
1740	function isHarvestableHerbWithSeed(st: TileStore, x: number, y: number, env: SmartCursorEnv): boolean {
1741	  if (!st.inBounds(x, y) || !activeAt(st, x, y)) return false;
1742	  const sheet = sheetOf(st.get(x, y));
1743	  if (sheet === 82) return false;
1744	  if (sheet !== 83 && sheet !== 84) return false;
1745	  if (sheet === 84) return true;
1746	  const a = env.alchemy;
1747	  if (!a) return false;
1748	  return isAlchemyPlantHarvestable(Math.trunc(st.frameX[st.idx(x, y)] / 18), y, a);
1749	}
1750	
1751	/** WorldGen.IsAlchemyPlantHarvestable（WorldGen.cs:66198-66225）：各药草的收获时段门 */
1752	function isAlchemyPlantHarvestable(
1753	  style: number, y: number,
1754	  a: NonNullable<SmartCursorEnv['alchemy']>,
1755	): boolean {
1756	  if (style === 0 && a.dayTime) return true;
1757	  if (style === 1 && !a.dayTime) return true;
1758	  if (style === 3 && !a.dayTime && (a.bloodMoon || a.moonPhase === 0)) return true;
1759	  if (style === 4 && (a.raining || a.cloudAlpha > 0)) return true;
1760	  if (style === 5) {
1761	    let flag = y > a.worldSurface;
1762	    if (a.remixWorld) flag = y < a.maxTilesY - 350;
1763	    if ((!a.raining || flag) && a.time > 40500) return true;
1764	  }
1765	  return false;
1766	}
1767	
1768	/** 八向至少一格暴露（GrassSeeds/Moss/StaffOfRegrowth 共用 :273-274） */function exposed8(st: TileStore, x: number, y: number): boolean {
1769	  for (const [ox, oy] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
1770	    const nx = x + ox, ny = y + oy;
1771	    if (st.inBounds(nx, ny) && !activeAt(st, nx, ny)) return true;
1772	  }
1773	  for (const [ox, oy] of [[-1, -1], [-1, 1], [1, 1], [1, -1]]) {
1774	    const nx = x + ox, ny = y + oy;
1775	    if (st.inBounds(nx, ny) && !activeAt(st, nx, ny)) return true;
1776	  }
1777	  return false;
1778	}
1779	
1780	/** :2867-2893 IsValidSpotForTorch（墙 → 左 → 右 → 下） */
1781	function isValidSpotForTorch(st: TileStore, x: number, y: number): boolean {
1782	  if (!st.inBounds(x, y)) return false;
1783	  const ii = st.idx(x, y);
1784	  if (st.wall[ii] > 0) return true; // :2869 有墙即放
1785	  if (TORCH_TILES.has(sheetOf(st.type[ii]))) return false; // :2873 自身是火把
1786	  const isTreeType = (tx: number, ty: number): boolean => {
1787	    if (!st.inBounds(tx, ty) || !activeAt(st, tx, ty)) return false;
1788	    return IS_A_TREE_TRUNK.has(sheetOf(st.get(tx, ty)));
1789	  };
1790	  // :2877-2881 左：slope 允许（0 或奇数坡）且 实心/梁/连续三格树干
1791	  if (st.inBounds(x - 1, y) && activeAt(st, x - 1, y)) {
1792	    const li = st.idx(x - 1, y);
1793	    const lt = st.get(x - 1, y);
1794	    const ls = sheetOf(lt);
1795	    if ((st.slope[li] === 0 || st.slope[li] % 2 !== 1)
1796	      && ((tileSolidType(lt) && !tileNoAttachType(ls) && !tileSolidTopType(lt) && !NOT_REALLY_SOLID.has(ls))
1797	        || IS_BEAM.has(ls)
1798	        || (isTreeType(x - 1, y) && isTreeType(x - 1, y - 1) && isTreeType(x - 1, y + 1)))) {
1799	      return true;
1800	    }
1801	  }
1802	  // :2882-2886 右：slope 允许（0 或偶数坡）
1803	  if (st.inBounds(x + 1, y) && activeAt(st, x + 1, y)) {
1804	    const ri = st.idx(x + 1, y);
1805	    const rt = st.get(x + 1, y);
1806	    const rs = sheetOf(rt);
1807	    if ((st.slope[ri] === 0 || st.slope[ri] % 2 !== 0)
1808	      && ((tileSolidType(rt) && !tileNoAttachType(rs) && !tileSolidTopType(rt) && !NOT_REALLY_SOLID.has(rs))
1809	        || IS_BEAM.has(rs)
1810	        || (isTreeType(x + 1, y) && isTreeType(x + 1, y - 1) && isTreeType(x + 1, y + 1)))) {
1811	      return true;
1812	    }
1813	  }
1814	  // :2887-2891 下：slope 0 且非半砖，实心（非平台）或平台
1815	  if (st.inBounds(x, y + 1) && activeAt(st, x + 0, y + 1)) {
1816	    const bi = st.idx(x, y + 1);
1817	    const bt = st.get(x, y + 1);
1818	    const bs = sheetOf(bt);
1819	    if (st.slope[bi] === 0 && st.half[bi] === 0
1820	      && ((tileSolidType(bt) && !tileSolidTopType(bt)) || PLATFORMS.has(bs))
1821	      && !NOT_REALLY_SOLID.has(bs)) {
1822	      return true;
1823	    }
1824	  }
1825	  return false;
1826	}
1827	
1828	// ===================== Collision.HitLineWall / HitWallSubstep 1:1（Collision.cs:1148-1359） =====================
1829	
1830	/**
1831	 * Collision.HitWallSubstep（Collision.cs:1312-1359）：该格墙"还有得锤"。
1832	 *  - wall==0 → false（:1314-1317）
1833	 *  - 房墙（Main.wallHouse，Main.cs 全表）→ flag=true（:1319-1322）
1834	 *  - 否则 3×3 任一邻格（含对角，跳过自身）wall==0 → flag=true（:1325-1334）
1835	 *  - 本格 active 且 flag：八邻全是 active+tileSolid+!tileSolidTop → flag=false
1836	 *    （墙被实心块完全包死，锤不到；:1336-1357）
1837	 * 返回 null 表示原版越界异常（Main.tile[x±1,y±1] 越界 → NullReference/IndexOutOfRange，
1838	 *  HitLineWall 的 catch 吞成 (-1,-1)；此处上层据此短路）。
1839	 */
1840	export function hitWallSubstepCore(st: TileStore, x: number, y: number): boolean | null {
1841	  if (!st.inBounds(x, y)) return null; // 原版 Main.tile[x,y] 越界 → 异常
1842	  const i = st.idx(x, y);
1843	  if (st.wall[i] === 0) return false;
1844	  let flag = false;
1845	  if (WALL_HOUSE.has(st.wall[i])) flag = true;
1846	  if (!flag) {
1847	    for (let k = -1; k < 2; k++) {
1848	      for (let l = -1; l < 2; l++) {
1849	        if (k === 0 && l === 0) continue;
1850	        if (!st.inBounds(x + k, y + l)) return null; // :1329 越界读 → 异常
1851	        if (st.wall[st.idx(x + k, y + l)] === 0) flag = true;
1852	      }
1853	    }
1854	  }
1855	  if (activeAt(st, x, y) && flag) {
1856	    let flag2 = true;
1857	    for (let k = -1; k < 2; k++) {
1858	      for (let l = -1; l < 2; l++) {
1859	        if (k === 0 && l === 0) continue;
1860	        if (!st.inBounds(x + k, y + l)) { flag2 = false; continue; } // 越界按"非实心邻"计
1861	        const t = st.type[st.idx(x + k, y + l)];
1862	        if (!activeAt(st, x + k, y + l) || !tileSolidType(t) || tileSolidTopType(t)) flag2 = false;
1863	      }
1864	    }
1865	    if (flag2) flag = false;
1866	  }
1867	  return flag;
1868	}
1869	
1870	/** Step_Hammers 全扫段（SmartCursorHelper.cs:1696）独立调用面：越界一律按 false */
1871	export function hitWallSubstep(st: TileStore, x: number, y: number): boolean {
1872	  return hitWallSubstepCore(st, x, y) === true;
1873	}
1874	
1875	/**
1876	 * Collision.HitLineWall（Collision.cs:1148-1310）1:1：DDA 步进找首个 HitWallSubstep 为真的格。
1877	 *  端点钳制 :1154-1185（x∈[1,maxTilesX-1]、y∈[1,maxTilesY-40]）；步比 :1192-1212；
1878	 *  起始分支 :1216-1219（y1<y2 先入 case 2）；剩余计数 :1220-1223。
1879	 *  两段循环体（:1232-1291）交替消耗 num9/num10 累积步进并逐格判 HitWallSubstep——
1880	 *  注意 case 2（:1232-1261）体内沿 X 步进、case 1（:1262-1291）体内沿 Y 步进，
1881	 *  斜线因此走出阶梯足迹；
1882	 *  末尾兜底再判一次（:1293-1301）；flag（计数耗尽）/flag2（恰好 1 步走完）终止（:1303）。
1883	 *  途中读到越界格 = 原版 null tile → 返回 (-1,-1)（:1293-1296 的 catch 等价）。
1884	 *  无命中时返回终点格（:1304）。
1885	 */
1886	export function hitLineWall(st: TileStore, x1: number, y1: number, x2: number, y2: number): Pt {
1887	  let num = Math.max(1, Math.min(x1, st.w - 1));       // :1154-1161
1888	  let num2 = Math.max(1, Math.min(y1, st.h - 40));     // :1170-1177
1889	  const num3 = Math.max(1, Math.min(x2, st.w - 1));    // :1162-1169
1890	  const num4 = Math.max(1, Math.min(y2, st.h - 40));   // :1178-1185
1891	  const num5 = Math.abs(num - num3);                    // :1186
1892	  const num6 = Math.abs(num2 - num4);                   // :1187
1893	  if (num5 === 0 && num6 === 0) return { x: num, y: num2 }; // :1188-1191
1894	  let num7 = 1, num8 = 1;                               // :1192-1193
1895	  if (num5 === 0 || num6 === 0) {                       // :1194-1204
1896	    if (num5 === 0) num7 = 0;
1897	    if (num6 === 0) num8 = 0;
1898	  } else if (num5 > num6) num7 = num5 / num6;           // :1205-1208
1899	  else num8 = num6 / num5;                              // :1209-1212
1900	  let num9 = 0, num10 = 0;                              // :1213-1214
1901	  let num11 = num2 < num4 ? 2 : 1;                      // :1215-1219
1902	  let num12 = Math.trunc(num5), num13 = Math.trunc(num6); // :1220-1221
1903	  const num14 = Math.sign(num3 - num);                  // :1222
1904	  const num15 = Math.sign(num4 - num2);                 // :1223
1905	  let flag = false, flag2 = false;                      // :1224-1225
1906	  do {
1907	    if (num11 === 2) {                                  // :1232-1261（y1<y2 首选；体内沿 X 步进）
1908	      num9 += num7;
1909	      const num17 = Math.trunc(num9);
1910	      num9 -= num17;
1911	      for (let j = 0; j < num17; j++) {
1912	        const r = hitWallSubstepCore(st, num, num2);
1913	        if (r === null) return { x: -1, y: -1 };        // 原版 null tile / 越界异常
1914	        if (r) return { x: num, y: num2 };
1915	        if (num12 === 0 && num13 === 0) { flag = true; break; } // :1244-1248
1916	        num += num14; num12--;                          // :1249
1917	        if (num12 === 0 && num13 === 0 && num17 === 1) flag2 = true; // :1251-1254
1918	      }
1919	      if (num13 !== 0) num11 = 1;                       // :1256-1259
1920	    } else {                                            // :1262-1291（体内沿 Y 步进）
1921	      num10 += num8;
1922	      const num16 = Math.trunc(num10);
1923	      num10 -= num16;
1924	      for (let i = 0; i < num16; i++) {
1925	        const r = hitWallSubstepCore(st, num, num2);
1926	        if (r === null) return { x: -1, y: -1 };
1927	        if (r) return { x: num, y: num2 };
1928	        if (num12 === 0 && num13 === 0) { flag = true; break; }
1929	        num2 += num15; num13--;
1930	        if (num12 === 0 && num13 === 0 && num16 === 1) flag2 = true;
1931	      }
1932	      if (num12 !== 0) num11 = 2;
1933	    }
1934	    if (!st.inBounds(num, num2)) return { x: -1, y: -1 }; // :1293-1296 null tile
1935	    const r2 = hitWallSubstepCore(st, num, num2);
1936	    if (r2 === null) return { x: -1, y: -1 };
1937	    if (r2) return { x: num, y: num2 };                  // :1298-1301
1938	  } while (!(flag || flag2));                            // :1303
1939	  return { x: num, y: num2 };                            // :1304
1940	}
1941	
1942	/** 锤目标剔除祭坛（SmartCursorHelper.cs:1662/:1704）：原版谓词 `!tile.active() || tile.type != 26` */
1943	function pickNonAltar(st: TileStore, targets: Pt[], world: (p: Pt) => { x: number; y: number }, ref: { x: number; y: number }): Pt | null {
1944	  let best = -1;
1945	  let point: Pt | null = null;
1946	  for (const t of targets) {
1947	    if (!st.inBounds(t.x, t.y)) continue;
1948	    const i = st.idx(t.x, t.y);
1949	    if (activeAt(st, t.x, t.y) && st.type[i] !== 0 && sheetOf(st.type[i]) === 26) continue;
1950	    const w = world(t);
1951	    const d = dist(w.x, w.y, ref.x, ref.y);
1952	    if (best === -1 || d < best) { best = d; point = t; }
1953	  }
1954	  return point;
1955	}
1956	
1957	// ===================== Collision.CanHitWithCheck 1:1（Collision.cs:492-589） =====================
1958	
1959	/**
1960	 * DelegateMethods.NotDoorStand（DelegateMethods.cs:858-869）：开着的门（sheet 11）的
1961	 *  "锚帧"（frameX<18 或 ≥54）返回 false（阻挡视线），门体帧（18≤frameX<54）返回 true。
1962	 *  CanHitWithCheck 的 do-while 以它为循环条件——锚帧直接终止循环 → 返回 false。
1963	 */
1964	function notDoorStand(st: TileStore, x: number, y: number): boolean {
1965	  if (!st.inBounds(x, y)) return true; // 原版 Main.tile[x,y]==null 短路 → true
1966	  const i = st.idx(x, y);
1967	  if (activeAt(st, x, y) && sheetOf(st.type[i]) === 11) {
1968	    const fx = st.frameX[i];
1969	    if (fx >= 18) return fx < 54;
1970	    return false;
1971	  }
1972	  return true;
1973	}
1974	
1975	/** WorldGen.IsOpenDoorAnchorFrame（WorldGen.cs:69228-69241）：sheet 11 且 frameX%72
1976	 *  落在锚帧（<18 或 ≥54）。Step_Walls 用它排除开门锚位格（SmartCursorHelper.cs:1137-1140）。 */
1977	export function isOpenDoorAnchorFrame(st: TileStore, x: number, y: number): boolean {
1978	  if (!st.inBounds(x, y) || !activeAt(st, x, y)) return false;
1979	  const i = st.idx(x, y);
1980	  if (sheetOf(st.type[i]) !== 11) return false;
1981	  const num = st.frameX[i] % 72;
1982	  if (num >= 18) return num >= 54;
1983	  return true;
1984	}
1985	
1986	/** 原版 CanHitWithCheck 邻格阻挡谓词（Collision.cs:551/:567）：
1987	 *  active && !inActive && tileSolid && !tileSolidTop && slope==0 && !halfBrick */
1988	function blocksSightFully(st: TileStore, x: number, y: number): boolean {
1989	  if (!st.inBounds(x, y)) return false; // 原版 null tile → 提前 return false
1990	  const i = st.idx(x, y);
1991	  return !inActiveAt(st, x, y) && activeAt(st, x, y)
1992	    && tileSolidType(st.type[i]) && !tileSolidTopType(st.type[i])
1993	    && st.slope[i] === 0 && st.half[i] === 0;
1994	}
1995	
1996	/**
1997	 * Collision.CanHitWithCheck（Collision.cs:492-589）1:1：视线逐格走查。
1998	 *  起点/终点取两盒中心格（:494-497），钳制 :498-529；
1999	 *  do-while（:532-578）：每步沿主轴（|dx|>|dy| 走 x，否则走 y）推进一格，
2000	 *  并要求两侧邻格不同时为"完整实心"（:540-566，夹缝不可视）；
2001	 *  到达终点格 → true（:536-539）；落入实心非平台格 → false（:573-576）；
2002	 *  循环条件 = check（Step_Walls 传 NotDoorStand）。
2003	 */
2004	export function canHitWithCheck(
2005	  st: TileStore,
2006	  p1: { x: number; y: number }, w1: number, h1: number,
2007	  p2: { x: number; y: number }, w2: number, h2: number,
2008	  check: (x: number, y: number) => boolean,
2009	): boolean {
2010	  let num = Math.trunc((p1.x + Math.trunc(w1 / 2)) / 16);    // :494
2011	  let num2 = Math.trunc((p1.y + Math.trunc(h1 / 2)) / 16);    // :495
2012	  const num3 = Math.trunc((p2.x + Math.trunc(w2 / 2)) / 16);  // :496
2013	  const num4 = Math.trunc((p2.y + Math.trunc(h2 / 2)) / 16);  // :497
2014	  num = Math.max(1, Math.min(num, st.w - 1));                 // :498-513
2015	  num2 = Math.max(1, Math.min(num2, st.h - 40));
2016	  const cx = Math.max(1, Math.min(num3, st.w - 1));
2017	  const cy = Math.max(1, Math.min(num4, st.h - 40));
2018	  do {
2019	    const num5 = Math.abs(num - cx);                          // :534
2020	    const num6 = Math.abs(num2 - cy);                         // :535
2021	    if (num === cx && num2 === cy) return true;               // :536-539
2022	    if (num5 > num6) {                                        // :540 沿 x 推进
2023	      num += num >= cx ? -1 : 1;
2024	      if (!st.inBounds(num, num2 - 1) || !st.inBounds(num, num2 + 1)) return false; // :543-550
2025	      if (blocksSightFully(st, num, num2 - 1) && blocksSightFully(st, num, num2 + 1)) return false; // :551-554
2026	    } else {                                                  // :556-558 沿 y 推进
2027	      num2 += num2 >= cy ? -1 : 1;
2028	      if (!st.inBounds(num - 1, num2) || !st.inBounds(num + 1, num2)) return false; // :559-566
2029	      if (blocksSightFully(st, num - 1, num2) && blocksSightFully(st, num + 1, num2)) return false; // :567-570
2030	    }
2031	    if (!st.inBounds(num, num2)) return false;                // :571-574
2032	    const i = st.idx(num, num2);
2033	    if (!inActiveAt(st, num, num2) && activeAt(st, num, num2)
2034	      && tileSolidType(st.type[i]) && !tileSolidTopType(st.type[i])) {
2035	      return false;                                           // :575-578
2036	    }
2037	  } while (check(num, num2));                                 // :579
2038	  return false;                                               // :580
2039	}
2040	
2041	/** PumpkinSeeds/Boulders 共用收尾（:1077-1096 / :946-965） */
2042	function pumpkinOrBoulderScan(
2043	  env: SmartCursorEnv, reach: Region,
2044	  set: (x: number, y: number) => void,
2045	  pred: (st: TileStore, i: number, j: number) => boolean,
2046	): void {
2047	  const st = env.st;
2048	  const targets: Pt[] = [];
2049	  for (let i = reach.x0; i <= reach.x1; i++) {
2050	    for (let j = reach.y0; j <= reach.y1; j++) {
2051	      if (!st.inBounds(i, j)) continue;
2052	      if (pred(st, i, j)) targets.push({ x: i, y: j });
2053	    }
2054	  }
2055	  const point = nearestOf(targets, env.mouse);
2056	  if (point && inTileBounds(point.x, point.y, reach.x0, reach.y0, reach.x1, reach.y1)) {
2057	    set(point.x, point.y);
2058	  }
2059	}
2060	

```


---

## 🤖 Assistant · 2026-08-13T01:25:27.438Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/player/SmartSelect.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:27.453Z

**📎 ToolResult**

```
1	// 智能选取（Smart Select）——原版 1.4.5.6 一比一移植。
2	//
3	// 与智能光标（SmartCursor.ts，Ctrl 选目标格）是相互独立的系统：
4	// Smart Select = 按住 Shift（键绑定 "SmartSelect"）时按鼠标所指方块自动换手持工具/光源。
5	//
6	// 权威源码对照（行号 = Terarria1456 反编译）：
7	//   - 键绑定 SmartSelect = "LeftShift"            PlayerInput.cs:1898 / :2011 / :2123 / :2235
8	//   - TriggersSet.CopyInto → p.controlTorch       TriggersSet.cs:782-795（mouseInterface 让位）
9	//   - 每帧驱动 SelectedItemState.Update           Player.cs:483-517（Player.Update :24923 调用）
10	//   - PickItemSelectionOverride                   Player.cs:17259-17280
11	//   - SmartSelectLookup                           Player.cs:17283-17309
12	//   - 目标格换算 SmartSelectLookup_GetTargetTile   SmartSelectGamepadPointer.cs:23-38
13	//     （Player.cs:17311-17319 还有一份同体私有副本，未被调用）
14	//   - SmartSelect_PickToolForStrategy             Player.cs:17321-17470
15	//   - SmartSelect_GetToolStrategy                 Player.cs:17472-17528
16	//   - SmartSelect_GetAvailableToolRanges          Player.cs:17530-17562
17	//   - 换选门 CanChangeSelectedItemImmediately     Player.cs:386-393
18	//   - 覆盖/还原 OverrideSelection                 Player.cs:424-434
19	//   - OnSelectionChanged                          Player.cs:519-533
20	//   - 物品集 ItemID.Sets.Torches/WaterTorches      ItemID.cs:1192 / :1194
21	//             Glowsticks                          ItemID.cs:1198
22	//             IsPaintScraper                      ItemID.cs:254
23	//             ExtractinatorMode                   ItemID.cs:1104
24	//   - 方块集 Main.tileHammer（4 条）              Main.cs:7153-7156
25	//             Main.tileAxe（16 条）               Main.cs:7157-7171
26	//   - 叶绿提取机兑换表                            ItemTrader.cs:82-108（TryGetTradeOption :66-80）
27	//   - 玩家湿身 Collision.WetCollision             Collision.cs:1575-1625（Player.cs:27540 置位）
28	//
29	// tile 桥接与 SmartCursor 共用 sheetOf / vanillaItemIdOf（src/player/SmartCursor.ts）。
30	import type { TileStore } from '../world/TileStore';
31	import { sheetOf, vanillaItemIdOf } from './SmartCursor';
32	import { CHLOROPHYTE_TRADES, EXTRACTINATOR_MODE } from '../world/Extractinator';
33	import type { ItemDef } from '../data/items';
34	
35	// ===================== 原版 ItemID.Sets 集合 =====================
36	
37	/** ItemID.cs:1192 Torches（CreateBoolSet 24 项） */
38	const TORCH_ITEMS: ReadonlySet<number> = new Set([8, 427, 3004, 523, 433, 429, 974, 1333, 1245, 3114,
39	  430, 3045, 428, 2274, 431, 432, 4383, 4384, 4385, 4386, 4387, 4388, 5293, 5353]);
40	
41	/** ItemID.cs:1194 WaterTorches（水中不熄：诅咒 523 / 脓血 1333 / 珊瑚 4384） */
42	const WATER_TORCH_ITEMS: ReadonlySet<number> = new Set([523, 1333, 4384]);
43	
44	/** ItemID.cs:1198 Glowsticks（荧光棒族 6 项） */
45	const GLOWSTICK_ITEMS: ReadonlySet<number> = new Set([282, 286, 3112, 3002, 4776, 5643]);
46	
47	/** ItemID.cs:254 IsPaintScraper（油漆刮刀；本作油漆系统未建——集合保留，策略 8 可选中刮刀） */
48	const PAINT_SCRAPER_ITEMS: ReadonlySet<number> = new Set([1100, 1545]);
49	
50	/** 信号枪 FlareGun（ItemID.cs:3399）——case 4/5 的特殊光源分支（Player.cs:17368/:17406） */
51	const FLARE_GUN = 930;
52	/** AmmoID.Flare = 931（AmmoID.cs:132） */
53	const AMMO_FLARE = 931;
54	/** 信号枪 useAmmo（Item.cs:12108 `useAmmo = AmmoID.Flare`）。
55	 *  vanilla-itemfunc.json 对 930 提取为 useAmmo:-1（tools/extract-itemfunc.mjs 缺该分支），
56	 *  此处按原版源码补正——case 4/5 的弹药门（Player.cs:17373-17384 / :17408-17420）依赖。 */
57	const FLARE_GUN_USE_AMMO: Readonly<Record<number, number>> = { 930: AMMO_FLARE };
58	/** 荧光弹族 ammo（Item.cs:12121 Flare / :19106 BlueFlare 均 `ammo = AmmoID.Flare`）。
59	 *  提取缺口同上（json 中均为 -1），按原版补正。 */
60	const FLARE_AMMO_ITEMS: ReadonlySet<number> = new Set([931, 1614]);
61	
62	// ===================== 原版 Main.tileHammer / Main.tileAxe（以 sheet = 原版 tile id 表达） =====================
63	
64	/** Main.cs:7153-7156 tileHammer 全表（26 祭坛 / 695 / 31 音符块 / 696） */
65	const TILE_HAMMER_SHEETS: ReadonlySet<number> = new Set([26, 31, 695, 696]);
66	
67	/** Main.cs:7157-7171 tileAxe 全表（树 5 / 蘑菇树 72 / 仙人掌 80 / 倒木 488 / 倒木回响 704 /
68	 *  棕榈树 323 / 樱花树 596 / 黄柳树 616 / 灰烬树 634 / 宝石树 583-589） */
69	const TILE_AXE_SHEETS: ReadonlySet<number> = new Set([
70	  5, 72, 80, 488, 704, 323, 596, 616, 634, 589, 584, 588, 586, 587, 585, 583,
71	]);
72	
73	/** 策略号语义（SmartSelect_GetToolStrategy 各分支的 toolStrategy 值） */
74	export const STRATEGY = {
75	  TORCH: 0,        // 默认：放火把/荧光棒
76	  HAMMER: 1,       // tileHammer 方块
77	  AXE: 2,          // tileAxe 方块
78	  PICK: 3,         // 其余实心方块
79	  WET_LIGHT: 4,    // 湿格/自身湿 → 水下光源
80	  FAR_LIGHT: 5,    // 超 200px：火把放不到 → 投掷光源
81	  CANNON: 6,       // tile 209 大炮 → 火把点火
82	  EXTRACT: 7,      // tile 219/642 提取机 → 可投入物
83	  PAINT_SCRAPER: 8,// tile 184 长苔藓 → 刮漆器
84	} as const;
85	
86	// ===================== 输入上下文 =====================
87	
88	/** inventory[0..57] 单槽语义（Player.inventory 的窄视图；0-49 背包 + 50-53 钱币 + 54-57 弹药） */
89	export interface SmartSelectSlot {
90	  /** Item.type（原版物品 id；空槽 0） */
91	  vid: number;
92	  /** Item.stack（空槽 0） */
93	  stack: number;
94	  /** Item.pick / Item.axe / Item.hammer（>0 = 该类工具） */
95	  pick: number;
96	  axe: number;
97	  hammer: number;
98	  /** Item.ammo（0 = AmmoID.None，AmmoID.cs:112） */
99	  ammo: number;
100	  /** Item.useAmmo（0 = AmmoID.None） */
101	  useAmmo: number;
102	  /** Item.tileBoost（Player.cs:17537-17560 取第一件对应工具的 reach 加成） */
103	  tileBoost: number;
104	}
105	
106	/** 空槽（inventory[i].IsAir → type=0 / stack=0 / 三力 0） */
107	export const EMPTY_SLOT: SmartSelectSlot = {
108	  vid: 0, stack: 0, pick: 0, axe: 0, hammer: 0, ammo: 0, useAmmo: 0, tileBoost: 0,
109	};
110	
111	/** 由 ItemDef + 三力画像构建槽语义（Game 每帧对 0-57 构建）。
112	 *  传 into 则原地填充（每帧复用缓冲，防分配热点）；legacy def.tool 画像只覆盖自身类型的
113	 *  主力（Game 工具判定同序 def.tool 优先），vi_ 双工具（Hamaxe 斧+锤 / Drax 镐+斧）
114	 *  其余副力保留 itemfunc 全量 */
115	export function smartSelectSlotOf(
116	  def: ItemDef | null | undefined,
117	  stack: number,
118	  itemFunc: { pick?: number; axe?: number; hammer?: number; ammo?: number; useAmmo?: number } | null | undefined,
119	  toolOverride?: { type: 'pick' | 'axe' | 'hammer'; power: number } | null,
120	  into?: SmartSelectSlot,
121	): SmartSelectSlot {
122	  const vid = vanillaItemIdOf(def) ?? 0;
123	  const pick = itemFunc?.pick ?? 0;
124	  const axe = itemFunc?.axe ?? 0;
125	  const hammer = itemFunc?.hammer ?? 0;
126	  const t = toolOverride;
127	  const out: SmartSelectSlot = into ?? {
128	    vid: 0, stack: 0, pick: 0, axe: 0, hammer: 0, ammo: 0, useAmmo: 0, tileBoost: 0,
129	  };
130	  out.vid = vid;
131	  out.stack = stack;
132	  out.pick = t?.type === 'pick' ? t.power : pick;
133	  out.axe = t?.type === 'axe' ? t.power : axe;
134	  out.hammer = t?.type === 'hammer' ? t.power : hammer;
135	  out.ammo = itemFunc?.ammo ?? 0;
136	  out.useAmmo = itemFunc?.useAmmo ?? 0;
137	  out.tileBoost = 0;
138	  return out;
139	}
140	
141	export interface SmartSelectPlayer {
142	  /** Player.position（px） */
143	  x: number; y: number;
144	  /** Player.width / height（px） */
145	  w: number; h: number;
146	  /** Player.wet（Player.cs:27540，经 Collision.WetCollision Collision.cs:1575 判定） */
147	  wet: boolean;
148	  /** Player.gravDir（反重力未实装，恒 1；SmartSelectGamepadPointer.cs:28-30 的翻转分支保留） */
149	  gravDir: number;
150	}
151	
152	export interface SmartSelectEnv {
153	  /** Player.controlTorch（TriggersSet.cs:794 = SmartSelect 键按住） */
154	  controlTorch: boolean;
155	  /** PlayerInput.UsingGamepad（本作恒 false——:17293-17296 手柄粘滞分支保留为死代码注释） */
156	  usingGamepad: boolean;
157	  st: TileStore;
158	  /** MouseWorld（Main.mouseX + screenPosition，px） */
159	  mouseX: number; mouseY: number;
160	  /** Main.screenPosition.Y（屏幕左上角世界 Y，px；gravDir=-1 翻转分支用） */
161	  screenTopY: number;
162	  /** Main.screenHeight（px，gravDir=-1 翻转分支用） */
163	  screenHeight: number;
164	  player: SmartSelectPlayer;
165	  /** inventory[0..57]（长度 58：0-49 背包 + 钱币 + 弹药；case 4/5 弹药门扫到 57，Player.cs:17374/:17410） */
166	  slots: SmartSelectSlot[];
167	  /** Player.selectedItem（SelectedItemState.Selected，Player.cs:3689） */
168	  selectedItem: number;
169	  /** IsInTileInteractionRange（Player.cs:31548，TileReachCheckSettings.Simple 档 + tileBoost） */
170	  inRange: (tx: number, ty: number, tileBoost: number) => boolean;
171	}
172	
173	/** SelectedItemState（Player.cs:383-517）的宿主窄视图——换选/还原语义由 SmartSelect 代管 */
174	export interface SmartSelectHost {
175	  /** 当前选中槽（读写在宿主上落地） */
176	  selected: number;
177	  /** SelectedItemState.Hotbar（Player.cs:391）——selected≥10 且空手时回退（:499-501） */
178	  hotbar: number;
179	  /** CanChangeSelectedItemImmediately（Player.cs:386-393：itemAnimation/reuseDelay/channel/
180	   *  pendingItemReuse 全空 且 itemTime==0） */
181	  canChangeImmediately: boolean;
182	  /** inventory[i].IsAir */
183	  isSlotEmpty: (i: number) => boolean;
184	  /** OnSelectionChanged（Player.cs:519-533）——宿主刷新热栏/挥击态 */
185	  onSelectionChanged: () => void;
186	}
187	
188	// ===================== 玩家湿身（Collision.WetCollision，Collision.cs:1575-1625） =====================
189	
190	/**
191	 * 玩家是否浸在液体中——Collision.WetCollision 1:1（不含 honey/shimmer 位，Smart Select 只用 wet）。
192	 * 以命中盒中心的 (min(10,width) × height/2) 盒与液体面（液量换算的表面下移）求交。
193	 */
194	export function wetCollision(st: TileStore, x: number, y: number, w: number, h: number): boolean {
195	  // :1579-1590 盒中心 + num=10 / num2=Height/2（各自截到宽/高）
196	  let num = 10;
197	  let num2 = Math.floor(h / 2);
198	  if (num > w) num = w;
199	  if (num2 > h) num2 = h;
200	  const vx = x + w / 2 - num / 2;
201	  const vy = y + h / 2 - num2 / 2;
202	  // :1591-1594 扫描区外扩 1-2 格
203	  const x0 = Math.max(0, Math.floor(x / 16) - 1);
204	  const x1 = Math.min(st.w - 1, Math.floor((x + w) / 16) + 2);
205	  const y0 = Math.max(0, Math.floor(y / 16) - 1);
206	  const y1 = Math.min(st.h - 1, Math.floor((y + h) / 16) + 2);
207	  for (let i = x0; i <= x1; i++) {
208	    for (let j = y0; j <= y1; j++) {
209	      const idx = st.idx(i, j);
210	      const liquid = st.liquid[idx];
211	      if (liquid <= 0) continue;                       // :1607-1610
212	      // :1612-1617 液面下移：num5=(256-liquid)/32，表面 y += num5*2，有效高 16-=num5*2
213	      const drop = (256 - liquid) / 32;
214	      const surfY = j * 16 + drop * 2;
215	      const surfH = 16 - drop * 2;
216	      // :1618 与中心盒 AABB 求交
217	      if (vx + num > i * 16 && vx < i * 16 + 16 && vy + num2 > surfY && vy < surfY + surfH) {
218	        return true;
219	      }
220	    }
221	  }
222	  return false;
223	}
224	
225	// ===================== 状态机 =====================
226	
227	export class SmartSelect {
228	  /** _lastSmartCursorToolStrategy（Player.cs:17286 清零 / :17306 写回；手柄粘滞 :17293-17296 用） */
229	  lastStrategy = -1;
230	  /** SelectedItemState.overridden（Player.cs:392）——行为选中前的原槽，松键还原用 */
231	  private overridden = -1;
232	  /** 本帧行为选中的槽（无行为选中 = -1；测试/调试观测用） */
233	  slot = -1;
234	  /** 本帧策略号与湿格（SmartSelectLookup 中间量，观测用） */
235	  strategy = 0;
236	  wetTile = false;
237	
238	  /**
239	   * 每帧驱动 = SelectedItemState.Update（Player.cs:483-517）中与行为选中相关的全部语义：
240	   *   1. 换选门 :484（CanChangeSelectedItemImmediately）
241	   *   2. 还原上帧行为选中 :491-494（无 buffered 且 HasActiveOverride → selected = overridden）
242	   *      + :497 清 overridden（buffered 我们没有——数字键直写 selected，效果等价见 Game 注释）
243	   *   3. :499-501 selected≥10 且空手 → 回退 hotbar
244	   *   4. :503-505 PickItemSelectionOverride（Player.cs:17259-17280）
245	   *      → :17266 SmartSelectLookup → OverrideSelection（:424-434）
246	   *   5. :511-513 selected 变化 → OnSelectionChanged（Player.cs:519-533）
247	   */
248	  update(env: SmartSelectEnv, host: SmartSelectHost): void {
249	    this.slot = -1;
250	    if (!host.canChangeImmediately) return;                    // :484
251	    const prev = host.selected;
252	    if (this.overridden >= 0) host.selected = this.overridden; // :491-494
253	    this.overridden = -1;                                      // :497
254	    if (host.selected >= 10 && host.isSlotEmpty(host.selected)) host.selected = host.hotbar; // :499-501
255	    // PickItemSelectionOverride（Player.cs:17259-17265）：Main.mouseItem 非空 → 选中槽 58。
256	    // 本作鼠标携带物仅存在于背包 UI 拖拽中，而 UI 打开时 controlTorch 已被屏蔽（Input.down
257	    // 的 uiBlocking 门 = TriggersSet.cs:783 键盘 UI 模式让位的等价），故此处无可让位分支。
258	    const slot = this.lookup(env);                             // :17266
259	    this.slot = slot;
260	    if (this.lookupActive(env)) {                              // SmartSelectLookup 返回 true
261	      this.overrideSelection(slot, host);                      // :514-516
262	    }
263	    if (host.selected !== prev) host.onSelectionChanged();     // :511-513
264	  }
265	
266	  /** 行为选中是否激活（SmartSelectLookup 返回值 :17308 = controlTorch） */
267	  private lookupActive(env: SmartSelectEnv): boolean {
268	    return env.controlTorch;
269	  }
270	
271	  /**
272	   * SmartSelectLookup 1:1（Player.cs:17283-17309）。返回行为选中槽。
273	   */
274	  lookup(env: SmartSelectEnv): number {
275	    if (!env.controlTorch) {                                   // :17285-17289
276	      this.lastStrategy = -1;
277	      return -1;
278	    }
279	    const { tX, tY } = this.getTargetTile(env);                // :17291
280	    const got = this.getToolStrategy(tX, tY, env);             // :17292
281	    this.wetTile = got.wetTile;
282	    let strategy = got.toolStrategy;
283	    // :17293-17296 手柄粘滞：UsingGamepad 且上帧有策略 → 沿用。
284	    // 本作 usingGamepad 恒 false（键盘/鼠标输入），分支保留供对照。
285	    if (env.usingGamepad && this.lastStrategy !== -1) strategy = this.lastStrategy;
286	    // :17297-17305 超 200px 修正：策略 0/4（放火把/水下光源）超出放置距离 → 投掷光源策略 5
287	    if (strategy === STRATEGY.TORCH || strategy === STRATEGY.WET_LIGHT) {
288	      const num = Math.abs(env.mouseX - (env.player.x + env.player.w / 2));
289	      const num2 = Math.abs(env.mouseY - (env.player.y + env.player.h / 2)) * 1.3;
290	      if (Math.sqrt(num * num + num2 * num2) > 200) strategy = STRATEGY.FAR_LIGHT;
291	    }
292	    this.lastStrategy = strategy;                              // :17306
293	    this.strategy = strategy;
294	    return this.pickToolForStrategy(tX, tY, strategy, got.wetTile, env); // :17307
295	  }
296	
297	  /**
298	   * SmartSelectLookup_GetTargetTile 1:1（SmartSelectGamepadPointer.cs:23-38）。
299	   * 手柄指针分支（ShouldBeUsed :8-16）本作不达（usingGamepad 恒 false）。
300	   */
301	  private getTargetTile(env: SmartSelectEnv): { tX: number; tY: number } {
302	    const tX = Math.floor(env.mouseX / 16);                     // :25
303	    let tY = Math.floor(env.mouseY / 16);                       // :26
304	    if (env.player.gravDir === -1) {                            // :27-30（反重力未实装，恒不达）
305	      // 原式 tY = (screenPosition.Y + screenHeight − mouseY) / 16（mouseY 为屏幕 px）
306	      const screenMouseY = env.mouseY - env.screenTopY;
307	      tY = Math.floor((env.screenTopY + env.screenHeight - screenMouseY) / 16);
308	    }
309	    return { tX, tY };
310	  }
311	
312	  /**
313	   * SmartSelect_GetAvailableToolRanges 1:1（Player.cs:17530-17562）。
314	   * 每类工具取背包 0-49 中第一件的 tileBoost；没有该类工具 = -10（负 reach → 永不可达，
315	   * 即"没带镐就不会出镐策略"的门）。原版全物品中 tileBoost≠0 的仅 195/196/-1、509/510/+20、
316	   * 1305/+1、3505-3510/-1、5329/5330/+3（Item.cs:3787/:7425/:16116/:31370-31411/:42229），
317	   * 均不属于六类 → 本作槽画像 tileBoost 恒 0，行为与原版一致。
318	   */
319	  private getAvailableToolRanges(env: SmartSelectEnv): {
320	    pickRange: number; axeRange: number; hammerRange: number;
321	    cannonRange: number; extractItemRange: number; paintScraperRange: number;
322	  } {
323	    let pickRange = -10, axeRange = -10, hammerRange = -10;    // :17537-17542
324	    let cannonRange = -10, extractItemRange = -10, paintScraperRange = -10;
325	    for (let i = 0; i < 50; i++) {                             // :17543
326	      const s = env.slots[i] ?? EMPTY_SLOT;
327	      if (s.pick > 0 && pickRange === -10) pickRange = s.tileBoost;        // :17545-17547
328	      if (s.axe > 0 && axeRange === -10) axeRange = s.tileBoost;           // :17548-17550
329	      if (s.hammer > 0 && hammerRange === -10) hammerRange = s.tileBoost;  // :17551-17553
330	      if (TORCH_ITEMS.has(s.vid) && cannonRange === -10) cannonRange = s.tileBoost;            // :17554-17556
331	      if (PAINT_SCRAPER_ITEMS.has(s.vid) && paintScraperRange === -10) paintScraperRange = s.tileBoost; // :17557-17559
332	      if (extractinatorModeOf(s.vid) !== -1 && extractItemRange === -10) extractItemRange = s.tileBoost;  // :17560-17562
333	    }
334	    return { pickRange, axeRange, hammerRange, cannonRange, extractItemRange, paintScraperRange };
335	  }
336	
337	  /**
338	   * SmartSelect_GetToolStrategy 1:1（Player.cs:17472-17528）。
339	   * 原版整段 try/catch 吞越界（:17478/:17526）；本作越界格按空 Tile 处理（TileStore OOB = 0），
340	   * 行为等价且无需异常控制流。
341	   */
342	  private getToolStrategy(tX: number, tY: number, env: SmartSelectEnv): { toolStrategy: number; wetTile: boolean } {
343	    let toolStrategy = 0;                                      // :17475
344	    let flag = false;                                          // :17476
345	    const st = env.st;
346	    const inB = st.inBounds(tX, tY);
347	    // :17480 wetTile：目标格有液体（Tile.liquid > 0；本作 liquid 通道 0-255 同义）
348	    const wetTile = inB ? st.liquid[st.idx(tX, tY)] > 0 : false;
349	    const tileType = inB ? st.get(tX, tY) : 0;
350	    if (tileType !== 0) {                                      // :17481 Main.tile.active()
351	      // 注意：active() = HasTile（含已致动格），不是 nactive()——TileStore.isActive 不可用
352	      const type = sheetOf(tileType);
353	      const r = this.getAvailableToolRanges(env);              // :17479
354	      if ((type === 219 || type === 642) && env.inRange(tX, tY, r.extractItemRange)) {
355	        toolStrategy = STRATEGY.EXTRACT;                       // :17486-17489
356	        flag = true;
357	      } else if (type === 209 && Math.floor(cannonFrameX(st, tX, tY) / 72) < 3
358	        && env.inRange(tX, tY, r.cannonRange)) {
359	        toolStrategy = STRATEGY.CANNON;                        // :17490-17492（frameX/72 整除 = 大炮样式 <3）
360	        flag = true;
361	      } else if (TILE_HAMMER_SHEETS.has(type) && env.inRange(tX, tY, r.hammerRange)) {
362	        toolStrategy = STRATEGY.HAMMER;                        // :17493-17495
363	        flag = true;
364	      } else if (TILE_AXE_SHEETS.has(type) && env.inRange(tX, tY, r.axeRange)) {
365	        toolStrategy = STRATEGY.AXE;                           // :17496-17498
366	        flag = true;
367	      } else if (type === 184 && env.inRange(tX, tY, r.paintScraperRange)) {
368	        toolStrategy = STRATEGY.PAINT_SCRAPER;                 // :17499-17501（长苔藓 → 刮漆）
369	        flag = true;
370	      } else if (env.inRange(tX, tY, r.pickRange)) {
371	        toolStrategy = STRATEGY.PICK;                          // :17502-17504
372	        flag = true;
373	      }
374	    } else if (wetTile && env.player.wet) {
375	      toolStrategy = STRATEGY.WET_LIGHT;                       // :17506-17508（湿格且自身湿 → 水下光源）
376	      flag = true;
377	    }
378	    if (!flag && env.player.wet) toolStrategy = STRATEGY.WET_LIGHT; // :17524-17527（兜底：湿身即水下光源）
379	    return { toolStrategy, wetTile };
380	  }
381	
382	  /**
383	   * SmartSelect_PickToolForStrategy 1:1（Player.cs:17321-17470）。
384	   * 在 inventory 0-49 找策略对应工具；无匹配返回 selectedItem（即"不切"）。
385	   */
386	  private pickToolForStrategy(
387	    tX: number, tY: number, toolStrategy: number, wetTile: boolean, env: SmartSelectEnv,
388	  ): number {
389	    let result = env.selectedItem;                             // :17323
390	    const selectedVid = env.slots[env.selectedItem]?.vid ?? 0; // inventory[selectedItem].type
391	    slotLoop: for (let i = 0; i < 50; i++) {                   // :17324
392	      const s = env.slots[i] ?? EMPTY_SLOT;
393	      const type = s.vid;                                      // :17326 inventory[i].type
394	      switch (toolStrategy) {
395	        case STRATEGY.TORCH: {                                 // :17339-17349
396	          if (TORCH_ITEMS.has(type)) { result = i; break; }    // 火把命中即定（后扫不换）
397	          if (GLOWSTICK_ITEMS.has(type)) result = i;           // 荧光棒先记候选
398	          continue;                                            // 继续找火把（火把优先级更高）
399	        }
400	        case STRATEGY.HAMMER: {                                // :17351-17355
401	          if (s.hammer <= 0) continue;
402	          result = i;
403	          break;
404	        }
405	        case STRATEGY.AXE: {                                   // :17357-17361
406	          if (s.axe <= 0) continue;
407	          result = i;
408	          break;
409	        }
410	        case STRATEGY.PICK: {                                  // :17363-17367
411	          if (s.pick <= 0) continue;
412	          result = i;
413	          break;
414	        }
415	        case STRATEGY.WET_LIGHT: {                             // :17369-17395
416	          if (!GLOWSTICK_ITEMS.has(type) && type !== FLARE_GUN
417	            && TORCH_ITEMS.has(type) && !WATER_TORCH_ITEMS.has(type)) {
418	            // 普通火把：手持已是火把则不动，否则记候选继续扫（给后面的荧光棒/水火把留机会）
419	            if (!TORCH_ITEMS.has(selectedVid)) result = i;
420	            continue;
421	          }
422	          if (GLOWSTICK_ITEMS.has(type) && wetTile) {
423	            result = i;
424	          } else if (type === FLARE_GUN && wetTile) {
425	            if (!this.hasAmmoFor(env, i)) continue;            // :17373-17384 弹药门（扫 57→0）
426	            result = i;
427	          } else {
428	            if (!WATER_TORCH_ITEMS.has(type)) continue;
429	            result = i;
430	          }
431	          break;
432	        }
433	        case STRATEGY.FAR_LIGHT: {                             // :17397-17423
434	          if (TORCH_ITEMS.has(type)) {
435	            // 手持已是火把则不动（放不到也保持火把），否则记候选继续扫
436	            if (!TORCH_ITEMS.has(selectedVid)) result = i;
437	            continue;
438	          }
439	          if (type === FLARE_GUN) {
440	            if (!this.hasAmmoFor(env, i)) continue;            // :17408-17420 弹药门
441	            result = i;
442	          } else {
443	            if (!GLOWSTICK_ITEMS.has(type)) continue;
444	            result = i;
445	          }
446	          break;
447	        }
448	        case STRATEGY.CANNON: {                                // :17425-17429
449	          if (!TORCH_ITEMS.has(type)) continue;                // 大炮点火 = 火把（PlaceThing_CannonBall :41139）
450	          result = i;
451	          break;
452	        }
453	        case STRATEGY.EXTRACT: {                               // :17431-17446
454	          // TryGettingItemTraderFromBlock（Player.cs:41043-41052）：仅 tile 642 叶绿提取机
455	          if (isChlorophyteTraderBlock(env, tX, tY) && chlorophyteTradeAccepts(s)) {
456	            result = i;
457	            break;
458	          }
459	          if (extractinatorModeOf(type) < 0) continue;         // :17441-17444
460	          result = i;
461	          break;
462	        }
463	        case STRATEGY.PAINT_SCRAPER: {                         // :17448-17452
464	          if (!PAINT_SCRAPER_ITEMS.has(type)) continue;
465	          result = i;
466	          break;
467	        }
468	        default:
469	          continue;                                            // :17454-17455
470	      }
471	      break slotLoop;                                          // :17457（C# switch 后的 break = 跳出 for）
472	    }
473	    return result;                                             // :17469
474	  }
475	
476	  /**
477	   * 信号枪弹药门 1:1（Player.cs:17374-17384 / :17410-17420）：
478	   * inventory[57..0] 中任一物品 ammo == 该槽 useAmmo 且 stack>0。
479	   * 荧光弹族的 useAmmo/ammo 提取缺口按原版源码补正（见 FLARE_GUN_USE_AMMO 注释）。
480	   */
481	  private hasAmmoFor(env: SmartSelectEnv, slotIndex: number): boolean {
482	    const useAmmo = flareUseAmmoOf(env.slots[slotIndex] ?? EMPTY_SLOT);
483	    for (let n = 57; n >= 0; n--) {
484	      const s = env.slots[n] ?? EMPTY_SLOT;
485	      if (flareAmmoOf(s) === useAmmo && s.stack > 0) return true;
486	    }
487	    return false;
488	  }
489	
490	  /** OverrideSelection 1:1（Player.cs:424-434） */
491	  private overrideSelection(item: number, host: SmartSelectHost): void {
492	    if (!host.canChangeImmediately || item === host.selected) return;   // :425-426
493	    if (this.overridden === -1) this.overridden = host.selected;        // :427-429 记住原槽
494	    if (item === this.overridden) this.overridden = -1;                 // :430-432 切回原槽 = 覆盖结束
495	    host.selected = item;                                               // :433
496	  }
497	}
498	
499	// ===================== 槽语义辅助（原版数据补正） =====================
500	
501	/** Item.useAmmo（信号枪族按 Item.cs:12108 补正） */
502	export function flareUseAmmoOf(s: SmartSelectSlot): number {
503	  return FLARE_GUN_USE_AMMO[s.vid] ?? s.useAmmo;
504	}
505	
506	/** Item.ammo（荧光弹族按 Item.cs:12121/:19106 补正） */
507	export function flareAmmoOf(s: SmartSelectSlot): number {
508	  return FLARE_AMMO_ITEMS.has(s.vid) ? AMMO_FLARE : s.ammo;
509	}
510	
511	/** ItemID.Sets.ExtractinatorMode[type]（ItemID.cs:1104；EXTRACTINATOR_MODE = 全表直录） */
512	function extractinatorModeOf(vid: number): number {
513	  return EXTRACTINATOR_MODE[vid] ?? -1;
514	}
515	
516	/** TryGettingItemTraderFromBlock（Player.cs:41043-41052）：tile 642 → ChlorophyteExtractinator */
517	function isChlorophyteTraderBlock(env: SmartSelectEnv, tX: number, tY: number): boolean {
518	  const st = env.st;
519	  if (!st.inBounds(tX, tY)) return false;
520	  return sheetOf(st.get(tX, tY)) === 642;
521	}
522	
523	/**
524	 * ItemTrader.TryGetTradeOption 1:1（ItemTrader.cs:66-80）：
525	 * 逐条 TradeOption 比较 TakingItemType == item.type && item.stack >= TakingItemStack。
526	 * ChlorophyteExtractinator 的 33 条选项全部 TakingItemStack=1（ItemTrader.cs:82-108，
527	 * Interchangable/CyclicLoop/FromAny 都经 AddOption_OneWay(taking, 1, giving, 1)），
528	 * 因此等价于"CHLOROPHYTE_TRADES 命中且 stack≥1"。
529	 */
530	function chlorophyteTradeAccepts(s: SmartSelectSlot): boolean {
531	  return s.stack >= 1 && CHLOROPHYTE_TRADES[s.vid] !== undefined;
532	}
533	
534	/** Tile.frameX（px；TileStore.frameX 通道与原版同单位——WldImport 直拷 wld 帧） */
535	function cannonFrameX(st: TileStore, x: number, y: number): number {
536	  return st.inBounds(x, y) ? st.frameX[st.idx(x, y)] : 0;
537	}
538	

```


---

## 🤖 Assistant · 2026-08-13T01:25:29.916Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
SmartCursor.ts is a very complete 1:1 port. Now let me look at Game.ts for the interaction distance (tileRange), quickHeal/quickMana/quickBuff, and how smart cursor integrates. Let me grep for specific things in Game.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:30.158Z · glm-x-preview-260804

```
SmartCursor/SmartSelect 移植非常完整。现在核对 Game.ts 侧的交互距离链与快捷键。
```


---

## 🤖 Assistant · 2026-08-13T01:25:31.157Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileRange\\|tileBoost\\|blockRange\\|quickHeal\\|quickMana\\|quickBuff\\|controlQuick\\|QuickHeal\\|QuickMana\\|QuickBuff\\|controlSmart\\|smartCursor\\|SmartCursor\\|builderAcc\\|buildingAcc\\|TileRange\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -60",
 "description": "Grep Game.ts for range and quick keys"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:31.186Z

**📎 ToolResult**

```
151:import { SmartCursor, smartCursorArrowAllowed, type SmartCursorSettings } from '../player/SmartCursor';
1202:    // TileReachCheckSettings.Simple 同款射程盒（inTileRange 口径：x 5 / y 3 + tileBoost）
1203:    const tb = (p.equipStats.tileRange ? 3 : 0) + (p.buffs.has(BuffType.Builder) ? 1 : 0);
1257:  /** 智能光标（SmartCursorHelper.cs 全量移植；状态机 + 39 策略链） */
1258:  smartCursor = new SmartCursor();
2039:    this.smartCursor.wanted = false;
2040:    this.smartCursor.showing = false;
2041:    VUI.smartCursorOn = false;
2694:    this.updateSmartCursor();
3664:   *  Player.cs QuickMana 原理同 QuickHeal；返回 true=已补蓝可重试施法） */
3785:  /** 智能光标设置（对齐原版 Player.SmartCursorSettings + Main.cs:49705 设置结构） */
3786:  private smartSettings(): SmartCursorSettings {
3789:      toggleMode: d.smartCursorMode === 'toggle',
3797:   * 智能光标每帧驱动（Player.cs:25159-25163 每帧 SmartCursorLookup + :28344-28374 Toggle/Hold 状态机）。
3801:  private updateSmartCursor() {
3803:    const sc = this.smartCursor;
3805:    const controlSmart = inp.down('ControlLeft') || inp.down('ControlRight');
3806:    if (sc.updateWanted(controlSmart, !!inp.mouseDown, s)) this.sfx.play('menuTick');
3810:    if (blocked || !sc.wanted) { sc.showing = false; VUI.smartCursorOn = false; return; }
3816:    // 放置物才有 blockRange（原版 SmartCursorLookup :95-98 createWall/createTile 才加）；
3817:    // 工具 tileBoost=0
3820:      ? (p.equipStats.tileRange ? 3 : 0) + (p.buffs.has(BuffType.Builder) ? 1 : 0)
3834:      tileBoost: tb,
3853:    VUI.smartCursorOn = sc.showing;
3884:        gravDir: 1,                              // 反重力未实装（同 SmartCursor 口径）
3891:      // IsInTileInteractionRange（Player.cs:31548，Simple 档 tileRangeX=5/tileRangeY=3 + TB）
3892:      inRange: (tx, ty, tb) => this.inTileRange(tx, ty, tb),
4032:    // 智能光标覆盖（SmartCursorHelper.cs:157-162）：只影响左键使用路径（挖掘/放置/电路工具），
4034:    if (this.smartCursor.showing) {
4035:      tx = this.smartCursor.x;
4036:      ty = this.smartCursor.y;
4138:      && this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) {
5006:   * （TileReachCheckSettings.cs:53）1:1：玩家盒外扩 tileRangeX=5 / tileRangeY=3
5007:   * （+tileBoost）的【矩形】判定（Simple 档 multiplier=1/上限 20）。非圆形距离 */
5008:  private inTileRange(tx: number, ty: number, tb = 0): boolean {
5094:    if (!this.inTileRange(tx, ty)) { this.mining = null; return; }
5818:    if (!this.inTileRange(tx, ty, 20)) return; // 原版多彩扳手/蓝图 tileBoost=20
5917:    if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) return;
5926:    // TileReplacement（Player.TileReplacementEnabled，cs:3225——builderAccStatus[10] 全程
5982:    if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) return;
6290:      if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) { this.input.rightDown = false; return; }
11290:      const sc = this.smartCursor;
11293:        // 否则传 null——渲染层见 null 即不画箭头（SmartCursor.smartCursorArrowAllowed）
11295:          && smartCursorArrowAllowed(this.world.store, sc.x, sc.y, sc.lockedDirection)

```


---

## 🤖 Assistant · 2026-08-13T01:25:31.707Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"quickHeal\\|quickMana\\|quickBuff\\|QuickHeal\\|QuickMana\\|QuickBuff\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" | head -30",
 "description": "Grep whole src for quick heal/mana/buff"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:31.744Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3664:   *  Player.cs QuickMana 原理同 QuickHeal；返回 true=已补蓝可重试施法） */

```


---

## 🤖 Assistant · 2026-08-13T01:25:41.492Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Interesting findings:
1. tileRange: Game.ts:1203, 5008 - tileRangeX=5/tileRangeY=3 + tileBoost
2. tileBoost = (equipStats.tileRange ? 3 : 0) + (Builder buff ? 1 : 0)

Wait — this is suspicious! In vanilla:
- Builder potion (buff) gives +1 tileBoost? Let me check. Actually in vanilla:
  - `Player.tileRangeX = 5; Player.tileRangeY = 3;` default
  - Accessories: Toolbelt (工具腰带) gives +1 block range → builderAccStatus... Actually let me check vanilla Player.cs.
  - Builder potion: the "Builder" buff increases block placement range by 1? Let me check. Actually the Builder buff gives +1 block range (tileBoost += 1). 
  - Toolbelt accessory: +1 range. Toolbelt is `builderAcc`? In Player.cs: `if (builderAccStatus[0]) tileBoost += 1;` etc.

Vanilla Player.cs has:
```csharp
public int tileRangeX = 5;
public int tileRangeY = 3;
```
And in ResetEffects or applyEquipEffects... Let me grep the decompiled source.

Also the implement uses `p.equipStats.tileRange ? 3 : 0` — that seems wrong! If tileRange is a boolean, then having the toolbelt gives +3?? Hmm, that's a numeric deviation: toolbelt should be +1, not +3. Need to check what equipStats.tileRange is in this repo. Maybe it's an accessory "Toolbelt + Portable Cement Mixer"? Actually there's a combo "Toolbelt" (+1 range). Hmm, `? 3 : 0` suggests maybe it's intentional to mimic "砖层放置范围"? Let me look at vanilla:

In vanilla Player.cs, tileBoost comes from:
```csharp
if (builderAccStatus[0]) tileBoost++;
if (builderAccStatus[1]) tileBoost++;
...
```
Actually the exact vanilla code (1.4.4 Player.cs, ItemCheck / ApplyEquipFunctional?) Let me grep.

From memory of Terraria source (Player.cs, `Player.TileRangeValidation`?):

```csharp
public int blockRange => tileRangeX + tileBoost? 
```

Actually vanilla:
```csharp
public int tileRangeX = 5;
public int tileRangeY = 3;
```
And `Player.tileBoost`:
```csharp
public int tileBoost {
    get {
        int num = 0;
        if (builderAccStatus[2]) num++;  // Architect goggle?
        ...
    }
}
```

Let me actually grep the decompiled source for tileBoost and builderAcc.

Also quickHeal/quickMana/quickBuff: only a comment at 3664 about QuickMana. So H/J/B quick keys are likely NOT implemented. Let me check Input.ts for key bindings, and check Options.ts.

Also multiplayer distance — this repo has multiplayer but range check client-side.

Let me now grep the vanilla source for tileRangeX/tileRangeY defaults and tileBoost computation.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:41.951Z · glm-x-preview-260804

```
关键疑点:实现里 tileBoost = `tileRange?3:0` + Builder+1。查原版 tileBoost 链与 QuickHeal/QuickBuff。
```


---

## 🤖 Assistant · 2026-08-13T01:25:42.979Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"tileRangeX = \\|tileRangeY = \\|tileRangeX=\\|tileRangeY=\" Player.cs | head -10; echo \"---tileBoost---\"; grep -n \"int tileBoost\\|tileBoost =>\" Player.cs | head; echo \"---builderAcc---\"; grep -n \"builderAccStatus\\[\" Player.cs | head -20",
 "description": "Grep vanilla Player.cs for range defaults"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:43.035Z

**📎 ToolResult**

```
2364:	public static int tileRangeX = DefaultTileRangeX;
2366:	public static int tileRangeY = DefaultTileRangeY;
18633:			tileRangeX = DefaultTileRangeX;
18634:			tileRangeY = DefaultTileRangeY;
---tileBoost---
---builderAcc---
3225:	public bool TileReplacementEnabled => builderAccStatus[10] == 0;
3796:			return builderAccStatus[11] == 0;
3800:			builderAccStatus[11] = ((!value) ? 1 : 0);
38966:			if (autoPaint && builderAccStatus[3] == 0)
39046:				if (autoPaint && builderAccStatus[3] == 0)
39164:			if (autoPaint && builderAccStatus[3] == 0)
39973:				if (autoPaint && builderAccStatus[3] == 0)
39977:				if (!autoActuator || builderAccStatus[2] != 0)
53950:			fileIO.Write(newPlayer.builderAccStatus[num9]);
54696:				newPlayer.builderAccStatus[num35] = fileIO.ReadInt32();
54700:				newPlayer.builderAccStatus[0] = 1;
54715:					newPlayer.builderAccStatus[1] = 1;
55137:		builderAccStatus[0] = 1;

```


---

## 🤖 Assistant · 2026-08-13T01:25:43.671Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"QuickHeal\\|QuickMana\\|QuickBuff\\|QuickMount\\|controlQuick\" Player.cs PlayerInput.cs Main.cs 2>/dev/null | head -30",
 "description": "Grep vanilla for quick heal/mana/buff"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:43.719Z

**📎 ToolResult**

```
Player.cs:1650:	public bool releaseQuickMana;
Player.cs:1652:	public bool releaseQuickHeal;
Player.cs:1678:	public bool controlQuickMana;
Player.cs:1680:	public bool controlQuickHeal;
Player.cs:5268:	public void QuickHeal()
Player.cs:5274:		Item item = QuickHeal_GetItemToUse();
Player.cs:5316:	public Item QuickHeal_GetItemToUse()
Player.cs:5323:			QuickHeal_GetItemToUse_TryChoosingItem(lifeDifference, ref bestItem, ref bestDifference, inventory[i]);
Player.cs:5329:				QuickHeal_GetItemToUse_TryChoosingItem(lifeDifference, ref bestItem, ref bestDifference, bank4.item[j]);
Player.cs:5335:	private static void QuickHeal_GetItemToUse_TryChoosingItem(int lifeDifference, ref Item bestItem, ref int bestDifference, Item nextItem)
Player.cs:5365:	public void QuickMana()
Player.cs:5371:		Item item = QuickMana_GetItemToUse();
Player.cs:5396:	public Item QuickMana_GetItemToUse()
Player.cs:5453:	public void QuickBuff()
Player.cs:5464:		Item item = QuickBuff_PickBestFoodItem();
Player.cs:5493:				if (QuickBuff_ShouldUseItem(item2, out var btype))
Player.cs:5500:					QuickBuff_UseItemForBuff(item2, btype);
Player.cs:5514:				if (QuickBuff_ShouldUseItem(item3, out var btype2))
Player.cs:5521:					QuickBuff_UseItemForBuff(item3, btype2);
Player.cs:5535:	private void QuickBuff_UseItemForBuff(Item item, int btype)
Player.cs:5553:	private bool QuickBuff_ShouldUseItem(Item item, out int btype)
Player.cs:5565:		bool flag = QuickBuff_ShouldBotherUsingThisBuff(btype);
Player.cs:5601:	private Item QuickBuff_PickBestFoodItem()
Player.cs:5609:				int num2 = QuickBuff_FindFoodPriority(buffType[i]);
Player.cs:5621:				int num3 = QuickBuff_FindFoodPriority(item2.buffType);
Player.cs:5636:					int num4 = QuickBuff_FindFoodPriority(item3.buffType);
Player.cs:5648:	private int QuickBuff_FindFoodPriority(int buffType)
Player.cs:5659:	private bool QuickBuff_ShouldBotherUsingThisBuff(int attemptedType)
Player.cs:5728:	public void QuickMount()
Player.cs:5761:			Item item = QuickMount_GetItemToUse();

```


---

## 🤖 Assistant · 2026-08-13T01:25:45.735Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla tileRangeX = DefaultTileRangeX. Let me find DefaultTileRangeX value, and the tileBoost chain. Also check QuickHeal etc. in implementation (probably not implemented). Let me search the decompiled source.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:46.293Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"DefaultTileRangeX\\|DefaultTileRangeY\" Player.cs | head -5; echo \"---tileBoost prop---\"; grep -n \"tileBoost\" Player.cs | head -25",
 "description": "Find default range and tileBoost chain"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:46.347Z

**📎 ToolResult**

```
2360:	public static readonly int DefaultTileRangeX = 5;
2362:	public static readonly int DefaultTileRangeY = 3;
2364:	public static int tileRangeX = DefaultTileRangeX;
2366:	public static int tileRangeY = DefaultTileRangeY;
18633:			tileRangeX = DefaultTileRangeX;
---tileBoost prop---
17542:				pickRange = inventory[i].tileBoost;
17546:				axeRange = inventory[i].tileBoost;
17550:				hammerRange = inventory[i].tileBoost;
17554:				cannonRange = inventory[i].tileBoost;
17558:				paintScraperRange = inventory[i].tileBoost;
17562:				extractItemRange = inventory[i].tileBoost;
38939:		if (inventory[selectedItem].createWall < 0 || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, inventory[selectedItem].tileBoost + blockRange))
39058:		if (tileToCreate < 0 || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, item.tileBoost + blockRange) || !SmartCursorHelper.TileTargetDesired())
40950:		if (!tile.active() || item.type != 5328 || !TileID.Sets.IsAContainer[tile.type] || tile.type == 88 || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, item.tileBoost + blockRange) || !ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem)
41012:		if (!tile.active() || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, item.tileBoost + blockRange) || !ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem)
41055:		if (inventory[selectedItem].type < 1874 || inventory[selectedItem].type > 1905 || !Main.tile[tileTargetX, tileTargetY].active() || Main.tile[tileTargetX, tileTargetY].type != 171 || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, inventory[selectedItem].tileBoost + blockRange) || !ItemTimeIsZero || itemAnimation <= 0 || !controlUseItem)
41140:		if (ItemID.Sets.Torches[inventory[selectedItem].type] && IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, inventory[selectedItem].tileBoost + blockRange))
41154:		if (ItemID.Sets.IsPaintScraper[inventory[selectedItem].type] && IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, inventory[selectedItem].tileBoost + blockRange))
41238:		if ((inventory[selectedItem].type != 1072 && inventory[selectedItem].type != 1544) || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, inventory[selectedItem].tileBoost + blockRange))
41256:		if ((inventory[selectedItem].type != 1071 && inventory[selectedItem].type != 1543) || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, inventory[selectedItem].tileBoost + blockRange))
42929:			if (!Main.GamepadDisableCursorItemIcon && IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
43384:		else if (IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
45701:		return IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost);
45706:		if (((sItem.type < 205 || sItem.type > 207) && sItem.type != 1128 && sItem.type != 3031 && sItem.type != 3032 && sItem.type != 4820 && sItem.type != 4872 && sItem.type != 5302 && sItem.type != 5303 && sItem.type != 5304 && sItem.type != 5364) || noBuilding || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
46154:		if ((sItem.type != 509 && sItem.type != 510 && sItem.type != 849 && sItem.type != 850 && sItem.type != 851 && sItem.type != 3612 && sItem.type != 3620 && sItem.type != 3625) || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost + blockRange))
46371:		if (sItem.type == 4049 && IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost + blockRange) && itemAnimation > 0 && ItemTimeIsZero && controlUseItem)
51852:		if (!IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))

```


---

## 🤖 Assistant · 2026-08-13T01:25:47.621Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"key === 'KeyH'\\|KeyH\\|KeyJ\\|KeyB'\\|quickHeal\\|QuickHeal\\|healPotion\\|manaPotion\" ~/Project/GLM/SandboxWorld/game/src/core/Input.ts ~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts 2>/dev/null | head -20; echo \"---equipStats tileRange---\"; grep -rn \"tileRange\" ~/Project/GLM/SandboxWorld/game/src/stats/*.ts ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts | head -20",
 "description": "Grep implementation for H/J/B keys and tileRange stat"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:47.705Z

**📎 ToolResult**

```
---equipStats tileRange---
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:251:    tileSpeed: boolean; wallSpeed: boolean; tileRange: boolean; pStone: boolean;
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:302:    let tileSpeed = false, wallSpeed = false, tileRange = false, skyStone = false, pStone = false, counterWeight = false;
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:379:        if (fx.tileRange) tileRange = true;
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:508:      tileSpeed, wallSpeed, tileRange, pStone, counterWeight,

```


---

## 🤖 Assistant · 2026-08-13T01:25:50.280Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need to find `blockRange` in vanilla Player.cs. It's a property. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:25:50.389Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"int blockRange\\|blockRange =>\" Player.cs | head -3",
 "description": "Locate blockRange property in Player.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:50.421Z

**📎 ToolResult**

```
2604:	public int blockRange;

```


---

## 🤖 Assistant · 2026-08-13T01:25:52.097Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"blockRange\" Player.cs | grep -v \"IsInTileInteractionRange\\|tileBoost\" | head -20",
 "description": "Find blockRange writes in Player.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:52.148Z

**📎 ToolResult**

```
2604:	public int blockRange;
9844:				blockRange++;
14877:			blockRange++;
18510:		blockRange = 0;

```


---

## 🤖 Assistant · 2026-08-13T01:25:54.522Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '9830,9850p' Player.cs; echo \"====14870====\"; sed -n '14860,14885p' Player.cs; echo \"====18500====\"; sed -n '18500,18515p' Player.cs",
 "description": "Read blockRange increment contexts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:25:54.582Z

**📎 ToolResult**

```
				fishingSkill += 15;
			}
			else if (buffType[j] == 122)
			{
				sonarPotion = true;
			}
			else if (buffType[j] == 123)
			{
				cratePotion = true;
			}
			else if (buffType[j] == 107)
			{
				tileSpeed += 0.25f;
				wallSpeed += 0.25f;
				blockRange++;
			}
			else if (buffType[j] == 108)
			{
				kbBuff = true;
			}
			else if (buffType[j] == 109)
====14870====
				hideWolf = true;
			}
		}
		if (currentItem.type == 1865 || currentItem.type == 3110)
		{
			skyStoneEffects = true;
		}
		if (currentItem.type == 899 && Main.dayTime)
		{
			skyStoneEffects = true;
		}
		if (currentItem.type == 900 && (!Main.dayTime || Main.eclipse))
		{
			skyStoneEffects = true;
		}
		if (currentItem.type == 407)
		{
			blockRange++;
		}
		if (currentItem.type == 489)
		{
			magicDamage += 0.15f;
		}
		if (currentItem.type == 490)
		{
			meleeDamage += 0.15f;
====18500====
		drippingSparkleSlime = false;
		burned = false;
		suffocating = false;
		onFire2 = false;
		onFire3 = false;
		onFrostBurn = false;
		onFrostBurn2 = false;
		frostBurn = false;
		noItems = false;
		cursed = false;
		blockRange = 0;
		pickSpeed = 1f;
		wereWolf = false;
		rulerGrid = false;
		rulerLine = true;
		bleed = false;

```


---

## 🤖 Assistant · 2026-08-13T01:25:59.500Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the vanilla blockRange chain:
- buffType[j] == 107 (Builder potion) → blockRange++ (tileSpeed += 0.25, wallSpeed += 0.25, blockRange++)
- currentItem.type == 407 (Toolbelt, 工具腰带) → blockRange++

So vanilla blockRange max = 2 (Toolbelt +1, Builder buff +1).

Now in implementation Game.ts:1203: `const tb = (p.equipStats.tileRange ? 3 : 0) + (p.buffs.has(BuffType.Builder) ? 1 : 0);`

So tileRange (Toolbelt) gives +3, Builder gives +1. Vanilla: Toolbelt +1, Builder +1. That's a numeric deviation! Toolbelt should be +1, not +3.

Wait, let me check Player.ts:379 `if (fx.tileRange) tileRange = true;` — which accessories set tileRange in vanillaAccFx.ts. Let me check.

Also, let me check what items have fx.tileRange. In vanilla, blockRange is incremented by item 407 (Toolbelt). Only toolbelt. Let me verify vanillaAccFx.

Let me also check BuffType.Builder in implementation — is Builder = 107?

Then let me verify the inTileRange implementation vs TileReachCheckSettings.

Let me read Game.ts around 1195-1270, 3780-3900, 4020-4150, 5000-5110, and 5900-6000, 6290.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:00.078Z · glm-x-preview-260804

```
原版 blockRange 链确认:Builder 药水(buff 107)+1、工具腰带(item 407)+1。现查实现侧 tileRange 数值来源与 inTileRange 公式。
```


---

## 🤖 Assistant · 2026-08-13T01:26:00.656Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tileRange\" ~/Project/GLM/SandboxWorld/game/src/data/vanillaAccFx.ts | head; echo \"---Builder buff---\"; grep -n \"Builder\" ~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts | head -5",
 "description": "Check tileRange accessory fx and Builder buff id"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:00.691Z

**📎 ToolResult**

```
61:  tileRange?: number;    // 工具/放置射程 +
---Builder buff---
55:  Builder = 32,       // 建筑工(107,900s)：tileSpeed+0.25/wallSpeed+0.25/blockRange+1（:9841）
171:  [BuffType.Builder]: { vanillaBuff: 107, descKey: 'Mods.SandboxWorld.Buff.Builder.Desc', fallbackName: '建筑工' },

```


---

## 🤖 Assistant · 2026-08-13T01:26:01.138Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1195,1215p;5000,5030p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read inTileRange implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:01.161Z

**📎 ToolResult**

```
  /** QuickMinecart（Player.cs:5796-5827）：射程内取视线可达的最近轨道格上车 */
  private tryQuickMinecart(): void {
    if (this.minecart) return;
    const st = this.world.store;
    const p = this.player;
    const ptx = Math.floor(p.cx / TILE), pty = Math.floor(p.cy / TILE);
    // TileReachCheckSettings.Simple 同款射程盒（inTileRange 口径：x 5 / y 3 + tileBoost）
    const tb = (p.equipStats.tileRange ? 3 : 0) + (p.buffs.has(BuffType.Builder) ? 1 : 0);
    const rx = Math.min(20, 5) + tb, ry = Math.min(20, 3) + tb;
    let best: { x: number; y: number } | null = null;
    let bestD = Infinity;
    for (let x = ptx - rx; x <= ptx + rx; x++) {
      for (let y = pty - ry; y <= pty + ry; y++) {
        if (!st.inBounds(x, y) || st.type[st.idx(x, y)] !== this.trackTile) continue;
        const wx = x * TILE + 8, wy = y * TILE + 8;
        const d = Math.hypot(wx - p.cx, wy - p.cy);
        if (d < bestD && canHitLine(st, p.cx, p.cy, 0, 0, wx, wy, 0, 0)) {
          bestD = d;
          best = { x, y };
        }
    if (toolType === 'pick') return d.pick >= 0 && power >= d.pick;
    if (toolType === 'axe') return d.axe >= 0;
    return false;
  }

  /** 原版 IsInTileInteractionRange（Player.cs:31548）+ GetTileRegion
   * （TileReachCheckSettings.cs:53）1:1：玩家盒外扩 tileRangeX=5 / tileRangeY=3
   * （+tileBoost）的【矩形】判定（Simple 档 multiplier=1/上限 20）。非圆形距离 */
  private inTileRange(tx: number, ty: number, tb = 0): boolean {
    const p = this.player;
    const x = Math.min(20, 5) + tb, y = Math.min(20, 3) + tb;
    const LX = Math.floor(p.x / TILE) - x;
    const HX = Math.ceil((p.x + p.w) / TILE) - 1 + x;
    const LY = Math.floor(p.y / TILE) - y;
    const HY = Math.ceil((p.y + p.h) / TILE) - 1 + y;
    return tx >= LX && tx <= HX && ty >= LY && ty <= HY;
  }

  /** 砸祭坛 = 原版 KillTile case 26 → SmashAltar（WorldGen.cs:48949）1:1：
   *  altarCount%3 选矿档(0 钴/钯、1 秘银/山铜、2 精金/钛)，/3+1 为波次衰减；
   *  矿脉数 num3 = w/4200×310 − 85×档 ×0.85 ÷ 波次——钴档恒 ×1.05（:49008），
   *  锁定到替代矿(221/222/223)再 ×0.9（:48991 等,替代矿更稀有）；
   *  矿种按世界锁定（SavedOreTiers :48981-49030：每档首砸 roll 一次 genRand.Next(2)==0
   *  → 替代矿,此后全世界固定,随存档持久化 world.savedOreTiers——此前每砸重 roll
   *  会导致同世界混出钴+钯）；深度带按锁定矿种（:49033-49040：107/221=地表线、
   *  108/222=岩层、111/223=(岩层×2+h)/3）；每脉 OreRunner Next(5,10) 恒定（:49045,
   *  旧实现的 5..9+w/4200 是误读）;最后生成 1-2 只幽灵(82)。祭坛 3×2 整体移除。
   *  计数存 world.altarCount（原版 WorldGen.altarCount 静态位，WorldFile.cs:1303/2100
   *  随存档持久化——跨会话保留；海盗入侵自然 roll 的 >0 门同源 Main.cs:64938） */
  private smashAltar(tx: number, ty: number): void {
    const st = this.world.store;

```


---

## 🤖 Assistant · 2026-08-13T01:26:03.269Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now check vanillaAccFx.ts:61 — `tileRange?: number` — so it's a number field. But Player.ts:379 `if (fx.tileRange) tileRange = true;` flattens it to boolean. And Game.ts:1203 treats tileRange as +3. Let me check which items have tileRange in vanillaAccFx and its value.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:04.052Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -B2 -A2 \"tileRange\" ~/Project/GLM/SandboxWorld/game/src/data/vanillaAccFx.ts | head -30; echo \"===Player.ts 370-385===\"; sed -n '370,385p' ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts",
 "description": "Find which items grant tileRange"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:04.085Z

**📎 ToolResult**

```
59-  tileSpeed?: number;    // 采矿/放置加速
60-  wallSpeed?: number;    // 铺墙加速
61:  tileRange?: number;    // 工具/放置射程 +
62-  skyStone?: number;     // 天界石族：全属性复合（:12558）
63-  counterWeight?: number; // 配重球（悠悠球命中触发）
===Player.ts 370-385===
        if (fx.goldRing) goldRing = true;
        if (fx.luckyCoin) luckyCoin = true;
        if (fx.discount) discount = true;
        if (fx.ammoSave || fx.huntressSave) ammoSave = true;
        if (fx.kbGlove) kbGlove = true;
        if (fx.autoReuseGlove) autoReuseGlove = true;   // 力量手套族：近战自动连挥
        if (fx.yoyoString) yoyoString = true;
        if (fx.tileSpeed) tileSpeed = true;
        if (fx.wallSpeed) wallSpeed = true;
        if (fx.tileRange) tileRange = true;
        if (fx.skyStone) skyStone = true;
        if (fx.pStone) pStone = true;
        if (fx.manaMagnet) manaMagnet = true;
        if (fx.magicCuffs) magicCuffs = true;
        if (fx.manaFlower) manaFlower = true;
        if (fx.manaRegenBonus) manaRegenBonus += fx.manaRegenBonus;           // 魔力斗篷 982（:14383）

```


---

## 🤖 Assistant · 2026-08-13T01:26:05.321Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me check where tileRange is set in vanillaAccFx data — which items. Let me grep for the fx assignments in the data table.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:06.343Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"tileRange\" ~/Project/GLM/SandboxWorld/game/src/data/*.ts ~/Project/GLM/SandboxWorld/game/src/**/*.json 2>/dev/null | grep -v \"vanillaAccFx.ts\\|Player.ts\\|Game.ts\\|Options.ts\\|Settings.ts\\|Renderer.ts\\|VUI.ts\\|SmartSelect\\|SmartCursor\" | head -10",
 "description": "Find tileRange in item data tables"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:06.383Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/data/vanilla-accfx.json:701:    "tileRange": 1
~/Project/GLM/SandboxWorld/game/src/data/vanilla-accfx.json:803:    "tileRange": 1
~/Project/GLM/SandboxWorld/game/src/data/vanilla-accfx.json:1017:    "tileRange": 1

```


---

## 🤖 Assistant · 2026-08-13T01:26:08.896Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/src/data/vanilla-accfx.json'))\nprint(type(d), list(d.keys())[:5] if isinstance(d,dict) else len(d))\n\" ; grep -n -B12 '\"tileRange\": 1' ~/Project/GLM/SandboxWorld/game/src/data/vanilla-accfx.json | grep '\"id\"\\|\"vid\"\\|\"key\"\\|tileRange' | head -12",
 "description": "Identify items granting tileRange=1"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:16.318Z

**📎 ToolResult**

```
<class 'dict'> ['53', '54', '100', '101', '102']
701:    "tileRange": 1
803:    "tileRange": 1
1017:    "tileRange": 1

```


---

## 🤖 Assistant · 2026-08-13T01:26:17.926Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/src/data/vanilla-accfx.json'))\nfor k,v in d.items():\n    if isinstance(v,dict) and v.get('tileRange'):\n        print('item vid',k,'tileRange=',v['tileRange'])\n\"",
 "description": "List items with tileRange flag"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:37.228Z

**📎 ToolResult**

```
item vid 2215 tileRange= 1
item vid 3061 tileRange= 1
item vid 5126 tileRange= 1

```


---

## 🤖 Assistant · 2026-08-13T01:26:40.847Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Item 2215 = Toolbox? Let me check: 
- 407 = Toolbelt (工具腰带) → vanilla blockRange++
- 2215 = Presserator (压力器)
- 3061 = Architect Gizmo Pack (建筑师小工具包)? 
- 5126 = ?

Actually in vanilla 1.4.4:
- Toolbelt (407): +1 block range
- Presserator (2215): auto-actuator placement
- Architect Gizmo Pack (3061): combination of Toolbelt+Presserator+... actually the Architect Gizmo Pack includes toolbelt effects
- Hand Of Creation (5126): combination item including Toolbox

Wait, let me check vanilla code for those. In Player.cs ApplyEquip / currentItem checks:
- 407 → blockRange++ (toolbelt)
- Let me check 2215, 3061, 5126.

Let me grep vanilla Player.cs for 2215, 3061, 5126.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:41.867Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"currentItem.type == 407\\|type == 2215\\|type == 3061\\|type == 5126\\|type == 4004\" Player.cs | head -10; echo \"---context 2215---\"; grep -n -A4 \"currentItem.type == 2215\" Player.cs | head -12",
 "description": "Check vanilla range items blockRange effects"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:41.893Z

**📎 ToolResult**

```
9319:		bool num = armorItem.wingSlot > 0 || armorItem.type == 934 || armorItem.type == 4341 || armorItem.type == 5126 || armorItem.type == 4563 || armorItem.type == 1987;
9430:		if (armorItem.type == 4341 || armorItem.type == 5126)
14718:		if (currentItem.type == 2215)
14730:		if (currentItem.type == 3061)
14737:		if (currentItem.type == 5126)
14875:		if (currentItem.type == 407)
15505:		if (currentItem.type == 4078)
15509:		if (currentItem.type == 4079)
15513:		if (currentItem.type == 4077)
---context 2215---
14718:		if (currentItem.type == 2215)
14719-		{
14720-			equippedAnyTileRangeAcc = true;
14721-		}
14722-		if (currentItem.type == 2216)

```


---

## 🤖 Assistant · 2026-08-13T01:26:43.431Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: `equippedAnyTileRangeAcc`. Let me read lines 14710-14745 to see what 2215/3061/5126 do, and find where `equippedAnyTileRangeAcc` is used.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:43.994Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '14710,14745p' Player.cs; echo \"===equippedAnyTileRangeAcc uses===\"; grep -n \"equippedAnyTileRangeAcc\" Player.cs | head",
 "description": "Read range accessory handling in vanilla"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:44.023Z

**📎 ToolResult**

```
			{
				Lighting.AddLight((int)base.Center.X / 16, (int)base.Center.Y / 16, 0.4f, 1.2f, 1.8f);
			}
		}
		if (currentItem.type == 2214)
		{
			equippedAnyTileSpeedAcc = true;
		}
		if (currentItem.type == 2215)
		{
			equippedAnyTileRangeAcc = true;
		}
		if (currentItem.type == 2216)
		{
			autoPaint = true;
		}
		if (currentItem.type == 2217)
		{
			equippedAnyWallSpeedAcc = true;
		}
		if (currentItem.type == 3061)
		{
			equippedAnyWallSpeedAcc = true;
			equippedAnyTileSpeedAcc = true;
			autoPaint = true;
			equippedAnyTileRangeAcc = true;
		}
		if (currentItem.type == 5126)
		{
			equippedAnyWallSpeedAcc = true;
			equippedAnyTileSpeedAcc = true;
			autoPaint = true;
			equippedAnyTileRangeAcc = true;
			treasureMagnet = true;
			chiselSpeed = true;
		}
===equippedAnyTileRangeAcc uses===
2900:	public bool equippedAnyTileRangeAcc;
12539:		equippedAnyTileRangeAcc = false;
12618:		if (equippedAnyTileRangeAcc && whoAmI == Main.myPlayer)
14720:			equippedAnyTileRangeAcc = true;
14735:			equippedAnyTileRangeAcc = true;
14742:			equippedAnyTileRangeAcc = true;

```


---

## 🤖 Assistant · 2026-08-13T01:26:45.441Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '12610,12630p' Player.cs",
 "description": "Read equippedAnyTileRangeAcc consumer"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:45.479Z

**📎 ToolResult**

```
		if (chiselSpeed)
		{
			pickSpeed -= 0.25f;
		}
		if (equippedAnyWallSpeedAcc)
		{
			wallSpeed += 0.5f;
		}
		if (equippedAnyTileRangeAcc && whoAmI == Main.myPlayer)
		{
			tileRangeX += 3;
			tileRangeY += 2;
		}
		if (!accThirdEye)
		{
			accThirdEyeCounter = 0;
		}
		RefreshInfoAccsFromTeamPlayers();
		if (whoAmI == Main.myPlayer && hasLuck_LuckyClover)
		{
			equipmentBasedLuckBonus += 0.03f;

```


---

## 🤖 Assistant · 2026-08-13T01:26:51.295Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent! This is a key vanilla fact: `equippedAnyTileRangeAcc` → tileRangeX += 3 AND tileRangeY += 2 (not blockRange!). And this only applies to whoAmI == Main.myPlayer (local player).

So vanilla has TWO distinct range bonuses:
1. **Toolbelt (407)**: blockRange++ → used only in placement contexts (item.tileBoost + blockRange) — applies to mining too? No wait — blockRange is used in `IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, item.tileBoost + blockRange)` in PlaceThing contexts. Let me check what mining uses — Player.TryHittingWall/Player.ItemCheck_UseMiningTools. Let me check which calls use blockRange vs plain tileBoost.

From grep:
- 38939 (place wall), 39058 (place tile), 40950 (chest rename?), 41012, 41055, 41140 (torch), 41154 (paint scraper), 41238, 41256, 46154 (wrenches), 46371 (lawnmower) → use `item.tileBoost + blockRange`
- 42929, 43384, 45701, 45706, 51852 → use `sItem.tileBoost` only (no blockRange)

So which is mining? Let me check line 45701/45706 and 51852. 45706 mentions noBuilding... Let me check ItemCheck for mining. Actually, mining is in Player.ItemCheck_UseMiningTools which calls CanUseMiningTools — hmm. Let me grep for where mining validates range.

Let me check 43384 and 51852 contexts.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:52.058Z · glm-x-preview-260804

```
关键原版事实:`equippedAnyTileRangeAcc → tileRangeX+=3 且 tileRangeY+=2`(非 blockRange);工具腰带 407 是 `blockRange++`。两者作用域不同,需分清挖掘/放置各自用哪条。
```


---

## 🤖 Assistant · 2026-08-13T01:26:53.060Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && echo \"===43370-43390===\"; sed -n '43370,43390p' Player.cs; echo \"===45690-45712===\"; sed -n '45690,45712p' Player.cs; echo \"===51845-51858===\"; sed -n '51845,51858p' Player.cs",
 "description": "Read range-check call sites in vanilla"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:53.188Z

**📎 ToolResult**

```
===43370-43390===
			else
			{
				NetMessage.SendData(61, -1, -1, null, whoAmI, -5f);
			}
		}
	}

	private void ItemCheck_ReleaseCritter(Item sItem)
	{
		if (sItem.makeNPC == 614)
		{
			ApplyItemTime(sItem);
			NPC.ReleaseNPC((int)base.Center.X, (int)base.Bottom.Y, sItem.makeNPC, sItem.placeStyle, whoAmI);
		}
		else if (IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
		{
			int num = (int)Main.MouseWorld.X;
			int num2 = (int)Main.MouseWorld.Y;
			int i = num / 16;
			int j = num2 / 16;
			if (!WorldGen.SolidTile(i, j))
===45690-45712===
			WorldGen.PoundTile(x, y);
			if (Main.netMode == 1)
			{
				NetMessage.SendData(17, -1, -1, null, 7, x, y, 1f);
			}
		}
		poundRelease = false;
	}

	public bool IsTargetTileInItemRange(Item sItem)
	{
		return IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost);
	}

	private void ItemCheck_UseBuckets(Item sItem)
	{
		if (((sItem.type < 205 || sItem.type > 207) && sItem.type != 1128 && sItem.type != 3031 && sItem.type != 3032 && sItem.type != 4820 && sItem.type != 4872 && sItem.type != 5302 && sItem.type != 5303 && sItem.type != 5304 && sItem.type != 5364) || noBuilding || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
		{
			return;
		}
		if (!Main.GamepadDisableCursorItemIcon)
		{
			cursorItemIconEnabled = true;
===51845-51858===
		{
			return;
		}
		if (sItem.useStyle == 0)
		{
			releaseUseItem = false;
		}
		if (!IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
		{
			return;
		}
		int num = tileTargetX;
		int num2 = tileTargetY;
		if (!Main.tile[num, num2].active() || (Main.tile[num, num2].type != 128 && Main.tile[num, num2].type != 269))

```


---

## 🤖 Assistant · 2026-08-13T01:26:56.121Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need to find what mining (TryUsingItem / ItemCheck for pickaxe) uses. Let me look at Player.ItemCheck_UseMiningTools or ItemCheck_TryUsingItem. Grep for "ItemCheck" around the pickaxe.

Also need to find tileTargetX/tileTargetY assignment (Main.tileTarget / Player tileTarget update) to check smart cursor override.

Let me grep for ItemCheck in Player.cs near mining.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:26:56.821Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"void ItemCheck_UseMiningTools\\|void ItemCheck_TryUsingItem\\|bool ItemCheck_CanUseTile\\|void ItemCheck\" Player.cs | head -20",
 "description": "List ItemCheck methods in vanilla Player.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:26:56.902Z

**📎 ToolResult**

```
31068:	public void ItemCheck_ManageRightClickFeatures()
31221:	public void ItemCheck_ManageRightClickFeatures_ShieldRaise(bool theGeneralCheck)
31314:	private void ItemCheckWrapped(int i)
41949:	public void ItemCheck()
42775:	private void ItemCheck_OwnerOnlyCode(ref ItemCheckContext context, Item sItem, int weaponDamage, Rectangle heldItemFrame)
43033:	private void ItemCheck_EmitFoodParticles(Item sItem)
43052:	private void ItemCheck_EmitDrinkParticles(Item sItem)
43071:	private void ItemCheck_UseBossSpawners(int onWhichPlayer, Item sItem)
43241:	private void ItemCheck_UseEventItems(Item sItem)
43377:	private void ItemCheck_ReleaseCritter(Item sItem)
43398:	private void ItemCheck_MeleeHitPVP(Item sItem, Rectangle itemRectangle, int damage, float knockBack)
43571:	private void ItemCheck_MeleeHitNPCs(Item sItem, Rectangle itemRectangle, int originalDamage, float knockBack)
43915:	private void ItemCheck_EmitHammushProjectiles(int i, Item sItem, Rectangle itemRectangle, int damage)
44009:	private void ItemCheck_CutTiles(Item sItem, Rectangle itemRectangle, bool[] shouldIgnore, bool cutExtraTiles = false)
44079:	private void ItemCheck_CatchCritters(Item sItem, Rectangle itemRectangle)
44126:	private void ItemCheck_EmitUseVisuals(Item sItem, Rectangle itemRectangle)
44429:	private void ItemCheck_GetMeleeHitboxParticles(Item sItem, Rectangle heldItemFrame)
44480:	private void ItemCheck_GetMeleeHitbox(Item sItem, Rectangle heldItemFrame, out bool dontAttack, out Rectangle itemRectangle)
44573:	private void ItemCheck_UseDemonHeart(Item sItem)
44583:	private void ItemCheck_UseMinecartPowerUp(Item sItem)

```


---

## 🤖 Assistant · 2026-08-13T01:27:00.273Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terrarria 2>/dev/null\"; cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"TryUsingItem\\|ItemCheck_ApplyUseStyle\\|void ItemCheck(\" Player.cs | head -8; echo \"===TryUsingItem range===\"; awk '/private.*TryUsingItem|public.*TryUsingItem/{print NR\": \"$0}' Player.cs | head -5",
 "description": "Locate TryUsingItem mining entry"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:07.071Z

**📎 ToolResult**

```
(eval):cd:1: no such file or directory: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria 2>/dev/null
41949:	public void ItemCheck()
42702:			ItemCheck_ApplyUseStyle(mountOffset, item, drawHitbox);
49921:	public void ItemCheck_ApplyUseStyle(float mountOffset, Item sItem, Rectangle heldItemFrame)
===TryUsingItem range===

```


---

## 🤖 Assistant · 2026-08-13T01:27:13.145Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Let me find where mining happens — search for "CanPlayerSandfall" no... Search for the pickaxe mining range check. In Player.cs there is `ItemCheck` → `ItemCheck_OwnerOnlyCode` → ... Let me grep for "MiningTools" or "pick > 0" mining check. Actually in 1.4.4 Player.ItemCheck has:

```csharp
if (sItem.pick > 0 || sItem.axe > 0 || sItem.hammer > 0) { ... ItemCheck_GetTileRangeCheckSettings? }
```

Let me grep "GetTileRangeCheckSettings" or "TileReachCheckSettings" usages in Player.cs to enumerate all range checks and which use blockRange vs not.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:27:13.545Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"TileReachCheckSettings\" Player.cs | grep -v \"tileBoost + blockRange\" | head -30",
 "description": "List all range-check sites without blockRange"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:13.598Z

**📎 ToolResult**

```
5798:		TileReachCheckSettings.Simple.GetTileRegion(this, out var LX, out var LY, out var HX, out var HY);
17252:		TileReachCheckSettings.Simple.GetTileRegion(this, out LX, out LY, out HX, out HY);
17484:				if ((type == 219 || type == 642) && IsInTileInteractionRange(tX, tY, TileReachCheckSettings.Simple, extractItemRange))
17489:				else if (type == 209 && Main.tile[tX, tY].frameX / 72 < 3 && IsInTileInteractionRange(tX, tY, TileReachCheckSettings.Simple, cannonRange))
17494:				else if (Main.tileHammer[type] && IsInTileInteractionRange(tX, tY, TileReachCheckSettings.Simple, hammerRange))
17499:				else if (Main.tileAxe[type] && IsInTileInteractionRange(tX, tY, TileReachCheckSettings.Simple, axeRange))
17504:				else if (type == 184 && IsInTileInteractionRange(tX, tY, TileReachCheckSettings.Simple, paintScraperRange))
17509:				else if (IsInTileInteractionRange(tX, tY, TileReachCheckSettings.Simple, pickRange))
22885:		if (!IsInTileInteractionRange(point.X, point.Y, TileReachCheckSettings.Simple))
27177:				Rectangle worldRegion = TileReachCheckSettings.Simple.GetWorldRegion(this);
27192:				Rectangle worldRegion2 = TileReachCheckSettings.Simple.GetWorldRegion(this);
30576:					if (!IsInTileInteractionRange(chestX, chestY, TileReachCheckSettings.Simple))
30600:					if (!IsInTileInteractionRange(chestX, chestY, TileReachCheckSettings.Simple))
30659:		return IsInTileInteractionRange(chestPointX, chestPointY, TileReachCheckSettings.Simple);
31485:		if (IsInTileInteractionRange(smartInteractX, smartInteractY, TileReachCheckSettings.Simple))
31508:				if (!IsInTileInteractionRange(i, j, TileReachCheckSettings.Simple))
31538:	public bool InTileEntityInteractionRange(int interactX, int interactY, int tileSizeX, int tileSizeY, TileReachCheckSettings settings)
31548:	public bool IsInTileInteractionRange(int targetX, int targetY, TileReachCheckSettings settings, int TB = 0)
35220:		Rectangle tileRegion = TileReachCheckSettings.Simple.GetTileRegion(this, ateArtisanBread ? 4 : 0);
35251:	public bool IsTileTypeInInteractionRange(int targetTileType, TileReachCheckSettings settings)
42929:			if (!Main.GamepadDisableCursorItemIcon && IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
43384:		else if (IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
45701:		return IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost);
45706:		if (((sItem.type < 205 || sItem.type > 207) && sItem.type != 1128 && sItem.type != 3031 && sItem.type != 3032 && sItem.type != 4820 && sItem.type != 4872 && sItem.type != 5302 && sItem.type != 5303 && sItem.type != 5304 && sItem.type != 5364) || noBuilding || !IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))
48859:		TileReachCheckSettings.Simple.GetTileRegion(this, out var LX, out var LY, out var HX, out var HY);
51852:		if (!IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost))

```


---

## 🤖 Assistant · 2026-08-13T01:27:20.482Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: line 35220 `TileReachCheckSettings.Simple.GetTileRegion(this, ateArtisanBread ? 4 : 0)` — that's mining (Artisan Bread 面包工匠 gives +4 mining range!). Let me read around 35220.

Also line 48859 — probably mining tools check. Let me read both.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:27:20.484Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && echo \"===35205-35260===\"; sed -n '35205,35260p' Player.cs; echo \"===48850-48880===\"; sed -n '48850,48880p' Player.cs",
 "description": "Read mining range contexts in vanilla"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:20.619Z

**📎 ToolResult**

```
===35205-35260===
		{
			SetAdjTile(item);
		}
	}

	public void AdjTiles()
	{
		Array.Clear(adjTile, 0, adjTile.Length);
		oldAdjWaterSource = adjWaterSource;
		adjWaterSource = false;
		oldAdjHoney = adjHoney;
		adjHoney = false;
		oldAdjLava = adjLava;
		adjLava = false;
		alchemyTable = false;
		Rectangle tileRegion = TileReachCheckSettings.Simple.GetTileRegion(this, ateArtisanBread ? 4 : 0);
		tileRegion = WorldUtils.ClampToWorld(tileRegion);
		for (int i = tileRegion.Left; i <= tileRegion.Right; i++)
		{
			for (int j = tileRegion.Top; j <= tileRegion.Bottom; j++)
			{
				Tile tile = Main.tile[i, j];
				if (tile.active())
				{
					SetAdjTile(tile.type);
					if (TileID.Sets.CountsAsWaterForCrafting[tile.type])
					{
						adjWaterSource = true;
					}
				}
				if (tile.liquid > 200 && tile.liquidType() == 0)
				{
					adjWaterSource = true;
				}
				if (tile.liquid > 200 && tile.liquidType() == 2)
				{
					adjHoney = true;
				}
				if (tile.liquid > 200 && tile.liquidType() == 1)
				{
					adjLava = true;
				}
			}
		}
	}

	public bool IsTileTypeInInteractionRange(int targetTileType, TileReachCheckSettings settings)
	{
		settings.GetRanges(out var _, out var _);
		settings.GetTileRegion(this, out var LX, out var LY, out var HX, out var HY);
		LX = Utils.Clamp(LX, 0, Main.maxTilesX - 1);
		HX = Utils.Clamp(HX, 0, Main.maxTilesX - 1);
		LY = Utils.Clamp(LY, 0, Main.maxTilesY - 1);
		HY = Utils.Clamp(HY, 0, Main.maxTilesY - 1);
		for (int i = LX; i <= HX; i++)
		{
===48850-48880===
		if (acceptDown && !WorldGen.SolidTile(x, y + 1))
		{
			return true;
		}
		return false;
	}

	public bool TryPlacingAGolfBallNearANearbyTee(Vector2 placePosition)
	{
		TileReachCheckSettings.Simple.GetTileRegion(this, out var LX, out var LY, out var HX, out var HY);
		LX = Utils.Clamp(LX, 10, Main.maxTilesX - 10);
		HX = Utils.Clamp(HX, 10, Main.maxTilesX - 10);
		LY = Utils.Clamp(LY, 10, Main.maxTilesY - 10);
		HY = Utils.Clamp(HY, 10, Main.maxTilesY - 10);
		Vector2 value = Main.screenPosition + new Vector2(Main.mouseX, Main.mouseY);
		if (gravDir == -1f)
		{
			value.Y = Main.screenPosition.Y + (float)Main.screenHeight - (float)Main.mouseY;
		}
		Point point = placePosition.ToTileCoordinates();
		List<Tuple<int, int>> list = new List<Tuple<int, int>>();
		for (int i = -2; i <= 2; i++)
		{
			for (int j = -2; j <= 2; j++)
			{
				int num = point.X + i;
				int num2 = point.Y + j;
				if (WorldGen.InWorld(num, num2, 1))
				{
					Tile tileSafely = Framing.GetTileSafely(num, num2);
					if (tileSafely.active() && tileSafely.type == 494)

```


---

## 🤖 Assistant · 2026-08-13T01:27:30.171Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now, where does mining itself check range? In Player.cs the mining happens in ItemCheck → which calls... Actually, in 1.4.4+, mining is handled by `Player.ItemCheck` → `ItemCheck_OwnerOnlyCode` → `TryUsingItem`? Hmm, no. Actually the tile mining is in `Main` via `Player.PickTile`? No. It's `Player.ItemCheck` calls `ItemCheck_ApplyUseStyle` then...

Actually I recall mining is in `Player.cs` `ItemCheck` → for pick/axe/hammer items it calls `ItemCheck_TryUsingTool`? Let me grep for "ItemCheck_TryUsingTool" or "MineHittingAWall"... Actually, the mining entry is `Player.ItemCheck` line 41949 with code:

```csharp
if (item.type == 0 || ... ) 
...
if (sItem.pick > 0) { ... }
```

Let me grep for "TryHittingWall" or "PoundTile" and "MineEverything"...

Actually simpler: search for "ItemCheck_GetTileRangeCheckSettings"? Or search for "IsInTileInteractionRange(tileTargetX" done above — I saw all of them. Mining might not have an explicit range check in Player.cs! In vanilla, mining is done in `Player.ItemCheck_UseMiningTools`? Let me grep "UseMiningTools".
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:27:30.893Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"MiningTools\\|Mining_Check\\|ItemCheck_TryUsing\" Player.cs | head -10; echo \"===tileTarget assign===\"; grep -n \"tileTargetX = \\|tileTargetX=\" Player.cs | head -10",
 "description": "Find mining tool entry and tileTarget assignment"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:30.959Z

**📎 ToolResult**

```
42905:		ItemCheck_UseMiningTools(sItem);
44967:	private void ItemCheck_UseMiningTools(Item sItem)
45016:			ItemCheck_UseMiningTools_ActuallyUseMiningTool(sItem, out canHitWalls, tileTargetX, tileTargetY);
45024:			ItemCheck_UseMiningTools_TryFindingWallToHammer(out var wX, out var wY);
45025:			ItemCheck_UseMiningTools_TryHittingWall(sItem, wX, wY);
45029:	private void ItemCheck_UseMiningTools_ActuallyUseMiningTool(Item sItem, out bool canHitWalls, int x, int y)
45165:		ItemCheck_UseMiningTools_TryPoundingTile(sItem, num, ref canHitWalls, x, y);
45217:	private static void ItemCheck_UseMiningTools_TryFindingWallToHammer(out int wX, out int wY)
45293:	private void ItemCheck_UseMiningTools_TryHittingWall(Item sItem, int wX, int wY)
45355:	private void ItemCheck_UseMiningTools_TryPoundingTile(Item sItem, int tileHitId, ref bool hitWall, int x, int y)
===tileTarget assign===
4923:			tileTargetX = (int)(((float)Main.mouseX + Main.screenPosition.X) / 16f);
25104:		tileTargetX = (int)(((float)Main.mouseX + Main.screenPosition.X) / 16f);
25112:			tileTargetX = Main.maxTilesX - 5;
25120:			tileTargetX = 5;
28021:					tileTargetX = num2;
31403:				tileTargetX = point.X;
31412:				tileTargetX = _tileTargetSmartSelect.X;

```


---

## 🤖 Assistant · 2026-08-13T01:27:32.723Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '44967,45030p' Player.cs",
 "description": "Read ItemCheck_UseMiningTools range gate"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:32.850Z

**📎 ToolResult**

```
	private void ItemCheck_UseMiningTools(Item sItem)
	{
		SpecialToolUsageSettings specialToolUsageSettings = default(SpecialToolUsageSettings);
		if (sItem.type == 4711)
		{
			specialToolUsageSettings = new SpecialToolUsageSettings
			{
				IsAValidTool = true,
				UsageAction = UseShovel
			};
		}
		if (sItem.pick <= 0 && sItem.axe <= 0 && sItem.hammer <= 0 && !specialToolUsageSettings.IsAValidTool)
		{
			return;
		}
		bool flag = IsTargetTileInItemRange(sItem);
		if (noBuilding)
		{
			flag = false;
		}
		if (flag && specialToolUsageSettings.UsageCondition != null)
		{
			flag = specialToolUsageSettings.UsageCondition(this, sItem, tileTargetX, tileTargetY);
		}
		if (toolTime == 0 && itemAnimation > 0 && controlUseItem)
		{
			Tile tile = Main.tile[tileTargetX, tileTargetY];
			if (!tile.active() || !IsAHammerTarget(tile))
			{
				poundRelease = false;
			}
		}
		if (!flag)
		{
			return;
		}
		if (!Main.GamepadDisableCursorItemIcon)
		{
			cursorItemIconEnabled = true;
			Main.ItemIconCacheUpdate(sItem.type);
		}
		bool canHitWalls = false;
		if (toolTime == 0 && itemAnimation > 0 && controlUseItem)
		{
			if (specialToolUsageSettings.UsageAction != null)
			{
				specialToolUsageSettings.UsageAction(this, sItem, tileTargetX, tileTargetY);
				return;
			}
			ItemCheck_UseMiningTools_ActuallyUseMiningTool(sItem, out canHitWalls, tileTargetX, tileTargetY);
		}
		if (releaseUseItem)
		{
			poundRelease = true;
		}
		if (toolTime == 0 && itemAnimation > 0 && controlUseItem && canHitWalls)
		{
			ItemCheck_UseMiningTools_TryFindingWallToHammer(out var wX, out var wY);
			ItemCheck_UseMiningTools_TryHittingWall(sItem, wX, wY);
		}
	}

	private void ItemCheck_UseMiningTools_ActuallyUseMiningTool(Item sItem, out bool canHitWalls, int x, int y)
	{

```


---

## 🤖 Assistant · 2026-08-13T01:27:42.368Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key confirmation:

**Mining** (`ItemCheck_UseMiningTools`) uses `IsTargetTileInItemRange(sItem)` = `IsInTileInteractionRange(tileTargetX, tileTargetY, TileReachCheckSettings.Simple, sItem.tileBoost)` — i.e. **mining does NOT include blockRange** (no Toolbelt bonus for mining; but the Toolbox-type accessories add to tileRangeX/tileRangeY directly via equippedAnyTileRangeAcc so they DO affect mining).

**Placement** (`PlaceThing` contexts: place tile/wall/torch/paint/wrench/lawnmower) uses `item.tileBoost + blockRange` — so Builder potion + Toolbelt extend placement range.

So the vanilla model:
1. tileRangeX/tileRangeY base 5/3 — used by Simple settings for ALL interactions.
2. equippedAnyTileRangeAcc (items 2215 Presserator? wait 2215... let me confirm item names):
   - 2214 = Toolbox (工具箱) → equippedAnyTileSpeedAcc (mining speed)
   - 2215 = Toolbelt? Hmm. Actually 2214 = Toolbox (tile speed +25%), 2215 = Toolbelt? Let me check. In 1.4:
     - 2214 Toolbox: +25% mining speed
     - 2215 Toolbelt: +1 block range? NO wait — the code says 2215 → equippedAnyTileRangeAcc → tileRangeX += 3, tileRangeY += 2. Hmm, that's the "Tool Belt" accessory which gives "+3 tiles horizontal, +2 tiles vertical" range? Hmm, the Tool Belt in Terraria says "Increases block placement range". Actually I recall Toolbelt = +1 block range. But code says tileRangeX += 3 / tileRangeY += 2.
     
     Wait — 407 is Toolbelt! Let me check. Item 407 = "Toolbelt". Item 2215 = "Presserator"? No, Presserator is 2215? Hmm.
     
     Let me check the wiki. Actually in Terraria 1.4:
     - 407 = Toolbelt — "Increases block placement range" (+1 block range, blockRange++)
     - 2214 = Toolbox — "25% increased mining speed"
     - 2215 = Presserator — "Enables auto-placement of actuators"... Hmm, but the code says 2215 → equippedAnyTileRangeAcc.
     
     Hmm, actually 2216 = Paint Sprayer (autoPaint), 2217 = Brick Layer? Let me be careful:
     - 2214 = Toolbox (mining speed)
     - 2215 = Toolbelt?? 
     - 2216 = Paint Sprayer (auto paint)
     - 2217 = Brick Layer (wall speed)
     
     Hmm, that doesn't sound right either. Let me check the actual item names from the wiki mirror or the game data. Actually from 1.4.4:
     - 2214 Toolbox: "Increases block placement & tool range" — wait!
     
     Let me just check the game's own data. The repo has item name data. Let me grep for item names with vid 2214/2215/407/3061/5126.

Let me use the game's l10n data or the items data.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:27:43.054Z · glm-x-preview-260804

```
原版确认:挖掘用 `sItem.tileBoost`(不含 blockRange),放置用 `item.tileBoost + blockRange`。再确认 407/2214/2215/3061/5126 的物品名。
```


---

## 🤖 Assistant · 2026-08-13T01:27:44.971Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"vi_2214_\\|vi_2215_\\|vi_407_\\|vi_3061_\\|vi_5126_\" ~/Project/GLM/SandboxWorld/game/src/data/ 2>/dev/null | head -5; echo \"---l10n---\"; python3 -c \"\nimport json\nfor loc in ['zh-Hans','en-US']:\n    d=json.load(open(f'~/Project/GLM/SandboxWorld/game/src/public/l10n/{loc}.json'))\n    for k in ['2214','2215','407','3061','5126']:\n        # find keys containing the number pattern\n        pass\n    print(loc,'loaded',len(d))\n\" 2>/dev/null || ls ~/Project/GLM/SandboxWorld/game/src/public/l10n/ 2>/dev/null || ls ~/Project/GLM/SandboxWorld/game/public/l10n/ 2>/dev/null | head",
 "description": "Find item names for range accessories"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:27:55.993Z

**📎 ToolResult**

```
<persisted-output>
Output too large (179.1KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/9adce254-f6c0-44ed-947b-3a226dd16828/tool-results/bsxjo54iq.txt

Preview (first 2KB):
~/Project/GLM/SandboxWorld/game/src/data/legacyItemIndex.generated.json:1:["dirt_block","stone_block","wood","sand_block","snow_block","platform","torch","door","workbench","furnace","anvil","chest","gel","acorn","mushroom_item","copper_ore","iron_ore","silver_ore","gold_ore","copper_bar","iron_bar","silver_bar","gold_bar","lens","suspicious_eye","lesser_healing_potion","coin_copper","coin_silver","coin_gold","coin_platinum","heal_potion","agility_potion","ironskin_potion","thorns_potion","regen_potion","obsidian_skin_potion","gills_potion","mana_regen_potion","magic_power_potion","featherfall_potion","water_walking_potion","archery_potion","night_owl_potion","lucky_horseshoe","feral_claws","copper_helmet","copper_chainmail","copper_greaves","iron_helmet","iron_chainmail","iron_greaves","silver_helmet","silver_chainmail","silver_greaves","gold_helmet","gold_chainmail","gold_greaves","wood_pickaxe","wood_axe","wood_sword","wood_hammer","copper_pickaxe","copper_axe","copper_sword","copper_hammer","iron_pickaxe","iron_axe","iron_sword","iron_hammer","silver_pickaxe","silver_axe","silver_sword","silver_hammer","gold_pickaxe","gold_axe","gold_sword","gold_hammer","tin_ore","lead_ore","tungsten_ore","platinum_ore","tin_bar","lead_bar","tungsten_bar","platinum_bar","demonite_ore","meteorite","hellstone","crimtane_ore","cobalt_ore","mythril_ore","adamantite_ore","palladium_ore","orichalcum_ore","titanium_ore","chlorophyte_ore","sapphire","ruby","emerald","topaz","amethyst","diamond","ice_block","ice_brick","snow_brick","sandstone_block","hardened_sand_block","desert_fossil","clay_block","glass","obsidian","gray_brick","red_brick","mud_block","silt_block","table","chair","bed","bookcase","grandfather_clock","piano","dresser","bench","bathtub","keg","cooking_pot","clay_pot","tombstone","life_crystal","vi_109_mana_crystal","vi_1291_life_fruit","candle","chandelier","lantern","candelabra","chinese_lantern","skull_lantern","water_candle","bomb","rope","vi_2350_recall
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-13T01:27:57.858Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld\" && for n in 407 2214 2215 3061 5126; do echo -n \"$n: \"; grep -o \"\\\"vi_${n}_[a-z_]*\\\"\" game/src/data/legacyItemIndex.generated.json | head -1; done",
 "description": "Get item names by vanilla id"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:01.810Z

**📎 ToolResult**

```
407: 2214: 2215: 3061: 5126:

```


---

## 🤖 Assistant · 2026-08-13T01:28:06.471Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Not in legacy index. Let me check the wiki mirror for Toolbelt / Toolbox names. Or check the Terraria wiki Controls/Smart cursor. Actually, easier: check the Terraria wiki item ids. From memory (1.4.4):
- 407 = Toolbelt
- 2214 = Toolbox  
- 2215 = Presserator
- 2216 = Paint Sprayer
- 2217 = Brick Layer
- 3061 = Architect Gizmo Pack
- 5126 = Hand of Creation

Hmm wait — that conflicts. 2215 Presserator → equippedAnyTileRangeAcc? No. Presserator is auto-actuator. Hmm.

Actually let me verify: In Terraria, the "Toolbelt" is item 407 and gives "+1 range" via blockRange++. And "Toolbox" (2214) is "Increases mining speed by 25%". And 2215 is... let me check the wiki. Actually maybe:
- 2214 = Toolbox (mining speed)
- 2215 = Toolbelt?? No, toolbelt is 407.

Hmm, actually I recall in 1.4 the "Toolbelt" was added in 1.4.0.5 along with Presserator etc. Wait no. Let me check the wiki mirror.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:28:07.266Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/ | head -20; echo \"---\"; ls ~/Project/GLM/SandboxWorld/terraria-wiki-md/ | grep -i \"tool\\|toolbox\\|gizmo\\|creation\" | head -10",
 "description": "List wiki mirror files"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:07.424Z

**📎 ToolResult**

```
_categories_partials_Category_3DS_content_pages_1.md
_categories_partials_Category_3DS_content_pages_2.md
_categories_partials_Category_3DS_content_pages_3.md
_categories_partials_Category_3DS_content_pages_4.md
_categories_partials_Category_3DS_content_pages_5.md
_categories_partials_Category_3DS_content_pages_6.md
_categories_partials_Category_3DS_content_pages_7.md
_categories_partials_Category_3DS_content_pages_8.md
_categories_partials_Category_Accessory_items_pages_1.md
_categories_partials_Category_Accessory_items_pages_2.md
_categories_partials_Category_Achievement-related_elements_pages_1.md
_categories_partials_Category_Achievement-related_elements_pages_2.md
_categories_partials_Category_Autoswing_items_pages_1.md
_categories_partials_Category_Autoswing_items_pages_2.md
_categories_partials_Category_Bag_loot_items_pages_1.md
_categories_partials_Category_Bag_loot_items_pages_2.md
_categories_partials_Category_Buffs_pages_1.md
_categories_partials_Category_Buffs_pages_2.md
_categories_partials_Category_By_Hand_pages_1.md
_categories_partials_Category_By_Hand_pages_2.md
---
Architect_Gizmo_Pack.md
Category_Tool_items
Category_Tool_items.md
Hand_Of_Creation
Hand_Of_Creation.md
Legacy_List_of_tooltips.md
Legacy_Spectre_tools.md
Legacy_Tool_speed.md
List_of_tooltips
List_of_tooltips.md

```


---

## 🤖 Assistant · 2026-08-13T01:28:09.932Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && grep -l \"internal item ID\" Toolbox*.md Toolbelt*.md 2>/dev/null; for f in Toolbox.md Toolbelt.md Presserator.md; do echo \"=== $f ===\"; grep -A3 \"internal item ID\" \"$f\" 2>/dev/null | head -6; done",
 "description": "Get item IDs from wiki pages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:21.357Z

**📎 ToolResult**

```
=== Toolbox.md ===
=== Toolbelt.md ===
=== Presserator.md ===

```


---

## 🤖 Assistant · 2026-08-13T01:28:23.474Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && ls | grep -i \"^Toolbox\\|^Toolbelt\\|^Presserator\\|^Brick_Layer\\|^Paint_Sprayer\" ; echo \"===\"; grep -rn \"2214\\|2215\" Architect_Gizmo_Pack.md | head -5",
 "description": "Locate accessory wiki pages and IDs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:23.533Z

**📎 ToolResult**

```
Brick_Layer.md
Paint_Sprayer.md
Presserator.md
Toolbelt.md
Toolbox.md
===

```


---

## 🤖 Assistant · 2026-08-13T01:28:26.760Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && for f in Toolbelt Toolbox Presserator Brick_Layer Paint_Sprayer Architect_Gizmo_Pack Hand_Of_Creation; do echo \"=== $f ===\"; grep -oiE \"Internal (Tile|Item) ID[^0-9]*[0-9]+\" $f.md | head -3; grep -E \"range|speed|placement\" $f.md | head -4; done",
 "description": "Extract effects and IDs from wiki accessory pages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:37.871Z

**📎 ToolResult**

```
=== Toolbelt ===
[Tooltip](Tooltips.md "Tooltips")|  _Increases block placement range by 1_  
[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_3 "Orange \(Rarity level: 3\)")  
The **Toolbelt** is a [construction accessory](Construction_accessory "Construction accessory") that can be purchased from the [Goblin Tinkerer](Goblin_Tinkerer.md "Goblin Tinkerer") for 10 _GC_. While equipped, it grants +1 [placement range](Placement_range.md "Placement range"), but not tool range. 
  * It stacks with all other placement range bonuses.
=== Toolbox ===
[Tooltip](Tooltips.md "Tooltips")|  _Increases block placement & tool range by 1_  
The **Toolbox** is a [construction accessory](Construction_accessory "Construction accessory") that is obtained when opening [Presents](Present.md "Present") dropped during the [Christmas](Christmas.md "Christmas") [seasonal event](Seasonal_event "Seasonal event"), with a chance of 0.309% in [pre-Hardmode](Pre-Hardmode.md "Pre-Hardmode") and 0.288% in [Hardmode](Hardmode.md "Hardmode"). While equipped, it grants +1 [placement range](Placement_range.md "Placement range") and tool range. 
  * It stacks with all other placement and tool range bonuses.
  * [](Orange_Dye.md "Orange Dye")[Orange](Orange_Dye.md "Orange Dye")**** __(Desktop, Console, Old-gen console and Mobile versions)
=== Presserator ===
[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_3 "Orange \(Rarity level: 3\)")  
  * [](Orange_Dye.md "Orange Dye")[Orange](Orange_Dye.md "Orange Dye")
  * [](Bright_Orange_Dye.md "Bright Orange Dye")[Orange](Bright_Orange_Dye.md "Bright Orange Dye")
  * [](Orange_and_Silver_Dye.md "Orange and Silver Dye")[Orange](Orange_and_Silver_Dye.md "Orange and Silver Dye")
=== Brick_Layer ===
[Tooltip](Tooltips.md "Tooltips")|  _Increases tile placement speed_  
[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_3 "Orange \(Rarity level: 3\)")  
The **Brick Layer** is a [construction accessory](Construction_accessory "Construction accessory") that is purchased from the [Traveling Merchant](Traveling_Merchant.md "Traveling Merchant") for 10 _GC_. While equipped, it grants +50% [placement speed](Placement_speed.md "Placement speed") when placing [blocks](Blocks.md "Blocks"). 
  * The tile placement speed from the Brick Layer will only apply while holding a non-[Torch](Torches.md "Torches") block.[1] This behavior also means that there is no bonus without holding a block, which is of little consequence save for [Roller Skates](Roller_Skates.md "Roller Skates"). These traits also apply to its upgrades.[2]
=== Paint_Sprayer ===
[Rarity](Rarity.md "Rarity")| [](Category%3AItems_of_rarity_3 "Orange \(Rarity level: 3\)")  
  * [Desktop 1.2.4.1](Desktop_1.2.4.1 "Desktop 1.2.4.1"): Using Paint Sprayer with [Brick Layer](Brick_Layer.md "Brick Layer") or [Cement Mixer](Cement_Mixer "Cement Mixer") now places at the proper speed.
  * [](Orange_Dye.md "Orange Dye")[Orange](Orange_Dye.md "Orange Dye")**** __(Desktop, Console, Old-gen console and Mobile versions)
  * [](Bright_Orange_Dye.md "Bright Orange Dye")[Orange](Bright_Orange_Dye.md "Bright Orange Dye")**** __(Desktop, Console, Old-gen console and Mobile versions)
=== Architect_Gizmo_Pack ===
[Tooltip](Tooltips.md "Tooltips")|  _Increases block & wall placement speed  
Increases block placement & tool range by 3  
  * +50% [placement speed](Placement_speed.md "Placement speed") when placing [blocks](Blocks.md "Blocks") and [walls](Walls "Walls")
  * Increased [placement range](Placement_range.md "Placement range") and tool range by 2 tiles vertically and 3 tiles horizontally
=== Hand_Of_Creation ===
[Tooltip](Tooltips.md "Tooltips")|  _Increases mining speed by 25%  
Increases block & wall placement speed  
Increases block placement & tool range by 3  
Increases pickup range for items

```


---

## 🤖 Assistant · 2026-08-13T01:28:46.170Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have the wiki facts:
- **Toolbelt** (407): +1 placement range, NOT tool range → blockRange++ (only placement)
- **Toolbox** (2214): +1 placement AND tool range — wait but code says 2214 → equippedAnyTileSpeedAcc?? Hmm. Let me recheck. Actually code: 2214 → equippedAnyTileSpeedAcc (mining speed). 2215 → equippedAnyTileRangeAcc. Hmm, that contradicts wiki naming: Toolbox tooltip "Increases block placement & tool range by 1". Hmm.

Wait, let me re-read vanilla code:
- 2214 → equippedAnyTileSpeedAcc
- 2215 → equippedAnyTileRangeAcc

Hmm so 2214 = Toolbox?? The wiki says Toolbox = "Increases block placement & tool range by 1". But equippedAnyTileSpeedAcc is mining/placement speed (+25%?). Hmm.

Hold on. equippedAnyTileSpeedAcc consumer: line ~12605 area:
```
if (equippedAnyTileSpeedAcc) { tileSpeed += ...; }
```
Let me check. And Hand of Creation tooltip says "Increases mining speed by 25%" first line — so in vanilla, Hand of Creation (5126) sets equippedAnyTileSpeedAcc (mining speed), equippedAnyTileRangeAcc (range), autoPaint, wallSpeed.

So equippedAnyTileSpeedAcc = mining speed +25%? The wiki says Toolbox "Increases block placement & tool range by 1"?? That doesn't match. Hmm — wait, actually I think I mixed up: **Toolbox** (2214) is "Increases block placement & tool range by 1" per wiki... but vanilla code gives 2214 equippedAnyTileSpeedAcc. Let me actually verify item IDs. Maybe 2214 = Toolbox... hmm.

Let me check what equippedAnyTileSpeedAcc does:
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:28:46.911Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n -A5 \"if (equippedAnyTileSpeedAcc)\" Player.cs | head -8; echo \"===2214/2215 in ItemSet=== \"; grep -n \"2214\\|2215\" ItemID.cs 2>/dev/null | head",
 "description": "Check equippedAnyTileSpeedAcc consumer"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:28:46.974Z

**📎 ToolResult**

```
12602:		if (equippedAnyTileSpeedAcc)
12603-		{
12604-			int createTile = inventory[selectedItem].createTile;
12605-			if (createTile >= 0 && !TileID.Sets.Torches[createTile])
12606-			{
12607-				tileSpeed += 0.5f;
===2214/2215 in ItemSet===

```


---

## 🤖 Assistant · 2026-08-13T01:29:00.481Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So equippedAnyTileSpeedAcc → tileSpeed += 0.5f (placement speed +50%, only when holding a placeable non-torch block) — that's **Brick Layer** behavior per wiki ("+50% placement speed"). So 2214 = Brick Layer! And 2215 = ... equippedAnyTileRangeAcc → tileRangeX+=3/tileRangeY+=2. Hmm, but wiki says Toolbelt gives +1.

Wait — I misread. Let me recheck which item is which. The Architect Gizmo Pack tooltip per wiki: "Increases block placement & tool range by 3 ... by 2 tiles vertically and 3 tiles horizontally" — that matches `tileRangeX += 3; tileRangeY += 2`.

So equippedAnyTileRangeAcc gives +3 horizontal/+2 vertical — matches Architect Gizmo Pack and Hand of Creation. And 2215 is one of the ingredients. Given 2214 = tileSpeed (Brick Layer), 2215 = tileRange... the four ingredients of Architect Gizmo Pack are: Toolbelt(407)? No wait — Architect Gizmo Pack = Brick Layer + Extendo Grip + Paint Sprayer + Presserator.

**Extendo Grip!** That's it. 2215 = Extendo Grip ("Increases block placement and tool range by 2 tiles vertically and 3 horizontally"). Hmm, actually Extendo Grip tooltip: "Increases block placement & tool range by 3". Yes! Extendo Grip is the item giving +3 horizontal/+2 vertical range.

So:
- 2214 = Brick Layer (tileSpeed +50%)
- 2215 = Extendo Grip (tileRangeX+3, tileRangeY+2)
- 2216 = Paint Sprayer (autoPaint)
- 2217 = Cement Mixer? (wallSpeed +50%)
- 3061 = Architect Gizmo Pack (all four)
- 5126 = Hand of Creation (all four + treasureMagnet + chiselSpeed)

And:
- 407 = Toolbelt → blockRange++ (placement range +1, NOT tool range)
- Builder potion (buff 107) → tileSpeed+0.25/wallSpeed+0.25/blockRange++

Now implementation side:
- `equipStats.tileRange` is set from fx.tileRange in vanillaAccFx for items vid 2215, 3061, 5126 — that matches Extendo Grip/Architect Gizmo Pack/Hand of Creation! Good, the data table is right (3 items).
- But Game.ts uses `p.equipStats.tileRange ? 3 : 0` for the X axis and... let me check: in `inTileRange` it's `const x = Math.min(20, 5) + tb, y = Math.min(20, 3) + tb;` — the same tb for both X and Y! Vanilla gives tileRangeX += 3 but tileRangeY += 2. So implementation gives Y +3 instead of +2 — a 1-tile vertical deviation.

Wait, but let me check how vanilla TileReachCheckSettings.GetTileRegion computes ranges. Let me read TileReachCheckSettings.cs:53.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:29:00.854Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && cat TileReachCheckSettings.cs",
 "description": "Read TileReachCheckSettings.cs fully"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:00.894Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
cat: TileReachCheckSettings.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-13T01:29:02.325Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find \"~/Project/GLM/SandboxWorld/Terarria1456\" -name \"TileReachCheckSettings.cs\" 2>/dev/null",
 "description": "Locate TileReachCheckSettings.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:02.407Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/TileReachCheckSettings.cs

```


---

## 🤖 Assistant · 2026-08-13T01:29:08.308Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.DataStructures/TileReachCheckSettings.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:08.336Z

**📎 ToolResult**

```
1	using System;
2	using Microsoft.Xna.Framework;
3	
4	namespace Terraria.DataStructures;
5	
6	public struct TileReachCheckSettings
7	{
8		public int TileRangeMultiplier;
9	
10		public int? TileReachLimit;
11	
12		public int? OverrideXReach;
13	
14		public int? OverrideYReach;
15	
16		public static readonly TileReachCheckSettings Simple = new TileReachCheckSettings
17		{
18			TileRangeMultiplier = 1,
19			TileReachLimit = 20
20		};
21	
22		public static readonly TileReachCheckSettings Pylons = new TileReachCheckSettings
23		{
24			OverrideXReach = 60,
25			OverrideYReach = 60
26		};
27	
28		public void GetRanges(out int x, out int y)
29		{
30			x = Player.tileRangeX * TileRangeMultiplier;
31			y = Player.tileRangeY * TileRangeMultiplier;
32			if (TileReachLimit.HasValue)
33			{
34				if (x > TileReachLimit.Value)
35				{
36					x = TileReachLimit.Value;
37				}
38				if (y > TileReachLimit.Value)
39				{
40					y = TileReachLimit.Value;
41				}
42			}
43			if (OverrideXReach.HasValue)
44			{
45				x = OverrideXReach.Value;
46			}
47			if (OverrideYReach.HasValue)
48			{
49				y = OverrideYReach.Value;
50			}
51		}
52	
53		public void GetTileRegion(Player player, out int LX, out int LY, out int HX, out int HY, int TB = 0)
54		{
55			GetRanges(out var x, out var y);
56			x += TB;
57			y += TB;
58			LX = (int)(player.position.X / 16f) - x;
59			HX = (int)Math.Ceiling((player.position.X + (float)player.width) / 16f) - 1 + x;
60			LY = (int)(player.position.Y / 16f) - y;
61			HY = (int)Math.Ceiling((player.position.Y + (float)player.height) / 16f) - 1 + y;
62		}
63	
64		public Rectangle GetTileRegion(Player player, int TB = 0)
65		{
66			GetTileRegion(player, out var LX, out var LY, out var HX, out var HY, TB);
67			return new Rectangle(LX, LY, HX - LX, HY - LY);
68		}
69	
70		public void GetWorldRegion(Player player, out int LX, out int LY, out int HX, out int HY, int TB = 0)
71		{
72			GetTileRegion(player, out LX, out LY, out HX, out HY, TB);
73			LX *= 16;
74			LY *= 16;
75			HX *= 16;
76			HY *= 16;
77			HX += 15;
78			HY += 15;
79		}
80	
81		public Rectangle GetWorldRegion(Player player, int TB = 0)
82		{
83			GetWorldRegion(player, out var LX, out var LY, out var HX, out var HY, TB);
84			return new Rectangle(LX, LY, HX - LX, HY - LY);
85		}
86	}
87	

```


---

## 🤖 Assistant · 2026-08-13T01:29:14.809Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: `GetRanges` uses `Player.tileRangeX * multiplier` and `Player.tileRangeY * multiplier` — so with Extendo Grip, tileRangeX=5+3=8, tileRangeY=3+2=5, then `+ TB`.

The implementation `inTileRange` hardcodes `x = Math.min(20, 5) + tb, y = Math.min(20, 3) + tb` — it bakes in 5/3 as the base and never accounts for `equippedAnyTileRangeAcc` adding 3 to X and 2 to Y separately. Instead the Game.ts caller computes `tb = (tileRange?3:0) + (Builder?1:0)` and applies the SAME tb to both X and Y. So:
- With Extendo Grip only: vanilla X=8, Y=5. Implementation X=8, Y=6 → **Y +1 off**.
- With Extendo Grip + Builder buff: vanilla X=8+1=9, Y=5+1=6. Implementation X=9, Y=9 → **Y +3 off**.

Also — critically — the implementation applies `tb` (including Builder +1) to **mining** too! Vanilla: mining uses `IsTargetTileInItemRange` = `sItem.tileBoost` only — blockRange (Toolbelt/Builder) does NOT extend mining. Implementation `Game.ts:5094`: `if (!this.inTileRange(tx, ty)) { this.mining = null; return; }` — with tb=0. Let me check that call site. Line 5094 uses default tb=0. Good — mining uses tb=0, so no Builder bonus in mining. But line 1203 (tryQuickMinecart) and 4138, 5917, 5982, 6290 include the Builder +1 and tileRange +3.

Let me read Game.ts sections to determine which are placement vs mining:
- 4138: context needed
- 5094: mining (tb=0 default)
- 5818: multicolor wrench tb=20 (vanilla: item.tileBoost=20 for wrenches — matches "inTileRange(tx,ty,20)")
- 5917, 5982, 6290: need context

Let me read these regions.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:29:15.131Z · glm-x-preview-260804

```
公式对齐确认完毕。现在读 Game.ts 各调用点上下文,区分挖掘/放置路径。
```


---

## 🤖 Assistant · 2026-08-13T01:29:15.891Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '4125,4145p;5085,5100p;5810,5822p;5910,5930p;5975,5990p;6285,6295p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read Game.ts range call sites contexts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:15.994Z

**📎 ToolResult**

```
          else if (hovered && /stone|ore|brick|obsidian|ash|gem_|fossil|silt/i.test(hovered.key)) this.sfx.play('tink');
          else this.sfx.play('dig');
        }
      }
      // HitTile 节流窗 = 实际挥击间隔（含攻速配饰加成），保证一挥一击
      this.tryMine(tx, ty, dual.power, dual.type, spd, tool.useTime ?? spd);
      return;
    }

    // 提取机（Player.cs:41008 PlaceThing_ItemInExtractinator——先于 PlaceThing_Tiles）：
    // 手持可提取物（泥沙/雪泥/沙漠化石/垃圾/苔藓/粪块/蜂巢/贝壳堆/黑曜石，ItemID.cs:1104）
    // 对准 219/642 左键使用 → 转化；642 先查矿物兑换表。useTime 冷却 = 10×(642?0.33:1)
    if (inp.mouseDown && !inp.rightDown && this.player.useTime === 0
      && this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) {
      const esh = this.wiring?.sheetOf(tx, ty) ?? -1;
      if (esh === 219 || esh === 642) {
        if (this.useExtractinator(tx, ty, true)) {
          // useAnimation 15（Item.cs:6301 泥沙/MakeUsableWithChlorophyteExtractinator:48120）
          this.swing = { t: 15, dur: 15, item: held!.id };
          this.swingHitSet.clear();
          this.swingTileCutSet.clear();
    this.world.altarCount++;
    // 成就：BEGONE_EVIL（WorldGen.cs:49111 event 6——每次砸祭坛都触发）
    this.achievements.notifyProgressionEvent(6);
  }

  private tryMine(tx: number, ty: number, power: number, toolType: 'pick' | 'axe' | 'hammer', speed: number, useTime?: number) {
    // 联机破坏保护（v3 房间制）：非房主禁挖/禁锤墙
    if (!this.netCanEditTile()) { this.mining = null; this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    // 范围检查
    if (!this.inTileRange(tx, ty)) { this.mining = null; return; }
    const type = this.world.store.get(tx, ty);
    // 恶魔祭坛（tile 26，原版 Player.cs:45058）：镐不可破坏（def pick:-1 拦）；
    // 锤 ≥80 锤力且困难模式 → SmashAltar（砸碎=困难矿三档轮换+幽灵）；
    // 否则进度清零 + 玩家受 statLife/2 电击（ByOther(4)）
    if (type === TILE_BY_KEY['v_26_altars']) {
      this.mining = null;
  /** 电路工具使用(原版 Player.cs:30289-30444 ItemCheck_UseWiringTools) */
  private useWireTool(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    const w = this.wiring;
    if (!w) return;
    const st = this.world.store;
    const dx = tx - Math.floor(this.player.cx / TILE);
    const dy = ty - Math.floor(this.player.cy / TILE);
    if (!this.inTileRange(tx, ty, 20)) return; // 原版多彩扳手/蓝图 tileBoost=20
    if (this.player.useTime > 0) return;
    const wt = itemDef.wireTool!;
    const inv = this.player.inv;

  private tryPlaceWall(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    const st = this.world.store;
    if (!st.inBounds(tx, ty)) return;
    // 射程（ItemReach，与 tryPlace 一致 5.5 格）
    const dx = tx - Math.floor(this.player.cx / TILE);
    const dy = ty - Math.floor(this.player.cy / TILE);
    if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) return;
    if (this.player.useTime > 0) return;
    const wallId = itemDef.wallId!;
    const i0 = st.idx(tx, ty);
    if (st.wall[i0] === wallId) return;  // 已是同墙
    // 邻接门（cs:38943-38952）：四邻至少一格 active 或 wall>0
    const adj = (ax: number, ay: number) =>
      st.inBounds(ax, ay) && ((st.flags[st.idx(ax, ay)] && st.type[st.idx(ax, ay)] !== 0) || st.wall[st.idx(ax, ay)] > 0);
    if (!adj(tx + 1, ty) && !adj(tx - 1, ty) && !adj(tx, ty + 1) && !adj(tx, ty - 1)) return;
    // TileReplacement（Player.TileReplacementEnabled，cs:3225——builderAccStatus[10] 全程
    // 默认 0=恒开）：目标已有墙时先试替换（PlaceThing_TryReplacingWalls → ReplaceWall）。
    // 门 = NearFriendlyWall（WorldGen.cs:52290：自身或四邻墙为空/房墙）+ 墙可破坏
    // （KillWall_CheckFailure :60434：地牢墙需 downedBoss3 / 87 蜥蜴墙需 downedGolemBoss）
    // + 墙 ≠ 350。成功：旧墙尘 + 换墙 + 消耗（KillWall_DropItems 墙掉落表未移植——
  private tryPlace(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    const st = this.world.store;
    if (!st.inBounds(tx, ty)) return;
    // 距离
    const dx = tx - Math.floor(this.player.cx / TILE);
    const dy = ty - Math.floor(this.player.cy / TILE);
    if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) return;
    const tileId = TILE_BY_KEY[itemDef.tile!];
    const def = TILE_DEFS[tileId];
    // 旧日军团竞技场建造封锁（Player.cs:25669-25672：DD2Event.Ongoing &&
    // ShouldBlockBuilding → 禁改方块，DD2Event.cs:794-796 包围盒判定）
    if (this.world.oldOnesArmy.ongoing
      && shouldBlockBuilding(this.world.oldOnesArmy, tx * TILE + 8, ty * TILE + 8)) {
      return;
    }
    // 距离门（原版 Player.IsInTileInteractionRange Simple：约 5 格）——此前整个
    // interactAt 无距离检查，隔全图右键可开储物/设床重生点
    {
      const dx = tx - Math.floor(this.player.cx / TILE);
      const dy = ty - Math.floor(this.player.cy / TILE);
      if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) { this.input.rightDown = false; return; }
    }
    const type = st.get(tx, ty);
    // 原版 tile sheet（八音盒/喷泉/天塔柱/派对柱右键分支用）
    const sh = this.wiring?.sheetOf(tx, ty) ?? -1;
    // 联机保护门禁（v3 房间制）：以下右键操作会改方块/世界状态——非房主在保护房拒绝。

```


---

## 🤖 Assistant · 2026-08-13T01:29:29.188Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I see the picture:

1. **Mining** (`tryMine` Game.ts:5094): `inTileRange(tx, ty)` with tb=0 → base 5/3 only. ✅ matches vanilla (mining = sItem.tileBoost, tools have tileBoost 0). BUT — does it account for equippedAnyTileRangeAcc? Vanilla: tileRangeX becomes 5+3=8 via the *static* tileRangeX which is used in GetRanges → so YES, Extendo Grip DOES extend mining in vanilla (wiki: Toolbox/Extendo Grip/Architect Gizmo Pack "block placement & tool range"). Implementation tryMine ignores tileRange entirely → mining range not extended by Extendo Grip/Toolbox/Architect Gizmo Pack/Hand of Creation. ❌ deviation.

2. **Placement** (`tryPlace` :5977, `tryPlaceWall` :5917): tb = (tileRange?3:0) + (Builder?1:0). Vanilla: `item.tileBoost + blockRange` where blockRange = Toolbelt(407)?1:0 + Builder?1:0. But placement also benefits from tileRangeX/Y += 3/2 (Extendo Grip). Implementation: X = 5+3(+1) ✅; Y = 3+3(+1) but vanilla Y = 3+2(+1) → ⚠️ Y off by +1.
   Also missing: **Toolbelt (407) blockRange+1** — implementation has no blockRange from Toolbelt. Let me check if toolbelt exists in vanillaAccFx... 407 wasn't in the tileRange list (only 2215/3061/5126). Let me grep for 407 in vanillaAccFx.json.

3. **Right-click interact** (interactAt :6290): includes tileRange +3 and Builder +1. Vanilla right-click interactions (chest/door) use `IsInTileInteractionRange(..., TileReachCheckSettings.Simple)` with NO TB → just base 5/3 (lines 30576, 30600, 30659, 22885). So implementation gives extra range (+3/+1) for right-click interactions that vanilla doesn't. ⚠️ deviation (over-range).

Wait — but is that right? Let me double check vanilla right-click on chests: line 30576 `if (!IsInTileInteractionRange(chestX, chestY, TileReachCheckSettings.Simple))` — no TB. And doors: Player.OpenDoor/PushDoor? Let me check. Search for "OpenDoor" range. Actually the chest check is `Player.chest` handling. Let me also check SmartInteract — 31485.

So vanilla right-click interact = base range 5/3 only (affected by tileRangeX/Y static which includes Extendo Grip +3/+2!). Hmm, right — tileRangeX is static and modified by equippedAnyTileRangeAcc, so Simple range checks DO include the +3/+2 for ALL interactions including right-click and mining. Only blockRange (Toolbelt + Builder) is placement-only.

So the vanilla model:
- base X=5, Y=3
- Extendo Grip (2215)/Architect Gizmo Pack (3061)/Hand of Creation (5126) → X+3, Y+2 → applies to EVERYTHING (mining, placement, right-click)
- Toolbelt (407) + Builder buff (107) → blockRange → applies ONLY to placement (place tile/wall/torch/paint/wrench/lawnmower)

Implementation model:
- base X=5, Y=3
- equipStats.tileRange (2215/3061/5126) → tb += 3 applied to BOTH X and Y (vanilla Y+2) → only in placement/wall/extract/right-click/minecart paths, NOT mining
- Builder → tb += 1 applied to X and Y equally → placement, wall, extract, right-click, minecart; NOT mining ✅ (mining correctly excludes Builder)
- Toolbelt 407 → missing entirely (no blockRange)

Deviations:
1. Y-axis: +3 instead of +2 for the tileRange accessory group (over-reach vertically 1 tile)
2. Mining doesn't get tileRange accessory bonus (under-reach horizontally 3 tiles, vertically 2)
3. Right-click interact gets Builder +1 (vanilla: right-click has no TB, base only) — but right-click DOES get tileRangeX/Y in vanilla. So implementation partially over (Builder+1 on right-click) — though honestly this is a small thing.
4. Toolbelt (407) missing entirely from blockRange. Let me verify 407 in vanillaAccFx.json.

Let me check for 407 in vanillaAccFx and in the acc data.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:29:30.164Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src/data && python3 -c \"\nimport json\nd=json.load(open('vanilla-accfx.json'))\nprint('407' in d and d['407'], '| 2214:', d.get('2214'), '| 2215:', d.get('2215'))\nprint('3061:', d.get('3061'), '| 5126:', d.get('5126'))\n\"",
 "description": "Check Toolbelt 407 in accfx data"
}
```


---

## 🤖 Assistant · 2026-08-13T01:29:31.049Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"vi_407_\\|'407'\\|\\\"407\\\"\" ~/Project/GLM/SandboxWorld/game/src/data/*.json 2>/dev/null | head -3; grep -rn \"toolbelt\\|Toolbelt\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" | head -5",
 "description": "Search for Toolbelt anywhere in src"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:46.516Z

**📎 ToolResult**

```
False | 2214: {'tileSpeed': 1} | 2215: {'tileRange': 1}
3061: {'tileSpeed': 1, 'wallSpeed': 1, 'tileRange': 1} | 5126: {'treasureMagnet': 1, 'tileSpeed': 1, 'wallSpeed': 1, 'tileRange': 1}

```


---

## 👤 User(sidechain) · 2026-08-13T01:29:46.579Z

**📎 ToolResult**

```
<persisted-output>
Output too large (227.6KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/9adce254-f6c0-44ed-947b-3a226dd16828/tool-results/bmx8ipfn4.txt

Preview (first 2KB):
~/Project/GLM/SandboxWorld/game/src/data/vanilla-bestiary-spawn.json:1:{"conditions":{"Invasions.Goblins":{"key":"Bestiary_Invasions.Goblins","priority":49},"Invasions.Pirates":{"key":"Bestiary_Invasions.Pirates","priority":50},"Invasions.Martian":{"key":"Bestiary_Invasions.Martian","priority":53},"Invasions.OldOnesArmy":{"key":"Bestiary_Invasions.OldOnesArmy","priority":55},"Invasions.PumpkinMoon":{"key":"Bestiary_Invasions.PumpkinMoon","priority":51},"Invasions.FrostMoon":{"key":"Bestiary_Invasions.FrostMoon","priority":52},"Invasions.FrostLegion":{"key":"Bestiary_Invasions.FrostLegion","priority":54},"Events.SlimeRain":{"key":"Bestiary_Events.SlimeRain","priority":47},"Events.WindyDay":{"key":"Bestiary_Events.WindyDay","priority":41},"Events.BloodMoon":{"key":"Bestiary_Events.BloodMoon","priority":38},"Events.Halloween":{"key":"Bestiary_Events.Halloween","priority":45},"Events.Rain":{"key":"Bestiary_Events.Rain","priority":40},"Events.Christmas":{"key":"Bestiary_Events.Christmas","priority":46},"Events.Eclipse":{"key":"Bestiary_Events.Eclipse","priority":39},"Events.Party":{"key":"Bestiary_Events.Party","priority":48},"Events.Blizzard":{"key":"Bestiary_Events.Blizzard","priority":42},"Events.Sandstorm":{"key":"Bestiary_Events.Sandstorm","priority":43},"Biomes.TheCorruption":{"key":"Bestiary_Biomes.TheCorruption","priority":7},"Biomes.TheCrimson":{"key":"Bestiary_Biomes.Crimson","priority":12},"Biomes.Surface":{"key":"Bestiary_Biomes.Surface","priority":0},"Biomes.Graveyard":{"key":"Bestiary_Biomes.Graveyard","priority":35},"Biomes.UndergroundJungle":{"key":"Bestiary_Biomes.UndergroundJungle","priority":23},"Biomes.TheUnderworld":{"key":"Bestiary_Biomes.TheUnderworld","priority":33},"Biomes.TheDungeon":{"key":"Bestiary_Biomes.TheDungeon","priority":32},"Biomes.Underground":{"key":"Bestiary_Biomes.Underground","priority":1},"Biomes.TheHallow":{"key":"Bestiary_Biomes.TheHallow","priority":17},"Biomes.UndergroundMushroom":{"key":"Bestiary_Biomes.Undergrou
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-13T01:29:49.259Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Toolbelt (407) is NOT in vanillaAccFx — so it exists as an item (probably as vi_407) but has no blockRange effect. Also I should verify whether toolbelt item exists at all in the items data. Let me quickly grep for vi_407 in the items data file.

Actually the earlier grep for `vi_407_` in game/src/data returned nothing before the output got flooded by the second grep. Let me do a precise grep.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:29:49.869Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rln \"vi_407_\" ~/Project/GLM/SandboxWorld/game/src/data/ 2>/dev/null | head -3; echo \"---grep key in items---\"; ls ~/Project/GLM/SandboxWorld/game/src/data/ | head -30",
 "description": "Check if Toolbelt item exists"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:49.966Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/data/legacyItemIndex.generated.json
---grep key in items---
Bestiary.ts
bestiaryStatics.generated.ts
critters.ts
enemies.ts
itemKeys.ts
itemMigration.ts
items.ts
legacyItemIndex.generated.json
Music.ts
npcLavaImmune.ts
npcPortraits.ts
tiles.ts
vanilla-accfx.json
vanilla-bestiary-spawn.json
vanilla-bestiary.json
vanilla-equip.json
vanilla-fishing.json
vanilla-itemcombat.json
vanilla-itemfunc.json
vanilla-itemrare.json
vanilla-itemstats.json
vanilla-itemvalue.json
vanilla-mapcolors.json
vanilla-npcdrops.json
vanilla-npcnetid.json
vanilla-npcvalue.json
vanilla-prefix.json
vanilla-projectiles.json
vanilla-projframes.json
vanilla-projstatus.json

```


---

## 🤖 Assistant · 2026-08-13T01:29:52.170Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/src/data/legacyItemIndex.generated.json'))\nfor i,k in enumerate(d):\n    if isinstance(k,str) and 'vi_407_' in k: print(i,k)\n\"",
 "description": "Find Toolbelt item key"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:29:58.806Z

**📎 ToolResult**

```
1651 vi_407_Toolbelt

```


---

## 🤖 Assistant · 2026-08-13T01:30:01.846Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Toolbelt exists as `vi_407_Toolbelt` (item index 1651) but has NO accFx → no blockRange effect in implementation. Confirmed deviation.

Now let me check the H/J/B quick keys. Grep Input.ts and Game.ts for key handling of healing/mana. Also check Options.ts for smart cursor settings and key bindings.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:02.000Z · glm-x-preview-260804

```
工具腰带存在(vi_407_Toolbelt)但无 blockRange 效果——缺失确认。现查 H/J/B 快捷键与键位绑定。
```


---

## 🤖 Assistant · 2026-08-13T01:30:03.235Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"KeyH\\b\\|'KeyH'\\|KeyJ\\b\\|'KeyJ'\\|KeyB\\b\\|'KeyB'\\|QuickHeal\\|QuickMana\\|QuickBuff\\|quickHeal\\|quickMana\\|quickBuff\\|quickMount\" ~/Project/GLM/SandboxWorld/game/src/core/Input.ts ~/Project/GLM/SandboxWorld/game/src/core/Options.ts ~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts ~/Project/GLM/SandboxWorld/game/src/vui/VUI.ts 2>/dev/null | head -20",
 "description": "Search H/J/B quick keys in input/options"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:03.266Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T01:30:06.885Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"KeyH\\|KeyJ\\|KeyB\\|heal\\|potion\" ~/Project/GLM/SandboxWorld/game/src/core/Input.ts | head -20; echo \"===Input.ts size===\"; wc -l ~/Project/GLM/SandboxWorld/game/src/core/Input.ts",
 "description": "Inspect Input.ts key handling"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:06.916Z

**📎 ToolResult**

```
===Input.ts size===
      85 ~/Project/GLM/SandboxWorld/game/src/core/Input.ts

```


---

## 🤖 Assistant · 2026-08-13T01:30:07.999Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Input.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:08.009Z

**📎 ToolResult**

```
1	// 键盘/鼠标输入。UI 打开时屏蔽游戏输入。
2	export class Input {
3	  keys = new Set<string>();
4	  mouseX = 0; mouseY = 0;
5	  mouseDown = false;
6	  /** 左键物理按住态(mousedown→true/mouseup→false,不随点击消费清零)。
7	   *  mouseDown 是"边沿消费"语义(use 代码用完置 false,等下一次真实点击),
8	   *  悠悠球/连枷 channel 等需要"电平"语义的判定必须用本字段——否则掷出当帧
9	   *  被 use 清掉后无 mousedown 事件回填,链球出生 1 帧即判松手回收(2026-08-13) */
10	  mouseHeld = false;
11	  rightDown = false;
12	  uiBlocking = false;     // 背包/合成等打开时为 true
13	  wheelDelta = 0;
14	  keydownHandlers: Array<(code: string) => void> = [];
15	
16	  private el: HTMLElement;
17	  /** 已注册监听(destroy 时全部移除——window 强引用曾把整个旧 Game 钉死,
18	   *  连续多次读档 GPU 内存累积 → contextlost 风暴卡死,2026-08-10 trace 实证) */
19	  private winListeners: Array<[string, EventListener, AddEventListenerOptions?]> = [];
20	  private elListeners: Array<[string, EventListener, AddEventListenerOptions?]> = [];
21	
22	  constructor(el: HTMLElement) {
23	    this.el = el;
24	    const onWin = (type: string, fn: EventListener, opts?: AddEventListenerOptions) => {
25	      window.addEventListener(type, fn, opts);
26	      this.winListeners.push([type, fn, opts]);
27	    };
28	    const onEl = (type: string, fn: EventListener, opts?: AddEventListenerOptions) => {
29	      el.addEventListener(type, fn, opts);
30	      this.elListeners.push([type, fn, opts]);
31	    };
32	
33	    onWin('keydown', ((e: KeyboardEvent) => {
34	      if (e.repeat) return;
35	      // 输入框内打字不算操作键位（合成搜索框等）：游戏键全不放行、也不吞事件
36	      const tgt = e.target as HTMLElement | null;
37	      if (tgt && (tgt.tagName === 'INPUT' || tgt.tagName === 'TEXTAREA' || tgt.isContentEditable)) return;
38	      this.keys.add(e.code);
39	      this.keydownHandlers.forEach((fn) => fn(e.code));
40	      if (['Space', 'ArrowUp', 'ArrowDown', 'Tab'].includes(e.code)) e.preventDefault();
41	      // F2 无敌+无限魔力(调试,Game) / F1 像素画导入(Game,自 F2 迁入)——防浏览器快捷
42	      if (e.code === 'F2' || e.code === 'F1') e.preventDefault();
43	    }) as EventListener);
44	    onWin('keyup', ((e: KeyboardEvent) => { this.keys.delete(e.code); }) as EventListener);
45	    onWin('blur', (() => { this.keys.clear(); this.mouseHeld = false; }) as EventListener);
46	    onEl('mousemove', ((e: MouseEvent) => {
47	      const r = this.el.getBoundingClientRect();
48	      this.mouseX = e.clientX - r.left;
49	      this.mouseY = e.clientY - r.top;
50	    }) as EventListener);
51	    // mousedown 挂 window：不依赖事件目标是否恰好是 canvas
52	    onWin('mousedown', ((e: MouseEvent) => {
53	      // UI 面板上的点击不穿透为游戏输入
54	      if ((e.target as HTMLElement)?.closest?.('.sw-panel, .sw-slot, .sw-recipe, .sw-btn')) return;
55	      if (e.button === 0) { this.mouseDown = true; this.mouseHeld = true; }
56	      if (e.button === 2) this.rightDown = true;
57	    }) as EventListener);
58	    onWin('mouseup', ((e: MouseEvent) => {
59	      if (e.button === 0) { this.mouseDown = false; this.mouseHeld = false; }
60	      if (e.button === 2) this.rightDown = false;
61	    }) as EventListener);
62	    onEl('contextmenu', (e) => e.preventDefault());
63	    onEl('wheel', ((e: WheelEvent) => {
64	      this.wheelDelta += Math.sign(e.deltaY);
65	      e.preventDefault();
66	    }) as EventListener, { passive: false });
67	  }
68	
69	  /** 移除全部监听(退出世界时 Game.destroy 调用) */
70	  destroy(): void {
71	    for (const [t, fn, opts] of this.winListeners) window.removeEventListener(t, fn, opts);
72	    for (const [t, fn, opts] of this.elListeners) this.el.removeEventListener(t, fn, opts);
73	    this.winListeners = [];
74	    this.elListeners = [];
75	  }
76	
77	  down(code: string): boolean {
78	    return !this.uiBlocking && this.keys.has(code);
79	  }
80	
81	  /** 每帧末调用，处理一次性输入（滚轮切换快捷栏） */
82	  endFrame() {
83	    this.wheelDelta = 0;
84	  }
85	}
86	

```


---

## 🤖 Assistant · 2026-08-13T01:30:09.855Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Input.ts is minimal — no middle-click (no pick block). No H/J/B keys handled here. Now let me check Game.ts keydownHandlers to see which keys are handled (Digit1-0 hotbar, H/J/B, etc.).
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:10.347Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"keydownHandlers\\|inp.down('\\|inp.keys\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -40",
 "description": "List key handlers in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:10.371Z

**📎 ToolResult**

```
1362:    this.input.keydownHandlers.push((code) => {
2383:    player.inputX = (inp.down('KeyA') || inp.down('ArrowLeft') ? -1 : 0) + (inp.down('KeyD') || inp.down('ArrowRight') ? 1 : 0);
2384:    player.inputJump = inp.down('Space') || inp.down('KeyW') || inp.down('ArrowUp');
2385:    player.inputDown = inp.down('KeyS') || inp.down('ArrowDown');
2386:    player.inputUp = inp.down('KeyW') || inp.down('ArrowUp');
3808:    const controlSmart = inp.down('ControlLeft') || inp.down('ControlRight');
3873:    const controlTorch = inp.down('ShiftLeft') && !this.renderer.fullMap.open;
3948:      if (inp.down('KeyR') && !this.cartKeyLatch) {
3952:      if (!inp.down('KeyR')) this.cartKeyLatch = false;
3968:    if (inp.down('KeyR') && !this.cartKeyLatch && this.trackTile !== 0) {
3972:    if (!inp.down('KeyR')) this.cartKeyLatch = false;

```


---

## 🤖 Assistant · 2026-08-13T01:30:12.319Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1355,1400p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read Game.ts keydown handler block"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:12.341Z

**📎 ToolResult**

```
    // 音效按需加载（2026-08-10）：不在此预读——播放未命中时后台 fetch+decode、
    // 首播合成兜底；常用战斗/交互声在世界就绪后小集合预热（见 afterWorldLoad），
    // 怪物专属声效随首次受击懒加载
    this.input = new Input(this.renderer.canvas);
    this.cb = cb;
    // 快捷栏数字键：事件驱动（避免单帧内 down+up 被轮询漏掉）。
    // 背包打开时不切栏（原版 inventory 开启时数字键归 UI 导航）
    this.input.keydownHandlers.push((code) => {
      if (this.player && /^Digit[0-9]$/.test(code) && !this.input.uiBlocking) {
        this.player.inv.selected = code === 'Digit0' ? 9 : Number(code.slice(5)) - 1;
        this.cb.onInventoryChanged();
      }
      // 缩放调节
      if (code === 'Equal' || code === 'NumpadAdd') this.setZoom(this.camera?.zoomTarget + 0.15);
      if (code === 'Minus' || code === 'NumpadSubtract') this.setZoom(this.camera?.zoomTarget - 0.15);
      // F2:无敌+无限魔力(调试工具,原版无;Input 已 preventDefault)——F2 原像素
      // 画导入 2026-08-13 让位本键,迁往 F1
      if (code === 'F2') this.toggleDebugGod();
      // F1:图片 → 像素方块群导入(自研创意工具,原版无;Input 已 preventDefault)。
      // 原 F11 与系统全屏冲突 → F2 → 2026-08-13 再迁 F1
      if (code === 'F1') this.openPixelArtImport();
      // T:旅程模式时间倍率循环（CreativePowers.ModifyTimeRate.TargetTimeRate 1-24×，
      // CreativePowers.cs:866-884；Main.cs:6278 UpdateTimeRate 消费）——仅旅程世界可用，
      // 原版为时间菜单滑杆，此处取最小实现：按键循环常用档 + toast
      if (code === 'KeyT' && this.world?.isJourney) {
        const rates = [1, 2, 4, 8, 16, 24];
        const cur = rates.indexOf(this.world.journeyTimeRate);
        this.world.journeyTimeRate = rates[(cur + 1) % rates.length];
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.JourneyTimeRate', String(this.world.journeyTimeRate)));
      }
      // R:五彩扳手/宏伟蓝图模式循环(红蓝绿黄→剪线→致动器→剪致动器)
      if (code === 'KeyR') {
        const held = this.player?.inv.heldItem();
        if (held && ITEM_DEFS[held.id]?.wireTool && (viIdFromKey(ITEM_DEFS[held.id]?.key ?? '') === 3625 || viIdFromKey(ITEM_DEFS[held.id]?.key ?? '') === 3611)) {
          const modes = [
            [TOOL_RED, TOOL_GREEN, TOOL_BLUE, TOOL_YELLOW],
            [TOOL_CUTTER, TOOL_RED, TOOL_GREEN, TOOL_BLUE, TOOL_YELLOW],
            [TOOL_ACTUATOR],
            [TOOL_CUTTER, TOOL_ACTUATOR],
          ];
          const cur = modes.findIndex((m) => m.reduce((a, b) => a | b, 0) === this.wireToolMode);
          const next = modes[(cur + 1) % modes.length].reduce((a, b) => a | b, 0);
          this.wireToolMode = next;
          const name = next & TOOL_CUTTER
            ? (next & TOOL_ACTUATOR ? Lang.text('Mods.SandboxWorld.Wire.CutActuator') : Lang.text('Mods.SandboxWorld.Wire.Cut'))
            : next & TOOL_ACTUATOR ? Lang.text('Mods.SandboxWorld.Wire.Actuator') : Lang.text('Mods.SandboxWorld.Wire.All');

```


---

## 🤖 Assistant · 2026-08-13T01:30:15.250Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: only Digit0-9 hotbar, zoom, F1/F2, T (journey), R (wire tool). **No H (QuickHeal), J (QuickMana), B (QuickBuff), H/H mount (QuickMount)**. So quick keys H/J/B/R-mount are NOT implemented ❌.

Wait — what about QuickHeal_GetItemToUse usage? Earlier grep found only a comment at 3664. Let me check that comment — it mentions QuickMana principle. Let me read 3650-3680 to see if there's auto-mana on spellcast.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:15.573Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3650,3700p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read mana auto-consume context"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:15.592Z

**📎 ToolResult**

```
    }
    this.dmgNumbers.length = wn;

    inp.endFrame();

    // 挥剑命中判定（实体更新后）
    this.postUpdate();
  }

  // ================= 物品使用：挖掘 / 放置 / 攻击 / 使用 =================

  /** vi_ 工具桥接（vanilla-itemfunc.json pick/axe/hammer → tool def）。
   *  双工具族（Hamaxe 579/990/1294/2176 = pick+axe；The Axe 132 等 6 件 = axe+hammer）
   *  按 Player.cs:45040-45045 语义单物品同时携带多力：主类型仍取 pick>axe>hammer
   *  供挥击/智能光标用，三力附在 pickPower/axePower/hammerPower 上——挖掘入口
   *  dualToolResolve 按目标 tile 族（tileAxe/tileHammer）分流取对应力 */
  /** 魔力花族自动喝蓝（manaFlower：施法魔力不足时自动消耗背包魔力药水，
   *  Player.cs QuickMana 原理同 QuickHeal；返回 true=已补蓝可重试施法） */
  private tryAutoManaPotion(): boolean {
    const inv = this.player.inv;
    for (let i = 0; i < inv.slots.length; i++) {
      const s = inv.slots[i];
      if (!s) continue;
      const def = ITEM_DEFS[s.id];
      if (!def) continue;
      const m = /^vi_(\d+)_/.exec(def.key);
      if (!m) continue;
      const f = itemFuncOfVid(+m[1]);
      if (f?.healMana && f.consumable && !f.createTile) {
        this.player.mana = Math.min(this.player.maxMana, this.player.mana + f.healMana);
        this.player.buffs.apply(BuffType.ManaSickness, 5); // 魔力眩晕（300t/瓶）
        inv.removeAt(i, 1);
        this.sfx.play('drink');
        this.cb.onInventoryChanged();
        return true;
      }
    }
    return false;
  }

  private itemFuncTool(id: number): (typeof ITEM_DEFS)[number]['tool'] {
    const def = ITEM_DEFS[id];
    if (!def) return undefined;
    const m = /^vi_(\d+)_/.exec(def.key);
    if (!m) return undefined;
    const f = itemFuncOfVid(+m[1]);
    if (!f || !(f.pick || f.axe || f.hammer)) return undefined;
    const c = itemCombat(+m[1]);
    return {
      type: f.pick ? 'pick' : f.axe ? 'axe' : 'hammer',
      power: f.pick ?? f.axe ?? f.hammer,

```


---

## 🤖 Assistant · 2026-08-13T01:30:20.927Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: no QuickHeal/QuickMana/QuickBuff keys. Only mana-flower auto-mana. Note: implementation applies ManaSickness 5s per potion — vanilla is 300 ticks? Let me check. Actually vanilla Mana Sickness per mana potion is 5 seconds? Vanilla: `QuickMana_GetItemToUse` and ManaSickness duration... In vanilla, drinking a mana potion applies Mana Sickness for 5 seconds? Hmm. From memory note "魔力眩晕=94非33(33是Weak)". Vanilla: buffTime = 5*60=300? Actually vanilla sets `AddBuff(94, 300)` per potion? Let me not go down this path — that's outside my domain (buff). Skip.

Now let me check:
1. Placement alignment — multi-tile object placement (TileObjectData anchor). Check the placeFurn code in Game.ts.
2. Right-click priority chain (door/chest/statue/bed/flag).
3. Pick block (middle click).
4. Cursor style change when smart cursor on.
5. Multi-tile placement aids (continuous wall/blocks).

Let me grep Game.ts for tryPlace details (anchor, overlap rejection, slope) and interactAt priority order.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:21.434Z · glm-x-preview-260804

```
快捷键 H/J/B 确认未实装(仅数字键/F1/F2/T/R)。现查放置对齐(锚点/多格/重叠拒绝/斜坡)与右键优先级链。
```


---

## 🤖 Assistant · 2026-08-13T01:30:22.037Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"placeFurn\\|interactAt\\|anchor\\|Anchor\\|slope\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | sed -n '1,40p'",
 "description": "Locate placement and interact functions"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:22.059Z

**📎 ToolResult**

```
17:import { torchAnchorFrame, torchStillAnchored, torchStyleOfItemKey, isWaterTorchStyle } from '../world/Torch';
45:  scanPylons, pylonAnchorAt, mapFocusRect, checkPylonTeleport,
72:  FURNITURE_TILE_KIND, furnitureAnchor, furniturePlaceSingle, furniturePopSingle,
883:  private netFindAnchor(s: ProjSnap, srcId?: number): Enemy | null {
887:    const anchorNetId = (s.netId >>> 24) * 0x1000000 + (srcId & 0xffffff);
888:    for (const [, pup] of this.netNpcPuppets) if (pup.e.netId === anchorNetId) return pup.e;
915:        const m = new MLDeathray(this.netFindAnchor(s, srcId), kindBit === 0 ? 'head' : 'core',
924:        const o = new LunarOrb(this.netFindAnchor(s, parentId), is574 ? 574 : 539, s.vx, s.vy, s.dmg, s.x + 9, s.y + (is574 ? 9 : 15));
1269:  grandAnchor: [number, number] | null = null;
2308:        // zoom 从 0.5 缓动到 2，缓动期间 applyMapAnchor 每帧补偿 pan，主角始终居中
2311:        fm.anchorU = player.cx / TILE;
2312:        fm.anchorV = player.cy / TILE;
2313:        fm.anchorMX = this.renderer.canvas.width / 2;
2314:        fm.anchorMY = this.renderer.canvas.height / 2;
2316:        fm.panX = (this.world.w * fm.zoom) / 2 - fm.anchorU * fm.zoom;
2317:        fm.panY = (this.world.h * fm.zoom) / 2 - fm.anchorV * fm.zoom;
4032:        this.interactAt(tx, ty);
5128:      // 原版锤循环（Player.cs:45625-45695）：整砖→半砖→slope1→2→3→4→整砖。
5129:      // 方向感知：右实左空 → 先 slope2；上实下空（天花板模式）→ 先 slope3/4。
5131:      // 平台 slope 帧的楼梯绘制 + 对应坡面碰撞（平台 slope1-4 的可行走楼梯几何）
5138:        // WorldGen.SolidTile：active && tileSolid && !solidTop && !half && slope==0
5143:          return !!st.flags[j] && !!dj && dj.solid && !dj.platform && !st.half[j] && st.slope[j] === 0;
5145:        if (st.half[i] || st.slope[i] !== 0) {
5147:          if ((solidFull(tx + 1, ty) || st.slope[st.idx(tx + 1, ty)] === 1 || st.slope[st.idx(tx + 1, ty)] === 3)
5150:          const s = st.slope[i];
5400:    const doorAnchor = clearDoorAt(st, x, y);
5401:    if (doorAnchor) {
5402:      this.spawnDrop(doorAnchor[0] * TILE + 8, doorAnchor[1] * TILE, typeof def.drop === 'number' ? VI(def.drop) : (def.drop ?? VI(25)), 1);
5414:      const [fax, fay] = furnitureAnchor(st, fKind, x, y);
5441:          const phaseAnchor = st.frameX[ni] % (ow * 18) === 0 && st.frameY[ni] % (oh * 18) === 0;
5443:          if (phaseAnchor && boxContains) {
5580:        const phaseAnchor = st.frameX[ni] % (ow * 18) === 0 && st.frameY[ni] % (oh * 18) === 0;
5582:        if (phaseAnchor && boxContains) {
5848:      if (!this.grandAnchor) { this.grandAnchor = [tx, ty]; return; }
5849:      const a = this.grandAnchor;
5850:      this.grandAnchor = null;
6034:      const frame = torchAnchorFrame(st, tx, ty);
6059:    // 锚点表：AnchorTop/Bottom/Wall/AlternateTiles + 方向备选），全量锚点表未提取——
6061:    // 矿车轨道（314）例外：无锚点可悬空铺设（TileObjectData 314 无 Anchor 项）
6226:    const [ax, ay] = furnitureAnchor(st, kind, tx, ty);

```


---

## 🤖 Assistant · 2026-08-13T01:30:23.740Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '6040,6120p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read furniture placement anchor logic"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:23.765Z

**📎 ToolResult**

```
      if (st.liquid[st.idx(tx, ty)] > 0 && !isWaterTorchStyle(style * 22)) return;
      st.setTile(tx, ty, tileId, frame, style * 22);
      this.player.inv.removeAt(this.player.inv.selected, 1);
      this.player.useTime = 14;
      this.sfx.play('place');
      this.cb.onInventoryChanged();
      return;
    }
    // 放置空间检查
    for (let dx2 = 0; dx2 < ow; dx2++) {
      for (let dy2 = 0; dy2 < oh; dy2++) {
        const px = tx + dx2, py = ty + dy2;
        if (!st.inBounds(px, py)) return;
        if (st.isActive(px, py)) return;
        // 实心物不能与玩家重叠
        if (def.solid && this.overlapsEntity(px, py)) return;
      }
    }
    // 支撑检查：非漂浮。原版权威 = TileObjectData.CanPlace（TileObjectData.cs 每_tile
    // 锚点表：AnchorTop/Bottom/Wall/AlternateTiles + 方向备选），全量锚点表未提取——
    // 此处以"下/上/侧邻任一格有内容或墙"近似（依赖登记：TileObjectData 锚点类型表）。
    // 矿车轨道（314）例外：无锚点可悬空铺设（TileObjectData 314 无 Anchor 项）
    const isTrack = def.vanilla?.sheet === TRACK_SHEET;
    const needSupport = !isTrack && (def.solid || def.platform || def.framed);
    if (needSupport && !this.hasSupport(tx, ty, ow, oh)) return;
    if (this.player.useTime > 0) return;

    // 矿车轨道（WorldGen.PlaceTile case 314 → Minecart.PlaceTrack + SquareTileFrame：
    // frameX/frameY 是连接 ID 非 18px 像素偏移，随后 FrameTrack 按邻接定型；
    // style = placeStyle：0 普通 / 1 压板(2492) / 2 左加速(2739)；声效 Item52）
    if (isTrack) {
      const style = Math.max(0, Math.min(3, itemDef.placeStyle ?? 0));
      placeTrack(st, tx, ty, style);
      frameTrackArea(st, tx, ty);
      this.player.inv.removeAt(this.player.inv.selected, 1);
      this.player.useTime = 14;
      this.playSfxFile('Item_52', 0.8, tx * TILE, ty * TILE);
      this.cb.onInventoryChanged();
      return;
    }

    // 放置
    const isVanillaStyle = !!def.vanilla && def.vanilla.frame === 'style';
    for (let dx2 = 0; dx2 < ow; dx2++) {
      for (let dy2 = 0; dy2 < oh; dy2++) {
        const px = tx + dx2, py = ty + dy2;
        // 原版多格家具：帧用 18px 步长偏移（与 .wld 原生一致，渲染端直用）。
        // 原版帧语义（TileObject.Place L74-102）：frameY 从【顶行 = 0】向下递增；
        // ty 是顶部行（放置时鼠标指向顶部锚点）→ dy2=0 即顶行，frameY = dy2*18 正确
        if (isVanillaStyle) {
          // placeStyle → 样式基偏移:权威布局表(FurnitureStyle.ts;竖排族写 Y,
          // 旧公式 style*fw*18 一刀切会把灯笼/蜡烛/吊灯等写成非法帧)
          const [bx2, by2] = furnitureStyleBase(def.vanilla?.sheet ?? -1, itemDef.placeStyle ?? 0, def.vanilla?.fw ?? 1);
          st.setTile(px, py, tileId, bx2 + dx2 * 18, by2 + dy2 * 18);
        } else {
          st.setTile(px, py, tileId, dx2, dy2);
        }
        // 水被方块挤出：水量转移到相邻可容纳的格子（上/左/右），
        // 而不是被方块吞掉消失。封闭无处可去时才消失
        const pi = st.idx(px, py);
        const liq = st.liquid[pi];
        if (liq > 0) {
          const ltype = st.liquidType[pi];
          st.setLiquid(px, py, 0, 0);
          let remaining = liq;
          for (const [ox, oy] of [[0, -1], [-1, 0], [1, 0]] as const) {
            if (remaining <= 0) break;
            const nx = px + ox, ny = py + oy;
            if (!st.inBounds(nx, ny)) continue;
            const nd = TILE_DEFS[st.type[st.idx(nx, ny)]];
            if (nd && nd.solid) continue;
            const ni = st.idx(nx, ny);
            const cap = 255 - st.liquid[ni];
            if (cap <= 0) continue;
            const t = Math.min(remaining, cap);
            st.setLiquid(nx, ny, st.liquid[ni] + t, ltype || st.liquidType[ni] || 1);
            remaining -= t;
          }
        }
      }
    }

```


---

## 🤖 Assistant · 2026-08-13T01:30:31.374Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key placement logic (tryPlace at ~6046-6120):
- Anchor: `tx, ty` = top-left of multi-tile object ("ty 是顶部行（放置时鼠标指向顶部锚点）"). Vanilla: TileObjectData.CoordinatePadding... Actually in vanilla, `PlaceThing_Tiles` calls `TileObject.CanPlace` with the target tile being the **bottom-left** anchor for most furniture? Hmm. Let me check vanilla: `TileObjectData.Coordinates`... In vanilla, when you place a multi-tile object like a table (3×2), the placement anchor is the **bottom-left tile** for objects with `AnchorBottom`? No wait.

Actually in vanilla, `TileObject.CanPlace(x, y)` — the x,y passed is the mouse target tile, and it's the **bottom-left** of the placement area? Let me check. From memory of TileObject.CanPlace: it computes `x -= ...`? Let me look at vanilla TileObject.cs CanPlace.

Actually — in Terraria, when you place a 3-wide 2-tall table, the game places it such that the mouse tile becomes the... I believe the anchor is the top-left, and objects are drawn downward. Hmm, but memory notes say "placeFurn 横排假设受害清单/灯笼亮灭档在X样式在Y/吊灯双轴" and "原版门帧竖排布局 — style=36*(fx/54)+fy/54、PlaceTile 放门要 j-2". The memory note says **PlaceTile 放门要 j-2** — meaning vanilla places doors at y-2 offset (i.e., mouse tile is the BOTTOM tile of the door, and the object extends UP). That's for doors (3-tall anchored at bottom).

So vanilla anchor depends on TileObjectData: for most multi-tile objects with AnchorBottom, the object's bottom row is at the mouse Y? Let me check TileObject.cs CanPlace to determine anchor semantics.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:31.961Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && find . -name \"TileObject.cs\" | head -2; grep -n \"public static bool CanPlace\" TileObject.cs 2>/dev/null | head -3",
 "description": "Locate TileObject.cs CanPlace"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:31.993Z

**📎 ToolResult**

```
./TileObject.cs
174:	public static bool CanPlace(int x, int y, int type, int style, int dir, out TileObject objectData, bool onlyCheck = false, int? forcedRandom = null)

```


---

## 🤖 Assistant · 2026-08-13T01:30:33.510Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '174,260p' TileObject.cs",
 "description": "Read TileObject.CanPlace anchor semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:33.530Z

**📎 ToolResult**

```
	public static bool CanPlace(int x, int y, int type, int style, int dir, out TileObject objectData, bool onlyCheck = false, int? forcedRandom = null)
	{
		TileObjectData tileData = TileObjectData.GetTileData(type, style);
		objectData = Empty;
		if (tileData == null)
		{
			return false;
		}
		int num = x - tileData.Origin.X;
		int num2 = y - tileData.Origin.Y;
		if (num < 0 || num + tileData.Width >= Main.maxTilesX || num2 < 0 || num2 + tileData.Height >= Main.maxTilesY)
		{
			return false;
		}
		bool flag = tileData.RandomStyleRange > 0;
		if (TileObjectPreviewData.placementCache == null)
		{
			TileObjectPreviewData.placementCache = new TileObjectPreviewData();
		}
		TileObjectPreviewData.placementCache.Reset();
		int num3 = 0;
		if (tileData.AlternatesCount != 0)
		{
			num3 = tileData.AlternatesCount;
		}
		float num4 = -1f;
		float num5 = -1f;
		int num6 = 0;
		TileObjectData tileObjectData = null;
		int num7 = -1;
		bool flag2 = false;
		while (num7 < num3)
		{
			num7++;
			TileObjectData tileData2 = TileObjectData.GetTileData(type, style, num7);
			if (tileData2.Direction != TileObjectDirection.None && ((tileData2.Direction == TileObjectDirection.PlaceLeft && dir == 1) || (tileData2.Direction == TileObjectDirection.PlaceRight && dir == -1)))
			{
				continue;
			}
			int num8 = x - tileData2.Origin.X;
			int num9 = y - tileData2.Origin.Y;
			if (num8 < 5 || num8 + tileData2.Width > Main.maxTilesX - 5 || num9 < 5 || num9 + tileData2.Height > Main.maxTilesY - 5)
			{
				return false;
			}
			Rectangle rectangle = new Rectangle(0, 0, tileData2.Width, tileData2.Height);
			int num10 = 0;
			int num11 = 0;
			if (tileData2.AnchorTop.tileCount != 0)
			{
				if (rectangle.Y == 0)
				{
					rectangle.Y = -1;
					rectangle.Height++;
					num11++;
				}
				int checkStart = tileData2.AnchorTop.checkStart;
				if (checkStart < rectangle.X)
				{
					rectangle.Width += rectangle.X - checkStart;
					num10 += rectangle.X - checkStart;
					rectangle.X = checkStart;
				}
				int num12 = checkStart + tileData2.AnchorTop.tileCount - 1;
				int num13 = rectangle.X + rectangle.Width - 1;
				if (num12 > num13)
				{
					rectangle.Width += num12 - num13;
				}
			}
			if (tileData2.AnchorBottom.tileCount != 0)
			{
				if (rectangle.Y + rectangle.Height == tileData2.Height)
				{
					rectangle.Height++;
				}
				int checkStart2 = tileData2.AnchorBottom.checkStart;
				if (checkStart2 < rectangle.X)
				{
					rectangle.Width += rectangle.X - checkStart2;
					num10 += rectangle.X - checkStart2;
					rectangle.X = checkStart2;
				}
				int num14 = checkStart2 + tileData2.AnchorBottom.tileCount - 1;
				int num15 = rectangle.X + rectangle.Width - 1;
				if (num14 > num15)
				{

```


---

## 🤖 Assistant · 2026-08-13T01:30:36.963Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla anchor = `x - tileData.Origin.X`, `y - tileData.Origin.Y` — i.e., the **Origin** (bottom-center for most furniture, e.g., Origin = (Width/2, Height-1)). For a 3-wide 2-tall table: Origin = (1,1) → object top-left = (x-1, y-1). So the mouse tile is roughly the object's **bottom-center** for furniture anchored at bottom.

The implementation places at top-left `tx,ty` directly (comment says "ty 是顶部行（放置时鼠标指向顶部锚点）"). That's a 🔀 logic difference: multi-tile furniture will be offset (up-left vs vanilla bottom-center origin). Hmm, but wait — maybe there's an offset somewhere. Let me check how tryPlace computes tx/ty and whether it subtracts an origin. Let me read the beginning of tryPlace.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:37.584Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '5975,6045p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read tryPlace head for anchor offset"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:37.602Z

**📎 ToolResult**

```
      }
    }
  }

  private tryPlace(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
    if (!this.netCanEditTile()) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    const st = this.world.store;
    if (!st.inBounds(tx, ty)) return;
    // 距离
    const dx = tx - Math.floor(this.player.cx / TILE);
    const dy = ty - Math.floor(this.player.cy / TILE);
    if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) return;
    const tileId = TILE_BY_KEY[itemDef.tile!];
    const def = TILE_DEFS[tileId];
    // 旧日军团竞技场建造封锁（Player.cs:25669-25672：DD2Event.Ongoing &&
    // ShouldBlockBuilding → 禁改方块，DD2Event.cs:794-796 包围盒判定）
    if (this.world.oldOnesArmy.ongoing
      && shouldBlockBuilding(this.world.oldOnesArmy, tx * TILE + 8, ty * TILE + 8)) {
      return;
    }
    // 传送晶塔放置门（TETeleportationPylon.PlacementPreviewHook_CheckIfCanPlace :158-166）：
    // 同型晶塔全图仅一座（HasPylonOfType TeleportPylonsSystem.cs:41-44）
    if (def?.vanilla?.sheet === 597) {
      this.refreshPylons();
      const style = itemDef.placeStyle ?? 0;
      if (hasPylonOfType(this.pylons, style)) return;
    }
    // 橡实: 只能种在草块正上方
    if (viIdFromKey(itemDef.key) === 27) {
      if (st.get(tx, ty + 1) !== T.GRASS) {
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.AcornGrassOnly'));
        return;
      }
      // 成就：种橡实（Player.PlantAcorn → PlantedAcorn，CONSERVATIONIST 计数）
      this.achievements.plantedAcorn();
    }
    const ow = def.w ?? 1, oh = def.h ?? 1;
    // 绳索(RopeCoil 语义):从放置点向下延伸至实心/最多 10 格
    if (viIdFromKey(itemDef.key) === 965) {
      const ropeTile = TILE_BY_KEY['v_213_rope']!;
      let placed = 0;
      for (let y = ty; y < ty + 10; y++) {
        if (!st.inBounds(tx, y) || st.isActive(tx, y)) break;
        st.setTile(tx, y, ropeTile, 0, 0);
        placed++;
      }
      if (placed > 0) {
        this.player.inv.removeAt(this.player.inv.selected, 1);
        this.player.useTime = 14;
        this.sfx.play('place');
        this.cb.onInventoryChanged();
      }
      return;
    }
    // 火把锚定（TileObjectData tile4 + TileObject.CanPlace 1:1）：
    // 底锚(0)→左锚(22)→右锚(44)→墙锚(0)；普通火把液体中拒绝、水炬 8/11/17 允许
    if (tileId === T.TORCH) {
      if (this.player.useTime > 0) return;
      if (st.isActive(tx, ty)) return;
      const frame = torchAnchorFrame(st, tx, ty);
      // placeStyle（Item.cs placeStyle→TileObjectData subtile）：彩色 427-433 /
      // 群系火把显式表 / 水炬 8/11/17——此前恒 0 = 群系火把放成普通火把（色光全失）
      const style = torchStyleOfItemKey(itemDef.key);
      if (frame < 0) return;
      // 液体门（WaterPlacement）：普通火把 NotAllowed、水炬三色 Allowed
      if (st.liquid[st.idx(tx, ty)] > 0 && !isWaterTorchStyle(style * 22)) return;
      st.setTile(tx, ty, tileId, frame, style * 22);
      this.player.inv.removeAt(this.player.inv.selected, 1);
      this.player.useTime = 14;
      this.sfx.play('place');
      this.cb.onInventoryChanged();

```


---

## 🤖 Assistant · 2026-08-13T01:30:43.100Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: `tryPlace` uses `tx, ty` as top-left, `ow/oh` from def, no Origin offset. Vanilla uses `x - Origin.X, y - Origin.Y` where Origin for most furniture is (w/2 floor, h-1) i.e. bottom-center. So a 3×2 table placed in vanilla at mouse tile m sits with its bottom-center at m; in this repo it sits with its top-left at m → the object appears **up to (w-1, h-1) tiles off** (for a 3-wide 2-tall table: 2 right + 1 down shift... wait, vanilla top-left = (x-1, y-1), impl top-left = (x, y) → impl object is 1 right and 1 down compared to vanilla).

Hmm, but let me double check whether the caller (useItem path at 4032-4050) subtracts an origin before calling tryPlace. Let me check where tryPlace is called and whether there's a furnitureAnchor adjustment. Earlier grep showed line 6226 `const [ax, ay] = furnitureAnchor(st, kind, tx, ty);` — that's in a different function (probably interactAt or furniture removal). Let me find tryPlace callers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:43.588Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"tryPlace(\\|tryPlaceWall(\\|hasSupport\\|overlapsEntity\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -15",
 "description": "Find tryPlace callers and support check"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:43.611Z

**📎 ToolResult**

```
4164:      this.tryPlaceWall(tx, ty, heldDef);
4168:      this.tryPlace(tx, ty, heldDef);
5914:  private tryPlaceWall(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
5979:  private tryPlace(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
6055:        if (def.solid && this.overlapsEntity(px, py)) return;
6064:    if (needSupport && !this.hasSupport(tx, ty, ow, oh)) return;
6187:  private overlapsEntity(px: number, py: number): boolean {
6196:  private hasSupport(x: number, y: number, w: number, h: number): boolean {
7641:      if (!closeDoor(st, x, y, Math.random, (bx, by) => this.overlapsEntity(bx, by))) return;

```


---

## 🤖 Assistant · 2026-08-13T01:30:46.730Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '4150,4175p;6187,6230p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read useItem placement dispatch and hasSupport"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:46.751Z

**📎 ToolResult**

```
          return;
        }
      }
    }

    // 电路工具(扳手/剪线钳/致动器/致动魔杖/五彩扳手/宏伟蓝图):左键,目标格可被占用
    if (heldDef?.wireTool && inp.mouseDown && !inp.rightDown) {
      this.useWireTool(tx, ty, heldDef);
      return;
    }

    // 可放置物品：左键放置
    // 墙面物品（Player.PlaceThing_Walls，Player.cs:38937）：左键铺墙
    if (heldDef?.wallId != null && inp.mouseDown && !inp.rightDown) {
      this.tryPlaceWall(tx, ty, heldDef);
      return;
    }
    if (heldDef?.tile && !inp.rightDown) {
      this.tryPlace(tx, ty, heldDef);
      return;
    }

    // 其它物品（药水/食物/镜子/召唤物等）：左键使用，useStyle 分族姿势
    // （Player.ItemCheck：itemAnimationMax = useAnimation，ApplyUseStyle 按 useStyle
    //  路由——4 举过头（镜子/机械三王召唤）/5 朝鼠标静持（火把族非放置路径）/
    //  9 举杯（增益药水 DefaultToHealingPotion）/2 咀嚼（食物 DefaultToFood）/
  private overlapsEntity(px: number, py: number): boolean {
    const rx = px * TILE, ry = py * TILE;
    if (this.player.x < rx + TILE && this.player.x + this.player.w > rx && this.player.y < ry + TILE && this.player.y + this.player.h > ry) return true;
    for (const e of this.entities.enemies) {
      if (e.x < rx + TILE && e.x + e.w > rx && e.y < ry + TILE && e.y + e.h > ry) return true;
    }
    return false;
  }

  private hasSupport(x: number, y: number, w: number, h: number): boolean {
    const st = this.world.store;
    // 下方
    for (let dx = 0; dx < w; dx++) {
      if (st.isActive(x + dx, y + h) || st.isSolid(x + dx, y + h) || st.wall[st.idx(x + dx, y + h)] !== 0) return true;
    }
    // 上方（火把等贴墙物）
    for (let dx = 0; dx < w; dx++) {
      if (st.isActive(x + dx, y - 1)) return true;
    }
    // 侧邻
    for (let dy = 0; dy < h; dy++) {
      if (st.isActive(x - 1, y + dy) || st.isActive(x + w, y + dy)) return true;
    }
    return false;
  }

  /**
   * 挂物族右键交互（Player.cs:32093-32121 → TE*.OnPlayerInteraction 1:1）：
   *  手持可放且未收藏 → 放入（单槽族 TryPlacing :83-100：占位物先弹出为掉落，
   *   再写入新物 stack=1，手持 -1；模特/帽架 TryFitting :680-725/:337-369：
   *   多叠放 1 克隆/单叠整槽交换，回写手持格）；
   *  否则 → 取出（单槽族 = OnPlayerInteraction else 分支 :134-151 →
   *   KillTile(fail:true) → KillTile_DropItems :63703 提前 return：存放物弹为
   *   世界掉落、方块保留；模特/帽架原版此时打开槽位 UI（BasicOpenCloseInteraction
   *   TileEntity.cs:250-285），本作无该 UI，最小等价 = 按原版槽位序取首个非空，
   *   空手优先回手持格（保留词缀），否则入包、装不下掉落）
   */
  private useFurnitureInteraction(tx: number, ty: number, kind: FurnitureKind) {
    const st = this.world.store;
    const [ax, ay] = furnitureAnchor(st, kind, tx, ty);
    const list = this.world.furnitureItems;
    const held = this.player.inv.heldItem();
    const vid = held ? slotVanillaId(held.id) : -1;
    if (held && vid > 0 && !held.favorited && fitsFurniture(kind, vid)) {

```


---

## 🤖 Assistant · 2026-08-13T01:30:50.974Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Confirmed:
- Placement anchor: top-left (tx,ty), no Origin centering → 🔀 vs vanilla bottom-center Origin.
- Support check (hasSupport): approximation — "下/上/侧邻任一格有内容或墙" — vs vanilla TileObjectData anchor table. The comment itself admits "全量锚点表未提取——此处近似".
- Overlap rejection: `if (st.isActive(px, py)) return;` — strict reject if ANY tile in the object footprint is active. Vanilla allows replacement of certain tiles: `TileID.Sets.BreakableWhenPlacing` (e.g., tall grass, vines) — vanilla `TileObject.CanPlace` allows placement over tiles in that set (it kills them). Let me verify: in TileObject.CanPlace there's a check:

```csharp
if (Main.tile[num8 + num10, num9 + num11].active() && !TileID.Sets.CanBeClearedDuringGeneration... 
```

Actually vanilla: `bool flag = ...; if (tile.active() && !Main.tileCut[tile.type] && !TileID.Sets.BreakableWhenPlacing[tile.type])`? Let me grep TileObject.cs for BreakableWhenPlacing.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:51.381Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"BreakableWhenPlacing\\|tileCut\" TileObject.cs | head -10",
 "description": "Check TileObject.CanPlace overlap allowance"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:30:51.404Z

**📎 ToolResult**

```
84:					if (tileSafely.active() && tileSafely.type != 484 && (Main.tileCut[tileSafely.type] || TileID.Sets.BreakableWhenPlacing[tileSafely.type]))
357:					if (tileSafely.active() && (!Main.tileCut[tileSafely.type] || tileSafely.type == 484 || tileSafely.type == 654) && !TileID.Sets.BreakableWhenPlacing[tileSafely.type])

```


---

## 🤖 Assistant · 2026-08-13T01:30:54.473Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla `TileObject.CanPlace` line 357: rejects a tile only if `active && !tileCut && !BreakableWhenPlacing` — so placing furniture over tall grass/vines IS allowed in vanilla. Implementation: `if (st.isActive(px, py)) return;` — strict rejection of any active tile → **placement over cut-plants (grass/vines) wrongly rejected**. That's a real 🔀/❌ deviation.

Note also vanilla treats `type == 484 || 654` specially in line 84 (that's during placement of the "preview"?). Line 357 is the actual check.

Now, right-click priority chain. Let me read interactAt to map the priority order. It's around line 6290+. Let me find the interactAt function start.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:30:54.918Z · glm-x-preview-260804

```
原版 CanPlace 允许压过可割植物/BreakableWhenPlacing——实现是全拒绝。现读 interactAt 右键优先级链。
```


---

## 🤖 Assistant · 2026-08-13T01:30:55.654Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private interactAt\\|interactAt(\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts; awk 'NR>=6240 && NR<=6290' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | grep -n \"//\" | head -30",
 "description": "Locate interactAt and its comment chain"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:07.621Z

**📎 ToolResult**

```
4032:        this.interactAt(tx, ty);
6287:  private interactAt(tx: number, ty: number) {
1:          this.sfx.play('pickup'); // SoundID 7（TryFitting :698）
9:          this.sfx.play('pickup'); // SoundID 7（TEHatRack.cs:351）
15:          // 占位旧物先弹出（TryPlacing :91-93 result.DropItem → 世界掉落）
26:    // 取出
50:    // 距离门（原版 Player.IsInTileInteractionRange Simple：约 5 格）——此前整个
51:    // interactAt 无距离检查，隔全图右键可开储物/设床重生点

```


---

## 🤖 Assistant · 2026-08-13T01:31:09.421Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '6287,6480p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read interactAt right-click priority chain"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:09.440Z

**📎 ToolResult**

```
  private interactAt(tx: number, ty: number) {
    const st = this.world.store;
    // 距离门（原版 Player.IsInTileInteractionRange Simple：约 5 格）——此前整个
    // interactAt 无距离检查，隔全图右键可开储物/设床重生点
    {
      const dx = tx - Math.floor(this.player.cx / TILE);
      const dy = ty - Math.floor(this.player.cy / TILE);
      if (!this.inTileRange(tx, ty, (this.player.equipStats.tileRange ? 3 : 0) + (this.player.buffs.has(BuffType.Builder) ? 1 : 0))) { this.input.rightDown = false; return; }
    }
    const type = st.get(tx, ty);
    // 原版 tile sheet（八音盒/喷泉/天塔柱/派对柱右键分支用）
    const sh = this.wiring?.sheetOf(tx, ty) ?? -1;
    // 联机保护门禁（v3 房间制）：以下右键操作会改方块/世界状态——非房主在保护房拒绝。
    // 玩家储物族/读碑文/设床不受限（前者是玩家自有物品，后两者不改方块）。
    const editDenied = !this.netCanEditTile() && (
      type === T.DOOR_CLOSED || type === T.DOOR_OPEN || type === TILE_BY_KEY['v_83_herbs_mature']
      || type === TILE_BY_KEY['v_84_herbs_bloom'] || type === TILE_BY_KEY['crystal_heart']
      || type === TILE_BY_KEY['v_132_lever'] || type === TILE_BY_KEY['v_136_switch'] || type === TILE_BY_KEY['v_144_timers']
      || type === TILE_BY_KEY['v_356_enchanted_sundial'] || type === TILE_BY_KEY['v_663_enchanted_moondial'] // 日晷/月晷右键改世界时间态
      || FURNITURE_TILE_KIND.has(type) // 挂物族右键会改存放物（世界状态）
      || sh === 35 || sh === 139 || sh === 207 || sh === 410 || sh === 480 || sh === 509 || sh === 455
      || sh === 425
    );
    if (editDenied) { this.netDeny(Lang.text('Mods.SandboxWorld.Toast.RoomProtectTiles')); return; }
    // ---- 挂物族（物品框 395/武器架 471/模特 470/帽架 475/食物盘 520/展示罐 698；
    //  Player.cs:32093-32121 右键分支 → TE*.OnPlayerInteraction，全量语义在
    //  world/FurnitureItems.ts）----
    if (FURNITURE_TILE_KIND.has(type)) {
      this.useFurnitureInteraction(tx, ty, FURNITURE_TILE_KIND.get(type)!);
      return;
    }
    // ---- 提取机（tile 219 普通版 / 642 叶绿版；Player.cs:41008-41049
    //  PlaceThing_ItemInExtractinator 1:1，全量转化表见 world/Extractinator.ts）----
    if (type === (TILE_BY_KEY['v_219_extractinator'] ?? -1)
      || type === (TILE_BY_KEY['v_642_chlorophyte_extractinator'] ?? -1)) {
      this.useExtractinator(tx, ty, false);
      this.input.rightDown = false;
      return;
    }
    // ---- 玩家储物族（原版 Player.cs:32598+）：29→bank / 97→bank2 / 463→bank3 / 491→bank4。
    //  内容随玩家存档（banks[0..3]），不随方块；复用宝箱面板（x 用 -2..-5 标识容器来源，
    //  与原版 player.chest = -2..-5 同约定）----
    for (const [key, bi] of BANK_TILES) {
      if (type === (TILE_BY_KEY[key] ?? -1)) {
        this.openChest?.({ x: -2 - bi, y: 0, items: this.player.banks[bi] });
        this.sfx.play('tink');
        this.input.rightDown = false;
        return;
      }
    }
    if (type === T.DOOR_CLOSED) {
      this.toggleDoor(tx, ty, true);
    } else if (type === T.DOOR_OPEN) {
      this.toggleDoor(tx, ty, false);
    } else if (type === T.CHEST || this.wiring?.sheetOf(tx, ty) === 441 || this.wiring?.sheetOf(tx, ty) === 468) {
      // 陷阱箱 441/468 也走开箱流程(tryOpenChest 内触发电路+射镖)
      // 打开宝箱：精确命中或 3×3 容差（点击宝箱边缘也算）
      const chest = this.findChest(tx, ty) ?? this.findChestNear(tx, ty);
      if (chest) this.tryOpenChest(chest);
      else if (this.net) {
        // 联机：本地无箱数据（msg7 不传 chests，权威在服务器）→ msg31 请求，
        // onChestSync 回包后登记 world.chests 并自动开面板
        this.netPendingChest = { x: tx, y: ty };
        this.net.requestChestOpen(tx, ty);
        this.input.rightDown = false;
      }
    } else if (sh === 425) {
      // 广播盒右键（Player.cs:32231-32250 tileSign 分支 → OpenSign）：按帧回算
      // 2×2 锚点（:32240-32245 frameX/18、frameY/18），Sign.ReadSign(anchor,
      // CreateIfMissing:true) 懒建空牌项 → 文本编辑面板（保存走 setSignText）
      const iBox = st.idx(tx, ty);
      this.openSignEditor(tx - Math.floor(st.frameX[iBox] / 18), ty - Math.floor(st.frameY[iBox] / 18));
      this.input.rightDown = false;
    } else if (type === TILE_BY_KEY['tombstone_v']) {
      // 墓碑：读碑文（原版 Sign 阅读；碑文在 2×2 锚点登记，点任意一格都能读到）
      const sign = this.world.signs.find((s) =>
        tx >= s.x && tx <= s.x + 1 && ty >= s.y && ty <= s.y + 1);
      if (sign) this.cb.onReadSign?.(sign.text);
      this.input.rightDown = false;
    } else if (type === TILE_BY_KEY['crystal_heart']) {
      // 生命水晶(放置态):右键使用(Player.cs ItemCheck_UseLifeCrystal L29358)
      // statLifeMax<400 → +20 上限并回满该部分,放置物消耗
      this.usePlacedLifeCrystal(tx, ty);
    } else if (type === TILE_BY_KEY['bed']) {
      // 床（PC:32183-32228）：上侧（枕）悬停=设重生点；下侧（脚）悬停=睡觉（无夜间限制）
      const fx = this.world.store.frameX[this.world.store.idx(tx, ty)];
      const bottomSide = (fx % 72 < 36) !== (Math.floor(fx / 72) === 1); // PC:32869-32878
      if (bottomSide && Math.hypot(this.player.cx - (tx + 2) * TILE, this.player.cy - ty * TILE) <= 96) {
        // StartSleeping（SH:155-191）：搬锚点+清速；再点同床=起床（SH:170-173）
        this.player.sleeping = !this.player.sleeping;
        if (this.player.sleeping) {
          this.player.timeSleeping = 0;
          this.player.vx = 0; this.player.vy = 0;
          this.player.x = (tx + 1) * TILE; this.player.y = (ty - 1) * TILE; // 锚点=床上格
          this.player.facing = Math.floor(fx / 72) === 0 ? -1 : 1; // SH:204-210 床朝向
        }
      } else {
        this.world.spawnX = tx + 1;
        this.world.spawnY = ty - 1;
        this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.SpawnSet'));
      }
      this.input.rightDown = false;
    } else if (type === TILE_BY_KEY['v_356_enchanted_sundial']
      || type === TILE_BY_KEY['v_663_enchanted_moondial']) {
      // 附魔日晷/月晷（Player.cs:32166-32183 右键分支 → Main.Sundialing/Moondialing
      // :6240-6268）：冷却为 0 且未在快进 → 置 fastForwardTimeToDawn/Dusk + 冷却 8 天，
      // 时间按 dayRate=60 快进到黎明/黄昏；音效 SoundID.Item4。冷却随存档持久化
      // （WorldFile.cs:1311/1417），血月夜清零（StartNight :64892-64893）
      const sundial = type === TILE_BY_KEY['v_356_enchanted_sundial'];
      if (sundial ? (!this.world.fastForwardTimeToDawn && this.world.sundialCooldown === 0)
        : (!this.world.fastForwardTimeToDusk && this.world.moondialCooldown === 0)) {
        if (sundial) { this.world.fastForwardTimeToDawn = true; this.world.sundialCooldown = 8; }
        else { this.world.fastForwardTimeToDusk = true; this.world.moondialCooldown = 8; }
        this.sfx.play('drink'); // SoundID.Item4
      }
      this.input.rightDown = false;
    } else if (type === TILE_BY_KEY['v_125_crystal_ball'] || type === TILE_BY_KEY['v_354_bewitching_table']
      || type === TILE_BY_KEY['v_377_sharpening_station'] || type === TILE_BY_KEY['v_287_ammo_box']
      || type === TILE_BY_KEY['v_464_war_table'] || type === TILE_BY_KEY['v_621_slice_of_cake']) {
      // 工位 buff（Player.cs:32126-32162 右键授予）：水晶球 29(1800s)/附魔台 150/磨刀石 159/
      // 弹药箱 93/战争桌 348 均 108000t=1800s；蛋糕 192=7200t=120s
      const dur = type === TILE_BY_KEY['v_621_slice_of_cake'] ? 120 : 1800;
      const bt = type === TILE_BY_KEY['v_125_crystal_ball'] ? BuffType.Clairvoyance
        : type === TILE_BY_KEY['v_354_bewitching_table'] ? BuffType.Bewitched
          : type === TILE_BY_KEY['v_377_sharpening_station'] ? BuffType.Sharpened
            : type === TILE_BY_KEY['v_287_ammo_box'] ? BuffType.AmmoBox
              : type === TILE_BY_KEY['v_464_war_table'] ? BuffType.WarTable : BuffType.SugarRush;
      this.player.buffs.apply(bt, dur);
      this.sfx.play('drink'); // 原版 SoundID.Item4（药水/授予类 UseSound 占位）
      this.cb.onInventoryChanged();
      this.input.rightDown = false;
    } else if (type === TILE_BY_KEY['v_132_lever'] || type === TILE_BY_KEY['v_136_switch'] || type === TILE_BY_KEY['v_144_timers']
      || type === TILE_BY_KEY['v_411_detonator']) {
      // 拉杆/开关/计时器：HitSwitch（Wiring.cs:163-252 1:1）——帧翻转 + tripWire
      // 四色信号 BFS（hitWire :693-827，沿导线网络传播），沿线全部器件真实触发；
      // 非"直线可见"近似（旧注释已过期，电路系统全量移植后语义为导线连通）
      // 起爆器 411：原版为"对准使用任意物品"触发（Player.cs:31865）+ 坠落触发（:34368，
      // 已接 Game.fixedUpdate landImpactVy）——本作并入右键交互
      this.toggleSwitch(tx, ty, type);
    } else if (type === TILE_BY_KEY['v_83_herbs_mature'] || type === TILE_BY_KEY['v_84_herbs_bloom']) {
      // 药草收获:成熟/开花态右键 → 掉种子(style = frameX/18,WorldGen.cs:38731)
      const i = st.idx(tx, ty);
      const style = Math.floor(st.frameX[i] / 18);
      st.setTile(tx, ty, 0);
      const seedKeys = ['vi_307_daybloom_seeds', 'vi_308_moonglow_seeds', 'vi_309_blinkroot_seeds',
        'vi_311_waterleaf_seeds', 'vi_310_deathweed_seeds', 'vi_312_fireblossom_seeds', 'vi_2357_shiverthorn_seeds'];
      const sk = seedKeys[style] ?? seedKeys[0];
      this.spawnDrop(tx * 16 + 8, ty * 16, sk, 1);
      this.input.rightDown = false;
    } else if (sh === 35 || sh === 139) {
      // 八音盒/南瓜灯右键（Player.cs:31759-31764）：SoundID 28 + SwitchMB（与电路共用）
      this.sfxAt('mech', tx * 16 + 8, ty * 16 + 8);
      this.wiring && switchMB(this.wiring, tx, ty);
      this.input.rightDown = false;
    } else if (sh === 207) {
      // 喷泉右键（Player.cs:31796-31800）
      this.sfxAt('mech', tx * 16 + 8, ty * 16 + 8);
      this.wiring && switchFountain(this.wiring, tx, ty);
      this.input.rightDown = false;
    } else if (sh === 410 || sh === 480 || sh === 509 || sh === 657 || sh === 658 || sh === 720 || sh === 721 || sh === 725 || sh === 733) {
      // 天塔柱族右键（Player.cs:31801-31808）
      this.sfxAt('mech', tx * 16 + 8, ty * 16 + 8);
      this.wiring && switchMonolith(this.wiring, tx, ty);
      this.input.rightDown = false;
    } else if (sh === 455) {
      // 派对纪念碑右键（Player.cs:31809-31814 → ToggleManualParty）
      this.sfxAt('mech', tx * 16 + 8, ty * 16 + 8);
      toggleManualParty(this.partyState);
      // 成就：派对进行中（prog 25，与自然派对同源）
      if (partyIsUp(this.partyState)) this.achievements.notifyProgressionEvent(25);
      this.input.rightDown = false;
    } else if (type === TILE_BY_KEY['v_237_lihzahrd_altar']) {
      // 蜥蜴祭坛 237（Player.cs:32303-32335）：消耗蜥蜴能量电池召石巨人
      this.useLihzahrdAltar(tx, ty);
    } else if (type === TILE_BY_KEY['v_466_elder_cystal_stand']) {
      // 永恒水晶座 466（Player.cs:31930-31977）：永恒水晶 → 旧日军团
      this.useEterniaStand(tx, ty);
    } else if (type === TILE_BY_KEY['v_597_pylons']) {
      // 传送晶塔 597（Player.cs:31707-31747）：开全屏地图选其它晶塔传送
      this.usePylon(tx, ty);
    }
  }

  /**
   * 提取机对准使用（Player.cs:41008-41049 PlaceThing_ItemInExtractinator 1:1）。
   * 优先级：642 叶绿版先查矿物兑换表（ItemTrader.ChlorophyteExtractinator，
   * Player.cs:41024-41033 / ItemTrader.cs:82-108），命中则 1:1 兑换（SkipItemConsumption
   * 语义——本方法自扣 stack）；否则按 ExtractinatorMode（ItemID.cs:1104）走转化表
   * （:41034-41044 → ExtractinatorHelper.RollExtractinatorDrop，全表在
   * world/Extractinator.ts）。原版消耗走通用 consumable 扣减（Player.cs:42602），此处等价
   * 为手持格扣 1。642 使用间隔 ×0.33（:41018-41020）。
   * @param viaUse true = 左键使用链（updateUse，受 useTime 冷却）；false = 右键交互
   * @returns 是否成功转化/兑换（false 时调用方应回落到普通放置/使用）
   */

```


---

## 🤖 Assistant · 2026-08-13T01:31:24.588Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
The right-click chain is quite complete. Now, vanilla right-click priority: `ItemCheck_ManageRightClickFeatures` (Player.cs:31068) and `ItemCheck` right-click handling via `Player.cs:31707+` (smartInteract). The vanilla chain order matters. Let me check vanilla's right-click dispatch order briefly to compare priority. The key question from the checklist: "门/宝箱/雕像/床/旗帜的右键优先级,同格多物件冲突时".

Vanilla: Player.cs ItemCheck → controlUseTile? Actually right-click is `PlayerInput` → `Main.mouseRight` → `Player.ItemCheck_ManageRightClickFeatures` (which handles shield raise, etc.) and the tile interaction is in `ItemCheck` → `SmartInteract` and then `ItemCheck_RightClick`? Let me look at how vanilla dispatches: `Player.cs:31650`? There's `ItemCheck` calling `ItemCheck_ManageRightClickFeatures` and the tile right-click is processed in `Player.TryInteractingWith...`? Let me grep for the smartInteract / "controlUseTile".

Actually, in vanilla the right-click tile interaction flows through `Player.ItemCheck()`:
```
if (controlUseTile && releaseUseTile) { ... }
```
Hmm, there's `SmartInteract` system: Main.SmartInteractX/Y computed each frame; then `ItemCheck` has a big if-chain in order. The order in Player.ItemCheck (1.4.4) around line 31707:

Let me grep for the ordering of those right-click branches in vanilla Player.cs to compare: search for "31707" area. Actually I already have enough for the report: the implementation order is furniture → extractinator → banks → doors → chests → sign → tombstone → life crystal → bed → sundial → workbench buffs → switches → herbs → music box → ... → lihzahrd altar → eternia → pylon.

One notable thing: **doors are checked AFTER chests** in implementation (chest branch before door branch: `if (type === T.DOOR_CLOSED)... else if (type === T.CHEST...)`). In vanilla, since a door tile and a chest tile can't occupy the same tile (both are tiles — one type per tile), same-tile conflicts are impossible at the tile level. The conflict arises for multi-tile objects (chest is 2×2): clicking the chest's top row vs a torch on top. Vanilla SmartInteract (Main.cs SmartInteract) handles the hover selection. This repo uses `findChest(tx,ty) ?? findChestNear(tx,ty)` (3×3 tolerance) which is an approximation of SmartInteract.

Also, **statues right-click**: implementation has no statue right-click branch (vanilla: right-clicking a statue does nothing special; statues are interacted via wire. Actually "雕像" in the checklist — vanilla right-click on statue does nothing; it's hit with hammer? No. Statues are just wire-triggered). So no statue right-click is correct-ish. Let me not claim.

**旗帜 (banner)**: right-click on banner — vanilla does nothing (banners are decorative buff-providing). Implementation has no branch = aligned (no-op).

Now — vanilla right-click priority for doors vs chest: if door tile type is door, it can't be chest. Fine.

What about **torch in same tile as a chest's anchor**? Not possible.

The real "same-tile conflict" in vanilla is handled by `Main.SmartInteract` (hover) and `Player.ItemCheck`'s sequential branches using `smartInteractX/Y`. Since each tile has one type, conflicts are resolved by which tile the smart interact picks. The implementation's 3×3 chest tolerance could grab a chest when clicking a nearby door — minor.

Now let me check:
1. Cursor style change when smart cursor on (VUI.smartCursorOn, Renderer.ts).
2. Pick block middle-click (中键选取).
3. Multi-tile placement aid (long wall continuous) — smart cursor BlocksLines covers this when smart cursor is ON. But without smart cursor, vanilla has no auto-continuous placement either. OK.
4. tileTargetX/tileTargetY smart cursor override — check Game.ts:4032-4040 (already seen: `if (this.smartCursor.showing) { tx = this.smartCursor.x; ty = this.smartCursor.y; }` — matches Main.cs tileTarget override).
5. Smart cursor key: vanilla default binding is LeftCtrl toggle? In vanilla, "Smart Cursor" key = LeftControl by default and can be toggle or hold (settings). Implementation: ControlLeft/ControlRight with toggleMode default true. ✅. Also vanilla supports gamepad.

Let me check VUI cursor rendering and middle click.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:24.920Z · glm-x-preview-260804

```
右键链已梳理。现查光标样式切换(VUI/Renderer)与中键选取方块。
```


---

## 🤖 Assistant · 2026-08-13T01:31:25.743Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"smartCursorOn\\|SmartCursor\\|middleClick\\|button === 1\\|MouseButton\\|pickBlock\\|middle\" ~/Project/GLM/SandboxWorld/game/src/vui/VUI.ts ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts ~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts 2>/dev/null | head -25",
 "description": "Check cursor rendering and middle click"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:25.763Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/vui/VUI.ts:177:  static smartCursorOn = false;
~/Project/GLM/SandboxWorld/game/src/vui/VUI.ts:182:    const tex = UITextures.get(VUI.smartCursorOn ? 'UI_Cursor_1' : 'UI_Cursor_0');
~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts:263:          Lang.text('Mods.SandboxWorld.Settings.SmartCursorMode'),
~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts:266:            ? 'Mods.SandboxWorld.Settings.SmartCursorToggle'
~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts:267:            : 'Mods.SandboxWorld.Settings.SmartCursorHold'),
~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts:280:      scHint.textContent = Lang.text('Mods.SandboxWorld.Settings.SmartCursorHint');
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:20:import { SMART_CURSOR_DIRECTION_LOCKS } from '../player/SmartCursor';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1031:    // 7b. 智能光标黄框（Main.cs:46016-46066 DrawSmartCursor）：光照合成之后画，
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1034:      this.drawSmartCursor(ctx, cam, hover, viewW, z,
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1161:    ctx.textBaseline = 'middle';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:3829:   * 智能光标黄框（Main.cs:46016-46066 DrawSmartCursor 1:1）：
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:3832:   * （SmartCursorArrow 贴图 8 帧；此处先用 canvas 三角形，沿方向 16/20px + 0.9s 正弦浮动）。
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:3906:  private drawSmartCursor(
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:3947:        ctx.rotate((idx * Math.PI) / 4); // SmartCursorDirectionLocks 上起顺时针（Main.cs:66188）

```


---

## 🤖 Assistant · 2026-08-13T01:31:29.733Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Cursor style: VUI.ts:182 — `smartCursorOn ? 'UI_Cursor_1' : 'UI_Cursor_0'`. Let me verify the vanilla cursor behavior: in vanilla, when smart cursor is active, the mouse cursor changes to a different cursor texture (Smart Cursor mode shows cursor_2? Let me check Main.cs for cursor switching). In vanilla `Main.LoadCursorTextures` and the cursor index logic: `Main.cursorMode`? There's `SmartCursorHelper` + Main.cs: `if (SmartCursorShowing) Main.cursorOverride = ...`? Let me grep Main.cs for cursorOverride / Cursor_1.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:30.386Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"cursorOverride\\|SmartCursorShowing\\|cursorTex\\[|Mouse\" Main.cs | grep -i \"cursor\" | head -20",
 "description": "Find vanilla cursor override logic"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:30.409Z

**📎 ToolResult**

```
2080:	public static bool SmartCursorShowing;
2112:	public static int cursorOverride;
39219:			cursorOverride = 2;
44378:		cursorOverride = -1;
44710:		else if (cursorOverride != -1)
44719:			if (cursorOverride == 2)
44726:			switch (cursorOverride)
44746:				spriteBatch.Draw(TextureAssets.Cursors[cursorOverride].Value, new Vector2(mouseX + 1, mouseY + 1), null, color, rotation, vector * TextureAssets.Cursors[cursorOverride].Value.Size(), cursorScale * 1.1f * num3, SpriteEffects.None, 0f);
44750:				spriteBatch.Draw(TextureAssets.Cursors[cursorOverride].Value, new Vector2(mouseX, mouseY), null, white, rotation, vector * TextureAssets.Cursors[cursorOverride].Value.Size(), cursorScale * num3, SpriteEffects.None, 0f);
46018:		if (!SmartCursorShowing || player[myPlayer].dead)
66093:		SmartCursorShowing = false;
66100:		cursorOverride = -1;

```


---

## 🤖 Assistant · 2026-08-13T01:31:32.175Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '39210,39225p' Main.cs; echo \"===44705-44730===\"; sed -n '44705,44730p' Main.cs",
 "description": "Read cursor override = 2 context"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:32.208Z

**📎 ToolResult**

```
			spriteBatch.Draw(itemTexture, bottomRight, rectangle, item.GetAlpha(Microsoft.Xna.Framework.Color.White), 0f, rectangle.Size(), num, SpriteEffects.None, 0f);
			if (item.color != default(Microsoft.Xna.Framework.Color))
			{
				spriteBatch.Draw(itemTexture, bottomRight, rectangle, item.GetColor(item.color), 0f, rectangle.Size(), num, SpriteEffects.None, 0f);
			}
			if (!new Microsoft.Xna.Framework.Rectangle((int)bottomRight.X - (int)((float)rectangle.Width * num), (int)bottomRight.Y - (int)((float)rectangle.Height * num), (int)((float)rectangle.Width * num), (int)((float)rectangle.Height * num)).Contains(new Microsoft.Xna.Framework.Point(mouseX, mouseY)))
			{
				return;
			}
			cursorOverride = 2;
			if (mouseLeftRelease && mouseLeft)
			{
				if (!drawingPlayerChat)
				{
					OpenPlayerChat();
				}
===44705-44730===
			mouseY = (int)housingScreenPosition.Y;
			DrawCursor(DrawThickCursor());
			mouseX = num;
			mouseY = num2;
		}
		else if (cursorOverride != -1)
		{
			Microsoft.Xna.Framework.Color color = new Microsoft.Xna.Framework.Color((int)((float)(int)cursorColor.R * 0.2f), (int)((float)(int)cursorColor.G * 0.2f), (int)((float)(int)cursorColor.B * 0.2f), (int)((float)(int)cursorColor.A * 0.5f));
			Microsoft.Xna.Framework.Color white = cursorColor;
			bool flag = true;
			bool flag2 = true;
			float rotation = 0f;
			Vector2 vector = default(Vector2);
			float num3 = 1f;
			if (cursorOverride == 2)
			{
				flag = false;
				white = Microsoft.Xna.Framework.Color.White;
				num3 = 0.7f;
				vector = new Vector2(0.1f);
			}
			switch (cursorOverride)
			{
			case 2:
				flag = false;
				white = Microsoft.Xna.Framework.Color.White;

```


---

## 🤖 Assistant · 2026-08-13T01:31:34.859Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
cursorOverride=2 is for chat cursor. Let me search for where smart cursor changes the cursor. In vanilla, when smart cursor is enabled, the mouse cursor switches to the "smart" cursor (Cursors[5]? there's Cursor_5 etc.). Let me grep for "Cursors[" usage with smart.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:35.558Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"SmartCursorIsUsed\\|myPlayer].smartCursor\\|smartCursor\\b\" Main.cs | head -20",
 "description": "Find smart cursor cursor-swap in Main.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:35.578Z

**📎 ToolResult**

```
2962:	public static bool SmartCursorIsUsed => SmartCursorWanted;
37210:		bool flag = !SmartCursorIsUsed && !PlayerInput.UsingGamepad;
37268:		if (!SmartCursorIsUsed && !PlayerInput.UsingGamepad)
37285:		bool flag = !SmartCursorIsUsed && !PlayerInput.UsingGamepad;
37347:		if (!SmartCursorIsUsed && !PlayerInput.UsingGamepad)
37378:		bool flag2 = !SmartCursorIsUsed && !PlayerInput.UsingGamepad;
37406:		if (!SmartCursorIsUsed && !PlayerInput.UsingGamepad)
44753:		else if (SmartCursorIsUsed)
45637:		bool flag = MouseShowBuildingGrid && !SmartCursorIsUsed;
45638:		if (PlayerInput.UsingGamepad && !SmartCursorIsUsed)
62242:			if (PlayerInput.GamepadThumbstickRight.Length() == 0f && SmartCursorIsUsed)

```


---

## 🤖 Assistant · 2026-08-13T01:31:37.271Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '44753,44775p' Main.cs",
 "description": "Read smart cursor cursor draw branch"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:37.294Z

**📎 ToolResult**

```
		else if (SmartCursorIsUsed)
		{
			DrawCursor(DrawThickCursor(smart: true), smart: true);
		}
		else
		{
			DrawCursor(DrawThickCursor());
		}
	}

	private static void DrawInterface_35_YouDied()
	{
		if (!player[myPlayer].dead)
		{
			return;
		}
		float num = -60f;
		string value = Lang.inter[38].Value;
		if (LocalPlayer.spectating < 0)
		{
			DynamicSpriteFontExtensionMethods.DrawString(spriteBatch, FontAssets.DeathText.Value, value, new Vector2((float)(screenWidth / 2) - FontAssets.DeathText.Value.MeasureString(value).X / 2f, (float)(screenHeight / 2) + num), player[myPlayer].GetDeathAlpha(Microsoft.Xna.Framework.Color.Transparent), 0f, default(Vector2), 1f, SpriteEffects.None, 0f, (Vector2[])null, (Microsoft.Xna.Framework.Color[])null);
			if (LocalPlayer.lostCoins > 0)
			{

```


---

## 🤖 Assistant · 2026-08-13T01:31:41.737Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla: `SmartCursorIsUsed` (i.e., wanted/on) → `DrawCursor(DrawThickCursor(smart: true), smart: true)` — the smart cursor texture variant. Implementation VUI.ts:182 uses `smartCursorOn` (which is set from `sc.showing`, i.e., SmartCursorShowing) not the "wanted" state. Vanilla uses `SmartCursorIsUsed` = SmartCursorWanted (the toggle state, not the showing state). Small nuance: vanilla swaps the cursor whenever smart cursor mode is ON (even when the yellow box isn't visible); implementation swaps only when showing (a target was found). Minor deviation — ⚠️/🔀 worth noting as low priority. Actually let me double check what UI_Cursor_1 vs vanilla: vanilla has Cursors[0..7]? The smart cursor in vanilla is cursor index... DrawCursor(smart:true) uses TextureAssets.Cursors[?]. Let me check DrawCursor signature quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:31:42.385Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"static void DrawCursor\\|DrawThickCursor(bool\" Main.cs | head -4; awk '/private static void DrawCursor\\(/,/^\t}/' Main.cs | head -20",
 "description": "Read DrawCursor smart variant"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:31:58.899Z

**📎 ToolResult**

```
47360:	public static void DrawCursor(Vector2 bonus, bool smart = false)
47442:	public static Vector2 DrawThickCursor(bool smart = false)

```


---

## 🤖 Assistant · 2026-08-13T01:32:00.510Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '47360,47400p' Main.cs",
 "description": "Read DrawCursor body"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:00.557Z

**📎 ToolResult**

```
	public static void DrawCursor(Vector2 bonus, bool smart = false)
	{
		if (gameMenu && alreadyGrabbingSunOrMoon)
		{
			return;
		}
		if (player[myPlayer].dead || player[myPlayer].mouseInterface || IsCameraTrackingObject)
		{
			ClearSmartInteract();
			TileInteractionLX = (TileInteractionHX = (TileInteractionLY = (TileInteractionHY = -1)));
		}
		Microsoft.Xna.Framework.Color color = cursorColor;
		if (!gameMenu && LocalPlayer.hasRainbowCursor)
		{
			color = hslToRgb(GlobalTimeWrappedHourly * 0.25f % 1f, 1f, 0.5f);
		}
		bool flag = UILinkPointNavigator.Available && !PlayerInput.InBuildingMode;
		if (PlayerInput.SettingsForUI.ShowGamepadCursor)
		{
			if ((player[myPlayer].dead && !player[myPlayer].ghost && !gameMenu) || player[myPlayer].spectating >= 0 || PlayerInput.InvisibleGamepadInMenus)
			{
				return;
			}
			Vector2 t = new Vector2(mouseX, mouseY);
			Vector2 t2 = Vector2.Zero;
			bool flag2 = smart;
			if (flag2)
			{
				PlayerInput.smartSelectPointer.UpdateCenter(ScreenSize.ToVector2() / 2f);
				t2 = PlayerInput.smartSelectPointer.GetPointerPosition();
				if (Vector2.Distance(t2, t) < 1f)
				{
					flag2 = false;
				}
				else
				{
					Utils.Swap(ref t, ref t2);
				}
			}
			float num = 1f;
			if (flag2)

```


---

## 🤖 Assistant · 2026-08-13T01:32:04.997Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK — vanilla smart cursor: when `SmartCursorIsUsed`, the cursor is drawn with the "smart" variant (the yellow/gold thick cursor). The exact texture is Cursors[4]/[5] family. Enough: the implementation swaps UI_Cursor_1 when showing. The nuance (wanted vs showing) is a real but minor deviation.

Now let me check the middle-click pick block. Input.ts has no middle button handling (`e.button === 1` missing — only 0 and 2). So middle-click pick block ❌ not implemented. Vanilla: middle click = "smart pick" (PickBlock)? Actually in vanilla, middle-click on a block while holding... no. Vanilla middle click: in inventory UI, middle-click favorites an item. In-world middle-click does nothing by default? Hmm. Actually, there's no "pick block" middle-click in vanilla Terraria (that's Minecraft). Let me verify with the Controls wiki page.

Let me check the Controls.md wiki page for the key list to cross-check H/J/B/quick mount/smart cursor.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:32:05.224Z · glm-x-preview-260804

```
查 wiki Controls 页核对 H/J/B/智能光标/中键绑定。
```


---

## 🤖 Assistant · 2026-08-13T01:32:05.826Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && grep -n \"Quick Heal\\|Quick Mana\\|Quick Buff\\|Quick Mount\\|Smart Cursor\\|Middle\\|Quick\" Controls.md | head -20",
 "description": "Check Controls wiki for quick keys"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:05.870Z

**📎 ToolResult**

```
ugrep: warning: Controls.md: No such file or directory

```


---

## 🤖 Assistant · 2026-08-13T01:32:08.214Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && ls | grep -i \"^Controls\\|^Smart_cursor\\|^Placement_range\\|^Tool_range\\|^Smart_select\" ",
 "description": "Find controls and smart cursor wiki pages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:08.317Z

**📎 ToolResult**

```
Placement_range.md
Smart_Cursor_Mode__Hold.md
Smart_Cursor_Mode__Toggle.md
Smart_Cursor.md
Tool_range.md

```


---

## 🤖 Assistant · 2026-08-13T01:32:10.341Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && grep -rn \"Quick Heal\\|Quick Mana\\|Quick Buff\\|Quick Mount\" *.md 2>/dev/null | grep -v \"Legacy\\|Category\" | head -8; echo \"===Tool_range===\"; head -40 Tool_range.md",
 "description": "Grep wiki for quick keys and tool range"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:11.165Z

**📎 ToolResult**

```
1.2.4.md:111:  * Changed the Quick Heal to use the best fit healing item instead of the first.
1.3.5.md:86:  * Using [Quick Heal](Quick_Heal.md "Quick Heal") to consume restoration potions now properly inflicts mana sickness
1.4.0.1.md:1456:  * Fixed an issue where you could not use Quick Buff while riding the Drill Containment Unit.
1.4.4.3.md:39:  * Fixed [Bottled Honey](Bottled_Honey.md "Bottled Honey") not giving the [Honey](Honey_\(buff\) "Honey \(buff\)") buff when used with Quick Heal
1.4.4.md:94:    * Using Quick Buff, Food, and Potions from its Storage. This includes Mana Flower Mana Potions. Wormhole Potions will also work automatically from within it.
1.4.5.0.md:1451:  * Fixed a bug where [`Quick Buff`](Game_controls.md "Game controls") could consume non-consumable items if used when you have no [buff](Buff "Buff") items in your inventory.
Bottled_Honey.md:92:  * Using the [`Quick Buff`](Game_controls.md "Game controls") hotkey will consume the item, granting the player the [Honey](Honey_\(buff\) "Honey \(buff\)") buff without restoring health or causing [Potion Sickness](Potion_Sickness.md "Potion Sickness"). This occurs only when the player is not afflicted with Potion Sickness.
Console_version_history.md:2276:  * Replaced “Drop” function with “Quick Buff” in the controller map
===Tool_range===
# Tool range

> 原页面: `Tool_range`

[Tool range](./Placement#Placement_range_and_tool_range)
  *[1 required]: Journey Mode
  *[Qty.]: Quantity
  *[100%]: Master Mode
  *[DPS]: Damage per detik
  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
  *[300]: Expert Mode
  *[400]: Master Mode
  *[160]: Expert Mode
  *[240]: Master Mode
  *[3 required]: Journey Mode
  *[#]: Number of summons, i.e. times that the Stardust Dragon Staff was used
  *[Max.  
enemies]: Maximum number of enemies Abigail can damage at once
  *[HM]: Hardmode
  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
  *[8]: Expert Mode
  *[10]: Expert Mode
  *[120]: Master Mode
  *[150]: Expert Mode
  *[13]: Chế độ Master
  *[195]: Master Mode
  *[Verify]: Define loaded.
  *[50 required]: Journey Mode
  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
  *[100 required]: Journey Mode
  *[cần có 1]: Chế độ Journey
  *[25 required]: Journey Mode
  *[cần có 25]: Chế độ Journey
  *[400 required]: Journey Mode
  *[membutuhkan 100]: Mode Journey
  *[cần có 100]: Chế độ Journey
  *[Slg.]: Số lượng
  *[1.99%]: Expert Mode

```


---

## 🤖 Assistant · 2026-08-13T01:32:13.303Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && grep -n \"Quick Heal\\|Quick Mana\\|Quick Buff\\|Quick Mount\\|Smart Cursor\" Game_controls.md | head -15; echo \"===range section===\"; grep -n -B2 -A12 \"Default\" Placement_range.md | head -50",
 "description": "Read game controls and placement range wiki"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:13.364Z

**📎 ToolResult**

```
57:[Smart Cursor](Smart_Cursor.md "Smart Cursor") | `Smart Cursor` | Left Ctrl  | Press R3  | Press  | Press  | Press  | Press/Hold  (based on Smart Cursor Mode setting)  | Toggles the Smart Cursor. When on, it will automatically target tiles depending on the tool selected, to semi-automate tasks such as tunneling and building.   
58:Quick [Mount](Mount "Mount") | `Quick Mount` | R  |  |  |  |  |  | Mount or dismount the mount located in the equipment slot.   
59:Quick Heal  | `Quick Heal` | H  | Unbound  |  \+  right  |  \+  right  |  |  \+  right  | Consumes the best healing item from inventory. (If all the healing items could not restore [health](Health.md "Health") to maximum health, the item with the largest amount of health restoration will be the best. If there are one or more items that can restore health to maximum health, the item with the least amount of spill health restoration will be the best. If [Restoration Potion](Restoration_Potion.md "Restoration Potion") exists and the number of health lost is greater than 90 and less than 120, the spill health restoration of Restoration Potion is considered 0.[1])   
60:Quick Mana  | `Quick Mana` | J  | Unbound  |  \+  left  |  \+  left  |  |  \+  left  | Consumes the first [mana](Mana.md "Mana") restoration item in inventory (starting from the top-left).   
61:Quick Buff  | `Quick Buff` | B  | Unbound  |  \+  down  |  \+  down  |  |  \+  down  | 
206:Toggle [Smart Cursor](Smart_Cursor.md "Smart Cursor") |  |  | Makes block placement easier. See [Smart Cursor](Smart_Cursor.md "Smart Cursor") for more information.   
===range section===

```


---

## 🤖 Assistant · 2026-08-13T01:32:20.257Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wiki confirms: H=Quick Heal, J=Quick Mana, B=Quick Buff, R=Quick Mount, Left Ctrl=Smart Cursor. And in the implementation, **R is bound to the wire-tool mode cycle** (Game.ts:1394) — which conflicts with vanilla's Quick Mount (R). Note: vanilla R = Quick Mount; the R for "wrench mode cycling" in vanilla is... Actually in vanilla, pressing R while holding a multicolor wrench cycles modes? No — vanilla multicolor wrench mode is changed via the wire UI (T key toggles the wire UI? No...). In vanilla, the wrench/cutter modes are toggled with the **"R" key while holding the wrench**? Let me check PlayerInput: there's `controlRight`... Actually vanilla: "Pressing R with a Multicolor Wrench" — hmm, no. In vanilla 1.4.4, the multicolor wrench mode selection is done in the wiring UI which is toggled by... the wire visibility toggle. Hmm.

Actually — from Terraria: "The Multicolor Wrench's mode can be toggled by right-clicking while... " no. Let me not over-claim. The key fact: vanilla R = Quick Mount (mount item in equip slot). Implementation R = wire mode cycle (no quick mount implemented). I'll note Quick Mount missing and R repurposed.

Also the wiki says Quick Mount = R. Since mounts are partially implemented (minecart), quick mount for mount items isn't there.

Now the Smart_cursor.md page — check the rules for enabling and per-tile behaviors, to complete coverage. Let me read key parts.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:32:20.631Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && grep -v \"^\\*\" Smart_Cursor.md | grep -v \"^$\" | head -70",
 "description": "Read Smart Cursor wiki content"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:24.445Z

**📎 ToolResult**

```
# Smart cursor
> 原页面: `Smart_cursor`
[Smart cursor](./Cursor_modes#Smart_Cursor)
  *[1 required]: Journey Mode
  *[Qty.]: Quantity
  *[100%]: Master Mode
  *[DPS]: Damage per second
  *[sic]: sīc erat scriptum (Latin: “thus it was written”) – any typographical or other errors in this quote are intentionally reproduced, exactly as they appear in the source.
  *[300]: Master Mode
  *[400]: Expert Mode
  *[160]: Expert Mode
  *[240]: Master Mode
  *[3 required]: Journey Mode
  *[#]: Number
  *[Max.  
enemies]: Maximum number of enemies Abigail can damage at once
  *[HM]: Hardmode
  *[**Click/tap here** to reveal this content. _(there may be a slight delay)_]: This content exists externally. Once you click, there may be a small delay while it is downloaded.
  *[**Klik/tap disini** untuk melihat isi konten. _(mungkin akan sedikit delay)_]: Konten ini tersedia secara eksternal. Ketika di klik, mungkin akan ada sedikit delay ketika melihat isi konten.
  *[**Bấm/Chạm vào đây** để hiển thị nội dung này. _(có thể sẽ bị delay một chút)_]: Nội dung này được lấy từ các nguồn bên ngoài. Khi bấm vào, có thể sẽ bị delay một chút trong khi nó tải.
  *[8]: Expert Mode
  *[10]: Expert Mode
  *[120]: Master Mode
  *[150]: Master Mode
  *[13]: Chế độ Master
  *[195]: Master Mode
  *[Verify]: In-game testing shows otherwise
  *[50 required]: Journey Mode
  *[0.05 mph]: 0.05 miles per hour (as measured by the Stopwatch item) or 0.04 tiles per second
  *[100 required]: Journey Mode
  *[cần có 1]: Chế độ Journey
  *[25 required]: Journey Mode
  *[cần có 25]: Chế độ Journey
  *[400 required]: Journey Mode
  *[membutuhkan 100]: Mode Journey
  *[cần có 100]: Chế độ Journey
  *[Slg.]: Số lượng
  *[1.99%]: Expert Mode
  *[199/10000 (1.99%)]: Expert Mode
  *[membutuhkan 1]: Mode Journey
  *[1,99%]: Expert Mode
  *[1/50 (2%)]: Mode Expert
  *[200 required]: Journey Mode
  *[15 mph]: 15 miles per hour (as measured by the Stopwatch item) or 11 tiles per second
  *[16 mph]: 16 miles per hour (as measured by the Stopwatch item) or 11.9390625 tiles per second
  *[20 required]: Journey Mode
  *[180]: Master Mode
  *[270]: Master Mode
  *[5–9 seconds]: Master Mode
  *[5–9]: Expert Mode
  *[15 required]: Journey Mode
  *[Critter]: May spawn a Worm, Gold Worm, or Maggot when destroyed, as described at the top of this article
  *[Power]: Bait power
  *[5 required]: Journey Mode
  *[cần có {{{research}}}]: Chế độ Journey
  *[31 mph]: 31 miles per hour (as measured by the Stopwatch item) or 22.5 tiles per second
  *[34 mph]: 34 miles per hour (as measured by the Stopwatch item) or 24.93 tiles per second
  *[30 mph]: 30 miles per hour (as measured by the Stopwatch item) or 22 tiles per second
  *[Expert Mode exclusive]: Expert Mode
  *[402]: Master Mode
  *[523]: Expert Mode
  *[41 mph]: 41 miles per hour (as measured by the Stopwatch item) or 30.07 tiles per second
  *[21 mph]: 21 miles per hour (as measured by the Stopwatch item) or 15.4 tiles per second
  *[800]: Expert Mode
  *[1200]: Master Mode
  *[15]: Expert Mode
  *[17]: Master Mode
  *[O. v. odražení]: Odolnost vůči odražení
  *[1 minute 30 seconds]: Expert Mode
  *[1 minute 52.5 seconds]: Master Mode

```


---

## 🤖 Assistant · 2026-08-13T01:32:27.618Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The wiki page is a redirect to Cursor_modes. Let me check Cursor_modes.md for the smart cursor behavior list.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:32:28.040Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && grep -v \"^\\*\" Cursor_modes.md | grep -v \"^$\" | sed -n '1,60p'",
 "description": "Read Cursor modes wiki page"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:32.433Z

**📎 ToolResult**

```
# Cursor modes
> 原页面: `Cursor_modes`
# Cursor modes
## Auto Select
[](Desktop_version_history.md "Desktop version") [](Console_version.md "Console version") [](Mobile_version.md "Mobile version")
Auto Select will automatically select an item to use, depending on where the cursor is pointed. The item does not need to be in the hot bar. By default, Auto Select is activated by pressing [`⇧ Left Shift`](Game_controls.md "Game controls") on PC, **R3** on PS3/PS4, or pressing down the **right thumbstick** on Xbox 360/Xbox 1. 
Target  | Item Selected   
---|---  
[Blocks](Blocks.md "Blocks") and most [Furniture](Furniture.md "Furniture") | [Pickaxe](Pickaxe "Pickaxe")  
[Tree](Tree "Tree"), [Giant Glowing Mushroom](Giant_Glowing_Mushroom.md "Giant Glowing Mushroom"), or [Cactus](Cactus.md "Cactus") | [Axe](Axe "Axe")  
[Altar](Altar "Altar"), [Shadow Orb](Shadow_Orb.md "Shadow Orb") or [Crimson Heart](Crimson_Heart.md "Crimson Heart") | [Hammer](Hammer "Hammer")  
[Extractinator](Extractinator.md "Extractinator") | [Silt](Silt "Silt") or [Slush](Slush "Slush")  
[Cannon](Cannon.md "Cannon") | [Cannonball](Cannonball.md "Cannonball")  
[Bunny Cannon](Bunny_Cannon.md "Bunny Cannon") | [Explosive Bunny](Explosive_Bunny.md "Explosive Bunny")  
When pointing at an empty space or a wall, a light source will be selected based on the following criteria   
Cursor is far from the player | [Glowstick](Glowstick.md "Glowstick"), [Spelunker Glowstick](Spelunker_Glowstick.md "Spelunker Glowstick") or [Flare Gun](Flare_Gun.md "Flare Gun")  
Player and cursor are in [water](Water.md "Water") (or other liquid) | [Cursed Torch](Cursed_Torch.md "Cursed Torch"), [Ichor Torch](Ichor_Torch.md "Ichor Torch"), [Glowstick](Glowstick.md "Glowstick") or [Flare Gun](Flare_Gun.md "Flare Gun")  
Player in [water](Water.md "Water") but cursor is not | [Cursed Torch](Cursed_Torch.md "Cursed Torch") or [Ichor Torch](Ichor_Torch.md "Ichor Torch")  
If none of the above apply | Any [torch](Torch.md "Torch")  
  
A [Flare Gun](Flare_Gun.md "Flare Gun") without [Flares](Flare "Flare") will not be selected. Nor will other light sources such as candles. If more than one item is equally appropriate it will normally select the first one in player's inventory. And if the preferred item is unavailable it will usually fall back to something else. 
## Smart Cursor
Smart Cursor selects a target based on the active item. By default, it is toggled on and off [](Desktop_version_history.md "Desktop version") by pressing [`Left Ctrl`](Game_controls.md "Game controls"), or [](Mobile_version.md "Mobile version") by the  /  Smart Cursor button. On [ Desktop version](Desktop_version_history.md "Desktop version history"), there is also an option in General [Settings](Settings.md "Settings") to make it last only while the key is held down. Smart Cursor mode is indicated by a slightly wider cursor, and the tile targeted is shown with a yellow box. On the [Nintendo 3DS](Legacy%3A3DS_version "Legacy:3DS version")[](Legacy%3A3DS_version "3DS")[ version](Legacy%3A3DS_version "Legacy:3DS version"), Smart Cursor is on by default unless the D-Pad or Touch Screen is used to target an area. 
Active Item  | Behavior   
---|---  
[Pickaxe](Pickaxe "Pickaxe") | Digs a passage wide enough to pass through in the direction indicated by the cursor. A tunnel going diagonally upwards will often have to be widened to go back down. As of [1.3.0.1](1.3.0.1.md "1.3.0.1")**** __(Desktop, Console and Mobile versions) , a vertical tunnel will have a width of 2 tiles, this is reduced from 3 tiles in previous versions.   
[Axe](Axe "Axe") | Chops the base of the tree nearest the cursor. It will target branches when the base is out of range. An item that functions like an axe/pickaxe will target trees first, then blocks. This can be easily seen with the [Laser Drill](Laser_Drill.md "Laser Drill")**** __(Desktop, Console and Mobile versions).   
[Hammer](Hammer "Hammer") | Removes the wall nearest the cursor.   
[Block](Block "Block") | Places a block at the nearest legal space to the cursor. If the space under the cursor already contains a block or other object, it will do nothing. However if the cursor is over an NPC or player, it will encase them in multiple layers. This is currently the only way to automatically fill a large area with blocks. On the [ Mobile version](Mobile_version.md "Mobile version"), this is quite unreliable.   
[Wall](Wall "Wall") | Places a wall at the nearest legal space to the cursor. Unlike other items, walls will only be placed by Smart Cursor within line of sight of the player. This makes it easy to fill a room without the walls "spilling" out.   
[Platform](Platform "Platform") | Adds to existing platforms (in any direction, including vertical).   
[Minecart Track](Minecart_Track.md "Minecart Track") | Extends existing tracks horizontally or diagonally.   
[Wrench](Wrench "Wrench") | Extends existing wires of the same color.   
[Wire Cutter](Wire_Cutter.md "Wire Cutter") | Removes the wire nearest the cursor.   
[Acorn](Acorn.md "Acorn") | Places an acorn on top of grass if two blocks beside it are free. Accounts for optimal range, so that saplings have at least three empty tiles between them.   
[Paint Roller](Paint_Roller.md "Paint Roller") | Using the Paint Roller on one spot (holding it without moving the cursor) will make the cursor grow in a circle from the nearest wall tile, painting every wall including ones behind furniture and platforms but ignoring walls that are behind solid blocks.   
  
Using Smart Cursor with a multi-function tool, like [Drax](Drax.md "Drax") or a [Hamaxe](Hamaxe "Hamaxe"), may have unexpected results. These tools will behave as an axe by default, meaning they always target a tree if one is in range. 
Smart Cursor can backfire unexpectedly, especially if the player has not realized it is active. For example, when extending platforms, if the player's aim is off, platforms can be built off in unexpected directions. Use of the [ruler function](Toggles#Ruler "Toggles") can help with this. Similarly, when digging near lava (or other liquids), the Smart Cursor can blindly mine blocks supporting the liquid. 
[](Desktop_version_history.md "Desktop version") Smart Cursor can be re-enabled to be used for common blocks (as in [1.2](1.2.md "1.2")**** __(Old-gen console and 3DS versions)) by editing Terraria's [config.json](Config.json "Config.json") file manually. See [config.json](Config.json#Hidden_settings "Config.json") to know how to do it. 
## Special cursors
[](Desktop_version_history.md "Desktop version")
The cursor will change accordingly when specific hotkey is pressed. Most of the special sprites are related with [inventory](Inventory.md "Inventory") management functions. 
Function | Default key | Description   
---|---|---  
Favorite  |  | [`Alt`](Game_controls.md "Game controls") | [Favorite](Favorite.md "Favorite")/unfavorite an item.   
Item tag  |  | [`Alt`](Game_controls.md "Game controls") | Insert an [item tag](Chat#Item "Chat") in chat.   
Loot  
Deposit  |   
| [`⇧ Left Shift`](Game_controls.md "Game controls") | Quick transfering items between opened [storage items](Storage_items.md "Storage items") and main inventory.   
Sell  |  | [`⇧ Left Shift`](Game_controls.md "Game controls") | Quick selling items when an [NPC](NPC "NPC") vendor's shop is opened.   
Unequip  |  | [`⇧ Left Shift`](Game_controls.md "Game controls") | Quick moving equipped items back to main inventory.   
Trash  |  | [`Left Ctrl`](Game_controls.md "Game controls")[a] | Quick moving items from main inventory to [trash slot](Trash_slot.md "Trash slot").   
Camera Mode  |   
| [`F4`](Game_controls.md "Game controls") | Cursors in [Camera Mode](Camera_Mode.md "Camera Mode")'s "Pin Frame" selection.   
  
## Footnotes
  1. ↑ Can be changed to [`⇧ Left Shift`](Game_controls.md "Game controls") in [Settings](Settings.md "Settings") at main menu.
View or edit this template
Game mechanics

```


---

## 🤖 Assistant · 2026-08-13T01:32:35.402Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wiki confirms smart cursor behaviors — implementation's strategy chain covers all of these (pickaxe/axe/hammer/block/wall/platform/track/wrench/cutter/acorn). Paint roller/brush/scraper are no-ops (paint system missing) — noted in code comments.

Now let me verify the smart cursor keyboard state machine vs vanilla Player.TryToToggleSmartCursor (Player.cs:28344-28374), and check whether the implementation's `updateWanted` uses the right semantics. Also check Main.cs:2074-2084. Let me read vanilla TryToToggleSmartCursor.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:32:35.947Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '28344,28380p' Player.cs; echo \"===Main 2074-2090===\"; sed -n '2074,2090p' Main.cs",
 "description": "Read vanilla smart cursor toggle state machine"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:36.008Z

**📎 ToolResult**

```
	private void TryToToggleSmartCursor(ref bool smartCursorWanted)
	{
		if (Main.cSmartCursorModeIsToggleAndNotHold)
		{
			if (controlSmart && releaseSmart)
			{
				SoundEngine.PlaySound(12);
				smartCursorWanted = !smartCursorWanted;
			}
			return;
		}
		if (controlSmart && releaseSmart)
		{
			SoundEngine.PlaySound(12);
		}
		if (SmartCursorSettings.SmartCursorHoldCanReleaseMidUse)
		{
			smartCursorWanted = controlSmart;
		}
		else if (smartCursorWanted)
		{
			if (!controlSmart && !controlUseItem)
			{
				smartCursorWanted = false;
			}
		}
		else
		{
			smartCursorWanted = controlSmart;
		}
	}

	private void TryToShimmerUnstuck()
	{
		timeShimmering = Utils.Clamp(timeShimmering + (shimmering ? 1 : (-10)), 0, 7200);
		bool flag = timeShimmering >= 3600;
		if (LocalInputCache.PressingAnyInput && timeShimmering >= 1200)
===Main 2074-2090===
	public static bool cSmartCursorModeIsToggleAndNotHold;

	public static bool SmartCursorWanted_Mouse;

	public static bool SmartCursorWanted_GamePad;

	public static bool SmartCursorShowing;

	public static int SmartCursorX;

	public static int SmartCursorY;

	public static bool SmartInteractShowingGenuine;

	public static bool SmartInteractShowingFake;

	public static int SmartInteractX;

```


---

## 🤖 Assistant · 2026-08-13T01:32:39.003Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
The implementation's `updateWanted` (SmartCursor.ts:402-417) matches vanilla TryToToggleSmartCursor 1:1, including the sound on toggle edge. 

Now let me verify the smart cursor lookup reach computation once more. SmartCursor.ts:441 uses `tileRegion(env.actor, env.tileBoost, st)` where tileRegion at :1679 does `x = Math.min(20, 5) + tb; y = Math.min(20, 3) + tb`. Vanilla SmartCursorLookup:

```csharp
Rectangle tileRegion = TileReachCheckSettings.Simple.GetTileRegion(player, TB);
```

Let me check the vanilla SmartCursorHelper.cs SmartCursorLookup lines 94-103 to see how TB is computed.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:32:39.376Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/GameContent\" && sed -n '61,120p' SmartCursorHelper.cs",
 "description": "Read vanilla SmartCursorLookup"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:39.416Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
(eval):cd:1: no such file or directory: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/GameContent

```


---

## 🤖 Assistant · 2026-08-13T01:32:41.329Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find \"~/Project/GLM/SandboxWorld/Terarria1456\" -name \"SmartCursorHelper.cs\" 2>/dev/null",
 "description": "Locate SmartCursorHelper.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:41.382Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent/SmartCursorHelper.cs

```


---

## 🤖 Assistant · 2026-08-13T01:32:43.452Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent\" && sed -n '61,170p' SmartCursorHelper.cs",
 "description": "Read vanilla SmartCursorLookup dispatch"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:43.503Z

**📎 ToolResult**

```
	public static void SmartCursorLookup(Player player)
	{
		Main.SmartCursorShowing = false;
		if (!player.controlUseItem || !Main.SmartCursorIsUsed)
		{
			_lockedDesiredDirection = null;
			_lockedContinuityCoords = null;
		}
		if (!Main.SmartCursorIsUsed)
		{
			return;
		}
		SmartCursorUsageInfo smartCursorUsageInfo = new SmartCursorUsageInfo
		{
			player = player,
			item = player.inventory[player.selectedItem],
			mouse = Main.MouseWorld,
			position = player.position,
			Center = player.Center
		};
		_ = player.gravDir;
		int tileTargetX = Player.tileTargetX;
		int tileTargetY = Player.tileTargetY;
		_ = Player.tileRangeX;
		_ = Player.tileRangeY;
		smartCursorUsageInfo.screenTargetX = Utils.Clamp(tileTargetX, 10, Main.maxTilesX - 10);
		smartCursorUsageInfo.screenTargetY = Utils.Clamp(tileTargetY, 10, Main.maxTilesY - 10);
		if (Main.tile[smartCursorUsageInfo.screenTargetX, smartCursorUsageInfo.screenTargetY] == null)
		{
			return;
		}
		bool num = IsHoveringOverAnInteractableTileThatBlocksSmartCursor(smartCursorUsageInfo);
		TryFindingPaintInplayerInventory(smartCursorUsageInfo, out smartCursorUsageInfo.paintLookup, out smartCursorUsageInfo.paintCoatingLookup);
		int num2 = smartCursorUsageInfo.item.tileBoost;
		if (smartCursorUsageInfo.item.createWall > 0 || smartCursorUsageInfo.item.createTile > 0 || smartCursorUsageInfo.item.tileWand > 0)
		{
			num2 += player.blockRange;
		}
		TileReachCheckSettings.Simple.GetTileRegion(player, out smartCursorUsageInfo.reachableStartX, out smartCursorUsageInfo.reachableStartY, out smartCursorUsageInfo.reachableEndX, out smartCursorUsageInfo.reachableEndY, num2);
		smartCursorUsageInfo.reachableStartX = Utils.Clamp(smartCursorUsageInfo.reachableStartX, 10, Main.maxTilesX - 10);
		smartCursorUsageInfo.reachableEndX = Utils.Clamp(smartCursorUsageInfo.reachableEndX, 10, Main.maxTilesX - 10);
		smartCursorUsageInfo.reachableStartY = Utils.Clamp(smartCursorUsageInfo.reachableStartY, 10, Main.maxTilesY - 10);
		smartCursorUsageInfo.reachableEndY = Utils.Clamp(smartCursorUsageInfo.reachableEndY, 10, Main.maxTilesY - 10);
		if (!num || smartCursorUsageInfo.screenTargetX < smartCursorUsageInfo.reachableStartX || smartCursorUsageInfo.screenTargetX > smartCursorUsageInfo.reachableEndX || smartCursorUsageInfo.screenTargetY < smartCursorUsageInfo.reachableStartY || smartCursorUsageInfo.screenTargetY > smartCursorUsageInfo.reachableEndY)
		{
			_grappleTargets.Clear();
			int[] grappling = player.grappling;
			int grapCount = player.grapCount;
			for (int i = 0; i < grapCount; i++)
			{
				Projectile obj = Main.projectile[grappling[i]];
				int x = (int)obj.Center.X / 16;
				int y = (int)obj.Center.Y / 16;
				_grappleTargets.Add(new Point(x, y));
			}
			int fX = -1;
			int fY = -1;
			if (!Player.SmartCursorSettings.SmartAxeAfterPickaxe)
			{
				Step_Axe(smartCursorUsageInfo, ref fX, ref fY);
			}
			Step_ForceCursorToAnyMinableThing(smartCursorUsageInfo, ref fX, ref fY);
			Step_Pickaxe_MineShinies(smartCursorUsageInfo, ref fX, ref fY);
			Step_Pickaxe_MineSolids(player, player.position, player.Center, player.width, player.direction, smartCursorUsageInfo, _grappleTargets, ref fX, ref fY);
			if (Player.SmartCursorSettings.SmartAxeAfterPickaxe)
			{
				Step_Axe(smartCursorUsageInfo, ref fX, ref fY);
			}
			Step_ColoredWrenches(smartCursorUsageInfo, ref fX, ref fY);
			Step_MulticolorWrench(smartCursorUsageInfo, ref fX, ref fY);
			Step_Hammers(smartCursorUsageInfo, ref fX, ref fY);
			Step_ActuationRod(smartCursorUsageInfo, ref fX, ref fY);
			Step_WireCutter(smartCursorUsageInfo, ref fX, ref fY);
			Step_Platforms(smartCursorUsageInfo, ref fX, ref fY);
			Step_MinecartTracks(smartCursorUsageInfo, ref fX, ref fY);
			Step_Walls(smartCursorUsageInfo, ref fX, ref fY);
			Step_PumpkinSeeds(smartCursorUsageInfo, ref fX, ref fY);
			Step_GrassSeeds(smartCursorUsageInfo, ref fX, ref fY);
			Step_Moss(smartCursorUsageInfo, ref fX, ref fY);
			Step_Pigronata(smartCursorUsageInfo, ref fX, ref fY);
			Step_Boulders(smartCursorUsageInfo, ref fX, ref fY);
			Step_Torch(smartCursorUsageInfo, ref fX, ref fY);
			Step_LawnMower(smartCursorUsageInfo, ref fX, ref fY);
			Step_BlocksFilling(smartCursorUsageInfo, ref fX, ref fY);
			Step_BlocksLines(smartCursorUsageInfo, ref fX, ref fY);
			Step_PaintRoller(smartCursorUsageInfo, ref fX, ref fY);
			Step_PaintBrush(smartCursorUsageInfo, ref fX, ref fY);
			Step_PaintScrapper(smartCursorUsageInfo, ref fX, ref fY);
			Step_Acorns(smartCursorUsageInfo, ref fX, ref fY);
			Step_GemCorns(smartCursorUsageInfo, ref fX, ref fY);
			Step_EmptyBuckets(smartCursorUsageInfo, ref fX, ref fY);
			Step_Actuators(smartCursorUsageInfo, ref fX, ref fY);
			Step_AlchemySeeds(smartCursorUsageInfo, ref fX, ref fY);
			Step_PlanterBox(smartCursorUsageInfo, ref fX, ref fY);
			Step_ClayPots(smartCursorUsageInfo, ref fX, ref fY);
			Step_StaffOfRegrowth(smartCursorUsageInfo, ref fX, ref fY);
			if (fX != -1 && fY != -1)
			{
				Main.SmartCursorX = (Player.tileTargetX = fX);
				Main.SmartCursorY = (Player.tileTargetY = fY);
				Main.SmartCursorShowing = true;
			}
			_grappleTargets.Clear();
		}
	}

	private static void TryFindingPaintInplayerInventory(SmartCursorUsageInfo providedInfo, out int paintLookup, out int coatingLookup)
	{
		_ = providedInfo.player.inventory;
		paintLookup = 0;

```


---

## 🤖 Assistant · 2026-08-13T01:32:51.278Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla SmartCursorLookup key facts:
1. TB = `item.tileBoost + (createWall>0 || createTile>0 || tileWand>0 ? player.blockRange : 0)` — the implementation matches this (SmartCursor.ts:3816-3820 comment says exactly this). But: the implementation's tb value is `(tileRange?3:0) + (Builder?1:0)` — it's missing `item.tileBoost` (wrenches have tileBoost 20!). Hmm wait, for smart cursor the reach region matters. For wrenches (item.tileBoost=20), vanilla TB = 20 + blockRange. Implementation: tb = (tileRange?3:0)+(Builder?1:0) → 0 for wrenches! So the smart cursor wrench reach region is 20 tiles short. BUT the actual placement (useWireTool at Game.ts:5818) uses inTileRange(tx,ty,20) ✅. So the smart cursor's *target search region* for wrenches is smaller than the actual usable range → smart cursor won't propose targets beyond 5/3 even though placement works at 20. ⚠️ deviation.

Also vanilla TB includes blockRange for placement items — implementation uses Builder+1 which maps to blockRange... but blockRange also includes Toolbelt. So smart cursor region misses Toolbelt. Same root cause as #1.

2. `_grappleTargets` from grappling hooks — implementation acknowledges grappleTargets = [] with comment (hooks not implemented). Fine.

3. Note vanilla also sets `Player.tileTargetX = fX` — implementation overrides tx/ty in Game.ts:4034-4036 ✅.

Now the remaining checks:
- Multi-tile placement aid (long wall continuous placement) — that's BlocksLines under smart cursor ✅. Without smart cursor, vanilla requires manual per-tile. ✅
- Doors: toggleDoor. Door placement is via tryPlace with def.w/h? Doors are 1×3. Let me quickly check door placement anchor. Memory note says "PlaceTile 放门要 j-2" — vanilla places door at j-2 (mouse tile = bottom of door). Implementation tryPlace uses top-left. Let me check if there's a door-specific offset. Let me grep door place.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:32:51.465Z · glm-x-preview-260804

```
核对门放置锚点与斜坡上放置。
```


---

## 🤖 Assistant · 2026-08-13T01:32:52.430Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"DOOR\\|door\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | grep -in \"place\\|j-2\\|ty - 2\\|ty-2\" | head -10; echo \"---door place in tryPlace?---\"; awk 'NR>=6120 && NR<=6187' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | grep -n \"door\\|Door\" | head",
 "description": "Check door placement anchor offset"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:56.233Z

**📎 ToolResult**

```
---door place in tryPlace?---

```


---

## 🤖 Assistant · 2026-08-13T01:32:59.547Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"DOOR_CLOSED\\b\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -3; grep -rn \"door\" ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts | head -5",
 "description": "Find door tile def and placement"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:32:59.699Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1964:          if (st.type[st.idx(x, y)] === T.DOOR_CLOSED) { doorX = x; doorY = y; break; }
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6302:      type === T.DOOR_CLOSED || type === T.DOOR_OPEN || type === TILE_BY_KEY['v_83_herbs_mature']
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6337:    if (type === T.DOOR_CLOSED) {
~/Project/GLM/SandboxWorld/game/src/data/tiles.ts:67:def({ key: 'door_closed', name: '门', solid: true, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#77694F', drop: 25, vanilla: { sheet: 10, frame: 'style', fw: 1, fh: 3 } });
~/Project/GLM/SandboxWorld/game/src/data/tiles.ts:68:def({ key: 'door_open', name: '门(开)', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#77694F', drop: 25, vanilla: { sheet: 11, frame: 'style', fw: 2, fh: 3 } });
~/Project/GLM/SandboxWorld/game/src/data/tiles.ts:339:def({ key: 'v_387_trap_door_closed', name: '', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 1, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 387, frame: 'style', fw: 2, fh: 1 } });
~/Project/GLM/SandboxWorld/game/src/data/tiles.ts:475:def({ key: 'v_386_trapdooropen', name: '', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#7F5C45', drop: null, vanilla: { sheet: 386, frame: 'style', fw: 2, fh: 2 } });

```


---

## 🤖 Assistant · 2026-08-13T01:33:04.207Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Door is defined w:1 h:3 with top-left placement in tryPlace → the mouse tile becomes the TOP of the door. Vanilla: door placed at j-2 (mouse tile = bottom). Let me verify vanilla WorldGen.PlaceTile door offset to be sure.

From memory note (vanilla-door-frames.md): "PlaceTile 放门要 j-2". So vanilla door anchor = mouse tile is the BOTTOM tile, object extends up 2. Implementation places at top-left → door appears 2 tiles LOWER than vanilla. That's a real placement anchor deviation for doors. Actually wait — is there a compensation in tryPlace for doors? No door-specific code in tryPlace. And the memory note says door *placement* was a known topic. Hmm, but that memory note is about generation-side PlaceTile (worldgen), not player placement. Player placement of doors in vanilla goes through PlaceThing_Tiles → TileObject.CanPlace with TileObjectData for tile 10 (closed door): Origin for doors = (0, 2)? Let me check TileObjectData for door.

Let me grep TileObjectData.cs for tile 10.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:33:05.354Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"addTile(10)\\|addTile(11)\\|addTile(19)\\|new TileObjectData.*Origin\" TileObjectData.cs | head -8; echo \"===door setup===\"; awk 'NR>=1 && NR<=200' TileObjectData.cs | grep -n \"Origin\\|addTile\\|StyleWrapLimit\\|CoordinateHeights\" | head -20",
 "description": "Check TileObjectData origin for doors"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:08.803Z

**📎 ToolResult**

```
ugrep: warning: TileObjectData.cs: No such file or directory
===door setup===
awk: can't open file TileObjectData.cs
 source line number 1

```


---

## 🤖 Assistant · 2026-08-13T01:33:10.414Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find \"~/Project/GLM/SandboxWorld/Terarria1456\" -name \"TileObjectData.cs\" | head -2",
 "description": "Locate TileObjectData.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:10.466Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData/TileObjectData.cs

```


---

## 🤖 Assistant · 2026-08-13T01:33:12.636Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && grep -n \"Origin\" TileObjectData.cs | head -5; grep -n \"CalculateOrigin\\|Origin = \" TileObjectData.cs | head -10",
 "description": "Find Origin calculation in TileObjectData"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:12.712Z

**📎 ToolResult**

```
1252:	public Point16 Origin
1258:				return _baseObject.Origin;
1279:					_alternates.data[i].Origin = value;
1781:		Origin = Point16.Zero;
2164:		newTile.Origin = new Point16(1, 7);
1279:					_alternates.data[i].Origin = value;
1781:		Origin = Point16.Zero;
2164:		newTile.Origin = new Point16(1, 7);
2175:		newTile.Origin = new Point16(0, 0);
2226:		newTile.Origin = new Point16(0, 0);
2238:		newAlternate.Origin = new Point16(0, 1);
2241:		newAlternate.Origin = new Point16(0, 2);
2251:		newTile.Origin = new Point16(0, 0);
2264:		newAlternate.Origin = new Point16(0, 1);
2267:		newAlternate.Origin = new Point16(0, 2);

```


---

## 🤖 Assistant · 2026-08-13T01:33:17.736Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && grep -n \"int num = 0\" TileObjectData.cs | head -3; grep -n \"public static void Initialize\\|void SetupData\" TileObjectData.cs | head -5; grep -n -A20 \"for (int i = 0; i < \" TileObjectData.cs | grep -n \"Origin\" | head; grep -n \"Origin.X = \\|Origin.Y = \" TileObjectData.cs | head",
 "description": "Find default Origin derivation loop"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:17.833Z

**📎 ToolResult**

```
1813:		int num = 0;
2111:	public static void Initialize()
581:1252-	public Point16 Origin
587:1258-				return _baseObject.Origin;
597:1279-					_alternates.data[i].Origin = value;

```


---

## 🤖 Assistant · 2026-08-13T01:33:19.623Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && sed -n '1800,1860p' TileObjectData.cs",
 "description": "Read TileObjectData base constructor origin"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:19.674Z

**📎 ToolResult**

```
		StyleHorizontal = false;
		StyleWrapLimit = 0;
		StyleMultiplier = 1;
	}

	private void Calculate()
	{
		if (_tileObjectCoords.calculated)
		{
			return;
		}
		_tileObjectCoords.calculated = true;
		_tileObjectCoords.styleWidth = (_tileObjectCoords.width + _tileObjectCoords.padding) * Width + _tileObjectCoords.paddingFix.X;
		int num = 0;
		_tileObjectCoords.styleHeight = 0;
		for (int i = 0; i < _tileObjectCoords.heights.Length; i++)
		{
			num += _tileObjectCoords.heights[i] + _tileObjectCoords.padding;
		}
		num += _tileObjectCoords.paddingFix.Y;
		_tileObjectCoords.styleHeight = num;
		if (_hasOwnLiquidDeath)
		{
			if (_liquidDeath.lava)
			{
				LavaPlacement = LiquidPlacement.NotAllowed;
			}
			if (_liquidDeath.water)
			{
				WaterPlacement = LiquidPlacement.NotAllowed;
			}
		}
	}

	private void WriteCheck()
	{
		if (readOnlyData)
		{
			throw new FieldAccessException("Tile data is locked and only accessible during startup.");
		}
	}

	private void LockWrites()
	{
		readOnlyData = true;
	}

	public void ApplyNaturalObjectRules()
	{
		UsesCustomCanPlace = false;
		UsesGlobalLiquidChecks = true;
	}

	public bool LiquidPlace(Tile checkTile)
	{
		if (checkTile == null)
		{
			return false;
		}
		if (checkTile.liquid > 0)
		{

```


---

## 🤖 Assistant · 2026-08-13T01:33:21.472Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Origin default = Point16.Zero (line 1781). So for doors, the Origin is explicitly set. Let me look at the door entry in TileObjectData.Initialize — grep for "newTile.Type = 10" or similar around line 2230.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:33:21.830Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && sed -n '2215,2270p' TileObjectData.cs",
 "description": "Read door TileObjectData entries"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:21.873Z

**📎 ToolResult**

```
		newTile.AnchorTop = AnchorData.Empty;
		newTile.AnchorBottom = new AnchorData(AnchorType.SolidTile | AnchorType.Table, newTile.Width, 0);
		newTile.Direction = TileObjectDirection.PlaceLeft;
		newTile.StyleHorizontal = true;
		newTile.DrawFlipHorizontal = false;
		newAlternate.CopyFrom(newTile);
		newAlternate.Direction = TileObjectDirection.PlaceRight;
		addAlternate(1);
		addTile(579);
		newTile.Width = 1;
		newTile.Height = 3;
		newTile.Origin = new Point16(0, 0);
		newTile.AnchorTop = new AnchorData(AnchorType.SolidTile, newTile.Width, 0);
		newTile.AnchorBottom = new AnchorData(AnchorType.SolidTile, newTile.Width, 0);
		newTile.UsesCustomCanPlace = true;
		newTile.LavaDeath = true;
		newTile.CoordinateHeights = new int[3] { 16, 16, 16 };
		newTile.CoordinateWidth = 16;
		newTile.CoordinatePadding = 2;
		newTile.StyleHorizontal = false;
		newTile.StyleWrapLimit = 36;
		newTile.StyleLineSkip = 3;
		newAlternate.CopyFrom(newTile);
		newAlternate.Origin = new Point16(0, 1);
		addAlternate(0);
		newAlternate.CopyFrom(newTile);
		newAlternate.Origin = new Point16(0, 2);
		addAlternate(0);
		newSubTile.CopyFrom(newTile);
		newSubTile.LinkedAlternates = true;
		newSubTile.LavaDeath = false;
		newSubTile.LavaPlacement = LiquidPlacement.Allowed;
		addSubTile(19, 48);
		addTile(10);
		newTile.Width = 2;
		newTile.Height = 3;
		newTile.Origin = new Point16(0, 0);
		newTile.AnchorTop = new AnchorData(AnchorType.SolidTile, 1, 0);
		newTile.AnchorBottom = new AnchorData(AnchorType.SolidTile, 1, 0);
		newTile.UsesCustomCanPlace = true;
		newTile.LavaDeath = true;
		newTile.CoordinateHeights = new int[3] { 16, 16, 16 };
		newTile.CoordinateWidth = 16;
		newTile.CoordinatePadding = 2;
		newTile.StyleHorizontal = false;
		newTile.StyleWrapLimit = 36;
		newTile.StyleLineSkip = 2;
		newTile.Direction = TileObjectDirection.PlaceRight;
		newAlternate.CopyFrom(newTile);
		newAlternate.Origin = new Point16(0, 1);
		addAlternate(0);
		newAlternate.CopyFrom(newTile);
		newAlternate.Origin = new Point16(0, 2);
		addAlternate(0);
		newAlternate.CopyFrom(newTile);
		newAlternate.Origin = new Point16(1, 0);

```


---

## 🤖 Assistant · 2026-08-13T01:33:28.230Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Door (tile 10): base Origin = (0,0), alternates (0,1) and (0,2). So the CanPlace tries alternate 0 (Origin 0,0 → object top at mouse Y), then alternate (0,1) → top at mouseY-1, then (0,2) → top at mouseY-2. The door is placed at the position where the anchor validation passes — effectively "the mouse tile is one of the door's three tiles, preferring the top". So vanilla door placement prefers top-anchored (mouse = top tile), falling back to y-1, y-2.

So implementation's top-left anchor for doors (mouse = top tile) matches the FIRST alternate. Not a deviation for doors in the common case. Good — I should not report doors as wrong.

But for general furniture: e.g., tables (tile 19 has subtiles with Origin (0,0),(0,1),(0,2) — wait, `addSubTile(19, 48)`? No — the block above (lines 2226-2248) is tile 10 (door). The `addSubTile(19, 48)` is platform on door? Actually the addTile(10) closes the door block and the subTile 19 = platform variant of door (door with platform)?

For typical furniture like tables: vanilla TileObjectData for a 3×2 table has Origin = (1, 1)? Let me check the table (tile 19 is workbench? no). Let me check tile 88 (table) Origin.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:33:28.942Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && grep -n -B3 -A12 \"addTile(88)\\|addTile(15)\" TileObjectData.cs | grep -n \"Origin\\|Width\\|Height\\|addTile\\|Anchor\" | head -20",
 "description": "Check table/workbench origins"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:28.998Z

**📎 ToolResult**

```
4:3204:		addTile(88);
8:3208-		addTile(237);
11:3211-		addTile(244);
14:3214-		addTile(647);
21:4164:		addTile(15);
23:4166-		newTile.CoordinateHeights = new int[2] { 16, 18 };

```


---

## 🤖 Assistant · 2026-08-13T01:33:30.557Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && sed -n '3180,3206p' TileObjectData.cs",
 "description": "Read table tile origin block"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:30.645Z

**📎 ToolResult**

```
		addSubTile(13);
		newSubTile.CopyFrom(Style3x2);
		newSubTile.Height = 1;
		newSubTile.Origin = new Point16(1, 0);
		newSubTile.CoordinateHeights = new int[1] { 16 };
		addSubTile(25);
		addTile(14);
		newTile.CopyFrom(Style3x2);
		newTile.CoordinateHeights = new int[2] { 16, 18 };
		newSubTile.CopyFrom(Style3x2);
		newSubTile.LavaDeath = false;
		newSubTile.LavaPlacement = LiquidPlacement.Allowed;
		addSubTile(11);
		addTile(469);
		newTile.CopyFrom(Style3x2);
		newTile.StyleWrapLimitVisualOverride = 37;
		newTile.HookCheckIfCanPlace = new PlacementHook(Chest.FindEmptyChest, -1, 0, processedCoordinates: true);
		newTile.HookPostPlaceMyPlayer = new PlacementHook(Chest.AfterPlacement_Hook, -1, 0, processedCoordinates: false);
		newTile.AnchorInvalidTiles = anchorInvalidTiles;
		newTile.LavaDeath = false;
		newSubTile.CopyFrom(newTile);
		newSubTile.LavaDeath = false;
		newSubTile.LavaPlacement = LiquidPlacement.Allowed;
		addSubTile(9, 42);
		addTile(88);
		newTile.CopyFrom(Style3x2);
		newTile.LavaDeath = false;

```


---

## 🤖 Assistant · 2026-08-13T01:33:33.317Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`Style3x2` — the base style for tables/chests. Let me find Style3x2 definition to get its Origin.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:33:34.097Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && grep -n -A14 \"Style3x2 = new TileObjectData\\|Style1x1 = new TileObjectData\\|Style2x2 = new TileObjectData\" TileObjectData.cs | grep -E \"Style|Origin|Width|Height|AnchorBottom\" | head -20",
 "description": "Read style base origins"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:34.167Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T01:33:36.081Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && grep -n \"Style3x2\" TileObjectData.cs | head -3; grep -n \"Style1x2\\|Style3x3\" TileObjectData.cs | head -3",
 "description": "Find style definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:36.165Z

**📎 ToolResult**

```
108:	private static TileObjectData Style3x2;
3174:		addBaseTile(out Style3x2);
3175:		newTile.CopyFrom(Style3x2);
86:	private static TileObjectData Style1x2;
102:	private static TileObjectData Style1x2Top;
110:	private static TileObjectData Style3x3;

```


---

## 🤖 Assistant · 2026-08-13T01:33:38.143Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && grep -n -A8 \"private static void addBaseTile\" TileObjectData.cs | head -14; grep -n \"private static void addTile(.*out TileObjectData\" TileObjectData.cs | head -3",
 "description": "Read addBaseTile origin"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:38.222Z

**📎 ToolResult**

```
2001:	private static void addBaseTile(out TileObjectData baseTile)
2002-	{
2003-		newTile.Calculate();
2004-		baseTile = newTile;
2005-		baseTile._parent = _baseObject;
2006-		newTile = new TileObjectData(_baseObject);
2007-	}
2008-
2009-	private static void addTile(int tileType)

```


---

## 🤖 Assistant · 2026-08-13T01:33:39.885Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && sed -n '1781,1800p' TileObjectData.cs",
 "description": "Read TileObjectData constructor defaults"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:39.927Z

**📎 ToolResult**

```
		Origin = Point16.Zero;
		Direction = TileObjectDirection.None;
		RandomStyleRange = 0;
		FlattenAnchors = false;
		_tileObjectCoords = new TileObjectCoordinatesModule();
		_hasOwnTileObjectCoords = true;
		CoordinateHeights = new int[1] { 16 };
		CoordinateWidth = 0;
		CoordinatePadding = 0;
		CoordinatePaddingFix = Point16.Zero;
		_tileObjectDraw = new TileObjectDrawModule();
		_hasOwnTileObjectDraw = true;
		DrawYOffset = 0;
		DrawFlipHorizontal = false;
		DrawFlipVertical = false;
		DrawStepDown = 0;
		_tileObjectStyle = new TileObjectStyleModule();
		_hasOwnTileObjectStyle = true;
		Style = 0;
		StyleHorizontal = false;

```


---

## 🤖 Assistant · 2026-08-13T01:33:44.347Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key finding: **vanilla default Origin = (0,0)** — so for most furniture (tables/chests via Style3x2 with no Origin override), the placement top-left = mouse tile = **top-left anchor**! So the implementation's top-left anchor actually matches vanilla default Origin (0,0)!

Let me double check: does Style3x2 set Origin anywhere? The addBaseTile just copies newTile (which has Origin=(0,0) default). Let me check whether newTile before addBaseTile sets Width=3/Height=2 and Origin. Let me look at lines 3160-3175.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:33:44.787Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && sed -n '3150,3176p' TileObjectData.cs",
 "description": "Read newTile setup before styles"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:44.828Z

**📎 ToolResult**

```
		addSubTile(32, 48);
		newSubTile.CopyFrom(newTile);
		newSubTile.WaterDeath = false;
		newSubTile.WaterPlacement = LiquidPlacement.Allowed;
		addSubTile(46);
		addTile(34);
		newTile.CopyFrom(Style3x3);
		newTile.Width = 4;
		newTile.Origin = new Point16(2, 0);
		newTile.AnchorTop = new AnchorData(AnchorType.SolidTile | AnchorType.SolidSide, 1, 1);
		newTile.AnchorBottom = AnchorData.Empty;
		newTile.LavaDeath = true;
		newTile.DrawYOffset = -2;
		addTile(454);
		newTile.Width = 3;
		newTile.Height = 2;
		newTile.Origin = new Point16(1, 1);
		newTile.AnchorBottom = new AnchorData(AnchorType.SolidTile | AnchorType.SolidWithTop | AnchorType.SolidSide, newTile.Width, 0);
		newTile.UsesCustomCanPlace = true;
		newTile.CoordinateHeights = new int[2] { 16, 16 };
		newTile.CoordinateWidth = 16;
		newTile.CoordinatePadding = 2;
		newTile.StyleHorizontal = true;
		newTile.LavaDeath = true;
		addBaseTile(out Style3x2);
		newTile.CopyFrom(Style3x2);
		newTile.CoordinateHeights = new int[2] { 16, 18 };

```


---

## 🤖 Assistant · 2026-08-13T01:33:51.388Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
**Critical correction**: `Style3x2` (base for tables tile 14/88, chests 21, dressers 88/469, pianos, etc.) has `Origin = new Point16(1, 1)` — i.e., **mouse tile = bottom-center of the 3×2 object** → object top-left = (x-1, y-1).

So for the majority of 3×2 furniture (tables, chests, bookcases?, pianos, workbenches via Style3x3? no workbench is tile 18?), the vanilla anchor is bottom-center.

Implementation: top-left = mouse tile. So a table placed in this repo appears **1 tile right and 1 tile down** relative to vanilla. That IS a real deviation for multi-tile furniture.

Let me verify what Style1x2 (doors/banners, 1 wide 2 tall?) and Style1x1 are. And chests (tile 21 → Style3x2 with Origin (1,1)). Yes — chest is 2×2? Vanilla chest is 2×2 tiles (sheet 21), style 3x2? Chest tile is 2 wide 2 tall. Hmm, Style3x2 → addSubTile(9,42) for tile 88 (dresser)... then addTile(88). Chests tile 21: let me check. Search "addTile(21)".
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:33:52.467Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terrarria 2>/dev/null\"; cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && grep -n -B12 \"addTile(21);\" TileObjectData.cs | grep -E \"Origin|Width|Height|Style|addTile|addSubTile\" | head -8; echo \"===workbench 18===\"; grep -n -B10 \"addTile(18);\" TileObjectData.cs | grep -E \"Origin|Width|Height|addTile\" | head -6",
 "description": "Check chest and workbench origins"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:33:58.121Z

**📎 ToolResult**

```
(eval):cd:1: no such file or directory: ~/Project/GLM/SandboxWorld/Terrarria 2>/dev/null
3455-		addBaseTile(out Style2x2);
3456-		newTile.CopyFrom(Style2x2);
3457-		newTile.Origin = new Point16(0, 1);
3458-		newTile.CoordinateHeights = new int[2] { 16, 18 };
3462-		newTile.StyleHorizontal = true;
3464-		newTile.AnchorBottom = new AnchorData(AnchorType.SolidTile | AnchorType.SolidWithTop | AnchorType.SolidSide, newTile.Width, 0);
3465:		addTile(21);
===workbench 18===
2811-		newTile.AnchorBottom = new AnchorData(AnchorType.Table, newTile.Width, 0);
2812-		addTile(462);
2815-		newTile.CoordinateHeights = new int[1] { 18 };
2820:		addTile(18);

```


---

## 🤖 Assistant · 2026-08-13T01:34:00.619Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.ObjectData\" && sed -n '3445,3460p' TileObjectData.cs; echo \"===Style1x2 (2800-2820)===\"; sed -n '2795,2820p' TileObjectData.cs | grep -E \"Origin|Width|Height|addBaseTile|CoordinateHeights\"",
 "description": "Read Style2x2 and workbench origins"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:00.708Z

**📎 ToolResult**

```
		addTile(699);
		newTile.Width = 2;
		newTile.Height = 2;
		newTile.Origin = new Point16(0, 1);
		newTile.AnchorBottom = new AnchorData(AnchorType.SolidTile | AnchorType.SolidWithTop | AnchorType.Table | AnchorType.SolidSide, newTile.Width, 0);
		newTile.UsesCustomCanPlace = true;
		newTile.CoordinateHeights = new int[2] { 16, 16 };
		newTile.CoordinateWidth = 16;
		newTile.CoordinatePadding = 2;
		newTile.LavaDeath = true;
		addBaseTile(out Style2x2);
		newTile.CopyFrom(Style2x2);
		newTile.Origin = new Point16(0, 1);
		newTile.CoordinateHeights = new int[2] { 16, 18 };
		newTile.HookCheckIfCanPlace = new PlacementHook(Chest.FindEmptyChest, -1, 0, processedCoordinates: true);
		newTile.HookPostPlaceMyPlayer = new PlacementHook(Chest.AfterPlacement_Hook, -1, 0, processedCoordinates: false);
===Style1x2 (2800-2820)===
		newTile.Origin = new Point16(0, 0);
		newTile.AnchorBottom = new AnchorData(AnchorType.SolidTile | AnchorType.SolidWithTop | AnchorType.SolidSide, newTile.Width, 0);
		newTile.CoordinateHeights = new int[1] { 16 };
		newTile.CoordinateWidth = 16;
		addBaseTile(out Style2x1);
		newTile.AnchorBottom = new AnchorData(AnchorType.Table, newTile.Width, 0);
		newTile.AnchorBottom = new AnchorData(AnchorType.Table, newTile.Width, 0);
		newTile.AnchorBottom = new AnchorData(AnchorType.Table, newTile.Width, 0);
		newTile.CoordinateHeights = new int[1] { 18 };

```


---

## 🤖 Assistant · 2026-08-13T01:34:10.765Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have solid evidence on placement anchors in vanilla:
- **Style2x2** (Origin (0,1)): chest (21) with Origin (0,1) → top-left = (x, y-1) — mouse tile = bottom-left of the 2×2.
- **Style3x2** (Origin (1,1)): tables/dressers → top-left = (x-1, y-1) — mouse = bottom-center.
- **Style2x1** (Origin (0,0)): benches etc.
- Doors (10): Origin (0,0) with alternates (0,1)/(0,2) → prefer mouse = top tile.

So vanilla anchor semantics vary per object; the common case is "mouse = bottom row, horizontally centered for 3-wide". Implementation uniformly uses top-left. This is a genuine 🔀 for multi-tile furniture (tables, chests, bookcases...) — the object renders up to (1,1) or (1,2) tiles off from vanilla.

Now let me quickly verify one thing on slope placement: the implementation's placement space check doesn't consider slope at all (just isActive). Vanilla TileObject.CanPlace has slope/half-brick handling in `TileUtilities`? Actually CanPlace checks `tile.halfBrick()`/slope via the anchor checks (AnchorBottom requires a full top). Also `PlaceThing_Tiles` → `CanPlaceWithSkipping`. Implementation's `hasSupport` (isActive on neighbors incl. wall) is cruder than AnchorBottom (SolidTile/SolidWithTop). Good enough to report as approximation.

Also should check the "smart cursor 对平台/门/轨道的特殊逻辑" — done (Step_Platforms writes direction locks; tracks; doors are in the DisableSmartCursor set → smart cursor yields to doors when hovering). ✅

Now, "开采优先级" (mining priority) — the step chain order is 1:1 ✅.

One more thing to verify: **联机距离** — vanilla: `IsInTileInteractionRange` is client-side; server validates via `NetMessage` / `Player.CheckMana`? Actually the server checks tile edits: `NetMessage` handlers check distance? In vanilla multiplayer, the server does NOT range-check block edits (trusts client) — actually it does have some checks in `NetSync`... Hmm. Vanilla server-side: `NetMessage.ReceiveBytes` → for tile edits (msg 17) the server just applies them (with a few checks like spawn protection). So range checks are client-side only in vanilla too. The implementation has client-side range checks + net room protection (its own system). I'll note it as aligned-by-equivalent (not vanilla but a self-made system; vanilla has no range check server-side, so client-side check = same effective).

Let me now double-check the Options.ts smart cursor settings and the Settings UI mapping (toggle/hold, SmartAxeAfterPickaxe, SmartBlocksEnabled, HoldCanReleaseMidUse).
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:34:11.644Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"smartCursor\\|SmartCursor\\|smart\" ~/Project/GLM/SandboxWorld/game/src/core/Options.ts | head -15; echo \"===Settings 255-285===\"; sed -n '255,285p' ~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts",
 "description": "Read smart cursor settings storage and UI"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:11.791Z

**📎 ToolResult**

```
11:  // 智能光标（对齐原版 Player.SmartCursorSettings + IngameOptions/Main.cs:49705 设置结构）
12:  smartCursorMode: 'toggle' | 'hold';  // Main.cSmartCursorModeIsToggleAndNotHold（默认 Toggle）
13:  smartAxeAfterPickaxe: boolean;       // UseSmartAxeAfterSmartPickaxe（默认 false）
14:  smartBlocksEnabled: boolean;         // SmartBlocksEnabled（默认 true）
15:  smartHoldCanReleaseMidUse: boolean;  // SmartCursorHoldCanReleaseMidUse（默认 true）
30:    smartCursorMode: 'toggle',
31:    smartAxeAfterPickaxe: false,
32:    smartBlocksEnabled: true,
33:    smartHoldCanReleaseMidUse: true,
===Settings 255-285===
        this.toggle(Lang.text('Mods.SandboxWorld.Settings.DevMode'), () => d.devMode, (v) => void options.set('devMode', v)),
        // 背景 开/关（Main.BackgroundEnabled Main.cs:790，原版视频设置项 Lang.menu[100/101]；
        // 天气阴天渐变 cloudBGAlpha 的门，Game.updateWeather 注入 WeatherCtx.backgroundEnabled）
        this.toggle(Lang.menu(100).replace(/[:：].*$/, ''), () => d.backgrounds, (v) => void options.set('backgrounds', v)),
        // 图块在风中摆动（原版视频设置 SettingsEnabled_TilesSwayInWind；WindSway 系统总门）
        this.toggle('图块在风中摆动', () => d.swayInWind, (v) => void options.set('swayInWind', v)),
        // 智能光标（原版 IngameOptions :1418 Smart Cursor 段）：模式 Toggle/Hold + 三开关
        this.modeRow(
          Lang.text('Mods.SandboxWorld.Settings.SmartCursorMode'),
          () => d.smartCursorMode,
          () => Lang.text(d.smartCursorMode === 'toggle'
            ? 'Mods.SandboxWorld.Settings.SmartCursorToggle'
            : 'Mods.SandboxWorld.Settings.SmartCursorHold'),
          () => void options.set('smartCursorMode', d.smartCursorMode === 'toggle' ? 'hold' : 'toggle'),
        ),
        this.toggle(Lang.text('Mods.SandboxWorld.Settings.SmartAxeAfterPickaxe'), () => d.smartAxeAfterPickaxe, (v) => void options.set('smartAxeAfterPickaxe', v)),
        this.toggle(Lang.text('Mods.SandboxWorld.Settings.SmartBlocks'), () => d.smartBlocksEnabled, (v) => void options.set('smartBlocksEnabled', v)),
        this.toggle(Lang.text('Mods.SandboxWorld.Settings.SmartHoldRelease'), () => d.smartHoldCanReleaseMidUse, (v) => void options.set('smartHoldCanReleaseMidUse', v)),
      );
      const hint = document.createElement('div');
      hint.className = 'sw-set-hint';
      hint.textContent = Lang.text('Mods.SandboxWorld.Settings.DevModeHint');
      this.content.append(hint);
      const scHint = document.createElement('div');
      scHint.className = 'sw-set-hint';
      scHint.textContent = Lang.text('Mods.SandboxWorld.Settings.SmartCursorHint');
      this.content.append(scHint);
    } else if (this.cat === 'data' && this.flow.onQuickLoad) {
      const btns = document.createElement('div');
      btns.className = 'sw-set-btns';
      const mk = (label: string, fn: () => void) => {

```


---

## 🤖 Assistant · 2026-08-13T01:34:13.367Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Settings are complete (toggle/hold + 3 sub-switches). ✅

Let me verify vanilla Player.SmartCursorSettings defaults to confirm the 4 fields and defaults.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:34:13.971Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n -A8 \"class SmartCursorSettings\\|struct SmartCursorSettings\" Player.cs | head -14; grep -n \"cSmartCursorModeIsToggleAndNotHold = \" Main.cs | head -3",
 "description": "Verify vanilla SmartCursorSettings defaults"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:14.045Z

**📎 ToolResult**

```
322:	public class SmartCursorSettings
323-	{
324-		public static bool SmartBlocksEnabled;
325-
326-		public static bool SmartAxeAfterPickaxe;
327-
328-		public static bool SmartCursorHoldCanReleaseMidUse;
329-	}
330-
4782:					cSmartCursorModeIsToggleAndNotHold = binaryReader.ReadBoolean();
49709:					cSmartCursorModeIsToggleAndNotHold = !cSmartCursorModeIsToggleAndNotHold;
66090:		cSmartCursorModeIsToggleAndNotHold = true;

```


---

## 🤖 Assistant · 2026-08-13T01:34:15.959Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla SmartCursorSettings statics default false (SmartBlocksEnabled=false, SmartAxeAfterPickaxe=false, SmartCursorHoldCanReleaseMidUse=false)! Hmm — but are they set true somewhere? Let me check where they're assigned (config load / Main).
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:34:16.533Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"SmartBlocksEnabled = \\|SmartAxeAfterPickaxe = \\|SmartCursorHoldCanReleaseMidUse = \" Player.cs Main.cs 2>/dev/null | head -10",
 "description": "Find vanilla smart settings assignments"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:16.580Z

**📎 ToolResult**

```
Main.cs:49716:					Player.SmartCursorSettings.SmartAxeAfterPickaxe = !Player.SmartCursorSettings.SmartAxeAfterPickaxe;
Main.cs:49723:					Player.SmartCursorSettings.SmartBlocksEnabled = !Player.SmartCursorSettings.SmartBlocksEnabled;

```


---

## 🤖 Assistant · 2026-08-13T01:34:18.876Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -rn \"SmartBlocksEnabled\\|SmartAxeAfterPickaxe\\|SmartCursorHoldCanReleaseMidUse\" Configuration.cs 2>/dev/null | head -6; find .. -name \"*.cs\" | xargs grep -ln \"SmartBlocksEnabled = true\\|SmartCursorHoldCanReleaseMidUse = true\" 2>/dev/null | head -3",
 "description": "Check config defaults for smart settings"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:24.385Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T01:34:29.656Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No assignments to true anywhere in the decompiled source (only toggles in options UI). So vanilla defaults (fresh config): SmartBlocksEnabled=false, SmartAxeAfterPickaxe=false, SmartCursorHoldCanReleaseMidUse=false.

Hmm wait — but `Main.cSmartCursorModeIsToggleAndNotHold = true` at Main.cs:66090. And the three settings are saved/loaded from config? Let me check Main.LoadSettings/SaveSettings for these.

Actually the toggle at Main.cs:49716/49723 is IngameOptions. And config.json loads them? Let me search for "useSmartAxeInsteadOfPickaxe" or similar in Main.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:34:30.092Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"smartCursorSettings\\|SmartCursorSettings\\.\" Main.cs | head -10",
 "description": "Check config persistence of smart settings"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:30.117Z

**📎 ToolResult**

```
4191:		configuration.Put("UseSmartCursorForCommonBlocks", Player.SmartCursorSettings.SmartBlocksEnabled);
4192:		configuration.Put("UseSmartAxeAfterSmartPickaxe", Player.SmartCursorSettings.SmartAxeAfterPickaxe);
4193:		configuration.Put("SmartCursorHoldCanReleaseMidUse", Player.SmartCursorSettings.SmartCursorHoldCanReleaseMidUse);
4438:		configuration.Get("UseSmartCursorForCommonBlocks", ref Player.SmartCursorSettings.SmartBlocksEnabled);
4439:		configuration.Get("UseSmartAxeAfterSmartPickaxe", ref Player.SmartCursorSettings.SmartAxeAfterPickaxe);
4440:		configuration.Get("SmartCursorHoldCanReleaseMidUse", ref Player.SmartCursorSettings.SmartCursorHoldCanReleaseMidUse);
49712:				array9[num37] = (Player.SmartCursorSettings.SmartAxeAfterPickaxe ? Lang.menu[214].Value : Lang.menu[213].Value);
49716:					Player.SmartCursorSettings.SmartAxeAfterPickaxe = !Player.SmartCursorSettings.SmartAxeAfterPickaxe;
49719:				array9[num37] = (Player.SmartCursorSettings.SmartBlocksEnabled ? Lang.menu[215].Value : Lang.menu[216].Value);
49723:					Player.SmartCursorSettings.SmartBlocksEnabled = !Player.SmartCursorSettings.SmartBlocksEnabled;

```


---

## 🤖 Assistant · 2026-08-13T01:34:36.217Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`configuration.Get(name, ref value)` with no default → default false. So vanilla defaults: SmartBlocksEnabled = **false**, SmartAxeAfterPickaxe = **false**, SmartCursorHoldCanReleaseMidUse = **false**, cSmartCursorModeIsToggleAndNotHold = **true**.

Implementation defaults (Options.ts:30-33): smartCursorMode 'toggle' ✅, smartAxeAfterPickaxe false ✅, smartBlocksEnabled **true** ❌ (vanilla false!), smartHoldCanReleaseMidUse **true** ❌ (vanilla false!).

So two default-value deviations. Impact:
- smartBlocksEnabled=true: but due to the vanilla "dead gate" preserved in stepBlocksFilling (SmartBlocksEnabled || → always return), BlocksFilling never fires when true. And BlocksLines requires smartBlocksEnabled to fire → with vanilla default false, **BlocksLines does nothing by default** (no smart block placement in a fresh vanilla game!). With implementation default true, BlocksLines is active → smart cursor block placement active by default. 🔀 behavioral difference from default config.
- smartHoldCanReleaseMidUse=true: only matters in Hold mode; default mode is Toggle → no impact in default config.

Good — that's a subtle but real finding (worth ⚠️).

Now let me confirm the tileTarget override and mining path don't double-apply the smart cursor for right-click. Game.ts:4032-4040 — `if (this.smartCursor.showing) { tx = sc.x; ty = sc.y; }` then interactAt is called at 4032? Let me re-read lines 4020-4040.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:34:36.525Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '4020,4050p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read smart cursor tile target override"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:36.551Z

**📎 ToolResult**

```
      } else if (heldDef && viIdFromKey(heldDef.key) === 43) {
        if (!this.world.clock.isDay) {
          // 被召唤门拦下（场上已有 NPC 4）时 SummonItemCheck=false → 不消耗（Player.cs:51441-51447）
          if (this.useSuspiciousEye()) {
            this.player.inv.removeAt(this.player.inv.selected, 1);
            this.cb.onInventoryChanged();
          }
        } else {
          this.cb.onToast(Lang.text('Mods.SandboxWorld.Toast.NothingHappened'));
        }
        this.input.rightDown = false;
      } else {
        this.interactAt(tx, ty);
      }
    }

    // 智能光标覆盖（SmartCursorHelper.cs:157-162）：只影响左键使用路径（挖掘/放置/电路工具），
    // 右键交互（宝箱/门/NPC 交谈）上面已用原始鼠标格 rawTx/rawTy 处理完毕
    if (this.smartCursor.showing) {
      tx = this.smartCursor.x;
      ty = this.smartCursor.y;
    }

    if (!inp.mouseDown || this.annotateMode) {
      this.mining = null;
      return;
    }

    // 近战挥剑（vi_ 数据驱动近战武器同走挥击，数值取 combat 表；攻速倍率 =
    // Player.attackSpeedMult = CapAttackSpeeds 倒数档，Player.cs:28555-28574）
    const cw = heldDef ? combatWeapon(heldDef) : null;

```


---

## 🤖 Assistant · 2026-08-13T01:34:44.058Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Smart cursor tile target override: implemented correctly (only for left-click use path, right-click uses raw tile — matches vanilla where SmartCursorHelper sets Player.tileTargetX/Y which is used by the use-item path).

Wait — in vanilla, `SmartCursorLookup` writes `Player.tileTargetX = fX` which IS used for right-click too? No — right-click (controlUseTile) uses Main.SmartInteractX/Y (`smartInteract`), not tileTarget. Actually Player.tileTargetX is used by both... hmm. In vanilla, `ItemCheck_ManageRightClickFeatures`/`TryInteract` uses `Main.SmartInteractX`. The implementation notes this correctly. Fine.

Now, I have enough for the report. Let me do a couple of final verifications:

1. Slope placement: does implementation reject placing blocks on slopes? Vanilla places fine (blocks merge). Not critical.

2. Check whether the quick-heal-like "best fit" exists in the inventory UI (maybe potion quick-use in UI)? Not required.

3. Verify the DebugReport smart cursor section exists (for completeness).

4. Confirm the middle-click: Input.ts has no button===1 → ❌ no middle click pick. Note vanilla has no middle-click pick block either (that's Minecraft). Vanilla middle click in inventory = favorite item. In-world middle click = nothing. So "方块拾取(中键选取)" per the checklist — in vanilla, there's no pick-block. Wait, the checklist says "方块拾取(选取同型/Pick 行为)、中键选取". In vanilla Terraria there is NO pick-block feature. The correct verdict: 原版无此机制(N/A),实现也无。Actually — hold on. There IS something: in vanilla, clicking a block with... no. There's "Auto Select" (Shift). I'll mark 中键选取 as N/A(原版无) + 实现未实现 = 无差异. Let me verify Game_controls.md middle click.

Let me grep the controls page for "middle".
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:34:44.569Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/terraria-wiki-md && grep -n -i \"middle\" Game_controls.md | head -5; grep -n -i \"favorite\" Game_controls.md | head -4",
 "description": "Check wiki for middle click bindings"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:44.634Z

**📎 ToolResult**

```
337:The touch screen features the player's hotbar, housing menu, map, and other utilities. This is referred to by the game as the "Quick Inventory". The quick inventory shows the first ten slots in the player's inventory, similarly to the mobile version of the game. The top left button under the hotbar allows the player to Quick Stack to Nearby Chests, which will be grayed out if the player is not near any chest. The middle button allows the player to drop an item they have tapped and held onto, grayed out if there is no item to drop. The top right button is the housing menu, which will be grayed out unless the player is in a [house](House.md "House"). 
128:  * To favorite an item (making it unable to be quick stacked, quick trashed, thrown, or deposited), hold Alt down clicking the item. A border should appear letting the player know that the item is favorited. Do note that placing favorited equipment onto the equipment slots and placing them back in the inventory will remove the favorite status on the equipment, in which case the player will to need to used Alt + Left Click again.
407:  * [Desktop 1.3.0.1](Desktop_1.3.0.1 "Desktop 1.3.0.1"): Added favorite option for items in the inventory and the mount hotkey.

```


---

## 🤖 Assistant · 2026-08-13T01:34:50.983Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: vanilla has no in-world middle-click pick-block. Favoriting is Alt+click. So checklist item 4 (方块拾取/中键选取) → N/A in vanilla; implementation has neither middle-click nor pick-block → no deviation to report, but I'll note "中键无绑定(与原版一致)".

One last check: multiplayer distance. The implementation has `netCanEditTile()` room protection — self-made. Vanilla: server does no range validation (client authoritative). I'll note briefly.

Also let me double check `quickHeal`-ish absence in VUI (hotbar right-click quick-use?). Not needed.

Let me also verify the claim about Game.ts:4138 (extractinator left-click use) range — vanilla Player.cs:41012 uses `item.tileBoost + blockRange` ✅ implementation matches.

And Game.ts:1203 tryQuickMinecart — vanilla Player.cs:5798 uses `TileReachCheckSettings.Simple.GetTileRegion(this)` with NO TB. Implementation adds tileRange+3 and Builder+1 → over-range. Minor.

Let me now also spot-check one thing in the smart cursor: the implementation env tileBoost (Game.ts:3820) — verify it matches vanilla (item.tileBoost + blockRange-if-placement-item). Let me read 3797-3856.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:34:51.368Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3785,3856p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Read updateSmartCursor env assembly"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:51.428Z

**📎 ToolResult**

```
    if (d.pickPower) return { type: 'pick', power: d.pickPower };
    return { type: 'hammer', power: d.hammerPower ?? tool.power ?? 10 };
  }

  /** 智能光标设置（对齐原版 Player.SmartCursorSettings + Main.cs:49705 设置结构） */
  private smartSettings(): SmartCursorSettings {
    const d = options.data;
    return {
      toggleMode: d.smartCursorMode === 'toggle',
      smartAxeAfterPickaxe: !!d.smartAxeAfterPickaxe,
      smartBlocksEnabled: !!d.smartBlocksEnabled,
      holdCanReleaseMidUse: !!d.smartHoldCanReleaseMidUse,
    };
  }

  /**
   * 智能光标每帧驱动（Player.cs:25159-25163 每帧 SmartCursorLookup + :28344-28374 Toggle/Hold 状态机）。
   * Ctrl 按下沿翻转（Toggle）/跟随（Hold）；切换播音效 12（menuTick）。
   * 必须在 updateUse 之前跑——同帧 lookup 结果即被挖掘/放置路径覆盖 tx/ty。
   */
  private updateSmartCursor() {
    const inp = this.input;
    const sc = this.smartCursor;
    const s = this.smartSettings();
    const controlSmart = inp.down('ControlLeft') || inp.down('ControlRight');
    if (sc.updateWanted(controlSmart, !!inp.mouseDown, s)) this.sfx.play('menuTick');
    const blocked = inp.uiBlocking || this.player.dead || !!this.minecart
      || this.renderer.fullMap.open || this.renderer.timeUiHover || this.renderer.weatherUiHover
      || this.annotateMode;
    if (blocked || !sc.wanted) { sc.showing = false; VUI.smartCursorOn = false; return; }
    const held = this.player.inv.heldItem();
    const heldDef = held ? ITEM_DEFS[held.id] : null;
    const tool = heldDef?.tool ?? (held ? this.itemFuncTool(held.id) : undefined);
    const [mx, my] = this.camera.screenToWorld(inp.mouseX, inp.mouseY);
    const p = this.player;
    // 放置物才有 blockRange（原版 SmartCursorLookup :95-98 createWall/createTile 才加）；
    // 工具 tileBoost=0
    const placing = heldDef?.tile != null || heldDef?.wallId != null;
    const tb = placing
      ? (p.equipStats.tileRange ? 3 : 0) + (p.buffs.has(BuffType.Builder) ? 1 : 0)
      : 0;
    // EmptyTile 的占位实体（玩家 + 敌怪 + 城镇 NPC）
    const occupants: Array<{ x: number; y: number; w: number; h: number }> = [
      { x: p.x, y: p.y, w: p.w, h: p.h },
    ];
    for (const e of this.entities.enemies) occupants.push({ x: e.x, y: e.y, w: e.w, h: e.h });
    for (const e of this.entities.npcs) occupants.push({ x: e.x, y: e.y, w: e.w, h: e.h });
    sc.lookup({
      st: this.world.store,
      mouse: { x: mx, y: my },
      actor: { x: p.x, y: p.y, w: p.w, h: p.h, cx: p.cx, cy: p.cy, facing: p.facing },
      held: { def: heldDef, tool: tool ? { type: tool.type, power: tool.power ?? 0 } : null },
      settings: s,
      tileBoost: tb,
      wireToolMode: this.wireToolMode,
      occupants,
      controlUseItem: !!inp.mouseDown,
      // Step_AlchemySeeds 成熟药草判定（WorldGen.cs:66198-66225 IsAlchemyPlantHarvestable）
      // 所需世界态；Main.time 口径 = 白天 (t-0.25)*54000 / 夜晚 (t-0.75 / t+0.25)*32400
      alchemy: {
        dayTime: this.world.clock.isDay,
        bloodMoon: this.world.clock.bloodMoon,
        moonPhase: this.world.clock.moonPhase,
        raining: this.world.weather.raining,
        cloudAlpha: this.world.weather.cloudAlpha,
        time: vanillaMainTime(this.world.clock.timeOfDay),
        worldSurface: this.world.groundLevel,
        remixWorld: false,
        maxTilesY: this.world.store.h,
      },
    });
    // 指针切到 Cursors[12] 智能光标帧（Main.cs:47442-47513 num=11+smart.ToInt()）

```


---

## 🤖 Assistant · 2026-08-13T01:34:56.475Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed the smart cursor TB: `placing ? (tileRange?3:0) + (Builder?1:0) : 0`. Missing:
1. `item.tileBoost` (wrenches 509/510/849/850/851/3612/3620/3625 have tileBoost 20 per vanilla — wait, earlier SmartSelect comment said "全物品中 tileBoost≠0 的仅 195/196/-1、509/510/+20、1305/+1、3505-3510/-1、5329/5330/+3". So wrenches (509/510) have tileBoost +20! So for wrenches, vanilla TB = 20 (+0 since not createTile). Implementation tb = 0 → smart cursor wrench search region = base 5/3 instead of 25/23. Real deviation.
2. blockRange from Toolbelt missing.

Let me verify vanilla item.tileBoost for 509: grep Item.cs for tileBoost = 20.

Actually the SmartSelect.ts comment (line 315-318) already documents this: "原版全物品中 tileBoost≠0 的仅 195/196/-1、509/510/+20、1305/+1、3505-3510/-1、5329/5330/+3（Item.cs:3787/:7425/:16116/:31370-31411/:42229）". So wrench tileBoost=20 is authoritative per their extraction. Good, I can cite SmartSelect.ts:313-318 as implementation-side evidence.

Now — the cursor swap. Let me read the last bit (3856+).
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:34:57.155Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '3856,3862p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts; echo \"===VUI 175-190===\"; sed -n '175,190p' ~/Project/GLM/SandboxWorld/game/src/vui/VUI.ts",
 "description": "Read cursor frame selection"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:34:57.215Z

**📎 ToolResult**

```
    // 指针切到 Cursors[12] 智能光标帧（Main.cs:47442-47513 num=11+smart.ToInt()）
    VUI.smartCursorOn = sc.showing;
  }

  /**
   * 智能选取每帧驱动（Player.cs:17283-17562 SmartSelectLookup 族）。
   * 与智能光标独立、可同按：Shift（键绑定 "SmartSelect" = LeftShift，PlayerInput.cs:1898）
===VUI 175-190===

  /** 智能光标激活中（Game 每帧写入）：指针切换到 Cursors[12] 帧（Main.cs:47442-47513 num=11+smart） */
  static smartCursorOn = false;

  /** Canvas 原版光标：菜单与游戏内统一绘制（系统光标已被 #sw-cursor-style 全树隐藏） */
  private static drawCursor() {
    if (!VUI.batch || !VUI.enabled) return;
    const tex = UITextures.get(VUI.smartCursorOn ? 'UI_Cursor_1' : 'UI_Cursor_0');
    if (!tex) return;
    const x = Math.round(UIScale.mouseX);
    const y = Math.round(UIScale.mouseY);
    VUI.batch.draw(tex, x, y, { color: rgb(255, 255, 255) });
  }

  /** 当前鼠标下的 UI 元素（供游戏输入分流：非空则 UI 消费了指针） */
  static elementUnderMouse() {

```


---

## 🤖 Assistant · 2026-08-13T01:35:37.655Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Confirmed: cursor frame swaps when `sc.showing` (SmartCursorShowing). Vanilla (Main.cs:44753): `else if (SmartCursorIsUsed) DrawCursor(..., smart: true)` — i.e., keyed on **SmartCursorWanted** (the mode being on), not on Showing. So when smart cursor is ON but no target found (e.g., aiming at sky), vanilla still shows the smart cursor; implementation shows the normal one. Minor 🔀.

I now have everything needed. Let me also quickly confirm the presence of the door toggle / chest open with smart interact (SmartInteract) — implementation uses findChestNear 3×3. Vanilla: Main.SmartInteract expands the hover to a region (TileInteractionLX..HX) so clicking any tile of a 2×2 chest opens it. Implementation 3×3 tolerance ≈ equivalent. OK.

One more: "放置时与现有格重叠的拒绝条件" — covered (isActive strict vs vanilla tileCut/BreakableWhenPlacing allowance). Also solid-vs-player overlap check exists ✅ (vanilla: WorldGen.CanPlaceWithSkipping? Actually vanilla rejects placement where solid tile overlaps player — yes via CanPlace → "Player.OverlappingTile"). Also enemies: vanilla allows placing blocks overlapping NPCs? Vanilla CanPlace checks only the local player (and other players in MP?) — hmm. Vanilla TileObject.CanPlace checks `Main.player[Main.myPlayer]` only? There's a check in CanPlace: `if (tile.active() && ...)`. The player-overlap check for solid tiles is in `Player.PlaceThing_Tiles`? Actually it's `WorldGen.CanPlaceWithSkipping`? Let me not over-verify; the implementation also rejects enemies (overlapsEntity includes enemies) which vanilla may not do for NPCs (vanilla DOES check all players? no). Minor; I'll note as unverified? Actually I recall vanilla `TileObject.CanPlace` has:

```csharp
if (tileData.IsPlatform ... ) 
```
and for solid there's a check in `Player.PlaceThing_Tiles`:
```csharp
if (!WorldGen.SolidTile(...) && tileData...)
```
Hmm. I'll mark the enemy-overlap nuance as ❓ to be safe.

Let me write the report now. Summary of findings:

**域:光标与方块交互**

差异清单:

1. **交互距离基础** — tileRangeX=5/tileRangeY=3 ✅ (Game.ts:5008-5016, TileReachCheckSettings.cs:53-62)
2. **range 配饰(Extendo Grip 2215/Architect Gizmo Pack 3061/Hand of Creation 5126)轴向偏差** — 原版 tileRangeX+=3/tileRangeY+=2 (Player.cs:12618-12621),实现把 +3 同时加到 X 和 Y (Game.ts:1203,5009-5010) → 垂直多 1 格 ⚠️
3. **挖掘距离不吃 range 配饰** — 原版挖掘 IsTargetTileInItemRange 用 Simple(含 tileRangeX/Y 静态值,即 +3/+2 生效);实现 tryMine 传 tb=0(Game.ts:5094)且 inTileRange 硬编码 5/3 → 挖掘距离不吃配饰 ❌
4. **Toolbelt(407) blockRange+1 完全缺失** — vanilla Player.cs:14875-14878 `currentItem.type == 407 → blockRange++`;vi_407_Toolbelt 存在但 vanilla-accfx.json 无该键 → 放置射程少 1 ❌
5. **Builder 药水 +1** ✅ (Game.ts:1203 等;Player.cs:9841-9845 buff 107 → blockRange++) — 但作用域过宽:右键交互(interactAt :6291)与 QuickMinecart(:1203)也吃了 Builder+1,原版这两处为 Simple 无 TB(Player.cs:30576/30600/5798)⚠️
6. **放置距离** ✅ tryPlace/tryPlaceWall 用 tileBoost+blockRange 口径(Player.cs:38939/39058)但缺 Toolbelt(见#4)
7. **智能光标开启规则** ✅ LeftCtrl toggle/hold + 4 设置项(SmartCursor.ts:402-417 对 Player.cs:28344-28374;Options.ts:30-33)
8. **设置默认值** — smartBlocksEnabled/smartHoldCanReleaseMidUse 默认 true(Options.ts:32-33),原版 configuration.Get 无默认=false(Main.cs:4438-4440,Player.cs:324-328) → 智能方块铺线默认开启(原版默认关)⚠️
9. **智能光标策略链** ✅ 39 策略 1:1 顺序(SmartCursor.ts:449-486 vs SmartCursorHelper.cs:117-156)
10. **智能光标搜索区 TB** — 缺 item.tileBoost(扳手族 509/510=+20,SmartSelect.ts:313-318)→ 扳手/剪线钳的智能光标搜索区只有 5/3,而实际放置可达 20(Game.ts:5818) ⚠️
11. **智能光标让位集/门/宝箱/床/拉杆等 57 项** ✅ SmartCursor.ts:24-26,101-105,1694-1700
12. **平台方向锁/轨道/砍树** ✅ SmartCursor.ts:898-978(平台锁),980-1037(轨道),501-563(树干帧校正)
13. **油漆三策略 no-op** — 油漆系统未建(SmartCursor.ts:1358-1387)❌(依赖缺失)
14. **放置对齐锚点** — 原版按 TileObjectData.Origin:Style3x2(桌/梳妆台)=(1,1) 即鼠标=底部中心;宝箱 21=(0,1) 鼠标=左下;门 10 备选 (0,0)/(0,1)/(0,2)。实现一律左上(Game.ts:6049-6060) → 多格家具整体偏移 1-2 格 🔀
15. **放置重叠拒绝** — 原版允许压过 tileCut(草/藤)与 BreakableWhenPlacing(TileObject.cs:357);实现 `if (st.isActive(px,py)) return` 全拒(Game.ts:6053) → 家具放不进草地 🔀
16. **放置支撑检查** — 原版 TileObjectData 锚点表(AnchorTop/Bottom/Side/Wall+Alternates);实现 hasSupport 下/上/侧任一近似(Game.ts:6196-6210,代码注释自认近似) ⚠️
17. **斜坡放置** — 实现未判 slope(vanilla CanPlace 有半砖/坡处理) ❓
18. **方块拾取/中键** — 原版无中键选取(仅 Alt 收藏/Shift 快移);实现无中键绑定(Input.ts:52-61) ✅(一致的无)
19. **H/J/B 快捷键** — 全部未实装 ❌(Game.ts:1366-1403 键位表无 H/J/B;vanilla Player.cs:5268 QuickHeal/5365 QuickMana/5453 QuickBuff)
20. **Quick Mount(R)** — 未实装,R 被占用为扳手模式循环(Game.ts:1394) ❌
21. **数字键热栏** ✅ Game.ts:1366-1370
22. **光标样式** — 原版 SmartCursorIsUsed(=Wanted)即换智能指针(Main.cs:44753);实现按 showing(有目标才换)(Game.ts:3858,VUI.ts:182) ⚠️
23. **黄框+方向箭头渲染** ✅ Renderer.ts:3829-3950 对 Main.cs:46016-46066
24. **多格连续放置辅助(BlocksLines/BlocksFilling)** ✅ 1:1 含原版死门(SmartCursor.ts:1264-1356);受 #8 默认值影响
25. **右键优先级链** ✅ 大体完整(挂物族→提取机→bank→门→箱→牌→墓碑→生命水晶→床→日晷→工位buff→开关→药草→八音盒/喷泉/天塔柱/派对柱→蜥蜴祭坛→永恒水晶座→晶塔);箱 3×3 容差≈SmartInteract;⚠️ 门在箱后判定顺序与原版 ItemCheck 序需对(原版按 tile 类型互斥,同格不可能双物,无实际冲突)
26. **Auto Select(Shift)** ✅ SmartSelect.ts 全量
27. **联机距离** — 客户端判定+房间保护(自研);原版服务器不校验射程 → 等价 ❓/ℹ️

TOP N 修复建议:
1. Toolbelt 407 blockRange 缺失(放置射程差 1) — data 层补键即可
2. range 配饰 Y 轴 +3→+2 + inTileRange 拆 X/Y 两参数
3. 挖掘路径不吃 range 配饰(tb=0) — 把 tileRangeX/Y 并入基础值
4. 多格家具放置锚点(Origin 表) — 影响所有 3×2/2×2 家具落点
5. 放置重叠拒绝过严(tileCut/BreakableWhenPlacing 放行)
6. H/J/B 快捷键未实装
7. 智能光标 TB 缺 item.tileBoost(扳手 20)
8. 智能光标默认值 smartBlocksEnabled/smartHoldCanReleaseMidUse 应为 false

Let me double check #26 evidence line numbers: SmartSelect.ts is 538 lines, full port. Update() at :248-264.

Also the interaction distance "放置 vs 挖掘 vs 使用物品" — vanilla: 使用物品(如药水/武器)无距离限制;放置类(PlaceThing)用 tileBoost+blockRange;挖掘用 tileBoost;右键 Simple 无TB。I covered this.

Also "联机距离" for vanilla: I'll mark as ℹ️ note.

Let me finalize file:line references I've verified:
- Game.ts:1202-1203 (QuickMinecart tb), 1257-1258 (smartCursor field), 3801-3858 (updateSmartCursor), 4032-4040 (override), 4138 (extractinator range), 5094 (tryMine range tb=0), 5006-5016 (inTileRange), 5818 (wire tb=20), 5917 (tryPlaceWall), 5982/5979 (tryPlace), 6049-6064 (space check + support), 6187-6210 (overlapsEntity/hasSupport), 6287-6291 (interactAt range), 6293-6480 (right-click chain), 1366-1403 (key handlers), 3664-3688 (auto mana).
- SmartCursor.ts: 24-26, 101-105, 108-110, 124-140, 402-417, 449-486, 1677-1691 (tileRegion), 1694-1700, 1264-1356 (blocks filling/lines dead gate), 1358-1387 (paint no-op).
- SmartSelect.ts: 313-318 (tileBoost=20 comment), 227-264 (update).
- Options.ts: 11-14, 30-33.
- VUI.ts: 176-186.
- Renderer.ts: 3829, 3906-3950.
- Player.ts(entities): 251, 379.
- vanilla: Player.cs:2360-2366 (defaults), 12617-12621 (range acc), 14875-14878 (toolbelt), 9841-9845 (builder buff), 18510 (reset), 44967-45027 (mining range = IsTargetTileInItemRange), 45700-45702, 28344-28374 (toggle), 5268/5365/5453 (quick), 30576/30600/5798 (right-click/minecart no TB); TileReachCheckSettings.cs:28-62; SmartCursorHelper.cs:92-104 (TB chain), 117-156 (chain); TileObjectData.cs:2225-2254 (door), 3164-3174 (Style3x2 Origin(1,1)), 3448-3465 (Style2x2 chest Origin(0,1)); TileObject.cs:357 (overlap allowance), 186-188 (Origin); Main.cs:44753 (cursor), 66090, 4438-4440 (config defaults), 47360-47442 (DrawCursor).
- vanilla-accfx.json: 2215/3061/5126 tileRange:1 (line 701/803/1017).
- legacyItemIndex.generated.json: vi_407_Toolbelt at index 1651.

Wiki: Game_controls.md:57-61 (Ctrl smart cursor, R mount, H heal, J mana, B buff), Cursor_modes.md (behaviors), Architect_Gizmo_Pack.md / Hand_Of_Creation.md (+3/+2), Toolbelt.md (+1 placement only).

Wiki vs source check: Toolbelt.md says "+1 placement range, but not tool range" — matches source (blockRange++ placement-only). Architect Gizmo Pack wiki "by 2 tiles vertically and 3 tiles horizontally" — matches source. Wiki and source agree here; no 📄 items. 

One wiki discrepancy to check: Toolbox.md tooltip says "Increases block placement & tool range by 1" — but source has NO Toolbox entry (2214 = Brick Layer per code semantics tileSpeed+0.5). Hmm, actually is 2214 Toolbox or Brick Layer? Wiki Brick_Layer.md tooltip: "Increases tile placement speed" and Toolbox.md: "Increases block placement & tool range by 1". Vanilla code: 2214 → equippedAnyTileSpeedAcc (placement speed +50%), 2215 → equippedAnyTileRangeAcc (+3/+2). 

So if 2214=Brick Layer(速度) and 2215=Extendo Grip(射程+3/+2), the item IDs map cleanly to the four construction accessories: Brick Layer 2214, Extendo Grip 2215, Paint Sprayer 2216, Cement Mixer 2217. Then what is Toolbox? Toolbox would be a different ID (maybe 4004?). And the repo's accfx gives 2214 tileSpeed:1 (labeled tileSpeed in accfx) — consistent with Brick Layer. But wait, wiki Toolbox = "+1 placement & tool range" — which vanilla implements as... hmm, is there an item with tileRangeX+1/tileRangeY+1? Let me check! That's the Toolbox. Let me grep vanilla Player.cs for a smaller range increment.

Actually equippedAnyTileRangeAcc gives +3/+2 — one-shot bool, not stackable. Is there anything giving +1/+1? Let me check for "tileRangeX += 1" or Toolbox id.
````

</details>


---

## 🤖 Assistant · 2026-08-13T01:35:37.931Z · glm-x-preview-260804

```
查 Toolbox(工具箱)在原版是否有独立 +1 射程实现。
```


---

## 🤖 Assistant · 2026-08-13T01:35:38.787Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"tileRangeX +=\\|tileRangeY +=\" Player.cs; echo \"---Toolbox id search---\"; grep -rn \"Toolbox\" *.cs 2>/dev/null | head -3; grep -rn \"4004\\|4759\" Player.cs | grep -i \"tile\\|range\" | head -3",
 "description": "Find Toolbox range implementation in vanilla"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:35:38.878Z

**📎 ToolResult**

```
12620:			tileRangeX += 3;
12621:			tileRangeY += 2;
18642:					tileRangeX += 8;
18643:					tileRangeY += 8;
---Toolbox id search---

```


---

## 🤖 Assistant · 2026-08-13T01:35:40.965Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '18630,18650p' Player.cs",
 "description": "Read tileRangeX += 8 context"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:35:41.006Z

**📎 ToolResult**

```
		{
			equipmentBasedLuckBonus = 0f;
			luckPotion = 0;
			tileRangeX = DefaultTileRangeX;
			tileRangeY = DefaultTileRangeY;
			if (Main.IsJourneyMode)
			{
				CreativePowers.FarPlacementRangePower power = CreativePowerManager.Instance.GetPower<CreativePowers.FarPlacementRangePower>();
				if (power.GetIsUnlocked() && power.IsEnabledForPlayer(whoAmI))
				{
					tileRangeX *= 2;
					tileRangeY *= 2;
					tileRangeX += 8;
					tileRangeY += 8;
				}
			}
		}
		MinecartSettings = Minecart.Customization.Default;
		if (!isDisplayDollOrInanimate)
		{
			mount.CheckMountBuff(this);

```


---

## 🤖 Assistant · 2026-08-13T01:35:43.118Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Player.cs:18633-18646: Journey mode "FarPlacementRangePower" doubles tileRangeX/Y then +8/+8. Is this implemented? Let me check the repo for journey placement range.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:35:43.620Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"FarPlacement\\|farPlacement\\|tileRangeX \\*\\|journey.*range\\|PlacementRange\" ~/Project/GLM/SandboxWorld/game/src/ --include=\"*.ts\" | head -5",
 "description": "Check journey far placement range in repo"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:35:43.665Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T01:35:46.765Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Journey Mode "Increased Placement Range" power (tileRangeX*=2 then +8/+8, Player.cs:18640-18644) is NOT implemented. Also Toolbox — no vanilla implementation found for "+1/+1" (wiki says +1 placement & tool range; the only code paths are +3/+2 via equippedAnyTileRangeAcc). So the wiki's Toolbox claim of "+1" has no matching vanilla code path I found → that's a potential 📄 (wiki与源码不符) OR Toolbox uses a different mechanism. Let me search ItemID/Item.cs for Toolbox.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:35:47.702Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"Toolbox\\|ToolBelt\\|ExtendoGrip\\|BrickLayer\" ItemID.cs Lang.cs 2>/dev/null | head -8; grep -rn \"case 4716\\|== 4716\" Player.cs | head -2",
 "description": "Find construction accessory item IDs"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:35:47.762Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T01:35:50.460Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -o \"vi_221[0-9]_[A-Za-z_]*\\|vi_407_[A-Za-z_]*\" game/src/data/legacyItemIndex.generated.json | sort -u | head -8",
 "description": "Map accessory ids to names in repo data"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:35:50.530Z

**📎 ToolResult**

```
vi_2210_EbonwoodFence
vi_2211_RichMahoganyFence
vi_2212_PearlwoodFence
vi_2213_ShadewoodFence
vi_2214_BrickLayer
vi_2215_ExtendoGrip
vi_2216_PaintSprayer
vi_2217_PortableCementMixer

```


---

## 🤖 Assistant · 2026-08-13T01:35:53.810Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: 2214=BrickLayer, 2215=ExtendoGrip, 2216=PaintSprayer, 2217=PortableCementMixer. So the repo's accfx mapping is correct for these.

Toolbox: its ID must be elsewhere. The wiki says Toolbox gives +1 placement & tool range. Vanilla code has no such +1 path... unless Toolbox sets equippedAnyTileRangeAcc too? No — only 2215/3061/5126 set it. Hmm, wait — maybe Toolbox's "+1" is via a different field. Let me search Player.cs for all currentItem checks that could be Toolbox. Actually, let me just search the repo's accfx for toolbox id. Or check the wiki's Toolbox page internal ID.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:35:54.862Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -o \"vi_[0-9]*_Toolbox\" game/src/data/legacyItemIndex.generated.json | head -2; grep -rn -i \"toolbox\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | head -3; grep -rn -i \"ToolBox\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Item.cs 2>/dev/null | head -3",
 "description": "Find Toolbox id and vanilla handling"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:35:54.934Z

**📎 ToolResult**

```
vi_1923_Toolbox

```


---

## 🤖 Assistant · 2026-08-13T01:35:57.315Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Toolbox = item 1923, and there's NO handling of 1923 in vanilla Player.cs for range. So the wiki's Toolbox page claim "+1 block placement & tool range" is NOT implemented in vanilla 1.4.5.6 source → 📄 wiki与源码不符 (wiki says +1, source has no effect for 1923). Actually wait — let me double-check by searching for "1923" in Player.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:35:58.441Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && grep -n \"== 1923\\|1923\" Player.cs | head -5; echo \"---all cs---\"; grep -rn \"1923\" --include=\"*.cs\" . 2>/dev/null | grep -v \"Lang\\|ItemID\\|Main.cs:.*num\\|//\\|Texture\\|Recipe\\|SpawnNPC\" | head -5",
 "description": "Search 1923 Toolbox in all vanilla source"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:35:58.506Z

**📎 ToolResult**

```
6693:			QuickSpawnItem(itemSource_OpenItem, 1923);
14405:		if (whoAmI == Main.myPlayer && currentItem.type == 1923)
---all cs---
Item.cs:20835:		case 1923:
Player.cs:6693:			QuickSpawnItem(itemSource_OpenItem, 1923);
Player.cs:14405:		if (whoAmI == Main.myPlayer && currentItem.type == 1923)

```


---

## 🤖 Assistant · 2026-08-13T01:36:00.365Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria\" && sed -n '14403,14412p' Player.cs; echo \"===Item.cs 20833-20840===\"; sed -n '20833,20840p' Item.cs",
 "description": "Read Toolbox 1923 vanilla effect"
}
```


---

## 👤 User(sidechain) · 2026-08-13T01:36:00.431Z

**📎 ToolResult**

```
			magicCuffs = true;
		}
		if (whoAmI == Main.myPlayer && currentItem.type == 1923)
		{
			tileRangeX++;
			tileRangeY++;
		}
		if (currentItem.type == 1247)
		{
			starCloakItem = currentItem;
===Item.cs 20833-20840===
			maxStack = 1;
			return;
		case 1923:
			width = 16;
			height = 24;
			accessory = true;
			rare = 2;
			value = 50000;

```


---

## 🤖 Assistant · 2026-08-13T01:36:09.946Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent! Toolbox (1923) → `tileRangeX++; tileRangeY++` (Player.cs:14405-14408). So wiki is correct (+1 placement & tool range). And this affects mining AND placement AND right-click (it's tileRangeX/Y, not blockRange).

Is 1923 in the repo's accfx? Earlier the tileRange list was 2215/3061/5126 only — NOT 1923. So **Toolbox (vi_1923_Toolbox) is also missing its +1/+1 range effect**. Second missing range item. 

So the missing range items: vi_407_Toolbelt (blockRange+1, placement only) and vi_1923_Toolbox (tileRangeX/Y+1, all interactions).

And the Y-axis handling: vanilla has THREE sources into tileRangeX/Y: base 5/3 + Toolbox +1/+1 + Extendo Grip family +3/+2 (journey power separate). Implementation collapses everything to a single tb added equally to X and Y, and only on some paths.

Let me verify the journey power unlock default & whether the repo has journey placement range... already confirmed not implemented.

Now let me write the final report. Also let me quickly double check where Game.ts uses `equipStats.tileRange` — note equipStats.tileRange is a boolean flattened from fx.tileRange (Player.ts:379). And accfx 2215/3061/5126 = tileRange:1. Fine.

One more sanity check on #5 (Builder on right-click path). Actually let me reconsider: is Builder on right-click actually wrong? Vanilla right-click interact: Player.cs:30576/30600 (chest) — `IsInTileInteractionRange(chestX, chestY, TileReachCheckSettings.Simple)` no TB. But since tileRangeX/Y include Extendo Grip/Toolbox bonuses, right-click DOES get those. It does NOT get blockRange (Toolbelt/Builder). So implementation right-click: gets tileRange(+3, vanilla +3/+2) and Builder(+1, vanilla 0). Missing Toolbox. Verdict stands.

I think I've done enough verification. Let me also quickly note the smart select (Shift) is in-domain adjacent (it's Auto Select) — implemented 1:1.

Also for completeness, "开采优先级" (mining priority within smart cursor) ✅ chain order.

Report time. Format:
## 域:光标与方块交互
### 差异清单 (table)
### 覆盖清单
### 最需修复 TOP N

Keep it structured with file:line evidence. Mark ❓ for unverified claims. Let me count the checklist items coverage:
1. 交互距离 ✅ covered (#1-#6, journey power)
2. 智能光标 ✅ (#7-#13)
3. 放置对齐 ✅ (#14-#17)
4. 方块拾取/中键 ✅ (#18)
5. 快捷键链 ✅ (#19-#21)
6. 光标样式 ✅ (#22-#23)
7. 多格放置辅助 ✅ (#24)
8. 右键优先级 ✅ (#25)

Plus #26 Auto Select bonus, #27 联机.

Now write it.
```

</details>


---

## 🤖 Assistant · 2026-08-13T01:36:49.797Z · glm-x-preview-260804

```
核对完成,证据链齐全。以下为最终审计报告。

---

## 域:光标与方块交互

### 差异清单

| # | 机制项 | 原版设定(wiki页+数值) | 本仓库实现(file:line) | 状态 | 差异细节 |
|---|--------|----------------------|---------------------|------|---------|
| 1 | 基础交互距离 | tileRangeX=5/tileRangeY=3 默认(Player.cs:2360-2366),Simple 档 multiplier=1/上限 20(TileReachCheckSettings.cs:16-51) | Game.ts:5008-5016 `inTileRange` | ✅对齐 | 矩形判定非圆形,公式 1:1(`Math.min(20,5)+tb`) |
| 2 | 射程配饰轴向(Extendo Grip/Architect Gizmo Pack/Hand of Creation) | `equippedAnyTileRangeAcc → tileRangeX+=3 且 tileRangeY+=2`(Player.cs:12617-12621;wiki Architect_Gizmo_Pack.md "by 2 vertically and 3 horizontally") | Game.ts:1203/3820/4138/5917/5982/6291 `(tileRange?3:0)` 单值同时加 X/Y;inTileRange(Game.ts:5009-5010)x、y 共用同一 tb | ⚠️数值偏差 | Y 轴 +3(应 +2)→垂直多 1 格;根因是 tb 未拆 X/Y 两参数 |
| 3 | 挖掘距离 vs 射程配饰 | 挖掘=IsTargetTileInItemRange→Simple+tileBoost(Player.cs:44989/45700-45702),Simple 内含 tileRangeX/Y 静态值 → **配饰 +3/+2 对挖掘生效** | tryMine 传 tb=0(Game.ts:5094),且 inTileRange 硬编码 5/3 | ❌未实现 | 挖掘完全不吃射程配饰,水平少 3 格/垂直少 2 格 |
| 4 | 工具腰带 Toolbelt(407) | `currentItem.type==407 → blockRange++`(Player.cs:14875-14878),仅放置生效(wiki Toolbelt.md "+1 placement range, but not tool range") | vi_407_Toolbelt 存在(legacyItemIndex.generated.json 索引 1651)但 vanilla-accfx.json 无 407 键,equipStats 无 blockRange 字段 | ❌未实现 | 放置射程恒少 1 |
| 5 | 工具箱 Toolbox(1923) | `tileRangeX++/tileRangeY++`(Player.cs:14405-14408),全交互生效(wiki Toolbox.md "+1 placement & tool range") | vi_1923_Toolbox 存在,accfx 无该键 | ❌未实现 | 全交互射程少 1 |
| 6 | 建筑工药水 Builder(buff 107) | `blockRange++` + tileSpeed/wallSpeed+0.25(Player.cs:9841-9845),仅放置 | `p.buffs.has(BuffType.Builder)?1:0`(Game.ts:1203 等) | ⚠️数值偏差 | +1 本身对,但被并进 tb 同时加到 X/Y 且泄漏到右键交互(interactAt:6291)与 QuickMinecart(:1203);原版这两处为 Simple 无 TB(Player.cs:30576/30600/5798) |
| 7 | 放置 vs 挖掘 vs 使用物品距离分档 | 放置=tileBoost+blockRange(Player.cs:38939/39058/41140/46154);挖掘=tileBoost(Player.cs:44989);右键交互=Simple 无TB(30576) | tryPlace(Game.ts:5982)/tryPlaceWall(:5917)/提取机(:4138)用 tileRange+Builder;挖掘 :5094 tb=0;右键 :6291 含 tileRange+Builder | 🔀逻辑不同 | 分档方向对,但数值源混用同一 tb(见 #2/#4/#5) |
| 8 | 旅程模式远距放置 | Journey 解锁"FarPlacementRange":tileRangeX/Y *=2 再 +8/+8(Player.cs:18638-18644) | 全仓 grep 无 FarPlacement/journey range | ❌未实现 | 旅程世界放置射程不翻倍 |
| 9 | 智能光标开启规则 | LeftCtrl 切换(Game_controls.md:57);Toggle 默认(Main.cs:66090);可设 Hold;四设置项持久化(Main.cs:4438-4440) | ControlLeft/Right(Game.ts:3805)+updateWanted 1:1(SmartCursor.ts:402-417 对 Player.cs:28344-28374,含音效12);Options.ts:11-14/30-33;Settings.ts:261-272 | ✅对齐 | 状态机逐行对齐 |
| 10 | 智能光标默认值 | SmartBlocksEnabled/SmartAxeAfterPickaxe/SmartCursorHoldCanReleaseMidUse 均 `configuration.Get` 无默认=**false**(Main.cs:4438-4440;Player.cs:324-328) | Options.ts:32-33 smartBlocksEnabled/smartHoldCanReleaseMidUse 默认 **true** | ⚠️数值偏差 | 原版新档智能方块铺线默认**关**(BlocksLines 需该开关),本仓库默认**开** |
| 11 | 智能光标策略链(39 策略+顺序) | SmartCursorHelper.cs:117-156 | SmartCursor.ts:449-486 | ✅对齐 | 斧插入位(默认斧最优先)、让位集、方向锁、平台/轨道/锤/扳手/火把/橡实/宝石橡实等全 1:1 |
| 12 | 智能光标让位集(门/宝箱/床/开关等57项) | TileID.cs:205 DisableSmartCursor | SmartCursor.ts:24-26/101-105/1694-1700 | ✅对齐 | 含轨道 314 特例 |
| 13 | 智能光标搜索区 TB | `item.tileBoost + (createWall/createTile/tileWand>0 ? blockRange : 0)`(SmartCursorHelper.cs:95-98) | Game.ts:3816-3820 `placing?(tileRange+Builder):0`,**未加 item.tileBoost** | ⚠️数值偏差 | 扳手族 509/510 tileBoost=+20(SmartSelect.ts:313-318 自证)→智能光标扳手/剪线钳搜索区仅 5/3,而实际放置可达 20(Game.ts:5818)→远端导线无法被智能光标吸附 |
| 14 | 油漆三策略(PaintRoller/Brush/Scraper) | SmartCursorHelper.cs:668-807 | SmartCursor.ts:1358-1387 显式 no-op(油漆系统未建) | ❌未实现 | 注释标明恢复时机;依赖 tile paint 通道 |
| 15 | 多格放置锚点 | TileObjectData.Origin 逐物定义:Style3x2(桌/梳妆台)=**(1,1)**鼠标=底中(TileObjectData.cs:3164-3174);宝箱21=**(0,1)**鼠标=左下(:3448-3465);门10 备选 (0,0)/(0,1)/(0,2) 优先顶(:2225-2254);TileObject.cs:186-188 | tryPlace 一律左上锚(Game.ts:6049-6060,注释自认"鼠标指向顶部锚点") | 🔀逻辑不同 | 3×2 家具整体偏右 1 格+偏下 1 格、2×2 偏下 1 格;门恰好与首选备选一致,门不偏 |
| 16 | 放置与现有格重叠拒绝 | 仅拒 `active && !tileCut && !BreakableWhenPlacing`(TileObject.cs:357)→**允许压过草/藤/可割植物** | `if (st.isActive(px,py)) return` 全拒(Game.ts:6053) | 🔀逻辑不同 | 家具放不进长草地/藤蔓区(原版可压) |
| 17 | 放置支撑检查 | TileObjectData 全量锚点表(AnchorTop/Bottom/Side/Wall/AlternateTiles+Direction) | hasSupport 下/上/侧任一近似(Game.ts:6196-6210,注释自认"全量锚点表未提取") | ⚠️数值偏差 | 近似:悬空可放的(如某些贴墙物)与需实心底的会判错 |
| 18 | 斜坡/半砖上放置 | CanPlace 内含 half/slope 处理(TileObject.cs AnchorBottom 需平顶) | 空间检查未读 slope/half(Game.ts:6050-6056);仅锤击路径有 slope 逻辑(:5128-5150) | ❓存疑 | 需探针验证半砖顶放家具行为差异,静态读码未能定论 |
| 19 | 方块拾取/中键选取 | 原版**无**中键拾取方块;收藏=Alt+点击,快移=Shift(Game_controls.md:128) | Input.ts:52-61 仅 button 0/2,无中键 | ✅对齐 | 双方都无中键机制,无差异 |
| 20 | H 快速治疗 | H=Quick Heal,取"最契合"治疗品(治愈差最小/溢出最少)(Game_controls.md:59;Player.cs:5268-5363) | 键位表无 H(Game.ts:1366-1403);全仓 grep quickHeal 仅注释 | ❌未实现 | |
| 21 | J 快速魔力 | J=Quick Mana,取背包首个魔力药水(Game_controls.md:60;Player.cs:5365-5394) | 无;仅有魔力花族施法自动喝蓝(Game.ts:3664-3688) | ❌未实现 | 魔力花路径在,按键路径缺 |
| 22 | B 快速增益 | B=Quick Buff,喝全部增益/食物(Game_controls.md:61;Player.cs:5453-5650) | 无 | ❌未实现 | |
| 23 | R 快速坐骑 | R=Quick Mount(Game_controls.md:58;Player.cs:5728) | R 被占用为五彩扳手模式循环(Game.ts:1394-1407);QuickMount 缺,仅有 QuickMinecart 自研(:1196) | 🔀逻辑不同 | R 键语义冲突;矿车上车为近似实现(射程盒多算了 Builder+1,原版 :5798 无 TB) |
| 24 | 数字键武器槽 | Digit1-0 选热栏(Game_controls.md) | Game.ts:1366-1370 事件驱动,UI 打开时不切 | ✅对齐 | |
| 25 | 光标样式切换 | `SmartCursorIsUsed`(=Wanted,模式开着)即换 smart 指针(Main.cs:44753-44755,DrawCursor smart:true :47360) | 按 `sc.showing`(须有目标才换)(Game.ts:3858;VUI.ts:182) | 🔀逻辑不同 | 智能光标开着但无目标(指天空)时原版仍显示智能指针,本仓库回落普通指针 |
| 26 | 智能光标黄框+方向箭头 | Main.cs:46016-46066 DrawSmartCursor | Renderer.ts:3829-3950,含方向锁箭头与 smartCursorArrowAllowed 门(SmartCursor.ts:200-205) | ✅对齐 | |
| 27 | 多格连续放置辅助(BlocksLines/BlocksFilling) | SmartCursorHelper.cs:809-883/2692-2793,含原版死门(`SmartBlocksEnabled \|\|` 恒真) | SmartCursor.ts:1322-1356/1268-1319,死门 1:1 保留 | ✅对齐 | 但受 #10 默认值影响:本仓库默认就能铺线,原版默认不能 |
| 28 | 右键优先级链 | Player.cs:31707-32335 + SmartInteract(hover 区域) | interactAt(Game.ts:6287-6480):挂物族→提取机→bank→门→箱(3×3容差)→牌→墓碑→生命水晶→床→日晷/月晷→工位buff→拉杆/开关/计时器/起爆器→药草→八音盒/南瓜灯→喷泉→天塔柱族→派对纪念碑→蜥蜴祭坛→永恒水晶座→晶塔 | ✅对齐 | 各分支均带原版行号注释;门/箱按 tile 类型互斥,同格不可能双物,3×3 箱容差≈SmartInteract;⚠️右键射程门混入 Builder+1(见 #6) |
| 29 | 智能选取 Auto Select(Shift) | Player.cs:17259-17562 九策略 | SmartSelect.ts 全量 538 行,含水下光源/信号枪弹药门/叶绿兑换表 | ✅对齐 | 仓库内最高完成度子系统 |
| 30 | 联机距离 | 原版服务器不校验射程(msg17 直接落地),距离纯客户端 | 客户端 inTileRange + 房间保护 netCanEditTile(Game.ts:5979,自研) | ℹ️ | 自研保护为额外层,不与原版冲突 |

📄 **wiki 与源码不符项**:本域未发现。Toolbelt.md("+1 placement only")、Toolbox.md("+1 placement & tool range")、Architect_Gizmo_Pack.md("+3 横/+2 竖")均与 Player.cs:14875/14405/12618 逐条吻合。

### 覆盖清单

| 必核项 | 结论 |
|--------|------|
| 1 交互距离(默认+加成链+分档+联机) | 已核(#1-#8, #30)。加成链共四源:Toolbox(+1/+1 全交互)、Extendo Grip 族(+3/+2 全交互)、Toolbelt(+1 仅放置)、Builder(+1 仅放置);实现只建模了后两者的混合近似 |
| 2 智能光标(开启/吸附/平台门轨道/开采优先级) | 已核(#9-#14);策略链与让位集全 1:1,仅 TB 数值与油漆缺失 |
| 3 放置对齐(锚点/重叠拒绝/斜坡) | 已核(#15-#18);锚点与重叠拒绝为最大逻辑差 |
| 4 方块拾取/中键 | 已核(#19);双方皆无 |
| 5 快捷键 H/J/B/数字键 | 已核(#20-#24);H/J/B 全缺,R 被占 |
| 6 光标样式 | 已核(#25-#26) |
| 7 多格放置辅助 | 已核(#27) |
| 8 右键优先级链 | 已核(#28) |

### 最需修复 TOP 8

1. **#15 多格放置锚点**(Game.ts:6049-6060):提取 TileObjectData.Origin 表,Style3x2=(1,1)、宝箱=(0,1)——影响所有 3×2/2×2 家具落点,玩家可感知度最高。
2. **#4+#5 Toolbelt/Toolbox 射程缺失**(vanilla-accfx.json 补 407→blockRange、1923→tileRangeX/Y+1):纯数据层修复,成本低收益直接。
3. **#2+#3 射程 tb 拆 X/Y 并接入挖掘路径**(Game.ts:5009-5010/5094):把 5/3 基础值改成 `tileRangeX/tileRangeY` 实时值(含配饰),tb 仅承载 blockRange。
4. **#16 放置重叠拒绝放行 tileCut/BreakableWhenPlacing**(Game.ts:6053,SmartCursor.ts:64 已有该表可复用):一行条件的事,修掉"家具放不进草地"。
5. **#20-#22 H/J/B 快捷键**:QuickHeal 选品算法(Player.cs:5316-5363"最契合"规则)是三件里最复杂的,建议按 QuickBuff→QuickMana→QuickHeal 顺序补。
6. **#13 智能光标 TB 补 item.tileBoost**(Game.ts:3816-3820):扳手族 +20,否则远端导线智能光标失效。
7. **#10 智能光标默认值改 false**(Options.ts:32-33):对齐原版 configuration.Get 语义。
8. **#25 光标样式改按 wanted 而非 showing**(Game.ts:3858→`sc.wanted`):一处字段替换。

**总体评价**:SmartCursor.ts/SmartSelect.ts 是该仓库完成度最高的两个子系统(策略链、状态机、射线算法均 1:1 且注释带反编译行号);欠账集中在**射程加成链的数据建模**(tb 单值化吞掉了 X/Y 非对称与放置/全交互两档)和**放置端 TileObjectData 锚点/重叠语义**,以及 H/J/B 快捷键整族缺失。
```
