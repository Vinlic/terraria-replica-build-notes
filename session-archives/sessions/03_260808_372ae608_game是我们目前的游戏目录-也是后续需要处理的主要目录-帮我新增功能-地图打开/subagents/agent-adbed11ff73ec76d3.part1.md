# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-10T06:28:11.010Z

```
为 ~/Project/GLM/SandboxWorld/game（Vite 5 + TS，Terraria 复刻）设计"世界生成/存档加载移入 Web Worker"的实施方案。以下是已完成的调研结论（可信，无需重查，可抽查关键文件确认）：

## 调研结论摘要

**可 worker 化的三个纯计算段**：
1. `generateWorld`（src/world/gen/WorldGen.ts:35）——16 个 pass 循环，pass 间已有 nextFrame() 让出但 pass 内同步；RNG（src/core/rng.ts mulberry32）+ simplex-noise 全纯计算，同 seedText 确定性复现。模块级单例 `ctxGs`（WorldGen.ts:310）不可重入（worker 内天然串行，无碍）。
2. `Game.settleLiquids`（src/core/Game.ts:405-438）——纯计算，gen/load 两种模式（gen=外层10轮，load=单轮 WorldFile 时序）。它内部 new LiquidSim（LiquidSim 构造器向 store 注册 onTileChanged/onLiquidChanged 闭包 + killTile 回调字段，Game 注入 breakTile——但 settle 模式不设 killTile）。附带发现：临时 LiquidSim dispose() 只置 flag，store.listeners 死闭包累积泄漏——worker 化顺带消除。
3. `loadSaveData`（src/save/SaveFile.ts:175-265）——JSON.parse + 5 段 RLE 解码纯 CPU；存档字符串从 IndexedDB（src/save/KvStore.ts）读出。注意 JSON 字符串很大（大世界几十 MB），传入 worker 用字符串本身（structured clone 字符串是拷贝）或考虑直接在 worker 内读 IndexedDB。

**数据搬运**：TileStore（src/world/TileStore.ts）10 个 TypedArray（type/flags/frameX/frameY/wall Uint16×3+Uint8，liquid/liquidType/half/slope/wire Uint8）+ World 标量（name/seed/spawnX/spawnY/groundLevel/rockLevel/lavaLine/crimson/dungeonX/dungeonY/jungleX/exploredVersion）+ chests/signs/trees/treeX/treeStyle/treeTops/flags/clock/explored(Uint8Array)。中世界 6400×1800 ≈ 173MB → **必须 transferable（ArrayBuffer 转移所有权）**，主线程 new World(w,h,seed,name) 重建 + 回填字段。TileStore 有私有 listeners/liquidListeners 函数数组——structured clone 会抛错，必须走"数据包重建"路径。
**注意**：transfer 后 worker 侧数组不可再用；settleLiquids 在 worker 里跑完再 transfer 最优（生成+沉降一个 worker 消息链完成）。

**必须留主线程**：preloadSceneAssets（Game.ts:328，new Image/decode/fetch/canvas）、afterWorldLoad（Game.ts:451，ChunkCache/Minimap/Renderer/LightingEngine/LiquidSim 运行期实例 + 监听注册，全部在数据就绪后，顺序天然兼容）。Game 构造器 DOM 绑定。

**onWorldPartial 实时预览**：mainFlow.ts:280 → UIWorldLoadState.attachWorld → GenWorldPreview（主线程 canvas 逐列重绘）。worker 化后需 worker 周期 postMessage 预览数据。注意预览自己扫 store 数组不依赖事件。

**Vite 5.4** 原生支持 `new Worker(new URL('./x.worker.ts', import.meta.url), { type: 'module' })`，dev 态 ESM、构建期自动打包。项目零现有 worker。

**调用方**：mainFlow.ts createWorldFlow（:271-289，vui UIWorldLoadState 进度条 setProgress(label,p)）、loadWorldFlow（:263-268，kvGet → loadFromJson → g.loadWorld）、importWld（:158-199）。Game.newWorld/loadWorld 是改造入口。

## 设计要求

1. **架构**：新建 src/workers/（worldGen.worker.ts 等），消息协议（请求类型：generate/settle/saveParse；进度消息；结果消息含 transfer 列表）。主线程封装一个 `WorldGenClient`（Promise 化 + 进度回调 + worker 复用/终止 + feature 回退：Worker 不可用时降级现有主线程路径）。
2. **World 数据包协议**：定义 `WorldPacket`（10 个 TypedArray 的 buffer + 标量 JSON + chests/signs/trees 等），双向：生成完→transfer 回主线程重建；settle 请求→主线程把已有世界打包 transfer 进 worker（注意 transfer 后主线程这份数据不可再用——loadWorld 场景 world 已在手，需要先 copy 还是接受所有权转移？读档场景 world 数据 transfer 走后主线程原 world 就废了——但 afterWorldLoad 用的是新 world，可行，但要分析 saveGame 时机等）。Worker 重建 World/TileStore 需要一个 `World.restore(packet)` / `TileStore.restore()` 静态构造。
3. **newWorld 消息链**：主线程请求 generate(cfg) → worker 跑 generateWorld（progress 消息每 pass）+ settleLiquids(gen)（settle 也进 worker，一处做完）→ 一次性 transfer 回。loadWorld 链：主线程从 IndexedDB 取字符串 → 传给 worker（或 worker 自取 IndexedDB——设计取舍：字符串几十 MB 的 clone 开销 vs worker 直接 kvGet）→ loadSaveData + settleLiquids(load) → transfer 回。
4. **实时预览保留**：worker 生成期周期 postMessage 预览快照（设计：全量 type 数组太贵——用降采样？GenWorldPreview 逐列重绘读 store.type——可改为传「列采样 Uint8Array（每列1字节 mapColor index？）」或干脆 type 的 transfer 一份副本每 N pass 一次。给出推荐与理由）。
5. **风险清单**：用户问了"有什么风险"——内存峰值（worker+主线程双份/transfer 时机）、Vite worker dev 构建坑（worker.format、跨 worker import 的 data/tiles 循环依赖）、错误处理与超时、Safari 老版本 module worker 兼容（降级路径）、确定性回归（同 seed 主线程/worker 结果一致——RNG 纯函数应一致但要验证）、探针脚本影响（puppeteer 探针靠 window.__swGame——不受影响）、wld 导入路径。
6. **分阶段实施**：第一阶段 generate+settle 进 worker（最大收益），第二阶段 saveParse 进 worker，可选第三阶段 saveGame 序列化进 worker。
7. **验证**：现有探针回归（_settleprobe/_liquidprobe/_waterfallprobe/_spawnposprobe 等）+ 新增 worker 探针（同 seed 双路径一致性断言：主线程 generate 与 worker generate 产出的 type 数组逐格相等——这验证 RNG/管线确定性）。

输出：详细实施计划（文件清单、消息协议类型定义草案、关键函数签名、改动点列表、风险表、验证清单）。
```

---

## 📎 Attachment · skill_listing · 2026-08-10T06:28:11.013Z

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

## 🤖 Assistant · 2026-08-10T06:28:12.886Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user needs a detailed implementation plan for moving world generation and save loading into a Web Worker. The research summary is trustworthy, but I should verify the key files to confirm signatures, message flow, and integration points before designing. Let me start by reading the core files in parallel: WorldGen.ts, Game.ts (the relevant sections), SaveFile.ts, TileStore.ts, World.ts, mainFlow.ts, KvStore.ts, LiquidSim.ts, and GenWorldPreview, plus vite.config.

Let me read them efficiently.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:28:13.111Z · glm-x-preview-260804

```
我先抽查关键文件确认签名与调用链，再给出完整实施方案。
```


---

