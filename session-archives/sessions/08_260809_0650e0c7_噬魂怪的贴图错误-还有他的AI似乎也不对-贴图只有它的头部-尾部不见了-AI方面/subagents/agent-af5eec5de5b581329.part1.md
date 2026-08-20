# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T04:08:31.976Z

```
调查 ~/Project/GLM/SandboxWorld/game/src/world/gen/ 的世界生成管线（搜索广度：very thorough）。目标：找出"生成早期往天空（y < groundLevel，地表以上）写入大量杂块、后期又被抹除"的来源。

需要回答：
1. `WorldGen.ts` `generateWorld` 的完整 pass 列表和执行顺序（含 lgcTerrain 分支差异）。哪些 pass 是 legacy 自有实现（terrainPass/cavePass/liquidPass/hellPass/potPass/surfacePass/structurePass/floatCleanupPass 等），哪些走 vanilla/ 目录的原版 1:1 pass（vanillaTerrain/vanillaCaches/vanillaBeaches/vanillaBiomes...）。注意 vanillaBiomes 内部又调用哪些 vanilla pass（给出顺序）。
2. 逐 pass 检查：哪些 pass 会在 y < groundLevel（天空区域）写 tile？特别注意：
   - legacy structurePass（buildHut/placeChest）的放置 y 范围
   - legacy surfacePass、potPass 的 y 范围
   - vanilla TreePass / FloatingIslandsPass / SurfaceDecorPass
   - halfBrickSmoothPass / waterfallLipPass（Smooth World）
   - vanilla CavesPass / TileRunner 是否会写到地表以上
   - liquidPass 在天空写水？
   - finalPass / finalize 做了什么"抹除"（比如清天空、floatCleanup）
3. 旧 fbm 地形回退（lgcTerrain=false）与原版地形两套管线的差异——legacy 管线是否会在天空生成杂块。
4. 记录关键文件与行号（generateWorld pass 数组、vanillaBiomes pass 链、finalPass/finalize 的清理逻辑）。

输出：pass 顺序完整清单（标注 legacy/vanilla），每个可能写天空的 pass 的 y 范围证据（文件:行号），以及 finalPass 里所有"清除/抹除"逻辑。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T04:08:31.978Z

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

## 🤖 Assistant · 2026-08-11T04:08:33.296Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a very thorough investigation of the world generation pipeline in ~/Project/GLM/SandboxWorld/game/src/world/gen/. Let me start by exploring the directory structure to understand the layout, then read WorldGen.ts and the vanilla passes.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:08:33.512Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src/world/gen -type f | sort",
 "description": "List all files in world gen directory"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:08:33.554Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/SeedEasterEggs.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CavesPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CleanupPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DirtToMudPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenState.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GrassPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HellFortPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HiveSpiderPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IceBiomePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IslandHousePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/JunglePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LakesPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MushroomPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/ShiniesPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/Spread.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SwordShrinePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TerrainPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TreePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGe
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts

```


---

## 🤖 Assistant · 2026-08-11T04:08:33.943Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/game/src/world/gen/ 2>/dev/null; wc -l ~/Project/GLM/SandboxWorld/game/src/world/gen/*.ts 2>/dev/null",
 "description": "List gen directory with file sizes"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:08:33.988Z

**📎 ToolResult**

```
total 144
drwxr-xr-x@  6 user  staff    192  8月 11 12:01 .
drwxr-xr-x@ 17 user  staff    544  8月 10 23:28 ..
-rw-r--r--@  1 user  staff   2365  8月 10 13:30 SeedEasterEggs.ts
drwxr-xr-x@ 31 user  staff    992  8月 11 11:51 vanilla
-rw-r--r--@  1 user  staff  17433  8月  6 00:30 WorldGe
-rw-r--r--@  1 user  staff  45781  8月 11 12:01 WorldGen.ts
      50 ~/Project/GLM/SandboxWorld/game/src/world/gen/SeedEasterEggs.ts
     974 ~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts
    1024 total

```


---

## 🤖 Assistant · 2026-08-11T04:08:35.432Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I'm in a read-only investigation task. Let me read WorldGen.ts fully and explore the vanilla directory. Note there's also a file "WorldGe" (odd truncated name). Let me read the main files.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:08:35.560Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:08:35.764Z

**📎 ToolResult**

```
1	// 程序化世界生成管线：地形 → 洞穴 → 矿石 → 液体 → 表面 → 结构
2	// 分帧执行以显示进度。纯函数式 pass，每个 pass 直接写 TileStore（生成期用 silent 写入）。
3	import { createNoise2D } from 'simplex-noise';
4	import { RNG, hashString } from '../../core/rng';
5	import { T, W, TILE_DEFS, TILE_BY_KEY } from '../../data/tiles';
6	import { World } from '../World';
7	
8	export interface GenConfig {
9	  width: number;
10	  height: number;
11	  seedText: string;
12	  name?: string;
13	  structures?: boolean;
14	  /** 邪恶群系：-1 随机（默认） 0 腐化 1 猩红（UIWorldCreation 对应原版 WorldGenParam_Evil） */
15	  evil?: -1 | 0 | 1;
16	  /** 每 pass 完成后回调部分世界（生成期实时地图预览用；无需等 finalize） */
17	  onWorldPartial?: (world: World, passIndex: number, passName: string) => void;
18	}
19	
20	export interface Pass {
21	  name: string;
22	  run: (ctx: GenCtx, report: (p: number) => void) => void;
23	}
24	
25	export interface GenCtx {
26	  world: World;
27	  store: World['store'];
28	  rng: RNG;
29	  noise2D: (x: number, y: number) => number;
30	  surface: Float32Array;   // 每列地表高度（tile y）
31	  cfg: GenConfig;
32	}
33	
34	/** 生成一个世界。passes 按序执行，每帧尽量做完一个 pass 后让出主线程。 */
35	export async function generateWorld(cfg: GenConfig, onProgress?: (label: string, p: number) => void): Promise<World> {
36	  const seed = hashString(cfg.seedText || String(Date.now()));
37	  const world = new World(cfg.width, cfg.height, seed, cfg.name ?? '新世界');
38	  const rng = new RNG(seed);
39	  const noise2D = createNoise2D(() => rng.next());
40	  const ctx: GenCtx = {
41	    world, store: world.store, rng, noise2D,
42	    surface: new Float32Array(cfg.width),
43	    cfg,
44	  };
45	
46	  // 原版管线:TerrainPass(五特征随机走) + TileRunner 泥石/洞穴;其余 pass 沿用
47	  // (lgcTerrain=false 走旧 fbm 地形作为回退开关)
48	  const useVanillaTerrain = (cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain !== false;
49	  const passes: Pass[] = [
50	    ...(useVanillaTerrain ? [
51	      { name: '原版地形', run: vanillaTerrain },
52	      { name: '洞穴', run: vanillaCaves },
53	      { name: '海滩', run: vanillaBeaches },
54	      { name: '生物群系', run: vanillaBiomes },
55	    ] as Pass[] : [
56	      { name: '地形', run: terrainPass },
57	      { name: '洞穴', run: cavePass },
58	    ]),
59	    // 原版注册序:Shinies(27) → Lakes(31) → Clean Up Dirt(37) → LifeCrystals(55)。
60	    // 生命水晶曾排在湖泊之前——湖泊 pass 挖湖盆会掏空已放水晶的脚下 → 凭空悬浮;
61	    // 清理(Clean Up Dirt)也须在矿石之后(原版 37>27,清理散块才知道哪些是散块)
62	    { name: '矿石', run: vanillaShinies },
63	    { name: '液体', run: vanillaLakes },
64	    ...(useVanillaTerrain ? [
65	      { name: '清理', run: vanillaCleanup },
66	      { name: '生命水晶', run: vanillaLifeCrystals },
67	    ] as Pass[] : []),
68	    ...(useVanillaTerrain ? [
69	      // 原版 "Smooth World"(L7568)+"Waterfalls"(L7697)：地表凸起与水边唇缘砸半砖
70	      // （半砖 = 原版水浸润/瀑布触发的核心，见 HalfBrickPass.ts）
71	      { name: '半砖平滑', run: halfBrickSmoothPass },
72	      { name: '瀑布唇缘', run: waterfallLipPass },
73	    ] as Pass[] : []),
74	    { name: '地狱', run: hellPass },
75	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [{ name: '清浮空', run: floatCleanupPass }] : []),
76	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '地狱屋', run: vanillaHellHouses }]),
77	    // 地狱箱:必须在地狱地形+地狱屋之后(原版 Underworld 29 < Buried Chests 59);
78	    // 曾在生物群系 pass 里随洞穴箱一起放 → 被后续 hellPass 重写 100% 抹除
79	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '地狱箱', run: underworldChestsPass }]),
80	    { name: '瓦罐', run: potPass },
81	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '矿骨堆', run: pilesPass }]),
82	    { name: '表面', run: surfacePass },
83	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '地表装饰', run: vanillaSurfaceDecor }]),
84	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '海滩装饰', run: vanillaBeachDecor }]),
85	    ...(cfg.structures === false ? [] : [{ name: '结构', run: structurePass }]),
86	  ];
87	
88	  for (let i = 0; i < passes.length; i++) {
89	    onProgress?.(passes[i].name, i / passes.length);
90	    await nextFrame();
91	    passes[i].run(ctx, () => {});
92	    // 部分世界回调（生成期实时预览）：pass 完成即暴露，不等 finalize
93	    if (cfg.onWorldPartial) cfg.onWorldPartial(world, i, passes[i].name);
94	  }
95	
96	  finalize(ctx);
97	  onProgress?.('完成', 1);
98	  return world;
99	}
100	
101	// ---------- 原版管线 pass(阶段 1-2 移植) ----------
102	import { newGenState, type GenState } from './vanilla/GenState';
103	import { runTerrainPass } from './vanilla/TerrainPass';
104	import { runRocksAndClayPass, runCavesPass } from './vanilla/CavesPass';
105	import { runOceanSandPass, runBeachesPass, runBeachDecorPass } from './vanilla/BeachPass';
106	import { runIceBiomePass, runSlushPass } from './vanilla/IceBiomePass';
107	import { runGrassPass } from './vanilla/GrassPass';
108	import { runJunglePass } from './vanilla/JunglePass';
109	import { spreadGrassAll } from './vanilla/Spread';
110	import { runDesertPass } from './vanilla/DesertPass';
111	import { runMushroomPass } from './vanilla/MushroomPass';
112	import { runMarbleGranitePass } from './vanilla/MarbleGranitePass';
113	import { runDirtToMudAndSiltPass } from './vanilla/DirtToMudPass';
114	import { runCleanupPass } from './vanilla/CleanupPass';
115	import { runSmoothWorldPass, runWaterfallLipPass } from './vanilla/HalfBrickPass';
116	import { runShiniesPass, runGemsPass } from './vanilla/ShiniesPass';
117	import { runMountCavesPass, runMountainCavesPass } from './vanilla/MountCavesPass';
118	import { runTreePass, randomizeTreeStyle } from './vanilla/TreePass';
119	import { runLakesPass } from './vanilla/LakesPass';
120	import { runTrapsPass } from './vanilla/TrapsPass';
121	import { runFloatingIslandsPass, runLifeCrystalsPass, runSurfaceDecorPass, runPyramidPass, runWetJunglePass } from './vanilla/StructuresPass';
122	import { runBeehivePass, runSpiderNestPass, runWebsInSpiderCavesPass, runWebsPass } from './vanilla/HiveSpiderPass';
123	import { tileRunner } from './vanilla/TileRunner';
124	import { runDungeonPass } from './vanilla/DungeonPass';
125	import { runTemplePass } from './vanilla/TemplePass';
126	import { runIslandHousePass } from './vanilla/IslandHousePass';
127	import { runHellFortPass } from './vanilla/HellFortPass';
128	import { runSwordShrinePass } from './vanilla/SwordShrinePass';
129	import { runBuriedChestsPass, runUnderworldChestsPass, runSurfaceChestsPass, runWaterChestsPass } from './vanilla/BuriedChestsPass';
130	import { runCorruptionPass } from './vanilla/CorruptionPass';
131	import { placeDoorClosed } from '../Door';
132	
133	function vanillaTerrain({ store, rng, world, surface, cfg }: GenCtx) {
134	  const gs = newGenState(store.w, store.h);
135	  // Reset pass 掷骰(WorldGen.cs L4780-4880,掷骰顺序 = RNG 契约不可调换)
136	  // 矿石替代对:Next(2)==0 → 替代矿(内部 id)
137	  gs.oreTiers = {
138	    copper: rng.next() < 0.5 ? TILE_BY_KEY['ore_tin']! : TILE_BY_KEY['ore_copper']!,
139	    iron: rng.next() < 0.5 ? TILE_BY_KEY['ore_lead']! : TILE_BY_KEY['ore_iron']!,
140	    silver: rng.next() < 0.5 ? TILE_BY_KEY['ore_tungsten']! : TILE_BY_KEY['ore_silver']!,
141	    gold: rng.next() < 0.5 ? TILE_BY_KEY['ore_platinum']! : TILE_BY_KEY['ore_gold']!,
142	  };
143	  gs.crimson = rng.next() < 0.5;
144	  // RandomizeTreeStyle（原版 Reset L4837：worldID 之后）——树冠样式与边界
145	  const ts = randomizeTreeStyle(rng, store.w);
146	  gs.treeX = ts.treeX;
147	  gs.treeStyle = ts.treeStyle;
148	  // 邪恶群系覆盖（RNG 契约：骰照掷，仅覆盖结果）
149	  if (cfg.evil === 0) gs.crimson = false;
150	  else if (cfg.evil === 1) gs.crimson = true;
151	  world.crimson = gs.crimson;
152	  gs.dungeonSide = rng.next() < 0.5 ? -1 : 1;
153	  // 丛林:与地牢异侧(Next(15,30) 即 15-29)
154	  const jf = rng.int(15, 29) * 0.01;
155	  gs.jungleX = Math.floor(store.w * (gs.dungeonSide === -1 ? 1 - jf : jf));
156	  world.jungleX = gs.jungleX;
157	  // 地牢 X:拒绝采样直到落在地牢侧 15% 区间
158	  let dX = rng.int(0, store.w - 1);
159	  const dLo = store.w * (gs.dungeonSide === 1 ? 0.60 : 0.25);
160	  const dHi = store.w * (gs.dungeonSide === 1 ? 0.75 : 0.40);
161	  while (dX < dLo || dX > dHi) dX = rng.int(0, store.w - 1);
162	  gs.dungeonX = dX;
163	  // 雪原:以地牢 X 为中心向两侧扩展(L4863-4879)——原版雪原与地牢同侧
164	  const snowScale = store.w / 4200;
165	  const snowExtend = () => rng.int(50, 89) + Math.floor(rng.int(20, 39) * snowScale) + Math.floor(rng.int(20, 39) * snowScale);
166	  gs.snowOriginLeft = Math.max(0, dX - snowExtend());
167	  gs.snowOriginRight = Math.min(store.w, dX + snowExtend());
168	  // 海滩宽度(原版固定 300-340+档位加成,按 4200 宽设计;小世界线性缩放保持比例)
169	  const beachRoll = () => Math.max(20, Math.floor(rng.int(300, 339) * snowScale));
170	  gs.beachLeftEnd = beachRoll() + (gs.dungeonSide === 1 ? 40 : 20) * (snowScale >= 1 ? 1 : Math.max(0.3, snowScale));
171	  gs.beachRightStart = store.w - beachRoll() - (gs.dungeonSide === -1 ? 40 : 20) * (snowScale >= 1 ? 1 : Math.max(0.3, snowScale));
172	  // 地牢入口(L4891-4894):地牢侧海滩内 15% 区间随机
173	  if (gs.dungeonSide === -1) {
174	    gs.dungeonLocation = rng.int(gs.beachLeftEnd + 50, Math.floor(store.w * 0.2));
175	  } else {
176	    gs.dungeonLocation = rng.int(Math.floor(store.w * 0.8), gs.beachRightStart - 50);
177	  }
178	  world.dungeonX = gs.dungeonLocation;
179	  // Terrain pass
180	  runTerrainPass(store, rng, gs);
181	  // surface 数组给后续旧 pass(surfacePass 树木等)用:每列首个实心行
182	  for (let x = 0; x < store.w; x++) {
183	    for (let y = 0; y < store.h; y++) {
184	      if (store.flags[store.idx(x, y)]) { surface[x] = y; break; }
185	    }
186	  }
187	  ctxGs[0] = gs;
188	  // 世界级常量同步
189	  world.groundLevel = gs.worldSurface;
190	  world.rockLevel = gs.rockLevel;
191	  world.lavaLine = gs.lavaLine;
192	}
193	
194	function vanillaLakes({ store, rng }: GenCtx) {
195	  // 原版 pass 31 Lakes + pass 36 Gems（cs 注册序 31<36）
196	  const gs = ctxGs[0];
197	  if (!gs) return;
198	  runLakesPass(store, rng, gs);
199	  runGemsPass(store, rng, gs);
200	}
201	
202	function vanillaShinies({ store, rng }: GenCtx) {
203	  // 原版 pass 27 Shinies（替换自研 orePass）
204	  const gs = ctxGs[0];
205	  if (!gs) return;
206	  runShiniesPass(store, rng, gs);
207	}
208	
209	function vanillaCaves({ store, rng }: GenCtx) {
210	  const gs = ctxGs[0];
211	  if (!gs) return;
212	  runOceanSandPass(store, rng, gs); // 原版 pass 3(顺序上先于泥石/洞穴)
213	  if (gs) runMountCavesPass(store, rng, gs); // 原版 pass 7 Mount Caves(山丘本体)
214	  runRocksAndClayPass(store, rng, gs);
215	  runCavesPass(store, rng, gs);
216	}
217	
218	function vanillaBeaches({ store, rng, surface }: GenCtx) {
219	  const gs = ctxGs[0];
220	  if (!gs) return;
221	  runMountainCavesPass(store, rng, gs); // 原版 pass 34 Mountain Caves(山侧开口+蜿蜒,先于海滩)
222	  runBeachesPass(store, rng, gs);
223	  // 海盆挖完后刷新 surface[](后续旧 pass 依赖)
224	  for (let x = 0; x < store.w; x++) {
225	    for (let y = 0; y < store.h; y++) {
226	      if (store.flags[store.idx(x, y)]) { surface[x] = y; break; }
227	    }
228	  }
229	}
230	
231	// 原版 pass 15-22:冰原→草种→丛林→泥转丛林草→沙漠→蘑菇→大理石/花岗岩
232	function vanillaBiomes({ store, rng, world }: GenCtx) {
233	  const gs = ctxGs[0];
234	  if (!gs) return;
235	  runIceBiomePass(store, rng, gs);       // 15 Generate Ice Biome
236	  runGrassPass(store, rng, gs);          // 16 Grass
237	  const jx = runJunglePass(store, rng, gs); // JunglePass
238	  world.jungleX = jx;
239	  // 丛林表面泥化:泥柱核心区 ±0.12w 内,表层 10 格 dirt→mud(原版巨型 runner
240	  // 覆盖表面所致;我们补这一步让丛林表面成草皮而非裸土)
241	  {
242	    const core = (gs as any).jungleCoreX ?? jx;
243	    const reach = Math.floor(store.w * 0.12);
244	    for (let x = Math.max(0, core - reach); x < Math.min(store.w, core + reach); x++) {
245	      let sy = 0;
246	      while (sy < store.h - 12 && !store.flags[store.idx(x, sy)]) sy++;
247	      for (let y = sy; y < sy + 10; y++) {
248	        if (store.get(x, y) === T.DIRT) store.setTileSilent(x, y, TILE_BY_KEY['mud']!);
249	      }
250	    }
251	  }
252	  spreadGrassAll(store, TILE_BY_KEY['mud']!, TILE_BY_KEY['v_60_jungle_grass_block']!, world.jungleX, Math.floor(store.w * 0.21)); // 17 Mud Caves To Grass(丛林核心区)
253	  runDesertPass(store, rng, gs);         // 18 Full Desert
254	  runFloatingIslandsPass(store, rng, gs); // 19 Floating Islands
255	  runMushroomPass(store, rng, gs);       // 20 Mushroom Patches
256	  runMarbleGranitePass(store, rng, gs);  // 21/22 Marble/Granite
257	  runDirtToMudAndSiltPass(store, rng, gs); // 23 Dirt To Mud / 24 Silt
258	  runSlushPass(store, gs);                 // 原版 pass 33 Slush（在 DirtToMud/Silt(25/26) 之后——泥已生成）
259	  runCorruptionPass(store, rng, gs);     // 28 Corruption/Crimson
260	  runDungeonPass(store, rng, gs, world.chests); // 30 Dungeon(蓝/粉砖主题+走廊房间+宝箱)
261	  // 地牢 pass 预计算会重掷 dungeonLocation(锚点 ±300 拒绝采样后迁移)——必须在此后
262	  // 回写最终位置,否则 world.dungeonX 停留在 Reset 期的旧值(与实际地牢偏差可达数百格)。
263	  // 优先取入口门厅可站立点(原版 dungeonX/Y 语义 cs L72510-72527:入口结构上可站处,
264	  // 守卫老人出生/游走锚)——塔心锚点会把老人漏进塔内
265	  world.dungeonX = gs.dungeonEntX || gs.dungeonLocation;
266	  world.dungeonY = gs.dungeonEntY || gs.dungeonY || 0;
267	  runPyramidPass(store, rng, gs, world.chests); // 38 Pyramids(沙岩砖金字塔+宝箱)
268	  runBuriedChestsPass(store, rng, gs, world.chests); // 59 Buried Chests(洞穴金/冰箱/沙箱;地狱箱已拆到地狱箱 pass)
269	  runSurfaceChestsPass(store, rng, gs, world.chests); // 36 Surface Chests(地表木箱)
270	  runWaterChestsPass(store, rng, gs, world.chests); // 39 Water Chests(水中 style17)
271	  runWetJunglePass(store, rng, gs);             // 43 Wet Jungle(丛林湿隧道灌水)
272	  runBeehivePass(store, rng, gs);               // 45 Hives(丛林蜂巢:蜂巢壳+蜂蜜+腔)
273	  runWebsPass(store, rng, gs);                  // 58 Webs(全局天花板蛛网 runner 51;原版序:Hives后/SpiderCaves前)
274	  runSpiderNestPass(store, rng, gs, world.chests); // 63 Spider Caves(countTiles 门+波前BFS刷墙62+蛛网罐/箱/垂网/覆饰)
275	  runWebsInSpiderCavesPass(store, rng, gs);     // 64 Webs In Spider Caves(墙62 9/10蛛网51)+蜂巢钟乳石/蜂蜜
276	  runTemplePass(store, rng, gs, world.chests);  // 44 Jungle Temple(之字形房间链+走廊+门+宝箱)
277	  runIslandHousePass(store, rng, gs, world.chests); // 浮空岛日光板房屋(Skyware 门+箱+桌椅)
278	  runSwordShrinePass(store, rng, gs);          // 附魔剑圣地(竖井+水潭洞+土丘剑)
279	}
280	
281	// 原版 pass 37 Clean Up Dirt:表层墙清理 + 连通小块(<20)清除
282	function vanillaCleanup({ store, rng }: GenCtx) {
283	  const gs = ctxGs[0];
284	  if (!gs) return;
285	  runCleanupPass(store, rng, gs);
286	}
287	
288	// 生命水晶(pass 55)——清完散块后放
289	function vanillaLifeCrystals({ store, rng }: GenCtx) {
290	  const gs = ctxGs[0];
291	  if (!gs) return;
292	  runLifeCrystalsPass(store, rng, gs);
293	}
294	
295	// 原版 "Smooth World"(L7568)：地表凸起 → 半砖/削除（HalfBrickPass）
296	function halfBrickSmoothPass({ store, rng }: GenCtx) {
297	  const gs = ctxGs[0];
298	  if (!gs) return;
299	  runSmoothWorldPass(store, rng, gs);
300	}
301	
302	// 原版 "Waterfalls"(L7697)：水边唇缘砸半砖（瀑布触发来源）
303	function waterfallLipPass({ store, rng }: GenCtx) {
304	  const gs = ctxGs[0];
305	  if (!gs) return;
306	  runWaterfallLipPass(store, rng, gs);
307	}
308	
309	// 地狱要塞 HellFort(5列×10行网格塔)——地狱层就绪后
310	function vanillaHellHouses({ store, rng }: GenCtx) {
311	  const gs = ctxGs[0];
312	  if (!gs) return;
313	  runHellFortPass(store, rng, gs);
314	}
315	
316	// 地狱箱(独立 pass,顺序见 passes 数组注释)
317	function underworldChestsPass({ store, rng, world }: GenCtx) {
318	  const gs = ctxGs[0];
319	  if (!gs) return;
320	  runUnderworldChestsPass(store, rng, gs, world.chests);
321	}
322	
323	// 矿/骨堆(原版 pass 77 Piles,cs:18928:w*0.06 次尝试,洞穴地面放小堆 185/骨堆 186)
324	function pilesPass({ store, rng }: GenCtx) {
325	  const { w, h } = store;
326	  const SMALL = TILE_BY_KEY['v_185_small_decos']!;
327	  const BONE = TILE_BY_KEY['v_186_decos_3x2']!;
328	  const tries = Math.floor(w * 0.06);
329	  let fail = 0;
330	  for (let n = 0; n < tries && fail < 10000; ) {
331	    const x = rng.int(20, w - 21);
332	    const y = rng.int(20, h - 20);
333	    // 落到第一个实心地面(与洞穴箱同式)
334	    let gy = y, guard = 0;
335	    while (guard++ < 400 && store.inBounds(x, gy) && !store.flags[store.idx(x, gy)]) gy++;
336	    if (!store.inBounds(x, gy) || !TILE_DEFS[store.type[store.idx(x, gy)]]?.solid) { fail++; continue; }
337	    const i = store.idx(x, gy - 1);
338	    if (!store.inBounds(x, gy - 1) || store.flags[i]) { fail++; continue; }
339	    if (store.liquid[i] > 100) { fail++; continue; }
340	    if (rng.next() < 0.7) {
341	      // 小堆 185:1×1,风格 ×18(fx 带 +18 偏移的下半帧;placeSmallPile size-0 语义)
342	      const style = rng.int(0, 9);
343	      store.setTileSilent(x, gy - 1, SMALL, style * 18, 0);
344	    } else {
345	      // 骨堆 186:3×2,风格 ×54(3 列 stride)
346	      let ok = true;
347	      for (let dx = 0; dx < 3 && ok; dx++) {
348	        for (let dy = 1; dy <= 2 && ok; dy++) {
349	          if (!store.inBounds(x + dx, gy - dy) || store.flags[store.idx(x + dx, gy - dy)]) ok = false;
350	        }
351	      }
352	      if (!ok) { fail++; continue; }
353	      const style = rng.int(0, 1);
354	      for (let dx = 0; dx < 3; dx++) {
355	        for (let dy = 0; dy < 2; dy++) {
356	          store.setTileSilent(x + dx, gy - 2 + dy, BONE, style * 54 + dx * 18, dy * 18);
357	        }
358	      }
359	    }
360	    n++;
361	  }
362	}
363	
364	// 生物群系感知地表装饰(替代旧 surfacePass 的种树部分)
365	function vanillaSurfaceDecor({ store, rng }: GenCtx) {
366	  const gs = ctxGs[0];
367	  if (!gs) return;
368	  runSurfaceDecorPass(store, rng, gs);
369	  runTrapsPass(store, rng, gs); // 原版 pass 76 Traps（返回 slot15 排查计数回归）
370	}
371	
372	// 海滩装饰：贝壳堆 + 海藻（原版 ShellPiles pass + GrowCheckSeaweed）
373	function vanillaBeachDecor({ store, rng }: GenCtx) {
374	  const gs = ctxGs[0];
375	  if (!gs) return;
376	  runBeachDecorPass(store, rng, gs);
377	}
378	
379	// 原版 pass 与旧 pass 的桥接存储(单次生成生命周期)
380	const ctxGs: [GenState | null] = [null];
381	/** 探针/测试用：最近一次生成的 GenState（山丘坐标等） */
382	export function lastGenState(): GenState | null { return ctxGs[0]; }
383	
384	function nextFrame(): Promise<void> {
385	  return new Promise((r) => setTimeout(r, 0));
386	}
387	
388	// ---------- 地形 ----------
389	function terrainPass({ store, surface, rng, cfg, noise2D }: GenCtx) {
390	  const { w, h } = store;
391	  const base = Math.floor(h * 0.28);
392	  // 多 octave 地表高度。平坦为主、偶发高峰：
393	  // 大势噪声幂次塑形（|v|^1.8）——噪声近 0 的大片区域被压平成平原，
394	  // 只有噪声较强处才隆起成峰；小起伏幅度减半避免处处尖刺
395	  const o1 = createNoise1Dish(rng, 0.012);
396	  const o2 = createNoise1Dish(rng, 0.05);
397	  const o3 = createNoise1Dish(rng, 0.11);
398	  for (let x = 0; x < w; x++) {
399	    const hill = (x > w * 0.18 && x < w * 0.82) ? 1 : 1.6; // 边缘更陡（近似海崖）
400	    const shape = (v: number, amp: number) => Math.sign(v) * Math.pow(Math.abs(v), 1.8) * amp;
401	    surface[x] = base + (shape(o1(x), 30) + o2(x) * 5 + o3(x) * 2) * hill;
402	  }
403	  // 左右海洋：最外侧 6% 下挖成海盆（岸边浅、世界缘深），后续灌水铺沙
404	  const oceanW = Math.max(24, Math.floor(w * 0.06));
405	  const seaLevel = base + 4; // 海平面（水表高度）
406	  for (let x = 0; x < w; x++) {
407	    const edge = Math.min(x, w - 1 - x);
408	    if (edge >= oceanW) continue;
409	    const t = 1 - edge / oceanW; // 0 岸边 → 1 世界缘
410	    const floorY = base + 2 + t * 16 + Math.sin(x * 0.3) * 1.5;
411	    surface[x] = Math.max(surface[x], Math.max(seaLevel + 2, floorY));
412	  }
413	  const rockLevel = Math.floor(h * 0.33);
414	  const nBlend = createNoise1Dish(rng, 0.05);
415	  for (let x = 0; x < w; x++) {
416	    const sy = Math.floor(surface[x]);
417	    // 每列岩石线带噪声起伏（±8 格），形成犬牙交错的土石过渡带
418	    const rl = rockLevel + nBlend(x) * 8;
419	    for (let y = 0; y < h; y++) {
420	      if (y < sy) continue;
421	      let type: number = T.DIRT;
422	      if (y >= rl) type = T.STONE;
423	      else if (y > rl - 14) {
424	        // 过渡带：噪声混入石块夹层
425	        if (fbm(noise2D, x * 0.09, y * 0.09, 2) > 0.12) type = T.STONE;
426	      }
427	      store.setTileSilent(x, y, type);
428	      // 自然墙：地下土/石区背景
429	      if (y > sy + 3) store.setWallSilent(x, y, type === T.STONE ? W.STONE : W.DIRT);
430	    }
431	  }
432	  // 海洋灌水 + 沙滩铺沙：海盆内从海平面灌满水；盆底与近岸滩涂表层铺沙
433	  for (let x = 0; x < w; x++) {
434	    const edge = Math.min(x, w - 1 - x);
435	    const sy = Math.floor(surface[x]);
436	    if (edge < oceanW) {
437	      for (let y = seaLevel; y < sy; y++) store.setLiquid(x, y, 255, 1);
438	      for (let y = sy; y < sy + 5 && y < store.h; y++) {
439	        const t = store.get(x, y);
440	        if (t === T.DIRT || t === T.GRASS) store.setTileSilent(x, y, T.SAND);
441	      }
442	    } else if (edge < oceanW + 8 && surface[x] >= seaLevel - 1) {
443	      // 近岸滩涂：海平面附近的陆地表面沙化过渡
444	      for (let y = sy; y < sy + 4 && y < store.h; y++) {
445	        const t = store.get(x, y);
446	        if (t === T.DIRT || t === T.GRASS) store.setTileSilent(x, y, T.SAND);
447	      }
448	    }
449	    // 沙漠地下层：海洋区沙层之下换沙岩/硬化沙（5-14 格深处随机夹层）
450	    if (edge < oceanW) {
451	      const SANDSTONE = TILE_BY_KEY['sandstone']!, HARDSAND = TILE_BY_KEY['hardened_sand']!;
452	      for (let y = sy + 5; y < sy + 14 && y < store.h; y++) {
453	        const t = store.get(x, y);
454	        if ((t === T.DIRT || t === T.STONE) && rng.next() < 0.45) {
455	          store.setTileSilent(x, y, y < sy + 9 ? SANDSTONE : HARDSAND);
456	        }
457	      }
458	    }
459	  }
460	  // 雪原带：随机一侧的 10%-24% 区间 —— 地表雪化 + 浅层冰夹层（无树：surfacePass 只在草上种树）
461	  {
462	    const ICE = TILE_BY_KEY['ice']!;
463	    const snowLeft = rng.next() < 0.5;
464	    const xs0 = snowLeft ? Math.floor(w * 0.10) : Math.floor(w * 0.76);
465	    const xs1 = snowLeft ? Math.floor(w * 0.24) : Math.floor(w * 0.90);
466	    for (let x = xs0; x <= xs1; x++) {
467	      const sy = Math.floor(surface[x]);
468	      for (let y = sy; y < sy + 4 && y < store.h; y++) {
469	        const t = store.get(x, y);
470	        if (t === T.GRASS || t === T.DIRT) store.setTileSilent(x, y, T.SNOW);
471	      }
472	      for (let y = sy + 4; y < sy + 12 && y < store.h; y++) {
473	        if (store.get(x, y) === T.DIRT && rng.next() < 0.45) store.setTileSilent(x, y, ICE);
474	      }
475	    }
476	  }
477	  // 世界最底部 3 行基岩（不可破坏 → 用 STONE 代替，破坏规则由硬度统一处理，简化）
478	}
479	
480	// 伪 1D 噪声：借用 2D 噪声 y=0
481	function createNoise1Dish(rng: RNG, freq: number) {
482	  const n = createNoise2D(() => rng.next());
483	  return (x: number) => n(x * freq, 0);
484	}
485	
486	// ---------- 洞穴 ----------
487	function cavePass({ store, surface, noise2D, rng, cfg }: GenCtx) {
488	  const { w, h } = store;
489	  // 1) 噪声挖空（海洋列跳过：保护海床，防止海水灌进洞穴系统）
490	  const caveOceanW = Math.max(24, Math.floor(w * 0.06)) + 2;
491	  for (let x = 0; x < w; x++) {
492	    if (Math.min(x, w - 1 - x) < caveOceanW) continue;
493	    const sy = surface[x];
494	    for (let y = Math.floor(sy) + 6; y < h - 3; y++) {
495	      const depth = (y - sy) / (h - sy);
496	      const threshold = 0.30 - depth * 0.06; // 越深洞越多
497	      const v = fbm(noise2D, x * 0.028, y * 0.028, 3);
498	      if (v > threshold) store.setTileSilent(x, y, 0);
499	    }
500	  }
501	  // 2) 蠕虫隧道（连通大洞穴）
502	  const worms = 16 + Math.floor(rng.range(0, 8));
503	  for (let i = 0; i < worms; i++) {
504	    let wx = rng.range(w * 0.08, w * 0.92);
505	    let wy = rng.range(h * 0.35, h * 0.92);
506	    let angle = rng.range(0, Math.PI * 2);
507	    const len = rng.int(60, 200);
508	    for (let s = 0; s < len; s++) {
509	      angle += (noise2D(s * 0.05, i * 10) * 0.6 + rng.range(-0.3, 0.3));
510	      wx += Math.cos(angle) * 1.2;
511	      wy += Math.sin(angle) * 0.8;
512	      if (wx < 4 || wx > w - 5 || wy < h * 0.25 || wy > h - 6) break;
513	      const r = 2.2 + noise2D(s * 0.03, i * 5) * 1.8;
514	      carveCircle(store, wx, wy, Math.max(1.2, r));
515	    }
516	  }
517	}
518	
519	function carveCircle(store: GenCtx['store'], cx: number, cy: number, r: number) {
520	  const x0 = Math.floor(cx - r), x1 = Math.ceil(cx + r);
521	  const y0 = Math.floor(cy - r), y1 = Math.ceil(cy + r);
522	  for (let x = x0; x <= x1; x++) {
523	    for (let y = y0; y <= y1; y++) {
524	      if (!store.inBounds(x, y)) continue;
525	      const dx = x - cx, dy = y - cy;
526	      if (dx * dx + dy * dy <= r * r) store.setTileSilent(x, y, 0);
527	    }
528	  }
529	}
530	
531	function fbm(n2: (x: number, y: number) => number, x: number, y: number, oct: number): number {
532	  let v = 0, amp = 1, freq = 1, norm = 0;
533	  for (let i = 0; i < oct; i++) {
534	    v += n2(x * freq, y * freq) * amp;
535	    norm += amp;
536	    amp *= 0.5; freq *= 2;
537	  }
538	  return v / norm; // -1..1
539	}
540	
541	// ---------- 地狱层(原版 Underworld pass,L5952,完整) ----------
542	// 1) 边界随机走(h-190..h-160),界上~20格灰烬,界下清空;
543	// 2) 岩浆线随机走(h-120..h-60),线以下空气灌岩浆;
544	// 3) 大灰烬丘陵(addTile 填充虚空)+ 横向灰烬团 + 挖掘隧道(填岩浆);
545	// 4) 底部 h-145/144 岩浆层 + 地狱石 58 矿脉
546	function hellPass({ store, rng }: GenCtx) {
547	  const st = store;
548	  const ASH = T.ASH;
549	  const HELLSTONE = TILE_BY_KEY['ore_hellstone']!;
550	  // 1) 边界 + 灰烬带 + 界下清空
551	  let boundary = st.h - rng.int(150, 189);
552	  for (let x = 0; x < st.w; x++) {
553	    boundary += rng.int(-3, 3);
554	    if (boundary < st.h - 190) boundary = st.h - 190;
555	    if (boundary > st.h - 160) boundary = st.h - 160;
556	    const ashTop = boundary - 20 - rng.int(0, 2);
557	    for (let y = ashTop; y < st.h; y++) {
558	      const i = st.idx(x, y);
559	      if (y >= boundary) {
560	        st.type[i] = 0; st.flags[i] = 0;
561	        st.liquid[i] = 0; st.liquidType[i] = 0;
562	      } else {
563	        st.type[i] = ASH; st.flags[i] = 1;
564	        st.wall[i] = 1;
565	      }
566	    }
567	  }
568	  // 2) 岩浆线
569	  let lavaY = st.h - rng.int(40, 69);
570	  for (let x = 10; x < st.w - 10; x++) {
571	    lavaY += rng.int(-10, 10);
572	    if (lavaY > st.h - 60) lavaY = st.h - 60;
573	    if (lavaY < st.h - 100) lavaY = st.h - 120;
574	    for (let y = lavaY; y < st.h - 10; y++) {
575	      const i = st.idx(x, y);
576	      if (!st.flags[i]) { st.liquid[i] = 255; st.liquidType[i] = 2; }
577	    }
578	  }
579	  const gs = ctxGs[0]!;
580	  // 3a) 大灰烬丘陵(1/50 列):巨型竖直灰烬 runner 填充虚空
581	  for (let x = 0; x < st.w; x++) {
582	    if (rng.next() * 50 >= 1) continue;
583	    let y = st.h - 65;
584	    while (!st.flags[st.idx(x, y)] && y > st.h - 135) y--;
585	    tileRunnerHell(st, rng, gs, rng.int(0, st.w - 1), y + rng.int(20, 49),
586	      rng.int(15, 19), 1000, ASH, true, 0, rng.int(1, 2), true);
587	  }
588	  // 3b) 每列 1/13:竖直灰烬柱 + 横向灰烬团 + 挖掘隧道(填岩浆)
589	  for (let x = 0; x < st.w; x++) {
590	    if (rng.next() * 13 >= 1) continue;
591	    let y = st.h - 65;
592	    while ((st.liquid[st.idx(x, y)] > 0 || st.flags[st.idx(x, y)]) && y > st.h - 140) y--;
593	    let scaleF = rng.int(1, 2);
594	    if (rng.next() * 3 < 1) scaleF *= 0.5;
595	    tileRunnerHell(st, rng, gs, x, y - rng.int(2, 4), rng.int(5, 29), 1000, ASH, true, 0, rng.int(1, 2), true);
596	    if (rng.next() < 0.5) {
597	      tileRunnerHell(st, rng, gs, x, y - rng.int(2, 4), Math.floor(rng.int(5, 14) * scaleF), Math.floor(rng.int(10, 14) * scaleF), ASH, true, 1, 0.3, false);
598	    }
599	    if (rng.next() < 0.5) {
600	      const s2 = rng.int(1, 2);
601	      tileRunnerHell(st, rng, gs, x, y - rng.int(2, 4), Math.floor(rng.int(5, 14) * s2), Math.floor(rng.int(10, 14) * s2), ASH, true, -1, 0.3, false);
602	    }
603	    tileRunnerHell(st, rng, gs, x + rng.int(-10, 9), y + rng.int(-10, 10), rng.int(5, 14), rng.int(5, 9), -2, false, rng.int(-1, 2), rng.int(-1, 2), false);
604	    if (rng.next() * 3 < 1) {
605	      tileRunnerHell(st, rng, gs, x + rng.int(-10, 9), y + rng.int(-10, 10), rng.int(10, 29), rng.int(10, 19), -2, false, rng.int(-1, 2), rng.int(-1, 2), false);
606	    }
607	    if (rng.next() * 5 < 1) {
608	      tileRunnerHell(st, rng, gs, x + rng.int(-15, 14), y + rng.int(-15, 9), rng.int(15, 29), rng.int(5, 19), -2, false, rng.int(-1, 2), rng.int(-1, 2), false);
609	    }
610	  }
611	  // 3c) 随机小挖掘(w 个)
612	  for (let n = 0; n < st.w; n++) {
613	    tileRunnerHell(st, rng, gs, rng.int(20, st.w - 21), rng.int(st.h - 180, st.h - 11),
614	      rng.int(2, 6), rng.int(2, 6), -2, false, 0, 0, false);
615	  }
616	  // 4) 底部岩浆层(h-145/144)+ 地狱石脉
617	  for (let x = 0; x < st.w; x++) {
618	    for (const dy of [145, 144]) {
619	      const i = st.idx(x, st.h - dy);
620	      if (!st.flags[i]) { st.liquid[i] = 255; st.liquidType[i] = 2; }
621	    }
622	  }
623	  for (let n = 0; n < st.w * st.h * 0.0008; n++) {
624	    tileRunnerHell(st, rng, gs, rng.int(0, st.w - 1), rng.int(st.h - 140, st.h - 1),
625	      rng.int(2, 6), rng.int(3, 6), HELLSTONE, false, 0, 0, false);
626	  }
627	}
628	
629	/** 地狱专用 runner:超界安全(地狱区常越界) */
630	function tileRunnerHell(st: World['store'], rng: RNG, gs: GenState, i: number, j: number,
631	  strength: number, steps: number, type: number, addTile: boolean,
632	  speedX: number, speedY: number, noYChange: boolean): void {
633	  tileRunner(st, rng, gs, i, Math.max(2, Math.min(st.h - 3, j)), {
634	    strength, steps, type, addTile, speedX, speedY, noYChange,
635	  });
636	}
637	
638	// ---------- 浮空方块清理 ----------
639	// 迭代剥离无支撑的孤立土/石块（下方三格全空且左右也空 → 移除），重复数次处理小簇
640	function floatCleanupPass({ store, surface }: GenCtx) {
641	  const st = store;
642	  for (let iter = 0; iter < 4; iter++) {
643	    let removed = 0;
644	    for (let x = 2; x < st.w - 2; x++) {
645	      const surfY = Math.floor(surface[x]);
646	      for (let y = surfY + 2; y < st.h - 2; y++) {
647	        const t = st.get(x, y);
648	        if (t !== T.DIRT && t !== T.STONE && t !== T.GRASS) continue;
649	        const below = st.isSolid(x, y + 1) || st.isSolid(x - 1, y + 1) || st.isSolid(x + 1, y + 1);
650	        const beside = st.isSolid(x - 1, y) || st.isSolid(x + 1, y);
651	        const above = st.isSolid(x, y - 1);
652	        if (!below && !beside && !above) {
653	          st.setTileSilent(x, y, 0);
654	          removed++;
655	        }
656	      }
657	    }
658	    if (removed === 0) break;
659	  }
660	}
661	
662	// ---------- 瓦罐散布 ----------
663	function potPass({ store, surface, rng }: GenCtx) {
664	  // 原版 Pots pass(1.4.5.6 WorldGen.cs:18186-18286)1:1:
665	  // count = 面积×0.0008(小 4200×1200 = 4032 个),每个成功点放 1 罐;
666	  // 进度 >75% 强制从地表浅层起扫、>93% 强制地狱行;2 宽×2 高 PlacePot
667	  // (cs:54082:frameX = k*18 + 变体*36、frameY = (l+1)*18 + style*36);
668	  // 样式按地面 tile/墙(冰雪 4-6/丛林草 7-9/地牢 10-12/腐化 16-18/猩红 22-24/
669	  // 花岗岩 31-33/蜥蜴砖 28-30/大理石墙 34-36/地狱 13-15/默认 0-3)。
670	  // 旧实现 w/6 次尝试+12 格排斥 → 只有原版 ~5%
671	  const gs = ctxGs[0];
672	  if (!gs) return;
673	  const { w, h } = store;
674	  const POT = TILE_BY_KEY['pot']!;
675	  const count = Math.floor(w * h * 0.0008);
676	  const surfHigh = Math.max(1, Math.floor(gs.worldSurfaceHigh));
677	  const surfLow = Math.floor(gs.worldSurfaceLow);
678	
679	  const SNOW = TILE_BY_KEY['snow']!, ICE = TILE_BY_KEY['ice']!, THIN_ICE = TILE_BY_KEY['thin_ice']!;
680	  const JUNGLE = TILE_BY_KEY['v_60_jungle_grass_block']!;
681	  const CORRUPT = new Set<number>([
682	    TILE_BY_KEY['v_23_corrupt_grass_block']!, TILE_BY_KEY['v_112_ebonsand_block']!,
683	    TILE_BY_KEY['v_116_pearlsand_block']!, TILE_BY_KEY['v_163_corrupt_ice_block']!,
684	  ].filter((v) => v !== undefined));
685	  const CRIMSON = new Set<number>([
686	    TILE_BY_KEY['v_199_crimson_grass_block']!, TILE_BY_KEY['v_203_crimstone_block']!,
687	    TILE_BY_KEY['v_204_crimsand_block']!, TILE_BY_KEY['v_200_crimson_ice_block']!,
688	  ].filter((v) => v !== undefined));
689	  const GRANITE = TILE_BY_KEY['v_368_granite_block'] ?? -1; // 368 = 花岗岩块
690	  const MARBLE = TILE_BY_KEY['v_367_marble_block'] ?? -1;    // 367 = 大理石块(样式由墙 187/216/223 判定,MARBLE 仅保留)
691	  const LIHZARD = TILE_BY_KEY['v_226_lihzahrd_brick'] ?? -1;
692	  const DUNGEON_WALLS = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
693	  const MARBLE_WALLS = new Set([187, 216, 223]);
694	
695	  /** cs:18220-18272 样式选择(按地面 tile / 墙 / 深度) */
696	  const potStyle = (x: number, y: number, ground: number, wall: number): number => {
697	    if (ground === SNOW || ground === ICE || ground === THIN_ICE) return rng.int(4, 6);
698	    if (ground === JUNGLE) return rng.int(7, 9);
699	    if (DUNGEON_WALLS.has(wall)) return rng.int(10, 12);
700	    if (CORRUPT.has(ground)) return rng.int(16, 18);
701	    if (CRIMSON.has(ground)) return rng.int(22, 24);
702	    if (ground === GRANITE) return rng.int(31, 33);
703	    if (ground === LIHZARD) return rng.int(28, 30);
704	    if (MARBLE_WALLS.has(wall)) return rng.int(34, 36);
705	    if (y > gs.rockLevel && y > h - 260) return rng.int(13, 15); // 地狱(cs: UnderworldLayer)
706	    return rng.int(0, 3);
707	  };
708	
709	  for (let n = 0; n < count; ) {
710	    const progress = n / count;
711	    let y0 = rng.int(surfHigh, Math.max(surfHigh + 1, h - 10));
712	    if (progress > 0.93) y0 = h - 150;          // 尾段强制地狱行(cs:18194)
713	    else if (progress > 0.75) y0 = surfLow;     // 后 1/4 起地表浅层(cs:18196)
714	    const x = rng.int(20, w - 20);
715	    // 向下扫描(cs:18210-18286):遇首个实心后进入候选模式,
716	    // 在满足"地表以下或背面有墙"的空腔地面放(2×2 净空+双列实心,PlacePot cs:54082)
717	    let foundSolid = false;
718	    let fail = true;
719	    for (let y = y0; y < h - 20 && fail; y++) {
720	      const t = store.get(x, y);
721	      if (!foundSolid) {
722	        if (t !== 0 && TILE_DEFS[t]?.solid && !store.liquid[store.idx(x, y - 1)]) foundSolid = true;
723	        continue;
724	      }
725	      if (y < surfLow && store.wall[store.idx(x, y)] === 0) continue; // cs:18216 地表上方需有墙
726	      const ground = store.get(x, y + 1);
727	      if (ground === 0 || !TILE_DEFS[ground]?.solid) continue;
728	      if (store.liquid[store.idx(x, y)] > 0) continue;
729	      // PlacePot 2×2 净空 + (x,y+1)(x+1,y+1) 实心 + 半砖/坡面检查(本仓库半砖简化跳过)
730	      let ok = true;
731	      for (let dx = 0; dx < 2 && ok; dx++) {
732	        for (let dy = -1; dy <= 0; dy++) {
733	          if (store.isActive(x + dx, y + dy)) ok = false;
734	        }
735	        if (!store.isSolid(x + dx, y + 1)) ok = false;
736	      }
737	      if (!ok) continue;
738	      const style = potStyle(x, y, ground, store.wall[store.idx(x, y)]);
739	      const variant = rng.int(0, 2) * 36;
740	      for (let dx = 0; dx < 2; dx++) {
741	        for (let dy = -1; dy <= 0; dy++) {
742	          store.setTileSilent(x + dx, y + dy, POT, dx * 18 + variant, (dy + 1) * 18 + style * 36);
743	        }
744	      }
745	      fail = false;
746	    }
747	    n++; // 原版每轮无论成败都推进 num8(10000 次失败预算内重试,这里简化为固定轮数)
748	  }
749	}
750	
751	// ---------- 矿石 ----------
752	// 已由 vanilla/ShiniesPass.ts（原版 pass 27/36）整体替换，旧 orePass/growOreBlob 删除
753	
754	// ---------- 液体 ----------
755	// 已由 vanilla/LakesPass.ts（原版 pass 31）替换，旧 liquidPass 删除
756	
757	// ---------- 表面 ----------
758	function surfacePass({ store, surface, rng, world }: GenCtx) {
759	  const { w } = store;
760	  // 铺草（原版 pass 73 Spreading Grass 尾段 L8731-8755：每列首个实心格为泥土 → SpreadGrass）
761	  // 旧实现用生成早期 surface[] 数组定位列顶——山坡/洞穴口露石露土全漏，树密度被卡死
762	  for (let x = 10; x < w - 10; x++) {
763	    for (let y = 0; y < world.groundLevel - 1; y++) {
764	      const i = store.idx(x, y);
765	      if (!store.flags[i]) continue;
766	      if (store.type[i] === T.DIRT) store.setTileSilent(x, y, T.GRASS);
767	      break; // 只处理首个实心格
768	    }
769	  }
770	  // 原版 pass 82 Planting Trees（铺草之后、杂草之前——原版 73<82<86 顺序）
771	  {
772	    const gs = ctxGs[0];
773	    if (gs) runTreePass(store, rng, gs);
774	  }
775	  // 地表植物装饰——原版 pass GrassPlantsEvilPlantsAndPumpkinsOnSurface（WorldGen.cs:20201-20266）+
776	  // PlaceTile 液体拒绝（WorldGen.cs:59477：tile 3/24/201/637 在液体中不放）。
777	  // 门禁 1:1：只铺在草族 tile 上方（普通草 2→tile 3 / 腐化草 23→24 / 猩红草 199→201 /
778	  // 丛林草 60→73 / 蘑菇草 70→71 发光蘑菇株）；沙滩/海水自然无杂草。
779	  {
780	    const CORRUPT_GRASS = TILE_BY_KEY['v_23_corrupt_grass_block'] ?? 0;
781	    const CRIMSON_GRASS = TILE_BY_KEY['v_199_crimson_grass_block'] ?? 0;
782	    const JUNGLE_GRASS = TILE_BY_KEY['v_60_jungle_grass_block'] ?? 0;
783	    const MUSH_GRASS = TILE_BY_KEY['v_70_mushroom_grass_block'] ?? 0;
784	    const CORRUPT_PLANTS = TILE_BY_KEY['v_24_corruption_short_plants'] ?? 0;
785	    const CRIMSON_PLANTS = TILE_BY_KEY['v_201_crimson_short_plants'] ?? 0;
786	    const JUNGLE_PLANTS = TILE_BY_KEY['v_73_forest_tall_plants'] ?? 0;
787	    const GLOW_SHROOM = TILE_BY_KEY['v_71_mushroom_plant'] ?? 0;
788	    const CORRUPT_THORNS = TILE_BY_KEY['v_32_corruption_thorns'] ?? 0;
789	    const CRIMSON_THORNS = TILE_BY_KEY['v_352_crimtane_thorns'] ?? 0;
790	    const GRASS_FX = [0, 18, 36, 54, 72, 90];
791	    const FLOWER_FX = [108, 126, 162, 180, 216, 252, 342, 540, 594];
792	    const plantAbove = (x: number, y: number, type: number, fx: number) => {
793	      if (y < 1 || !store.inBounds(x, y)) return;
794	      const i = store.idx(x, y);
795	      if (store.flags[i] || store.liquid[i] > 0) return; // 上方格须空气且无液体
796	      store.setTileSilent(x, y, type, fx, 0);
797	    };
798	    for (let x = 0; x < w; x++) {
799	      for (let y = 1; y < store.h; y++) {
800	        const bi = store.idx(x, y);
801	        if (!store.flags[bi]) continue;
802	        const below = store.type[bi];
803	        if (below === T.GRASS) {
804	          // 普通草：每格必铺（原版语义），变体 = 草丛 6 / 花 9 / 蘑菇(144)
805	          const r = rng.next();
806	          if (r < 0.82) plantAbove(x, y - 1, T.TALLGRASS, GRASS_FX[Math.floor(rng.next() * 6)]);
807	          else if (r < 0.97) plantAbove(x, y - 1, T.FLOWER, FLOWER_FX[Math.floor(rng.next() * 9)]);
808	          else plantAbove(x, y - 1, T.MUSHROOM, 144);
809	        } else if (below === CORRUPT_GRASS) {
810	          // 腐化草 13% → 荆棘 32（原版 IsFitToPlaceFlowerIn 分支）；帧 144 = 邪恶蘑菇
811	          if (rng.next() < 0.13 && CORRUPT_THORNS) plantAbove(x, y - 1, CORRUPT_THORNS, 0);
812	          else plantAbove(x, y - 1, CORRUPT_PLANTS, rng.next() < 0.08 ? 144 : Math.floor(rng.next() * 6) * 18);
813	        } else if (below === CRIMSON_GRASS) {
814	          if (rng.next() < 0.13 && CRIMSON_THORNS) plantAbove(x, y - 1, CRIMSON_THORNS, 0);
815	          else plantAbove(x, y - 1, CRIMSON_PLANTS, Math.floor(rng.next() * 11) * 18);
816	        } else if (below === JUNGLE_GRASS) {
817	          plantAbove(x, y - 1, JUNGLE_PLANTS, Math.floor(rng.next() * 6) * 18);
818	        } else if (below === MUSH_GRASS && GLOW_SHROOM) {
819	          // 蘑菇草 → 发光蘑菇株（v_71 5 变体；GlowingMushroomPlants pass 语义）
820	          plantAbove(x, y - 1, GLOW_SHROOM, Math.floor(rng.next() * 5) * 18);
821	        }
822	      }
823	    }
824	  }
825	  // 树已由 vanilla/TreePass.ts（原版 pass 82 AddTrees/GrowTree/GrowPalmTree/GrowEpicTree）替换
826	}
827	
828	// ---------- 结构（地下小屋 + 宝箱） ----------
829	function placeChest(store: GenCtx['store'], x: number, y: number) {
830	  // 2×2 宝箱 object（锚点在左上）。帧 = 18px 像素步长（原版 TileObject.Place 语义）——
831	  // 此前误写格索引(0/1)，渲染端只偏 1px → 四格显示同一贴图
832	  store.setTileSilent(x, y, T.CHEST, 0, 0);
833	  store.setTileSilent(x + 1, y, T.CHEST, 18, 0);
834	  store.setTileSilent(x, y + 1, T.CHEST, 0, 18);
835	  store.setTileSilent(x + 1, y + 1, T.CHEST, 18, 18);
836	}
837	
838	function structurePass({ store, surface, rng, world }: GenCtx) {
839	  const { w, h } = store;
840	  // 地下小屋数量:对齐原版 CaveHouseCount 35-40 × WorldArea/5040000(Configuration.json
841	  // ScaleWith:WorldArea)。旧值写死 4 → 小世界即差 10 倍(中/大差更多)
842	  const hutCount = Math.max(4, Math.round(rng.int(35, 40) * (w * h) / 5040000));
843	  for (let i = 0; i < hutCount; i++) {
844	    const hx = rng.int(20, w - 30);
845	    const hy = rng.int(Math.floor(h * 0.45), h - 40);
846	    buildHut(store, hx, hy, rng);
847	    // 小屋中心宝箱（坐在地板上：地板在 hy+6）
848	    placeChest(store, hx + 4, hy + 4);
849	    world.chests.push({ x: hx + 4, y: hy + 4, items: Array(10).fill(null) });
850	  }
851	  // 地表/浅层散落宝箱
852	  for (let i = 0; i < 8; i++) {
853	    const cx = rng.int(10, w - 12);
854	    // 放在洞穴空地的地上（需要 2×2 空间）
855	    for (let y = Math.floor(surface[cx]) + 8; y < h - 10; y++) {
856	      const clear =
857	        !store.isActive(cx, y) && !store.isActive(cx + 1, y) &&
858	        !store.isActive(cx, y - 1) && !store.isActive(cx + 1, y - 1) &&
859	        !store.isActive(cx, y + 1) && !store.isActive(cx + 1, y + 1);
860	      if (clear && store.isSolid(cx, y + 2) && store.isSolid(cx + 1, y + 2)) {
861	        placeChest(store, cx, y);
862	        world.chests.push({ x: cx, y, items: Array(10).fill(null) });
863	        break;
864	      }
865	    }
866	  }
867	}
868	
869	function buildHut(store: GenCtx['store'], hx: number, hy: number, rng: RNG) {
870	  const rw = 9, rh = 6;
871	  // 清空内部
872	  for (let x = hx; x < hx + rw; x++) {
873	    for (let y = hy; y < hy + rh; y++) {
874	      store.setTileSilent(x, y, 0);
875	      store.setWallSilent(x, y, W.WOOD);
876	    }
877	  }
878	  // 地板与墙
879	  for (let x = hx - 1; x <= hx + rw; x++) {
880	    store.setTileSilent(x, hy + rh, T.WOOD);
881	    store.setTileSilent(x, hy - 1, T.WOOD);
882	  }
883	  for (let y = hy; y <= hy + rh; y++) {
884	    store.setTileSilent(hx - 1, y, T.WOOD);
885	    store.setTileSilent(hx + rw, y, T.WOOD);
886	  }
887	  // 门洞（左侧地板上方 3 格）
888	  for (let y = hy + rh - 3; y < hy + rh; y++) store.setTileSilent(hx - 1, y, 0);
889	  placeDoorClosed(store, hx - 1, hy + rh - 3, 0);
890	  // 内部陈设
891	  store.setTileSilent(hx + 1, hy + rh - 1, T.WORKBENCH, 0, 0);
892	  store.setTileSilent(hx + 3, hy + rh - 1, T.TORCH, 0, 0);
893	  if (rng.chance(0.5)) store.setTileSilent(hx + 5, hy + rh - 1, T.FURNACE, 0, 0);
894	}
895	
896	// ---------- 收尾：出生点（选最平坦区域并整平） ----------
897	function finalize({ store, surface, world, cfg, rng }: GenCtx) {
898	  // 幽灵净化:生成期 TileRunner 会在空气格写残留 type(原版语义,渲染不可见),
899	  // 但我们的存档格式无 active 位——进入存档前归零(防重读激活成浮空块)
900	  for (let i = 0; i < store.type.length; i++) {
901	    if (!store.flags[i] && store.type[i] !== 0) store.type[i] = 0; // 幽灵 type
902	    if (store.type[i] === 0) store.flags[i] = 0; // 幻影活性(type 0 不可有 flags)
903	  }
904	  // ---- 原版 pass 78 Spawn Point（cs:9471-9508）：中心随机扩张采样，自然地表，不改地形 ----
905	  // 旧实现为"找最平坦窗口+人工整平平台"——出生点是一块突兀平台，与原版自然地表不符
906	  let range = 5;
907	  let sx = Math.floor(store.w / 2), sy = 0;
908	  for (;;) {
909	    const x = Math.floor(store.w / 2) + rng.int(-range, range); // Next(-num2, num2+1)
910	    for (let y = 0; y < store.h; y++) {
911	      const i = store.idx(x, y);
912	      // 首个【实心】格——首个 active 格可能是树干(solid:false)致浮空出生
913	      if (store.flags[i] && !!TILE_DEFS[store.type[i]]?.solid) { sx = x; sy = y; break; }
914	    }
915	    let bad = false;
916	    range++;
917	    const gs2 = ctxGs[0];
918	    if (gs2 && sy > gs2.worldSurface) bad = true;
919	    if (store.liquid[store.idx(sx, Math.max(0, sy - 1))] > 0) bad = true;
920	    if (!bad) break;
921	  }
922	  let widen = 10;
923	  const gs0 = ctxGs[0];
924	  while (gs0 && sy > gs0.worldSurface) {
925	    const x = rng.int(Math.floor(store.w / 2) - widen, Math.floor(store.w / 2) + widen);
926	    for (let y = 0; y < store.h; y++) {
927	      const i = store.idx(x, y);
928	      if (store.flags[i] && !!TILE_DEFS[store.type[i]]?.solid) { sx = x; sy = y; break; }
929	    }
930	    widen++;
931	  }
932	  world.spawnX = sx;
933	  world.spawnY = Math.max(4, sy - 3);
934	  // 出生点上空净空保留（防卡块；不整平地形）。
935	  // ★必须豁免树干:树干非实心不会卡人,整格清空会把清理盒内的树干中段删掉
936	  // (基座行 dy=0 与上部 dy>5 保留)→ 浮空断干"贴图透明"。
937	  const clearSpawnCell = (x: number, y: number, keepGrass: boolean) => {
938	    if (!store.inBounds(x, y)) return;
939	    const i = store.idx(x, y);
940	    const t = store.type[i];
941	    if (!store.flags[i] || t === T.TREE) return;
942	    if (keepGrass && t === T.GRASS) return;
943	    store.setTileSilent(x, y, 0);
944	  };
945	  for (let dx = -1; dx <= 1; dx++) {
946	    for (let dy = 1; dy <= 3; dy++) {
947	      clearSpawnCell(sx + dx, sy - dy, false);
948	    }
949	  }
950	
951	  // 原版管线的地表/岩石线来自 TerrainPass 输出,旧 fbm 常数仅作回退
952	  const gs = ctxGs[0];
953	  if (gs) {
954	    world.groundLevel = gs.worldSurface;
955	    world.rockLevel = gs.rockLevel;
956	  } else {
957	    world.groundLevel = Math.floor(store.h * 0.28);
958	    world.rockLevel = Math.floor(store.h * 0.33);
959	  }
960	  // 原版树样式（RandomizeTreeStyle 掷出：边界 + 互异样式）
961	  if (gs) {
962	    world.treeX = gs.treeX;
963	    world.treeStyle = gs.treeStyle;
964	    world.trees = gs.genTrees; // 砍伐整棵判定（Player/Game 消费）
965	  }
966	  // 出生点上空净空（宽区:5×5,豁免草面/树干——草面保持地表,树干保持完整见上注）
967	  for (let dx = -2; dx <= 2; dx++) {
968	    for (let dy = 1; dy <= 5; dy++) {
969	      clearSpawnCell(sx + dx, sy - dy, true);
970	    }
971	  }
972	  // 树登记保留:树干不再被清理盒删除,world.trees 与实际树一一对应
973	  // (原 |t.x-sx|<=5 过滤是配合"清掉树干防幽灵树"的,已不适用)
974	}
975	

```


---

## 🤖 Assistant · 2026-08-11T04:08:39.039Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the main file. Let me now read the vanilla files. Key ones for the "writes to sky" question:

1. TreePass.ts — trees grow above surface
2. StructuresPass.ts — FloatingIslands, SurfaceDecor, LifeCrystals, Pyramid, WetJungle
3. HalfBrickPass.ts — Smooth World / Waterfall lip
4. CavesPass.ts — CavesPass / TileRunner
5. TerrainPass.ts — terrain, floating islands y
6. BeachPass.ts
7. LakesPass.ts — water
8. CleanupPass.ts
9. TileRunner.ts
10. JunglePass, DesertPass, IceBiomePass, GrassPass, MushroomPass, MarbleGranitePass, DirtToMudPass, CorruptionPass, DungeonPass, TemplePass, IslandHousePass, SwordShrinePass, BuriedChestsPass, TrapsPass, MountCavesPass, GenState.ts

Let me read them in parallel batches. First batch: TerrainPass, CavesPass, TileRunner, HalfBrickPass.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:08:39.503Z · glm-x-preview-260804

```
现在我来读取处理天空区域写入的关键 vanilla pass 文件。
```


---

## 🤖 Assistant · 2026-08-11T04:08:39.515Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TerrainPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:08:39.525Z

**📎 ToolResult**

```
1	// 原版 TerrainPass 移植(Terrarria1405/GameContent/Biomes/TerrainPass.cs,1:1)。
2	// 逐列随机走 5 种地形特征(Plateau/Hill/Dale/Mountain/Valley)驱动 worldSurface/rockLayer;
3	// 输出 worldSurfaceHigh/Low、rockLevelHigh/Low、waterLine、lavaLine 到 GenState;
4	// 海滩区按 Reset 掷的 beachLeftEnd/beachRightStart 平坦化,右海滩入口 Retarget 收平。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { fround } from '../../../core/csCompat';
9	import { T, W } from '../../../data/tiles';
10	
11	const enum Feature { Plateau, Hill, Dale, Mountain, Valley }
12	
13	// GenerateWorldSurfaceOffset(TerrainPass.cs:222-251,普通模式分支)
14	function genSurfaceOffset(rng: RNG, f: Feature): number {
15	  let n = 0;
16	  switch (f) {
17	    case Feature.Plateau:
18	      while (rng.next() * 7 < 1) n += rng.int(-1, 1);
19	      break;
20	    case Feature.Hill:
21	      while (rng.next() * 4 < 1) n--;
22	      while (rng.next() * 10 < 1) n++;
23	      break;
24	    case Feature.Dale:
25	      while (rng.next() * 4 < 1) n++;
26	      while (rng.next() * 10 < 1) n--;
27	      break;
28	    case Feature.Mountain:
29	      while (rng.next() * 2 < 1) n--;
30	      while (rng.next() * 6 < 1) n++;
31	      break;
32	    case Feature.Valley:
33	      while (rng.next() * 2 < 1) n++;
34	      while (rng.next() * 5 < 1) n--;
35	      break;
36	  }
37	  return n;
38	}
39	
40	export function runTerrainPass(st: TileStore, rng: RNG, gs: GenState, flatBeachPadding = 5): void {
41	  const { w, h } = st;
42	  const leftBeach = gs.beachLeftEnd, rightBeach = w - gs.beachRightStart;
43	  let feature: Feature = Feature.Plateau;
44	  let num2 = h * 0.3 * (rng.int(90, 109) * 0.005);            // worldSurface(逐列游走)
45	  let num3 = (num2 + h * 0.2) * (rng.int(90, 109) * 0.01);      // rockLayer(逐列游走)
46	  let loSurf = num2, hiSurf = num2, loRock = num3, hiRock = num3;
47	  const maxSurf = h * 0.23;
48	  const history: number[] = []; // 近 500 列地表(右海滩 Retarget 用)
49	
50	  let runLen = leftBeach + flatBeachPadding;
51	  for (let x = 0; x < w; x++) {
52	    loSurf = Math.min(num2, loSurf);
53	    hiSurf = Math.max(num2, hiSurf);
54	    loRock = Math.min(num3, loRock);
55	    hiRock = Math.max(num3, hiRock);
56	    if (runLen <= 0) {
57	      feature = rng.int(0, 4);
58	      runLen = rng.int(5, 39);
59	      if (feature === Feature.Plateau) runLen *= Math.floor(rng.int(5, 29) * 0.2);
60	    }
61	    runLen--;
62	    // 出生点 ±2% 强制高原;±5% 内避免山/谷(原版换 0-2 低洼特征)
63	    if (x > w * 0.45 && x < w * 0.55 && (feature === Feature.Mountain || feature === Feature.Valley)) {
64	      feature = rng.int(0, 2);
65	    }
66	    if (x > w * 0.48 && x < w * 0.52) feature = Feature.Plateau;
67	    num2 = fround(num2 + genSurfaceOffset(rng, feature)); // C# float：每步舍 float32
68	    if (x < leftBeach + flatBeachPadding || x > w - rightBeach - flatBeachPadding) {
69	      num2 = Math.max(h * 0.17, Math.min(num2, maxSurf)); // 海滩 clamp
70	    } else if (num2 < h * 0.17) { num2 = h * 0.17; runLen = 0; }
71	    else if (num2 > h * 0.26) { num2 = h * 0.26; runLen = 0; }
72	    num2 = fround(num2);
73	    while (rng.int(0, 2) === 0) num3 += rng.int(-2, 2);
74	    if (num3 < num2 + h * 0.06) num3++;
75	    if (num3 > num2 + h * 0.35) num3--;
76	    num3 = fround(num3);
77	    history.push(num2);
78	    if (history.length > 500) history.shift();
79	    // 填列:地表以上空气,到 rockLayer 为泥土,以下石头 + 自然墙
80	    for (let y = 0; y < h; y++) {
81	      const i = st.idx(x, y);
82	      if (y < num2) {
83	        st.type[i] = 0; st.flags[i] = 0;
84	      } else if (y < num3) {
85	        st.type[i] = T.DIRT; st.flags[i] = 1;
86	        if (y > num2 + 3) st.wall[i] = W.DIRT;
87	      } else {
88	        st.type[i] = T.STONE; st.flags[i] = 1;
89	        st.wall[i] = W.STONE;
90	      }
91	    }
92	    // 右海滩入口:若地表高于 maxSurf,回溯改写近 500 列向下收平(TerrainPass.cs:101-107)
93	    if (x === w - rightBeach - flatBeachPadding) {
94	      if (num2 > maxSurf) retargetSurfaceHistory(st, history, x, maxSurf);
95	      feature = Feature.Plateau;
96	      runLen = w - x;
97	    }
98	  }
99	
100	  // 输出常量(TerrainPass.cs:109-132)
101	  const worldSurface = Math.floor(hiSurf + 25);
102	  const rockLayer = Math.floor(worldSurface + Math.floor((hiRock - worldSurface) / 6) * 6);
103	  gs.waterLine = Math.floor((rockLayer + h) / 2) + rng.int(-100, 19);
104	  gs.lavaLine = gs.waterLine + rng.int(50, 79);
105	  // num11 校正:rockLayerLow 与 worldSurfaceHigh 间距 < 20 → 拉开
106	  const num11 = 20;
107	  if (loRock < hiSurf + num11) {
108	    const mid = (loRock + hiSurf) / 2;
109	    let spread = Math.abs(loRock - hiSurf);
110	    if (spread < num11) spread = num11;
111	    loRock = mid + spread / 2;
112	    hiSurf = mid - spread / 2;
113	  }
114	  gs.worldSurface = worldSurface;
115	  gs.rockLevel = rockLayer;
116	  gs.worldSurfaceLow = Math.floor(loSurf);
117	  gs.worldSurfaceHigh = Math.floor(hiSurf);
118	  gs.rockLevelLow = Math.floor(loRock);
119	  gs.rockLevelHigh = Math.floor(hiRock);
120	}
121	
122	// RetargetSurfaceHistory(TerrainPass.cs:256-276):将历史地表逐列下压到目标高度后重写地形
123	function retargetSurfaceHistory(st: TileStore, history: number[], targetX: number, targetHeight: number): void {
124	  for (let i1 = 0; i1 < history.length / 2 && history[history.length - 1] > targetHeight; i1++) {
125	    for (let i2 = 0; i2 < history.length - i1 * 2; i2++) {
126	      const v = history[history.length - i2 - 1] - 1;
127	      history[history.length - i2 - 1] = v;
128	      if (v <= targetHeight) break;
129	    }
130	  }
131	  for (let i = 0; i < history.length; i++) {
132	    const surf = history[history.length - i - 1];
133	    retargetColumn(st, targetX - i, surf);
134	  }
135	}
136	
137	function retargetColumn(st: TileStore, x: number, worldSurface: number): void {
138	  if (x < 0 || x >= st.w) return;
139	  for (let y = 0; y < st.h; y++) {
140	    const i = st.idx(x, y);
141	    if (y < worldSurface) {
142	      st.type[i] = 0; st.flags[i] = 0;
143	    } else if (!(st.type[i] === T.STONE && st.flags[i])) {
144	      st.type[i] = T.DIRT; st.flags[i] = 1;
145	    }
146	  }
147	}
148	

```


---

## 🤖 Assistant · 2026-08-11T04:08:39.590Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CavesPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:08:39.601Z

**📎 ToolResult**

```
1	// 原版 pass 8-14 移植(参数 1:1 对齐 WorldGen.cs L5174-5372):
2	// Rocks In Dirt / Dirt In Rocks / Clay / Small Holes / Dirt Layer Caves /
3	// Rock Layer Caves / Surface Caves(5 组,含大竖井)。
4	import type { TileStore } from '../../TileStore';
5	import type { RNG } from '../../../core/rng';
6	import type { GenState } from './GenState';
7	import { T, TILE_BY_KEY } from '../../../data/tiles';
8	import { tileRunner, digTunnel } from './TileRunner';
9	
10	const DIRT = T.DIRT;
11	const CLAY = TILE_BY_KEY['clay']!;
12	
13	/** pass 8-10:泥石混合 + 粘土 */
14	export function runRocksAndClayPass(st: TileStore, rng: RNG, gs: GenState): void {
15	  const { w, h } = st;
16	  const area = w * h;
17	  const run = (count: number, yMin: number, yMax: number, type: number, sMin: number, sMax: number, stMin: number, stMax: number) => {
18	    for (let n = 0; n < count; n++) {
19	      tileRunner(st, rng, gs, rng.int(0, w - 1), rng.int(Math.max(0, Math.floor(yMin)), Math.min(h - 1, Math.floor(yMax))), {
20	        strength: rng.int(sMin, sMax), steps: rng.int(stMin, stMax), type,
21	      });
22	    }
23	  };
24	  // 8 Rocks In Dirt(L5178):三档密度带,石嵌泥
25	  run(area * 0.00015, 0, gs.worldSurfaceLow, T.STONE, 4, 14, 5, 39);
26	  for (let n = 0; n < area * 0.0002; n++) { // 中带:起点上方 10 格须为实心否则重掷一次
27	    const i = rng.int(0, w - 1);
28	    let j = rng.int(gs.worldSurfaceLow, gs.worldSurfaceHigh);
29	    if (!st.flags[st.idx(i, Math.max(0, j - 10))]) j = rng.int(gs.worldSurfaceLow, gs.worldSurfaceHigh);
30	    tileRunner(st, rng, gs, i, j, { strength: rng.int(4, 9), steps: rng.int(5, 29), type: T.STONE });
31	  }
32	  run(area * 0.0045, gs.worldSurfaceHigh, gs.rockLevelHigh, T.STONE, 2, 6, 2, 22);
33	  // 9 Dirt In Rocks(L5203):泥嵌石
34	  run(area * 0.005, gs.rockLevelLow, h, DIRT, 2, 5, 2, 39);
35	  // 10 Clay(L5212):三带 + 表层粘土清除
36	  run(area * 0.00002, 0, gs.worldSurfaceLow - 1, CLAY, 4, 13, 10, 49);
37	  run(area * 0.00005, gs.worldSurfaceLow, gs.worldSurfaceHigh, CLAY, 8, 13, 15, 44);
38	  run(area * 0.00002, gs.worldSurfaceHigh, gs.rockLevelHigh, CLAY, 8, 14, 5, 49);
39	  for (let x = 5; x < w - 5; x++) {
40	    for (let y = 1; y < gs.worldSurface - 1; y++) {
41	      if (!st.flags[st.idx(x, y)]) continue;
42	      for (let y2 = y; y2 < y + 5; y2++) {
43	        if (st.get(x, y2) === CLAY) st.setTileSilent(x, y2, 0);
44	      }
45	      break;
46	    }
47	  }
48	}
49	
50	/** pass 11-14:洞穴(小孔/泥土层/岩石层/地表入口) */
51	export function runCavesPass(st: TileStore, rng: RNG, gs: GenState): void {
52	  const { w, h } = st;
53	  const area = w * h;
54	  // 位置避让(cs:4733):beachSandRandomCenter(320)+20 = 340
55	  const avoidBeach = 340;
56	  // 11 Small Holes(L5238):每轮两个 runner,1/5 液体;
57	  // 避让:海滩 340 内且浅于 worldSurfaceHigh、或中部 45-55% 且浅于 worldSurface → 重掷
58	  for (let n = 0; n < area * 0.0015; n++) {
59	    const type = rng.next() * 5 < 1 ? -2 : -1;
60	    let x1 = rng.int(0, w - 1), y1 = rng.int(gs.worldSurfaceHigh, h - 1);
61	    for (let a = 0; a < 40 && (((x1 < avoidBeach || x1 > w - avoidBeach) && y1 < gs.worldSurfaceHigh)
62	      || (x1 > w * 0.45 && x1 < w * 0.55 && y1 < gs.worldSurface)); a++) {
63	      x1 = rng.int(0, w - 1);
64	      y1 = rng.int(gs.worldSurfaceHigh, h - 1);
65	    }
66	    tileRunner(st, rng, gs, x1, y1, { strength: rng.int(2, 4), steps: rng.int(2, 19), type });
67	    let x2 = rng.int(0, w - 1), y2 = rng.int(gs.worldSurfaceHigh, h - 1);
68	    for (let a = 0; a < 40 && (((x2 < avoidBeach || x2 > w - avoidBeach) && y2 < gs.worldSurfaceHigh)
69	      || (x2 > w * 0.45 && x2 < w * 0.55 && y2 < gs.worldSurface)); a++) {
70	      x2 = rng.int(0, w - 1);
71	      y2 = rng.int(gs.worldSurfaceHigh, h - 1);
72	    }
73	    tileRunner(st, rng, gs, x2, y2, { strength: rng.int(8, 14), steps: rng.int(7, 29), type });
74	  }
75	  // 12 Dirt Layer Caves(L5262):1/6 液体;中部条件为闭区间 >=45% <=55%
76	  for (let n = 0; n < area * 0.00003; n++) {
77	    const type = rng.next() * 6 < 1 ? -2 : -1;
78	    let i = rng.int(0, w - 1);
79	    let j = rng.int(gs.worldSurfaceLow, gs.rockLevelHigh);
80	    for (let a = 0; a < 40 && ((i < avoidBeach || i > w - avoidBeach) && j < gs.worldSurfaceHigh
81	      || (i >= w * 0.45 && i <= w * 0.55 && j < gs.worldSurface)); a++) {
82	      i = rng.int(0, w - 1);
83	      j = rng.int(gs.worldSurfaceLow, gs.rockLevelHigh);
84	    }
85	    // digTunnel 蜿蜒版(原版 1.4.0.5 为直线 TileRunner;参考 1.4.4 洞型走 digTunnel,
86	    // 数量/尺寸/位置与原版一致,仅形状改为有机蜿蜒)
87	    const dx = rng.int(-100, 100) * 0.01, dy = rng.int(-100, 100) * 0.01;
88	    digTunnel(st, rng, i, j, dx, dy, rng.int(30, 199), rng.int(3, 7), type === -2);
89	  }
90	  // 13 Rock Layer Caves(L5280):1/10 液体(digTunnel 蜿蜒版,尺寸对齐原版 strength×0.5)
91	  for (let n = 0; n < area * 0.00013; n++) {
92	    const wet = rng.next() * 10 < 1;
93	    const dx = rng.int(-100, 100) * 0.01, dy = rng.int(-100, 100) * 0.01;
94	    digTunnel(st, rng, rng.int(0, w - 1), rng.int(gs.rockLevelHigh, h - 1), dx, dy,
95	      rng.int(50, 299), rng.int(3, 9), wet);
96	  }
97	  // 14 Surface Caves(L5296):五组地表入口
98	  const beachL = gs.beachLeftEnd + 20, beachR = gs.beachRightStart - 20;
99	  const surfaceCave = (count: number, lo: number, hi: number, runners: Array<[(i2: number) => void]>) => {
100	    for (let n = 0; n < count; n++) {
101	      let x = rng.int(0, w - 1);
102	      for (let a = 0; a < 40 && (x > w * lo && x < w * hi || x < beachL || x > beachR); a++) {
103	        x = rng.int(0, w - 1);
104	      }
105	      // 找该列首个实心行
106	      let sy = -1;
107	      for (let y = 0; y < gs.worldSurfaceHigh; y++) {
108	        if (st.flags[st.idx(x, y)]) { sy = y; break; }
109	      }
110	      if (sy < 0) continue;
111	      for (const r of runners) r[0](x);
112	    }
113	  };
114	  // 14a:细入口
115	  surfaceCave(Math.floor(w * 0.002), 0.45, 0.55, [[(x) => {
116	    tileRunner(st, rng, gs, x, firstSolid(st, gs, x), { strength: rng.int(3, 5), steps: rng.int(5, 49), type: -1, speedX: rng.int(-10, 10) * 0.1, speedY: 1 });
117	  }]]);
118	  // 14b:中入口
119	  surfaceCave(Math.floor(w * 0.0007), 0.43, 0.57, [[(x) => {
120	    tileRunner(st, rng, gs, x, firstSolid(st, gs, x), { strength: rng.int(10, 14), steps: rng.int(50, 129), type: -1, speedX: rng.int(-10, 10) * 0.1, speedY: 2 });
121	  }]]);
122	  // 14c:大竖井(三连 runner)
123	  surfaceCave(Math.floor(w * 0.0003), 0.40, 0.60, [[(x) => {
124	    const y = firstSolid(st, gs, x);
125	    tileRunner(st, rng, gs, x, y, { strength: rng.int(12, 24), steps: rng.int(150, 499), type: -1, speedX: rng.int(-10, 10) * 0.1, speedY: 4 });
126	    tileRunner(st, rng, gs, x, y, { strength: rng.int(8, 16), steps: rng.int(60, 199), type: -1, speedX: rng.int(-10, 10) * 0.1, speedY: 2 });
127	    tileRunner(st, rng, gs, x, y, { strength: rng.int(5, 12), steps: rng.int(40, 169), type: -1, speedX: rng.int(-10, 10) * 0.1, speedY: 2 });
128	  }]]);
129	  // 14d:noYChange 入口
130	  surfaceCave(Math.floor(w * 0.0004), 0.40, 0.60, [[(x) => {
131	    tileRunner(st, rng, gs, x, firstSolid(st, gs, x), { strength: rng.int(7, 11), steps: rng.int(150, 249), type: -1, speedY: 1, noYChange: true });
132	  }]]);
133	  // 14e Caverer(L5360):5×(w/4200 整除截断) 个大洞穴系统;起点边距 340、y 上界 h-400 开
134	  const cavCount = 5 * Math.floor(w / 4200);
135	  for (let n = 0; n < cavCount; n++) {
136	    const cx = rng.int(340, w - 341);
137	    const cy = rng.int(gs.rockLevel, Math.max(gs.rockLevel + 1, h - 401));
138	    caverer(st, rng, gs, cx, cy);
139	  }
140	}
141	
142	/** Caverer(L48064)1:1:模式 0 = 主隧道+粗支洞,模式 1 = 长细链 */
143	function caverer(st: TileStore, rng: RNG, gs: GenState, X: number, Y: number): void {
144	  const randDir = () => {
145	    let dx = rng.int(0, 99) * 0.01;
146	    let dy = 1 - dx;
147	    if (rng.next() < 0.5) dx = -dx;
148	    if (rng.next() < 0.5) dy = -dy;
149	    return [dx, dy] as [number, number];
150	  };
151	  if (rng.next() < 0.5) {
152	    // 模式 0:7-8 段,每段主挖(6-19 步,粗 4-8)+ 支挖(30-49 步,细 2-5)+ 小 runner
153	    let px = X + 0.0, py = Y + 0.0;
154	    let [dx, dy] = randDir();
155	    const segs = rng.int(7, 8);
156	    for (let k = 0; k < segs; k++) {
157	      [px, py] = digTunnel(st, rng, px, py, dx, dy, rng.int(6, 19), rng.int(4, 8));
158	      dx += rng.int(-20, 20) * 0.1; dy += rng.int(-20, 20) * 0.1;
159	      dx = Math.max(-1.5, Math.min(1.5, dx));
160	      dy = Math.max(-1.5, Math.min(1.5, dy));
161	      const [bx, by] = randDir();
162	      const [ex, ey] = digTunnel(st, rng, px, py, bx, by, rng.int(30, 49), rng.int(3, 5));
163	      tileRunner(st, rng, gs, Math.floor(ex), Math.floor(ey), {
164	        strength: rng.int(10, 19), steps: rng.int(5, 9), type: -1,
165	      });
166	    }
167	  } else {
168	    // 模式 1:15-29 段长细链(湿)
169	    let px = X + 0.0, py = Y + 0.0;
170	    let [dx, dy] = randDir();
171	    const segs = rng.int(15, 29);
172	    for (let k = 0; k < segs; k++) {
173	      [px, py] = digTunnel(st, rng, px, py, dx, dy, rng.int(5, 14), rng.int(2, 5), true);
174	      dx += rng.int(-20, 20) * 0.1; dy += rng.int(-20, 20) * 0.1;
175	      dx = Math.max(-1.5, Math.min(1.5, dx));
176	      dy = Math.max(-1.5, Math.min(1.5, dy));
177	    }
178	  }
179	}
180	
181	function firstSolid(st: TileStore, gs: GenState, x: number): number {
182	  for (let y = 0; y < gs.worldSurfaceHigh && y < st.h; y++) {
183	    if (st.flags[st.idx(x, y)]) return y;
184	  }
185	  return Math.floor(gs.worldSurfaceHigh);
186	}
187	

```


---

## 🤖 Assistant · 2026-08-11T04:08:47.602Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Important observations:

TerrainPass line 80-91: fills columns. For y < num2 → air. So no sky writes.

CavesPass line 25: `run(area * 0.00015, 0, gs.worldSurfaceLow, T.STONE, 4, 14, 5, 39);` — Rocks In Dirt with yMin=0! This is a SKY WRITER. Wait, in the original WorldGen.cs L5178, it's `num = (double)(Main.maxTilesX * Main.maxTilesY) * 3E-05` with `Main.tile[i, j]` where j is `GenBase._random.Next(0, Main.worldSurfaceLow)` — hmm, actually in the original: "Rocks in Dirt" places stone in the DIRT layer, which spans surface to rock layer. Let me check the original. Actually in vanilla WorldGen.cs:

```csharp
double num = (double)(Main.maxTilesX * Main.maxTilesY) * 0.00015;
for (int num2 = 0; num2 < num; num2++)
{
    int i = GenBase._random.Next(0, Main.maxTilesX - 1);
    int j = GenBase._random.Next(0, (int)Main.worldSurfaceLow);
    WorldGen.TileRunner(i, j, (double)GenBase._random.Next(4, 14), GenBase._random.Next(5, 39), 1);
}
```

Hmm, that's vanilla. TileRunner with type 1 (stone) and addTile default... In vanilla TileRunner, there's `bool fail = true` loop — the runner only places tiles if the target tile is not air? Let me check TileRunner.ts in this repo. Vanilla TileRunner:

```csharp
public static void TileRunner(int i, int j, double strength, int steps, int type, bool addTile = false, short speedX = 0, short speedY = 0, bool noYChange = false, bool overRide = false)
```

And inside: it checks `if (!Main.tile[(int)Math.Round(num2), (int)Math.Round(num3)].nactive()) continue;` or something — the runner skips air tiles when placing (addTile=false means it only replaces existing active tiles). That's the crucial semantic: with addTile=false, TileRunner only converts existing solid tiles, never writes into air. So the yMin=0 runs don't write sky. But the finalize() comment says "TileRunner 会在空气格写残留 type(原版语义,渲染不可见)" — the ghost type! So TileRunner DOES write type into air cells but without flags (ghost type), and finalize zeroes them. THIS is the "写入大量杂块、后期又被抹除" source!

Let me read TileRunner.ts to confirm.
````

</details>


---

## 🤖 Assistant · 2026-08-11T04:08:48.109Z · glm-x-preview-260804

```
这是关键文件——`finalize` 提到了来自 `TileRunner` 的 "ghost types"。让我来读取 `TileRunner.ts` 和 `HalfBrickPass.ts`。
```


---

## 🤖 Assistant · 2026-08-11T04:08:48.278Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:08:48.292Z

**📎 ToolResult**

```
1	// 原版 WorldGen.TileRunner 移植(WorldGen.cs:46405)——地形/洞穴/矿石/沙/泥的万能 workhorse。
2	// 沿随机方向走 steps 步,每步以衰减半径的钻石区域(L1 距离 + 1.5% 抖动)铺设/挖除 type。
3	// type<0 = 挖空(-1 空气 / -2 遇活性块则填液体);type>=0 = 铺设(仅改写活性块 type,
4	// addTile 才激活空气格——原版语义,空气格上的幽灵 type 不渲染)。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T, TILE_BY_KEY, TILE_DEFS } from '../../../data/tiles';
9	
10	const MUD = TILE_BY_KEY['mud']!;
11	const CLAY = TILE_BY_KEY['clay']!;
12	const SANDSTONE = TILE_BY_KEY['sandstone']!;
13	const HARDSAND = TILE_BY_KEY['hardened_sand']!;
14	const MARBLE = TILE_BY_KEY['v_367_marble_block']!;
15	const GRANITE = TILE_BY_KEY['v_368_granite_block']!;
16	
17	/** 按 vanilla sheet id 收集本仓库 tile id(缺失的自动跳过) */
18	export function idsByVanillaSheet(...sheets: number[]): Set<number> {
19	  const out = new Set<number>();
20	  for (const d of TILE_DEFS) {
21	    const vs = d.vanilla?.sheet;
22	    if (vs !== undefined && sheets.includes(vs)) out.add(TILE_BY_KEY[d.key]);
23	  }
24	  return out;
25	}
26	
27	// 原版 Main.tileStone(Main.cs:6120-6139):宝石 63-68 + 活/失活石 130/131 + 琥珀石 566。
28	// 只有这些"放置类型"触发 flag3(仅替换石头)
29	const STONE_PLACED = idsByVanillaSheet(63, 64, 65, 66, 67, 68, 130, 131, 566);
30	// TileID.Sets.CanBeClearedDuringGeneration 默认 true,仅这 11 种不可被生成期覆盖(TileID.cs:702)
31	export const NOT_CLEARABLE = idsByVanillaSheet(396, 400, 401, 397, 398, 399, 404, 368, 367, 226, 237,
32	  135, 136, 137, 141, 443,   // 电路器件（压板/开关/陷阱/炸药/喷泉）：矿石 runner 不可覆盖
33	  41, 43, 44);              // 地牢砖（原版顺序中矿石先于地牢，此处防反向覆盖）
34	// 原版 switch case 45/147/189/190/196/460:无条件 flag3(金砖/雪/云/荧光菇/雨云/雪云)
35	const FLAG3_ALWAYS = idsByVanillaSheet(45, 147, 189, 190, 196, 460);
36	// TileID.Sets.Ore:铺设 396/397 时矿石可覆盖
37	const ORE_SET = new Set<number>();
38	{
39	  for (const k of ['ore_copper', 'ore_tin', 'ore_iron', 'ore_lead', 'ore_silver', 'ore_tungsten',
40	    'ore_gold', 'ore_platinum', 'ore_demonite', 'ore_crimtane', 'ore_cobalt', 'ore_mythril',
41	    'ore_adamantite', 'ore_palladium', 'ore_orichalcum', 'ore_titanium', 'ore_chlorophyte',
42	    'ore_hellstone', 'ore_meteorite']) { const id = TILE_BY_KEY[k]; if (id !== undefined) ORE_SET.add(id); }
43	}
44	
45	export interface TileRunnerOpts {
46	  strength: number;
47	  steps: number;
48	  type: number;          // <0 挖空;>=0 铺设的 tile id
49	  addTile?: boolean;     // 铺设时激活格子并清液体(挖空恒 false)
50	  speedX?: number;
51	  speedY?: number;
52	  noYChange?: boolean;   // 地表以上铺设时填土墙(墙 2)
53	  overRide?: boolean;    // 覆盖已有活性块(默认 true)
54	  ignoreTileType?: number; // 遇此类型跳过(-1 不过滤)
55	  mudWall?: boolean;     // 丛林泥墙模式(墙 15/64 按深度)
56	}
57	
58	export function tileRunner(
59	  st: TileStore, rng: RNG, gs: GenState,
60	  i: number, j: number, o: TileRunnerOpts,
61	): void {
62	  const { strength, steps, type } = o;
63	  const addTile = o.addTile ?? false;
64	  const overRide = o.overRide ?? true;
65	  const noYChange = o.noYChange ?? false;
66	  const ignoreTileType = o.ignoreTileType ?? -1;
67	  let num1 = strength;          // 当前半径(衰减)
68	  let num2 = steps;             // 剩余步数
69	  let px = i + 0.0, py = j + 0.0;
70	  // 原版初始速度 Next(-10,11)*0.1(0.1 步长离散);仅 speedX/speedY 任一非 0 才覆写
71	  let vx = rng.int(-10, 10) * 0.1;
72	  let vy = rng.int(-10, 10) * 0.1;
73	  if ((o.speedX ?? 0) !== 0 || (o.speedY ?? 0) !== 0) {
74	    vx = o.speedX ?? 0; vy = o.speedY ?? 0;
75	  }
76	
77	  while (num1 > 0 && num2 > 0) {
78	    // 泥向上钻出世界顶即停(原版)
79	    if (py < 0 && num2 > 0 && type === MUD) num2 = 0;
80	    num1 = strength * (num2 / steps);
81	    num2--;
82	    const x0 = Math.max(1, Math.floor(px - num1 * 0.5));
83	    const x1 = Math.min(st.w - 1, Math.floor(px + num1 * 0.5));
84	    const y0 = Math.max(1, Math.floor(py - num1 * 0.5));
85	    const y1 = Math.min(st.h - 1, Math.floor(py + num1 * 0.5));
86	    for (let x = x0; x < x1; x++) {
87	      for (let y = y0; y < y1; y++) {
88	        if (ignoreTileType >= 0 && st.type[st.idx(x, y)] === ignoreTileType && st.flags[st.idx(x, y)]) continue;
89	        const dist = Math.abs(x - px) + Math.abs(y - py);
90	        if (dist >= strength * 0.5 * (1 + rng.int(-10, 10) * 0.015)) continue;
91	        const ti = st.idx(x, y);
92	        // 丛林泥墙(原版 mudWall 分支:浅层墙 15,深层墙 64,均避让邻墙)
93	        if (o.mudWall && y > gs.worldSurface && st.wall[st.idx(x, y - 1)] !== 2
94	          && y < st.h - 210 - rng.int(0, 2)
95	          && dist < strength * 0.45 * (1 + rng.int(-10, 10) * 0.01)) {
96	          if (y > gs.lavaLine - rng.int(0, 3) - 50) {
97	            if (st.wall[st.idx(x, y - 1)] !== 64 && st.wall[st.idx(x, y + 1)] !== 64
98	              && st.wall[st.idx(x - 1, y)] !== 64) st.wall[ti] = 15;
99	          } else if (st.wall[st.idx(x, y - 1)] !== 15 && st.wall[st.idx(x, y + 1)] !== 15
100	            && st.wall[st.idx(x - 1, y)] !== 15) {
101	            st.wall[ti] = 64;
102	          }
103	        }
104	        // granite/marble 伴生墙(cs L46503-46506):核心 0.3R 内同步铺墙 180/178
105	        if (type === GRANITE || type === MARBLE) {
106	          if (dist < strength * 0.3 * (1 + rng.int(-10, 10) * 0.01)) {
107	            st.wall[ti] = type === GRANITE ? 180 : 178;
108	          }
109	        }
110	        if (type < 0) {
111	          // 挖空:沙不挖(原版 53 保护);-2 在活性块上填液体
112	          if (st.type[ti] === T.SAND) continue;
113	          if (type === -2 && st.flags[ti] && (y < gs.waterLine || y > gs.lavaLine)) {
114	            st.liquid[ti] = 255;
115	            st.liquidType[ti] = y > gs.lavaLine ? 2 : 1;
116	          }
117	          st.type[ti] = 0;
118	          st.flags[ti] = 0;
119	        } else {
120	          // 铺设:原版 flag3 规则(WorldGen.cs:46509-46555)
121	          if (overRide || !st.flags[ti]) {
122	            const cur = st.type[ti];
123	            // Main.tileStone[type](放置类型是宝石族)且目标非石头 → flag3
124	            let flag3 = STONE_PLACED.has(type) && cur !== T.STONE;
125	            // CanBeClearedDuringGeneration:11 种不可清 tile 被覆盖时恒 flag3
126	            if (NOT_CLEARABLE.has(cur)) flag3 = true;
127	            if (cur === T.STONE) {
128	              // 泥不替换近地表的石头(±50 抖动)
129	              if (type === MUD && y < gs.worldSurface + rng.int(-50, 49)) flag3 = true;
130	            } else if (FLAG3_ALWAYS.has(cur)) {
131	              // 金砖/雪/云/荧光菇/雨云/雪云:无条件保护
132	              flag3 = true;
133	            } else if (cur === T.SAND) {
134	              if (type === MUD && inUndergroundDesert(gs, x, y)) flag3 = true;
135	              if (type === CLAY) flag3 = true;  // 原版:沙上不可铺粘土
136	              if (y < gs.worldSurface && type !== MUD) flag3 = true;
137	            } else if (cur === MARBLE || cur === GRANITE) {
138	              if (type === MUD) flag3 = true;
139	            } else if (cur === SANDSTONE || cur === HARDSAND) {
140	              if (!ORE_SET.has(type)) flag3 = true;
141	            }
142	            if (!flag3) st.type[ti] = type;
143	          }
144	          if (addTile) {
145	            st.flags[ti] = 1;
146	            st.liquid[ti] = 0;
147	            st.liquidType[ti] = 0;
148	          }
149	          if (noYChange && y < gs.worldSurface && type !== MUD) st.wall[ti] = 2;
150	          if (type === MUD && y > gs.waterLine && st.liquid[ti] > 0) {
151	            st.liquid[ti] = 0;
152	            st.liquidType[ti] = 0;
153	          }
154	        }
155	      }
156	    }
157	    // 移动 + 大半径加速(原版 12 档阶梯 50..900,每档速度抖动 ±0.05)
158	    px += vx; py += vy;
159	    for (const thr of [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900]) {
160	      if (num1 > thr) {
161	        px += vx; py += vy;
162	        num2--;
163	        vy += rng.int(-10, 10) * 0.05;
164	        vx += rng.int(-10, 10) * 0.05;
165	      } else break;
166	    }
167	    // 每步全局速度抖动 + ±1 钳制(cs L46659-46673):X 恒抖;
168	    // !noYChange 时 Y 抖动;noYChange 且非泥、半径<3 时只钳不抖
169	    vx += rng.int(-10, 10) * 0.05;
170	    if (vx > 1) vx = 1;
171	    if (vx < -1) vx = -1;
172	    if (!noYChange) {
173	      vy += rng.int(-10, 10) * 0.05;
174	      if (vy > 1) vy = 1;
175	      if (vy < -1) vy = -1;
176	    } else if (type !== MUD && num1 < 3) {
177	      if (vy > 1) vy = 1;
178	      if (vy < -1) vy = -1;
179	    }
180	    // 泥专用 vy 规则(1456 cs L77484-77500)：±0.5 钳 + 岩层上界/地狱带上界定向推挤——
181	    // 丛林首轮泥 runner(vy 初始 ±1)靠它被压进 [rockLayer+100, maxTilesY-300] 带；缺失时泥漂出丛林
182	    if (type === MUD && !noYChange) {
183	      if (vy > 0.5) vy = 0.5;
184	      if (vy < -0.5) vy = -0.5;
185	      if (py < gs.rockLevel + 100) vy = 1;
186	      if (py > st.h - 300) vy = -1;
187	    }
188	  }
189	}
190	
191	/**
192	 * 原版 WorldGen.digTunnel(L48132)移植:蜿蜒洞穴原语。
193	 * 速度 = (dir + 噪声游走±0.2/步) × 0.6 → 会拐弯;半径在 [Size×0.6, Size×2] 随机波动 → 粗细变化。
194	 * 这是有机洞型的来源(TileRunner strength<50 时恒速恒宽 = 直线刀砍)。
195	 */
196	export function digTunnel(
197	  st: TileStore, rng: RNG,
198	  X: number, Y: number, xDir: number, yDir: number,
199	  steps: number, size: number, wet = false,
200	): [number, number] {
201	  let x = Math.max(size + 1, Math.min(st.w - size - 1, X));
202	  let y = Math.max(size + 1, Math.min(st.h - size - 1, Y));
203	  let noiseX = 0, noiseY = 0;
204	  let radius = size;
205	  for (let step = 0; step < steps; step++) {
206	    const x0 = Math.floor(x - radius), x1 = Math.floor(x + radius);
207	    const y0 = Math.floor(y - radius), y1 = Math.floor(y + radius);
208	    for (let ix = x0; ix <= x1; ix++) {
209	      for (let iy = y0; iy <= y1; iy++) {
210	        if (Math.abs(ix - x) + Math.abs(iy - y) < radius * (1 + rng.int(-10, 10) * 0.005)
211	          && st.inBounds(ix, iy)) {
212	          const i = st.idx(ix, iy);
213	          st.type[i] = 0; st.flags[i] = 0;
214	          if (wet) { st.liquid[i] = 255; st.liquidType[i] = 1; }
215	        }
216	      }
217	    }
218	    radius += rng.int(-50, 50) * 0.03;
219	    if (radius < size * 0.6) radius = size * 0.6;
220	    if (radius > size * 2) radius = size * 2;
221	    noiseX += rng.int(-20, 20) * 0.01;
222	    noiseY += rng.int(-20, 20) * 0.01;
223	    noiseX = Math.max(-1, Math.min(1, noiseX));
224	    noiseY = Math.max(-1, Math.min(1, noiseY));
225	    x += (xDir + noiseX) * 0.6;
226	    y += (yDir + noiseY) * 0.6;
227	  }
228	  return [x, y];
229	}
230	
231	function inUndergroundDesert(gs: GenState, x: number, y: number): boolean {
232	  const ud = gs.undergroundDesert;
233	  return !!ud && x >= ud.x0 && x <= ud.x1 && y >= ud.y0 && y <= ud.y1;
234	}
235	

```


---

## 🤖 Assistant · 2026-08-11T04:08:48.451Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:08:48.481Z

**📎 ToolResult**

```
1	// 原版 "Smooth World"(L7568) + "Waterfalls"(L7697) 两个生成 pass 的半砖移植 +
2	// PoundTile/SlopeTile/CanPoundTile（L49122-49232）。
3	// 半砖是原版"水浸润到方块贴图透明区"与瀑布触发（WaterfallManager 靠 halfBrick 唇缘）
4	// 的核心：Smooth World 把地表凸起砸成半砖/坡面，Waterfalls pass 专门在水边唇缘砸半砖。
5	// 偏离原版处（坡面渲染未实现前）：
6	//  - 原版随机二选一的 SlopeTile 分支统一改为 PoundTile（视觉安全，唇缘效果等价）
7	//  - slope 3/4 的坡面分支暂不生成；Tile Cleanup 的 slope→halfBrick 转换随之无需
8	//  - CanPoundTile 的原版类型黑名单（10/48/137/...）近似为"非 solid 的 framed/decor 不砸"
9	import type { TileStore } from '../../TileStore';
10	import type { RNG } from '../../../core/rng';
11	import type { GenState } from './GenState';
12	import { TILE_DEFS } from '../../../data/tiles';
13	
14	/** WorldGen.SolidTile(i, j, false) 等价（WorldGen.cs:42370）：
15	 *  active && tileSolid && !tileSolidTop && !halfBrick && slope==0 —— 半砖/坡面格不算实心。
16	 *  这对 PoundTile（toggle 语义）至关重要：已砸的半砖不会被后续 pass 再"砸回"整砖 */
17	export function solidTile(st: TileStore, x: number, y: number): boolean {
18	  if (x < 0 || y < 0 || x >= st.w || y >= st.h) return false;
19	  const i = st.idx(x, y);
20	  // 原版 SolidTile 检查 active()（=flags）：TileRunner 幽灵 tile（有 type 无 flags）
21	  // 不得当实心——曾致补角分支实体化天空幽灵块成浮空半砖（2583 个）
22	  if (!st.flags[i]) return false;
23	  const t = st.type[i];
24	  if (t === 0) return false;
25	  const d = TILE_DEFS[t];
26	  return !!d && d.solid && !d.platform && !st.half[i] && st.slope[i] === 0;
27	}
28	
29	/** 可砸判定（WorldGen.cs:49122 CanPoundTile 简化）：实心非平台非框架物 */
30	function canPoundTile(st: TileStore, x: number, y: number): boolean {
31	  const i = st.idx(x, y);
32	  if (!st.flags[i]) return false; // 同 solidTile：幽灵 tile 不可砸
33	  const t = st.type[i];
34	  if (t === 0) return false;
35	  const d = TILE_DEFS[t];
36	  return !!d && d.solid && !d.platform && !d.framed;
37	}
38	
39	/** 砸半砖（WorldGen.cs:49198 PoundTile 的生成期路径）：切换 halfBrick 位 */
40	function poundTile(st: TileStore, x: number, y: number): boolean {
41	  if (!canPoundTile(st, x, y)) return false;
42	  const i = st.idx(x, y);
43	  st.half[i] = st.half[i] ? 0 : 1;
44	  if (st.half[i]) st.slope[i] = 0;
45	  return true;
46	}
47	
48	/** 原版 pass "Smooth World"（WorldGen.cs:7568-7696）：地表凸起 → 半砖/削除 */
49	export function runSmoothWorldPass(st: TileStore, rng: RNG, _gs: GenState): void {
50	  const { w, h } = st;
51	  // —— 第一遍：主凸起模式（L7580-7668）——
52	  for (let i = 20; i < w - 20; i++) {
53	    for (let j = 20; j < h - 20; j++) {
54	      const ti = st.idx(i, j);
55	      const t = st.type[ti];
56	      const d = TILE_DEFS[t];
57	      // 原版跳过 48/137/232/191/151/274（雕像/树木/蜂巢类）≈ framed 物体跳过
58	      if (d && d.framed) continue;
59	      if (!st.flags[st.idx(i, j - 1)]) {
60	        // 上方无块：对凸起顶端做半砖/削除
61	        if (solidTile(st, i, j)) {
62	          const li = st.idx(i - 1, j), ri = st.idx(i + 1, j);
63	          if (!st.half[li] && !st.half[ri] && st.slope[li] === 0 && st.slope[ri] === 0) {
64	            if (solidTile(st, i, j + 1)) {
65	              // 模式 A（L7598-7605）：左凸 → 右坡/半砖；模式 B（L7606-7616）：右凸 → 左坡/半砖
66	              if (!solidTile(st, i - 1, j) && !st.half[st.idx(i - 1, j + 1)]
67	                && solidTile(st, i - 1, j + 1) && solidTile(st, i + 1, j)
68	                && !st.flags[st.idx(i + 1, j - 1)]) {
69	                poundTile(st, i, j); // 原版另一半走 SlopeTile(2)（坡面未实现，统一半砖）
70	              } else if (!solidTile(st, i + 1, j) && !st.half[st.idx(i + 1, j + 1)]
71	                && solidTile(st, i + 1, j + 1) && solidTile(st, i - 1, j)
72	                && !st.flags[st.idx(i - 1, j - 1)]) {
73	                poundTile(st, i, j); // 原版另一半走 SlopeTile(1)
74	              } else if (solidTile(st, i + 1, j + 1) && solidTile(st, i - 1, j + 1)
75	                && !st.flags[st.idx(i + 1, j)] && !st.flags[st.idx(i - 1, j)]) {
76	                // 孤立凸起（L7629）：直接半砖
77	                poundTile(st, i, j);
78	              }
79	              // 悬空支脚削除（L7634-7668）：两侧下方空 + 对角支撑 → 删
80	              if (solidTile(st, i, j)) {
81	                if (solidTile(st, i - 1, j) && solidTile(st, i + 1, j + 2)
82	                  && !st.flags[st.idx(i + 1, j)] && !st.flags[st.idx(i + 1, j + 1)]
83	                  && !st.flags[st.idx(i - 1, j - 1)]) {
84	                  st.setTileSilent(i, j, 0);
85	                } else if (solidTile(st, i + 1, j) && solidTile(st, i - 1, j + 2)
86	                  && !st.flags[st.idx(i - 1, j)] && !st.flags[st.idx(i - 1, j + 1)]
87	                  && !st.flags[st.idx(i + 1, j - 1)]) {
88	                  st.setTileSilent(i, j, 0);
89	                } else if (!st.flags[st.idx(i - 1, j + 1)] && !st.flags[st.idx(i - 1, j)]
90	                  && solidTile(st, i + 1, j) && solidTile(st, i, j + 2)) {
91	                  if (rng.chance(0.2)) st.setTileSilent(i, j, 0);
92	                  else if (rng.chance(0.25)) poundTile(st, i, j);
93	                } else if (!st.flags[st.idx(i + 1, j + 1)] && !st.flags[st.idx(i + 1, j)]
94	                  && solidTile(st, i - 1, j) && solidTile(st, i, j + 2)) {
95	                  if (rng.chance(0.2)) st.setTileSilent(i, j, 0);
96	                  else if (rng.chance(0.25)) poundTile(st, i, j);
97	                }
98	              }
99	            }
100	            // 顶部单格立柱（L7662）：两侧皆空 → 删
101	            if (solidTile(st, i, j) && !st.flags[st.idx(i - 1, j)] && !st.flags[st.idx(i + 1, j)]) {
102	              st.setTileSilent(i, j, 0);
103	            }
104	          }
105	        } else if (st.type[ti] === 0) {
106	          // 空位补角（L7669-7695）：下方实心 + 单侧实心 → 补一块并半砖（原版另一半 SlopeTile）
107	          const bi = st.idx(i, j + 1);
108	          const belowType = solidTile(st, i, j + 1) ? st.type[bi] : 0;
109	          if (belowType !== 0 && !TILE_DEFS[belowType]?.framed) {
110	            if (solidTile(st, i - 1, j + 1) && solidTile(st, i + 1, j)
111	              && !st.flags[st.idx(i - 1, j)] && !st.flags[st.idx(i + 1, j - 1)]) {
112	              st.setTileSilent(i, j, belowType);
113	              poundTile(st, i, j);
114	            } else if (solidTile(st, i + 1, j + 1) && solidTile(st, i - 1, j)
115	              && !st.flags[st.idx(i + 1, j)] && !st.flags[st.idx(i - 1, j - 1)]) {
116	              st.setTileSilent(i, j, belowType);
117	              poundTile(st, i, j);
118	            }
119	          }
120	        }
121	      }
122	    }
123	  }
124	  // —— 第二遍（L7677-7694）：斜坡补坡（原版 SlopeTile 1/2）+ 悬坡回落半砖 ——
125	  for (let i = 20; i < w - 20; i++) {
126	    for (let j = 20; j < h - 20; j++) {
127	      const ti = st.idx(i, j);
128	      const d = TILE_DEFS[st.type[ti]];
129	      if (d && d.framed) continue;
130	      if (rng.chance(0.5) && !st.flags[st.idx(i, j - 1)] && solidTile(st, i, j)) {
131	        if (solidTile(st, i, j + 1) && solidTile(st, i + 1, j) && !st.flags[st.idx(i - 1, j)]) {
132	          poundTile(st, i, j); // 原版 SlopeTile(2)
133	        } else if (solidTile(st, i, j + 1) && solidTile(st, i - 1, j) && !st.flags[st.idx(i + 1, j)]) {
134	          poundTile(st, i, j); // 原版 SlopeTile(1)
135	        }
136	      }
137	    }
138	  }
139	}
140	
141	/** 原版 pass "Waterfalls"（WorldGen.cs:7697-7743）：水边唇缘砸半砖（瀑布触发的来源） */
142	export function runWaterfallLipPass(st: TileStore, _rng: RNG, _gs: GenState): void {
143	  const { w, h } = st;
144	  // —— 第一遍（L7701-7723）：实心顶格、左右空、侧旁有水 → 砸半砖 ——
145	  for (let i = 20; i < w - 20; i++) {
146	    for (let j = 20; j < h - 20; j++) {
147	      if (!solidTile(st, i, j)) continue;
148	      const li = st.idx(i - 1, j), ri = st.idx(i + 1, j);
149	      if (st.type[li] !== 0 || st.type[ri] !== 0) continue;
150	      if (!solidTile(st, i, j + 1)) continue;
151	      if (st.liquid[li] === 0 && st.liquid[ri] === 0) continue;
152	      // 上方 8-20 格内已有半砖则跳过（原版防连续砸穿）
153	      let flag = true;
154	      const num3 = 8 + Math.floor(_rng.next() * 12), num4 = 8 + Math.floor(_rng.next() * 12);
155	      for (let k = j - num3; k <= j + num4; k++) {
156	        if (k >= 0 && k < h && st.half[st.idx(i, k)]) flag = false;
157	      }
158	      if (flag) poundTile(st, i, j);
159	    }
160	  }
161	  // —— 第二遍（L7725-7741）：唇缘向相邻实心格扩展半砖 ——
162	  for (let i = 20; i < w - 20; i++) {
163	    for (let j = 20; j < h - 20; j++) {
164	      const ti = st.idx(i, j);
165	      if (!solidTile(st, i, j) || !solidTile(st, i, j + 1)) continue;
166	      if (!solidTile(st, i + 1, j) && st.half[st.idx(i - 1, j)] && st.liquid[st.idx(i - 2, j)] > 0) {
167	        poundTile(st, i, j);
168	      }
169	      if (!solidTile(st, i - 1, j) && st.half[st.idx(i + 1, j)] && st.liquid[st.idx(i + 2, j)] > 0) {
170	        poundTile(st, i, j);
171	      }
172	    }
173	  }
174	}
175	

```


---

## 🤖 Assistant · 2026-08-11T04:08:59.469Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I've found the mechanism. TileRunner line 121-142: when placing (type >= 0) without addTile, the code does:

```ts
if (overRide || !st.flags[ti]) {
  ...
  if (!flag3) st.type[ti] = type;   // ← writes type even into AIR cells (flags=0)!
}
```

Wait — `overRide` defaults to TRUE. So `overRide || !st.flags[ti]` is always true when overRide is true. And then `if (!flag3) st.type[ti] = type;` — it writes the type into the cell even if the cell is air (flags=0). Without `addTile`, flags remain 0 → "ghost tile": type != 0 but flags == 0. This is vanilla behavior (vanilla writes `tile.type` on inactive tiles too? Actually in vanilla the condition is `if (overRide || !Main.tile[num4, num5].active())` then sets type... yes vanilla TileRunner does:

```csharp
if (overRide || !Main.tile[num4, num5].active())
{
    ... flag3 logic ...
    if (!flag3) Main.tile[num4, num5].type = (ushort)type;
}
```

Yes — vanilla writes `type` on inactive tiles (ghost type), and since vanilla saves have an active bit, the ghost is invisible. This repo's save format lacks an active bit, so finalize() zeroes them (WorldGen.ts:900-903).

So the answer to the user's question "生成早期往天空写入大量杂块、后期又被抹除" = TileRunner ghost-type writes into sky air cells by ALL placing passes with y ranges that reach into sky (especially CavesPass "Rocks In Dirt" pass 8 yMin=0!, and many others), then finalized at WorldGen.ts:897-903.

Wait, but the user asks about "y < groundLevel" meaning sky. Hmm, the user says "y < groundLevel（地表以上）" — yes sky. Note tile coordinates: smaller y = higher. So sky = y < groundLevel.

Also there could be passes that write ACTUAL blocks (flags=1) into the sky that later get removed. Let me check:
- floatCleanupPass (legacy only, runs below surface from surfY+2) — that's the cleanup.
- vanillaCleanup — CleanupPass.ts
- HalfBrickPass smooth world: "空位补角" branch at line 105-119 — writes belowType at (i,j) where the cell is air. If j is in sky and j+1 is solid... at sky, j+1 solid means floating islands or surface. Actually this fills in corners — near surface this writes into the sky above the surface! It writes `st.setTileSilent(i, j, belowType)` which sets flags=1 (need to check setTileSilent). This is a genuine sky writer that is NOT removed later (it stays as half brick). But the comment says solidTile requires flags so ghost tiles are not solidified (they fixed a bug where 2583 ghost blocks became floating half bricks).

Now let me read the remaining pass files for y-ranges: StructuresPass.ts (FloatingIslands, SurfaceDecor, LifeCrystals, Pyramid, WetJungle), TreePass.ts, LakesPass.ts, CleanupPass.ts, BeachPass.ts, JunglePass, DesertPass, IceBiomePass, GrassPass, MushroomPass, MarbleGranitePass, DirtToMudPass, CorruptionPass, GenState, MountCavesPass, ShiniesPass, DungeonPass, TemplePass, IslandHousePass, SwordShrinePass, BuriedChestsPass, TrapsPass, HellFortPass.

Let me read StructuresPass.ts and TreePass.ts next (probably big).
````

</details>


---

## 🤖 Assistant · 2026-08-11T04:08:59.718Z · glm-x-preview-260804

```
已找到核心机制。现在让我读取 `StructuresPass` (FloatingIslands/SurfaceDecor) 和 `TreePass`。
```


---

## 🤖 Assistant · 2026-08-11T04:08:59.843Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:08:59.864Z

**📎 ToolResult**

```
1	// 阶段 4 结构 pass:
2	// - FloatingIslands(pass 19,L5552 + CloudIsland L47397 简化):云岛(云 189 壳 + 土芯 + 草皮)
3	// - LifeCrystals(pass 55,L7828):area×2e-5 个生命水晶(岩层空腔地上)
4	// - HellHouses 已由 HellFortPass.runHellFortPass 取代
5	// - SurfaceDecor:生物群系感知地表(丛林/雪原树密度、沙漠仙人掌、丛林藤蔓/蘑菇)
6	import type { TileStore } from '../../TileStore';
7	import type { RNG } from '../../../core/rng';
8	import type { GenState } from './GenState';
9	import { T, TILE_BY_KEY } from '../../../data/tiles';
10	import { ITEM_BY_KEY } from '../../../data/items';
11	import { digTunnel } from './TileRunner';
12	
13	const CLOUD = TILE_BY_KEY['v_189_cloud_block']!;
14	const EBONSAND = TILE_BY_KEY['v_112_ebonsand_block']!;
15	const CRIMSAND = TILE_BY_KEY['v_234_crimsand_block']!;
16	const JUNGLE_GRASS = TILE_BY_KEY['v_60_jungle_grass_block']!;
17	const CACTUS = TILE_BY_KEY['v_80_cactus']!;
18	const VINE = TILE_BY_KEY['v_52_vines']!;
19	const HEART = TILE_BY_KEY['crystal_heart']!;
20	
21	
22	export function runFloatingIslandsPass(st: TileStore, rng: RNG, gs: GenState): void {
23	  const { w } = st;
24	  // 原版 pass 21（L5552-5637）：岛数 = w*0.0008，另加 skyLakes（1 + w>8000 + w>6000）。
25	  // 前 islands 个 = CloudIsland，其余 = CloudLake；间距/中心避让为固定值（不缩放）
26	  const islands = Math.floor(w * 0.0008);
27	  let skyLakes = 1;
28	  if (w > 8000) skyLakes++;
29	  if (w > 6000) skyLakes++;
30	  const total = islands + skyLakes;
31	  const placed: number[] = [];
32	  let lakeIdx = 0;
33	  for (let n = 0; n < total; n++) {
34	    let x = 0, ok = false;
35	    for (let attempt = 0; attempt < 200 && !ok; attempt++) {
36	      x = rng.int(Math.floor(w * 0.1), Math.floor(w * 0.9) - 1);
37	      while (x > w / 2 - 150 && x < w / 2 + 150) {
38	        x = rng.int(Math.floor(w * 0.1), Math.floor(w * 0.9) - 1);
39	      }
40	      ok = placed.every((px) => Math.abs(px - x) >= 180);
41	    }
42	    // 该列地表（原版从 y=200 起扫）
43	    let surf = 0;
44	    let found = false;
45	    for (let y = 200; y < gs.worldSurface; y++) {
46	      if (st.flags[st.idx(x, y)]) { surf = y; found = true; break; }
47	    }
48	    if (!found) continue;
49	    const y = Math.min(rng.int(90, Math.max(91, surf - 100)), gs.worldSurfaceLow - 50);
50	    const isLake = lakeIdx >= islands;
51	    if (isLake) cloudLake(st, rng, x, y);
52	    else cloudIsland(st, rng, x, y);
53	    placed.push(x);
54	    gs.floatingIslands.push({ x, y, style: 0, isLake });
55	    if (!isLake) lakeIdx++;
56	  }
57	}
58	
59	/** 雨云凸包（CloudIsland L47484-47522 / CloudLake 尾段同构）：
60	 *  自 bbox 左+Next(5) 起，步进 Next(r, 1.5r)；每步从岛底向上找实心面，
61	 *  中心下移 Next(-3,4)，椭圆 r=Next(4,8)（纵压×2），1/4 雨云 196 其余云 189 */
62	function rainBumps(st: TileStore, rng: RNG, bx0: number, bx1: number, by0: number, by1: number): void {
63	  const RAIN = TILE_BY_KEY['v_196_rain_cloud_block']!;
64	  let r = rng.int(4, 7);
65	  for (let x = bx0 + rng.int(0, 4); x < bx1; x += rng.int(r, Math.floor(r * 1.5))) {
66	    let y = by1;
67	    while (y > 1 && !st.flags[st.idx(x, y)]) y--;
68	    const cy = y + rng.int(-3, 3);
69	    r = rng.int(4, 7);
70	    const mat = rng.int(0, 3) === 0 ? RAIN : CLOUD;
71	    for (let dx = -r; dx <= r; dx++) {
72	      for (let dy = -r; dy <= r; dy++) {
73	        const tx = x + dx, ty = cy + dy;
74	        if (ty <= by0 || !st.inBounds(tx, ty)) continue;
75	        if (Math.hypot(dx, dy * 2) < r + rng.int(0, 1)) {
76	          const ti = st.idx(tx, ty);
77	          st.type[ti] = mat; st.flags[ti] = 1;
78	        }
79	      }
80	    }
81	  }
82	}
83	
84	/** CloudLake（L47704）：天湖 = 纯云盘 + 雨云凸包（无土芯/无墙/无水池） */
85	function cloudLake(st: TileStore, rng: RNG, i: number, j: number): void {
86	  let num1 = rng.int(100, 149);
87	  let steps = rng.int(20, 29);
88	  let px = i + 0.0, py = j + 0.0;
89	  let vx = rng.int(-20, 20) * 0.2;
90	  while (vx > -2 && vx < 2) vx = rng.int(-20, 20) * 0.2;
91	  let vy = rng.int(-20, -11) * 0.02;
92	  let bx0 = i, bx1 = i, by0 = j, by1 = j;
93	  while (num1 > 0 && steps > 0) {
94	    num1 -= rng.int(0, 3);
95	    steps--;
96	    const x0 = Math.max(0, Math.floor(px - num1 * 0.5)), x1 = Math.min(st.w, Math.floor(px + num1 * 0.5));
97	    const y0 = Math.max(0, Math.floor(py - num1 * 0.5)), y1 = Math.min(st.h, Math.floor(py + num1 * 0.5));
98	    const r = num1 * rng.int(80, 119) * 0.01;
99	    let top = py + 1;
100	    for (let x = x0; x < x1; x++) {
101	      if (rng.next() < 0.5) top += rng.int(-1, 1);
102	      top = Math.max(py, Math.min(py + 2, top));
103	      for (let y = y0; y < y1; y++) {
104	        if (y <= top || !st.inBounds(x, y)) continue;
105	        if (Math.hypot(x - px, (y - py) * 3) < r * 0.4) {
106	          const ti = st.idx(x, y);
107	          st.type[ti] = CLOUD; st.flags[ti] = 1;
108	          bx0 = Math.min(bx0, x); bx1 = Math.max(bx1, x);
109	          by0 = Math.min(by0, y); by1 = Math.max(by1, y);
110	        }
111	      }
112	    }
113	    px += vx; py += vy;
114	    vx += rng.int(-20, 20) * 0.05;
115	    vx = Math.max(-1, Math.min(1, vx));
116	    vy = Math.max(-0.2, Math.min(0.2, vy));
117	  }
118	  if (bx1 > bx0) rainBumps(st, rng, bx0, bx1, by0, by1);
119	}
120	
121	/** CloudIsland(L47397)核心移植:扁平云盘(纵压3+顶面游走)→雨云凸包→
122	 * 土芯只嵌云内 → 内部云墙 73 → 10% 水池。岛屋由独立 pass 处理。 */
123	function cloudIsland(st: TileStore, rng: RNG, i: number, j: number): void {
124	  let num1 = rng.int(100, 149);
125	  let steps = rng.int(20, 29);
126	  let px = i + 0.0, py = j + 0.0;
127	  let vx = rng.int(-20, 20) * 0.2;
128	  while (vx > -2 && vx < 2) vx = rng.int(-20, 20) * 0.2;
129	  let vy = rng.int(-20, -11) * 0.02;
130	  let bboxX0 = i, bboxX1 = i, bboxY0 = j, bboxY1 = j;
131	  while (num1 > 0 && steps > 0) {
132	    num1 -= rng.int(0, 3);
133	    steps--;
134	    const x0 = Math.max(0, Math.floor(px - num1 * 0.5)), x1 = Math.min(st.w, Math.floor(px + num1 * 0.5));
135	    const y0 = Math.max(0, Math.floor(py - num1 * 0.5)), y1 = Math.min(st.h, Math.floor(py + num1 * 0.5));
136	    const r = num1 * rng.int(80, 119) * 0.01;
137	    let top = py + 1; // 每列顶面游走(钳 [py, py+2])
138	    for (let x = x0; x < x1; x++) {
139	      if (rng.next() < 0.5) top += rng.int(-1, 1);
140	      top = Math.max(py, Math.min(py + 2, top));
141	      for (let y = y0; y < y1; y++) {
142	        if (y <= top || !st.inBounds(x, y)) continue;
143	        if (Math.hypot(x - px, (y - py) * 3) < r * 0.4) {
144	          const ti = st.idx(x, y);
145	          st.type[ti] = CLOUD;
146	          st.flags[ti] = 1;
147	          bboxX0 = Math.min(bboxX0, x); bboxX1 = Math.max(bboxX1, x);
148	          bboxY0 = Math.min(bboxY0, y); bboxY1 = Math.max(bboxY1, y);
149	        }
150	      }
151	    }
152	    px += vx;
153	    py += vy;
154	    vx += rng.int(-20, 20) * 0.05;
155	    vx = Math.max(-1, Math.min(1, vx));
156	    vy = Math.max(-0.2, Math.min(0.2, vy));
157	  }
158	  if (bboxX1 <= bboxX0) return;
159	  // ---- 阶段2:雨云凸包（L47484-47522） ----
160	  rainBumps(st, rng, bboxX0, bboxX1, bboxY0, bboxY1);
161	  // ---- 阶段3:土芯(80-95,只把云换土)----
162	  let dR = rng.int(80, 94);
163	  let dSteps = rng.int(10, 14);
164	  let dx0 = i + 0.0, dy0 = bboxY0 + 0.0;
165	  let dvx = rng.int(-20, 20) * 0.2;
166	  while (dvx > -2 && dvx < 2) dvx = rng.int(-20, 20) * 0.2;
167	  let dvy = rng.int(-20, -11) * 0.02;
168	  while (dR > 0 && dSteps > 0) {
169	    dR -= rng.int(0, 3);
170	    dSteps--;
171	    const x0 = Math.max(0, Math.floor(dx0 - dR * 0.5)), x1 = Math.min(st.w, Math.floor(dx0 + dR * 0.5));
172	    const y0 = Math.max(0, Math.floor(dy0 - dR * 0.5)), y1 = Math.min(st.h, Math.floor(dy0 + dR * 0.5));
173	    const r = dR * rng.int(80, 119) * 0.01;
174	    for (let x = x0; x < x1; x++) {
175	      for (let y = y0; y < y1; y++) {
176	        if (!st.inBounds(x, y)) continue;
177	        const ti = st.idx(x, y);
178	        if (st.type[ti] === CLOUD && Math.hypot(x - dx0, (y - dy0) * 3) < r * 0.4) {
179	          st.type[ti] = T.DIRT;
180	        }
181	      }
182	    }
183	    dx0 += dvx;
184	    dy0 += dvy;
185	    dvx += rng.int(-20, 20) * 0.05;
186	    dvx = Math.max(-1, Math.min(1, dvx));
187	    dvy = Math.max(-0.2, Math.min(0.2, dvy));
188	  }
189	  // ---- 阶段5:内部云墙(3×3 全包裹 → wall 73)----
190	  for (let x = bboxX0; x <= bboxX1; x++) {
191	    for (let y = bboxY0; y <= bboxY1; y++) {
192	      let all = true;
193	      for (let ax = -1; ax <= 1 && all; ax++) {
194	        for (let ay = -1; ay <= 1; ay++) {
195	          if (!st.inBounds(x + ax, y + ay) || !st.flags[st.idx(x + ax, y + ay)]) { all = false; break; }
196	        }
197	      }
198	      if (all) st.wall[st.idx(x, y)] = 73;
199	    }
200	  }
201	  // ---- 阶段6:水池(每列 10% 在云顶凹处放水)----
202	  for (let x = bboxX0 + 2; x < bboxX1 - 2; x++) {
203	    if (rng.next() >= 0.1) continue;
204	    let y = Math.max(1, bboxY0 - 10);
205	    while (y < st.h - 1 && !st.flags[st.idx(x, y)]) y++;
206	    const below = st.idx(x, y + 1);
207	    if (y < bboxY1 && st.type[below] === CLOUD) {
208	      const ti = st.idx(x, y);
209	      st.type[ti] = 0; st.flags[ti] = 0;
210	      st.liquid[ti] = 255; st.liquidType[ti] = 1;
211	    }
212	  }
213	}
214	
215	/** 生命水晶(pass 57):area×2e-5,岩层空腔地面 */
216	export function runLifeCrystalsPass(st: TileStore, rng: RNG, gs: GenState): void {
217	  const { w, h } = st;
218	  const yMin = Math.floor((gs.worldSurface * 2 + gs.rockLevel) / 3);
219	  const count = Math.floor(w * h * 0.00002);
220	  let placed = 0;
221	  for (let n = 0; n < count * 30 && placed < count; n++) {
222	    const x = rng.int(40, w - 41);
223	    const y = rng.int(yMin, Math.max(yMin + 1, h - 300));
224	    if (!st.inBounds(x, y + 1) || !st.inBounds(x + 1, y + 1)) continue;
225	    // 2×2 净空 + 下方实心
226	    let clear = true;
227	    for (let dx = 0; dx < 2; dx++) {
228	      for (let dy = 0; dy < 2; dy++) {
229	        if (st.flags[st.idx(x + dx, y - dy)]) { clear = false; break; }
230	      }
231	    }
232	    if (!clear || !st.isSolid(x, y + 1) || !st.isSolid(x + 1, y + 1)) continue;
233	    // 原版 AddLifeCrystal(cs:16023-16038):顶行 frameY=0、底行 18
234	    st.setTileSilent(x, y - 1, HEART, 0, 0);
235	    st.setTileSilent(x + 1, y - 1, HEART, 18, 0);
236	    st.setTileSilent(x, y, HEART, 0, 18);
237	    st.setTileSilent(x + 1, y, HEART, 18, 18);
238	    placed++;
239	  }
240	}
241	
242	/** 地表装饰:按生物群系种树/仙人掌/藤蔓/蘑菇(原版 pass 60+ 系列简化) */
243	export function runSurfaceDecorPass(st: TileStore, rng: RNG, gs: GenState): void {
244	  const { w, h } = st;
245	  const isSoft = (t: number) => t === T.TALLGRASS || t === T.FLOWER || t === T.MUSHROOM || t === VINE;
246	  const ud = gs.undergroundDesert;
247	  const inDesert = (x: number) => !!ud && x >= ud.x0 && x <= ud.x1;
248	  let x = rng.int(6, 14);
249	  let sinceLast = 0;
250	  while (x < w - 6) {
251	    let sy = -1;
252	    for (let y = 0; y < h; y++) {
253	      if (st.flags[st.idx(x, y)]) { sy = y; break; }
254	    }
255	    if (sy >= 0) {
256	      const ground = st.type[st.idx(x, sy)];
257	      const relaxed = sinceLast >= 24;
258	      // ---- 树已由 vanilla/TreePass.ts 替换（原版 AddTrees 逐列语义）----
259	      // ---- 仙人掌(沙漠沙/邪恶沙面)----
260	      if ((ground === T.SAND || ground === EBONSAND || ground === CRIMSAND) && inDesert(x)
261	        && !st.flags[st.idx(x, sy - 1)] && rng.next() < 0.12) {
262	        const ch = rng.int(2, 5);
263	        let ok = true;
264	        for (let dy = 1; dy <= ch; dy++) if (st.flags[st.idx(x, sy - dy)]) { ok = false; break; }
265	        if (ok) {
266	          for (let dy = 1; dy <= ch; dy++) st.setTileSilent(x, sy - dy, CACTUS, 0, 0);
267	          x += rng.int(4, 9);
268	          sinceLast = 0;
269	          continue;
270	        }
271	      }
272	      // ---- 杂草/花/蘑菇 ----(藤蔓在下方统一扫描)
273	      // ---- 杂草/花/蘑菇 ----
274	      if (!st.flags[st.idx(x, sy - 1)] && (ground === T.GRASS || ground === JUNGLE_GRASS || ground === T.SNOW)) {
275	        const r = rng.next();
276	        if (r < 0.3) st.setTileSilent(x, sy - 1, T.TALLGRASS, [0, 18, 36, 54, 72, 90][rng.int(0, 5)], 0);
277	        else if (r < 0.42) st.setTileSilent(x, sy - 1, T.FLOWER, [108, 126, 162, 180, 216, 252, 342, 540, 594][rng.int(0, 8)], 0);
278	        else if (r < 0.45 && ground !== T.SNOW) st.setTileSilent(x, sy - 1, T.MUSHROOM, 144, 0);
279	      }
280	    }
281	    x++;
282	    sinceLast++;
283	  }
284	  // ---- 藤蔓:挂在悬空草根/草皮下方(洞穴顶/崖底)----
285	  for (let vx = 2; vx < w - 2; vx++) {
286	    for (let vy = 2; vy < h - 2; vy++) {
287	      const i = st.idx(vx, vy);
288	      if (st.type[i] !== JUNGLE_GRASS && st.type[i] !== T.GRASS) continue;
289	      if (!st.flags[i] || st.flags[st.idx(vx, vy + 1)]) continue;
290	      if (st.liquid[st.idx(vx, vy + 1)] > 0) continue;
291	      if (rng.next() < 0.5) continue;
292	      const len = rng.int(1, 8);
293	      for (let k = 1; k <= len; k++) {
294	        const ii = st.idx(vx, vy + k);
295	        if (vy + k >= h - 1 || st.flags[ii] || st.type[ii] !== 0) break;
296	        st.setTileSilent(vx, vy + k, VINE, 0, 0);
297	      }
298	      vy += 10; // 稀疏
299	    }
300	  }
301	}
302	
303	const SANDSTONE_BRICK = TILE_BY_KEY['v_151_sandstone_brick']!;
304	const CHEST = TILE_BY_KEY['chest']!;
305	
306	/** 金字塔(pass 38 Pyramids 简化):gs.pyramidSpots 候选 → 地下沙岩砖金字塔 + 宝箱 */
307	export function runPyramidPass(
308	  st: TileStore, rng: RNG, gs: GenState,
309	  chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null> }>,
310	): void {
311	  for (const spot of gs.pyramidSpots.slice(0, 2)) {
312	    const size = rng.int(14, 20); // 半宽
313	    const baseY = Math.min(st.h - 260, spot.y + rng.int(60, 90));
314	    if (spot.x < size + 5 || spot.x > st.w - size - 5) continue;
315	    // 金字塔主体(逐层收窄)
316	    for (let layer = 0; layer < size; layer++) {
317	      const halfW = size - layer;
318	      for (let x = spot.x - halfW; x <= spot.x + halfW; x++) {
319	        for (let y = baseY - layer; y <= baseY - layer; y++) {
320	          const i = st.idx(x, y);
321	          st.type[i] = SANDSTONE_BRICK; st.flags[i] = 1;
322	          st.wall[i] = 34; // SandstoneBrickUnsafe
323	        }
324	      }
325	    }
326	    // 内腔(倒阶梯掏空)
327	    for (let layer = 2; layer < size - 2; layer++) {
328	      const halfW = size - layer - 2;
329	      for (let x = spot.x - halfW; x <= spot.x + halfW; x++) {
330	        const i = st.idx(x, baseY - layer);
331	        st.type[i] = 0; st.flags[i] = 0;
332	      }
333	    }
334	    // 宝箱(内腔底部,cs L12417-12426):style1 金箱,战利品三选一
335	    // (857 沙暴瓶/848 法老面具/934 飞毯)
336	    const bx = spot.x, by = baseY - 2;
337	    st.setTileSilent(bx, by, CHEST, 1 * 36, 0);
338	    st.setTileSilent(bx + 1, by, CHEST, 1 * 36 + 18, 0);
339	    st.setTileSilent(bx, by + 1, CHEST, 1 * 36, 18);
340	    st.setTileSilent(bx + 1, by + 1, CHEST, 1 * 36 + 18, 18);
341	    const lootKeys = ['vi_857_sandstorm_in_a_bottle', 'vi_848_PharaohsMask', 'vi_934_FlyingCarpet'];
342	    const lootId = ITEM_BY_KEY[lootKeys[rng.int(0, 2)]];
343	    chests.push({
344	      x: bx, y: by,
345	      items: lootId !== undefined ? [{ id: lootId, stack: 1 }, ...Array(9).fill(null)] : Array(10).fill(null),
346	    });
347	  }
348	}
349	
350	/** Wet Jungle(pass 43 简化):从丛林草 tile 起挖湿隧道(灌水) */
351	export function runWetJunglePass(st: TileStore, rng: RNG, gs: GenState): void {
352	  const core = (gs as any).jungleCoreX ?? gs.jungleX;
353	  const JG = JUNGLE_GRASS;
354	  const tunnels = Math.max(4, Math.floor(st.w / 500)); // C# (int)
355	  let dug = 0;
356	  for (let n = 0; n < tunnels * 60 && dug < tunnels; n++) {
357	    const x = core + rng.int(-Math.floor(st.w * 0.12), Math.floor(st.w * 0.12));
358	    const y = rng.int(gs.rockLevel, Math.max(gs.rockLevel + 1, st.h - 500));
359	    if (!st.inBounds(x, y) || st.type[st.idx(x, y)] !== JG || !st.flags[st.idx(x, y)]) continue;
360	    const dx = rng.int(-100, 100) * 0.01, dy = rng.int(-100, 100) * 0.01;
361	    digTunnel(st, rng, x, y, dx, dy, rng.int(30, 120), rng.int(3, 6), true);
362	    dug++;
363	  }
364	}
365	
366	
367	

```


---

## 🤖 Assistant · 2026-08-11T04:09:00.131Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/*.ts",
 "description": "Count lines of vanilla pass files"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:00.172Z

**📎 ToolResult**

```
     271 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts
     219 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts
     186 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CavesPass.ts
     118 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CleanupPass.ts
     645 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts
     259 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts
      40 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DirtToMudPass.ts
    1635 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts
      74 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenState.ts
      30 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GrassPass.ts
     174 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts
     337 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HellFortPass.ts
     444 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HiveSpiderPass.ts
     102 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IceBiomePass.ts
     124 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IslandHousePass.ts
     206 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/JunglePass.ts
     184 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LakesPass.ts
     116 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts
     180 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts
     118 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MushroomPass.ts
     115 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/ShiniesPass.ts
      75 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/Spread.ts
     366 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts
     100 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SwordShrinePass.ts
     532 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts
     147 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TerrainPass.ts
     234 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts
     320 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts
     245 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TreePass.ts
    7596 total

```


---

## 🤖 Assistant · 2026-08-11T04:09:11.193Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Important: StructuresPass FloatingIslands writes cloud blocks (flags=1!) into the sky at y ~90 to worldSurfaceLow-50 — these are REAL sky blocks (intended, floating islands). These are NOT removed later.

Wait — but they're placed in `vanillaBiomes` at pass index 4 ("生物群系"). And hellPass runs later but only touches y > h-190. So islands survive.

But the question is about "生成早期往天空写入大量杂块、后期又被抹除". The ghost type mechanism fits: TileRunner writes type into air (flags=0), including sky, and finalize zeroes all `type[i] != 0` where `!flags[i]`. Note finalize also zeroes `flags[i]=0` when type[i]===0.

But wait — there's another subtlety: the ghost-type writes happen for ALL placing tileRunner calls whose y range covers sky. The biggest: CavesPass line 25 `run(area * 0.00015, 0, gs.worldSurfaceLow, T.STONE, 4, 14, 5, 39)` — yMin=0 means start y can be anywhere from 0 (top of the world, deep sky!) to worldSurfaceLow. That's the vanilla "Rocks In Dirt" first band. With strength 4-14 and steps 5-39, these runners wander and paint ghost stone into sky air cells. Hmm, but actually does vanilla have yMin 0 there? Let me recall vanilla WorldGen.cs:

```csharp
// 8 - "Rocks in Dirt"
double num = (double)(Main.maxTilesX * Main.maxTilesY) * 0.00015;
for (...) {
  int i = GenBase._random.Next(0, Main.maxTilesX - 1);
  int j = GenBase._random.Next(0, (int)Main.worldSurfaceLow);  // ← yes, 0!
  WorldGen.TileRunner(i, j, strength 4-14, steps 5-39, 1);
}
```

Actually I believe vanilla uses `(int)Main.worldSurfaceLow` — hmm. Vanilla code (pass list in GenerateWorld):

```csharp
currentPass = new PassLegacy("Rocks In Dirt", delegate(GenerationProgress progress, GameConfiguration configuration)
{
    progress.Message = Lang.gen[12].Value;
    double num = (double)(Main.maxTilesX * Main.maxTilesY) * 0.00015;
    for (int num2 = 0; num2 < num; num2++)
    {
        WorldGen.TileRunner(GenBase._random.Next(0, Main.maxTilesX - 1), GenBase._random.Next(0, (int)Main.worldSurfaceLow), GenBase._random.Next(4, 14), GenBase._random.Next(5, 39), 1);
    }
    ...
```

I'm fairly confident that's right — y from 0 to worldSurfaceLow. So the port is 1:1 with vanilla, and in vanilla those runners only convert existing active tiles (dirt) to stone — in air, they write ghost type but invisible. Here the same. So sky ghost writes come from this and others.

Let me now check the other passes for y ranges. I need:
- TreePass (trees grow above surface — writes trunk into sky, intended, stays)
- LakesPass (water in sky? lakes pass digs and fills)
- CleanupPass (cleanup: what does it erase — "连通小块(<20)清除")
- BeachPass
- JunglePass (mud runners — y range? mud vy pushes; mud runner can climb above surface?)
- DesertPass (sand above surface?)
- IceBiomePass, GrassPass, MushroomPass, MarbleGranitePass, DirtToMudPass, CorruptionPass, MountCavesPass, ShiniesPass, GenState

Let me read them in parallel — the small ones first.
````

</details>


---

## 🤖 Assistant · 2026-08-11T04:09:11.320Z · glm-x-preview-260804

```
现在让我分批读取剩余的 pass 文件。
```


---

## 🤖 Assistant · 2026-08-11T04:09:11.473Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TreePass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:11.484Z

**📎 ToolResult**

```
1	// 原版 pass 82 "Planting Trees" 1:1（1405 WorldGen.cs:9651-9670 + AddTrees:15642 +
2	// GrowTree:14171 + GrowPalmTree:11785 + GrowEpicTree:11850 + RandomizeTreeStyle:2817）。
3	// 帧表逐格核对自源码（Tiles_5 网格 22px）：干身 8 case×3 变体 + 侧枝/根部/基座/树冠标记帧。
4	// 渲染端 VanillaTiler.drawTreeCell 消费同一语义（fy≥198 为树冠标记帧；棕榈 sheet 323）。
5	// RNG 映射：Next(a,b) → rng.int(a, b-1)。
6	import { TileStore } from '../../TileStore';
7	import type { RNG } from '../../../core/rng';
8	import type { GenState } from './GenState';
9	import { idsByVanillaSheet } from './TileRunner';
10	import { T, TILE_BY_KEY } from '../../../data/tiles';
11	
12	const TREE = TILE_BY_KEY['tree']!;              // tile 5
13	const PALM = TILE_BY_KEY['v_323_palm_trees']!;  // tile 323
14	/** IsTileTypeFitForTree（L14147）：草族 9 种 */
15	const FIT = idsByVanillaSheet(2, 23, 60, 70, 109, 147, 199, 477, 492);
16	/** GrowTree 头部墙白名单（L14176：0/80/106/107/138-141/145/150/152） */
17	const TREE_WALLS = new Set([0, 80, 106, 107, 138, 139, 140, 141, 145, 150, 152]);
18	/** 棕榈基座沙族（L11793：53/234/116/112） */
19	const PALM_GROUND = idsByVanillaSheet(53, 234, 116, 112);
20	const JUNGLE_GRASS = idsByVanillaSheet(60);
21	/** 植物（vanilla tile 20）：GrowTree 头部越过找基座（原版 while type==20） */
22	const PLANTS = idsByVanillaSheet(20);
23	
24	/** 干身帧表：num5 case → num4(变体 0-2) → [fx,fy]（L14213-14425 逐 case 提取） */
25	const TRUNK: Record<number, Array<[number, number]>> = {
26	  0: [[0, 0], [0, 22], [0, 44]],
27	  1: [[0, 66], [0, 88], [0, 110]],
28	  2: [[22, 0], [22, 22], [22, 44]],
29	  3: [[44, 66], [44, 88], [44, 110]],
30	  4: [[22, 66], [22, 88], [22, 110]],
31	  5: [[88, 0], [88, 22], [88, 44]],
32	  6: [[66, 66], [66, 88], [66, 110]],
33	  7: [[110, 66], [110, 88], [110, 110]],
34	  8: [[0, 0], [0, 22], [0, 44]],
35	  9: [[0, 0], [0, 22], [0, 44]],
36	};
37	
38	/** EmptyTileCheck（L15685，ignoreID=-1 简化：出界 false，任何实心 false） */
39	function emptyTileCheck(st: TileStore, x0: number, x1: number, y0: number, y1: number): boolean {
40	  if (x0 < 0 || x1 >= st.w || y0 < 0 || y1 >= st.h) return false;
41	  for (let x = x0; x <= x1; x++) {
42	    for (let y = y0; y <= y1; y++) {
43	      if (st.flags[st.idx(x, y)]) return false;
44	    }
45	  }
46	  return true;
47	}
48	
49	/** 树干+枝+根+冠 共体（GrowTree L14203-14606 / GrowEpicTree 同表）。
50	 *  groundType：基座 tile（判丛林加高）；返回是否成树 */
51	function growTrunk(st: TileStore, rng: RNG, gs: GenState, i: number, index1: number, height: number): boolean {
52	  let flagL = false, flagR = false; // 侧枝去重（num5 5/7 左、6/7 右不同帧连续限制）
53	  for (let y = index1 - height; y < index1; y++) {
54	    // num4 = 枝型 0-9；顶/底强制 0；5/7 与 6/7 连续出现需重投
55	    let num5 = rng.int(0, 9);
56	    if (y === index1 - 1 || y === index1 - height) num5 = 0;
57	    while (((num5 === 5 || num5 === 7) && flagL) || ((num5 === 6 || num5 === 7) && flagR)) {
58	      num5 = rng.int(0, 9);
59	    }
60	    flagL = false; flagR = false;
61	    if (num5 === 5 || num5 === 7) flagL = true;
62	    if (num5 === 6 || num5 === 7) flagR = true;
63	    const num4 = rng.int(0, 2);
64	    const [fx, fy] = TRUNK[num5][num4];
65	    st.setTileSilent(i, y, TREE, fx, fy);
66	    // 侧枝帧（L14362-14426）：Next(3)<2 走 198+ 行（贴干枝），否则行内变体
67	    if (num5 === 5 || num5 === 7) {
68	      const k = rng.int(0, 2);
69	      const [bfx, bfy] = rng.int(0, 2) < 2 ? [44, 198 + k * 22] : [66, k * 22];
70	      st.setTileSilent(i - 1, y, TREE, bfx, bfy);
71	    }
72	    if (num5 === 6 || num5 === 7) {
73	      const k = rng.int(0, 2);
74	      const [bfx, bfy] = rng.int(0, 2) < 2 ? [66, 198 + k * 22] : [88, 66 + k * 22];
75	      st.setTileSilent(i + 1, y, TREE, bfx, bfy);
76	    }
77	  }
78	  // 基座方向 num7（L14439-14543）：两侧地面适配 → 决定根部与基座帧。
79	  //  侧根放置前提 = 邻格整砖(L30230/30234:!halfBrick && slope==0)——半砖/坡面侧不出根
80	  const fitSide = (dx: number) => {
81	    if (!st.inBounds(i + dx, index1)) return false;
82	    const si = st.idx(i + dx, index1);
83	    return !!st.flags[si] && !st.half[si] && st.slope[si] === 0 && FIT.has(st.type[si]);
84	  };
85	  let num7 = rng.int(0, 2);
86	  const sideL = fitSide(-1), sideR = fitSide(1);
87	  if (!sideL) { if (num7 === 0) num7 = 2; else if (num7 === 1) num7 = 3; }
88	  if (!sideR) { if (num7 === 0) num7 = 1; else if (num7 === 2) num7 = 3; }
89	  if (sideL && !sideR) num7 = 2;
90	  if (sideR && !sideL) num7 = 1;
91	  const k8 = rng.int(0, 2);
92	  if (num7 === 0 || num7 === 1) st.setTileSilent(i + 1, index1 - 1, TREE, 22, 132 + k8 * 22); // 右根
93	  if (num7 === 0 || num7 === 2) st.setTileSilent(i - 1, index1 - 1, TREE, 44, 132 + k8 * 22); // 左根
94	  // 基座干身（switch num7，L14519-14566）
95	  const baseFx = num7 === 0 ? 88 : num7 === 1 ? 0 : num7 === 2 ? 66 : -1;
96	  if (baseFx >= 0) st.setTileSilent(i, index1 - 1, TREE, baseFx, 132 + k8 * 22);
97	  // 树冠标记帧（L14568-14600）：12/13 fx=22，否则 fx=0；fy=198+22*k
98	  const crownFx = rng.int(0, 12) !== 0 ? 22 : 0;
99	  st.setTileSilent(i, index1 - height, TREE, crownFx, 198 + rng.int(0, 2) * 22);
100	  gs.genTrees.push({ x: i, y: index1 - height, h: height }); // 砍伐整棵判定用
101	  return true;
102	}
103	
104	/** GrowTree（L14171）：常规树。height=Next(5,17)；丛林草基座净空 +5 */
105	function growTree(st: TileStore, rng: RNG, gs: GenState, i: number, y: number): boolean {
106	  let index1 = y;
107	  while (st.inBounds(i, index1) && st.flags[st.idx(i, index1)] && PLANTS.has(st.type[st.idx(i, index1)])) index1++;
108	  if (!st.inBounds(i, index1) || index1 < 1) return false;
109	  const gi = st.idx(i, index1);
110	  // 头部适配检查：基座上一格三列无液体 / 基座活跃且适树且整砖(L29934:!halfBrick&&slope==0) /
111	  // 上格墙白名单 / 至少一侧邻格适树（侧根前提同款整砖检查）
112	  if (st.liquid[st.idx(i - 1, index1 - 1)] > 0 || st.liquid[st.idx(i, index1 - 1)] > 0 || st.liquid[st.idx(i + 1, index1 - 1)] > 0) return false;
113	  if (!st.flags[gi] || st.half[gi] || st.slope[gi] !== 0 || !FIT.has(st.type[gi])) return false;
114	  if (!TREE_WALLS.has(st.wall[st.idx(i, index1 - 1)])) return false;
115	  const fitSide = (dx: number) => {
116	    if (!st.inBounds(i + dx, index1)) return false;
117	    const si = st.idx(i + dx, index1);
118	    return !!st.flags[si] && !st.half[si] && st.slope[si] === 0 && FIT.has(st.type[si]);
119	  };
120	  if (!fitSide(-1) && !fitSide(1)) return false;
121	  const height = rng.int(5, 16);                       // Next(5,17)
122	  let clear = height + 4;                              // num3
123	  if (JUNGLE_GRASS.has(st.type[gi])) clear += 5;
124	  if (!emptyTileCheck(st, i - 2, i + 2, index1 - clear, index1 - 1)) return false;
125	  return growTrunk(st, rng, gs, i, index1, height);
126	}
127	
128	/** GrowEpicTree（L11850）：巨型树。基座严格草(2)、邻格草族、净空 55、height=Next(20,30) */
129	function growEpicTree(st: TileStore, rng: RNG, gs: GenState, i: number, y: number): boolean {
130	  let index1 = y;
131	  while (st.inBounds(i, index1) && st.flags[st.idx(i, index1)] && PLANTS.has(st.type[st.idx(i, index1)])) index1++;
132	  if (!st.inBounds(i, index1) || index1 < 1) return false;
133	  const gi = st.idx(i, index1);
134	  const GRASS = idsByVanillaSheet(2);
135	  // 基座整砖检查(GrowEpicTree 同 GrowTree 头部语义:半砖/坡面拒绝)
136	  if (!st.flags[gi] || st.half[gi] || st.slope[gi] !== 0 || !GRASS.has(st.type[gi])) return false;
137	  if (st.wall[st.idx(i, index1 - 1)] !== 0 || st.liquid[st.idx(i, index1 - 1)] > 0) return false;
138	  const family = idsByVanillaSheet(2, 23, 60, 109);
139	  const fitSide = (dx: number) => st.inBounds(i + dx, index1)
140	    && st.flags[st.idx(i + dx, index1)] && family.has(st.type[st.idx(i + dx, index1)]);
141	  if (!fitSide(-1) && !fitSide(1)) return false;
142	  if (!emptyTileCheck(st, i - 2, i + 2, index1 - 55, index1 - 1)) return false;
143	  return growTrunk(st, rng, gs, i, index1, rng.int(20, 29)); // Next(20,30)
144	}
145	
146	/** GrowPalmTree（L11785）：沙滩棕榈，干身倾斜帧 fy=num4（±2 步进趋向 num3） */
147	function growPalmTree(st: TileStore, rng: RNG, i: number, y: number): boolean {
148	  if (!st.inBounds(i, y)) return false;
149	  let index1 = y;
150	  while (st.inBounds(i, index1) && st.flags[st.idx(i, index1)] && PLANTS.has(st.type[st.idx(i, index1)])) index1++;
151	  if (!st.inBounds(i, index1) || index1 < 1) return false;
152	  const gi = st.idx(i, index1);
153	  // 基座整砖检查(GrowPalmTree:27280-27285 active && !halfBrick && slope==0)
154	  if (!st.flags[gi] || st.half[gi] || st.slope[gi] !== 0 || !PALM_GROUND.has(st.type[gi])) return false;
155	  if (st.wall[st.idx(i, index1 - 1)] !== 0 || st.liquid[st.idx(i, index1 - 1)] > 0) return false;
156	  if (!emptyTileCheck(st, i, i, index1 - 2, index1 - 1)) return false;
157	  if (!emptyTileCheck(st, i - 1, i + 1, index1 - 30, index1 - 3)) return false;
158	  const height = rng.int(10, 20);                 // Next(10,21)
159	  const target = rng.int(-8, 8) * 2;              // Next(-8,9)*2
160	  let tilt = 0;
161	  for (let k = 0; k < height; k++) {
162	    if (k === 0) {
163	      st.setTileSilent(i, index1 - 1, PALM, 66, 0);
164	      continue;
165	    }
166	    if (k === height - 1) {
167	      st.setTileSilent(i, index1 - 1 - k, PALM, 22 * rng.int(4, 6), tilt); // 顶段 fx=22*Next(4,7)
168	      continue;
169	    }
170	    if (tilt !== target) {
171	      const prog = k / height;                    // 倾斜步进阈值（L11814-11820）
172	      if (prog >= 0.25 && ((prog < 0.5 && rng.int(0, 12) === 0)
173	        || (prog < 0.7 && rng.int(0, 8) === 0)
174	        || (prog < 0.95 && rng.int(0, 4) === 0) || true)) {
175	        tilt += Math.sign(target) * 2;
176	      }
177	    }
178	    st.setTileSilent(i, index1 - 1 - k, PALM, 22 * rng.int(0, 2), tilt); // fx=22*Next(0,3)
179	  }
180	  return true;
181	}
182	
183	/** AddTrees（L15642）：逐列尝试（~1.6 列间距）；沙滩棕榈按每侧固定概率；
184	 *  草上 1/20 观赏树（柳/樱 GrowTreeWithSettings 未移植——缺对应生成管线，留待 C 批） */
185	export function runTreePass(st: TileStore, rng: RNG, gs: GenState): void {
186	  // EpicTree 林区（pass 82 头段，L9656-9666）：w*0.003 个 25-50 半宽林区逐格尝试
187	  for (let n = 0; n < st.w * 0.003; n++) {
188	    const cx = rng.int(50, st.w - 51);            // Next(50, maxTilesX-50)
189	    const hw = rng.int(25, 49);                  // Next(25, 50)
190	    for (let x = cx - hw; x < cx + hw; x++) {
191	      for (let y = 20; y < gs.worldSurface; y++) growEpicTree(st, rng, gs, x, y);
192	    }
193	  }
194	  const palmL = 0.1 + rng.next() * 0.35;          // 每侧棕榈概率（L15644-45）
195	  const palmR = 0.1 + rng.next() * 0.35;
196	  for (let x = 1; x < st.w - 1; x++) {
197	    for (let y = 20; y < gs.worldSurface; y++) {
198	      if (x < 380) {
199	        if (rng.next() < palmL && st.liquid[st.idx(x, y)] === 0) growPalmTree(st, rng, x, y);
200	      } else if (x > st.w - 380) {
201	        if (rng.next() < palmR && st.liquid[st.idx(x, y)] === 0) growPalmTree(st, rng, x, y);
202	      }
203	      growTree(st, rng, gs, x, y);
204	    }
205	    if (rng.int(0, 2) === 0) x++;                 // Next(3)==0 跳列
206	    if (rng.int(0, 3) === 0) x++;                 // Next(4)==0 跳列
207	  }
208	}
209	
210	/** RandomizeTreeStyle（L2817）：按世界宽掷 treeX 边界与 treeStyle（互异，style0→4 概率 2/3）。
211	 *  Reset pass 调用（L4837，worldID 之后 dungeonSide 之前） */
212	export function randomizeTreeStyle(rng: RNG, w: number): { treeX: number[]; treeStyle: number[] } {
213	  const treeX = [0, 0, 0], treeStyle = [0, 0, 0, 0];
214	  const roll6 = () => rng.int(0, 5);
215	  const fix0 = (arr: number[]) => {
216	    for (let i = 0; i < arr.length; i++) {
217	      if (arr[i] === 0 && rng.int(0, 2) !== 0) arr[i] = 4; // style0 → 4（2/3）
218	    }
219	  };
220	  if (w === 4200) {
221	    treeX[0] = rng.int(Math.floor(w * 0.5 - w * 0.25), Math.floor(w * 0.5 + w * 0.25) - 1);
222	    treeStyle[0] = roll6(); treeStyle[1] = roll6();
223	    while (treeStyle[1] === treeStyle[0]) treeStyle[1] = roll6();
224	    treeX[1] = w; treeX[2] = w;
225	    fix0([treeStyle[0], treeStyle[1]]);
226	  } else if (w === 6400) {
227	    treeX[0] = rng.int(Math.floor(w * 0.334 - w * 0.2), Math.floor(w * 0.334 + w * 0.2) - 1);
228	    treeX[1] = rng.int(Math.floor(w * 0.667 - w * 0.2), Math.floor(w * 0.667 + w * 0.2) - 1);
229	    treeStyle[0] = roll6(); treeStyle[1] = roll6(); treeStyle[2] = roll6();
230	    while (treeStyle[1] === treeStyle[0]) treeStyle[1] = roll6();
231	    while (treeStyle[2] === treeStyle[0] || treeStyle[2] === treeStyle[1]) treeStyle[2] = roll6();
232	    treeX[2] = w;
233	    fix0([treeStyle[0], treeStyle[1], treeStyle[2]]);
234	  } else {
235	    treeX[0] = rng.int(Math.floor(w * 0.25 - w * 0.15), Math.floor(w * 0.25 + w * 0.15) - 1);
236	    treeX[1] = rng.int(Math.floor(w * 0.5 - w * 0.15), Math.floor(w * 0.5 + w * 0.15) - 1);
237	    treeX[2] = rng.int(Math.floor(w * 0.75 - w * 0.15), Math.floor(w * 0.75 + w * 0.15) - 1);
238	    treeStyle[0] = roll6(); treeStyle[1] = roll6(); treeStyle[2] = roll6(); treeStyle[3] = roll6();
239	    while (treeStyle[1] === treeStyle[0]) treeStyle[1] = roll6();
240	    while (treeStyle[2] === treeStyle[0] || treeStyle[2] === treeStyle[1]) treeStyle[2] = roll6();
241	    while (treeStyle[3] === treeStyle[0] || treeStyle[3] === treeStyle[1] || treeStyle[3] === treeStyle[2]) treeStyle[3] = roll6();
242	    fix0(treeStyle);
243	  }
244	  return { treeX, treeStyle };
245	}
246	

```


---

## 🤖 Assistant · 2026-08-11T04:09:11.636Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CleanupPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:11.651Z

**📎 ToolResult**

```
1	// 原版 pass 37 "Clean Up Dirt"(L6873)移植:
2	// 1) 表层天然墙清理:地表以上暴露区的土/雪/丛林/蜂巢墙(2/40/64/86)清除(含左右 ±3 邻列,±2/3 各 50%);
3	// 2) ScanTileColumnAndRemoveClumps(L4141):逐列找竖向连续 < tileCounterMax(20) 的可清实心段,
4	//    连通块总 size < 20 则整块移除(消灭浮空散块)。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T, TILE_DEFS, TILE_BY_KEY } from '../../../data/tiles';
9	
10	const TILE_COUNTER_MAX = 20;
11	const EBONSAND = TILE_BY_KEY['v_112_ebonsand_block']!;
12	const CRIMSAND = TILE_BY_KEY['v_234_crimsand_block']!;
13	
14	export function runCleanupPass(st: TileStore, rng: RNG, gs: GenState): void {
15	  const { w } = st;
16	  // 1) 表层墙清理两遍(cs L6877-6938):
17	  //    左→右(3..w-4):中央清 2/40/64/86;右→左(w-5..5):中央清 2/40/64(不重复清蜂巢墙)。
18	  //    邻列两遍都只清 2/40;沙系 tile(53/112/234,第二遍仅 53)跳过邻列清理
19	  for (let dir = 0; dir < 2; dir++) {
20	    const from = dir === 0 ? 3 : w - 5;
21	    const to = dir === 0 ? w - 4 : 5;
22	    for (let x = from; dir === 0 ? x <= to : x >= to; x += dir === 0 ? 1 : -1) {
23	      let open = true;
24	      for (let y = 0; y < gs.worldSurface; y++) {
25	        if (open) {
26	          clearWallSet(st, x, y, dir === 0 ? [2, 40, 64, 86] : [2, 40, 64]);
27	          const t = st.type[st.idx(x, y)];
28	          const isSand = dir === 0
29	            ? (t === T.SAND || t === EBONSAND || t === CRIMSAND)
30	            : t === T.SAND;
31	          if (!isSand) {
32	            if (clearWallSet(st, x - 1, y, [2, 40])) { /* 邻列 1 恒清 */ }
33	            if (rng.next() < 0.5) clearWallSet(st, x - 2, y, [2, 40]);
34	            if (rng.next() < 0.5) clearWallSet(st, x - 3, y, [2, 40]);
35	            clearWallSet(st, x + 1, y, [2, 40]);
36	            if (rng.next() < 0.5) clearWallSet(st, x + 2, y, [2, 40]);
37	            if (rng.next() < 0.5) clearWallSet(st, x + 3, y, [2, 40]);
38	          }
39	          if (st.flags[st.idx(x, y)]) open = false;
40	        } else {
41	          // 重新开放判定:本格与下方 4 格、左右 2 格全无墙且上方 4 格无活性块
42	          let reopen = true;
43	          for (let dy = 0; dy <= 4 && reopen; dy++) if (st.wall[st.idx(x, y + dy)] !== 0) reopen = false;
44	          for (const dx of [-2, -1, 1, 2]) if (st.wall[st.idx(x + dx, y)] !== 0) reopen = false;
45	          for (let dy = 0; dy <= 3 && reopen; dy++) if (st.flags[st.idx(x, y + dy)]) reopen = false;
46	          if (reopen) open = true;
47	        }
48	      }
49	    }
50	  }
51	  // 2) 连通小块清除(< 20):扫描列范围 [10, w-10)(cs L5519-5521)
52	  for (let x = 10; x < w - 10; x++) scanTileColumnAndRemoveClumps(st, x);
53	}
54	
55	function clearWallSet(st: TileStore, x: number, y: number, set: number[]): boolean {
56	  if (!st.inBounds(x, y)) return false;
57	  const wl = st.wall[st.idx(x, y)];
58	  if (set.includes(wl)) { st.wall[st.idx(x, y)] = 0; return true; }
59	  return false;
60	}
61	
62	/** 可被生成期清除的实心块(关键物块 fw/fh 不算) */
63	function clearable(st: TileStore, i: number): boolean {
64	  const d = TILE_DEFS[st.type[i]];
65	  if (!d) return false;
66	  if (d.vanilla?.fw || d.vanilla?.fh) return false;
67	  return !!d.solid;
68	}
69	
70	function scanTileColumnAndRemoveClumps(st: TileStore, x: number): void {
71	  const { h } = st;
72	  let run = 0, runY = 0;
73	  for (let y = 10; y < h - 10; y++) {
74	    const i = st.idx(x, y);
75	    if (st.flags[i] && TILE_DEFS[st.type[i]]?.solid && clearable(st, i)) {
76	      if (run === 0) runY = y;
77	      run++;
78	    } else {
79	      if (run > 0 && run < TILE_COUNTER_MAX) {
80	        // 连通块计数(BFS,cap 20)
81	        if (tileCounter(st, x, runY) < TILE_COUNTER_MAX) tileCounterKill(st);
82	      }
83	      run = 0;
84	    }
85	  }
86	}
87	
88	const _cx = new Int32Array(TILE_COUNTER_MAX);
89	const _cy = new Int32Array(TILE_COUNTER_MAX);
90	let _cn = 0;
91	
92	function tileCounter(st: TileStore, x: number, y: number): number {
93	  _cn = 0;
94	  tileCounterNext(st, x, y);
95	  return _cn;
96	}
97	
98	function tileCounterNext(st: TileStore, x: number, y: number): void {
99	  if (_cn >= TILE_COUNTER_MAX || x < 5 || x > st.w - 5 || y < 5 || y > st.h - 5) return;
100	  const i = st.idx(x, y);
101	  if (!st.flags[i] || !TILE_DEFS[st.type[i]]?.solid || !clearable(st, i)) return;
102	  for (let k = 0; k < _cn; k++) {
103	    if (_cx[k] === x && _cy[k] === y) return;
104	  }
105	  _cx[_cn] = x; _cy[_cn] = y; _cn++;
106	  tileCounterNext(st, x - 1, y);
107	  tileCounterNext(st, x + 1, y);
108	  tileCounterNext(st, x, y - 1);
109	  tileCounterNext(st, x, y + 1);
110	}
111	
112	function tileCounterKill(st: TileStore): void {
113	  for (let k = 0; k < _cn; k++) {
114	    const i = st.idx(_cx[k], _cy[k]);
115	    st.flags[i] = 0;
116	    st.type[i] = 0;
117	  }
118	}
119	

```


---

## 🤖 Assistant · 2026-08-11T04:09:11.827Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LakesPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:11.843Z

**📎 ToolResult**

```
1	// 原版 pass 31 "Lakes" 1:1（1405 WorldGen.cs:6448-6560 + SonOfLakinater:48516）。
2	// 拒绝采样找地表湖位（避海滩/中心±5%/前湖±150/山丘±100/沙顶/猩红石/宝箱/地下沙漠），
3	// SonOfLakinater 自地表向下蜿蜒掏湖腔并灌水（首步上方漏斗入口 + 周壁泥土壳）。
4	// RNG 映射：Next(a,b) → rng.int(a, b-1)；NextFloat → rng.next()。
5	import { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T, TILE_BY_KEY } from '../../../data/tiles';
9	
10	const MUD = TILE_BY_KEY['mud']!;
11	const JUNGLE_GRASS = TILE_BY_KEY['v_60_jungle_grass_block']!;
12	const SAND = TILE_BY_KEY['sand']!;
13	const CRIMSTONE = TILE_BY_KEY['v_203_crimstone_block'] ?? -1;
14	const CHEST = TILE_BY_KEY['chest']!;
15	
16	/** WillWaterPlacedHereStayPut 近似：下方实心且自身无液体 → 水放得住 */
17	function willWaterStayPut(st: TileStore, x: number, y: number): boolean {
18	  return !!st.inBounds(x, y + 1) && !!st.flags[st.idx(x, y + 1)] && st.liquid[st.idx(x, y)] === 0;
19	}
20	
21	/** SonOfLakinater（L48516）：向下蜿蜒湖腔。lava 恒 false（getGoodWorld 不支持） */
22	function sonOfLakinater(st: TileStore, rng: RNG, gs: GenState, i: number, j: number, strengthMultiplier = 1): void {
23	  let radius = rng.int(15, 30) * strengthMultiplier;   // num1（1/5 ×1.3）
24	  let steps = rng.int(30, 60);                         // num2
25	  if (rng.int(0, 4) === 0) { radius *= 1.3; steps *= 1.3; }
26	  let px = i + 0.0, py = j + 0.0;
27	  let wander = rng.next() * (1 / 500);                 // num3
28	  let vx: number;
29	  if (rng.int(0, 3) !== 0) {
30	    vx = rng.int(-15, 15) * 0.01;
31	  } else {
32	    vx = rng.int(-50, 50) * 0.01;
33	    wander = rng.next() * 0.004 + 0.001;
34	  }
35	  let vy = rng.int(0, 100) * 0.01;
36	  const stepsTotal = steps;                            // num4
37	  while (radius > 3 && steps > 0) {
38	    radius -= rng.int(0, 10) * 0.1;
39	    steps--;
40	    let x0 = Math.floor(px - radius * 4), x1 = Math.floor(px + radius * 4);
41	    let y0 = Math.floor(py - radius * 3), y1 = Math.floor(py + radius * 2);
42	    if (x0 < 0) x0 = 0;
43	    if (x1 > st.w) x1 = st.w;
44	    if (y0 < 0) y0 = 0;
45	    if (y1 > st.h) y1 = st.h;
46	    const r = radius;                                  // num9
47	    const entranceY = j + 5;                           // num17
48	    for (let x = x0; x < x1; x++) {
49	      for (let y = y0; y < y1; y++) {
50	        if (!st.inBounds(x, y)) continue;
51	        const ti = st.idx(x, y);
52	        const t = Math.min(1, Math.max(0, steps / stepsTotal)); // num2/num4（lerp 系数）
53	        const xc = (Math.abs(x - px) * 0.6) * (1 - t) + (Math.abs(x - px) * 0.3) * t;
54	        const yc = (Math.abs(y - py) * 1.4) * (1 - t) + (Math.abs(y - py) * 5) * t;
55	        const dist = Math.hypot(xc, yc);               // num16
56	        if (dist < r * 0.4) {
57	          // 湖腔主体：掏空 + 灌水
58	          if (y >= j) {
59	            const ti2 = st.idx(x, Math.min(st.h - 1, y));
60	            if (y <= j + 1 ? willWaterStayPut(st, x, y) : true) {
61	              st.liquid[ti2] = 255;
62	              st.liquidType[ti2] = 1;
63	            }
64	          }
65	          const wasGrass = st.flags[ti] && (st.type[ti] === MUD || st.type[ti] === JUNGLE_GRASS);
66	          st.setTileSilent(x, y, 0);
67	          // 原版此处 SpreadGrass 邻格（59/60 转草）——草传播未移植，跳过（后续 pass 铺草）
68	          void wasGrass;
69	        } else if (y > j + 1 && dist < r && st.liquid[ti] === 0) {
70	          // 腔壁泥土壳：窄处且有墙三面包围 → 填实
71	          if (Math.abs(x - px) * 0.8 < r && st.wall[ti] > 0
72	            && st.wall[st.idx(x - 1, y)] > 0 && st.wall[st.idx(x + 1, y)] > 0
73	            && st.wall[st.idx(x, y + 1)] > 0) {
74	            st.flags[ti] = 1;
75	          }
76	        } else if (y < j && steps === stepsTotal - 1 && y > gs.worldSurfaceLow - 20) {
77	          // 首步：向上漏斗入口（L48617-48638）
78	          const cloud = TILE_BY_KEY['v_189_cloud_block']!;
79	          if (!(st.flags[ti] && (st.type[ti] === cloud || st.type[ti] === TILE_BY_KEY['v_196_rain_cloud_block']))) {
80	            const fx = Math.abs(x - i) * 0.7;
81	            const fy = Math.abs(y - entranceY) * 1.35;
82	            const width = (1 - Math.abs(x - i) / Math.max(1, x1 - i)) * 2.3;
83	            const pow = width ** 4;
84	            if (y < entranceY && fx < r * 0.4 + Math.abs(y - entranceY) * 0.5 * pow) {
85	              st.setTileSilent(x, y, 0);
86	            }
87	          }
88	        }
89	      }
90	    }
91	    px += vx; py += vy;
92	    vx += rng.int(-100, 100) * wander;
93	    vy += rng.int(-100, 100) * 0.01;
94	    if (vx > 1) vx = 1;
95	    if (vx < -1) vx = -1;
96	    if (vy > 1) vy = 1;
97	    const floor = 0.5 * (1 - steps / stepsTotal);
98	    if (vy < floor) vy = floor;
99	  }
100	}
101	
102	/** pass 31 Lakes（L6450-6560）：num3 = Next(n*3, n*6) 次尝试（n=w/4200），上限 maxLakes-1 */
103	export function runLakesPass(st: TileStore, rng: RNG, gs: GenState): void {
104	  const { w } = st;
105	  const n = Math.floor(w / 4200);
106	  const tries = rng.int(n * 3, n * 6 - 1);             // Next(n*3, n*6)
107	  const beachAvoid = 275 + 5 + 40 + 20;                // lakesBeachAvoidance = beachSandRandomCenter(320)+20
108	  const maxLakes = 50;
109	  const lakeX: number[] = [];
110	  let budget = Math.floor(w / 4);                      // num4 尝试预算
111	  for (let k = 0; k < tries; k++) {
112	    if (lakeX.length >= maxLakes - 1) break;
113	    while (budget > 0) {
114	      let bad = false;
115	      budget--;
116	      let x = rng.int(beachAvoid, w - beachAvoid - 1); // Next(avoid, w-avoid)
117	      while (x > w * 0.45 && x < w * 0.55) {
118	        x = rng.int(beachAvoid, w - beachAvoid - 1);
119	      }
120	      for (const lx of lakeX) { if (Math.abs(x - lx) < 150) { bad = true; break; } }
121	      if (!bad) {
122	        for (let c = 0; c < gs.numMCaves; c++) {
123	          if (Math.abs(x - gs.mCaveX[c]) < 100) { bad = true; break; }
124	        }
125	      }
126	      if (bad) continue;
127	      // 自 worldSurfaceLow-20 向下找实心
128	      let y = gs.worldSurfaceLow - 20;
129	      for (;;) {
130	        if (st.flags[st.idx(x, y)]) break;
131	        y++;
132	        if (y >= gs.worldSurface || st.wall[st.idx(x, y)] > 0) { bad = true; break; }
133	      }
134	      if (!bad && st.type[st.idx(x, y)] === SAND) bad = true;
135	      if (bad) continue;
136	      // ±50 无猩红石/宝箱
137	      for (let dx = -50; dx <= 50 && !bad; dx++) {
138	        for (let dy = -50; dy <= 50; dy++) {
139	          if (!st.inBounds(x + dx, y + dy)) continue;
140	          const t = st.type[st.idx(x + dx, y + dy)];
141	          if (st.flags[st.idx(x + dx, y + dy)] && (t === CRIMSTONE || t === CHEST)) { bad = true; break; }
142	        }
143	      }
144	      if (bad) continue;
145	      // 两侧 ±20 皆实心为止下沉（上限 worldSurface-50）
146	      const anchor = y;
147	      const solidAt = (xx: number, yy: number) => st.inBounds(xx, yy) && st.flags[st.idx(xx, yy)];
148	      while (!solidAt(x - 20, y) || !solidAt(x + 20, y)) {
149	        y++;
150	        if (y > gs.worldSurface - 50) { bad = true; break; }
151	      }
152	      if (bad || y - anchor <= 10) continue;
153	      // ±60 顶部 20 格净空（无块无墙）
154	      for (let dx = -60; dx <= 60 && !bad; dx++) {
155	        const ty = y - 20;
156	        if (!st.inBounds(x + dx, ty)) continue;
157	        if (st.flags[st.idx(x + dx, ty)] || st.wall[st.idx(x + dx, ty)] > 0) bad = true;
158	      }
159	      if (bad) continue;
160	      // 121×121 实心率 ≥80%
161	      let solidN = 0;
162	      for (let dx = -60; dx <= 60; dx++) {
163	        for (let dy = 0; dy <= 120; dy++) {
164	          if (solidAt(x + dx, y + dy)) solidN++;
165	        }
166	      }
167	      if (solidN < 121 * 121 * 0.8) continue;
168	      // 非地下沙漠 ±8（无记录区间，墙 187/216/217 近似）
169	      let inDesert = false;
170	      for (let dx = -8; dx <= 8 && !inDesert; dx++) {
171	        for (let dy = -8; dy <= 8; dy++) {
172	          if (!st.inBounds(x + dx, y + dy)) continue;
173	          const wl = st.wall[st.idx(x + dx, y + dy)];
174	          if (wl === 187 || wl === 216 || wl === 217) { inDesert = true; break; }
175	        }
176	      }
177	      if (inDesert) continue;
178	      sonOfLakinater(st, rng, gs, x, y, 1);
179	      lakeX.push(x);
180	      break;
181	    }
182	  }
183	  gs.lakeX = lakeX;
184	}
185	

```


---

## 🤖 Assistant · 2026-08-11T04:09:14.939Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me check the other passes for sky writes. Need: BeachPass, IceBiomePass, GrassPass, JunglePass, DesertPass, MushroomPass, MarbleGranitePass, DirtToMudPass, CorruptionPass, MountCavesPass, ShiniesPass, GenState, plus IslandHousePass, SwordShrinePass, BuriedChestsPass, TrapsPass, HellFortPass, HiveSpiderPass (sky writes unlikely), TemplePass, DungeonPass, Spread.

Let me grep for y ranges. Read smaller ones in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:09:15.097Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:15.108Z

**📎 ToolResult**

```
1	// 原版 pass 3 "Ocean Sand"(L4962) + pass 33 "Beaches"(L6639) 移植。
2	// Ocean Sand:海滩区地表按深度随机走铺沙(50-200),顺手记录金字塔候选;
3	// Beaches:从海滩边缘挖出斜坡海盆( TuneOceanDepth 深度曲线),灌水,清墙,盆底铺沙。
4	// 原版固定 tile 常量按 4200 宽设计,此处按 w/4200 线性缩放保持比例(大世界 = 精确原版)。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T } from '../../../data/tiles';
9	
10	/** Ocean Sand:海滩铺沙 + 金字塔候选(L4962-5042) */
11	export function runOceanSandPass(st: TileStore, rng: RNG, gs: GenState): void {
12	  const w = st.w;
13	  const sandDepthLimit = Math.floor((gs.worldSurface + gs.rockLevel) / 2);
14	  for (let i = 0; i < 3; i++) {
15	    // 拒绝采样:中部 40%-60% 区间的起点重掷(原版 while 循环)
16	    let x0 = rng.int(0, w - 1);
17	    while (x0 > w * 0.40 && x0 < w * 0.60) x0 = rng.int(0, w - 1);
18	    let left = rng.int(35, 89);
19	    if (i === 1) left += Math.floor(rng.int(20, 39) * (w / 4200));
20	    if (rng.next() * 3 < 1) left *= 2;
21	    if (i === 1) left *= 2;
22	    let right = rng.int(35, 89);
23	    if (rng.next() * 3 < 1) right *= 2;
24	    if (i === 1) right *= 2;
25	    let x1 = x0 - left, x2 = x0 + right;
26	    if (x1 < 0) x1 = 0;
27	    if (x2 > w) x2 = w;
28	    if (i === 1) continue; // 中段跳过(原版 case 1: continue)
29	    if (i === 0) { x1 = 0; x2 = gs.beachLeftEnd; }
30	    if (i === 2) { x1 = gs.beachRightStart; x2 = w; }
31	    // 沙层厚度随机走(50-200)
32	    let depth = rng.int(50, 99);
33	    for (let x = x1; x < x2; x++) {
34	      if (rng.next() < 0.5) {
35	        depth += rng.int(-1, 1);
36	        if (depth < 50) depth = 50;
37	        if (depth > 200) depth = 200;
38	      }
39	      for (let y = 0; y < sandDepthLimit; y++) {
40	        const ii = st.idx(x, y);
41	        if (!st.flags[ii]) continue;
42	        // 金字塔候选:区域中心 1/6 概率
43	        if (x === ((x1 + x2) >> 1) && rng.next() < 1 / 6) {
44	          gs.pyramidSpots.push({ x, y });
45	        }
46	        const edge = Math.min(depth, x - x1, x2 - x);
47	        const thick = edge + rng.int(0, 4);
48	        for (let y2 = y; y2 < y + thick && y2 < st.h; y2++) {
49	          const jj = st.idx(x, y2);
50	          if (x > x1 + rng.int(0, 4) && x < x2 - rng.int(0, 4)) {
51	            st.type[jj] = T.SAND;
52	          }
53	        }
54	        break;
55	      }
56	    }
57	  }
58	}
59	
60	/** TuneOceanDepth(L11682):逐列深度增量曲线,阈值按世界宽度比例缩放 */
61	function tuneOceanDepth(rng: RNG, count: number, depth: number, van: number, floridaStyle: boolean): number {
62	  const inc = (f: number) => depth + rng.int(10, 19) * f;
63	  const t = (n: number) => Math.max(1, Math.floor(n * van));
64	  if (!floridaStyle) {
65	    if (count < t(3)) return inc(0.2);
66	    if (count < t(6)) return inc(0.15);
67	    if (count < t(9)) return inc(0.1);
68	    if (count < t(15)) return inc(0.07);
69	    if (count < t(50)) return inc(0.05);
70	    if (count < t(75)) return inc(0.04);
71	    if (count < t(100)) return inc(0.03);
72	    if (count < t(125)) return inc(0.02);
73	    if (count < t(150)) return inc(0.01);
74	    if (count < t(175)) return inc(0.005);
75	    if (count < t(200)) return inc(0.001);
76	    if (count < t(230)) return inc(0.01);
77	    if (count < t(235)) return inc(0.05);
78	    if (count < t(240)) return inc(0.1);
79	    if (count < t(245)) return inc(0.05);
80	    if (count < t(255)) return inc(0.01);
81	    return depth;
82	  }
83	  // florida 变体:同阈值曲线,近岸增量极小、远岸陡增(L11719-11748)
84	  if (count < t(3)) return inc(0.001);
85	  if (count < t(6)) return inc(0.002);
86	  if (count < t(9)) return inc(0.004);
87	  if (count < t(15)) return inc(0.007);
88	  if (count < t(50)) return inc(0.01);
89	  if (count < t(75)) return inc(0.014);
90	  if (count < t(100)) return inc(0.019);
91	  if (count < t(125)) return inc(0.027);
92	  if (count < t(150)) return inc(0.038);
93	  if (count < t(175)) return inc(0.052);
94	  if (count < t(200)) return inc(0.08);
95	  if (count < t(230)) return inc(0.12);
96	  if (count < t(235)) return inc(0.16);
97	  if (count < t(240)) return inc(0.27);
98	  if (count < t(245)) return inc(0.43);
99	  if (count < t(255)) return inc(0.6);
100	  return depth;
101	}
102	
103	/** Beaches:挖海盆灌水(L6639-6728) */
104	export function runBeachesPass(st: TileStore, rng: RNG, gs: GenState): void {
105	  const w = st.w;
106	  const van = w / 4200;
107	  const sc = (n: number) => Math.max(1, Math.floor(n * van)); // C# (int) 截断
108	  const oceanWaterMin = sc(220), oceanWaterMax = sc(260), forcedJungleLen = sc(275), minSand = sc(50);
109	  const edgeWall = Math.max(4, Math.floor(30 * van));
110	
111	  let floridaL = false, floridaR = false;
112	  if (rng.next() < 0.25) {
113	    if (rng.next() < 0.5) floridaL = true; else floridaR = true;
114	  }
115	
116	  for (let side = 0; side < 2; side++) {
117	    if (side === 0) {
118	      // 左海盆:从 beachLeftEnd-50 之左往世界缘挖
119	      let waterX = rng.int(oceanWaterMin, oceanWaterMax - 1);  // 原版 Next(220,260) 上界开
120	      if (gs.dungeonSide === 1) waterX = forcedJungleLen; // 丛林侧强制 275(缩放)
121	      const cap = gs.beachLeftEnd - minSand;
122	      if (waterX > cap) waterX = Math.max(2, cap);
123	      // 该列地表
124	      let surfY = 0;
125	      while (!st.flags[st.idx(waterX - 1, surfY)]) surfY++;
126	      const waterY = surfY + rng.int(1, 4);
127	      let count = 0, depth = 1;
128	      for (let x = waterX - 1; x >= 0; x--) {
129	        if (x > edgeWall) { count++; depth = tuneOceanDepth(rng, count, depth, van, floridaL); }
130	        else depth += 1;
131	        const pad = rng.int(15, 19);
132	        const yEnd = waterY + depth + pad;
133	        for (let y = 0; y < yEnd && y < st.h; y++) {
134	          const i = st.idx(x, y);
135	          if (y < waterY + depth * 0.75 - 3) {
136	            st.flags[i] = 0; st.type[i] = 0; st.frameX[i] = 0; st.frameY[i] = 0;
137	            if (y > waterY) { st.liquid[i] = 255; st.liquidType[i] = 1; }
138	            else if (y === waterY) { st.liquid[i] = 127; st.liquidType[i] = 1; }
139	          } else if (y > waterY) {
140	            st.type[i] = T.SAND; st.flags[i] = 1;
141	          }
142	          st.wall[i] = 0;
143	        }
144	      }
145	    } else {
146	      // 右海盆:镜像
147	      let waterX = w - rng.int(oceanWaterMin, oceanWaterMax - 1);  // 上界开,同原版 Next
148	      if (gs.dungeonSide === -1) waterX = w - forcedJungleLen;
149	      const cap = gs.beachRightStart + minSand;
150	      if (waterX < cap) waterX = Math.min(w - 2, cap);
151	      let surfY = 0;
152	      while (!st.flags[st.idx(waterX, surfY)]) surfY++;
153	      const waterY = surfY + rng.int(1, 4);
154	      let count = 0, depth = 1;
155	      for (let x = waterX; x < w; x++) {
156	        if (x < w - edgeWall) { count++; depth = tuneOceanDepth(rng, count, depth, van, floridaR); }
157	        else depth += 1;
158	        const pad = rng.int(15, 19);
159	        const yEnd = waterY + depth + pad;
160	        for (let y = 0; y < yEnd && y < st.h; y++) {
161	          const i = st.idx(x, y);
162	          if (y < waterY + depth * 0.75 - 3) {
163	            st.flags[i] = 0; st.type[i] = 0; st.frameX[i] = 0; st.frameY[i] = 0;
164	            if (y > waterY) { st.liquid[i] = 255; st.liquidType[i] = 1; }
165	            else if (y === waterY) { st.liquid[i] = 127; st.liquidType[i] = 1; }
166	          } else if (y > waterY) {
167	            st.type[i] = T.SAND; st.flags[i] = 1;
168	          }
169	          st.wall[i] = 0;
170	        }
171	      }
172	    }
173	  }
174	}
175	
176	// ---- 原版 ShellPiles pass（WorldGen.cs:16385-16450 + ShellPile L10307-10420）----
177	// 每侧 50% 概率，最多 6 堆；ShellPile：沙面上椭圆随机漂移填 tile 495（贝壳堆块），
178	// 下方悬空时补 495→沙 53→硬化沙 397（原版 10350-10403 逐层下探）
179	import { TILE_BY_KEY } from '../../../data/tiles';
180	
181	function shellPile(st: TileStore, rng: RNG, X: number, Y: number, worldSurface: number): boolean {
182	  if (X < 1 || Y < 1 || X >= st.w - 1 || Y >= st.h - 1) return false;
183	  let y = Y;
184	  while (y < st.h && !st.flags[st.idx(X, y)]) y++;
185	  if (y > worldSurface || y >= st.h) return false;          // 原版：仅地表内（海盆深度容差已放宽）
186	  if (st.type[st.idx(X, y)] !== T.SAND) return false;       // 必须沙面
187	  if (st.wall[st.idx(X, y)] !== 0) return false;            // 无背景墙
188	  y--;
189	  const SHELL = TILE_BY_KEY['v_495_shell_pile_block'] ?? 0;
190	  const HARD_SAND = TILE_BY_KEY['hardened_sand'] ?? 0;
191	  if (!SHELL) return false;
192	  let cx = X, cy = y;
193	  let vx = rng.next() * 0.6 - 0.3, vy = rng.next() * 0.5 + 0.5;
194	  let radius = rng.int(2, 4);
195	  if (rng.int(0, 9) === 0) radius += 1;
196	  let layers = rng.int(3, 6);
197	  const put = (x: number, yy: number, type: number) => {
198	    if (!st.inBounds(x, yy)) return;
199	    const i = st.idx(x, yy);
200	    st.type[i] = type; st.flags[i] = 1; st.frameX[i] = 0; st.frameY[i] = 0;
201	  };
202	  while (layers-- > 0) {
203	    const r = radius * (0.7 + rng.next() * 0.2);
204	    for (let x = Math.floor(X - radius * 4); x <= X + radius * 4; x++) {
205	      for (let yy = y + Math.floor(radius * 4); yy > y - radius * 4; yy--) {
206	        const dx = (cx - x) * 0.6, dyy = cy - yy;
207	        if (Math.hypot(dx, dyy) >= r) continue;
208	        if (yy <= y + 1 || rng.int(0, 5) === 0) {
209	          put(x, yy, SHELL);
210	          // 下方悬空补壳/沙/硬化沙（原版 10373-10399 三层下探）
211	          if (st.inBounds(x, yy + 1) && !st.flags[st.idx(x, yy + 1)]) {
212	            put(x, yy + 1, SHELL);
213	            if (st.inBounds(x, yy + 2) && !st.flags[st.idx(x, yy + 2)]) {
214	              put(x, yy + 2, T.SAND);
215	              if (st.inBounds(x, yy + 3) && !st.flags[st.idx(x, yy + 3)]) put(x, yy + 3, HARD_SAND);
216	            }
217	          }
218	        } else if (st.type[st.idx(x, yy)] !== SHELL) {
219	          put(x, yy, T.SAND);
220	        }
221	      }
222	    }
223	    cx += vx; cy += vy;
224	    vx = Math.max(-0.3, Math.min(0.3, vx + (rng.next() * 0.2 - 0.1)));
225	    vy = Math.max(0.5, Math.min(1.0, vy + (rng.next() * 0.2 - 0.1)));
226	  }
227	  return true;
228	}
229	
230	/** 海滩装饰：贝壳堆 + 海藻（GrowCheckSeaweed 简化 1:1：沙面+上方 4 格全满水才长） */
231	export function runBeachDecorPass(st: TileStore, rng: RNG, gs: GenState): void {
232	  const SEAWEED = TILE_BY_KEY['v_549_seaweed'] ?? 0;
233	  const sides: Array<[number, number, number]> = [
234	    [1, Math.max(1, gs.beachLeftEnd - 120), gs.beachLeftEnd],
235	    [-1, gs.beachRightStart, Math.min(st.w - 2, gs.beachRightStart + 120)],
236	  ];
237	  for (const [dir, x0, x1] of sides) {
238	    // 贝壳堆：50% 概率，锚点 = 海滩边界附近沙面（原版 shellStart 扫描近似）
239	    if (rng.next() < 0.5) {
240	      const baseX = dir === 1 ? gs.beachLeftEnd - rng.int(0, 5) : gs.beachRightStart + rng.int(0, 5);
241	      // 全列扫沙面（真实海盆深浅不一，固定窗口会漏锚）
242	      let by = -1;
243	      for (let y = 2; y < gs.worldSurface + 120 && y < st.h - 4; y++) {
244	        if (st.flags[st.idx(baseX, y)] && st.type[st.idx(baseX, y)] === T.SAND) { by = y; break; }
245	      }
246	      if (by > 0) {
247	        const offsets = [0, 10, 40, 70, 100, 25];
248	        for (const off of offsets) {
249	          if (off !== 0 && rng.next() >= 0.5) continue; // 原版 Next(maxValue 2..3) 门
250	          const x = dir === 1 ? baseX - off : baseX + off;
251	          shellPile(st, rng, x, Math.max(2, by - 50), gs.worldSurface + 120);
252	        }
253	      }
254	    }
255	    // 海藻：每个海洋列找沙面，上方 4 格全满水 → 2/3 放（原版 GrowCheckSeaweed 深水条件）
256	    if (SEAWEED) {
257	      for (let x = x0; x < x1; x++) {
258	        for (let y = 2; y < st.h - 4; y++) {
259	          const i = st.idx(x, y);
260	          if (!st.flags[i] || st.type[i] !== T.SAND) continue;
261	          const deep = [1, 2, 3, 4].every((d) => st.liquid[st.idx(x, y - d)] === 255 && !st.flags[st.idx(x, y - d)]);
262	          if (deep && rng.int(0, 2) !== 0) {
263	            const ai = st.idx(x, y - 1);
264	            st.type[ai] = SEAWEED; st.flags[ai] = 1; st.frameX[ai] = Math.floor(rng.next() * 3) * 18; st.frameY[ai] = 0;
265	          }
266	          break; // 每列只处理首个沙面
267	        }
268	      }
269	    }
270	  }
271	}
272	

```


---

## 🤖 Assistant · 2026-08-11T04:09:15.253Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenState.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:15.264Z

**📎 ToolResult**

```
1	// 原版生成管线共享状态（对应 WorldGen.GenerateWorld 闭包变量 L4694-4741 + Reset pass 掷的骰子）。
2	// 105 个 pass 按序读写,顺序不可调换。
3	export interface GenState {
4	  // 世界常量（Reset / Terrain pass 输出）
5	  worldSurface: number;   // 平均地表 y（tile）
6	  worldSurfaceLow: number;
7	  worldSurfaceHigh: number;
8	  rockLevel: number;
9	  rockLevelLow: number;
10	  rockLevelHigh: number;
11	  waterLine: number;      // 雪原上方（原版 waterLine ≈ 0.35×h）
12	  lavaLine: number;       // 地狱顶（原版 ≈ h-200）
13	  beachDistance: number;
14	
15	  // Reset pass 掷的世界级选择
16	  crimson: boolean;           // 50% 猩红 / 50% 腐化
17	  oreTiers: { copper: number; iron: number; silver: number; gold: number }; // 含替代 id
18	  dungeonSide: 1 | -1;        // 地牢在地图哪侧
19	  dungeonX: number;           // 地牢位置（Reset num4：仅作雪原中心）
20	  dungeonLocation: number;    // 地牢入口实际位置（Reset 末掷）
21	  dungeonY: number;           // 地牢入口地表 Y（DungeonPass 回填；刷怪门槛 dungeonY+40 用）
22	  dungeonEntX: number;        // 入口门厅可站立点 X（DungeonPass 回填；原版 dungeonX 语义=老头锚）
23	  dungeonEntY: number;        // 入口门厅可站立点 Y
24	  jungleX: number;            // 丛林（与地牢异侧）
25	  snowOriginLeft: number;
26	  snowOriginRight: number;
27	  beachLeftEnd: number;       // 左海滩右界（Reset L4880 掷，Ocean Sand/Beaches 消费）
28	  beachRightStart: number;    // 右海滩左界
29	
30	  // 各 pass 记录给后续 pass 用的区域
31	  // RandomizeTreeStyle（Reset 掷）：树冠样式边界与样式（finalize 写回 world）
32	  treeX: number[];
33	  treeStyle: number[];
34	  /** 生成的树登记（{x, y=树顶, h}；finalize 写 world.trees 供砍伐整棵判定） */
35	  genTrees: Array<{ x: number; y: number; h: number }>;
36	  /** Lakes pass 记录的湖位 x（后续 pass 避让用） */
37	  lakeX: number[];
38	  // Mount Caves（pass 7）记录的山丘坐标（pass 34/Webs 消费）
39	  mCaveX: Int32Array;
40	  mCaveY: Int32Array;
41	  numMCaves: number;
42	  snowMinX: Int32Array | null; // 每行雪原左边界（C# int[]；Ice Biome pass 写）
43	  snowMaxX: Int32Array | null;
44	  snowTop: number; snowBottom: number;
45	  jungleBounds: [number, number] | null; // [minX, maxX]
46	  evilZones: Array<{ x0: number; x1: number }>;
47	  undergroundDesert: { x0: number; y0: number; x1: number; y1: number } | null;
48	
49	  // 结构候选（由早期 pass 排队、后期 pass 消费）
50	  pyramidSpots: Array<{ x: number; y: number }>;
51	  floatingIslands: Array<{ x: number; y: number; style: number; isLake: boolean }>;
52	}
53	
54	export function newGenState(w: number, h: number): GenState {
55	  return {
56	    worldSurface: Math.floor(h * 0.3), worldSurfaceLow: 0, worldSurfaceHigh: 0,
57	    rockLevel: Math.floor(h * 0.42), rockLevelLow: 0, rockLevelHigh: 0,
58	    waterLine: Math.floor(h * 0.35), lavaLine: h - 200,
59	    beachDistance: Math.max(24, Math.floor(w * 0.06)),
60	    crimson: false,
61	    oreTiers: { copper: 0, iron: 0, silver: 0, gold: 0 },
62	    dungeonSide: 1, dungeonX: 0, dungeonLocation: 0, dungeonY: 0, dungeonEntX: 0, dungeonEntY: 0, jungleX: 0,
63	    snowOriginLeft: 0, snowOriginRight: 0,
64	    beachLeftEnd: 0, beachRightStart: 0,
65	    treeX: [0, 0, 0], treeStyle: [0, 0, 0, 0], genTrees: [], lakeX: [],
66	    mCaveX: new Int32Array(1024), mCaveY: new Int32Array(1024), numMCaves: 0,
67	    snowMinX: null, snowMaxX: null, snowTop: 0, snowBottom: 0,
68	    jungleBounds: null,
69	    evilZones: [],
70	    undergroundDesert: null,
71	    pyramidSpots: [],
72	    floatingIslands: [],
73	  };
74	}
75	

```


---

## 🤖 Assistant · 2026-08-11T04:09:20.371Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Beaches pass is important! Line 133-143: for the ocean basin, `for (let y = 0; y < yEnd ...)`: if `y < waterY + depth*0.75 - 3` → clear (flags=0, type=0) and water if y > waterY; else if y > waterY → SAND flags=1. So all sand writes are below waterY. No sky writes (waterY ≈ surfY+1..4, below surface). OK.

But note: the beach carve clears everything above the basin floor — including sky (already air). Fine.

Now let me check the rest: IceBiome, Grass, Jungle, Desert, Mushroom, MarbleGranite, DirtToMud, Corruption, MountCaves, Shinies, IslandHouse, SwordShrine, BuriedChests, Traps, HellFort, HiveSpider, Spread, Dungeon, Temple.

Key for sky writes: Jungle (mud runners), Desert (sand), IceBiome (ice), Corruption (ebonstone), MountCaves (hills above surface?), Shinies (ores with yMin?), SwordShrine (mound), Dungeon (above-ground entrance?).

Let me read JunglePass, MountCavesPass, IceBiomePass, DesertPass in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:09:20.493Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/JunglePass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:20.509Z

**📎 ToolResult**

```
1	// 原版 JunglePass 移植(GameContent/Biomes/JunglePass.cs,1:1)。
2	// 起点 (jungleOriginX, (h+rockLayer)/2):三轮随机移动 + 泥 runner(带宝石 63/65/67),
3	// 巨型泥 runner(num2=400-600×scale,steps 10000,向上 -20)+ 地表隧道,
4	// 泥墙挖洞(简化)+ 收尾(泥簇/石囊/宝石)。mudWall 期间铺丛林天然墙 64。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T, TILE_BY_KEY } from '../../../data/tiles';
9	import { tileRunner } from './TileRunner';
10	
11	const MUD = TILE_BY_KEY['mud']!;
12	const GEMS = ['gem_sapphire', 'gem_ruby', 'gem_emerald', 'gem_topaz', 'gem_amethyst', 'gem_diamond'].map((k) => TILE_BY_KEY[k]!);
13	
14	export function runJunglePass(st: TileStore, rng: RNG, gs: GenState): number {
15	  const { w, h } = st;
16	  const scale = (w / 4200) * 1.5;
17	  const van = w / 4200;
18	  let x = gs.jungleX;
19	  let y = Math.floor((h + gs.rockLevel) / 2);
20	  let zeroX = 0, zeroY = 0;
21	
22	  const applyRandomMovement = (xRange: number, yRange: number) => {
23	    x += rng.int(Math.floor(-xRange * scale), Math.floor(xRange * scale));
24	    y += rng.int(Math.floor(-yRange * scale), Math.floor(yRange * scale));
25	    y = Math.max(gs.rockLevel, Math.min(h - 1, y));
26	  };
27	  const placeFirstPassMud = (xSpeedScale: number) => {
28	    const str = rng.int(Math.floor(250 * scale), Math.floor(500 * scale));
29	    // 原版步数固定 50-150 不缩放(speedX=±3 → 漂移 ≤450;4200 宽的 10.7%)
30	    const stp = rng.int(50, 149);
31	    tileRunner(st, rng, gs, x, y, { strength: str, steps: stp, type: MUD, speedX: gs.dungeonSide * xSpeedScale, speedY: 0, mudWall: true });
32	  };
33	  const placeGemsAt = (baseGem: number, variants: number) => {
34	    for (let n = 0; n < 6 * scale; n++) {
35	      tileRunner(st, rng, gs,
36	        x + rng.int(-Math.floor(125 * scale), Math.floor(125 * scale)),
37	        y + rng.int(-Math.floor(125 * scale), Math.floor(125 * scale)), {
38	          strength: rng.int(3, 6), steps: rng.int(3, 7),
39	          type: GEMS[baseGem + rng.int(0, variants - 1)],
40	        });
41	    }
42	  };
43	
44	  applyRandomMovement(100, 100);
45	  zeroX += x; zeroY += y;
46	  placeFirstPassMud(3);
47	  placeGemsAt(0, 2); // 蓝宝石 63
48	  applyRandomMovement(250, 150);
49	  zeroX += x; zeroY += y;
50	  placeFirstPassMud(0);
51	  placeGemsAt(2, 2); // 祖母绿 65
52	  const oldX = x, oldY = y;
53	  applyRandomMovement(400, 150);
54	  zeroX += x; zeroY += y;
55	  placeFirstPassMud(-3);
56	  placeGemsAt(4, 2); // 黄玉 67
57	
58	  // 巨型泥 runner:三次移动点的均值为中心
59	  const cx = Math.floor(zeroX / 3), cy = Math.floor(zeroY / 3);
60	  const num2 = rng.int(Math.floor(400 * scale), Math.floor(600 * scale));
61	  const num3 = Math.floor(25 * scale);
62	  const i = Math.max(gs.beachLeftEnd + Math.floor(num2 / 2) + num3, Math.min(gs.beachRightStart - Math.floor(num2 / 2) - num3, cx));
63	  // JunglePass.cs:50-54：noYChange:true——vy=-20 保持原速直上；缺失时被钳到 ±1
64	  // （曾致泥柱矮、泥量大范围横向堆积，丛林地下形态与原版明显不同）
65	  tileRunner(st, rng, gs, i, cy, { strength: num2, steps: 10000, type: MUD, speedY: -20, noYChange: true, mudWall: true });
66	  // 泥柱中心记录给后续(丛林表面草化)
67	  (gs as any).jungleCoreX = i;
68	  const jungleXOut = generateTunnelToSurface(st, rng, gs, i, cy);
69	  generateHolesInMudWalls(st, rng, gs);
70	  generateFinishingTouches(st, rng, gs, oldX, oldY, scale, van);
71	  return jungleXOut;
72	}
73	
74	function generateTunnelToSurface(st: TileStore, rng: RNG, gs: GenState, i: number, j: number): number {
75	  let radius = rng.int(5, 10);
76	  let px = i + 0.0, py = j + 0.0;
77	  let vx = rng.int(-10, 10) * 0.1;
78	  let vy = rng.int(10, 19) * 0.1;
79	  let count = 0;
80	  let running = true;
81	  let jungleX = i;
82	  while (running) {
83	    if (py < gs.worldSurface) {
84	      const cx = Math.max(10, Math.min(st.w - 10, Math.floor(px)));
85	      const cy = Math.max(10, Math.min(st.h - 10, Math.floor(py)));
86	      // 隧道顶到达无墙无块的开放区即停(检查上方 1-5 格)
87	      let open = true;
88	      for (let d = 0; d <= 5; d++) {
89	        const ii = st.idx(cx, Math.max(5, cy - d));
90	        if (st.wall[ii] !== 0 || st.flags[ii]) { open = false; break; }
91	      }
92	      if (open) running = false;
93	    }
94	    jungleX = Math.floor(px);
95	    radius += rng.int(-20, 20) * 0.1;
96	    if (radius < 5) radius = 5;
97	    if (radius > 10) radius = 10;
98	    const x0 = Math.max(10, Math.min(st.w - 10, Math.floor(px - radius * 0.5)));
99	    const x1 = Math.max(10, Math.min(st.w - 10, Math.floor(px + radius * 0.5)));
100	    const y0 = Math.max(10, Math.min(st.h - 10, Math.floor(py - radius * 0.5)));
101	    const y1 = Math.max(10, Math.min(st.h - 10, Math.floor(py + radius * 0.5)));
102	    for (let x = x0; x < x1; x++) {
103	      for (let y = y0; y < y1; y++) {
104	        if (Math.abs(x - px) + Math.abs(y - py) < radius * 0.5 * (1 + rng.int(-10, 10) * 0.015)) {
105	          st.setTileSilent(x, y, 0);
106	        }
107	      }
108	    }
109	    count++;
110	    // 偶发分支洞穴
111	    if (count > 10 && rng.int(0, 49) < count) {
112	      count = 0;
113	      const side = rng.next() < 0.5 ? -2 : 2;
114	      tileRunner(st, rng, gs, Math.floor(px), Math.floor(py), {
115	        strength: rng.int(3, 19), steps: rng.int(10, 99), type: -1, speedX: side,
116	      });
117	    }
118	    px += vx; py += vy;
119	    vy += rng.int(-10, 10) * 0.01;
120	    if (vy > 0) vy = 0;
121	    if (vy < -2) vy = -2;
122	    vx += rng.int(-10, 10) * 0.1;
123	    if (px < i - 200) vx += rng.int(5, 20) * 0.1;
124	    if (px > i + 200) vx -= rng.int(5, 20) * 0.1;
125	    if (vx > 1.5) vx = 1.5;
126	    if (vx < -1.5) vx = -1.5;
127	    if (py < -50 || py > st.h + 50) running = false; // 安全阀
128	  }
129	  return jungleX;
130	}
131	
132	/** 泥墙挖洞(原版 MudWallRunner 的简化:在丛林墙上随机游走清出通道) */
133	function generateHolesInMudWalls(st: TileStore, rng: RNG, gs: GenState): void {
134	  const tries = Math.floor(st.w / 4);
135	  for (let n = 0; n < tries; n++) {
136	    let x = rng.int(20, st.w - 21);
137	    let y = rng.int(gs.worldSurface + 10, st.h - 150);
138	    let found = false;
139	    for (let attempt = 0; attempt < 40; attempt++) {
140	      const i = st.idx(x, y);
141	      if (st.wall[i] === 64 || st.wall[i] === 15) { found = true; break; }
142	      x = rng.int(20, st.w - 21);
143	      y = rng.int(gs.worldSurface + 10, st.h - 150);
144	    }
145	    if (!found) continue;
146	    // 简化随机走:清墙 30-80 步
147	    let steps = rng.int(30, 80);
148	    while (steps-- > 0) {
149	      if (!st.inBounds(x, y)) break;
150	      const i = st.idx(x, y);
151	      if (st.wall[i] === 64 || st.wall[i] === 15) st.wall[i] = 0;
152	      x += rng.int(-1, 1);
153	      y += rng.int(-1, 1);
154	    }
155	  }
156	}
157	
158	function generateFinishingTouches(st: TileStore, rng: RNG, gs: GenState, oldX: number, oldY: number, scale: number, van: number): void {
159	  let x = oldX, y = oldY;
160	  // 大泥簇
161	  for (let n = 0; n <= 20 * scale; n++) {
162	    x += rng.int(Math.floor(-5 * scale), Math.floor(5 * scale));
163	    y += rng.int(Math.floor(-5 * scale), Math.floor(5 * scale));
164	    // 原版 300-500 步固定不缩放
165	    const str = rng.int(40, 99), stp = rng.int(300, 499);
166	    tileRunner(st, rng, gs, x, y, { strength: str, steps: stp, type: MUD });
167	  }
168	  // 洞穴(1/7 填液体)
169	  for (let n = 0; n <= 10 * scale; n++) {
170	    let i2 = oldX + rng.int(-Math.floor(600 * scale), Math.floor(600 * scale));
171	    let j2 = oldY + rng.int(-Math.floor(200 * scale), Math.floor(200 * scale));
172	    let found = false;
173	    for (let attempt = 0; attempt < 40; attempt++) {
174	      if (i2 >= 1 && i2 < st.w - 1 && j2 >= 1 && j2 < st.h - 1 && st.type[st.idx(i2, j2)] === MUD) { found = true; break; }
175	      i2 = oldX + rng.int(-Math.floor(600 * scale), Math.floor(600 * scale));
176	      j2 = oldY + rng.int(-Math.floor(200 * scale), Math.floor(200 * scale));
177	    }
178	    if (!found) continue;
179	    for (let k = 0; k < 8 * scale; k++) {
180	      i2 += rng.int(-30, 30);
181	      j2 += rng.int(-30, 30);
182	      tileRunner(st, rng, gs, i2, j2, {
183	        strength: rng.int(10, 19), steps: rng.int(30, 69),
184	        type: rng.next() * 7 < 1 ? -2 : -1,
185	      });
186	    }
187	  }
188	  // 泥内石囊 + 宝石
189	  for (let n = 0; n <= 300 * scale; n++) {
190	    let i2 = oldX + rng.int(-Math.floor(600 * scale), Math.floor(600 * scale));
191	    let j2 = oldY + rng.int(-Math.floor(200 * scale), Math.floor(200 * scale));
192	    let found = false;
193	    for (let attempt = 0; attempt < 40; attempt++) {
194	      if (i2 >= 1 && i2 < st.w - 1 && j2 >= 1 && j2 < st.h - 1 && st.type[st.idx(i2, j2)] === MUD) { found = true; break; }
195	      i2 = oldX + rng.int(-Math.floor(600 * scale), Math.floor(600 * scale));
196	      j2 = oldY + rng.int(-Math.floor(200 * scale), Math.floor(200 * scale));
197	    }
198	    if (!found) continue;
199	    tileRunner(st, rng, gs, i2, j2, { strength: rng.int(4, 9), steps: rng.int(5, 29), type: T.STONE });
200	    if (rng.next() * 4 < 1) {
201	      tileRunner(st, rng, gs,
202	        i2 + rng.int(-1, 1), j2 + rng.int(-1, 1),
203	        { strength: rng.int(3, 6), steps: rng.int(4, 7), type: GEMS[rng.int(0, 5)] });
204	    }
205	  }
206	}
207	

```


---

## 🤖 Assistant · 2026-08-11T04:09:20.689Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:20.701Z

**📎 ToolResult**

```
1	// 原版山丘双 pass 1:1（1405 WorldGen.cs）：
2	//  - pass 7 "Mount Caves"（L5091-5150，1456 MountainCaves:11811 常数一致）：地表随机位置
3	//    用 Mountinater（L48367）造上漂泥土山丘，记录 mCave 坐标
4	//  - pass 34 "Mountain Caves"（L6628-6639）：每座山丘侧面开洞（CaveOpenater L48789）
5	//    + 向下蜿蜒洞穴（Cavinator L48733，递归至岩层）
6	// RNG 映射：Next(a,b) 左闭右开 → rng.int(a, b-1)；(int) → ctrunc。
7	import { TileStore } from '../../TileStore';
8	import type { RNG } from '../../../core/rng';
9	import type { GenState } from './GenState';
10	import { ctrunc } from '../../../core/csCompat';
11	import { idsByVanillaSheet, NOT_CLEARABLE } from './TileRunner';
12	import { T, TILE_BY_KEY } from '../../../data/tiles';
13	
14	/** 山丘区域避让的沙族（原版 box 检查 type 53/151/274：沙/沙岩砖/沙岩板） */
15	const SAND_AVOID = idsByVanillaSheet(53, 151, 274);
16	
17	/** Mountinater（L48367）：上漂泥土 blob = 山丘本体。只在空气格激活填土(type 0=Dirt) */
18	function mountinater(st: TileStore, rng: RNG, i: number, j: number): void {
19	  let num1 = rng.int(79, 119);            // Next(80,120)
20	  let num2 = rng.int(39, 54);             // Next(40,55)
21	  let px = i, py = j + num2 / 2;
22	  let vx = rng.int(-10, 10) * 0.1;        // Next(-10,11)
23	  let vy = rng.int(-20, -11) * 0.1;       // Next(-20,-10)
24	  while (num1 > 0 && num2 > 0) {
25	    num1 -= rng.int(0, 3);                // Next(4)
26	    num2--;
27	    let x0 = ctrunc(px - num1 * 0.5), x1 = ctrunc(px + num1 * 0.5);
28	    let y0 = ctrunc(py - num1 * 0.5), y1 = ctrunc(py + num1 * 0.5);
29	    if (x0 < 0) x0 = 0;
30	    if (x1 > st.w) x1 = st.w;
31	    if (y0 < 0) y0 = 0;
32	    if (y1 > st.h) y1 = st.h;
33	    const r = num1 * rng.int(79, 119) * 0.01; // Next(80,120)
34	    for (let x = x0; x < x1; x++) {
35	      for (let y = y0; y < y1; y++) {
36	        const dx = Math.abs(x - px), dy = Math.abs(y - py);
37	        if (Math.sqrt(dx * dx + dy * dy) < r * 0.4) {
38	          const k = st.idx(x, y);
39	          if (!st.flags[k]) st.setTileSilent(x, y, T.DIRT); // 原版 active(true)+type 0(=Dirt)
40	        }
41	      }
42	    }
43	    px += vx; py += vy;
44	    vx += rng.int(-10, 10) * 0.05;
45	    vy += rng.int(-10, 10) * 0.05;
46	    if (vx > 0.5) vx = 0.5;
47	    if (vx < -0.5) vx = -0.5;
48	    if (vy > -0.5) vy = -0.5;
49	    if (vy < -1.5) vy = -1.5;
50	  }
51	}
52	
53	/** pass 7 Mount Caves：w*0.001 次尝试，避开中心 ±90/沙族 ±50×25/前丘 ±100（L5095-5148） */
54	export function runMountCavesPass(st: TileStore, rng: RNG, gs: GenState): void {
55	  const count = Math.floor(st.w * 0.001);
56	  for (let n = 0; n < count; n++) {
57	    let x = rng.int(Math.floor(st.w * 0.25), Math.floor(st.w * 0.75) - 1); // Next(w*.25, w*.75)
58	    let tries = 0;
59	    let giveUp = false;
60	    let placed = false;
61	    while (!placed && !giveUp) {
62	      placed = true;
63	      while (x > st.w / 2 - 90 && x < st.w / 2 + 90) {
64	        x = rng.int(Math.floor(st.w * 0.25), Math.floor(st.w * 0.75) - 1);
65	      }
66	      for (let k = 0; k < gs.numMCaves; k++) {
67	        if (Math.abs(x - gs.mCaveX[k]) < 100) { tries++; placed = false; break; }
68	      }
69	      if (tries >= st.w / 5) { giveUp = true; break; }
70	    }
71	    if (giveUp) continue;
72	    // 找该列地表首个实心格
73	    for (let y = 0; y < gs.worldSurface; y++) {
74	      if (!st.flags[st.idx(x, y)]) continue;
75	      let nearSand = false;
76	      for (let dx = -50; dx < 50 && !nearSand; dx++) {
77	        for (let dy = -25; dy < 25; dy++) {
78	          const xx = x + dx, yy = y + dy;
79	          if (!st.inBounds(xx, yy) || !st.flags[st.idx(xx, yy)]) continue;
80	          if (SAND_AVOID.has(st.type[st.idx(xx, yy)])) { nearSand = true; break; }
81	        }
82	      }
83	      if (!nearSand) {
84	        mountinater(st, rng, x, y);
85	        gs.mCaveX[gs.numMCaves] = x;
86	        gs.mCaveY[gs.numMCaves] = y;
87	        gs.numMCaves++;
88	      }
89	      break; // 原版无论放没放都 break 出列扫描
90	    }
91	  }
92	}
93	
94	/** CaveOpenater（L48789）：山侧横向开口，100 步或直到离开墙/碰不可清 tile */
95	function caveOpenater(st: TileStore, rng: RNG, i: number, j: number): void {
96	  let num1 = rng.int(6, 11);              // Next(7,12)
97	  let dir = rng.int(0, 1) === 0 ? -1 : 1; // Next(2)
98	  if (rng.int(0, 9) !== 0) dir = i >= st.w / 2 ? -1 : 1; // 90% 朝世界外侧（Next(10)!=0）
99	  let px = i, py = j;
100	  let steps = 100;
101	  let vx = dir, vy = 0;
102	  while (steps > 0) {
103	    const k = st.idx(Math.max(0, Math.min(st.w - 1, ctrunc(px))), Math.max(0, Math.min(st.h - 1, ctrunc(py))));
104	    const t = st.type[k];
105	    if (st.wall[k] === 0 || (st.flags[k] && NOT_CLEARABLE.has(t))) steps = 0;
106	    steps--;
107	    let x0 = ctrunc(px - num1 * 0.5), x1 = ctrunc(px + num1 * 0.5);
108	    let y0 = ctrunc(py - num1 * 0.5), y1 = ctrunc(py + num1 * 0.5);
109	    if (x0 < 0) x0 = 0;
110	    if (x1 > st.w) x1 = st.w;
111	    if (y0 < 0) y0 = 0;
112	    if (y1 > st.h) y1 = st.h;
113	    const r = num1 * rng.int(79, 119) * 0.01;
114	    for (let x = x0; x < x1; x++) {
115	      for (let y = y0; y < y1; y++) {
116	        const dx = Math.abs(x - px), dy = Math.abs(y - py);
117	        if (Math.sqrt(dx * dx + dy * dy) < r * 0.4) {
118	          const kk = st.idx(x, y);
119	          if (st.flags[kk] && !NOT_CLEARABLE.has(st.type[kk])) st.setTileSilent(x, y, 0);
120	        }
121	      }
122	    }
123	    px += vx; py += vy;
124	    vx += rng.int(-10, 10) * 0.05;
125	    vy += rng.int(-10, 10) * 0.05;
126	    if (vx > dir + 0.5) vx = dir + 0.5;
127	    if (vx < dir - 0.5) vx = dir - 0.5;
128	    if (vy > 0) vy = 0;
129	    if (vy < -0.5) vy = -0.5;
130	  }
131	}
132	
133	/** Cavinator（L48733）：向下蜿蜒洞穴，递归 steps 次直至岩层（不挖沙 53） */
134	function cavinator(st: TileStore, rng: RNG, gs: GenState, i: number, j: number, steps: number): void {
135	  let num1 = rng.int(6, 14);              // Next(7,15)
136	  const dir = rng.int(0, 1) === 0 ? -1 : 1;
137	  let px = i, py = j;
138	  let count = rng.int(19, 39);            // Next(20,40)
139	  let vx = dir, vy = rng.int(10, 19) * 0.01; // Next(10,20)
140	  const SAND = TILE_BY_KEY['sand']!;
141	  while (count > 0) {
142	    count--;
143	    let x0 = ctrunc(px - num1 * 0.5), x1 = ctrunc(px + num1 * 0.5);
144	    let y0 = ctrunc(py - num1 * 0.5), y1 = ctrunc(py + num1 * 0.5);
145	    if (x0 < 0) x0 = 0;
146	    if (x1 > st.w) x1 = st.w;
147	    if (y0 < 0) y0 = 0;
148	    if (y1 > st.h) y1 = st.h;
149	    const r = num1 * rng.int(79, 119) * 0.01;
150	    for (let x = x0; x < x1; x++) {
151	      for (let y = y0; y < y1; y++) {
152	        const dx = Math.abs(x - px), dy = Math.abs(y - py);
153	        if (Math.sqrt(dx * dx + dy * dy) < r * 0.4) {
154	          const kk = st.idx(x, y);
155	          if (st.flags[kk] && !NOT_CLEARABLE.has(st.type[kk]) && st.type[kk] !== SAND) {
156	            st.setTileSilent(x, y, 0);
157	          }
158	        }
159	      }
160	    }
161	    px += vx; py += vy;
162	    vx += rng.int(-10, 10) * 0.05;
163	    vy += rng.int(-10, 10) * 0.05;
164	    if (vx > dir + 0.5) vx = dir + 0.5;
165	    if (vx < dir - 0.5) vx = dir - 0.5;
166	    if (vy > 2) vy = 2;
167	    if (vy < 0) vy = 0;
168	  }
169	  if (steps <= 0 || ctrunc(py) >= gs.rockLevel + 50) return;
170	  cavinator(st, rng, gs, ctrunc(px), ctrunc(py), steps - 1);
171	}
172	
173	/** pass 34 Mountain Caves（L6628-6639）：每座山丘 开口+蜿蜒 */
174	export function runMountainCavesPass(st: TileStore, rng: RNG, gs: GenState): void {
175	  for (let n = 0; n < gs.numMCaves; n++) {
176	    const x = gs.mCaveX[n], y = gs.mCaveY[n];
177	    caveOpenater(st, rng, x, y);
178	    cavinator(st, rng, gs, x, y, rng.int(39, 49)); // Next(40,50)
179	  }
180	}
181	

```


---

## 🤖 Assistant · 2026-08-11T04:09:32.246Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
MAJOR finding: `mountinater` (MountCavesPass.ts:18-51) — "上漂泥土山丘" writes REAL DIRT blocks (setTileSilent = flags=1) into the SKY above the surface (y from surface upward ~54 tiles). This is a legitimate sky writer (hills). It's intended in vanilla too.

JunglePass: placeFirstPassMud uses tileRunner with type MUD — no addTile → ghost types only (unless converting existing). But wait: for the giant mud runner (line 65), strength 400-600×scale with steps 10000, speedY=-20 — that's a huge runner. With overRide=true (default), it writes `st.type[ti] = MUD` in air cells too — ghost types. Huge volume of ghost mud types! Also mudWall writes walls.

Hmm wait, does tileRunner write type into air cells? Line 121: `if (overRide || !st.flags[ti])` — overRide defaults true → enters. Then flag3 checks. `if (!flag3) st.type[ti] = type;` — for an air cell (type=0, flags=0): cur=0 (T.DIRT? no—0 = air). Checks: STONE_PLACED.has(type) for MUD? no. NOT_CLEARABLE.has(0)? idsByVanillaSheet filters by defs with vanilla sheet; tile id 0 air probably has no vanilla sheet → NOT_CLEARABLE doesn't contain 0. cur===T.STONE? no. FLAG3_ALWAYS.has(0)? no. cur===SAND? no. So flag3=false → `st.type[ti] = MUD` written into air cell WITHOUT flags (addTile false) → ghost. Confirmed.

So EVERY placing tileRunner call writes ghost types into whatever air it touches, including sky. That's the "杂块" (garbage blocks) — invisible until... they ARE invisible because flags=0. But hold on: are they really invisible? Rendering probably uses flags. And the finalize erases them all.

Wait — but the user says "生成早期往天空写入大量杂块、后期又被抹除". Perhaps they observed via the partial preview (onWorldPartial) that sky had blocks visible at intermediate passes, then gone at the end. That's consistent: ghost types written early (visible in preview if the renderer draws type without flags check, or if flags get set), erased at finalize.

Actually wait — there might be another path: does anything later set flags on ghost cells? `addTile` passes: e.g. ShiniesPass? Let me check ShiniesPass for addTile usage. Also `halfBrick` Smooth World corner-fill branch: `st.setTileSilent(i, j, belowType)` — writes flags=1 above a solid tile in sky region → real sky blocks (floating half bricks). The comment in HalfBrickPass.ts:19-21 mentions the earlier bug: "曾致补角分支实体化天空幽灵块成浮空半砖（2583 个）" — fixed by making solidTile require flags.

Hmm, but the corner-fill writes at (i,j) where `st.type[ti] === 0` — checks `st.type[ti] === 0`, so it won't fire on ghost cells (ghost cells have type != 0). OK good.

Now let me check remaining passes quickly with grep for y bounds and setTileSilent/type writes. Let me look at ShiniesPass, IceBiomePass, DesertPass, CorruptionPass, MushroomPass, MarbleGranitePass, DirtToMudPass, GrassPass, Spread, IslandHousePass, SwordShrinePass, BuriedChestsPass, TrapsPass, HellFortPass, HiveSpiderPass, TemplePass, DungeonPass.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:09:32.790Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/ShiniesPass.ts"
}
```


---

## 🤖 Assistant · 2026-08-11T04:09:32.794Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IceBiomePass.ts"
}
```


---

## 🤖 Assistant · 2026-08-11T04:09:32.796Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:32.798Z

**📎 ToolResult**

```
1	// 原版矿石 pass 27 "Shinies"（1405 WorldGen.cs:5837-5922；1456 OresAndShinies:13233 常数一致）
2	// + 宝石 pass 36 "Gems"（1405 L6754-6830，含尾部浮沙拱形化循环）。
3	// 密度=面积×常数、深度三带（surfLow..surfHigh / surfHigh..rockHigh / rockLow..底）、
4	// 脉体=TileRunner（菱形椭圆），邪恶矿 22/204 只在岩层以下。
5	// RNG 映射：C# Next(a,b) 左闭右开 → rng.int(a, b-1)。
6	import { TileStore } from '../../TileStore';
7	import type { RNG } from '../../../core/rng';
8	import type { GenState } from './GenState';
9	import { tileRunner } from './TileRunner';
10	import { T, TILE_BY_KEY } from '../../../data/tiles';
11	
12	/** 单深度带放矿：count 次尝试，y∈[yMin,yMax)，strength/steps 各自区间 */
13	function band(
14	  st: TileStore, rng: RNG, gs: GenState,
15	  count: number, yMin: number, yMax: number,
16	  type: number, s: [number, number], steps: [number, number],
17	) {
18	  for (let i = 0; i < count; i++) {
19	    const x = rng.int(0, st.w - 1);              // Next(0, maxTilesX)
20	    const y = rng.int(Math.max(0, yMin), yMax - 1); // Next(yMin, yMax)
21	    tileRunner(st, rng, gs, x, y, {
22	      strength: rng.int(s[0], s[1]), steps: rng.int(steps[0], steps[1]),
23	      type, addTile: false,
24	    });
25	  }
26	}
27	
28	export function runShiniesPass(st: TileStore, rng: RNG, gs: GenState): void {
29	  const area = st.w * st.h;
30	  const surfLow = gs.worldSurfaceLow, surfHigh = gs.worldSurfaceHigh;
31	  const rockHigh = gs.rockLevelHigh, rockLow = gs.rockLevelLow;
32	
33	  // 铜/锡：三带 6e-5 / 8e-5 / 2e-4（cs:5840-5862）
34	  band(st, rng, gs, Math.floor(area * 6e-5), surfLow, surfHigh, gs.oreTiers.copper, [3, 5], [2, 5]);
35	  band(st, rng, gs, Math.floor(area * 8e-5), surfHigh, rockHigh, gs.oreTiers.copper, [3, 6], [3, 6]);
36	  band(st, rng, gs, Math.floor(area * 2e-4), rockLow, st.h, gs.oreTiers.copper, [4, 8], [4, 7]);
37	  // 铁/铅：三带 3e-5 / 8e-5 / 2e-4（cs:5863-5892）
38	  band(st, rng, gs, Math.floor(area * 3e-5), surfLow, surfHigh, gs.oreTiers.iron, [3, 6], [2, 4]);
39	  band(st, rng, gs, Math.floor(area * 8e-5), surfHigh, rockHigh, gs.oreTiers.iron, [3, 5], [3, 5]);
40	  band(st, rng, gs, Math.floor(area * 2e-4), rockLow, st.h, gs.oreTiers.iron, [4, 8], [4, 7]);
41	  // 银/钨：中层 2.6e-5 / 深层 1.5e-4 / 天空带 1.7e-4（cs:5893-5915）
42	  band(st, rng, gs, Math.floor(area * 2.6e-5), surfHigh, rockHigh, gs.oreTiers.silver, [3, 5], [3, 5]);
43	  band(st, rng, gs, Math.floor(area * 1.5e-4), rockLow, st.h, gs.oreTiers.silver, [4, 8], [4, 7]);
44	  band(st, rng, gs, Math.floor(area * 1.7e-4), 0, surfLow, gs.oreTiers.silver, [4, 8], [4, 7]);
45	  // 金/铂：深层 1.2e-4 / 近地表带 1.2e-4（cs:5916-5931）
46	  band(st, rng, gs, Math.floor(area * 1.2e-4), rockLow, st.h, gs.oreTiers.gold, [4, 7], [4, 7]);
47	  band(st, rng, gs, Math.floor(area * 1.2e-4), 0, Math.max(1, surfLow - 20), gs.oreTiers.gold, [4, 7], [4, 7]);
48	  // 邪恶矿：2.25e-5，仅岩层以下（cs:5932-5949）
49	  const evil = gs.crimson ? TILE_BY_KEY['ore_crimtane']! : TILE_BY_KEY['ore_demonite']!;
50	  band(st, rng, gs, Math.floor(area * 2.25e-5), gs.rockLevel, st.h, evil, [3, 5], [4, 7]);
51	}
52	
53	/** 宝石 pass 36（cs:6754-6814）：六宝石独立数量（w×[0.3,0.1,0.25,0.45,0.5,0.05]×0.2），
54	 *  拒绝采样到石头上再 TileRunner；type 63-68 = 紫晶/黄玉/蓝宝/绿宝/红宝/钻石。
55	 *  （原版开头 Main.tileSolid[484]=false 是滚动仙人掌临时非固体——我们不生成 484，跳过） */
56	export function runGemsPass(st: TileStore, rng: RNG, gs: GenState): void {
57	  const gems: Array<[string, number]> = [
58	    ['gem_sapphire', 0.3],   // 63
59	    ['gem_ruby', 0.1],       // 64
60	    ['gem_emerald', 0.25],   // 65
61	    ['gem_topaz', 0.45],     // 66
62	    ['gem_amethyst', 0.5],   // 67
63	    ['gem_diamond', 0.05],   // 68
64	  ];
65	  for (const [key, density] of gems) {
66	    const type = TILE_BY_KEY[key]!;
67	    const count = Math.floor(st.w * density * 0.2);
68	    for (let i = 0; i < count; i++) {
69	      // 拒绝采样：直到命中石头（原版死循环到命中为止；限 64 次防极端卡死）
70	      let x = rng.int(0, st.w - 1);
71	      let y = rng.int(gs.worldSurface, st.h - 1);
72	      for (let tries = 0; tries < 64 && st.type[st.idx(x, y)] !== T.STONE; tries++) {
73	        x = rng.int(0, st.w - 1);
74	        y = rng.int(gs.worldSurface, st.h - 1);
75	      }
76	      if (st.type[st.idx(x, y)] !== T.STONE) continue;
77	      tileRunner(st, rng, gs, x, y, {
78	        strength: rng.int(2, 5), steps: rng.int(3, 6), // Next(2,6)/Next(3,7)
79	        type, addTile: false,
80	      });
81	    }
82	  }
83	  sandArch(st);
84	}
85	
86	/** 浮沙拱形化（cs:6815-6830，Gems pass 尾段）：悬空沙柱顶格平移到侧下方贴地——
87	 *  消除生成期浮沙，避免进游戏后大范围流沙塌落 */
88	function sandArch(st: TileStore) {
89	  const SANDS = new Set<number>(
90	    ['sand', 'v_112_ebonsand_block', 'v_234_crimsand_block']
91	      .map((k) => TILE_BY_KEY[k])
92	      .filter((v): v is number => v != null),
93	  );
94	  for (let dir = 0; dir < 2; dir++) {
95	    const step = dir === 0 ? 1 : -1;
96	    const x0 = dir === 0 ? 5 : st.w - 6;
97	    const x1 = dir === 0 ? st.w - 5 : 4;
98	    for (let x = x0; x !== x1; x += step) {
99	      for (let y = 10; y < st.h - 10; y++) {
100	        const i = st.idx(x, y);
101	        // 原版按 UndergroundDesertLocation x 区间跳过地下沙漠列（未记录 x；用蜂窝墙 187/216/217 近似）
102	        if (st.wall[i] === 187 || st.wall[i] === 216 || st.wall[i] === 217) continue;
103	        if (!st.flags[i] || !st.flags[st.idx(x, y + 1)]) continue;
104	        if (!SANDS.has(st.type[i]) || !SANDS.has(st.type[st.idx(x, y + 1)])) continue;
105	        const nx = x + step;
106	        if (st.flags[st.idx(nx, y)] || st.flags[st.idx(nx, y + 1)]) continue;
107	        let ny = y + 1;
108	        while (ny < st.h - 1 && !st.flags[st.idx(nx, ny + 1)]) ny++;
109	        const sandType = st.type[i]; // 先取后清
110	        st.setTileSilent(x, y, 0);
111	        st.setTileSilent(nx, ny, sandType);
112	      }
113	    }
114	  }
115	}
116	

```


---

## 👤 User(sidechain) · 2026-08-11T04:09:32.799Z

**📎 ToolResult**

```
1	// 原版 pass 15 "Generate Ice Biome"(WorldGen.cs:5372)移植。
2	// 以 Reset 掷的 snowOriginLeft/Right(=地牢 X ± 扩展)为起点,逐行随机走左右边界;
3	// num2 行以上整体转换(土/草/腐草/粘土/沙→雪 147,石→冰 161,土墙→雪墙 40),
4	// num2 行以下按随机走厚度 num5(0-50)向下转换。记录 snowMinX/snowMaxX/snowBottom。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T, TILE_BY_KEY, TILE_DEFS } from '../../../data/tiles';
9	
10	export function runIceBiomePass(st: TileStore, rng: RNG, gs: GenState): void {
11	  const { w, h } = st;
12	  gs.snowTop = gs.worldSurface;
13	  const num2 = gs.lavaLine - rng.int(160, 199); // 完整转换深度线
14	  let left = gs.snowOriginLeft, right = gs.snowOriginRight;
15	  let thickness = 10;
16	  // C# 是 int[]：边界与厚度全程整数、`/2` 为整除截断（cs L5408-5411）。
17	  // 曾用 Float32Array 浮点累积 → 边界逐行漂移、雪原范围与原版不符
18	  gs.snowMinX = new Int32Array(h);
19	  gs.snowMaxX = new Int32Array(h);
20	
21	  const CORRUPT_GRASS = TILE_BY_KEY['v_23_corrupt_grass_block']!;
22	  const CLAY = TILE_BY_KEY['clay']!;
23	  const ICE = TILE_BY_KEY['ice']!;
24	
25	  for (let y = 0; y <= gs.lavaLine - 140; y++) {
26	    left += rng.int(-4, 3);
27	    right += rng.int(-3, 4);
28	    if (y > 0) {
29	      // C# int[] 整除截断（非负 → Math.floor 等价）
30	      left = Math.floor((left + gs.snowMinX[y - 1]) / 2);
31	      right = Math.floor((right + gs.snowMaxX[y - 1]) / 2);
32	    }
33	    // 雪原整体向地牢侧缓慢漂移
34	    if (gs.dungeonSide > 0) {
35	      if (rng.next() * 4 < 1) { left++; right++; }
36	    } else if (rng.next() * 4 < 1) { left--; right--; }
37	    gs.snowMinX[y] = left;
38	    gs.snowMaxX[y] = right;
39	    const x0 = Math.max(0, Math.ceil(left)), x1 = Math.min(w, Math.ceil(right));
40	    for (let x = x0; x < x1; x++) {
41	      if (y < num2) {
42	        const i = st.idx(x, y);
43	        // 原版只写 type 不激活——未激活格保持空气,跳过
44	        if (!st.flags[i]) continue;
45	        if (st.wall[i] === 2) st.wall[i] = 40;
46	        const t = st.type[i];
47	        if (t === T.DIRT || t === T.GRASS || t === CORRUPT_GRASS || t === CLAY || t === T.SAND) st.type[i] = T.SNOW;
48	        else if (t === T.STONE) st.type[i] = ICE;
49	      } else {
50	        thickness += rng.int(-3, 3);
51	        if (rng.next() * 3 < 1) {
52	          thickness += rng.int(-4, 4);
53	          if (rng.next() * 3 < 1) thickness += rng.int(-6, 6);
54	        }
55	        if (thickness < 0) thickness = rng.int(0, 2);
56	        else if (thickness > 50) thickness = 50 - rng.int(0, 2);
57	        for (let y2 = y; y2 < y + thickness && y2 < h; y2++) {
58	          const i = st.idx(x, y2);
59	          if (!st.flags[i]) continue;
60	          if (st.wall[i] === 2) st.wall[i] = 40;
61	          const t = st.type[i];
62	          if (t === T.DIRT || t === T.GRASS || t === CORRUPT_GRASS || t === CLAY || t === T.SAND) st.type[i] = T.SNOW;
63	          else if (t === T.STONE) st.type[i] = ICE;
64	        }
65	      }
66	    }
67	    if (gs.snowBottom < y) gs.snowBottom = y;
68	  }
69	}
70	
71	/** 原版 pass 33 "Slush"（cs:6591-6624）：雪原带内 石→冰、泥/沙泥→雪泥(224)。
72	 *  泥转雪泥前查 ±3 无丛林草/蘑菇草族（60/70/71/72）。无 RNG 消耗（与原版一致）。 */
73	export function runSlushPass(st: TileStore, gs: GenState): void {
74	  if (!gs.snowMinX || !gs.snowMaxX) return; // 雪原未生成（守卫）
75	  const ICE = TILE_BY_KEY['ice']!;
76	  const MUD = TILE_BY_KEY['mud']!;
77	  const SILT = TILE_BY_KEY['silt']!;
78	  const SLUSH = TILE_BY_KEY['v_224_slush_block']!;
79	  const STONE = TILE_BY_KEY['stone']!;
80	  for (let y = gs.snowTop; y <= gs.snowBottom && y < st.h; y++) {
81	    for (let x = gs.snowMinX[y]; x < gs.snowMaxX[y]; x++) {
82	      const i = st.idx(x, y);
83	      if (!st.flags[i]) continue;
84	      const t = st.type[i];
85	      if (t === STONE) {
86	        st.setTileSilent(x, y, ICE);
87	      } else if (t === MUD || t === SILT) {
88	        let nearGrass = false;
89	        for (let dy = -3; dy <= 3 && !nearGrass; dy++) {
90	          for (let dx = -3; dx <= 3; dx++) {
91	            if (!st.inBounds(x + dx, y + dy)) continue;
92	            const j = st.idx(x + dx, y + dy);
93	            if (!st.flags[j]) continue;
94	            const sh = TILE_DEFS[st.type[j]]?.vanilla?.sheet;
95	            if (sh === 60 || sh === 70 || sh === 71 || sh === 72) { nearGrass = true; break; }
96	          }
97	        }
98	        if (!nearGrass) st.setTileSilent(x, y, SLUSH);
99	      }
100	    }
101	  }
102	}
103	

```


---

## 👤 User(sidechain) · 2026-08-11T04:09:32.799Z

**📎 ToolResult**

```
1	// 原版 pass 18 "Full Desert" 移植(WorldGen.cs:5525 + GameContent/Biomes/Desert/*)。
2	// 沙丘:SandMound.Place 1:1——sqrt(1-t⁴) 四次超椭圆剖面 + ±10 双随机游走噪声,
3	// 中心削平,整柱纯沙(53)填充到 desert2.Bottom(无硬化沙分层——硬化沙只来自蜂巢壳)。
4	// 蜂巢:DesertHive 场强分层简化(4×2 腔室格阵 cellular 平滑):腔室清空+墙187+化石,
5	// 壁硬化沙/沙+墙216;入口 33% 竖井。记录 gs.undergroundDesert。
6	import type { TileStore } from '../../TileStore';
7	import type { RNG } from '../../../core/rng';
8	import type { GenState } from './GenState';
9	import { T, TILE_BY_KEY } from '../../../data/tiles';
10	
11	const MUD = TILE_BY_KEY['mud']!;
12	const JUNGLE_GRASS = TILE_BY_KEY['v_60_jungle_grass_block']!;
13	const SNOW = TILE_BY_KEY['snow']!;
14	const ICE = TILE_BY_KEY['ice']!;
15	const SAND = T.SAND;
16	const SANDSTONE = TILE_BY_KEY['sandstone']!;
17	const HARDSAND = TILE_BY_KEY['hardened_sand']!;
18	const FOSSIL = TILE_BY_KEY['desert_fossil']!;
19	
20	export function runDesertPass(st: TileStore, rng: RNG, gs: GenState): void {
21	  const { w, h } = st;
22	  const factor = w / 4200;
23	  // 沙漠 X(地牢异侧):x = w/2 + (rand(w/2)/8 + w/16) * -dungeonSide
24	  const half = Math.floor(w / 2);
25	  let num2 = 0, side = gs.dungeonSide, tries = 0;
26	  let x = 0;
27	  for (;;) {
28	    const off = Math.floor(rng.next() * half / 8) + Math.floor(half / 8);
29	    x = half + off * -side;
30	    if (++tries > Math.floor(w / 4)) { side = -side as 1 | -1; tries = 0; if (++num2 >= 2) break; }
31	    if (rowIsValid(st, x, factor)) break;
32	    if (tries > Math.floor(w / 2)) break;
33	  }
34	
35	  // DesertDescription.CreateFromPlacement
36	  const blockCols = Math.max(16, Math.floor(80 * factor));
37	  // DesertDescription.cs:53：(NextDouble()*0.5+1.5)*170*factor → 深度范围 255-340·factor。
38	  // 曾误写 (next+1)*170 → 范围 170-340，最浅时蜂巢只有原版 2/3 深
39	  const blockRows = Math.max(40, Math.floor((rng.next() * 0.5 + 1.5) * 170 * factor));
40	  const width = Math.min(w - 20, Math.floor(4 * blockCols));
41	  const ox = Math.max(10, Math.min(w - 10 - width, x - Math.floor(width / 2)));
42	  // SurfaceMap:平均/最底(钳到 worldSurface-10)
43	  let surfSum = 0, surfMax = 0, count = 0;
44	  for (let i = ox; i < ox + width; i += 4) {
45	    let y = 0;
46	    while (y < h - 2 && !st.flags[st.idx(i, y)]) y++;
47	    surfSum += y; surfMax = Math.max(surfMax, y); count++;
48	  }
49	  const avg = surfSum / Math.max(1, count);
50	  const topY = Math.floor((avg + surfMax) / 2);
51	  const hiveTop = topY + rng.int(40, 59);
52	  const hiveHeight = Math.floor(2 * blockRows);
53	  const hiveBottom = Math.min(h - 2, hiveTop + hiveHeight);
54	  const desertBottom = hiveTop + Math.floor((hiveBottom - hiveTop) / 2);
55	
56	  // ---- SandMound.Place 1:1 ----
57	  const moundH = Math.floor((hiveBottom - hiveTop) / 2);
58	  let coarse = 0, fine = 0; // ±10 双随机游走
59	  for (let dx = -5; dx < width + 5; dx++) {
60	    const cx = ox + dx;
61	    if (cx < 0 || cx >= w) continue;
62	    const t = Math.max(-1, Math.min(1, Math.abs((dx + 5) / (width + 10)) * 2 - 1));
63	    if (dx % 3 === 0) coarse = Math.max(-10, Math.min(10, coarse + rng.int(-1, 1)));
64	    fine = Math.max(-10, Math.min(10, fine + rng.int(-1, 1)));
65	    const profile = Math.sqrt(1 - Math.pow(t, 4));
66	    const moundSurfY = (topY + moundH) - Math.floor(profile * moundH) + coarse;
67	    // 中心削平/边缘抬升(SmoothStep(0.5,0.8,|t|)³)
68	    if (Math.abs(t) < 1) {
69	      const s = Math.max(0, Math.min(1, (Math.abs(t) - 0.5) / 0.3));
70	      const ss = s * s * (3 - 2 * s);
71	      const flatten = Math.min(10 + Math.floor((topY - Math.pow(ss, 3) * 20)) + fine, moundSurfY);
72	      // 从地表上一格清到 flatten(削掉沙丘上方突出物)
73	      let sy = 0;
74	      while (sy < h - 2 && !st.flags[st.idx(cx, sy)]) sy++;
75	      for (let y = sy - 1; y < flatten && y >= 0; y++) {
76	        const i = st.idx(cx, y);
77	        st.type[i] = 0; st.flags[i] = 0; st.wall[i] = 0;
78	      }
79	    }
80	    // 纯沙柱:从 moundSurfY 填到 hiveBottom(整柱)
81	    for (let y = moundSurfY; y < hiveBottom; y++) {
82	      if (y < 0 || y >= h) continue;
83	      const i = st.idx(cx, y);
84	      st.type[i] = SAND; st.flags[i] = 1;
85	      st.liquid[i] = 0; st.liquidType[i] = 0;
86	    }
87	  }
88	
89	  // ---- DesertHive(DesertHive.cs 1:1):椭圆散点 → 深度2 DFS 簇 → AttemptClaim 合并
90	  // 场强 = 各簇内全部块的 Σ1/d²,取前二大簇求和;阈值 3.5/1.8/0.7/0.25 ----
91	  const cellW = 4, cellH = 2;
92	  const gw = blockCols, gh = blockRows;
93	  // 1) 椭圆掩码 50% 散点(ClusterGroup.Generate)
94	  const blockMap: boolean[][] = [];
95	  for (let c = 0; c < gw; c++) blockMap.push(new Array(gh).fill(false));
96	  {
97	    const num1 = Math.floor(gw / 2) - 1, y1 = Math.max(1, Math.floor(gh / 2) - 1);
98	    const num2 = (num1 + 1) * (num1 + 1);
99	    for (let r = 0; r < gh; r++) {
100	      const num3 = (num1 / y1) * (r - y1);
101	      const num4 = Math.min(num1, Math.floor(Math.sqrt(Math.max(0, num2 - num3 * num3))));
102	      for (let c = num1 - num4; c <= num1 + num4; c++) {
103	        if (c < 0 || c >= gw) continue;
104	        blockMap[c][r] = rng.int(0, 1) === 0;
105	      }
106	    }
107	  }
108	  // 2) 深度 2 DFS 搜簇(起点再过 50%),>2 点保留
109	  const pointClusters: Array<Array<[number, number]>> = [];
110	  {
111	    const dfs = (x: number, y: number, level: number, out: Array<[number, number]>) => {
112	      out.push([x, y]);
113	      blockMap[x][y] = false;
114	      level--;
115	      if (level === -1) return;
116	      if (x > 0 && blockMap[x - 1][y]) dfs(x - 1, y, level, out);
117	      if (x < gw - 1 && blockMap[x + 1][y]) dfs(x + 1, y, level, out);
118	      if (y > 0 && blockMap[x][y - 1]) dfs(x, y - 1, level, out);
119	      if (y < gh - 1 && blockMap[x][y + 1]) dfs(x, y + 1, level, out);
120	    };
121	    for (let x = 0; x < gw; x++) {
122	      for (let y = 0; y < gh; y++) {
123	        if (blockMap[x][y] && rng.int(0, 1) === 0) {
124	          const pc: Array<[number, number]> = [];
125	          dfs(x, y, 2, pc);
126	          if (pc.length > 2) pointClusters.push(pc);
127	        }
128	      }
129	    }
130	  }
131	  // 3) 索引图 + AttemptClaim:邻簇随机整体并入或删除
132	  const idxMap: number[][] = [];
133	  for (let c = 0; c < gw; c++) idxMap.push(new Array(gh).fill(-1));
134	  pointClusters.forEach((pc, i) => { for (const [px, py] of pc) idxMap[px][py] = i; });
135	  for (let i = 0; i < pointClusters.length; i++) {
136	    for (const [px, py] of pointClusters[i]) {
137	      if (idxMap[px][py] === -1) break;
138	      const ci = idxMap[px][py];
139	      const claim = (nx: number, ny: number) => {
140	        if (nx < 0 || ny < 0 || nx >= gw || ny >= gh) return;
141	        const other = idxMap[nx][ny];
142	        if (other === -1 || other === ci) return;
143	        const val = rng.int(0, 1) === 0 ? -1 : ci;
144	        for (const [qx, qy] of pointClusters[other]) idxMap[qx][qy] = val;
145	      };
146	      claim(px - 1, py); claim(px + 1, py); claim(px, py - 1); claim(px, py + 1);
147	    }
148	  }
149	  // 4) 重组成簇,<4 点丢弃;块坐标 ±0.25 抖动
150	  const clusters: Array<Array<[number, number]>> = pointClusters.map(() => []);
151	  for (let x = 0; x < gw; x++) {
152	    for (let y = 0; y < gh; y++) {
153	      if (idxMap[x][y] !== -1) clusters[idxMap[x][y]].push([x, y]);
154	    }
155	  }
156	  const finalClusters: Array<Array<[number, number]>> = [];
157	  for (const cl of clusters) {
158	    if (cl.length < 4) continue;
159	    finalClusters.push(cl.map(([bx, by]) => [
160	      bx + (rng.next() - 0.5) * 0.5, by + (rng.next() - 0.5) * 0.5,
161	    ] as [number, number]));
162	  }
163	  const hiveW = width, hiveH = hiveBottom - hiveTop;
164	  // ---- 场强分层(PlaceClustersArea):±10 窗口判簇(簇首块),簇内求和取前二大 ----
165	  for (let dx = -20; dx < hiveW + 20; dx++) {
166	    for (let dy = -20; dy < hiveH + 20; dy++) {
167	      const px = ox + dx, py = hiveTop + dy;
168	      if (!st.inBounds(px, py)) continue;
169	      let shellType: number = SAND;
170	      if (rng.int(0, 2) === 0) shellType = HARDSAND;
171	      const vx = dx / cellW - 0.5, vy = dy / cellH - 0.5;
172	      let m1 = 0, m2 = 0, m1Idx = -1;
173	      for (let ci = 0; ci < finalClusters.length; ci++) {
174	        const c0 = finalClusters[ci][0];
175	        if (Math.abs(c0[0] - vx) > 10 || Math.abs(c0[1] - vy) > 10) continue;
176	        let f = 0;
177	        for (const [bx, by] of finalClusters[ci]) {
178	          const ddx = bx - vx, ddy = by - vy;
179	          f += 1 / (ddx * ddx + ddy * ddy);
180	        }
181	        if (f > m1) { if (m1 > m2) m2 = m1; m1 = f; m1Idx = ci; }
182	        else if (f > m2) m2 = f;
183	      }
184	      const field = m1 + m2;
185	      const ex = (dx / hiveW) * 2 - 1, ey = (dy / hiveH) * 2 - 1;
186	      const isEdge = Math.hypot(ex, ey) >= 0.8;
187	      const i = st.idx(px, py);
188	      if (field > 3.5) {
189	        // 腔室:清空 + 墙187;获胜簇索引 %15==2 → 化石(确定性判定)
190	        st.type[i] = 0; st.flags[i] = 0; st.liquid[i] = 0; st.liquidType[i] = 0;
191	        st.wall[i] = 187;
192	        if (m1Idx % 15 === 2) { st.type[i] = FOSSIL; st.flags[i] = 1; }
193	      } else if (field > 1.8) {
194	        // 隧道带:墙187 + 沙岩;地表以下注岩浆
195	        st.wall[i] = 187;
196	        if (py < gs.worldSurface) { st.liquid[i] = 0; st.liquidType[i] = 0; }
197	        else st.liquidType[i] = 2;
198	        if (!isEdge || st.flags[i]) { st.type[i] = SANDSTONE; st.flags[i] = 1; }
199	      } else if (field > 0.7 || !isEdge) {
200	        // 硬化沙壳:墙216 + 沙/硬化沙(1/3)
201	        st.wall[i] = 216;
202	        st.liquid[i] = 0; st.liquidType[i] = 0;
203	        if (!isEdge || st.flags[i]) { st.type[i] = shellType; st.flags[i] = 1; }
204	      } else if (field > 0.25 && rng.next() < (field - 0.25) / 0.45) {
205	        // 隧道外缘噪声
206	        st.wall[i] = 187;
207	        if (py < gs.worldSurface) { st.liquid[i] = 0; st.liquidType[i] = 0; }
208	        else st.liquidType[i] = 2;
209	        if (st.flags[i]) { st.type[i] = shellType; st.flags[i] = 1; }
210	      }
211	    }
212	  }
213	  // ---- AddTileVariance:沙 53 下方 2 格非实心 → 酥化为 397(装饰 485/484/165/187 略)----
214	  for (let dx = -20; dx < width + 20; dx++) {
215	    for (let dy = -20; dy < hiveH + 20; dy++) {
216	      const px = ox + dx, py = hiveTop + dy;
217	      if (!st.inBounds(px, py) || !st.inBounds(px, py + 2)) continue;
218	      const i = st.idx(px, py);
219	      if (st.type[i] === SAND && st.flags[i]
220	        && !(st.isSolid(px, py + 1) && st.isSolid(px, py + 2))) {
221	        st.type[i] = HARDSAND;
222	      }
223	    }
224	  }
225	
226	  // ---- 入口(33%):竖井通到蜂巢顶(原版四种入口的简化)----
227	  if (rng.next() <= 0.3333) {
228	    const ex = ox + rng.int(Math.floor(width * 0.2), Math.floor(width * 0.8));
229	    let ey = 0;
230	    while (ey < h - 2 && !st.flags[st.idx(ex, ey)]) ey++;
231	    const shaftW = rng.int(0, 3) === 0 ? 8 : 4;
232	    for (let y = ey - 2; y <= hiveTop + 8; y++) {
233	      for (let dx = 0; dx < shaftW; dx++) {
234	        if (!st.inBounds(ex + dx, y)) continue;
235	        const i = st.idx(ex + dx, y);
236	        st.type[i] = 0; st.flags[i] = 0;
237	        st.wall[i] = 187;
238	      }
239	    }
240	  }
241	
242	  gs.undergroundDesert = {
243	    x0: Math.max(0, ox - 10), y0: Math.max(0, topY - 10),
244	    x1: Math.min(w, ox + width + 10), y1: Math.min(h, hiveBottom + 10),
245	  };
246	}
247	
248	function rowIsValid(st: TileStore, x: number, factor: number): boolean {
249	  const width = Math.floor(320 * factor);
250	  const x0 = Math.max(1, x - Math.floor(width / 2));
251	  let y = 0;
252	  while (y < st.h - 2 && !st.flags[st.idx(x, y)]) y++;
253	  y = Math.min(st.h - 2, y + 2);
254	  for (let i = x0; i < Math.min(st.w - 1, x0 + width); i++) {
255	    const t = st.type[st.idx(i, y)];
256	    if (t === MUD || t === JUNGLE_GRASS || t === SNOW || t === ICE) return false;
257	  }
258	  return true;
259	}
260	

```


---

## 🤖 Assistant · 2026-08-11T04:09:50.475Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Key findings so far:

- ShiniesPass: `band(..., 0, surfLow, silver)` — y from 0! (line 44: `band(st, rng, gs, Math.floor(area * 1.7e-4), 0, surfLow, gs.oreTiers.silver, ...)` — "天空带" comment says sky band!). And gold line 47: `band(..., 0, Math.max(1, surfLow - 20), ...)`. These runners have addTile: false → ghost ore types written into sky air! Vanilla "银/钨 天空带 1.7e-4" — in vanilla this is meant to replace dirt at shallow depths (0..worldSurfaceLow covers sky+surface). Since TileRunner without addTile only "should" replace active tiles but the port writes type into air cells too (matching vanilla's inactive type write). This IS a major ghost-type source in the sky.

Let me double check the vanilla: "Shinies" pass 27 in 1.4.0.5 cs:5893-5915:

```csharp
num = (double)(Main.maxTilesX * Main.maxTilesY) * 0.00017;
for (...) {
  WorldGen.TileRunner(i, GenBase._random.Next(0, (int)Main.worldSurfaceLow), GenBase._random.Next(4, 9), GenBase._random.Next(4, 8), Main.copper);
}
```
Hmm something like that — the "sky band" for silver. Yes. So port is 1:1.

So the ghost-type-in-sky writers (all later erased at finalize) include:
1. CavesPass runRocksAndClayPass: line 25 `run(area*0.00015, 0, gs.worldSurfaceLow, T.STONE, 4,14,5,39)` — sky band, plus line 36 `run(area*0.00002, 0, gs.worldSurfaceLow-1, CLAY, ...)`.
2. ShiniesPass silver sky band (line 44) and gold near-surface band (line 47, yMin=0).
3. JunglePass giant mud runner — mud ghost types mostly underground though (start y at rockLevel+ area, going up with strength 400-600, speedY -20, 10000 steps — it can reach high up; mud runner stops at py<0). This writes mud ghost type into air within the jungle column from deep underground up to the top of the world! Actually `if (py < 0 && num2 > 0 && type === MUD) num2 = 0;` — stops at top. The runner is a vertical column of mud with strength ~400-900 (radius huge) — it converts air cells' type to MUD (ghost) across a massive vertical swath in the jungle region, including sky. Hmm, but wait: for MUD in air cells, line 127: `if (cur === T.STONE)` — cur=0 for air so skip; then `else if (FLAG3_ALWAYS.has(cur))` no; `else if (cur === T.SAND)` no... So flag3 false → ghost mud written. YES. The jungle giant runner is the single largest ghost writer, and it spans from deep underground to y<0. But the visible effect in the jungle region only.

Hmm, actually wait. Does the mud runner convert the whole column to mud including the sky? In vanilla, `TileRunner(..., addTile: false)` only sets `type` on inactive tiles too (vanilla does the same!) — vanilla writes type but inactive stays inactive. In vanilla rendering, inactive tiles are not drawn. So identical behavior. The difference: this repo's save format has no active bit, so the ghost types must be purged at finalize. So the "write then erase" is by design, matching vanilla.

4. DesertPass: mound fill writes real sand (flags=1) from moundSurfY down. moundSurfY = (topY + moundH) - profile*moundH + coarse — the dune rises ABOVE the original surface (moundSurfY < topY near center since profile high) → real sky sand blocks (the dune). Also lines 75-78 clear above the mound (from sy-1 to flatten) → that's a "抹除" of sky stuff above the dune! Note this clears tiles in the sky region (removing hill overhangs above the dune).

Also Desert hive field layering can set type/flags above worldSurface? hiveTop = topY + 40..59 → below surface. OK.

5. IceBiomePass: converts existing active tiles only (skips !flags). No new sky blocks. But wait — line 41: `if (y < num2)` — y from 0 to lavaLine-140, i.e. includes sky; but `if (!st.flags[i]) continue;` so only converts active blocks in sky (floating islands → snow? Islands are generated AFTER ice biome in vanillaBiomes order, so no). OK no sky writes.

Now remaining: CorruptionPass, MushroomPass, MarbleGranitePass, DirtToMudPass, GrassPass, Spread, IslandHousePass, SwordShrinePass, BuriedChestsPass, TrapsPass, HellFortPass, HiveSpiderPass, TemplePass, DungeonPass.

DungeonPass — dungeon entrance is above ground (sky): the entrance corridor/tower goes up into the sky? In vanilla, the dungeon entrance is at the surface and the structure extends below; but there's a visible above-ground entrance. Let me check.

SwordShrinePass — "竖井+水潭洞+土丘剑" — mound of dirt above surface → sky writer.

Let me read these.
````

</details>


---

## 🤖 Assistant · 2026-08-11T04:09:50.627Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SwordShrinePass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:50.647Z

**📎 ToolResult**

```
1	// 原版附魔剑圣地(EnchantedSwordBiome.cs L16-85)移植。
2	// 外形:地表 1 格宽竖井 + 地下 ~40×40 水潭洞穴(花墙 68/草缘/藤蔓)+ 中央土丘上的剑。
3	import type { TileStore } from '../../TileStore';
4	import type { RNG } from '../../../core/rng';
5	import type { GenState } from './GenState';
6	import { T, TILE_BY_KEY } from '../../../data/tiles';
7	import { placeFurn } from './DungeonPass';
8	
9	const SWORD_TILE = TILE_BY_KEY['v_187_decos_3x2_group_2']!;
10	const FAKE_TILE = TILE_BY_KEY['v_186_decos_3x2']!;
11	const VINE = TILE_BY_KEY['v_52_vines']!;
12	
13	export function runSwordShrinePass(st: TileStore, rng: RNG, gs: GenState): void {
14	  const { w } = st;
15	  const count = 2; // 每世界约 1-2 处
16	  for (let n = 0; n < count * 80; n++) {
17	    // 位置:左/右 30%
18	    const left = rng.next() < 0.5;
19	    const x = left ? rng.int(50, Math.floor(w * 0.3)) : rng.int(Math.floor(w * 0.7), w - 50);
20	    const oy = Math.floor(gs.worldSurface) + rng.int(50, 99);
21	    if (!st.inBounds(x, oy) || !st.flags[st.idx(x, oy)]) continue;
22	    // 上方不能有沙(不在沙漠下)
23	    let sandAbove = false;
24	    for (let y = 0; y < oy && !sandAbove; y++) if (st.type[st.idx(x, y)] === T.SAND && st.flags[st.idx(x, y)]) sandAbove = true;
25	    if (sandAbove) continue;
26	    // 洞穴中心:种子点上方 10-20(EnchantedSwordBiome 的 point1/point2 语义)
27	    const sy = oy - rng.int(10, 20);
28	    if (sy < gs.worldSurface + 30) continue;
29	    // ---- 地下小屋(Slime(20, 0.8-1.3) 清空 + 灌水 + 花墙 68)----
30	    const xScale = 0.8 + rng.next() * 0.5;
31	    const rx = 20 * xScale, ry = 20;
32	    for (let dx = Math.floor(-rx); dx <= Math.ceil(rx); dx++) {
33	      for (let dy = Math.floor(-ry); dy <= Math.ceil(ry); dy++) {
34	        const d = (dx / rx) ** 2 + (dy / ry) ** 2;
35	        if (d > 1) continue;
36	        if (rng.next() < 0.15) continue; // Blotches 不规则边
37	        const px = x + dx, py = sy + dy;
38	        if (!st.inBounds(px, py)) continue;
39	        const i = st.idx(px, py);
40	        st.type[i] = 0; st.flags[i] = 0;
41	        st.wall[i] = 68; // Flower Wall
42	        st.liquid[i] = 255; st.liquidType[i] = 1;
43	
44	      }
45	    }
46	    // 草缘(洞缘土改草)+ 藤蔓
47	    for (let dx = Math.floor(-rx); dx <= Math.ceil(rx); dx++) {
48	      for (let dy = Math.floor(-ry); dy <= Math.ceil(ry); dy++) {
49	        const px = x + dx, py = sy + dy;
50	        if (!st.inBounds(px, py)) continue;
51	        const i = st.idx(px, py);
52	        if (!st.flags[i] || st.type[i] !== T.DIRT) continue;
53	        // 实心但邻空腔 → 草
54	        let nearCavity = false;
55	        for (const [ax, ay] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as const) {
56	          const j = st.idx(px + ax, py + ay);
57	          if (st.inBounds(px + ax, py + ay) && !st.flags[j] && st.wall[j] === 68) { nearCavity = true; break; }
58	        }
59	        if (nearCavity) {
60	          st.type[i] = T.GRASS;
61	          if (py % 3 === 0 && st.inBounds(px, py + 1) && !st.flags[st.idx(px, py + 1)]) {
62	            st.setTileSilent(px, py + 1, VINE, 0, 0);
63	          }
64	        }
65	      }
66	    }
67	    // 中央土丘(14×14 泥土)隆出水面
68	    for (let dx = -7; dx <= 7; dx++) {
69	      for (let dy = -7; dy <= 7; dy++) {
70	        if ((dx / 7) ** 2 + (dy / 7) ** 2 > 1) continue;
71	        const px = x + dx, py = sy - 4 + dy;
72	        if (!st.inBounds(px, py)) continue;
73	        const i = st.idx(px, py);
74	        st.type[i] = T.DIRT; st.flags[i] = 1;
75	        st.liquid[i] = 0;
76	      }
77	    }
78	    // ---- 1 格宽竖井通地表(切割一切,原版 SkipTiles 仅生命木)----
79	    for (let y = sy + 5; y >= Math.max(2, Math.floor(gs.worldSurface) - 2); y--) {
80	      if (!st.inBounds(x, y)) continue;
81	      const i = st.idx(x, y);
82	      st.type[i] = 0; st.flags[i] = 0;
83	      st.liquid[i] = 0;
84	    }
85	    // 剑插土丘上方(cs L76-78):真 1/3 → tile187 style17,假 → tile186 style15。
86	    // 原版 PlaceTile force=true 强制覆盖;3×2 完整放置(底行锚点,居中),
87	    // 样式步长 fw*18=54(此前单格残件 + 36 步长 + 净空校验致常年放不上)
88	    const real = rng.next() < 1 / 3;
89	    const swordTile = real ? SWORD_TILE : FAKE_TILE;
90	    const swordStyle = real ? 17 : 15;
91	    for (let dx = 0; dx < 3; dx++) {
92	      for (let dy = 0; dy < 2; dy++) {
93	        if (st.inBounds(x - 1 + dx, sy - 13 + dy)) {
94	          st.setTileSilent(x - 1 + dx, sy - 13 + dy, swordTile, swordStyle * 54 + dx * 18, dy * 18);
95	        }
96	      }
97	    }
98	    return; // 每世界一处足矣
99	  }
100	}
101	

```


---

## 🤖 Assistant · 2026-08-11T04:09:50.848Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:50.860Z

**📎 ToolResult**

```
1	// 原版 "Buried Chests"(L7907)+ "Surface Chests"(L8019)+ "Water Chests"(L8058)移植。
2	// 样式语义(AddBuriedChest L21335+ / PlaceChestDirect L34112:frameX=36*style 横排):
3	//   -1 默认:y≥ws+25 → 金(1);冰系 tile(147/161/162)→ 冰箱(11)+冰系战利品;
4	//   地下沙漠 → tile467 style10+沙漠战利品;y>h-205 → 地狱箱(4)+地狱武器序;
5	//   Water Chests pass 固定 style17(水箱)+水中战利品;地表箱 style0 木箱。
6	// 宝箱数量(Configuration.json):CaveChestCount 35-40 ScaleWith:WorldArea(÷5040000)、
7	//   UnderworldChestCount 10-15 ScaleWith:WorldWidth(÷4200)。金/木箱主件战利品池
8	//   = cs:21500+ 大 switch 的常用主件子集(id 经 id-maps 核对)。
9	import type { TileStore } from '../../TileStore';
10	import type { RNG } from '../../../core/rng';
11	import type { GenState } from './GenState';
12	import { TILE_BY_KEY, TILE_DEFS } from '../../../data/tiles';
13	import { ITEM_BY_KEY } from '../../../data/items';
14	import { vanillaItemKey } from '../../../data/vanillaNpcs';
15	
16	const CHEST = TILE_BY_KEY['chest']!;
17	const CHEST2 = TILE_BY_KEY['v_467_chests_group_2']!;
18	const SNOW = TILE_BY_KEY['snow']!;
19	const ICE = TILE_BY_KEY['ice']!;
20	const THIN_ICE = TILE_BY_KEY['thin_ice']!;
21	const ALTAR = TILE_BY_KEY['v_26_altars']!;
22	const TALTAR = TILE_BY_KEY['v_237_lihzahrd_altar']!;
23	
24	export type ChestSink = Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null>; locked?: boolean }>;
25	
26	const iceLoot = [
27	  'vi_670_ice_boomerang', 'vi_724_ice_blade', 'vi_950_ice_skates',
28	  'vi_1319_snowball_cannon', 'vi_987_blizzard_in_a_bottle', 'vi_1579_flurry_boots',
29	];
30	const desertShallowLoot = ['vi_4056_ancient_chisel', 'vi_4055_dunerider_boots', 'vi_4262_snake_charmer_s_flute', 'vi_4263_magic_conch'];
31	const desertDeepLoot = ['vi_4061_storm_spear', 'vi_4062_thunder_zapper', 'vi_4276_bast_statue'];
32	const hellLoot = ['vi_274_dark_lance', 'vi_112_flower_of_fire', 'vi_218_flamelash', 'vi_3019_hellwing_bow', 'vi_5010_treasure_magnet'];
33	const waterLoot = ['vi_186_breathing_reed', 'vi_4404_inner_tube', 'vi_277_trident', 'vi_187_flipper'];
34	
35	/** 地牢墙集合(DungeonPass roomWall:L850 type 7/8/9 + 94-99 变体)。
36	 *  原版只排除 wallDungeon[](AddBuriedChest L17086)——曾用 wl∈[7,99] 一刀切,
37	 *  连带拒掉大量自然洞穴墙(泥墙/大理石墙),额外压低洞穴箱成功率 */
38	const DUNGEON_WALLS = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
39	function isDungeonWall(wl: number): boolean {
40	  return DUNGEON_WALLS.has(wl);
41	}
42	
43	/** 金箱主件池(cs:21500+ 常用主件子集,原版 id) */
44	const goldMainIds = [285, 953, 53, 54, 158, 50, 5011, 42, 280, 279, 3069, 49];
45	/** 木箱主件池(地表箱) */
46	const woodMainIds = [281, 3069, 280, 953, 285, 946];
47	
48	/** 主件 + 概率杂物(火把/药水)。cs:21500+ 的 switch 只取主件语义子集 */
49	function rollCommonLoot(rng: RNG, mainIds: number[]): Array<{ id: number; stack: number } | null> {
50	  const key = vanillaItemKey(mainIds[rng.int(0, mainIds.length - 1)]);
51	  const out: Array<{ id: number; stack: number } | null> = Array(10).fill(null);
52	  if (key && ITEM_BY_KEY[key] !== undefined) out[0] = { id: ITEM_BY_KEY[key], stack: 1 };
53	  const roll = rng.int(0, 2);
54	  if (roll === 0) out[1] = { id: ITEM_BY_KEY['torch'] ?? out[0]?.id ?? -1, stack: rng.int(3, 9) };
55	  else if (roll === 1) out[1] = { id: ITEM_BY_KEY['lesser_healing_potion'] ?? -1, stack: rng.int(1, 3) };
56	  return out;
57	}
58	
59	/** AddBuriedChest 近似:从 (i,j) 向下落,按上下文解析样式与战利品,2×2 放置 */
60	export function placeBuriedChest(
61	  st: TileStore, rng: RNG, gs: GenState, chests: ChestSink,
62	  i: number, j: number, opts: { style?: number; tile?: number; loot?: string } = {},
63	): boolean {
64	  // ±2 内不得有滚石/祭坛/其他宝箱(原版 num4=2 检查)
65	  for (let dx = -2; dx <= 2; dx++) {
66	    for (let dy = -2; dy <= 2; dy++) {
67	      if (!st.inBounds(i + dx, j + dy)) continue;
68	      const t = st.type[st.idx(i + dx, j + dy)];
69	      if (!st.flags[st.idx(i + dx, j + dy)]) continue;
70	      if (t === ALTAR || t === TALTAR || t === CHEST || t === CHEST2) return false;
71	    }
72	  }
73	  // 下落到地面
74	  let gy = j;
75	  let guard = 0;
76	  while (guard++ < 400 && st.inBounds(i, gy) && !st.flags[st.idx(i, gy)]) gy++;
77	  if (!st.inBounds(i, gy) || !st.flags[st.idx(i, gy)]) return false;
78	  if (!TILE_DEFS[st.type[st.idx(i, gy)]]?.solid) return false;
79	
80	  let tile = opts.tile ?? CHEST;
81	  let style = opts.style;
82	  let lootKey = opts.loot;
83	  if (style === undefined) {
84	    if (gy > st.h - 205) {
85	      // 地狱箱:style 4 + 地狱武器序(每个世界乱序取用)
86	      style = 4;
87	      if (!lootKey) lootKey = hellLoot[rng.int(0, hellLoot.length - 1)];
88	    } else {
89	      style = gy >= gs.worldSurface + 25 ? 1 : 0;
90	      const tBelow = st.type[st.idx(i, gy)];
91	      if (!lootKey && (tBelow === SNOW || tBelow === ICE || tBelow === THIN_ICE)) {
92	        style = 11;
93	        lootKey = iceLoot[rng.int(0, iceLoot.length - 1)];
94	        if (rng.int(0, 19) === 0) lootKey = 'vi_997_extractinator';
95	      }
96	      const ud = gs.undergroundDesert;
97	      if (!lootKey && ud && i >= ud.x0 && i <= ud.x1 && gy >= ud.y0 && gy <= ud.y1
98	        && gy >= gs.worldSurface + 25 && gy <= st.h - 205) {
99	        tile = CHEST2;
100	        style = 10;
101	        const deep = gy > (ud.y0 * 3 + ud.y1 * 4) / 7;
102	        const pool = deep ? desertDeepLoot : desertShallowLoot;
103	        lootKey = pool[rng.int(0, pool.length - 1)];
104	      }
105	    }
106	  }
107	
108	  // 2×2 放置:顶行 frameY=0、frameX = style*36 + dx*18(PlaceChestDirect 语义)
109	  const topY = gy - 2;
110	  if (topY < 1) return false;
111	  for (let dx = 0; dx < 2; dx++) {
112	    for (let dy = 0; dy < 2; dy++) {
113	      if (!st.inBounds(i + dx, topY + dy) || st.flags[st.idx(i + dx, topY + dy)]) return false;
114	    }
115	  }
116	  if (!st.inBounds(i + 1, gy) || !st.flags[st.idx(i + 1, gy)]
117	    || !TILE_DEFS[st.type[st.idx(i + 1, gy)]]?.solid) return false;
118	  const fw = TILE_DEFS[tile].vanilla?.fw ?? 2;
119	  for (let dx = 0; dx < 2; dx++) {
120	    for (let dy = 0; dy < 2; dy++) {
121	      st.setTileSilent(i + dx, topY + dy, tile, style * fw * 18 + dx * 18, dy * 18);
122	    }
123	  }
124	  // 战利品:特殊池优先;金(1)/木(0)箱走主件+杂物池(此前是空箱,体感稀缺主因之一)
125	  let items: Array<{ id: number; stack: number } | null>;
126	  const lootId = lootKey ? ITEM_BY_KEY[lootKey] : undefined;
127	  if (lootId !== undefined) {
128	    items = [{ id: lootId, stack: 1 }, ...Array(9).fill(null)];
129	  } else if (style === 1) {
130	    items = rollCommonLoot(rng, goldMainIds);
131	  } else if (style === 0) {
132	    items = rollCommonLoot(rng, woodMainIds);
133	  } else {
134	    items = Array(10).fill(null);
135	  }
136	  chests.push({ x: i, y: topY, items });
137	  return true;
138	}
139	
140	/** Buried Chests pass:L7907 洞穴段(CaveChestCount 35-40 × WorldArea/5040000)。
141	 *  ★地狱段拆出 runUnderworldChestsPass:本函数曾在 hellPass 之前执行,
142	 *  地狱箱被后续地狱地形重写 100% 抹除(实际 0 个) */
143	export function runBuriedChestsPass(st: TileStore, rng: RNG, gs: GenState, chests: ChestSink): void {
144	  const { w, h } = st;
145	  const yMin = Math.floor((gs.worldSurfaceHigh + 20 + gs.rockLevel) / 2);
146	  // 洞穴箱:35-40 × 面积缩放(Configuration.json CaveChestCount ScaleWith:WorldArea;
147	  // 小世界(4200×1200=5040000)= 1.0 → 35-40;中 ×2.29;大 ×4.0)
148	  const target = Math.round(rng.int(35, 40) * (w * h) / 5040000);
149	  let fail = 10000;
150	  for (let n = 0; n < target && fail > 0; ) {
151	    const x = rng.int(20, w - 21);
152	    const y = rng.int(yMin, h - 231);
153	    const wl = st.inBounds(x, y) ? st.wall[st.idx(x, y)] : -1;
154	    if (isDungeonWall(wl) || !placeBuriedChest(st, rng, gs, chests, x, y)) {
155	      fail--; continue;
156	    }
157	    n++;
158	  }
159	}
160	
161	/** 地狱箱(UnderworldChestCount 10-15 × WorldWidth/4200)。
162	 *  必须在 hellPass + 地狱屋之后调用(原版 Underworld(cs:13697) < Buried Chests(cs:17066)) */
163	export function runUnderworldChestsPass(st: TileStore, rng: RNG, gs: GenState, chests: ChestSink): void {
164	  const { w, h } = st;
165	  const target = Math.round(rng.int(10, 15) * (w / 4200));
166	  let fail = 10000;
167	  for (let n = 0; n < target && fail > 0; ) {
168	    const x = rng.int(20, w - 21);
169	    const y = rng.int(h - 200, h - 51);
170	    if (!placeBuriedChest(st, rng, gs, chests, x, y)) {
171	      fail--; continue;
172	    }
173	    n++;
174	  }
175	}
176	
177	/** Surface Chests pass(L8019):w*0.005 个地表木箱(style 0) */
178	export function runSurfaceChestsPass(st: TileStore, rng: RNG, gs: GenState, chests: ChestSink): void {
179	  const { w } = st;
180	  const count = Math.floor(w * 0.005);
181	  for (let n = 0; n < count; n++) {
182	    let ok = false;
183	    for (let tries = 0; tries < 2000 && !ok; tries++) {
184	      const x = rng.int(300, w - 301);
185	      const y = rng.int(Math.floor(gs.worldSurfaceLow), Math.floor(gs.worldSurface));
186	      if (!st.inBounds(x, y)) continue;
187	      const i = st.idx(x, y);
188	      // 空格 + 泥土系自然墙(2/59/244)
189	      if (st.flags[i] || (st.wall[i] !== 2 && st.wall[i] !== 59 && st.wall[i] !== 244)) continue;
190	      if (placeBuriedChest(st, rng, gs, chests, x, y, { style: 0 })) ok = true;
191	    }
192	  }
193	}
194	
195	/** Water Chests pass(L8058):9×w/4200 个,水中(liquid≥250 且为水)放置,style 17 */
196	export function runWaterChestsPass(st: TileStore, rng: RNG, gs: GenState, chests: ChestSink): void {
197	  const { w } = st;
198	  const count = Math.floor(9 * (w / 4200));
199	  let waterIdx = 0;
200	  for (let n = 0; n < count; n++) {
201	    // 战利品序(cs L8087-8112):1/10 鲨鱼饵/水上漂靴,否则循环 芦笛/游泳圈/三叉戟/脚蹼
202	    let loot: string;
203	    if (rng.int(0, 9) === 0) loot = 'vi_4425_shark_bait';
204	    else if (rng.int(0, 9) === 0) loot = 'vi_863_water_walking_boots';
205	    else {
206	      loot = waterLoot[waterIdx % waterLoot.length];
207	      waterIdx++;
208	    }
209	    let ok = false;
210	    for (let tries = 0; tries < 10000 && !ok; tries++) {
211	      const x = rng.int(50, w - 51);
212	      const y = rng.int(1, st.h - 210);
213	      if (!st.inBounds(x, y)) continue;
214	      const i = st.idx(x, y);
215	      if (st.liquid[i] < 250 || st.liquidType[i] === 2) continue;
216	      if (placeBuriedChest(st, rng, gs, chests, x, y, { style: 17, loot })) ok = true;
217	    }
218	  }
219	}
220	

```


---

## 🤖 Assistant · 2026-08-11T04:09:54.212Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
SwordShrine: mound of dirt is underground (sy = worldSurface + 30..79, mound at sy-4±7 — still underground). The shaft clears to worldSurface-2. Sword placed at sy-13 — underground. No sky writes.

Buried chests: surface chests y between worldSurfaceLow and worldSurface (below surface). No sky.

Now check: GrassPass, Spread, MushroomPass, MarbleGranitePass, DirtToMudPass, CorruptionPass, IslandHousePass, TrapsPass, HellFortPass, HiveSpiderPass, TemplePass, DungeonPass. Let me grep for the key parts rather than read everything. DungeonPass is 1635 lines — let me grep for its y-ranges and any writes above worldSurface.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:09:54.359Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GrassPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:54.373Z

**📎 ToolResult**

```
1	// 原版 pass 16 "Grass"(WorldGen.cs:5440)移植:播草种。
2	// 地下(worldSurfaceLow-High 间)与地表上方各随机点:四邻全为活性泥土 → 中心转草。
3	import type { TileStore } from '../../TileStore';
4	import type { RNG } from '../../../core/rng';
5	import type { GenState } from './GenState';
6	import { T } from '../../../data/tiles';
7	
8	export function runGrassPass(st: TileStore, rng: RNG, gs: GenState): void {
9	  const { w, h } = st;
10	  const count = (w * h) / 500;
11	  const isDirt = (x: number, y: number) =>
12	    st.inBounds(x, y) && st.flags[st.idx(x, y)] && st.type[st.idx(x, y)] === T.DIRT;
13	  const seed = (x: number, y: number) => {
14	    if (isDirt(x - 1, y) && isDirt(x + 1, y) && isDirt(x, y - 1) && isDirt(x, y + 1)) {
15	      const i = st.idx(x, y);
16	      st.flags[i] = 1;
17	      st.type[i] = T.GRASS;
18	    }
19	  };
20	  for (let n = 0; n < count; n++) {
21	    const x1 = rng.int(1, w - 2);
22	    let y1 = rng.int(gs.worldSurfaceLow, Math.max(gs.worldSurfaceLow, gs.worldSurfaceHigh - 1));
23	    if (y1 >= h) y1 = h - 2;
24	    seed(x1, y1);
25	    const x2 = rng.int(1, w - 2);
26	    let y2 = rng.int(0, Math.max(1, gs.worldSurfaceLow - 1));
27	    if (y2 >= h) y2 = h - 2;
28	    seed(x2, y2);
29	  }
30	}
31	

```


---

## 🤖 Assistant · 2026-08-11T04:09:54.592Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:54.606Z

**📎 ToolResult**

```
1	// 原版 pass 21 "Marble" / 22 "Granite" 移植(MarbleBiome.cs / GraniteBiome.cs)。
2	// 大理石:板格穹顶洞窟——宽 Next(80,150)/3×3 = 78-149 tile,高 39-57;
3	// 上半中空(墙 178)+下半实心大理石(367),边缘毛化。
4	// 花岗岩:200×200 岩浆区——大实心花岗岩体(368,墙 180)+ digTunnel 蜿蜒洞。
5	// 位置:横向扫过,避开中部 45-55% 与冰雪/丛林/沙漠带(BiomeTileCheck 半径 50 简化为 30)。
6	import type { TileStore } from '../../TileStore';
7	import type { RNG } from '../../../core/rng';
8	import type { GenState } from './GenState';
9	import { T, TILE_BY_KEY } from '../../../data/tiles';
10	import { tileRunner, digTunnel } from './TileRunner';
11	
12	const MARBLE = TILE_BY_KEY['v_367_marble_block']!;
13	const GRANITE = TILE_BY_KEY['v_368_granite_block']!;
14	const SNOW = TILE_BY_KEY['snow']!, ICE = TILE_BY_KEY['ice']!;
15	const JUNGLE_GRASS = TILE_BY_KEY['v_60_jungle_grass_block']!;
16	const SANDSTONE = TILE_BY_KEY['sandstone']!, HARDSAND = TILE_BY_KEY['hardened_sand']!;
17	
18	export function runMarbleGranitePass(st: TileStore, rng: RNG, gs: GenState): void {
19	  const count = Math.max(2, Math.floor(st.w / 700)); // C# (int)
20	  // 大理石带:xPad 80;花岗岩带:xPad 100
21	  placeMarbleCaves(st, rng, gs, count, 80);
22	  placeGraniteCaves(st, rng, gs, count, 100);
23	}
24	
25	function biomeClear(st: TileStore, x: number, y: number): boolean {
26	  // BiomeTileCheck 简化:半径 30 内无冰雪/丛林/沙漠材料
27	  for (let dx = -30; dx <= 30; dx += 5) {
28	    for (let dy = -30; dy <= 30; dy += 5) {
29	      if (!st.inBounds(x + dx, y + dy)) continue;
30	      const t = st.type[st.idx(x + dx, y + dy)];
31	      if (t === SNOW || t === ICE || t === JUNGLE_GRASS || t === SANDSTONE || t === HARDSAND) return false;
32	    }
33	  }
34	  return true;
35	}
36	
37	/** 大理石穹顶洞窟(MarbleBiome.Place 主体流程简化) */
38	function placeMarbleCaves(st: TileStore, rng: RNG, gs: GenState, count: number, xPad: number): void {
39	  for (let n = 0; n < count; n++) {
40	    // 横向扫过分布
41	    let x = Math.floor((n / count) * (st.w - 2 * xPad)) + xPad + rng.int(-20, 20);
42	    while (x > st.w * 0.45 && x < st.w * 0.55) x = rng.int(gs.beachLeftEnd, st.w - gs.beachLeftEnd - 1);
43	    x = Math.max(xPad, Math.min(st.w - xPad, x));
44	    const y = rng.int(gs.rockLevel + 20, Math.max(gs.rockLevel + 21, st.h - 240));
45	    if (!biomeClear(st, x, y)) continue;
46	    // 尺寸(MarbleBiome):宽 78-149,高 39-57
47	    const halfW = Math.floor((rng.int(80, 149) / 3) * 3 / 2);   // 39-74
48	    const fullH = Math.floor((rng.int(40, 59) / 3) * 3);         // 39-57
49	    const halfH = Math.floor(fullH / 2);
50	    const oy = Math.max(4, y - halfH);
51	    // 椭圆穹顶放置
52	    for (let dx = -halfW; dx <= halfW; dx++) {
53	      const chord = Math.floor(Math.sqrt(Math.max(0, 1 - (dx / halfW) ** 2)) * halfH);
54	      if (chord <= 0) continue;
55	      for (let dy = -chord; dy <= chord; dy++) {
56	        const px = x + dx, py = oy + halfH + dy;
57	        if (!st.inBounds(px, py)) continue;
58	        const i = st.idx(px, py);
59	        // 上半(含中线以上 40%)= 洞窟:墙 178,保留原 tile 但清实心块?原版腔内 ClearEverything
60	        if (dy < -chord * 0.2) {
61	          st.type[i] = 0; st.flags[i] = 0;
62	          st.wall[i] = 178;
63	        } else if (dy > chord * 0.15 || rng.next() < 0.4) {
64	          // 下半 = 实心大理石(矿石保留由 flag3 语义覆盖,这里直接覆盖)
65	          st.type[i] = MARBLE; st.flags[i] = 1;
66	          if (dy < chord * 0.3) st.wall[i] = 178;
67	        }
68	      }
69	      // 边缘毛化:两端列 50% 跳过
70	      if ((dx === -halfW || dx === halfW) && rng.next() < 0.5) continue;
71	    }
72	  }
73	}
74	
75	/** 花岗岩岩浆体(GraniteBiome.Place 简化:200×200 区大实心体 + 蜿蜒洞) */
76	function placeGraniteCaves(st: TileStore, rng: RNG, gs: GenState, count: number, xPad: number): void {
77	  for (let n = 0; n < count; n++) {
78	    let x = Math.floor((n / count) * (st.w - 2 * xPad)) + xPad + rng.int(-20, 20);
79	    while (x > st.w * 0.45 && x < st.w * 0.55) x = rng.int(gs.beachLeftEnd, st.w - gs.beachLeftEnd - 1);
80	    x = Math.max(xPad, Math.min(st.w - xPad, x));
81	    const y = rng.int(gs.rockLevel + 20, Math.max(gs.rockLevel + 21, st.h - 240));
82	    if (!biomeClear(st, x, y)) continue;
83	    // 大实心花岗岩体(半径 ~55-75),矿石保留:用 tileRunner(石族只换石头)
84	    const radius = rng.int(55, 75);
85	    tileRunner(st, rng, gs, x, y, { strength: radius * 2, steps: 30, type: GRANITE });
86	    // 墙 180 涂抹
87	    for (let dx = -radius; dx <= radius; dx += 2) {
88	      for (let dy = -radius; dy <= radius; dy += 2) {
89	        if (!st.inBounds(x + dx, y + dy)) continue;
90	        const i = st.idx(x + dx, y + dy);
91	        if (st.type[i] === GRANITE && dx * dx + dy * dy < radius * radius) st.wall[i] = 180;
92	      }
93	    }
94	    // 岩浆洞:2-3 条蜿蜒隧道穿体(深于 lavaLine-30 用岩浆)
95	    const deep = y > gs.lavaLine - 30;
96	    for (let k = 0; k < rng.int(2, 3); k++) {
97	      const dx = rng.int(-100, 100) * 0.01, dy = rng.int(-100, 100) * 0.01;
98	      digTunnel(st, rng, x + rng.int(-radius / 2, radius / 2), y + rng.int(-radius / 2, radius / 2),
99	        dx, dy, rng.int(30, 60), rng.int(3, 6), deep && rng.next() < 0.5);
100	    }
101	    // 孤块清理:3×3 实心邻 <3 的花岗岩移除
102	    for (let dx = -radius; dx <= radius; dx++) {
103	      for (let dy = -radius; dy <= radius; dy++) {
104	        if (!st.inBounds(x + dx, y + dy)) continue;
105	        const i = st.idx(x + dx, y + dy);
106	        if (st.type[i] !== GRANITE || !st.flags[i]) continue;
107	        let n = 0;
108	        for (let ax = -1; ax <= 1; ax++) for (let ay = -1; ay <= 1; ay++) {
109	          const j = st.idx(x + dx + ax, y + dy + ay);
110	          if (st.inBounds(x + dx + ax, y + dy + ay) && st.flags[j]) n++;
111	        }
112	        if (n < 3) { st.type[i] = 0; st.flags[i] = 0; st.wall[i] = 180; }
113	      }
114	    }
115	  }
116	}
117	

```


---

## 🤖 Assistant · 2026-08-11T04:09:55.052Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DirtToMudPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:55.062Z

**📎 ToolResult**

```
1	// 原版 pass 23 "Dirt To Mud"(L5809) + 24 "Silt"(L5819)移植。
2	// Dirt To Mud:area/1000 个小泥 runner 铺深层(避开沙 53);
3	// Silt:岩层以下淤泥 123 脉(避开沙漠墙 187/216)。
4	import type { TileStore } from '../../TileStore';
5	import type { RNG } from '../../../core/rng';
6	import type { GenState } from './GenState';
7	import { T, TILE_BY_KEY } from '../../../data/tiles';
8	import { tileRunner } from './TileRunner';
9	
10	const MUD = TILE_BY_KEY['mud']!;
11	const SILT = TILE_BY_KEY['silt']!;
12	const SAND = T.SAND;
13	
14	export function runDirtToMudAndSiltPass(st: TileStore, rng: RNG, gs: GenState): void {
15	  const { w, h } = st;
16	  const area = w * h;
17	  // Dirt To Mud:小泥团撒深层
18	  for (let n = 0; n < area / 1000; n++) {
19	    tileRunner(st, rng, gs, rng.int(0, w - 1), rng.int(gs.rockLevelLow, h - 1), {
20	      strength: rng.int(2, 5), steps: rng.int(2, 39), type: MUD, ignoreTileType: SAND,
21	    });
22	  }
23	  // Silt:两档淤泥脉(沙漠墙区跳过)
24	  for (let n = 0; n < area * 0.0001; n++) {
25	    const i = rng.int(0, w - 1);
26	    const j = rng.int(gs.rockLevelHigh, h - 1);
27	    const wall = st.wall[st.idx(i, j)];
28	    if (wall !== 187 && wall !== 216) {
29	      tileRunner(st, rng, gs, i, j, { strength: rng.int(5, 11), steps: rng.int(15, 49), type: SILT });
30	    }
31	  }
32	  for (let n = 0; n < area * 0.0005; n++) {
33	    const i = rng.int(0, w - 1);
34	    const j = rng.int(gs.rockLevelHigh, h - 1);
35	    const wall = st.wall[st.idx(i, j)];
36	    if (wall !== 187 && wall !== 216) {
37	      tileRunner(st, rng, gs, i, j, { strength: rng.int(2, 4), steps: rng.int(2, 4), type: SILT });
38	    }
39	  }
40	}
41	

```


---

## 🤖 Assistant · 2026-08-11T04:09:55.062Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MushroomPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:09:55.073Z

**📎 ToolResult**

```
1	// 原版 pass 20 "Mushroom Patches"(WorldGen.cs:5634 + ShroomPatch L48648)移植。
2	// 岩层深处放 numMushroomBiomes 个蘑菇生态:ShroomPatch 泥 blob(墙 80 蘑菇),
3	// 随后泥 59→蘑菇草 70 全图传播(我们的 spreadGrassAll 近似原版逐 tile SpreadGrass)。
4	import type { TileStore } from '../../TileStore';
5	import type { RNG } from '../../../core/rng';
6	import type { GenState } from './GenState';
7	import { TILE_BY_KEY } from '../../../data/tiles';
8	import { tileRunner } from './TileRunner';
9	import { spreadGrassAll } from './Spread';
10	
11	const MUD = TILE_BY_KEY['mud']!;
12	const JUNGLE_GRASS = TILE_BY_KEY['v_60_jungle_grass_block']!;
13	const MUSH_GRASS = TILE_BY_KEY['v_70_mushroom_grass_block']!;
14	const SNOW = TILE_BY_KEY['snow']!;
15	const ICE = TILE_BY_KEY['ice']!;
16	const THIN_ICE = TILE_BY_KEY['thin_ice']!;
17	const GRANITE = TILE_BY_KEY['v_368_granite_block']!;
18	const MARBLE = TILE_BY_KEY['v_367_marble_block']!;
19	
20	export function runMushroomPass(st: TileStore, rng: RNG, gs: GenState): void {
21	  const { w, h } = st;
22	  const van = w / 4200;
23	  // 原版:min(w/700, maxMushroomBiomes=50, WorldGen.cs:111/5637)
24	  const maxBiomes = Math.min(Math.floor(w / 700), 50);
25	  const placed: Array<[number, number]> = [];
26	
27	  for (let n = 0; n < maxBiomes; n++) {
28	    let attempts = 0;
29	    while (attempts <= Math.floor(w / 2)) {
30	      let i = rng.int(Math.floor(w * 0.2), Math.floor(w * 0.8) - 1);
31	      if (attempts > Math.floor(w / 4)) {
32	        i = rng.int(Math.floor(w * 0.25), Math.floor(w * 0.975) - 1);
33	      }
34	      const j = rng.int(gs.rockLevel + 50, h - 301);
35	      // 区域检查:避开雪/冰/丛林/花岗岩/大理石与已放蘑菇(原版 100/500 距离)
36	      let bad = false;
37	      for (let x = i - 100; x < i + 100 && !bad; x += 3) {
38	        for (let y = j - 100; y < j + 100; y += 3) {
39	          if (!st.inBounds(x, y)) { bad = true; break; }
40	          const t = st.type[st.idx(x, y)];
41	          if (t === SNOW || t === ICE || t === THIN_ICE || t === JUNGLE_GRASS || t === GRANITE || t === MARBLE) { bad = true; break; }
42	          // 原版:落在地下沙漠范围内也重掷(cs L5673)
43	          if (gs.undergroundDesert && x >= gs.undergroundDesert.x0 && x <= gs.undergroundDesert.x1
44	            && y >= gs.undergroundDesert.y0 && y <= gs.undergroundDesert.y1) { bad = true; break; }
45	        }
46	      }
47	      if (!bad) {
48	        for (const [px, py] of placed) {
49	          if (Math.hypot(px - i, py - j) < 500) { bad = true; break; }
50	        }
51	      }
52	      if (!bad && placed.length < maxBiomes) {
53	        shroomPatch(st, rng, gs, i, j, van);
54	        for (let k = 0; k < 5; k++) shroomPatch(st, rng, gs, i + rng.int(-40, 40), j + rng.int(-40, 40), van);
55	        placed.push([i, j]);
56	        break;
57	      }
58	      attempts++;
59	    }
60	  }
61	  // 泥→蘑菇草传播
62	  spreadGrassAll(st, MUD, MUSH_GRASS);
63	}
64	
65	/** ShroomPatch(WorldGen.cs:48648)1:1:泥 blob 随机走,中心上空挖空,墙→80,尾端泥 runner */
66	function shroomPatch(st: TileStore, rng: RNG, gs: GenState, i: number, j: number, van: number): void {
67	  let stepsLeft = rng.int(80, 99);
68	  let radius = rng.int(20, 25) * van;
69	  const startR = radius;
70	  let px = i + 0.0, py = j - radius * 0.3;
71	  let vx = rng.int(-100, 100) * 0.005;
72	  let vy = rng.int(-200, -101) * 0.005;
73	  while (stepsLeft > 0 && radius > 0) {
74	    stepsLeft -= rng.int(0, 2);
75	    radius--;
76	    const x0 = Math.max(0, Math.floor(px - stepsLeft * 0.5));
77	    const x1 = Math.min(st.w, Math.floor(px + stepsLeft * 0.5));
78	    const y0 = Math.max(0, Math.floor(py - stepsLeft * 0.5));
79	    const y1 = Math.min(st.h, Math.floor(py + stepsLeft * 0.5));
80	    const r = stepsLeft * rng.int(80, 119) * 0.01;
81	    for (let x = x0; x < x1; x++) {
82	      for (let y = y0; y < y1; y++) {
83	        const d = Math.hypot(x - px, (y - py) * 2.3);
84	        const ti = st.idx(x, y);
85	        if (d < r * 0.8 && st.liquidType[ti] === 2) st.liquid[ti] = 0;
86	        if (d < r * 0.2 && y < py) {
87	          st.type[ti] = 0; st.flags[ti] = 0;
88	          if (st.wall[ti] > 0) st.wall[ti] = 80;
89	        } else if (d < r * 0.4 * (0.95 + rng.next() * 0.1)) {
90	          st.type[ti] = MUD;
91	          if (radius === startR && y > py) st.flags[ti] = 1;
92	          if (st.wall[ti] > 0) st.wall[ti] = 80;
93	        }
94	      }
95	    }
96	    px += vx; py += vy;
97	    px += vx;
98	    vx += rng.int(-100, 109) * 0.005;
99	    vy -= rng.int(0, 109) * 0.005;
100	    if (vx > -0.5 && vx < 0.5) vx = vx >= 0 ? 0.5 : -0.5;
101	    vx = Math.max(-0.5, Math.min(0.5, vx));
102	    vy = Math.max(-0.5, Math.min(0.5, vy));
103	    // 尾端两支向下泥 runner(cs L48722-48729:落点无界重掷)
104	    for (let k = 0; k < 2; k++) {
105	      let i1 = Math.floor(px) + rng.int(-20, 19);
106	      let j1 = Math.floor(py) + rng.int(0, 19);
107	      let found = false;
108	      while (!found) {
109	        if (!st.inBounds(i1, j1)) { found = true; break; }  // 越界保护,跳过本支
110	        if (st.flags[st.idx(i1, j1)] || st.type[st.idx(i1, j1)] === MUD) { found = true; break; }
111	        i1 = Math.floor(px) + rng.int(-20, 19);
112	        j1 = Math.floor(py) + rng.int(0, 19);
113	      }
114	      if (!st.inBounds(i1, j1)) continue;
115	      tileRunner(st, rng, gs, i1, j1, { strength: rng.int(10, 19), steps: rng.int(10, 19), type: MUD, speedY: 2, noYChange: true });
116	    }
117	  }
118	}
119	

```


---

## 🤖 Assistant · 2026-08-11T04:09:59.807Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
GrassPass: line 26-27: `y2 = rng.int(0, Math.max(1, gs.worldSurfaceLow - 1))` — seeds above surface ("地表上方"), but the seed function requires all 4 neighbors to be active DIRT — in sky, no dirt → no-op. Only converts existing dirt to grass, no sky blocks. Vanilla comment says "地表上方各随机点" — matches vanilla.

ShroomPatch: `st.type[ti] = MUD` (line 90) — sets type WITHOUT flags (except first iteration where radius===startR && y>py sets flags=1)! This is a ghost-type writer — but deep underground (j = rockLevel+50..h-301). Note this matches vanilla (inactive mud). Not sky.

Now remaining: CorruptionPass (645 lines), IslandHousePass, TrapsPass, HellFortPass, HiveSpiderPass, TemplePass, DungeonPass, Spread. Let me grep for their y-ranges and sky writes. I'll grep for "worldSurface" usage and setTileSilent in those files to find y-bound logic quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:00.410Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla && grep -n \"worldSurface\\|rng.int(0\\|addTile\" CorruptionPass.ts | head -60",
 "description": "Grep CorruptionPass for y ranges"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:00.445Z

**📎 ToolResult**

```
36:    for (let y = 0; y < gs.worldSurface; y++) {
62:      zLo = cx - rng.int(0, 199) - 100;
63:      zHi = cx + rng.int(0, 199) + 100;
81:      crimStart(st, rng, gs, cx, gs.worldSurfaceLow - 10);
93:        for (let y = gs.worldSurfaceLow; y < gs.worldSurface - 1; y++) {
97:              chasmRunner(st, rng, gs, x, y, rng.int(0, 149) + 150, true);
98:            } else if (rng.int(0, 34) === 0) {
100:              chasmRunner(st, rng, gs, x, y, rng.int(0, 49) + 50, true);
117:    for (let y = gs.worldSurfaceLow; y < gs.worldSurface - 1; y++) {
122:        if ((t === MUD || t === JUNGLE_GRASS) && x >= zLo + rng.int(0, 4) && x < zHi - rng.int(0, 4)) {
130:  let bandY = gs.worldSurface + 40;
133:    if (bandY < gs.worldSurface + 30) bandY = gs.worldSurface + 30;
134:    if (bandY > gs.worldSurface + 50) bandY = gs.worldSurface + 50;
136:    for (let y = gs.worldSurfaceLow; y < bandY; y++) {
140:      const inCore = x >= zLo + rng.int(0, 4) && x <= zHi - rng.int(0, 4);
142:      if (t === T.DIRT && y < gs.worldSurface - 1 && first) {
167:      // 原版 y 带(cs L6243-6244):worldSurface-widen/2 .. worldSurface+100+widen
168:      let y = rng.int(Math.max(2, Math.floor(gs.worldSurface - widen / 2)), Math.floor(gs.worldSurface + 100 + widen) - 1);
174:        while (st.flags[st.idx(x, y)] && y > gs.worldSurface) y--;
235:  let vy = rng.int(0, 10) * 0.2 + 0.5;
236:  let radius = rng.int(0, 4) + 7;
239:      radius += rng.int(0, 2) - rng.int(0, 2);
243:    } else if (py > gs.worldSurface + 45) {
244:      radius -= rng.int(0, 3);
248:    if (!sideways && py > gs.worldSurface + 20) {
267:    if (num1 <= 2 && py < gs.worldSurface + 45) num1 = 2;
280:          if (y > gs.worldSurface) {
331:  let radius = rng.int(0, 4) + 7;
334:      radius += rng.int(0, 2) - rng.int(0, 2);
338:    } else radius -= rng.int(0, 3);
354:    if (py < j - 20) vy += rng.int(0, 19) * 0.01;
355:    if (py > j + 20) vy -= rng.int(0, 19) * 0.01;
386:  if (rng.int(0, 2) !== 0) return;
403:  const entryX = i, entryY0 = Math.min(j, gs.worldSurface);
445:    if (py > gs.worldSurface + 100) break;
478:      vy2 = rng.int(0, 20) * 0.15;
488:  let rise = rng.int(0, 5);
634:          if (Math.abs(dx) + Math.abs(dy) < 9 + rng.int(0, 10) && rng.int(0, 2) !== 0 && st.type[ti] !== ORB) {
638:          if (st.type[ti] !== ORB && Math.abs(dx) <= 2 + rng.int(0, 2) && Math.abs(dy) <= 2 + rng.int(0, 2)) {

```


---

## 🤖 Assistant · 2026-08-11T04:10:00.564Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IslandHousePass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:00.574Z

**📎 ToolResult**

```
1	// 原版 "Floating Island Houses" pass(L8463 + IslandHouse L48185)移植。
2	// 日光板 202 外壳 + Disc Wall 82 室内 + Skyware 门(tile10 style9)+ 天空宝箱(chest,style13 近似帧0)
3	// + 桌椅横幅。对 gs.floatingIslands 每个非湖岛建房。
4	import type { TileStore } from '../../TileStore';
5	import type { RNG } from '../../../core/rng';
6	import type { GenState } from './GenState';
7	import { T, TILE_BY_KEY } from '../../../data/tiles';
8	import { ITEM_BY_KEY } from '../../../data/items';
9	import { placeDoorClosed } from '../../Door';
10	import { placeFurn, flipFurn } from './DungeonPass';
11	
12	const SUNPLATE = TILE_BY_KEY['v_202_sunplate_block']!;
13	const CHEST = TILE_BY_KEY['chest']!;
14	const TABLE = TILE_BY_KEY['table']!;
15	const CHAIR = TILE_BY_KEY['chair']!;
16	const BANNER = TILE_BY_KEY['v_91_banners']!;
17	
18	export function runIslandHousePass(
19	  st: TileStore, rng: RNG, gs: GenState,
20	  chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null> }>,
21	): void {
22	  let houseCount = 0;
23	  for (const isl of gs.floatingIslands) {
24	    if (isl.isLake) continue;
25	    islandHouse(st, rng, isl.x, isl.y, chests, houseCount);
26	    houseCount++;
27	  }
28	}
29	
30	function islandHouse(
31	  st: TileStore, rng: RNG, i: number, j: number,
32	  chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null> }>,
33	  houseIdx: number,
34	): void {
35	  const dir = rng.next() < 0.5 ? -1 : 1;
36	  const halfW = rng.int(7, 11);
37	  const hgt = rng.int(5, 6);
38	  // 找地板(cs L48195-48203):门口侧探测列首个实心行的上一格;找不到保持 j
39	  let floorY = j;
40	  const probeX = i + (halfW + 2) * dir;
41	  for (let y = j - 15; y < j + 30; y++) {
42	    if (st.inBounds(probeX, y) && st.flags[st.idx(probeX, y)]) { floorY = y - 1; break; }
43	  }
44	  // 外壳(cs L48217-48231):整块实心日光板+清墙,仅顶行两角跳过
45	  for (let x = i - halfW - 1; x <= i + halfW + 1; x++) {
46	    for (let y = floorY - hgt - 2; y <= floorY + 3; y++) {
47	      if (y === floorY - hgt - 2 && (x === i - halfW - 1 || x === i + halfW + 1)) continue;
48	      if (!st.inBounds(x, y)) continue;
49	      const idx = st.idx(x, y);
50	      st.type[idx] = SUNPLATE; st.flags[idx] = 1; st.liquid[idx] = 0; st.liquidType[idx] = 0;
51	      st.wall[idx] = 0;
52	    }
53	  }
54	  // 内部挖空 + Disc Wall 82(cs L48244-48254):仅原墙为 0 处,跳过顶行两角
55	  const j1 = floorY - hgt, j2 = floorY + 1;
56	  for (let x = i - halfW; x <= i + halfW; x++) {
57	    for (let y = j1; y <= j2; y++) {
58	      if (y === j1 && (x === i - halfW || x === i + halfW)) continue;
59	      if (!st.inBounds(x, y)) continue;
60	      const idx = st.idx(x, y);
61	      if (st.wall[idx] === 0) {
62	        st.type[idx] = 0; st.flags[idx] = 0;
63	        st.wall[idx] = 82;
64	      }
65	    }
66	  }
67	  // 门(Skyware style9;5×3 门洞,cs L48255-48263)
68	  const doorX = i + (halfW + 1) * dir;
69	  for (let dx = -2; dx <= 2; dx++) {
70	    for (let dy = -2; dy <= 0; dy++) {
71	      if (!st.inBounds(doorX + dx, floorY + dy)) continue;
72	      const idx = st.idx(doorX + dx, floorY + dy);
73	      st.type[idx] = 0; st.flags[idx] = 0;
74	    }
75	  }
76	  // 原版 L48263 PlaceTile(i1, y) → 门顶在 y-2（占 y-2..y，门洞已清 y-2..y）
77	  if (st.inBounds(doorX, floorY - 2)) placeDoorClosed(st, doorX, floorY - 2, 9);
78	  // 对侧补柱(cs L48264-48273)
79	  const pillarX = i + (halfW + 1) * -dir - dir;
80	  for (let y = j1; y <= j2 + 1; y++) {
81	    if (!st.inBounds(pillarX, y)) continue;
82	    const idx = st.idx(pillarX, y);
83	    st.type[idx] = SUNPLATE; st.flags[idx] = 1; st.wall[idx] = 0;
84	  }
85	  // 天空宝箱(cs L48274-48293):style13 Skyware(战利品序 0=气球/1=星怒/2=马蹄铁,第 3 间起随机)
86	  let loot = houseIdx;
87	  if (loot > 2) loot = rng.int(0, 2);
88	  const lootKeys = ['vi_159_shiny_red_balloon', 'vi_65_starfury', 'vi_158_lucky_horseshoe'];
89	  const lootId = ITEM_BY_KEY[lootKeys[loot]] ?? ITEM_BY_KEY[lootKeys[0]];
90	  const bx = i, by = floorY - 1;
91	  // PlaceChestDirect 语义:frameX = 36*style + dx*18,顶行 frameY=0
92	  st.setTileSilent(bx, by, CHEST, 13 * 36, 0);
93	  st.setTileSilent(bx + 1, by, CHEST, 13 * 36 + 18, 0);
94	  st.setTileSilent(bx, by + 1, CHEST, 13 * 36, 18);
95	  st.setTileSilent(bx + 1, by + 1, CHEST, 13 * 36 + 18, 18);
96	  chests.push({ x: bx, y: by, items: [{ id: lootId, stack: 1 }, ...Array(9).fill(null)] });
97	  // 窗(Glass Wall 21,cs L48312-48327):halfW>10 → ±2 宽,否则 ±1;
98	  // 中心 x = i∓halfW/2±1,y = (j1+j2)/2 - 1 ± 1
99	  const winHalf = halfW > 10 ? 2 : 1;
100	  const winY = Math.floor((j1 + j2) / 2) - 1;
101	  for (const wx of [i - Math.floor(halfW / 2) + 1, i + Math.floor(halfW / 2) - 1]) {
102	    for (let dx = -winHalf; dx <= winHalf; dx++) {
103	      for (let dy = -1; dy <= 1; dy++) {
104	        if (!st.inBounds(wx + dx, winY + dy)) continue;
105	        st.wall[st.idx(wx + dx, winY + dy)] = 21;
106	      }
107	    }
108	  }
109	  // 桌+两椅(cs L48328-48333):桌 style7(步长 54),椅 style10(左椅翻转 +18)——
110	  // 此前是单格残件 + 错误步长(桌 36/旗 36),现为完整多格放置
111	  const tableX = i + (Math.floor(halfW / 2) + 1) * -dir;
112	  if (placeFurn(st, tableX, j2, TABLE, 7)) {
113	    if (placeFurn(st, tableX - 2, j2, CHAIR, 10)) flipFurn(st, tableX - 2, j2, CHAIR);
114	    placeFurn(st, tableX + 2, j2, CHAIR, 10);
115	  }
116	  // 横幅(cs L48334-48348):1×3 顶锚,style 7-9(步长 18)
117	  for (const bx2 of [i - halfW + 1, i + halfW - 1]) {
118	    placeFurn(st, bx2, j1, BANNER, rng.int(7, 9), 'top');
119	  }
120	  const bannerX = dir > 0 ? i - halfW : i + halfW;
121	  placeFurn(st, bannerX, j1 + 1, BANNER, rng.int(7, 9), 'top');
122	}
123	
124	void T;
125	

```


---

## 🤖 Assistant · 2026-08-11T04:10:03.072Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
IslandHousePass writes real sunplate blocks in the sky (on floating islands). Intended.

CorruptionPass line 81: `crimStart(st, rng, gs, cx, gs.worldSurfaceLow - 10)` — starts 10 above surfaceLow. Line 168: y band `worldSurface - widen/2 .. worldSurface + 100 + widen` — above surface! Let me read the relevant section of CorruptionPass (lines 1-200 and 220-300, 380-500) to check sky writes.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:03.265Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts",
 "limit": 300
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:03.280Z

**📎 ToolResult**

```
1	// 原版 pass 28 "Corruption"(WorldGen.cs:6059)移植。
2	// 腐化:ChasmRunner 裂隙(黑檀石 25 壳 + 暗影之球 31 style0 + 恶魔祭坛 26 style0);
3	// 猩红:CrimStart 弹坑隧道(猩红石 203 墙 83 + 恶魔之心 31 style1 + 祭坛 style1)。
4	// 区域避开:出生点±200、地下沙漠、地牢±100、丛林/雪原带(±10 收缩)。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T, TILE_BY_KEY } from '../../../data/tiles';
9	
10	const EBONSTONE = TILE_BY_KEY['v_25_ebonstone_block']!;
11	const CORRUPT_GRASS = TILE_BY_KEY['v_23_corrupt_grass_block']!;
12	const EBONSAND = TILE_BY_KEY['v_112_ebonsand_block']!;
13	const CRIMSTONE = TILE_BY_KEY['v_203_crimstone_block']!;
14	const CRIMSON_GRASS = TILE_BY_KEY['v_199_crimson_grass_block']!;
15	const CRIMSAND = TILE_BY_KEY['v_234_crimsand_block']!;
16	const CORRUPT_HARDSAND = TILE_BY_KEY['v_398_corrupt_hardened_sand_block']!;
17	const SNOW_BRICK = TILE_BY_KEY['ice']!;   // sheet 161=Ice Block（旧 key v_161_snow_brick 误名）
18	const CORRUPT_ICE = TILE_BY_KEY['v_163_purple_ice_block']!;   // 163=Purple Ice
19	const CRIMSON_ICE = TILE_BY_KEY['v_200_red_ice_block']!;   // 200=Red Ice
20	const CRIMSON_HARDSAND = TILE_BY_KEY['v_399_crimson_hardened_sand_block']!;
21	const ICE = TILE_BY_KEY['ice']!;
22	const MUD = TILE_BY_KEY['mud']!;
23	const JUNGLE_GRASS = TILE_BY_KEY['v_60_jungle_grass_block']!;
24	const SNOW = TILE_BY_KEY['snow']!;
25	const ALTAR = TILE_BY_KEY['v_26_altars']!;
26	const ORB = TILE_BY_KEY['v_31_orb_heart']!;
27	const SANDSTONE = TILE_BY_KEY['sandstone']!;
28	const HARDSAND = TILE_BY_KEY['hardened_sand']!;
29	
30	export function runCorruptionPass(st: TileStore, rng: RNG, gs: GenState): void {
31	  const { w, h } = st;
32	  const van = w / 4200;
33	  // 丛林/雪原横向范围(±10 回避)
34	  let jMin = w, jMax = 0, sMin = w, sMax = 0;
35	  for (let x = 0; x < w; x++) {
36	    for (let y = 0; y < gs.worldSurface; y++) {
37	      if (!st.flags[st.idx(x, y)]) continue;
38	      const t = st.type[st.idx(x, y)];
39	      if (t === JUNGLE_GRASS) { jMin = Math.min(jMin, x); jMax = Math.max(jMax, x); }
40	      else if (t === SNOW || t === ICE) { sMin = Math.min(sMin, x); sMax = Math.max(sMax, x); }
41	    }
42	  }
43	  const avoid = 10;
44	  const jLo = jMin - avoid, jHi = jMax + avoid, sLo = sMin - avoid, sHi = sMax + avoid;
45	  // 原版全部为固定常数(cs:4720-4731/6092-6095):beachAvoidance=275+5+40+60=380、
46	  // minCenter=500、中央回避=200、地牢回避=100、midFixer=50
47	  const beachAvoid = 380;
48	  const minCenter = 500;
49	  const midAvoid = 200;
50	  const dungeonAvoid = 100;
51	  const midFixer = 50;
52	  const groups = Math.max(1, Math.floor(w * 0.00045));
53	
54	  for (let g = 0; g < groups; g++) {
55	    let jnLo = jLo, jnHi = jHi, snLo = sLo, snHi = sHi;
56	    let cx = 0, zLo = 0, zHi = 0;
57	    // 拒绝采样区域
58	    let ok = false;
59	    for (let attempt = 0; attempt < 4000 && !ok; attempt++) {
60	      ok = true;
61	      cx = rng.int(minCenter, w - 1 - minCenter);
62	      zLo = cx - rng.int(0, 199) - 100;
63	      zHi = cx + rng.int(0, 199) + 100;
64	      if (zLo < beachAvoid) zLo = beachAvoid;
65	      if (zHi > w - beachAvoid) zHi = w - beachAvoid;
66	      if (cx < zLo + midFixer) cx = zLo + midFixer;
67	      if (cx > zHi - midFixer) cx = zHi - midFixer;
68	      if (gs.dungeonSide < 0 && zLo < 400) zLo = 400;
69	      else if (gs.dungeonSide > 0 && zLo > w - 400) zLo = w - 400;
70	      const mid = w / 2;
71	      if (Math.abs(cx - mid) < midAvoid || Math.abs(zLo - mid) < midAvoid || Math.abs(zHi - mid) < midAvoid) ok = false;
72	      const ud = gs.undergroundDesert;
73	      if (ud && ((cx > ud.x0 && cx < ud.x1) || (zLo > ud.x0 && zLo < ud.x1) || (zHi > ud.x0 && zHi < ud.x1))) ok = false;
74	      if (zLo < gs.dungeonLocation + dungeonAvoid && zHi > gs.dungeonLocation - dungeonAvoid) ok = false;
75	      if (zLo < jnHi && zHi > jnLo) { jnLo++; jnHi--; ok = false; }
76	      if (zLo < snHi && zHi > snLo) { snLo++; snHi--; ok = false; }
77	    }
78	    gs.evilZones.push({ x0: zLo, x1: zHi });
79	
80	    if (gs.crimson) {
81	      crimStart(st, rng, gs, cx, gs.worldSurfaceLow - 10);
82	      // 地表转换:猩红石/猩红草/猩红沙 + 墙 216→218、187→221;丛林泥/草清除
83	      convertSurface(st, rng, gs, zLo, zHi, true);
84	      // 祭坛 10-14 个(v_26 style 1)
85	      placeAltars(st, rng, gs, zLo, zHi, 1, CRIMSTONE);
86	    } else {
87	      // 腐化裂隙:主裂隙(cx, 150-300 步) + 35 分之一支裂隙(50-100 步带球)
88	      let cooldown = 0;
89	      for (let x = zLo; x < zHi; x++) {
90	        if (cooldown > 0) cooldown--;
91	        if (x !== cx && cooldown !== 0) continue;
92	        let sy = -1;
93	        for (let y = gs.worldSurfaceLow; y < gs.worldSurface - 1; y++) {
94	          if (st.flags[st.idx(x, y)] || st.wall[st.idx(x, y)] > 0) {
95	            if (x === cx) {
96	              cooldown = 20;
97	              chasmRunner(st, rng, gs, x, y, rng.int(0, 149) + 150, true);
98	            } else if (rng.int(0, 34) === 0) {
99	              cooldown = 30;
100	              chasmRunner(st, rng, gs, x, y, rng.int(0, 49) + 50, true);
101	            }
102	            break;
103	          }
104	        }
105	      }
106	      convertSurface(st, rng, gs, zLo, zHi, false);
107	      // 暗影之球周的黑檀石囊清理(原版 6416-6446)
108	      cleanOrbPockets(st, rng);
109	    }
110	  }
111	}
112	
113	/** 地表转换(腐化/猩红通用):L6195-6232 / L6388-6414 */
114	function convertSurface(st: TileStore, rng: RNG, gs: GenState, zLo: number, zHi: number, crimson: boolean): void {
115	  // 丛林泥/草清除(地表 10-14 格深)
116	  for (let x = zLo; x < zHi; x++) {
117	    for (let y = gs.worldSurfaceLow; y < gs.worldSurface - 1; y++) {
118	      if (!st.flags[st.idx(x, y)]) continue;
119	      const depth = y + rng.int(10, 13);
120	      for (let y2 = y; y2 < depth; y2++) {
121	        const t = st.type[st.idx(x, y2)];
122	        if ((t === MUD || t === JUNGLE_GRASS) && x >= zLo + rng.int(0, 4) && x < zHi - rng.int(0, 4)) {
123	          st.type[st.idx(x, y2)] = 0;
124	        }
125	      }
126	      break;
127	    }
128	  }
129	  // 深度游走转换带
130	  let bandY = gs.worldSurface + 40;
131	  for (let x = zLo; x < zHi; x++) {
132	    bandY += rng.int(-2, 2);
133	    if (bandY < gs.worldSurface + 30) bandY = gs.worldSurface + 30;
134	    if (bandY > gs.worldSurface + 50) bandY = gs.worldSurface + 50;
135	    let first = true;
136	    for (let y = gs.worldSurfaceLow; y < bandY; y++) {
137	      const i = st.idx(x, y);
138	      if (!st.flags[i]) continue;
139	      const t = st.type[i];
140	      const inCore = x >= zLo + rng.int(0, 4) && x <= zHi - rng.int(0, 4);
141	      if (t === T.SAND && inCore) st.type[i] = crimson ? CRIMSAND : EBONSAND;
142	      if (t === T.DIRT && y < gs.worldSurface - 1 && first) {
143	        // 暴露泥土 → 邪恶草(原版 SpreadGrass(0→23/199))
144	        st.type[i] = crimson ? CRIMSON_GRASS : CORRUPT_GRASS;
145	      }
146	      first = false;
147	      if (st.wall[i] === 216) st.wall[i] = crimson ? 218 : 217;
148	      else if (st.wall[i] === 187) st.wall[i] = crimson ? 221 : 220;
149	      if (t === T.STONE) {
150	        if (inCore) st.type[i] = crimson ? CRIMSTONE : EBONSTONE;
151	      } else if (t === T.GRASS) st.type[i] = crimson ? CRIMSON_GRASS : CORRUPT_GRASS;
152	      else if (t === SNOW_BRICK) st.type[i] = crimson ? CRIMSON_ICE : CORRUPT_ICE; // 原版 161→163/200(cs L6397)
153	      else if (t === SANDSTONE) { /* 腐化沙岩 v_400/v_401 暂缺 */ }
154	      else if (t === HARDSAND) st.type[i] = crimson ? CRIMSON_HARDSAND : CORRUPT_HARDSAND;
155	    }
156	  }
157	}
158	
159	/** 恶魔祭坛:10-14 个,落在邪恶石地表上(Place3x2) */
160	function placeAltars(st: TileStore, rng: RNG, gs: GenState, zLo: number, zHi: number, style: number, stoneType: number): void {
161	  const count = rng.int(10, 14);
162	  for (let n = 0; n < count; n++) {
163	    let widen = 0, tries = 0, done = false;
164	    while (!done) {
165	      tries++;
166	      let x = rng.int(zLo - widen, zHi - 1 + widen);
167	      // 原版 y 带(cs L6243-6244):worldSurface-widen/2 .. worldSurface+100+widen
168	      let y = rng.int(Math.max(2, Math.floor(gs.worldSurface - widen / 2)), Math.floor(gs.worldSurface + 100 + widen) - 1);
169	      if (x < 2) x = 2; if (x > st.w - 3) x = st.w - 3;
170	      if (!st.flags[st.idx(x, y)]) {
171	        while (!st.flags[st.idx(x, y)] && y < st.h - 2) y++;
172	        y--;
173	      } else {
174	        while (st.flags[st.idx(x, y)] && y > gs.worldSurface) y--;
175	      }
176	      if ((widen > 10 || (st.flags[st.idx(x, y + 1)] && st.type[st.idx(x, y + 1)] === stoneType)) && !isTileNearby(st, x, y, ALTAR, 3)) {
177	        place3x2(st, x, y, ALTAR, style);
178	        if (st.type[st.idx(x, y)] === ALTAR) done = true;
179	      }
180	      if (tries > 100) { widen++; tries = 0; }
181	      if (widen > 100) done = true;
182	    }
183	  }
184	}
185	
186	function isTileNearby(st: TileStore, x: number, y: number, type: number, radius: number): boolean {
187	  for (let dx = -radius; dx <= radius; dx++) {
188	    for (let dy = -radius; dy <= radius; dy++) {
189	      if (!st.inBounds(x + dx, y + dy)) continue;
190	      if (st.type[st.idx(x + dx, y + dy)] === type) return true;
191	    }
192	  }
193	  return false;
194	}
195	
196	/** 3×2 物件放置(锚点=中下):帧 style*54 + col*18 / row*18 */
197	function place3x2(st: TileStore, x: number, y: number, type: number, style: number): void {
198	  if (x < 5 || x > st.w - 5 || y < 5 || y > st.h - 5) return;
199	  for (let dx = -1; dx <= 1; dx++) {
200	    if (!st.isSolid(x + dx, y + 1)) return; // 底座须实心
201	  }
202	  for (let dx = -1; dx <= 1; dx++) {
203	    for (let dy = -1; dy <= 0; dy++) {
204	      if (st.flags[st.idx(x + dx, y + dy)]) return; // 区域须净空
205	    }
206	  }
207	  for (let dx = -1; dx <= 1; dx++) {
208	    for (let dy = -1; dy <= 0; dy++) {
209	      st.setTileSilent(x + dx, y + dy, type, style * 54 + (dx + 1) * 18, (dy + 1) * 18);
210	    }
211	  }
212	}
213	
214	/** 暗影之球(AddShadowOrb L16035):2×2,猩红 style 偏移 +36 */
215	function addShadowOrb(st: TileStore, x: number, y: number, crimson: boolean): void {
216	  if (x < 10 || x > st.w - 10 || y < 10 || y > st.h - 10) return;
217	  for (let dx = -1; dx < 1; dx++) {
218	    for (let dy = -1; dy < 1; dy++) {
219	      if (st.flags[st.idx(x + dx, y + dy)] && st.type[st.idx(x + dx, y + dy)] === ORB) return;
220	    }
221	  }
222	  const fx = crimson ? 36 : 0;
223	  st.setTileSilent(x - 1, y - 1, ORB, fx, 0);
224	  st.setTileSilent(x, y - 1, ORB, 18 + fx, 0);
225	  st.setTileSilent(x - 1, y, ORB, fx, 18);
226	  st.setTileSilent(x, y, ORB, 18 + fx, 18);
227	}
228	
229	/** ChasmRunner(L45779)1:1:竖直裂隙,黑檀石壳 + 球/祭坛收尾 */
230	function chasmRunner(st: TileStore, rng: RNG, gs: GenState, i: number, j: number, steps: number, makeOrb: boolean): void {
231	  let sideways = false, orbPlaced = !makeOrb, altarPlaced = false;
232	  let num1 = steps;
233	  let px = i + 0.0, py = j + 0.0;
234	  let vx = rng.int(-10, 10) * 0.1;
235	  let vy = rng.int(0, 10) * 0.2 + 0.5;
236	  let radius = rng.int(0, 4) + 7;
237	  while (radius > 0) {
238	    if (num1 > 0) {
239	      radius += rng.int(0, 2) - rng.int(0, 2);
240	      if (radius < 7) radius = 7;
241	      if (radius > 20) radius = 20;
242	      if (num1 === 1 && radius < 10) radius = 10;
243	    } else if (py > gs.worldSurface + 45) {
244	      radius -= rng.int(0, 3);
245	    }
246	    if (py > gs.rockLevel && num1 > 0) num1 = 0;
247	    num1--;
248	    if (!sideways && py > gs.worldSurface + 20) {
249	      sideways = true;
250	      chasmRunnerSideways(st, rng, gs, Math.floor(px), Math.floor(py), -1, rng.int(20, 39));
251	      chasmRunnerSideways(st, rng, gs, Math.floor(px), Math.floor(py), 1, rng.int(20, 39));
252	    }
253	    // 挖空(中心)
254	    if (num1 > 5) {
255	      const x0 = Math.max(0, Math.floor(px - radius * 0.5)), x1 = Math.min(st.w - 1, Math.floor(px + radius * 0.5));
256	      const y0 = Math.max(0, Math.floor(py - radius * 0.5)), y1 = Math.min(st.h, Math.floor(py + radius * 0.5));
257	      for (let x = x0; x < x1; x++) {
258	        for (let y = y0; y < y1; y++) {
259	          const ti = st.idx(x, y);
260	          if (Math.abs(x - px) + Math.abs(y - py) < radius * 0.5 * (1 + rng.int(-10, 10) * 0.015)
261	            && st.type[ti] !== ORB) {
262	            st.flags[ti] = 0; // 只清 active 保留 type(原版 KillTile)——壳层才不会回填隧道
263	          }
264	        }
265	      }
266	    }
267	    if (num1 <= 2 && py < gs.worldSurface + 45) num1 = 2;
268	    if (num1 <= 0) {
269	      if (!orbPlaced) {
270	        orbPlaced = true;
271	        addShadowOrb(st, Math.floor(px), Math.floor(py), false);
272	      } else if (!altarPlaced) {
273	        altarPlaced = true;
274	        let tries = 0, done = false;
275	        while (!done) {
276	          let x = rng.int(Math.floor(px) - 25, Math.floor(px) + 24);
277	          let y = rng.int(Math.floor(py) - 50, Math.floor(py) - 1);
278	          x = Math.max(5, Math.min(st.w - 5, x));
279	          y = Math.max(5, Math.min(st.h - 5, y));
280	          if (y > gs.worldSurface) {
281	            // 落点吸附(原版):空气则落到地面,实心则升到表面
282	            if (!st.flags[st.idx(x, y)]) {
283	              while (!st.flags[st.idx(x, y)] && y < st.h - 2) y++;
284	              y--;
285	            } else {
286	              while (st.flags[st.idx(x, y)] && y > 4) y--;
287	            }
288	            if (!isTileNearby(st, x, y, ALTAR, 3)) place3x2(st, x, y, ALTAR, 0);
289	            if (st.type[st.idx(x, y)] === ALTAR) done = true;
290	            else if (++tries >= 10000) done = true;
291	          } else if (++tries >= 10000) done = true; // 原版此处直接放弃;小世界采样带浅,改为重试
292	        }
293	      }
294	    }
295	    px += vx; py += vy;
296	    vx += rng.int(-10, 10) * 0.01;
297	    vx = Math.max(-0.3, Math.min(0.3, vx));
298	    // 黑檀石壳(外圈 1.1×)
299	    const x0 = Math.max(1, Math.floor(px - radius * 1.1)), x1 = Math.min(st.w - 1, Math.floor(px + radius * 1.1));
300	    const y0 = Math.max(0, Math.floor(py - radius * 1.1)), y1 = Math.min(st.h, Math.floor(py + radius * 1.1));

```


---

## 🤖 Assistant · 2026-08-11T04:10:05.795Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important detail at line 262: `st.flags[ti] = 0; // 只清 active 保留 type(原版 KillTile)` — this creates GHOST types (type preserved, flags cleared)! These ghosts are later purged by finalize. But that's underground (chasm).

Corruption chasm runner starts at y between worldSurfaceLow and worldSurface-1 (below surface), digs down. CrimStart starts at worldSurfaceLow - 10 → possibly slightly above surface. Let me check crimStart (line 300-400).
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:06.016Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts",
 "offset": 300,
 "limit": 200
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:06.027Z

**📎 ToolResult**

```
300	    const y0 = Math.max(0, Math.floor(py - radius * 1.1)), y1 = Math.min(st.h, Math.floor(py + radius * 1.1));
301	    for (let x = x0; x < x1; x++) {
302	      for (let y = y0; y < y1; y++) {
303	        const ti = st.idx(x, y);
304	        if (Math.abs(x - px) + Math.abs(y - py) < radius * 1.1 * (1 + rng.int(-10, 10) * 0.015)) {
305	          if (st.type[ti] !== EBONSTONE && y > j + rng.int(3, 19)) st.flags[ti] = 1;
306	          if (steps <= 5) st.flags[ti] = 1;
307	          if (st.type[ti] !== ORB) st.type[ti] = EBONSTONE;
308	        }
309	      }
310	    }
311	    for (let x = x0; x < x1; x++) {
312	      for (let y = y0; y < y1; y++) {
313	        const ti = st.idx(x, y);
314	        if (Math.abs(x - px) + Math.abs(y - py) < radius * 1.1 * (1 + rng.int(-10, 10) * 0.015)) {
315	          if (st.type[ti] !== ORB) st.type[ti] = EBONSTONE;
316	          if (steps <= 5) st.flags[ti] = 1;
317	          if (y > j + rng.int(3, 19)) st.wall[ti] = 3;
318	        }
319	      }
320	    }
321	  }
322	}
323	
324	/** ChasmRunnerSideways(L45313)1:1:水平裂隙 */
325	function chasmRunnerSideways(st: TileStore, rng: RNG, gs: GenState, i: number, j: number, direction: number, steps: number): void {
326	  let num1 = steps;
327	  let px = i + 0.0, py = j + 0.0;
328	  let vx = rng.int(10, 20) * 0.1 * direction;
329	  // 原版初速 vy = Next(-10,10)*0.01 = -0.10..-0.01(恒向下,cs L45321)
330	  let vy = rng.int(-10, -1) * 0.01;
331	  let radius = rng.int(0, 4) + 7;
332	  while (radius > 0) {
333	    if (num1 > 0) {
334	      radius += rng.int(0, 2) - rng.int(0, 2);
335	      if (radius < 7) radius = 7;
336	      if (radius > 20) radius = 20;
337	      if (num1 === 1 && radius < 10) radius = 10;
338	    } else radius -= rng.int(0, 3);
339	    if (py > gs.rockLevel && num1 > 0) num1 = 0;
340	    num1--;
341	    const x0 = Math.max(0, Math.floor(px - radius * 0.5)), x1 = Math.min(st.w - 1, Math.floor(px + radius * 0.5));
342	    const y0 = Math.max(0, Math.floor(py - radius * 0.5)), y1 = Math.min(st.h, Math.floor(py + radius * 0.5));
343	    for (let x = x0; x < x1; x++) {
344	      for (let y = y0; y < y1; y++) {
345	        const ti = st.idx(x, y);
346	        if (Math.abs(x - px) + Math.abs(y - py) < radius * 0.5 * (1 + rng.int(-10, 10) * 0.015)
347	          && st.type[ti] !== ORB) {
348	          st.flags[ti] = 0; // 只清 active(原版 KillTile)——壳层不回填
349	        }
350	      }
351	    }
352	    px += vx; py += vy;
353	    vy += rng.int(-10, 9) * 0.1;
354	    if (py < j - 20) vy += rng.int(0, 19) * 0.01;
355	    if (py > j + 20) vy -= rng.int(0, 19) * 0.01;
356	    vy = Math.max(-0.5, Math.min(0.5, vy));
357	    vx += rng.int(-10, 10) * 0.01;
358	    if (direction === -1) { if (vx > -0.5) vx = -0.5; if (vx < -2) vx = -2; }
359	    else { if (vx < 0.5) vx = 0.5; if (vx > 2) vx = 2; }
360	    // 黑檀石壳 + 墙 3
361	    const x2 = Math.max(1, Math.floor(px - radius * 1.1)), x3 = Math.min(st.w - 1, Math.floor(px + radius * 1.1));
362	    const y2 = Math.max(0, Math.floor(py - radius * 1.1)), y3 = Math.min(st.h, Math.floor(py + radius * 1.1));
363	    for (let x = x2; x < x3; x++) {
364	      for (let y = y2; y < y3; y++) {
365	        const ti = st.idx(x, y);
366	        if (Math.abs(x - px) + Math.abs(y - py) < radius * 1.1 * (1 + rng.int(-10, 10) * 0.015) && st.wall[ti] !== 3) {
367	          if (st.type[ti] !== EBONSTONE && y > j + rng.int(3, 19)) st.flags[ti] = 1;
368	          st.flags[ti] = 1;
369	          if (st.type[ti] !== ORB && st.type[ti] !== EBONSTONE) st.type[ti] = EBONSTONE;
370	          if (st.wall[ti] === 2) st.wall[ti] = 0;
371	        }
372	      }
373	    }
374	    for (let x = x2; x < x3; x++) {
375	      for (let y = y2; y < y3; y++) {
376	        const ti = st.idx(x, y);
377	        if (Math.abs(x - px) + Math.abs(y - py) < radius * 1.1 * (1 + rng.int(-10, 10) * 0.015) && st.wall[ti] !== 3) {
378	          if (st.type[ti] !== ORB && st.type[ti] !== EBONSTONE) st.type[ti] = EBONSTONE;
379	          st.flags[ti] = 1;
380	          st.wall[ti] = 3;
381	        }
382	      }
383	    }
384	  }
385	  // 1/3 概率末端魔矿脉
386	  if (rng.int(0, 2) !== 0) return;
387	  const x = Math.floor(px);
388	  let y = Math.floor(py);
389	  while (!st.flags[st.idx(x, y)] && y < st.h - 2) y++;
390	  // 魔矿 22 缺独立 tile,用黑檀石小脉近似
391	  for (let dx = -2; dx <= 2; dx++) {
392	    for (let dy = -2; dy <= 2; dy++) {
393	      if (dx * dx + dy * dy <= 4 && st.inBounds(x + dx, y + dy)) {
394	        st.flags[st.idx(x + dx, y + dy)] = 1;
395	        st.type[st.idx(x + dx, y + dy)] = EBONSTONE;
396	      }
397	    }
398	  }
399	}
400	
401	/** CrimStart(L45443):弹坑隧道 + CrimVein 血管(5-8 条,终点=恶魔之心) */
402	function crimStart(st: TileStore, rng: RNG, gs: GenState, i: number, j: number): void {
403	  const entryX = i, entryY0 = Math.min(j, gs.worldSurface);
404	  let py = entryY0;
405	  while (!st.isSolid(i, py) && py < st.h - 2) py++;
406	  let px = i + 0.0;
407	  const startY = py;
408	  let vx = rng.int(-20, 20) * 0.1;
409	  let vy = rng.int(20, 200) * 0.01;
410	  let radius = rng.int(15, 25);
411	  let recenter = 0;  // cs L45517 num4:X 回中状态(漂离入口 ±50 后反向修正)
412	  // 主通道随机走(向下椭圆隧道)
413	  while (true) {
414	    radius += rng.int(-50, 50) * 0.01;
415	    radius = Math.max(15, Math.min(25, radius));
416	    const x0 = Math.floor(px - radius / 2), x1 = Math.floor(px + radius / 2);
417	    const y0 = Math.floor(py - radius / 2), y1 = Math.floor(py + radius / 2);
418	    for (let x = x0; x < x1; x++) {
419	      for (let y = y0; y < y1; y++) {
420	        if (!st.inBounds(x, y)) continue;
421	        const d = Math.abs(x - px) + Math.abs(y - py);
422	        const ti = st.idx(x, y);
423	        if (y > startY) {
424	          if (d < radius * 0.3) {
425	            st.type[ti] = 0; st.flags[ti] = 0; st.wall[ti] = 83;
426	          } else if (d < radius * 0.8 && st.wall[ti] !== 83) {
427	            st.flags[ti] = 1; st.type[ti] = CRIMSTONE;
428	            if (d < radius * 0.6) st.wall[ti] = 83;
429	          }
430	        } else if (d < radius * 0.3 && st.flags[ti]) {
431	          st.type[ti] = 0; st.flags[ti] = 0; st.wall[ti] = 83;
432	        }
433	      }
434	    }
435	    // X 回中(cs L45494-45503):漂离入口 ±50 后设反向偏置,未漂时正常随机走
436	    if (px > entryX + 50) recenter = -100;
437	    if (px < entryX - 50) recenter = 100;
438	    if (recenter < 0) vx -= rng.int(20, 50) * 0.01;
439	    else if (recenter > 0) vx += rng.int(20, 50) * 0.01;
440	    else vx += rng.int(-50, 50) * 0.01;
441	    vy += rng.int(-50, 50) * 0.01;
442	    vy = Math.max(0.25, Math.min(2, vy));
443	    vx = Math.max(-2, Math.min(2, vx));
444	    px += vx; py += vy;
445	    if (py > gs.worldSurface + 100) break;
446	    if (py > st.h - 10 || px < 5 || px > st.w - 5) break;
447	  }
448	  // ---- 隧道终点囊群(cs L45551-45585):50 个半径 40-54 球,核心 0.25R 清空、壳 0.4R 猩红石 ----
449	  const endR = rng.int(40, 54);
450	  for (let n = 0; n < 50; n++) {
451	    const cx = Math.floor(px) + rng.int(-20, 20);
452	    const cy = Math.floor(py) + rng.int(-20, 20);
453	    for (let x = Math.floor(cx - endR / 2); x < cx + endR / 2; x++) {
454	      for (let y = Math.floor(cy - endR / 2); y < cy + endR / 2; y++) {
455	        if (!st.inBounds(x, y)) continue;
456	        const d = Math.hypot(
457	          Math.abs(x - cx) * (1 + rng.int(-20, 20) * 0.01),
458	          Math.abs(y - cy) * (1 + rng.int(-20, 20) * 0.01),
459	        );
460	        const ti = st.idx(x, y);
461	        if (d < endR * 0.25) {
462	          st.type[ti] = 0; st.flags[ti] = 0; st.wall[ti] = 83;
463	        } else if (d < endR * 0.4 && st.wall[ti] !== 83) {
464	          st.flags[ti] = 1; st.type[ti] = CRIMSTONE;
465	          if (d < endR * 0.35) st.wall[ti] = 83;
466	        }
467	      }
468	    }
469	  }
470	  // ---- CrimVein:5-8 条血管从通道终点出发(Y 只向下/水平),终点记录为心位 ----
471	  const veinCount = rng.int(5, 8);
472	  const usedV: Array<[number, number]> = [];
473	  const hearts: Array<[number, number]> = [];
474	  for (let n = 0; n < veinCount; n++) {
475	    let vx2 = 0, vy2 = 0, tries2 = 0;
476	    for (;;) {
477	      vx2 = rng.int(-20, 20) * 0.15;
478	      vy2 = rng.int(0, 20) * 0.15;
479	      if (Math.abs(vx2) + Math.abs(vy2) >= 1.5
480	        && usedV.every(([ux, uy]) => Math.abs(ux - vx2) >= 0.75 || Math.abs(uy - vy2) >= 0.75)) break;
481	      if (++tries2 > 10000) break;
482	    }
483	    usedV.push([vx2, vy2]);
484	    hearts.push(crimVein(st, rng, px, py, vx2, vy2));
485	  }
486	  // ---- 地表囊群(CrimStart 末段:从入口点向上漂移的 25-35 半径球)----
487	  let sx = entryX + 0.0, sy = startY + 0.0;
488	  let rise = rng.int(0, 5);
489	  const pocketR = rng.int(25, 34);
490	  let shellMinX = st.w, shellMaxX = 0;  // 壳层覆盖范围(列填充用,cs L45587-45589)
491	  for (let n = 0; n < 50; n++) {
492	    if (rise > 0) {
493	      const step = rng.int(10, 29) * 0.01;
494	      rise -= step;
495	      sy -= step;
496	    }
497	    const cx = Math.floor(sx) + rng.int(-2, 2);
498	    const cy = Math.floor(sy) + rng.int(-2, 2);
499	    for (let x = Math.floor(cx - pocketR / 2); x < cx + pocketR / 2; x++) {

```


---

## 🤖 Assistant · 2026-08-11T04:10:10.763Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
CrimStart: startY = first solid at entryX from entryY0 (= min(worldSurfaceLow-10, worldSurface)) — that's at/near the surface. Main tunnel: for y > startY → carve/crimstone below start. For y <= startY (line 430): `else if (d < radius*0.3 && st.flags[ti])` → clears tiles ABOVE startY — i.e., carves a crater opening into the sky area (removes surface blocks above startY, within radius 0.3 of the tunnel center as py increases... wait py increases downward, so at the beginning py ≈ startY, and the box y0..y1 includes y < startY — cells above the start → cleared if active). So CrimStart removes surface blocks to open a crater — this REMOVES sky-adjacent blocks, doesn't add.

Then the "surface pockets" at line 486+: pockets rising upward from entry (sy -= step) with radius 25-34 — these are placed ABOVE the surface start (sy rises above startY)! Let me read lines 499-560 to see whether they write crimstone in the sky.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:11.008Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts",
 "offset": 499,
 "limit": 146
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:11.028Z

**📎 ToolResult**

```
499	    for (let x = Math.floor(cx - pocketR / 2); x < cx + pocketR / 2; x++) {
500	      for (let y = Math.floor(cy - pocketR / 2); y < cy + pocketR / 2; y++) {
501	        if (!st.inBounds(x, y)) continue;
502	        const d = Math.hypot(
503	          Math.abs(x - cx) * (1 + rng.int(-20, 20) * 0.005),
504	          Math.abs(y - cy) * (1 + rng.int(-20, 20) * 0.005),
505	        );
506	        const ti = st.idx(x, y);
507	        if (d < pocketR * 0.2 * (rng.int(90, 110) * 0.01)) {
508	          st.type[ti] = 0; st.flags[ti] = 0; st.wall[ti] = 83;
509	        } else if (d < pocketR * 0.45) {
510	          if (x < shellMinX) shellMinX = x;
511	          if (x > shellMaxX) shellMaxX = x;
512	          if (st.wall[ti] !== 83) {
513	            st.flags[ti] = 1; st.type[ti] = CRIMSTONE;
514	            if (d < pocketR * 0.35) st.wall[ti] = 83;
515	          }
516	        }
517	      }
518	    }
519	  }
520	  // ---- 列填充(cs L45629-45640):囊群覆盖范围内每列向下补 15-19 格猩红石 ----
521	  for (let x = shellMinX; x <= shellMaxX; x++) {
522	    if (x < 1 || x >= st.w - 1) continue;
523	    let y = startY;
524	    if (y < 0) y = 0;
525	    while (y < st.h - 1 && ((st.type[st.idx(x, y)] === CRIMSTONE && st.flags[st.idx(x, y)]) || st.wall[st.idx(x, y)] === 83)) y++;
526	    let fill = rng.int(15, 19);
527	    while (y < st.h - 1 && !st.flags[st.idx(x, y)] && fill > 0 && st.wall[st.idx(x, y)] !== 83) {
528	      fill--;
529	      st.type[st.idx(x, y)] = CRIMSTONE;
530	      st.flags[st.idx(x, y)] = 1;
531	      y++;
532	    }
533	  }
534	  // ---- CrimEnt:水平入口(半径 6-10,只挖猩红石,20 步无肉即停)----
535	  crimEnt(st, rng, entryX, Math.floor(sy), vx >= 0 ? -1 : 1);
536	  // ---- CrimPlaceHearts:心室(壳→空腔→心)----
537	  for (const [hx, hy] of hearts) {
538	    const r1 = rng.int(16, 20);
539	    for (let x = hx - Math.floor(r1 / 2); x < hx + r1 / 2; x++) {
540	      for (let y = hy - Math.floor(r1 / 2); y < hy + r1 / 2; y++) {
541	        if (!st.inBounds(x, y)) continue;
542	        if (Math.hypot(x - hx, y - hy) < r1 * 0.4) {
543	          const ti = st.idx(x, y);
544	          st.flags[ti] = 1; st.type[ti] = CRIMSTONE; st.wall[ti] = 83;
545	        }
546	      }
547	    }
548	    const r2 = rng.int(10, 13);
549	    for (let x = hx - Math.floor(r2 / 2); x < hx + r2 / 2; x++) {
550	      for (let y = hy - Math.floor(r2 / 2); y < hy + r2 / 2; y++) {
551	        if (!st.inBounds(x, y)) continue;
552	        if (Math.hypot(x - hx, y - hy) < r2 * 0.3) {
553	          const ti = st.idx(x, y);
554	          st.type[ti] = 0; st.flags[ti] = 0; st.wall[ti] = 83;
555	        }
556	      }
557	    }
558	    addShadowOrb(st, hx, hy, true);
559	  }
560	}
561	
562	/** CrimVein(L45724)1:1:血管走——核心 0.2R 挖空(墙83)/壳 0.5R 猩红石;曼哈顿行程 100-150 */
563	function crimVein(st: TileStore, rng: RNG, sx: number, sy: number, ivx: number, ivy: number): [number, number] {
564	  let radius = rng.int(15, 25);
565	  const trip = rng.int(100, 149) - (ivy < 0 ? 25 : 0);
566	  let px = sx, py = sy;
567	  let vx = ivx, vy = ivy;
568	  while (Math.abs(px - sx) + Math.abs(py - sy) <= trip) {
569	    radius += rng.int(-50, 50) * 0.02;
570	    radius = Math.max(15, Math.min(25, radius));
571	    const x0 = Math.floor(px - radius / 2), x1 = Math.floor(px + radius / 2);
572	    const y0 = Math.floor(py - radius / 2), y1 = Math.floor(py + radius / 2);
573	    for (let x = x0; x < x1; x++) {
574	      for (let y = y0; y < y1; y++) {
575	        if (!st.inBounds(x, y)) continue;
576	        const d = Math.hypot(x - px, y - py);
577	        const ti = st.idx(x, y);
578	        if (d < radius * 0.2) {
579	          st.type[ti] = 0; st.flags[ti] = 0; st.wall[ti] = 83;
580	        } else if (d < radius * 0.5 && st.wall[ti] !== 83) {
581	          st.flags[ti] = 1; st.type[ti] = CRIMSTONE;
582	          if (d < radius * 0.4) st.wall[ti] = 83;
583	        }
584	      }
585	    }
586	    vx += rng.int(-50, 50) * 0.05;
587	    vy += rng.int(-50, 50) * 0.05;
588	    vx = Math.max(ivx - 0.75, Math.min(ivx + 0.75, vx));
589	    vy = Math.max(ivy - 0.75, Math.min(ivy + 0.75, vy));
590	    px += vx; py += vy;
591	    if (py > st.h - 30 || py < 5 || px < 5 || px > st.w - 5) break;
592	  }
593	  return [Math.floor(px), Math.floor(py)];
594	}
595	
596	/** CrimEnt(L45689)1:1:水平入口隧道,只贯穿猩红石,连续 20 步无肉即停 */
597	function crimEnt(st: TileStore, rng: RNG, x0: number, y0: number, dir: number): void {
598	  let radius = rng.int(6, 10);
599	  const vx = 2 * -dir;
600	  let vy = rng.int(-20, -1) * 0.01;
601	  let px = x0 + 0.0, py = y0 + 0.0;
602	  let misses = 0;
603	  while (misses < 20) {
604	    misses++;
605	    radius += rng.int(-10, 10) * 0.02;
606	    radius = Math.max(6, Math.min(10, radius));
607	    const bx0 = Math.floor(px - radius / 2), bx1 = Math.floor(px + radius / 2);
608	    const by0 = Math.floor(py - radius / 2), by1 = Math.floor(py + radius / 2);
609	    for (let x = bx0; x < bx1; x++) {
610	      for (let y = by0; y < by1; y++) {
611	        if (!st.inBounds(x, y)) continue;
612	        const ti = st.idx(x, y);
613	        if (st.flags[ti] && st.type[ti] === CRIMSTONE && Math.hypot(x - px, y - py) < radius * 0.5) {
614	          st.type[ti] = 0; st.flags[ti] = 0;
615	          misses = 0;
616	        }
617	      }
618	    }
619	    px += vx; py += vy;
620	  }
621	}
622	
623	/** 暗影之球周的黑檀石囊(L6416-6446):球周 ±13 L1<9-19 处填黑檀石、球旁清空 */
624	function cleanOrbPockets(st: TileStore, rng: RNG): void {
625	  const { w, h } = st;
626	  for (let x = 0; x < w; x++) {
627	    for (let y = 0; y < h - 50; y++) {
628	      if (!st.flags[st.idx(x, y)] || st.type[st.idx(x, y)] !== ORB) continue;
629	      for (let dx = -13; dx < 13; dx++) {
630	        if (x + dx <= 10 || x + dx >= w - 10) continue;
631	        for (let dy = -13; dy < 13; dy++) {
632	          if (y + dy < 0 || y + dy >= h) continue;
633	          const ti = st.idx(x + dx, y + dy);
634	          if (Math.abs(dx) + Math.abs(dy) < 9 + rng.int(0, 10) && rng.int(0, 2) !== 0 && st.type[ti] !== ORB) {
635	            st.flags[ti] = 1; st.type[ti] = EBONSTONE;
636	            if (Math.abs(dx) <= 1 && Math.abs(dy) <= 1) { st.flags[ti] = 0; st.type[ti] = 0; }
637	          }
638	          if (st.type[ti] !== ORB && Math.abs(dx) <= 2 + rng.int(0, 2) && Math.abs(dy) <= 2 + rng.int(0, 2)) {
639	            st.flags[ti] = 0; st.type[ti] = 0;
640	          }
641	        }
642	      }
643	    }
644	  }

```


---

## 🤖 Assistant · 2026-08-11T04:10:22.736Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
MAJOR FINDING — Crimson sky writer:

CrimStart "surface pockets" (lines 486-519): from entry (startY ≈ surface), 50 spheres of radius 25-34 that RISE (sy -= step up to 5 tiles) — each sphere writes CRIMSTONE with flags=1 (line 513) for d < pocketR*0.45. Since pockets rise above startY and the surface at startX may be lower (valley), the sphere shells extend ABOVE the original surface → real CRIMSTONE blocks written into the SKY (the crimson crater mounds). This is vanilla behavior too (crimson surface mounds). But wait — rise is only rng.int(0,5) total, decremented by 0.1-0.29 per step over 50 iterations... Actually rise decreases by up to 2.9 per iteration; the pockets drift up at most 5 tiles from startY. With radius 25-34 and shell at 0.45R (≈11-15 tiles from center), pockets centered at startY-5 with radius ~15 → up to y ≈ startY-20 in the sky! So yes, up to ~20 tiles of real crimstone above the surface → the crater mound. That's intentional vanilla look (crimson chasm mounds).

Hmm, but note the pocket cores (d < 0.2R) clear to air. OK.

Now, let me also check TrapsPass, HellFortPass, HiveSpiderPass, TemplePass, DungeonPass, Spread, and HiveSpider for sky writes. DungeonPass especially — the dungeon entrance extends above the surface. Let me grep DungeonPass for above-surface logic.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:23.246Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla && grep -n \"worldSurface\\|dungeonY\\|groundLevel\" DungeonPass.ts | head -50",
 "description": "Grep DungeonPass y anchors"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:23.285Z

**📎 ToolResult**

```
129:  let y0 = Math.floor((gs.worldSurface + gs.rockLevel) / 2) + rng.int(-200, 199);
133:    const cap = Math.floor((gs.worldSurface + gs.rockLevel) / 2) + 200;
136:  y0 = Math.max(gs.worldSurface + 10, Math.min(h - 220, y0));
179:      if (delay === 0 && rng.next() < 0.2 && dy > gs.worldSurface + 100) {
197:    gs.dungeonY = entPos[1];   // 入口地表 Y（刷怪门槛 CheckToSpawnDungeonEnemies）
204:      if (delay === 0 && rng.next() < 0.2 && dy > gs.worldSurface + 100) {
216:    if (dy > gs.worldSurface - 5) {
219:      while (sy2 > gs.worldSurface - 5 && guard2++ < 800) {
242:    gs.dungeonY = gY;          // 入口地表 Y（刷怪门槛 CheckToSpawnDungeonEnemies）
439:      if (py < gs.worldSurface - 5) {
483:    if (!precalc && py < gs.worldSurface) vy *= 0.98;
490: * 周期 2+Next(4))→ 下延到 worldSurface → 0.6 框刷墙×2 → 0.5 框清空(塔内厅)。
550:  // 下延到 worldSurface(num6 → worldSurface):填砖,内列刷墙
552:    for (let y = b1; y < Math.min(st.h, Math.floor(gs.worldSurface)); y++) {
606:    for (let y = b2; y < Math.min(st.h, Math.floor(gs.worldSurface)); y++) extFill(x, y, true, false);
744:      const y = rng.int(Math.max(gs.worldSurface, dc.minYY), Math.max(dc.minYY + 1, dc.maxY));
868:          if (y <= gs.worldSurface) continue;
881:    const maxSpan = py0 < gs.worldSurface + 50 ? 20 : 10;
935:      const y = rng.int(Math.floor(gs.worldSurface), by1);
1026:        if (y < gs.worldSurface + 50) loot = { item: 'vi_327_golden_key', style: 0 };
1178:      while (y < gs.worldSurface && y < ey1) y = rng.int(ey0, ey1);
1205:        y = rng.int(Math.floor(gs.worldSurface) + 10, ey1);
1309:        y = rng.int(Math.floor(gs.worldSurface), ey1);

```


---

## 🤖 Assistant · 2026-08-11T04:10:23.905Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla && grep -n \"worldSurface\\|rng.int(0\\|setTileSilent\" TrapsPass.ts HellFortPass.ts HiveSpiderPass.ts TemplePass.ts Spread.ts | head -60",
 "description": "Grep other passes for y anchors"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:23.951Z

**📎 ToolResult**

```
HellFortPass.ts:36:    if (rng.next() < 0.1) i += rng.int(0, 199);
HellFortPass.ts:65:      st.setTileSilent(x + side, y, TORCH, 7 * 36, 0);
HellFortPass.ts:93:    if (rng.int(0, 2) === 0) {
HellFortPass.ts:95:      let r = rng.int(0, 9);
HellFortPass.ts:99:      if (rng.int(0, 1) === 0) { occ[0][r] = true; occ[1][r] = true; wingCol = 0; }
HellFortPass.ts:101:      let dir = rng.int(0, 1); if (dir === 0) dir = -1;
HellFortPass.ts:102:      for (let steps = rng.int(0, 9); steps > 0 && r >= 0 && r < 10; r += dir) occ[wingCol][r] = true;
HellFortPass.ts:104:    if (rng.int(0, 2) === 0) {
HellFortPass.ts:106:      let r = rng.int(0, 9);
HellFortPass.ts:110:      if (rng.int(0, 1) === 0) { occ[3][r] = true; occ[4][r] = true; wingCol = 4; }
HellFortPass.ts:112:      let dir = rng.int(0, 1); if (dir === 0) dir = -1;
HellFortPass.ts:113:      for (let steps = rng.int(0, 9); steps > 0 && r >= 0 && r < 10; r += dir) occ[wingCol][r] = true;
HellFortPass.ts:128:  let n4 = rng.int(0, 9); if (n4 < spanLo) spanLo = n4;
HellFortPass.ts:129:  let n5 = rng.int(0, 9); if (n5 > spanHi) spanHi = n5;
HellFortPass.ts:133:      const a = rng.int(0, 9); if (a < spanLo) spanLo = a;
HellFortPass.ts:134:      const b = rng.int(0, 9); if (b > spanHi) spanHi = b;
HellFortPass.ts:172:      const r = rng.int(0, 9);
HellFortPass.ts:206:            st.setTileSilent(x, rowT[r], PLATFORM, 0, 13 * 18);
HellFortPass.ts:211:      if (c < 4 && occ[c + 1][r] && rng.int(0, 2) === 0) {
HellFortPass.ts:243:        const r = rng.int(0, 9);
HellFortPass.ts:279:        const r = rng.int(0, 9);
HellFortPass.ts:306:        const c = rng.int(0, 4);
HellFortPass.ts:328:              st.setTileSilent(x, rowT[r], PLATFORM, 0, 13 * 18);
TrapsPass.ts:52:  if (type === -1 && rng.int(0, 19) === 0) type = 2;
TrapsPass.ts:53:  else if (type === -1 && py > gs.lavaLine + 30 && rng.int(0, 5) !== 0) type = 3;
TrapsPass.ts:54:  else if (type === -1) type = rng.int(0, 1);
TrapsPass.ts:86:      if (top < gs.worldSurface) return false;
TrapsPass.ts:92:      for (let yy = top; yy <= py; yy++) st.setTileSilent(xx, yy, 0);
TrapsPass.ts:97:        if (solidAt(st, xx, yy)) st.setTileSilent(xx, yy, T.STONE);   // 石头壳（内部 id 非 sheet）
TrapsPass.ts:101:    st.setTileSilent(px, py, PLATE, 0, 126);
TrapsPass.ts:103:    st.setTileSilent(colX + 1, top + 1, BOULDER138, 0, 0);
TrapsPass.ts:110:        st.setTileSilent(gx, gy, T.STONE);
TrapsPass.ts:132:    st.setTileSilent(bx, by, EXPLOSIVES, 0, rng.int(0, 1) * 18);
TrapsPass.ts:133:    st.setTileSilent(px, py, PLATE, 0, rng.int(2, 3) * 18);
TrapsPass.ts:143:    const fx = rng.int(0, 1);
TrapsPass.ts:145:      st.setTileSilent(px + k, py, GEYSER, 18 * k + 36 * fx, 0);
TrapsPass.ts:174:  const j2 = py - rng.int(0, 2);
TrapsPass.ts:195:    if (rng.int(0, 1) === 0) { i5 = i4; dir = -1; }
TrapsPass.ts:201:  st.setTileSilent(px, py, PLATE, 0, st.wall[st.idx(px, py)] > 0 ? 36 : rng.int(2, 3) * 18);
TrapsPass.ts:202:  st.setTileSilent(i5, j2, TRAP, dir === 1 ? 18 : 0, 0);
TrapsPass.ts:272:        if (!flag) st.setTileSilent(xx, yy, SANDSTONE);
TrapsPass.ts:274:        st.setTileSilent(xx, yy, !flag || !st.flags[st.idx(xx, yy - 1)] ? SANDSTONE : HARDSAND);
TrapsPass.ts:276:        if (!flag) st.setTileSilent(xx, yy, SANDSTONE);
TrapsPass.ts:278:        st.setTileSilent(xx, yy, SAND);
TrapsPass.ts:301:      let y = rng.int(gs.worldSurface, st.h - 211);           // Next(surface, h-210)
TrapsPass.ts:303:      const oceanTop = (gs.worldSurface + gs.rockLevel) / 2 + 40;
TrapsPass.ts:307:        y = rng.int(gs.worldSurface, st.h - 211);
TrapsPass.ts:316:      const y = rng.int(gs.worldSurface + 20, st.h - 211);
TemplePass.ts:85:        if (rng.int(0, 99) === 0) overlap++;
TemplePass.ts:137:        if (rng.int(0, 19) === 0) t += rng.int(-1, 1);
TemplePass.ts:138:        if (rng.int(0, 19) === 0) b += rng.int(-1, 1);
TemplePass.ts:139:        if (rng.int(0, 19) === 0) l += rng.int(-1, 1);
TemplePass.ts:140:        if (rng.int(0, 19) === 0) rr += rng.int(-1, 1);
TemplePass.ts:156:        if (rng.int(0, 19) === 0) t += rng.int(-1, 1);
TemplePass.ts:157:        if (rng.int(0, 19) === 0) b += rng.int(-1, 1);
TemplePass.ts:158:        if (rng.int(0, 19) === 0) l += rng.int(-1, 1);
TemplePass.ts:159:        if (rng.int(0, 19) === 0) rr += rng.int(-1, 1);
TemplePass.ts:213:      if (rng.int(0, 2) !== 0) {
TemplePass.ts:358:    const ax = acx + 15 - rng.int(0, 29);
TemplePass.ts:359:    const ay = acy + 15 - rng.int(0, 29);

```


---

## 🤖 Assistant · 2026-08-11T04:10:27.088Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
DungeonPass line 216-219 and 439, 550-552, 606: the dungeon tower extends UP to worldSurface-5, i.e., the tower/entrance structure rises above the surface into the sky! Line 550: "下延到 worldSurface(num6 → worldSurface):填砖,内列刷墙" — the entrance corridor rises to worldSurface. And line 439: `if (py < gs.worldSurface - 5)`. Let me read DungeonPass around 120-260 and 420-620 to understand the above-ground part.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:27.294Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts",
 "offset": 110,
 "limit": 160
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:27.314Z

**📎 ToolResult**

```
110	        for (let y = Math.max(50, ny - 50); y < ny; y++) {
111	          if (st.inBounds(nx + dx, y) && CLOUD.has(st.type[st.idx(nx + dx, y)])) { cloud = true; break; }
112	        }
113	      }
114	      if (cloud || ny - 80 <= 0) continue;
115	      found = true;
116	    }
117	    if (found) {
118	      gs.dungeonLocation = nx + 25 - rng.int(0, 49);
119	      entPos = [nx, ny];
120	    }
121	  }
122	  const x0 = gs.dungeonLocation;
123	  if (x0 < 30 || x0 > w - 30) return;
124	  // 原版主题:Next(3) → 蓝41/墙7、绿43/墙8、粉44/墙9
125	  const theme = rng.int(0, 2);
126	  const brick = theme === 0 ? BLUE : theme === 1 ? GREEN : PINK;
127	  const wallId = brick === BLUE ? 7 : brick === GREEN ? 8 : 9;
128	  // 深度:找实心(L6565)
129	  let y0 = Math.floor((gs.worldSurface + gs.rockLevel) / 2) + rng.int(-200, 199);
130	  let solid = false;
131	  for (let d = 0; d < 10; d++) if (st.flags[st.idx(x0, y0 + d)]) { solid = true; break; }
132	  if (!solid) {
133	    const cap = Math.floor((gs.worldSurface + gs.rockLevel) / 2) + 200;
134	    while (y0 < cap && !st.flags[st.idx(x0, y0 + 10)]) y0++;
135	  }
136	  y0 = Math.max(gs.worldSurface + 10, Math.min(h - 220, y0));
137	  const dc = new DungeonCtx(brick, wallId, x0, y0);
138	  // 原版 L18045-18048:入口塔尺寸强度(DungeonEnt 与竖井出口探测共用)
139	  dc.dxS1 = rng.int(25, 29); dc.dyS1 = rng.int(20, 24);
140	  dc.dxS2 = rng.int(35, 49); dc.dyS2 = rng.int(10, 14);
141	  // ---- 主链随机游走(L18053)----
142	  let budget = w / 60 + rng.int(0, Math.max(1, Math.floor(w / 180)));
143	  let dx = x0, dy = y0;
144	  dungeonRoom(st, rng, gs, dc, dx, dy);
145	  let step5 = 5;
146	  while (budget > 0) {
147	    dc.updateBBox(dx, dy);
148	    budget--;
149	    step5--;
150	    if (step5 === 0 && rng.next() * 3 < 1) {
151	      step5 = 5;
152	      if (rng.next() < 0.5) {
153	        // 分支:保存位置→走廊(可能两条)+房→恢复
154	        const sx = dx, sy = dy;
155	        [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
156	        if (rng.next() < 0.5) [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
157	        dungeonRoom(st, rng, gs, dc, dx, dy);
158	        dx = sx; dy = sy;
159	      } else {
160	        dungeonRoom(st, rng, gs, dc, dx, dy);
161	      }
162	    } else {
163	      [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
164	    }
165	  }
166	  dungeonRoom(st, rng, gs, dc, dx, dy);
167	  // ---- 爬升到地表(1456 语义,DungeonCrawler.cs L400-449):上限 100;num8 到 0 后
168	  // 每轮 1/5 概率 halls(forceX)+room 分支(原版 num8 保持在 0) ----
169	  let best = dc.rooms[0];
170	  for (const r of dc.rooms) if (r.t < best.t) best = r;
171	  dc.entranceX = best.cx;
172	  dx = best.cx; dy = best.cy;
173	  if (entPos) {
174	    // 预计算模式:沿直线分段走向入口,每段 10-29 步,剩余距离耗尽即达(确定性终止)
175	    let remaining = Math.hypot(entPos[0] - dx, entPos[1] - dy);
176	    let delay = 5, guard = 0;
177	    while (remaining > 0 && guard++ < 100) {
178	      if (delay > 0) delay--;
179	      if (delay === 0 && rng.next() < 0.2 && dy > gs.worldSurface + 100) {
180	        delay = 10;
181	        const sx = dx, sy = dy;
182	        [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, true);
183	        dungeonRoom(st, rng, gs, dc, dx, dy);
184	        dx = sx; dy = sy;
185	      }
186	      let steps = rng.int(10, 29);
187	      if (steps > remaining) steps = Math.max(1, Math.floor(remaining));
188	      const d = Math.hypot(entPos[0] - dx, entPos[1] - dy) || 1;
189	      const res = dungeonStairs(st, rng, gs, dc, dx, dy, {
190	        vx: (entPos[0] - dx) / d, vy: (entPos[1] - dy) / d, steps,
191	      });
192	      dx = res[0]; dy = res[1];
193	      remaining -= steps;
194	    }
195	    dx = entPos[0]; dy = entPos[1];
196	    dungeonEnt(st, rng, gs, dc, dx, dy);
197	    gs.dungeonY = entPos[1];   // 入口地表 Y（刷怪门槛 CheckToSpawnDungeonEnemies）
198	  } else {
199	    // legacy 盲爬(1405 结构 + 1456 的 100 上限):外壳探测到开放天空即停
200	    let reached = false;
201	    let delay = 5, guard = 0;
202	    while (!reached && guard++ < 100) {
203	      if (delay > 0) delay--;
204	      if (delay === 0 && rng.next() < 0.2 && dy > gs.worldSurface + 100) {
205	        delay = 10;
206	        const sx = dx, sy = dy;
207	        [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, true);
208	        dungeonRoom(st, rng, gs, dc, dx, dy);
209	        dx = sx; dy = sy;
210	      }
211	      const res = dungeonStairs(st, rng, gs, dc, dx, dy);
212	      dx = res[0]; dy = res[1];
213	      reached = res[2];
214	    }
215	    // 兜底:楼梯没到地表则从当前位置直挖竖井到地表(垂直,保证衔接)
216	    if (dy > gs.worldSurface - 5) {
217	      let sx2 = dx, sy2 = dy;
218	      let guard2 = 0;
219	      while (sy2 > gs.worldSurface - 5 && guard2++ < 800) {
220	        for (let ax = -3; ax <= 3; ax++) {
221	          for (let ay = -3; ay <= 3; ay++) {
222	            if (!st.inBounds(sx2 + ax, sy2 + ay)) continue;
223	            const i = st.idx(sx2 + ax, sy2 + ay);
224	            st.flags[i] = 0; st.wall[i] = dc.wall;
225	          }
226	        }
227	        for (let ax = -4; ax <= 4; ax++) {
228	          for (let ay = -4; ay <= 4; ay++) {
229	            if (!st.inBounds(sx2 + ax, sy2 + ay)) continue;
230	            const i = st.idx(sx2 + ax, sy2 + ay);
231	            if (!dc.isDungeonWall(st, sx2 + ax, sy2 + ay)) { st.type[i] = dc.brick; st.flags[i] = 1; }
232	          }
233	        }
234	        sy2--;
235	      }
236	      dx = sx2; dy = sy2;
237	    }
238	    // 找楼梯出口列的真实地表,塔吸附其上
239	    let gY = 0;
240	    while (gY < st.h - 2 && !st.flags[st.idx(dx, gY)]) gY++;
241	    dungeonEnt(st, rng, gs, dc, dx, gY);
242	    gs.dungeonY = gY;          // 入口地表 Y（刷怪门槛 CheckToSpawnDungeonEnemies）
243	  }
244	  if (dc.entStand) {
245	    gs.dungeonEntX = dc.entStand[0];
246	    gs.dungeonEntY = dc.entStand[1];
247	  }
248	  // ---- 房口平台候选(cs L18137-18180,与门候选同期收集)----
249	  for (const room of dc.rooms) {
250	    for (let x = room.l; x <= room.r; x++) {
251	      if (st.inBounds(x, room.t - 1) && !st.flags[st.idx(x, room.t - 1)]) { dc.dPlatforms.push([x, room.t - 1]); break; }
252	    }
253	    for (let x = room.l; x <= room.r; x++) {
254	      if (st.inBounds(x, room.b + 1) && !st.flags[st.idx(x, room.b + 1)]) { dc.dPlatforms.push([x, room.b + 1]); break; }
255	    }
256	  }
257	  // ---- 尖刺(L18188)----
258	  placeSpikes(st, rng, gs, dc, Math.floor(w / 100));
259	  // ---- 门(L18311)----
260	  placeDoors(st, rng, dc);
261	  // ---- 陈设管线(L18441-19613):墙变体→房口平台→特殊宝箱→书架平台→房间金箱→
262	  //      灯具+开关布线→陷阱→地面家具→墙饰→旗帜 ----
263	  placeFurnishing(st, rng, gs, dc, chests);
264	}
265	
266	/** DungeonHalls(L20255):走廊随机游走 */
267	function dungeonHalls(st: TileStore, rng: RNG, gs: GenState, dc: DungeonCtx, ix: number, iy: number, forceX: boolean): [number, number] {
268	  let radius = rng.int(4, 5);
269	  const baseR = radius;

```


---

## 🤖 Assistant · 2026-08-11T04:10:30.046Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The dungeon entrance (`dungeonEnt`) is at the surface (gY). Let me read dungeonEnt (around line 480-620) to see how far above the surface it builds (the entrance tower). Lines 550-552 and 606 mention "下延到 worldSurface:填砖" — that means fill bricks from b1 down to worldSurface. Let me read.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:30.090Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts",
 "limit": 180,
 "offset": 480
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:30.109Z

**📎 ToolResult**

```
480	    }
481	    dc.updateBBox(Math.floor(px), Math.floor(py));
482	    px += vx; py += vy;
483	    if (!precalc && py < gs.worldSurface) vy *= 0.98;
484	  }
485	  return [Math.floor(px), Math.floor(py), reached];
486	}
487	
488	/** DungeonEnt(L20726-21273)逐行 1:1:两段式入口。
489	 * 主塔段:0.6±Next(2,5) 实心(内缩1刷墙)→ 垛口(5+Next(4) 宽)→ 顶齿(1+Next(2) 高,
490	 * 周期 2+Next(4))→ 下延到 worldSurface → 0.6 框刷墙×2 → 0.5 框清空(塔内厅)。
491	 * 外门厅段(中心 = 主塔中心 + (dx1*0.6+dx2*0.55)*dir, Y + dy1/2 - dy2/2):
492	 * 0.6±Next(1,3) 只填远侧半(dx2*0.5 内)→ 下延(全列刷墙)→ 0.5 边缘垛口+顶齿 →
493	 * 0.6 框清墙 → **0.5 框 active=false+wall=0(开放门厅,老头 NPC 位)** →
494	 * 100 列砖坡(对角步降) → 条纹窗墙(2-5 刷-2 倍跳) → 门洞 15×3+门 style13。 */
495	function dungeonEnt(st: TileStore, rng: RNG, gs: GenState, dc: DungeonCtx, i: number, j: number): void {
496	  // 清 ±60 液体
497	  for (let x = i - 60; x < i + 60; x++) {
498	    for (let y = j - 60; y < j + 60; y++) {
499	      if (!st.inBounds(x, y)) continue;
500	      st.liquid[st.idx(x, y)] = 0;
501	    }
502	  }
503	  const dx1 = rng.int(25, 29) + 0.0, dy1 = rng.int(20, 24) + 0.0;
504	  let cx = i + 0.0, cy = j - dy1 / 2; // 塔中心(vanilla vector2)
505	  dc.minYY = Math.floor(cy);
506	  const dir = i > st.w / 2 ? -1 : 1; // num2:背向地图中心
507	  const isDW = (x: number, y: number) => st.inBounds(x, y) && dc.isDungeonWall(st, x, y);
508	  const fillB = (x: number, y: number, paintWall: boolean) => {
509	    if (!st.inBounds(x, y)) return;
510	    const ti = st.idx(x, y);
511	    st.liquid[ti] = 0;
512	    if (!isDW(x, y)) {
513	      st.wall[ti] = 0;
514	      if (paintWall) st.wall[ti] = dc.wall;
515	      st.type[ti] = dc.brick; st.flags[ti] = 1;
516	    }
517	  };
518	  const extFill = (x: number, y: number, wallAll: boolean, innerW: boolean) => {
519	    if (!st.inBounds(x, y)) return;
520	    const ti = st.idx(x, y);
521	    st.liquid[ti] = 0;
522	    if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
523	    if (wallAll || innerW) st.wall[ti] = dc.wall;
524	  };
525	  // ---- 主塔段主体(num3..num6)----
526	  const l1 = Math.floor(cx - dx1 * 0.6 - rng.int(2, 4));
527	  const r1 = Math.floor(cx + dx1 * 0.6 + rng.int(2, 4));
528	  const t1 = Math.floor(cy - dy1 * 0.6 - rng.int(2, 4));
529	  const b1 = Math.floor(cy + dy1 * 0.6 + rng.int(8, 15));
530	  for (let x = l1; x < r1; x++) {
531	    for (let y = t1; y < b1; y++) {
532	      fillB(x, y, x > l1 + 1 && x < r1 - 2 && y > t1 + 1 && y < b1 - 2);
533	    }
534	  }
535	  // 垛口(左右块 5+Next(4) 宽、3+Next(3) 高)
536	  for (const sd of [-1, 1]) {
537	    const bx0 = sd < 0 ? l1 : r1 - 5 - rng.int(0, 3);
538	    const bx1 = sd < 0 ? l1 + 5 + rng.int(0, 3) : r1;
539	    const by0 = t1 - 3 - rng.int(0, 2);
540	    for (let x = bx0; x < bx1; x++) for (let y = by0; y < t1; y++) fillB(x, y, false);
541	  }
542	  // 顶齿(齿高 1+Next(2),周期 2+Next(4):刷 num16 列跳 num16 列)
543	  const th1 = 1 + rng.int(0, 1);
544	  const tp1 = 2 + rng.int(0, 3);
545	  let cnt = 0;
546	  for (let x = l1; x < r1; x++) {
547	    for (let y = t1 - th1; y < t1; y++) fillB(x, y, false);
548	    if (++cnt >= tp1) { x += tp1; cnt = 0; }
549	  }
550	  // 下延到 worldSurface(num6 → worldSurface):填砖,内列刷墙
551	  for (let x = l1; x < r1; x++) {
552	    for (let y = b1; y < Math.min(st.h, Math.floor(gs.worldSurface)); y++) {
553	      extFill(x, y, false, x > l1 && x < r1 - 1);
554	    }
555	  }
556	  // 0.6 框刷墙(精确,无抖动)×2
557	  for (let pass = 0; pass < 2; pass++) {
558	    for (let x = Math.floor(cx - dx1 * 0.6) - (pass ? 1 : 0); x <= Math.floor(cx + dx1 * 0.6) + (pass ? 1 : 0); x++) {
559	      for (let y = Math.floor(cy - dy1 * 0.6) - (pass ? 1 : 0); y <= Math.floor(cy + dy1 * 0.6) + (pass ? 1 : 0); y++) {
560	        if (!st.inBounds(x, y)) continue;
561	        const ti = st.idx(x, y);
562	        st.liquid[ti] = 0; st.wall[ti] = dc.wall;
563	      }
564	    }
565	  }
566	  // 0.5 框清空(塔内厅)
567	  for (let x = Math.floor(cx - dx1 * 0.5); x < Math.floor(cx + dx1 * 0.5); x++) {
568	    for (let y = Math.floor(cy - dy1 * 0.5); y < Math.floor(cy + dy1 * 0.5); y++) {
569	      if (!st.inBounds(x, y)) continue;
570	      const ti = st.idx(x, y);
571	      st.liquid[ti] = 0; st.flags[ti] = 0; st.wall[ti] = dc.wall;
572	    }
573	  }
574	  // 塔底井口(连通楼梯竖井,原版由 DungeonStairs 自带)
575	  for (let x = -1; x <= 1; x++) {
576	    for (let y = Math.floor(cy + dy1 * 0.5); y < Math.floor(cy + dy1 * 0.5) + 4; y++) {
577	      if (st.inBounds(Math.floor(cx) + x, y)) {
578	        const ti = st.idx(Math.floor(cx) + x, y);
579	        st.flags[ti] = 0; st.wall[ti] = dc.wall;
580	      }
581	    }
582	  }
583	  // ---- 外门厅段 ----
584	  cx += dx1 * 0.6 * dir;
585	  cy += dy1 * 0.5;
586	  const dx2 = rng.int(35, 49) + 0.0, dy2 = rng.int(10, 14) + 0.0;
587	  cx += dx2 * 0.55 * dir;
588	  cy -= dy2 * 0.5;
589	  const l2 = Math.floor(cx - dx2 * 0.6 - rng.int(1, 2));
590	  const r2 = Math.floor(cx + dx2 * 0.6 + rng.int(1, 2));
591	  const t2 = Math.floor(cy - dy2 * 0.6 - rng.int(1, 2));
592	  const b2 = Math.floor(cy + dy2 * 0.6 + rng.int(6, 15));
593	  // 只填远侧半(num2<0 → x >= X-dx2*0.5;否则 x <= X+dx2*0.5-1)
594	  for (let x = l2; x < r2; x++) {
595	    for (let y = t2; y < b2; y++) {
596	      const far = dir < 0 ? x >= cx - dx2 * 0.5 : x <= cx + dx2 * 0.5 - 1;
597	      if (!far) continue;
598	      if (!st.inBounds(x, y)) continue;
599	      const ti = st.idx(x, y);
600	      st.liquid[ti] = 0;
601	      if (!isDW(x, y)) { st.wall[ti] = 0; st.type[ti] = dc.brick; st.flags[ti] = 1; }
602	    }
603	  }
604	  // 下延(全列刷墙)
605	  for (let x = l2; x < r2; x++) {
606	    for (let y = b2; y < Math.min(st.h, Math.floor(gs.worldSurface)); y++) extFill(x, y, true, false);
607	  }
608	  // 外段垛口(0.5 边缘:块1 从 num34(+1 若 dir<0) 起 5+Next(4) 宽;块2 [num35-5-Next(4), num35))
609	  const n34 = Math.floor(cx - dx2 * 0.5);
610	  let n35 = Math.floor(cx + dx2 * 0.5);
611	  const n36 = dir < 0 ? n34 + 1 : n34;
612	  {
613	    const by0 = t2 - 3 - rng.int(0, 2);
614	    for (let x = n36; x < n36 + 5 + rng.int(0, 3); x++) {
615	      for (let y = by0; y < t2; y++) {
616	        if (!st.inBounds(x, y)) continue;
617	        const ti = st.idx(x, y);
618	        st.liquid[ti] = 0;
619	        if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
620	      }
621	    }
622	    const bx0 = n35 - 5 - rng.int(0, 3);
623	    for (let x = bx0; x < n35; x++) {
624	      for (let y = by0; y < t2; y++) {
625	        if (!st.inBounds(x, y)) continue;
626	        const ti = st.idx(x, y);
627	        st.liquid[ti] = 0;
628	        if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
629	      }
630	    }
631	  }
632	  // 外段顶齿(dir<0 时 num35++)
633	  if (dir < 0) n35++;
634	  const th2 = 1 + rng.int(0, 1);
635	  const tp2 = 2 + rng.int(0, 3);
636	  cnt = 0;
637	  for (let x = n34 + 1; x < n35 - 1; x++) {
638	    for (let y = t2 - th2; y < t2; y++) {
639	      if (!st.inBounds(x, y)) continue;
640	      const ti = st.idx(x, y);
641	      st.liquid[ti] = 0;
642	      if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
643	    }
644	    if (++cnt >= tp2) { x += tp2; cnt = 0; }
645	  }
646	  // 0.6 框清墙(开放感)
647	  for (let x = Math.floor(cx - dx2 * 0.6); x < Math.floor(cx + dx2 * 0.6); x++) {
648	    for (let y = Math.floor(cy - dy2 * 0.6); y < Math.floor(cy + dy2 * 0.6); y++) {
649	      if (!st.inBounds(x, y)) continue;
650	      st.liquid[st.idx(x, y)] = 0;
651	      st.wall[st.idx(x, y)] = 0;
652	    }
653	  }
654	  // 0.5 框:active=false + wall=0(开放门厅——老头 NPC 位)
655	  const n51 = Math.floor(cx - dx2 * 0.5), n52 = Math.floor(cx + dx2 * 0.5);
656	  const n53 = Math.floor(cy - dy2 * 0.5), n54 = Math.floor(cy + dy2 * 0.5);
657	  for (let x = n51; x < n52; x++) {
658	    for (let y = n53; y < n54; y++) {
659	      if (!st.inBounds(x, y)) continue;

```


---

## 🤖 Assistant · 2026-08-11T04:10:34.784Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Dungeon entrance (dungeonEnt): the tower is built around cy = j - dy1/2 where j = surface. dy1 = 20-24, so cy ≈ surface - 10..12; t1 = cy - dy1*0.6 - 2..4 ≈ surface - 25..30; the tower rises ~25-30 tiles ABOVE the surface into the sky (real bricks, flags=1). This is the intended vanilla dungeon entrance tower. Sky writer (legit).

Now, everything gathered. I should also check:
- HiveSpiderPass (webs "全局天花板蛛网" — runWebsPass "58 Webs(全局天花板蛛网 runner 51)" — webs hang from cave ceilings; might be above surface? Let me check).
- TemplePass (jungle temple is underground).
- HellFortPass (hell only).
- TrapsPass — y ≥ worldSurface (line 86: top < worldSurface return false; line 301: y from worldSurface). OK.
- Spread.ts

Let me quickly check HiveSpiderPass webs and Spread.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:35.440Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla && grep -n \"worldSurface\\|rockLevel\\|rng.int(0, st.h\\|rng.int(1, st.h\\|rng.int(2, st.h\" HiveSpiderPass.ts Spread.ts | head -40",
 "description": "Grep HiveSpider and Spread for y anchors"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:35.479Z

**📎 ToolResult**

```
HiveSpiderPass.ts:42:          if (y < gs.worldSurface && st.inBounds(x, y - 5) && st.wall[st.idx(x, y - 5)] === 0) next2 = 0;
HiveSpiderPass.ts:105:  const yMin = Math.floor((gs.worldSurface + gs.rockLevel) / 2);
HiveSpiderPass.ts:325:      if (cy < gs.worldSurface + rng.int(0, 4)) continue;
HiveSpiderPass.ts:366:  const yMin = Math.floor((gs.worldSurface + gs.rockLevel) / 2);
HiveSpiderPass.ts:388:    for (let j = Math.floor(gs.worldSurface); j < st.h - 100; j++) {
HiveSpiderPass.ts:426:    let num = rng.int(Math.floor(gs.worldSurfaceHigh), st.h - 21);
HiveSpiderPass.ts:431:    if (!(num > gs.worldSurface || st.wall[st.idx(j, num)] > 0)) continue;
HiveSpiderPass.ts:432:    while (num > Math.floor(gs.worldSurfaceLow) && !st.flags[st.idx(j, num)]) num--;
HiveSpiderPass.ts:438:    if (!(num > gs.worldSurface || st.wall[st.idx(j, num)] > 0)) continue;

```


---

## 🤖 Assistant · 2026-08-11T04:10:35.627Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/Spread.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:35.647Z

**📎 ToolResult**

```
1	// 原版 WorldGen.SpreadGrass 移植(WorldGen.cs:45236)——生成期草皮传播。
2	// 泥/石完全被包住(3×3 全实心)不转;岩浆邻接不转;向日葵上方不转腐化/猩红/神圣草。
3	import type { TileStore } from '../../TileStore';
4	import { T, TILE_BY_KEY, TILE_DEFS } from '../../../data/tiles';
5	import { NOT_CLEARABLE } from './TileRunner';
6	
7	/** 把 (x,y) 及相邻同源 tile 转 grass 类型;repeat=true 时 BFS 式向四周扩散 */
8	export function spreadGrass(st: TileStore, x: number, y: number, dirt: number, grass: number, repeat = true, depth = 0): void {
9	  if (depth > 400) return;
10	  if (!st.inBounds(x, y)) return;
11	  const i = st.idx(x, y);
12	  if (st.type[i] !== dirt) return;
13	  // 完全封闭(3×3 全实心)不转;岩浆邻接恒不转(cs L45269-45273:flag 强制 true)
14	  let enclosed = true;
15	  let lavaNear = false;
16	  for (let dx = -1; dx <= 1 && !lavaNear; dx++) {
17	    for (let dy = -1; dy <= 1; dy++) {
18	      const nx = x + dx, ny = y + dy;
19	      if (!st.inBounds(nx, ny)) continue;
20	      const j = st.idx(nx, ny);
21	      if (st.liquidType[j] === 2 && st.liquid[j] > 0) { lavaNear = true; break; }
22	      if (dx === 0 && dy === 0) continue;
23	      if ((!st.flags[j] || !TILE_DEFS[st.type[j]]?.solid)) enclosed = false;
24	    }
25	  }
26	  if (lavaNear) return;
27	  if (enclosed) return;
28	  // 原版:CanBeClearedDuringGeneration 为 false 的泥(沙漠沙岩族等)不转
29	  if (NOT_CLEARABLE.has(st.type[i])) return;
30	  st.type[i] = grass;
31	  if (!repeat) return;
32	  for (let dx = -1; dx <= 1; dx++) {
33	    for (let dy = -1; dy <= 1; dy++) {
34	      if (dx === 0 && dy === 0) continue;
35	      const nx = x + dx, ny = y + dy;
36	      if (!st.inBounds(nx, ny)) continue;
37	      const ni = st.idx(nx, ny);
38	      if (st.type[ni] === dirt) spreadGrass(st, nx, ny, dirt, grass, true, depth + 1);
39	    }
40	  }
41	}
42	
43	/** 全图传播(对应原版逐 tile 调用 SpreadGrass 的 pass,如 Mud Caves To Grass)。
44	 * centerX/maxDist 可选:仅转换距中心 maxDist 内的泥(参考世界正是泥迹全图、
45	 * 丛林草紧贴丛林核心——远离核心的泥保持泥色) */
46	export function spreadGrassAll(st: TileStore, dirt: number, grass: number, centerX = -1, maxDist = 0): void {
47	  for (let y = 0; y < st.h; y++) {
48	    for (let x = 0; x < st.w; x++) {
49	      if (centerX >= 0 && Math.abs(x - centerX) > maxDist) continue;
50	      if (st.type[st.idx(x, y)] === dirt) spreadGrass(st, x, y, dirt, grass, false);
51	    }
52	  }
53	  // 单格不扩散传播力弱,重复两轮让草皮连通。
54	  // 关键:必须以"轮初快照"判定邻草——同轮内边扫边转会在扫描方向上链式雪崩,
55	  // 把整条连通泥网全部转成草(丛林"全草无泥"与远程草带的根因)
56	  for (let round = 0; round < 2; round++) {
57	    const targets: number[] = [];
58	    for (let y = 0; y < st.h; y++) {
59	      for (let x = 0; x < st.w; x++) {
60	        const i = st.idx(x, y);
61	        if (st.type[i] !== dirt) continue;
62	        let touch = false;
63	        for (let dx = -1; dx <= 1 && !touch; dx++) {
64	          for (let dy = -1; dy <= 1; dy++) {
65	            if (!st.inBounds(x + dx, y + dy)) continue;
66	            if (st.type[st.idx(x + dx, y + dy)] === grass) { touch = true; break; }
67	          }
68	        }
69	        if (touch) targets.push(i);
70	      }
71	    }
72	    for (const i of targets) st.type[i] = grass;
73	  }
74	  void T; void TILE_BY_KEY;
75	}
76	

```


---

## 🤖 Assistant · 2026-08-11T04:10:43.179Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
IMPORTANT BUG DETECTOR: `spreadGrassAll` line 47-50: `if (st.type[st.idx(x,y)] === dirt) spreadGrass(...)` — this checks `type` WITHOUT checking `flags`! Ghost mud cells (type=mud, flags=0) created by TileRunner in the AIR/SKY will be converted to jungle grass / mushroom grass via `st.type[i] = grass` — again ghost (no flags set). But `spreadGrass` line 12 checks `st.type[i] !== dirt` and then line 23 checks neighbors' flags for "enclosed": for a ghost cell surrounded by air (all !flags), enclosed = false → proceeds → converts type to grass. And in spreadGrassAll's rounds 2-3 (lines 56-73): targets = cells whose type is dirt AND neighbor type is grass — again purely type-based, no flags. So ghost mud in sky → ghost grass in sky. All still ghosts (flags=0) → erased at finalize. But it SPREADS the ghost pollution widely across the sky!

Wait, does it set flags? No — only `st.type[i] = grass`. So ghosts remain ghosts.

Hmm, but wait: is the "mushroom grass" spread run over the whole map (runMushroomPass line 62: spreadGrassAll(st, MUD, MUSH_GRASS) with no center limit) — converts ALL mud-typed cells (including ghost sky mud from the jungle giant runner? no, that's jungle region; but DirtToMud pass creates deep mud ghosts) to mushroom grass ghosts. And the jungle one is limited to ±0.21w of jungleCoreX.

OK. Now also check HiveSpiderPass runWebsPass line 426-438: webs placed at num from worldSurfaceHigh..h-21, with conditions `num > worldSurface || wall > 0`. Fine — below surface.

Now let me verify the TileStore setTileSilent semantics (does it set flags=1?) to confirm ghost vs real writes. Let me check TileStore.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:10:43.511Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"setTileSilent\\|setWallSilent\\|setLiquid\" ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts | head -20",
 "description": "Find TileStore silent setters"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:43.548Z

**📎 ToolResult**

```
109:  /** 唯一的写入入口（生成/导入期可绕过用 setTileSilent） */
140:  setTileSilent(x: number, y: number, type: number, frameX = 0, frameY = 0) {
160:  setWallSilent(x: number, y: number, wall: number) {
188:  setLiquid(x: number, y: number, amount: number, type: number) {

```


---

## 🤖 Assistant · 2026-08-11T04:10:45.062Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts",
 "limit": 80,
 "offset": 125
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:10:45.080Z

**📎 ToolResult**

```
125	    const i = this.idx(x, y);
126	    this.half[i] = v ? 1 : 0;
127	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetHalfBrick, x, y, v: v ? 1 : 0, fx: 0, fy: 0 });
128	    this.listeners.forEach((fn) => fn(x, y));
129	  }
130	
131	  setSlope(x: number, y: number, s: number) {
132	    if (!this.inBounds(x, y)) return;
133	    const i = this.idx(x, y);
134	    this.slope[i] = s;
135	    this.half[i] = 0; // 原版 SlopeTile 无条件 halfBrick(false)（WorldGen.cs:49174），slope=0 复位时同样
136	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetSlope, x, y, v: s, fx: 0, fy: 0 });
137	    this.listeners.forEach((fn) => fn(x, y));
138	  }
139	
140	  setTileSilent(x: number, y: number, type: number, frameX = 0, frameY = 0) {
141	    if (!this.inBounds(x, y)) return;
142	    const i = this.idx(x, y);
143	    this.type[i] = type;
144	    this.flags[i] = type !== 0 ? 1 : 0;
145	    this.frameX[i] = frameX;
146	    this.frameY[i] = frameY;
147	    if (type === 0) { this.half[i] = 0; this.slope[i] = 0; } // 挖除同步清位（防生成期脏残留）
148	  }
149	
150	  setWall(x: number, y: number, wall: number) {
151	    if (!this.inBounds(x, y)) return;
152	    const i = this.idx(x, y);
153	    if (this.wall[i] !== wall) {
154	      this.wall[i] = wall;
155	      if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetWall, x, y, v: wall, fx: 0, fy: 0 });
156	      this.listeners.forEach((fn) => fn(x, y));
157	    }
158	  }
159	
160	  setWallSilent(x: number, y: number, wall: number) {
161	    if (!this.inBounds(x, y)) return;
162	    this.wall[this.idx(x, y)] = wall;
163	  }
164	
165	  /** 导线/致动位写入（Wiring 系统）。不发 listeners：导线不进 chunk 烘焙画布，
166	   *  走 Renderer 动态覆盖层；致动位变化才需要标脏 chunk（调用方负责） */
167	  setWire(x: number, y: number, bits: number) {
168	    if (!this.inBounds(x, y)) return;
169	    this.wire[this.idx(x, y)] = bits & 63;
170	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetWire, x, y, v: bits & 63, fx: 0, fy: 0 });
171	  }
172	
173	  setWireSilent(x: number, y: number, bits: number) {
174	    this.setWire(x, y, bits);
175	  }
176	
177	  /** 致动器翻转 inActive 态（Wiring.DeActive/ReActive 用）：影响碰撞与渲染，须发 listeners */
178	  setActuated(x: number, y: number, v: boolean) {
179	    if (!this.inBounds(x, y)) return;
180	    const i = this.idx(x, y);
181	    const b = v ? (this.wire[i] | TileStore.WIRE_ACTUATED) : (this.wire[i] & ~TileStore.WIRE_ACTUATED);
182	    if (this.wire[i] === b) return;
183	    this.wire[i] = b;
184	    if (this.netReporter && !this.netSuppress) this.netReporter({ a: TileOpAction.SetActuated, x, y, v: v ? 1 : 0, fx: 0, fy: 0 });
185	    this.listeners.forEach((fn) => fn(x, y));
186	  }
187	
188	  setLiquid(x: number, y: number, amount: number, type: number) {
189	    if (!this.inBounds(x, y)) return;
190	    const i = this.idx(x, y);
191	    const a = Math.max(0, Math.min(255, amount | 0));
192	    if (this.liquid[i] === a && this.liquidType[i] === type) return;
193	    this.liquid[i] = a;
194	    this.liquidType[i] = type;
195	    this.liquidListeners.forEach((fn) => fn(x, y));
196	  }
197	}
198	

```


---

## 🤖 Assistant · 2026-08-11T04:11:15.342Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: `setTileSilent` sets flags=1 for type≠0 (real blocks). Direct `st.type[i] = X` writes without flags are ghost writes.

So sky writers split into:
A. Ghost-type writers into sky air (type set, flags stays 0) — invisible, purged at finalize:
   - TileRunner with type≥0, addTile=false, overRide=true (default): writes `st.type[ti] = type` into ANY cell including air (TileRunner.ts:121-142). All placing runners whose y-range touches sky:
     * CavesPass Rocks In Dirt band yMin=0 (CavesPass.ts:25), Clay band yMin=0 (CavesPass.ts:36)
     * ShiniesPass silver "sky band" yMin=0 (ShiniesPass.ts:44), gold near-surface yMin=0 (ShiniesPass.ts:47)
     * JunglePass giant mud runner (JunglePass.ts:65): strength 400-600*1.5scale, steps 10000, speedY=-20, noYChange — vertical mud column from (h+rockLevel)/2 up to y<0, covering jungle sky with ghost MUD types + mudWall walls (walls written for y > gs.worldSurface only — line 93 `y > gs.worldSurface`, so sky walls not written by mudWall; but `noYChange && y < gs.worldSurface && type !== MUD` n/a for mud).
     * GrassPass seeds above surface (y2 ∈ [0, worldSurfaceLow-1]) — no-op in sky unless surrounded by dirt.
     * IceBiome/Slush/Corruption convertSurface — skip !flags so no ghost creation, they only rewrite type of ACTIVE tiles (though they don't clear... fine).
   - CorruptionPass chasmRunner/chasmRunnerSideways: `st.flags[ti] = 0` (KillTile) leaving type → ghosts underground; and `st.type[ti] = EBONSTONE` written in shell loops WITHOUT flags in some branches (line 307: `if (st.type[ti] !== ORB) st.type[ti] = EBONSTONE;` — that's inside the first shell loop where flags may not be set... Actually line 305-307: first sets flags=1 if conditions, then always writes type. So ghost ebonstone possible in air cells within radius*1.1 of the chasm — mostly underground though (chasm starts below surface).
   - MushroomPass shroomPatch line 90: `st.type[ti] = MUD` without flags (except first ring) — deep underground.
   - spreadGrassAll / spreadGrass: `st.type[i] = grass` without flags check — converts ghost mud (in sky, from jungle runner) to ghost grass. Also jungle mud→jungle grass limited to ±0.21w of core; mushroom mud→mushroom grass FULL MAP (Spread.ts:46-73 checks type only, no flags).

B. Real (flags=1) sky writers — intentional content, never erased:
   - MountCavesPass.mountinater (MountCavesPass.ts:18-51): dirt hills above surface (~40-54 tiles up), via setTileSilent only in air cells.
   - FloatingIslands (StructuresPass.ts:22-57, 123-213): cloud/rain-cloud islands at y ∈ [90, worldSurfaceLow-50]; + IslandHousePass sunplate houses in sky.
   - TreePass: trees grow up from surface into sky (trunk y = index1-height .. index1, height 5-16; epic 20-29; palm 10-20) — TreePass.ts:53-99, 121-125.
   - surfacePass plants (WorldGen.ts:798-823): grass/flowers 1 tile above surface; also writes at any y where a solid tile exists (loops y=1..h) — could place plants above floating islands/mount hills? It places above grass-family tiles only — on floating island dirt tops? Islands' dirt core converted? They're dirt (cloud islands have dirt core) — the loop `for y=1..h` finds the FIRST solid tile per column — for island columns that's the island top → plants on islands. OK not "junk".
   - Dungeon entrance tower (DungeonPass.ts:488-655): rises ~25-35 tiles above surface with real bricks.
   - Desert dune mound (DesertPass.ts:59-87): real sand column from moundSurfY (above original surface) down; plus clears sky cells above the dune (lines 72-78: from sy-1 down... wait `for (let y = sy - 1; y < flatten && y >= 0; y--)` — clears tiles above the dune surface → removes any hill blocks in sky above the dune).
   - Corruption/Crimson crater: crimStart pockets (CorruptionPass.ts:486-533) write real CRIMSTONE up to ~20 tiles above the surface (the crater mounds); chasm runner EBONSTONE shells.
   - halfBrickSmoothPass corner-fill (HalfBrickPass.ts:105-119): writes real belowType blocks (setTileSilent) into air corners above solid ground — including just above surface → sky blocks at y = surface-1 (with half brick). Also deletes tiles (SmoothWorld lines 84-96, 101-103).
   - hellPass: y > h-190 only; no sky.
   - liquidPass → vanillaLakes: Lakes dig below surface (y from worldSurfaceLow-20 downward); the funnel entrance carves to y > worldSurfaceLow-20 — slightly above surfaceLow but that's the lake mouth. No sky water. Note: TileRunner type -2 fills liquid only in active cells. digTunnel wet fills liquid in carved cells below surface.

C. Erasers (抹除):
   1. finalize (WorldGen.ts:897-903): global purge — `if (!flags[i] && type[i] !== 0) type[i] = 0` (ghost purge) + `if (type[i] === 0) flags[i] = 0`. This erases ALL ghost sky junk at the very end. THIS is the main "后期抹除".
   2. finalize spawn clearing (WorldGen.ts:937-949, 967-971): clears 3×3 + 5×5 above spawn.
   3. vanillaCleanup (CleanupPass.ts:14-53): (a) clears natural walls above surface (2/40/64/86) for y < worldSurface — sky wall cleanup; (b) removes connected clumps < 20 solid tiles (scanTileColumnAndRemoveClumps, y from 10 to h-10 — includes sky!) → removes small floating sky debris (including mount hill fragments, floating island fragments < 20 tiles!). Note this runs BEFORE halfBrick/life crystals.
   4. floatCleanupPass (WorldGen.ts:640-660) — LEGACY ONLY (lgcTerrain=false): strips unsupported dirt/stone/grass below surfY+2 — doesn't touch sky above surface.
   5. SmoothWorld (HalfBrickPass.ts:49-139): deletes protruding/hanging blocks (setTileSilent 0) across whole map including sky region (j from 20 to h-20).
   6. DesertPass lines 72-78: clears above-dune sky cells.
   7. BeachesPass: clears ocean basin (y from 0) — removes everything above basin floor in ocean columns (sky already air; but removes land).
   8. SwordShrine shaft clears from sy+5 up to worldSurface-2 (SwordShrinePass.ts:79-84).
   9. ShiniesPass sandArch (88-115): moves floating sand — anti-floating cleanup.
   10. hellPass: overwrites everything below h-160 with ash/air — the "地狱箱被 hellPass 100% 抹除" note (WorldGen.ts:77-79 comment).
   11. potPass? No.

Also legacy structurePass: huts at hy ∈ [0.45h, h-40] (underground); scattered chests y from surface+8 downward (WorldGen.ts:852-866). buildHut clears 9×6 and builds wood — underground. No sky writes in legacy structurePass. Note: legacy surfacePass (WorldGen.ts:758-826) writes grass conversion loop y < world.groundLevel-1 — above-ground region! It converts first-solid dirt to grass for y in [0, groundLevel) — that includes sky area but only touches already-solid tiles (flags check at 764). Then plants: loop y=1..h — writes plants 1 above any grass-family tile, including in sky if such tiles exist there (islands). OK.

Legacy terrainPass (fbm fallback): surface[x] = base(0.28h) + noise; fills from sy downward; ocean carve; snow; no sky blocks. Legacy cavePass carves from sy+6 downward. So legacy pipeline writes essentially NOTHING into the sky except via structurePass/surfacePass trees (which in legacy mode... wait, surfacePass calls runTreePass only `if (gs)` — in legacy mode ctxGs[0] is null → no trees! So legacy has NO trees). And floatCleanupPass only below surfY+2. Legacy pipeline: no sky junk at all.

Hmm — one more important check: does vanillaBiomes' runFloatingIslandsPass run BEFORE hellPass etc. Yes (pass 4 生物群系). And the user asked specifically: "生成早期往天空写入大量杂块、后期又被抹除" — the best candidates:

(a) Ghost types from TileRunner placing passes with yMin=0 (Rocks In Dirt, Clay, Shinies silver/gold sky bands) + jungle giant mud runner + grass spreading — all purged at finalize (WorldGen.ts:900-903). Massive in count (e.g. area*0.00015 runners of strength 4-14 × steps 5-39 wandering in sky; silver band area*1.7e-4 runners strength 4-8; each runner paints a diamond of radius ~strength/2 per step over ~steps steps).

(b) CleanupPass clump removal (y from 10) — removes small real sky fragments.

Wait — but there's one more candidate I should double check: is there anything that writes REAL blocks into the sky early that gets erased later? The user's phrasing "写入大量杂块、后期又被抹除" suggests observed: sky had many blocks during early passes, gone at end. That is EXACTLY the ghost-type mechanism IF the partial preview renderer draws cells by type without checking flags. Let me check how the preview renderer decides to draw — check Renderer or minimap: do they check flags? Let me grep quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:11:15.743Z · glm-x-preview-260804

```
Let me check how rendering/preview treats cells with type but no flags (ghosts), since that determines whether ghost sky blocks are visible mid-generation.
```


---

## 🤖 Assistant · 2026-08-11T04:11:16.364Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -rn \"onWorldPartial\" --include=\"*.ts\" --include=\"*.tsx\" | head; grep -rln \"flags\\[\" world/Renderer* render* 2>/dev/null | head",
 "description": "Find partial preview consumers"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:11:16.408Z

**📎 ToolResult**

```
mainFlow.ts:470:        onWorldPartial: (world) => loadState.attachWorld(world), // 主线程 fallback：列扫描预览
core/Game.ts:405:  async newWorld(seedText: string, width: number, height: number, onProgress?: (label: string, p: number) => void, opts?: { name?: string; evil?: -1 | 0 | 1; onWorldPartial?: (world: import('../world/World').World, passIndex: number, passName: string) => void; /** worker 路径的降采样预览帧回调（位图模式） */ onPreview?: (f: import('../workers/WorldGenClient').PreviewFrame) => void }) {
core/Game.ts:434:    this.world = await generateWorld({ width, height, seedText, name: opts?.name, evil: opts?.evil, onWorldPartial: opts?.onWorldPartial }, (label, p) => onProgress?.(label, p * 0.7));
world/gen/WorldGen.ts:17:  onWorldPartial?: (world: World, passIndex: number, passName: string) => void;
world/gen/WorldGen.ts:93:    if (cfg.onWorldPartial) cfg.onWorldPartial(world, i, passes[i].name);
workers/protocol.ts:7:/** GenConfig 的纯数据投影：剥掉 onWorldPartial 回调（worker 内改发 preview 消息） */
workers/worldGen.worker.ts:31:          // 生成期实时预览：worker 侧降采样 RGBA → transfer（替代旧 onWorldPartial 整 world 回调）
workers/worldGen.worker.ts:32:          onWorldPartial: req.cfg.preview
vui/states/UIWorldLoadState.ts:61:  /** WorldGen.onWorldPartial 回调：挂上部分世界，开启实时预览（主线程 fallback 路径） */
(eval):1: no matches found: world/Renderer*

```


---

## 🤖 Assistant · 2026-08-11T04:11:17.833Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -rn \"\\.flags\\[\" --include=\"*.ts\" --include=\"*.tsx\" . | grep -v \"world/gen\\|world/TileStore\\|test\\|spec\" | head -30",
 "description": "Find flags consumers outside gen"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:11:17.870Z

**📎 ToolResult**

```
core/Game.ts:496:        if (st.flags[i]) {
core/Game.ts:741:    if (this.world.flags[savedFlag]) return false;
core/Game.ts:759:    if (flag) this.world.flags[flag] = true;
core/Game.ts:1198:          w.flags[downedKey] = true;
core/Game.ts:1230:          const p = w.flags['downedGoblins']
core/Game.ts:1238:          const p = w.flags['downedPirates'] ? 1 / 60 : 1 / 30;
core/Game.ts:1269:        if (inv.won === INVASION_GOBLIN) w.flags['downedGoblins'] = true;
core/Game.ts:1270:        else if (inv.won === INVASION_SNOW_LEGION) w.flags['downedFrost'] = true;
core/Game.ts:1271:        else if (inv.won === INVASION_PIRATE) w.flags['downedPirates'] = true;
core/Game.ts:2455:      st.inBounds(ax, ay) && ((st.flags[st.idx(ax, ay)] && st.type[st.idx(ax, ay)] !== 0) || st.wall[st.idx(ax, ay)] > 0);
core/Game.ts:3258:      if (!st.flags[i]) {
core/Game.ts:3685:        return !!(this.world.flags['downed_4'] || this.world.flags['downed_13']
core/Game.ts:3686:          || this.world.flags['downed_266'] || this.world.flags['downed_35']
core/Game.ts:3690:        return !!(this.world.flags['downed_35'] || this.world.flags.downedSkeletron);
core/Game.ts:3696:        return !!(this.world.flags['downed_125'] || this.world.flags['downed_126']
core/Game.ts:3697:          || this.world.flags['downed_127'] || this.world.flags['downed_134']);
core/Game.ts:3700:        return !!this.world.flags['downed_222'];
core/Game.ts:3703:        return !!this.world.flags.hardMode && !!this.world.flags['downed_262'];
core/Game.ts:3706:        return !!this.world.flags['downedPirates'];
core/Game.ts:3712:        return !!this.world.flags['bestiaryTenPercent'];
core/Game.ts:3728:        return !!this.world.flags['savedGoblin']; // 救援系统（bound NPC 解救）置位
core/Game.ts:3730:        return !!this.world.flags['savedWizard'];
core/Game.ts:3732:        return !!this.world.flags['savedMech'];
core/Game.ts:3734:        return !!this.world.flags['savedStylist'];
core/Game.ts:3736:        return !!this.world.flags['savedTaxCollector'];
core/Game.ts:3738:        return !!this.world.flags['savedGolfer'];
core/Game.ts:3914:    const boss1 = !!(w.flags['downed_4'] || w.flags.downedEyeOfCthulhu);
core/Game.ts:3915:    const boss2 = !!(w.flags['downed_13'] || w.flags['downed_266']);
core/Game.ts:3916:    const boss3 = !!(w.flags['downed_35'] || w.flags.downedSkeletron);
core/Game.ts:4720:        return !!st.flags[ii] && !st.half[ii] && st.slope[ii] === 0 && FIT_GRASS.has(st.type[ii]);

```


---

## 🤖 Assistant · 2026-08-11T04:11:20.381Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me check the worker preview renderer — does it draw cells based on type or flags? workers/worldGen.worker.ts and WorldGenClient.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:11:20.574Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && sed -n 1,120p workers/worldGen.worker.ts",
 "description": "Read worker preview downsample code"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:11:20.606Z

**📎 ToolResult**

```
// 世界生成/存档解析 worker：generate（生成+沉降一条链）与 saveParse（读档解析+沉降）。
// 全程纯计算（generateWorld/settleWorldLiquids/loadSaveData 均无 DOM 依赖），
// 结果 packWorld 转移所有权回传。错误按请求 id 回传，绝不静默 pending。
/// <reference lib="webworker" />
import { generateWorld } from '../world/gen/WorldGen';
import { settleWorldLiquids } from '../world/liquid/settle';
import { packWorld } from './worldPacket';
import { renderPreviewBitmap } from './previewBitmap';
import { loadSaveData } from '../save/SaveFile';
import { kvGetIdb } from '../save/KvStore';
import type { WorldWorkerRequest, WorldWorkerEvent } from './protocol';

const ctx = self as unknown as {
  postMessage(msg: WorldWorkerEvent, transfer?: Transferable[]): void;
  onmessage: ((e: MessageEvent<WorldWorkerRequest>) => void) | null;
};

ctx.onmessage = async (e) => {
  const req = e.data;
  try {
    if (req.type === 'ping') {
      ctx.postMessage({ id: req.id, type: 'ready' });
      return;
    }
    if (req.type === 'generate') {
      const world = await generateWorld(
        {
          width: req.cfg.width, height: req.cfg.height, seedText: req.cfg.seedText,
          name: req.cfg.name, structures: req.cfg.structures, evil: req.cfg.evil,
          ...(req.cfg.lgcTerrain !== undefined ? { lgcTerrain: req.cfg.lgcTerrain } : {}),
          // 生成期实时预览：worker 侧降采样 RGBA → transfer（替代旧 onWorldPartial 整 world 回调）
          onWorldPartial: req.cfg.preview
            ? (w, passIndex, passName) => {
              const f = renderPreviewBitmap(w.store);
              ctx.postMessage(
                { id: req.id, type: 'preview', passIndex, passName, width: f.width, height: f.height, rgba: f.rgba.buffer as ArrayBuffer },
                [f.rgba.buffer],
              );
            }
            : undefined,
        },
        (label, p) => ctx.postMessage({ id: req.id, type: 'progress', phase: 'generate', label, p }),
      );
      await settleWorldLiquids(world, 'gen',
        (p) => ctx.postMessage({ id: req.id, type: 'progress', phase: 'settle', label: '水体沉降', p }));
      const { packet, transfer } = packWorld(world); // 转移所有权（本分支最后一步）
      ctx.postMessage({ id: req.id, type: 'result', world: packet }, transfer);
      return;
    }
    if (req.type === 'saveParse') {
      // 三源：key=worker 内直读 IDB（主路径，免大字符串 clone）；json=小档/调试；save=.wld 导入
      const data = req.save
        ? req.save
        : JSON.parse(req.json ?? (await kvGetIdb(req.key ?? '')) ?? 'null') as import('../save/SaveFile').SaveData | null;
      if (!data) throw new Error('存档数据缺失');
      ctx.postMessage({ id: req.id, type: 'progress', phase: 'parse', p: 0.3 });
      const { world, player } = loadSaveData(data);
      await settleWorldLiquids(world, 'load',
        (p) => ctx.postMessage({ id: req.id, type: 'progress', phase: 'settle', label: '水体沉降', p: 0.3 + p * 0.5 }));
      const { packet, transfer } = packWorld(world);
      ctx.postMessage({ id: req.id, type: 'result', world: packet, player }, transfer);
      return;
    }
  } catch (err) {
    ctx.postMessage({
      id: req.id, type: 'error',
      message: err instanceof Error ? `${err.message}` : String(err),
      stack: err instanceof Error ? err.stack : undefined,
    });
  }
};

```


---

## 🤖 Assistant · 2026-08-11T04:11:22.494Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && cat workers/previewBitmap.ts 2>/dev/null | head -80",
 "description": "Read preview bitmap renderer"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:11:22.530Z

**📎 ToolResult**

```
// 生成期实时预览的降采样 RGBA 位图（worker 侧渲染，transfer 回主线程 putImageData）。
// 预览控件显示宽度上限 ~520 CSS px（GenWorldPreview），maxW=640 已超显示分辨率；
// 全量 type 数组每 pass 34MB 拷贝不可接受——此处直接在 worker 着色输出 RGBA。
import type { TileStore } from '../world/TileStore';
import { mapColor24 } from '../render/MapColors';

/** 降采样：每个输出像素取源格 (x*fx, y*fy) 的 mapColor24（tile>liquid>wall 优先级，
 *  MapColors.mapColor24 已封装）。中世界 6400×1800 → 640×180×4 ≈ 460KB/帧 */
export function renderPreviewBitmap(st: TileStore, maxW = 640): {
  width: number; height: number; rgba: Uint8ClampedArray;
} {
  const fx = Math.max(1, Math.ceil(st.w / maxW));
  const fy = fx; // 保持纵横比
  const width = Math.floor(st.w / fx);
  const height = Math.floor(st.h / fy);
  const rgba = new Uint8ClampedArray(width * height * 4);
  for (let oy = 0; oy < height; oy++) {
    for (let ox = 0; ox < width; ox++) {
      const c = mapColor24(st, ox * fx, oy * fy);
      const i = (oy * width + ox) * 4;
      rgba[i] = (c >> 16) & 255;
      rgba[i + 1] = (c >> 8) & 255;
      rgba[i + 2] = c & 255;
      rgba[i + 3] = 255;
    }
  }
  return { width, height, rgba };
}

```


---

## 🤖 Assistant · 2026-08-11T04:11:24.614Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"mapColor24\" -A 30 render/MapColors.ts | head -50",
 "description": "Read mapColor24 priority logic"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:11:24.650Z

**📎 ToolResult**

```
29:export function mapColor24(st: TileStore, x: number, y: number): number {
30-  const i = st.idx(x, y);
31-  const t = st.type[i];
32-  if (t !== 0) {
33-    const c = TILE_COLORS.get(t);
34-    return c !== undefined ? c : UNKNOWN;
35-  }
36-  if (st.liquid[i] > 40) return st.liquidType[i] === 2 ? LAVA : WATER;
37-  const w = st.wall[i];
38-  if (w !== 0) {
39-    const c = WALL_COLORS.get(w);
40-    return c !== undefined ? c : UNKNOWN_WALL;
41-  }
42-  return SKY;
43-}

```


---

## 🤖 Assistant · 2026-08-11T04:11:28.798Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
CONFIRMED AND CRITICAL: `mapColor24` (render/MapColors.ts:29-43) colors a cell by `type` alone — it does NOT check `flags`! So ghost cells (type != 0, flags == 0) ARE VISIBLE in the generation-time preview as colored blocks. This explains the user's observation perfectly: during early passes, the sky (y < groundLevel) shows large amounts of "杂块" (ghost stone/ore/mud/grass types painted by TileRunner and spread passes into air), and after finalize (WorldGen.ts:900-903) they are zeroed → sky appears clean.

Also, the main game renderer might also draw by type — let me quickly verify whether the in-game renderer checks flags, to note whether ghosts would be visible in-game too (they're purged at finalize, so no). Not necessary but useful: check render chunk baking. Let me grep quickly for how the tile renderer decides visibility.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:11:29.225Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -rn \"flags\" render/*.ts | grep -i \"idx\\|\\[i\\]\" | head -15",
 "description": "Check main renderer flags usage"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:11:29.272Z

**📎 ToolResult**

```
render/ChunkCache.ts:160:    const same = (nx: number, ny: number) => st.inBounds(nx, ny) && st.flags[st.idx(nx, ny)] && st.type[st.idx(nx, ny)] === type ? 1 : 0;
render/ChunkCache.ts:223:        if (type === 0 || !st.flags[i]) continue;
render/VanillaWallTiler.ts:83:    if (st.flags[i] && truncates.includes(st.type[i])) return true;
render/VanillaLiquidRenderer.ts:344:      if (!st.flags[i]) continue; // 空格没有"方块后面"
render/WaterfallRenderer.ts:51:        if (!st.flags[i] || !st.half[i]) continue;          // active && halfBrick（L102）

```


---

## 🤖 Assistant · 2026-08-11T04:11:31.392Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: the in-game chunk renderer (ChunkCache.ts:223) requires `flags` — so ghosts are invisible in-game; only the generation preview (mapColor24, type-only) shows them. 

Now I have a complete picture. Let me also double-check the `lgcTerrain` config source to describe the branch. grep for lgcTerrain usage.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:11:31.926Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -rn \"lgcTerrain\" --include=\"*.ts\" --include=\"*.tsx\" . | grep -v \"world/gen/WorldGen.ts\\|workers/worldGen.worker\" | head -10",
 "description": "Find lgcTerrain config source"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:11:31.971Z

**📎 ToolResult**

```
workers/protocol.ts:16:  lgcTerrain?: boolean;

```


---

## 🤖 Assistant · 2026-08-11T04:11:46.751Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`lgcTerrain` is only in protocol.ts and WorldGen.ts — no UI sets it, so default is vanilla terrain (lgcTerrain !== false). The legacy fbm path is dead code unless explicitly requested via worker protocol.

Now let me compile the final report. I have all the evidence. Let me organize:

## 1. Pass list & order (WorldGen.ts:49-86)

Vanilla branch (default, lgcTerrain !== false):
1. 原版地形 vanillaTerrain (WorldGen.ts:133) — Reset dice + runTerrainPass; legacy wrapper
2. 洞穴 vanillaCaves (WorldGen.ts:209) — runOceanSandPass(3), runMountCavesPass(7), runRocksAndClayPass(8-10), runCavesPass(11-14+e Caverer)
3. 海滩 vanillaBeaches (WorldGen.ts:218) — runMountainCavesPass(34), runBeachesPass(33)
4. 生物群系 vanillaBiomes (WorldGen.ts:232) — long chain (list below)
5. 矿石 vanillaShinies (WorldGen.ts:202) — runShiniesPass(27)
6. 液体 vanillaLakes (WorldGen.ts:194) — runLakesPass(31) + runGemsPass(36)
7. 清理 vanillaCleanup (WorldGen.ts:282) — runCleanupPass(37)
8. 生命水晶 vanillaLifeCrystals (WorldGen.ts:289) — pass 55
9. 半砖平滑 halfBrickSmoothPass (WorldGen.ts:296) — Smooth World L7568
10. 瀑布唇缘 waterfallLipPass (WorldGen.ts:303) — Waterfalls L7697
11. 地狱 hellPass (WorldGen.ts:546) — legacy own implementation (Underworld)
12. 地狱屋 vanillaHellHouses (WorldGen.ts:310) — runHellFortPass
13. 地狱箱 underworldChestsPass (WorldGen.ts:317)
14. 瓦罐 potPass (WorldGen.ts:663) — legacy own (vanilla 1:1 semantics, Pots cs:18186)
15. 矿骨堆 pilesPass (WorldGen.ts:324) — legacy wrapper of pass 77
16. 表面 surfacePass (WorldGen.ts:758) — legacy: grass + runTreePass(82) + plants (pass 86-ish)
17. 地表装饰 vanillaSurfaceDecor (WorldGen.ts:365) — runSurfaceDecorPass + runTrapsPass(76)
18. 海滩装饰 vanillaBeachDecor (WorldGen.ts:373) — ShellPiles + seaweed
19. 结构 structurePass (WorldGen.ts:838) — legacy hut + chests
then finalize (WorldGen.ts:897)

Legacy branch (lgcTerrain === false):
1. 地形 terrainPass (WorldGen.ts:389) — fbm
2. 洞穴 cavePass (WorldGen.ts:487)
3. 矿石 vanillaShinies — WAIT: vanillaShinies requires ctxGs[0] which is null in legacy mode → returns immediately (no-op). Same for vanillaLakes, vanillaSurfaceDecor etc. So in legacy mode those passes are no-ops.
4. 液体 vanillaLakes (no-op, gs null)
5. 地狱 hellPass — uses ctxGs[0]! at line 579 `const gs = ctxGs[0]!` — non-null assertion; in legacy mode ctxGs[0] is null → tileRunnerHell would receive null gs... Actually hellPass line 579 `const gs = ctxGs[0]!;` then tileRunnerHell(st, rng, gs, ...) → tileRunner(st, rng, gs=null, ...) → inside tileRunner accesses gs.worldSurface at line 93 (only if o.mudWall) and gs.waterLine line 113 (type===-2 branch) and line 129 (cur===STONE && type===MUD), 149 (noYChange && y<gs.worldSurface) → hellPass calls use noYChange:true for some (line 586,595: noYChange true) → line 149 `if (noYChange && y < gs.worldSurface ...)` → gs null → TypeError crash! Hmm, wait: line 586: `tileRunnerHell(st, rng, gs, ..., true, 0, rng.int(1,2), true)` — noYChange=true → in tileRunner line 149: `if (noYChange && y < gs.worldSurface && type !== MUD)` → gs is null → throws. So legacy path would crash in hellPass? Unless... hmm. That's a potential bug but the legacy path is likely dead code. I should mention it as an observation: hellPass assumes ctxGs[0] non-null (WorldGen.ts:579) so the lgcTerrain=false path would crash at the hell pass (tileRunner dereferences gs at TileRunner.ts:93/113/129/149). Actually let me double check line 93: `if (o.mudWall && y > gs.worldSurface ...` — only when mudWall. Line 113: `if (type === -2 && st.flags[ti] && (y < gs.waterLine ...)` — hellPass 3c uses type -2 → gs.waterLine → crash. So yes, legacy branch crashes. Worth noting.

6. 清浮空 floatCleanupPass (WorldGen.ts:640)
7. 瓦罐 potPass (WorldGen.ts:663) — requires ctxGs[0]; legacy → gs null → returns (no-op!)
8. 表面 surfacePass (WorldGen.ts:758) — grass part works (uses world.groundLevel... wait world.groundLevel set in finalize only! In legacy mode, finalize sets groundLevel = h*0.28 fallback — but surfacePass runs BEFORE finalize, and world.groundLevel is set in vanillaTerrain (world.groundLevel = gs.worldSurface) — legacy terrainPass never sets world.groundLevel! World constructor may default. Let me check World constructor quickly for groundLevel default. Not critical but let me check.
9. 结构 structurePass

Let me check World's groundLevel default to be accurate about legacy surfacePass grass loop bound.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:11:47.123Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/src && grep -n \"groundLevel\\|rockLevel\\|lavaLine\" world/World.ts | head -10",
 "description": "Check World groundLevel default"
}
```


---

## 👤 User(sidechain) · 2026-08-11T04:11:47.170Z

**📎 ToolResult**

```
42:  groundLevel = 0; rockLevel = 0;   // tile 坐标
44:  lavaLine = 0;
67:   *  缺省 0=未知，使用处以 groundLevel 回退 */
127:    w.groundLevel = p.groundLevel; w.rockLevel = p.rockLevel; w.lavaLine = p.lavaLine;

```


---

## 🤖 Assistant · 2026-08-11T04:11:51.601Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
In legacy mode world.groundLevel = 0 during surfacePass → the grass loop `for (let y = 0; y < world.groundLevel - 1; y++)` → `y < -1` → no iterations → no grass in legacy. Consistent with legacy being semi-broken/dead.

I now have everything needed. Let me write the final report. It should be comprehensive with file:line references.

Structure:
1. Root cause answer (short, up front): the "sky junk written early, erased later" = ghost-type writes by placing TileRunner calls + Spread passes into air cells (flags=0), visible in the generation preview because mapColor24 colors by type only, and purged globally in finalize.
2. Pass order table with legacy/vanilla labels.
3. vanillaBiomes internal chain.
4. Per-pass sky-write analysis with y ranges + file:line.
5. finalPass/finalize erase logic.
6. Legacy vs vanilla pipeline differences.

Let me write it.
```

</details>


---

## 🤖 Assistant · 2026-08-11T04:12:51.287Z · glm-x-preview-260804

````
调查完成。以下为完整报告。

---

# 结论（先说答案）

**"生成早期往天空写入大量杂块、后期又被抹除"的主因是幽灵 tile（ghost type）机制**，而非真实的浮空块：

1. **写入端**：所有走 `tileRunner` 的"铺设型" pass（`addTile=false`，`overRide` 默认 true）会在**空气格上直接写 `type` 而不置 `flags`**（`TileRunner.ts:121-142`，`if (!flag3) st.type[ti] = type;` 且只在 `addTile` 时才 `flags=1`，见 `TileRunner.ts:144-148`）。多个 pass 的 y 采样下界是 **0（世界顶，纯天空）**，于是大量石/矿/泥的"幽灵 type"被刷进天空。`Spread.ts` 的草传播同样只比对 `type` 不看 `flags`（`Spread.ts:12, 47-50`），把幽灵泥进一步扩散成幽灵草。
2. **可见端**：生成期实时预览的着色函数 `mapColor24` **只看 `type` 不看 `flags`**（`render/MapColors.ts:29-35`），所以这些幽灵杂块在逐 pass 预览里**看得见**（天空出现大片色块）。而游戏内渲染 `ChunkCache.ts:223` 要求 `flags`，所以进游戏不可见。
3. **抹除端**：`finalize()` 开头的全图净化循环（`WorldGen.ts:900-903`）把所有 `!flags && type!==0` 的格子归零——这就是"后期被抹除"的那一刀。

---

# 1. `generateWorld` pass 列表与执行顺序

数组定义在 `WorldGen.ts:49-86`，`useVanillaTerrain = lgcTerrain !== false`（`WorldGen.ts:48`，默认走原版）。

## 1a. 默认管线（lgcTerrain ≠ false，vanilla 地形）

| # | pass 名 | 实现位置 | legacy 自有 / vanilla 移植 |
|---|---|---|---|
| 1 | 原版地形 | `WorldGen.ts:133` `vanillaTerrain` | vanilla（Reset 掷骰 + `vanilla/TerrainPass.ts:40 runTerrainPass`），外壳是本文件 wrapper |
| 2 | 洞穴 | `WorldGen.ts:209` `vanillaCaves` | vanilla：`runOceanSandPass`(pass 3) → `runMountCavesPass`(7) → `runRocksAndClayPass`(8-10) → `runCavesPass`(11-14e)，`vanilla/CavesPass.ts` |
| 3 | 海滩 | `WorldGen.ts:218` `vanillaBeaches` | vanilla：`runMountainCavesPass`(34) → `runBeachesPass`(33)，`vanilla/BeachPass.ts` |
| 4 | 生物群系 | `WorldGen.ts:232` `vanillaBiomes` | vanilla 超长链（见 §1c） |
| 5 | 矿石 | `WorldGen.ts:202` `vanillaShinies` | vanilla：`runShiniesPass`(27)，`vanilla/ShiniesPass.ts:28` |
| 6 | 液体 | `WorldGen.ts:194` `vanillaLakes` | vanilla：`runLakesPass`(31) + `runGemsPass`(36)（顺序注释在 `WorldGen.ts:59-61`：Shinies 27 → Lakes 31 → Gems 36 → Cleanup 37 → LifeCrystals 55） |
| 7 | 清理 | `WorldGen.ts:282` `vanillaCleanup` | vanilla：`runCleanupPass`(37)，`vanilla/CleanupPass.ts:14` |
| 8 | 生命水晶 | `WorldGen.ts:289` `vanillaLifeCrystals` | vanilla：`runLifeCrystalsPass`(55)，`vanilla/StructuresPass.ts:216` |
| 9 | 半砖平滑 | `WorldGen.ts:296` `halfBrickSmoothPass` | vanilla：`runSmoothWorldPass`（cs L7568），`vanilla/HalfBrickPass.ts:49` |
| 10 | 瀑布唇缘 | `WorldGen.ts:303` `waterfallLipPass` | vanilla：`runWaterfallLipPass`（cs L7697），`vanilla/HalfBrickPass.ts:142` |
| 11 | 地狱 | `WorldGen.ts:546` `hellPass` | **legacy 自有**（Underworld 移植，但写在本文件，调用 `vanilla/TileRunner.ts tileRunner`） |
| 12 | 地狱屋 | `WorldGen.ts:310` `vanillaHellHouses` | vanilla：`runHellFortPass`，`vanilla/HellFortPass.ts` |
| 13 | 地狱箱 | `WorldGen.ts:317` `underworldChestsPass` | vanilla：`runUnderworldChestsPass`（顺序注释 `WorldGen.ts:77-79`：必须在 hellPass 之后，否则被 100% 抹除） |
| 14 | 瓦罐 | `WorldGen.ts:663` `potPass` | **legacy 自有**（按原版 Pots cs:18186 1:1 语义重写，但代码在本文件） |
| 15 | 矿骨堆 | `WorldGen.ts:324` `pilesPass` | legacy wrapper（原版 pass 77 Piles 近似） |
| 16 | 表面 | `WorldGen.ts:758` `surfacePass` | **legacy 自有**外壳：铺草 + 内嵌 vanilla `runTreePass`(82) + 杂草/花/蘑菇（pass 86 语义） |
| 17 | 地表装饰 | `WorldGen.ts:365` `vanillaSurfaceDecor` | vanilla：`runSurfaceDecorPass` + `runTrapsPass`(76) |
| 18 | 海滩装饰 | `WorldGen.ts:373` `vanillaBeachDecor` | vanilla：`runBeachDecorPass`（ShellPiles + 海藻） |
| 19 | 结构 | `WorldGen.ts:838` `structurePass` | **legacy 自有**（buildHut + placeChest；`cfg.structures===false` 时跳过，`WorldGen.ts:85`） |
| — | finalize | `WorldGen.ts:897` | legacy 自有收尾（幽灵净化 + 出生点） |

每个 pass 完成后触发 `onWorldPartial`（`WorldGen.ts:93`）——这就是预览逐帧看到天空杂块的时机。

## 1b. 旧 fbm 回退管线（`lgcTerrain === false`）

`WorldGen.ts:55-58, 64-67, 68-73, 75, 76, 79, 81, 83, 84` 的条件展开后：

1. 地形 `terrainPass`（`WorldGen.ts:389`，fbm 多 octave + 海盆）
2. 洞穴 `cavePass`（`WorldGen.ts:487`，噪声挖空 + 蠕虫隧道）
3. 矿石 `vanillaShinies` → **空转**（`WorldGen.ts:204-205` `if (!gs) return;`，legacy 下 `ctxGs[0]` 恒 null）
4. 液体 `vanillaLakes` → **空转**（同上）
5. 地狱 `hellPass` → **会崩**：`WorldGen.ts:579` `const gs = ctxGs[0]!;` 非空断言，随后 `tileRunner` 内部解引用 `gs.waterLine/worldSurface`（`TileRunner.ts:93, 113, 129, 149`），null 直接 TypeError
6. 清浮空 `floatCleanupPass`（`WorldGen.ts:640`，仅 legacy 有）
7. 瓦罐 `potPass` → **空转**（`WorldGen.ts:671-672` `if (!gs) return;`）
8. 表面 `surfacePass` → 铺草循环空转（`world.groundLevel` 此时为 0，`World.ts:42` 默认，`WorldGen.ts:763` `y < groundLevel-1` 不成立）；树也空转（`WorldGen.ts:772-773` `if (gs)`）；只有杂草/花部分会跑
9. 结构 `structurePass`

即：legacy 分支没有 7-13、15、17、18 这些 vanilla pass。`lgcTerrain` 只在 `workers/protocol.ts:16` 出现，**没有任何 UI 设置它**——legacy 路径实际是死代码/半损坏状态。

## 1c. `vanillaBiomes` 内部链（`WorldGen.ts:232-279`）

| 内部顺序 | 调用 | 原版 pass 号 | 文件 |
|---|---|---|---|
| 1 | `runIceBiomePass` | 15 | `IceBiomePass.ts:10` |
| 2 | `runGrassPass` | 16 | `GrassPass.ts:8` |
| 3 | `runJunglePass` | Jungle（含巨型泥 runner + 地表隧道） | `JunglePass.ts:14` |
| 4 | 丛林表面泥化（自制补丁，非原版 pass） | — | `WorldGen.ts:241-251` |
| 5 | `spreadGrassAll`（泥→丛林草，限丛林核心 ±0.21w） | 17 Mud Caves To Grass | `WorldGen.ts:252` |
| 6 | `runDesertPass` | 18 Full Desert | `DesertPass.ts:20` |
| 7 | `runFloatingIslandsPass` | 19 Floating Islands | `StructuresPass.ts:22` |
| 8 | `runMushroomPass` | 20 Mushroom Patches | `MushroomPass.ts:20` |
| 9 | `runMarbleGranitePass` | 21/22 | `MarbleGranitePass.ts:18` |
| 10 | `runDirtToMudAndSiltPass` | 23/24 | `DirtToMudPass.ts:14` |
| 11 | `runSlushPass` | 33 | `IceBiomePass.ts:73` |
| 12 | `runCorruptionPass` | 28 | `CorruptionPass.ts:30` |
| 13 | `runDungeonPass` | 30 | `DungeonPass.ts` |
| 14 | `runPyramidPass` | 38 | `StructuresPass.ts:307` |
| 15 | `runBuriedChestsPass` | 59 | `BuriedChestsPass.ts:143` |
| 16 | `runSurfaceChestsPass` | 36 | `BuriedChestsPass.ts:178` |
| 17 | `runWaterChestsPass` | 39 | `BuriedChestsPass.ts:196` |
| 18 | `runWetJunglePass` | 43 | `StructuresPass.ts:351` |
| 19 | `runBeehivePass` | 45 Hives | `HiveSpiderPass.ts` |
| 20 | `runWebsPass` | 58 Webs | `HiveSpiderPass.ts` |
| 21 | `runSpiderNestPass` | 63 Spider Caves | `HiveSpiderPass.ts` |
| 22 | `runWebsInSpiderCavesPass` | 64 | `HiveSpiderPass.ts` |
| 23 | `runTemplePass` | 44 Jungle Temple | `TemplePass.ts` |
| 24 | `runIslandHousePass` | 浮空岛房屋 | `IslandHousePass.ts:18` |
| 25 | `runSwordShrinePass` | 附魔剑圣地 | `SwordShrinePass.ts:13` |

---

# 2. 逐 pass 天空写入（y < groundLevel）分析

坐标系注意：**y 越小越高**，天空 = y < `worldSurface/groundLevel`。

## 2a. 幽灵写入（type 写入空气格，flags=0 → 预览可见、finalize 抹除）——这就是"杂块"

核心机制：`TileRunner.ts:121-142`
```ts
if (overRide || !st.flags[ti]) {   // overRide 默认 true → 恒进
  ...
  if (!flag3) st.type[ti] = type;  // 空气格也写 type（原版语义）
}
if (addTile) { st.flags[ti] = 1; ... }  // 默认 false → flags 保持 0
```
注释自证：`TileRunner.ts:3-4` "空气格上的幽灵 type 不渲染"；`WorldGen.ts:898-899` "生成期 TileRunner 会在空气格写残留 type(原版语义,渲染不可见)"。

具体天空写手（按 y 下界排序）：

| pass | 证据（文件:行） | y 范围 | 写入物 |
|---|---|---|---|
| 洞穴-pass8 Rocks In Dirt 第一带 | `CavesPass.ts:25` `run(area*0.00015, 0, gs.worldSurfaceLow, T.STONE, 4,14,5,39)` | **y ∈ [0, worldSurfaceLow)**，起点可在纯天空 | 幽灵 STONE |
| 洞穴-pass10 Clay 第一带 | `CavesPass.ts:36` `run(area*0.00002, 0, gs.worldSurfaceLow-1, CLAY, ...)` | **y ∈ [0, worldSurfaceLow-1)** | 幽灵 CLAY |
| 矿石-pass27 银/钨"天空带" | `ShiniesPass.ts:44` `band(..., area*1.7e-4, 0, surfLow, silver, [4,8],[4,7])`，注释"天空带 1.7e-4" | **y ∈ [0, surfLow)** | 幽灵银/钨矿 |
| 矿石-pass27 金/铂近地表带 | `ShiniesPass.ts:47` `band(..., area*1.2e-4, 0, max(1, surfLow-20), gold, ...)` | **y ∈ [0, surfLow-20)** | 幽灵金/铂矿 |
| 生物群系-Jungle 巨型泥 runner | `JunglePass.ts:65` `tileRunner(..., {strength: num2(400-600×scale), steps: 10000, type: MUD, speedY: -20, noYChange: true, mudWall: true})`；上升停止条件 `TileRunner.ts:79`（py<0 才停） | 起点 `cy≈(h+rockLevel)/2`，**一路向上冲到世界顶 y<0**，半径 400-900 | 丛林整列天空被刷满**幽灵 MUD**（量级最大）；mudWall 墙只在 y>worldSurface 写（`TileRunner.ts:93`），天空墙不写 |
| 生物群系-Grass 种子第二组 | `GrassPass.ts:26-27` `y2 = rng.int(0, max(1, worldSurfaceLow-1))` | y ∈ [0, worldSurfaceLow) | 需四邻全为活性泥土（`GrassPass.ts:14`）→ 天空基本 no-op，仅转已有活性格 |
| 草传播（放大器） | `Spread.ts:12`（只比 type）、`Spread.ts:47-50`（全图扫描不看 flags）、`Spread.ts:56-73`（两轮扩散也只比 type） | 全图 | 把幽灵 MUD 转**幽灵蘑菇草**（`MushroomPass.ts:62` 全图无中心限制）/**幽灵丛林草**（`WorldGen.ts:252` 限 ±0.21w） |
| 腐化裂隙壳层 | `CorruptionPass.ts:307, 315`（`st.type[ti] = EBONSTONE` 先于/独立于 flags 置位） | 裂隙起于 `worldSurfaceLow..worldSurface-1`（`CorruptionPass.ts:93`），壳半径 ×1.1 可越出地表上方少许 | 幽灵 EBONSTONE（主要在地下） |
| 蘑菇区泥 blob | `MushroomPass.ts:90` `st.type[ti] = MUD`（仅首圈置 flags，`MushroomPass.ts:91`） | 深 underground（j∈[rockLevel+50, h-301]，`MushroomPass.ts:34`） | 幽灵 MUD（不在天空） |
| 腐化裂隙挖空 | `CorruptionPass.ts:262, 348` `st.flags[ti] = 0`（只清 active 保留 type，原版 KillTile 语义） | 地下 | 制造地下幽灵（非天空） |

## 2b. 真实天空写入（flags=1，最终**保留**，属正常内容）

| pass | 证据 | y 范围 |
|---|---|---|
| Mount Caves 山丘（pass 7，在"洞穴"pass 内） | `MountCavesPass.ts:18-51 mountinater`，`MountCavesPass.ts:39` `if (!st.flags[k]) st.setTileSilent(x, y, T.DIRT)`；起点取列首实心行（`MountCavesPass.ts:73`），blob 以 vy=-1..-2 上漂约 40 格 | **地表以上 ~40-54 格**的泥土山丘 |
| Floating Islands（pass 19，"生物群系"内） | `StructuresPass.ts:49` `y = min(rng.int(90, surf-100), worldSurfaceLow-50)`；`StructuresPass.ts:77, 107, 145-146` `st.type= CLOUD; st.flags = 1` | **y ≈ [90, worldSurfaceLow-50]** 的云/雨云岛 + 土芯 |
| 浮空岛房屋 | `IslandHousePass.ts:50, 83` 日光板 `flags=1` | 岛上（天空） |
| 树（pass 82，在"表面"pass 内） | `TreePass.ts:53-99 growTrunk`（树干 y=index1-height..index1，height 5-16，`TreePass.ts:121`）；epic 20-29（`TreePass.ts:143`）；palm 10-20（`TreePass.ts:158`） | **从地表向上 5-29 格**树干/枝/根/冠 |
| 地表装饰 | `StructuresPass.ts:266`（仙人掌高 2-5）、`276-278`（杂草/花/蘑菇，地表上 1 格） | 地表以上 1-5 格 |
| legacy surfacePass 杂草 | `WorldGen.ts:798-823`（`for y=1..h`，任何草族 tile 上方 1 格） | 地表/岛面/山丘上方 1 格 |
| 地牢入口塔 | `DungeonPass.ts:488-655 dungeonEnt`：`cy = j - dy1/2`（dy1=20-24，`DungeonPass.ts:503-504`），塔顶 `t1 = cy - dy1*0.6 - 2..4`（`DungeonPass.ts:528`）→ 塔体/垛口/顶齿用 `fillB/extFill`（`flags=1`，`DungeonPass.ts:515, 522`） | **地表以上约 25-35 格**的实体地牢砖塔 |
| 沙漠沙丘 | `DesertPass.ts:81-86` 纯沙柱 `st.type=SAND; st.flags=1`，`moundSurfY = (topY+moundH) - profile*moundH + coarse`（`DesertPass.ts:66`） | 沙丘**隆起在地表之上**（中心处高出约 moundH×profile） |
| 猩红弹坑土丘 | `CorruptionPass.ts:486-519` 地表囊群（从 startY 向上漂 ≤5 格、半径 25-34、壳 0.45R），`CorruptionPass.ts:513` `flags=1; type=CRIMSTONE`；列填充 `CorruptionPass.ts:527-532` | **起点 surfaceLow-10**（`CorruptionPass.ts:81`），壳层可探到**地表以上 ~15-20 格** |
| Smooth World 空位补角 | `HalfBrickPass.ts:105-119`（`st.type===0` 且下方实心+单侧实心 → `setTileSilent(i,j,belowType)` + 半砖） | 凸起地表上方的角落（天空边缘 1 格）。注释 `HalfBrickPass.ts:19-21` 记录过该分支曾把天空幽灵实体化成 2583 个浮空半砖，现已用 `solidTile` 要求 flags 修复（`HalfBrickPass.ts:22-24, 32`） |

## 2c. 明确**不**写天空的（问题清单逐项回答）

- **legacy structurePass（buildHut/placeChest）**：小屋 `hy = rng.int(floor(h*0.45), h-40)`（`WorldGen.ts:845`）→ **深地下**；散落宝箱从 `surface[cx]+8` 向下扫（`WorldGen.ts:855`）→ 地表以下。buildHut 9×6 全在 hy..hy+6（`WorldGen.ts:869-894`）。**不写天空**。
- **legacy surfacePass**：铺草循环 `y < world.groundLevel-1` 只处理已实心格（`WorldGen.ts:762-769`）；植物只放草族上方 1 格（`WorldGen.ts:792-797`）。无杂块。
- **potPass**：`y0 = rng.int(surfHigh, h-10)`，且"地表以上需有墙"（`WorldGen.ts:725` `if (y < surfLow && wall===0) continue`）→ 不写天空。
- **vanilla CavesPass / TileRunner 挖空**：`type<0` 分支只清已有格（`TileRunner.ts:110-118`）；地表洞穴入口 runner 起点=列首实心行（`CavesPass.ts:107-111, 181-186`），向下挖。**不往地表以上加块**（但 §2a 的"铺设"分支会写幽灵）。
- **liquidPass（已删，现 vanillaLakes）**：湖锚点从 `worldSurfaceLow-20` 向下找实心（`LakesPass.ts:128-133`），SonOfLakinater 只在 `y>=j` 灌水（`LakesPass.ts:58-64`），漏斗入口只**挖**不灌（`LakesPass.ts:76-88`）。**天空不写水**。挖空型 runner 的 `-2` 液体也只在活性格（`TileRunner.ts:113-116`）。
- **hellPass**：全部 y > h-190（`WorldGen.ts:551-567`）。
- **Beaches**：沙只写在 `y > waterY`（`BeachPass.ts:139-141, 166-168`），水在 waterY 之下——海盆内不涉及天空。

---

# 3. finalize 的全部"抹除"逻辑（`WorldGen.ts:897-974`）

1. **幽灵净化（最大一刀）** `WorldGen.ts:900-903`：
   ```ts
   for (let i = 0; i < store.type.length; i++) {
     if (!store.flags[i] && store.type[i] !== 0) store.type[i] = 0; // 幽灵 type
     if (store.type[i] === 0) store.flags[i] = 0;                   // 幻影活性
   }
   ```
   全图 O(w×h) 扫描，**把所有幽灵杂块（含天空的幽灵石/矿/泥/草）一次性清零**。注释明确动机：存档格式无 active 位，防重读激活成浮空块。

2. **出生点选取** `WorldGen.ts:904-931`（原版 pass 78 Spawn Point）：中心扩张采样找首个实心格，`bad` 判定 `sy > worldSurface`（`WorldGen.ts:917-919`）——拒绝地下/水下出生，不改地形。

3. **出生点上空净空 ×2**：
   - 窄盒 3×3（dx −1..1, dy 1..3）`WorldGen.ts:945-949`，`keepGrass=false`；
   - 宽盒 5×5（dx −2..2, dy 1..5）`WorldGen.ts:967-971`，`keepGrass=true`；
   - 清除函数 `clearSpawnCell` `WorldGen.ts:937-944`：**豁免树干（`t === T.TREE` 直接 return）与（可选）草面**，其余 `setTileSilent(x,y,0)`。注释 `WorldGen.ts:934-936` 解释这是为防"浮空断干"。

4. **回填世界常量** `WorldGen.ts:951-965`：`groundLevel/rockLevel`（无 gs 时回退 `h*0.28 / h*0.33`）、`treeX/treeStyle/trees`。

其他（非 finalize 但属"抹除"的 pass）：
- **vanillaCleanup** `CleanupPass.ts:14-53`：(a) 表层天然墙清理（y < worldSurface，清墙 2/40/64/86，`CleanupPass.ts:24-49`）——**会清天空区域的墙**；(b) 连通小块 <20 清除 `scanTileColumnAndRemoveClumps`（`CleanupPass.ts:70-86`，**y 从 10 起，包含天空**）→ 会抹掉天空里 <20 格的实心碎屑（含山丘/浮空岛残片）。这就是"清理(Clean Up Dirt)须在矿石之后"的注释（`WorldGen.ts:59-61`）。
- **SmoothWorld** `HalfBrickPass.ts:84-96, 101-103`：悬空支脚/孤立立柱 `setTileSilent(i,j,0)`，扫描范围 j ∈ [20, h-20]（`HalfBrickPass.ts:52-53`）——含天空。
- **DesertPass 沙丘上方削平** `DesertPass.ts:72-78`：从地表上一格清到 flatten（清掉沙丘上方的突出物，含天空残留）。
- **SwordShrine 竖井** `SwordShrinePass.ts:79-84`：从洞心向上清到 `worldSurface-2`。
- **hellPass 界下清空** `WorldGen.ts:559-562`：y ≥ boundary 全部 `type=0; flags=0` ——即注释（`WorldGen.ts:77-79`）所说"地狱箱曾被 hellPass 100% 抹除"的来源。
- **floatCleanupPass**（仅 legacy）`WorldGen.ts:640-660`：从 `surfY+2` 向下剥离无支撑土/石/草——**只处理地表以下，不碰天空**。
- **ShiniesPass.sandArch** `ShiniesPass.ts:88-115`：浮沙下落归位（防流沙塌落）。

---

# 4. legacy fbm vs vanilla 两套管线差异（天空杂块视角）

| 维度 | vanilla（默认） | legacy fbm（lgcTerrain=false） |
|---|---|---|
| 地形 | `TerrainPass.ts:40-120` 逐列随机走；`y < num2` 一律 `type=0; flags=0`（`TerrainPass.ts:82-83`）——**天空本来干净** | `WorldGen.ts:389-478` fbm；`y < sy` 直接 skip（`WorldGen.ts:420`）——也干净 |
| 天空幽灵写入 | **大量**：§2a 全部来源（CavesPass 两条 yMin=0 带、Shinies 两条 yMin=0 带、Jungle 巨型泥 runner、Spread 草扩散） | **几乎没有**：不走 tileRunner 铺设（cavePass 只挖空，`WorldGen.ts:494-516`），gs 为 null 使 Shinies/Lakes/Pots 全部空转 |
| 天空真实块 | 山丘、浮空岛、岛屋、树、地牢塔、沙丘、猩红土丘、Smooth 补角 | 无树（`WorldGen.ts:772-773`）、无浮空岛、无山丘；只有结构 pass 的小屋（地下） |
| 后期抹除 | finalize 幽灵净化 + Cleanup 小块清除 + Smooth 削除 | 只有 floatCleanupPass（地下） + finalize |
| 健康度 | 完整 | hellPass 处 `ctxGs[0]!` 断言会 null 崩溃（`WorldGen.ts:579` → `TileRunner.ts:113/149`） |

**结论：天空杂块问题只存在于 vanilla 管线**，且是"原版 1:1 语义 + 本仓库无 active 位"的组合结果：原版 TileRunner 也往 inactive 格写 type（渲染不可见），这里因为存档/预览按 type 着色而显形，最后靠 finalize 统一清除。如果要减少预览期的天空杂块观感，候选改法是在 `TileRunner.ts:121` 增加 `st.flags[ti]` 守卫（偏离原版但消除幽灵），或让 `mapColor24`（`render/MapColors.ts:32`）加 `st.flags[i]` 判断（只影响预览显示，不动数据）。

# 关键文件索引

- pass 数组与分支：`~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:49-86`
- vanillaBiomes 链：`WorldGen.ts:232-279`
- finalize 抹除：`WorldGen.ts:897-974`（净化 900-903；出生净空 937-949, 967-971）
- 幽灵写入机制：`~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts:110-154`
- 预览可见性根源：`~/Project/GLM/SandboxWorld/game/src/render/MapColors.ts:29-43`
- 游戏内不可见性：`~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:223`
- yMin=0 天空带：`CavesPass.ts:25,36`、`ShiniesPass.ts:44,47`
- 巨型泥 runner：`JunglePass.ts:59-67`
- 草扩散放大器：`Spread.ts:8-75`
- Cleanup 双重清除：`CleanupPass.ts:14-118`
````
