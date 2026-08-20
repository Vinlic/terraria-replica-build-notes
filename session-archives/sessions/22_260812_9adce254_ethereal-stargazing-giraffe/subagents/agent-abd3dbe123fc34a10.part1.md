# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T08:54:43.790Z

```
在 ~/Project/GLM/SandboxWorld/game（TypeScript+Vite+Canvas 的泰拉瑞亚复刻）探明"游戏资源加载与缓存"现状，回答：

1. **资源取用路径**：src/assets/SpriteAtlas.ts（及同目录）如何取贴图——最终 fetch/XHR 的 URL 形态（如 sprites/vanilla/XXX.png）、有哪些入口（ensureVImage/loadBitmapOnly/atlas 常驻表等）；音效/BGM 如何取（src/audio 或 Sound 相关，xwb/wav 文件路径形态）；贴图总数与磁盘总量（对 public/sprites 等目录 find|wc、du -sh 各子目录，列前几大头）。
2. **Service Worker**：找到 SW 文件（可能 public/sw.js 或 src 下生成）——注册点、缓存名/版本策略、缓存的是什么（fetch 事件拦截? Cache API?）、"分块接力 warm"（sw-asset-preload 相关，约 3 分钟全量预热）实现在哪（src 里调 SW 预热列表的代码）、如何决定要 warm 哪些文件（清单文件? assets-index.json?）。
3. **已有本地持久层**：是否用过 OPFS / IndexedDB / Cache API 存资源；public/assets-index.json 的生成与消费（谁生成、谁读、结构）。
4. **首屏加载流程**：主菜单→进世界前资源可用性保证（preloadSceneAssets 等）；当前"每个文件一次 HTTP"的实际规模感（一次典型会话会请求多少个文件）。

输出：每点给出文件路径+行号锚点、关键代码摘要（勿贴大段）、目录体量数字。只读不改。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T08:54:43.798Z

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

## 🤖 Assistant · 2026-08-19T08:54:49.810Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me explore the codebase to answer these questions. I'll start with a broad overview of the directory structure and the key files mentioned.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:54:50.815Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game && ls ~/Project/GLM/SandboxWorld/game/src && ls ~/Project/GLM/SandboxWorld/game/public 2>/dev/null | head -50",
 "description": "List top-level project structure"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:54:50.921Z

**📎 ToolResult**

```
_audit2.mts
_bst2.mts
_chk_orb.py
1
1.ghost
chrome-profiles
dbg-music.mjs
debug-line.html
dist
docs
index.html
logs
node_modules
package-lock.json
package.json
probe-bee-despawn.mjs
probe-boss-dead.mjs
probe-day-despawn.mjs
probe-eoc-dead.mjs
probe-eoc-trace.mjs
probe-events.mjs
probe-gems.mjs
probe-heart.mjs
probe-invasion.mjs
probe-music.mjs
probe-npc-chat.mjs
probe-npc-full.mjs
probe-npcdrops.mjs
probe-oldman.mjs
probe-pot-heart.mjs
probe-rain-spawn.mjs
probe-sky-preview.mjs
probe-statue.mjs
probe-tax.mjs
probe-time-ui.mjs
probe-town-arrival.mjs
probe-wind-spawn.mjs
public
scripts
shots
src
Starter_World Master.wld
tests
tools
tsconfig.json
vite.config.ts
whip-probe.mjs
whip10-batchB.mjs
whip11-batchC.mjs
whip12-batchD.mjs
whip13-dd2-wolf.mjs
whip14-fox.mjs
whip15-nebula.mjs
whip16-aggro.mjs
whip2.mjs
whip3-sfx.mjs
whip4-shoot.mjs
whip5-summon-full.mjs
whip6-mult-check.mjs
whip7-class-probe.mjs
whip8-time-probe.mjs
whip9-batchA.mjs
assets
core
data
debug
dev
drops
entities
fx
i18n
items
lighting
main.ts
mainFlow.ts
net
physics
player
remaster
render
save
stats
ui
vui
wld
workers
world
annotator.html
assets-index.json
audios
debug-save.sbw.json
fonts
hitbox-lab.html
hitbox-names.json
l10n
remaster.html
sheet-probe.html
sounds
sprites
sw.js
tree-inspect.html
water-audit.html

```


---

## 🤖 Assistant · 2026-08-19T08:54:51.786Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/assets/ 2>/dev/null; echo ---; ls ~/Project/GLM/SandboxWorld/game/src/audio/ 2>/dev/null",
 "description": "List assets and audio source directories"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:54:51.880Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
AssetGen.ts
CharacterSheetGen.ts
ItemIconGen.ts
Palette.ts
SpriteAtlas.ts
TileSheetGen.ts
---

```


---

## 🤖 Assistant · 2026-08-19T08:54:54.030Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
There's no src/audio directory. Let me look for sound-related files. Let me read the key files in parallel and gather statistics.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:54:54.717Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src -iname \"*sound*\" -o -iname \"*audio*\" -o -iname \"*music*\" | head -30",
 "description": "Find sound/audio related source files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:54:54.801Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Audio.ts
~/Project/GLM/SandboxWorld/game/src/data/vanilla-soundtracks.json
~/Project/GLM/SandboxWorld/game/src/data/Music.ts
~/Project/GLM/SandboxWorld/game/src/data/vanilla-itemusesound.json
~/Project/GLM/SandboxWorld/game/src/data/itemUseSound.ts

```


---

## 🤖 Assistant · 2026-08-19T08:54:56.226Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts ~/Project/GLM/SandboxWorld/game/public/sw.js ~/Project/GLM/SandboxWorld/game/public/assets-index.json 2>/dev/null; echo ---; du -sh ~/Project/GLM/SandboxWorld/game/public/* 2>/dev/null | sort -rh | head -20",
 "description": "Check sizes of key files and public subdirectories"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:54:56.337Z

**📎 ToolResult**

```
    1107 ~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts
     220 ~/Project/GLM/SandboxWorld/game/public/sw.js
       0 ~/Project/GLM/SandboxWorld/game/public/assets-index.json
    1327 total
---
178M	~/Project/GLM/SandboxWorld/game/public/sounds
160M	~/Project/GLM/SandboxWorld/game/public/audios
104M	~/Project/GLM/SandboxWorld/game/public/sprites
 12M	~/Project/GLM/SandboxWorld/game/public/l10n
4.9M	~/Project/GLM/SandboxWorld/game/public/debug-save.sbw.json
904K	~/Project/GLM/SandboxWorld/game/public/fonts
388K	~/Project/GLM/SandboxWorld/game/public/hitbox-names.json
356K	~/Project/GLM/SandboxWorld/game/public/assets-index.json
260K	~/Project/GLM/SandboxWorld/game/public/water-audit.html
 40K	~/Project/GLM/SandboxWorld/game/public/remaster.html
 24K	~/Project/GLM/SandboxWorld/game/public/tree-inspect.html
 16K	~/Project/GLM/SandboxWorld/game/public/hitbox-lab.html
 12K	~/Project/GLM/SandboxWorld/game/public/sw.js
8.0K	~/Project/GLM/SandboxWorld/game/public/sheet-probe.html
8.0K	~/Project/GLM/SandboxWorld/game/public/annotator.html

