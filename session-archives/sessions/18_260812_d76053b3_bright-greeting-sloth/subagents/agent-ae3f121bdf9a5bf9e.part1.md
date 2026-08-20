# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T03:09:32.684Z

```
你在 ~/Project/GLM/SandboxWorld 做泰拉瑞亚 1.4.5.6 复刻的 Boss AI 1:1 抽查审计。**严格只读:禁止编辑任何文件、禁止跑游戏/vite/测试。**

标杆(唯一权威):~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs(96369 行)
我方文件:
- ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts
- ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_deerclops.ts

背景:我方是手工移植;注释里 "cs:NNNNN"/"NPC.cs:NNNNN" 就是这份 NPC.cs 的行号。我方 ai0..ai3 = 原版 npc.ai[0..3],localAI ≈ localAI[i]。专家门:mainExpertMode() ≈ Main.expertMode。

你负责:
1. Golem(石巨人,aiStyle 45 → AI_045_Golem @19447-19760):蓄力跳/头部联动无敌门/血量阈值二段(头飞起)/激光与火焰弹节奏/专家分支
   - 挂载头 246(aiStyle 46 @31269-31500 前后):锚定本体、火焰弹+眼激光
   - 自由头 249(aiStyle 48 @31500-31742):弹射
   - 拳 247/248(aiStyle 47 → AI_047_GolemFist @19171-19446):肩锚冲拳/回收
   - 联动:本体死→部件死、头被击落后本体可受伤
2. Deerclops(鹿角怪 667,aiStyle 123 → AI_123_Deerclops @44338-45044 + 辅助函数 @44754-45141):九态状态机(待机/尖刺前刺/双侧刺/碎石上抛/影手/返回)、地面行走/AI_123_Deerclops_Movement、玩家死亡/走远回家语义、专家分支

审计维度(抓结构性偏差,不是数值噪音):阶段缺失/转换条件错/速度档错/专家分支漏/弹幕 id-计数-速度错/flee 语义无出处/部件联动错。

方法:先 Read 我方对应函数,再 sed -n '起,止p' 读原版对应段对照,不要泛读全文。注释声称的行号要抽验(注释可能撒谎/过时)。

输出格式(最终回复直接文本,不写文件):
逐 Boss 一节:"核了什么+发现什么"。每条 CONFIRMED 偏差给:我方文件:行号 / 原版 NPC.cs 行号 / 症状 / 最小修复建议 / 置信度(高/中/低)。没问题的 Boss 一句话带过。存疑单列。最多报 10 条,按严重度排序。禁止编造行号——每条 CONFIRMED 必须两边都真实读过。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T03:09:32.685Z

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

## 🤖 Assistant · 2026-08-19T03:09:37.696Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by reading our two files, then compare against the vanilla NPC.cs sections.

Plan:
1. Read game/src/entities/bossAI_golem.ts
2. Read game/src/entities/bossAI_deerclops.ts
3. Read NPC.cs sections:
   - AI_045_Golem @19447-19760
   - AI_047_GolemFist @19171-19446
   - aiStyle 46 (head attached) around 31269-31500
   - aiStyle 48 (free head) 31500-31742
   - AI_123_Deerclops @44338-45044 + helpers @44754-45141

Let me read our files first.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:38.027Z · glm-x-preview-260804

```
我先读我方两个文件，再对照原版 NPC.cs 对应段。
```


---

## 🤖 Assistant · 2026-08-19T03:09:38.258Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts"
}
```


---

## 🤖 Assistant · 2026-08-19T03:09:38.440Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_deerclops.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:38.450Z

**📎 ToolResult**

```
1	// 石巨人 Boss 族 AI 1:1 移植(Terarria1456,1.4.5.6):
2	//   本体 245  aiStyle 45  AI_045_Golem        NPC.cs:19447-19722(地面蓄力→跳跃循环/断臂尘/离场)
3	//   挂载头 246 aiStyle 46                       NPC.cs:31273-31499(锚本体;嘴部火焰弹/眼激光)
4	//   拳 247/248 aiStyle 47  AI_047_GolemFist    NPC.cs:19171-19446(肩锚归位→蓄力→直线冲拳→回位)
5	//   自由头 249 aiStyle 48  GolemHeadFree       NPC.cs:31500-31741(自主悬浮+火焰弹/眼激光)
6	//   SetDefaults:NPC.cs:12095-12149(245-249 属性)、17943-17960(245-249 scale *= 0.5)。
7	// 经典模式主链 1:1;getGoodWorld 分支已实装(balance +2/+3/蓄力 +100/本体+拳落体砸
8	// 火把/FTW 断臂尘由砸火把取代);expert 分支保留注释;netcode/纯视觉尘(Gore/netOffset)跳过。
9	//
10	// 死亡链(任务约定,原版 checkDead 语义的对齐版):
11	//   · 挂载头在场时本体无敌(NPC.cs:19513 dontTakeDamage = flag)——一阶段打头/拳;
12	//   · 本体血尽 → 死亡演出 60t 后真死(ai3=1 标记),挂载头转自由态续战(本体死透后头继续);
13	//   · 挂载头血尽 → 原地转自由态(原版 HitEffect :85842-85847 在原地 NewNPC 249;
14	//     此处头原体变身,满血+属性对齐 249 SetDefaults),本体解除无敌;
15	//   · 自由头血尽 → 全族自毁(战斗结束;原版由 245 死亡置 downedGolemBoss,:80146)。
16	//   以上转换全部在各自 AI 首行处理,不依赖外部钩子。
17	import type { Enemy } from './Enemy';
18	import type { GameHooks } from './types';
19	import type { Player } from './Player';
20	import { TILE } from '../core/constants';
21	import { TILE_DEFS } from '../data/tiles';
22	import { vanillaNpc } from '../data/vanillaNpcs';
23	import { spawnPart, shoot, accelTo, losClear } from './bossAI';
24	
25	/** 原版 NPC 通用重力/maxFall(NPC.UpdateNPC 非 noGravity 族:0.3/2t、maxFall 10) */
26	const GRAV = 0.3;
27	const MAX_FALL = 10;
28	/** SetDefaults 245-249 scale *= 0.5(NPC.cs:17943-17960)——族内所有像素偏移按此缩放 */
29	const SCALE = 0.5;
30	const clamp = (v: number, lo: number, hi: number) => (v < lo ? lo : v > hi ? hi : v);
31	
32	/** Boss 伤害/防御基值缓存(自由头切换 249 属性时从基值派生,防重复写膨胀) */
33	const baseStats = new WeakMap<Enemy, { dmg: number; def: number }>();
34	const baseOf = (e: Enemy) => {
35	  let b = baseStats.get(e);
36	  if (!b) { b = { dmg: e.def.damage, def: e.def.defense ?? 0 }; baseStats.set(e, b); }
37	  return b;
38	};
39	
40	/** 每实例附加槽位(原版 alpha/noTileCollide/localAI 等无对应 Enemy 字段) */
41	interface BodyX { alpha: number; noTC: boolean; dying: boolean; deadT: number }
42	interface HeadX { alpha: number; free: boolean; l0: number; l1: number }
43	interface FistX { alpha: number; noTC: boolean; state: number }
44	const bodyX = new WeakMap<Enemy, BodyX>();
45	const headX = new WeakMap<Enemy, HeadX>();
46	const fistX = new WeakMap<Enemy, FistX>();
47	const bodyXOf = (e: Enemy): BodyX => {
48	  let x = bodyX.get(e);
49	  if (!x) { x = { alpha: 255, noTC: false, dying: false, deadT: 0 }; bodyX.set(e, x); }
50	  return x;
51	};
52	const headXOf = (e: Enemy): HeadX => {
53	  let x = headX.get(e);
54	  if (!x) { x = { alpha: 255, free: false, l0: 0, l1: 0 }; headX.set(e, x); }
55	  return x;
56	};
57	const fistXOf = (e: Enemy): FistX => {
58	  let x = fistX.get(e);
59	  if (!x) { x = { alpha: 255, noTC: true, state: 0 }; fistX.set(e, x); }
60	  return x;
61	};
62	
63	// ---------------------------------------------------------------------------
64	// 族内查找(原版静态 golemBoss 索引的等价物:NPC.cs:6052 声明、:19449 每帧回填)
65	// ---------------------------------------------------------------------------
66	
67	const findBody = (game: GameHooks): Enemy | null =>
68	  (game.enemies() as Enemy[]).find((n) => !n.dead && n.vanillaId === 245) ?? null;
69	const findHead = (game: GameHooks): Enemy | null =>
70	  (game.enemies() as Enemy[]).find((n) => !n.dead && (n.vanillaId === 246 || n.vanillaId === 249)) ?? null;
71	
72	/** GetMyBalance + getGoodWorld/脱离神庙/丛林加成(NPC.cs:19450-19457 / :19173-19180 /
73	 *  :31274-31282 / :31506-31512):
74	 *  经典单人 = 1;getGoodWorld 本体 +2、拳/挂载头/自由头 +3(先加再乘);
75	 *  (!ZoneLihzhardTemple && !ZoneJungle) || 玩家 Center.Y < worldSurface*16 → ×2(expert 档略)。
76	 *  Zone 判定接 Game.scene(SceneMetrics):zoneTemple = 中心格墙 87(SceneMetrics.cs:688,
77	 *  神庙砖 226 不构成独立 Zone,只计入 JungleTileCount——SceneMetrics.cs:613,阈值 140)。 */
78	const balanceNum = (game: GameHooks, player: Player | null, ftwBonus = 0): number => {
79	  let num = 1;
80	  if (ftwBonus > 0 && game.world.seedFlags?.getGoodWorld) num += ftwBonus;
81	  const s = game.scene;
82	  const inTempleOrJungle = !!s?.zoneTemple || !!s?.zoneJungle;
83	  if (!inTempleOrJungle || (player != null && player.cy < game.world.groundLevel * TILE)) num *= 2;
84	  return num;
85	};
86	
87	/** getGoodWorld 落体砸火把(TileID.Sets.Torches = tile 4;NPC.cs:19510-19532 本体 /
88	 *  :19335-19366 拳冲拳段):像素带内激活的火把格直接置非激活(无掉落/无音效)。
89	 *  火把判定同 TorchGod:sheet===4(仓内 tile id 空间非原版号)。
90	 *  ★ 调用方照原版传带界——本体 Y 上界用 width(非 height)是原版笔误,1:1 保留 */
91	const smashTorches = (
92	  st: GameHooks['world']['store'],
93	  x0: number, x1: number, y0: number, y1: number,
94	): void => {
95	  for (let j = Math.floor(x0 / TILE); j < x1 / TILE; j++) {
96	    for (let k = Math.floor(y0 / TILE); k < y1 / TILE; k++) {
97	      if (!st.inBounds(j, k)) continue;
98	      const i = st.idx(j, k);
99	      if (st.flags[i] && TILE_DEFS[st.type[i]]?.vanilla?.sheet === 4) st.setTile(j, k, 0);
100	    }
101	  }
102	};
103	
104	/** 出生渐显(SetDefaults alpha=255;AI 内 alpha -= 10/2t,NPC.cs:19477-19485 / :31310-31317 / :19187-19194)。
105	 *  返回剩余 alpha;期间 ai[1] 由调用方冻结(本体/拳 0、挂载头 30)——蓄力计时不起跑 */
106	const fadeAlpha = (e: Enemy, x: { alpha: number }): number => {
107	  if (x.alpha <= 0) return 0;
108	  x.alpha = Math.max(0, x.alpha - 10);
109	  e.spawnAlpha = Math.min(254, x.alpha);
110	  return x.alpha;
111	};
112	
113	// ---------------------------------------------------------------------------
114	// 碰撞(本族私有拷贝:bossAI.collideGround 是 private;140px 宽本体需多列采样防半悬空)
115	// ---------------------------------------------------------------------------
116	
117	/** 落地/顶墙/侧墙判定(原版共享 Collision 的 AABB 近似:底/顶三列、侧墙三点) */
118	function collideGround(e: Enemy, game: GameHooks): void {
119	  const st = game.world.store;
120	  const cols = [e.x + 2, e.cx, e.x + e.w - 2];
121	  if (e.vy >= 0) {
122	    const ty = Math.floor((e.y + e.h) / TILE);
123	    let top = Infinity;
124	    for (const cx of cols) {
125	      const tx = Math.floor(cx / TILE);
126	      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) top = Math.min(top, ty * TILE);
127	    }
128	    if (top < Infinity) { e.y = top - e.h; e.vy = 0; e.onGround = true; }
129	    else e.onGround = false;
130	  } else {
131	    e.onGround = false;
132	    const ty = Math.floor(e.y / TILE);
133	    let bottom = -Infinity;
134	    for (const cx of cols) {
135	      const tx = Math.floor(cx / TILE);
136	      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) bottom = Math.max(bottom, (ty + 1) * TILE);
137	    }
138	    if (bottom > -Infinity) { e.y = bottom; e.vy = 0; }
139	  }
140	  const rows = [e.y + 2, e.cy, e.y + e.h - 2];
141	  if (e.vx > 0) {
142	    const tx = Math.floor((e.x + e.w) / TILE);
143	    for (const ry of rows) {
144	      const ty = Math.floor(ry / TILE);
145	      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { e.x = tx * TILE - e.w; e.vx = 0; break; }
146	    }
147	  } else if (e.vx < 0) {
148	    const tx = Math.floor(e.x / TILE);
149	    for (const ry of rows) {
150	      const ty = Math.floor(ry / TILE);
151	      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { e.x = (tx + 1) * TILE; e.vx = 0; break; }
152	    }
153	  }
154	}
155	
156	/** AABB 与实心块相交(原版 Collision.SolidTiles 近似):拳冲拳段关闭穿墙后的撞停判定 */
157	function hitSolid(game: GameHooks, e: Enemy): boolean {
158	  const st = game.world.store;
159	  const x0 = Math.floor(e.x / TILE), x1 = Math.floor((e.x + e.w - 0.01) / TILE);
160	  const y0 = Math.floor(e.y / TILE), y1 = Math.floor((e.y + e.h - 0.01) / TILE);
161	  for (let tx = x0; tx <= x1; tx++) {
162	    for (let ty = y0; ty <= y1; ty++) {
163	      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) return true;
164	    }
165	  }
166	  return false;
167	}
168	
169	// ---------------------------------------------------------------------------
170	// 弹幕(原版 NewProjectile 调用点:id 258 火焰弹 / 259 眼激光)
171	// ---------------------------------------------------------------------------
172	
173	/** 嘴部/额前火焰弹(:31329-31347 / :31430-31447 / :31596-31617):
174	 *  从 (e.center + (ox,oy)) 朝玩家中心 proj 258 */
175	function golemSpit(
176	  game: GameHooks, e: Enemy, player: Player, ox: number, oy: number,
177	  spd: number, dmg: number, projId: number,
178	): void {
179	  const sx = e.cx + ox, sy = e.cy + oy;
180	  const dx = player.cx - sx, dy = player.cy - sy;
181	  const d = Math.hypot(dx, dy) || 1;
182	  shoot(game, sx, sy, (dx / d) * spd, (dy / d) * spd, dmg, projId);
183	}
184	
185	/** 挂载头眼激光(:31459-31484):双侧眼(±18*scale,-22*scale)各一发 11 速;
186	 *  玩家在头正上/下方(localAI[1]==0)→ 双眼齐射,否则朝向侧单眼(±30*scale)12 速;伤 28,proj 259 */
187	function golemEyeLasers(game: GameHooks, e: Enemy, player: Player, side: number): void {
188	  const fire = (ox: number, spd: number) => {
189	    const sx = e.cx + ox, sy = e.cy - 22 * SCALE;
190	    const dx = player.cx - sx, dy = player.cy - sy;
191	    const d = Math.hypot(dx, dy) || 1;
192	    const vx = (dx / d) * spd, vy = (dy / d) * spd;
193	    shoot(game, sx + vx * 3, sy + vy * 3, vx, vy, 28, 259, 300);
194	  };
195	  if (side === 0) { fire(-18 * SCALE, 11); fire(18 * SCALE, 11); }
196	  else fire(side * 30 * SCALE, 12);
197	}
198	
199	/** 自由头眼激光(:31659-31717):双眼(±14*scale,-50*scale)各一发 proj 259;
200	 *  伤 24/速 11,本体(245)残血每降一档 +1 伤/+0.25 速(调用方传本体血量比值 r);
201	 *  无视线(flag49)→ 伤 ×1.5、速 ×2.5、按玩家速度随机提前量瞄准 */
202	function golemEyeLasersFree(
203	  game: GameHooks, e: Enemy, player: Player, noLos: boolean, r: number,
204	): void {
205	  for (let i = 0; i < 2; i++) {
206	    const sx = e.cx + (i === 0 ? -14 : 14) * SCALE;
207	    const sy = e.cy - 50 * SCALE;
208	    let dmg = 24, spd = 11;
209	    if (r < 0.5) { dmg += 1; spd += 0.25; }
210	    if (r < 0.4) { dmg += 1; spd += 0.25; }
211	    if (r < 0.3) { dmg += 1; spd += 0.25; }
212	    if (r < 0.2) { dmg += 1; spd += 0.25; }
213	    if (r < 0.1) { dmg += 1; spd += 0.25; }
214	    let tx = player.cx, ty = player.cy;
215	    if (noLos) {
216	      dmg = Math.floor(dmg * 1.5);
217	      spd *= 2.5;
218	      const pvx = (player as unknown as { vx: number }).vx ?? 0;
219	      const pvy = (player as unknown as { vy: number }).vy ?? 0;
220	      tx += pvx * Math.random() * 50;
221	      ty += pvy * Math.random() * 50;
222	    }
223	    const dx = tx - sx, dy = ty - sy;
224	    const d = Math.hypot(dx, dy) || 1;
225	    const vx = (dx / d) * spd, vy = (dy / d) * spd;
226	    shoot(game, sx + vx * 3, sy + vy * 3, vx, vy, dmg, 259, 300);
227	  }
228	}
229	
230	// ---------------------------------------------------------------------------
231	// AI_045 石巨人本体 245(NPC.cs:19447-19722)
232	// ---------------------------------------------------------------------------
233	
234	/** 挂载头 → 自由态(原版 HitEffect :85842-85847:246 血尽原地 NewNPC 249;
235	 *  本工程头原体变身,满血+属性对齐 249 SetDefaults :12139-12149) */
236	function golemHeadGoFree(e: Enemy, game: GameHooks): void {
237	  const x = headXOf(e);
238	  if (x.free) return;
239	  x.free = true;
240	  e.ai3 = 1;          // 自由态标记(探针/部件锚定可观测)
241	  e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;
242	  e.hp = e.maxHp;     // 原版 249 满血登场
243	  game.spawnParticles(e.cx, e.cy, '#C04030', 16, 2.6, { life: 30 });
244	  game.playSfx('roar', 1, e.cx, e.cy);   // :32587 style0 满响(曾 0.8,2026-08-18 对账修)
245	}
246	
247	export function golemAI(e: Enemy, game: GameHooks, player: Player | null) {
248	  const x = bodyXOf(e);
249	
250	  // ---- 血尽转换(首行):死亡演出 60t 后真死;头由自身 AI 转自由态续战 ----
251	  if (e.hp <= 0 && !x.dying) {
252	    x.dying = true; x.deadT = 0;
253	    e.ai3 = 1;          // 死亡标记(头据此转自由态)
254	    e.hp = e.maxHp;     // 满血续命防每 tick 重入
255	    // 原版本体血尽零吼(aiStyle54 块仅头自由 :32587 一声 Item8/:32577)——
256	    // 曾 0.9 吼与头自由吼构成同事件双吼,2026-08-18 对账删除
257	  }
258	
259	  // ---- 首帧:localAI[0]==0 生成部件(NPC.cs:19458-19467) ----
260	  //  原版 NewNPC 传左上角坐标:拳 247=(Center-84,-9)、248=(+78,-9)、头 246=(-3,-57)
261	  if (!e.bInit) {
262	    e.bInit = true;
263	    e.ai0 = 0; e.ai1 = 0; e.ai3 = 0;
264	    e.alphaFade = false;           // 接管渐显(原版 AI 内 alpha -= 10)
265	    const spawn = (id: number, ox: number, oy: number, side: number) => {
266	      const p = spawnPart(game, e, id);
267	      if (!p) return;
268	      p.x = e.cx + ox; p.y = e.cy + oy;
269	      p.ai0 = side;                // 拳 ai0=侧别(-1 左/1 右;头不使用)
270	    };
271	    spawn(247, -84, -9, -1);
272	    spawn(248, 78, -9, 1);
273	    spawn(246, -3, -57, 0);
274	  }
275	
276	  // ---- 出生渐显(NPC.cs:19477-19485):期间 ai[1]=0,蓄力冻结 ----
277	  if (fadeAlpha(e, x) > 0) e.ai1 = 0;
278	
279	  // ---- 死亡演出:无敌+碎裂尘,60t 后真死(头/拳继续) ----
280	  if (x.dying) {
281	    e.iframes = 2;
282	    e.vx *= 0.9;
283	    e.vy = Math.min(e.vy + GRAV, MAX_FALL);
284	    e.x += e.vx; e.y += e.vy;
285	    collideGround(e, game);
286	    x.deadT++;
287	    if (x.deadT % 6 === 0) {
288	      game.spawnParticles(
289	        e.cx + (Math.random() - 0.5) * e.w, e.cy + (Math.random() - 0.5) * e.h,
290	        '#B04030', 6, 2.4, { life: 36 });
291	    }
292	    if (x.deadT >= 60) { e.dead = true; return; }
293	    return;
294	  }
295	
296	  const num = balanceNum(game, player, 2);   // 本体 getGoodWorld +2(:19451-19454)
297	
298	  // ---- 部件存活扫描(NPC.cs:19487-19512):flag=头/flag2=左拳/flag3=右拳 ----
299	  //  注意头原体变身自由态后(ai3=1)视为"挂载头已失"——本体解除无敌且蓄力提速,
300	  //  对齐原版"246 死亡 → NewNPC 249"后 flag 为假的语义
301	  let hasHead = false, hasL = false, hasR = false;
302	  for (const n of game.enemies() as Enemy[]) {
303	    if (n.dead) continue;
304	    if (n.vanillaId === 246 && n.ai3 !== 1) hasHead = true;
305	    else if (n.vanillaId === 247) hasL = true;
306	    else if (n.vanillaId === 248) hasR = true;
307	  }
308	  // dontTakeDamage = 挂载头在场(NPC.cs:19513):一阶段本体无敌,先打头/拳
309	  if (hasHead) e.iframes = 2;
310	  // getGoodWorld 落体砸火把(:19510-19532):下落中(vy>0)扫过 AABB 的火把全部熄灭。
311	  // Y 上界用 width 是原版笔误,1:1 照抄
312	  if (game.world.seedFlags?.getGoodWorld && e.vy > 0) {
313	    smashTorches(game.world.store, e.x, e.x + e.w, e.y, e.y + e.w);
314	  }
315	
316	  // ---- 断臂尘(NPC.cs:19529-19595):原版整块被 !getGoodWorld 包住(FTW 下由砸火把
317	  //      取代,无断臂尘);此处每 10t 一簇粒子近似 ----
318	  if (!game.world.seedFlags?.getGoodWorld) {
319	    if (!hasL && e.aiT % 10 === 0) game.spawnParticles(e.cx - 80 * SCALE, e.cy - 9, '#9A8FA0', 3, 1.2, { life: 40 });
320	    if (!hasR && e.aiT % 10 === 0) game.spawnParticles(e.cx + 62 * SCALE, e.cy - 9, '#9A8FA0', 3, 1.2, { life: 40 });
321	  }
322	
323	  // ---- 跳跃穿墙解除(NPC.cs:19569-19578):下落低于玩家顶 / 有视线且自身不在块内 ----
324	  if (x.noTC && player && !player.dead) {
325	    if (e.vy > 0 && e.y + e.h > player.y) x.noTC = false;
326	    else if (losClear(game, e.cx, e.cy, player.cx, player.cy) && !hitSolid(game, e)) x.noTC = false;
327	  }
328	
329	  // TargetClosest 的 direction 近似:朝玩家符号,同侧回退 facing
330	  const dir = player ? (Math.sign(player.cx - e.cx) || e.facing || 1) : 1;
331	  if (player) e.facing = dir;
332	
333	  if (player && e.ai0 === 0) {
334	    // ---- 地面蓄力(NPC.cs:19580-19645):ai[1] 攒 300 → -20 蹲伏 20t → ==-1 起跳 ----
335	    //  蹲伏段(负值)num4 固定 1;蓄力段按断臂/残血提速,再乘脱庙狂暴系数
336	    if (e.vy === 0) {
337	      e.vx *= 0.8;
338	      let num4 = 1;
339	      if (e.ai1 > 0) {
340	        if (!hasL) num4 += 2;
341	        if (!hasR) num4 += 2;
342	        if (!hasHead) num4 += 2;
343	        if (e.hp < e.maxHp) num4 += 1;
344	        if (e.hp < e.maxHp / 2) num4 += 4;
345	        if (e.hp < e.maxHp / 3) num4 += 8;
346	        num4 *= num;
347	        if (game.world.seedFlags?.getGoodWorld) num4 += 100;   // :19613-19616(乘后再加)
348	      }
349	      e.ai1 += num4;
350	      if (e.ai1 >= 300) e.ai1 = -20;
351	      else if (e.ai1 === -1) {
352	        // 起跳(:19624-19643):穿墙跳,vx=4*dir;残血跳更高 -12.1*(num+9)/10 钳 -19.1
353	        x.noTC = true;
354	        e.vx = 4 * dir;
355	        e.vy = e.hp < e.maxHp ? Math.max(-19.1, (-12.1 * (num + 9)) / 10) : -12.1;
356	        e.ai0 = 1; e.ai1 = 0;
357	      }
358	    }
359	  } else if (player && e.ai0 === 1) {
360	    // ---- 跳跃段(NPC.cs:19646-19708) ----
361	    if (e.vy === 0) {
362	      // 落地(:19648-19661):Item14 音效 + 落地尘/Gore(曾借 roar 0.35,2026-08-18 对账修)
363	      game.playSfxWav?.('Item_14', 1, e.cx, e.cy);
364	      game.spawnParticles(e.cx, e.y + e.h, '#9A8FA0', 12, 2.2, { life: 40 });
365	      e.ai0 = 0;
366	    } else {
367	      // 玩家在身下水平跨度内 → 收横向速度(夹住玩家下压),否则朝玩家加速钳 ±num7
368	      if (e.x < player.x + player.w && e.x + e.w > player.x) {
369	        e.vx *= 0.9;
370	        if (e.y + e.h < player.y) e.vy += (0.2 * (num + 1)) / 2;
371	      } else {
372	        e.vx += 0.2 * dir;
373	        let num7 = 3;
374	        if (e.hp < e.maxHp) num7 += 1;
375	        if (e.hp < e.maxHp / 2) num7 += 1;
376	        if (e.hp < e.maxHp / 4) num7 += 1;
377	        num7 *= (num + 1) / 2;
378	        e.vx = clamp(e.vx, -num7, num7);
379	      }
380	    }
381	  }
382	
383	  // ---- 玩家死亡 vs 远离（NPC.cs:19469-19475 / 19709-19721）----
384	  // 玩家死：仅 noTileCollide=true（无 despawn 无状态切换，AI 继续跑）；
385	  // 活人曼哈顿 >3000：瞬消（二次判定 TargetClosest 后）
386	  if (!player) {
387	    x.noTC = true;
388	  } else if (Math.abs(e.cx - player.cx) + Math.abs(e.cy - player.cy) > 3000) {
389	    e.dead = true; e.bossFled = true;
390	    return;
391	  }
392	
393	  // ---- 重力+位移+落地(原版共享物理:noGravity=false → 0.3/2t、maxFall 10) ----
394	  e.vy = Math.min(e.vy + GRAV, MAX_FALL);
395	  e.x += e.vx;
396	  e.y += e.vy;
397	  if (!x.noTC) collideGround(e, game);
398	  else e.onGround = false;
399	}
400	
401	// ---------------------------------------------------------------------------
402	// aiStyle 46 挂载头 246(NPC.cs:31273-31499)+ aiStyle 48 自由头 249(NPC.cs:31500-31741)
403	// ---------------------------------------------------------------------------
404	
405	export function golemHeadAI(e: Enemy, game: GameHooks, player: Player | null) {
406	  const x = headXOf(e);
407	  if (e.vanillaId === 249) x.free = true;   // 直接生成的自由头(原版 NewNPC 249)
408	  if (!e.bInit) {
409	    e.bInit = true;
410	    e.ai0 = 0; e.ai1 = 0; e.ai2 = 0;
411	    e.ai3 = x.free ? 1 : 0;
412	    e.alphaFade = false;
413	    x.alpha = x.free ? 0 : 255;             // 249 SetDefaults 无 alpha(:12139-12149)
414	  }
415	
416	  // ---- 血尽转换(首行):自由头死=战斗结束全族自毁;挂载头死=转自由态 ----
417	  if (e.hp <= 0) {
418	    if (x.free) {
419	      e.dead = true;
420	      for (const n of game.enemies() as Enemy[]) {
421	        if (!n.dead && n !== e && n.vanillaId !== null && n.vanillaId >= 245 && n.vanillaId <= 249) n.dead = true;
422	      }
423	      game.spawnParticles(e.cx, e.cy, '#C04030', 20, 3, { life: 40 });
424	      // 原版自由头消亡零吼(aiStyle54 块仅 32577/32587/Item8)——曾自加 roar,2026-08-18 对账删
425	      return;
426	    }
427	    golemHeadGoFree(e, game);
428	  }
429	
430	  // ---- 属性:自由头按 249 SetDefaults(NPC.cs:12139-12149:damage 80/defense 32) ----
431	  if (x.free) {
432	    const free = vanillaNpc(249);
433	    e.def.damage = free?.damage ?? 80;
434	    e.def.defense = free?.defense ?? 32;
435	  } else {
436	    const b = baseOf(e);
437	    e.def.damage = b.dmg;
438	    e.def.defense = b.def;
439	  }
440	
441	  // 本体死亡/缺失 → 挂载头转自由态(本体死透后头继续)
442	  const body = findBody(game);
443	  if (!x.free && (!body || body.ai3 === 1 || body.hp <= 0)) golemHeadGoFree(e, game);
444	
445	  const num = balanceNum(game, player, 3);   // 挂载/自由头 getGoodWorld +3(:31277-31280/:31505-31508)
446	
447	  if (!x.free && body) {
448	    // ================= 挂载态 aiStyle 46(NPC.cs:31273-31499) =================
449	    // noTileCollide = true(:31284);锚点 = 本体.Center + (-3*scale,-57*scale)(:31290-31308)
450	    const dx = body.cx - 3 * SCALE - e.cx;
451	    const dy = body.cy - 57 * SCALE - e.cy;
452	    const dist = Math.hypot(dx, dy);
453	    if (dist < 100) { e.spin = 0; e.vx = dx; e.vy = dy; }        // 100 内整帧贴锚
454	    else { e.vx = (dx / dist) * 100; e.vy = (dy / dist) * 100; e.spin = e.vx * 0.1; }
455	    // 渐显(:31310-31317):期间 ai[1]=30
456	    if (fadeAlpha(e, x) > 0) e.ai1 = 30;
457	
458	    if (player) {
459	      if (e.ai0 === 0) {
460	        // ---- 嘴部火焰弹循环(:31319-31347):300t 一发 proj 258(伤 18 速 8) ----
461	        e.ai1 += 1;
462	        if (e.ai1 < 20 || e.ai1 > 280) { e.ai1 += (2 * (num - 1)) / 3; x.l0 = 1; }  // 张嘴帧
463	        else { e.ai1 += (1 * (num - 1)) / 2; x.l0 = 0; }
464	        if (e.ai1 >= 300) {
465	          e.ai1 = 0;
466	          golemSpit(game, e, player, 0, 10 * SCALE, 8, 18, 258);
467	        }
468	      } else if (e.ai0 === 1) {
469	        // ---- 眼部阶段(:31353-31486):嘴弹伤 24 + 眼激光 259(伤 28) ----
470	        x.l1 = player.cx < e.cx - e.w ? -1 : player.cx > e.cx + e.w ? 1 : 0;        // localAI[1]
471	        const num733 = (num + 3) / 4;
472	        e.ai1 += num733;
473	        if (e.hp < e.maxHp * 0.4) e.ai1 += num733;
474	        if (e.hp < e.maxHp * 0.2) e.ai1 += num733;
475	        x.l0 = e.ai1 < 20 || e.ai1 > 280 ? 1 : 0;
476	        if (e.ai1 >= 300) {
477	          e.ai1 = 0;
478	          golemSpit(game, e, player, x.l1 * 40 * SCALE, 10 * SCALE, 8, 24, 258);
479	        }
480	        e.ai2 += num733;
481	        if (e.hp < e.maxHp / 3) e.ai2 += num733;
482	        if (e.hp < e.maxHp / 4) e.ai2 += num733;
483	        if (e.hp < e.maxHp / 5) e.ai2 += num733;
484	        if (!losClear(game, e.cx, e.cy, player.cx, player.cy)) e.ai2 += 4;          // :31456 无视线催速
485	        if (e.ai2 > 60 + Math.random() * 600) {
486	          e.ai2 = 0;
487	          golemEyeLasers(game, e, player, x.l1);
488	        }
489	      }
490	      // 阶段派生(:31487-31491):血 < 半 → 眼部阶段
491	      e.ai0 = e.hp < e.maxHp / 2 ? 1 : 0;
492	    }
493	  } else {
494	    // ================= 自由态 aiStyle 48 GolemHeadFree(NPC.cs:31500-31741) =================
495	    // flag48(:31503-31515):头自身看不到玩家 → 穿墙 + 火焰弹不蓄满(头↔玩家视线)
496	    const rBody = findBody(game);
497	    const noLos = !player || !losClear(game, e.cx, e.cy, player.cx, player.cy);
498	    // flag49(:31646-31651):本体↔玩家无视线 → 激光催速 + 弹道预判;
499	    // 本体已亡(本移植死亡链)→ 退化为头↔玩家视线
500	    const noLosBody = rBody
501	      ? !player || !losClear(game, rBody.cx, rBody.cy, player.cx, player.cy)
502	      : noLos;
503	    if (player) {
504	      // 悬浮(:31521-31564):目标 = 玩家 + (0,-300),7 速/0.05 步进(符号翻转双步进)
505	      const dx = player.cx - e.cx, dy = player.cy - 300 - e.cy;
506	      const d = Math.hypot(dx, dy) || 1;
507	      e.vx = accelTo(e.vx, (dx / d) * 7, 0.05);
508	      e.vy = accelTo(e.vy, (dy / d) * 7, 0.05);
509	      // 火焰弹节奏(:31566-31595):num761=(num+4)/5,分档读本体(golemBoss=245)残血(:31574-31594)。
510	      // 本体已亡(本移植死亡链,原版无此态)→ 比值 0 = 全档,等价原版读尸体槽 life<=0 恒真
511	      const num761 = (num + 4) / 5;
512	      e.ai1 += num761;
513	      const r = rBody ? rBody.hp / rBody.maxHp : 0;
514	      if (r < 0.8) e.ai1 += num761;
515	      if (r < 0.6) e.ai1 += num761;
516	      if (r < 0.2) e.ai1 += num761;
517	      if (r < 0.1) e.ai1 += num761;
518	      x.l0 = e.ai1 < 20 || e.ai1 > 280 ? 1 : 0;   // 张嘴帧(:31584-31592)
519	      if (noLos) e.ai1 = 20;                       // :31593-31595 无视线时不蓄满
520	      if (e.ai1 >= 300) {                          // :31596-31617 嘴弹 proj 258(伤 20 速 8)
521	        e.ai1 = 0;
522	        golemSpit(game, e, player, 0, -10 * SCALE, 8, 20, 258);
523	      }
524	      // 眼激光节奏(:31618-31658):基数 num,分档读本体残血(:31626-31645;r 与上方火焰弹
525	      // 同源);激光伤/速分档(:31683-31705,阈值 0.5/0.4/0.3/0.2/0.1)经 golemEyeLasersFree 传 r
526	      e.ai2 += num;
527	      if (r < 1 / 1.25) e.ai2 += num;
528	      if (r < 1 / 1.5) e.ai2 += num;
529	      if (r < 1 / 2) e.ai2 += num;
530	      if (r < 1 / 3) e.ai2 += num;
531	      if (r < 1 / 4) e.ai2 += num;
532	      if (r < 1 / 5) e.ai2 += num;
533	      if (r < 1 / 6) e.ai2 += num;
534	      if (noLosBody) e.ai2 += num * 10;            // :31646-31651 flag49 催速
535	      if (e.ai2 > 100 + Math.random() * 4800) {
536	        e.ai2 = 0;
537	        golemEyeLasersFree(game, e, player, noLosBody, r);
538	      }
539	    }
540	    // :31721-31740 排焰尘(纯视觉,略)
541	  }
542	
543	  e.x += e.vx;
544	  e.y += e.vy;
545	}
546	
547	// ---------------------------------------------------------------------------
548	// AI_047 石巨人拳 247/248(NPC.cs:19171-19446)
549	// ---------------------------------------------------------------------------
550	// 原版 ai[0] 是状态机(0 归位/1 蓄力/2 冲拳/3 直飞);任务约定 ai0=侧别,
551	// 状态机落在本文件 WeakMap(fistX.state),计时仍用 ai[1]。
552	
553	export function golemFistAI(e: Enemy, game: GameHooks, player: Player | null) {
554	  const x = fistXOf(e);
555	  if (!e.bInit) {
556	    e.bInit = true;
557	    e.ai0 = e.vanillaId === 247 ? -1 : 1;   // ai0=侧别(-1 左拳/1 右拳;由本体生成时预置)
558	    e.ai1 = 0;
559	    e.alphaFade = false;
560	    x.alpha = 255;
561	  }
562	  const isLeft = e.vanillaId === 247;
563	
564	  // ---- 锚主:golemBoss 缺失 → 自毁(NPC.cs:19182-19186) ----
565	  //  本体存活(含死亡演出)→ 锚本体;本体死透 → 锚自由头(任务约定"锚定本体(或头)")
566	  const body = findBody(game);
567	  const head = findHead(game);
568	  const anchor = body && !body.dead ? body : head;
569	  if (!anchor) { e.dead = true; return; }
570	  e.master = anchor; // 拳链渲染用（Renderer.drawGolemFistChain，Main.cs:22593-22632）
571	
572	  const num = balanceNum(game, player, 3);   // 拳 getGoodWorld +3(:19173-19176)
573	  // 渐显(:19187-19194):期间 ai[1]=0
574	  if (fadeAlpha(e, x) > 0) e.ai1 = 0;
575	
576	  // ---- 肩锚点(:19197-19199):锚主.Center + 锚主.velocity + (±84/78*scale, -9*scale) ----
577	  const offX = isLeft ? -84 : 78;
578	  const tx = anchor.cx + anchor.vx + offX * SCALE;
579	  const ty = anchor.cy + anchor.vy - 9 * SCALE;
580	  const dx = tx - e.cx, dy = ty - e.cy;
581	  const dist = Math.hypot(dx, dy);
582	  e.facing = isLeft ? 1 : -1;               // 镜像朝向(原版贴图方向)
583	
584	  if (!player) { e.x += e.vx; e.y += e.vy; return; }
585	
586	  if (x.state === 0) {
587	    // ---- 归位/待机蓄力(:19202-19270) ----
588	    x.noTC = true;
589	    let num3 = 14;
590	    if (e.hp < e.maxHp / 2) num3 += 3;
591	    if (e.hp < e.maxHp / 4) num3 += 3;
592	    if (anchor.hp < anchor.maxHp) num3 += 8;
593	    num3 *= (num + 3) / 4;
594	    if (num3 > 32) num3 = 32;
595	    if (dist < 12 + num3) {
596	      // 贴肩:整帧速度 = 偏移量(原版 velocity = delta),蓄力计时(:19216-19259)
597	      e.spin = 0;
598	      e.vx = dx; e.vy = dy;
599	      e.ai1 += num;
600	      if (e.hp < e.maxHp / 2) e.ai1 += num;
601	      if (e.hp < e.maxHp / 4) e.ai1 += num;
602	      if (anchor.hp < anchor.maxHp) e.ai1 += 10 * num;
603	      if (e.ai1 >= 60) {
604	        // 出拳侧别门(:19244-19256):左拳只在玩家偏左时出、右拳对称
605	        const sideOk = isLeft ? e.cx + 100 > player.cx : e.cx - 100 < player.cx;
606	        e.ai1 = 0;
607	        if (sideOk) x.state = 1;
608	      }
609	    } else {
610	      e.vx = (dx / dist) * num3;
611	      e.vy = (dy / dist) * num3;
612	      // 归位朝向(:19260-19262):默认 atan2(-vy,-vx),247 镜像为 atan2(vy,vx)
613	      e.spin = isLeft ? Math.atan2(e.vy, e.vx) : Math.atan2(-e.vy, -e.vx);
614	    }
615	  } else if (x.state === 1) {
616	    // ---- 蓄力:贴肩 30t(:19271-19332) ----
617	    e.ai1 += 1;
618	    e.x = tx - e.w / 2;                     // 原版 base.Center = vector(整帧钉在肩锚)
619	    e.y = ty - e.h / 2;
620	    e.spin = 0; e.vx = 0; e.vy = 0;
621	    if (e.ai1 <= 15) {                      // :19278-19292 聚能尘(粒子近似)
622	      game.spawnParticles(
623	        e.cx + (Math.random() - 0.5) * 30, e.cy + (Math.random() - 0.5) * 30,
624	        '#C8A040', 1, 0.8, { life: 26 });
625	    }
626	    if (e.ai1 >= 30) {
627	      x.noTC = true;
628	      x.state = 2; e.ai1 = 0;
629	      // 冲拳速度(:19302-19321):12 + 残血/本体受损加成,×(num+3)/4 钳 48
630	      let num6 = 12;
631	      if (e.hp < e.maxHp / 2) num6 += 4;
632	      if (e.hp < e.maxHp / 4) num6 += 4;
633	      if (anchor.hp < anchor.maxHp) num6 += 10;
634	      num6 *= (num + 3) / 4;
635	      if (num6 > 48) num6 = 48;
636	      const pdx = player.cx - e.cx, pdy = player.cy - e.cy;
637	      const pd = Math.hypot(pdx, pdy) || 1;
638	      e.vx = (pdx / pd) * num6; e.vy = (pdy / pd) * num6;
639	      // 冲拳朝向(:19325-19328):默认 atan2(vy,vx),247 镜像为 atan2(-vy,-vx)(与归位相反)
640	      e.spin = isLeft ? Math.atan2(-e.vy, -e.vx) : Math.atan2(e.vy, e.vx);
641	    }
642	  } else if (x.state === 2) {
643	    // ---- 冲拳飞行(:19333-19393) ----
644	    // getGoodWorld 冲拳沿途砸火把(:19335-19362):AABB 外扩 1 格扫过即熄
645	    // (Y 上界同样用 width,原版笔误 1:1)
646	    if (game.world.seedFlags?.getGoodWorld) {
647	      smashTorches(game.world.store, e.x - TILE, e.x + e.w + TILE, e.y - TILE, e.y + e.w + TILE);
648	    }
649	    e.ai1 += 1;
650	    if (e.ai1 === 1) game.playSfxWav?.('Item_14', 1, e.cx, e.cy);   // SoundID.Item14(:19344-19346;曾借 roar 0.4)
651	    if (e.aiT % 2 === 0) {                        // :19348-19356 焰尾尘(粒子近似)
652	      game.spawnParticles(e.cx + e.vx * 0.5, e.cy + e.vy * 0.5, '#E08040', 1, 0.6, { life: 20 });
653	    }
654	    // 过轴判定(:19363-19388):主轴冲过玩家 → 关穿墙(开始撞墙)
655	    if (Math.abs(e.vx) > Math.abs(e.vy)) {
656	      if (e.vx > 0 && e.cx > player.cx) x.noTC = false;
657	      if (e.vx < 0 && e.cx < player.cx) x.noTC = false;
658	    } else {
659	      if (e.vy > 0 && e.cy > player.cy) x.noTC = false;
660	      if (e.vy < 0 && e.cy < player.cy) x.noTC = false;
661	    }
662	    // 离锚 700 → 回位(:19389-19392;撞墙分支在位移后判定)
663	    if (dist > 700) { x.noTC = true; x.state = 0; }
664	  } else if (x.state === 3) {
665	    // ---- 直飞追击(:19394-19446;原版无处置 ai[0]=3 的代码,保留 1:1) ----
666	    x.noTC = true;
667	    const pdx = player.cx - e.cx, pdy = player.cy - e.cy;
668	    const pd = Math.hypot(pdx, pdy) || 1;
669	    e.vx = accelTo(e.vx, (pdx / pd) * 12, 0.4);
670	    e.vy = accelTo(e.vy, (pdy / pd) * 12, 0.4);
671	    e.spin = isLeft ? Math.atan2(-e.vy, -e.vx) : Math.atan2(e.vy, e.vx);
672	  }
673	
674	  // ---- 位移(蓄力态已整帧钉锚;冲拳非穿墙段撞墙即回位) ----
675	  if (x.state !== 1) {
676	    e.x += e.vx;
677	    e.y += e.vy;
678	    if (x.state === 2 && !x.noTC && hitSolid(game, e)) {
679	      x.noTC = true;
680	      x.state = 0;                          // :19389-19392 collideX/collideY → 回位
681	    }
682	  }
683	}
684	

```


---

## 👤 User(sidechain) · 2026-08-19T03:09:38.669Z

**📎 ToolResult**

```
1	// 鹿角怪 668 全链（NPC.cs AI_123_Deerclops :44338-44752 + 尖刺/碎石助手 :44754-44955
2	// + Movement :44957-45042 + 弹幕 961/962/965）1:1 移植。
3	//   状态机 ai0：-1 入场走位 / 0 追击选招 / 1 前向尖刺 / 2 碎石喷发 / 3 咆哮减速 /
4	//   4 双侧尖刺 / 5 影手六连 / 6 回家 / 7 回家落地传送 / 8 离场消散。
5	//   ai1=段内计数；ai2/ai3=家 tile（首帧落点）；lai0=空中标志（Movement 用）；
6	//   lai2=专家影手被动计数；lai3=远距免伤爬升（≥450px 每 t+1,满 30 免伤；
7	//   近距 -1）+出生红雾源。
8	//   近似：Boss_CanShootExtraAt（多人）→ 单人 1200px 距离门；dust 109 → 粒子。
9	import { Entity } from './Entity';
10	import type { Enemy } from './Enemy';
11	import type { GameHooks } from './types';
12	import type { Player } from './Player';
13	import { BuffType } from '../stats/Buffs';
14	import { TILE } from '../core/constants';
15	
16	const SCREAM = ['deerclops_scream_0', 'deerclops_scream_1', 'deerclops_scream_2'];
17	const ICE = ['deerclops_ice_attack_0', 'deerclops_ice_attack_1', 'deerclops_ice_attack_2'];
18	
19	/** WorldGen.SolidTile 语义（active+solid） */
20	function solidAt(game: GameHooks, x: number, y: number): boolean {
21	  const st = game.world.store;
22	  return st.inBounds(x, y) && st.flags[st.idx(x, y)] !== 0 && !!st.isSolid(x, y);
23	}
24	
25	/** WorldGen.ActiveAndWalkableTile：active 且非 solidTop 平台族（本仓 isPlatform 近似） */
26	function walkableAt(game: GameHooks, x: number, y: number): boolean {
27	  const st = game.world.store;
28	  return st.inBounds(x, y) && st.flags[st.idx(x, y)] !== 0 && !st.isPlatform(x, y);
29	}
30	
31	/** Collision.SolidCollision（px 盒内有实心块；acceptTopSurfaces=false 时半砖/上坡不算） */
32	function solidCollisionPx(game: GameHooks, x: number, y: number, w: number, h: number): boolean {
33	  const st = game.world.store;
34	  const i0 = Math.floor(x / TILE), j0 = Math.floor(y / TILE);
35	  const i1 = Math.floor((x + w - 0.01) / TILE), j1 = Math.floor((y + h - 0.01) / TILE);
36	  for (let i = i0; i <= i1; i++) {
37	    for (let j = j0; j <= j1; j++) {
38	      if (!st.inBounds(i, j)) continue;
39	      const idx = st.idx(i, j);
40	      if (st.flags[idx] !== 0 && st.isSolid(i, j)) return true;
41	    }
42	  }
43	  return false;
44	}
45	
46	/** ShouldRunAway（NPC.cs:44716-44738）：死/出雪原（或离家 480px 内视为雪原）且非追击态/
47	 *  离玩家 2400px → 撤。isChasing=false 时"非雪原"即撤（回家态）。
48	 *  zoneSnow 读 game.scene（SceneMetrics 每 15t 刷新）——★勿读 player 字段(不存在) */
49	function shouldRunAway(e: Enemy, game: GameHooks, p: Player | null, isChasing: boolean, homeX: number, homeY: number): boolean {
50	  if (!p || p.dead) return true;
51	  const zoneSnow = !!game.scene?.zoneSnow
52	    || Math.hypot(p.cx - homeX * TILE, p.cy - homeY * TILE) <= 480;
53	  if (!isChasing && !zoneSnow) return true;
54	  return Math.hypot(p.cx - e.cx, p.cy - e.cy) >= 2400;
55	}
56	
57	/** AI_123 主状态机（NPC.cs:44338-44752） */
58	export function deerclopsAI(e: Enemy, game: GameHooks, p: Player | null): void {
59	  if (e.ai0 === -1120) e.ai0 = 0;   // 本仓 ai0 缺省 -1120（史莱姆族哨兵）→ 原版 ai[0] 缺省 0
60	  const DMG_HANDS = 15;   // 主线影手/咆哮段伤害（外层 num）
61	  const far = p != null && !p.dead && Math.hypot(p.cx - e.cx, p.cy - e.cy) >= 450;
62	  // :44346-44347 lai3 远距爬升 + 免伤（下界 -10 供入场段清零语义）
63	  e.lai3 = Math.max(-10, Math.min(30, e.lai3 + (far ? 1 : -1)));
64	  e.dontTakeDamage = e.lai3 >= 30;
65	  if (e.lai3 > 0) {
66	    // :44352-44360 红雾（dust 109）密度随 lai3/30
67	    const k = e.lai3 / 30;
68	    let n = Math.random() * k * 3;
69	    while (n > 0) { n -= 1; game.spawnParticles(e.cx, e.cy, '#A03030', 1, 1.4, { life: 30, grav: -0.04 }); }
70	  }
71	  // :44362-44374 家 tile 初始化（首帧落点 → ai2/ai3）+ 离场计时
72	  if (e.ai2 === 0 && e.ai3 === 0) {
73	    e.ai2 = Math.floor(e.cx / TILE);
74	    e.ai3 = Math.floor((e.y + e.h) / TILE);
75	    e.despawnTimer = 86400;
76	  }
77	  if (e.despawnTimer > 0) e.despawnTimer--;
78	  const homeX = e.ai2, homeY = e.ai3;
79	  // :44378-44382 专家被动影手（SpawnPassiveShadowHands :44723-44752：
80	  //   间隔随血量 80→40t,连发 3 只后重置;单人近似 Boss_CanShootExtraAt=1200px 门）
81	  if (game.world.isExpert && p && !p.dead) {
82	    const lifePct = e.hp / e.maxHp;
83	    const interval = Math.round(80 + (0 - (1 - lifePct)) * 40 || 40);
84	    e.lai2 += 1;
85	    const idx = e.lai2 / interval;
86	    if (e.lai2 % interval === 0 && idx < 3
87	      && Math.hypot(p.cx - e.cx, p.cy - e.cy) < 1200) {
88	      addProj(game, new InsanityShadowProj(p, 10, Math.floor(idx) % 3));
89	    }
90	    if (idx >= 3) e.lai2 = 0;
91	  } else {
92	    e.lai2 = 0;
93	  }
94	
95	  let halt = false, goHome = false;
96	  switch (e.ai0) {
97	    case -1: e.lai3 = -10; break;                    // :44386-44387
98	    case 6: {                                        // 回家态 :44389-44439
99	      if (p && !p.dead && !shouldRunAway(e, game, p, false, homeX, homeY)) {
100	        e.ai0 = 0; e.ai1 = 0; e.lai1 = 0; break;
101	      }
102	      if (e.despawnTimer <= 0) { e.ai0 = 8; e.ai1 = 0; e.lai1 = 0; break; }
103	      goHome = true;
104	      e.ai1 += 1;
105	      const homePx = { x: homeX * TILE, y: homeY * TILE };
106	      const aboveLine = e.y < homePx.y + 1600;       // 原版 Top.Y > other.Y+1600 = 深于家 1600px
107	      const nearHome = Math.hypot(homePx.x - e.cx, homePx.y - e.cy) < 1020;
108	      if (nearHome && e.ai1 % 600 < 420) halt = true;
109	      if ((!aboveLine && e.ai1 >= 300) || (!nearHome && e.ai1 >= 1500)) {
110	        // 深于家 1600px 且 >300t,或远离超 1500t → 落地传送段
111	        e.ai0 = 7; e.ai1 = 0; e.lai1 = 0;
112	      }
113	      break;
114	    }
115	    case 0: {                                        // 追击选招 :44441-44526
116	      if (!p || p.dead || shouldRunAway(e, game, p, true, homeX, homeY)) {
117	        e.ai0 = 6; e.ai1 = 0; e.lai1 = 0; break;
118	      }
119	      e.ai1 += 1;
120	      // 玩家脚底参考点（base.Bottom-32 → 目标盒最近点）
121	      const vx = e.cx, vy = e.y + e.h - 32;
122	      const tx = Math.max(p.x, Math.min(vx, p.x + p.w));
123	      const ty = Math.max(p.y, Math.min(vy, p.y + p.h));
124	      const dx = tx - vx, dy = ty - vy;
125	      const facingX = Math.abs(dx) >= Math.abs(dy) * 0.6 || Math.hypot(dx, dy) < 48;
126	      const nearVert = dy <= 100 + p.h && dy >= -200;
127	      if (Math.abs(dx) < 120 && nearVert && e.vy === 0 && e.lai1 >= 2) {
128	        e.vx = 0; e.ai0 = 4; e.ai1 = 0; e.lai1 = 0; break;   // 双侧尖刺
129	      }
130	      if (Math.abs(dx) < 120 && nearVert && e.vy === 0 && facingX) {
131	        e.vx = 0; e.ai0 = 1; e.ai1 = 0; e.lai1 += 1; break;  // 前向尖刺
132	      }
133	      if (e.vy === 0 && e.vx !== 0 && e.ai1 >= 240) {
134	        e.vx = 0; e.ai0 = 2; e.ai1 = 0; e.lai1 = 0; break;   // 碎石
135	      }
136	      if (e.vy === 0 && e.vx === 0 && e.ai1 >= 90) {
137	        e.vx = 0; e.ai0 = 5; e.ai1 = 0; e.lai1 = 0; break;   // 影手
138	      }
139	      if (e.vy === 0 && e.ai1 >= 120 && Math.abs(dx) > 100 && !p.buffs.has(BuffType.Slow)) {
140	        e.vx = 0; e.ai0 = 3; e.ai1 = 0; e.lai1 = 0;          // 咆哮减速
141	      }
142	      break;
143	    }
144	    case 1:                                          // 前向尖刺 :44528-44538
145	      e.ai1 += 1; halt = true;
146	      makeSpikesForward(game, e, p, 1);
147	      if (e.ai1 >= 80) { e.ai0 = 0; e.ai1 = 0; }
148	      break;
149	    case 4:                                          // 双侧尖刺 :44530-44543
150	      e.ai1 += 1; halt = true;
151	      makeSpikesBothSides(game, e, p, 1);
152	      if (e.ai1 >= 90) { e.ai0 = 0; e.ai1 = 0; }
153	      break;
154	    case 2: {                                        // 碎石喷发 :44545-44588
155	      const START = 32;                              // num8=4 → num9=8×4=32
156	      e.ai1 += 1;
157	      if (e.ai1 === START - 20) game.playSfxFiles(SCREAM, 1, e.cx, e.cy);
158	      if (e.ai1 === START) game.playSfxFile?.('deerclops_rubble_attack', 1, e.cx, e.cy);
159	      halt = true;
160	      if (e.ai1 >= START) {
161	        const srcX = Math.floor(e.cx / TILE) + e.facing * 3;
162	        const srcY = Math.floor(e.y / TILE) - 10;
163	        const since = e.ai1 - START;
164	        if (since === 0) punch(game, e.cx, e.cy, 0, -1, 30);
165	        // 每 t 一颗（num12=1）,共 20 颗
166	        shootRubbleUp(game, e, p, srcX, srcY, 20, 1, 200, since);
167	      }
168	      if (e.ai1 >= 60) { e.ai0 = 0; e.ai1 = 0; }     // :44587
169	      break;
170	    }
171	    case 3:                                          // 咆哮减速 :44589-44623
172	      if (e.ai1 === 30) { game.playSfxFiles(SCREAM, 1, e.cx, e.cy); e.facing = p && p.cx > e.cx ? 1 : -1; }
173	      e.ai1 += 1; halt = true;
174	      if (e.ai1 % 4 === 0 && e.ai1 >= 28) {
175	        punch(game, e.cx, e.cy, Math.cos(Math.random() * Math.PI * 2), Math.sin(Math.random() * Math.PI * 2), 20);
176	        // :44609-44616 800px 内玩家无 Slow(buff32) → AddBuff(32, 720t)
177	        if (p && !p.dead && Math.hypot(p.cx - e.cx, p.cy - e.cy) < 800 && !p.buffs.has(BuffType.Slow)) {
178	          p.buffs.apply(BuffType.Slow, 720 / 60);
179	        }
180	      }
181	      if (e.ai1 >= 60) { e.ai0 = 0; e.ai1 = 0; }
182	      break;
183	    case 7:                                          // 回家落地 :44624-44646
184	      if (e.ai1 === 30) game.playSfxFiles(SCREAM, 1, e.cx, e.cy);
185	      e.ai1 += 1; halt = true;
186	      if (e.ai1 % 4 === 0 && e.ai1 >= 28) {
187	        punch(game, e.cx, e.cy, Math.cos(Math.random() * Math.PI * 2), Math.sin(Math.random() * Math.PI * 2), 20);
188	      }
189	      if (e.ai1 === 40) {                            // :44637-44641 传送回家（Bottom 落点）
190	        if (p && !p.dead) e.facing = p.cx > e.cx ? 1 : -1;
191	        e.x = homeX * TILE - e.w / 2;
192	        e.y = homeY * TILE - e.h;
193	      }
194	      if (e.ai1 >= 60) { e.ai0 = 0; e.ai1 = 0; }
195	      break;
196	    case 8:                                          // 离场消散 :44647-44670
197	      if (e.ai1 === 30) game.playSfxFiles(SCREAM, 1, e.cx, e.cy);
198	      e.ai1 += 1; halt = true;
199	      if (e.ai1 % 4 === 0 && e.ai1 >= 28) {
200	        punch(game, e.cx, e.cy, Math.cos(Math.random() * Math.PI * 2), Math.sin(Math.random() * Math.PI * 2), 20);
201	      }
202	      if (e.ai1 >= 40) {
203	        // :44667-44670 life=-1 → 无掉落消散（直置 dead 绕过 hurt 死亡链即无掉落/公告）
204	        e.hp = -1; e.dead = true;
205	        return;
206	      }
207	      break;
208	    case 5:                                          // 影手六连 :44671-44707
209	      if (e.ai1 === 30) {
210	        game.playSfxFiles(SCREAM, 1, e.cx, e.cy);
211	        if (p && !p.dead) e.facing = p.cx > e.cx ? 1 : -1;
212	        for (let i = 0; i < 6; i++) addProj(game, new InsanityShadowProj(p, DMG_HANDS, i % 3));
213	      }
214	      e.ai1 += 1; halt = true;
215	      if (e.ai1 % 4 === 0 && e.ai1 >= 28) {
216	        punch(game, e.cx, e.cy, Math.cos(Math.random() * Math.PI * 2), Math.sin(Math.random() * Math.PI * 2), 20);
217	      }
218	      if (e.ai1 >= 60) { e.ai0 = 0; e.ai1 = 0; }
219	      break;
220	  }
221	  deerclopsMovement(e, game, p, halt, goHome, homeX, homeY);
222	}
223	
224	/** PunchCameraModifier 近似（Main.instance.CameraModifiers） */
225	function punch(game: GameHooks, x: number, y: number, dirX: number, dirY: number, frames: number): void {
226	  void x; void y;
227	  game.punchCamera?.(dirX, dirY, frames);
228	}
229	
230	/** AI_123_Deerclops_MakeSpikesForward（:44776-44810）:ai1≥36 起每 4t 一根,前向 20 根 */
231	function makeSpikesForward(game: GameHooks, e: Enemy, p: Player | null, slot: number): void {
232	  const LEAD = 36;
233	  const ai1 = slot === 1 ? e.ai1 : e.lai1;
234	  if (ai1 < LEAD) return;
235	  const srcX = Math.floor((e.x + e.w / 2) / TILE) + e.facing * 3;
236	  const srcY = Math.floor((e.y + e.h) / TILE);
237	  const since = ai1 - LEAD;
238	  if (since === 0) punch(game, e.cx, e.cy, 0, 1, 30);
239	  const step = Math.floor(since / 4) * 4;
240	  const hi = since % 4 === 0 ? step + 4 : step;
241	  for (let i = step; i < hi && i < 20; i++) {
242	    tryMakingSpike(game, e, p, srcX, srcY, e.facing, 20, i, i);
243	  }
244	}
245	
246	/** AI_123_Deerclops_MakeSpikesBothSides（:44812-44842）:ai1≥56 起每 2t,双侧各 15 根 */
247	function makeSpikesBothSides(game: GameHooks, e: Enemy, p: Player | null, slot: number): void {
248	  const LEAD = 56;
249	  const ai1 = slot === 1 ? e.ai1 : e.lai1;
250	  if (ai1 < LEAD) return;
251	  const srcX = Math.floor((e.x + e.w / 2) / TILE) + e.facing * 3;
252	  const srcY = Math.floor((e.y + e.h) / TILE);
253	  const since = ai1 - LEAD;
254	  if (since === 0) punch(game, e.cx, e.cy, 0, 1, 30);
255	  const step = Math.floor(since / 2) * 2;
256	  const hi = since % 2 === 0 ? step + 2 : step;
257	  for (let i = step; i >= 0 && i < hi && i < 15; i++) {
258	    tryMakingSpike(game, e, p, srcX, srcY, e.facing, 15, -i, i);
259	    tryMakingSpike(game, e, p, srcX, srcY, -e.facing, 15, -i, i);
260	  }
261	}
262	
263	/** AI_123_Deerclops_TryMakingSpike（:44887-44908）：落点 BestY + 961 弹（伤害 13,
264	 *  ai1 = 0.1+rand0.1+xOffset*1.1/howMany 尺度相位） */
265	function tryMakingSpike(
266	  game: GameHooks, e: Enemy, p: Player | null,
267	  srcX: number, srcY: number, dir: number, howMany: number, whichOne: number, xOffset: number,
268	): void {
269	  const DMG = 13;
270	  const x = srcX + xOffset * dir;
271	  const y = findBestSpikeY(game, e, p, srcY, x);
272	  if (!walkableAt(game, x, y)) return;
273	  const px = x * TILE + 8, py = y * TILE - 8;
274	  const ang = -Math.PI / 2 + whichOne * dir * 0.7 * (Math.PI / 4 / howMany);
275	  addProj(game, new DeerclopsSpikeProj(px, py, ang, DMG,
276	    0.1 + Math.random() * 0.1 + (xOffset * 1.1) / howMany));
277	}
278	
279	/** AI_123_Deerclops_TryMakingSpike_FindBestY（:44900-44955）：目标侧向找最近可行走面,
280	 *  再上拔 20 格出实心、下探 20 格落到可行走 */
281	function findBestSpikeY(game: GameHooks, e: Enemy, p: Player | null, srcY: number, x: number): number {
282	  void e;
283	  let y = srcY;
284	  if (p && !p.dead) {
285	    const tBottom = Math.floor((p.y + p.h) / TILE);
286	    const sgn = Math.sign(tBottom - srcY) || 1;
287	    const end = tBottom + sgn * 15;
288	    let best: number | null = null, bestD = Infinity;
289	    for (let i = srcY; i !== end; i += sgn) {
290	      if (!game.world.store.inBounds(x, i)) continue;
291	      if (walkableAt(game, x, i)) {
292	        const d = Math.abs(i * TILE + 8 - (p.y + p.h));
293	        if (best === null || d < bestD) { best = i; bestD = d; }
294	      }
295	    }
296	    if (best !== null) y = best;
297	  }
298	  for (let k = 0; k < 20; k++) {                 // 上拔出实心
299	    if (y < 10 || !solidAt(game, x, y)) break;
300	    y--;
301	  }
302	  for (let k = 0; k < 20; k++) {                 // 下探到可行走
303	    if (y > game.world.store.h - 10 || walkableAt(game, x, y)) break;
304	    y++;
305	  }
306	  return y;
307	}
308	
309	/** AI_123_Deerclops_ShootRubbleUp（:44754-44781）：从实心块顶喷 962 碎石（伤害 18,
310	 *  速度 = (0,-1) 旋 (whichOne*dir)*0.7*π/4/howMany × (8+rand8)） */
311	function shootRubbleUp(
312	  game: GameHooks, e: Enemy, p: Player | null,
313	  srcX: number, srcY: number, howMany: number, dist: number, upBias: number, whichOne: number,
314	): void {
315	  void p;
316	  const DMG = 18;
317	  const offset = whichOne * dist;
318	  for (let i = 0; i < 35; i++) {
319	    const x = srcX + offset * e.facing, y = srcY + i;
320	    if (!solidAt(game, x, y)) continue;
321	    const ang = -Math.PI / 2 + whichOne * e.facing * 0.7 * (Math.PI / 4 / howMany);
322	    const spd = 8 + Math.random() * 8;
323	    // ai[1] = rand(projFrames[962] × 4) = rand(12)——3×4 网格全 12 格随机(NPC.cs:44768-44770;
324	    // 此前误写 6..11 只取下两行)
325	    addProj(game, new DeerclopsRubbleProj(x * TILE + 8, y * TILE - 8,
326	      Math.cos(ang) * spd, Math.sin(ang) * spd, DMG, Math.floor(Math.random() * 12)));
327	    break;
328	  }
329	}
330	
331	/** AI_123_Deerclops_Movement（:44957-45042）：自定义重力/跳跃（noTileCollide 下自管垂直） */
332	function deerclopsMovement(
333	  e: Enemy, game: GameHooks, p: Player | null,
334	  halt: boolean, goHome: boolean, homeX: number, homeY: number,
335	): void {
336	  const rage = 1 - e.hp / e.maxHp;
337	  const speed = 3.5 + rage;                    // :44959 num3 = 3.5 + 1×(1-lifeFrac)
338	  let tx: number, ty: number, tw: number, th: number;
339	  if (goHome) {
340	    tx = homeX * TILE; ty = homeY * TILE; tw = 16; th = 16;
341	    if (Math.hypot(tx - e.cx, ty - e.cy) < 240) { tx = e.cx + 160 * e.facing; }
342	  } else if (p && !p.dead) {
343	    tx = p.x; ty = p.y; tw = p.w; th = p.h;
344	  } else {
345	    tx = e.cx + 100 * e.facing; ty = e.y; tw = 16; th = 16;
346	  }
347	  const dx = (tx + tw / 2) - e.cx;
348	  const adx = Math.abs(dx);
349	  if (goHome && dx !== 0) e.facing = Math.sign(dx);
350	  const nearX = adx < 80;
351	  let stop = nearX || halt;
352	  let spd = speed;
353	  let dir = dx;
354	  if (e.ai0 === -1) { dir = 5; spd = 5.35; stop = false; }   // :44985-44988 入场
355	  if (stop) {
356	    e.vx *= 0.9;
357	    if (Math.abs(e.vx) < 0.1) e.vx = 0;
358	  } else {
359	    e.vx += (Math.sign(dir) * spd - e.vx) / 4;                // Lerp(v, target, 1/4)
360	  }
361	  // :44998-45018 底部碰撞探针（40×20）+ 前方净空（16×80）
362	  const bx = e.cx - 20, by = e.y + e.h - 20;
363	  const straddle = bx < tx && bx + e.w > tx + tw;             // num13：横跨目标
364	  const targetAbove = by + 20 < ty + th - 16;                 // flag3
365	  const teleporting = e.ai0 === 7;
366	  const ground = solidCollisionPx(game, bx, by, 40, 20);
367	  const groundHigh = solidCollisionPx(game, bx, by, 40, 16);
368	  const openAhead = !solidCollisionPx(game, bx + 40 * e.facing, by, 16, 80);
369	  if (ground || groundHigh) e.lai0 = 0;
370	  if (teleporting) e.vy = -0.1;
371	  if ((straddle || nearX) && targetAbove) {
372	    e.vy = Math.min(Math.max(e.vy + 0.8, 0.001), 16);         // 落到目标层
373	  } else if (ground && !groundHigh) {
374	    e.vy = 0;                                                 // 半砖缘站定
375	  } else if (ground) {
376	    e.vy = Math.max(Math.min(e.vy - 0.4, 0), -8);             // 贴地
377	  } else if (e.vy === 0 && openAhead) {
378	    e.vy = -8; e.lai0 = 1;                                    // 起跳
379	  } else {
380	    e.vy = Math.min(Math.max(e.vy + 0.4, -8), 16);            // 重力
381	  }
382	  // 位置积分（SetDefaults :17384 noGravity+noTileCollide → 原版引擎直移穿墙；
383	  // AI 只经底部/前方探针模拟"贴地行走"）。★曾整段漏接——AI 状态机照跑但坐标
384	  // 永不动 = 召唤在哪冻在哪（2026-08-19 用户实报"冻结在半空"，探针复现恒 y）
385	  e.x += e.vx;
386	  e.y += e.vy;
387	}
388	
389	// ---------------------------------------------------------------------------
390	// 弹幕 961 冰尖刺（AI_157_SharpTears :48432-48567 type==961 段）
391	// ---------------------------------------------------------------------------
392	export class DeerclopsSpikeProj extends Entity {
393	  w = 32; h = 32;
394	  dead = false;
395	  private ai0 = 0;
396	  private readonly ai1: number;
397	  private opacity = 0;      // Opacity（0-1 语义）
398	  private readonly rot: number;
399	  /** 变体帧:AI_157 flag=true → frame=rand(5)（Projectile.cs:48487-48490,maxValue=5） */
400	  private readonly frame: number;
401	  life = 20;                // num9=20 出世
402	  constructor(x: number, y: number, angle: number, private dmg: number, ai1: number) {
403	    super();
404	    this.x = x - this.w / 2; this.y = y - this.h / 2;
405	    this.rot = angle;
406	    this.ai1 = ai1;
407	    this.frame = Math.floor(Math.random() * 5);
408	  }
409	  fixedUpdate(_dt: number, game: GameHooks): void {
410	    const was = this.ai0;
411	    this.ai0 += 1;
412	    if (--this.life <= 0) { this.dead = true; game.onProjectileDeath?.(961, this.x, this.y); return; }
413	    if (was === 0) {
414	      // :48498-48526 首帧：尘爆 + 冰攻音
415	      game.spawnParticles(this.cx, this.cy, '#BFE8FF', 5, 2.2, { life: 24 });
416	      game.playSfxFiles(ICE, 1, this.cx, this.cy);
417	    }
418	    if (was < 10) {          // :48536-48539 生长期 [0,10)：Opacity+0.1,scale=Opacity*ai1
419	      this.opacity = Math.min(1, this.opacity + 0.1);
420	    } else {                 // :48548-48551 收缩期 [10,20)：Opacity-0.2
421	      this.opacity = Math.max(0, this.opacity - 0.2);
422	    }
423	    // 接触伤害（hostile 全窗有效；iframes 由 damagePlayer 节流）
424	    const p = game.player;
425	    if (p && !p.dead && this.opacity > 0.05
426	      && p.x < this.x + this.w && p.x + p.w > this.x && p.y < this.y + this.h && p.y + p.h > this.y) {
427	      game.damagePlayer(this.dmg, this.cx, this.cy);
428	    }
429	    void game.world;
430	  }
431	  scale(): number { return this.opacity * this.ai1; }
432	  draw(r: import('../render/Renderer').Renderer, _cam: import('../render/Camera').Camera): void {
433	    const ctx = r.canvas.getContext('2d');
434	    if (!ctx) return;
435	    const img = r.atlas?.ensureVImage('vanilla/Projectile_961.png');
436	    const s = this.scale();
437	    ctx.save();
438	    ctx.globalAlpha = this.opacity;
439	    ctx.translate(this.cx, this.cy);
440	    // 朝右贴图:原版 rotation = velocity.ToRotation()（:48485）,无 +π/2 偏置——
441	    // 曾 +π/2 把横置冰泪竖过来（G11 旋转模式）。AI 的 scaleY 生长斜坡
442	    // GetLerpValue(30,25,ai0)（Main.cs:31009-31011）在 ai0<=20 即 Kill 的寿命内恒 1,死码
443	    ctx.rotate(this.rot);
444	    ctx.imageSmoothingEnabled = false;
445	    if (img) {
446	      // Frame(1,5)（Main.cs:31004）:贴图 200×240 → 帧格 200×48,× scale=Opacity*ai[1]（:48536）。
447	      // 曾压成 32×32 判定盒（横向 6.25× / 纵向 5× 失真）。origin (16, 24) = (16, 帧高/2)
448	      // （Main.cs:31005）——泪体自锚点向 velocity 方向前伸
449	      const fh = img.height / 5;
450	      ctx.drawImage(img, 0, Math.round(this.frame * fh), img.width, Math.round(fh),
451	        -16 * s, -(fh / 2) * s, img.width * s, fh * s);
452	    } else { ctx.fillStyle = '#9FD8F0'; ctx.fillRect(-16 * s, -16 * s, 32 * s, 32 * s); }
453	    ctx.restore();
454	  }
455	}
456	
457	// ---------------------------------------------------------------------------
458	// 弹幕 962 碎石（aiStyle 1 抛物线 + ai1 = rand(12) 3×4 网格变体;timeLeft 220）
459	// ---------------------------------------------------------------------------
460	export class DeerclopsRubbleProj extends Entity {
461	  w = 32; h = 32;
462	  dead = false;
463	  life = 220;
464	  /** 出世姿态角（:54039 localAI[0]==0 时 rotation = velocity.ToRotation() 一次定型,
465	   *  此后不随当前速度更新——曾每帧重算 atan2(vy,vx)） */
466	  private readonly spawnRot: number;
467	  constructor(x: number, y: number, public vx: number, public vy: number,
468	    private dmg: number, private frame: number) {
469	    super();
470	    this.x = x - this.w / 2; this.y = y - this.h / 2;
471	    this.spawnRot = Math.atan2(vy, vx);
472	  }
473	  fixedUpdate(_dt: number, game: GameHooks): void {
474	    if (--this.life <= 0) { this.dead = true; game.onProjectileDeath?.(962, this.x, this.y); return; }
475	    this.vy = Math.min(this.vy + 0.3, 16);                    // aiStyle 1 重力
476	    this.x += this.vx; this.y += this.vy;                     // tileCollide=false 穿落
477	    const p = game.player;
478	    if (p && !p.dead
479	      && p.x < this.x + this.w && p.x + p.w > this.x && p.y < this.y + this.h && p.y + p.h > this.y) {
480	      game.damagePlayer(this.dmg, this.cx, this.cy);
481	    }
482	  }
483	  draw(r: import('../render/Renderer').Renderer, _cam: import('../render/Camera').Camera): void {
484	    const ctx = r.canvas.getContext('2d');
485	    if (!ctx) return;
486	    const img = r.atlas?.ensureVImage('vanilla/Projectile_962.png');
487	    ctx.save();
488	    ctx.translate(this.cx, this.cy);
489	    ctx.rotate(this.spawnRot);
490	    ctx.imageSmoothingEnabled = false;
491	    if (img) {
492	      // 网格 = Frame(3,4)（Main.cs:32828-32834:projFrames[962]=3 横 × 4 纵,帧格 34×34）;
493	      // frameX = frame%3 / frameY = frame/3。曾按 4 列×3 行（25.5×45.33 非整数格）切片
494	      // 并归一到 32×32 判定盒（纵横比翻转,G11）
495	      const fw = img.width / 3, fh = img.height / 4;
496	      const f = Math.max(0, Math.min(11, this.frame));
497	      ctx.drawImage(img, Math.round((f % 3) * fw), Math.round(Math.floor(f / 3) * fh),
498	        Math.round(fw), Math.round(fh), -fw / 2, -fh / 2, fw, fh);
499	    } else { ctx.fillStyle = '#887860'; ctx.fillRect(-16, -16, 32, 32); }
500	    ctx.restore();
501	  }
502	}
503	
504	// ---------------------------------------------------------------------------
505	// 弹幕 965 敌对影手（AI_187_ShadowHand :39798-39940 + RandomizeInsanityShadowFor
506	// :39703-39796）。ai0 初值 0/180/300/390 直接选定变体段,到段尾即灭（总寿 480t 封顶）
507	// ---------------------------------------------------------------------------
508	export class InsanityShadowProj extends Entity {
509	  w = 40; h = 40;
510	  dead = false;
511	  life = 480;
512	  alpha = 255;              // 255=全透明（SetDefaults）→ 淡入至 50
513	  private ai0: number;
514	  private readonly ai1: number;
515	  private rotation = 0;
516	  constructor(target: { cx: number; cy: number; vx: number } | null, private dmg: number, hint: number) {
517	    super();
518	    // RandomizeInsanityShadowFor 单人近似：玩家环上随机点 + 段直选
519	    const c = target ?? { cx: 0, cy: 0, vx: 0 };
520	    const a = Math.random() * Math.PI * 2;
521	    this.x = c.cx - Math.cos(a) * 200 - this.w / 2;
522	    this.y = c.cy - Math.sin(a) * 200 - this.h / 2;
523	    this.vx = Math.cos(a) * 4;
524	    this.vy = Math.sin(a) * 4;
525	    this.ai0 = [0, 180, 300, 390][hint % 4];
526	    this.ai1 = a;
527	  }
528	  fixedUpdate(_dt: number, game: GameHooks): void {
529	    this.ai0 += 1;
530	    // 变体段（:39903-39940）
531	    let variation = 0, start = 0, len = 180;
532	    if (this.ai0 >= 390) { variation = 3; start = 390; len = 90; }
533	    else if (this.ai0 >= 300) { variation = 2; start = 300; len = 90; }
534	    else if (this.ai0 >= 180) { variation = 1; start = 180; len = 120; }
535	    const fc = this.ai0 - start;
536	    // :39825-39841 alpha：段尾 15t 淡出至 255,否则淡入至 50
537	    if (fc > len - 15) this.alpha = Math.min(255, this.alpha + 25);
538	    else this.alpha = Math.max(50, this.alpha - 25);
539	    if (fc >= len - 1 || --this.life <= 0) {
540	      this.dead = true;
541	      game.onProjectileDeath?.(965, this.x, this.y);
542	      return;
543	    }
544	    if (variation === 0) {                       // :39847-39856 减速滑行
545	      this.vx *= 0.98; this.vy *= 0.98;
546	      this.rotation = Math.atan2(this.vy, this.vx) + (this.vx < 0 ? Math.PI : 0);
547	    } else if (variation === 1) {                // :39857-39874 绕轴摆荡
548	      const t = fc / len;
549	      if (Math.hypot(this.vx, this.vy) > 0.1) { this.vx *= 0.95; this.vy *= 0.95; }
550	      const pivotD = 70 * (this.vx >= 0 ? 1 : -1);
551	      const a1 = remap(t, 0.3, 0.5, 0, 1) * remap(t, 0.45, 0.5, 1, 0);
552	      const a2 = remap(t, 0.5, 0.55, 0, 1) * remap(t, 0.5, 1, 1, 0);
553	      this.rotation += (a1 * (Math.PI / 60) + a2 * (-Math.PI * 8 / 60)) * -(this.vx >= 0 ? 1 : -1);
554	      const px = this.cx - Math.cos(this.rotation) * pivotD;
555	      const py = this.cy - Math.sin(this.rotation) * pivotD;
556	      this.x = px + Math.cos(this.rotation) * pivotD - this.w / 2;
557	      this.y = py + Math.sin(this.rotation) * pivotD - this.h / 2;
558	    } else if (variation === 2) {                // :39875-39888 俯冲（0.4 处峰值速）
559	      const t = fc / len;
560	      const v1 = remap(t, 0, 0.4, 1, 0);
561	      const v2 = remap(t, 0.3, 0.4, 0, 1) * remap(t, 0.4, 1, 1, 0);
562	      const spd = v1 * 2 + v2 * 8 + 0.01;
563	      this.vx = Math.cos(this.ai1) * spd;
564	      this.vy = Math.sin(this.ai1) * spd;
565	      this.rotation = Math.atan2(this.vy, this.vx) + (this.vx < 0 ? Math.PI : 0);
566	    } else {                                     // :39889-39899 旋进
567	      const w = this.ai1;
568	      const cos = Math.cos(w), sin = Math.sin(w);
569	      const nvx = this.vx * cos - this.vy * sin;
570	      const nvy = this.vx * sin + this.vy * cos;
571	      this.vx = nvx; this.vy = nvy;
572	      this.rotation = Math.atan2(this.vy, this.vx) + (this.vx < 0 ? Math.PI : 0);
573	    }
574	    const p = game.player;
575	    if (p && !p.dead && this.alpha < 250
576	      && p.x < this.x + this.w && p.x + p.w > this.x && p.y < this.y + this.h && p.y + p.h > this.y) {
577	      game.damagePlayer(this.dmg, this.cx, this.cy);
578	    }
579	  }
580	  draw(r: import('../render/Renderer').Renderer, _cam: import('../render/Camera').Camera): void {
581	    const ctx = r.canvas.getContext('2d');
582	    if (!ctx) return;
583	    const img = r.atlas?.ensureVImage('vanilla/Projectile_965.png');
584	    ctx.save();
585	    ctx.globalAlpha = 1 - this.alpha / 255;
586	    ctx.translate(this.cx, this.cy);
587	    // 原版:rotation = ToRotation(+π 向左) 且 dir=FlipHorizontally（AI_187 :39850-39857
588	    // 等:velocity.X<0 → spriteDirection=-1 + rotation += π）——两变换叠加,曾漏镜像。
589	    // 未单独登记的 vanilla 视觉层（登记偏差）:4 尾影幽灵拷贝 + Black×Opacity 剪影着色
590	    // （Main.cs:30747-30757/:30793-30796）
591	    ctx.rotate(this.rotation);
592	    if (this.vx < 0) ctx.scale(-1, 1);
593	    ctx.imageSmoothingEnabled = false;
594	    if (img) {
595	      // 原生 80×84 × scale=1（SetDefaults 965 无 scale;曾归一 40×40 判定盒 → 整体减半）。
596	      // origin（Main.cs:29934-29937）:X = spriteDirection==1 ? W-20 : 20,Y = H/2——腕部锚点
597	      const ox = this.vx >= 0 ? img.width - 20 : 20;
598	      const oy = img.height / 2;
599	      ctx.drawImage(img, -ox, -oy, img.width, img.height);
600	    } else { ctx.fillStyle = '#6020B0'; ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI * 2); ctx.fill(); }
601	    ctx.restore();
602	  }
603	}
604	
605	function remap(x: number, a: number, b: number, c: number, d: number): number {
606	  if (x < a) return c;
607	  if (x > b) return d;
608	  return c + (d - c) * ((x - a) / (b - a));
609	}
610	
611	/** 弹幕入桶（与 duke 系同款：hostile 类自管运动,dead 由桶清理） */
612	function addProj(game: GameHooks, p: Entity): void {
613	  (game as unknown as { entities: { add(e: Entity, bucket: string): void } })
614	    .entities.add(p, 'projectiles');
615	}
616	

```


---

## 🤖 Assistant · 2026-08-19T03:09:53.707Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the vanilla NPC.cs sections. Let me start with the Golem body AI_045 @19447-19760 (or 19447-19722 as claimed). Let me read generously: 19440-19770.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:54.053Z · glm-x-preview-260804

```
我方文件已读。现在读原版 NPC.cs 对应段，先 Golem 本体 AI_045。
```


---

## 🤖 Assistant · 2026-08-19T03:09:54.625Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '19440,19770p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read Golem body AI_045 section from NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:54.666Z

**📎 ToolResult**

```
			if (type == 247)
			{
				rotation = (float)Math.Atan2(0f - velocity.Y, 0f - velocity.X);
			}
		}
	}

	private void AI_045_Golem()
	{
		golemBoss = whoAmI;
		float num = GetMyBalance();
		if (Main.getGoodWorld)
		{
			num += 2f;
		}
		if ((!Main.player[target].ZoneLihzhardTemple && !Main.player[target].ZoneJungle) || (double)Main.player[target].Center.Y < Main.worldSurface * 16.0)
		{
			num *= 2f;
		}
		if (localAI[0] == 0f)
		{
			localAI[0] = 1f;
			if (Main.netMode != 1)
			{
				NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X - 84, (int)base.Center.Y - 9, 247);
				NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X + 78, (int)base.Center.Y - 9, 248);
				NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X - 3, (int)base.Center.Y - 57, 246);
			}
		}
		if (target >= 0 && Main.player[target].dead)
		{
			TargetClosest();
			if (Main.player[target].dead)
			{
				noTileCollide = true;
			}
		}
		if (alpha > 0)
		{
			alpha -= 10;
			if (alpha < 0)
			{
				alpha = 0;
			}
			ai[1] = 0f;
		}
		bool flag = false;
		bool flag2 = false;
		bool flag3 = false;
		dontTakeDamage = false;
		for (int i = 0; i < Main.maxNPCs; i++)
		{
			NPC nPC = Main.npc[i];
			if (nPC.active)
			{
				switch (nPC.type)
				{
				case 246:
					flag = true;
					break;
				case 247:
					flag2 = true;
					break;
				case 248:
					flag3 = true;
					break;
				}
			}
		}
		dontTakeDamage = flag;
		if (Main.netMode != 1 && Main.getGoodWorld && velocity.Y > 0f)
		{
			for (int j = (int)(position.X / 16f); (float)j < (position.X + (float)width) / 16f; j++)
			{
				for (int k = (int)(position.Y / 16f); (float)k < (position.Y + (float)width) / 16f; k++)
				{
					Tile tile = Main.tile[j, k];
					if (tile != null && tile.active() && TileID.Sets.Torches[tile.type])
					{
						Main.tile[j, k].active(active: false);
						if (Main.netMode == 2)
						{
							NetMessage.SendTileSquare(-1, j, k);
						}
					}
				}
			}
		}
		position += netOffset;
		if (!Main.getGoodWorld)
		{
			if (!flag2)
			{
				int num2 = Dust.NewDust(new Vector2(base.Center.X - 80f * scale, base.Center.Y - 9f), 8, 8, 31, 0f, 0f, 100);
				Main.dust[num2].alpha += Main.rand.Next(100);
				Main.dust[num2].velocity *= 0.2f;
				Main.dust[num2].velocity.Y -= 0.5f + (float)Main.rand.Next(10) * 0.1f;
				Main.dust[num2].fadeIn = 0.5f + (float)Main.rand.Next(10) * 0.1f;
				if (Main.rand.Next(10) == 0)
				{
					num2 = Dust.NewDust(new Vector2(base.Center.X - 80f * scale, base.Center.Y - 9f), 8, 8, 6);
					if (Main.rand.Next(20) != 0)
					{
						Main.dust[num2].noGravity = true;
						Main.dust[num2].scale *= 1f + (float)Main.rand.Next(10) * 0.1f;
						Main.dust[num2].velocity.Y -= 1f;
					}
				}
			}
			if (!flag3)
			{
				int num3 = Dust.NewDust(new Vector2(base.Center.X + 62f * scale, base.Center.Y - 9f), 8, 8, 31, 0f, 0f, 100);
				Main.dust[num3].alpha += Main.rand.Next(100);
				Main.dust[num3].velocity *= 0.2f;
				Main.dust[num3].velocity.Y -= 0.5f + (float)Main.rand.Next(10) * 0.1f;
				Main.dust[num3].fadeIn = 0.5f + (float)Main.rand.Next(10) * 0.1f;
				if (Main.rand.Next(10) == 0)
				{
					num3 = Dust.NewDust(new Vector2(base.Center.X + 62f * scale, base.Center.Y - 9f), 8, 8, 6);
					if (Main.rand.Next(20) != 0)
					{
						Main.dust[num3].noGravity = true;
						Main.dust[num3].scale *= 1f + (float)Main.rand.Next(10) * 0.1f;
						Main.dust[num3].velocity.Y -= 1f;
					}
				}
			}
		}
		position -= netOffset;
		if (noTileCollide && !Main.player[target].dead)
		{
			if (velocity.Y > 0f && base.Bottom.Y > Main.player[target].Top.Y)
			{
				noTileCollide = false;
			}
			else if (Collision.CanHit(position, width, height, Main.player[target].Center, 1, 1) && !Collision.SolidTiles(position, width, height))
			{
				noTileCollide = false;
			}
		}
		if (ai[0] == 0f)
		{
			if (velocity.Y == 0f)
			{
				velocity.X *= 0.8f;
				float num4 = 1f;
				if (ai[1] > 0f)
				{
					if (!flag2)
					{
						num4 += 2f;
					}
					if (!flag3)
					{
						num4 += 2f;
					}
					if (!flag)
					{
						num4 += 2f;
					}
					if (life < lifeMax)
					{
						num4 += 1f;
					}
					if (life < lifeMax / 2)
					{
						num4 += 4f;
					}
					if (life < lifeMax / 3)
					{
						num4 += 8f;
					}
					num4 *= num;
					if (Main.getGoodWorld)
					{
						num4 += 100f;
					}
				}
				ai[1] += num4;
				if (ai[1] >= 300f)
				{
					ai[1] = -20f;
					frameCounter = 0.0;
				}
				else if (ai[1] == -1f)
				{
					noTileCollide = true;
					TargetClosest();
					velocity.X = 4 * direction;
					if (life < lifeMax)
					{
						velocity.Y = -12.1f * (num + 9f) / 10f;
						if ((double)velocity.Y < -19.1)
						{
							velocity.Y = -19.1f;
						}
					}
					else
					{
						velocity.Y = -12.1f;
					}
					ai[0] = 1f;
					ai[1] = 0f;
				}
			}
		}
		else if (ai[0] == 1f)
		{
			if (velocity.Y == 0f)
			{
				SoundEngine.PlaySound(SoundID.Item14, position);
				ai[0] = 0f;
				for (int l = (int)position.X - 20; l < (int)position.X + width + 40; l += 20)
				{
					for (int m = 0; m < 4; m++)
					{
						int num5 = Dust.NewDust(new Vector2(position.X - 20f, position.Y + (float)height), width + 20, 4, 31, 0f, 0f, 100, default(Color), 1.5f);
						Main.dust[num5].velocity *= 0.2f;
					}
					int num6 = Gore.NewGore(new Vector2(l - 20, position.Y + (float)height - 8f), default(Vector2), Main.rand.Next(61, 64));
					Main.gore[num6].velocity *= 0.4f;
				}
			}
			else
			{
				TargetClosest();
				if (position.X < Main.player[target].position.X && position.X + (float)width > Main.player[target].position.X + (float)Main.player[target].width)
				{
					velocity.X *= 0.9f;
					if (base.Bottom.Y < Main.player[target].position.Y)
					{
						velocity.Y += 0.2f * (num + 1f) / 2f;
					}
				}
				else
				{
					if (direction < 0)
					{
						velocity.X -= 0.2f;
					}
					else if (direction > 0)
					{
						velocity.X += 0.2f;
					}
					float num7 = 3f;
					if (life < lifeMax)
					{
						num7 += 1f;
					}
					if (life < lifeMax / 2)
					{
						num7 += 1f;
					}
					if (life < lifeMax / 4)
					{
						num7 += 1f;
					}
					num7 *= (num + 1f) / 2f;
					if (velocity.X < 0f - num7)
					{
						velocity.X = 0f - num7;
					}
					if (velocity.X > num7)
					{
						velocity.X = num7;
					}
				}
			}
		}
		if (target <= 0 || target == 255 || Main.player[target].dead)
		{
			TargetClosest();
		}
		int num8 = 3000;
		if (Math.Abs(base.Center.X - Main.player[target].Center.X) + Math.Abs(base.Center.Y - Main.player[target].Center.Y) > (float)num8)
		{
			TargetClosest();
			if (Math.Abs(base.Center.X - Main.player[target].Center.X) + Math.Abs(base.Center.Y - Main.player[target].Center.Y) > (float)num8)
			{
				active = false;
			}
		}
	}

	public static bool SpawnMechQueen(int onWhichPlayer)
	{
		if (AnyNPCs(127) || AnyNPCs(134) || AnyNPCs(125) || AnyNPCs(126))
		{
			return false;
		}
		if (!SpecialSeedFeatures.Mechdusa)
		{
			return false;
		}
		if (Main.netMode == 1)
		{
			NetMessage.SendData(61, -1, -1, null, onWhichPlayer, -16f);
		}
		else
		{
			mechQueen = -2;
			SpawnOnPlayer(onWhichPlayer, 127);
			mechQueen = FindFirstNPC(127);
			NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 125, 1);
			NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 126, 1);
			int num = NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 134, 1);
			NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 139, 1, 0f, 0f, num, -1f);
			NewNPC(GetBossSpawnSource(onWhichPlayer), (int)Main.npc[mechQueen].Center.X, (int)Main.npc[mechQueen].Center.Y, 139, 1, 0f, 0f, num, 1f);
		}
		return true;
	}

	public bool IsCritterThatIsHostileToPlayers()
	{
		if (type >= 0 && NPCID.Sets.CritterThatCanTurnOnPlayers[type])
		{
			return aiStyle == 3;
		}
		return false;
	}

	public void AI()
	{
		//IL_50cf9: Unknown result type (might be due to invalid IL or missing references)
		//IL_50ac3: Unknown result type (might be due to invalid IL or missing references)
		//IL_50ad0: Unknown result type (might be due to invalid IL or missing references)
		//IL_50ad5: Unknown result type (might be due to invalid IL or missing references)
		//IL_4fefc: Unknown result type (might be due to invalid IL or missing references)
		//IL_50d54: Unknown result type (might be due to invalid IL or missing references)
		//IL_50d35: Unknown result type (might be due to invalid IL or missing references)
		//IL_50d3a: Unknown result type (might be due to invalid IL or missing references)

```


---

## 🤖 Assistant · 2026-08-19T03:09:55.620Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '19165,19450p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read GolemFist AI_047 section from NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:55.665Z

**📎 ToolResult**

```
			}
			Projectile.NewProjectile(new EntitySource_DebugCommand(), vector3 + vector2, Vector2.Zero, 995, 0, 0f, Main.myPlayer);
			break;
		}
	}

	private void AI_047_GolemFist()
	{
		float num = GetMyBalance();
		if (Main.getGoodWorld)
		{
			num += 3f;
		}
		if ((!Main.player[target].ZoneLihzhardTemple && !Main.player[target].ZoneJungle) || (double)Main.player[target].Center.Y < Main.worldSurface * 16.0)
		{
			num *= 2f;
		}
		if (golemBoss < 0)
		{
			StrikeNPCNoInteraction(9999, 0f, 0);
			return;
		}
		if (alpha > 0)
		{
			alpha -= 10;
			if (alpha < 0)
			{
				alpha = 0;
			}
			ai[1] = 0f;
		}
		Player player = Main.player[target];
		NPC nPC = Main.npc[golemBoss];
		Vector2 vector = nPC.Center + nPC.velocity + new Vector2(0f, -9f * scale);
		vector.X += (float)((type == 247) ? (-84) : 78) * scale;
		Vector2 vector2 = vector - base.Center;
		float num2 = vector2.Length();
		if (ai[0] == 0f)
		{
			noTileCollide = true;
			float num3 = 14f;
			if (life < lifeMax / 2)
			{
				num3 += 3f;
			}
			if (life < lifeMax / 4)
			{
				num3 += 3f;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
			{
				num3 += 8f;
			}
			num3 *= (num + 3f) / 4f;
			if (num3 > 32f)
			{
				num3 = 32f;
			}
			float x = vector2.X;
			float y = vector2.Y;
			float num4 = num2;
			if (num4 < 12f + num3)
			{
				rotation = 0f;
				velocity.X = x;
				velocity.Y = y;
				float num5 = num;
				ai[1] += num5;
				if (life < lifeMax / 2)
				{
					ai[1] += num5;
				}
				if (life < lifeMax / 4)
				{
					ai[1] += num5;
				}
				if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
				{
					ai[1] += 10f * num5;
				}
				if (ai[1] >= 60f)
				{
					TargetClosest();
					if ((type == 247 && base.Center.X + 100f > Main.player[target].Center.X) || (type == 248 && base.Center.X - 100f < Main.player[target].Center.X))
					{
						ai[1] = 0f;
						ai[0] = 1f;
					}
					else
					{
						ai[1] = 0f;
					}
				}
			}
			else
			{
				num4 = num3 / num4;
				velocity.X = x * num4;
				velocity.Y = y * num4;
				rotation = (float)Math.Atan2(0f - velocity.Y, 0f - velocity.X);
				if (type == 247)
				{
					rotation = (float)Math.Atan2(velocity.Y, velocity.X);
				}
			}
		}
		else if (ai[0] == 1f)
		{
			ai[1] += 1f;
			base.Center = vector;
			rotation = 0f;
			velocity = Vector2.Zero;
			if (ai[1] <= 15f)
			{
				for (int i = 0; i < 1; i++)
				{
					Vector2 vector3 = Main.rand.NextVector2Circular(80f, 80f);
					Vector2 vector4 = vector3 * -1f * 0.05f;
					Vector2 vector5 = Main.rand.NextVector2Circular(20f, 20f);
					Dust dust = Dust.NewDustPerfect(base.Center + vector4 + vector3 + vector5, 228, vector4);
					dust.fadeIn = 1.5f;
					dust.scale = 0.5f;
					if (Main.getGoodWorld)
					{
						dust.noLight = true;
					}
					dust.noGravity = true;
				}
			}
			if (ai[1] >= 30f)
			{
				noTileCollide = true;
				collideX = false;
				collideY = false;
				ai[0] = 2f;
				ai[1] = 0f;
				float num6 = 12f;
				if (life < lifeMax / 2)
				{
					num6 += 4f;
				}
				if (life < lifeMax / 4)
				{
					num6 += 4f;
				}
				if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
				{
					num6 += 10f;
				}
				num6 *= (num + 3f) / 4f;
				if (num6 > 48f)
				{
					num6 = 48f;
				}
				Vector2 vector6 = new Vector2(base.Center.X, base.Center.Y);
				float num7 = Main.player[target].Center.X - vector6.X;
				float num8 = Main.player[target].Center.Y - vector6.Y;
				float num9 = (float)Math.Sqrt(num7 * num7 + num8 * num8);
				num9 = num6 / num9;
				velocity.X = num7 * num9;
				velocity.Y = num8 * num9;
				rotation = (float)Math.Atan2(velocity.Y, velocity.X);
				if (type == 247)
				{
					rotation = (float)Math.Atan2(0f - velocity.Y, 0f - velocity.X);
				}
			}
		}
		else if (ai[0] == 2f)
		{
			if (Main.netMode != 1 && Main.getGoodWorld)
			{
				for (int j = (int)(position.X / 16f) - 1; (float)j < (position.X + (float)width) / 16f + 1f; j++)
				{
					for (int k = (int)(position.Y / 16f) - 1; (float)k < (position.Y + (float)width) / 16f + 1f; k++)
					{
						Tile tile = Main.tile[j, k];
						if (tile != null && tile.active() && TileID.Sets.Torches[tile.type])
						{
							Main.tile[j, k].active(active: false);
							if (Main.netMode == 2)
							{
								NetMessage.SendTileSquare(-1, j, k);
							}
						}
					}
				}
			}
			ai[1] += 1f;
			if (ai[1] == 1f)
			{
				SoundEngine.PlaySound(SoundID.Item14, position);
			}
			if (Main.rand.Next(2) == 0)
			{
				Vector2 vector7 = velocity * 0.5f;
				Vector2 vector8 = Main.rand.NextVector2Circular(20f, 20f);
				Dust.NewDustPerfect(base.Center + vector7 + vector8, 306, vector7, 0, Main.OurFavoriteColor).scale = 2f;
			}
			if (Math.Abs(velocity.X) > Math.Abs(velocity.Y))
			{
				if (velocity.X > 0f && base.Center.X > player.Center.X)
				{
					noTileCollide = false;
				}
				if (velocity.X < 0f && base.Center.X < player.Center.X)
				{
					noTileCollide = false;
				}
			}
			else
			{
				if (velocity.Y > 0f && base.Center.Y > player.Center.Y)
				{
					noTileCollide = false;
				}
				if (velocity.Y < 0f && base.Center.Y < player.Center.Y)
				{
					noTileCollide = false;
				}
			}
			if (num2 > 700f || collideX || collideY)
			{
				noTileCollide = true;
				ai[0] = 0f;
			}
		}
		else
		{
			if (ai[0] != 3f)
			{
				return;
			}
			noTileCollide = true;
			float num10 = 0.4f;
			Vector2 vector9 = new Vector2(base.Center.X, base.Center.Y);
			float num11 = Main.player[target].Center.X - vector9.X;
			float num12 = Main.player[target].Center.Y - vector9.Y;
			float num13 = (float)Math.Sqrt(num11 * num11 + num12 * num12);
			num13 = 12f / num13;
			num11 *= num13;
			num12 *= num13;
			if (velocity.X < num11)
			{
				velocity.X += num10;
				if (velocity.X < 0f && num11 > 0f)
				{
					velocity.X += num10 * 2f;
				}
			}
			else if (velocity.X > num11)
			{
				velocity.X -= num10;
				if (velocity.X > 0f && num11 < 0f)
				{
					velocity.X -= num10 * 2f;
				}
			}
			if (velocity.Y < num12)
			{
				velocity.Y += num10;
				if (velocity.Y < 0f && num12 > 0f)
				{
					velocity.Y += num10 * 2f;
				}
			}
			else if (velocity.Y > num12)
			{
				velocity.Y -= num10;
				if (velocity.Y > 0f && num12 < 0f)
				{
					velocity.Y -= num10 * 2f;
				}
			}
			rotation = (float)Math.Atan2(velocity.Y, velocity.X);
			if (type == 247)
			{
				rotation = (float)Math.Atan2(0f - velocity.Y, 0f - velocity.X);
			}
		}
	}

	private void AI_045_Golem()
	{
		golemBoss = whoAmI;
		float num = GetMyBalance();

```


---

## 🤖 Assistant · 2026-08-19T03:10:44.624Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me analyze the Golem body AI comparison.

Vanilla AI_045_Golem:
1. golemBoss = whoAmI
2. num = GetMyBalance(); getGoodWorld → +2; temple/jungle/above-surface logic ×2
3. localAI[0]==0 → spawn 247/248/246
4. target dead → TargetClosest; if still dead → noTileCollide = true
5. alpha -= 10, ai[1] = 0
6. flag/flag2/flag3 scan; dontTakeDamage = flag
7. getGoodWorld torch smash
8. dust for missing fists (not getGoodWorld)
9. noTileCollide release logic: velocity.Y > 0 && Bottom.Y > player.Top.Y → false; else CanHit + !SolidTiles → false
10. ai[0]==0: if vy==0: vx*=0.8; num4 logic; ai[1] += num4; >=300 → -20; ==-1 → jump
11. ai[0]==1: vy==0 → sound + dust; else targetclosest, if overlapping X → vx *= 0.9 and if Bottom.Y < player.position.Y → vy += 0.2*(num+1)/2; else direction accel ±0.2, num7 clamp
12. despawn: target<=0...dead → TargetClosest; then 3000 manhattan check, double check → active=false.

Our version:
- Line 333-357: ai0==0 branch. `if (player && e.ai0 === 0)`. Then `if (e.vy === 0)`. vx *= 0.8; num4... matches. One thing: vanilla jump condition: `ai[1] == -1f` — our `else if (e.ai1 === -1)`. OK. Note vanilla checks `ai[1] >= 300 → -20` FIRST then `else if ai[1] == -1`. Ours matches order. In vanilla, once ai[1] = -20, next ticks decrement by num4=1 (since ai[1] > 0 is false during negative → num4 stays 1). Ours: `if (e.ai1 > 0)` gate on the boosts — correct.

Wait — during crouch (negative) num4 = 1 in ours since `e.ai1 > 0` false → num4 stays 1. Yes.

- Jump: vx = 4*dir; vy = ... matches. TargetClosest in vanilla sets direction; ours uses player.cx sign. Fine approximation.

- ai0==1 branch: ours matches: on land sound + dust; else if overlapping X: vx *= 0.9; if (e.y + e.h < player.y) vy += 0.2*(num+1)/2. Vanilla: `base.Bottom.Y < Main.player[target].position.Y` — position.Y is player's top. Ours uses player.y. Match.

Else branch: `e.vx += 0.2 * dir` vs vanilla direction-based ±0.2. Match. num7 clamp logic: ours clamp(-num7, num7) matches.

- Despawn: vanilla checks `target <= 0 || target == 255 || dead → TargetClosest` then 3000 check twice with TargetClosest in between; active = false. Ours: if !player → noTC = true... wait vanilla's "player dead" handling at 19469-19475: TargetClosest; if still dead → noTileCollide = true. Ours line 386-391: `if (!player) { x.noTC = true; }` — !player is not the same as player dead. If player exists but dead, ours doesn't set noTC=true and doesn't despawn via the 3000 check (it computes distance to dead player). Hmm, but `player` param — depends on the caller's semantics. If the caller passes null when dead... uncertain. This is a candidate "存疑" item. Actually let me check: the caller might pass p only if alive. Let me check how golemAI is invoked. I'll grep for golemAI call site.

Also one important thing: vanilla's despawn check happens regardless of ai state; ours happens after AI branches (fine). But ours: `!player` → noTC = true only; vanilla player dead → noTileCollide = true AND then the 3000 check uses TargetClosest result (may target another player). In single-player, TargetClosest with a dead player... Actually TargetClosest would find nearest player; if the only player is dead, target stays but the NPC continues. Vanilla: `if (target >= 0 && Main.player[target].dead) { TargetClosest(); if (dead) noTileCollide = true; }`. So the body becomes noTileCollide but does NOT despawn while player dead... then the 3000 check: dead player still within 3000 usually → stays. So vanilla golem does NOT despawn on player death; it just phases through tiles. Ours: !player → noTC = true. If the harness passes null for dead player, then equivalent-ish. But if harness passes the dead player object, ours would keep chasing/attacking a dead player and even despawn at 3000 (dead player stays at death location, distance < 3000 typically → no despawn). Minor. Need to check the call convention. Let me check bossAI.ts for how player is passed.

- HitEffect for 245: In vanilla, when golem body dies (checkDead), what happens? Let me check HitEffect :85842-85847 and checkDead for 245. Also the claim "本体血尽 → 死亡演出 60t 后真死" — vanilla: golem body life reaches 0 → since dontTakeDamage was only while head alive... Actually in vanilla, once head is killed (246 → spawns 249), body becomes damageable; killing body → normal death (checkDead → NPCLoot → downedGolemBoss). The head 249 continues fighting?? In vanilla, when body 245 dies, does head 249 remain? Yes! In vanilla Terraria, if you kill the body after the head is off... Actually the classic strategy: kill head first (spawns free head), then body is vulnerable. If body dies while free head alive — in vanilla the free head remains and you must kill it. Actually I recall in vanilla, killing the body while the head is detached does NOT end the fight; the head remains. And head 249's AI references golemBoss... 249 doesn't anchor to body. Fist anchors golemBoss — if body died, golemBoss index → inactive NPC... The fist checks `if (golemBoss < 0) strike`. golemBoss is a static set by AI_045 each tick while body alive; when body inactive, golemBoss stays stale? There's code somewhere resetting. Not critical.

Our death chain: body hp<=0 → dying 60t → dead. During dying, ai3=1 and hp reset to max. Head attached → free when body.ai3===1. That means: killing the BODY (while head still attached) also detaches head — in vanilla, killing body while head attached... can't happen since body is invulnerable (dontTakeDamage = flag) while head alive. Wait — dontTakeDamage only set true while 246 active. But what if head 246 dies → NewNPC 249 → body becomes vulnerable. OK.

But hold on: in vanilla, 246 dying spawns 249 with full life. Our golemHeadGoFree sets hp = maxHp. But it uses e.maxHp of 246! 246 lifeMax vs 249 lifeMax. In vanilla, NewNPC 249 gets its own SetDefaults lifeMax. 246 SetDefaults lifeMax vs 249 lifeMax — likely the same (both 6739? scaled by expert). Hmm: 246 GolemHead lifeMax and 249 GolemHeadFree... Let me check SetDefaults :12095-12149. I'll read that range.

Also `e.hp = e.maxHp` — if 246's maxHp equals 249's maxHp, fine. Let me check.

Now the fist: vanilla AI_047.
- num = GetMyBalance; getGoodWorld +3 — ours matches (ftwBonus 3).
- golemBoss < 0 → StrikeNPCNoInteraction(9999) → dies. Ours: anchor null → dead. OK.
- alpha fade → ai[1] = 0. Ours matches.
- vector = npc.Center + npc.velocity + (0, -9*scale); vector.X += (247 ? -84 : 78)*scale. Ours matches.
- ai[0]==0: noTileCollide=true; num3 = 14 + boosts ×(num+3)/4 clamp 32 — matches. If num2 < 12+num3: rotation=0; velocity = (x,y); ai[1] += num; boosts; if ai[1]>=60: TargetClosest; side gate; ai[0]=1. Ours matches (sideOk formula: isLeft ? e.cx + 100 > player.cx : e.cx - 100 < player.cx). Vanilla: (type==247 && Center.X + 100 > player.Center.X) || (type==248 && Center.X - 100 < player.Center.X). Match.
- else: velocity = (x,y)*num3/num2; rotation = atan2(-vy,-vx); if 247 → atan2(vy,vx). Ours: `e.spin = isLeft ? Math.atan2(e.vy, e.vx) : Math.atan2(-e.vy, -e.vx);` — isLeft means type 247. Vanilla: default atan2(-vy,-vx), then if 247 override atan2(vy,vx). Ours: isLeft(247) → atan2(vy,vx); else (248) → atan2(-vy,-vx). Match.
- ai[0]==1: ai[1]+=1; Center = vector; rotation=0; velocity=Zero; dust if <=15; if >=30: noTC=true, collideX=false, collideY=false, ai[0]=2, ai[1]=0; num6 = 12 + boosts ×(num+3)/4 clamp 48; velocity = direction*num6; rotation = atan2(vy,vx); if 247 → atan2(-vy,-vx). Ours matches. Note `e.x = tx - e.w / 2; e.y = ty - e.h / 2;` — Center = vector. Match.
- ai[0]==2: torch smash; ai[1]+=1; if ==1 sound; rand dust; axis pass checks; if num2 > 700 || collideX || collideY → noTC=true, ai[0]=0. Ours: after movement, `if (x.state === 2 && !x.noTC && hitSolid) { noTC=true; state=0 }` and `if (dist > 700) { noTC = true; state = 0; }`. Vanilla checks `num2 > 700 || collideX || collideY` — collideX/collideY are set by the collision system when the fist hits a wall (after movement, with noTileCollide=false). Ours approximates with hitSolid after movement. Reasonable. But note: ours checks dist > 700 inside state===2 branch BEFORE movement (dist computed from pre-movement position). Vanilla num2 is also computed pre-movement (at top). Both pre-movement. OK.

Wait, one subtlety: in vanilla, the ai[0]==2 branch checks num2 which was computed at the top of AI this tick (pre-movement). Ours also uses dist computed before the state machine. Match.

- ai[0]==3 (else branch): vanilla: `if (ai[0] != 3f) return;` then noTC=true, accelerate toward player at 12 speed with 0.4 steps and double-step boost. Ours state===3: uses accelTo(e.vx, target*12, 0.4) — approximate but doesn't have the "extra boost when opposite signs" (velocity.X += num10*2). accelTo is a helper in bossAI.ts; need to check its semantics. Minor numeric.

But wait — is state 3 ever reached? Vanilla ai[0]=3 is never set anywhere in AI_047 (dead code in vanilla too? Actually golem fist ai[0]=3... I don't think vanilla ever sets 3). Ours also never sets state 3. Fine.

Now the head aiStyle 46 @31273-31499 and 48 @31500-31741. Let me read those.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:45.168Z · glm-x-preview-260804

```
Golem 本体与拳的原版段已核对。现在读挂载头 aiStyle 46 与自由头 aiStyle 48 段。
```


---

## 🤖 Assistant · 2026-08-19T03:10:45.681Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '31265,31500p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read Golem head aiStyle 46 section"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:45.714Z

**📎 ToolResult**

```
					velocity.Y = -4f;
				}
			}
		}
		else if (aiStyle == 45)
		{
			AI_045_Golem();
		}
		else if (aiStyle == 46)
		{
			float num720 = GetMyBalance();
			if (Main.getGoodWorld)
			{
				num720 += 3f;
			}
			if ((!Main.player[target].ZoneLihzhardTemple && !Main.player[target].ZoneJungle) || (double)Main.player[target].Center.Y < Main.worldSurface * 16.0)
			{
				num720 *= 2f;
			}
			noTileCollide = true;
			if (golemBoss < 0)
			{
				StrikeNPCNoInteraction(9999, 0f, 0);
				return;
			}
			float num721 = 100f;
			Vector2 vector83 = new Vector2(base.Center.X, base.Center.Y);
			float num722 = Main.npc[golemBoss].Center.X - vector83.X;
			float num723 = Main.npc[golemBoss].Center.Y - vector83.Y;
			num723 -= 57f * scale;
			num722 -= 3f * scale;
			float num724 = (float)Math.Sqrt(num722 * num722 + num723 * num723);
			if (num724 < num721)
			{
				rotation = 0f;
				velocity.X = num722;
				velocity.Y = num723;
			}
			else
			{
				num724 = num721 / num724;
				velocity.X = num722 * num724;
				velocity.Y = num723 * num724;
				rotation = velocity.X * 0.1f;
			}
			if (alpha > 0)
			{
				alpha -= 10;
				if (alpha < 0)
				{
					alpha = 0;
				}
				this.ai[1] = 30f;
			}
			if (this.ai[0] == 0f)
			{
				this.ai[1] += 1f;
				int num725 = 300;
				if (this.ai[1] < 20f || this.ai[1] > (float)(num725 - 20))
				{
					this.ai[1] += 2f * (num720 - 1f) / 3f;
					localAI[0] = 1f;
				}
				else
				{
					this.ai[1] += 1f * (num720 - 1f) / 2f;
					localAI[0] = 0f;
				}
				if (this.ai[1] >= (float)num725)
				{
					TargetClosest();
					this.ai[1] = 0f;
					Vector2 vector84 = new Vector2(base.Center.X, base.Center.Y + 10f * scale);
					float num726 = 8f;
					float num727 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector84.X;
					float num728 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector84.Y;
					float num729 = (float)Math.Sqrt(num727 * num727 + num728 * num728);
					num729 = num726 / num729;
					num727 *= num729;
					num728 *= num729;
					int num730 = 18;
					int num731 = 258;
					if (Main.netMode != 1)
					{
						int num732 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector84.X, vector84.Y, num727, num728, num731, num730, 0f, Main.myPlayer);
					}
				}
			}
			else if (this.ai[0] == 1f)
			{
				TargetClosest();
				Vector2 vector85 = new Vector2(base.Center.X, base.Center.Y + 10f * scale);
				if (Main.player[target].Center.X < base.Center.X - (float)width)
				{
					localAI[1] = -1f;
					vector85.X -= 40f * scale;
				}
				else if (Main.player[target].Center.X > base.Center.X + (float)width)
				{
					localAI[1] = 1f;
					vector85.X += 40f * scale;
				}
				else
				{
					localAI[1] = 0f;
				}
				float num733 = (num720 + 3f) / 4f;
				this.ai[1] += num733;
				if ((double)life < (double)lifeMax * 0.4)
				{
					this.ai[1] += num733;
				}
				if ((double)life < (double)lifeMax * 0.2)
				{
					this.ai[1] += num733;
				}
				int num734 = 300;
				if (this.ai[1] < 20f || this.ai[1] > (float)(num734 - 20))
				{
					localAI[0] = 1f;
				}
				else
				{
					localAI[0] = 0f;
				}
				if (this.ai[1] >= (float)num734)
				{
					TargetClosest();
					this.ai[1] = 0f;
					float num735 = 8f;
					float num736 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector85.X;
					float num737 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector85.Y;
					float num738 = (float)Math.Sqrt(num736 * num736 + num737 * num737);
					num738 = num735 / num738;
					num736 *= num738;
					num737 *= num738;
					int num739 = 24;
					int num740 = 258;
					if (Main.netMode != 1)
					{
						int num741 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector85.X, vector85.Y, num736, num737, num740, num739, 0f, Main.myPlayer);
					}
				}
				this.ai[2] += num733;
				if (life < lifeMax / 3)
				{
					this.ai[2] += num733;
				}
				if (life < lifeMax / 4)
				{
					this.ai[2] += num733;
				}
				if (life < lifeMax / 5)
				{
					this.ai[2] += num733;
				}
				if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[2] += 4f;
				}
				if (this.ai[2] > (float)(60 + Main.rand.Next(600)))
				{
					this.ai[2] = 0f;
					int num742 = 28;
					int num743 = 259;
					if (localAI[1] == 0f)
					{
						for (int num744 = 0; num744 < 2; num744++)
						{
							vector85 = new Vector2(base.Center.X, base.Center.Y - 22f * scale);
							if (num744 == 0)
							{
								vector85.X -= 18f * scale;
							}
							else
							{
								vector85.X += 18f * scale;
							}
							float num745 = 11f;
							float num746 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector85.X;
							float num747 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector85.Y;
							float num748 = (float)Math.Sqrt(num746 * num746 + num747 * num747);
							num748 = num745 / num748;
							num746 *= num748;
							num747 *= num748;
							vector85.X += num746 * 3f;
							vector85.Y += num747 * 3f;
							if (Main.netMode != 1)
							{
								int num749 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector85.X, vector85.Y, num746, num747, num743, num742, 0f, Main.myPlayer);
								Main.projectile[num749].timeLeft = 300;
							}
						}
					}
					else if (localAI[1] != 0f)
					{
						vector85 = new Vector2(base.Center.X, base.Center.Y - 22f * scale);
						if (localAI[1] == -1f)
						{
							vector85.X -= 30f * scale;
						}
						else if (localAI[1] == 1f)
						{
							vector85.X += 30f * scale;
						}
						float num750 = 12f;
						float num751 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector85.X;
						float num752 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector85.Y;
						float num753 = (float)Math.Sqrt(num751 * num751 + num752 * num752);
						num753 = num750 / num753;
						num751 *= num753;
						num752 *= num753;
						vector85.X += num751 * 3f;
						vector85.Y += num752 * 3f;
						if (Main.netMode != 1)
						{
							int num754 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector85.X, vector85.Y, num751, num752, num743, num742, 0f, Main.myPlayer);
							Main.projectile[num754].timeLeft = 300;
						}
					}
				}
			}
			if (life < lifeMax / 2)
			{
				this.ai[0] = 1f;
			}
			else
			{
				this.ai[0] = 0f;
			}
		}
		else if (aiStyle == 47)
		{
			AI_047_GolemFist();
		}
		else if (aiStyle == 48)

```


---

## 🤖 Assistant · 2026-08-19T03:10:46.121Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '31500,31760p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read Golem free head aiStyle 48 section"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:46.147Z

**📎 ToolResult**

```
		else if (aiStyle == 48)
		{
			bool flag48 = false;
			float num755 = GetMyBalance();
			if (Main.getGoodWorld)
			{
				num755 += 3f;
			}
			if ((!Main.player[target].ZoneLihzhardTemple && !Main.player[target].ZoneJungle) || (double)Main.player[target].Center.Y < Main.worldSurface * 16.0)
			{
				num755 *= 2f;
			}
			if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
			{
				noTileCollide = true;
				flag48 = true;
			}
			else if (noTileCollide && Collision.SolidTiles(position, width, height))
			{
				noTileCollide = false;
			}
			if (golemBoss < 0)
			{
				StrikeNPCNoInteraction(9999, 0f, 0);
				return;
			}
			TargetClosest();
			float num756 = 7f;
			float num757 = 0.05f;
			Vector2 vector86 = new Vector2(base.Center.X, base.Center.Y);
			float num758 = Main.player[target].Center.X - vector86.X;
			float num759 = Main.player[target].Center.Y - vector86.Y - 300f;
			float num760 = (float)Math.Sqrt(num758 * num758 + num759 * num759);
			num760 = num756 / num760;
			num758 *= num760;
			num759 *= num760;
			if (velocity.X < num758)
			{
				velocity.X += num757;
				if (velocity.X < 0f && num758 > 0f)
				{
					velocity.X += num757;
				}
			}
			else if (velocity.X > num758)
			{
				velocity.X -= num757;
				if (velocity.X > 0f && num758 < 0f)
				{
					velocity.X -= num757;
				}
			}
			if (velocity.Y < num759)
			{
				velocity.Y += num757;
				if (velocity.Y < 0f && num759 > 0f)
				{
					velocity.Y += num757;
				}
			}
			else if (velocity.Y > num759)
			{
				velocity.Y -= num757;
				if (velocity.Y > 0f && num759 < 0f)
				{
					velocity.Y -= num757;
				}
			}
			float num761 = (num755 + 4f) / 5f;
			this.ai[1] += num761;
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.8)
			{
				this.ai[1] += num761;
			}
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.6)
			{
				this.ai[1] += num761;
			}
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.2)
			{
				this.ai[1] += num761;
			}
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.1)
			{
				this.ai[1] += num761;
			}
			int num762 = 300;
			if (this.ai[1] < 20f || this.ai[1] > (float)(num762 - 20))
			{
				localAI[0] = 1f;
			}
			else
			{
				localAI[0] = 0f;
			}
			if (flag48)
			{
				this.ai[1] = 20f;
			}
			if (this.ai[1] >= (float)num762)
			{
				TargetClosest();
				this.ai[1] = 0f;
				Vector2 vector87 = new Vector2(base.Center.X, base.Center.Y - 10f * scale);
				float num763 = 8f;
				int num764 = 20;
				int num765 = 258;
				float num766 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector87.X;
				float num767 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector87.Y;
				float num768 = (float)Math.Sqrt(num766 * num766 + num767 * num767);
				num768 = num763 / num768;
				num766 *= num768;
				num767 *= num768;
				if (Main.netMode != 1)
				{
					int num769 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector87.X, vector87.Y, num766, num767, num765, num764, 0f, Main.myPlayer);
				}
			}
			float num770 = num755;
			this.ai[2] += num770;
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax / 1.25)
			{
				this.ai[2] += num770;
			}
			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax / 1.5)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 2)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 3)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 4)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 5)
			{
				this.ai[2] += num770;
			}
			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 6)
			{
				this.ai[2] += num770;
			}
			bool flag49 = false;
			if (!Collision.CanHit(Main.npc[golemBoss].Center, 1, 1, Main.player[target].Center, 1, 1))
			{
				flag49 = true;
			}
			if (flag49)
			{
				this.ai[2] += num770 * 10f;
			}
			if (this.ai[2] > (float)(100 + Main.rand.Next(4800)))
			{
				this.ai[2] = 0f;
				for (int num771 = 0; num771 < 2; num771++)
				{
					Vector2 vector88 = new Vector2(base.Center.X, base.Center.Y - 50f * scale);
					switch (num771)
					{
					case 0:
						vector88.X -= 14f * scale;
						break;
					case 1:
						vector88.X += 14f * scale;
						break;
					}
					float num772 = 11f;
					int num773 = 24;
					int num774 = 259;
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.5)
					{
						num773++;
						num772 += 0.25f;
					}
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.4)
					{
						num773++;
						num772 += 0.25f;
					}
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.3)
					{
						num773++;
						num772 += 0.25f;
					}
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.2)
					{
						num773++;
						num772 += 0.25f;
					}
					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.1)
					{
						num773++;
						num772 += 0.25f;
					}
					float num775 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f;
					float num776 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f;
					if (flag49)
					{
						num773 = (int)((double)num773 * 1.5);
						num772 *= 2.5f;
						num775 += Main.player[target].velocity.X * Main.rand.NextFloat() * 50f;
						num776 += Main.player[target].velocity.Y * Main.rand.NextFloat() * 50f;
					}
					num775 -= vector88.X;
					num776 -= vector88.Y;
					float num777 = (float)Math.Sqrt(num775 * num775 + num776 * num776);
					num777 = num772 / num777;
					num775 *= num777;
					num776 *= num777;
					vector88.X += num775 * 3f;
					vector88.Y += num776 * 3f;
					if (Main.netMode != 1)
					{
						int num778 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector88.X, vector88.Y, num775, num776, num774, num773, 0f, Main.myPlayer);
						Main.projectile[num778].timeLeft = 300;
					}
				}
			}
			if (!Main.getGoodWorld)
			{
				position += netOffset;
				int num779 = Main.rand.Next(2) * 2 - 1;
				Vector2 vector89 = base.Bottom + new Vector2((float)(num779 * 22) * scale, -22f * scale);
				Dust dust7 = Dust.NewDustPerfect(vector89, 228, (MathF.PI / 2f + -MathF.PI / 2f * (float)num779 + Main.rand.NextFloatDirection() * (MathF.PI / 4f)).ToRotationVector2() * (2f + Main.rand.NextFloat()));
				Dust dust = dust7;
				dust.velocity += velocity;
				dust7.noGravity = true;
				dust7 = Dust.NewDustPerfect(base.Bottom + new Vector2(Main.rand.NextFloatDirection() * 6f * scale, (Main.rand.NextFloat() * -4f - 8f) * scale), 228, Vector2.UnitY * (2f + Main.rand.NextFloat()));
				dust7.fadeIn = 0f;
				dust7.scale = 0.7f + Main.rand.NextFloat() * 0.5f;
				dust7.noGravity = true;
				dust = dust7;
				dust.velocity += velocity;
				position -= netOffset;
			}
		}
		else if (aiStyle == 49)
		{
			noGravity = true;
			TargetClosest();
			float num780 = 4f;
			float num781 = 0.25f;
			Vector2 vector90 = new Vector2(base.Center.X, base.Center.Y);
			float num782 = Main.player[target].Center.X - vector90.X;
			float num783 = Main.player[target].Center.Y - vector90.Y - 200f;
			float num784 = (float)Math.Sqrt(num782 * num782 + num783 * num783);
			if (num784 < 20f)
			{
				num782 = velocity.X;
				num783 = velocity.Y;
			}
			else
			{
				num784 = num780 / num784;
				num782 *= num784;

```


---

## 🤖 Assistant · 2026-08-19T03:11:57.572Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Key findings so far for the Golem head (aiStyle 46):

1. **Vanilla aiStyle 46 mouth fireball damage is 18** — ours passes 18. ✓ (vanilla num730 = 18, proj 258)
2. Stage 1 (ai[0]==1): spit damage 24 ✓, laser damage 28 ✓ speed 11/12 ✓.
3. Our `golemEyeLasers`: localAI[1]==0 → two shots at ±18*scale, speed 11. ✓. Side: ±30*scale, speed 12. ✓.
4. Free head (aiStyle 48):
   - flag48: `!CanHit(head, player)` → noTileCollide = true, flag48 = true; else if noTileCollide && SolidTiles → noTileCollide = false. Ours: `noLos` computed but never sets noTC... wait, does the free head in ours handle tile collision at all? Ours just does `e.x += e.vx; e.y += e.vy;` at the end with no collision. The vanilla head is noTileCollide toggling. Ours ignores tile collision entirely for the head — meaning always phase. Vanilla: head only phases when it can't see the player; otherwise collides with tiles. Structural difference but minor (head flies at player-300 mostly above). Hmm, but is this "structural"? It changes behavior when head chases into ceiling. I'd rank it low-medium. Actually ours never sets e's noTileCollide equivalent... In our engine, does Enemy have noTileCollide? The fist uses x.noTC and only applies collideGround when... actually the fist never calls collideGround at all. For the head, ours just adds velocity. Vanilla noTileCollide=false → head collides with tiles. Ours never collides → head can pass through floor when it can see the player. Low severity.

   - flag48 → ai[1] = 20 (not "not charging"). Ours: `if (noLos) e.ai1 = 20;` — matches (ai[1] = 20f). ✓ Note ours sets this AFTER computing l0 and BEFORE the >= 300 check — vanilla also: flag48 → ai[1]=20 comes before the >= 300 check. ✓

   - Fireball from free head: vanilla spawns at Center + (0, -10*scale) — ours passes (0, -10*SCALE). ✓ damage 20 ✓ speed 8 ✓.

   - Laser cadence: vanilla num770 = num755 (the balance multiplier), thresholds: /1.25, /1.5, /2, /3, /4, /5, /6. Ours: `r < 1/1.25, r < 1/1.5, r < 1/2, r < 1/3, r < 1/4, r < 1/5, r < 1/6` — matches.

   - flag49: `!CanHit(body.Center, player.Center)` → flag49; ours noLosBody matches.

   - Laser damage/speed tiers: 24 base, +1 dmg/+0.25 spd per tier at 0.5/0.4/0.3/0.2/0.1 ✓. flag49: dmg = (int)(dmg*1.5), spd *= 2.5, aim lead ✓.

   - Wait, ours `dmg = Math.floor(dmg * 1.5)` matches `(int)((double)num773 * 1.5)`.

5. **The laser `timeLeft = 300`** — ours passes 300 to shoot(). OK presumably.

6. Important check — vanilla free-head laser tier conditions read `Main.npc[golemBoss].life < lifeMax * X`. golemBoss is the static index — in vanilla, golemBoss is set by AI_045 each tick while the body is alive; if body died, golemBoss stays pointing at inactive NPC slot → life would be... Actually when the body 245 dies in vanilla, is the free head still around? In vanilla 1.4, the golem fight: you kill head 246 first → 249 spawns. Body becomes vulnerable. If you kill body → NPCLoot, downedGolemBoss set... and the free head 249 remains alive (fight continues until head dies? Actually no — I recall when the body dies, everything dies... Hmm. Let me check vanilla checkDead / HitEffect for 245. Let me look at 85842 area for 246→249 spawn and checkDead for 245.

Actually there's a well-known mechanic: in vanilla, killing the body of Golem before the head... the body is invulnerable while the head lives. Once head detaches (249), killing body ends? Let me check NPCLoot/checkDead for 245.

Let me grep for "downedGolemBoss" in NPC.cs.

Also need to check 246 HitEffect → 249 spawn, and whether the vanilla head-freed head inherits ai etc.

Now for our implementation — one significant structural deviation candidate: **the free head's laser uses `r` = body life ratio, and when body is dead (r=0) all tiers active** — ours handles rBody missing → r=0. Vanilla with dead golemBoss → npc[golemBoss].life of an inactive NPC... whatever. Fine.

Now the important check on **our attached-head stage 0 timing**: vanilla ai[0]==0:
```
ai[1] += 1f;
if (ai[1] < 20 || ai[1] > 280) { ai[1] += 2*(num-1)/3; localAI[0]=1 }
else { ai[1] += 1*(num-1)/2; localAI[0]=0 }
if (ai[1] >= 300) { fire; ai[1] = 0 }
```
Ours:
```
e.ai1 += 1;
if (e.ai1 < 20 || e.ai1 > 280) { e.ai1 += (2 * (num - 1)) / 3; x.l0 = 1; }
else { e.ai1 += (1 * (num - 1)) / 2; x.l0 = 0; }
if (e.ai1 >= 300) { ... }
```
✓ matches.

Attached head stage 1: vanilla TargetClosest each tick then localAI[1] & vector85 offset; num733 = (num+3)/4; ai[1] += num733 (+tiers 0.4/0.2); localAI[0]; fire 24 dmg at vector85 (offset ±40*scale); ai[2] += num733 + tiers /3 /4 /5 + CanHit miss +4; fire lasers at > 60+rand600.

Ours matches: dmg 24, offset x.l1*40*SCALE, oy 10*SCALE ✓; tiers 0.4/0.2 ✓; ai2 tiers maxHp/3, /4, /5 ✓; no-LOS +4 ✓; threshold 60 + rand*600 ✓.

Stage derivation: vanilla `life < lifeMax/2 → ai[0]=1 else 0` — ours `e.ai0 = e.hp < e.maxHp / 2 ? 1 : 0` ✓.

Anchoring: vanilla anchor: num722 = body.Center.X - center.X - 3*scale; num723 = body.Center.Y - center.Y - 57*scale. Ours: dx = body.cx - 3*SCALE - e.cx; dy = body.cy - 57*SCALE - e.cy. ✓ <100 → snap; else *100 toward, rotation = vx*0.1 ✓.

alpha: `if alpha > 0: alpha -= 10; ai[1] = 30` — ours fadeAlpha sets ai1=30 ✓.

Balance num for head: getGoodWorld +3 ✓.

Now — a key check on our `golemHeadAI` for the **free-head hovering**: vanilla target = player.Center + (0,-300), speed 7, accel 0.05 with the "double step when opposite signs". Ours uses accelTo(e.vx, target, 0.05). Need to check accelTo semantics in bossAI.ts. Vanilla's conditional double-step: when velocity and target have opposite signs, add an extra 0.05. accelTo probably just moves toward target by step without the double-step. Minor numeric (2x turn rate). Not structural.

Now — big structural question #1: **our death chain semantics vs vanilla**. Vanilla:
- 246 (attached head) killed → HitEffect spawns 249 at head position. Body loses dontTakeDamage (flag false since 246 inactive).
- Body 245 killed → checkDead → normal death → loot, downed flag. The free head 249 remains (since 249's AI doesn't depend on body except golemBoss static which stays... but wait, golemBoss < 0 check → if golemBoss < 0 → strike 9999. golemBoss is static int; when body dies it isn't reset to -1 immediately? There's code in NPC.UpdateNPC somewhere resetting statics when npc inactive. Let me check: `golemBoss = -1` somewhere. grep.

So in vanilla, killing the body while free head alive: the free head REMAINS and can still kill you; fight ends when head dies? Hmm, actually no — I remember the Golem fight ends when the BODY dies in 1.4? Let me actually check: In Terraria 1.4, Golem: The head is invulnerable... no wait. Golem's body is protected while head is attached. You damage the head/fists. When head's HP drops to 0, the head detaches and flies around (249), and the body becomes vulnerable. The boss dies when the BODY dies (the detached head keeps fighting but killing body ends fight?). Hmm — actually in vanilla, when body dies, the whole boss dies. Let me check NPCLoot / checkDead for 245 to see if it kills other parts.

Let me grep "case 245" or check HitEffect around 85842.

Question #2: our body `dying` handling — sets iframes = 2 every tick during death animation, so it's invulnerable during the 60t. And `e.hp = e.maxHp` at start. That's our own invention ("任务约定" = task convention), documented as intentional deviation. The task says audit for structural deviations; documented deviations per "任务约定" were part of the porting task spec. The prompt says "本体死→部件死、头被击落后本体可受伤" as the linkage to audit. Hmm: "联动:本体死→部件死、头被击落后本体可受伤". Let me verify vanilla: body dies → parts die? If vanilla kills parts when body dies (via NPCLoot_downedGolemBoss or checkDead), then ours must too. Ours: body dying → dead after 60t; the fist anchors: `anchor = body && !body.dead ? body : head` — after body dead, fist anchors to head! In vanilla, fist AI: `golemBoss < 0 → strike 9999`. golemBoss static — when body 245 goes inactive, does golemBoss get reset? If yes → fists die when body dies. Ours keeps fists anchored to the free head — that could be a structural deviation! Let me check where golemBoss is reset.

Let me grep golemBoss in NPC.cs.

Question #3: free head death → ours kills entire family (245-249). In vanilla, killing the free head 249: does the body die too? If in vanilla killing 249 leaves the (invulnerable?) body... body was vulnerable after head detached. If you kill 249 first then body remains alive and vulnerable — you then kill body to finish. Vanilla: killing the head 249 does NOT kill the body. Our version: free head death → whole family self-destructs ("战斗结束"). That IS potentially a structural deviation — the boss would die when you kill the free head, even though the body still has HP. Hmm wait — but actually, in vanilla when the head detaches, the body's remaining HP is what you fight. The head 249 has its own HP (17k?). Killing 249 alone does NOT end the fight in vanilla — you'd still have the body jumping around. Let me verify by checking NPCLoot for 249 and checkDead. Common knowledge: In Terraria, after the head detaches, you can kill either... hmm, actually I believe killing the flying head does NOT kill the body; the body remains and must be killed. And killing the body while head is flying... the head remains? There are videos of "golem head left after body death"? I'm not sure. MUST check source.

Let me grep: "golemBoss" occurrences, "case 245:", "case 246:", "case 249:", HitEffect 85842 area, checkDead.

Question #4 (deerclops later).

Also our attached-head branch when `player` is null: ours skips attack updates entirely but still anchors... vanilla aiStyle 46 uses Main.player[target] always (target guaranteed by boss). Minor.

Now for the free head in ours — vanilla `if (golemBoss < 0) strike`. Ours free head doesn't die when body missing (it reads rBody null → r=0). Documented as "本体已亡(本移植死亡链,原版无此态)" — they claim vanilla has no such state, implying in vanilla the head can't outlive body? If vanilla golemBoss stays valid (static not reset on death) then head continues reading a dead NPC's life (0) → all tiers. Need to check whether golemBoss is reset when body inactive. grep.

Let me also check the vanilla aiStyle 46's flag48-type logic — none for 46.

Also our head: when player exists but dead — vanilla TargetClosest handles. skip.

Now check the vanilla HitEffect 85842-85847 and checkDead for golem family. And NPCLoot for 245/249 (loot conditions like "any part alive"). Let me grep.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:58.536Z · glm-x-preview-260804

```
Golem 头两段已核。关键疑问在死亡链语义(部件联动)。查原版 golemBoss 静态索引的复位、HitEffect 246→249、checkDead/NPCLoot 的家族联动。
```


---

## 🤖 Assistant · 2026-08-19T03:11:58.931Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"golemBoss\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -50",
 "description": "Find all golemBoss static references in NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:58.996Z

**📎 ToolResult**

```
6052:	public static int golemBoss = -1;
19182:		if (golemBoss < 0)
19197:		NPC nPC = Main.npc[golemBoss];
19214:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
19241:				if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
19310:				if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax)
19449:		golemBoss = whoAmI;
31285:			if (golemBoss < 0)
31292:			float num722 = Main.npc[golemBoss].Center.X - vector83.X;
31293:			float num723 = Main.npc[golemBoss].Center.Y - vector83.Y;
31521:			if (golemBoss < 0)
31570:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.8)
31574:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.6)
31578:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.2)
31582:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.1)
31620:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax / 1.25)
31624:			if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax / 1.5)
31628:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 2)
31632:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 3)
31636:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 4)
31640:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 5)
31644:			if (Main.npc[golemBoss].life < Main.npc[golemBoss].lifeMax / 6)
31649:			if (!Collision.CanHit(Main.npc[golemBoss].Center, 1, 1, Main.player[target].Center, 1, 1))
31675:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.5)
31680:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.4)
31685:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.3)
31690:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.2)
31695:					if ((double)Main.npc[golemBoss].life < (double)Main.npc[golemBoss].lifeMax * 0.1)

```


---

## 🤖 Assistant · 2026-08-19T03:11:59.644Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '85820,85870p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read HitEffect area for golem head 246"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:59.708Z

**📎 ToolResult**

```
				{
					Dust.NewDust(position, width, height, 192, hitDirection, -1f, 100, new Color(100, 100, 100, 100));
				}
			}
			else
			{
				for (int num356 = 0; num356 < 50; num356++)
				{
					Dust.NewDust(position, width, height, 192, 2 * hitDirection, -2f, 100, new Color(100, 100, 100, 100));
				}
				Gore.NewGore(position, velocity, 440, scale);
			}
		}
		if (type >= 245 && type <= 249)
		{
			if (life > 0)
			{
				for (int num357 = 0; (double)num357 < dmg / (double)lifeMax * 100.0; num357++)
				{
					Dust.NewDust(position, width, height, 148, hitDirection, -1f);
				}
			}
			else if (type == 246)
			{
				if (Main.netMode != 1)
				{
					NewNPC(GetSpawnSource_NPCHurt(), (int)base.Center.X, (int)position.Y + height, 249, whoAmI);
				}
			}
			else
			{
				for (int num358 = 0; num358 < 50; num358++)
				{
					Dust.NewDust(position, width, height, 148, 2 * hitDirection, -2f);
				}
				if (type == 245)
				{
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 368, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 370, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 368, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 370, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 368, scale);
					Gore.NewGore(new Vector2(position.X + (float)Main.rand.Next(width), position.Y + (float)Main.rand.Next(height)), velocity, 370, scale);
					Gore.NewGore(position, velocity, 360, scale);
					Gore.NewGore(position, velocity, 361, scale);
					Gore.NewGore(position, velocity, 362, scale);
					Gore.NewGore(position, velocity, 363, scale);
					Gore.NewGore(position, velocity, 364, scale);
					Gore.NewGore(position, velocity, 367, scale);
					Gore.NewGore(position, velocity, 366, scale);
				}

```


---

## 🤖 Assistant · 2026-08-19T03:12:09.776Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: `golemBoss` is a static set once at 19449 while the body's AI runs. It's never reset to -1 within these greps (only declared -1 at 6052). So if body dies, `golemBoss` keeps its last index (the inactive slot). The head 249 continues, reading `Main.npc[golemBoss].life` — a dead/inactive NPC has life = 0 typically → all tiers true. The fists keep `golemBoss >= 0` → they don't die; they anchor to `Main.npc[golemBoss]` (inactive NPC at stale position — Center probably stays where it died). Hmm — inactive NPC fields remain stale (position frozen at death). So vanilla fists after body death keep anchoring to the corpse position. Interesting — so "本体死→部件死" claim in the task prompt... In vanilla, killing the body does NOT kill the parts. The parts (fists, free head) keep fighting. Let me verify: is there anything in NPCLoot/checkDead for 245 that kills other parts? Let me search NPCLoot for 245.

Also NewNPC 249 at HitEffect: `NewNPC(source, (int)Center.X, (int)position.Y + height, 249, whoAmI)` — spawn at head's center X, bottom Y. Our golemHeadGoFree transforms in place with full HP.

Wait — important: in vanilla, 249 spawns fresh with full life from its own SetDefaults. Ours sets `e.hp = e.maxHp` where maxHp is 246's maxHp. Need to compare 246 vs 249 lifeMax in SetDefaults :12095-12149. Let me read.

Also need to check NPCLoot 245 / checkDead: does killing body 245 set downedGolemBoss only, or also despawn parts? And does killing 249 give loot/end fight? Let me grep "downedGolemBoss" and check NPCLoot.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:10.572Z · glm-x-preview-260804

```
golemBoss 静态索引除声明外从不复位——部件死后仍锚尸体槽。查 NPCLoot/checkDead 的家族联动与 downedGolemBoss,以及 245-249 SetDefaults。
```


---

## 🤖 Assistant · 2026-08-19T03:12:11.654Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"downedGolemBoss\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; grep -n \"case 245\\|case 246\\|case 247\\|case 248\\|case 249\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -30",
 "description": "Find golem family loot and death handling"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:11.738Z

**📎 ToolResult**

```
1308:				else if (flag5 && Main.hardMode && downedGolemBoss && ((!downedMartians && Main.rand.Next(maxValue2) == 0) || Main.rand.Next(maxValue3) == 0) && !AnyNPCs(399))
1312:				else if (flag5 && Main.hardMode && downedGolemBoss && ((!downedMartians && Main.rand.Next(maxValue2) == 0) || Main.rand.Next(maxValue3) == 0) && !AnyNPCs(399) && ZoneWaterCandle)
4104:					if (flag17 && Main.hardMode && downedGolemBoss && ((!downedMartians && Main.rand.Next(100) == 0) || Main.rand.Next(400) == 0) && !AnyNPCs(399))
6282:	public static bool downedGolemBoss = false;
15947:			if (downedGolemBoss && Main.hardMode)
53521:			if (downedGolemBoss)
80147:			SetEventFlagCleared(ref downedGolemBoss, 6);
92900:			if (downedGolemBoss)
19497:				case 246:
19500:				case 247:
19503:				case 248:
73581:		case 245:
73614:		case 246:
73646:		case 249:
78618:		case 246:
78619:		case 247:
78620:		case 248:
78621:		case 249:
80146:		case 245:
81281:		case 245:

```


---

## 🤖 Assistant · 2026-08-19T03:12:12.205Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '12090,12155p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read SetDefaults for golem family 245-249"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:12.276Z

**📎 ToolResult**

```
			alpha = 175;
			value = Item.buyPrice(0, 0, 20);
			knockBackResist = 0.3f;
			rarity = 1;
		}
		else if (type == 245)
		{
			width = 140;
			height = 140;
			aiStyle = 45;
			damage = 72;
			defense = 26;
			lifeMax = 15000;
			HitSound = SoundID.NPCHit4;
			DeathSound = SoundID.NPCDeath14;
			knockBackResist = 0f;
			value = Item.buyPrice(0, 15);
			alpha = 255;
			boss = true;
			npcSlots = 5f;
		}
		else if (type == 246)
		{
			noGravity = true;
			width = 70;
			height = 70;
			aiStyle = 46;
			damage = 64;
			defense = 20;
			lifeMax = 25000;
			HitSound = SoundID.NPCHit4;
			DeathSound = null;
			knockBackResist = 0f;
			alpha = 255;
		}
		else if (type == 247 || type == 248)
		{
			noGravity = true;
			width = 40;
			height = 30;
			aiStyle = 47;
			damage = 59;
			defense = 28;
			lifeMax = 10000;
			HitSound = SoundID.NPCHit4;
			DeathSound = SoundID.NPCDeath14;
			alpha = 255;
			knockBackResist = 0f;
		}
		else if (type == 249)
		{
			noGravity = true;
			width = 70;
			height = 70;
			aiStyle = 48;
			damage = 80;
			defense = 32;
			lifeMax = 16000;
			HitSound = SoundID.NPCHit4;
			DeathSound = SoundID.NPCDeath14;
			knockBackResist = 0f;
			dontTakeDamage = true;
		}
		else if (type == 250)
		{
			width = 34;

```


---

## 🤖 Assistant · 2026-08-19T03:12:47.704Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key facts:
- 246 lifeMax = 25000; 249 lifeMax = 16000. So when 246 dies and spawns 249 in vanilla, the 249 has 16000 HP (fresh). Our golemHeadGoFree sets `e.hp = e.maxHp` — maxHp is 246's maxHp (25000, or our engine's scaled version). So our free head spawns with FULL 246 HP instead of 16000. That's a structural/HP-pool deviation: the free head phase has 25000 HP instead of 16000. But wait — our engine may scale maxHp differently. In our code, `e.maxHp` for the 246 entity. If our spawner sets maxHp from vanillaNpc(246).lifeMax = 25000, then freed head has 25000 HP vs vanilla 16000. CONFIRMED deviation (HP pool). Severity: medium-high (fight lengthens by ~56% in phase 2 head). But they claim "满血+属性对齐 249 SetDefaults" — they align damage/defense but NOT lifeMax/hp. Actually they set `e.hp = e.maxHp` — keeps 246's maxHp. Deviation.

Wait — actually, is it? Let me double check vanilla: NewNPC 249 → SetDefaults → lifeMax = 16000 → life = lifeMax. Yes. And with expert scaling? Expert multiplier applies via SetDefaults GameDifficulty? Actually life scaling happens in NewNPC via NPC.SetDefaults... whatever, vanilla 249 = 16000 base.

- 249 SetDefaults: `dontTakeDamage = true`! Interesting — the free head 249 is initially dontTakeDamage=true, and then... where does it get cleared? In aiStyle 48 AI I didn't see dontTakeDamage = false. Hmm wait — there must be something. Let me check: In vanilla, the flying golem head after detachment... you CAN damage it. Let me search "249" or aiStyle 48 for dontTakeDamage. In the AI_048 section I read (31500-31742), no dontTakeDamage = false. Hmm! Let me grep "dontTakeDamage" in the file to see the general handling. There's a generic piece in UpdateNPC: `if (dontTakeDamage) ...` hmm. Actually I recall: NPC.dontTakeDamage is set true in SetDefaults 249, then in SpawnNPC or somewhere... Let me grep for context around lines with dontTakeDamage.

Actually — vanilla Golem: the free head 249 is INVULNERABLE! The fight after head detachment is against the body only. Wait, really? Hmm. Let me think about actual gameplay: In Terraria, when Golem's head detaches and starts flying and shooting lasers... can you damage the flying head? I believe the flying head is invulnerable, and the body becomes vulnerable; killing the body ends the fight. YES — that's right! The Golem fight: phase 1, the head and fists take damage (body invulnerable). When the head's HP is depleted, the head detaches and flies around (invulnerable), and the body becomes vulnerable. You kill the BODY to end the fight. The flying head is purely an additional threat you cannot kill.

Hold on, but our implementation says: "自由头血尽 → 全族自毁(战斗结束)". If the free head is invulnerable in vanilla (dontTakeDamage=true, never cleared in AI_048), then the free head can NEVER be killed, and the fight only ends via body death. Our implementation allows damaging the free head and ends the fight when it dies — completely inverted phase-2 semantics!

Wait, wait. Let me be careful. Let me verify dontTakeDamage isn't cleared somewhere for 249. Also check that hurt() respects dontTakeDamage. And also check what happens in checkDead for 245 (line 80146: SetEventFlagCleared(ref downedGolemBoss, 6)). And line 81281 case 245 — probably NPCLoot drop conditions.

Also need to check: when 246 dies → NewNPC 249. But also there's code somewhere that when 249 exists... hmm, but does the BODY die when...? No.

So vanilla phase flow:
1. Body invulnerable (dontTakeDamage = flag) while 246 head active. Head 246 (25000 HP) and fists (10000 HP each) damageable.
2. Head 246 dies → 249 spawns (16000 HP but invulnerable!). Body becomes damageable (flag false since 246 inactive).
3. Kill body (15000 HP) → fight ends, downedGolemBoss set. 249...? When body 245 dies, does 249 despawn? The golemBoss static keeps pointing at the dead body index. 249's AI runs fine. Hmm — but when the boss dies, does the head linger? There might be code in checkDead/NPCLoot... Let me look at 80146 context (case 245 in checkDead?) and check if it kills 249.

Also there's the "active = false" despawn for 245 — when all players dead/far. 249's own despawn: bosses despawn when player far? 249 is not boss flag. Its AI has TargetClosest; when target invalid... aiStyle 48 has no despawn logic shown. Hmm, NPC.UpdateNPC general despawn: if `npc.boss` and player far... general: "if (timeLeft...)". Not critical.

Our implementation's phase flow (from the file header):
- 挂载头在场时本体无敌 ✓ (matches vanilla)
- 本体血尽 → 死亡演出 60t 后真死 — vanilla: body death ends fight immediately (loot). Ours adds 60t death animation — visual invention, acceptable-ish.
- 挂载头血尽 → 原地转自由态 (matches vanilla HitEffect spawn 249), "满血" — 246's full HP not 249's 16000 — DEVIATION (HP pool).
- 自由头血尽 → 全族自毁(战斗结束) — vanilla: 249 is INVULNERABLE (dontTakeDamage=true in SetDefaults, never cleared). The fight CANNOT end via head death. DEVIATION — structural phase inversion!

Hmm wait, actually — let me double-check that dontTakeDamage for 249 isn't cleared. Let me grep dontTakeDamage occurrences near 31500-31760 — I already read the whole aiStyle 48 block; there's no dontTakeDamage mention. But there might be generic code in UpdateNPC that clears dontTakeDamage for non-245 family, or in AI() entry. Let me grep "dontTakeDamage = false" to see all sites.

Also — what about our free head damaging: our engine presumably uses e.dontTakeDamage or iframes. Our code never sets e.dontTakeDamage = true for the free head. In our golemHeadAI, when x.free, we don't set invulnerability. So player CAN kill free head → ends fight. In vanilla, killing the head is impossible; fight ends on body death only.

Actually hold on, let me reconsider — in-game experience: when Golem's head detaches, can you kill it? Searching memory: The Golem's head after detaching... The wiki says: "Once the head's health is depleted, it detaches and flies around, firing lasers. It becomes invulnerable, and the body becomes vulnerable." Hmm, actually I recall the wiki saying the flying head is NOT invulnerable... Let me just check the code. dontTakeDamage = true in SetDefaults 249 — need to find where it's reset. Common pattern: In NPC.UpdateNPC or AI() entry: `dontTakeDamage = false`? No — that would break 245's per-tick set. 245 sets it every tick in AI_045. Let me grep "dontTakeDamage = false".
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:48.285Z · glm-x-preview-260804

```
249 SetDefaults 里有 `dontTakeDamage = true`——这是关键。查它是否在别处被清除，以及 245 死亡(checkDead :80146)是否联动清部件。
```


---

## 🤖 Assistant · 2026-08-19T03:12:49.394Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dontTakeDamage = false\\|dontTakeDamage=false\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -30; echo ---; grep -n \"dontTakeDamage\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | sed -n '1,60p'",
 "description": "Find where dontTakeDamage is cleared"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:49.480Z

**📎 ToolResult**

```
8439:		dontTakeDamage = false;
19489:		dontTakeDamage = false;
24219:				dontTakeDamage = false;
32589:				dontTakeDamage = false;
35293:					dontTakeDamage = false;
35414:				dontTakeDamage = false;
36636:				dontTakeDamage = false;
36907:						dontTakeDamage = false;
36914:				dontTakeDamage = false;
39523:			dontTakeDamage = false;
40690:			dontTakeDamage = false;
42886:					dontTakeDamage = false;
43056:					dontTakeDamage = false;
43145:					dontTakeDamage = false;
43878:		dontTakeDamage = false;
50887:						dontTakeDamage = false;
50905:					dontTakeDamage = false;
50915:				dontTakeDamage = false;
50927:				dontTakeDamage = false;
53591:		dontTakeDamage = false;
56634:				dontTakeDamage = false;
56650:			dontTakeDamage = false;
64055:				dontTakeDamage = false;
---
6194:	public bool dontTakeDamageFromHostiles;
6440:	public bool dontTakeDamage;
8433:		dontTakeDamageFromHostiles = false;
8439:		dontTakeDamage = false;
9626:			dontTakeDamage = true;
9661:			dontTakeDamage = true;
12151:			dontTakeDamage = true;
12338:			dontTakeDamage = true;
12372:			dontTakeDamage = true;
13103:			dontTakeDamage = true;
13707:			dontTakeDamageFromHostiles = true;
13726:			dontTakeDamageFromHostiles = true;
13940:			dontTakeDamage = true;
13992:			dontTakeDamage = true;
14067:			dontTakeDamage = true;
14087:			dontTakeDamage = true;
14123:			dontTakeDamage = true;
14577:			dontTakeDamage = true;
15211:			dontTakeDamage = true;
15229:			dontTakeDamage = true;
15980:			dontTakeDamage = true;
17139:			dontTakeDamage = true;
17573:			dontTakeDamageFromHostiles = true;
17619:			dontTakeDamage = true;
19489:		dontTakeDamage = false;
19509:		dontTakeDamage = flag;
21422:			if (Main.getGoodWorld && !dontTakeDamage)
21426:					dontTakeDamage = true;
21430:					dontTakeDamage = true;
21434:					dontTakeDamage = true;
21612:				dontTakeDamage = this.ai[3] == 4f;
24219:				dontTakeDamage = false;
24238:						dontTakeDamage = true;
30053:					dontTakeDamage = true;
32589:				dontTakeDamage = false;
35189:				dontTakeDamage = true;
35212:				dontTakeDamage = true;
35293:					dontTakeDamage = false;
35365:					dontTakeDamage = true;
35414:				dontTakeDamage = false;
36636:				dontTakeDamage = false;
36788:				dontTakeDamage = true;
36812:				dontTakeDamage = true;
36856:				dontTakeDamage = true;
36907:						dontTakeDamage = false;
36914:				dontTakeDamage = false;
36927:				dontTakeDamage = true;
37067:				dontTakeDamage = true;
37211:			if (frameCounter == 19.0 && !dontTakeDamage)
37215:			dontTakeDamage = frameCounter >= 21.0;
37256:				dontTakeDamage = true;
37703:				dontTakeDamage = true;
37720:			if (localAI[3] == 13f && !dontTakeDamage)
37724:			dontTakeDamage = localAI[3] >= 15f;
37766:				dontTakeDamage = true;
37790:				dontTakeDamage = true;
39523:			dontTakeDamage = false;
39644:				dontTakeDamage = true;
39921:				dontTakeDamage = true;
40507:				dontTakeDamage = true;

```


---

## 🤖 Assistant · 2026-08-19T03:12:50.637Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '80120,80175p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo =====; sed -n '73570,73680p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read checkDead case 245 and NPCLoot golem cases"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:50.712Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
			}
			break;
		case 517:
			downedTowerSolar = true;
			TowerActiveSolar = false;
			WorldGen.UpdateLunarApocalypse();
			WorldGen.MessageLunarApocalypse();
			break;
		case 422:
			downedTowerVortex = true;
			TowerActiveVortex = false;
			WorldGen.UpdateLunarApocalypse();
			WorldGen.MessageLunarApocalypse();
			break;
		case 507:
			downedTowerNebula = true;
			TowerActiveNebula = false;
			WorldGen.UpdateLunarApocalypse();
			WorldGen.MessageLunarApocalypse();
			break;
		case 493:
			downedTowerStardust = true;
			TowerActiveStardust = false;
			WorldGen.UpdateLunarApocalypse();
			WorldGen.MessageLunarApocalypse();
			break;
		case 245:
			SetEventFlagCleared(ref downedGolemBoss, 6);
			break;
		case 370:
			SetEventFlagCleared(ref downedFishron, 7);
			break;
		case 636:
			SetEventFlagCleared(ref downedEmpressOfLight, 23);
			break;
		case 668:
			SetEventFlagCleared(ref downedDeerclops, 25);
			break;
		case 657:
			SetEventFlagCleared(ref downedQueenSlime, 24);
			break;
		case 22:
			if (Collision.LavaCollision(position, width, height))
			{
				SpawnWOF(position);
			}
			break;
		case 614:
		{
			int num2 = 175;
			if (SpawnedFromStatue)
			{
				num2 = 0;
			}
			Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, 0f, 0f, 281, num2, 0f, Main.myPlayer, -2f, releaseOwner + 1);
			break;
(eval):1: ==== not found

```


---

## 🤖 Assistant · 2026-08-19T03:12:57.607Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The second command failed on `=====` (zsh interpreted). But I got the first part. Key line 8439: `dontTakeDamage = false;` — need context. Let me check line 8433-8445 to see where that reset happens — it might be in `ClearNPC` or in the per-tick reset (like `AI()` preamble or `UpdateNPC`). Let me check.

Also — line 12151 dontTakeDamage = true is the 249 SetDefaults. The clears at 8439 — let me see which method contains it. If it's in UpdateNPC per-tick reset, then 249 would be damageable... Let me read around 8420-8450.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:58.259Z · glm-x-preview-260804

```
第二个命令的分隔符出错，重跑；同时查 ：8439 的 dontTakeDamage=false 在哪个方法里。
```


---

## 🤖 Assistant · 2026-08-19T03:12:58.737Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '8400,8445p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read context around line 8439 dontTakeDamage reset"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:58.785Z

**📎 ToolResult**

```
			oldRot[i] = 0f;
			oldPos[i].X = 0f;
			oldPos[i].Y = 0f;
		}
		for (int j = 0; j < BuffID.Count; j++)
		{
			buffImmune[j] = false;
		}
		setFrameSize = false;
		spawnNeedsSyncing = false;
		realLife = -1;
		lifeRegen = 0;
		lifeRegenExpectedLossPerSecond = -1;
		lifeRegenCount = 0;
		markedByScytheWhip = false;
		markedByEelWhip = false;
		poisoned = false;
		bleeding = false;
		tipsy = false;
		hemorrhage = false;
		soulDrain = false;
		venom = false;
		shadowFlame = false;
		canDisplayBuffs = true;
		onFire = false;
		midas = false;
		ichor = false;
		brokenArmor = false;
		onFrostBurn = false;
		onFrostBurn2 = false;
		shimmering = false;
		confused = false;
		loveStruck = false;
		dontTakeDamageFromHostiles = false;
		stinky = false;
		dryadWard = false;
		onFire2 = false;
		onFire3 = false;
		justHit = false;
		dontTakeDamage = false;
		catchableNPCTempImmunityCounter = 0;
		electricEelCounter = 0;
		npcSlots = 1f;
		lavaImmune = false;
		wetCount = 0;
		townNPC = false;

```


---

## 🤖 Assistant · 2026-08-19T03:12:59.263Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '73570,73680p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPCLoot golem family cases"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:59.318Z

**📎 ToolResult**

```
			frameCounter += 1.0;
			if (frameCounter >= 6.0)
			{
				frame.Y += num;
				frameCounter = 0.0;
			}
			if (frame.Y >= num * Main.npcFrameCount[type])
			{
				frame.Y = 0;
			}
			break;
		case 245:
			if (ai[0] == 0f)
			{
				if (ai[1] < -16f)
				{
					frame.Y = 0;
				}
				else if (ai[1] < -12f)
				{
					frame.Y = num;
				}
				else if (ai[1] < -8f)
				{
					frame.Y = num * 2;
				}
				else if (ai[1] < -4f)
				{
					frame.Y = num * 3;
				}
				else if (ai[1] < 0f)
				{
					frame.Y = num * 4;
				}
				else
				{
					frame.Y = 0;
				}
			}
			else if (ai[0] == 1f)
			{
				frame.Y = 1;
			}
			break;
		case 246:
			if (ai[0] == 0f)
			{
				if (localAI[0] == 1f)
				{
					frame.Y = num;
				}
				else
				{
					frame.Y = 0;
				}
			}
			else if (ai[0] == 1f)
			{
				if (localAI[0] == 1f)
				{
					frame.Y = num;
				}
				else
				{
					frame.Y = 0;
				}
				if (localAI[1] == -1f)
				{
					frame.Y += num * 4;
				}
				if (localAI[1] == 1f)
				{
					frame.Y += num * 2;
				}
			}
			break;
		case 249:
			if (localAI[0] == 1f)
			{
				frame.Y = num;
			}
			else
			{
				frame.Y = 0;
			}
			if ((frameCounter += 1.0) >= 16.0)
			{
				frameCounter = 0.0;
			}
			break;
		case 141:
			spriteDirection = direction;
			if (velocity.Y != 0f)
			{
				frame.Y = num * 2;
				break;
			}
			frameCounter += 1.0;
			if (frameCounter >= 8.0)
			{
				frame.Y += num;
				frameCounter = 0.0;
			}
			if (frame.Y > num)
			{
				frame.Y = 0;
			}
			break;
		case 243:
			if (frameCounter < 0.0)
			{

```


---

## 🤖 Assistant · 2026-08-19T03:13:34.303Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line 8439's `dontTakeDamage = false` is inside SetDefaults (the big reset loop at the start of SetDefaults — line 8400-8445 shows field resets including realLife, buffImmune, etc., which is the SetDefaults preamble). So it's the SetDefaults reset, not a per-tick clear. 

So: 249 SetDefaults sets dontTakeDamage = true (line 12151) at the END of SetDefaults (after the reset at 8439). aiStyle 48 AI never clears it. Nothing else clears it for 249. Therefore **the free golem head 249 is permanently invulnerable in vanilla**. This confirms: the vanilla fight's only kill target after head detachment is the body.

Wait — but let me double check whether something else clears dontTakeDamage for 249. Possible candidates: `StrikeNPC`? No, that respects it. Transform? Let me also grep in the 31500-31742 range again — no dontTakeDamage. Also check `NewNPC` post-spawn code that might clear... The HitEffect spawn: `NewNPC(GetSpawnSource_NPCHurt(), x, y, 249, whoAmI)`. NewNPC applies SetDefaults (dontTakeDamage=true). No override.

Hmm, but wait — there IS one more consideration: the vanilla wiki. In actual gameplay, when Golem's head flies free, can you damage it? Yes... no? Let me think about actual gameplay footage. Golem: you break the head's HP → it detaches, keeps shooting. Players continue attacking the BODY. The head circles above. I'm fairly confident the flying head is invulnerable — the wiki states "The head will detach and become invulnerable once its health is depleted" — actually I recall the wiki: "When the head's health reaches zero, it detaches from the body and hovers around, continuing to attack. The body then becomes vulnerable to damage. The flying head itself is invulnerable." Yes, this matches dontTakeDamage=true in SetDefaults with no clear.

So OUR implementation has TWO structural deviations:

A) Our free head (after golemHeadGoFree) is damageable and when killed → whole family dies (fight ends). In vanilla the free head is invulnerable and unkillable; fight ends only via body death. This inverts phase 2: a player can "cheese" by killing the flying head to end the fight without damaging the body; and conversely must kill head-pool HP (25000 in ours due to maxHp bug) — wait ours: the head goes free with e.hp = e.maxHp (246's 25000). And our free head can be damaged (no invuln set). So phase 2 = kill flying head (25000 HP) OR kill body (15000). Two kill paths vs vanilla's one (body).

Hmm wait — but hold on. Our body: `hasHead` requires 246 with ai3 !== 1. After head goes free, hasHead false → body vulnerable. OK. So in ours, both body and free head are damageable, and killing EITHER ends the fight (free head death → 全族自毁; body death → dying → dead... wait, does body death in ours kill the free head? Body dying sets ai3=1; head AI: `if (!x.free && (!body || body.ai3 === 1 || body.hp <= 0)) golemHeadGoFree` — that's for attached head. Free head continues after body death (fist anchors to head). Body death in ours does NOT kill the free head or fists! So fight continues until free head killed. Vanilla: body death ends fight (downedGolemBoss at 80146-80147, in what method? case 245 in... let me check which method line 80146 is in — need to confirm it's checkDead or NPCLoot. Either way killing body sets the flag → fight over; and 249 remains invulnerable-but-alive? It would linger... hmm, actually there might be despawn handling. Whatever — the flag gets set on body death.

So ours: fight ends only via free-head death (or body death → but that doesn't end it since head persists!). Wait no — body death → dying → after 60t, e.dead = true. Head continues (findBody returns null → free head continues flying, shooting). Fists anchor to head. So after body death, fight continues until player kills the free head. In vanilla, body death = fight over.

This is a MAJOR structural deviation: inverted win condition. In vanilla phase 2, the player kills the BODY to win (head invulnerable). In ours, the player must kill the FLYING HEAD to win (body death doesn't end fight), and the flying head has 25000 HP instead of... well it's damageable.

Hmm wait, let me re-read our code once more.

golemAI (body):
- hp<=0 && !dying → dying=true, deadT=0, ai3=1, hp=maxHp. 
- During dying: 60t animation, then e.dead = true. No family kill, no downedGolemBoss equivalent (that's presumably handled by our engine when e.dead && bossFled false... our engine's death chain - can't verify without reading Enemy; but the file comment says "原版由 245 死亡置 downedGolemBoss" implying engine handles).

golemHeadAI (head):
- hp<=0: if free → e.dead = true + kill all 245-249 → fight over. If not free → golemHeadGoFree.

So: killing the body does NOT end the fight in ours (head keeps fighting). Killing the free head DOES end the fight. That's exactly inverted from vanilla where body death = victory and head is invulnerable.

BUT — wait. Consider the actual vanilla flow again more carefully. In vanilla, which entity ends the fight? checkDead case 245 → SetEventFlagCleared(downedGolemBoss). Let me confirm 80146 is in checkDead. It's likely in " NPCLoot " or "checkDead". Line 80120-80175 shows a switch with tower flags (downedTowerSolar etc.) — these SetEventFlagCleared calls are in... probably `CheckBossFlag` no — they're in some method called on boss death. Let me find the method name. Also for 249: does its death even drop loot? 249 is invulnerable so it never dies — moot.

Also — do the FISTS die when body dies in vanilla? golemBoss static never reset (only -1 at declaration). After body death, Main.npc[golemBoss] is inactive. Fists check `golemBoss < 0` → false → continue, anchoring to inactive NPC slot (position frozen where body died). Hmm, that means in vanilla after body death, fists keep punching from the corpse position and the invulnerable head keeps flying?? That seems odd but it's what the code says. Actually wait — is there a static-reset when NPC deactivates? Let me grep for something like `if (!Main.npc[golemBoss].active)`. Search "golemBoss" gave all occurrences — none check .active. Hmm, but NPC slots get reused! When the body's slot is reused by another NPC spawn, golemBoss points at a random NPC. Messy vanilla edge case. In practice: body dies → 249 and fists linger? There must be something. Let me check if there's despawn logic in UpdateNPC for boss parts — e.g., `if (Main.npc[i].boss && ...)`. Or maybe the fists/head despawn when no players nearby.

Actually, hmm, let me look for how vanilla handles "boss died while parts alive" — e.g. for Skeletron Prime hands. Common pattern: in checkDead of the boss, parts get killed. Let me check the method containing line 80146. Let me search backwards for "private void" / "public void" before 80120.

Also for the Deerclops audit, I still need to read 44338-45141. Let me do that next.

Let me first determine the method at 80146.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:35.508Z · glm-x-preview-260804

```
8439 的复位在 SetDefaults 前导里，非逐帧清除——即 249 的 dontTakeDamage=true 永不被清，自由头恒无敌。确认 ：80146 所在方法及 245 死亡时对部件的处置。
```


---

## 🤖 Assistant · 2026-08-19T03:13:37.435Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=79900 && NR<=80150 && (/private|public|internal/ && /void|bool|int|float/)' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | tail -5; echo ---; awk 'NR<=80146' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"void NPCLoot\\|bool CheckDead\\|void checkDead\\|private void.*Dead\\|public bool.*Dead\" | tail -5",
 "description": "Identify method containing line 80146"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:37.742Z

**📎 ToolResult**

```
	private void DoDeathEvents(Player closestPlayer)
---
78828:	public void checkDead()
79212:	private void DropEoWLoot(bool fromCheckDead = true)
79628:	public void NPCLoot()
79726:	private void NPCLoot_DropItems(Player closestPlayer)
79899:	private void NPCLoot_DropHeals(Player closestPlayer)

```


---

## 🤖 Assistant · 2026-08-19T03:13:38.049Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case 668\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "Locate deerclops death flag sites"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:38.141Z

**📎 ToolResult**

```
67390:		case 668:
80155:		case 668:

```


---

## 🤖 Assistant · 2026-08-19T03:14:14.859Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line 80146 (case 245 → SetEventFlagCleared(downedGolemBoss)) is inside `DoDeathEvents` — called on the NPC's actual death. So killing the body 245 fires the downed flag and loot. Killing the free head 249 does nothing special (it's invulnerable anyway).

Now — does killing 245 despawn 249/fists? Not in DoDeathEvents per what we saw. The parts linger until they despawn naturally (players leave, or...?). Actually there might be something in UpdateNPC: bosses despawn when players are dead/far. 249 isn't boss=true. Fists aren't boss. So they linger but the fight flag is set. Edge case, not critical for our audit.

Conclusion for Golem death chain: OUR inverted win condition is a CONFIRMED structural deviation:
1. Vanilla: 249 invulnerable (SetDefaults 12151 dontTakeDamage=true, never cleared — aiStyle 48 block 31500-31742 has no clear; the only "false" resets are in SetDefaults preamble 8439 / other AI styles). Fight ends when body 245 dies (DoDeathEvents case 245 sets downedGolemBoss).
2. Ours: free head damageable, killing it ends the whole fight (golemHeadAI lines 417-428); body death does NOT end fight (head+fists persist; head remains attackable).

Severity: HIGH. This inverts phase 2's win condition.

Second deviation: freed head HP = 246's maxHp (25000) instead of 249's 16000 (SetDefaults 12127 vs 12143). Combined with #1 — in ours head has 25000 HP pool. Medium.

Third: our body `dying` 60t death-animation is an invention but cosmetic-ish. However it also resets hp to maxHp and sets iframes — meaning the body "survives" 60 more ticks while head detaches. Not a vanilla behavior but documented as task convention. I'd note it as documented deviation, not CONFIRMED bug per instructions? The prompt says "审计维度:阶段缺失/转换条件错/速度档错/专家分支漏/弹幕id-计数-速度错/flee语义无出处/部件联动错". The win-condition inversion IS 部件联动错. The HP pool is 数值错 but structural-ish (phase-2 HP pool).

Now — check our body ai0===0 gate `if (player && e.ai0 === 0)`: vanilla runs ai[0]==0 branch regardless of target validity (uses Main.player[target]). If player is null in ours (dead?), AI skips charging. Vanilla: target always set for bosses via TargetClosest; if all players dead → still runs with dead player target... eh. Minor.

Vanilla despawn: `target <= 0 || target == 255 || dead → TargetClosest; 3000 manhattan double-check → active=false`. Ours: `!player → noTC=true only` (no despawn — matches vanilla player-dead behavior of no despawn); `> 3000 → dead + bossFled`. Vanilla: distance check happens regardless of player dead (dead player position → TargetClosest may switch to another player). Ours uses player param. Need to check the call convention — if the harness passes null when player dead, then ours never despawns while player dead but vanilla also doesn't (unless far). Roughly equivalent. OK, minor.

Now — the jump condition `else if (e.ai1 === -1)`: vanilla `ai[1] == -1f` — from -20 incrementing by 1 each tick while vy==0: -20→-19→...→-1 triggers. Ours same. ✓ But note vanilla decrements? No: ai[1] += num4 where num4 = 1 (ai[1] not > 0) → -20 + 1 → increments toward -1. ✓.

One more check in ours body: `if (e.vy === 0)` — vanilla `velocity.Y == 0f`. After collideGround sets vy=0 on landing. But our collideGround runs at the END (after AI). At the start of a tick, e.vy reflects last tick's post-collision state. Fine.

getGoodWorld smashTorches: ours y range `e.y to e.y + e.w` — vanilla: `k from position.Y/16 to (position.Y + width)/16` — yes width. Ours 1:1 including the quirk. ✓ (documented).

Fist: `e.facing = isLeft ? 1 : -1` — irrelevant to vanilla (uses rotation). Fine.

Fist state 1: ours pins `e.x = tx - e.w / 2; e.y = ty - e.h / 2` — vanilla `base.Center = vector` — same. ✓ And ours skips movement for state 1 (`if (x.state !== 1)`). ✓

Fist collideX/collideY: vanilla checks AFTER movement (collide flags set during movement). Ours: `if (x.state === 2 && !x.noTC && hitSolid(game, e))` after movement. Vanilla's condition `num2 > 700 || collideX || collideY` — num2 computed pre-movement. Ours checks dist>700 pre-movement (inside state 2 branch, before the movement block). ✓ 

Hmm wait, one subtlety: in ours, `dist` for state 2 is computed BEFORE the branch (line 580), pre-movement — same as vanilla num2. ✓

Now — our fist when `!player` returns after setting spin but... `if (!player) { e.x += e.vx; e.y += e.vy; return; }` — fine.

But CRITICAL fist deviation: vanilla fist anchors `Main.npc[golemBoss]` — the BODY only, even if dead (stale slot). Ours anchors to head after body death. But that's part of the death-chain deviation already noted. Actually more precisely: in vanilla after body death, fists keep operating anchored to the dead body slot. Ours re-anchors to the head — different but both "weird". Given vanilla 249 invulnerable + body death = fight over, the cleanest fix: body death should end fight (kill parts) per DoDeathEvents... but vanilla doesn't kill parts in code. OK.

Also note: our head AI's `findBody` for attached head: `body.ai3 === 1` — body dying → head detaches immediately. In vanilla, head stays attached while body at 0 HP pre-death? Body at 0 → checkDead → death same tick basically. Fine.

Now — the free head aiStyle 48's noTileCollide toggling: ours never collides with tiles (movement is raw). Vanilla: noTileCollide=false when it can see player and not inside solid → head collides with tiles. Structural-ish but head hovers at player-300; would rarely hit tiles except when player under ceiling. Medium-low. I might list as minor/存疑. Actually the flag48 branch: `if (!CanHit) { noTileCollide = true; flag48 = true } else if (noTileCollide && SolidTiles) { noTileCollide = false }`. Ours ignores entirely → head never blocked by terrain when it CAN see player (it would fly through floor toward a player below?). Target is player-300 (above player), so mostly flies up. Meh, minor.

Now the attached head when player null: ours skips attacks. Vanilla uses Main.player[target] — for bosses target is whoever; fine.

OK now — one more Golem check: our `golemSpit` from attached head stage 0: origin (0, +10*SCALE) ✓ vanilla Center + 10*scale down. Speed 8, dmg 18, proj 258 ✓.

Free head fireball: origin (0, -10*SCALE) ✓ dmg 20 spd 8 ✓.

Free-head lasers: origin ±14*SCALE, -50*SCALE ✓; dmg 24 spd 11 + tiers ✓; +3*velocity offset ✓; timeLeft 300 ✓.

Attached head lasers: origin ±18 or ±30 *SCALE at -22*SCALE ✓ dmg 28 ✓ spd 11/12 ✓.

Balance num: vanilla `GetMyBalance()` — what is it? It's a method; for single player returns 1? It's probably player-count scaling. Ours `num = 1` + ftw + temple/jungle ×2. GetMyBalance for classic single = 1. OK.

Now Deerclops. Read NPC.cs 44338-45141.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:15.969Z · glm-x-preview-260804

```
Golem 结论成形：249 自由头在原版恒无敌(dontTakeDamage=true 只在 SetDefaults 前导清零后立刻置真，AI_048 全段无清除)，胜利条件=杀本体。现在读 Deerclops 全段。
```


---

## 🤖 Assistant · 2026-08-19T03:14:16.423Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '44338,44530p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_123_Deerclops part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:16.485Z

**📎 ToolResult**

```
	private void AI_123_Deerclops()
	{
		deerclopsBoss = whoAmI;
		int num = 15;
		NPCAimedTarget targetData = GetTargetData();
		bool haltMovement = false;
		bool goHome = false;
		bool flag = Distance(targetData.Center) >= 450f;
		localAI[3] = MathHelper.Clamp(localAI[3] + (float)flag.ToDirectionInt(), 0f, 30f);
		dontTakeDamage = localAI[3] >= 30f;
		float lifePercent = (float)life / (float)lifeMax;
		bool expertMode = Main.expertMode;
		int shadowHandDamage = 10;
		float num2 = Utils.Remap(localAI[3], 0f, 30f, 0f, 1f);
		if (num2 > 0f)
		{
			float num3 = Main.rand.NextFloat() * num2 * 3f;
			while (num3 > 0f)
			{
				num3 -= 1f;
				Dust.NewDustDirect(position, width, height, 109, 0f, -3f, 0, default(Color), 1.4f).noGravity = true;
			}
		}
		if (homeTileX == -1 && homeTileY == -1)
		{
			Point point = base.Bottom.ToTileCoordinates();
			homeTileX = point.X;
			homeTileY = point.Y;
			this.ai[2] = homeTileX;
			this.ai[3] = homeTileY;
			netUpdate = true;
			timeLeft = 86400;
		}
		timeLeft -= Main.dayRate;
		if (timeLeft < 0)
		{
			timeLeft = 0;
		}
		homeTileX = (int)this.ai[2];
		homeTileY = (int)this.ai[3];
		if (!expertMode)
		{
			localAI[2] = 0f;
		}
		if (expertMode && Main.netMode != 1)
		{
			SpawnPassiveShadowHands(lifePercent, shadowHandDamage);
		}
		switch ((int)this.ai[0])
		{
		case -1:
			localAI[3] = -10f;
			break;
		case 6:
		{
			TargetClosest(faceTarget: false);
			targetData = GetTargetData();
			if (Main.netMode != 1)
			{
				if (!ShouldRunAway(ref targetData, isChasing: false))
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
					localAI[1] = 0f;
					netUpdate = true;
					break;
				}
				if (timeLeft <= 0)
				{
					this.ai[0] = 8f;
					this.ai[1] = 0f;
					localAI[1] = 0f;
					netUpdate = true;
					break;
				}
			}
			if (direction != oldDirection)
			{
				netUpdate = true;
			}
			goHome = true;
			this.ai[1] += 1f;
			Vector2 other = new Vector2(homeTileX * 16, homeTileY * 16);
			bool flag2 = base.Top.Y > other.Y + 1600f;
			bool num4 = Distance(other) < 1020f;
			Distance(targetData.Center);
			float num5 = this.ai[1] % 600f;
			if (num4 && num5 < 420f)
			{
				haltMovement = true;
			}
			bool flag3 = false;
			int num6 = 300;
			if (flag2 && this.ai[1] >= (float)num6)
			{
				flag3 = true;
			}
			int num7 = 1500;
			if (!num4 && this.ai[1] >= (float)num7)
			{
				flag3 = true;
			}
			if (flag3)
			{
				this.ai[0] = 7f;
				this.ai[1] = 0f;
				localAI[1] = 0f;
				netUpdate = true;
			}
			break;
		}
		case 0:
		{
			TargetClosest();
			targetData = GetTargetData();
			if (ShouldRunAway(ref targetData, isChasing: true))
			{
				this.ai[0] = 6f;
				this.ai[1] = 0f;
				localAI[1] = 0f;
				netUpdate = true;
				break;
			}
			this.ai[1] += 1f;
			Vector2 vector = base.Bottom + new Vector2(0f, -32f);
			Vector2 vector2 = targetData.Hitbox.ClosestPointInRect(vector);
			Vector2 vector3 = vector2 - vector;
			(vector2 - base.Center).Length();
			float num15 = 0.6f;
			bool flag4 = Math.Abs(vector3.X) >= Math.Abs(vector3.Y) * num15 || vector3.Length() < 48f;
			bool flag5 = vector3.Y <= (float)(100 + targetData.Height) && vector3.Y >= -200f;
			if (Math.Abs(vector3.X) < 120f && flag5 && velocity.Y == 0f && localAI[1] >= 2f)
			{
				velocity.X = 0f;
				this.ai[0] = 4f;
				this.ai[1] = 0f;
				localAI[1] = 0f;
				netUpdate = true;
				break;
			}
			if (Math.Abs(vector3.X) < 120f && flag5 && velocity.Y == 0f && flag4)
			{
				velocity.X = 0f;
				this.ai[0] = 1f;
				this.ai[1] = 0f;
				localAI[1] += 1f;
				netUpdate = true;
				break;
			}
			bool flag6 = this.ai[1] >= 240f;
			if (velocity.Y == 0f && velocity.X != 0f && flag6)
			{
				velocity.X = 0f;
				this.ai[0] = 2f;
				this.ai[1] = 0f;
				localAI[1] = 0f;
				netUpdate = true;
				break;
			}
			bool flag7 = this.ai[1] >= 90f;
			if (velocity.Y == 0f && velocity.X == 0f && flag7)
			{
				velocity.X = 0f;
				this.ai[0] = 5f;
				this.ai[1] = 0f;
				localAI[1] = 0f;
				netUpdate = true;
				break;
			}
			bool flag8 = this.ai[1] >= 120f;
			int num16 = 32;
			bool flag9 = targetData.Type == NPCTargetType.Player && !Main.player[target].buffImmune[num16] && Main.player[target].FindBuffIndex(num16) == -1;
			if (velocity.Y == 0f && flag8 && flag9 && Math.Abs(vector3.X) > 100f)
			{
				velocity.X = 0f;
				this.ai[0] = 3f;
				this.ai[1] = 0f;
				localAI[1] = 0f;
				netUpdate = true;
			}
			break;
		}
		case 1:
			this.ai[1] += 1f;
			haltMovement = true;
			AI_123_Deerclops_MakeSpikesForward(1, targetData);
			if (this.ai[1] >= 80f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				netUpdate = true;
			}
			break;

```


---

## 🤖 Assistant · 2026-08-19T03:14:19.307Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continue reading 44530-44760.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:19.508Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '44530,44760p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_123_Deerclops part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:19.797Z

**📎 ToolResult**

```
			break;
		case 4:
			this.ai[1] += 1f;
			haltMovement = true;
			TargetClosest();
			AI_123_Deerclops_MakeSpikesBothSides(1, targetData);
			if (this.ai[1] >= 90f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				netUpdate = true;
			}
			break;
		case 2:
		{
			int num8 = 4;
			int num9 = 8 * num8;
			this.ai[1] += 1f;
			if (this.ai[1] == (float)(num9 - 20))
			{
				SoundEngine.PlaySound(SoundID.DeerclopsScream, base.Center);
			}
			if (this.ai[1] == (float)num9)
			{
				SoundEngine.PlaySound(SoundID.DeerclopsRubbleAttack, base.Center);
			}
			haltMovement = true;
			if (Main.netMode != 1 && this.ai[1] >= (float)num9)
			{
				Point sourceTileCoords = base.Top.ToTileCoordinates();
				int num10 = 20;
				int distancedByThisManyTiles = 1;
				float upBiasPerSpike = 200f;
				sourceTileCoords.X += direction * 3;
				sourceTileCoords.Y -= 10;
				int num11 = (int)this.ai[1] - num9;
				if (num11 == 0)
				{
					PunchCameraModifier modifier4 = new PunchCameraModifier(base.Center, new Vector2(0f, -1f), 20f, 6f, 30, 1000f, "Deerclops");
					Main.instance.CameraModifiers.Add(modifier4);
				}
				int num12 = 1;
				int num13 = num11 / num12 * num12;
				int num14 = num13 + num12;
				if (num11 % num12 != 0)
				{
					num14 = num13;
				}
				for (int j = num13; j < num14 && j < num10; j++)
				{
					AI_123_Deerclops_ShootRubbleUp(ref targetData, ref sourceTileCoords, num10, distancedByThisManyTiles, upBiasPerSpike, j);
				}
			}
			if (this.ai[1] >= 60f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				netUpdate = true;
			}
			break;
		}
		case 3:
			if (this.ai[1] == 30f)
			{
				SoundEngine.PlaySound(SoundID.DeerclopsScream, base.Center);
			}
			this.ai[1] += 1f;
			haltMovement = true;
			if ((int)this.ai[1] % 4 == 0 && this.ai[1] >= 28f)
			{
				PunchCameraModifier modifier5 = new PunchCameraModifier(base.Center, (Main.rand.NextFloat() * (MathF.PI * 2f)).ToRotationVector2(), 20f, 6f, 20, 1000f, "Deerclops");
				Main.instance.CameraModifiers.Add(modifier5);
				if (Main.netMode != 2)
				{
					Player player = Main.player[Main.myPlayer];
					_ = Main.myPlayer;
					int num17 = 32;
					int time = 720;
					if (!player.dead && player.active && player.FindBuffIndex(num17) == -1 && (player.Center - base.Center).Length() < 800f && !player.creativeGodMode)
					{
						player.AddBuff(num17, time);
					}
				}
			}
			if (this.ai[1] == 30f)
			{
				TargetClosest();
			}
			if (this.ai[1] >= 60f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				netUpdate = true;
			}
			break;
		case 7:
			if (this.ai[1] == 30f)
			{
				SoundEngine.PlaySound(SoundID.DeerclopsScream, base.Center);
			}
			this.ai[1] += 1f;
			haltMovement = true;
			if ((int)this.ai[1] % 4 == 0 && this.ai[1] >= 28f)
			{
				PunchCameraModifier modifier3 = new PunchCameraModifier(base.Center, (Main.rand.NextFloat() * (MathF.PI * 2f)).ToRotationVector2(), 20f, 6f, 20, 1000f, "Deerclops");
				Main.instance.CameraModifiers.Add(modifier3);
			}
			if (this.ai[1] == 40f)
			{
				TargetClosest();
				if (Main.netMode != 1)
				{
					netUpdate = true;
					base.Bottom = new Vector2(homeTileX * 16, homeTileY * 16);
				}
			}
			if (this.ai[1] >= 60f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				netUpdate = true;
			}
			break;
		case 8:
			if (this.ai[1] == 30f)
			{
				SoundEngine.PlaySound(SoundID.DeerclopsScream, base.Center);
			}
			this.ai[1] += 1f;
			haltMovement = true;
			if ((int)this.ai[1] % 4 == 0 && this.ai[1] >= 28f)
			{
				PunchCameraModifier modifier2 = new PunchCameraModifier(base.Center, (Main.rand.NextFloat() * (MathF.PI * 2f)).ToRotationVector2(), 20f, 6f, 20, 1000f, "Deerclops");
				Main.instance.CameraModifiers.Add(modifier2);
			}
			if (this.ai[1] >= 40f)
			{
				life = -1;
				HitEffect();
				active = false;
				if (Main.netMode != 1)
				{
					NetMessage.SendData(28, -1, -1, null, whoAmI, -1f);
				}
				return;
			}
			break;
		case 5:
			if (this.ai[1] == 30f)
			{
				SoundEngine.PlaySound(SoundID.DeerclopsScream, base.Center);
			}
			this.ai[1] += 1f;
			haltMovement = true;
			if ((int)this.ai[1] % 4 == 0 && this.ai[1] >= 28f)
			{
				PunchCameraModifier modifier = new PunchCameraModifier(base.Center, (Main.rand.NextFloat() * (MathF.PI * 2f)).ToRotationVector2(), 20f, 6f, 20, 1000f, "Deerclops");
				Main.instance.CameraModifiers.Add(modifier);
			}
			if (this.ai[1] == 30f)
			{
				TargetClosest();
				if (Main.netMode != 1)
				{
					for (int i = 0; i < 6; i++)
					{
						Projectile.RandomizeInsanityShadowFor(Main.player[target], isHostile: true, out var spawnposition, out var spawnvelocity, out var ai, out var ai2);
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), spawnposition, spawnvelocity, 965, num, 0f, Main.myPlayer, ai, ai2);
					}
				}
			}
			if (this.ai[1] >= 60f)
			{
				this.ai[0] = 0f;
				this.ai[1] = 0f;
				netUpdate = true;
			}
			break;
		}
		AI_123_Deerclops_Movement(haltMovement, goHome);
	}

	private bool ShouldRunAway(ref NPCAimedTarget targetData, bool isChasing)
	{
		if (targetData.Type == NPCTargetType.Player)
		{
			Player player = Main.player[target];
			bool zoneSnow = player.ZoneSnow;
			Vector2 other = new Vector2(homeTileX * 16, homeTileY * 16);
			int num = 480;
			zoneSnow |= player.Distance(other) <= (float)num;
			return (player.dead || (!isChasing && !zoneSnow)) | (Distance(player.Center) >= 2400f);
		}
		if (targetData.Type == NPCTargetType.None)
		{
			return true;
		}
		return false;
	}

	private void SpawnPassiveShadowHands(float lifePercent, int shadowHandDamage)
	{
		int num = (int)Utils.Remap(lifePercent, 1f, 0f, 80f, 40f);
		localAI[2] += 1f;
		int num2 = (int)localAI[2];
		if (num2 % num != 0)
		{
			return;
		}
		int num3 = num2 / num;
		if (num2 / num >= 3)
		{
			localAI[2] = 0f;
		}
		for (int i = 0; i < 255; i++)
		{
			if (Boss_CanShootExtraAt(i, num3 % 3, 3, 1200f, alwaysSkipMainTarget: false))
			{
				Projectile.RandomizeInsanityShadowFor(Main.player[i], isHostile: true, out var spawnposition, out var spawnvelocity, out var ai, out var ai2);
				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), spawnposition, spawnvelocity, 965, shadowHandDamage, 0f, Main.myPlayer, ai, ai2);
			}
		}
	}

	private void AI_123_Deerclops_ShootRubbleUp(ref NPCAimedTarget targetData, ref Point sourceTileCoords, int howMany, int distancedByThisManyTiles, float upBiasPerSpike, int whichOne)
	{
		int num = 18;
		int num2 = whichOne * distancedByThisManyTiles;
		for (int i = 0; i < 35; i++)
		{
			int num3 = sourceTileCoords.X + num2 * direction;

```


---

## 🤖 Assistant · 2026-08-19T03:15:37.387Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now compare case 3 (scream) carefully:

Vanilla case 3:
```
if (ai[1] == 30) → sound
ai[1] += 1
halt
if ((int)ai[1] % 4 == 0 && ai[1] >= 28) → punch + player buff check (main myPlayer, not target!) — Main.player[Main.myPlayer], distance < 800, FindBuffIndex(32) == -1
if (ai[1] == 30) → TargetClosest
if (ai[1] >= 60) → reset
```

Ours case 3:
```
if (e.ai1 === 30) { playSfxFiles(SCREAM); e.facing = p && p.cx > e.cx ? 1 : -1; }   // facing set — vanilla does TargetClosest() at ==30 AFTER increment... wait vanilla has TWO separate ai[1]==30 checks: one BEFORE increment (sound) and one AFTER increment (TargetClosest). Both trigger at the same tick (ai1==30 → sound, then increment → 31... wait no: first check `if (this.ai[1] == 30f)` → at tick when ai1 is 30, sound plays; then ai[1] += 1 → 31; then later `if (this.ai[1] == 30f)` — now ai1 is 31, so TargetClosest never fires at the same tick... Actually the second check sees 31. Hmm — so when does the second ==30 fire? It never does! Because ai1 increments by exactly 1 each tick, first check fires at ai1==30, then increment makes 31, second check tests 31≠30. The second ==30 check is dead code?? Wait no — order: 
if (ai[1] == 30) sound;      // ai1 = 30
ai[1] += 1;                   // ai1 = 31
...punch/buff...
if (ai[1] == 30) TargetClosest();   // tests 31 → false, dead
```
Yes — dead code in vanilla (or fires only if ai1 was 29 before the first check... no, first check would be 29≠30). So TargetClosest at case 3 never runs. Funny. Ours sets facing at ai1==30 (approximating TargetClosest). Harmless.

Buff condition: vanilla applies to Main.player[Main.myPlayer] (single local player), requires !dead && active && FindBuffIndex(32)==-1 && distance < 800 && !creativeGodMode. Ours: p && !p.dead && dist < 800 && !p.buffs.has(Slow). ✓ (buffImmune check ~ buffs.has). OK.

case 5 (shadow hands): vanilla at ai[1]==30 (before increment... wait same pattern: `if (ai[1]==30) sound`, then `ai[1]+=1`, punch stuff, then `if (ai[1]==30)` — AGAIN after increment → dead?? No wait — case 5:
```
case 5:
    if (this.ai[1] == 30f) → sound
    this.ai[1] += 1f;
    haltMovement = true;
    if (%4==0 && >=28) punch
    if (this.ai[1] == 30f)  ← AFTER increment: tests 31 → never true??
```
Hold on — for case 5, the second `if (this.ai[1] == 30f)` appears AFTER `ai[1] += 1f` in the code:
```
case 5:
    if (this.ai[1] == 30f) { SoundEngine.PlaySound(...); }
    this.ai[1] += 1f;
    haltMovement = true;
    if ((int)this.ai[1] % 4 == 0 && this.ai[1] >= 28f) { punch }
    if (this.ai[1] == 30f)
    {
        TargetClosest();
        ... spawn 6 hands ...
    }
```
ai[1] incremented from 30 → 31 before the second check → the hand-spawn block NEVER executes?!

Wait wait. Let me re-read. Hmm, `this.ai[1] += 1f;` then later `if (this.ai[1] == 30f)`. If ai[1] was 29 at tick start: first check 29≠30 no sound; increment → 30; punch check: 30%4=2 no; second check: 30 == 30 → TRUE → spawn hands! So the spawn fires on the tick when ai[1] BECOMES 30 (post-increment value 30). And the sound fires the NEXT tick (when ai[1] is 30 at entry). OK so: at tick N (ai1: 29→30): hands spawn, no sound. At tick N+1 (ai1: 30→31): sound. Both around ai1=30. Fine — not dead code. I misread. Same for case 3's TargetClosest (fires when ai1 becomes 30) and sound (fires next tick when ai1 is 30 at entry). And case 7 teleport at `ai[1] == 40` — post-increment check: fires when ai1 becomes 40. And sound at ==30 pre-increment fires next tick. Ours: sound at ai1===30 pre-increment ✓; teleport `if (e.ai1 === 40)` post-increment (ours increments ai1 at line 185 `e.ai1 += 1; halt = true;` before the check at 189) ✓. Ours case 5: spawns hands at ai1===30 pre-increment (line 209: `if (e.ai1 === 30)` before `e.ai1 += 1`). Vanilla spawns post-increment-value-30 → one tick earlier than sound. Ours: sound+hands+facing all at pre-increment 30 (same tick). 1-tick skew, not structural.

case 5 hand damage: vanilla `num` = 15 (the outer `int num = 15`)! `Projectile.NewProjectile(..., 965, num, ...)` → damage 15. Ours DMG_HANDS = 15 ✓. Passive hands: shadowHandDamage = 10 ✓ ours 10 ✓.

SpawnPassiveShadowHands: vanilla: num = Remap(lifePercent, 1→0, 80→40) — at full life 80, at 0 life 40. interval. localAI[2] += 1 each tick (expert only); if localAI[2] % num != 0 return; num3 = localAI[2]/num; if num3 >= 3 → reset localAI[2]=0. Then for players: Boss_CanShootExtraAt(i, num3%3, 3, 1200, false) → spawn hand at that player.

Note: when num3 >= 3 → reset to 0 AND still spawn for num3=3 (num3%3=0)? The reset happens before the loop, so hands spawn with num3=3 on the third interval tick, then counter resets. So bursts of 3 (num3=1,2,3) then reset. Hmm actually first hand at localAI[2]=num (num3=1).

Ours: 
```
const interval = Math.round(80 + (0 - (1 - lifePct)) * 40 || 40);
```
Remap(lifePercent,1,0,80,40): value = 80 + (lifePercent-1)/(0-1)*(40-80) = 80 + (1-lifePct)*40. So at full life: 80; at 0: 40? Wait: Remap(x, 1, 0, 80, 40) maps x=1→80, x=0→40. value = 80 + (x-1)*(-40) = 80 - 40x + 40 = 120 - 40x. At x=1 → 80 ✓; x=0 → 120?? Hmm: Remap(value, a, b, c, d) = if x<a →c; x>b→d; else c + (x-a)/(b-a)*(d-c). a=1,b=0,c=80,d=40. For x in [0,1]: 80 + (x-1)/(0-1)*(40-80) = 80 + (x-1)*(-1)*(-40) = 80 + 40(x-1) = 40x + 40. At x=1 → 80 ✓, x=0 → 40 ✓. OK so interval = 40 + 40*lifePct.

Ours: `80 + (0 - (1 - lifePct)) * 40` = 80 + (lifePct - 1)*40 = 40 + 40*lifePct ✓ same. `|| 40` guard. ✓. But ours uses Math.round; vanilla (int) cast truncates. Minor.

Ours: `e.lai2 += 1; const idx = e.lai2 / interval; if (e.lai2 % interval === 0 && idx < 3 && dist < 1200) spawn(hint = floor(idx)%3); if (idx >= 3) e.lai2 = 0;`

Vanilla: if (localAI[2] % num != 0) return; — so non-multiples return early (no reset check). num3 = localAI[2]/num; if num3 >= 3 → reset. Then spawn loop (for num3=1,2,3 before... wait when num3=3, reset happens and THEN the loop runs spawning num3%3=0 hint). Ours: `idx < 3` gate prevents the third hand (num3=3), then reset when idx>=3. So ours spawns only 2 hands per burst (idx 1,2) vs vanilla 3 (idx 1,2,3). Hmm wait — vanilla num3 = num2 / num where num2 = (int)localAI[2]. If num = 40: localAI[2] hits 40 → num3=1 spawn; 80 → num3=2 spawn; 120 → num3=3 ≥3 → reset localAI[2]=0, and STILL spawns (loop after reset). So vanilla spawns 3 per cycle. Ours: at idx=3: `idx < 3` false → no spawn; `idx >= 3` → reset. So ours spawns 2 per cycle, missing the third hand. Also vanilla's hint = num3 % 3 → 1, 2, 0. Ours hint = floor(idx)%3 → 1, 2 (never 0). Structural-ish: expert passive hands fire 2/3 of vanilla cadence. Medium-low severity but it's an expert-branch count error — audit dimension "专家分支漏". I'd report as CONFIRMED (medium confidence on severity, high on the diff).

Wait, also vanilla's `for (int i = 0; i < 255; i++)` loops all players with Boss_CanShootExtraAt(i, num3%3, 3, 1200f, alwaysSkipMainTarget:false) — in single player, i=0 is the main player; Boss_CanShootExtraAt(main target...) with alwaysSkipMainTarget:false → returns true if within 1200. So single player: 1 hand per interval. Ours approximates with distance < 1200 ✓.

Now case 6 (goHome). Vanilla:
```
TargetClosest(faceTarget: false)
if netMode != 1:
    if !ShouldRunAway(isChasing:false) → ai0=0, reset, break
    if timeLeft <= 0 → ai0=8, reset, break
goHome = true
ai[1] += 1
other = home px
flag2 = Top.Y > other.Y + 1600   (deeper than home by 1600)
num4 = Distance(other) < 1020
num5 = ai[1] % 600
if (num4 && num5 < 420) halt = true
flag3 = false
if (flag2 && ai[1] >= 300) flag3 = true
if (!num4 && ai[1] >= 1500) flag3 = true
if flag3 → ai0=7 reset
```

Ours case 6:
```
if (p && !p.dead && !shouldRunAway(...false...)) { ai0=0; ... break; }
if (e.despawnTimer <= 0) { ai0 = 8; ... break; }
goHome = true; ai1 += 1;
const aboveLine = e.y < homePx.y + 1600;    // Top.Y > other.Y+1600 → deeper. ours: aboveLine = e.y < homeY+1600 (NOT deeper) — then uses `!aboveLine && e.ai1 >= 300` = deeper && ≥300 ✓
const nearHome = dist < 1020 ✓
if (nearHome && ai1 % 600 < 420) halt ✓
if ((!aboveLine && ai1 >= 300) || (!nearHome && ai1 >= 1500)) → ai0=7 ✓
```
✓ matches. Note ours' first check `p && !p.dead && !shouldRunAway` — vanilla ShouldRunAway returns true if player.dead etc.; !ShouldRunAway covers it; ours adds redundant p check fine. But vanilla has the timeLeft check nested inside netMode!=1 — fine.

One nuance: vanilla case 6 gate `if (Main.netMode != 1)` wraps both transitions; client skips → single-player equivalent fine.

Case 0 (chase):
Vanilla checks in order:
1. |dx|<120 && flag5 && vy==0 && localAI[1]>=2 → state 4 (both sides)
2. |dx|<120 && flag5 && vy==0 && flag4 → state 1 (forward), localAI[1] += 1
3. vy==0 && vx!=0 && ai1>=240 → state 2
4. vy==0 && vx==0 && ai1>=90 → state 5
5. vy==0 && ai1>=120 && flag9(!Slow) && |dx|>100 → state 3

Ours matches order and conditions. flag4 = |dx| >= |dy|*0.6 || len<48 ✓ ours facingX. flag5 = dy <= 100+p.h && dy >= -200 ✓ ours nearVert uses p.h ✓. 

BUT: vanilla case 0 begins with TargetClosest() then ShouldRunAway check → state 6. Ours: `if (!p || p.dead || shouldRunAway(...true))` → 6 ✓.

Also vector = base.Bottom + (0,-32) — ours `vy = e.y + e.h - 32` ✓. ClosestPointInRect on target hitbox ✓ ours clamps vx,vy into [p.x,p.x+p.w]×[p.y,p.y+p.h] ✓.

Case 1: forward spikes with slot 1 ✓ ≥80 → 0 ✓. Vanilla case 1: no TargetClosest. Ours none ✓.

Case 4: vanilla has TargetClosest() each tick; ours doesn't (only initial facing from movement). Minor.

Case 2 (rubble): vanilla num8=4, num9=32; sounds at 12 and 32 ✓ ours. sourceTileCoords = Top.ToTileCoordinates() → (Center.X tile? No — Top = position.Y). base.Top = position (top-left? Top is position, i.e., top-left corner X = position.X). Point = (position.X/16, position.Y/16). Then X += direction*3, Y -= 10.

Ours: `srcX = floor(e.cx / TILE) + e.facing * 3; srcY = floor(e.y / TILE) - 10;` — vanilla uses position.X (left edge) not Center.X! Hmm: `base.Top.ToTileCoordinates()` — Top property = new Vector2(position.X, position.Y)? Actually NPC.Top = position + (0,0)? In Terraria Entity: Top => new Vector2(Center.X - width/2, position.Y) = position (top-left). ToTileCoordinates of a Vector2 gives (int)(x/16), (int)(y/16) — hmm actually Vector2.ToTileCoordinates() → Point((int)(X/16f), (int)(Y/16f))? There might be flooring. So srcX vanilla = position.X/16 (left edge), ours = cx/16 (center). Deerclops width? SetDefaults for 668... width maybe 70? offset diff = width/2 = ~2 tiles. Minor numeric noise — I'll skip or note as minor. Actually the audit says "抓结构性偏差,不是数值噪音" — 2-tile source offset is noise-ish. Skip.

Camera punch at num11==0: vanilla (0,-1) 20f,6f,30 frames ✓ ours punch(0,-1,30) ✓.

Rubble count: num10=20, distanced=1, upBias=200. Loop j from num13 to num14 (<num10): num12=1 → 1 per tick, 20 total ✓ ours.

End at ai1>=60 ✓.

Case 7: teleport: `base.Bottom = new Vector2(homeTileX*16, homeTileY*16)` — sets BOTTOM to home tile pos. Ours: `e.x = homeX*TILE - e.w/2; e.y = homeY*TILE - e.h;` → bottom = homeY*TILE ✓ center X ✓. Also TargetClosest before (ours sets facing) ✓.

Case 8: life=-1, HitEffect, active=false → despawn without loot. Ours: hp=-1, dead=true. ✓ (assuming engine treats dead without loot; they set hp=-1 to signal no-drop presumably).

Now lai3 clamp: vanilla Clamp(localAI[3] + flag.ToDirectionInt(), 0, 30) — clamped to [0,30]. flag = Distance(targetData.Center) >= 450. ToDirectionInt: true→1, false→-1.

Ours: `e.lai3 = Math.max(-10, Math.min(30, e.lai3 + (far ? 1 : -1)))` — lower clamp -10 (documented: to let case -1 set -10 and case -1 assigns -10 anyway...). Vanilla clamps at 0 lower. But then case -1 sets localAI[3] = -10f explicitly (overriding). Then subsequent ticks clamp(−10+1, 0, 30) → 0. Hmm: vanilla entry state -1: lai3 = -10; next tick lai3 = clamp(-10 + dir, 0, 30) → if far: clamp(-9,0,30) = 0; if near: clamp(-11,0,30)=0. So vanilla's -10 decays to 0 immediately. Ours keeps -10 floor so it climbs -9, -8... meaning after entry, lai3 needs more ticks to reach 30?? Vanilla: lai3=0 → needs 30 ticks far. Ours: lai3=-10 → 40 ticks. Also `dontTakeDamage = lai3 >= 30` — with -10 floor, during entry walking it takes longer to become invulnerable. Also our `far` requires `!p.dead` — vanilla Distance(targetData.Center) with no target → targetData.Center for None type = ? Probably Vector2.Zero → distance huge → >= 450 true → lai3 climbs even without target. Ours: far = p != null && !p.dead && ... → when no player, far=false → lai3 decays. Hmm. Vanilla with no player: GetTargetData() Type None — Center property likely returns... unclear. Minor.

More important: ours `e.dontTakeDamage = e.lai3 >= 30` — vanilla `dontTakeDamage = localAI[3] >= 30f` ✓. Distance >= 450 ✓ (Distance(targetData.Center) — NPC.Distance = distance from Center to other ✓ ours hypot from e.cx,cy to p.cx,cy ✓).

Dust: vanilla `Main.rand.NextFloat() * num2 * 3` while > 0: spawn dust 109 ✓ ours approximates ✓.

timeLeft: vanilla timeLeft = 86400 on home init; `timeLeft -= Main.dayRate` each tick. Ours despawnTimer = 86400, decrement 1 per tick. dayRate is normally 1 (master mode day rate faster?). Main.dayRate = 1 normally. ✓ close enough.

Note: vanilla home init condition `homeTileX == -1 && homeTileY == -1`; ours `if (e.ai2 === 0 && e.ai3 === 0)` — if home tile X or Y happens to be 0... unlikely. Fine.

Now Movement. Read vanilla 44957-45141 — I need the rest of the helpers too (MakeSpikesForward/BothSides/TryMakingSpike/FindBestY 44776-44955, ShootRubbleUp continuation). Let me read 44760-45141.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:37.813Z · glm-x-preview-260804

```
主状态机已对上大半。继续读辅助函数与 Movement(44760-45141)。
```


---

## 🤖 Assistant · 2026-08-19T03:15:38.269Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '44760,45141p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read Deerclops helpers and Movement"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:38.322Z

**📎 ToolResult**

```
			int num3 = sourceTileCoords.X + num2 * direction;
			int num4 = sourceTileCoords.Y + i;
			if (WorldGen.SolidTile(num3, num4))
			{
				Vector2 vector = targetData.Center + new Vector2(num2 * direction * 20, (0f - upBiasPerSpike) * (float)howMany + (float)num2 * upBiasPerSpike / (float)distancedByThisManyTiles);
				Vector2 vector2 = new Vector2(num3 * 16 + 8, num4 * 16 + 8);
				Vector2 vector3 = (vector - vector2).SafeNormalize(-Vector2.UnitY);
				vector3 = new Vector2(0f, -1f).RotatedBy((float)(whichOne * direction) * 0.7f * (MathF.PI / 4f / (float)howMany));
				int num5 = Main.rand.Next(Main.projFrames[962] * 4);
				num5 = 6 + Main.rand.Next(6);
				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), new Vector2(num3 * 16 + 8, num4 * 16 - 8), vector3 * (8f + Main.rand.NextFloat() * 8f), 962, num, 0f, Main.myPlayer, 0f, num5);
				break;
			}
		}
	}

	private void AI_123_Deerclops_MakeSpikesForward(int AISLOT_PhaseCounter, NPCAimedTarget targetData)
	{
		int num = 9;
		int num2 = 4;
		if (Main.netMode == 1)
		{
			return;
		}
		int num3 = num * num2;
		if (!(ai[AISLOT_PhaseCounter] < (float)num3))
		{
			Point sourceTileCoords = base.Bottom.ToTileCoordinates();
			int num4 = 20;
			int num5 = 1;
			sourceTileCoords.X += direction * 3;
			int num6 = (int)ai[AISLOT_PhaseCounter] - num3;
			if (num6 == 0)
			{
				PunchCameraModifier modifier = new PunchCameraModifier(base.Center, new Vector2(0f, 1f), 20f, 6f, 30, 1000f, "Deerclops");
				Main.instance.CameraModifiers.Add(modifier);
			}
			int num7 = 4;
			int num8 = num6 / num7 * num7;
			int num9 = num8 + num7;
			if (num6 % num7 != 0)
			{
				num9 = num8;
			}
			for (int i = num8; i < num9 && i < num4; i++)
			{
				int xOffset = i * num5;
				AI_123_Deerclops_TryMakingSpike(ref sourceTileCoords, direction, num4, i, xOffset);
			}
		}
	}

	private void AI_123_Deerclops_MakeSpikesBothSides(int AISLOT_PhaseCounter, NPCAimedTarget targetData)
	{
		if (Main.netMode == 1)
		{
			return;
		}
		int num = 56;
		if (!(ai[AISLOT_PhaseCounter] < (float)num))
		{
			Point sourceTileCoords = base.Bottom.ToTileCoordinates();
			int num2 = 15;
			int num3 = 1;
			int num4 = (int)ai[AISLOT_PhaseCounter] - num;
			if (num4 == 0)
			{
				PunchCameraModifier modifier = new PunchCameraModifier(base.Center, new Vector2(0f, 1f), 20f, 6f, 30, 1000f, "Deerclops");
				Main.instance.CameraModifiers.Add(modifier);
			}
			int num5 = 2;
			int num6 = num4 / num5 * num5;
			int num7 = num6 + num5;
			if (num4 % num5 != 0)
			{
				num7 = num6;
			}
			for (int i = num6; i >= 0 && i < num7 && i < num2; i++)
			{
				int xOffset = i * num3;
				AI_123_Deerclops_TryMakingSpike(ref sourceTileCoords, direction, num2, -i, xOffset);
				AI_123_Deerclops_TryMakingSpike(ref sourceTileCoords, -direction, num2, -i, xOffset);
			}
		}
	}

	public static bool IsADeerclopsNearScreen()
	{
		return npcsFoundForCheckActive[668];
	}

	private void AI_123_Deerclops_FindSpotToSpawnSpike(int howMany, int whichOne, ref int x, ref int y)
	{
		if (WorldGen.ActiveAndWalkableTile(x, y))
		{
			return;
		}
		Rectangle rectangle = targetRect;
		int num = rectangle.Center.X / 16;
		int num2 = (rectangle.Bottom - 16) / 16;
		int num3 = ((num2 - y > 0) ? 1 : (-1));
		int num4 = y;
		for (int i = 1; i <= 10; i++)
		{
			int num5 = y + num3 * i;
			if (num5 >= 20 && num5 <= Main.maxTilesY - 20 && WorldGen.ActiveAndWalkableTile(x, num5))
			{
				num4 = num5;
			}
		}
		if (num4 != y)
		{
			y = num4;
			return;
		}
		y = (int)MathHelper.Lerp(num2, y, (float)Math.Abs(num - x) * 0.1f);
		for (int j = 0; j < 4; j++)
		{
			int num6 = y + j;
			if (num6 >= 20 && num6 <= Main.maxTilesY - 20 && WorldGen.ActiveAndWalkableTile(x, num6))
			{
				y = num6;
				break;
			}
		}
	}

	private void AI_123_Deerclops_TryMakingSpike(ref Point sourceTileCoords, int dir, int howMany, int whichOne, int xOffset)
	{
		int num = 13;
		int num2 = sourceTileCoords.X + xOffset * dir;
		int num3 = AI_123_Deerclops_TryMakingSpike_FindBestY(ref sourceTileCoords, num2);
		if (WorldGen.ActiveAndWalkableTile(num2, num3))
		{
			Vector2 vector = new Vector2(num2 * 16 + 8, num3 * 16 - 8);
			Vector2 vector2 = new Vector2(0f, -1f).RotatedBy((float)(whichOne * dir) * 0.7f * (MathF.PI / 4f / (float)howMany));
			Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector, vector2, 961, num, 0f, Main.myPlayer, 0f, 0.1f + Main.rand.NextFloat() * 0.1f + (float)xOffset * 1.1f / (float)howMany);
		}
	}

	private int AI_123_Deerclops_TryMakingSpike_FindBestY(ref Point sourceTileCoords, int x)
	{
		int num = sourceTileCoords.Y;
		NPCAimedTarget targetData = GetTargetData();
		if (!targetData.Invalid)
		{
			Rectangle hitbox = targetData.Hitbox;
			Vector2 vector = new Vector2(hitbox.Center.X, hitbox.Bottom);
			int num2 = (int)(vector.Y / 16f);
			int num3 = Math.Sign(num2 - num);
			int num4 = num2 + num3 * 15;
			int? num5 = null;
			float num6 = float.PositiveInfinity;
			for (int i = num; i != num4; i += num3)
			{
				if (WorldGen.ActiveAndWalkableTile(x, i))
				{
					float num7 = new Point(x, i).ToWorldCoordinates().Distance(vector);
					if (!num5.HasValue || !(num7 >= num6))
					{
						num5 = i;
						num6 = num7;
					}
				}
			}
			if (num5.HasValue)
			{
				num = num5.Value;
			}
		}
		for (int j = 0; j < 20; j++)
		{
			if (num < 10)
			{
				break;
			}
			if (!WorldGen.SolidTile(x, num))
			{
				break;
			}
			num--;
		}
		for (int k = 0; k < 20; k++)
		{
			if (num > Main.maxTilesY - 10)
			{
				break;
			}
			if (WorldGen.ActiveAndWalkableTile(x, num))
			{
				break;
			}
			num++;
		}
		return num;
	}

	private void AI_123_Deerclops_Movement(bool haltMovement, bool goHome)
	{
		float num = (float)life / (float)lifeMax;
		float num2 = 1f - num;
		float num3 = 3.5f + 1f * num2;
		float num4 = 4f;
		float num5 = -0.4f;
		float min = -8f;
		float num6 = 0.4f;
		Rectangle rectangle = GetTargetData().Hitbox;
		if (goHome)
		{
			rectangle = new Rectangle(homeTileX * 16, homeTileY * 16, 16, 16);
			if (Distance(rectangle.Center.ToVector2()) < 240f)
			{
				rectangle.X = (int)(base.Center.X + (float)(160 * direction));
			}
		}
		float num7 = (float)rectangle.Center.X - base.Center.X;
		float num8 = Math.Abs(num7);
		if (goHome && num7 != 0f)
		{
			direction = (spriteDirection = Math.Sign(num7));
		}
		bool flag = num8 < 80f;
		bool flag2 = flag || haltMovement;
		if (ai[0] == -1f)
		{
			num7 = 5f;
			num3 = 5.35f;
			flag2 = false;
		}
		if (flag2)
		{
			velocity.X *= 0.9f;
			if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
			{
				velocity.X = 0f;
			}
		}
		else
		{
			int num9 = Math.Sign(num7);
			velocity.X = MathHelper.Lerp(velocity.X, (float)num9 * num3, 1f / num4);
		}
		int num10 = 40;
		int num11 = 20;
		int num12 = 0;
		Vector2 vector = new Vector2(base.Center.X - (float)(num10 / 2), position.Y + (float)height - (float)num11 + (float)num12);
		bool num13 = vector.X < (float)rectangle.X && vector.X + (float)width > (float)(rectangle.X + rectangle.Width);
		bool flag3 = vector.Y + (float)num11 < (float)(rectangle.Y + rectangle.Height - 16);
		bool flag4 = ai[0] == 7f;
		bool acceptTopSurfaces = base.Bottom.Y >= (float)rectangle.Top && !flag4;
		bool flag5 = Collision.SolidCollision(vector, num10, num11, acceptTopSurfaces);
		bool flag6 = Collision.SolidCollision(vector, num10, num11 - 4, acceptTopSurfaces);
		bool flag7 = !Collision.SolidCollision(vector + new Vector2(num10 * direction, 0f), 16, 80, acceptTopSurfaces);
		float num14 = 8f;
		if (flag5 || flag6)
		{
			localAI[0] = 0f;
		}
		if (flag4)
		{
			velocity.Y = -0.1f;
		}
		if ((num13 || flag) && flag3)
		{
			velocity.Y = MathHelper.Clamp(velocity.Y + num6 * 2f, 0.001f, 16f);
		}
		else if (flag5 && !flag6)
		{
			velocity.Y = 0f;
		}
		else if (flag5)
		{
			velocity.Y = MathHelper.Clamp(velocity.Y + num5, min, 0f);
		}
		else if (velocity.Y == 0f && flag7)
		{
			velocity.Y = 0f - num14;
			localAI[0] = 1f;
		}
		else
		{
			velocity.Y = MathHelper.Clamp(velocity.Y + num6, 0f - num14, 16f);
		}
	}

	private void AI_124_DeerclopsLeg()
	{
		int num = (int)ai[0];
		if (num < 0 || num > Main.maxNPCs)
		{
			active = false;
			if (Main.netMode != 1)
			{
				NetMessage.SendData(23, -1, -1, null, whoAmI);
			}
			return;
		}
		NPC nPC = Main.npc[num];
		if (!nPC.active || nPC.type != 668)
		{
			active = false;
			if (Main.netMode != 1)
			{
				NetMessage.SendData(23, -1, -1, null, whoAmI);
			}
			return;
		}
		NPCAimedTarget targetData = nPC.GetTargetData();
		Vector2 vector = targetData.Center - base.Center;
		float num2 = targetData.Center.X - (float)(width / 2);
		int num3 = Math.Sign(num2 - position.X);
		float val = Math.Abs(num2 - position.X);
		float num4 = Math.Min(50f, val);
		float num5 = num2 + (float)(-num3) * num4;
		Math.Abs(vector.X);
		if (Math.Abs(num5 - base.Center.X) >= 30f && localAI[0] == 0f)
		{
			localAI[0] = 1f;
		}
		float num6 = 4f;
		float num7 = 30f;
		if (localAI[0] < 0f)
		{
			localAI[0] += 1f;
		}
		if (localAI[0] > 0f)
		{
			localAI[0] += 1f;
			if (localAI[0] >= num7)
			{
				localAI[0] = 0f - num6;
			}
		}
		int num8 = ((ai[1] != 0f) ? 1 : (-1));
		if (localAI[0] > 0f)
		{
			Vector2 vector2 = new Vector2(num8 * 14, -20f);
			Vector2 searchStartPositionInWorld = nPC.Bottom + vector2 + new Vector2(0f, 30f);
			int searchRange = 16;
			int tilesTraveled = 0;
			float? num9 = TryFindingFloor(searchStartPositionInWorld, searchRange, out tilesTraveled);
			float amount = 1f / 3f;
			Vector2 value = new Vector2(searchStartPositionInWorld.X, searchStartPositionInWorld.Y + 100f);
			float num10 = localAI[0] / num7;
			if (num9.HasValue && tilesTraveled > 2)
			{
				new Vector2(searchStartPositionInWorld.X, num9.Value * 16f);
				value = new Vector2(searchStartPositionInWorld.X, num9.Value * 16f);
				amount = num10;
			}
			value.Y -= (1f - num10) * 30f;
			Vector2 bottom = Vector2.Lerp(base.Bottom, value, amount);
			base.Bottom = bottom;
		}
		int num11 = num8;
		if (Math.Abs(vector.X) > 30f)
		{
			num11 = Math.Sign(vector.X);
		}
		spriteDirection = -num11;
	}

	private static float? TryFindingFloor(Vector2 searchStartPositionInWorld, int searchRange, out int tilesTraveled)
	{
		Point point = searchStartPositionInWorld.ToTileCoordinates();
		int x = point.X;
		for (int i = point.Y; i < point.Y + searchRange; i++)
		{
			if (Main.tile[x, i] == null)
			{
				Main.tile[x, i] = new Tile();
			}
			if (Main.tile[x, i].nactive() && Main.tileSolid[Main.tile[x, i].type])
			{
				tilesTraveled = i - point.Y;
				return i;
			}
		}
		tilesTraveled = 0;
		return null;
	}

```


---

## 🤖 Assistant · 2026-08-19T03:17:14.363Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now compare Deerclops details:

**ShootRubbleUp velocity** — IMPORTANT. Vanilla:
```
Vector2 vector = targetData.Center + new Vector2(num2 * direction * 20, -upBiasPerSpike * howMany + num2 * upBiasPerSpike / distancedByThisManyTiles);
Vector2 vector2 = new Vector2(num3 * 16 + 8, num4 * 16 + 8);
Vector2 vector3 = (vector - vector2).SafeNormalize(-Vector2.UnitY);   // computed then OVERWRITTEN:
vector3 = new Vector2(0, -1).RotatedBy((whichOne * direction) * 0.7 * (π/4 / howMany));
Projectile.NewProjectile(pos, vector3 * (8 + rand*8), 962, damage 18, ..., 0f, num5);
```
So velocity = unit vector rotated from up by (whichOne*direction)*0.7*(π/4/howMany) × (8+rand8). Ours: `ang = -π/2 + whichOne * e.facing * 0.7 * (π/4/howMany); spd = 8 + rand*8` ✓ matches (note: vanilla `whichOne * direction` where whichOne = j (0..19) — ours `whichOne * e.facing` ✓ since ours passes e.facing implicitly. Wait ours: `const ang = -Math.PI / 2 + whichOne * e.facing * 0.7 * (Math.PI / 4 / howMany);` ✓.

Frame num5: `int num5 = Main.rand.Next(Main.projFrames[962] * 4); num5 = 6 + Main.rand.Next(6);` — the first assignment is dead; num5 = 6 + rand(6) → 6..11! Our comment claims: "ai[1] = rand(projFrames[962] × 4) = rand(12)——3×4 网格全 12 格随机(NPC.cs:44768-44770; 此前误写 6..11 只取下两行)". But the actual vanilla code OVERRIDES num5 with `6 + Main.rand.Next(6)` — so vanilla IS 6..11! Our comment says the opposite — they "fixed" it to rand(12) based on the dead first line, but the SECOND line `num5 = 6 + Main.rand.Next(6)` is the live one! Let me re-read:

```
int num5 = Main.rand.Next(Main.projFrames[962] * 4);
num5 = 6 + Main.rand.Next(6);
```
Yes — decompiled shows two assignments; the second wins. projFrames[962]... Main.projFrames[962] = 3 presumably → rand(12) first, then overwritten by 6+rand(6) = 6..11. So vanilla frame = 6..11 (bottom two rows of the 3×4 grid). OURS: `Math.floor(Math.random() * 12)` → 0..11 (all 12). The comment claims they deliberately changed FROM 6..11 TO rand(12), citing the dead first assignment. That's a CONFIRMED deviation — they misread dead code. Confidence: high (I read both lines directly at 44768-44769).

Wait, let me get exact line numbers. The ShootRubbleUp function starts at 44754-ish. The lines: from my sed output starting 44760:
```
44760: int num3 = sourceTileCoords.X + num2 * direction;
44761: int num4 = sourceTileCoords.Y + i;
44762: if (WorldGen.SolidTile(num3, num4))
44763: {
44764:     Vector2 vector = targetData.Center + ...
44765:     Vector2 vector2 = ...
44766:     Vector2 vector3 = (vector - vector2).SafeNormalize...
44767:     vector3 = new Vector2(0f, -1f).RotatedBy(...)
44768:     int num5 = Main.rand.Next(Main.projFrames[962] * 4);
44769:     num5 = 6 + Main.rand.Next(6);
44770:     Projectile.NewProjectile(...)
```
Roughly. Let me verify exact line numbers with grep. I'll do that.

Also rubble spawn Y: vanilla `new Vector2(num3 * 16 + 8, num4 * 16 - 8)` — top of solid tile. Ours: `y * TILE - 8` ✓. But ours finds solid starting from srcY going DOWN 35 (i from 0..34, `y = srcY + i`); vanilla loop `num4 = sourceTileCoords.Y + i` for i 0..34 → also downward ✓. Vanilla breaks on first WorldGen.SolidTile ✓ ours `if (!solidAt) continue; ... break;` ✓.

Rubble projectile damage: vanilla `num` in ShootRubbleUp... wait, ShootRubbleUp uses `num` for damage? Looking: `Projectile.NewProjectile(..., 962, num, 0f, Main.myPlayer, 0f, num5)` — what's `num` in that scope? ShootRubbleUp starts `private void AI_123_Deerclops_ShootRubbleUp(ref NPCAimedTarget targetData, ref Point sourceTileCoords, int howMany, int distancedByThisManyTiles, float upBiasPerSpike, int whichOne)`. Inside: `int num = 18;`? Hmm — the sed output at 44754+ — the function signature was at the end of the previous read (44338-44530 output ended with the function start):
```
private void AI_123_Deerclops_ShootRubbleUp(...)
{
    int num = 18;
    int num2 = whichOne * distancedByThisManyTiles;
    for (int i = 0; i < 35; i++)
    {
        int num3 = sourceTileCoords.X + num2 * direction;
```
From the 44338-44530 output, the last lines were:
```
	private void AI_123_Deerclops_ShootRubbleUp(ref NPCAimedTarget targetData, ref Point sourceTileCoords, int howMany, int distancedByThisManyTiles, float upBiasPerSpike, int whichOne)
	{
		int num = 18;
		int num2 = whichOne * distancedByThisManyTiles;
		for (int i = 0; i < 35; i++)
		{
			int num3 = sourceTileCoords.X + num2 * direction;
```
Yes damage 18 ✓ ours DMG 18 ✓.

**MakeSpikesForward**: vanilla num=9, num2=4 → num3 = 36 lead ✓ ours LEAD=36. Every 4 ticks one spike (num7=4), 20 total ✓. xOffset = i * 1. TryMakingSpike(dir=direction, howMany=20, whichOne=i, xOffset=i). Ours: `tryMakingSpike(game, e, p, srcX, srcY, e.facing, 20, i, i)` ✓.

Vanilla spike origin: `base.Bottom.ToTileCoordinates()` then X += direction*3. Bottom.ToTileCoordinates: Bottom = Center.X, position.Y+height → (Center.X/16, bottom/16). Ours: `srcX = floor((e.x + e.w / 2) / TILE) + e.facing * 3` ✓ (uses center ✓ here). `srcY = floor((e.y + e.h) / TILE)` ✓.

Spike velocity angle: `(0,-1).RotatedBy(whichOne * dir * 0.7 * (π/4/howMany))` — ours: `-π/2 + whichOne * dir * 0.7 * (π/4/howMany)` ✓. Note BOTH-sides passes whichOne = -i, dir = ±direction ✓ ours passes (-i, i) and (-i, i) with dir ±facing... ours: `tryMakingSpike(game, e, p, srcX, srcY, e.facing, 15, -i, i); tryMakingSpike(..., -e.facing, 15, -i, i);` — vanilla: `TryMakingSpike(ref stc, direction, num2, -i, xOffset=i)` and `TryMakingSpike(ref stc, -direction, num2, -i, i)`. ✓ match (whichOne=-i, xOffset=i).

x offset: `num2 = sourceTileCoords.X + xOffset * dir` ✓ ours `x = srcX + xOffset * dir` ✓.

ai1 param: `0.1f + NextFloat()*0.1f + xOffset * 1.1f / howMany` ✓ ours.

Damage 13 ✓. proj 961 ✓.

**BothSides lead 56** ✓; every 2 ticks; 15 each ✓. Loop `for (int i = num6; i >= 0 && i < num7 && i < num2; i++)` ✓ ours `for (let i = step; i >= 0 && i < hi && i < 15; i++)` ✓.

**FindBestY** — compare vanilla vs ours:
Vanilla:
```
num = sourceTileCoords.Y
targetData valid → 
    vector = (hitbox.Center.X, hitbox.Bottom)
    num2 = (int)(vector.Y / 16)     // player bottom tile
    num3 = Sign(num2 - num)
    num4 = num2 + num3 * 15         // end
    scan i from num to num4 (exclusive), find walkable closest to vector (distance in world coords)
    if found → num = best
then 20 up: if num<10 break; if !SolidTile break; num--
then 20 down: if num > maxTilesY-10 break; if ActiveAndWalkable break; num++
```
Ours findBestSpikeY:
```
let y = srcY
if p: tBottom = floor((p.y+p.h)/16); sgn = sign(tBottom - srcY); end = tBottom + sgn*15
  scan, distance = |i*16+8 - (p.y+p.h)| — vanilla: new Point(x,i).ToWorldCoordinates().Distance(vector) — ToWorldCoordinates default = center (x*16+8, y*16+8). Distance from (x*16+8, i*16+8) to (hitboxCenter.X, hitbox.Bottom). Ours only vertical distance |i*16+8 - player bottom| — x constant anyway since same column... vanilla includes the X offset which is constant across candidates so irrelevant for comparison. ✓ fine.
up/down loops ✓ (num<10 → ours `y < 10`; maxTilesY-10 → `y > h-10` ✓).
```
✓ Good.

Note: vanilla `if (!targetData.Invalid)` — includes any target; ours `if (p && !p.dead)` ✓.

**Movement** — vanilla:
- num3 = 3.5 + 1*(1-lifeFrac) ✓ ours.
- rectangle = target hitbox; goHome → home rect; if Distance(rect center) < 240 → rectangle.X = Center.X + 160*direction ✓ ours.
- num7 = rect.Center.X - Center.X; adx; goHome → direction = sign ✓ ours.
- flag = adx < 80 ✓ nearX.
- flag2 = flag || halt ✓.
- ai[0]==-1: num7 = 5, num3 = 5.35, flag2 = false ✓ ours (dir=5, spd=5.35, stop=false).
- flag2 → vx *= 0.9; |vx|<0.1 → 0 ✓ ours.
- else: vx = Lerp(vx, sign(num7)*num3, 1/4) ✓ ours `(Math.sign(dir) * spd - e.vx) / 4`.

Hmm — one nuance: ours `e.vx += (Math.sign(dir) * spd - e.vx) / 4;` = Lerp ✓.

- Probe: vector = (Center.X - 20, position.Y + height - 20) ✓ ours bx = e.cx - 20, by = e.y + e.h - 20.
- num13 (straddle): vector.X < rect.X && vector.X + width > rect.X + rect.Width ✓ ours.
- flag3: vector.Y + 20 < rect.Y + rect.Height - 16 ✓ ours `by + 20 < ty + th - 16`.
- flag4: ai[0]==7 ✓ teleporting.
- acceptTopSurfaces = Bottom.Y >= rect.Top && !flag4 — OURS MISSES THIS. Vanilla's SolidCollision calls use acceptTopSurfaces: when boss bottom is at/below target top and not teleporting, top surfaces (platforms/half blocks) count as solid. Ours' solidCollisionPx ignores acceptTopSurfaces entirely (treats all solids incl. platforms? depends on st.isSolid semantics — does isSolid include platforms? In this repo, isSolid probably excludes platforms (tileSolid excludes SolidTop). acceptTopSurfaces=true ADDS platforms to the collision test). So ours' ground probes never count platforms as ground. Effect: deerclops standing on platforms (snow biomes have... mostly not) — minor. Also flag4 (teleporting) → acceptTopSurfaces false — only affects platform counting. Low severity; skip or minor note.
- flag5 = SolidCollision(vector, 40, 20, acceptTopSurfaces) → ours `ground = solidCollisionPx(game, bx, by, 40, 20)` ✓.
- flag6 = SolidCollision(vector, 40, 16) → ours groundHigh (40,16) ✓.
- flag7 = !SolidCollision(vector + (40*direction, 0), 16, 80) → ours openAhead = !solidCollisionPx(game, bx + 40 * e.facing, by, 16, 80) ✓.
- localAI[0] = 0 if flag5||flag6 ✓ ours lai0=0.
- flag4 → vy = -0.1 ✓ ours.
- (num13||flag) && flag3 → vy = Clamp(vy + 0.4*2, 0.001, 16) ✓ ours `Math.min(Math.max(e.vy + 0.8, 0.001), 16)` ✓.
- flag5 && !flag6 → vy = 0 ✓.
- flag5 → vy = Clamp(vy - 0.4, -8, 0) ✓ ours.
- vy==0 && flag7 → vy = -8, lai0=1 ✓.
- else vy = Clamp(vy + 0.4, -8, 16) ✓.

Movement ✓ structurally.

Note: ours integrates `e.x += e.vx; e.y += e.vy;` — vanilla's movement integration happens in the shared UpdateNPC (position += velocity). ✓.

**Case -1 entry**: ours `case -1: e.lai3 = -10; break;` ✓ vanilla.

**timeLeft → ai0=8**: ✓.

**Despawn on player-dead**: vanilla case 0 → ShouldRunAway true (player.dead) → case 6 (go home), NOT despawn immediately ✓ ours.

Now the AI_124_DeerclopsLeg — legs NPC (visual). Ours doesn't implement legs (668's legs are NPCs 669/670? deerclops legs). The task focuses on the main AI; legs are drawing appendages. Not in our file; presumably Renderer handles. Skip (visual).

**Spike projectile (961)**: ours life=20 with life<=0 → dead. Vanilla AI_157 for 961: num9=20? Comment says ":48432-48567 type==961 段". The task doesn't require auditing projectiles deeply, but AI_157's lifetime — the spike grows [0,10) opacity+0.1 then [10,20) opacity-0.2, then dead. Ours life=20 decrements before... `if (--this.life <= 0) dead` then `was === 0` first-frame check. Fine-ish. Not core.

One important check — the spike projectile should NOT deal damage while... vanilla 961 hostile contact damage full window; ours `opacity > 0.05` gate. Fine.

Now — **expert passive shadow hands count** (2 vs 3 per cycle): let me recheck vanilla:
```
int num = (int)Remap(lifePercent, 1, 0, 80, 40);
localAI[2] += 1;
int num2 = (int)localAI[2];
if (num2 % num != 0) return;
int num3 = num2 / num;
if (num2 / num >= 3) localAI[2] = 0;
for players... Boss_CanShootExtraAt(i, num3 % 3, 3, 1200, false) → spawn
```
Sequence with num=40 (half life): localAI[2]: 40 → num3=1, spawn hint 1. 80 → num3=2, spawn hint 2. 120 → num3=3 → reset localAI[2]=0, spawn hint 0. Then counts from 0 again → 40 → num3=1... So cycle = 3 hands (hints 1,2,0) every 3×40=120 ticks. Ours:
```
e.lai2 += 1; idx = e.lai2 / interval;
if (e.lai2 % interval === 0 && idx < 3 && dist < 1200) spawn(hint = floor(idx)%3);
if (idx >= 3) e.lai2 = 0;
```
At interval multiples: 40 → idx 1 spawn; 80 → idx 2 spawn; 120 → idx 3: no spawn, reset. So ours = 2 hands per cycle (hints 1,2), missing hint-0 hand. CONFIRMED expert-branch deviation (33% fewer passive hands). Also ours gates spawn on distance < 1200 INSIDE the modulo check; vanilla Boss_CanShootExtraAt includes the 1200 radius ✓ equivalent-ish.

Also vanilla interval: Remap clamp — for lifePercent exactly 1 → 80; ours formula ✓. But vanilla `(int)` truncation; ours Math.round. Minor.

Also — vanilla resets localAI[2]=0 when NOT expert (case `if (!expertMode) localAI[2] = 0`). Ours: else branch `e.lai2 = 0` ✓.

Now — **case 3 buff target**: vanilla applies to Main.player[Main.myPlayer] — in single player = the player. ✓ ours.

**lai3 far flag**: vanilla `Distance(targetData.Center) >= 450` — when target invalid (None), what's targetData.Center? NPCAimedTarget.Center for None → probably Vector2.Zero → Distance from boss position to (0,0) — huge → >= 450 → true → lai3 climbs to 30 → dontTakeDamage... But when target is None, boss goes home anyway. Ours: `far = p != null && !p.dead && ...` — when no player → far=false → lai3 decays → damageable. Vanilla: climbs → invulnerable. Edge case (no valid target). Minor/ignore.

Now — the AI entry: `if (e.ai0 === -1120) e.ai0 = 0;` — our engine sentinel; fine.

**despawnTimer day rate**: fine.

**Case 6 → ai0=7 teleport** — vanilla also `netUpdate` only. ✓.

**Case 8**: ours `e.hp = -1; e.dead = true;` — vanilla life=-1 + HitEffect + active=false → no loot ✓.

Now — **the missing halt for case 0**... vanilla case 0 doesn't set halt. ✓ ours.

**Case 2 START=32** ✓. Sounds: vanilla DeerclopsScream at ai1==12 (num9-20=12) ✓ ours START-20=12; RubbleAttack at 32 ✓.

**Case 2 spawn position**: vanilla `base.Top.ToTileCoordinates()` — Top = (position.X, position.Y). Ours uses `floor(e.cx / TILE)` — center vs left edge. Deerclops width? Let me check SetDefaults for 668 to quantify. Width probably 70-ish → 35px ≈ 2 tiles offset. Minor numeric noise — but combined with facing*3, the rubble source is shifted ~2 tiles toward facing side. I'll call it minor noise; the task says ignore numeric noise but this is an origin bias, consistent direction. Not reporting as top-10 worthy? Maybe as minor. We have limited slots (max 10). Let me prioritize.

Now back to remaining Golem checks:

1. **Free head 249 invulnerability + win condition** — CONFIRMED HIGH.
2. **Freed head HP pool 25000 vs 16000** — CONFIRMED (they set e.hp = e.maxHp which is 246's pool). Wait — actually is e.maxHp of the head entity 246's maxHp? In our engine, when spawned via spawnPart(game, e, 246) — presumably creates Enemy with vanillaNpc(246) def → maxHp from def (scaled by difficulty). So yes 25000 base (or engine-scaled). And 249 would be 16000. So freed head has ~1.56× the intended HP. But given fix #1 (make head invulnerable), this becomes moot-ish; still report.
3. **Expert branch for golem?** — vanilla golem has no expertMode branches in these sections? AI_045 has none. OK, "expert 分支保留注释" in our header. Let me double check there's no expert branch in vanilla golem... The sections I read have no Main.expertMode references. ✓.
4. Fist anchor to head after body death vs vanilla anchoring to dead-body stale slot — part of #1's cluster. Vanilla behavior: fists remain active anchored to inactive NPC (position frozen). Ours re-anchors to head (moving anchor). Both non-vanilla-ish; ours documented as task convention ("锚定本体(或头)"). Given the task prompt itself says "联动:本体死→部件死" — hmm, the prompt's expectation is body death → parts die. Vanilla doesn't kill parts on body death (they linger). But the practical vanilla outcome: fight flag set on body death. Since we're auditing vs vanilla, I'll note the fist re-anchor as deviation sub-point of #1.

5. **Golem body player-dead handling**: ours `if (!player) noTC = true` — but does our harness pass null for dead players? Also ours despawns only when player non-null and far. Vanilla: dead player → no despawn (TargetClosest still returns the dead player in SP). Equivalent enough if harness passes the dead player. If harness passes null on death, ours: no despawn, noTC=true ✓ matches vanilla. OK fine.

6. **Golem body: `if (player && e.ai0 === 0)`** — when player null (dead), body doesn't charge/jump — vanilla keeps running AI (charging toward dead player's position). Minor edge.

7. Attached head stage 1 initial ai2: vanilla ai[2] starts 0; fine.

8. **golemEyeLasers**: vanilla for localAI[1]==0: TWO projectiles from ±18*scale at speed 11; else ONE from ±30*scale at 12. Ours ✓.

9. **Attached head laser dmg 28** ✓; free head 24 ✓.

10. Attached-head ai0 stage gate: ours `e.ai0 = e.hp < e.maxHp / 2 ? 1 : 0;` ✓ vanilla.

11. **Balance num ×2 zone check**: vanilla `(!ZoneLihzhardTemple && !ZoneJungle) || player.Center.Y < worldSurface*16` → ×2. Ours: `if (!inTempleOrJungle || (player != null && player.cy < groundLevel * TILE)) num *= 2` — when player null, ours skips the surface check but still ×2 if not in temple/jungle (scene is global). Vanilla requires Main.player[target] — boss always has target. Minor.

Hmm wait — actually one more important Golem check: **the jump `ai[1] === -1` exact equality with fractional num4**. During negative ai1, num4 = 1 exactly (boosts gated by ai1 > 0). But getGoodWorld +100 is also inside the `ai[1] > 0` gate ✓ ours. OK exact -1 reachable ✓.

12. Fist `e.ai1 >= 60` gate with side check: vanilla when side fails → ai[1]=0 and stays ai[0]=0 (retry) ✓ ours (state stays 0, ai1=0) ✓.

13. Fist hitSolid check placement: vanilla collideX/collideY set during movement when noTileCollide=false. Ours: after moving, if state===2 && !noTC && hitSolid → return. But ours' hitSolid checks ANY overlap with solid tile — vanilla collideX/Y require actual movement blocked. Also vanilla would zero velocity on collision (engine). Ours keeps velocity but returns to state 0 (velocity retained → will fly back toward shoulder at residual velocity... state 0 overrides velocity next tick anyway via shoulder seek). Close enough.

14. Head attach when body missing mid-fight: vanilla golemBoss < 0 → head strikes itself (dies). Ours: attached head with no body → golemHeadGoFree. Deviation but tied to death-chain redesign (#1).

Now — one more check on golem: **`fadeAlpha` sets `e.spawnAlpha = Math.min(254, x.alpha)`** — visual. Fine.

**Free head hovering accel**: vanilla has the double-step (when velocity and target opposite sign → extra 0.05). Ours accelTo — check bossAI.ts accelTo definition to be precise.

Also `spawnPart`, `shoot`, `losClear` semantics — shoot(game, sx, sy, vx, vy, dmg, projId, timeLeft?) — our calls pass 300 as 8th arg for lasers ✓ timeLeft.

Let me check accelTo and shoot and losClear quickly in bossAI.ts. Also check how golemAI/golemHeadAI/golemFistAI are routed (aiStyle mapping) and whether player param is null on death. Quick grep.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:15.551Z · glm-x-preview-260804

```
Deerclops 原版全段已核。发现一个高疑点：ShootRubbleUp 里 `num5 = Main.rand.Next(projFrames[962]*4)` 下一行被 `num5 = 6 + Main.rand.Next(6)` 覆盖。精确定位行号，并抽查我方 bossAI.ts 的 accelTo/shoot 语义。
```


---

## 🤖 Assistant · 2026-08-19T03:17:16.758Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"num5 = 6 + Main.rand.Next(6)\\|Main.rand.Next(Main.projFrames\\[962\\]\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; grep -n \"export function accelTo\\|export function shoot\\|export function losClear\\|export function spawnPart\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts",
 "description": "Pin exact rubble frame line numbers and bossAI helper definitions"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:16.815Z

**📎 ToolResult**

```
44768:				int num5 = Main.rand.Next(Main.projFrames[962] * 4);
44769:				num5 = 6 + Main.rand.Next(6);
---
148:export function spawnPart(game: GameHooks, src: Enemy, id: number): Enemy | null {
633:export function accelTo(v: number, target: number, a: number): number {
648:export function losClear(game: GameHooks, x0: number, y0: number, x1: number, y1: number): boolean {
654:export function shoot(game: GameHooks, x: number, y: number, vx: number, vy: number, dmg: number, projId: number, life = 300, arrowOpts?: Partial<import('./Arrow').ArrowOpts>): void {

```


---

## 🤖 Assistant · 2026-08-19T03:17:22.195Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '625,700p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts",
 "description": "Read accelTo, losClear, shoot helper implementations"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:22.229Z

**📎 ToolResult**

```
}

// ================= 机械三王(NPC.cs AI_030-037,1.4.5.6 行号见各核注释) =================
// 经典模式参数 1:1;getGoodWorld(FTW)分支已全量实装(克脑/双子/毁灭者/爬行者);
// 专家/大师分支仅注释保留。史莱姆王 AI_015 的 FTW 分支(:43440/:43662)依赖的
// 基线行为(空中横移 num7=3、跳跃 num2 缩放)本仓未建模,无可挂载点,登记跳过。

/** 原版速度逼近(L26539-26670 雏形):朝目标速度单轴步进,符号翻转时双倍步进 */
export function accelTo(v: number, target: number, a: number): number {
  if (v < target) { v += a; if (v < 0 && target > 0) v += a; }
  else if (v > target) { v -= a; if (v > 0 && target < 0) v -= a; }
  return v;
}
/** 朝 (tx,ty) 以速度 spd/加速度 acc 追赶(vanilla numXXX = spd/dist 归一后 accelTo) */
export function seek(e: Enemy, tx: number, ty: number, spd: number, acc: number): void {
  const dx = tx - e.cx, dy = ty - e.cy;
  const d = Math.hypot(dx, dy) || 1;
  e.vx = accelTo(e.vx, (dx / d) * spd, acc);
  e.vy = accelTo(e.vy, (dy / d) * spd, acc);
}
/** 直线视线(Collision.CanHit 1:1,Collision.cs:388-480:逐 tile 扫描,半砖/坡面/
 *  平台/已致动/开门态不阻挡,"两邻格均整实心"=被夹住 → 无视线;8px 采样近似已退役)。
 *  入参为像素点对(w=h=0 → 中心=该点);原版 CanHitLine 场景见 physics/LineOfSight */
export function losClear(game: GameHooks, x0: number, y0: number, x1: number, y1: number): boolean {
  return canHit(game.world.store, x0, y0, 0, 0, x1, y1, 0, 0);
}
/** Boss 弹幕:直飞(grav 0)+ 原版 Projectile_N 贴图。
 *  hostile=true(原版 Projectile.hostile):命中玩家结算——所有走本出口的弹都是
 *  Boss/敌怪发射的敌弹(双子激光/死光/蜂后毒刺/哥布林弹等) */
export function shoot(game: GameHooks, x: number, y: number, vx: number, vy: number, dmg: number, projId: number, life = 300, arrowOpts?: Partial<import('./Arrow').ArrowOpts>): void {
  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
    new Arrow(x, y, vx, vy, dmg, 0, projId, null, { grav: 0, life, pierce: 1, hostile: true, ...arrowOpts }), 'projectiles');
}

/** NPC.SpawnMechQueen 合体召唤链(NPC.cs:19739-19748,Game.summonMechdusa 调用)：
 *  queen(127) 落位 → markMechQueen(=SpawnBoss :81472 写 ai[3]=mechQueen 非零标记)
 *  → 以 queen Center 为共同出生点同点 NewNPC 125/126/134 + 2×139 探针
 *  (ai2=毁灭者头引用,ai3=∓1 侧位——原版第 7/8 参 ai2/ai3,曾误记 ai0)。
 *  调用方须已过 anyMechBossUp 门与 Mechdusa 种子门(remix+getGood)。 */
export function spawnMechQueenEnsemble(game: GameHooks, cx: number, cy: number): Enemy | null {
  const queen = spawnVanillaEnemy(game, 127, cx, cy);
  if (!queen) return null;
  // SpawnBoss :81469-81473：Type==127 且 mechQueen!=-1 → ai[3]=whoAmI(非零标记)；
  // 本仓 ai3 是旋冲方向缓存(±1)不冲突——mech 态旋转走 AngleLerp 不读 ai3,标记走 WeakSet
  markMechQueen(queen);
  queen.ai3 = queen.id;
  // :19743-19747 同点伴随(取 mechQueen 的 Center);探针 ai2=134 引用、ai3=∓1 侧位
  for (const id of [125, 126]) spawnVanillaEnemy(game, id, queen.cx, queen.cy);
  const head = spawnVanillaEnemy(game, 134, queen.cx, queen.cy);
  for (const side of [-1, 1]) {
    const probe = spawnVanillaEnemy(game, 139, queen.cx, queen.cy);
    if (probe) { probe.ai2 = head ? head.id : -1; probe.ai3 = side; }
  }
  return queen;
}

/** Mechdusa 探针 139 挂链锁位(NPC.cs AI_005 :50866-50920 + :50975-51007)：
 *  ai3≠0 = 召唤链出生的挂链探针——queen 失效/头失效 → 脱落(ai3=0 回常规 swarmer,
 *  dontTakeDamage 解除);头在场 → 锁位绕头(头中心 + (26×ai3,0).RotatedBy(头 rotation,
 *  头中心)),速度 = queen 速度,无敌;localAI[0] 每 tick +3、受击清零,≥360 发 84 号
 *  弹(25 伤,玩家速度×20 预判 8 速,Projectile.cs 命中端另乘难度)。
 *  返回 true = 已锁位并完成积分(调用方须跳过常规移动段)。 */
export function mechProbeLock(e: Enemy, game: GameHooks, player: Player | null): boolean {
  if (!mechQueenUp()) {
    e.dontTakeDamage = false;
    e.ai3 = 0;                        // :50909-50919 else 分支:脱落
    return false;
  }
  const queen = getMechQueen()!;
  // :50877-50881 ai2 引用失效(头槽变号) → FindFirstNPC(134) 重挂
  const ens = game.enemies() as Enemy[];
  let host: Enemy | null = ens.find((n) => !n.dead && n.vanillaId === 134 && n.id === e.ai2) ?? null;
  if (!host) {
    host = ens.find((n) => !n.dead && n.vanillaId === 134) ?? null;
    if (host) e.ai2 = host.id;
  }

```


---

## 🤖 Assistant · 2026-08-19T03:17:34.880Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
accelTo has the double-step ("符号翻转时双倍步进") ✓ matching vanilla pattern. Good — so the free-head hovering matches including double-step.

shoot() defaults life=300 ✓ — and importantly: `pierce: 1, grav: 0, hostile: true`. Vanilla 258 fireball / 259 laser — laser proj 259 no gravity ✓, fireball 258 (golem fireball) — does it have gravity? ProjectileID 258 GolemFireball? Actually 258 = "golem fireball"... In vanilla, deerclops... no wait, 258 is from NPC.cs NewProjectile with no extra ai; the projectile's own AI handles gravity. projFrames etc. Not in audit scope (Projectile.cs). grav 0 likely fine since 258 flies straight (I believe golem fireballs fly straight). OK.

Now let me verify how our engine routes these AI functions and what `player` param means when dead — quick grep for golemHeadAI call site. Also verify Enemy has dontTakeDamage field that engine respects (deerclops sets e.dontTakeDamage). For golem our code uses iframes=2 for invulnerability instead. Fine.

Let me check the router quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:35.490Z · glm-x-preview-260804

```
accelTo 含符号翻转双步进 ✓。查 AI 路由与 player 参数语义(死亡时传 null 还是死玩家)。
```


---

## 🤖 Assistant · 2026-08-19T03:17:36.629Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"golemAI\\|golemHeadAI\\|golemFistAI\\|deerclopsAI\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts -l | grep -v bossAI_golem | grep -v bossAI_deerclops; echo ---; grep -n \"golemAI\\|golemHeadAI\\|golemFistAI\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head",
 "description": "Find AI routing call sites for golem and deerclops"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:36.673Z

**📎 ToolResult**

```
(eval):1: no matches found: --include=*.ts
---
44:import { golemAI, golemHeadAI, golemFistAI } from './bossAI_golem';
1266:        case 45: golemAI(this, game, p); break;                        // AI_045 石巨人本体 245(蓄力跳/挂头无敌)
1267:        case 46: golemHeadAI(this, game, p); break;                      // AI_046 挂载头 246(锚本体/火焰弹眼激光;249 自由态)
1268:        case 47: golemFistAI(this, game, p); break;                      // AI_047 石巨人拳 247/248(肩锚冲拳)
1320:        case 48: golemHeadAI(this, game, p); break;                       // AI_048 自由石巨人头 249（cs:31500,golemHeadAI 已含自由态分支）

```


---

## 🤖 Assistant · 2026-08-19T03:17:38.719Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1200,1270p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read Enemy AI dispatch to see player param semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:38.742Z

**📎 ToolResult**

```
        case 4: this.eocAI(game, (game as unknown as { player: Player }).player ?? null); break; // AI_004 克苏鲁之眼（NPC.cs:19909）
        case 5: this.swarmerAI(game, p); break;                         // AI_005 噬魂怪族（原版蜂群核）
        case 6:
          // AI_006 蠕虫族（头）；412 爬尾虫走专属核（bossAI_lunar_misc：
          // 30 段链 + 空泳追击环 + 414 尾受击红闪 localAI[2] 状态机，cs:51357-52671）
          if (this.vanillaId === 412) crawltipedeAI(this, game, p);
          else this.wormAI(game, p);
          break;
        case 8: this.casterAI(game, p); break;                          // AI_008 法师族（传送+弹幕）
        case 10: this.cursedSkullAI(game, p); break;                     // AI_010 诅咒头骨（地牢飞行族）
        case 11:
          // 68 守卫走专用分支（bossAI.skeletronBossAI 注释"守卫分支已在 skeletronHeadAI"
          // 即此拆分：守卫恒速追击与骷髅王战斗状态机互不混用）
          if (this.vanillaId === 68) this.dungeonGuardianAI(game, p);
          else skeletronBossAI(this, game, p);
          break;                                                         // AI_011 骷髅王头战斗核/地牢守卫
        case 12: skeletronHandAI(this, game, p); break;                    // AI_012 骷髅王手(锚定头)
        case 20: this.blazingWheelAI(); break;                           // AI_020 火轮（地牢陷阱）
        case 21: this.spikeBallAI(game); break;                          // AI_021 刺球（地牢陷阱）
        case 14: this.batAI(game, p); break;                            // AI_014 蝙蝠/飞行族（1.4.5.6 原版核）
        case 16: this.swimAI(game, p); break;                           // AI_016 游泳族（鲨鱼/食人鱼）
        case 18: this.jellyfishAI(game, p); break;                      // AI_018 水母族（脉冲游动）
        case 22: this.ghostAI(game, p); break;                          // AI_022 幽灵族（穿墙缓速）
        case 13: this.plantAI(game, p); break;                          // AI_013 植物/攀爬者族（锚点伸展）
        case 15: kingSlimeAI(this, game, p); break;                       // AI_015 史莱姆王(大跳+小史莱姆)
        case 54: brainOfCthulhuAI(this, game, p); break;                  // AI_054 克脑(爬行者环→瞬移冲刺)
        case 55: creeperAI(this, game, p); break;                         // AI_055 爬行者(环绕漂移)
        case 30: twinsAI(this, game, p, false); break;                    // AI_030 雷神之眼 125(悬浮/连冲/变身/激光)
        case 31: twinsAI(this, game, p, true); break;                     // AI_031 魔神之眼 126(诅咒焰/火焰喷射)
        case 32: skeletronPrimeAI(this, game, p); break;                  // AI_032 机械骷髅王头 127(4 部件/旋冲/白天狂暴)
        case 33: case 34: case 35: case 36: primePartAI(this, game, p); break; // AI_033-036 Prime 部件(锯/激光/钳/炮)
        case 37: destroyerAI(this, game, p); break;                       // AI_037 毁灭者 134(80 段链穿地/探针激光)
        case 27: wallOfFleshAI(this, game, (game as unknown as { player: Player }).player ?? null); break; // AI_027 血肉墙(空腔扫描/速度血量档/Leech 轮)
        case 28: wofEyeAI(this, game, p); break;                          // AI_028 血肉墙之眼(钉墙吸附/激光连射 83)
        case 29: hungryAI(this, game, p); break;                          // AI_029 饥饿者(挂墙环绕→受击脱落扑咬)
        case 84: lunaticCultistAI(this, game, p); break;                  // AI_084 拜月教邪教徒(瞬移+四系弹幕轮换)
        // ---- 月系批（bossAI_lunar_misc.ts）----
        case 81: moonLordFreeEyeAI(this, game, p); break;                // AI_081 月总游离眼 400（cs:38224 十槽攻击表+死光）
        case 82: moonLeechAI(this, game, p); break;                       // AI_082 月总水蛭块 401（cs:38668 90t 插值吸血回灌）
        case 83:                                                            // AI_083 神秘石碑 437/忠实信徒 438（cs:38793）
          if (this.vanillaId === 437) cultistTabletAI(this, game, p);
          else lunaticDevoteeAI(this, game, p);
          break;
        case 86: phantomAI(this, game, p); break;                          // AI_086 暗焰幻影 472/远古幻影 521（cs:39261 穿墙横掠循环）
        case 87: bigMimicAI(this, game, p); break;                         // AI_087 珍稀四宝箱怪 473-476（cs:39520 跳扑+蓄能/俯冲/三连扑）
        case 88: mothronAI(this, game, p); break;                          // AI_088 飞蛾魔 477（cs:39876 日食限定轮换+产卵）
        case 89: mothronEggAI(this, game, p); break;                       // AI_089 蛾卵 478（cs:40407 900t→Transform 479）
        case 90: babyMothronAI(this, game, p); break;                      // AI_090 幼蛾 479（cs:40450 日食贴脸冲撞）
        case 91: graniteElementalAI(this, game, p); break;                 // AI_091 花岗岩元素 483（cs:40686 五态寻路）
        case 120: empressOfLightAI(this, game, p); break;                 // AI_120 光之女皇(连段选招/半血变身)
        case 121: queenSlimeAI(this, game, p); break;                     // AI_121 史莱姆皇后(走路四连跳→飞行二阶段)
        case 122: this.pirateGhostAI(game, p); break;                     // AI_122 海盗幽灵 662（穿墙追击+失标渐隐自灭）
        case 123: deerclopsAI(this, game, p); break;                      // AI_123 鹿角怪(尖刺/碎石/影手/回家)
        case 100: ancientLightAI(this, game, p); break;                  // AI_100 远古之光 522(直飞投射物型)
        case 101: ancientDoomAI(this, game, p); break;                  // AI_101 远古末日 523(锚邪教徒蓄能自爆)
        case 43: queenBeeAI(this, game, p); break;                        // AI_043 蜂后(悬浮俯冲/蜜蜂机枪/毒刺)
        case 50: planteraHookAI(this, game, p); break;                    // AI_050 真菌孢子 261/孢子 265
        case 51: planteraAI(this, game, p); break;                        // AI_051 世纪之花(钩蔓牵引→二阶段)
        case 52: planteraTentacleAI(this, game, p); break;                // AI_052 钩蔓 263(抓墙换锚收线)
        case 53: planteraTentacle2AI(this, game, p); break;               // AI_053 触须 264(二阶段环绕)
        case 69: dukeFishronAI(this, game, p); break;                     // AI_069 猪鲨(冲撞/泡泡/龙卷,半血变身)
        case 70: dukeBubbleAI(this, game, p); break;                      // AI_070 爆裂泡泡 371
        case 71: sharkronAI(this, game, p); break;                        // AI_071 鲨鱼龙 372/373(龙卷出鲨,升空蓄力→扑咬)
        case 77: moonLordCoreAI(this, game, p); break;                    // AI_077 月总核心 398(双手死前无敌)
        case 78: moonLordHandAI(this, game, p); break;                    // AI_078 月总手 397(攻表/睁眼可击)
        case 79: moonLordHeadAI(this, game, p); break;                    // AI_079 月总头 396(死亡之光/吸血)
        case 45: golemAI(this, game, p); break;                        // AI_045 石巨人本体 245(蓄力跳/挂头无敌)
        case 46: golemHeadAI(this, game, p); break;                      // AI_046 挂载头 246(锚本体/火焰弹眼激光;249 自由态)
        case 47: golemFistAI(this, game, p); break;                      // AI_047 石巨人拳 247/248(肩锚冲拳)
        case 40: this.wallCreeperAI(game, p); break;                      // AI_040 爬墙蜘蛛族（贴背景墙爬行+形态互转）
        case 42: this.lostGirlAI(game, p); break;                         // AI_042 失落女孩（伪装静止→Nymph 变身 cs:30281-30310）

```


---

## 🤖 Assistant · 2026-08-19T03:17:43.034Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me see where `p` comes from — a few lines above case 4. Let me look at the function header around line 1150-1200.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:43.655Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1150,1200p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | grep -n \"p =\\|const p\\|player\" ",
 "description": "Find where p is assigned in Enemy AI dispatch"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:43.693Z

**📎 ToolResult**

```
14:    const player = (game as unknown as { player: Player }).player;
15:    const hasPlayer = !!player && !player.dead;
25:      this.critterWanderAI(game, hasPlayer ? player : null);
27:      const p = hasPlayer ? player : null;
51:        case 4: this.eocAI(game, (game as unknown as { player: Player }).player ?? null); break; // AI_004 克苏鲁之眼（NPC.cs:19909）

```


---

## 🤖 Assistant · 2026-08-19T03:18:39.892Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So `p` is null when the player is dead (`hasPlayer ? player : null`). So in our golemAI, `!player` = player dead → noTC = true (matches vanilla's dead → noTileCollide = true). Good — that path is equivalent.

But one consequence: ours `if (player && e.ai0 === 0)` — when player dead, AI freezes (no charging, no jumping, gravity continues). Vanilla: continues charging with the dead player as target (target stays). Minor.

Also for deerclops: `p` null when dead → our shouldRunAway(!p) → true → case 6 go home ✓ vanilla.

Now let me nail down the remaining verification points:

1. Deerclops rubble frame: vanilla 44768-44769 → final num5 = 6 + rand(6) = 6..11. Ours rand(12) = 0..11 with a comment claiming 0..11 is right and 6..11 was the "误写". CONFIRMED deviation (ours cites the dead first assignment). Severity: visual frame choice only (which of 12 rubble variants spawns — top row vs bottom two rows... wait 3×4 grid: frame index 0..11; 6..11 = bottom two rows of 4? frame = 6..11; drawImage frameX = f%3, frameY = f/3 → frames 6-11 → row 2-3 (0-indexed rows 2,3). Ours 0..11 → all rows. Effect: purely visual variety of rubble chunks. LOW severity but CONFIRMED and it's a comment-lie ("注释撒谎" case). Include with low/medium severity since task explicitly wants comment-vs-reality checks. Actually the audit is about AI behavior; visual frame is noise-level. But it's also a factual misread of source (claimed fix introduced deviation). I'll include it ranked low.

2. Expert passive hands 2 vs 3 per cycle. CONFIRMED. Medium.

3. Golem free head killable + whole-family death = win condition; vanilla free head invulnerable + body death = win. HIGH.

4. Freed head HP 25000 vs 16000. MEDIUM (subsumed by 3's fix, but independently wrong since golemHeadGoFree sets hp = e.maxHp).

Wait — actually, if #3 is fixed by making the head invulnerable, #4 becomes moot. But as long as both exist... I'll report separately but note dependency.

5. Also — in ours, body death does NOT set anything that ends the fight: head keeps fighting. In vanilla, body death sets downedGolemBoss (DoDeathEvents) — fight over (head invulnerable, remains but harmless-ish? it keeps shooting actually). Practically: vanilla = loot + flag on body death. Ours = no loot/flag until free head killed. This is part of #3 (inverted win condition) — I'll fold into one finding with sub-bullets, since they're one structural redesign.

Actually let me reconsider: is our engine's death/loot driven by e.dead? Our body dying → e.dead = true after 60t — that presumably triggers loot/flag via the engine's normal death chain. So body death DOES drop loot + flag in ours (after 60t) — but the fight continues (head + fists). In vanilla, killing body = flag + loot, and head remains invulnerable shooting... hmm, so vanilla post-body-death: 249 + fists linger! Do they despawn? golemBoss stale... 249 has no despawn logic in aiStyle 48 (TargetClosest only). Hmm — actually wait, general NPC despawn: `if (npc.boss ...)`. 249 not boss. There IS generic despawn in UpdateNPC: when `npc.active && ... Main.player[npc.target].dead`? No... Generic: NPCs despawn when offscreen for non-boss: `if (!boss && Distance > 3000 ...) active=false`? There's the standard "NPCs despawn when far from all players" logic (num217 etc. in UpdateNPC). 249 and fists would eventually despawn when player leaves. In practice after body death the fight flag is set, loot dropped; leftovers annoy briefly.

OK. So the essential inversion: ours requires killing the head to finish (and allows it), vanilla requires killing the body. Both directions wrong-ish:
- Ours: head killable (vanilla: invulnerable) → players can end fight by killing head.
- Ours: body death doesn't end fight (head persists as the last word) — vanilla ends it.
Combined: win condition inverted.

But hold on — one more scenario in ours: what if player kills the head FIRST while body alive? Head goes free (can't die while attached since hp<=0 → goFree restores full HP... wait: golemHeadGoFree sets e.hp = e.maxHp — the attached head reaching 0 "dies" → goes free with FULL HP again. So phase 1 head pool = 25000, then free head = another 25000. Then player must kill free head (25000) OR body (15000, but body death doesn't end fight...). Hmm wait — does body death end the fight in ours? After body dead=true, head continues. Fists anchor to head. So fight continues until free head killed. Total effective HP to win: 25000 (head phase) + 25000 (free head) = 50000, ignoring body. Vanilla: 25000 (head) + 15000 (body) = 40000, head free-head invulnerable. Ours ~50000 + body optional. Anyway.

Also check: in ours, when free head is killed → whole family dies. e.dead = true for head + all 245-249. Body already dead presumably. OK.

6. Golem fist post-body-death re-anchor to head: fold into #3 note.

7. Attached head anchored 100-unit snap: ✓.

8. Attached-head laser damage tier at hp<40%/20% ✓.

9. Now — what about `e.iframes = 2` as dontTakeDamage for the body? Vanilla body: `dontTakeDamage = flag` (head attached). Ours sets iframes=2 every tick while hasHead. Engine-specific equivalent ✓. Deerclops uses e.dontTakeDamage. OK.

10. Now Deerclops case 0 → 3 (scream): vanilla flag9 = `targetData.Type == Player && !Main.player[target].buffImmune[32] && FindBuffIndex(32) == -1` — buffImmune[32] check (player immune to Slow). Ours `!p.buffs.has(BuffType.Slow)` ✓ (misses immunity nuance, fine).

11. Deerclops lai1: case 0 → 1 (forward) does `localAI[1] += 1f` ✓ ours `e.lai1 += 1` — wait ours line 131: `e.vx = 0; e.ai0 = 1; e.ai1 = 0; e.lai1 += 1; break;` ✓. And state 4 requires lai1 >= 2 ✓ ours.

12. Hmm — case 1 (forward spikes): vanilla calls MakeSpikesForward(1, targetData) with slot 1 (ai[1]). Ours `makeSpikesForward(game, e, p, 1)` ✓. Case 4: BothSides(1, ...) ✓. Where is slot != 1 used? Maybe nowhere (legs?). Fine.

13. Deerclops spike AI_157 life=20... vanilla projFrames 961 and lifetime: num9=20; the proj spawns with ai[1] param as scale factor; timeLeft default... vanilla 961 hostile spike lasts ~20 frames growth/shrink then Kill. Ours life=20 with `--this.life <= 0` → dies after 20 ticks ✓ roughly. But ours decrements BEFORE the was===0 first-frame block: on first fixedUpdate, life 20→19, was=0 → first-frame dust+sound ✓. On 20th update life→0 → dead. Opacity: was<10 → +0.1 (ticks 0..9 = 10 ticks → opacity 1.0); then -0.2 → 0 at was=15... vanilla num9=20: `if (ai[0] < 10) opacity += 0.1 else if (ai[0] < 20) opacity -= 0.2` roughly then kill at 20. Close.

14. Shadow hands damage: case 5 uses num=15 ✓; passive 10 ✓. Vanilla InsanityShadowProj 965 damage passed as `num`/`shadowHandDamage` ✓ ours DMG_HANDS=15, passive 10 ✓.

15. RandomizeInsanityShadowFor — ours approximates spawn ring 200px around player, ai0 hint [0,180,300,390]. Vanilla RandomizeInsanityShadowFor picks random variation & spawn position relative to target... ours is an approximation documented. The hint selection: vanilla `Projectile.RandomizeInsanityShadowFor(player, isHostile, out spawnposition, out spawnvelocity, out ai, out ai2)` — ai out is the starting ai0 (variation), randomized among [0,180,300,390]? and ai2 = some angle. Ours picks ai0 = [0,180,300,390][hint%4] where hint = num3%3 for passive (1,2 → 180,300) and i%3 for case 5 (0,1,2 → 0,180,300). Vanilla's hint (Boss_CanShootExtraAt second arg num3%3)... wait — Boss_CanShootExtraAt(i, num3 % 3, 3, 1200f, false) — the second parameter is actually "whichVariant"? Let me not go down this hole; it's Projectile.cs territory (RandomizeInsanityShadowFor at Projectile.cs :39703-39796 per our comment — wait no, our comment says AI_187_ShadowHand :39798-39940 + RandomizeInsanityShadowFor :39703-39796 — those are NPC.cs line numbers? No — RandomizeInsanityShadowFor is a Projectile static. The comment cites ":39703-39796" which is likely Projectile.cs. Not in scope (we're told to audit vs NPC.cs; Projectile internals out of scope). The Boss_CanShootExtraAt signature: (int playerIndex, int variant, int maxVariants, float maxDistance, bool alwaysSkipMainTarget)? If second arg is the variant hint, then vanilla passive hands get variant num3%3 ∈ {1,2,0} and case 5 hands get... case 5 calls RandomizeInsanityShadowFor directly (no variant arg — fully random). Ours case 5 passes i%3 hint → hands 1,2... wait ours: `new InsanityShadowProj(p, DMG_HANDS, i % 3)` for i 0..5 → hints 0,1,2,0,1,2 → ai0 = 0,180,300,0,180,300 — vanilla case 5: fully random variants. Approximation, fine.

Now — one more Deerclops check: **case 6 halt condition** `nearHome && e.ai1 % 600 < 420` ✓.

**Entry state -1**: how does ai0 become -1 in ours? Engine's ai0 default -1120 → mapped to 0 at line 59! Vanilla deerclops spawns with ai[0] = -1? Let me check SpawnBoss or the deerclops spawn: search "668" NewNPC with ai. In vanilla NPC.SpawnNPC / SpawnBoss — deerclops summon item (Pew-mar? "Deerclops Talisman"?): the item spawns 668 with ai0... Actually aiStyle 123's case -1 handles entry walk. Where's -1 set? Probably NewNPC call from item with aiStyle... Let me grep quickly for ", 668, " in NPC.cs / Item source? The summon is from ItemCheck in Player.cs or Item.cs. Out of scope-ish, but the -1120→0 mapping means our deerclops NEVER walks the -1 entry state unless the summon sets ai0=-1. Let me check our spawner: grep for 668 in game/src to see if spawn sets ai0=-1. If not, deerclops skips the intro walk — check vanilla: does the natural spawn also use -1?

Vanilla: Deerclops spawns naturally in snow blizzard at night OR via Deerclops Talisman item. The item: NewNPC(...668, ai?) hmm. Let me grep "668" around spawn sites in Player.cs/Item.cs... The task scope is NPC.cs AI comparison; but "阶段缺失" — if our summon never sets ai0=-1 while vanilla does, the intro phase is missing. Let me check vanilla: grep -n "668" in Player.cs for the summon item usage.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:40.427Z · glm-x-preview-260804

```
查 Deerclops 的入场态 ai0=-1 由谁设定(原版召唤点 vs 我方生成点)。
```


---

## 🤖 Assistant · 2026-08-19T03:18:42.427Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"668\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | grep -in \"newnpc\\|spawn\" | head; echo ---; grep -rn \"668\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Item.cs | grep -in \"newnpc\\|spawn\\|668\" | head; echo ---; grep -rn \"vanillaId === 668\\|spawnBoss?.*(668\\|, 668,\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v deerclops | head",
 "description": "Find deerclops spawn sites in vanilla and our engine"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:42.584Z

**📎 ToolResult**

```
2:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:7533:				QuickSpawnItem(source, 668);
8:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:43232:				NPC.SpawnOnPlayer(onWhichPlayer, 668);
---
1:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Item.cs:9175:		case 668:
2:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Item.cs:19164:		case 1668:
3:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Item.cs:25778:				if (type >= 2664 && type <= 2668)
4:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Item.cs:32859:		case 3668:
5:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Item.cs:38471:		case 4668:
6:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Item.cs:47374:		case 5668:
---
~/Project/GLM/SandboxWorld/game/src/world/liquid/LiquidSim.ts:53:const LAVA_DEATH_SHEETS = new Set([630, 631, 571, 579, 591, 538, 544, 629, 550, 551, 533, 553, 554, 555, 556, 558, 559, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 632, 640, 643, 644, 645, 710, 568, 569, 570, 580, 582, 619, 620, 572, 560, 564, 567, 565, 654, 529, 530, 705, 484, 3, 5, 10, 11, 12, 13, 14, 469, 486, 488, 704, 487, 489, 490, 15, 497, 16, 17, 18, 19, 24, 27, 28, 29, 32, 33, 34, 35, 36, 42, 49, 50, 707, 51, 697, 52, 55, 61, 703, 62, 69, 655, 71, 72, 73, 74, 79, 80, 81, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 106, 110, 113, 115, 125, 126, 128, 149, 172, 173, 174, 184, 201, 205, 209, 210, 212, 213, 353, 215, 216, 217, 218, 219, 642, 220, 227, 228, 233, 236, 702, 238, 240, 241, 242, 243, 244, 245, 246, 247, 254, 269, 270, 271, 581, 698, 660, 275, 413, 276, 277, 278, 279, 280, 281, 282, 283, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 532, 316, 317, 318, 319, 354, 355, 699, 499, 323, 335, 338, 339, 528, 636, 352, 382, 425, 453, 456, 463, 464, 465, 485, 511, 510, 547, 548, 552, 573, 621, 622, 623, 624, 700, 656, 701, 493, 395, 520, 471, 405, 406, 452, 457, 454, 494, 387, 386, 388, 389, 646, 372, 639, 668, 324, 427, 390]);
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts:3995:      if (e.vanillaId === 668) { this.drawDeerclopsGrid(e); return; }
~/Project/GLM/SandboxWorld/game/src/entities/MinionProj.ts:851:              Object.assign(new Arrow(mx - 8, my - 8, vx, vy, dmgOf(), this.knockback, 668, null, { grav: 0.2 }), { whipTagShot: true }),
~/Project/GLM/SandboxWorld/game/src/entities/WhipTag.ts:67:export const SENTRY_SHOT_SET = new Set([680, 664, 666, 668, 694, 695, 696, 644, 642, 378, 379, 309, 967, 1026]);
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:191:  439, 578, 636, 657, 664, 668,

```


---

## 🤖 Assistant · 2026-08-19T03:18:47.488Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla deerclops spawn: `NPC.SpawnOnPlayer(onWhichPlayer, 668)` at Player.cs:43232 — that's the natural/item spawn. Does SpawnOnPlayer set ai[0]=-1? Let me check SpawnOnPlayer → NewNPC with default ai 0. Hmm, but case -1 in the AI is "入场走位". Who sets ai[0]=-1? Maybe the NPC spawning code for natural deerclops at spawn: `NewNPC(..., 668, -1)`? Let me search for where -1 ai is passed for 668. Actually — check NPC.cs SpawnNPC for deerclops natural spawn, or search ", 668, " in NPC.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:48.179Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \", 668\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; echo ---; sed -n '43220,43245p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs",
 "description": "Find deerclops NewNPC calls with ai args"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:48.275Z

**📎 ToolResult**

```
87303:					Gore.NewGore(position, velocity, 668);
---
				else
				{
					NetMessage.SendData(61, -1, -1, null, whoAmI, 657f);
				}
			}
		}
		else if (sItem.type == 5120 && ZoneSnow)
		{
			ApplyItemTime(sItem);
			SoundEngine.PlaySound(15, (int)position.X, (int)position.Y, 0);
			if (Main.netMode != 1)
			{
				NPC.SpawnOnPlayer(onWhichPlayer, 668);
			}
			else
			{
				NetMessage.SendData(61, -1, -1, null, whoAmI, 668f);
			}
		}
	}

	private void ItemCheck_UseEventItems(Item sItem)
	{
		if (ItemTimeIsZero && itemAnimation > 0 && sItem.type == 361 && Main.CanStartInvasion(1, ignoreDelay: true))
		{
			ApplyItemTime(sItem);

```


---

## 🤖 Assistant · 2026-08-19T03:18:53.028Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So item 5120 (Deerclops Talisman / "鹿角怪护符"?) spawns via SpawnOnPlayer(668) — default ai 0? Hmm. Then when is ai[0] = -1 used? Maybe natural spawn sets it. Let me check NPC.cs natural spawn for deerclops — search "668" in the spawn section. Actually let me search for how SpawnNPC handles 668.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:54.319Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"num973 == 668\\|== 668\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; echo ---; grep -rn \"deerclops\\|Deerclops\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -in \"spawn\" | head",
 "description": "Find natural deerclops spawn code in NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:54.415Z

**📎 ToolResult**

```
17384:		else if (type == 668)
18241:		else if (type == 668)
18548:		if (type == 668)
78581:		return type == 668;
79758:		else if (type == 668)
82673:		if (type == 668)
---
39:~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:44851:	private void AI_123_Deerclops_FindSpotToSpawnSpike(int howMany, int whichOne, ref int x, ref int y)

```


---

## 🤖 Assistant · 2026-08-19T03:18:59.954Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '82660,82720p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ===; sed -n '17384,17400p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read deerclops spawn-inject ai0 and SetDefaults 668"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:00.016Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
				}
			}
			else
			{
				for (int num14 = 0; (float)num14 < 200f; num14++)
				{
					Dust dust5 = Dust.NewDustDirect(position, width, height, 228, 6 * hitDirection, velocity.Y, 0, Color.Transparent, 3f);
					dust5.noGravity = true;
					Dust dust = dust5;
					dust.velocity *= 5f;
				}
			}
		}
		if (type == 668)
		{
			if (life > 0)
			{
				for (int num15 = 0; (double)num15 < dmg / (double)lifeMax * 100.0; num15++)
				{
					Dust.NewDust(position, width, height, 5, hitDirection, -1f, 0, default(Color), 1.2f);
				}
			}
			else
			{
				int num16 = 15;
				Vector2 vector7 = position - new Vector2(num16, num16);
				for (int num17 = 0; num17 < 120; num17++)
				{
					int num18 = Dust.NewDust(vector7, width + num16 * 2, height + num16 * 2, 5, 0f, 0f, 0, default(Color), 1.5f);
					Main.dust[num18].velocity = Main.rand.NextVector2Circular(4f, 4f);
				}
				Vector2 vector8 = velocity * 0.6f;
				Gore.NewGore(base.Bottom + new Vector2(-10f, 0f), vector8, 1274, scale);
				Gore.NewGore(base.Bottom + new Vector2(10f, 0f), vector8, 1274, scale);
				Gore.NewGore(base.Center, vector8, 1272, scale);
				Gore.NewGore(base.Center + new Vector2(-10f, 0f), vector8, 1273, scale);
				Gore.NewGore(base.Center + new Vector2(10f, 0f), vector8, 1273, scale);
				Gore.NewGore(base.Top, vector8, 1270, scale);
				Gore.NewGore(base.Top, vector8, 1271, scale);
			}
		}
		if (type == 636)
		{
			if (life > 0)
			{
				for (int num19 = 0; (double)num19 < dmg / (double)lifeMax * 100.0; num19++)
				{
					if (Main.rand.Next(2) == 0)
					{
						Dust.NewDust(position, width, height, 67, hitDirection, -1f);
					}
					else
					{
						Dust.NewDust(position, width, height, 69, hitDirection, -1f);
					}
				}
			}
			else
			{
				for (int num20 = 0; num20 < 50; num20++)
				{
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-19T03:19:04.040Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `===` broke zsh again. But I got the first part (HitEffect for 668 — dust/gore, no ai injection). Let me check line 18241 and 18548 separately with proper quoting.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:04.742Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '18235,18260p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; sed -n '18540,18570p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read type 668 branches at 18241 and 18548"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:04.850Z

**📎 ToolResult**

```
		else if (type == 36)
		{
			num2 = 1.3;
			num3 *= CommonMasterBossLifeReduction;
			num = 1.1;
		}
		else if (type == 668)
		{
			num2 = 0.85;
			num3 *= CommonMasterBossLifeReduction;
		}
		else if (type == 113 || type == 114)
		{
			num2 = 0.7;
			num3 *= CommonMasterBossLifeReduction;
			num = 1.5;
			if (difficulty >= GameDifficultyLevel.Expert)
			{
				defense += 6;
			}
		}
		else if (type == 115)
		{
			num2 = 0.7;
			if (difficulty >= GameDifficultyLevel.Expert)
			{
---
		if (type == 35)
		{
			num *= (double)balance;
		}
		else if (type == 36)
		{
			num *= (double)balance;
		}
		if (type == 668)
		{
			num *= (double)balance;
		}
		if (type == 113 || type == 114)
		{
			num *= (double)balance;
		}
		else if (type == 115)
		{
			num *= (double)balance;
			if (numPlayers > 4)
			{
				knockBackResist = 0f;
			}
			else if (numPlayers > 1)
			{
				knockBackResist *= 1f - boost;
			}
		}
		else if (type == 116)
		{
			num *= (double)balance;

```


---

## 🤖 Assistant · 2026-08-19T03:19:15.720Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Those are life-scaling blocks, not ai0 injection. So who sets ai[0] = -1 for deerclops? Let me check SpawnOnPlayer → it calls SpawnBoss? Actually — check `NewNPC` calls with 668... Player.cs:43232 SpawnOnPlayer. And NPC.SpawnOnPlayer → eventually NewNPC with default ai 0. Hmm — but then when does case -1 run? Search: maybe the natural spawn (SpawnNPC) spawns deerclops with ai0=-1... grep "deerclopsBoss" or the spawn conditions. Actually, maybe case -1 is dead in practice too, OR the summon animation... Let me search Player.cs 43232's SpawnOnPlayer — hmm. Alternatively check NPC.SpawnOnPlayer for special ai injection per type.

Actually — item 5120 is "Pew-maid... " no. Let me think: the Deerclops summon item in 1.4.5 is "Deerclops Talisman"? Hmm, actually item 5120 = "Strange Tarot Card"? No... whatever. The point: SpawnOnPlayer(668) with default ai 0. But wait — maybe SpawnBoss handles: line 81469-ish "SpawnBoss :81472 写 ai[3]" mentioned in comments for mech queen. Let me check NPC.SpawnBoss / SpawnOnPlayer for 668 handling.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:16.673Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public static int SpawnOnPlayer\\|private static int SpawnBoss\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; sed -n '81440,81560p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read SpawnOnPlayer and SpawnBoss for ai injection"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:16.757Z

**📎 ToolResult**

```
		}
		int num = 0;
		for (int i = 0; i < highestNPCSlotIndexWeWillPick; i++)
		{
			if (!Main.npc[i].active)
			{
				num++;
				if (num >= amountWeWant)
				{
					return amountWeWant;
				}
			}
		}
		return num;
	}

	public static IEntitySource GetBossSpawnSource(int targetPlayerIndex)
	{
		return new EntitySource_BossSpawn(Main.player[targetPlayerIndex]);
	}

	public static void SpawnBoss(int spawnPositionX, int spawnPositionY, int Type, int targetPlayerIndex, float ai0 = 0f, float ai1 = 0f, float ai2 = 0f, float ai3 = 0f)
	{
		int maxNPCs = Main.maxNPCs;
		bool flag = Type == 134 || Type == 127 || Type == 126 || Type == 125;
		if (flag)
		{
			AchievementsHelper.MechaMayhem_Clear();
		}
		if (Type == 127 && mechQueen != -1)
		{
			maxNPCs = (mechQueen = NewNPC(GetBossSpawnSource(targetPlayerIndex), spawnPositionX, spawnPositionY, Type, 100, ai0, ai1, ai2, ai3, targetPlayerIndex));
			Main.npc[mechQueen].ai[3] = mechQueen;
		}
		else
		{
			maxNPCs = NewNPC(GetBossSpawnSource(targetPlayerIndex), spawnPositionX, spawnPositionY, Type, 1, ai0, ai1, ai2, ai3, targetPlayerIndex);
		}
		if (maxNPCs == Main.maxNPCs)
		{
			return;
		}
		if (flag)
		{
			AchievementsHelper.MechaMayhem_Start();
		}
		Main.npc[maxNPCs].timeLeft *= 20;
		_ = Main.npc[maxNPCs].TypeName;
		if (Main.netMode == 2 && maxNPCs < Main.maxNPCs)
		{
			NetMessage.SendData(23, -1, -1, null, maxNPCs);
		}
		if (Type == 127 && mechQueen == maxNPCs)
		{
			ChatHelper.BroadcastChatMessage(Lang.misc[107].ToNetworkText(), ChatColors.BossOrEvent);
			return;
		}
		switch (Type)
		{
		case 125:
			ChatHelper.BroadcastChatMessage(Lang.misc[48].ToNetworkText(), ChatColors.BossOrEvent);
			break;
		default:
			ChatHelper.BroadcastChatMessage(NetworkText.FromKey("Announcement.HasAwoken", Main.npc[maxNPCs].GetTypeNetName()), ChatColors.BossOrEvent);
			break;
		case 50:
		case 82:
		case 126:
		case 316:
		case 398:
		case 551:
		case 662:
			break;
		}
	}

	public static void UpdateProtectedSpawnSlots()
	{
		for (int i = 0; i < Main.maxNPCs; i++)
		{
			spawnSlotProtected[i] = Math.Max(Main.npc[i].active ? 2 : (spawnSlotProtected[i] - 1), 0);
		}
	}

	public static int NewNPC(IEntitySource source, int X, int Y, int Type, int Start = 0, float ai0 = 0f, float ai1 = 0f, float ai2 = 0f, float ai3 = 0f, int Target = 255)
	{
		if (Main.getGoodWorld && Main.rand.Next(3) != 0)
		{
			if (Type == 46)
			{
				Type = 614;
			}
			if (Type == 62)
			{
				Type = 66;
			}
		}
		int availableNPCSlot = GetAvailableNPCSlot(Type, Start);
		if (availableNPCSlot >= 0)
		{
			spawnSlotProtected[availableNPCSlot] = 2;
			NPC nPC = new NPC();
			Main.npc[availableNPCSlot] = nPC;
			nPC.whoAmI = availableNPCSlot;
			nPC.ResetForNewNPC();
			nPC.SetDefaults(Type);
			GiveTownUniqueDataToNPCsThatNeedIt(Type, availableNPCSlot);
			nPC.Bottom = new Vector2(X, Y);
			nPC.active = true;
			nPC.timeLeft = (int)((double)activeTime * 1.25);
			if (!nPC.noTileCollide)
			{
				nPC.wet = Collision.WetCollision(nPC.position, nPC.width, nPC.height);
			}
			nPC.ai[0] = ai0;
			nPC.ai[1] = ai1;
			nPC.ai[2] = ai2;
			nPC.ai[3] = ai3;
			nPC.target = Target;
			if (Main.netMode == 2)
			{

```


---

## 🤖 Assistant · 2026-08-19T03:19:20.933Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
SpawnBoss takes ai0 param. Where is SpawnBoss called with Type 668 and ai0=-1? Player.cs:43232 calls SpawnOnPlayer. Let me check SpawnOnPlayer → likely calls SpawnBoss with ai0... Let me grep SpawnOnPlayer definition.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:22.106Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"public static int SpawnOnPlayer\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; sed -n \"$(grep -n 'public static int SpawnOnPlayer' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | cut -d: -f1),+80p\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read SpawnOnPlayer implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:22.172Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: 1: ",+80p
": invalid command code ,

```


---

## 🤖 Assistant · 2026-08-19T03:19:25.407Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"SpawnOnPlayer(int\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Locate SpawnOnPlayer definition line"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:25.449Z

**📎 ToolResult**

```
81273:	public static void SpawnOnPlayer(int plr, int npcType, float ai0 = 0f, float ai1 = 0f, float ai2 = 0f, float ai3 = 0f)

```


---

## 🤖 Assistant · 2026-08-19T03:19:30.096Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '81273,81340p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read SpawnOnPlayer body"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:30.154Z

**📎 ToolResult**

```
	public static void SpawnOnPlayer(int plr, int npcType, float ai0 = 0f, float ai1 = 0f, float ai2 = 0f, float ai3 = 0f)
	{
		if (Main.netMode == 1 || (npcType == 262 && AnyNPCs(262)))
		{
			return;
		}
		switch (npcType)
		{
		case 245:
			if (AnyNPCs(245))
			{
				return;
			}
			try
			{
				int num2 = (int)Main.player[plr].Center.X / 16;
				int num3 = (int)Main.player[plr].Center.Y / 16;
				int num4 = 0;
				int num5 = 0;
				for (int j = num2 - 20; j < num2 + 20; j++)
				{
					for (int k = num3 - 20; k < num3 + 20; k++)
					{
						if (Main.tile[j, k].active() && Main.tile[j, k].type == 237 && Main.tile[j, k].frameX == 18 && Main.tile[j, k].frameY == 0)
						{
							num4 = j;
							num5 = k;
						}
					}
				}
				if (num4 <= 0 || num5 <= 0)
				{
					return;
				}
				int num6 = num5 - 15;
				int num7 = num5 - 15;
				for (int num8 = num5; num8 > num5 - 50; num8--)
				{
					if (WorldGen.SolidTile(num4, num8))
					{
						num6 = num8;
						break;
					}
				}
				for (int l = num5; l < num5 + 50; l++)
				{
					if (WorldGen.SolidTile(num4, l))
					{
						num7 = l;
						break;
					}
				}
				num5 = (num6 + num6 + num7) / 3;
				int num9 = NewNPC(GetBossSpawnSource(plr), num4 * 16 + 8, num5 * 16, npcType);
				Main.npc[num9].target = plr;
				ChatHelper.BroadcastChatMessage(NetworkText.FromKey("Announcement.HasAwoken", Main.npc[num9].GetTypeNetName()), ChatColors.BossOrEvent);
				return;
			}
			catch
			{
				return;
			}
		case 370:
		{
			Player player = Main.player[plr];
			if (!player.active || player.dead)
			{
				return;

```


---

## 🤖 Assistant · 2026-08-19T03:19:39.772Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
SpawnOnPlayer(668) uses default ai0=0 (no special case for 668 shown — let me confirm there's no case 668 in this switch that passes ai0=-1). Let me grep within the SpawnOnPlayer body. Actually easier: check whether ANY caller passes ai0=-1 for 668. Common knowledge: Deerclops spawns walking in from the side of the screen. The natural spawn in vanilla: "SpawnNPC" spawns deerclops offscreen with ai0=-1 so it walks toward the player (the case -1 "入场走位" with speed 5.35). Let me search where NewNPC/SpawnNPC passes -1. Check NPC.cs SpawnNPC region for deerclops (search "668" near "spawn"). Earlier grep of "== 668" found: 17384 (life scale), 18241, 18548, 78581 (IsABoss?), 79758 (NPCLoot?), 82673 (HitEffect). None are spawn injection. So maybe the deerclops natural spawn is via "SpawnNPC" generic offscreen spawn which doesn't set ai... Then case -1 would never trigger?? Hmm.

Wait — maybe case -1 is set by the item at Player.cs:43232? No — SpawnOnPlayer(plr, 668) default ai0 0.

Hmm, then how does deerclops walk in? Let me check SpawnOnPlayer's default branch: maybe generic branch passes... let me read the default case of SpawnOnPlayer.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:40.707Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '81340,81470p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"case\\|ai0\\|default\\|NewNPC\\|SpawnBoss\" | head -40",
 "description": "Scan SpawnOnPlayer switch cases for ai0 usage"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:40.766Z

**📎 ToolResult**

```
8:					int num = NewNPC(GetBossSpawnSource(plr), (int)projectile.Center.X, (int)projectile.Center.Y + 100, 370);
15:		case 398:
19:				NewNPC(GetBossSpawnSource(plr), (int)player2.Center.X, (int)player2.Center.Y - 150, npcType);
92:			SpawnBoss(spawnPositionX, spawnPositionY, npcType, plr, ai0, ai1, ai2, ai3);
122:	public static void SpawnBoss(int spawnPositionX, int spawnPositionY, int Type, int targetPlayerIndex, float ai0 = 0f, float ai1 = 0f, float ai2 = 0f, float ai3 = 0f)

```


---

## 🤖 Assistant · 2026-08-19T03:19:47.850Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No 668-specific ai0. So `SpawnOnPlayer(plr, 668)` → SpawnBoss(..., ai0=0). Deerclops summoned by item starts at ai[0]=0, NOT -1. So where does -1 come from? Possibly the natural blizzard spawn. Let me check the natural spawn: search "deerclops" case-insensitively in SpawnNPC-related code... Earlier grep for ", 668" found only a Gore line. Let me search for "668" more broadly in NPC.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:49.018Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"668\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -v \"82673\\|87303\\|18241\\|18548\\|17384\\|78581\\|79758\\|80155\\|44338\\|44716\\|44788\" | head -20",
 "description": "All remaining 668 references in NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:49.077Z

**📎 ToolResult**

```
30492:					float num668 = 12f;
30498:							num668 += 1f;
30503:							num668 += 1f;
30508:							num668 += 2f;
30513:							num668 += 2f;
30517:					num668 += 3f * num658;
30527:					if (velocity.Y < 0f - num668)
30529:						velocity.Y = 0f - num668;
30531:					if (velocity.Y > num668)
30533:						velocity.Y = num668;
44321:		if (!nPC.active || nPC.type != 668)
44848:		return npcsFoundForCheckActive[668];
45058:		if (!nPC.active || nPC.type != 668)
67390:		case 668:
89029:				for (int num668 = 0; num668 < 50; num668++)
96318:			if (nPC.type != 668)

```


---

## 🤖 Assistant · 2026-08-19T03:19:52.953Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No natural-spawn NewNPC for 668 in NPC.cs with ai0=-1. Let me check Player.cs / other files for ai0=-1 spawn of deerclops. Actually — the deerclops natural spawn might be in Player.cs UpdateBiology / "SpawnBoss via blizzard": search Player.cs for 668.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:54.145Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"668\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs | head; echo ---; grep -rn \"SpawnOnPlayer(.*668\\|SpawnBoss(.*668\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria --include=\"*.cs\" | head",
 "description": "Search all vanilla sources for deerclops spawn with ai"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:54.208Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:7465:			num10 = 668;
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:7533:				QuickSpawnItem(source, 668);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:12666:		if (armor[num4].type == 668 || armor[num5].type == 668)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:20797:					if (nPC.type == 668)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:20858:				if (nPC2.type == 668)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:20917:				if (nPC3.type == 668)
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:41520:			if (nPC.active && ((type == 43 && nPC.type == 4) || (type == 70 && nPC.type == 13) || ((type == 560) & (nPC.type == 50)) || (type == 544 && nPC.type == 125) || (type == 544 && nPC.type == 126) || (type == 556 && nPC.type == 134) || (type == 557 && nPC.type == 127) || (type == 1133 && nPC.type == 222) || (type == 1331 && nPC.type == 266) || (type == 4988 && nPC.type == 657) || (type == 5120 && nPC.type == 668)))
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:43232:				NPC.SpawnOnPlayer(onWhichPlayer, 668);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:43236:				NetMessage.SendData(61, -1, -1, null, whoAmI, 668f);
---
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Main.cs:64610:								NPC.SpawnOnPlayer(num13, 668);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Player.cs:43232:				NPC.SpawnOnPlayer(onWhichPlayer, 668);

```


---

## 🤖 Assistant · 2026-08-19T03:20:49.286Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Player.cs:7465 `num10 = 668` — that's in the natural spawn selection (UpdateTime/SpawnNPC-ish in Player? Actually it's Player.UpdateBiology? No — 7465 is in Player.cs "GetSpawnChanceNPC"? whatever). Main.cs:64610 — `NPC.SpawnOnPlayer(num13, 668)` — natural blizzard spawn, also default ai0=0.

So in vanilla 1.4.5.6, deerclops NEVER spawns with ai[0]=-1! The case -1 handler exists but nothing sets it (maybe multiplayer net-sync from old versions). So our line 59 `if (e.ai0 === -1120) e.ai0 = 0` matches the effective vanilla default. Good — no deviation. And case -1 handling exists in ours too ✓.

Hmm wait — actually let me double check Main.cs:64610 context quickly... it's the blizzard natural spawn. Both use ai0 default 0. OK.

Now let me also verify our `shouldRunAway` vanilla:

```
if (targetData.Type == Player) {
    zoneSnow = player.ZoneSnow;
    zoneSnow |= player.Distance(home) <= 480;
    return (player.dead || (!isChasing && !zoneSnow)) | (Distance(player.Center) >= 2400);
}
if None → true
```
Ours: `if (!p || p.dead) return true;` — vanilla: player.dead → true ✓; !p → Type None → true ✓.
zoneSnow = scene.zoneSnow || dist(player, home) <= 480 ✓.
`if (!isChasing && !zoneSnow) return true;` ✓.
`return dist(e, p) >= 2400` ✓.



Now, let me double check the AI_123 lai3 red dust: vanilla spawn `Dust.NewDustDirect(position, width, height, 109, 0, -3, 0, default, 1.4)` — ours approximates ✓.

Now — our deerclops head check: case 2 rubble srcX uses e.cx (center); vanilla uses Top.ToTileCoordinates() X = position.X (left edge). Deerclops width — check SetDefaults 17384 region: `else if (type == 668)` at 17384 — that was life scaling. The SetDefaults for 668 — let me find. Actually the earlier grep "type == 668" list: 17384 is in a life/damage scaling function. SetDefaults for 668... find "num == 668" or in SetDefaults region. Not critical — the MakeSpikes* use Bottom.ToTileCoordinates → X = Center.X (Bottom = (Center.X, position.Y + height)). Ours uses e.cx ✓ for spikes. Only case 2 rubble uses Top → position.X. Ours uses cx. Offset = width/2. Deerclops width is probably 70 → 35px ≈ 2.2 tiles. The rubble spawns offset by facing*3 tiles from source; using center shifts source ~2 tiles toward facing. Minor numeric — mention as minor if room. Probably not top-10.

Now let me re-examine the remaining significant Golem checks I haven't verified:

A. **Attached head flag48-like noTileCollide**: aiStyle 46 sets `noTileCollide = true` at top ✓ ours never collides anyway.

B. **Free head noTileCollide toggling** — ours never collides; vanilla phases only when can't see player. Minor-medium. Given free head hovers at player-300 and vanilla only collides when it has LOS and is inside... eh. I'll list as minor/存疑? Actually let me think about the practical impact: free head with LOS + noTileCollide=false → it collides with ceiling/floor. If player is in a room, the head can't pass through the ceiling — it would bump. Ours passes through everything always. In the temple (boss arena with ceiling), vanilla head stays inside the room-ish; ours can fly outside through walls. It also matters for flag48/ai1=20 gating... The noTC flag in vanilla affects only collision, not the attack logic. Report as minor CONFIRMED (low severity).

Hmm, wait — actually ours has NO collision at all for the head (attached or free). For the ATTACHED head that's correct (vanilla noTileCollide=true). For free head, vanilla toggles. Ours = always phase. Minor.

C. **Fist despawn when anchor missing**: vanilla golemBoss < 0 → strike 9999 (die). golemBoss only -1 initially before any golem AI ran. After body dies, stale index → fists keep going. Ours: anchor = body alive ? body : head; if both gone → dead. OK-ish.

D. **`e.master = anchor`** for chain rendering — visual.

E. Now — very important one I should double-check: **our body's `dying` state and `hp = e.maxHp`**. If the body enters dying while the attached head is STILL attached (player somehow kills body while head attached — impossible since iframes=2 makes body invulnerable... e.iframes = 2 every tick while hasHead; but wait — the player CAN kill the body if... hmm, iframes=2 set every tick → effectively permanent invulnerability ✓). But what if the head is destroyed and both go free simultaneously... fine.

But here's a subtle bug: our body `hasHead` check requires `n.vanillaId === 246 && n.ai3 !== 1`. When the head goes free, we set e.ai3 = 1 on the HEAD entity (in golemHeadGoFree). But our head ALSO overwrites `e.vanillaId`? No — golemHeadGoFree doesn't change vanillaId (stays 246!). findHead looks for vanillaId 246 OR 249 ✓. But the fist's `anchor = body && !body.dead ? body : head` — findHead finds the freed head (still vanillaId 246) ✓.

But — the freed head keeps vanillaId 246, and our head AI: `if (e.vanillaId === 249) x.free = true` — for a freed 246, x.free was set by golemHeadGoFree ✓ persists via WeakMap ✓.

However — in `golemAI`'s parts scan, freed head (246, ai3=1) correctly excluded from hasHead ✓.

And `spawn(246, -3, -57, 0)` sets p.ai0 = side = 0 for head ✓ (unused).

F. **Freed head damage/defense**: ours sets e.def.damage/defense from vanillaNpc(249) ✓ but maxHp/hp stays 246's. Also knockBackResist etc — fine.

G. **The freed head width/height** stays 70×70 ✓ same as 249.

H. What about `e.def.name`/display? irrelevant.

I. **Free head laser noLosBody when body missing**: vanilla reads stale slot (life 0 → all tiers, and CanHit from stale position...). Ours: rBody null → noLosBody = noLos (head↔player LOS) — reasonable.

Now, let me double-check the **expert mode handling for deerclops hands**: `game.world.isExpert` — vanilla `Main.expertMode` ✓. But note: vanilla also gates `Main.netMode != 1` — fine.

Also **Boss_CanShootExtraAt** semantics: (playerIndex, projectileIdentity?, ...). Hmm, the second arg `num3 % 3` — what is it? Signature: Boss_CanShootExtraAt(int playerIndex, int attackCounter, int maxAttacks, float maxDistance, bool alwaysSkipMainTarget) probably: returns true if this player should be targeted by an "extra" attack in multiplayer beyond the main target, using attackCounter % maxAttacks to distribute. In single player, player 0 is the main target and alwaysSkipMainTarget=false → qualifies when within 1200. So ours' approximation ✓.

Now — **the AI_123 legs** (AI_124_DeerclopsLeg, NPC 669/670): our file doesn't implement legs; presumably rendered procedurally (Renderer.drawDeerclopsGrid). Visual, skip.

Now finalize the Deerclops rubbles frame deviation + passive hands count + maybe case-3 sound/facing tick skew (trivial, skip).

Let me now double-check the **golem attached head stage 0/1 ai1 gate on player**: ours wraps both stages in `if (player)`; vanilla always runs (target = player). When player dead (p null in ours), head stops attacking ✓-ish (vanilla would keep shooting at dead player — TargetClosest keeps them). Minor.

Now — one more important golem body check: **`else if (e.ai1 === -1)` only fires if the FIRST branch `e.ai1 >= 300` didn't fire**. Vanilla identical ✓.

And **the crouch timer**: vanilla during negative ai1, num4 = 1 (boosts skipped) — BUT getGoodWorld +100 is inside `if (ai[1] > 0)` too ✓ ours.

Wait, actually — vanilla: `if (ai[1] > 0f) { ...boosts...; num4 *= num; if (getGoodWorld) num4 += 100 }` — the `num4 *= num` multiply is inside. Ours: `num4 *= num; if (getGoodWorld) num4 += 100;` inside `if (e.ai1 > 0)` ✓.

Also during crouch (ai1 negative): vanilla num4 = 1 (no multiply!) — so crouch decrements... increments by exactly 1 ✓ ours.

**Jump vy**: vanilla: `if (life < lifeMax) { vy = -12.1*(num+9)/10; if (vy < -19.1) vy = -19.1 } else vy = -12.1` ✓ ours exactly.

**Landing sound**: Item14 ✓ ours playSfxWav('Item_14').

OK. Now — did I miss "蓄力跳" nuance: vanilla sets `noTileCollide = true` on jump start (ours x.noTC = true ✓) and TargetClosest before direction ✓ (ours uses dir each tick).

Now, potential missing piece: **vanilla body ai[0]==0 branch requires `velocity.Y == 0`**; ours `if (e.vy === 0)` ✓. But ours wraps in `if (player && ...)` — if p null (dead), no charge. Vanilla charges anyway. Minor.

Now the **golem head free-state balance**: ftwBonus 3 ✓ (:31505-31508 confirms +3).

Now — **deerclops interval Math.round vs (int)**: skip.

**One more deerclops check — case 0 transition order**: ours checks state 4 (both-sides) BEFORE state 1 (forward). Vanilla: state 4 check first (localAI[1] >= 2), then state 1 (flag4). ✓ ours.

But hmm — vanilla state 4 gate: `Math.Abs(vector3.X) < 120 && flag5 && velocity.Y == 0 && localAI[1] >= 2` ✓ ours. And forward: `... && flag4` where flag4 = |dx| >= |dy|*0.6 || len < 48 ✓ ours facingX.

Wait ours line 125: `const facingX = Math.abs(dx) >= Math.abs(dy) * 0.6 || Math.hypot(dx, dy) < 48;` ✓.

Now the spikes: ours `tryMakingSpike` damage 13, angle: `-π/2 + whichOne * dir * 0.7 * (π/4/howMany)` ✓. Spawn pos: `(x*TILE + 8, y*TILE - 8)` ✓ vanilla `new Vector2(num2*16+8, num3*16-8)` ✓.

`walkableAt` = active && !isPlatform — vanilla `WorldGen.ActiveAndWalkableTile` = nactive() && !Main.tileSolid[type]... hmm: ActiveAndWalkableTile: `Main.tile[x,y].nactive() && (Main.tileSolid[...] || Main.tileSolidTop[...])`? Let me check — actually in Terraria source, ActiveAndWalkableTile = tile active && (tileSolid || tileSolidTop)? Hmm. Let me grep WorldGen.ActiveAndWalkableTile definition to verify ours' !isPlatform approximation. Actually ActiveAndWalkableTile(i,j) => `Main.tile[i, j].nactive() && (Main.tileSolid[(int)Main.tile[i, j].type] || Main.tileSolidTop[(int)Main.tile[i, j].type])`? Not sure. Ours: active && !isPlatform — is isPlatform == SolidTop? Probably (tileSolidTop). So ours = active && !solidTop — that EXCLUDES solid tiles?? No wait: walkableAt returns flags!==0 && !isPlatform. For a stone tile: active, not platform → true ✓. For a platform: active, platform → false. For air: false. Vanilla: active && (solid || solidTop)? That would INCLUDE platforms as walkable. Hmm — "ActiveAndWalkableTile" in vanilla: let me check quickly. If vanilla includes platforms but ours excludes them, spikes wouldn't spawn on platforms. Platform in snow biome — rare but player arenas often use platforms! Let me check WorldGen.cs.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:49.637Z · glm-x-preview-260804

```
查 WorldGen.ActiveAndWalkableTile 定义，校对我方 walkableAt 近似。
```


---

## 🤖 Assistant · 2026-08-19T03:20:50.934Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"public static bool ActiveAndWalkableTile\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs; sed -n \"$(grep -n 'public static bool ActiveAndWalkableTile' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs | cut -d: -f1),+6p\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs 2>/dev/null || true",
 "description": "Read ActiveAndWalkableTile definition"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:51.027Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs:70305:	public static bool ActiveAndWalkableTile(int i, int j)
	public static bool ActiveAndWalkableTile(int i, int j)
	{
		try
		{
			Tile tile = Main.tile[i, j];
			if (tile == null)
			{

```


---

## 🤖 Assistant · 2026-08-19T03:20:53.349Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '70305,70340p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "description": "Read full ActiveAndWalkableTile body"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:53.408Z

**📎 ToolResult**

```
	public static bool ActiveAndWalkableTile(int i, int j)
	{
		try
		{
			Tile tile = Main.tile[i, j];
			if (tile == null)
			{
				return true;
			}
			if (tile.active() && Main.tileSolid[tile.type] && !tile.inActive())
			{
				return true;
			}
		}
		catch
		{
		}
		return false;
	}

	public static bool SolidTileAllowTopSlope(int i, int j)
	{
		try
		{
			Tile tile = Main.tile[i, j];
			if (tile == null)
			{
				return true;
			}
			if (tile.active() && (Main.tileSolid[tile.type] || tile.type == 380) && ((!TileID.Sets.Platforms[tile.type] && !tile.bottomSlope()) || (TileID.Sets.Platforms[tile.type] && tile.halfBrick())) && !tile.inActive())
			{
				return true;
			}
		}
		catch
		{

```


---

## 🤖 Assistant · 2026-08-19T03:22:26.924Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
ActiveAndWalkableTile = active && tileSolid && !inActive — SOLID tiles only, platforms EXCLUDED (platforms are tileSolid=false). So ours' `active && !isPlatform` — hmm, that's active && NOT platform. For a non-solid non-platform tile (torch, flower): ours → walkable (true), vanilla → false! Torch is active, not solid, not platform → vanilla false, ours TRUE. So spikes could spawn "on top of" torch tiles in ours. Actually wait — does ours' `st.isPlatform` semantics differ? Ours: `walkableAt = flags !== 0 && !st.isPlatform(x, y)`. For torch: flags active, isPlatform false → walkable=true. Vanilla: false. For platform: ours false ✓ matches. So ours over-includes non-solid decorations. Minor noise-level (spawns a spike near a torch). Skip — too minor for top 10. Hmm, actually solidAt uses isSolid — the walkableAt should be `active && isSolid` to match. But whatever — noise.

Now — let me also double-check **`e.despawnTimer`** exists on Enemy and dayRate. Skip.

Now the **spike 961 lifetime**: ours life=20. Vanilla AI_157 num9=20 → at ai[0] >= 20 → Kill? Let me quickly read 48432-48567 type 961 to verify life=20 and that spikes are 32×32... Actually the prompt's scope for Deerclops is the NPC AI + projectiles 961/962/965 broadly mentioned. I've already spot-checked. The frame claim (rand(5) for 961) — "Projectile.cs:48487-48490, maxValue=5"... wait that's NPC.cs? The comment says AI_157_SharpTears :48432-48567 — that's in Projectile.cs presumably. Out of my audit scope (NPC.cs only per prompt: "标杆(唯一权威):NPC.cs"). The 962 frame deviation IS in NPC.cs (44768-44769) so it's in scope.

Now, let me nail down line numbers for all confirmed findings.

**Finding 1 (Golem, HIGH): 自由头 249 可被击杀且击杀=战斗结束;原版 249 恒无敌,胜利条件=杀本体 245**
- Ours: ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts:416-428 (hp<=0 && x.free → dead + kill 245..249), and 250-257 + 279-294 (body death → 60t 演出后 dead,不终战).
- Vanilla: NPC.cs:12139-12151 (249 SetDefaults ends with `dontTakeDamage = true`), the only resets of dontTakeDamage are SetDefaults preamble :8439 (runs before the type-specific block) and other AI styles; aiStyle 48 block :31500-31741 contains no clear → 249 permanently invulnerable. Vanilla fight end: checkDead→DoDeathEvents case 245 :80146-80148 sets downedGolemBoss. Also fists: AI_047 :19182-19186 golemBoss<0 → strike; golemBoss static (:6052, set :19449) never reset → after body death parts anchor stale corpse slot (vanilla leaves them, but the fight flag is already set).
- Symptom: 玩家可跳过本体直接杀飞头结束战斗(原版不可能);杀本体后战斗不结束(头+拳继续)。
- Fix: 自由态恒设无敌(如每 tick iframes/dontTakeDamage),移除"自由头血尽→全族自毁";本体血尽走正常死亡链(loot+downed flag),部件随本体死清理(或按任务约定保留视觉)。
- Confidence: 高.

**Finding 2 (Golem, MEDIUM): 转自由态满血用 246 的 maxHp(25000)而非 249 的 16000**
- Ours: bossAI_golem.ts:242 (`e.hp = e.maxHp` — maxHp 为 246 的 25000;头变身未换 249 生命池). Also header comment claims "满血+属性对齐 249 SetDefaults" but lifeMax not aligned.
- Vanilla: NPC.cs:12127 (246 lifeMax=25000) vs :12143-12151 (249 lifeMax=16000); HitEffect :85842-85847 NewNPC 249 → fresh 16000.
- Symptom: 二阶段可打目标(现行实现下=自由头)血量虚高 56%。
- Fix: golemHeadGoFree 里把 maxHp/hp 一并换成 vanillaNpc(249) 的 lifeMax。
- Confidence: 高。(若采纳 Finding1 修复则此项自然消失。)

**Finding 3 (Deerclops, MEDIUM): 专家被动影手每轮 2 只,原版 3 只**
- Ours: bossAI_deerclops.ts:84-90 — `idx < 3` 门使 idx==3 不发射,第三只(变体 hint 0)缺失;且 hint=floor(idx)%3 永远只取 1,2。
- Vanilla: NPC.cs:44723-44752 SpawnPassiveShadowHands — `num2 % num != 0 → return; num3 = num2/num; if (num3 >= 3) localAI[2]=0;` reset 之后当拍仍以 num3=3(hint 0)发射一只 → 每轮 3 只(hint 1,2,0)。
- Symptom: 专家/大师下被动影手频率少 1/3,变体 0(0-179 段)永不出现于被动轮。
- Fix: 先判 reset 之外照发:把 `idx < 3` 改为允许 idx==3 发射后再清零(即发射条件去掉 idx<3,发射后 idx>=3 时 lai2=0)。
- Confidence: 高。

**Finding 4 (Deerclops, LOW-MED): 962 碎石变体帧 rand(12) 覆盖全 12 格,原版死代码后实取 6..11**
- Ours: bossAI_deerclops.ts:325-326 (`Math.floor(Math.random() * 12)`),注释 :322-324 断言 6..11 是"误写"。
- Vanilla: NPC.cs:44768-44769:
  ```
  int num5 = Main.rand.Next(Main.projFrames[962] * 4);
  num5 = 6 + Main.rand.Next(6);
  ```
  第二行覆盖第一行 → 实际帧 6..11(3×4 网格的下面两行);注释把死代码当权威反向"修复"。
- Symptom: 碎石视觉变体多了上两行(纯视觉)。
- Fix: 改回 6 + Math.floor(Math.random()*6) 并修正注释。
- Confidence: 高(两行都直接读过)。

**Finding 5 (Golem, LOW): 自由头永不与地形碰撞**
- Ours: bossAI_golem.ts:543-545 (无碰撞直接积分),且 494-540 未实现 noTileCollide 翻转。
- Vanilla: NPC.cs:31515-31524 — `!CanHit(head,player) → noTileCollide=true, flag48=true; else if (noTileCollide && SolidTiles(...)) → noTileCollide=false` → 有视线时头与实心地形碰撞。
- Symptom: 有视线时穿墙(原版会被天花板/墙挡)。
- Fix: 复用本体 collideGround 近似,在 noLos 翻转 noTC。
- Confidence: 高(偏差确认),影响低。

More candidates:

**Finding 6 (Golem, LOW): 挂载头 death→free 时 DamageSound 等属性**... skip.

**Finding 7?** — Golem body when player dead: ours stops charging (gate `if (player && ...)`), vanilla continues. LOW. Also `!player → noTC=true` ✓ good.

**Finding 8?** — Deerclops rubble source X uses center vs vanilla left edge (position.X). LOW noise. Both-sides/forward spikes use Bottom (=Center.X) ✓. Only case 2 uses Top (left edge). Width of 668 — check SetDefaults quickly? Let me not; classify as minor noise, mention in 存疑/minor without a number? The output format wants ≤10 CONFIRMED; I can add a minor list. Actually rubble srcX = center vs left edge: vanilla `base.Top.ToTileCoordinates()` → X=(int)(position.X/16) left edge. Ours center. If width 70 → +35px ≈ +2.2 tiles toward the direction it faces (since +facing*3 applied after). This biases rubble spawn 2 tiles in facing direction. Borderline noise. I'll mention briefly under "minor/存疑" without full finding status.

**Finding 9?** — Deerclops case 3/5 sound+hands same-tick vs vanilla one-tick skew — trivial, skip.

**Finding 10?** — walkableAt over-includes non-solid decorations (torch etc.) — noise, skip into minor list.

Also — should double check one thing about Finding 1's claim "原版杀本体后 249/拳残留": Actually, hold on. Let me reconsider whether killing the BODY in vanilla while the head is STILL ATTACHED is possible — no (invulnerable). And after head detaches, body killable → fight flag. The lingering 249: it remains active, invulnerable, shooting lasers at the player. That's actually vanilla behavior (annoying leftover). Some sources say the head disappears... whatever — code says what it says: no despawn on body death.

Hmm — but wait, there's one more thing to verify for fairness: does vanilla 245's death maybe clear golemBoss? grep showed golemBoss assignments only at 6052 (init -1) and 19449 (set each body AI tick). So no. ✓.

Also verify claim in our header: ":80146 由 245 死亡置 downedGolemBoss" ✓ they knew. The header comment says "自由头血尽 → 全族自毁(战斗结束;原版由 245 死亡置 downedGolemBoss,:80146)" — so they KNEW vanilla sets flag on body death but still chose head-kill as the terminator. The header documents it as "任务约定". Per audit instructions, documented-by-design deviations... the prompt says audit dimensions include 部件联动错. The task background says "联动:本体死→部件死、头被击落后本体可受伤" — that's the AUDITOR's checklist from the task-giver. Our impl: 本体死→部件不死 (head continues); 头被击落后本体可受伤 ✓ that one is right. So the 本体死→部件死 linkage expectation also violated. I'll report Finding 1 as the umbrella: inverted win condition + body-death doesn't end fight/kill parts + head killable.

Now, is there anything about **expert branches for golem**? Vanilla golem AI has NO expert branches (confirmed by reading the four sections — no Main.expertMode references). Ours comments "expert 分支保留注释" — consistent. ✓.

One more check — **our golem body jump: `x.noTC` release logic** placement: vanilla's noTileCollide release happens BEFORE the ai[0] branches each tick (19569-19578) ✓ ours at 323-327 before branches ✓. Condition: `velocity.Y > 0 && Bottom.Y > player.Top.Y` → ours `e.vy > 0 && e.y + e.h > player.y` ✓; `CanHit && !SolidTiles` → ours losClear && !hitSolid ✓.

Also **the body's despawn**: ours `e.dead = true; e.bossFled = true` — vanilla active=false (silent). bossFled flag might suppress loot/announcement ✓ equivalent intent.

Now — one more Deerclops check on `far`/lai3: ours lower-clamps at -10 (documented). Vanilla clamps [0,30]. The -10 floor makes post-entry invuln ramp 40 ticks instead of 30. Trivial.

And **lai3 during ai0=-1**: vanilla sets localAI[3]=-10 each tick in case -1; then Movement. Never reached in practice (nothing sets ai0=-1) — ours same.

OK — and one more important check: **deerclops entry `e.despawnTimer`** — vanilla `timeLeft = 86400` set on home init, decremented by Main.dayRate (=1 normally, 1.5? dayRate is normally 1; in 1.4 it can be up to 1.25? Actually dayRate depends on... it's 1 usually). Fine.

Also — vanilla `if (homeTileX == -1 && homeTileY == -1)` — homeTileX default -1. Ours `if (e.ai2 === 0 && e.ai3 === 0)` — if deerclops spawns at tile x=0 (world edge) → skip. Non-issue.

Now — the last big thing to verify: **our deerclops buff check uses BuffType.Slow = 32?** Our memory note says "Slow buff(78被Poisoned占!)" — hmm, from deerclops-port memory: "Slow buff(78被Poisoned占!)" meaning BuffType.Slow might be mapped differently. The vanilla buff 32 = Slow ("减速"). Ours `BuffType.Slow` and apply 720/60 seconds ✓. Trust it.

Let me also double-check the case 3 scream: vanilla sound DeerclopsScream at ai1==30 (pre-increment check fires when ai1 IS 30 at entry — i.e., tick when ai1=30 entering). Ours: `if (e.ai1 === 30) { playSfxFiles(SCREAM) ... }` at entry ✓ same tick. Vanilla's punch/buff gating `%4==0 && >= 28` post-increment ✓ ours. ✓.

And case 2's `if (e.ai1 === START - 20)` → 12 ✓ (vanilla num9-20 = 12 ✓); `if (e.ai1 === START)` → 32 ✓.

Also — **case 2 rubbles "共 20 颗"**: num10=20, one per tick from since=0..19, ours `shootRubbleUp(..., 20, 1, 200, since)` with loop `for i = step; i < hi && i < 20` — step=floor(since/1)*1=since, hi=since%1===0? since+1:since → since%1 is always 0 → hi=since+1 → i in {since} → 1 per tick ✓ 20 total ✓.

Alright — also confirm **ours case 2 ends at ai1>=60** ✓ vanilla.

**case 1 ends at 80** ✓; **case 4 ends at 90** ✓.

Now Golem fist — one more: vanilla `if (ai[0] == 0f) noTileCollide = true` ✓ ours state 0 x.noTC=true. state 2 keeps prior noTC until pass-axis logic ✓ ours. state 1: vanilla doesn't change noTC in state 1 (set at transition to 2). Ours state 1 doesn't touch noTC except at >=30 sets noTC=true ✓ vanilla `noTileCollide = true` at :19302 before state 2 ✓.

Fist movement for state 0: velocity = toward anchor; ours applies movement `e.x += e.vx` ✓ (vanilla position += velocity by engine).

Fist rotation for state 1: vanilla rotation = 0 ✓ ours e.spin = 0 ✓.

OK — one more potential item: **golem fist `e.ai0` set to side (-1/1) breaks vanilla ai[0] state machine** — ours keeps state in WeakMap, documented. Since ai0 is repurposed and state is in WeakMap, no functional loss except netcode. Fine.

**Attached head `x.l1` (localAI[1])**: ours computes when ai0===1 only — vanilla localAI[1] set in stage 1 each tick ✓; in stage 0 stale — irrelevant.

**Attached head stage 0 fireball dmg**: 18 ✓ — WAIT. Let me double check vanilla num730 = 18 with proj 258 → damage 18. Yes read: `int num730 = 18; int num731 = 258;` ✓ ours 18 ✓.

Stage 1: num739 = 24 dmg ✓.

So the head attacks are all 1:1.

Now — one more possibly-significant thing: **ours attached-head stage gate `e.ai0 = e.hp < e.maxHp / 2 ? 1 : 0`** — after golemHeadGoFree, ai0 was reset to 0; free branch uses ai1/ai2 only ✓ no conflict.

And the free head's `x.l0` mouth frame ✓ visual.

Now — decide the final list (≤10, ordered by severity):

1. [HIGH] Golem 胜利条件倒置/自由头可杀 (golem.ts:416-428, 250-257 vs NPC.cs:12151, 80146-80148)
2. [MED] 自由头血池 25000 vs 16000 (golem.ts:242 vs NPC.cs:12127/12143-12151, 85845)
3. [MED] 专家被动影手 2/3 (deerclops.ts:84-90 vs NPC.cs:44734-44744)
4. [LOW-MED] 962 变体帧 (deerclops.ts:322-326 vs NPC.cs:44768-44769)
5. [LOW] 自由头不撞地形 (golem.ts:494-545 vs NPC.cs:31515-31524)

存疑/次要:
- 拳在本体死后改锚自由头(原版锚 golemBoss 僵尸槽)——与 #1 同簇,若按原版修则应保持锚尸体或直接随本体消亡; ours documented as task convention.
- 本体在玩家死亡时停止蓄力跳 (golem.ts:333 `if (player && ...)`) — vanilla continues charging at dead player's position (NPC.cs:19580+ 无 target 有效性门)。低。
- Deerclops case 2 碎石源 X 用中心而非左缘 (deerclops.ts:161 vs NPC.cs:44558 `base.Top.ToTileCoordinates()`) — 偏 facing 方向 ~2 格。低(数值噪音边缘)。
- walkableAt 把非实心装饰(火把等)当可落地面 (deerclops.ts:26-29 vs WorldGen.cs:70305-70323 应为 active&&tileSolid&&!inActive)。低。
- lai3 下限 -10 导致入场后免伤爬升慢 10t (deerclops.ts:63 vs NPC.cs:44346 clamp 0..30)。trivial。

Wait — before finalizing #3, let me re-verify the vanilla SpawnPassiveShadowHands logic once more from the actual read:

```
private void SpawnPassiveShadowHands(float lifePercent, int shadowHandDamage)
{
    int num = (int)Utils.Remap(lifePercent, 1f, 0f, 80f, 40f);
    localAI[2] += 1f;
    int num2 = (int)localAI[2];
    if (num2 % num != 0) return;
    int num3 = num2 / num;
    if (num2 / num >= 3) localAI[2] = 0f;
    for (int i = 0; i < 255; i++)
        if (Boss_CanShootExtraAt(i, num3 % 3, 3, 1200f, alwaysSkipMainTarget: false))
            spawn hand at player i with ai hint = num3 % 3 (via RandomizeInsanityShadowFor out ai)
}
```
Yes: at num2 = 3*num → num3 = 3 → reset AND spawn with hint 0. So cycle: hints 1, 2, 0 → 3 hands. Ours: 2 hands (1, 2), then reset. Confirmed.

Also Boss_CanShootExtraAt's role: in SP with alwaysSkipMainTarget=false → player 0 within 1200 → true. Ours equivalent ✓.

Now, let me also verify the exact line numbers of vanilla SpawnPassiveShadowHands. From my sed of 44338-44530, the function appeared after ShouldRunAway. ShouldRunAway at :44716-44738 (per our comment), SpawnPassiveShadowHands follows. My earlier grep: "44723-44752" per ours. Let me pin: grep -n "SpawnPassiveShadowHands".

Also pin exact lines: "num5 = 6 + Main.rand.Next(6);" = 44769 ✓ already pinned. The shootRubbleUp in ours is at lines 311-329 with the frame comment 322-326.

Also for Finding 1: ours lines: 416-428 (free-head death → family kill), 249-257 (body dying), and the invuln absence: free branch never sets iframes/dontTakeDamage (lines 430-541). Vanilla: NPC.cs 12139-12151 (249 block with dontTakeDamage=true at 12151). Let me verify 12151 is exactly the dontTakeDamage line: from my SetDefaults read — the 249 block:
```
else if (type == 249)
{
    noGravity = true;
    width = 70; height = 70;
    aiStyle = 48;
    damage = 80; defense = 32;
    lifeMax = 16000;
    HitSound = NPCHit4; DeathSound = NPCDeath14;
    knockBackResist = 0f;
    dontTakeDamage = true;      ← line 12151 per grep ✓
}
```
grep showed 12151: dontTakeDamage = true ✓. And lifeMax 16000 at ~12147. The block start 12139? grep earlier showed "12338: dontTakeDamage = true" too (different type). The 249 `else if` line: I read 12090-12155 — "else if (type == 249)" appeared right after 247/248 block. Counting: 12090 + offset. The sed output line count: 12090 is first line shown. The `else if (type == 249)` line — let me count from the output: lines shown from 12090: 
12090 alpha = 175... 
Let me just grep exact line numbers for "type == 249" and "lifeMax = 16000".
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:22:27.302Z · glm-x-preview-260804

```
核对我方 Finding 3 的原版行号与 249 块的精确行号。
```


---

## 🤖 Assistant · 2026-08-19T03:22:28.159Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private void SpawnPassiveShadowHands\\|private bool ShouldRunAway\\|type == 249\\|lifeMax = 16000\\|lifeMax = 25000\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Pin exact line numbers for findings"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:28.183Z

**📎 ToolResult**

```
12119:			lifeMax = 25000;
12139:		else if (type == 249)
12147:			lifeMax = 16000;
14035:			lifeMax = 25000;
17958:		else if (type == 249)
44712:	private bool ShouldRunAway(ref NPCAimedTarget targetData, bool isChasing)
44730:	private void SpawnPassiveShadowHands(float lifePercent, int shadowHandDamage)
85871:				else if (type == 249)

```


---

## 🤖 Assistant · 2026-08-19T03:22:52.956Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Confirmed:
- 249 block: NPC.cs:12139-12152, lifeMax=16000 at :12147, dontTakeDamage=true at :12151.
- 246 lifeMax=25000 at :12119.
- SpawnPassiveShadowHands at :44730-44752.
- ShouldRunAway :44712-44728.

Also 17958 — `else if (type == 249)` in the scale *= 0.5 block (our comment cites 17943-17960) ✓.

One more sanity check on our golem: `e.iframes = 2` for body invulnerability while head attached — does iframes block ALL damage in our engine (including the intent to be fully invulnerable)? Presumably (they used the same trick in dying). Fine.

Now double-check Finding 5's vanilla lines: aiStyle 48 block starts 31500; the flag48 logic:
```
31503: bool flag48 = false;
31504: float num755 = GetMyBalance();
...
31515: if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
31516: {
31517:     noTileCollide = true;
31518:     flag48 = true;
31519: }
31520: else if (noTileCollide && Collision.SolidTiles(position, width, height))
31521: {
31522:     noTileCollide = false;
31523: }
```
From my sed output starting at 31500: line 31500 = "else if (aiStyle == 48)"... let me count: the output began "else if (aiStyle == 48)" as line 31500? My sed -n '31500,31760p' printed starting with "		else if (aiStyle == 48)" — yes line 31500. Then:
31501 {
31502 bool flag48 = false;
31503 float num755 = GetMyBalance();
31504 if (Main.getGoodWorld)
31505 {
31506 num755 += 3f;
31507 }
31508 if ((!Main.player[target]...
31509-31511 ×2 block
31512 }
31513 if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
31514 {
31515 noTileCollide = true;
31516 flag48 = true;
31517 }
31518 else if (noTileCollide && Collision.SolidTiles(position, width, height))
31519 {
31520 noTileCollide = false;
31521 }
31522 if (golemBoss < 0)...
Hmm — grep said 31521: `if (golemBoss < 0)`. Let me recount: grep result "31521: if (golemBoss < 0)". So flag48 block = ~31513-31521. Our file's comment says "flag48(:31503-31515)". Close enough; I'll cite 31513-31521 (approx). Let me verify precisely.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:22:53.986Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '31512,31524p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | cat -n",
 "description": "Pin exact flag48 lines in aiStyle 48"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:54.020Z

**📎 ToolResult**

```
     1				if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
     2				{
     3					noTileCollide = true;
     4					flag48 = true;
     5				}
     6				else if (noTileCollide && Collision.SolidTiles(position, width, height))
     7				{
     8					noTileCollide = false;
     9				}
    10				if (golemBoss < 0)
    11				{
    12					StrikeNPCNoInteraction(9999, 0f, 0);
    13					return;

```


---

## 🤖 Assistant · 2026-08-19T03:23:04.396Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
flag48 block = NPC.cs:31512-31520.

Now let me do a couple of final spot-checks on things I haven't fully verified:

1. Our golem body's torch smash gate: vanilla `Main.netMode != 1 && Main.getGoodWorld && velocity.Y > 0` ✓ ours.

2. Our `fadeAlpha` sets `e.spawnAlpha` — visual only.

3. Deerclops: `if (e.aiT % 2 === 0)`... not deerclops, that's golem fist dust `Main.rand.Next(2) == 0` ≈ 50% vs ours every-2-ticks — visual noise.

4. Golem fist: vanilla state 2 `if (num2 > 700f || collideX || collideY)` — num2 is distance from anchor computed BEFORE movement. Ours `dist > 700` with dist also computed before the state machine ✓.

BUT — one subtle thing: ours computes `dist` ONCE before the branches using tx,ty from the CURRENT anchor position. Vanilla likewise (vector2.Length() computed once before branches) ✓.

5. Deerclops movement: ours integrates position inside deerclopsMovement ✓ (vanilla engine does it after AI). Equivalent.

6. Deerclops `punch()` — ours' punch ignores x,y — vanilla PunchCameraModifier position-based but effect is camera shake ✓.

7. Deerclops scream sound set: SCREAM array = deerclops_scream_0/1/2 — vanilla SoundID.DeerclopsScream — fine.

Now — one thing I should double check for Finding 1 fairness: does OUR engine treat `e.dontTakeDamage` on Enemy as actual invulnerability? deerclops uses it (lai3>=30). For golem they used iframes=2. If our Enemy has dontTakeDamage honored by the damage path, then the fix suggestion is trivial. Let me grep Enemy for dontTakeDamage usage.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:23:05.471Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dontTakeDamage\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head; grep -rn \"dontTakeDamage\" ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts 2>/dev/null | head -5; grep -rln \"dontTakeDamage\" ~/Project/GLM/SandboxWorld/game/src | head",
 "description": "Check how our engine honors dontTakeDamage"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:23:05.513Z

**📎 ToolResult**

```
795:    // 266 克脑 SetDefaults :12372 dontTakeDamage=true——一阶段（爬行者存活）不可击，
797:    if (id === 266) e.dontTakeDamage = true;
798:    // 263 世纪之花钩蔓 SetDefaults :12331-12332 dontTakeDamage=true——恒不可击
800:    if (id === 263) e.dontTakeDamage = true;
801:    // 690 雕像宝箱怪 SetDefaults :17615-17627 immortal+dontTakeDamage=true——伪装态
803:    if (id === 690) e.dontTakeDamage = true;
1006:  /** 原版 NPC.dontTakeDamage（SetDefaults 静态置位，如 266 克脑 :12372 一阶段
1008:  dontTakeDamage = false;
1371:    //      渐隐期 dontTakeDamage + 每 tick 2 颗 228 紫尘（noGravity/noLight/scale 2）----
1375:        this.dontTakeDamage = this.spawnAlpha > 0;    // :51381-51382
~/Project/GLM/SandboxWorld/game/src/render/Renderer.ts
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_deerclops.ts
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lategame.ts
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts
~/Project/GLM/SandboxWorld/game/src/entities/Minecart.ts
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts

```


---

## 🤖 Assistant · 2026-08-19T03:23:19.759Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Enemy.ts line 1006-1008: `dontTakeDamage = false;` — wait, that resets it per tick? Line 1008 `dontTakeDamage = false;` — in what method? If it's reset at the start of each AI tick (like vanilla's pattern of AI setting it each tick), then deerclops setting it each tick works, and a golem free head could set it each tick too. Interesting: bossAI_golem.ts is in the list of files using dontTakeDamage — where? Let me grep in golem file... I read the whole file — no "dontTakeDamage" appears. Oh — the grep -rln matched files containing the string; bossAI_golem.ts contains it? Let me check: my read of the file shows no dontTakeDamage... wait, line 308 comment: "dontTakeDamage = 挂载头在场(NPC.cs:19513)" — the comment mentions it. OK.

Line 1006-1008 context: let me check quickly what method resets dontTakeDamage=false. If it's reset per-tick before AI dispatch, then our golem body's iframes=2 approach vs deerclops' assignment both work.

Not critical. Let me check line 1000-1010 to be sure the reset exists per tick (so that the deerclops AI setting it works and golem could too).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:23:20.159Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '995,1020p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read dontTakeDamage reset context in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:23:20.182Z

**📎 ToolResult**

```
  /** 点光像素坐标覆盖（缺省=实体中心）：光源不在中心格的原版语义位——
   *  火把僵尸 590/591 手持火把（NPC.cs:57309-57366，±22/±36px 偏移格） */
  lightRGBAt: { x: number; y: number } | null = null;
  lai0 = 0;              // localAI 语义位（萤火虫：闪烁间隔计时）
  lai1 = 0;              // localAI 语义位（萤火虫：发光剩余帧）
  lai2 = 0;              // localAI[2] 语义位（AI_054 克脑：二阶段入场演出门）
  lai3 = 0;              // localAI[3] 语义位（AI_054 克脑：玩家死/离场下坠计数；AI_008 法师 32：RedHat 变体带 +3）
  /** 红帽骷髅王标记（NPC.cs:81262-81266 redHatMode 召唤置 ai[3]=1；RedHatSkeletron
   *  AdjustmentsEnabled :67282 消费）。本仓 Chippy 沙发召唤链未实装 → 恒 false，
   *  32 的 lai3 变体带/双倍计时因此不触发（常态=单一头饰形态，2026-08-17 帧修复的门） */
  redHat = false;
  /** 原版 NPC.dontTakeDamage（SetDefaults 静态置位，如 266 克脑 :12372 一阶段
   *  不可击；AI 段自行清除）。与 iframes 不同：持续态而非帧计数 */
  dontTakeDamage = false;
  /** 击退抗性运行时覆写（游泳族专用）：461 wet→0 / dry→0.4（难度曲线，
   *  NPC.cs:56366/:56412 GetKnockbackMultiplier_ScaledByDifficulty）；null=用 def 值 */
  kbResistOverride: number | null = null;
  /** 694 水书宝箱怪专用帧计数（FindFrame case 694 frameCounter，态切换清零） */
  npcFrameT = 0;
  /** AI 侧算定的帧号直读位（694 态机帧；null=走渲染端 vanillaFrameIdx 通用档） */
  customFrameIdx: number | null = null;
  /** 运行时 noGravity 位（原版 NPC.noGravity 逐 tick 置位，StrikeNPC :82217/:82228
   *  受击档读【运行时值】非静态表）：AI_017 秃鹫(:24079 飞行态 true/栖息 0 态 false)、
   *  AI_087 珍珑宝箱怪(:39525 起始 false、4/4.1/5 空中态 true)、AI_091 花岗岩元素
   *  (:40688 起始 true、-1 石化态 false)在各自 AI 内同步置位；hurt() 读
   *  noGravity || def.flying（def.flying=静态兜底，覆盖数据 noGravity 族与

```


---

## 🤖 Assistant · 2026-08-19T03:24:09.738Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
OK — `dontTakeDamage` is a persistent field on Enemy ("持续态而非帧计数"), honored by hurt(). Deerclops sets it each tick ✓. For the golem fix suggestion, free head could set `e.dontTakeDamage = true` persistently.

Also note Enemy.ts:797 — spawn-side already sets dontTakeDamage for 266/263/690 by vanillaId. It does NOT set it for 249 (nor does our golemHeadGoFree). If the engine spawned a literal 249... line 191 list included 668 — what's that list? Probably boss ids. Anyway.

I have enough for the report. Let me also double-check one loose end I claimed: "attached head ai0 stage gate" — ours line 491 `e.ai0 = e.hp < e.maxHp / 2 ? 1 : 0;` — placed INSIDE `if (player)`. Vanilla runs it unconditionally. When player dead → stage frozen. Trivial.

One more check on our Finding 3 fix suggestion — ours:
```
e.lai2 += 1;
const idx = e.lai2 / interval;
if (e.lai2 % interval === 0 && idx < 3 && dist < 1200) { spawn(hint = floor(idx) % 3); }
if (idx >= 3) e.lai2 = 0;
```
Minimal fix: remove `idx < 3` from the spawn condition (so idx==3 spawns hint 0) — keep reset after. That yields hints 1,2,0 per cycle ✓ matches vanilla.

Also double check interval edge: interval could be 0 if lifePct... 40+40*lifePct ≥ 40 — Math.round ≥ 40, `|| 40` guard for NaN. fine.

Now — severity ordering. The prompt wants ≤10, by severity. I'll report 5 CONFIRMED + 存疑 list.

Actually — wait. I should double-check one more possible structural issue in our golem head: **`findBody` for the ATTACHED head also matches a body in dying state** — body dying → ai3=1 → head goes free immediately at death start ✓ (documented "本体死透后头继续" — actually goes free at death START, comment says 死透后 but code triggers on ai3===1 immediately). Whatever — same cluster.

And **free head `if (e.hp <= 0)` check happens before the props switch each tick** — with Finding 1's fix irrelevant.

Also — hmm, one more scenario for Finding 1: our free head death → kills family including a body that's mid-dying. Fine.

Let me also double check that our body really is damage-blocking via iframes: `if (hasHead) e.iframes = 2;` — every tick refresh. If our engine decrements iframes per tick and blocks damage when >0 ✓ standard. OK.

Now for completeness, the Deerclops audit "玩家死亡/走远回家语义" — verified ✓ matches (case 0 → 6 → go home; despawnTimer → 8 → silent despawn; home teleport via case 7). ✓

"专家分支" for deerclops: passive hands ✓ found deviation #3; case 5 hands damage 15 ✓ vanilla (num=15) — wait, actually for EXPERT the scream damage... vanilla num=15 is used for case 5 hands regardless of expert; ours DMG_HANDS=15 ✓.

Hmm — one more expert nuance: vanilla hand damage num is the plain `int num = 15` — not scaled by difficulty (difficulty scaling happens projectile-side via Main.DifficultyDamageScale? hostile projectile damage gets scaled at hit time by difficulty in vanilla Player.Hurt via projectile damage scaling... whatever, our engine may scale too). Skip.

Final check on our Golem file header claim "挂载头 246 ... NPC.cs:31273-31499" — I read 31265-31500: aiStyle 46 block starts at 31272 (`else if (aiStyle == 46)`)... close enough (31273 = `{`). ✓ Comments' line numbers are accurate — good.

One last verification for Finding 2: does our engine scale maxHp at spawn (e.g., expert ×2)? If our spawner multiplies 246's lifeMax by difficulty, freed head inherits the scaled 25000-equivalent — still wrong pool (should be 16000-based scaled). The vanilla 249 NewNPC would also get difficulty scaling on ITS 16000. So the ratio stands. ✓

Also — hmm, one more thing: in vanilla, when 246 dies → NewNPC 249 spawns at head's position with FULL 16000. Our in-place transform heals the head to full of 25000. Both "heal to full" — vanilla also full-heals (fresh NPC). So the only delta is the pool size. ✓ (Some might think vanilla frees head with remaining HP — no, it's full.)

Ready to write the report. Structure:

## Golem
核了什么: AI_045 (19447-19722) 全段逐行对照本体蓄力跳/无敌门/断臂尘/砸火把/3000 脱离;AI_047 (19171-19446) 全段;aiStyle 46 (31272-31499) 与 48 (31500-31741) 全段;SetDefaults 245-249 (12095-12152);HitEffect (85830-85870);DoDeathEvents (80146);golemBoss 静态 (6052/19449) 复位语义;dontTakeDamage 全文件清除点排查。

CONFIRMED #1, #2, #5. 没问题的部分:蓄力跳全数值链(300/-20/-1、num4 加成、跳速 -12.1×(num+9)/10 钳 -19.1)、落地音/双侧激光 259(11/12 速、28 伤、±18/±30*scale、+3*速度提前量、timeLeft 300)、嘴弹 258(18/24/20 伤、8 速)、自由头悬浮 7/0.05 双步进、火焰弹/激光全部分档阈值(0.8/0.6/0.2/0.1 与 1.25~1/6 与 0.5~0.1)、flag48/49 语义、拳全状态机(14→32、60、30、12→48、700 回收、过轴关碰撞、±84/78 肩锚、247/248 镜像 atan2 方向)、FTW 砸火把含 Y 上界 width 笔误 1:1——全部吻合。

## Deerclops
核了什么:AI_123 主状态机 (44338-44710) 全部九态逐条、ShouldRunAway (44712-44728)、SpawnPassiveShadowHands (44730-44752)、ShootRubbleUp (44754-44777)、MakeSpikesForward/BothSides (44779-44843)、TryMakingSpike+FindBestY (44870-44955)、Movement (44957-45042)、SetDefaults/spawn 链(SpawnOnPlayer 81273→SpawnBoss 无 ai0=-1 注入,case -1 原版同样无来源)。

CONFIRMED #3, #4. 没问题:选招五门顺序与条件(|dx|<120+nearVert+lai1≥2→双侧、facingX→前刺、240/90/120 档、Slow 免疫门)、尖刺 LEAD 36/56+每 4/2t+20/15 根、961 角度/伤害 13/ai1 尺度、碎石 32 起 20 颗/8+rand8 速/200 upBias、咆哮 800px Slow 720t、回家 halt 420/600、深 1600px→300t 传送/1500t、ai1==40 落点 Bottom 传送、离场 life=-1 静默消散、Movement 全链(3.5+rage、±80 停、-1 入场 5.35、40×20/40×16 探针、±8/16 钳、跳 -8)全对上。

存疑列表:
1. 拳死后锚定(任务约定 vs 原版僵尸槽)
2. 本体死亡 60t 演出(任务约定发明)
3. case 2 碎石源 X 用中心 vs 原版左缘(偏 ~2 格,噪音级)
4. walkableAt 把非实心非平台块(火把)算可行走(应 active&&solid)
5. lai3 下限 -10(入场后免伤爬升慢 10t)
6. golem 本体玩家死时停止蓄力(原版继续朝尸体蓄力)
7. deerclops 桥 acceptTopSurfaces 未建模(平台不算地面)

Wait — should I count #7 into CONFIRMED? "Movement 的 acceptTopSurfaces" — vanilla `Collision.SolidCollision(vector, w, h, acceptTopSurfaces)` where acceptTopSurfaces = Bottom.Y >= rect.Top && !flag4. With acceptTopSurfaces=true, solidTop platforms count. Ours ignores. It IS a real branch omission in an audit dimension (地面行走语义). But impact: deerclops in snow on natural terrain rarely on platforms; player arenas use platforms though — deerclops would fall through platforms in ours? Ours: ground probes only check isSolid (platforms excluded unless isSolid includes them...). In this repo, per memory "平台站立穿透修复 — tileSolid∩tileSolidTop{19,239,380,427}恒可站" — isSolid likely excludes platforms. So ours: deerclops treats platforms as non-ground (falls through), vanilla treats them as ground when boss bottom at/below target top (which is the common case when walking toward a player standing on platforms!). Actually acceptTopSurfaces = boss's Bottom.Y >= target.Top — when the boss is below the player's top (typical), true → platforms count as solid for the ground probes. So vanilla deerclops walks ON platforms; ours falls through. That's a genuine behavioral deviation worth listing as CONFIRMED #6-ish. Hmm, but it depends on our solidCollisionPx — `st.isSolid(i,j)` — does our isSolid include platforms? Need to check store.isSolid. Let me check quickly.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:10.103Z · glm-x-preview-260804

```
Movement 里 acceptTopSurfaces 我方未建模——需确认我方 isSolid 是否含平台。
```


---

## 🤖 Assistant · 2026-08-19T03:24:11.347Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"isSolid\" ~/Project/GLM/SandboxWorld/game/src/world/*.ts 2>/dev/null | head -5; grep -rn \"isSolid(x: number, y: number)\\|isSolid(tx\\|isSolid(i\" ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts 2>/dev/null | head -3; ls ~/Project/GLM/SandboxWorld/game/src/world/ | head -20",
 "description": "Locate isSolid implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:11.385Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/BossSummonStations.ts:26:    if (st.inBounds(ax, y) && st.isSolid(ax, y)) { up = y; break; }
~/Project/GLM/SandboxWorld/game/src/world/BossSummonStations.ts:29:    if (st.inBounds(ax, y) && st.isSolid(ax, y)) { down = y; break; }
~/Project/GLM/SandboxWorld/game/src/world/MeteorFall.ts:45:const isSolidSheet = (st: TileStore, idx: number): boolean => {
~/Project/GLM/SandboxWorld/game/src/world/MeteorFall.ts:108:      set(x, y, isSolidSheet(st, idx) ? type : 0);
~/Project/GLM/SandboxWorld/game/src/world/MeteorFall.ts:138:          && isSolidSheet(st, st.idx(x + dx, y + dy));
~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts:111:  isSolid(x: number, y: number): boolean {
audit
Banners.ts
BossSummonStations.ts
CrackedBricks.ts
Door.ts
DropBait.ts
Eclipse.ts
evolution
Extractinator.ts
FlexibleTileWands.ts
FurnitureItems.ts
FurnitureStyle.ts
gen
golf
hive.ts
Housing.ts
Invasion.ts
JourneyPowers.ts
LanternNight.ts
liquid

```


---

## 🤖 Assistant · 2026-08-19T03:24:17.495Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '100,135p' ~/Project/GLM/SandboxWorld/game/src/world/TileStore.ts",
 "description": "Read isSolid and isPlatform implementations"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:17.517Z

**📎 ToolResult**

```
  isActive(x: number, y: number): boolean {
    // 原版 nactive() = active && !inActive（Tile.cs:383-394）：已致动格视为不活跃
    return this.inBounds(x, y) && this.type[this.idx(x, y)] !== 0
      && (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) === 0;
  }

  /** 原版 inActive()：致动器翻转后的"缩入地下"态（有 type 但不碰撞不阻挡） */
  isActuated(x: number, y: number): boolean {
    return this.inBounds(x, y) && (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) !== 0;
  }

  isSolid(x: number, y: number): boolean {
    if (!this.inBounds(x, y)) return false; // 世界外视为空（边缘自由）
    if (this.wire[this.idx(x, y)] & TileStore.WIRE_ACTUATED) return false; // 已致动不碰撞
    const d = TILE_DEFS[this.type[this.idx(x, y)]];
    return !!d && d.solid;
  }

  /** 站顶单向面（原版 Collision.TileCollision :2330-2333 的 flag 门：
   *  `flag = tileSolid[type]; if (tileSolidTop[type] && frameY == 0) flag = true`
   *  分两族语义——
   *  ① 平台行为族 = tileSolid∩tileSolidTop 四件套（Main.cs:7841/:9568/:9570/:9888）：
   *    19 平台/239 矿锭/380 花盆箱/427 团队平台。flag=tileSolid **恒真**——其 frameY 是
   *    材质行（PlaceTile case 19/380 `frameY = 18*style`，TileFrameImportant 只重写
   *    frameX 连接形态），**可站与 frameY 无关**。曾把家具的 frameY==0 门套到平台族
   *    → 世界生成放的 13+ 材质平台（CaveHouse/HouseBuilder PlatformStyle）全体穿透。
   *  ② 家具族（tileSolid=false：桌/铁砧/工作台/钢琴/书架/笼子等）：frameY==0=底行
   *    才可站，上半格（frameY>0）不站。
   *  nactive 门（:2327）：已致动(inActive)的平台/家具顶不可站。
   *  单向性（X 轴/上顶不拦）由消费端保证：TileCollision X/上顶分支不查 isPlatform。
   *  注：SolidCollision(acceptTopSurfaces) :2771 对 Platforms 集合改用
   *  PlatformProperTopFrame(frameX)——该查询路径本仓无消费者，不移植（登记）。 */
  isPlatform(x: number, y: number): boolean {
    if (!this.inBounds(x, y)) return false;
    const i = this.idx(x, y);
    if (this.wire[i] & TileStore.WIRE_ACTUATED) return false;   // nactive()（致动=不可站）

```


---

## 🤖 Assistant · 2026-08-19T03:24:43.923Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So our `isSolid` uses `d.solid` — platforms (19 etc.) have solid=false in TILE_DEFS (they're solidTop). So:

- deerclops `solidCollisionPx` (isSolid-based) excludes platforms → boss's ground probes never register platforms as ground. Vanilla: with acceptTopSurfaces=true (which is true whenever boss bottom >= target top — the common walking-at-player case), Collision.SolidCollision counts platforms as solid. So vanilla deerclops treats platforms as ground while chasing a player standing on them; ours falls through / keeps gravity. CONFIRMED (medium-low). The comment in TileStore even notes: "注:SolidCollision(acceptTopSurfaces) :2771 对 Platforms 集合改用 PlatformProperTopFrame(frameX)——该查询路径本仓无消费者,不移植(登记)" — they consciously skipped acceptTopSurfaces path as "no consumer" — but deerclops IS a consumer (bossAI_deerclops implements SolidCollision with acceptTopSurfaces semantics by hand and got it wrong/omitted). 

Also the same acceptTopSurfaces applies to the straddle/flag probes AND flag7 (open ahead) in Movement — vanilla passes acceptTopSurfaces to ALL THREE SolidCollision calls. Ours uses plain solid for all. Also vanilla SolidCollision with acceptTopSurfaces=false ignores... wait — what does acceptTopSurfaces actually do exactly? In Collision.SolidCollision(Vector2 position, int width, int height, bool acceptTopSurfaces = false): tiles that are tileSolidTop (platforms) are only counted when acceptTopSurfaces is true AND proper top frame. Also for half-bricks/slopes? The deerclops usage: `acceptTopSurfaces = base.Bottom.Y >= rectangle.Top && !flag4` — when boss's bottom is below the target's top (i.e., roughly same level or below) and not teleporting. So when the boss and player are on the same platform level, platforms count as ground → boss walks on the arena platform floor. When boss is ABOVE the target (Bottom above target top — e.g., player below), platforms don't count → boss falls through platforms to reach the player below. Clever vanilla pathing. Ours: platforms never count → boss always falls through platforms (then keeps falling since below may be air; movement has no tile collision at all — it only probes to set vy! Note: our deerclopsMovement integrates position directly with NO collision resolution — the "ground" probe only zeroes vy when flag5. If boss is above a platform-only floor: probes false → vy grows → falls through floor forever until solid ground far below (gravity else-branch clamps 16). So on a platform arena over a drop, our deerclops falls out of the arena. Vanilla would stand on platforms while player is level. This is a real behavioral deviation in ground-walk semantics.

I'll add as CONFIRMED #5 or so (medium). Given max 10, fine.

Also NOTE: vanilla flag3 `(vector.Y + 20 < rectangle.Y + Height - 16)` — ours ✓.

OK, let me also double-check that vanilla `Collision.SolidCollision` with acceptTopSurfaces only adds platforms, not remove anything — yes.

Now, finalize. One more possible check: our `solidAt` for rubble/spike uses isSolid — vanilla WorldGen.SolidTile = active && tileSolid && !inActive ✓ matches (isSolid includes actuated check ✓).

`walkableAt` = flags!==0 && !isPlatform — hmm wait, flags!==0 means "has type" but doesn't exclude actuated! vanilla ActiveAndWalkableTile requires !inActive. Ours' flags check: `st.flags[st.idx(x,y)] !== 0` — per earlier code, `st.type[idx] !== 0` is the active check; flags might be a different array (active flags). In solidAt they use `st.flags[st.idx(x,y)] !== 0 && !!st.isSolid(x,y)` — and isSolid checks actuated. For walkableAt: `flags !== 0 && !isPlatform` — isPlatform returns false for actuated ✓, so actuated platforms → walkable? actuated tile: vanilla → not active → false; ours: flags!==0 (type exists) && !isPlatform(actuated→false) → TRUE. Minor inconsistency; plus non-solid decorations count as walkable. I'll fold these into one minor note.

Enough. Write the final report now.

Order by severity:
1. Golem 胜利条件倒置(自由头可杀且杀头=终战;原版 249 恒无敌、杀本体=终战) — 高
2. Golem 自由头血池 25000 vs 16000 — 中高(依附#1但独立成立)
3. Deerclops 专家被动影手每轮缺第三只 — 中
4. Deerclops Movement 漏 acceptTopSurfaces(平台不算地面) — 中低
5. Deerclops 962 碎石变体帧 rand(12) vs 6..11(注释把死代码当权威) — 低
6. Golem 自由头永不撞地形 — 低

存疑:
- 拳在本体死后锚自由头(任务约定"锚定本体(或头)" vs 原版锚 golemBoss 僵尸槽)——与#1同簇
- 本体死亡 60t 演出+满血续命(任务约定发明;原版 checkDead 即死)
- 本体在玩家死亡时停止蓄力/跳跃(我方 p=null 门;原版继续)
- case 2 碎石源 X 用中心,原版 Top=左缘(~2 格偏移)
- walkableAt 把火把等非实心装饰当可行走面、致动格未排除(原版 active&&solid&&!inActive)
- lai3 下限 -10(原版 clamp 0..30)→入场后免伤爬升慢 10t

Also mention verified-clean summary per boss.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:25:23.968Z · glm-x-preview-260804

````
审计完成。以下为最终报告。

---

# Boss AI 1:1 抽查审计报告(Golem + Deerclops)

## Golem(bossAI_golem.ts vs NPC.cs)

**核了什么**:AI_045 本体(19447-19722)、AI_047 拳(19171-19446)、aiStyle 46 挂载头(31272-31499)、aiStyle 48 自由头(31500-31741)四段全部逐行对照;外加 SetDefaults 245-249(12095-12152)、HitEffect 246→249(85830-85870)、DoDeathEvents case 245(80146-80148)、`golemBoss` 静态索引全文件引用排查(6052/19449,从不复位)、`dontTakeDamage` 全部清除点排查(8439=SetDefaults 前导，非逐帧)。

**对得上的**(抽样全绿)：蓄力跳全链(300→-20→-1、断臂/残血 num4 加成、跳速 -12.1×(num+9)/10 钳 -19.1、穿墙跳、落地 Item14)、FTW 砸火把含“Y 上界用 width”原版笔误 1:1、嘴弹 258(伤 18/24/20、速 8)、挂载头双侧/单眼激光 259(±18·11 速 / ±30·12 速、伤 28、+3×速度提前量、timeLeft 300)、自由头悬浮 7/0.05 含符号翻转双步进(accelTo 已实现)、火焰弹/激光全部分档阈值(0.8/0.6/0.2/0.1;1.25~1/6;0.5~0.1)、flag48(ai1=20)/flag49(×1.5 伤/×2.5 速/速度预判)语义、拳全状态机(14→32 归位速、60 蓄力、30 钉肩、12→48 冲拳速、700 回收、过轴关碰撞、±84/78 肩锚、247/248 的 atan2 镜像方向、出拳侧别门)。注释行号抽验全部属实。

**CONFIRMED 偏差**：

1. **胜利条件整体倒置：自由头可被击杀且“杀自由头=全族自毁终战”；原版 249 恒无敌，终战=杀本体** — 高
   - 我方:`bossAI_golem.ts:416-428`(自由头 hp≤0 → `e.dead=true` + 灭 245-249 全家)、`:250-257` + `:279-294`(本体血尽只走 60t 死亡演出，头/拳继续战斗，不终战)。
   - 原版:`NPC.cs:12151`(249 SetDefaults 末行 `dontTakeDamage = true`),aiStyle 48 全段(31500-31741)无任何清除；文件里 `dontTakeDamage=false` 的清除点全在 SetDefaults 前导(8439)或其他 AI 风格内 → 249 永久免击。终战标志在 `DoDeathEvents` case 245(NPC.cs:80146-80148 `SetEventFlagCleared(ref downedGolemBoss, 6)`)。
   - 症状：玩家可跳过本体直接杀飞头结束战斗(原版不可能)；反过来杀掉本体后战斗不结束，飞头+双拳继续。
   - 最小修复：自由态每 tick 置 `e.dontTakeDamage = true`(Enemy 已有该字段且 hurt() 尊重)，删除“自由头血尽→全族自毁”分支；本体血尽走正常死亡链(loot+downed)。
   - 置信度：高(两侧均直读)。

2. **转自由态满血用了 246 的血池(25000)而非 249 的(16000)** — 中高(独立成立，即使不采纳 #1)
   - 我方:`bossAI_golem.ts:242`(`e.hp = e.maxHp`,maxHp 是 246 的;`:430-439` 只对齐了 damage/defense,头注释“属性对齐 249 SetDefaults”名不副实——lifeMax 没换)。
   - 原版:`NPC.cs:12119`(246 lifeMax=25000)vs `:12147`(249 lifeMax=16000);`:85845` HitEffect 是全新 NewNPC 249 → 满的 16000。
   - 症状：现行实现下二阶段可击目标血量虚高 ~56%。
   - 最小修复：golemHeadGoFree 里同时换 `e.maxHp = vanillaNpc(249).lifeMax`(按本仓难度缩放口径)，再 `e.hp = e.maxHp`。
   - 置信度：高。

3. **自由头永不与地形碰撞** — 低
   - 我方:`bossAI_golem.ts:494-545`(自由态无任何碰撞，直接积分)。
   - 原版:`NPC.cs:31512-31520`——头↔玩家无视线→`noTileCollide=true`;否则若当前穿墙中且身处实心块→`noTileCollide=false`(即有视线时会被天花板/墙阻挡)。
   - 症状：有视线时也穿墙，神庙房间内可飞出墙外。
   - 最小修复：自由态按该二分支维护 noTC,有视线时套用 collideGround 近似。
   - 置信度：高(偏差确认)，影响低。

## Deerclops(bossAI_deerclops.ts vs NPC.cs)

**核了什么**：AI_123 主状态机(44338-44710)九态逐条、ShouldRunAway(44712-44728)、SpawnPassiveShadowHands(44730-44752)、ShootRubbleUp(44754-44777)、MakeSpikesForward/BothSides(44779-44843)、TryMakingSpike+FindBestY(44870-44955)、Movement(44957-45042);外加召唤链(SpawnOnPlayer 81273→SpawnBoss 81550,确认原版召唤/自然刷新均不注入 ai0=-1,case -1 在原版同样无触发来源——我方 -1120→0 映射无偏差)、DoDeathEvents 668(80155)。

**对得上的**(抽样全绿)：选招五门的顺序与全部条件(|dx|<120+nearVert+lai1≥2→双侧、facingX→前刺、240 碎石、90 影手、120+Slow 免疫+|dx|>100 咆哮)、尖刺 LEAD 36/56+每 4/2t+20/15 根+双侧镜像 whichOne=-i、961 角度公式/伤 13/ai1 尺度 0.1+rand0.1+xOffset·1.1/howMany、碎石 32 起共 20 颗/8+rand8 速/upBias 200、咆哮 800px Slow(32) 720t+每 4t 震屏、回家语义全链(halt 420/600、深 1600px→300t 转 7、远离 1500t、ai1==40 Bottom 落点传送、timeLeft 86400→8 静默消散 life=-1)、Movement 主体(3.5+rage、±80 停、入场 5.35、40×20/40×16 探针、-8/+0.8/-0.4/±0.4/16 全钳位、跳 -8+ai1 落地门)、影手伤害 15/10。

**CONFIRMED 偏差**：

4. **专家被动影手每轮 2 只，原版 3 只** — 中
   - 我方:`bossAI_deerclops.ts:84-90`——`idx < 3` 门把 idx==3 的第三只(hint 0 变体段)挡掉了；`floor(idx)%3` 因此永远只取 1、2。
   - 原版:`NPC.cs:44730-44752`——`num2 % num != 0 → return; num3 = num2/num; if (num3 >= 3) localAI[2]=0;` **复位之后当拍仍以 num3=3(hint 0)照发** → 每轮 3 只(hint 1,2,0)。
   - 症状：专家/大师下被动影手频率少 1/3,0-179 变体段在被动轮永不出现。
   - 最小修复：发射条件去掉 `idx < 3`(发射后再执行 `idx >= 3 → lai2 = 0`)。
   - 置信度：高。

5. **Movement 漏 `acceptTopSurfaces`(平台不算地面)** — 中低
   - 我方:`bossAI_deerclops.ts:32-44,366-368`——三处 solidCollisionPx 恒用 `isSolid`(本仓平台 solid=false),无 acceptTopSurfaces 概念。
   - 原版:`NPC.cs:45016` `acceptTopSurfaces = base.Bottom.Y >= rectangle.Top && !flag4`,三个 SolidCollision 探针(45020-45024)全部带此参——追击同层玩家时平台算地面，鹿角怪能站在平台竞技场上。
   - 症状：平台上战斗时鹿角怪穿台坠落(且 Movement 无碰撞解析，会一路掉出场地)。
   - 最小修复：solidCollisionPx 加 acceptTopSurfaces 形参，true 时把 isPlatform 格计入；三处调用按原式传 `e.y+e.h >= ty && !teleporting`。注：TileStore.ts isPlatform 注释声称“该查询路径本仓无消费者”，本函数就是被漏掉的消费者。
   - 置信度：高(偏差确认)。

6. **962 碎石变体帧 rand(12) 全 12 格，原版实取 6..11;注释把死代码当权威反向“修复”** — 低
   - 我方:`bossAI_deerclops.ts:322-326`(`Math.floor(Math.random()*12)`,注释断言 6..11 是“误写”)。
   - 原版:`NPC.cs:44768-44769` 两行连写：
     ```csharp
     int num5 = Main.rand.Next(Main.projFrames[962] * 4);
     num5 = 6 + Main.rand.Next(6);
     ```
     第二行覆盖第一行 → 生效值 6..11(3×4 网格下两行)。
   - 症状：纯视觉(碎石变体多了上两行)。
   - 最小修复：改回 `6 + Math.floor(Math.random()*6)` 并改注释。
   - 置信度：高(两行都直读)。

## 存疑(不单独定级)

- **拳在本体死透后锚自由头**(golem.ts:565-569):文件头称“任务约定：锚定本体(或头)”；原版锚 `golemBoss` 僵尸槽(静态从不复位，部件锚在尸体冻结位)。与 #1 同簇——若按原版修胜利条件，此约定建议一并复核。
- **本体 60t 死亡演出+满血续命**(golem.ts:250-257):任务约定发明，原版 checkDead 当拍即死。
- **玩家死亡时本体停止蓄力**(golem.ts:333/359 的 `if (player …)` 门；本仓 p 死亡即 null):原版无 target 有效性门，继续朝尸体蓄力跳。低影响。
- **case 2 碎石源 X 用中心**(deerclops.ts:161)vs 原版 `base.Top.ToTileCoordinates()` 取左缘(NPC.cs:44558)——朝 facing 方向偏 ~2 格，噪音级。
- **walkableAt 语义偏宽**(deerclops.ts:26-29):原版 `active && tileSolid && !inActive`(WorldGen.cs:70305-70323);我方把火把等非实心装饰也算“可行走尖刺落点”，且致动格未排除。噪音级。
- **lai3 下限 -10**(deerclops.ts:63,注释自认)：原版 clamp(0,30)(NPC.cs:44346)——入场态后免伤爬升慢 10t。trivial。
- **Deerclops 尖刺 961/影手 965 的 Projectile 侧细节**(寿命 20/480、RandomizeInsanityShadowFor 单人近似)本次仅抽查，未对 Projectile.cs 逐行——如需可另开。
````
