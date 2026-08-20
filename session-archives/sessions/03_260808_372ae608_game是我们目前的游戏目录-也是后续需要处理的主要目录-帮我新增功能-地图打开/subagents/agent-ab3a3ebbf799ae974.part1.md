# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-09T02:57:35.016Z

```
审计两个文件的移植一致性：

1. ~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts vs ~/Project/GLM/SandboxWorld/Terarria1405/WaterfallManager.cs：
   - findWaterfalls 触发条件 vs L100-130（halfBrick、上格 liquid<16||SolidTile、一侧>160 对侧空、类型判定上/右/左三格）
   - draw 的走向循环 vs L421-507（下方空直落、撞地向空侧平移、偏折计数 ≥2 停）与 L531-532（撞地 yOff=8——注意原版条件是 SolidTile(below)&&!tile.halfBrick，我们用的是 isSolid）
   - 透明度 vs L538-551（岩浆1.0/蜂蜜0.8/水 0.6 地下或 Alpha、末 10 格衰减）、帧动画 vs L171-209（regular 3 tick、slow 7 tick）
   - 断流条件 vs L427（blockType==0 才断，半砖豁免）与 L777-778（liquid>0 && !halfBrick → 停）

2. ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts vs ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs：
   - runSmoothWorldPass vs "Smooth World" pass L7568-7696：逐个凸起模式的条件核对（L7580-7668 主模式 A/B/孤立凸起、L7634-7668 悬空支脚削除的 5 个分支、L7669-7695 空位补角两个分支、L7677-7694 第二遍斜坡）
   - runWaterfallLipPass vs "Waterfalls" pass L7697-7743：第一遍条件（SolidTile/左右空/侧旁有液/上下 8-20 格无半砖防串）、第二遍扩展条件（左半砖+左2液 → 砸、右对称）
   - 已知偏离（报告时确认影响即可，不用修）：SlopeTile 随机分支统一改 PoundTile、slope 3/4 未生成、CanPoundTile 类型黑名单简化

输出：每处偏差一行，格式 `偏差 | 文件:位置 | 原版行号 | 影响程度（高/中/低）`。只报差异，≤50 行。
```

---

## 📎 Attachment · skill_listing · 2026-08-09T02:57:35.020Z

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

## 🤖 Assistant · 2026-08-09T02:57:37.888Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I need to audit two files for porting consistency. Let me read all the relevant files in parallel:

1. `~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts` vs `WaterfallManager.cs` (specific line ranges)
2. `~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts` vs `WorldGen.cs` L7568-7743

Let me start by reading the TS files fully and the C# files at the specified ranges.
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:57:37.889Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T02:57:37.891Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T02:57:37.893Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WaterfallManager.cs",
 "limit": 480,
 "offset": 90
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:37.899Z

**📎 ToolResult**

```
1	// 原版 1.4.0.5 WaterfallManager.cs 移植：液体从边缘倾泻时的长条瀑布贴图。
2	// 与 LiquidRenderer 的 P3 瀑布拖尾（10 格内液体本体渐隐）互补——这里画的是
3	// 独立的 Waterfall_N 贴图柱（最长 100 格），原版在半砖唇缘触发。
4	// 本仓库无半砖/坡面系统，触发条件按原版语义适配为"倾泻点"：
5	//   液量 ≥160 的格子、正下方为空且可通行（液体正在从边缘落下），每列连续段只取最高一格。
6	// 其它规则照抄原版：
7	//  - 贴图 Waterfall_N.png：512×56 胶片条，帧宽 32、16 帧；流柱格取 (frameX,0,16,16-liquid/16)
8	//  - 帧速：水 regularFrame 每 3 tick、岩浆/蜂蜜 slowFrame 每 7 tick（WaterfallManager.cs:171-209）
9	//  - 透明度：岩浆 1.0 / 蜂蜜 0.8 / 水地表 1.0、地下或有墙 0.6；末 10 格线性衰减（行 538-551）
10	//  - 走向：下方空→直落；撞地→向空侧平移一格再落（偏折 ≥2 次停）；流入液池停（行 421-507/777）
11	//  - 撞地格绘制上移 8px 贴住地面（num11，行 531-532）
12	// 省略（周边系统缺失）：雨/雪云柱、彩虹/荧光砖改写、溅落 2px 斜切片、环境音、Grate 穿透。
13	import type { SpriteAtlas } from '../assets/SpriteAtlas';
14	import type { TileStore } from '../world/TileStore';
15	import { TILE_DEFS } from '../data/tiles';
16	
17	interface Waterfall { x: number; y: number; type: number; } // type: 0 水 / 1 岩浆 / 2 蜂蜜（本仓库编码）
18	
19	const MAX_FALLS = 1000;      // 原版 qualityMax = maxWaterfallCount(1000) * gfxQuality(1)
20	const WATERFALL_DIST = 100;  // 原版 waterfallDist = 75*gfxQuality + 25
21	
22	const SHEET = ['vanilla/Waterfall_0.png', 'vanilla/Waterfall_1.png', 'vanilla/Waterfall_14.png'];
23	
24	export class WaterfallRenderer {
25	  private falls: Waterfall[] = [];
26	  private lastFind = -1;
27	  private findFrame = 0;
28	
29	  /** 扫描触发（WaterfallManager.cs FindWaterfalls 90-168，每 30 帧一次）。view 为可见 tile 窗口。
30	   *  原版条件：halfBrick 唇缘格 + 上方近干/实心 + 一侧液量>160 且对侧空 */
31	  findWaterfalls(st: TileStore, tx0: number, ty0: number, tx1: number, ty1: number, frame: number) {
32	    if (frame === this.lastFind) return;
33	    this.lastFind = frame;
34	    this.findFrame++;
35	    if (this.findFrame % 30 !== 1) return; // 与原版同节流：约 0.5s 一扫
36	    this.falls.length = 0;
37	    const x0 = Math.max(2, tx0 - 2), x1 = Math.min(st.w - 3, tx1 + 2);
38	    const y0 = Math.max(2, ty0 - 2), y1 = Math.min(st.h - 3, ty1 + 2);
39	    const solid = (x: number, y: number) => {
40	      if (x < 0 || y < 0 || x >= st.w || y >= st.h) return false;
41	      const t = st.type[st.idx(x, y)];
42	      if (t === 0) return false;
43	      const d = TILE_DEFS[t];
44	      return !!d && d.solid && !d.platform;
45	    };
46	    for (let x = x0; x <= x1; x++) {
47	      for (let y = y0; y <= y1; y++) {
48	        const i = st.idx(x, y);
49	        if (!st.flags[i] || !st.half[i]) continue;          // active && halfBrick（L102）
50	        const ui = i - st.w;
51	        const uq = y > 0 ? st.liquid[ui] : 0;
52	        if (!(uq < 16 || solid(x, y - 1))) continue;          // 上方近干或实心（L110）
53	        const li = i - 1, ri = i + 1;
54	        const lq = st.liquid[li], rq = st.liquid[ri];
55	        const lOpen = lq === 0 && !solid(x - 1, y) && st.slope[li] === 0;
56	        const rOpen = rq === 0 && !solid(x + 1, y) && st.slope[ri] === 0;
57	        if (!((lq > 160 || rq > 160) && (lOpen || rOpen))) continue; // L124
58	        // 类型：上/右/左三格任一岩浆→1 蜂蜜→14，否则水（L126-127）
59	        let type = 0;
60	        const isLava = (ii: number) => st.liquid[ii] > 0 && st.liquidType[ii] === 2;
61	        const isHoney = (ii: number) => st.liquid[ii] > 0 && st.liquidType[ii] === 3;
62	        if (isLava(ui) || isLava(ri) || isLava(li)) type = 1;
63	        else if (isHoney(ui) || isHoney(ri) || isHoney(li)) type = 2;
64	        this.falls.push({ x, y, type });
65	        if (this.falls.length >= MAX_FALLS) return;
66	      }
67	    }
68	  }
69	
70	  /** 绘制（DrawWaterfall 行 211-803 的主体路径；style 固定 0=水） */
71	  draw(ctx: CanvasRenderingContext2D, atlas: SpriteAtlas | null, st: TileStore, groundLevel: number, nowMs: number) {
72	    if (!atlas || this.falls.length === 0) return;
73	    const tex = SHEET.map((s) => atlas.vimages.get(s) ?? null);
74	    if (!tex[0] && !tex[1] && !tex[2]) return;
75	    // 帧动画：水 3 tick/帧、岩浆蜂蜜 7 tick/帧（1 tick ≈ 16.67ms）
76	    const regular = Math.floor(nowMs / 50) % 16;
77	    const slow = Math.floor(nowMs / 117) % 16;
78	    ctx.imageSmoothingEnabled = false;
79	    for (const wf of this.falls) {
80	      const texImg = tex[wf.type] ?? tex[0];
81	      if (!texImg) continue;
82	      const frameX = 32 * (wf.type === 0 ? regular : slow);
83	      let cx = wf.x, cy = wf.y; // 原版从唇缘格本体开始画（半砖 blockType=1 不断流，WaterfallManager.cs:427）
84	      let turns = 0;
85	      for (let step = 0; step < WATERFALL_DIST; step++) {
86	        if (cx < 1 || cy < 1 || cx >= st.w - 1 || cy >= st.h - 1) break;
87	        const ci = st.idx(cx, cy);
88	        // 原版断流条件 blockType==0（全实心）；半砖豁免
89	        const tt = st.type[ci];
90	        if (tt !== 0) {
91	          const d = TILE_DEFS[tt];
92	          if (d && d.solid && !d.platform && !st.half[ci]) break;
93	        }
94	        const liq = st.liquid[ci];
95	        // 透明度（WaterfallManager.cs:538-551）
96	        let alpha = wf.type === 1 ? 1.0 : wf.type === 2 ? 0.8
97	          : (st.wall[ci] !== 0 || cy >= groundLevel ? 0.6 : 1.0);
98	        if (step > WATERFALL_DIST - 10) alpha *= (WATERFALL_DIST - step) / 10;
99	        const crop = Math.floor(liq / 16);           // num21：按格内液量裁掉底部
100	        const sh = 16 - crop;
101	        const yOff = st.isSolid(cx, cy + 1) ? 8 : 0; // 撞地格上移 8px（行 531-532）
102	        if (sh > 0) {
103	          ctx.globalAlpha = Math.max(0, Math.min(1, alpha));
104	          ctx.drawImage(texImg, frameX, 0, 16, sh, cx * 16, cy * 16 + yOff, 16, sh);
105	        }
106	        if (liq > 0) break;                          // 溶入液池（行 777-778）
107	        // 走向决策（行 421-507 简化）：下方空→直落；撞地→向空侧平移
108	        if (!st.isSolid(cx, cy + 1)) { cy++; continue; }
109	        const rightOpen = !st.isSolid(cx + 1, cy) && !st.isSolid(cx + 1, cy + 1);
110	        const leftOpen = !st.isSolid(cx - 1, cy) && !st.isSolid(cx - 1, cy + 1);
111	        if (rightOpen) cx++;
112	        else if (leftOpen) cx--;
113	        else break;
114	        if (++turns >= 2) break;                     // 偏折 ≥2 次停（行 503-507）
115	      }
116	    }
117	    ctx.globalAlpha = 1;
118	  }
119	
120	  get count() { return this.falls.length; }
121	}
122	

```


---