```


---

## 🤖 Assistant · 2026-08-19T08:54:59.438Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — assets-index.json shows 0 lines from wc -l but 356K size — it's probably a single-line JSON. Let me look at the structure of these key files. Let me read SpriteAtlas.ts, sw.js, Audio.ts, and check the assets-index.json structure.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:54:59.722Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:00.001Z

**📎 ToolResult**

```
1	// Unity 素材图集运行时加载器
2	// 数据由 scripts/build-atlas.mjs 生成（public/sprites/atlas.json + resources.json）
3	// 原版素材由 scripts/vanilla-atlas.mjs 生成（public/sprites/vanilla.json，独立命名空间、无 Unity y 翻转）
4	// 注意：Unity 精灵 rect 的 y 轴原点在【左下】，Canvas 在【左上】，取用时要翻转。
5	import atlasJson from '../../public/sprites/atlas.json';
6	import resourcesJson from '../../public/sprites/resources.json';
7	import vanillaJson from '../../public/sprites/vanilla.json';
8	import vanillaNpcsJson from '../../public/sprites/vanilla-npcs.json';
9	import vanillaUiJson from '../../public/sprites/vanilla-ui.json';
10	
11	/** npc id → 动画帧数（SetDefaults 提取数据派生；懒加载 NPC 表用） */
12	const vanillaNpcFrames: Record<string, number> = Object.fromEntries(
13	  Object.entries(vanillaNpcsJson as Record<string, { frames?: number }>).map(([k, v]) => [k, v.frames ?? 1]),
14	);
15	
16	export interface SpriteRect { name: string; x: number; y: number; w: number; h: number; }
17	export interface SpriteRef { file: string; sprite: string; }
18	export interface RuleDef {
19	  id: number;
20	  sprites: SpriteRef[];
21	  neighbors: number[];
22	  positions: Array<[number, number]>;
23	  transform: number;
24	  output: number;
25	}
26	export interface RuleTileDef { defaultSprite: SpriteRef | null; tilingRules: RuleDef[]; }
27	
28	export interface AtlasFile { guid: string; sprites: SpriteRect[]; idToName: Record<string, string>; }
29	export interface AtlasData {
30	  files: Record<string, AtlasFile>;
31	  guidToFile: Record<string, string>;
32	}
33	export interface ResourcesData {
34	  items: Array<{ name: string; type: string; iconGuid: string | null; placeTile: string | null; funcList: string }>;
35	  tiles: Array<{ name: string; tileGuid: string; layer: string; digList: string; digTime: string; dropItemGuid: string }>;
36	  potions: Array<{ name: string; type: string; iconGuid: string | null; buffType: number | null; duration: number | null; isHealType: string }>;
37	  accessories: Array<{ name: string; type: string; iconGuid: string | null }>;
38	  buffs: Array<{ name: string; iconGuid: string | null }>;
39	  anims: Record<string, SpriteRef[]>;
40	  rules: Record<string, RuleTileDef>;
41	}
42	
43	export interface DrawRect { img: ImageBitmap | ImageBitmap | HTMLImageElement | HTMLCanvasElement; sx: number; sy: number; sw: number; sh: number; }
44	
45	// ---- 原版素材命名空间（vanilla.json，TEdit 数据驱动） ----
46	
47	// 进图必预载的杂项单图(2026-08-13 大瘦身 304→88):
48	// 保留两类——①chunk 静态烘焙消费(树冠/树枝/树干/仙人掌/蘑菇顶):晚到要等
49	// invalidateAll 重烘焙,fallback 会烤进 chunk,必须预载;②液体渲染首帧可见
50	// (水/岩浆/蜂蜜/微光的基础四张+瀑布三张):首帧闪素色不可接受。
51	// 其余全部移除转懒加载:NPC_Head 旗帜头像(vmisc)/链条与 Boss 部件叠画(vmisc)/
52	// Glow 叠画(ensureVImage)/机关弹幕(弹幕渲染懒加载)/导线图集(ensureVImage)/
53	// 月总手与光之女皇部件(vmisc)/Misc_Perlin——消费方全部每帧活画,ensureVImage
54	// 未就绪跳帧、下帧自愈。注意 NPC_Head 此前 121 张盲扫 id 0-120,其中 81-120
55	// 磁盘上不存在(真文件 0-80 + 独立命名的 NPC_Head_Boss_N)= 每次进图 40 个 404。
56	export const VANILLA_MISC = [
57	  // ① chunk 烘焙族
58	  // 开关换 tile 对(全部跨表,开门/开栅态世界生成极罕见→表常未载→重烘跳格=消失~1s;
59	  // 2026-08-13 用户报地牢门,全族排查:门 10↔11/高门 388↔389/活板门 387↔386/格栅 557↔558)
60	  'vanilla/Tiles_10.png', 'vanilla/Tiles_11.png',
61	  'vanilla/Tiles_386.png', 'vanilla/Tiles_387.png', 'vanilla/Tiles_388.png', 'vanilla/Tiles_389.png',
62	  'vanilla/Tiles_557.png', 'vanilla/Tiles_558.png',
63	  ...Array.from({ length: 32 }, (_, i) => `vanilla/Tree_Tops_${i}.png`),
64	  ...Array.from({ length: 32 }, (_, i) => `vanilla/Tree_Branches_${i}.png`),
65	  ...Array.from({ length: 7 }, (_, i) => `vanilla/Tiles_5_${i}.png`),
66	  'vanilla/Tiles_323.png', 'vanilla/Tiles_72.png',  // 棕榈/发光蘑菇树干(群系专属但极小,常驻防传送闪失)
67	  'vanilla/Evil_Cactus.png', 'vanilla/Good_Cactus.png', 'vanilla/Crimson_Cactus.png',
68	  'vanilla/Shroom_Tops.png',
69	  // ② 液体首帧必需(其余 waterStyle 变体由 VanillaLiquidRenderer/WaterfallRenderer
70	  //    的 ensureVImage 活画路径按当前样式自取)
71	  'vanilla/Liquid_0.png', 'vanilla/Liquid_1.png', 'vanilla/Liquid_11.png', 'vanilla/Liquid_14.png',
72	  'vanilla/Misc_water_0.png', 'vanilla/Misc_water_1.png', 'vanilla/Misc_water_11.png', 'vanilla/Misc_water_14.png',
73	  'vanilla/Waterfall_0.png', 'vanilla/Waterfall_1.png', 'vanilla/Waterfall_14.png',
74	];
75	export interface VanillaTileMeta {
76	  name: string; key: string; sheet: string;
77	  solid: boolean; blend: boolean; framed: boolean; light: boolean;
78	  color: string; placement: string | null;
79	  grid: [number, number];      // 帧像素尺寸（蜡烛类 [16,20]）
80	  stride: [number, number];    // 表内帧步长（grid+gap，如 [18,18]）
81	  frameSize: Array<[number, number]>; // 每个 style 的占格数
82	  cols: number; rows: number;
83	  isStone?: boolean; isGrass?: boolean; mergeWith?: number | null;
84	}
85	export interface VanillaItemMeta {
86	  name: string; key: string; icon: string; createTile: number | null;
87	  /** 图集子矩形(vanilla-atlas.mjs shelf-pack 后携带;旧单体条目无此组) */
88	  ix?: number; iy?: number; iw?: number; ih?: number;
89	}
90	export interface VanillaWallMeta {
91	  name: string; key: string; sheet: string; color: string;
92	  grid: [number, number]; stride: [number, number]; cols: number; rows: number;
93	  largeFrame?: number;
94	}
95	// NPC 贴图表（纵向帧条：小动物等）
96	export interface VanillaNpcMeta { sheet: string; frameW: number; frameH: number; count: number; }
97	export interface VanillaData {
98	  tiles: Record<string, VanillaTileMeta>;
99	  items: Record<string, VanillaItemMeta>;
100	  walls: Record<string, VanillaWallMeta>;
101	  npcs?: Record<string, VanillaNpcMeta>;
102	  tileNames?: Record<string, string>;  // 全量原版 tile id → 英文名（兼容报告用）
103	  itemNames?: Record<string, string>;
104	  /** 盔甲贴图槽位序号（Armor_Head/Armor_Armor/Armor_Legs 的索引，非物品 id） */
105	  armorIndex?: Record<string, { head: number; body: number; legs: number }>;
106	}
107	
108	/** vui 键失配登记(运行期防线,2026-08-13;2026-08-14 精细化):
109	 *  二分类——【设计内回退查询】静默登记(仍入 F5 assetHealth 供审计);
110	 *  【真失配】详细 warn+调用点定位。判别:Paper_{v}_{n} 女性变体缺通道回退男体
111	 *  =PaperDoll.sheetRect 的正常路径,画面正确,不该刷屏。 */
112	const _vuiKeyMisses = new Set<string>();
113	const _vuiFallbackMisses = new Set<string>();
114	/** 设计内回退查询的键形态(命中即静默) */
115	const VUI_FALLBACK_SAFE: Array<RegExp> = [
116	  /^Player_\d+_\d+\.png$/,        // 纸娃娃变体通道回退(sheetRect ?? Player_0_N)
117	  /^Armor_Head_\d+\.png$/,         // 头甲可选槽(0=无头盔查询)
118	];
119	function vuiKeyMiss(name: string): void {
120	  const isFallback = VUI_FALLBACK_SAFE.some((re) => re.test(name));
121	  if (isFallback) { _vuiFallbackMisses.add(name); return; }  // 静默:F5 仍可见
122	  if (_vuiKeyMisses.has(name)) return;
123	  _vuiKeyMisses.add(name);
124	  // 调用点(首帧非本模块处)辅助定位:错误栈在此不可靠,给最近消费提示
125	  const near = _lastVuiConsumer ? ` 最近消费:最近一次 vui() 前 3 帧@${_lastVuiConsumer}` : '';
126	  console.warn(
127	    `[vui失配] '${name}' — 清单无此键。检查:①须带 .png 后缀 ②键拼写(vanilla-ui.json 为准) ` +
128	    `③若是新素材先跑 node scripts/vanilla-atlas.mjs 重建清单${near}`,
129	  );
130	}
131	/** vui() 调用方上下文记录(失配时给"谁在查"线索;只留最近 3 个消费点) */
132	const _vuiConsumerRing: string[] = [];
133	let _lastVuiConsumer = '';
134	export function noteVuiConsumer(where: string): void {
135	  _lastVuiConsumer = where;
136	  _vuiConsumerRing.push(where);
137	  if (_vuiConsumerRing.length > 3) _vuiConsumerRing.shift();
138	}
139	
140	/** 整图硬 alpha：alpha ≥128 → 255，<128 → 0（并清零 RGB），消除提取 PNG 的半透明镶边 */
141	function hardAlpha(img: ImageBitmap | HTMLImageElement): HTMLCanvasElement {
142	  const c = document.createElement('canvas');
143	  c.width = img.width; c.height = img.height;
144	  const ctx = c.getContext('2d')!;
145	  ctx.drawImage(img, 0, 0);
146	  const d = ctx.getImageData(0, 0, c.width, c.height);
147	  const px = d.data;
148	  for (let i = 0; i < px.length; i += 4) {
149	    if (px[i + 3] >= 128) px[i + 3] = 255;
150	    else {
151	      px[i] = 0; px[i + 1] = 0; px[i + 2] = 0; px[i + 3] = 0;
152	    }
153	  }
154	  ctx.putImageData(d, 0, 0);
155	  return c;
156	}
157	
158	export class SpriteAtlas {
159	  data = atlasJson as unknown as AtlasData;
160	  resources = resourcesJson as unknown as ResourcesData;
161	  vanilla = vanillaJson as unknown as VanillaData;
162	  images = new Map<string, ImageBitmap | ImageBitmap | HTMLImageElement | HTMLCanvasElement>();
163	  /** ★ImageBitmap 化(2026-08-14 根治):drawImage(HTMLImageElement) 走浏览器
164	   *  懒解码缓存,GPU 压力下被驱逐→静默重解码(三份 trace 14-21 万次解码风暴)。
165	   *  createImageBitmap = 自持已解码像素(原版 Texture2D 语义):绘制永不重解码,
166	   *  close() = Dispose。?bitmap=0 走旧 Image 路径(逃生门) */
167	  static readonly USE_BITMAP = typeof createImageBitmap === 'function'
168	    && !(typeof location !== 'undefined' && new URLSearchParams(location.search).has('bitmap') && location.search.includes('bitmap=0'));
169	  vimages = new Map<string, ImageBitmap | HTMLImageElement>(); // 原版 PNG（干净像素，不做 hardAlpha）
170	  /** UI 贴图（vanilla-ui/，干净像素不 hardAlpha——UI 有抗锯齿边缘） */
171	  uiimages = new Map<string, ImageBitmap | HTMLImageElement>();
172	  private uiFiles = (vanillaUiJson as { files: Record<string, string> }).files;
173	  /** 人工标注（annotator.html 导出）：sheet → spriteName → 方位标签 */
174	  annotations: Record<string, Record<string, string>> = {};
175	
176	  async load(onProgress?: (p: number) => void): Promise<void> {
177	    // 封面/Splash_*:Maples 源包的 1920×1080 启动插画(每张 ~17MB 解码 + hardAlpha
178	    // canvas 拷贝),全仓无消费方(菜单用 vanilla-ui/Logo)——启动即死重,跳过
179	    const files = Object.keys(this.data.files).filter((f) => !/封面\/Splash_/.test(f));
180	    // 原版 vanilla 素材与 vanilla-ui 贴图全部不在启动预载(8550 请求/主菜单 2GB 根因):
181	    // 图块/墙/NPC 表 → Game.newWorld/loadWorld 里 preloadVanillaWorld() 预载
182	    // (onWorldReady 之前完成,首帧 chunk 烘焙无回退);物品图标 → vicon 按需
183	    // 懒加载 + 进世界后 prefetchIcons() 后台补齐;UI 贴图 → vui() 按需
184	    // 懒加载(全部 11 处消费方每帧重查,首帧 null 自兜底)
185	    const vfiles: string[] = [];
186	    const uifiles: string[] = [];
187	    let done = 0;
188	    const total = files.length + vfiles.length + uifiles.length;
189	    await Promise.all([
190	      ...files.map((f) => new Promise<void>((resolve) => {
191	        const img = new Image();
192	        img.onload = () => {
193	          // 根源处理：整图硬 alpha —— 抗锯齿半透明像素（提取 PNG 的灰/黑镶边来源）
194	          // 二值化为 0/255，所有消费方（tile/墙/图标/角色）统一获得干净像素
195	          const hc = hardAlpha(img);
196	          this.images.set(f, hc);
197	          // ★异步升格 ImageBitmap(2026-08-19 双开 IOSurface 审计:hardAlpha 家族
198	          // 18 张/窗持久 canvas 后备;bitmap = CPU 常驻+绘制同走硬件+GPU 拷贝
199	          // 浏览器托管可驱逐 = 零持久面,与 vimages 350 张同形态)。烘焙源只在
200	          // chunk 重烘时被 drawImage,转换无感;竞态守卫:仍是同一张才替换
201	          if (typeof createImageBitmap === 'function') {
202	            createImageBitmap(hc).then((b) => {
203	              if (this.images.get(f) === hc) this.images.set(f, b);
204	            }).catch(() => { /* 保持 canvas,形态等价 */ });
205	          }
206	          done++;
207	          onProgress?.(done / total);
208	          resolve();
209	        };
210	        img.onerror = () => resolve();
211	        img.src = `sprites/${encodeURI(f)}`;
212	      })),
213	    ]);
214	    // 人工标注（可选，缺失时回退）
215	    try {
216	      const r = await fetch('sprites/annotations.json');
217	      if (r.ok) this.annotations = await r.json();
218	    } catch { /* 无标注 */ }
219	  }
220	
221	  // ---- 原版素材 API（无 Unity y 翻转，按 TEdit 网格寻址） ----
222	
223	  /** 原版图块元数据 */
224	  vmeta(sheetId: number): VanillaTileMeta | null {
225	    return this.vanilla.tiles[String(sheetId)] ?? null;
226	  }
227	
228	  /** 原版图块表取帧（col,row 从 0 起）。越界/缺失返回 null */
229	  vframe(sheetId: number, col: number, row: number): DrawRect | null {
230	    const m = this.vmeta(sheetId);
231	    if (!m) return null;
232	    const img = this.ensureVImage(m.sheet);  // 懒加载兜底(正常路径 preloadVanillaWorld 已就绪)
233	    if (!img) return null;
234	    if (col < 0 || row < 0 || col >= m.cols || row >= m.rows) return null;
235	    return { img, sx: col * m.stride[0], sy: row * m.stride[1], sw: m.grid[0], sh: m.grid[1] };
236	  }
237	
238	  /** 原版表内任意像素偏移取帧（style/显式帧：18px 步长的 frameX/frameY 直用） */
239	  vframeAt(sheetId: number, fx: number, fy: number): DrawRect | null {
240	    const m = this.vmeta(sheetId);
241	    if (!m) return null;
242	    // 与 vframe/vrect 同语义懒加载（ensureVImage）：place_v_* 物品图标走本方法,
243	    // 此前直接 vimages.get——表未载时不发加载请求,宝箱内家具类物品图标永久回退
244	    const img = this.ensureVImage(m.sheet);
245	    if (!img) return null;
246	    if (fx < 0 || fy < 0 || fx + m.grid[0] > img.width || fy + m.grid[1] > img.height) return null;
247	    return { img, sx: fx, sy: fy, sw: m.grid[0], sh: m.grid[1] };
248	  }
249	
250	  /** 原版表内任意矩形（多格物体整体取图，如墓碑 2×2 = 34×34px） */
251	  vrect(sheetId: number, fx: number, fy: number, w: number, h: number): DrawRect | null {
252	    const m = this.vmeta(sheetId);
253	    if (!m) return null;
254	    const img = this.ensureVImage(m.sheet);
255	    if (!img) return null;
256	    if (fx < 0 || fy < 0 || fx + w > img.width || fy + h > img.height) return null;
257	    return { img, sx: fx, sy: fy, sw: w, sh: h };
258	  }
259	
260	  /** 原版 NPC 贴图表取帧（纵向帧条，frameIdx 0-based）。
261	   *  未登记的 id 懒加载 vanilla/NPC_{id}.png（帧数来自 vanilla-npcs.json），首帧返回 null 下一帧生效 */
262	  private lazyNpcMeta = new Map<string, VanillaNpcMeta>();
263	  /** ⚠仅适用【纵向帧条】NPC 表。横向变体横条 NPC（如 594 风气球 = 8 列×32px 变体,
264	   *  Main.cs:23383 Frame(8,1,ai[2])）走此路径会把整条横排画出来——此类 NPC 必须
265	   *  在 Renderer.drawEnemy 加专属分支按列切片（见 drawWindyBalloon）。 */
266	  vnpc(npcId: number, frameIdx: number): DrawRect | null {
267	    let m: VanillaNpcMeta | undefined = this.vanilla.npcs?.[String(npcId)];
268	    if (!m) {
269	      const key = String(npcId);
270	      m = this.lazyNpcMeta.get(key);
271	      if (!m) {
272	        const sheet = `vanilla/NPC_${npcId}.png`;
273	        const img = this.ensureVImage(sheet); // 懒加载+去重+失败负缓存(2026-08-13 前手动 new Image 无 onerror:404 时每次调用重发请求)
274	        if (!img) return null;
275	        const frames = (vanillaNpcFrames as Record<string, number>)[key] ?? 1;
276	        const fh = Math.max(1, Math.floor(img.height / frames));
277	        const meta: VanillaNpcMeta = { sheet, frameW: img.width, frameH: fh, count: frames };
278	        this.lazyNpcMeta.set(key, meta);
279	        m = meta;
280	      }
281	    }
282	    // 已注册路径同样走 ensureVImage(2026-08-13 前直取):预载失败(onerror 静默)时
283	    // NPC 永不显示——现在 miss 会触发重载,每帧活画自愈
284	    const img = this.ensureVImage(m.sheet);
285	    if (!img) return null;
286	    const idx = Math.max(0, Math.min(m.count - 1, frameIdx));
287	    return { img, sx: 0, sy: idx * m.frameH, sw: m.frameW, sh: m.frameH };
288	  }
289	
290	  /** 原版 tile/item 英文名（全量表，未白名单的也有） */
291	  vTileName(id: number): string | null { return this.vanilla.tileNames?.[String(id)] ?? null; }
292	  vItemName(id: number): string | null { return this.vanilla.itemNames?.[String(id)] ?? null; }
293	
294	  vnpcMeta(npcId: number): VanillaNpcMeta | null {
295	    return this.vanilla.npcs?.[String(npcId)] ?? null;
296	  }
297	
298	  /** 原版杂项单图（呼吸气泡等） */
299	  /** 杂项单图(旗帜头像/链条/Boss 部件/Glow 叠画等,全为每帧活画)——
300	   *  miss 走 ensureVImage 触发懒加载:未就绪返回 null,消费方下帧自愈
301	   *  (2026-08-13 前 vimages.get 直取——脱离 VANILLA_MISC 预载即永不出现) */
302	  vmisc(path: string): DrawRect | null {
303	    const hit = this.vimages.get(path); // 命中直接返回(node 测试环境的已注入项同样有效)
304	    if (hit) return { img: hit, sx: 0, sy: 0, sw: hit.width, sh: hit.height };
305	    if (typeof Image === 'undefined') return null; // node 测试环境:无 Image,不触发加载
306	    const img = this.ensureVImage(path);
307	    if (!img) return null;
308	    return { img, sx: 0, sy: 0, sw: img.width, sh: img.height };
309	  }
310	
311	  /** UI 贴图（vanilla-ui/ 命名空间）。name 为白名单键，如 'UI_PanelBackground'。
312	   *  按需懒加载(消费方每帧重查,未就绪返回 null 自兜底)。
313	   *  ★键必须带 .png 后缀(uiFiles 键全部带)——裸键恒 null 且连请求都不发;
314	   *  每键 warn 一次(F5 报告 warn 环自动留痕;全屏地图 MapBG/Map 键失配由此类
315	   *  bug 实锤,2026-08-13) */
316	  vui(name: string): DrawRect | null {
317	    const path = this.uiFiles[name];
318	    if (!path) {
319	      vuiKeyMiss(name);
320	      return null;
321	    }
322	    const img = this.ensureUiImage(path);
323	    if (!img) return null;
324	    return { img, sx: 0, sy: 0, sw: img.width, sh: img.height };
325	  }
326	
327	  private _uiPending = new Set<string>();
328	  /** UI 贴图失败负缓存(与 ensureVImage._vImageFailed 对称,2026-08-13 补):
329	   *  清单内但 404 的键若不加终态标记,每帧重查的消费方会每帧重发请求 */
330	  private _uiFailed = new Set<string>();
331	  private ensureUiImage(file: string): ImageBitmap | ImageBitmap | HTMLImageElement | null {
332	    const hit = this.uiimages.get(file);
333	    if (hit) return hit;
334	    if (this._uiPending.has(file) || this._uiFailed.has(file)) return null;
335	    this._uiPending.add(file);
336	    const im = new Image();
337	    im.onload = () => {
338	      // ImageBitmap 桥:入表即自持已解码像素(懒解码缓存驱逐免疫)
339	      const land = (store: ImageBitmap | HTMLImageElement) => {
340	        this.uiimages.set(file, store);
341	        this._uiPending.delete(file);
342	        this._uiFailed.delete(file);
343	      };
344	      if (!SpriteAtlas.USE_BITMAP) land(im);
345	      else tryBitmapUpgrade(im, file, land, () => land(im));  // 失败回退+退避重试(2026-08-18)
346	    };
347	    im.onerror = () => { this._uiPending.delete(file); this._uiFailed.add(file); };
348	    im.src = `sprites/${encodeURI(file)}`;
349	    return null;
350	  }
351	
352	  /** 原版物品图标。构建期已 shelf-pack 进少数 Item_Atlas_k.png 图集(ix/iy/iw/ih
353	   *  子矩形,见 scripts/vanilla-atlas.mjs);旧单体条目(无矩形字段)回退整图语义。
354	   *  未加载时触发后台懒加载并返回 null(下帧生效) */
355	  vicon(itemId: number): DrawRect | null {
356	    const m = this.vanilla.items[String(itemId)];
357	    if (!m) return null;
358	    const img = this.ensureVImage(m.icon);
359	    if (!img) return null;
360	    if (m.ix !== undefined && m.iw !== undefined && m.ih !== undefined) {
361	      return { img, sx: m.ix, sy: m.iy ?? 0, sw: m.iw, sh: m.ih };
362	    }
363	    return { img, sx: 0, sy: 0, sw: img.width, sh: img.height };
364	  }
365	
366	  private _iconPending = new Set<string>();
367	  private _worldPreloaded = false;
368	  /** 懒加载完成回调(Game 注册 → ChunkCache 全量标脏:晚到的表重新烘焙
369	   *  已缓存的 chunk,否则 fallback 会永久烤进 canvas) */
370	  onVImageLoaded: ((file: string) => void) | null = null;
371	
372	  /** 预载文件清单(去重+decode)。tile/wall/NPC/misc 表与图标的统一底层 */
373	  async preloadFiles(files: Iterable<string>, onProgress?: (p: number) => void): Promise<void> {
374	    const list = [...new Set(files)];
375	    let done = 0;
376	    await Promise.all(list.map((f) => new Promise<void>((resolve) => {
377	      if (this.vimages.has(f)) { done++; onProgress?.(done / list.length); return resolve(); }
378	      const img = new Image();
379	      img.onload = () => {
380	        // ImageBitmap 桥(字节+解码双就绪的原生语义,替代 img.decode());
381	        // 晚到钩子须在 bitmap 落地后触发(消费方读的是表内对象)。
382	        // settled 门:进度/resolve 只结算一次;onVImageLoaded 在"失败落 Image→
383	        // 重试成功换 bitmap"路径会发第二次(=晚到表语义,触发对应 chunk 重烘,故意的)
384	        let settled = false;
385	        const land = (store: ImageBitmap | HTMLImageElement) => {
386	          this.vimages.set(f, store);
387	          if (!settled) { settled = true; done++; onProgress?.(done / list.length); resolve(); }
388	          this.onVImageLoaded?.(f);
389	        };
390	        if (!SpriteAtlas.USE_BITMAP) land(img);
391	        else tryBitmapUpgrade(img, f, land, () => land(img));
392	      };
393	      img.onerror = () => resolve();
394	      img.src = `sprites/${encodeURI(f)}`;
395	    })));
396	  }
397	
398	  /** 按图块 sheet id + 墙 id 预载对应贴图表。
399	   *  Game 用出生点区域类型扫描调用——只载画面涉及的表(出生点半径内实测仅
400	   *  22/378 张图块表),而不是全量 ~750 张(~250MB 解码) */
401	  preloadTileSheetsFor(tileSheets: Iterable<number>, wallIds: Iterable<number>): Promise<void> {
402	    const files = new Set<string>();
403	    for (const id of tileSheets) {
404	      const m = this.vanilla.tiles[String(id)];
405	      if (m) files.add(m.sheet);
406	    }
407	    for (const id of wallIds) {
408	      const m = this.vanilla.walls[String(id)];
409	      if (m) files.add(m.sheet);
410	    }
411	    return this.preloadFiles(files);
412	  }
413	
414	  /** 预载常驻杂项(树冠/液体/瀑布/电路)+ NPC 表(小动物)——出生点必有,量小全载 */
415	  preloadMiscAndNpcs(): Promise<void> {
416	    return this.preloadFiles([
417	      ...VANILLA_MISC,
418	      ...Object.values(this.vanilla.npcs ?? {}).map((n) => n.sheet),
419	    ]);
420	  }
421	
422	  /** 预载世界渲染所需原版表(全量,~750 张)。仅调试/兜底用;正常路径走
423	   *  preloadTileSheetsFor + preloadMiscAndNpcs 的出生点子集 */
424	  async preloadVanillaWorld(): Promise<void> {
425	    if (this._worldPreloaded) return;
426	    this._worldPreloaded = true;
427	    await Promise.all([
428	      this.preloadTileSheetsFor(
429	        Object.keys(this.vanilla.tiles).map(Number),
430	        Object.keys(this.vanilla.walls).map(Number),
431	      ),
432	      this.preloadMiscAndNpcs(),
433	    ]);
434	  }
435	  /** 按需加载 vanilla 单图(去重;失败静默)。命中返回元素,否则 null。
436	   *  渲染路径一律用此入口(经 vimg 别名)——直接 vimages.get 会绕过懒加载与
437	   *  onVImageLoaded 重烘焙钩子(棕榈树干传送消失的根因)。
438	   *  烘焙追踪(bakeTracker,2026-08-13):ChunkCache 烘焙期间置 _baking,此处
439	   *  miss 发起加载时 note、onload 到达时 onLoaded——烘焙消费的任何懒取贴图
440	   *  晚到自动触发重烘焙,不再依赖 Game.ts 的前缀白名单(白名单保留作纵深) */
441	  bakeTracker: { _baking?: boolean; note(file: string): void; noteConsumed?: (file: string) => void; onLoaded(file: string): void } | null = null;
442	  ensureVImage(file: string): ImageBitmap | ImageBitmap | HTMLImageElement | null {
443	    const hit = this.vimages.get(file);
444	    if (hit) {
445	      // 消费登记(2026-08-19 素材重制热补丁):烘焙期命中(hit)的表也要登记到
446	      // ChunkCache.chunkConsumed——替换已就位 sheet 的精确重烘依据(onBakeAssetArrived
447	      // 只覆盖 miss 晚到链,对已就位表是 no-op)。可选方法:无 ChunkCache 的环境安全
448	      if (this.bakeTracker?._baking) this.bakeTracker.noteConsumed?.(file);
449	      return hit;
450	    }
451	    // ★note 先于 pending/failed 早退(2026-08-19 用户实报"生命树贴图不及时,
452	    // 手动破坏才渲染"):加载已在飞行中(预载/他人发起)时烘焙期 ensure 会早退,
453	    // 曾把 note 一起吞掉 → 表晚到无人重烘 = 缺表 fallback 钉死。failed 同 note:
454	    // 重试成功会二次 land → onLoaded → 重烘,链路反而闭环
455	    if (this.bakeTracker?._baking) this.bakeTracker.note(file);
456	    if (this._iconPending.has(file) || this._vImageFailed.has(file)) return null;
457	    this._iconPending.add(file);
458	    const im = new Image();
459	    im.onload = () => {
460	      // ImageBitmap 桥(2026-08-14 根治):入表即自持已解码像素;晚到/烘焙
461	      // 钩子在 bitmap 落地后触发(消费方读表内对象)
462	      const land = (store: ImageBitmap | HTMLImageElement) => {
463	        this.vimages.set(file, store);
464	        this._iconPending.delete(file);
465	        this._vImageFailed.delete(file);
466	        if (this.bakeTracker) this.bakeTracker.onLoaded(file);
467	        this.onVImageLoaded?.(file);  // 晚到的表 → ChunkCache 重烘焙
468	      };
469	      if (!SpriteAtlas.USE_BITMAP) land(im);
470	      else tryBitmapUpgrade(im, file, land, () => land(im));  // 失败回退+退避重试(重试成功二次 land=晚到重烘,安全)
471	    };
472	    im.onerror = () => {
473	      this._iconPending.delete(file);
474	      this._vImageFailed.add(file);   // 永久失败:不再重复请求,供消费方分级告警
475	    };
476	    im.src = `sprites/${encodeURI(file)}`;
477	    return null;
478	  }
479	  /** 表是否已确认加载失败(404 等)——与"加载中瞬态"区分 */
480	  vImageFailed(file: string): boolean { return this._vImageFailed.has(file); }
481	  private _vImageFailed = new Set<string>();
482	
483	  // ---- 资产健康只读视图(F5 调试报告 assetHealth 段;运行期防线,2026-08-13) ----
484	  failedVImages(): string[] { return [...this._vImageFailed]; }
485	  failedUiImages(): string[] { return [...this._uiFailed]; }
486	  vuiMissKeys(): string[] { return [..._vuiKeyMisses]; }
487	  /** 设计内回退 miss(静默但可审计) */
488	  vuiFallbackMisses(): string[] { return [..._vuiFallbackMisses]; }
489	  /** 后台预取全部物品图标(保留兼容入口;预载流程请用 awaited 的 preloadIcons) */
490	  prefetchIcons(): void {
491	    void this.preloadIcons();
492	  }
493	
494	  private _iconsPromise: Promise<void> | null = null;
495	  /** 预载全部物品图标素材。图集化后清单 = 去重后的 ~3 张 Item_Atlas_k.png
496	   *  (此前 6059 张单体逐张请求);缓存 Promise——并发 await 的调用者
497	   *  都会等到同一批加载完成(此前旗标早退会让第二个调用者拿到假完成) */
498	  preloadIcons(onProgress?: (p: number) => void): Promise<void> {
499	    if (this._iconsPromise) return this._iconsPromise;
500	    const icons = [...new Set(Object.values(this.vanilla.items).map((m) => m.icon))];
501	    let done = 0;
502	    this._iconsPromise = Promise.all(icons.map((f) => new Promise<void>((resolve) => {
503	      if (this.vimages.has(f)) { done++; onProgress?.(done / icons.length); return resolve(); }
504	      const im = new Image();
505	      im.onload = () => { this.vimages.set(f, im); done++; onProgress?.(done / icons.length); resolve(); };
506	      im.onerror = () => resolve();
507	      im.src = `sprites/${encodeURI(f)}`;
508	    }))).then(() => undefined);
509	    return this._iconsPromise;
510	  }
511	
512	  /** 预载 UI 贴图按 key 前缀(如 ['Player_'] = 纸娃娃身体/发型,545 张)。
513	   *  exclude:子族前缀排除表(如 'UI_Bestiary')——面板专属子族只在面板打开时
514	   *  由 vui 懒加载自愈,不进启动/进图预载(2026-08-13 UI_ 397 键收窄用)。 */
515	  async preloadUiPrefix(prefixes: string[], onProgress?: (p: number) => void, exclude?: string[]): Promise<void> {
516	    const files = Object.entries(this.uiFiles)
517	      .filter(([k]) => prefixes.some((p) => k.startsWith(p))
518	        && !(exclude ?? []).some((e) => k.startsWith(e)))
519	      .map(([, f]) => f);
520	    return this.preloadUiFiles(files, onProgress);
521	  }
522	
523	  /** 按 UI 文件路径预载(装备中的具体 Armor 表;decode 保证首帧无解码卡顿) */
524	  async preloadUiFiles(files: Iterable<string>, onProgress?: (p: number) => void): Promise<void> {
525	    const list = [...new Set(files)];
526	    let done = 0;
527	    await Promise.all(list.map((f) => new Promise<void>((resolve) => {
528	      if (this.uiimages.has(f)) { done++; onProgress?.(done / list.length); return resolve(); }
529	      const im = new Image();
530	      im.onload = () => {
531	        // ImageBitmap 桥(2026-08-18 imglog 实锤漏网第四站:此处曾直接 set(Image)
532	        // +decode() ——预载清单含 UI_Cursor_0(菜单起每帧画)与 Player_ 纸娃娃表
533	        // (进世界起每帧画),永久 Image = trace 残余流两大恒定家族的全部来源)
534	        // settled 门:进度/resolve 只结算一次(失败重试成功会二次 land,只换表项)
535	        let settled = false;
536	        const land = (store: ImageBitmap | HTMLImageElement) => {
537	          this.uiimages.set(f, store);
538	          if (settled) return;
539	          settled = true;
540	          done++; onProgress?.(done / list.length); resolve();
541	        };
542	        if (!SpriteAtlas.USE_BITMAP) { land(im); return; }
543	        tryBitmapUpgrade(im, f, land, () => land(im));
544	      };
545	      im.onerror = () => resolve();
546	      im.src = `sprites/${encodeURI(f)}`;
547	    })));
548	  }
549	
550	  has(file: string): boolean {
551	    return this.images.has(file);
552	  }
553	
554	  /** 取精灵绘制矩形（Unity y 翻转已处理）。找不到返回 null。 */
555	  rect(file: string, sprite: string): DrawRect | null {
556	    const img = this.images.get(file);
557	    const entry = this.data.files[file];
558	    if (!img || !entry) return null;
559	    const s = entry.sprites.find((x) => x.name === sprite);
560	    if (!s) return null;
561	    return { img, sx: s.x, sy: img.height - s.y - s.h, sw: s.w, sh: s.h };
562	  }
563	
564	  animFrames(anim: string): DrawRect[] {
565	    const frames = this.resources.anims[anim] ?? [];
566	    return frames.map((f) => this.rect(f.file, f.sprite)).filter(Boolean) as DrawRect[];
567	  }
568	}
569	
570	// ---- 物品图标：一律原版 Item_N（旧 Maples UI/ 图标层已整体移除） ----
571	import { TILE_BY_KEY, TILE_DEFS } from '../data/tiles';
572	
573	/** DrawAnimationVertical(int.MaxValue, 3) 的静态等价(IsFood 全表) */
574	const FOOD = { dur: Number.MAX_SAFE_INTEGER, n: 3, static: true };
575	const FOOD_IDS: number[] = [
576	  353, 357, 967, 969, 1787, 1911, 1912, 1919, 1920, 2266, 2267, 2268, 
577	  2425, 2426, 2427, 3195, 3532, 4009, 4010, 4011, 4012, 4013, 4014, 4015, 
578	  4016, 4017, 4018, 4019, 4020, 4021, 4022, 4023, 4024, 4025, 4026, 4027, 
579	  4028, 4029, 4030, 4031, 4032, 4033, 4034, 4035, 4036, 4037, 4282, 4283, 
580	  4284, 4285, 4286, 4287, 4288, 4289, 4290, 4291, 4292, 4293, 4294, 4295, 
581	  4296, 4297, 4403, 4411, 4614, 4615, 4616, 4617, 4618, 4619, 4620, 4621, 
582	  4622, 4623, 4624, 4625, 5009, 5041, 5042, 5092, 5093, 5275, 5277, 5278, 
583	  5537, 5645, 
584	];
585	
586	/**
587	 * 物品贴图动画注册表(Main.InitializeItemAnimations :3685-3722 1:1)。
588	 * 食物族:ItemID.Sets.IsFood(:258,86 项)全部为竖 3 帧条,原版注册
589	 * DrawAnimationVertical(int.MaxValue,3) = 恒帧 0(顶部一帧);本表以 FOOD
590	 * 静态条目等价表达(切片帧高 = 总高/3)。
591	 * 物品源图是竖排多帧条(如坠星 Item_75=22×208),不切片会整条入画。
592	 * dur=tick/帧;pingPong=往返;static=true=恒帧 0(IsFood 的 int.MaxValue
593	 * 静态三帧与 NotActuallyAnimating 族)。
594	 */
595	export const ITEM_ANIMATION: Record<number, { dur: number; n: number; pingPong?: boolean; static?: boolean }> = {
596	  3581: { dur: 4, n: 4 },
597	  3580: { dur: 6, n: 4 },
598	  75: { dur: 5, n: 8, pingPong: true },    // 坠星 8 帧 PingPong 旋转
599	  575: { dur: 6, n: 4 }, 547: { dur: 6, n: 4 }, 520: { dur: 6, n: 4 },
600	  548: { dur: 6, n: 4 }, 521: { dur: 6, n: 4 }, 549: { dur: 6, n: 4 },
601	  3453: { dur: 6, n: 4 }, 3454: { dur: 6, n: 4 }, 3455: { dur: 6, n: 4 },
602	  4068: { dur: 6, n: 4, static: true },   // NotActuallyAnimating(:3701-3709)
603	  4069: { dur: 6, n: 4, static: true },
604	  4070: { dur: 6, n: 4, static: true },
605	  5644: { dur: 7, n: 9 },                 // ScryingOrb(专属着色器,垂直循环近似)
606	  // ---- 食物族(IsFood :258):竖 3 帧条,原版 int.MaxValue 恒帧 0 ----
607	  ...Object.fromEntries(FOOD_IDS.map((v) => [v, FOOD])),
608	};
609	
610	
611	/** 物品动画当前帧(DrawAnimationVertical.GetFrame 语义;tick=游戏 tick 或等价毫秒换算) */
612	export function itemAnimFrame(vid: number, tick: number): number {
613	  const a = ITEM_ANIMATION[vid];
614	  if (!a || a.static) return 0;
615	  const span = a.pingPong ? a.n * 2 - 2 : a.n;
616	  const idx = Math.floor(tick / a.dur) % span;
617	  return a.pingPong && idx >= a.n ? span - idx : idx;
618	}
619	
620	/** 把整条 DrawRect 按帧切片(vid 无动画原样返回) */
621	export function sliceItemAnimFrame(vid: number, ar: DrawRect, tick: number): DrawRect {
622	  const a = ITEM_ANIMATION[vid];
623	  if (!a || a.n <= 1) return ar;
624	  const fh = ar.sh / a.n;
625	  const f = Math.min(a.n - 1, itemAnimFrame(vid, tick));
626	  return { img: ar.img, sx: ar.sx, sy: ar.sy + Math.round(fh * f), sw: ar.sw, sh: Math.round(fh) };
627	}
628	
629	export function atlasIconForKey(atlas: SpriteAtlas, key: string): DrawRect | null {
630	  const vid = VANILLA_ITEM_ICON_MAP[key];
631	  if (vid !== undefined) return atlas.vicon(vid);
632	  // 阶段 5:vi_<id>_* 全量物品回退原版图标
633	  if (key.startsWith('vi_')) {
634	    const id = parseInt(key.slice(3), 10);
635	    if (Number.isFinite(id)) return atlas.vicon(id);
636	  }
637	  // 阶段 5:place_v_* 放置物品回退用图块贴图首帧作图标
638	  if (key.startsWith('place_v_')) {
639	    const tk = key.slice('place_'.length);
640	    const tid = TILE_BY_KEY[tk];
641	    if (tid !== undefined) {
642	      const td = TILE_DEFS[tid];
643	      // vframeAt 而非 vframe:窄条表(如压板 135 的 16×200 竖条)cols=0 会让 vframe 判越界
644	      if (td?.vanilla) return atlas.vframeAt(td.vanilla.sheet, 0, 0) ?? atlas.vframe(td.vanilla.sheet, 0, 0);
645	    }
646	  }
647	  return null;
648	}
649	
650	// 我们的 item key → 原版物品图标 id（TEdit items.json 核实；Maples 缺图标的用这层）
651	export const VANILLA_ITEM_ICON_MAP: Record<string, number> = {
652	  cs: 1547,
653	  // 电路工具(id-maps items.json 核实:530 电线/509,850,851,3612 四色扳手/510 钢丝钳/
654	  // 849 致动器/3620 致动魔杖/3625 五彩扳手/3611 宏伟蓝图)
655	  // 盔甲三件套（原版 id：胫甲 76-79 / 胸甲 80-83 / 头盔 89-92）
656	  // ---- 原版批次新材料 / 方块 / 家具 ----
657	  // wld 导入补全物品图标
658	  vi_2350_recall_potion: 2350,
659	  vi_188_healing_potion: 188,
660	  vi_282_glowstick: 282,
661	  vi_41_flaming_arrow: 41,
662	  vi_167_dynamite: 167,
663	  vi_279_throwing_knife: 279,
664	  vi_51_jester_s_arrow: 51,
665	  vi_19_gold_bar: 19,
666	  vi_302_water_walking_potion: 302,
667	  vi_305_gravitation_potion: 305,
668	  vi_43_suspicious_looking_eye: 43,
669	  vi_296_spelunker_potion: 296,
670	  vi_299_night_owl_potion: 299,
671	  vi_965_rope: 965,
672	  vi_303_archery_potion: 303,
673	  vi_304_hunter_potion: 304,
674	  vi_50_magic_mirror: 50,
675	  vi_42_shuriken: 42,
676	  vi_295_featherfall_potion: 295,
677	  vi_53_cloud_in_a_bottle: 53,
678	  vi_2329_dangersense_potion: 2329,
679	  vi_40_wooden_arrow: 40,
680	  vi_975_shoe_spikes: 975,
681	  vi_54_hermes_boots: 54,
682	  vi_301_thorns_potion: 301,
683	  vi_49_band_of_regeneration: 49,
684	  vi_2326_titan_potion: 2326,
685	  vi_297_invisibility_potion: 297,
686	  vi_166_bomb: 166,
687	  vi_5011_mace: 5011,
688	  vi_4425_shark_bait: 4425,
689	  vi_2351_teleportation_potion: 2351,
690	  vi_4460_sandcastle_bucket: 4460,
691	  vi_168_grenade: 168,
692	  vi_227_restoration_potion: 227,
693	  vi_930_flare_gun: 930,
694	  vi_931_flare: 931,
695	  vi_997_extractinator: 997,
696	  vi_52_angel_statue: 52,
697	  vi_265_hellfire_arrow: 265,
698	  vi_298_shine_potion: 298,
699	  vi_5007_dead_man_s_sweater: 5007,
700	  vi_117_meteorite_bar: 117,
701	  vi_186_breathing_reed: 186,
702	  vi_329_shadow_key: 329,
703	  vi_974_ice_torch: 974,
704	  vi_2322_mining_potion: 2322,
705	  vi_4915_tungsten_bullet: 4915,
706	  vi_946_umbrella: 946,
707	  vi_939_web_slinger: 939,
708	  vi_4870_potion_of_return: 4870,
709	  vi_288_obsidian_skin_potion: 288,
710	  vi_31_bottle: 31,
711	  vi_211_feral_claws: 211,
712	  vi_4404_inner_tube: 4404,
713	  vi_187_flipper: 187,
714	  vi_2198_ice_machine: 2198,
715	  vi_274_dark_lance: 274,
716	  vi_285_aglet: 285,
717	  vi_213_staff_of_regrowth: 213,
718	  vi_964_boomstick: 964,
719	  vi_1293_lihzahrd_power_cell: 1293,
720	  vi_2195_lihzahrd_furnace: 2195,
721	  vi_2766_solar_tablet_fragment: 2766,
722	  vi_300_battle_potion: 300,
723	  vi_2348_inferno_potion: 2348,
724	  vi_218_flamelash: 218,
725	  vi_3019_hellwing_bow: 3019,
726	  vi_112_flower_of_fire: 112,
727	  vi_220_sunfury: 220,
728	  vi_4345_can_of_worms: 4345,
729	  vi_953_climbing_claws: 953,
730	  vi_3069_wand_of_sparking: 3069,
731	  vi_212_anklet_of_the_wind: 212,
732	  vi_2204_honey_dispenser: 2204,
733	  vi_277_trident: 277,
734	  vi_863_water_walking_boots: 863,
735	  vi_751_cloud: 751,
736	  vi_155_muramasa: 155,
737	  vi_289_regeneration_potion: 289,
738	  vi_906_lava_charm: 906,
739	  vi_4055_dunerider_boots: 4055,
740	  vi_724_ice_blade: 724,
741	  vi_670_ice_boomerang: 670,
742	  vi_4061_storm_spear: 4061,
743	  vi_987_blizzard_in_a_bottle: 987,
744	  vi_4551_slice_of_hell_cake: 4551,
745	  vi_5010_treasure_magnet: 5010,
746	  vi_2323_heartreach_potion: 2323,
747	  vi_2345_lifeforce_potion: 2345,
748	  vi_290_swiftness_potion: 290,
749	  vi_291_gills_potion: 291,
750	  vi_280_spear: 280,
751	  vi_2325_builder_potion: 2325,
752	  vi_284_wooden_boomerang: 284,
753	  vi_2192_bone_welder: 2192,
754	  vi_5234_remnants_of_devotion: 5234,
755	  vi_156_cobalt_shield: 156,
756	  vi_157_aqua_scepter: 157,
757	  vi_163_blue_moon: 163,
758	  vi_113_magic_missile: 113,
759	  vi_3317_valor: 3317,
760	  vi_327_golden_key: 327,
761	  vi_164_handgun: 164,
762	  vi_294_magic_power_potion: 294,
763	  vi_4263_magic_conch: 4263,
764	  vi_4062_thunder_zapper: 4062,
765	  vi_1579_flurry_boots: 1579,
766	  vi_4056_ancient_chisel: 4056,
767	  vi_4346_encumbering_stone: 4346,
768	  vi_1319_snowball_cannon: 1319,
769	  vi_3199_ice_mirror: 3199,
770	  vi_950_ice_skates: 950,
771	  vi_4443_demonic_hellcart: 4443,
772	  vi_4737_ornate_shadow_key: 4737,
773	  vi_4276_bast_statue: 4276,
774	  vi_4262_snake_charmer_s_flute: 4262,
775	  vi_3093_herb_bag: 3093,
776	  vi_292_ironskin_potion: 292,
777	  vi_3084_radar: 3084,
778	  vi_4341_step_stool: 4341,
779	  vi_4978_fledgling_wings: 4978,
780	  vi_2197_sky_mill: 2197,
781	  vi_158_lucky_horseshoe: 158,
782	  vi_5254_blessing_from_the_heavens: 5254,
783	  vi_1156_piranha_gun: 1156,
784	  vi_1571_scourge_of_the_corruptor: 1571,
785	  vi_1260_rainbow_gun: 1260,
786	  vi_1572_staff_of_the_frost_hydra: 1572,
787	  vi_4607_desert_tiger_staff: 4607,
788	  vi_933_leaf_wand: 933,
789	  vi_832_living_wood_wand: 832,
790	  vi_4066_desert_minecart: 4066,
791	  vi_4450_shroom_minecart: 4450,
792	  vi_4423_scarab_bomb: 4423,
793	  vi_159_shiny_red_balloon: 159,
794	  vi_5258_see_the_world_for_what_it_is: 5258,
795	  vi_65_starfury: 65,
796	  vi_5388_eye_of_the_sun: 5388,
797	  vi_2219_celestial_magnet: 2219,
798	  vi_5255_love_is_in_the_trash_slot: 5255,
799	  vi_4426_bee_minecart: 4426,
800	  vi_3017_flower_boots: 3017,
801	  vi_3360_living_mahogany_wand: 3360,
802	  vi_3361_rich_mahogany_leaf_wand: 3361,
803	  vi_1309_slime_staff: 1309,
804	  vi_1845_necromantic_scroll: 1845,
805	  vi_1864_papyrus_scarab: 1864,
806	  vi_1158_pygmy_necklace: 1158,
807	  vi_3034_coin_ring: 3034,
808	  vi_308_moonglow_seeds: 308,
809	  vi_312_fireblossom_seeds: 312,
810	  vi_310_deathweed_seeds: 310,
811	  vi_307_daybloom_seeds: 307,
812	  vi_309_blinkroot_seeds: 309,
813	  vi_2357_shiverthorn_seeds: 2357,
814	  vi_311_waterleaf_seeds: 311,
815	  vi_1828_pumpkin_seed: 1828,
816	  vi_126_bottled_water: 126,
817	  vi_1134_bottled_honey: 1134,
818	  vi_3068_guide_to_plant_fiber_cordage: 3068,
819	  vi_4779_mushroom_hat: 4779,
820	  vi_4780_mushroom_vest: 4780,
821	  vi_4781_mushroom_pants: 4781,
822	vi_678_red_potion: 678,
823	  vi_281_blowpipe: 281,
824	  vi_293_mana_regeneration_potion: 293,
825	  vi_2767_solar_tablet: 2767,
826	  vi_3_stone_block: 3,
827	  vi_3213_money_trough: 3213,
828	  vi_94_wood_platform: 94,
829	  vi_2757_vortex_helmet: 2757,
830	  vi_4989_soaring_insignia: 4989,
831	  vi_75_fallen_star: 75,
832	  vi_3383_stardust_leggings: 3383,
833	  vi_4914_kaleidoscope: 4914,
834	  vi_26_stone_wall: 26,
835	  vi_1991_bug_net: 1991,
836	  vi_4828_superheated_blood: 4828,
837	  vi_3509_copper_pickaxe: 3509,
838	  vi_3507_copper_shortsword: 3507,
839	  vi_4755_grox_the_great_s_horned_cowl: 4755,
840	  vi_4756_grox_the_great_s_chestplate: 4756,
841	  vi_4757_grox_the_great_s_greaves: 4757,
842	  vi_214_hellstone_brick: 214,
843	  vi_5000_terraspark_boots: 5000,
844	  vi_5339_arcane_crystal: 5339,
845	  vi_5391_uncumbering_stone: 5391,
846	  vi_2585_slime_hook: 2585,
847	  vi_313_daybloom: 313,
848	  vi_267_guide_voodoo_doll: 267,
849	  vi_2649_steampunk_candle: 2649,
850	  vi_286_sticky_glowstick: 286,
851	  vi_3002_spelunker_glowstick: 3002,
852	  vi_4819_demon_conch: 4819,
853	  vi_1802_raven_staff: 1802,
854	  vi_3382_stardust_plate: 3382,
855	  vi_3270_item_frame: 3270,
856	  vi_3771_ancient_horn: 3771,
857	  vi_93_wood_wall: 93,
858	  vi_4281_finch_staff: 4281,
859	  vi_5407_star_royale_brick: 5407,
860	  vi_5401_lunar_rust_brick: 5401,
861	  vi_4716_mollusk_whistle: 4716,
862	  vi_3540_phantasm: 3540,
863	  vi_2176_shroomite_digging_claw: 2176,
864	  vi_2349_wrath_potion: 2349,
865	  vi_4679_morning_star: 4679,
866	  vi_1169_bone_key: 1169,
867	  vi_3863_betsy_mask: 3863,
868	  vi_3124_cell_phone: 3124,
869	  vi_3506_copper_axe: 3506,
870	  vi_4680_dark_harvest: 4680,
871	  vi_543_brown_pressure_plate: 543,
872	  vi_172_ash_block: 172,
873	  vi_171_sign: 171,
874	  vi_1723_living_wood_wall: 1723,
875	  vi_4754_grox_the_great_s_wings: 4754,
876	  vi_3353_mechanical_cart: 3353,
877	  vi_2287_winter_cape: 2287,
878	  vi_1179_chlorophyte_bullet: 1179,
879	  vi_4766_world_globe: 4766,
880	  vi_4954_celestial_starboard: 4954,
881	  vi_4730_ghostar_s_infinity_eight: 4730,
882	  vi_4758_blade_staff: 4758,
883	  vi_4765_tree_globe: 4765,
884	  vi_5342_ambrosia: 5342,
885	  vi_5328_chest_lock: 5328,
886	  vi_5343_peddler_s_satchel: 5343,
887	  vi_5285_moon_globe: 5285,
888	  vi_5289_minecart_upgrade_kit: 5289,
889	  vi_5336_advanced_combat_techniques_volume_two: 5336,
890	  vi_5451_kwad_racer_drone: 5451,
891	  vi_5359_shellphone_spawn: 5359,
892	  vi_3032_super_absorbant_sponge: 3032,
893	  vi_3031_bottomless_water_bucket: 3031,
894	  vi_509_red_wrench: 509,
895	  vi_4741_butcher_s_bloodstained_apron: 4741,
896	  vi_3065_star_wrath: 3065,
897	  vi_3063_meowmere: 3063,
898	  vi_3372_lunatic_cultist_mask: 3372,
899	  vi_1504_spectre_robe: 1504,
900	  vi_2769_cosmic_car_key: 2769,
901	  vi_216_shackle: 216,
902	  vi_4415_stone_door: 4415,
903	  vi_118_hook: 118,
904	  vi_1681_skeleton_banner: 1681,
905	  vi_283_seed: 283,
906	  vi_1173_grave_marker: 1173,
907	  vi_4379_wyvern_kite: 4379,
908	  vi_4378_xenon_moss: 4378,
909	  vi_4377_krypton_moss: 4377,
910	  vi_4376_rat_cage: 4376,
911	  vi_4375_rat: 4375,
912	  vi_4484_1_2_second_timer: 4484,
913	  vi_4824_wet_bomb: 4824,
914	  vi_4485_1_4_second_timer: 4485,
915	  vi_5378_cursed_flare: 5378,
916	  vi_5354_reflective_shades: 5354,
917	  vi_5387_raynbro_s_pants: 5387,
918	  vi_5386_raynbro_s_hoodie: 5386,
919	  vi_5390_raynbro_s_hood: 5390,
920	  vi_5338_aegis_fruit: 5338,
921	  vi_5404_cosmic_ember_brick: 5404,
922	  vi_5405_cryocore_brick: 5405,
923	  vi_5403_astra_brick: 5403,
924	  vi_346_safe: 346,
925	  vi_4829_cat_license: 4829,
926	  vi_3335_demon_heart: 3335,
927	  vi_4750_foodbarbarian_s_tattered_dragon_wings: 4750,
928	  vi_3042_phase_dye: 3042,
929	  vi_3024_skiphs_blood: 3024,
930	  vi_3054_shadowflame_knife: 3054,
931	  vi_5275_joja_cola: 5275,
932	  vi_5278_pomegranate: 5278,
933	  vi_5277_spicy_pepper: 5277,
934	  vi_5437_shellphone: 5437,
935	  vi_1507_spectre_hamaxe: 1507,
936	  vi_2250_steampunk_chest: 2250,
937	  vi_392_glass_wall: 392,
938	  vi_2699_weapon_rack: 2699,
939	  vi_3552_blue_flame_and_silver_dye: 3552,
940	  vi_5005_terraprisma: 5005,
941	  vi_4604_exotic_chew_toy: 4604,
942	  vi_4611_world_feeder_kite: 4611,
943	  vi_4649_blue_jellyfish_kite: 4649,
944	  vi_4796_dark_mage_s_tome: 4796,
945	  vi_4553_plasma_lamp: 4553,
946	  vi_4365_celestial_wand: 4365,
947	  vi_331_jungle_spores: 331,
948	  vi_2430_slimy_saddle: 2430,
949	  vi_4956_zenith: 4956,
950	  vi_2798_laser_drill: 2798,
951	  vi_2814_martian_chest: 2814,
952	  vi_210_vine: 210,
953	  vi_4371_yellow_kite: 4371,
954	  vi_4291_lemon: 4291,
955	  vi_2493_king_slime_mask: 2493,
956	  vi_1919_sugar_cookie: 1919,
957	  vi_1912_eggnog: 1912,
958	  vi_4023_grapes: 4023,
959	  vi_4792_the_black_spot: 4792,
960	  vi_529_red_pressure_plate: 529,
961	  vi_3066_smooth_marble_block: 3066,
962	  vi_183_glowing_mushroom: 183,
963	  vi_1103_slush_block: 1103,
964	  vi_2119_stone_slab: 2119,
965	  vi_593_snow_block: 593,
966	  vi_3081_marble_block: 3081,
967	  vi_1111_blue_berries: 1111,
968	  vi_1115_red_husk: 1115,
969	  vi_217_molten_hamaxe: 217,
970	  vi_122_molten_pickaxe: 122,
971	  vi_1827_bladed_glove: 1827,
972	  vi_2263_white_dynasty_wall: 2263,
973	  vi_330_obsidian_brick_wall: 330,
974	  vi_130_gray_brick_wall: 130,
975	  vi_2433_stone_slab_wall: 2433,
976	  vi_452_hornet_statue: 452,
977	  vi_453_bomb_statue: 453,
978	  vi_360_armor_statue: 360,
979	  vi_3711_wraith_statue: 3711,
980	  vi_438_star_statue: 438,
981	  vi_446_skeleton_statue: 446,
982	  vi_458_cross_statue: 458,
983	  vi_3655_scorpion_statue: 3655,
984	  vi_328_shadow_chest: 328,
985	  vi_2196_living_loom: 2196,
986	  vi_916_shadewood_work_bench: 916,
987	  vi_35_iron_anvil: 35,
988	  vi_36_work_bench: 36,
989	  vi_3240_tall_gate: 3240,
990	  vi_337_red_banner: 337,
991	  vi_3381_stardust_helmet: 3381,
992	  vi_1765_vampire_pants: 1765,
993	  vi_2859_lunar_cultist_robe: 2859,
994	  vi_2857_lunar_cultist_hood: 2857,
995	  vi_2998_summoner_emblem: 2998,
996	  vi_1175_headstone: 1175,
997	  vi_25_wooden_door: 25,
998	  vi_46_light_s_bane: 46,
999	  vi_352_keg: 352,
1000	  vi_2340_minecart_track: 2340,
1001	  vi_498_mannequin: 498,
1002	  vi_4721_mushroom_beam: 4721,
1003	  vi_819_living_wood_door: 819,
1004	  vi_1458_obsidian_door: 1458,
1005	  vi_3763_0x33_s_aviators: 3763,
1006	  vi_176_mud_block: 176,
1007	  vi_1569_vampire_knives: 1569,
1008	  vi_857_sandstorm_in_a_bottle: 857,
1009	  vi_2292_fiberglass_fishing_pole: 2292,
1010	  vi_5238_constellation: 5238,
1011	  vi_753_seaweed: 753,
1012	  vi_5120_deer_thing: 5120,
1013	  vi_5508_grim_old_barb: 5508,
1014	  vi_5465_ram_rune: 5465,
1015	  vi_5500_goat_s_tuft: 5500,
1016	  vi_5499_froggy_neckband: 5499,
1017	  vi_5507_balloony_beads: 5507,
1018	  vi_5485_chicken_charm: 5485,
1019	  vi_5502_cat_chime: 5502,
1020	  vi_5504_turkey_wattle_necklace: 5504,
1021	  vi_5506_crow_s_beak: 5506,
1022	  vi_5503_dog_collar: 5503,
1023	  vi_5534_fairy_choker: 5534,
1024	  vi_5484_cow_bell: 5484,
1025	  vi_5501_old_companion_locket: 5501,
1026	  vi_5509_vampire_pendant: 5509,
1027	  vi_5505_mean_goblin_s_spikes: 5505,
1028	  vi_5525_cursed_piper_flute: 5525,
1029	  // ---- 旧 UI 移除迁移补全（2026-08-09，全部 id 经 TEdit items.json 核实；
1030	  //      木镐/木斧原版不存在，用铜镐 3509/铜斧 3506 代位） ----
1031	};
1032	
1033	/** 独立加载器共用 ImageBitmap 桥(二期,2026-08-14):
1034	 *  用法:im.onload 里先照旧 set(Image),再调 upgradeToBitmap(im, b => map.set(k, b))
1035	 *  ——消费方每帧重查,下一帧起拿到的就是自持解码像素;契约零变化 */
1036	export function upgradeToBitmap(img: HTMLImageElement, onReady: (b: ImageBitmap) => void, onFail?: () => void): void {
1037	  if (!SpriteAtlas.USE_BITMAP) return;
1038	  tryBitmapUpgrade(img, bitmapLabel(img), onReady, () => onFail?.());
1039	}
1040	
1041	/** createImageBitmap 失败统计(2026-08-18;?imglog=1 / F5 可见)。
1042	 *  ★压力窗口期(大世界进图/GPU 预算临界)失败并不罕见——此前静默回退 Image
1043	 *  且【永不重试】= 每帧绘制的贴图(天空/群系背景)永久停在 Image 阶段,
1044	 *  解码位图被逐出时反复 LazyPixelRef(trace 残余流 ~240/s 的主源) */
1045	export const bmpFailStats = { count: 0, files: new Map<string, number>() };
1046	function bitmapLabel(img: HTMLImageElement): string {
1047	  const p = (img.src || '').split('/').filter(Boolean);
1048	  return p.slice(-2).join('/');
1049	}
1050	const BMP_RETRY_DELAYS = [10_000, 20_000, 40_000];
1051	const _bmpFailWarned = new Set<string>();
1052	function noteBmpFail(label: string, attempt: number): void {
1053	  bmpFailStats.count++;
1054	  bmpFailStats.files.set(label, (bmpFailStats.files.get(label) ?? 0) + 1);
1055	  // 每文件只警告一次(压力爆发期 50 张×3 重试=200 行会淹没警告环;计数仍全量入 stats)
1056	  if (_bmpFailWarned.has(label)) return;
1057	  _bmpFailWarned.add(label);
1058	  console.warn(`[bitmap失败] ${label} — createImageBitmap 失败(GPU 压力窗口期常见),已回退 Image`
1059	    + (attempt < BMP_RETRY_DELAYS.length ? `,${BMP_RETRY_DELAYS[attempt] / 1000}s 后自动重试` : ',放弃重试(重载页面可再试)'));
1060	}
1061	/** 带退避重试的升级:失败先让调用方落一次 Image(不缺图),10/20/40s 后重试;
1062	 *  重试成功 onReady(bitmap) 把持有方的 Image 原地换掉。
1063	 *  ★fallback 只在【首次失败】触发——后续重试失败不再重复落钩
1064	 *  (ensureVImage 的 land 会发 onVImageLoaded→chunk 重烘,重复触发=重烘风暴) */
1065	function tryBitmapUpgrade(
1066	  img: HTMLImageElement, label: string,
1067	  onReady: (b: ImageBitmap) => void, fallback: () => void, attempt = 0,
1068	): void {
1069	  let fellBack = false;
1070	  const attemptOnce = (n: number): void => {
1071	    createImageBitmap(img).then((b) => {
1072	      if (n > 0) console.log(`[bitmap重试成功] ${label}(第 ${n} 次)`);
1073	      onReady(b);
1074	    }, () => {
1075	      if (!fellBack) { fellBack = true; fallback(); }
1076	      noteBmpFail(label, n);
1077	      if (n < BMP_RETRY_DELAYS.length) {
1078	        setTimeout(() => {
1079	          if (!(img.width > 0)) return;   // 图已被释放,放弃
1080	          attemptOnce(n + 1);
1081	        }, BMP_RETRY_DELAYS[n]);
1082	      }
1083	    });
1084	  };
1085	  attemptOnce(attempt);
1086	}
1087	/** 通用 bitmap-only 加载器(2026-08-17 修 trace⑨ 收尾两个真 bug):
1088	 *  ①在飞守卫——此前未就绪期间每帧重 new Image = 请求风暴(雨/尘每粒子每帧)
1089	 *  ②失败回退存 Image——此前失败静默 = 纹理永久缺(用户报"贴图丢失")
1090	 *  ③(2026-08-18)失败回退非终态:退避重试,成功后 store(bitmap) 原地替换 */
1091	const _bmpOnlyPending = new Set<string>();
1092	export function loadBitmapOnly(
1093	  file: string, has: () => boolean, store: (x: ImageBitmap | HTMLImageElement) => void,
1094	): void {
1095	  if (has() || _bmpOnlyPending.has(file)) return;
1096	  _bmpOnlyPending.add(file);
1097	  const im = new Image();
1098	  im.onload = () => {
1099	    const land = (x: ImageBitmap | HTMLImageElement) => { store(x); _bmpOnlyPending.delete(file); };
1100	    if (!SpriteAtlas.USE_BITMAP) { land(im); return; }
1101	    tryBitmapUpgrade(im, file, (b) => land(b), () => land(im));
1102	  };
1103	  im.onerror = () => _bmpOnlyPending.delete(file);
1104	  im.src = `sprites/${file}`;
1105	}
1106	
1107	export const USE_BITMAP = SpriteAtlas.USE_BITMAP;
1108	

