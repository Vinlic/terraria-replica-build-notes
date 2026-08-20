# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-09T10:48:41.420Z

```
Explore the game engine at ~/Project/GLM/SandboxWorld/game/src (TypeScript, Terraria remake). Search breadth: very thorough. Goal: map every integration point needed to add a full wiring/circuit system (wire bits per tile, wire items/placement, signal propagation, wire rendering, persistence).

Report on:
1. **TileStore** (src/world/TileStore.ts): full field list & memory layout (typed arrays: type/flags/frameX/frameY/wall/liquid/slope/half etc.), idx() addressing, setTile/setTileSilent listeners, any spare/unused arrays, how slope/half stored. Report exact field names and how they're allocated.
2. **Save format**: src/save/SaveFile.ts (saveGame/loadSave) — how world tile data is serialized (per-tile arrays? versioning? checksums?), where a new per-tile wire byte array would slot in; also src/save/KvStore.ts basics. And src/world/World.ts fields (header info, trees/chests lists, any versioning field).
3. **WldParser** (src/wld/WldParser.ts): how tiles are parsed — the exact bit layout of the per-tile data block (flags 1-3, frameX/frameY etc.), specifically whether wire bits (red/blue/green/yellow + actuator in flags) are currently parsed or skipped, and where they'd be extracted. Note the exact flag constants used.
4. **Items & placement**: src/data/items.ts structure (ItemDef fields incl. tile, placeStyle, maxStack), src/core/Game.ts tryPlace/canPlace/overlapsEntity + mining breakTile flow, how consumable placement items deduct + useTime, and how interactAt dispatches right-click. Where wrench-like tools (place-on-existing-tile, no tile consumed into a tile slot) could hook in.
5. **Game loop**: Game.ts update() structure — tick order (player, entities, liquid, lighting, chunks dirty), where a Wiring.update per tick would go; existing mechanism bits (toggleSwitch/fireTrapsFrom/checkPressurePlates, trapCooldown/plateLatch fields) around lines 1420-1470; sfx system (Sfx.ts available sound names, is there 'tink'?); how projectiles/entities spawn (Dart class pattern, entities.add).
6. **Rendering**: src/render/ChunkCache.ts render passes (wall layer, tile layer, water), how a wire overlay pass could be added (draw order vs water/tile), ChunkCache CHUNK=16 grid; src/render/Renderer.ts main composite (where chunk canvases get drawn, any existing overlay toggles like mechanical ruler / F-keys); how UI toggles/keyboard shortcuts are registered in Input/Game (e.g. F5 annotate mode, F8 enemy spawn).
7. **Existing related systems**: Door.ts (openDoor/closeDoor signatures — door wiring would call these), LiquidSim (pump integration points), enemy spawn API (statue spawns), teleport (is there any /tp or spawnX/Y mechanics).
Report exact file:line references and code patterns to reuse. Output a structured report.
```

---

## 📎 Attachment · skill_listing · 2026-08-09T10:48:41.423Z

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

## 🤖 Assistant · 2026-08-09T10:48:42.946Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me explore the codebase thoroughly. Start by getting the directory structure and then reading key files in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:48:42.954Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src -type f -name \"*.ts\" | sort",
 "description": "List all TypeScript files in src"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:42.976Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/assets/AssetGen.ts
~/Project/GLM/SandboxWorld/game/src/assets/CharacterSheetGen.ts
~/Project/GLM/SandboxWorld/game/src/assets/ItemIconGen.ts
~/Project/GLM/SandboxWorld/game/src/assets/Palette.ts
~/Project/GLM/SandboxWorld/game/src/assets/SpriteAtlas.ts
~/Project/GLM/SandboxWorld/game/src/assets/TileSheetGen.ts
~/Project/GLM/SandboxWorld/game/src/core/Audio.ts
~/Project/GLM/SandboxWorld/game/src/core/constants.ts
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/core/HitTile.ts
~/Project/GLM/SandboxWorld/game/src/core/Input.ts
~/Project/GLM/SandboxWorld/game/src/core/rng.ts
~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts
~/Project/GLM/SandboxWorld/game/src/data/critters.ts
~/Project/GLM/SandboxWorld/game/src/data/enemies.ts
~/Project/GLM/SandboxWorld/game/src/data/items.ts
~/Project/GLM/SandboxWorld/game/src/data/recipes.ts
~/Project/GLM/SandboxWorld/game/src/data/tiles.ts
~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts
~/Project/GLM/SandboxWorld/game/src/entities/Arrow.ts
~/Project/GLM/SandboxWorld/game/src/entities/Critter.ts
~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts
~/Project/GLM/SandboxWorld/game/src/entities/MagicProj.ts
~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts
~/Project/GLM/SandboxWorld/game/src/entities/Tombstone.ts
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts
~/Project/GLM/SandboxWorld/game/src/entities/types.ts
~/Project/GLM/SandboxWorld/game/src/entities/waterAvoid.ts
~/Project/GLM/SandboxWorld/game/src/i18n/Lang.ts
~/Project/GLM/SandboxWorld/game/src/i18n/worldgenKeys.ts
~/Project/GLM/SandboxWorld/game/src/items/Inventory.ts
~/Project/GLM/SandboxWorld/game/src/lighting/LightingEngine.ts
~/Project/GLM/SandboxWorld/game/src/main.ts
~/Project/GLM/SandboxWorld/game/src/mainFlow.ts
~/Project/GLM/SandboxWorld/game/src/physics/TileCollision.ts
~/Project/GLM/SandboxWorld/game/src/player/Appearance.ts
~/Project/GLM/SandboxWorld/game/src/player/PaperDoll.ts
~/Project/GLM/SandboxWorld/game/src/render/AutoTiler.ts
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts
~/Project/GLM/SandboxWorld/game/src/render/Camera.ts
~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts
~/Project/GLM/SandboxWorld/game/src/render/MenuBackground.ts
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
~/Project/GLM/SandboxWorld/game/src/render/SkyRenderer.ts
~/Project/GLM/SandboxWorld/game/src/render/VanillaLiquidRenderer.ts
~/Project/GLM/SandboxWorld/game/src/render/VanillaTiler.ts
~/Project/GLM/SandboxWorld/game/src/render/VanillaWallTiler.ts
~/Project/GLM/SandboxWorld/game/src/render/WallTiler.ts
~/Project/GLM/SandboxWorld/game/src/render/WaterfallRenderer.ts
~/Project/GLM/SandboxWorld/game/src/save/CharacterStore.ts
~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts
~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts
~/Project/GLM/SandboxWorld/game/src/vui/assets/UITextures.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/CalculatedStyle.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/RootDimension.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/StyleDimension.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/UIElement.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/UIMouseEvent.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/UIState.ts
~/Project/GLM/SandboxWorld/game/src/vui/core/UserInterface.ts
~/Project/GLM/SandboxWorld/game/src/vui/draw/PixelText.ts
~/Project/GLM/SandboxWorld/game/src/vui/draw/UIFont.ts
~/Project/GLM/SandboxWorld/game/src/vui/draw/UIScale.ts
~/Project/GLM/SandboxWorld/game/src/vui/draw/UISpriteBatch.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UICharacterListItem.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UICharacterPreview.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIHeader.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIImage.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIList.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIPanel.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIScrollbar.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UIText.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UITextBox.ts
~/Project/GLM/SandboxWorld/game/src/vui/elements/UITextPanel.ts
~/Project/GLM/SandboxWorld/game/src/vui/states/DataState.ts
~/Project/GLM/SandboxWorld/game/src/vui/states/TitleState.ts
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterCreationState.ts
~/Project/GLM/SandboxWorld/game/src/vui/states/UICharacterSelectState.ts
~/Project/GLM/SandboxWorld/game/src/vui/states/VuiDemoState.ts
~/Project/GLM/SandboxWorld/game/src/vui/VUI.ts
~/Project/GLM/SandboxWorld/game/src/wld/BinaryReaderLE.ts
~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts
~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts
~/Project/GLM/SandboxWorld/game/src/world/Door.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts
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
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MushroomPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/Spread.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SwordShrinePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TemplePass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TerrainPass.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts
~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts
~/Project/GLM/SandboxWorld/game/src/world/World.ts

```


---

## 🤖 Assistant · 2026-08-09T10:48:43.738Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts ~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts ~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts ~/Project/GLM/SandboxWorld/game/src/world/World.ts ~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts ~/Project/GLM/SandboxWorld/game/src/core/Game.ts ~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts ~/Project/GLM/SandboxWorld/game/src/data/items.ts 2>/dev/null",
 "description": "Get line counts of key files"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:43.773Z

**📎 ToolResult**

```
     130 ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts
     212 ~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts
      86 ~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts
     104 ~/Project/GLM/SandboxWorld/game/src/world/World.ts
     349 ~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts
    2339 ~/Project/GLM/SandboxWorld/game/src/core/Game.ts
     297 ~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts
    1426 ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
     724 ~/Project/GLM/SandboxWorld/game/src/data/items.ts
    5667 total

```


---

## 🤖 Assistant · 2026-08-09T10:48:46.407Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:46.413Z

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
16	
17	  // tile 变更监听（chunk 缓存 / 光照脏标记 / 液体模拟统一从这里拿事件）
18	  private listeners: Array<(x: number, y: number) => void> = [];
19	
20	  constructor(w: number, h: number) {
21	    this.w = w; this.h = h;
22	    const n = w * h;
23	    this.type = new Uint16Array(n);
24	    this.flags = new Uint8Array(n);
25	    this.frameX = new Uint16Array(n);
26	    this.frameY = new Uint16Array(n);
27	    this.wall = new Uint16Array(n);
28	    this.liquid = new Uint8Array(n);
29	    this.liquidType = new Uint8Array(n);
30	    this.half = new Uint8Array(n);
31	    this.slope = new Uint8Array(n);
32	  }
33	
34	  idx(x: number, y: number): number { return y * this.w + x; }
35	
36	  inBounds(x: number, y: number): boolean {
37	    return x >= 0 && y >= 0 && x < this.w && y < this.h;
38	  }
39	
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
60	  }
61	
62	  /** 液体变化独立通道：chunk 缓存不订阅（水不入烘焙画布，无需重建），
63	   *  只有光照订阅（水的光衰减）——避免水流时每帧冲爆 chunk 重建队列造成卡顿 */
64	  private liquidListeners: Array<(x: number, y: number) => void> = [];
65	  onLiquidChanged(fn: (x: number, y: number) => void) {
66	    this.liquidListeners.push(fn);
67	  }
68	
69	  /** 唯一的写入入口（生成/导入期可绕过用 setTileSilent） */
70	  setTile(x: number, y: number, type: number, frameX = 0, frameY = 0) {
71	    if (!this.inBounds(x, y)) return;
72	    const i = this.idx(x, y);
73	    this.type[i] = type;
74	    this.flags[i] = type !== 0 ? 1 : 0;
75	    this.frameX[i] = frameX;
76	    this.frameY[i] = frameY;
77	    if (type === 0) { this.half[i] = 0; this.slope[i] = 0; } // 挖除清半砖/坡面
78	    this.listeners.forEach((fn) => fn(x, y));
79	  }
80	
81	  /** 运行期改半砖/坡面位（锤子交互用；生成期直接写数组即可） */
82	  setHalfBrick(x: number, y: number, v: boolean) {
83	    if (!this.inBounds(x, y)) return;
84	    const i = this.idx(x, y);
85	    this.half[i] = v ? 1 : 0;
86	    this.listeners.forEach((fn) => fn(x, y));
87	  }
88	
89	  setSlope(x: number, y: number, s: number) {
90	    if (!this.inBounds(x, y)) return;
91	    const i = this.idx(x, y);
92	    this.slope[i] = s;
93	    this.half[i] = 0; // 原版 SlopeTile 无条件 halfBrick(false)（WorldGen.cs:49174），slope=0 复位时同样
94	    this.listeners.forEach((fn) => fn(x, y));
95	  }
96	
97	  setTileSilent(x: number, y: number, type: number, frameX = 0, frameY = 0) {
98	    if (!this.inBounds(x, y)) return;
99	    const i = this.idx(x, y);
100	    this.type[i] = type;
101	    this.flags[i] = type !== 0 ? 1 : 0;
102	    this.frameX[i] = frameX;
103	    this.frameY[i] = frameY;
104	    if (type === 0) { this.half[i] = 0; this.slope[i] = 0; } // 挖除同步清位（防生成期脏残留）
105	  }
106	
107	  setWall(x: number, y: number, wall: number) {
108	    if (!this.inBounds(x, y)) return;
109	    const i = this.idx(x, y);
110	    if (this.wall[i] !== wall) {
111	      this.wall[i] = wall;
112	      this.listeners.forEach((fn) => fn(x, y));
113	    }
114	  }
115	
116	  setWallSilent(x: number, y: number, wall: number) {
117	    if (!this.inBounds(x, y)) return;
118	    this.wall[this.idx(x, y)] = wall;
119	  }
120	
121	  setLiquid(x: number, y: number, amount: number, type: number) {
122	    if (!this.inBounds(x, y)) return;
123	    const i = this.idx(x, y);
124	    const a = Math.max(0, Math.min(255, amount | 0));
125	    if (this.liquid[i] === a && this.liquidType[i] === type) return;
126	    this.liquid[i] = a;
127	    this.liquidType[i] = type;
128	    this.liquidListeners.forEach((fn) => fn(x, y));
129	  }
130	}
131	

```


---

## 🤖 Assistant · 2026-08-09T10:48:46.414Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T10:48:46.416Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T10:48:46.418Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/World.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:46.421Z

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
34	  clock: Clock;
35	  chests: ChestData[] = [];
36	  // Boss 进度旗标
37	  flags: Record<string, boolean> = { downedEyeOfCthulhu: false, shadowOrbSmashed: false };
38	  // 树登记：砍树干时找到整棵树（roots → 范围）
39	  trees: Array<{ x: number; y: number; h: number }> = [];
40	  /** 战争迷雾：1 = 已探索。按 tile 粒度。 */
41	  explored: Uint8Array;
42	  /** 原版树样式数据（header treeX/treeStyle）：横向 4 区森林树冠样式 */
43	  treeX: number[] = [];
44	  treeStyle: number[] = [0, 0, 0, 0];
45	  /** 世界级生物群系常量(原版 header,生成期 Reset pass 掷出) */
46	  crimson = false;          // true=猩红 false=腐化
47	  dungeonX = 0;            // 地牢位置
48	  jungleX = 0;             // 丛林位置
49	  /** TreeTops 13 区域变体（v≥211 wld 权威；索引 0-3 森林/5 丛林/6 雪/7 神圣） */
50	  treeTops: number[] = [];
51	
52	  exploredVersion = 0;
53	  markExplored(cx: number, cy: number, radius: number) {
54	    this.exploredVersion++;
55	    const st = this.store;
56	    const x0 = Math.max(0, cx - radius), x1 = Math.min(st.w - 1, cx + radius);
57	    const y0 = Math.max(0, cy - radius), y1 = Math.min(st.h - 1, cy + radius);
58	    for (let y = y0; y <= y1; y++) {
59	      for (let x = x0; x <= x1; x++) {
60	        if ((x - cx) ** 2 + (y - cy) ** 2 <= radius * radius) {
61	          this.explored[y * st.w + x] = 1;
62	        }
63	      }
64	    }
65	  }
66	
67	  constructor(w: number, h: number, seed: number, name = '新世界') {
68	    this.store = new TileStore(w, h);
69	    this.explored = new Uint8Array(w * h);
70	    this.seed = seed;
71	    this.name = name;
72	    // 1 游戏日 = 30 现实分钟（24→40 后折中）
73	    this.clock = new Clock(30 * 60 * 1000);
74	  }
75	
76	  get w() { return this.store.w; }
77	  get h() { return this.store.h; }
78	  get tiles() { return this.store; }
79	
80	  /** 破坏一个 tile（含 framed 物体的锚点处理由调用方负责），返回掉落 item key */
81	  breakTileAt(x: number, y: number): string | null {
82	    const t = this.store.get(x, y);
83	    if (t === 0) return null;
84	    const d = TILE_DEFS[t];
85	    this.store.setTile(x, y, 0);
86	    // v_ 图块无显式 drop → 回退同名放置物品(阶段5 自动注册)
87	    return d.drop ?? (d.key.startsWith('v_') ? 'place_' + d.key : null);
88	  }
89	
90	  isSolidPx(px: number, py: number): boolean {
91	    return this.store.isSolid(Math.floor(px / 16), Math.floor(py / 16));
92	  }
93	
94	  /** 液体量（0-255）按像素坐标 */
95	  liquidAt(px: number, py: number): number {
96	    return this.store.liquid[this.store.idx(Math.floor(px / 16), Math.floor(py / 16))];
97	  }
98	
99	  registerTree(x: number, y: number, h: number) {
100	    this.trees.push({ x, y, h });
101	  }
102	}
103	
104	export { T };
105	

```


---

## 👤 User(sidechain) · 2026-08-09T10:48:46.422Z

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

## 👤 User(sidechain) · 2026-08-09T10:48:46.423Z

**📎 ToolResult**

```
1	// 自有存档格式：JSON 外壳（人可读）+ RLE 二进制 tile 段（base64）
2	import type { World } from '../world/World';
3	import { World as WorldClass } from '../world/World';
4	import type { Player } from '../entities/Player';
5	
6	// ---- varint / base64 工具 ----
7	function writeVarint(out: number[], v: number) {
8	  v = v < 0 ? 0 : v;
9	  while (v >= 0x80) {
10	    out.push((v & 0x7f) | 0x80);
11	    v >>>= 7;
12	  }
13	  out.push(v);
14	}
15	
16	export function bytesToB64(bytes: number[]): string {
17	  const u8 = new Uint8Array(bytes);
18	  let s = '';
19	  for (let i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]);
20	  return btoa(s);
21	}
22	
23	function b64ToBytes(b64: string): Uint8Array {
24	  const s = atob(b64);
25	  const u8 = new Uint8Array(s.length);
26	  for (let i = 0; i < s.length; i++) u8[i] = s.charCodeAt(i);
27	  return u8;
28	}
29	
30	function readVarint(u8: Uint8Array, pos: { i: number }): number {
31	  let v = 0, shift = 0;
32	  while (pos.i < u8.length) {
33	    const b = u8[pos.i++];
34	    v |= (b & 0x7f) << shift;
35	    if (!(b & 0x80)) break;
36	    shift += 7;
37	  }
38	  return v;
39	}
40	
41	// ---- 正式 RLE 格式 ----
42	// tiles 每条目: varint(run-1) varint(type) [varint(frameX) varint(frameY) 仅当 type!=0]
43	// walls/liquid: varint(run-1) varint(value)
44	
45	export interface SaveData {
46	  format: 'sandboxworld.save';
47	  version: number;
48	  header: {
49	    name: string; seed: number; width: number; height: number;
50	    spawn: [number, number]; groundLevel: number; rockLevel: number;
51	    crimson?: boolean; dungeonX?: number; jungleX?: number;
52	    treeX?: number[]; treeStyle?: number[]; treeTops?: number[];
53	    created: number; playTimeMs: number;
54	    wldVersion?: number;
55	  };
56	  clock: { timeOfDay: number; dayCount: number };
57	  tiles: string;   // base64 RLE
58	  walls: string;
59	  liquid: string;
60	  liquidType: string;  // base64 RLE（0无 1水 2岩浆 3蜂蜜）
61	  chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null> }>;
62	  player: {
63	    hp: number; x: number; y: number;
64	    inventory: Array<{ id: number; stack: number } | null>;
65	    selected: number;
66	  };
67	  npcs: Array<{ key: string; x: number; y: number; home: [number, number] | null }>;
68	  flags: Record<string, boolean>;
69	}
70	
71	export function rlePairs(values: ArrayLike<number>): number[] {
72	  const out: number[] = [];
73	  const n = values.length;
74	  let i = 0;
75	  while (i < n) {
76	    const v = values[i];
77	    let run = 1;
78	    while (i + run < n && values[i + run] === v && run < 0x7fffffff) run++;
79	    writeVarint(out, run - 1);
80	    writeVarint(out, v);
81	    i += run;
82	  }
83	  return out;
84	}
85	
86	export function rleTiles(st: { type: Uint16Array; frameX: Uint16Array; frameY: Uint16Array }): number[] {
87	  const out: number[] = [];
88	  const n = st.type.length;
89	  let i = 0;
90	  while (i < n) {
91	    const t = st.type[i], fx = st.frameX[i], fy = st.frameY[i];
92	    let run = 1;
93	    while (i + run < n && st.type[i + run] === t && st.frameX[i + run] === fx && st.frameY[i + run] === fy) run++;
94	    writeVarint(out, run - 1);
95	    writeVarint(out, t);
96	    if (t !== 0) {
97	      writeVarint(out, fx);
98	      writeVarint(out, fy);
99	    }
100	    i += run;
101	  }
102	  return out;
103	}
104	
105	export function saveGame(world: World, player: Player, playTimeMs: number): string {
106	  const st = world.store;
107	  // 幽灵净化:存档格式不携带 active 位(加载时 type≠0 即激活),
108	  // 非活性格上的残留 type 必须归零,否则重读后全部变成浮空实体块
109	  for (let i = 0; i < st.type.length; i++) {
110	    if (!st.flags[i] && st.type[i] !== 0) st.type[i] = 0;
111	  }
112	  const data: SaveData = {
113	    format: 'sandboxworld.save',
114	    version: 2,
115	    header: {
116	      name: world.name, seed: world.seed, width: st.w, height: st.h,
117	      spawn: [world.spawnX, world.spawnY], groundLevel: world.groundLevel, rockLevel: world.rockLevel,
118	      treeX: world.treeX, treeStyle: world.treeStyle, treeTops: world.treeTops,
119	      crimson: world.crimson, dungeonX: world.dungeonX, jungleX: world.jungleX,
120	      created: Date.now(), playTimeMs,
121	    },
122	    clock: { timeOfDay: world.clock.timeOfDay, dayCount: world.clock.dayCount },
123	    tiles: bytesToB64(rleTiles(st)),
124	    walls: bytesToB64(rlePairs(st.wall)),
125	    liquid: bytesToB64(rlePairs(st.liquid)),
126	    liquidType: bytesToB64(rlePairs(st.liquidType)),
127	    chests: world.chests,
128	    player: {
129	      hp: player.hp, x: player.x, y: player.y,
130	      inventory: player.inv.slots, selected: player.inv.selected,
131	    },
132	    npcs: [],
133	    flags: world.flags,
134	  };
135	  return JSON.stringify(data);
136	}
137	
138	export function loadSave(json: string): { world: World; player: { hp: number; x: number; y: number; inventory: Array<{ id: number; stack: number } | null>; selected: number } } {
139	  const data = JSON.parse(json) as SaveData;
140	  const world = new WorldClass(data.header.width, data.header.height, data.header.seed, data.header.name);
141	  world.spawnX = data.header.spawn[0];
142	  world.spawnY = data.header.spawn[1];
143	  world.groundLevel = data.header.groundLevel;
144	  world.rockLevel = data.header.rockLevel;
145	  if (data.header.treeX) world.treeX = data.header.treeX;
146	  if (data.header.treeStyle) world.treeStyle = data.header.treeStyle;
147	  if (data.header.treeTops?.length) world.treeTops = data.header.treeTops;
148	  if (data.header.crimson !== undefined) world.crimson = data.header.crimson;
149	  if (data.header.dungeonX !== undefined) world.dungeonX = data.header.dungeonX;
150	  if (data.header.jungleX !== undefined) world.jungleX = data.header.jungleX;
151	  world.clock.timeOfDay = data.clock.timeOfDay;
152	  world.clock.dayCount = data.clock.dayCount;
153	  world.chests = data.chests;
154	  world.flags = data.flags;
155	
156	  const st = world.store;
157	  // tiles
158	  {
159	    const u8 = b64ToBytes(data.tiles);
160	    const pos = { i: 0 };
161	    let i = 0;
162	    while (i < st.type.length && pos.i < u8.length) {
163	      const run = readVarint(u8, pos) + 1;
164	      const t = readVarint(u8, pos);
165	      let fx = 0, fy = 0;
166	      if (t !== 0) {
167	        fx = readVarint(u8, pos);
168	        fy = readVarint(u8, pos);
169	      }
170	      for (let k = 0; k < run && i < st.type.length; k++, i++) {
171	        st.type[i] = t; st.flags[i] = t !== 0 ? 1 : 0;
172	        st.frameX[i] = fx; st.frameY[i] = fy;
173	      }
174	    }
175	  }
176	  // walls（version<2 的旧档墙值迁移：1=土→2, 2=石→1, 3=木→4（现为原版 id））
177	  {
178	    const legacy = (data.version ?? 1) < 2;
179	    const migrate = (v: number) => (legacy ? (v === 1 ? 2 : v === 2 ? 1 : v === 3 ? 4 : v) : v);
180	    const u8 = b64ToBytes(data.walls);
181	    const pos = { i: 0 };
182	    let i = 0;
183	    while (i < st.wall.length && pos.i < u8.length) {
184	      const run = readVarint(u8, pos) + 1;
185	      const v = migrate(readVarint(u8, pos));
186	      for (let k = 0; k < run && i < st.wall.length; k++, i++) st.wall[i] = v;
187	    }
188	  }
189	  // liquid type（旧存档缺此字段 → 全 0，由液体模拟按 1=水 补全）
190	  {
191	    const u8 = b64ToBytes(data.liquidType ?? '');
192	    const pos = { i: 0 };
193	    let i = 0;
194	    while (i < st.liquidType.length && pos.i < u8.length) {
195	      const run = readVarint(u8, pos) + 1;
196	      const v = readVarint(u8, pos);
197	      for (let k = 0; k < run && i < st.liquidType.length; k++, i++) st.liquidType[i] = v;
198	    }
199	  }
200	  // liquid
201	  {
202	    const u8 = b64ToBytes(data.liquid);
203	    const pos = { i: 0 };
204	    let i = 0;
205	    while (i < st.liquid.length && pos.i < u8.length) {
206	      const run = readVarint(u8, pos) + 1;
207	      const v = readVarint(u8, pos);
208	      for (let k = 0; k < run && i < st.liquid.length; k++, i++) st.liquid[i] = v;
209	    }
210	  }
211	  return { world, player: data.player };
212	}
213	

```


---

## 🤖 Assistant · 2026-08-09T10:48:46.517Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:46.522Z

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
34	  treeX: number[];
35	  treeStyle: number[];
36	  treeTops: number[];
37	  tiles: WldTileData;
38	  chests: WldChest[];
39	  npcs: WldNPC[];
40	}
41	
42	export class WldParseError extends Error {}
43	
44	export function parseWld(buf: Uint8Array): WldWorld {
45	  const r = new BinaryReaderLE(buf);
46	  const version = r.u32();
47	  if (version < 210) {
48	    throw new WldParseError(`不支持的世界文件版本 ${version}（需要 1.4+，version >= 210）。请在游戏中重新保存该地图。`);
49	  }
50	  if (version >= 140) {
51	    // header magic（中文版为不同常量，这里宽放校验）
52	    const magic = new TextDecoder().decode(r.bytes(7));
53	    const fileType = r.byte();
54	    // TEdit FileType 枚举：None=0, Map=1, World=2, Player=3
55	    if (fileType !== 2) throw new WldParseError(`不是世界文件（fileType=${fileType}）`);
56	    if (magic !== 'relogic') {
57	      // 宽放：中文版魔数，只要不是明显非法就继续
58	      if (!/^[a-z]{7}$/i.test(magic)) throw new WldParseError(`无效的文件头魔数: "${magic}"`);
59	    }
60	    r.u32(); // revision
61	    r.u64(); // favorite flags
62	  }
63	  const sectionCount = r.i16();
64	  const pointers: number[] = [];
65	  for (let i = 0; i < sectionCount; i++) pointers.push(r.i32());
66	  // tileFrameImportant 位图（TEdit ReadBitArray：每字节 LSB 在前）
67	  const bitLen = r.i16();
68	  const frameImportant: boolean[] = new Array(bitLen);
69	  {
70	    let data = 0;
71	    for (let i = 0; i < bitLen; i++) {
72	      if ((i & 7) === 0) data = r.byte();
73	      frameImportant[i] = ((data >> (i & 7)) & 1) !== 0;
74	    }
75	  }
76	
77	  // ---- header flags ----
78	  r.seek(pointers[0]);
79	  const title = r.string();
80	  let seed = '';
81	  if (version >= 179) {
82	    seed = version === 179 ? String(r.i32()) : r.string();
83	    r.u64(); // worldGenVersion
84	  }
85	  if (version >= 181) r.bytes(16); // guid
86	  r.i32(); // worldId
87	  r.i32(); r.i32(); r.i32(); r.i32(); // bounds
88	  const tilesHigh = r.i32();
89	  const tilesWide = r.i32();
90	  // gameMode
91	  if (version >= 209) {
92	    r.i32();
93	    if (version >= 222) r.boolean(); // drunk
94	    if (version >= 227) r.boolean(); // good
95	    if (version >= 238) r.boolean();
96	    if (version >= 239) r.boolean();
97	    if (version >= 241) r.boolean();
98	    if (version >= 249) r.boolean(); // remix
99	    if (version >= 266) r.boolean(); // notraps
100	    if (version >= 267) r.boolean(); // zenith
101	    if (version >= 302) r.boolean(); // skyblock
102	  } else if (version === 208 || version >= 112) {
103	    r.boolean();
104	  }
105	  if (version >= 141) r.i64(); // creationTime
106	  if (version >= 284) r.i64(); // lastPlayed
107	  r.u8(); // moonType
108	  const treeX = [r.i32(), r.i32(), r.i32()];       // 世界横向 4 区分界（树样式用）
109	  let treeTops: number[] = [];                    // TreeTops 13 区域变体（v≥211 优先于 header treeStyle）
110	  const treeStyle = [r.i32(), r.i32(), r.i32(), r.i32()]; // 各区森林树样式
111	  for (let i = 0; i < 3; i++) r.i32(); // caveBackX
112	  for (let i = 0; i < 4; i++) r.i32(); // caveBackStyle
113	  r.i32(); r.i32(); r.i32(); // ice/jungle/hell back style
114	  const spawnX = r.i32();
115	  const spawnY = r.i32();
116	  const groundLevel = r.f64();
117	  const rockLevel = r.f64();
118	  const time = r.f64();
119	  const dayTime = r.boolean();
120	  r.i32(); // moonPhase
121	  r.boolean(); // blood moon
122	  r.boolean(); // eclipse
123	  r.i32(); r.i32(); // dungeon xy
124	  const isCrimson = r.boolean();
125	  for (let i = 0; i < 10; i++) r.boolean(); // downed bosses
126	  if (version >= 118) r.boolean(); // slime king
127	  for (let i = 0; i < 7; i++) r.boolean(); // saved goblin etc
128	  r.boolean(); r.boolean(); // orb smashed / spawn meteor
129	  r.u8(); // orb count
130	  r.i32(); // altar count
131	  const hardMode = r.boolean();
132	  if (version >= 257) r.boolean(); // party of doom
133	  r.i32(); r.i32(); r.i32(); r.f64(); // invasion
134	  if (version >= 118) r.f64(); // slime rain
135	  if (version >= 113) r.u8(); // sundial
136	  r.boolean(); r.i32(); r.f32(); // rain
137	  r.i32(); r.i32(); r.i32(); // ore tiers
138	  for (let i = 0; i < 8; i++) r.u8(); // bg styles
139	  r.i32(); r.i16(); r.f32(); // clouds/wind
140	  // angler
141	  {
142	    const n = r.i32();
143	    for (let i = 0; i < n; i++) r.string();
144	  }
145	  r.boolean(); // savedAngler
146	  r.i32(); // anglerQuest
147	  r.boolean(); // savedStylist
148	  if (version >= 140) r.boolean(); // tax collector
149	  if (version >= 201) r.boolean(); // golfer
150	  if (version >= 107) r.i32(); // invasionSizeStart
151	  if (version >= 108) r.i32(); // cultistDelay
152	  // banners
153	  {
154	    const n = r.i16();
155	    for (let i = 0; i < n; i++) r.i32();
156	    if (version >= 289) {
157	      const m = r.i16();
158	      for (let i = 0; i < m; i++) r.u16();
159	    }
160	  }
161	  if (version >= 140) r.boolean(); // fastForwardTime
162	  r.boolean(); // fishron
163	  if (version >= 140) { r.boolean(); r.boolean(); r.boolean(); } // martians/cultist/moonlord
164	  for (let i = 0; i < 5; i++) r.boolean(); // holiday bosses
165	  for (let i = 0; i < 4; i++) r.boolean(); // celestial downed
166	  for (let i = 0; i < 4; i++) r.boolean(); // celestial active
167	  r.boolean(); // apocalypse
168	  if (version >= 170) {
169	    r.boolean(); r.boolean(); r.i32();
170	    const n = r.i32();
171	    for (let i = 0; i < n; i++) r.i32();
172	  }
173	  if (version >= 174) { r.boolean(); r.i32(); r.f32(); r.f32(); }
174	  if (version >= 178) { r.boolean(); r.boolean(); r.boolean(); r.boolean(); }
175	  if (version > 194) r.u8(); // mushroom bg
176	  if (version >= 215) r.u8(); // underworld bg
177	  if (version >= 195) { r.u8(); r.u8(); r.u8(); }
178	  if (version >= 204) r.boolean(); // combat book
179	  if (version >= 207) { r.i32(); r.boolean(); r.boolean(); r.boolean(); }
180	  if (version >= 211) {
181	    // TreeTops 变体表（WorldGen.TreeTops.Load：13 个区域树样式，v≥211 世界用这个）
182	    const n = r.i32();
183	    treeTops = [];
184	    for (let i = 0; i < n; i++) treeTops.push(r.i32());
185	  }
186	  if (version >= 212) { r.boolean(); r.boolean(); }
187	  if (version >= 216) { r.i32(); r.i32(); r.i32(); r.i32(); }
188	  if (version >= 217) { r.boolean(); r.boolean(); r.boolean(); }
189	  if (version >= 223) { r.boolean(); r.boolean(); }
190	  if (version >= 240) r.boolean();
191	  if (version >= 250) r.boolean();
192	  if (version >= 251) { for (let i = 0; i < 8; i++) r.boolean(); }
193	  if (version >= 259) r.boolean();
194	  if (version >= 260) r.boolean();
195	  if (version >= 261) { for (let i = 0; i < 7; i++) r.boolean(); }
196	  if (version >= 264) { r.boolean(); r.u8(); }
197	  if (version >= 287) { r.boolean(); r.boolean(); }
198	  if (version >= 288) r.boolean();
199	  if (version >= 296) r.boolean();
200	  if (version >= 291) { r.i32(); r.i32(); }
201	  if (version >= 297) {
202	    r.boolean();
203	    const n = r.u8();
204	    for (let i = 0; i < n; i++) { r.i16(); r.i16(); }
205	  }
206	  if (version >= 304) r.boolean();
207	  if (version >= 299 && version < 313) r.u32();
208	  if (version >= 299) r.string(); // manifest
209	
210	  // ---- tiles ----
211	  if (pointers.length < 5) throw new WldParseError('section 数量不足，不是有效的 1.4 世界文件');
212	  r.seek(pointers[1]);
213	  const tiles = decodeTiles(r, tilesWide, tilesHigh, version, frameImportant);
214	
215	  // ---- chests ----
216	  r.seek(pointers[2]);
217	  const chests: WldChest[] = [];
218	  {
219	    const total = r.i16();
220	    let maxItems = 40;
221	    if (version < 294) maxItems = r.i16();
222	    for (let i = 0; i < total; i++) {
223	      const x = r.i32(), y = r.i32();
224	      const name = r.string();
225	      if (version >= 294) maxItems = r.i32();
226	      const items: Array<{ id: number; stack: number } | null> = [];
227	      for (let s = 0; s < maxItems; s++) {
228	        const stack = r.i16();
229	        if (stack > 0) {
230	          const id = r.i32();
231	          r.u8(); // prefix
232	          items.push({ id, stack });
233	        } else {
234	          items.push(null);
235	        }
236	      }
237	      chests.push({ x, y, name, items });
238	    }
239	  }
240	
241	  // ---- npcs ----
242	  r.seek(pointers[4]);
243	  const npcs: WldNPC[] = [];
244	  {
245	    if (version >= 268) {
246	      const n = r.i32();
247	      for (let i = 0; i < n; i++) r.i32();
248	    }
249	    while (r.boolean()) {
250	      const spriteId = version >= 190 ? r.i32() : 0;
251	      if (version < 190) r.string();
252	      const displayName = r.string();
253	      const x = r.f32(), y = r.f32();
254	      r.boolean(); // homeless
255	      const homeX = r.i32(), homeY = r.i32();
256	      if (version >= 213) {
257	        const flag = r.u8();
258	        if (flag & 1) r.i32();
259	      }
260	      if (version >= 315) r.boolean();
261	      npcs.push({ spriteId, name: displayName, x, y, homeX, homeY });
262	    }
263	  }
264	
265	  return {
266	    version, title, seed, tilesWide, tilesHigh, spawnX, spawnY,
267	    groundLevel, rockLevel, time, dayTime, isCrimson, hardMode,
268	    treeX, treeStyle, treeTops,
269	    tiles, chests, npcs,
270	  };
271	}
272	
273	/** tiles 段解码：列优先 + header 链 + RLE */
274	function decodeTiles(
275	  r: BinaryReaderLE, w: number, h: number,
276	  version: number, frameImportant: boolean[],
277	): WldTileData {
278	  const n = w * h;
279	  const active = new Uint8Array(n);
280	  const type = new Uint16Array(n);
281	  const frameX = new Uint16Array(n);
282	  const frameY = new Uint16Array(n);
283	  const wall = new Uint16Array(n);
284	  const liquid = new Uint8Array(n);
285	  const liquidType = new Uint8Array(n);
286	
287	  let idx = 0; // y * w + x，列优先推进
288	  for (let x = 0; x < w; x++) {
289	    for (let y = 0; y < h; y++) {
290	      const header1 = r.u8();
291	      let header2 = 0, header3 = 0, header4 = 0;
292	      if (header1 & 0x01) header2 = r.u8();
293	      if (header2 & 0x01) header3 = r.u8();
294	      if (version >= 269 && header3 & 0x01) header4 = r.u8();
295	      void header4;
296	
297	      let tileType = 0;
298	      let fx = 0, fy = 0;
299	      if (header1 & 0x02) {
300	        // active
301	        if (header1 & 0x20) {
302	          tileType = r.u16();
303	        } else {
304	          tileType = r.u8();
305	        }
306	        const isFramed = tileType < frameImportant.length ? frameImportant[tileType] : true;
307	        if (isFramed) {
308	          fx = r.u16();
309	          fy = r.u16();
310	        }
311	        if (header3 & 0x08) r.u8(); // tile color
312	      }
313	      let wl = 0;
314	      if (header1 & 0x04) {
315	        wl = r.u8();
316	        if (header3 & 0x10) r.u8(); // wall color
317	        if (version >= 222 && header3 & 0x40) {
318	          wl |= r.u8() << 8;
319	        }
320	      }
321	      const lqType = (header1 & 0x18) >> 3;
322	      let lqAmount = 0, lqKind = 0;
323	      if (lqType !== 0) {
324	        lqAmount = r.u8();
325	        lqKind = (version >= 269 && header3 & 0x80) ? 1 : lqType;
326	      }
327	      // RLE 计数
328	      const rleStorage = (header1 & 0xC0) >> 6;
329	      let rle = 0;
330	      if (rleStorage === 1) rle = r.u8();
331	      else if (rleStorage >= 2) rle = r.u16();
332	
333	      // 写入本格 + RLE 重复格（列优先向下）
334	      for (let k = 0; k <= rle && y + k < h; k++) {
335	        const i = (y + k) * w + x;
336	        active[i] = (header1 & 0x02) ? 1 : 0;
337	        type[i] = tileType;
338	        frameX[i] = fx;
339	        frameY[i] = fy;
340	        wall[i] = wl;
341	        liquid[i] = lqAmount;
342	        liquidType[i] = lqKind;
343	      }
344	      y += rle;
345	    }
346	  }
347	  void idx;
348	  return { active, type, frameX, frameY, wall, liquid, liquidType };
349	}
350	

```


---

## 🤖 Assistant · 2026-08-09T10:48:49.263Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read Game.ts (large, 2339 lines), items.ts, ChunkCache.ts, Renderer.ts, Door.ts, LiquidSim.ts, Sfx.ts, Input.ts, Dart.ts.

Let me read Game.ts in chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:48:49.266Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 700
}
```


---

## 🤖 Assistant · 2026-08-09T10:48:49.270Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:49.283Z

**📎 ToolResult**

```
1	// chunk 静态缓存：每 chunk 16×16 tile 预渲染到离屏 canvas（墙层+tile 层）
2	import { CHUNK, TILE } from '../core/constants';
3	import { T, TILE_DEFS, WALL_DEFS, TILE_BY_KEY } from '../data/tiles';
4	import { hash2 } from '../core/rng';
5	import { drawVanillaCell, drawTreeCell } from './VanillaTiler';
6	import { VanillaWallTiler } from './VanillaWallTiler';
7	import { shade } from '../assets/Palette';
8	import type { TileSheetEntry } from '../assets/TileSheetGen';
9	import type { AutoTiler } from './AutoTiler';
10	import type { World } from '../world/World';
11	
12	// 我们的 tile → Maples RuleTile 规则名（有规则的走素材自动贴合，无规则回退程序化）
13	// Grass 走人工标注（'@grass'）：Tiles_2.png 是多 tile 混排图集，自动分类不可靠；
14	// 用 public/annotator.html 标注后写入 sprites/annotations.json。无标注时回退程序化。
15	const TILE_RULES: Record<number, string> = {
16	  // 泥土/石/草走原版 BlendRules；铁矿走原版表——均不再用 Maples 规则
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
31	  wallTiler: VanillaWallTiler | null;
32	  truncatesWalls: number[] = [];
33	
34	  constructor(world: World, sheets: Map<number, TileSheetEntry>, autotiler: AutoTiler | null = null, wallTiler: VanillaWallTiler | null = null) {
35	    this.world = world;
36	    this.sheets = sheets;
37	    this.autotiler = autotiler;
38	    this.wallTiler = wallTiler;
39	    // 原版 TileID.Sets.TruncatesWalls（54 玻璃 / 328 暗影宝箱 / 459 / 748）→ 内部 tile id
40	    this.truncatesWalls = ['glass', 'v_328_shadow_chest', 'v_459_', 'v_748_']
41	      .map((k) => TILE_BY_KEY[k] ?? -1)
42	      .filter((id) => id >= 0);
43	    world.store.onTileChanged((x, y) => this.markDirtyAround(x, y));
44	  }
45	
46	  static key(cx: number, cy: number): number {
47	    return (cx & 0xffff) | ((cy & 0xffff) << 16);
48	  }
49	
50	  markDirty(cx: number, cy: number) {
51	    const k = ChunkCache.key(cx, cy);
52	    if (!this.chunks.has(k)) return; // 未生成的 chunk 惰性创建
53	    this.chunks.set(k, undefined as unknown as ChunkPair); // 标记删除，重绘时重建
54	    if (!this.dirtyQueue.includes(k)) this.dirtyQueue.push(k);
55	  }
56	
57	  /** 区域标脏（tile 范围）：供树冠等大范围精灵清理使用 */
58	  markDirtyArea(x0: number, y0: number, x1: number, y1: number) {
59	    for (let cy = Math.floor(y0 / CHUNK); cy <= Math.floor(y1 / CHUNK); cy++) {
60	      for (let cx = Math.floor(x0 / CHUNK); cx <= Math.floor(x1 / CHUNK); cx++) {
61	        if (cx < 0 || cy < 0) continue;
62	        this.markDirty(cx, cy);
63	      }
64	    }
65	  }
66	
67	  markDirtyAround(x: number, y: number) {
68	    const cx = Math.floor(x / CHUNK), cy = Math.floor(y / CHUNK);
69	    this.markDirty(cx, cy);
70	    // 边缘融合：邻接 chunk 也要标脏
71	    if (x % CHUNK === 0) this.markDirty(cx - 1, cy);
72	    if (x % CHUNK === CHUNK - 1) this.markDirty(cx + 1, cy);
73	    if (y % CHUNK === 0) this.markDirty(cx, cy - 1);
74	    if (y % CHUNK === CHUNK - 1) this.markDirty(cx, cy + 1);
75	  }
76	
77	  /** 每帧最多重绘 maxN 个脏 chunk */
78	  flushDirty(maxN = 4) {
79	    let n = 0;
80	    while (this.dirtyQueue.length && n < maxN) {
81	      const k = this.dirtyQueue.shift()!;
82	      const cx = k & 0xffff, cy = (k >> 16) & 0xffff;
83	      if (this.chunks.get(k) !== undefined) continue; // 已重建
84	      this.get(cx, cy);
85	      n++;
86	    }
87	  }
88	
89	  /** 取 chunk 双层画布（惰性生成） */
90	  get(cx: number, cy: number): ChunkPair {
91	    const k = ChunkCache.key(cx, cy);
92	    let c = this.chunks.get(k);
93	    if (c) return c;
94	    c = this.renderChunk(cx, cy);
95	    this.chunks.set(k, c);
96	    return c;
97	  }
98	
99	  /** 树枝判定：TREE 且上下皆非 TREE、恰好一侧为 TREE（横向独连树干）。
100	   *  下方是实心地面的属于树根底座 —— 走规则表渲染底座贴图，不算枝干 */
101	
102	  private neighborMask(x: number, y: number, type: number): number {
103	    const st = this.world.store;
104	    let mask = 0;
105	    const same = (nx: number, ny: number) => st.inBounds(nx, ny) && st.flags[st.idx(nx, ny)] && st.type[st.idx(nx, ny)] === type ? 1 : 0;
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
129	    // 原版墙 framing（VanillaWallTiler）：32×32 帧以格为中心外溢 8px →
130	    // 扫描范围外扩 1 格，跨 chunk 边界的帧由相邻 chunk 补齐（像素一致无副作用）
131	    if (this.wallTiler) {
132	      const EXT = 1;
133	      for (let ly = -EXT; ly < CHUNK + EXT; ly++) {
134	        for (let lx = -EXT; lx < CHUNK + EXT; lx++) {
135	          const x = x0 + lx, y = y0 + ly;
136	          if (!st.inBounds(x, y)) continue;
137	          const i = st.idx(x, y);
138	          const wallId = st.wall[i];
139	          if (wallId === 0) continue;
140	          const px = lx * TILE, py = ly * TILE;
141	          if (this.wallTiler.hasTexture(wallId)) {
142	            this.wallTiler.draw(ctx, st, x, y, wallId, this.truncatesWalls, px, py);
143	          } else {
144	            const wd = WALL_DEFS[wallId];
145	            if (wd) {
146	              ctx.fillStyle = wd.mapColor;
147	              ctx.fillRect(px, py, TILE, TILE);
148	              ctx.fillStyle = shade(wd.mapColor, 0.8);
149	              ctx.fillRect(px, py + TILE - 1, TILE, 1);
150	              ctx.fillRect(px + TILE - 1, py, 1, TILE);
151	            }
152	          }
153	        }
154	      }
155	    }
156	
157	    // ---- 第二遍：前景 tile / 物体（绘制到 tile 层画布；水渲染在墙层与 tile 层之间）----
158	    ctx = tile.getContext('2d')!;
159	    ctx.imageSmoothingEnabled = false;
160	    for (let ly = 0; ly < CHUNK; ly++) {
161	      for (let lx = 0; lx < CHUNK; lx++) {
162	        const x = x0 + lx, y = y0 + ly;
163	        if (!st.inBounds(x, y)) continue;
164	        const i = st.idx(x, y);
165	        const px = lx * TILE, py = ly * TILE;
166	        const type = st.type[i];
167	        // 原版语义:非活性格不渲染(TileRunner 会给空气格写幽灵 type)
168	        if (type === 0 || !st.flags[i]) continue;
169	        const def = TILE_DEFS[type];
170	        if (!def) { ctx.fillStyle = '#808080'; ctx.fillRect(px, py, TILE, TILE); continue; }
171	        // 原版素材图块（TileDef.vanilla）：TEdit framing 查找表（auto）或显式 18px 帧（style）
172	        if (def.vanilla && this.autotiler) {
173	          drawVanillaCell(
174	            ctx, this.autotiler.atlas, def.vanilla.sheet, def.vanilla.frame,
175	            def.vanilla.fw ?? 1, def.vanilla.fh ?? 1,
176	            st, x, y, type,
177	            (t) => t === type, // 同 id 融合判定（后续可扩 mergeWith）
178	            px, py, st.frameX[i], st.frameY[i],
179	            { treeX: this.world.treeX, treeStyle: this.world.treeStyle, treeTops: this.world.treeTops,
180	              worldSurface: this.world.groundLevel, worldW: this.world.w },
181	          );
182	          continue;
183	        }
184	        // 树苗：Tree_Bodys 树干段作小苗（底部对齐）
185	        if (type === T.SAPLING && this.autotiler) {
186	          const r = this.autotiler.saplingSprite(x, y);
187	          if (r) {
188	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px + (TILE - r.sw) / 2, py + TILE - r.sh, r.sw, r.sh);
189	            continue;
190	          }
191	        }
192	        // 杂草：Maples Tiles_3 杂草贴图（16×20，底部对齐，hash 选变体）
193	        if (type === T.TALLGRASS && this.autotiler) {
194	          const r = this.autotiler.weedSprite(x, y);
195	          if (r) {
196	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px - (r.sw - TILE) / 2, py + TILE - r.sh, r.sw, r.sh);
197	            continue;
198	          }
199	        }
200	        // 有 RuleTile 规则的 tile 用 Maples 素材自动贴合
201	        const ruleName = this.autotiler ? TILE_RULES[type] : undefined;
202	        if (ruleName && this.autotiler) {
203	          // 草皮覆盖件：保持原生透明（缺口露出背后的墙/天空），不做任何垫底/填充
204	          if (ruleName === '@grass') {
205	            const r = this.autotiler.tile(ruleName, st, x, y, type);
206	            if (r) ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, px, py, TILE, TILE);
207	            continue;
208	          }
209	          const r = this.autotiler.tile(ruleName, st, x, y, type);
210	          if (r) {
211	            // 大图（树冠 80×80，宽>2格）跳过 —— 第三遍统一绘制（跨 chunk 补全 + 树叶盖树干）
212	            if (r.sw > TILE * 2) continue;
213	            // 按精灵原始尺寸绘制。树干等"宽≤2格、高>1格"的竖向件顶部对齐：
214	            // 溢出向下伸，由更下方的格（后画）覆盖 —— 下层不压上层。
215	            let dy = py + (TILE - r.sh) / 2;
216	            if (r.sh > TILE && r.sw <= TILE * 2) dy = py;
217	            const dx = px + (TILE - r.sw) / 2;
218	            ctx.drawImage(r.img, r.sx, r.sy, r.sw, r.sh, dx, dy, r.sw, r.sh);
219	            continue;
220	          }
221	        }
222	        const entry = this.sheets.get(type);
223	        if (!entry) {
224	          ctx.fillStyle = '#FF00FF';
225	          ctx.fillRect(px, py, TILE, TILE);
226	          continue;
227	        }
228	        if (entry.kind === 'blend') {
229	          const mask = this.neighborMask(x, y, type);
230	          const col = mask & 15, row = mask >> 4;
231	          ctx.drawImage(entry.canvas, col * TILE, row * TILE, TILE, TILE, px, py, TILE, TILE);
232	        } else if (entry.kind === 'object') {
233	          // 仅锚点绘制整体
234	          if (st.frameX[i] === 0 && st.frameY[i] === 0) {
235	            const w = (entry.w ?? 1) * TILE, h = (entry.h ?? 1) * TILE;
236	            ctx.drawImage(entry.canvas, px, py, w, h);
237	          }
238	        } else {
239	          // single：帧偏移直接取
240	          ctx.drawImage(entry.canvas, st.frameX[i], st.frameY[i], TILE, TILE, px, py, TILE, TILE);
241	        }
242	      }
243	    }
244	    // ---- 第三遍：半砖（halfBrick）——主绘制后清掉上半 8px ----
245	    // 原版 TileDrawing.cs:689-690：源矩形高度 -8、目标下移 8（贴图上半画进格下半）。
246	    // 此处统一后处理 clearRect 上半（对 blend/auto/rule 全部绘制路径生效；
247	    // 与原版的差异是保留贴图下半而非上半，纹理内容差异可忽略）
248	    for (let ly = 0; ly < CHUNK; ly++) {
249	      for (let lx = 0; lx < CHUNK; lx++) {
250	        const i = st.idx(x0 + lx, y0 + ly);
251	        if (st.half[i]) ctx.clearRect(lx * TILE, ly * TILE, TILE, 8);
252	      }
253	    }
254	
255	    // ---- 第四遍：原版树冠/树枝（tile 5 标记帧，跨 chunk 外扩绘制） ----
256	    // 树冠 80×80 / 树枝 40×40 跨多格，主遍跳过这些标记帧，由此外扩遍统一绘制防裁剪。
257	    // 棕榈（323）整棵都在此绘制：干身 frameY 是倾斜偏移（最大 ±12px 跨列），
258	    // 主遍画会在 chunk 边缘列被裁剪 → 干+冠全部走外扩遍
259	    if (this.autotiler) {
260	      const treeIds = ['tree', 'v_72_mushroom_tree', 'v_323_palm_trees', 'v_5_trees',
261	        'v_583_topaz_tree', 'v_584_amethyst_tree', 'v_585_sapphire_tree', 'v_586_emerald_tree',
262	        'v_587_ruby_tree', 'v_588_diamond_tree', 'v_589_amber_tree',
263	        'v_596_vanity_tree_sakura', 'v_616_vanity_tree_yellow_willow', 'v_634_ash_tree']
264	        .map((k) => TILE_BY_KEY[k]).filter((id) => id !== undefined);
265	      for (const v5 of treeIds) {
266	        const EXT = 6;
267	        for (let ty = y0 - EXT; ty < y0 + CHUNK + EXT; ty++) {
268	          for (let tx = x0 - EXT; tx < x0 + CHUNK + EXT; tx++) {
269	            if (!st.inBounds(tx, ty)) continue;
270	            const i = st.idx(tx, ty);
271	            if (st.type[i] !== v5) continue;
272	            const fx = st.frameX[i], fy = st.frameY[i];
273	            const def = TILE_DEFS[st.type[i]];
274	            const sheet = def?.vanilla?.sheet ?? 5;
275	            const isPalm = sheet === 323;
276	            const isCrown = isPalm ? (fx >= 88 && fx <= 132) : (fy >= 198 && fx >= 22);
277	            if (isPalm) {
278	              // 棕榈：干+冠都画（干身倾斜跨列，必须外扩遍）
279	              drawTreeCell(ctx, this.autotiler.atlas, st, tx, ty, fx, fy,
280	                tx * TILE - x0 * TILE, ty * TILE - y0 * TILE, sheet, isCrown,
281	                { treeX: this.world.treeX, treeStyle: this.world.treeStyle, treeTops: this.world.treeTops,
282	                worldSurface: this.world.groundLevel, worldW: this.world.w });
283	            } else if (isCrown) {
284	              // 其他树：仅标记帧（干身由主遍绘制）
285	              drawTreeCell(ctx, this.autotiler.atlas, st, tx, ty, fx, fy,
286	                tx * TILE - x0 * TILE, ty * TILE - y0 * TILE, sheet, true,
287	                { treeX: this.world.treeX, treeStyle: this.world.treeStyle, treeTops: this.world.treeTops,
288	                worldSurface: this.world.groundLevel, worldW: this.world.w });
289	            }
290	          }
291	        }
292	      }
293	    }
294	
295	    return { wall, tile };
296	  }
297	}
298	

```


---

## 👤 User(sidechain) · 2026-08-09T10:48:49.458Z

**📎 ToolResult**

```
1	// 游戏主控制器：状态、主循环、挖掘/放置/战斗/生成/存档的总装
2	import { TILE, SPAWN_CHECK_INTERVAL, ENEMY_CAP, SPAWN_MIN_DIST, SPAWN_MAX_DIST } from './constants';
3	import { RNG } from './rng';
4	import { Input } from './Input';
5	import { buildAssets, AssetBundle } from '../assets/AssetGen';
6	import { World, ChestData } from '../world/World';
7	import { generateWorld } from '../world/gen/WorldGen';
8	import { openDoor, closeDoor, clearDoorAt } from '../world/Door';
9	import { TILE_DEFS, T, TILE_BY_KEY } from '../data/tiles';
10	import { ITEM_DEFS, ITEM_BY_KEY } from '../data/items';
11	import { poolFor, vanillaNpc } from '../data/vanillaNpcs';
12	import { ENEMY_DEFS } from '../data/enemies';
13	import { RECIPES } from '../data/recipes';
14	import { Player } from '../entities/Player';
15	import { Enemy } from '../entities/Enemy';
16	import { ItemDrop } from '../entities/ItemDrop';
17	import { TownNPC } from '../entities/TownNPC';
18	import { Tombstone } from '../entities/Tombstone';
19	import { Critter } from '../entities/Critter';
20	import { CRITTER_DEFS } from '../data/critters';
21	import { EntityManager, Entity } from '../entities/Entity';
22	import { Camera } from '../render/Camera';
23	import { ChunkCache } from '../render/ChunkCache';
24	import { Renderer, Particle, DamageNumber, Minimap } from '../render/Renderer';
25	import { LightingEngine } from '../lighting/LightingEngine';
26	import { Inventory, ACCESSORY_START, ARMOR_START } from '../items/Inventory';
27	
28	// 导入的原版树族 tile（fellImportedTree 整棵砍伐）：普通树 + 宝石树 + 装饰树 + 灰烬树
29	const IMPORTED_TREE_TYPES = new Set<number>(
30	  ['v_5_trees',
31	    'v_583_topaz_tree', 'v_584_amethyst_tree', 'v_585_sapphire_tree', 'v_586_emerald_tree',
32	    'v_587_ruby_tree', 'v_588_diamond_tree', 'v_589_amber_tree',
33	    'v_596_vanity_tree_sakura', 'v_616_vanity_tree_yellow_willow', 'v_634_ash_tree',
34	    'v_72_mushroom_tree', 'v_323_palm_trees']
35	    .map((k) => TILE_BY_KEY[k])
36	    .filter((v): v is number => v !== undefined),
37	);
38	import { LiquidSim } from '../world/liquid/LiquidSim';
39	import { BuffType } from '../stats/Buffs';
40	import { SpriteAtlas } from '../assets/SpriteAtlas';
41	import { AutoTiler } from '../render/AutoTiler';
42	import { VanillaWallTiler } from '../render/VanillaWallTiler';
43	import { Sfx, SfxName } from './Sfx';
44	import { HitTile } from './HitTile';
45	import type { GameHooks } from '../entities/types';
46	import { Dart } from '../entities/Dart';
47	import { Arrow } from '../entities/Arrow';
48	import { Minecart } from '../entities/Minecart';
49	import { MagicProj } from '../entities/MagicProj';
50	
51	const FIXED_DT = 1 / 60;
52	
53	export interface GameCallbacks {
54	  onWorldReady: () => void;
55	  onInventoryChanged: () => void;
56	  onToast: (msg: string) => void;
57	  onBuffsChanged?: () => void;
58	  onDayNight?: (isDay: boolean) => void;
59	}
60	
61	export class Game implements GameHooks {
62	  assets: AssetBundle;
63	  atlas: SpriteAtlas | null = null;
64	  autotiler: AutoTiler | null = null;
65	  world!: World;
66	  player!: Player;
67	  camera!: Camera;
68	  renderer: Renderer;
69	  chunks!: ChunkCache;
70	  lighting!: LightingEngine;
71	  liquid!: LiquidSim;
72	  entities = new EntityManager();
73	  input: Input;
74	  cb: GameCallbacks;
75	  sfx = new Sfx();
76	
77	  running = false;
78	  paused = false;
79	  private acc = 0;
80	  private lastTime = 0;
81	  private tickCount = 0;
82	
83	  // 挖掘状态
84	  private mining: { x: number; y: number; progress: number } | null = null;
85	  /** 当前挖掘目标的硬度缓存（进度归一化用） */
86	  private hardnessCache = 1;
87	  /** 原版 HitTile 伤害积累（劈砍/挖掘通用，阈值 100） */
88	  private hitTiles = new HitTile();
89	  private lastMineHitTick = -999;
90	  swing: { t: number; dur: number; item: number } | null = null;
91	  private swingHitSet = new Set<number>();
92	
93	  // 弹药
94	  particles: Particle[] = [];
95	  dmgNumbers: DamageNumber[] = [];
96	
97	  // 敌人生成
98	  private spawnTimer = 0;
99	  boss: Enemy | null = null;
100	  /** tile key → id 反查表（调试句柄/wld 导入映射用） */
101	  tileByKey = TILE_BY_KEY;
102	
103	  /** 开发者模式：全部道具入包（溢出的落在展示区上方）+ 出生点右侧摆放所有可放置图块供检验 */
104	  setupDevMode() {
105	    const p = this.player;
106	    const st = this.world.store;
107	    // ---- 1) 全道具入包 ----
108	    const overflow: Array<[string, number]> = [];
109	    for (const def of ITEM_DEFS) {
110	      const n = def.maxStack === 1 ? 1 : Math.min(def.maxStack, 99);
111	      const left = p.inv.add(ITEM_BY_KEY[def.key], n);
112	      if (left > 0) overflow.push([def.key, left]);
113	    }
114	    // ---- 2) 展示区：出生点右侧清空并逐行摆放全部可放置图块 ----
115	    const sx = this.world.spawnX, sy = this.world.spawnY;
116	    const x0 = sx + 6, x1 = sx + 70, yBot = sy - 2, yTop = sy - 40;
117	    for (let x = x0; x <= x1; x++) {
118	      for (let y = yTop; y <= yBot; y++) {
119	        st.setTile(x, y, 0);
120	        st.setLiquid(x, y, 0, 0);
121	      }
122	      st.setTile(x, yBot, T.STONE);
123	      st.setTile(x, yBot + 1, T.STONE);
124	    }
125	    // 收集可放置 tile（有物品指向，去重）
126	    const placeable: number[] = [];
127	    const seen = new Set<number>();
128	    for (const def of ITEM_DEFS) {
129	      if (!def.tile) continue;
130	      const tid = TILE_BY_KEY[def.tile];
131	      if (tid === undefined || tid === 0 || seen.has(tid)) continue;
132	      seen.add(tid);
133	      placeable.push(tid);
134	    }
135	    // 逐行摆放：行高 7（最高家具 5 格 + 间隙），每行放满换行并铺新地板
136	    let cx = x0 + 1, cy = yBot - 1;
137	    const rowH = 7;
138	    for (const tid of placeable) {
139	      const td = TILE_DEFS[tid];
140	      const w = td.vanilla?.fw ?? td.w ?? 1;
141	      const h = td.vanilla?.fh ?? td.h ?? 1;
142	      if (cx + w > x1 - 1) {
143	        cx = x0 + 1;
144	        cy -= rowH;
145	        for (let x = x0; x <= x1; x++) st.setTile(x, cy, T.STONE);
146	      }
147	      for (let dx = 0; dx < w; dx++) {
148	        for (let dy = 0; dy < h; dy++) {
149	          // 原版帧语义（TileObject.Place）：顶行 frameY=0，底行最大——
150	          // 此处 cy 是底部行，dy=0 是底行 → frameY = (h-1-dy)*18
151	          st.setTile(cx + dx, cy - dy, tid, td.vanilla ? dx * 18 : dx, td.vanilla ? (h - 1 - dy) * 18 : dy);
152	        }
153	      }
154	      cx += w + 1;
155	    }
156	    // ---- 3) 溢出道具以掉落物排在展示区上方（背包 40 格装不下的部分） ----
157	    let dxDrop = x0;
158	    let dyDrop = yTop + 3;
159	    for (const [key, n] of overflow) {
160	      this.spawnDrop(dxDrop * TILE + 8, dyDrop * TILE, key, n, 0, 0);
161	      dxDrop += 2;
162	      if (dxDrop > x1 - 1) { dxDrop = x0; dyDrop += 3; }
163	    }
164	    this.cb.onInventoryChanged();
165	    this.cb.onToast(`开发者模式：${overflow.length} 种道具背包装不下，已排在展示区上方；全部可放置图块在出生点右侧`);
166	  }
167	
168	  // NPC 系统
169	  private housingCheckTimer = 0;
170	  guideSpawned = false;
171	  private lastWasDay: boolean | null = null;
172	  private _mapClickLatch = false;
173	  private _mapClickLatch2 = false;
174	  /** 地图内按压起点（松开时与当前位置比对 <6px 判定为点击，否则是拖动） */
175	  private _mapPressX = 0;
176	  private _mapPressY = 0;
177	  private _tpTarget: { x: number; y: number } | null = null;
178	  // 方块标注模式（F5）：点击标记问题方块，导出标注+地图给开发者定位
179	  annotateMode = false;
180	  waterCandleNear = false;
181	  heldWaterCandle = false;
182	  trackTile = TILE_BY_KEY['v_314_minecart_track'] ?? 0;
183	  minecart: import('../entities/Minecart').Minecart | null = null;
184	  trapCooldown = new Map<string, number>();
185	  plateLatch = new Set<string>();
186	  // 贴图纠错子模式：点击方块弹出该图块的完整原版贴图表供选帧
187	  fixTexMode = false;
188	  // 敌人生成开关（F8）：关闭后不再生成新怪物（已有的不受影响）
189	  enemySpawnEnabled = true;
190	  marks: Array<{ x: number; y: number }> = [];
191	  private _annoLatch = false;
192	
193	  constructor(root: HTMLElement, cb: GameCallbacks, atlas?: SpriteAtlas | null) {
194	    this.assets = buildAssets();
195	    if (atlas) {
196	      this.atlas = atlas;
197	      this.autotiler = new AutoTiler(atlas);
198	    }
199	    this.renderer = new Renderer(this.assets, atlas);
200	    this.renderer.attach(root);
201	    this.sfx.load(); // 原版 wav 预解码（挂起态也可解码）
202	    // 怪物专属声效文件追加载入
203	    const extra = new Set<string>();
204	    for (const d of Object.values(ENEMY_DEFS)) for (const f of [...d.hitSound, ...d.killedSound]) extra.add(f);
205	    this.sfx.addFiles([...extra]);
206	    this.input = new Input(this.renderer.canvas);
207	    this.cb = cb;
208	    // 快捷栏数字键：事件驱动（避免单帧内 down+up 被轮询漏掉）
209	    this.input.keydownHandlers.push((code) => {
210	      if (this.player && /^Digit[0-9]$/.test(code)) {
211	        this.player.inv.selected = code === 'Digit0' ? 9 : Number(code.slice(5)) - 1;
212	        this.cb.onInventoryChanged();
213	      }
214	      // 缩放调节
215	      if (code === 'Equal' || code === 'NumpadAdd') this.setZoom(this.camera?.zoomTarget + 0.15);
216	      if (code === 'Minus' || code === 'NumpadSubtract') this.setZoom(this.camera?.zoomTarget - 0.15);
217	    });
218	  }
219	
220	  // ================= 生命周期 =================
221	
222	  async newWorld(seedText: string, width: number, height: number, onProgress?: (label: string, p: number) => void) {
223	    this.world = await generateWorld({ width, height, seedText }, (label, p) => onProgress?.(label, p * 0.7));
224	    // 水体预沉降：创建世界时全图激活+步进至稳定，带进度条
225	    onProgress?.('水体沉降', 0.72);
226	    await this.settleLiquids((p) => onProgress?.('水体沉降', 0.72 + p * 0.27));
227	    onProgress?.('完成', 1);
228	    this.afterWorldLoad();
229	    this.cb.onWorldReady();
230	  }
231	
232	  /** 全图液体沉降：原版 WorldFile.cs:365-389 读档时序 1:1 移植。
233	   *  QuickWater 自底向上直接搬运 → WaterCheck 重建活动列表 →
234	   *  quickSettle 循环 UpdateLiquid 至收敛 → 复位后再次 WaterCheck。
235	   *  收敛后世界液体即达最终静止状态，进游戏不再有"靠近才流动" */
236	  private async settleLiquids(onProgress?: (p: number) => void) {
237	    const sim = new LiquidSim(this.world);
238	    onProgress?.(0.05);
239	    sim.quickWater();
240	    onProgress?.(0.35);
241	    await new Promise((r) => setTimeout(r, 0));
242	    sim.waterCheck();
243	    sim.quickSettle = true;
244	    const MAX_ITER = 100000; // 原版 WorldFile 同上限
245	    let iter = 0;
246	    while (sim.numLiquid > 0 && iter < MAX_ITER) {
247	      sim.updateLiquid();
248	      iter++;
249	      if (iter % 500 === 0) {
250	        onProgress?.(0.35 + Math.min(0.6, iter / 20000));
251	        await new Promise((r) => setTimeout(r, 0));
252	      }
253	    }
254	    sim.quickSettle = false;
255	    sim.waterCheck();
256	    sim.dispose(); // 丢弃临时模拟器（注销监听，避免泄漏到运行期）
257	    onProgress?.(1);
258	  }
259	
260	  async loadWorld(world: World, onProgress?: (label: string, p: number) => void) {
261	    this.world = world;
262	    onProgress?.('水体沉降', 0.5);
263	    await this.settleLiquids((p) => onProgress?.('水体沉降', p));
264	    this.afterWorldLoad();
265	    this.cb.onWorldReady();
266	  }
267	
268	  private afterWorldLoad() {
269	    const w = this.world;
270	    // 原版墙渲染器（TEdit WallFraming 移植；墙 id 直用 wld id，贴图 Wall_N.png）
271	    const wallTiler = this.atlas ? new VanillaWallTiler(this.atlas) : null;
272	    this.chunks = new ChunkCache(w, this.assets.tileSheets, this.autotiler, wallTiler);
273	    this.lighting = new LightingEngine(w);
274	    this.liquid = new LiquidSim(w);
275	    this.liquid.waterCheck(); // 原版读档末尾的 WaterCheck：把沉降后仍可流动的少量格子交给运行时收敛
276	    this.camera = new Camera(w.w, w.h);
277	    this.renderer.minimap = new Minimap(w);
278	    this.entities.clear();
279	    this.player = new Player(w.spawnX * TILE + 8, (w.spawnY - 3) * TILE, new Inventory()); // 主角 3 格高，抬高出生点
280	    // 初始装备（铁器三件套与 Maples 素材对齐；含药水与配饰便于体验 Buff/配饰系统）
281	    this.player.inv.add(ITEM_BY_KEY['iron_pickaxe'], 1);
282	    this.player.inv.add(ITEM_BY_KEY['iron_axe'], 1);
283	    this.player.inv.add(ITEM_BY_KEY['iron_sword'], 1);
284	    this.player.inv.add(ITEM_BY_KEY['torch'], 12);
285	    // 药水/召唤物放入背包格（10 起），不占快捷栏
286	    const bag: Array<[string, number]> = [
287	      ['heal_potion', 2], ['agility_potion', 2], ['ironskin_potion', 2],
288	      ['thorns_potion', 2], ['regen_potion', 2], ['suspicious_eye', 3], ['lens', 6],
289	    ];
290	    let bi = 10;
291	    for (const [key, n] of bag) {
292	      this.player.inv.slots[bi++] = { id: ITEM_BY_KEY[key], stack: n };
293	    }
294	    // 开局体验盔甲：铁三件套穿上
295	    this.player.inv.slots[ARMOR_START] = { id: ITEM_BY_KEY['iron_helmet'], stack: 1 };
296	    this.player.inv.slots[ARMOR_START + 1] = { id: ITEM_BY_KEY['iron_chainmail'], stack: 1 };
297	    this.player.inv.slots[ARMOR_START + 2] = { id: ITEM_BY_KEY['iron_greaves'], stack: 1 };
298	    // 配饰直接放入配饰栏（槽 40-44）
299	    this.player.inv.slots[ACCESSORY_START] = { id: ITEM_BY_KEY['lucky_horseshoe'], stack: 1 };
300	    this.player.inv.slots[ACCESSORY_START + 1] = { id: ITEM_BY_KEY['feral_claws'], stack: 1 };
301	    this.camera.x = this.player.cx;
302	    this.camera.y = this.player.cy;
303	    this.boss = null;
304	    this.guideSpawned = true; // 向导已移除；保留字段避免存档兼容问题
305	    // 商人 NPC(原版 Merchant 语义简化:出生点旁常驻,对话=购买)
306	    const merch = new TownNPC('merchant', this.world.spawnX * 16 - 40, (this.world.spawnY - 2) * 16);
307	    this.entities.add(merch, 'npcs');
308	    // 护士(原版:击败任一 Boss 后入住;checkNpcArrival 每帧判定)
309	    const nurse = new TownNPC('nurse', this.world.spawnX * 16 + 40, (this.world.spawnY - 2) * 16);
310	    this.entities.add(nurse, 'npcs');
311	    this.cb.onInventoryChanged();
312	  }
313	
314	  /** 销毁：停止循环并移除画布（退出到主菜单时调用） */
315	  destroy() {
316	    this.running = false;
317	    this.renderer.canvas.remove();
318	  }
319	
320	  start() {
321	    if (this.running) return;
322	    this.running = true;
323	    this.lastTime = performance.now();
324	    const loop = (now: number) => {
325	      if (!this.running) return;
326	      this.frame(now);
327	      requestAnimationFrame(loop);
328	    };
329	    requestAnimationFrame(loop);
330	  }
331	
332	  private frame(now: number) {
333	    const elapsed = Math.min((now - this.lastTime) / 1000, 0.25);
334	    this.lastTime = now;
335	    if (!this.paused) {
336	      this.acc += elapsed;
337	      let steps = 0;
338	      while (this.acc >= FIXED_DT && steps < 5) {
339	        this.fixedUpdate(FIXED_DT);
340	        this.acc -= FIXED_DT;
341	        steps++;
342	      }
343	    }
344	    this.render();
345	  }
346	
347	  // ================= 固定步逻辑 =================
348	
349	  private fixedUpdate(dt: number) {
350	    this.tickCount++;
351	    // 原版 HitTile 衰减（每 2 tick 一次——原版按帧衰减配原版 ~27 帧挥速；
352	    // 我们的挥击间隔更长，等比减半保持"连击可积累、停手会消退"）
353	    if (this.tickCount % 2 === 0) this.hitTiles.update();
354	    const w = this.world;
355	    w.clock.tick(dt * 1000);
356	    // 昼夜切换：提示 + BGM 变奏
357	    const isDay = w.clock.isDay;
358	    if (isDay !== this.lastWasDay) {
359	      if (this.lastWasDay !== null) {
360	        this.cb.onToast(isDay ? '☀ 太阳升起来了，新的一天开始了' : '🌙 夜幕降临，小心出没的怪物…');
361	        this.cb.onDayNight?.(isDay);
362	      }
363	      this.lastWasDay = isDay;
364	    }
365	    const player = this.player;
366	
367	    // ---- 玩家输入 ----
368	    const inp = this.input;
369	    // 点击右上角小地图 → 开关全屏地图
370	    if (inp.mouseDown && !this._mapClickLatch) {
371	      const r = this.renderer.minimapRect;
372	      const fm = this.renderer.fullMap;
373	      const inMap = inp.mouseX >= r.x && inp.mouseX <= r.x + r.w && inp.mouseY >= r.y && inp.mouseY <= r.y + r.h;
374	      if (!fm.open && inMap && !inp.uiBlocking) {
375	        fm.open = true;
376	        // 打开即放大到主角：锚点 = 主角 tile 坐标 → 屏幕中心，
377	        // zoom 从 0.5 缓动到 2，缓动期间 applyMapAnchor 每帧补偿 pan，主角始终居中
378	        fm.zoom = 0.5;
379	        fm.zoomTarget = 2;
380	        fm.anchorU = player.cx / TILE;
381	        fm.anchorV = player.cy / TILE;
382	        fm.anchorMX = this.renderer.canvas.width / 2;
383	        fm.anchorMY = this.renderer.canvas.height / 2;
384	        // 预置 pan（此时 _fmWorldW 可能还是 0，不能等 easeFullMap 反解，首帧会跳）
385	        fm.panX = (this.world.w * fm.zoom) / 2 - fm.anchorU * fm.zoom;
386	        fm.panY = (this.world.h * fm.zoom) / 2 - fm.anchorV * fm.zoom;
387	        this.renderer['_mapInit'] = false;
388	        // 打开地图的这次点击不算拖拽（否则按住期间 drawFullMap 会把锚点重设到点击处，飞向主角变飞向点击处）
389	        this.renderer['_mapOpenClick'] = true;
390	        this._mapClickLatch = true;
391	      }
392	    }
393	    if (!inp.mouseDown) this._mapClickLatch = false;
394	    // 全屏地图：点击传送（两次确认）——第一次预选标记，第二次传送。
395	    // 按下只记起点，松开时位移 < 6px 才算"点击"（拖动平移、打开地图的按压都不误触传送）
396	    if (this.renderer.fullMap.open && !inp.uiBlocking) {
397	      if (inp.mouseDown && !this._mapClickLatch2 && !this._mapClickLatch && !this.renderer['_mapOpenClick']) {
398	        this._mapClickLatch2 = true;
399	        this._mapPressX = inp.mouseX;
400	        this._mapPressY = inp.mouseY;
401	      }
402	      if (!inp.mouseDown && this._mapClickLatch2) {
403	        this._mapClickLatch2 = false;
404	        const moved = Math.hypot(inp.mouseX - this._mapPressX, inp.mouseY - this._mapPressY);
405	        if (moved < 6) {
406	          const fm = this.renderer.fullMap;
407	          // 屏幕坐标 → 地图源坐标（与 zoomFullMapAt 的逆变换一致）
408	          const viewW = this.renderer.canvas.width, viewH = this.renderer.canvas.height;
409	          const cx0 = viewW / 2 - (this.world.w * fm.zoom) / 2 + fm.panX;
410	          const cy0 = viewH / 2 - (this.world.h * fm.zoom) / 2 + fm.panY;
411	          // 地图绘制：mapW = world.w * zoom（1 tile = zoom 像素）——直接除 zoom 得 tile 坐标
412	          const tx = Math.floor((inp.mouseX - cx0) / fm.zoom);
413	          const ty = Math.floor((inp.mouseY - cy0) / fm.zoom);
414	          if (tx >= 0 && ty >= 0 && tx < this.world.w && ty < this.world.h) {
415	            if (this._tpTarget && this._tpTarget.x === tx && this._tpTarget.y === ty) {
416	              // 第二次点击同一点 → 传送；失败不关图、保留标记可重试
417	              if (this.teleportNear(tx, ty)) {
418	                this._tpTarget = null;
419	                this.renderer.tpMark = null;
420	                this.renderer.fullMap.open = false;
421	                this.cb.onToast('传送完成');
422	              }
423	            } else {
424	              this._tpTarget = { x: tx, y: ty };
425	              this.renderer.tpMark = { x: tx, y: ty };
426	              this.cb.onToast(`已选传送点 (${tx}, ${ty})，再次点击确认`);
427	            }
428	          }
429	        }
430	      }
431	    } else {
432	      this._mapClickLatch2 = false;
433	    }
434	    // ---- 标注模式：点击标记方块（优先于挖掘/放置/使用） ----
435	    if (this.annotateMode && inp.mouseDown && !this._annoLatch && !inp.uiBlocking && !this.renderer.fullMap.open) {
436	      this._annoLatch = true;
437	      const [tx, ty] = this.camera.tileUnder(inp.mouseX, inp.mouseY);
438	      if (this.fixTexMode) {
439	        // 贴图纠错子模式：点击弹出该图块的完整原版贴图表
440	        if (this.world.store.inBounds(tx, ty)) {
441	          (window as unknown as { __swUI?: { openTexPicker?: (x: number, y: number) => void } }).__swUI?.openTexPicker?.(tx, ty);
442	        }
443	      } else if (this.world.store.inBounds(tx, ty)) {
444	        const existed = this.marks.some((m) => m.x === tx && m.y === ty);
445	        this.marks = this.marks.filter((m) => m.x !== tx || m.y !== ty); // 同格重复点 = 取消
446	        if (!existed) this.marks.push({ x: tx, y: ty });
447	        this.cb.onToast(existed ? `已取消标记 (${tx}, ${ty})` : `已标记 (${tx}, ${ty})，再次点击取消`);
448	        (window as unknown as { __swUI?: { updateAnnotateCount: (n: number) => void } }).__swUI?.updateAnnotateCount(this.marks.length);
449	      }
450	    }
451	    if (!inp.mouseDown) this._annoLatch = false;
452	    player.inputX = (inp.down('KeyA') || inp.down('ArrowLeft') ? -1 : 0) + (inp.down('KeyD') || inp.down('ArrowRight') ? 1 : 0);
453	    player.inputJump = inp.down('Space') || inp.down('KeyW') || inp.down('ArrowUp');
454	    player.inputDown = inp.down('KeyS') || inp.down('ArrowDown');
455	    player.inputUp = inp.down('KeyW') || inp.down('ArrowUp');
456	
457	    // 滚轮：全屏地图打开时缩放地图，否则缩放游戏画面
458	    if (inp.wheelDelta !== 0) {
459	      if (this.renderer.fullMap.open) {
460	        // 以鼠标为锚点缩放（缩放不乱飞）
461	        this.renderer.zoomFullMapAt(
462	          this.renderer.fullMap.zoom * (inp.wheelDelta > 0 ? 0.85 : 1.18),
463	          inp.mouseX, inp.mouseY,
464	        );
465	      } else {
466	        this.setZoom(this.camera.zoomTarget * (inp.wheelDelta > 0 ? 0.94 : 1.064));
467	      }
468	    }
469	
470	    player.fixedUpdate(dt, this);
471	    if (player.dead) {
472	      // 死亡瞬间：红色粉碎粒子 + 原地留墓碑（只处理一次）
473	      if (!this._deathHandled) {
474	        this._deathHandled = true;
475	        this.handlePlayerDeath();
476	      }
477	      // 重生计时
478	      player.respawnTimer++;
479	      if (player.respawnTimer > 180) this.respawnPlayer();
480	    } else {
481	      this._deathHandled = false;
482	    }
483	
484	    // ---- 使用物品（鼠标） ----
485	    this.updateUse(dt);
486	
487	    // ---- 实体 ----
488	    this.entities.update(dt, this);
489	
490	    // ---- 液体（原版每 2 tick 一次 UpdateLiquid）----
491	    if (this.tickCount % 2 === 0) {
492	      this.liquid.step();
493	      // 液体直接写数组绕过 store 监听：有活动液体时手动通知光照衰减变化
494	      if (this.liquid.numLiquid > 0) this.lighting.liquidDirty = true;
495	    }
496	
497	    // ---- 敌人生成（F8 可关闭） ----
498	    this.spawnTimer++;
499	    // 水蜡烛(Main.waterCandle 语义):手持或 32 格内有放置态 → 刷怪率 ×2(间隔减半)
500	    const held2 = this.player.inv.heldItem();
501	    const heldWC = !!held2 && ITEM_DEFS[held2.id]?.key === 'water_candle';
502	    this.heldWaterCandle = heldWC;
503	    let nearWC = false;
504	    if (this.tickCount % 30 === 0) {
505	      nearWC = false;
506	      const st2 = this.world.store;
507	      const ptx = Math.floor(this.player.cx / TILE), pty = Math.floor(this.player.cy / TILE);
508	      const WCT = TILE_BY_KEY['water_candle'];
509	      for (let dx = -32; dx <= 32 && !nearWC; dx += 4) {
510	        for (let dy = -24; dy <= 24; dy += 4) {
511	          if (st2.get(ptx + dx, pty + dy) === WCT) { nearWC = true; break; }
512	        }
513	      }
514	      this.waterCandleNear = nearWC;
515	    }
516	    // 篝火/心灯光环:篝火 lifeRegen+1 = 0.5 HP/s;心灯(灯笼 tile42 frameY 324-358,
517	    // SceneMetrics.cs:207-208)lifeRegen+2 = 1 HP/s,两者独立
518	    if (this.tickCount % 20 === 0) {
519	      const ptx2 = Math.floor(this.player.cx / TILE), pty2 = Math.floor(this.player.cy / TILE);
520	      let fire = false, heart = false;
521	      const FIRE = TILE_BY_KEY['v_215_campfires'];
522	      const LANTERN = TILE_BY_KEY['lantern'];
523	      const st3 = this.world.store;
524	      for (let dx = -48; dx <= 48 && !(fire && heart); dx += 3) {
525	        for (let dy = -36; dy <= 36; dy += 3) {
526	          const lx = ptx2 + dx, ly = pty2 + dy;
527	          if (!st3.inBounds(lx, ly)) continue;
528	          const li = st3.idx(lx, ly);
529	          if (st3.type[li] === FIRE && st3.frameX[li] < 18) fire = true;
530	          if (st3.type[li] === LANTERN && st3.frameY[li] >= 324 && st3.frameY[li] <= 358) heart = true;
531	          if (fire && heart) break;
532	        }
533	      }
534	      if (fire) this.player.buffs.apply(BuffType.Campfire, 0.5);
535	      this.player.buffs.lanternHeal = heart ? 1 : 0;
536	    }
537	    const wcBoost = heldWC || this.waterCandleNear;
538	    // 原版 spawnRate×0.75(≈间隔×4/3)
539	    const interval = wcBoost ? Math.ceil(SPAWN_CHECK_INTERVAL / 0.75) : SPAWN_CHECK_INTERVAL;
540	    if (this.enemySpawnEnabled && this.spawnTimer >= interval) {
541	      this.spawnTimer = 0;
542	      this.trySpawnEnemy();
543	    }
544	
545	    // ---- 压力板触发 ----
546	    this.checkPressurePlates();
547	
548	    // ---- Boss 逻辑 ----
549	    if (this.boss) {
550	      if (this.boss.dead || w.clock.isDay) {
551	        if (this.boss.dead && !w.flags.downedEyeOfCthulhu) {
552	          w.flags.downedEyeOfCthulhu = true;
553	          this.cb.onToast('克苏鲁之眼已被击败！');
554	        }
555	        if (w.clock.isDay && !this.boss.dead) {
556	          this.boss.dead = true;
557	          this.cb.onToast('克苏鲁之眼在黎明逃走了…');
558	        }
559	        this.boss = null;
560	      }
561	    }
562	
563	    // ---- 树苗生长（每 5 秒扫一次） ----
564	    if (this.tickCount % 300 === 0) this.growSaplings();
565	
566	    // ---- 战争迷雾：玩家周围探索标记（每 15 tick） ----
567	    if (this.tickCount % 15 === 0) {
568	      w.markExplored(Math.floor(player.cx / TILE), Math.floor(player.cy / TILE), 28);
569	    }
570	
571	    // ---- Buff 状态栏刷新（每秒） ----
572	    if (this.tickCount % 60 === 0) this.cb.onBuffsChanged?.();
573	
574	    // ---- 相机 / 光照 ----
575	    this.camera.follow(player.cx, player.cy);
576	    this.camera.easeZoom();
577	    this.camera.clamp();
578	    this.chunks.flushDirty();
579	    const viewTW = Math.ceil(this.camera.viewW / this.camera.zoom / TILE) + 2;
580	    const viewTH = Math.ceil(this.camera.viewH / this.camera.zoom / TILE) + 2;
581	    this.lighting.ensureRegion(player.cx, player.cy, viewTW, viewTH);
582	    // 手持火把照明：选中火把即点亮周围（#11）
583	    const heldDef = player.inv.heldDef();
584	    const torchOn = !!heldDef && heldDef.key === 'torch';
585	    const ptx = Math.floor(player.cx / TILE), pty = Math.floor(player.cy / TILE);
586	    const prevLight = this.lighting.heldLight;
587	    this.lighting.heldLight = torchOn ? { tx: ptx, ty: pty } : null;
588	    if (torchOn !== !!prevLight ||
589	      (torchOn && prevLight && (prevLight.tx !== ptx || prevLight.ty !== pty))) {
590	      this.lighting.dirty = true;
591	    }
592	    this.lighting.compute(w.clock.dayFactor);
593	
594	    // ---- 粒子与飘字 ----
595	    this.flushInvNotify();
596	    // 小动物环境生成：按昼夜在地表视野外生成，上限 8 只
597	    if (this.tickCount % 120 === 0 && this.entities.critters.length < 8) {
598	      this.spawnCritter();
599	    }
600	    // 怪物碾压小动物：任意敌人身体接触即杀死（不视为交战）
601	    if (this.tickCount % 4 === 0 && this.entities.critters.length) {
602	      for (const cent of this.entities.critters) {
603	        const c = cent as Critter;
604	        if (c.dead) continue;
605	        for (const eent of this.entities.enemies) {
606	          const e = eent as Enemy;
607	          if (c.x < e.x + e.w && c.x + c.w > e.x && c.y < e.y + e.h && c.y + c.h > e.y) {
608	            c.hurt(this);
609	            break;
610	          }
611	        }
612	      }
613	    }
614	    // 僵尸环境呻吟：附近有僵尸时偶发（每 ~4-8 秒）
615	    if (this.tickCount % 300 === 0) {
616	      for (const ent of this.entities.enemies) {
617	        const e = ent as Enemy;
618	        if (e.key !== 'zombie' && e.key !== 'magma_zombie') continue;
619	        if (Math.hypot(e.cx - this.player.cx, e.cy - this.player.cy) < TILE * 30) {
620	          this.sfx.playWav('zombie', 0.6);
621	          break;
622	        }
623	      }
624	    }
625	    // 火把火苗：视内点燃火把随机飘出火星（火点在格顶上方 20px 精灵的火焰处）
626	    this.emitTorchSparks();
627	    for (const p of this.particles) {
628	      p.life--;
629	      p.vy += p.grav ?? 0.12;
630	      if (p.damp) { p.vx *= p.damp; p.vy *= p.damp; } // 空气阻力：喷溅后缓慢减速飘散
631	      // 地形碰撞：目标位置实心则反弹（冲击大）或停驻地表（冲击小，重力归零缓慢淡出）
632	      const st = this.world.store;
633	      const solidAt = (x: number, y: number) => {
634	        const tx = Math.floor(x / TILE), ty = Math.floor(y / TILE);
635	        return st.inBounds(tx, ty) && st.isSolid(tx, ty);
636	      };
637	      let nx = p.x + p.vx;
638	      if (solidAt(nx, p.y)) { p.vx *= -0.4; nx = p.x; }
639	      let ny = p.y + p.vy;
640	      if (solidAt(nx, ny)) {
641	        if (p.vy > 1.6) {
642	          p.vy = -p.vy * 0.35; // 溅落反弹
643	          p.vx *= 0.6;
644	        } else {
645	          p.vy = 0; p.vx *= 0.5; p.grav = 0; // 停驻地表
646	        }
647	        ny = p.y;
648	      }
649	      p.x = nx; p.y = ny;
650	    }
651	    this.particles = this.particles.filter((p) => p.life > 0);
652	    for (const d of this.dmgNumbers) {
653	      d.life--;
654	      d.y += d.vy;
655	      d.vy *= 0.94;
656	    }
657	    this.dmgNumbers = this.dmgNumbers.filter((d) => d.life > 0);
658	
659	    inp.endFrame();
660	
661	    // 挥剑命中判定（实体更新后）
662	    this.postUpdate();
663	  }
664	
665	  // ================= 物品使用：挖掘 / 放置 / 攻击 / 使用 =================
666	
667	  private updateUse(dt: number) {
668	    const inp = this.input;
669	    // 矿车骑乘驱动:左右加速,跳车
670	    if (this.minecart) {
671	      const cart = this.minecart;
672	      const ix = this.player.inputX;
673	      if (ix !== 0) cart.vx = Math.max(-8, Math.min(8, cart.vx + ix * 0.15));
674	      if (inp.down('KeyR')) {
675	        // 跳车(原版 R 键下车;Space 与跳跃共用会误触)
676	        this.player.x = cart.x;
677	        this.player.y = cart.y - 24;
678	        this.player.vy = -4;
679	        cart.mounted = false;
680	        this.minecart = null;
681	        this.input.rightDown = false;
682	      }
683	      // 玩家跟随车位置
684	      this.player.x = cart.x;
685	      this.player.y = cart.y - 26;
686	      this.player.vx = cart.vx;
687	      this.player.vy = 0;
688	      if (cart.dead) { this.minecart = null; }
689	      return;
690	    }
691	    // 全屏地图打开时鼠标交给地图（拖动/缩放/传送），不触发挖掘/放置/攻击/使用
692	    if (inp.uiBlocking || this.player.dead || this.renderer.fullMap.open) {
693	      this.mining = null;
694	      return;
695	    }
696	    const held = this.player.inv.heldItem();
697	    const heldDef = held ? ITEM_DEFS[held.id] : null;
698	    const [tx, ty] = this.camera.tileUnder(inp.mouseX, inp.mouseY);
699	    const tool = heldDef?.tool;
700	    const vw2 = this.renderer.canvas.width, vh2 = this.renderer.canvas.height;

```


---

## 🤖 Assistant · 2026-08-09T10:48:51.584Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now read the rest of Game.ts — particularly updateUse (tryPlace, canPlace, overlapsEntity, interactAt), the mechanism bits around 1420-1470 (toggleSwitch/fireTrapsFrom/checkPressurePlates), breakTile flow. Let me read 700-1200 and 1200-1700 and the rest.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:48:51.590Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "offset": 700,
 "limit": 560
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:51.603Z

**📎 ToolResult**

```
700	    const vw2 = this.renderer.canvas.width, vh2 = this.renderer.canvas.height;
701	
702	    // 右键：手持矿车点轨道(最优先,防 NPC 交谈拦截)→ 附近宝箱 → NPC 交谈 → 交互
703	    const type = this.world.store.get(tx, ty);
704	    if (inp.rightDown && !this.minecart && type === this.trackTile && this.trackTile !== 0) {
705	      const h = this.player.inv.heldItem();
706	      if (h && ITEM_DEFS[h.id]?.key === 'minecart_item') {
707	        const cart = new Minecart();
708	        cart.x = tx * TILE; cart.y = (ty - 1) * TILE;
709	        this.entities.add(cart, 'props');
710	        this.minecart = cart;
711	        cart.mounted = true;
712	        this.player.inv.removeAt(this.player.inv.selected, 1);
713	        this.cb.onInventoryChanged();
714	        this.input.rightDown = false;
715	        return;
716	      }
717	    }
718	    if (inp.rightDown) {
719	      const nearChest = this.findChestNear(tx, ty);
720	      if (nearChest) {
721	        this.tryOpenChest(nearChest);
722	        this.input.rightDown = false;
723	      } else if (this.talkToNearbyNpc(tx, ty)) {
724	        this.input.rightDown = false;
725	      } else if (heldDef?.key === 'suspicious_eye') {
726	        if (!this.world.clock.isDay) {
727	          this.useSuspiciousEye();
728	          this.player.inv.removeAt(this.player.inv.selected, 1);
729	          this.cb.onInventoryChanged();
730	        } else {
731	          this.cb.onToast('什么都没有发生...');
732	        }
733	        this.input.rightDown = false;
734	      } else {
735	        this.interactAt(tx, ty);
736	      }
737	    }
738	
739	    if (!inp.mouseDown || this.annotateMode) {
740	      this.mining = null;
741	      return;
742	    }
743	
744	    // 近战挥剑（攻速配饰：猛爪手套 ×2）
745	    if (tool?.type === 'sword') {
746	      const spd = Math.max(12, Math.round((tool.speed ?? 42) / this.player.attackSpeedMult));
747	      if (!this.swing && this.player.useTime === 0) {
748	        this.swing = { t: spd, dur: spd, item: held!.id };
749	        this.player.useTime = spd;
750	        this.swingHitSet.clear();
751	      }
752	      this.mining = null;
753	      return;
754	    }
755	
756	    // 镐/斧/锤：挖掘（按住累计）+ 同时作为武器挥击（伤害低于剑）
757	    if (tool && (tool.type === 'pick' || tool.type === 'axe' || tool.type === 'hammer')) {
758	      const spd = Math.max(14, Math.round((tool.speed ?? 46) / this.player.attackSpeedMult));
759	      if (!this.swing && this.player.useTime === 0) {
760	        this.swing = { t: spd, dur: spd, item: held!.id };
761	        this.player.useTime = spd;
762	        this.swingHitSet.clear();
763	        // 每次挥砍一声：斧砍植物纤维、镐按材质区分土闷/石金（跟随挥砍节奏，不再密集连响）。
764	        // 没有生效对象（镐没对准可挖方块 / 斧没对准树）则不出声
765	        const hType = this.world.store.get(tx, ty);
766	        const hovered = TILE_DEFS[hType];
767	        const axeOnTarget = hType === T.TREE || (hovered?.decor ?? false);
768	        const pickOnTarget = hType !== 0 && this.toolCanBreak(hType, tool.power ?? 10, tool.type);
769	        if (tool.type === 'axe' ? axeOnTarget : pickOnTarget) {
770	          if (tool.type === 'axe') this.sfx.play('chop');
771	          else if (hovered && /stone|ore|brick|obsidian|ash|gem_|fossil|silt/i.test(hovered.key)) this.sfx.play('tink');
772	          else this.sfx.play('dig');
773	        }
774	      }
775	      // HitTile 节流窗 = 实际挥击间隔（含攻速配饰加成），保证一挥一击
776	      this.tryMine(tx, ty, tool.power ?? 10, tool.type, spd);
777	      return;
778	    }
779	
780	    // 可放置物品：左键放置
781	    if (heldDef?.tile && !inp.rightDown) {
782	      this.tryPlace(tx, ty, heldDef);
783	      return;
784	    }
785	
786	    // 其它物品（方块/药水等）：左键使用并带挥砍动画
787	    if (heldDef && inp.mouseDown && this.player.useTime === 0 && !heldDef.tool) {
788	      const spd = 30;
789	      this.swing = { t: spd, dur: spd, item: held!.id };
790	      this.swingHitSet.clear();
791	      // 召唤道具（原版左键使用）
792	      if (heldDef.key === 'suspicious_eye') {
793	        if (!this.world.clock.isDay) {
794	          this.useSuspiciousEye();
795	          this.player.inv.removeAt(this.player.inv.selected, 1);
796	          this.cb.onInventoryChanged();
797	        } else {
798	          this.cb.onToast('什么都没有发生...');
799	        }
800	        this.player.useTime = 30;
801	      }
802	    }
803	    // 药水饮用（移植自 Maples：点击饮用，治疗类受耐药性封锁）
804	    if (heldDef?.potion && inp.mouseDown && this.player.useTime === 0) {
805	      const p = heldDef.potion;
806	      const buffTypeMap: Record<string, BuffType> = {
807	        agility: BuffType.Agility, ironskin: BuffType.Ironskin,
808	        resistance: BuffType.Resistance, thorns: BuffType.Thorns, regen: BuffType.Regen,
809	      };
810	      if (p.isHealType && this.player.buffs.healBlocked) {
811	        this.cb.onToast('耐药性生效中，无法饮用治疗药水');
812	        this.player.useTime = 30;
813	      } else {
814	        const bt = buffTypeMap[p.buff];
815	        this.player.buffs.apply(bt, p.duration);
816	        if (heldDef.heal) {
817	          this.player.hp = Math.min(this.player.maxHp, this.player.hp + heldDef.heal);
818	          this.addDamageNumber(this.player.cx, this.player.y, heldDef.heal, false, '#40E080');
819	        }
820	        this.player.inv.removeAt(this.player.inv.selected, 1);
821	        this.player.useTime = 60;
822	        this.sfx.play('drink');
823	        this.cb.onInventoryChanged();
824	        this.cb.onToast(`${heldDef.name}：${p.duration} 秒`);
825	      }
826	    } else if (heldDef && (heldDef.key === 'life_crystal' || heldDef.key === 'vi_29_LifeCrystal')) {
827	      // 物品态生命水晶(Player.cs:29358:item 29,statLifeMax<400 → +20)
828	      if (this.player.baseMaxHp >= 400) {
829	        this.cb.onToast('生命上限已达到 400');
830	      } else {
831	        this.player.baseMaxHp += 20;
832	        this.player.hp = Math.min(this.player.maxHp, this.player.hp + 20);
833	        this.addDamageNumber(this.player.cx, this.player.y, 20, false, '#40E080');
834	        this.player.inv.removeAt(this.player.inv.selected, 1);
835	        this.player.useTime = 30;
836	        this.sfx.play('drink');
837	        this.cb.onInventoryChanged();
838	      }
839	      this.player.useTime = Math.max(this.player.useTime, 30);
840	    } else if (heldDef?.ranged && inp.mouseDown && this.player.useTime === 0) {
841	      // 远程武器(弓):消耗弹药 → 沿鼠标方向发射箭(Player.ItemCheck_Shoot 语义)
842	      const rg = heldDef.ranged;
843	      const ammoId = ITEM_BY_KEY[rg.ammo];
844	      let ammoSlot = -1;
845	      for (let i = 0; i < this.player.inv.slots.length; i++) {
846	        const sl = this.player.inv.slots[i];
847	        if (sl && sl.id === ammoId && sl.stack > 0) { ammoSlot = i; break; }
848	      }
849	      if (ammoSlot >= 0) {
850	        const ang = Math.atan2(inp.mouseY - this.renderer.canvas.height / 2, inp.mouseX - this.renderer.canvas.width / 2);
851	        const ax = this.player.cx + Math.cos(ang) * 14;
852	        const ay = this.player.cy - 4 + Math.sin(ang) * 14;
853	        const arrow = new Arrow(ax, ay, Math.cos(ang) * rg.projSpeed, Math.sin(ang) * rg.projSpeed, rg.damage, rg.ammo);
854	        this.entities.add(arrow, 'projectiles');
855	        this.player.inv.removeAt(ammoSlot, 1);
856	        this.player.useTime = rg.speed;
857	        this.sfx.play('tink');
858	        this.cb.onInventoryChanged();
859	      }
860	    } else if (heldDef && (heldDef.key === 'worm_food' || heldDef.key === 'bloody_spine' || heldDef.key === 'slime_crown')
861	      && inp.mouseDown && this.player.useTime === 0) {
862	      // Boss 召唤物(原版 worm food/bloody spine/slime crown)
863	      if (heldDef.key === 'worm_food') this.summonBoss('eater_of_worlds_head');
864	      else if (heldDef.key === 'bloody_spine') this.summonBoss('brain_of_cthulhu');
865	      else this.summonBoss('king_slime');
866	      this.player.inv.removeAt(this.player.inv.selected, 1);
867	      this.player.useTime = 60;
868	      this.cb.onInventoryChanged();
869	      this.input.mouseDown = false;
870	    } else if (heldDef?.magic && inp.mouseDown && this.player.useTime === 0) {
871	      // 魔法武器:消耗 mana → 发射魔法弹(Player.ItemCheck_Shoot 语义)
872	      const mg = heldDef.magic;
873	      if (this.player.mana < mg.manaCost) {
874	        this.cb.onToast('魔力不足');
875	        this.input.mouseDown = false;
876	      } else {
877	        this.player.mana -= mg.manaCost;
878	        const ang = Math.atan2(inp.mouseY - vh2 / 2, inp.mouseX - vw2 / 2);
879	        const mx = this.player.cx + Math.cos(ang) * 14;
880	        const my = this.player.cy - 4 + Math.sin(ang) * 14;
881	        const color = mg.proj === 'bolt' ? '#A040FF' : '#FFB040';
882	        const proj = new MagicProj(mx, my, Math.cos(ang) * mg.projSpeed, Math.sin(ang) * mg.projSpeed, mg.damage, 45, color);
883	        this.entities.add(proj, 'projectiles');
884	        this.player.useTime = mg.speed;
885	        this.sfx.play('tink');
886	        this.input.mouseDown = false;
887	      }
888	    } else if (heldDef && (heldDef.key === 'empty_bucket' || heldDef.key === 'water_bucket'
889	      || heldDef.key === 'lava_bucket' || heldDef.key === 'honey_bucket')) {
890	      this.useBucket(heldDef.key, tx, ty);
891	    }
892	    this.mining = null;
893	  }
894	
895	  private toolCanBreak(type: number, power: number, toolType: string): boolean {
896	    const d = TILE_DEFS[type];
897	    if (!d) return false;
898	    if (toolType === 'pick') return d.pick >= 0 && power >= d.pick;
899	    if (toolType === 'axe') return d.axe >= 0;
900	    return false;
901	  }
902	
903	  private tryMine(tx: number, ty: number, power: number, toolType: 'pick' | 'axe' | 'hammer', speed: number) {
904	    // 范围检查
905	    const dx = tx - Math.floor(this.player.cx / TILE);
906	    const dy = ty - Math.floor(this.player.cy / TILE);
907	    if (Math.hypot(dx, dy) > 4.5) { this.mining = null; return; }
908	    const type = this.world.store.get(tx, ty);
909	    // 锤：敲除背景墙（无墙则无事发生；也可清装饰）
910	    if (toolType === 'hammer') {
911	      // 原版语义:锤子优先循环实心块状态(整块→半砖→整块;坡面渲染未实现暂两态)
912	      if (type !== 0 && this.world.store.isSolid(tx, ty) && this.tickCount - this.lastMineHitTick >= Math.max(8, speed)) {
913	        this.lastMineHitTick = this.tickCount;
914	        const i = this.world.store.idx(tx, ty);
915	        const cur = this.world.store.half[i];
916	        this.world.store.setHalfBrick(tx, ty, !cur);
917	        this.sfx.play('tink');
918	        this.mining = null;
919	        return;
920	      }
921	      const wall = this.world.store.get(tx, ty) === 0 ? this.world.store.wall[this.world.store.idx(tx, ty)] : 0;
922	      if (type !== 0 && TILE_DEFS[type]?.decor) {
923	        this.breakTile(tx, ty);
924	        this.sfx.play('chop');
925	        this.mining = null;
926	        return;
927	      }
928	      if (!wall) { this.mining = null; return; }
929	      // HitTile 制（type 2 = 墙）：每挥一击，阈值 100
930	      if (this.tickCount - this.lastMineHitTick < Math.max(8, speed)) {
931	        this.hardnessCache = 100;
932	        this.mining = { x: tx, y: ty, progress: this.hitTiles.getDamage(tx, ty, 2) };
933	        return;
934	      }
935	      this.lastMineHitTick = this.tickCount;
936	      const total = this.hitTiles.addDamage(tx, ty, Math.round(power * 2), 2); // 锤墙：木 5 击 / 铜 2 击
937	      this.hardnessCache = 100;
938	      this.mining = { x: tx, y: ty, progress: total };
939	      this.spawnParticles(tx * TILE + 8, ty * TILE + 8, '#5C4436', 2, 1.2);
940	      if (total >= 100) {
941	        this.hitTiles.clear(tx, ty, 2);
942	        this.world.store.setWall(tx, ty, 0);
943	        this.spawnParticles(tx * TILE + 8, ty * TILE + 8, '#5C4436', 8, 1.8);
944	        this.sfx.play('chop');
945	        this.mining = null;
946	      }
947	      return;
948	    }
949	    if (type === 0 || !this.toolCanBreak(type, power, toolType)) {
950	      // 装饰物（杂草等）任意工具/武器一下清掉并掉落
951	      if (type !== 0 && TILE_DEFS[type]?.decor && (toolType === 'pick' || toolType === 'axe')) {
952	        this.breakTile(tx, ty);
953	        this.sfx.play('chop');
954	        this.mining = null;
955	        return;
956	      }
957	      this.mining = null;
958	      return;
959	    }
960	    // ---- 原版 HitTile 制（Player.PickTile 移植）：每挥一击积累伤害，阈值 100 破坏 ----
961	    // 每挥一击（按工具速度节流），伤害 = 工具力 × 材质系数（GetPickaxeDamage 简化）
962	    if (this.tickCount - this.lastMineHitTick < Math.max(8, speed)) {
963	      // 节流窗内：只刷新裂缝显示，不积累
964	      this.hardnessCache = 100;
965	      this.mining = { x: tx, y: ty, progress: this.hitTiles.getDamage(tx, ty) };
966	      return;
967	    }
968	    this.lastMineHitTick = this.tickCount;
969	    const d = TILE_DEFS[type];
970	    // 原版 GetPickaxeDamage：普通块 = 镐力；泥土族（0/40/53/57/59/123/147/224/397）= 镐力×2。
971	    // 矿石无系数（只靠镐力门槛 gate）；家具软质 ×2 保持原版 tileNoFail 方向。
972	    // 斧 = 斧力×1.2（原版 Player.cs:29576）——绝对值配原版节奏需十击太多，
973	    // 按同比例放大（≈斧力×5.5）适配我们的挥击间隔+衰减：铜斧 7→39（3 击）/ 金斧 11→61（2 击）
974	    let dmg: number;
975	    if (type === T.TREE || IMPORTED_TREE_TYPES.has(type)) {
976	      dmg = toolType === 'axe' ? Math.round(power * 5.5) : power;
977	    } else if (toolType === 'axe') {
978	      dmg = Math.round(power * 5.5);
979	    } else if (d.decor || (d.framed && !d.solid)) {
980	      dmg = power * 2;
981	    } else {
982	      const dirtFamily = /^(dirt|grass|sand|snow|mud|silt|clay|ash|slush|ebonsand|crimsand|pearlsand|hardened_sand)/i.test(d.key)
983	        || d.key === 'v_123_silt' || d.key === 'v_224_slush_block' || d.key === 'v_397_hardened_sand' || d.key === 'v_112_ebonsand_block';
984	      dmg = power * (dirtFamily ? 2 : 1);
985	    }
986	    const total = this.hitTiles.addDamage(tx, ty, dmg);
987	    this.hardnessCache = 100;
988	    this.mining = { x: tx, y: ty, progress: total }; // 裂缝显示 = 积累进度
989	    this.spawnParticles(tx * TILE + 8, ty * TILE + 8, d.mapColor, 2, 1.2);
990	    if (total >= 100) {
991	      this.hitTiles.clear(tx, ty);
992	      this.breakTile(tx, ty);
993	      this.mining = null;
994	      // 破坏完成音：按材质区分
995	      if (toolType === 'axe') this.sfx.play('chop');
996	      else if (/stone|ore|brick|obsidian|ash|gem_|fossil|silt/i.test(d.key)) this.sfx.play('tink');
997	      else this.sfx.play('dig');
998	    }
999	  }
1000	
1001	  private tileHardness(type: number): number {
1002	    const d = TILE_DEFS[type];
1003	    // 铜镐基准（52/tick）：泥土 ~0.25s / 石 ~0.6s / 铜矿 ~0.8s / 金矿 ~1.6s
1004	    // 树（斧）：木斧 ~2s / 铜斧 ~1s / 金斧 ~0.4s
1005	    if (type === T.TREE) return 3400;
1006	    if (type === T.LEAVES) return 40;
1007	    if (d.decor) return 60;
1008	    if (d.framed && !d.solid) return 300;               // 工作台/铁砧等
1009	    switch (type) {
1010	      case T.DIRT: case T.GRASS: case T.SAND: case T.SNOW: return 780;
1011	      case T.STONE: return 1870;
1012	      case T.WOOD: case T.PLATFORM: return 1250;
1013	      case T.ORE_COPPER: return 2500;
1014	      case T.ORE_IRON: return 3100;
1015	      case T.ORE_SILVER: return 4100;
1016	      case T.ORE_GOLD: return 5000;
1017	      default: return 1000;
1018	    }
1019	  }
1020	
1021	  /** 破坏 tile：处理树整体砍伐与 object 锚点 */
1022	  private breakTile(x: number, y: number) {
1023	    const st = this.world.store;
1024	    const type = st.get(x, y);
1025	    if (type === 0) return;
1026	    const def = TILE_DEFS[type];
1027	
1028	    // 树：砍树干 → 整棵树倒下（自有树 + 导入的原版树族）
1029	    if (type === T.TREE) {
1030	      this.fellTree(x, y);
1031	      return;
1032	    }
1033	    // 暗影之球/恶魔之心：整体破碎（原版 WorldGen.CheckOrb 移植）
1034	    if (type === TILE_BY_KEY['v_31_orb_heart']) {
1035	      this.smashOrbHeart(x, y);
1036	      return;
1037	    }
1038	    if (IMPORTED_TREE_TYPES.has(type)) {
1039	      this.fellImportedTree(x, y, type);
1040	      return;
1041	    }
1042	    // 门：竖排帧布局（Door.ts），通用锚点算法不适用，整扇移除
1043	    const doorAnchor = clearDoorAt(st, x, y);
1044	    if (doorAnchor) {
1045	      this.spawnDrop(doorAnchor[0] * TILE + 8, doorAnchor[1] * TILE, def.drop ?? 'door', 1);
1046	      this.spawnParticles(x * TILE + 8, y * TILE + 8, def.mapColor, 8, 1.8);
1047	      return;
1048	    }
1049	    // object：找锚点整体移除
1050	    if ((def.w ?? 1) > 1 || (def.h ?? 1) > 1) {
1051	      const fi = st.idx(x, y);
1052	      const fv = st.frameX[fi], fyv = st.frameY[fi];
1053	      // 原版家具帧是 18px 像素偏移，先归一成格偏移再找锚点
1054	      const gx = def.vanilla ? Math.floor(fv / 18) : fv;
1055	      const gy = def.vanilla ? Math.floor(fyv / 18) : fyv;
1056	      const ax = gx === 0 && gy === 0 ? x : x - gx;
1057	      const ay = gx === 0 && gy === 0 ? y : y - gy;
1058	      for (let dx = 0; dx < (def.w ?? 1); dx++) {
1059	        for (let dy = 0; dy < (def.h ?? 1); dy++) {
1060	          st.setTile(ax + dx, ay + dy, 0);
1061	        }
1062	      }
1063	      this.spawnDrop(ax * TILE + 8, ay * TILE, def.drop ?? (def.key.startsWith('v_') ? 'place_' + def.key : ''), 1);
1064	      // 宝箱内容物掉出
1065	      if (type === T.CHEST) this.dumpChest(ax, ay);
1066	      this.spawnParticles(x * TILE + 8, y * TILE + 8, def.mapColor, 8, 1.8);
1067	      return;
1068	    }
1069	    // 瓦罐：碎裂音 + 随机战利品（火把/炸弹/绳/小血瓶/铜币）
1070	    if (TILE_BY_KEY['pot'] !== undefined && type === TILE_BY_KEY['pot']) {
1071	      st.setTile(x, y, 0);
1072	      this.sfx.play('shatter');
1073	      this.spawnParticles(x * TILE + 8, y * TILE + 8, '#974F50', 10, 2);
1074	      const loot: Array<[string, number, number, number]> = [
1075	        // [itemKey, min, max, 概率]
1076	        ['torch', 3, 8, 0.55],
1077	        ['bomb', 1, 3, 0.22],
1078	        ['rope', 5, 15, 0.20],
1079	        ['lesser_healing_potion', 1, 1, 0.22],
1080	        ['coin_copper', 5, 20, 0.45],
1081	        ['gel', 1, 2, 0.15],
1082	      ];
1083	      for (const [key, mn, mx, ch] of loot) {
1084	        if (Math.random() < ch) {
1085	          this.spawnDrop(x * TILE + 8, y * TILE, key, mn + Math.floor(Math.random() * (mx - mn + 1)),
1086	            (Math.random() - 0.5) * 2.5, -2.5 - Math.random());
1087	        }
1088	      }
1089	      return;
1090	    }
1091	    // 普通
1092	    st.setTile(x, y, 0);
1093	    // 破坏树木正下方的支撑方块 → 整棵树倒下（掉木材）
1094	    const treeOnTop = this.world.trees.find((t) => t.x === x && t.y + t.h === y);
1095	    if (treeOnTop) this.fellTree(x, y - 1);
1096	    if (def.drop) this.spawnDrop(x * TILE + 8, y * TILE + 8, def.drop, 1);
1097	    else if (def.key.startsWith('v_')) this.spawnDrop(x * TILE + 8, y * TILE + 8, 'place_' + def.key, 1);
1098	    this.spawnParticles(x * TILE + 8, y * TILE + 8, def.mapColor, 6, 1.5);
1099	  }
1100	
1101	  private fellTree(x: number, y: number) {
1102	    // 向上找树顶（同列 TREE tile），向下到 Grass
1103	    const st = this.world.store;
1104	    let top = y;
1105	    while (st.get(x, top - 1) === T.TREE) top--;
1106	    let bottom = y;
1107	    while (st.get(x, bottom + 1) === T.TREE) bottom++;
1108	    const height = bottom - top + 1;
1109	    // 树冠 80×80 以树顶为中心外扩 2-3 格：显式区域标脏，
1110	    // 否则不含树干格的邻 chunk 不会重绘 → 树叶残留
1111	    this.chunks.markDirtyArea(x - 4, top - 4, x + 4, bottom + 1);
1112	    // 清除树干 + 两侧树枝（支干只在紧邻树干处生成，不会误伤邻树），并记录枝干位置
1113	    const branchSpots: Array<{ x: number; y: number }> = [];
1114	    for (let yy = top; yy <= bottom; yy++) {
1115	      st.setTile(x, yy, 0);
1116	      for (const s of [-1, 1]) {
1117	        if (st.get(x + s, yy) === T.TREE) {
1118	          branchSpots.push({ x: x + s, y: yy });
1119	          st.setTile(x + s, yy, 0);
1120	        }
1121	      }
1122	    }
1123	    // 清除树冠（树顶周围半径 3 的 LEAVES）
1124	    for (let dx = -3; dx <= 3; dx++) {
1125	      for (let dy = -4; dy <= 1; dy++) {
1126	        if (st.get(x + dx, top + dy) === T.LEAVES) st.setTile(x + dx, top + dy, 0);
1127	      }
1128	    }
1129	    // 掉木材：树干每段 1 个独立掉落物沿干散落；每根枝干也额外掉 1 份（掉在枝干处）
1130	    const wood = Math.max(1, Math.floor(height * 0.8));
1131	    for (let p = 0; p < wood; p++) {
1132	      const dropY = (top + Math.floor((p + 0.5) * height / wood)) * TILE;
1133	      this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, dropY, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
1134	    }
1135	    for (const b of branchSpots) {
1136	      this.spawnDrop(b.x * TILE + 8, b.y * TILE + 8, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
1137	    }
1138	    // 橡实：较大概率（75%）掉 2-3 颗，沿树冠区域散落供补种
1139	    if (Math.random() < 0.75) {
1140	      const nAcorn = 2 + Math.floor(Math.random() * 2);
1141	      for (let a = 0; a < nAcorn; a++) {
1142	        const ax = x + (Math.random() - 0.5) * 2.5;
1143	        const ay = top + Math.random() * height * 0.4;
1144	        this.spawnDrop(ax * TILE + 8, ay * TILE, 'acorn', 1, (Math.random() - 0.5) * 3, -3 - Math.random());
1145	      }
1146	    }
1147	    this.spawnParticles(x * TILE + 8, top * TILE + 8, '#2E8B3D', 14, 2.2);
1148	    // 从登记表移除
1149	    const t = this.world.trees.findIndex((tr) => tr.x === x && Math.abs(tr.y - top) <= 2);
1150	    if (t >= 0) this.world.trees.splice(t, 1);
1151	  }
1152	
1153	  /** 砍导入的原版树（tile 5 / 宝石树 / 装饰树 / 灰烬树）：
1154	   *  同列同类型连续段 = 整棵树（含顶部树冠标记格），整棵移除 + 掉木材。
1155	   *  首击即倒（不做倒树动画——动画实体绑定自有树的登记表结构） */
1156	  /** 暗影之球/恶魔之心整体破碎（原版 WorldGen.CheckOrb 移植，WorldGen.cs:31813-31960）：
1157	   *  帧锚点定位（frameX∈{0,36} 是左列）→ 2×2 四格一起清除；
1158	   *  战利品：首破固定（暗影之球:恶魔之心 + 凝胶100；恶魔之心:生命水晶 + 凝胶100），
1159	   *  之后 5 选 1 随机；无原版物品的部分用现有道具近似 */
1160	  private smashOrbHeart(x: number, y: number) {
1161	    const st = this.world.store;
1162	    const orbId = TILE_BY_KEY['v_31_orb_heart'];
1163	    const i = st.idx(x, y);
1164	    const fx = st.frameX[i];
1165	    const isDemonHeart = fx >= 36; // 原版：frameX ≥ 36 = 恶魔之心（猩红世界）
1166	    const ax = (fx === 0 || fx === 36) ? x : x - 1;
1167	    const ay = st.frameY[i] !== 0 ? y - 1 : y;
1168	    this.chunks.markDirtyArea(ax - 1, ay - 1, ax + 2, ay + 2);
1169	    for (let dx = 0; dx < 2; dx++) {
1170	      for (let dy = 0; dy < 2; dy++) st.setTile(ax + dx, ay + dy, 0);
1171	    }
1172	    // 战利品（近似：首破固定 + 之后随机）
1173	    const drops: Array<[string, number]> = !this.world.flags.shadowOrbSmashed
1174	      ? (isDemonHeart ? [['coin_gold', 1], ['gel', 100]] : [['suspicious_eye', 1], ['gel', 100]])
1175	      : [['coin_silver', 5], ['gel', 60]];
1176	    for (const [key, n] of drops) {
1177	      this.spawnDrop(ax * TILE + 8, ay * TILE + 8, key, n, (Math.random() - 0.5) * 3, -3);
1178	    }
1179	    this.spawnParticles(ax * TILE + 16, ay * TILE + 16, isDemonHeart ? '#FF4060' : '#9A6AE0', 16, 2.5);
1180	    this.sfx.play('tink');
1181	    this.cb.onToast(isDemonHeart ? '恶魔之心被击碎了！' : '暗影之球被击碎了！');
1182	    if (!this.world.flags.shadowOrbSmashed) {
1183	      this.world.flags.shadowOrbSmashed = true;
1184	    }
1185	  }
1186	
1187	  private fellImportedTree(x: number, y: number, type: number) {
1188	    const st = this.world.store;
1189	    let top = y;
1190	    while (st.get(x, top - 1) === type) top--;
1191	    let bottom = y;
1192	    while (st.get(x, bottom + 1) === type) bottom++;
1193	    const height = bottom - top + 1;
1194	    this.chunks.markDirtyArea(x - 6, top - 7, x + 6, bottom + 1);
1195	    // 清树干列 + 紧邻的侧枝（同类型，仅 ±1 防 "格洞" 残留）
1196	    for (let yy = top; yy <= bottom; yy++) {
1197	      st.setTile(x, yy, 0);
1198	      for (const s of [-1, 1]) {
1199	        if (st.get(x + s, yy) === type) st.setTile(x + s, yy, 0);
1200	      }
1201	    }
1202	    // 掉木材（与自有树同比例）+ 树顶枝条额外几份
1203	    const wood = Math.max(1, Math.floor(height * 0.8));
1204	    for (let p = 0; p < wood; p++) {
1205	      const dropY = (top + Math.floor((p + 0.5) * height / wood)) * TILE;
1206	      this.spawnDrop(x * TILE + 8 + (Math.random() - 0.5) * 14, dropY, 'wood', 1, (Math.random() - 0.5) * 2, -2 - Math.random());
1207	    }
1208	    // 橡实：与自有树同规则（75% 掉 2-3 颗，沿树冠区域散落供补种）
1209	    if (Math.random() < 0.75) {
1210	      const nAcorn = 2 + Math.floor(Math.random() * 2);
1211	      for (let a = 0; a < nAcorn; a++) {
1212	        const ax = x + (Math.random() - 0.5) * 2.5;
1213	        const ay = top + Math.random() * height * 0.4;
1214	        this.spawnDrop(ax * TILE + 8, ay * TILE, 'acorn', 1, (Math.random() - 0.5) * 3, -3 - Math.random());
1215	      }
1216	    }
1217	    this.spawnParticles(x * TILE + 8, top * TILE + 8, '#2E8B3D', 14, 2.2);
1218	  }
1219	
1220	  private tryPlace(tx: number, ty: number, itemDef: (typeof ITEM_DEFS)[number]) {
1221	    const st = this.world.store;
1222	    if (!st.inBounds(tx, ty)) return;
1223	    // 距离
1224	    const dx = tx - Math.floor(this.player.cx / TILE);
1225	    const dy = ty - Math.floor(this.player.cy / TILE);
1226	    if (Math.hypot(dx, dy) > 5.5) return;
1227	    const tileId = TILE_BY_KEY[itemDef.tile!];
1228	    const def = TILE_DEFS[tileId];
1229	    // 橡实: 只能种在草块正上方
1230	    if (itemDef.key === 'acorn' && st.get(tx, ty + 1) !== T.GRASS) {
1231	      this.cb.onToast('橡实只能种在草块上');
1232	      return;
1233	    }
1234	    const ow = def.w ?? 1, oh = def.h ?? 1;
1235	    // 绳索(RopeCoil 语义):从放置点向下延伸至实心/最多 10 格
1236	    if (itemDef.key === 'rope') {
1237	      const ropeTile = TILE_BY_KEY['v_213_rope']!;
1238	      let placed = 0;
1239	      for (let y = ty; y < ty + 10; y++) {
1240	        if (!st.inBounds(tx, y) || st.isActive(tx, y)) break;
1241	        st.setTile(tx, y, ropeTile, 0, 0);
1242	        placed++;
1243	      }
1244	      if (placed > 0) {
1245	        this.player.inv.removeAt(this.player.inv.selected, 1);
1246	        this.player.useTime = 14;
1247	        this.sfx.play('place');
1248	        this.cb.onInventoryChanged();
1249	      }
1250	      return;
1251	    }
1252	    // 放置空间检查
1253	    for (let dx2 = 0; dx2 < ow; dx2++) {
1254	      for (let dy2 = 0; dy2 < oh; dy2++) {
1255	        const px = tx + dx2, py = ty + dy2;
1256	        if (!st.inBounds(px, py)) return;
1257	        if (st.isActive(px, py)) return;
1258	        // 实心物不能与玩家重叠
1259	        if (def.solid && this.overlapsEntity(px, py)) return;

```


---

## 🤖 Assistant · 2026-08-09T10:48:52.928Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continue reading Game.ts from 1260 to end.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:48:52.929Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 560,
 "offset": 1260
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:52.933Z

**📎 ToolResult**

```
1260	      }
1261	    }
1262	    // 支撑检查：非漂浮（简化：需要任意相邻格有内容或墙）
1263	    const needSupport = def.solid || def.platform || def.framed;
1264	    if (needSupport && !this.hasSupport(tx, ty, ow, oh)) return;
1265	    if (this.player.useTime > 0) return;
1266	
1267	    // 放置
1268	    const isVanillaStyle = !!def.vanilla && def.vanilla.frame === 'style';
1269	    for (let dx2 = 0; dx2 < ow; dx2++) {
1270	      for (let dy2 = 0; dy2 < oh; dy2++) {
1271	        const px = tx + dx2, py = ty + dy2;
1272	        // 原版多格家具：帧用 18px 步长偏移（与 .wld 原生一致，渲染端直用）。
1273	        // 原版帧语义（TileObject.Place L74-102）：frameY 从【顶行 = 0】向下递增；
1274	        // ty 是顶部行（放置时鼠标指向顶部锚点）→ dy2=0 即顶行，frameY = dy2*18 正确
1275	        if (isVanillaStyle) {
1276	          // placeStyle:样式索引 → X 偏移 style*fw*18(2 宽物件步长 36,3 宽 54)
1277	          const strideX = (def.vanilla?.fw ?? 1) * 18;
1278	          st.setTile(px, py, tileId, (itemDef.placeStyle ?? 0) * strideX + dx2 * 18, dy2 * 18);
1279	        } else {
1280	          st.setTile(px, py, tileId, dx2, dy2);
1281	        }
1282	        // 水被方块挤出：水量转移到相邻可容纳的格子（上/左/右），
1283	        // 而不是被方块吞掉消失。封闭无处可去时才消失
1284	        const pi = st.idx(px, py);
1285	        const liq = st.liquid[pi];
1286	        if (liq > 0) {
1287	          const ltype = st.liquidType[pi];
1288	          st.setLiquid(px, py, 0, 0);
1289	          let remaining = liq;
1290	          for (const [ox, oy] of [[0, -1], [-1, 0], [1, 0]] as const) {
1291	            if (remaining <= 0) break;
1292	            const nx = px + ox, ny = py + oy;
1293	            if (!st.inBounds(nx, ny)) continue;
1294	            const nd = TILE_DEFS[st.type[st.idx(nx, ny)]];
1295	            if (nd && nd.solid) continue;
1296	            const ni = st.idx(nx, ny);
1297	            const cap = 255 - st.liquid[ni];
1298	            if (cap <= 0) continue;
1299	            const t = Math.min(remaining, cap);
1300	            st.setLiquid(nx, ny, st.liquid[ni] + t, ltype || st.liquidType[ni] || 1);
1301	            remaining -= t;
1302	          }
1303	        }
1304	      }
1305	    }
1306	    if (tileId === T.CHEST) {
1307	      this.world.chests.push({ x: tx, y: ty, items: Array(10).fill(null) });
1308	    }
1309	    this.player.inv.removeAt(this.player.inv.selected, 1);
1310	    this.player.useTime = 14;
1311	    this.sfx.play('place');
1312	    this.cb.onInventoryChanged();
1313	  }
1314	
1315	  private overlapsEntity(px: number, py: number): boolean {
1316	    const rx = px * TILE, ry = py * TILE;
1317	    if (this.player.x < rx + TILE && this.player.x + this.player.w > rx && this.player.y < ry + TILE && this.player.y + this.player.h > ry) return true;
1318	    for (const e of this.entities.enemies) {
1319	      if (e.x < rx + TILE && e.x + e.w > rx && e.y < ry + TILE && e.y + e.h > ry) return true;
1320	    }
1321	    return false;
1322	  }
1323	
1324	  private hasSupport(x: number, y: number, w: number, h: number): boolean {
1325	    const st = this.world.store;
1326	    // 下方
1327	    for (let dx = 0; dx < w; dx++) {
1328	      if (st.isActive(x + dx, y + h) || st.isSolid(x + dx, y + h) || st.wall[st.idx(x + dx, y + h)] !== 0) return true;
1329	    }
1330	    // 上方（火把等贴墙物）
1331	    for (let dx = 0; dx < w; dx++) {
1332	      if (st.isActive(x + dx, y - 1)) return true;
1333	    }
1334	    // 侧邻
1335	    for (let dy = 0; dy < h; dy++) {
1336	      if (st.isActive(x - 1, y + dy) || st.isActive(x + w, y + dy)) return true;
1337	    }
1338	    return false;
1339	  }
1340	
1341	  private interactAt(tx: number, ty: number) {
1342	    const st = this.world.store;
1343	    const type = st.get(tx, ty);
1344	    if (type === T.DOOR_CLOSED) {
1345	      this.toggleDoor(tx, ty, true);
1346	    } else if (type === T.DOOR_OPEN) {
1347	      this.toggleDoor(tx, ty, false);
1348	    } else if (type === T.CHEST) {
1349	      // 打开宝箱：精确命中或 3×3 容差（点击宝箱边缘也算）
1350	      const chest = this.findChest(tx, ty) ?? this.findChestNear(tx, ty);
1351	      if (chest) this.tryOpenChest(chest);
1352	    } else if (type === TILE_BY_KEY['crystal_heart']) {
1353	      // 生命水晶(放置态):右键使用(Player.cs ItemCheck_UseLifeCrystal L29358)
1354	      // statLifeMax<400 → +20 上限并回满该部分,放置物消耗
1355	      this.usePlacedLifeCrystal(tx, ty);
1356	    } else if (type === TILE_BY_KEY['bed']) {
1357	      // 床:设重生点(vanilla Player.FindBed 语义;敌怪环绕检查略)
1358	      this.world.spawnX = tx + 1;
1359	      this.world.spawnY = ty - 1;
1360	      this.cb.onToast('重生点已设置');
1361	      this.input.rightDown = false;
1362	    } else if (type === TILE_BY_KEY['v_132_lever'] || type === TILE_BY_KEY['v_136_switch']) {
1363	      // 拉杆/开关:切换通断(帧 +18 翻转),触发直线可见的陷阱(WorldGen Wiring 简化)
1364	      this.toggleSwitch(tx, ty, type);
1365	    } else if (type === TILE_BY_KEY['v_83_herbs_mature'] || type === TILE_BY_KEY['v_84_herbs_bloom']) {
1366	      // 药草收获:成熟/开花态右键 → 掉种子(style = frameX/18,WorldGen.cs:38731)
1367	      const i = st.idx(tx, ty);
1368	      const style = Math.floor(st.frameX[i] / 18);
1369	      st.setTile(tx, ty, 0);
1370	      const seedKeys = ['vi_307_daybloom_seeds', 'vi_308_moonglow_seeds', 'vi_309_blinkroot_seeds',
1371	        'vi_311_waterleaf_seeds', 'vi_310_deathweed_seeds', 'vi_312_fireblossom_seeds', 'vi_2357_shiverthorn_seeds'];
1372	      const sk = seedKeys[style] ?? seedKeys[0];
1373	      this.spawnDrop(tx * 16 + 8, ty * 16, sk, 1);
1374	      this.input.rightDown = false;
1375	    }
1376	  }
1377	
1378	  /** 放置态生命水晶使用(Player.cs:29358:statLifeMax≥400 拒绝,+20 上限+回复,消耗) */
1379	  private usePlacedLifeCrystal(tx: number, ty: number): void {
1380	    const st = this.world.store;
1381	    const def = TILE_DEFS[st.get(tx, ty)];
1382	    if (this.player.baseMaxHp >= 400) {
1383	      this.cb.onToast('生命上限已达到 400');
1384	      this.input.rightDown = false;
1385	      return;
1386	    }
1387	    this.player.baseMaxHp += 20;
1388	    this.player.hp = Math.min(this.player.maxHp, this.player.hp + 20);
1389	    this.addDamageNumber(this.player.cx, this.player.y, 20, false, '#40E080');
1390	    // 消耗放置物(2×2)
1391	    for (let dx = 0; dx < 2; dx++) {
1392	      for (let dy = 0; dy < 2; dy++) {
1393	        if (st.get(tx + dx, ty + dy) === TILE_BY_KEY['crystal_heart']) st.setTile(tx + dx, ty + dy, 0);
1394	      }
1395	    }
1396	    this.sfx.play('drink');
1397	    this.input.rightDown = false;
1398	    void def;
1399	  }
1400	
1401	  /** 开宝箱统一入口:锁定箱(原版 Chest.locked)需金钥匙,首次开启消耗 */
1402	  private tryOpenChest(chest: { locked?: boolean }): void {
1403	    if (chest.locked) {
1404	      const keyId = ITEM_BY_KEY['vi_327_golden_key'];
1405	      let keySlot = -1;
1406	      for (let i = 0; i < this.player.inv.slots.length; i++) {
1407	        const sl = this.player.inv.slots[i];
1408	        if (sl && sl.id === keyId && sl.stack > 0) { keySlot = i; break; }
1409	      }
1410	      if (keySlot < 0) { this.cb.onToast('宝箱被锁住了,需要金钥匙'); this.input.rightDown = false; return; }
1411	      this.player.inv.removeAt(keySlot, 1);
1412	      chest.locked = false;
1413	      this.sfx.play('tink');
1414	      this.cb.onToast('用金钥匙打开了宝箱');
1415	      this.cb.onInventoryChanged();
1416	    }
1417	    this.openChest?.(chest as never);
1418	    this.input.rightDown = false;
1419	  }
1420	
1421	  /** 拉杆/开关切换:帧翻转(原版 style 内 on/off 两态),直线驱动陷阱 */
1422	  private toggleSwitch(x: number, y: number, type: number): void {
1423	    const st = this.world.store;
1424	    const i = st.idx(x, y);
1425	    const on = st.frameX[i] >= 18;
1426	    st.setTile(x, y, type, on ? 0 : 18, st.frameY[i]);
1427	    this.sfx.play('tink');
1428	    this.fireTrapsFrom(x, y, !on);
1429	    this.input.rightDown = false;
1430	  }
1431	
1432	  /** 从电源点向四方向直线扫描 ≤60 格,遇陷阱(无实心阻挡)发射飞镖 */
1433	  private fireTrapsFrom(px: number, py: number, powerOn: boolean): void {
1434	    if (!powerOn) return;
1435	    const st = this.world.store;
1436	    const TRAP = TILE_BY_KEY['v_137_traps'];
1437	    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as const) {
1438	      for (let d = 1; d <= 60; d++) {
1439	        const x = px + dx * d, y = py + dy * d;
1440	        if (!st.inBounds(x, y)) break;
1441	        if (st.isSolid(x, y) && st.get(x, y) !== TRAP) break;
1442	        if (st.get(x, y) === TRAP) {
1443	          const key = x + ',' + y;
1444	          const last = this.trapCooldown.get(key) ?? -999;
1445	          if (this.tickCount - last < 40) return;
1446	          this.trapCooldown.set(key, this.tickCount);
1447	          const dart = new Dart(x * TILE + 8 + dx * 10, y * TILE + 8 + dy * 10, dx * 9, dy * 9, 20);
1448	          this.entities.add(dart, 'projectiles');
1449	          this.sfx.play('tink');
1450	          return;
1451	        }
1452	      }
1453	    }
1454	  }
1455	
1456	  /** 压力板:玩家踩上瞬间触发(原版 PressurePlate 语义,人触发灰板) */
1457	  private checkPressurePlates(): void {
1458	    const st = this.world.store;
1459	    const p = this.player;
1460	    const tx = Math.floor(p.cx / TILE), ty = Math.floor((p.y + p.h) / TILE);
1461	    const key = tx + ',' + ty;
1462	    if (st.get(tx, ty) === TILE_BY_KEY['v_135_pressure_plates'] && !this.plateLatch.has(key)) {
1463	      this.plateLatch.add(key);
1464	      this.fireTrapsFrom(tx, ty, true);
1465	    } else if (st.get(tx, ty) !== TILE_BY_KEY['v_135_pressure_plates']) {
1466	      this.plateLatch.delete(key);
1467	    }
1468	  }
1469	
1470	  /** 桶三态(Player.cs ItemCheck_Buckets L28137 语义):
1471	   *  空桶点液体 → 舀成对应满桶;满桶点空格 → 放置液体变空桶 */
1472	  private useBucket(key: string, tx: number, ty: number): void {
1473	    const st = this.world.store;
1474	    const liqTypeMap: Record<string, number> = { water_bucket: 1, lava_bucket: 2, honey_bucket: 3 };
1475	    const swap = (toKey: string) => {
1476	      // 原版语义:桶在手中原格替换(不跳格)
1477	      this.player.inv.slots[this.player.inv.selected] = { id: ITEM_BY_KEY[toKey], stack: 1 };
1478	      this.cb.onInventoryChanged();
1479	      this.player.useTime = 30;
1480	      this.input.rightDown = false;
1481	    };
1482	    if (key === 'empty_bucket') {
1483	      const i = st.idx(tx, ty);
1484	      if (st.liquid[i] > 0) {
1485	        const t = st.liquidType[i] || 1;
1486	        st.setLiquid(tx, ty, 0, 0);
1487	        swap(t === 2 ? 'lava_bucket' : t === 3 ? 'honey_bucket' : 'water_bucket');
1488	      }
1489	    } else {
1490	      // 满桶:目标格须空且(相邻可铺展/有底)——简化:空即可
1491	      const i = st.idx(tx, ty);
1492	      if (!st.flags[i]) {
1493	        const lt = liqTypeMap[key];
1494	        st.setLiquid(tx, ty, 255, lt);
1495	        swap('empty_bucket');
1496	      }
1497	    }
1498	  }
1499	
1500	  /** 门交互：开门按玩家朝向、失败换反向（原版 Player.cs L20965-20974）；
1501	   *  帧算法/样式保留/方向锚点见 world/Door.ts（原版 OpenDoor L22384 / CloseDoor L15901 语义） */
1502	  private toggleDoor(x: number, y: number, open: boolean) {
1503	    const st = this.world.store;
1504	    if (open) {
1505	      const dir = this.player.facing >= 0 ? 1 : -1;
1506	      if (!openDoor(st, x, y, dir) && !openDoor(st, x, y, -dir)) return;
1507	      this.sfx.play('door_open');
1508	    } else {
1509	      if (!closeDoor(st, x, y, Math.random, (bx, by) => this.overlapsEntity(bx, by))) return;
1510	      this.sfx.play('door_close');
1511	    }
1512	    this.input.rightDown = false;
1513	  }
1514	
1515	  openChest: ((c: ChestData) => void) | null = null;
1516	
1517	  private findChest(tx: number, ty: number): ChestData | null {
1518	    for (const c of this.world.chests) {
1519	      if ((c.x === tx || c.x + 1 === tx) && (c.y === ty || c.y + 1 === ty)) return c;
1520	    }
1521	    return null;
1522	  }
1523	
1524	  /** 3×3 邻域内找宝箱（点击容差） */
1525	  private findChestNear(tx: number, ty: number): ChestData | null {
1526	    for (let dy = -1; dy <= 1; dy++) {
1527	      for (let dx = -1; dx <= 1; dx++) {
1528	        const c = this.findChest(tx + dx, ty + dy);
1529	        if (c) return c;
1530	      }
1531	    }
1532	    return null;
1533	  }
1534	
1535	  private dumpChest(x: number, y: number) {
1536	    const c = this.findChest(x, y);
1537	    if (!c) return;
1538	    for (const item of c.items) {
1539	      if (item) this.spawnDrop(x * TILE + 16, y * TILE, ITEM_DEFS[item.id].key, item.stack);
1540	    }
1541	    this.world.chests = this.world.chests.filter((cc) => cc !== c);
1542	  }
1543	
1544	  // ================= 战斗 =================
1545	
1546	  private updateSwingHits() {
1547	    if (!this.swing) return;
1548	    this.swing.t--;
1549	    if (this.swing.t <= 0) { this.swing = null; return; }
1550	    const held = this.player.inv.heldItem();
1551	    if (!held) return;
1552	    const tool = ITEM_DEFS[held.id].tool;
1553	    // 近战判定范围因武器而异：剑用完整 reach；镐/斧/锤当武器不顺手（×0.8）；
1554	    // 空手默认 3 格
1555	    const reach = (tool?.reach ?? TILE * 3) * (tool?.type === 'sword' ? 1 : tool ? 0.8 : 1);
1556	    // 剑/工具挥舞顺带清除鼠标处的杂草
1557	    {
1558	      const [htx, hty] = this.camera.tileUnder(this.input.mouseX, this.input.mouseY);
1559	      if (this.world.store.get(htx, hty) === T.TALLGRASS) this.breakTile(htx, hty);
1560	    }
1561	    // 弧线判定：圆心向朝向方向平移（身后不再被波及；小动物/怪物共用同一判定圆）
1562	    const arcX = this.player.cx + this.player.facing * reach * 0.35;
1563	    const prog = 1 - this.swing.t / this.swing.dur;
1564	    // 小动物：任何挥击一击致死
1565	    for (const cent of this.entities.critters) {
1566	      const c = cent as Critter;
1567	      if (this.swingHitSet.has(c.id)) continue;
1568	      const cdx = c.cx - arcX, cdy = c.cy - this.player.cy;
1569	      if (Math.hypot(cdx, cdy) <= reach + c.w / 2) {
1570	        this.swingHitSet.add(c.id);
1571	        c.hurt(this);
1572	      }
1573	    }
1574	    for (const ent of this.entities.enemies) {
1575	      const e = ent as Enemy;
1576	      if (this.swingHitSet.has(e.id)) continue;
1577	      const dx = e.cx - arcX;
1578	      const dy = e.cy - this.player.cy;
1579	      const dist = Math.hypot(dx, dy);
1580	      if (dist > reach + e.w / 2) continue;
1581	      // 朝向检查（挥舞半程后命中判定放宽）
1582	      if (Math.sign(dx) !== this.player.facing && Math.abs(dx) > e.w / 2) continue;
1583	      this.swingHitSet.add(e.id);
1584	      // 怪物专属受击声（各家族不同）；播放失败回退通用 hit
1585	      if (!this.sfx.playFiles(e.def.hitSound)) this.sfx.play('hit');
1586	      const crit = Math.random() < 0.04; // 原版近战基础暴击 4%（Player.meleeCrit）
1587	      // 工具（镐/斧）也有攻击力但远弱于剑：功率/16（铁镐 3 / 铁斧 4，铁剑 16）—— 仅应急
1588	      const baseDmg = tool?.damage ?? Math.max(1, Math.ceil((tool?.power ?? 10) / 16));
1589	      // 原版 Main.DamageVar：±15% 浮动（1 + rand(-15..15)/100）
1590	      const dmg = Math.max(1, Math.round((baseDmg + this.player.meleeDamageBonus) * (crit ? 2 : 1) * (1 + (Math.random() * 30 - 15) / 100)));
1591	      const kdir = Math.sign(dx) || this.player.facing;
1592	      // 击退 = 工具官方击退值（原版 knockBack 2-5.5 → 速度系数 0.65）
1593	      const kb = (tool?.knockback ?? 3) * 0.65;
1594	      const killed = e.hurt(dmg, kdir * kb, -2.5, this);
1595	      this.addDamageNumber(e.cx, e.y, dmg, crit, crit ? '#FFD040' : '#FF7060');
1596	      if (killed && e.def.boss) { /* boss 死亡处理在 fixedUpdate */ }
1597	    }
1598	    void prog;
1599	  }
1600	
1601	  // ================= 生成 =================
1602	
1603	  private trySpawnEnemy() {
1604	    const w = this.world;
1605	    const p = this.player;
1606	    if (p.dead) return;
1607	    const isDay = w.clock.isDay;
1608	    const count = this.entities.enemies.filter((e) => !(e as Enemy).def.boss && !(e as Enemy).wormFollow).length;
1609	    // 水蜡烛(NPC.cs:43241-43247):spawnRate×0.75 且 maxSpawns×1.5
1610	    const cap = this.heldWaterCandle || this.waterCandleNear ? Math.floor(ENEMY_CAP * 1.5) : ENEMY_CAP;
1611	    if (count >= cap) return;
1612	    if (this.boss) return;
1613	
1614	    const rng = new RNG((Math.random() * 1e9) | 0);
1615	    // 生成点：玩家周围环带
1616	    const ang = rng.range(0, Math.PI * 2);
1617	    const dist = rng.range(SPAWN_MIN_DIST, SPAWN_MAX_DIST);
1618	    const ex = p.cx + Math.cos(ang) * dist;
1619	    const ey = p.cy + Math.sin(ang) * dist;
1620	    const tx = Math.floor(ex / TILE), ty = Math.floor(ey / TILE);
1621	    const st = w.store;
1622	    if (!st.inBounds(tx, ty) || tx < 2 || tx > st.w - 3) return;
1623	
1624	    const isUnderground = st.wall[st.idx(tx, ty)] !== 0 || ty > w.rockLevel;
1625	    // 海洋/水域排除：该列从天空到 rockLevel 全是液体 = 海里——除鱼类外不生成
1626	    // （蝙蝠等飞行怪在海面上盘旋也不合理，一并排除）
1627	    {
1628	      let liquidTop = -1;
1629	      for (let y = 2; y < Math.min(w.rockLevel, st.h); y++) {
1630	        if (st.liquid[st.idx(tx, y)] > 40) { liquidTop = y; break; }
1631	      }
1632	      if (liquidTop >= 0) {
1633	        // 水面之下 10 格仍是液体 → 判定为海/深水区
1634	        let deep = true;
1635	        for (let y = liquidTop; y < Math.min(liquidTop + 10, st.h); y++) {
1636	          if (st.liquid[st.idx(tx, y)] <= 40) { deep = false; break; }
1637	        }
1638	        if (deep) return;
1639	      }
1640	    }
1641	    // 地狱区：熔岩史莱姆 / 熔岩僵尸（不怕岩浆）
1642	    const hellTop = Math.floor(st.h * 0.86);
1643	    let key: string | null = null;
1644	    if (ty > hellTop) {
1645	      key = rng.chance(0.55) ? 'lava_slime' : 'magma_zombie';
1646	    } else if (isUnderground) {
1647	      key = rng.chance(0.6) ? 'cave_bat' : (rng.chance(0.5) ? 'slime_blue' : 'slime_green');
1648	    } else if (isDay) {
1649	      key = 'slime_green';
1650	    } else {
1651	      // 夜间地表：僵尸/恶魔眼/史莱姆——洞穴蝙蝠不在此列（只在洞里）
1652	      const r = rng.next();
1653	      key = r < 0.4 ? 'zombie' : r < 0.75 ? 'demon_eye' : 'slime_blue';
1654	    }
1655	    const def = ENEMY_DEFS[key];
1656	    if (def.nightOnly && isDay) return;
1657	    if (def.dayOnly && !isDay && !isUnderground) { /* 史莱姆夜间也可少量 */ }
1658	    // 找落脚点：从 ty 向下找空中有地面的位置
1659	    let spawnY = -1;
1660	    // 原版数据驱动怪（50% 概率从原版生成池选，属性/AI/贴图全走 vanilla-npcs.json）
1661	    let vanillaSpawn: Enemy | null = null;
1662	    if (rng.chance(0.5)) {
1663	      const pool = poolFor(Math.floor(w.groundLevel), st.h - 200, ty, isDay);
1664	      const vid = pool[(rng.next() * pool.length) | 0];
1665	      vanillaSpawn = Enemy.fromVanilla(vid, 0, 0);
1666	    }
1667	    const effDef = vanillaSpawn?.def ?? def;
1668	    // 蠕虫族（aiStyle 6）穿墙钻地：直接用环带点生成，不找空中落脚位
1669	    if (vanillaSpawn?.vanilla?.aiStyle === 6) {
1670	      vanillaSpawn.x = tx * TILE + 8 - vanillaSpawn.w / 2;
1671	      vanillaSpawn.y = ty * TILE + 8 - vanillaSpawn.h / 2;
1672	      vanillaSpawn.id = this.entities.nextId++;
1673	      this.entities.enemies.push(vanillaSpawn);
1674	      const segs = Enemy.spawnWormChain(vanillaSpawn, 5 + ((rng.next() * 4) | 0));
1675	      for (const s of segs) { s.id = this.entities.nextId++; this.entities.enemies.push(s); }
1676	      return;
1677	    }
1678	    for (let dy = -8; dy <= 12; dy++) {
1679	      const yy = ty + dy;
1680	      if (yy < 2 || yy > st.h - 3) continue;
1681	      // 落脚点必须无液体（方块之上有水 = 水下/水面，非鱼类不生成——
1682	      // 否则史莱姆会从湖/海底生成然后浮上来）
1683	      const dry = st.liquid[st.idx(tx, yy)] <= 40 && st.liquid[st.idx(tx, yy - 1)] <= 40;
1684	      const clear = !st.isSolid(tx, yy) && !st.isSolid(tx, yy - 1) && dry;
1685	      const ground = st.isSolid(tx, yy + 1) || st.isSolid(tx, yy + 2);
1686	      if (effDef.flying) {
1687	        if (!st.isSolid(tx, yy) && dry) { spawnY = yy; break; }
1688	      } else if (clear && ground) {
1689	        spawnY = yy;
1690	        break;
1691	      }
1692	    }
1693	    if (spawnY < 0) return;
1694	    // 地表暗处不生成（夜间地表有天空光 0.12，算可见）
1695	    if (vanillaSpawn) {
1696	      vanillaSpawn.x = tx * TILE + 8 - vanillaSpawn.w / 2;
1697	      vanillaSpawn.y = spawnY * TILE + TILE - vanillaSpawn.h;
1698	      vanillaSpawn.id = this.entities.nextId++;
1699	      this.entities.enemies.push(vanillaSpawn);
1700	      // 蠕虫族（aiStyle 6）：生成身×n+尾的段链（原版 NewNPC 链 NPC.cs:18174+）
1701	      if (vanillaSpawn.vanilla?.aiStyle === 6 && vanillaNpc(vanillaSpawn.vanillaId! + 1)) {
1702	        const segs = Enemy.spawnWormChain(vanillaSpawn, 5 + ((rng.next() * 4) | 0));
1703	        for (const s of segs) { s.id = this.entities.nextId++; this.entities.enemies.push(s); }
1704	      }
1705	      return;
1706	    }
1707	    this.spawnEnemy(key, tx * TILE + 8, spawnY * TILE);
1708	  }
1709	
1710	  // ================= NPC =================
1711	
1712	  private checkHousing() {
1713	    // 向导已随世界出生；此处仅在有合格房屋时为其安家
1714	    const guide = this.entities.npcs.find((n) => (n as TownNPC).npcKey === 'guide') as TownNPC | undefined;
1715	    if (!guide || guide.home) return;
1716	    const st = this.world.store;
1717	    outer:
1718	    for (let x = 3; x < st.w - 3; x++) {
1719	      for (let y = 3; y < st.h - 4; y++) {
1720	        if (st.get(x, y) !== T.DOOR_CLOSED) continue;
1721	        if (this.isValidHouse(x, y)) {
1722	          guide.home = { x: x + 2, y: y - 2 };
1723	          break outer;
1724	        }
1725	      }
1726	    }
1727	  }
1728	
1729	  /** 右键与附近 NPC 交谈(#13):点击目标须在 NPC 4 格内(否则不拦截右键交互) */
1730	  private talkToNearbyNpc(ctX: number, ctY: number): boolean {
1731	    const p = this.player;
1732	    for (const n of this.entities.npcs) {
1733	      const npc = n as TownNPC;
1734	      // 原版 ObjectData.Chat 语义:光标须落在 NPC 身上(命中盒 ±8px 容差),不是旁边
1735	      if (Math.hypot(npc.cx - p.cx, npc.cy - p.cy) > TILE * 3.5) continue;
1736	      const mx = (ctX + 0.5) * TILE, my = (ctY + 0.5) * TILE;
1737	      if (mx < npc.x - 8 || mx > npc.x + npc.w + 8 || my < npc.y - 8 || my > npc.y + npc.h + 8) continue;
1738	      const tips = [
1739	        '你好！我是向导。按 E 打开背包，那里可以合成物品。',
1740	        '用镐挖矿、斧砍树。木头+凝胶可以做火把！',
1741	        '夜里会有僵尸和恶魔眼出现，小心行事。',
1742	        '挖到矿石后，用熔炉炼锭、铁砧做更好的装备。',
1743	        '手持火把也能照亮周围，不用非得放置。',
1744	        '想知道更多？去地下找找宝箱吧！',
1745	      ];
1746	      if (npc.npcKey === 'nurse') {
1747	        // 护士:50 铜币治疗至满(原版 Nurse 治疗费随缺失血量;简化固定)
1748	        if (npc.talkCooldown <= 0) {
1749	          if (p.hp >= p.maxHp) { this.cb.onToast('护士:你很健康,不需要我'); }
1750	          else {
1751	            const coinId2 = ITEM_BY_KEY['coin_copper'];
1752	            let coins2 = 0;
1753	            for (const sl of this.player.inv.slots) if (sl && sl.id === coinId2) coins2 += sl.stack;
1754	            if (coins2 < 50) { this.cb.onToast('护士:治疗要 50 铜币'); }
1755	            else {
1756	              let left2 = 50;
1757	              for (let i = 0; i < this.player.inv.slots.length && left2 > 0; i++) {
1758	                const sl = this.player.inv.slots[i];
1759	                if (!sl || sl.id !== coinId2) continue;
1760	                const take = Math.min(sl.stack, left2);
1761	                sl.stack -= take; left2 -= take;
1762	                if (sl.stack <= 0) this.player.inv.slots[i] = null;
1763	              }
1764	              p.hp = p.maxHp;
1765	              this.cb.onInventoryChanged();
1766	              this.addDamageNumber(p.cx, p.y, p.maxHp - p.hp, false, '#40E080');
1767	              this.cb.onToast('护士:治疗完成(-50 铜币)');
1768	            }
1769	          }
1770	          npc.talkCooldown = 120;
1771	        }
1772	        return true;
1773	      }
1774	      if (npc.npcKey === 'merchant') {
1775	        if (npc.talkCooldown <= 0) {
1776	          this.merchantTrade();
1777	          npc.talkCooldown = 120;
1778	        }
1779	        return true;
1780	      }
1781	      npc.bubble = tips[Math.floor(Math.random() * tips.length)];
1782	      npc.bubbleT = 360;
1783	      npc.talkCooldown = 600;
1784	      return true;
1785	    }
1786	    return false;
1787	  }
1788	
1789	  /** 商人交易(简化商店):铜币买固定商品——火把10/木材20/铜镐/次级治疗药水 */
1790	  private merchantTrade(): void {
1791	    const inv = this.player.inv;
1792	    const coinId = ITEM_BY_KEY['coin_copper'];
1793	    let coins = 0;
1794	    for (const sl of inv.slots) if (sl && sl.id === coinId) coins += sl.stack;
1795	    const stock: Array<[string, number, number]> = [
1796	      ['torch', 10, 50], ['wood', 20, 20], ['copper_pickaxe', 1, 500], ['lesser_healing_potion', 3, 150],
1797	    ];
1798	    const affordable = stock.filter(([, , cost]) => cost <= coins);
1799	    if (affordable.length === 0) {
1800	      this.cb.onToast('商人:铜币不够呀(最便宜木材 20)');
1801	      return;
1802	    }
1803	    const [key, n, cost] = affordable[Math.floor(Math.random() * affordable.length)];
1804	    // 扣币
1805	    let left = cost;
1806	    for (let i = 0; i < inv.slots.length && left > 0; i++) {
1807	      const sl = inv.slots[i];
1808	      if (!sl || sl.id !== coinId) continue;
1809	      const take = Math.min(sl.stack, left);
1810	      sl.stack -= take; left -= take;
1811	      if (sl.stack <= 0) inv.slots[i] = null;
1812	    }
1813	    inv.add(ITEM_BY_KEY[key], n);
1814	    this.cb.onInventoryChanged();
1815	    this.cb.onToast(`商人:买到 ${n} × ${ITEM_DEFS[ITEM_BY_KEY[key]].name}(-${cost} 铜币)`);
1816	  }
1817	
1818	  private isValidHouse(doorX: number, doorY: number): boolean {
1819	    // 门占 3 格（doorY 为门顶），检查门内空间：有光源 + 有实心地板 + 有背景墙

```


---

## 🤖 Assistant · 2026-08-09T10:48:56.258Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continue reading the rest of Game.ts (1820-2339), then items.ts, Door.ts, LiquidSim, Sfx.ts, Renderer.ts, Input.ts, Dart.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:48:56.260Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "offset": 1820
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:56.276Z

**📎 ToolResult**

```
1820	    // doorY+3 为地板行
1821	    const st = this.world.store;
1822	    let light = false, solidFloor = 0, walls = 0;
1823	    for (let dx = 1; dx <= 12; dx++) {
1824	      for (let dy = -6; dy <= 4; dy++) {
1825	        const x = doorX + dx, y = doorY + dy;
1826	        if (!st.inBounds(x, y)) continue;
1827	        if (st.get(x, y) === T.TORCH) light = true;
1828	        if (dy === 3 && st.isSolid(x, y)) solidFloor++;
1829	        if (dy >= -2 && dy <= 2 && st.wall[st.idx(x, y)] !== 0) walls++;
1830	      }
1831	    }
1832	    return light && solidFloor >= 6 && walls >= 20;
1833	  }
1834	
1835	  // ================= GameHooks 实现 =================
1836	
1837	  enemies() {
1838	    return this.entities.enemies;
1839	  }
1840	
1841	  spawnDrop(x: number, y: number, itemKey: string, count = 1, vx = 0, vy = -2) {
1842	    const id = ITEM_BY_KEY[itemKey];
1843	    if (id === undefined) return;
1844	    const drop = new ItemDrop(x - 6, y - 6, id, count, vx, vy);
1845	    this.entities.add(drop, 'drops');
1846	  }
1847	
1848	  damagePlayer(dmg: number, srcX: number, srcY: number, attacker?: Enemy) {
1849	    const p = this.player;
1850	    if (p.dead) return;
1851	    const ok = p.damage(dmg, srcX, srcY);
1852	    if (ok) {
1853	      // 致死一击：不播受击声，只播死亡声（保证最后听到的音效是死亡）
1854	      if (p.hp <= 0) this.sfx.play('pkilled');
1855	      else this.sfx.play('hurt');
1856	      // 实际扣血 = max(1, dmg - defense*0.5)（在 Player.damage 内）
1857	      const dealt = Math.max(1, dmg - p.defense * 0.5);
1858	      this.addDamageNumber(p.cx, p.y, Math.round(dealt), false, '#FF5050');
1859	      // 荆棘 Buff：受击反弹 2 伤害（移植自 Maples Player.Thorn）
1860	      if (p.thornsActive && attacker && !attacker.dead) {
1861	        attacker.hurt(2, Math.sign(attacker.cx - p.cx) || 1, -1.5, this);
1862	        this.addDamageNumber(attacker.cx, attacker.y, 2, false, '#80FF80');
1863	      }
1864	      if (p.hp <= 0) {
1865	        p.dead = true;
1866	        p.respawnTimer = 0;
1867	        // 死亡音由 Player 中央逻辑统一发声（覆盖所有死法），此处不重复
1868	        this.cb.onToast('你死了…');
1869	        // 掉一半铜币
1870	        const coins = p.inv.countOf(ITEM_BY_KEY['coin_copper']);
1871	        if (coins > 0) {
1872	          p.inv.remove(ITEM_BY_KEY['coin_copper'], Math.floor(coins / 2));
1873	        }
1874	      }
1875	    }
1876	  }
1877	
1878	  addDamageNumber(x: number, y: number, amount: number, crit: boolean, color = '#FFF') {
1879	    this.dmgNumbers.push({ x, y, vy: -1.6, value: amount, crit, color, life: 50 });
1880	  }
1881	
1882	  onEnemyKilled(key: string) {
1883	    if (key === 'eye_of_cthulhu') {
1884	      this.world.flags.downedEyeOfCthulhu = true;
1885	    }
1886	  }
1887	
1888	  /** 小动物生成：视野外地表，按昼夜 + 栖息生态筛选，权重抽取。
1889	   *  地面种：脚底精确贴地表格顶（此前高度>1格的实体被埋进地里卡死）；
1890	   *  飞行种：仅开阔天空（向上 30 格无实心）且地表无水（鸭子除外）；
1891	   *  蝴蝶：低空（地表上 1-4 格），优先附近有花的列 */
1892	  private spawnCritter() {
1893	    const st = this.world.store;
1894	    const isDay = this.world.clock.isDay;
1895	    const halfView = Math.ceil((this.camera.viewW / (this.camera.zoom || 1)) / 2 / TILE) + 8;
1896	    const side = Math.random() < 0.5 ? -1 : 1;
1897	    // 找列：蝴蝶优先附近 8 格内有 FLOWER 的列
1898	    let tx = Math.floor(this.player.cx / TILE) + side * (halfView + Math.floor(Math.random() * 18));
1899	    const isButterflyTentative = isDay && Math.random() < 0.35;
1900	    if (isButterflyTentative) {
1901	      for (let attempt = 0; attempt < 6; attempt++) {
1902	        const fx = tx + Math.floor((Math.random() - 0.5) * 16);
1903	        if (fx < 4 || fx >= st.w - 4) continue;
1904	        let found = false;
1905	        for (let dx = -4; dx <= 4 && !found; dx++) {
1906	          for (let y = Math.max(4, Math.floor(this.player.cy / TILE) - 24); y < Math.min(st.h - 4, Math.floor(this.player.cy / TILE) + 30); y++) {
1907	            if (st.type[st.idx(fx + dx, y)] === T.FLOWER) { found = true; break; }
1908	          }
1909	        }
1910	        if (found) { tx = fx; break; }
1911	      }
1912	    }
1913	    if (tx < 4 || tx >= st.w - 4) return;
1914	    // 找地表
1915	    const startY = Math.max(4, Math.floor(this.player.cy / TILE) - 24);
1916	    let groundY = -1;
1917	    for (let y = startY; y < Math.min(st.h - 4, startY + 70); y++) {
1918	      if (st.isSolid(tx, y)) { groundY = y; break; }
1919	    }
1920	    if (groundY < 0) return;
1921	    const surfaceWater = st.liquid[st.idx(tx, groundY - 1)] > 80;
1922	    // 生态判定
1923	    const gTile = st.type[st.idx(tx, groundY)];
1924	    let biome: 'forest' | 'snow' | 'sand' = 'forest';
1925	    if (gTile === T.SNOW) biome = 'snow';
1926	    else if (gTile === T.SAND || gTile === TILE_BY_KEY['sandstone'] || gTile === TILE_BY_KEY['hardened_sand']) biome = 'sand';
1927	    const nearWater = surfaceWater || (() => {
1928	      for (let dx = -2; dx <= 2; dx++) {
1929	        for (let dy = 0; dy <= 2; dy++) {
1930	          if (st.liquid[st.idx(tx + dx, groundY + dy)] > 80) return true;
1931	        }
1932	      }
1933	      return false;
1934	    })();
1935	    // 按昼夜 + 栖息生态过滤（水面列只出 water 生态或飞行种）
1936	    const pool = CRITTER_DEFS.filter((c) => {
1937	      if (c.dayOnly && !isDay) return false;
1938	      if (c.nightOnly && isDay) return false;
1939	      // 鸭子是两栖：水面列可生成（落在岸边浅水/滩涂），其余地面种不能在水列
1940	      if (surfaceWater && !c.water && c.kind !== 'fly' && c.key !== 'duck') return false;
1941	      if (!c.biomes.includes(biome) && !(nearWater && c.biomes.includes('water'))) return false;
1942	      return true;
1943	    });
1944	    if (!pool.length) return;
1945	    const total = pool.reduce((s2, c) => s2 + c.weight, 0);
1946	    let r = Math.random() * total;
1947	    let pick = pool[0];
1948	    for (const c of pool) { r -= c.weight; if (r <= 0) { pick = c; break; } }
1949	
1950	    if (pick.kind === 'fly') {
1951	      // 飞行种：地表不能是水（水面飞鸟/蝴蝶不合理，鸭子除外但鸭子不是 fly）
1952	      if (surfaceWater) return;
1953	      // 开阔天空检查（洞穴/地底不生成）
1954	      for (let k = 2; k <= 30; k++) {
1955	        if (groundY - k < 4) return;
1956	        if (st.isSolid(tx, groundY - k)) return;
1957	      }
1958	      // 蝴蝶低空（1-4 格）、鸟/萤火虫中高空
1959	      const lowFly = pick.key === 'butterfly' || pick.key === 'gold_butterfly';
1960	      const flyY = lowFly ? (groundY - 1 - Math.random() * 3) * TILE : (groundY - 8 - Math.random() * 12) * TILE;
1961	      this.entities.add(new Critter(pick.key, tx * TILE + 8, flyY), 'critters');
1962	    } else if (pick.water && surfaceWater) {
1963	      // 水生种（鸭子）：落在水面上（自上而下第一个液体格），不是湖底
1964	      let surfY = 4;
1965	      while (surfY < st.h - 4 && st.liquid[st.idx(tx, surfY)] <= 80) surfY++;
1966	      if (surfY >= st.h - 4) return;
1967	      this.entities.add(new Critter(pick.key, tx * TILE + 8, surfY * TILE), 'critters');
1968	    } else {
1969	      // 地面种：参数即脚底 y（构造器内减 h），精确站上地表格顶
1970	      const c = new Critter(pick.key, tx * TILE + 8, groundY * TILE);
1971	      // 安全兜底：身体中心在实心块内则放弃（防卡死）
1972	      const ci = st.idx(Math.floor(c.cx / TILE), Math.floor(c.cy / TILE));
1973	      if (st.type[ci] !== 0 && st.isSolid(Math.floor(c.cx / TILE), Math.floor(c.cy / TILE))) return;
1974	      this.entities.add(c, 'critters');
1975	    }
1976	  }
1977	
1978	  spawnEnemy(key: string, x: number, y: number) {
1979	    const e = new Enemy(key, x, y);
1980	    this.entities.add(e, 'enemies');
1981	    if (e.def.boss) this.boss = e;
1982	    return e;
1983	  }
1984	
1985	  /** 树苗生长成树 */
1986	  private growSaplings() {
1987	    const st = this.world.store;
1988	    const grown: Array<[number, number]> = [];
1989	    // 只扫玩家附近 60×40 区域
1990	    const ptx = Math.floor(this.player.cx / TILE), pty = Math.floor(this.player.cy / TILE);
1991	    for (let dy = -20; dy <= 20; dy++) {
1992	      for (let dx = -30; dx <= 30; dx++) {
1993	        const x = ptx + dx, y = pty + dy;
1994	        if (!st.inBounds(x, y) || st.get(x, y) !== T.SAPLING) continue;
1995	        // 上方 2-3 格净空才长
1996	        if (st.isActive(x, y - 1) || st.isActive(x, y - 2) || st.isActive(x, y - 3)) continue;
1997	        if (Math.random() < 0.5) { // 每次一半概率，模拟时间流逝
1998	          grown.push([x, y]);
1999	        }
2000	      }
2001	    }
2002	    for (const [x, y] of grown) {
2003	      const groundY = y + 1;
2004	      const th = 5 + Math.floor(Math.random() * 4);
2005	      st.setTile(x, y, 0);
2006	      for (let dy2 = 1; dy2 <= th; dy2++) {
2007	        if (!st.inBounds(x, groundY - dy2)) break;
2008	        if (st.isActive(x, groundY - dy2)) break;
2009	        st.setTile(x, groundY - dy2, T.TREE, dy2 === th ? 22 : 0, dy2 === th ? 198 : 0); // 原版帧：顶标记(22,198)+干身(0,0)
2010	      }
2011	      this.world.registerTree(x, groundY - th, th);
2012	      this.chunks.markDirtyArea(x - 4, groundY - th - 4, x + 4, groundY);
2013	    }
2014	  }
2015	
2016	  /** 拾取物品飘名（主角旁浅白文本）。同一时间只保留一个，
2017	   * 新拾取直接替换旧的 —— 不产生拖影，不会误读为多个物品 */
2018	  showPickupLabel(itemKey: string) {
2019	    const def = ITEM_DEFS[ITEM_BY_KEY[itemKey]];
2020	    if (!def) return;
2021	    this.dmgNumbers = this.dmgNumbers.filter((d) => !d.label);
2022	    this.dmgNumbers.push({
2023	      x: this.player.cx, y: this.player.y - 8, vy: -0.7,
2024	      value: 0, crit: false, color: '#F0F0F0', life: 55, label: def.name,
2025	    });
2026	  }
2027	
2028	  playSfx(name: string, vol?: number) {
2029	    this.sfx.play(name as SfxName, vol ?? 1);
2030	  }
2031	
2032	  playSfxFiles(files: string[], vol?: number) {
2033	    if (!this.sfx.playFiles(files, vol ?? 1)) this.sfx.play('hit', vol ?? 1);
2034	  }
2035	
2036	  /** 拾取物品后刷新 UI（带轻量节流 + 尾包补发，最多延迟 ~166ms） */
2037	  private invNotifyAt = -100;
2038	  private invNotifyPending = false;
2039	  /** 新物品入手飘名（主角旁浅白文本） */
2040	
2041	  notifyInventoryChanged() {
2042	    // 检测新物品：与上次快照比较，新增的种类在主角旁飘名
2043	    const inv = this.player.inv;
2044	    if (!this._invSnapshot) {
2045	      this._invSnapshot = new Map<number, number>();
2046	      for (const s2 of inv.slots) {
2047	        if (s2) this._invSnapshot.set(s2.id, (this._invSnapshot.get(s2.id) ?? 0) + s2.stack);
2048	      }
2049	      return;
2050	    }
2051	    const now = new Map<number, number>();
2052	    for (const s2 of inv.slots) {
2053	      if (s2) now.set(s2.id, (now.get(s2.id) ?? 0) + s2.stack);
2054	    }
2055	    for (const [id, n] of now) {
2056	      const before = this._invSnapshot.get(id) ?? 0;
2057	      if (n > before && this.tickCount - this.lastNotifiedAt > 30) {
2058	        this.lastNotifiedAt = this.tickCount;
2059	        const def = ITEM_DEFS[id];
2060	        if (def) {
2061	          this.dmgNumbers.push({
2062	            x: this.player.cx, y: this.player.y - 6, vy: -0.9,
2063	            value: 0, crit: false, color: '#FFFFFF', life: 60, label: def.name,
2064	          } as DamageNumber & { label: string });
2065	        }
2066	        break; // 每次 refresh 只飘一个
2067	      }
2068	    }
2069	    this._invSnapshot = now;
2070	    if (this.tickCount - this.invNotifyAt >= 10) {
2071	      this.invNotifyAt = this.tickCount;
2072	      this.invNotifyPending = false;
2073	      this.cb.onInventoryChanged();
2074	    } else {
2075	      this.invNotifyPending = true;
2076	    }
2077	  }
2078	  private _invSnapshot: Map<number, number> | null = null;
2079	  private lastNotifiedAt = 0;
2080	
2081	  private flushInvNotify() {
2082	    if (this.invNotifyPending && this.tickCount - this.invNotifyAt >= 10) {
2083	      this.invNotifyAt = this.tickCount;
2084	      this.invNotifyPending = false;
2085	      this.cb.onInventoryChanged();
2086	    }
2087	  }
2088	
2089	  /** 火把火星：视区内点燃的火把按概率在火点处飘出上浮火粒 */
2090	  private emitTorchSparks() {
2091	    if (this.tickCount % 3 !== 0) return; // 20Hz 足够，省扫描
2092	    const st = this.world.store;
2093	    const cam = this.camera;
2094	    const z = cam.zoom || 1;
2095	    const tx0 = Math.max(0, Math.floor((cam.x - cam.viewW / 2 / z) / TILE));
2096	    const tx1 = Math.min(this.world.w - 1, Math.ceil((cam.x + cam.viewW / 2 / z) / TILE));
2097	    const ty0 = Math.max(0, Math.floor((cam.y - cam.viewH / 2 / z) / TILE));
2098	    const ty1 = Math.min(this.world.h - 1, Math.ceil((cam.y + cam.viewH / 2 / z) / TILE));
2099	    for (let y = ty0; y <= ty1; y++) {
2100	      for (let x = tx0; x <= tx1; x++) {
2101	        const i = st.idx(x, y);
2102	        if (st.type[i] !== T.TORCH) continue;
2103	        if (Math.random() >= 0.14) continue;
2104	        // 帧为 0(地面) 时火点在格顶上方；墙面变体也近似取格顶
2105	        this.particles.push({
2106	          x: x * TILE + 5 + Math.random() * 6,
2107	          y: y * TILE - 2 + Math.random() * 4,
2108	          vx: (Math.random() - 0.5) * 0.25,
2109	          vy: -0.35 - Math.random() * 0.4,
2110	          life: 16 + Math.random() * 12, maxLife: 28,
2111	          color: Math.random() < 0.55 ? '#FFB642' : Math.random() < 0.5 ? '#FF8A2A' : '#FFD97A',
2112	          size: 1 + Math.random() * 1.2,
2113	          grav: -0.015,  // 微浮力：火星徐徐上飘
2114	          damp: 0.985,
2115	        });
2116	      }
2117	    }
2118	  }
2119	
2120	  spawnParticles(
2121	    x: number, y: number, color: string, count: number, speed = 2,
2122	    opts: { life?: number; damp?: number; grav?: number } = {},
2123	  ) {
2124	    const base = opts.life ?? 40;
2125	    for (let i = 0; i < count; i++) {
2126	      const a = Math.random() * Math.PI * 2;
2127	      const life = Math.round(base * (0.6 + Math.random() * 0.4));
2128	      this.particles.push({
2129	        x, y, vx: Math.cos(a) * speed * Math.random(), vy: Math.sin(a) * speed * Math.random() - 1,
2130	        life, maxLife: life, color, size: 2 + Math.random() * 2,
2131	        damp: opts.damp, grav: opts.grav,
2132	      });
2133	    }
2134	    if (this.particles.length > 600) this.particles.splice(0, this.particles.length - 600);
2135	  }
2136	
2137	  setZoom(z: number) {
2138	    if (!this.camera) return;
2139	    this.camera.setZoomTarget(z);
2140	  }
2141	
2142	  // ================= 合成 =================
2143	
2144	  itemId(key: string): number {
2145	    return ITEM_BY_KEY[key];
2146	  }
2147	
2148	  stationsNearby(): Set<string> {
2149	    const st = this.world.store;
2150	    const px = Math.floor(this.player.cx / TILE), py = Math.floor(this.player.cy / TILE);
2151	    const found = new Set<string>(['hand']);
2152	    for (let dx = -4; dx <= 4; dx++) {
2153	      for (let dy = -3; dy <= 3; dy++) {
2154	        const t = st.get(px + dx, py + dy);
2155	        if (t === T.WORKBENCH) found.add('workbench');
2156	        if (t === T.FURNACE) found.add('furnace');
2157	        if (t === T.ANVIL) found.add('anvil');
2158	      }
2159	    }
2160	    return found;
2161	  }
2162	
2163	  canCraft(r: (typeof RECIPES)[number]): boolean {
2164	    if (!this.stationsNearby().has(r.station)) return false;
2165	    return r.inputs.every(([key, n]) => this.player.inv.countOf(ITEM_BY_KEY[key]) >= n);
2166	  }
2167	
2168	  craft(r: (typeof RECIPES)[number]) {
2169	    if (!this.canCraft(r)) return;
2170	    for (const [key, n] of r.inputs) this.player.inv.remove(ITEM_BY_KEY[key], n);
2171	    this.player.inv.add(ITEM_BY_KEY[r.out], r.count);
2172	    this.cb.onInventoryChanged();
2173	  }
2174	
2175	  // ================= 召唤 Boss =================
2176	
2177	  /** 通用 Boss 召唤:vanilla 数据路径(NPC 13=世吞头带体节链 / 50=史莱姆王 / 266=克脑) */
2178	  summonBoss(key: string): void {
2179	    if (this.boss) { this.cb.onToast('已有 Boss 在场'); return; }
2180	    const side = Math.random() < 0.5 ? -1 : 1;
2181	    const tx = Math.floor((this.player.cx + side * 55 * TILE) / TILE);
2182	    let ty = 10;
2183	    for (; ty < this.world.h; ty++) {
2184	      if (this.world.store.type[this.world.store.idx(tx, ty)] !== 0) break;
2185	    }
2186	    const spawnY = Math.max(4, ty - 12) * TILE;
2187	    const vanillaId = key === 'eater_of_worlds_head' ? 13 : key === 'king_slime' ? 50 : key === 'brain_of_cthulhu' ? 266 : -1;
2188	    if (vanillaId >= 0 && Enemy.fromVanilla) {
2189	      const head = Enemy.fromVanilla(vanillaId, tx * TILE + 8, spawnY);
2190	      if (head) {
2191	        this.entities.add(head, 'enemies');
2192	        this.boss = head;
2193	        if (vanillaId === 13) {
2194	          // 世吞体节链(原版 15-30 段)
2195	          const segs = Enemy.spawnWormChain(head, 15 + Math.floor(Math.random() * 16));
2196	          for (const sg of segs) this.entities.add(sg, 'enemies');
2197	        }
2198	        this.sfx.playWav('roar');
2199	        this.cb.onToast('你感到有个邪恶的东西在看着你……');
2200	        return;
2201	      }
2202	    }
2203	    this.spawnEnemy(key, tx * TILE + 8, spawnY);
2204	    this.sfx.playWav('roar');
2205	    this.cb.onToast('你感到有个邪恶的东西在看着你……');
2206	  }
2207	
2208	  useSuspiciousEye() {
2209	    if (this.world.clock.isDay) {
2210	      this.cb.onToast('夜晚才能使用…');
2211	      return;
2212	    }
2213	    if (this.boss) return;
2214	    // 从远处地表生成（离玩家 ~55 格），Boss 会自己飞过来
2215	    const side = Math.random() < 0.5 ? -1 : 1;
2216	    const tx = Math.floor((this.player.cx + side * 55 * TILE) / TILE);
2217	    let ty = 10;
2218	    for (; ty < this.world.h; ty++) {
2219	      if (this.world.store.type[this.world.store.idx(tx, ty)] !== 0) break;
2220	    }
2221	    const spawnY = Math.max(4, ty - 12) * TILE;
2222	    const e = this.spawnEnemy('eye_of_cthulhu', tx * TILE + 8, spawnY);
2223	    void e;
2224	    this.sfx.playWav('roar');
2225	    this.cb.onToast('你感到有个邪恶的东西在看着你……');
2226	  }
2227	
2228	  /** 地图传送：在目标点附近找可容纳主角的空间（2 格高净空 + 站立地面）。
2229	   *  优先目标点自身，然后螺旋外扩到 24 格内就近安置 */
2230	  private teleportNear(tx: number, ty: number): boolean {
2231	    const st = this.world.store;
2232	    const p = this.player;
2233	    // 空中落点：2 格净空即可（无地面要求）
2234	    const fitsAir = (x: number, y: number) => {
2235	      for (let dy = 0; dy <= 1; dy++) {
2236	        if (!st.inBounds(x, y - dy) || st.isSolid(x, y - dy)) return false;
2237	      }
2238	      return true;
2239	    };
2240	    const fits = (x: number, y: number) => {
2241	      // (x, y-1..y) 两格净空（无实心/无液体），y+1 格实心站立
2242	      for (let dy = 0; dy <= 1; dy++) {
2243	        if (!st.inBounds(x, y - dy) || st.isSolid(x, y - dy)) return false;
2244	        if (st.liquid[st.idx(x, y - dy)] > 100) return false;
2245	      }
2246	      return st.inBounds(x, y + 1) && st.isSolid(x, y + 1);
2247	    };
2248	    if (fits(tx, ty)) {
2249	      p.x = tx * TILE + 1; p.y = (ty - 1) * TILE;
2250	    } else {
2251	      // 螺旋外扩找最近可站位置
2252	      let found = false;
2253	      for (let r = 1; r <= 24 && !found; r++) {
2254	        for (let dx = -r; dx <= r && !found; dx++) {
2255	          for (let dy = -r; dy <= r && !found; dy++) {
2256	            if (Math.max(Math.abs(dx), Math.abs(dy)) !== r) continue;
2257	            if (fits(tx + dx, ty + dy)) {
2258	              p.x = (tx + dx) * TILE + 1;
2259	              p.y = (ty + dy - 1) * TILE;
2260	              found = true;
2261	            }
2262	          }
2263	        }
2264	      }
2265	      if (!found) {
2266	        // 高空/无地面：允许落在空中（目标列上下找 2 格净空，重力会带下来）
2267	        for (let dy = 0; dy <= 6; dy++) {
2268	          for (const sy of [ty - dy, ty + dy]) {
2269	            if (fitsAir(tx, sy)) {
2270	              p.x = tx * TILE + 1; p.y = (sy - 1) * TILE;
2271	              p.vx = 0; p.vy = 0;
2272	              this.camera.x = p.cx; this.camera.y = p.cy;
2273	              return true;
2274	            }
2275	          }
2276	        }
2277	        this.cb.onToast('传送失败：目标区域完全实心');
2278	        return false;
2279	      }
2280	    }
2281	    p.vx = 0; p.vy = 0;
2282	    this.camera.x = p.cx; this.camera.y = p.cy;
2283	    return true;
2284	  }
2285	
2286	  // ================= 重生 =================
2287	
2288	  /** 玩家死亡瞬间：红色粉碎粒子散落 + 脚下留一块墓碑 */
2289	  private _deathHandled = false;
2290	  private handlePlayerDeath() {
2291	    const p = this.player;
2292	    // 红色粉碎粒子：身体范围多层爆散，喷溅落地反弹/停驻后缓慢淡出（约 5 秒）
2293	    this.spawnParticles(p.cx, p.y + 8, '#C02020', 22, 3.2, { life: 300, damp: 0.988, grav: 0.09 });
2294	    this.spawnParticles(p.cx, p.cy, '#8A1010', 16, 2.4, { life: 280, damp: 0.985, grav: 0.09 });
2295	    this.spawnParticles(p.cx, p.cy - 6, '#E85050', 10, 2.8, { life: 260, damp: 0.988, grav: 0.09 });
2296	    // 墓碑：作为物理实体从死亡点掉落（空中死亡则从空中坠落，落地弹跳翻滚后安放）
2297	    this.entities.add(new Tombstone(p.cx, p.cy), 'props');
2298	  }
2299	
2300	
2301	  respawnPlayer() {
2302	    const p = this.player;
2303	    p.hp = p.maxHp;
2304	    p.dead = false;
2305	    p.iframes = 90;
2306	    p.respawnTimer = 0;
2307	    p.x = this.world.spawnX * TILE + 8;
2308	    p.y = (this.world.spawnY - 3) * TILE;
2309	    p.vx = 0; p.vy = 0;
2310	  }
2311	
2312	  // ================= 渲染 =================
2313	
2314	  render() {
2315	    const cam = this.camera;
2316	    const L = this.lighting;
2317	    this.renderer.annotateMarks = this.annotateMode ? this.marks : null;
2318	    const hover = this.input.uiBlocking ? null : (() => {
2319	      const [tx, ty] = cam.tileUnder(this.input.mouseX, this.input.mouseY);
2320	      return this.world.store.inBounds(tx, ty) ? { x: tx, y: ty } : null;
2321	    })();
2322	    this.renderer.render(
2323	      cam, this.world, this.world.clock, this.chunks,
2324	      L.r, L.g, L.b, L.rx, L.ry, L.rw, L.rh,
2325	      this.player,
2326	      this.entities.all(),
2327	      this.particles, this.dmgNumbers,
2328	      this.swing, hover,
2329	      this.boss ? { name: this.boss.def.name, hp: this.boss.hp, maxHp: this.boss.maxHp } : null,
2330	      this.input.mouseX, this.input.mouseY, this.input.mouseDown,
2331	      this.mining ? Math.min(1, this.mining.progress / this.hardnessCache) : 0,
2332	    );
2333	  }
2334	
2335	  /** 每逻辑帧后处理挥舞命中（在 fixedUpdate 实体更新后调用） */
2336	  postUpdate() {
2337	    this.updateSwingHits();
2338	  }
2339	}
2340	

```


---

## 🤖 Assistant · 2026-08-09T10:48:58.495Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read items.ts (structure — ItemDef fields), Sfx.ts, Door.ts, LiquidSim.ts, Dart.ts, Input.ts, Renderer.ts key parts, constants.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:48:58.501Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/data/items.ts",
 "limit": 260
}
```


---

## 🤖 Assistant · 2026-08-09T10:48:58.503Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:58.506Z

**📎 ToolResult**

```
1	// 音效：原版 wav 素材（public/sounds/）+ WebAudio 合成兜底
2	// hit 敌人受击 / hurt 玩家受击 / pickup 拾取 / dig 挖掘 / place 放置 / drink 饮用 / chop 砍树 / splash 落水
3	// + killed 怪物死亡 / zombie 僵尸环境声 / roar Boss咆哮 / coin 拾币 / door_open door_close / tink 敲石 / shatter 玻璃破碎 / drown 溺水
4	export type SfxName =
5	  | 'hit' | 'hurt' | 'pickup' | 'dig' | 'place' | 'drink' | 'chop' | 'splash'
6	  | 'killed' | 'pkilled' | 'zombie' | 'roar' | 'coin' | 'door_open' | 'door_close' | 'tink' | 'shatter' | 'drown';
7	
8	// 逻辑名 → 原版 wav 文件（多文件随机选 + 音高扰动）
9	const WAV_MAP: Record<SfxName, string[]> = {
10	  hit: ['NPC_Hit_1', 'NPC_Hit_2', 'NPC_Hit_3', 'NPC_Hit_4', 'NPC_Hit_5'],
11	  hurt: ['Player_Hit_0', 'Player_Hit_1', 'Player_Hit_2'],
12	  killed: ['NPC_Killed_1', 'NPC_Killed_2', 'NPC_Killed_3'],
13	  pkilled: ['Player_Killed'],
14	  zombie: ['Zombie_1', 'Zombie_2', 'Zombie_3', 'Zombie_4', 'Zombie_5', 'Zombie_6'],
15	  roar: ['Roar_0', 'Roar_1'],
16	  pickup: ['Grab'],
17	  dig: ['Dig_0', 'Dig_1', 'Dig_2'],
18	  chop: ['Grass'],
19	  tink: ['Tink_0', 'Tink_1'],
20	  place: ['Dig_1', 'Dig_2'],
21	  shatter: ['Shatter'],
22	  coin: ['Coin_0', 'Coin_1', 'Coins'],
23	  door_open: ['Door_Opened'],
24	  door_close: ['Door_Closed'],
25	  splash: ['Splash_0', 'Splash_1'],
26	  drown: ['Drown'],
27	  // 以下无原版素材，走合成
28	  drink: [],
29	};
30	
31	export class Sfx {
32	  private ctx: AudioContext | null = null;
33	  private buffers = new Map<string, AudioBuffer>();
34	  muted = false;
35	
36	  private extraFiles = new Set<string>();
37	  /** 追加加载额外 wav 文件（怪物专属声效等） */
38	  addFiles(files: string[]) {
39	    for (const f of files) this.extraFiles.add(f);
40	    const ctx = this.ctx;
41	    if (!ctx) return;
42	    for (const f of files) {
43	      if (this.buffers.has(f)) continue;
44	      fetch(`sounds/${f}.wav`).then((r) => (r.ok ? r.arrayBuffer() : null)).then((ab) => {
45	        if (!ab) return;
46	        ctx.decodeAudioData(ab).then((buf) => this.buffers.set(f, buf)).catch(() => {});
47	      }).catch(() => {});
48	    }
49	  }
50	
51	  /** 预加载全部 wav（在用户手势后调用可获得最佳兼容；挂起态 decodeAudioData 也可用） */
52	  async load(): Promise<void> {
53	    const ctx = this.ensure(true);
54	    if (!ctx) return;
55	    const files = new Set<string>();
56	    for (const list of Object.values(WAV_MAP)) for (const f of list) files.add(f);
57	    for (const f of this.extraFiles) files.add(f);
58	    await Promise.all([...files].map(async (f) => {
59	      try {
60	        const r = await fetch(`sounds/${f}.wav`);
61	        if (!r.ok) return;
62	        const buf = await ctx.decodeAudioData(await r.arrayBuffer());
63	        this.buffers.set(f, buf);
64	      } catch { /* 单文件失败静默 */ }
65	    }));
66	  }
67	
68	  private ensure(silent = false): AudioContext | null {
69	    if (this.muted && !silent) return null;
70	    if (!this.ctx) {
71	      const AC = window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
72	      if (!AC) return null;
73	      this.ctx = new AC();
74	    }
75	    if (this.ctx.state === 'suspended') this.ctx.resume().catch(() => {});
76	    return this.ctx;
77	  }
78	
79	  /** 播放原版 wav（随机变体 + 轻微音高扰动）；vol 0-1 */
80	  playWav(name: SfxName, vol = 1): boolean {
81	    const list = WAV_MAP[name];
82	    if (!list || !list.length) return false;
83	    return this.playWavFile(list[Math.floor(Math.random() * list.length)], vol);
84	  }
85	
86	  /** 播放任意 wav 文件列表（随机选 + 音高扰动）；供怪物专属声效用 */
87	  playFiles(files: string[], vol = 1): boolean {
88	    if (!files.length) return false;
89	    return this.playWavFile(files[Math.floor(Math.random() * files.length)], vol);
90	  }
91	
92	  /** 按文件名直播 */
93	  playWavFile(file: string, vol = 1): boolean {
94	    const ctx = this.ensure();
95	    if (!ctx) return false;
96	    const buf = this.buffers.get(file);
97	    if (!buf) return false;
98	    const src = ctx.createBufferSource();
99	    src.buffer = buf;
100	    src.playbackRate.value = 0.92 + Math.random() * 0.16;
101	    const g = ctx.createGain();
102	    g.gain.value = Math.min(1, vol);
103	    src.connect(g).connect(ctx.destination);
104	    src.start();
105	    return true;
106	  }
107	
108	  play(name: SfxName, vol = 1) {
109	    // 优先原版素材，失败回退合成
110	    if (this.playWav(name, vol)) return;
111	    const ctx = this.ensure();
112	    if (!ctx) return;
113	    const t = ctx.currentTime;
114	    const osc = (type: OscillatorType, f0: number, f1: number, dur: number, vol: number, delay = 0) => {
115	      const o = ctx.createOscillator();
116	      const g = ctx.createGain();
117	      o.type = type;
118	      o.frequency.setValueAtTime(f0, t + delay);
119	      o.frequency.exponentialRampToValueAtTime(Math.max(1, f1), t + delay + dur);
120	      g.gain.setValueAtTime(vol, t + delay);
121	      g.gain.exponentialRampToValueAtTime(0.001, t + delay + dur);
122	      o.connect(g).connect(ctx.destination);
123	      o.start(t + delay);
124	      o.stop(t + delay + dur);
125	    };
126	    switch (name) {
127	      case 'hit': osc('square', 320, 110, 0.09, 0.12); break;
128	      case 'chop': osc('triangle', 220, 80, 0.12, 0.16); break;
129	      case 'hurt': osc('sawtooth', 180, 60, 0.22, 0.14); break;
130	      case 'killed': osc('square', 260, 60, 0.25, 0.14); break;
131	      case 'pkilled': osc('sawtooth', 160, 40, 0.6, 0.18); break;
132	      case 'zombie': osc('sawtooth', 90, 55, 0.5, 0.1); break;
133	      case 'roar': osc('sawtooth', 70, 40, 0.9, 0.2); break;
134	      case 'pickup': osc('sine', 520, 990, 0.09, 0.1); osc('sine', 780, 1320, 0.08, 0.06, 0.05); break;
135	      case 'dig': osc('square', 140, 90, 0.05, 0.06); break;
136	      case 'tink': osc('sine', 900, 500, 0.06, 0.08); break;
137	      case 'place': osc('triangle', 260, 120, 0.08, 0.12); break;
138	      case 'drink': osc('sine', 300, 620, 0.06, 0.08); osc('sine', 420, 780, 0.06, 0.07, 0.07); osc('sine', 560, 940, 0.06, 0.06, 0.14); break;
139	      case 'splash': osc('sine', 700, 200, 0.18, 0.1); break;
140	      case 'coin': osc('sine', 990, 1400, 0.07, 0.08); osc('sine', 1320, 1760, 0.09, 0.06, 0.05); break;
141	      case 'door_open': osc('triangle', 180, 320, 0.12, 0.1); break;
142	      case 'door_close': osc('triangle', 320, 160, 0.1, 0.1); break;
143	      case 'shatter': osc('square', 1400, 300, 0.15, 0.1); break;
144	      case 'drown': osc('sine', 400, 90, 0.4, 0.1); break;
145	    }
146	  }
147	}
148	

```


---

## 👤 User(sidechain) · 2026-08-09T10:48:58.507Z

**📎 ToolResult**

```
1	// 物品注册表
2	export type ToolType = 'pick' | 'axe' | 'sword' | 'hammer';
3	// Buff 类型（药水饮用后生效）
4	export type PotionBuff = 'agility' | 'ironskin' | 'resistance' | 'thorns' | 'regen';
5	// 盔甲部位：0 头盔 1 胸甲 2 胫甲（与 Inventory.armorSlotReq 的格位对应）
6	export type ArmorSlot = 0 | 1 | 2;
7	
8	export interface ItemDef {
9	  key: string;
10	  name: string;
11	  maxStack: number;
12	  tile?: string;          // 放置的 tile key
13	  placeStyle?: number;     // 放置的样式索引(vanilla style 帧 X 偏移 = style*fw*18)
14	  magic?: {               // 魔法武器:消耗 mana 发射投射物
15	    damage: number;
16	    speed: number;        // 使用冷却 tick
17	    manaCost: number;
18	    projSpeed: number;
19	    proj?: 'spark' | 'bolt'; // 投射物外观
20	  };
21	  ranged?: {              // 远程武器:消耗 ammo 弹药发射投射物
22	    damage: number;
23	    speed: number;        // 使用冷却 tick
24	    knockback: number;
25	    ammo: string;         // 弹药 item key(箭)
26	    projSpeed: number;    // 投射物速度 px/tick
27	  };
28	  wall?: string;          // 放置的 wall key
29	  tool?: {
30	    type: ToolType;
31	    power?: number;       // 工具力（镐/斧/锤）
32	    damage?: number;      // 武器伤害
33	    speed?: number;       // 使用间隔 tick
34	    knockback?: number;
35	    reach?: number;       // 攻击/作用半径（px）
36	  };
37	  heal?: number;          // 食用/饮用回复
38	  potion?: {
39	    buff: PotionBuff;
40	    duration: number;     // 秒
41	    isHealType: boolean;  // 受"耐药性"封锁
42	  };
43	  accessory?: 'lucky_horseshoe' | 'feral_claws'; // 配饰效果
44	  armor?: { slot: ArmorSlot; defense: number };   // 盔甲（可穿装备/时装格，仅装备格计防御）
45	  value?: number;         // 钱币价值（铜币）
46	  desc?: string;
47	}
48	
49	export const ITEM_DEFS: ItemDef[] = [];
50	const byKey: Record<string, number> = {};
51	export const ITEM_BY_KEY: Record<string, number> = byKey;
52	
53	function item(d: Partial<ItemDef> & { key: string; name: string }) {
54	  byKey[d.key] = ITEM_DEFS.length;
55	  ITEM_DEFS.push({ maxStack: 999, ...d } as ItemDef);
56	}
57	
58	// ---- 基础方块 ----
59	item({ key: 'dirt_block', name: '泥土块', tile: 'dirt' });
60	item({ key: 'stone_block', name: '石块', tile: 'stone' });
61	item({ key: 'wood', name: '木材', tile: 'wood' });
62	item({ key: 'sand_block', name: '沙块', tile: 'sand' });
63	item({ key: 'snow_block', name: '雪块', tile: 'snow' });
64	item({ key: 'platform', name: '木平台', tile: 'platform', maxStack: 999 });
65	item({ key: 'torch', name: '火把', tile: 'torch' });
66	item({ key: 'door', name: '木门', tile: 'door_closed', maxStack: 99 });
67	item({ key: 'workbench', name: '工作台', tile: 'workbench', maxStack: 99 });
68	item({ key: 'furnace', name: '熔炉', tile: 'furnace', maxStack: 99 });
69	item({ key: 'anvil', name: '铁砧', tile: 'anvil', maxStack: 99 });
70	item({ key: 'chest', name: '宝箱', tile: 'chest', maxStack: 99 });
71	
72	// ---- 材料 ----
73	item({ key: 'gel', name: '凝胶', desc: '史莱姆的残留物' });
74	item({ key: 'acorn', name: '橡实', desc: '种在草块上会长成树', maxStack: 99, tile: 'acorn_sapling' });
75	item({ key: 'mushroom_item', name: '蘑菇', heal: 15, value: 1 });
76	item({ key: 'copper_ore', name: '铜矿', desc: '可在熔炉炼成铜锭' });
77	item({ key: 'iron_ore', name: '铁矿' });
78	item({ key: 'silver_ore', name: '银矿' });
79	item({ key: 'gold_ore', name: '金矿' });
80	item({ key: 'copper_bar', name: '铜锭' });
81	item({ key: 'iron_bar', name: '铁锭' });
82	item({ key: 'silver_bar', name: '银锭' });
83	item({ key: 'gold_bar', name: '金锭' });
84	item({ key: 'lens', name: '晶状体', desc: '恶魔眼的眼睛' });
85	item({ key: 'suspicious_eye', name: '可疑的眼球', desc: '夜间使用会召唤不祥之物…', maxStack: 20 });
86	item({ key: 'lesser_healing_potion', name: '弱效治疗药水', heal: 50, maxStack: 30 });
87	item({ key: 'coin_copper', name: '铜币', maxStack: 999, value: 1 });
88	item({ key: 'coin_silver', name: '银币', maxStack: 999, value: 100 });
89	item({ key: 'coin_gold', name: '金币', maxStack: 999, value: 10000 });
90	
91	// ---- 药水（Buff 来源，数值移植自 Maples Potions/*.asset）----
92	item({ key: 'heal_potion', name: '治疗药水', maxStack: 30, heal: 100, desc: '回复 100 生命',
93	  potion: { buff: 'resistance', duration: 60, isHealType: true } });
94	item({ key: 'agility_potion', name: '敏捷药水', maxStack: 30, desc: '移速 +25%，持续 4 分钟',
95	  potion: { buff: 'agility', duration: 240, isHealType: false } });
96	item({ key: 'ironskin_potion', name: '铁皮药水', maxStack: 30, desc: '防御 +6，持续 5 分钟',
97	  potion: { buff: 'ironskin', duration: 300, isHealType: false } });
98	item({ key: 'thorns_potion', name: '荆棘药水', maxStack: 30, desc: '受击反弹 2 伤害，持续 2 分钟',
99	  potion: { buff: 'thorns', duration: 120, isHealType: false } });
100	item({ key: 'regen_potion', name: '恢复药水', maxStack: 30, desc: '每 5 秒回复 10 生命，持续 2 分钟',
101	  potion: { buff: 'regen', duration: 120, isHealType: true } });
102	
103	// ---- 配饰（移植自 Maples Accessory）----
104	item({ key: 'lucky_horseshoe', name: '幸运马掌', maxStack: 1, accessory: 'lucky_horseshoe',
105	  desc: '免疫摔落伤害' });
106	item({ key: 'feral_claws', name: '猛爪手套', maxStack: 1, accessory: 'feral_claws',
107	  desc: '近战攻速 ×2，伤害 +5' });
108	
109	// ---- 盔甲（铜/铁/银/金三件套，防御取原版）----
110	const armorTiers: Array<[string, string, [number, number, number]]> = [
111	  // key 前缀, 显示前缀, [头盔, 胸甲, 胫甲] 防御
112	  ['copper', '铜', [1, 2, 1]],
113	  ['iron', '铁', [2, 3, 2]],
114	  ['silver', '银', [3, 4, 3]],
115	  ['gold', '金', [4, 5, 4]],
116	];
117	const armorParts: Array<[string, string, ArmorSlot]> = [
118	  ['helmet', '头盔', 0], ['chainmail', '胸甲', 1], ['greaves', '胫甲', 2],
119	];
120	for (const [prefix, cn, defs] of armorTiers) {
121	  armorParts.forEach(([suffix, cnPart, slot], k) => {
122	    item({
123	      key: `${prefix}_${suffix}`, name: `${cn}${cnPart}`, maxStack: 1,
124	      armor: { slot, defense: defs[k] },
125	      desc: `防御 +${defs[k]}`,
126	    });
127	  });
128	}
129	
130	// ---- 工具/武器（数值 = 官方原版 1.4.0.5 Item.cs SetDefaults，铜币价值）----
131	// 木镐/木斧为自定义低档（原版无对应）；木剑(24)=官方 7 伤、木锤(196)=官方 25 锤力
132	item({ key: 'wood_pickaxe', name: '木镐', maxStack: 1, value: 50,
133	  tool: { type: 'pick', power: 12, damage: 2, speed: 23, knockback: 2, reach: 2.6 * 16 } });
134	item({ key: 'wood_axe', name: '木斧', maxStack: 1, value: 50,
135	  tool: { type: 'axe', power: 4, damage: 2, speed: 30, knockback: 4.5, reach: 2.4 * 16 } });
136	item({ key: 'wood_sword', name: '木剑', maxStack: 1, value: 100,
137	  tool: { type: 'sword', damage: 7, speed: 25, knockback: 4, reach: 2.2 * 16 } });
138	item({ key: 'wood_hammer', name: '木锤', maxStack: 1, value: 50,
139	  tool: { type: 'hammer', power: 25, damage: 2, speed: 37, knockback: 5.5, reach: 2.4 * 16 },
140	  desc: '敲除背景墙' });
141	// 铜（3509/3506/3508/3505）
142	item({ key: 'copper_pickaxe', name: '铜镐', maxStack: 1, value: 500,
143	  tool: { type: 'pick', power: 35, damage: 4, speed: 23, knockback: 2, reach: 2.6 * 16 } });
144	item({ key: 'copper_axe', name: '铜斧', maxStack: 1, value: 400,
145	  tool: { type: 'axe', power: 7, damage: 3, speed: 30, knockback: 4.5, reach: 2.4 * 16 } });
146	item({ key: 'copper_sword', name: '铜剑', maxStack: 1, value: 450,
147	  tool: { type: 'sword', damage: 8, speed: 23, knockback: 5, reach: 2.2 * 16 } });
148	item({ key: 'copper_hammer', name: '铜锤', maxStack: 1, value: 400,
149	  tool: { type: 'hammer', power: 35, damage: 4, speed: 33, knockback: 5.5, reach: 2.4 * 16 },
150	  desc: '敲除背景墙' });
151	// 铁（1/10/4/7）
152	item({ key: 'iron_pickaxe', name: '铁镐', maxStack: 1, value: 2000,
153	  tool: { type: 'pick', power: 40, damage: 5, speed: 20, knockback: 2, reach: 2.6 * 16 } });
154	item({ key: 'iron_axe', name: '铁斧', maxStack: 1, value: 1600,
155	  tool: { type: 'axe', power: 9, damage: 5, speed: 27, knockback: 4.5, reach: 2.4 * 16 } });
156	item({ key: 'iron_sword', name: '铁剑', maxStack: 1, value: 1800,
157	  tool: { type: 'sword', damage: 10, speed: 21, knockback: 5, reach: 2.2 * 16 } });
158	item({ key: 'iron_hammer', name: '铁锤', maxStack: 1, value: 1600,
159	  tool: { type: 'hammer', power: 40, damage: 7, speed: 30, knockback: 5.5, reach: 2.4 * 16 },
160	  desc: '敲除背景墙' });
161	// 银（3515/3512/3514/3511）
162	item({ key: 'silver_pickaxe', name: '银镐', maxStack: 1, value: 5000,
163	  tool: { type: 'pick', power: 45, damage: 6, speed: 19, knockback: 2, reach: 2.6 * 16 } });
164	item({ key: 'silver_axe', name: '银斧', maxStack: 1, value: 4000,
165	  tool: { type: 'axe', power: 10, damage: 6, speed: 26, knockback: 4.5, reach: 2.4 * 16 } });
166	item({ key: 'silver_sword', name: '银剑', maxStack: 1, value: 4500,
167	  tool: { type: 'sword', damage: 11, speed: 21, knockback: 5, reach: 2.2 * 16 } });
168	item({ key: 'silver_hammer', name: '银锤', maxStack: 1, value: 4000,
169	  tool: { type: 'hammer', power: 45, damage: 9, speed: 29, knockback: 5.5, reach: 2.4 * 16 },
170	  desc: '敲除背景墙' });
171	// 金（3521/3518/3520/3517）
172	item({ key: 'gold_pickaxe', name: '金镐', maxStack: 1, value: 10000,
173	  tool: { type: 'pick', power: 55, damage: 6, speed: 20, knockback: 2, reach: 2.6 * 16 } });
174	item({ key: 'gold_axe', name: '金斧', maxStack: 1, value: 8000,
175	  tool: { type: 'axe', power: 11, damage: 7, speed: 26, knockback: 4.5, reach: 2.4 * 16 } });
176	item({ key: 'gold_sword', name: '金剑', maxStack: 1, value: 9000,
177	  tool: { type: 'sword', damage: 13, speed: 20, knockback: 5, reach: 2.2 * 16 } });
178	item({ key: 'gold_hammer', name: '金锤', maxStack: 1, value: 8000,
179	  tool: { type: 'hammer', power: 55, damage: 9, speed: 28, knockback: 5.5, reach: 2.4 * 16 },
180	  desc: '敲除背景墙' });
181	
182	// ===================== 原版素材批次：新材料 / 方块 / 家具 =====================
183	// ---- 替代矿与困难模式矿（先做美术/掉落） ----
184	item({ key: 'tin_ore', name: '锡矿' });
185	item({ key: 'lead_ore', name: '铅矿' });
186	item({ key: 'tungsten_ore', name: '钨矿' });
187	item({ key: 'platinum_ore', name: '铂金矿' });
188	item({ key: 'tin_bar', name: '锡锭' });
189	item({ key: 'lead_bar', name: '铅锭' });
190	item({ key: 'tungsten_bar', name: '钨锭' });
191	item({ key: 'platinum_bar', name: '铂金锭' });
192	item({ key: 'demonite_ore', name: '魔矿' });
193	item({ key: 'meteorite', name: '陨石' });
194	item({ key: 'hellstone', name: '狱石' });
195	item({ key: 'crimtane_ore', name: '猩红矿' });
196	item({ key: 'cobalt_ore', name: '钴矿' });
197	item({ key: 'mythril_ore', name: '秘银矿' });
198	item({ key: 'adamantite_ore', name: '精金矿' });
199	item({ key: 'palladium_ore', name: '钯金矿' });
200	item({ key: 'orichalcum_ore', name: '山铜矿' });
201	item({ key: 'titanium_ore', name: '钛矿' });
202	item({ key: 'chlorophyte_ore', name: '叶绿矿' });
203	
204	// ---- 宝石 ----
205	item({ key: 'sapphire', name: '蓝宝石', value: 15 });
206	item({ key: 'ruby', name: '红宝石', value: 22 });
207	item({ key: 'emerald', name: '翡翠', value: 15 });
208	item({ key: 'topaz', name: '黄玉', value: 11 });
209	item({ key: 'amethyst', name: '紫水晶', value: 11 });
210	item({ key: 'diamond', name: '钻石', value: 30 });
211	
212	// ---- 冰雪 / 沙漠 / 基础方块 ----
213	item({ key: 'ice_block', name: '冰块', tile: 'ice' });
214	item({ key: 'ice_brick', name: '冰砖', tile: 'ice_brick' });
215	item({ key: 'snow_brick', name: '雪砖', tile: 'snow_brick' });
216	item({ key: 'sandstone_block', name: '沙岩', tile: 'sandstone' });
217	item({ key: 'hardened_sand_block', name: '硬化沙块', tile: 'hardened_sand' });
218	item({ key: 'desert_fossil', name: '沙漠化石' });
219	item({ key: 'clay_block', name: '粘土块', tile: 'clay' });
220	item({ key: 'glass', name: '玻璃', tile: 'glass' });
221	item({ key: 'obsidian', name: '黑曜石', tile: 'obsidian' });
222	item({ key: 'gray_brick', name: '灰砖', tile: 'gray_brick' });
223	item({ key: 'red_brick', name: '红砖', tile: 'red_brick' });
224	item({ key: 'mud_block', name: '泥块', tile: 'mud' });
225	item({ key: 'silt_block', name: '淤泥块', tile: 'silt' });
226	
227	// ---- 家具 ----
228	item({ key: 'table', name: '木桌', tile: 'table', maxStack: 99 });
229	item({ key: 'chair', name: '木椅', tile: 'chair', maxStack: 99 });
230	item({ key: 'bed', name: '床', tile: 'bed', maxStack: 99 });
231	item({ key: 'bookcase', name: '书架', tile: 'bookcase', maxStack: 99 });
232	item({ key: 'grandfather_clock', name: '落地钟', tile: 'grandfather_clock', maxStack: 99 });
233	item({ key: 'piano', name: '钢琴', tile: 'piano', maxStack: 99 });
234	item({ key: 'dresser', name: '梳妆台', tile: 'dresser', maxStack: 99 });
235	item({ key: 'bench', name: '长凳', tile: 'bench', maxStack: 99 });
236	item({ key: 'bathtub', name: '浴缸', tile: 'bathtub', maxStack: 99 });
237	item({ key: 'keg', name: '酒桶', tile: 'keg', maxStack: 99 });
238	item({ key: 'cooking_pot', name: '汤锅', tile: 'cooking_pot', maxStack: 99 });
239	item({ key: 'clay_pot', name: '陶盆', tile: 'clay_pot', maxStack: 99 });
240	item({ key: 'tombstone', name: '墓碑', tile: 'tombstone_v', maxStack: 99 });
241	item({ key: 'life_crystal', name: '水晶之心', maxStack: 99, desc: '古老的生命结晶' });
242	item({ key: 'candle', name: '蜡烛', tile: 'candle', maxStack: 99 });
243	item({ key: 'chandelier', name: '吊灯', tile: 'chandelier', maxStack: 99 });
244	item({ key: 'lantern', name: '吊挂灯笼', tile: 'lantern', maxStack: 99 });
245	item({ key: 'candelabra', name: '烛台', tile: 'candelabra', maxStack: 99 });
246	item({ key: 'chinese_lantern', name: '中式灯笼', tile: 'chinese_lantern', maxStack: 99 });
247	item({ key: 'skull_lantern', name: '骷髅灯笼', tile: 'skull_lantern', maxStack: 99 });
248	item({ key: 'water_candle', name: '水蜡烛', tile: 'water_candle', maxStack: 99 });
249	// 瓦罐战利品
250	item({ key: 'bomb', name: '小型炸弹', maxStack: 99, desc: '用力扔出去会爆炸…（待实装）', value: 5 });
251	item({ key: 'rope', name: '攀爬绳', maxStack: 999, desc: '左键放置绳列,触碰可攀爬', value: 1, tile: 'v_213_rope' });
252	
253	export interface ItemStack { id: number; stack: number; }
254	export function mkStack(key: string, stack = 1): ItemStack | null {
255	  const id = byKey[key];
256	  if (id === undefined) return null;
257	  return { id, stack };
258	}
259	
260	// ===================== wld 导入补全物品（compat-report 驱动） =====================

```


---

## 🤖 Assistant · 2026-08-09T10:48:58.562Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/Door.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:48:58.568Z

**📎 ToolResult**

```
1	// 门帧算法（原版 Tiles_10/11 表竖排布局，WorldGen.OpenDoor L22384 / CloseDoor L15901 反推）：
2	//   关门 style = 36*(frameX/54) + frameY/54 —— 每列 36 个样式，frameX 只有 0/54 两列；
3	//   frameX = 变体(0/18/36 三张纹理) + 54*列，frameY = 54*(style%36) + 行内偏移(0/18/36)。
4	//   开门 frameX = 72*列 + (direction==-1 ? 36 : 0)（%72 后 0/36 为锚点列、18/54 为右侧列）。
5	// 本项目曾误用 frameX = style*54（横排），越界导致门贴图不可见/错位。
6	import type { TileStore } from './TileStore';
7	import { T } from '../data/tiles';
8	
9	/** 关门锚点帧（顶格）：[frameX, frameY] */
10	export function doorClosedFrame(style: number, variant = 0): [number, number] {
11	  return [variant * 18 + 54 * Math.floor(style / 36), 54 * (style % 36)];
12	}
13	
14	/** 由任意关门格帧反推 style */
15	export function doorStyleOf(fx: number, fy: number): number {
16	  return Math.floor(fx / 54) * 36 + Math.floor(fy / 54);
17	}
18	
19	/** 生成期放置整扇关闭门（1×3，锚点在顶格 (x,y)） */
20	export function placeDoorClosed(st: TileStore, x: number, y: number, style: number, variant = 0): void {
21	  const [fx, fy] = doorClosedFrame(style, variant);
22	  for (let dy = 0; dy < 3; dy++) {
23	    if (st.inBounds(x, y + dy)) st.setTileSilent(x, y + dy, T.DOOR_CLOSED, fx, fy + dy * 18);
24	  }
25	}
26	
27	/** 挖除含 (x,y) 格的整扇门（关门 1×3 / 开门 2×3，帧内偏移 = frame%/格步长）。
28	 *  返回掉落锚点；非门格返回 null。 */
29	export function clearDoorAt(st: TileStore, x: number, y: number): [number, number] | null {
30	  const t = st.get(x, y);
31	  if (t !== T.DOOR_CLOSED && t !== T.DOOR_OPEN) return null;
32	  const i = st.idx(x, y);
33	  const w = t === T.DOOR_OPEN ? 2 : 1;
34	  const col = Math.floor(st.frameX[i] / 18) % w;
35	  const row = Math.floor(st.frameY[i] / 18) % 3;
36	  const ax = x - col, ay = y - row;
37	  for (let dx = 0; dx < w; dx++) {
38	    for (let dy = 0; dy < 3; dy++) {
39	      if (st.inBounds(ax + dx, ay + dy) && st.get(ax + dx, ay + dy) === t) st.setTile(ax + dx, ay + dy, 0);
40	    }
41	  }
42	  return [ax, ay];
43	}
44	
45	/** 开门（原版 OpenDoor 语义）。direction: 玩家面朝方向 ±1。
46	 *  返回 false = 目标侧被挡（调用方应换 -direction 重试）。 */
47	export function openDoor(st: TileStore, x: number, y: number, direction: number): boolean {
48	  if (st.get(x, y) !== T.DOOR_CLOSED) return false;
49	  // 锚点行：frameY % 54 === 0
50	  let ay = y;
51	  while (st.get(x, ay) === T.DOOR_CLOSED && st.frameY[st.idx(x, ay)] % 54 !== 0) {
52	    if (--ay < 0) return false;
53	  }
54	  if (st.get(x, ay) !== T.DOOR_CLOSED) return false;
55	  const ai = st.idx(x, ay);
56	  const style = doorStyleOf(st.frameX[ai], st.frameY[ai]);
57	  const col = Math.floor(style / 36), row = style % 36;
58	  // 目标侧列须为空（原版只砍草藤类，这里保守要求空格）
59	  const clearX = direction === -1 ? x - 1 : x + 1;
60	  for (let dy = 0; dy < 3; dy++) {
61	    if (st.get(clearX, ay + dy) !== 0) return false;
62	  }
63	  // 开门占 2 列：direction==-1 锚点左移一格、frameX+36（原版 num1/x 逻辑）
64	  const ax = direction === -1 ? x - 1 : x;
65	  const baseFx = 72 * col + (direction === -1 ? 36 : 0);
66	  for (let dx = 0; dx < 2; dx++) {
67	    for (let dy = 0; dy < 3; dy++) {
68	      if (!st.inBounds(ax + dx, ay + dy)) continue;
69	      st.setTile(ax + dx, ay + dy, T.DOOR_OPEN, baseFx + dx * 18, 54 * row + dy * 18);
70	    }
71	  }
72	  return true;
73	}
74	
75	/** 关门（原版 CloseDoor 语义，点到的可以是开门 2×3 中任意一格）。
76	 *  blocked = 实体占格判定（原版 Collision.EmptyTile(ignoreTiles:true)：只看玩家/NPC，忽略图格——
77	 *  关门列此刻还是开门图格）。返回 false = 门位被实体挡住。 */
78	export function closeDoor(st: TileStore, x: number, y: number, rng: () => number = Math.random, blocked?: (x: number, y: number) => boolean): boolean {
79	  if (st.get(x, y) !== T.DOOR_OPEN) return false;
80	  // 锚点行：frameY % 54 === 0
81	  let ay = y;
82	  while (st.get(x, ay) === T.DOOR_OPEN && st.frameY[st.idx(x, ay)] % 54 !== 0) {
83	    if (--ay < 0) return false;
84	  }
85	  if (st.get(x, ay) !== T.DOOR_OPEN) return false;
86	  const fx = st.frameX[st.idx(x, ay)];
87	  // 原版 switch(frameX % 72)：关门列与开门方向
88	  let closedX: number;
89	  switch (fx % 72) {
90	    case 18: closedX = x - 1; break;   // 点到右侧列 → 锚点在左
91	    case 36: closedX = x + 1; break;   // direction==-1 的锚点列
92	    case 54: closedX = x; break;       // direction==-1 的右侧列
93	    default: closedX = x; break;       // 0：direction==+1 锚点列
94	  }
95	  // 关门位实体检查（原版 Collision.EmptyTile(ignoreTiles:true)：图格忽略，只挡实体）
96	  for (let dy = 0; dy < 3; dy++) {
97	    if (blocked?.(closedX, ay + dy)) return false;
98	  }
99	  // 样式行先取（清格后 frameY 归零；原版关门不重写 frameY，样式行开门/关门一致）
100	  const col = Math.floor(fx / 72);
101	  const row = Math.floor(st.frameY[st.idx(x, ay)] / 54) % 36;
102	  // 清两列再写关门列（原版 num6..num6+1 循环）
103	  const sweepL = Math.min(closedX, x - 1), sweepR = Math.max(closedX + 1, x + 1);
104	  for (let sx = sweepL; sx <= sweepR; sx++) {
105	    for (let dy = 0; dy < 3; dy++) {
106	      if (!st.inBounds(sx, ay + dy)) continue;
107	      st.setTile(sx, ay + dy, 0);
108	    }
109	  }
110	  const [cfx] = doorClosedFrame(col * 36, Math.floor(rng() * 3));
111	  for (let dy = 0; dy < 3; dy++) {
112	    if (!st.inBounds(closedX, ay + dy)) continue;
113	    st.setTile(closedX, ay + dy, T.DOOR_CLOSED, cfx, 54 * row + dy * 18);
114	  }
115	  return true;
116	}
117	

```


---

## 🤖 Assistant · 2026-08-09T10:49:00.849Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now Renderer.ts and Input.ts and LiquidSim.ts and Dart.ts and constants.ts. Also WldImport.ts (how tiles from WldParser map into TileStore — wire data discarded there). Let me read those in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:49:00.850Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "limit": 400
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:00.856Z

**📎 ToolResult**

```
1	// 主渲染器：天空 → chunk → 液体 → 实体 → 粒子/飘字 → 光照合成 → 小地图
2	import { TILE, CHUNK } from '../core/constants';
3	import type { Camera } from './Camera';
4	import { SkyRenderer } from './SkyRenderer';
5	import { ChunkCache } from './ChunkCache';
6	import type { World, Clock } from '../world/World';
7	import type { AssetBundle } from '../assets/AssetGen';
8	import type { SpriteAtlas } from '../assets/SpriteAtlas';
9	import { atlasIconForKey } from '../assets/SpriteAtlas';
10	import { drawVanillaLiquids } from './VanillaLiquidRenderer';
11	import { WaterfallRenderer } from './WaterfallRenderer';
12	import { TILE_DEFS, WALL_DEFS } from '../data/tiles';
13	import { ITEM_DEFS } from '../data/items';
14	import type { Player } from '../entities/Player';
15	import { Enemy } from '../entities/Enemy';
16	import { ItemDrop } from '../entities/ItemDrop';
17	import { TownNPC } from '../entities/TownNPC';
18	import { Tombstone, getTombstoneCanvas } from '../entities/Tombstone';
19	import { Critter } from '../entities/Critter';
20	import type { Entity } from '../entities/Entity';
21	
22	export interface Particle { x: number; y: number; vx: number; vy: number; life: number; maxLife: number; color: string; size: number; damp?: number; grav?: number; }
23	export interface DamageNumber { x: number; y: number; vy: number; value: number; crit: boolean; color: string; life: number; label?: string; }
24	
25	export class Minimap {
26	  canvas: HTMLCanvasElement;
27	  ctx: CanvasRenderingContext2D;
28	  dirtyChunks = new Set<number>();
29	  constructor(public world: World) {
30	    this.canvas = document.createElement('canvas');
31	    this.canvas.width = world.w;
32	    this.canvas.height = world.h;
33	    this.ctx = this.canvas.getContext('2d')!;
34	    this.redrawAll();
35	    world.store.onTileChanged((x, y) => {
36	      this.dirtyChunks.add(ChunkCache.key(Math.floor(x / CHUNK), Math.floor(y / CHUNK)));
37	    });
38	  }
39	
40	  colorFor(x: number, y: number): string | null {
41	    const st = this.world.store;
42	    const i = st.idx(x, y);
43	    if (st.type[i] !== 0) {
44	      const d = TILE_DEFS[st.type[i]];
45	      return d ? d.mapColor : '#808080';
46	    }
47	    // 液体：水蓝 / 岩浆橙
48	    if (st.liquid[i] > 40) return st.liquidType[i] === 2 ? '#E8622C' : '#3D6FD1';
49	    if (st.wall[i] !== 0) {
50	      // 墙色 = 深化（地下洞穴空气）
51	      const w = st.wall[i];
52	      return WALL_DEFS[w]?.mapColor ?? '#2E2E2E'; // 全量权威墙色（TEdit walls.json）
53	    }
54	    // 探索过的天空 = 亮蓝（未探索区域由迷雾层另盖黑）
55	    return '#7EB6E8';
56	  }
57	
58	  redrawAll() {
59	    const { world, ctx } = this;
60	    const img = ctx.createImageData(world.w, world.h);
61	    for (let y = 0; y < world.h; y++) {
62	      for (let x = 0; x < world.w; x++) {
63	        const c = this.colorFor(x, y);
64	        const i = (y * world.w + x) * 4;
65	        if (c) {
66	          const v = parseInt(c.slice(1), 16);
67	          img.data[i] = (v >> 16) & 255; img.data[i + 1] = (v >> 8) & 255; img.data[i + 2] = v & 255;
68	        }
69	        img.data[i + 3] = 255;
70	      }
71	    }
72	    ctx.putImageData(img, 0, 0);
73	    this.dirtyChunks.clear();
74	  }
75	
76	  flushDirty() {
77	    if (this.dirtyChunks.size === 0) return;
78	    const st = this.world.store;
79	    let n = 0;
80	    for (const k of this.dirtyChunks) {
81	      if (n++ > 24) break;
82	      this.dirtyChunks.delete(k);
83	      const cx = (k & 0xffff) << 16 >> 16, cy = (k >> 16) << 16 >> 16;
84	      const x0 = cx * CHUNK, y0 = cy * CHUNK;
85	      for (let y = y0; y < y0 + CHUNK; y++) {
86	        for (let x = x0; x < x0 + CHUNK; x++) {
87	          if (!st.inBounds(x, y)) continue;
88	          const c = this.colorFor(x, y);
89	          this.ctx.fillStyle = c ?? '#000';
90	          this.ctx.fillRect(x, y, 1, 1);
91	        }
92	      }
93	    }
94	  }
95	}
96	
97	export class Renderer {
98	  /** 调试面板开关（F3 切换）：碰撞盒高亮等 */
99	  debugMode = false;
100	  /** 方块标注（F5 标注模式）：标记的问题方块，非空时叠加绘制 */
101	  annotateMarks: Array<{ x: number; y: number }> | null = null;
102	  canvas: HTMLCanvasElement;
103	  ctx: CanvasRenderingContext2D;
104	  sky = new SkyRenderer();
105	  lightCanvas: HTMLCanvasElement;
106	  lightCtx: CanvasRenderingContext2D;
107	  minimap: Minimap | null = null;
108	  /** 原版瀑布贴图系统（WaterfallManager 移植）：液体倾泻的长条水流柱 */
109	  waterfalls = new WaterfallRenderer();
110	
111	  // 全屏地图查看器状态（zoom 向 zoomTarget 缓动；缓动期间按锚点补偿 pan）
112	  fullMap = {
113	    open: false, zoom: 0.5, zoomTarget: 0.5, panX: 0, panY: 0,
114	    anchorU: 0, anchorV: 0, anchorMX: 0, anchorMY: 0,
115	  };
116	
117	  /** 全屏地图缩放：以鼠标位置为锚点（鼠标下的地图点不动，不乱飞） */
118	  zoomFullMapAt(newZoom: number, mouseX: number, mouseY: number) {
119	    const fm = this.fullMap;
120	    const viewW = this.canvas.width, viewH = this.canvas.height;
121	    const clamped = Math.max(0.5, Math.min(6, newZoom));
122	    // 记录锚点：鼠标下的地图源坐标 + 鼠标屏幕位置。
123	    // 缓动期间每帧按公式 pan = anchorMX - viewW/2 + W*zoom/2 - u*zoom 重解，
124	    // 保证缓动全程锚点不动（否则缓动中 pan 固定会让地图"自己跑"）
125	    const cx0 = viewW / 2 - (this._fmWorldW * fm.zoom) / 2 + fm.panX;
126	    const cy0 = viewH / 2 - (this._fmWorldH * fm.zoom) / 2 + fm.panY;
127	    fm.anchorU = (mouseX - cx0) / fm.zoom;
128	    fm.anchorV = (mouseY - cy0) / fm.zoom;
129	    fm.anchorMX = mouseX;
130	    fm.anchorMY = mouseY;
131	    fm.zoomTarget = clamped;
132	    this.applyMapAnchor();
133	  }
134	
135	  /** 按锚点反解 pan（当前 zoom 下鼠标处的地图点固定在鼠标下） */
136	  private applyMapAnchor() {
137	    const fm = this.fullMap;
138	    const viewW = this.canvas.width, viewH = this.canvas.height;
139	    fm.panX = fm.anchorMX - viewW / 2 + (this._fmWorldW * fm.zoom) / 2 - fm.anchorU * fm.zoom;
140	    fm.panY = fm.anchorMY - viewH / 2 + (this._fmWorldH * fm.zoom) / 2 - fm.anchorV * fm.zoom;
141	  }
142	
143	  /** 每帧缓动 fullMap.zoom → zoomTarget；缓动期间同步按锚点补偿 pan */
144	  easeFullMap() {
145	    const fm = this.fullMap;
146	    const diff = fm.zoomTarget - fm.zoom;
147	    if (Math.abs(diff) < 0.002) { fm.zoom = fm.zoomTarget; return; }
148	    fm.zoom += diff * 0.16;
149	    this.applyMapAnchor();
150	  }
151	  private _fmWorldW = 0;
152	  private _fmWorldH = 0;
153	  minimapRect = { x: 0, y: 0, w: 0, h: 0 };
154	  private mapDragging = false;
155	  private lastMouse = { x: 0, y: 0 };
156	
157	  constructor(public assets: AssetBundle, public atlas: SpriteAtlas | null = null) {
158	    this.canvas = document.createElement('canvas');
159	    this.ctx = this.canvas.getContext('2d')!;
160	    this.lightCanvas = document.createElement('canvas');
161	    this.lightCtx = this.lightCanvas.getContext('2d')!;
162	    window.addEventListener('resize', () => this.resize());
163	    this.resize();
164	  }
165	
166	  /** 物品图标：优先 Maples 素材，缺省回退程序化 */
167	  itemIcon(id: number): HTMLCanvasElement | null {
168	    return this.assets.itemIcons.get(id) ?? null;
169	  }
170	
171	  /** Maples 图标绘制矩形（找不到返回 null） */
172	  atlasIcon(id: number) {
173	    if (!this.atlas) return null;
174	    const def = ITEM_DEFS[id];
175	    if (!def) return null;
176	    return atlasIconForKey(this.atlas, def.key);
177	  }
178	
179	  resize() {
180	    this.canvas.width = window.innerWidth;
181	    this.canvas.height = window.innerHeight;
182	  }
183	
184	  attach(parent: HTMLElement) {
185	    parent.appendChild(this.canvas);
186	  }
187	
188	  private _mouseX = 0;
189	  private _mouseY = 0;
190	  private _mouseDown = false;
191	
192	  render(
193	    cam: Camera, world: World, clock: Clock,
194	    chunks: ChunkCache,
195	    lightR: Uint8Array, lightG: Uint8Array, lightB: Uint8Array,
196	    lightRX: number, lightRY: number, lightRW: number, lightRH: number,
197	    player: Player, entities: Entity[],
198	    particles: Particle[], dmgNumbers: DamageNumber[],
199	    swing: { t: number; dur: number; item: number } | null,
200	    hover: { x: number; y: number } | null,
201	    boss: { name: string; hp: number; maxHp: number } | null,
202	    mouseX = 0, mouseY = 0, mouseDown = false,
203	    mineProgress = 0,
204	  ) {
205	    this._mouseX = mouseX;
206	    this._mouseY = mouseY;
207	    this._mouseDown = mouseDown;
208	    this._liquidNow = performance.now(); // 帧 first thing 采样：背景水/瀑布/前景水共用同一时刻
209	    this.easeFullMap();
210	    const ctx = this.ctx;
211	    const viewW = this.canvas.width, viewH = this.canvas.height;
212	    cam.viewW = viewW; cam.viewH = viewH;
213	    const z = cam.zoom;
214	
215	    // 1. 天空
216	    this.sky.draw(ctx, clock, viewW, viewH, cam.x);
217	
218	    ctx.save();
219	    // 世界变换：平移 + 缩放（以屏幕中心为相机中心）
220	    // 像素风关键：tile/实体用最近邻采样保持锐利（光照层单独用平滑）
221	    ctx.imageSmoothingEnabled = false;
222	    ctx.translate(viewW / 2, viewH / 2);
223	    ctx.scale(z, z);
224	    ctx.translate(-cam.x, -cam.y);
225	
226	    // 2. chunks 绘制序列（对照原版 Main.cs 帧序：背景水 → 墙 → 方块 → 瀑布 → 实体 → 前景水）
227	    const ts = TILE;
228	    const x0 = Math.floor((cam.x - viewW / 2 / z) / (CHUNK * ts)) - 1;
229	    const x1 = Math.floor((cam.x + viewW / 2 / z) / (CHUNK * ts)) + 1;
230	    const y0 = Math.floor((cam.y - viewH / 2 / z) / (CHUNK * ts)) - 1;
231	    const y1 = Math.floor((cam.y + viewH / 2 / z) / (CHUNK * ts)) + 1;
232	    const chunkVisible = (cx: number, cy: number) =>
233	      cx >= 0 && cy >= 0 && cx * CHUNK < world.w && cy * CHUNK < world.h;
234	    // 2a. 液体背景 pass（原版 backWaterTarget 先于墙合成，Main.cs:46619）：
235	    //     不透明水画在墙/方块之前——方块贴图透明像素处露出这层水 = 浸润，
236	    //     有墙的水格由墙盖住、只留前景 0.6 层 → 墙在水中可见
237	    this.drawLiquids(world, cam, viewW, viewH, z, true);
238	
239	    // 2b. 背景墙层
240	    for (let cy = y0; cy <= y1; cy++) {
241	      for (let cx = x0; cx <= x1; cx++) {
242	        if (!chunkVisible(cx, cy)) continue;
243	        ctx.drawImage(chunks.get(cx, cy).wall, cx * CHUNK * ts, cy * CHUNK * ts);
244	      }
245	    }
246	
247	    // 2c. 前景 tile/物体层
248	    for (let cy = y0; cy <= y1; cy++) {
249	      for (let cx = x0; cx <= x1; cx++) {
250	        if (!chunkVisible(cx, cy)) continue;
251	        ctx.drawImage(chunks.get(cx, cy).tile, cx * CHUNK * ts, cy * CHUNK * ts);
252	      }
253	    }
254	
255	    // 2d. 瀑布贴图（原版画在 tile 层后、实体前，Main.cs:47460，被地形遮挡）
256	    this.drawWaterfalls(world, cam, viewW, viewH, z);
257	
258	    // 4. 实体（按 y 排序）
259	    const sorted = [...entities].sort((a, b) => a.y - b.y);
260	    for (const e of sorted) {
261	      if (e instanceof Enemy) this.drawEnemy(e, world);
262	      else if (e instanceof ItemDrop) this.drawDrop(e);
263	      else if (e instanceof TownNPC) this.drawTownNPC(e);
264	      else if (e instanceof Tombstone) this.drawTombstone(e);
265	      else if (e instanceof Critter) this.drawCritter(e);
266	      else (e as Player).draw && null;
267	    }
268	    this.drawPlayer(player, world, swing);
269	
270	    // 4.5 液体前景 pass（原版 waterTarget 在玩家/掉落物之后合成，Main.cs:46720）：
271	    //     水 0.6 半透明盖在实体上——水中角色带水色
272	    this.drawLiquids(world, cam, viewW, viewH, z, false);
273	
274	    // 5. 粒子
275	    for (const p of particles) {
276	      ctx.globalAlpha = Math.max(0, p.life / p.maxLife);
277	      ctx.fillStyle = p.color;
278	      ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
279	    }
280	    ctx.globalAlpha = 1;
281	
282	    // 6. 挖掘/放置光标：挖掘中黄色填充随进度加深（半透明黄 → 破坏完成时最深）
283	    if (hover) {
284	      ctx.strokeStyle = 'rgba(255,255,255,0.7)';
285	      ctx.lineWidth = 1 / z;
286	      ctx.strokeRect(hover.x * ts + 0.5, hover.y * ts + 0.5, ts - 1, ts - 1);
287	      if (mineProgress > 0) {
288	        // 进度 0→1，黄色 alpha 0.15→0.8 加深渐变（接近破坏时深黄）
289	        ctx.globalAlpha = 0.15 + Math.min(1, mineProgress) * 0.65;
290	        ctx.fillStyle = '#FFC419';
291	        ctx.fillRect(hover.x * ts + 1, hover.y * ts + 1, ts - 2, ts - 2);
292	        ctx.globalAlpha = 1;
293	      }
294	    }
295	
296	    ctx.restore();
297	
298	    // 7. 光照合成
299	    this.compositeLight(cam, viewW, viewH, lightR, lightG, lightB, lightRX, lightRY, lightRW, lightRH);
300	
301	    // 8. 飘字（受光照影响后画）
302	    ctx.save();
303	    ctx.font = 'bold 14px monospace';
304	    ctx.textAlign = 'center';
305	    for (const d of dmgNumbers) {
306	      ctx.globalAlpha = Math.min(1, d.life / 30);
307	      const [sx, sy] = cam.worldToScreen(d.x, d.y);
308	      // 物品名飘字：带阴影浅白文本
309	      if (d.label) {
310	        ctx.font = '13px sans-serif';
311	        ctx.strokeStyle = 'rgba(0,0,0,0.75)';
312	        ctx.lineWidth = 3;
313	        ctx.strokeText(d.label, sx, sy);
314	        ctx.fillStyle = '#F0F0F0';
315	        ctx.fillText(d.label, sx, sy);
316	        continue;
317	      }
318	      ctx.fillStyle = d.color;
319	      ctx.font = d.crit ? 'bold 18px monospace' : 'bold 14px monospace';
320	      ctx.strokeStyle = '#000';
321	      ctx.lineWidth = 3;
322	      ctx.strokeText(String(d.value), sx, sy);
323	      ctx.fillText(String(d.value), sx, sy);
324	    }
325	    ctx.restore();
326	
327	    this._lastPlayer = player;
328	    // 9. 小地图
329	    this.drawMinimap(ctx, cam, world, player, clock);
330	    // 9.5 全屏地图
331	    if (this.fullMap.open && this.minimap) {
332	      this.drawFullMap(ctx, world, this._mouseX, this._mouseY, this._mouseDown);
333	      return; // 全屏地图时跳过其余 HUD
334	    }
335	
336	    // 9.8 调试面板：碰撞盒高亮（F3 切换）
337	    // 方块标注叠加（F5 标注模式）：红圈 + 序号
338	    if (this.annotateMarks && this.annotateMarks.length && !this.fullMap.open) {
339	      const z = cam.zoom;
340	      ctx.save();
341	      ctx.font = `bold ${Math.max(10, 12 * z)}px monospace`;
342	      ctx.textAlign = 'center';
343	      this.annotateMarks.forEach((m, idx) => {
344	        const [sx, sy] = cam.worldToScreen(m.x * TILE + TILE / 2, m.y * TILE + TILE / 2);
345	        ctx.strokeStyle = '#FF3355';
346	        ctx.lineWidth = 2;
347	        ctx.beginPath();
348	        ctx.arc(sx, sy, 10 * z + 4, 0, Math.PI * 2);
349	        ctx.stroke();
350	        ctx.fillStyle = '#FF3355';
351	        ctx.fillText(String(idx + 1), sx, sy - 12 * z - 6);
352	      });
353	      ctx.restore();
354	    }
355	    if (this.debugMode) this.drawDebugOverlay(ctx, cam, viewW, viewH, player, entities, mouseX, mouseY, hover);
356	
357	    // 10. Boss 血条
358	    if (boss) this.drawBossBar(ctx, viewW, boss);
359	
360	    // 11. HP 显示
361	    this.drawHp(ctx, player);
362	  }
363	
364	  private drawLiquids(world: World, cam: Camera, viewW: number, viewH: number, z: number, isBackground: boolean) {
365	    // 原版 1.4.0.5 LiquidRenderer 移植（多 pass 网格算法，见 VanillaLiquidRenderer）。
366	    // isBackground：背景 pass（墙层之前，不透明）或前景 pass（实体之后，0.6）
367	    const ts = TILE;
368	    const tx0 = Math.max(2, Math.floor((cam.x - viewW / 2 / z) / ts));
369	    const tx1 = Math.min(world.w - 3, Math.ceil((cam.x + viewW / 2 / z) / ts));
370	    const ty0 = Math.max(2, Math.floor((cam.y - viewH / 2 / z) / ts));
371	    // 底边 +5 行（原版 Main.cs:42900-42908 屏下 +5/+4 边距）：P3 不处理窗口底部 10 行，
372	    // 外扩后未构建带落在屏幕外，防止视口底缘液体类型错画
373	    const ty1 = Math.min(world.h - 3, Math.ceil((cam.y + viewH / 2 / z) / ts) + 5);
374	    // 双 pass 共用同一时刻，避免动画帧错位（原版 PrepareDraw 每帧一次、两 pass 共享缓存）
375	    drawVanillaLiquids(this.ctx, this.atlas, world.store, world.groundLevel, tx0, ty0, tx1, ty1, this._liquidNow, isBackground);
376	  }
377	
378	  /** 瀑布贴图（tile 层后、实体前；扫描窗口外扩 100 格在内部，30 帧节流） */
379	  private drawWaterfalls(world: World, cam: Camera, viewW: number, viewH: number, z: number) {
380	    if (!this.atlas) return;
381	    const ts = TILE;
382	    const tx0 = Math.max(2, Math.floor((cam.x - viewW / 2 / z) / ts));
383	    const tx1 = Math.min(world.w - 3, Math.ceil((cam.x + viewW / 2 / z) / ts));
384	    const ty0 = Math.max(2, Math.floor((cam.y - viewH / 2 / z) / ts));
385	    const ty1 = Math.min(world.h - 3, Math.ceil((cam.y + viewH / 2 / z) / ts));
386	    const now = this._liquidNow; // 与液体双 pass 同帧同时刻
387	    this.waterfalls.findWaterfalls(world.store, tx0, ty0, tx1, ty1, Math.floor(now / 16.67));
388	    this.waterfalls.draw(this.ctx, this.atlas, world.store, world.groundLevel, now);
389	  }
390	  /** 本帧液体动画时刻（双 pass 共享） */
391	  private _liquidNow = 0;
392	
393	  /** 墓碑：以底部中心为支点按倾角旋转绘制（翻滚/侧躺/倒扣）。
394	   *  优先原版 Tiles_85 样式块——四格 16×16 无缝拼到离屏画布再绘制
395	   *  （直接取 34×34 矩形会把表内 2px 间隙画成十字缝），程序化仅兜底 */
396	  private tombstoneCache = new Map<number, HTMLCanvasElement>();
397	  private drawTombstone(t: Tombstone) {
398	    const ctx = this.ctx;
399	    ctx.save();
400	    ctx.translate(t.cx, t.y + t.h);

```


---

## 🤖 Assistant · 2026-08-09T10:49:00.857Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Input.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:00.865Z

**📎 ToolResult**

```
1	// 键盘/鼠标输入。UI 打开时屏蔽游戏输入。
2	export class Input {
3	  keys = new Set<string>();
4	  mouseX = 0; mouseY = 0;
5	  mouseDown = false;
6	  rightDown = false;
7	  uiBlocking = false;     // 背包/合成等打开时为 true
8	  wheelDelta = 0;
9	  keydownHandlers: Array<(code: string) => void> = [];
10	
11	  private el: HTMLElement;
12	
13	  constructor(el: HTMLElement) {
14	    this.el = el;
15	    window.addEventListener('keydown', (e) => {
16	      if (e.repeat) return;
17	      this.keys.add(e.code);
18	      this.keydownHandlers.forEach((fn) => fn(e.code));
19	      if (['Space', 'ArrowUp', 'ArrowDown', 'Tab'].includes(e.code)) e.preventDefault();
20	    });
21	    window.addEventListener('keyup', (e) => this.keys.delete(e.code));
22	    window.addEventListener('blur', () => this.keys.clear());
23	    el.addEventListener('mousemove', (e) => {
24	      const r = this.el.getBoundingClientRect();
25	      this.mouseX = e.clientX - r.left;
26	      this.mouseY = e.clientY - r.top;
27	    });
28	    // mousedown 挂 window：不依赖事件目标是否恰好是 canvas
29	    window.addEventListener('mousedown', (e) => {
30	      // UI 面板上的点击不穿透为游戏输入
31	      if ((e.target as HTMLElement)?.closest?.('.sw-panel, .sw-slot, .sw-recipe, .sw-btn')) return;
32	      if (e.button === 0) this.mouseDown = true;
33	      if (e.button === 2) this.rightDown = true;
34	    });
35	    window.addEventListener('mouseup', (e) => {
36	      if (e.button === 0) this.mouseDown = false;
37	      if (e.button === 2) this.rightDown = false;
38	    });
39	    el.addEventListener('contextmenu', (e) => e.preventDefault());
40	    el.addEventListener('wheel', (e) => {
41	      this.wheelDelta += Math.sign(e.deltaY);
42	      e.preventDefault();
43	    }, { passive: false });
44	  }
45	
46	  down(code: string): boolean {
47	    return !this.uiBlocking && this.keys.has(code);
48	  }
49	
50	  /** 每帧末调用，处理一次性输入（滚轮切换快捷栏） */
51	  endFrame() {
52	    this.wheelDelta = 0;
53	  }
54	}
55	

```


---

## 🤖 Assistant · 2026-08-09T10:49:03.400Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I need: where F3/F5/F8 are registered (probably in UI.ts or main.ts/mainFlow.ts). Let me grep for F5/F8/F3 keybindings. Also WldImport.ts (mapping of parsed tiles to TileStore). Also LiquidSim basics (pump integration), Dart.ts, constants.ts, Entity.ts (entities.add, buckets), tiles.ts structure (TileDef fields), and the rest of items.ts (place_ items etc.).
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:49:04.099Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"F3\\|F5\\|F8\\|F2\\|F4\\|F6\\|F7\\|F9\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | grep -v \"worldgenKeys\" | head -50",
 "description": "Find F-key shortcut registrations"
}
```


---

## 🤖 Assistant · 2026-08-09T10:49:04.106Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/wld/WldImport.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:04.132Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-09T10:49:04.158Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:04.166Z

**📎 ToolResult**

```
1	// 飞镖投射物(原版 Projectile 10 Dart 语义:直线飞行、撞块消失、命中伤害)。
2	// 陷阱(137)发射;简化布线:同排/同列直线可见(≤60 格无实心阻挡)的拉杆/开关/压力板驱动。
3	import { Entity } from './Entity';
4	import { TILE } from '../core/constants';
5	import type { GameHooks } from './types';
6	import type { Renderer } from '../render/Renderer';
7	import type { Camera } from '../render/Camera';
8	
9	export class Dart extends Entity {
10	  w = 8; h = 4;
11	  vx: number;
12	  vy: number;
13	  damage: number;
14	  life = 600; // tick 上限(原版 timeLeft 600)
15	  dead = false;
16	
17	  constructor(x: number, y: number, vx: number, vy: number, damage: number) {
18	    super();
19	    this.x = x; this.y = y;
20	    this.vx = vx; this.vy = vy;
21	    this.damage = damage;
22	  }
23	
24	  draw(r: Renderer, cam: Camera): void {
25	    const ctx = r.canvas.getContext('2d');
26	    if (!ctx) return;
27	    const x = (this.x - cam.x) * cam.zoom + r.canvas.width / 2;
28	    const y = (this.y - cam.y) * cam.zoom + r.canvas.height / 2;
29	    ctx.fillStyle = '#C8B89A';
30	    ctx.fillRect(x, y, this.w * cam.zoom, this.h * cam.zoom);
31	  }
32	
33	  fixedUpdate(_dt: number, game: GameHooks) {
34	    if (--this.life <= 0) { this.dead = true; return; }
35	    const world = game.world;
36	    this.x += this.vx;
37	    this.y += this.vy;
38	    // 撞实心块消失
39	    const tx = Math.floor((this.x + this.w / 2) / TILE);
40	    const ty = Math.floor((this.y + this.h / 2) / TILE);
41	    if (world.store.isSolid(tx, ty)) { this.dead = true; return; }
42	    // 命中玩家(敌对陷阱):矩形相交
43	    const p = game.player;
44	    if (!p.dead && this.x < p.x + p.w && this.x + this.w > p.x && this.y < p.y + p.h && this.y + this.h > p.y) {
45	      p.damage(this.damage, this.x, this.y);
46	      game.addDamageNumber(p.cx, p.y, this.damage, false, '#FF8060');
47	      this.dead = true;
48	    }
49	  }
50	}
51	

```


---

## 👤 User(sidechain) · 2026-08-09T10:49:04.314Z

**📎 ToolResult**

```
1	// .wld → 自有存档格式转换（导入后即可进入游戏）
2	// tile/wall/item 的 id 映射基于 Terraria 1.4 的事实数据；未映射内容做可玩性降级。
3	import { parseWld, WldWorld } from './WldParser';
4	import { SaveData, rleTiles, rlePairs, bytesToB64 } from '../save/SaveFile';
5	import { TILE_BY_KEY, T } from '../data/tiles';
6	import { ITEM_BY_KEY } from '../data/items';
7	
8	// wld tile id → 内部 tile key（null = 清空丢弃；copyFrame = 原版 framed 家具，18px 帧直拷）
9	type MapEntry = string | { key: string; copyFrame?: boolean } | null;
10	const TILE_MAP: Record<number, MapEntry> = {
11	  0: 'dirt',          // Dirt
12	  1: 'stone',         // Stone
13	  2: 'grass',         // Grass
14	  3: { key: 'v_3_forest_short_plants', copyFrame: true },  // Plants（花草杂草变体帧直拷）
15	  4: { key: 'torch', copyFrame: true },  // Torch（保留原版墙面/熄灭变体帧）
16	  5: { key: 'v_5_trees', copyFrame: true },  // Tree（原版 Tiles_5，22px 步长样式帧直拷）
17	  6: 'ore_iron',      // Iron
18	  7: 'ore_copper',    // Copper
19	  8: 'ore_gold',      // Gold
20	  9: 'ore_silver',    // Silver
21	  10: { key: 'door_closed', copyFrame: true },  // Closed Door（原版变体帧）
22	  16: 'anvil',        // Anvil
23	  17: 'anvil',        // Mythril Anvil
24	  18: 'workbench',    // Work Bench
25	  19: { key: 'platform', copyFrame: true },  // Wood Platform（原版帧直拷）
26	  21: 'chest',  // Chest（帧按格距重建，不直拷——wld 存的是格偏移 0/1 不是像素）
27	  53: 'sand',         // Sand
28	  59: 'mud',          // Mud
29	  73: { key: 'v_73_forest_tall_plants', copyFrame: true },  // Plants 2（高草，16×32 帧）
30	  147: 'snow',        // Snow
31	  // ---- 原版素材批次（Tiles_N 表 + TEdit framing） ----
32	  57: 'ash', 123: 'silt', 40: 'clay', 54: 'glass', 56: 'obsidian',
33	  38: 'gray_brick', 39: 'red_brick',
34	  161: 'ice', 162: 'thin_ice', 206: 'ice_brick', 148: 'snow_brick',
35	  396: 'sandstone', 397: 'hardened_sand', 404: 'desert_fossil',
36	  166: 'ore_tin', 167: 'ore_lead', 168: 'ore_tungsten', 169: 'ore_platinum',
37	  22: 'ore_demonite', 37: 'ore_meteorite', 58: 'ore_hellstone', 204: 'ore_crimtane',
38	  107: 'ore_cobalt', 108: 'ore_mythril', 111: 'ore_adamantite',
39	  221: 'ore_palladium', 222: 'ore_orichalcum', 223: 'ore_titanium', 211: 'ore_chlorophyte',
40	  63: 'gem_sapphire', 64: 'gem_ruby', 65: 'gem_emerald',
41	  66: 'gem_topaz', 67: 'gem_amethyst', 68: 'gem_diamond',
42	  // 家具（framed：18px 帧/样式直拷，渲染端原样使用）
43	  14: { key: 'table', copyFrame: true },
44	  15: { key: 'chair', copyFrame: true },
45	  79: { key: 'bed', copyFrame: true },
46	  33: { key: 'candle', copyFrame: true },
47	  34: { key: 'chandelier', copyFrame: true },
48	  42: { key: 'lantern', copyFrame: true },
49	  100: { key: 'candelabra', copyFrame: true },
50	  101: { key: 'bookcase', copyFrame: true },
51	  104: { key: 'grandfather_clock', copyFrame: true },
52	  87: { key: 'piano', copyFrame: true },
53	  88: { key: 'dresser', copyFrame: true },
54	  89: { key: 'bench', copyFrame: true },
55	  90: { key: 'bathtub', copyFrame: true },
56	  94: { key: 'keg', copyFrame: true },
57	  95: { key: 'chinese_lantern', copyFrame: true },
58	  96: { key: 'cooking_pot', copyFrame: true },
59	  98: { key: 'skull_lantern', copyFrame: true },
60	  78: { key: 'clay_pot', copyFrame: true },
61	  85: { key: 'tombstone_v', copyFrame: true },
62	  12: { key: 'crystal_heart', copyFrame: true },
63	  49: { key: 'water_candle', copyFrame: true },
64	  // 降级为 stone 的常见方块
65	  // ---- 全量补全（compat-report 驱动，187 种）----
66	  165: { key: 'v_165_cave_decos', copyFrame: true },  // Cave Decos
67	  51: 'v_51_cobweb',  // Cobweb
68	  368: 'v_368_granite_block',  // Granite Block
69	  226: 'v_226_lihzahrd_brick',  // Lihzahrd Brick
70	  367: 'v_367_marble_block',  // Marble Block
71	  184: { key: 'v_184_moss_plants', copyFrame: true },  // Moss Plants
72	  633: 'v_633_ash_grass_block',  // Ash Grass Block
73	  181: 'v_181_red_moss_block',  // Red Moss Block
74	  189: 'v_189_cloud_block',  // Cloud Block
75	  183: 'v_183_purple_moss_block',  // Purple Moss Block
76	  536: 'v_536_xenon_moss_block',  // Xenon Moss Block
77	  225: 'v_225_hive_block',  // Hive Block
78	  483: 'v_483_cracked_pink_brick',  // Cracked Pink Brick
79	  638: 'v_638_ash_vines',  // Ash Vines
80	  224: 'v_224_slush_block',  // Slush Block
81	  383: 'v_383_living_mahogany_block',  // Living Mahogany Block
82	  179: 'v_179_green_moss_block',  // Green Moss Block
83	  314: { key: 'v_314_minecart_track', copyFrame: true },  // Minecart Track
84	  384: 'v_384_living_mahogany_leaves_block',  // Living Mahogany Leaves Block
85	  185: { key: 'v_185_small_decos', copyFrame: true },  // Small Decos
86	  373: { key: 'v_373_water_drip', copyFrame: true },  // Water Drip
87	  273: 'v_273_stone_slab',  // Stone Slab
88	  187: { key: 'v_187_decos_3x2_group_2', copyFrame: true },  // Decos (3x2) (Group 2)
89	  484: { key: 'v_484_rolling_cactus', copyFrame: true },  // Rolling Cactus
90	  374: { key: 'v_374_lava_drip', copyFrame: true },  // Lava Drip
91	  381: 'v_381_lava_moss',  // Lava Moss
92	  48: 'v_48_spike',  // Spike
93	  192: 'v_192_living_leaf_block',  // Living Leaf Block
94	  191: 'v_191_living_wood_block',  // Living Wood Block
95	  233: { key: 'v_233_jungle_large_plants', copyFrame: true },  // Jungle Large Plants
96	  528: 'v_528_mushroom_vines',  // Mushroom Vines
97	  105: { key: 'v_105_statue', copyFrame: true },  // Statue
98	  186: { key: 'v_186_decos_3x2', copyFrame: true },  // Decos (3x2)
99	  196: 'v_196_rain_cloud_block',  // Rain Cloud Block
100	  461: { key: 'v_461_sand_drip', copyFrame: true },  // Sand Drip
101	  382: 'v_382_flower_vines',  // Flower Vines
102	  178: { key: 'v_178_gems', copyFrame: true },  // Gems
103	  118: 'v_118_pearlstone_brick',  // Pearlstone Brick
104	  485: { key: 'v_485_antlion_larva', copyFrame: true },  // Antlion Larva
105	  321: 'v_321_boreal_wood',  // Boreal Wood
106	  637: { key: 'v_637_ash_short_plants', copyFrame: true },  // Ash Short Plants
107	  444: { key: 'v_444_bee_hive', copyFrame: true },  // Bee Hive
108	  240: { key: 'v_240_wall_hangings_3x3', copyFrame: true },  // Wall Hangings 3x3
109	  152: 'v_152_ebonstone_brick',  // Ebonstone Brick
110	  124: 'v_124_wooden_beam',  // Wooden Beam
111	  158: 'v_158_rich_mahogany',  // Rich Mahogany
112	  519: { key: 'v_519_cattails', copyFrame: true },  // Cattails
113	  357: 'v_357_smooth_marble_block',  // Smooth Marble Block
114	  272: 'v_272_cog_block',  // Cog Block
115	  229: 'v_229_honey_block',  // Honey Block
116	  138: { key: 'v_138_boulder', copyFrame: true },  // Boulder
117	  634: { key: 'v_634_ash_tree', copyFrame: true },  // Ash Tree
118	  575: 'v_575_rich_mahogany_beam',  // Rich Mahogany Beam
119	  26: { key: 'v_26_altars', copyFrame: true },  // Altars
120	  311: 'v_311_dynasty_wood',  // Dynasty Wood
121	  130: 'v_130_active_stone_block',  // Active Stone Block
122	  82: { key: 'v_82_herbs_sprout', copyFrame: true },  // Herbs (Sprout)
123	  193: 'v_193_slime_block',  // Slime Block
124	  323: { key: 'v_323_palm_trees', copyFrame: true },  // Palm Trees
125	  190: 'v_190_glowing_mushroom_block',  // Glowing Mushroom Block
126	  350: 'v_350_martian_conduit_plating',  // Martian Conduit Plating
127	  369: 'v_369_smooth_granite_block',  // Smooth Granite Block
128	  135: { key: 'v_135_pressure_plates', copyFrame: true },  // Pressure Plates
129	  91: { key: 'v_91_banners', copyFrame: true },  // Banners
130	  242: { key: 'v_242_paintings_6x4', copyFrame: true },  // Paintings 6x4
131	  50: { key: 'v_50_books', copyFrame: true },  // Books
132	  93: { key: 'v_93_lamps', copyFrame: true },  // Lamps
133	  549: { key: 'v_549_seaweed', copyFrame: true },  // Seaweed
134	  137: { key: 'v_137_traps', copyFrame: true },  // Traps
135	  117: 'v_117_pearlstone_block',  // Pearlstone Block
136	  112: 'v_112_ebonsand_block',  // Ebonsand Block
137	  254: { key: 'v_254_pumpkin_plant', copyFrame: true },  // Pumpkin Plant
138	  571: { key: 'v_571_bamboo', copyFrame: true },  // Bamboo
139	  232: 'v_232_wooden_spike',  // Wooden Spike
140	  274: 'v_274_sandstone_slab',  // Sandstone Slab
141	  246: { key: 'v_246_paintings_3x2', copyFrame: true },  // Paintings 3x2
142	  213: 'v_213_rope',  // Rope
143	  245: { key: 'v_245_paintings_2x3', copyFrame: true },  // Paintings 2x3
144	  322: 'v_322_palm_wood',  // Palm Wood
145	  586: { key: 'v_586_emerald_tree', copyFrame: true },  // Emerald Tree
146	  596: { key: 'v_596_vanity_tree_sakura', copyFrame: true },  // Vanity Tree Sakura
147	  636: 'v_636_corrupt_vines',  // Corrupt Vines
148	  574: 'v_574_boreal_beam',  // Boreal Beam
149	  467: { key: 'v_467_chests_group_2', copyFrame: true },  // Chests (Group 2)
150	  109: 'v_109_hallowed_grass_block',  // Hallowed Grass Block
151	  443: { key: 'v_443_geyser', copyFrame: true },  // Geyser
152	  312: 'v_312_red_dynasty_shingles',  // Red Dynasty Shingles
153	  589: { key: 'v_589_amber_tree', copyFrame: true },  // Amber Tree
154	  411: { key: 'v_411_detonator', copyFrame: true },  // Detonator
155	  518: { key: 'v_518_lily_pads', copyFrame: true },  // Lily Pads
156	  588: { key: 'v_588_diamond_tree', copyFrame: true },  // Diamond Tree
157	  422: 'v_422_conveyor_belt_ccw',  // Conveyor Belt (CCW)
158	  585: { key: 'v_585_sapphire_tree', copyFrame: true },  // Sapphire Tree
159	  583: { key: 'v_583_topaz_tree', copyFrame: true },  // Topaz Tree
160	  13: { key: 'v_13_placed_bottles', copyFrame: true },  // Placed Bottles
161	  530: { key: 'v_530_oasis_plants', copyFrame: true },  // Oasis Plants
162	  495: 'v_495_shell_pile_block',  // Shell Pile Block
163	  479: 'v_479_smooth_sandstone_block',  // Smooth Sandstone Block
164	  616: { key: 'v_616_vanity_tree_yellow_willow', copyFrame: true },  // Vanity Tree Yellow Willow
165	  215: { key: 'v_215_campfires', copyFrame: true },  // Campfires
166	  141: { key: 'v_141_explosives', copyFrame: true },  // Explosives
167	  333: 'v_333_platinum_coin_pile',  // Platinum Coin Pile
168	  597: { key: 'v_597_pylons', copyFrame: true },  // Pylons
169	  592: { key: 'v_592_hanging_brazier', copyFrame: true },  // Hanging Brazier
170	  375: { key: 'v_375_honey_drip', copyFrame: true },  // Honey Drip
171	  227: { key: 'v_227_dye_plants', copyFrame: true },  // Dye Plants
172	  353: 'v_353_vine_rope',  // Vine Rope
173	  584: { key: 'v_584_amethyst_tree', copyFrame: true },  // Amethyst Tree
174	  231: { key: 'v_231_larva', copyFrame: true },  // Larva
175	  332: 'v_332_gold_coin_pile',  // Gold Coin Pile
176	  395: { key: 'v_395_item_frame', copyFrame: true },  // Item Frame
177	  241: { key: 'v_241_catacombs', copyFrame: true },  // Catacombs
178	  587: { key: 'v_587_ruby_tree', copyFrame: true },  // Ruby Tree
179	  86: { key: 'v_86_loom', copyFrame: true },  // Loom
180	  477: 'v_477_mowed_grass_block',  // Mowed Grass Block
181	  376: { key: 'v_376_fishing_crates', copyFrame: true },  // Fishing Crates
182	  470: { key: 'v_470_mannequins', copyFrame: true },  // Mannequins
183	  577: 'v_577_sandstone_column',  // Sandstone Column
184	  561: 'v_561_marble_column',  // Marble Column
185	  324: { key: 'v_324_seashells', copyFrame: true },  // Seashells
186	  81: { key: 'v_81_coral', copyFrame: true },  // Coral
187	  576: 'v_576_granite_column',  // Granite Column
188	  214: 'v_214_chain',  // Chain
189	  380: { key: 'v_380_planter_boxes', copyFrame: true },  // Planter Boxes
190	  136: { key: 'v_136_switch', copyFrame: true },  // Switch
191	  355: { key: 'v_355_alchemy_table', copyFrame: true },  // Alchemy Table
192	  354: { key: 'v_354_bewitching_table', copyFrame: true },  // Bewitching Table
193	  103: { key: 'v_103_bowls', copyFrame: true },  // Bowls
194	  529: { key: 'v_529_sea_oats', copyFrame: true },  // Sea Oats
195	  506: { key: 'v_506_bast_statue', copyFrame: true },  // Bast Statue
196	  349: { key: 'v_349_mushroom_statue', copyFrame: true },  // Mushroom Statue
197	  377: { key: 'v_377_sharpening_station', copyFrame: true },  // Sharpening Station
198	  613: { key: 'v_613_potted_lava_plants', copyFrame: true },  // Potted Lava Plants
199	  230: 'v_230_crispy_honey_block',  // Crispy Honey Block
200	  219: { key: 'v_219_extractinator', copyFrame: true },  // Extractinator
201	  388: { key: 'v_388_tall_gate_closed', copyFrame: true },  // Tall Gate (Closed)
202	  129: { key: 'v_129_crystal_shard', copyFrame: true },  // Crystal Shard
203	  466: { key: 'v_466_elder_cystal_stand', copyFrame: true },  // Elder Cystal Stand
204	  562: 'v_562_bamboo_block',  // Bamboo Block
205	  220: { key: 'v_220_solidifier', copyFrame: true },  // Solidifier
206	  303: { key: 'v_303_lihzahrd_furnace', copyFrame: true },  // Lihzahrd Furnace
207	  469: { key: 'v_469_tables_group_2', copyFrame: true },  // Tables (Group 2)
208	  304: { key: 'v_304_living_loom', copyFrame: true },  // Living Loom
209	  488: { key: 'v_488_fallen_log', copyFrame: true },  // Fallen Log
210	  548: { key: 'v_548_potted_trees_group_2', copyFrame: true },  // Potted Trees (Group 2)
211	  614: { key: 'v_614_potted_ember_tendrils', copyFrame: true },  // Potted Ember Tendrils
212	  598: { key: 'v_598_lava_serpent_bowl', copyFrame: true },  // Lava Serpent Bowl
213	  371: 'v_371_pink_slime_block',  // Pink Slime Block
214	  406: { key: 'v_406_chimney', copyFrame: true },  // Chimney
215	  305: { key: 'v_305_sky_mill', copyFrame: true },  // Sky Mill
216	  300: { key: 'v_300_bone_welder', copyFrame: true },  // Bone Welder
217	  302: { key: 'v_302_glass_kiln', copyFrame: true },  // Glass Kiln
218	  306: { key: 'v_306_ice_machine', copyFrame: true },  // Ice Machine
219	  247: { key: 'v_247_autohammer', copyFrame: true },  // Autohammer
220	  491: { key: 'v_491_void_vault', copyFrame: true },  // Void Vault
221	  106: { key: 'v_106_sawmill', copyFrame: true },  // Sawmill
222	  642: { key: 'v_642_chlorophyte_extractinator', copyFrame: true },  // Chlorophyte Extractinator
223	  319: { key: 'v_319_ship_in_a_bottle', copyFrame: true },  // Ship in a Bottle
224	  487: { key: 'v_487_picnic_tables', copyFrame: true },  // Picnic Tables
225	  97: { key: 'v_97_safe', copyFrame: true },  // Safe
226	  668: 'v_668_the_dirtiest_block',  // The Dirtiest Block
227	  320: { key: 'v_320_seaweed_planter', copyFrame: true },  // Seaweed Planter
228	  405: { key: 'v_405_fireplace', copyFrame: true },  // Fireplace
229	  378: { key: 'v_378_target_dummy', copyFrame: true },  // Target Dummy
230	  218: { key: 'v_218_meat_grinder', copyFrame: true },  // Meat Grinder
231	  356: { key: 'v_356_enchanted_sundial', copyFrame: true },  // Enchanted Sundial
232	  114: { key: 'v_114_tinkerer_s_workshop', copyFrame: true },  // Tinkerer's Workshop
233	  578: 'v_578_mushroom_beam',  // Mushroom Beam
234	  237: { key: 'v_237_lihzahrd_altar', copyFrame: true },  // Lihzahrd Altar
235	  110: { key: 'v_110_hallow_short_plants', copyFrame: true },  // Hallow Short Plants
236	  621: { key: 'v_621_slice_of_cake', copyFrame: true },  // Slice of Cake
237	  387: { key: 'v_387_trap_door_closed', copyFrame: true },  // Trap Door (Closed)
238	  316: { key: 'v_316_blue_jellyfish_jar', copyFrame: true },  // Blue Jellyfish Jar
239	  125: { key: 'v_125_crystal_ball', copyFrame: true },  // Crystal Ball
240	  287: { key: 'v_287_ammo_box', copyFrame: true },  // Ammo Box
241	  294: { key: 'v_294_zebra_swallowtail_butterfly_jar', copyFrame: true },  // Zebra Swallowtail Butterfly Jar
242	  291: { key: 'v_291_ulysses_butterfly_jar', copyFrame: true },  // Ulysses Butterfly Jar
243	  292: { key: 'v_292_sulphur_butterfly_jar', copyFrame: true },  // Sulphur Butterfly Jar
244	  289: { key: 'v_289_purple_emperor_butterfly_jar', copyFrame: true },  // Purple Emperor Butterfly Jar
245	  172: { key: 'v_172_sinks', copyFrame: true },  // Sinks
246	  656: { key: 'v_656_glow_tulip', copyFrame: true },  // Glow Tulip
247	  113: { key: 'v_113_hallow_tall_plants', copyFrame: true },  // Hallow Tall Plants
248	  235: { key: 'v_235_teleporter', copyFrame: true },  // Teleporter
249	  567: { key: 'v_567_garden_gnome', copyFrame: true },  // Garden Gnome
250	  398: 'v_398_corrupt_hardened_sand_block',  // Corrupt Hardened Sand Block
251	  379: 'v_379_bubble',  // Bubble
252	  618: 'v_618_stone_accent_slab',  // Stone Accent Slab
253	  // 清空的装饰/不可表示物
254	  11: { key: 'door_open', copyFrame: true },  // Open Door（原版变体帧）
255	  28: { key: 'pot', copyFrame: true }, 29: null, 30: 'wood',  // Pots(原版) / Piggy Bank(暂无) / Wood→木材
256	  52: 'v_52_vines', 55: null,  // 藤蔓 / 乐器架
257	  61: 'tallgrass', 62: 'v_62_jungle_vines', 69: 'v_69_jungle_thorns', // jungle plants(草化)/藤蔓/荆棘
258	  74: 'tallgrass', 76: { key: 'furnace', copyFrame: true }, 77: { key: 'furnace', copyFrame: true }, 80: 'v_80_cactus', // plants2→草 / Hellforge→熔炉 / 仙人掌（渲染端现场分帧）
259	  83: { key: 'v_83_herbs_mature', copyFrame: true },  // Herbs (Mature)
260	  84: { key: 'v_84_herbs_bloom', copyFrame: true },  // Herbs (Bloom)
261	  // ---- FTW_V2 补全 ----
262	  625: 'v_625_neon_moss_block',  // Neon Moss Block
263	  151: 'v_151_sandstone_brick',  // Sandstone Brick
264	  234: 'v_234_crimsand_block',  // Crimsand Block
265	  182: 'v_182_blue_moss_block',  // Blue Moss Block
266	  205: 'v_205_crimson_vines',  // Crimson Vines
267	  45: 'v_45_gold_brick',  // Gold Brick
268	  399: 'v_399_crimson_hardened_sand_block',  // Crimson Hardened Sand Block
269	  352: 'v_352_crimtane_thorns',  // Crimtane Thorns
270	  248: 'v_248_palladium_column',  // Palladium Column
271	  340: 'v_340_living_cursed_fire_block',  // Living Cursed Fire Block
272	  207: { key: 'v_207_water_fountains', copyFrame: true },  // Water Fountains
273	  144: { key: 'v_144_timers', copyFrame: true },  // Timers
274	  475: { key: 'v_475_hat_rack', copyFrame: true },  // Hat Rack
275	  175: 'v_175_tin_brick',  // Tin Brick
276	  132: { key: 'v_132_lever', copyFrame: true },  // Lever
277	  // ---- 不负责任的女妖啤酒厂 补全 ----
278	  539: 'v_539_argon_moss_block',  // Argon Moss Block
279	  481: 'v_481_cracked_blue_brick',  // Cracked Blue Brick
280	  120: 'v_120_mudstone_brick',  // Mudstone Brick
281	  714: { key: 'v_714_spider_boulder', copyFrame: true },  // Spider Boulder
282	  752: { key: 'v_752_chillet_egg', copyFrame: true },  // Chillet Egg
283	  751: { key: 'v_751_sleeping_digtoise', copyFrame: true },  // Sleeping Digtoise
284	  664: { key: 'v_664_bouncy_boulder', copyFrame: true },  // Bouncy Boulder
285	  711: { key: 'v_711_rainbow_boulder', copyFrame: true },  // Rainbow Boulder
286	  715: { key: 'v_715_ghoulder', copyFrame: true },  // Ghoulder
287	  716: { key: 'v_716_friendly_boulder', copyFrame: true },  // Friendly Boulder
288	  713: { key: 'v_713_lava_boulder', copyFrame: true },  // Lava Boulder
289	  23: 'v_23_corrupt_grass_block',
290	  31: { key: 'v_31_orb_heart', copyFrame: true },  // Orb Heart（2×2 style 帧直拷）
291	  41: 'v_41_blue_brick', 43: 'v_43_green_brick',
292	  60: 'v_60_jungle_grass_block',
293	  70: 'v_70_mushroom_grass_block',
294	  25: 'v_25_ebonstone_block',  // Ebonstone Block
295	  202: 'v_202_sunplate_block', // Sunplate Block
296	  71: { key: 'v_71_mushroom_plant', copyFrame: true }, // Mushroom Plant
297	  72: { key: 'v_72_mushroom_tree', copyFrame: true },  // Mushroom Tree（U≥36 标记帧走 ShroomTop）
298	  24: { key: 'v_24_corruption_short_plants', copyFrame: true }, // Corruption Short Plants
299	  32: { key: 'v_32_corruption_thorns', copyFrame: true }, // Corruption Thorns
300	  27: { key: 'v_27_sunflower', copyFrame: true }, // Sunflower (2x4)
301	  44: 'v_44_pink_brick',  // Pink Brick
302	  203: 'v_203_crimstone_block',  // Crimstone Block
303	  201: { key: 'v_201_crimson_short_plants', copyFrame: true }, // Crimson Short Plants
304	  75: 'v_75_obsidian_brick',
305	  199: 'v_199_crimson_grass_block',
306	};
307	
308	// 墙 id 直用原版 wld 墙 id（WALL_DEFS 已按 TEdit walls.json 全量注册 367 种）
309	
310	// wld item id → 内部 item key（宝箱战利品用）
311	const ITEM_MAP: Record<number, string> = {
312	  2: 'dirt_block', 8: 'torch', 9: 'wood', 175: 'stone_block',
313	  11: 'iron_ore', 12: 'copper_ore', 13: 'gold_ore', 14: 'silver_ore',
314	  20: 'copper_bar', 22: 'iron_bar', 23: 'gel',
315	  28: 'lesser_healing_potion', 38: 'lens',
316	  71: 'coin_copper', 72: 'coin_copper', 73: 'coin_copper', 74: 'coin_copper',
317	  // 原版批次材料
318	  699: 'tin_ore', 700: 'lead_ore', 701: 'tungsten_ore', 702: 'platinum_ore',
319	  703: 'tin_bar', 704: 'lead_bar', 705: 'tungsten_bar', 706: 'platinum_bar',
320	  177: 'sapphire', 178: 'ruby', 179: 'emerald', 180: 'topaz', 181: 'amethyst', 182: 'diamond',
321	  664: 'ice_block', 883: 'ice_brick', 594: 'snow_brick',
322	  133: 'clay_block', 170: 'glass', 173: 'obsidian', 129: 'gray_brick', 131: 'red_brick',
323	  32: 'table', 34: 'chair', 224: 'bed', 354: 'bookcase', 359: 'grandfather_clock',
324	  105: 'candle', 136: 'lantern', 349: 'candelabra', 222: 'clay_pot', 29: 'life_crystal',
325	  5: 'mushroom_item', 27: 'acorn',
326	  // ---- 全量补全（compat-report 驱动）----
327	  2350: 'vi_2350_recall_potion',  // Recall Potion
328	  188: 'vi_188_healing_potion',  // Healing Potion
329	  282: 'vi_282_glowstick',  // Glowstick
330	  167: 'vi_167_dynamite',  // Dynamite
331	  279: 'vi_279_throwing_knife',  // Throwing Knife
332	  51: 'vi_51_jester_s_arrow',  // Jester's Arrow
333	  19: 'vi_19_gold_bar',  // Gold Bar
334	  302: 'vi_302_water_walking_potion',  // Water Walking Potion
335	  305: 'vi_305_gravitation_potion',  // Gravitation Potion
336	  43: 'vi_43_suspicious_looking_eye',  // Suspicious Looking Eye
337	  296: 'vi_296_spelunker_potion',  // Spelunker Potion
338	  299: 'vi_299_night_owl_potion',  // Night Owl Potion
339	  965: 'vi_965_rope',  // Rope
340	  303: 'vi_303_archery_potion',  // Archery Potion
341	  304: 'vi_304_hunter_potion',  // Hunter Potion
342	  50: 'vi_50_magic_mirror',  // Magic Mirror
343	  42: 'vi_42_shuriken',  // Shuriken
344	  295: 'vi_295_featherfall_potion',  // Featherfall Potion
345	  53: 'vi_53_cloud_in_a_bottle',  // Cloud in a Bottle
346	  2329: 'vi_2329_dangersense_potion',  // Dangersense Potion
347	  40: 'vi_40_wooden_arrow',  // Wooden Arrow
348	  975: 'vi_975_shoe_spikes',  // Shoe Spikes
349	  54: 'vi_54_hermes_boots',  // Hermes Boots
350	  301: 'vi_301_thorns_potion',  // Thorns Potion
351	  49: 'vi_49_band_of_regeneration',  // Band of Regeneration
352	  2326: 'vi_2326_titan_potion',  // Titan Potion
353	  297: 'vi_297_invisibility_potion',  // Invisibility Potion
354	  166: 'vi_166_bomb',  // Bomb
355	  5011: 'vi_5011_mace',  // Mace
356	  4425: 'vi_4425_shark_bait',  // Shark Bait
357	  2351: 'vi_2351_teleportation_potion',  // Teleportation Potion
358	  4460: 'vi_4460_sandcastle_bucket',  // Sandcastle Bucket
359	  168: 'vi_168_grenade',  // Grenade
360	  227: 'vi_227_restoration_potion',  // Restoration Potion
361	  930: 'vi_930_flare_gun',  // Flare Gun
362	  931: 'vi_931_flare',  // Flare
363	  997: 'vi_997_extractinator',  // Extractinator
364	  52: 'vi_52_angel_statue',  // Angel Statue
365	  265: 'vi_265_hellfire_arrow',  // Hellfire Arrow
366	  298: 'vi_298_shine_potion',  // Shine Potion
367	  5007: 'vi_5007_dead_man_s_sweater',  // Dead Man's Sweater
368	  117: 'vi_117_meteorite_bar',  // Meteorite Bar
369	  186: 'vi_186_breathing_reed',  // Breathing Reed
370	  329: 'vi_329_shadow_key',  // Shadow Key
371	  974: 'vi_974_ice_torch',  // Ice Torch
372	  2322: 'vi_2322_mining_potion',  // Mining Potion
373	  4915: 'vi_4915_tungsten_bullet',  // Tungsten Bullet
374	  946: 'vi_946_umbrella',  // Umbrella
375	  939: 'vi_939_web_slinger',  // Web Slinger
376	  4870: 'vi_4870_potion_of_return',  // Potion of Return
377	  288: 'vi_288_obsidian_skin_potion',  // Obsidian Skin Potion
378	  211: 'vi_211_feral_claws',  // Feral Claws
379	  4404: 'vi_4404_inner_tube',  // Inner Tube
380	  187: 'vi_187_flipper',  // Flipper
381	  2198: 'vi_2198_ice_machine',  // Ice Machine
382	  274: 'vi_274_dark_lance',  // Dark Lance
383	  285: 'vi_285_aglet',  // Aglet
384	  213: 'vi_213_staff_of_regrowth',  // Staff of Regrowth
385	  964: 'vi_964_boomstick',  // Boomstick
386	  1293: 'vi_1293_lihzahrd_power_cell',  // Lihzahrd Power Cell
387	  2195: 'vi_2195_lihzahrd_furnace',  // Lihzahrd Furnace
388	  2766: 'vi_2766_solar_tablet_fragment',  // Solar Tablet Fragment
389	  300: 'vi_300_battle_potion',  // Battle Potion
390	  2348: 'vi_2348_inferno_potion',  // Inferno Potion
391	  218: 'vi_218_flamelash',  // Flamelash
392	  3019: 'vi_3019_hellwing_bow',  // Hellwing Bow
393	  112: 'vi_112_flower_of_fire',  // Flower of Fire
394	  220: 'vi_220_sunfury',  // Sunfury
395	  4345: 'vi_4345_can_of_worms',  // Can Of Worms
396	  953: 'vi_953_climbing_claws',  // Climbing Claws
397	  3069: 'vi_3069_wand_of_sparking',  // Wand of Sparking
398	  212: 'vi_212_anklet_of_the_wind',  // Anklet of the Wind
399	  2204: 'vi_2204_honey_dispenser',  // Honey Dispenser
400	  277: 'vi_277_trident',  // Trident
401	  863: 'vi_863_water_walking_boots',  // Water Walking Boots
402	  751: 'vi_751_cloud',  // Cloud
403	  155: 'vi_155_muramasa',  // Muramasa
404	  289: 'vi_289_regeneration_potion',  // Regeneration Potion
405	  906: 'vi_906_lava_charm',  // Lava Charm
406	  4055: 'vi_4055_dunerider_boots',  // Dunerider Boots
407	  724: 'vi_724_ice_blade',  // Ice Blade
408	  670: 'vi_670_ice_boomerang',  // Ice Boomerang
409	  4061: 'vi_4061_storm_spear',  // Storm Spear
410	  987: 'vi_987_blizzard_in_a_bottle',  // Blizzard in a Bottle
411	  4551: 'vi_4551_slice_of_hell_cake',  // Slice of Hell Cake
412	  5010: 'vi_5010_treasure_magnet',  // Treasure Magnet
413	  2323: 'vi_2323_heartreach_potion',  // Heartreach Potion
414	  2345: 'vi_2345_lifeforce_potion',  // Lifeforce Potion
415	  290: 'vi_290_swiftness_potion',  // Swiftness Potion
416	  291: 'vi_291_gills_potion',  // Gills Potion
417	  280: 'vi_280_spear',  // Spear
418	  2325: 'vi_2325_builder_potion',  // Builder Potion
419	  284: 'vi_284_wooden_boomerang',  // Wooden Boomerang
420	  2192: 'vi_2192_bone_welder',  // Bone Welder
421	  5234: 'vi_5234_remnants_of_devotion',  // Remnants of Devotion
422	  156: 'vi_156_cobalt_shield',  // Cobalt Shield
423	  157: 'vi_157_aqua_scepter',  // Aqua Scepter
424	  163: 'vi_163_blue_moon',  // Blue Moon
425	  113: 'vi_113_magic_missile',  // Magic Missile
426	  3317: 'vi_3317_valor',  // Valor
427	  327: 'vi_327_golden_key',  // Golden Key
428	  164: 'vi_164_handgun',  // Handgun
429	  294: 'vi_294_magic_power_potion',  // Magic Power Potion
430	  4263: 'vi_4263_magic_conch',  // Magic Conch
431	  4062: 'vi_4062_thunder_zapper',  // Thunder Zapper
432	  1579: 'vi_1579_flurry_boots',  // Flurry Boots
433	  4056: 'vi_4056_ancient_chisel',  // Ancient Chisel
434	  4346: 'vi_4346_encumbering_stone',  // Encumbering Stone
435	  1319: 'vi_1319_snowball_cannon',  // Snowball Cannon
436	  3199: 'vi_3199_ice_mirror',  // Ice Mirror
437	  950: 'vi_950_ice_skates',  // Ice Skates
438	  4443: 'vi_4443_demonic_hellcart',  // Demonic Hellcart
439	  4737: 'vi_4737_ornate_shadow_key',  // Ornate Shadow Key
440	  4276: 'vi_4276_bast_statue',  // Bast Statue
441	  4262: 'vi_4262_snake_charmer_s_flute',  // Snake Charmer's Flute
442	  3093: 'vi_3093_herb_bag',  // Herb Bag
443	  292: 'vi_292_ironskin_potion',  // Ironskin Potion
444	  3084: 'vi_3084_radar',  // Radar
445	  4341: 'vi_4341_step_stool',  // Step Stool
446	  4978: 'vi_4978_fledgling_wings',  // Fledgling Wings
447	  2197: 'vi_2197_sky_mill',  // Sky Mill
448	  158: 'vi_158_lucky_horseshoe',  // Lucky Horseshoe
449	  5254: 'vi_5254_blessing_from_the_heavens',  // Blessing from the Heavens
450	  1156: 'vi_1156_piranha_gun',  // Piranha Gun
451	  1571: 'vi_1571_scourge_of_the_corruptor',  // Scourge of the Corruptor
452	  1260: 'vi_1260_rainbow_gun',  // Rainbow Gun
453	  1572: 'vi_1572_staff_of_the_frost_hydra',  // Staff of the Frost Hydra
454	  4607: 'vi_4607_desert_tiger_staff',  // Desert Tiger Staff
455	  933: 'vi_933_leaf_wand',  // Leaf Wand
456	  832: 'vi_832_living_wood_wand',  // Living Wood Wand
457	  4066: 'vi_4066_desert_minecart',  // Desert Minecart
458	  4450: 'vi_4450_shroom_minecart',  // Shroom Minecart
459	  4423: 'vi_4423_scarab_bomb',  // Scarab Bomb
460	  159: 'vi_159_shiny_red_balloon',  // Shiny Red Balloon
461	  5258: 'vi_5258_see_the_world_for_what_it_is',  // See The World For What It Is
462	  65: 'vi_65_starfury',  // Starfury
463	  5388: 'vi_5388_eye_of_the_sun',  // Eye of the Sun
464	  2219: 'vi_2219_celestial_magnet',  // Celestial Magnet
465	  5255: 'vi_5255_love_is_in_the_trash_slot',  // Love is in the Trash Slot
466	  4426: 'vi_4426_bee_minecart',  // Bee Minecart
467	  3017: 'vi_3017_flower_boots',  // Flower Boots
468	  3360: 'vi_3360_living_mahogany_wand',  // Living Mahogany Wand
469	  3361: 'vi_3361_rich_mahogany_leaf_wand',  // Rich Mahogany Leaf Wand
470	  1309: 'vi_1309_slime_staff',  // Slime Staff
471	  1845: 'vi_1845_necromantic_scroll',  // Necromantic Scroll
472	  1864: 'vi_1864_papyrus_scarab',  // Papyrus Scarab
473	  1158: 'vi_1158_pygmy_necklace',  // Pygmy Necklace
474	  3034: 'vi_3034_coin_ring',  // Coin Ring
475	  308: 'vi_308_moonglow_seeds',  // Moonglow Seeds
476	  312: 'vi_312_fireblossom_seeds',  // Fireblossom Seeds
477	  310: 'vi_310_deathweed_seeds',  // Deathweed Seeds
478	  307: 'vi_307_daybloom_seeds',  // Daybloom Seeds
479	  309: 'vi_309_blinkroot_seeds',  // Blinkroot Seeds
480	  2357: 'vi_2357_shiverthorn_seeds',  // Shiverthorn Seeds
481	  311: 'vi_311_waterleaf_seeds',  // Waterleaf Seeds
482	  1828: 'vi_1828_pumpkin_seed',  // Pumpkin Seed
483	  126: 'vi_126_bottled_water',  // Bottled Water
484	  1134: 'vi_1134_bottled_honey',  // Bottled Honey
485	  3068: 'vi_3068_guide_to_plant_fiber_cordage',  // Guide to Plant Fiber Cordage
486	  4779: 'vi_4779_mushroom_hat',  // Mushroom Hat
487	  4780: 'vi_4780_mushroom_vest',  // Mushroom Vest
488	  4781: 'vi_4781_mushroom_pants',  // Mushroom Pants
489	  678: 'vi_678_red_potion',  // Red Potion
490	  281: 'vi_281_blowpipe',  // Blowpipe
491	  293: 'vi_293_mana_regeneration_potion',  // Mana Regeneration Potion
492	  2767: 'vi_2767_solar_tablet',  // Solar Tablet
493	  3: 'vi_3_stone_block',  // Stone Block
494	  3213: 'vi_3213_money_trough',  // Money Trough
495	  94: 'vi_94_wood_platform',  // Wood Platform
496	  2757: 'vi_2757_vortex_helmet',  // Vortex Helmet
497	  4989: 'vi_4989_soaring_insignia',  // Soaring Insignia
498	  3383: 'vi_3383_stardust_leggings',  // Stardust Leggings
499	  4914: 'vi_4914_kaleidoscope',  // Kaleidoscope
500	  26: 'vi_26_stone_wall',  // Stone Wall
501	  1991: 'vi_1991_bug_net',  // Bug Net
502	  4828: 'vi_4828_superheated_blood',  // Superheated Blood
503	  3509: 'vi_3509_copper_pickaxe',  // Copper Pickaxe
504	  3507: 'vi_3507_copper_shortsword',  // Copper Shortsword
505	  4755: 'vi_4755_grox_the_great_s_horned_cowl',  // Grox The Great's Horned Cowl
506	  4756: 'vi_4756_grox_the_great_s_chestplate',  // Grox The Great's Chestplate
507	  4757: 'vi_4757_grox_the_great_s_greaves',  // Grox The Great's Greaves
508	  214: 'vi_214_hellstone_brick',  // Hellstone Brick
509	  5000: 'vi_5000_terraspark_boots',  // Terraspark Boots
510	  5339: 'vi_5339_arcane_crystal',  // Arcane Crystal
511	  5391: 'vi_5391_uncumbering_stone',  // Uncumbering Stone
512	  2585: 'vi_2585_slime_hook',  // Slime Hook
513	  313: 'vi_313_daybloom',  // Daybloom
514	  267: 'vi_267_guide_voodoo_doll',  // Guide Voodoo Doll
515	  2649: 'vi_2649_steampunk_candle',  // Steampunk Candle
516	  286: 'vi_286_sticky_glowstick',  // Sticky Glowstick
517	  3002: 'vi_3002_spelunker_glowstick',  // Spelunker Glowstick
518	  4819: 'vi_4819_demon_conch',  // Demon Conch
519	  1802: 'vi_1802_raven_staff',  // Raven Staff
520	  3382: 'vi_3382_stardust_plate',  // Stardust Plate
521	  3270: 'vi_3270_item_frame',  // Item Frame
522	  3771: 'vi_3771_ancient_horn',  // Ancient Horn
523	  93: 'vi_93_wood_wall',  // Wood Wall
524	  4281: 'vi_4281_finch_staff',  // Finch Staff
525	  5407: 'vi_5407_star_royale_brick',  // Star Royale Brick
526	  5401: 'vi_5401_lunar_rust_brick',  // Lunar Rust Brick
527	  4716: 'vi_4716_mollusk_whistle',  // Mollusk Whistle
528	  3540: 'vi_3540_phantasm',  // Phantasm
529	  2176: 'vi_2176_shroomite_digging_claw',  // Shroomite Digging Claw
530	  2349: 'vi_2349_wrath_potion',  // Wrath Potion
531	  4679: 'vi_4679_morning_star',  // Morning Star
532	  1169: 'vi_1169_bone_key',  // Bone Key
533	  3863: 'vi_3863_betsy_mask',  // Betsy Mask
534	  3124: 'vi_3124_cell_phone',  // Cell Phone
535	  3506: 'vi_3506_copper_axe',  // Copper Axe
536	  4680: 'vi_4680_dark_harvest',  // Dark Harvest
537	  543: 'vi_543_brown_pressure_plate',  // Brown Pressure Plate
538	  172: 'vi_172_ash_block',  // Ash Block
539	  171: 'vi_171_sign',  // Sign
540	  1723: 'vi_1723_living_wood_wall',  // Living Wood Wall
541	  4754: 'vi_4754_grox_the_great_s_wings',  // Grox The Great's Wings
542	  3353: 'vi_3353_mechanical_cart',  // Mechanical Cart
543	  2287: 'vi_2287_winter_cape',  // Winter Cape
544	  1179: 'vi_1179_chlorophyte_bullet',  // Chlorophyte Bullet
545	  4766: 'vi_4766_world_globe',  // World Globe
546	  4954: 'vi_4954_celestial_starboard',  // Celestial Starboard
547	  4730: 'vi_4730_ghostar_s_infinity_eight',  // Ghostar's Infinity Eight
548	  4758: 'vi_4758_blade_staff',  // Blade Staff
549	  4765: 'vi_4765_tree_globe',  // Tree Globe
550	  5342: 'vi_5342_ambrosia',  // Ambrosia
551	  5328: 'vi_5328_chest_lock',  // Chest Lock
552	  5343: 'vi_5343_peddler_s_satchel',  // Peddler's Satchel
553	  5285: 'vi_5285_moon_globe',  // Moon Globe
554	  5289: 'vi_5289_minecart_upgrade_kit',  // Minecart Upgrade Kit
555	  5336: 'vi_5336_advanced_combat_techniques_volume_two',  // Advanced Combat Techniques: Volume Two
556	  5451: 'vi_5451_kwad_racer_drone',  // Kwad Racer Drone
557	  5359: 'vi_5359_shellphone_spawn',  // Shellphone (Spawn)
558	  3032: 'vi_3032_super_absorbant_sponge',  // Super Absorbant Sponge
559	  3031: 'vi_3031_bottomless_water_bucket',  // Bottomless Water Bucket
560	  509: 'vi_509_red_wrench',  // Red Wrench
561	  4741: 'vi_4741_butcher_s_bloodstained_apron',  // Butcher's Bloodstained Apron
562	  3065: 'vi_3065_star_wrath',  // Star Wrath
563	  3063: 'vi_3063_meowmere',  // Meowmere
564	  3372: 'vi_3372_lunatic_cultist_mask',  // Lunatic Cultist Mask
565	  1504: 'vi_1504_spectre_robe',  // Spectre Robe
566	  2769: 'vi_2769_cosmic_car_key',  // Cosmic Car Key
567	  216: 'vi_216_shackle',  // Shackle
568	  4415: 'vi_4415_stone_door',  // Stone Door
569	  118: 'vi_118_hook',  // Hook
570	  1681: 'vi_1681_skeleton_banner',  // Skeleton Banner
571	  283: 'vi_283_seed',  // Seed
572	  1173: 'vi_1173_grave_marker',  // Grave Marker
573	  4379: 'vi_4379_wyvern_kite',  // Wyvern Kite
574	  4378: 'vi_4378_xenon_moss',  // Xenon Moss
575	  4377: 'vi_4377_krypton_moss',  // Krypton Moss
576	  4376: 'vi_4376_rat_cage',  // Rat Cage
577	  4375: 'vi_4375_rat',  // Rat
578	  4484: 'vi_4484_1_2_second_timer',  // 1/2 Second Timer
579	  4824: 'vi_4824_wet_bomb',  // Wet Bomb
580	  4485: 'vi_4485_1_4_second_timer',  // 1/4 Second Timer
581	  5378: 'vi_5378_cursed_flare',  // Cursed Flare
582	  5354: 'vi_5354_reflective_shades',  // Reflective Shades
583	  5387: 'vi_5387_raynbro_s_pants',  // Raynbro's Pants
584	  5386: 'vi_5386_raynbro_s_hoodie',  // Raynbro's Hoodie
585	  5390: 'vi_5390_raynbro_s_hood',  // Raynbro's Hood
586	  5338: 'vi_5338_aegis_fruit',  // Aegis Fruit
587	  5404: 'vi_5404_cosmic_ember_brick',  // Cosmic Ember Brick
588	  5405: 'vi_5405_cryocore_brick',  // Cryocore Brick
589	  5403: 'vi_5403_astra_brick',  // Astra Brick
590	  346: 'vi_346_safe',  // Safe
591	  4829: 'vi_4829_cat_license',  // Cat License
592	  3335: 'vi_3335_demon_heart',  // Demon Heart
593	  4750: 'vi_4750_foodbarbarian_s_tattered_dragon_wings',  // FoodBarbarian's Tattered Dragon Wings
594	  3042: 'vi_3042_phase_dye',  // Phase Dye
595	  3024: 'vi_3024_skiphs_blood',  // Skiphs' Blood
596	  3054: 'vi_3054_shadowflame_knife',  // Shadowflame Knife
597	  5275: 'vi_5275_joja_cola',  // Joja Cola
598	  5278: 'vi_5278_pomegranate',  // Pomegranate
599	  5277: 'vi_5277_spicy_pepper',  // Spicy Pepper
600	  5437: 'vi_5437_shellphone',  // Shellphone
601	  1507: 'vi_1507_spectre_hamaxe',  // Spectre Hamaxe
602	  2250: 'vi_2250_steampunk_chest',  // Steampunk Chest
603	  392: 'vi_392_glass_wall',  // Glass Wall
604	  2699: 'vi_2699_weapon_rack',  // Weapon Rack
605	  3552: 'vi_3552_blue_flame_and_silver_dye',  // Blue Flame and Silver Dye
606	  5005: 'vi_5005_terraprisma',  // Terraprisma
607	  4604: 'vi_4604_exotic_chew_toy',  // Exotic Chew Toy
608	  4611: 'vi_4611_world_feeder_kite',  // World Feeder Kite
609	  4649: 'vi_4649_blue_jellyfish_kite',  // Blue Jellyfish Kite
610	  4796: 'vi_4796_dark_mage_s_tome',  // Dark Mage's Tome
611	  4553: 'vi_4553_plasma_lamp',  // Plasma Lamp
612	  4365: 'vi_4365_celestial_wand',  // Celestial Wand
613	  331: 'vi_331_jungle_spores',  // Jungle Spores
614	  2430: 'vi_2430_slimy_saddle',  // Slimy Saddle
615	  4956: 'vi_4956_zenith',  // Zenith
616	  2798: 'vi_2798_laser_drill',  // Laser Drill
617	  2814: 'vi_2814_martian_chest',  // Martian Chest
618	  210: 'vi_210_vine',  // Vine
619	  4371: 'vi_4371_yellow_kite',  // Yellow Kite
620	  4291: 'vi_4291_lemon',  // Lemon
621	  2493: 'vi_2493_king_slime_mask',  // King Slime Mask
622	  1919: 'vi_1919_sugar_cookie',  // Sugar Cookie
623	  1912: 'vi_1912_eggnog',  // Eggnog
624	  4023: 'vi_4023_grapes',  // Grapes
625	  4792: 'vi_4792_the_black_spot',  // The Black Spot
626	  529: 'vi_529_red_pressure_plate',  // Red Pressure Plate
627	  3066: 'vi_3066_smooth_marble_block',  // Smooth Marble Block
628	  183: 'vi_183_glowing_mushroom',  // Glowing Mushroom
629	  1103: 'vi_1103_slush_block',  // Slush Block
630	  2119: 'vi_2119_stone_slab',  // Stone Slab
631	  593: 'vi_593_snow_block',  // Snow Block
632	  3081: 'vi_3081_marble_block',  // Marble Block
633	  1111: 'vi_1111_blue_berries',  // Blue Berries
634	  1115: 'vi_1115_red_husk',  // Red Husk
635	  217: 'vi_217_molten_hamaxe',  // Molten Hamaxe
636	  122: 'vi_122_molten_pickaxe',  // Molten Pickaxe
637	  1827: 'vi_1827_bladed_glove',  // Bladed Glove
638	  2263: 'vi_2263_white_dynasty_wall',  // White Dynasty Wall
639	  330: 'vi_330_obsidian_brick_wall',  // Obsidian Brick Wall
640	  130: 'vi_130_gray_brick_wall',  // Gray Brick Wall
641	  2433: 'vi_2433_stone_slab_wall',  // Stone Slab Wall
642	  452: 'vi_452_hornet_statue',  // Hornet Statue
643	  453: 'vi_453_bomb_statue',  // Bomb Statue
644	  360: 'vi_360_armor_statue',  // Armor Statue
645	  3711: 'vi_3711_wraith_statue',  // Wraith Statue
646	  438: 'vi_438_star_statue',  // Star Statue
647	  446: 'vi_446_skeleton_statue',  // Skeleton Statue
648	  458: 'vi_458_cross_statue',  // Cross Statue
649	  3655: 'vi_3655_scorpion_statue',  // Scorpion Statue
650	  328: 'vi_328_shadow_chest',  // Shadow Chest
651	  2196: 'vi_2196_living_loom',  // Living Loom
652	  916: 'vi_916_shadewood_work_bench',  // Shadewood Work Bench
653	  35: 'vi_35_iron_anvil',  // Iron Anvil
654	  36: 'vi_36_work_bench',  // Work Bench
655	  3240: 'vi_3240_tall_gate',  // Tall Gate
656	  337: 'vi_337_red_banner',  // Red Banner
657	  3381: 'vi_3381_stardust_helmet',  // Stardust Helmet
658	  1765: 'vi_1765_vampire_pants',  // Vampire Pants
659	  2859: 'vi_2859_lunar_cultist_robe',  // Lunar Cultist Robe
660	  2857: 'vi_2857_lunar_cultist_hood',  // Lunar Cultist Hood
661	  2998: 'vi_2998_summoner_emblem',  // Summoner Emblem
662	  1175: 'vi_1175_headstone',  // Headstone
663	  25: 'vi_25_wooden_door',  // Wooden Door
664	  46: 'vi_46_light_s_bane',  // Light's Bane
665	  352: 'vi_352_keg',  // Keg
666	  2340: 'vi_2340_minecart_track',  // Minecart Track
667	  498: 'vi_498_mannequin',  // Mannequin
668	  4721: 'vi_4721_mushroom_beam',  // Mushroom Beam
669	  819: 'vi_819_living_wood_door',  // Living Wood Door
670	  1458: 'vi_1458_obsidian_door',  // Obsidian Door
671	  3763: 'vi_3763_0x33_s_aviators',  // 0x33's Aviators
672	  176: 'vi_176_mud_block',  // Mud Block
673	  1569: 'vi_1569_vampire_knives',  // Vampire Knives
674	  857: 'vi_857_sandstorm_in_a_bottle',  // Sandstorm in a Bottle
675	  2292: 'vi_2292_fiberglass_fishing_pole',  // Fiberglass Fishing Pole
676	  5238: 'vi_5238_constellation',  // Constellation
677	  753: 'vi_753_seaweed',  // Seaweed
678	  5120: 'vi_5120_deer_thing',  // Deer Thing
679	  5508: 'vi_5508_grim_old_barb',  // Grim Old Barb
680	  5465: 'vi_5465_ram_rune',  // Ram Rune
681	  5500: 'vi_5500_goat_s_tuft',  // Goat\'s Tuft
682	  5499: 'vi_5499_froggy_neckband',  // Froggy Neckband
683	  5507: 'vi_5507_balloony_beads',  // Balloony Beads
684	  5485: 'vi_5485_chicken_charm',  // Chicken Charm
685	  5502: 'vi_5502_cat_chime',  // Cat Chime
686	  5504: 'vi_5504_turkey_wattle_necklace',  // Turkey Wattle Necklace
687	  5506: 'vi_5506_crow_s_beak',  // Crow\'s Beak
688	  5503: 'vi_5503_dog_collar',  // Dog Collar
689	  5534: 'vi_5534_fairy_choker',  // Fairy Choker
690	  5484: 'vi_5484_cow_bell',  // Cow Bell
691	  5501: 'vi_5501_old_companion_locket',  // Old Companion Locket
692	  5509: 'vi_5509_vampire_pendant',  // Vampire Pendant
693	  31: 'vi_31_bottle',  // Bottle
694	  41: 'vi_41_flaming_arrow',  // Flaming Arrow
695	  75: 'vi_75_fallen_star',  // Fallen Star
696	  5505: 'vi_5505_mean_goblin_s_spikes',  // Mean Goblin\'s Spikes
697	  5525: 'vi_5525_cursed_piper_flute',  // Cursed Piper Flute
698	};
699	
700	export interface CompatEntry { id: number; name: string | null; count: number; action: string }
701	export interface CompatReport {
702	  worldName: string; wldVersion: number; size: [number, number];
703	  tilesDegraded: CompatEntry[];  // 未映射 tile → 降级石块
704	  tilesCleared: CompatEntry[];   // 映射为 null → 清空丢弃
705	  itemsSkipped: CompatEntry[];   // 宝箱内未映射物品 → 跳过
706	}
707	export interface ImportResult { save: SaveData; warnings: string[]; report: CompatReport }
708	
709	export function parseWldToSave(buf: Uint8Array): ImportResult {
710	  const wld: WldWorld = parseWld(buf);
711	  const warnings: string[] = [];
712	  const tileNames = vanillaTileNames;
713	  const itemNames = vanillaItemNames;
714	  const deg = new Map<number, number>(), clr = new Map<number, number>(), itm = new Map<number, number>();
715	  const bump = (m: Map<number, number>, id: number) => m.set(id, (m.get(id) ?? 0) + 1);
716	
717	  const w = wld.tilesWide, h = wld.tilesHigh;
718	  const n = w * h;
719	  const type = new Uint16Array(n);
720	  const frameX = new Uint16Array(n);
721	  const frameY = new Uint16Array(n);
722	  const wall = new Uint16Array(n); // 原版墙 id 直存（0-366）
723	  const liquidArr = new Uint8Array(n);
724	  const liquidTypeArr = new Uint8Array(n);
725	
726	  const chestAt = new Map<string, { x: number; y: number }>();
727	  for (const c of wld.chests) chestAt.set(`${c.x},${c.y}`, c);
728	
729	  let unmapped = 0;
730	  for (let i = 0; i < n; i++) {
731	    const wt = wld.tiles.type[i];
732	    if (wld.tiles.active[i]) {
733	      const mapped = TILE_MAP[wt];
734	      if (mapped === undefined) {
735	        // 未映射：framed 物体丢弃，方块降级为 stone（保持地形完整可玩）
736	        unmapped++;
737	        bump(deg, wt);
738	        type[i] = T.STONE;
739	      } else if (mapped === null) {
740	        bump(clr, wt);
741	        type[i] = 0;
742	      } else if (typeof mapped === 'string') {
743	        type[i] = TILE_BY_KEY[mapped] ?? 0;
744	      } else {
745	        // 原版 framed 家具：18px 帧/样式偏移直拷（与 .wld 原生一致，渲染端零换算）
746	        type[i] = TILE_BY_KEY[mapped.key] ?? 0;
747	        if (mapped.copyFrame) {
748	          frameX[i] = wld.tiles.frameX[i];
749	          frameY[i] = wld.tiles.frameY[i];
750	        }
751	      }
752	    }
753	    wall[i] = wld.tiles.wall[i]; // 直拷原版墙 id
754	    const lq = wld.tiles.liquid[i];
755	    if (lq > 0) liquidArr[i] = lq;
756	    // 液体类型：parser 已按内部编码输出（1水 2岩浆 3蜂蜜），直拷
757	    if (lq > 0) liquidTypeArr[i] = wld.tiles.liquidType[i] || 1;
758	  }
759	  if (unmapped > 0) warnings.push(`${unmapped} 个未知 tile 已降级为石块`);
760	
761	  // 宝箱：转内部格式（锚点 + 战利品）。帧统一 18px 像素偏移（vanilla style 规范语义，
762	  // 与 tryPlace / breakTile 的 floor(f/18) 归一化一致）
763	  const chests: SaveData['chests'] = [];
764	  for (const c of wld.chests) {
765	    // 在 chest 周围找锚点（wld chest 坐标可能是左上）
766	    type[c.y * w + c.x] = TILE_BY_KEY['chest'];
767	    frameX[c.y * w + c.x] = 0;
768	    frameY[c.y * w + c.x] = 0;
769	    if (c.x + 1 < w) { type[c.y * w + c.x + 1] = TILE_BY_KEY['chest']; frameX[c.y * w + c.x + 1] = 18; frameY[c.y * w + c.x + 1] = 0; }
770	    if (c.y + 1 < h) { type[(c.y + 1) * w + c.x] = TILE_BY_KEY['chest']; frameX[(c.y + 1) * w + c.x] = 0; frameY[(c.y + 1) * w + c.x] = 18; }
771	    if (c.x + 1 < w && c.y + 1 < h) { type[(c.y + 1) * w + c.x + 1] = TILE_BY_KEY['chest']; frameX[(c.y + 1) * w + c.x + 1] = 18; frameY[(c.y + 1) * w + c.x + 1] = 18; }
772	    const items: Array<{ id: number; stack: number } | null> = [];
773	    for (const it of c.items.slice(0, 10)) {
774	      if (!it) { items.push(null); continue; }
775	      const key = ITEM_MAP[it.id];
776	      if (key && ITEM_BY_KEY[key] !== undefined) {
777	        items.push({ id: ITEM_BY_KEY[key], stack: Math.min(999, it.stack) });
778	      } else {
779	        bump(itm, it.id);
780	        items.push(null);
781	      }
782	    }
783	    while (items.length < 10) items.push(null);
784	    chests.push({ x: c.x, y: c.y, items });
785	  }
786	
787	  // 时间换算：wld time 0 = 4:30AM（白天起点）
788	  let timeOfDay: number;
789	  if (wld.dayTime) {
790	    timeOfDay = 0.1875 + (wld.time % 1) * 0.5;
791	  } else {
792	    timeOfDay = 0.6875 + (wld.time % 1) * 0.5;
793	  }
794	  timeOfDay = timeOfDay % 1;
795	
796	  const save: SaveData = {
797	    format: 'sandboxworld.save',
798	    version: 2, // 墙已是原版 id 语义——不能低于 2，否则 loadSave 触发旧墙值迁移翻转
799	    header: {
800	      name: wld.title || '导入的地图',
801	      seed: 0,
802	      width: w,
803	      height: h,
804	      spawn: [wld.spawnX, wld.spawnY],
805	      groundLevel: Math.floor(wld.groundLevel),
806	      rockLevel: Math.floor(wld.rockLevel),
807	      created: Date.now(),
808	      playTimeMs: 0,
809	      wldVersion: wld.version,
810	      treeX: wld.treeX,
811	      treeStyle: wld.treeStyle,
812	      treeTops: wld.treeTops?.length ? wld.treeTops : undefined,
813	      crimson: wld.isCrimson,
814	    },
815	    clock: { timeOfDay, dayCount: 1 },
816	    tiles: bytesToB64(rleTiles({ type, frameX, frameY })),
817	    walls: bytesToB64(rlePairs(wall)),
818	    liquid: bytesToB64(rlePairs(liquidArr)),
819	    liquidType: bytesToB64(rlePairs(liquidTypeArr)),
820	    chests,
821	    player: {
822	      hp: 100,
823	      x: wld.spawnX * 16 + 8,
824	      y: (wld.spawnY - 2) * 16,
825	      inventory: Array(40).fill(null),
826	      selected: 0,
827	    },
828	    npcs: [],
829	    flags: { downedEyeOfCthulhu: false },
830	  };
831	  const toEntries = (m: Map<number, number>, names: Record<string, string>): CompatEntry[] =>
832	    [...m.entries()].map(([id, count]) => ({ id, name: names[String(id)] ?? null, count, action: '' }))
833	      .sort((a, b) => b.count - a.count);
834	  const report: CompatReport = {
835	    worldName: wld.title || '导入的地图',
836	    wldVersion: wld.version,
837	    size: [w, h],
838	    tilesDegraded: toEntries(deg, tileNames).map((e) => ({ ...e, action: 'degraded-to-stone' })),
839	    tilesCleared: toEntries(clr, tileNames).map((e) => ({ ...e, action: 'cleared' })),
840	    itemsSkipped: toEntries(itm, itemNames).map((e) => ({ ...e, action: 'skipped' })),
841	  };
842	  void warnings;
843	  void chestAt;
844	  return { save, warnings, report };
845	}
846	
847	// 全量名称表（vanilla.json 生成时从 TEdit tiles/items.json 提取）
848	import vanillaJson from '../../public/sprites/vanilla.json';
849	const vanillaData = vanillaJson as unknown as { tileNames?: Record<string, string>; itemNames?: Record<string, string> };
850	const vanillaTileNames = vanillaData.tileNames ?? {};
851	const vanillaItemNames = vanillaData.itemNames ?? {};
852	

```


---

## 🤖 Assistant · 2026-08-09T10:49:07.053Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The grep for F-keys failed because of zsh globbing. Let me quote. Also need: Entity.ts (EntityManager buckets), LiquidSim basics, constants.ts, tiles.ts TileDef structure, and where keyboard shortcuts F5/F8 etc. are registered (likely in UI.ts or main.ts). Let me search.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:49:07.401Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"'F[0-9]'\\|\\\"F[0-9]\\\"\" ~/Project/GLM/SandboxWorld/game/src | head -40",
 "description": "Find F-key shortcut handling"
}
```


---

## 🤖 Assistant · 2026-08-09T10:49:07.408Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts"
}
```


---

## 🤖 Assistant · 2026-08-09T10:49:07.410Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/constants.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:07.415Z

**📎 ToolResult**

```
1	// 实体基类与分桶管理器
2	import type { GameHooks } from './types';
3	import type { Camera } from '../render/Camera';
4	import type { Renderer } from '../render/Renderer';
5	
6	export abstract class Entity {
7	  id = 0;
8	  x = 0; y = 0;          // 左上角 px
9	  w = 16; h = 16;
10	  vx = 0; vy = 0;
11	  dead = false;
12	  onGround = false;
13	  hitWall = false;
14	  hitHead = false;
15	  dropThrough = false;
16	
17	  abstract fixedUpdate(dt: number, game: GameHooks): void;
18	  abstract draw(r: Renderer, cam: Camera): void;
19	
20	  get cx() { return this.x + this.w / 2; }
21	  get cy() { return this.y + this.h / 2; }
22	  aabbOverlaps(o: Entity): boolean {
23	    return this.x < o.x + o.w && this.x + this.w > o.x && this.y < o.y + o.h && this.y + this.h > o.y;
24	  }
25	}
26	
27	export class EntityManager {
28	  nextId = 1;
29	  enemies: Entity[] = [];
30	  drops: Entity[] = [];
31	  npcs: Entity[] = [];
32	  projectiles: Entity[] = [];
33	  props: Entity[] = [];   // 场景物件（墓碑等不可拾取物理实体）
34	  critters: Entity[] = []; // 小动物（无害被动生物）
35	
36	  add(e: Entity, bucket: 'enemies' | 'drops' | 'npcs' | 'projectiles' | 'props' | 'critters') {
37	    e.id = this.nextId++;
38	    this[bucket].push(e);
39	  }
40	
41	  update(dt: number, game: GameHooks) {
42	    for (const list of [this.enemies, this.drops, this.npcs, this.projectiles, this.props, this.critters]) {
43	      for (const e of list) e.fixedUpdate(dt, game);
44	    }
45	    this.enemies = this.enemies.filter((e) => !e.dead);
46	    this.drops = this.drops.filter((e) => !e.dead);
47	    this.npcs = this.npcs.filter((e) => !e.dead);
48	    this.projectiles = this.projectiles.filter((e) => !e.dead);
49	    this.props = this.props.filter((e) => !e.dead);
50	    this.critters = this.critters.filter((e) => !e.dead);
51	  }
52	
53	  clear() {
54	    this.enemies.length = 0;
55	    this.drops.length = 0;
56	    this.npcs.length = 0;
57	    this.projectiles.length = 0;
58	    this.props.length = 0;
59	    this.critters.length = 0;
60	  }
61	
62	  all(): Entity[] {
63	    return [...this.enemies, ...this.drops, ...this.npcs, ...this.projectiles, ...this.props, ...this.critters];
64	  }
65	}
66	

```


---

## 👤 User(sidechain) · 2026-08-09T10:49:07.416Z

**📎 ToolResult**

```
1	// 全局调参集中地：物理、渲染、生成、平衡数值
2	export const TILE = 16; // tile 尺寸（px）
3	
4	// ---- 物理 ----
5	export const GRAVITY = 0.36; // px/tick^2
6	export const MAX_FALL_SPEED = 9.5;
7	export const PLAYER_WALK_ACCEL = 0.32;
8	export const PLAYER_WALK_MAX = 2.6; // px/tick
9	export const PLAYER_FRICTION = 0.72; // 地面摩擦系数（乘法）
10	export const PLAYER_AIR_FRICTION = 0.94;
11	export const PLAYER_JUMP_SPEED = 6.6;
12	export const PLAYER_JUMP_TICKS = 9; // 长按跳跃的持续加速度 tick 数
13	export const ENEMY_GRAVITY = 0.32;
14	
15	// ---- 世界 ----
16	export const CHUNK = 16; // chunk 边长（tile）
17	
18	// ---- 光照 ----
19	export const LIGHT_AIR_COST = 12; // 光穿过空气每格衰减（最大传播 ~21 格；火把照明半径加大）
20	export const SKY_LIGHT = 255;
21	
22	// ---- 时间 ----
23	export const DAY_LENGTH = 24 * 60 * 60 * 1000 / 60; // 1 游戏日 = 24 现实分钟（ms 现实时间）
24	export const TICK_RATE = 60; // 固定逻辑帧率
25	
26	// ---- 战斗 ----
27	export const PLAYER_IFRAME_TICKS = 40; // 受击无敌帧
28	export const PLAYER_MAX_HP = 100;
29	export const KNOCKBACK_BASE = 3.2;
30	export const ENEMY_CAP = 9;
31	export const MAGNET_RADIUS = 3.2 * TILE; // 掉落物磁吸半径（px）
32	export const PICKUP_DELAY = 25; // 掉落物产生后多少 tick 才能被拾取
33	
34	// ---- 敌人生成 ----
35	export const SPAWN_MIN_DIST = 42 * TILE; // 距玩家最小生成距离：必在屏幕外（zoom1.25 半屏≈32格）
36	export const SPAWN_MAX_DIST = 72 * TILE;
37	export const SPAWN_CHECK_INTERVAL = 30; // tick
38	

```


---

## 👤 User(sidechain) · 2026-08-09T10:49:07.437Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/main.ts:89:    case 'F3':
~/Project/GLM/SandboxWorld/game/src/main.ts:94:    case 'F4':
~/Project/GLM/SandboxWorld/game/src/main.ts:100:    case 'F5':
~/Project/GLM/SandboxWorld/game/src/main.ts:104:    case 'F6':
~/Project/GLM/SandboxWorld/game/src/main.ts:108:    case 'F8':
~/Project/GLM/SandboxWorld/game/src/main.ts:113:    case 'F9':
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:144:    R(0x0, 0x0, 0x1000, 0x0, 'F7', 'H7'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:157:    R(0x0, 0x0, 0x1000, 0x0, 'F8', 'H8'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:162:    R(0x0, 0x0, 0x1000, 0x0, 'F5', 'H5'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:179:    R(0x0, 0x0, 0x1000, 0x0, 'F6', 'H6'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:184:    R(0x0, 0x0, 0x1000, 0x0, 'F9', 'F11'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:193:    R(0x0, 0x0, 0x110, 0x0, 'F3', 'J3'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:209:    R(0x0, 0x0, 0x11, 0x0, 'F4', 'J4'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:223:    R(0x0, 0x0, 0x10000000, 0x0, 'F1', 'J1'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:224:    R(0x0, 0x0, 0x1000000, 0x0, 'F2', 'J2'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:244:    R(0x0, 0x0, 0x1000, 0x0, 'F7', 'H7'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:257:    R(0x0, 0x0, 0x1100, 0x11, 'F6', 'H6'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:258:    R(0x0, 0x0, 0x1001, 0x110, 'F5', 'H5'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:259:    R(0x0, 0x0, 0x1000, 0x0, 'F8', 'H8'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:265:    R(0x0, 0x0, 0x1000, 0x0, 'F5', 'H5'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:281:    R(0x0, 0x0, 0x1000, 0x0, 'F6', 'H6'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:301:    R(0x0, 0x1000, 0x110, 0x10000000, 'F3', 'J3'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:315:    R(0x0, 0x1000, 0x100, 0x10000000, 'F3', 'J3'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:318:    R(0x0, 0x100, 0x11, 0x1000000, 'F4', 'J4'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:328:    R(0x0, 0x100, 0x10, 0x1000000, 'F4', 'J4'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:329:    R(0x0, 0x1000, 0x10, 0x10000000, 'F3', 'J3'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:337:    R(0x0, 0x100, 0x1, 0x1000000, 'F4', 'J4'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:353:    R(0x0, 0x100, 0x0, 0x1000000, 'F4', 'J4'),
~/Project/GLM/SandboxWorld/game/src/render/BlendFraming.ts:354:    R(0x0, 0x1000, 0x0, 0x10000000, 'F3', 'J3'),

```


---

## 🤖 Assistant · 2026-08-09T10:49:09.056Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/main.ts",
 "limit": 150
}
```


---

## 🤖 Assistant · 2026-08-09T10:49:09.062Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts",
 "limit": 120
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:09.079Z

**📎 ToolResult**

```
1	// 入口：加载素材/字体/文案 → VUI 主菜单 → 生成/加载世界 → 进入游戏
2	// 流程编排见 mainFlow.ts；本文件只做装配 + 游戏内键盘/开发者工具接线。
3	import { Game } from './core/Game';
4	import { UI } from './ui/UI';
5	import { kvHas } from './save/KvStore';
6	import { saveGame } from './save/SaveFile';
7	import { ITEM_BY_KEY } from './data/items';
8	import { TILE_BY_KEY, T, TILE_DEFS, WALL_DEFS } from './data/tiles';
9	import { parseWldToSave } from './wld/WldImport';
10	// 调试句柄：页面内直接测 .wld 转换
11	(window as unknown as { __parseWld?: (b: Uint8Array) => unknown }).__parseWld = parseWldToSave as unknown as (b: Uint8Array) => unknown;
12	import { SpriteAtlas } from './assets/SpriteAtlas';
13	import { AudioSystem } from './core/Audio';
14	import { setDebugPool } from './data/vanillaNpcs';
15	import { VUI } from './vui/VUI';
16	import { UITextures } from './vui/assets/UITextures';
17	import { UIFont } from './vui/draw/UIFont';
18	import { Lang } from './i18n/Lang';
19	import { VuiDemoState } from './vui/states/VuiDemoState';
20	import { createFlow } from './mainFlow';
21	import type { FlowHandle } from './mainFlow';
22	
23	const root = document.getElementById('game-root')!;
24	const ui = new UI(root);
25	const audio = new AudioSystem();
26	let atlas: SpriteAtlas | null = null;
27	
28	let flow: FlowHandle;
29	let inGame = false;
30	let pausePanel: HTMLElement | null = null;
31	
32	async function loadAssets() {
33	  atlas = new SpriteAtlas();
34	  try {
35	    await atlas.load();
36	  } catch {
37	    atlas = null; // 素材缺失时回退程序化生成
38	  }
39	}
40	
41	function enterGameHooks() {
42	  const g = flow.game!;
43	  inGame = true;
44	  (window as unknown as { __swTiles: typeof TILE_BY_KEY }).__swTiles = TILE_BY_KEY;
45	  (window as unknown as { __swItems: typeof ITEM_BY_KEY }).__swItems = ITEM_BY_KEY;
46	  (window as unknown as { __swSetPool?: (p: number[] | null) => void }).__swSetPool = setDebugPool;
47	}
48	
49	// ---- 键盘：背包/暂停/保存 ----
50	window.addEventListener('keydown', (e) => {
51	  const game = flow.game;
52	  if (!inGame || !game) return;
53	  switch (e.code) {
54	    case 'KeyE':
55	    case 'Escape':
56	      e.preventDefault();
57	      if (game.renderer.fullMap.open) {
58	        game.renderer.fullMap.open = false;
59	        break;
60	      }
61	      if (pausePanel) {
62	        pausePanel.remove();
63	        pausePanel = null;
64	        game.paused = false;
65	        ui.closeInventory();
66	        game.input.uiBlocking = false;
67	      } else if (ui.invPanel && ui.invPanel.style.display === 'block') {
68	        ui.closeInventory();
69	      } else if (e.code === 'Escape') {
70	        game.paused = true;
71	        pausePanel = ui.showPause({
72	          onResume: () => {
73	            pausePanel?.remove();
74	            pausePanel = null;
75	            game!.paused = false;
76	          },
77	          onSave: () => flow.doSave(),
78	          onQuit: () => {
79	            pausePanel = null;
80	            game!.paused = false;
81	            inGame = false;
82	            flow.quitToMenu();
83	          },
84	        });
85	      } else {
86	        ui.openInventory();
87	      }
88	      break;
89	    case 'F3':
90	      e.preventDefault();
91	      game.renderer.debugMode = !game.renderer.debugMode;
92	      ui.toast(game.renderer.debugMode ? '调试面板已开启（碰撞盒高亮）' : '调试面板已关闭');
93	      break;
94	    case 'F4':
95	      e.preventDefault();
96	      game.world.explored.fill(1);
97	      game.world.exploredVersion++; // 使迷雾缓存失效重建
98	      ui.toast('已消除全图迷雾');
99	      break;
100	    case 'F5':
101	      e.preventDefault();
102	      toggleAnnotate();
103	      break;
104	    case 'F6':
105	      e.preventDefault();
106	      flow.doSave();
107	      break;
108	    case 'F8':
109	      e.preventDefault();
110	      game.enemySpawnEnabled = !game.enemySpawnEnabled;
111	      ui.toast(game.enemySpawnEnabled ? '怪物生成已开启' : '怪物生成已关闭（已有怪物不受影响）');
112	      break;
113	    case 'F9':
114	      e.preventDefault();
115	      game.renderer.fullbright = !game.renderer.fullbright;
116	      ui.toast(game.renderer.fullbright ? '已开灯：全画面无暗影' : '已关灯：恢复正常光照');
117	      break;
118	    case 'KeyM':
119	      if (game.renderer.fullMap.open) {
120	        game.renderer.fullMap.open = false;
121	      } else {
122	        ui.toast(audio.toggleMute() ? '音乐已关闭' : '音乐已开启');
123	      }
124	      break;
125	  }
126	});
127	
128	function downloadText(filename: string, text: string) {
129	  const blob = new Blob([text], { type: 'application/json' });
130	  const a = document.createElement('a');
131	  a.href = URL.createObjectURL(blob);
132	  a.download = filename;
133	  a.click();
134	  URL.revokeObjectURL(a.href);
135	}
136	
137	// ---- 方块标注模式（F5）：标记问题方块，导出标注 + 地图给开发者 ----
138	function toggleAnnotate() {
139	  const game = flow.game;
140	  if (!game) return;
141	  game.annotateMode = !game.annotateMode;
142	  if (game.annotateMode) {
143	    ui.showAnnotatePanel({
144	      onExportMarks: exportMarks,
145	      onExportMap: exportMap,
146	      onClear: () => {
147	        if (!flow.game) return;
148	        flow.game.marks = [];
149	        ui.updateAnnotateCount(0);
150	      },

```


---

## 👤 User(sidechain) · 2026-08-09T10:49:09.080Z

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
39	  private stuckAmount = 0; // 原版 ReInit 置 0（Liquid.cs:69）
40	  private disposed = false;
41	  /** LiquidBuffer 溢出缓冲（Liquid.cs:840-843 入队 / 799-807 清扫轮回灌，上限 49998） */
42	  private buffer: Array<{ x: number; y: number }> = [];
43	
44	  constructor(world: World) {
45	    this.world = world;
46	    const st = world.store;
47	    this.checking = new Uint8Array(st.w * st.h);
48	    this.skip = new Uint8Array(st.w * st.h);
49	    // 挖掘/放置唤醒：原版 SquareTileFrame 会对 3×3 内每格 TileFrame→AddWater（WorldGen.cs:49664）
50	    st.onTileChanged((x, y) => {
51	      if (this.disposed) return;
52	      for (let dy = -1; dy <= 1; dy++)
53	        for (let dx = -1; dx <= 1; dx++) this.addWater(x + dx, y + dy);
54	    });
55	    // 液体直接写入（水桶等）：唤醒目标及四邻
56	    st.onLiquidChanged((x, y) => {
57	      if (this.disposed) return;
58	      this.addWater(x, y);
59	      this.addWater(x, y - 1); this.addWater(x, y + 1);
60	      this.addWater(x - 1, y); this.addWater(x + 1, y);
61	    });
62	  }
63	
64	  /** 丢弃模拟器：预沉降临时实例调用，停止响应唤醒 */
65	  dispose() {
66	    this.disposed = true;
67	    this.liquids.length = 0;
68	    this.numLiquid = 0;
69	  }
70	
71	  private idx(x: number, y: number): number { return y * this.world.store.w + x; }
72	
73	  /** 格子是否阻挡液体（原版 nactive() && tileSolid && !tileSolidTop） */
74	  private blocksLiquid(x: number, y: number): boolean {
75	    const st = this.world.store;
76	    if (x < 0 || y < 0 || x >= st.w || y >= st.h) return true;
77	    const t = st.type[this.idx(x, y)];
78	    if (t === 0) return false;
79	    const d = TILE_DEFS[t];
80	    return !!d && d.solid && !d.platform;
81	  }
82	
83	  /** WorldGen.SolidTile 语义（WorldGen.cs:42370）：实心 && !平台 && !半砖 && !坡面。
84	   *  仅 LavaCheck/HoneyCheck 入口使用——半砖格允许发生交互（Liquid.cs:898/1020） */
85	  private solidTileFull(x: number, y: number): boolean {
86	    const st = this.world.store;
87	    if (x < 0 || y < 0 || x >= st.w || y >= st.h) return true;
88	    const i = this.idx(x, y);
89	    const t = st.type[i];
90	    if (t === 0) return false;
91	    const d = TILE_DEFS[t];
92	    return !!d && d.solid && !d.platform && !st.half[i] && st.slope[i] === 0;
93	  }
94	
95	  // ================= AddWater（Liquid.cs:835-872） =================
96	
97	  addWater(x: number, y: number) {
98	    const st = this.world.store;
99	    if (x >= st.w - 5 || y >= st.h - 5 || x < 5 || y < 5) return;
100	    const i = this.idx(x, y);
101	    if (this.checking[i] || st.liquid[i] === 0) return;
102	    const t = st.type[i];
103	    if (t !== 0) {
104	      const d = TILE_DEFS[t];
105	      if (d && d.solid && !d.platform) return;
106	    }
107	    if (this.numLiquid >= this.curMaxLiquid - 1) {
108	      // 原版走 LiquidBuffer 缓冲、清扫轮回灌（Liquid.cs:840-843），超缓冲上限才丢
109	      if (this.buffer.length < 49998) this.buffer.push({ x, y });
110	      return;
111	    }
112	    this.checking[i] = 1;
113	    this.skip[i] = 0;
114	    this.liquids[this.numLiquid] = { x, y, kill: 0, delay: 0 };
115	    this.numLiquid++;
116	  }
117	
118	  // ================= UpdateLiquid 调度（Liquid.cs:691-833） =================
119	
120	  /** 每 2 个逻辑 tick 调一次（原版 WorldGen.UpdateWorld 内 skipCount 节流） */

```


---

## 🤖 Assistant · 2026-08-09T10:49:13.099Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have almost everything. A few more things to confirm quickly:

1. tiles.ts TileDef structure (fields incl. w/h, vanilla, solid, platform, framed, decor, drop, mapColor).
2. items.ts remaining part (lines 260-724) — place_ items for vanilla tiles.
3. Renderer.ts overlay toggles (fullbright at ~line 355 area, drawDebugOverlay). Also compositeLight.
4. Check whether there is a 'lever'/'switch'/'teleporter'/'statue' tile keys: v_132_lever, v_136_switch, v_137_traps, v_135_pressure_plates, v_105_statue, v_235_teleporter, v_144_timers.
5. Check pressure plate / statue usage — Enemy.fromVanilla for statue spawns; teleportNear exists.
6. ChunkCache draw order for a wire overlay — done.
7. Check T enum in tiles.ts for keys and TileDef interface.

Let me grep a few things quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:49:13.963Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 1,120p ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts",
 "description": "Read TileDef interface and T enum head"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:13.993Z

**📎 ToolResult**

```
// 内部 tile / wall 注册表。id 即数组下标。
// 数值（硬度/光照）为原创平衡设计；mapColor 参考 TEdit tiles.json 的地图配色后重新取整。

export interface TileDef {
  key: string;
  name: string;
  solid: boolean;        // 参与碰撞
  platform: boolean;     // 单向平台（下跳可穿）
  decor: boolean;        // 装饰物（不碰撞、可被任何工具秒清）
  framed: boolean;       // 多格框架物体（使用 frameX/frameY 定位贴图）
  opacity: number;       // 光照阻挡 0-1
  light?: [number, number, number]; // 自发光 RGB
  pick: number;          // 所需镐力（-1 不可挖）
  axe: number;           // 所需斧力
  mapColor: string;      // 小地图颜色
  drop?: string;         // 破坏掉落 item key（缺省掉同名 key）
  rope?: boolean;        // 绳索类（攀爬判定）
  blend: boolean;        // 是否参与同类边缘融合
  attach?: 'ground' | 'wall'; // 装饰物附着需求
  w?: number; h?: number;     // framed 物体占格数
  vanilla?: {                 // 原版素材渲染（terraria-assets + TEdit 数据）
    sheet: number;            // Tiles_N 表 id
    frame: 'auto' | 'style' | 'blend'; // auto=47 表 8 向；style=显式帧；blend=BlendRules 合并分帧（泥土/石/草族）
    fw?: number; fh?: number; // style 类的占格数（TEdit frameSize）
  };
}

export const T = {
  EMPTY: 0, DIRT: 1, STONE: 2, GRASS: 3,
  ORE_COPPER: 4, ORE_IRON: 5, ORE_SILVER: 6, ORE_GOLD: 7,
  TREE: 8, LEAVES: 9, WOOD: 10, PLATFORM: 11,
  TORCH: 12, WORKBENCH: 13, FURNACE: 14, ANVIL: 15,
  CHEST: 16, DOOR_CLOSED: 17, DOOR_OPEN: 18,
  MUSHROOM: 19, FLOWER: 20, TALLGRASS: 21, SAND: 22, SNOW: 23,
  SAPLING: 24, ASH: 25,
} as const;

export const TILE_DEFS: TileDef[] = [];
function def(d: Partial<TileDef> & { key: string }): number {
  const id = TILE_DEFS.length;
  TILE_DEFS.push({
    name: d.key, solid: false, platform: false, decor: false, framed: false,
    opacity: 0, pick: -1, axe: -1, mapColor: '#000', blend: false, ...d, id,
  } as TileDef);
  return id;
}
// 保证 id 与 T 常量一致（按顺序注册）
def({ key: 'empty', name: '空气' });
def({ key: 'dirt', name: '泥土', solid: true, opacity: 1, pick: 0, mapColor: '#976B4B', blend: true, drop: 'dirt_block', vanilla: { sheet: 0, frame: 'blend' } });
def({ key: 'stone', name: '石块', solid: true, opacity: 1, pick: 0, mapColor: '#808080', blend: true, drop: 'stone_block', vanilla: { sheet: 1, frame: 'blend' } });
def({ key: 'grass', name: '草块', solid: true, opacity: 1, pick: 0, mapColor: '#1CD85E', blend: true, drop: 'dirt_block', vanilla: { sheet: 2, frame: 'blend' } });
def({ key: 'ore_copper', name: '铜矿', solid: true, opacity: 1, pick: 0, mapColor: '#964316', blend: false, drop: 'copper_ore', vanilla: { sheet: 7, frame: 'auto' } });
def({ key: 'ore_iron', name: '铁矿', solid: true, opacity: 1, pick: 0, mapColor: '#8C6A56', blend: false, drop: 'iron_ore', vanilla: { sheet: 6, frame: 'auto' } });
def({ key: 'ore_silver', name: '银矿', solid: true, opacity: 1, pick: 20, mapColor: '#B9C2C3', blend: false, drop: 'silver_ore', vanilla: { sheet: 9, frame: 'auto' } });
def({ key: 'ore_gold', name: '金矿', solid: true, opacity: 1, pick: 40, mapColor: '#B9A417', blend: false, drop: 'gold_ore', vanilla: { sheet: 8, frame: 'auto' } });
def({ key: 'tree', name: '树干', solid: false, framed: true, opacity: 0.1, axe: 0, mapColor: '#6B4A2B', drop: 'wood', vanilla: { sheet: 5, frame: 'style', fw: 1, fh: 1 } });
def({ key: 'leaves', name: '树叶', decor: true, framed: true, opacity: 0.05, pick: 0, axe: 0, mapColor: '#2E8B3D', drop: null as unknown as string });
def({ key: 'wood', name: '木材块', solid: true, opacity: 1, pick: 0, mapColor: '#A97D4E', blend: true, drop: 'wood', vanilla: { sheet: 30, frame: 'auto' } });
def({ key: 'platform', name: '木平台', platform: true, opacity: 0.15, pick: 0, axe: 0, mapColor: '#B0885A', drop: 'platform', vanilla: { sheet: 19, frame: 'style', fw: 1, fh: 1 } });
def({ key: 'torch', name: '火把', decor: true, framed: true, opacity: 0, pick: 0, light: [255, 225, 150], mapColor: '#FDDD03', drop: 'torch', vanilla: { sheet: 4, frame: 'style', fw: 1, fh: 1 } });
// 注：火把光值见下（更亮版本）
def({ key: 'workbench', name: '工作台', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#A97D4E', drop: 'workbench', vanilla: { sheet: 18, frame: 'style', fw: 2, fh: 1 } });
def({ key: 'furnace', name: '熔炉', solid: true, framed: true, opacity: 1, pick: 0, w: 3, h: 2, light: [255, 140, 70], mapColor: '#5A5A5A', drop: 'furnace', vanilla: { sheet: 17, frame: 'style', fw: 3, fh: 2 } });
def({ key: 'anvil', name: '铁砧', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#6E6E78', drop: 'anvil', vanilla: { sheet: 16, frame: 'style', fw: 2, fh: 1 } });
def({ key: 'chest', name: '宝箱', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#D4A017', drop: 'chest', vanilla: { sheet: 21, frame: 'style', fw: 2, fh: 2 } });
def({ key: 'door_closed', name: '门', solid: true, framed: true, opacity: 0.05, pick: 0, w: 1, h: 3, mapColor: '#A97D4E', drop: 'door', vanilla: { sheet: 10, frame: 'style', fw: 1, fh: 3 } });
def({ key: 'door_open', name: '门(开)', decor: true, framed: true, opacity: 0, pick: 0, w: 2, h: 3, mapColor: '#A97D4E', drop: 'door', vanilla: { sheet: 11, frame: 'style', fw: 2, fh: 3 } });
def({ key: 'mushroom', name: '蘑菇', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#C36927', drop: 'mushroom_item', vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
def({ key: 'flower', name: '花', decor: true, framed: true, opacity: 0, pick: 0, mapColor: '#D0699E', drop: null as unknown as string, vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
def({ key: 'tallgrass', name: '草丛', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#1E9648', drop: 'acorn', vanilla: { sheet: 3, frame: 'style', fw: 1, fh: 1 } });
def({ key: 'sand', name: '沙块', solid: true, opacity: 1, pick: 0, mapColor: '#FFDA38', blend: true, drop: 'sand_block', vanilla: { sheet: 53, frame: 'blend' } });
def({ key: 'snow', name: '雪块', solid: true, opacity: 1, pick: 0, mapColor: '#E8F0F4', blend: true, drop: 'snow_block', vanilla: { sheet: 147, frame: 'blend' } });
def({ key: 'acorn_sapling', name: '树苗', decor: true, framed: true, opacity: 0, pick: 0, axe: 0, mapColor: '#6B4A2B', drop: 'acorn', vanilla: { sheet: 20, frame: 'style', fw: 1, fh: 1 } });
def({ key: 'ash', name: '灰烬块', solid: true, opacity: 1, pick: 0, mapColor: '#44444C', blend: true, drop: 'stone_block', vanilla: { sheet: 57, frame: 'auto' } });

// ===================== 原版素材图块（terraria-assets + TEdit 数据） =====================
// 4a：矿石 / 宝石 / 冰雪 / 沙漠 / 基础方块（1x1 实心，frame:'auto' 8 向贴合）
// mapColor/pick 取自 TEdit tiles.json；sheet = 原版 Tiles_N 表 id

// ---- 矿石（含替代矿与困难模式矿，后者先只做美术） ----
def({ key: 'ore_tin', name: '锡矿', solid: true, opacity: 1, pick: 0, mapColor: '#817D5D', drop: 'tin_ore', vanilla: { sheet: 166, frame: 'auto' } });
def({ key: 'ore_lead', name: '铅矿', solid: true, opacity: 1, pick: 0, mapColor: '#3E5272', drop: 'lead_ore', vanilla: { sheet: 167, frame: 'auto' } });
def({ key: 'ore_tungsten', name: '钨矿', solid: true, opacity: 1, pick: 20, mapColor: '#849D7F', drop: 'tungsten_ore', vanilla: { sheet: 168, frame: 'auto' } });
def({ key: 'ore_platinum', name: '铂金矿', solid: true, opacity: 1, pick: 40, mapColor: '#98ABC6', drop: 'platinum_ore', vanilla: { sheet: 169, frame: 'auto' } });
def({ key: 'ore_demonite', name: '魔矿', solid: true, opacity: 1, pick: 55, mapColor: '#625FA7', drop: 'demonite_ore', vanilla: { sheet: 22, frame: 'auto' } });
def({ key: 'ore_meteorite', name: '陨石', solid: true, opacity: 1, pick: 50, mapColor: '#685654', drop: 'meteorite', vanilla: { sheet: 37, frame: 'auto' } });
def({ key: 'ore_hellstone', name: '狱石', solid: true, opacity: 1, pick: 70, mapColor: '#8E4242', drop: 'hellstone', light: [255, 90, 40], vanilla: { sheet: 58, frame: 'auto' } });
def({ key: 'ore_crimtane', name: '猩红矿', solid: true, opacity: 1, pick: 65, mapColor: '#7D3741', drop: 'crimtane_ore', vanilla: { sheet: 204, frame: 'auto' } });
def({ key: 'ore_cobalt', name: '钴矿', solid: true, opacity: 1, pick: 65, mapColor: '#0B508F', drop: 'cobalt_ore', vanilla: { sheet: 107, frame: 'auto' } });
def({ key: 'ore_mythril', name: '秘银矿', solid: true, opacity: 1, pick: 65, mapColor: '#5BA9A9', drop: 'mythril_ore', vanilla: { sheet: 108, frame: 'auto' } });
def({ key: 'ore_adamantite', name: '精金矿', solid: true, opacity: 1, pick: 65, mapColor: '#801A34', drop: 'adamantite_ore', vanilla: { sheet: 111, frame: 'auto' } });
def({ key: 'ore_palladium', name: '钯金矿', solid: true, opacity: 1, pick: 65, mapColor: '#EF5A32', drop: 'palladium_ore', vanilla: { sheet: 221, frame: 'auto' } });
def({ key: 'ore_orichalcum', name: '山铜矿', solid: true, opacity: 1, pick: 65, mapColor: '#E760E4', drop: 'orichalcum_ore', vanilla: { sheet: 222, frame: 'auto' } });
def({ key: 'ore_titanium', name: '钛矿', solid: true, opacity: 1, pick: 65, mapColor: '#395565', drop: 'titanium_ore', vanilla: { sheet: 223, frame: 'auto' } });
def({ key: 'ore_chlorophyte', name: '叶绿矿', solid: true, opacity: 1, pick: 65, mapColor: '#BFE973', drop: 'chlorophyte_ore', vanilla: { sheet: 211, frame: 'auto' } });

// ---- 宝石矿（掉对应宝石） ----
def({ key: 'gem_sapphire', name: '蓝宝石矿', solid: true, opacity: 1, pick: 30, mapColor: '#6E8CB6', drop: 'sapphire', vanilla: { sheet: 63, frame: 'auto' } });
def({ key: 'gem_ruby', name: '红宝石矿', solid: true, opacity: 1, pick: 30, mapColor: '#C46072', drop: 'ruby', vanilla: { sheet: 64, frame: 'auto' } });
def({ key: 'gem_emerald', name: '翡翠矿', solid: true, opacity: 1, pick: 30, mapColor: '#389661', drop: 'emerald', vanilla: { sheet: 65, frame: 'auto' } });
def({ key: 'gem_topaz', name: '黄玉矿', solid: true, opacity: 1, pick: 30, mapColor: '#A0763A', drop: 'topaz', vanilla: { sheet: 66, frame: 'auto' } });
def({ key: 'gem_amethyst', name: '紫水晶矿', solid: true, opacity: 1, pick: 30, mapColor: '#8C3AA6', drop: 'amethyst', vanilla: { sheet: 67, frame: 'auto' } });
def({ key: 'gem_diamond', name: '钻石矿', solid: true, opacity: 1, pick: 30, mapColor: '#7DBFC5', drop: 'diamond', vanilla: { sheet: 68, frame: 'auto' } });

// ---- 冰雪 ----
def({ key: 'ice', name: '冰块', solid: true, opacity: 1, pick: 0, mapColor: '#90C3E8', blend: true, drop: 'ice_block', vanilla: { sheet: 161, frame: 'auto' } });
def({ key: 'thin_ice', name: '薄冰', solid: true, opacity: 1, pick: 0, mapColor: '#B8DBF0', blend: true, drop: 'ice_block', vanilla: { sheet: 162, frame: 'auto' } });
def({ key: 'ice_brick', name: '冰砖', solid: true, opacity: 1, pick: 0, mapColor: '#7CAFC9', blend: true, drop: 'ice_brick', vanilla: { sheet: 206, frame: 'auto' } });
def({ key: 'snow_brick', name: '雪砖', solid: true, opacity: 1, pick: 0, mapColor: '#B5D3D2', blend: true, drop: 'snow_brick', vanilla: { sheet: 148, frame: 'auto' } });

// ---- 沙漠 / 基础方块 ----
def({ key: 'sandstone', name: '沙岩', solid: true, opacity: 1, pick: 0, mapColor: '#C67C4E', blend: true, drop: 'sandstone_block', vanilla: { sheet: 396, frame: 'auto' } });
def({ key: 'hardened_sand', name: '硬化沙块', solid: true, opacity: 1, pick: 0, mapColor: '#D4C064', blend: true, drop: 'hardened_sand_block', vanilla: { sheet: 397, frame: 'auto' } });
def({ key: 'desert_fossil', name: '沙漠化石', solid: true, opacity: 1, pick: 0, mapColor: '#8C543C', blend: true, drop: 'desert_fossil', vanilla: { sheet: 404, frame: 'auto' } });
def({ key: 'clay', name: '粘土块', solid: true, opacity: 1, pick: 0, mapColor: '#925144', blend: true, drop: 'clay_block', vanilla: { sheet: 40, frame: 'auto' } });
def({ key: 'glass', name: '玻璃', solid: true, opacity: 0.15, pick: 0, mapColor: '#C8F6FE', drop: 'glass', vanilla: { sheet: 54, frame: 'auto' } });
def({ key: 'obsidian', name: '黑曜石', solid: true, opacity: 1, pick: 40, mapColor: '#2B2854', blend: true, drop: 'obsidian', vanilla: { sheet: 56, frame: 'auto' } });
def({ key: 'gray_brick', name: '灰砖', solid: true, opacity: 1, pick: 0, mapColor: '#909090', blend: true, drop: 'gray_brick', vanilla: { sheet: 38, frame: 'auto' } });
def({ key: 'red_brick', name: '红砖', solid: true, opacity: 1, pick: 0, mapColor: '#B53E3B', blend: true, drop: 'red_brick', vanilla: { sheet: 39, frame: 'auto' } });
def({ key: 'mud', name: '泥块', solid: true, opacity: 1, pick: 0, mapColor: '#5C4449', blend: true, drop: 'mud_block', vanilla: { sheet: 59, frame: 'blend' } });

```


---

## 🤖 Assistant · 2026-08-09T10:49:14.474Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 260,340p ~/Project/GLM/SandboxWorld/game/src/data/items.ts; echo ----; grep -n \"place_v_\\|function place\\|maxStack: 99, tile\" ~/Project/GLM/SandboxWorld/game/src/data/items.ts | head -20",
 "description": "Read items.ts wld-compat item section"
}
```


---

## 🤖 Assistant · 2026-08-09T10:49:14.481Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"fullbright\\|debugMode\\|drawDebugOverlay\\|compositeLight\" ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts | head -20",
 "description": "Find overlay toggles in Renderer"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:14.501Z

**📎 ToolResult**

```
99:  debugMode = false;
299:    this.compositeLight(cam, viewW, viewH, lightR, lightG, lightB, lightRX, lightRY, lightRW, lightRH);
355:    if (this.debugMode) this.drawDebugOverlay(ctx, cam, viewW, viewH, player, entities, mouseX, mouseY, hover);
939:  fullbright = false;
941:  private compositeLight(
946:    if (this.fullbright) return; // 开灯：不做 multiply，全部原色
1259:  private drawDebugOverlay(

```


---

## 👤 User(sidechain) · 2026-08-09T10:49:14.509Z

**📎 ToolResult**

```
// ===================== wld 导入补全物品（compat-report 驱动） =====================
// 这些物品目前只做图标与存档保留（占位），后续按需实装功能
item({ key: 'vi_2350_recall_potion', name: 'Recall Potion', maxStack: 999, value: 1 });
item({ key: 'vi_188_healing_potion', name: 'Healing Potion', maxStack: 999, value: 1 });
item({ key: 'vi_282_glowstick', name: 'Glowstick', maxStack: 999, value: 1 });
item({ key: 'vi_41_flaming_arrow', name: 'Flaming Arrow', maxStack: 999, value: 1 });
item({ key: 'vi_167_dynamite', name: 'Dynamite', maxStack: 999, value: 1 });
item({ key: 'vi_279_throwing_knife', name: 'Throwing Knife', maxStack: 999, value: 1 });
item({ key: 'vi_51_jester_s_arrow', name: 'Jester\'s Arrow', maxStack: 999, value: 1 });
item({ key: 'vi_19_gold_bar', name: 'Gold Bar', maxStack: 999, value: 1 });
item({ key: 'vi_302_water_walking_potion', name: 'Water Walking Potion', maxStack: 999, value: 1 });
item({ key: 'vi_305_gravitation_potion', name: 'Gravitation Potion', maxStack: 999, value: 1 });
item({ key: 'vi_43_suspicious_looking_eye', name: 'Suspicious Looking Eye', maxStack: 999, value: 1 });
item({ key: 'vi_296_spelunker_potion', name: 'Spelunker Potion', maxStack: 999, value: 1 });
item({ key: 'vi_299_night_owl_potion', name: 'Night Owl Potion', maxStack: 999, value: 1 });
item({ key: 'vi_965_rope', name: 'Rope', maxStack: 999, value: 1 });
item({ key: 'vi_303_archery_potion', name: 'Archery Potion', maxStack: 999, value: 1 });
item({ key: 'vi_304_hunter_potion', name: 'Hunter Potion', maxStack: 999, value: 1 });
item({ key: 'vi_50_magic_mirror', name: 'Magic Mirror', maxStack: 999, value: 1 });
item({ key: 'vi_42_shuriken', name: 'Shuriken', maxStack: 999, value: 1 });
item({ key: 'vi_295_featherfall_potion', name: 'Featherfall Potion', maxStack: 999, value: 1 });
item({ key: 'vi_53_cloud_in_a_bottle', name: 'Cloud in a Bottle', maxStack: 999, value: 1 });
item({ key: 'vi_2329_dangersense_potion', name: 'Dangersense Potion', maxStack: 999, value: 1 });
item({ key: 'vi_40_wooden_arrow', name: 'Wooden Arrow', maxStack: 999, value: 1 });
item({ key: 'vi_975_shoe_spikes', name: 'Shoe Spikes', maxStack: 999, value: 1 });
item({ key: 'vi_54_hermes_boots', name: 'Hermes Boots', maxStack: 999, value: 1 });
item({ key: 'vi_301_thorns_potion', name: 'Thorns Potion', maxStack: 999, value: 1 });
item({ key: 'vi_49_band_of_regeneration', name: 'Band of Regeneration', maxStack: 999, value: 1 });
item({ key: 'vi_2326_titan_potion', name: 'Titan Potion', maxStack: 999, value: 1 });
item({ key: 'vi_297_invisibility_potion', name: 'Invisibility Potion', maxStack: 999, value: 1 });
item({ key: 'vi_166_bomb', name: 'Bomb', maxStack: 999, value: 1 });
item({ key: 'vi_5011_mace', name: 'Mace', maxStack: 999, value: 1 });
item({ key: 'vi_4425_shark_bait', name: 'Shark Bait', maxStack: 999, value: 1 });
item({ key: 'vi_2351_teleportation_potion', name: 'Teleportation Potion', maxStack: 999, value: 1 });
item({ key: 'vi_4460_sandcastle_bucket', name: 'Sandcastle Bucket', maxStack: 999, value: 1 });
item({ key: 'vi_168_grenade', name: 'Grenade', maxStack: 999, value: 1 });
item({ key: 'vi_227_restoration_potion', name: 'Restoration Potion', maxStack: 999, value: 1 });
item({ key: 'vi_930_flare_gun', name: 'Flare Gun', maxStack: 999, value: 1 });
item({ key: 'vi_931_flare', name: 'Flare', maxStack: 999, value: 1 });
item({ key: 'vi_997_extractinator', name: 'Extractinator', maxStack: 999, value: 1 });
item({ key: 'vi_52_angel_statue', name: 'Angel Statue', maxStack: 999, value: 1 });
item({ key: 'vi_265_hellfire_arrow', name: 'Hellfire Arrow', maxStack: 999, value: 1 });
item({ key: 'vi_298_shine_potion', name: 'Shine Potion', maxStack: 999, value: 1 });
item({ key: 'vi_5007_dead_man_s_sweater', name: 'Dead Man\'s Sweater', maxStack: 999, value: 1 });
item({ key: 'vi_117_meteorite_bar', name: 'Meteorite Bar', maxStack: 999, value: 1 });
item({ key: 'vi_186_breathing_reed', name: 'Breathing Reed', maxStack: 999, value: 1 });
item({ key: 'vi_329_shadow_key', name: 'Shadow Key', maxStack: 999, value: 1 });
item({ key: 'vi_974_ice_torch', name: 'Ice Torch', maxStack: 999, value: 1 });
item({ key: 'vi_2322_mining_potion', name: 'Mining Potion', maxStack: 999, value: 1 });
item({ key: 'vi_4915_tungsten_bullet', name: 'Tungsten Bullet', maxStack: 999, value: 1 });
item({ key: 'vi_946_umbrella', name: 'Umbrella', maxStack: 999, value: 1 });
item({ key: 'vi_939_web_slinger', name: 'Web Slinger', maxStack: 999, value: 1 });
item({ key: 'vi_4870_potion_of_return', name: 'Potion of Return', maxStack: 999, value: 1 });
item({ key: 'vi_288_obsidian_skin_potion', name: 'Obsidian Skin Potion', maxStack: 999, value: 1 });
item({ key: 'vi_31_bottle', name: 'Bottle', maxStack: 999, value: 1 });
item({ key: 'vi_211_feral_claws', name: 'Feral Claws', maxStack: 999, value: 1 });
item({ key: 'vi_4404_inner_tube', name: 'Inner Tube', maxStack: 999, value: 1 });
item({ key: 'vi_187_flipper', name: 'Flipper', maxStack: 999, value: 1 });
item({ key: 'vi_2198_ice_machine', name: 'Ice Machine', maxStack: 999, value: 1 });
item({ key: 'vi_274_dark_lance', name: 'Dark Lance', maxStack: 999, value: 1 });
item({ key: 'vi_285_aglet', name: 'Aglet', maxStack: 999, value: 1 });
item({ key: 'vi_213_staff_of_regrowth', name: 'Staff of Regrowth', maxStack: 999, value: 1 });
item({ key: 'vi_964_boomstick', name: 'Boomstick', maxStack: 999, value: 1 });
item({ key: 'vi_1293_lihzahrd_power_cell', name: 'Lihzahrd Power Cell', maxStack: 999, value: 1 });
item({ key: 'vi_2195_lihzahrd_furnace', name: 'Lihzahrd Furnace', maxStack: 999, value: 1 });
item({ key: 'vi_2766_solar_tablet_fragment', name: 'Solar Tablet Fragment', maxStack: 999, value: 1 });
item({ key: 'vi_300_battle_potion', name: 'Battle Potion', maxStack: 999, value: 1 });
item({ key: 'vi_2348_inferno_potion', name: 'Inferno Potion', maxStack: 999, value: 1 });
item({ key: 'vi_218_flamelash', name: 'Flamelash', maxStack: 999, value: 1 });
item({ key: 'vi_3019_hellwing_bow', name: 'Hellwing Bow', maxStack: 999, value: 1 });
item({ key: 'vi_112_flower_of_fire', name: 'Flower of Fire', maxStack: 999, value: 1 });
item({ key: 'vi_220_sunfury', name: 'Sunfury', maxStack: 999, value: 1 });
item({ key: 'vi_4345_can_of_worms', name: 'Can Of Worms', maxStack: 999, value: 1 });
item({ key: 'vi_953_climbing_claws', name: 'Climbing Claws', maxStack: 999, value: 1 });
item({ key: 'vi_3069_wand_of_sparking', name: 'Wand of Sparking', maxStack: 999, value: 1 });
item({ key: 'vi_212_anklet_of_the_wind', name: 'Anklet of the Wind', maxStack: 999, value: 1 });
item({ key: 'vi_2204_honey_dispenser', name: 'Honey Dispenser', maxStack: 999, value: 1 });
item({ key: 'vi_277_trident', name: 'Trident', maxStack: 999, value: 1 });
item({ key: 'vi_863_water_walking_boots', name: 'Water Walking Boots', maxStack: 999, value: 1 });
item({ key: 'vi_751_cloud', name: 'Cloud', maxStack: 999, value: 1 });
item({ key: 'vi_155_muramasa', name: 'Muramasa', maxStack: 999, value: 1 });
----
74:item({ key: 'acorn', name: '橡实', desc: '种在草块上会长成树', maxStack: 99, tile: 'acorn_sapling' });
641:// 每个 v_ 图块注册 place_v_<key> 放置物品(tryPlace 走 vanilla style 帧语义);

```


---

## 🤖 Assistant · 2026-08-09T10:49:18.095Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Check items.ts lines 630-724 (place_v_ registration), and also check the "teleporter" / statue / lever tile keys exist. Also check UI.ts toggle registration for toggles (like annotate). Also check Renderer.drawDebugOverlay to see overlay draw pattern, and compositeLight region. Also LightingEngine maybe. Also check HitTile. But I have enough. Let me quickly read items.ts 630-724 and grep for teleporter/statue keys in tiles.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:49:18.852Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 625,724p ~/Project/GLM/SandboxWorld/game/src/data/items.ts",
 "description": "Read place_v_ item registration block"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:18.881Z

**📎 ToolResult**

```
item({ key: 'vi_5499_froggy_neckband', name: 'Froggy Neckband', maxStack: 999, value: 1 });
item({ key: 'vi_5507_balloony_beads', name: 'Balloony Beads', maxStack: 999, value: 1 });
item({ key: 'vi_5485_chicken_charm', name: 'Chicken Charm', maxStack: 999, value: 1 });
item({ key: 'vi_5502_cat_chime', name: 'Cat Chime', maxStack: 999, value: 1 });
item({ key: 'vi_5504_turkey_wattle_necklace', name: 'Turkey Wattle Necklace', maxStack: 999, value: 1 });
item({ key: 'vi_5506_crow_s_beak', name: 'Crow\'s Beak', maxStack: 999, value: 1 });
item({ key: 'vi_5503_dog_collar', name: 'Dog Collar', maxStack: 999, value: 1 });
item({ key: 'vi_5534_fairy_choker', name: 'Fairy Choker', maxStack: 999, value: 1 });
item({ key: 'vi_5484_cow_bell', name: 'Cow Bell', maxStack: 999, value: 1 });
item({ key: 'vi_5501_old_companion_locket', name: 'Old Companion Locket', maxStack: 999, value: 1 });
item({ key: 'vi_5509_vampire_pendant', name: 'Vampire Pendant', maxStack: 999, value: 1 });
item({ key: 'vi_5505_mean_goblin_s_spikes', name: 'Mean Goblin\'s Spikes', maxStack: 999, value: 1 });
item({ key: 'vi_5525_cursed_piper_flute', name: 'Cursed Piper Flute', maxStack: 999, value: 1 });


// ---- 阶段 5:v_ 图块放置物品自动注册 + 掉落连线 ----
// 每个 v_ 图块注册 place_v_<key> 放置物品(tryPlace 走 vanilla style 帧语义);
// 无掉落的 v_ 图块 drop 连到该物品(破坏可回收再放置)。
import { TILE_DEFS } from './tiles';
for (const td of TILE_DEFS) {
  if (!td.key.startsWith('v_')) continue;
  const ik = 'place_' + td.key;
  if (byKey[ik] === undefined) {
    item({ key: ik, name: td.name, maxStack: 999, value: 1, tile: td.key });
  }
  // 掉落连线在读取端回退(World.breakTileAt),避免多模块实例下改写失效
}
void 0;

// ---- 阶段 5:生物群系草种子(种出对应草块)----
item({ key: 'corrupt_grass_seeds', name: '腐化草地种子', maxStack: 999, value: 1, tile: 'v_23_corrupt_grass_block' });
item({ key: 'crimson_grass_seeds', name: '猩红草地种子', maxStack: 999, value: 1, tile: 'v_199_crimson_grass_block' });
item({ key: 'jungle_grass_seeds', name: '丛林草地种子', maxStack: 999, value: 1, tile: 'v_60_jungle_grass_block' });
item({ key: 'mushroom_grass_seeds', name: '蘑菇草地种子', maxStack: 999, value: 1, tile: 'v_70_mushroom_grass_block' });


// ---- 阶段 5:原版物品全量注册(6146 件,图标走 atlas.vicon(id) 回退) ----
import vanillaItemMeta from '../../public/sprites/vanilla.json';
const _vim = (vanillaItemMeta as unknown as { items: Record<string, { name: string; key: string }> }).items ?? {};
for (const [idStr, m] of Object.entries(_vim)) {
  if (!m || typeof m.key !== 'string' || !m.key) continue;
  const ik = 'vi_' + idStr + '_' + m.key.replace(/[^A-Za-z0-9]/g, '');
  if (byKey[ik] !== undefined) continue;
  item({ key: ik, name: m.name, maxStack: 999, value: 1 });
}
void 0;

// ---- 阶段 6:功能道具(桶三态/绳圈) ----
item({ key: 'empty_bucket', name: '空桶', maxStack: 99, value: 1, desc: '右键舀取液体' });
item({ key: 'water_bucket', name: '水桶', maxStack: 1, value: 1, desc: '右键放置水' });
item({ key: 'lava_bucket', name: '岩浆桶', maxStack: 1, value: 1, desc: '右键放置岩浆' });
item({ key: 'honey_bucket', name: '蜂蜜桶', maxStack: 1, value: 1, desc: '右键放置蜂蜜' });

// ---- 阶段 6 第三轮:替代矿工具链(官方数值,与铜/铁/银/金同档) ----
item({ key: 'tin_pickaxe', name: '锡镐', maxStack: 1, value: 400,
  tool: { type: 'pick', power: 35, damage: 4, speed: 23, knockback: 2, reach: 2.6 * 16 } });
item({ key: 'tin_axe', name: '锡斧', maxStack: 1, value: 350,
  tool: { type: 'axe', power: 7, damage: 3, speed: 30, knockback: 4.5, reach: 2.4 * 16 } });
item({ key: 'tin_sword', name: '锡剑', maxStack: 1, value: 450,
  tool: { type: 'sword', damage: 8, speed: 23, knockback: 5, reach: 2.2 * 16 } });
item({ key: 'lead_pickaxe', name: '铅镐', maxStack: 1, value: 900,
  tool: { type: 'pick', power: 45, damage: 5, speed: 22, knockback: 2.5, reach: 2.6 * 16 } });
item({ key: 'lead_axe', name: '铅斧', maxStack: 1, value: 800,
  tool: { type: 'axe', power: 9, damage: 4, speed: 30, knockback: 5, reach: 2.4 * 16 } });
item({ key: 'lead_sword', name: '铅剑', maxStack: 1, value: 900,
  tool: { type: 'sword', damage: 10, speed: 23, knockback: 5, reach: 2.2 * 16 } });
item({ key: 'tungsten_pickaxe', name: '钨镐', maxStack: 1, value: 1800,
  tool: { type: 'pick', power: 55, damage: 6, speed: 21, knockback: 2.5, reach: 2.6 * 16 } });
item({ key: 'tungsten_axe', name: '钨斧', maxStack: 1, value: 1600,
  tool: { type: 'axe', power: 11, damage: 5, speed: 29, knockback: 5.5, reach: 2.4 * 16 } });
item({ key: 'tungsten_sword', name: '钨剑', maxStack: 1, value: 1800,
  tool: { type: 'sword', damage: 13, speed: 22, knockback: 5.5, reach: 2.2 * 16 } });
item({ key: 'platinum_pickaxe', name: '铂金镐', maxStack: 1, value: 3600,
  tool: { type: 'pick', power: 59, damage: 7, speed: 20, knockback: 3, reach: 2.6 * 16 } });
item({ key: 'platinum_axe', name: '铂金斧', maxStack: 1, value: 3200,
  tool: { type: 'axe', power: 13, damage: 6, speed: 28, knockback: 6, reach: 2.4 * 16 } });
item({ key: 'platinum_sword', name: '铂金剑', maxStack: 1, value: 3600,
  tool: { type: 'sword', damage: 15, speed: 22, knockback: 6, reach: 2.2 * 16 } });

// ---- 阶段 6 第五轮:弓箭系统(官方数值 Item.cs:2996-3010:木弓伤4/UseTime30/射速6.1/击退0) ----
item({ key: 'wooden_bow', name: '木弓', maxStack: 1, value: 100,
  ranged: { damage: 4, speed: 30, knockback: 0, ammo: 'wooden_arrow', projSpeed: 6.1 } });
item({ key: 'wooden_arrow', name: '木箭', maxStack: 999, value: 1 });
item({ key: 'flaming_arrow', name: '燃烧箭', maxStack: 999, value: 1 });
item({ key: 'iron_bow', name: '铁弓', maxStack: 1, value: 360,
  ranged: { damage: 11, speed: 25, knockback: 1.5, ammo: 'wooden_arrow', projSpeed: 11 } });

// ---- 阶段 6 第六轮:矿车 ----
item({ key: 'minecart_item', name: '矿车', maxStack: 99, value: 1, desc: '右键轨道放置并骑乘' });

// ---- 阶段 6 第八轮:魔法武器(官方 Item.cs:30765-30778,火花法杖=ItemID 3069:伤14/魔力2/UseTime26/射速7/暴击10) ----
item({ key: 'wand_of_sparking', name: '火花法杖', maxStack: 1, value: 100,
  magic: { damage: 14, speed: 26, manaCost: 2, projSpeed: 7, proj: 'spark' } });
item({ key: 'amethyst_bolt', name: '紫晶法杖', maxStack: 1, value: 900,
  magic: { damage: 14, speed: 26, manaCost: 5, projSpeed: 9, proj: 'bolt' } });

// ---- 阶段 6 第九轮:Boss 召唤物(官方:蠕虫食物 70/血腥脊椎 1331/史莱姆王冠 560) ----
item({ key: 'worm_food', name: '蠕虫食物', maxStack: 20, value: 1, desc: '腐化之地使用:召唤世界吞噬者' });
item({ key: 'bloody_spine', name: '血腥脊椎', maxStack: 20, value: 1, desc: '猩红之地使用:召唤克苏鲁之脑' });
item({ key: 'slime_crown', name: '史莱姆王冠', maxStack: 20, value: 1, desc: '任意时刻:召唤史莱姆王' });

```


---

## 🤖 Assistant · 2026-08-09T10:49:19.601Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"v_105_statue\\|v_235_teleporter\\|v_132_lever\\|v_136_switch\\|v_137_traps\\|v_135_pressure_plates\\|v_144_timers\\|v_130_active_stone_block\\|v_443_geyser\" ~/Project/GLM/SandboxWorld/game/src/data/tiles.ts | head",
 "description": "Find wiring-related tile registrations"
}
```


---

## 🤖 Assistant · 2026-08-09T10:49:19.609Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 930,1000p ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts; echo ----; sed -n 1259,1310p ~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts",
 "description": "Read compositeLight and drawDebugOverlay"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:19.640Z

**📎 ToolResult**

```
  /** 光照 gamma 曲线 LUT（指数 0.78）：提亮中间调，柔化光源边缘的"切黑"硬边 */
  private static lightLUT: Uint8Array = (() => {
    const t = new Uint8Array(256);
    for (let i = 0; i < 256; i++) t[i] = Math.round(255 * Math.pow(i / 255, 0.78));
    return t;
  })();

  /** 全亮模式（F9）：跳过光照合成，画面无暗影 */
  fullbright = false;

  private compositeLight(
    cam: Camera, viewW: number, viewH: number,
    lightR: Uint8Array, lightG: Uint8Array, lightB: Uint8Array,
    rx: number, ry: number, rw: number, rh: number,
  ) {
    if (this.fullbright) return; // 开灯：不做 multiply，全部原色
    const z = cam.zoom;
    const ts = TILE;
    const tilesX = Math.ceil(viewW / z / ts) + 2;
    const tilesY = Math.ceil(viewH / z / ts) + 2;
    const tx0 = Math.floor((cam.x - viewW / 2 / z) / ts);
    const ty0 = Math.floor((cam.y - viewH / 2 / z) / ts);
    // 2× 超采样：光照图每半格一个采样点，tile 中心间双线性插值，
    // 光斑梯度曲率更细腻（每格一采样时火把光斑有明显的马赛克棱面感）
    const SS = 2;
    const w2 = tilesX * SS, h2 = tilesY * SS;
    if (this.lightCanvas.width !== w2 || this.lightCanvas.height !== h2) {
      this.lightCanvas.width = w2;
      this.lightCanvas.height = h2;
    }
    const lc = this.lightCtx;
    const img = lc.createImageData(w2, h2);
    const lut = Renderer.lightLUT;
    // tile 中心光值采样（区域外 0，由环境光下限兜底）
    const tap = (gx: number, gy: number): [number, number, number] => {
      const tx = tx0 + gx, ty = ty0 + gy;
      if (tx >= rx && ty >= ry && tx < rx + rw && ty < ry + rh) {
        const li = (ty - ry) * rw + (tx - rx);
        return [lightR[li], lightG[li], lightB[li]];
      }
      return [0, 0, 0];
    };
    for (let py = 0; py < h2; py++) {
      const gy = py / SS - 0.5;              // 亚格坐标（tile 中心在整数处）
      const y0 = Math.floor(gy), fy = gy - y0;
      const wy0 = 1 - fy, wy1 = fy;
      for (let px = 0; px < w2; px++) {
        const gx = px / SS - 0.5;
        const x0 = Math.floor(gx), fx = gx - x0;
        const wx0 = 1 - fx, wx1 = fx;
        // 4 tap 双线性
        const a = tap(x0, y0), b = tap(x0 + 1, y0), c = tap(x0, y0 + 1), d = tap(x0 + 1, y0 + 1);
        const w00 = wx0 * wy0, w10 = wx1 * wy0, w01 = wx0 * wy1, w11 = wx1 * wy1;
        let r = a[0] * w00 + b[0] * w10 + c[0] * w01 + d[0] * w11;
        let g = a[1] * w00 + b[1] * w10 + c[1] * w01 + d[1] * w11;
        let b2 = a[2] * w00 + b[2] * w10 + c[2] * w01 + d[2] * w11;
        // gamma 柔化 + 最低可见度
        const amb = 10;
        const i = (py * w2 + px) * 4;
        img.data[i] = Math.max(lut[Math.min(255, Math.round(r))], amb);
        img.data[i + 1] = Math.max(lut[Math.min(255, Math.round(g))], amb);
        img.data[i + 2] = Math.max(lut[Math.min(255, Math.round(b2))], amb);
        img.data[i + 3] = 255;
      }
    }
    lc.putImageData(img, 0, 0);
    const ctx = this.ctx;
    ctx.save();
    ctx.imageSmoothingEnabled = true;
    ctx.globalCompositeOperation = 'multiply';
----
  private drawDebugOverlay(
    ctx: CanvasRenderingContext2D, cam: Camera, viewW: number, viewH: number,
    player: Player, entities: Entity[], mouseX: number, mouseY: number,
    hover: { x: number; y: number } | null,
  ) {
    const z = cam.zoom;
    const [mx, my] = cam.worldToScreen(mouseX, mouseY);
    const box = (e: { x: number; y: number; w: number; h: number; cx: number }, color: string, label?: string) => {
      const [sx, sy] = cam.worldToScreen(e.x, e.y);
      const sw = e.w * z, sh = e.h * z;
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 3]);
      ctx.strokeRect(sx, sy, sw, sh);
      ctx.setLineDash([]);
      if (label) {
        ctx.font = '10px monospace';
        ctx.fillStyle = color;
        ctx.fillText(label, sx + 2, sy - 3);
      }
    };
    // 主角碰撞盒（亮绿）
    box(player, '#00FF66', `player ${player.w}x${player.h} og:${player.onGround} vy:${player.vy.toFixed(1)}`);
    // 主角中心点
    const [pcx, pcy] = cam.worldToScreen(player.cx, player.cy);
    ctx.fillStyle = '#FF6600';
    ctx.fillRect(pcx - 2, pcy - 2, 4, 4);
    // 手持工具/武器的范围显示（与 Game 判定一致）：
    // 1) 近战判定圆：剑 = 完整 reach，镐/斧/锤 ×0.8，空手 3 格；圆心向朝向平移 reach×0.35
    // 2) 挖掘圆（镐/锤）：4.5 格（tryMine 范围）
    // 3) 砍树圆（斧）：4.5 格（同一 tryMine 通路，斧作用对象为树）
    {
      const held = player.inv.heldItem();
      const tool = held ? ITEM_DEFS[held.id]?.tool : undefined;
      const reach = (tool?.reach ?? TILE * 3) * (tool?.type === 'sword' ? 1 : tool ? 0.8 : 1);
      const circle = (cx: number, r: number, color: string, label: string) => {
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.5;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.arc(cx, pcy, r * z, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.font = '10px monospace';
        ctx.fillStyle = color;
        ctx.fillText(label, cx + 6, pcy - 6);
      };
      // 近战判定圆（朝向前移）
      const acx = pcx + player.facing * reach * 0.35 * z;
      circle(acx, reach, tool ? 'rgba(0,255,200,0.55)' : 'rgba(120,120,160,0.4)',
        `attack ${(reach / TILE).toFixed(1)} tiles${tool ? '' : ' (no tool)'}`);
      // 挖掘范围（镐/锤）

```


---

## 👤 User(sidechain) · 2026-08-09T10:49:19.643Z

**📎 ToolResult**

```
197:def({ key: 'v_130_active_stone_block', name: 'Active Stone Block', solid: true, opacity: 1, pick: 0, mapColor: '#A0A0A0', blend: true, drop: null as unknown as string, vanilla: { sheet: 130, frame: 'auto' } });
202:def({ key: 'v_137_traps', name: 'Traps', solid: true, opacity: 1, pick: 0, mapColor: '#909490', blend: true, drop: null as unknown as string, vanilla: { sheet: 137, frame: 'auto' } });
234:def({ key: 'v_105_statue', name: 'Statue', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 3, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 105, frame: 'style', fw: 2, fh: 3 } });
248:def({ key: 'v_135_pressure_plates', name: 'Pressure Plates', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#FD7272', drop: null as unknown as string, vanilla: { sheet: 135, frame: 'style', fw: 1, fh: 1 } });
261:def({ key: 'v_443_geyser', name: 'Geyser', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 1, mapColor: '#7b7b7b', drop: null as unknown as string, vanilla: { sheet: 443, frame: 'style', fw: 2, fh: 1 } });
287:def({ key: 'v_136_switch', name: 'Switch', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#D5CBCC', drop: null as unknown as string, vanilla: { sheet: 136, frame: 'style', fw: 1, fh: 1 } });
340:def({ key: 'v_235_teleporter', name: 'Teleporter', solid: true, framed: true, opacity: 1, pick: 0, w: 3, h: 1, mapColor: '#D6B82E', drop: null as unknown as string, vanilla: { sheet: 235, frame: 'style', fw: 3, fh: 1 } });
377:def({ key: 'v_144_timers', name: 'Timers', solid: false, framed: true, opacity: 0.05, pick: 0, w: 1, h: 1, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 144, frame: 'style', fw: 1, fh: 1 } });
380:def({ key: 'v_132_lever', name: 'Lever', solid: false, framed: true, opacity: 0.05, pick: 0, w: 2, h: 2, mapColor: '#909490', drop: null as unknown as string, vanilla: { sheet: 132, frame: 'style', fw: 2, fh: 2 } });

```


---

## 🤖 Assistant · 2026-08-09T10:49:23.616Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I now have a very complete picture. A couple more small things worth confirming:

- UI.ts toggle registration pattern for annotate (already seen via main.ts).
- HitTile.ts (damage array keyed by tile) — minor, skip or quick check.
- LightingEngine fields (r,g,b, rx, ry, rw, rh, liquidDirty) — mentioned in Game.
- Check `frameX` semantics for lever (2x2) and switch — toggleSwitch flips frameX>=18. OK.
- Check `GameHooks` interface (src/entities/types.ts) — useful for wiring update hooks. Let me quickly read types.ts.
- Also check if `tpMark` in Renderer.
- Also check `UI.ts` how toast/toggle work (for wire overlay toggle maybe). Not strictly needed.

Let me read types.ts quickly and HitTile briefly.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:49:23.618Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/types.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:23.637Z

**📎 ToolResult**

```
1	// 实体与 Game 交互的接口（避免循环依赖，只放类型）
2	import type { World } from '../world/World';
3	
4	export interface GameHooks {
5	  world: World;
6	  /** 主角(投射物命中判定用) */
7	  player: import('./Player').Player;
8	  /** 敌人列表(投射物命中判定用) */
9	  enemies(): unknown[];
10	  /** 在世界上生成掉落物 */
11	  spawnDrop(x: number, y: number, itemKey: string, count?: number, vx?: number, vy?: number): void;
12	  /** 对玩家造成伤害（attacker 用于荆棘反伤） */
13	  damagePlayer(dmg: number, srcX: number, srcY: number, attacker?: unknown): void;
14	  /** 伤害数字飘字 */
15	  addDamageNumber(x: number, y: number, amount: number, crit: boolean, color?: string): void;
16	  /** 敌人死亡 */
17	  onEnemyKilled(key: string): void;
18	  /** 出生敌人 */
19	  spawnEnemy(key: string, x: number, y: number): void;
20	  /** 粒子 */
21	  spawnParticles(
22	    x: number, y: number, color: string, count: number, speed?: number,
23	    opts?: { life?: number; damp?: number; grav?: number },
24	  ): void;
25	  /** 拾取物品后刷新 UI（掉落物实体调用） */
26	  notifyInventoryChanged(): void;
27	  /** 播放音效 */
28	  playSfx(name: string, vol?: number): void; // vol 0-1 按距离衰减
29	  playSfxFiles(files: string[], vol?: number): void; // 怪物专属声效（原版文件名列表）
30	  /** 拾取物品时在主角旁飘出物品名 */
31	  showPickupLabel(itemKey: string): void;
32	}
33	

```


---

## 🤖 Assistant · 2026-08-09T10:49:23.675Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/HitTile.ts",
 "limit": 60
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:49:23.686Z

**📎 ToolResult**

```
1	// 原版劈砍/挖掘伤害积累系统：Terraria1405/HitTile.cs 移植。
2	// 每次挥击对目标格积累伤害（阈值 100 破坏），停止攻击后按 TTL 分档衰减：
3	//   TTL<48 → -2/帧, <36 → -5, <24 → -7, <12 → -10；归零清除（原版 Prune 语义）
4	// 槽位用插入序 Map 简化（原版 500 槽 + order 换序，行为等价：最近使用的存活最久）
5	export interface HitTileEntry { damage: number; ttl: number }
6	
7	export class HitTile {
8	  private data = new Map<string, HitTileEntry>();
9	  private static readonly CAP = 500;
10	  private static readonly TTL = 60;
11	
12	  /** 命中目标格：积累伤害并重置 TTL。返回积累后的伤害值 */
13	  addDamage(x: number, y: number, amount: number, type = 1): number {
14	    const key = `${x},${y},${type}`;
15	    let e = this.data.get(key);
16	    if (!e) {
17	      // 容量控制：超过上限淘汰最旧条目（原版环形缓冲的等价行为）
18	      if (this.data.size >= HitTile.CAP) {
19	        const oldest = this.data.keys().next().value;
20	        if (oldest !== undefined) this.data.delete(oldest);
21	      }
22	      e = { damage: 0, ttl: HitTile.TTL };
23	      this.data.set(key, e);
24	    }
25	    e.damage += amount;
26	    e.ttl = HitTile.TTL;
27	    // 最近使用移到末尾（LRU 语义）
28	    this.data.delete(key);
29	    this.data.set(key, e);
30	    return e.damage;
31	  }
32	
33	  /** 读取当前积累伤害（不改 TTL） */
34	  getDamage(x: number, y: number, type = 1): number {
35	    return this.data.get(`${x},${y},${type}`)?.damage ?? 0;
36	  }
37	
38	  /** 清除指定格（破坏完成/格已空时调用） */
39	  clear(x: number, y: number, type = 1) {
40	    this.data.delete(`${x},${y},${type}`);
41	  }
42	
43	  clearAll() {
44	    this.data.clear();
45	  }
46	
47	  /** 每帧衰减（原版 HitTile.Prune 分档） */
48	  update() {
49	    for (const [key, e] of [...this.data]) {
50	      e.ttl--;
51	      if (e.ttl <= 1) { this.data.delete(key); continue; }
52	      if (e.ttl < 12) e.damage -= 10;
53	      else if (e.ttl < 24) e.damage -= 7;
54	      else if (e.ttl < 36) e.damage -= 5;
55	      else if (e.ttl < 48) e.damage -= 2;
56	      if (e.damage < 0) this.data.delete(key);
57	    }
58	  }
59	}
60	

```


---

## 🤖 Assistant · 2026-08-09T10:50:16.129Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I have everything I need. Now write the structured report with exact file:line references.

Let me compile key line numbers:

**TileStore.ts** (~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts)
- Fields: lines 5-15: w, h (readonly), type Uint16Array, flags Uint8Array (bit0 active, bit1 framedDecor placeholder 预留!), frameX Uint16Array, frameY Uint16Array, wall Uint16Array, liquid Uint8Array, liquidType Uint8Array, half Uint8Array, slope Uint8Array.
- listeners: line 18; liquidListeners line 64.
- constructor lines 20-32, n = w*h.
- idx() line 34 = y*w+x.
- inBounds 36-38, get 40, isActive 42, isSolid 46, isPlatform 52.
- onTileChanged 58-60.
- setTile 70-79 (type, frameX, frameY; clears half/slope when type 0; notifies listeners).
- setHalfBrick 82-87, setSlope 89-95 (slope clears half).
- setTileSilent 97-105.
- setWall 107-114, setWallSilent 116-119.
- setLiquid 121-129 → liquidListeners only.
- Note: flags bit1 is documented as 预留 (reserved) — spare capacity. No other spare arrays. half/slope stored as full Uint8Array per tile (not packed into flags), separate from vanilla bit layout.

**Save format** SaveFile.ts
- SaveData interface 45-69: format 'sandboxworld.save', version: number (currently 2 at line 114), header {...} incl wldVersion?, clock, tiles/walls/liquid/liquidType base64 RLE strings, chests, player, npcs, flags.
- rlePairs 71-84, rleTiles 86-103 (per-tile: varint(run-1) varint(type) [fx fy if type!=0]).
- saveGame 105-136; ghost purge 109-111.
- loadSave 138-212; wall legacy migration with version<2 (176-188); liquidType default '' fallback (189-199).
- No checksum. Versioning via `version` field; migration example exists.
- Where new per-tile wire byte array slots: add `wire: string` to SaveData next to liquidType (line 60), encode with rlePairs(st.wire), decode in a block mirroring 189-199, bump version to 3 or treat missing field as all-zero like liquidType.

KvStore.ts: IndexedDB 'sandboxworld'/'kv' + localStorage fallback; kvHas/kvGet/kvSet (≤2MB → localStorage)/kvDelete. Strings only.

World.ts fields: store, name, seed, spawnX/spawnY, groundLevel/rockLevel, clock, chests, flags, trees, explored Uint8Array, treeX/treeStyle, crimson, dungeonX, jungleX, treeTops, exploredVersion; breakTileAt 81-88; registerTree 99. No versioning field on World itself (wldVersion lives only in SaveData header).

**WldParser.ts**
- WldTileData 7-15: active, type, frameX, frameY, wall, liquid, liquidType. No wire arrays.
- decodeTiles 274-349. Tile block layout:
  - header1 = u8 (line 290); header2 if header1&0x01 (292); header3 if header2&0x01 (293); header4 if version>=269 && header3&0x01 (294) — header4 read but `void header4` (295): unused.
  - header1 & 0x02 → active; &0x20 → u16 tileType else u8 (299-305).
  - framed → fx,fy u16 (306-310).
  - header3 & 0x08 → tile color (311).
  - header1 & 0x04 → wall u8; header3&0x10 wall color; version>=222 && header3&0x40 → high wall byte (313-320).
  - liquid: (header1 & 0x18) >> 3 (321).
  - RLE: (header1 & 0xC0) >> 6 (328-331).
- So vanilla wire bits live in header2/header3 but are NOT parsed:
  - Vanilla (TEdit World.FileV2.cs): header2 bit1(0x02)=red wire, bit2(0x04)=blue wire, bit3(0x08)=green wire, bit4(0x10)=yellow wire, bit5(0x20)=actuator, bit6(0x40)=actuator's active state ("halfBlock"/inactive via bTileHeader3 actually); header3 bit4(0x08)=tileColor present, bit5(0x10)=wallColor, bit3(0x04)? Let me be precise based on TEdit: 
    - header2: bit1 (0x02) red wire, bit2 (0x04) blue, bit3 (0x08) green, bit4 (0x10) yellow, bit5 (0x20) actuator, bit6 (0x40) active and actuator (b3 bTileFrameNumber?) Actually TEdit: `if (bit2) tile2 = ...;` flags: TileImportant... In TEdit FileRework/World.FileV2.cs `LoadTileTiles`: 
      ```
      if ((tileData1 & 1) != 0) { // has more
        tileData2 = reader.ReadByte();
        tile.HasRedWire = ... actually:
      ```
      Known standard mapping (from TEdit & tModPorter):
      header2: 0x01 = has header3; 0x02 = red wire; 0x04 = blue wire; 0x08 = green wire; 0x10 = yellow wire; 0x20 = actuator; 0x40 = "actuator active" (tile is in inactive state, stored in bTileHeader half? Actually 0x40 = checkingLiquid? no).
      Actually in TEdit WorldFile.LoadTileTiles:
      ```
      if ((tileData[0] & Flags1.hasExtraTile) != 0) ...
      tileData[1]: Flags2: 1 = hasMoreFlags, 2 = redWire, 4 = blueWire, 8 = greenWire, 16 = yellowWire, 32 = actuator, 64 = actuator'sActiveState
      tileData[2]: Flags3: 1 = hasMoreFlags (header4 for v269), 2 = slope flag? Actually flags3: 1 = hasFourth, 2 = slope2, 4 = slope1, 8 = tileColor, 16 = wallColor, 32 = goldWire?? no...
      ```
      Precisely (Terraria TileHeader Flags3): bit1 (0x02) = slope var 2, bit2 (0x04) = slope var 1, bit3 (0x08) = tile color, bit4 (0x10) = wall color, bit5 (0x20) = gold brick blend? Hmm — Flags3: unknown1 = 2 (slope), unknown2 = 4 (slope), unknown3 = 8 (tileActiveColor), unknown4 = 16 (wallColor), unknown5 = 32 (slope frame?), unknown6 = 64 (wall > 255, high byte), unknown7 = 128 (liquid > 255 indicator / shimmer).
      This parser already uses header3 & 0x08 (tile color), 0x10 (wall color), 0x40 (wall high byte, v222+), 0x80 (shimmer liquid v269+). That's consistent with Flags3: 0x08 tileColor, 0x10 wallColor, 0x40 = wall high byte?? Hmm, in vanilla Flags3: unknown6 = 64 is actually "wall amount > 255"... whatever. The parser is internally consistent.
      
      For wires: header2 bits 0x02 red, 0x04 blue, 0x08 green, 0x10 yellow, 0x20 actuator, 0x40 actuator active (inactive block state). These are parsed nowhere — decodeTiles reads header2 only for the 0x01 bit (line 293) and never for 0x02-0x40.
- Where they'd be extracted: in decodeTiles after reading header2/header3 (lines 290-295), store into new WldTileData arrays (e.g., wire: Uint8Array, actuator: Uint8Array), then write in the RLE fill loop at 334-343. Then in WldImport.parseWldToSave (line 730-758 loop) copy into new arrays, and add to SaveData at 796-830.
- Also note: the parser ignores half/slope too (header3 0x02/0x04 bits) — TileStore has half/slope arrays but wld import doesn't populate them.

**Items & placement**
- items.ts: ItemDef interface lines 8-47; registration helper `item()` 53-56 (maxStack default 999, byKey index). Fields: key, name, maxStack, tile?, placeStyle?, magic?, ranged?, wall?, tool? {type, power, damage, speed, knockback, reach}, heal?, potion?, accessory?, armor?, value?, desc?.
- Note `wall?: string` field exists for wall placement items but tryPlace doesn't handle walls (hammer removes walls; there's no wall placing item flow in Game). Let me verify — grep for itemDef.wall usage in Game.ts. I didn't see one. Let me check quickly. Actually I should verify to be accurate.
- place_v_ auto-registration: items.ts 641-655 (for each v_ tile, item place_v_<key> with tile: td.key, maxStack 999). So levers/switches/teleporters/timers/statues already have placement items: place_v_132_lever, place_v_136_switch, place_v_137_traps, place_v_135_pressure_plates, place_v_235_teleporter, place_v_144_timers, place_v_105_statue, place_v_130_active_stone_block, place_v_443_geyser.
- vi_509_red_wrench exists as item (registered from vanilla.json, inert).
- Game.updateUse (667-893): right-click dispatch 718-737 (chest → npc → suspicious_eye → interactAt). Tools 757-778. Placement 781-784: `if (heldDef?.tile && !inp.rightDown) this.tryPlace(tx,ty,heldDef)`. Wrench-like tool hook: add a branch before 781 checking e.g. `heldDef.wireTool`, handling place-on-existing-tile; deduct with inv.removeAt(selected,1), useTime=14, sfx 'place' — pattern from rope branch (1236-1251) and tryPlace ending (1309-1312).
- tryPlace 1220-1313: range check 5.5 tiles (1224-1226), tileId lookup (1227), acorn special (1230), rope special (1236-1251), space check loop (1253-1261) incl overlapsEntity for solid, support check 1263-1264 (hasSupport 1324-1339), useTime gate 1265, placement loop 1269-1305 with vanilla style frames (placeStyle * strideX + dx*18, dy*18), chest registration 1306-1308, consume 1309, useTime 14 (1310), sfx place (1311).
- overlapsEntity 1315-1322 (player + enemies AABB).
- breakTile flow 1022-1099: door → clearDoorAt (1043-1048), multi-tile objects anchor walk 1050-1067 (frameX/18 normalization), chest dump 1065, generic 1092-1098. setTile(x,y,0) does NOT clear wall/wires currently; half/slope cleared at TileStore 77/104.
- Mining: tryMine 903-999 — HitTile.addDamage, threshold 100 → breakTile (990-993).
- interactAt 1341-1376: doors (1344-1347), chest, crystal_heart, bed spawn, lever/switch (1362-1364 → toggleSwitch), herb harvest.
- toggleSwitch 1422-1430: flips frameX 0/18, sfx tink, fireTrapsFrom(x,y,!on), rightDown=false.
- fireTrapsFrom 1433-1454: 4-directional line scan ≤60 tiles, breaks on solid non-trap, TRAP tile → trapCooldown Map<string,number> ('x,y' key, 40 tick cooldown) → spawn Dart via entities.add(dart,'projectiles'), sfx tink. Note bug: `return` inside the per-direction trap found (line 1445/1450 returns from whole function) — with new wiring this would be replaced.
- checkPressurePlates 1457-1468: player feet tile === v_135_pressure_plates && !plateLatch → fireTrapsFrom; plateLatch is Set<string> of 'x,y'.
- trapCooldown/plateLatch fields: Game.ts lines 184-185.

**Game loop**
- frame 332-345: accumulator, max 5 steps, render().
- fixedUpdate 349-663 order: tickCount++, hitTiles.update every 2 ticks (353), clock tick (355), day/night toast (357-364), input handling/minimap/teleport/annotate (368-451), player movement input (452-455), wheel zoom (458-468), player.fixedUpdate (470), death/respawn (471-482), updateUse (485), entities.update (488), liquid every 2 ticks (491-495), spawnTimer/water candle/campfire + trySpawnEnemy (498-543), checkPressurePlates (546), boss logic (549-561), saplings every 300 (564), fog every 15 (567-569), buffs refresh (572), camera/chunks.flushDirty/lighting.ensureRegion/compute (575-592), inv notify (595), critters (597+), particles/dmg numbers (627-657), inp.endFrame (659), postUpdate (662).
- Wiring.update placement suggestion: after checkPressurePlates (546) or replacing it, before entities/boss — e.g., right after liquid step or after entity update; and with tickCount % 2 throttle possible.
- Sfx: SfxName list line 4-6, includes 'tink' (yes) — WAV_MAP tink: ['Tink_0','Tink_1'] line 19. No dedicated switch/lever sound; tink used for lever (Game 1427).
- Projectiles: Dart class entities/Dart.ts (w 8 h 4, vx/vy, damage, life 600, dead flag; fixedUpdate uses game.world.store.isSolid; draw uses r.canvas + cam). Spawn pattern Game 1447-1448: new Dart(x,y,vx,vy,dmg); this.entities.add(dart,'projectiles').
- GameHooks interface entities/types.ts 4-32 — for a Wiring system interacting with doors/sfx etc.

**Rendering**
- ChunkCache: CHUNK=16 from constants (constants.ts:16). ChunkPair {wall, tile} (20-23). renderChunk 117-296: pass 1 walls w/ EXT=1 (128-155), pass 2 tiles (157-243), pass 3 half-brick clearRect (244-253), pass 4 tree crowns EXT=6 (255-293). Water is NOT in chunk canvases; rendered by Renderer between wall and tile passes (see below). markDirty/flushDirty budget 4/frame (78-87), get() lazy (90-97), markDirtyAround (67-75).
- Wire overlay options: (a) third canvas in ChunkPair (wire) drawn as its own pass — but wire is usually drawn semi-transparent overlay ABOVE tiles in vanilla; would be a separate pass in Renderer after 2c; or (b) dynamic per-frame draw in Renderer (like drawLiquids/drawWaterfalls) gated by toggle, avoiding chunk rebuilds — better since wire bits change rarely but overlay is toggled.
- Renderer.render 192-362: order: sky (216), world transform (218-224), background liquids (237), wall chunks (240-245), tile chunks (248-253), waterfalls (256), entities (259-267), player (268), foreground liquids (272), particles (275-280), cursor (283-294), restore (296), compositeLight (299), dmg numbers (302-325), minimap (329), fullmap (331-334), annotateMarks overlay (338-354), debug overlay (355), boss bar (358), HP (361).
  - A wire overlay pass could go right after tile chunks 2c (before waterfalls/entities) or after entities but before/after compositeLight. Vanilla draws wires over tiles with transparency; best insertion: after 2c tile layer (so wires visible over blocks but under entities) or as screen-space pass after compositeLight so it's visible in darkness (mechanical lens style). Pattern to copy: drawWaterfalls (379-389) which scans tx0..tx1/ty0..ty1.
- Toggles: Renderer.debugMode (line 99, F3), Renderer.annotateMarks (100-101), Renderer.fullbright (939, F9). Keyboard registration in main.ts 50-126 (switch on e.code; F3 89, F4 94, F5 100, F6 104, F8 108, F9 113). Game-side keydown handlers via input.keydownHandlers (Input.ts:9, Game.ts:209-217 for hotbar digits/zoom). Game.annotateMode (Game.ts:179) with _annoLatch (191) for click latching — pattern for a wire-tool mode.

**Related systems**
- Door.ts: openDoor(st,x,y,direction): boolean (47-73), closeDoor(st,x,y,rng,blocked): boolean (78-116), clearDoorAt 29-43, placeDoorClosed 20-25, doorClosedFrame 10-12, doorStyleOf 15-17. Game.toggleDoor 1502-1513 wraps them with sfx door_open/door_close and overlapsEntity as blocked callback — door wiring should call toggleDoor or directly openDoor/closeDoor + sfx.
- LiquidSim: constructor subscribes onTileChanged (50-54) and onLiquidChanged (56-61); addWater 97-116 (public); step() called every 2 ticks from Game (491-493); setLiquid public on store 121-129. Pump integration: pump would compute transfers and call st.setLiquid(x,y,amount,type) which wakes the sim via liquidListeners.
- Enemy spawn: Game.spawnEnemy (1978-1983) — public, returns Enemy, sets boss if boss; Enemy.fromVanilla(id,x,y) used at 1665 and 2189 for vanilla ids (statue spawns: 446 skeleton statue, 452 hornet statue, etc. in WldImport ITEM_MAP — item ids exist; tile v_105_statue exists at tiles.ts:234 with 2x3 frame style; statue style determined by frameX/frameY).
- Teleport: Game.teleportNear(tx,ty) private (2230-2284) — used by full-map click-to-teleport (two-click confirm, 396-433), sets player.x/y and camera; renderer.tpMark for marker. v_235_teleporter tile exists (tiles.ts:340, 3x1 solid). No /tp command. spawnX/spawnY set by bed (interactAt 1356-1361); respawnPlayer 2301-2310.

Also worth mentioning:
- LightingEngine is in Game (this.lighting) with fields r/g/b/rx/ry/rw/rh, liquidDirty, heldLight, dirty, ensureRegion, compute (used at Game 574-592, render 2324). Wiring could add light sources but not required.
- Minimap subscribes onTileChanged (Renderer.ts 35-37); wire changes through setTile would mark minimap dirty — but if we add wire via separate setter not notifying listeners, no chunk/minimap rebuild happens (good for overlay-only).
- Note flags bit1 reserved comment (TileStore.ts:8) — could be reused, but a dedicated wire Uint8Array is cleaner.
- Check SaveFile version field: `version: 2` at line 114; SaveData.version line 47. Migration pattern at 176-179.

One thing to verify: does tryPlace handle `heldDef.wall`? Let me grep quickly for '.wall' in Game.ts to be accurate.
````

</details>


---

## 🤖 Assistant · 2026-08-09T10:50:16.137Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\\.wall\\b\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head; echo ----; grep -rn \"heldDef.wall\\|itemDef.wall\\|def.wall\" ~/Project/GLM/SandboxWorld/game/src | head",
 "description": "Check whether wall placement items are handled anywhere"
}
```


---

## 👤 User(sidechain) · 2026-08-09T10:50:16.162Z

**📎 ToolResult**

```
921:      const wall = this.world.store.get(tx, ty) === 0 ? this.world.store.wall[this.world.store.idx(tx, ty)] : 0;
1328:      if (st.isActive(x + dx, y + h) || st.isSolid(x + dx, y + h) || st.wall[st.idx(x + dx, y + h)] !== 0) return true;
1624:    const isUnderground = st.wall[st.idx(tx, ty)] !== 0 || ty > w.rockLevel;
1829:        if (dy >= -2 && dy <= 2 && st.wall[st.idx(x, y)] !== 0) walls++;
----

```


---

## 🤖 Assistant · 2026-08-09T10:50:18.808Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: `ItemDef.wall` is declared but never used — no wall placement flow exists in Game. Good to note as a hook precedent.

Now write the structured report. Since plan mode is active, I should present this as a report (read-only exploration was requested). The instructions say I may create a plan file, but this is a search/report task — I'll just output the report as my final message. The parent agent reads my text output.
```

</details>


---

## 🤖 Assistant · 2026-08-09T10:51:31.417Z · glm-x-preview-260804

```
# Wiring/Circuit System — Integration Point Map

All paths absolute. Line numbers from current working tree.

---

## 1. TileStore — `~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts` (130 lines)

Structure-of-arrays, column/row indexing, all hot code touches TypedArrays directly.

**Fields (exact names, lines 5–15):**
| Field | Type | Notes |
|---|---|---|
| `w`, `h` | `readonly number` | dimensions in tiles |
| `type` | `Uint16Array` | tile id (index into `TILE_DEFS`) |
| `flags` | `Uint8Array` | line 8: `bit0 active, bit1 framedDecor占位(预留)` — **bit1 is explicitly documented as reserved/spare** |
| `frameX`, `frameY` | `Uint16Array` | 18px pixel offsets for vanilla framed objects |
| `wall` | `Uint16Array` | vanilla wld wall id 0–366 |
| `liquid` | `Uint8Array` | 0–255 amount |
| `liquidType` | `Uint8Array` | 0 none / 1 water / 2 lava / 3 honey |
| `half` | `Uint8Array` | half-brick bit, **full byte per tile** (not packed into flags) |
| `slope` | `Uint8Array` | slope 0–4, **full byte per tile** |

Allocation: constructor lines 20–32, `const n = w * h`, each `new UintNArray(n)`.

**Addressing:** `idx(x, y) { return y * this.w + x; }` — line 34. `inBounds` 36–38.

**Readers:** `get` 40, `isActive` 42, `isSolid` 46, `isPlatform` 52 (all bounds-checked, out-of-bounds = empty).

**Listeners:** two independent channels —
- `private listeners: Array<(x,y)=>void>` line 18; `onTileChanged(fn)` 58–60. Subscribed by `ChunkCache` (ChunkCache.ts:43), `Minimap` (Renderer.ts:35–37), `LiquidSim` (LiquidSim.ts:50–54).
- `private liquidListeners` line 64; `onLiquidChanged(fn)` 65–67. Comment: liquid changes deliberately bypass chunk rebuilds; only lighting subscribes.

**Writers:**
- `setTile(x,y,type,frameX=0,frameY=0)` 70–79 — sets `flags[i] = type!==0 ? 1 : 0`, clears `half`/`slope` when type 0 (line 77), fires `listeners`.
- `setHalfBrick(x,y,v)` 82–87, `setSlope(x,y,s)` 89–95 (`setSlope` force-clears `half`) — both fire `listeners` (this is the model for a `setWire()` mutator).
- `setTileSilent` 97–105 — no listener fan-out (gen/import path).
- `setWall` 107–114 (fires listeners only on change), `setWallSilent` 116–119.
- `setLiquid(x,y,amount,type)` 121–129 — fires `liquidListeners` **only**.

**Integration guidance for wire bits:**
- Add `readonly wire: Uint8Array` (+ optionally `actuator: Uint8Array`) allocated in the constructor, one byte per tile (bit0 red / bit1 blue / bit2 green / bit3 yellow / bit4 actuator — mirrors vanilla `bTileHeader`). Follow the `half`/`slope` precedent: separate byte array, not packed into `flags`.
- Add `setWire(x, y, bits)` mirroring `setHalfBrick` (82–87). **Do not** fire `this.listeners` — chunk canvases don't contain wires, and firing would cause pointless chunk + minimap rebuilds (see §6). If wires are baked into chunks, then do fire.
- `setTile`/`setTileSilent` with `type===0` currently clear `half`/`slope` (77, 104) but **do not** need to clear wire (vanilla keeps wires on mined tiles — worth deciding explicitly; vanilla keeps them).
- `flags` bit1 is free if packing is preferred.

---

## 2. Save format

### `SaveFile.ts` — `~/Project/GLM/SandboxWorld/game/src/save/SaveFile.ts` (212 lines)

JSON shell + base64 RLE binary sections.

**`SaveData` interface 45–69:** `format: 'sandboxworld.save'`, **`version: number`** (line 47; written as `version: 2` at line 114), `header {name, seed, width, height, spawn, groundLevel, rockLevel, crimson?, dungeonX?, jungleX?, treeX?, treeStyle?, treeTops?, created, playTimeMs, wldVersion?}`, `clock`, **`tiles`/`walls`/`liquid`/`liquidType` as base64 RLE strings** (57–60), `chests`, `player`, `npcs`, `flags`.

**RLE encoding:** `rlePairs(values)` 71–84 → `varint(run-1) varint(value)`. `rleTiles(st)` 86–103 → per run `varint(run-1) varint(type) [varint(fx) varint(fy) if type!=0]`.

**`saveGame(world, player, playTimeMs)` 105–136:** ghost-purge loop at 109–111 zeroes non-active `type` residue before serializing (format doesn't carry the active bit; reload re-derives `flags` from type≠0). Sections assembled at 123–126.

**`loadSave(json)` 138–212:** tiles decoded 158–175 (rebuilds `flags[i] = t!==0?1:0`), walls 176–188 **with a version-gated legacy migration** (`const legacy = (data.version ?? 1) < 2` line 178 — the exact pattern to copy for a wire section), `liquidType` 189–199 (**tolerates missing field**: `b64ToBytes(data.liquidType ?? '')` — copy this for wire), liquid 200–210.

**No checksums anywhere.** Versioning is the single `version` integer + field-optional-with-fallback reads.

**Where a wire byte array slots in:**
1. Add `wire: string` to `SaveData` next to `liquidType` (line 60).
2. `saveGame`: `wire: bytesToB64(rlePairs(st.wire))` after line 126.
3. `loadSave`: add a decode block mirroring the `liquidType` block 189–199 with `data.wire ?? ''`; bump `version` to 3 only if you need migration semantics (missing field already works).
4. Same change in **`WldImport.parseWldToSave`** (`WldImport.ts:796–830`) which builds a `SaveData` directly and hard-codes `version: 2` (line 798) with a comment that it must not drop below 2.

### `KvStore.ts` — `~/Project/GLM/SandboxWorld/game/src/save/KvStore.ts` (86 lines)
String-only key-value layer. IndexedDB (`sandboxworld`/`kv`, DB version 1) primary, localStorage fallback. API: `kvHas` 21–34, `kvGet` 38–50, `kvSet` 53–72 (**≤2MB strings → localStorage, else IDB only**), `kvDelete` 75–86. No schema involvement — no changes needed for wiring.

### `World.ts` — `~/Project/GLM/SandboxWorld/game/src/world/World.ts` (104 lines)
Fields (28–52): `store`, `name`, `seed`, `spawnX/spawnY`, `groundLevel/rockLevel`, `clock` (Clock class 7–26: `timeOfDay`, `dayCount`, `isDay`, `dayFactor`), `chests: ChestData[]`, `flags: Record<string,boolean>` (37), `trees: Array<{x,y,h}>` (39), `explored: Uint8Array` (41) + `exploredVersion` (52), `treeX/treeStyle/treeTops`, `crimson/dungeonX/jungleX`.
There is **no versioning field on `World` itself** — `wldVersion` lives only in `SaveData.header` (SaveFile.ts:54) and is never read back. Convenient spot for a `wiring` subsystem field (`world.wiring = new Wiring(world.store)`), constructed in `World`'s constructor (67–74) or in `Game.afterWorldLoad`.

---

## 3. WldParser — `~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts` (349 lines)

**`WldTileData` 7–15:** `active`, `type`, `frameX`, `frameY`, `wall`, `liquid`, `liquidType` (all per-tile arrays). **No wire arrays — wire bits are read as headers but discarded.**

**`decodeTiles(r, w, h, version, frameImportant)` 274–349**, column-major (`for x … for y`), RLE fills downward. Per-tile bit layout as parsed here:

| Read | Line | Mask | Meaning |
|---|---|---|---|
| `header1 = r.u8()` | 290 | — | flags1 |
| `header2 = r.u8()` | 292 | `header1 & 0x01` | flags2 present |
| `header3 = r.u8()` | 293 | `header2 & 0x01` | flags3 present |
| `header4 = r.u8()` | 294 | `version >= 269 && header3 & 0x01` | flags4 — read then **`void header4`** (295) |
| active | 299 | `header1 & 0x02` | tile present |
| type u16 vs u8 | 301–305 | `header1 & 0x20` | extended id |
| frameX/frameY u16 | 306–310 | `frameImportant[tileType]` | framed object |
| tile color | 311 | `header3 & 0x08` | skipped byte |
| wall u8 | 314–315 | `header1 & 0x04` | |
| wall color | 316 | `header3 & 0x10` | skipped |
| wall high byte | 317–319 | `version >= 222 && header3 & 0x40` | `wl |= u8 << 8` |
| liquid type | 321 | `(header1 & 0x18) >> 3` | |
| liquid amount u8 | 322–326 | `lqType !== 0`; `header3 & 0x80` (v269+) → honey/shimmer kind 1 |
| RLE count | 328–331 | `(header1 & 0xC0) >> 6` (1→u8, 2+→u16) | |

**Wire bits are NOT parsed.** In vanilla's flags layout, the wire/actuator bits are in `header2` (bit `0x01` is the only one consumed here, at line 293):

- `header2 & 0x02` — red wire
- `header2 & 0x04` — blue wire
- `header2 & 0x08` — green wire
- `header2 & 0x10` — yellow wire
- `header2 & 0x20` — actuator
- `header2 & 0x40` — actuator's inactive/active state (inactive stone)

`header3 & 0x02 / 0x04` (slope bits) are likewise ignored — `TileStore.half/slope` are never populated by wld import.

**Where to extract:** in `decodeTiles`, right after lines 290–295, accumulate `wireBits = (header2 & 0x3E) >> 1` (red|blue|green|yellow|actuator) into new `WldTileData` arrays (`wire: Uint8Array`, optionally `actuator: Uint8Array` + actuator-active). Then write them in the RLE fill loop at 334–343 (`for k = 0; k <= rle …` — the loop that writes `active/type/frameX/frameY/wall/liquid/liquidType`), and return them at line 348.

**Downstream:** `WldImport.parseWldToSave` (`WldImport.ts:730–758`) iterates `wld.tiles.*` per tile and copies to fresh arrays — add wire there (e.g. `wireArr[i] = wld.tiles.wire[i]`), then emit `wire: bytesToB64(rlePairs(wireArr))` into the `SaveData` literal at 816–819.

---

## 4. Items & placement

### `items.ts` — `~/Project/GLM/SandboxWorld/game/src/data/items.ts` (724 lines)

**`ItemDef` interface 8–47:** `key`, `name`, `maxStack` (default 999 via `item()` at 53–56 which also fills `byKey`), **`tile?: string`** (12), **`placeStyle?: number`** (13, → frameX offset `style * fw * 18`), `magic?`, `ranged?`, **`wall?: string`** (28 — declared but **never used** anywhere; there is no wall-placement flow in Game), `tool? {type: 'pick'|'axe'|'sword'|'hammer', power?, damage?, speed?, knockback?, reach?}` (29–36), `heal?`, `potion?`, `accessory?`, `armor?`, `value?`, `desc?`.
`ToolType` at line 2 — extend this union for a wrench (e.g. `'wrench'`) or add a new `wireTool?` field.

**Placement items already exist for every wiring tile.** Auto-registration block 641–655: for every `v_*` tile a `place_v_<key>` item is registered with `tile: td.key, maxStack: 999`. So `place_v_132_lever`, `place_v_136_switch`, `place_v_137_traps`, `place_v_135_pressure_plates`, `place_v_235_teleporter`, `place_v_144_timers`, `place_v_105_statue`, `place_v_130_active_stone_block`, `place_v_443_geyser` are all live. `vi_509_red_wrench` exists as an inert vanilla item (registered from `vanilla.json`, lines 669–675).

### `Game.ts` flow — `~/Project/GLM/SandboxWorld/game/src/core/Game.ts` (2339 lines)

**`updateUse(dt)` 667–893** — dispatch order:
1. minecart override 670–690; uiBlocking/dead/fullMap guard 692–695.
2. held item + hover tile 696–699.
3. **Right-click dispatch 718–737:** minecart-on-track (704–717) → nearby chest (719) → NPC talk (723) → suspicious eye (725) → **`interactAt(tx, ty)` (735)**.
4. Sword 745–754; pick/axe/hammer mining 757–778.
5. **Placement: `if (heldDef?.tile && !inp.rightDown) { this.tryPlace(tx, ty, heldDef); return; }` — 781–784.**
6. Generic use / potions / bows / magic / buckets 787–891.

**`tryPlace(tx, ty, itemDef)` 1220–1313:**
- range gate 5.5 tiles (1224–1226), `TILE_BY_KEY[itemDef.tile!]` lookup 1227.
- special-cases inline: acorn 1230–1233, **rope 1236–1251 (the pattern to copy for a wrench)** — vertical multi-place, `player.inv.removeAt(selected, 1)`, `useTime = 14`, `sfx.play('place')`, `cb.onInventoryChanged()`.
- space check loop 1253–1261 (`isActive` rejection; `def.solid && overlapsEntity` rejection).
- support check 1263–1264 via `hasSupport` 1324–1339.
- `useTime` gate 1265.
- placement loop 1269–1305 — vanilla style frames: `frameX = (itemDef.placeStyle ?? 0) * strideX + dx*18`, `frameY = dy*18` (1275–1279), non-vanilla `setTile(px, py, tileId, dx2, dy2)` (1280). Liquid displacement logic 1282–1303.
- chest registration 1306–1308; **consume + cooldown: `inv.removeAt(selected,1)`, `useTime = 14`, `sfx.play('place')` — 1309–1312.**

**Wrench hook point:** a branch in `updateUse` immediately before line 781, e.g. `if (heldDef?.wireTool && inp.mouseDown && !inp.rightDown) { this.tryPlaceWire(tx, ty, heldDef); return; }`. Key differences vs `tryPlace`: **must allow the target tile to be occupied** (skip the `isActive` rejection), writes `st.setWire` bits instead of a tile, and consumes item + sets `useTime`/sfx exactly like the rope branch. A cutter/remover variant ORs the bits out.

**`overlapsEntity(px, py)` 1315–1322** — AABB vs player + all enemies.

**Mining → break:** `tryMine` 903–999 (HitTile damage accumulation, threshold 100 at 990 → `breakTile(tx,ty)` 992). `breakTile` 1022–1099: tree felling 1029–1031, orb 1034–1037, imported trees 1038–1041, **door `clearDoorAt` 1043–1048**, multi-tile object anchor walk (frame/18 normalization) 1050–1067, chest dump 1065, generic `setTile(x,y,0)` 1092 + drops/particles. **Note:** `setTile(x,y,0)` clears `half`/`slope` (TileStore 77) but nothing else — decide whether wire survives mining (vanilla: it does).

**`interactAt(tx, ty)` 1341–1376:** closed/open door (1344–1347), chest (1348), crystal heart (1352), bed → `world.spawnX/spawnY` (1356–1361), **lever `v_132_lever` / switch `v_136_switch` → `toggleSwitch(tx,ty,type)` (1362–1364)**, herb harvest (1365).

---

## 5. Game loop

**`frame(now)` 332–345:** fixed-step accumulator, `FIXED_DT = 1/60` (line 51), max 5 catch-up steps, `render()` every rAF.

**`fixedUpdate(dt)` 349–663** — tick order:
| Step | Lines |
|---|---|
| `tickCount++`, HitTile decay every 2 ticks | 350–353 |
| `clock.tick`, day/night toast | 355–364 |
| input: minimap click, full-map teleport (2-click), annotate mode | 368–451 |
| movement keys, wheel zoom | 452–468 |
| `player.fixedUpdate`, death/respawn | 470–482 |
| **`updateUse(dt)`** | 485 |
| `entities.update(dt, this)` | 488 |
| liquid sim every 2 ticks + `lighting.liquidDirty` | 491–495 |
| enemy spawn timer / water candle / campfire / `trySpawnEnemy` | 498–543 |
| **`checkPressurePlates()`** | 546 |
| boss logic | 549–561 |
| sapling growth (every 300) | 564 |
| fog of war (every 15) | 567–569 |
| buff refresh (every 60) | 572 |
| camera follow/clamp, `chunks.flushDirty()`, lighting ensure/compute | 575–592 |
| critter spawn/crushing, ambient sfx, torch sparks, particles, dmg numbers | 595–657 |
| `inp.endFrame()`, `postUpdate()` (swing hits) | 659–662 |

**Wiring.update placement:** directly alongside/after `checkPressurePlates()` at line 546 (replace or feed it), after `updateUse`/entities so player-triggered sources are seen same tick. Throttle pattern available: `this.tickCount % 2 === 0` (cf. 491) for vanilla's every-2-ticks signal cadence. Timers (`v_144_timers`) need per-tick scheduling — a `Map<string, number>` cooldown keyed `'x,y'` already exists as precedent.

**Existing mechanism bits (all in Game.ts):**
- `trapCooldown = new Map<string, number>()` — line 184.
- `plateLatch = new Set<string>()` — line 185.
- `toggleSwitch(x, y, type)` 1422–1430: `on = st.frameX[i] >= 18`; `st.setTile(x, y, type, on ? 0 : 18, st.frameY[i])`; `sfx.play('tink')`; `fireTrapsFrom(x, y, !on)`; `input.rightDown = false`.
- `fireTrapsFrom(px, py, powerOn)` 1433–1454: 4-directional line scan ≤60 tiles, breaks on solid non-trap, on `v_137_traps` applies 40-tick `trapCooldown` then `new Dart(x*16+8+dx*10, y*16+8+dy*10, dx*9, dy*9, 20)` + `entities.add(dart, 'projectiles')` + tink. **Note the `return` at 1445/1450 exits the whole method (fires only one trap)** — a real BFS signal propagation replaces this.
- `checkPressurePlates()` 1457–1468: player feet tile (`floor(p.cx/16), floor((p.y+p.h)/16)`) === `v_135_pressure_plates` and not latched → `fireTrapsFrom(tx, ty, true)`; unlatches when tile changes.

**Sfx — `~/Project/GLM/SandboxWorld/game/src/core/Sfx.ts`:** `SfxName` union 4–6: `hit | hurt | pickup | dig | place | drink | chop | splash | killed | pkilled | zombie | roar | coin | door_open | door_close | tink | shatter | drown`. **Yes, `'tink'` exists** (`WAV_MAP` 19: `tink: ['Tink_0','Tink_1']`; synth fallback 136) — it's the existing lever/switch sound (Game.ts:1427). No dedicated vanilla lever sound is wired up. Public API: `play(name, vol)` 108, `playWav(name, vol)` 80, `playFiles(files, vol)` 87, `playWavFile` 93, `addFiles(files)` 38 (to register extra wavs from `public/sounds/`).

**Projectile spawn pattern — `~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts`:** `class Dart extends Entity { w=8; h=4; vx; vy; damage; life=600; dead=false }`, constructor 17–22, `draw(r, cam)` 24–31 (screen projection via `r.canvas` + `cam`), `fixedUpdate(dt, game: GameHooks)` 33–49 (`game.world.store.isSolid`, player AABB via `game.player`). Spawn: Game.ts:1447–1448. `EntityManager` (`~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts`): buckets 29–34 (`enemies/drops/npcs/projectiles/props/critters`), `add(e, bucket)` 36–39 assigns `nextId++`, `update` 41–51 filters `dead`. `GameHooks` interface (`entities/types.ts` 4–32) exposes `world`, `player`, `spawnEnemy`, `spawnDrop`, `spawnParticles`, `playSfx`, `addDamageNumber` — the natural contract for a Wiring system.

---

## 6. Rendering

### `ChunkCache.ts` — `~/Project/GLM/SandboxWorld/game/src/render/ChunkCache.ts` (297 lines)

- `CHUNK = 16` from `~/Project/GLM/SandboxWorld/game/src/core/constants.ts:16` (also `TILE = 16` line 2).
- `interface ChunkPair { wall: HTMLCanvasElement; tile: HTMLCanvasElement }` — lines 20–23, comment: wall layer has water painted above it, tile layer above water.
- `chunks = Map<number, ChunkPair>` keyed `(cx & 0xffff) | ((cy & 0xffff) << 16)` (`static key` 46–48).
- `get(cx,cy)` 90–97 lazy build; `markDirty` 50–55; `markDirtyArea` 58–65; `markDirtyAround` 67–75 (edge-chunk neighbors); `flushDirty(maxN = 4)` 78–87, called once per tick from Game.ts:578.
- `renderChunk(cx, cy)` 117–296 passes: **(1) walls** 128–155 with `EXT = 1` overshoot; **(2) foreground tiles/objects** 157–243 (skips `type === 0 || !st.flags[i]`, vanilla framing via `drawVanillaCell`, autotile rules, blend sheets); **(3) half-brick post-pass** 244–253 (`clearRect` top 8px when `st.half[i]`); **(4) tree crowns** 255–293 with `EXT = 6`.
- **Water is NOT baked into chunk canvases** — drawn live by Renderer between the wall and tile passes.

**Wire overlay options:**
- *Dynamic pass (recommended):* a `drawWires(world, cam, viewW, viewH, z)` method in `Renderer` scanning the visible tile window, exactly like `drawWaterfalls` (Renderer.ts:379–389) / `drawLiquids` (364–376). Advantages: toggleable without chunk rebuilds, no `TileStore` listener load, can pulse/animate. Insertion point: after step 2c (tile chunks, Renderer.ts:248–253) and before 2d waterfalls — wires over tiles, under entities.
- *Baked third canvas:* extend `ChunkPair` with `wire: HTMLCanvasElement`, render it in `renderChunk` as a pass after the half-brick pass (244–253), and fire `this.listeners` from a `setWire` mutator so `markDirtyAround` picks it up. Higher quality per-chunk batching but pays a rebuild per wire edit.

### `Renderer.ts` — `~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts` (1426 lines)

**`render(...)` composite 192–362**, exact order:
1. sky 216; world transform 218–224 (nearest-neighbor, `translate/scale/translate`);
2. background liquid pass 237 (`drawLiquids(..., true)`);
3. **wall chunks 240–245** (`ctx.drawImage(chunks.get(cx,cy).wall, …)`);
4. **tile chunks 248–253** (`.tile`);
5. waterfalls 256;
6. entities y-sorted 259–267, player 268;
7. foreground liquid pass 272 (alpha 0.6 over entities);
8. particles 275–280; mining cursor 283–294;
9. `ctx.restore()` 296; **light composite `compositeLight` 299** (def 941–1000+, `fullbright` skip at 946);
10. dmg numbers 302–325; minimap 329; full map 331–334; **annotate overlay 338–354**; **`if (this.debugMode) this.drawDebugOverlay(...)` 355**; boss bar 358; HP 361.

`drawDebugOverlay` def 1259+ — screen-space drawing pattern (`cam.worldToScreen`, dashed strokes) to copy for a wire overlay that must remain visible in darkness (draw *after* `compositeLight`, like the annotate/debug overlays, for a "mechanical lens" style; draw *before* it for in-world wires).

**Existing overlay toggles (pattern to copy):** `Renderer.debugMode` line 99 (F3), `Renderer.annotateMarks` 100–101 (fed from `Game.annotateMode` at Game.ts:2317), `Renderer.fullbright` line 939 (F9), `Renderer.tpMark` (set at Game.ts:419/425).

**Keyboard/UI toggle registration:** all F-keys live in `~/Project/GLM/SandboxWorld/game/src/main.ts` 50–126 — a `switch (e.code)` on `window` keydown: F3 debug 89, F4 reveal fog 94, **F5 annotate mode 100** (`toggleAnnotate()` 138+ flips `game.annotateMode`, opens a panel, toasts), F6 save 104, **F8 enemy spawn toggle 108** (`game.enemySpawnEnabled = !…` + `ui.toast`), F9 fullbright 113. A second hook mechanism exists inside Game: `this.input.keydownHandlers.push((code) => …)` (Game.ts:209–217, used for hotbar digits and zoom). Click-latch pattern for mode-based placement: `Game.annotateMode` + `_annoLatch` (Game.ts:179, 191, 435–451) — reusable verbatim for "hold wrench, click tiles".

---

## 7. Existing related systems

### Doors — `~/Project/GLM/SandboxWorld/game/src/world/Door.ts` (117 lines)
- `doorClosedFrame(style, variant): [number, number]` 10–12; `doorStyleOf(fx, fy)` 15–17.
- `placeDoorClosed(st, x, y, style, variant)` 20–25 (silent 1×3 placement).
- `clearDoorAt(st, x, y): [number, number] | null` 29–43.
- **`openDoor(st: TileStore, x, y, direction: number): boolean`** 47–73 — returns false if blocked; caller retries `-direction`.
- **`closeDoor(st, x, y, rng = Math.random, blocked?: (x,y)=>boolean): boolean`** 78–116.
- Game wrapper `toggleDoor(x, y, open)` — Game.ts:1502–1513: picks direction from `player.facing`, passes `overlapsEntity` as the `blocked` callback, plays `door_open`/`door_close`. **Door wiring should call this wrapper** (or `openDoor`/`closeDoor` + sfx directly when no player-facing context exists).

### LiquidSim — `~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts`
- Subscribes `onTileChanged` (3×3 wake, 50–54) and `onLiquidChanged` (plus-neighbors, 56–61); `dispose()` 65–69.
- `addWater(x, y)` public 97–116; `step()` invoked every 2 ticks from Game.ts:491–493; `numLiquid` public.
- **Pump integration:** a pump has no direct API — move liquid by calling `world.store.setLiquid(x, y, amount, type)` (TileStore.ts:121–129), which wakes the sim via `liquidListeners`. `setTile`-based activation (e.g. toggling `v_130_active_stone_block` solid state) will also wake the sim through `onTileChanged`. Note `blocksLiquid` 74–81 / `solidTileFull` 85–93 consult `TILE_DEFS[t].solid` and `st.half`/`st.slope` — an actuator-driven inactive-block implementation that flips solidity must keep these consistent.

### Enemy/statue spawn API
- `Game.spawnEnemy(key, x, y)` — Game.ts:1978–1983 (public, `entities.add(e,'enemies')`, sets `this.boss` if `def.boss`).
- Vanilla-data path: `Enemy.fromVanilla(vanillaId, x, y)` — used at Game.ts:1665 (ambient spawn) and 2189 (`summonBoss` 2178–2206); worm chains via `Enemy.spawnWormChain`.
- Statue tile `v_105_statue` exists — `~/Project/GLM/SandboxWorld/game/src/data/tiles.ts:234` (2×3, `frame: 'style'`, so the statue *style* is encoded in `frameX`/`frameY`; style→NPC mapping would be a lookup table keyed off `floor(frameX/18)`/`floor(frameY/18)`). Statue items are already mapped in `WldImport.ts` ITEM_MAP (442–443: hornet/bomb statue, 438 star statue, 446 skeleton, etc.).

### Teleport
- `Game.teleportNear(tx, ty): boolean` — Game.ts:2230–2284 (private; fits check 2-tile clearance + solid ground, spiral out to 24, air fallback; sets `p.x/p.y`, zeroes velocity, snaps camera).
- Full-map click-to-teleport with two-click confirm at Game.ts:396–433 (uses `renderer.tpMark`), `_tpTarget` field at 177.
- Teleporter tile `v_235_teleporter` exists — tiles.ts:340 (3×1, `solid: true`), plus placement item `place_v_235_teleporter` (auto-registered, items.ts:641–655). No `/tp` command; `spawnX/spawnY` set by bed at Game.ts:1356–1361, used by `respawnPlayer` 2301–2310.

---

## Quick checklist of every file a wiring system must touch

1. `src/world/TileStore.ts` — `wire` (± `actuator`) `Uint8Array` + `setWire`/silent variant.
2. `src/save/SaveFile.ts` — `SaveData.wire`, encode in `saveGame`, decode (missing-field-tolerant) in `loadSave`, bump/branch `version`.
3. `src/wld/WldParser.ts` — `WldTileData.wire`, extract `header2 & 0x3E` in `decodeTiles` (lines 290–295, 334–343, 348).
4. `src/wld/WldImport.ts` — copy wire in the per-tile loop (730–758) and into `SaveData` (796–830).
5. `src/world/World.ts` (or new `src/world/Wiring.ts`) — signal propagation, per-tick `update()`.
6. `src/data/items.ts` — wrench/cutter `ItemDef`s (`tool.type` extension or new `wireTool` field).
7. `src/core/Game.ts` — wrench branch before line 781 in `updateUse`; `Wiring.update` call at/near line 546 (replacing/generalizing `toggleSwitch`/`fireTrapsFrom`/`checkPressurePlates` 1422–1468); door/teleport/statue/pump effect dispatch.
8. `src/render/Renderer.ts` (+ optionally `src/render/ChunkCache.ts`) — wire overlay pass after tile chunks (248–253) or post-light like debug/annotate overlays (338–355).
9. `src/main.ts` — F-key toggle for the wire overlay following the F5/F8/F9 pattern (lines 100–117).
```
