# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T03:09:24.348Z

```
你在 ~/Project/GLM/SandboxWorld 做泰拉瑞亚 1.4.5.6 复刻的 Boss AI 1:1 抽查审计。**严格只读:禁止编辑任何文件、禁止跑游戏/vite/测试。**

标杆(唯一权威):~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs(96369 行)
我方:~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts

背景:我方是手工移植;文件注释里引用的 "cs:NNNNN" 就是上面这份 NPC.cs 的行号。我方 ai0..ai3 = 原版 npc.ai[0..3],localAI ≈ localAI[i],bInit ≈ 出生初始化段。专家/大师门:mainExpertMode() ≈ Main.expertMode。

你负责审计整个文件,重点(按优先级):
1. DukeFishron(猪鲨 370,aiStyle 69 → AI_069_DukeFishron @49143-50128):冲刺链计数、专家/大师分支、半血变身(传送+狂暴)、死亡掉落门;鲨鱼龙/sharkron(372/373,aiStyle 71 @35196)、爆裂泡泡(371,aiStyle 70 @35122)
2. MoonLord 家族:
   - 核心 398(aiStyle 77 @36774-37198):双手死前无敌、藏地演出、真死亡时序
   - 手 397(aiStyle 78 @37199-37711):攻击表(横扫/拍击/死光)、睁眼可击窗口
   - 头 396(aiStyle 79 @37712-38128):第三只眼死亡之光/吸血鞭
3. 相互联动:头/手/眼死亡顺序、core 等待门(双手+头死才进二阶段)、flee(白天/玩家死)语义

审计维度(抓结构性偏差,不是数值噪音):
- 状态机阶段与转换(计时器/血量阈值/专家大师分支门漏掉或写错)
- 移动物理(冲刺速度档/悬浮/传送节奏)
- 攻击循环参数(弹幕 id/速度/计数/连发间隔;猪鲨 expert 变体弹)
- 玩家死亡/Boss 离场(flee)语义有无原版出处
- 部件联动(手锚定/眼睛建)

方法:先 Read 我方对应函数,再 sed -n '起,止p' 读原版对应段对照,不要泛读全文。注释声称的行号要抽验(注释可能撒谎/过时)。

输出格式(最终回复直接文本,不写文件):
逐 Boss 一节:"核了什么+发现什么"。每条 CONFIRMED 偏差给:我方文件:行号 / 原版 NPC.cs 行号 / 症状 / 最小修复建议 / 置信度(高/中/低)。没问题的 Boss 一句话带过。存疑单列。最多报 10 条,按严重度排序。禁止编造行号——每条 CONFIRMED 必须两边都真实读过。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T03:09:24.350Z

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

## 🤖 Assistant · 2026-08-19T03:09:26.811Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by reading our file bossAI_duke_moonlord.ts, then compare against the decompiled NPC.cs at the given line ranges.

Let me first check the size of our file, then read it.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:27.871Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Count lines in both files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:27.898Z

**📎 ToolResult**

```
    1634 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts
   96369 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs
   98003 total

```


---

## 🤖 Assistant · 2026-08-19T03:09:35.229Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read our file first.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:35.230Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:35.579Z

**📎 ToolResult**

```
1	// Boss AI 1:1 移植(二):猪鲨鱼龙 AI_069(NPC 370)与月亮领主 aiStyle 77/78/79(NPC 398 核心 / 397 手 / 396 头)。
2	// 源码:Terarria1456(1.4.5.6)NPC.cs ——
3	//   猪鲨 AI_069_DukeFishron        :49143-50127
4	//   月总核心 aiStyle 77(398)      :36774-37198
5	//   月总手   aiStyle 78(397)      :37199-37711
6	//   月总头   aiStyle 79(396)      :37712-38128
7	//   攻击时间表 MoonLordAttacksArray :6830-6946 / MoonLordAttacksArray2 :6948-6987
8	//   死亡转换 checkDead             :78841-78867(396/397 血尽→ai0=-2 闭眼残肢+召真眼;398 血尽→ai0=2 死亡演出)
9	//   鲨鱼 NPC aiStyle 71(372/373)  :35196-35328(升空蓄力 90t→16 速扑咬,撞墙即死)
10	// 弹体(原版 Projectile.cs 1:1,本文件内实现为投射桶实体):
11	//   龙卷水弹 385 aiStyle 65        :28402-28482(小:斜落/大:追踪玩家 50px 引爆)+ Kill 落龙卷 :70714-70778
12	//   鲨鱼龙卷 384/386 aiStyle 64    :28287-28398(逐段向上生长,周期 NewNPC 372/373 出鲨)
13	//   死亡之光 455 aiStyle 84        :30291-30549(锚源 NPC 眼部,±2π/540 每 t 扫射,180t 寿命,
14	//                                  Colliding 线段判定 :14673-14682,命中伤害 = NewProjectile 伤 ×2 :13781)
15	// 经典模式主链 1:1;getGoodWorld 分支已实装(月总头死亡之光收束尾 30 连射 1021,
16	// :37940-37950;猪鲨 AI_069 与月总手/核心 1456 无 g 分支);expert 分支保留注释;
17	// netcode 跳过。
18	// 无敌语义:dontTakeDamage 用 e.iframes=2 每 tick 刷新近似(同 bossAI.ts 克脑一阶段)。
19	import type { Enemy } from './Enemy';
20	import type { GameHooks } from './types';
21	import type { Player } from './Player';
22	import type { Camera } from '../render/Camera';
23	import type { Renderer } from '../render/Renderer';
24	import { Entity } from './Entity';
25	import { TILE } from '../core/constants';
26	import { spawnPart, shoot, accelTo, losClear } from './bossAI';
27	import { projSprite, projFrameCount } from './Arrow';
28	import { BuffType } from '../stats/Buffs';
29	
30	// ---------------------------------------------------------------------------
31	// 通用工具
32	// ---------------------------------------------------------------------------
33	
34	/** Boss 伤害/防御基值缓存(状态机每 tick 从基值派生临时修正,防重复乘膨胀) */
35	const baseStats = new WeakMap<Enemy, { dmg: number; def: number }>();
36	const baseOf = (e: Enemy) => {
37	  let b = baseStats.get(e);
38	  if (!b) { b = { dmg: e.def.damage, def: e.def.defense ?? 0 }; baseStats.set(e, b); }
39	  return b;
40	};
41	
42	const TAU = Math.PI * 2;
43	const clamp = (v: number, lo: number, hi: number) => (v < lo ? lo : v > hi ? hi : v);
44	const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
45	/** 标量区间平滑(驱动向量 SmoothStep 的 amount 因子) */
46	const smoothAmt = (t: number) => {
47	  t = clamp(t, 0, 1);
48	  return t * t * (3 - 2 * t);
49	};
50	/** 原版 Vector2.SmoothStep(cur, target, amount):Lerp(amount²(3-2amount)) */
51	const vSmoothStep = (cur: number, target: number, amount: number) => lerp(cur, target, smoothAmt(amount));
52	/** 角度插值(原版 float.AngleLerp:取最短方向步进) */
53	const angleLerp = (cur: number, target: number, t: number) => {
54	  let d = target - cur;
55	  while (d > Math.PI) d -= TAU;
56	  while (d < -Math.PI) d += TAU;
57	  return cur + d * t;
58	};
59	
60	/** 原版 SimpleFlyMovement(:78100)+ 速度折半混合(月总 8/0.5+Lerp0.5 的组合写法):
61	 *  先单轴步进逼近目标速度,再与步进前速度做 0.5 Lerp(等效步长减半) */
62	const flyLerp = (e: Enemy, tx: number, ty: number, acc: number) => {
63	  const ox = e.vx, oy = e.vy;
64	  e.vx = accelTo(e.vx, tx, acc);
65	  e.vy = accelTo(e.vy, ty, acc);
66	  e.vx = lerp(ox, e.vx, 0.5);
67	  e.vy = lerp(oy, e.vy, 0.5);
68	};
69	
70	/** 每实例附加槽位(原版 direction/spriteDirection/localAI/frameCounter 等无对应 Enemy 字段) */
71	interface DukeX { dir: number; spr: number }
72	const dukeX = new WeakMap<Enemy, DukeX>();
73	const dukeOf = (e: Enemy): DukeX => {
74	  let x = dukeX.get(e);
75	  if (!x) { x = { dir: 1, spr: 1 }; dukeX.set(e, x); }
76	  return x;
77	};
78	interface HandX { frame: number; l0: number; l1: number }
79	const handX = new WeakMap<Enemy, HandX>();
80	const handOf = (e: Enemy): HandX => {
81	  let x = handX.get(e);
82	  if (!x) { x = { frame: 0, l0: 0, l1: 0 }; handX.set(e, x); }
83	  return x;
84	};
85	interface HeadX { f2: number; f3: number; l0: number; l1: number; l2: number }
86	const headX = new WeakMap<Enemy, HeadX>();
87	const headOf = (e: Enemy): HeadX => {
88	  let x = headX.get(e);
89	  if (!x) { x = { f2: 0, f3: 0, l0: 0, l1: 0, l2: 0 }; headX.set(e, x); }
90	  return x;
91	};
92	
93	/** 实心块内判定(原版 Collision.SolidCollision 的中心点近似) */
94	const inSolid = (game: GameHooks, e: Enemy): boolean => {
95	  const st = game.world.store;
96	  const tx = Math.floor(e.cx / TILE), ty = Math.floor(e.cy / TILE);
97	  return st.inBounds(tx, ty) && st.isSolid(tx, ty);
98	};
99	
100	/** 原版"攻击时间表"推进(NPC.cs :37229-37251 / :37740-37762 / :38243-38264 同构):
101	 *  ai1 全局计时,逐槽累计时长定位当前槽;全部槽走完回绕 ai1=0。
102	 *  注意:只回写 ai1,不写 ai0——手/头由调用方把槽攻击号赋给 ai0(即其状态),
103	 *  核心二阶段 ai0 是相位状态(0/1/2/3),绝不能被攻击号覆盖。 */
104	function attackSlot(e: Enemy, table: ReadonlyArray<readonly [number, number]>): { atk: number; inSlot: number; dur: number } {
105	  let slot = 0, consumed = 0;
106	  while (slot < table.length) {
107	    const dur = table[slot][1];
108	    if (dur + consumed > e.ai1) break;
109	    consumed += dur;
110	    slot++;
111	  }
112	  if (slot === table.length) { slot = 0; e.ai1 = 0; consumed = 0; }
113	  const atk = table[slot][0];
114	  return { atk, inSlot: e.ai1 - consumed, dur: table[slot][1] };
115	}
116	
117	// ---------------------------------------------------------------------------
118	// AI_069 猪鲨鱼龙(NPC 370,NPC.cs:49143-50127)
119	// ---------------------------------------------------------------------------
120	// 状态 ai0:-1 出生(75t) → 一阶段循环 0 悬浮(num3 t)→1 冲撞(num6 t)×5→2 泡泡弹(80t)
121	//   →3 鲨鱼龙卷(90t);血 ≤50% →4 变身(180t) →5 二阶段循环:0→6 冲撞→7 旋转泡泡冲刺(120t)
122	//   →8 鲨鱼龙卷;9(expert 15% 血)二段变身(180t) →10 隐身悬浮→11 冲撞/12 瞬移(30t)/13 旋转冲刺。
123	// 经典参数:悬浮 60t/0.45/7.5、冲撞 30t@16 速、泡泡 80t 每 4t 一发、龙卷 90t(60t 时发射)、变身 180t。
124	
125	const DUKE = {
126	  spawnT: 75,          // num21 :49215
127	  hoverT: 60,          // num3  :49168(经典)
128	  hoverAcc: 0.45,      // num4  :49169
129	  hoverSpd: 7.5,       // num5  :49170
130	  chargeT: 30,         // num6  :49187
131	  chargeSpd: 16,       // num7  :49188
132	  bubbleT: 80,         // num8  :49202
133	  bubbleEvery: 4,      // num9  :49203
134	  bubbleAcc: 0.3,      // num10 :49204
135	  bubbleSpd: 5,        // num11 :49205
136	  nadoT: 90,           // num12 :49206
137	  p1T: 180,            // num13 :49207(一→二阶段变身)
138	  p2T: 180,            // num14 :49208(二段狂暴变身,expert)
139	  teleT: 30,           // num15 :49209(瞬移)
140	  spinT: 120,          // num16 :49210(旋转冲刺)
141	  spinEvery: 4,        // num17 :49211
142	  spinBubbleSpd: 6,    // num18 :49212
143	  spinDashSpd: 20,     // num19 :49213
144	};
145	/** 旋转冲刺角速度 num20 = 2π/(num16/2) = 2π/60(:49214) */
146	const DUKE_SPIN_RATE = TAU / (DUKE.spinT / 2);
147	
148	/** 狂暴判定 flag6(:49238):玩家在太空(y<800)/地下(y>worldSurface*16)/离开两侧海洋带 */
149	function dukeEnraged(game: GameHooks, player: Player): boolean {
150	  const st = game.world.store;
151	  const surface = (game.world.groundLevel || Math.floor(st.h * 0.3)) * TILE;
152	  return player.y < 800 || player.y > surface ||
153	    (player.x > 6400 && player.x < st.w * TILE - 6400);
154	}
155	
156	/** 一阶段悬浮结束的下一招(:49471-49542) */
157	function dukePick1(e: Enemy, enraged: boolean): number {
158	  const a3 = Math.floor(e.ai3);
159	  let next = 0; // 0=无事(原版 switch 无匹配分支,ai2 继续累计)
160	  if (a3 >= 0 && a3 <= 9) next = 1;          // 冲撞
161	  else if (a3 === 10) { e.ai3 = 1; next = 2; } // 泡泡弹
162	  else if (a3 === 11) { e.ai3 = 0; next = 3; } // 鲨鱼龙卷
163	  if (enraged && next === 2) next = 3;       // :49495 狂暴时泡泡弹换龙卷
164	  if (e.hp <= e.maxHp * 0.5) next = 4;       // :49499 半血变身
165	  return next;
166	}
167	/** 二阶段悬浮结束的下一招(:49736-49809) */
168	function dukePick2(e: Enemy, enraged: boolean): number {
169	  const a3 = Math.floor(e.ai3);
170	  let next = 0;
171	  if (a3 >= 0 && a3 <= 5) next = 1;          // 冲撞(6)
172	  else if (a3 === 6) { e.ai3 = 1; next = 2; } // 旋转泡泡冲刺(7)
173	  else if (a3 === 7) { e.ai3 = 0; next = 3; } // 鲨鱼龙卷(8)
174	  // flag2(expert hp≤15%):next=4 → ai0=9(:49756-49759)——经典模式不可达,代码保留见 dukeState9
175	  if (enraged && next === 2) next = 3;       // :49760
176	  return next;
177	}
178	/** 冲撞起手(:49503-49520 / :49764-49781 / :49988-50004 同构):定速直冲+朝向修正 */
179	function dukeCharge(e: Enemy, player: Player, spd: number, toState: number, st: DukeX) {
180	  const dx = player.cx - e.cx, dy = player.cy - e.cy;
181	  const d = Math.hypot(dx, dy) || 1;
182	  e.vx = (dx / d) * spd;
183	  e.vy = (dy / d) * spd;
184	  e.ai0 = toState; e.ai1 = 0; e.ai2 = 0;
185	  e.spin = Math.atan2(e.vy, e.vx);
186	  const s = Math.sign(dx) || st.dir;
187	  st.dir = s;
188	  if (st.spr === 1) e.spin += Math.PI;
189	  st.spr = -s;
190	}
191	/** 悬浮段共用(:49415-49468 / :49680-49733 / :49932-49967 同构):
192	 *  目标点 = 玩家 + (ai1 侧偏, -200);desired = normalize(目标-自身-速度)*spd 后 SimpleFlyMovement */
193	function dukeHover(e: Enemy, player: Player, acc: number, spd: number, sideOff: number, st: DukeX) {
194	  if (e.ai1 === 0) e.ai1 = sideOff * Math.sign(e.cx - player.cx || 1);
195	  const dx = player.cx + e.ai1 - e.cx - e.vx;
196	  const dy = player.cy - 200 - e.cy - e.vy;
197	  const d = Math.hypot(dx, dy) || 1;
198	  e.vx = accelTo(e.vx, (dx / d) * spd, acc);
199	  e.vy = accelTo(e.vy, (dy / d) * spd, acc);
200	  const s = Math.sign(player.cx - e.cx) || st.dir;
201	  if (e.ai2 === 0 && s !== st.dir) e.spin += Math.PI;
202	  st.dir = s;
203	  if (st.spr !== -st.dir) e.spin += Math.PI;
204	  st.spr = -st.dir;
205	}
206	
207	/** AI_069 主入口(经典模式) */
208	export function dukeFishronAI(e: Enemy, game: GameHooks, player: Player | null) {
209	  const st = dukeOf(e);
210	  if (!e.bInit) { e.bInit = true; e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; e.spawnAlpha = 255; } // :49247-49257
211	  const b = baseOf(e);
212	  const enraged = player ? dukeEnraged(game, player) : false;
213	  const flag = e.hp <= e.maxHp * 0.5;                       // flag  :49147 二阶段
214	  const flag3 = e.ai0 > 4;                                  // flag3 :49149(二阶段状态 5-13)
215	  const flag4 = e.ai0 > 9;                                  // flag4 :49150(expert 狂暴段 10-13)
216	  const flag5 = e.ai3 < (flag3 ? 3 : 5) * 2;                // flag5 :49151-49152
217	
218	  // 伤害/防御修正(:49153-49167 + 狂暴 :49239-49245)——每 tick 从基值派生
219	  if (flag4) { e.def.damage = Math.round(b.dmg * 1.1); e.def.defense = 0; }
220	  else if (flag3) { e.def.damage = Math.round(b.dmg * 1.2); e.def.defense = Math.round(b.def * 0.8); }
221	  else { e.def.damage = b.dmg; e.def.defense = b.def; }
222	  if (enraged) { e.def.damage = b.dmg * 2; e.def.defense = b.def * 2; }
223	
224	  // 悬浮/冲撞参数(:49168-49201;expert 档注释)
225	  let hoverT = DUKE.hoverT, hoverAcc = DUKE.hoverAcc, hoverSpd = DUKE.hoverSpd;
226	  if (flag4) { hoverAcc = 0.7; hoverSpd = 12; hoverT = 30; }            // :49171-49176
227	  else if (flag3 && flag5) { hoverAcc = 0.5; hoverSpd = 8; hoverT = 20; } // :49177-49182
228	  else if (flag5 && !flag3 && !flag4) hoverT = 30;                       // :49183-49186
229	  let chargeT = DUKE.chargeT, chargeSpd = DUKE.chargeSpd;
230	  if (flag4) { chargeT = 25; chargeSpd = 27; }                           // :49189-49193(expert 同档)
231	  if (enraged) { hoverT = 10; chargeSpd += 6; }                          // :49239-49245
232	
233	  // 玩家死/远离 5600px(:49218-49237):减速升空离场(原版另 EncourageDespawn(10);
234	  // 本工程 Boss 不参与 despawn 块,故仅保留升空)。原版此处无回血逻辑。
235	  if (!player || player.dead || Math.hypot(player.cx - e.cx, player.cy - e.cy) > 5600) {
236	    e.vy -= 0.4;
237	    e.encourageDespawn(10); // :49234 急升逃离 + EncourageDespawn(10)
238	    e.ai0 = e.ai0 > 4 ? 5 : 0;
239	    e.ai2 = 0;
240	    e.x += e.vx; e.y += e.vy;
241	    return;
242	  }
243	
244	  // ---- 身体旋转朝向(:49258-49345)----
245	  let target = Math.atan2(player.cy - e.cy, player.cx - e.cx);
246	  if (st.spr === 1) target += Math.PI;
247	  if (target < 0) target += TAU; else if (target > TAU) target -= TAU;
248	  if (e.ai0 === -1 || e.ai0 === 3 || e.ai0 === 4 || e.ai0 === 8) target = 0; // :49271-49286
249	  let step = 0.04;                                                            // num23 :49287
250	  if (e.ai0 === 1 || e.ai0 === 6 || e.ai0 === 7) step = 0;                    // :49288-49295
251	  if (e.ai0 === 3 || e.ai0 === 4 || e.ai0 === 8) step = 0.01;                 // :49296-49307
252	  let rot = e.spin;
253	  if (rot < target) rot += (target - rot > Math.PI ? -step : step);
254	  if (rot > target) rot += (rot - target > Math.PI ? step : -step);
255	  if (rot > target - step && rot < target + step) rot = target;
256	  if (rot < 0) rot += TAU; else if (rot > TAU) rot -= TAU;
257	  if (rot > target - step && rot < target + step) rot = target;
258	  e.spin = rot;
259	
260	  // ---- 透明度(:49346-49364 + 各状态内分支;近似为 spawnAlpha 渐变) ----
261	  if (e.ai0 !== -1 && e.ai0 < 9) e.spawnAlpha = inSolid(game, e) ? Math.min(255, e.spawnAlpha + 15) : Math.max(0, e.spawnAlpha - 15);
262	
263	  let invuln = false; // flag7(dontTakeDamage = !flag7,:50126)
264	  switch (e.ai0) {
265	    case -1: { // 出生(:49365-49414)
266	      invuln = true;
267	      e.vx *= 0.98; e.vy *= 0.98;
268	      const s = Math.sign(player.cx - e.cx) || st.dir;
269	      st.dir = s; st.spr = -s;
270	      if (e.ai2 > 20) {
271	        e.vy = -2;
272	        e.spawnAlpha = clamp(e.spawnAlpha - 5 + (inSolid(game, e) ? 15 : 0), 0, 150); // :49375-49391
273	      } else if (e.spawnAlpha < 255) e.spawnAlpha = 255;
274	      if (e.ai2 === DUKE.nadoT - 30) { // :49392 出生尘环
275	        game.spawnParticles(e.cx, e.cy, '#8FD8FF', 18, 2.4, { life: 40 });
276	        game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49404 PlaySound(29,…,20) 满响(曾借 roar 0.8)
277	      }
278	      e.ai2 += 1;
279	      if (e.ai2 >= DUKE.spawnT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; }
280	      break;
281	    }
282	    case 0: { // 一阶段悬浮(:49415-49543)
283	      if (player.dead) break;
284	      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
285	      e.ai2 += 1;
286	      if (e.ai2 >= hoverT) {
287	        const next = dukePick1(e, enraged);
288	        if (next === 1) dukeCharge(e, player, chargeSpd, 1, st);
289	        else if (next === 2) { e.ai0 = 2; e.ai1 = 0; e.ai2 = 0; }
290	        else if (next === 3) {
291	          e.ai0 = 3; e.ai1 = 0; e.ai2 = 0;
292	          if (enraged) e.ai2 = DUKE.nadoT - 40; // :49530-49533 狂暴跳过前摇
293	        } else if (next === 4) { e.ai0 = 4; e.ai1 = 0; e.ai2 = 0; }
294	      }
295	      break;
296	    }
297	    case 1: { // 冲撞(:49544-49566)
298	      game.spawnParticles(e.cx + e.w / 2 - Math.cos(e.spin) * e.w * 0.3, e.cy + e.h / 2 - Math.sin(e.spin) * e.h * 0.3, '#8FD8FF', 2, 1.5, { life: 18 });
299	      e.ai2 += 1;
300	      if (e.ai2 >= chargeT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 += 2; }
301	      break;
302	    }
303	    case 2: { // 泡泡弹幕(:49567-49637)
304	      if (player.dead) break;
305	      if (e.ai1 === 0) e.ai1 = 300 * Math.sign(e.cx - player.cx || 1);
306	      const dx = player.cx + e.ai1 - e.cx - e.vx;
307	      const dy = player.cy - 200 - e.cy - e.vy;
308	      const d = Math.hypot(dx, dy) || 1;
309	      e.vx = accelTo(e.vx, (dx / d) * DUKE.bubbleSpd, DUKE.bubbleAcc);
310	      e.vy = accelTo(e.vy, (dy / d) * DUKE.bubbleSpd, DUKE.bubbleAcc);
311	      if (e.ai2 === 0) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49608 PlaySound(29,…,20) 满响(曾借 roar 0.5)
312	      if (e.ai2 % DUKE.bubbleEvery === 0) { // :49610-49618 每 4t 吐一颗爆裂泡泡(NPC 371)
313	        const ddx = player.cx - e.cx, ddy = player.cy - e.cy;
314	        const dd = Math.hypot(ddx, ddy) || 1;
315	        const bub = spawnPart(game, e, 371);
316	        if (bub) {
317	          bub.x = e.cx + (ddx / dd) * ((e.w + 20) / 2) - bub.w / 2;
318	          bub.y = e.cy + (ddy / dd) * ((e.w + 20) / 2) + 45 - bub.h / 2;
319	        }
320	      }
321	      const s = Math.sign(player.cx - e.cx) || st.dir;
322	      st.dir = s; st.spr = -s;
323	      e.ai2 += 1;
324	      if (e.ai2 >= DUKE.bubbleT) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; }
325	      break;
326	    }
327	    case 3: dukeSharknado(e, game, player, st, false); break;          // :49638-49660
328	    case 4: { // 一→二阶段变身(:49661-49679)
329	      invuln = true;
330	      e.vx *= 0.98;
331	      e.vy = lerp(e.vy, 0, 0.02);
332	      if (e.ai2 === DUKE.p1T - 60) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49668 PlaySound(29,…,20)(曾借 roar 0.9)
333	      e.ai2 += 1;
334	      if (e.ai2 >= DUKE.p1T) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
335	      break;
336	    }
337	    case 5: { // 二阶段悬浮(:49680-49811)
338	      if (player.dead) break;
339	      dukeHover(e, player, hoverAcc, hoverSpd, 300, st);
340	      e.ai2 += 1;
341	      if (e.ai2 >= hoverT) {
342	        const next = dukePick2(e, enraged);
343	        if (next === 1) dukeCharge(e, player, chargeSpd, 6, st);
344	        else if (next === 2) { // 旋转泡泡冲刺起手(:49782-49797):20 速直冲
345	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
346	          const d = Math.hypot(dx, dy) || 1;
347	          e.vx = (dx / d) * DUKE.spinDashSpd;
348	          e.vy = (dy / d) * DUKE.spinDashSpd;
349	          e.spin = Math.atan2(e.vy, e.vx);
350	          const s = Math.sign(dx) || st.dir;
351	          st.dir = s;
352	          if (st.spr === 1) e.spin += Math.PI;
353	          st.spr = -s;
354	          e.ai0 = 7; e.ai1 = 0; e.ai2 = 0;
355	        } else if (next === 3) { e.ai0 = 8; e.ai1 = 0; e.ai2 = 0; }
356	        else if (next === 4) { e.ai0 = 9; e.ai1 = 0; e.ai2 = 0; } // expert
357	      }
358	      break;
359	    }
360	    case 6: { // 二阶段冲撞(:49812-49834)
361	      game.spawnParticles(e.cx, e.cy, '#8FD8FF', 2, 1.5, { life: 18 });
362	      e.ai2 += 1;
363	      if (e.ai2 >= chargeT) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; e.ai3 += 2; }
364	      break;
365	    }
366	    case 7: { // 旋转泡泡冲刺(:49835-49864)
367	      if (e.ai2 === 0) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49839 PlaySound(29,…,20)(曾借 roar 0.6)
368	      if (e.ai2 % DUKE.spinEvery === 0) { // 每 4t 沿垂直方向甩一颗泡泡
369	        const vlen = Math.hypot(e.vx, e.vy) || 1;
370	        const bub = spawnPart(game, e, 371);
371	        if (bub) {
372	          bub.bInit = true; bub.ai0 = 0; bub.ai1 = 0;          // 预置初速,跳过自初始化
373	          bub.ai3 = (80 + Math.random() * 41) / 100;            // :49751 随机 scale
374	          bub.x = e.cx + (e.vx / vlen) * ((e.w + 20) / 2) - bub.w / 2;
375	          bub.y = e.cy + (e.vy / vlen) * ((e.w + 20) / 2) + 45 - bub.h / 2;
376	          const ang = Math.atan2(e.vy / vlen, e.vx / vlen) + (Math.PI / 2) * st.dir;
377	          bub.vx = Math.cos(ang) * DUKE.spinBubbleSpd;
378	          bub.vy = Math.sin(ang) * DUKE.spinBubbleSpd;
379	        }
380	      }
381	      // 速度/身体同步旋转(-num20*direction,:49854-49855)
382	      {
383	        const r = -DUKE_SPIN_RATE * st.dir;
384	        const cos = Math.cos(r), sin = Math.sin(r);
385	        const nvx = e.vx * cos - e.vy * sin, nvy = e.vx * sin + e.vy * cos;
386	        e.vx = nvx; e.vy = nvy;
387	        e.spin -= DUKE_SPIN_RATE * st.dir;
388	      }
389	      e.ai2 += 1;
390	      if (e.ai2 >= DUKE.spinT) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; }
391	      break;
392	    }
393	    case 8: dukeSharknado(e, game, player, st, true); break;           // :49865-49885
394	    case 9: { // expert 二段狂暴变身(:49886-49931;经典不可达,保留供 expert 接线)
395	      invuln = true;
396	      if (e.ai2 < DUKE.p2T - 90) e.spawnAlpha = clamp(e.spawnAlpha + (inSolid(game, e) ? 15 : -15), 0, 255);
397	      else e.spawnAlpha = Math.min(255, e.spawnAlpha + 4);
398	      e.vx *= 0.98;
399	      e.vy = lerp(e.vy, 0, 0.02);
400	      if (e.ai2 === DUKE.p2T - 60) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :49920 PlaySound(29,…,20)(曾借 roar 0.9)
401	      e.ai2 += 1;
402	      if (e.ai2 >= DUKE.p2T) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
403	      break;
404	    }
405	    case 10: { // expert 狂暴段悬浮(:49932-50018)
406	      if (player.dead) break;
407	      e.spawnAlpha = Math.min(255, e.spawnAlpha + 25); // 隐身逼近
408	      dukeHover(e, player, hoverAcc, hoverSpd, 360, st);
409	      e.ai2 += 1;
410	      if (e.ai2 >= hoverT) {
411	        const a3 = Math.floor(e.ai3);
412	        const next = (a3 === 0 || a3 === 2 || a3 === 3 || a3 === 5 || a3 === 6 || a3 === 7) ? 1 : 2;
413	        if (next === 1) dukeCharge(e, player, chargeSpd, 11, st);
414	        else { e.ai0 = 12; e.ai1 = 0; e.ai2 = 0; }
415	      }
416	      break;
417	    }
418	    case 11: { // expert 狂暴段冲撞(:50019-50047)
419	      e.spawnAlpha = Math.max(0, e.spawnAlpha - 25);
420	      game.spawnParticles(e.cx, e.cy, '#8FD8FF', 2, 1.5, { life: 18 });
421	      e.ai2 += 1;
422	      if (e.ai2 >= chargeT) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1; }
423	      break;
424	    }
425	    case 12: { // expert 瞬移爆冲(:50048-50107)
426	      invuln = true;
427	      e.spawnAlpha = Math.min(255, e.spawnAlpha + 17);
428	      e.vx *= 0.98;
429	      e.vy = lerp(e.vy, 0, 0.02);
430	      if (e.ai2 === DUKE.teleT / 2) { // :50066-50093 中点瞬移到玩家另一侧
431	        if (e.ai1 === 0) e.ai1 = 300 * Math.sign(e.cx - player.cx || 1);
432	        e.x = player.cx - e.ai1 - e.w / 2;
433	        e.y = player.cy - 200 - e.h / 2;
434	        const s = Math.sign(player.cx - e.cx) || st.dir;
435	        st.dir = s; st.spr = -s;
436	        game.spawnParticles(e.cx, e.cy, '#8FD8FF', 14, 2.4, { life: 30 });
437	        game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :50064 PlaySound(29,…,20)(曾借 roar 0.6)
438	      }
439	      e.ai2 += 1;
440	      if (e.ai2 >= DUKE.teleT) {
441	        e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1;
442	        if (e.ai3 >= 9) e.ai3 = 0;
443	      }
444	      break;
445	    }
446	    case 13: { // expert 狂暴段旋转冲刺(:50108-50125;不吐泡泡)
447	      if (e.ai2 === 0) game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);   // :50112 PlaySound(29,…,20)(曾借 roar 0.6)
448	      {
449	        const r = -DUKE_SPIN_RATE * st.dir;
450	        const cos = Math.cos(r), sin = Math.sin(r);
451	        const nvx = e.vx * cos - e.vy * sin, nvy = e.vx * sin + e.vy * cos;
452	        e.vx = nvx; e.vy = nvy;
453	        e.spin -= DUKE_SPIN_RATE * st.dir;
454	      }
455	      e.ai2 += 1;
456	      if (e.ai2 >= DUKE.spinT) { e.ai0 = 10; e.ai1 = 0; e.ai2 = 0; e.ai3 += 1; }
457	      break;
458	    }
459	    default: break;
460	  }
461	  if (invuln) e.iframes = 2;
462	  e.facing = st.spr;
463	  e.x += e.vx;
464	  e.y += e.vy;
465	}
466	
467	/** 鲨鱼龙卷(状态 3 :49638-49660 / 状态 8 :49865-49885 共用):
468	 *  减速悬停,ai2==60(nadoT-30)时发射龙卷水弹 proj 385(伤害 0 的落地生成器)——
469	 *  小龙卷两发斜落(±dir*2, 8)、克苏龙卷一发原地(0,0,ai0=1=追踪型,ai2=狂暴旗)。
470	 *  落地/近身 50px 后由弹体自身 Kill 生成 384/386 龙卷,龙卷逐段向上生长并周期
471	 *  NewNPC 372/373 鲨鱼(见 DukeSharknadoBolt / DukeSharknadoTornado)。 */
472	function dukeSharknado(e: Enemy, game: GameHooks, player: Player, st: DukeX, big: boolean) {
473	  e.vx *= 0.98;
474	  e.vy = lerp(e.vy, 0, 0.02);
475	  if (e.ai2 === DUKE.nadoT - 30) {
476	    if (big) {
477	      // :49871 大龙卷 = PlaySound(29,…,20) Zombie_20 满响(曾借 roar 0.7)
478	      game.playSfxWav?.('Zombie_20', 1, e.cx, e.cy);
479	      // 状态 8:克苏龙卷弹(:49873-49876;ai2=flag6 狂暴→追踪速度 +12)
480	      addProj(game, new DukeSharknadoBolt(e.cx, e.cy, 0, 0, true, dukeEnraged(game, player), e));
481	    } else {
482	      // :49644 小龙卷 = PlaySound(29,…,9) Zombie_9 满响
483	      game.playSfxWav?.('Zombie_9', 1, e.cx, e.cy);
484	      // 状态 3:左右两发斜落(:49646-49651;vector8 = rotation·(dir,0)·(w+20)/2 偏移)
485	      const ox = Math.cos(e.spin) * st.dir * (e.w + 20) / 2;
486	      addProj(game, new DukeSharknadoBolt(e.cx + ox, e.cy, st.dir * 2, 8, false, false, e));
487	      addProj(game, new DukeSharknadoBolt(e.cx + ox, e.cy, -st.dir * 2, 8, false, false, e));
488	    }
489	  }
490	  e.ai2 += 1;
491	  if (e.ai2 >= DUKE.nadoT) { e.ai0 = big ? 5 : 0; e.ai1 = 0; e.ai2 = 0; }
492	}
493	
494	/** 投射桶入桶辅助(同 bossAI.addProj;类在本文件内,避免跨模块构造注入) */
495	function addProj(game: GameHooks, p: Entity): void {
496	  (game as unknown as { entities: { add: (e: Entity, b: string) => void } }).entities.add(p, 'projectiles');
497	}
498	
499	// ---------------------------------------------------------------------------
500	// 龙卷水弹 385(Projectile.cs:28402-28482 AI / :70714-70778 Kill 落龙卷)
501	// ---------------------------------------------------------------------------
502	// aiStyle 65:ai1==0(状态 3 小弹)→ vy 余弦摆动斜落,撞块/入水/超时 Kill;
503	//  ai1>0(状态 8 克苏弹)→ 追踪玩家,速 4(+12 狂暴)+age/20,贴身 50px Kill。
504	//  Kill:小弹原地落 384 鲨鱼龙卷(伤 40);大弹自弹体 tile 向下扫描 100 格落 386
505	//  克苏龙卷(伤 80)——龙卷接触伤另按原版 hostile ×2 规则结算(Projectile.cs:13781)。
506	/** v6 联机弹体打包元数据（Boss 锚定弹体族共用形状，Game.netProjBroadcast 消费） */
507	export interface NetProjMeta {
508	  kind: number;        // msg27 kind（5-8）
509	  tag: string;         // 锚参数打包（各类自定义，≤32 字符）
510	  aux: number;         // i16 辅助通道
511	  dmg: number;         // 快照 dmg 字段
512	  /** 可选：以 vx/vy 通道携带的角度方向（重建端 atan2 还原） */
513	  exVx?: number;
514	  exVy?: number;
515	}
516	
517	export class DukeSharknadoBolt extends Entity {
518	  w = 30; h = 30; // SetDefaults 385
519	  private vx0: number;
520	  private vy0: number;
521	  private big: boolean;
522	  private enraged: boolean;
523	  /** 小弹 vy 摆动相位(原版 ai[0]) */
524	  private phase = 0;
525	  private age = 0;
526	  life = 300; // SetDefaults timeLeft
527	  /** 鲨鱼生成所需的 Duke 引用(spawnPart 位置供体,实际落点由龙卷覆写) */
528	  private src: Enemy;
529	  dead = false;
530	
531	  constructor(x: number, y: number, vx: number, vy: number, big: boolean, enraged: boolean, src: Enemy) {
532	    super();
533	    this.x = x - this.w / 2;
534	    this.y = y - this.h / 2;
535	    this.vx0 = vx; this.vy0 = vy;
536	    this.big = big; this.enraged = enraged;
537	    this.src = src;
538	  }
539	
540	  fixedUpdate(_dt: number, game: GameHooks): void {
541	    if (--this.life <= 0) { this.kill(game); return; }
542	    this.age++;
543	    const p = game.player;
544	    if (this.big) {
545	      // :28405-28447 追踪:速 4(+12 狂暴)+localAI[0]/20,距玩家 <50px 即 Kill
546	      if (p && !p.dead) {
547	        const dx = p.cx - this.cx, dy = p.cy - this.cy;
548	        const d = Math.hypot(dx, dy) || 1;
549	        const spd = 4 + (this.enraged ? 12 : 0) + this.age / 20;
550	        this.vx0 = (dx / d) * spd;
551	        this.vy0 = (dy / d) * spd;
552	        if (d < 50) { this.kill(game); return; }
553	      }
554	    } else {
555	      // :28448-28475 vy 余弦摆动:vy += (cos(π/15·θₙ₊₁) − cos(π/15·θₙ))·4
556	      const f = (t: number) => (Math.cos((Math.PI / 15) * t) - 0.5) * 4;
557	      const d0 = f(this.phase);
558	      this.phase += 1;
559	      this.vy0 += f(this.phase) - d0;
560	    }
561	    this.x += this.vx0;
562	    this.y += this.vy0;
563	    // :28477-28481 入水上浮 16px 后 Kill
564	    const st = game.world.store;
565	    const tx = Math.floor(this.cx / TILE), ty = Math.floor(this.cy / TILE);
566	    if (st.inBounds(tx, ty) && st.liquid[st.idx(tx, ty)] > 0) { this.y -= 16; this.kill(game); return; }
567	    if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { this.kill(game); return; }
568	  }
569	
570	  /** Kill(:70714-70778):尘环 + 落龙卷(小 384 / 大 386 向下扫描地面)。
571	   *  v6 联机傀儡:运动/消亡本地自算(确定性),但不落龙卷——房主的龙卷经 kind6 同步,
572	   *  双端各自生成会重复 */
573	  private kill(game: GameHooks): void {
574	    this.dead = true;
575	    game.spawnParticles(this.cx, this.cy, '#7FB8E8', 10, 2.4, { life: 24, damp: 0.94 });
576	    if (this.netPuppet) return;
577	    if (this.big) {
578	      // :70752-70770 自弹体 tile 向下扫 100 格,落点 = 首个实心/液体格上沿 -24px
579	      const st = game.world.store;
580	      let tx = clamp(Math.floor(this.cx / TILE), 10, st.w - 10);
581	      let ty = clamp(Math.floor(this.cy / TILE), 10, st.h - 110);
582	      let ground = ty + 15;
583	      for (let y = ty; y < ty + 100; y++) {
584	        if (st.inBounds(tx, y) && (st.isSolid(tx, y) || st.liquid[st.idx(tx, y)] !== 0)) { ground = y; break; }
585	      }
586	      addProj(game, new DukeSharknadoTornado(tx * TILE + 8, ground * TILE - 24, true, this.src));
587	    } else {
588	      // :70733-70737 原地落 384(中心反向偏移 direction*30, y-4)
589	      const dir = Math.sign(this.vx0) || 1;
590	      addProj(game, new DukeSharknadoTornado(this.cx - dir * 30, this.cy - 4, false, this.src));
591	    }
592	  }
593	
594	  /** v6 联机打包：kind=5，tag=big 标记（访客重建后本地跑确定性运动，见 kill 傀儡门禁）。
595	   *  终审 M1：速度经 exVx/exVy 通道携带（本类运动用私有 vx0/vy0，Entity.vx/vy 恒 0——
596	   *  不补则访客重建的小弹水平静止原地摆到寿终） */
597	  netProjMeta(): NetProjMeta {
598	    return { kind: 5, tag: this.big ? '1' : '0', aux: 0, dmg: 0, exVx: this.vx0, exVy: this.vy0 };
599	  }
600	
601	  draw(r: Renderer, _cam: Camera): void {
602	    const ctx = r.canvas.getContext('2d');
603	    if (!ctx) return;
604	    ctx.fillStyle = '#8FD8FF';
605	    ctx.beginPath();
606	    ctx.arc(this.cx, this.cy, 6, 0, TAU);
607	    ctx.fill();
608	  }
609	}
610	
611	// ---------------------------------------------------------------------------
612	// 鲨鱼龙卷 384 / 克苏龙卷 386(Projectile.cs:28287-28398,aiStyle 64)
613	// ---------------------------------------------------------------------------
614	// 原版是"父段 ai0 倒计时到 1 → 在正上方生成子段(ai0=10, ai1-1)直至 ai1=0"的投射物塔;
615	// 本实现以单实体模拟该塔:列顶随段生长上移,鲨鱼在"新段出现且 ai1 % 出鲨模 == 0"时
616	// 于列顶 NewNPC(小 384:模 4 → 3 只/塔;大 386:模 2 → 12 只/塔,ai2=幅宽 ai3=-1.5)。
617	// 接触伤害:小 40 / 大 80(经典 NewProjectile 值),命中按原版 hostile 弹 ×2 规则(:13781)。
618	export class DukeSharknadoTornado extends Entity {
619	  private big: boolean;
620	  private ai0: number;   // 段生长倒计时(父段 16,子段 10)
621	  private ai1: number;   // 剩余段数(小 15 / 大 24)
622	  private ai1Start: number;
623	  /** 列顶中心 y(鲨鱼生成点/绘制塔顶) */
624	  private topY: number;
625	  private segs = 0;      // 已生长段数
626	  private age = 0;
627	  private alpha = 255;   // 原版 alpha(实体内嵌 SolidCollision 逐渐显形)
628	  life: number;          // timeLeft 小 540 / 大 840
629	  private src: Enemy;
630	  dead = false;
631	
632	  constructor(x: number, y: number, big: boolean, src: Enemy) {
633	    super();
634	    this.big = big;
635	    this.ai0 = 16;                       // NewProjectile ai0
636	    this.ai1 = big ? 24 : 15;            // NewProjectile ai1
637	    this.ai1Start = this.ai1;
638	    this.topY = y;
639	    this.life = big ? 840 : 540;         // SetDefaults timeLeft
640	    this.src = src;
641	    this.x = x; this.y = y;
642	    this.resize();
643	  }
644	
645	  /** 段缩放(aiStyle 64 :28297-28316):小 (25-ai1)/25;大 (32-ai1)*1.5/32 */
646	  private scaleOf(ai1: number): number {
647	    return this.big ? (32 - ai1) * 1.5 / 32 : (25 - ai1) / 25;
648	  }
649	  private resize(): void {
650	    const s = this.scaleOf(this.ai1);
651	    this.w = Math.round(150 * s);        // SetDefaults 150×42 × scale
652	    this.h = Math.round(42 * s);
653	    this.x = this.cx - this.w / 2;
654	    this.y = this.topY - this.h / 2;
655	  }
656	
657	  fixedUpdate(_dt: number, game: GameHooks): void {
658	    if (--this.life <= 0) { this.dead = true; return; }
659	    this.age++;
660	    // alpha(:28336-28360):嵌实体块渐隐,否则向 60(大 100)显形
661	    const st = game.world.store;
662	    const inSolidTile = st.inBounds(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE)) && st.isSolid(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE));
663	    if (inSolidTile) this.alpha = Math.min(150, this.alpha + 30);
664	    else this.alpha = Math.max(this.big ? 100 : 60, this.alpha - 30);
665	
666	    if (this.ai0 > 0) this.ai0--;
667	    if (this.ai0 === 1 && this.ai1 > 0) {
668	      // :28363-28390 子段落点:列顶再上移 (42·sP + 42·sC)/2 − 2
669	      const sP = this.scaleOf(this.ai1), sC = this.scaleOf(this.ai1 - 1);
670	      this.topY -= (42 * sP) / 2 + (42 * sC) / 2 - 2;
671	      // 出鲨(:28372-28385):ai1 % 模 == 0 且 ai1≠0 → NewNPC 372/373 于列顶。
672	      // v6 傀儡不出鲨——房主的鲨鱼经 msg23 同步,双端各出会翻倍
673	      const mod = this.big ? 2 : 4;
674	      if (!this.netPuppet && this.ai1 % mod === 0 && this.ai1 !== 0) {
675	        const shark = spawnPart(game, this.src, this.big ? 373 : 372);
676	        if (shark) {
677	          shark.x = this.cx - shark.w / 2;
678	          shark.y = this.topY - shark.h / 2;
679	          shark.vx = this.vx; shark.vy = this.vy; // Main.npc.velocity = 弹体速度
680	          shark.bInit = false;                    // 由 sharkronAI 按 ai2/ai3 初始化
681	          shark.ai2 = this.big ? this.w : 0;      // 373 横游幅宽(:28382)
682	          shark.ai3 = this.big ? -1.5 : 0;        // 373 升速(:28383)
683	        }
684	      }
685	      this.ai1 -= 1;
686	      this.ai0 = 10;
687	      this.segs += 1;
688	      this.resize();
689	    }
690	    if (this.ai0 <= 0 && this.ai1 <= 0) {
691	      // :28392-28398 停止生长后横向摇摆(cos(π/30·−ai0) − 0.5)·幅宽
692	      const amp = (this.w / 5) * (this.big ? 2 : 1);
693	      const f = (t: number) => (Math.cos((Math.PI / 30) * t) - 0.5) * amp;
694	      this.x -= f(-this.ai0) * -1;
695	      this.ai0 -= 1;
696	      this.x += f(-this.ai0) * -1;
697	    }
698	
699	    // 接触伤害(hostile 弹 ×2 规则,Projectile.cs:13781:小 40→80 / 大 80→160)
700	    // 判定盒 = 整列(基座→列顶),宽取当前最宽段(= this.w,列顶段)
701	    const p = game.player;
702	    if (p && !p.dead) {
703	      const halfW = this.w / 2;
704	      const colTop = Math.min(this.topY, this.cy);
705	      const colH = Math.abs(this.cy - this.topY) + this.h;
706	      if (Math.abs(p.cx - this.cx) < halfW + p.w / 2 && Math.abs(p.cy - (colTop + colH / 2)) < colH / 2 + p.h / 2) {
707	        // 弹幕命中：attacker 仅做死亡归因，contactOnly 缺省 false → 荆棘不反伤
708	        // （反伤只在 NPC 接触分支 Player.cs:30910-30944）
709	        game.damagePlayer(this.big ? 160 : 80, this.cx, this.cy, this.src);
710	      }
711	    }
712	  }
713	
714	  /** v6 联机打包：kind=6，tag=`${big},${剩余段数ai1},${段倒计时ai0}`。
715	   *  近似收紧②：携带生长状态——中途入视野的龙卷按快照段盒+段数确定性恢复
716	   *  （topY = 快照y + 当前段半高,与房主同公式）,不再从零重长 */
717	  netProjMeta() {
718	    return { kind: 6, tag: `${this.big ? 1 : 0},${this.ai1},${this.ai0}`, aux: 0, dmg: 0 };
719	  }
720	
721	  /** v6 近似收紧②：访客重建时由快照段盒 + ai1/ai0 恢复生长态。
722	   *  topY 与 ai1 是确定性函数关系（resize: y = topY − h(ai1)/2），故由
723	   *  snapY 反解即可精确对齐房主当前态（含列顶位置,判定盒不再错位） */
724	  netStateSync(ai1: number, ai0: number, snapX: number, snapY: number): void {
725	    if (!Number.isFinite(ai1) || ai1 < 0 || ai1 > this.ai1Start) return; // 非法态保持新建
726	    this.ai1 = ai1;
727	    this.ai0 = Number.isFinite(ai0) ? ai0 : 10;
728	    this.segs = this.ai1Start - ai1;
729	    this.resize();
730	    this.x = snapX;                    // cx = snapX + w/2,resize 后 x = cx − w/2 = snapX
731	    this.topY = snapY + this.h / 2;    // 反解列顶（y = topY − h/2 的逆）
732	    this.y = snapY;
733	  }
734	
735	  draw(r: Renderer, _cam: Camera): void {
736	    const ctx = r.canvas.getContext('2d');
737	    if (!ctx) return;
738	    ctx.save();
739	    ctx.globalAlpha = 1 - this.alpha / 255;
740	    // 塔形:自基座向列顶逐段变宽(384 族贴图未解包,按段缩放画半透明白蓝柱)
741	    let segY = this.cy + this.h / 2;
742	    for (let i = this.segs; i >= 0; i--) {
743	      const s = this.scaleOf(Math.max(0, this.ai1Start - i));
744	      const sw = 150 * s, sh = 42 * s;
745	      segY -= sh;
746	      ctx.fillStyle = i % 2 ? '#9FD4F0' : '#7FB8E8';
747	      ctx.fillRect(this.cx - sw / 2, segY, sw, sh);
748	    }
749	    ctx.restore();
750	  }
751	}
752	
753	// ---------------------------------------------------------------------------
754	// 鲨鱼 NPC aiStyle 71(NPC 372 Sharkron / 373,NPC.cs:35196-35328)
755	// ---------------------------------------------------------------------------
756	// ai0=0:ai3 升速垂直蓄力 90t(dontTakeDamage;373 另带 ai2 幅宽余弦横游+渐显);
757	// 期满 ai0=1 → 16 速直扑玩家;ai0=1:渐显(−60/t)、撞实心块即死、60t 后恢复重力。
758	export function sharkronAI(e: Enemy, game: GameHooks, player: Player | null): void {
759	  if (!e.bInit) {
760	    e.bInit = true;
761	    e.ai0 = 0; e.ai1 = 0;
762	    e.spawnAlpha = 255; e.alphaFade = false; // 渐显由本 AI 按 :35228/:35267 驱动
763	  }
764	  if (!player || player.dead) { e.dead = true; return; } // TargetClosest 落空即消散
765	  const RISE_T = 90; // num1077
766	  if (e.ai0 === 0) {
767	    e.iframes = 2;              // dontTakeDamage(:35211)
768	    e.vx = 0;
769	    e.vy = e.ai3;               // velocity.Y = ai[3](:35212)
770	    if (e.vanillaId === 373) {
771	      e.spawnAlpha = Math.max(0, e.spawnAlpha - 6); // :35228 渐显
772	      // :35222-35227 贴图倾斜 rotation = vy·spriteDirection·0.1(钳 ±0.2)
773	      e.spin = clamp(e.vy * -e.facing * 0.1, -0.2, 0.2);
774	    }
775	    e.ai1 += 1;
776	    if (e.ai1 >= RISE_T) {
777	      // :35232-35252 蓄力期满:16 速扑咬(撞块内则 ai1=0 延后起扑)
778	      e.ai0 = 1;
779	      e.ai1 = inSolid(game, e) ? 0 : 1;
780	      const dx = player.cx - e.cx, dy = player.cy - e.cy;
781	      const d = Math.hypot(dx, dy) || 1;
782	      e.vx = (dx / d) * 16;
783	      e.vy = (dy / d) * 16;
784	      e.facing = dx < 0 ? -1 : 1;
785	      e.spin = Math.atan2(e.vy, e.vx) + (e.facing < 0 ? Math.PI : 0);
786	    }
787	  } else {
788	    // ai0 === 1(:35254-35310)
789	    if (e.ai1 < 1 && !inSolid(game, e)) e.ai1 = 1;
790	    if (inSolid(game, e)) e.spawnAlpha = Math.min(150, e.spawnAlpha + 15); // :35260
791	    if (e.ai1 >= 1) {
792	      e.spawnAlpha = Math.max(0, e.spawnAlpha - 60); // :35267 渐显
793	      e.ai1 += 1;
794	      if (inSolid(game, e)) { e.dead = true; return; } // :35282-35297 撞墙即死
795	    }
796	    if (e.ai1 >= 60) e.vy = Math.min(e.vy + 0.3, 16); // :35305-35309 恢复重力
797	    e.spin = Math.atan2(e.vy, e.vx) + (e.facing < 0 ? Math.PI : 0); // :35311-35315
798	  }
799	  // 373 蓄力段横游(:35213-35221):x += (cos(π/30·l1) − 0.5)·ai2·(−direction) 位移差
800	  if (e.ai0 === 0 && e.vanillaId === 373 && e.ai2 > 0) {
801	    const f = (t: number) => (Math.cos((Math.PI / 30) * t) - 0.5) * e.ai2;
802	    const prev = f(e.ai1 - 1), cur = f(e.ai1);
803	    e.x += (cur - prev) * -e.facing;
804	  }
805	  e.x += e.vx;
806	  e.y += e.vy;
807	}
808	
809	/** AI_070 爆裂泡泡(NPC 371,NPC.cs:35122-35195):
810	 *  朝玩家漂移(风偏+微上浮),玩家贴近(外扩 40px)或 150t 后爆炸(体积扩到 100×100,
811	 *  4t 后消散)。原版命中是 justHit→爆炸而非死亡;本工程近似为 hp 受损即转爆炸。
812	 *  简化:ai3 的随机 scale(:35134)无 Enemy 对应字段,仅记录不应用。 */
813	export function dukeBubbleAI(e: Enemy, game: GameHooks, player: Player | null) {
814	  void game;
815	  // :35180-35194 受击（justHit 单帧旗标）→ 无敌 + 爆炸体积；hp 损失本身不触发——
816	  // 真身是 StrikeNPC cs:82102-82107（371 伤害清零、ai0=1/ai1=4/dontTakeDamage），
817	  // 已由 Enemy.hurt() 同构处理，此处 justHit 为 AI 侧兜底
818	  if (e.ai0 !== 1 && e.justHit) { e.ai0 = 1; e.ai1 = 4; }
819	  // ai0/ai1 复位先于任何读点(原在 player 门内——无玩家时 ai0 留 -1120 会让
820	  // :844 `ai0===0` 落空直入爆炸分支 1 tick 即死;2026-08-13 ai0 清查)
821	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }
822	  if (e.bInit && player && e.ai3 <= 0) { // :35124-35131 初速 = 朝玩家 ±100px 随机偏移 × 11~17.7 速
823	    e.ai3 = (80 + Math.random() * 41) / 100;
824	    const jx = e.cx - player.cx + (Math.random() - 0.5) * 200;
825	    const jy = e.cy - player.cy + (Math.random() - 0.5) * 200;
826	    const d = Math.hypot(jx, jy) || 1;
827	    const spd = (165 + Math.random() * 100) / 15;
828	    e.vx = -(jx / d) * spd;
829	    e.vy = -(jy / d) * spd;
830	    e.alphaFade = false;
831	    e.spawnAlpha = 50; // :35136-35140
832	  }
833	  if (player) {
834	    // :35132-35133 主漂移:v = (v*40 + dir*20)/41
835	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
836	    const d = Math.hypot(dx, dy) || 1;
837	    e.vx = (e.vx * 40 + (dx / d) * 20) / 41;
838	    e.vy = (e.vy * 40 + (dy / d) * 20) / 41;
839	  }
840	  // :35141-35146 风扰+上浮(风取 0)
841	  e.vx = (e.vx * 50 + (Math.random() - 0.5) * 2) / 51;
842	  e.vy = (e.vy * 50 - 0.25 + (Math.random() - 0.5) * 4) / 51;
843	  if (e.vy > 0) e.vy -= 0.04;
844	  if (e.ai0 === 0 && player) { // :35147-35175 玩家贴近 → 爆炸
845	    const pad = 40 + e.w / 2;
846	    if (Math.abs(player.cx - e.cx) < pad + player.w / 2 && Math.abs(player.cy - e.cy) < pad + player.h / 2) {
847	      e.ai0 = 1; e.ai1 = 4;
848	    }
849	  }
850	  if (e.ai0 === 0) {
851	    e.ai1 += 1;
852	    if (e.ai1 >= 150) { e.ai0 = 1; e.ai1 = 4; } // :35167-35175 超时自爆
853	  } else {
854	    // 爆炸:体积扩到 100×100(:35187-35193)并 4t 后消散
855	    if (e.w !== 100) {
856	      e.x = e.cx - 50; e.y = e.cy - 50;
857	      e.w = 100; e.h = 100;
858	      game.spawnParticles(e.cx, e.cy, '#BFE8FF', 8, 2, { life: 20 });
859	    }
860	    e.iframes = 2; // dontTakeDamage
861	    e.ai1 -= 1;
862	    if (e.ai1 <= 0) { e.dead = true; return; }
863	  }
864	  e.x += e.vx;
865	  e.y += e.vy;
866	}
867	
868	// ---------------------------------------------------------------------------
869	// 月亮领主 aiStyle 77 核心(NPC 398,NPC.cs:36774-37198)
870	// ---------------------------------------------------------------------------
871	// ai0:-1 出生演出(60t,生成 2×397 手 + 1×396 头)→ 0 一阶段(双手+头存活期间无敌,随玩家悬停)
872	//   → 1 二阶段(三部件全部闭眼(ai0=-2)后解除无敌,自主追玩家+弹幕循环)
873	//   → 2 死亡演出(600t 后真死,全族消散)/ 3 玩家全灭离场(60t 后全族清除)。
874	//   -2:远距(>2400px)传送归位后的短演出。
875	
876	/** 二阶段弹幕表 = MoonLordAttacksArray2(:6966-6985,10 槽循环),驱动 NPC 400 真眼
877	 *  (aiStyle 81,:38243-38264,由部件 checkDead 召出,见 spawnTrueEye)。
878	 *  真眼数据/贴图缺失导致 spawn 失败时,攻击主链才折叠到核心上执行兜底。 */
879	const ML_CORE_P2: ReadonlyArray<readonly [number, number]> = [
880	  [0, 90], [1, 90], [0, 90], [2, 135], [0, 90], [3, 200], [0, 90], [4, 375], [0, 90], [2, 135],
881	];
882	
883	/** 朝玩家发射一发弹幕的通用出口(伤害/弹 id 全部来自原版 NewProjectile 调用点) */
884	function mlShoot(e: Enemy, game: GameHooks, player: Player, ox: number, oy: number,
885	  spd: number, dmg: number, projId: number) {
886	  const dx = player.cx - (e.cx + ox), dy = player.cy - (e.cy + oy);
887	  const d = Math.hypot(dx, dy) || 1;
888	  shoot(game, e.cx + ox, e.cy + oy, (dx / d) * spd, (dy / d) * spd, dmg, projId, 600);
889	}
890	
891	/** checkDead(:78845-78857):手 397 / 头 396 血尽 → ai0=-2 闭眼残肢的同时,于部件中心
892	 *  召 NPC 400 真眼,ai[3] = 部件的 ai[3](核心 id,游离眼 AI 据此锚定核心) */
893	function spawnTrueEye(game: GameHooks, part: Enemy): void {
894	  const eye = spawnPart(game, part, 400);
895	  if (!eye) return;
896	  eye.x = part.cx - eye.w / 2;
897	  eye.y = part.cy - eye.h / 2;
898	  eye.ai0 = 0; eye.ai1 = 0; eye.ai2 = 0; eye.ai3 = part.ai3;
899	}
900	
901	/** 月噬弹 456（Projectile.cs:5008 SetDefaults + aiStyle 85 :30678-30750）：
902	 *  16×16 / hostile / 0 伤 / noTileCollide / timeLeft 600。ai[0]>0 出击段：每 tick 朝
903	 *  玩家 min(16, 距离) 直飞，贴身 <20px 时 AddBuff(145 MoonLeech, 840t/专家 960t)
904	 *  （:30722-30732，本仓经典模式恒 840t = 14s）；age≥330 或玩家失联 → ai[0] 翻负
905	 *  回程段：朝 额前(0,+216) 直飞，<20px Kill（吸血视觉闭环）。
906	 *  弹体自旋角 = (源心 - 玩家心 + (0,216)).ToRotation() + π/2（:30717）。 */
907	export class MoonLeechProj extends Entity {
908	  w = 16; h = 16;
909	  vx = 0; vy = 0;
910	  private srcId: number;
911	  private out = true;      // ai[0] 符号：true = 出击 / false = 回程
912	  private age = 0;         // localAI[0]
913	  private fed = false;     // localAI[1]（已吸血，不重复授 buff）
914	  private life = 600;      // timeLeft
915	  dead = false;
916	
917	  constructor(src: Enemy, player: Player) {
918	    super();
919	    this.srcId = src.id;
920	    this.x = src.cx - this.w / 2;
921	    this.y = src.cy + 216 - this.h / 2;   // 额前 (0,+216)
922	    const dx = player.cx - this.cx, dy = player.cy - this.cy;
923	    const d = Math.hypot(dx, dy) || 1;
924	    this.vx = (dx / d) * 6; this.vy = (dy / d) * 6;   // :37823 出速 6（AI 段接管为 16 上限）
925	  }
926	
927	  fixedUpdate(_dt: number, game: GameHooks): void {
928	    const src = (game.enemies() as Enemy[]).find((n) => n.id === this.srcId);
929	    const player = game.player;
930	    if (--this.life <= 0 || !src || src.dead) { this.dead = true; return; }
931	    if (!player || player.dead) { if (this.out) this.out = false; }   // :30706-30712 玩家失联即回程
932	    this.age++;
933	    if (this.age >= 330 && this.out) this.out = false;                // :30702-30705
934	    // 出击：朝玩家心直飞（:30722-30725）；回程：朝源额前 (0,+216)（:30734-30738）
935	    const tx = this.out ? player.cx : src.cx;
936	    const ty = this.out ? player.cy : src.cy + 216;
937	    const dx = tx - this.cx, dy = ty - this.cy;
938	    const d = Math.hypot(dx, dy);
939	    const spd = Math.min(16, d);
940	    if (d > 0.001) { this.vx = (dx / d) * spd; this.vy = (dy / d) * spd; }
941	    this.x += this.vx; this.y += this.vy;
942	    // 贴身结算：出击段 <20px 授 MoonLeech 145（:30726-30732）；回程段 <20px Kill（:30740-30743）
943	    if (this.out && d < 20 && !this.fed) {
944	      this.fed = true;
945	      player.buffs.apply(BuffType.MoonLeech, 840 / 60);
946	    } else if (!this.out && d < 20) {
947	      this.dead = true;
948	    }
949	  }
950	
951	  draw(r: Renderer, _cam: Camera): void {
952	    const ctx = r.canvas.getContext('2d');
953	    if (!ctx) return;
954	    const img = projSprite(456);
955	    if (!img || !(img.width > 0) || img.width === 0) return;
956	    // 自旋（:30717）：(源心 - 玩家心 + (0,216)) 角 + π/2——回程矢量已同向，直接用速度角近似
957	    const ang = Math.atan2(this.vy, this.vx) + Math.PI / 2;
958	    ctx.save();
959	    ctx.translate(this.cx, this.cy);
960	    ctx.rotate(ang);
961	    ctx.imageSmoothingEnabled = false;
962	    // 多帧行切片（Main.projFrames[456]=4，Main.cs:8490；aiStyle 85 不推帧 → 恒帧 0，
963	    // 帧格 22×24）。曾整条 22×96 压进 16×16 判定盒 = 胶片条（G11）
964	    const frames = projFrameCount(456);
965	    const fh = img.height / frames;
966	    ctx.drawImage(img, 0, 0, img.width, fh, -img.width / 2, -fh / 2,
967	      img.width, fh);
968	    ctx.restore();
969	  }
970	}
971	
972	/** 月噬怪召出(:37828-37842 残肢 / :37975-37989 月噬攻击):头在 lt/inSlot=120/180/240
973	 *  于玩家处召 NPC 401,ai[0]=头 whoAmI+1 / ai[1]=源弹 456 索引。
974	 *  原版门禁 = 遍历全部 456 弹,其 ai[1] 指向的玩家 FindBuffIndex(145) != -1 才召
975	 *  （每弹一只）。本仓单玩家:debuff 145 已由 MoonLeechProj 贴身授予 → 玩家身中
976	 *  MoonLeech 即召,等价替换旧「弹已射出即命中」无条件近似
977	 *  (ai[1] 源弹索引以 -1 代,moonLeechAI 以出生点代弹着点,不受影响)。 */
978	function spawnMoonLeech(game: GameHooks, head: Enemy, player: Player): void {
979	  if (!player.buffs.moonLeech) return;
980	  const leech = spawnPart(game, head, 401);
981	  if (!leech) return;
982	  leech.x = player.cx - leech.w / 2;
983	  leech.y = player.cy - leech.h / 2;
984	  leech.ai0 = head.id + 1;
985	  leech.ai1 = -1;
986	  leech.ai2 = 0;
987	  leech.vx = 0; leech.vy = 0;
988	}
989	
990	// ---------------------------------------------------------------------------
991	// 死亡之光 455 PhantasmalDeathray(Projectile.cs:30291-30549,aiStyle 84)
992	// ---------------------------------------------------------------------------
993	// 定轴扫射激光:锚定源 NPC 眼部(头 396 椭圆 (27,59)·睁眼度 / 真眼 400 椭圆 (30,30)),
994	// 每 tick 转 ai0(=±2π/540),寿命 180t,scale = sin(age·π/180)·10·maxScale 脉冲张合;
995	// 束长 LaserScan(3 采样,最大 2400)以 0.5/t Lerp 逼近;命中判定 = 玩家矩形 vs
996	// 「源心 → 源心+dir·束长」线段,线宽 36·scale(Colliding :14673-14682);
997	// 伤害 = NewProjectile 值 ×2(hostile 弹规则 :13781:头 75→150 / 真眼 50→100)。
998	export class MLDeathray extends Entity {
999	  w = 36; h = 36; // SetDefaults 455
1000	  private srcId: number;
1001	  /** v6 联机：锚定 NPC 的 netId（访客端锚=msg23 傀儡；0=本端真身走 srcId 查找） */
1002	  srcNetId = 0;
1003	  /** 'head' = 396 头眼 / 'core' = 400 真眼(本仓折叠到核心 398) */
1004	  private kind: 'head' | 'core';
1005	  /** 扫射角速度(原版 ai[0] = ±2π/540) */
1006	  private sweep: number;
1007	  /** 当前束角(原版 velocity.ToRotation,每 tick +sweep) */
1008	  private angle: number;
1009	  private age = 0;
1010	  /** 束长 Lerp 值(原版 localAI[1]) */
1011	  private len = 0;
1012	  private dmg: number;
1013	  dead = false;
1014	
1015	  constructor(src: Enemy | null, kind: 'head' | 'core', angle: number, sweep: number, dmg: number, x?: number, y?: number) {
1016	    super();
1017	    this.srcId = src?.id ?? 0;
1018	    this.kind = kind;
1019	    this.angle = angle;
1020	    this.sweep = sweep;
1021	    this.dmg = dmg;
1022	    // v6 傀儡重建：src=null 时由调用方传显式坐标（真身路径 src 必非空）
1023	    this.x = (x ?? src!.cx) - this.w / 2;
1024	    this.y = (y ?? src!.cy) - this.h / 2;
1025	  }
1026	
1027	  /** v6 联机打包：kind=7，tag=`${srcId},${0|1 数值位（0=head 1=core）}`，aux=扫速×10000，
1028	   *  束角经 vx/vy 通道携带（重建端 atan2 还原后本地扫射——确定性自包含） */
1029	  netProjMeta(): NetProjMeta {
1030	    return {
1031	      kind: 7,
1032	      tag: `${this.srcId},${this.kind === 'head' ? 0 : 1}`,
1033	      aux: Math.max(-32768, Math.min(32767, Math.round(this.sweep * 10000))),
1034	      dmg: this.dmg,
1035	      exVx: Math.cos(this.angle) * 1000,
1036	      exVy: Math.sin(this.angle) * 1000,
1037	    };
1038	  }
1039	
1040	  /** scale 上限:头 1.0 / 真眼 0.4(:30468-30478 num728) */
1041	  private get maxScale(): number { return this.kind === 'head' ? 1 : 0.4; }
1042	
1043	  fixedUpdate(_dt: number, game: GameHooks): void {
1044	    // v6 近似收紧①：束角回写——快照把房主实时角度放在 vx/vy 通道（exVx/exVy），
1045	    // 傀儡消费式同步（读后清零防下一 tick 重复回拉振荡）；快照间隙内本地按扫速
1046	    // 自推插值。后台页暂停恢复后由下一快照纠偏（此前只按首帧角自推会永久漂移）
1047	    if (this.netPuppet && (this.vx !== 0 || this.vy !== 0)) {
1048	      this.angle = Math.atan2(this.vy, this.vx);
1049	      this.vx = 0; this.vy = 0;
1050	    }
1051	    // v6 联机：傀儡端按 netId 找锚（msg23 傀儡）；本端真身按本地 id
1052	    const src = this.srcNetId
1053	      ? (game.enemies() as Enemy[]).find((n) => n.netId === this.srcNetId)
1054	      : (game.enemies() as Enemy[]).find((n) => n.id === this.srcId);
1055	    if (!src || src.dead) { this.dead = true; return; }        // 源消亡即 Kill(:30297)
1056	    if (!this.netPuppet && this.kind === 'head' && src.ai0 === -2) { this.dead = true; return; } // :30296 头闭眼残肢（ai0 不同步,傀儡跳过——msg28 兜底）
1057	    this.age++;
1058	    if (this.age >= 180) { this.dead = true; return; }         // :30472 寿命 180t
1059	    this.angle += this.sweep;                                  // :30521 rotation += ai[0]
1060	
1061	    // 锚点:束原点 = 源心 + 眼球椭圆偏移(:30293-30308)
1062	    const hx = headOf(src);
1063	    const open = this.kind === 'head' ? hx.l1 : 1;
1064	    const eyeA = this.kind === 'head' ? hx.l0 : this.angle;    // 真眼无独立瞳角,随束角
1065	    const ex = this.kind === 'head' ? Math.cos(eyeA) * 27 * open : Math.cos(eyeA) * 30;
1066	    const ey = this.kind === 'head' ? Math.sin(eyeA) * 59 * open : Math.sin(eyeA) * 30;
1067	    this.x = src.cx + ex - this.w / 2;
1068	    this.y = src.cy + ey - this.h / 2;
1069	
1070	    // 束长:LaserScan 3 采样(线宽 36·scale,最大 2400)均值,:30483-30509
1071	    const scale = Math.min(this.maxScale, Math.sin((this.age * Math.PI) / 180) * 10 * this.maxScale);
1072	    const wSq = 36 * scale;
1073	    const dirX = Math.cos(this.angle), dirY = Math.sin(this.angle);
1074	    let amt = 0.5;
1075	    let dist = this.laserScan(game, dirX, dirY, wSq);
1076	    const p = game.player;
1077	    if (this.kind === 'head' && p && !p.dead && !losClear(game, this.cx, this.cy, p.cx, p.cy)) {
1078	      // :30511-30519 头与玩家无视线 → 束长取 距玩家+150(防隔墙盲射)
1079	      dist = Math.min(2400, Math.hypot(p.cx - src.cx, p.cy - src.cy) + 150);
1080	      amt = 0.75;
1081	    }
1082	    this.len = lerp(this.len, dist, amt);
1083	
1084	    // 命中:玩家矩形 vs 束线段(线宽 36·scale),伤害走 damagePlayer(iframes 节流)。
1085	    // 弹幕命中：attacker 仅做死亡归因，contactOnly 缺省 false → 荆棘不反伤
1086	    // （反伤只在 NPC 接触分支 Player.cs:30910-30944）
1087	    if (p && !p.dead && segHitsRect(this.cx, this.cy, dirX * this.len, dirY * this.len, wSq, p)) {
1088	      game.damagePlayer(this.dmg, this.cx, this.cy, src);
1089	    }
1090	  }
1091	
1092	  /** Collision.LaserScan 近似:垂直束向 ±半宽 3 条采样线,8px 步进至首实心块 */
1093	  private laserScan(game: GameHooks, dirX: number, dirY: number, width: number): number {
1094	    const px = -dirY, py = dirX; // 垂直束向
1095	    let sum = 0;
1096	    for (let k = -1; k <= 1; k++) {
1097	      const off = (k * width) / 2;
1098	      const ox = this.cx + px * off, oy = this.cy + py * off;
1099	      const steps = Math.ceil(2400 / 8);
1100	      let d = 2400;
1101	      for (let i = 1; i <= steps; i++) {
1102	        const t = i * 8;
1103	        const tx = Math.floor((ox + dirX * t) / TILE), ty = Math.floor((oy + dirY * t) / TILE);
1104	        const st = game.world.store;
1105	        if (!st.inBounds(tx, ty)) { d = t - 8; break; }
1106	        if (st.isSolid(tx, ty)) { d = t - 8; break; }
1107	      }
1108	      sum += d;
1109	    }
1110	    return sum / 3;
1111	  }
1112	
1113	  draw(r: Renderer, _cam: Camera): void {
1114	    const ctx = r.canvas.getContext('2d');
1115	    if (!ctx) return;
1116	    const scale = Math.min(this.maxScale, Math.sin((this.age * Math.PI) / 180) * 10 * this.maxScale);
1117	    if (scale <= 0.01 || this.len <= 1) return;
1118	    const thick = Math.max(2, 36 * scale);
1119	    ctx.save();
1120	    ctx.globalAlpha = clamp(scale * 1.6, 0.25, 1);
1121	    ctx.translate(this.cx, this.cy);
1122	    ctx.rotate(this.angle);
1123	    ctx.fillStyle = '#B040D0';
1124	    ctx.fillRect(0, -thick / 2, this.len, thick);
1125	    ctx.globalAlpha = clamp(scale * 0.9, 0.15, 0.6);
1126	    ctx.fillStyle = '#F0C8FF';
1127	    ctx.fillRect(0, -thick / 4, this.len, thick / 2);
1128	    ctx.restore();
1129	  }
1130	}
1131	
1132	/** 线段 vs AABB(原版 Collision.CheckAABBvLineCollision 语义:线宽胶囊与矩形相交) */
1133	function segHitsRect(x0: number, y0: number, dx: number, dy: number, width: number,
1134	  t: { x: number; y: number; w: number; h: number }): boolean {
1135	  // 最近点参数 t∈[0,1](钳到段内)
1136	  const cx = t.x + t.w / 2, cy = t.y + t.h / 2;
1137	  const len2 = dx * dx + dy * dy || 1;
1138	  let k = ((cx - x0) * dx + (cy - y0) * dy) / len2;
1139	  k = clamp(k, 0, 1);
1140	  const px = x0 + dx * k, py = y0 + dy * k;
1141	  // 最近点到矩形距离(逐轴钳位)
1142	  const nx = clamp(px, t.x, t.x + t.w), ny = clamp(py, t.y, t.y + t.h);
1143	  return Math.hypot(px - nx, py - ny) < width / 2;
1144	}
1145	
1146	/** 死亡之光发射出口(原版 :37902-37916 头 / :38625-38637 真眼):
1147	 *  起角 = 朝玩家角 ∓ 60°(num1278 = 玩家在左 +1),角速度 = num1278·2π/540。
1148	 *  返回源 NPC 的扫射编码角初值((起角+3π)·num1278,头部 ai2 逐 t 解码步进用)。 */
1149	function mlDeathray(game: GameHooks, src: Enemy, kind: 'head' | 'core', player: Player, dmg: number): number {
1150	  const dx = player.cx - src.cx, dy = player.cy - src.cy;
1151	  const d = Math.hypot(dx, dy) || 1;
1152	  const n = dx / d < 0 ? 1 : -1;                       // num1278
1153	  const ang = Math.atan2(dy, dx) - n * (TAU / 6);
1154	  addProj(game, new MLDeathray(src, kind, ang, n * (TAU / 540), dmg));
1155	  return (ang + Math.PI * 3) * n;
1156	}
1157	
1158	/** 核心悬停移动(:36854-36865 / :36912-36923 同构):目标 = 玩家 + (0,130),8 速/0.5 步进+半程混合 */
1159	function mlCoreHover(e: Enemy, player: Player) {
1160	  const dx = player.cx - e.cx;
1161	  const dy = player.cy + 130 - e.cy;
1162	  if (Math.hypot(dx, dy) > 20) {
1163	    const d = Math.hypot(dx - e.vx, dy - e.vy) || 1;
1164	    flyLerp(e, ((dx - e.vx) / d) * 8, ((dy - e.vy) / d) * 8, 0.5);
1165	  }
1166	}
1167	
1168	export function moonLordCoreAI(e: Enemy, game: GameHooks, player: Player | null) {
1169	  if (!e.bInit) { e.bInit = true; e.ai0 = -1; e.ai1 = 0; e.ai2 = 0; } // :36780-36785
1170	  // 原版 checkDead(:78859-78867):血尽 → ai0=2 死亡演出,满血续命 600t 后真死
1171	  if (e.hp <= 0 && e.ai0 !== 2) { e.ai0 = 2; e.ai1 = 0; e.hp = e.maxHp; e.iframes = 2; }
1172	
1173	  if (e.ai0 === -2) { // 远距传送归位(:36786-36809)
1174	    e.iframes = 2;
1175	    e.ai1 += 1;
1176	    if (e.ai1 >= 60) { e.ai1 = 0; e.ai0 = 0; }
1177	  } else if (e.ai0 === -1) { // 出生演出(:36810-36853)
1178	    e.iframes = 2;
1179	    e.ai1 += 1;
1180	    if (e.ai1 >= 60) {
1181	      e.ai1 = 0; e.ai0 = 0; e.ai2 = 0;
1182	      // 生成双手 397(核心两侧 ±400)与头 396(上方 400);ai3 = 核心 id(锚定)
1183	      for (let i = 0; i < 2; i++) {
1184	        const h = spawnPart(game, e, 397);
1185	        if (h) {
1186	          h.x = e.cx + i * 800 - 400 - h.w / 2;
1187	          h.y = e.cy - 100 - h.h / 2;
1188	          h.ai0 = 0; h.ai1 = 0; h.ai2 = i; h.ai3 = e.id; h.bInit = true;
1189	        }
1190	      }
1191	      const hd = spawnPart(game, e, 396);
1192	      if (hd) {
1193	        hd.x = e.cx - hd.w / 2;
1194	        hd.y = e.cy - 400 - hd.h / 2;
1195	        hd.ai0 = 0; hd.ai1 = 0; hd.ai2 = 0; hd.ai3 = e.id; hd.bInit = true;
1196	      }
1197	      game.playSfxWav?.('Zombie_92', 1, e.cx, e.cy);   // :36816 PlaySound(29,…,92)——case29 style92 ×0.5 自动档(曾借 roar 1.0)
1198	    }
1199	  } else if (e.ai0 === 0 || e.ai0 === 1) {
1200	    // 三部件(锚定本核心)
1201	    const parts = (game.enemies() as Enemy[]).filter(
1202	      (n) => !n.dead && (n.vanillaId === 396 || n.vanillaId === 397) && n.ai3 === e.id);
1203	    if (e.ai0 === 0) {
1204	      e.iframes = 2; // dontTakeDamage(:36856)
1205	      // 部件缺失 → 核心即毁(:36866-36890 flag84)
1206	      if (parts.length < 3) { e.dead = true; return; }
1207	      // 三部件全部闭眼残肢(ai0=-2)→ 解除无敌进二阶段(:36891-36909 flag85)
1208	      if (parts.every((p) => p.ai0 === -2)) { e.ai0 = 1; e.ai1 = 0; }
1209	    }
1210	    if (player) mlCoreHover(e, player);
1211	    if (e.ai0 === 1 && player) {
1212	      // 原版二阶段核心只悬停(:36912-36923),攻击全部由真眼 400(aiStyle 81)执行;
1213	      // 真眼已由部件 checkDead 召出 → 不再走折叠弹幕(否则双倍)。真眼 spawn 失败
1214	      // (数据缺失)时保留折叠兜底
1215	      const eyes = (game.enemies() as Enemy[]).some(
1216	        (n) => !n.dead && n.vanillaId === 400 && n.ai3 === e.id);
1217	      if (!eyes) {
1218	        e.ai1 += 1;
1219	        mlCoreBarrage(e, game, player); // 二阶段弹幕(真眼主链折叠兜底)
1220	      }
1221	    }
1222	  } else if (e.ai0 === 2) { // 死亡演出(:36925-37064)
1223	    e.iframes = 2;
1224	    e.vx = lerp(e.vx, 0, 0.02);
1225	    e.vy = lerp(e.vy, -0.5, 0.02);
1226	    e.ai1 += 1;
1227	    // :36954-37022 每 3t 一簇爆炎(60t<ai1<580);:37049 起声效/光效略
1228	    if (e.ai1 % 3 === 0 && e.ai1 > 60 && e.ai1 < 580) {
1229	      game.spawnParticles(
1230	        e.cx + (Math.random() - 0.5) * 400, e.cy + (Math.random() - 0.5) * 400,
1231	        '#C04030', 6, 3, { life: 30 });
1232	    }
1233	    if (e.ai1 >= 600) { // :37053-37063 真死 → 全族由各部件 AI 检测 core.dead 自毁
1234	      e.dead = true;
1235	      return;
1236	    }
1237	  } else if (e.ai0 === 3) { // 玩家全灭离场(:37065-37135)
1238	    e.iframes = 2;
1239	    e.vx = lerp(e.vx, e.facing, 0.02);
1240	    e.vy = lerp(e.vy, -0.5, 0.02);
1241	    e.ai1 += 1;
1242	    if (e.ai1 >= 60) { // :37109-37127 清除全部部件与自身
1243	      for (const n of game.enemies() as Enemy[]) {
1244	        if (!n.dead && (n.vanillaId === 396 || n.vanillaId === 397 || n.vanillaId === 400) && n.ai3 === e.id) n.dead = true;
1245	      }
1246	      e.dead = true;
1247	      return;
1248	    }
1249	  }
1250	
1251	  // 玩家全灭 → 离场(:37136-37161)
1252	  if (!player && e.ai0 !== -1 && e.ai0 !== -2 && e.ai0 !== 2 && e.ai0 !== 3) { e.ai0 = 3; e.ai1 = 0; }
1253	  // 玩家远距 >2400px → 全族瞬移归位(:37162-37197)
1254	  if (player && e.ai0 >= 0 && e.ai0 < 2 && Math.hypot(player.cx - e.cx, player.cy - e.cy) > 2400) {
1255	    const dx = player.cx - e.cx;
1256	    const dy = player.cy - 150 - e.cy;
1257	    e.x += dx; e.y += dy;
1258	    for (const n of game.enemies() as Enemy[]) {
1259	      if (!n.dead && (n.vanillaId === 396 || n.vanillaId === 397 || n.vanillaId === 400) && n.ai3 === e.id) {
1260	        n.x += dx; n.y += dy;
1261	      }
1262	    }
1263	    e.ai0 = -2; e.ai1 = 0;
1264	  }
1265	  e.x += e.vx;
1266	  e.y += e.vy;
1267	}
1268	
1269	/** 核心二阶段弹幕(原版 NPC 400 真眼攻击链,aiStyle 81 :38347-38600;
1270	 *  投射物/伤害取原版调用点:462 PhantasmalBolt 35(:38382)、454 PhantasmalSphere 40(:38455)、
1271	 *  455 PhantasmalDeathray 75(:37913)、452 PhantasmalEye 30(:37333)) */
1272	function mlCoreBarrage(e: Enemy, game: GameHooks, player: Player) {
1273	  const { atk, inSlot, dur } = attackSlot(e, ML_CORE_P2);
1274	  switch (atk) {
1275	    case 1: // 幻影之眼 452×4 扇形(:37326-37334)
1276	      if (inSlot === 0) {
1277	        for (let k = -1.5; k <= 1.5; k++) {
1278	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
1279	          const d = Math.hypot(dx, dy) || 1;
1280	          const ang = Math.atan2(dy, dx) + k * 0.35;
1281	          shoot(game, e.cx, e.cy, Math.cos(ang) * 8, Math.sin(ang) * 8, 30, 452, 600);
1282	        }
1283	      }
1284	      break;
1285	    case 2: // 幻影能量球 454:先慢速散出,后段朝玩家加速(原版 30t 后转向寻的,:38447-38456/:38475)
1286	      if (inSlot === 0) {
1287	        for (let k = 0; k < 3; k++) {
1288	          const ang = -Math.PI / 2 + (k - 1) * 0.6;
1289	          shoot(game, e.cx, e.cy, Math.cos(ang) * 4, Math.sin(ang) * 4, 40, 454, 600);
1290	        }
1291	      } else if (inSlot === 60) {
1292	        for (let k = -1; k <= 1; k++) mlShoot(e, game, player, 0, 0, 12, 40, 454);
1293	      }
1294	      break;
1295	    case 3: // 三连幻影矢 462(:38378-38383,slot 末 14/7/0 三发)
1296	      if (inSlot === dur - 14 || inSlot === dur - 7 || inSlot === dur) {
1297	        mlShoot(e, game, player, 0, 0, 8, 35, 462);
1298	      }
1299	      break;
1300	    case 4: // 死亡之光 455(:38625-38647):inSlot==180 一发定轴扫射激光(50 伤→命中×2=100)
1301	      // 原版此槽 375t:0-179 蓄能尘,180 发束,束体自转 180t 至槽末;真眼瞳角动画随束同步
1302	      // (localAI[0],:38642-38652)——真眼不在本仓范围,锚点用核心中心 (30,30) 椭圆近似
1303	      if (inSlot === 180) { e.ai2 = mlDeathray(game, e, 'core', player, 50 * 2); }
1304	      break;
1305	    default: break; // 0 = 闭眼冷却 90t
1306	  }
1307	}
1308	
1309	// ---------------------------------------------------------------------------
1310	// 月亮领主 aiStyle 78 手(NPC 397,NPC.cs:37199-37711)
1311	// ---------------------------------------------------------------------------
1312	// 攻击时间表 MoonLordAttacksArray[0, ai2](:6854-6883):
1313	//   ai2=0(左手,side=-1):[闭50, 眼70, 球330, 闭60, 矢90]
1314	//   ai2=1(右手,side=+1):[眼70, 闭50, 矢90, 闭60, 球330]
1315	// 攻击:0 闭眼悬停(无敌)/ 1 眼球环射 452(30 伤)/ 2 能量球扫射 454(40 伤,末段全数转向玩家)
1316	//   / 3 三连幻影矢 462(30 伤,预判 20t)。
1317	// 无敌语义:dontTakeDamage = frame>=21(:37215)——只有攻击中(睁眼)可受击。
1318	
1319	const ML_HAND_ATTACKS: Readonly<Record<number, ReadonlyArray<readonly [number, number]>>> = {
1320	  0: [[0, 50], [1, 70], [2, 330], [0, 60], [3, 90]],
1321	  1: [[1, 70], [0, 50], [3, 90], [0, 60], [2, 330]],
1322	};
1323	
1324	export function moonLordHandAI(e: Enemy, game: GameHooks, player: Player | null) {
1325	  // 锚定核心;核心缺失/死亡 → 自毁(:37202-37207)
1326	  const core = (game.enemies() as Enemy[]).find((n) => n.id === e.ai3 && n.vanillaId === 398);
1327	  if (!core || core.dead) { e.dead = true; return; }
1328	  // 原版 checkDead(:78845-78857):血尽 → ai0=-2 闭眼残肢(满血续命+无敌)+召真眼 400
1329	  if (e.hp <= 0 && e.ai0 !== -2) {
1330	    e.ai0 = -2; e.ai1 = 0; e.hp = e.maxHp; e.iframes = 2;
1331	    spawnTrueEye(game, e);
1332	  }
1333	
1334	  const x = handOf(e);
1335	  const side = e.ai2 === 0 ? -1 : 1;  // num1231 :37208-37210
1336	  e.facing = side;                    // spriteDirection
1337	
1338	  // 攻击表推进(:37221-37251;ai0=-2 残肢态不参与调度)
1339	  let inSlot = 0, dur = 0;
1340	  if (e.ai0 !== -2) {
1341	    e.ai1 += 1;
1342	    const s = attackSlot(e, ML_HAND_ATTACKS[e.ai2 === 0 ? 0 : 1]);
1343	    e.ai0 = s.atk; // :37245 原版 ai[0] 即攻击号(亦为手部状态)
1344	    inSlot = s.inSlot; dur = s.dur;
1345	  }
1346	  let frameT = 0; // num1234(帧目标=frameT*7)
1347	
1348	  if (e.ai0 === -2) { // 闭眼残肢(:37252-37280)
1349	    frameT = 0;
1350	    e.def.damage = 80; // :37254
1351	    if (e.ai1 >= 32) e.ai1 = 0;
1352	    handHover(e, core, side);
1353	  } else if (e.ai0 === 0) { // 闭眼悬停(:37281-37303)
1354	    frameT = 3;
1355	    x.l1 = Math.max(0, x.l1 - 0.05);
1356	    handHover(e, core, side);
1357	  } else if (e.ai0 === 1 && player) { // 眼球环射(:37304-37346)
1358	    frameT = 0;
1359	    const cyc = 28; // num1240*num1241 = 7*4
1360	    if (inSlot >= cyc * 2) {
1361	      x.l1 = Math.max(0, x.l1 - 0.07);
1362	    } else if (inSlot >= cyc) {
1363	      x.l1 = Math.min(0.75, x.l1 + 0.05);
1364	      const ang = (TAU * (inSlot % cyc)) / cyc - Math.PI / 2; // :37324
1365	      x.l0 = Math.atan2(Math.sin(ang) * 66, Math.cos(ang) * 30);
1366	      if (inSlot % 4 === 0) handFireEye(e, game, x, side); // :37326-37334 452(30 伤)
1367	    } else {
1368	      x.l1 = Math.min(0.75, x.l1 + 0.02);
1369	      const ang = (TAU * (inSlot % cyc)) / cyc - Math.PI / 2;
1370	      x.l0 = Math.atan2(Math.sin(ang) * 66, Math.cos(ang) * 30);
1371	    }
1372	  } else if (e.ai0 === 2) { // 能量球扫射(:37347-37447)
1373	    const ax = core.cx + 220 * side + side * 100;   // vector168
1374	    const ay = core.cy - 60 - 50;
1375	    const swx = 400 * side, swy = -60;              // vector169
1376	    if (inSlot < 30) {
1377	      handApproach(e, ax, ay, 8, 0.2);
1378	    } else if (inSlot < 210) {
1379	      frameT = 1;
1380	      if ((inSlot - 30) % 30 === 0 && player) { // :37372-37380 每 30t 一发 454(40 伤)
1381	        const k = Math.floor((inSlot - 30) / 30);
1382	        let vx = 5 * side + (k - 3.5) * side * 3;
1383	        let vy = -8 + (k - 4.5);
1384	        vx *= 1.2; vy *= 1.2;
1385	        shoot(game, e.cx, e.cy, vx, vy, 40, 454, 600);
1386	      }
1387	      const t = smoothAmt((inSlot - 30) / 180);
1388	      handSeek(e, ax + swx * t, ay + swy * t, 20, 0.5); // :37381-37387
1389	    } else if (inSlot < 282) {
1390	      frameT = 0;
1391	      e.vx *= 0.9; e.vy *= 0.9;
1392	    } else if (inSlot < 287) {
1393	      frameT = 1;
1394	      e.vx *= 0.9; e.vy *= 0.9;
1395	    } else if (inSlot < 292) {
1396	      frameT = 2;
1397	      e.vx *= 0.9; e.vy *= 0.9;
1398	    } else if (inSlot < 300) {
1399	      frameT = 3;
1400	      // :37407-37427 原版在此把本手全部 454 弹转向玩家(12 速);本工程投射物无寻的,
1401	      // 近似为朝玩家补射 6 发 454(40 伤)
1402	      if (inSlot === 292 && player) {
1403	        for (let k = 0; k < 6; k++) {
1404	          const dx = player.cx - e.cx, dy = player.cy - e.cy;
1405	          const d = Math.hypot(dx, dy) || 1;
1406	          const ang = Math.atan2(dy, dx) + (k - 2.5) * 0.18;
1407	          shoot(game, e.cx, e.cy, Math.cos(ang) * 12, Math.sin(ang) * 12, 40, 454, 600);
1408	        }
1409	      }
1410	      const t = 1 - (inSlot - 270) / 30;
1411	      handSeek(e, ax + swx * smoothAmt(t), ay + swy * smoothAmt(t), 14, 0.1); // :37428-37434
1412	    } else {
1413	      frameT = 3;
1414	      handApproach(e, ax, ay, 8, 0.2); // :37436-37446 归位
1415	    }
1416	  } else if (e.ai0 === 3 && player) { // 三连幻影矢(:37448-37472)
1417	    frameT = 0;
1418	    const pvx = (player as unknown as { vx: number }).vx ?? 0;
1419	    const pvy = (player as unknown as { vy: number }).vy ?? 0;
1420	    const dx = player.cx + pvx * 20 - e.cx, dy = player.cy + pvy * 20 - e.cy; // :37455 预判 20t
1421	    x.l0 = angleLerp(x.l0, Math.atan2(dy, dx), 0.5);
1422	    x.l1 = Math.min(1, x.l1 + 0.05);
1423	    if (inSlot === dur - 35) game.playSfxWav?.('NPC_Hit_6', 1, e.cx, e.cy);   // :37464 PlaySound(4,…,6)=NPCHit style6(曾借 roar 0.5)
1424	    if (inSlot === dur - 14 || inSlot === dur - 7 || inSlot === dur) {
1425	      // :37466-37471 从眼球位置射 462(30 伤,8 速)
1426	      const exx = Math.cos(x.l0) * 30 * x.l1, eyy = Math.sin(x.l0) * 66 * x.l1;
1427	      const d = Math.hypot(dx, dy) || 1;
1428	      shoot(game, e.cx + exx, e.cy + eyy, (dx / d) * 8, (dy / d) * 8, 30, 462, 600);
1429	    }
1430	  }
1431	
1432	  // 睁闭眼帧推进(:37493-37509):每 tick 向目标帧走 1,dontTakeDamage = frame>=21
1433	  const frameTarget = frameT * 7;
1434	  if (frameTarget > x.frame) x.frame += 1;
1435	  else if (frameTarget < x.frame) x.frame -= 1;
1436	  x.frame = clamp(x.frame, 0, 21);
1437	
1438	  // 位置钳制(:37473-37492):下一位置锁在核心侧上方盒内
1439	  let minX = core.cx + 220 * side + 110 * side, minY = core.cy - 60 - 150;
1440	  let maxX = minX + 370 * side, maxY = minY + 150;
1441	  if (minX > maxX) { const t = minX; minX = maxX; maxX = t; }
1442	  if (minY > maxY) { const t = minY; minY = maxY; maxY = t; }
1443	  const nx = clamp(e.cx + e.vx, minX, maxX);
1444	  const ny = clamp(e.cy + e.vy, minY, maxY);
1445	  e.x = nx - e.w / 2;
1446	  e.y = ny - e.h / 2;
1447	
1448	  // 无敌:闭眼(frame>=21)或残肢态;可受击时不写 iframes,保留 hurt() 的 8t 受击免疫
1449	  if (x.frame >= 21 || e.ai0 === -2) e.iframes = 2;
1450	  e.spin = x.l0; // 手部眼球角度(渲染朝向)
1451	}
1452	
1453	/** 手部悬停(:37266-37279 / :37289-37302):核心侧上方 (350*side, -100),6 速/0.3 步进+半程混合 */
1454	function handHover(e: Enemy, core: Enemy, side: number) {
1455	  const dx = core.cx + 350 * side - e.cx;
1456	  const dy = core.cy - 100 - e.cy;
1457	  const d = Math.hypot(dx, dy);
1458	  if (d > 20) flyLerp(e, (dx / d) * 6, (dy / d) * 6, 0.3);
1459	}
1460	/** SmoothStep 趋近(:37358-37367 / :37438-37445):velocity = SmoothStep(v, normalize(delta)*min(spd,|delta|), k) */
1461	function handApproach(e: Enemy, tx: number, ty: number, spd: number, k: number) {
1462	  const dx = tx - e.cx, dy = ty - e.cy;
1463	  const d = Math.hypot(dx, dy);
1464	  if (d < 0.01) return;
1465	  const m = Math.min(spd, d);
1466	  e.vx = vSmoothStep(e.vx, (dx / d) * m, k);
1467	  e.vy = vSmoothStep(e.vy, (dy / d) * m, k);
1468	}
1469	/** 扫射段追随(:37381-37387 / :37428-37434):Lerp(v, normalize(delta)*min(spd,|delta|), k) */
1470	function handSeek(e: Enemy, tx: number, ty: number, spd: number, k: number) {
1471	  const dx = tx - e.cx, dy = ty - e.cy;
1472	  const d = Math.hypot(dx, dy);
1473	  if (d < 0.01) return;
1474	  e.vx = lerp(e.vx, (dx / d) * Math.min(spd, d), k);
1475	  e.vy = lerp(e.vy, (dy / d) * Math.min(spd, d), k);
1476	}
1477	/** 眼球环射一发 452(:37326-37334):从眼球椭圆外沿射出,沿眼球朝向 8 速,30 伤 */
1478	function handFireEye(e: Enemy, game: GameHooks, x: HandX, side: number) {
1479	  const exx = Math.cos(x.l0) * 30 * x.l1, eyy = Math.sin(x.l0) * 66 * x.l1;
1480	  const d = Math.hypot(exx, eyy) || 1;
1481	  const px = e.cx + (exx / d) * 72.46 * 0.4 - side; // |vector159|=√(30²+66²)≈72.46(:37330)
1482	  const py = e.cy + (eyy / d) * 72.46 * 0.4 + 3;
1483	  shoot(game, px, py, (exx / d) * 8, (eyy / d) * 8, 30, 452, 600);
1484	}
1485	
1486	// ---------------------------------------------------------------------------
1487	// 月亮领主 aiStyle 79 头(NPC 396,NPC.cs:37712-38128)
1488	// ---------------------------------------------------------------------------
1489	// 恒定悬停在核心正上方 400px(无自主移动);攻击表 MoonLordAttacksArray[0,2](:6874-6883):
1490	//   [矢180, 闭30, 吸血435, 矢180, 光375]。
1491	// 攻击:0 睁眼瞄准(无敌)/ 1 死亡之光 455(75 伤,:37902-37916)/ 2 月噬 456(0 伤,:37957-37973)
1492	//   / 3 三连幻影矢 462(30 伤,:37991-38015)。-2 闭眼残肢(80 接触伤)/ -3 核心死亡后永闭。
1493	// 无敌语义:dontTakeDamage = localAI[3]>=15(:37724)。
1494	
1495	const ML_HEAD_ATTACKS: ReadonlyArray<readonly [number, number]> = [
1496	  [3, 180], [0, 30], [2, 435], [3, 180], [1, 375],
1497	];
1498	
1499	export function moonLordHeadAI(e: Enemy, game: GameHooks, player: Player | null) {
1500	  // 类默认 ai0=-1120 会令 `ai0>=0` 攻击表门恒假 = 头部冻结(2026-08-13 ai0 清查;
1501	  // 现网靠父核 :1184 预置 0 挡住,此为入口防御)。放行运行态 -2/-3(闭眼残肢)
1502	  if (e.ai0 < -3) e.ai0 = 0;
1503	  const core = (game.enemies() as Enemy[]).find((n) => n.id === e.ai3 && n.vanillaId === 398);
1504	  if (!core || core.dead) { e.dead = true; return; } // :37714-37719
1505	  // checkDead(:78845-78857)同手:血尽 → ai0=-2 闭眼残肢 + 召真眼 400
1506	  if (e.hp <= 0 && e.ai0 !== -2 && e.ai0 !== -3) {
1507	    e.ai0 = -2; e.ai1 = 0; e.ai2 = 0; e.hp = e.maxHp; e.iframes = 2;
1508	    spawnTrueEye(game, e);
1509	  }
1510	
1511	  const x = headOf(e);
1512	  e.vx = 0; e.vy = 0; // :37725
1513	  e.x = core.cx - e.w / 2; // :37726 恒定在核心上方 400px
1514	  e.y = core.cy - 400 - e.h / 2;
1515	
1516	  // 攻击表推进(:37732-37762;ai0<0 不参与)
1517	  let inSlot = 0, dur = 0;
1518	  if (e.ai0 >= 0) {
1519	    e.ai1 += 1;
1520	    const s = attackSlot(e, ML_HEAD_ATTACKS);
1521	    e.ai0 = s.atk; // :37756 原版 ai[0] 即攻击号(亦为头部状态)
1522	    inSlot = s.inSlot; dur = s.dur;
1523	  }
1524	  let f2T = 0, f3T = 0; // num1262/num1263(帧目标 = f2T*7 / f3T*5)
1525	
1526	  if (e.ai0 === -3) { // 核心死亡后永闭(:37763-37781;由 -2 分支转入 :37784-37788)
1527	    e.def.damage = 0;
1528	    e.spin = lerp(e.spin, Math.PI / 12, 0.07);
1529	    if (e.ai1 >= 32) e.ai1 = 0;
1530	    if (x.f2 < 14) x.f2 += 1;
1531	    e.iframes = 2;
1532	    return;
1533	  }
1534	  if (e.ai0 === -2) { // 闭眼残肢(:37782-37844)
1535	    if (core.ai0 === 2) { e.ai0 = -3; return; } // :37784-37788
1536	    e.def.damage = 80;
1537	    e.iframes = 2;
1538	    if (e.ai1 >= 32) e.ai1 = 0;
1539	    e.ai2 += 1;
1540	    if (e.ai2 >= 555) e.ai2 = 0;
1541	    if (e.ai2 >= 120 && player) { // :37805-37843 残肢期月噬循环
1542	      const lt = e.ai2 - 120;
1543	      if (lt === 0) { // :37811-37827 从额前 216px 发月噬 456(0 伤,纯吸血视觉→MoonLeechProj)
1544	        addProj(game, new MoonLeechProj(e, player));
1545	      }
1546	      // :37828-37842 lt=120/180/240 于玩家处召 401 月噬怪(门禁说明见 spawnMoonLeech)
1547	      if ((lt === 120 || lt === 180 || lt === 240)) spawnMoonLeech(game, e, player);
1548	    }
1549	    return;
1550	  }
1551	
1552	  if (e.ai0 === 0 && player) { // 睁眼瞄准(:37845-37864)
1553	    f3T = 3;
1554	    const dx = player.cx - e.cx, dy = player.cy + 22 - e.cy;
1555	    const d = Math.hypot(dx, dy) || 1;
1556	    x.l0 = Math.atan2(dy, dx);
1557	    x.l1 = Math.min(1, Math.max(0, (1 - Math.min(1, d / 500)) * 2)); // :37850-37860
1558	    x.l2 = lerp(x.l2, 1, 0.2);
1559	  } else if (e.ai0 === 1 && player) { // 死亡之光(:37865-37952)
1560	    if (inSlot < 180) {
1561	      x.l1 = Math.max(0, x.l1 - 0.05);
1562	      if (inSlot >= 60) { // :37876-37898 聚能尘
1563	        game.spawnParticles(
1564	          e.cx + (Math.random() - 0.5) * 27, e.cy + (Math.random() - 0.5) * 59, '#B040C0', 2, 1.2, { life: 24 });
1565	      }
1566	    } else if (inSlot < dur - 15) {
1567	      // :37902-37916 发射 455 死亡之光(75 伤→命中×2=150):起角 ∓60° 预偏,
1568	      // 束体以 ±2π/540 每 t 扫射 180t(束体自转见 MLDeathray)
1569	      if (inSlot === 180) {
1570	        e.ai2 = mlDeathray(game, e, 'head', player, 75 * 2); // :37913 扫射编码角初值
1571	        // 原版 NPC 侧死光发射零吼(:37700-37970 无 PlaySound)——曾借 roar 0.8,2026-08-18 对账删
1572	      }
1573	      // :37917-37947 头部瞳角与束体同角速度扫射(ai2 存编码角,逐 t 解码步进)
1574	      if (inSlot >= 180) {
1575	        const n = e.ai2 >= 0 ? 1 : -1; // num1279
1576	        const a = Math.abs(e.ai2) - Math.PI * 3 + n * (TAU / 540);
1577	        x.l0 = a;
1578	        e.ai2 = (a + Math.PI * 3) * n;
1579	      }
1580	      x.l1 = Math.min(1, x.l1 + 0.05);
1581	    } else {
1582	      f3T = 3;
1583	      // :37927-37950 收束段:l1 −0.07/t;跌破 0 的 tick 在 FTW 下于头部中心连射
1584	      // 30 发 1021 弹(伤 70;±15.99 / [−15.99,0) 随机速;逐发门 = 中心格非实心)。
1585	      // 原文先钳 0 再掷,状态尾段仅 ~15t 且 l1 自 1 收束,实际近似每轮死亡之光一发;
1586	      // 逐句照抄(钳后若状态仍延续会连发——原版语义)
1587	      x.l1 -= 0.07;
1588	      if (x.l1 < 0) {
1589	        x.l1 = 0;
1590	        if (game.world.seedFlags?.getGoodWorld) {
1591	          const st = game.world.store;
1592	          const tx = Math.floor(e.cx / TILE), ty = Math.floor(e.cy / TILE);
1593	          if (st.inBounds(tx, ty) && !st.isSolid(tx, ty)) {
1594	            for (let num1281 = 0; num1281 < 30; num1281++) {
1595	              shoot(game, e.cx, e.cy,
1596	                (Math.floor(Math.random() * 3199) - 1599) * 0.01,
1597	                (Math.floor(Math.random() * 1600) - 1599) * 0.01, 70, 1021);
1598	            }
1599	          }
1600	        }
1601	      }
1602	    }
1603	  } else if (e.ai0 === 2) { // 月噬(:37953-37990)
1604	    f2T = 2;
1605	    f3T = 3;
1606	    if (inSlot === 0 && player) { // :37958-37973 额前 216px 朝玩家月噬 456(0 伤,MoonLeechProj)
1607	      addProj(game, new MoonLeechProj(e, player));
1608	    }
1609	    // :37975-37989 inSlot=120/180/240 于玩家处召 401 月噬怪(门禁说明见 spawnMoonLeech)
1610	    if (player && (inSlot === 120 || inSlot === 180 || inSlot === 240)) spawnMoonLeech(game, e, player);
1611	  } else if (e.ai0 === 3 && player) { // 三连幻影矢(:37991-38015)
1612	    const pvx = (player as unknown as { vx: number }).vx ?? 0;
1613	    const pvy = (player as unknown as { vy: number }).vy ?? 0;
1614	    const dx = player.cx + pvx * 20 - e.cx, dy = player.cy + pvy * 20 - e.cy;
1615	    x.l0 = angleLerp(x.l0, Math.atan2(dy, dx), 0.5);
1616	    x.l1 = Math.min(1, x.l1 + 0.05);
1617	    if (inSlot === dur - 35) game.playSfxWav?.('NPC_Hit_6', 1, e.cx, e.cy);   // :38007 PlaySound(4,…,6)(曾借 roar 0.5)
1618	    if (inSlot === dur - 14 || inSlot === dur - 7 || inSlot === dur) {
1619	      // 眼球椭圆 (27,59)(:37727 vector200),8 速 30 伤
1620	      const exx = Math.cos(x.l0) * 27 * x.l1, eyy = Math.sin(x.l0) * 59 * x.l1;
1621	      const d = Math.hypot(dx, dy) || 1;
1622	      shoot(game, e.cx + exx, e.cy + eyy, (dx / d) * 8, (dy / d) * 8, 30, 462, 600);
1623	    }
1624	  }
1625	
1626	  // 帧推进(:38016-38049;注:原版 :38042-38048 钳制误写 localAI[2],此处按语义钳 [3])
1627	  const f2Target = f2T * 7, f3Target = f3T * 5;
1628	  if (f2Target > x.f2) x.f2 += 1; else if (f2Target < x.f2) x.f2 -= 1;
1629	  x.f2 = clamp(x.f2, 0, 14);
1630	  if (f3Target > x.f3) x.f3 += 1; else if (f3Target < x.f3) x.f3 -= 1;
1631	  x.f3 = clamp(x.f3, 0, 15);
1632	  if (x.f3 >= 15) e.iframes = 2; // dontTakeDamage = localAI[3]>=15(闭眼无敌)
1633	  e.spin = x.l0;
1634	}
1635	

```


---

## 🤖 Assistant · 2026-08-19T03:09:44.152Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the original decompiled source for each section. Let me start with Duke Fishron AI_069 at 49143-50128.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:44.153Z · glm-x-preview-260804

```
现在我来读取猪鲨 (Duke Fishron) AI_069 的原版反编译源码。
```


---

## 🤖 Assistant · 2026-08-19T03:09:44.171Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '49143,49270p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Duke Fishron AI_069 part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:44.212Z

**📎 ToolResult**

```
	private void AI_069_DukeFishron()
	{
		bool expertMode = Main.expertMode;
		float num = (expertMode ? 1.2f : 1f);
		bool flag = (double)life <= (double)lifeMax * 0.5;
		bool flag2 = expertMode && (double)life <= (double)lifeMax * 0.15;
		bool flag3 = ai[0] > 4f;
		bool flag4 = ai[0] > 9f;
		int num2 = (flag3 ? 3 : 5);
		bool flag5 = ai[3] < (float)(num2 * 2);
		if (flag4)
		{
			damage = (int)((float)defDamage * 1.1f * num);
			defense = 0;
		}
		else if (flag3)
		{
			damage = (int)((float)defDamage * 1.2f * num);
			defense = (int)((float)defDefense * 0.8f);
		}
		else
		{
			damage = defDamage;
			defense = defDefense;
		}
		int num3 = (expertMode ? 40 : 60);
		float num4 = (expertMode ? 0.55f : 0.45f);
		float num5 = (expertMode ? 8.5f : 7.5f);
		if (flag4)
		{
			num4 = 0.7f;
			num5 = 12f;
			num3 = 30;
		}
		else if (flag3 && flag5)
		{
			num4 = (expertMode ? 0.6f : 0.5f);
			num5 = (expertMode ? 10f : 8f);
			num3 = (expertMode ? 40 : 20);
		}
		else if (flag5 && !flag3 && !flag4)
		{
			num3 = 30;
		}
		int num6 = (expertMode ? 28 : 30);
		float num7 = (expertMode ? 17f : 16f);
		if (flag4)
		{
			num6 = 25;
			num7 = 27f;
		}
		else if (flag5 && flag3)
		{
			num6 = (expertMode ? 27 : 30);
			if (expertMode)
			{
				num7 = 21f;
			}
		}
		int num8 = 80;
		int num9 = 4;
		float num10 = 0.3f;
		float num11 = 5f;
		int num12 = 90;
		int num13 = 180;
		int num14 = 180;
		int num15 = 30;
		int num16 = 120;
		int num17 = 4;
		float num18 = 6f;
		float num19 = 20f;
		float num20 = MathF.PI * 2f / (float)(num16 / 2);
		int num21 = 75;
		Vector2 center = base.Center;
		Player player = Main.player[target];
		if (target < 0 || target == 255 || player.dead || !player.active || Vector2.Distance(player.Center, center) > 5600f)
		{
			TargetClosest();
			player = Main.player[target];
			netUpdate = true;
		}
		if (player.dead || Vector2.Distance(player.Center, center) > 5600f)
		{
			velocity.Y -= 0.4f;
			EncourageDespawn(10);
			if (ai[0] > 4f)
			{
				ai[0] = 5f;
			}
			else
			{
				ai[0] = 0f;
			}
			ai[2] = 0f;
		}
		bool flag6 = player.position.Y < 800f || (double)player.position.Y > Main.worldSurface * 16.0 || (player.position.X > 6400f && player.position.X < (float)(Main.maxTilesX * 16 - 6400));
		if (flag6)
		{
			num3 = 10;
			damage = defDamage * 2;
			defense = defDefense * 2;
			num7 += 6f;
		}
		bool flag7 = true;
		if (localAI[0] == 0f)
		{
			localAI[0] = 1f;
			alpha = 255;
			rotation = 0f;
			if (Main.netMode != 1)
			{
				ai[0] = -1f;
				netUpdate = true;
			}
		}
		float num22 = (float)Math.Atan2(player.Center.Y - center.Y, player.Center.X - center.X);
		if (spriteDirection == 1)
		{
			num22 += MathF.PI;
		}
		if (num22 < 0f)
		{
			num22 += MathF.PI * 2f;
		}
		if (num22 > MathF.PI * 2f)
		{
			num22 -= MathF.PI * 2f;
		}

```


---

## 🤖 Assistant · 2026-08-19T03:09:59.328Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Interesting: flag6 (enraged) in the original uses `player.position.Y` not `player.Center.Y`. Also note: `player.position.X > 6400 && player.position.X < (maxTilesX*16 - 6400)`. Our version uses `player.y` and `player.x` which are position (top-left), consistent. But our dukeEnraged uses `player.y < 800` — position.Y — good.

Note: our version computes enraged BEFORE the player.dead check, which doesn't matter since we check player exists.

But wait — our version's damage/defense modifiers: `if (enraged) { e.def.damage = b.dmg * 2; ... }` matches `damage = defDamage * 2; defense = defDefense * 2;`.

Also our chargeT/chargeSpd: `if (flag4) { chargeT = 25; chargeSpd = 27; }` — matches. But we miss the `else if (flag5 && flag3)` branch: `num6 = (expertMode ? 27 : 30); if (expertMode) num7 = 21f;` — in classic mode this is num6=30, num7 stays 16. Our version: chargeT = 30, chargeSpd = 16 default; flag4 overrides to 25/27. In classic, flag5&&flag3 gives 30/16 — same as default. OK.

Now check the enraged threshold `player.y > surface`: original is `Main.worldSurface * 16.0`. Our version uses `(game.world.groundLevel || Math.floor(st.h * 0.3)) * TILE`. That's approximate but presumably fine.

Continue reading.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:59.866Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '49270,49415p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Duke Fishron AI_069 part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:59.895Z

**📎 ToolResult**

```
		}
		if (ai[0] == -1f)
		{
			num22 = 0f;
		}
		if (ai[0] == 3f)
		{
			num22 = 0f;
		}
		if (ai[0] == 4f)
		{
			num22 = 0f;
		}
		if (ai[0] == 8f)
		{
			num22 = 0f;
		}
		float num23 = 0.04f;
		if (ai[0] == 1f || ai[0] == 6f)
		{
			num23 = 0f;
		}
		if (ai[0] == 7f)
		{
			num23 = 0f;
		}
		if (ai[0] == 3f)
		{
			num23 = 0.01f;
		}
		if (ai[0] == 4f)
		{
			num23 = 0.01f;
		}
		if (ai[0] == 8f)
		{
			num23 = 0.01f;
		}
		if (rotation < num22)
		{
			if ((double)(num22 - rotation) > Math.PI)
			{
				rotation -= num23;
			}
			else
			{
				rotation += num23;
			}
		}
		if (rotation > num22)
		{
			if ((double)(rotation - num22) > Math.PI)
			{
				rotation += num23;
			}
			else
			{
				rotation -= num23;
			}
		}
		if (rotation > num22 - num23 && rotation < num22 + num23)
		{
			rotation = num22;
		}
		if (rotation < 0f)
		{
			rotation += MathF.PI * 2f;
		}
		if (rotation > MathF.PI * 2f)
		{
			rotation -= MathF.PI * 2f;
		}
		if (rotation > num22 - num23 && rotation < num22 + num23)
		{
			rotation = num22;
		}
		if (ai[0] != -1f && ai[0] < 9f)
		{
			if (Collision.SolidCollision(position, width, height))
			{
				alpha += 15;
			}
			else
			{
				alpha -= 15;
			}
			if (alpha < 0)
			{
				alpha = 0;
			}
			if (alpha > 150)
			{
				alpha = 150;
			}
		}
		if (ai[0] == -1f)
		{
			flag7 = false;
			velocity *= 0.98f;
			int num24 = Math.Sign(player.Center.X - center.X);
			if (num24 != 0)
			{
				direction = num24;
				spriteDirection = -direction;
			}
			if (ai[2] > 20f)
			{
				velocity.Y = -2f;
				alpha -= 5;
				if (Collision.SolidCollision(position, width, height))
				{
					alpha += 15;
				}
				if (alpha < 0)
				{
					alpha = 0;
				}
				if (alpha > 150)
				{
					alpha = 150;
				}
			}
			if (ai[2] == (float)(num12 - 30))
			{
				int num25 = 36;
				for (int i = 0; i < num25; i++)
				{
					Vector2 vector = (Vector2.Normalize(velocity) * new Vector2((float)width / 2f, height) * 0.75f * 0.5f).RotatedBy((float)(i - (num25 / 2 - 1)) * (MathF.PI * 2f) / (float)num25) + base.Center;
					Vector2 vector2 = vector - base.Center;
					int num26 = Dust.NewDust(vector + vector2, 0, 0, 172, vector2.X * 2f, vector2.Y * 2f, 100, default(Color), 1.4f);
					Main.dust[num26].noGravity = true;
					Main.dust[num26].noLight = true;
					Main.dust[num26].velocity = Vector2.Normalize(vector2) * 3f;
				}
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 20);
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num21)
			{
				ai[0] = 0f;
				ai[1] = 0f;
				ai[2] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 0f && !player.dead)

```


---

## 🤖 Assistant · 2026-08-19T03:10:05.452Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '49415,49545p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Duke Fishron AI_069 part 3"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:05.481Z

**📎 ToolResult**

```
		else if (ai[0] == 0f && !player.dead)
		{
			if (ai[1] == 0f)
			{
				ai[1] = 300 * Math.Sign((center - player.Center).X);
			}
			Vector2 vector3 = Vector2.Normalize(player.Center + new Vector2(ai[1], -200f) - center - velocity) * num5;
			if (velocity.X < vector3.X)
			{
				velocity.X += num4;
				if (velocity.X < 0f && vector3.X > 0f)
				{
					velocity.X += num4;
				}
			}
			else if (velocity.X > vector3.X)
			{
				velocity.X -= num4;
				if (velocity.X > 0f && vector3.X < 0f)
				{
					velocity.X -= num4;
				}
			}
			if (velocity.Y < vector3.Y)
			{
				velocity.Y += num4;
				if (velocity.Y < 0f && vector3.Y > 0f)
				{
					velocity.Y += num4;
				}
			}
			else if (velocity.Y > vector3.Y)
			{
				velocity.Y -= num4;
				if (velocity.Y > 0f && vector3.Y < 0f)
				{
					velocity.Y -= num4;
				}
			}
			int num27 = Math.Sign(player.Center.X - center.X);
			if (num27 != 0)
			{
				if (ai[2] == 0f && num27 != direction)
				{
					rotation += MathF.PI;
				}
				direction = num27;
				if (spriteDirection != -direction)
				{
					rotation += MathF.PI;
				}
				spriteDirection = -direction;
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num3)
			{
				int num28 = 0;
				switch ((int)ai[3])
				{
				case 0:
				case 1:
				case 2:
				case 3:
				case 4:
				case 5:
				case 6:
				case 7:
				case 8:
				case 9:
					num28 = 1;
					break;
				case 10:
					ai[3] = 1f;
					num28 = 2;
					break;
				case 11:
					ai[3] = 0f;
					num28 = 3;
					break;
				}
				if (flag6 && num28 == 2)
				{
					num28 = 3;
				}
				if (flag)
				{
					num28 = 4;
				}
				switch (num28)
				{
				case 1:
					ai[0] = 1f;
					ai[1] = 0f;
					ai[2] = 0f;
					velocity = Vector2.Normalize(player.Center - center) * num7;
					rotation = (float)Math.Atan2(velocity.Y, velocity.X);
					if (num27 != 0)
					{
						direction = num27;
						if (spriteDirection == 1)
						{
							rotation += MathF.PI;
						}
						spriteDirection = -direction;
					}
					break;
				case 2:
					ai[0] = 2f;
					ai[1] = 0f;
					ai[2] = 0f;
					break;
				case 3:
					ai[0] = 3f;
					ai[1] = 0f;
					ai[2] = 0f;
					if (flag6)
					{
						ai[2] = num12 - 40;
					}
					break;
				case 4:
					ai[0] = 4f;
					ai[1] = 0f;
					ai[2] = 0f;
					break;
				}
				netUpdate = true;
			}
		}
		else if (ai[0] == 1f)
		{

```


---

## 🤖 Assistant · 2026-08-19T03:10:17.278Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important structural note: in the original, the flag (half health) check `if (flag) { num28 = 4; }` happens inside `ai[2] >= num3` — i.e. only at the end of a hover cycle, and after the switch. Our dukePick1 matches this. But wait — important: in the original, the half-health check `if (flag) num28 = 4` overrides even the switch results. Our version: `if (e.hp <= e.maxHp * 0.5) next = 4;` — same.

Hmm, but note in dukePick1: `if (a3 >= 0 && a3 <= 9) next = 1;` — matches cases 0-9. `else if (a3 === 10) { e.ai3 = 1; next = 2; }` — matches. `else if (a3 === 11) { e.ai3 = 0; next = 3; }` — matches. Default: no case → num28 = 0 → nothing happens, ai[2] keeps incrementing... wait no. If num28==0, then the switch(num28) does nothing, and ai[2] was already incremented past num3. Next tick ai[2] >= num3 still true, so it re-evaluates the switch each tick with ai[3] unchanged. So it keeps hovering with ai[2] growing — matches our "next = 0 → nothing" behavior since our case 0 also re-runs hover and increments ai2 each tick. OK.

Now the important part: in the original state 1 (charge):

Let me continue reading 49545 onwards.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:17.819Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '49545,49700p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Duke Fishron AI_069 part 4"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:17.853Z

**📎 ToolResult**

```
		{
			int num29 = 7;
			for (int j = 0; j < num29; j++)
			{
				Vector2 vector4 = (Vector2.Normalize(velocity) * new Vector2((float)(width + 50) / 2f, height) * 0.75f).RotatedBy((double)(j - (num29 / 2 - 1)) * Math.PI / (double)(float)num29) + center;
				Vector2 vector5 = ((float)(Main.rand.NextDouble() * 3.1415927410125732) - MathF.PI / 2f).ToRotationVector2() * Main.rand.Next(3, 8);
				int num30 = Dust.NewDust(vector4 + vector5, 0, 0, 172, vector5.X * 2f, vector5.Y * 2f, 100, default(Color), 1.4f);
				Main.dust[num30].noGravity = true;
				Main.dust[num30].noLight = true;
				Main.dust[num30].velocity /= 4f;
				Main.dust[num30].velocity -= velocity;
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num6)
			{
				ai[0] = 0f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] += 2f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 2f)
		{
			if (ai[1] == 0f)
			{
				ai[1] = 300 * Math.Sign((center - player.Center).X);
			}
			Vector2 vector6 = Vector2.Normalize(player.Center + new Vector2(ai[1], -200f) - center - velocity) * num11;
			if (velocity.X < vector6.X)
			{
				velocity.X += num10;
				if (velocity.X < 0f && vector6.X > 0f)
				{
					velocity.X += num10;
				}
			}
			else if (velocity.X > vector6.X)
			{
				velocity.X -= num10;
				if (velocity.X > 0f && vector6.X < 0f)
				{
					velocity.X -= num10;
				}
			}
			if (velocity.Y < vector6.Y)
			{
				velocity.Y += num10;
				if (velocity.Y < 0f && vector6.Y > 0f)
				{
					velocity.Y += num10;
				}
			}
			else if (velocity.Y > vector6.Y)
			{
				velocity.Y -= num10;
				if (velocity.Y > 0f && vector6.Y < 0f)
				{
					velocity.Y -= num10;
				}
			}
			if (ai[2] == 0f)
			{
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 20);
			}
			if (ai[2] % (float)num9 == 0f)
			{
				SoundEngine.PlaySound(4, (int)base.Center.X, (int)base.Center.Y, 19);
				if (Main.netMode != 1)
				{
					Vector2 vector7 = Vector2.Normalize(player.Center - center) * (width + 20) / 2f + center;
					NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)vector7.X, (int)vector7.Y + 45, 371);
				}
			}
			int num31 = Math.Sign(player.Center.X - center.X);
			if (num31 != 0)
			{
				direction = num31;
				if (spriteDirection != -direction)
				{
					rotation += MathF.PI;
				}
				spriteDirection = -direction;
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num8)
			{
				ai[0] = 0f;
				ai[1] = 0f;
				ai[2] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 3f)
		{
			velocity *= 0.98f;
			velocity.Y = MathHelper.Lerp(velocity.Y, 0f, 0.02f);
			if (ai[2] == (float)(num12 - 30))
			{
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 9);
			}
			if (Main.netMode != 1 && ai[2] == (float)(num12 - 30))
			{
				Vector2 vector8 = rotation.ToRotationVector2() * (Vector2.UnitX * direction) * (width + 20) / 2f + center;
				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector8.X, vector8.Y, direction * 2, 8f, 385, 0, 0f, Main.myPlayer);
				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector8.X, vector8.Y, -direction * 2, 8f, 385, 0, 0f, Main.myPlayer);
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num12)
			{
				ai[0] = 0f;
				ai[1] = 0f;
				ai[2] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 4f)
		{
			flag7 = false;
			velocity *= 0.98f;
			velocity.Y = MathHelper.Lerp(velocity.Y, 0f, 0.02f);
			if (ai[2] == (float)(num13 - 60))
			{
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 20);
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num13)
			{
				ai[0] = 5f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 5f && !player.dead)
		{
			if (ai[1] == 0f)
			{
				ai[1] = 300 * Math.Sign((center - player.Center).X);
			}
			Vector2 vector9 = Vector2.Normalize(player.Center + new Vector2(ai[1], -200f) - center - velocity) * num5;
			if (velocity.X < vector9.X)
			{
				velocity.X += num4;
				if (velocity.X < 0f && vector9.X > 0f)
				{
					velocity.X += num4;
				}
			}
			else if (velocity.X > vector9.X)
			{
				velocity.X -= num4;
				if (velocity.X > 0f && vector9.X < 0f)
				{
					velocity.X -= num4;

```


---

## 🤖 Assistant · 2026-08-19T03:10:24.403Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
State 3 (sharknado): matches our implementation. Note the sound: PlaySound(29, ..., 9) — our version uses 'Zombie_9'. PlaySound 29 is Zombie, style 9 → Zombie_9. OK.

One detail: our `dukeSharknado` for small nado: `ox = Math.cos(e.spin) * st.dir * (e.w + 20) / 2;` — original: `vector8 = rotation.ToRotationVector2() * (Vector2.UnitX * direction) * (width + 20) / 2f + center`. Hmm, `rotation.ToRotationVector2()` is (cos rot, sin rot). `Vector2.UnitX * direction` is (direction, 0). The `*` between two Vector2s is component-wise multiply. So vector8.X = cos(rot) * direction * (width+20)/2 + center.X, vector8.Y = sin(rot) * 0 * ... + center.Y = center.Y. Our version: `ox = Math.cos(e.spin) * st.dir * (e.w + 20) / 2`, and passes `(e.cx + ox, e.cy)`. Good.

Continue with state 5 hover → 7, 8, etc.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:24.846Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '49700,49870p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Duke Fishron AI_069 part 5"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:24.881Z

**📎 ToolResult**

```
					velocity.X -= num4;
				}
			}
			if (velocity.Y < vector9.Y)
			{
				velocity.Y += num4;
				if (velocity.Y < 0f && vector9.Y > 0f)
				{
					velocity.Y += num4;
				}
			}
			else if (velocity.Y > vector9.Y)
			{
				velocity.Y -= num4;
				if (velocity.Y > 0f && vector9.Y < 0f)
				{
					velocity.Y -= num4;
				}
			}
			int num32 = Math.Sign(player.Center.X - center.X);
			if (num32 != 0)
			{
				if (ai[2] == 0f && num32 != direction)
				{
					rotation += MathF.PI;
				}
				direction = num32;
				if (spriteDirection != -direction)
				{
					rotation += MathF.PI;
				}
				spriteDirection = -direction;
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num3)
			{
				int num33 = 0;
				switch ((int)ai[3])
				{
				case 0:
				case 1:
				case 2:
				case 3:
				case 4:
				case 5:
					num33 = 1;
					break;
				case 6:
					ai[3] = 1f;
					num33 = 2;
					break;
				case 7:
					ai[3] = 0f;
					num33 = 3;
					break;
				}
				if (flag2)
				{
					num33 = 4;
				}
				if (flag6 && num33 == 2)
				{
					num33 = 3;
				}
				switch (num33)
				{
				case 1:
					ai[0] = 6f;
					ai[1] = 0f;
					ai[2] = 0f;
					velocity = Vector2.Normalize(player.Center - center) * num7;
					rotation = (float)Math.Atan2(velocity.Y, velocity.X);
					if (num32 != 0)
					{
						direction = num32;
						if (spriteDirection == 1)
						{
							rotation += MathF.PI;
						}
						spriteDirection = -direction;
					}
					break;
				case 2:
					velocity = Vector2.Normalize(player.Center - center) * num19;
					rotation = (float)Math.Atan2(velocity.Y, velocity.X);
					if (num32 != 0)
					{
						direction = num32;
						if (spriteDirection == 1)
						{
							rotation += MathF.PI;
						}
						spriteDirection = -direction;
					}
					ai[0] = 7f;
					ai[1] = 0f;
					ai[2] = 0f;
					break;
				case 3:
					ai[0] = 8f;
					ai[1] = 0f;
					ai[2] = 0f;
					break;
				case 4:
					ai[0] = 9f;
					ai[1] = 0f;
					ai[2] = 0f;
					break;
				}
				netUpdate = true;
			}
		}
		else if (ai[0] == 6f)
		{
			int num34 = 7;
			for (int k = 0; k < num34; k++)
			{
				Vector2 vector10 = (Vector2.Normalize(velocity) * new Vector2((float)(width + 50) / 2f, height) * 0.75f).RotatedBy((double)(k - (num34 / 2 - 1)) * Math.PI / (double)(float)num34) + center;
				Vector2 vector11 = ((float)(Main.rand.NextDouble() * 3.1415927410125732) - MathF.PI / 2f).ToRotationVector2() * Main.rand.Next(3, 8);
				int num35 = Dust.NewDust(vector10 + vector11, 0, 0, 172, vector11.X * 2f, vector11.Y * 2f, 100, default(Color), 1.4f);
				Main.dust[num35].noGravity = true;
				Main.dust[num35].noLight = true;
				Main.dust[num35].velocity /= 4f;
				Main.dust[num35].velocity -= velocity;
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num6)
			{
				ai[0] = 5f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] += 2f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 7f)
		{
			if (ai[2] == 0f)
			{
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 20);
			}
			if (ai[2] % (float)num17 == 0f)
			{
				SoundEngine.PlaySound(4, (int)base.Center.X, (int)base.Center.Y, 19);
				if (Main.netMode != 1)
				{
					Vector2 vector12 = Vector2.Normalize(velocity) * (width + 20) / 2f + center;
					int num36 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)vector12.X, (int)vector12.Y + 45, 371);
					Main.npc[num36].target = target;
					Main.npc[num36].velocity = Vector2.Normalize(velocity).RotatedBy(MathF.PI / 2f * (float)direction) * num18;
					Main.npc[num36].netUpdate = true;
					Main.npc[num36].ai[3] = (float)Main.rand.Next(80, 121) / 100f;
				}
			}
			velocity = velocity.RotatedBy((0f - num20) * (float)direction);
			rotation -= num20 * (float)direction;
			ai[2] += 1f;
			if (ai[2] >= (float)num16)
			{
				ai[0] = 5f;
				ai[1] = 0f;
				ai[2] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 8f)
		{
			velocity *= 0.98f;
			velocity.Y = MathHelper.Lerp(velocity.Y, 0f, 0.02f);
			if (ai[2] == (float)(num12 - 30))
			{

```


---

## 🤖 Assistant · 2026-08-19T03:10:39.648Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note state 5 → case 2 (spin dash): the charge velocity is `num19` = 20 (spinDashSpd). Our version does that inline. And case 2's direction rotation matches.

Note in state 7 (spin): bubble velocity = `Vector2.Normalize(velocity).RotatedBy(MathF.PI / 2f * direction) * num18` — matches our ang + (π/2)*dir.

One difference: our case 7 spawns bubble on `e.ai2 % DUKE.spinEvery === 0` — original `ai[2] % num17 == 0` → at ai2==0 as well. Our version spawns at ai2==0. But note in our version, the bubble spawn happens BEFORE velocity rotation; in the original, also before `velocity = velocity.RotatedBy(...)` — yes: spawn uses current velocity, then velocity rotates. Good.

Wait, one thing: original spawn at ai2==0: velocity was set to num19*direction toward player from state 5 transition. OK.

Also in our case 7, the bubble spawn code sets `bub.ai3 = (80 + Math.random() * 41) / 100;` — original `Main.rand.Next(80, 121) / 100f` → 80..120 / 100. Ours: 80 + rand*41 → 80..121. Slight off-by-one, negligible.

Also `Main.npc[num36].target = target` — set bubble target so it initializes properly. We set bInit/ai fields manually.

Continue reading 49870-50130.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:40.137Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '49870,50130p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Duke Fishron AI_069 part 6"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:40.164Z

**📎 ToolResult**

```
			{
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 20);
			}
			if (Main.netMode != 1 && ai[2] == (float)(num12 - 30))
			{
				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center.X, center.Y, 0f, 0f, 385, 0, 0f, Main.myPlayer, 1f, target + 1, flag6 ? 1 : 0);
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num12)
			{
				ai[0] = 5f;
				ai[1] = 0f;
				ai[2] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 9f)
		{
			flag7 = false;
			if (ai[2] < (float)(num14 - 90))
			{
				if (Collision.SolidCollision(position, width, height))
				{
					alpha += 15;
				}
				else
				{
					alpha -= 15;
				}
				if (alpha < 0)
				{
					alpha = 0;
				}
				if (alpha > 150)
				{
					alpha = 150;
				}
			}
			else if (alpha < 255)
			{
				alpha += 4;
				if (alpha > 255)
				{
					alpha = 255;
				}
			}
			velocity *= 0.98f;
			velocity.Y = MathHelper.Lerp(velocity.Y, 0f, 0.02f);
			if (ai[2] == (float)(num14 - 60))
			{
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 20);
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num14)
			{
				ai[0] = 10f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 10f && !player.dead)
		{
			chaseable = false;
			if (alpha < 255)
			{
				alpha += 25;
				if (alpha > 255)
				{
					alpha = 255;
				}
			}
			if (ai[1] == 0f)
			{
				ai[1] = 360 * Math.Sign((center - player.Center).X);
			}
			Vector2 desiredVelocity = Vector2.Normalize(player.Center + new Vector2(ai[1], -200f) - center - velocity) * num5;
			SimpleFlyMovement(desiredVelocity, num4);
			int num37 = Math.Sign(player.Center.X - center.X);
			if (num37 != 0)
			{
				if (ai[2] == 0f && num37 != direction)
				{
					rotation += MathF.PI;
					for (int l = 0; l < oldPos.Length; l++)
					{
						oldPos[l] = Vector2.Zero;
					}
				}
				direction = num37;
				if (spriteDirection != -direction)
				{
					rotation += MathF.PI;
				}
				spriteDirection = -direction;
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num3)
			{
				int num38 = 0;
				switch ((int)ai[3])
				{
				case 0:
				case 2:
				case 3:
				case 5:
				case 6:
				case 7:
					num38 = 1;
					break;
				case 1:
				case 4:
				case 8:
					num38 = 2;
					break;
				}
				switch (num38)
				{
				case 1:
					ai[0] = 11f;
					ai[1] = 0f;
					ai[2] = 0f;
					velocity = Vector2.Normalize(player.Center - center) * num7;
					rotation = (float)Math.Atan2(velocity.Y, velocity.X);
					if (num37 != 0)
					{
						direction = num37;
						if (spriteDirection == 1)
						{
							rotation += MathF.PI;
						}
						spriteDirection = -direction;
					}
					break;
				case 2:
					ai[0] = 12f;
					ai[1] = 0f;
					ai[2] = 0f;
					break;
				case 3:
					ai[0] = 13f;
					ai[1] = 0f;
					ai[2] = 0f;
					break;
				}
				netUpdate = true;
			}
		}
		else if (ai[0] == 11f)
		{
			chaseable = true;
			alpha -= 25;
			if (alpha < 0)
			{
				alpha = 0;
			}
			int num39 = 7;
			for (int m = 0; m < num39; m++)
			{
				Vector2 vector13 = (Vector2.Normalize(velocity) * new Vector2((float)(width + 50) / 2f, height) * 0.75f).RotatedBy((double)(m - (num39 / 2 - 1)) * Math.PI / (double)(float)num39) + center;
				Vector2 vector14 = ((float)(Main.rand.NextDouble() * 3.1415927410125732) - MathF.PI / 2f).ToRotationVector2() * Main.rand.Next(3, 8);
				int num40 = Dust.NewDust(vector13 + vector14, 0, 0, 172, vector14.X * 2f, vector14.Y * 2f, 100, default(Color), 1.4f);
				Main.dust[num40].noGravity = true;
				Main.dust[num40].noLight = true;
				Main.dust[num40].velocity /= 4f;
				Main.dust[num40].velocity -= velocity;
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num6)
			{
				ai[0] = 10f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] += 1f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 12f)
		{
			flag7 = false;
			chaseable = false;
			if (alpha < 255)
			{
				alpha += 17;
				if (alpha > 255)
				{
					alpha = 255;
				}
			}
			velocity *= 0.98f;
			velocity.Y = MathHelper.Lerp(velocity.Y, 0f, 0.02f);
			if (ai[2] == (float)(num15 / 2))
			{
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 20);
			}
			if (Main.netMode != 1 && ai[2] == (float)(num15 / 2))
			{
				if (ai[1] == 0f)
				{
					ai[1] = 300 * Math.Sign((center - player.Center).X);
				}
				Vector2 vector15 = player.Center + new Vector2(0f - ai[1], -200f);
				Vector2 vector16 = (base.Center = vector15);
				center = vector16;
				int num41 = Math.Sign(player.Center.X - center.X);
				if (num41 != 0)
				{
					if (ai[2] == 0f && num41 != direction)
					{
						rotation += MathF.PI;
						for (int n = 0; n < oldPos.Length; n++)
						{
							oldPos[n] = Vector2.Zero;
						}
					}
					direction = num41;
					if (spriteDirection != -direction)
					{
						rotation += MathF.PI;
					}
					spriteDirection = -direction;
				}
			}
			ai[2] += 1f;
			if (ai[2] >= (float)num15)
			{
				ai[0] = 10f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] += 1f;
				if (ai[3] >= 9f)
				{
					ai[3] = 0f;
				}
				netUpdate = true;
			}
		}
		else if (ai[0] == 13f)
		{
			if (ai[2] == 0f)
			{
				SoundEngine.PlaySound(29, (int)center.X, (int)center.Y, 20);
			}
			velocity = velocity.RotatedBy((0f - num20) * (float)direction);
			rotation -= num20 * (float)direction;
			ai[2] += 1f;
			if (ai[2] >= (float)num16)
			{
				ai[0] = 10f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] += 1f;
				netUpdate = true;
			}
		}
		dontTakeDamage = !flag7;
	}

	private void AI_037_Destroyer()
	{

```


---

## 🤖 Assistant · 2026-08-19T03:11:29.496Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Duke Fishron fully read. Now checking important details vs ours:

1. State 10 hover offset: original uses `ai[1] = 360 * Math.Sign(...)` — our case 10 passes `360` as sideOff. Good.

2. State 10 → switch(ai[3]): cases 0,2,3,5,6,7 → num38=1; cases 1,4,8 → num38=2. Note: ai[3] after state 12 reaches 9 → resets to 0. But wait — case 3 (num38=3 → ai0=13) is unreachable because num38 is only 1 or 2 in state 10's switch. Our version: `const next = (a3 === 0 || a3 === 2 || a3 === 3 || a3 === 5 || a3 === 6 || a3 === 7) ? 1 : 2;` — matches (all other values → 2). Since state 13 is unreachable in vanilla too (num38=3 never set), our case 13 exists but unreachable — fine.

3. State 12 teleport: original `ai[2] == num15/2` (=15) — teleport AND sound at that tick. Our version does the teleport in `if (e.ai2 === DUKE.teleT / 2)` and plays sound there. Good.

4. Big sharknado bolt (state 8): `Projectile.NewProjectile(..., 385, 0, 0f, Main.myPlayer, 1f, target + 1, flag6 ? 1 : 0)` — ai0=1, ai1=target+1, ai2=flag6. Our DukeSharknadoBolt big constructor takes enraged flag. Good.

5. Half-health check timing: original checks `flag` ONLY within the ai[2]>=num3 branch of states 0 and 5. Ours matches (dukePick1 checks hp; dukePick2 doesn't check flag — correct! In the original, state 5's switch doesn't have a `flag` check; only `flag2` (expert). Our dukePick2 has flag2 as commented-out code with comment "expert 不可达" — and does NOT apply it since classic. Hmm wait, in the original state 5: `if (flag2) { num33 = 4; }`. flag2 = expertMode && life <= 15%. In classic mode flag2 is always false. Our comment says expert branch preserved as comment. OK for classic.

6. Enraged (flag6): sets `num3 = 10; damage = defDamage * 2; defense = defDefense * 2; num7 += 6f;`. Our code: `if (enraged) { hoverT = 10; chargeSpd += 6; }` and damage/defense ×2. But note ORDER: in the original, flag6 block runs AFTER num7 determined by flag4 etc. Our order: flag4 sets chargeSpd=27, then enraged adds 6 → 33. Same as original (27+6=33). OK.

One subtle thing: original enraged damage = defDamage * 2 (not multiplied by expert `num` factor). Ours: `e.def.damage = b.dmg * 2` — overrides any flag4/flag3 multiplier. Matches.

7. flag7/dontTakeDamage: original sets flag7=false in states -1, 4, 9, 12 (invuln states). Our invuln=true in case -1, 4, 9, 12. Good.

8. Alpha handling: our `if (e.ai0 !== -1 && e.ai0 < 9)` — original `if (ai[0] != -1f && ai[0] < 9f)`. Good.

Hmm wait — actually in the original, alpha is clamped to [0,150] in that block. Our version: `e.spawnAlpha = inSolid(game, e) ? Math.min(255, e.spawnAlpha + 15) : Math.max(0, e.spawnAlpha - 15);` — clamps to 255, not 150! Original clamps alpha to 150 (which means the Duke becomes semi-transparent... wait, alpha 255 in Terraria NPC drawing is INVISIBLE? Let me think. In Terraria, NPC alpha: 0 = fully visible, 255 = invisible. Alpha is used as transparency. So alpha 150 = quite transparent; 255 = fully invisible.

Hmm — our spawnAlpha semantics: spawnAlpha=255 at spawn, and in case -1 else branch `if (e.spawnAlpha < 255) e.spawnAlpha = 255`. Then in the visible block, alpha decreases to 0 when not in solid → visible. So our spawnAlpha matches Terraria alpha semantics (255 = invisible, 0 = visible). But we clamp to 255 instead of 150. Minor numeric — but wait, actually the original clamp is `alpha > 150 → alpha = 150`?? Hmm, actually for Duke Fishron the vanish max is 150? Hmm, in game the Duke fades to semi-transparent when out of sight, not fully invisible. Yes — the max alpha (transparency) is 150. Our version lets it go to 255 (fully invisible). That's a minor visual divergence — but wait, is spawnAlpha used as visibility in our render? If spawnAlpha=255 means invisible, then our Duke would become FULLY invisible when off in solid, vs vanilla semi-transparent. This is a numeric-ish deviation but structural enough to note? It's a minor clamp. Severity low. Might include as minor note.

Actually wait — let me double check: in state 10 (expert), alpha += 25 up to 255 (invisible) — that's the "invisible approach". And in the main block `ai[0] < 9` applies only to states 0..8. So in states 0-8 max transparency = 150. Ours clamps at 255 → Duke disappears entirely when player can't see him (in solid). Hmm, but wait — `inSolid` checks the Duke's own position being inside solid tiles, not line of sight. Anyway it's the same condition as the original SolidCollision.

Let me note it as a minor finding (confidence high, severity low).

9. The rotation code: ours matches.

10. In case -1 spawn: `e.ai2 === DUKE.nadoT - 30` → 60. num12-30 = 60. Good. Sound: PlaySound(29,...,20) — Zombie_20. Good.

11. In case 0: our dukeHover passes sideOff=300 — original `ai[1] = 300 * Math.Sign((center - player.Center).X)`. Good.

12. State 2 bubble: `vector7 = Vector2.Normalize(player.Center - center) * (width + 20) / 2f + center;` then NewNPC at (vector7.X, vector7.Y + 45, 371). Our version: `bub.x = e.cx + (ddx / dd) * ((e.w + 20) / 2) - bub.w / 2; bub.y = e.cy + (ddy / dd) * ((e.w + 20) / 2) + 45 - bub.h / 2;` — converts center to top-left. Good.

13. In case 2 hover: original uses num11 (5) speed and num10 (0.3) acc. Ours: DUKE.bubbleSpd=5, DUKE.bubbleAcc=0.3. Good. Also `ai[1] = 300 * Sign(...)` side offset. Ours. Good.

14. State 1/6 charge particles — ours approximates with spawnParticles. Fine.

15. Player-dead/far branch: ours checks distance > 5600 and player.dead — and also `!player`. Original also does TargetClosest() first when target invalid; ours lacks TargetClosest but has fallback null → despawn. Fine-ish.

Also note in ours: `e.ai0 = e.ai0 > 4 ? 5 : 0;` matches.

One important thing: in the original, the far/dead branch does NOT return — it continues into flag6 computation, rotation code, and the state switch in the same tick (since velocity.Y -= 0.4 then states run... wait no: after the dead branch, the code continues: flag6 calc, flag7=true, localAI[0] init, rotation targeting, then the state machine. So state machine still runs! E.g. if ai0=0 and player.dead: `else if (ai[0] == 0f && !player.dead)` fails → nothing. State 1 (charge) would still run its particle code and ai2 increment! Hmm interesting. Our version `return`s early. That means in our version, during player-dead, ai2 resets to 0 and no state runs — matches effectively since original resets ai[2]=0 in the dead branch; for state 1, ai[2] would increment from 0 with particles... then if charge completes, ai[0]=0. Minor difference: original continues running charge state motion while dead (with velocity unchanged — charge keeps flying), ours stops moving horizontally (only vy -= 0.4). Meh — flee semantics. The charge would continue flying straight in original. Ours: vy -= 0.4 and no x movement. Minor deviation in flee behavior; acceptable? It's a subtle behavioral difference. Original: player dead → velocity.Y -= 0.4 each tick but state 1 continues ai2++ until chargeT then back to hover 0... but hover needs !player.dead. So Duke would keep flying in a straight line slightly rising. Ours: rises with no horizontal movement. Low severity.

Now the enraged check: our dukeEnraged uses `player.y > surface` where surface = groundLevel*TILE. Original: `player.position.Y > Main.worldSurface * 16.0`. worldSurface is the tile-Y of the surface (e.g. ~ tiles). groundLevel is presumably worldSurface equivalent in our project. OK.

BUT: ours checks `(player.x > 6400 && player.x < st.w * TILE - 6400)` — matches original `player.position.X > 6400 && player.position.X < maxTilesX*16 - 6400`. Good.

Now Duke bubble AI 371 @35122. Let me read.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:30.069Z · glm-x-preview-260804

```
Duke 的主要状态机已验证。现在我来检查 bubble (371) 和 sharkron (372/373) 的原版逻辑。
```


---

## 🤖 Assistant · 2026-08-19T03:11:30.657Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '35122,35330p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs bubble 371 and sharkron 372/373"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:30.686Z

**📎 ToolResult**

```
		else if (aiStyle == 70)
		{
			if (target == 255)
			{
				TargetClosest();
				this.ai[3] = (float)Main.rand.Next(80, 121) / 100f;
				float num1074 = (float)Main.rand.Next(165, 265) / 15f;
				velocity = Vector2.Normalize(Main.player[target].Center - base.Center + new Vector2(Main.rand.Next(-100, 101), Main.rand.Next(-100, 101))) * num1074;
				netUpdate = true;
			}
			Vector2 vector124 = Vector2.Normalize(Main.player[target].Center - base.Center);
			velocity = (velocity * 40f + vector124 * 20f) / 41f;
			scale = this.ai[3];
			alpha -= 30;
			if (alpha < 50)
			{
				alpha = 50;
			}
			alpha = 50;
			velocity.X = (velocity.X * 50f + Main.windSpeedCurrent * 2f + (float)Main.rand.Next(-10, 11) * 0.1f) / 51f;
			velocity.Y = (velocity.Y * 50f + -0.25f + (float)Main.rand.Next(-10, 11) * 0.2f) / 51f;
			if (velocity.Y > 0f)
			{
				velocity.Y -= 0.04f;
			}
			if (this.ai[0] == 0f)
			{
				int num1075 = 40;
				Rectangle rect = getRect();
				rect.X -= num1075 + width / 2;
				rect.Y -= num1075 + height / 2;
				rect.Width += num1075 * 2;
				rect.Height += num1075 * 2;
				for (int num1076 = 0; num1076 < 255; num1076++)
				{
					Player player11 = Main.player[num1076];
					if (player11.active && !player11.dead && rect.Intersects(player11.getRect()))
					{
						this.ai[0] = 1f;
						this.ai[1] = 4f;
						netUpdate = true;
						break;
					}
				}
			}
			if (this.ai[0] == 0f)
			{
				this.ai[1]++;
				if (this.ai[1] >= 150f)
				{
					this.ai[0] = 1f;
					this.ai[1] = 4f;
				}
			}
			if (this.ai[0] == 1f)
			{
				this.ai[1]--;
				if (this.ai[1] <= 0f)
				{
					life = 0;
					HitEffect();
					active = false;
					return;
				}
			}
			if (justHit || this.ai[0] == 1f)
			{
				dontTakeDamage = true;
				position = base.Center;
				width = (height = 100);
				position = new Vector2(position.X - (float)(width / 2), position.Y - (float)(height / 2));
				EncourageDespawn(3);
			}
		}
		else if (aiStyle == 71)
		{
			noTileCollide = true;
			int num1077 = 90;
			if (target < 0 || target == 255 || Main.player[target].dead)
			{
				TargetClosest(faceTarget: false);
				direction = 1;
				netUpdate = true;
			}
			if (this.ai[0] == 0f)
			{
				this.ai[1]++;
				_ = type;
				_ = 372;
				noGravity = true;
				dontTakeDamage = true;
				velocity.Y = this.ai[3];
				if (type == 373)
				{
					float num1078 = MathF.PI / 30f;
					float num1079 = this.ai[2];
					float num1080 = (float)(Math.Cos(num1078 * localAI[1]) - 0.5) * num1079;
					position.X -= num1080 * (float)(-direction);
					localAI[1]++;
					num1080 = (float)(Math.Cos(num1078 * localAI[1]) - 0.5) * num1079;
					position.X += num1080 * (float)(-direction);
					if (Math.Abs(Math.Cos(num1078 * localAI[1]) - 0.5) > 0.25)
					{
						spriteDirection = ((!(Math.Cos(num1078 * localAI[1]) - 0.5 >= 0.0)) ? 1 : (-1));
					}
					rotation = velocity.Y * (float)spriteDirection * 0.1f;
					if ((double)rotation < -0.2)
					{
						rotation = -0.2f;
					}
					if ((double)rotation > 0.2)
					{
						rotation = 0.2f;
					}
					alpha -= 6;
					if (alpha < 0)
					{
						alpha = 0;
					}
				}
				if (this.ai[1] >= (float)num1077)
				{
					this.ai[0] = 1f;
					this.ai[1] = 0f;
					if (!Collision.SolidCollision(position, width, height))
					{
						this.ai[1] = 1f;
					}
					SoundEngine.PlaySound(4, (int)base.Center.X, (int)base.Center.Y, 19);
					TargetClosest();
					spriteDirection = direction;
					Vector2 vector125 = Main.player[target].Center - base.Center;
					vector125.Normalize();
					velocity = vector125 * 16f;
					rotation = velocity.ToRotation();
					if (direction == -1)
					{
						rotation += MathF.PI;
					}
					netUpdate = true;
				}
			}
			else
			{
				if (this.ai[0] != 1f)
				{
					return;
				}
				noGravity = true;
				if (!Collision.SolidCollision(position, width, height))
				{
					if (this.ai[1] < 1f)
					{
						this.ai[1] = 1f;
					}
				}
				else
				{
					alpha -= 15;
					if (alpha < 150)
					{
						alpha = 150;
					}
				}
				if (this.ai[1] >= 1f)
				{
					alpha -= 60;
					if (alpha < 0)
					{
						alpha = 0;
					}
					dontTakeDamage = false;
					this.ai[1]++;
					if (Collision.SolidCollision(position, width, height))
					{
						if (DeathSound != null)
						{
							SoundEngine.PlaySound(DeathSound, position);
						}
						life = 0;
						HitEffect();
						active = false;
						return;
					}
				}
				if (this.ai[1] >= 60f)
				{
					noGravity = false;
				}
				rotation = velocity.ToRotation();
				if (direction == -1)
				{
					rotation += MathF.PI;
				}
			}
		}
		else if (aiStyle == 72)
		{
			if (type == 384)
			{
				int num1081 = (int)this.ai[0];
				if (Main.npc[num1081].active && Main.npc[num1081].type == 383)
				{
					velocity = Vector2.Zero;
					position = Main.npc[num1081].Center;
					position.X -= width / 2;
					position.Y -= height / 2;
					gfxOffY = Main.npc[num1081].gfxOffY;
					Lighting.AddLight((int)base.Center.X / 16, (int)base.Center.Y / 16, 0.1f, 0.5f, 0.7f);

```


---

## 🤖 Assistant · 2026-08-19T03:12:20.188Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Bubble 371 (aiStyle 70) details vs ours:

- Init when target==255: ai[3] = rand(80,121)/100; velocity = Normalize(playerCenter - center + rand(-100,101)) * rand(165,265)/15. Ours: `(80 + rand*41)/100`, `(165 + rand*100)/15`, and jx = e.cx - player.cx + (rand-0.5)*200 → that's -(player.cx - e.cx) + rand(-100..100). Then velocity = -(jx/d)*spd = (player-e)... let me check: jx = e.cx - player.cx + randoffset; velocity = -(jx/d)*spd = (player.cx - e.cx - randoffset)/d * spd = Normalize(player - center + (−randoffset)). Hmm: -(e.cx - player.cx + r) = player.cx - e.cx - r. Original: player.Center - Center + new Vector2(Next(-100,101)) — i.e. +r where r ∈ [-100,100]. Ours: -r where r ∈ [-100,100] — same distribution. Fine.

- alpha -= 30, floor 50, then `alpha = 50;` (unconditional). Ours: spawnAlpha = 50. OK.

- Wind: velocity.X = (vx*50 + windSpeed*2 + rand(-10,11)*0.1)/51. Ours: (vx*50 + (Math.random()-0.5)*2)/51 — (rand-0.5)*2 ∈ [-1,1) vs rand(-10,11)*0.1 ∈ [-1,1]. Equivalent-ish. vy: (vy*50 - 0.25 + rand(-10,11)*0.2)/51; ours: (vy*50 - 0.25 + (rand-0.5)*4)/51 — (rand-0.5)*4 ∈ [-2,2) vs [-2,2]. Equivalent. OK.

- Proximity: rect expanded by 40+width/2... our pad = 40 + w/2, then checks |player.cx - e.cx| < pad + player.w/2 — that's 40 + w/2 + pw/2 vs original rect grows X by 40+width/2 on left and width += 80+width... let me compute: rect.X -= 40 + width/2; rect.Width += 80 + width... wait: `rect.Width += num1075 * 2` = 80 only. Hmm: rect.X -= num1075 + width/2 (=40 + w/2), rect.Y -= 40 + h/2, rect.Width += 80, rect.Height += 80. So expanded rect = x from (x - 40 - w/2), width w + 80 → right edge at x + w + 40 + w/2... wait: original rect x = position.X, width = width. New: X' = X - 40 - w/2, W' = w + 80. Right edge = X - 40 - w/2 + w + 80 = X + w/2 + 40. So horizontally, rect spans center ± (w/2 + 40). Vertically: Y' = Y - 40 - h/2, H' = h + 80 → bottom = Y + h/2 + 40. So vertical also ±(h/2+40). Our check: |player.cx - e.cx| < pad + player.w/2 with pad = 40 + w/2 — that's ±(w/2 + 40 + pw/2), matching rect-vs-rect intersection (|dcx| < (w+pw)/2 + 40). Good.

- ai0==1: position = Center; width=height=100; reposition center. Ours: e.x = e.cx - 50 etc. Good. dontTakeDamage on justHit||ai0==1: ours sets iframes=2 only in ai0==1 branch (and justHit triggers ai0=1). Reasonable.

- Timeout: ai1 >= 150 → ai0=1, ai1=4. Good.

- Original has no e.ai1-- before position reset... The explosion shrinks: ai1-- each tick, when <= 0 → deactivate. Ours: ai1 -=1, if <= 0 dead. Good.

One deviation: ours sets `if (e.ai0 === 0 && player)` for proximity only when player exists — fine.

The bubble init in ours is gated on `e.ai3 <= 0` rather than target==255 — a redesign but equivalent given bInit handling. Also spawnAlpha=50. OK.

Sharkron 372/373 (aiStyle 71) vs ours:

- `noTileCollide = true` for both phases. Ours moves freely; presumably enemy collision ignores tiles by default in this project? Actually Enemy update may do tile collision. Not verifiable here; skip.

- target dead → TargetClosest(faceTarget:false), direction=1. Ours: `if (!player || player.dead) { e.dead = true; return; }` — deviation! Original re-targets to another player (single player → target stays dead player? TargetClosest picks nearest active player; if player dead... hmm TargetClosest won't pick dead players. With all players dead, target==255, then `Main.player[target]` would crash? Actually target stays 255... but this is single player: if the player is dead, TargetClosest(false) → target = 255? Then the ai[0]==0 branch does `velocity.Y = ai[3]` etc. and at num1077 expiry: `TargetClosest(); ... Main.player[target].Center` — with target 255 this would be player 0 anyway. Hmm, our project's "player dead → shark dies" is a simplification for multiplayer semantics. In single player when player is dead... sharks persist and fly at player corpse position (players remain at position when dead in Terraria). Ours kills them. Minor deviation; multiplayer semantics. Note as low.

- ai[0]==0: ai[1]++; noGravity; dontTakeDamage; velocity.Y = ai[3]; type==373 horizontal wiggle using localAI[1] (NOT ai[1]!). Ours uses `e.ai1 - 1` and `e.ai1` as the phase — since ai1 increments 1/t from 0, ai1 ≈ localAI[1]+1. Original: localAI[1] starts 0; computes num1080 with localAI[1], position.X -= num1080 * (-direction); localAI[1]++; then computes with new localAI[1], position.X += num1080 * (-direction). So net displacement = f(l1+1) - f(l1) times (-direction)... wait: position.X -= f(l1)*(-direction) then += f(l1+1)*(-direction) → net = (f(l1+1) - f(l1)) * (-direction). Ours: `e.x += (cur - prev) * -e.facing;` with prev = f(e.ai1 - 1), cur = f(e.ai1), where ai1 has already been incremented? Let me re-check order in ours:

```
if (e.ai0 === 0) {
  e.iframes = 2;
  e.vx = 0;
  e.vy = e.ai3;
  if 373: spawnAlpha..., spin...
  e.ai1 += 1;
  if (e.ai1 >= RISE_T) {...}
}
...
// 373 horizontal swim
if (e.ai0 === 0 && e.vanillaId === 373 && e.ai2 > 0) {
  const f = ...
  const prev = f(e.ai1 - 1), cur = f(e.ai1);
  e.x += (cur - prev) * -e.facing;
}
```

ai1 incremented at the top, so after first tick ai1=1, prev=f(0), cur=f(1) → displacement (f(1)-f(0))·(-facing). Original first tick: localAI[1]=0 → displacement (f(1)-f(0))·(-direction). Matches. Also velocity.Y = ai[3] is set... note in original this branch runs and does NOT add velocity to position here — position updated by the main NPC update (velocity applied). But wait, in the original, the wiggle code directly manipulates position.X, and then the main NPC movement applies velocity on top. Our x += vx (0) + wiggle. Good.

But direction: original sets direction=1 when target invalid; spriteDirection flips during wiggle based on cos. And `rotation = velocity.Y * spriteDirection * 0.1` clamped ±0.2. Ours: `e.spin = clamp(e.vy * -e.facing * 0.1, -0.2, 0.2);` — uses -e.facing as spriteDirection. Hmm, ours uses `e.vy * -e.facing`. Is our facing = spriteDirection or direction? In our code `e.facing` — in sharkronAI ai0==1 branch we set `e.facing = dx < 0 ? -1 : 1` and spin = atan2 + (facing<0 ? π) — so facing maps to direction (spriteDirection = direction when charging; rotation += π when direction==-1... wait original: `spriteDirection = direction; velocity = ...; rotation = velocity.ToRotation(); if (direction == -1) rotation += π`. So facing ≈ direction. In ai0==0 with 373, rotation = velocity.Y * spriteDirection * 0.1. spriteDirection here is the wiggle-driven spriteDirection (default -direction initially? at spawn direction=1 only when target invalid...). Ours uses -e.facing. Since default facing=1 presumably, -1 vs 1 sign difference. Negligible visual.

- At rise completion: ai1 = 0 unless in solid (then 1). Wait, original: ai[1] = 0; if NOT SolidCollision → ai[1] = 1. Ours: `e.ai1 = inSolid(game, e) ? 0 : 1;` — matches (in solid → 0, else 1).

- PlaySound(4, ..., 19) at rise completion — ours doesn't play. Minor (missing sound).

- ai0==1: original checks SolidCollision → if NOT solid and ai1<1 → ai1=1; else (in solid) alpha -= 15 clamp to min 150 (i.e. alpha floor is 150 → wait `alpha -= 15; if (alpha < 150) alpha = 150;` — that's weird: -=15 then floor at 150? If alpha < 150 set to 150 — so being in solid forces alpha UP to 150?? Wait alpha semantics: 0=visible, 255=invisible. alpha -= 15 makes MORE visible... then `if (alpha < 150) alpha = 150;` clamps to at least 150 (semi-transparent). Hmm so when in solid, alpha → 150 (partially transparent). Ours: `if (inSolid(game, e)) e.spawnAlpha = Math.min(150, e.spawnAlpha + 15);` — alpha +15 clamped at max 150. Hmm: original `alpha -= 15` then clamp to >= 150. If alpha was 255 → 240, clamp 240? no, 240 > 150 stays 240. So alpha decreases toward 150 but never below while in solid. Ours: alpha increases toward 150 max. Confusing but roughly "alpha sits at 150 in solid". Ours approaches 150 from below (from 0). Minor.

- ai1>=1: alpha -= 60 (fade in visible), ai1++, if SolidCollision → die. Ours matches (checks inSolid AFTER increment). Wait ours:

```
if (e.ai1 >= 1) {
  e.spawnAlpha = Math.max(0, e.spawnAlpha - 60);
  e.ai1 += 1;
  if (inSolid(game, e)) { e.dead = true; return; }
}
if (e.ai1 >= 60) e.vy = Math.min(e.vy + 0.3, 16);
```

Original: `if (this.ai[1] >= 60f) noGravity = false;` — gravity restored at ai1>=60. Ours adds vy 0.3 capped 16 — an approximation of gravity restore (noGravity=false → gravity applies in main update). OK.

- Note: original death on collision also plays DeathSound. Ours silent. Minor.

Now, the tornado bolt (Projectile 385 aiStyle 65 @28402-28482) and tornado 384/386 (aiStyle 64 @28287-28398). Let me read those from Projectile.cs. The task says NPC.cs is the reference for NPC AI, but projectiles are in Projectile.cs. The user's priority list mentions them. Let me read Projectile.cs 28287-28482.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:20.615Z · glm-x-preview-260804

```
现在我来处理原版 Projectile.cs 中的龙卷风弹幕族群 (385/384/386)。
```


---

## 🤖 Assistant · 2026-08-19T03:12:21.209Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '28287,28482p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs",
 "description": "Read Projectile.cs aiStyle 64/65 tornado family"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:21.259Z

**📎 ToolResult**

```
		else if (aiStyle == 64)
		{
			int num538 = 10;
			int num539 = 15;
			float num540 = 1f;
			int num541 = 150;
			int num542 = 42;
			if (type == 386)
			{
				num538 = 16;
				num539 = 16;
				num540 = 1.5f;
			}
			if (velocity.X != 0f)
			{
				direction = (spriteDirection = -Math.Sign(velocity.X));
			}
			frameCounter++;
			if (frameCounter > 2)
			{
				frame++;
				frameCounter = 0;
			}
			if (frame >= 6)
			{
				frame = 0;
			}
			if (localAI[0] == 0f && Main.myPlayer == owner)
			{
				localAI[0] = 1f;
				base.position.X += width / 2;
				base.position.Y += height / 2;
				scale = ((float)(num538 + num539) - this.ai[1]) * num540 / (float)(num539 + num538);
				width = (int)((float)num541 * scale);
				height = (int)((float)num542 * scale);
				base.position.X -= width / 2;
				base.position.Y -= height / 2;
				netUpdate = true;
			}
			if (this.ai[1] != -1f)
			{
				scale = ((float)(num538 + num539) - this.ai[1]) * num540 / (float)(num539 + num538);
				width = (int)((float)num541 * scale);
				height = (int)((float)num542 * scale);
			}
			if (!Collision.SolidCollision(base.position, width, height))
			{
				alpha -= 30;
				if (alpha < 60)
				{
					alpha = 60;
				}
				if (type == 386 && alpha < 100)
				{
					alpha = 100;
				}
			}
			else
			{
				alpha += 30;
				if (alpha > 150)
				{
					alpha = 150;
				}
			}
			if (this.ai[0] > 0f)
			{
				this.ai[0]--;
			}
			if (this.ai[0] == 1f && this.ai[1] > 0f && owner == Main.myPlayer)
			{
				netUpdate = true;
				Vector2 center4 = base.Center;
				center4.Y -= (float)num542 * scale / 2f;
				float num543 = ((float)(num538 + num539) - this.ai[1] + 1f) * num540 / (float)(num539 + num538);
				center4.Y -= (float)num542 * num543 / 2f;
				center4.Y += 2f;
				NewProjectile(GetProjectileSource_FromThis(), center4.X, center4.Y, velocity.X, velocity.Y, type, damage, knockBack, owner, 10f, this.ai[1] - 1f);
				int num544 = 4;
				if (type == 386)
				{
					num544 = 2;
				}
				if ((int)this.ai[1] % num544 == 0 && this.ai[1] != 0f)
				{
					int num545 = 372;
					if (type == 386)
					{
						num545 = 373;
					}
					int num546 = NPC.NewNPC(GetNPCSource_FromThis(), (int)center4.X, (int)center4.Y, num545);
					Main.npc[num546].velocity = velocity;
					Main.npc[num546].netUpdate = true;
					if (type == 386)
					{
						Main.npc[num546].ai[2] = width;
						Main.npc[num546].ai[3] = -1.5f;
					}
				}
			}
			if (this.ai[0] <= 0f)
			{
				float num547 = MathF.PI / 30f;
				float num548 = (float)width / 5f;
				if (type == 386)
				{
					num548 *= 2f;
				}
				float num549 = (float)(Math.Cos(num547 * (0f - this.ai[0])) - 0.5) * num548;
				base.position.X -= num549 * (float)(-direction);
				this.ai[0]--;
				num549 = (float)(Math.Cos(num547 * (0f - this.ai[0])) - 0.5) * num548;
				base.position.X += num549 * (float)(-direction);
			}
		}
		else if (aiStyle == 65)
		{
			if (this.ai[1] > 0f)
			{
				int num550 = (int)this.ai[1] - 1;
				if (num550 < 255)
				{
					localAI[0]++;
					if (localAI[0] > 10f)
					{
						int num551 = 6;
						for (int num552 = 0; num552 < num551; num552++)
						{
							Vector2 spinningpoint = Vector2.Normalize(velocity) * new Vector2((float)width / 2f, height) * 0.75f;
							spinningpoint = spinningpoint.RotatedBy((double)(num552 - (num551 / 2 - 1)) * Math.PI / (double)num551) + base.Center;
							Vector2 vector39 = ((float)(Main.rand.NextDouble() * 3.1415927410125732) - MathF.PI / 2f).ToRotationVector2() * Main.rand.Next(3, 8);
							int num553 = Dust.NewDust(spinningpoint + vector39, 0, 0, 172, vector39.X * 2f, vector39.Y * 2f, 100, default(Color), 1.4f);
							Main.dust[num553].noGravity = true;
							Main.dust[num553].noLight = true;
							Dust dust2 = Main.dust[num553];
							dust2.velocity /= 4f;
							dust2 = Main.dust[num553];
							dust2.velocity -= velocity;
						}
						alpha -= 5;
						if (alpha < 100)
						{
							alpha = 100;
						}
						rotation += velocity.X * 0.1f;
						frame = (int)(localAI[0] / 3f) % 3;
					}
					Vector2 value5 = Main.player[num550].Center - base.Center;
					float num554 = 4f;
					if (this.ai[2] == 1f)
					{
						num554 += 12f;
					}
					num554 += localAI[0] / 20f;
					velocity = Vector2.Normalize(value5) * num554;
					if (value5.Length() < 50f)
					{
						Kill();
					}
				}
			}
			else
			{
				float num555 = MathF.PI / 15f;
				float num556 = 4f;
				float num557 = (float)(Math.Cos(num555 * this.ai[0]) - 0.5) * num556;
				velocity.Y -= num557;
				this.ai[0]++;
				num557 = (float)(Math.Cos(num555 * this.ai[0]) - 0.5) * num556;
				velocity.Y += num557;
				localAI[0]++;
				if (localAI[0] > 10f)
				{
					alpha -= 5;
					if (alpha < 100)
					{
						alpha = 100;
					}
					rotation += velocity.X * 0.1f;
					frame = (int)(localAI[0] / 3f) % 3;
				}
			}
			if (wet)
			{
				base.position.Y -= 16f;
				Kill();
			}
		}
		else if (aiStyle == 66)
		{
			float num558 = 0f;
			float num559 = 0f;
			float num560 = 0f;
			float num561 = 0f;
			bool flag31 = type == 387 || type == 388;
			if (flag31)

```


---

## 🤖 Assistant · 2026-08-19T03:12:49.834Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Tornado (aiStyle 64) details vs ours:

- num538=10, num539=15 for 384; for 386: num538=16, num539=16, num540=1.5.
- scale = ((num538+num539) - ai[1]) * num540 / (num539+num538). For 384: (25 - ai1)/25. For 386: (32 - ai1)*1.5/32. Ours: `scaleOf` matches.
- Initial ai0: NewProjectile from Duke's 385 Kill passes ai0... wait — our DukeSharknadoTornado constructor sets ai0=16 for both. Original: 385 Kill spawns the 384/386 with what ai0? Let me check Kill at :70714-70778. I'll read that next.
- timeLeft: need to check SetDefaults for 384/386: small 540, big 840. Can't verify without SetDefaults; skip.
- Segment growth: when ai0==1 && ai1>0: NewProjectile(same type, ai0=10, ai1=ai1-1) at center4 which is Center shifted up. Ours simulates a single entity tower. OK as designed (documented deviation).
- Shark spawn condition: (int)ai[1] % num544 == 0 && ai[1] != 0, num544=4 (384) / 2 (386). Ours: mod 4 / 2 — good. NPC velocity = velocity (tornado's velocity, which is 0 for the initial... actually segments are spawned with velocity of parent which is whatever; typically 0). Ours passes this.vx/this.vy (0). Fine.
- 386: npc ai[2]=width, ai[3]=-1.5. Ours matches.
- Sway after ai0<=0: num548 = width/5, ×2 for 386; position.X -= f(-ai0)*(-direction); ai0--; position.X += f(-ai0)*(-direction). Net displacement = (f(-(ai0-1)) - f(-ai0)) * (-direction). Ours:
```
const amp = (this.w / 5) * (this.big ? 2 : 1);
const f = (t) => (Math.cos((Math.PI / 30) * t) - 0.5) * amp;
this.x -= f(-this.ai0) * -1;
this.ai0 -= 1;
this.x += f(-this.ai0) * -1;
```
Ours: x -= f(-ai0)·(−1); ai0 -= 1; x += f(-ai0)·(−1). Net = (f(-(ai0-1)) − f(-ai0))·(−1)... wait: x_net = -f(-a0) + f(-(a0-1)) times (-1)^... let me be careful: `this.x -= f(-this.ai0) * -1` means x = x + f(-ai0). Then ai0--. `this.x += f(-this.ai0) * -1` means x = x - f(-ai0_new) = x - f(-(a0-1)). Net = f(-a0) - f(-(a0-1)) = -( f(-(a0-1)) - f(-a0) ).

Original: position.X -= num549 * (-direction) → x = x + num549·direction. ai0--. x += num549_new * (-direction) → x = x - num549_new·direction. Net = (f(-a0) - f(-(a0-1)))·direction.

So ours = original with direction=1. And direction here: `if (velocity.X != 0) direction = spriteDirection = -Sign(velocity.X)`. Tornado's velocity is ~0 → direction unchanged (default 1). OK, equivalent when velocity 0. Note ours doesn't track direction — but velocity ≈ 0 anyway. Fine.

Also alpha: ours in solid: alpha = min(150, alpha+30); else alpha = max(big?100:60, alpha-30). Original: not solid: alpha -= 30, floor 60; if 386 && alpha < 100 → alpha = 100. In solid: alpha += 30, cap 150. Matches (including the 386 alpha floor of 100 via max).

Hmm wait, original applies the alpha logic using SolidCollision(position, width, height) — the full rect, ours uses center point. Approximation, documented.

Bolt 385 (aiStyle 65):
- ai[1] > 0 (big/homing): num550 = ai[1]-1 = player index (target+1). localAI[0]++ ... velocity = Normalize(playerCenter - center) * (4 + (ai2==1 ? 12 : 0) + localAI[0]/20); if dist < 50 → Kill. Ours: spd = 4 + enraged?12 + age/20 — but note: `this.age++` happens AFTER... ours increments age at top (this.age++ after life check). localAI[0] starts 0, incremented each tick; first tick velocity uses localAI[0]=1? Actually original: localAI[0]++ then velocity uses localAI[0]/20 → first tick 1/20. Ours: `this.age++` at top → first tick age=1 → 1/20. Match.
- Small (ai1==0): vy oscillation: num557 = (cos(π/15 · ai0) - 0.5)*4; velocity.Y -= num557; ai0++; num557 = (cos(π/15·ai0)-0.5)*4; velocity.Y += num557. Net: vy += f(ai0+1) - f(ai0). Ours: f(t) = (cos(π/15 t) - 0.5)*4; d0 = f(phase); phase++; vy0 += f(phase) - d0. Match.
- wet → y -= 16, Kill. Ours: liquid check → y -= 16, kill. Good.
- But: small bolt Kill on solid tile collision? Original aiStyle 65 has no tile collision Kill unless... projectile has tileCollide? 385 SetDefaults — need to check. The AI doesn't Kill on solid. Ours kills on solid: `if (st.isSolid(tx, ty)) { this.kill(game); return; }`. Is that in the original? Projectile 385 — need SetDefaults to see tileCollide. Let me check Kill at 70714-70778 which handles tornado spawn. In vanilla, the 385 projectile: I recall it falls and explodes on hitting tiles (Kill is triggered by tile collision through projectile's generic tile collision → Kill()). Yes, standard tile collision kills it. OK ours matches.

Big bolt homing: original tracks the player from `Main.player[num550]` — always tracks, even if player dead? player dead → still targets. Ours: `if (p && !p.dead)`. Minor.

Now the Kill at 70714-70778. Let me read.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:50.241Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '70714,70780p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs",
 "description": "Read Projectile.cs Kill for 385"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:50.296Z

**📎 ToolResult**

```
		if (type == 385)
		{
			SoundEngine.PlaySound(4, (int)base.Center.X, (int)base.Center.Y, 19);
			int num447 = 36;
			for (int num448 = 0; num448 < num447; num448++)
			{
				Vector2 spinningpoint = Vector2.Normalize(velocity) * new Vector2((float)width / 2f, height) * 0.75f;
				spinningpoint = spinningpoint.RotatedBy((float)(num448 - (num447 / 2 - 1)) * (MathF.PI * 2f) / (float)num447) + base.Center;
				Vector2 vector50 = spinningpoint - base.Center;
				int num449 = Dust.NewDust(spinningpoint + vector50, 0, 0, 172, vector50.X * 2f, vector50.Y * 2f, 100, default(Color), 1.4f);
				Main.dust[num449].noGravity = true;
				Main.dust[num449].noLight = true;
				Main.dust[num449].velocity = vector50;
			}
			if (owner == Main.myPlayer)
			{
				if (ai[1] < 1f)
				{
					int num450 = (Main.expertMode ? 25 : 40);
					int num451 = NewProjectile(GetProjectileSource_FromThis(), base.Center.X - (float)(direction * 30), base.Center.Y - 4f, (float)(-direction) * 0.01f, 0f, 384, num450, 4f, owner, 16f, 15f);
					Main.projectile[num451].netUpdate = true;
				}
				else
				{
					int num452 = (int)(base.Center.Y / 16f);
					int num453 = (int)(base.Center.X / 16f);
					int num454 = 100;
					if (num453 < 10)
					{
						num453 = 10;
					}
					if (num453 > Main.maxTilesX - 10)
					{
						num453 = Main.maxTilesX - 10;
					}
					if (num452 < 10)
					{
						num452 = 10;
					}
					if (num452 > Main.maxTilesY - num454 - 10)
					{
						num452 = Main.maxTilesY - num454 - 10;
					}
					int num455 = num452 + num454;
					int num456 = num452 + 15;
					for (int num457 = num452; num457 < num455; num457++)
					{
						Tile tile2 = Main.tile[num453, num457];
						if (tile2.active() && (Main.tileSolid[tile2.type] || tile2.liquid != 0))
						{
							num456 = num457;
							break;
						}
					}
					num452 = num456;
					int num458 = (Main.expertMode ? 50 : 80);
					int num459 = NewProjectile(GetProjectileSource_FromThis(), num453 * 16 + 8, num452 * 16 - 24, 0f, 0f, 386, num458, 4f, Main.myPlayer, 16f, 24f);
					Main.projectile[num459].netUpdate = true;
				}
			}
		}
		else if (type >= 424 && type <= 426)
		{
			SoundEngine.PlaySound(SoundID.Item89, position);
			position.X += width / 2;
			position.Y += height / 2;
			width = (int)(128f * scale);

```


---

## 🤖 Assistant · 2026-08-19T03:13:08.333Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Kill for 385: our implementation matches closely (small: center - direction*30, y-4 → 384, ai0=16, ai1=15; big: scan down from tile pos, ground default = num452+15 = ty+15; ours `let ground = ty + 15` — matches; spawns at tx*16+8, ty*16-24 → ours `tx*TILE+8, ground*TILE-24` — matches).

Damage: small 40 (classic) / big 80 (classic) — ours uses 40/80 contact via the doubled hostile rule... wait. Original NewProjectile damage for 384 = 40 classic; 386 = 80 classic. Projectile damage is applied when the projectile hits (hostile → damage ×2? no!). Hmm — the hostile ×2 rule: in Terraria, hostile projectile damage is doubled in... Actually Projectile damage for hostile projectiles: `Main.CalculateDamage`... The known mechanic: NPC projectile damage is doubled for players? Yes — "Projectile damage is doubled when hostile" (in Player.HitInfo, damage = proj.damage * 2 for hostile projectiles). Our code comments say so (:13781). OK, that's their established convention from previous audits. Their tornado contact damage: `game.damagePlayer(this.big ? 160 : 80, ...)` = 80×2 / 40×2. OK consistent with their claimed rule.

Now — small nado spawn offset: original `base.Center.X - direction*30` where direction of the 385 projectile (spriteDirection = -Sign(velocity.X)). Ours: `const dir = Math.sign(this.vx0) || 1; addProj(new DukeSharknadoTornado(this.cx - dir * 30, ...))`. Original uses `direction` (not spriteDirection): direction = -Sign(velocity.X) when velocity.X != 0. So original offset = Center.X - direction*30 = Center.X + Sign(vx)*30. Ours: cx - Sign(vx)*30 — SIGN FLIPPED!

Wait let me recheck: `if (velocity.X != 0f) { direction = spriteDirection = -Math.Sign(velocity.X); }` — that's in aiStyle 64, not 65. For 385 (aiStyle 65), direction is the default projectile direction which starts as Sign(velocity.X)? Projectile.direction default: set in NewProjectile → direction = Sign(speedX) if speedX != 0. Actually Projectile.NewProjectile sets `direction = ((speedX > 0) ? 1 : (-1))` roughly... Let me not guess. The small bolt is spawned with vx = direction*2 (from Duke) or -direction*2. The 385 projectile has its own direction = sign of its velocity X presumably. In Kill, `base.Center.X - (float)(direction * 30)`. If direction = Sign(vx), offset = cx - Sign(vx)*30 — ours: `cx - dir*30` with dir = Sign(vx0). That matches IF projectile.direction = Sign(velocity.X).

Projectile.NewProjectile: `num4.direction = ((num4.velocity.X < 0f) ? (-1) : 1);`? There's something in SetDefaults/NewProjectile. Default direction for projectiles: In Projectile.NewProjectile, `projectile.direction = 1` unless velocity.X negative? Hmm. I recall `direction` defaults to 1 and is updated in AI by projectile code. For 385, aiStyle 65 doesn't touch direction. NewProjectile code: let me check quickly to be safe.

Actually this is a 30px offset detail — visual spawn position of the tornado. Low importance either way. Skip.

Now the Moon Lord. Let me read 36774-37198 (core).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:08.692Z · glm-x-preview-260804

```
现在我来读取 NPC.cs 中的 Moon Lord 核心 aiStyle 77。
```


---

## 🤖 Assistant · 2026-08-19T03:13:09.134Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '36774,36930p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Moon Lord core part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:09.196Z

**📎 ToolResult**

```
		else if (aiStyle == 77)
		{
			if (this.ai[0] != -1f && this.ai[0] != 2f && Main.rand.Next(200) == 0)
			{
				SoundEngine.PlaySound(29, (int)base.Center.X, (int)base.Center.Y, Main.rand.Next(93, 100));
			}
			if (localAI[3] == 0f)
			{
				netUpdate = true;
				localAI[3] = 1f;
				this.ai[0] = -1f;
			}
			if (this.ai[0] == -2f)
			{
				dontTakeDamage = true;
				this.ai[1]++;
				if (this.ai[1] == 30f)
				{
					SoundEngine.PlaySound(29, (int)base.Center.X, (int)base.Center.Y, 92);
				}
				if (this.ai[1] < 60f)
				{
					MoonlordDeathDrama.RequestLight(this.ai[1] / 30f, base.Center);
				}
				if (this.ai[1] == 60f)
				{
					this.ai[1] = 0f;
					this.ai[0] = 0f;
					if (Main.netMode != 1 && type == 398)
					{
						this.ai[2] = Main.rand.Next(3);
						this.ai[2] = 0f;
						netUpdate = true;
					}
				}
			}
			if (this.ai[0] == -1f)
			{
				dontTakeDamage = true;
				this.ai[1]++;
				if (this.ai[1] == 30f)
				{
					SoundEngine.PlaySound(29, (int)base.Center.X, (int)base.Center.Y, 92);
				}
				if (this.ai[1] < 60f)
				{
					MoonlordDeathDrama.RequestLight(this.ai[1] / 30f, base.Center);
				}
				if (this.ai[1] == 60f)
				{
					this.ai[1] = 0f;
					this.ai[0] = 0f;
					if (Main.netMode != 1 && type == 398)
					{
						this.ai[2] = Main.rand.Next(3);
						this.ai[2] = 0f;
						netUpdate = true;
						int[] array5 = new int[3];
						int num1208 = 0;
						for (int num1209 = 0; num1209 < 2; num1209++)
						{
							int num1210 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X + num1209 * 800 - 400, (int)base.Center.Y - 100, 397, whoAmI);
							Main.npc[num1210].ai[2] = num1209;
							Main.npc[num1210].netUpdate = true;
							array5[num1208++] = num1210;
						}
						int num1211 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X, (int)base.Center.Y - 400, 396, whoAmI);
						Main.npc[num1211].netUpdate = true;
						array5[num1208++] = num1211;
						for (int num1212 = 0; num1212 < 3; num1212++)
						{
							Main.npc[array5[num1212]].ai[3] = whoAmI;
						}
						for (int num1213 = 0; num1213 < 3; num1213++)
						{
							localAI[num1213] = array5[num1213];
						}
					}
				}
			}
			if (this.ai[0] == 0f)
			{
				dontTakeDamage = true;
				TargetClosest(faceTarget: false);
				Vector2 vector151 = Main.player[target].Center - base.Center + new Vector2(0f, 130f);
				if (vector151.Length() > 20f)
				{
					Vector2 desiredVelocity = Vector2.Normalize(vector151 - velocity) * 8f;
					Vector2 value2 = velocity;
					SimpleFlyMovement(desiredVelocity, 0.5f);
					velocity = Vector2.Lerp(velocity, value2, 0.5f);
				}
				if (Main.netMode != 1)
				{
					bool flag84 = false;
					if (localAI[0] < 0f || localAI[1] < 0f || localAI[2] < 0f)
					{
						flag84 = true;
					}
					else if (!Main.npc[(int)localAI[0]].active || Main.npc[(int)localAI[0]].type != 397)
					{
						flag84 = true;
					}
					else if (!Main.npc[(int)localAI[1]].active || Main.npc[(int)localAI[1]].type != 397)
					{
						flag84 = true;
					}
					else if (!Main.npc[(int)localAI[2]].active || Main.npc[(int)localAI[2]].type != 396)
					{
						flag84 = true;
					}
					if (flag84)
					{
						life = 0;
						HitEffect();
						active = false;
					}
					bool flag85 = true;
					if (Main.npc[(int)localAI[0]].ai[0] != -2f)
					{
						flag85 = false;
					}
					if (Main.npc[(int)localAI[1]].ai[0] != -2f)
					{
						flag85 = false;
					}
					if (Main.npc[(int)localAI[2]].ai[0] != -2f)
					{
						flag85 = false;
					}
					if (flag85)
					{
						this.ai[0] = 1f;
						dontTakeDamage = false;
						netUpdate = true;
					}
				}
			}
			else if (this.ai[0] == 1f)
			{
				dontTakeDamage = false;
				TargetClosest(faceTarget: false);
				Vector2 vector152 = Main.player[target].Center - base.Center + new Vector2(0f, 130f);
				if (vector152.Length() > 20f)
				{
					Vector2 desiredVelocity2 = Vector2.Normalize(vector152 - velocity) * 8f;
					Vector2 value3 = velocity;
					SimpleFlyMovement(desiredVelocity2, 0.5f);
					velocity = Vector2.Lerp(velocity, value3, 0.5f);
				}
			}
			else if (this.ai[0] == 2f)
			{
				dontTakeDamage = true;
				velocity = Vector2.Lerp(value2: new Vector2(0f, -0.5f), value1: velocity, amount: 0.98f);
				this.ai[1]++;
				if (this.ai[1] < 60f)

```


---

## 🤖 Assistant · 2026-08-19T03:13:32.899Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key structural points so far:

1. State 0 core: `dontTakeDamage = true`; checks parts exist via localAI[0..2] (whoAmI indices) — if any part inactive/wrong type → core dies. Ours: `parts.length < 3 → dead`. Equivalent-ish. Note: ours filters by `n.ai3 === e.id`, and parts are spawned with ai3 = core id. OK.

2. flag85: all three parts ai0 == -2 → core ai0 = 1. Ours matches.

3. Note the core in state 1: NO attacks from core — matches ours (attack only if no true eyes exist, fallback).

4. In state 1 the core itself hovers.

Important: state 2 death drama; state 3; the teleport; the despawn-when-no-players. Let me continue reading 36930-37198.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:32.986Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '36930,37198p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Moon Lord core part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:33.068Z

**📎 ToolResult**

```
				if (this.ai[1] < 60f)
				{
					MoonlordDeathDrama.RequestLight(this.ai[1] / 60f, base.Center);
				}
				if (this.ai[1] == 60f)
				{
					for (int num1214 = 0; num1214 < 1000; num1214++)
					{
						Projectile projectile = Main.projectile[num1214];
						if (projectile.active && (projectile.type == 456 || projectile.type == 462 || projectile.type == 455 || projectile.type == 452 || projectile.type == 454))
						{
							projectile.Kill();
						}
					}
					for (int num1215 = 0; num1215 < Main.maxNPCs; num1215++)
					{
						NPC nPC7 = Main.npc[num1215];
						if (nPC7.active && nPC7.type == 400)
						{
							nPC7.HitEffect(0, 9999.0);
							nPC7.active = false;
						}
					}
				}
				if (this.ai[1] % 3f == 0f && this.ai[1] < 580f && this.ai[1] > 60f)
				{
					Vector2 vector153 = Utils.RandomVector2(Main.rand, -1f, 1f);
					if (vector153 != Vector2.Zero)
					{
						vector153.Normalize();
					}
					vector153 *= 20f + Main.rand.NextFloat() * 400f;
					bool flag86 = true;
					Vector2 vector154 = base.Center + vector153;
					Point point5 = vector154.ToTileCoordinates();
					if (!WorldGen.InWorld(point5.X, point5.Y))
					{
						flag86 = false;
					}
					if (flag86 && WorldGen.SolidTile(point5.X, point5.Y))
					{
						flag86 = false;
					}
					float num1216 = Main.rand.Next(6, 19);
					float num1217 = MathF.PI * 2f / num1216;
					float num1218 = MathF.PI * 2f * Main.rand.NextFloat();
					float num1219 = 1f + Main.rand.NextFloat() * 2f;
					float num1220 = 1f + Main.rand.NextFloat();
					float fadeIn = 0.4f + Main.rand.NextFloat();
					int num1221 = Utils.SelectRandom<int>(Main.rand, 31, 229);
					if (flag86 && !Main.dedServ)
					{
						MoonlordDeathDrama.AddExplosion(vector154);
						for (float num1222 = 0f; num1222 < num1216 * 2f; num1222++)
						{
							Dust dust8 = Main.dust[Dust.NewDust(vector154, 0, 0, 229)];
							dust8.noGravity = true;
							dust8.position = vector154;
							dust8.velocity = Vector2.UnitY.RotatedBy(num1218 + num1217 * num1222) * num1219 * (Main.rand.NextFloat() * 1.6f + 1.6f);
							dust8.fadeIn = fadeIn;
							dust8.scale = num1220;
						}
					}
					for (float num1223 = 0f; num1223 < this.ai[1] / 60f; num1223++)
					{
						Vector2 vector155 = Utils.RandomVector2(Main.rand, -1f, 1f);
						if (vector155 != Vector2.Zero)
						{
							vector155.Normalize();
						}
						vector155 *= 20f + Main.rand.NextFloat() * 800f;
						Vector2 vec2 = base.Center + vector155;
						Point point6 = vec2.ToTileCoordinates();
						bool flag87 = true;
						if (!WorldGen.InWorld(point6.X, point6.Y))
						{
							flag87 = false;
						}
						if (flag87 && WorldGen.SolidTile(point6.X, point6.Y))
						{
							flag87 = false;
						}
						if (flag87)
						{
							Dust dust9 = Main.dust[Dust.NewDust(vec2, 0, 0, num1221)];
							dust9.noGravity = true;
							dust9.position = vec2;
							dust9.velocity = -Vector2.UnitY * num1219 * (Main.rand.NextFloat() * 0.9f + 1.6f);
							dust9.fadeIn = fadeIn;
							dust9.scale = num1220;
						}
					}
				}
				if (this.ai[1] % 15f == 0f && this.ai[1] < 480f && this.ai[1] >= 90f && Main.netMode != 1)
				{
					Vector2 vector156 = Utils.RandomVector2(Main.rand, -1f, 1f);
					if (vector156 != Vector2.Zero)
					{
						vector156.Normalize();
					}
					vector156 *= 20f + Main.rand.NextFloat() * 400f;
					bool flag88 = true;
					Vector2 vec3 = base.Center + vector156;
					Point point7 = vec3.ToTileCoordinates();
					if (!WorldGen.InWorld(point7.X, point7.Y))
					{
						flag88 = false;
					}
					if (flag88 && WorldGen.SolidTile(point7.X, point7.Y))
					{
						flag88 = false;
					}
					if (flag88)
					{
						float num1224 = (float)(Main.rand.Next(4) < 2).ToDirectionInt() * (MathF.PI / 8f + MathF.PI / 4f * Main.rand.NextFloat());
						Vector2 vector157 = new Vector2(0f, (0f - Main.rand.NextFloat()) * 0.5f - 0.5f).RotatedBy(num1224) * 6f;
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vec3.X, vec3.Y, vector157.X, vector157.Y, 622, 0, 0f, Main.myPlayer);
					}
				}
				if (this.ai[1] == 1f)
				{
					SoundEngine.PlaySound(SoundID.NPCDeath61, base.Center);
				}
				if (this.ai[1] >= 480f)
				{
					MoonlordDeathDrama.RequestLight((this.ai[1] - 480f) / 120f, base.Center);
				}
				if (this.ai[1] >= 600f)
				{
					life = 0;
					HitEffect(0, 1337.0);
					checkDead();
					return;
				}
			}
			else if (this.ai[0] == 3f)
			{
				dontTakeDamage = true;
				velocity = Vector2.Lerp(value2: new Vector2(direction, -0.5f), value1: velocity, amount: 0.98f);
				this.ai[1]++;
				if (this.ai[1] < 60f)
				{
					MoonlordDeathDrama.RequestLight(this.ai[1] / 40f, base.Center);
				}
				if (this.ai[1] == 40f)
				{
					for (int num1225 = 0; num1225 < 1000; num1225++)
					{
						Projectile projectile2 = Main.projectile[num1225];
						if (projectile2.active && (projectile2.type == 456 || projectile2.type == 462 || projectile2.type == 455 || projectile2.type == 452 || projectile2.type == 454))
						{
							projectile2.active = false;
							if (Main.netMode != 1)
							{
								NetMessage.SendData(27, -1, -1, null, num1225);
							}
						}
					}
					for (int num1226 = 0; num1226 < Main.maxNPCs; num1226++)
					{
						NPC nPC8 = Main.npc[num1226];
						if (nPC8.active && nPC8.type == 400)
						{
							nPC8.active = false;
							if (Main.netMode != 1)
							{
								NetMessage.SendData(23, -1, -1, null, nPC8.whoAmI);
							}
						}
					}
					for (int num1227 = 0; num1227 < 600; num1227++)
					{
						Gore gore2 = Main.gore[num1227];
						if (gore2.active && gore2.type >= 619 && gore2.type <= 622)
						{
							gore2.active = false;
						}
					}
				}
				if (this.ai[1] >= 60f)
				{
					for (int num1228 = 0; num1228 < Main.maxNPCs; num1228++)
					{
						NPC nPC9 = Main.npc[num1228];
						if (nPC9.active && (nPC9.type == 400 || nPC9.type == 397 || nPC9.type == 396))
						{
							nPC9.active = false;
							if (Main.netMode != 1)
							{
								NetMessage.SendData(23, -1, -1, null, nPC9.whoAmI);
							}
						}
					}
					active = false;
					if (Main.netMode != 1)
					{
						NetMessage.SendData(23, -1, -1, null, whoAmI);
					}
					LunarApocalypseIsUp = false;
					if (Main.netMode == 2)
					{
						NetMessage.SendData(7);
					}
					return;
				}
			}
			bool flag89 = false;
			if (this.ai[0] == -2f || this.ai[0] == -1f || this.ai[0] == 2f || this.ai[0] == 3f)
			{
				flag89 = true;
			}
			if (Main.player[target].active && !Main.player[target].dead)
			{
				flag89 = true;
			}
			if (!flag89)
			{
				for (int num1229 = 0; num1229 < 255; num1229++)
				{
					if (Main.player[num1229].active && !Main.player[num1229].dead)
					{
						flag89 = true;
						break;
					}
				}
			}
			if (!flag89)
			{
				this.ai[0] = 3f;
				this.ai[1] = 0f;
				netUpdate = true;
			}
			if (!(this.ai[0] >= 0f) || !(this.ai[0] < 2f) || Main.netMode == 1 || !(Distance(Main.player[target].Center) > 2400f))
			{
				return;
			}
			this.ai[0] = -2f;
			netUpdate = true;
			Vector2 vector158 = Main.player[target].Center - Vector2.UnitY * 150f - base.Center;
			position += vector158;
			if (Main.npc[(int)localAI[0]].active)
			{
				NPC nPC3 = Main.npc[(int)localAI[0]];
				nPC3.position += vector158;
				Main.npc[(int)localAI[0]].netUpdate = true;
			}
			if (Main.npc[(int)localAI[1]].active)
			{
				NPC nPC3 = Main.npc[(int)localAI[1]];
				nPC3.position += vector158;
				Main.npc[(int)localAI[1]].netUpdate = true;
			}
			if (Main.npc[(int)localAI[2]].active)
			{
				NPC nPC3 = Main.npc[(int)localAI[2]];
				nPC3.position += vector158;
				Main.npc[(int)localAI[2]].netUpdate = true;
			}
			for (int num1230 = 0; num1230 < Main.maxNPCs; num1230++)
			{
				NPC nPC10 = Main.npc[num1230];
				if (nPC10.active && nPC10.type == 400)
				{
					NPC nPC3 = nPC10;
					nPC3.position += vector158;
					nPC10.netUpdate = true;
				}
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:14:26.723Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Core details vs ours:

1. State -2 (teleport re-entry): dontTakeDamage, ai1++, sound at ai1==30 (PlaySound(29,...,92)), light drama, at ai1==60 → ai0=0. Ours: no sound at 30. Minor.

2. State -1 (spawn): at ai1==60 spawns 2 hands at `Center.X + num1209*800 - 400, Center.Y - 100` and head at `Center.X, Center.Y - 400`. NOTE: NewNPC takes position as top-left-ish? NewNPC spawns at given position (X, Y is the NPC position top-left). Ours: `h.x = e.cx + i*800 - 400 - h.w/2; h.y = e.cy - 100 - h.h/2;` — treats as center. NewNPC's x/y are the position (top-left) directly, though NPC.NewNPC does some adjustment? NPC.NewNPC → npc.position = new Vector2(X, Y)? Actually NewNPC spawns with position set to (X, Y) — that's the top-left of the NPC box. Hmm, vanilla NewNPC: `npc.position.X = X; npc.position.Y = Y;`? I believe NewNPC sets `npc.Center`? No — NewNPC sets position directly to (X,Y) as top-left. Actually, in Terraria's NewNPC: `npc.position = new Vector2(X, Y);`? Let me not go down this hole — 397 hand is huge (probably 200+ px). The difference is a half-width offset on spawn; the hand AI clamps into its box around the core immediately anyway. Skip.

3. Sound at ai1==30 in state -1 (Zombie_92): ours plays at ai1 >= 60 transition ('Zombie_92' after spawn). Wait ours: `if (e.ai1 >= 60) { ...; game.playSfxWav?.('Zombie_92', ...) }` — plays sound at the END (ai1==60, when spawning parts). Original plays at ai1==30 (mid-drama). Timing off by 30 ticks. Minor cosmetic.

4. State 0: ours `if (parts.length < 3) { e.dead = true; return; }` — original kills core if any part inactive/wrong type. Equivalent. Original flag85: all parts ai0==-2 → core ai0=1. Ours matches.

Wait — CRITICAL: in the original state 0, `dontTakeDamage = true` but there's also a subtle thing — the core hovers via SimpleFlyMovement with velocity Lerp trick; ours mlCoreHover: flyLerp(e, ...) where the "desired" = normalize(delta - velocity)*8 — original: `vector151 = playerCenter - center + (0,130); if (vector151.Length() > 20) { desired = Normalize(vector151 - velocity) * 8; SimpleFlyMovement(desired, 0.5); velocity = Lerp(velocity, oldValue, 0.5); }`.

Ours:
```
const dx = player.cx - e.cx;
const dy = player.cy + 130 - e.cy;
if (Math.hypot(dx, dy) > 20) {
  const d = Math.hypot(dx - e.vx, dy - e.vy) || 1;
  flyLerp(e, ((dx - e.vx) / d) * 8, ((dy - e.vy) / d) * 8, 0.5);
}
```
flyLerp: vx = accelTo(vx, tx, 0.5) then lerp with old by 0.5. SimpleFlyMovement(desired, 0.5) = per-axis step toward desired by 0.5, doubling when crossing zero — accelTo presumably does that. Then velocity = Lerp(velocity, oldValue, 0.5) — ours: lerp(ox, new, 0.5) — same thing. Match.

5. State 2 (death drama): ai1==60 → kill all projectiles 456/462/455/452/454 and NPC 400s. Ours: doesn't clear true eyes at ai1==60! Ours at ai1>=600 → dead. Hmm wait, ours in ai0===2: only particles; at 600 → dead. The parts AI self-destruct when core dead (396 -3 branch? no...). Actually ours: head ai0=-3 when core.ai0===2; the head's -3 branch returns early each tick but never dies! Let me check: head -3: `if (x.f2 < 14) x.f2 += 1; e.iframes = 2; return;` — never sets dead. And hand -2: `handHover(e, core, side)` — but wait, moonLordHandAI first line: `if (!core || core.dead) { e.dead = true; return; }` — core.dead only when the 600t death completes. So during the 600t drama, hands/head (ai0=-2) persist and continue hovering. In original, hands/head/eyes persist too during death drama (they're killed... hmm, actually in vanilla when the core dies, what happens to the hands? The head goes -3 (closed forever) via its -2 branch when core ai0==2. The hands in -2 state keep hovering... Let me check the hand AI for what happens when core ai0==2. I'll read the hand section. Also the original at ai1==60 kills projectiles and NPC 400 (true eyes). Ours doesn't kill true eyes (NPC 400) during death drama — is 400 (true eye) even implemented in this project? The comment says "真眼数据/贴图缺失导致 spawn 失败时" — so spawnPart(400) may fail; but if it exists elsewhere... The core state 2 in ours doesn't clear NPC 400 or MLDeathray/MoonLeechProj entities. MLDeathray self-kills when src dead only. During 600t drama, existing deathrays would continue... but their srcs (parts) are in -2 which kills head deathray (kind head checks src.ai0 === -2 → dead). OK-ish. Missing: kill projectiles at ai1==60 — minor given entity buckets.

Hmm wait, actually there's something more important: ours plays 'Zombie_92' when spawning parts at ai1==60 of state -1; and no NPCDeath61 sound at death drama ai1==1. Minor.

6. State 3 (flee): original at ai1==40 clears projectiles and 400s; at ai1>=60 deactivates 400/397/396 and self. Ours: at ai1>=60 kills parts + self. Missing the ai1==40 cleanup — minor.

Also ours state 3: `e.vx = lerp(e.vx, e.facing, 0.02);` — original: `velocity = Vector2.Lerp(value1: velocity, value2: new Vector2(direction, -0.5f), amount: 0.98f)` — WAIT. Look carefully at the decompiled signature: `Vector2.Lerp(value2: new Vector2(0f, -0.5f), value1: velocity, amount: 0.98f)` — named arguments! value1 = velocity, value2 = (0,-0.5), amount = 0.98. So Lerp(velocity, (0,-0.5), 0.98) → velocity moves 98% toward target each tick. That's the state-2 death drama too: `velocity = Vector2.Lerp(value2: new Vector2(0f, -0.5f), value1: velocity, amount: 0.98f)`.

Ours state 2: `e.vx = lerp(e.vx, 0, 0.02); e.vy = lerp(e.vy, -0.5, 0.02);` — amount 0.02, NOT 0.98! That's a significant behavioral difference: original approaches (0,-0.5) at 98%/tick (instant), ours at 2%/tick (slow drift).

Hold on — is that right? Let me double check the decompiled named args. In C# decompiled code by dnSpy/ILSpy, `Vector2.Lerp(value1, value2, amount)`. The named-argument syntax `Vector2.Lerp(value2: X, value1: Y, amount: Z)` means value2 = (0,-0.5), value1 = velocity, amount = 0.98. So result = velocity + 0.98*((0,-0.5) - velocity) ≈ (0,-0.5) immediately.

Hmm, but semantically for a death drama, drifting slowly upward at ~-0.5 velocity... In-game, when the Moon Lord core dies, it slowly floats upward? Actually the core's death: it stays and explodes for 10 seconds. With Lerp amount 0.98 it instantly gets velocity (0,-0.5) and floats up at 0.5 px/t = 30px/s ≈ slow rise. With 0.02, velocity approaches -0.5 asymptotically (never quite reaching) — over 600 ticks: vy(t) = -0.5*(1-0.98^t). After 600 ticks 0.98^600 ≈ e^(-12) ≈ 0. So it converges almost fully after ~200 ticks; the rise distance differs: with 0.98, distance = 0.5*600 = 300px total rise. With 0.02: vy = -0.5(1-0.98^t), distance = 0.5*(600 - (1-0.98^600)/0.02) = 0.5*(600 - 50) ≈ 275px. Close-ish. Meh — actually not that different! Because velocity itself is small. Hmm. But for state 3 flee: original Lerp toward (direction, -0.5) at 0.98 → instantly vx = direction (≈ ±1) rising at -0.5 — that's the classic boss flee speed (1 px/t horizontal). Ours at 0.02: vx approaches facing slowly (takes ~50 ticks to reach 0.6). Over the 60-tick flee window, ours moves almost not at all horizontally; original moves ~60px. But since the whole thing despawns at 60 ticks anyway, the visible difference is small. Still, it's a real parameter deviation worth noting? The visible symptom: during flee the core barely drifts. Severity low. But it's a misread of the named-args Lerp — worth reporting as a CONFIRMED minor.

Actually wait — I should double-check whether our lerp direction is even right. ours: lerp(e.vx, 0, 0.02) — vx + 0.02*(0 - vx) — approaches target at 2%/tick. Original: 98%/tick. So ours is a ~50× slower convergence. For state 2 (death), the drama lasts 600 ticks and the velocity is tiny; visually near-identical. For state 3 flee (60 ticks), original core has basically velocity=(direction,-0.5) immediately; ours ramps slowly. Low severity but CONFIRMED. Both hand/head -3 branches also use 0.07 for spin lerp — let me verify those against original later.

7. The "no players" flee: original flag89 logic — ai0 in {-2,-1,2,3} OR target player active&alive OR any player active&alive. If none → ai0=3. Ours: `if (!player && e.ai0 !== -1 && e.ai0 !== -2 && e.ai0 !== 2 && e.ai0 !== 3)`. Equivalent for single player. OK.

8. Teleport: original teleports when `ai[0] >= 0 && ai[0] < 2 && Distance(player.Center) > 2400` → sets ai0=-2, moves core + parts (localAI 0-2) + all 400s by vector158 = playerCenter - UnitY*150 - center. Ours: moves core + parts with ai3===e.id (includes 396/397/400) by (dx, dy) where dy = player.cy - 150 - e.cy. Match. Ours also requires `player` non-null. OK.

But ours: `if (player && e.ai0 >= 0 && e.ai0 < 2 && ...)`. Original also requires `Main.netMode != 1`. Fine.

9. IMPORTANT — state 0 core part-death check: ours `parts.length < 3 → dead`. But ours counts parts by filter (vanillaId 396/397 && ai3===e.id). What about true eyes 400? Not counted — correct.

BUT what about the case where the core is in state 0 and ALL parts are -2: ours `parts.every(p => p.ai0 === -2)` → ai0=1. Original identical. OK.

10. checkDead for 398: original at :78841-78867. Let me read that to verify death transition.

Also missing in ours: random ambient sound `Main.rand.Next(200)==0 → PlaySound(29, ..., Next(93,100))` for ai0 != -1 && != 2. Minor ambient. Note.

Now let me read the checkDead section 78841-78867.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:27.092Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '78841,78880p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs checkDead for Moon Lord parts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:27.158Z

**📎 ToolResult**

```
		}
		if (type == 397 || type == 396)
		{
			if (ai[0] != -2f)
			{
				ai[0] = -2f;
				life = lifeMax;
				netUpdate = true;
				dontTakeDamage = true;
				if (Main.netMode != 1)
				{
					int num = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X, (int)base.Center.Y, 400);
					Main.npc[num].ai[3] = ai[3];
					Main.npc[num].netUpdate = true;
				}
			}
			return;
		}
		if (type == 398 && ai[0] != 2f)
		{
			ai[0] = 2f;
			life = lifeMax;
			netUpdate = true;
			dontTakeDamage = true;
			return;
		}
		if ((type == 517 || type == 422 || type == 507 || type == 493) && ai[2] != 1f)
		{
			ai[2] = 1f;
			ai[1] = 0f;
			life = lifeMax;
			dontTakeDamage = true;
			netUpdate = true;
			return;
		}
		if (type == 548 && ai[1] != 1f)
		{
			ai[1] = 1f;
			ai[0] = 0f;
			life = lifeMax;

```


---

## 🤖 Assistant · 2026-08-19T03:14:30.649Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
checkDead for 397/396: ai0=-2, life=lifeMax, dontTakeDamage, spawn NPC 400 at Center with ai[3] = part's ai[3] (core id). Ours matches (spawnTrueEye). For 398: ai0=2, life=lifeMax. Ours: `e.hp = e.maxHp`. Match.

Now the hand AI 37199-37711.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:31.292Z · glm-x-preview-260804

```
现在我来处理原版中的手部 aiStyle 78。
```


---

## 🤖 Assistant · 2026-08-19T03:14:31.485Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '37199,37350p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Moon Lord hand part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:31.542Z

**📎 ToolResult**

```
		else if (aiStyle == 78)
		{
			InitializeMoonLordAttacks();
			if (!Main.npc[(int)this.ai[3]].active || Main.npc[(int)this.ai[3]].type != 398)
			{
				life = 0;
				HitEffect();
				active = false;
			}
			bool flag90 = this.ai[2] == 0f;
			float num1231 = -flag90.ToDirectionInt();
			spriteDirection = (int)num1231;
			if (frameCounter == 19.0 && !dontTakeDamage)
			{
				PopAllAttachedProjectilesAndTakeDamageForThem();
			}
			dontTakeDamage = frameCounter >= 21.0;
			Vector2 vector159 = new Vector2(30f, 66f);
			float num1232 = 0f;
			float num1233 = 0f;
			bool flag91 = true;
			int num1234 = 0;
			if (this.ai[0] != -2f)
			{
				float num1235 = this.ai[0];
				this.ai[1]++;
				int num1236 = (int)Main.npc[(int)this.ai[3]].ai[2];
				int num1237 = ((!flag90) ? 1 : 0);
				int num1238 = 0;
				int num1239 = 0;
				for (; num1238 < 5; num1238++)
				{
					num1233 = MoonLordAttacksArray[num1236, num1237, 1, num1238];
					if (!(num1233 + (float)num1239 <= this.ai[1]))
					{
						break;
					}
					num1239 += (int)num1233;
				}
				if (num1238 == 5)
				{
					num1238 = 0;
					this.ai[1] = 0f;
					num1233 = MoonLordAttacksArray[num1236, num1237, 1, num1238];
					num1239 = 0;
				}
				this.ai[0] = MoonLordAttacksArray[num1236, num1237, 0, num1238];
				num1232 = (int)this.ai[1] - num1239;
				if (this.ai[0] != num1235)
				{
					netUpdate = true;
				}
			}
			if (this.ai[0] == -2f)
			{
				damage = 80;
				num1234 = 0;
				dontTakeDamage = true;
				this.ai[1]++;
				if (this.ai[1] >= 32f)
				{
					this.ai[1] = 0f;
				}
				if (this.ai[1] < 0f)
				{
					this.ai[1] = 0f;
				}
				Vector2 center27 = Main.npc[(int)this.ai[3]].Center;
				Vector2 vector160 = center27 + new Vector2(350f * num1231, -100f);
				Vector2 vector161 = vector160 - base.Center;
				if (vector161.Length() > 20f)
				{
					vector161.Normalize();
					vector161 *= 6f;
					Vector2 value4 = velocity;
					if (vector161 != Vector2.Zero)
					{
						SimpleFlyMovement(vector161, 0.3f);
					}
					velocity = Vector2.Lerp(value4, velocity, 0.5f);
				}
			}
			else if (this.ai[0] == 0f)
			{
				num1234 = 3;
				localAI[1] -= 0.05f;
				if (localAI[1] < 0f)
				{
					localAI[1] = 0f;
				}
				Vector2 center28 = Main.npc[(int)this.ai[3]].Center;
				Vector2 vector162 = center28 + new Vector2(350f * num1231, -100f);
				Vector2 vector163 = vector162 - base.Center;
				if (vector163.Length() > 20f)
				{
					vector163.Normalize();
					vector163 *= 6f;
					Vector2 value5 = velocity;
					if (vector163 != Vector2.Zero)
					{
						SimpleFlyMovement(vector163, 0.3f);
					}
					velocity = Vector2.Lerp(value5, velocity, 0.5f);
				}
			}
			else if (this.ai[0] == 1f)
			{
				num1234 = 0;
				int num1240 = 7;
				int num1241 = 4;
				if (num1232 >= (float)(num1240 * num1241 * 2))
				{
					localAI[1] -= 0.07f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
				}
				else if (num1232 >= (float)(num1240 * num1241))
				{
					localAI[1] += 0.05f;
					if (localAI[1] > 0.75f)
					{
						localAI[1] = 0.75f;
					}
					float num1242 = MathF.PI * 2f * (num1232 % (float)(num1240 * num1241)) / (float)(num1240 * num1241) - MathF.PI / 2f;
					localAI[0] = new Vector2((float)Math.Cos(num1242) * vector159.X, (float)Math.Sin(num1242) * vector159.Y).ToRotation();
					if (num1232 % (float)num1241 == 0f)
					{
						Vector2 vector164 = new Vector2(1f * (0f - num1231), 3f);
						Vector2 vector165 = Utils.Vector2FromElipse(localAI[0].ToRotationVector2(), vector159 * localAI[1]);
						Vector2 vector166 = base.Center + Vector2.Normalize(vector165) * vector159.Length() * 0.4f + vector164;
						Vector2 vector167 = Vector2.Normalize(vector165) * 8f;
						float ai = (MathF.PI * 2f * (float)Main.rand.NextDouble() - MathF.PI) / 30f + MathF.PI / 180f * num1231;
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector166.X, vector166.Y, vector167.X, vector167.Y, 452, 30, 0f, Main.myPlayer, 0f, ai);
					}
				}
				else
				{
					localAI[1] += 0.02f;
					if (localAI[1] > 0.75f)
					{
						localAI[1] = 0.75f;
					}
					float num1243 = MathF.PI * 2f * (num1232 % (float)(num1240 * num1241)) / (float)(num1240 * num1241) - MathF.PI / 2f;
					localAI[0] = new Vector2((float)Math.Cos(num1243) * vector159.X, (float)Math.Sin(num1243) * vector159.Y).ToRotation();
				}
			}
			else if (this.ai[0] == 2f)
			{
				localAI[1] -= 0.05f;
				if (localAI[1] < 0f)

```


---

## 🤖 Assistant · 2026-08-19T03:15:04.572Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Hand AI details so far:

1. `InitializeMoonLordAttacks()` — populates MoonLordAttacksArray based on core's ai[2] (num1236 = core.ai[2] as index). In the core, `ai[2] = Main.rand.Next(3); ai[2] = 0f;` — net effect always 0. So num1236 = 0. Ours hardcodes table index 0 via ML_HAND_ATTACKS keyed by ai2===0?0:1 for the hand's own ai[2] (side). Original: `num1237 = (!flag90) ? 1 : 0` — ai[2]!=0 → 1. So [core.ai2=0, hand side, 1(slot idx), attackIdx]. Ours matches.

2. Attack table advance: `num1233 = Array[.., .., 1, num1238]; if (!(num1233 + num1239 <= ai[1])) break; num1239 += (int)num1233;` — hmm: condition `!(num1233 + num1239 <= ai[1])` breaks when slotDur + consumed > ai1. So continues while slotDur + consumed <= ai1. Ours: `if (dur + consumed > e.ai1) break; consumed += dur; slot++`. Match. And when all 5 consumed → slot 0, ai1=0. Match. inSlot = ai1 - consumed. Match.

3. dontTakeDamage = frameCounter >= 21. Ours: `if (x.frame >= 21 || e.ai0 === -2) e.iframes = 2;` — and frameT mapping: num1234 values → frame target = num1234*7? Let me check the frame code at the end of the hand AI. Also `frameCounter == 19 && !dontTakeDamage → PopAllAttachedProjectilesAndTakeDamageForThem()` — projectiles stuck to the hand (the "open eye window"). Ours skips (approximation, documented? not mentioned). Minor.

4. State -2 (dead hand): damage=80, num1234=0, dontTakeDamage, ai1++ wrap at 32, hover at core+(350*side, -100) with 6/0.3 SimpleFlyMovement + Lerp(value4, velocity, 0.5).

IMPORTANT: `velocity = Vector2.Lerp(value4, velocity, 0.5)` — value4 = old velocity, velocity = new (after SimpleFlyMovement). Lerp(old, new, 0.5) = halfway. Ours flyLerp does exactly this. Good.

Ours -2: `if (e.ai1 >= 32) e.ai1 = 0;` and hover. But ours in -2 does NOT increment ai1! Let me re-check ours:

```
if (e.ai0 !== -2) {
  e.ai1 += 1;
  ...attackSlot...
}
...
if (e.ai0 === -2) { // closed-eye stump
  frameT = 0;
  e.def.damage = 80;
  if (e.ai1 >= 32) e.ai1 = 0;
  handHover(e, core, side);
}
```

Original in -2: `this.ai[1]++` — the ai1 increments ONLY in the -2 branch (the first block `if (this.ai[0] != -2f)` skipped). So in -2 state, ai1 increments each tick, wrapping at 32. Ours does NOT increment ai1 in -2 — the `if (e.ai1 >= 32) e.ai1 = 0` is a no-op then. What's ai1 used for in -2? Original: ai1 wrap 0-32, used for... in state -2 nothing else reads ai1 (maybe animation via frameCounter elsewhere?). Actually the hand's -2 uses ai1 for nothing except wrap. So the missing increment is harmless? In the head -2, ai2 drives the leech cycle; for hand, ai1 in -2 seems unused. But WAIT — there's a subtlety: original hand increments ai1 at the top when ai0 != -2 (before attack table). When hand enters -2 (checkDead), ai1 keeps its value, then in -2 increments and wraps 0..31. If it were to leave -2... never. So no impact. Fine.

5. State 0 (closed hover): num1234=3, localAI[1] -= 0.05 (clamp 0), hover. Ours matches (frameT=3, x.l1 -= 0.05 max 0).

6. State 1 (eye ring): num1234=0; num1240=7, num1241=4; cyc = 28.
   - if inSlot >= 56: l1 -= 0.07 clamp 0.
   - else if inSlot >= 28: l1 += 0.05 clamp 0.75; angle num1242 = 2π*(inSlot%28)/28 - π/2; l0 = (cos*30, sin*66).ToRotation(); if inSlot % 4 == 0 → fire 452.
   - else: l1 += 0.02 clamp 0.75; same angle.
   
   Ours matches: `if (inSlot >= cyc*2) ... else if (inSlot >= cyc) ... else ...`. Good.
   
   Fire: vector164 = (1*-side, 3); vector165 = Vector2FromElipse(l0.ToRotationVector2(), vector159 * l1) — i.e. the ellipse offset (cos(l0)*30*l1, sin(l0)*66*l1); vector166 = Center + Normalize(vector165)*vector159.Length()*0.4 + vector164. vector159.Length() = √(30²+66²) ≈ 72.46. vector167 = Normalize(vector165)*8. Projectile 452, 30 dmg, ai0=0, ai1=(2π·rand−π)/30 + π/180*side (some wobble). Ours handFireEye: px = e.cx + (exx/d)*72.46*0.4 - side; py = e.cy + (eyy/d)*72.46*0.4 + 3. Match (vector164 = (-side, 3)). Ours ignores the ai wobble arg — projectile 452 PhantasmalEye has ai wobble in its own AI; ours' shoot may not support. Minor.

7. Ours state 1 has NO hover movement — original state 1 also has no movement code (hand stays put / keeps velocity). Hmm — actually the hand keeps whatever velocity it had; there's damping? No — nothing. Original hand in attack states doesn't move itself; velocity persists → position += velocity each tick by the main update. That'd make the hand drift forever? No wait — the hand's velocity gets updated in states -2 and 0 via SimpleFlyMovement, and in state 2 via handSeek. In state 1 and 3, velocity is untouched → hand continues moving at its last velocity (which was hovering ~6 toward its spot). Hmm, but there's the position clamp box at the end (vector173 clamp). So it drifts but is clamped. Ours: same — no velocity change in state 1/3 (except ours... ours state 1 does nothing to velocity, then clamp box applies). OK equivalent.

Wait — does the position clamp apply in ours in every state? Ours applies the clamp unconditionally at the end (outside the state ifs). Original — let me verify it's also unconditional. Will read the rest.

Continue reading the hand 37350-37520.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:05.011Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '37350,37520p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Moon Lord hand part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:05.068Z

**📎 ToolResult**

```
				if (localAI[1] < 0f)
				{
					localAI[1] = 0f;
				}
				Vector2 center29 = Main.npc[(int)this.ai[3]].Center;
				Vector2 vector168 = new Vector2(220f * num1231, -60f) + center29;
				vector168 += new Vector2(num1231 * 100f, -50f);
				Vector2 vector169 = new Vector2(400f * num1231, -60f);
				if (num1232 < 30f)
				{
					Vector2 vector170 = vector168 - base.Center;
					if (vector170 != Vector2.Zero)
					{
						Vector2 vector171 = vector170;
						vector171.Normalize();
						velocity = Vector2.SmoothStep(velocity, vector171 * Math.Min(8f, vector170.Length()), 0.2f);
					}
				}
				else if (num1232 < 210f)
				{
					num1234 = 1;
					int num1244 = (int)num1232 - 30;
					if (num1244 % 30 == 0 && Main.netMode != 1)
					{
						Vector2 vector172 = new Vector2(5f * num1231, -8f);
						int num1245 = num1244 / 30;
						vector172.X += ((float)num1245 - 3.5f) * num1231 * 3f;
						vector172.Y += ((float)num1245 - 4.5f) * 1f;
						vector172 *= 1.2f;
						int num1246 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector172.X, vector172.Y, 454, 40, 1f, Main.myPlayer, 0f, whoAmI);
					}
					Vector2 vector173 = Vector2.SmoothStep(vector168, vector168 + vector169, (num1232 - 30f) / 180f) - base.Center;
					if (vector173 != Vector2.Zero)
					{
						Vector2 vector174 = vector173;
						vector174.Normalize();
						velocity = Vector2.Lerp(velocity, vector174 * Math.Min(20f, vector173.Length()), 0.5f);
					}
				}
				else if (num1232 < 282f)
				{
					num1234 = 0;
					velocity *= 0.9f;
				}
				else if (num1232 < 287f)
				{
					num1234 = 1;
					velocity *= 0.9f;
				}
				else if (num1232 < 292f)
				{
					num1234 = 2;
					velocity *= 0.9f;
				}
				else if (num1232 < 300f)
				{
					num1234 = 3;
					if (num1232 == 292f && Main.netMode != 1)
					{
						int num1247 = Player.FindClosest(position, width, height);
						Vector2 vector175 = Vector2.Normalize(Main.player[num1247].Center - (base.Center + Vector2.UnitY * -350f));
						if (float.IsNaN(vector175.X) || float.IsNaN(vector175.Y))
						{
							vector175 = Vector2.UnitY;
						}
						vector175 *= 12f;
						for (int num1248 = 0; num1248 < 1000; num1248++)
						{
							Projectile projectile3 = Main.projectile[num1248];
							if (projectile3.active && projectile3.type == 454 && projectile3.ai[1] == (float)whoAmI && projectile3.ai[0] != -1f)
							{
								projectile3.ai[0] = -1f;
								projectile3.velocity = vector175;
								projectile3.netUpdate = true;
								NetMessage.SendData(27, -1, -1, null, num1248);
							}
						}
					}
					Vector2 vector176 = Vector2.SmoothStep(vector168, vector168 + vector169, 1f - (num1232 - 270f) / 30f) - base.Center;
					if (vector176 != Vector2.Zero)
					{
						Vector2 vector177 = vector176;
						vector177.Normalize();
						velocity = Vector2.Lerp(velocity, vector177 * Math.Min(14f, vector176.Length()), 0.1f);
					}
				}
				else
				{
					num1234 = 3;
					Vector2 vector178 = vector168 - base.Center;
					if (vector178 != Vector2.Zero)
					{
						Vector2 vector179 = vector178;
						vector179.Normalize();
						velocity = Vector2.SmoothStep(velocity, vector179 * Math.Min(8f, vector178.Length()), 0.2f);
					}
				}
			}
			else if (this.ai[0] == 3f)
			{
				if (num1232 == 0f)
				{
					TargetClosest(faceTarget: false);
					netUpdate = true;
				}
				Vector2 v5 = Main.player[target].Center + Main.player[target].velocity * 20f - base.Center;
				localAI[0] = localAI[0].AngleLerp(v5.ToRotation(), 0.5f);
				localAI[1] += 0.05f;
				if (localAI[1] > 1f)
				{
					localAI[1] = 1f;
				}
				if (num1232 == num1233 - 35f)
				{
					SoundEngine.PlaySound(4, (int)position.X, (int)position.Y, 6);
				}
				if ((num1232 == num1233 - 14f || num1232 == num1233 - 7f || num1232 == num1233) && Main.netMode != 1)
				{
					Vector2 vector180 = Utils.Vector2FromElipse(localAI[0].ToRotationVector2(), vector159 * localAI[1]);
					Vector2 vector181 = Vector2.Normalize(v5) * 8f;
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + vector180.X, base.Center.Y + vector180.Y, vector181.X, vector181.Y, 462, 30, 0f, Main.myPlayer);
				}
			}
			if (flag91)
			{
				Vector2 center30 = Main.npc[(int)this.ai[3]].Center;
				Vector2 vector182 = new Vector2(220f * num1231, -60f) + center30;
				Vector2 vector183 = vector182 + new Vector2(num1231 * 110f, -150f);
				Vector2 max = vector183 + new Vector2(num1231 * 370f, 150f);
				if (vector183.X > max.X)
				{
					Utils.Swap(ref vector183.X, ref max.X);
				}
				if (vector183.Y > max.Y)
				{
					Utils.Swap(ref vector183.Y, ref max.Y);
				}
				Vector2 vector184 = Vector2.Clamp(base.Center + velocity, vector183, max);
				if (vector184 != base.Center + velocity)
				{
					base.Center = vector184 - velocity;
				}
			}
			int num1249 = num1234 * 7;
			if ((double)num1249 > frameCounter)
			{
				frameCounter++;
			}
			if ((double)num1249 < frameCounter)
			{
				frameCounter--;
			}
			if (frameCounter < 0.0)
			{
				frameCounter = 0.0;
			}
			if (frameCounter > 21.0)
			{
				frameCounter = 21.0;
			}
			int num1250 = 0;
			if (flag90)
			{
				num1250 = 0;
			}
			switch (num1250)
			{
			case 1:
				if (this.ai[0] == 0f)
				{
					if ((this.ai[1] += 1f) >= 20f)

```


---

## 🤖 Assistant · 2026-08-19T03:15:35.779Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Hand part 2 details vs ours:

State 2 (sphere): 
- vector168 = core.Center + (220*side, -60) + (side*100, -50). Ours: `ax = core.cx + 220*side + side*100; ay = core.cy - 60 - 50;` Match.
- vector169 = (400*side, -60). Ours match.
- inSlot<30: SmoothStep(velocity, dir*min(8, dist), 0.2). Ours handApproach(..., 8, 0.2) using vSmoothStep — Vector2.SmoothStep per-axis? Vector2.SmoothStep(cur, target, amount) is per-component smoothstep? Actually XNA Vector2.SmoothStep does per-component smoothstep interpolation: Lerp with smooth amount. Their vSmoothStep: lerp(cur, target, smoothAmt(amount)) — that's per-axis Lerp with smoothstep weight. Our helper doc says original Vector2.SmoothStep — fine.
- inSlot in [30,210): num1244 = inSlot-30; if %30==0 → fire 454 (40 dmg): vector172 = (5*side, -8); x += (k-3.5)*side*3; y += (k-4.5); *=1.2. Ours: `vx = 5*side + (k-3.5)*side*3; vy = -8 + (k-4.5); vx*=1.2; vy*=1.2`. Match.
- movement: target = SmoothStep(vector168, vector168+vector169, (inSlot-30)/180) - Center; velocity = Lerp(velocity, norm*min(20, len), 0.5). Ours: handSeek(ax+swx*t, ay+swy*t, 20, 0.5) with t = smoothAmt((inSlot-30)/180). Match.
- inSlot [210,282): frameT 0, vel *=0.9. [282,287): frameT1, *=0.9. [287,292): frameT2 *=0.9. [292,300): frameT3; at 292: redirect all own 454 projectiles toward player (from Center + UnitY*-350 = center+(0,-350)); vector175 = Normalize(player - (center + (0,-350)))*12. Ours approximates with 6 fresh 454 shots at 12 speed with spread — documented deviation. Acceptable per doc? It's flagged in comments as approximation. I might mention in "存疑/近似" but the task says focus on structural deviations. It IS a deviation with原版出处 difference but documented deliberately. I'll list under noted approximations, not CONFIRMED bugs.
- [300,330]: frameT3, SmoothStep back: t = 1-(inSlot-270)/30 → at inSlot 300: 1-1 = 0... wait (300-270)/30 = 1 → t=0; at 330: t=1-2= -1?? Hmm inSlot<330 total (330 slot). At inSlot=329: 1-59/30 = 1-1.97 = -0.97. Negative t! SmoothStep with negative amount → extrapolates beyond vector168 opposite... Whatever, ours clamps smoothAmt to [0,1]. Original would extrapolate. Minor.

Hmm wait, ours: `const t = 1 - (inSlot - 270) / 30; handSeek(e, ax + swx * smoothAmt(t), ..., 14, 0.1)`. smoothAmt clamps [0,1] — deviation but tiny.

- else (inSlot >= 300): hmm wait. Original: `else if (num1232 < 300f) {...}` then `else {...}` → inSlot in [300, 330): frameT3 + return-to-spot. But ours: `else if (inSlot < 300) {... frameT=3, redirect shots ...}` then `else { frameT = 3; handApproach(e, ax, ay, 8, 0.2); }`. Match.

State 3 (bolts): TargetClosest at inSlot==0; v5 = playerCenter + player.velocity*20 - Center; l0 = AngleLerp(l0, v5.ToRotation(), 0.5); l1 += 0.05 clamp 1; sound at inSlot == num1233-35 where num1233 = slot duration (ours: dur - 35 ✓); fire 462 (30 dmg) at inSlot == dur-14/-7/dur from ellipse offset (30,66)*l1, velocity Normalize(v5)*8. Ours matches (uses (exx, eyy) offset ✓, shoot from e.cx+exx... ✓, speed 8 ✓, dmg 30 ✓).

Note: ours plays 'NPC_Hit_6' for PlaySound(4,...,6) ✓.

- Position clamp (flag91=true always): vector182 = core.Center + (220*side,-60); vector183 = vector182 + (side*110, -150); max = vector183 + (side*370, 150). So box = [cx + 220*side + 110*side ... + 370*side]. Ours: `minX = core.cx + 220*side + 110*side; minY = core.cy - 60 - 150; maxX = minX + 370*side; maxY = minY + 150;` then swap. Match. Then Center clamped to box; position = clamped - velocity → equivalent to clamping next position (Center + velocity). Ours: `nx = clamp(e.cx + e.vx, minX, maxX); e.x = nx - e.w/2`. Match.

- frameCounter advance: num1249 = num1234*7; ++/-- clamp [0,21]. Ours matches. dontTakeDamage = frameCounter >= 21. Ours: `if (x.frame >= 21 || e.ai0 === -2) e.iframes = 2;` — the -2 explicit invuln matches original's explicit `dontTakeDamage = true` in -2 branch. 

BUT note ordering: in the original, `dontTakeDamage = frameCounter >= 21.0` happens EARLY (before the state machine), then the -2 branch sets it true again. In states 1/2/3 the hand is attack-open with frame < 21 (frameT 0..3*7=21 max? frameT=3 → target 21!). Hmm wait: num1234 = 3 in state 0 and in parts of state 2/else → target frame 21 → dontTakeDamage TRUE when frame reaches 21. So in state 0 (closed hover) the hand is invulnerable — matches "只有攻击中(睁眼)可受击" comment. In state 1/3 frameT=0 → frame drops → vulnerable. State 2 frameT 0..3 depending on phase: during sweep it's 1 (14), after 282 → 3 (21). Hmm: frame 14 → vulnerable; frame 21 → invulnerable. Interesting: during the 454-launch window (frameT=1 → 14) the hand is vulnerable. OK ours replicates via frame progression. Good.

- num1250/flag90 switch: `int num1250 = 0; if (flag90) num1250 = 0; switch (num1250) case 1:...` — dead code (case 0 does nothing?) Let me read what follows: the switch(num1250) with case 1 — but num1250 is always 0 when flag90 else... `if (flag90) num1250 = 0;` — else it stays 0 too. So the case-1 block is dead? Let me read the rest to make sure.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:36.181Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '37520,37712p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Moon Lord hand part 3"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:36.249Z

**📎 ToolResult**

```
					if ((this.ai[1] += 1f) >= 20f)
					{
						this.ai[1] = 0f;
						this.ai[0] = 1f;
						netUpdate = true;
					}
					velocity = Vector2.UnitX * 4f;
				}
				else if (this.ai[0] == 1f)
				{
					if ((this.ai[1] += 1f) >= 20f)
					{
						this.ai[1] = 0f;
						this.ai[0] = 2f;
						netUpdate = true;
					}
					velocity = Vector2.UnitX * -4f;
				}
				else if (this.ai[0] == 2f || this.ai[0] == 4f)
				{
					if ((this.ai[1] += 1f) >= 20f)
					{
						this.ai[1] = 0f;
						this.ai[0]++;
						netUpdate = true;
					}
					velocity = Vector2.UnitY * -4f * (flag90 ? 1 : (-1));
				}
				else
				{
					if (this.ai[0] != 3f && this.ai[0] != 5f)
					{
						break;
					}
					if ((this.ai[1] += 1f) >= 20f)
					{
						this.ai[1] = 0f;
						this.ai[0]++;
						if (this.ai[0] == 6f)
						{
							this.ai[0] = 0f;
						}
						netUpdate = true;
					}
					velocity = Vector2.UnitY * 4f * (flag90 ? 1 : (-1));
				}
				break;
			case 2:
			{
				Vector2 vector185 = new Vector2(30f, 66f);
				TargetClosest(faceTarget: false);
				Vector2 v6 = Main.screenPosition + new Vector2(Main.mouseX, Main.mouseY) - base.Center;
				float num1251 = v6.Length() / 200f;
				if (num1251 > 1f)
				{
					num1251 = 1f;
				}
				num1251 = 1f - num1251;
				num1251 *= 2f;
				if (num1251 > 1f)
				{
					num1251 = 1f;
				}
				localAI[0] = v6.ToRotation();
				localAI[1] = num1251;
				localAI[1] = 1f;
				break;
			}
			case 3:
			{
				int num1257 = 7;
				int num1258 = 4;
				this.ai[1]++;
				if (this.ai[1] >= (float)(num1257 * num1258 * 10))
				{
					this.ai[1] = 0f;
					break;
				}
				if (this.ai[1] >= (float)(num1257 * num1258))
				{
					localAI[1] -= 0.07f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
					break;
				}
				localAI[1] += 0.05f;
				if (localAI[1] > 0.75f)
				{
					localAI[1] = 0.75f;
				}
				float num1259 = MathF.PI * 2f * (this.ai[1] % (float)(num1257 * num1258)) / (float)(num1257 * num1258) - MathF.PI / 2f;
				localAI[0] = new Vector2((float)Math.Cos(num1259) * vector159.X, (float)Math.Sin(num1259) * vector159.Y).ToRotation();
				if (this.ai[1] % (float)num1258 == 0f)
				{
					Vector2 vector196 = new Vector2(1f * (0f - num1231), 3f);
					Vector2 vector197 = Utils.Vector2FromElipse(localAI[0].ToRotationVector2(), vector159 * localAI[1]);
					Vector2 vector198 = base.Center + Vector2.Normalize(vector197) * vector159.Length() * 0.4f + vector196;
					Vector2 vector199 = Vector2.Normalize(vector197) * 8f;
					float ai2 = (MathF.PI * 2f * (float)Main.rand.NextDouble() - MathF.PI) / 30f + MathF.PI / 180f * num1231;
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector198.X, vector198.Y, vector199.X, vector199.Y, 452, 5, 0f, Main.myPlayer, 0f, ai2);
				}
				break;
			}
			case 4:
			{
				Vector2 center31 = Main.npc[(int)this.ai[3]].Center;
				Vector2 vector186 = new Vector2(220f * num1231, -60f) + center31;
				vector186 += new Vector2(num1231 * 100f, -50f);
				Vector2 vector187 = new Vector2(400f * num1231, -60f);
				this.ai[1]++;
				if (this.ai[1] < 30f)
				{
					Vector2 vector188 = vector186 - base.Center;
					if (vector188 != Vector2.Zero)
					{
						Vector2 vector189 = vector188;
						vector189.Normalize();
						velocity = Vector2.SmoothStep(velocity, vector189 * Math.Min(8f, vector188.Length()), 0.2f);
					}
				}
				else if (this.ai[1] < 210f)
				{
					int num1252 = (int)this.ai[1] - 30;
					if (num1252 % 30 == 0 && Main.netMode != 1)
					{
						Vector2 vector190 = new Vector2(5f * num1231, -8f);
						int num1253 = num1252 / 30;
						vector190.X += ((float)num1253 - 3.5f) * num1231 * 3f;
						vector190.Y += ((float)num1253 - 4.5f) * 1f;
						vector190 *= 1.2f;
						int num1254 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector190.X, vector190.Y, 454, 1, 1f, Main.myPlayer, 0f, whoAmI);
					}
					Vector2 vector191 = Vector2.SmoothStep(vector186, vector186 + vector187, (this.ai[1] - 30f) / 180f) - base.Center;
					if (vector191 != Vector2.Zero)
					{
						Vector2 vector192 = vector191;
						vector192.Normalize();
						velocity = Vector2.Lerp(velocity, vector192 * Math.Min(4f, vector191.Length()), 0.1f);
					}
				}
				else if (this.ai[1] < 270f)
				{
					velocity *= 0.9f;
				}
				else if (this.ai[1] < 300f)
				{
					if (this.ai[1] == 270f && Main.netMode != 1)
					{
						int num1255 = Player.FindClosest(position, width, height);
						Vector2 vector193 = Vector2.Normalize(Main.player[num1255].Center - (base.Center + Vector2.UnitY * -350f));
						if (float.IsNaN(vector193.X) || float.IsNaN(vector193.Y))
						{
							vector193 = Vector2.UnitY;
						}
						vector193 *= 12f;
						for (int num1256 = 0; num1256 < 1000; num1256++)
						{
							Projectile projectile4 = Main.projectile[num1256];
							if (projectile4.active && projectile4.type == 454 && projectile4.ai[1] == (float)whoAmI && projectile4.ai[0] != -1f)
							{
								projectile4.ai[0] = -1f;
								projectile4.velocity = vector193;
								projectile4.netUpdate = true;
							}
						}
					}
					Vector2 vector194 = Vector2.SmoothStep(vector186, vector186 + vector187, 1f - (this.ai[1] - 270f) / 30f) - base.Center;
					if (vector194 != Vector2.Zero)
					{
						Vector2 vector195 = vector194;
						vector195.Normalize();
						velocity = Vector2.Lerp(velocity, vector195 * Math.Min(14f, vector194.Length()), 0.1f);
					}
				}
				else
				{
					this.ai[1] = 0f;
				}
				break;
			}
			case 5:
				dontTakeDamage = true;
				this.ai[1]++;
				if (this.ai[1] >= 40f)
				{
					this.ai[1] = 0f;
				}
				break;
			}
		}
		else if (aiStyle == 79)

```


---

## 🤖 Assistant · 2026-08-19T03:15:40.418Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `switch (num1250)` cases 1-5 are dead code (num1250 always 0) — probably debug leftovers from development. Ours ignores them. Fine.

Hand state 3 detail: sound condition `num1232 == num1233 - 35` where num1233 is the slot duration... wait num1233 was last assigned in the attack-slot loop: `num1233 = MoonLordAttacksArray[num1236, num1237, 1, num1238]` — after the loop completes/breaks, num1233 is the CURRENT slot's duration. So num1233 = dur. Ours uses `dur - 35` ✓.

Now the head aiStyle 79 at 37712-38128.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:40.873Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '37712,37902p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read NPC.cs Moon Lord head part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:40.932Z

**📎 ToolResult**

```
		else if (aiStyle == 79)
		{
			if (!Main.npc[(int)this.ai[3]].active || Main.npc[(int)this.ai[3]].type != 398)
			{
				life = 0;
				HitEffect();
				active = false;
			}
			if (localAI[3] == 13f && !dontTakeDamage)
			{
				PopAllAttachedProjectilesAndTakeDamageForThem();
			}
			dontTakeDamage = localAI[3] >= 15f;
			velocity = Vector2.Zero;
			base.Center = Main.npc[(int)this.ai[3]].Center + new Vector2(0f, -400f);
			Vector2 vector200 = new Vector2(27f, 59f);
			float num1260 = 0f;
			float num1261 = 0f;
			int num1262 = 0;
			int num1263 = 0;
			if (this.ai[0] >= 0f)
			{
				float num1264 = this.ai[0];
				this.ai[1]++;
				int num1265 = (int)Main.npc[(int)this.ai[3]].ai[2];
				int num1266 = 2;
				int num1267 = 0;
				int num1268 = 0;
				for (; num1267 < 5; num1267++)
				{
					num1261 = MoonLordAttacksArray[num1265, num1266, 1, num1267];
					if (!(num1261 + (float)num1268 <= this.ai[1]))
					{
						break;
					}
					num1268 += (int)num1261;
				}
				if (num1267 == 5)
				{
					num1267 = 0;
					this.ai[1] = 0f;
					num1261 = MoonLordAttacksArray[num1265, num1266, 1, num1267];
					num1268 = 0;
				}
				this.ai[0] = MoonLordAttacksArray[num1265, num1266, 0, num1267];
				num1260 = (int)this.ai[1] - num1268;
				if (this.ai[0] != num1264)
				{
					netUpdate = true;
				}
			}
			if (this.ai[0] == -3f)
			{
				damage = 0;
				dontTakeDamage = true;
				rotation = MathHelper.Lerp(rotation, MathF.PI / 12f, 0.07f);
				this.ai[1]++;
				if (this.ai[1] >= 32f)
				{
					this.ai[1] = 0f;
				}
				if (this.ai[1] < 0f)
				{
					this.ai[1] = 0f;
				}
				if (localAI[2] < 14f)
				{
					localAI[2]++;
				}
			}
			else if (this.ai[0] == -2f)
			{
				if (Main.npc[(int)this.ai[3]].ai[0] == 2f)
				{
					this.ai[0] = -3f;
					return;
				}
				damage = 80;
				dontTakeDamage = true;
				this.ai[1]++;
				if (this.ai[1] >= 32f)
				{
					this.ai[1] = 0f;
				}
				if (this.ai[1] < 0f)
				{
					this.ai[1] = 0f;
				}
				this.ai[2]++;
				if (this.ai[2] >= 555f)
				{
					this.ai[2] = 0f;
				}
				if (this.ai[2] >= 120f)
				{
					num1260 = this.ai[2] - 120f;
					num1261 = 555f;
					num1262 = 2;
					Vector2 vector201 = new Vector2(0f, 216f);
					if (num1260 == 0f && Main.netMode != 1)
					{
						Vector2 vector202 = base.Center + vector201;
						for (int num1269 = 0; num1269 < 255; num1269++)
						{
							Player player14 = Main.player[num1269];
							if (player14.active && !player14.dead && Vector2.Distance(player14.Center, vector202) <= 3000f)
							{
								Vector2 vector203 = Main.player[target].Center - vector202;
								if (vector203 != Vector2.Zero)
								{
									vector203.Normalize();
								}
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector202.X, vector202.Y, vector203.X, vector203.Y, 456, 0, 0f, Main.myPlayer, whoAmI + 1, num1269);
							}
						}
					}
					if ((num1260 == 120f || num1260 == 180f || num1260 == 240f) && Main.netMode != 1)
					{
						for (int num1270 = 0; num1270 < 1000; num1270++)
						{
							Projectile projectile5 = Main.projectile[num1270];
							if (projectile5.active && projectile5.type == 456 && Main.player[(int)projectile5.ai[1]].FindBuffIndex(145) != -1)
							{
								Vector2 center32 = Main.player[target].Center;
								int num1271 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)center32.X, (int)center32.Y, 401);
								Main.npc[num1271].netUpdate = true;
								Main.npc[num1271].ai[0] = whoAmI + 1;
								Main.npc[num1271].ai[1] = num1270;
							}
						}
					}
				}
			}
			else if (this.ai[0] == 0f)
			{
				num1263 = 3;
				TargetClosest(faceTarget: false);
				Vector2 v7 = Main.player[target].Center - base.Center - new Vector2(0f, -22f);
				float num1272 = v7.Length() / 500f;
				if (num1272 > 1f)
				{
					num1272 = 1f;
				}
				num1272 = 1f - num1272;
				num1272 *= 2f;
				if (num1272 > 1f)
				{
					num1272 = 1f;
				}
				localAI[0] = v7.ToRotation();
				localAI[1] = num1272;
				localAI[2] = MathHelper.Lerp(localAI[2], 1f, 0.2f);
			}
			if (this.ai[0] == 1f)
			{
				if (num1260 < 180f)
				{
					localAI[1] -= 0.05f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
					if (num1260 >= 60f)
					{
						Vector2 center33 = base.Center;
						int num1273 = 0;
						if (num1260 >= 120f)
						{
							num1273 = 1;
						}
						for (int num1274 = 0; num1274 < 1 + num1273; num1274++)
						{
							int num1275 = 229;
							float num1276 = 0.8f;
							if (num1274 % 2 == 1)
							{
								num1275 = 229;
								num1276 = 1.65f;
							}
							Vector2 vector204 = center33 + ((float)Main.rand.NextDouble() * (MathF.PI * 2f)).ToRotationVector2() * vector200 / 2f;
							int num1277 = Dust.NewDust(vector204 - Vector2.One * 8f, 16, 16, num1275, velocity.X / 2f, velocity.Y / 2f);
							Main.dust[num1277].velocity = Vector2.Normalize(center33 - vector204) * 3.5f * (10f - (float)num1273 * 2f) / 10f;
							Main.dust[num1277].noGravity = true;
							Main.dust[num1277].scale = num1276;
							Main.dust[num1277].customData = this;
						}
					}
				}
				else if (num1260 < num1261 - 15f)
				{
					if (num1260 == 180f && Main.netMode != 1)

```


---

## 🤖 Assistant · 2026-08-19T03:15:58.417Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Head part 1 vs ours:

1. -3 branch: ours `if (e.ai0 === -3)` — sets damage 0, spin lerp to π/12 at 0.07, ai1 wrap 32, f2 → 14, iframes. Ours misses `e.ai1++` in -3! Ours:
```
if (e.ai0 === -3) {
  e.def.damage = 0;
  e.spin = lerp(e.spin, Math.PI / 12, 0.07);
  if (e.ai1 >= 32) e.ai1 = 0;
  if (x.f2 < 14) x.f2 += 1;
  e.iframes = 2;
  return;
}
```
Original -3: ai1++ wrap. Unused elsewhere — harmless (same as hand -2).

BUT importantly: original -3 branch — `rotation = Lerp(rotation, π/12, 0.07)` — fine.

2. -2 branch: if core.ai0==2 → -3, return. Ours ✓. damage=80, dontTakeDamage, ai1++ wrap 32, ai2++ wrap 555. Ours: `if (e.ai1 >= 32) e.ai1 = 0; e.ai2 += 1; if (e.ai2 >= 555) e.ai2 = 0;` — ours does NOT increment ai1 in -2 (same no-op wrap). OK harmless.

Wait — ours increments ai2 BEFORE the >= 120 check. Original too. OK.

3. -2 leech: ai2>=120 → lt = ai2-120. At lt==0: spawn 456 from Center+(0,216) toward player (per player within 3000px). Ours: `if (lt === 0) addProj(new MoonLeechProj(e, player))` — MoonLeechProj spawns at src.cy+216 ✓ with speed 6 toward player. Original: velocity = Normalize(player.Center - spawn)*speed — speed unspecified (NewProjectile arg... `Projectile.NewProjectile(source, X, Y, SpeedX, SpeedY, 456, 0, 0f, Main.myPlayer, whoAmI+1, num1269)` — SpeedX/Y = vector203 normalized ×1 → speed 1?? Hmm: `vector203 = Main.player[target].Center - vector202; Normalize;` then passed as SpeedX/SpeedY → speed = 1. The projectile 456 aiStyle 85 accelerates to 16 anyway (per their comment). Ours initial speed 6 — from :37823? They cite 37823 出速 6 — that's the state-2 (attack) spawn. For the -2 branch it's speed 1. Tiny.

Also original passes ai[0]=whoAmI+1 (head id +1), ai[1]=player index. Ours MoonLeechProj stores srcId. Fine.

4. Moon leech spawn gate: original iterates projectiles 456 where player has buff 145 → NewNPC 401 at Main.player[target].Center. Ours: `if (!player.buffs.moonLeech) return;` — single gate, spawns ONE 401 per trigger tick instead of one per active leech projectile. Documented approximation. OK.

5. State 0: num1263=3; v7 = playerCenter - Center - (0,-22) → playerCenter - Center + (0,22). Ours: `dy = player.cy + 22 - e.cy` ✓. num1272 = clamp(1 - len/500, ...)*2 clamp 1 — ours: `x.l1 = Math.min(1, Math.max(0, (1 - Math.min(1, d / 500)) * 2));` ✓. l0 = v7.ToRotation() ✓ (set, not lerped — ours `x.l0 = Math.atan2(dy, dx)` ✓). l2 = Lerp(l2, 1, 0.2) ✓.

Note: original state 0 does NOT clamp localAI[1] to >= 0 after... it's computed from formula ≥ 0. fine.

Also note: TargetClosest in state 0.

6. State 1 (deathray): 
- lt < 180: l1 -= 0.05 clamp 0; if lt >= 60: charge dust (1 or 2 dusts based on lt>=120). Ours: particles 2 per tick in ellipse ±27/59 — approximates. OK.
- 180 <= lt < dur-15: at lt==180 → spawn 455. Then pupil tracks.

Let me read the rest 37902-38128.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:58.874Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '37902,38130p' ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria/NPC.cs",
 "description": "Read NPC.cs Moon Lord head part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:58.916Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria/NPC.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T03:16:05.344Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Typo in path — I missed "ra" in Terarria. Correct path: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs. Wait, earlier commands succeeded with "Terarria1456". The last one I typed "Terarria1456"? Let me check: error says `~/Project/GLM/SandboxWorld/Terarria1456/...` hmm, it shows Terarria1456 — no wait the error shows "Terarria1456"? The error message shows `~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs: No such file or directory` — hmm it displays "Terarria1456"? I can't tell from the rendering. Let me just retry with the exact path I used before (copy from earlier successful command).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:05.710Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '37902,38130p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read NPC.cs Moon Lord head part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:05.765Z

**📎 ToolResult**

```
					if (num1260 == 180f && Main.netMode != 1)
					{
						TargetClosest(faceTarget: false);
						Vector2 spinningpoint9 = Main.player[target].Center - base.Center;
						spinningpoint9.Normalize();
						float num1278 = -1f;
						if (spinningpoint9.X < 0f)
						{
							num1278 = 1f;
						}
						spinningpoint9 = spinningpoint9.RotatedBy((0f - num1278) * (MathF.PI * 2f) / 6f);
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, spinningpoint9.X, spinningpoint9.Y, 455, 75, 0f, Main.myPlayer, num1278 * (MathF.PI * 2f) / 540f, whoAmI);
						this.ai[2] = (spinningpoint9.ToRotation() + MathF.PI * 3f) * num1278;
						netUpdate = true;
					}
					localAI[1] += 0.05f;
					if (localAI[1] > 1f)
					{
						localAI[1] = 1f;
					}
					float num1279 = (this.ai[2] >= 0f).ToDirectionInt();
					float num1280 = this.ai[2];
					if (num1280 < 0f)
					{
						num1280 *= -1f;
					}
					num1280 += MathF.PI * -3f;
					num1280 += num1279 * (MathF.PI * 2f) / 540f;
					localAI[0] = num1280;
					this.ai[2] = (num1280 + MathF.PI * 3f) * num1279;
				}
				else
				{
					localAI[1] -= 0.07f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
						if (Main.netMode != 1 && Main.getGoodWorld)
						{
							for (int num1281 = 0; num1281 < 30; num1281++)
							{
								if (!WorldGen.SolidTile((int)(base.Center.X / 16f), (int)(base.Center.Y / 16f)))
								{
									Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, (float)Main.rand.Next(-1599, 1600) * 0.01f, (float)Main.rand.Next(-1599, 1) * 0.01f, 1021, 70, 10f);
								}
							}
						}
					}
					num1263 = 3;
				}
			}
			else if (this.ai[0] == 2f)
			{
				num1262 = 2;
				num1263 = 3;
				Vector2 vector205 = new Vector2(0f, 216f);
				if (num1260 == 0f && Main.netMode != 1)
				{
					Vector2 vector206 = base.Center + vector205;
					for (int num1282 = 0; num1282 < 255; num1282++)
					{
						Player player15 = Main.player[num1282];
						if (player15.active && !player15.dead && Vector2.Distance(player15.Center, vector206) <= 3000f)
						{
							Vector2 vector207 = Main.player[target].Center - vector206;
							if (vector207 != Vector2.Zero)
							{
								vector207.Normalize();
							}
							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector206.X, vector206.Y, vector207.X, vector207.Y, 456, 0, 0f, Main.myPlayer, whoAmI + 1, num1282);
						}
					}
				}
				if ((num1260 == 120f || num1260 == 180f || num1260 == 240f) && Main.netMode != 1)
				{
					for (int num1283 = 0; num1283 < 1000; num1283++)
					{
						Projectile projectile6 = Main.projectile[num1283];
						if (projectile6.active && projectile6.type == 456 && Main.player[(int)projectile6.ai[1]].FindBuffIndex(145) != -1)
						{
							Vector2 center34 = Main.player[target].Center;
							int num1284 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)center34.X, (int)center34.Y, 401);
							Main.npc[num1284].netUpdate = true;
							Main.npc[num1284].ai[0] = whoAmI + 1;
							Main.npc[num1284].ai[1] = num1283;
						}
					}
				}
			}
			else if (this.ai[0] == 3f)
			{
				if ((double)num1260 == 1.0)
				{
					TargetClosest(faceTarget: false);
					netUpdate = true;
				}
				Vector2 v8 = Main.player[target].Center + Main.player[target].velocity * 20f - base.Center;
				localAI[0] = localAI[0].AngleLerp(v8.ToRotation(), 0.5f);
				localAI[1] += 0.05f;
				if (localAI[1] > 1f)
				{
					localAI[1] = 1f;
				}
				if (num1260 == num1261 - 35f)
				{
					SoundEngine.PlaySound(4, (int)position.X, (int)position.Y, 6);
				}
				if ((num1260 == num1261 - 14f || num1260 == num1261 - 7f || num1260 == num1261) && Main.netMode != 1)
				{
					Vector2 vector208 = Utils.Vector2FromElipse(localAI[0].ToRotationVector2(), vector200 * localAI[1]);
					Vector2 vector209 = Vector2.Normalize(v8) * 8f;
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + vector208.X, base.Center.Y + vector208.Y, vector209.X, vector209.Y, 462, 30, 0f, Main.myPlayer);
				}
			}
			int num1285 = num1262 * 7;
			if ((float)num1285 > localAI[2])
			{
				localAI[2]++;
			}
			if ((float)num1285 < localAI[2])
			{
				localAI[2]--;
			}
			if (localAI[2] < 0f)
			{
				localAI[2] = 0f;
			}
			if (localAI[2] > 14f)
			{
				localAI[2] = 14f;
			}
			int num1286 = num1263 * 5;
			if ((float)num1286 > localAI[3])
			{
				localAI[3]++;
			}
			if ((float)num1286 < localAI[3])
			{
				localAI[3]--;
			}
			if (localAI[3] < 0f)
			{
				localAI[2] = 0f;
			}
			if (localAI[3] > 15f)
			{
				localAI[2] = 15f;
			}
			int num1287 = 0;
			if (num1287 == 1)
			{
				Vector2 vector210 = new Vector2(27f, 59f);
				TargetClosest(faceTarget: false);
				Vector2 v9 = Main.screenPosition + new Vector2(Main.mouseX, Main.mouseY) - base.Center;
				float num1288 = v9.Length() / 200f;
				if (num1288 > 1f)
				{
					num1288 = 1f;
				}
				num1288 = 1f - num1288;
				num1288 *= 2f;
				if (num1288 > 1f)
				{
					num1288 = 1f;
				}
				localAI[0] = v9.ToRotation();
				localAI[1] = num1288;
				localAI[1] = 1f;
			}
			if (num1287 == 2)
			{
				Vector2 vector211 = new Vector2(27f, 59f);
				float num1289 = MathF.PI * 2f * ((float)Main.timeForVisualEffects % 600f) / 600f;
				localAI[0] = new Vector2((float)Math.Cos(num1289) * vector211.X, (float)Math.Sin(num1289) * vector211.Y).ToRotation();
				localAI[1] = 0.75f;
				if (this.ai[1] == 0f)
				{
					Vector2 vector212 = num1289.ToRotationVector2();
					vector212 = Vector2.One;
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector212.X, vector212.Y, 455, 1, 0f, Main.myPlayer, MathF.PI / 300f, whoAmI);
				}
				this.ai[1]++;
				if (this.ai[1] >= 600f)
				{
					this.ai[1] = 0f;
				}
			}
			if (num1287 == 3)
			{
				Vector2 vector213 = new Vector2(0f, 216f);
				if (this.ai[1] == 0f)
				{
					TargetClosest(faceTarget: false);
					Vector2 vector214 = Main.player[target].Center - base.Center;
					vector214.Normalize();
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + vector213.X, base.Center.Y + vector213.Y, vector214.X, vector214.Y, 456, 0, 0f, Main.myPlayer, whoAmI + 1, target);
				}
				this.ai[1]++;
				if (this.ai[1] >= 600f)
				{
					this.ai[1] = 0f;
				}
			}
			if (num1287 == 4)
			{
				Vector2 vector215 = new Vector2(27f, 59f);
				TargetClosest(faceTarget: false);
				Vector2 v10 = Main.player[target].Center + Main.player[target].velocity * 20f - base.Center;
				localAI[0] = localAI[0].AngleLerp(v10.ToRotation(), 0.5f);
				localAI[1] = 1f;
				this.ai[1]++;
				if (this.ai[1] == 55f)
				{
					SoundEngine.PlaySound(4, (int)position.X, (int)position.Y, 6);
				}
				if (this.ai[1] == 76f || this.ai[1] == 83f || this.ai[1] == 90f)
				{
					Vector2 vector216 = Utils.Vector2FromElipse(elipseSizes: new Vector2(27f, 59f) * localAI[1], angleVector: localAI[0].ToRotationVector2());
					Vector2 vector217 = Vector2.Normalize(v10) * 8f;
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + vector216.X, base.Center.Y + vector216.Y, vector217.X, vector217.Y, 462, 5, 0f, Main.myPlayer);
				}
				if (this.ai[1] >= 90f)
				{
					this.ai[1] = 0f;
				}
			}
		}
		else if (aiStyle == 80)
		{

```


---

## 🤖 Assistant · 2026-08-19T03:16:54.004Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Head part 2 vs ours:

1. Deathray launch at lt==180: num1278 = -1 if spinningpoint9.X >= 0, +1 if < 0 (player on LEFT → +1). Ours: `const n = dx / d < 0 ? 1 : -1;` ✓. Angle: dir rotated by -num1278·2π/6. Ours: `ang = atan2 - n*(TAU/6)` ✓. ai2 = (angle + 3π)·num1278 — ours returns `(ang + Math.PI * 3) * n` ✓. Sweep = num1278·2π/540 ✓.

2. Pupil tracking after 180: num1279 = sign(ai2); num1280 = |ai2| + -3π + num1279·2π/540; l0 = num1280; ai2 = (num1280 + 3π)·num1279. Ours:
```
const n = e.ai2 >= 0 ? 1 : -1;
const a = Math.abs(e.ai2) - Math.PI * 3 + n * (TAU / 540);
x.l0 = a;
e.ai2 = (a + Math.PI * 3) * n;
```
✓. Note original increments l1 += 0.05 AFTER spawning ray, before tracking; ours sets `x.l1 = Math.min(1, x.l1 + 0.05)` after tracking code — same tick order irrelevant. ✓

Wait — one thing: original `localAI[1] += 0.05f` happens for the whole `lt in [180, dur-15)` window, ours `x.l1 = Math.min(1, x.l1 + 0.05)` at end of that branch ✓.

3. Final else (lt >= dur-15): l1 -= 0.07; when l1 < 0 → clamp 0 AND getGoodWorld → 30 shots of 1021 (70 dmg) each iteration while center not solid... wait, original: `for num1281 < 30: if (!SolidTile) { NewProjectile(...) }` — the solid check is INSIDE the loop, per shot but same value each iteration. Ours: checks solid once outside loop, fires 30 if not solid ✓ equivalent. Speed: `rand(-1599,1600)*0.01` for X (range -15.99..15.99), `rand(-1599,1)*0.01` for Y (range -15.99..0). Ours: `(Math.floor(Math.random() * 3199) - 1599) * 0.01` → [-1599, 1599]·0.01 ✓; `(Math.floor(Math.random() * 1600) - 1599) * 0.01` → [-1599, 0]·0.01 ✓. knockback 10 ignored. OK.

IMPORTANT: the l1 < 0 → 0 clamp happens ONCE? Original: `localAI[1] -= 0.07; if (localAI[1] < 0) { localAI[1] = 0; fire }` — every tick in this window, l1 goes from previous (≤1) down 0.07; once ≤ 0 it's clamped to 0, and next tick 0-0.07 < 0 → clamps again AND FIRES AGAIN each tick! Wait: after clamping to 0, the next tick subtracts 0.07 → -0.07 < 0 → clamp to 0 + fire 30 shots AGAIN. So in FTW it fires 30 shots EVERY tick for the remaining window (dur-15 - the time until l1 hits 0 ≈ 15 ticks → ~14 ticks × 30 = 420 projectiles)! Ours: `x.l1 -= 0.07; if (x.l1 < 0) { x.l1 = 0; if getGood fire 30 }` — same repeated-fire semantics! Ours comment says exactly that ("逐句照抄...原版语义" and "会连发——原版语义"). ✓ Good faithful.

4. Frame advance: num1285 = num1262*7 → localAI[2]; num1286 = num1263*5 → localAI[3]; clamps: `if (localAI[2] < 0) localAI[2] = 0; if (localAI[2] > 14) localAI[2] = 14;` then `if (localAI[3] < 0) localAI[2] = 0; if (localAI[3] > 15) localAI[2] = 15;` — decompiled BUG (should clamp localAI[3]). Ours clamps f3 to [0,15] and comments on this ("原版 :38042-38048 钳制误写 localAI[2],此处按语义钳 [3]") ✓ documented.

5. dontTakeDamage = localAI[3] >= 15 — ours: `if (x.f3 >= 15) e.iframes = 2;` ✓. Also original: `if (localAI[3] == 13 && !dontTakeDamage) PopAllAttachedProjectiles()` — ours skips. Minor.

6. State 2 (leech): num1262=2, num1263=3; at lt==0 spawn 456 at Center+(0,216) toward player; at lt 120/180/240 spawn 401 gated by buff. Ours ✓ (f2T=2, f3T=3; inSlot===0 spawn MoonLeechProj; 120/180/240 spawnMoonLeech).

Wait — ours head state 2: `if (inSlot === 0 && player)` — original spawns at num1260==0. But note ours' attackSlot returns inSlot = ai1 - consumed where ai1 was just incremented — at slot entry ai1=consumed+1? Let me trace: original: ai[1]++ then loop: slot found where slotDur+consumed > ai1. On entry to a new slot, ai1 = consumed+1 (just incremented past the boundary)... hmm. Original on transition tick: ai1 becomes e.g. 181; loop: slot0 dur 180: 180+0 <= 181 → consume; slot1 dur 30: 30+180=210 > 181 → break. inSlot = 181-180 = 1. So inSlot starts at 1, NOT 0! Because ai1 is incremented before the slot computation.

Ours: `e.ai1 += 1; const s = attackSlot(e, table);` — same: ai1 incremented first, then attackSlot. So inSlot starts at 1 for each slot. So `inSlot === 0` NEVER fires? Wait: at slot 0 after wrap: when table completes, slot=0, ai1=0, consumed=0 → inSlot = 0 - 0 = 0. Then next tick ai1=1 → inSlot=1. So inSlot===0 happens exactly once per full-table wrap (the tick where the table wrapped and ai1 was reset to 0 — but wait, the reset happens inside attackSlot when slot===table.length: `slot=0; e.ai1 = 0; consumed = 0;` and returns inSlot = 0-0 = 0. So the wrap tick has inSlot 0, then subsequent slot-0 ticks have inSlot 1,2,...

Original: same logic — `if (num1238 == 5) { num1238 = 0; ai[1] = 0; ... } num1232 = ai[1] - num1239 = 0`. So original also only sees num1260==0 on the wrap tick. And head state 2 is at slot index 2 — original checks `num1260 == 0f` which per above only happens on WRAP, not on entry to slot 2! Hmm interesting. So in vanilla, the 456 spawn at "slot 2 entry" actually fires only when the table wraps (ai1=0)? No wait — think again. num1260 = ai1 - consumed. When transitioning into slot 2, ai1 = consumed_2 + 1 → num1260 = 1. So `num1260 == 0` never true at slot-2 entry; only at wrap. But at wrap, slot becomes 0, not 2! So the `num1260 == 0` condition for state 2 would NEVER fire?!

Hmm, that can't be right — the Moon Leech Head does fire 456 in game. Let me re-check the slot loop:

```
for (; num1267 < 5; num1267++)
{
    num1261 = Array[...1, num1267];
    if (!(num1261 + (float)num1268 <= this.ai[1]))
        break;
    num1268 += (int)num1261;
}
if (num1267 == 5)
{
    num1267 = 0;
    this.ai[1] = 0f;
    ...
}
this.ai[0] = Array[...0, num1267];
num1260 = (int)this.ai[1] - num1268;
```

Hmm wait — when does ai[0] become 2? ai[0] = Array[0, slot]. The head table (index 2): [3,180],[0,30],[2,435],[3,180],[1,375]. On wrap, slot=0 → atk 3. Consumed grows: 180, 210, 645, 825, 1200. At ai1=826 (after passing 825): loop: slot0: 180<=826 consume(180); slot1: 30+180=210<=826 consume(210); slot2: 435+210=645<=826 consume(645); slot3: 180+645=825<=826 consume(825); slot4: 375+825=1200>826 break. slot=4 → atk 1 (deathray). num1260 = 826-825 = 1.

At ai1=646: slot0 consume 180; slot1: 210<=646 consume; slot2: 435+210=645<=646 consume; slot3: 180+645=825>646 break → slot=2, atk=2, num1260=646-645=1. So the leech slot's first tick has num1260==1, and num1260==0 only on wrap tick when slot resets to 0. So `if (num1260 == 0f)` in state 2 NEVER fires?? That would mean the head never fires 456 during slot 2!

Wait, that can't be. Let me recheck: maybe ai[1]++ happens where? For the head: inside `if (this.ai[0] >= 0f) { float num1264 = ai[0]; this.ai[1]++; ... }`. Yes incremented first. Hmm, so on wrap tick ai1=0: slot loop: slot0: num1261=180; 180+0 <= 0? No → break immediately. slot=0, atk=3, num1260 = 0-0 = 0. So num1260==0 on wrap tick with atk=3 (state 3 checks num1260==1 for TargetClosest — indeed state 3 uses num1260==1, interesting!).

State 2's spawn condition `num1260 == 0f`... under my trace it never fires within slot 2 (which spans num1260 1..435). Hmm — UNLESS ai[0]==2 can be entered from the checkDead reset (ai[0] set to something?) or... hmm. Actually wait — maybe I'm wrong about `(int)` casts: `num1268 += (int)num1261;` num1261 is float; slot durations from MoonLordAttacksArray. And num1260 = `(int)this.ai[1] - num1268`. All integers. OK.

Hmm, but hold on — maybe ai[0]==2 state is entered via the -2→? No. Let me think about actual vanilla behavior: the Moon Lord head's Moon Leech attack — the head opens its mouth and shoots the leech orb at the player. It definitely happens in game. So num1260 must equal 0 at some point during slot 2.

Let me re-trace more carefully. Initial spawn: ai0=0 (set by parent NewNPC? no — head spawned with ai[0]=0? Actually spawned with default ai[0]=0). ai1 starts 0. First tick: ai0=0 (from previous table assignment) — hmm the `if (ai[0] >= 0)` block: ai1++ → 1. slot loop with ai1=1: slot0: 180 <= 1? No → slot=0, atk=3. num1260=1-0=1. So state 3 inSlot=1... 

Hmm OK here's the thing — when does ai1 hit 181? tick: ai1=181: slot0: 180<=181 consume 180; slot1: 30+180=210<=181? No → slot=1, atk=0, num1260=181-180=1. ai1=211: slot1 consume; slot2: 435+210=645<=211? No → slot=2, atk=2, num1260=211-210=1. STILL 1.

So state 2 num1260 range = [1, 435]. `num1260 == 0` never. So how does vanilla fire the 456??

Unless... MoonLordAttacksArray durations differ. The table is [0,2] slot: [3,180],[0,30],[2,435],[3,180],[1,375]? Let me verify against InitializeMoonLordAttacks at 6830-6946. Maybe I have the order wrong. Let me read it.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:54.323Z · glm-x-preview-260804

```
我需要核实 `MoonLordAttacksArray` 表和 `true eye` 表。
```


---

## 🤖 Assistant · 2026-08-19T03:16:54.730Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '6830,6990p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read MoonLordAttacksArray initialization"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:54.779Z

**📎 ToolResult**

```
	public static int[,,,] InitializeMoonLordAttacks()
	{
		int[,,,] array = null;
		if (MoonLordAttacksArray != null)
		{
			array = MoonLordAttacksArray;
			for (int i = 0; i < array.GetLength(0); i++)
			{
				for (int j = 0; j < array.GetLength(1); j++)
				{
					for (int k = 0; k < array.GetLength(2); k++)
					{
						for (int l = 0; l < array.GetLength(3); l++)
						{
							array[i, j, k, l] = 0;
						}
					}
				}
			}
		}
		else
		{
			array = new int[3, 3, 2, 5];
		}
		array[0, 0, 0, 0] = 0;
		array[0, 0, 1, 0] = 50;
		array[0, 0, 0, 1] = 1;
		array[0, 0, 1, 1] = 70;
		array[0, 0, 0, 2] = 2;
		array[0, 0, 1, 2] = 330;
		array[0, 0, 0, 3] = 0;
		array[0, 0, 1, 3] = 60;
		array[0, 0, 0, 4] = 3;
		array[0, 0, 1, 4] = 90;
		array[0, 1, 0, 0] = 1;
		array[0, 1, 1, 0] = 70;
		array[0, 1, 0, 1] = 0;
		array[0, 1, 1, 1] = 50;
		array[0, 1, 0, 2] = 3;
		array[0, 1, 1, 2] = 90;
		array[0, 1, 0, 3] = 0;
		array[0, 1, 1, 3] = 60;
		array[0, 1, 0, 4] = 2;
		array[0, 1, 1, 4] = 330;
		array[0, 2, 0, 0] = 3;
		array[0, 2, 1, 0] = 180;
		array[0, 2, 0, 1] = 0;
		array[0, 2, 1, 1] = 30;
		array[0, 2, 0, 2] = 2;
		array[0, 2, 1, 2] = 435;
		array[0, 2, 0, 3] = 3;
		array[0, 2, 1, 3] = 180;
		array[0, 2, 0, 4] = 1;
		array[0, 2, 1, 4] = 375;
		array[1, 0, 0, 0] = 0;
		array[1, 0, 1, 0] = 0;
		array[1, 0, 0, 1] = 0;
		array[1, 0, 1, 1] = 0;
		array[1, 0, 0, 2] = 0;
		array[1, 0, 1, 2] = 0;
		array[1, 0, 0, 3] = 0;
		array[1, 0, 1, 3] = 0;
		array[1, 0, 0, 4] = 0;
		array[1, 0, 1, 4] = 0;
		array[1, 1, 0, 0] = 0;
		array[1, 1, 1, 0] = 0;
		array[1, 1, 0, 1] = 0;
		array[1, 1, 1, 1] = 0;
		array[1, 1, 0, 2] = 0;
		array[1, 1, 1, 2] = 0;
		array[1, 1, 0, 3] = 0;
		array[1, 1, 1, 3] = 0;
		array[1, 1, 0, 4] = 0;
		array[1, 1, 1, 4] = 0;
		array[1, 2, 0, 0] = 0;
		array[1, 2, 1, 0] = 0;
		array[1, 2, 0, 1] = 0;
		array[1, 2, 1, 1] = 0;
		array[1, 2, 0, 2] = 0;
		array[1, 2, 1, 2] = 0;
		array[1, 2, 0, 3] = 0;
		array[1, 2, 1, 3] = 0;
		array[1, 2, 0, 4] = 0;
		array[1, 2, 1, 4] = 0;
		array[2, 0, 0, 0] = 0;
		array[2, 0, 1, 0] = 0;
		array[2, 0, 0, 1] = 0;
		array[2, 0, 1, 1] = 0;
		array[2, 0, 0, 2] = 0;
		array[2, 0, 1, 2] = 0;
		array[2, 0, 0, 3] = 0;
		array[2, 0, 1, 3] = 0;
		array[2, 0, 0, 4] = 0;
		array[2, 0, 1, 4] = 0;
		array[2, 1, 0, 0] = 0;
		array[2, 1, 1, 0] = 0;
		array[2, 1, 0, 1] = 0;
		array[2, 1, 1, 1] = 0;
		array[2, 1, 0, 2] = 0;
		array[2, 1, 1, 2] = 0;
		array[2, 1, 0, 3] = 0;
		array[2, 1, 1, 3] = 0;
		array[2, 1, 0, 4] = 0;
		array[2, 1, 1, 4] = 0;
		array[2, 2, 0, 0] = 0;
		array[2, 2, 1, 0] = 0;
		array[2, 2, 0, 1] = 0;
		array[2, 2, 1, 1] = 0;
		array[2, 2, 0, 2] = 0;
		array[2, 2, 1, 2] = 0;
		array[2, 2, 0, 3] = 0;
		array[2, 2, 1, 3] = 0;
		array[2, 2, 0, 4] = 0;
		array[2, 2, 1, 4] = 0;
		InitializeMoonLordAttacks2();
		return array;
	}

	public static int[,] InitializeMoonLordAttacks2()
	{
		int[,] array = null;
		if (MoonLordAttacksArray2 != null)
		{
			array = MoonLordAttacksArray2;
			for (int i = 0; i < array.GetLength(0); i++)
			{
				for (int j = 0; j < array.GetLength(1); j++)
				{
					array[i, j] = 0;
				}
			}
		}
		else
		{
			array = new int[2, 10];
		}
		array[0, 0] = 0;
		array[1, 0] = 90;
		array[0, 1] = 1;
		array[1, 1] = 90;
		array[0, 2] = 0;
		array[1, 2] = 90;
		array[0, 3] = 2;
		array[1, 3] = 135;
		array[0, 4] = 0;
		array[1, 4] = 90;
		array[0, 5] = 3;
		array[1, 5] = 200;
		array[0, 6] = 0;
		array[1, 6] = 90;
		array[0, 7] = 4;
		array[1, 7] = 375;
		array[0, 8] = 0;
		array[1, 8] = 90;
		array[0, 9] = 2;
		array[1, 9] = 135;
		return array;
	}

	public static string GetFullnameByID(int npcID)
	{

```


---

## 🤖 Assistant · 2026-08-19T03:18:34.243Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
The tables match ours exactly:
- Hand ai2=0 (left): [[0,50],[1,70],[2,330],[0,60],[3,90]] ✓
- Hand ai2=1 (right): [[1,70],[0,50],[3,90],[0,60],[2,330]] ✓
- Head [0,2]: [[3,180],[0,30],[2,435],[3,180],[1,375]] ✓
- Array2 (true eyes): [[0,90],[1,90],[0,90],[2,135],[0,90],[3,200],[0,90],[4,375],[0,90],[2,135]] ✓ = ML_CORE_P2 ✓

Now back to the inSlot===0 question. With the loop as written, inSlot (num1260) at slot entry is 1, not 0... UNLESS the transition happens on a tick where ai1 jumps past multiple slots — no, durations ≥ 30.

Hmm wait, let me recompute. Loop: `if (!(num1233 + num1239 <= ai[1])) break;` Continue condition: num1233 + num1239 <= ai1, i.e. ai1 >= slotEnd. So while ai1 >= cumulative end of slot, advance. Break when ai1 < cumulative end. Then inSlot = ai1 - consumed where consumed = end of previous slots.

Entry into slot k happens when ai1 first exceeds end of slot k-1. Since ai1 increments by 1 per tick, first tick in slot k has ai1 = end_{k-1} + 1 → inSlot = 1. So inSlot ∈ [1, dur_k].

So `num1260 == 0` can only happen on the wrap tick (ai1=0 → slot 0, inSlot=0). And in state 2 (head), slot 2, inSlot==0 never fires. Same in ours: `inSlot === 0` in head state 2 never fires; ours' 456 spawn `if (inSlot === 0 && player)` — also never fires!

Wait but hold on — wrap tick: slot=0, ai1=0, atk = table[0] = 3. InSlot=0 with atk 3, not 2. Right.

Hmm, but wait — ours also does `e.ai1 += 1` then attackSlot. Same. So ours faithfully reproduces the (never-firing?) condition... That means in BOTH vanilla and ours, the head's Moon Leech 456 shot at slot-entry never fires? That seems wrong for vanilla. Let me reconsider: is there any other path where ai[0] becomes 2 with ai1 exactly at slot boundary?

What about when the head transitions from -2 back? No, -2 is permanent.

What about netUpdate/multiplayer resets? No.

Hmm, actually wait. Let me re-examine: maybe I have the wrong sign on the comparison. `if (!(num1233 + (float)num1239 <= this.ai[1])) { break; }` — breaks if NOT(slotDur + consumed <= ai1), i.e., breaks if slotDur + consumed > ai1. So we advance past slot only while ai1 >= slotEnd... Let me redo with numbers. Table head: durations [180, 30, 435, 180, 375].

Tick with ai1 = 180: slot0: num1233=180, num1239=0 → 180+0 <= 180 TRUE → don't break; num1239=180; slot1: num1233=30 → 30+180=210 <= 180? FALSE → break. slot=1, atk=0, inSlot = 180-180 = 0!! 

There it is — the boundary tick ai1 == 180 exactly gives inSlot 0 for slot 1. Because ai1 >= slotEnd uses <= (inclusive). So the slot switch happens when ai1 EQUALS the cumulative end: the last tick of slot k (ai1 == end_k) actually already lands in slot k+1 with inSlot=0.

So slots span inSlot ∈ [0, dur-1]... let me recompute: entry tick into slot k is when ai1 == end_{k-1} (the exact boundary), giving inSlot = end_{k-1} - consumed_{k-1} = 0. Then subsequent ticks inSlot 1..? until ai1 == end_k → transitions to slot k+1. So slot k covers inSlot ∈ [0, dur_k - 1]... wait: entry inSlot=0 at ai1=end_{k-1}; next tick ai1=end_{k-1}+1 → check: slot k-1: end_{k-1} <= ai1? Yes (equal was already consumed... careful: loop starts from slot 0 each tick).

Redo cleanly. Each tick: loop from slot 0; for each slot, if cumEnd <= ai1 → consume, advance. So slot selected = first slot where cumEnd > ai1. inSlot = ai1 - prevCumEnd.

ai1=1: cumEnd_0=180 > 1 → slot 0, inSlot 1.
...
ai1=180: cumEnd_0 = 180 <= 180 → consume (prev=180); slot1: cumEnd=210 > 180 → slot 1, inSlot = 180-180 = 0.
ai1=181..209: slot 1, inSlot 1..29.
ai1=210: slot1 consumed (210<=210); slot2 cumEnd 645 > 210 → slot 2, inSlot = 210-210 = 0. ✓
ai1=211..644: slot 2, inSlot 1..434.
ai1=645: slot 3, inSlot 0.
ai1=646..824: slot 3, inSlot 1..179.
ai1=825: slot 4, inSlot 0.
ai1=826..1199: slot 4, inSlot 1..374.
ai1=1200: loop consumes all 5 → slot==5 → wrap: slot=0, ai1=0, inSlot=0, atk=3 (slot 0 of table... atk = table[0]=3).

So slot durations effectively span inSlot 0..dur-1. Great — so `num1260 == 0` fires exactly on slot ENTRY. My earlier concern was wrong.

And OURS: attackSlot: `if (dur + consumed > e.ai1) break; consumed += dur; slot++;` — break if dur+consumed > ai1; else consume. Same semantics: advance while cumEnd <= ai1. So ours: entry tick inSlot = 0. ✓ Our `inSlot === 0` fires on slot entry. 

Now: ours' state 3 uses `if (inSlot === dur - 35)` sound — original `num1260 == num1261 - 35`. Slot 3 dur 180: fires at inSlot 145 ✓.

Ours fires 462 at inSlot === dur-14, dur-7, dur ✓.

Deathray slot 1 dur 375: original: lt < 180 fade; lt in [180, 360): fire at 180, pupil track until num1261-15 = 360; else (lt >= 360): closing 15 ticks. Ours: `else if (inSlot < dur - 15)` ✓ and else closing ✓.

OK so the head is faithful.

Now the deathray sweep direction/pupil: OK.

Now the true-eye fallback barrage ML_CORE_P2 with attacks 1-4. Ours only implements atk 1,2,3,4 with slot table; attack 0 = idle. Note case 4 deathray: `if (inSlot === 180) { e.ai2 = mlDeathray(...) }`. Fine as fallback (documented as fallback since true eyes are separate). But wait — ours runs this barrage when no NPC 400 exists. If spawnPart(400) succeeds (does NPC 400 exist in this project?), the barrage is skipped. Whatever.

But hold on — one important check on mlCoreBarrage case 2: `else if (inSlot === 60) { for k -1..1 mlShoot(...) }` — hmm whatever, fallback approximation, documented.

Now — CRITICAL check: the core state 1 in ours increments e.ai1 only when no eyes exist. In original, core state 1 doesn't run attacks at all. Ours matches (fallback only).

Now let me verify the true-eye AI (aiStyle 81 @38129+) is out of scope for this file (400 not implemented here; the fallback is in-file). The task says MoonLord family: 398/397/396 — done. 

Now remaining checks on our file:

A. moonLordCoreAI state 2 death drama: ours `e.vx = lerp(e.vx, 0, 0.02)` vs original Lerp amount 0.98. CONFIRMED deviation (named-args misread). Also state 3 flee same issue: ours lerp(e.vx, e.facing, 0.02) vs original 0.98. Also head -3 spin lerp 0.07: original `rotation = MathHelper.Lerp(rotation, MathF.PI / 12f, 0.07f)` — ours uses 0.07 ✓ (that one is fine).

Wait, let me double-check the state 2 lerp named args once more from the actual source text I read:

`velocity = Vector2.Lerp(value2: new Vector2(0f, -0.5f), value1: velocity, amount: 0.98f);`

Yes: value1=velocity, value2=(0,-0.5), amount=0.98 → Lerp(velocity, (0,-0.5), 0.98) — 98% per tick. Ours 0.02. Deviation CONFIRMED. Severity: state 2 lasts 600 ticks; velocity target tiny so net effect small; state 3 lasts 60 ticks — original core immediately moves at (±1, -0.5)·60 ≈ 60px sideways rise; ours barely moves. Visible but minor. Report as low-severity CONFIRMED.

B. Core death drama missing: at ai1==60, kill projectiles 456/462/455/452/454 and NPC 400s; ours doesn't. Also missing sound NPCDeath61 at ai1==1, missing projectile 622 explosions every 15 ticks (90-480). Ours has the %3 explosion particles but not 622. These are cosmetic-ish but the "kill remaining projectiles + true eyes at 60t" is structural: in ours, if true eyes (400) existed, they'd keep attacking during the 600t death drama. But since NPC 400 likely doesn't exist in the project, effect is limited to MLDeathray/MoonLeechProj entities persisting. Head deathray self-kills via ai0=-2 check. MoonLeechProj: dies when src dead — src is the head, which stays alive (ai0=-2) until core dead... Actually head -2 persists through the drama; MoonLeechProj would keep chasing. Minor. I'll fold this into one finding: "死亡演出缺 ai1==60 全弹幕清除" — medium-low.

C. Hand: `PopAllAttachedProjectilesAndTakeDamageForThem` at frame 19 (hand) / localAI[3]==13 (head) — skipped in ours. This handles... it's for projectiles attached to the NPC (like the eyes popping). Minor, skip or mention in passing.

D. Core state 0: original `TargetClosest(faceTarget: false)` — ours uses `player` param. Fine.

E. Core ambient sound `Main.rand.Next(200)==0 → PlaySound(29, Next(93,100))` when ai0 not -1/2 — missing in ours. Minor.

F. Hand -2: missing ai1++ (harmless).

G. Duke: alpha clamp 255 vs 150. Let me double check our line 261:
`if (e.ai0 !== -1 && e.ai0 < 9) e.spawnAlpha = inSolid(game, e) ? Math.min(255, e.spawnAlpha + 15) : Math.max(0, e.spawnAlpha - 15);`

Original clamps to 150 max in that block. And in case -1: `e.spawnAlpha = clamp(e.spawnAlpha - 5 + (inSolid ? 15 : 0), 0, 150)` ✓ (uses 150 there). So only the general block is wrong: 255 vs 150. CONFIRMED minor deviation. Symptom: Duke becomes fully invisible instead of semi-transparent when inside solid tiles (e.g. during sharknado hover inside walls). Wait — but does spawnAlpha 255 mean invisible in this engine? In case -1 spawn: spawnAlpha=255 initially and the comment says spawn演出 — the boss spawns invisible and fades in (alpha decreasing). So yes 255=invisible. Deviation real. Severity low-medium (visual: boss fully vanishes inside walls; vanilla keeps 150 = visible ghost).

Hmm wait, also for the enraged: ours computes enraged before the player-dead branch and uses `player.y < 800` — original `player.position.Y < 800`. position.Y = top. Ours player.y = top presumably ✓.

H. Duke case 0/5 hover: `if (player.dead) break;` — original `else if (ai[0] == 0f && !player.dead)`. ✓. But ours case 2 (bubbles) also has `if (player.dead) break` — original: state 2 branch has NO !player.dead guard! `else if (ai[0] == 2f)` — no player check... it uses player.Center etc. (player dead but still exists as entity). So in original, bubble state continues while player dead (using corpse position). Ours breaks (no movement/no bubbles; position += vx/vy still runs? no — `break` skips to after switch, then x+=vx,y+=vy DOES run at the end. Wait ours: `case 2: { if (player.dead) break; ... }` — break exits the switch, then `e.x += e.vx; e.y += e.vy;` runs. So velocity persists, boss drifts. Original: full bubble logic continues targeting dead player's body. Minor deviation in flee semantics. Actually the far/dead branch resets ai2 and ai0 to 0/5 at the top anyway (both original and ours), so state 2 wouldn't persist... in ours the dead branch returns early with ai0 reset to 0/5 — so case 2 wouldn't even be reached with dead player except... ours' dead branch: `if (!player || player.dead || dist > 5600) { ...; return; }` — resets ai0 to 0 or 5 and returns. So case 2 with dead player never happens in ours. The `if (player.dead) break` guards are dead code. OK.

But WAIT — there's a subtle issue with ours' early-return dead branch: it sets ai0 = (ai0>4 ? 5 : 0) EVERY tick while player dead. Original does the same (inside the dead branch, not a return). ✓.

I. dukeHover: ours reads `if (e.ai1 === 0) e.ai1 = sideOff * Math.sign(...)` — original `if (ai[1] == 0f) ai[1] = 300 * Math.Sign((center - player.Center).X)`. Hmm — Math.Sign returns 0 if X==0 → ai1 stays 0? then velocity target = player.Center + (0,-200). Ours: `Math.sign(e.cx - player.cx || 1)` — never 0. Trivial.

Note: ours dukeHover clamps nothing; direction/rotation code:
```
const s = Math.sign(player.cx - e.cx) || st.dir;
if (e.ai2 === 0 && s !== st.dir) e.spin += Math.PI;
st.dir = s;
if (st.spr !== -st.dir) e.spin += Math.PI;
st.spr = -st.dir;
```
Original:
```
int num27 = Math.Sign(player.Center.X - center.X);
if (num27 != 0)
{
    if (ai[2] == 0f && num27 != direction) rotation += PI;
    direction = num27;
    if (spriteDirection != -direction) rotation += PI;
    spriteDirection = -direction;
}
```
Match ✓ (ours guards num27==0 via || st.dir — keeps direction; original skips the whole block if 0 — equivalent since direction unchanged... well ours sets st.dir = s = st.dir; fine).

J. dukeCharge: original sets `velocity = Normalize(playerCenter - center) * num7; rotation = atan2(vy,vx); if (num27 != 0) { direction = num27; if (spriteDirection == 1) rotation += PI; spriteDirection = -direction; }`. Ours:
```
const s = Math.sign(dx) || st.dir;
st.dir = s;
if (st.spr === 1) e.spin += Math.PI;
st.spr = -s;
```
✓.

K. Case 12 teleport: original ALSO has the direction/rotation flip inside the teleport block with `if (ai[2] == 0f && ...)` — note ai2==15 at that point, so the rotation+=PI for direction change is skipped; only `if (spriteDirection != -direction) rotation += PI` applies. Ours:
```
const s = Math.sign(player.cx - e.cx) || st.dir;
st.dir = s; st.spr = -s;
```
— ours does NOT add π when spriteDirection flips! Original: after teleport, num41 = Sign(playerX - newCenterX); direction = num41; if (spriteDirection != -direction) rotation += PI. Ours skips the rotation adjustment → visual facing flip glitch in expert mode only. Expert-only (state 12 unreachable in classic). Minor; mention briefly maybe. Actually our comment block says "expert 分支保留注释" but state 12 IS implemented. It's reachable only in expert. Low.

L. Sharkron: missing PlaySound(4,...,19) at rise completion and DeathSound on wall hit. Also "player dead → shark dies" vs original re-target. Low.

M. ML_CORE_P2 case 2: shoots at inSlot===0 3 spheres slow, then at inSlot===60 redirect — fallback approximation. Documented. Fine.

N. MoonLeechProj: buff duration 840/60 = 14s ✓ classic. Ours uses `player.buffs.apply(BuffType.MoonLeech, 840/60)`. Fine.

O. mlDeathray: dmg passed as 75*2=150 (head) and 50*2=100 (core fallback) — comments justify via hostile×2. Fine per project convention.

P. Hand state 2 at inSlot<300 redirect: ours fires 6 new 454s instead of redirecting existing. Documented approximation. The count 6 is arbitrary (original redirects all 6 launched spheres — actually 6 spheres launched over 180 ticks (every 30t from 30..180 → 6 shots ✓). So 6 is right count. Speed 12 ✓ (direction toward player from center+(0,-350)... ours shoots from hand center toward player with spread. Documented). OK.

Q. Head state 1 charge dust: ours `if (inSlot >= 60)` spawns 2 particles in ±27/59 ellipse; original 1 dust (or 2 if lt>=120) — cosmetic. Fine.

R. Ours moonLordHeadAI: `if (e.ai0 < -3) e.ai0 = 0;` — defensive, fine.

S. Ours hand ai0: when player is null and ai0==1/3, the branches `e.ai0 === 1 && player` fail → frameT stays 0 and NOTHING happens (no hover). Original would use Main.player[target] regardless (dead players still have position). Ours: hand freezes (velocity persists, clamped in box). Minor single-player edge (player death during fight: hands freeze in place until core flee kicks in at ai1>=60 → parts killed). Original: same-ish since target dead → core ai0=3 at next tick → cleanup at 60. Fine.

T. spawnTrueEye position: original NewNPC at part Center — NewNPC X/Y is position (top-left)? or center? For the core spawn of hands ours subtracts h.w/2 — consistent treatment. Fine.

U. IMPORTANT — Duke state 4 (transformation): ours `invuln=true` (flag7=false ✓). Sound at ai2 === p1T-60 ✓.

V. Duke case 10: `e.spawnAlpha = Math.min(255, e.spawnAlpha + 25)` ✓ (alpha += 25 → MORE invisible; comment says 隐身逼近 — matches original alpha+=25 up to 255 invisible). But wait — original state 10 also sets `chaseable = false` (can't be hit by non-homing?) — ours ignores. Expert-only anyway.

W. In dukeFishronAI, the far-player branch: ours `e.encourageDespawn(10)` + manual vy. Hmm — does Enemy have encourageDespawn? It's called on e. Fine.

X. One more Duke check — flag5: `ai[3] < (flag3 ? 3 : 5)*2`. Ours ✓.

Y. Duke case 7 bubble spawn position: `bub.x = e.cx + (e.vx / vlen) * ((e.w + 20) / 2) - bub.w / 2; bub.y = ... + 45 - bub.h / 2;` ✓ matches vector12 + 45.

Z. MLDeathray hitbox/damage — plausible.

AA. Now check ours head -2 leech at `lt === 0` — fires MoonLeechProj — original ALSO gates on player within 3000px of spawn point. Ours no distance gate. Minor.

BB. Duke bubble spawn in state 2: `if (e.ai2 % DUKE.bubbleEvery === 0)` — original also plays PlaySound(4,...,19) each bubble (KidGrind?). Ours doesn't play the per-bubble sound. Minor sound gap. Eh.

CC. Now — one significant thing to verify: ours `moonLordCoreAI` — when core is in state 1 (phase 2), the parts (head -2, hands -2) remain; true eyes 400 exist → barrage skipped ✓. Core hovers ✓.

Also when ALL parts are -2 and eyes spawned — ours' state 0→1 transition requires parts.every(ai0===-2) ✓.

DD. What about hands/head being killed by damage → their AI runs `if (e.hp <= 0 && e.ai0 !== -2)` → set -2, heal to max, spawn eye ✓ matches checkDead. But NOTE: original checkDead also runs when the CORE is killed... whatever.

EE. Ours: head checkDead condition `e.ai0 !== -2 && e.ai0 !== -3` — original checkDead: `if (ai[0] != -2f)` only. If head is -3 (core died) and hp<=0... it's invulnerable anyway. Fine.

FF. Duke: ours plays 'Zombie_20' via playSfxWav for PlaySound(29,...,20). Wait — SoundID 29 is "Zombie" with style → Zombie_{style}.wav? Per memory "roar 键恒 Roar_0" and PlaySound(29) = Zombie sounds. Their mapping seems established. Skip.

GG. Now the one potentially REAL structural finding I should double-check: dukeEnraged uses `game.world.groundLevel` vs original `Main.worldSurface`. And the condition `player.y > surface` — worldSurface in tiles × 16. Ours: `(game.world.groundLevel || Math.floor(st.h * 0.3)) * TILE`. If groundLevel is already in pixels, multiplying by TILE would double-scale! Can't verify without reading GameHooks/world. Let me check quickly what groundLevel is in this project. Actually memory notes say world.groundLevel is used elsewhere. Let me grep quickly.

Also check `st.h * 0.3` fallback: worldSurface ≈ ~0.3·maxTilesY? Roughly (surface varies 0.25-0.35). OK.

Let me grep groundLevel definition.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:35.342Z · glm-x-preview-260804

```
这一部分的逻辑核对无误。让我来核实一下我们的代码所依赖的几个项目侧事实：`world.groundLevel` 单位（用于狂怒阈值）、`accelTo` 语义以及 `spawnPart`。
```


---

## 🤖 Assistant · 2026-08-19T03:18:36.296Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"groundLevel\" src/world/*.ts src/core/*.ts 2>/dev/null | head -20; grep -n \"export function accelTo\\|export function spawnPart\\|export function shoot\\|export function losClear\" src/entities/bossAI.ts",
 "description": "Find groundLevel definition and helper functions"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:36.392Z

**📎 ToolResult**

```
src/world/Invasion.ts:145:  if (py > w.groundLevel * 16 + screenHPx && w.spawnY <= w.groundLevel) return false; // 地下
src/world/MeteorFall.ts:17:  spawnX: number; groundLevel: number; rockLevel: number;
src/world/MeteorFall.ts:55:  for (let y = 5; y < h.groundLevel; y++) {
src/world/MeteorFall.ts:185:  const startDepth = Math.floor(h.groundLevel * 0.3);
src/world/SceneMetrics.ts:238:  const worldSurface = world.groundLevel;
src/world/World.ts:161:  groundLevel = 0; rockLevel = 0;   // tile 坐标
src/world/World.ts:245:   *  缺省 0=未知，使用处以 groundLevel 回退 */
src/world/World.ts:328:    w.groundLevel = p.groundLevel; w.rockLevel = p.rockLevel; w.lavaLine = p.lavaLine;
src/world/LunarEvent.ts:143:  const surface = Math.floor(w.groundLevel);         // (int)Main.worldSurface
src/core/Game.ts:349:export function saplingScanPlan(wTiles: number, hTiles: number, groundLevel: number,
src/core/Game.ts:357:  const underTiles = Math.max(1, (hTiles - Math.floor(groundLevel) - 19) * wTiles);
src/core/Game.ts:358:  const overTiles = Math.max(1, (Math.floor(groundLevel) - 11) * wTiles);
src/core/Game.ts:360:  const rows = Math.max(1, Math.max(0, Math.floor(groundLevel) - 11)
src/core/Game.ts:361:    + Math.max(0, hTiles - Math.floor(groundLevel) - 19));
src/core/Game.ts:369:    underY0: Math.floor(groundLevel) - 1, underY1: hTiles - 20,   // [gl-1, h-21]
src/core/Game.ts:370:    overY0: 10, overY1: Math.floor(groundLevel) - 1,              // [10, gl-2]
src/core/Game.ts:2849:    this.wiring.worldSurface = w.groundLevel;
src/core/Game.ts:2861:      worldSurface: w.groundLevel,
src/core/Game.ts:2883:      worldSurface: w.groundLevel,
src/core/Game.ts:3094:    const surface = Math.floor(w.groundLevel);  // 原版门 y<ws(:1835)仅干沙分支;此处扩展至 +40 捕获沙滩坡面
148:export function spawnPart(game: GameHooks, src: Enemy, id: number): Enemy | null {
633:export function accelTo(v: number, target: number, a: number): number {
648:export function losClear(game: GameHooks, x0: number, y0: number, x1: number, y1: number): boolean {
654:export function shoot(game: GameHooks, x: number, y: number, vx: number, vy: number, dmg: number, projId: number, life = 300, arrowOpts?: Partial<import('./Arrow').ArrowOpts>): void {

```


---

## 🤖 Assistant · 2026-08-19T03:18:40.983Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
groundLevel is in TILE coordinates (World.ts:161 "tile 坐标"), so `groundLevel * TILE` = pixels = worldSurface*16. ✓ Good, dukeEnraged is correct.

Let me check accelTo to confirm SimpleFlyMovement equivalence.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:41.295Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '625,665p' src/entities/bossAI.ts",
 "description": "Read accelTo and spawnPart helpers"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:41.427Z

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

```


---

## 🤖 Assistant · 2026-08-19T03:18:45.249Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
accelTo matches SimpleFlyMovement ✓.

Now let me double check the remaining flagged concern: the DeathrayProjectile AI at 30291-30549 — check a couple of key claims (sweep ±2π/540, life 180, scale formula, LOS branch). Let me read that section quickly to verify our MLDeathray.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:46.709Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '30291,30550p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs\" | grep -n \"num72\\|Kill\\|rotation\\|alpha\\|Laser\\|scale\\|localAI\\|SolidOrNo\\|position\\|num730\\|rectangle\" | head -80",
 "description": "Skim key lines of deathray AI 84"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:46.889Z

**📎 ToolResult**

```
7:					Kill();
10:				Vector2 vector58 = Utils.Vector2FromElipse(elipseSizes: new Vector2(27f, 59f) * Main.npc[(int)this.ai[1]].localAI[1], angleVector: Main.npc[(int)this.ai[1]].localAI[0].ToRotationVector2());
11:				base.position = Main.npc[(int)this.ai[1]].Center + vector58 - new Vector2(width, height) / 2f;
15:				Vector2 vector59 = Utils.Vector2FromElipse(elipseSizes: new Vector2(30f, 30f) * Main.npc[(int)this.ai[1]].localAI[1], angleVector: Main.npc[(int)this.ai[1]].localAI[0].ToRotationVector2());
16:				base.position = Main.npc[(int)this.ai[1]].Center + vector59 - new Vector2(width, height) / 2f;
21:				base.position = Main.npc[(int)this.ai[1]].Center + vector60 - base.Size / 2f + new Vector2(0f, 0f - Main.npc[(int)this.ai[1]].gfxOffY);
26:				base.position = Main.projectile[(int)this.ai[1]].Center + vector61 * 16f - new Vector2(width, height) / 2f + new Vector2(0f, 0f - Main.projectile[(int)this.ai[1]].gfxOffY);
41:					Kill();
44:				float num721 = (float)(int)this.ai[0] - 2.5f;
47:				float num722 = num721 * (MathF.PI / 6f);
48:				float num723 = 20f;
50:				float num724 = 1f;
51:				float num725 = 15f;
52:				float num726 = -2f;
55:					num724 = 1f - projectile3.ai[0] / 180f;
56:					num725 = 20f - projectile3.ai[0] / 180f * 14f;
59:						num723 = 20f - 4f * (projectile3.ai[0] / 120f);
64:						num723 = 16f - 10f * ((projectile3.ai[0] - 120f) / 60f);
67:					num726 = -22f + projectile3.ai[0] / 180f * 20f;
71:					num724 = 0f;
72:					num723 = 1.75f;
73:					num725 = 6f;
75:					num726 = -2f;
77:				float num727 = (projectile3.ai[0] + num721 * num723) / (num723 * 6f) * (MathF.PI * 2f);
78:				num722 = Vector2.UnitY.RotatedBy(num727).Y * (MathF.PI / 6f) * num724;
79:				zero3 = (Vector2.UnitY.RotatedBy(num727) * new Vector2(4f, num725)).RotatedBy(projectile3.velocity.ToRotation());
80:				base.position = projectile3.Center + vector63 * 16f - base.Size / 2f + new Vector2(0f, 0f - Main.projectile[(int)this.ai[1]].gfxOffY);
81:				base.position += projectile3.velocity.ToRotation().ToRotationVector2() * num726;
82:				base.position += zero3;
83:				velocity = Vector2.Normalize(projectile3.velocity).RotatedBy(num722);
84:				scale = 1.4f * (1f - num724);
106:					Kill();
109:				scale = (float)Math.Sin(this.ai[0] * MathF.PI / 300f) * 10f;
110:				if (scale > 1f)
112:					scale = 1f;
117:				if (localAI[0] == 0f)
119:					SoundEngine.PlaySound(29, (int)base.position.X, (int)base.position.Y, 104);
121:				float num728 = 1f;
124:					num728 = 0.4f;
126:				localAI[0]++;
127:				if (localAI[0] >= 180f)
129:					Kill();
132:				scale = (float)Math.Sin(localAI[0] * MathF.PI / 180f) * 10f * num728;
133:				if (scale > num728)
135:					scale = num728;
140:				float num729 = 1f;
141:				localAI[0]++;
142:				if (localAI[0] >= 50f)
144:					Kill();
147:				scale = (float)Math.Sin(localAI[0] * MathF.PI / 50f) * 10f * num729;
148:				if (scale > num729)
150:					scale = num729;
155:				float num730 = 0.8f;
156:				localAI[0]++;
157:				if (localAI[0] >= 90f)
159:					Kill();
162:				scale = (float)Math.Sin(localAI[0] * MathF.PI / 90f) * 10f * num730;
163:				if (scale > num730)
165:					scale = num730;
173:			rotation = num731 - MathF.PI / 2f;
208:			Collision.LaserScan(samplingPoint, velocity, num733 * scale, 2400f, array4);
222:					if (!Collision.CanHitLine(nPC13.position, nPC13.width, nPC13.height, player10.position, player10.width, player10.height))
233:			localAI[1] = MathHelper.Lerp(localAI[1], num734, amount);
236:				Vector2 vector64 = base.Center + velocity * (localAI[1] - 14f);
244:					Main.dust[num739].scale = 1.7f;
255:				Utils.PlotTileLine(base.Center, base.Center + velocity * localAI[1], (float)width * scale, DelegateMethods.CastLight);
259:				Vector2 vector67 = base.Center + velocity * (localAI[1] - 14f);

```


---

## 🤖 Assistant · 2026-08-19T03:18:55.882Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line numbers within the grep are relative to 30291. Let me look at the actual sub-block for aiStyle 84 with num728 (maxScale 1 / 0.4) — that's the one at relative line ~121-135: localAI[0]++, >= 180 → Kill; scale = sin(localAI[0]·π/180)·10·num728 clamped num728. Ours: `Math.sin((this.age * Math.PI) / 180) * 10 * this.maxScale` clamped ✓.

Note ours age++ happens BEFORE the 180 check (`this.age++; if (this.age >= 180) dead`), original: localAI[0]++ then >= 180 → Kill — same order ✓. But ours checks `if (!src || src.dead) dead` BEFORE age++ — fine.

Wait — one detail: ours does `this.angle += this.sweep` AFTER age++ — original: `rotation += ai[0]`? Let me look at the full block for the anchor and rotation to verify: line rel 173: `rotation = num731 - MathF.PI / 2f`? Hmm that's a different sub-style. The ai[0] sweep: I saw in the summary `:30521 rotation += ai[0]`. Let me read the specific block (rel ~105-140 abs 30395-30430).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:56.551Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '30390,30480p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs\"",
 "description": "Read deathray aiStyle 84 anchor and rotation block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:56.613Z

**📎 ToolResult**

```
			}
			if (type == 461)
			{
				this.ai[0]++;
				if (this.ai[0] >= 300f)
				{
					Kill();
					return;
				}
				scale = (float)Math.Sin(this.ai[0] * MathF.PI / 300f) * 10f;
				if (scale > 1f)
				{
					scale = 1f;
				}
			}
			if (type == 455)
			{
				if (localAI[0] == 0f)
				{
					SoundEngine.PlaySound(29, (int)base.position.X, (int)base.position.Y, 104);
				}
				float num728 = 1f;
				if (Main.npc[(int)this.ai[1]].type == 400)
				{
					num728 = 0.4f;
				}
				localAI[0]++;
				if (localAI[0] >= 180f)
				{
					Kill();
					return;
				}
				scale = (float)Math.Sin(localAI[0] * MathF.PI / 180f) * 10f * num728;
				if (scale > num728)
				{
					scale = num728;
				}
			}
			if (type == 642)
			{
				float num729 = 1f;
				localAI[0]++;
				if (localAI[0] >= 50f)
				{
					Kill();
					return;
				}
				scale = (float)Math.Sin(localAI[0] * MathF.PI / 50f) * 10f * num729;
				if (scale > num729)
				{
					scale = num729;
				}
			}
			if (type == 537)
			{
				float num730 = 0.8f;
				localAI[0]++;
				if (localAI[0] >= 90f)
				{
					Kill();
					return;
				}
				scale = (float)Math.Sin(localAI[0] * MathF.PI / 90f) * 10f * num730;
				if (scale > num730)
				{
					scale = num730;
				}
			}
			float num731 = velocity.ToRotation();
			if (type == 455)
			{
				num731 += this.ai[0];
			}
			rotation = num731 - MathF.PI / 2f;
			velocity = num731.ToRotationVector2();
			float num732 = 0f;
			float num733 = 0f;
			Vector2 samplingPoint = base.Center;
			if (vector57.HasValue)
			{
				samplingPoint = vector57.Value;
			}
			if (type == 455)
			{
				num732 = 3f;
				num733 = width;
			}
			else if (type == 461)
			{
				num732 = 2f;
				num733 = 0f;

```


---

## 🤖 Assistant · 2026-08-19T03:19:13.558Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
For 455: `num731 = velocity.ToRotation() + ai[0]; velocity = num731.ToRotationVector2();` — so the angle advances by ai[0] (sweep) each tick by rotating velocity. Ours: `this.angle += this.sweep` — equivalent ✓. Note the original rotation (sprite) = num731 - π/2, ours draws rotated by this.angle (draw code rotates by angle and draws a horizontal rect — equivalent to angle-π/2 sprite convention) ✓.

Also 455 anchored: earlier block at rel line 10-16: `if (Main.npc[ai[1]].type == 396) { vector58 = FromElipse(elipseSizes: (27,59)*npc.localAI[1], angleVector: npc.localAI[0].ToRotationVector2()); position = npc.Center + vector58 - size/2 } else if type==400 { vector59 = FromElipse((30,30)*localAI[1], localAI[0].ToRotationVector2()); ...}`. Ours: head → (cos·27·l1, sin·59·l1); core/true eye → (cos·30, sin·30) with l1=1 fixed (since true-eye NPC not implemented, anchored to our core fallback). Hmm — ours uses eyeA = this.angle for core (not npc's localAI[0]) — approximation documented ✓. But wait, for ours' 'core' kind anchored on OUR core enemy (398): the original anchor is the TRUE EYE (400) whose localAI tracks; ours uses core center + 30·direction(angle). Fine as documented fallback.

Also note original: `if (localAI[0] == 0) PlaySound(29,...,104)` — spawn sound Zombie_104; ours doesn't play. Minor.

Also the LaserScan branch and the "no line of sight → dist = distance-to-player + 150, amount 0.75": I saw at rel 222: `if (!Collision.CanHitLine(nPC13...player10...))`. And ours has that for head ✓ — but note: original applies the LOS check presumably only when the source NPC type... ours gates `this.kind === 'head'` ✓ plausible.

The Kill conditions at the top (rel 7, 41): `if (Main.npc[(int)ai[1]].ai[0] == -2) Kill()` (head closed eye) and general src-dead → Kill ✓ ours.

OK. Now let me also verify our ML_CORE_P2 fallback attack 1 (452 fan): cited from :37326-37334 which is the HAND eye-ring fire (single shot with wobble ai), not a 4-way fan with k from -1.5..1.5 step... Ours `for (let k = -1.5; k <= 1.5; k++)` → k = -1.5, -0.5, 0.5, 1.5 → 4 shots at ±0.35 rad spacing. Where's that from? The comment says "幻影之眼 452×4 扇形(:37326-37334)". The true-eye AI (aiStyle 81 :38243+) attack 1 (eye ring) — let me check :38326-38334 region... Actually ML_CORE_P2 case 1 cites :38243-38264-driven slot table and the true eye attack implementations at :38347-38600. Let me spot check the true eye AI attack 1 to see if it's a 4-fan. Since this is the fallback path only active when NPC 400 doesn't exist, precision matters less. But let me quickly verify to see whether the fallback matches true eye attack semantics.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:15.041Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38340,38400p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"; echo ----; sed -n '38440,38490p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"; echo ----; sed -n '38620,38660p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read true eye attacks for fallback comparison"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:15.248Z

**📎 ToolResult**

```
						else
						{
							velocity.Y += num1302;
						}
					}
				}
			}
			else if (this.ai[0] == 1f)
			{
				if (num1294 == 0f)
				{
					TargetClosest(faceTarget: false);
					netUpdate = true;
				}
				velocity *= 0.95f;
				if (velocity.Length() < 1f)
				{
					velocity = Vector2.Zero;
				}
				Vector2 v12 = Main.player[target].Center + Main.player[target].velocity * 20f - base.Center;
				localAI[0] = localAI[0].AngleLerp(v12.ToRotation(), 0.5f);
				localAI[1] += 0.05f;
				if (localAI[1] > 1f)
				{
					localAI[1] = 1f;
				}
				if (num1294 < 20f)
				{
					localAI[2] = MathHelper.Lerp(localAI[2], 1.1f, 0.2f);
				}
				else
				{
					localAI[2] = MathHelper.Lerp(localAI[2], 0.4f, 0.2f);
				}
				if (num1294 == num1295 - 35f)
				{
					SoundEngine.PlaySound(4, (int)position.X, (int)position.Y, 6);
				}
				if ((num1294 == num1295 - 14f || num1294 == num1295 - 7f || num1294 == num1295) && Main.netMode != 1)
				{
					Vector2 vector221 = Utils.Vector2FromElipse(localAI[0].ToRotationVector2(), vector218 * localAI[1]);
					Vector2 vector222 = Vector2.Normalize(v12) * 8f;
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + vector221.X, base.Center.Y + vector221.Y, vector222.X, vector222.Y, 462, 35, 0f, Main.myPlayer);
				}
			}
			else if (this.ai[0] == 2f)
			{
				if (num1294 < 15f)
				{
					localAI[1] -= 0.07f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
					localAI[2] = MathHelper.Lerp(localAI[2], 0.4f, 0.2f);
					velocity *= 0.8f;
					if (velocity.Length() < 1f)
					{
						velocity = Vector2.Zero;
					}
				}
----
					for (int num1307 = 0; num1307 < 2; num1307++)
					{
						int num1308 = Dust.NewDust(base.Center + vector223 - Vector2.One * 4f, 0, 0, 229);
						Dust dust = Main.dust[num1308];
						dust.velocity += vector223 / 15f;
						Main.dust[num1308].noGravity = true;
					}
					if ((num1294 - 15f) % 10f == 0f && Main.netMode != 1)
					{
						Vector2 vec4 = Vector2.Normalize(vector223);
						if (vec4.HasNaNs())
						{
							vec4 = Vector2.UnitY * -1f;
						}
						vec4 *= 4f;
						int num1309 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + vector223.X, base.Center.Y + vector223.Y, vec4.X, vec4.Y, 454, 40, 0f, Main.myPlayer, 30f, whoAmI);
					}
				}
				else if (num1294 < 105f)
				{
					localAI[0] = localAI[0].AngleLerp(this.ai[2] - MathF.PI / 2f, 0.2f);
					localAI[2] = MathHelper.Lerp(localAI[2], 0.75f, 0.2f);
					if (num1294 == 75f)
					{
						TargetClosest(faceTarget: false);
						netUpdate = true;
						velocity = Vector2.UnitY * -7f;
						for (int num1310 = 0; num1310 < 1000; num1310++)
						{
							Projectile projectile7 = Main.projectile[num1310];
							if (projectile7.active && projectile7.type == 454 && projectile7.ai[1] == (float)whoAmI && projectile7.ai[0] != -1f)
							{
								Projectile projectile8 = projectile7;
								projectile8.velocity += velocity;
								projectile7.netUpdate = true;
							}
						}
					}
					velocity.Y *= 0.96f;
					this.ai[2] = (Main.player[target].Center - base.Center).ToRotation() + MathF.PI / 2f;
					rotation = rotation.AngleTowards(this.ai[2], MathF.PI / 30f);
				}
				else if (num1294 < 120f)
				{
					SoundEngine.PlaySound(29, (int)base.Center.X, (int)base.Center.Y, 102);
					if (num1294 == 105f)
					{
						netUpdate = true;
					}
					Vector2 vector224 = (this.ai[2] - MathF.PI / 2f).ToRotationVector2() * 12f;
					velocity = vector224 * 2f;
----
						Main.dust[num1317].noGravity = true;
						Main.dust[num1317].scale = num1316;
						Main.dust[num1317].customData = this;
					}
				}
				else if (num1294 < num1295 - 15f)
				{
					if (num1294 == 180f && Main.netMode != 1)
					{
						TargetClosest(faceTarget: false);
						Vector2 spinningpoint11 = Main.player[target].Center - base.Center;
						spinningpoint11.Normalize();
						float num1318 = -1f;
						if (spinningpoint11.X < 0f)
						{
							num1318 = 1f;
						}
						spinningpoint11 = spinningpoint11.RotatedBy((0f - num1318) * (MathF.PI * 2f) / 6f);
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, spinningpoint11.X, spinningpoint11.Y, 455, 50, 0f, Main.myPlayer, num1318 * (MathF.PI * 2f) / 540f, whoAmI);
						this.ai[2] = (spinningpoint11.ToRotation() + MathF.PI * 3f) * num1318;
						netUpdate = true;
					}
					localAI[1] += 0.05f;
					if (localAI[1] > 1f)
					{
						localAI[1] = 1f;
					}
					float num1319 = (this.ai[2] >= 0f).ToDirectionInt();
					float num1320 = this.ai[2];
					if (num1320 < 0f)
					{
						num1320 *= -1f;
					}
					num1320 += MathF.PI * -3f;
					num1320 += num1319 * (MathF.PI * 2f) / 540f;
					localAI[0] = num1320;
					this.ai[2] = (num1320 + MathF.PI * 3f) * num1319;
				}
				else
				{
					localAI[1] -= 0.07f;

```


---

## 🤖 Assistant · 2026-08-19T03:19:35.321Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
The true-eye attack details differ substantially from ours' fallback (e.g. true eye attack 1 = triple 462 at 35 dmg — ours case 3 uses 462 ×3 at inSlot dur-14/-7/dur ✓ with dmg 35 ✓ citing :38382 ✓ — that matches). Our case 1 (452×4 fan) — the actual true-eye attack... let me not dig deeper; the fallback is explicitly a documented fallback. Note the true eye deathray dmg 50 ✓ matches our fallback case 4 (50 → ×2 = 100) ✓.

Our case 1 (four 452s in a fan) — where from? Maybe from true-eye attack 0? Actually the true eye slot 1 attack (array2 index1 = 1) → ai0==1 = triple 462. Hmm wait our ML_CORE_P2 maps atk numbers: [0,90],[1,90],... atk 1 = ? In the true eye AI, ai0==1 is the 462 triple (35 dmg). But OUR case 1 is "幻影之眼 452×4 扇形". And our case 3 is "三连幻影矢 462" citing :38378-38383. Hmm — so ours' atk 1 and atk 3 BOTH... let me look at true eye ai0 == 0 and 4:

From what I read: `else if (this.ai[0] == 1f)` = triple 462 (num1294 = dur-14/-7/dur, 35 dmg). So the true eye attack numbers: need the full mapping. Let me quickly grep the true eye AI's state list (ai0 values 0-5).

Actually — wait. Our ML_CORE_P2 = Array2 = [[0,90],[1,90],[0,90],[2,135],[0,90],[3,200],[0,90],[4,375],[0,90],[2,135]]. True eye ai0 ∈ {0,1,2,3,4,5}: 0 = idle/eye?, 1 = 462 triple, 2 = spheres 454, 3 = ?, 4 = deathray. Our case 1 = 452 fan — the true eye attack 1 is the 462 triple per the code above... That suggests our fallback's attack-number mapping is WRONG (case 1 should be triple 462 @35, not a 452 fan @30). And our case 3 (triple 462) cites :38378-38383 — the code at :38378 is exactly the 462 triple inside ai0==1! So ours assigned the SAME vanilla code to both case 1 (as 452 fan?) and case 3 (as 462 triple)?

Let me read our case 1 again:

```
case 1: // 幻影之眼 452×4 扇形(:37326-37334)
  if (inSlot === 0) {
    for (let k = -1.5; k <= 1.5; k++) {
      ... shoot 30 dmg 452, speed 8, angles atan2 + k*0.35
```

:37326-37334 is the HAND's eye-ring 452 shot (single shot from hand). So case 1 in our fallback uses the hand's 452 semantics as a 4-fan — an invented hybrid. In vanilla, true-eye slot "1" fires 3× 462 at 35 dmg.

Hmm — but hold on. Which is right for the FALLBACK? The fallback is supposed to emulate the true eyes (400). Array2 attack numbers index the TRUE EYE's ai0 states. True eye ai0==1 = triple 462 (35 dmg). So during a real fight phase 2, eyes cycle: idle(0) → 462 triple(1) → idle → spheres(2) → idle → ?(3) → idle → deathray(4) → idle → spheres(2).

What's true eye ai0 == 3? Let me check. If ai0==3 is something else (e.g. "eye spawn 452s"?) I need to see. Our case 3 = triple 462 citing :38378-38383 — but :38378 belongs to ai0==1. So our mapping looks shifted/wrong: case 1 should be 462 triple; case 3 should be whatever ai0==3 actually is.

Let me read the true eye AI fully to map ai0 states 0-5. It's at ~38129-38650. Let me scan for the branch labels.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:36.090Z · glm-x-preview-260804

```
后备方案中的 attack-number 映射需要与真实 aiStyle 81 状态进行验证。我先来映射它的 ai0 状态。
```


---

## 🤖 Assistant · 2026-08-19T03:19:37.276Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38129,38345p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | grep -n \"ai\\[0\\] ==\\|aiStyle == 81\\|MoonLordAttacksArray2\\|NewProjectile\\|num129\\|for (int num\" | head -60",
 "description": "Map true eye aiStyle 81 states"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:37.339Z

**📎 ToolResult**

```
3:			if (this.ai[0] == 0f)
18:				int num1290 = 30;
21:					for (int num1291 = 0; num1291 < 30; num1291++)
23:						if (WorldGen.SolidTile(point8.X, point8.Y + num1291))
25:							num1290 = num1291;
30:				if (num1290 < 15)
34:				else if (num1290 < 20)
43:				int num1292 = FindClosestPlayer(out distanceToPlayer);
44:				if (num1292 == -1 || Main.player[num1292].dead)
48:				if (distanceToPlayer < 352f && Main.player[num1292].Center.Y > base.Center.Y)
55:			else if (this.ai[0] == 1f)
63:					int num1293 = FindClosestPlayer();
64:					if (num1293 != -1)
66:						this.ai[3] = ((Main.player[num1293].Center.X > base.Center.X) ? (-1f) : 1f);
75:			else if (this.ai[0] == 2f)
89:			if (this.ai[0] == 2f)
96:		else if (aiStyle == 81)
109:			float num1294 = 0f;
110:			float num1295 = 0f;
111:			float num1296 = this.ai[0];
113:			int num1297 = 0;
114:			int num1298 = 0;
115:			for (; num1297 < 10; num1297++)
117:				num1295 = MoonLordAttacksArray2[1, num1297];
118:				if (!(num1295 + (float)num1298 <= this.ai[1]))
122:				num1298 += (int)num1295;
124:			if (num1297 == 10)
126:				num1297 = 0;
128:				num1295 = MoonLordAttacksArray2[1, num1297];
129:				num1298 = 0;
131:			this.ai[0] = MoonLordAttacksArray2[0, num1297];
132:			num1294 = (int)this.ai[1] - num1298;
133:			if (this.ai[0] != num1296)
137:			if (this.ai[0] == -1f)
144:				float num1299 = 1f;
147:					num1299 = 0.75f;
157:					num1299 = 1f;
166:					num1299 = 1.15f;
173:				localAI[2] = MathHelper.Lerp(localAI[2], num1299, 0.3f);
175:			if (this.ai[0] == 0f)
196:				for (int num1303 = 0; num1303 < Main.maxNPCs; num1303++)

```


---

## 🤖 Assistant · 2026-08-19T03:19:42.612Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=38324 && NR<=38650 && (/this\\.ai\\[0\\] ==/ || /NewProjectile/ || /else if/ || /PlaySound/)' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head; echo ====; grep -n \"this.ai\\[0\\] ==\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | awk -F: '$1>38220 && $1<38700'",
 "description": "List true eye state branch line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:42.738Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
			else if (this.ai[0] == 1f)
					SoundEngine.PlaySound(4, (int)position.X, (int)position.Y, 6);
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + vector221.X, base.Center.Y + vector221.Y, vector222.X, vector222.Y, 462, 35, 0f, Main.myPlayer);
			else if (this.ai[0] == 2f)
				else if (num1294 < 75f)
						int num1309 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + vector223.X, base.Center.Y + vector223.Y, vec4.X, vec4.Y, 454, 40, 0f, Main.myPlayer, 30f, whoAmI);
				else if (num1294 < 105f)
				else if (num1294 < 120f)
					SoundEngine.PlaySound(29, (int)base.Center.X, (int)base.Center.Y, 102);
			else if (this.ai[0] == 3f)
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-19T03:19:47.389Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n 'this.ai\\[0\\] ==' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | awk -F: '$1>38220 && $1<38700 {print}'",
 "description": "List true eye state lines precisely"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:47.447Z

**📎 ToolResult**

```
38265:			if (this.ai[0] == -1f)
38303:			if (this.ai[0] == 0f)
38347:			else if (this.ai[0] == 1f)
38385:			else if (this.ai[0] == 2f)
38508:			else if (this.ai[0] == 3f)

```


---

## 🤖 Assistant · 2026-08-19T03:19:55.026Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
True eye states: -1 (spawn/spinup), 0 (hover/anchor near core), 1 (triple 462 @35), 2 (spheres 454 @40 with redirect), 3 (deathray 455 @50), 4?? — wait, Array2 contains attack 4 (slot 7, 375t). Is there an ai0==4 branch? The grep shows branches only up to ==3f at 38508. The 455 deathray code I read at :38620-38660 is inside ai0==3! (num1294 == 180 → NewProjectile 455...). So ai0==3 = deathray, and ai0==4 = ...? No branch → nothing (default: nothing happens, just hover). Hmm wait — Array2 slot 7 = [4, 375]. If ai0==4 has no branch, the eye just hovers for 375 ticks? That seems odd. Let me check state 4 — maybe labeled differently, or maybe the ai0==4 slot is when the eye uses the "4" attack... Let me look at what's between 38508-38620 and after 38660.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:55.989Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38508,38560p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"; echo ----------; sed -n '38660,38700p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read true eye state 3 and after state block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:56.072Z

**📎 ToolResult**

```
			else if (this.ai[0] == 3f)
			{
				if (num1294 < 15f)
				{
					localAI[1] -= 0.07f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
					localAI[2] = MathHelper.Lerp(localAI[2], 0.4f, 0.2f);
					velocity *= 0.9f;
					if (velocity.Length() < 1f)
					{
						velocity = Vector2.Zero;
					}
				}
				else if (num1294 < 45f)
				{
					localAI[0] = 0f;
					localAI[1] = (float)Math.Sin((num1294 - 15f) * (MathF.PI * 2f) / 15f) * 0.5f;
					if (localAI[1] < 0f)
					{
						localAI[0] = MathF.PI;
					}
				}
				else if (num1294 < 185f)
				{
					if (num1294 == 45f)
					{
						this.ai[2] = (float)(Main.rand.Next(2) == 0).ToDirectionInt() * (MathF.PI * 2f) / 40f;
						netUpdate = true;
					}
					if ((num1294 - 15f - 30f) % 40f == 0f)
					{
						this.ai[2] *= 0.95f;
					}
					localAI[0] += this.ai[2];
					localAI[1] += 0.05f;
					if (localAI[1] > 1f)
					{
						localAI[1] = 1f;
					}
					Vector2 vector225 = localAI[0].ToRotationVector2() * vector218 * localAI[1];
					float num1312 = MathHelper.Lerp(8f, 20f, (num1294 - 15f - 30f) / 140f);
					velocity = Vector2.Normalize(vector225) * num1312;
					rotation = rotation.AngleLerp(velocity.ToRotation() + MathF.PI / 2f, 0.2f);
					if ((num1294 - 15f - 30f) % 10f == 0f && Main.netMode != 1)
					{
						Vector2 vector226 = base.Center + Vector2.Normalize(vector225) * vector218.Length() * 0.4f;
						Vector2 vector227 = Vector2.Normalize(vector225) * 8f;
						float ai3 = (MathF.PI * 2f * (float)Main.rand.NextDouble() - MathF.PI) / 30f + MathF.PI / 180f * this.ai[2];
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector226.X, vector226.Y, vector227.X, vector227.Y, 452, 35, 0f, Main.myPlayer, 0f, ai3);
					}
----------
					localAI[1] -= 0.07f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
				}
			}
		}
		else if (aiStyle == 82)
		{
			float num1321 = 90f;
			Vector2 vector229 = new Vector2(0f, 216f);
			int num1322 = (int)Math.Abs(this.ai[0]) - 1;
			int num1323 = (int)this.ai[1];
			if (!Main.npc[num1322].active || Main.npc[num1322].type != 396)
			{
				life = 0;
				HitEffect();
				active = false;
				return;
			}
			this.ai[2]++;
			if (this.ai[2] >= num1321)
			{
				if (Main.netMode != 1)
				{
					int num1324 = (int)Main.npc[num1322].ai[3];
					int num1325 = -1;
					int num1326 = -1;
					int num1327 = num1322;
					for (int num1328 = 0; num1328 < Main.maxNPCs; num1328++)
					{
						if (Main.npc[num1328].active && Main.npc[num1328].ai[3] == (float)num1324)
						{
							if (num1325 == -1 && Main.npc[num1328].type == 397 && Main.npc[num1328].ai[2] == 0f)
							{
								num1325 = num1328;
							}
							if (num1326 == -1 && Main.npc[num1328].type == 397 && Main.npc[num1328].ai[2] == 1f)
							{
								num1326 = num1328;

```


---

## 🤖 Assistant · 2026-08-19T03:20:09.591Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
True eye state mapping (aiStyle 81):
- ai0==0: hover/anchor (near core / retreat)
- ai0==1: triple 462 @35
- ai0==2: spheres 454 @40 (spiral launch + redirect downward at 75)
- ai0==3: 452 spiral shots @35 (spinning wheel attack, 375t? No — slot [3,200])... wait, Array2 slot 5 = [3, 200]. And the deathray is at :38620 — which state is that in? It's after 38508 (ai0==3)? The grep earlier showed `else if (this.ai[0] == 3f)` at 38508 and the 455 code at ~38625. So ai0==3 CONTAINS both the 452 spiral (num1294 < 185) AND... no wait, let me check: the 455 spawn at :38625 was inside `else if (num1294 < num1295 - 15f)` — that's within ai0==3? But Array2 slot 7 = [4, 375] and no ai0==4 branch exists. Hmm — the 455 in state 3? But slot 5 is [3,200] — 200t slot; the deathray needs ~375t.

Hold on — maybe I mis-attributed. Let me check whether there's an `else if (this.ai[0] == 4f)` after 38508 within the 81 block. The grep for 'this.ai[0] ==' between 38220-38700 showed only -1, 0, 1, 2, 3. So the block for ai0==3 spans from 38508 to... where does it end? aiStyle 82 starts at 38667. So ai0==3 branch runs 38508-38666 and includes sub-branches: <15, <45, <185 (452 spiral), then presumably <num1295-15 (455 deathray!) and else. So state 3 = "spin + 452 shots THEN deathray"?? But the slot for 3 is 200t... the 452 spiral covers <185, then deathray at 180?? overlapping... hmm confusing. Actually wait — maybe state 4 exists but written as `else` (final else, no condition). Let me check the structure between 38560 and 38625.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:10.047Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38560,38625p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\"",
 "description": "Read gap in true eye state 3"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:10.101Z

**📎 ToolResult**

```
					}
				}
				else
				{
					velocity *= 0.88f;
					rotation = rotation.AngleLerp(0f, 0.2f);
					localAI[1] -= 0.07f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
					localAI[2] = MathHelper.Lerp(localAI[2], 1f, 0.2f);
				}
			}
			else
			{
				if (this.ai[0] != 4f)
				{
					return;
				}
				if (num1294 == 0f)
				{
					TargetClosest(faceTarget: false);
					netUpdate = true;
				}
				if (num1294 < 180f)
				{
					localAI[2] = MathHelper.Lerp(localAI[2], 1f, 0.2f);
					localAI[1] -= 0.05f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
					velocity *= 0.95f;
					if (velocity.Length() < 1f)
					{
						velocity = Vector2.Zero;
					}
					if (!(num1294 >= 60f))
					{
						return;
					}
					Vector2 center38 = base.Center;
					int num1313 = 0;
					if (num1294 >= 120f)
					{
						num1313 = 1;
					}
					for (int num1314 = 0; num1314 < 1 + num1313; num1314++)
					{
						int num1315 = 229;
						float num1316 = 0.8f;
						if (num1314 % 2 == 1)
						{
							num1315 = 229;
							num1316 = 1.65f;
						}
						Vector2 vector228 = center38 + ((float)Main.rand.NextDouble() * (MathF.PI * 2f)).ToRotationVector2() * vector218 / 2f;
						int num1317 = Dust.NewDust(vector228 - Vector2.One * 8f, 16, 16, num1315, velocity.X / 2f, velocity.Y / 2f);
						Main.dust[num1317].velocity = Vector2.Normalize(center38 - vector228) * 3.5f * (10f - (float)num1313 * 2f) / 10f;
						Main.dust[num1317].noGravity = true;
						Main.dust[num1317].scale = num1316;
						Main.dust[num1317].customData = this;
					}
				}
				else if (num1294 < num1295 - 15f)

```


---

## 🤖 Assistant · 2026-08-19T03:20:20.078Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the mapping is clear:
- True eye ai0==1: triple 462 @35 (200t? no — slot [1,90]).
- ai0==2: spheres 454 @40 (slot [2,135]).
- ai0==3: 452 spiral spin attack @35 (slot [3,200]).
- ai0==4: deathray 455 @50 (slot [4,375]) — charge 180 then ray at 180, exactly like head.

OUR fallback ML_CORE_P2 mapping:
- case 1: "幻影之眼 452×4 扇形" citing :37326-37334 (hand's ring) — WRONG attack. Should be triple 462 @35 (:38378-38383).
- case 2: spheres 454 @40 — roughly right (approximation).
- case 3: "三连幻影矢 462" citing :38378-38383 — that's actually attack 1's code! Ours fires 462 @35 speed 8 at dur-14/-7/dur ✓ semantics — but assigned to attack 3 (which in vanilla is the 452 spiral).
- case 4: deathray @50 ✓.

So ours has attacks 1 and 3 swapped/mixed: attack 1 fires a made-up 452 fan, attack 3 fires the 462 triple (which belongs to attack 1), and the real attack 3 (452 spiral @35) is missing. HOWEVER — this fallback only runs when no NPC 400 exists. Does NPC 400 exist in this project? spawnPart(game, part, 400) — if 400 is in the enemy defs, true eyes spawn and the fallback is dead code. Let me check whether NPC 400 (Moon_LordFreeEye / "真眼") exists in the project's enemy data.

Also — hmm, wait. Actually let me reconsider: does the true eye exist? If not, then phase 2 = core fallback barrage ONLY, and these mapping errors are live behavior: phase 2 would never fire the 462 triple at the right slot or the 452 spiral at all. Let me check.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:21.292Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"400\" src/entities/*.ts src/data/*.ts 2>/dev/null | grep -i \"eye\\|真眼\\|MoonLordCore\\|moon_lord\" | head; grep -rln \"aiStyle 81\\|trueEye\\|TrueEye\" src/ | head",
 "description": "Check whether NPC 400 true eye exists in project"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:21.388Z

**📎 ToolResult**

```
src/entities/bossAI_duke_moonlord.ts:876:/** 二阶段弹幕表 = MoonLordAttacksArray2(:6966-6985,10 槽循环),驱动 NPC 400 真眼
src/entities/bossAI_duke_moonlord.ts:892: *  召 NPC 400 真眼,ai[3] = 部件的 ai[3](核心 id,游离眼 AI 据此锚定核心) */
src/entities/bossAI_duke_moonlord.ts:894:  const eye = spawnPart(game, part, 400);
src/entities/bossAI_duke_moonlord.ts:993:// 定轴扫射激光:锚定源 NPC 眼部(头 396 椭圆 (27,59)·睁眼度 / 真眼 400 椭圆 (30,30)),
src/entities/bossAI_duke_moonlord.ts:1003:  /** 'head' = 396 头眼 / 'core' = 400 真眼(本仓折叠到核心 398) */
src/entities/bossAI_duke_moonlord.ts:1212:      // 原版二阶段核心只悬停(:36912-36923),攻击全部由真眼 400(aiStyle 81)执行;
src/entities/bossAI_duke_moonlord.ts:1269:/** 核心二阶段弹幕(原版 NPC 400 真眼攻击链,aiStyle 81 :38347-38600;
src/entities/bossAI_duke_moonlord.ts:1328:  // 原版 checkDead(:78845-78857):血尽 → ai0=-2 闭眼残肢(满血续命+无敌)+召真眼 400
src/entities/bossAI_duke_moonlord.ts:1505:  // checkDead(:78845-78857)同手:血尽 → ai0=-2 闭眼残肢 + 召真眼 400
src/entities/Enemy.ts:1237:        case 81: moonLordFreeEyeAI(this, game, p); break;                // AI_081 月总游离眼 400（cs:38224 十槽攻击表+死光）
src/entities/bossAI_duke_moonlord.ts
src/entities/TideSlash.ts
src/entities/bossAI_lunar_misc.ts

```


---

## 🤖 Assistant · 2026-08-19T03:20:50.604Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
NPC 400 exists — `moonLordFreeEyeAI` in bossAI_lunar_misc.ts handles aiStyle 81. So the core's `mlCoreBarrage` fallback runs only when the true eyes failed to spawn (`!eyes`). Normally eyes exist → fallback dead. So the case 1/3 mis-mapping in the fallback is a dormant-code issue only. Still worth mentioning as a low-severity finding (fallback mislabeled: attack 1 should be 462 triple, attack 3 should be the 452 spiral; currently 1 is an invented 452 fan and 3 duplicates attack 1's vanilla code).

Wait, actually let me double-check moonLordFreeEyeAI quickly to see if IT implements the attacks correctly — it's out of scope (different file, task is this file). The task scope: "你负责审计整个文件" = bossAI_duke_moonlord.ts. OK stay in scope but can mention.

Now let me also double-check our core phase-2 gate: `eyes = enemies.some(n => !n.dead && n.vanillaId === 400 && n.ai3 === e.id)`. spawnTrueEye sets eye.ai3 = part.ai3 = core id ✓. And moonLordFreeEyeAI's own ai3 usage — whatever.

One more important check — in ours moonLordCoreAI, `if (e.hp <= 0 && e.ai0 !== 2) { e.ai0 = 2; ... }` runs BEFORE the state machine. checkDead in vanilla is invoked from StrikeNPC/hit pipeline, not in AI. Ours does it in AI — fine.

Also: our head/hand checkDead in AI sets `e.hp = e.maxHp` — but does Enemy.hurt() already handle "hp<=0 → die"? If the engine's generic death pipeline kills them before AI runs (hp<=0 → dead=true), the AI would never reach the checkDead emulation. Presumably the engine handles this via the `dontTakeDamage` iframes convention — they've done this pattern for other bosses (wof memory says "AI爆裂须die()勿直写dead"). The iframes=2 prevents death? Their established convention: e.iframes=2 refresh means hurt() no-ops, so hp never reaches 0 while invulnerable; when vulnerable and hp hits 0... hmm, then the NPC would die via the normal pipeline before our AI check. But that's engine-level; the boss code presumably has special handling for NPC 396/397/398 checkDead equivalents elsewhere (maybe in Enemy.hurt). Out of scope to fully verify — but let me do a quick sanity grep for how 396/397/398 death is handled in Enemy.ts to make sure the -2 transformation actually triggers.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:50.621Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"396\\|397\\|398\\|370\" src/entities/Enemy.ts | head -30",
 "description": "Check engine-side death handling for Moon Lord parts and Duke"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:50.690Z

**📎 ToolResult**

```
140: *  月总游离眼 400（锚核心 398 生命周期，自身不参与离屏消散）。
157:  263, 267, 328, 379, 380, 392, 393, 394, 396, 397, 398, 400, 413, 414, 422, 437, 438,
176: *  134 毁灭者 / 222 蜂后 / 245 石巨人 / 262 世纪之花 / 266 克脑 / 370 猪鲨 /
177: *  395 火星飞碟(:13993) / 396/397 月总头手 / 398 月总核心 / 439 异教徒 /
183: *  downed）。396/397/578/664 已随消散审计补入（EoW 14/15 同款离屏消散隐患,
187: *  4/35/50/113/125/126/127/134/222/245/262/266/370/395/396/397/398/439/578/
190:  4, 13, 35, 50, 113, 125, 126, 127, 134, 222, 245, 262, 266, 370, 395, 396, 397, 398,
333:    // 水蛭 117 出生爆尘+音（:51357-51370 localAI[1]==0 首帧）：NPCDeath13 + 20 尘
603:      // 目标速度（:52396-52401 归一到 num46 模长）
1245:        case 88: mothronAI(this, game, p); break;                          // AI_088 飞蛾魔 477（cs:39876 日食限定轮换+产卵）
1263:        case 77: moonLordCoreAI(this, game, p); break;                    // AI_077 月总核心 398(双手死前无敌)
1264:        case 78: moonLordHandAI(this, game, p); break;                    // AI_078 月总手 397(攻表/睁眼可击)
1265:        case 79: moonLordHeadAI(this, game, p); break;                    // AI_079 月总头 396(死亡之光/吸血)
1703:        case 1: return 4368; case 2: return 4369; case 3: return 4370; case 4: return 4371;
4537:        // 垂直 ai[0] 慢振荡 ±0.3（cs:23968-23981,0.01 步进）贴水深游
4562:          // 浅水上升检查（cs:23984-24000）：头顶格 liquid>128 且脚下 1-2 格
4845:  /** AI_024 鸟（NPC.cs:25396-25622 1:1）：三态——0 地面站立 / 1 飞行 / 2 降落。
4851:   *  鸟粪弹(BirdThatCanPoop→proj 1080,:25398-25407)未接——缺小动物→弹幕钩子,备案 */
5207:        this.vy *= 1.2; // TownCritter 上升补偿（cs:54398-54405）
5247:    //  `onGround && vx*=0.85` 自创衰减把巡航压到 0.397px/t（稳态 0.07/0.15），
7520:          const theta = (Math.random() * 2 - 1) * 0.7853981852531433;   // RotatedByRandom(0.785)
7698:      // 月总族(396/397/398)血尽不直死:原版 checkDead(:78841-78867)转为闭眼残肢/死亡演出,
7700:      if (this.vanillaId === 396 || this.vanillaId === 397 || this.vanillaId === 398) return false;
7907:      // PlaySound(15)，×2 次迭代 → 连播两声）；月总核心 398 DeathSound=null 无声。
7913:      if (this.vanillaId !== 398) {

```


---

## 🤖 Assistant · 2026-08-19T03:21:32.576Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Line 7698-7700 in Enemy.ts: Moon Lord family (396/397/398) does NOT die directly when hp hits 0 — engine-side gate exists. So the in-AI checkDead emulation works. Good.

Now let me quickly double check one more thing in the Duke: our case 12 teleport — original also re-checks `ai[2] == 0` for rotation π (false at 15) and `if (spriteDirection != -direction) rotation += PI`. Ours omits the spriteDirection flip π — expert only.

Also Duke: `case 10` in ours sets spawnAlpha +25 but never plays... original state 10: `chaseable = false`. Not modeled (Enemy may not have chaseable). Fine.

Now let me also verify our hand state 1 fire condition once more vs original: original `if (num1232 % (float)num1241 == 0f)` → inSlot % 4 == 0 (including inSlot 0? inSlot starts at 0 for slot entry — 0 % 4 == 0 → fires immediately at entry!). But wait — the fire block is inside `else if (num1232 >= num1240*num1241)` (inSlot >= 28). At entry inSlot=0 → the third branch (else). So firing happens at inSlot 28, 32, ..., 52. Ours: `if (inSlot >= cyc) { ... if (inSlot % 4 === 0) handFireEye(...) }` — fires at 28,32,...,52 ✓.

Hand state 2: `if ((inSlot - 30) % 30 === 0 && player)` → inSlot 30, 60, ..., 180 → 6 spheres ✓ k = (inSlot-30)/30 → 0..5 ✓.

Our hand 454 spawn: `shoot(game, e.cx, e.cy, vx, vy, 40, 454, 600)` from hand center ✓ (original from base.Center). ✓ Original also passes ai[1]=whoAmI for the redirect later — ours approximates.

OK. Now — the OTHER major thing to verify: our hand state 2's `frameT` (num1234) values. Original: inSlot<30: num1234 stays 0 (initialized 0). Wait — original sets `int num1234 = 0;` before states. State 2 at inSlot<30 doesn't set num1234 → 0. Ours: `if (inSlot < 30) { handApproach(...) }` — doesn't set frameT → 0 ✓. [30,210): num1234=1 ✓ ours frameT=1 ✓. [210,282): 0 ✓. [282,287): 1 ✓. [287,292): 2 ✓. [292,300): 3 ✓. else: 3 ✓. 

Hand state 3 num1234 = 0 (never set) ✓ ours frameT=0 ✓.

Head: num1262 (f2T) / num1263 (f3T): state -2: neither set (0,0)... wait original -2 doesn't set them (only in the ai2>=120 sub-block it sets num1260/61/62 — num1262=2!). Look: in head -2, `if (this.ai[2] >= 120f) { num1260 = ai2-120; num1261 = 555; num1262 = 2; ...}` — so during the -2 leech phase, num1262=2 → f2 target = 14 (mouth open). Ours -2: doesn't set f2T=2 during leech! Ours: `let f2T = 0, f3T = 0;` and in -2 branch returns early before the frame advance! Look at ours:

```
if (e.ai0 === -2) { // 闭眼残肢(:37782-37844)
  if (core.ai0 === 2) { e.ai0 = -3; return; }
  e.def.damage = 80;
  e.iframes = 2;
  if (e.ai1 >= 32) e.ai1 = 0;
  e.ai2 += 1;
  if (e.ai2 >= 555) e.ai2 = 0;
  if (e.ai2 >= 120 && player) { ...leech... }
  return;
}
```

Ours RETURNS — so f2/f3 never advance in -2 (and f2 never opens the mouth during leech). Original -2 does NOT return — falls through to the frame advance (num1285 = num1262*7 = 14 target → localAI[2] climbs to 14 = mouth open). And the -3 branch also falls through (no return; num1262=0, num1263=0 → frames close). Ours -3 returns too but sets f2 → 14 manually ✓ for -3 (visual closed... hmm wait ours -3 sets `if (x.f2 < 14) x.f2 += 1;` — that OPENS to 14, same as original's fall-through where num1262=0 → target 0 → f2 DECREASES to 0!

Hold on. Original -3: `if (localAI[2] < 14f) localAI[2]++;` — WAIT that's in the original -3 branch: `if (localAI[2] < 14f) { localAI[2]++; }` — the original ITSELF increments localAI[2] toward 14 in -3! Let me re-read:

```
if (this.ai[0] == -3f)
{
    damage = 0;
    dontTakeDamage = true;
    rotation = MathHelper.Lerp(rotation, MathF.PI / 12f, 0.07f);
    this.ai[1]++;
    if (this.ai[1] >= 32f) ...
    if (localAI[2] < 14f)
    {
        localAI[2]++;
    }
}
```

Yes — original -3 increments localAI[2] to 14 (and then falls through to the num1285 advance where target = num1262*7 = 0 < 14 → decrements... wait that would fight itself!). num1285 = num1262*7 = 0 → since 0 < localAI[2] → localAI[2]--. And the -3 branch did ++. Net: oscillates? ++ then -- = no change → stuck at whatever value ≤14... Actually per tick: -3 branch: if <14 → ++. Then frame advance: target 0 → --. Net zero. Hmm, funny vanilla quirk. Whatever — ours -3: `if (x.f2 < 14) x.f2 += 1; return;` → climbs to 14 and stays. Original: stuck oscillating (net frozen) at current value. Ours differs but this is a degenerate vanilla quirk. Not worth reporting as a top-10 maybe; it's cosmetic frame stuff. Hmm — actually wait, but original -3 does NOT return... it continues to num1287 blocks (dead code num1287=0). So yes only frame advance runs.

The -2 RETURN in ours is a real (small) deviation: during the残肢 leech phase, the head's mouth frame (f2) never opens in ours (original: num1262=2 → target 14, mouth opens while shooting leeches) and f3 closes at its own pace (original: num1263=0 → target 0). Also -2 in ours skips the f3 close (it stays wherever it was — likely 15 from closed invuln). Cosmetic-only (frame animation), but it's a structural branch difference: ours returns, original falls through. Also — the head -2 in ours never advances e.spin either; original -2 doesn't touch rotation. Fine.

Severity: low (visual). But CONFIRMED with both sides read. I'll include it in the report as a minor.

Also NOTE for the head -2: original head -2 continues executing the shared code AND — importantly — the `dontTakeDamage = localAI[3] >= 15` at top plus explicit `dontTakeDamage = true` in -2 ✓ ours.

Now, let me ALSO verify our hand -2 doesn't return: ours hand -2 does NOT return — it continues to frame advance and clamp ✓ matches original fall-through. Good — only the HEAD -2/-3 return early. And head -3 in ours returns before frame advance but manually advances f2 ✓-ish.

Next: verify our head state 1 `else` closing branch condition `inSlot < dur - 15` — original `num1260 < num1261 - 15f` ✓.

Now let me consolidate the findings list. Before that, a couple more checks:

1. Duke's `flag2` (expert 15%) — not applied (comment says classic unreachable) ✓ fine for classic mode. But note: our dukeFishronAI has no expert gating at all — mainExpertMode ≈ Main.expertMode. The file header says "expert 分支保留注释". OK consistent.

2. dukeEnraged: `player.y < 800` — original `player.position.Y < 800` ✓.

3. Our Duke damage mult: original `(int)(defDamage * 1.2f * num)` where num = expert ? 1.2 : 1 → classic: 1.2 ✓ ours (classic only) ✓.

4. Duke state 5→case2 transition: original sets velocity=norm*num19 (20), rotation, direction stuff, THEN ai0=7. Ours sets velocity, spin, dir/spr, then ai0=7 ✓.

5. Our dukeSharknado state 8 big: `addProj(new DukeSharknadoBolt(e.cx, e.cy, 0, 0, true, dukeEnraged(game, player), e))` ✓ (ai0=1, ai2=flag6).

6. ML deathray dmg: head passes 75*2=150. But hold on — hostile×2 rule at :13781 — that's for... their established convention (memory: several audits confirmed). Trust it.

7. MoonLeechProj out-phase speed: `spd = Math.min(16, d)` — if d < 20... hmm `Math.min(16, d)` where d = full distance to target — if player is 500px away, spd = 16 ✓. If d = 5, spd = 5 → then hit check `d < 20` → feeds buff. OK.

Wait — original: `Vector2 value = player.Center - center; velocity = ... Normalize(value) * min(16, value.Length())`? Let me verify the aiStyle 85 block quickly to confirm the min(16,d) claim and the (0,216) return target.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:33.038Z · glm-x-preview-260804

```
我来验证 Projectile.cs 中的 Moon Leech 弹射物 aiStyle 85。
```


---

## 🤖 Assistant · 2026-08-19T03:21:33.579Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '30678,30752p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs\"",
 "description": "Read Moon Leech projectile AI 85"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:33.634Z

**📎 ToolResult**

```
		else if (aiStyle == 85)
		{
			Vector2 vector79 = new Vector2(0f, 216f);
			alpha -= 15;
			if (alpha < 0)
			{
				alpha = 0;
			}
			int num764 = (int)Math.Abs(this.ai[0]) - 1;
			int num765 = (int)this.ai[1];
			if (!Main.npc[num764].active || Main.npc[num764].type != 396)
			{
				Kill();
				return;
			}
			localAI[0]++;
			if (localAI[0] >= 330f && this.ai[0] > 0f && Main.netMode != 1)
			{
				this.ai[0] *= -1f;
				netUpdate = true;
			}
			if (Main.netMode != 1 && this.ai[0] > 0f && (!Main.player[(int)this.ai[1]].active || Main.player[(int)this.ai[1]].dead))
			{
				this.ai[0] *= -1f;
				netUpdate = true;
			}
			rotation = (Main.npc[(int)Math.Abs(this.ai[0]) - 1].Center - Main.player[(int)this.ai[1]].Center + vector79).ToRotation() + MathF.PI / 2f;
			if (this.ai[0] > 0f)
			{
				Vector2 value8 = Main.player[(int)this.ai[1]].Center - base.Center;
				if (value8.X != 0f || value8.Y != 0f)
				{
					velocity = Vector2.Normalize(value8) * Math.Min(16f, value8.Length());
				}
				else
				{
					velocity = Vector2.Zero;
				}
				if (value8.Length() < 20f && localAI[1] == 0f)
				{
					localAI[1] = 1f;
					int buffTime = 840;
					if (Main.expertMode)
					{
						buffTime = 960;
					}
					if (!Main.player[num765].creativeGodMode)
					{
						ApplyBuffTo(Main.player[num765], 145, buffTime);
					}
				}
			}
			else
			{
				Vector2 value9 = Main.npc[(int)Math.Abs(this.ai[0]) - 1].Center - base.Center + vector79;
				if (value9.X != 0f || value9.Y != 0f)
				{
					velocity = Vector2.Normalize(value9) * Math.Min(16f, value9.Length());
				}
				else
				{
					velocity = Vector2.Zero;
				}
				if (value9.Length() < 20f)
				{
					Kill();
				}
			}
		}
		else if (aiStyle == 86)
		{
			if (localAI[1] == 0f)
			{
				localAI[1] = 1f;
				SoundEngine.PlaySound(SoundID.Item120, base.position);

```


---

## 🤖 Assistant · 2026-08-19T03:22:30.720Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
MoonLeechProj matches: min(16, dist) ✓, out→player, return→npc.Center+(0,216) ✓, buff 840/960 ✓, age 330 flip ✓, player-dead flip ✓, kill when source head dead (ours: src.dead — but note ours requires src alive where src = the head 396; original requires npc ai[0]-1 is an active 396 ✓).

One nuance: ours' `fed` gate: buffs applied once when d < 20 && out ✓ localAI[1]==0 gate ✓.

Ours' life 600: SetDefaults 456 timeLeft — plausible.

Ours: `if (!player || player.dead) { if (this.out) this.out = false; }` ✓.

Now compile the final findings. Let me rank:

CONFIRMED findings:

1. [Medium] Core death/flee velocity Lerp amount 0.02 vs original 0.98 (named-args misread).
   - Ours: lines 1224-1225 (state 2) and 1239-1240 (state 3).
   - Original: NPC.cs :37055-ish (state 2, "velocity = Vector2.Lerp(value2: new Vector2(0f, -0.5f), value1: velocity, amount: 0.98f)") and :37134 (state 3, "new Vector2(direction, -0.5f)").
   Let me get exact line numbers for those two. I read them in the 36930-37198 dump. State 2 lerp is right after `else if (this.ai[0] == 2f) { dontTakeDamage = true;` — need line number. Let me grep.

2. [Low-Med] Duke Fishron transparency clamp 255 vs 150 (line 261): boss fully invisible in solid vs vanilla semi-transparent. Original :49346-49364 (alpha clamp 150).

3. [Low-Med] Head -2 (残肢) returns early — skips frame advance (mouth never opens during leech loop, f3 never closes); original falls through with num1262=2 during leech. Ours lines 1534-1549; original :37782-37844 + :38016-38049.

4. [Low] Core state 2/3 missing ai1==60/40 projectile+true-eye cleanup (456/462/455/452/454 + NPC 400) — ours lines 1222-1248; original :36941-36952 (ai1==60) and :37130-37140 (ai1==40). Also missing NPCDeath61 at ai1==1.

5. [Low] Core ambient random sound (PlaySound 29 style 93-99 every ~200t) missing — ours whole core; original :36775-36778. Cosmetic.

6. [Low] Fallback barrage attack-number mapping wrong: case 1 should be true-eye attack 1 = triple 462 @35 (:38378-38383), case 3 should be the 452 spiral @35 (:38546-38554); ours case 1 = invented 452 fan (citing the HAND's :37326), case 3 = the 462 triple. Dormant unless NPC 400 spawn fails. Ours lines 1275-1299.

7. [Low] Sharkron: player-dead → dies (ours) vs vanilla re-target/continue; missing PlaySound(4,...,19) at lunge start and death sound on wall hit. Ours line 764; original :35196-35210.

8. [Low] Duke expert state 12 teleport omits the `spriteDirection != -direction → rotation += PI` flip (ours 430-438); original :50083-50097. Expert-only.

9. [Low] Hand/head: PopAllAttachedProjectilesAndTakeDamageForThem at frame 19 / localAI[3]==13 not implemented (ours none; original :37212-37214 hand, :37717-37720 head). Effect depends on attached-projectile mechanics (Eye tracker?); probably nil in our engine. Maybe fold into "minor" list.

10. [Low] Duke dead-player branch returns early — original continues state machine that tick (charge state keeps flying). Minor.

Also: bubble 371: ours `bub.ai3` random scale; fine. Bubble sound per spawn (PlaySound 4 style 19) missing in state 2/7 bubble spawns — original :49611/:49838 PlaySound(4,...,19) per bubble. Ours plays none. Minor sound.

Hmm, are there any HIGH severity findings? Let me think about whether I missed something structural in the priority list:

- Duke charge chain counting: ai3 += 2 per charge; pick tables ✓; enraged bubble→nado swap ✓; half-hp → state 4 ✓; expert second transformation gated by flag2 (expert only) ✓.
- Duke sharkron bolts ✓; tornado sharks ✓ (documented single-entity tower approximation).
- Moon Lord: hands dead → invulnerable until -2; core invuln until all -2 ✓; head -2 → -3 when core dying ✓; core death 600t ✓; teleport >2400 ✓; player-dead flee ai0=3 ✓.

One thing I should double check: the core's state 1 in ours — `if (e.ai0 === 1 && player)` — hovers via mlCoreHover ✓. But in state 1, when player is null → the "no player" gate sets ai0=3 ✓.

Another: in ours core state 0, `if (parts.length < 3) { e.dead = true; return; }` — original kills core if a part is inactive OR wrong type. Ours counts ai3===e.id parts among alive ones. If a hand is removed from the entities list entirely when dead (filtered by !n.dead) → length < 3 → core dies. In vanilla, dead hands become -2 (never inactive) so flag84 only triggers on true removal. Equivalent ✓.

Another potential issue: ours core `else if (e.ai0 === 0 || e.ai0 === 1)` block — in state 1, the parts filter still runs but unused. Fine.

What about ours hand: `const core = (game.enemies() as Enemy[]).find((n) => n.id === e.ai3 && n.vanillaId === 398); if (!core || core.dead) { e.dead = true; return; }` — matches original (inactive or type != 398 → deactivate) ✓. Note: `n.id === e.ai3` — ai3 stores core id ✓ set at spawn (h.ai3 = e.id) ✓.

BUT — original also requires `Main.npc[(int)this.ai[3]].type != 398` check → dies if ai3 points to a non-398. Ours checks vanillaId === 398 ✓.

What about hand when core is in state -2 (teleport drama)? Hand keeps hovering around core position ✓ (original: same, no special case).

Duke spawn state -1: `if (e.ai2 > 20) { e.vy = -2; ... }` — original `if (ai[2] > 20f)` ✓. Alpha: original in spawn: alpha -= 5 (+15 solid), clamp [0,150] ✓ ours clamp 0..150 ✓ (line 272).

Hmm wait — ours line 272: `e.spawnAlpha = clamp(e.spawnAlpha - 5 + (inSolid(game, e) ? 15 : 0), 0, 150);` ✓.

And line 273: `else if (e.spawnAlpha < 255) e.spawnAlpha = 255;` — original: no else-clause... original: only the ai2>20 block modifies alpha; else nothing. But initial alpha=255 set at localAI[0] init. So else-restore-to-255 is harmless (alpha already 255 at that point? Not necessarily — the general block `if (ai[0] != -1 && ai[0] < 9)` doesn't run in state -1. So alpha stays 255 in spawn until ai2>20 fades it. Ours' else forces 255 — same since nothing else changed it. ✓ fine.

Now — the biggest remaining question: is there any HIGH-severity structural miss? Let me re-scan our Duke one more time for the hover parameter flags:

```
let hoverT = DUKE.hoverT (60), hoverAcc = 0.45, hoverSpd = 7.5;
if (flag4) { hoverAcc = 0.7; hoverSpd = 12; hoverT = 30; }
else if (flag3 && flag5) { hoverAcc = 0.5; hoverSpd = 8; hoverT = 20; }
else if (flag5 && !flag3 && !flag4) hoverT = 30;
```
✓ matches classic columns.

chargeT/chargeSpd: 30/16; flag4 → 25/27; (flag5&&flag3 classic → 30/16 no change) ✓. enraged: hoverT=10, chargeSpd+=6 ✓.

BUT: original enraged also multiplies damage/defense — ours does (line 222) ✓. However ordering: ours computes `enraged` before the player-dead early-return; the damage assignment happens before too ✓. Note original computes flag6 AFTER the dead-check (with the possibly re-targeted player) — ours before; but if player null ours enraged=false and the dead branch handles it. Equivalent.

One more Duke check — case 3/8 sharknado hover: original `velocity *= 0.98; velocity.Y = Lerp(vy, 0, 0.02)` ✓ ours.

State 4 sound: `if (e.ai2 === DUKE.p1T - 60)` ✓ = 120.

State 9: ours plays sound at p2T-60=120 ✓; alpha handling `ai2 < p2T-90` ✓; else alpha += 4 clamp 255 ✓ (original `else if (alpha < 255) alpha += 4`).

State 13: rotation ✓; no bubbles ✓ (original state 13 has no bubble spawn ✓).

OK — and the expert state 10 pick: ours `(a3 === 0 || 2 || 3 || 5 || 6 || 7) ? 1 : 2` ✓.

Now — one more potential structural issue: ours `dukeFishronAI` doesn't implement TargetClosest on invalid target (original retargets when target dead/far before the despawn branch). Single-player equivalent. OK.

Alright — one more important verification: the Duke's rotation logic lines 252-257. Original:

```
if (rotation < num22) {
  if (num22 - rotation > PI) rotation -= num23; else rotation += num23;
}
if (rotation > num22) {
  if (rotation - num22 > PI) rotation += num23; else rotation -= num23;
}
if (rotation > num22 - num23 && rotation < num22 + num23) rotation = num22;
if (rotation < 0) rotation += 2PI;
if (rotation > 2PI) rotation -= 2PI;
if (rotation > num22 - num23 && rotation < num22 + num23) rotation = num22;
```

Ours:
```
let rot = e.spin;
if (rot < target) rot += (target - rot > Math.PI ? -step : step);
if (rot > target) rot += (rot - target > Math.PI ? step : -step);
if (rot > target - step && rot < target + step) rot = target;
if (rot < 0) rot += TAU; else if (rot > TAU) rot -= TAU;
if (rot > target - step && rot < target + step) rot = target;
e.spin = rot;
```
✓ identical.

Note original `if (rotation > MathF.PI * 2f)` without else — ours `else if` — same.

Also target num22 computed from player — with `if (st.spr === 1) target += Math.PI` ✓ (spriteDirection==1 → +PI) ✓.

OK. Now — final check on hand state -2 in ours: `handHover(e, core, side)` where original hovers to core+(350*side, -100) ✓. And damage=80 ✓.

Also ours hand -2 does NOT set `e.facing = side`... wait it's set before (line 1336 `e.facing = side`) ✓ spriteDirection = num1231 ✓.

Now, hand dontTakeDamage: ours `if (x.frame >= 21 || e.ai0 === -2) e.iframes = 2;` — but in ORIGINAL, dontTakeDamage is recomputed EVERY tick at top (`dontTakeDamage = frameCounter >= 21.0`) — i.e., when frame < 21 and not -2, dontTakeDamage is explicitly FALSE (can take damage). Ours: when frame < 21, we just don't set iframes → damage allowed ✓ (comment says保留 hurt() 的 8t 受击免疫). ✓.

But subtle: original `if (frameCounter == 19.0 && !dontTakeDamage) PopAllAttachedProjectilesAndTakeDamageForThem();` — not modeled. OK.

Let me now also confirm the exact original line numbers for the Lerp issue so my report cites real lines. Grep for "value2: new Vector2(0f, -0.5f)" and "value2: new Vector2(direction, -0.5f)".
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:22:31.170Z · glm-x-preview-260804

```
所有主要部分已验证。我来确定一下发现问题的确切原始行号。
```


---

## 🤖 Assistant · 2026-08-19T03:22:32.334Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"value2: new Vector2(0f, -0.5f)\\|value2: new Vector2(direction, -0.5f)\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head; grep -n \"Main.rand.Next(200) == 0\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | head -3",
 "description": "Locate Lerp named-arg lines and ambient sound line"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:32.370Z

**📎 ToolResult**

```
36928:				velocity = Vector2.Lerp(value2: new Vector2(0f, -0.5f), value1: velocity, amount: 0.98f);
37068:				velocity = Vector2.Lerp(value2: new Vector2(direction, -0.5f), value1: velocity, amount: 0.98f);
4281:						else if (!waterTile && num46 > Main.maxTilesX / 8 && (spawnTileType == 2 || spawnTileType == 147 || spawnTileType == 60 || spawnTileType == 161) && Main.rand.Next(200) == 0 && !AnyNPCs(696) && !AnyNPCs(695))
4917:					if (Main.hardMode && (Main.remixWorld || (double)spawnTileY > (Main.rockLayer + (double)Main.maxTilesY) / 2.0) && Main.rand.Next(200) == 0)
4922:					if ((Main.remixWorld || (double)spawnTileY > (Main.rockLayer + (double)Main.maxTilesY) / 2.0) && (Main.rand.Next(200) == 0 || (offensiveToTim && Main.rand.Next(50) == 0)))

```


---

## 🤖 Assistant · 2026-08-19T03:23:37.003Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line 36928 (state 2 death drama Lerp 0.98) and 37068 (state 3 flee Lerp 0.98). Confirmed.

Let me also double check the head -2 fall-through claim by looking at exact line numbers: head -2 branch :37782-37844; the frame advance num1285/num1286 at :38016-38049. And num1262=2 set inside the -2 leech block. From my read: in the -2 branch: `if (this.ai[2] >= 120f) { num1260 = ...; num1261 = 555f; num1262 = 2; ...`. Yes.

And our head -2 return: line 1549 (`return;`). Ours line numbers:
- head -2 block: 1534-1550.
- head -3 block: 1526-1533.
- Duke alpha clamp line 261.
- Core lerps: 1224-1225 (state 2), 1239-1240 (state 3).
- Core cleanup missing: state 2 block 1222-1236; state 3 block 1237-1248.
- Fallback mapping: case 1 lines 1275-1284; case 3 lines 1295-1298.
- Sharkron player-dead kill: line 764.
- Duke expert state 12 missing rotation flip: lines 430-438.

Now — one more sanity check on the "head -2 return" — does anything else run after the state ifs in ours? Looking at ours moonLordHeadAI structure: after the if-chain (ai0===0/1/2/3 blocks), there's the frame advance (1626-1632) and `e.spin = x.l0`. The -2/-3 branches `return` before those. So yes f2/f3 freeze. And e.spin = x.l0 not updated in -2 (original: rotation untouched in -2 → stays; -3: lerps to π/12). Ours -3 does lerp spin ✓; ours -2 leaves spin — original -2 leaves rotation ✓.

Actually wait — original -2 with num1262=2 → target frame f2=14 (mouth OPEN — the head残肢 opens its mouth to spawn leeches). Ours freezes f2 at whatever it was when the head died (likely whatever attack state — e.g. deathray slot has f2T=0 → f2 low). So the visual difference: mouth stays closed during leech loop. Cosmetic. OK.

Also one more consideration on finding #4 (missing projectile/eye cleanup): in ours, when the core enters state 2 (death), the head transitions -2→-3, and the head's -3 has `e.def.damage = 0` ✓. Hands stay -2 hovering with damage 80 ✓ (original same). True eyes (400, in bossAI_lunar_misc) presumably have their own core-death handling. So the cleanup gap mainly affects MoonLeechProj instances (continue flying until they return/expire — original kills 456s at ai1==60) and MLDeathray from core fallback. Low severity.

One more: ours core state 2 missing sound NPCDeath61 at ai1==1 (original :37045-37048 — `if (this.ai[1] == 1f) SoundEngine.PlaySound(SoundID.NPCDeath61...)`). Minor.

Also — did ours play 'Zombie_92' at the right time? Ours plays at end of -1 (ai1>=60, on part spawn). Original plays at ai1==30 (both -1 and -2). Minor timing; also ours misses it in -2. Cosmetic — I'll fold into the cleanup/sound finding or skip. I have enough findings.

Let me also double check finding #6 (fallback mapping) is really "wrong" vs vanilla by re-reading our case1 comment: "case 1: // 幻影之眼 452×4 扇形(:37326-37334)". :37326-37334 is the hand eye-ring single-shot code — not the true eye attack 1. True-eye attack 1 (slot [1,90]) = triple 462 @35 (:38347-38384). Ours case 3 does the 462 triple citing :38378-38383 — which is attack 1's code! So during a no-eyes fallback fight: slot cycle [0,90],[1,90],[0,90],[2,135],[0,90],[3,200],[0,90],[4,375],[0,90],[2,135]: ours would fire 452-fan at "1", spheres at "2", 462-triple at "3", deathray at "4". Vanilla eyes: 462-triple at "1", spheres at "2", 452-spiral-spin at "3", deathray at "4". So attack 1 is wrong (452 fan instead of 462 triple), attack 3 is wrong (462 triple instead of 452 spiral). CONFIRMED — but dormant when eyes spawn successfully. Note: our case-2 "redirect at 60" approximates the eye's sphere redirect (vanilla redirects at num1294==75 downward -7) — approximate but ballpark.

Severity: Medium-low (only matters if eyes missing). Actually — wait. Is there a scenario where eyes don't spawn? spawnPart(400) → NPC 400 exists (moonLordFreeEyeAI in Enemy.ts case 81) — wait, that's aiStyle 81 routing; spawnPart(game, part, 400) spawns enemy id 400 whose def has aiStyle 81 → routed to moonLordFreeEyeAI. So eyes normally spawn fine. The `eyes` check in core requires `n.ai3 === e.id` — spawnTrueEye sets eye.ai3 = part.ai3 = core.id ✓. So fallback is truly dormant. Low severity. But hmm — moonLordFreeEyeAI is in bossAI_lunar_misc.ts (another file) — out of scope, fine.

Now — priority ordering by severity:

1. Core flee/death Lerp 0.02 vs 0.98 (state 3 flee most visible; state 2 death drift). Medium.
2. Duke alpha clamp 255 vs 150 — Duke turns fully invisible inside tiles. Medium-low (actually this one's quite visible in gameplay: during sharknado hover the boss can overlap walls... the boss mostly stays in air; inSolid is center-point only. Hmm — visibility: alpha 150 vs 255. It'd matter when the Duke's center enters terrain, which happens when charging through walls? Duke charges with noTileCollide? Duke Fishron ignores tiles (noTileCollide true presumably). If our engine's Duke passes through terrain during charges, then inSolid triggers and the boss would vanish for stretches. That's a real visible bug.) Medium.
3. Head -2 early return skips mouth frame advance. Low.
4. Core death/flee missing projectile & true-eye cleanup at ai1 60/40 + missing drama sounds. Low.
5. Fallback barrage attack 1/3 mapping. Low (dormant).
6. Sharkron despawn-on-dead-player + missing lunge/death sounds. Low.
7. Duke expert state 12 missing spriteDirection rotation flip. Low (expert-only, currently unreachable since expert branch not gated in? wait — our duke case 9 is reachable only if dukePick2 returns 4, which requires flag2 = expert && hp<=15% — dukePick2 never returns 4 (commented out). So states 10-13 are unreachable in our build entirely. OK truly dormant).
8. Missing ambient sound for core (200-roll). Cosmetic — fold into 4? Keep separate tiny mention.
9. Bubble 371: justHit fallback + init redesign — fine. Skip.
10. Duke dead-player early return skips same-tick state machine — minor; maybe skip given 10-item cap.

Also PopAllAttachedProjectiles — skip (engine has no attached projectiles presumably).

Hmm, wait — one more thing worth double-checking: our dukeBubbleAI handles `e.ai3 <= 0` gating for init — bubbles spawned by Duke case 7 preset ai3 = (80+rand*41)/100 ✓ ≥ 0.8 > 0 → skips re-init ✓ good.

And sharkronAI init: spawned with bInit=false → bInit sets ai0=0,ai1=0 — but tornado preset ai2/ai3 BEFORE... ours tornado sets `shark.bInit = false` and ai2/ai3 — then sharkronAI init sets ai0/ai1 only ✓ preserves ai2/ai3 ✓.

But note: sharkron 373 needs spawnAlpha to start at 255 and fade to 0 (invisible→visible). Ours sets `e.spawnAlpha = 255` at init ✓.

One more: ours sharkron `if (!player || player.dead) { e.dead = true; return; }` — original: retarget; direction=1... with all players dead, TargetClosest leaves target... then ai0==1 branch does `Main.player[target].Center` — if target==255 → Main.player[255] exists (dummy). Sharks would fly toward (0,0)-ish. Ours despawns. For single player, player.dead → ours kills sharks instantly. Vanilla keeps them until they hit walls/timeout. Minor behavioral diff in death scenarios. Keep as low finding.

Let me also spot-check one numeric: DUKE.hoverT classic 60 ✓ (num3 = 60 classic) ✓. Enraged hoverT=10 ✓ (num3=10).

I think I have my list. One more possible check: our `attackSlot` wrap behavior — when ai1 lands exactly at 1200 (total), loop consumes all → slot===length → wrap. But note: ai1=1200 tick: all slots consumed (1200<=1200) → wrap to slot 0, ai1=0, inSlot=0 → atk 3 fires 462 immediately (slot 0's attack continues as if fresh). Vanilla identical (num1267==5 → wrap). ✓.

Also the head: our `if (e.ai0 >= 0) { e.ai1 += 1; ... }` — original `if (this.ai[0] >= 0f)` ✓.

Hand: original `if (this.ai[0] != -2f)` — ours `if (e.ai0 !== -2)` ✓.

Done. Also the "存疑" bucket:
- Tornado single-entity tower approximation (documented, contact damage column box) — deliberate.
- Hand state 2 inSlot>=292 redirect approximation (6 fresh 454s) — deliberate, documented.
- ML_CORE_P2 case 2 (spheres) approximation.
- MoonLeechProj initial speed 6 vs vanilla 1 (from head -2) / whatever from state 2 — initial speed barely matters since AI takes over at min(16,d) next tick. Note: ours first fixedUpdate overrides velocity anyway. Actually — ours sets vx/vy in constructor (speed 6) and then AI recomputes every tick. Vanilla first AI tick also recomputes. So initial speed irrelevant. Skip.
- spawnTrueEye: NewNPC position semantics (top-left vs center) — ours subtracts half-size; vanilla NewNPC uses position directly (top-left). So ours places the eye half-width off from vanilla. Given hands/head spawn also use center-offset convention consistently, and eyes then run their own anchoring AI (which positions them near core), negligible. Skip/mention.

Now, regarding the biggest question — is there anything HIGH severity? Honestly the port is remarkably faithful. The Lerp one is the most "wrong-parameter" bug. The Duke alpha clamp is a visible one. I'll present in ranked order with confidence levels.

Let me get our exact line numbers once more for each:
1. Core Lerp: ours 1224-1225 (state2), 1239-1240 (state3). Original 36928, 37068.
2. Duke alpha: ours 261. Original :49352-49363 (the clamp block). Let me cite 49346-49363.
3. Head -2 return: ours 1534-1549 (return at 1549), also -3 return at 1532. Original -2: 37782-37844 (num1262=2 at ~37803), frame advance 38016-38049.
4. Core cleanup: ours 1222-1236 / 1237-1248. Original ai1==60 kill: 36940-36952; ai1==40: 37129-37140; NPCDeath61: 37045-37048; -1/-2 Zombie_92 at ai1==30: 36789-36792 / 36813-36816.
5. Fallback mapping: ours 1275-1299. Original true-eye atk1: 38347-38384; atk3: 38508-38574.
6. Sharkron: ours 764. Original 35196-35210.
7. Duke state 12: ours 430-438. Original 50083-50097.
8. Core ambient sound: ours whole moonLordCoreAI. Original 36775-36778.

Wait — I should double check #4's exact line numbers. The ai1==60 block within state 2: from my sed dump starting 36930: "if (this.ai[1] == 60f)" appeared after `MoonlordDeathDrama.RequestLight(this.ai[1] / 60f...)`. Line numbers: 36930 was "if (this.ai[1] < 60f)". So RequestLight ~36931, `if (this.ai[1] == 60f)` ~36935. Projectile kill loop ~36936-36947, NPC 400 kill ~36948-36956. Let me grep exact.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:23:38.081Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"if (this.ai\\[1\\] == 60f)\\|if (this.ai\\[1\\] == 40f)\\|NPCDeath61\\|if (this.ai\\[1\\] == 30f)\" \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs\" | awk -F: '$1>36700 && $1<37200'",
 "description": "Locate exact cleanup/sound line numbers in core"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:23:38.113Z

**📎 ToolResult**

```
36790:				if (this.ai[1] == 30f)
36798:				if (this.ai[1] == 60f)
36814:				if (this.ai[1] == 30f)
36822:				if (this.ai[1] == 60f)
36934:				if (this.ai[1] == 60f)
37051:					SoundEngine.PlaySound(SoundID.NPCDeath61, base.Center);
37074:				if (this.ai[1] == 40f)

```


---

## 🤖 Assistant · 2026-08-19T03:24:03.185Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed:
- state -2: sound at ai1==30 (36790), transition at 36798.
- state -1: sound at ai1==30 (36814), spawn at 36822.
- state 2: projectile/eye cleanup at ai1==60 (36934).
- NPCDeath61 at 37051 (inside ai1==1 check at 37049-37052).
- state 3: cleanup at ai1==40 (37074).

Also confirm the alpha clamp line numbers for Duke: the block was in my second read starting 49270. `if (ai[0] != -1f && ai[0] < 9f)` then SolidCollision alpha += 15 else -= 15, clamp 0/150. From dump: after the rotation code. The dump 49270-49415 shows the block — `if (ai[0] != -1f && ai[0] < 9f)` appeared at approximately line 49346 (matches our comment :49346-49364). Good, trust the comment (it aligned with everything else).

Now write the final report. Keep to ≤10 findings, ranked by severity, each with both file:line refs, symptom, minimal fix, confidence.

Findings list final:

1. 月总核心 死亡演出/玩家全灭离场速度 Lerp 步长 0.02 vs 原版 0.98 (named-args 误读) — ours:1224-1225/1239-1240 vs cs:36928/37068. 置信度高. Severity medium.

2. 猪鲨体内透明度钳 255 vs 150 — ours:261 vs cs:49346-49363. 高.

3. 月总头 -2 残肢提前 return,漏帧推进(月噬循环张嘴 f2 恒不开) — ours:1534-1549 (return 1549) vs cs:37782-37844(num1262=2)+38016-38049. 高. Also -3 return at 1532 vs fall-through — but ours -3 手动推 f2 到 14 与原版净零振荡不同 — 原版 -3 是 ++ 然后 -- (净冻结), ours 爬到 14。把 -3 的差异并进这条说明。

4. 月总核心 ai0=2/3 漏 ai1==60/40 的弹幕+真眼清除(456/462/455/452/454 + NPC400)及 NPCDeath61/Zombie_92(ai1==30)音效 — ours:1222-1248 vs cs:36934-36956/37074-37084/37049-37052/36790. 高.

5. 核心二阶段兜底弹幕攻击号映射错位(1↔3):case1 应为三连462@35(cs:38347-38384),case3 应为 452 旋射@35(cs:38508-38574);现 case1 是自造 452 扇形(引用的是手部 :37326)、case3 重复了攻击1代码 — ours:1275-1299. 高(映射错)/影响低(真眼存在时休眠).

6. 鲨鱼龙 372/373 玩家死亡即消散(原版重定向继续飞)+缺起扑音 PlaySound(4,19) 与撞墙死亡音 — ours:764 vs cs:35196-35210/35238-35252(:35248). 高. Let me get the sound line: from the 35122 dump: "SoundEngine.PlaySound(4, (int)base.Center.X, (int)base.Center.Y, 19);" inside the ai1>=90 transition — that was around 35245-35250. And death sound at the SolidCollision death ~35290. Fine, cite ranges.

7. 猪鲨 expert 状态12瞬移缺 spriteDirection 翻转补偿 rotation+=π — ours:430-438 vs cs:50083-50097. 高/expert-only休眠.

8. 月总核心缺随机环境吼叫(200掷 PlaySound(29, 93-99)) — ours moonLordCoreAI 全函数 vs cs:36775-36778. 高. Cosmetic.

Maybe also mention: Duke 死亡/远离分支 return 跳过当 tick 状态机(原版继续跑) — low confidence relevance... I verified original continues. Symptom: charge 中玩家死亡时猪鲨水平速度保留但不再位移 (ours return 前手动 x+=vx,y+=vy! wait — ours lines 240: `e.x += e.vx; e.y += e.vy;` INSIDE the dead branch before return. So it does move with full velocity! OK so that's actually handled. The only diff: original state machine could run for ai0 in {1,2,...} etc. — mostly no-ops with dead player except charge states continue dust+counters. Negligible → drop.

Also worth a 存疑 bucket: documented approximations (tornado tower single-entity; hand 454 redirect→补射6发; ML_CORE_P2 case2; spawnTrueEye/MoonLeechProj 位置与出速细节; PopAllAttachedProjectiles 未建模)。

Also positive summary: everything else checked clean — list briefly.

Format: 逐 Boss 一节. Max 10 findings. I have 8. Good.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:46.062Z · glm-x-preview-260804

```
审计完成。以下为按 Boss 分节的结论。

# DukeFishron(370 / 371 / 372-373 / 385 / 384·386)

**核了什么**：AI_069 全 14 状态(cs:49143-50128)逐段对照——出生/悬浮/冲撞/泡泡/双龙卷/半血变身/二阶段循环/旋转冲刺/expert 10-13 段、狂暴 flag6 判据与数值覆盖顺序、旋转体代码、无敌门、flee 分支；弹桶 385(aiStyle 65)、龙卷塔 384/386(aiStyle 64 + Kill:70714)、鲨鱼 372/373(aiStyle 71)、泡泡 371(aiStyle 70)。

**结论**：状态机/计时器/速度档/弹幕 id·速度·计数·间隔、`attackSlot` 槽表推进(含 inSlot 从 0 起的边界语义)、半血→4、狂暴泡泡换龙卷、expert 二段变身门(flag2 经典不可达，与原版一致)、flee(y-=0.4 + ai0 归位 + EncourageDespawn(10))、传送龙卷弹参数、杀鲨节奏(小模4/大模2、373 ai2=width/ai3=-1.5)全部对上。发现 2 处偏差(见汇总 #2/#6/#7)。

# MoonLord 核心 398(aiStyle 77)

**核了什么**：cs:36774-37198 全段 + checkDead:78841-78867 + MoonLordAttacksArray:6830-6990。状态 -2/-1/0/1/2/3、双手死前无敌(dontTakeDamage @36856)、三部件全 -2 才进二阶段(flag85)、部件缺失即毁(flag84)、死亡演出 600t、玩家全灭 ai0=3、>2400px 全族传送。

**结论**：结构全对，含攻击表数值(与 cs:6854-6883/6874-6883 逐槽核对为零差)。偏差：死亡/离场速度 Lerp 步长(汇总 #1)、演出期弹幕/真眼清除缺失(汇总 #4)、环境吼叫缺失(汇总 #8)、二阶段兜底弹幕攻击号错位(汇总 #5,真眼存在时休眠)。

# MoonLord 手 397(aiStyle 78)

**核了什么**：cs:37199-37711 全段。攻击表(ai2=0/1 两套，数值零差)、四攻击(452 环射椭圆/454 扫射+末段转向/462 三连预判 20t)、SimpleFlyMovement+半程 Lerp 混合、位置钳制盒(220+110→+370,-60-150→+150)、frameCounter→dontTakeDamage≥21 睁眼可击窗口、-2 残肢悬停(350·side,-100)伤 80、死 switch(num1250) 死代码确认。

**结论**：1:1。仅 454 末段“原弹转向”被近似为补射 6 发(文件内已备案，幅度合理——原版也恰是 6 发转向、12 速)。

# MoonLord 头 396(aiStyle 79)

**核了什么**：cs:37712-38128 全段。攻击表 [3,180/0,30/2,435/3,180/1,375] 零差、死亡之光起角 ∓60°+编码角逐 t 解码、月噬 456(额前 216)+401 召唤门(FindBuffIndex 145,单玩家等价替换已备案)、462 三连、FTW 尾段 30 连射 1021(含“跌破 0 后连发”原版语义)、f3≥15 闭眼无敌、-2→-3 核死永闭。

**结论**：除汇总 #3(残肢提前 return)外 1:1,含反编译 localAI[2]/[3] 钳制笔误的语义化处理。

---

## CONFIRMED 偏差(按严重度)

1. **月总核心死亡/离场速度 Lerp 步长 0.02 应为 0.98**(命名参数误读)
 我方 `bossAI_duke_moonlord.ts:1224-1225`(ai0=2)与 `:1239-1240`(ai0=3)/ 原版 NPC.cs:36928、37068 —— `Vector2.Lerp(value1: velocity, value2: (direction,-0.5), amount: 0.98f)` 即每 tick 98% 逼近目标速；我方写 `lerp(v, target, 0.02)`,收敛慢 ~50 倍。症状：死亡演出 10 秒内几乎悬停(原版以 0.5px/t 上浮 ~300px);玩家全灭离场 60t 内横移≈0(原版立即以 ±1px/t 横漂)。修复：两处 0.02→0.98。置信度：高。

2. **猪鲨地形内透明度钳 255 应为 150**
 我方 `:261` / 原版 ：49346-49363(`alpha > 150 → 150`)。症状：猪鲨(穿墙冲锋/龙卷悬停)中心进实心块后整体隐身消失，原版只淡到半透明残影。修复:`Math.min(255,…)`→`Math.min(150,…)`。置信度：高。

3. **月总头 -2 闭眼残肢提前 return,漏帧推进**
 我方 `:1534-1549`(尤其 1549 的 `return`)/ 原版 ：37782-37844 无 return,且月噬循环段置 `num1262=2`(:37803 附近)使 f2 目标=14(张嘴),再落入 ：38016-38049 帧推进。症状：残肢期月噬循环时嘴部帧永不开合(f2/f3 冻结在死亡瞬间值)。附带：我方 -3 分支(`:1526-1533`)手动把 f2 爬到 14,而原版 -3 是 `if(localAI[2]<14) localAI[2]++` 后又被帧推进 `--` 抵消=净冻结——两边终态不同但同属退化外观。修复：去掉 -2 的 return,把 f2T=2 挂到 `e.ai2 >= 120` 分支并让帧推进统一执行。置信度：高。

4. **核心 ai0=2/3 漏 ai1==60/40 的弹幕与真眼清除及演出音效**
 我方 `:1222-1248` 无对应 / 原版 ：36934-36956(死亡演出 ai1==60:Kill 全部 456/462/455/452/454 + 清 NPC400)、:37074-37084(离场 ai1==40 同款)、:37049-37052(ai1==1 播 NPCDeath61)、:36790/:36814(-2/-1 段 ai1==30 播 style92,我方错排在 ai1==60 部件生成时)。症状：死亡演出 10 秒内残存月噬弹/死光继续索敌，离场清场不干净；开场/死亡吼叫时机偏移。修复：在两状态按 ai1 补清除(遍历 `game.enemies()` 中 ai3===id 的 400 与 projectiles 桶中的 MLDeathray/MoonLeechProj)并补音效点。置信度：高。

5. **二阶段兜底弹幕攻击号映射错位(1↔3)**
 我方 `:1275-1299`:case1=自造“452×4 扇形”(引用 ：37326-37334 实为**手部**环射单发)、case3=三连 462(引 ：38378-38383)。原版真眼(aiStyle 81)攻击 1=三连 462@35(cs:38347-38384)、攻击 3=**452 旋射**@35(cs:38508-38574,自旋瞄准轮射)。症状：仅当 NPC400 出生失败走兜底时，槽 1 漏 462 三连、槽 3 打成 462 而非 452 旋射。修复：case1 改三连 462@35(inSlot=dur-14/-7/dur),case3 改 452 旋射。置信度：高(映射)；影响低(真眼常在，兜底休眠)。

6. **鲨鱼龙玩家死亡即消散 + 缺起扑/撞墙音**
 我方 `:764`(`!player||dead → e.dead=true`)/ 原版 ：35196-35210 为重新 TargetClosest 继续存活，起扑时 ：35248 `PlaySound(4,…,19)`,撞墙死亡播 DeathSound(:35290 附近)。症状：玩家死亡瞬间全场鲨鱼消失(原版继续扑咬尸体位置直至撞墙/超时)；起扑/死亡静默。修复：死亡门改为保留 + 朝最后玩家位置直飞，补两处音效。置信度：高。

7. **猪鲨 expert 状态 12 瞬移缺朝向翻转补偿**
 我方 `:430-438` / 原版 ：50083-50097:瞬移后 `if (spriteDirection != -direction) rotation += π`。我方只改 dir/spr 不加 π。症状：瞬移后贴图倒挂一拍(仅 expert,当前经典模式该状态不可达)。修复：翻转时 `e.spin += Math.PI`。置信度：高。

8. **月总核心缺随机环境吼**
 我方 `moonLordCoreAI` 全函数无 / 原版 ：36775-36778:`ai0 != -1 && != 2` 时每 tick 1/200 掷 `PlaySound(29, Next(93,100))`。修复：状态 0/1/-2 内补 1/200 随机吼。置信度：高。

## 存疑/已备案近似(不计偏差)

- 龙卷塔单实体化(段生长/出鲨/摇摆公式均对，判定盒为整列近似)——文件头已备案。
- 手 454 末段转向→补射 6 发、ML_CORE_P2 case2 球转向近似、spawnMoonLeech 单玩家门等价、spawnTrueEye/部件落位半宽偏移(NewNPC 传参语义)——均有备案注释，幅度可接受。
- `PopAllAttachedProjectilesAndTakeDamageForThem`(手 frame==19/头 f3==13,cs:37212/37717)未建模，本仓无附着弹机制，判定无影响。
- 验证过 `world.groundLevel` 为 tile 坐标(World.ts:161),猪鲨狂暴阈值 `groundLevel*TILE ≡ worldSurface*16` 成立;`accelTo` ≡ SimpleFlyMovement 含符号翻转双步进。

总体评价：两 Boss 族移植质量很高——攻击表、计时边界(inSlot 从 0 起)、椭圆锚点、编码角解码、FTW 连发语义、named-args Lerp 以外的全部数值均与 1456 逐行一致；上述 8 条中仅 #1/#2 会在正常游玩中直接可见。
```