## 🤖 Assistant · 2026-08-10T06:28:13.323Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts",
 "limit": 80
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:13.335Z

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
55	      { name: '清理', run: vanillaCleanup },
56	      { name: '生命水晶', run: vanillaLifeCrystals },
57	    ] as Pass[] : [
58	      { name: '地形', run: terrainPass },
59	      { name: '洞穴', run: cavePass },
60	    ]),
61	    { name: '矿石', run: vanillaShinies },
62	    { name: '液体', run: vanillaLakes },
63	    ...(useVanillaTerrain ? [
64	      // 原版 "Smooth World"(L7568)+"Waterfalls"(L7697)：地表凸起与水边唇缘砸半砖
65	      // （半砖 = 原版水浸润/瀑布触发的核心，见 HalfBrickPass.ts）
66	      { name: '半砖平滑', run: halfBrickSmoothPass },
67	      { name: '瀑布唇缘', run: waterfallLipPass },
68	    ] as Pass[] : []),
69	    { name: '地狱', run: hellPass },
70	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [{ name: '清浮空', run: floatCleanupPass }] : []),
71	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '地狱屋', run: vanillaHellHouses }]),
72	    { name: '瓦罐', run: potPass },
73	    { name: '表面', run: surfacePass },
74	    ...((cfg as GenConfig & { lgcTerrain?: boolean }).lgcTerrain === false ? [] : [{ name: '地表装饰', run: vanillaSurfaceDecor }]),
75	    ...(cfg.structures === false ? [] : [{ name: '结构', run: structurePass }]),
76	  ];
77	
78	  for (let i = 0; i < passes.length; i++) {
79	    onProgress?.(passes[i].name, i / passes.length);
80	    await nextFrame();

```


---

## 🤖 Assistant · 2026-08-10T06:28:13.546Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "offset": 300,
 "limit": 180
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:13.557Z

**📎 ToolResult**

```
300	          const next = modes[(cur + 1) % modes.length].reduce((a, b) => a | b, 0);
301	          this.wireToolMode = next;
302	          const name = next & TOOL_CUTTER ? (next & TOOL_ACTUATOR ? '剪致动器' : '剪线') : next & TOOL_ACTUATOR ? '致动器' : '四色铺线';
303	          this.cb.onToast(`工具模式:${name}`);
304	        }
305	      }
306	    });
307	  }
308	
309	  // ================= 生命周期 =================
310	
311	  async newWorld(seedText: string, width: number, height: number, onProgress?: (label: string, p: number) => void, opts?: { name?: string; evil?: -1 | 0 | 1; onWorldPartial?: (world: import('../world/World').World, passIndex: number, passName: string) => void }) {
312	    this.world = await generateWorld({ width, height, seedText, name: opts?.name, evil: opts?.evil, onWorldPartial: opts?.onWorldPartial }, (label, p) => onProgress?.(label, p * 0.7));
313	    // 水体预沉降：创建世界时全图激活+步进至稳定，带进度条
314	    onProgress?.('水体沉降', 0.72);
315	    await this.settleLiquids((p) => onProgress?.('水体沉降', 0.72 + p * 0.15));
316	    // 进图前贴图预载(用户要求:不进图后才动态加载)
317	    await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.87 + p * 0.13));
318	    onProgress?.('完成', 1);
319	    this.afterWorldLoad();
320	    this.cb.onWorldReady();
321	  }
322	
323	  /** 进图前统一预载:onWorldReady 之前把首帧画面涉及的贴图全部就位。
324	   *  图块/墙表按【出生点区域类型扫描】精确预载(半径 240 实测仅 22/378 张表,
325	   *  而非全量 ~250MB)——远行遇到的类型走懒加载,onVImageLoaded 回调全量标脏
326	   *  chunk 自动重烘焙;物品图标全量(18MB);角色 = Player_ 全量 + 当前装备的
327	   *  3 张 Armor 表(换装走懒加载);出生点森林背景 */
328	  private async preloadSceneAssets(onProgress?: (label: string, p: number) => void): Promise<void> {
329	    const a = this.atlas;
330	    if (!a) return;
331	    onProgress?.('加载世界贴图', 0.05);
332	    // 出生点半径类型扫描:只预载画面涉及的图块/墙表
333	    const st = this.world.store;
334	    const { tileSheets, wallIds } = this.collectSheetsAround(this.world.spawnX, this.world.spawnY, 240);
335	    await Promise.all([
336	      a.preloadTileSheetsFor(tileSheets, wallIds),
337	      a.preloadMiscAndNpcs(),
338	    ]);
339	    onProgress?.('加载物品图标', 0.15);
340	    await a.preloadIcons();
341	    onProgress?.('加载角色贴图', 0.7);
342	    // Player_ 全量(纸娃娃全部身体通道) + 仅当前装备的 Armor 表;
343	    // 换装时 vui 懒加载 + PaperDoll 就绪预检自动兜住
344	    const armorFiles = new Set<string>();
345	    for (const id of this.playerPreviewArmor()) {
346	      if (id == null) continue;
347	      const def = ITEM_DEFS[id];
348	      if (!def) continue;
349	      const vid = VANILLA_ITEM_ICON_MAP[def.key] ?? (def.key.startsWith('vi_') ? parseInt(def.key.slice(3), 10) : NaN);
350	      const entry = Number.isFinite(vid) ? a.vanilla.armorIndex?.[String(vid)] : null;
351	      if (!entry) continue;
352	      if (entry.head) armorFiles.add(`Armor_Head_${entry.head}.png`);
353	      if (entry.body) armorFiles.add(`Armor_Armor_${entry.body}.png`);
354	      if (entry.legs) armorFiles.add(`Armor_Legs_${entry.legs}.png`);
355	    }
356	    await a.preloadUiPrefix(['Player_']);
357	    await a.preloadUiFiles(armorFiles);
358	    onProgress?.('加载背景图', 0.9);
359	    await this.renderer.biomeBg.preloadInitial(this.world);
360	    onProgress?.('加载背景图', 1);
361	  }
362	
363	  /** 区域类型扫描:中心 ±R 内出现的图块 sheet id + 墙 id 集合(出生点预载/传送门共用) */
364	  private collectSheetsAround(cx: number, cy: number, R: number): { tileSheets: Set<number>; wallIds: Set<number> } {
365	    const st = this.world.store;
366	    const tileSheets = new Set<number>();
367	    const wallIds = new Set<number>();
368	    for (let x = Math.max(0, cx - R); x < Math.min(st.w, cx + R); x++) {
369	      for (let y = Math.max(0, cy - R); y < Math.min(st.h, cy + R); y++) {
370	        const i = st.idx(x, y);
371	        if (st.flags[i]) {
372	          const vs = TILE_DEFS[st.type[i]]?.vanilla?.sheet;
373	          if (vs !== undefined) tileSheets.add(vs);
374	        }
375	        if (st.wall[i] > 0) wallIds.add(st.wall[i]);
376	      }
377	    }
378	    // 兜底常驻:草/泥/石表全时有(暴露地表转草、autotile 邻接)
379	    for (const k of ['dirt', 'stone', 'grass']) {
380	      const vs = TILE_DEFS[TILE_BY_KEY[k]]?.vanilla?.sheet;
381	      if (vs !== undefined) tileSheets.add(vs);
382	    }
383	    return { tileSheets, wallIds };
384	  }
385	
386	  /** 预载期的装备槽位(此时 player 尚未创建,读初始装备常量:afterWorldLoad 同源) */
387	  private playerPreviewArmor(): Array<number | null> {
388	    // 与 afterWorldLoad 初始装备一致:铁三件(头/胸/腿)
389	    const ids: Array<number | null> = [null, null, null];
390	    const order = ['iron_helmet', 'iron_chainmail', 'iron_greaves'];
391	    for (let k = 0; k < 3; k++) {
392	      const id = ITEM_BY_KEY[order[k]];
393	      ids[k] = id !== undefined ? id : null;
394	    }
395	    return ids;
396	  }
397	
398	  /** 全图液体沉降。
399	   *  mode='gen'（新建世界）：原版 WorldGen pass 49/97 Settle Liquids（WorldGen.cs:7395/10247）
400	   *    ——外层 10 轮跑到收敛，清除生成期晚到的回流（漏斗入口等）。
401	   *  mode='load'（读档）：原版 WorldFile.cs:738-770 时序 1:1——单轮上限 100000，
402	   *    不收敛的少量残留活水交给运行时（尾部 WaterCheck），与原版一致（同帧完成，无外层循环）。
403	   *  yield 按真实耗时让出（≥32ms 一次）——按次数让出会把上万次迭代拖成数千次 setTimeout
404	   *  造成读档进度条"假慢" */
405	  private async settleLiquids(onProgress?: (p: number) => void, mode: 'gen' | 'load' = 'gen') {
406	    const sim = new LiquidSim(this.world);
407	    onProgress?.(0.05);
408	    sim.quickWater();
409	    onProgress?.(0.35);
410	    await new Promise((r) => setTimeout(r, 0));
411	    sim.waterCheck();
412	    sim.quickSettle = true;
413	    // 轮上限：读档 = WorldFile 单轮 100000（L752）；生成期 = 每轮 活量×5（WorldGen.cs:16252 num5）
414	    const MAX_ROUNDS = mode === 'gen' ? 10 : 1; // 读档无外层循环（WorldFile.cs:746-762）
415	    let iter = 0;
416	    let lastYield = performance.now();
417	    for (let round = 0; round < MAX_ROUNDS; round++) {
418	      const MAX_ITER = mode === 'gen' ? Math.max(1000, (sim.numLiquid + sim.bufferLen) * 5) : 100000;
419	      let roundIter = 0;
420	      while (sim.numLiquid > 0 && roundIter < MAX_ITER) {
421	        sim.updateLiquid();
422	        iter++; roundIter++;
423	        if (roundIter % 2000 === 0) {
424	          onProgress?.(0.35 + Math.min(0.6, iter / 20000));
425	          if (performance.now() - lastYield >= 32) {
426	            await new Promise((r) => setTimeout(r, 0));
427	            lastYield = performance.now();
428	          }
429	        }
430	      }
431	      sim.waterCheck();
432	      if (sim.numLiquid === 0) break;
433	    }
434	    sim.quickSettle = false;
435	    sim.waterCheck(); // 残留活水交给运行时收敛（原版 WorldFile.cs:769 同款）
436	    sim.dispose();
437	    onProgress?.(1);
438	  }
439	
440	  async loadWorld(world: World, onProgress?: (label: string, p: number) => void) {
441	    this.world = world;
442	    onProgress?.('水体沉降', 0.5);
443	    // 读档模式：原版 WorldFile 单轮语义（存档水体已静止，QuickWater+WaterCheck 后
444	    // 活水极少，单轮快速收敛；残留交给运行时——不再跑生成期的 10 轮全沉降）
445	    await this.settleLiquids((p) => onProgress?.('水体沉降', p * 0.8), 'load');
446	    await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.8 + p * 0.2));
447	    this.afterWorldLoad();
448	    this.cb.onWorldReady();
449	  }
450	
451	  private afterWorldLoad() {
452	    const w = this.world;
453	    // 原版墙渲染器（TEdit WallFraming 移植；墙 id 直用 wld id，贴图 Wall_N.png）
454	    const wallTiler = this.atlas ? new VanillaWallTiler(this.atlas) : null;
455	    this.chunks = new ChunkCache(w, this.assets.tileSheets, this.autotiler, wallTiler);
456	    // 懒加载晚到的新图块/墙表 → 全量标脏重烘焙:出生点子集预载后,远行遇到
457	    // 新类型时 vframe 先返回 null(fallback 烤进 chunk),表到位后此回调修正
458	    if (this.atlas) {
459	      this.atlas.onVImageLoaded = () => this.chunks.invalidateAll();
460	    }
461	    // 电路系统(Wiring.cs 移植):器件表 + 触发源登记(测重板 428/感应器 423)
462	    this.wiring = new Wiring(w.store);
463	    this.wiring.worldSurface = w.groundLevel;
464	    attachDevices(this.wiring, this.makeDeviceCtx());
465	    this.scanTriggerTiles();
466	    this.lighting = new LightingEngine(w);
467	    this.liquid = new LiquidSim(w);
468	    // 1456 AddWater/WaterCheck 尾部 KillTile（液体冲毁火把等）：走 breakTile（掉落+音效+帧刷新）
469	    this.liquid.killTile = (x, y) => this.breakTile(x, y);
470	    this.liquid.waterCheck(); // 原版读档末尾的 WaterCheck：把沉降后仍可流动的少量格子交给运行时收敛
471	    this.camera = new Camera(w.w, w.h);
472	    this.renderer.minimap = new Minimap(w);
473	    this.entities.clear();
474	    this.player = new Player(w.spawnX * TILE + 8, (w.spawnY - 3) * TILE, new Inventory()); // 主角 3 格高，抬高出生点
475	    // 初始装备（铁器三件套与 Maples 素材对齐；含药水与配饰便于体验 Buff/配饰系统）
476	    this.player.inv.add(ITEM_BY_KEY['iron_pickaxe'], 1);
477	    this.player.inv.add(ITEM_BY_KEY['iron_axe'], 1);
478	    this.player.inv.add(ITEM_BY_KEY['iron_sword'], 1);
479	    // 铁弓 + 木箭（射击系统测试；PickAmmo 会自动按 ammoId 找背包任意箭）

```


---

## 🤖 Assistant · 2026-08-10T06:28:13.767Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts",
 "offset": 150,
 "limit": 130
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:13.772Z

**📎 ToolResult**

```
150	    clock: { timeOfDay: world.clock.timeOfDay, dayCount: world.clock.dayCount },
151	    tiles: bytesToB64(rleTiles(st)),
152	    walls: bytesToB64(rlePairs(st.wall)),
153	    liquid: bytesToB64(rlePairs(st.liquid)),
154	    liquidType: bytesToB64(rlePairs(st.liquidType)),
155	    wire: bytesToB64(rlePairs(st.wire)),
156	    chests: world.chests,
157	    player: {
158	      hp: player.hp, x: player.x, y: player.y,
159	      inventory: player.inv.slots, selected: player.inv.selected,
160	      baseMaxHp: player.baseMaxHp, baseMaxMana: player.baseMaxMana, mana: player.mana,
161	    },
162	    npcs: [],
163	    signs: world.signs,
164	    flags: world.flags,
165	  };
166	  return JSON.stringify(data);
167	}
168	
169	export function loadSave(json: string): ReturnType<typeof loadSaveData> {
170	  return loadSaveData(JSON.parse(json) as SaveData);
171	}
172	
173	/** 直接从内存 SaveData 构建(导入 .wld 路径用——跳过 stringify→parse 双拷贝,
174	 *  2026-08 审计 #3:该往返单次 20~50MB×2) */
175	export function loadSaveData(data: SaveData): { world: World; player: SaveData['player'] } {
176	  const world = new WorldClass(data.header.width, data.header.height, data.header.seed, data.header.name);
177	  world.spawnX = data.header.spawn[0];
178	  world.spawnY = data.header.spawn[1];
179	  world.groundLevel = data.header.groundLevel;
180	  world.rockLevel = data.header.rockLevel;
181	  // 旧档缺 lavaLine（原版 UnderworldLayer = maxTilesY-200）
182	  world.lavaLine = data.header.lavaLine ?? data.header.height - 200;
183	  if (data.header.treeX) world.treeX = data.header.treeX;
184	  if (data.header.treeStyle) world.treeStyle = data.header.treeStyle;
185	  if (data.header.treeTops?.length) world.treeTops = data.header.treeTops;
186	  if (data.header.crimson !== undefined) world.crimson = data.header.crimson;
187	  if (data.header.dungeonX !== undefined) world.dungeonX = data.header.dungeonX;
188	  // dungeonY 缺省（旧档/导入）回退地表线：CheckToSpawnDungeonEnemies 的 pY<dungeonY+40 门槛近似成立
189	  if (data.header.dungeonY !== undefined && data.header.dungeonY > 0) world.dungeonY = data.header.dungeonY;
190	  else world.dungeonY = world.groundLevel;
191	  if (data.header.jungleX !== undefined) world.jungleX = data.header.jungleX;
192	  world.clock.timeOfDay = data.clock.timeOfDay;
193	  world.clock.dayCount = data.clock.dayCount;
194	  world.chests = data.chests;
195	  world.flags = data.flags;
196	  if (data.signs) world.signs = data.signs;
197	
198	  const st = world.store;
199	  // tiles
200	  {
201	    const u8 = b64ToBytes(data.tiles);
202	    const pos = { i: 0 };
203	    let i = 0;
204	    while (i < st.type.length && pos.i < u8.length) {
205	      const run = readVarint(u8, pos) + 1;
206	      const t = readVarint(u8, pos);
207	      let fx = 0, fy = 0;
208	      if (t !== 0) {
209	        fx = readVarint(u8, pos);
210	        fy = readVarint(u8, pos);
211	      }
212	      for (let k = 0; k < run && i < st.type.length; k++, i++) {
213	        st.type[i] = t; st.flags[i] = t !== 0 ? 1 : 0;
214	        st.frameX[i] = fx; st.frameY[i] = fy;
215	      }
216	    }
217	  }
218	  // walls（version<2 的旧档墙值迁移：1=土→2, 2=石→1, 3=木→4（现为原版 id））
219	  {
220	    const legacy = (data.version ?? 1) < 2;
221	    const migrate = (v: number) => (legacy ? (v === 1 ? 2 : v === 2 ? 1 : v === 3 ? 4 : v) : v);
222	    const u8 = b64ToBytes(data.walls);
223	    const pos = { i: 0 };
224	    let i = 0;
225	    while (i < st.wall.length && pos.i < u8.length) {
226	      const run = readVarint(u8, pos) + 1;
227	      const v = migrate(readVarint(u8, pos));
228	      for (let k = 0; k < run && i < st.wall.length; k++, i++) st.wall[i] = v;
229	    }
230	  }
231	  // wire 电路位（旧存档缺此字段 → 全 0 = 无导线，缺字段容忍同 liquidType）
232	  {
233	    const u8 = b64ToBytes(data.wire ?? '');
234	    const pos = { i: 0 };
235	    let i = 0;
236	    while (i < st.wire.length && pos.i < u8.length) {
237	      const run = readVarint(u8, pos) + 1;
238	      const v = readVarint(u8, pos);
239	      for (let k = 0; k < run && i < st.wire.length; k++, i++) st.wire[i] = v;
240	    }
241	  }
242	  // liquid type（旧存档缺此字段 → 全 0，由液体模拟按 1=水 补全）
243	  {
244	    const u8 = b64ToBytes(data.liquidType ?? '');
245	    const pos = { i: 0 };
246	    let i = 0;
247	    while (i < st.liquidType.length && pos.i < u8.length) {
248	      const run = readVarint(u8, pos) + 1;
249	      const v = readVarint(u8, pos);
250	      for (let k = 0; k < run && i < st.liquidType.length; k++, i++) st.liquidType[i] = v;
251	    }
252	  }
253	  // liquid
254	  {
255	    const u8 = b64ToBytes(data.liquid);
256	    const pos = { i: 0 };
257	    let i = 0;
258	    while (i < st.liquid.length && pos.i < u8.length) {
259	      const run = readVarint(u8, pos) + 1;
260	      const v = readVarint(u8, pos);
261	      for (let k = 0; k < run && i < st.liquid.length; k++, i++) st.liquid[i] = v;
262	    }
263	  }
264	  return { world, player: data.player };
265	}
266	