## 👤 User(sidechain) · 2026-08-09T02:57:37.899Z

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
14	/** WorldGen.SolidTile(i, j, false) 等价：active && tileSolid[type] && !tileSolidTop */
15	export function solidTile(st: TileStore, x: number, y: number): boolean {
16	  if (x < 0 || y < 0 || x >= st.w || y >= st.h) return false;
17	  const t = st.type[st.idx(x, y)];
18	  if (t === 0) return false;
19	  const d = TILE_DEFS[t];
20	  return !!d && d.solid && !d.platform;
21	}
22	
23	/** 可砸判定（WorldGen.cs:49122 CanPoundTile 简化）：实心非平台非框架物 */
24	function canPoundTile(st: TileStore, x: number, y: number): boolean {
25	  const t = st.type[st.idx(x, y)];
26	  if (t === 0) return false;
27	  const d = TILE_DEFS[t];
28	  return !!d && d.solid && !d.platform && !d.framed;
29	}
30	
31	/** 砸半砖（WorldGen.cs:49198 PoundTile 的生成期路径）：切换 halfBrick 位 */
32	function poundTile(st: TileStore, x: number, y: number): boolean {
33	  if (!canPoundTile(st, x, y)) return false;
34	  const i = st.idx(x, y);
35	  st.half[i] = st.half[i] ? 0 : 1;
36	  if (st.half[i]) st.slope[i] = 0;
37	  return true;
38	}
39	
40	/** 原版 pass "Smooth World"（WorldGen.cs:7568-7696）：地表凸起 → 半砖/削除 */
41	export function runSmoothWorldPass(st: TileStore, rng: RNG, _gs: GenState): void {
42	  const { w, h } = st;
43	  // —— 第一遍：主凸起模式（L7580-7668）——
44	  for (let i = 20; i < w - 20; i++) {
45	    for (let j = 20; j < h - 20; j++) {
46	      const ti = st.idx(i, j);
47	      const t = st.type[ti];
48	      const d = TILE_DEFS[t];
49	      // 原版跳过 48/137/232/191/151/274（雕像/树木/蜂巢类）≈ framed 物体跳过
50	      if (d && d.framed) continue;
51	      if (st.type[st.idx(i, j - 1)] === 0) {
52	        // 上方无块：对凸起顶端做半砖/削除
53	        if (solidTile(st, i, j)) {
54	          const li = st.idx(i - 1, j), ri = st.idx(i + 1, j);
55	          if (!st.half[li] && !st.half[ri] && st.slope[li] === 0 && st.slope[ri] === 0) {
56	            if (solidTile(st, i, j + 1)) {
57	              // 模式 A（L7600）：左凸 → 右坡/半砖；模式 B：右凸 → 左坡/半砖（原版随机 SlopeTile|PoundTile）
58	              if (!solidTile(st, i - 1, j) && solidTile(st, i - 1, j + 1) && solidTile(st, i + 1, j)
59	                && st.type[st.idx(i - 1, j)] === 0 && st.type[st.idx(i + 1, j - 1)] === 0
60	                && !st.half[st.idx(i - 1, j + 1)]) {
61	                if (rng.chance(0.5)) poundTile(st, i, j); // 原版另一半走 SlopeTile(2)
62	                else poundTile(st, i, j);
63	              } else if (!solidTile(st, i + 1, j) && solidTile(st, i + 1, j + 1) && solidTile(st, i - 1, j)
64	                && st.type[st.idx(i + 1, j)] === 0 && st.type[st.idx(i - 1, j - 1)] === 0
65	                && !st.half[st.idx(i + 1, j + 1)]) {
66	                poundTile(st, i, j); // 原版另一半走 SlopeTile(1)
67	              } else if (solidTile(st, i + 1, j + 1) && solidTile(st, i - 1, j + 1)
68	                && st.type[st.idx(i + 1, j)] === 0 && st.type[st.idx(i - 1, j)] === 0) {
69	                // 孤立凸起（L7629）：直接半砖
70	                poundTile(st, i, j);
71	              }
72	              // 悬空支脚削除（L7634-7668）：两侧下方空 + 对角支撑 → 删
73	              if (solidTile(st, i, j)) {
74	                if (solidTile(st, i - 1, j) && solidTile(st, i + 1, j + 2)
75	                  && st.type[st.idx(i + 1, j)] === 0 && st.type[st.idx(i + 1, j + 1)] === 0
76	                  && st.type[st.idx(i - 1, j - 1)] === 0) {
77	                  st.setTileSilent(i, j, 0);
78	                } else if (solidTile(st, i + 1, j) && solidTile(st, i - 1, j + 2)
79	                  && st.type[st.idx(i - 1, j)] === 0 && st.type[st.idx(i - 1, j + 1)] === 0
80	                  && st.type[st.idx(i + 1, j - 1)] === 0) {
81	                  st.setTileSilent(i, j, 0);
82	                } else if (st.type[st.idx(i - 1, j + 1)] === 0 && st.type[st.idx(i - 1, j)] === 0
83	                  && solidTile(st, i + 1, j) && solidTile(st, i, j + 2)) {
84	                  if (rng.chance(0.2)) st.setTileSilent(i, j, 0);
85	                  else if (rng.chance(0.25)) poundTile(st, i, j);
86	                } else if (st.type[st.idx(i + 1, j + 1)] === 0 && st.type[st.idx(i + 1, j)] === 0
87	                  && solidTile(st, i - 1, j) && solidTile(st, i, j + 2)) {
88	                  if (rng.chance(0.2)) st.setTileSilent(i, j, 0);
89	                  else if (rng.chance(0.25)) poundTile(st, i, j);
90	                }
91	              }
92	            }
93	            // 顶部单格立柱（L7662）：两侧皆空 → 删
94	            if (solidTile(st, i, j) && st.type[st.idx(i - 1, j)] === 0 && st.type[st.idx(i + 1, j)] === 0) {
95	              st.setTileSilent(i, j, 0);
96	            }
97	          }
98	        } else if (st.type[ti] === 0) {
99	          // 空位补角（L7669-7695）：下方实心 + 单侧实心 → 补一块并半砖（原版另一半 SlopeTile）
100	          const belowType = st.type[st.idx(i, j + 1)];
101	          if (belowType !== 0 && !TILE_DEFS[belowType]?.framed) {
102	            if (solidTile(st, i - 1, j + 1) && solidTile(st, i + 1, j)
103	              && st.type[st.idx(i - 1, j)] === 0 && st.type[st.idx(i + 1, j - 1)] === 0) {
104	              st.setTileSilent(i, j, belowType);
105	              poundTile(st, i, j);
106	            } else if (solidTile(st, i + 1, j + 1) && solidTile(st, i - 1, j)
107	              && st.type[st.idx(i + 1, j)] === 0 && st.type[st.idx(i - 1, j - 1)] === 0) {
108	              st.setTileSilent(i, j, belowType);
109	              poundTile(st, i, j);
110	            }
111	          }
112	        }
113	      }
114	    }
115	  }
116	  // —— 第二遍（L7677-7694）：斜坡补坡（原版 SlopeTile 1/2）+ 悬坡回落半砖 ——
117	  for (let i = 20; i < w - 20; i++) {
118	    for (let j = 20; j < h - 20; j++) {
119	      const ti = st.idx(i, j);
120	      const d = TILE_DEFS[st.type[ti]];
121	      if (d && d.framed) continue;
122	      if (rng.chance(0.5) && st.type[st.idx(i, j - 1)] === 0 && solidTile(st, i, j)) {
123	        if (solidTile(st, i, j + 1) && solidTile(st, i + 1, j) && st.type[st.idx(i - 1, j)] === 0) {
124	          poundTile(st, i, j); // 原版 SlopeTile(2)
125	        } else if (solidTile(st, i, j + 1) && solidTile(st, i - 1, j) && st.type[st.idx(i + 1, j)] === 0) {
126	          poundTile(st, i, j); // 原版 SlopeTile(1)
127	        }
128	      }
129	    }
130	  }
131	}
132	
133	/** 原版 pass "Waterfalls"（WorldGen.cs:7697-7743）：水边唇缘砸半砖（瀑布触发的来源） */
134	export function runWaterfallLipPass(st: TileStore, _rng: RNG, _gs: GenState): void {
135	  const { w, h } = st;
136	  // —— 第一遍（L7701-7723）：实心顶格、左右空、侧旁有水 → 砸半砖 ——
137	  for (let i = 20; i < w - 20; i++) {
138	    for (let j = 20; j < h - 20; j++) {
139	      if (!solidTile(st, i, j)) continue;
140	      const li = st.idx(i - 1, j), ri = st.idx(i + 1, j);
141	      if (st.type[li] !== 0 || st.type[ri] !== 0) continue;
142	      if (!solidTile(st, i, j + 1)) continue;
143	      if (st.liquid[li] === 0 && st.liquid[ri] === 0) continue;
144	      // 上方 8-20 格内已有半砖则跳过（原版防连续砸穿）
145	      let flag = true;
146	      const num3 = 8 + Math.floor(_rng.next() * 12), num4 = 8 + Math.floor(_rng.next() * 12);
147	      for (let k = j - num3; k <= j + num4; k++) {
148	        if (k >= 0 && k < h && st.half[st.idx(i, k)]) flag = false;
149	      }
150	      if (flag) poundTile(st, i, j);
151	    }
152	  }
153	  // —— 第二遍（L7725-7741）：唇缘向相邻实心格扩展半砖 ——
154	  for (let i = 20; i < w - 20; i++) {
155	    for (let j = 20; j < h - 20; j++) {
156	      const ti = st.idx(i, j);
157	      if (!solidTile(st, i, j) || !solidTile(st, i, j + 1)) continue;
158	      if (!solidTile(st, i + 1, j) && st.half[st.idx(i - 1, j)] && st.liquid[st.idx(i - 2, j)] > 0) {
159	        poundTile(st, i, j);
160	      }
161	      if (!solidTile(st, i - 1, j) && st.half[st.idx(i + 1, j)] && st.liquid[st.idx(i + 2, j)] > 0) {
162	        poundTile(st, i, j);
163	      }
164	    }
165	  }
166	}
167	

