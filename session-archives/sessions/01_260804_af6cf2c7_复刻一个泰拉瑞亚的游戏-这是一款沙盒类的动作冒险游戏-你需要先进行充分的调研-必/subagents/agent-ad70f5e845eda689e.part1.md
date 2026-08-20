# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-07T05:46:06.582Z

```
Explore ~/Project/GLM/SandboxWorld/game — the wall (background wall) rendering system of this Terraria clone. Report:

1. `src/render/WallTiler.ts` — full logic: how it analyzes wall sheet patterns, how it picks frames for each wall cell (neighbor masks? pattern matching?), any caching. Include key method names, mask conventions, and how it handles corners/edges.
2. `src/render/ChunkCache.ts` — the wall rendering pass (first pass?): how WallTiler is invoked, what wall id/source images are used (Maples wall sheets? '地形/Wall_1.png' etc.), draw order relative to tiles.
3. `src/data/tiles.ts` — WALL_DEFS / WALL_BY_KEY / W interface (wall types 0-3?), wall properties (opacity, mapColor).
4. `src/wld/WldImport.ts` — WALL_MAP: which wld wall ids are mapped, what happens to unmapped wall ids (fallback 'stone_wall'?), count of entries.
5. `src/wld/WldParser.ts` — how wall ids are read (u8 + u16 extension bit?).
6. Are vanilla wall textures used anywhere? Check vanilla.json for 'walls' section (scripts/vanilla-atlas.mjs outputs walls count=0 — confirm), and VANILLA_MISC.
7. Any rendering of walls with lighting/darkening (shade function usage in ChunkCache wall pass).

Report file paths + line numbers, the exact neighbor mask bit order used by WallTiler, and how a wall cell's frame is chosen for interior/edge/corner cases. Medium thoroughness.
```

---

## 📎 Attachment · skill_listing · 2026-08-07T05:46:06.585Z

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

## 🤖 Assistant · 2026-08-07T05:46:09.972Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants me to explore the wall rendering system. Let me start by reading the key files in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:46:10.098Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/WallTiler.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:10.104Z

**📎 ToolResult**

```
1	// 数据驱动的墙体自动贴合器。
2	// Maples 的 RuleTile 规则表把内墙变体错误映射到 1/4 小块（覆盖率 25%），
3	// 因此不使用其规则，而是分析每张墙精灵的 alpha 边缘轮廓：
4	//   按四侧（上右下左）是否"敞开"分类，运行时按 2×2 块的敞开方向选变体。
5	import type { SpriteAtlas, DrawRect } from '../assets/SpriteAtlas';
6	import { hash2 } from '../core/rng';
7	
8	interface SideProfile { open: [boolean, boolean, boolean, boolean]; } // 上 右 下 左
9	
10	export class WallTiler {
11	  private groups = new Map<string, Array<{ file: string; name: string; rect: DrawRect }>>();
12	
13	  constructor(private atlas: SpriteAtlas, private files: string[]) {}
14	
15	  /** 启动期调用一次：分析精灵轮廓（需图片已解码，走 canvas 拷贝） */
16	  analyze() {
17	    for (const file of this.files) {
18	      const entry = this.atlas.data.files[file];
19	      const img = this.atlas.images.get(file);
20	      if (!entry || !img) continue;
21	      const c = document.createElement('canvas');
22	      c.width = img.width; c.height = img.height;
23	      const ctx = c.getContext('2d')!;
24	      ctx.drawImage(img, 0, 0);
25	      for (const s of entry.sprites) {
26	        const rect = this.atlas.rect(file, s.name);
27	        if (!rect) continue;
28	        const d = ctx.getImageData(rect.sx, rect.sy, rect.sw, rect.sh).data;
29	        const w = rect.sw, h = rect.sh;
30	        const bandOpaque = (x0: number, y0: number, bw: number, bh: number) => {
31	          let n = 0, t = 0;
32	          for (let y = y0; y < y0 + bh; y++) {
33	            for (let x = x0; x < x0 + bw; x++) {
34	              t++;
35	              if (d[(y * w + x) * 4 + 3] > 40) n++;
36	            }
37	          }
38	          return t ? n / t : 0;
39	        };
40	        const coverage = bandOpaque(0, 0, w, h);
41	        if (coverage < 0.15) continue; // 空块/噪声
42	        // 内墙变体（覆盖率 ≥75% 的完整块）强制归入 '0000'，
43	        // 否则半块边缘件会污染内墙组（此前"看起来没变"的根因）
44	        if (coverage >= 0.75) {
45	          if (!this.groups.has('0000')) this.groups.set('0000', []);
46	          this.groups.get('0000')!.push({ file, name: s.name, rect });
47	          continue;
48	        }
49	        const BAND = Math.max(2, Math.floor(Math.min(w, h) / 8));
50	        const innerOpaque = bandOpaque(BAND, BAND, w - BAND * 2, h - BAND * 2);
51	        if (innerOpaque < 0.4) continue;
52	        // 相对比较：某侧带明显低于该精灵最实一侧 → 该侧敞开（变体向此侧收窄）
53	        const bands = [
54	          bandOpaque(0, 0, w, BAND),          // 上
55	          bandOpaque(w - BAND, 0, BAND, h),   // 右
56	          bandOpaque(0, h - BAND, w, BAND),   // 下
57	          bandOpaque(0, 0, BAND, h),          // 左
58	        ];
59	        const maxBand = Math.max(...bands);
60	        const open: [boolean, boolean, boolean, boolean] = [
61	          bands[0] < maxBand * 0.6,
62	          bands[1] < maxBand * 0.6,
63	          bands[2] < maxBand * 0.6,
64	          bands[3] < maxBand * 0.6,
65	        ];
66	        // 低于内墙阈值的件必是边缘/角块：若四侧都判封闭，强制最弱一侧敞开，
67	        // 防止半块件混入内墙组
68	        if (!open[0] && !open[1] && !open[2] && !open[3]) {
69	          let minIdx = 0;
70	          for (let k = 1; k < 4; k++) if (bands[k] < bands[minIdx]) minIdx = k;
71	          open[minIdx] = true;
72	        }
73	        const key = open.map((o) => (o ? 1 : 0)).join('');
74	        if (!this.groups.has(key)) this.groups.set(key, []);
75	        this.groups.get(key)!.push({ file, name: s.name, rect });
76	      }
77	    }
78	  }
79	
80	  /**
81	   * 按 2×2 块的敞开方向选精灵。
82	   * open: [上右下左] 该侧是否有同类墙（true=有墙=封闭）
83	   */
84	  pick(closed: [boolean, boolean, boolean, boolean], x: number, y: number): DrawRect | null {
85	    // 需要的 key：封闭侧为 0（不敞开），敞开侧为 1
86	    const want = closed.map((c) => (c ? 0 : 1)).join('');
87	    let list = this.groups.get(want);
88	    if (!list || !list.length) {
89	      // 逐侧放宽：找不到精确组合时退回内墙
90	      list = this.groups.get('0000');
91	    }
92	    if (!list || !list.length) return null;
93	    const pick = list[Math.floor(hash2(x, y, 131) * list.length) % list.length];
94	    return pick.rect;
95	  }
96	
97	  // ---- 梅花格（骰子5）连续图案 ----
98	  // 原版机制：砖块双层对角交叠 —— A 层平铺，B 层错开半个周期叠上，
99	  // 圆角/缺口互相咬合形成双轴交错的梅花格。合成 64×64 可平铺图案后按世界坐标连续取样。
100	  patterns: HTMLCanvasElement[] = [];
101	
102	  buildPatterns() {
103	    const interior = this.groups.get('0000') ?? [];
104	    for (const item of interior) {
105	      const c = document.createElement('canvas');
106	      c.width = 64; c.height = 64;
107	      const ctx = c.getContext('2d')!;
108	      ctx.imageSmoothingEnabled = false;
109	      const r = item.rect;
110	      // A 层：64×64 四角平铺（完整覆盖），随后把整幅透明像素用自身土色填实
111	      // —— 完全封闭的内墙不再有砖缝漏光
112	      for (const [ox, oy] of [[0, 0], [32, 0], [0, 32], [32, 32]]) {
113	        ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, ox, oy, 32, 32);
114	      }
115	      {
116	        const img = ctx.getImageData(0, 0, 64, 64);
117	        const d = img.data;
118	        // 采样不透明像素平均色
119	        let sr = 0, sg = 0, sb = 0, n = 0;
120	        for (let i = 0; i < d.length; i += 4) {
121	          if (d[i + 3] > 40) { sr += d[i]; sg += d[i + 1]; sb += d[i + 2]; n++; }
122	        }
123	        if (n > 0) {
124	          sr = Math.round(sr / n); sg = Math.round(sg / n); sb = Math.round(sb / n);
125	          for (let i = 0; i < d.length; i += 4) {
126	            if (d[i + 3] <= 40) {
127	              const f = 0.92 + hash2(i >> 2, 9, 17) * 0.16;
128	              d[i] = Math.min(255, sr * f);
129	              d[i + 1] = Math.min(255, sg * f);
130	              d[i + 2] = Math.min(255, sb * f);
131	              d[i + 3] = 255;
132	            }
133	          }
134	          ctx.putImageData(img, 0, 0);
135	        }
136	      }
137	      // B 层：对角错开半周期（16px）叠上（含 -64 环绕保证无缝）。
138	      // 低透明度（35%）弱化梅花感 —— 整体读作一面连续的墙，
139	      // 只有隐约的交错纹理，避免"一大格一大格"的突兀中心块
140	      ctx.globalAlpha = 0.35;
141	      for (const [bx, by] of [[16, 16], [48, 16], [16, 48], [48, 48]]) {
142	        for (const [wx, wy] of [[0, 0], [-64, 0], [0, -64], [-64, -64]]) {
143	          ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, bx + wx, by + wy, 32, 32);
144	        }
145	      }
146	      ctx.globalAlpha = 1;
147	      this.patterns.push(c);
148	    }
149	  }
150	
151	  /** 内墙连续取样：按世界坐标从 64×64 图案取 16×16 */
152	  patternSample(x: number, y: number): { canvas: HTMLCanvasElement; sx: number; sy: number } | null {
153	    if (!this.patterns.length) return null;
154	    // 变体按 4×4 tile 超格 hash
155	    const supX = Math.floor(x / 4), supY = Math.floor(y / 4);
156	    const canvas = this.patterns[Math.floor(hash2(supX, supY, 313) * this.patterns.length) % this.patterns.length];
157	    return { canvas, sx: (x * 16) % 64, sy: (y * 16) % 64 };
158	  }
159	}
160	

```


---