```


---

## 🤖 Assistant · 2026-08-19T08:55:00.031Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/public/sw.js"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:00.056Z

**📎 ToolResult**

```
1	/* SandboxWorld 资产持久缓存 Service Worker(2026-08-13)。
2	 * 职责:①拦截 /sprites|fonts|l10n|sounds|audios 的 GET 走 Cache API 磁盘缓存
3	 * (cache-first,未命中网络回填;l10n 例外=网络优先+离线回退,见 fetch 段注)——
4	 * 对 new Image()/fetch/@font-face 全透明;
5	 * ②接收页面 AssetCache 驱动器的 {init/warm/warm-cancel} 消息做优先级后台下载:
6	 *   warm 前 cache.keys() 建已缓存集,只 fetch 缺失(不重复下载+被系统清理后
7	 *   只补缺=自愈);并发 6,逐文件失败跳过,进度 postMessage 回页面。
8	 * 版本:缓存名 sw-assets-v{version},version 由页面运行时计算(vanilla.json+
9	 * vanilla-ui.json 内容 hash + 手填 CACHE_BUSTER)——activate 清除非当前版本。
10	 * 不缓存:HTML/JS/API(vite hash 自足;碰它会有更新卡壳风险)。 */
11	'use strict';
12	
13	const ASSET_RE = /\/(sprites|fonts|l10n|sounds|audios)\//;
14	const CACHE_PREFIX = 'sw-assets-v';
15	let currentVersion = '';
16	let cacheReady = null;
17	let warmAbort = false;
18	
19	const cacheName = () => CACHE_PREFIX + currentVersion;
20	function getCache() {
21	  if (!cacheReady) cacheReady = caches.open(cacheName());
22	  return cacheReady;
23	}
24	
25	self.addEventListener('install', () => self.skipWaiting());
26	
27	self.addEventListener('activate', (e) => {
28	  e.waitUntil((async () => {
29	    await self.clients.claim();
30	    const keep = cacheName();
31	    for (const name of await caches.keys()) {
32	      if (name.startsWith(CACHE_PREFIX) && name !== keep) await caches.delete(name);
33	    }
34	  })());
35	});
36	
37	self.addEventListener('fetch', (e) => {
38	  const req = e.request;
39	  // ★scheme 门(2026-08-13 用户实报):浏览器扩展注入的 chrome-extension:// 等
40	  // 请求也会进页面 SW——Cache API 只收 http(s),put 即抛
41	  // "Request scheme 'chrome-extension' is unsupported"。非 http(s) 一律放行。
42	  const url = new URL(req.url);
43	  if (url.protocol !== 'http:' && url.protocol !== 'https:') return;
44	  if (req.method !== 'GET' || !currentVersion) return;
45	  const path = url.pathname;
46	  // ② 应用壳(vite 内容寻址 JS/CSS + 文档):网络优先+离线回退——真断网也能进游戏
47	  //    (JS 带 hash,旧缓存仅在离线时兜底,在线永远走网络=更新不卡壳)
48	  const isShellJs = /^\/assets\/.+\.(js|css|woff2?)$/.test(path);
49	  const isDoc = req.destination === 'document' || path === '/' || path.endsWith('.html');
50	  if (isShellJs || isDoc) {
51	    e.respondWith((async () => {
52	      const cache = await getCache();
53	      try {
54	        const res = await fetch(req);
55	        if (res && res.ok) cache.put(req, res.clone());
56	        return res;
57	      } catch (err) {
58	        const hit = await cache.match(req);
59	        if (hit) return hit;
60	        throw err;
61	      }
62	    })());
63	    return;
64	  }
65	  // ① 资产前缀:cache-first,未命中网络回填。
66	  //    ★例外:l10n 语言包是可变配置(build-l10n 会再生成)——网络优先+离线回退。
67	  //    cache-first 曾把 2026-08-14 多语言批的新键卡死在旧包(缓存版本号只由
68	  //    vanilla.json/ui 哈希决定,l10n 重建不换版本 → SW 永远命中旧包,页面显示裸键)
69	  if (path.startsWith('/l10n/')) {
70	    e.respondWith((async () => {
71	      const cache = await getCache();
72	      try {
73	        const res = await fetch(req);
74	        if (res && res.ok && res.type === 'basic') cache.put(req, res.clone());
75	        return res;
76	      } catch (err) {
77	        const hit = await cache.match(req);
78	        if (hit) return hit;
79	        throw err;
80	      }
81	    })());
82	    return;
83	  }
84	  if (!ASSET_RE.test(path)) return;
85	  e.respondWith((async () => {
86	    const cache = await getCache();
87	    const hit = await cache.match(req);
88	    if (hit) return hit;
89	    try {
90	      const res = await fetch(req);
91	      if (res && res.ok && res.type === 'basic') cache.put(req, res.clone());
92	      return res;
93	    } catch (err) {
94	      return hit || Response.error();
95	    }
96	  })());
97	});
98	
99	async function warm(tag, urls, base) {
100	  if (lastWarm.running) return;  // 重入守卫:看门狗补发时旧 warm 未死不叠跑
101	  warmAbort = false;
102	  const done0 = base || 0;
103	  lastWarm = { done: done0, total: done0 + urls.length, failed: 0, running: true };
104	  const cache = await getCache();
105	  // pathname 归一(去前导 /):cache 条目是绝对 URL 的 pathname,清单是相对路径
106	  const have = new Set((await cache.keys()).map((r) => new URL(r.url).pathname.replace(/^\//, '')));
107	  const missing = urls.filter((u) => !have.has(u.replace(/^\//, '')));
108	  const total = done0 + urls.length;
109	  let done = total - missing.length;
110	  let failed = 0;
111	  // ---- 自适应并发(2026-08-18 用户"按下载/处理速度自适应并行";曾固定 3 路) ----
112	  // AIMD:按实测单文件完成延迟 EMA 在 [MIN_CONC, MAX_CONC] 间调节——
113	  //   快(本地/内网,ema<30ms)每 32 文件 +1 路;慢(弱网/磁盘拥塞,ema>150ms)
114	  //   路数减半。MAX=8:HTTP/1.1 浏览器同源也就 6 连接,更高无意义(HTTP/2 部署
115	  //   下 8 路流也够吃带宽)。重试等待不计入延迟(那是网络瞬态,不是容量信号)。
116	  const MIN_CONC = 2, MAX_CONC = 8, START_CONC = 3;
117	  const BREATH_EVERY = 400;
118	  const BREATH_MS = 250;         // 喘息保持:Cache API 磁盘落盘缓冲排空窗口
119	  let conc = START_CONC;
120	  let ema = 60;                  // 单文件毫秒 EMA(初值中性)
121	  let sinceTune = 0;
122	  let cursor = 0;
123	  let sinceBreath = 0;
124	  let active = 0;
125	  const breath = () => new Promise((r) => setTimeout(r, BREATH_MS));
126	  // 固定开 MAX 路 worker,用动态 conc 信号量闸住——升/降路不重建 worker 池
127	  const workers = Array.from({ length: Math.min(MAX_CONC, missing.length) }, async () => {
128	    for (;;) {
129	      if (warmAbort) return;
130	      // 信号量:活跃数超过当前 conc 档 → 让出(微任务轮询,无计时器开销)
131	      while (active >= conc) {
132	        if (warmAbort) return;
133	        await new Promise((r) => setTimeout(r, 15));
134	      }
135	      active++;
136	      try {
137	        if (sinceBreath >= BREATH_EVERY) { sinceBreath = 0; await breath(); }
138	        const i = cursor++;
139	        if (i >= missing.length) return;
140	        const u = missing[i];
141	        const t0 = Date.now();
142	        // 单文件即时重试 ×3(间隔 300/600ms):弱网瞬断就地恢复,不必等全量
143	        // 跑完后的整轮补拉(2026-08-13 可靠性 review)
144	        let ok = false;
145	        for (let attempt = 0; attempt < 3 && !ok; attempt++) {
146	          if (warmAbort) return;
147	          try {
148	            const res = await fetch(u);
149	            if (res && res.ok) { await cache.put(u, res); ok = true; }
150	            else if (attempt === 2) failed++;
151	          } catch (err) {
152	            if (attempt === 2) failed++;
153	          }
154	          if (!ok && attempt < 2) await new Promise((r) => setTimeout(r, 300 * (attempt + 1)));
155	        }
156	        // 延迟采样与调参(仅成功文件计入;失败重试的等待会污染信号)
157	        if (ok) {
158	          ema = ema * 0.9 + (Date.now() - t0) * 0.1;
159	          if (++sinceTune >= 32) {
160	            sinceTune = 0;
161	            if (ema < 30 && conc < MAX_CONC) conc++;
162	            else if (ema > 150 && conc > MIN_CONC) conc = Math.max(MIN_CONC, Math.floor(conc / 2));
163	          }
164	        }
165	        done++;
166	        sinceBreath++;
167	        lastWarm.done = done; lastWarm.failed = failed;
168	        if ((done & 7) === 0 || done === total) postProgress(tag, done, total, failed);
169	      } finally {
170	        active--;
171	      }
172	    }
173	  });
174	  await Promise.all(workers);
175	  lastWarm = { done, total, failed, running: false };
176	  postProgress(tag, done, total, failed);
177	  postMessageToPages({ type: 'warm-done', tag, done, total, failed, aborted: warmAbort, conc, emaMs: Math.round(ema) });
178	}
179	
180	/** 缓存现状查询(页面初始完成判定/清理检测;附最近一轮 warm 统计) */
181	let lastWarm = { done: 0, total: 0, failed: 0, running: false };
182	async function reportStatus() {
183	  const cache = await getCache();
184	  const cached = (await cache.keys()).length;
185	  postMessageToPages({ type: 'status', version: currentVersion, cached, warm: lastWarm });
186	}
187	
188	function postProgress(tag, done, total, failed) {
189	  postMessageToPages({ type: 'warm-progress', tag, done, total, failed });
190	}
191	function postMessageToPages(msg) {
192	  self.clients.matchAll({ includeUncontrolled: true }).then((cs) => {
193	    for (const c of cs) c.postMessage(msg);
194	  }).catch(() => {});
195	}
196	
197	self.addEventListener('message', (e) => {
198	  const d = e.data || {};
199	  // ★version 无状态化(2026-08-13 实测):SW 会被浏览器在 ~3min 处击杀,重启后
200	  // 内存里的 currentVersion 丢失——warm/status 消息必须自带 version 才能选对缓存
201	  const msgVersion = typeof d.version === 'string' && d.version ? d.version : null;
202	  if (msgVersion && msgVersion !== currentVersion) {
203	    currentVersion = msgVersion;
204	    cacheReady = null;
205	  }
206	  if (d.type === 'init') {
207	    getCache();
208	  } else if (d.type === 'warm') {
209	    if (!currentVersion) return; // 无版本(未 init 且消息未带)拒绝,防写错缓存
210	    // ★必须 waitUntil:否则 message 事件结束后 Chrome 随时终止 SW
211	    e.waitUntil(warm(d.tag || '', d.urls || [], d.base || 0).catch(() => {}));
212	  } else if (d.type === 'warm-cancel') {
213	    warmAbort = true;
214	  } else if (d.type === 'ping') {
215	    postMessageToPages({ type: 'pong', version: currentVersion });
216	  } else if (d.type === 'status') {
217	    if (!currentVersion) return;
218	    reportStatus();
219	  }
220	});
221	

```


---

## 🤖 Assistant · 2026-08-19T08:55:03.035Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at the AssetCache driver in src, the Audio.ts, and the assets-index.json structure. Also look at file counts.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:04.086Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"sw-asset-preload\\|AssetCache\\|assets-index\\|serviceWorker\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" -l | sort -u",
 "description": "Find SW registration and asset cache driver files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:04.158Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/debug/DebugReport.ts
~/Project/GLM/SandboxWorld/game/src/main.ts
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts
~/Project/GLM/SandboxWorld/game/src/net/AssetCache.ts
~/Project/GLM/SandboxWorld/game/src/remaster/RemasterManager.ts
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts

```


---

## 🤖 Assistant · 2026-08-19T08:55:07.666Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/game/public && echo \"== sprites tree ==\"; for d in sprites/*/; do printf \"%-28s %6s files  %s\\n\" \"$d\" \"$(find \"$d\" -type f | wc -l | tr -d ' ')\" \"$(du -sh \"$d\" | cut -f1)\"; done; echo \"== top files ==\"; find sprites -type f -exec du -k {} + | sort -rn | head -8; echo \"== sounds/audios ==\"; ls sounds | head; find sounds -type f | wc -l; ls audios | head; find audios -type f | wc -l",
 "description": "Count files and sizes in sprites, sounds, audios"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:07.894Z

**📎 ToolResult ⚠️ERROR**

```
glm-x-preview-260804[1m] is temporarily unavailable, so auto mode cannot determine the safety of Bash right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.

```


---

## 🤖 Assistant · 2026-08-19T08:55:10.680Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The classifier is temporarily unavailable for the compound bash command. Let me break it into simpler read-only commands. Let me use `find` and `du` separately, and read AssetCache.ts and Audio.ts meanwhile.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:10.988Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/net/AssetCache.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:11.027Z

**📎 ToolResult**

```
1	// SW 资产预载驱动器(2026-08-13,弱网/首进体验)。
2	// 设计见 plans/gleaming-singing-biscuit.md:进主菜单即按优先级全量下载到
3	// Cache API 磁盘缓存(public/sw.js 拦截服务);右下角悬浮进度 + 单人游戏门槛
4	// 弹窗在 src/ui/AssetDownloadUI.ts。本模块只做:门控/版本/优先级清单枚举/
5	// SW 消息协议/进度状态。
6	//
7	// ★版本 = fnv1a32(vanilla.json + vanilla-ui.json 内容 + CACHE_BUSTER)。
8	//   贴图清单变了 → JSON 变 → bundle 变 → version 变 → 新缓存整批重建。
9	//   只改 sounds/fonts/audios 内容时 JSON 不变 → 需手动 bump CACHE_BUSTER。
10	//   l10n 已豁免(2026-08-16 裸键事故):sw.js 对 /l10n/ 走网络优先+离线回退,
11	//   重建语言包即时生效,不再依赖版本号/CACHE_BUSTER。
12	import vanillaJson from '../../public/sprites/vanilla.json';
13	import vanillaUiJson from '../../public/sprites/vanilla-ui.json';
14	import assetsIndexJson from '../../public/assets-index.json';
15	import { MUSIC } from '../data/Music';
16	import { VANILLA_MISC } from '../assets/SpriteAtlas';
17	
18	/** 手动版本闸:仅 sounds/audios/fonts/l10n 内容变更时 +1(贴图走 JSON 内容 hash 自动) */
19	export const CACHE_BUSTER = 1;
20	
21	type VanillaMeta = { sheet?: string; icon?: string };
22	type VanillaData = {
23	  tiles?: Record<string, VanillaMeta>;
24	  walls?: Record<string, VanillaMeta>;
25	  npcs?: Record<string, VanillaMeta>;
26	  items?: Record<string, VanillaMeta>;
27	};
28	type UiFiles = Record<string, string>;
29	type AssetsIndex = { sounds?: string[]; fonts?: string[]; l10n?: string[]; miscVanilla?: string[]; miscUi?: string[] };
30	
31	// ---- 版本(纯函数,可测) ----
32	
33	export function fnv1a32(s: string): number {
34	  let h = 0x811c9dc5;
35	  for (let i = 0; i < s.length; i++) {
36	    h ^= s.charCodeAt(i);
37	    h = Math.imul(h, 0x01000193);
38	  }
39	  return h >>> 0;
40	}
41	
42	export function assetVersion(
43	  vanilla: unknown = vanillaJson,
44	  ui: unknown = vanillaUiJson,
45	  buster = CACHE_BUSTER,
46	): string {
47	  return fnv1a32(JSON.stringify(vanilla) + '|' + JSON.stringify(ui) + '|' + buster).toString(36);
48	}
49	
50	// ---- 优先级清单枚举(纯函数,可测;顺序即下载优先级 P0→P4) ----
51	
52	/** P0 菜单壳:与 main.ts 菜单预载同款前缀集(减面板专属子族)+ 字体 + 语言包 */
53	export function menuWarmUrls(uiFiles: UiFiles, index: AssetsIndex = assetsIndexJson, lang = 'zh-Hans'): string[] {
54	  const prefixes = ['UI_', 'Inventory_', 'logo', 'Logo'];
55	  const exclude = ['UI_Bestiary', 'UI_Minimap', 'UI_WorldCreation', 'UI_CharCreation',
56	    'UI_PlayerResourceSets', 'UI_Workshop', 'UI_Creative', 'UI_Wires',
57	    'UI_DisplaySlots', 'UI_Achievement', 'UI_Craft', 'UI_InfoIcon', 'UI_Settings', 'UI_Camera'];
58	  const out: string[] = [];
59	  for (const [k, v] of Object.entries(uiFiles)) {
60	    if (!prefixes.some((p) => k.startsWith(p))) continue;
61	    if (exclude.some((e) => k.startsWith(e))) continue;
62	    out.push(`sprites/${v}`);
63	  }
64	  out.push(...(index.fonts ?? []).map((f) => f));
65	  out.push('l10n/index.json', `l10n/${lang}.json`);
66	  return out;
67	}
68	
69	/** P1 游戏贴图:全部图块/墙表 + NPC 表 + VANILLA_MISC(烘焙族/门对/液体) + 物品图标图集 */
70	export function worldWarmUrls(vanilla: VanillaData = vanillaJson): string[] {
71	  const out = new Set<string>();
72	  for (const m of Object.values(vanilla.tiles ?? {})) if (m.sheet) out.add(`sprites/${m.sheet}`);
73	  for (const m of Object.values(vanilla.walls ?? {})) if (m.sheet) out.add(`sprites/${m.sheet}`);
74	  for (const m of Object.values(vanilla.npcs ?? {})) if (m.sheet) out.add(`sprites/${m.sheet}`);
75	  for (const m of Object.values(vanilla.items ?? {})) if (m.icon) out.add(`sprites/${m.icon}`);
76	  for (const f of VANILLA_MISC) out.add(`sprites/${f}`);
77	  return [...out];
78	}
79	
80	/** P2 其余贴图:assets-index 的 miscVanilla/miscUi(已剔除 P1 的表族,构建期扫盘生成) */
81	export function miscWarmUrls(index: AssetsIndex = assetsIndexJson): string[] {
82	  return [...(index.miscVanilla ?? []), ...(index.miscUi ?? [])];
83	}
84	
85	/** P3 音效全量 / P4 音乐(MUSIC 表枚举,0=None 跳过) */
86	export function soundsWarmUrls(index: AssetsIndex = assetsIndexJson): string[] {
87	  return [...(index.sounds ?? [])];
88	}
89	export function musicWarmUrls(): string[] {
90	  const ids = new Set<number>();
91	  for (const id of Object.values(MUSIC)) if (id > 0) ids.add(id);
92	  return [...ids].sort((a, b) => a - b).map((id) => `audios/music/Music_${id}.mp3`);
93	}
94	
95	export type AssetPhase = 'menu' | 'game-sprites' | 'misc-sprites' | 'sounds' | 'music';
96	export const PHASE_LABEL: Record<AssetPhase, string> = {
97	  // 展示文案由消费端走 l10n(Mods.SandboxWorld.AssetDl.Phase_*);此处仅相位键
98	  menu: 'menu', 'game-sprites': 'game-sprites', 'misc-sprites': 'misc-sprites',
99	  sounds: 'sounds', music: 'music',
100	};
101	
102	/** 全量优先级清单 + 分段边界(进度阶段名用) */
103	export function priorityPlan(): { urls: string[]; phases: Array<{ phase: AssetPhase; start: number; end: number }> } {
104	  const phases: Array<{ phase: AssetPhase; urls: string[] }> = [
105	    { phase: 'menu', urls: menuWarmUrls((vanillaUiJson as { files: UiFiles }).files) },
106	    { phase: 'game-sprites', urls: worldWarmUrls() },
107	    { phase: 'misc-sprites', urls: miscWarmUrls() },
108	    { phase: 'sounds', urls: soundsWarmUrls() },
109	    { phase: 'music', urls: musicWarmUrls() },
110	  ];
111	  const seen = new Set<string>();
112	  const urls: string[] = [];
113	  const bounds: Array<{ phase: AssetPhase; start: number; end: number }> = [];
114	  for (const p of phases) {
115	    const start = urls.length;
116	    for (const u of p.urls) {
117	      if (seen.has(u)) continue;
118	      seen.add(u);
119	      urls.push(u);
120	    }
121	    bounds.push({ phase: p.phase, start, end: urls.length });
122	  }
123	  return { urls, phases: bounds };
124	}
125	
126	// ---- 运行时状态与 SW 协议(浏览器侧;vitest 环境下均短路) ----
127	
128	export interface AssetCacheState {
129	  enabled: boolean;
130	  version: string;
131	  total: number;
132	  done: number;
133	  failed: number;
134	  phase: AssetPhase | 'done' | 'idle';
135	  warming: boolean;
136	}
137	
138	const state: AssetCacheState = {
139	  enabled: false, version: '', total: 0, done: 0, failed: 0, phase: 'idle', warming: false,
140	};
141	
142	let plan = priorityPlan();
143	state.total = plan.urls.length;
144	const progressCbs = new Set<(s: AssetCacheState) => void>();
145	
146	export function assetCacheState(): AssetCacheState { return { ...state }; }
147	
148	export function onAssetProgress(cb: (s: AssetCacheState) => void): () => void {
149	  progressCbs.add(cb);
150	  return () => progressCbs.delete(cb);
151	}
152	
153	function emit(): void {
154	  for (const cb of progressCbs) cb(assetCacheState());
155	}
156	
157	function phaseAt(done: number): AssetPhase | 'done' {
158	  for (const p of plan.phases) {
159	    if (done < p.end) return p.phase;
160	  }
161	  return 'done';
162	}
163	
164	export function assetCacheEnabled(): boolean { return state.enabled; }
165	
166	/** 全部资产就绪?(门槛判定) */
167	export function assetsComplete(): boolean {
168	  return state.enabled && state.total > 0 && state.done >= state.total && state.failed === 0;
169	}
170	
171	/** 完成态本地标志(★2026-08-18 用户报"每次 build 后进单人游戏卡下载门槛"):
172	 *  门槛真正在等的是 SW status 回包——SW 冷启动 + cache.keys() 枚举万条缓存
173	 *  要 1-2s,期间 done=0 → 门槛误显示"正在下载 0%"(实际零下载,trace 实证
174	 *  仅 133 条正常懒载)。完成态落 localStorage:门槛先查标志秒开;SW 回包
175	 *  到达后若实测缓存被清,撤销标志回到真实门槛。版本随 key 走,新资产自然失效 */
176	const COMPLETE_FLAG = 'swAssetsComplete:';
177	function writeCompleteFlag(v: boolean): void {
178	  try {
179	    if (v) localStorage.setItem(COMPLETE_FLAG + state.version, '1');
180	    else localStorage.removeItem(COMPLETE_FLAG + state.version);
181	  } catch { /* 隐私模式等 */
182	  }
183	}
184	/** 快速判定:SW 回包未达前也能凭上轮完成记录放行(代价:缓存被系统清理的
185	 *  罕见窗口里,懒载会走网络并由 SW 边下边补——自愈,可接受) */
186	export function assetsCompleteFast(): boolean {
187	  if (assetsComplete()) return true;
188	  try { return !!localStorage.getItem(COMPLETE_FLAG + state.version); } catch { return false; }
189	}
190	
191	function postToSw(msg: Record<string, unknown>): void {
192	  const sw = typeof navigator !== 'undefined' ? navigator.serviceWorker?.controller : undefined;
193	  // version 随消息走:SW 被浏览器击杀重启后内存版本丢失,靠消息里的 version 选对缓存
194	  sw?.postMessage({ version: state.version, ...msg });
195	}
196	
197	/** 注册 SW 并启动(仅生产构建;?sw=1 强制开、?nosw 关)。幂等。 */
198	export async function initAssetCache(): Promise<void> {
199	  if (state.enabled || typeof navigator === 'undefined' || !navigator.serviceWorker) return;
200	  const q = new URLSearchParams(typeof location !== 'undefined' ? location.search : '');
201	  const force = q.has('sw');
202	  if (q.has('nosw')) return;
203	  if (!force && !import.meta.env.PROD) return;               // dev 默认关(探针/HMR 零干扰)
204	  if (typeof isSecureContext !== 'undefined' && !isSecureContext) return; // 纯 http 非 localhost 降级
205	  try {
206	    state.version = assetVersion();
207	    // updateViaCache:'none':SW 脚本本身绕过 HTTP 缓存——否则部署新版 sw.js 后
208	    // 浏览器最长 24h 仍跑旧 SW(标准坑,2026-08-13)
209	    const reg = await navigator.serviceWorker.register('sw.js', { updateViaCache: 'none' });
210	    await navigator.serviceWorker.ready;
211	    const sw = navigator.serviceWorker.controller ?? reg.active ?? null;
212	    if (!sw) return;
213	    state.enabled = true;
214	    (globalThis as unknown as { __swAssetCache?: unknown }).__swAssetCache = {
215	      state: assetCacheState, warm: warmAllAssets, complete: assetsComplete,
216	    }; // 调试/探针句柄
217	    sw.postMessage({ type: 'init', version: state.version });
218	    postToSw({ type: 'status' });
219	    navigator.serviceWorker.addEventListener('message', onSwMessage);
220	    // SW 被击杀重启后 controller 会换新实例——重新对齐版本并触发看门狗续传
221	    navigator.serviceWorker.addEventListener('controllerchange', () => {
222	      postToSw({ type: 'status' });
223	      state.warming = false;
224	    });
225	    startWatchdog();
226	  } catch { /* 注册失败(老浏览器/隐私模式)→ 降级现状,零影响 */ }
227	}
228	
229	function onSwMessage(e: MessageEvent): void {
230	  const d = e.data || {};
231	  if (d.type === 'status') {
232	    // 初始判定:以 SW 实测缓存数对齐进度(被系统清理→cached 变小→重新补下)
233	    if (typeof d.cached === 'number' && d.version === state.version) {
234	      state.done = Math.min(d.cached, state.total);
235	      // 满缓存直接判定完成——免得每次进菜单空跑 23 个块(SW keys() 扫一遍×23)
236	      if (state.done >= state.total && chunkCursor === 0) {
237	        chunkCursor = plan.urls.length;
238	        state.warming = false;
239	        state.phase = 'done';
240	      }
241	      writeCompleteFlag(state.done >= state.total);   // 实测校准:满=落标志,被清理=撤销
242	      lastProgressAt = Date.now();
243	      emit();
244	    }
245	  } else if (d.type === 'warm-progress') {
246	    // done 为绝对值(SW 侧 base 偏移);failed 为当前块计数,跨块累计
247	    state.done = Math.min(d.done ?? 0, state.total);
248	    state.failed = chunkFailedAcc + (d.failed ?? 0);
249	    state.warming = true;
250	    state.phase = state.done >= state.total ? 'done' : phaseAt(state.done);
251	    lastProgressAt = Date.now();
252	    emit();
253	  } else if (d.type === 'warm-done') {
254	    chunkFailedAcc += d.failed ?? 0;
255	    state.failed = chunkFailedAcc;
256	    if ((d.done ?? 0) > chunkCursor) chunkCursor = d.done;  // 块完成→接力下一块
257	    sendChunk();
258	  }
259	}
260	
261	let lastProgressAt = 0;
262	let watchdogTimer: ReturnType<typeof setInterval> | 0 = 0;
263	/** 分块接力(2026-08-13 实测 SW 会被浏览器 ~3min 击杀,单发全量 11k 无法跑完):
264	 *  页面按 CHUNK 个文件一批发给 SW,块完成(done 消息)自动发下一块;看门狗对
265	 *  当前块停滞 >15s 补发(SW keys() 过滤=断点续传)。块粒度 500 → 单块 ~15-30s,
266	 *  远低于 SW 死亡窗口;即使整块死亡也只损失当前块,接力自愈 */
267	const CHUNK = 500;
268	let chunkCursor = 0;      // 下一块在 plan.urls 的起始下标
269	let chunkFailedAcc = 0;   // 跨块累计失败
270	let autoRetries = 0;      // 全量跑完仍有失败时的自动补拉轮数(限速期偶发失败自愈)
271	
272	function sendChunk(): void {
273	  const slice = plan.urls.slice(chunkCursor, chunkCursor + CHUNK);
274	  if (!slice.length) {
275	    // 全量跑完仍有失败 → 自动重拉一轮(keys() 过滤=只补失败项,极快);
276	    // 3 轮后放弃,交人工(门槛弹窗的"重新下载"按钮)
277	    if (chunkFailedAcc > 0 && autoRetries < 3) {
278	      autoRetries++;
279	      chunkFailedAcc = 0;
280	      state.failed = 0;
281	      chunkCursor = 0;
282	      sendChunk();
283	      return;
284	    }
285	    state.warming = false;
286	    state.phase = 'done';
287	    state.done = plan.urls.length;
288	    emit();
289	    return;
290	  }
291	  state.warming = true;
292	  state.phase = phaseAt(state.done);
293	  lastProgressAt = Date.now();
294	  postToSw({ type: 'warm', tag: 'chunk', urls: slice, base: chunkCursor });
295	}
296	
297	function startWatchdog(): void {
298	  if (watchdogTimer || typeof setInterval === 'undefined') return;
299	  watchdogTimer = setInterval(() => {
300	    if (!state.enabled || state.phase === 'done') return;
301	    // 停滞补发(SW 死亡/切后台 throttling):重发当前块,keys() 过滤只补缺
302	    if (!state.warming || Date.now() - lastProgressAt > 15_000) sendChunk();
303	  }, 5_000) as unknown as ReturnType<typeof setInterval>;
304	}
305	
306	/** 全量后台下载(进菜单即调;分块接力+断点续传,已下载跳过/被清理只补缺)。
307	 *  force=true:门槛弹窗"重新下载"按钮用——**绕过已完成早退守卫**(3 轮自动
308	 *  重试耗尽后 done>=total 恒真,不绕过则按钮点了没反应=用户永久卡死,2026-08-13) */
309	export function warmAllAssets(force = false): void {
310	  if (!state.enabled) return;
311	  if (state.warming) return;
312	  if (!force && state.done >= state.total && chunkCursor >= plan.urls.length) return; // 已完成(幂等)
313	  if (force) { chunkCursor = 0; state.done = 0; state.phase = phaseAt(0); }
314	  chunkFailedAcc = 0;
315	  autoRetries = 0;
316	  sendChunk();
317	}
318	
319	/** DebugReport/探针用:刷新计划(测试注入) */
320	export function __setPlanForTest(urls: string[], phases: Array<{ phase: AssetPhase; start: number; end: number }>): void {
321	  plan = { urls, phases };
322	  state.total = urls.length;
323	}
324	

```


---

## 🤖 Assistant · 2026-08-19T08:55:11.893Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "du -sk ~/Project/GLM/SandboxWorld/game/public/sprites/*/ | sort -rn",
 "description": "Show per-subdirectory sizes under sprites"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:11.983Z

**📎 ToolResult**

```
95156	~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/
8256	~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui/
780	~/Project/GLM/SandboxWorld/game/public/sprites/封面/
116	~/Project/GLM/SandboxWorld/game/public/sprites/地形/
112	~/Project/GLM/SandboxWorld/game/public/sprites/portraits/
44	~/Project/GLM/SandboxWorld/game/public/sprites/角色/

```


---

## 🤖 Assistant · 2026-08-19T08:55:14.816Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me get file counts, Audio.ts, Music.ts, assets-index.json structure, and the sw-asset-preload plan doc. Also main.ts / mainFlow.ts registration points and preloadSceneAssets.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:16.874Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/public/sprites -type f | wc -l; find ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla -type f | wc -l; find ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui -type f | wc -l; find ~/Project/GLM/SandboxWorld/game/public/sounds -type f | wc -l; find ~/Project/GLM/SandboxWorld/game/public/audios -type f | wc -l",
 "description": "Count files in asset directories"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:17.129Z

**📎 ToolResult**

```
   11030
    9195
    1779
     852
     106

```


---

## 🤖 Assistant · 2026-08-19T08:55:17.194Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Audio.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:17.205Z

**📎 ToolResult**

```
1	// 原版 BGM 系统（LegacyAudioSystem.cs 交叉淡化语义 1:1）：
2	// WebAudio AudioBufferSourceNode 无缝循环（loop=true，解码后内存播放，零接缝）——
3	// 修复 <audio loop> 播 mp3 的循环点卡顿 + 切曲冷启动顿挫（原版 XACT 同为解码循环）。
4	// musicFade[id] ±0.005/帧 逼近目标曲（:281 UpdateCommonTrack / :309 TowardStopping）。
5	// audios/music/Music_<id>.mp3（tools/xwb-extract.mjs 提取）。
6	import { MUSIC } from '../data/Music';
7	
8	const TITLE_ID = MUSIC.TitleIntro; // 50
9	
10	interface Track {
11	  src: AudioBufferSourceNode;
12	  gain: GainNode;
13	  fade: number;   // 0..1（≈原版 Main.musicFade[id]）
14	}
15	
16	export class AudioSystem {
17	  private ac: AudioContext | null = null;
18	  private pool = new Map<number, Track>();
19	  /** 解码 PCM 常驻上限:每首 mp3 解码后 30-45MB,104 首全驻 = GB 级;
20	   *  保留最近 MAX_BUFFERS 首(Map 迭代序=LRU),超限淘汰最旧并重解码(可接受) */
21	  private static readonly MAX_BUFFERS = 3;
22	  private buffers = new Map<number, AudioBuffer | null>();
23	  private decoding = new Set<number>();
24	  /** 目标曲目（≈原版 Main.curMusic；0 = 静音） */
25	  curMusic = 0;
26	  muted = false;
27	  /** 音乐音量 0..1（options.musicVol，M6 设置页） */
28	  volume = 0.35;
29	  private rafId = 0;
30	  private lastTs = 0;
31	
32	  constructor() {
33	    this.startLoop();
34	  }
35	
36	  private audio(): AudioContext | null {
37	    if (!this.ac) {
38	      const AC = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
39	      if (!AC) return null;
40	      this.ac = new AC();
41	    }
42	    if (this.ac.state === 'suspended') this.ac.resume().catch(() => { /* 手势前恢复被拒，播放时重试 */ });
43	    return this.ac;
44	  }
45	
46	  /** 解码缓存（每曲一次；解码失败标记 null 防重复请求;LRU 上限 MAX_BUFFERS） */
47	  private async buffer(id: number): Promise<AudioBuffer | null> {
48	    const hit = this.buffers.get(id);
49	    if (hit !== undefined) return hit;
50	    if (this.decoding.has(id)) return null; // 解码中：本帧跳过，就绪后 track() 会补建
51	    this.decoding.add(id);
52	    try {
53	      const r = await fetch(`audios/music/Music_${id}.mp3`);
54	      if (!r.ok) throw new Error(String(r.status));
55	      const buf = await this.ac!.decodeAudioData(await r.arrayBuffer());
56	      this.buffers.set(id, buf);
57	      this.evictOld();
58	      return buf;
59	    } catch {
60	      this.buffers.set(id, null); // 永久失败标记(体积零,不参与淘汰)
61	      return null;
62	    } finally {
63	      this.decoding.delete(id);
64	    }
65	  }
66	
67	  /** LRU 淘汰:超限后删最旧的可淘汰条目(非失败哨兵、非 pool 播放中)。
68	   *  一轮全扫收集候选再删,避免 refresh-continue 式死循环(全部不可淘汰时);
69	   *  只删 Map 条目,已建的 AudioBufferSourceNode 仍引用旧 buffer(播放不受影响),
70	   *  之后 track() 重建才需重解码。pool 只存交叉淡化中的曲目(tickFade 停播即
71	   *  移出),故候选不足降到上限的情形可忽略 */
72	  private evictOld(): void {
73	    if (this.buffers.size <= AudioSystem.MAX_BUFFERS) return;
74	    const evictable: number[] = [];
75	    for (const [id, buf] of this.buffers) {
76	      if (buf === null) continue;        // 失败哨兵:零体积,清了会重发 404
77	      if (this.pool.has(id)) continue;   // 播放/淡化中:track() 不可失源
78	      evictable.push(id);
79	    }
80	    for (const id of evictable) {
81	      if (this.buffers.size <= AudioSystem.MAX_BUFFERS) break;
82	      this.buffers.delete(id);
83	    }
84	  }
85	
86	  /** 建立播放源（目标曲就绪后调用；重复调用幂等） */
87	  private track(id: number) {
88	    const ac = this.audio();
89	    if (!ac) return;
90	    if (this.pool.has(id)) return;
91	    const buf = this.buffers.get(id);
92	    if (!buf) return; // 未就绪：ensureTrack 的解码回调里补建
93	    const src = ac.createBufferSource();
94	    src.buffer = buf;
95	    src.loop = true;
96	    const gain = ac.createGain();
97	    gain.gain.value = 0;
98	    src.connect(gain).connect(ac.destination);
99	    src.start();
100	    this.pool.set(id, { src, gain, fade: 0 });
101	  }
102	
103	  /** rAF 驱动淡化（原版按游戏帧 ±0.005，这里按 60fps 归一时间步进） */
104	  private startLoop() {
105	    if (this.rafId) return;
106	    const step = (ts: number) => {
107	      const dt = this.lastTs ? Math.min(100, ts - this.lastTs) : 16.7;
108	      this.lastTs = ts;
109	      const frames = dt / (1000 / 60);
110	      this.tickFade(frames * 0.005);
111	      this.rafId = requestAnimationFrame(step);
112	    };
113	    this.rafId = requestAnimationFrame(step);
114	  }
115	
116	  /** 步进淡化量 d（0.005/帧）：目标曲 fade+=d 至 1，其余 -=d 至 0 并停播 */
117	  private tickFade(d: number) {
118	    if (this.muted) {
119	      for (const [id, t] of this.pool) {
120	        if (t.fade > 0) { t.fade = 0; t.gain.gain.value = 0; }
121	      }
122	      return;
123	    }
124	    for (const [id, t] of this.pool) {
125	      const target = id === this.curMusic ? 1 : 0;
126	      if (t.fade < target) {
127	        t.fade = Math.min(target, t.fade + d);
128	        // AudioContext 挂起态（浏览器手势前）：gain 无声但源持续跑，恢复后即出声
129	      } else if (t.fade > target) {
130	        t.fade = Math.max(target, t.fade - d);
131	        if (t.fade === 0) {
132	          t.src.stop();
133	          this.pool.delete(id);
134	          continue;
135	        }
136	      }
137	      t.gain.gain.value = Math.min(1, t.fade) * this.volume;
138	    }
139	  }
140	
141	  setVolume(v: number) {
142	    this.volume = Math.max(0, Math.min(1, v));
143	  }
144	
145	  /** 切换目标曲目（≈原版 curMusic 赋值；实际音量由淡化循环渐变） */
146	  playMusic(id: number) {
147	    if (this.muted) return;
148	    if (this.curMusic === id) return;
149	    this.curMusic = id;
150	    if (id === 0) return;
151	    const ac = this.audio();
152	    if (!ac) return;
153	    // 缓冲未就绪：解码完成后补建源（此时才真正起播，无冷启动顿挫）
154	    if (!this.buffers.has(id)) {
155	      void this.buffer(id).then((buf) => { if (buf && this.curMusic === id) this.track(id); });
156	    } else {
157	      this.track(id);
158	    }
159	  }
160	
161	  /** 兼容旧调用：'title' = 原版标题曲；'main' = 交由环境选曲接管（此处仅解除标题曲） */
162	  play(which: 'title' | 'main') {
163	    if (this.muted) return;
164	    if (which === 'title') this.playMusic(TITLE_ID);
165	    else if (this.curMusic === TITLE_ID) this.playMusic(0);
166	  }
167	
168	  /** 旧昼夜变奏钩子：曲目切换已由选曲链接管（昼/夜曲不同 id），无操作 */
169	  setDayNight(_isDay: boolean) { /* no-op */ }
170	
171	  stop() {
172	    this.curMusic = 0;
173	  }
174	
175	  toggleMute(): boolean {
176	    this.muted = !this.muted;
177	    if (this.muted) this.stop();
178	    return this.muted;
179	  }
180	}
181	

```


---

## 🤖 Assistant · 2026-08-19T08:55:22.250Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now find the sound effects (SFX) system — 852 sound files under public/sounds. Let me find where sounds are fetched (Sound.ts or similar in src). Also look at assets-index.json structure, who generates it (scripts), and main.ts/mainFlow.ts registration + preloadSceneAssets.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:23.972Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"sounds/\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" -l | head; echo ---; grep -rln \"new Audio\\|AudioBuffer\\|\\.wav\\|\\.ogg\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head",
 "description": "Find sound effect loading code"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:24.214Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/net/AssetCache.ts
~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts
---
~/Project/GLM/SandboxWorld/game/src/main.ts
~/Project/GLM/SandboxWorld/game/src/ui/Settings.ts
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts
~/Project/GLM/SandboxWorld/game/src/core/Audio.ts
~/Project/GLM/SandboxWorld/game/src/core/Options.ts
~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts

```


---

## 🤖 Assistant · 2026-08-19T08:55:25.727Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/sounds | head -20; echo ---; ls ~/Project/GLM/SandboxWorld/game/public/audios; echo ---; ls ~/Project/GLM/SandboxWorld/game/public/audios/music | head -5; ls ~/Project/GLM/SandboxWorld/game/public/audios/music | wc -l",
 "description": "Inspect sounds and audios directory contents"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:25.864Z

**📎 ToolResult**

```
abigail_attack.wav
abigail_cry_0.wav
abigail_cry_1.wav
abigail_cry_2.wav
abigail_summon.wav
abigail_upgrade_0.wav
abigail_upgrade_1.wav
abigail_upgrade_2.wav
achievement_complete.wav
best_reforge.wav
blizzard_inside_building_loop.wav
blizzard_strong_loop.wav
Camera.wav
Chat.wav
chester_close_0.wav
chester_close_1.wav
chester_open_0.wav
chester_open_1.wav
Coin_0.wav
Coin_1.wav
---
main.mp3
music
title.mp3
---
Music_1.mp3
Music_10.mp3
Music_100.mp3
Music_101.mp3
Music_102.mp3
     104

```


---

## 🤖 Assistant · 2026-08-19T08:55:28.825Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts",
 "limit": 120
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:28.848Z

**📎 ToolResult**

```
1	// 音效：原版 wav 素材（public/sounds/）+ WebAudio 合成兜底。
2	// **按需加载（与贴图懒加载同策略，2026-08-10）**：不预读任何文件——播放未命中时
3	// 后台 fetch+decode（pending 防重入、failed 负缓存防 404 循环），首播走合成兜底/静默，
4	// 解码完成后后续播放命中真声。定向预热用 preloadFiles（如 Boss 召唤前取咆哮声）。
5	// hit 敌人受击 / hurt 玩家受击 / pickup 拾取 / dig 挖掘 / place 放置 / drink 饮用 / chop 砍树 / splash 落水
6	// + killed 怪物死亡 / zombie 僵尸环境声 / roar Boss咆哮 / coin 拾币 / door_open door_close / tink 敲石 / shatter 玻璃破碎 / drown 溺水
7	export type SfxName =
8	  | 'hit' | 'hurt' | 'pickup' | 'dig' | 'place' | 'drink' | 'chop' | 'splash'
9	  | 'killed' | 'pkilled' | 'zombie' | 'roar' | 'coin' | 'door_open' | 'door_close' | 'tink' | 'shatter' | 'drown'
10	  | 'menuOpen' | 'menuClose' | 'menuTick'
11	  | 'unlock'
12	  | 'bowShoot'   // 原版 SoundID.Item5（弓弦，Item.cs case 99 UseSound）
13	  | 'throw'      // 原版 SoundID.Item1（手里剑/投掷刀 UseSound）
14	  | 'explosion'  // 原版 SoundID.Item14（爆炸通用：手雷/炸弹/炸药/巨石,Projectile.cs 20+ 处）
15	  | 'rocketJet' | 'starboardJet'  // 原版 SoundID.Item13/Item24（妖精翅 4/星璇悬浮板 45 喷射音）
16	  | 'beeSummon'  // 原版 SoundID.Item173（Abeemination 蜂后召唤音，Player.cs:43185——Boss 召唤音唯一非 Roar 例外）
17	  | 'thunder'   // 原版 SoundID 43（Thunder_0-5，NewLightning 的 thunderDelay 归零时播）
18	  | 'mech'       // 原版 SoundID 28（Mech_0：器件右键切换音，Player.cs:31762/31799/31803）
19	  | 'portalOrange' | 'portalBlue' // 原版 Item_115 / Item_114（传送门弹撞块落门音，Projectile.cs:16675-16683）
20	  | 'dd2Flameburst'  // DD2_FlameburstTowerShot（Sounds/Custom/dd2_flameburst_tower_shot_0-2，AI_131 :65533）
21	  | 'dd2Ballista'    // DD2_BallistaTowerShot（AI_134 :65674）
22	  | 'dd2Explosive'   // DD2_ExplosiveTrapExplode（AI_138 :66104）
23	  | 'dd2Zap'         // DD2_LightningAuraZap（AI_137 :65947）
24	  | 'whipCrack'   // 原版 Item_152（DefaultToWhip UseSound——鞭甩响，Item.cs:47448）
25	  | 'summon'      // 原版 Item_44（召唤杖通用 UseSound）
26	  | 'eowDig'      // EOWDiggin（CreateTrackable("eow_dig") SoundID.cs:1151——EoW 三段掘地专属,
27	                  //   AI_006 :52389；此前误用 Dig_0/1/2 近似,2026-08-18 对齐）
28	  // ---- 液体六配对专属轨（SoundID.cs:823-827 CreateTrackable("liquids_*",3,Ambient)，原 Sounds/Custom/）----
29	  | 'liquidWaterLava'   // 水岩浆（TileChangeType.LavaWater）
30	  | 'liquidHoneyWater'  // 水蜂蜜
31	  | 'liquidHoneyLava'   // 岩浆蜂蜜
32	  | 'shimmerSplash'     // 微光×3：原版即 PlaySound(19,…,4) = Splash_4（case 19 style 4 音量 ×0.75，FILE_CASE_VOL 统一乘）
33	  // ---- 雕像宝箱怪三轨（SoundID.cs:1105/1107/1109 CreateTrackable，Sounds/Custom/）----
34	  | 'statueMimicScare'  // 唤醒惊吓（AI_126 :43878，音量 0.8）
35	  | 'statueMimicJump'   // 跳跃（:43892/:43900，音量 0.3）
36	  | 'statueMimicLaugh'  // 玩家死亡嘲笑 ×3 变体（:43928，音量 0.8）
37	  // ---- 枪族 UseSound（Item.cs：其余枪械通用 Item_11，此前已在库内）----
38	  | 'gunShot'      // SoundID.Item11 枪械通用
39	  | 'gunShotgun'   // SoundID.Item36 霰弹枪族 534/964/3788/4703
40	  | 'gunHandgun'   // SoundID.Item41 手枪族 164/219/1255/1929/2269/2270
41	  | 'record'      // SoundID.Item166（八音盒录音完成，Player.cs:15054）
42	  | 'mirror'      // SoundID.Item6（魔镜族 UseSound：Magic/Ice Mirror/Cell Phone/Shellphone :42297 族）
43	  | 'bombFuse'    // SoundID.BombFuse = CreateTrackable("fuse")（SoundID.cs:1153，引信嘶声循环 0.2 音量）
44	  | 'conch'       // SoundID.Item64（海螺族 UseSound：Magic/Demon Conch/Shellphone 海洋地狱款）
45	  | 'manaCrystal' // SoundID.Item29（LegacySoundStyle(2,29)：Item.cs:2657 物品 109 魔力水晶 UseSound
46	                  //   + ParticleOrchestrator.Spawn_ShimmerTownNPC :1756 城镇 NPC 微光到位音）
47	  // ---- 天气环境音循环轨（SceneState.cs:235-297 暴风雪双轨；SoundType.Ambient）----
48	  | 'blizzardStrong'    // blizzard_strong_loop（SoundID.cs:821 BlizzardStrongLoop，WithVolume(0.5)）
49	  | 'blizzardInside'    // blizzard_inside_building_loop（:819 BlizzardInsideBuildingLoop）
50	  | 'sandstormWind';    // ★登记缺失：原版沙暴无专属 wav（Sandstorm 只有视觉 shader + 风场 BGM），
51	                        //   全量 852 wav 中无 sandstorm/wind 条目——素材出现前 playLoop 恒 null
52	
53	/** 天气环境音循环轨名（Weather.update 状态机 ↔ Sfx 循环句柄的接口面） */
54	export type WeatherLoopName = 'blizzardStrong' | 'blizzardInside' | 'sandstormWind';
55	
56	/** 循环轨基础音量（SoundID 定义侧的 WithVolume，SfxName 注释同源） */
57	export const LOOP_BASE_VOL: Record<WeatherLoopName, number> = {
58	  blizzardStrong: 0.5,    // SoundID.cs:821 WithVolume(0.5f)
59	  blizzardInside: 1,      // :819 无 WithVolume → 1.0
60	  sandstormWind: 1,       // 素材缺失，占位
61	};
62	
63	/** 循环音句柄（SceneState.cs:235-297 暴风雪双轨的常驻轨管理面：
64	 *  原版 PlayTrackedSound 拿 SlotId 后每帧改 Volume，轨不拆；此处同构） */
65	export interface SfxLoop {
66	  /** 停止并释放节点（幂等） */
67	  stop(): void;
68	  /** 目标音量 0-1（setTargetAtTime 平滑逼近 ~0.2s，防切换爆音） */
69	  setVolume(v: number): void;
70	  /** 节点是否仍在发声（含缓冲解码完成后起振；pending 期为 false） */
71	  readonly playing: boolean;
72	  /** 终态（stop() 或缓冲加载失败）——调用方可丢弃重建；
73	   *  非 dead 且 !playing = 解码在途，勿重建（否则每帧泄漏 GainNode） */
74	  readonly dead: boolean;
75	}
76	
77	// 逻辑名 → 原版 wav 文件（多文件随机选 + 音高扰动；导出供测试/预热侧消费）
78	export const WAV_MAP: Record<SfxName, string[]> = {
79	  hit: ['NPC_Hit_1', 'NPC_Hit_2', 'NPC_Hit_3', 'NPC_Hit_4', 'NPC_Hit_5'],
80	  hurt: ['Player_Hit_0', 'Player_Hit_1', 'Player_Hit_2'],
81	  killed: ['NPC_Killed_1', 'NPC_Killed_2', 'NPC_Killed_3'],
82	  pkilled: ['Player_Killed'],
83	  // case 14 默认变体组 Main.rand.Next(3)（LegacySoundPlayer.cs:816）；音量 ×0.4 见 FILE_CASE_VOL
84	  zombie: ['Zombie_0', 'Zombie_1', 'Zombie_2'],
85	  // roar = boss 吼(Roar_0)——原版 NPC.cs 16 处 PlaySound(15,x,y,0) 全显式 style0;
86	  // 蠕虫掘地(:52393)/毁灭者(:50473)是 PlaySound(15,x,y) 无 style(style 默认 1)=Roar_1,
87	  // 走 playSfxWav('Roar_1') 直文件,勿用本键(曾随机二选一→一半概率播成 boss 唤醒音,
88	  // 2026-08-18 用户报"地底蠕虫音全变 boss 咆哮"修正)
89	  roar: ['Roar_0'],
90	  eowDig: ['eow_dig'],   // EoW 掘地专属轨（单文件;AI_006 :52389）
91	  pickup: ['Grab'],
92	  dig: ['Dig_0', 'Dig_1', 'Dig_2'],
93	  chop: ['Grass'],
94	  tink: ['Tink_0', 'Tink_1'],
95	  place: ['Dig_1', 'Dig_2'],
96	  shatter: ['Shatter'],
97	  coin: ['Coin_0', 'Coin_1', 'Coins'],
98	  door_open: ['Door_Opened'],
99	  door_close: ['Door_Closed'],
100	  splash: ['Splash_0', 'Splash_1'],
101	  drown: ['Drown'],
102	  bowShoot: ['Item_5'],
103	  // 菜单 UI（原版 id 10=Menu_Open / id 11=Menu_Close / id 12=Menu_Tick）
104	  menuOpen: ['Menu_Open'],
105	  menuClose: ['Menu_Close'],
106	  unlock: ['Unlock'],   // SoundID 22 Unlock（神庙钥匙开锁 WorldGen.cs:37627/金钥匙:37628）
107	  menuTick: ['Menu_Tick'],
108	  throw: ['Item_1'],
109	  explosion: ['Item_14'],
110	  rocketJet: ['Item_13'],  // SoundID.Item13（妖精翅 4 飞行喷射音，WingFrame :29034）
111	  starboardJet: ['Item_24'], // SoundID.Item24（星璇悬浮板 45 喷射音，:29716）
112	  // 2026-08-13 修正：素材提取管线把 Sounds/Custom/ 拍平进 public/sounds/ 根目录，
113	  // 此前带 'Custom/' 前缀的 fetch 恒 404（failed 静默无声）——改用平铺名
114	  dd2Flameburst: ['dd2_flameburst_tower_shot_0', 'dd2_flameburst_tower_shot_1', 'dd2_flameburst_tower_shot_2'],
115	  dd2Ballista: ['dd2_ballista_tower_shot_0', 'dd2_ballista_tower_shot_1', 'dd2_ballista_tower_shot_2'],
116	  dd2Explosive: ['dd2_explosive_trap_explode_0', 'dd2_explosive_trap_explode_1', 'dd2_explosive_trap_explode_2'],
117	  dd2Zap: ['dd2_lightning_aura_zap_0', 'dd2_lightning_aura_zap_1', 'dd2_lightning_aura_zap_2', 'dd2_lightning_aura_zap_3'],
118	  whipCrack: ['Item_152'],
119	  summon: ['Item_44'],
120	  beeSummon: ['Item_173'],

```


---

## 🤖 Assistant · 2026-08-19T08:55:30.245Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"preloadSceneAssets\\|initAssetCache\\|warmAllAssets\\|sw.js\\|serviceWorker\" ~/Project/GLM/SandboxWorld/game/src/main.ts ~/Project/GLM/SandboxWorld/game/src/mainFlow.ts | head -40",
 "description": "Find SW registration and preload call sites in main entry"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:30.331Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/main.ts:18:import { initAssetCache } from './net/AssetCache';
~/Project/GLM/SandboxWorld/game/src/main.ts:500:  void initAssetCache();
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:18:import { warmAllAssets } from './net/AssetCache';
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:809:    warmAllAssets();

```


---

## 🤖 Assistant · 2026-08-19T08:55:34.697Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at how Sfx actually fetches (fetch URL form), and the assets-index.json generation script, plus preloadSceneAssets, main.ts menu preload, mainFlow.ts context around line 809 and 500.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:36.209Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"fetch(\\|sounds/\" ~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts | head -20; echo ---; grep -rn \"assets-index\" ~/Project/GLM/SandboxWorld/game/scripts ~/Project/GLM/SandboxWorld/game/vite.config.ts 2>/dev/null | head -10",
 "description": "Find Sfx fetch URL and assets-index generator"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:36.359Z

**📎 ToolResult**

```
1:// 音效：原版 wav 素材（public/sounds/）+ WebAudio 合成兜底。
112:  // 2026-08-13 修正：素材提取管线把 Sounds/Custom/ 拍平进 public/sounds/ 根目录，
287:    fetch(`sounds/${file}.wav`)
323:      fetch('audios/music/Music_28.mp3')
418:    const p = fetch(`sounds/${file}.wav`)
---
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:470:// 产出 public/assets-index.json:页面侧 AssetCache 的 P2(其余贴图)/P3(音效)枚举源。
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:494:  writeFileSync(join(pub, 'assets-index.json'), JSON.stringify(index));
~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs:495:  console.log(`assets-index: sounds=${index.sounds.length} fonts=${index.fonts.length} l10n=${index.l10n.length} miscVanilla=${index.miscVanilla.length} miscUi=${index.miscUi.length}`);

```


---

## 🤖 Assistant · 2026-08-19T08:55:36.959Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"preloadSceneAssets\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -20",
 "description": "Find preloadSceneAssets definition and callers"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:37.076Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2442:        await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.87 + p * 0.13));
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2460:    await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.87 + p * 0.13));
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2473:  private async preloadSceneAssets(onProgress?: (label: string, p: number) => void, playerAt?: { x: number; y: number }): Promise<void> {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2613:    await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.8 + p * 0.2), opts?.playerAt);
~/Project/GLM/SandboxWorld/game/src/render/BiomeBackground.ts:225:   *  Game.preloadSceneAssets 在 onWorldReady 前调用——否则首帧背景图动态加载有闪空 */

```


---

## 🤖 Assistant · 2026-08-19T08:55:39.902Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "offset": 2400,
 "limit": 230
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:39.925Z

**📎 ToolResult**

```
2400	            [TOOL_RED, TOOL_GREEN, TOOL_BLUE, TOOL_YELLOW],
2401	            [TOOL_CUTTER, TOOL_RED, TOOL_GREEN, TOOL_BLUE, TOOL_YELLOW],
2402	            [TOOL_ACTUATOR],
2403	            [TOOL_CUTTER, TOOL_ACTUATOR],
2404	          ];
2405	          const cur = modes.findIndex((m) => m.reduce((a, b) => a | b, 0) === this.wireToolMode);
2406	          const next = modes[(cur + 1) % modes.length].reduce((a, b) => a | b, 0);
2407	          this.wireToolMode = next;
2408	          const name = next & TOOL_CUTTER
2409	            ? (next & TOOL_ACTUATOR ? Lang.text('Mods.SandboxWorld.Wire.CutActuator') : Lang.text('Mods.SandboxWorld.Wire.Cut'))
2410	            : next & TOOL_ACTUATOR ? Lang.text('Mods.SandboxWorld.Wire.Actuator') : Lang.text('Mods.SandboxWorld.Wire.All');
2411	          this.cb.onToast(Lang.text('Mods.SandboxWorld.Wire.ToolMode', name));
2412	        }
2413	      }
2414	    });
2415	  }
2416	
2417	  // ================= 生命周期 =================
2418	
2419	  async newWorld(seedText: string, width: number, height: number, onProgress?: (label: string, p: number) => void, opts?: { name?: string; evil?: -1 | 0 | 1; /** 世界尺寸档（0 小/1 中/2 大，UIWorldCreation 三档；给出时 generateWorld 以 SIZE_DIMS 派生 W/H） */ size?: import('../world/World').WorldSize; /** 世界难度 = Main.GameMode（Main.cs:2677：0 经典 1 专家 2 大师 3 旅程） */ difficulty?: number; onWorldPartial?: (world: import('../world/World').World, passIndex: number, passName: string) => void; /** worker 路径的降采样预览帧回调（位图模式） */ onPreview?: (f: import('../workers/WorldGenClient').PreviewFrame) => void }) {
2420	    this.freshlyCreated = true; // NPC 入驻公告只在新生成的世界播(WorldGen 语义)
2421	    // 原版 gen[27]"正在安置液体"(SettleLiquids :16219;UIWorldLoadState 经
2422	    // worldgenText('水体沉降') 同键转换,双路一致)
2423	    const settleLabel = () => Lang.text('LegacyWorldGen.27');
2424	    // 世界难度（Main.GameMode，Main.cs:2677）：worker/主线程两路生成完成后统一灌入——
2425	    // worker GenConfig 不带此字段，fromPacket 回 0，此处覆盖（创建 UI 已选档）
2426	    const applyDifficulty = () => { if (opts?.difficulty !== undefined) this.world.difficulty = opts.difficulty; };
2427	    // ---- worker 路径（generate + settle 一条链在后台完成，UI 全程不卡） ----
2428	    if (!this.genClient) this.genClient = new WorldGenClient();
2429	    if (await this.genClient.probe()) {
2430	      try {
2431	        this.world = await this.genClient.generate(
2432	          { width, height, size: opts?.size, seedText, name: opts?.name, evil: opts?.evil, preview: !!opts?.onPreview },
2433	          {
2434	            onPreview: opts?.onPreview,
2435	            // 进度区间映射与主线程路径一致：generate 0–0.7、settle 0.72–0.87
2436	            onProgress: (phase, label, p) => {
2437	              if (phase === 'generate') onProgress?.(label, p * 0.7);
2438	              else onProgress?.(settleLabel(), 0.72 + p * 0.15);
2439	            },
2440	          },
2441	        );
2442	        await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.87 + p * 0.13));
2443	        onProgress?.(Lang.text('Mods.SandboxWorld.Progress.Done'), 1);
2444	        applyDifficulty();
2445	        this.afterWorldLoad();
2446	        await this.minimapReady;   // 小地图拆带构建完成(见 new Minimap 注释)再进图
2447	        this.cb.onWorldReady();
2448	        return;
2449	      } catch (e) {
2450	        if (!(e instanceof WorldGenUnavailable)) throw e; // 真实业务错误（如 OOM）不吞
2451	        // worker 失败 → 落回主线程路径
2452	      }
2453	    }
2454	    // ---- 主线程 fallback（原路径原样保留：worker 不可用 + 探针依赖） ----
2455	    this.world = await generateWorld({ width, height, size: opts?.size, seedText, name: opts?.name, evil: opts?.evil, onWorldPartial: opts?.onWorldPartial }, (label, p) => onProgress?.(label, p * 0.7));
2456	    // 水体预沉降：原版二次沉降(cs:21051)自 2026-08-17 起已归位 generateWorld 管线内
2457	    //（蜂巢幼虫之后、仙人掌珊瑚之前——曾在此处/worker 生成后补跑 = 时点晚 8 个 pass，
2458	    //  #98 珊瑚/水盒/燕麦液体门读到未沉降水体）。此处不再重复沉降。
2459	    // 进图前贴图预载(用户要求:不进图后才动态加载)
2460	    await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.87 + p * 0.13));
2461	    onProgress?.(Lang.text('Mods.SandboxWorld.Progress.Done'), 1);
2462	    applyDifficulty();
2463	    this.afterWorldLoad();
2464	    await this.minimapReady;       // 同 worker 路径:拆带构建完成再进图
2465	    this.cb.onWorldReady();
2466	  }
2467	
2468	  /** 进图前统一预载:onWorldReady 之前把首帧画面涉及的贴图全部就位。
2469	   *  图块/墙表按【出生点区域类型扫描】精确预载(半径 240 实测仅 22/378 张表,
2470	   *  而非全量 ~250MB)——远行遇到的类型走懒加载,onVImageLoaded 回调全量标脏
2471	   *  chunk 自动重烘焙;物品图标全量(18MB);角色 = Player_ 全量 + 当前装备的
2472	   *  3 张 Armor 表(换装走懒加载);出生点森林背景 */
2473	  private async preloadSceneAssets(onProgress?: (label: string, p: number) => void, playerAt?: { x: number; y: number }): Promise<void> {
2474	    const a = this.atlas;
2475	    if (!a) return;
2476	    onProgress?.(Lang.text('Mods.SandboxWorld.Progress.LoadWorldTex'), 0.05);
2477	    // 画面类型扫描:只预载涉及的图块/墙表。★中心=存档玩家落点(2026-08-17 用户
2478	    // "允许加载页停一下,全部就位再进"):读档玩家常远离出生点,只扫出生点会让玩家
2479	    // 区表缺席→首烘回退绿块+2.5s 保险补丁;扫玩家点则表在加载页 await 完,零回退
2480	    const st = this.world.store;
2481	    const cx0 = playerAt ? Math.floor(playerAt.x / TILE) : this.world.spawnX;
2482	    const cy0 = playerAt ? Math.floor(playerAt.y / TILE) : this.world.spawnY;
2483	    const { tileSheets, wallIds } = this.collectSheetsAround(cx0, cy0, 240);
2484	    await Promise.all([
2485	      a.preloadTileSheetsFor(tileSheets, wallIds),
2486	      a.preloadMiscAndNpcs(),
2487	    ]);
2488	    onProgress?.(Lang.text('Mods.SandboxWorld.Progress.LoadItemIcons'), 0.15);
2489	    // 物品图标（6059 张/24MB）改为后台补齐——不再阻塞进图：渲染/道具栏走
2490	    // vicon→ensureVImage 懒加载（未就绪回退程序化图标，paintSlot 每次刷新自愈升级）；
2491	    // 补齐完成后触发一次背包刷新，把兜底图标原地替换为原版图标
2492	    void a.preloadIcons().then(() => this.cb.onInventoryChanged?.());
2493	    onProgress?.(Lang.text('Mods.SandboxWorld.Progress.LoadCharTex'), 0.7);
2494	    // Player_ 全量 545 张(77MB 解码)收窄为【当前外观所需】:纸娃娃 14 通道 × 变体
2495	    // (女性变体缺通道回退男体,故男体常备) + 发型正/帽发各 1 张 ≈ 30 张;
2496	    // 换装/更衣走 vui 懒加载 + PaperDoll 就绪预检自愈(2026-08-13)
2497	    const app = this.preloadAppearance; // ★此时 player 尚未创建(见 playerPreviewArmor 注释),勿读 this.player
2498	    const variant = app?.skinVariant ?? 0;
2499	    const hair = app?.hair ?? 0;
2500	    const playerFiles = new Set<string>();
2501	    for (const s of [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13]) {
2502	      playerFiles.add(`vanilla-ui/Player_${variant}_${s}.png`);
2503	      if (variant !== 0) playerFiles.add(`vanilla-ui/Player_0_${s}.png`); // 女体缺通道男体回退
2504	    }
2505	    playerFiles.add(`vanilla-ui/Player_Hair_${hair + 1}.png`);
2506	    playerFiles.add(`vanilla-ui/Player_HairAlt_${hair + 1}.png`); // 帽子发型头盔(小图,直接备上)
2507	    await a.preloadUiFiles(playerFiles);
2508	    // 仅当前装备的 Armor 表;换装时 vui 懒加载 + PaperDoll 就绪预检自动兜住
2509	    const armorFiles = new Set<string>();
2510	    for (const id of this.playerPreviewArmor()) {
2511	      if (id == null) continue;
2512	      const def = ITEM_DEFS[id];
2513	      if (!def) continue;
2514	      const vid = VANILLA_ITEM_ICON_MAP[def.key] ?? (def.key.startsWith('vi_') ? parseInt(def.key.slice(3), 10) : NaN);
2515	      const entry = Number.isFinite(vid) ? a.vanilla.armorIndex?.[String(vid)] : null;
2516	      if (!entry) continue;
2517	      if (entry.head) armorFiles.add(`vanilla-ui/Armor_Head_${entry.head}.png`);
2518	      if (entry.body) armorFiles.add(`vanilla-ui/Armor_Armor_${entry.body}.png`);
2519	      if (entry.legs) armorFiles.add(`vanilla-ui/Armor_Legs_${entry.legs}.png`);
2520	    }
2521	    // ★此前 armorFiles 用的是键形态(无 vanilla-ui/ 前缀),preloadUiFiles 按路径
2522	    // 直取 → 初始护甲预载一直在静默 404(靠 PaperDoll 懒加载兜底才没暴露)
2523	    await a.preloadUiFiles(armorFiles);
2524	    onProgress?.(Lang.text('Mods.SandboxWorld.Progress.LoadBg'), 0.9);
2525	    await this.renderer.biomeBg.preloadInitial(this.world);
2526	    onProgress?.(Lang.text('Mods.SandboxWorld.Progress.LoadBg'), 1);
2527	  }
2528	
2529	  /** 区域类型扫描:中心 ±R 内出现的图块 sheet id + 墙 id 集合(出生点预载/传送门共用) */
2530	  private collectSheetsAround(cx: number, cy: number, R: number): { tileSheets: Set<number>; wallIds: Set<number> } {
2531	    const st = this.world.store;
2532	    const tileSheets = new Set<number>();
2533	    const wallIds = new Set<number>();
2534	    for (let x = Math.max(0, cx - R); x < Math.min(st.w, cx + R); x++) {
2535	      for (let y = Math.max(0, cy - R); y < Math.min(st.h, cy + R); y++) {
2536	        const i = st.idx(x, y);
2537	        if (st.flags[i]) {
2538	          const vs = TILE_DEFS[st.type[i]]?.vanilla?.sheet;
2539	          if (vs !== undefined) tileSheets.add(vs);
2540	        }
2541	        if (st.wall[i] > 0) wallIds.add(st.wall[i]);
2542	      }
2543	    }
2544	    // 兜底常驻:草/泥/石表全时有(暴露地表转草、autotile 邻接)
2545	    for (const k of ['dirt', 'stone', 'grass']) {
2546	      const vs = TILE_DEFS[TILE_BY_KEY[k]]?.vanilla?.sheet;
2547	      if (vs !== undefined) tileSheets.add(vs);
2548	    }
2549	    return { tileSheets, wallIds };
2550	  }
2551	
2552	  /** 预载期的装备槽位(此时 player 尚未创建,读初始装备常量:afterWorldLoad 同源) */
2553	  private playerPreviewArmor(): Array<number | null> {
2554	    // 与 afterWorldLoad 初始装备一致:铁三件(头/胸/腿)
2555	    const ids: Array<number | null> = [null, null, null];
2556	    const order = [VI_KEY.IRON_HELMET, VI_KEY.IRON_CHAINMAIL, VI_KEY.IRON_GREAVES];
2557	    for (let k = 0; k < 3; k++) {
2558	      const id = ITEM_BY_KEY[order[k]];
2559	      ids[k] = id !== undefined ? id : null;
2560	    }
2561	    return ids;
2562	  }
2563	
2564	  /** 预热背包全部武器/弹药的弹幕贴图(2026-08-13,用户报"发射阶段回退兜底,
2565	   *  过一会才是正确贴图"):懒加载下首发射击时 Projectile_{id} 未就绪会先画短线
2566	   *  兜底。projId 链 = 弹药 shoot ?? 武器 shoot(fire 路径同式)——背包+装备槽
2567	   *  全扫(≤78 格);afterWorldLoad 与 onInventoryChanged(mainFlow)各调一次,
2568	   *  拾取新弹药/换装自动覆盖 */
2569	  prefetchInvProjectiles(): void {
2570	    // ★player 是 player!: Player(确定赋值断言)——loadWorld :2232 才实例化;
2571	    // onInventoryChanged 在存档异步加载链中可能先于赋值触发(读档时物品入包
2572	    // → 回调 → this.player.inv 崩,2026-08-13 生产构建实锤)。守护退出
2573	    if (!this.player?.inv) return;
2574	    const ids = new Set<number>();
2575	    const scan = (it: { id: number } | null | undefined) => {
2576	      if (!it) return;
2577	      const def = ITEM_DEFS[it.id];
2578	      if (!def) return;
2579	      const vid = def.vid ?? viIdFromKey(def.key);
2580	      if (!Number.isFinite(vid)) return;
2581	      const shoot = itemCombat(vid)?.shoot;
2582	      if (shoot && shoot > 0) {
2583	        ids.add(shoot);
2584	        if (shoot === 707) { ids.add(708); ids.add(709); ids.add(1110); }   // 天龙之怒右键 alt 链族（708 弧/709 弹/1110 圈）
2585	        if (shoot === 714) { ids.add(715); ids.add(716); ids.add(717); ids.add(718); }   // MK2 烟花弹族
2586	        if (shoot === 615) ids.add(616);                                    // 派对机枪彩带弹
2587	      }
2588	    };
2589	    for (const s of this.player.inv.slots) scan(s);
2590	    for (const a of this.player.inv.armor) scan(a);
2591	    if (ids.size) prefetchProjectiles(ids);
2592	  }
2593	
2594	  /** 全图液体沉降（薄封装 → settleWorldLiquids，主线程 fallback 与 worker 共用同一实现）。
2595	   *  mode 语义见 src/world/liquid/settle.ts 头注释 */
2596	  private settleLiquids(onProgress?: (p: number) => void, mode: 'gen' | 'load' = 'gen') {
2597	    return settleWorldLiquids(this.world, mode, onProgress);
2598	  }
2599	
2600	  async loadWorld(world: World, onProgress?: (label: string, p: number) => void, opts?: { settled?: boolean; playerAt?: { x: number; y: number } }) {
2601	    this.freshlyCreated = false;
2602	    this.world = world;
2603	    if (!opts?.settled) {
2604	      // 读档沉降文案=原版 gen[27] 收敛比例 50-100%(WorldFile.cs:762;主线程 fallback
2605	      // 路径与 worker 路径同款——mainFlow.loadProgressLabel)
2606	      const loadSettleLabel = (p: number) =>
2607	        Lang.text('LegacyWorldGen.27') + ' ' + Math.min(100, Math.floor(50 + p * 50)) + '%';
2608	      onProgress?.(loadSettleLabel(0), 0.5);
2609	      // 读档模式：原版 WorldFile 单轮语义（存档水体已静止，QuickWater+WaterCheck 后
2610	      // 活水极少，单轮快速收敛；残留交给运行时——不再跑生成期的 10 轮全沉降）
2611	      await this.settleLiquids((p) => onProgress?.(loadSettleLabel(p), p * 0.8), 'load');
2612	    }
2613	    await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.8 + p * 0.2), opts?.playerAt);
2614	    this.afterWorldLoad();
2615	    await this.minimapReady;       // 同生成路径:大世界拆带构建完成再进图
2616	    this.cb.onWorldReady();
2617	  }
2618	
2619	  /** 内存趋势哨兵(2026-08-14,用户定位"感觉仍有泄漏"):
2620	   *  每 5s 采样 usedJSHeapSize;环比上一采样上涨 >8MB 时打印增量行,
2621	   *  并附当 5s 窗口内 [rload] 加载的贴图数 + chunk 数变化(嫌疑面归因)。
2622	   *  JS 堆只是三维之一(另两维:GPU 显存≈live canvas 数×尺寸、解码位图≈
2623	   *  vimages 数)——snap() 一起看。window.__swMemLog 常开,?mlog=0 关 */
2624	  private memSamplePrev = 0;
2625	  private memRloadPrev = 0;
2626	  attachMemSentinel(): void {
2627	    if (new URLSearchParams(location.search).has('mlog')) return;
2628	    const perf = performance as unknown as { memory?: { usedJSHeapSize: number } };
2629	    setInterval(() => {

```


---

## 🤖 Assistant · 2026-08-19T08:55:40.642Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs",
 "offset": 455,
 "limit": 45
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:40.655Z

**📎 ToolResult**

```
455	    walkD(join(imgDir, sub), `${sub}/`);
456	  };
457	  for (const sub of SUBDIRS_UI) copySub(sub, true);
458	  for (const sub of SUBDIRS_MISC) copySub(sub, false);
459	  console.log(`bulk-family copied: ${bulk}`);
460	}
461	writeFileSync(UI_OUT_JSON, JSON.stringify(uiOut));
462	console.log(`vanilla-ui: copied=${uiCopied}`);
463	if (uiMissing.length) console.warn('UI 缺失:', uiMissing.join(', '));
464	
465	writeFileSync(OUT_JSON, JSON.stringify(out));
466	console.log(`vanilla-atlas: tiles=${Object.keys(out.tiles).length} items=${Object.keys(out.items).length} walls=${Object.keys(out.walls).length} copied=${copied}`);
467	if (missing.length) console.warn('缺失（白名单有但文件/数据不存在）:', missing.join(', '));
468	
469	// ---------- SW 资产预载索引(2026-08-13)----------
470	// 产出 public/assets-index.json:页面侧 AssetCache 的 P2(其余贴图)/P3(音效)枚举源。
471	// 音乐不走这里(页面从 data/Music.ts MUSIC 表枚举)。fonts/l10n 也列入 misc。
472	// 本脚本在 vanillaAtlasAuto 的 stale 源清单里 → dev 启动与 vite build 自动重跑;
473	// ★若只改了 sounds/fonts/l10n 内容,需手动 `node scripts/vanilla-atlas.mjs` 或
474	//   bump AssetCache.CACHE_BUSTER 使 SW 版本缓存失效。
475	{
476	  const pub = join(ROOT, 'public');
477	  const listDir = (dir, ext) => {
478	    const d = join(pub, dir);
479	    if (!existsSync(d)) return [];
480	    return readdirSync(d).filter((f) => f.endsWith(ext)).map((f) => `${dir}/${f}`).sort();
481	  };
482	  const index = {
483	    generatedAt: new Date().toISOString(),
484	    sounds: listDir('sounds', '.wav'),
485	    fonts: listDir('fonts', '.woff2'),
486	    l10n: ['l10n/index.json', ...readdirSync(join(pub, 'l10n')).filter((f) => f.endsWith('.json') && f !== 'index.json').map((f) => `l10n/${f}`)],
487	    miscVanilla: readdirSync(join(pub, 'sprites', 'vanilla'))
488	      .filter((f) => f.endsWith('.png') && !/^Item_Atlas_/.test(f) && !/^Tiles_\d+\.png$/.test(f) && !/^Wall_\d+\.png$/.test(f) && !/^NPC_\d+\.png$/.test(f))
489	      .map((f) => `sprites/vanilla/${f}`).sort(),
490	    miscUi: readdirSync(join(pub, 'sprites', 'vanilla-ui'))
491	      .filter((f) => f.endsWith('.png'))
492	      .map((f) => `sprites/vanilla-ui/${f}`).sort(),
493	  };
494	  writeFileSync(join(pub, 'assets-index.json'), JSON.stringify(index));
495	  console.log(`assets-index: sounds=${index.sounds.length} fonts=${index.fonts.length} l10n=${index.l10n.length} miscVanilla=${index.miscVanilla.length} miscUi=${index.miscUi.length}`);
496	}
497	

```


---

## 🤖 Assistant · 2026-08-19T08:55:45.274Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have a good picture. Let me check:
1. assets-index.json actual counts (head of JSON)
2. main.ts menu preload (line ~500 context) and mainFlow.ts line ~809 context
3. Whether OPFS / IndexedDB used anywhere
4. AssetDownloadUI gate
5. l10n / fonts counts

Let me also check main.ts for the menu preload flow and the atlas.load() call.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:46.698Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"OPFS\\|opfs\\|getDirectory\\|indexedDB\\|IndexedDB\\|caches\\.\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v \"^Binary\" | head -20",
 "description": "Search for OPFS and IndexedDB usage in src"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:46.781Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:623:        // 列出世界槽位并读出存档 JSON（IndexedDB → 上传给中央服务器建房）
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:881:          // ui.toast(Lang.text('Mods.SandboxWorld.Toast.Saved', where === 'idb' ? mb.toFixed(1) + ' MB → IndexedDB' : Lang.text('Mods.SandboxWorld.Save.Local')));
~/Project/GLM/SandboxWorld/game/src/remaster/PackStore.ts:1:// 素材包持久化(IndexedDB remaster blob store 高层封装,KvStore v2 之上):
~/Project/GLM/SandboxWorld/game/src/remaster/PackStore.ts:8:/** 进度 JSON 的 kv 键(★kvSetIdb 只进 IndexedDB——含 prompt 全文历史随验收
~/Project/GLM/SandboxWorld/game/src/remaster/PackStore.ts:11:/** prompt 微调(增量)的 kv 键(同上,只进 IndexedDB) */
~/Project/GLM/SandboxWorld/game/src/remaster/PackStore.ts:84:/** prompt 微调('entryKey|idx' → 增量文本;IndexedDB 通道,刷新/重开不丢)。 */
~/Project/GLM/SandboxWorld/game/src/core/Options.ts:131:   *  一次 set——此前每次 JSON.stringify 全量 + IndexedDB 写,拖动即 IO 风暴。
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:1:// 键值存储：优先 IndexedDB（容量数百 MB+，大地图存档不受 localStorage ~5MB 限制），
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:13:    const req = indexedDB.open(DB_NAME, 2);
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:16:    req.onblocked = () => console.warn('[kv] IndexedDB 升级被其他标签页阻塞(关闭旧标签页即恢复)');
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:34:/** 是否有某 key（IndexedDB 或 localStorage） */
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:50:/** 只读 IndexedDB（worker 安全：无 localStorage 依赖；大存档只进 IDB）。
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:66:/** 写入只进 IndexedDB(不占 localStorage)——大 JSON 专用:重制进度(含 prompt
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:84:/** 读取（IndexedDB 优先——大存档只进 IDB，localStorage 可能留着旧的小存档；
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:92:/** 写入：字符串 ≤ 2MB 进 localStorage（快速路径），否则只进 IndexedDB */
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts:98:    } catch { /* 超限或被禁 → 落 IndexedDB */ }

```


---

## 🤖 Assistant · 2026-08-19T08:55:48.583Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/public/assets-index.json'))\nfor k,v in d.items():\n    print(k, len(v) if isinstance(v,list) else v)\nprint('sample sounds:', d['sounds'][:2])\nprint('sample miscVanilla:', d['miscVanilla'][:2])\nprint('sample miscUi:', d['miscUi'][:2])\n\"",
 "description": "Inspect assets-index.json structure and counts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:48.808Z

**📎 ToolResult ⚠️ERROR**

```
glm-x-preview-260804[1m] is temporarily unavailable, so auto mode cannot determine the safety of Bash right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.

```


---

## 🤖 Assistant · 2026-08-19T08:55:53.330Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The python command was blocked by classifier unavailability. Let me use grep to count the entries in assets-index.json instead, or read the first part of the file with head. The file is one line. Let me use grep -o.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:55:56.814Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -o '\"sounds\":\\[[^]]*\\]' ~/Project/GLM/SandboxWorld/game/public/assets-index.json | tr ',' '\\n' | wc -l; grep -o '\"miscVanilla\":\\[[^]]*\\]' ~/Project/GLM/SandboxWorld/game/public/assets-index.json | tr ',' '\\n' | wc -l; grep -o '\"miscUi\":\\[[^]]*\\]' ~/Project/GLM/SandboxWorld/game/public/assets-index.json | tr ',' '\\n' | wc -l; grep -o '\"fonts\":\\[[^]]*\\]' ~/Project/GLM/SandboxWorld/game/public/assets-index.json | tr ',' '\\n' | wc -l; grep -o '\"l10n\":\\[[^]]*\\]' ~/Project/GLM/SandboxWorld/game/public/assets-index.json | tr ',' '\\n' | wc -l; grep -o '\"generatedAt\":\"[^\"]*\"' ~/Project/GLM/SandboxWorld/game/public/assets-index.json",
 "description": "Count entries per array in assets-index.json"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:57.074Z

**📎 ToolResult**

```
     852
    7377
    1779
       1
      13
"generatedAt":"2026-08-13T11:27:17.139Z"

```


---

## 🤖 Assistant · 2026-08-19T08:55:57.384Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/main.ts",
 "offset": 470,
 "limit": 90
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:55:57.413Z

**📎 ToolResult**

```
470	// 观察进游戏事件（mainFlow 的 enterGame 发生在 Game 回调里，这里轮询 __swGame 变化）
471	let lastGameRef: Game | null = null;
472	setInterval(() => {
473	  const g = (window as unknown as { __swGame?: Game }).__swGame ?? null;
474	  if (g && g !== lastGameRef) {
475	    lastGameRef = g;
476	    inGame = true;
477	    enterGameHooks();
478	  } else if (!g && lastGameRef) {
479	    lastGameRef = null;
480	    inGame = false;
481	  }
482	}, 250);
483	
484	// ---- 启动 ----
485	kvHas('sandboxworld.quicksave').then(async () => {
486	  // 启动加载画面（Main.DrawSplash :51908：随机三件套+淡入淡出时序+LoadingSunflower）
487	  const splashGate: { resolve: () => void } = { resolve: () => {} };
488	  const splash = showSplash({ loading: new Promise<void>((r) => { splashGate.resolve = r; }) });
489	  await loadAssets();
490	  splashGate.resolve();
491	  splash.done();
492	  if (atlas) UITextures.setAtlas(atlas);
493	  // options 先行(语言设置在 options 里),Lang.init 按 options.data.lang 加载语言包;
494	  // mainFlow 内的 options.load() 幂等,此处已加载则直接返回
495	  await options.load();
496	  await Promise.all([UIFont.load(), Lang.init(options.data.lang)]);
497	  VUI.init(root);
498	  VUI.startLoop(); // 自愈帧循环（HMR 杀不死，看门狗 1s 内重启）
499	  // SW 资产持久缓存(仅生产构建;dev 需 ?sw=1):注册后由 mainFlow.showTitle 驱动全量预载
500	  void initAssetCache();
501	  flow = createFlow(root, atlas, ui, audio);
502	
503	  // M0 验收入口：?vuidemo=1 只跑 VUI 框架演示
504	  if (new URLSearchParams(location.search).has('vuidemo')) {
505	    VUI.setState(new VuiDemoState());
506	    return;
507	  }
508	
509	  // 旁路路由：?play[=small|medium|large] 跳过主菜单直接生成世界进游戏
510	  // （主菜单 UI 改造期间绕行用；也可 ?quickload 直接读快速存档）
511	  const bootParams = new URLSearchParams(location.search);
512	  if (bootParams.has('quickload')) {
513	    void flow.quickLoad();
514	    return;
515	  }
516	  if (bootParams.has('play')) {
517	    const sz = bootParams.get('play') || 'medium';
518	    const [w, h] = sz === 'small' ? [4200, 1200] : sz === 'large' ? [8400, 2400] : [6400, 1800];
519	    void flow.newWorld('', w, h);
520	    return;
521	  }
522	
523	  flow.showTitle();
524	});
525	

```


---

## 🤖 Assistant · 2026-08-19T08:56:03.679Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait, fonts count = 1? Let me double check — the grep -o '"fonts":\[[^]]*\]' counts commas+1 entries; 1 means one entry (no comma). And l10n = 13. Let me verify the fonts dir contents and l10n contents. Also check mainFlow.ts line 809 (warmAllAssets) and the menu preload in main.ts (loadAssets / menu preload prefixes). Also the AssetDownloadUI gate. And check "sw-asset-preload" plan doc mentioned. Let me also check mainFlow showTitle and single-player gate.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:56:06.032Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/fonts ~/Project/GLM/SandboxWorld/game/public/l10n; grep -rn \"fonts/\" ~/Project/GLM/SandboxWorld/game/src/ui/UIFont.ts 2>/dev/null | head -5; grep -rn \"l10n/\" ~/Project/GLM/SandboxWorld/game/src/i18n/*.ts 2>/dev/null | head -5",
 "description": "List fonts and l10n files and their consumers"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:06.165Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/public/fonts:
fusion-pixel-12px-proportional-zh_hans.ttf.woff2
OFL.txt

~/Project/GLM/SandboxWorld/game/public/l10n:
de-DE.json
en-US.json
es-ES.json
fr-FR.json
index.json
it-IT.json
ja-JP.json
ko-KR.json
pl-PL.json
pt-BR.json
ru-RU.json
zh-Hans.json
zh-Hant.json
~/Project/GLM/SandboxWorld/game/src/i18n/GameCulture.ts:3:// 与 public/l10n/index.json 同源(scripts/build-l10n.mjs 的 CULTURES 表)。
~/Project/GLM/SandboxWorld/game/src/i18n/Lang.ts:4:// 数据 = public/l10n/<culture>.json(scripts/build-l10n.mjs 构建,扁平
~/Project/GLM/SandboxWorld/game/src/i18n/Lang.ts:15:  /** 语言列表(设置面板数据源,来自 l10n/index.json) */
~/Project/GLM/SandboxWorld/game/src/i18n/RandomText.ts:1:// 原版随机文本体系 1:1 移植（数据全部来自 l10n/zh-Hans.json 分节，零硬编码文案）。
~/Project/GLM/SandboxWorld/game/src/i18n/LanguageManager.ts:171:  cultures: LangCultureInfo[] = [];            // 来自 public/l10n/index.json(设置面板数据源)

```


---

## 🤖 Assistant · 2026-08-19T08:56:06.604Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/mainFlow.ts",
 "limit": 80,
 "offset": 770
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:06.616Z

**📎 ToolResult**

```
770	  function openBestiary() {
771	    if (document.querySelector('.sw-bst')) return;  // 已开守卫(2026-08-13 泄露 review:叠层累积 Esc 捕获)
772	    const g = game;
773	    if (!g) return;
774	    const wasPaused = g.paused;
775	    const wasBlocking = g.input.uiBlocking;
776	    g.paused = true;
777	    g.input.uiBlocking = true;
778	    new BestiaryPanel(root, {
779	      getTracker: () => g.world.bestiary,
780	      atlas,
781	      isCrimson: () => g.world.crimson,
782	      onBack: () => {
783	        if (!wasPaused) g.paused = false;
784	        if (!wasBlocking) g.input.uiBlocking = false;
785	      },
786	    });
787	  }
788	
789	  /** 住房面板（原版背包房屋界面 B 方案）：不暂停世界（要点击世界分配/查询）；
790	   *  光标态双向同步（面板选择 → game.housingMode;Game 单发完成 → onHousingCursor
791	   *  → 面板自毁）。Esc/再点按钮 = 取消光标并关面板。 */
792	  async function openHousing() {
793	    const g = game;
794	    if (!g) return;
795	    document.querySelector('.sw-housing-panel')?.remove();
796	    const { HousingPanel } = await import('./ui/HousingPanel');
797	    const panel = new HousingPanel(g,
798	      (m) => { g.housingMode = m; },
799	      () => { /* onClosed: 仅自毁 */ });
800	    panel.canvas.classList.add('sw-housing-panel');
801	    (window as unknown as { __swHousingPanel?: unknown }).__swHousingPanel = panel;
802	  }
803	
804	  function showTitle() {
805	    audio.play('title');
806	    ui.closeAll();
807	    // SW 资产预载(仅生产构建):进菜单即按优先级全量后台下载 + 挂右下角进度徽标
808	    // (warmAll 幂等,SW 侧 keys() 过滤已下载;被系统清理只补缺=自愈)
809	    warmAllAssets();
810	    mountAssetBadge();
811	    if (!menuBg) {
812	      menuBg = new MenuBackground(root);
813	      (window as unknown as { __swMenuBg?: MenuBackground }).__swMenuBg = menuBg; // 调试句柄
814	    }
815	    titleMenu?.destroy();
816	    titleMenu = new TitleMenu(root, {
817	      onSinglePlayer: () => gateAssetsOrRun(() => showCharacterSelect()),
818	      onSettings: () => openSettings(false),
819	      onQuit: () => ui.toast(Lang.text('Mods.SandboxWorld.Toast.QuitUnsupported')),
820	      onCredits: () => ui.toast(Lang.text('Mods.SandboxWorld.CreditsLine')),
821	      onMultiplayer: () => showMultiplayerSelect(),
822	      // 素材包管理(自制:重制热补丁;面板动态 import 分块,HousingPanel 同模式)
823	      onAssetPacks: () => {
824	        const m = (window as unknown as { __swRemaster?: { manager: import('./remaster/RemasterManager').RemasterManager } }).__swRemaster?.manager;
825	        if (!m) { ui.toast(Lang.text('Mods.SandboxWorld.Remaster.NotReady')); return; }
826	        void import('./ui/RemasterPanel').then(({ openRemasterPanel }) => {
827	          openRemasterPanel(root, m, { onToast: (msg) => ui.toast(msg) });
828	        });
829	      },
830	      // GOING_OLDSCHOOL B2：日月拖拽 → 菜单时钟跟手（Main.cs:62434-62446 反算 t01）
831	      onSunMoonGrab: (info) => menuBg?.setClockT(info.time01),
832	    });
833	    installLegacyShim();
834	  }
835	
836	  /** 旧 puppeteer 脚本兼容垫片：select(尺寸)+button(创建) 隐藏 DOM（M7 移除）。
837	   *  挂 root 末尾（在天空画布之上）；标题页按钮在屏幕中央不与垫片（左上角）重叠，
838	   *  querySelector('button') 仍命中垫片——旧探针脚本零修改。 */
839	  function installLegacyShim() {
840	    if (legacyShim) return;
841	    const div = document.createElement('div');
842	    div.style.cssText = 'position:absolute;left:0;top:0;width:2px;height:2px;opacity:0.01;z-index:1;';
843	    const sel = document.createElement('select');
844	    sel.innerHTML = '<option value="4200x1200">小</option><option value="6400x1800" selected>中</option><option value="8400x2400">大</option>';
845	    const btn = document.createElement('button');
846	    btn.textContent = '创建新世界';
847	    btn.addEventListener('click', () => {
848	      const [w, h] = (sel.value || '6400x1800').split('x').map(Number);
849	      void newWorld('', w, h);

```


---

## 🤖 Assistant · 2026-08-19T08:56:09.774Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at gateAssetsOrRun (single-player gate) and the AssetDownloadUI, plus the menu preload (loadAssets in main.ts and menu preload of UI textures). Also check main.ts menu preload (preloadUiPrefix call sites).
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:56:11.917Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"gateAssetsOrRun\\|mountAssetBadge\\|assetsCompleteFast\\|assetsComplete()\" ~/Project/GLM/SandboxWorld/game/src/mainFlow.ts ~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts | head -20; echo ---; grep -n \"preloadUiPrefix\\|loadAssets\\|atlas.load\" ~/Project/GLM/SandboxWorld/game/src/main.ts ~/Project/GLM/SandboxWorld/game/src/mainFlow.ts | head -20",
 "description": "Find asset gate and menu preload call sites"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:12.003Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:19:import { gateAssetsOrRun, mountAssetBadge } from './ui/AssetDownloadUI';
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:810:    mountAssetBadge();
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:817:      onSinglePlayer: () => gateAssetsOrRun(() => showCharacterSelect()),
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:8:import { assetCacheState, assetsComplete, assetsCompleteFast, onAssetProgress, warmAllAssets, PHASE_LABEL, type AssetCacheState } from '../net/AssetCache';
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:156:export function mountAssetBadge(): void {
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:163:        if (st.enabled && !badgeEl) { badgePending = false; off(); mountAssetBadge(); }
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:189:      setTimeout(() => { unmountAssetBadge(); }, 700);
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:196:export function unmountAssetBadge(): void {
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:208:export function gateAssetsOrRun(action: () => void): void {
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:211:  if (assetsCompleteFast()) { action(); return; }
~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:247:    if (assetsComplete()) { close(); action(); }
---
~/Project/GLM/SandboxWorld/game/src/main.ts:124:async function loadAssets() {
~/Project/GLM/SandboxWorld/game/src/main.ts:127:    await atlas.load();
~/Project/GLM/SandboxWorld/game/src/main.ts:134:    await atlas.preloadUiPrefix(
~/Project/GLM/SandboxWorld/game/src/main.ts:489:  await loadAssets();
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts:177:    atlas?.preloadUiPrefix(['MapBG', 'Map.png']).catch(() => {});

```


---

## 🤖 Assistant · 2026-08-19T08:56:14.756Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/main.ts",
 "limit": 50,
 "offset": 118
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:14.775Z

**📎 ToolResult**

```
118	let atlas: SpriteAtlas | null = null;
119	
120	let flow: FlowHandle;
121	let inGame = false;
122	let pausePanel: HTMLElement | null = null;
123	
124	async function loadAssets() {
125	  atlas = new SpriteAtlas();
126	  try {
127	    await atlas.load();
128	    // 菜单首帧所需的 UI 贴图(面板/按钮/光标/logo)在显示主菜单前就位——
129	    // 否则 vui 懒加载下首帧控件用兜底样式闪一帧。
130	    // ★UI_ 全量族按子族排除(2026-08-13):素材全量入库后 UI_ 76→397 键,
131	    //   面板专属子族(图鉴/小地图/世界创建/角色创建/创意/工坊/成就…)只在各自
132	    //   面板打开时才需要,vui 消费方每帧重查 ensureUiImage 缺图自愈——
133	    //   收窄到菜单/加载页 chrome,请求 426→~170,零闪烁风险
134	    await atlas.preloadUiPrefix(
135	      ['UI_', 'Inventory_', 'logo', 'Logo'], undefined,
136	      ['UI_Bestiary', 'UI_Minimap', 'UI_WorldCreation', 'UI_CharCreation',
137	       'UI_PlayerResourceSets', 'UI_Workshop', 'UI_Creative', 'UI_Wires',
138	       'UI_DisplaySlots', 'UI_Achievement', 'UI_Craft', 'UI_InfoIcon',
139	       'UI_Settings', 'UI_Camera'],
140	    );
141	  } catch {
142	    atlas = null; // 素材缺失时回退程序化生成
143	  }
144	  (window as unknown as { __swAtlas?: SpriteAtlas | null }).__swAtlas = atlas; // 调试/探针句柄
145	  // 素材重制热补丁(2026-08-19):已装 pack 在菜单显示前应用——此刻无 chunk 烘焙、
146	  // 无懒加载竞争,vimages.set 直接覆盖,后继 ensureVImage 的 has 检查命中早退。
147	  // 失败静默(坏包不阻断启动;面板导入路径有显式报错)
148	  if (atlas) {
149	    remasterRuntime = new RemasterRuntime(atlas);
150	    remasterManager = new RemasterManager(remasterRuntime, () => assetVersion());
151	    const rt = remasterRuntime;
152	    remasterRuntime.onApplied = (info) => {
153	      // UI 派生缓存:物品图标 dataURL 缓存按物品 id 键不自动失效(Atlas 替换须清);
154	      // buff 栏直链 <img src> 经钩子取 runtime 的 objectURL 覆盖
155	      if (info.hasItemAtlas) clearIconCache();
156	      setRemasterBuffIcon((id) => rt.buffIconUrl(id));
157	    };
158	    try {
159	      // ★超时保护:IDB v2 升级遇旧标签页持有 v1 连接不让路时 openDb 永久 pending
160	      // (onversionchange 只对同代码版本生效;生产首次部署旧页在跑旧 bundle)——
161	      // 素材包是增强不是必需,8s 不到就放弃,绝不阻断启动
162	      await Promise.race([
163	        remasterManager.applyInstalled(),
164	        new Promise<void>((resolve) => setTimeout(resolve, 8000)),
165	      ]);
166	    } catch (err) {
167	      console.warn('[remaster] 启动应用素材包失败(已跳过):', err);

```


---

## 🤖 Assistant · 2026-08-19T08:56:15.396Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts",
 "limit": 70,
 "offset": 200
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:15.410Z

**📎 ToolResult**

```
200	}
201	
202	// ---- 单人游戏门槛弹窗 ----
203	
204	let gateEl: HTMLElement | null = null;
205	let gateUnsub: (() => void) | null = null;
206	
207	/** 资产未就绪时弹窗等待(实时进度);就绪/完成后执行 action。已就绪直接 action。 */
208	export function gateAssetsOrRun(action: () => void): void {
209	  // ★快速路径:上轮完成记录在(门槛真正等的是 SW status 回包的 1-2s keys()
210	  // 枚举,期间误显示下载中;trace 实证该窗口零实际下载)
211	  if (assetsCompleteFast()) { action(); return; }
212	  const s = assetCacheState();
213	  if (!s.enabled) { action(); return; } // SW 未启用(降级环境)不拦
214	  if (gateEl) return; // 已在等待
215	  ensureStyle();
216	  gateEl = document.createElement('div');
217	  gateEl.className = 'sw-asset-gate';
218	  gateEl.innerHTML = `
219	    <div class="panel">
220	      <div class="sw-asset-title">正在下载游戏资源</div>
221	      <div class="sw-asset-barwrap">
222	        <div class="outer"></div>
223	        <div class="slot"><div style="width:0%"></div></div>
224	      </div>
225	      <div class="sw-asset-pct"></div>
226	      <div class="sw-asset-note">下载完成后将自动进入(已下载部分不会重复下载)</div>
227	      <button class="sw-asset-retry" style="display:none">重新下载</button>
228	    </div>`;
229	  document.body.appendChild(gateEl);
230	  ensurePanelBg(gateEl.querySelector('.panel') as HTMLElement);
231	  const bar = gateEl.querySelector('.slot > div') as HTMLElement;
232	  const pct = gateEl.querySelector('.sw-asset-pct') as HTMLElement;
233	  const retry = gateEl.querySelector('.sw-asset-retry') as HTMLElement;
234	  retry.addEventListener('click', () => {
235	    retry.style.display = 'none';
236	    warmAllAssets(true);  // force:绕过已完成早退守卫,重拉失败项(2026-08-13 review:不绕过则按钮是死的)
237	  });
238	  const close = () => {
239	    gateUnsub?.(); gateUnsub = null;
240	    gateEl?.remove(); gateEl = null;
241	  };
242	  gateUnsub = onAssetProgress((st) => {
243	    if (!gateEl) return;
244	    bar.style.width = st.total > 0 ? `${Math.floor((st.done / st.total) * 100)}%` : '0%';
245	    pct.textContent = `${fmtPct(st)} · ${phaseText(st)}(${st.done}/${st.total})`;
246	    retry.style.display = st.failed > 0 && !st.warming ? '' : 'none';
247	    if (assetsComplete()) { close(); action(); }
248	  });
249	  pct.textContent = `${fmtPct(s)} · ${phaseText(s)}(${s.done}/${s.total})`;
250	  if (s.failed > 0 && !s.warming) retry.style.display = '';
251	}
252	

```


---

## 🤖 Assistant · 2026-08-19T08:56:29.076Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Very good. Now I have almost everything. A few remaining details:

1. Count atlas.json / resources.json / vanilla.json sizes (bundled via import). Also the count of files in atlas.json (Unity atlas) — the `data.files` keys count. The startup `load()` loads all files in atlas.json (Unity namespace). Let me check how many files that is — those are the sprites in 封面/地形/角色/portraits dirs. 封面 excluded by regex.

2. The vanilla.json keys count (tiles/items/walls/npcs) for the warm list sizes. Let me compute worldWarmUrls approximate size — the plan total. Let me check quickly via grep counting on the JSON... that's harder. I can count: plan = menu(~170 UI files + 1 font + 2 l10n) + world (tiles sheets + walls + npcs + items icons + VANILLA_MISC) + misc (7377+1779) + sounds (852) + music (~103). Let me compute the number of unique tile/wall/npc sheets from vanilla.json. I can use grep -o on the JSON for `"sheet":"vanilla/[^"]*"` unique count. But the classifier for python was down; grep -o + sort -u should be fine.

Let me also verify the dist directory has sw.js copied (build includes public). And check vite.config.ts for anything relevant (vanillaAtlasAuto plugin).

Also confirm Music ids count: audios/music has 104 files; MUSIC table values unique count. Fine to approximate.

Let me run the remaining greps.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:56:30.911Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -o '\"sheet\":\"[^\"]*\"' ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla.json | sort -u | wc -l; grep -o '\"icon\":\"[^\"]*\"' ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla.json | sort -u | wc -l; ls -la ~/Project/GLM/SandboxWorld/game/public/sprites/*.json | awk '{print $5, $9}'",
 "description": "Count unique sheets and icons in vanilla.json"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:31.088Z

**📎 ToolResult**

```
    1139
       2
655 ~/Project/GLM/SandboxWorld/game/public/sprites/annotations.json
190860 ~/Project/GLM/SandboxWorld/game/public/sprites/atlas.json
408261 ~/Project/GLM/SandboxWorld/game/public/sprites/remaster-index.json
35819 ~/Project/GLM/SandboxWorld/game/public/sprites/resources.json
2334 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcgore.json
145845 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json
84498 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui.json
1350148 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla.json

```


---

## 🤖 Assistant · 2026-08-19T08:56:33.522Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"vanillaAtlasAuto\\|vanilla-atlas\" ~/Project/GLM/SandboxWorld/game/vite.config.ts | head -5; grep -rn \"OPFS\\|showDirectoryPicker\\|navigator.storage\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -5; du -sh ~/Project/GLM/SandboxWorld/game/public/sounds ~/Project/GLM/SandboxWorld/game/public/audios/music 2>/dev/null",
 "description": "Check vite atlas auto-rebuild, OPFS usage, music size"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:33.699Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/vite.config.ts:69: *  晚于产物(vanilla.json / Item_Atlas_0.png)的最旧 mtime → 同步重跑 vanilla-atlas.mjs。
~/Project/GLM/SandboxWorld/game/vite.config.ts:71:function vanillaAtlasAuto(): Plugin {
~/Project/GLM/SandboxWorld/game/vite.config.ts:76:    join(ROOT, 'scripts', 'vanilla-atlas.mjs'),
~/Project/GLM/SandboxWorld/game/vite.config.ts:93:    console.log('[vanilla-atlas] 素材源有更新,自动重打包…');
~/Project/GLM/SandboxWorld/game/vite.config.ts:94:    execFileSync('node', [join(ROOT, 'scripts', 'vanilla-atlas.mjs')], { stdio: 'inherit' });
178M	~/Project/GLM/SandboxWorld/game/public/sounds
157M	~/Project/GLM/SandboxWorld/game/public/audios/music

```


---

## 🤖 Assistant · 2026-08-19T08:56:41.784Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting — "sheet" unique count = 1139, "icon" unique = 2 (because item icons are shelf-packed into ~2-3 Item_Atlas_k.png files). Let me verify icons list. And count NPC sheets. Actually the 1139 includes tile+walls+npcs sheets. Good enough.

Wait — icon count 2 means items icons resolve to 2 unique files (Item_Atlas_0/1). Let me confirm quickly. Also check dist to see the built size. Also let me confirm the total warm plan size = 170ish + 1139 + 2 + misc(7377+1779=9156) + 852 + ~103 music ≈ ~11400 files. That matches the "~3 min full warm" and "11k" mention in AssetCache comment ("单发全量 11k 无法跑完").

Let me check dist size, and grep the icons.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:56:44.005Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -o '\"icon\":\"[^\"]*\"' ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla.json | sort -u; ls ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_Atlas_*.png 2>/dev/null | head; du -sh ~/Project/GLM/SandboxWorld/game/dist 2>/dev/null; find ~/Project/GLM/SandboxWorld/game/dist -maxdepth 1 2>/dev/null | head",
 "description": "Check item atlas files and dist build output"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:44.172Z

**📎 ToolResult**

```
"icon":"vanilla/Item_Atlas_0.png"
"icon":"vanilla/Item_Atlas_1.png"
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_Atlas_0.png
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla/Item_Atlas_1.png
565M	~/Project/GLM/SandboxWorld/game/dist
~/Project/GLM/SandboxWorld/game/dist
~/Project/GLM/SandboxWorld/game/dist/hitbox-lab.html
~/Project/GLM/SandboxWorld/game/dist/l10n
~/Project/GLM/SandboxWorld/game/dist/debug-save.sbw.json
~/Project/GLM/SandboxWorld/game/dist/annotator.html
~/Project/GLM/SandboxWorld/game/dist/audios
~/Project/GLM/SandboxWorld/game/dist/index.html
~/Project/GLM/SandboxWorld/game/dist/hitbox-names.json
~/Project/GLM/SandboxWorld/game/dist/water-audit.html
~/Project/GLM/SandboxWorld/game/dist/tree-inspect.html

```


---

## 🤖 Assistant · 2026-08-19T08:56:51.559Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have everything. Let me also quickly verify:
- The "sw-asset-preload" plan doc: plans/gleaming-singing-biscuit.md mentioned in AssetCache.ts header. Check if it exists (at repo root plans/? or ~/.claude/plans?). The comment says "plans/gleaming-singing-biscuit.md". Let me check.
- Largest files in each dir for "前几大头".

Also, note the system reminder about plan mode: I'm a read-only search agent; I should NOT create a plan file — my task is to report findings. The plan-mode reminder says I can create a plan file, but my role is read-only exploration and reporting. The instruction from parent says "只读不改" and my final output is a report. I will not write any files.

Let me do the last checks.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:56:55.030Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game -maxdepth 3 -name \"*gleaming-singing-biscuit*\" -o -maxdepth 3 -name \"*sw-asset*\" 2>/dev/null | grep -v node_modules | head; echo ---; find ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui -type f -exec du -k {} + | sort -rn | head -6; echo ---; find ~/Project/GLM/SandboxWorld/game/public/sounds -type f -exec du -k {} + | sort -rn | head -4; find ~/Project/GLM/SandboxWorld/game/public/audios/music -type f -exec du -k {} + | sort -rn | head -4",
 "description": "Locate warm plan doc and largest asset files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:55.226Z

**📎 ToolResult ⚠️ERROR**

```
glm-x-preview-260804[1m] is temporarily unavailable, so auto mode cannot determine the safety of Bash right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.

```


---

## 🤖 Assistant · 2026-08-19T08:56:58.777Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game -maxdepth 3 -name \"*sw-asset*\" -not -path \"*/node_modules/*\" 2>/dev/null | head",
 "description": "Search for sw-asset preload plan document"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:56:58.853Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-19T08:57:02.102Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla -type f -exec du -k {} + | sort -rn | head -5",
 "description": "List largest files in vanilla sprites"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:02.355Z

**📎 ToolResult ⚠️ERROR**

```
glm-x-preview-260804[1m] is temporarily unavailable, so auto mode cannot determine the safety of Bash right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.

```


---

## 🤖 Assistant · 2026-08-19T08:57:02.853Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/public/sounds -type f -exec du -k {} + | sort -rn | head -4",
 "description": "List largest sound files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:03.032Z

**📎 ToolResult ⚠️ERROR**

```
glm-x-preview-260804[1m] is temporarily unavailable, so auto mode cannot determine the safety of Bash right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.

```


---

## 🤖 Assistant · 2026-08-19T08:57:09.268Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The classifier keeps being intermittently unavailable for `find -exec du`. Let me wait a moment and try with a simpler form, or just use `du -k` on the dirs and `ls -lS`. `ls -lS` is read-only and simple.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:57:09.781Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -lSk ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla | head -6",
 "description": "List largest vanilla sprite files by size"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:09.978Z

**📎 ToolResult**

```
total 95156
-rw-r--r--@ 1 user  staff  1839675  8月 13 19:27 Item_Atlas_0.png
-rw-r--r--@ 1 user  staff   816463  8月 13 19:27 Item_Atlas_1.png
-rw-r--r--@ 1 user  staff   785338  8月 13 14:55 Flare2.png
-rw-r--r--@ 1 user  staff   785338  8月 13 14:54 Misc_Sunflare_Lens_Flare2.png
-rw-r--r--@ 1 user  staff   785338  8月 13 14:49 Sunflare_Lens_Flare2.png

```


---

## 🤖 Assistant · 2026-08-19T08:57:13.766Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -lSk ~/Project/GLM/SandboxWorld/game/public/sounds | head -5; ls -lSk ~/Project/GLM/SandboxWorld/game/public/audios/music | head -4; ls -lSk ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-ui | head -4",
 "description": "List largest files in sounds, music, vanilla-ui"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:13.920Z

**📎 ToolResult**

```
total 181816
-rw-r--r--@ 1 user  staff  11364804  8月 13 14:49 blizzard_inside_building_loop.wav
-rw-r--r--@ 1 user  staff   6838640  8月 13 14:49 blizzard_strong_loop.wav
-rw-r--r--@ 1 user  staff   4370696  8月 13 14:49 Liquid_1.wav
-rw-r--r--@ 1 user  staff   4132528  8月 13 14:49 Liquid_0.wav
total 160564
-rw-r--r--@ 1 user  staff  3398470  8月 10 11:11 Music_49.mp3
-rw-r--r--@ 1 user  staff  2857213  8月 10 11:12 Music_100.mp3
-rw-r--r--@ 1 user  staff  2766515  8月 10 11:12 Music_101.mp3
total 8256
-rw-r--r--@ 1 user  staff  284307  8月 13 14:54 UI_Achievements.png
-rw-r--r--@ 1 user  staff   65353  8月 13 19:27 logo_8.png
-rw-r--r--@ 1 user  staff   61344  8月 13 19:27 logo_2.png

```


---

## 🤖 Assistant · 2026-08-19T08:57:24.982Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have all data. Let me compile a couple of remaining details for completeness:

1. atlas.json (Unity namespace) file count — the `load()` loads all files from `data.files`. Those are the 封面/地形/角色/portraits directories. 封面 (Splash_) excluded. Total files in sprites excluding vanilla + vanilla-ui: 11030 - 9195 - 1779 = 56 (+ json files). Actually the json files are also in the count. Let me quickly count png in the four non-vanilla dirs. But roughly: 地形(112K) + portraits(112K) + 角色(44K) ≈ 268K ≈ tiny. The atlas.json data.files — let me count keys quickly. `grep -o '"guid"'` counts files entries. Simpler: count "sprites":[ occurrences.

Actually this is minor; the load() at startup loads the Unity atlas files which are small (few dozen files). Let me do one quick count and then also check that Sfx.ts line ~287 fetch and 418 (preloadFiles). Also confirm where music list / MUSIC count. And mainFlow.ts:177 MapBG preload.

Let me quickly grep the atlas.json files count.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:57:27.813Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -o '\"guid\":' ~/Project/GLM/SandboxWorld/game/public/sprites/atlas.json | wc -l; find ~/Project/GLM/SandboxWorld/game/public/sprites/封面 ~/Project/GLM/SandboxWorld/game/public/sprites/地形 ~/Project/GLM/SandboxWorld/game/public/sprites/portraits ~/Project/GLM/SandboxWorld/game/public/sprites/角色 -type f | wc -l; grep -c \"id\" ~/Project/GLM/SandboxWorld/game/src/data/Music.ts",
 "description": "Count Unity atlas files and MUSIC table entries"
}
```


---

## 👤 User(sidechain) · 2026-08-19T08:57:27.909Z

**📎 ToolResult**

```
      20
      48
9

```


---

## 🤖 Assistant · 2026-08-19T08:57:41.958Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All data gathered. Now let me write the final report. I'm in "plan mode" per the system reminder, but I'm a read-only search subagent — my job is to return findings as my final message. I won't create a plan file since the parent task is a read-only investigation report (and my role instructions say to return findings directly).

Let me compile the report with file paths + line anchors, key code summaries, and volume numbers.

Key numbers:
- public/sprites: 104MB total (95156K vanilla + 8256K vanilla-ui + 780K 封面 + 116K 地形 + 112K portraits + 44K 角色 ≈ 104MB), 11030 files total; vanilla 9195 files / 93MB; vanilla-ui 1779 files / 8.1MB.
- public/sounds: 852 wav / 178MB. Top: blizzard_inside_building_loop.wav 11.4MB, blizzard_strong_loop.wav 6.8MB, Liquid_1.wav 4.4MB, Liquid_0.wav 4.1MB.
- public/audios: 160MB total, music/ 104 mp3 / 157MB, plus main.mp3 + title.mp3. Top: Music_49 3.4MB.
- l10n: 12MB (13 json incl index).
- fonts: 1 woff2 (fusion-pixel 12px zh_hans).
- dist: 565MB.

Warm plan total ≈ menu (~170 UI + 1 font + 2 l10n) + game-sprites (1139 unique sheets + 2 Item_Atlas + VANILLA_MISC ~115) + misc-sprites (7377 miscVanilla + 1779 miscUi) + sounds (852) + music (103) ≈ ~11.3k files. Matches AssetCache comment "单发全量 11k".

Report structure:
1. 资源取用路径
2. Service Worker
3. 已有本地持久层
4. 首屏加载流程

With paths and line anchors.
```

</details>


---

## 🤖 Assistant · 2026-08-19T08:58:54.271Z · glm-x-preview-260804

```
调查完成。以下为四点结论（均为只读探查,未改动任何文件）。

# 1. 资源取用路径

## 贴图 — `~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts` (1107 行)

**最终 URL 形态**: 全部相对路径 `sprites/<encodeURI(file)>`,即 `sprites/vanilla/Tiles_10.png`、`sprites/vanilla-ui/Player_0_0.png` 这类。无 XHR,统一 `new Image()` + `img.src` 赋值(或 fetch 用于 json)。五个发起点:

| 入口 | 行号 | 作用 |
|---|---|---|
| `SpriteAtlas.load()` | :176-219 | 启动预载 Unity 图集(`atlas.json` 的 `data.files`,仅 20 个文件;`:179` 过滤掉 `封面/Splash_`;`:211` `img.src = sprites/${encodeURI(f)}`;`:216` fetch `sprites/annotations.json`) |
| `ensureVImage(file)` | :442-478 | **渲染路径统一懒加载入口**:miss 发 `new Image()`,pending 去重(`_iconPending`)、404 负缓存(`_vImageFailed` :481)、onload 后 `tryBitmapUpgrade` 升 ImageBitmap;`onVImageLoaded` 回调(:370)触发 ChunkCache 重烘焙 |
| `ensureUiImage(file)` | :331-350 | vanilla-ui 命名空间懒加载,`_uiPending`/`_uiFailed` 同构 |
| `preloadFiles(files)` | :373-396 | 预载清单底层(vframe/vframeAt/vrect/vnpc/vmisc/vicon 全部经 ensureVImage 间接消费) |
| `loadBitmapOnly()` (模块级导出) | :1092-1105 | 通用 bitmap-only 加载器(雨/尘粒子等),`_bmpOnlyPending` 防每帧重发 |

**常驻清单/入口表**:
- `VANILLA_MISC` :56-74 — 进图必预载的 88 张杂项单图(树冠 32 + 树枝 32 + 门对 + 液体/瀑布基表),2026-08-13 从 304 张瘦身而来。
- 元数据表经 Vite `import` 打进 bundle(:5-9): `atlas.json`(190KB)、`resources.json`(36KB)、`vanilla.json`(1.35MB)、`vanilla-npcs.json`(146KB)、`vanilla-ui.json`(84KB) — **不产生运行时请求**。
- `vicon` :355-364 — 物品图标走 `Item_Atlas_0/1.png` 两张 shelf-pack 大图(ix/iy/iw/ih 子矩形),不再是 6059 张单体。
- `preloadIcons()` :498-510 — 缓存 Promise,实际只载 2 张 Item_Atlas。
- `preloadUiPrefix()` :515-521 / `preloadUiFiles()` :524-548 — UI 前缀批量预载。

## 音效 — `~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts`

- 按需懒加载:播放未命中才 `fetch(\`sounds/${file}.wav\`)`(:287 普通音效、:418 `preloadFiles` 定向预热);pending 防重入 + failed 负缓存;首播走 WebAudio 合成兜底。WAV_MAP(:78 起)逻辑名→`public/sounds/*.wav` 平铺文件名(Sounds/Custom 已拍平进根目录)。
- 无 xwb 运行时读取;xwb 是提取前形态(`tools/xwb-extract.mjs`)。

## BGM — `~/Project/GLM/SandboxWorld/game/src/core/Audio.ts`

- :53 `fetch(\`audios/music/Music_${id}.mp3\`)` → `decodeAudioData`,AudioBuffer 内存缓存 LRU 上限 3 首(:21),失败负缓存 `null`。曲目 id 来自 `src/data/Music.ts` 的 MUSIC 表。

## 体量

| 目录 | 文件数 | 磁盘 |
|---|---|---|
| `public/sprites`(总) | **11030** | 104MB |
| ├ `sprites/vanilla/` | 9195 | 93MB |
| ├ `sprites/vanilla-ui/` | 1779 | 8.1MB |
| └ 封面+地形+portraits+角色 | 48 | ~0.3MB |
| `public/sounds` | 852 wav | **178MB** |
| `public/audios`(music 104 曲 + main/title.mp3) | 106 | 160MB(music 157MB) |
| `public/l10n` | 13 json | 12MB |
| `public/fonts` | 1 woff2 | ~0.9MB |
| `dist/`(构建产物) | — | 565MB |

单文件大头: `sounds/blizzard_inside_building_loop.wav` 11.4MB、`blizzard_strong_loop.wav` 6.8MB、`Liquid_1/0.wav` 4.4/4.1MB; `sprites/vanilla/Item_Atlas_0.png` 1.8MB、`Item_Atlas_1.png` 0.8MB; music 最大 `Music_49.mp3` 3.4MB。

# 2. Service Worker

**文件**: `~/Project/GLM/SandboxWorld/game/public/sw.js` (220 行,手写,非生成)。

**注册点**: `~/Project/GLM/SandboxWorld/game/src/net/AssetCache.ts` `initAssetCache()` :198-227 — `navigator.serviceWorker.register('sw.js', { updateViaCache: 'none' })`(:209)。仅生产构建(dev 需 `?sw=1`,`?nosw` 强制关,:203);非 secureContext 降级跳过(:204)。调用处 `src/main.ts:500`(`void initAssetCache()`,启动即注册)。

**缓存名/版本**: `sw-assets-v{version}`(sw.js:14);version 由页面算 `fnv1a32(JSON(vanilla.json)+JSON(vanilla-ui.json)+CACHE_BUSTER)`(AssetCache.ts:42-48,`CACHE_BUSTER = 1` :19)→ 随每条 postMessage 下发(sw.js:197-204,SW 被 ~3min 击杀重启后无状态恢复)。activate 清非当前版本(sw.js:27-35)。

**fetch 拦截**(sw.js:37-97):
- `/sprites|fonts|l10n|sounds|audios/` 的 GET → **Cache API(cache-first,未命中网络回填)**;非 http(s) scheme 放行(:43)。
- 例外1 `/l10n/` :69-83 网络优先+离线回退(可变配置,2026-08-16 裸键事故修)。
- 例外2 应用壳 `/assets/*.js|css|woff2` + document :48-64 网络优先+离线回退。

**分块接力 warm**(约 3 分钟全量预热):
- SW 侧 `warm()` sw.js:99-178: 先 `cache.keys()` 建已缓存集只 fetch 缺失(断点续传/自愈);AIMD 自适应并发 2-8 路(:116-124);每 400 文件停 250ms 喘息;单文件 3 次重试(300/600ms);进度 `postMessage` 回页。
- **页面侧驱动器** `~/Project/GLM/SandboxWorld/game/src/net/AssetCache.ts`: `sendChunk()` :272-295 按 `CHUNK = 500`(:267)一批发 `{type:'warm', urls, base}`;块完成(warm-done 消息 :253-258)自动接力下一块;看门狗 `startWatchdog()` :297-304 每 5s 检查,停滞 >15s 补发当前块——应对"SW 被浏览器 ~3min 击杀"(注释 :263-266)。全量跑完仍有失败自动补拉 3 轮(:277-283)。
- 启动点: `src/mainFlow.ts:809` `warmAllAssets()`(showTitle 进主菜单即调,幂等)。

**warm 什么由 `priorityPlan()` 决定**(AssetCache.ts:103-124),五个相位:
- P0 `menuWarmUrls` :53-67 — vanilla-ui 前缀 `UI_/Inventory_/logo/Logo` 减 14 个面板子族 + fonts + `l10n/{index,zh-Hans}.json`(≈170 文件)
- P1 `worldWarmUrls` :70-78 — vanilla.json 全部 tile/wall/npc sheet(实测唯一 1139 张)+ 全部 item icon(=2 张 Item_Atlas)+ VANILLA_MISC
- P2 `miscWarmUrls` :81-83 — **assets-index.json** 的 miscVanilla(7377)+ miscUi(1779)
- P3 `soundsWarmUrls` :86-88 — assets-index 的 sounds(852)
- P4 `musicWarmUrls` :89-93 — MUSIC 表枚举 `audios/music/Music_<id>.mp3`(103 曲)

合计 **≈11.3k 文件 / ~440MB**(注释 :263 "单发全量 11k 无法跑完" 佐证)。

# 3. 已有本地持久层

| 技术 | 用途 | 位置 |
|---|---|---|
| **Cache API** | 全量游戏资产(第 2 点,唯一存"资源"的层) | public/sw.js |
| **IndexedDB** | 只存存档/配置/素材包 blob,**不存游戏资源** | `src/save/KvStore.ts`(:1-13,IDB v2;≤2MB 走 localStorage :92)、`src/remaster/PackStore.ts`(重制素材包 blob) |
| **OPFS** | **完全未使用**(全 src 无 `getDirectory`/`navigator.storage` 命中) | — |
| **localStorage** | 小配置 + SW 完成态标志 `swAssetsComplete:<version>`(AssetCache.ts:176-189,门槛秒开用) | — |

**assets-index.json 生成/消费**:
- 生成: `~/Project/GLM/SandboxWorld/game/scripts/vanilla-atlas.mjs` :469-496 — 扫盘枚举,结构 `{ generatedAt, sounds: [...852], fonts: [...1], l10n: [...13], miscVanilla: [...7377], miscUi: [...1779] }`(miscVanilla 过滤掉 `Item_Atlas_*`/`Tiles_\d+`/`Wall_\d+`/`NPC_\d+` 避免与 P1 重复)。由 `vite.config.ts:71` `vanillaAtlasAuto()` 插件在 dev 启动/build 时按 mtime stale 自动重跑(:69-94)。
- 消费: AssetCache.ts:14 静态 import(356KB 进 bundle),P2/P3 相位数据源。

# 4. 首屏加载流程

**主菜单前**(`src/main.ts`):
- `loadAssets()` :124-143 → `atlas.load()`(Unity 图集 20 文件,Splash 过滤)→ `preloadUiPrefix(['UI_','Inventory_','logo','Logo'], 排除14子族)` :134-140 — 注释实锤请求 **426→~170 收窄**。
- :496-500 字体/语言包加载 → `initAssetCache()` 注册 SW。
- `flow.showTitle()`(mainFlow.ts:804-834): `warmAllAssets()` 后台全量预热 + `mountAssetBadge()` 右下角进度徽标。

**进世界门槛**: `TitleMenu.onSinglePlayer → gateAssetsOrRun(...)`(mainFlow.ts:817)。`gateAssetsOrRun` 在 `~/Project/GLM/SandboxWorld/game/src/ui/AssetDownloadUI.ts:208-251`: `assetsCompleteFast()`(localStorage 完成标志)秒过,否则弹"正在下载游戏资源"进度弹窗,`assetsComplete()`(done≥total 且 failed=0,AssetCache.ts:167-169)才放行;带"重新下载"按钮(`warmAllAssets(true)` 绕过早退守卫 :236)。

**进图前资源保证** — `Game.preloadSceneAssets()` `~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2473-2527`(newWorld :2442/:2460 与 loadWorld :2613 均在 `onWorldReady` 前 await):
- `collectSheetsAround(玩家点, R=240)` :2530-2550 精确扫描——只预载涉及的 tile/wall 表(实测 **22/378 张**,:2469 注释),加草/泥/石兜底;
- `preloadMiscAndNpcs()`(VANILLA_MISC 88 张 + NPC 表);
- 物品图标 `preloadIcons()`(:2492)**不阻塞**——后台补齐后 `onInventoryChanged` 刷背包;
- 角色贴图收窄为当前外观 ~30 张 Player_ + 装备 3 张 Armor 表(:2497-2523);
- 群系背景 `biomeBg.preloadInitial` :2525。

**"每文件一次 HTTP"的实际规模**(无打包合并,一图一 wav 一 mp3 一请求):
- 冷启动到主菜单: ~20(Unity 图集)+ ~170(UI)+ 字体/语言 ≈ **200 请求**;
- 典型进图(预热未完成时): +22 张表 + 88 misc + ~30 Player/Armor + 少量图标 ≈ **+150**;
- SW 全量 warm: **~11.3k 请求 / ~440MB**(500/块 × ~23 块接力,单文件最大 11.4MB wav);
- 长会话懒加载: vicon/vui/弹幕/NPC 表按需,每文件独立请求(benchmark 注释提到典型会话懒载 133 条量级,DebugReport.ts 有 F5 assetHealth 审计)。

**关键观察**: 资源本身无任何合并打包(sprites/vanilla 9195 个 PNG 单文件),持久化完全依赖 SW + Cache API;IndexedDB 仅存档/素材包;OPFS 空白。
```