```


---

## 🤖 Assistant · 2026-08-10T06:28:13.958Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts",
 "limit": 120
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:13.970Z

**📎 ToolResult**

```
1	// SoA 多通道平面数组存储。所有热点代码只碰 TypedArray。
2	import { TILE_DEFS } from '../data/tiles';
3	
4	export class TileStore {
5	  readonly w: number;
6	  readonly h: number;
7	  readonly type: Uint16Array;
8	  readonly flags: Uint8Array; // bit0 active bit1 framedDecor占位(预留)
9	  readonly frameX: Uint16Array;
10	  readonly frameY: Uint16Array;
11	  readonly wall: Uint16Array; // 原版 wld 墙 id（0-366）
12	  readonly liquid: Uint8Array;   // 0-255 液量
13	  readonly liquidType: Uint8Array; // 0无 1水 2岩浆 3蜂蜜
14	  readonly half: Uint8Array;      // halfBrick 位（原版 Tile.cs bTileHeader bit1）：下半 8px 实心
15	  readonly slope: Uint8Array;     // 坡面 0-4（原版编码；渲染暂未支持，生成期少用）
16	  readonly wire: Uint8Array;      // 电路位（原版 Tile.cs sTileHeader）：bit0红 bit1蓝 bit2绿 bit3黄 bit4致动器 bit5已致动(inActive)
17	  // wire 位掩码常量（对应原版 Tile.cs:396-459 的 wire/wire2/wire3/wire4/actuator/inActive）
18	  static readonly WIRE_RED = 1;
19	  static readonly WIRE_BLUE = 2;
20	  static readonly WIRE_GREEN = 4;
21	  static readonly WIRE_YELLOW = 8;
22	  static readonly WIRE_ACTUATOR = 16;
23	  static readonly WIRE_ACTUATED = 32;
24	  static readonly WIRE_COLORS = 15; // 四色掩码
25	
26	  // tile 变更监听（chunk 缓存 / 光照脏标记 / 液体模拟统一从这里拿事件）
27	  private listeners: Array<(x: number, y: number) => void> = [];
28	
29	  constructor(w: number, h: number) {
30	    this.w = w; this.h = h;
31	    const n = w * h;
32	    this.type = new Uint16Array(n);
33	    this.flags = new Uint8Array(n);
34	    this.frameX = new Uint16Array(n);
35	    this.frameY = new Uint16Array(n);
36	    this.wall = new Uint16Array(n);
37	    this.liquid = new Uint8Array(n);
38	    this.liquidType = new Uint8Array(n);
39	    this.half = new Uint8Array(n);
40	    this.slope = new Uint8Array(n);
41	    this.wire = new Uint8Array(n);
42	  }
43	
44	  idx(x: number, y: number): number { return y * this.w + x; }
45	
46	  inBounds(x: number, y: number): boolean {
47	    return x >= 0 && y >= 0 && x < this.w && y < this.h;
48	  }
49	
50	  get(x: number, y: number): number { return this.inBounds(x, y) ? this.type[this.idx(x, y)] : 0; }
51	
52	  isActive(x: number, y: number): boolean {
53	    // 原版 nactive() = active && !inActive（Tile.cs:383-394）：已致动格视为不活跃
54	    return this.inBounds(x, y) && this.type[this.idx(x, y)] !== 0
55	      && (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) === 0;
56	  }
57	
58	  /** 原版 inActive()：致动器翻转后的"缩入地下"态（有 type 但不碰撞不阻挡） */
59	  isActuated(x: number, y: number): boolean {
60	    return this.inBounds(x, y) && (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) !== 0;
61	  }
62	
63	  isSolid(x: number, y: number): boolean {
64	    if (!this.inBounds(x, y)) return false; // 世界外视为空（边缘自由）
65	    if (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) return false; // 已致动不碰撞
66	    const d = TILE_DEFS[this.type[this.idx(x, y)]];
67	    return !!d && d.solid;
68	  }
69	
70	  isPlatform(x: number, y: number): boolean {
71	    if (!this.inBounds(x, y)) return false;
72	    const d = TILE_DEFS[this.type[this.idx(x, y)]];
73	    return !!d && d.platform;
74	  }
75	
76	  onTileChanged(fn: (x: number, y: number) => void) {
77	    this.listeners.push(fn);
78	  }
79	
80	  /** 液体变化独立通道：chunk 缓存不订阅（水不入烘焙画布，无需重建），
81	   *  只有光照订阅（水的光衰减）——避免水流时每帧冲爆 chunk 重建队列造成卡顿 */
82	  private liquidListeners: Array<(x: number, y: number) => void> = [];
83	  onLiquidChanged(fn: (x: number, y: number) => void) {
84	    this.liquidListeners.push(fn);
85	  }
86	
87	  /** 唯一的写入入口（生成/导入期可绕过用 setTileSilent） */
88	  setTile(x: number, y: number, type: number, frameX = 0, frameY = 0) {
89	    if (!this.inBounds(x, y)) return;
90	    const i = this.idx(x, y);
91	    this.type[i] = type;
92	    this.flags[i] = type !== 0 ? 1 : 0;
93	    this.frameX[i] = frameX;
94	    this.frameY[i] = frameY;
95	    if (type === 0) { this.half[i] = 0; this.slope[i] = 0; } // 挖除清半砖/坡面
96	    this.listeners.forEach((fn) => fn(x, y));
97	  }
98	
99	  /** 运行期改半砖/坡面位（锤子交互用；生成期直接写数组即可） */
100	  setHalfBrick(x: number, y: number, v: boolean) {
101	    if (!this.inBounds(x, y)) return;
102	    const i = this.idx(x, y);
103	    this.half[i] = v ? 1 : 0;
104	    this.listeners.forEach((fn) => fn(x, y));
105	  }
106	
107	  setSlope(x: number, y: number, s: number) {
108	    if (!this.inBounds(x, y)) return;
109	    const i = this.idx(x, y);
110	    this.slope[i] = s;
111	    this.half[i] = 0; // 原版 SlopeTile 无条件 halfBrick(false)（WorldGen.cs:49174），slope=0 复位时同样
112	    this.listeners.forEach((fn) => fn(x, y));
113	  }
114	
115	  setTileSilent(x: number, y: number, type: number, frameX = 0, frameY = 0) {
116	    if (!this.inBounds(x, y)) return;
117	    const i = this.idx(x, y);
118	    this.type[i] = type;
119	    this.flags[i] = type !== 0 ? 1 : 0;
120	    this.frameX[i] = frameX;

```


---

## 🤖 Assistant · 2026-08-10T06:28:16.436Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I'm in plan mode. I'm a read-only planning agent. I should continue exploring key files, then produce a detailed plan as my final message. The system says I may create a plan file at a specific path — but my agent instructions say don't write report files and return findings directly. The plan-mode reminder says I "should create your plan at ... if you need to." The parent expects text output. I'll just return the plan as text.

Let me read a few more files: mainFlow.ts (relevant sections), World.ts, KvStore.ts, LiquidSim.ts constructor/dispose, GenWorldPreview, vite.config, UIWorldLoadState, and probe files.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:28:16.569Z · glm-x-preview-260804

```
继续抽查调用链与其余关键文件。
```


---

## 🤖 Assistant · 2026-08-10T06:28:16.784Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/mainFlow.ts",
 "limit": 160,
 "offset": 140
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:16.790Z

**📎 ToolResult ⚠️ERROR**

```
File does not exist. Note: your current working directory is ~/Project/GLM/SandboxWorld/game.

```


---

## 🤖 Assistant · 2026-08-10T06:28:16.943Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/World.ts",
 "limit": 100
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:16.948Z

**📎 ToolResult**

```
1	// 世界门面：TileStore + 元数据 + 实体容器 + 昼夜时钟
2	import { TileStore } from './TileStore';
3	import { T, TILE_DEFS } from '../data/tiles';
4	
5	export interface ChestData { x: number; y: number; items: Array<{ id: number; stack: number } | null>; locked?: boolean; }
6	
7	export class Clock {
8	  timeOfDay: number = 0.3;   // 0-1，0=午夜 0.5=正午（起始上午 7:12 ≈ 0.3）
9	  dayCount: number = 1;
10	  readonly dayLengthMs: number;
11	  constructor(dayLengthMs: number) { this.dayLengthMs = dayLengthMs; }
12	  tick(dtMs: number) {
13	    this.timeOfDay += dtMs / this.dayLengthMs;
14	    while (this.timeOfDay >= 1) { this.timeOfDay -= 1; this.dayCount++; }
15	  }
16	  get isDay(): boolean { return this.timeOfDay > 0.25 && this.timeOfDay < 0.75; }
17	  get dayFactor(): number {
18	    // 昼夜平滑系数：白天 1，夜晚 0.32（月光下地表仍可见，火把不再像贴在黑幕上），晨昏过渡
19	    const t = this.timeOfDay;
20	    if (t > 0.28 && t < 0.72) return 1;
21	    if (t >= 0.72 && t < 0.80) return 1 - (t - 0.72) / 0.08 * 0.68;
22	    if (t >= 0.80 || t < 0.20) return 0.32;
23	    return 0.32 + (t - 0.20) / 0.08 * 0.68;
24	  }
25	  get hourFloat(): number { return this.timeOfDay * 24; }
26	}
27	
28	export class World {
29	  store: TileStore;
30	  name: string;
31	  seed: number;
32	  spawnX = 0; spawnY = 0;
33	  groundLevel = 0; rockLevel = 0;   // tile 坐标
34	  /** 地狱顶（原版 UnderworldLayer = maxTilesY-200；TerrainPass 设定，SceneMetrics/BGM/背景共用） */
35	  lavaLine = 0;
36	  clock: Clock;
37	  chests: ChestData[] = [];
38	  /** 墓碑碑文（原版 Sign 系统的最小子集）：锚点 = 墓碑 tile 左上格 */
39	  signs: Array<{ x: number; y: number; text: string }> = [];
40	  // Boss 进度旗标
41	  flags: Record<string, boolean> = { downedEyeOfCthulhu: false, downedSkeletron: false, shadowOrbSmashed: false, hardMode: false };
42	  // 树登记：砍树干时找到整棵树（roots → 范围）
43	  trees: Array<{ x: number; y: number; h: number }> = [];
44	  /** 战争迷雾：1 = 已探索。按 tile 粒度。 */
45	  explored: Uint8Array;
46	  /** 原版树样式数据（header treeX/treeStyle）：横向 4 区森林树冠样式 */
47	  treeX: number[] = [];
48	  treeStyle: number[] = [0, 0, 0, 0];
49	  /** 世界级生物群系常量(原版 header,生成期 Reset pass 掷出) */
50	  crimson = false;          // true=猩红 false=腐化
51	  dungeonX = 0;            // 地牢位置
52	  /** 地牢入口地表 Y（原版 Main.dungeonY：CheckToSpawnDungeonEnemies 要求玩家在其 +40 格以下才刷地牢怪）。
53	   *  缺省 0=未知，使用处以 groundLevel 回退 */
54	  dungeonY = 0;
55	  jungleX = 0;             // 丛林位置
56	  /** TreeTops 13 区域变体（v≥211 wld 权威；索引 0-3 森林/5 丛林/6 雪/7 神圣） */
57	  treeTops: number[] = [];
58	
59	  exploredVersion = 0;
60	  markExplored(cx: number, cy: number, radius: number) {
61	    this.exploredVersion++;
62	    const st = this.store;
63	    const x0 = Math.max(0, cx - radius), x1 = Math.min(st.w - 1, cx + radius);
64	    const y0 = Math.max(0, cy - radius), y1 = Math.min(st.h - 1, cy + radius);
65	    for (let y = y0; y <= y1; y++) {
66	      for (let x = x0; x <= x1; x++) {
67	        if ((x - cx) ** 2 + (y - cy) ** 2 <= radius * radius) {
68	          this.explored[y * st.w + x] = 1;
69	        }
70	      }
71	    }
72	  }
73	
74	  constructor(w: number, h: number, seed: number, name = '新世界') {
75	    this.store = new TileStore(w, h);
76	    this.explored = new Uint8Array(w * h);
77	    this.seed = seed;
78	    this.name = name;
79	    // 1 游戏日 = 30 现实分钟（24→40 后折中）
80	    this.clock = new Clock(30 * 60 * 1000);
81	  }
82	
83	  get w() { return this.store.w; }
84	  get h() { return this.store.h; }
85	  get tiles() { return this.store; }
86	
87	  /** 破坏一个 tile（含 framed 物体的锚点处理由调用方负责），返回掉落 item key */
88	  breakTileAt(x: number, y: number): string | null {
89	    const t = this.store.get(x, y);
90	    if (t === 0) return null;
91	    const d = TILE_DEFS[t];
92	    this.store.setTile(x, y, 0);
93	    // v_ 图块无显式 drop → 回退同名放置物品(阶段5 自动注册)
94	    return d.drop ?? (d.key.startsWith('v_') ? 'place_' + d.key : null);
95	  }
96	
97	  isSolidPx(px: number, py: number): boolean {
98	    return this.store.isSolid(Math.floor(px / 16), Math.floor(py / 16));
99	  }
100	

```


---

## 🤖 Assistant · 2026-08-10T06:28:17.104Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:17.116Z

**📎 ToolResult**

```
1	// 键值存储：优先 IndexedDB（容量数百 MB+，大地图存档不受 localStorage ~5MB 限制），
2	// localStorage 作为小存档缓存与回退。async API，调用方 await。
3	const DB_NAME = 'sandboxworld';
4	const STORE = 'kv';
5	let dbPromise: Promise<IDBDatabase> | null = null;
6	
7	function openDb(): Promise<IDBDatabase> {
8	  if (dbPromise) return dbPromise;
9	  dbPromise = new Promise((resolve, reject) => {
10	    const req = indexedDB.open(DB_NAME, 1);
11	    req.onupgradeneeded = () => {
12	      if (!req.result.objectStoreNames.contains(STORE)) req.result.createObjectStore(STORE);
13	    };
14	    req.onsuccess = () => resolve(req.result);
15	    req.onerror = () => reject(req.error);
16	  });
17	  return dbPromise;
18	}
19	
20	/** 是否有某 key（IndexedDB 或 localStorage） */
21	export async function kvHas(key: string): Promise<boolean> {
22	  if (localStorage.getItem(key) !== null) return true;
23	  try {
24	    const db = await openDb();
25	    return await new Promise<boolean>((resolve) => {
26	      const tx = db.transaction(STORE, 'readonly');
27	      const req = tx.objectStore(STORE).getKey(key);
28	      req.onsuccess = () => resolve(req.result !== undefined);
29	      req.onerror = () => resolve(false);
30	    });
31	  } catch {
32	    return false;
33	  }
34	}
35	
36	/** 读取（IndexedDB 优先——大存档只进 IDB，localStorage 可能留着旧的小存档；
37	   读取顺序必须与写入优先级一致，否则会读到过期档） */
38	export async function kvGet(key: string): Promise<string | null> {
39	  try {
40	    const db = await openDb();
41	    const idbVal = await new Promise<string | null>((resolve) => {
42	      const tx = db.transaction(STORE, 'readonly');
43	      const req = tx.objectStore(STORE).get(key);
44	      req.onsuccess = () => resolve(typeof req.result === 'string' ? req.result : null);
45	      req.onerror = () => resolve(null);
46	    });
47	    if (idbVal !== null) return idbVal;
48	  } catch { /* IDB 不可用 → 回退 localStorage */ }
49	  return localStorage.getItem(key);
50	}
51	
52	/** 写入：字符串 ≤ 2MB 进 localStorage（快速路径），否则只进 IndexedDB */
53	export async function kvSet(key: string, value: string): Promise<'local' | 'idb' | 'fail'> {
54	  if (value.length <= 2 * 1024 * 1024) {
55	    try {
56	      localStorage.setItem(key, value);
57	      return 'local';
58	    } catch { /* 超限或被禁 → 落 IndexedDB */ }
59	  }
60	  try {
61	    const db = await openDb();
62	    await new Promise<void>((resolve, reject) => {
63	      const tx = db.transaction(STORE, 'readwrite');
64	      tx.objectStore(STORE).put(value, key);
65	      tx.oncomplete = () => resolve();
66	      tx.onerror = () => reject(tx.error);
67	    });
68	    return 'idb';
69	  } catch {
70	    return 'fail';
71	  }
72	}
73	
74	/** 删除（两处都清） */
75	export async function kvDelete(key: string): Promise<void> {
76	  localStorage.removeItem(key);
77	  try {
78	    const db = await openDb();
79	    await new Promise<void>((resolve, reject) => {
80	      const tx = db.transaction(STORE, 'readwrite');
81	      tx.objectStore(STORE).delete(key);
82	      tx.oncomplete = () => resolve();
83	      tx.onerror = () => reject(tx.error);
84	    });
85	  } catch { /* IDB 不可用则忽略 */ }
86	}
87	

```


---

## 🤖 Assistant · 2026-08-10T06:28:18.627Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
mainFlow.ts is not at src/ui/mainFlow.ts. Let me find it.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:28:18.965Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src -name \"mainFlow*\" -o -name \"*GenWorldPreview*\" -o -name \"vite.config*\" | head -20",
 "description": "Locate mainFlow, preview, vite config"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:18.996Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts
~/Project/GLM/SandboxWorld/game/src/vui/states/GenWorldPreview.ts

```


---

## 🤖 Assistant · 2026-08-10T06:28:19.577Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"onWorldPartial\\|GenWorldPreview\\|attachWorld\" -r ~/Project/GLM/SandboxWorld/game/src --include=*.ts -l",
 "description": "Find onWorldPartial usages"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:19.599Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-10T06:28:20.724Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/mainFlow.ts",
 "limit": 150,
 "offset": 140
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:20.739Z

**📎 ToolResult**

```
140	      ui.showProgress('读取存档…', 0.3);
141	      await g.loadWorld(world, (label, p) => ui.showProgress(label, 0.3 + p * 0.6));
142	      g.player.hp = player.hp;
143	      g.player.x = player.x;
144	      g.player.y = player.y;
145	      // 上限扩容进度（水晶之心/生命果/魔力水晶；旧档缺省 100/20/20）
146	      if (player.baseMaxHp !== undefined) g.player.baseMaxHp = player.baseMaxHp;
147	      if (player.baseMaxMana !== undefined) g.player.baseMaxMana = player.baseMaxMana;
148	      if (player.mana !== undefined) g.player.mana = player.mana;
149	      g.player.inv.slots = player.inventory.concat(Array(Math.max(0, INV_SIZE - player.inventory.length)).fill(null));
150	      g.player.inv.selected = player.selected;
151	    } catch (e) {
152	      console.error(e);
153	      ui.hideProgress();
154	      alert('存档读取失败：' + (e as Error).message);
155	    }
156	  }
157	
158	  async function importWld(buf: Uint8Array) {
159	    ui.showProgress('正在解析 .wld 地图…', 0.1);
160	    try {
161	      const { save, report, seedText, gameMode } = parseWldToSave(buf);
162	      (window as unknown as { __lastCompatReport?: unknown }).__lastCompatReport = report;
163	      ui.showProgress('正在转换世界…', 0.7);
164	      const g = makeGame();
165	      // 直接消费内存 SaveData(2026-08 审计 #3:此前的 stringify→parse 双拷贝
166	      // 每次导入多出 2×20~50MB 峰值,且让 5 份全图副本并存更久)
167	      const { world } = loadSaveData(save);
168	      await g.loadWorld(world, (label, p) => ui.showProgress(label, 0.7 + p * 0.3));
169	      g.player.inv.add(ITEM_BY_KEY['copper_pickaxe'], 1);
170	      g.player.inv.add(ITEM_BY_KEY['copper_axe'], 1);
171	      g.player.inv.add(ITEM_BY_KEY['copper_sword'], 1);
172	      g.player.inv.add(ITEM_BY_KEY['torch'], 20);
173	      ui.toast(`成功导入「${save.header.name}」(v${save.header.wldVersion})`);
174	      // 登记世界槽位并持久化：导入不再是一次性的，重进游戏可在世界列表中看到并继续游玩
175	      await worldStore.ensureLoaded();
176	      const names = new Set(worldStore.list().map((m) => m.name));
177	      let name = save.header.name;
178	      if (names.has(name)) {
179	        let i = 2;
180	        while (names.has(`${name} (${i})`)) i++;
181	        name = `${name} (${i})`;
182	      }
183	      currentWorld = await worldStore.register({
184	        name, seed: seedText || String(save.header.seed),
185	        w: save.header.width, h: save.header.height,
186	        difficulty: gameMode, evil: save.header.crimson ? 1 : 0,
187	      });
188	      doSave();
189	      // 兼容报告：有降级/跳过内容时弹窗
190	      const rpt = (window as unknown as { __lastCompatReport?: import('./ui/UI').CompatReport }).__lastCompatReport;
191	      if (rpt && (rpt.tilesDegraded.length || rpt.tilesCleared.length || rpt.itemsSkipped.length)) {
192	        ui.showCompatReport(rpt);
193	      }
194	    } catch (e) {
195	      console.error(e);
196	      ui.hideProgress();
197	      alert('.wld 导入失败：' + (e as Error).message);
198	    }
199	  }
200	
201	  // ---- 菜单 ----
202	
203	  /** 帧回调注入 VUI 自愈循环（VUI.startLoop 持有 rAF，HMR 杀不死） */
204	  VUI.frameHook = (dt) => {
205	    menuBg?.tick(dt);
206	    if (menuBg) menuBg.lastDt = dt;
207	  };
208	
209	  function stopMenu() {
210	    menuBg?.destroy();
211	    menuBg = null;
212	    legacyShim?.remove();
213	    legacyShim = null;
214	    // 进游戏前清空 VUI（游戏内 UI 走 DOM，生成页仍用 VUI）
215	    VUI.setState(null);
216	    VUI.clear();
217	  }
218	
219	  /** 角色列表（DOM）。切页前清 VUI 防穿透 */
220	  function showCharacterSelect() {
221	    VUI.setState(null);
222	    VUI.clear();
223	    titleMenu?.destroy();
224	    titleMenu = null;
225	    new CharSelectPanel(root, charStore, {
226	      onPlay: (a) => {
227	        selectedAppearance = a;
228	        showWorldSelect();
229	      },
230	      onNew: () => {
231	        new CharCreation(root, {
232	          onCreate: async (a) => {
233	            await charStore.create(a);
234	            showCharacterSelect();
235	          },
236	          onCancel: () => showCharacterSelect(),
237	        });
238	      },
239	      onBack: () => showTitle(),
240	    });
241	  }
242	
243	  /** 世界列表（DOM） */
244	  function showWorldSelect() {
245	    VUI.setState(null);
246	    VUI.clear();
247	    new WorldSelectPanel(root, worldStore, {
248	      onPlay: (meta) => void loadWorldFlow(meta),
249	      onNew: () => {
250	        // 世界创建页（DOM）
251	        VUI.setState(null);
252	        VUI.clear();
253	        new WorldCreationPanel(root, {
254	          onCreate: (cfg) => void createWorldFlow(cfg),
255	          onCancel: () => showWorldSelect(),
256	        });
257	      },
258	      onBack: () => showCharacterSelect(),
259	    });
260	  }
261	
262	  /** 从世界槽位读取并进入游戏 */
263	  async function loadWorldFlow(meta: WorldMeta) {
264	    const text = await worldStore.load(meta);
265	    if (!text) { ui.toast('世界数据缺失或损坏'); return; }
266	    currentWorld = meta;
267	    await loadFromJson(text);
268	  }
269	
270	  /** 创建新世界：原版生成页（双进度条+实时地图预览）→ 注册槽位 → 进游戏 */
271	  async function createWorldFlow(cfg: { name: string; seed: string; w: number; h: number; difficulty: number; evil: -1 | 0 | 1 }) {
272	    const loadState = new UIWorldLoadState(cfg.evil);
273	    VUI.setState(loadState);
274	    const g = makeGame();
275	    await g.newWorld(cfg.seed || String(Date.now()), cfg.w, cfg.h,
276	      (label, p) => loadState.setProgress(label, p),
277	      {
278	        name: cfg.name,
279	        evil: cfg.evil,
280	        onWorldPartial: (world) => loadState.attachWorld(world),
281	      });
282	    // onWorldReady 已进游戏；登记世界槽位并保存初始数据
283	    const meta = await worldStore.register({
284	      name: cfg.name, seed: cfg.seed, w: cfg.w, h: cfg.h,
285	      difficulty: cfg.difficulty, evil: cfg.evil,
286	    });
287	    currentWorld = meta;
288	    doSave();
289	  }

```


---

## 🤖 Assistant · 2026-08-10T06:28:20.806Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/vui/states/GenWorldPreview.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:20.814Z

**📎 ToolResult**

```
1	// 生成期实时世界地图预览（用户特有需求；原版 1.4.0.5 无此功能）。
2	// 策略：离屏 canvas（1px/tile）+ 每帧限量「列扫描」增量重绘（等价原版 DrawToMap 的
3	// maxMapUpdates 限额思想）；生成中数据持续变化，扫描循环刷新而非脏块跟踪
4	// （生成期 setTileSilent 不触发 onTileChanged）。
5	import { UIElement } from '../core/UIElement';
6	import { StyleDimension } from '../core/StyleDimension';
7	import type { UISpriteBatch } from '../draw/UISpriteBatch';
8	import { rgb } from '../draw/UISpriteBatch';
9	import { UIScale } from '../draw/UIScale';
10	import { mapColor24 } from '../../render/MapColors';
11	import type { World } from '../../world/World';
12	
13	/** 每帧重绘的列数（列 = 全高 1px 宽；8400 列大世界约 2 秒扫完一轮） */
14	const COLUMNS_PER_FRAME = 64;
15	
16	export class GenWorldPreview extends UIElement {
17	  private off: HTMLCanvasElement;
18	  private offCtx: CanvasRenderingContext2D;
19	  private colImg: ImageData;
20	  private sweepCol = 0;
21	
22	  constructor(private world: World) {
23	    super();
24	    this.off = document.createElement('canvas');
25	    this.off.width = world.w;
26	    this.off.height = world.h;
27	    this.offCtx = this.off.getContext('2d')!;
28	    this.colImg = this.offCtx.createImageData(1, world.h);
29	    // 底部居中：宽度取屏宽 55%（上限 520），高度按世界纵横比等比缩放（不变形）；
30	    // 底部留 56px 避开小贴士行
31	    const w = Math.min(UIScale.logicalW * 0.55, 520);
32	    const h = w * (world.h / world.w);
33	    this.width = StyleDimension.fromPixels(w);
34	    this.height = StyleDimension.fromPixels(h);
35	    this.hAlign = 0.5;
36	    this.vAlign = 1;
37	    this.marginBottom = 56;
38	  }
39	
40	  update(): void {
41	    this.sweep();
42	    super.update();
43	  }
44	
45	  /** 列扫描增量重绘（每帧限量防卡顿） */
46	  private sweep() {
47	    const st = this.world.store;
48	    const w = this.world.w, h = this.world.h;
49	    const data = this.colImg.data;
50	    let n = COLUMNS_PER_FRAME;
51	    while (n-- > 0) {
52	      const x = this.sweepCol;
53	      for (let y = 0; y < h; y++) {
54	        const c = mapColor24(st, x, y);
55	        const i = y * 4;
56	        data[i] = (c >> 16) & 255;
57	        data[i + 1] = (c >> 8) & 255;
58	        data[i + 2] = c & 255;
59	        data[i + 3] = 255;
60	      }
61	      this.offCtx.putImageData(this.colImg, x, 0);
62	      this.sweepCol = (x + 1) % w;
63	      if (this.sweepCol === 0) break; // 扫完一轮，下一帧从头
64	    }
65	  }
66	
67	  protected drawSelf(batch: UISpriteBatch): void {
68	    const d = this.getDimensions();
69	    if (d.width <= 0 || d.height <= 0) return;
70	    batch.draw({ img: this.off, sx: 0, sy: 0, sw: this.off.width, sh: this.off.height },
71	      d.x, d.y, { scaleX: d.width / this.off.width, scaleY: d.height / this.off.height });
72	    // 边框
73	    batch.fillRect(d.x, d.y, d.width, 2, rgb(0, 0, 0, 160));
74	    batch.fillRect(d.x, d.y + d.height - 2, d.width, 2, rgb(0, 0, 0, 160));
75	    batch.fillRect(d.x, d.y, 2, d.height, rgb(0, 0, 0, 160));
76	    batch.fillRect(d.x + d.width - 2, d.y, 2, d.height, rgb(0, 0, 0, 160));
77	  }
78	}
79	

```


---

## 🤖 Assistant · 2026-08-10T06:28:20.942Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/vite.config.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:20.949Z

**📎 ToolResult**

```
1	// vite/vitest 共用配置。
2	// resolve.extensions 把 .ts 提到 .js 之前：`npm run build` 的 tsc 会在 src/ 里
3	// 产出与源码同名的 .js 编译产物，默认扩展序（.js 优先）会让 vitest/vite 解析到
4	// 过期的 .js 而不是 .ts 源码（表现为改了 .ts 测试却跑旧逻辑）。
5	import { defineConfig } from 'vite';
6	
7	export default defineConfig({
8	  resolve: {
9	    extensions: ['.ts', '.mts', '.mjs', '.js', '.jsx', '.tsx', '.json'],
10	  },
11	});
12	

```


---

## 🤖 Assistant · 2026-08-10T06:28:22.358Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me check UIWorldLoadState.attachWorld, LiquidSim constructor/dispose, and probe scripts. Also check generateWorld tail (nextFrame usage, onWorldPartial). And Game.ts imports of LiquidSim.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:28:23.152Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"attachWorld\\|GenWorldPreview\" ~/Project/GLM/SandboxWorld/game/src/vui/states/UIWorldLoadState.ts | head; grep -n \"constructor\\|dispose\\|killTile\\|onTileChanged\\|onLiquidChanged\" ~/Project/GLM/SandboxWorld/game/src/sim/LiquidSim.ts | head -30",
 "description": "Check UIWorldLoadState and LiquidSim hooks"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:23.191Z

**📎 ToolResult**

```
2:// 外加用户特有需求：左侧 GenWorldPreview 实时地图预览。
9:import { GenWorldPreview } from './GenWorldPreview';
18:  private preview: GenWorldPreview | null = null;
62:  attachWorld(world: World) {
64:    this.preview = new GenWorldPreview(world);
ugrep: warning: ~/Project/GLM/SandboxWorld/game/src/sim/LiquidSim.ts: No such file or directory

```


---

## 🤖 Assistant · 2026-08-10T06:28:24.729Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 80,120p ~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts; ls ~/Project/GLM/SandboxWorld/game/scripts 2>/dev/null; ls ~/Project/GLM/SandboxWorld/game | head -30",
 "description": "Read generateWorld tail and list probes"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:24.763Z

**📎 ToolResult**

```
    await nextFrame();
    passes[i].run(ctx, () => {});
    // 部分世界回调（生成期实时预览）：pass 完成即暴露，不等 finalize
    if (cfg.onWorldPartial) cfg.onWorldPartial(world, i, passes[i].name);
  }

  finalize(ctx);
  onProgress?.('完成', 1);
  return world;
}

// ---------- 原版管线 pass(阶段 1-2 移植) ----------
import { newGenState, type GenState } from './vanilla/GenState';
import { runTerrainPass } from './vanilla/TerrainPass';
import { runRocksAndClayPass, runCavesPass } from './vanilla/CavesPass';
import { runOceanSandPass, runBeachesPass } from './vanilla/BeachPass';
import { runIceBiomePass } from './vanilla/IceBiomePass';
import { runGrassPass } from './vanilla/GrassPass';
import { runJunglePass } from './vanilla/JunglePass';
import { spreadGrassAll } from './vanilla/Spread';
import { runDesertPass } from './vanilla/DesertPass';
import { runMushroomPass } from './vanilla/MushroomPass';
import { runMarbleGranitePass } from './vanilla/MarbleGranitePass';
import { runDirtToMudAndSiltPass } from './vanilla/DirtToMudPass';
import { runCleanupPass } from './vanilla/CleanupPass';
import { runSmoothWorldPass, runWaterfallLipPass } from './vanilla/HalfBrickPass';
import { runShiniesPass, runGemsPass } from './vanilla/ShiniesPass';
import { runMountCavesPass, runMountainCavesPass } from './vanilla/MountCavesPass';
import { runTreePass, randomizeTreeStyle } from './vanilla/TreePass';
import { runLakesPass } from './vanilla/LakesPass';
import { runTrapsPass } from './vanilla/TrapsPass';
import { runFloatingIslandsPass, runLifeCrystalsPass, runSurfaceDecorPass, runPyramidPass, runWetJunglePass } from './vanilla/StructuresPass';
import { runBeehivePass, runSpiderNestPass } from './vanilla/HiveSpiderPass';
import { tileRunner } from './vanilla/TileRunner';
import { runDungeonPass } from './vanilla/DungeonPass';
import { runTemplePass } from './vanilla/TemplePass';
import { runIslandHousePass } from './vanilla/IslandHousePass';
import { runHellFortPass } from './vanilla/HellFortPass';
import { runSwordShrinePass } from './vanilla/SwordShrinePass';
import { runBuriedChestsPass, runSurfaceChestsPass, runWaterChestsPass } from './vanilla/BuriedChestsPass';
import { runCorruptionPass } from './vanilla/CorruptionPass';
_alphaprobe.mjs
_audit7.mjs
_batprobe.mjs
_biomeaudio.mjs
_biomeprobe.mjs
_bossprobe.mts
_bowprobe.mjs
_cactus3.mjs
_casterprobe.mjs
_chan.mjs
_chargerprobe.mjs
_cursor-probe.mjs
_dbgalpha.mjs
_death-probe.mjs
_dgndbg.mjs
_dukemlprobe.mts
_dungeondtrap.mjs
_dungeonprobe.mjs
_eaterai.mjs
_eaterdbg.mjs
_eaterdbg2.mjs
_eaterpix.mjs
_eyeprobe.mjs
_fighterprobe.mjs
_genwatch.mjs
_globaldg.mjs
_greenbrickprobe.mjs
_halfbrickprobe.mjs
_hud-probe.mjs
_lategameprobe.mts
_lavabottom.mjs
_liquidprobe.mjs
_lootprobe.mjs
_mapprobe.mjs
_mechprobe.mts
_minimap-btn-probe.mjs
_musicprobe.mjs
_npcprobe.mjs
_pixanal.mjs
_potprobe.mjs
_qbprobe.mts
_refdg.mjs
_seamdiag.mjs
_settleprobe.mjs
_sign-verify.mjs
_slimetintprobe.mjs
_soakprobe.mjs
_spawndbg.mjs
_spawnmoveprobe.mjs
_spawnposprobe.mjs
_spawnrateprobe.mjs
_spotdbg.mjs
_spritedbg.mjs
_swarmprobe.mjs
_tex-broken.mjs
_townnpc-pix.mjs
_townnpc.mjs
_trapdmg.mjs
_trapfire.mjs
_trapshot-tex.mjs
_waterfallprobe.mjs
_weap-probe.mts
_wofprobe.mts
_wormprobe.mjs
ascii-map.mjs
asset-audit.mjs
boss.mjs
buffs.mjs
build-atlas.mjs
build-l10n.mjs
carve-shape.mjs
char-smoke.mjs
combat.mjs
copy-sfx.mjs
door-test.mjs
feat-test.mjs
feat-test2.mjs
feat-test3.mjs
feat-test4.mjs
feat-test5.mjs
feat-test6.mjs
feat-test6b.mjs
feat-test7.mjs
feat-test8.mjs
feat-test8b.mjs
feat-test9.mjs
feat-test9b.mjs
feat-test9c.mjs
gen-audit.mjs
gen-determinism.mjs
gen-preview-smoke.mjs
gen-vanilla-test.mjs
import.mjs
interact.mjs
inv-smoke.mjs
jungle-probe.mjs
l10n-merge.d.mts
l10n-merge.mjs
l10n-smoke.mjs
lighting-test.mts
m4.mjs
probe.mjs
region-compare.mjs
roundtrip-test.mjs
runner-test.mjs
save-ascii.mjs
settings-smoke.mjs
smallholes-test.mjs
smoke.mjs
straight-test.mjs
title-smoke.mjs
vanilla-atlas.mjs
vanilla-smoke.mjs
vanilla-ui-whitelist.json
vanilla-whitelist.json
visual-check.mjs
vui-smoke.mjs
wiring-test.mts
dist
docs
index.html
node_modules
package-lock.json
package.json
probe-eoc-dead.mjs
probe-eoc-trace.mjs
probe-time-ui.mjs
public
scripts
shots
src
Starter_World Master.wld
tests
tools
tsconfig.json
vite.config.ts

```


---

## 🤖 Assistant · 2026-08-10T06:28:26.778Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
There's `gen-determinism.mjs` already! Let me check it — useful for validation plan. Also find LiquidSim location.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:28:27.249Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src -name \"LiquidSim*\"; grep -rn \"new LiquidSim\" ~/Project/GLM/SandboxWorld/game/src | head",
 "description": "Locate LiquidSim"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:27.278Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:406:    const sim = new LiquidSim(this.world);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:467:    this.liquid = new LiquidSim(w);

```


---

## 🤖 Assistant · 2026-08-10T06:28:27.444Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/scripts/gen-determinism.mjs",
 "limit": 60
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:27.452Z

**📎 ToolResult**

```
1	// 阶段2 验证:同 seed 二次生成逐 tile 一致(RNG 契约)+ 三种尺寸可生成
2	import puppeteer from 'puppeteer-core';
3	const browser = await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:'new', args:['--no-sandbox'], defaultViewport:{width:1280,height:800}});
4	const page = await browser.newPage();
5	const errs = [];
6	page.on('pageerror', e => errs.push(e.message));
7	await page.goto('http://localhost:5199', {waitUntil:'domcontentloaded', timeout:60000});
8	const out = await page.evaluate(async () => {
9	  const mod = await import('/src/world/gen/WorldGen.ts');
10	  const hash = (st) => {
11	    let h = 2166136261 >>> 0;
12	    for (let i = 0; i < st.type.length; i += 7) {
13	      h = Math.imul(h ^ st.type[i], 16777619);
14	      h = Math.imul(h ^ st.liquid[i], 16777619);
15	    }
16	    return h >>> 0;
17	  };
18	  const results = {};
19	  // 确定性
20	  const a = await mod.generateWorld({ width: 4200, height: 1200, seedText: 'det' });
21	  const b = await mod.generateWorld({ width: 4200, height: 1200, seedText: 'det' });
22	  results.deterministic = hash(a.store) === hash(b.store);
23	  // 三尺寸
24	  for (const [w, h] of [[4200, 1200], [6400, 1800], [8400, 2400]]) {
25	    const t0 = Date.now();
26	    try {
27	      const wld = await mod.generateWorld({ width: w, height: h, seedText: 'size' });
28	      const st = wld.store;
29	      let bad = 0, water = 0;
30	      for (let i = 0; i < st.type.length; i += 11) { if (st.liquid[i]) water++; }
31	      results[`${w}x${h}`] = { ms: Date.now() - t0, spawn: [wld.spawnX, wld.spawnY], waterSample: water, err: null };
32	    } catch (e) {
33	      results[`${w}x${h}`] = { ms: Date.now() - t0, err: String(e) };
34	    }
35	  }
36	  // 经典回退开关
37	  try {
38	    const c = await mod.generateWorld({ width: 4200, height: 1200, seedText: 'classic', lgcTerrain: false });
39	    results.classicFallback = { ok: c.store.type.length === 4200 * 1200 };
40	  } catch (e) { results.classicFallback = { err: String(e) }; }
41	  return results;
42	});
43	console.log(JSON.stringify(out, null, 1));
44	console.log('pageErrors:', errs.slice(0, 3));
45	await browser.close();
46	

```


---

## 🤖 Assistant · 2026-08-10T06:28:28.933Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good — gen-determinism.mjs exists and runs generateWorld in main thread via import. For worker determinism validation we'd need a new probe.

Now check LiquidSim constructor/dispose quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:28:29.433Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"constructor\\|dispose\\|killTile\\|onTileChanged\\|onLiquidChanged\\|import \" ~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts | head -20",
 "description": "Check LiquidSim constructor and dispose"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:28:29.459Z

**📎 ToolResult**

```
17:import { TILE_DEFS, TILE_BY_KEY } from '../../data/tiles';
18:import type { World } from '../World';
62:  private disposed = false;
72:  killTile: ((x: number, y: number) => void) | null = null;
78:  constructor(world: World) {
93:    st.onTileChanged((x, y) => {
94:      if (this.disposed) return;
99:    st.onLiquidChanged((x, y) => {
100:      if (this.disposed) return;
111:  dispose() {
112:    this.disposed = true;
166:      if (dies) this.killTile?.(x, y);
749:          if (st.liquidType[i] === 2) { if (this.lavaDeathIds.has(t)) this.killTile?.(x, y); }
750:          else if (this.waterDeathIds.has(t)) this.killTile?.(x, y);

```


---

## 🤖 Assistant · 2026-08-10T06:29:56.330Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I have enough. Now write the plan. It should be a detailed implementation plan covering:

1. 架构: src/workers/, message protocol, WorldGenClient
2. WorldPacket protocol
3. newWorld message chain + loadWorld chain
4. Preview design
5. Risk list
6. Phased implementation
7. Validation

Output as final message (text), with "Critical Files for Implementation" 3-5 files at the end.

Key design decisions to make and justify:

**WorldPacket**:
```ts
interface WorldPacket {
  w, h, seed, name
  scalars: {...}  // spawnX etc, clock, chests, signs, flags, trees, treeX/style/tops, exploredVersion
  arrays: {
    type: ArrayBuffer, flags, frameX, frameY, wall, liquid, liquidType, half, slope, wire, explored
  }
}
```
All transferable. Build helpers:
- `packWorld(world): { packet: WorldPacket; transfer: ArrayBuffer[] }`
- `World.fromPacket(packet): World` — static restore
- `TileStore.fromBuffers(w,h,bufs): TileStore` — static restore (bypasses listener arrays)

Important detail: TileStore fields are `readonly` TypedArrays — restore must use a static factory that constructs an empty store then assigns via a cast, or a private constructor overload. Recommend: `static restore(w,h,b: TileBuffers): TileStore` that creates instance via `Object.create` or sets fields (readonly prevents assignment → use `as` cast internally or make constructor accept optional buffers). Cleanest: change constructor to `constructor(w, h, bufs?: TileBuffers)` where bufs provided skips allocation. That keeps readonly intact.

Similarly `World.fromPacket`: `new World(w,h,seed,name)` then replace `world.store = TileStore.restore(...)` — store is not readonly (declared `store: TileStore`) so assignable. And `explored` is not readonly. Good.

**settle in worker**: settleLiquids is a private method on Game that uses setTimeout yields. In worker, we want a pure function `settleLiquids(world, mode, onProgress)` extracted into a module e.g. `src/world/liquid/settle.ts`, used both by Game (fallback path) and worker. The yield logic uses performance.now + setTimeout; in worker setTimeout exists, but since worker blocking is fine we can run it synchronously without yields (faster!) — but we still want periodic progress postMessage, which requires yielding to the event loop, so keep the async-yield version in worker to post progress. Actually in a worker, blocking is acceptable for correctness, but progress messages won't be delivered until yield. Keep yields (32ms) → progress flows.

**Worker chaining**: worker holds the World between generate and settle (no transfer back and forth) — one message `generate` request → worker does generate + settle(gen) → transfers back. This avoids double transfer. For load: `saveParse` request carrying either the JSON string (main thread reads IDB) or a key (worker reads IDB). Design decision: recommend worker-side kvGet by key.

Trade-off analysis:
- Option A: main thread kvGet → postMessage(string). Structured clone of a 20–50MB string = one memcpy (~10-25ms/10MB — actually string clone is fast, roughly memcpy speed, maybe 50–150ms for 50MB). But it doubles peak memory (main thread string + clone). Also main thread IDB read is off-thread anyway (IDB is async, doesn't block main thread much — the parsing blocks).
- Option B: worker does kvGet directly. No big-string clone at all. Worker needs KvStore import (fine, pure IDB code, no DOM — localStorage access in fallback would break in worker though! KvStore falls back to localStorage, which doesn't exist in worker → `localStorage` reference throws ReferenceError. Need a worker-safe kvGet: guard `typeof localStorage !== 'undefined'`). Recommendation: worker reads IDB via a shared worker-safe function; keep localStorage fallback only on main thread. For small saves stored in localStorage, main thread passes string. So: main thread checks localStorage first (cheap, sync), if miss → ask worker to kvGet from IDB. Simpler alternative: main thread always kvGet (it's cheap and non-blocking) and passes the string; accept clone cost. Hmm.

Actually the dominant cost is JSON.parse + RLE decode + settle. kvGet is IDB async (already off main thread). The clone cost of a 50MB string is real but modest (~50ms). But peak memory: string on main thread (50MB as UTF-16 = 100MB!) + clone in worker (100MB) = 200MB transient. Note JS strings are UTF-16 in memory, so a 50MB file = 100MB RAM. JSON.parse creates many objects. Hmm, that's significant.

Recommended: worker-side kvGet (Option B) with a `kvGetWorker` that only touches IndexedDB; main thread checks localStorage fallback before delegating (or: main thread does kvGet and passes string only when it came from localStorage; if from IDB, pass key and let worker read). Simplest robust: `loadSaveRequest = { kind:'saveParse', key } | { kind:'saveParse', json }`. worldStore.load(meta) — let me check what it does... it likely wraps kvGet. I'll note that we add a method to read raw. Also `.wld` import path: parseWldToSave produces in-memory SaveData (main thread, binary parse of the wld file — also CPU heavy but phase 2). For phase 1/2, importWld passes SaveData JSON — structured clone of SaveData object (structured clone of a big JS object is also expensive but it's one pass). Alternative: structured clone can transfer? SaveData contains strings (b64) + objects — clone is a deep copy, expensive for 50MB. Better: in importWld, stringify once (already available? parseWldToSave returns save object; we can JSON.stringify) and pass the string. Actually structured clone of a plain object graph is roughly comparable to stringify+parse... but safer/simpler: pass the SaveData object and let structured clone handle it (no JSON.parse needed in worker — we can skip stringify entirely and call loadSaveData directly in worker). That's the audit #3 lesson: avoid stringify→parse double copy. Structured clone of SaveData: one deep copy on main thread (blocking! structured clone of 50MB object happens synchronously in postMessage on main thread — could take a few hundred ms). Acceptable; note as risk. Or defer wld path to phase 2 and keep main-thread for it initially.

**Preview design**: Recommend: worker posts a downsampled preview. Options:
(a) transfer full `type` array copy every pass — 6400×1800×2 = 23MB per post × 16 passes = way too much.
(b) column-sampled RGB: worker builds a full-resolution RGB Uint8Array (w×h×3 = 34MB for medium) once per pass and transfers it — also heavy.
(c) downsample: worker renders preview at fixed max width, e.g. 420 px wide, height proportional (for 6400 wide → 420×118 ≈ 50k px ×3 bytes = 150KB per pass). But GenWorldPreview renders 1px/tile with mapColor24 which uses type/liquid etc. Downsampled preview loses fidelity but it's a progress preview.
(d) Recommended: worker computes a per-column "map color index" or direct RGB at 1px/tile only for a strided sample.

Hmm, but the existing preview canvas is w×h (1px/tile) and sweep-repaints 64 columns/frame reading live store. The simplest faithful approach that preserves visual quality: **transfer a copy of the `type` (and maybe `liquid`/`wall`) arrays as the "preview snapshot" every N passes**, and GenWorldPreview reads from snapshot instead of live world. Cost: type copy 23MB (Uint16Array copy) + liquid 11.5MB per snapshot — with transfer, per snapshot cost = one memcpy 35MB (~30-50ms) in worker + zero-copy transfer to main. If done every 2 passes → 8 snapshots × 35MB transfers. Transfer itself is cheap (handoff), the memcpy is the cost. 50ms memcpy in worker is fine. Main thread then owns 35MB snapshot buffers — fine.

But wait — we could avoid the copy entirely: since worker owns the world during generation, and we need the final world transferred at the end anyway... but preview needs intermediate states. The final pass snapshot IS the final array, so the last preview message can transfer ownership of the actual type/liquid arrays (no copy) — but then the final packet transfer can't include them. Actually we could make the last preview message carry the real arrays via transfer and then the result message doesn't re-send them (worker marks them as already-transferred, main thread stitches: preview buffers become the world's arrays!). That's elegant: zero extra copy for the last snapshot. But it complicates the protocol and the worker still needs arrays for settle after generate... settle changes liquid! So the liquid array transferred at preview would be stale after settle. Type array isn't touched by settle (except killTile via breakTile — settle mode doesn't set killTile, confirmed) — but LiquidSim.quickWater can kill tiles? `sim.killTile` null in settle. But does LiquidSim itself mutate type without killTile? Let me not over-claim; I'll note it must be verified. Given complexity, I'll recommend the pragmatic option:

**Recommended preview protocol**: worker posts `{type: 'preview', passIndex, passName, preview: {width, height, rgb: Uint8ClampedArray}}` where worker renders a **capped-resolution RGB bitmap** (maxW ≈ 640, i.e. downsample factor = ceil(w/640), taking the topmost non-air tile per column-block via mapColor24 logic) — size ≤ 640×(h/factor)... hmm height also needs downsample for big worlds (8400×2400 → 640 wide → factor 14 → 171 tall). ~110k px ×4 = 440KB per snapshot. Tiny. 16 snapshots = 7MB total. Main thread GenWorldPreview just drawImage's the bitmap (no more column sweep). Simple, cheap, and arguably looks fine (it's a small preview widget 520px wide anyway!). Key insight: **the on-screen preview widget is at most 520 CSS px wide** — rendering at 640px internal width exceeds display resolution, so quality loss is invisible. Strong justification.

Even simpler: reuse mapColor24 in worker? MapColors import — check it's pure (reads st arrays). mapColor24(st,x,y) from render/MapColors — likely pure. In worker we can import it. Downsample by sampling: for each output pixel (ox, oy), sample the tile at (ox*f, oy*f) and use mapColor24. That's a strided sample — fine for preview. Or column-top approach (like Terraria's map: first non-air from top) which looks better for terrain silhouette. Recommend strided sampling of mapColor24 for fidelity + it matches existing look closely enough; or take max-density sample per block. I'll recommend: for each output column, find topmost non-air tile (gives clean terrain silhouette + liquids below via sampling), per output row-block take the representative tile. Keep it simple: strided mapColor24 sampling.

Progress: also pass progress {label, p}.

Also preview must be optional (cfg.preview:true) so non-UI flows skip cost.

**Protocol draft**:

```ts
// src/workers/protocol.ts
export type WorldGenRequest =
  | { id: number; type: 'generate'; cfg: GenConfigDTO; settle: 'gen'; preview: boolean }
  | { id: number; type: 'saveParse'; key?: string; json?: string; save?: SaveData; settle: 'load' }
  | { id: number; type: 'settle'; packet: WorldPacket; mode: 'gen'|'load' };

export type WorldGenEvent =
  | { id: number; type: 'progress'; phase: 'generate'|'settle'|'parse'; label?: string; p: number }
  | { id: number; type: 'preview'; passIndex: number; passName: string; width: number; height: number; rgba: ArrayBuffer }
  | { id: number; type: 'result'; world: WorldPacket; player?: SaveData['player'] }
  | { id: number; type: 'error'; message: string; stack?: string };
```

WorldPacket:
```ts
export interface WorldPacket {
  w: number; h: number; seed: number; name: string;
  spawnX: number; spawnY: number;
  groundLevel: number; rockLevel: number; lavaLine: number;
  crimson: boolean; dungeonX: number; dungeonY: number; jungleX: number;
  exploredVersion: number;
  clock: { timeOfDay: number; dayCount: number };
  chests: ChestData[]; signs: ...; trees: ...; flags: Record<string,boolean>;
  treeX: number[]; treeStyle: number[]; treeTops: number[];
  buf: {
    type, flags, frameX, frameY, wall, liquid, liquidType, half, slope, wire, explored: ArrayBuffer
  };
}
```

**WorldGenClient**:
```ts
class WorldGenClient {
  static isAvailable(): boolean  // typeof Worker !== 'undefined'
  async generate(cfg, opts: { onProgress, onPreview }): Promise<World>  // throws WorkerUnavailableError
  async loadSave(args: {key?: string; json?: string; save?: SaveData}, opts): Promise<{world, player}>
  terminate(): void
}
```
- lazy-spawn worker on first request, reuse; feature-detect module worker via try/catch (worker.onerror / construction in Safari old) — fallback: `WorldGenFallback` runs existing main-thread path.
- Error + timeout: watchdog timer (e.g. 120s for large gen configurable), on timeout terminate worker (terminating mid-job loses job → reject promise). Keep simple.
- termination: keep worker alive across newWorld→(later saveParse) reuse; terminate on game start? Keep alive is fine (idle worker ~small RSS). Actually worker with no world held is cheap. Reuse.

**Game.ts changes**:
- `newWorld` becomes: try worker path (`worldGenClient.generate`), on fallback run existing code. Note: worker path does generate+settle both; main thread then does preloadSceneAssets + afterWorldLoad. Progress mapping changes: worker reports phase; map to 0–0.87 range.
- `loadWorld(world, onProgress)`: for the worker path, loadWorld receives the world already settled from worker — but signature takes a World. Restructure: `loadWorldFromWorker` internal: skip settle. Cleaner: split `settleLiquids` out of loadWorld: `loadWorld(world, onProgress, opts?: { settled?: boolean })`. Fallback path does settle on main thread.
- onWorldPartial: no longer available via World object in worker path — Game.newWorld opts.onWorldPartial replaced by opts.onPreview (bitmap) → mainFlow passes loadState.attachPreview(rgba,w,h).

**settleLiquids extraction**: move the loop body from Game.settleLiquids into `src/world/liquid/settle.ts`:
```ts
export async function settleWorldLiquids(world: World, mode: 'gen'|'load', onProgress?: (p:number)=>void): Promise<void>
```
Game.settleLiquids delegates (keeps private method as thin wrapper for fallback).

**mainFlow changes**:
- createWorldFlow: onWorldPartial → onPreview bitmap.
- loadWorldFlow: currently worldStore.load(meta) returns json → loadFromJson(text) does loadSaveData + g.loadWorld. Worker path: `client.loadSave({key}, ...)` → {world, player} → g.loadWorld(world, ..., {settled:true}) + apply player fields. Need worldStore to expose the kv key (probably meta has id/key — load(meta) internally kvGet). Add `worldStore.keyOf(meta)` or have load return {text,key}. Note localStorage-resident small saves: main thread should check and pass json if from localStorage. Simplest: keep worldStore.load returning text, and mainFlow passes {json: text} when small... but then we clone the string anyway. Given audit concern, recommend: worldStore gains `loadRef(meta): {key} | {json}` — or simpler: `kvSource(meta)` returning whether IDB holds it. Hmm, KvStore.kvGet checks localStorage first then IDB. To keep it simple and correct: **Phase 2 recommends worker-side IDB read by key; mainFlow first tries localStorage synchronously (kvGetLocal?), else passes key.** I'll spec: add to KvStore `kvGetLocal(key): string|null` and `kvGetIdb(key)` (the latter safe in worker). worldStore.load delegates to kvGet today — add `worldStore.loadRef(meta): Promise<{key:string} | {json:string}>`.

Wait — is localStorage even reachable in worker? No. So guard needed. And IDB is available in workers (dedicated workers: yes, IndexedDB works in dedicated workers in modern browsers; Safari supports IDB in workers since ~10? Actually dedicated workers have IDB support broadly; module workers Safari 15+; IDB-in-worker Safari yes).

**saveGame timing analysis (transfer ownership question)**: In loadWorld worker path, the World only exists on main thread AFTER worker returns it (constructed from packet). So there's no "main thread's original world becomes dead" problem for the load path — the packet is created in the worker from freshly parsed data and transferred once. The transfer-back direction (main→worker for a `settle` request on an existing world) only arises if we ever want to re-settle an in-memory world — e.g., future "settle more" or phase 3 serialization. For those: analyze ownership: transferring the live world's buffers to worker detaches them on main thread; saveGame (which RLE-serializes from store) must not run during that window. Rule: only transfer a world the main thread can fully discard or has snapshotted. For phase 1/2 we never need main→worker transfer of a live world (generate and saveParse both construct the world inside the worker). State this clearly — it sidesteps the ownership hazard entirely. Optional `settle` request type supports packet created by copying (pack with copy flag) for future use.

**explored array**: new world starts all-zero; save has explored data? SaveData doesn't seem to persist explored (not in saveGame snapshot shown — no explored field). So packet explored: for generate it's zeros (worker can create); for saveParse also zeros. But WorldPacket should still include explored buffer for completeness (cheap to keep) — or omit and let restore allocate zeros. Recommend include for forward-compat (phase 3 might persist it), but note: allocating zeros twice (worker + main) wastes 11.5MB transiently; simpler to omit in phase 1–2 and have restore allocate. Decide: omit explored from transfer in phase 1/2; restore allocates. Hmm — but if worker settle doesn't touch explored, fine. Keep protocol field optional.

**Memory peak analysis**:
- Worker path generate: worker allocates 173MB (medium world) + main thread receives 173MB at end → peak ~350MB transient (two copies during handoff) vs current main-thread-only 173MB. Wait — currently main thread holds world 173MB plus during saveGame RLE etc. The double-hold during handoff is unavoidable with transfer? With transfer, at the moment of postMessage the worker's buffers move — main thread allocates its copies inside World.fromPacket via `new` (main thread copy creation happens while worker still holds? No — worker has already detached after postMessage; the deserialization on main thread allocates the ArrayBuffers from the transferred memory... Actually structured clone with transfer: the receiving side gets the same ArrayBuffer objects re-created; the underlying memory is the same allocation (no copy, ownership handoff). So no double allocation for transferred buffers! Main thread just wraps them. Peak = 173MB (worker) → handoff → 173MB (main). Not 350MB. The copy only happens for cloned (non-transferred) data: scalars/chests (small). Good — must state this correctly: transfer means no copy, so memory peak stays single-copy. But during worker lifetime, main thread shows the preview bitmap (tiny) — great.
- Caveat: garbage collection timing — worker keeps references until it clears them; after postMessage the detached buffers are neutered (zero length), so no double hold. 
- saveParse: worker parses JSON (SaveData object graph ~ several hundred MB transient for 50MB json? JSON.parse of 50MB with many small objects — big but transient in worker, GC'd) then RLE-decodes into store, then JSON discarded. Peak inside worker: SaveData graph + store. Main thread never sees the JSON → big win vs today.

**Vite worker pitfalls**:
- Vite 5: `new Worker(new URL('./worldGen.worker.ts', import.meta.url), { type:'module' })` works in dev and build. Build output: worker.format defaults to 'iife' which **breaks when worker code is split into chunks or uses code-splitting imports** — our worker imports a huge graph (WorldGen pulls ~40 modules, no dynamic imports hopefully — need to check no dynamic import() in the graph; if there are any, iife fails at build with "UMD and IIFE output formats are not supported for code-splitting builds"). Mitigation: set `worker.format: 'es'` in vite.config (needs browsers supporting module workers — Safari 15+). Since we have a runtime fallback, 'es' is fine; note the tradeoff.
- Circular imports: data/tiles imports — check for cycles that break in ESM worker at module-init order. The main bundle already handles them (same ESM semantics), so dev parity is good.
- `import.meta.url` base: with `new URL(..., import.meta.url)` Vite handles both dev and build (relative to chunk). Fine.
- vitest: worker module imports — tests that import Game would import WorldGenClient which references Worker — guard.
- tsconfig: `webworker` lib? Worker file uses self.postMessage — add `"webworker"` lib to a separate tsconfig or use `self as unknown as DedicatedWorkerGlobalScope` with DOM lib. Simplest: declare `const ctx = self as unknown as { postMessage(msg, transfer?): void; onmessage: ... }` to avoid lib conflicts (project tsconfig likely has "DOM"). Note it.

**Safari module worker**: Safari <15 no module workers. Feature-detect: try constructing `{type:'module'}` worker and catch? Construction rarely throws synchronously for unsupported type... Reliable detection: `'HTMLMod..."` hmm. Known approach: check `navigator.userAgent` or attempt and listen for error/timeout. Pragmatic: try worker with a `ping` handshake — if no 'ready' within e.g. 3s, terminate and fall back. That's robust across all failure modes (old Safari, CSP blocking worker, file:// where workers fail). Recommend handshake-based availability: WorldGenClient.spawn() → postMessage({type:'ping'}) → await ready/timeout(3s) → fallback. Good, covers CSP/file:// too.

**Determinism**: RNG mulberry32 + hashString pure; createNoise2D(() => rng.next()) deterministic given same seed. Worker runs identical code (same bundle) → deterministic. Risks: any pass using Math.random() directly (audit grep), Date.now() (generateWorld uses Date.now() only when seedText empty — mainFlow always passes seed `cfg.seed || String(Date.now())` so worker receives explicit seed text — must ensure mainFlow computes the fallback seed BEFORE calling, which it does at call site. Good — but Game.newWorld(seedText...) receives the resolved string; ensure client passes the same string). Also `performance.now()` yields don't affect results. Add grep for Math.random in world/gen as a checklist item.

Also note `ctxGs` module singleton in worker: serial per worker, fine. But if the same worker later handles another generate, ctxGs stale state could leak across jobs! Check: ctxGs is module-level and presumably reset per generate (newGenState). Need to verify it's re-initialized at generate start. Flag as a must-verify item (worker reuse across two generates = same as two main-thread generates sequentially, which already happens in gen-determinism probe — so it's fine).

**Probes**: existing `_settleprobe`, `_liquidprobe`, `_waterfallprobe`, `_spawnposprobe` rely on `window.__swGame` presumably and main-thread generate. If generate moves to worker, probes that import WorldGen directly (like gen-determinism.mjs importing /src/world/gen/WorldGen.ts) still work — main-thread path must remain (fallback path preserved!). Important design point: **keep the main-thread path fully functional as fallback**, which also keeps probes working. Add new probe `_workerprobe.mjs`: same seed via worker client vs main-thread generateWorld → compare hashes/typed arrays. Also a probe to run worker twice (reuse determinism).

Let me quickly check one probe to confirm __swGame usage. And check whether ctxGs is reset. Two quick greps.
````

</details>


---

## 🤖 Assistant · 2026-08-10T06:29:56.994Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"ctxGs\" ~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts | head; grep -rn \"Math.random\\|Date.now\" ~/Project/GLM/SandboxWorld/game/src/world/gen | grep -v \"\\.d\\.ts\" | head",
 "description": "Check ctxGs lifecycle and nondeterminism sources"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:29:57.029Z

**📎 ToolResult**

```
177:  ctxGs[0] = gs;
186:  const gs = ctxGs[0];
194:  const gs = ctxGs[0];
200:  const gs = ctxGs[0];
209:  const gs = ctxGs[0];
223:  const gs = ctxGs[0];
268:  const gs = ctxGs[0];
275:  const gs = ctxGs[0];
282:  const gs = ctxGs[0];
289:  const gs = ctxGs[0];
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGe:32:  const seed = hashString(cfg.seedText || String(Date.now()));
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:36:  const seed = hashString(cfg.seedText || String(Date.now()));

```


---

## 🤖 Assistant · 2026-08-10T06:29:57.552Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -30 ~/Project/GLM/SandboxWorld/game/scripts/_settleprobe.mjs; grep -n \"__swGame\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head -3",
 "description": "Check probe pattern and __swGame"
}
```


---

## 👤 User(sidechain) · 2026-08-10T06:29:57.586Z

**📎 ToolResult**

```
// 读档沉降诊断：模拟"存档里已沉降的水"再跑一遍 settle（等价 loadWorld 路径），
// 统计 QuickWater/WaterCheck 后的 numLiquid、每轮收敛迭代数与耗时
import puppeteer from 'puppeteer-core';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', defaultViewport: { width: 1280, height: 800 }, protocolTimeout: 600000 });
const page = await browser.newPage();
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
await page.goto('http://localhost:5199', { waitUntil: 'domcontentloaded', timeout: 60000 });
await new Promise((r) => setTimeout(r, 2500));
await page.waitForSelector('select', { timeout: 120000 });
await page.evaluate(() => { const _s = document.querySelector('select'); _s.selectedIndex = 0; _s.parentElement.querySelector('button').click(); });
await page.waitForFunction(() => window.__swGame && window.__swGame.world && window.__swGame.player && window.__swGame.liquid, { timeout: 300000 });
await new Promise((r) => setTimeout(r, 1500));

const out = await page.evaluate(async () => {
  const g = window.__swGame;
  // 手搓与 settleLiquids 同构的循环（可观测内部状态）
  const LiquidSim = g.liquid.constructor;
  const sim = new LiquidSim(g.world);
  const t0 = performance.now();
  const tQuick0 = performance.now();
  sim.quickWater();
  const tQuick = performance.now() - tQuick0;
  sim.waterCheck();
  const afterCheck = sim.numLiquid;
  sim.quickSettle = true;
  const rounds = [];
  let totalIter = 0;

```


---

## 🤖 Assistant · 2026-08-10T06:30:01.326Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
ctxGs is set at line 177 (`ctxGs[0] = gs`) — presumably inside a runVanillaTerrain entry where gs = newGenState(...). So it's re-initialized per generate. Good. No Math.random in gen (only Date.now() fallback when seedText empty — call sites always pass seed).

I have everything I need. Now write the comprehensive plan as my final message.

Let me structure:

1. 总体架构（图/文字）
2. 文件清单（新增/修改）
3. 消息协议类型定义草案（protocol.ts）
4. WorldPacket + restore 签名
5. 关键函数签名（WorldGenClient、settleWorldLiquids、worker 主循环）
6. 改动点列表（Game.newWorld / loadWorld、mainFlow、GenWorldPreview、KvStore、worldStore）
7. 预览方案推荐与理由
8. 风险表
9. 分阶段实施
10. 验证清单
11. Critical Files

Keep it detailed but organized. Use absolute paths.
```

</details>


---

## 🤖 Assistant · 2026-08-10T06:31:31.116Z · glm-x-preview-260804

````
调研结论与代码抽查一致（`generateWorld` 签名、`settleLiquids` 双模式、`loadSaveData` 五段 RLE、TileStore 10 数组 + 双 listeners 数组、`gen-determinism.mjs` 已有同 seed 双跑探针可复用）。补充两个抽查发现，直接写入方案：

- `ctxGs` 在 `WorldGen.ts:177` 每个 generate 开头重新赋值（`ctxGs[0] = gs`），跨任务无残留状态 → worker 复用安全。
- `src/world/gen` 下唯一非确定性来源是 `seedText` 为空时的 `Date.now()` 兜底（`WorldGen.ts:36`）；`mainFlow.ts:275` 在调用前已解析 `cfg.seed || String(Date.now())`，只要把**解析后的字符串**传给 worker 即封闭。`Math.random()` 在 gen 目录 grep 为零。

以下是完整实施方案。

---

# 世界生成 / 存档加载移入 Web Worker 实施方案

## 0. 核心设计决策（先给结论）

| 决策点 | 结论 | 一句话理由 |
|---|---|---|
| 生成 + 沉降合并为一条 worker 消息链 | ✅ generate 请求内 worker 顺序跑 `generateWorld` + `settleLiquids('gen')`，一次性 transfer 回 | settle 是纯内存操作，切回主线程再传回 worker 是两次 173MB 搬运，纯浪费 |
| saveParse 的存档字符串来源 | **worker 内直接 kvGet（IndexedDB）**，主线程只在 localStorage 命中小档时传字符串 | JSON 字符串在 V8 内存是 UTF-16，50MB 文件 ≈ 100MB；structured clone 会再做一份 → 瞬时 200MB，而 IDB 本身异步不阻塞主线程，读取放 worker 零成本 |
| 实时预览数据形态 | **worker 侧降采样 RGB 位图**（上限 ~640px 宽），transfer RGBA buffer | 预览控件显示宽度上限 520 CSS px（GenWorldPreview.ts:31），1px/tile 的 8400px 内部位图远超显示分辨率；全量 type 数组每 pass 23MB 拷贝不可接受 |
| 主→worker 的 world 转移 | **阶段 1/2 完全不需要** | generate 与 saveParse 都在 worker 内"从零构造 World"，天然单向；现有 in-memory world 的 settle 需求不存在，ownership 问题被架构绕开 |
| 回退路径 | 保留现有主线程代码路径为 fallback | 老 Safari 无 module worker、CSP 禁 worker、`file://` 下 worker 全挂；且现有探针（gen-determinism.mjs 直接 import WorldGen）依赖主线程路径存活 |
| 可用性判定 | ping/ready 握手 + 3s 超时 | 比 `typeof Worker` 或 UA 嗅探可靠，覆盖所有失败模式（构造成功但加载失败也能兜住） |

---

## 1. 目标架构

```
主线程                                    Worker (worldGen.worker.ts)
──────                                    ──────────────────────────
mainFlow.createWorldFlow                  
  └─ Game.newWorld()
       └─ WorldGenClient.generate(cfg, {onProgress, onPreview})
            │  postMessage({type:'generate', cfg, preview:true})
            │                            ├─ generateWorld(cfg, onProgress→postMessage)
            │  ◄─ {type:'progress'} ×N   │   └─ 每 pass: 渲染降采样位图 → postMessage(transfer)
            │  ◄─ {type:'preview'} ×N    ├─ settleWorldLiquids(world,'gen', onProgress→postMessage)
            │  ◄─ {type:'progress'}      └─ packWorld(world) → postMessage({type:'result'}, transfer)
            │  ◄─ {type:'result', world: WorldPacket}
            ├─ World.fromPacket(packet)   ← transfer 零拷贝，buffer 所有权移交
            └─ preloadSceneAssets + afterWorldLoad + onWorldReady   （原样留在主线程）

mainFlow.loadWorldFlow
  └─ WorldGenClient.loadSave({key}, {onProgress})
            │                            ├─ kvGetIdb(key)  （worker 内读 IDB，零字符串拷贝）
            │                            ├─ loadSaveData(JSON.parse(...))  + 5 段 RLE
            │                            ├─ settleWorldLiquids(world,'load', ...)
            │                            └─ postMessage({type:'result', world, player}, transfer)
            └─ World.fromPacket + player 字段回填 + Game.loadWorld(world, {settled:true})
```

关键性质：**transfer 的 ArrayBuffer 是所有权移交而非拷贝**——postMessage 后 worker 侧 buffer 被 detach（length=0，立即可 GC），主线程 `World.fromPacket` 直接以这些 buffer 构造 TypedArray 包装。所以稳态内存峰值仍是单份 ~173MB（中世界），不存在"worker + 主线程双份长期并存"。双份只出现在两类地方：worker 内部生成期的中间产物（surface Float32Array、noise 状态、LiquidSim 双缓冲），和 saveParse 时 worker 内的 JSON 对象图（几十至几百 MB，但全程在 worker 堆里，解析完即可 GC，主线程全程不可见——这正是相对现状的最大收益）。

---

## 2. 文件清单

### 新增

| 文件 | 职责 |
|---|---|
| `~/Project/GLM/SandboxWorld/game/src/workers/protocol.ts` | 消息协议类型 + `WorldPacket` + `GenConfigDTO`（剥离 onWorldPartial 回调的纯数据版 GenConfig） |
| `~/Project/GLM/SandboxWorld/game/src/workers/worldPacket.ts` | `packWorld(world)` / `World.fromPacket()` / `TileStore.fromBuffers()` 双向打包-重建（主线程与 worker 共用，纯函数） |
| `~/Project/GLM/SandboxWorld/game/src/workers/worldGen.worker.ts` | worker 入口：onmessage 分发 generate/saveParse，进度与预览 postMessage |
| `~/Project/GLM/SandboxWorld/game/src/workers/WorldGenClient.ts` | 主线程封装：worker 懒加载、ping 握手可用性检测、Promise 化、进度/预览回调、复用/terminate、超时看门狗 |
| `~/Project/GLM/SandboxWorld/game/src/workers/previewBitmap.ts` | 降采样预览渲染（worker 侧 `renderPreviewBitmap(store, maxW)` → RGBA + transfer） |
| `~/Project/GLM/SandboxWorld/game/src/world/liquid/settle.ts` | 从 `Game.settleLiquids` 抽出的纯函数 `settleWorldLiquids(world, mode, onProgress)`（主线程 fallback 与 worker 共用同一实现） |
| `~/Project/GLM/SandboxWorld/game/scripts/_workerprobe.mjs` | worker/主线程双路径同 seed 一致性探针 |

### 修改

| 文件 | 改动 |
|---|---|
| `~/Project/GLM/SandboxWorld/game/src/core/Game.ts` | `newWorld` / `loadWorld` 改为先走 worker、失败/不可用走原主线程路径；`settleLiquids` 变为对 `settleWorldLiquids` 的薄封装 |
| `~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts` | 构造器加可选 `buffers` 参数（restore 路径跳过分配，保住 `readonly` 字段声明） |
| `~/Project/GLM/SandboxWorld/game/src/world/World.ts` | 加 `static fromPacket(p: WorldPacket): World` |
| `~/Project/GLM/SandboxWorld/game/src/mainFlow.ts` | `createWorldFlow` 的 `onWorldPartial` → `onPreview`（位图）；`loadWorldFlow` 改走 client.loadSave；`importWld` 阶段 2 接入 |
| `~/Project/GLM/SandboxWorld/game/src/vui/states/UIWorldLoadState.ts` + `GenWorldPreview.ts` | `attachWorld(world)` 旁加 `attachPreview(rgba, w, h)`；GenWorldPreview 增加位图模式（直接 drawImage，替代列扫描） |
| `~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts` | 拆出 `kvGetIdb(key)`（不触 localStorage，worker 安全）；`kvGetLocal(key)`（同步、仅主线程） |
| `~/Project/GLM/SandboxWorld/game/src/save/worldStore.ts`（实际文件名以 `worldStore.load` 定义处为准） | 增加 `loadRef(meta): Promise<{key} \| {json}>`——区分 IDB 直读（传 key 给 worker）与 localStorage 小档（传 json） |
| `~/Project/GLM/SandboxWorld/game/vite.config.ts` | `worker: { format: 'es' }`（见风险 R3） |

---

## 3. 消息协议类型草案（`src/workers/protocol.ts`）

```ts
import type { ChestData } from '../world/World';
import type { SaveData } from '../save/SaveFile';

/** GenConfig 的纯数据投影：剥掉 onWorldPartial（worker 里改为 preview 消息） */
export interface GenConfigDTO {
  width: number; height: number; seedText: string;
  name?: string; structures?: boolean; evil?: -1 | 0 | 1;
  lgcTerrain?: boolean;               // 经典地形回退开关（探针用）
  preview?: boolean;                   // 是否需要降采样预览消息
}

/** 11 个全图数组，值均为 ArrayBuffer（transfer 目标） */
export interface TileBuffers {
  type: ArrayBuffer; flags: ArrayBuffer; frameX: ArrayBuffer; frameY: ArrayBuffer;
  wall: ArrayBuffer; liquid: ArrayBuffer; liquidType: ArrayBuffer;
  half: ArrayBuffer; slope: ArrayBuffer; wire: ArrayBuffer;
  explored?: ArrayBuffer;               // 阶段 1/2 可省略（全零，restore 时分配）
}

export interface WorldPacket {
  w: number; h: number; seed: number; name: string;
  spawnX: number; spawnY: number;
  groundLevel: number; rockLevel: number; lavaLine: number;
  crimson: boolean; dungeonX: number; dungeonY: number; jungleX: number;
  exploredVersion: number;
  clock: { timeOfDay: number; dayCount: number };
  chests: ChestData[];
  signs: Array<{ x: number; y: number; text: string }>;
  trees: Array<{ x: number; y: number; h: number }>;
  flags: Record<string, boolean>;
  treeX: number[]; treeStyle: number[]; treeTops: number[];
  buf: TileBuffers;
}

export type WorldWorkerRequest =
  | { id: number; type: 'generate'; cfg: GenConfigDTO }
  | { id: number; type: 'saveParse'; key?: string; json?: string; save?: SaveData }
  | { id: number; type: 'ping' };

export type WorldWorkerEvent =
  | { id: number; type: 'ready' }                                       // 握手
  | { id: number; type: 'progress'; phase: 'generate'|'settle'|'parse'; label?: string; p: number }
  | { id: number; type: 'preview'; passIndex: number; passName: string;
      width: number; height: number; rgba: ArrayBuffer }                // rgba 为 transfer
  | { id: number; type: 'result'; world: WorldPacket; player?: SaveData['player'] }
  | { id: number; type: 'error'; message: string; stack?: string };
```

要点：
- 每个请求带自增 `id`，事件原样回带 → 单 worker 复用时多任务路由（当前实际串行，但 id 让 client 可以安全地"一请求一 Promise"并检测串线）。
- `settle` 独立请求类型**阶段 1/2 不实现**（见决策表）。协议里不预留半吊子字段，需要时再加 `{type:'settle'; packet: WorldPacket; mode}`。
- `saveParse` 三种载荷：`key`（IDB 直读，主路径）、`json`（localStorage 小档 / 调试）、`save`（.wld 导入的内存 SaveData，structured clone 直传、跳过 stringify→parse）。

---

## 4. 打包 / 重建签名（`src/workers/worldPacket.ts`）

```ts
/** 主线程/worker 通用。copy=false 时转移所有权（调用方此后不可再碰这些数组） */
export function packWorld(world: World, opts?: { copy?: boolean }): {
  packet: WorldPacket;
  transfer: ArrayBuffer[];
}

// TileStore.ts 内新增（保住 readonly 字段声明、跳过零分配）：
export class TileStore {
  constructor(w: number, h: number, bufs?: TileBuffers) {
    ...
    this.type = bufs ? new Uint16Array(bufs.type) : new Uint16Array(n);
    // 其余 9 个同构
  }
}

// World.ts 内新增：
export class World {
  static fromPacket(p: WorldPacket): World {
    const w = new World(p.w, p.h, p.seed, p.name);
    w.store = new TileStore(p.w, p.h, p.buf);     // store 非 readonly，可直接赋值
    w.explored = p.buf.explored ? new Uint8Array(p.buf.explored) : new Uint8Array(p.w * p.h);
    // 回填全部标量 + chests/signs/trees/flags/treeX/treeStyle/treeTops/clock
    return w;
  }
}
```

注意点：
- `packWorld` **不碰** `store.listeners / liquidListeners`（函数数组，clone 必抛 `DataCloneError`）——天然满足，因为只读 TypedArray 的 `.buffer`。
- `structuredClone` 对 `chests/signs/trees/flags` 等纯 JSON 结构可行，走默认 clone（小，几 KB～几十 KB）。
- `explored` 在阶段 1/2 建议省略：saveGame 快照（SaveFile.ts:150-165）未持久化 explored，新生成与读档都是全零，让 `fromPacket` 分配省一次 11.5MB 的 worker→主线程移交与双份瞬存。

---

## 5. 关键函数签名

### `src/world/liquid/settle.ts`（从 Game.ts:405-438 平移）

```ts
/** 全图液体沉降。mode='gen'：外层 10 轮（WorldGen.cs:7395）；mode='load'：单轮 100000 上限（WorldFile.cs:738-770）。
 *  yield ≥32ms 一次——worker 内也保留：让 progress postMessage 能流出。 */
export async function settleWorldLiquids(
  world: World,
  mode: 'gen' | 'load',
  onProgress?: (p: number) => void,
): Promise<void>;
```

worker 内它照常 `new LiquidSim(world)`——LiquidSim 构造器向 store 注册 onTileChanged/onLiquidChanged 闭包、`killTile` 保持 null（settle 模式不设，语义与现状一致）；`dispose()` 只置 flag 的 listener 泄漏问题在 worker 里随 worker 终止/世界丢弃自然消解，顺手在注释里记录"若日后 settle 需在长寿对象上跑，需改 dispose 真正解绑"。

### `src/workers/WorldGenClient.ts`

```ts
export interface PreviewFrame { width: number; height: number; rgba: Uint8ClampedArray;
  passIndex: number; passName: string; }

export class WorldGenUnavailable extends Error { /* 触发主线程 fallback */ }

export class WorldGenClient {
  static async probe(): Promise<boolean>;                 // 单例内缓存：spawn + ping，3s 无 ready → false

  generate(cfg: GenConfigDTO, cb?: {
    onProgress?: (phase: 'generate'|'settle', label: string, p: number) => void;
    onPreview?: (f: PreviewFrame) => void;
    timeoutMs?: number;                                   // 默认 180s（大世界 8400×2400 余量）
  }): Promise<World>;                                     // 内部 World.fromPacket

  loadSave(args: { key?: string; json?: string; save?: SaveData }, cb?: {
    onProgress?: (phase: 'parse'|'settle', p: number) => void;
    timeoutMs?: number;
  }): Promise<{ world: World; player: SaveData['player'] }>;

  terminate(): void;                                      // 页面卸载 / 手动放弃
}
```

实现要点：
- worker 懒加载：`new Worker(new URL('./worldGen.worker.ts', import.meta.url), { type: 'module' })`，**不要**在构造时立即 spawn，避免菜单页空耗。
- 单事件总线：`worker.onmessage` 按 `id` 分发给 pending map；`worker.onerror` / `onmessageerror` → 全部 pending reject + 标记不可用（后续请求直接走 fallback，避免每次重试 3s）。
- 超时看门狗：到时 `terminate()`（杀掉卡死任务）+ reject；下次请求重新 spawn。terminate 必须做，否则一个挂死的 worker 会永久占住后续请求。
- **不做** worker 池：生成是低频重操作，单 worker 串行足够；`ctxGs` 单例也决定了天然串行最安全。

### `src/workers/worldGen.worker.ts` 主循环

```ts
const ctx = self as unknown as {
  postMessage(msg: WorldWorkerEvent, transfer?: Transferable[]): void;
  onmessage: ((e: MessageEvent<WorldWorkerRequest>) => void) | null;
};
ctx.onmessage = async (e) => {
  const req = e.data;
  try {
    if (req.type === 'ping') { ctx.postMessage({ id: req.id, type: 'ready' }); return; }
    if (req.type === 'generate') {
      // generateWorld 的 onWorldPartial 在 worker 内改造成：渲染降采样位图 → transfer
      const world = await generateWorld({ ...req.cfg,
        onWorldPartial: req.cfg.preview ? (w, i, name) => postPreview(req.id, w, i, name) : undefined,
      }, (label, p) => ctx.postMessage({ id: req.id, type: 'progress', phase: 'generate', label, p }));
      await settleWorldLiquids(world, 'gen',
        (p) => ctx.postMessage({ id: req.id, type: 'progress', phase: 'settle', label: '水体沉降', p }));
      const { packet, transfer } = packWorld(world);          // 转移所有权
      ctx.postMessage({ id: req.id, type: 'result', world: packet }, transfer);
      return;
    }
    if (req.type === 'saveParse') { /* kvGetIdb / json / save 三源 → loadSaveData →
                                        settleWorldLiquids(world,'load') → packWorld + player */ }
  } catch (err) {
    ctx.postMessage({ id: req.id, type: 'error', message: (err as Error).message, stack: (err as Error).stack });
  }
};
```

`ctx` 用类型断言而非引入 `webworker` lib——项目 tsconfig 是 DOM 环境，双 lib 会打架（风险 R7）。

---

## 6. 改动点明细

### `Game.newWorld`（Game.ts:311-321）

```ts
async newWorld(seedText, width, height, onProgress?, opts?) {
  if (await WorldGenClient.probe()) {
    try {
      this.world = await this.client.generate(
        { width, height, seedText, name: opts?.name, evil: opts?.evil, preview: !!opts?.onPreview },
        {
          // 进度区间映射保持现有观感：generate 占 0–0.7、settle 占 0.72–0.87
          onProgress: (phase, label, p) => onProgress?.(label,
            phase === 'generate' ? p * 0.7 : 0.72 + p * 0.15),
          onPreview: opts?.onPreview,
        });
      await this.preloadSceneAssets((l, p) => onProgress?.(l, 0.87 + p * 0.13));
      onProgress?.('完成', 1);
      this.afterWorldLoad();
      this.cb.onWorldReady();
      return;
    } catch (e) {
      if (!(e instanceof WorldGenUnavailable)) throw e;   // 真实业务错误（如内存溢出）不吞
      // 落到下方主线程路径
    }
  }
  // ── 现有主线程路径原样保留（fallback + 探针依赖）──
  this.world = await generateWorld(...);
  await this.settleLiquids(...);
  await this.preloadSceneAssets(...);
  this.afterWorldLoad(); this.cb.onWorldReady();
}
```

要点：
- `opts.onWorldPartial` 字段名改为 `opts.onPreview`，类型从 `(world, passIndex, passName) => void` 改为 `(f: PreviewFrame) => void`。
- `preloadSceneAssets` / `afterWorldLoad` 保持在主线程且保持在 worker 结果之后——现有顺序天然兼容（数据就绪 → 扫描出生点 sheet → 建运行期实例）。

### `Game.loadWorld`（Game.ts:440-449）

签名加 `opts?: { settled?: boolean }`：worker 路径世界已在 worker 沉降完，跳过主线程 `settleLiquids`，直接 preload + afterWorldLoad。fallback 路径 `settled=false` 走原逻辑。**所有权分析**：这条链里 worker 返回的 World 是从 packet 在主线程重建的唯一实例，主线程不存在"另一份被 transfer 掏空的 world"——不存在 saveGame 与 transfer 的竞态。唯一要保证的是：`onWorldReady` 之前用户无法触发 `doSave()`（现状已满足：mainFlow 在 `loadWorld` await 完成后才登记槽位/保存）。

### `mainFlow.ts`

- `createWorldFlow`（:271-289）：`onWorldPartial: (world) => loadState.attachWorld(world)` → `onPreview: (f) => loadState.attachPreview(f)`。注意 ：275 的 `cfg.seed || String(Date.now())` 保持原位，worker 收到的已是确定字符串。
- `loadWorldFlow`（:263-268）：`worldStore.load(meta)` 改 `worldStore.loadRef(meta)`：
  - 命中 localStorage → `{json}` 传字符串（小档 ≤2MB，clone 开销可忽略）；
  - 否则 `{key}` 传 key，worker 内 `kvGetIdb`。
  - 后接 `client.loadSave(...)` → `g.loadWorld(world, onProgress, { settled: true })` + player 字段回填（mainFlow.ts:142-150 那段整体平移，建议抽成 `applyPlayer(g, player)` 两处共用）。
- `importWld`（:158-199）：阶段 1 保持主线程不动；阶段 2 改 `client.loadSave({ save }, ...)`——structured clone 直接传 SaveData 对象图，延续审计 #3"跳过 stringify→parse 双拷贝"的成果。
- `loadFromJson`（:135 附近，loadWorldFlow 的另一入口）在阶段 2 一并切换。

### `GenWorldPreview` 预览改造

新增位图模式，保留列扫描模式给 fallback 路径：

```ts
// 位图模式：worker 已渲染好，直接上屏（不再逐列扫 store）
setPreviewFrame(f: PreviewFrame): void;   // putImageData 到 off canvas（尺寸=位图尺寸）
// fallback 模式：现有 sweep() 不动
```

### `previewBitmap.ts`（推荐方案展开）

```ts
/** 降采样预览：maxW 默认 640。每个输出像素取源格 (ox*f, oy*f) 的 mapColor24。
 *  中世界 6400×1800 → 640×180×4 ≈ 460KB/帧；16 pass 共 ~7MB 总流量。 */
export function renderPreviewBitmap(st: TileStore, maxW = 640): {
  width: number; height: number; rgba: Uint8ClampedArray;
}
```

- 复用 `src/render/MapColors.ts` 的 `mapColor24(st, x, y)`（抽查确认它只读 store 数组，worker 可直接 import；若发现它引用 DOM/渲染上下文则回退为"topmost non-air per column + liquid 采样"的简化着色，预览用途足够）。
- **为什么不用 type 数组副本**：Uint16 type + Uint8 liquid 每 pass 34.5MB memcpy，16 pass 550MB 纯拷贝流量，且 GenWorldPreview 列扫描逻辑要整体重写成"读快照"——而预览控件显示宽度上限 520px，1px/tile 的保真度根本不可见。
- **为什么不用"列 mapColor index"再主线程着色**：把着色放主线程等于把 173MB 遍历搬回主线程，违背目标。worker 出 RGBA、主线程只 putImageData，是最干净的分工。

---

## 7. 风险清单

| # | 风险 | 等级 | 缓解 |
|---|---|---|---|
| R1 | **内存峰值**：transfer 是所有权移交，主线程不双份；但 worker 内 saveParse 时"JSON 对象图 + 解码后 store"并存（几百 MB 瞬时） | 中 | 全部发生在 worker 堆，GC 后归还；`loadSaveData` 解码完 5 段后显式丢掉 u8 临时数组（现状已丢）。若要进一步压：worker 内 JSON.parse 后先删大字符串引用 |
| R2 | **Vite 构建期 worker 打包**：`worker.format` 默认 `'iife'`，worker 图内出现动态 import / 代码分割会直接构建报错 | 高 | vite.config 设 `worker: { format: 'es' }`；同时 grep `src/world`、`src/save` 图内不得有 `import()` 动态导入（抽查 WorldGen 的 40 个静态 import 均为静态）。构建后用 `npm run build` + 预览环境跑一次 _workerprobe 兜底 |
| R3 | **module worker 兼容**：Safari <15 不支持 `type:'module'`；CSP 禁 worker；`file://` 协议下 worker 全挂 | 高 | ping/ready 握手 + 3s 超时 → `WorldGenUnavailable` → 主线程 fallback。`onerror` 一旦触发即标记不可用，避免每次请求重付 3s |
| R4 | **确定性回归**：worker 与主线程产出必须逐格一致 | 中 | 依赖 RNG 纯函数（mulberry32 + hashString + `createNoise2D(() => rng.next())`），同 bundle 同输入必然一致。已 grep 确认 gen 目录无 `Math.random`、唯一 `Date.now()` 在 seedText 为空兜底（调用方已传确定字符串）。用 _workerprobe 做 type/liquid 数组逐格相等断言（见 §9） |
| R5 | **跨 worker import 的循环依赖**：WorldGen ↔ data/tiles 的环在 ESM 下靠 hoisting 消化，与主 bundle 同语义 | 低 | dev 态与主线程同一套 ESM 解析，行为天然一致；若构建产物在 Safari 出 TDZE，将环上模块改为延迟访问 |
| R6 | **错误处理与超时**：worker 内未捕获异常若无 id 回传会永久 pending | 中 | worker 入口整体 try/catch，按 req.id 回 `error` 事件；client 侧 `onerror/onmessageerror` 全量 reject pending；看门狗超时 `terminate()` + 重新 spawn |
| R7 | **tsconfig lib 冲突**：worker 里 `self.postMessage` 需要 webworker lib，项目是 DOM lib | 低 | 不改全局 lib，worker 入口用 `self as unknown as {...}` 类型断言（见 §5），零配置改动 |
| R8 | **探针兼容**：`_settleprobe` 等靠 `window.__swGame` 驱动 UI 进世界，generate 进 worker 后 `g.world` 仍是完整 World 实例（fromPacket 重建），探针无感 | 低 | `__swGame` 挂载点与 `g.liquid.constructor` 取法均不受影响。`gen-determinism.mjs` 直接 import WorldGen 主线程跑——**必须保留主线程 fallback 路径**（本方案已保） |
| R9 | **.wld 导入路径**：`parseWldToSave` 的二进制解析仍在主线程（CPU 重） | 低 | 阶段 1 不动；阶段 2 传 `{save}` structured clone（延续审计 #3 免 stringify）。structured clone 大对象在主线程 postMessage 内同步执行，量级几百 ms——预览进度条已就位，可接受 |
| R10 | **LiquidSim listener 泄漏**：`dispose()` 只置 flag，store.listeners 死闭包累积（现状已存在） | 低 | worker 路径下临时 LiquidSim 随世界丢弃，天然消解。留 TODO：日后 settle 需跑在长寿对象上时改 dispose 为真解绑 |
| R11 | **worker 生命周期**：长期驻留 worker 空闲内存 | 低 | 不主动terminate，空闲 worker RSS 极小；`beforeunload` 时 terminate；超时/错误时 terminate 重建 |
| R12 | **transfer 后误用**：`packWorld` 之后 worker 侧 TypedArray 全部 length=0，任何后续读取得静默错误数据 | 中 | `packWorld` 内部约定"调用即终局"，TS 层面把返回值设计成转移语义（函数名 + 注释），并在 worker 主循环里保证 pack 是 generate/saveParse 分支的最后一步 |

---

## 8. 分阶段实施

### 阶段 1：generate + settle 进 worker（最大收益，主线程卡顿消除）
1. `protocol.ts` + `worldPacket.ts`（packWorld / fromPacket / TileStore buffers 构造）+ 单测（小世界 roundtrip 逐字段相等）
2. `settle.ts` 抽取 + `Game.settleLiquids` 改薄封装（行为零变化，跑现有 `_settleprobe` 验证）
3. `worldGen.worker.ts`（先只支持 generate）+ `WorldGenClient`（ping 探测/超时/fallback）
4. `previewBitmap.ts` + `GenWorldPreview.setPreviewFrame` + `UIWorldLoadState.attachPreview`
5. `Game.newWorld` 接线 + `mainFlow.createWorldFlow` 改 `onPreview`
6. `vite.config.ts` worker.format；`_workerprobe.mjs`
7. 回归：gen-determinism / _settleprobe / _spawnposprobe / _waterfallprobe / gen-preview-smoke

### 阶段 2：saveParse 进 worker（读档 JSON.parse + RLE 消除主线程卡顿）
1. KvStore 拆 `kvGetIdb` / `kvGetLocal`；worldStore 加 `loadRef`
2. worker 加 `saveParse` 分支（key/json/save 三源）
3. `Game.loadWorld` 加 `settled` 选项；mainFlow `loadWorldFlow` / `loadFromJson` / `importWld` 接线
4. 回归：roundtrip-test / save-ascii / _liquidprobe（load 模式）/ title-smoke → 读档流

### 阶段 3（可选）：saveGame 序列化进 worker
反向链：主线程 `packWorld(world, {copy:true})`（**必须 copy**，运行期 world 不能掏空——saveGame 之后游戏继续用这份 world）→ worker `rleTiles` + `rlePairs` + `JSON.stringify` → 字符串回传 → 主线程 kvSet。方向与阶段 1/2 相反，先做profiling确认序列化确实是可感知卡顿再上。

---

## 9. 验证清单

**新增 `_workerprobe.mjs`（双路径一致性）**
- 同 seedText（固定 'det'）分别走 `WorldGenClient.generate`（worker）与直接 `import('/src/world/gen/WorldGen.ts').generateWorld`（主线程 fallback），4200×1200
- 断言：`type`/`liquid`/`wall`/`half` 数组**逐格相等**（不是采样 hash——逐格才能暴露单点 RNG 漂移）；标量 spawnX/spawnY/groundLevel/crimson/dungeonX 相等
- 断言：`World.fromPacket(packWorld(w))` roundtrip 后所有数组逐格相等（packet 协议正确性）
- 断言：worker 复用——同一 client 连续两次 generate 同 seed 结果一致（`ctxGs` 无跨任务残留）
- 断言：fallback 生效——用 `page.evaluate` 篡改 `Worker` 构造为抛错，确认主线程路径照常产出且结果与 worker 路径一致
- 断言：预览消息到达次数 ≥ pass 数、RGBA 尺寸 ≤ 640 宽

**现有探针回归**（全部应无改动通过）
- `gen-determinism.mjs`（依赖主线程路径存活——fallback 保留的直接受益者）
- `_settleprobe.mjs` / `_liquidprobe.mjs`（gen 与 load 双模式沉降数值不变）
- `_waterfallprobe.mjs` / `_halfbrickprobe.mjs`（沉降后水体/半砖形态不变）
- `_spawnposprobe.mjs`（出生点不变——确定性回归的终端表现）
- `roundtrip-test.mjs` / `save-ascii.mjs`（阶段 2 存档链）
- `gen-preview-smoke.mjs`（预览 UI 不回归）
- 手测：dev 态 `npm run dev` 生成大世界确认进度条流畅、预览图渐进出现；`npm run build` + 预览态再跑一遍 _workerprobe（覆盖 R2 构建期风险）

---

### Critical Files for Implementation

- ~/Project/GLM/SandboxWorld/game/src/core/Game.ts（newWorld/loadWorld/settleLiquids 改造入口，Game.ts:311/405/440）
- ~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts（generateWorld 主循环与 onWorldPartial 挂点，:35/:83-86）
- ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts（buffers 注入构造 + 与 World.fromPacket 的重建路径）
- ~/Project/GLM/SandboxWorld/game/src/mainFlow.ts（createWorldFlow/loadWorldFlow/importWld 三条调用链接线）
- ~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts（loadSaveData 与 SaveData 类型，阶段 2 saveParse 的 worker 侧复用）
````