## 🤖 Assistant · 2026-08-07T05:46:10.236Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/data/tiles.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:10.407Z

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
16	  drop?: string;         // 破坏掉落 item key（缺省掉同名 key）
17	  blend: boolean;        // 是否参与同类边缘融合
18	  attach?: 'ground' | 'wall'; // 装饰物附着需求
19	  w?: number; h?: number;     // framed 物体占格数
20	  vanilla?: {                 // 原版素材渲染（terraria-assets + TEdit 数据）
21	    sheet: number;            // Tiles_N 表 id
22	    frame: 'auto' | 'style';  // auto=1x1 实心块现场 8 向 framing；style=多格家具用显式 18px 帧偏移
23	    fw?: number; fh?: number; // style 类的占格数（TEdit frameSize）
24	  };
25	}
26	
27	export const T = {
28	  EMPTY: 0, DIRT: 1, STONE: 2, GRASS: 3,
29	  ORE_COPPER: 4, ORE_IRON: 5, ORE_SILVER: 6, ORE_GOLD: 7,
30	  TREE: 8, LEAVES: 9, WOOD: 10, PLATFORM: 11,
31	  TORCH: 12, WORKBENCH: 13, FURNACE: 14, ANVIL: 15,
32	  CHEST: 16, DOOR_CLOSED: 17, DOOR_OPEN: 18,
33	  MUSHROOM: 19, FLOWER: 20, TALLGRASS: 21, SAND: 22, SNOW: 23,
34	  SAPLING: 24, ASH: 25,
35	} as const;
36	
37	export const TILE_DEFS: TileDef[] = [];
38	function def(d: Partial<TileDef> & { key: string }): number {
39	  const id = TILE_DEFS.length;
40	  TILE_DEFS.push({
41	    name: d.key, solid: false, platform: false, decor: false, framed: false,
42	    opacity: 0, pick: -1, axe: -1, mapColor: '#000', blend: false, ...d, id,
43	  } as TileDef);
44	  return id;
45	}
46	// 保证 id 与 T 常量一致（按顺序注册）
47	def({ key: 'empty', name: '空气' });
48	def({ key: 'dirt', name: '泥土', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: 'dirt_block' });
49	def({ key: 'stone', name: '石块', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: 'stone_block' });
50	def({ key: 'grass', name: '草块', solid: true, opacity: 1, pick: 0, mapColor: '#1CD85E', blend: true, drop: 'dirt_block' });
51	def({ key: 'ore_copper', name: '铜矿', solid: true, opacity: 1, pick: 0, mapColor: '#964316', blend: false, drop: 'copper_ore', vanilla: { sheet: 7, frame: 'auto' } });
52	def({ key: 'ore_iron', name: '铁矿', solid: true, opacity: 1, pick: 0, mapColor: '#8C6A56', blend: false, drop: 'iron_ore' });
53	def({ key: 'ore_silver', name: '银矿', solid: true, opacity: 1, pick: 20, mapColor: '#B9C2C3', blend: false, drop: 'silver_ore', vanilla: { sheet: 9, frame: 'auto' } });
54	def({ key: 'ore_gold', name: '金矿', solid: true, opacity: 1, pick: 40, mapColor: '#B9A417', blend: false, drop: 'gold_ore', vanilla: { sheet: 8, frame: 'auto' } });
55	def({ key: 'tree', name: '树干', solid: false, framed: true, opacity: 0.1, axe: 0, mapColor: '#6B4A2B', drop: 'wood' });
56	def({ key: 'leaves', name: '树叶', decor: true, framed: true, opacity: 0.05, pick: 0, axe: 0, mapColor: '#2E8B3D', drop: null as unknown as string });
57	def({ key: 'wood', name: '木材块', solid: true, opacity: 1, pick: 0, mapColor: '#A97D4E', blend: true, drop: 'wood', vanilla: { sheet: 30, frame: 'auto' } });
58	def({ key: 'platform', name: '木平台', platform: true, opacity: 0.15, pick: 0, axe: 0, mapColor: '#B0885A', drop: 'platform', vanilla: { sheet: 19, frame: 'style', fw: 1, fh: 1 } });
59	def({ key: 'torch', name: '火把', decor: true, framed: true, opacity: 0, pick: 0, light: [255, 225, 150], mapColor: '#FDDD03', drop: 'torch', vanilla: { sheet: 4, frame: 'style', fw: 1, fh: 1 } });
60	// 注：火把光值见下（更亮版本）
61	def({ key: 'workbench', name: '工作台', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#A97D4E', drop: 'workbench', vanilla: { sheet: 18, frame: 'style', fw: 2, fh: 1 } });
62	def({ key: 'furnace', name: '熔炉', solid: true, framed: true, opacity: 1, pick: 0, w: 3, h: 2, light: [255, 140, 70], mapColor: '#5A5A5A', drop: 'furnace', vanilla: { sheet: 17, frame: 'style', fw: 3, fh: 2 } });
63	def({ key: 'anvil', name: '铁砧', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#6E6E78', drop: 'anvil', vanilla: { sheet: 16, frame: 'style', fw: 2, fh: 1 } });
64	def({ key: 'chest', name: '宝箱', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#D4A017', drop: 'chest', vanilla: { sheet: 21, frame: 'style', fw: 2, fh: 2 } });
65	def({ key: 'door_closed', name: '门', solid: true, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#A97D4E', drop: 'door', vanilla: { sheet: 10, frame: 'style', fw: 1, fh: 3 } });
66	def({ key: 'door_open', name: '门(开)', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#A97D4E', drop: 'door', vanilla: { sheet: 11, frame: 'style', fw: 2, fh: 3 } });
67	def({ key: 'mushroom', name: '蘑菇', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#C36927', drop: 'mushroom_item' });
68	def({ key: 'flower', name: '花', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#D0699E', drop: null as unknown as string });
69	def({ key: 'tallgrass', name: '草丛', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#1E9648', drop: 'acorn' });
70	def({ key: 'sand', name: '沙块', solid: true, opacity: 1, pick: 0, mapColor: '#FFDA38', blend: true, drop: 'sand_block', vanilla: { sheet: 53, frame: 'auto' } });
71	def({ key: 'snow', name: '雪块', solid: true, opacity: 1, pick: 0, mapColor: '#E8F0F4', blend: true, drop: 'snow_block' });
72	def({ key: 'acorn_sapling', name: '树苗', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#6B4A2B', drop: 'acorn' });
73	def({ key: 'ash', name: '灰烬块', solid: true, opacity: 1, pick: 0, mapColor: '#44444C', blend: true, drop: 'stone_block', vanilla: { sheet: 57, frame: 'auto' } });
74	
75	// ===================== 原版素材图块（terraria-assets + TEdit 数据） =====================
76	// 4a：矿石 / 宝石 / 冰雪 / 沙漠 / 基础方块（1x1 实心，frame:'auto' 8 向贴合）
77	// mapColor/pick 取自 TEdit tiles.json；sheet = 原版 Tiles_N 表 id
78	
79	// ---- 矿石（含替代矿与困难模式矿，后者先只做美术） ----
80	def({ key: 'ore_tin', name: '锡矿', solid: true, opacity: 1, pick: 0, mapColor: '#817D5D', drop: 'tin_ore', vanilla: { sheet: 166, frame: 'auto' } });
81	def({ key: 'ore_lead', name: '铅矿', solid: true, opacity: 1, pick: 0, mapColor: '#3E5272', drop: 'lead_ore', vanilla: { sheet: 167, frame: 'auto' } });
82	def({ key: 'ore_tungsten', name: '钨矿', solid: true, opacity: 1, pick: 20, mapColor: '#849D7F', drop: 'tungsten_ore', vanilla: { sheet: 168, frame: 'auto' } });
83	def({ key: 'ore_platinum', name: '铂金矿', solid: true, opacity: 1, pick: 40, mapColor: '#98ABC6', drop: 'platinum_ore', vanilla: { sheet: 169, frame: 'auto' } });
84	def({ key: 'ore_demonite', name: '魔矿', solid: true, opacity: 1, pick: 55, mapColor: '#625FA7', drop: 'demonite_ore', vanilla: { sheet: 22, frame: 'auto' } });
85	def({ key: 'ore_meteorite', name: '陨石', solid: true, opacity: 1, pick: 50, mapColor: '#685654', drop: 'meteorite', vanilla: { sheet: 37, frame: 'auto' } });
86	def({ key: 'ore_hellstone', name: '狱石', solid: true, opacity: 1, pick: 70, mapColor: '#8E4242', drop: 'hellstone', light: [255, 90, 40], vanilla: { sheet: 58, frame: 'auto' } });
87	def({ key: 'ore_crimtane', name: '猩红矿', solid: true, opacity: 1, pick: 65, mapColor: '#7D3741', drop: 'crimtane_ore', vanilla: { sheet: 204, frame: 'auto' } });
88	def({ key: 'ore_cobalt', name: '钴矿', solid: true, opacity: 1, pick: 65, mapColor: '#0B508F', drop: 'cobalt_ore', vanilla: { sheet: 107, frame: 'auto' } });
89	def({ key: 'ore_mythril', name: '秘银矿', solid: true, opacity: 1, pick: 65, mapColor: '#5BA9A9', drop: 'mythril_ore', vanilla: { sheet: 108, frame: 'auto' } });
90	def({ key: 'ore_adamantite', name: '精金矿', solid: true, opacity: 1, pick: 65, mapColor: '#801A34', drop: 'adamantite_ore', vanilla: { sheet: 111, frame: 'auto' } });
91	def({ key: 'ore_palladium', name: '钯金矿', solid: true, opacity: 1, pick: 65, mapColor: '#EF5A32', drop: 'palladium_ore', vanilla: { sheet: 221, frame: 'auto' } });
92	def({ key: 'ore_orichalcum', name: '山铜矿', solid: true, opacity: 1, pick: 65, mapColor: '#E760E4', drop: 'orichalcum_ore', vanilla: { sheet: 222, frame: 'auto' } });
93	def({ key: 'ore_titanium', name: '钛矿', solid: true, opacity: 1, pick: 65, mapColor: '#395565', drop: 'titanium_ore', vanilla: { sheet: 223, frame: 'auto' } });
94	def({ key: 'ore_chlorophyte', name: '叶绿矿', solid: true, opacity: 1, pick: 65, mapColor: '#BFE973', drop: 'chlorophyte_ore', vanilla: { sheet: 211, frame: 'auto' } });
95	
96	// ---- 宝石矿（掉对应宝石） ----
97	def({ key: 'gem_sapphire', name: '蓝宝石矿', solid: true, opacity: 1, pick: 30, mapColor: '#6E8CB6', drop: 'sapphire', vanilla: { sheet: 63, frame: 'auto' } });
98	def({ key: 'gem_ruby', name: '红宝石矿', solid: true, opacity: 1, pick: 30, mapColor: '#C46072', drop: 'ruby', vanilla: { sheet: 64, frame: 'auto' } });
99	def({ key: 'gem_emerald', name: '翡翠矿', solid: true, opacity: 1, pick: 30, mapColor: '#389661', drop: 'emerald', vanilla: { sheet: 65, frame: 'auto' } });
100	def({ key: 'gem_topaz', name: '黄玉矿', solid: true, opacity: 1, pick: 30, mapColor: '#A0763A', drop: 'topaz', vanilla: { sheet: 66, frame: 'auto' } });
101	def({ key: 'gem_amethyst', name: '紫水晶矿', solid: true, opacity: 1, pick: 30, mapColor: '#8C3AA6', drop: 'amethyst', vanilla: { sheet: 67, frame: 'auto' } });
102	def({ key: 'gem_diamond', name: '钻石矿', solid: true, opacity: 1, pick: 30, mapColor: '#7DBFC5', drop: 'diamond', vanilla: { sheet: 68, frame: 'auto' } });
103	
104	// ---- 冰雪 ----
105	def({ key: 'ice', name: '冰块', solid: true, opacity: 1, pick: 0, mapColor: '#90C3E8', blend: true, drop: 'ice_block', vanilla: { sheet: 161, frame: 'auto' } });
106	def({ key: 'thin_ice', name: '薄冰', solid: true, opacity: 1, pick: 0, mapColor: '#B8DBF0', blend: true, drop: 'ice_block', vanilla: { sheet: 162, frame: 'auto' } });
107	def({ key: 'ice_brick', name: '冰砖', solid: true, opacity: 1, pick: 0, mapColor: '#7CAFC9', blend: true, drop: 'ice_brick', vanilla: { sheet: 206, frame: 'auto' } });
108	def({ key: 'snow_brick', name: '雪砖', solid: true, opacity: 1, pick: 0, mapColor: '#B5D3D2', blend: true, drop: 'snow_brick', vanilla: { sheet: 148, frame: 'auto' } });
109	
110	// ---- 沙漠 / 基础方块 ----
111	def({ key: 'sandstone', name: '沙岩', solid: true, opacity: 1, pick: 0, mapColor: '#C67C4E', blend: true, drop: 'sandstone_block', vanilla: { sheet: 396, frame: 'auto' } });
112	def({ key: 'hardened_sand', name: '硬化沙块', solid: true, opacity: 1, pick: 0, mapColor: '#D4C064', blend: true, drop: 'hardened_sand_block', vanilla: { sheet: 397, frame: 'auto' } });
113	def({ key: 'desert_fossil', name: '沙漠化石', solid: true, opacity: 1, pick: 0, mapColor: '#8C543C', blend: true, drop: 'desert_fossil', vanilla: { sheet: 404, frame: 'auto' } });
114	def({ key: 'clay', name: '粘土块', solid: true, opacity: 1, pick: 0, mapColor: '#925144', blend: true, drop: 'clay_block', vanilla: { sheet: 40, frame: 'auto' } });
115	def({ key: 'glass', name: '玻璃', solid: true, opacity: 0.15, pick: 0, mapColor: '#C8F6FE', drop: 'glass', vanilla: { sheet: 54, frame: 'auto' } });
116	def({ key: 'obsidian', name: '黑曜石', solid: true, opacity: 1, pick: 40, mapColor: '#2B2854', blend: true, drop: 'obsidian', vanilla: { sheet: 56, frame: 'auto' } });
117	def({ key: 'gray_brick', name: '灰砖', solid: true, opacity: 1, pick: 0, mapColor: '#909090', blend: true, drop: 'gray_brick', vanilla: { sheet: 38, frame: 'auto' } });
118	def({ key: 'red_brick', name: '红砖', solid: true, opacity: 1, pick: 0, mapColor: '#B53E3B', blend: true, drop: 'red_brick', vanilla: { sheet: 39, frame: 'auto' } });
119	def({ key: 'mud', name: '泥块', solid: true, opacity: 1, pick: 0, mapColor: '#5C4449', blend: true, drop: 'mud_block', vanilla: { sheet: 59, frame: 'auto' } });
120	def({ key: 'silt', name: '淤泥块', solid: true, opacity: 1, pick: 0, mapColor: '#6A6B76', blend: true, drop: 'silt_block', vanilla: { sheet: 123, frame: 'auto' } });
121	
122	// 4b：家具 / 装饰（多格 framed，frame:'style' 显式 18px 帧；w/h = TEdit frameSize）
123	const VAN = (sheet: number, w: number, h: number) => ({ vanilla: { sheet, frame: 'style' as const, fw: w, fh: h } });
124	
125	def({ key: 'table', name: '木桌', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 'table', ...VAN(14, 3, 2) });
126	def({ key: 'chair', name: '木椅', framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#BF8E6F', drop: 'chair', ...VAN(15, 1, 2) });
127	def({ key: 'bed', name: '床', framed: true, opacity: 0.05, pick: 0, w: 4, h: 2, mapColor: '#BF8E6F', drop: 'bed', ...VAN(79, 4, 2) });
128	def({ key: 'bookcase', name: '书架', framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#BF8E6F', drop: 'bookcase', ...VAN(101, 3, 4) });
129	def({ key: 'grandfather_clock', name: '落地钟', framed: true, opacity: 0.05, pick: 0, w: 2, h: 5, mapColor: '#BF8E6F', drop: 'grandfather_clock', ...VAN(104, 2, 5) });
130	def({ key: 'piano', name: '钢琴', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 'piano', ...VAN(87, 3, 2) });
131	def({ key: 'dresser', name: '梳妆台', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 'dresser', ...VAN(88, 3, 2) });
132	def({ key: 'bench', name: '长凳', framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: 'bench', ...VAN(89, 3, 2) });
133	def({ key: 'bathtub', name: '浴缸', framed: true, opacity: 0.05, pick: 0, w: 4, h: 2, mapColor: '#909490', drop: 'bathtub', ...VAN(90, 4, 2) });
134	def({ key: 'keg', name: '酒桶', framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: 'keg', ...VAN(94, 2, 2) });
135	def({ key: 'cooking_pot', name: '汤锅', framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: 'cooking_pot', ...VAN(96, 2, 2) });
136	def({ key: 'clay_pot', name: '陶盆', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#796E61', drop: 'clay_pot', ...VAN(78, 1, 1) });
137	def({ key: 'tombstone_v', name: '墓碑', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#C0C0C0', drop: 'tombstone', ...VAN(85, 2, 2) });
138	def({ key: 'crystal_heart', name: '水晶之心', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#AE1845', drop: 'life_crystal', light: [255, 60, 90], ...VAN(12, 2, 2) });
139	// 发光灯具
140	def({ key: 'candle', name: '蜡烛', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#FDDD03', drop: 'candle', light: [255, 185, 110], ...VAN(33, 1, 1) });
141	def({ key: 'chandelier', name: '吊灯', decor: true, framed: true, opacity: 0, pick: 0, w: 3, h: 3, mapColor: '#EBA687', drop: 'chandelier', light: [255, 190, 120], ...VAN(34, 3, 3) });
142	def({ key: 'lantern', name: '吊挂灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 1, h: 2, mapColor: '#FBEB7F', drop: 'lantern', light: [255, 170, 90], ...VAN(42, 1, 2) });
143	def({ key: 'candelabra', name: '烛台', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FDDD03', drop: 'candelabra', light: [255, 185, 110], ...VAN(100, 2, 2) });
144	def({ key: 'chinese_lantern', name: '中式灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FFA21F', drop: 'chinese_lantern', light: [255, 160, 70], ...VAN(95, 2, 2) });
145	def({ key: 'skull_lantern', name: '骷髅灯笼', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#FDDD03', drop: 'skull_lantern', light: [255, 160, 70], ...VAN(98, 2, 2) });
146	def({ key: 'water_candle', name: '水蜡烛', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#2B8FFF', drop: 'water_candle', light: [140, 180, 255], ...VAN(49, 1, 1) });
147	// 瓦罐（世界生成散布）：打破掉随机常用道具（breakTile 特判），不做放置物
148	def({ key: 'pot', name: '瓦罐', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 2, mapColor: '#974F50', drop: null as unknown as string, vanilla: { sheet: 28, frame: 'style', fw: 2, fh: 2 } });
149	
150	export const TILE_BY_KEY: Record<string, number> = {};
151	// 注意：构建必须放在文件末尾（所有 def() 之后），v_ 批量补全定义在下方，
152	// 此处先注册占位，末尾 rebuildTILE_BY_KEY() 统一回填
153	export function isSolidTile(type: number): boolean {
154	  const d = TILE_DEFS[type];
155	  return !!d && d.solid;
156	}
157	
158	// ---- 墙 ----
159	export interface WallDef { key: string; name: string; mapColor: string; opacity: number; }
160	export const W = { NONE: 0, DIRT: 1, STONE: 2, WOOD: 3 } as const;
161	export const WALL_DEFS: WallDef[] = [
162	  { key: 'none', name: '无', mapColor: '#000', opacity: 0 },
163	  { key: 'dirt_wall', name: '土墙', mapColor: '#5C4128', opacity: 1 },
164	  { key: 'stone_wall', name: '石墙', mapColor: '#4A4A4A', opacity: 1 },
165	  { key: 'wood_wall', name: '木墙', mapColor: '#6B4A2B', opacity: 1 },
166	];
167	export const WALL_BY_KEY: Record<string, number> = {};
168	WALL_DEFS.forEach((d, i) => (WALL_BY_KEY[d.key] = i));
169	
170	// ===================== wld 导入全量补全（compat-report 驱动） =====================
171	// 实心 1x1 方块（frame:auto 8 向贴合）
172	def({ key: 'v_51_cobweb', name: 'Cobweb', solid: true, opacity: 1, pick: 0, mapColor: '#C0CACB', blend: true, drop: null as unknown as string, vanilla: { sheet: 51, frame: 'auto' } });
173	def({ key: 'v_368_granite_block', name: 'Granite Block', solid: true, opacity: 1, pick: 0, mapColor: '#322E68', blend: true, drop: null as unknown as string, vanilla: { sheet: 368, frame: 'auto' } });
174	def({ key: 'v_226_lihzahrd_brick', name: 'Lihzahrd Brick', solid: true, opacity: 1, pick: 0, mapColor: '#8D3800', blend: true, drop: null as unknown as string, vanilla: { sheet: 226, frame: 'auto' } });
175	def({ key: 'v_367_marble_block', name: 'Marble Block', solid: true, opacity: 1, pick: 0, mapColor: '#A8B2CC', blend: true, drop: null as unknown as string, vanilla: { sheet: 367, frame: 'auto' } });
176	def({ key: 'v_633_ash_grass_block', name: 'Ash Grass Block', solid: true, opacity: 1, pick: 0, mapColor: '#66474A', blend: true, drop: null as unknown as string, vanilla: { sheet: 633, frame: 'auto' } });
177	def({ key: 'v_181_red_moss_block', name: 'Red Moss Block', solid: true, opacity: 1, pick: 0, mapColor: '#863B31', blend: true, drop: null as unknown as string, vanilla: { sheet: 181, frame: 'auto' } });
178	def({ key: 'v_189_cloud_block', name: 'Cloud Block', solid: true, opacity: 1, pick: 0, mapColor: '#DFFFFF', blend: true, drop: null as unknown as string, vanilla: { sheet: 189, frame: 'auto' } });
179	def({ key: 'v_183_purple_moss_block', name: 'Purple Moss Block', solid: true, opacity: 1, pick: 0, mapColor: '#793186', blend: true, drop: null as unknown as string, vanilla: { sheet: 183, frame: 'auto' } });
180	def({ key: 'v_536_xenon_moss_block', name: 'Xenon Moss Block', solid: true, opacity: 1, pick: 0, mapColor: '#589498', blend: true, drop: null as unknown as string, vanilla: { sheet: 536, frame: 'auto' } });
181	def({ key: 'v_225_hive_block', name: 'Hive Block', solid: true, opacity: 1, pick: 0, mapColor: '#E37D16', blend: true, drop: null as unknown as string, vanilla: { sheet: 225, frame: 'auto' } });
182	def({ key: 'v_483_cracked_pink_brick', name: 'Cracked Pink Brick', solid: true, opacity: 1, pick: 0, mapColor: '#7A405F', blend: true, drop: null as unknown as string, vanilla: { sheet: 483, frame: 'auto' } });
183	def({ key: 'v_224_slush_block', name: 'Slush Block', solid: true, opacity: 1, pick: 0, mapColor: '#6B848B', blend: true, drop: null as unknown as string, vanilla: { sheet: 224, frame: 'auto' } });
184	def({ key: 'v_383_living_mahogany_block', name: 'Living Mahogany Block', solid: true, opacity: 1, pick: 0, mapColor: '#DD8890', blend: true, drop: null as unknown as string, vanilla: { sheet: 383, frame: 'auto' } });
185	def({ key: 'v_179_green_moss_block', name: 'Green Moss Block', solid: true, opacity: 1, pick: 0, mapColor: '#318672', blend: true, drop: null as unknown as string, vanilla: { sheet: 179, frame: 'auto' } });
186	def({ key: 'v_384_living_mahogany_leaves_block', name: 'Living Mahogany Leaves Block', solid: true, opacity: 1, pick: 0, mapColor: '#83CE0C', blend: true, drop: null as unknown as string, vanilla: { sheet: 384, frame: 'auto' } });
187	def({ key: 'v_273_stone_slab', name: 'Stone Slab', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: null as unknown as string, vanilla: { sheet: 273, frame: 'auto' } });
188	def({ key: 'v_381_lava_moss', name: 'Lava Moss', solid: true, opacity: 1, pick: 0, mapColor: '#FE7902', blend: true, drop: null as unknown as string, light: [255, 120, 30], vanilla: { sheet: 381, frame: 'auto' } });
189	def({ key: 'v_48_spike', name: 'Spike', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: null as unknown as string, vanilla: { sheet: 48, frame: 'auto' } });
190	def({ key: 'v_192_living_leaf_block', name: 'Living Leaf Block', solid: true, opacity: 1, pick: 0, mapColor: '#1AC454', blend: true, drop: null as unknown as string, vanilla: { sheet: 192, frame: 'auto' } });
191	def({ key: 'v_191_living_wood_block', name: 'Living Wood Block', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: null as unknown as string, vanilla: { sheet: 191, frame: 'auto' } });
192	def({ key: 'v_196_rain_cloud_block', name: 'Rain Cloud Block', solid: true, opacity: 1, pick: 0, mapColor: '#9390B2', blend: true, drop: null as unknown as string, vanilla: { sheet: 196, frame: 'auto' } });
193	def({ key: 'v_118_pearlstone_brick', name: 'Pearlstone Brick', solid: true, opacity: 1, pick: 0, mapColor: '#EEE1DA', blend: true, drop: null as unknown as string, vanilla: { sheet: 118, frame: 'auto' } });
194	def({ key: 'v_321_boreal_wood', name: 'Boreal Wood', solid: true, opacity: 1, pick: 0, mapColor: '#604D40', blend: true, drop: null as unknown as string, vanilla: { sheet: 321, frame: 'auto' } });
195	def({ key: 'v_152_ebonstone_brick', name: 'Ebonstone Brick', solid: true, opacity: 1, pick: 0, mapColor: '#8085B8', blend: true, drop: null as unknown as string, vanilla: { sheet: 152, frame: 'auto' } });
196	def({ key: 'v_158_rich_mahogany', name: 'Rich Mahogany', solid: true, opacity: 1, pick: 0, mapColor: '#915155', blend: true, drop: null as unknown as string, vanilla: { sheet: 158, frame: 'auto' } });
197	def({ key: 'v_357_smooth_marble_block', name: 'Smooth Marble Block', solid: true, opacity: 1, pick: 0, mapColor: '#A8B2CC', blend: true, drop: null as unknown as string, vanilla: { sheet: 357, frame: 'auto' } });
198	def({ key: 'v_272_cog_block', name: 'Cog Block', solid: true, opacity: 1, pick: 0, mapColor: '#797765', blend: true, drop: null as unknown as string, vanilla: { sheet: 272, frame: 'auto' } });
199	def({ key: 'v_229_honey_block', name: 'Honey Block', solid: true, opacity: 1, pick: 0, mapColor: '#FF9C0C', blend: true, drop: null as unknown as string, vanilla: { sheet: 229, frame: 'auto' } });
200	def({ key: 'v_311_dynasty_wood', name: 'Dynasty Wood', solid: true, opacity: 1, pick: 0, mapColor: '#753D19', blend: true, drop: null as unknown as string, vanilla: { sheet: 311, frame: 'auto' } });
201	def({ key: 'v_130_active_stone_block', name: 'Active Stone Block', solid: true, opacity: 1, pick: 0, mapColor: '#A0A0A0', blend: true, drop: null as unknown as string, vanilla: { sheet: 130, frame: 'auto' } });
202	def({ key: 'v_193_slime_block', name: 'Slime Block', solid: true, opacity: 1, pick: 0, mapColor: '#3879FF', blend: true, drop: null as unknown as string, vanilla: { sheet: 193, frame: 'auto' } });
203	def({ key: 'v_190_glowing_mushroom_block', name: 'Glowing Mushroom Block', solid: true, opacity: 1, pick: 0, mapColor: '#B6AF82', blend: true, drop: null as unknown as string, light: [120, 110, 180], vanilla: { sheet: 190, frame: 'auto' } });
204	def({ key: 'v_350_martian_conduit_plating', name: 'Martian Conduit Plating', solid: true, opacity: 1, pick: 0, mapColor: '#37619B', blend: true, drop: null as unknown as string, vanilla: { sheet: 350, frame: 'auto' } });
205	def({ key: 'v_369_smooth_granite_block', name: 'Smooth Granite Block', solid: true, opacity: 1, pick: 0, mapColor: '#322E68', blend: true, drop: null as unknown as string, vanilla: { sheet: 369, frame: 'auto' } });
206	def({ key: 'v_137_traps', name: 'Traps', solid: true, opacity: 1, pick: 0, mapColor: '#909490', blend: true, drop: null as unknown as string, vanilla: { sheet: 137, frame: 'auto' } });
207	def({ key: 'v_117_pearlstone_block', name: 'Pearlstone Block', solid: true, opacity: 1, pick: 0, mapColor: '#B5ACBE', blend: true, drop: null as unknown as string, vanilla: { sheet: 117, frame: 'auto' } });
208	def({ key: 'v_112_ebonsand_block', name: 'Ebonsand Block', solid: true, opacity: 1, pick: 0, mapColor: '#67627A', blend: true, drop: null as unknown as string, vanilla: { sheet: 112, frame: 'auto' } });
209	def({ key: 'v_232_wooden_spike', name: 'Wooden Spike', solid: true, opacity: 1, pick: 0, mapColor: '#915155', blend: true, drop: null as unknown as string, vanilla: { sheet: 232, frame: 'auto' } });
210	def({ key: 'v_274_sandstone_slab', name: 'Sandstone Slab', solid: true, opacity: 1, pick: 0, mapColor: '#BEAB5E', blend: true, drop: null as unknown as string, vanilla: { sheet: 274, frame: 'auto' } });
211	def({ key: 'v_322_palm_wood', name: 'Palm Wood', solid: true, opacity: 1, pick: 0, mapColor: '#C6AA68', blend: true, drop: null as unknown as string, vanilla: { sheet: 322, frame: 'auto' } });
212	def({ key: 'v_109_hallowed_grass_block', name: 'Hallowed Grass Block', solid: true, opacity: 1, pick: 0, mapColor: '#4EC1E3', blend: true, drop: null as unknown as string, vanilla: { sheet: 109, frame: 'auto' } });
213	def({ key: 'v_312_red_dynasty_shingles', name: 'Red Dynasty Shingles', solid: true, opacity: 1, pick: 0, mapColor: '#CC5D49', blend: true, drop: null as unknown as string, vanilla: { sheet: 312, frame: 'auto' } });
214	def({ key: 'v_422_conveyor_belt_ccw', name: 'Conveyor Belt (CCW)', solid: true, opacity: 1, pick: 0, mapColor: '#494646', blend: true, drop: null as unknown as string, vanilla: { sheet: 422, frame: 'auto' } });
215	def({ key: 'v_495_shell_pile_block', name: 'Shell Pile Block', solid: true, opacity: 1, pick: 0, mapColor: '#AF976E', blend: true, drop: null as unknown as string, vanilla: { sheet: 495, frame: 'auto' } });
216	def({ key: 'v_479_smooth_sandstone_block', name: 'Smooth Sandstone Block', solid: true, opacity: 1, pick: 0, mapColor: '#BC7347', blend: true, drop: null as unknown as string, vanilla: { sheet: 479, frame: 'auto' } });
217	def({ key: 'v_353_vine_rope', name: 'Vine Rope', solid: true, opacity: 1, pick: 0, mapColor: '#1CD85E', blend: true, drop: null as unknown as string, vanilla: { sheet: 353, frame: 'auto' } });
218	def({ key: 'v_477_mowed_grass_block', name: 'Mowed Grass Block', solid: true, opacity: 1, pick: 0, mapColor: '#607044', blend: true, drop: null as unknown as string, vanilla: { sheet: 477, frame: 'auto' } });
219	def({ key: 'v_380_planter_boxes', name: 'Planter Boxes', solid: true, opacity: 1, pick: 0, mapColor: '#BF8E6F', blend: true, drop: null as unknown as string, vanilla: { sheet: 380, frame: 'auto' } });
220	def({ key: 'v_230_crispy_honey_block', name: 'Crispy Honey Block', solid: true, opacity: 1, pick: 0, mapColor: '#834F0D', blend: true, drop: null as unknown as string, vanilla: { sheet: 230, frame: 'auto' } });
221	def({ key: 'v_562_bamboo_block', name: 'Bamboo Block', solid: true, opacity: 1, pick: 0, mapColor: '#737A2D', blend: true, drop: null as unknown as string, vanilla: { sheet: 562, frame: 'auto' } });
222	def({ key: 'v_371_pink_slime_block', name: 'Pink Slime Block', solid: true, opacity: 1, pick: 0, mapColor: '#F965BD', blend: true, drop: null as unknown as string, vanilla: { sheet: 371, frame: 'auto' } });
223	def({ key: 'v_668_the_dirtiest_block', name: 'The Dirtiest Block', solid: true, opacity: 1, pick: 0, mapColor: '#bf8e6f', blend: true, drop: null as unknown as string, vanilla: { sheet: 668, frame: 'auto' } });
224	def({ key: 'v_398_corrupt_hardened_sand_block', name: 'Corrupt Hardened Sand Block', solid: true, opacity: 1, pick: 0, mapColor: '#64527E', blend: true, drop: null as unknown as string, vanilla: { sheet: 398, frame: 'auto' } });
225	def({ key: 'v_379_bubble', name: 'Bubble', solid: true, opacity: 1, pick: 0, mapColor: '#FBD1F0', blend: true, drop: null as unknown as string, vanilla: { sheet: 379, frame: 'auto' } });
226	def({ key: 'v_618_stone_accent_slab', name: 'Stone Accent Slab', solid: true, opacity: 1, pick: 0, mapColor: '#828282', blend: true, drop: null as unknown as string, vanilla: { sheet: 618, frame: 'auto' } });
227	
228	// framed 物体（frame:style 显式 18px 帧）
229	def({ key: 'v_165_cave_decos', name: 'Cave Decos', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#646464', drop: null as unknown as string, vanilla: { sheet: 165, frame: 'style', fw: 1, fh: 2 } });
230	def({ key: 'v_184_moss_plants', name: 'Moss Plants', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#646464', drop: null as unknown as string, vanilla: { sheet: 184, frame: 'style', fw: 1, fh: 1 } });
231	def({ key: 'v_314_minecart_track', name: 'Minecart Track', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#B5A47D', drop: null as unknown as string, vanilla: { sheet: 314, frame: 'style', fw: 1, fh: 1 } });
232	def({ key: 'v_185_small_decos', name: 'Small Decos', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#959573', drop: null as unknown as string, vanilla: { sheet: 185, frame: 'style', fw: 1, fh: 1 } });
233	def({ key: 'v_373_water_drip', name: 'Water Drip', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#093DBF', drop: null as unknown as string, vanilla: { sheet: 373, frame: 'style', fw: 1, fh: 1 } });
234	def({ key: 'v_187_decos_3x2_group_2', name: 'Decos (3x2) (Group 2)', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#FF00FF', drop: null as unknown as string, vanilla: { sheet: 187, frame: 'style', fw: 3, fh: 2 } });
235	def({ key: 'v_484_rolling_cactus', name: 'Rolling Cactus', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#737E3D', drop: null as unknown as string, vanilla: { sheet: 484, frame: 'style', fw: 2, fh: 2 } });
236	def({ key: 'v_374_lava_drip', name: 'Lava Drip', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FD2003', drop: null as unknown as string, vanilla: { sheet: 374, frame: 'style', fw: 1, fh: 1 } });
237	def({ key: 'v_233_jungle_large_plants', name: 'Jungle Large Plants', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#FF00FF', drop: null as unknown as string, vanilla: { sheet: 233, frame: 'style', fw: 3, fh: 2 } });
238	def({ key: 'v_105_statue', name: 'Statue', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 105, frame: 'style', fw: 2, fh: 3 } });
239	def({ key: 'v_186_decos_3x2', name: 'Decos (3x2)', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#FF00FF', drop: null as unknown as string, vanilla: { sheet: 186, frame: 'style', fw: 3, fh: 2 } });
240	def({ key: 'v_461_sand_drip', name: 'Sand Drip', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FFDE64', drop: null as unknown as string, vanilla: { sheet: 461, frame: 'style', fw: 1, fh: 1 } });
241	def({ key: 'v_178_gems', name: 'Gems', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FF00FF', drop: null as unknown as string, vanilla: { sheet: 178, frame: 'style', fw: 1, fh: 1 } });
242	def({ key: 'v_485_antlion_larva', name: 'Antlion Larva', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#A17956', drop: null as unknown as string, vanilla: { sheet: 485, frame: 'style', fw: 2, fh: 2 } });
243	def({ key: 'v_637_ash_short_plants', name: 'Ash Short Plants', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#884338', drop: null as unknown as string, vanilla: { sheet: 637, frame: 'style', fw: 1, fh: 1 } });
244	def({ key: 'v_444_bee_hive', name: 'Bee Hive', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#bfb07c', drop: null as unknown as string, vanilla: { sheet: 444, frame: 'style', fw: 2, fh: 2 } });
245	def({ key: 'v_240_wall_hangings_3x3', name: 'Wall Hangings 3x3', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#63321E', drop: null as unknown as string, vanilla: { sheet: 240, frame: 'style', fw: 3, fh: 3 } });
246	def({ key: 'v_519_cattails', name: 'Cattails', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#7F7F99', drop: null as unknown as string, vanilla: { sheet: 519, frame: 'style', fw: 1, fh: 1 } });
247	def({ key: 'v_138_boulder', name: 'Boulder', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#606060', drop: null as unknown as string, vanilla: { sheet: 138, frame: 'style', fw: 2, fh: 2 } });
248	def({ key: 'v_634_ash_tree', name: 'Ash Tree', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#7D5453', drop: null as unknown as string, vanilla: { sheet: 634, frame: 'style', fw: 1, fh: 1 } });
249	def({ key: 'v_26_altars', name: 'Altars', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#77657D', drop: null as unknown as string, vanilla: { sheet: 26, frame: 'style', fw: 3, fh: 2 } });
250	def({ key: 'v_82_herbs_sprout', name: 'Herbs (Sprout)', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FF7800', drop: null as unknown as string, vanilla: { sheet: 82, frame: 'style', fw: 1, fh: 1 } });
251	def({ key: 'v_323_palm_trees', name: 'Palm Trees', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#B68D56', drop: null as unknown as string, vanilla: { sheet: 323, frame: 'style', fw: 1, fh: 1 } });
252	def({ key: 'v_135_pressure_plates', name: 'Pressure Plates', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FD7272', drop: null as unknown as string, vanilla: { sheet: 135, frame: 'style', fw: 1, fh: 1 } });
253	def({ key: 'v_91_banners', name: 'Banners', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#0D5882', drop: null as unknown as string, vanilla: { sheet: 91, frame: 'style', fw: 1, fh: 3 } });
254	def({ key: 'v_242_paintings_6x4', name: 'Paintings 6x4', solid: false, framed: true, opacity: 0.05, pick: 0, w: 6, h: 4, mapColor: '#63321E', drop: null as unknown as string, vanilla: { sheet: 242, frame: 'style', fw: 6, fh: 4 } });
255	def({ key: 'v_50_books', name: 'Books', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#AA3072', drop: null as unknown as string, vanilla: { sheet: 50, frame: 'style', fw: 1, fh: 1 } });
256	def({ key: 'v_93_lamps', name: 'Lamps', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#FDDD03', drop: null as unknown as string, light: [255, 185, 110], vanilla: { sheet: 93, frame: 'style', fw: 1, fh: 3 } });
257	def({ key: 'v_549_seaweed', name: 'Seaweed', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#385806', drop: null as unknown as string, vanilla: { sheet: 549, frame: 'style', fw: 1, fh: 1 } });
258	def({ key: 'v_254_pumpkin_plant', name: 'Pumpkin Plant', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#F89E5C', drop: null as unknown as string, vanilla: { sheet: 254, frame: 'style', fw: 2, fh: 2 } });
259	def({ key: 'v_571_bamboo', name: 'Bamboo', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#638017', drop: null as unknown as string, vanilla: { sheet: 571, frame: 'style', fw: 1, fh: 1 } });
260	def({ key: 'v_246_paintings_3x2', name: 'Paintings 3x2', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#63321E', drop: null as unknown as string, vanilla: { sheet: 246, frame: 'style', fw: 3, fh: 2 } });
261	def({ key: 'v_245_paintings_2x3', name: 'Paintings 2x3', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#63321E', drop: null as unknown as string, vanilla: { sheet: 245, frame: 'style', fw: 2, fh: 3 } });
262	def({ key: 'v_586_emerald_tree', name: 'Emerald Tree', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#717171', drop: null as unknown as string, vanilla: { sheet: 586, frame: 'style', fw: 1, fh: 1 } });
263	def({ key: 'v_596_vanity_tree_sakura', name: 'Vanity Tree Sakura', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#6E5B4D', drop: null as unknown as string, vanilla: { sheet: 596, frame: 'style', fw: 1, fh: 1 } });
264	def({ key: 'v_467_chests_group_2', name: 'Chests (Group 2)', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#E9CF5E', drop: null as unknown as string, vanilla: { sheet: 467, frame: 'style', fw: 2, fh: 2 } });
265	def({ key: 'v_443_geyser', name: 'Geyser', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#7b7b7b', drop: null as unknown as string, vanilla: { sheet: 443, frame: 'style', fw: 2, fh: 1 } });
266	def({ key: 'v_589_amber_tree', name: 'Amber Tree', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#717171', drop: null as unknown as string, vanilla: { sheet: 589, frame: 'style', fw: 1, fh: 1 } });
267	def({ key: 'v_411_detonator', name: 'Detonator', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#E32E2E', drop: null as unknown as string, vanilla: { sheet: 411, frame: 'style', fw: 2, fh: 2 } });
268	def({ key: 'v_518_lily_pads', name: 'Lily Pads', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#6C5F84', drop: null as unknown as string, vanilla: { sheet: 518, frame: 'style', fw: 1, fh: 1 } });
269	def({ key: 'v_588_diamond_tree', name: 'Diamond Tree', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#717171', drop: null as unknown as string, vanilla: { sheet: 588, frame: 'style', fw: 1, fh: 1 } });
270	def({ key: 'v_585_sapphire_tree', name: 'Sapphire Tree', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#717171', drop: null as unknown as string, vanilla: { sheet: 585, frame: 'style', fw: 1, fh: 1 } });
271	def({ key: 'v_583_topaz_tree', name: 'Topaz Tree', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#717171', drop: null as unknown as string, vanilla: { sheet: 583, frame: 'style', fw: 1, fh: 1 } });
272	def({ key: 'v_13_placed_bottles', name: 'Placed Bottles', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#85D5F7', drop: null as unknown as string, vanilla: { sheet: 13, frame: 'style', fw: 1, fh: 1 } });
273	def({ key: 'v_530_oasis_plants', name: 'Oasis Plants', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#5B546C', drop: null as unknown as string, vanilla: { sheet: 530, frame: 'style', fw: 3, fh: 2 } });
274	def({ key: 'v_616_vanity_tree_yellow_willow', name: 'Vanity Tree Yellow Willow', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#854F4D', drop: null as unknown as string, vanilla: { sheet: 616, frame: 'style', fw: 1, fh: 1 } });
275	def({ key: 'v_215_campfires', name: 'Campfires', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#FE7902', drop: null as unknown as string, light: [255, 185, 110], vanilla: { sheet: 215, frame: 'style', fw: 3, fh: 2 } });
276	def({ key: 'v_141_explosives', name: 'Explosives', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#C03B3B', drop: null as unknown as string, vanilla: { sheet: 141, frame: 'style', fw: 1, fh: 1 } });
277	def({ key: 'v_597_pylons', name: 'Pylons', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#787F4B', drop: null as unknown as string, vanilla: { sheet: 597, frame: 'style', fw: 3, fh: 4 } });
278	def({ key: 'v_592_hanging_brazier', name: 'Hanging Brazier', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#A57345', drop: null as unknown as string, light: [255, 185, 110], vanilla: { sheet: 592, frame: 'style', fw: 2, fh: 3 } });
279	def({ key: 'v_375_honey_drip', name: 'Honey Drip', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FF9C0C', drop: null as unknown as string, vanilla: { sheet: 375, frame: 'style', fw: 1, fh: 1 } });
280	def({ key: 'v_227_dye_plants', name: 'Dye Plants', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FFFFFF', drop: null as unknown as string, vanilla: { sheet: 227, frame: 'style', fw: 1, fh: 1 } });
281	def({ key: 'v_584_amethyst_tree', name: 'Amethyst Tree', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#717171', drop: null as unknown as string, vanilla: { sheet: 584, frame: 'style', fw: 1, fh: 1 } });
282	def({ key: 'v_231_larva', name: 'Larva', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#E0C265', drop: null as unknown as string, vanilla: { sheet: 231, frame: 'style', fw: 3, fh: 3 } });
283	def({ key: 'v_395_item_frame', name: 'Item Frame', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#BF8E6F', drop: null as unknown as string, vanilla: { sheet: 395, frame: 'style', fw: 2, fh: 2 } });
284	def({ key: 'v_241_catacombs', name: 'Catacombs', solid: false, framed: true, opacity: 0.05, pick: 0, w: 4, h: 3, mapColor: '#4D4A48', drop: null as unknown as string, vanilla: { sheet: 241, frame: 'style', fw: 4, fh: 3 } });
285	def({ key: 'v_587_ruby_tree', name: 'Ruby Tree', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#717171', drop: null as unknown as string, vanilla: { sheet: 587, frame: 'style', fw: 1, fh: 1 } });
286	def({ key: 'v_86_loom', name: 'Loom', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null as unknown as string, vanilla: { sheet: 86, frame: 'style', fw: 3, fh: 2 } });
287	def({ key: 'v_376_fishing_crates', name: 'Fishing Crates', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#A0785C', drop: null as unknown as string, vanilla: { sheet: 376, frame: 'style', fw: 2, fh: 2 } });
288	def({ key: 'v_470_mannequins', name: 'Mannequins', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#7B5B44', drop: null as unknown as string, vanilla: { sheet: 470, frame: 'style', fw: 2, fh: 3 } });
289	def({ key: 'v_324_seashells', name: 'Seashells', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#E4D5AD', drop: null as unknown as string, vanilla: { sheet: 324, frame: 'style', fw: 1, fh: 1 } });
290	def({ key: 'v_81_coral', name: 'Coral', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#F585BF', drop: null as unknown as string, vanilla: { sheet: 81, frame: 'style', fw: 1, fh: 1 } });
291	def({ key: 'v_136_switch', name: 'Switch', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#D5CBCC', drop: null as unknown as string, vanilla: { sheet: 136, frame: 'style', fw: 1, fh: 1 } });
292	def({ key: 'v_355_alchemy_table', name: 'Alchemy Table', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#8D6B59', drop: null as unknown as string, vanilla: { sheet: 355, frame: 'style', fw: 3, fh: 3 } });
293	def({ key: 'v_354_bewitching_table', name: 'Bewitching Table', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#8D6B59', drop: null as unknown as string, vanilla: { sheet: 354, frame: 'style', fw: 3, fh: 3 } });
294	def({ key: 'v_103_bowls', name: 'Bowls', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#8D624D', drop: null as unknown as string, vanilla: { sheet: 103, frame: 'style', fw: 2, fh: 1 } });
295	def({ key: 'v_529_sea_oats', name: 'Sea Oats', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#675874', drop: null as unknown as string, vanilla: { sheet: 529, frame: 'style', fw: 1, fh: 2 } });
296	def({ key: 'v_506_bast_statue', name: 'Bast Statue', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#291C13', drop: null as unknown as string, vanilla: { sheet: 506, frame: 'style', fw: 2, fh: 3 } });
297	def({ key: 'v_349_mushroom_statue', name: 'Mushroom Statue', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 349, frame: 'style', fw: 2, fh: 3 } });
298	def({ key: 'v_377_sharpening_station', name: 'Sharpening Station', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null as unknown as string, vanilla: { sheet: 377, frame: 'style', fw: 3, fh: 2 } });
299	def({ key: 'v_613_potted_lava_plants', name: 'Potted Lava Plants', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 5, mapColor: '#885D34', drop: null as unknown as string, vanilla: { sheet: 613, frame: 'style', fw: 3, fh: 5 } });
300	def({ key: 'v_219_extractinator', name: 'Extractinator', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 219, frame: 'style', fw: 3, fh: 3 } });
301	def({ key: 'v_388_tall_gate_closed', name: 'Tall Gate (Closed)', solid: true, framed: true, opacity: 1, pick: 0, w: 1, h: 5, mapColor: '#7F5C45', drop: null as unknown as string, vanilla: { sheet: 388, frame: 'style', fw: 1, fh: 5 } });
302	def({ key: 'v_129_crystal_shard', name: 'Crystal Shard', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FF75E0', drop: null as unknown as string, vanilla: { sheet: 129, frame: 'style', fw: 1, fh: 1 } });
303	def({ key: 'v_466_elder_cystal_stand', name: 'Elder Cystal Stand', solid: false, framed: true, opacity: 0.05, pick: 0, w: 5, h: 4, mapColor: '#CD9949', drop: null as unknown as string, vanilla: { sheet: 466, frame: 'style', fw: 5, fh: 4 } });
304	def({ key: 'v_220_solidifier', name: 'Solidifier', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 220, frame: 'style', fw: 3, fh: 3 } });
305	def({ key: 'v_303_lihzahrd_furnace', name: 'Lihzahrd Furnace', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 303, frame: 'style', fw: 3, fh: 3 } });
306	def({ key: 'v_469_tables_group_2', name: 'Tables (Group 2)', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null as unknown as string, vanilla: { sheet: 469, frame: 'style', fw: 3, fh: 2 } });
307	def({ key: 'v_304_living_loom', name: 'Living Loom', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 304, frame: 'style', fw: 3, fh: 3 } });
308	def({ key: 'v_488_fallen_log', name: 'Fallen Log', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#72654F', drop: null as unknown as string, vanilla: { sheet: 488, frame: 'style', fw: 3, fh: 2 } });
309	def({ key: 'v_548_potted_trees_group_2', name: 'Potted Trees (Group 2)', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 6, mapColor: '#866036', drop: null as unknown as string, vanilla: { sheet: 548, frame: 'style', fw: 3, fh: 6 } });
310	def({ key: 'v_614_potted_ember_tendrils', name: 'Potted Ember Tendrils', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 6, mapColor: '#724D31', drop: null as unknown as string, vanilla: { sheet: 614, frame: 'style', fw: 3, fh: 6 } });
311	def({ key: 'v_598_lava_serpent_bowl', name: 'Lava Serpent Bowl', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#92726F', drop: null as unknown as string, light: [255, 185, 110], vanilla: { sheet: 598, frame: 'style', fw: 2, fh: 2 } });
312	def({ key: 'v_406_chimney', name: 'Chimney', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#787878', drop: null as unknown as string, vanilla: { sheet: 406, frame: 'style', fw: 3, fh: 3 } });
313	def({ key: 'v_305_sky_mill', name: 'Sky Mill', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 305, frame: 'style', fw: 3, fh: 3 } });
314	def({ key: 'v_300_bone_welder', name: 'Bone Welder', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 300, frame: 'style', fw: 3, fh: 3 } });
315	def({ key: 'v_302_glass_kiln', name: 'Glass Kiln', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 302, frame: 'style', fw: 3, fh: 3 } });
316	def({ key: 'v_306_ice_machine', name: 'Ice Machine', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 306, frame: 'style', fw: 3, fh: 3 } });
317	def({ key: 'v_247_autohammer', name: 'Autohammer', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#8C9696', drop: null as unknown as string, vanilla: { sheet: 247, frame: 'style', fw: 3, fh: 3 } });
318	def({ key: 'v_491_void_vault', name: 'Void Vault', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#8149B1', drop: null as unknown as string, vanilla: { sheet: 491, frame: 'style', fw: 3, fh: 3 } });
319	def({ key: 'v_106_sawmill', name: 'Sawmill', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#BF8E6F', drop: null as unknown as string, vanilla: { sheet: 106, frame: 'style', fw: 3, fh: 3 } });
320	def({ key: 'v_642_chlorophyte_extractinator', name: 'Chlorophyte Extractinator', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 3, mapColor: '#6E8B81', drop: null as unknown as string, vanilla: { sheet: 642, frame: 'style', fw: 3, fh: 3 } });
321	def({ key: 'v_319_ship_in_a_bottle', name: 'Ship in a Bottle', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#604430', drop: null as unknown as string, vanilla: { sheet: 319, frame: 'style', fw: 2, fh: 2 } });
322	def({ key: 'v_487_picnic_tables', name: 'Picnic Tables', solid: false, framed: true, opacity: 0.05, pick: 0, w: 4, h: 2, mapColor: '#8D5A57', drop: null as unknown as string, vanilla: { sheet: 487, frame: 'style', fw: 4, fh: 2 } });
323	def({ key: 'v_97_safe', name: 'Safe', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 97, frame: 'style', fw: 2, fh: 2 } });
324	def({ key: 'v_320_seaweed_planter', name: 'Seaweed Planter', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#CBB997', drop: null as unknown as string, vanilla: { sheet: 320, frame: 'style', fw: 2, fh: 3 } });
325	def({ key: 'v_405_fireplace', name: 'Fireplace', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#8C8C8C', drop: null as unknown as string, light: [255, 185, 110], vanilla: { sheet: 405, frame: 'style', fw: 3, fh: 2 } });
326	def({ key: 'v_378_target_dummy', name: 'Target Dummy', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#A07864', drop: null as unknown as string, vanilla: { sheet: 378, frame: 'style', fw: 2, fh: 3 } });
327	def({ key: 'v_218_meat_grinder', name: 'Meat Grinder', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 218, frame: 'style', fw: 3, fh: 2 } });
328	def({ key: 'v_356_enchanted_sundial', name: 'Enchanted Sundial', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#E9CB18', drop: null as unknown as string, vanilla: { sheet: 356, frame: 'style', fw: 2, fh: 3 } });
329	def({ key: 'v_114_tinkerer_s_workshop', name: 'Tinkerer\'s Workshop', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#BF8E6F', drop: null as unknown as string, vanilla: { sheet: 114, frame: 'style', fw: 3, fh: 2 } });
330	def({ key: 'v_237_lihzahrd_altar', name: 'Lihzahrd Altar', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 2, mapColor: '#FFF133', drop: null as unknown as string, vanilla: { sheet: 237, frame: 'style', fw: 3, fh: 2 } });
331	def({ key: 'v_110_hallow_short_plants', name: 'Hallow Short Plants', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#30BA87', drop: null as unknown as string, vanilla: { sheet: 110, frame: 'style', fw: 1, fh: 1 } });
332	def({ key: 'v_621_slice_of_cake', name: 'Slice of Cake', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#8E6A67', drop: null as unknown as string, vanilla: { sheet: 621, frame: 'style', fw: 2, fh: 2 } });
333	def({ key: 'v_387_trap_door_closed', name: 'Trap Door (Closed)', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 1, mapColor: '#7F5C45', drop: null as unknown as string, vanilla: { sheet: 387, frame: 'style', fw: 2, fh: 1 } });
334	def({ key: 'v_316_blue_jellyfish_jar', name: 'Blue Jellyfish Jar', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null as unknown as string, vanilla: { sheet: 316, frame: 'style', fw: 2, fh: 2 } });
335	def({ key: 'v_125_crystal_ball', name: 'Crystal Ball', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#8DAFFF', drop: null as unknown as string, vanilla: { sheet: 125, frame: 'style', fw: 2, fh: 2 } });
336	def({ key: 'v_287_ammo_box', name: 'Ammo Box', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#4F8011', drop: null as unknown as string, vanilla: { sheet: 287, frame: 'style', fw: 2, fh: 2 } });
337	def({ key: 'v_294_zebra_swallowtail_butterfly_jar', name: 'Zebra Swallowtail Butterfly Jar', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null as unknown as string, vanilla: { sheet: 294, frame: 'style', fw: 2, fh: 2 } });
338	def({ key: 'v_291_ulysses_butterfly_jar', name: 'Ulysses Butterfly Jar', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null as unknown as string, vanilla: { sheet: 291, frame: 'style', fw: 2, fh: 2 } });
339	def({ key: 'v_292_sulphur_butterfly_jar', name: 'Sulphur Butterfly Jar', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null as unknown as string, vanilla: { sheet: 292, frame: 'style', fw: 2, fh: 2 } });
340	def({ key: 'v_289_purple_emperor_butterfly_jar', name: 'Purple Emperor Butterfly Jar', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7AD9E8', drop: null as unknown as string, vanilla: { sheet: 289, frame: 'style', fw: 2, fh: 2 } });
341	def({ key: 'v_172_sinks', name: 'Sinks', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#B5C2D9', drop: null as unknown as string, vanilla: { sheet: 172, frame: 'style', fw: 2, fh: 2 } });
342	def({ key: 'v_656_glow_tulip', name: 'Glow Tulip', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#3995B3', drop: null as unknown as string, light: [255, 185, 110], vanilla: { sheet: 656, frame: 'style', fw: 1, fh: 1 } });
343	def({ key: 'v_113_hallow_tall_plants', name: 'Hallow Tall Plants', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#30D0EA', drop: null as unknown as string, vanilla: { sheet: 113, frame: 'style', fw: 1, fh: 1 } });
344	def({ key: 'v_235_teleporter', name: 'Teleporter', solid: true, framed: true, opacity: 1, pick: 0, w: 3, h: 1, mapColor: '#D6B82E', drop: null as unknown as string, vanilla: { sheet: 235, frame: 'style', fw: 3, fh: 1 } });
345	def({ key: 'v_567_garden_gnome', name: 'Garden Gnome', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 2, mapColor: '#938381', drop: null as unknown as string, vanilla: { sheet: 567, frame: 'style', fw: 1, fh: 2 } });
346	
347	// 装饰/植物/藤蔓（非实心非framed）
348	def({ key: 'v_638_ash_vines', name: 'Ash Vines', decor: true, opacity: 0, pick: 0, mapColor: '#844A3C', drop: null as unknown as string, vanilla: { sheet: 638, frame: 'auto' } });
349	def({ key: 'v_528_mushroom_vines', name: 'Mushroom Vines', decor: true, opacity: 0, pick: 0, mapColor: '#827E5D', drop: null as unknown as string, vanilla: { sheet: 528, frame: 'auto' } });
350	def({ key: 'v_382_flower_vines', name: 'Flower Vines', decor: true, opacity: 0, pick: 0, mapColor: '#1CD85E', drop: null as unknown as string, vanilla: { sheet: 382, frame: 'auto' } });
351	def({ key: 'v_124_wooden_beam', name: 'Wooden Beam', decor: true, opacity: 0, pick: 0, mapColor: '#493324', drop: null as unknown as string, vanilla: { sheet: 124, frame: 'auto' } });
352	def({ key: 'v_575_rich_mahogany_beam', name: 'Rich Mahogany Beam', decor: true, opacity: 0, pick: 0, mapColor: '#60393C', drop: null as unknown as string, vanilla: { sheet: 575, frame: 'auto' } });
353	def({ key: 'v_213_rope', name: 'Rope', decor: true, opacity: 0, pick: 0, mapColor: '#897843', drop: null as unknown as string, vanilla: { sheet: 213, frame: 'auto' } });
354	def({ key: 'v_636_corrupt_vines', name: 'Corrupt Vines', decor: true, opacity: 0, pick: 0, mapColor: '#746CA3', drop: null as unknown as string, vanilla: { sheet: 636, frame: 'auto' } });
355	def({ key: 'v_574_boreal_beam', name: 'Boreal Beam', decor: true, opacity: 0, pick: 0, mapColor: '#44372F', drop: null as unknown as string, vanilla: { sheet: 574, frame: 'auto' } });
356	def({ key: 'v_333_platinum_coin_pile', name: 'Platinum Coin Pile', decor: true, opacity: 0, pick: 0, mapColor: '#BEBEB2', drop: null as unknown as string, vanilla: { sheet: 333, frame: 'auto' } });
357	def({ key: 'v_332_gold_coin_pile', name: 'Gold Coin Pile', decor: true, opacity: 0, pick: 0, mapColor: '#CCB548', drop: null as unknown as string, vanilla: { sheet: 332, frame: 'auto' } });
358	def({ key: 'v_577_sandstone_column', name: 'Sandstone Column', decor: true, opacity: 0, pick: 0, mapColor: '#885635', drop: null as unknown as string, vanilla: { sheet: 577, frame: 'auto' } });
359	def({ key: 'v_561_marble_column', name: 'Marble Column', decor: true, opacity: 0, pick: 0, mapColor: '#6E7482', drop: null as unknown as string, vanilla: { sheet: 561, frame: 'auto' } });
360	def({ key: 'v_576_granite_column', name: 'Granite Column', decor: true, opacity: 0, pick: 0, mapColor: '#242659', drop: null as unknown as string, vanilla: { sheet: 576, frame: 'auto' } });
361	def({ key: 'v_214_chain', name: 'Chain', decor: true, opacity: 0, pick: 0, mapColor: '#676767', drop: null as unknown as string, vanilla: { sheet: 214, frame: 'auto' } });
362	def({ key: 'v_578_mushroom_beam', name: 'Mushroom Beam', decor: true, opacity: 0, pick: 0, mapColor: '#575340', drop: null as unknown as string, vanilla: { sheet: 578, frame: 'auto' } });
363	
364	// cleared 组补全（藤蔓/荆棘，原版 51/52/62/69）
365	def({ key: 'v_52_vines', name: 'Vines', decor: true, opacity: 0, pick: 0, mapColor: '#3E7A2E', drop: null as unknown as string, vanilla: { sheet: 52, frame: 'auto' } });
366	def({ key: 'v_62_jungle_vines', name: 'Jungle Vines', decor: true, opacity: 0, pick: 0, mapColor: '#2E8B3D', drop: null as unknown as string, vanilla: { sheet: 62, frame: 'auto' } });
367	def({ key: 'v_69_jungle_thorns', name: 'Jungle Thorns', decor: true, opacity: 0, pick: 0, mapColor: '#4A5E3E', drop: null as unknown as string, vanilla: { sheet: 69, frame: 'auto' } });
368	
369	// ===================== FTW_V2 兼容补全 =====================
370	def({ key: 'v_625_neon_moss_block', name: 'Neon Moss Block', solid: true, opacity: 1, pick: 0, mapColor: '#906094', blend: true, drop: null as unknown as string, vanilla: { sheet: 625, frame: 'auto' } });
371	def({ key: 'v_151_sandstone_brick', name: 'Sandstone Brick', solid: true, opacity: 1, pick: 0, mapColor: '#BEAB5E', blend: true, drop: null as unknown as string, vanilla: { sheet: 151, frame: 'auto' } });
372	def({ key: 'v_234_crimsand_block', name: 'Crimsand Block', solid: true, opacity: 1, pick: 0, mapColor: '#352C29', blend: true, drop: null as unknown as string, vanilla: { sheet: 234, frame: 'auto' } });
373	def({ key: 'v_182_blue_moss_block', name: 'Blue Moss Block', solid: true, opacity: 1, pick: 0, mapColor: '#2B568C', blend: true, drop: null as unknown as string, vanilla: { sheet: 182, frame: 'auto' } });
374	def({ key: 'v_205_crimson_vines', name: 'Crimson Vines', solid: true, opacity: 1, pick: 0, mapColor: '#BA3234', blend: true, drop: null as unknown as string, vanilla: { sheet: 205, frame: 'auto' } });
375	def({ key: 'v_45_gold_brick', name: 'Gold Brick', solid: true, opacity: 1, pick: 0, mapColor: '#B9A417', blend: true, drop: null as unknown as string, vanilla: { sheet: 45, frame: 'auto' } });
376	def({ key: 'v_399_crimson_hardened_sand_block', name: 'Crimson Hardened Sand Block', solid: true, opacity: 1, pick: 0, mapColor: '#4D4C42', blend: true, drop: null as unknown as string, vanilla: { sheet: 399, frame: 'auto' } });
377	def({ key: 'v_352_crimtane_thorns', name: 'Crimtane Thorns', solid: true, opacity: 1, pick: 0, mapColor: '#EE615E', blend: true, drop: null as unknown as string, vanilla: { sheet: 352, frame: 'auto' } });
378	def({ key: 'v_248_palladium_column', name: 'Palladium Column', solid: true, opacity: 1, pick: 0, mapColor: '#DB4726', blend: true, drop: null as unknown as string, vanilla: { sheet: 248, frame: 'auto' } });
379	def({ key: 'v_340_living_cursed_fire_block', name: 'Living Cursed Fire Block', solid: true, opacity: 1, pick: 0, mapColor: '#60F802', blend: true, drop: null as unknown as string, vanilla: { sheet: 340, frame: 'auto' } });
380	def({ key: 'v_207_water_fountains', name: 'Water Fountains', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 4, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 207, frame: 'style', fw: 2, fh: 4 } });
381	def({ key: 'v_144_timers', name: 'Timers', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 144, frame: 'style', fw: 1, fh: 1 } });
382	def({ key: 'v_475_hat_rack', name: 'Hat Rack', solid: false, framed: true, opacity: 0.05, pick: 0, w: 3, h: 4, mapColor: '#6B4F3B', drop: null as unknown as string, vanilla: { sheet: 475, frame: 'style', fw: 3, fh: 4 } });
383	def({ key: 'v_175_tin_brick', name: 'Tin Brick', solid: true, opacity: 1, pick: 0, mapColor: '#817D5D', blend: true, drop: null as unknown as string, vanilla: { sheet: 175, frame: 'auto' } });
384	def({ key: 'v_132_lever', name: 'Lever', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 132, frame: 'style', fw: 2, fh: 2 } });
385	
386	// ===================== 不负责任的女妖啤酒厂 兼容补全 =====================
387	def({ key: 'v_539_argon_moss_block', name: 'Argon Moss Block', solid: true, opacity: 1, pick: 0, mapColor: '#9A6387', blend: true, drop: null as unknown as string, vanilla: { sheet: 539, frame: 'auto' } });
388	def({ key: 'v_481_cracked_blue_brick', name: 'Cracked Blue Brick', solid: true, opacity: 1, pick: 0, mapColor: '#383E50', blend: true, drop: null as unknown as string, vanilla: { sheet: 481, frame: 'auto' } });
389	def({ key: 'v_120_mudstone_brick', name: 'Mudstone Brick', solid: true, opacity: 1, pick: 0, mapColor: '#5C4449', blend: true, drop: null as unknown as string, vanilla: { sheet: 120, frame: 'auto' } });
390	def({ key: 'v_714_spider_boulder', name: 'Spider Boulder', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#7ad9e8', drop: null as unknown as string, vanilla: { sheet: 714, frame: 'style', fw: 2, fh: 2 } });
391	def({ key: 'v_752_chillet_egg', name: 'Chillet Egg', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#7ad9e8', drop: null as unknown as string, vanilla: { sheet: 752, frame: 'style', fw: 2, fh: 2 } });
392	def({ key: 'v_751_sleeping_digtoise', name: 'Sleeping Digtoise', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#baa854', drop: null as unknown as string, vanilla: { sheet: 751, frame: 'style', fw: 2, fh: 2 } });
393	def({ key: 'v_664_bouncy_boulder', name: 'Bouncy Boulder', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#497811', drop: null as unknown as string, vanilla: { sheet: 664, frame: 'style', fw: 2, fh: 2 } });
394	def({ key: 'v_711_rainbow_boulder', name: 'Rainbow Boulder', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#b6af82', drop: null as unknown as string, vanilla: { sheet: 711, frame: 'style', fw: 2, fh: 2 } });
395	def({ key: 'v_715_ghoulder', name: 'Ghoulder', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#7ad9e8', drop: null as unknown as string, vanilla: { sheet: 715, frame: 'style', fw: 2, fh: 2 } });
396	def({ key: 'v_716_friendly_boulder', name: 'Friendly Boulder', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#7ad9e8', drop: null as unknown as string, vanilla: { sheet: 716, frame: 'style', fw: 2, fh: 2 } });
397	def({ key: 'v_713_lava_boulder', name: 'Lava Boulder', solid: true, framed: true, opacity: 1, pick: 0, w: 2, h: 2, mapColor: '#7ad9e8', drop: null as unknown as string, vanilla: { sheet: 713, frame: 'style', fw: 2, fh: 2 } });
398	
399	// ===================== wld 独立映射修复（原为错误复用） =====================
400	def({ key: 'v_23_corrupt_grass_block', name: 'Corrupt Grass Block', solid: true, opacity: 1, pick: 0, mapColor: '#8D89DF', blend: true, drop: null as unknown as string, vanilla: { sheet: 23, frame: 'auto' } });
401	def({ key: 'v_31_orb_heart', name: 'Orb Heart', solid: true, opacity: 1, pick: 0, mapColor: '#8D78A8', blend: true, drop: null as unknown as string, vanilla: { sheet: 31, frame: 'auto' } });
402	def({ key: 'v_41_blue_brick', name: 'Blue Brick', solid: true, opacity: 1, pick: 0, mapColor: '#42546D', blend: true, drop: null as unknown as string, vanilla: { sheet: 41, frame: 'auto' } });
403	def({ key: 'v_75_obsidian_brick', name: 'Obsidian Brick', solid: true, opacity: 1, pick: 0, mapColor: '#242424', blend: true, drop: null as unknown as string, vanilla: { sheet: 75, frame: 'auto' } });
404	def({ key: 'v_199_crimson_grass_block', name: 'Crimson Grass Block', solid: true, opacity: 1, pick: 0, mapColor: '#D05050', blend: true, drop: null as unknown as string, vanilla: { sheet: 199, frame: 'auto' } });
405	def({ key: 'v_60_jungle_grass_block', name: 'Jungle Grass Block', solid: true, opacity: 1, pick: 0, mapColor: '#8FD71D', blend: true, drop: null as unknown as string, vanilla: { sheet: 60, frame: 'auto' } });
406	def({ key: 'v_70_mushroom_grass_block', name: 'Mushroom Grass Block', solid: true, opacity: 1, pick: 0, mapColor: '#5D7FFF', blend: true, drop: null as unknown as string, vanilla: { sheet: 70, frame: 'auto' } });
407	
408	def({ key: 'v_25_ebonstone_block', name: 'Ebonstone Block', solid: true, opacity: 1, pick: 0, mapColor: '#6D5A80', blend: true, drop: null as unknown as string, vanilla: { sheet: 25, frame: 'auto' } });
409	def({ key: 'v_202_sunplate_block', name: 'Sunplate Block', solid: true, opacity: 1, pick: 0, mapColor: '#D5B21C', blend: true, drop: null as unknown as string, vanilla: { sheet: 202, frame: 'auto' } });
410	def({ key: 'v_71_mushroom_plant', name: 'Mushroom Plant', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#B6AF82', drop: null as unknown as string, vanilla: { sheet: 71, frame: 'style', fw: 1, fh: 1 } });
411	def({ key: 'v_24_corruption_short_plants', name: 'Corruption Short Plants', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#7A74DA', drop: null as unknown as string, vanilla: { sheet: 24, frame: 'style', fw: 1, fh: 1 } });
412	def({ key: 'v_32_corruption_thorns', name: 'Corruption Thorns', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#9787B7', drop: null as unknown as string, vanilla: { sheet: 32, frame: 'style', fw: 1, fh: 1 } });
413	def({ key: 'v_27_sunflower', name: 'Sunflower', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 4, mapColor: '#E2C431', drop: null as unknown as string, vanilla: { sheet: 27, frame: 'style', fw: 2, fh: 4 } });
414	def({ key: 'v_5_trees', name: 'Trees', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#6B4A2B', drop: null as unknown as string, vanilla: { sheet: 5, frame: 'style', fw: 1, fh: 1 } });
415	def({ key: 'v_80_cactus', name: 'Cactus Plant', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#5A7A3A', drop: null as unknown as string, vanilla: { sheet: 80, frame: 'style', fw: 1, fh: 1 } });
416	
417	def({ key: 'v_44_pink_brick', name: 'Pink Brick', solid: true, opacity: 1, pick: 0, mapColor: '#6B4463', blend: true, drop: null as unknown as string, vanilla: { sheet: 44, frame: 'auto' } });
418	def({ key: 'v_203_crimstone_block', name: 'Crimstone Block', solid: true, opacity: 1, pick: 0, mapColor: '#802C2D', blend: true, drop: null as unknown as string, vanilla: { sheet: 203, frame: 'auto' } });
419	def({ key: 'v_201_crimson_short_plants', name: 'Crimson Short Plants', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#CB3D40', drop: null as unknown as string, vanilla: { sheet: 201, frame: 'style', fw: 1, fh: 1 } });
420	
421	// 所有 def() 注册完毕后统一回填 key→id 映射（必须位于文件末尾）
422	TILE_DEFS.forEach((d, i) => (TILE_BY_KEY[d.key] = i));
423	

```


---

## 🤖 Assistant · 2026-08-07T05:46:10.703Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game ~/Project/GLM/SandboxWorld/game/src ~/Project/GLM/SandboxWorld/game/src/render ~/Project/GLM/SandboxWorld/game/src/wld",
 "description": "List project directories"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:10.736Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game:
dist
index.html
node_modules
package-lock.json
package.json
public
scripts
shots
src
Starter_World Master.wld
tests
tsconfig.json

~/Project/GLM/SandboxWorld/game/src:
assets
core
data
entities
items
lighting
main.ts
physics
render
save
stats
ui
wld
world

~/Project/GLM/SandboxWorld/game/src/render:
AutoTiler.ts
Camera.ts
ChunkCache.ts
Renderer.ts
SkyRenderer.ts
VanillaTiler.ts
WallTiler.ts

~/Project/GLM/SandboxWorld/game/src/wld:
BinaryReaderLE.ts
WldImport.ts
WldParser.ts

```


---

## 🤖 Assistant · 2026-08-07T05:46:13.546Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I'm a read-only search agent; plan mode doesn't change my task much — I just need to read files and report. Continue reading ChunkCache.ts, WldImport.ts (WALL_MAP), WldParser.ts, vanilla.json, VANILLA_MISC.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:46:13.959Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:13.966Z

**📎 ToolResult**

```
1	// chunk 静态缓存：每 chunk 16×16 tile 预渲染到离屏 canvas（墙层+tile 层）
2	import { CHUNK, TILE } from '../core/constants';
3	import { T, TILE_DEFS, WALL_DEFS, TILE_BY_KEY } from '../data/tiles';
4	import { hash2 } from '../core/rng';
5	import { drawVanillaCell, drawTreeCell } from './VanillaTiler';
6	import { shade } from '../assets/Palette';
7	import type { TileSheetEntry } from '../assets/TileSheetGen';
8	import type { AutoTiler } from './AutoTiler';
9	import type { WallTiler } from './WallTiler';
10	import type { World } from '../world/World';
11	
12	// 我们的 tile → Maples RuleTile 规则名（有规则的走素材自动贴合，无规则回退程序化）
13	// Grass 走人工标注（'@grass'）：Tiles_2.png 是多 tile 混排图集，自动分类不可靠；
14	// 用 public/annotator.html 标注后写入 sprites/annotations.json。无标注时回退程序化。
15	const TILE_RULES: Record<number, string> = {
16	  1: 'Dirt', 2: 'Stone', 3: '@grass', 5: 'Iron', 8: 'Tree',
17	  13: '工作台', 14: '熔炉', 15: '铁砧',
18	};
19	
20	export interface ChunkPair {
21	  wall: HTMLCanvasElement;   // 背景墙层（水画在它之上）
22	  tile: HTMLCanvasElement;   // 前景 tile/物体层（画在水之上）
23	}
24	
25	export class ChunkCache {
26	  chunks = new Map<number, ChunkPair>();
27	  dirtyQueue: number[] = [];
28	  sheets: Map<number, TileSheetEntry>;
29	  world: World;
30	  autotiler: AutoTiler | null;
31	  wallTilers: Map<number, WallTiler>;
32	
33	  constructor(world: World, sheets: Map<number, TileSheetEntry>, autotiler: AutoTiler | null = null, wallTilers: Map<number, WallTiler> = new Map()) {
34	    this.world = world;
35	    this.sheets = sheets;
36	    this.autotiler = autotiler;
37	    this.wallTilers = wallTilers;
38	    world.store.onTileChanged((x, y) => this.markDirtyAround(x, y));
39	  }
40	
41	  static key(cx: number, cy: number): number {
42	    return (cx & 0xffff) | ((cy & 0xffff) << 16);
43	  }
44	
45	  markDirty(cx: number, cy: number) {
46	    const k = ChunkCache.key(cx, cy);
47	    if (!this.chunks.has(k)) return; // 未生成的 chunk 惰性创建
48	    this.chunks.set(k, undefined as unknown as ChunkPair); // 标记删除，重绘时重建
49	    if (!this.dirtyQueue.includes(k)) this.dirtyQueue.push(k);
50	  }
51	
52	  /** 区域标脏（tile 范围）：供树冠等大范围精灵清理使用 */
53	  markDirtyArea(x0: number, y0: number, x1: number, y1: number) {
54	    for (let cy = Math.floor(y0 / CHUNK); cy <= Math.floor(y1 / CHUNK); cy++) {
55	      for (let cx = Math.floor(x0 / CHUNK); cx <= Math.floor(x1 / CHUNK); cx++) {
56	        if (cx < 0 || cy < 0) continue;
57	        this.markDirty(cx, cy);
58	      }
59	    }
60	  }
61	
62	  markDirtyAround(x: number, y: number) {
63	    const cx = Math.floor(x / CHUNK), cy = Math.floor(y / CHUNK);
64	    this.markDirty(cx, cy);
65	    // 边缘融合：邻接 chunk 也要标脏
66	    if (x % CHUNK === 0) this.markDirty(cx - 1, cy);
67	    if (x % CHUNK === CHUNK - 1) this.markDirty(cx + 1, cy);
68	    if (y % CHUNK === 0) this.markDirty(cx, cy - 1);
69	    if (y % CHUNK === CHUNK - 1) this.markDirty(cx, cy + 1);
70	  }
71	
72	  /** 每帧最多重绘 maxN 个脏 chunk */
73	  flushDirty(maxN = 4) {
74	    let n = 0;
75	    while (this.dirtyQueue.length && n < maxN) {
76	      const k = this.dirtyQueue.shift()!;
77	      const cx = k & 0xffff, cy = (k >> 16) & 0xffff;
78	      if (this.chunks.get(k) !== undefined) continue; // 已重建
79	      this.get(cx, cy);
80	      n++;
81	    }
82	  }
83	
84	  /** 取 chunk 双层画布（惰性生成） */
85	  get(cx: number, cy: number): ChunkPair {
86	    const k = ChunkCache.key(cx, cy);
87	    let c = this.chunks.get(k);
88	    if (c) return c;
89	    c = this.renderChunk(cx, cy);
90	    this.chunks.set(k, c);
91	    return c;
92	  }
93	
94	  /** 树枝判定：TREE 且上下皆非 TREE、恰好一侧为 TREE（横向独连树干）。
95	   *  下方是实心地面的属于树根底座 —— 走规则表渲染底座贴图，不算枝干 */
96	  private isBranchTile(st: World['store'], x: number, y: number): boolean {
97	    const at = (ax: number, ay: number) => st.inBounds(ax, ay) && st.type[st.idx(ax, ay)] === T.TREE;
98	    const up = at(x, y - 1), dn = at(x, y + 1), lf = at(x - 1, y), rt = at(x + 1, y);
99	    return !up && !dn && lf !== rt && !st.isSolid(x, y + 1);
100	  }
101	
102	  private neighborMask(x: number, y: number, type: number): number {
103	    const st = this.world.store;
104	    let mask = 0;
105	    const same = (nx: number, ny: number) => st.inBounds(nx, ny) && st.type[st.idx(nx, ny)] === type ? 1 : 0;
106	    mask |= same(x, y - 1);        // N
107	    mask |= same(x + 1, y) << 1;   // E
108	    mask |= same(x, y + 1) << 2;   // S
109	    mask |= same(x - 1, y) << 3;   // W
110	    mask |= same(x + 1, y - 1) << 4; // NE
111	    mask |= same(x + 1, y + 1) << 5; // SE
112	    mask |= same(x - 1, y + 1) << 6; // SW
113	    mask |= same(x - 1, y - 1) << 7; // NW
114	    return mask;
115	  }
116	
117	  private renderChunk(cx: number, cy: number): ChunkPair {
118	    // 双层画布：墙层 / tile 层分离 —— 水渲染在两层之间（墙之上、图块之下）
119	    const wall = document.createElement('canvas');
120	    wall.width = CHUNK * TILE; wall.height = CHUNK * TILE;
121	    const tile = document.createElement('canvas');
122	    tile.width = CHUNK * TILE; tile.height = CHUNK * TILE;
123	    let ctx = wall.getContext('2d')!;
124	    ctx.imageSmoothingEnabled = false;
125	    const st = this.world.store;
126	    const x0 = cx * CHUNK, y0 = cy * CHUNK;
127	
128	    // ---- 第一遍：背景墙全部先画（避免后格的墙盖住跨格物体如宝箱/树冠）----
129	    for (let ly = 0; ly < CHUNK; ly++) {
130	      for (let lx = 0; lx < CHUNK; lx++) {
131	        const x = x0 + lx, y = y0 + ly;
132	        if (!st.inBounds(x, y)) continue;
133	        const i = st.idx(x, y);
134	        const px = lx * TILE, py = ly * TILE;
135	
136	        // 背景墙：原版"骰子5"（梅花/丁砌）排布
137	        const wall = st.wall[i];
138	        if (wall !== 0) {
139	          const wallTiler = this.wallTilers.get(wall);
140	          if (wallTiler) {
141	            // 砖锚点：行对齐 2 格；行序 (y&2) 决定横向错开 0/1 格
142	            const by = y & ~1;
143	            const rowOff = (y & 2) >> 1;
144	            const bx = ((x - rowOff) & ~1) + rowOff;
145	            const qx = x - bx, qy = y - by; // 0/1 象限
146	            // 砖四侧封闭状态（周界任一格有同类墙即封闭）
147	            const wAt = (xx: number, yy: number) => (st.inBounds(xx, yy) ? st.wall[st.idx(xx, yy)] : 0);
148	            const same = (v: number) => v === wall;
149	            const cellClosed: [boolean, boolean, boolean, boolean] = [
150	              same(wAt(x, y - 1)),   // 上
151	              same(wAt(x + 1, y)),   // 右
152	              same(wAt(x, y + 1)),   // 下
153	              same(wAt(x - 1, y)),   // 左
154	            ];
155	            const allClosed = cellClosed[0] && cellClosed[1] && cellClosed[2] && cellClosed[3];
156	            if (allClosed) {
157	              // 内墙：梅花格连续图案按世界坐标取样（双轴交错的骰子5排布）
158	              const pat = wallTiler.patternSample(x, y);
159	              if (pat) {
160	                ctx.drawImage(pat.canvas, pat.sx, pat.sy, TILE, TILE, px, py, TILE, TILE);
161	              }
162	            } else {
163	              // 边界格：按砖锚点敞开方向选收窄变体，画对应象限
164	              const closed: [boolean, boolean, boolean, boolean] = [
165	                same(wAt(bx, by - 1)) || same(wAt(bx + 1, by - 1)),   // 上
166	                same(wAt(bx + 2, by)) || same(wAt(bx + 2, by + 1)),   // 右
167	                same(wAt(bx, by + 2)) || same(wAt(bx + 1, by + 2)),   // 下
168	                same(wAt(bx - 1, by)) || same(wAt(bx - 1, by + 1)),   // 左
169	              ];
170	              const r = wallTiler.pick(closed, bx, by)
171	                ?? wallTiler.pick([false, false, false, false], x, y);
172	              if (r) {
173	                const hw = r.sw / 2, hh = r.sh / 2;
174	                ctx.drawImage(r.img, r.sx + qx * hw, r.sy + qy * hh, hw, hh, px, py, TILE, TILE);
175	              }
176	            }
177	          } else {
178	            const wd = WALL_DEFS[wall];
179	            ctx.fillStyle = wd.mapColor;
180	            ctx.fillRect(px, py, TILE, TILE);
181	            ctx.fillStyle = shade(wd.mapColor, 0.8);
182	            ctx.fillRect(px, py + TILE - 1, TILE, 1);
183	            ctx.fillRect(px + TILE - 1, py, 1, TILE);
184	          }
185	        }
186	      }
187	    }
188	
189	    // ---- 第二遍：前景 tile / 物体（绘制到 tile 层画布；水渲染在墙层与 tile 层之间）----
190	    ctx = tile.getContext('2d')!;
191	    ctx.imageSmoothingEnabled = false;
192	    for (let ly = 0; ly < CHUNK; ly++) {
193	      for (let lx = 0; lx < CHUNK; lx++) {
194	        const x = x0 + lx, y = y0 + ly;
195	        if (!st.inBounds(x, y)) continue;
196	        const i = st.idx(x, y);
197	        const px = lx * TILE, py = ly * TILE;
198	        const type = st.type[i];
199	        if (type === 0) continue;
200	        const def = TILE_DEFS[type];
201	        if (!def) { ctx.fillStyle = '#808080'; ctx.fillRect(px, py, TILE, TILE); continue; }
202	        // 树枝：TREE 且仅横向连接树干 → 跳过常规路径（第二遍半按 pivot 锚定专用绘制，
203	        // 规则表变体池混有树干碎片贴图，hash 选变体会 50% 画出残片）
204	        if (type === T.TREE && this.isBranchTile(st, x, y)) continue;
205	        // 原版素材图块（TileDef.vanilla）：TEdit framing 查找表（auto）或显式 18px 帧（style）
206	        if (def.vanilla && this.autotiler) {
207	          drawVanillaCell(
208	            ctx, this.autotiler.atlas, def.vanilla.sheet, def.vanilla.frame,
209	            def.vanilla.fw ?? 1, def.vanilla.fh ?? 1,
210	            st, x, y, type,
211	            (t) => t === type, // 同 id 融合判定（后续可扩 mergeWith）
212	            px, py, st.frameX[i], st.frameY[i],
213	          );
214	          continue;
215	        }
216	        // 树苗：Tree_Bodys 树干段作小苗（底部对齐）
217	        if (type === T.SAPLING && this.autotiler) {
218	          const r = this.autotiler.saplingSprite(x, y);
219	          if (r) {
220	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px + (TILE - r.sw) / 2, py + TILE - r.sh, r.sw, r.sh);
221	            continue;
222	          }
223	        }
224	        // 杂草：Maples Tiles_3 杂草贴图（16×20，底部对齐，hash 选变体）
225	        if (type === T.TALLGRASS && this.autotiler) {
226	          const r = this.autotiler.weedSprite(x, y);
227	          if (r) {
228	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px - (r.sw - TILE) / 2, py + TILE - r.sh, r.sw, r.sh);
229	            continue;
230	          }
231	        }
232	        // 有 RuleTile 规则的 tile 用 Maples 素材自动贴合
233	        const ruleName = this.autotiler ? TILE_RULES[type] : undefined;
234	        if (ruleName && this.autotiler) {
235	          // 草皮覆盖件：保持原生透明（缺口露出背后的墙/天空），不做任何垫底/填充
236	          if (ruleName === '@grass') {
237	            const r = this.autotiler.tile(ruleName, st, x, y, type);
238	            if (r) ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px, py, TILE, TILE);
239	            continue;
240	          }
241	          const r = this.autotiler.tile(ruleName, st, x, y, type);
242	          if (r) {
243	            // 大图（树冠 80×80，宽>2格）跳过 —— 第三遍统一绘制（跨 chunk 补全 + 树叶盖树干）
244	            if (r.sw > TILE * 2) continue;
245	            // 按精灵原始尺寸绘制。树干等"宽≤2格、高>1格"的竖向件顶部对齐：
246	            // 溢出向下伸，由更下方的格（后画）覆盖 —— 下层不压上层。
247	            let dy = py + (TILE - r.sh) / 2;
248	            if (r.sh > TILE && r.sw <= TILE * 2) dy = py;
249	            const dx = px + (TILE - r.sw) / 2;
250	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, dx, dy, r.sw, r.sh);
251	            continue;
252	          }
253	        }
254	        const entry = this.sheets.get(type);
255	        if (!entry) {
256	          ctx.fillStyle = '#FF00FF';
257	          ctx.fillRect(px, py, TILE, TILE);
258	          continue;
259	        }
260	        if (entry.kind === 'blend') {
261	          const mask = this.neighborMask(x, y, type);
262	          const col = mask & 15, row = mask >> 4;
263	          ctx.drawImage(entry.canvas, col * TILE, row * TILE, TILE, TILE, px, py, TILE, TILE);
264	        } else if (entry.kind === 'object') {
265	          // 仅锚点绘制整体
266	          if (st.frameX[i] === 0 && st.frameY[i] === 0) {
267	            const w = (entry.w ?? 1) * TILE, h = (entry.h ?? 1) * TILE;
268	            ctx.drawImage(entry.canvas, px, py, w, h);
269	          }
270	        } else {
271	          // single：帧偏移直接取
272	          ctx.drawImage(entry.canvas, st.frameX[i], st.frameY[i], TILE, TILE, px, py, TILE, TILE);
273	        }
274	      }
275	    }
276	    // ---- 第二遍半：树枝（pivot 锚定专用绘制） ----
277	    // Unity 切片 pivot：左向枝 0/2/4 = x0.8，右向枝 1/3/5 = x0.2（pivot 对齐格子中心），
278	    // 按 0.5 居中画会整体偏移 12-24px。外扩扫描防跨 chunk 裁剪（右向枝外伸 24px）。
279	    if (this.autotiler) {
280	      const EXT = 3;
281	      for (let ty = y0 - EXT; ty < y0 + CHUNK + EXT; ty++) {
282	        for (let tx = x0 - EXT; tx < x0 + CHUNK + EXT; tx++) {
283	          if (!st.inBounds(tx, ty)) continue;
284	          if (st.type[st.idx(tx, ty)] !== T.TREE) continue;
285	          if (!this.isBranchTile(st, tx, ty)) continue;
286	          // 树干在右 → 左向枝；树干在左 → 右向枝。
287	          // 只用朝上变体：_1/_4 的美术在下半部（下垂朝地），正常枝干应朝上
288	          const left = st.type[st.idx(tx + 1, ty)] === T.TREE;
289	          const names = left ? ['Tree_Branches_0', 'Tree_Branches_2']
290	            : ['Tree_Branches_3', 'Tree_Branches_5'];
291	          const name = names[Math.floor(hash2(tx, ty, 71) * names.length) % names.length];
292	          const r = this.autotiler.atlas.rect('地形/Tree_Branches.png', name);
293	          if (!r) continue;
294	          const pivX = left ? 0.8 : 0.2;
295	          const pivY = name === 'Tree_Branches_2' ? 0.475 : name === 'Tree_Branches_5' ? 0.4 : 0.5;
296	          const dx = tx * TILE + TILE / 2 - pivX * r.sw - x0 * TILE;
297	          const dy = ty * TILE + TILE / 2 - pivY * r.sh - y0 * TILE;
298	          ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, dx, dy, r.sw, r.sh);
299	        }
300	      }
301	    }
302	
303	    // ---- 第三遍：树冠大图最上层 ----
304	    // 扫描本 chunk 及外扩 5 格的树顶格（上空气、下树干），绘制整幅树冠。
305	    // 外扩保证树冠跨 chunk 时不被裁剪（右边缺一块/头上缺一块的根因）。
306	    if (this.autotiler) {
307	      const EXT = 5;
308	      for (let ty = y0 - EXT; ty < y0 + CHUNK + EXT; ty++) {
309	        for (let tx = x0 - EXT; tx < x0 + CHUNK + EXT; tx++) {
310	          if (!st.inBounds(tx, ty)) continue;
311	          if (st.type[st.idx(tx, ty)] !== T.TREE) continue;
312	          if (st.inBounds(tx, ty - 1) && st.type[st.idx(tx, ty - 1)] === T.TREE) continue; // 非树顶
313	          if (!st.inBounds(tx, ty + 1) || st.type[st.idx(tx, ty + 1)] !== T.TREE) continue; // 下方须为树干
314	          const r = this.autotiler.tile('Tree', st, tx, ty, T.TREE);
315	          if (!r || r.sw <= TILE * 2) continue;
316	          const wx = tx * TILE, wy = ty * TILE; // 世界像素
317	          const dx = wx + (TILE - r.sw) / 2 - x0 * TILE;
318	          const dy = wy + (TILE - r.sh) / 2 - y0 * TILE;
319	          ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, dx, dy, r.sw, r.sh);
320	        }
321	      }
322	    }
323	
324	    // ---- 第四遍：原版树冠/树枝（tile 5 标记帧，跨 chunk 外扩绘制） ----
325	    // 树冠 80×80 / 树枝 40×40 跨多格，主遍跳过这些标记帧，由此外扩遍统一绘制防裁剪
326	    if (this.autotiler) {
327	      const v5 = TILE_BY_KEY['v_5_trees'];
328	      if (v5 !== undefined) {
329	        const EXT = 6;
330	        for (let ty = y0 - EXT; ty < y0 + CHUNK + EXT; ty++) {
331	          for (let tx = x0 - EXT; tx < x0 + CHUNK + EXT; tx++) {
332	            if (!st.inBounds(tx, ty)) continue;
333	            const i = st.idx(tx, ty);
334	            if (st.type[i] !== v5) continue;
335	            const fx = st.frameX[i], fy = st.frameY[i];
336	            if (fy < 198 || fx < 22) continue; // 树干由主遍绘制
337	            drawTreeCell(ctx, this.autotiler.atlas, st, tx, ty, fx, fy,
338	              tx * TILE - x0 * TILE, ty * TILE - y0 * TILE, true);
339	          }
340	        }
341	      }
342	    }
343	
344	    return { wall, tile };
345	  }
346	}
347	

```


---

## 🤖 Assistant · 2026-08-07T05:46:13.978Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:13.989Z

**📎 ToolResult**

```
1	// .wld 地图解析器（Terraria 1.4+，version >= 210）
2	// 格式参考 TEdit（Terraria-Map-Editor）的 World.FileV2.cs，此处为独立 TS 实现。
3	// 只支持读取：section header / header flags / tiles（RLE）/ chests / town npcs。
4	// bestiary 等尾部 section 通过 sectionPointers 跳过，不做 footer 校验。
5	import { BinaryReaderLE } from './BinaryReaderLE';
6	
7	export interface WldTileData {
8	  active: Uint8Array;    // active 标志（dirt 的 id 是 0，必须用此数组区分空气）
9	  type: Uint16Array;
10	  frameX: Uint16Array;
11	  frameY: Uint16Array;
12	  wall: Uint16Array;
13	  liquid: Uint8Array;
14	  liquidType: Uint8Array; // 1水 2岩浆 3蜂蜜
15	}
16	
17	export interface WldChest { x: number; y: number; name: string; items: Array<{ id: number; stack: number } | null>; }
18	export interface WldNPC { spriteId: number; name: string; x: number; y: number; homeX: number; homeY: number; }
19	
20	export interface WldWorld {
21	  version: number;
22	  title: string;
23	  seed: string;
24	  tilesWide: number;
25	  tilesHigh: number;
26	  spawnX: number;
27	  spawnY: number;
28	  groundLevel: number;
29	  rockLevel: number;
30	  time: number;
31	  dayTime: boolean;
32	  isCrimson: boolean;
33	  hardMode: boolean;
34	  tiles: WldTileData;
35	  chests: WldChest[];
36	  npcs: WldNPC[];
37	}
38	
39	export class WldParseError extends Error {}
40	
41	export function parseWld(buf: Uint8Array): WldWorld {
42	  const r = new BinaryReaderLE(buf);
43	  const version = r.u32();
44	  if (version < 210) {
45	    throw new WldParseError(`不支持的世界文件版本 ${version}（需要 1.4+，version >= 210）。请在游戏中重新保存该地图。`);
46	  }
47	  if (version >= 140) {
48	    // header magic（中文版为不同常量，这里宽放校验）
49	    const magic = new TextDecoder().decode(r.bytes(7));
50	    const fileType = r.byte();
51	    // TEdit FileType 枚举：None=0, Map=1, World=2, Player=3
52	    if (fileType !== 2) throw new WldParseError(`不是世界文件（fileType=${fileType}）`);
53	    if (magic !== 'relogic') {
54	      // 宽放：中文版魔数，只要不是明显非法就继续
55	      if (!/^[a-z]{7}$/i.test(magic)) throw new WldParseError(`无效的文件头魔数: "${magic}"`);
56	    }
57	    r.u32(); // revision
58	    r.u64(); // favorite flags
59	  }
60	  const sectionCount = r.i16();
61	  const pointers: number[] = [];
62	  for (let i = 0; i < sectionCount; i++) pointers.push(r.i32());
63	  // tileFrameImportant 位图（TEdit ReadBitArray：每字节 LSB 在前）
64	  const bitLen = r.i16();
65	  const frameImportant: boolean[] = new Array(bitLen);
66	  {
67	    let data = 0;
68	    for (let i = 0; i < bitLen; i++) {
69	      if ((i & 7) === 0) data = r.byte();
70	      frameImportant[i] = ((data >> (i & 7)) & 1) !== 0;
71	    }
72	  }
73	
74	  // ---- header flags ----
75	  r.seek(pointers[0]);
76	  const title = r.string();
77	  let seed = '';
78	  if (version >= 179) {
79	    seed = version === 179 ? String(r.i32()) : r.string();
80	    r.u64(); // worldGenVersion
81	  }
82	  if (version >= 181) r.bytes(16); // guid
83	  r.i32(); // worldId
84	  r.i32(); r.i32(); r.i32(); r.i32(); // bounds
85	  const tilesHigh = r.i32();
86	  const tilesWide = r.i32();
87	  // gameMode
88	  if (version >= 209) {
89	    r.i32();
90	    if (version >= 222) r.boolean(); // drunk
91	    if (version >= 227) r.boolean(); // good
92	    if (version >= 238) r.boolean();
93	    if (version >= 239) r.boolean();
94	    if (version >= 241) r.boolean();
95	    if (version >= 249) r.boolean(); // remix
96	    if (version >= 266) r.boolean(); // notraps
97	    if (version >= 267) r.boolean(); // zenith
98	    if (version >= 302) r.boolean(); // skyblock
99	  } else if (version === 208 || version >= 112) {
100	    r.boolean();
101	  }
102	  if (version >= 141) r.i64(); // creationTime
103	  if (version >= 284) r.i64(); // lastPlayed
104	  r.u8(); // moonType
105	  for (let i = 0; i < 3; i++) r.i32(); // treeX
106	  for (let i = 0; i < 4; i++) r.i32(); // treeStyle
107	  for (let i = 0; i < 3; i++) r.i32(); // caveBackX
108	  for (let i = 0; i < 4; i++) r.i32(); // caveBackStyle
109	  r.i32(); r.i32(); r.i32(); // ice/jungle/hell back style
110	  const spawnX = r.i32();
111	  const spawnY = r.i32();
112	  const groundLevel = r.f64();
113	  const rockLevel = r.f64();
114	  const time = r.f64();
115	  const dayTime = r.boolean();
116	  r.i32(); // moonPhase
117	  r.boolean(); // blood moon
118	  r.boolean(); // eclipse
119	  r.i32(); r.i32(); // dungeon xy
120	  const isCrimson = r.boolean();
121	  for (let i = 0; i < 10; i++) r.boolean(); // downed bosses
122	  if (version >= 118) r.boolean(); // slime king
123	  for (let i = 0; i < 7; i++) r.boolean(); // saved goblin etc
124	  r.boolean(); r.boolean(); // orb smashed / spawn meteor
125	  r.u8(); // orb count
126	  r.i32(); // altar count
127	  const hardMode = r.boolean();
128	  if (version >= 257) r.boolean(); // party of doom
129	  r.i32(); r.i32(); r.i32(); r.f64(); // invasion
130	  if (version >= 118) r.f64(); // slime rain
131	  if (version >= 113) r.u8(); // sundial
132	  r.boolean(); r.i32(); r.f32(); // rain
133	  r.i32(); r.i32(); r.i32(); // ore tiers
134	  for (let i = 0; i < 8; i++) r.u8(); // bg styles
135	  r.i32(); r.i16(); r.f32(); // clouds/wind
136	  // angler
137	  {
138	    const n = r.i32();
139	    for (let i = 0; i < n; i++) r.string();
140	  }
141	  r.boolean(); // savedAngler
142	  r.i32(); // anglerQuest
143	  r.boolean(); // savedStylist
144	  if (version >= 140) r.boolean(); // tax collector
145	  if (version >= 201) r.boolean(); // golfer
146	  if (version >= 107) r.i32(); // invasionSizeStart
147	  if (version >= 108) r.i32(); // cultistDelay
148	  // banners
149	  {
150	    const n = r.i16();
151	    for (let i = 0; i < n; i++) r.i32();
152	    if (version >= 289) {
153	      const m = r.i16();
154	      for (let i = 0; i < m; i++) r.u16();
155	    }
156	  }
157	  if (version >= 140) r.boolean(); // fastForwardTime
158	  r.boolean(); // fishron
159	  if (version >= 140) { r.boolean(); r.boolean(); r.boolean(); } // martians/cultist/moonlord
160	  for (let i = 0; i < 5; i++) r.boolean(); // holiday bosses
161	  for (let i = 0; i < 4; i++) r.boolean(); // celestial downed
162	  for (let i = 0; i < 4; i++) r.boolean(); // celestial active
163	  r.boolean(); // apocalypse
164	  if (version >= 170) {
165	    r.boolean(); r.boolean(); r.i32();
166	    const n = r.i32();
167	    for (let i = 0; i < n; i++) r.i32();
168	  }
169	  if (version >= 174) { r.boolean(); r.i32(); r.f32(); r.f32(); }
170	  if (version >= 178) { r.boolean(); r.boolean(); r.boolean(); r.boolean(); }
171	  if (version > 194) r.u8(); // mushroom bg
172	  if (version >= 215) r.u8(); // underworld bg
173	  if (version >= 195) { r.u8(); r.u8(); r.u8(); }
174	  if (version >= 204) r.boolean(); // combat book
175	  if (version >= 207) { r.i32(); r.boolean(); r.boolean(); r.boolean(); }
176	  if (version >= 211) {
177	    const n = r.i32();
178	    for (let i = 0; i < n; i++) r.i32();
179	  }
180	  if (version >= 212) { r.boolean(); r.boolean(); }
181	  if (version >= 216) { r.i32(); r.i32(); r.i32(); r.i32(); }
182	  if (version >= 217) { r.boolean(); r.boolean(); r.boolean(); }
183	  if (version >= 223) { r.boolean(); r.boolean(); }
184	  if (version >= 240) r.boolean();
185	  if (version >= 250) r.boolean();
186	  if (version >= 251) { for (let i = 0; i < 8; i++) r.boolean(); }
187	  if (version >= 259) r.boolean();
188	  if (version >= 260) r.boolean();
189	  if (version >= 261) { for (let i = 0; i < 7; i++) r.boolean(); }
190	  if (version >= 264) { r.boolean(); r.u8(); }
191	  if (version >= 287) { r.boolean(); r.boolean(); }
192	  if (version >= 288) r.boolean();
193	  if (version >= 296) r.boolean();
194	  if (version >= 291) { r.i32(); r.i32(); }
195	  if (version >= 297) {
196	    r.boolean();
197	    const n = r.u8();
198	    for (let i = 0; i < n; i++) { r.i16(); r.i16(); }
199	  }
200	  if (version >= 304) r.boolean();
201	  if (version >= 299 && version < 313) r.u32();
202	  if (version >= 299) r.string(); // manifest
203	
204	  // ---- tiles ----
205	  if (pointers.length < 5) throw new WldParseError('section 数量不足，不是有效的 1.4 世界文件');
206	  r.seek(pointers[1]);
207	  const tiles = decodeTiles(r, tilesWide, tilesHigh, version, frameImportant);
208	
209	  // ---- chests ----
210	  r.seek(pointers[2]);
211	  const chests: WldChest[] = [];
212	  {
213	    const total = r.i16();
214	    let maxItems = 40;
215	    if (version < 294) maxItems = r.i16();
216	    for (let i = 0; i < total; i++) {
217	      const x = r.i32(), y = r.i32();
218	      const name = r.string();
219	      if (version >= 294) maxItems = r.i32();
220	      const items: Array<{ id: number; stack: number } | null> = [];
221	      for (let s = 0; s < maxItems; s++) {
222	        const stack = r.i16();
223	        if (stack > 0) {
224	          const id = r.i32();
225	          r.u8(); // prefix
226	          items.push({ id, stack });
227	        } else {
228	          items.push(null);
229	        }
230	      }
231	      chests.push({ x, y, name, items });
232	    }
233	  }
234	
235	  // ---- npcs ----
236	  r.seek(pointers[4]);
237	  const npcs: WldNPC[] = [];
238	  {
239	    if (version >= 268) {
240	      const n = r.i32();
241	      for (let i = 0; i < n; i++) r.i32();
242	    }
243	    while (r.boolean()) {
244	      const spriteId = version >= 190 ? r.i32() : 0;
245	      if (version < 190) r.string();
246	      const displayName = r.string();
247	      const x = r.f32(), y = r.f32();
248	      r.boolean(); // homeless
249	      const homeX = r.i32(), homeY = r.i32();
250	      if (version >= 213) {
251	        const flag = r.u8();
252	        if (flag & 1) r.i32();
253	      }
254	      if (version >= 315) r.boolean();
255	      npcs.push({ spriteId, name: displayName, x, y, homeX, homeY });
256	    }
257	  }
258	
259	  return {
260	    version, title, seed, tilesWide, tilesHigh, spawnX, spawnY,
261	    groundLevel, rockLevel, time, dayTime, isCrimson, hardMode,
262	    tiles, chests, npcs,
263	  };
264	}
265	
266	/** tiles 段解码：列优先 + header 链 + RLE */
267	function decodeTiles(
268	  r: BinaryReaderLE, w: number, h: number,
269	  version: number, frameImportant: boolean[],
270	): WldTileData {
271	  const n = w * h;
272	  const active = new Uint8Array(n);
273	  const type = new Uint16Array(n);
274	  const frameX = new Uint16Array(n);
275	  const frameY = new Uint16Array(n);
276	  const wall = new Uint16Array(n);
277	  const liquid = new Uint8Array(n);
278	  const liquidType = new Uint8Array(n);
279	
280	  let idx = 0; // y * w + x，列优先推进
281	  for (let x = 0; x < w; x++) {
282	    for (let y = 0; y < h; y++) {
283	      const header1 = r.u8();
284	      let header2 = 0, header3 = 0, header4 = 0;
285	      if (header1 & 0x01) header2 = r.u8();
286	      if (header2 & 0x01) header3 = r.u8();
287	      if (version >= 269 && header3 & 0x01) header4 = r.u8();
288	      void header4;
289	
290	      let tileType = 0;
291	      let fx = 0, fy = 0;
292	      if (header1 & 0x02) {
293	        // active
294	        if (header1 & 0x20) {
295	          tileType = r.u16();
296	        } else {
297	          tileType = r.u8();
298	        }
299	        const isFramed = tileType < frameImportant.length ? frameImportant[tileType] : true;
300	        if (isFramed) {
301	          fx = r.u16();
302	          fy = r.u16();
303	        }
304	        if (header3 & 0x08) r.u8(); // tile color
305	      }
306	      let wl = 0;
307	      if (header1 & 0x04) {
308	        wl = r.u8();
309	        if (header3 & 0x10) r.u8(); // wall color
310	        if (version >= 222 && header3 & 0x40) {
311	          wl |= r.u8() << 8;
312	        }
313	      }
314	      const lqType = (header1 & 0x18) >> 3;
315	      let lqAmount = 0, lqKind = 0;
316	      if (lqType !== 0) {
317	        lqAmount = r.u8();
318	        lqKind = (version >= 269 && header3 & 0x80) ? 1 : lqType;
319	      }
320	      // RLE 计数
321	      const rleStorage = (header1 & 0xC0) >> 6;
322	      let rle = 0;
323	      if (rleStorage === 1) rle = r.u8();
324	      else if (rleStorage >= 2) rle = r.u16();
325	
326	      // 写入本格 + RLE 重复格（列优先向下）
327	      for (let k = 0; k <= rle && y + k < h; k++) {
328	        const i = (y + k) * w + x;
329	        active[i] = (header1 & 0x02) ? 1 : 0;
330	        type[i] = tileType;
331	        frameX[i] = fx;
332	        frameY[i] = fy;
333	        wall[i] = wl;
334	        liquid[i] = lqAmount;
335	        liquidType[i] = lqKind;
336	      }
337	      y += rle;
338	    }
339	  }
340	  void idx;
341	  return { active, type, frameX, frameY, wall, liquid, liquidType };
342	}
343	

```


---

## 🤖 Assistant · 2026-08-07T05:46:14.176Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n -i \"WALL_MAP\\|wall\" ~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts | head -80",
 "description": "Find wall mapping in WldImport"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:14.209Z

**📎 ToolResult**

```
2:// tile/wall/item 的 id 映射基于 Terraria 1.4 的事实数据；未映射内容做可玩性降级。
5:import { TILE_BY_KEY, WALL_BY_KEY, T } from '../data/tiles';
108:  240: { key: 'v_240_wall_hangings_3x3', copyFrame: true },  // Wall Hangings 3x3
241:  294: { key: 'v_294_zebra_swallowtail_butterfly_jar', copyFrame: true },  // Zebra Swallowtail Butterfly Jar
306:// wld wall id → 内部 wall key
307:const WALL_MAP: Record<number, string> = {
308:  1: 'stone_wall',   // Stone (natural)
309:  2: 'dirt_wall',    // Dirt (natural)
310:  3: 'stone_wall',   // Ebonstone
311:  4: 'wood_wall',    // Wood
312:  5: 'stone_wall', 6: 'stone_wall', 7: 'stone_wall', 8: 'stone_wall', 9: 'stone_wall',
313:  10: 'stone_wall', 11: 'stone_wall', 12: 'stone_wall', 13: 'stone_wall', 14: 'stone_wall',
314:  15: 'dirt_wall', 16: 'dirt_wall',
507:  26: 'vi_26_stone_wall',  // Stone Wall
530:  93: 'vi_93_wood_wall',  // Wood Wall
547:  1723: 'vi_1723_living_wood_wall',  // Living Wood Wall
610:  392: 'vi_392_glass_wall',  // Glass Wall
645:  2263: 'vi_2263_white_dynasty_wall',  // White Dynasty Wall
646:  330: 'vi_330_obsidian_brick_wall',  // Obsidian Brick Wall
647:  130: 'vi_130_gray_brick_wall',  // Gray Brick Wall
648:  2433: 'vi_2433_stone_slab_wall',  // Stone Slab Wall
729:  const wall = new Uint8Array(n);
760:    const ww = wld.tiles.wall[i];
762:      wall[i] = WALL_BY_KEY[WALL_MAP[ww] ?? 'stone_wall'] ?? 0;
823:    walls: bytesToB64(rlePairs(wall)),

```


---

## 🤖 Assistant · 2026-08-07T05:46:16.659Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need to look at WldImport.ts around lines 306-320 and 500-760 for WALL_MAP details and wall-related vanilla imports (vi_ keys). Also check where wallTilers are constructed (which wall sheets — '地形/Wall_1.png'). Search main.ts / Renderer for WallTiler instantiation and VANILLA_MISC, vanilla.json walls section.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:46:16.893Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts",
 "offset": 295,
 "limit": 75
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:16.898Z

**📎 ToolResult**

```
295	  71: { key: 'v_71_mushroom_plant', copyFrame: true }, // Mushroom Plant
296	  24: { key: 'v_24_corruption_short_plants', copyFrame: true }, // Corruption Short Plants
297	  32: { key: 'v_32_corruption_thorns', copyFrame: true }, // Corruption Thorns
298	  27: { key: 'v_27_sunflower', copyFrame: true }, // Sunflower (2x4)
299	  44: 'v_44_pink_brick',  // Pink Brick
300	  203: 'v_203_crimstone_block',  // Crimstone Block
301	  201: { key: 'v_201_crimson_short_plants', copyFrame: true }, // Crimson Short Plants
302	  75: 'v_75_obsidian_brick',
303	  199: 'v_199_crimson_grass_block',
304	};
305	
306	// wld wall id → 内部 wall key
307	const WALL_MAP: Record<number, string> = {
308	  1: 'stone_wall',   // Stone (natural)
309	  2: 'dirt_wall',    // Dirt (natural)
310	  3: 'stone_wall',   // Ebonstone
311	  4: 'wood_wall',    // Wood
312	  5: 'stone_wall', 6: 'stone_wall', 7: 'stone_wall', 8: 'stone_wall', 9: 'stone_wall',
313	  10: 'stone_wall', 11: 'stone_wall', 12: 'stone_wall', 13: 'stone_wall', 14: 'stone_wall',
314	  15: 'dirt_wall', 16: 'dirt_wall',
315	};
316	
317	// wld item id → 内部 item key（宝箱战利品用）
318	const ITEM_MAP: Record<number, string> = {
319	  2: 'dirt_block', 8: 'torch', 9: 'wood', 175: 'stone_block',
320	  11: 'iron_ore', 12: 'copper_ore', 13: 'gold_ore', 14: 'silver_ore',
321	  20: 'copper_bar', 22: 'iron_bar', 23: 'gel',
322	  28: 'lesser_healing_potion', 38: 'lens',
323	  71: 'coin_copper', 72: 'coin_copper', 73: 'coin_copper', 74: 'coin_copper',
324	  // 原版批次材料
325	  699: 'tin_ore', 700: 'lead_ore', 701: 'tungsten_ore', 702: 'platinum_ore',
326	  703: 'tin_bar', 704: 'lead_bar', 705: 'tungsten_bar', 706: 'platinum_bar',
327	  177: 'sapphire', 178: 'ruby', 179: 'emerald', 180: 'topaz', 181: 'amethyst', 182: 'diamond',
328	  664: 'ice_block', 883: 'ice_brick', 594: 'snow_brick',
329	  133: 'clay_block', 170: 'glass', 173: 'obsidian', 129: 'gray_brick', 131: 'red_brick',
330	  32: 'table', 34: 'chair', 224: 'bed', 354: 'bookcase', 359: 'grandfather_clock',
331	  105: 'candle', 136: 'lantern', 349: 'candelabra', 222: 'clay_pot', 29: 'life_crystal',
332	  5: 'mushroom_item', 27: 'acorn',
333	  // ---- 全量补全（compat-report 驱动）----
334	  2350: 'vi_2350_recall_potion',  // Recall Potion
335	  188: 'vi_188_healing_potion',  // Healing Potion
336	  282: 'vi_282_glowstick',  // Glowstick
337	  167: 'vi_167_dynamite',  // Dynamite
338	  279: 'vi_279_throwing_knife',  // Throwing Knife
339	  51: 'vi_51_jester_s_arrow',  // Jester's Arrow
340	  19: 'vi_19_gold_bar',  // Gold Bar
341	  302: 'vi_302_water_walking_potion',  // Water Walking Potion
342	  305: 'vi_305_gravitation_potion',  // Gravitation Potion
343	  43: 'vi_43_suspicious_looking_eye',  // Suspicious Looking Eye
344	  296: 'vi_296_spelunker_potion',  // Spelunker Potion
345	  299: 'vi_299_night_owl_potion',  // Night Owl Potion
346	  965: 'vi_965_rope',  // Rope
347	  303: 'vi_303_archery_potion',  // Archery Potion
348	  304: 'vi_304_hunter_potion',  // Hunter Potion
349	  50: 'vi_50_magic_mirror',  // Magic Mirror
350	  42: 'vi_42_shuriken',  // Shuriken
351	  295: 'vi_295_featherfall_potion',  // Featherfall Potion
352	  53: 'vi_53_cloud_in_a_bottle',  // Cloud in a Bottle
353	  2329: 'vi_2329_dangersense_potion',  // Dangersense Potion
354	  40: 'vi_40_wooden_arrow',  // Wooden Arrow
355	  975: 'vi_975_shoe_spikes',  // Shoe Spikes
356	  54: 'vi_54_hermes_boots',  // Hermes Boots
357	  301: 'vi_301_thorns_potion',  // Thorns Potion
358	  49: 'vi_49_band_of_regeneration',  // Band of Regeneration
359	  2326: 'vi_2326_titan_potion',  // Titan Potion
360	  297: 'vi_297_invisibility_potion',  // Invisibility Potion
361	  166: 'vi_166_bomb',  // Bomb
362	  5011: 'vi_5011_mace',  // Mace
363	  4425: 'vi_4425_shark_bait',  // Shark Bait
364	  2351: 'vi_2351_teleportation_potion',  // Teleportation Potion
365	  4460: 'vi_4460_sandcastle_bucket',  // Sandcastle Bucket
366	  168: 'vi_168_grenade',  // Grenade
367	  227: 'vi_227_restoration_potion',  // Restoration Potion
368	  930: 'vi_930_flare_gun',  // Flare Gun
369	  931: 'vi_931_flare',  // Flare

```


---

## 🤖 Assistant · 2026-08-07T05:46:17.349Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"WallTiler\\|wallTilers\\|Wall_\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | grep -v \"^.*WallTiler.ts\"",
 "description": "Find WallTiler usage and wall sheet files"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:17.369Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-07T05:46:18.109Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"walls\" ~/Project/GLM/SandboxWorld/game/public/assets/vanilla.json 2>/dev/null | head; ls ~/Project/GLM/SandboxWorld/game/public/assets 2>/dev/null | head -30; grep -rn \"VANILLA_MISC\" ~/Project/GLM/SandboxWorld/game/src ~/Project/GLM/SandboxWorld/game/scripts 2>/dev/null | head -20",
 "description": "Check vanilla.json walls and VANILLA_MISC"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:18.146Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:42:export const VANILLA_MISC = [
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts:108:      ...VANILLA_MISC, // 杂项单图（呼吸气泡等）

```


---

## 🤖 Assistant · 2026-08-07T05:46:20.850Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
zsh glob issue with --include=*.ts. Quote it. Also find WallTiler instantiation and wall sheets.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:46:21.239Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"WallTiler\\|wallTilers\\|Wall_\" ~/Project/GLM/SandboxWorld/game/src | grep -v \"src/render/WallTiler.ts\"",
 "description": "Find WallTiler usage and wall sheet files"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:21.264Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:9:import type { WallTiler } from './WallTiler';
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:31:  wallTilers: Map<number, WallTiler>;
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:33:  constructor(world: World, sheets: Map<number, TileSheetEntry>, autotiler: AutoTiler | null = null, wallTilers: Map<number, WallTiler> = new Map()) {
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:37:    this.wallTilers = wallTilers;
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts:139:          const wallTiler = this.wallTilers.get(wall);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:29:import { WallTiler } from '../render/WallTiler';
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:253:    const wallTilers = new Map<number, WallTiler>();
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:255:      const sheetByWall: Record<number, string> = { 1: '地形/Wall_2.png', 2: '地形/Wall_1.png' };
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:258:        const tiler = new WallTiler(this.atlas, [file]);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:261:        wallTilers.set(Number(wallId), tiler);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:264:    this.chunks = new ChunkCache(w, this.assets.tileSheets, this.autotiler, wallTilers);

```


---

## 🤖 Assistant · 2026-08-07T05:46:21.733Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/assets/ 2>/dev/null; find ~/Project/GLM/SandboxWorld/game/public -name \"vanilla.json\" -o -name \"*Wall*\" | head -20",
 "description": "Find vanilla.json and wall assets"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:21.774Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla.json
~/Project/GLM/SandboxWorld/game/public/sprites/地形/Wall_1.png
~/Project/GLM/SandboxWorld/game/public/sprites/地形/Wall_2.png

```


---

## 🤖 Assistant · 2026-08-07T05:46:23.026Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 30,
 "offset": 245
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:23.032Z

**📎 ToolResult**

```
245	    await this.settleLiquids((p) => onProgress?.('水体沉降', p));
246	    this.afterWorldLoad();
247	    this.cb.onWorldReady();
248	  }
249	
250	  private afterWorldLoad() {
251	    const w = this.world;
252	    // 墙体贴合器（按墙类型分 sheet；alpha 轮廓分类，规避 Maples 错误规则表）
253	    const wallTilers = new Map<number, WallTiler>();
254	    if (this.atlas) {
255	      const sheetByWall: Record<number, string> = { 1: '地形/Wall_2.png', 2: '地形/Wall_1.png' };
256	      for (const [wallId, file] of Object.entries(sheetByWall)) {
257	        if (!this.atlas.has(file)) continue;
258	        const tiler = new WallTiler(this.atlas, [file]);
259	        tiler.analyze();
260	        tiler.buildPatterns();
261	        wallTilers.set(Number(wallId), tiler);
262	      }
263	    }
264	    this.chunks = new ChunkCache(w, this.assets.tileSheets, this.autotiler, wallTilers);
265	    this.lighting = new LightingEngine(w);
266	    this.liquid = new LiquidSim(w);
267	    this.camera = new Camera(w.w, w.h);
268	    this.renderer.minimap = new Minimap(w);
269	    this.entities.clear();
270	    this.player = new Player(w.spawnX * TILE + 8, (w.spawnY - 3) * TILE, new Inventory()); // 主角 3 格高，抬高出生点
271	    // 初始装备（铁器三件套与 Maples 素材对齐；含药水与配饰便于体验 Buff/配饰系统）
272	    this.player.inv.add(ITEM_BY_KEY['iron_pickaxe'], 1);
273	    this.player.inv.add(ITEM_BY_KEY['iron_axe'], 1);
274	    this.player.inv.add(ITEM_BY_KEY['iron_sword'], 1);

```


---

## 🤖 Assistant · 2026-08-07T05:46:23.786Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla.json'))\nprint(list(d.keys()))\nprint('walls' in d, len(d.get('walls',[])) if 'walls' in d else None)\nfor k,v in d.items():\n    print(k, type(v), (len(v) if hasattr(v,'__len__') else v))\n\"",
 "description": "Inspect vanilla.json sections and walls count"
}
```


---

## 🤖 Assistant · 2026-08-07T05:46:24.477Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"vi_26_stone_wall\\|vi_93_wood_wall\\|vi_1723\\|vi_392_glass_wall\\|vi_2263\\|vi_330\\|vi_130\\|vi_2433\" ~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts | head -20",
 "description": "Find vi_ wall references in WldImport"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:26.999Z

**📎 ToolResult**

```
['tiles', 'items', 'walls', 'npcs', 'tileNames', 'itemNames']
True 0
tiles <class 'dict'> 310
items <class 'dict'> 479
walls <class 'dict'> 0
npcs <class 'dict'> 17
tileNames <class 'dict'> 753
itemNames <class 'dict'> 6121

```


---

## 👤 User(sidechain) · 2026-08-07T05:46:27.023Z

**📎 ToolResult**

```
477:  1309: 'vi_1309_slime_staff',  // Slime Staff
507:  26: 'vi_26_stone_wall',  // Stone Wall
530:  93: 'vi_93_wood_wall',  // Wood Wall
547:  1723: 'vi_1723_living_wood_wall',  // Living Wood Wall
610:  392: 'vi_392_glass_wall',  // Glass Wall
645:  2263: 'vi_2263_white_dynasty_wall',  // White Dynasty Wall
646:  330: 'vi_330_obsidian_brick_wall',  // Obsidian Brick Wall
647:  130: 'vi_130_gray_brick_wall',  // Gray Brick Wall
648:  2433: 'vi_2433_stone_slab_wall',  // Stone Slab Wall

```


---

## 🤖 Assistant · 2026-08-07T05:46:30.359Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The vi_*_wall entries at lines 507, 530, 547, 610, 645-648 — need to check which map those belong to. They could be TILE_MAP (walls-as-items?) or ITEM_MAP. Let me look at context. Also check whether walls are exported in vanilla.json walls=0 (confirmed count 0).

Let me check the context around line 507 and 645 in WldImport.ts to determine which map they're in.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:46:30.720Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"^const \\|^};\\|^export const\" ~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts | head -20",
 "description": "List map declarations in WldImport"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:30.748Z

**📎 ToolResult**

```
10:const TILE_MAP: Record<number, MapEntry> = {
304:};
307:const WALL_MAP: Record<number, string> = {
315:};
318:const ITEM_MAP: Record<number, string> = {
705:};
855:const vanillaData = vanillaJson as unknown as { tileNames?: Record<string, string>; itemNames?: Record<string, string> };
856:const vanillaTileNames = vanillaData.tileNames ?? {};
857:const vanillaItemNames = vanillaData.itemNames ?? {};

```


---

## 🤖 Assistant · 2026-08-07T05:46:30.970Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts",
 "limit": 45,
 "offset": 725
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:30.988Z

**📎 ToolResult**

```
725	  const n = w * h;
726	  const type = new Uint16Array(n);
727	  const frameX = new Uint16Array(n);
728	  const frameY = new Uint16Array(n);
729	  const wall = new Uint8Array(n);
730	  const liquidArr = new Uint8Array(n);
731	  const liquidTypeArr = new Uint8Array(n);
732	
733	  const chestAt = new Map<string, { x: number; y: number }>();
734	  for (const c of wld.chests) chestAt.set(`${c.x},${c.y}`, c);
735	
736	  let unmapped = 0;
737	  for (let i = 0; i < n; i++) {
738	    const wt = wld.tiles.type[i];
739	    if (wld.tiles.active[i]) {
740	      const mapped = TILE_MAP[wt];
741	      if (mapped === undefined) {
742	        // 未映射：framed 物体丢弃，方块降级为 stone（保持地形完整可玩）
743	        unmapped++;
744	        bump(deg, wt);
745	        type[i] = T.STONE;
746	      } else if (mapped === null) {
747	        bump(clr, wt);
748	        type[i] = 0;
749	      } else if (typeof mapped === 'string') {
750	        type[i] = TILE_BY_KEY[mapped] ?? 0;
751	      } else {
752	        // 原版 framed 家具：18px 帧/样式偏移直拷（与 .wld 原生一致，渲染端零换算）
753	        type[i] = TILE_BY_KEY[mapped.key] ?? 0;
754	        if (mapped.copyFrame) {
755	          frameX[i] = wld.tiles.frameX[i];
756	          frameY[i] = wld.tiles.frameY[i];
757	        }
758	      }
759	    }
760	    const ww = wld.tiles.wall[i];
761	    if (ww !== 0) {
762	      wall[i] = WALL_BY_KEY[WALL_MAP[ww] ?? 'stone_wall'] ?? 0;
763	    }
764	    const lq = wld.tiles.liquid[i];
765	    if (lq > 0) liquidArr[i] = lq;
766	    // 液体类型：parser 已按内部编码输出（1水 2岩浆 3蜂蜜），直拷
767	    if (lq > 0) liquidTypeArr[i] = wld.tiles.liquidType[i] || 1;
768	  }
769	  if (unmapped > 0) warnings.push(`${unmapped} 个未知 tile 已降级为石块`);

```


---

## 🤖 Assistant · 2026-08-07T05:46:38.188Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The vi_*_wall entries (lines 507, 530, 547, 610, 645-648) are within ITEM_MAP (lines 318-705) — those are wall *items* (wall placeable items), not wall types. So WALL_MAP has exactly 16 entries (ids 1-16) mapping to only 3 internal wall types (stone/dirt/wood). Fallback for unmapped: 'stone_wall' (line 762). Note the imported wall array is Uint8Array (line 729), so the u16 extension (wall >= 256) gets truncated? Actually wall[i] = value of WALL_BY_KEY[...] which is 0-3, fine.

Also note: WALL_MAP only covers natural walls 1-16; placed walls (e.g. 27 wood wall, 41 stone brick wall etc.) all fall back to stone_wall.

Now check shade usage in ChunkCache wall pass — line 181, used only in the fallback (flat color) branch. Does the WallTiler branch apply any darkening/lighting? Check Renderer.ts for how wall layer is drawn with lighting.

Also confirm vanilla-atlas.mjs outputs walls count=0. Check scripts/vanilla-atlas.mjs for walls section. And check VANILLA_MISC in SpriteAtlas.ts line 42.

Let me quickly check Renderer.ts wall draw + lighting.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:46:38.601Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"wall\\|shade\\|lightness\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -40",
 "description": "Find wall drawing and lighting in Renderer"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:38.633Z

**📎 ToolResult**

```
47:    if (st.wall[i] !== 0) {
49:      const w = st.wall[i];
233:        ctx.drawImage(chunks.get(cx, cy).wall, cx * CHUNK * ts, cy * CHUNK * ts);

```


---

## 🤖 Assistant · 2026-08-07T05:46:39.120Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"walls\" ~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs | head -10; sed -n 38,60p ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts",
 "description": "Check walls in vanilla-atlas.mjs and VANILLA_MISC"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:39.157Z

**📎 ToolResult**

```
25:const walls = JSON.parse(readFileSync(join(TEDIT_DATA, 'walls.json'), 'utf8'));
28:const wallById = new Map(walls.map((w) => [w.id, w]));
50:const out = { tiles: {}, items: {}, walls: {}, npcs: {} };
102:for (const id of whitelist.walls) {
110:  out.walls[id] = {
139:console.log(`vanilla-atlas: tiles=${Object.keys(out.tiles).length} items=${Object.keys(out.items).length} walls=${Object.keys(out.walls).length} copied=${copied}`);
// ---- 原版素材命名空间（vanilla.json，TEdit 数据驱动） ----

// 杂项单图素材（非表驱动，直接整图使用）
// 树木专用：Tree_Tops/Branches（树冠树枝，TEdit style 0-10）+ Tiles_5_N（生物群系树干）
export const VANILLA_MISC = [
  'vanilla/Bubble.png',
  ...Array.from({ length: 11 }, (_, i) => `vanilla/Tree_Tops_${i}.png`),
  ...Array.from({ length: 11 }, (_, i) => `vanilla/Tree_Branches_${i}.png`),
  ...Array.from({ length: 7 }, (_, i) => `vanilla/Tiles_5_${i}.png`),
  'vanilla/Evil_Cactus.png', 'vanilla/Good_Cactus.png', 'vanilla/Crimson_Cactus.png',
];
export interface VanillaTileMeta {
  name: string; key: string; sheet: string;
  solid: boolean; blend: boolean; framed: boolean; light: boolean;
  color: string; placement: string | null;
  grid: [number, number];      // 帧像素尺寸（蜡烛类 [16,20]）
  stride: [number, number];    // 表内帧步长（grid+gap，如 [18,18]）
  frameSize: Array<[number, number]>; // 每个 style 的占格数
  cols: number; rows: number;
}
export interface VanillaItemMeta { name: string; key: string; icon: string; createTile: number | null; }
export interface VanillaWallMeta {
  name: string; key: string; sheet: string; color: string;

```


---

## 🤖 Assistant · 2026-08-07T05:46:41.870Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 40,
 "offset": 35
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:41.880Z

**📎 ToolResult**

```
35	    });
36	  }
37	
38	  colorFor(x: number, y: number): string | null {
39	    const st = this.world.store;
40	    const i = st.idx(x, y);
41	    if (st.type[i] !== 0) {
42	      const d = TILE_DEFS[st.type[i]];
43	      return d ? d.mapColor : '#808080';
44	    }
45	    // 液体：水蓝 / 岩浆橙
46	    if (st.liquid[i] > 40) return st.liquidType[i] === 2 ? '#E8622C' : '#3D6FD1';
47	    if (st.wall[i] !== 0) {
48	      // 墙色 = 深化（地下洞穴空气）
49	      const w = st.wall[i];
50	      return w === 1 ? '#3A2A1A' : w === 2 ? '#2E2E2E' : '#3A2812';
51	    }
52	    // 探索过的天空 = 亮蓝（未探索区域由迷雾层另盖黑）
53	    return '#7EB6E8';
54	  }
55	
56	  redrawAll() {
57	    const { world, ctx } = this;
58	    const img = ctx.createImageData(world.w, world.h);
59	    for (let y = 0; y < world.h; y++) {
60	      for (let x = 0; x < world.w; x++) {
61	        const c = this.colorFor(x, y);
62	        const i = (y * world.w + x) * 4;
63	        if (c) {
64	          const v = parseInt(c.slice(1), 16);
65	          img.data[i] = (v >> 16) & 255; img.data[i + 1] = (v >> 8) & 255; img.data[i + 2] = v & 255;
66	        }
67	        img.data[i + 3] = 255;
68	      }
69	    }
70	    ctx.putImageData(img, 0, 0);
71	    this.dirtyChunks.clear();
72	  }
73	
74	  flushDirty() {

```


---

## 🤖 Assistant · 2026-08-07T05:46:42.485Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"walls\" ~/Project/GLM/SandboxWorld/game/scripts/*.mjs ~/Project/GLM/SandboxWorld/game/scripts/*.json 2>/dev/null | head; grep -rn \"whitelist\" ~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs | head -5",
 "description": "Check walls whitelist source"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:42.537Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:25:const walls = JSON.parse(readFileSync(join(TEDIT_DATA, 'walls.json'), 'utf8'));
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:28:const wallById = new Map(walls.map((w) => [w.id, w]));
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:50:const out = { tiles: {}, items: {}, walls: {}, npcs: {} };
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:102:for (const id of whitelist.walls) {
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:110:  out.walls[id] = {
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:139:console.log(`vanilla-atlas: tiles=${Object.keys(out.tiles).length} items=${Object.keys(out.items).length} walls=${Object.keys(out.walls).length} copied=${copied}`);
~/Project/GLM/SandboxWorld/game/scripts/vanilla-whitelist.json:2: "_comment": "原版素材白名单：构建脚本按此拷贝 PNG + 提取 TEdit 元数据。tiles=Tiles_N 表 id，items=Item_N 图标 id，walls=Wall_N 表 id",
~/Project/GLM/SandboxWorld/game/scripts/vanilla-whitelist.json:796: "walls": [],
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:15:const whitelist = JSON.parse(readFileSync(join(here, 'vanilla-whitelist.json'), 'utf8'));
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:63:for (const id of whitelist.tiles) {
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:89:for (const id of whitelist.items) {
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:102:for (const id of whitelist.walls) {
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:119:for (const id of whitelist.npcs ?? []) {

```


---

## 🤖 Assistant · 2026-08-07T05:46:45.664Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: vanilla-whitelist.json "walls": [] (empty), so vanilla.json walls = {} (count 0). So no vanilla wall textures are used; walls are rendered from Maples sheets '地形/Wall_1.png' / '地形/Wall_2.png'.

Now check how the wall canvas layer gets lit/darkened at draw time (main render path, line ~233 in Renderer.ts draws chunk wall canvas). Check for lighting multiplication on wall layer.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:46:46.349Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"shade\\|lightness\\|multiply\\|globalCompositeOperation\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -30; grep -n \"drawImage(chunks\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "description": "Check lighting application in Renderer draw path"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:46.396Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:999:    ctx.globalCompositeOperation = 'multiply';
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:1003:    ctx.globalCompositeOperation = 'source-over';
233:        ctx.drawImage(chunks.get(cx, cy).wall, cx * CHUNK * ts, cy * CHUNK * ts);
244:        ctx.drawImage(chunks.get(cx, cy).tile, cx * CHUNK * ts, cy * CHUNK * ts);

```


---

## 🤖 Assistant · 2026-08-07T05:46:46.655Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 200,280p ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "description": "Read main world draw pass in Renderer"
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:46.684Z

**📎 ToolResult**

```
  ) {
    this._mouseX = mouseX;
    this._mouseY = mouseY;
    this._mouseDown = mouseDown;
    this.easeFullMap();
    const ctx = this.ctx;
    const viewW = this.canvas.width, viewH = this.canvas.height;
    cam.viewW = viewW; cam.viewH = viewH;
    const z = cam.zoom;

    // 1. 天空
    this.sky.draw(ctx, clock, viewW, viewH, cam.x);

    ctx.save();
    // 世界变换：平移 + 缩放（以屏幕中心为相机中心）
    // 像素风关键：tile/实体用最近邻采样保持锐利（光照层单独用平滑）
    ctx.imageSmoothingEnabled = false;
    ctx.translate(viewW / 2, viewH / 2);
    ctx.scale(z, z);
    ctx.translate(-cam.x, -cam.y);

    // 2. chunks（双层画布：墙层 → 水 → tile 层，水夹在墙与图块之间）
    const ts = TILE;
    const x0 = Math.floor((cam.x - viewW / 2 / z) / (CHUNK * ts)) - 1;
    const x1 = Math.floor((cam.x + viewW / 2 / z) / (CHUNK * ts)) + 1;
    const y0 = Math.floor((cam.y - viewH / 2 / z) / (CHUNK * ts)) - 1;
    const y1 = Math.floor((cam.y + viewH / 2 / z) / (CHUNK * ts)) + 1;
    const chunkVisible = (cx: number, cy: number) =>
      cx >= 0 && cy >= 0 && cx * CHUNK < world.w && cy * CHUNK < world.h;
    // 2a. 背景墙层
    for (let cy = y0; cy <= y1; cy++) {
      for (let cx = x0; cx <= x1; cx++) {
        if (!chunkVisible(cx, cy)) continue;
        ctx.drawImage(chunks.get(cx, cy).wall, cx * CHUNK * ts, cy * CHUNK * ts);
      }
    }

    // 2b. 液体（墙之上、图块之下；向实心邻格浸润外扩一格遮住贴图透明缝隙）
    this.drawLiquids(world, cam, viewW, viewH, z);

    // 2c. 前景 tile/物体层
    for (let cy = y0; cy <= y1; cy++) {
      for (let cx = x0; cx <= x1; cx++) {
        if (!chunkVisible(cx, cy)) continue;
        ctx.drawImage(chunks.get(cx, cy).tile, cx * CHUNK * ts, cy * CHUNK * ts);
      }
    }

    // 4. 实体（按 y 排序）
    const sorted = [...entities].sort((a, b) => a.y - b.y);
    for (const e of sorted) {
      if (e instanceof Enemy) this.drawEnemy(e, world);
      else if (e instanceof ItemDrop) this.drawDrop(e);
      else if (e instanceof TownNPC) this.drawTownNPC(e);
      else if (e instanceof Tombstone) this.drawTombstone(e);
      else if (e instanceof Critter) this.drawCritter(e);
      else (e as Player).draw && null;
    }
    this.drawPlayer(player, world, swing);

    // 5. 粒子
    for (const p of particles) {
      ctx.globalAlpha = Math.max(0, p.life / p.maxLife);
      ctx.fillStyle = p.color;
      ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
    }
    ctx.globalAlpha = 1;

    // 6. 挖掘/放置光标：挖掘中黄色填充随进度加深（半透明黄 → 破坏完成时最深）
    if (hover) {
      ctx.strokeStyle = 'rgba(255,255,255,0.7)';
      ctx.lineWidth = 1 / z;
      ctx.strokeRect(hover.x * ts + 0.5, hover.y * ts + 0.5, ts - 1, ts - 1);
      if (mineProgress > 0) {
        // 进度 0→1，黄色 alpha 0.15→0.8 加深渐变（接近破坏时深黄）
        ctx.globalAlpha = 0.15 + Math.min(1, mineProgress) * 0.65;
        ctx.fillStyle = '#FFC419';
        ctx.fillRect(hover.x * ts + 1, hover.y * ts + 1, ts - 2, ts - 2);
        ctx.globalAlpha = 1;
      }
    }

```


---

## 🤖 Assistant · 2026-08-07T05:46:47.956Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me check lines 985-1010 in Renderer.ts (multiply composite) — this is the lighting overlay applied over everything (likely). Confirm quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:46:48.154Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 30,
 "offset": 980
}
```


---

## 👤 User(sidechain) · 2026-08-07T05:46:48.173Z

**📎 ToolResult**

```
980	        // 4 tap 双线性
981	        const a = tap(x0, y0), b = tap(x0 + 1, y0), c = tap(x0, y0 + 1), d = tap(x0 + 1, y0 + 1);
982	        const w00 = wx0 * wy0, w10 = wx1 * wy0, w01 = wx0 * wy1, w11 = wx1 * wy1;
983	        let r = a[0] * w00 + b[0] * w10 + c[0] * w01 + d[0] * w11;
984	        let g = a[1] * w00 + b[1] * w10 + c[1] * w01 + d[1] * w11;
985	        let b2 = a[2] * w00 + b[2] * w10 + c[2] * w01 + d[2] * w11;
986	        // gamma 柔化 + 最低可见度
987	        const amb = 10;
988	        const i = (py * w2 + px) * 4;
989	        img.data[i] = Math.max(lut[Math.min(255, Math.round(r))], amb);
990	        img.data[i + 1] = Math.max(lut[Math.min(255, Math.round(g))], amb);
991	        img.data[i + 2] = Math.max(lut[Math.min(255, Math.round(b2))], amb);
992	        img.data[i + 3] = 255;
993	      }
994	    }
995	    lc.putImageData(img, 0, 0);
996	    const ctx = this.ctx;
997	    ctx.save();
998	    ctx.imageSmoothingEnabled = true;
999	    ctx.globalCompositeOperation = 'multiply';
1000	    const [sx, sy] = cam.worldToScreen(tx0 * ts, ty0 * ts);
1001	    ctx.drawImage(this.lightCanvas, sx, sy, tilesX * ts * z, tilesY * ts * z);
1002	    ctx.restore();
1003	    ctx.globalCompositeOperation = 'source-over';
1004	  }
1005	
1006	  private drawMinimap(ctx: CanvasRenderingContext2D, cam: Camera, world: World, player: Player, clock: Clock) {
1007	    if (!this.minimap) return;
1008	    this.minimap.flushDirty();
1009	    const size = 240;                 // 放大

```


---

## 🤖 Assistant · 2026-08-07T05:47:00.384Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything needed. Now write the report. I'm in plan mode as a read-only search agent — my task is to report findings. I don't need to create a plan file; the task is a search/report task. I'll just deliver the findings as my final message.

Let me compile:

1. WallTiler.ts — full logic.
2. ChunkCache.ts wall pass.
3. tiles.ts W/WALL_DEFS/WALL_BY_KEY.
4. WldImport WALL_MAP — 16 entries (ids 1-16), fallback 'stone_wall' at line 762.
5. WldParser wall reading: header1 & 0x04 → u8, header3 & 0x10 wall color, version>=222 && header3&0x40 → u8 << 8 extension.
6. Vanilla walls: vanilla-whitelist.json "walls": [] line 796 → vanilla.json walls = {} count 0. Confirmed.
7. shade usage: ChunkCache line 181-183 fallback flat-color branch only; wall pass itself has no lighting; lighting applied globally via multiply composite (Renderer ~996-1003).

Exact mask convention for WallTiler: key string order [上,右,下,左] = [top, right, bottom, left]. In pick(), closed param: true = same-type wall on that side (closed); want key = closed ? '0' : '1' — so '1' bit = open side. groups keys from analyze() are 'open' bits (1 = open side).

Caching: groups Map keyed by 4-bit string; patterns array of 64×64 canvases prebuilt at startup; no per-chunk caching in WallTiler itself; ChunkCache caches rendered chunk canvases.

Frame selection for interior/edge/corner:
- interior (all 4 neighbors same wall): patternSample(x,y) → continuous 64×64 plum-blossom pattern sampling at ((x*16)%64, (y*16)%64), variant chosen per 4×4 supertile hash.
- edge/corner: brick anchor 2×2 — by = y & ~1; rowOff = (y&2)>>1; bx = ((x-rowOff) & ~1) + rowOff; quadrant qx = x-bx, qy = y-by (0/1). Closed computed per brick side using two perimeter cells per side (e.g. top: wAt(bx,by-1) || wAt(bx+1,by-1)). pick(closed, bx, by) → fallback pick([false,false,false,false], x, y) i.e. all-open. Draw quadrant quarter of the picked sprite: hw=r.sw/2, hh=r.sh/2, source sx+qx*hw, sy+qy*hh → draw stretched to TILE×TILE.
- Fallback if no wallTiler: flat mapColor fill + shade(mapColor, 0.8) bottom/right 1px edge lines.

In analyze(): for each sprite in file: getImageData; coverage<0.15 skip; coverage>=0.75 → '0000' interior group; BAND = max(2, min(w,h)/8); innerOpaque<0.4 skip; bands [top,right,bottom,left]; open[i] = bands[i] < maxBand*0.6; if none open, force weakest side open; key = bits of open.

pick(): want = closed?0:1 per side; group lookup; fallback '0000'; select variant via hash2(x,y,131)*len.

buildPatterns(): A layer 4× tiles at 0/32 offsets → 64×64; fill transparent pixels with average color ± hash jitter (0.92–1.08); B layer diagonal offset 16 with globalAlpha 0.35, wrapping -64.

Note also: WallTiler instantiated per wall id in Game.afterWorldLoad (Game.ts:250-263): sheetByWall {1: '地形/Wall_2.png', 2: '地形/Wall_1.png'} — i.e., internal wall id 1 = dirt_wall → Wall_2.png; id 2 = stone_wall → Wall_1.png. Wall 3 (wood) has no tiler → flat color fallback.

Wait — check: WALL_DEFS: 1 dirt_wall, 2 stone_wall, 3 wood_wall. sheetByWall {1: Wall_2, 2: Wall_1}. So dirt uses Wall_2.png, stone uses Wall_1.png. Good.

Also WldImport wall array Uint8Array (line 729) — but import maps to ids 0-3 anyway.

Also ChunkCache's own neighborMask (lines 102-115) is for tiles (blend sheets), not walls — 8-bit N,E,S,W,NE,SE,SW,NW with bits 0..7; used at line 261-263 for 'blend' tile sheets. Mention for contrast.

Report now.
```

</details>


---

## 🤖 Assistant · 2026-08-07T05:47:34.961Z · glm-x-preview-260804

````
# Wall Rendering System — Findings

## 1. `~/Project/GLM/SandboxWorld/game/src/render/WallTiler.ts` (159 lines)

Data-driven wall auto-tiler. Header comment (lines 1–4) explains the design decision: **Maples' RuleTile rule tables mis-map interior wall variants to 1/4-size pieces (25% coverage), so the tiler ignores those rules entirely and instead analyzes the alpha silhouette of each wall sprite**, classifying by which of the four sides (top/right/bottom/left) are "open", then picking variants at runtime per 2×2 block.

### `analyze()` (lines 16–78) — startup-time sheet analysis
For each file passed in (constructor takes `atlas` + `files: string[]`), it copies the decoded atlas image to a scratch canvas (lines 21–24) and `getImageData`s each sprite rect. Then:

- `bandOpaque(x0,y0,bw,bh)` helper (lines 30–39): fraction of pixels in a band with alpha > 40.
- Whole-sprite `coverage < 0.15` → skipped as empty/noise (line 41).
- **`coverage >= 0.75` → forced into the `'0000'` interior group** (lines 44–48). Comment notes this prevents half-block edge pieces from polluting the interior group ("the root cause of it previously looking unchanged").
- `BAND = max(2, floor(min(w,h)/8))` (line 49); `innerOpaque < 0.4` → skipped (line 51).
- Four edge bands measured in **[top, right, bottom, left]** order (lines 53–58).
- Relative comparison: a side is *open* if its band opacity `< maxBand * 0.6` (lines 59–65).
- If all four sides read closed, the **weakest side is force-marked open** (lines 68–72) so half-pieces can't sneak into the interior group.
- Key = 4-char string of `open` bits (`'1' = open`), sprite pushed into `this.groups` (a `Map<string, Array<{file,name,rect}>>`).

### Exact mask convention
- **Bit/string order is always `[top, right, bottom, left]`** (上 右 下 左), declared at line 8 (`SideProfile.open`) and in the `pick` doc comment (line 82).
- `analyze()` keys = **open** bits (`'1'` = that side is open/receded).
- `pick()` keys = **inverted**: caller passes `closed` (true = same-type wall present = sealed), and line 86 builds `want = closed.map(c => c ? 0 : 1).join('')` — so `'1'` still means *open* in the lookup key.

### `pick(closed, x, y)` (lines 84–95)
Looks up `groups.get(want)`; if empty, falls back to the `'0000'` interior group (lines 88–91). Variant chosen deterministically via `hash2(x, y, 131) * list.length` (line 93) — stable per anchor cell. Note the comment on line 89 says "逐侧放宽" (relax per-side) but the implementation is a straight fallback to interior.

### Caching
- `groups` map is built once at startup; no runtime caching.
- `patterns: HTMLCanvasElement[]` (line 100) — prebuilt 64×64 seamless canvases.

### `buildPatterns()` (lines 102–149) — "dice-5" / plum-blossom continuous pattern
Per interior (`'0000'`) sprite: A layer tiles the sprite at 32px offsets `(0,0),(32,0),(0,32),(32,32)` covering the full 64×64 (lines 112–114); then **all remaining transparent pixels are flood-filled with the sprite's average opaque color, jittered ±8% by hash** (lines 115–136) so sealed interior walls have no see-through brick seams. B layer overlays the sprite diagonally offset by 16px (with -64 wrapping for seamlessness) at `globalAlpha = 0.35` (lines 137–146) to soften the quincunx into a continuous wall.

### `patternSample(x, y)` (lines 152–158)
Interior walls sample the 64×64 pattern continuously by world coords: `sx = (x*16) % 64`, `sy = (y*16) % 64`; pattern variant selected per 4×4-tile supertile via `hash2(floor(x/4), floor(y/4), 313)`.

### Corners/edges
WallTiler itself has **no diagonal/corner bits** — only the 4 cardinal sides. Corner appearance emerges because an edge/corner brick is a 2×2 block of cells sharing one picked sprite (see ChunkCache below), so an L-shaped boundary gets one side open on each axis from the 4-side mask.

---

## 2. `~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts`

`renderChunk(cx, cy)` (lines 117–345) renders two canvases: `wall` (16×16 tiles × 16px = 256×256) and `tile`. **Wall pass is the first pass** (lines 129–187), tiles are the second pass (lines 192–275) plus 2.5/3/4 passes for branches/canopies. Comment at line 128: walls drawn first so later cells' walls don't cover multi-cell objects (chests/tree crowns).

### WallTiler invocation per cell (lines 138–184)
`wall = st.wall[i]`; `wallTiler = this.wallTilers.get(wall)`:

- **Brick anchor (2×2)**: lines 142–145 — `by = y & ~1`; `rowOff = (y & 2) >> 1`; `bx = ((x - rowOff) & ~1) + rowOff`; quadrant `qx = x - bx`, `qy = y - by` (each 0 or 1). Rows alternate stagger 0/1 every 2 rows (vanilla running-bond).
- **Per-cell closed test** (lines 149–155): cardinal neighbors `wAt(x,y±1)`, `wAt(x±1,y)` equal to this wall id → `[top, right, bottom, left]`.
- **Interior** (all four closed, line 156): `patternSample(x, y)` → draw 16×16 region of the 64×64 pattern canvas (lines 158–161).
- **Edge/corner** (else branch, lines 163–176): brick-level closed state uses **two perimeter cells per side** — e.g. top = `same(wAt(bx, by-1)) || same(wAt(bx+1, by-1))`, right = `same(wAt(bx+2, by)) || same(wAt(bx+2, by+1))`, etc. Then `wallTiler.pick(closed, bx, by)`; fallback `pick([false,false,false,false], x, y)` (all-open, line 171). The picked sprite is drawn as a **quadrant**: source `sx + qx*hw, sy + qy*hh` where `hw = r.sw/2, hh = r.sh/2`, stretched to TILE×TILE (lines 173–174).
- **No WallTiler for this wall id** (lines 177–184): flat `WALL_DEFS[wall].mapColor` fill + 1px darker `shade(mapColor, 0.8)` lines on bottom and right edges.

### Wall sheet sources
Set in `~/Project/GLM/SandboxWorld/game/src/core/Game.ts` `afterWorldLoad()` lines 250–263:
```ts
const sheetByWall: Record<number, string> = { 1: '地形/Wall_2.png', 2: '地形/Wall_1.png' };
```
i.e. internal wall id **1 = dirt_wall → `public/sprites/地形/Wall_2.png`**, **2 = stone_wall → `地形/Wall_1.png`**. For each, `new WallTiler(atlas, [file]); tiler.analyze(); tiler.buildPatterns();` then `wallTilers.set(wallId, tiler)`, and the map is passed to `new ChunkCache(...)` (line 264). Wall id 3 (wood) has no tiler → flat-color fallback.

### Caching / draw order
Chunk canvases cached in `chunks: Map<number, ChunkPair>` (line 26), lazily built in `get()` (85–92), invalidated via `markDirty`/`markDirtyAround` (62–70) on tile changes, redraw budget of 4/frame in `flushDirty` (73–82). At draw time (`~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts` lines 230–246): wall layer (2a) → liquids (2b) → tile layer (2c).

Note: `ChunkCache.neighborMask` (lines 102–115) is for **tile** blend sheets only, not walls — 8 bits: N=bit0, E=bit1, S=bit2, W=bit3, NE=bit4, SE=bit5, SW=bit6, NW=bit7, used at lines 261–263 (`col = mask & 15`, `row = mask >> 4`).

---

## 3. `~/Project/GLM/SandboxWorld/game/src/data/tiles.ts`

Lines 158–168:

```ts
export interface WallDef { key: string; name: string; mapColor: string; opacity: number; }
export const W = { NONE: 0, DIRT: 1, STONE: 2, WOOD: 3 } as const;
export const WALL_DEFS: WallDef[] = [
  { key: 'none', name: '无', mapColor: '#000', opacity: 0 },
  { key: 'dirt_wall', name: '土墙', mapColor: '#5C4128', opacity: 1 },
  { key: 'stone_wall', name: '石墙', mapColor: '#4A4A4A', opacity: 1 },
  { key: 'wood_wall', name: '木墙', mapColor: '#6B4A2B', opacity: 1 },
];
export const WALL_BY_KEY: Record<string, number> = {};
WALL_DEFS.forEach((d, i) => (WALL_BY_KEY[d.key] = i));
```

Exactly 4 wall types (0–3): none, dirt, stone, wood. Properties are only `key/name/mapColor/opacity` — no pick/axe, no blend flag, no vanilla sheet reference. `mapColor` is used both for the flat-color render fallback and the minimap (`Renderer.ts` lines 47–51 hardcodes darker wall minimap colors `#3A2A1A`/`#2E2E2E`/`#3A2812`).

---

## 4. `~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts`

`WALL_MAP` at lines 307–315 — **16 entries total** (wld wall ids 1–16), mapping to only 3 internal wall keys:

- `1: 'stone_wall'` (Stone natural), `2: 'dirt_wall'` (Dirt natural), `3: 'stone_wall'` (Ebonstone), `4: 'wood_wall'` (Wood)
- `5–14: 'stone_wall'` (ten ids on lines 312–313)
- `15: 'dirt_wall'`, `16: 'dirt_wall'`

So all natural/underground wall varieties collapse to stone; only dirt and wood survive distinctly. **All other wld wall ids (every placed wall: wood fence, brick walls, sheet walls, etc.) hit the fallback at line 762**:

```ts
wall[i] = WALL_BY_KEY[WALL_MAP[ww] ?? 'stone_wall'] ?? 0;
```

— unmapped walls become **`'stone_wall'`** (internal id 2), not dropped. The imported wall array is `new Uint8Array(n)` (line 729), which is fine since internal ids are 0–3.

Note: the `vi_26_stone_wall` (line 507), `vi_93_wood_wall` (530), `vi_1723_living_wood_wall` (547), `vi_392_glass_wall` (610), and the wall block at 645–648 (`vi_2263_white_dynasty_wall`, `vi_330_obsidian_brick_wall`, `vi_130_gray_brick_wall`, `vi_2433_stone_slab_wall`) are all inside **`ITEM_MAP`** (declared line 318, closed at 705) — they are wall *items* (inventory icons / craftables), **not** wall type mappings, and there are no corresponding `vi_*_wall` entries in `WALL_DEFS`.

---

## 5. `~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts`

Wall ids read in `decodeTiles()`, lines 306–313:

```ts
let wl = 0;
if (header1 & 0x04) {          // wall-present flag in header1
  wl = r.u8();                 // base u8 wall id
  if (header3 & 0x10) r.u8();  // wall color (discarded)
  if (version >= 222 && header3 & 0x40) {
    wl |= r.u8() << 8;         // u16 extension: high byte
  }
}
```

So: yes — **u8 base, plus a u16 extension high byte when version ≥ 222 and header3 bit 0x40 is set**, OR'd in as `<< 8`. Output stored in `wall: Uint16Array` (declared line 12, allocated line 276, written line 333). Wall colors are read and discarded.

---

## 6. Vanilla wall textures — **not used**

Confirmed:
- `~/Project/GLM/SandboxWorld/game/scripts/vanilla-whitelist.json` line 796: `"walls": []` — the whitelist is empty.
- `~/Project/GLM/SandboxWorld/game/public/sprites/vanilla.json` has a `walls` key but it is an **empty object (count = 0)**; other sections for contrast: tiles=310, items=479, npcs=17, tileNames=753, itemNames=6121.
- `scripts/vanilla-atlas.mjs` iterates `whitelist.walls` (line 102) and emits `walls=${Object.keys(out.walls).length}` in its log (line 139) — with an empty whitelist that prints `walls=0`, matching the claim.
- `VANILLA_MISC` (`~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts` lines 42–49) contains **no wall sheets** — only `vanilla/Bubble.png`, `Tree_Tops_0..10`, `Tree_Branches_0..10`, `Tiles_5_0..6`, and three cactus images. `SpriteAtlas` does define a `VanillaWallMeta` interface (line ~58: `name/key/sheet/color/...`), so the plumbing exists, but nothing populates it.

Wall art comes exclusively from the Maples sheets `地形/Wall_1.png` and `地形/Wall_2.png` (both in `public/sprites/地形/`).

---

## 7. Lighting / darkening of walls

- **Inside the ChunkCache wall pass**: the only `shade` usage is lines 181–183 — and only in the **flat-color fallback branch** (walls without a WallTiler): `shade(wd.mapColor, 0.8)` for 1px bottom/right edge lines. The WallTiler-drawn path applies **no per-cell darkening or light occlusion**; `WALL_DEFS[i].opacity` is never consulted during wall rendering.
- **Global lighting**: applied after the fact in `Renderer.ts` `drawLighting`-ish code at lines 996–1003 — a bilinear-interpolated light canvas is composited with `ctx.globalCompositeOperation = 'multiply'` over the already-drawn scene (walls, liquids, tiles alike), with an ambient floor of 10 (lines 986–992). So walls get darkened by the same lighting pass as everything else, not by anything wall-specific. Minimap wall colors are separately hardcoded darker at `Renderer.ts` lines 47–51.

### Key takeaways on frame selection
- **Interior cell** (all 4 cardinal neighbors same wall): continuous plum-blossom pattern sample, `patternSample(x,y)`, no per-cell variant.
- **Edge/corner cell**: 2×2 brick anchor (staggered every 2 rows); brick-level 4-side closed mask from *two perimeter cells per side*; `pick()` selects a narrowed variant sprite by matching open-side key (fallback: interior group), and only the quadrant `(qx,qy)` of that sprite is drawn stretched to the cell.
- **Mask order everywhere**: `[top, right, bottom, left]`; `'1'`/`true` convention flips between analyze (open) and pick (closed→inverted at lookup).
````