```


---

## 👤 User(sidechain) · 2026-08-09T02:57:37.900Z

**📎 ToolResult**

```
90	      for (int index1 = num5; index1 < num6; ++index1)
91	      {
92	        for (int index2 = num7; index2 < num8; ++index2)
93	        {
94	          Tile tile = Main.tile[index1, index2];
95	          if (tile == null)
96	          {
97	            tile = new Tile();
98	            Main.tile[index1, index2] = tile;
99	          }
100	          if (tile.active())
101	          {
102	            if (tile.halfBrick())
103	            {
104	              Tile testTile1 = Main.tile[index1, index2 - 1];
105	              if (testTile1 == null)
106	              {
107	                testTile1 = new Tile();
108	                Main.tile[index1, index2 - 1] = testTile1;
109	              }
110	              if (testTile1.liquid < (byte) 16 || WorldGen.SolidTile(testTile1))
111	              {
112	                Tile testTile2 = Main.tile[index1 - 1, index2];
113	                if (testTile2 == null)
114	                {
115	                  testTile2 = new Tile();
116	                  Main.tile[index1 - 1, index2] = testTile2;
117	                }
118	                Tile testTile3 = Main.tile[index1 + 1, index2];
119	                if (testTile3 == null)
120	                {
121	                  testTile3 = new Tile();
122	                  Main.tile[index1 + 1, index2] = testTile3;
123	                }
124	                if ((testTile2.liquid > (byte) 160 || testTile3.liquid > (byte) 160) && (testTile2.liquid == (byte) 0 && !WorldGen.SolidTile(testTile2) && testTile2.slope() == (byte) 0 || testTile3.liquid == (byte) 0 && !WorldGen.SolidTile(testTile3) && testTile3.slope() == (byte) 0) && this.currentMax < this.qualityMax)
125	                {
126	                  this.waterfalls[this.currentMax].type = 0;
127	                  this.waterfalls[this.currentMax].type = testTile1.lava() || testTile3.lava() || testTile2.lava() ? 1 : (testTile1.honey() || testTile3.honey() || testTile2.honey() ? 14 : 0);
128	                  this.waterfalls[this.currentMax].x = index1;
129	                  this.waterfalls[this.currentMax].y = index2;
130	                  ++this.currentMax;
131	                }
132	              }
133	            }
134	            if (tile.type == (ushort) 196)
135	            {
136	              Tile testTile = Main.tile[index1, index2 + 1];
137	              if (testTile == null)
138	              {
139	                testTile = new Tile();
140	                Main.tile[index1, index2 + 1] = testTile;
141	              }
142	              if (!WorldGen.SolidTile(testTile) && testTile.slope() == (byte) 0 && this.currentMax < this.qualityMax)
143	              {
144	                this.waterfalls[this.currentMax].type = 11;
145	                this.waterfalls[this.currentMax].x = index1;
146	                this.waterfalls[this.currentMax].y = index2 + 1;
147	                ++this.currentMax;
148	              }
149	            }
150	            if (tile.type == (ushort) 460)
151	            {
152	              Tile testTile = Main.tile[index1, index2 + 1];
153	              if (testTile == null)
154	              {
155	                testTile = new Tile();
156	                Main.tile[index1, index2 + 1] = testTile;
157	              }
158	              if (!WorldGen.SolidTile(testTile) && testTile.slope() == (byte) 0 && this.currentMax < this.qualityMax)
159	              {
160	                this.waterfalls[this.currentMax].type = 22;
161	                this.waterfalls[this.currentMax].x = index1;
162	                this.waterfalls[this.currentMax].y = index2 + 1;
163	                ++this.currentMax;
164	              }
165	            }
166	          }
167	        }
168	      }
169	    }
170	
171	    public void UpdateFrame()
172	    {
173	      ++this.wFallFrCounter;
174	      if (this.wFallFrCounter > 2)
175	      {
176	        this.wFallFrCounter = 0;
177	        ++this.regularFrame;
178	        if (this.regularFrame > 15)
179	          this.regularFrame = 0;
180	      }
181	      ++this.wFallFrCounter2;
182	      if (this.wFallFrCounter2 > 6)
183	      {
184	        this.wFallFrCounter2 = 0;
185	        ++this.slowFrame;
186	        if (this.slowFrame > 15)
187	          this.slowFrame = 0;
188	      }
189	      ++this.rainFrameCounter;
190	      if (this.rainFrameCounter > 0)
191	      {
192	        ++this.rainFrameForeground;
193	        if (this.rainFrameForeground > 7)
194	          this.rainFrameForeground -= 8;
195	        if (this.rainFrameCounter > 2)
196	        {
197	          this.rainFrameCounter = 0;
198	          --this.rainFrameBackground;
199	          if (this.rainFrameBackground < 0)
200	            this.rainFrameBackground = 7;
201	        }
202	      }
203	      if (++this.snowFrameCounter <= 3)
204	        return;
205	      this.snowFrameCounter = 0;
206	      if (++this.snowFrameForeground <= 7)
207	        return;
208	      this.snowFrameForeground = 0;
209	    }
210	
211	    private void DrawWaterfall(SpriteBatch spriteBatch, int Style = 0, float Alpha = 1f)
212	    {
213	      Main.tileSolid[546] = false;
214	      float num1 = 0.0f;
215	      float num2 = 99999f;
216	      float num3 = 99999f;
217	      int num4 = -1;
218	      int num5 = -1;
219	      float num6 = 0.0f;
220	      float num7 = 99999f;
221	      float num8 = 99999f;
222	      int num9 = -1;
223	      int num10 = -1;
224	      for (int index1 = 0; index1 < this.currentMax; ++index1)
225	      {
226	        int num11 = 0;
227	        int index2 = this.waterfalls[index1].type;
228	        int x1 = this.waterfalls[index1].x;
229	        int y = this.waterfalls[index1].y;
230	        int num12 = 0;
231	        int num13 = 0;
232	        int num14 = 0;
233	        int num15 = 0;
234	        int num16 = 0;
235	        int index3 = 0;
236	        int x2;
237	        switch (index2)
238	        {
239	          case 0:
240	            index2 = Style;
241	            goto default;
242	          case 1:
243	          case 14:
244	            if (!Main.drewLava && this.waterfalls[index1].stopAtStep != 0)
245	            {
246	              x2 = 32 * this.slowFrame;
247	              break;
248	            }
249	            continue;
250	          case 2:
251	            if (Main.drewLava)
252	              continue;
253	            goto default;
254	          case 11:
255	          case 22:
256	            if (!Main.drewLava)
257	            {
258	              int num17 = this.waterfallDist / 4;
259	              if (index2 == 22)
260	                num17 = this.waterfallDist / 2;
261	              if (this.waterfalls[index1].stopAtStep > num17)
262	                this.waterfalls[index1].stopAtStep = num17;
263	              if (this.waterfalls[index1].stopAtStep != 0 && (double) (y + num17) >= (double) Main.screenPosition.Y / 16.0 && ((double) x1 >= (double) Main.screenPosition.X / 16.0 - 20.0 && (double) x1 <= ((double) Main.screenPosition.X + (double) Main.screenWidth) / 16.0 + 20.0))
264	              {
265	                int num18;
266	                int num19;
267	                if (x1 % 2 == 0)
268	                {
269	                  num18 = this.rainFrameForeground + 3;
270	                  if (num18 > 7)
271	                    num18 -= 8;
272	                  num19 = this.rainFrameBackground + 2;
273	                  if (num19 > 7)
274	                    num19 -= 8;
275	                  if (index2 == 22)
276	                  {
277	                    num18 = this.snowFrameForeground + 3;
278	                    if (num18 > 7)
279	                      num18 -= 8;
280	                  }
281	                }
282	                else
283	                {
284	                  num18 = this.rainFrameForeground;
285	                  num19 = this.rainFrameBackground;
286	                  if (index2 == 22)
287	                    num18 = this.snowFrameForeground;
288	                }
289	                Rectangle rectangle1 = new Rectangle(num19 * 18, 0, 16, 16);
290	                Rectangle rectangle2 = new Rectangle(num18 * 18, 0, 16, 16);
291	                Vector2 origin = new Vector2(8f, 8f);
292	                Vector2 position = y % 2 != 0 ? new Vector2((float) (x1 * 16 + 8), (float) (y * 16 + 8)) - Main.screenPosition : new Vector2((float) (x1 * 16 + 9), (float) (y * 16 + 8)) - Main.screenPosition;
293	                Tile tile = Main.tile[x1, y - 1];
294	                if (tile.active() && tile.bottomSlope())
295	                  position.Y -= 16f;
296	                bool flag = false;
297	                float rotation = 0.0f;
298	                for (int index4 = 0; index4 < num17; ++index4)
299	                {
300	                  Color color1 = Lighting.GetColor(x1, y);
301	                  float num20 = 0.6f;
302	                  float num21 = 0.3f;
303	                  if (index4 > num17 - 8)
304	                  {
305	                    float num22 = (float) (num17 - index4) / 8f;
306	                    num20 *= num22;
307	                    num21 *= num22;
308	                  }
309	                  Color color2 = color1 * num20;
310	                  Color color3 = color1 * num21;
311	                  if (index2 == 22)
312	                  {
313	                    spriteBatch.Draw(this.waterfallTexture[22].Value, position, new Rectangle?(rectangle2), color2, 0.0f, origin, 1f, SpriteEffects.None, 0.0f);
314	                  }
315	                  else
316	                  {
317	                    spriteBatch.Draw(this.waterfallTexture[12].Value, position, new Rectangle?(rectangle1), color3, rotation, origin, 1f, SpriteEffects.None, 0.0f);
318	                    spriteBatch.Draw(this.waterfallTexture[11].Value, position, new Rectangle?(rectangle2), color2, rotation, origin, 1f, SpriteEffects.None, 0.0f);
319	                  }
320	                  if (!flag)
321	                  {
322	                    ++y;
323	                    Tile testTile = Main.tile[x1, y];
324	                    if (WorldGen.SolidTile(testTile))
325	                      flag = true;
326	                    if (testTile.liquid > (byte) 0)
327	                    {
328	                      int num22 = (int) (16.0 * ((double) testTile.liquid / (double) byte.MaxValue)) & 254;
329	                      if (num22 < 15)
330	                      {
331	                        rectangle2.Height -= num22;
332	                        rectangle1.Height -= num22;
333	                      }
334	                      else
335	                        break;
336	                    }
337	                    if (y % 2 == 0)
338	                      ++position.X;
339	                    else
340	                      --position.X;
341	                    position.Y += 16f;
342	                  }
343	                  else
344	                    break;
345	                }
346	                this.waterfalls[index1].stopAtStep = 0;
347	                continue;
348	              }
349	              continue;
350	            }
351	            continue;
352	          default:
353	            x2 = 32 * this.regularFrame;
354	            break;
355	        }
356	        int num23 = 0;
357	        int num24 = this.waterfallDist;
358	        Color color4 = Color.White;
359	        for (int index4 = 0; index4 < num24; ++index4)
360	        {
361	          if (num23 < 2)
362	          {
363	            switch (index2)
364	            {
365	              case 1:
366	                double num17;
367	                float r1 = (float) (num17 = (0.550000011920929 + (double) (270 - (int) Main.mouseTextColor) / 900.0) * 0.400000005960464);
368	                float g1 = (float) (num17 * 0.300000011920929);
369	                float b1 = (float) (num17 * 0.100000001490116);
370	                Lighting.AddLight(x1, y, r1, g1, b1);
371	                break;
372	              case 2:
373	                float num18 = (float) Main.DiscoR / (float) byte.MaxValue;
374	                float num19 = (float) Main.DiscoG / (float) byte.MaxValue;
375	                float num20 = (float) Main.DiscoB / (float) byte.MaxValue;
376	                float r2 = num18 * 0.2f;
377	                float g2 = num19 * 0.2f;
378	                float b2 = num20 * 0.2f;
379	                Lighting.AddLight(x1, y, r2, g2, b2);
380	                break;
381	              case 15:
382	                float r3 = 0.0f;
383	                float g3 = 0.0f;
384	                float b3 = 0.2f;
385	                Lighting.AddLight(x1, y, r3, g3, b3);
386	                break;
387	              case 16:
388	                float r4 = 0.0f;
389	                float g4 = 0.2f;
390	                float b4 = 0.0f;
391	                Lighting.AddLight(x1, y, r4, g4, b4);
392	                break;
393	              case 17:
394	                float r5 = 0.0f;
395	                float g5 = 0.0f;
396	                float b5 = 0.2f;
397	                Lighting.AddLight(x1, y, r5, g5, b5);
398	                break;
399	              case 18:
400	                float r6 = 0.0f;
401	                float g6 = 0.2f;
402	                float b6 = 0.0f;
403	                Lighting.AddLight(x1, y, r6, g6, b6);
404	                break;
405	              case 19:
406	                float r7 = 0.2f;
407	                float g7 = 0.0f;
408	                float b7 = 0.0f;
409	                Lighting.AddLight(x1, y, r7, g7, b7);
410	                break;
411	              case 20:
412	                Lighting.AddLight(x1, y, 0.2f, 0.2f, 0.2f);
413	                break;
414	              case 21:
415	                float r8 = 0.2f;
416	                float g8 = 0.0f;
417	                float b8 = 0.0f;
418	                Lighting.AddLight(x1, y, r8, g8, b8);
419	                break;
420	            }
421	            Tile tile = Main.tile[x1, y];
422	            if (tile == null)
423	            {
424	              tile = new Tile();
425	              Main.tile[x1, y] = tile;
426	            }
427	            if (!tile.nactive() || !Main.tileSolid[(int) tile.type] || (Main.tileSolidTop[(int) tile.type] || TileID.Sets.Platforms[(int) tile.type]) || tile.blockType() != 0)
428	            {
429	              Tile testTile1 = Main.tile[x1 - 1, y];
430	              if (testTile1 == null)
431	              {
432	                testTile1 = new Tile();
433	                Main.tile[x1 - 1, y] = testTile1;
434	              }
435	              Tile testTile2 = Main.tile[x1, y + 1];
436	              if (testTile2 == null)
437	              {
438	                testTile2 = new Tile();
439	                Main.tile[x1, y + 1] = testTile2;
440	              }
441	              Tile testTile3 = Main.tile[x1 + 1, y];
442	              if (testTile3 == null)
443	              {
444	                testTile3 = new Tile();
445	                Main.tile[x1 + 1, y] = testTile3;
446	              }
447	              int num21 = (int) tile.liquid / 16;
448	              int num22 = 0;
449	              int num25 = num15;
450	              int num26;
451	              int num27;
452	              if (testTile2.topSlope() && !tile.halfBrick() && testTile2.type != (ushort) 19)
453	              {
454	                if (testTile2.slope() == (byte) 1)
455	                {
456	                  num22 = 1;
457	                  num26 = 1;
458	                  num14 = 1;
459	                  num15 = num14;
460	                }
461	                else
462	                {
463	                  num22 = -1;
464	                  num26 = -1;
465	                  num14 = -1;
466	                  num15 = num14;
467	                }
468	                num27 = 1;
469	              }
470	              else if (!WorldGen.SolidTile(testTile2) && !testTile2.bottomSlope() && !tile.halfBrick() || !testTile2.active() && !tile.halfBrick())
471	              {
472	                num23 = 0;
473	                num27 = 1;
474	                num26 = 0;
475	              }
476	              else if ((WorldGen.SolidTile(testTile1) || testTile1.topSlope() || testTile1.liquid > (byte) 0) && (!WorldGen.SolidTile(testTile3) && testTile3.liquid == (byte) 0))
477	              {
478	                if (num14 == -1)
479	                  ++num23;
480	                num26 = 1;
481	                num27 = 0;
482	                num14 = 1;
483	              }
484	              else if ((WorldGen.SolidTile(testTile3) || testTile3.topSlope() || testTile3.liquid > (byte) 0) && (!WorldGen.SolidTile(testTile1) && testTile1.liquid == (byte) 0))
485	              {
486	                if (num14 == 1)
487	                  ++num23;
488	                num26 = -1;
489	                num27 = 0;
490	                num14 = -1;
491	              }
492	              else if ((!WorldGen.SolidTile(testTile3) && !tile.topSlope() || testTile3.liquid == (byte) 0) && (!WorldGen.SolidTile(testTile1) && !tile.topSlope() && testTile1.liquid == (byte) 0))
493	              {
494	                num27 = 0;
495	                num26 = num14;
496	              }
497	              else
498	              {
499	                ++num23;
500	                num27 = 0;
501	                num26 = 0;
502	              }
503	              if (num23 >= 2)
504	              {
505	                num14 *= -1;
506	                num26 *= -1;
507	              }
508	              int num28 = -1;
509	              if (index2 != 1 && index2 != 14)
510	              {
511	                if (testTile2.active())
512	                  num28 = (int) testTile2.type;
513	                if (tile.active())
514	                  num28 = (int) tile.type;
515	              }
516	              switch (num28)
517	              {
518	                case 160:
519	                  index2 = 2;
520	                  break;
521	                case 262:
522	                case 263:
523	                case 264:
524	                case 265:
525	                case 266:
526	                case 267:
527	                case 268:
528	                  index2 = 15 + num28 - 262;
529	                  break;
530	              }
531	              if (WorldGen.SolidTile(testTile2) && !tile.halfBrick())
532	                num11 = 8;
533	              else if (num13 != 0)
534	                num11 = 0;
535	              Color color1 = Lighting.GetColor(x1, y);
536	              Color color2 = color1;
537	              float num29;
538	              switch (index2)
539	              {
540	                case 1:
541	                  num29 = 1f;
542	                  break;
543	                case 14:
544	                  num29 = 0.8f;
545	                  break;
546	                default:
547	                  num29 = tile.wall != (ushort) 0 || (double) y >= Main.worldSurface ? 0.6f * Alpha : Alpha;
548	                  break;
549	              }
550	              if (index4 > num24 - 10)
551	                num29 *= (float) (num24 - index4) / 10f;
552	              float num30 = (float) color1.R * num29;
553	              float num31 = (float) color1.G * num29;
554	              float num32 = (float) color1.B * num29;
555	              float num33 = (float) color1.A * num29;
556	              switch (index2)
557	              {
558	                case 1:
559	                  if ((double) num30 < 190.0 * (double) num29)
560	                    num30 = 190f * num29;
561	                  if ((double) num31 < 190.0 * (double) num29)
562	                    num31 = 190f * num29;
563	                  if ((double) num32 < 190.0 * (double) num29)
564	                  {
565	                    num32 = 190f * num29;
566	                    break;
567	                  }
568	                  break;
569	                case 2:

```


---

## 🤖 Assistant · 2026-08-09T02:57:37.957Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "limit": 200,
 "offset": 7560
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:37.967Z

**📎 ToolResult**

```
7560	        if (WorldGen.genRand.Next(maxValue1) != 0)
7561	          return;
7562	        WorldGen.ShellPile(shellStartXRight - WorldGen.genRand.Next(10, 25), shellStartYRight);
7563	      }));
7564	      WorldGen.AddGenerationPass("Smooth World", (WorldGenLegacyMethod) ((progress, passConfig) =>
7565	      {
7566	        progress.Message = Lang.gen[60].Value;
7567	        Main.tileSolid[(int) WorldGen.crackedType] = true;
7568	        for (int index1 = 20; index1 < Main.maxTilesX - 20; ++index1)
7569	        {
7570	          float num2 = (float) index1 / (float) Main.maxTilesX;
7571	          progress.Set(num2);
7572	          for (int index2 = 20; index2 < Main.maxTilesY - 20; ++index2)
7573	          {
7574	            if (Main.tile[index1, index2].type != (ushort) 48 && Main.tile[index1, index2].type != (ushort) 137 && (Main.tile[index1, index2].type != (ushort) 232 && Main.tile[index1, index2].type != (ushort) 191) && (Main.tile[index1, index2].type != (ushort) 151 && Main.tile[index1, index2].type != (ushort) 274))
7575	            {
7576	              if (!Main.tile[index1, index2 - 1].active() && Main.tile[index1 - 1, index2].type != (ushort) 136 && Main.tile[index1 + 1, index2].type != (ushort) 136)
7577	              {
7578	                if (WorldGen.SolidTile(index1, index2, false) && TileID.Sets.CanBeClearedDuringGeneration[(int) Main.tile[index1, index2].type])
7579	                {
7580	                  if (!Main.tile[index1 - 1, index2].halfBrick() && !Main.tile[index1 + 1, index2].halfBrick() && (Main.tile[index1 - 1, index2].slope() == (byte) 0 && Main.tile[index1 + 1, index2].slope() == (byte) 0))
7581	                  {
7582	                    if (WorldGen.SolidTile(index1, index2 + 1, false))
7583	                    {
7584	                      if (!WorldGen.SolidTile(index1 - 1, index2, false) && !Main.tile[index1 - 1, index2 + 1].halfBrick() && (WorldGen.SolidTile(index1 - 1, index2 + 1, false) && WorldGen.SolidTile(index1 + 1, index2, false)) && !Main.tile[index1 + 1, index2 - 1].active())
7585	                      {
7586	                        if (WorldGen.genRand.Next(2) == 0)
7587	                          WorldGen.SlopeTile(index1, index2, 2, false);
7588	                        else
7589	                          WorldGen.PoundTile(index1, index2);
7590	                      }
7591	                      else if (!WorldGen.SolidTile(index1 + 1, index2, false) && !Main.tile[index1 + 1, index2 + 1].halfBrick() && (WorldGen.SolidTile(index1 + 1, index2 + 1, false) && WorldGen.SolidTile(index1 - 1, index2, false)) && !Main.tile[index1 - 1, index2 - 1].active())
7592	                      {
7593	                        if (WorldGen.genRand.Next(2) == 0)
7594	                          WorldGen.SlopeTile(index1, index2, 1, false);
7595	                        else
7596	                          WorldGen.PoundTile(index1, index2);
7597	                      }
7598	                      else if (WorldGen.SolidTile(index1 + 1, index2 + 1, false) && WorldGen.SolidTile(index1 - 1, index2 + 1, false) && (!Main.tile[index1 + 1, index2].active() && !Main.tile[index1 - 1, index2].active()))
7599	                        WorldGen.PoundTile(index1, index2);
7600	                      if (WorldGen.SolidTile(index1, index2, false))
7601	                      {
7602	                        if (WorldGen.SolidTile(index1 - 1, index2, false) && WorldGen.SolidTile(index1 + 1, index2 + 2, false) && (!Main.tile[index1 + 1, index2].active() && !Main.tile[index1 + 1, index2 + 1].active()) && !Main.tile[index1 - 1, index2 - 1].active())
7603	                          WorldGen.KillTile(index1, index2, false, false, false);
7604	                        else if (WorldGen.SolidTile(index1 + 1, index2, false) && WorldGen.SolidTile(index1 - 1, index2 + 2, false) && (!Main.tile[index1 - 1, index2].active() && !Main.tile[index1 - 1, index2 + 1].active()) && !Main.tile[index1 + 1, index2 - 1].active())
7605	                          WorldGen.KillTile(index1, index2, false, false, false);
7606	                        else if (!Main.tile[index1 - 1, index2 + 1].active() && !Main.tile[index1 - 1, index2].active() && (WorldGen.SolidTile(index1 + 1, index2, false) && WorldGen.SolidTile(index1, index2 + 2, false)))
7607	                        {
7608	                          if (WorldGen.genRand.Next(5) == 0)
7609	                            WorldGen.KillTile(index1, index2, false, false, false);
7610	                          else if (WorldGen.genRand.Next(5) == 0)
7611	                            WorldGen.PoundTile(index1, index2);
7612	                          else
7613	                            WorldGen.SlopeTile(index1, index2, 2, false);
7614	                        }
7615	                        else if (!Main.tile[index1 + 1, index2 + 1].active() && !Main.tile[index1 + 1, index2].active() && (WorldGen.SolidTile(index1 - 1, index2, false) && WorldGen.SolidTile(index1, index2 + 2, false)))
7616	                        {
7617	                          if (WorldGen.genRand.Next(5) == 0)
7618	                            WorldGen.KillTile(index1, index2, false, false, false);
7619	                          else if (WorldGen.genRand.Next(5) == 0)
7620	                            WorldGen.PoundTile(index1, index2);
7621	                          else
7622	                            WorldGen.SlopeTile(index1, index2, 1, false);
7623	                        }
7624	                      }
7625	                    }
7626	                    if (WorldGen.SolidTile(index1, index2, false) && !Main.tile[index1 - 1, index2].active() && !Main.tile[index1 + 1, index2].active())
7627	                      WorldGen.KillTile(index1, index2, false, false, false);
7628	                  }
7629	                }
7630	                else if (!Main.tile[index1, index2].active() && Main.tile[index1, index2 + 1].type != (ushort) 151 && Main.tile[index1, index2 + 1].type != (ushort) 274)
7631	                {
7632	                  if (Main.tile[index1 + 1, index2].type != (ushort) 190 && Main.tile[index1 + 1, index2].type != (ushort) 48 && (Main.tile[index1 + 1, index2].type != (ushort) 232 && WorldGen.SolidTile(index1 - 1, index2 + 1, false)) && (WorldGen.SolidTile(index1 + 1, index2, false) && !Main.tile[index1 - 1, index2].active() && !Main.tile[index1 + 1, index2 - 1].active()))
7633	                  {
7634	                    if (Main.tile[index1 + 1, index2].type == (ushort) 495)
7635	                      WorldGen.PlaceTile(index1, index2, (int) Main.tile[index1 + 1, index2].type, false, false, -1, 0);
7636	                    else
7637	                      WorldGen.PlaceTile(index1, index2, (int) Main.tile[index1, index2 + 1].type, false, false, -1, 0);
7638	                    if (WorldGen.genRand.Next(2) == 0)
7639	                      WorldGen.SlopeTile(index1, index2, 2, false);
7640	                    else
7641	                      WorldGen.PoundTile(index1, index2);
7642	                  }
7643	                  if (Main.tile[index1 - 1, index2].type != (ushort) 190 && Main.tile[index1 - 1, index2].type != (ushort) 48 && (Main.tile[index1 - 1, index2].type != (ushort) 232 && WorldGen.SolidTile(index1 + 1, index2 + 1, false)) && (WorldGen.SolidTile(index1 - 1, index2, false) && !Main.tile[index1 + 1, index2].active() && !Main.tile[index1 - 1, index2 - 1].active()))
7644	                  {
7645	                    if (Main.tile[index1 - 1, index2].type == (ushort) 495)
7646	                      WorldGen.PlaceTile(index1, index2, (int) Main.tile[index1 - 1, index2].type, false, false, -1, 0);
7647	                    else
7648	                      WorldGen.PlaceTile(index1, index2, (int) Main.tile[index1, index2 + 1].type, false, false, -1, 0);
7649	                    if (WorldGen.genRand.Next(2) == 0)
7650	                      WorldGen.SlopeTile(index1, index2, 1, false);
7651	                    else
7652	                      WorldGen.PoundTile(index1, index2);
7653	                  }
7654	                }
7655	              }
7656	              else if (!Main.tile[index1, index2 + 1].active() && WorldGen.genRand.Next(2) == 0 && (WorldGen.SolidTile(index1, index2, false) && !Main.tile[index1 - 1, index2].halfBrick()) && (!Main.tile[index1 + 1, index2].halfBrick() && Main.tile[index1 - 1, index2].slope() == (byte) 0 && (Main.tile[index1 + 1, index2].slope() == (byte) 0 && WorldGen.SolidTile(index1, index2 - 1, false))))
7657	              {
7658	                if (WorldGen.SolidTile(index1 - 1, index2, false) && !WorldGen.SolidTile(index1 + 1, index2, false) && WorldGen.SolidTile(index1 - 1, index2 - 1, false))
7659	                  WorldGen.SlopeTile(index1, index2, 3, false);
7660	                else if (WorldGen.SolidTile(index1 + 1, index2, false) && !WorldGen.SolidTile(index1 - 1, index2, false) && WorldGen.SolidTile(index1 + 1, index2 - 1, false))
7661	                  WorldGen.SlopeTile(index1, index2, 4, false);
7662	              }
7663	              if (TileID.Sets.Conversion.Sand[(int) Main.tile[index1, index2].type])
7664	                Tile.SmoothSlope(index1, index2, false, false);
7665	            }
7666	          }
7667	        }
7668	        for (int i = 20; i < Main.maxTilesX - 20; ++i)
7669	        {
7670	          for (int j = 20; j < Main.maxTilesY - 20; ++j)
7671	          {
7672	            if (WorldGen.genRand.Next(2) == 0 && !Main.tile[i, j - 1].active() && (Main.tile[i, j].type != (ushort) 137 && Main.tile[i, j].type != (ushort) 48) && (Main.tile[i, j].type != (ushort) 232 && Main.tile[i, j].type != (ushort) 191 && (Main.tile[i, j].type != (ushort) 151 && Main.tile[i, j].type != (ushort) 274)) && (Main.tile[i, j].type != (ushort) 75 && Main.tile[i, j].type != (ushort) 76 && (WorldGen.SolidTile(i, j, false) && Main.tile[i - 1, j].type != (ushort) 137) && Main.tile[i + 1, j].type != (ushort) 137))
7673	            {
7674	              if (WorldGen.SolidTile(i, j + 1, false) && WorldGen.SolidTile(i + 1, j, false) && !Main.tile[i - 1, j].active())
7675	                WorldGen.SlopeTile(i, j, 2, false);
7676	              if (WorldGen.SolidTile(i, j + 1, false) && WorldGen.SolidTile(i - 1, j, false) && !Main.tile[i + 1, j].active())
7677	                WorldGen.SlopeTile(i, j, 1, false);
7678	            }
7679	            if (Main.tile[i, j].slope() == (byte) 1 && !WorldGen.SolidTile(i - 1, j, false))
7680	            {
7681	              WorldGen.SlopeTile(i, j, 0, false);
7682	              WorldGen.PoundTile(i, j);
7683	            }
7684	            if (Main.tile[i, j].slope() == (byte) 2 && !WorldGen.SolidTile(i + 1, j, false))
7685	            {
7686	              WorldGen.SlopeTile(i, j, 0, false);
7687	              WorldGen.PoundTile(i, j);
7688	            }
7689	          }
7690	        }
7691	        Main.tileSolid[137] = true;
7692	        Main.tileSolid[190] = false;
7693	        Main.tileSolid[192] = false;
7694	        Main.tileSolid[(int) WorldGen.crackedType] = false;
7695	      }));
7696	      WorldGen.AddGenerationPass("Waterfalls", (WorldGenLegacyMethod) ((progress, passConfig) =>
7697	      {
7698	        progress.Message = Lang.gen[69].Value;
7699	        Main.tileSolid[191] = false;
7700	        for (int i = 20; i < Main.maxTilesX - 20; ++i)
7701	        {
7702	          float num2 = (float) i / (float) Main.maxTilesX;
7703	          progress.Set(num2 * 0.5f);
7704	          for (int j = 20; j < Main.maxTilesY - 20; ++j)
7705	          {
7706	            if (WorldGen.SolidTile(i, j, false) && !Main.tile[i - 1, j].active() && (WorldGen.SolidTile(i, j + 1, false) && !Main.tile[i + 1, j].active()) && (Main.tile[i - 1, j].liquid > (byte) 0 || Main.tile[i + 1, j].liquid > (byte) 0))
7707	            {
7708	              bool flag = true;
7709	              int num3 = WorldGen.genRand.Next(8, 20);
7710	              int num4 = WorldGen.genRand.Next(8, 20);
7711	              int num5 = j - num3;
7712	              int num6 = num4 + j;
7713	              for (int index = num5; index <= num6; ++index)
7714	              {
7715	                if (Main.tile[i, index].halfBrick())
7716	                  flag = false;
7717	              }
7718	              if ((Main.tile[i, j].type == (ushort) 75 || Main.tile[i, j].type == (ushort) 76) && WorldGen.genRand.Next(10) != 0)
7719	                flag = false;
7720	              if (flag)
7721	                WorldGen.PoundTile(i, j);
7722	            }
7723	          }
7724	        }
7725	        for (int i = 20; i < Main.maxTilesX - 20; ++i)
7726	        {
7727	          float num2 = (float) i / (float) Main.maxTilesX;
7728	          progress.Set((float) ((double) num2 * 0.5 + 0.5));
7729	          for (int j = 20; j < Main.maxTilesY - 20; ++j)
7730	          {
7731	            if (Main.tile[i, j].type != (ushort) 48 && Main.tile[i, j].type != (ushort) 232 && (WorldGen.SolidTile(i, j, false) && WorldGen.SolidTile(i, j + 1, false)))
7732	            {
7733	              if (!WorldGen.SolidTile(i + 1, j, false) && Main.tile[i - 1, j].halfBrick() && Main.tile[i - 2, j].liquid > (byte) 0)
7734	                WorldGen.PoundTile(i, j);
7735	              if (!WorldGen.SolidTile(i - 1, j, false) && Main.tile[i + 1, j].halfBrick() && Main.tile[i + 2, j].liquid > (byte) 0)
7736	                WorldGen.PoundTile(i, j);
7737	            }
7738	          }
7739	        }
7740	        Main.tileSolid[191] = true;
7741	      }));
7742	      WorldGen.AddGenerationPass("Ice", (WorldGenLegacyMethod) ((progress, passConfig) =>
7743	      {
7744	        if (WorldGen.notTheBees)
7745	          WorldGen.NotTheBees();
7746	        progress.Set(1f);
7747	        for (int i = 10; i < Main.maxTilesX - 10; ++i)
7748	        {
7749	          for (int worldSurface1 = (int) Main.worldSurface; worldSurface1 < Main.maxTilesY - 100; ++worldSurface1)
7750	          {
7751	            if (Main.tile[i, worldSurface1].liquid > (byte) 0 && !Main.tile[i, worldSurface1].lava())
7752	              WorldGen.MakeWateryIceThing(i, worldSurface1);
7753	          }
7754	        }
7755	        Main.tileSolid[226] = false;
7756	        Main.tileSolid[162] = false;
7757	      }));
7758	      WorldGen.AddGenerationPass("Wall Variety", (WorldGenLegacyMethod) ((progress, passConfig) =>
7759	      {

```


---

## 🤖 Assistant · 2026-08-09T02:57:40.220Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read the remaining parts of WaterfallManager.cs draw (L569-803) to check the rest of the walk loop and stop conditions, and also find the FindWaterfalls beginning (L1-90).
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:57:40.224Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WaterfallManager.cs",
 "limit": 90
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:40.233Z

**📎 ToolResult**

```
1	// Decompiled with JetBrains decompiler
2	// Type: Terraria.WaterfallManager
3	// Assembly: Terraria, Version=1.4.0.5, Culture=neutral, PublicKeyToken=null
4	// MVID: 67F9E73E-0A81-4937-A22C-5515CD405A83
5	// Assembly location: C:\Program Files (x86)\Steam\steamapps\common\Terraria\Terraria.exe
6	
7	using Microsoft.Xna.Framework;
8	using Microsoft.Xna.Framework.Graphics;
9	using ReLogic.Content;
10	using System;
11	using Terraria.ID;
12	using Terraria.IO;
13	
14	namespace Terraria
15	{
16	  public class WaterfallManager
17	  {
18	    public int maxWaterfallCount = 1000;
19	    private Asset<Texture2D>[] waterfallTexture = new Asset<Texture2D>[24];
20	    private int waterfallDist = 100;
21	    private const int minWet = 160;
22	    private const int maxWaterfallCountDefault = 1000;
23	    private const int maxLength = 100;
24	    private const int maxTypes = 24;
25	    private int qualityMax;
26	    private int currentMax;
27	    private WaterfallManager.WaterfallData[] waterfalls;
28	    private int wFallFrCounter;
29	    private int regularFrame;
30	    private int wFallFrCounter2;
31	    private int slowFrame;
32	    private int rainFrameCounter;
33	    private int rainFrameForeground;
34	    private int rainFrameBackground;
35	    private int snowFrameCounter;
36	    private int snowFrameForeground;
37	    private int findWaterfallCount;
38	
39	    public WaterfallManager()
40	    {
41	      this.waterfalls = new WaterfallManager.WaterfallData[1000];
42	      Main.Configuration.OnLoad += (Action<Preferences>) (preferences =>
43	      {
44	        this.maxWaterfallCount = Math.Max(0, preferences.Get<int>("WaterfallDrawLimit", 1000));
45	        this.waterfalls = new WaterfallManager.WaterfallData[this.maxWaterfallCount];
46	      });
47	    }
48	
49	    public void LoadContent()
50	    {
51	      for (int index = 0; index < 24; ++index)
52	        this.waterfallTexture[index] = (Asset<Texture2D>) Main.Assets.Request<Texture2D>("Images/Waterfall_" + (object) index, (AssetRequestMode) 2);
53	    }
54	
55	    public bool CheckForWaterfall(int i, int j)
56	    {
57	      for (int index = 0; index < this.currentMax; ++index)
58	      {
59	        if (this.waterfalls[index].x == i && this.waterfalls[index].y == j)
60	          return true;
61	      }
62	      return false;
63	    }
64	
65	    public void FindWaterfalls(bool forced = false)
66	    {
67	      ++this.findWaterfallCount;
68	      if (this.findWaterfallCount < 30 && !forced)
69	        return;
70	      this.findWaterfallCount = 0;
71	      this.waterfallDist = (int) (75.0 * (double) Main.gfxQuality) + 25;
72	      this.qualityMax = (int) ((double) this.maxWaterfallCount * (double) Main.gfxQuality);
73	      this.currentMax = 0;
74	      int num1 = (int) ((double) Main.screenPosition.X / 16.0 - 1.0);
75	      int num2 = (int) (((double) Main.screenPosition.X + (double) Main.screenWidth) / 16.0) + 2;
76	      int num3 = (int) ((double) Main.screenPosition.Y / 16.0 - 1.0);
77	      int num4 = (int) (((double) Main.screenPosition.Y + (double) Main.screenHeight) / 16.0) + 2;
78	      int num5 = num1 - this.waterfallDist;
79	      int num6 = num2 + this.waterfallDist;
80	      int num7 = num3 - this.waterfallDist;
81	      int num8 = num4 + 20;
82	      if (num5 < 0)
83	        num5 = 0;
84	      if (num6 > Main.maxTilesX)
85	        num6 = Main.maxTilesX;
86	      if (num7 < 0)
87	        num7 = 0;
88	      if (num8 > Main.maxTilesY)
89	        num8 = Main.maxTilesY;
90	      for (int index1 = num5; index1 < num6; ++index1)

```


---

## 🤖 Assistant · 2026-08-09T02:57:40.319Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WaterfallManager.cs",
 "limit": 240,
 "offset": 569
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:57:40.325Z

**📎 ToolResult**

```
569	                case 2:
570	                  num30 = (float) Main.DiscoR * num29;
571	                  num31 = (float) Main.DiscoG * num29;
572	                  num32 = (float) Main.DiscoB * num29;
573	                  break;
574	                case 15:
575	                case 16:
576	                case 17:
577	                case 18:
578	                case 19:
579	                case 20:
580	                case 21:
581	                  num30 = (float) byte.MaxValue * num29;
582	                  num31 = (float) byte.MaxValue * num29;
583	                  num32 = (float) byte.MaxValue * num29;
584	                  break;
585	              }
586	              color1 = new Color((int) num30, (int) num31, (int) num32, (int) num33);
587	              if (index2 == 1)
588	              {
589	                float num34 = Math.Abs((float) (x1 * 16 + 8) - (Main.screenPosition.X + (float) (Main.screenWidth / 2)));
590	                float num35 = Math.Abs((float) (y * 16 + 8) - (Main.screenPosition.Y + (float) (Main.screenHeight / 2)));
591	                if ((double) num34 < (double) (Main.screenWidth * 2) && (double) num35 < (double) (Main.screenHeight * 2))
592	                {
593	                  float num36 = (float) (1.0 - Math.Sqrt((double) num34 * (double) num34 + (double) num35 * (double) num35) / ((double) Main.screenWidth * 0.75));
594	                  if ((double) num36 > 0.0)
595	                    num6 += num36;
596	                }
597	                if ((double) num34 < (double) num7)
598	                {
599	                  num7 = num34;
600	                  num9 = x1 * 16 + 8;
601	                }
602	                if ((double) num35 < (double) num8)
603	                {
604	                  num8 = num34;
605	                  num10 = y * 16 + 8;
606	                }
607	              }
608	              else if (index2 != 1 && index2 != 14 && (index2 != 11 && index2 != 12) && index2 != 22)
609	              {
610	                float num34 = Math.Abs((float) (x1 * 16 + 8) - (Main.screenPosition.X + (float) (Main.screenWidth / 2)));
611	                float num35 = Math.Abs((float) (y * 16 + 8) - (Main.screenPosition.Y + (float) (Main.screenHeight / 2)));
612	                if ((double) num34 < (double) (Main.screenWidth * 2) && (double) num35 < (double) (Main.screenHeight * 2))
613	                {
614	                  float num36 = (float) (1.0 - Math.Sqrt((double) num34 * (double) num34 + (double) num35 * (double) num35) / ((double) Main.screenWidth * 0.75));
615	                  if ((double) num36 > 0.0)
616	                    num1 += num36;
617	                }
618	                if ((double) num34 < (double) num2)
619	                {
620	                  num2 = num34;
621	                  num4 = x1 * 16 + 8;
622	                }
623	                if ((double) num35 < (double) num3)
624	                {
625	                  num3 = num34;
626	                  num5 = y * 16 + 8;
627	                }
628	              }
629	              if (index4 > 50 && (color2.R > (byte) 20 || color2.B > (byte) 20 || color2.G > (byte) 20))
630	              {
631	                float num34 = (float) color2.R;
632	                if ((double) color2.G > (double) num34)
633	                  num34 = (float) color2.G;
634	                if ((double) color2.B > (double) num34)
635	                  num34 = (float) color2.B;
636	                if ((double) Main.rand.Next(20000) < (double) num34 / 30.0)
637	                {
638	                  int index5 = Dust.NewDust(new Vector2((float) (x1 * 16 - num14 * 7), (float) (y * 16 + 6)), 10, 8, 43, 0.0f, 0.0f, 254, Color.White, 0.5f);
639	                  Main.dust[index5].velocity *= 0.0f;
640	                }
641	              }
642	              if (num12 == 0 && num22 != 0 && (num13 == 1 && num14 != num15))
643	              {
644	                num22 = 0;
645	                num14 = num15;
646	                color1 = Color.White;
647	                if (num14 == 1)
648	                  spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16 - 16), (float) (y * 16 + 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color1, 0.0f, Vector2.Zero, 1f, SpriteEffects.FlipHorizontally, 0.0f);
649	                else
650	                  spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16 - 16), (float) (y * 16 + 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 8)), color1, 0.0f, Vector2.Zero, 1f, SpriteEffects.FlipHorizontally, 0.0f);
651	              }
652	              if (num16 != 0 && num26 == 0 && num27 == 1)
653	              {
654	                if (num14 == 1)
655	                {
656	                  if (index3 != index2)
657	                    spriteBatch.Draw(this.waterfallTexture[index3].Value, new Vector2((float) (x1 * 16), (float) (y * 16 + num11 + 8)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 0, 16, 16 - num21 - 8)), color4, 0.0f, Vector2.Zero, 1f, SpriteEffects.FlipHorizontally, 0.0f);
658	                  else
659	                    spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16 + num11 + 8)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 0, 16, 16 - num21 - 8)), color1, 0.0f, Vector2.Zero, 1f, SpriteEffects.FlipHorizontally, 0.0f);
660	                }
661	                else
662	                  spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16 + num11 + 8)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 0, 16, 16 - num21 - 8)), color1, 0.0f, Vector2.Zero, 1f, SpriteEffects.None, 0.0f);
663	              }
664	              if (num11 == 8 && num13 == 1 && num16 == 0)
665	              {
666	                if (num15 == -1)
667	                {
668	                  if (index3 != index2)
669	                    spriteBatch.Draw(this.waterfallTexture[index3].Value, new Vector2((float) (x1 * 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 8)), color4, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
670	                  else
671	                    spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 8)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
672	                }
673	                else if (index3 != index2)
674	                  spriteBatch.Draw(this.waterfallTexture[index3].Value, new Vector2((float) (x1 * 16 - 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 8)), color4, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
675	                else
676	                  spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16 - 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 8)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
677	              }
678	              if (num22 != 0 && num12 == 0)
679	              {
680	                if (num25 == 1)
681	                {
682	                  if (index3 != index2)
683	                    spriteBatch.Draw(this.waterfallTexture[index3].Value, new Vector2((float) (x1 * 16 - 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color4, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
684	                  else
685	                    spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16 - 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
686	                }
687	                else if (index3 != index2)
688	                  spriteBatch.Draw(this.waterfallTexture[index3].Value, new Vector2((float) (x1 * 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color4, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
689	                else
690	                  spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
691	              }
692	              if (num27 == 1 && num22 == 0 && num16 == 0)
693	              {
694	                if (num14 == -1)
695	                {
696	                  if (num13 == 0)
697	                    spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16 + num11)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 0, 16, 16 - num21)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
698	                  else if (index3 != index2)
699	                    spriteBatch.Draw(this.waterfallTexture[index3].Value, new Vector2((float) (x1 * 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color4, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
700	                  else
701	                    spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
702	                }
703	                else if (num13 == 0)
704	                  spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16 + num11)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 0, 16, 16 - num21)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
705	                else if (index3 != index2)
706	                  spriteBatch.Draw(this.waterfallTexture[index3].Value, new Vector2((float) (x1 * 16 - 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color4, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
707	                else
708	                  spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16 - 16), (float) (y * 16)) - Main.screenPosition, new Rectangle?(new Rectangle(x2, 24, 32, 16 - num21)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
709	              }
710	              else
711	              {
712	                switch (num26)
713	                {
714	                  case -1:
715	                    if (Main.tile[x1, y].liquid <= (byte) 0 || Main.tile[x1, y].halfBrick())
716	                    {
717	                      if (num22 == -1)
718	                      {
719	                        for (int index5 = 0; index5 < 8; ++index5)
720	                        {
721	                          int num34 = index5 * 2;
722	                          int num35 = index5 * 2;
723	                          int num36 = 14 - index5 * 2;
724	                          num11 = 8;
725	                          if (num12 == 0 && index5 > 5)
726	                            num36 = 4;
727	                          spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16 + num34), (float) (y * 16 + num11 + num36)) - Main.screenPosition, new Rectangle?(new Rectangle(16 + x2 + num35, 0, 2, 16 - num11)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
728	                        }
729	                        break;
730	                      }
731	                      int height = 16;
732	                      if (TileID.Sets.BlocksWaterDrawingBehindSelf[(int) Main.tile[x1, y].type])
733	                        height = 8;
734	                      else if (TileID.Sets.BlocksWaterDrawingBehindSelf[(int) Main.tile[x1, y + 1].type])
735	                        height = 8;
736	                      spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16 + num11)) - Main.screenPosition, new Rectangle?(new Rectangle(16 + x2, 0, 16, height)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
737	                      break;
738	                    }
739	                    break;
740	                  case 0:
741	                    if (num27 == 0)
742	                    {
743	                      if (Main.tile[x1, y].liquid <= (byte) 0 || Main.tile[x1, y].halfBrick())
744	                        spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16 + num11)) - Main.screenPosition, new Rectangle?(new Rectangle(16 + x2, 0, 16, 16)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.None, 0.0f);
745	                      index4 = 1000;
746	                      break;
747	                    }
748	                    break;
749	                  case 1:
750	                    if (Main.tile[x1, y].liquid <= (byte) 0 || Main.tile[x1, y].halfBrick())
751	                    {
752	                      if (num22 == 1)
753	                      {
754	                        for (int index5 = 0; index5 < 8; ++index5)
755	                        {
756	                          int num34 = index5 * 2;
757	                          int num35 = 14 - index5 * 2;
758	                          int num36 = num34;
759	                          num11 = 8;
760	                          if (num12 == 0 && index5 < 2)
761	                            num36 = 4;
762	                          spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16 + num34), (float) (y * 16 + num11 + num36)) - Main.screenPosition, new Rectangle?(new Rectangle(16 + x2 + num35, 0, 2, 16 - num11)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
763	                        }
764	                        break;
765	                      }
766	                      int height = 16;
767	                      if (TileID.Sets.BlocksWaterDrawingBehindSelf[(int) Main.tile[x1, y].type])
768	                        height = 8;
769	                      else if (TileID.Sets.BlocksWaterDrawingBehindSelf[(int) Main.tile[x1, y + 1].type])
770	                        height = 8;
771	                      spriteBatch.Draw(this.waterfallTexture[index2].Value, new Vector2((float) (x1 * 16), (float) (y * 16 + num11)) - Main.screenPosition, new Rectangle?(new Rectangle(16 + x2, 0, 16, height)), color1, 0.0f, new Vector2(), 1f, SpriteEffects.FlipHorizontally, 0.0f);
772	                      break;
773	                    }
774	                    break;
775	                }
776	              }
777	              if (tile.liquid > (byte) 0 && !tile.halfBrick())
778	                index4 = 1000;
779	              num13 = num27;
780	              num15 = num14;
781	              num12 = num26;
782	              x1 += num26;
783	              y += num27;
784	              num16 = num22;
785	              color4 = color1;
786	              if (index3 != index2)
787	                index3 = index2;
788	              if (testTile1.active() && (testTile1.type == (ushort) 189 || testTile1.type == (ushort) 196) || testTile3.active() && (testTile3.type == (ushort) 189 || testTile3.type == (ushort) 196) || testTile2.active() && (testTile2.type == (ushort) 189 || testTile2.type == (ushort) 196))
789	                num24 = (int) ((double) (40 * (Main.maxTilesX / 4200)) * (double) Main.gfxQuality);
790	            }
791	            else
792	              break;
793	          }
794	        }
795	      }
796	      Main.ambientWaterfallX = (float) num4;
797	      Main.ambientWaterfallY = (float) num5;
798	      Main.ambientWaterfallStrength = num1;
799	      Main.ambientLavafallX = (float) num9;
800	      Main.ambientLavafallY = (float) num10;
801	      Main.ambientLavafallStrength = num6;
802	      Main.tileSolid[546] = true;
803	    }
804	
805	    public void Draw(SpriteBatch spriteBatch)
806	    {
807	      for (int index = 0; index < this.currentMax; ++index)
808	        this.waterfalls[index].stopAtStep = this.waterfallDist;

```


---

## 🤖 Assistant · 2026-08-09T02:58:50.064Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have all source. Let me carefully compare.

### 1. WaterfallRenderer.ts vs WaterfallManager.cs

**findWaterfalls:**

TS:
- throttling: `findFrame % 30 !== 1` — original: `findWaterfallCount < 30 && !forced` → runs every 30 calls. TS runs at findFrame%30===1, i.e., also every 30 calls. OK-ish. But note: original scans region extended by waterfallDist (100) horizontally beyond screen; TS only extends ±2. Minor (low) — shorter range.
- Original checks `tile.active()` then `tile.halfBrick()` — TS checks `st.flags[i] && st.half[i]`. flags presumably active. OK.
- L110: `testTile1.liquid < 16 || WorldGen.SolidTile(testTile1)`. TS: `uq < 16 || solid(x, y-1)` where solid = solidTile equivalent. OK.
- L124: `(testTile2.liquid > 160 || testTile3.liquid > 160) && (testTile2.liquid == 0 && !SolidTile(testTile2) && slope==0 || testTile3...)`. TS: lOpen = `lq===0 && !solid && slope[li]===0`. OK. One nuance: TS `st.slope[li]` accessed without bounds check but x range clamps to ≥2 so fine.
- Type: original uses `testTile1.lava() || testTile3.lava() || testTile2.lava()` — lava() is liquid type check. TS isLava checks liquidType===2 — need to check repo's liquidType encoding. Not verifying; assume ok. Note the order in original: testTile1 (up), testTile3 (right), testTile2 (left) — same as TS (ui, ri, li). OK.
- MAX check: original `currentMax < qualityMax` before adding. TS checks after push, `falls.length >= MAX_FALLS` return. Equivalent enough.

One real difference: the comment at file top (L4-5) says "触发条件按原版语义适配为'倾泻点'：液量 ≥160 的格子、正下方为空..." — that's stale/wrong documentation, but the code actually follows halfBrick. Minor doc mismatch. Might mention low.

Also original draw loop: the walk condition L427: `if (!tile.nactive() || !Main.tileSolid[type] || tileSolidTop || Platforms || tile.blockType() != 0)` — that's the condition to CONTINUE (enter the draw/walk body). If tile is active solid full block (blockType==0) and not platform/solidTop → `else break` (L791-792). So break when tile.nactive() && tileSolid && !tileSolidTop && !Platform && blockType==0. TS: `if (d && d.solid && !d.platform && !st.half[ci]) break;` — matches blockType==0 exemption for halfBrick; slope not considered (blockType() for slopes = 1..4). In repo slope exists (st.slope). TS treats slope tiles as pass-through (doesn't break), while original would break for slope tiles (blockType != 0 → continue... wait no).

Let me re-derive: L427 condition C = !nactive || !tileSolid || tileSolidTop || Platforms || blockType!=0. If C true → proceed to draw; if false → L791 `else break`. So break when: active && solid && !solidTop && !platform && blockType==0. I.e., break only on full solid block. Slope tiles (blockType 1-4) do NOT break — they're traversed. TS breaks when solid && !platform && !half — so slope tiles break in TS. Since repo generates slope 0 everywhere? HalfBrickPass says slope 3/4 not generated but slope 1/2 might be? In HalfBrickPass, SlopeTile branches were replaced with PoundTile, so slope is probably never set. So low impact. Still a deviation: TS ignores slope (treats sloped solid as full block → break), original passes through. Also original `nactive()` = active && !inActive. Not relevant.

Bigger: L470's fall-through condition: original `else if (!WorldGen.SolidTile(testTile2) && !testTile2.bottomSlope() && !tile.halfBrick() || !testTile2.active() && !tile.halfBrick())` → num27=1, num26=0 (fall down). Note: it falls down only if current tile is NOT halfBrick. If current tile is halfBrick, it does not fall through. TS: `if (!st.isSolid(cx, cy+1)) { cy++; continue; }` — no halfBrick check. So on a halfBrick lip cell, original wouldn't descend; TS descends. Impact: medium. Hmm, but wait — actually the first cell is the lip (halfBrick), and original does descend from the lip? Let's trace: at step 0, tile = lip (halfBrick). testTile2 = below. If below empty: condition `!SolidTile(below) && !bottomSlope && !tile.halfBrick()` → halfBrick true → false; second clause `!testTile2.active() && !tile.halfBrick()` → also false due to halfBrick. So falls to next branch: L476 check sides... The lip has liquid on one side (that's the trigger), so `(SolidTile(left) || left.topSlope || left.liquid>0) && (!SolidTile(right) && right.liquid==0)` — the side with liquid satisfies liquid>0, other side empty. So num26 = ±1 (move sideways), num27=0! So from the lip the original moves horizontally first, not down. Interesting — the horizontal shift happens while tile.halfBrick. Then next step tile is the air cell beside, and then it falls down (num27=1).

Hmm wait, but liquid >0 side: say left has liquid. Branch L476 requires (SolidTile(left) || topSlope(left) || left.liquid>0) && (!SolidTile(right) && right.liquid==0). Left liquid>0 → true; right empty & no solid → true. So num26=1 (move right), num27=0. So the waterfall starts by moving sideways away from the liquid, then falls. That's the "pour over the edge" look. TS: at the lip cell, it draws the lip cell itself, then `!st.isSolid(cx, cy+1)` → if below the lip is air, cy++ immediately (vertical), no sideways shift. So the TS column is one tile to the liquid side vs original. Actually the original's x after step 0 is x+1 (or x-1). TS draws at x going down. This is a positional offset deviation — medium. Hmm, but actually does it? Let's double check num23 counter and the branch. Yes.

Actually wait — is the below cell of the lip typically air? The waterfall scenario: liquid sits beside a halfBrick lip; below the lip... The lip is at the edge of a cliff, so below is air. Then original goes sideways. TS goes down. Both produce a waterfall but offset by one tile horizontally. Hmm, but careful: in the original, at step 0, before moving, it DRAWS at (x1,y) the lip cell. Then moves x1+=1. So the drawn column is at x+1 going down; the lip cell drawn at x. TS draws lip cell at x, then goes down at x. So offset. Medium impact — affects alignment with the ledge.

Hmm, but actually, wait: is it possible the below is air and this sideways-then-down... Actually there's also the possibility that below the lip is solid (lip on flat ground with water beside it — a "pour" that immediately spreads). Then original: L470 fails (below solid), L476 side branch → sideways. TS: below solid → checks rightOpen/leftOpen = !solid(x±1,y) && !solid(x±1,y+1). Original's side-move conditions are different: `(SolidTile(left)||topSlope(left)||liquid>0) && (!SolidTile(right) && right.liquid==0)`. TS rightOpen requires right non-solid and right-down non-solid; original requires only right non-solid && right no liquid (liquid check, not solid check on below). Different conditions. Also original prefers moving AWAY from liquid (if left has liquid, move right). TS prefers right always (rightOpen checked first). That's a directional bias deviation — medium.

Also the turns counting: original `num23` counts direction reversals (num14 flips sign), reset to 0 when falling straight down (L472). TS `turns` counts every sideways move and never resets on vertical fall. Original: num23 resets to 0 on fall-through; increments only when reversing direction. TS: increments on each horizontal move, cumulative. So TS stops after 2 total horizontal moves; original allows many horizontal moves as long as <2 reversals, and resets on descent. This is a significant behavioral deviation — medium/high. Impact: TS waterfalls stop earlier / can't flow long diagonals. I'd say 中.

Also L492 branch (`num27=0; num26=num14;` — continue in previous direction) — TS lacks; minor.

Also note the original `if (num23 >= 2) { num14 *= -1; num26 *= -1; }` — it REVERSES direction instead of stopping! TS breaks. Deviation: original bounces back, TS stops. Medium.

**yOff (L531-532):** original `if (WorldGen.SolidTile(testTile2) && !tile.halfBrick()) num11 = 8; else if (num13 != 0) num11 = 0;`. TS: `st.isSolid(cx, cy+1) ? 8 : 0` — missing `!tile.halfBrick()` and missing reset. The user explicitly flagged this. Need to check what st.isSolid does — presumably solid including half? Let me check TileStore.isSolid. Impact: medium (up-shift applied on halfBrick lips and sticky when leaving ground).

**Transparency (L538-551):** original: lava 1.0, honey 0.8, default `tile.wall != 0 || y >= Main.worldSurface ? 0.6 * Alpha : Alpha`. TS: `st.wall[ci] !== 0 || cy >= groundLevel ? 0.6 : 1.0` — Alpha param is 1 presumably. Need to check groundLevel passed corresponds to worldSurface. Callers? Probably. Also original lava/honey alpha NOT affected by wall/underground — TS same. OK. Tail fade `index4 > num24 - 10 → num29 *= (num24-index4)/10` — TS `step > WATERFALL_DIST - 10 → alpha *= (WATERFALL_DIST - step)/10`. num24 = waterfallDist = 100; WATERFALL_DIST=100. OK. But note original num24 can shrink to 40*maxTilesX/4200*gfxQuality near waterfall blocks (L788-789) — omitted, low.

Also original tail fade uses `index4 > num24 - 10` i.e. step > 90 → steps 91..99 multiplier (100-step)/10. TS same. Good.

**Frame animation:** original: regularFrame increments every 3 updates (counter > 2 → i.e., every 3 frames... counter increments to 3 then resets → frame advances every 3 ticks). TS: `Math.floor(nowMs/50) % 16` → every 50ms. Terraria tick = 1/60 s = 16.67ms → 3 ticks = 50ms. Correct! slow: counter > 6 → every 7 ticks = 116.7ms; TS uses 117ms. Fine. But `%16` cycles 0..15 matching. OK. One nuance: the lava/honey (slowFrame) path in original `case 1/14` also checks `Main.drewLava` and `stopAtStep != 0` — the draw is split into two passes (behind tiles / in front). TS single pass. That's architecture, low.

Also: original texture for water type uses `Style` (index2 = Style when 0), water style affects which Waterfall_N texture; TS uses fixed sheet index 0. Low.

Also missing type checks for lava light emission, ambient audio — documented omission, skip.

**断流 (stop):** L777-778: `if (tile.liquid > 0 && !tile.halfBrick()) index4 = 1000;` TS: `if (liq > 0) break;` — missing halfBrick exemption. Medium/low. Also L743-745 (num26==0 && num27==0 → index4=1000) — stop when neither down nor side move. TS has `else break` for no side open, ok. But also original only draws that final cell when `liquid<=0 || halfBrick`; TS draws regardless then breaks. Minor.

Also crop `num21 = liquid/16; height = 16 - num21` — TS `crop = floor(liq/16); sh = 16 - crop`. liquid is byte 0-255, /16 → 0..15. TS same. OK.

Also `MAX_FALLS`/qualityMax: original qualityMax = 1000 * gfxQuality; TS 1000. Fine.

Also findWaterfalls region: original extends x by waterfallDist beyond screen and y by +20 below, and importantly scans from num3 - waterfallDist vertically (above screen) — TS ±2 only. So waterfalls starting above the visible window (falling into view) are missed. Low/medium. Also original y lower bound extends 20 below screen only (not waterfallDist). TS ty1+2. So long falls partially visible won't be found if their lip is >2 tiles above the view. Medium-low. I'll list as one line: 扫描窗口 ±2 vs 原版左右 ±waterfallDist(100)/上方100/下方20 — 中.

Hmm wait, actually original: num5 = screenLeft-1 - waterfallDist, num6 = right+2 + dist; num7 = top-1-dist; num8 = bottom+2+20. Yes.

### 2. HalfBrickPass.ts vs WorldGen.cs

**runSmoothWorldPass vs L7568-7696:**

Note the user's line references (L7580-7668 etc.) don't match the actual file I read: actual pass is L7564-7695, main patterns at L7580-7628, floating stubs L7600-7624, empty corner fill L7630-7653, slope3/4 L7656-7662, second pass L7668-7689. The user's numbering is off by ~30 lines. I'll report using actual line numbers.

Deviations:

a) L7574 type skip list 48/137/232/191/151/274 → TS `d.framed` skip. Known simplification-ish; also skips everything framed. Also original checks `Main.tile[index1-1,index2].type != 136 && [index1+1] != 136` (moss? 136 = moss stone?) — TS missing the neighbor-type-136 check. Wait: L7576: `if (!Main.tile[index1,index2-1].active() && Main.tile[index1-1,index2].type != 136 && Main.tile[index1+1,index2].type != 136)`. Hmm that's inside. 136 is... "Moss block"? Actually 136 might be moss. Missing check — low. Hmm, but note that condition structure: L7576 block contains the SolidTile branch (L7578) and the else-if at L7630 (empty fill). Then L7656 `else if` attaches to L7576's if — the slope 3/4 branch requires `tile[i,j+1] not active`. And L7663 sand smooth is outside. TS: the slope3/4 branch (L7656-7662) is entirely missing (documented known deviation for slope 3/4). And sand smoothing missing — but no sand slope system; low.

b) L7578: `WorldGen.SolidTile(i,j,false) && TileID.Sets.CanBeClearedDuringGeneration[type]` — TS only checks solidTile, missing CanBeClearedDuringGeneration (e.g., dungeon brick 41 not clearable? actually 41 is clearable... chest etc.). Since solidTile already excludes non-solid, CanBeClearedDuringGeneration matters for things like obsidian? Low.

c) 模式 A (L7584): original conditions: `!SolidTile(i-1,j) && !tile[i-1,j+1].halfBrick() && (SolidTile(i-1,j+1) && SolidTile(i+1,j)) && !tile[i+1,j-1].active()`. TS L58-60: `!solidTile(i-1,j) && solidTile(i-1,j+1) && solidTile(i+1,j) && type[i-1,j]===0 && type[i+1,j-1]===0 && !half[i-1,j+1]`. All five present. ✓. Then `if (rng.chance(0.5)) poundTile else poundTile` — both branches identical (dead code) — matches "统一改 PoundTile" known deviation but the code is silly; it's effectively always PoundTile which is the stated known deviation. Not a new deviation but worth noting the 50% branch is a no-op — could mention as 低 (code smell, no behavioral diff beyond known deviation).

Wait — but there IS a behavioral difference in pattern A! Original: SlopeTile(i,j,2) OR PoundTile. PoundTile only pounds if... PoundTile requires CanPoundTile (generation path). TS poundTile → canPoundTile requires !framed. Same-ish.

d) 模式 B (L7591): original: `!SolidTile(i+1,j) && !tile[i+1,j+1].halfBrick() && (SolidTile(i+1,j+1) && SolidTile(i-1,j)) && !tile[i-1,j-1].active()`. TS L63-65 mirrors. ✓

e) 孤立凸起 (L7598): original `SolidTile(i+1,j+1) && SolidTile(i-1,j+1) && (!tile[i+1,j].active() && !tile[i-1,j].active())`. TS ✓.

f) 悬空支脚削除 5 branches (L7600-7623):
   1. L7602: `SolidTile(i-1,j) && SolidTile(i+1,j+2) && (!tile[i+1,j].active() && !tile[i+1,j+1].active()) && !tile[i-1,j-1].active()` → KillTile. TS L74-76: `solidTile(i-1,j) && solidTile(i+1,j+2) && type[i+1,j]===0 && type[i+1,j+1]===0 && type[i-1,j-1]===0` ✓.
   2. L7604 mirror ✓ (TS L78-80).
   3. L7606: `!tile[i-1,j+1].active() && !tile[i-1,j].active() && (SolidTile(i+1,j) && SolidTile(i,j+2))` → 1/5 kill, 1/5 pound, else SlopeTile(2). TS L82-85: rng.chance(0.2) kill; else rng.chance(0.25) pound; else nothing (SlopeTile omitted → known deviation). Note probability semantics: original `genRand.Next(5)==0` twice — two independent draws; TS chance(0.2) then chance(0.25) — equivalent. ✓ except slope branch missing (known).
   4. L7615 mirror ✓.
   
   Wait — original has 4 branches in the stub-removal, not 5. The user said "5 个分支" — maybe counting the isolated bump. Whatever; TS covers all 4. ✓

g) 顶部单格立柱 L7626: `SolidTile(i,j) && !tile[i-1,j].active() && !tile[i+1,j].active()` → KillTile. TS L94 ✓. But note: in original this is INSIDE the `if (!half[i-1,j] && !half[i+1,j] && slope both 0)` block (L7580) and after the `if (SolidTile(i,j+1))` block — TS has it inside the half/slope guard too (L94 within L55 block, after L92 closing). ✓ Actually check indentation: TS L94 is inside `if (!st.half[li] && ...)` (L55) — yes, at L97 closes. ✓

h) 空位补角 (L7630-7653): original outer: `else if (!tile[i,j].active() && tile[i,j+1].type != 151 && != 274)`. TS L98-101: `else if type[ti]===0` then `belowType !== 0 && !framed`. The 151/274 exclusion replaced by framed check — fine-ish (低, known simplification style).
   - Branch 1 (L7632): `tile[i+1,j].type != 190 && != 48 && != 232 && SolidTile(i-1,j+1) && (SolidTile(i+1,j) && !tile[i-1,j].active() && !tile[i+1,j-1].active())` → PlaceTile from tile[i+1,j].type if 495 else from tile[i,j+1].type; then 50% SlopeTile(2) else PoundTile. TS L102-105: `solidTile(i-1,j+1) && solidTile(i+1,j) && type[i-1,j]===0 && type[i+1,j-1]===0` → setTileSilent(belowType) + poundTile. Missing: neighbor type != 190/48/232 exclusion (190 = pesticide plant? actually 190 is... whatever; 48/232 exclusions); and 495 special-case (source type from i+1 rather than below); and SlopeTile(2) branch. Impact: 低-中. The 190/48/232 check matters when the adjacent tile is a non-solid decor like 190 (which can't be SolidTile so the SolidTile(i+1,j) already excludes 190? SolidTile(i+1,j) requires active && tileSolid — 190 is tileSolid? In pass, tileSolid[190]=false set later at L7692... during the pass 190 might be solid. Eh. Low.
   - Branch 2 mirror ✓ similar omissions.

i) 第二遍 (L7668-7689): original: `genRand.Next(2)==0 && !tile[i,j-1].active() && type not in {137,48,232,191,151,274,75,76} && (SolidTile(i,j) && tile[i-1,j].type != 137 && tile[i+1,j].type != 137)` then two SlopeTile branches (slope 2 if right solid+left empty; slope 1 if left solid+right empty). Then slope→halfBrick fallback: if slope==1 && !SolidTile(i-1,j) → SlopeTile(0)+PoundTile; slope==2 && !SolidTile(i+1,j) → same.
   TS second pass L117-130: framed skip; `rng.chance(0.5) && type[i,j-1]===0 && solidTile(i,j)` then poundTile for the two branches. Missing: neighbor 137 exclusion (低), type 75/76 (gem tree? 75/76 are... whatever) exclusion (低). The main known deviation: SlopeTile → PoundTile. Note the TS has NO equivalent of the slope fallback (slope==1/2 with open side → pound) — because slopes never generated; but the fallback also matters for slopes created elsewhere. 低.
   
   Also important: original second pass uses `!Main.tile[i,j-1].active()`; TS uses `st.type[idx]===0` ✓ equivalent.

**runWaterfallLipPass vs L7697-7743:**

第一遍 L7706: `SolidTile(i,j) && !tile[i-1,j].active() && SolidTile(i,j+1) && !tile[i+1,j].active() && (liquid[i-1]>0 || liquid[i+1]>0)`. TS L139-143 ✓. Then flag scan `j-num3..j+num4` for halfBrick in column i — TS ✓ (but TS doesn't bounds-check k negative... it does `k>=0 && k<h`). Original doesn't bounds-check but tiles exist. Fine.
- Missing: L7718 `(type==75||type==76) && genRand.Next(10)!=0 → flag=false` — 10% chance only. 75/76 are... "Amber Gemspark"? Actually 75 = ... whatever, gem trees? TS missing this exclusion entirely → those tile types always get pounded. 低 (depends if those types exist in repo). Mention 低.
- num3/num4 range: original Next(8,20) → 8..19 inclusive; TS `8 + floor(rng.next()*12)` → 8..19 ✓.

第二遍 L7731-7736: original outer: `tile[i,j].type != 48 && != 232 && (SolidTile(i,j) && SolidTile(i,j+1))`. TS L157: `!solidTile(i,j) || !solidTile(i,j+1) → continue` — missing the 48/232 exclusion (低, framed covers 48? 48 is a statue? Actually 48 might be... TS has no type check but solidTile covers solid). Then branch 1: `!SolidTile(i+1,j) && tile[i-1,j].halfBrick() && tile[i-2,j].liquid>0` → Pound. TS L158 ✓. Branch 2 ✓.

Also note pass ordering: original "Smooth World" L7663 `Tile.SmoothSlope` for sand — missing (低).

Also `Main.tileSolid[crackedType]=true` during pass — repo N/A.

Also the user-stated known deviations (SlopeTile→PoundTile, slope 3/4 not generated, CanPoundTile blacklist) — confirm impact only:
- SlopeTile→PoundTile: affects look (no slopes) — 中 for visuals, low for waterfall triggers (halfBrick still set). Actually PoundTile sets halfBrick which is what triggers waterfalls — equivalent for that purpose. Visual: no sloped edges → terrain looks blockier. 中.
- slope 3/4 (L7656-7662) missing: no half-dome tops — 低/中. It also requires the outer else-if condition `!tile[i,j+1].active()` — the TS skips entirely. 低.
- CanPoundTile blacklist (10/48/137/...): original CanPoundTile excludes certain types (e.g., 10 ashes? 48, 137...). TS uses !framed. If repo tiles map differently, some poundable-in-original tiles skipped or vice versa. 低.

Let me also check what st.isSolid is in TileStore to assess the yOff issue properly. And check callers of draw() to see groundLevel meaning. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:58:50.913Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"isSolid\" ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts | head -20; echo ---; grep -rn \"WaterfallRenderer\\|waterfall.draw\\|\\.draw(\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts -l | head",
 "description": "Find isSolid definition and WaterfallRenderer callers"
}
```


---

## 🤖 Assistant · 2026-08-09T02:58:50.925Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"liquidType\" ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts | head; echo ---; grep -rn \"groundLevel\" ~/Project/GLM/SandboxWorld/game/src/render/*.ts ~/Project/GLM/SandboxWorld/game/src/*.ts 2>/dev/null | head",
 "description": "Check liquidType encoding and groundLevel usage"
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:58:50.950Z

**📎 ToolResult**

```
46:  isSolid(x: number, y: number): boolean {
---
(eval):1: no matches found: --include=*.ts

```


---

## 👤 User(sidechain) · 2026-08-09T02:58:50.952Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:13:  readonly liquidType: Uint8Array; // 0无 1水 2岩浆 3蜂蜜
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:29:    this.liquidType = new Uint8Array(n);
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:125:    if (this.liquid[i] === a && this.liquidType[i] === type) return;
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:127:    this.liquidType[i] = type;
---
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:367:    drawVanillaLiquids(this.ctx, this.atlas, world.store, world.groundLevel, tx0, ty0, tx1, ty1, performance.now(), isBackground);
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:372:      this.waterfalls.draw(this.ctx, this.atlas, world.store, world.groundLevel, now);
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:180:              worldSurface: this.world.groundLevel, worldW: this.world.w },
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:282:                worldSurface: this.world.groundLevel, worldW: this.world.w });
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:288:                worldSurface: this.world.groundLevel, worldW: this.world.w });
~/Project/GLM/SandboxWorld/game/src/render/VanillaLiquidRenderer.ts:27:  st: TileStore, groundLevel: number,
~/Project/GLM/SandboxWorld/game/src/render/VanillaLiquidRenderer.ts:250:      const isSurface = fx[i] === 16 && fy[i] === 0 && y > groundLevel - 40;
~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts:71:  draw(ctx: CanvasRenderingContext2D, atlas: SpriteAtlas | null, st: TileStore, groundLevel: number, nowMs: number) {
~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts:97:          : (st.wall[ci] !== 0 || cy >= groundLevel ? 0.6 : 1.0);

```


---

## 🤖 Assistant · 2026-08-09T02:58:52.113Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts",
 "limit": 20,
 "offset": 40
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:58:52.118Z

**📎 ToolResult**

```
40	  get(x: number, y: number): number { return this.inBounds(x, y) ? this.type[this.idx(x, y)] : 0; }
41	
42	  isActive(x: number, y: number): boolean {
43	    return this.inBounds(x, y) && this.type[this.idx(x, y)] !== 0;
44	  }
45	
46	  isSolid(x: number, y: number): boolean {
47	    if (!this.inBounds(x, y)) return false; // 世界外视为空（边缘自由）
48	    const d = TILE_DEFS[this.type[this.idx(x, y)]];
49	    return !!d && d.solid;
50	  }
51	
52	  isPlatform(x: number, y: number): boolean {
53	    if (!this.inBounds(x, y)) return false;
54	    const d = TILE_DEFS[this.type[this.idx(x, y)]];
55	    return !!d && d.platform;
56	  }
57	
58	  onTileChanged(fn: (x: number, y: number) => void) {
59	    this.listeners.push(fn);

```


---

## 🤖 Assistant · 2026-08-09T02:59:14.256Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have everything. Let me compose the deviation list, ≤50 lines, format:

`偏差 | 文件:位置 | 原版行号 | 影响程度`

Let me list, ordered.

**WaterfallRenderer.ts:**

1. 起点 x 偏移：原版在唇缘格(半砖)上因 `!tile.halfBrick()` 不满足直落分支，走 L476/484 侧移一格(远离液体侧)再下落；TS 直接从唇缘格垂直下落，整柱横向差 1 格 | WaterfallRenderer.ts:108 | WaterfallManager.cs:470-491 | 中
2. 侧移条件不同：原版 `对侧非Solid && 对侧liquid==0`（不查对角下方），且方向由液体位置决定(远离液体)；TS `!solid(x±1,y) && !solid(x±1,y+1)` 且固定先试右 | :109-112 | :476-491 | 中
3. 偏折计数语义：原版 num23 计"方向反转"次数且直落时清零，≥2 时翻转 num26/num14 继续走(不掉头停)；TS 累计每次平移、不清零，≥2 直接 break | :114 | :472,478-490,503-507 | 中(长斜流提前截断)
4. yOff：原版 `SolidTile(below) && !tile.halfBrick() → num11=8`，且 `num13!=0` 时清 0；TS 用 `st.isSolid(cx,cy+1)`（含半砖、无 halfBrick 豁免、无复位）| :101 | :531-534 | 中
5. 断流半砖豁免缺失：原版 `liquid>0 && !halfBrick` 才停；TS `liq>0` 即 break（半砖格有液会提前停）| :106 | :777-778 | 低
6. 扫描窗口：原版左右扩 waterfallDist(100)、上方扩 100、下方 +20；TS 只扩 ±2（视口外起点的长瀑会漏）| :37-38 | :74-81 | 中
7. 断流 blockType 判定：原版仅 blockType==0(完整实心块)断流，slope 1-4 可穿过；TS 忽略 slope(坡面按整块断流)。本仓库 slope 恒 0 故当前无差异 | :92 | :427 | 低
8. 帧速 tick 换算：regular 50ms/帧、slow 117ms/帧 ≈ 原 3/7 tick(60fps)，数值自洽；无偏差(确认)。— 不用报，因为只报差异。但 slow 用 117 vs 116.7 — 微小，不报。

也许报: L124 触发条件中 lOpen/rOpen 检查 `st.slope[li]===0` 但未检查对侧 — actually original checks the same side. Fine.

Also type 判定 lava(): lava() in decompiled = liquid type. OK.

One more: original `num21 = liquid/16` then final draw height 16-num21, and only draws final cell if liquid<=0||halfBrick (L743/750). TS draws crop cell always then breaks. 微小,可并入5。

Also: 透明度 default 分支 `y >= Main.worldSurface` — TS `cy >= groundLevel`。groundLevel = world.groundLevel, presumably worldSurface equivalent. OK.

**HalfBrickPass.ts:**

9. 缺相邻格 type!=136(苔藓)豁免（L7576 外层条件的一部分）| HalfBrickPass.ts:51 | WorldGen.cs:7576 | 低
10. 缺 CanBeClearedDuringGeneration 过滤（不可清除类照砸）| :53 | :7578 | 低
11. 模式 A 的 50% 分支两支都是 poundTile（死代码，等价于必然砸；属已知 SlopeTile→Pound 偏离的实现冗余）| :61-62 | :7586-7589 | 低
12. 悬空支脚第3/4分支缺 else 分支的 SlopeTile(2/1)（80% 走坡面→现在什么都不做/或概率换算后 pound）。Wait — TS: 20% kill, else 25% pound, else nothing. Original: 20% kill, else 20% pound, else 60% SlopeTile. TS: 80%*25% = 20% pound. Equivalent probabilities! Nice — actually TS chance(0.2) kill, then chance(0.25) of remaining 80% → 20% pound. So identical distribution except slope branch (60%) does nothing. Good, so only slope omission — known deviation. Not a new numeric deviation. I can note it as confirmed-equivalent or just include in known deviation impact.
13. 空位补角：缺相邻格 type!=190/48/232 排除、缺 495 特例（贴图来源取侧格而非下格）| :102-110 | :7632-7648 | 低
14. 空位补角下格类型排除 151/274 简化为 !framed | :101 | :7630 | 低(已知风格)
15. 缺 slope 3/4 分支整段(L7656-7662)（已知；且其外层条件 `!tile[i,j+1].active()` 的 else-if 结构在 TS 中不存在）| HalfBrickPass.ts(缺) | :7656-7662 | 低
16. 缺沙类 Tile.SmoothSlope 调用(L7663) | (缺) | :7663-7664 | 低
17. 第二遍缺 type 75/76/137 及左右邻 137 排除 | :122 | :7672 | 低
18. 第二遍缺 slope 回落分支(slope1/2 且侧空 → SlopeTile(0)+PoundTile)——因 slope 恒 0 当前无行为差异 | (缺) | :7679-7688 | 低
19. WaterfallLip 第一遍缺 75/76 类型 10% 概率豁免(L7718) | :150(前) | :7718-7719 | 低
20. WaterfallLip 第二遍缺 type!=48/232 外层排除(L7731) | :157 | :7731 | 低
21. 已知偏离影响确认：SlopeTile→PoundTile — 触发瀑布的 halfBrick 等价(低)，但地表无坡面、轮廓更方块化(中，视觉)；slope 3/4 缺失使圆顶缺失(低)；CanPoundTile 黑名单简化为 !framed，若 TILE_DEFS 与原版 type 映射不同可能多砸/漏砸(低)。

Also check: smooth pass 第一遍中,原版 L7580 的 half/slope guard 要求左右邻 `!halfBrick && slope==0` — TS L55 ✓.

Also: original pass 处理顺序中 L7626 顶部立柱删除在 `if(SolidTile(i,j+1))` 之外但在 half guard 之内 — TS ✓ matches.

Also worth checking: TS poundTile toggles half (`st.half[i] ? 0 : 1`), original PoundTile at gen — sets halfBrick=true (probably doesn't toggle; pounding an already-half tile no-op or re-pounds). Toggle could un-pound a half brick if called on an already-half tile! In smooth pass, the guard `!half[i-1,j] && !half[i+1,j]` only checks neighbors, not (i,j) itself. So if (i,j) is already halfBrick, original PoundTile — let me check original PoundTile L49198. Let me read quickly. Actually the gen PoundTile:

Let me check WorldGen.cs:49198 region to be accurate about toggle vs set.
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:59:14.297Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 49120,49235p ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "description": "Read CanPoundTile/PoundTile/SlopeTile source"
}
```


---

## 👤 User(sidechain) · 2026-08-09T02:59:14.327Z

**📎 ToolResult**

```
    }

    public static bool CanPoundTile(int x, int y)
    {
      if (Main.tile[x, y] == null)
        Main.tile[x, y] = new Tile();
      if (Main.tile[x, y - 1] == null)
        Main.tile[x, y - 1] = new Tile();
      if (Main.tile[x, y + 1] == null)
        Main.tile[x, y + 1] = new Tile();
      switch (Main.tile[x, y].type)
      {
        case 10:
        case 48:
        case 137:
        case 138:
        case 232:
        case 380:
        case 387:
        case 388:
        case 476:
        case 484:
          return false;
        default:
          if (WorldGen.gen && (Main.tile[x, y].type == (ushort) 190 || Main.tile[x, y].type == (ushort) 30))
            return false;
          if (Main.tile[x, y - 1].active())
          {
            switch (Main.tile[x, y - 1].type)
            {
              case 21:
              case 26:
              case 77:
              case 88:
              case 235:
              case 237:
              case 441:
              case 467:
              case 468:
              case 470:
              case 475:
              case 488:
              case 597:
                return false;
            }
          }
          return WorldGen.CanKillTile(x, y);
      }
    }

    public static bool SlopeTile(int i, int j, int slope = 0, bool noEffects = false)
    {
      if (!WorldGen.CanPoundTile(i, j))
        return false;
      Main.tile[i, j].halfBrick(false);
      Main.tile[i, j].slope((byte) slope);
      if (!WorldGen.gen)
      {
        if (!noEffects)
          WorldGen.KillTile(i, j, true, true, false);
        SoundEngine.PlaySound(0, i * 16, j * 16, 1, 1f, 0.0f);
        WorldGen.SquareTileFrame(i, j, true);
        if (Main.tile[i, j].slope() == (byte) 0)
        {
          Microsoft.Xna.Framework.Rectangle rectangle = new Microsoft.Xna.Framework.Rectangle(i * 16, j * 16, 16, 16);
          for (int index = 0; index < (int) byte.MaxValue; ++index)
          {
            if (Main.player[index].active && !Main.player[index].dead && rectangle.Intersects(new Microsoft.Xna.Framework.Rectangle((int) Main.player[index].position.X, (int) Main.player[index].position.Y, Main.player[index].width, Main.player[index].height)))
            {
              Main.player[index].gfxOffY += Main.player[index].position.Y + (float) Main.player[index].height - (float) rectangle.Y;
              Main.player[index].position.Y = (float) (rectangle.Y - Main.player[index].height);
            }
          }
        }
      }
      return true;
    }

    public static bool PoundTile(int i, int j)
    {
      if (!WorldGen.CanPoundTile(i, j))
        return false;
      if (!Main.tile[i, j].halfBrick())
        Main.tile[i, j].halfBrick(true);
      else
        Main.tile[i, j].halfBrick(false);
      if (!WorldGen.gen)
      {
        WorldGen.KillTile(i, j, true, true, false);
        SoundEngine.PlaySound(0, i * 16, j * 16, 1, 1f, 0.0f);
        WorldGen.SquareTileFrame(i, j, true);
        if (!Main.tile[i, j].halfBrick())
        {
          Microsoft.Xna.Framework.Rectangle rectangle = new Microsoft.Xna.Framework.Rectangle(i * 16, j * 16, 16, 16);
          for (int index = 0; index < (int) byte.MaxValue; ++index)
          {
            if (Main.player[index].active && !Main.player[index].dead && rectangle.Intersects(new Microsoft.Xna.Framework.Rectangle((int) Main.player[index].position.X, (int) Main.player[index].position.Y, Main.player[index].width, Main.player[index].height)))
            {
              Main.player[index].gfxOffY += Main.player[index].position.Y + (float) Main.player[index].height - (float) rectangle.Y;
              Main.player[index].position.Y = (float) (rectangle.Y - Main.player[index].height);
            }
          }
        }
      }
      return true;
    }

    public static void PoundPlatform(int x, int y)
    {
      if (Main.tile[x, y].halfBrick())
      {
        WorldGen.PoundTile(x, y);
        if (Main.netMode != 1)
          return;
        NetMessage.SendData(17, -1, -1, (NetworkText) null, 7, (float) x, (float) y, 1f, 0, 0, 0);
      }

```


---

## 🤖 Assistant · 2026-08-09T02:59:36.119Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
PoundTile does toggle (same as TS). And CanPoundTile also checks `tile[x,y-1].active()` with a blacklist (leeches/pressure plates? 21 dart trap etc.) and `WorldGen.CanKillTile(x,y)`. TS canPoundTile misses the above-tile blacklist (21/26/77/88/235/...) and CanKillTile. 低.

Also original SlopeTile(2) does `halfBrick(false)` + slope(2) — TS replacing with poundTile sets half, which changes which cells have halfBrick. Known deviation.

Now compose final answer, ≤50 lines, one line per deviation. Include file:位置 with absolute paths? "share file paths (always absolute)". The format says `文件:位置` — I'll use absolute path once in a header maybe, or short names. The instructions say absolute paths in final response. To keep lines short I'll use absolute path prefix in each line but that's long. Maybe define abbreviations at top: WR = /Users/.../WaterfallRenderer.ts, HB = .../HalfBrickPass.ts. That's acceptable and keeps lines readable. But instruction says always absolute paths — I'll list the two absolute paths in a legend and use WR/HB. Hmm, risk. I'll use full paths in the legend and short refs in lines; that's a reasonable compromise... Actually to be safe I'll put absolute paths in each deviation line but abbreviated with the two names after a legend. I think legend approach is fine.

Line count: aim ~25 lines.

Let me finalize entries with impact levels.

WaterfallRenderer:
1. 直落分支缺 `!tile.halfBrick()` 门 → 唇缘格直接下落；原版在半砖上先走 L476/484 侧移一格(远离液体侧)再落，TS 整柱横移 1 格偏差 | WR.ts:106-108 | 470-491 | 中
2. 侧移条件与方向：原版看对侧 `!SolidTile && liquid==0`(不查对角下格)，方向=远离液体；TS 用 `!solid(x±1,y)&&!solid(x±1,y+1)` 且固定先试右 | :109-112 | 476-491 | 中
3. 偏折计数：原版 num23 只在方向反转时 +1、直落清零、≥2 时翻转方向继续；TS 每次平移累计且不清零、≥2 直接 break → 斜向长流被提前截断 | :114 | 472/478-507 | 中
4. yOff=8：原版要求 `SolidTile(below) && !tile.halfBrick()`，且下一格非落地时经 num13 复位 0；TS 用 isSolid(含半砖、无 half 豁免、永不复位) | :101 | 531-534 | 中
5. 溶池断流：原版 `liquid>0 && !halfBrick` 才停；TS `liq>0` 即停，半砖格带液提前断 | :106 | 777-778 | 低
6. 扫描窗口 ±2 vs 原版左右/上各 +waterfallDist(100)、下 +20：视口上方起点的长瀑漏检 | :37-38 | 74-81 | 中
7. 断流判定忽略 slope：原版 blockType==0 才断(slope1-4 穿过)；TS 坡面按整块断流——本仓库 slope 恒 0，暂无差异 | :90-93 | 427 | 低
8. 尾部衰减的 num24 动态缩短(撞 Water Fountain/Lavafall 189/196 时降为 ~40)未移植 | — | 788-789 | 低
9. 顶部注释 L4-5 仍写"适配为倾泻点：液量≥160…"，与实际半砖实现矛盾(文档漂移) | :4-5 | 100-131 | 低

Also maybe: 水 style(Style 参数/水样式选图)固定 0 — low; skip or include. I'll include as 低? Keep ≤. I'll include since it's a real diff: 原版水瀑布贴图随水样式 Style 变化，TS 固定 Waterfall_0 | WR.ts:22,82 | 239-241/353 | 低.

HalfBrick:
10. 缺左右邻 type!=136(苔藓)豁免 | HB.ts:51 | 7576 | 低
11. 缺 CanBeClearedDuringGeneration 过滤(不可清除方块照砸/照删) | :53 | 7578 | 低
12. 模式A 50% 分支两支同为 poundTile(死代码；SlopeTile(2) 分支丢失，属已知偏离) | :61-62 | 7586-7589 | 低
13. 空位补角缺邻格 type!=190/48/232 排除与 495 特例(495 时贴图取侧格而非下格) | :102-110 | 7632-7648 | 低
14. 空位补角下格 151/274 排除近似为 !framed | :101 | 7630 | 低
15. 缺 slope3/4 分支整段(L7656-7662,外层 else-if 结构 `!tile[i,j+1].active()`)——已知，圆顶缺失 | 缺 | 7656-7662 | 低
16. 缺沙类 Tile.SmoothSlope | 缺 | 7663-7664 | 低
17. 第二遍缺 type 75/76 与左右邻 137 排除 | :117-122 | 7672 | 低
18. 第二遍缺 slope 回落分支(slope1/2 侧空→SlopeTile(0)+PoundTile)；slope 恒 0 故暂无差异 | 缺 | 7679-7688 | 低
19. WaterfallLip 第一遍缺 75/76 的 10% 概率豁免(原版此类仅 1/10 砸) | :139-150 | 7718-7719 | 低
20. WaterfallLip 第二遍缺外层 type!=48/232 排除 | :157 | 7731 | 低
21. canPoundTile 缺"上格有物(21/26/77/88/…)不砸"与 CanKillTile 检查(已知黑名单简化的具体漏项) | :24-29 | 49122-49164 | 低
22. PoundTile toggle 语义一致(half 取反) | — | 49198-49204 | 无偏差 — skip (only report diffs).
23. 已知偏离影响确认: SlopeTile→Pound: 瀑布触发(halfBrick)等价/低，视觉上地表全无坡面、轮廓方块化/中。

Also one numeric check worth noting: 悬空支脚 3/4 分支概率 TS 20% kill / 20% pound / 60% 无操作 = 原版分布(20/20/60 SlopeTile)，仅 Slope 分支改为无操作 — 已知偏离内,确认无额外概率漂移。I can add as a confirmation line (不算偏差) — maybe mention in a short note. I'll add one line noting it as 无概率漂移.

That's ~21 lines + legend. Good. Note user line refs were offset (~-34): user said L7580-7668 for 主模式 but actual is 7580-7628 etc. I should note the actual line numbers I used. I'll add a brief note that the user's quoted line numbers are offset by ~+4 to +34 vs the decompiled file, and I report actual decompiled lines.

Let me double check offsets: user said "L100-130" for findWaterfalls — actual 100-131 ✓. "L421-507" ✓ actual 421-507 ✓. "L531-532" ✓. "L538-551" ✓. "L171-209" ✓. "L427" ✓ "L777-778" ✓. WaterfallManager refs all match. WorldGen: user said "Smooth World L7568-7696" — actual pass 7564-7695 ✓ close. 主模式 A/B "L7580-7668" — actual 7580-7628. 悬空支脚 "L7634-7668" → actual 7600-7624. 空位补角 "L7669-7695" → actual 7630-7653. 第二遍斜坡 "L7677-7694" → actual 7668-7689. Waterfalls pass "L7697-7743" → actual 7696-7741 ✓. So the user's WorldGen sub-refs are shifted +30 to +54. I'll note this once.

Good. Write the final answer.
```

</details>


---

## 🤖 Assistant · 2026-08-09T02:59:50.649Z · glm-x-preview-260804

````
审计完成。说明：**WaterfallManager.cs 的行号与你给的一致**；**WorldGen.cs 的子区间行号整体偏移 +30~54**（实际：主模式 A/B/孤立凸起 7580-7628、悬空支脚削除 7600-7624、空位补角 7630-7653、第二遍斜坡 7668-7689、Waterfalls pass 7696-7741），下表按反编译实际行号报告。

文件缩写：
- WR = ~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts
- HB = ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts

## 一、WaterfallRenderer.ts

```
偏差 | 文件:位置 | 原版行号 | 影响
直落分支缺 !tile.halfBrick() 门：原版在唇缘半砖格上不满足 L470 直落条件，先经 L476/484 向空侧平移 1 格再落；TS 直接从唇缘格垂直下落，整条流柱横向偏 1 格 | WR.ts:106-108 | WaterfallManager.cs:470-491 | 中
侧移判定不同：原版仅看目标侧 !SolidTile && liquid==0（不查对角下格），方向=远离液体侧；TS 用 !solid(x±1,y)&&!solid(x±1,y+1) 且固定先试右侧 | WR.ts:109-112 | :476-491 | 中
偏折计数语义不同：原版 num23 仅方向反转时+1、直落时清零、≥2 时翻转 num26 继续走；TS 每次平移累计且不清零、≥2 直接 break → 斜向长流被提前截断 | WR.ts:114 | :472,478-507 | 中
yOff=8 判定偏离（你已标记）：原版 SolidTile(below) && !tile.halfBrick()，且下一格非落地时经 num13!=0 复位 0；TS 用 st.isSolid（含半砖、无 half 豁免、永不复位），半砖唇缘格会被错误上移 | WR.ts:101（对比 TileStore.ts:46-50）| :531-534 | 中
溶池断流缺半砖豁免：原版 liquid>0 && !halfBrick 才停；TS liq>0 即 break，半砖格带液会提前断流 | WR.ts:106 | :777-778 | 低
扫描窗口过小：原版左右/上方各扩 waterfallDist(100)、下方 +20；TS 仅 ±2，视口外起点的长瀑漏检（原版 L74-81）| WR.ts:37-38 | :74-81 | 中
断流判定忽略 slope：原版仅 blockType==0（完整实心块）断流，slope 1-4 可穿过；TS 把坡面当整块断流——本仓库 slope 恒 0，当前无实际差异 | WR.ts:90-93 | :427 | 低
尾部衰减基准 num24 可动态缩短（邻格 189/196 喷泉时降为约 40）未移植，TS 固定 100 | WR.ts:98 | :788-789 | 低
水样式选图未移植：原版 type 0 时 index2=Style（随世界水样式换贴图），TS 固定 Waterfall_0 | WR.ts:22,82 | :239-241,353 | 低
文件头注释 L4-5 仍写"触发条件适配为倾泻点：液量≥160 的格子"，与实际半砖实现矛盾（文档漂移） | WR.ts:4-5 | :100-131 | 低
```

核对一致、无需改动：触发四条件（halfBrick + 上格 liquid<16||SolidTile + 一侧>160 对侧空 + slope==0，L102-127）、类型判定顺序（上/右/左，L126-127）、liquidType 编码（TileStore.ts:13：2岩浆 3蜂蜜）、帧速 50ms/117ms ≈ 3/7 tick@60fps、透明度三档与末 10 格衰减、crop=liquid/16。

## 二、HalfBrickPass.ts

```
偏差 | 文件:位置 | 原版行号 | 影响
缺左右邻格 type!=136（苔藓）豁免，苔藓旁凸起照砸 | HB.ts:51 | WorldGen.cs:7576 | 低
缺 TileID.Sets.CanBeClearedDuringGeneration 过滤，不可清除类方块也会被砸/删 | HB.ts:53 | :7578 | 低
模式 A 的 50% 分支两支都是 poundTile（死代码；SlopeTile(2) 分支丢失，属已知偏离的冗余写法） | HB.ts:61-62 | :7586-7589 | 低
空位补角缺邻格 type!=190/48/232 排除，以及 495 特例（495 时贴图来源取侧格而非下格） | HB.ts:102-110 | :7632-7648 | 低
空位补角的下格 151/274 排除被近似为 !framed | HB.ts:101 | :7630 | 低
slope 3/4 分支整段缺失（含其外层 else-if 结构 !tile[i,j+1].active()）——已知偏离，地表圆顶缺失 | HB.ts（缺）| :7656-7662 | 低
缺沙类的 Tile.SmoothSlope 调用 | HB.ts（缺）| :7663-7664 | 低
第二遍缺 type 75/76/137 及左右邻 137 的排除 | HB.ts:117-122 | :7672 | 低
第二遍缺 slope 回落分支（slope1/2 且侧空 → SlopeTile(0)+PoundTile）；slope 恒 0 故暂无行为差异 | HB.ts（缺）| :7679-7688 | 低
WaterfallLip 第一遍缺 75/76 类型豁免：原版仅 1/10 概率砸，TS 必砸 | HB.ts:139-150 | :7718-7719 | 低
WaterfallLip 第二遍缺外层 type!=48/232 排除 | HB.ts:157 | :7731 | 低
canPoundTile 缺"上格挂有物（21/26/77/88/235/…）不砸"与 CanKillTile 检查（已知黑名单简化的具体漏项） | HB.ts:24-29 | :49122-49164 | 低
```

核对一致：模式 A/B/孤立凸起五条件全对（7580-7599）、悬空支脚 4 分支全对且 20%/25% 复合概率与原版 Next(5)/Next(5) 分布等价（仅 Slope 分支改为无操作）、顶部单格立柱删除（7626-7627）、第一遍 SolidTile/左右空/侧液/上下 8-20 格防串判定（7706-7717）、第二遍左右对称扩展（7733-7736）、PoundTile 的 half 取反语义（49198-49204）。

已知偏离影响确认：
- SlopeTile→PoundTile：瀑布触发的 halfBrick 等价（低），但地表完全没有坡面，轮廓比原版更方块化（中，纯视觉）。
- slope 3/4 未生成：仅损失圆顶细节（低）。
- CanPoundTile 黑名单简化为 !framed：若 TILE_DEFS 与原版 type 编号映射有出入，可能多砸/漏砸个别类型（低）。

优先级建议：WaterfallRenderer 的三项"中"里，#1（起点横移 1 格）与 #4（yOff 半砖豁免）直接决定瀑布贴图与崖壁的对位，建议先核。
````
