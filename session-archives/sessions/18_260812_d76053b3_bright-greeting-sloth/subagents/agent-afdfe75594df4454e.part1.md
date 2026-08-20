# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T03:09:57.587Z

```
你在 ~/Project/GLM/SandboxWorld 做泰拉瑞亚 1.4.5.6 复刻的 Boss AI 1:1 抽查审计。**严格只读:禁止编辑任何文件、禁止跑游戏/vite/测试。**

标杆(唯一权威):~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs(96369 行)
我方:~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts

背景:我方是手工移植;注释里 "cs:NNNNN"/"NPC.cs:NNNNN" 就是这份 NPC.cs 的行号。我方 ai0..ai3 = 原版 npc.ai[0..3],localAI ≈ localAI[i]。专家门:mainExpertMode() ≈ Main.expertMode。

你负责审计整个文件(月总部件+拜月教仪式+月亮事件四塔专属怪)。重点(按优先级):
1. moonLordFreeEyeAI(月总游离眼 400,aiStyle 81 @38224-38667):十槽攻击表+死光充能
2. moonLeechAI(水蛭块 401,aiStyle 82 @38668-38792):90t 插值吸血回灌
3. cultistTabletAI(神秘石碑 437,aiStyle 83 @38793)+lunaticDevoteeAI(忠实信徒 438)+cultistArcherStandbyAI:仪式链
4. phantomAI(暗焰幻影 472/远古幻影 521,aiStyle 86 @39261-39519):穿墙横掠循环
5. bigMimicAI(珍稀宝箱怪 473-476,aiStyle 87 @39520-39875):跳扑+蓄能/俯冲/三连扑
6. mothronAI(飞蛾魔 477,aiStyle 88 @39876-40406)/mothronEggAI(478)/babyMothronAI(479)
7. graniteElementalAI(483,aiStyle 91 @40686)、星璇塔四组怪:starCellAI(405/421,aiStyle 85 @38967)、smallStarCellAI(406,aiStyle 95 @41445)、flowInvaderAI(407/408,aiStyle 96 @41493)、nebulaFloaterAI(420,aiStyle 97 @41536)、solarSlimeAI(519,aiStyle 99 @41997)、crawltipedeAI(412,aiStyle 6 内专属段 @51357-52671)

审计维度(抓结构性偏差,不是数值噪音):阶段缺失/转换条件错/速度档错/专家分支漏/弹幕 id-计数-速度错/flee 或事件结束语义无出处/链体联动错。

方法:先 Read 我方对应函数,再 sed -n '起,止p' 读原版对应段对照,不要泛读全文(文件 94KB,别整读)。注释声称的行号要抽验(注释可能撒谎/过时)。

输出格式(最终回复直接文本,不写文件):
逐族一节:"核了什么+发现什么"。每条 CONFIRMED 偏差给:我方文件:行号 / 原版 NPC.cs 行号 / 症状 / 最小修复建议 / 置信度(高/中/低)。没问题的族一句话带过。存疑单列。最多报 10 条,按严重度排序。禁止编造行号——每条 CONFIRMED 必须两边都真实读过。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T03:09:57.590Z

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

## 🤖 Assistant · 2026-08-19T03:10:03.503Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by reading the target file (our implementation) and the relevant sections of the vanilla NPC.cs. The task is a read-only audit of bossAI_lunar_misc.ts against Terraria 1.4.5.6 NPC.cs.

Plan:
1. Read ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts fully (it's probably large, but let me read it in chunks).
2. For each AI family, read the corresponding vanilla section with sed.

Let me start.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:03.628Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Count lines in both files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:03.659Z

**📎 ToolResult**

```
    1929 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts
   96369 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs
   98298 total

```


---

## 🤖 Assistant · 2026-08-19T03:10:07.208Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The file is 1929 lines. Let me read it fully in two chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:07.259Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts",
 "limit": 1000
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:07.455Z

**📎 ToolResult**

```
1	// 月系批 AI 家族 1:1 移植(Terarria1456, 1.4.5.6)：
2	//   aiStyle 81  月总游离眼 400            NPC.cs:38224-38667（攻击表 MoonLordAttacksArray2
3	//                                              :6966-6985 十槽循环:悬停/幻影矢 462/幻影球 454
4	//                                              六角螺旋/幻影眼 452 洒射/死亡之光 455;锚核心 398
5	//                                              ai[3],核心亡→静默消散;SetDefaults dontTakeDamage
6	//                                              =true → 恒无敌）
7	//   aiStyle 82  月总水蛭块 401            NPC.cs:38668-38792（ai[2] 90t 从弹着点插值飞向
8	//                                              头额(0,+216);到位把 1000 点治疗按
9	//                                              头396→核心398→手397(ai2=0)→手(ai2=1) 亏血序回灌）
10	//   aiStyle 83  神秘石碑 437/忠实信徒 438  NPC.cs:38793-38962（石碑 CheckFloor 落地校验后召
11	//                                              4 教徒(379×2 外侧/438×2 内侧,ai[3]=-(碑id+1));
12	//                                              信徒受击→石碑 localAI[0]=1→弓手激活;四教徒全灭
13	//                                              →侧面落点召 439 邪教徒 + 300t 仪式倒计时消散）
14	//   aiStyle 86  暗焰幻影 472/远古幻影 521  NPC.cs:39261-39519（穿墙横掠→越过 660/500px 掉头
15	//                                              →回摆循环;521 全参数强化(0.7/14/500/6/3)+
16	//                                              228 号紫雾拖尾;出生 120t 显形爆发音 Item8）
17	//   aiStyle 87  珍稀四宝箱怪 473-476       NPC.cs:39520-39875（ai[0] 0 伪装箱→1 蓄力 36t→
18	//                                              2 贴地跳扑(每 210t 随机 3 蓄能无敌 180t/
19	//                                              4 飞天俯冲/6 三连扑,每第 3 跳双倍高度);
20	//                                              7 玩家死→零伤满血渐隐;8 十周年世界炮连发不可达）
21	//   aiStyle 88  飞蛾魔 477                NPC.cs:39876-40406（日食限定;-1 无日食爬升无敌/
22	//                                              0 悬顶伺服 180t 轮换 2 追击(×0.5 伤)/3 侧掠
23	//                                              冲刺(3.2 ×1.3 伤)/4 扫地产卵 478(上限 7 只)）
24	//   aiStyle 89  蛾卵 478                  NPC.cs:40407-40449（900t(专家 600)→Transform 479;
25	//                                              受击 -10..20×2 孵化加速;末期 75% 抽搐跳）
26	//   aiStyle 90  幼蛾 479                  NPC.cs:40450-40685（日食限定;-1 爬升/0 悬停 90t→
27	//                                              2 贴脸 10t 瞄准→2.1 冲刺;无日食→上浮消散）
28	//   aiStyle 91  花岗岩元素 483            NPC.cs:40686-40870（AI 自置 noGravity=true;穿墙追击/
29	//                                              侧移锚点/漂移弹壁,与 AI_085 同构五态寻路）
30	// 去重核实(任务卡勘误):aiStyle 84 ≠ 月总死光——84 = 拜月教邪教徒 439/克隆体 440
31	//   (NPC.cs:38963-38966 → AI_084_LunaticCultist :64921,Enemy.ts case 84 已落位);
32	//   "月总死光"是投射物 455 PhantasmalDeathray(本批 aiStyle 81 状态 4 发射,复用
33	//   bossAI_duke_moonlord 导出的 MLDeathray 类 'core' 档)。星璇塔四组专属怪
34	//   aiStyle 85/95/96/97/99（405/421/406/407(/408)/420/519）已在本文件 1:1 落位
35	//   （文件尾段），Enemy.ts 一期近似档（swarmerAI/casterAI）退役；421 头顶吸附的
36	//   Obstructed(buff 163)已实装（每 tick AddBuff 续期 + Renderer 遮屏滤镜）。
37	// 弹幕贴图 Projectile_{452,454,462}.png 已入 sprites/vanilla(原 RENDER_PROXY 代渲退役,
38	//   见 shootL 注释);455 走 MLDeathray 类自绘;526 仪式粒子有贴图但带 ai[0..1] 归巢弹道,降级为粒子。
39	import type { Enemy } from './Enemy';
40	import type { GameHooks } from './types';
41	import type { Player } from './Player';
42	import { TILE, GRAVITY, MAX_FALL_SPEED } from '../core/constants';
43	import { BuffType } from '../stats/Buffs';
44	import { moveAndCollide } from '../physics/TileCollision';
45	import { spawnPart, losClear, enemySpawnChain, addEnemy } from './bossAI';
46	import { Arrow } from './Arrow';
47	import { projFrameImg } from './Arrow';
48	import { Entity } from './Entity';
49	import { canHitLine } from '../physics/LineOfSight';
50	import { MLDeathray, type NetProjMeta } from './bossAI_duke_moonlord';
51	import type { Renderer } from '../render/Renderer';
52	import type { Camera } from '../render/Camera';
53	
54	/** 原版 localAI[0..3](Enemy 只有 ai0-ai3,localAI 独立 → WeakMap 落盘) */
55	const localAI = new WeakMap<Enemy, number[]>();
56	export const lunarLocalAI = (e: Enemy): number[] => {
57	  let a = localAI.get(e);
58	  if (!a) { a = [0, 0, 0, 0]; localAI.set(e, a); }
59	  return a;
60	};
61	const TAU = Math.PI * 2;
62	const rnd = (n: number): number => Math.floor(Math.random() * n);
63	const rndRange = (a: number, b: number): number => a + Math.floor(Math.random() * (b - a));
64	const clamp = (v: number, lo: number, hi: number): number => (v < lo ? lo : v > hi ? hi : v);
65	const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;
66	/** 最短弧插值(原版 MathHelper 曲线角度语义) */
67	const angleLerp = (a: number, b: number, t: number): number => {
68	  let d = b - a;
69	  while (d > Math.PI) d -= TAU;
70	  while (d < -Math.PI) d += TAU;
71	  return a + d * t;
72	};
73	/** 朝目标角按最大步长逼近(原版 AngleTowards) */
74	const angleTowards = (a: number, b: number, maxStep: number): number => {
75	  let d = b - a;
76	  while (d > Math.PI) d -= TAU;
77	  while (d < -Math.PI) d += TAU;
78	  return Math.abs(d) <= maxStep ? b : a + Math.sign(d) * maxStep;
79	};
80	/** expert 门(本工程恒 false,Game.ts expertMode:false) */
81	const EXPERT = false;
82	/** 直积分(原版 noTileCollide 族;NPC.cs UpdateNPC :91400 段共享位移的穿墙分支) */
83	const fly = (e: Enemy): void => { e.x += e.vx; e.y += e.vy; };
84	
85	const enemies = (game: GameHooks): Enemy[] => game.enemies() as Enemy[];
86	const countNpc = (game: GameHooks, id: number): number =>
87	  enemies(game).filter((n) => !n.dead && n.vanillaId === id).length;
88	
89	/** 矩形区域含实心(Collision.SolidTiles 近似) */
90	function solidRect(game: GameHooks, x0: number, y0: number, x1: number, y1: number): boolean {
91	  const st = game.world.store;
92	  for (let x = x0; x <= x1; x++) {
93	    for (let y = y0; y <= y1; y++) {
94	      if (x < 0 || y < 0 || x >= st.w || y >= st.h) continue;
95	      if (st.isSolid(x, y)) return true;
96	    }
97	  }
98	  return false;
99	}
100	/** 身体完全埋入实心(Collision.SolidCollision 近似) */
101	function inSolidBody(game: GameHooks, e: Enemy): boolean {
102	  const st = game.world.store;
103	  for (let tx = Math.floor(e.x / TILE); tx <= Math.floor((e.x + e.w - 0.01) / TILE); tx++) {
104	    for (let ty = Math.floor(e.y / TILE); ty <= Math.floor((e.y + e.h - 0.01) / TILE); ty++) {
105	      if (tx < 0 || ty < 0 || tx >= st.w || ty >= st.h) return false;
106	      if (!st.isSolid(tx, ty)) return false;
107	    }
108	  }
109	  return true;
110	}
111	function solidTileAt(game: GameHooks, x: number, y: number): boolean {
112	  const st = game.world.store;
113	  return x >= 0 && y >= 0 && x < st.w && y < st.h && st.isSolid(x, y);
114	}
115	
116	// ---------------------------------------------------------------------------
117	// 弹幕出口:452 PhantasmalEye / 454 PhantasmalSphere / 462 PhantasmalBolt 贴图
118	// Projectile_{452,454,462}.png 已按 601/602 先例补入 sprites/vanilla(Arrow 按 projId
119	// 懒加载真图),原 EnchantedBeam 173 代渲登记退役。454/452 的原版归巢弹道
120	// (弹 ai[0] 标记 + ai[1]=源 NPC)Arrow 无 ai 槽,不实装(按发射初速直飞)。
121	// ---------------------------------------------------------------------------
122	function shootL(
123	  game: GameHooks, x: number, y: number, vx: number, vy: number,
124	  dmg: number, projId: number, life = 300,
125	): void {
126	  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
127	    new Arrow(x, y, vx, vy, dmg, 0, projId, null, { grav: 0, life, pierce: 1, hostile: true }),
128	    'projectiles');
129	}
130	
131	// ---------------------------------------------------------------------------
132	// AI_081 月总游离眼 400(NPC.cs:38224-38667)
133	// 攻击表 MoonLordAttacksArray2(:6966-6985)十槽循环,ai[1] 为全局计时逐槽累计:
134	//   [悬停90, 矢90, 悬停90, 球135, 悬停90, 眼200, 悬停90, 光375, 悬停90, 球135]
135	// localAI[0]=瞳孔角 [1]=睁眼度 [2]=缩放;ai[2]=球的扫射编码角/眼的螺旋角。
136	// 注意:原版 ai[0]==-1 分支(:38284)在表驱动下不可达(表值仅 0..4),不移植。
137	// ---------------------------------------------------------------------------
138	const ML_EYE_ATTACKS: ReadonlyArray<readonly [number, number]> = [
139	  [0, 90], [1, 90], [0, 90], [2, 135], [0, 90], [3, 200], [0, 90], [4, 375], [0, 90], [2, 135],
140	];
141	
142	export function moonLordFreeEyeAI(e: Enemy, game: GameHooks, player: Player | null) {
143	  // :38227 PlaySound(29,…,Next(100,101))——含头不含尾=恒 100 → Zombie_100,
144	  // case29 style100 ×0.25 由 FILE_CASE_VOL 自动乘(曾借 roar 轨 0.15,2026-08-18 对账修)
145	  if (rnd(420) === 0) game.playSfxWav?.('Zombie_100', 1, e.cx, e.cy);
146	  // ---- 核心锚定(:38231-38237):ai[3]=核心 id,亡→静默消散 ----
147	  const core = enemies(game).find((n) => n.id === e.ai3 && n.vanillaId === 398);
148	  if (!core || core.dead) { e.dead = true; return; }
149	  e.iframes = 2;                        // SetDefaults dontTakeDamage=true(:14090)
150	
151	  // ---- 攻击表推进(:38240-38264) ----
152	  const x = lunarLocalAI(e);
153	  e.ai1 += 1;
154	  let slot = 0, consumed = 0, dur = 0;
155	  for (; slot < 10; slot++) {
156	    dur = ML_EYE_ATTACKS[slot][1];
157	    if (!(dur + consumed <= e.ai1)) break;
158	    consumed += dur;
159	  }
160	  if (slot === 10) { slot = 0; e.ai1 = 0; consumed = 0; dur = ML_EYE_ATTACKS[0][1]; }
161	  e.ai0 = ML_EYE_ATTACKS[slot][0];
162	  const t = e.ai1 - consumed;           // num1294 槽内已历时
163	  const pcx = player ? player.cx : e.cx, pcy = player ? player.cy : e.cy;
164	
165	  if (e.ai0 === 0) {
166	    // ---- 悬停(:38309-38345):玩家上方 200px 伺服(24 速/30 步进) + 同族 150px 排斥 ----
167	    if (player) e.facing = e.seekDirX(player);
168	    const dx = pcx + (player ? player.vx : 0) * 20 - e.cx;
169	    const dy = pcy + (player ? player.vy : 0) * 20 - e.cy;
170	    x[0] = angleLerp(x[0], Math.atan2(dy, dx), 0.5);
171	    x[1] = Math.min(0.7, x[1] + 0.05);
172	    x[2] = lerp(x[2], 1, 0.2);
173	    let tx = pcx - e.cx, ty = pcy - 200 - e.cy;
174	    const d = Math.hypot(tx, ty) || 1;
175	    tx = (tx / d) * 24; ty = (ty / d) * 24;
176	    e.vx = (e.vx * 29 + tx) / 30;
177	    e.vy = (e.vy * 29 + ty) / 30;
178	    for (const n of enemies(game)) {                      // :38327-38345
179	      if (n !== e && !n.dead && n.vanillaId === 400
180	        && Math.hypot(n.cx - e.cx, n.cy - e.cy) < 150) {
181	        if (e.x < n.x) e.vx -= 0.25; else e.vx += 0.25;
182	        if (e.y < n.y) e.vy -= 0.25; else e.vy += 0.25;
183	      }
184	    }
185	  } else if (e.ai0 === 1) {
186	    // ---- 幻影矢 462(:38347-38395):减速瞄准,dur-14/-7/dur 三连(35 伤,速 8) ----
187	    if (t === 0 && player) e.facing = e.seekDirX(player);
188	    e.vx *= 0.95; e.vy *= 0.95;
189	    if (Math.hypot(e.vx, e.vy) < 1) { e.vx = 0; e.vy = 0; }
190	    const dx = pcx + (player ? player.vx : 0) * 20 - e.cx;
191	    const dy = pcy + (player ? player.vy : 0) * 20 - e.cy;
192	    x[0] = angleLerp(x[0], Math.atan2(dy, dx), 0.5);
193	    x[1] = Math.min(1, x[1] + 0.05);
194	    x[2] = lerp(x[2], t < 20 ? 1.1 : 0.4, 0.2);
195	    if (t === dur - 35) game.playSfxWav?.('NPC_Hit_6', 1, e.cx, e.cy);   // :38389 PlaySound(4,…,6)=NPCHit style6(曾借 roar 0.3)
196	    if (t === dur - 14 || t === dur - 7 || t === dur) {          // :38392-38398
197	      const ox = Math.cos(x[0]) * 30 * x[1], oy = Math.sin(x[0]) * 30 * x[1];
198	      const d = Math.hypot(dx, dy) || 1;
199	      shootL(game, e.cx + ox, e.cy + oy, (dx / d) * 8, (dy / d) * 8, 35, 462);
200	    }
201	  } else if (e.ai0 === 2) {
202	    // ---- 幻影球 454 六角螺旋(:38397-38491) ----
203	    if (t < 15) {                                            // :38398-38406 收瞳减速
204	      x[1] = Math.max(0, x[1] - 0.07);
205	      x[2] = lerp(x[2], 0.4, 0.2);
206	      e.vx *= 0.8; e.vy *= 0.8;
207	      if (Math.hypot(e.vx, e.vy) < 1) { e.vx = 0; e.vy = 0; }
208	    } else if (t < 75) {
209	      // :38408-38460 六顶点两两插值轨道(0→2→5→3→1→4→0),每 10t 沿轨道外发 454(40 伤,速 4)
210	      const k = Math.floor((t - 15) / 10);
211	      const PAIRS: ReadonlyArray<readonly [number, number]> = [[0, 2], [2, 5], [5, 3], [3, 1], [1, 4], [4, 0]];
212	      const [p0, p1] = PAIRS[k] ?? [0, 2];
213	      const hex = (i: number): [number, number] => {
214	        const a = -Math.PI / 2 + (i * TAU) / 6;             // Vector2.UnitY*-30 旋转 i·π/3
215	        return [Math.cos(a) * 30, Math.sin(a) * 30];
216	      };
217	      const f = (t - 15) / 10 - k;
218	      const [ax, ay] = hex(p0), [bx, by] = hex(p1);
219	      const px = lerp(ax, bx, f), py = lerp(ay, by, f);
220	      x[0] = Math.atan2(py, px);
221	      x[1] = lerp(x[1], Math.hypot(px, py) / 30, 0.5);
222	      game.spawnParticles(e.cx + px, e.cy + py, '#C040D0', 2, 0.8, { life: 20 });  // :38455-38459
223	      if ((t - 15) % 10 === 0) {
224	        const d = Math.hypot(px, py);
225	        const ux = d > 0.001 ? px / d : 0, uy = d > 0.001 ? py / d : -1;
226	        shootL(game, e.cx + px, e.cy + py, ux * 4, uy * 4, 40, 454, 600);
227	      }
228	    } else if (t < 105) {
229	      // :38462-38485 瞄准升空(75t 起跳 vy=-7);原版同步给已发 454 叠加速度,Arrow 无弹 ai 槽,略
230	      x[0] = angleLerp(x[0], e.ai2 - Math.PI / 2, 0.2);
231	      x[2] = lerp(x[2], 0.75, 0.2);
232	      if (t === 75) { e.vx = 0; e.vy = -7; }
233	      e.vy *= 0.96;
234	      if (player) e.ai2 = Math.atan2(pcy - e.cy, pcx - e.cx) + Math.PI / 2;
235	      e.spin = angleTowards(e.spin, e.ai2, Math.PI / 30);
236	    } else if (t < 120) {
237	      // :38487-38505 发射:沿瞄准向 24 速冲出;已发 454 改归巢(ai[0]=-1),略
238	      game.playSfxWav?.('Zombie_102', 1, e.cx, e.cy);        // :38487 PlaySound(29,…,102)——case29 style102 ×0.4 自动档(曾借 roar 0.4 恰同值)
239	      e.vx = Math.cos(e.ai2 - Math.PI / 2) * 24;
240	      e.vy = Math.sin(e.ai2 - Math.PI / 2) * 24;
241	    } else {
242	      e.vx *= 0.92; e.vy *= 0.92;                            // :38507-38510
243	      e.spin = angleLerp(e.spin, 0, 0.2);
244	    }
245	  } else if (e.ai0 === 3) {
246	    // ---- 幻影眼 452 洒射(:38512-38583) ----
247	    if (t < 15) {
248	      x[1] = Math.max(0, x[1] - 0.07);
249	      x[2] = lerp(x[2], 0.4, 0.2);
250	      e.vx *= 0.9; e.vy *= 0.9;
251	      if (Math.hypot(e.vx, e.vy) < 1) { e.vx = 0; e.vy = 0; }
252	    } else if (t < 45) {
253	      // :38530-38538 瞳孔摆正
254	      x[0] = 0;
255	      x[1] = Math.sin((t - 15) * TAU / 15) * 0.5;
256	      if (x[1] < 0) x[0] = Math.PI;
257	    } else if (t < 185) {
258	      // :38540-38568 螺旋外扩洒射(8→20 速,每 10t 一发 452,35 伤,速 8)
259	      if (t === 45) e.ai2 = (Math.random() < 0.5 ? 1 : -1) * TAU / 40;
260	      if ((t - 45) % 40 === 0) e.ai2 *= 0.95;
261	      x[0] += e.ai2;
262	      x[1] = Math.min(1, x[1] + 0.05);
263	      const ox = Math.cos(x[0]) * 30 * x[1], oy = Math.sin(x[0]) * 30 * x[1];
264	      const spd = lerp(8, 20, (t - 45) / 140);
265	      const d = Math.hypot(ox, oy) || 1;
266	      e.vx = (ox / d) * spd; e.vy = (oy / d) * spd;
267	      e.spin = angleLerp(e.spin, Math.atan2(e.vy, e.vx) + Math.PI / 2, 0.2);
268	      if ((t - 45) % 10 === 0) {
269	        // :38557-38563 弹 ai[3]=随机弧线扰动,Arrow 无 ai 槽,略
270	        shootL(game, e.cx + (ox / d) * 12, e.cy + (oy / d) * 12,
271	          (ox / d) * 8, (oy / d) * 8, 35, 452, 600);
272	      }
273	    } else {
274	      // :38570-38583 收势
275	      e.vx *= 0.88; e.vy *= 0.88;
276	      e.spin = angleLerp(e.spin, 0, 0.2);
277	      x[1] = Math.max(0, x[1] - 0.07);
278	      x[2] = lerp(x[2], 1, 0.2);
279	    }
280	  } else if (e.ai0 === 4) {
281	    // ---- 死亡之光 455(:38585-38665):180t 吸能 → MLDeathray('core' 档,50 伤×2) ----
282	    if (t === 0 && player) e.facing = e.seekDirX(player);
283	    if (t < 180) {
284	      x[2] = lerp(x[2], 1, 0.2);
285	      x[1] = Math.max(0, x[1] - 0.05);
286	      e.vx *= 0.95; e.vy *= 0.95;
287	      if (Math.hypot(e.vx, e.vy) < 1) { e.vx = 0; e.vy = 0; }
288	      if (t >= 60) {                                          // :38616-38632 吸能粒子
289	        game.spawnParticles(e.cx + (Math.random() - 0.5) * 30, e.cy + (Math.random() - 0.5) * 30,
290	          '#B040D0', t >= 120 ? 2 : 1, 1.2, { life: 24 });
291	      }
292	    } else if (t < dur - 15) {
293	      if (t === 180 && player) {
294	        // :38634-38650 起角 = 朝玩家 ∓ 60°,角速度 = ±2π/540(MLDeathray 'core' 档 1:1)
295	        const dx = pcx - e.cx, dy = pcy - e.cy;
296	        const dd = Math.hypot(dx, dy) || 1;
297	        const n = dx / dd < 0 ? 1 : -1;                       // num1318
298	        const ang = Math.atan2(dy, dx) - n * TAU / 6;
299	        (game as unknown as { entities: { add: (en: unknown, b: string) => void } }).entities.add(
300	          new MLDeathray(e, 'core', ang, n * TAU / 540, 50 * 2), 'projectiles');
301	        e.ai2 = (ang + Math.PI * 3) * n;                      // :38649 扫射编码角
302	      }
303	      x[1] = Math.min(1, x[1] + 0.05);
304	      // :38656-38663 编码角逐 t 解码步进(瞳角跟踪扫射束)
305	      const s = e.ai2 >= 0 ? 1 : -1;
306	      const a = Math.abs(e.ai2) - Math.PI * 3 + (s * TAU) / 540;
307	      x[0] = a;
308	      e.ai2 = (a + Math.PI * 3) * s;
309	    } else {
310	      x[1] = Math.max(0, x[1] - 0.07);                        // :38664-38666
311	    }
312	  }
313	  fly(e);
314	}
315	
316	// ---------------------------------------------------------------------------
317	// AI_082 月总水蛭块 401(NPC.cs:38668-38792)
318	// ai[0]=头 396 id+1 / ai[1]=源弹索引(本仓 Arrow 无索引,以出生点代源弹 456 弹着点);
319	// ai[2] 90t 插值 头额(0,+216);到位 1000 点治疗按 头→核心→手0→手1 亏血序回灌后消散。
320	// ---------------------------------------------------------------------------
321	export function moonLeechAI(e: Enemy, game: GameHooks, _player: Player | null) {
322	  const x = lunarLocalAI(e);
323	  if (!e.bInit) {
324	    e.bInit = true;
325	    e.ai2 = 0;
326	    x[0] = e.cx; x[1] = e.cy;    // 源弹 456 弹着点(=玩家处)近似:出生点即弹着点(:37832)
327	  }
328	  // ---- 头锚定(:38676-38684) ----
329	  const head = enemies(game).find((n) => n.id === Math.floor(e.ai0) - 1 && n.vanillaId === 396);
330	  if (!head || head.dead) { e.dead = true; return; }
331	  e.ai2 += 1;
332	  const LEECH_T = 90;                                       // num1321
333	  if (e.ai2 >= LEECH_T) {
334	    // ---- 治疗回灌(:38689-38772):池 1000,按 头→核心→手0→手1 亏血序 ----
335	    const core = enemies(game).find((n) => n.id === head.ai3 && n.vanillaId === 398);
336	    const hands = enemies(game).filter((n) => !n.dead && n.vanillaId === 397 && n.ai3 === head.ai3);
337	    const hand0 = hands.find((n) => n.ai2 === 0);
338	    const hand1 = hands.find((n) => n.ai2 === 1);
339	    let pool = 1000;                                        // num1329
340	    for (const tgt of [head, core, hand0, hand1]) {
341	      if (!tgt || tgt.dead || pool <= 0) continue;
342	      const deficit = tgt.maxHp - tgt.hp;
343	      if (deficit <= 0) continue;
344	      const amt = Math.min(pool, deficit);                  // num1335 = pool+min(deficit-pool,0)
345	      tgt.hp += amt;
346	      pool -= amt;
347	      game.spawnParticles(tgt.cx, tgt.cy, '#5AE86A',
348	        Math.min(8, 2 + Math.floor(amt / 100)), 1.6, { life: 30 });   // HealEffect 近似
349	    }
350	    e.dead = true;                                          // :38770-38772 静默消散
351	    return;
352	  }
353	  // ---- 插值飞行(:38775-38791):出生点 → 头额 ----
354	  e.vx = 0; e.vy = 0;
355	  const k = e.ai2 / LEECH_T;
356	  e.x = lerp(x[0], head.cx, k) - e.w / 2;
357	  e.y = lerp(x[1], head.cy + 216, k) - e.h / 2;
358	  game.spawnParticles(e.cx, e.cy - e.h / 2, '#B040D0', 3, 0.7, { life: 20 });   // 紫尘双环
359	}
360	
361	// ---------------------------------------------------------------------------
362	// AI_083a 神秘石碑 437(NPC.cs:38795-38920 + CultistRitual.cs CheckFloor)
363	// 落地校验(CheckFloor:±6/±10 格四点 3 格净空)→ 召 4 教徒;信徒受击→弓手激活;
364	// 四教徒全灭 → 侧面召 439 + 300t 仪式倒计时(120t 起每 10t 仪式粒子)消散。
365	// 槽位:弓手 id+1 存 ai[0..1](原版同),信徒 id+1 存 localAI[1..2];ai[0]=-1 标记
366	// 邪教徒已召(此后 ai[3] 为倒计时)。
367	// ---------------------------------------------------------------------------
368	/** CultistRitual.CheckFloor(CultistRitual.cs:88-124 1:1):i∈{-5,-3,3,5} → x=tileX+i*2,
369	 *  y 自 tileY-5 向下扫至 +11,取首个"实心/平台 且上方 3 格净空"的点;不足 4 点 → null */
370	export function ritualCheckFloor(game: GameHooks, cx: number, cy: number): Array<{ x: number; y: number }> | null {
371	  const pts: Array<{ x: number; y: number }> = [];
372	  const tx = Math.floor(cx / TILE), ty = Math.floor(cy / TILE);
373	  for (const i of [-5, -3, 3, 5]) {
374	    const x = tx + i * 2;
375	    for (let j = -5; j < 12; j++) {
376	      const y = ty + j;
377	      if (y < 1 || y >= game.world.store.h - 1) break;
378	      const floor = solidTileAt(game, x, y) || game.world.store.isPlatform(x, y);
379	      if (!floor) continue;
380	      // 净空:本柱 3 格全空,或(本柱空 且 左右柱上两行空)——原版双条件或语义
381	      const clearMid = !solidRect(game, x - 1, x + 1, y - 3, y - 1);
382	      const clearSide = !solidRect(game, x, x, y - 3, y - 1)
383	        && !solidRect(game, x + 1, x + 1, y - 3, y - 2)
384	        && !solidRect(game, x - 1, x - 1, y - 3, y - 2);
385	      if (clearMid || clearSide) { pts.push({ x, y }); break; }
386	    }
387	  }
388	  return pts.length === 4 ? pts : null;
389	}
390	
391	export function cultistTabletAI(e: Enemy, game: GameHooks, _player: Player | null) {
392	  const x = lunarLocalAI(e);
393	  e.iframes = 2;                       // SetDefaults dontTakeDamage=true(:14115 段)
394	  e.lightRGB = [0.8, 0.75, 0.55];      // :38957 Lighting.AddLight
395	  if (!e.bInit) {
396	    // ---- 落地校验 + 召四教徒(:38798-38824) ----
397	    e.bInit = true;
398	    e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
399	    const pts = ritualCheckFloor(game, e.cx, e.cy);
400	    if (!pts) { e.dead = true; return; }               // 站不住 → 静默消散
401	    let arcN = 0, devN = 0;
402	    for (let k = 0; k < 4; k++) {
403	      const isDevotee = k === 1 || k === 2;            // 内侧两点信徒,外侧两点弓手
404	      const child = spawnPart(game, e, isDevotee ? 438 : 379);
405	      if (!child) continue;
406	      child.x = pts[k].x * TILE + 8 - child.w / 2;
407	      child.y = pts[k].y * TILE - child.h;             // 站上落点面(原版顶锚 y-48)
408	      child.ai3 = -(e.id + 1);                          // ai[3]=-(碑id+1) 待机锚
409	      child.bInit = true;
410	      if (isDevotee) x[1 + devN++] = child.id + 1;      // localAI[1..2]=信徒 id+1
411	      else if (arcN === 0) { e.ai0 = child.id + 1; arcN = 1; }   // ai[0]=弓手0 id+1
412	      else { e.ai1 = child.id + 1; arcN = 2; }                   // ai[1]=弓手1 id+1
413	    }
414	    if (arcN < 2 || devN < 2) { e.dead = true; return; }   // 生成不足 → 消散
415	    return;
416	  }
417	  // ---- 信徒受击 → 弓手激活(:38826-38839 localAI[0]==1) ----
418	  if (x[0] === 1) {
419	    x[0] = 2;
420	    for (let k = 0; k < 2; k++) {
421	      const dev = enemies(game).find((n) => n.id === x[k + 1] - 1 && n.vanillaId === 438);
422	      if (dev) dev.ai1 = 1;   // :38831 信徒 ai[1]=1(1.4.5.6 无消费方,存档语义保留)
423	      const arcId = k === 0 ? e.ai0 : e.ai1;
424	      const arc = enemies(game).find((n) => n.id === Math.floor(arcId) - 1 && n.vanillaId === 379);
425	      if (arc) arc.ai3 = 0;   // :38834 弓手解除待机(零伤恢复见 cultistArcherWake)
426	    }
427	  }
428	  // ---- 四教徒全灭 → 召 439(:38841-38879) ----
429	  if (e.ai0 !== -1) {
430	    const gone = [0, 1].every((k) => {
431	      const dev = enemies(game).find((n) => n.id === x[k + 1] - 1);
432	      const arc = enemies(game).find((n) => n.id === Math.floor(k === 0 ? e.ai0 : e.ai1) - 1);
433	      return (!dev || dev.dead || dev.vanillaId !== 438)
434	        && (!arc || arc.dead || arc.vanillaId !== 379);
435	    });
436	    if (gone) {
437	      // :38853-38868 侧面 11 格找落地列(±随机向),自碑心向下扫首个实心面
438	      const side = Math.random() < 0.5 ? 1 : -1;
439	      const tx = Math.floor(e.cx / TILE) + 11 * side;
440	      let ty = Math.floor(e.cy / TILE);
441	      for (let j = -5; j < 12; j++) {
442	        const y = Math.floor(e.cy / TILE) + j;
443	        if (solidTileAt(game, tx, y) && !solidRect(game, tx - 1, tx + 1, y - 3, y - 1)) { ty = y; break; }
444	        if (j === 11) ty = y;
445	      }
446	      const cultist = spawnPart(game, e, 439);
447	      // TabletDestroyed(delay=43200 重置)由 Game 侧 ai0==-1 边沿捕获记账
448	      // （_cultistTabletDone WeakSet 去重）——勿在此再调,避免双路径
449	      if (cultist) {
450	        cultist.x = tx * TILE + 10 - cultist.w / 2;
451	        cultist.y = ty * TILE - cultist.h;              // 原版顶锚 y=tileY*16-2,本仓落底对齐
452	        cultist.facing = Math.sign(e.cx - (tx * TILE + 10)) || 1;
453	        cultist.bInit = true;
454	        e.ai2 = cultist.id;                             // :38875 ai[2]=邪教徒 id
455	      }
456	      e.ai0 = -1; e.ai1 = 0; e.ai3 = 0;
457	      // CultistRitual.TabletDestroyed()(复活延迟账)——事件延迟系统未引入,略
458	    }
459	  }
460	  // ---- 仪式倒计时(:38881-38954):300t 满 → 爆散;120t 起每 10t 一枚 526(粒子代) ----
461	  if (e.ai0 === -1) {
462	    e.ai3 += 1;
463	    if (e.ai3 > 300) {
464	      e.dead = true;
465	      for (let k = 0; k < 6; k++) {                     // :38893-38903 六枚直飞
466	        game.spawnParticles(e.cx, e.cy, '#B080FF', 3, 3, { life: 30 });
467	      }
468	      for (let k = 0; k < 20; k++) {                    // :38905-38919 二十枚上抛(1/2 保留)
469	        if (Math.random() < 0.5) continue;
470	        game.spawnParticles(e.cx, e.cy, '#B080FF', 3, 3, { life: 30 });
471	      }
472	    } else if (e.ai3 % 10 === 1 && e.ai3 > 120) {       // :38921-38931
473	      game.spawnParticles(e.cx, e.cy, '#B080FF', 2, 2.4, { life: 34 });
474	    }
475	  }
476	  // 石碑静止(noGravity,noTileCollide;SetDefaults :14115 段)
477	}
478	
479	// ---------------------------------------------------------------------------
480	// AI_083b 拜月忠实信徒 438(NPC.cs:38926-38954)
481	// 站立面碑:横向摩擦 ±0.1 清零、朝碑翻转清 vx;受击 → 碑 localAI[0]=1(弓手激活链);
482	// ai[0] 300t 循环(站立摆动帧驱动)。重力/落地走共享块(NPC.cs UpdateNPC :91400 段)。
483	// ---------------------------------------------------------------------------
484	export function lunaticDevoteeAI(e: Enemy, game: GameHooks, _player: Player | null) {
485	  e.vx *= 0.93;
486	  if (e.vx > -0.1 && e.vx < 0.1) e.vx = 0;
487	  const owner = enemies(game).find((n) => n.id === -e.ai3 - 1 && n.vanillaId === 437);
488	  if (!owner || owner.dead) { e.dead = true; return; }   // :38934-38938 碑亡→消散
489	  const dir = Math.sign(owner.cx - e.cx);
490	  if (dir !== 0 && dir !== e.facing) { e.vx = 0; e.facing = dir; }   // :38940-38947
491	  if (e.justHit) {                                       // :38949-38952 → 碑 localAI[0]=1
492	    const ox = lunarLocalAI(owner);
493	    if (ox[0] === 0) ox[0] = 1;
494	  }
495	  if (e.ai0 < 0 || e.ai0 >= 300) e.ai0 = 0;              // 原版 ai[0] 出生 0
496	  e.ai0 += 1;
497	  if (e.ai0 >= 300) e.ai0 = 0;                           // :38953-38956
498	  e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
499	  moveAndCollide(e, game.world, e.vx, e.vy);
500	}
501	
502	// ---------------------------------------------------------------------------
503	// AI_003 待机尾段:拜月教弓手 379/380(NPC.cs:56575-56610)
504	// ai[3]<0 仪式待机:零接触伤、静立面碑(同信徒摩擦/翻转)、ai[0] 卡 1000..1300 站立帧
505	// 循环;受击 → 碑 localAI[0]=1。碑置 ai[3]=0 后:ai[0]≥1000 清零 + damage 恢复
506	// (:56602-56609),回 AI_003 战士核(射击参数见 Enemy.RANGED_TABLE 379/380 条目)。
507	// ---------------------------------------------------------------------------
508	export function cultistArcherStandbyAI(e: Enemy, game: GameHooks) {
509	  e.def.damage = 0;                                      // :56581 damage=0(待机零伤)
510	  const owner = enemies(game).find((n) => n.id === -e.ai3 - 1 && n.vanillaId === 437);
511	  if (!owner || owner.dead) { e.dead = true; return; }
512	  e.vx *= 0.93;
513	  if (e.vx > -0.1 && e.vx < 0.1) e.vx = 0;
514	  const dir = Math.sign(owner.cx - e.cx);
515	  if (dir !== 0 && dir !== e.facing) { e.vx = 0; e.facing = dir; }
516	  if (e.justHit) {                                       // :56593-56597 → 碑 localAI[0]=1
517	    const ox = lunarLocalAI(owner);
518	    if (ox[0] === 0) ox[0] = 1;
519	  }
520	  if (e.ai0 < 1000) e.ai0 = 1000;                        // :56599-56601 站立帧段
521	  e.ai0 += 1;
522	  if (e.ai0 >= 1300) e.ai0 = 1000;
523	  e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
524	  moveAndCollide(e, game.world, e.vx, e.vy);
525	}
526	
527	/** 弓手激活复位(:56602-56609):ai[0]≥1000 清零、damage 恢复 defDamage(待机段置 0) */
528	export function cultistArcherWake(e: Enemy) {
529	  if (e.ai0 >= 1000) e.ai0 = 0;
530	  e.def.damage = e.vanilla?.damage ?? e.def.damage;
531	}
532	
533	// ---------------------------------------------------------------------------
534	// AI_086 暗焰幻影 472 / 远古幻影 521(NPC.cs:39261-39519)
535	// 穿墙飞行族:0 定向 → 1 横掠(越玩家 660/500px 掉头)→ 2 竖摆 → 3 回掠 循环;
536	// 521 参数强化(0.7/14/500/6/3)+ 228 号紫雾拖尾;出生 120t 显形(Item8 音+尘爆)。
537	// ---------------------------------------------------------------------------
538	export function phantomAI(e: Enemy, game: GameHooks, player: Player | null) {
539	  const x = lunarLocalAI(e);
540	  const big = e.vanillaId === 521;
541	  if (e.spawnAlpha > 0) e.spawnAlpha = Math.max(0, e.spawnAlpha - 30);   // :39265-39271
542	  // ---- 同族 50px 排斥(:39277-39299) ----
543	  for (const n of enemies(game)) {
544	    if (n === e || n.dead || n.vanillaId !== e.vanillaId) continue;
545	    let dx = n.cx - e.cx, dy = n.cy - e.cy;
546	    const d = Math.hypot(dx, dy);
547	    if (d >= 50) continue;
548	    if (d > 0.001) { dx /= d; dy /= d; } else { dx = n.id > e.id ? 1 : -1; dy = 0; }
549	    e.vx -= dx * 0.4; e.vy -= dy * 0.4;
550	    n.vx += dx * 0.4; n.vy += dy * 0.4;
551	  }
552	  // ---- 出生显形(:39302-39335 472 / :39337-39360 521) ----
553	  if (x[3] < 120) {
554	    if (x[3] === 0) {
555	      game.playSfxFiles?.(['Item_8'], 0.5, e.cx, e.cy); // :39307 SoundID.Item8（原 roar 为错键）
556	      if (player) e.facing = e.seekDirX(player);
557	      e.vx += e.facing * 2;
558	      if (!big) game.spawnParticles(e.cx, e.cy - 18, '#7A4BD0', 20, 4, { life: 30 });
559	    }
560	    x[3] += 1;
561	    if (big) game.spawnParticles(e.cx, e.cy, '#5A2BA0', 2, 1.5, { life: 20 });
562	  }
563	  // ---- 状态机(:39362-39509);原版 ai[0] 出生 0,Enemy 哨兵 -1120 归一 ----
564	  if (e.ai0 < 0 || e.ai0 > 3) e.ai0 = 0;
565	  if (e.ai0 === 0) {
566	    if (player) e.facing = e.seekDirX(player);
567	    e.ai0 = 1; e.ai1 = e.facing;
568	  } else if (e.ai0 === 1) {
569	    // 横掠:加速 0.3/0.7 封顶 7/14,纵轴 4/6 伺服;越玩家 660/500px → 2
570	    const acc = big ? 0.7 : 0.3, max = big ? 14 : 7;
571	    const yClamp = big ? 6 : 4, range = big ? 500 : 660, yStep = big ? 3 : 4;
572	    if (player) e.facing = e.seekDirX(player);
573	    e.vx = clamp(e.vx + e.ai1 * acc, -max, max);
574	    let dy = player ? player.cy - e.cy : 0;
575	    let step = yStep;
576	    if (Math.abs(dy) > yClamp) { step = 15; dy = clamp(dy, -yClamp, yClamp); }
577	    e.vy = (e.vy * (step - 1) + dy) / step;
578	    const dpx = player ? player.cx - e.cx : 0;
579	    if ((e.ai1 > 0 && dpx < -range) || (e.ai1 < 0 && dpx > range)) {
580	      e.ai0 = 2;
581	      e.ai1 = player && e.cy + 20 > player.cy ? -1 : 1;  // :39400-39404
582	    }
583	  } else if (e.ai0 === 2) {
584	    // 竖摆:vy += ai[1]*0.4/0.3,超速 5/7 ×0.95/0.9;|vx|<1 → 3
585	    const acc = big ? 0.3 : 0.4, cap = big ? 7 : 5, damp = big ? 0.9 : 0.95;
586	    e.vy += e.ai1 * acc;
587	    if (Math.hypot(e.vx, e.vy) > cap) { e.vx *= damp; e.vy *= damp; }
588	    if (e.vx > -1 && e.vx < 1) {
589	      if (player) e.facing = e.seekDirX(player);
590	      e.ai0 = 3; e.ai1 = e.facing;
591	    }
592	  } else if (e.ai0 === 3) {
593	    // 回掠:vx += ai[1]*0.4/0.6,纵轴追玩家 ±0.2/0.3,超速 ×0.95/0.9;|vy|<1 → 0
594	    const acc = big ? 0.6 : 0.4, vyAcc = big ? 0.3 : 0.2;
595	    const cap = big ? 7 : 5, damp = big ? 0.9 : 0.95;
596	    e.vx += e.ai1 * acc;
597	    if (player) e.vy += e.cy > player.cy ? -vyAcc : vyAcc;
598	    if (Math.hypot(e.vx, e.vy) > cap) { e.vx *= damp; e.vy *= damp; }
599	    if (e.vy > -1 && e.vy < 1) {
600	      if (player) e.facing = e.seekDirX(player);
601	      e.ai0 = 0; e.ai1 = e.facing;
602	    }
603	  }
604	  if (big) game.spawnParticles(e.cx, e.cy, '#5A2BA0', 1, 0.6, { life: 16 });   // :39511-39518
605	  fly(e);
606	}
607	
608	// ---------------------------------------------------------------------------
609	// AI_087 珍稀四宝箱怪 473-476(NPC.cs:39520-39875)
610	// 0 伪装箱(唤醒:有速度/受击/玩家 80px)→ 1 蓄力 36t → 2 贴地跳扑主循环;
611	// 2 每 210t 随机 3 蓄能无敌 180t(expert 反弹投射物,不可达)/4 飞天俯冲/6 三连扑;
612	// 跳扑参数按血量:等待 15+30×HP比、横速 3+4×(1-HP比)、跳力 4(+2 无视线),
613	// 每 3 跳(ai[3])双倍跳力/半横速;7 玩家死→零伤满血渐隐;8 十周年炮连发不可达。
614	// ---------------------------------------------------------------------------
615	export function bigMimicAI(e: Enemy, game: GameHooks, player: Player | null) {
616	  if (e.ai0 < 0 || e.ai0 > 8) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
617	  // noGravity 运行时位（:39525 起始 false；4/4.1 俯冲分支/5 空中态置 true——
618	  // 4.1 仅"未过玩家 Y 且 ai[2]==0 的真俯冲段"(:39724-39730)，过顶回落段 false）。
619	  // StrikeNPC :82217 受击档（def.flying=false 覆盖不到，2026-08-17 补）
620	  e.noGravity = false;
621	  const p = player && !player.dead ? player : null;
622	  const los = !!p && losClear(game, e.cx, e.cy, p.cx, p.cy);
623	  // ---- 玩家全灭 → 7 隐身僵坐(:39526-39534) ----
624	  if (e.ai0 !== 7 && !p) { e.ai0 = 7; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
625	  const grounded = () => {
626	    e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
627	    moveAndCollide(e, game.world, e.vx, e.vy);
628	  };
629	
630	  if (e.ai0 === 0) {
631	    // ---- 伪装(:39536-39547) ----
632	    if (p) e.facing = e.seekDirX(p);
633	    const near = !!p && Math.hypot(p.cx - e.cx, p.cy - e.cy) < 80;
634	    if (e.vx !== 0 || e.vy > 100 || e.justHit || near) { e.ai0 = 1; e.ai1 = 0; }
635	    grounded();
636	  } else if (e.ai0 === 1) {
637	    // ---- 蓄力 36t(:39549-39557) ----
638	    e.ai1 += 1;
639	    if (e.ai1 > 36) { e.ai0 = 2; e.ai1 = 0; }
640	    grounded();
641	  } else if (e.ai0 === 2) {
642	    // ---- 贴地跳扑主循环(:39559-39621) ----
643	    if (p && Math.hypot(p.cx - e.cx, p.cy - e.cy) > 600) { e.ai0 = 5; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
644	    if (e.onGround && e.vy === 0) {
645	      if (p) e.facing = e.seekDirX(p);
646	      e.vx *= 0.85;
647	      e.ai1 += 1;
648	      const hpFrac = e.hp / e.maxHp;
649	      const wait = 15 + 30 * hpFrac;                       // num1409
650	      let jumpV = 3 + 4 * (1 - hpFrac);                    // num1410
651	      let jumpPow = los ? 4 : 6;                           // num1411(+2 无视线)
652	      if (e.ai1 > wait) {
653	        e.ai3 += 1;
654	        if (e.ai3 >= 3) { e.ai3 = 0; jumpPow *= 2; jumpV /= 2; }   // :39583-39588 每 3 跳大跳
655	        e.ai1 = 0;
656	        e.vy -= jumpPow;
657	        e.vx = jumpV * e.facing;
658	      }
659	    } else {
660	      e.vx *= 0.99;                                        // :39603-39610 空中保底 ±1
661	      if (e.facing === -1 && e.vx > -1) e.vx = -1;
662	      else if (e.facing === 1 && e.vx < 1) e.vx = 1;
663	    }
664	    e.ai2 += 1;                                            // :39612-39620 210t 随机换招
665	    if (e.ai2 > 210 && e.onGround && e.vy === 0) {
666	      const pick = rnd(3);
667	      e.ai0 = pick === 0 ? 3 : pick === 1 ? 4 : 6;
668	      if (pick === 1) e.vy = -8;                           // 4 号态起跳穿墙
669	      e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
670	    }
671	    grounded();
672	  } else if (e.ai0 === 3) {
673	    // ---- 蓄能无敌 180t(:39623-39637;expert ReflectProjectiles 不可达) ----
674	    e.vx *= 0.85;
675	    e.iframes = 2;
676	    e.ai1 += 1;
677	    if (e.ai1 >= 180) { e.ai0 = 2; e.ai1 = 0; }
678	    grounded();
679	  } else if (e.ai0 === 4) {
680	    // ---- 飞天(:39639-39677):悬玩家上方 350px → ai[2]=1 短瞄 6t → 4.1 俯冲 ----
681	    e.noGravity = true;                                    // :39661 整态置位
682	    if (p) e.facing = e.vx < 0 ? -1 : 1;
683	    const dx = p ? p.cx - e.cx : e.facing * 100;
684	    const dy = (p ? p.cy : e.cy) - 350 - e.cy;
685	    if (e.ai2 === 1) {
686	      e.ai1 += 1;
687	      const d = Math.hypot(dx, dy) || 1;
688	      const tx = (dx / d) * 8, ty = (dy / d) * 8;
689	      e.vx = (e.vx * 4 + tx) / 5; e.vy = (e.vy * 4 + ty) / 5;
690	      if (e.ai1 > 6) { e.ai0 = 4.1; e.ai1 = 0; e.ai2 = 0; e.vx = tx; e.vy = ty; }
691	    } else if (p && Math.abs(e.cx - p.cx) < 40 && e.cy < p.cy - 300) {
692	      e.ai1 = 0; e.ai2 = 1;
693	    } else {
694	      const d = Math.hypot(dx, dy) || 1;
695	      e.vx = (e.vx * 5 + (dx / d) * 12) / 6;
696	      e.vy = (e.vy * 5 + (dy / d) * 12) / 6;
697	    }
698	    fly(e);
699	  } else if (e.ai0 === 4.1) {
700	    // ---- 俯冲下坠(:39679-39709):过玩家 Y 或弹起 → 10t 后回 2(埋块则 5) ----
701	    if (e.ai2 === 0 && p && losClear(game, e.cx, e.cy, p.cx, p.cy) && !inSolidBody(game, e)) e.ai2 = 1;
702	    e.vy = Math.min(e.vy + 0.2, 16);
703	    if (!p || e.y + e.h >= p.y || e.vy <= 0) {
704	      e.ai1 += 1;
705	      if (e.ai1 > 10) {
706	        e.ai0 = inSolidBody(game, e) ? 5 : 2;
707	        e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
708	      }
709	      moveAndCollide(e, game.world, e.vx, e.vy);          // 碰撞下坠
710	    } else if (e.ai2 === 0) {
711	      e.noGravity = true;                                 // :39724-39730 真俯冲段
712	      fly(e);                                             // 未对齐前穿墙
713	    }
714	  } else if (e.ai0 === 5) {
715	    // ---- 穿墙归位(:39711-39734):追玩家,近 200px 且不埋块 → 回 2 ----
716	    e.noGravity = true;                                    // :39743 整态置位
717	    if (p) e.facing = e.vx > 0 ? 1 : -1;
718	    let dx = p ? p.cx - e.cx : 0, dy = (p ? p.cy : e.cy) - 4 - e.cy;
719	    if (p && Math.hypot(dx, dy) < 200 && !inSolidBody(game, e)) {
720	      e.ai0 = 2; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
721	    }
722	    const d = Math.hypot(dx, dy);
723	    if (d > 10) { dx = (dx / d) * 10; dy = (dy / d) * 10; }
724	    e.vx = (e.vx * 4 + dx) / 5; e.vy = (e.vy * 4 + dy) / 5;
725	    fly(e);
726	  } else if (e.ai0 === 6) {
727	    // ---- 三连扑(:39736-39795):每 5t 起跳(玩家越高/无视线 跳力越高),vx=12×dir ----
728	    if (e.onGround && e.vy === 0) {
729	      if (p) e.facing = e.seekDirX(p);
730	      e.vx *= 0.8;
731	      e.ai1 += 1;
732	      if (e.ai1 > 5) {
733	        e.ai1 = 0;
734	        e.vy -= 4;
735	        if (p && p.y + p.h < e.cy) e.vy -= 1.25;
736	        if (p && p.y + p.h < e.cy - 40) e.vy -= 1.5;
737	        if (p && p.y + p.h < e.cy - 80) e.vy -= 1.75;
738	        if (p && p.y + p.h < e.cy - 120) e.vy -= 2;
739	        if (p && p.y + p.h < e.cy - 160) e.vy -= 2.25;
740	        if (p && p.y + p.h < e.cy - 200) e.vy -= 2.5;
741	        if (p && !losClear(game, e.cx, e.cy, p.cx, p.cy)) e.vy -= 2;
742	        e.vx = 12 * e.facing;
743	        e.ai2 += 1;
744	      }
745	    } else {
746	      e.vx *= 0.98;                                       // :39780-39788 空中保底 ±8
747	      if (e.facing === -1 && e.vx > -8) e.vx = -8;
748	      else if (e.facing === 1 && e.vx < 8) e.vx = 8;
749	    }
750	    if (e.ai2 >= 3 && e.onGround && e.vy === 0) {         // :39791-39799
751	      e.ai0 = 2; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
752	    }
753	    grounded();
754	  } else if (e.ai0 === 7) {
755	    // ---- 玩家死隐身僵坐(:39801-39814):零伤/满血/渐隐,离屏由 despawn 清 ----
756	    e.def.damage = 0;
757	    e.hp = e.maxHp;
758	    e.spawnAlpha = Math.min(255, e.spawnAlpha + 7);
759	    e.vx *= 0.98;
760	    grounded();
761	  } else if (e.ai0 === 8) {
762	    // ---- 十周年世界炮连发(:39816-39835,getGoodWorld 不可达) ----
763	    e.vx *= 0.85;
764	    e.ai1 += 1;
765	    if (e.ai1 >= 180) { e.ai0 = 2; e.ai1 = 0; }
766	    grounded();
767	  }
768	}
769	
770	// ---------------------------------------------------------------------------
771	// AI_088 飞蛾魔 477(NPC.cs:39876-40406)——日食限定
772	// -1 无日食/玩家失效爬升无敌 / 0 悬顶 200px 伺服(180t 轮换,受击加速) /
773	// 1 穿墙追击 / 2 近距缠斗(×0.5 伤,LOS 断→0) / 3+3.1+3.2 侧掠冲刺(×1.3 伤) /
774	// 4+4.1+4.2 扫地产卵 478(478+479<7 时;专家孵化 70→52t,不可达)
775	// ---------------------------------------------------------------------------
776	export function mothronAI(e: Enemy, game: GameHooks, player: Player | null) {
777	  const p = player && !player.dead ? player : null;
778	  const baseDmg = e.vanilla?.damage ?? e.def.damage;
779	  e.def.damage = baseDmg;                                 // :39881 damage=defDamage
780	  const eggCap = 7;                                       // num1412
781	
782	  // 原版 ai[0] 出生 0,Enemy 哨兵 -1120 归一
783	  if (e.ai0 < -1 || e.ai0 > 4.2) e.ai0 = 0;
784	  // ---- 日食/目标门(:39882-39915) ----
785	  if (!game.world.clock.eclipse) {
786	    if (e.ai0 !== -1) e.ai0 = -1;
787	  } else if (!p) {
788	    e.ai0 = -1;
789	  } else if (e.ai0 > 1 && Math.hypot(p.cx - e.cx, p.cy - e.cy) > 1000) {
790	    e.ai0 = 1;                                            // :39906-39913 远距穿墙贴近
791	  }
792	
793	  if (e.ai0 === -1) {
794	    // ---- 爬升离场(:39917-39921) ----
795	    e.vx = (e.vx * 9) / 10; e.vy = (e.vy * 9 - 8) / 10;
796	    e.iframes = 2;
797	    fly(e);
798	    return;
799	  }
800	  if (!p) { fly(e); return; }
801	
802	  if (e.ai0 === 0) {
803	    // ---- 悬顶伺服(:39923-39988):目标=玩家上方 200px;>800px→1,>80px 追,近距微调 ----
804	    e.facing = e.cx < p.cx - 2 ? 1 : e.cx > p.cx + 2 ? -1 : e.facing;
805	    e.spin = (e.spin * 9 + e.vx * 0.1) / 10;
806	    const preVx = e.vx, preVy = e.vy;
807	    moveAndCollide(e, game.world, e.vx, e.vy);
808	    bounceAxis(e, preVx, preVy);
809	    let dx = p.cx - e.cx, dy = p.cy - 200 - e.cy;
810	    const d = Math.hypot(dx, dy);
811	    if (d > 800) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
812	    else if (d > 80) {
813	      e.vx = (e.vx * 29 + (dx / d) * 6) / 30;
814	      e.vy = (e.vy * 29 + (dy / d) * 6) / 30;
815	    } else if (Math.hypot(e.vx, e.vy) > 2) { e.vx *= 0.95; e.vy *= 0.95; }
816	    else if (Math.hypot(e.vx, e.vy) < 1) { e.vx *= 1.05; e.vy *= 1.05; }
817	    // ---- 180t 轮换(:39962-39992):受击 +10..30;2 需视线,4 需卵量 ----
818	    e.ai1 += 1;
819	    if (e.justHit) e.ai1 += rndRange(10, 30);
820	    if (e.ai1 < 180) return;
821	    e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
822	    const pick = rnd(3);                                  // 原版 while 重摇,单帧一次近似
823	    if (pick === 0 && losClear(game, e.cx, e.cy, p.cx, p.cy)) e.ai0 = 2;
824	    else if (pick === 1) e.ai0 = 3;
825	    else if (countNpc(game, 478) + countNpc(game, 479) < eggCap) e.ai0 = 4;
826	    return;
827	  }
828	  if (e.ai0 === 1) {
829	    // ---- 穿墙追击(:39994-40028):7+距/100 速,近 300px 且不埋块 → 0 ----
830	    let dx = p.cx - e.cx, dy = p.cy - e.cy;
831	    const d = Math.hypot(dx, dy);
832	    if (d < 300 && !inSolidBody(game, e)) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
833	    const spd = 7 + d / 100;
834	    e.vx = (e.vx * 24 + (dx / (d || 1)) * spd) / 25;
835	    e.vy = (e.vy * 24 + (dy / (d || 1)) * spd) / 25;
836	    e.facing = e.vx < 0 ? -1 : 1;
837	    e.spin = (e.spin * 9 + e.vx * 0.08) / 10;
838	    fly(e);
839	    return;
840	  }
841	  if (e.ai0 === 2) {
842	    // ---- 近距缠斗(:40030-40091):×0.5 伤;4+ai[2]+距/120 速递增;240t 或断视线 → 0 ----
843	    e.def.damage = Math.round(baseDmg * 0.5);
844	    if (p.cx - 10 < e.cx) e.facing = -1;
845	    else if (p.cx + 10 > e.cx) e.facing = 1;
846	    e.spin = (e.spin * 4 + e.vx * 0.1) / 5;
847	    const preVx = e.vx, preVy = e.vy;
848	    moveAndCollide(e, game.world, e.vx, e.vy);
849	    bounceAxis(e, preVx, preVy);
850	    const dx = p.cx - e.cx, dy = p.cy - 20 - e.cy;
851	    e.ai2 += 1 / 45;
852	    if (EXPERT) e.ai2 += 1 / 60;
853	    const d = Math.hypot(dx, dy);
854	    const spd = 4 + e.ai2 + d / 120;
855	    e.vx = (e.vx * 19 + (dx / (d || 1)) * spd) / 20;
856	    e.vy = (e.vy * 19 + (dy / (d || 1)) * spd) / 20;
857	    e.ai1 += 1;
858	    if (e.ai1 > 240 || !losClear(game, e.cx, e.cy, p.cx, p.cy)) {
859	      e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
860	    }
861	    return;
862	  }
863	  if (e.ai0 === 3 || e.ai0 === 3.1 || e.ai0 === 3.2) {
864	    // ---- 侧掠冲刺(:40093-40216) ----
865	    if (e.ai0 === 3) {
866	      // 拉开 400px 侧位(8+ai[1] 速),横距>350 且纵差<20 → 3.1
867	      let dx = p.cx - e.cx, dy = p.cy - 12 - e.cy;
868	      if (e.cx > p.cx) dx += 400; else dx -= 400;
869	      if (Math.abs(e.cx - p.cx) > 350 && Math.abs(e.cy - p.cy) < 20) { e.ai0 = 3.1; e.ai1 = 0; }
870	      e.ai1 += 1 / 30;
871	      const d = Math.hypot(dx, dy);
872	      const spd = 8 + e.ai1;
873	      e.vx = (e.vx * 3 + (dx / (d || 1)) * spd) / 4;
874	      e.vy = (e.vy * 3 + (dy / (d || 1)) * spd) / 4;
875	    } else if (e.ai0 === 3.1) {
876	      // 10t 瞄准(16 速贴脸) → 3.2 定向冲
877	      const dx = p.cx - e.cx, dy = p.cy - 12 - e.cy;
878	      const d = Math.hypot(dx, dy);
879	      e.vx = (e.vx * 7 + (dx / (d || 1)) * 16) / 8;
880	      e.vy = (e.vy * 7 + (dy / (d || 1)) * 16) / 8;
881	      e.facing = e.vx < 0 ? -1 : 1;
882	      e.spin = (e.spin * 4 + e.vx * 0.07) / 5;
883	      e.ai1 += 1;
884	      if (e.ai1 > 10) {
885	        e.ai0 = 3.2; e.ai1 = e.facing;
886	        e.vx = (dx / (d || 1)) * 16; e.vy = (dy / (d || 1)) * 16;
887	      }
888	    } else {
889	      // 直冲(16+ai[2] 速 ×1.3 伤),过玩家 260px 且不埋块 → 0;埋块且 >800px → 1
890	      e.def.damage = Math.round(baseDmg * 1.3);
891	      e.ai2 += 1 / 30;
892	      e.vx = (16 + e.ai2) * e.ai1;
893	      if ((e.ai1 > 0 && e.cx > p.cx + 260) || (e.ai1 < 0 && e.cx < p.cx - 260)) {
894	        if (!inSolidBody(game, e)) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
895	        else if (Math.abs(e.cx - p.cx) > 800) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
896	      }
897	      e.spin = (e.spin * 4 + e.vx * 0.07) / 5;
898	    }
899	    fly(e);
900	    return;
901	  }
902	  // ---- 扫地产卵(:40218-40404) ----
903	  if (e.ai0 === 4) {
904	    // 玩家周身 ±30/±20 格随机落点(越扫越宽),下潜 50 格找实心面,600px 内 → 4.1
905	    e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
906	    const aboveGround = e.cy / TILE < game.world.groundLevel;
907	    const ptx = Math.floor(p.cx / TILE), pty = Math.floor(p.cy / TILE);
908	    const st = game.world.store;
909	    for (let k = 0; k < 1000; k++) {
910	      const rx = 30 + Math.floor(k / 50), ry = 20 + Math.floor(k / 75);
911	      let tx = ptx + rndRange(-rx, rx + 1);
912	      let ty = pty + rndRange(-ry, ry + 1);
913	      if (solidTileAt(game, tx, ty)) continue;
914	      let bad = false;
915	      let n = 50;
916	      while (n > 0) {
917	        n--;
918	        if (tx < 5 || ty < 5 || tx >= st.w - 5 || ty >= st.h - 5) { bad = true; break; }
919	        const ii = st.idx(tx, ty);
920	        if (st.liquid[ii] > 0 && st.liquidType[ii] === 2) { bad = true; break; }   // 岩浆
921	        const iiA = st.idx(tx, ty - 1);
922	        if (st.liquid[iiA] > 0 && st.liquidType[iiA] === 2) { bad = true; break; }
923	        if (solidTileAt(game, tx, ty) || (aboveGround && ty > game.world.groundLevel)) break;
924	        ty++;
925	      }
926	      if (n <= 0 || bad) continue;
927	      if (Math.hypot(tx * TILE + 8 - p.cx, ty * TILE + 8 - p.cy) >= 600) continue;
928	      e.ai0 = 4.1; e.ai1 = tx; e.ai2 = ty;
929	      break;
930	    }
931	    return;
932	  }
933	  if (e.ai0 === 4.1) {
934	    // 飞向落点(6+距/150 封顶 10 速),<10px → 4.2
935	    e.facing = e.vx < -2 ? -1 : e.vx > 2 ? 1 : e.facing;
936	    e.spin = (e.spin * 9 + e.vx * 0.1) / 10;
937	    const gx = e.ai1 * TILE + 8, gy = e.ai2 * TILE - 20;
938	    const dx = gx - e.cx, dy = gy - e.cy;
939	    const d = Math.hypot(dx, dy);
940	    const spd = Math.min(6 + d / 150, 10);
941	    if (d < 10) { e.ai0 = 4.2; e.ai3 = 0; }
942	    e.vx = (e.vx * 9 + (dx / (d || 1)) * spd) / 10;
943	    e.vy = (e.vy * 9 + (dy / (d || 1)) * spd) / 10;
944	    const vl = Math.hypot(e.vx, e.vy);
945	    if (vl > spd) { e.vx = (e.vx / vl) * spd; e.vy = (e.vy / vl) * spd; }
946	    fly(e);
947	    return;
948	  }
949	  // 4.2 悬停产卵(:40357-40404):70t(专家 52)产 478,140t 收工(2/3 概率续扫)
950	  e.spin = (e.spin * 9 + e.vx * 0.1) / 10;
951	  const gx = e.ai1 * TILE + 8, gy = e.ai2 * TILE - 20;
952	  let dx = gx - e.cx, dy = gy - e.cy;
953	  const d = Math.hypot(dx, dy);
954	  if (d < 4) {
955	    const hatchT = EXPERT ? Math.round(70 * 0.75) : 70;
956	    e.ai3 += 1;
957	    if (e.ai3 === hatchT) {
958	      const egg = spawnPart(game, e, 478);
959	      if (egg) { egg.x = e.ai1 * TILE + 8 - egg.w / 2; egg.y = e.ai2 * TILE - egg.h; egg.bInit = true; }
960	    } else if (e.ai3 === hatchT * 2) {
961	      e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
962	      if (countNpc(game, 478) + countNpc(game, 479) < eggCap && rnd(3) !== 0) e.ai0 = 4;
963	      else if (inSolidBody(game, e)) e.ai0 = 1;
964	    }
965	  }
966	  if (d > 4) { dx = (dx / d) * 4; dy = (dy / d) * 4; }
967	  e.vx = (e.vx + dx) / 2;
968	  e.vy = (e.vy + dy) / 2;
969	  const vl = Math.hypot(e.vx, e.vy);
970	  if (vl > 4) { e.vx = (e.vx / vl) * 4; e.vy = (e.vy / vl) * 4; }
971	  fly(e);
972	}
973	
974	// ---------------------------------------------------------------------------
975	// AI_089 蛾卵 478(NPC.cs:40407-40449)
976	// 900t(专家 600)孵化 → Transform 479;受击 -10..20(普通双扣);末期 75% 起抽搐跳。
977	// ---------------------------------------------------------------------------
978	export function mothronEggAI(e: Enemy, game: GameHooks, _player: Player | null) {
979	  const hatchT = EXPERT ? 600 : 900;                      // num1440
980	  if (e.ai0 < 0) e.ai0 = 0;                              // 原版 ai[0] 出生 0,Enemy 哨兵 -1120 归一
981	  if (e.vy === 0) {
982	    e.vx *= 0.9;
983	    e.spin += e.vx * 0.02;
984	  } else {
985	    e.vx *= 0.99;
986	    e.spin += e.vx * 0.04;
987	  }
988	  if (e.justHit) {                                        // :40419-40425
989	    e.ai0 -= rndRange(10, 21);
990	    if (!EXPERT) e.ai0 -= rndRange(10, 21);
991	  }
992	  e.ai0 += 1;
993	  if (e.ai0 >= hatchT) {
994	    e.transformTo(479, game.world.store, false, game);   // :40428 Transform(479)
995	    return;
996	  }
997	  if (e.vy === 0 && Math.abs(e.vx) < 0.2 && e.ai0 >= hatchT * 0.75) {
998	    // :40431-40445 末期抽搐:越接近孵化越频繁的随机跳
999	    const k = (e.ai0 - hatchT * 0.75) / (hatchT * 0.25);
1000	    if (rndRange(-10, 120) < k * 100) {

```


---

## 🤖 Assistant · 2026-08-19T03:10:13.561Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me continue reading the file.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:14.047Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_lunar_misc.ts",
 "offset": 1000,
 "limit": 929
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:14.288Z

**📎 ToolResult**

```
1000	    if (rndRange(-10, 120) < k * 100) {
1001	      e.vy -= rndRange(20, 40) * 0.025;
1002	      e.vx += rndRange(-20, 20) * 0.025;
1003	      e.vx *= 1 + k * 2; e.vy *= 1 + k * 2;
1004	    }
1005	  }
1006	  e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);
1007	  moveAndCollide(e, game.world, e.vx, e.vy);
1008	}
1009	
1010	// ---------------------------------------------------------------------------
1011	// AI_090 幼蛾 479(NPC.cs:40450-40685)——日食限定
1012	// 无日食 → EncourageDespawn(5)+上浮;-1 爬升无敌 / 0 悬停(90t→2,同族排斥)/
1013	// 1 穿墙追击(近 300px → 0)/ 2+2.1 贴脸冲撞(9 速,45t 后埋块判 0/1)
1014	// ---------------------------------------------------------------------------
1015	export function babyMothronAI(e: Enemy, game: GameHooks, player: Player | null) {
1016	  const p = player && !player.dead ? player : null;
1017	  e.spin = (e.spin * 9 + e.vx * 0.1) / 10;                // :40456
1018	  // 原版 ai[0] 出生 0,Enemy 哨兵 -1120 归一
1019	  if (e.ai0 < -1 || e.ai0 > 2.1) e.ai0 = 0;
1020	  if (!game.world.clock.eclipse) {                              // :40458-40467
1021	    e.encourageDespawn(5);
1022	    e.vy = Math.max(e.vy - 0.2, -8);
1023	    fly(e);
1024	    return;
1025	  }
1026	  // ---- 同族排斥(状态 0/1,:40469-40491) ----
1027	  if (e.ai0 === 0 || e.ai0 === 1) {
1028	    for (const n of enemies(game)) {
1029	      if (n === e || n.dead || n.vanillaId !== e.vanillaId) continue;
1030	      let dx = n.cx - e.cx, dy = n.cy - e.cy;
1031	      const d = Math.hypot(dx, dy);
1032	      if (d >= e.w + e.h || d === 0) continue;
1033	      dx = (dx / d) * -0.1; dy = (dy / d) * -0.1;
1034	      e.vx += dx; e.vy += dy;
1035	      n.vx -= dx; n.vy -= dy;
1036	    }
1037	  }
1038	  // ---- 目标门(:40493-40509) ----
1039	  if (!p) e.ai0 = -1;
1040	  else if (e.ai0 > 1 && Math.hypot(p.cx - e.cx, p.cy - e.cy) > 1000) e.ai0 = 1;
1041	
1042	  if (e.ai0 === -1) {
1043	    // ---- 爬升(:40511-40515) ----
1044	    e.vx = (e.vx * 9) / 10; e.vy = (e.vy * 9 - 8) / 10;
1045	    e.iframes = 2;
1046	    fly(e);
1047	    return;
1048	  }
1049	  if (!p) { fly(e); return; }
1050	
1051	  if (e.ai0 === 0) {
1052	    // ---- 悬停(:40517-40577):>800px→1 / >200px 追(5.5+距/100+ai[1]/15)/ 近距微调;90t→2 ----
1053	    const preVx = e.vx, preVy = e.vy;
1054	    moveAndCollide(e, game.world, e.vx, e.vy);
1055	    bounceAxis(e, preVx, preVy);
1056	    const dx = p.cx - e.cx, dy = p.cy - e.cy;
1057	    const d = Math.hypot(dx, dy);
1058	    if (d > 800) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1059	    else if (d > 200) {
1060	      const spd = 5.5 + d / 100 + e.ai1 / 15;
1061	      e.vx = (e.vx * 39 + (dx / d) * spd) / 40;
1062	      e.vy = (e.vy * 39 + (dy / d) * spd) / 40;
1063	    } else if (Math.hypot(e.vx, e.vy) > 2) { e.vx *= 0.95; e.vy *= 0.95; }
1064	    else if (Math.hypot(e.vx, e.vy) < 1) { e.vx *= 1.05; e.vy *= 1.05; }
1065	    e.ai1 += 1;
1066	    if (e.ai1 >= 90) { e.ai1 = 0; e.ai0 = 2; }
1067	    return;
1068	  }
1069	  if (e.ai0 === 1) {
1070	    // ---- 穿墙追击(:40579-40613):5.5+ai[2]+距/150 速;近 300px 且不埋块 → 0 ----
1071	    const dx = p.cx - e.cx, dy = p.cy - e.cy;
1072	    const d = Math.hypot(dx, dy);
1073	    if (d < 300 && !inSolidBody(game, e)) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1074	    e.ai2 += 1 / 60;
1075	    const spd = 5.5 + e.ai2 + d / 150;
1076	    e.vx = (e.vx * 34 + (dx / (d || 1)) * spd) / 35;
1077	    e.vy = (e.vy * 34 + (dy / (d || 1)) * spd) / 35;
1078	    e.facing = e.vx < 0 ? -1 : 1;
1079	    e.spin = (e.spin * 9 + e.vx * 0.08) / 10;
1080	    fly(e);
1081	    return;
1082	  }
1083	  if (e.ai0 === 2) {
1084	    // ---- 贴脸瞄准 10t(9 速,:40615-40652) → 2.1 定向冲 ----
1085	    const dx = p.cx - e.cx, dy = p.cy - 8 - e.cy;
1086	    const d = Math.hypot(dx, dy);
1087	    e.facing = e.vx < 0 ? -1 : 1;
1088	    e.spin = (e.spin * 7 + e.vx * 0.1) / 8;
1089	    e.vx = (e.vx * 7 + (dx / (d || 1)) * 9) / 8;
1090	    e.vy = (e.vy * 7 + (dy / (d || 1)) * 9) / 8;
1091	    e.ai1 += 1;
1092	    if (e.ai1 > 10) {
1093	      e.ai0 = 2.1; e.ai1 = 0;
1094	      e.vx = (dx / (d || 1)) * 9; e.vy = (dy / (d || 1)) * 9;
1095	    }
1096	    fly(e);
1097	    return;
1098	  }
1099	  // ---- 2.1 冲刺(:40654-40682):×1.01/t 增速;45t 后不埋块→0,埋块且 90t→1 ----
1100	  e.facing = e.vx < 0 ? -1 : 1;
1101	  e.vx *= 1.01; e.vy *= 1.01;
1102	  e.ai1 += 1;
1103	  if (e.ai1 > 45) {
1104	    if (!inSolidBody(game, e)) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; }
1105	    else if (e.ai1 > 90) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1106	  }
1107	  fly(e);
1108	}
1109	
1110	/** 撞轴 ×(-旧速·0.5) 封顶 ±4(NPC.cs Mothron 族 collide 语义,:39933-39939) */
1111	function bounceAxis(e: Enemy, preVx: number, preVy: number) {
1112	  if (e.hitWall) { e.vx *= -preVx * 0.5; e.vx = clamp(e.vx, -4, 4); }
1113	  if (e.hitHead || (e.onGround && preVy > 0)) { e.vy *= -preVy * 0.5; e.vy = clamp(e.vy, -4, 4); }
1114	}
1115	
1116	// ---------------------------------------------------------------------------
1117	// AI_091 花岗岩元素 483(NPC.cs:40686-40870)
1118	// AI 自置 noGravity=true(:40688)——全程无重力,碰撞按态开合:
1119	// -1 受击石化 120t(专家限定,不可达)/ 0 视线判别→1 直追(2+距/200 速)/
1120	// 2 穿墙冲刺(近 600px 且不埋块→0)/ 3 锚点侧移(1 速,撞轴/到点/通视线→0)/
1121	// 4 漂移弹壁(1.5 速,180t 或通视线→0;每 5t 重试锚点)。
1122	// 与 AI_085(星细胞族)同构五态寻路——aiStyle 85 的 1:1 内核在此。
1123	// ---------------------------------------------------------------------------
1124	export function graniteElementalAI(e: Enemy, game: GameHooks, player: Player | null) {
1125	  const p = player && !player.dead ? player : null;
1126	  const x = lunarLocalAI(e);
1127	  // 原版 ai[0] 出生 0,Enemy 哨兵 -1120 归一(-1 石化态合法保留)
1128	  if (e.ai0 !== -1 && (e.ai0 < 0 || e.ai0 > 4)) e.ai0 = 0;
1129	  // noGravity 运行时位（:40688 起始 true / -1 石化态 :40699 置 false）——
1130	  // StrikeNPC :82217 受击档（def.flying=false 覆盖不到，2026-08-17 补）
1131	  // ---- 专家受击石化(:40692-40697,EXPERT 恒 false 不可达,代码保留) ----
1132	  if (e.justHit && EXPERT && rnd(6) === 0) { e.ai0 = -1; e.ai1 = 0; }
1133	  e.noGravity = e.ai0 !== -1;   // 转移 tick 即置 false（原版 -1 分支同 tick 生效）
1134	
1135	  if (e.ai0 === -1) {
1136	    // ---- 石化(:40699-40708) ----
1137	    e.iframes = 2;
1138	    e.vx *= 0.98;
1139	    e.ai1 += 1;
1140	    moveAndCollide(e, game.world, e.vx, e.vy);
1141	    if (e.ai1 >= 120) { e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1142	    return;
1143	  }
1144	  if (!p) { moveAndCollide(e, game.world, e.vx, e.vy); return; }
1145	  const los = losClear(game, e.cx, e.cy, p.cx, p.cy);
1146	
1147	  if (e.ai0 === 0) {
1148	    // ---- 视线判别(:40710-40752):通视线→1;否则找中转锚(玩家正上/正下列)→3;无→4 ----
1149	    if (los) { e.ai0 = 1; return; }
1150	    // 锚 1:玩家正上/正下列 (px, selfY)(:40722-40732)
1151	    if (Math.abs(p.cx - e.cx) > 8 && losClear(game, e.cx, e.cy, p.cx, e.cy)) {
1152	      e.ai0 = 3; e.ai1 = p.cx; e.ai2 = e.cy;
1153	      // 命中再升级为 (selfX, playerY) 双段锚(:40734-40742)
1154	      if (Math.abs(p.cy - e.cy) > 8 && losClear(game, e.cx, e.cy, e.cx, p.cy)
1155	        && losClear(game, e.cx, p.cy, p.x, p.y)) {
1156	        e.ai1 = e.cx; e.ai2 = p.cy;
1157	      }
1158	    } else if (Math.abs(p.cy - e.cy) > 8 && losClear(game, e.cx, e.cy, e.cx, p.cy)) {
1159	      e.ai0 = 3; e.ai1 = e.cx; e.ai2 = p.cy;              // :40744-40750 行锚
1160	    }
1161	    if (e.ai0 === 0) {
1162	      // 无锚:直朝玩家轻推 0.5 → 4 漂移(:40744-40752)
1163	      x[0] = 0;
1164	      const dx = p.cx - e.cx, dy = p.cy - p.h / 4 - e.cy;
1165	      const d = Math.hypot(dx, dy) || 1;
1166	      e.vx += (dx / d) * 0.5; e.vy += (dy / d) * 0.5;
1167	      e.ai0 = 4; e.ai1 = 0;
1168	    }
1169	  } else if (e.ai0 === 1) {
1170	    // ---- 直追(:40754-40768):2+距/200 速(50 步进);断视线 → 0 ----
1171	    const dx = p.cx - e.cx, dy = p.cy - e.cy;
1172	    const d = Math.hypot(dx, dy);
1173	    const spd = 2 + d / 200;
1174	    e.vx = (e.vx * 49 + (dx / (d || 1)) * spd) / 50;
1175	    e.vy = (e.vy * 49 + (dy / (d || 1)) * spd) / 50;
1176	    moveAndCollide(e, game.world, e.vx, e.vy);
1177	    if (!los) { e.ai0 = 0; e.ai1 = 0; }
1178	    return;
1179	  } else if (e.ai0 === 2) {
1180	    // ---- 穿墙冲刺(:40770-40783):2 速;近 600px 且不埋块 → 0 ----
1181	    const dx = p.cx - e.cx, dy = p.cy - e.cy;
1182	    const d = Math.hypot(dx, dy);
1183	    e.vx = (e.vx * 3 + (dx / (d || 1)) * 2) / 4;
1184	    e.vy = (e.vy * 3 + (dy / (d || 1)) * 2) / 4;
1185	    fly(e);
1186	    if (d < 600 && !inSolidBody(game, e)) e.ai0 = 0;
1187	    return;
1188	  } else if (e.ai0 === 3) {
1189	    // ---- 锚点侧移(:40785-40801):1 速(3 步进);撞轴→4;到点/超 800px/通视线→0 ----
1190	    const dx = e.ai1 - e.cx, dy = e.ai2 - e.cy;
1191	    const d = Math.hypot(dx, dy);
1192	    e.vx = (e.vx * 2 + (dx / (d || 1)) * 1) / 3;
1193	    e.vy = (e.vy * 2 + (dy / (d || 1)) * 1) / 3;
1194	    const preVy = e.vy;
1195	    moveAndCollide(e, game.world, e.vx, e.vy);
1196	    if (e.hitWall || e.hitHead || (e.onGround && preVy > 0)) { e.ai0 = 4; e.ai1 = 0; }
1197	    if (d < 1 || d > 800 || los) { e.ai0 = 0; }
1198	    return;
1199	  } else if (e.ai0 === 4) {
1200	    // ---- 漂移弹壁(:40803-40854):1.5 速(20 步进);180t 或通视线 → 0 ----
1201	    if (e.hitWall) e.vx *= -0.8;
1202	    if (e.hitHead || e.onGround) e.vy *= -0.8;
1203	    if (e.vx === 0 && e.vy === 0) {
1204	      const dx = p.cx - e.cx, dy = p.cy - p.h / 4 - e.cy;
1205	      const d = Math.hypot(dx, dy) || 1;
1206	      e.vx = (dx / d) * 0.1; e.vy = (dy / d) * 0.1;
1207	    }
1208	    const v = Math.hypot(e.vx, e.vy) || 1;
1209	    e.vx = (e.vx * 19 + (e.vx / v) * 1.5) / 20;
1210	    e.vy = (e.vy * 19 + (e.vy / v) * 1.5) / 20;
1211	    e.ai1 += 1;
1212	    if (e.ai1 > 180 || los) { e.ai0 = 0; e.ai1 = 0; }
1213	    moveAndCollide(e, game.world, e.vx, e.vy);
1214	    // ---- 每 5t 重试中转锚(:40858-40870) ----
1215	    x[0] += 1;
1216	    if (x[0] >= 5 && !inSolidBody(game, e)) {
1217	      x[0] = 0;
1218	      // 先试列锚 (px, selfY)(需三方视线),再试行锚 (selfX, py)
1219	      if (losClear(game, e.cx, e.cy, p.cx, e.cy) && losClear(game, p.cx, p.cy, p.cx, e.cy)) {
1220	        e.ai0 = 3; e.ai1 = p.cx; e.ai2 = e.cy;
1221	      } else if (losClear(game, e.cx, e.cy, e.cx, p.cy) && losClear(game, p.cx, p.cy, e.cx, p.cy)) {
1222	        e.ai0 = 3; e.ai1 = e.cx; e.ai2 = p.cy;
1223	      }
1224	    }
1225	  }
1226	}
1227	
1228	// ---------------------------------------------------------------------------
1229	// 星璇塔四组专属怪批(aiStyle 85/95/96/97/99)——替换 Enemy.ts 一期近似档
1230	// (swarmerAI/casterAI)。锚点:
1231	//   aiStyle 85  星细胞 405 / 星云头蟹 421   NPC.cs:38967-39220(六态寻路+421 头顶吸附)
1232	//   aiStyle 95  小星细胞 406                NPC.cs:41445-41492(300t 长大 → Transform 405)
1233	//   aiStyle 96  水流入侵者 407(/408)        NPC.cs:41493-41535(悬顶伺服 + 投射物 539)
1234	//   aiStyle 97  星云悬浮脑 420              NPC.cs:41536-41750(瞬移 + 环绕球 574 → 弹 576)
1235	//   aiStyle 99  日耀黏液 519                NPC.cs:41997-42056(重力坠落 → 落地 5t 自爆)
1236	// 勘误(1.4.5.6 全树核对):NPC 408 无任何 NewNPC/Transform 调用源——docs/
1237	//   event-lunar-pillars.md §4"408 由投射物 539 生成"不成立;539 自身只绕 407 盘旋
1238	//   210t 后以 16 速冲玩家、亡时 80×80 范围伤害(Projectile.cs:32040-32280/:69366-69405),
1239	//   不生怪。407/408 共用 aiStyle 96,本实现对其一视同仁。
1240	// ---------------------------------------------------------------------------
1241	
1242	/** Collision.SolidCollision 近似(矩形内 ANY 实心)——AI_085 态 2 出墙判定(:39090) */
1243	function touchesSolid(game: GameHooks, e: Enemy, inflate = 0): boolean {
1244	  const st = game.world.store;
1245	  const x0 = Math.floor((e.x - inflate) / TILE), x1 = Math.floor((e.x + e.w - 0.01 + inflate) / TILE);
1246	  const y0 = Math.floor((e.y - inflate) / TILE), y1 = Math.floor((e.y + e.h - 0.01 + inflate) / TILE);
1247	  for (let tx = x0; tx <= x1; tx++) {
1248	    for (let ty = y0; ty <= y1; ty++) {
1249	      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) return true;
1250	    }
1251	  }
1252	  return false;
1253	}
1254	
1255	/** 星细胞族尾段:405 旋转清零 / 421 旋转=vx×0.1(:39104-39119) + 同族排斥(:39106-39131) */
1256	function starCellTail(e: Enemy, game: GameHooks, is405: boolean): void {
1257	  if (is405) e.visAngle = 0;
1258	  else e.visAngle = e.vx * 0.1;
1259	  for (const n of enemies(game)) {
1260	    if (n === e || n.dead || n.vanillaId !== e.vanillaId) continue;
1261	    if (Math.abs(e.x - n.x) + Math.abs(e.y - n.y) < e.w) {
1262	      e.vx += e.x < n.x ? -0.05 : 0.05;
1263	      e.vy += e.y < n.y ? -0.05 : 0.05;
1264	    }
1265	  }
1266	}
1267	
1268	/** AI_085 星细胞 405 / 星云头蟹 421(NPC.cs:38967-39220)六态:
1269	 *  0 视线判别(通→1;远 800→2;找中转锚→3;无→轻推入 4)/ 1 直追(5.5|8+距/100,50 步进)/
1270	 *  2 穿墙(3|6 速,noTileCollide;近 600 且离实心→0)/ 3 锚点侧移(2|3 速,撞→4)/
1271	 *  4 漂移弹壁(2|3 速,180t;每 5t 重试锚)/ 5(仅 421)钉玩家头顶 Obstructed。 */
1272	export function starCellAI(e: Enemy, game: GameHooks, player: Player | null) {
1273	  const p = player && !player.dead ? player : null;
1274	  const is405 = e.vanillaId === 405;
1275	  const lai = lunarLocalAI(e);
1276	  if (e.ai0 < 0 || e.ai0 > 5) e.ai0 = 0;            // Enemy 哨兵 -1120 归一,原版出生 0
1277	  if (e.ai0 === 5) {
1278	    // ---- 421 头顶吸附(:39183-39202):Center=player.Top+(direction*4,0);失活→脱落 ----
1279	    if (!p) { e.ai0 = 0; e.ai1 = 0; }
1280	    else {
1281	      const dir = p.facing ?? 1;
1282	      e.x = p.cx + dir * 4 - e.w / 2;
1283	      e.y = p.y - e.h / 2;
1284	      e.vx = 0; e.vy = 0;
1285	      // AddBuff(163 Obstructed,59) 每 tick 续期(:39197-39201)——BuffState.apply 取
1286	      // max 合并,吸附期间恒 ≤1s 存量,脱落后自然消退。遮屏视觉在 Renderer
1287	      // drawScreenObstruction（ScreenObstruction.cs 1:1）。
1288	      // （原版另以 hide=ai[0]==5 隐藏本体——保持可见为已登记偏差,否则吸附期完全不可见）
1289	      p.buffs.apply(BuffType.Obstructed, 59 / 60);
1290	    }
1291	    starCellTail(e, game, is405);
1292	    return;
1293	  }
1294	  if (!p) { moveAndCollide(e, game.world, e.vx, e.vy); starCellTail(e, game, is405); return; }
1295	  const los = losClear(game, e.cx, e.cy, p.cx, p.cy); // CanHit(Center,1,1,…)
1296	  let flyPhase = false;
1297	
1298	  if (e.ai0 === 0) {
1299	    // ---- 视线判别(:38974-39030) ----
1300	    if (los) { e.ai0 = 1; }
1301	    else {
1302	      const dx = p.cx - e.cx, dy = p.cy - p.h / 4 - e.cy;
1303	      if (Math.hypot(dx, dy) > 800) { e.ai0 = 2; }
1304	      else {
1305	        // 列锚 (px, selfY)(:38987-38997);命中升级双段锚 (selfX, py)(:38999-39008,
1306	        // 原文复用列距 >8 判据——按原文照抄)
1307	        if (Math.abs(p.cx - e.cx) > 8 && losClear(game, e.cx, e.cy, p.cx, e.cy)) {
1308	          e.ai0 = 3; e.ai1 = p.cx; e.ai2 = e.cy;
1309	          if (Math.abs(p.cx - e.cx) > 8 && losClear(game, e.cx, e.cy, e.cx, p.cy)
1310	            && losClear(game, e.cx, p.cy, p.x, p.y)) {
1311	            e.ai0 = 3; e.ai1 = e.cx; e.ai2 = p.cy;
1312	          }
1313	        } else if (Math.abs(p.cy - e.cy) > 8 && losClear(game, e.cx, e.cy, e.cx, p.cy)) {
1314	          e.ai0 = 3; e.ai1 = e.cx; e.ai2 = p.cy;      // 行锚(:39015-39022)
1315	        }
1316	        if (e.ai0 === 0) {
1317	          // 无锚:朝玩家(Y 抬高 h/4)轻推 0.5 → 4 漂移(:39023-39030)
1318	          lai[0] = 0;
1319	          const d = Math.hypot(dx, dy) || 1;
1320	          e.vx += (dx / d) * 0.5; e.vy += (dy / d) * 0.5;
1321	          e.ai0 = 4; e.ai1 = 0;
1322	        }
1323	      }
1324	    }
1325	  } else if (e.ai0 === 1) {
1326	    // ---- 直追(:39031-39069):(5.5|8)+距/100 速,50 步进;断视线→0 ----
1327	    // 421 瞄 player.Top（:39032-39035 if type==421 → vector = player.Top - center）；
1328	    // 405/467 瞄 player.Center
1329	    const is421 = e.vanillaId === 421;
1330	    const tx = p.cx - e.cx, ty = (is421 ? p.y : p.cy) - e.cy;
1331	    const d = Math.hypot(tx, ty);
1332	    const spd = (is405 ? 8 : 5.5) + d / 100;
1333	    const n = d || 1;
1334	    e.vx = (e.vx * 49 + (tx / n) * spd) / 50;
1335	    e.vy = (e.vy * 49 + (ty / n) * spd) / 50;
1336	    if (!los) { e.ai0 = 0; e.ai1 = 0; }
1337	    // 421 专属吸附门（:39052-39068 if type==421 && num<40）：近 40px 且场上无同族
1338	    // 吸附中才钉上。467 致命球（日食怪，同 aiStyle 85）**不**吸附——此前误写成
1339	    // !is405 导致致命球钉头 + 每 tick 灌 Obstructed(163)
1340	    if (is421 && d < 40
1341	      && !enemies(game).some((o) => o !== e && !o.dead && o.vanillaId === 421 && o.ai0 === 5)) {
1342	      e.x = p.cx - e.w / 2; e.y = p.y - e.h;        // Center=player.Top
1343	      e.vx = 0; e.vy = 0;
1344	      e.ai0 = 5; e.ai1 = 0;
1345	    }
1346	  } else if (e.ai0 === 2) {
1347	    // ---- 穿墙(:39071-39094):noTileCollide=true;3|6 速 3 步进;近 600 且离实心→0 ----
1348	    flyPhase = true;
1349	    const tx = p.cx - e.cx, ty = p.cy - e.cy;
1350	    const d = Math.hypot(tx, ty) || 1;
1351	    const spd = is405 ? 6 : 3;
1352	    e.vx = (e.vx * 2 + (tx / d) * spd) / 3;
1353	    e.vy = (e.vy * 2 + (ty / d) * spd) / 3;
1354	    if (d < 600 && !touchesSolid(game, e)) e.ai0 = 0;
1355	  } else if (e.ai0 === 3) {
1356	    // ---- 锚点侧移(:39096-39115):2|3 速 3 步进;撞轴→4;到点/超 800/通视线→0 ----
1357	    const tx = e.ai1 - e.cx, ty = e.ai2 - e.cy;
1358	    const d = Math.hypot(tx, ty) || 1;
1359	    const spd = is405 ? 3 : 2;
1360	    e.vx = (e.vx * 2 + (tx / d) * spd) / 3;
1361	    e.vy = (e.vy * 2 + (ty / d) * spd) / 3;
1362	    if (e.hitWall || e.hitHead || e.onGround) { e.ai0 = 4; e.ai1 = 0; }
1363	    if (d < spd || d > 800 || los) e.ai0 = 0;
1364	  } else if (e.ai0 === 4) {
1365	    // ---- 漂移弹壁(:39117-39175):弹壁 ×-0.8;2|3 速 20 步进;180t 或通视线→0 ----
1366	    if (e.hitWall) e.vx *= -0.8;
1367	    if (e.hitHead || e.onGround) e.vy *= -0.8;
1368	    if (e.vx === 0 && e.vy === 0) {
1369	      const dx = p.cx - e.cx, dy = p.cy - p.h / 4 - e.cy;
1370	      const d = Math.hypot(dx, dy) || 1;
1371	      e.vx = (dx / d) * 0.1; e.vy = (dy / d) * 0.1;
1372	    }
1373	    const spd = is405 ? 3 : 2;
1374	    const v = Math.hypot(e.vx, e.vy) || 1;
1375	    e.vx = (e.vx * 19 + (e.vx / v) * spd) / 20;
1376	    e.vy = (e.vy * 19 + (e.vy / v) * spd) / 20;
1377	    e.ai1 += 1;
1378	    if (e.ai1 > 180) { e.ai0 = 0; e.ai1 = 0; }
1379	    if (los) e.ai0 = 0;
1380	    // 每 5t 重试中转锚(:39160-39175):列锚需三方视线(原文 CanHit 重复两次照抄)
1381	    lai[0] += 1;
1382	    if (lai[0] >= 5 && !touchesSolid(game, e, 10)) {
1383	      lai[0] = 0;
1384	      if (losClear(game, e.cx, e.cy, p.cx, e.cy) && losClear(game, e.cx, e.cy, p.cx, e.cy)
1385	        && losClear(game, p.cx, p.cy, p.cx, e.cy)) {
1386	        e.ai0 = 3; e.ai1 = p.cx; e.ai2 = e.cy;
1387	      } else if (losClear(game, e.cx, e.cy, e.cx, p.cy) && losClear(game, p.cx, p.cy, e.cx, p.cy)) {
1388	        e.ai0 = 3; e.ai1 = e.cx; e.ai2 = p.cy;
1389	      }
1390	    }
1391	  }
1392	
1393	  if (flyPhase) fly(e);
1394	  else moveAndCollide(e, game.world, e.vx, e.vy);
1395	  starCellTail(e, game, is405);
1396	}
1397	
1398	/** AI_095 小星细胞 406(NPC.cs:41445-41492):无重力漂移减速,300t 线性长大
1399	 *  (scale 1→1.3)→ Transform 405;20t 起喷 226 号尘环(圈层随龄收窄)。 */
1400	export function smallStarCellAI(e: Enemy, game: GameHooks, _player: Player | null) {
1401	  const MAX = 300;
1402	  if (e.ai0 < 0) e.ai0 = 0;
1403	  if (Math.hypot(e.vx, e.vy) > 4) { e.vx *= 0.95; e.vy *= 0.95; }
1404	  e.vx *= 0.99; e.vy *= 0.99;
1405	  e.ai0 += 1;
1406	  e.vanillaScale = 1 + 0.3 * clamp(e.ai0 / MAX, 0, 1);   // :41455 scale
1407	  if (e.ai0 >= MAX) {
1408	    // Transform(405)(:41457-41461)——transformTo 埋块时会失败,下 tick 原地重试
1409	    e.transformTo(405, game.world.store, false, game);
1410	    return;
1411	  }
1412	  e.visAngle += e.vx * 0.1;
1413	  if (e.ai0 > 20) {
1414	    // 尘环(:41466-41490):tier=龄/150,半径 12-tier*2,半数概率
1415	    const tier = Math.floor(e.ai0 / (MAX / 2));
1416	    for (let k = 0; k < tier + 1; k++) {
1417	      if (rnd(2) === 0) continue;
1418	      const a = Math.random() * TAU;
1419	      const r = 12 - tier * 2;
1420	      game.spawnParticles(e.cx + Math.cos(a) * r, e.cy + Math.sin(a) * r,
1421	        k % 2 === 1 ? '#7FD8FF' : '#4FB8E8', 1, 1.5 * ((10 - tier * 2) / 10),
1422	        { life: 40, damp: 0.96 });
1423	    }
1424	  }
1425	  moveAndCollide(e, game.world, e.vx, e.vy);
1426	}
1427	
1428	/** AI_096 水流入侵者 407/408(NPC.cs:41493-41535):SimpleFlyMovement 悬顶伺服
1429	 *  (目标=玩家上方 250px,5 速 0.15 步进,近距减速档 0.35/0.65);每 70t 甩投射物 539
1430	 *  (近水平随机向,|vx|≥1.5,60 伤)。 */
1431	export function flowInvaderAI(e: Enemy, game: GameHooks, player: Player | null) {
1432	  const SPD = 5, ACC = 0.15;
1433	  if (e.ai0 < 0) e.ai0 = 0;
1434	  const p = player && !player.dead ? player : null;
1435	  if (p) {
1436	    const dx = p.cx - e.cx, dy = p.cy - 250 - e.cy;
1437	    const d = Math.hypot(dx, dy);
1438	    let dvx = e.vx, dvy = e.vy;                        // <20px:期望=现速(:41501-41503)
1439	    if (d >= 20 && d < 40) { dvx = (dx / d) * SPD * 0.35; dvy = (dy / d) * SPD * 0.35; }
1440	    else if (d >= 40 && d < 80) { dvx = (dx / d) * SPD * 0.65; dvy = (dy / d) * SPD * 0.65; }
1441	    else if (d >= 80) { dvx = (dx / d) * SPD; dvy = (dy / d) * SPD; }
1442	    e.vx += clamp(dvx - e.vx, -ACC, ACC);              // SimpleFlyMovement(:41523-41525)
1443	    e.vy += clamp(dvy - e.vy, -ACC, ACC);
1444	  }
1445	  e.visAngle = e.vx * 0.1;
1446	  e.ai0 += 1;
1447	  if (e.ai0 < 70) { moveAndCollide(e, game.world, e.vx, e.vy); return; }
1448	  e.ai0 = 0;
1449	  // 甩 539(:41528-41535):UnitY.RotatedByRandom(π/2)×(5,3),重掷至 |vx|≥1.5
1450	  let ox = 0, oy = 0;
1451	  do {
1452	    const a = Math.PI / 2 + (Math.random() * 2 - 1) * (Math.PI / 2);
1453	    ox = Math.cos(a) * 5; oy = Math.sin(a) * 3;
1454	  } while (Math.abs(ox) < 1.5);
1455	  (game as unknown as { entities: { add: (x: unknown, b: string) => void } }).entities.add(
1456	    new LunarOrb(e, 539, ox, oy, 60), 'projectiles');
1457	  moveAndCollide(e, game.world, e.vx, e.vy);
1458	}
1459	
1460	/** AI_AttemptToFindTeleportSpot(NPC.cs:18876-18946)收敛:AI_097 传参
1461	 *  (20,12,1,solidTileCheckCentered,teleportInAir)。原文 for 体尾 break → 每 attempt
1462	 *  只验一个候选格;距目标 2000px 以上直接放弃;落点 3×3 须净空、岩浆格排除、
1463	 *  落点外扩 12 tile 不得扫到玩家(telefrag 防护)。 */
1464	function findTeleportSpot(game: GameHooks, e: Enemy, p: Player): { x: number; y: number } | null {
1465	  const selfTx = Math.floor(e.cx / 16), selfTy = Math.floor(e.cy / 16);
1466	  const ptx = Math.floor(p.cx / 16), pty = Math.floor(p.cy / 16);
1467	  if (Math.abs(selfTx * 16 - ptx * 16) + Math.abs(selfTy * 16 - pty * 16) > 2000) return null;
1468	  const st = game.world.store;
1469	  for (let attempt = 0; attempt < 100; attempt++) {
1470	    const tx = ptx - 20 + rnd(41);
1471	    const ty = pty - 20 + rnd(41);
1472	    if (ty >= selfTy - 1 && ty <= selfTy + 1 && tx >= selfTx - 1 && tx <= selfTx + 1) continue;
1473	    if (st.inBounds(tx, ty - 1)) {                    // (tx,ty-1) 岩浆 → 弃
1474	      const li = st.idx(tx, ty - 1);
1475	      if (st.liquid[li] > 0 && st.liquidType[li] === 2) continue;
1476	    }
1477	    if (solidRect(game, tx - 1, ty - 1, tx + 1, ty + 1)) continue;   // 3×3 净空
1478	    // telefrag:落点 tile 外扩 12 tile vs 玩家 hitbox∪(hitbox+vel*20)
1479	    const inf = 12 * 16;
1480	    const rx0 = tx * 16 - inf, ry0 = ty * 16 - inf;
1481	    const rx1 = tx * 16 + 16 + inf, ry1 = ty * 16 + 16 + inf;
1482	    const px0 = p.x + Math.min(0, p.vx * 20), py0 = p.y + Math.min(0, p.vy * 20);
1483	    const px1 = p.x + p.w + Math.max(0, p.vx * 20), py1 = p.y + p.h + Math.max(0, p.vy * 20);
1484	    if (px0 < rx1 && px1 > rx0 && py0 < ry1 && py1 > ry0) continue;
1485	    return { x: tx, y: ty };
1486	  }
1487	  return null;
1488	}
1489	
1490	/** AI_097 星云悬浮脑 420(NPC.cs:41536-41750):noTileCollide 穿墙。开场 180t 每 60t
1491	 *  放环绕球 574(球每 180t 朝玩家线发 576 弹,8 速 65 伤);受击 1/6 概率瞬移
1492	 *  (StrikeNPC :82097 置 localAI[1]);480t 周期 AI_AttemptToFindTeleportSpot 落点
1493	 *  瞬移(起终双段尘爆 + 全场 574 球计时 -30);>400px 或断视线追击(7 速 30 步进),
1494	 *  否则滞空缓降。玩家失活 → ai[1]=1 渐隐消散(3t)。 */
1495	export function nebulaFloaterAI(e: Enemy, game: GameHooks, player: Player | null) {
1496	  const SPD = 7, TP_T = 480, ORB_DELAY = 30;
1497	  const lai = lunarLocalAI(e);
1498	  if (e.ai0 < 0) e.ai0 = 0;
1499	  const p = player && !player.dead ? player : null;
1500	  // ---- 开场环绕球(:41542-41554) ----
1501	  if (lai[2] < 180) {
1502	    lai[2] += 1;
1503	    if (lai[2] % 60 === 0) {
1504	      let ox = 0, oy = 0;
1505	      do {
1506	        const a = Math.PI / 2 + (Math.random() * 2 - 1) * (Math.PI / 2);
1507	        ox = Math.cos(a) * 4; oy = Math.sin(a) * 2.5;
1508	      } while (Math.abs(ox) < 1.5);
1509	      (game as unknown as { entities: { add: (x: unknown, b: string) => void } }).entities.add(
1510	        new LunarOrb(e, 574, ox, oy, 0), 'projectiles');
1511	    }
1512	  }
1513	  if (e.justHit) lai[1] = 1;                          // StrikeNPC(:82097)受击触发
1514	  if (lai[1] === 1) {
1515	    lai[1] = 0;
1516	    if (rnd(6) === 0) e.ai0 = TP_T;                   // :41556-41561 受击 1/6 立即瞬移
1517	  }
1518	  const dir = p ? e.seekDirX(p) : e.facing;           // TargetClosest(confused 反向)
1519	  if (!p) {                                           // 玩家失活 → 渐隐消散(:41566-41574)
1520	    e.ai0 = 0; e.ai1 = 1; e.ai2 = 0; e.ai3 = 0;
1521	  }
1522	  e.visAngle = Math.abs(e.vx) * dir * 0.1;            // rotation(:41576)
1523	  e.facing = -dir;                                    // spriteDirection=-direction
1524	  if (e.ai1 === 1) {
1525	    // ---- 消散段(:41582-41601):3t 倒数后 active=false ----
1526	    if (lai[3] === 0) {
1527	      lai[3] = 1; e.ai3 = 3;
1528	      // 消散音 = Item8（:41584 原文 PlaySound(SoundID.Item8)，与传送同款）。
1529	      // ★曾播 menuOpen(UI 菜单声)——"原键名拼错"的修补方向反了，应改真轨（审计 #22）
1530	      game.playSfxFiles(['Item_8'], 1, e.cx, e.cy);
1531	      game.spawnParticles(e.cx, e.cy, '#C060FF', 20, 3, { life: 40 });
1532	    }
1533	    e.ai3 -= 1;
1534	    if (e.ai3 <= 0) e.dead = true;
1535	    return;
1536	  }
1537	  if (!p) return;
1538	  const los = losClear(game, e.cx, e.cy, p.cx, p.cy); // flag103(:41581)
1539	  // 瞄点 = Center+(direction*20,6)(:41578-41580)
1540	  const ax = e.cx + dir * 20, ay = e.cy + 6;
1541	  const tdx = p.cx - ax, tdy = p.cy - ay;
1542	  const td = Math.hypot(tdx, tdy);
1543	  let hover = false;
1544	  if (td > 400 || !los) {
1545	    // 追击(:41603-41613):7 速钳制,30 步进
1546	    let mx = tdx, my = tdy;
1547	    const m = Math.hypot(mx, my);
1548	    if (m > SPD) { mx = (mx / m) * SPD; my = (my / m) * SPD; }
1549	    e.vx = (e.vx * 29 + mx) / 30;
1550	    e.vy = (e.vy * 29 + my) / 30;
1551	  } else {
1552	    e.vx *= 0.98; e.vy *= 0.98;                       // 视线内滞空缓降(:41615-41618)
1553	    hover = true;
1554	  }
1555	  // ---- 瞬移执行段(:41620-41644)：起终双端 Item8 + 尘 242 各 20（scale2.5 初速 ×3）----
1556	  if (e.ai2 !== 0 && e.ai3 !== 0) {
1557	    game.playSfxFiles?.(['Item_8'], 1, e.cx, e.cy);   // :41620 旧位置
1558	    game.spawnParticles(e.cx, e.cy, '#C060FF', 20, 3, { life: 40 });
1559	    e.x = e.ai2 * 16 - e.w / 2;                       // Center=(ai[2]*16, ai[3]*16)
1560	    e.y = e.ai3 * 16 - e.h / 2;
1561	    e.vx = 0; e.vy = 0;
1562	    e.ai2 = 0; e.ai3 = 0;
1563	    game.playSfxFiles?.(['Item_8'], 1, e.cx, e.cy);   // :41633 新位置
1564	    game.spawnParticles(e.cx, e.cy, '#C060FF', 20, 3, { life: 40 });
1565	  }
1566	  // ---- 瞬移周期(:41646-41693) ----
1567	  e.ai0 += 1;
1568	  if (e.ai0 >= TP_T) {
1569	    e.ai0 = 0;
1570	    const spot = findTeleportSpot(game, e, p);
1571	    if (spot) {
1572	      e.ai1 = 20;                                     // :41670(除 ==1 外无读者,照抄)
1573	      e.ai2 = spot.x; e.ai3 = spot.y;
1574	      // 全场自有 574 球计时 -30(原文 flag105 门 ai[0]<0 恒假 → 恒全量,:41673-41691)
1575	      const orbs = (game as unknown as { entities: { projectiles?: LunarOrb[] } })
1576	        .entities.projectiles;
1577	      if (Array.isArray(orbs)) {
1578	        for (const o of orbs) {
1579	          if (!o.dead && o instanceof LunarOrb && o.kind === 574 && o.parentId === e.id) {
1580	            o.delay(ORB_DELAY);
1581	          }
1582	        }
1583	      }
1584	    }
1585	  }
1586	  if (hover && Math.hypot(e.vx, e.vy) < 2) lai[0] += 1;   // :41695-41700(无消费者,照抄)
1587	  fly(e);                                             // noTileCollide=true
1588	}
1589	
1590	/** AI_099 日耀黏液 519(NPC.cs:41997-42056):自身重力 0.2(钳 12)坠落,贴图随速度
1591	 *  转向;落地(vy==0)→ 5t 定格(每 tick 回退到 oldPosition)→ HitEffect 自爆消亡
1592	 *  (active=false,不走掉落/扣盾)。519 专属火尘拖尾(6 号尘)。 */
1593	export function solarSlimeAI(e: Enemy, game: GameHooks, _player: Player | null) {
1594	  if (e.ai0 < 0) e.ai0 = 0;                           // Enemy 哨兵 -1120 归一,原版出生 0
1595	  if (e.vy === 0 && e.ai0 === 0) {                    // :41999-42005 落地门
1596	    e.ai0 = 1; e.ai1 = 0;
1597	    return;
1598	  }
1599	  if (e.ai0 === 1) {
1600	    // ---- 自爆定格(:42007-42014) ----
1601	    e.vx = 0; e.vy = 0;
1602	    e.x = e.prevX; e.y = e.prevY;                     // position=oldPosition
1603	    e.ai1 += 1;
1604	    if (e.ai1 >= 5) {
1605	      game.spawnParticles(e.cx, e.cy, '#FFB060', 26, 3.4, { life: 34, damp: 0.95 });
1606	      game.spawnParticles(e.cx, e.cy, '#FFE080', 18, 2.6, { life: 30, damp: 0.95 });
1607	      e.dead = true;                                  // HitEffect(0,9999)+active=false
1608	    }
1609	    return;
1610	  }
1611	  e.vy = Math.min(e.vy + 0.2, 12);                    // :42016-42020
1612	  e.visAngle = Math.atan2(e.vy, e.vx) - Math.PI / 2;  // rotation(:42022)
1613	  // 519 火尘(:42026-42055):首帧 13 粒爆发 + 每帧 3 粒 2/3 概率
1614	  if (lai0Of(e) === 0) {
1615	    setLai0(e, 1);
1616	    game.spawnParticles(e.cx, e.cy, '#FF9A3C', 13, 2.2, { life: 40, damp: 0.94 });
1617	  }
1618	  if (rnd(3) < 2) game.spawnParticles(e.cx, e.cy, Math.random() < 0.7 ? '#FF9A3C' : '#FFD24A',
1619	    1, 1.4, { life: 30, damp: 0.94 });
1620	  moveAndCollide(e, game.world, e.vx, e.vy);
1621	}
1622	
1623	/** 519 火尘首帧门(localAI[0] 复用) */
1624	function lai0Of(e: Enemy): number { return lunarLocalAI(e)[0]; }
1625	function setLai0(e: Enemy, v: number): void { lunarLocalAI(e)[0] = v; }
1626	
1627	// ---------------------------------------------------------------------------
1628	// AI_006 爬尾虫族 412/413/414（NPC.cs:51357-52671 的 412 专属段，1.4.5.6 1:1）
1629	//   头 412 首帧自建 30 段链（29×413 身 + 1×414 尾，:51764-51785 num35=30），
1630	//   全链 realLife=头（:51770/:51782——受击传导扣头 10000 总血，段不可单杀）；
1631	//   空泳追击环（flag3 恒 true :51955-51957）：玩家下方 15 格内有地面 → 目标改为
1632	//   地面上方 800px 悬停线，|dx|<500 时再沿速度向外推 ±600px 环绕（:52198-52208）；
1633	//   玩家悬空（下方无地）→ 直追且提速 10/0.3 → 14/0.5（:52211-52214）；
1634	//   速度带钳 [0.7n,1.3n]（:52216-52230）；同族头分离（:52232-52254，60/200 或
1635	//   400/1000）；段链收缩 linkDist = width+6（:52292-52294）；头火尘双粒（:52050-52067）。
1636	//   段完整性 + 414 红闪原版由各段独立跑 AI_006 承担；本仓段（wormBody）跳过 AI
1637	//   分发 → 头循环代行（:51807-51819 身/尾查前段 / :51850-51862 头/身查下段）。
1638	// ---------------------------------------------------------------------------
1639	
1640	/** 414 尾受击红闪一步（NPC.cs:52026-52047 纯函数化，仅 type 414）：
1641	 *  受击 → localAI[3]=3；localAI[2]>0 每 tick −16、过零翻 −128；负段 +16 回 0；
1642	 *  归零且 localAI[3]>0 → 重发 128 并消耗一发。渲染侧
1643	 *  Renderer.npcGlowCrawltipedeFlash 消费 e.lai2（n=trunc，负段 n=128+trunc，
1644	 *  RGB=(255-n,n,n)、A=255-n）——AI 侧必须按本节奏写 lai2，否则 Glow_159 红闪
1645	 *  永不触发。 */
1646	export function crawltipedeFlashStep(
1647	  lai2: number, lai3: number, justHit: boolean,
1648	): { lai2: number; lai3: number } {
1649	  if (justHit) lai3 = 3;                                              // :52027-52029 受击装填 3 发
1650	  if (lai2 > 0) {
1651	    lai2 -= 16;                                                       // :52030-52033 正段衰减
1652	    if (lai2 === 0) lai2 = -128;                                      // :52033-52035 过零翻转
1653	  } else if (lai2 < 0) {
1654	    lai2 += 16;                                                       // :52038-52040 负段回升
1655	  } else if (lai3 > 0) {
1656	    lai2 = 128;                                                       // :52041-52045 归零且有存货 → 重发
1657	    lai3 -= 1;
1658	  }
1659	  return { lai2, lai3 };
1660	}
1661	
1662	export function crawltipedeAI(e: Enemy, game: GameHooks, player: Player | null): void {
1663	  if (!e.bInit) {
1664	    e.bInit = true;
1665	    // :51764-51785 头首帧建链：num35=30 段（末段 414，其余 413）
1666	    const segs = enemySpawnChain(e, 30);
1667	    e.realLifeHost = e;
1668	    for (const s of segs) { s.realLifeHost = e; addEnemy(game, s); }
1669	  }
1670	  const st = game.world.store;
1671	  // ---- 段完整性与 414 红闪（原版各段独立自查，头循环代行）----
1672	  if (!e.wormNext || e.wormNext.dead) { e.die(game); return; }        // :51850-51862 头下段失效自灭
1673	  for (let s = e.wormNext; s; s = s.wormNext!) {
1674	    if (s.dead) continue;
1675	    const prevDead = !s.wormFollow || s.wormFollow.dead;              // :51807-51819（413/414 查前段）
1676	    const nextDead = s.vanillaId === 413 && (!s.wormNext || s.wormNext.dead); // :51850-51862（413 查下段）
1677	    if (prevDead || nextDead) { s.die(game); continue; }              // 同 tick 逐段级联
1678	    if (s.vanillaId === 414) {                                        // :52026-52047 尾段红闪
1679	      const f = crawltipedeFlashStep(s.lai2, s.lai3, s.justHit);
1680	      s.lai2 = f.lai2; s.lai3 = f.lai3;
1681	    }
1682	  }
1683	  // 无目标：缓漂（与 Enemy.wormAI 同近似，原版 TargetClosest 指向死亡槽位照飞）
1684	  if (!player) {
1685	    e.vx *= 0.97; e.vy *= 0.97;
1686	    e.x += e.vx; e.y += e.vy;
1687	    e.visAngle = Math.atan2(e.vy, e.vx) + Math.PI * 0.5;
1688	    return;
1689	  }
1690	  // ---- 头火尘双粒（:52050-52067：Center + (rotation−π/2)±8 ± rotation 向量×16，
1691	  //      位居舵机/rotation 赋值之前 → 读上一 tick 的 rotation，与本处取值一致）----
1692	  {
1693	    const fw = e.visAngle - Math.PI * 0.5;                            // (rotation − π/2).ToRotationVector2()
1694	    const mv = e.visAngle;                                            // rotation.ToRotationVector2()
1695	    game.spawnParticles(
1696	      e.cx + Math.cos(fw) * 8 + Math.cos(mv) * 16,
1697	      e.cy + Math.sin(fw) * 8 + Math.sin(mv) * 16,
1698	      '#FF9A3C', 1, 0.4, { life: 26, damp: 0.94 });
1699	    game.spawnParticles(
1700	      e.cx + Math.cos(fw) * 8 - Math.cos(mv) * 16,
1701	      e.cy + Math.sin(fw) * 8 - Math.sin(mv) * 16,
1702	      '#FF9A3C', 1, 0.4, { life: 26, damp: 0.94 });
1703	  }
1704	  // ---- 412 目标覆写（:52176-52254）----
1705	  let num46 = 10, num47 = 0.3;                                        // :52178-52179 基础速/加速
1706	  let tx = player.cx, ty = player.cy;                                 // num49/num50 初值 = 玩家中心（:52173-52175）
1707	  const ptx = Math.floor(player.cx / TILE), pty = Math.floor(player.cy / TILE);
1708	  let groundRow = -1;                                                 // num51：玩家下方首个实心行（:52180）
1709	  for (let dx = -2; dx <= 2; dx++) {                                  // :52183-52191 列 ±2 × 下 15 格
1710	    for (let dy = 0; dy <= 15; dy++) {
1711	      // WorldGen.SolidTile2（WorldGen.cs:70178——null tile 视为实心）→ 世界外按实心
1712	      if (!st.inBounds(ptx + dx, pty + dy) || st.isSolid(ptx + dx, pty + dy)) {
1713	        groundRow = pty + dy;
1714	        break;
1715	      }
1716	    }
1717	    if (groundRow > 0) break;                                         // :52193-52196 仅正行号中断外层
1718	  }
1719	  let sepDist = 60, sepPush = 200;                                    // num60/num61（:52232-52233）
1720	  if (groundRow > 0) {
1721	    const hoverY = groundRow * TILE - 800;                            // :52200-52201 num56 = num51×16 − 800
1722	    if (player.y > hoverY) {                                          // :52202 玩家顶低于悬停线
1723	      ty = hoverY;                                                    // :52204 目标改悬停线
1724	      if (Math.abs(e.cx - player.cx) < 500) {                         // :52205
1725	        tx = e.vx > 0 ? player.cx + 600 : player.cx - 600;            // :52207 沿速度向外推 600px 环绕
1726	      }
1727	    }
1728	    sepDist = 400; sepPush = 1000;                                    // :52234-52237 有地 → 分离加强
1729	  } else {
1730	    num46 = 14; num47 = 0.5;                                          // :52211-52214 玩家悬空 → 直追提速
1731	  }
1732	  // ---- 速度带钳 [0.7n, 1.3n]（:52216-52230，舵机前的存量速度）----
1733	  const spd = Math.hypot(e.vx, e.vy);
1734	  if (spd > 0) {
1735	    if (spd > num46 * 1.3) { e.vx = (e.vx / spd) * num46 * 1.3; e.vy = (e.vy / spd) * num46 * 1.3; }
1736	    else if (spd < num46 * 0.7) { e.vx = (e.vx / spd) * num46 * 0.7; e.vy = (e.vy / spd) * num46 * 0.7; }
1737	  }
1738	  // ---- 同族头分离（:52239-52254）：目标点沿远离方向推 sepPush ----
1739	  for (const o of enemies(game)) {
1740	    if (o === e || o.dead || o.vanillaId !== 412) continue;
1741	    const d = Math.hypot(o.cx - e.cx, o.cy - e.cy);
1742	    if (d > 0.01 && d < sepDist) {
1743	      tx -= ((o.cx - e.cx) / d) * sepPush;
1744	      ty -= ((o.cy - e.cy) / d) * sepPush;
1745	    }
1746	  }
1747	  // ---- 16px 量化（:52254-52259）----
1748	  const dxq = Math.floor(tx / TILE) * TILE - Math.floor(e.cx / TILE) * TILE;
1749	  const dyq = Math.floor(ty / TILE) * TILE - Math.floor(e.cy / TILE) * TILE;
1750	  // ---- 期望速度向量（:52396-52401 num68 = num46/num63）----
1751	  const dist = Math.hypot(dxq, dyq) || 1;
1752	  const ax = Math.abs(dxq), ay = Math.abs(dyq);                       // num66/num67（:52397-52398，均匀缩放下比较不变）
1753	  const wantX = (dxq / dist) * num46, wantY = (dyq / dist) * num46;
1754	  const step = num47;
1755	  // ---- 舵机（:52511-52583 的 !flag8 分支；flag8 仅 87/454/621 置位，412 恒 false）----
1756	  if ((e.vx > 0 && wantX > 0) || (e.vx < 0 && wantX < 0)
1757	    || (e.vy > 0 && wantY > 0) || (e.vy < 0 && wantY < 0)) {
1758	    if (e.vx < wantX) e.vx += step; else if (e.vx > wantX) e.vx -= step;
1759	    if (e.vy < wantY) e.vy += step; else if (e.vy > wantY) e.vy -= step;
1760	    if (Math.abs(wantY) < num46 * 0.2 && ((e.vx > 0 && wantX < 0) || (e.vx < 0 && wantX > 0))) {
1761	      if (e.vy > 0) e.vy += step * 2; else e.vy -= step * 2;
1762	    }
1763	    if (Math.abs(wantX) < num46 * 0.2 && ((e.vy > 0 && wantY < 0) || (e.vy < 0 && wantY > 0))) {
1764	      if (e.vx > 0) e.vx += step * 2; else e.vx -= step * 2;
1765	    }
1766	  } else if (ax > ay) {
1767	    if (e.vx < wantX) e.vx += step * 1.1; else if (e.vx > wantX) e.vx -= step * 1.1;
1768	    if (Math.abs(e.vx) + Math.abs(e.vy) < num46 * 0.5) {
1769	      if (e.vy > 0) e.vy += step; else e.vy -= step;
1770	    }
1771	  } else {
1772	    if (e.vy < wantY) e.vy += step * 1.1; else if (e.vy > wantY) e.vy -= step * 1.1;
1773	    if (Math.abs(e.vx) + Math.abs(e.vy) < num46 * 0.5) {
1774	      if (e.vx > 0) e.vx += step; else e.vx -= step;
1775	    }
1776	  }
1777	  e.facing = e.vx > 0 ? 1 : -1;
1778	  e.visAngle = Math.atan2(e.vy, e.vx) + Math.PI * 0.5;                // :52600 头 rotation
1779	  // ---- 位移（noTileCollide 直积分）----
1780	  e.x += e.vx; e.y += e.vy;
1781	  // ---- 段链收缩跟随（:52266-52323：rotation :52277 / num64=width+6 :52292-52294 /
1782	  for (let s = e.wormNext; s && !s.dead; s = s.wormNext!) {
1783	    const fx = s.wormFollow!;
1784	    const dxC = fx.cx - s.cx, dyC = fx.cy - s.cy;
1785	    const d = Math.hypot(dxC, dyC);
1786	    if (d > 0.01) {
1787	      const shrink = (d - (s.w + 6)) / d;                             // :52304 收缩比 = (dist−num64)/dist
1788	      s.x += dxC * shrink;
1789	      s.y += dyC * shrink;
1790	      s.visAngle = Math.atan2(dyC, dxC) + Math.PI * 0.5;              // :52277
1791	    }
1792	    s.facing = dxC < 0 ? 1 : -1;
1793	    s.vx = 0; s.vy = 0;                                               // :52307 velocity = Vector2.Zero
1794	  }
1795	}
1796	
1797	// ---------------------------------------------------------------------------
1798	// 环绕球投射物 539/574(Projectile.cs:5864-5878 SetDefaults + AI_102 :32040-32280)
1799	//  539(水流入侵者 407 甩出):绕父 407 盘旋 210t(0.15/0.075 符号步进钳 6,随父位移),
1800	//    到点取最近玩家方向(±50px 抖动 ×0.8-1.2)以 16 速直冲;亡时(撞块/到期)80×80
1801	//    范围 60 伤(:69366-69405)。
1802	//  574(悬浮脑 420 环绕):随 420 存活;每 180t 且对玩家 CanHitLine → 线发 576 弹
1803	//    (8 速 65 伤)后重置计时继续盘旋;悬浮脑瞬移时全量计时 -30(accelerate)。
1804	// ---------------------------------------------------------------------------
1805	export class LunarOrb extends Entity {
1806	  w = 18; h = 18;
1807	  vx: number; vy: number;
1808	  readonly kind: 539 | 574;
1809	  readonly parentId: number;
1810	  /** v6 联机：父体 netId（访客端父=msg23 傀儡；0=本端真身走 parentId 查找） */
1811	  parentNetId = 0;
1812	  private ai0 = 0;
1813	  private dmg: number;
1814	  private life = 600;
1815	  private frame = 0;
1816	  private frameT = 0;
1817	  dead = false;
1818	
1819	  constructor(parent: Enemy | null, kind: 539 | 574, vx: number, vy: number, dmg: number, x?: number, y?: number) {
1820	    super();
1821	    this.kind = kind;
1822	    this.parentId = parent?.id ?? 0;
1823	    this.vx = vx; this.vy = vy;
1824	    this.dmg = dmg;
1825	    if (kind === 539) { this.w = 18; this.h = 30; }
1826	    // v6 傀儡重建：parent=null 时由调用方传显式坐标
1827	    this.x = (x ?? parent!.cx) - this.w / 2;
1828	    this.y = (y ?? parent!.cy) - this.h / 2;
1829	  }
1830	
1831	  /** v6 联机打包：kind=8，tag=`${539|574},${parentId}`。
1832	   *  访客重建后本地跑盘旋/冲刺/爆炸（确定性自包含，父=傀儡）；
1833	   *  574 的线发 576 弹经 !netPuppet 门禁排除（房主侧已发） */
1834	  netProjMeta(): NetProjMeta {
1835	    return { kind: 8, tag: `${this.kind},${this.parentId}`, aux: 0, dmg: this.dmg };
1836	  }
1837	
1838	  /** 悬浮脑瞬移同步:全场计时 -30(:41682-41691) */
1839	  delay(t: number): void { this.ai0 -= t; }
1840	
1841	  fixedUpdate(_dt: number, game: GameHooks): void {
1842	    // v6 联机：傀儡端按 netId 找父（msg23 傀儡）；本端真身按本地 id
1843	    const parent = this.parentNetId
1844	      ? (game.enemies() as Enemy[]).find((n) => n.netId === this.parentNetId)
1845	      : (game.enemies() as Enemy[]).find((n) => n.id === this.parentId);
1846	    const orbitT = this.kind === 539 ? 210 : 180;
1847	    const alive = !!parent && !parent.dead;
1848	    if (this.kind === 574 && !alive) { this.dead = true; return; }   // :32083-32092
1849	    this.ai0 += 1;
1850	    if (this.life-- <= 0) { this.explode(game); return; }
1851	    if (this.ai0 < orbitT && alive) {
1852	      // 盘旋:随父位移 + 符号步进逼近父心(钳 6)(:32100-32118)
1853	      this.x += parent!.x - parent!.prevX;
1854	      this.y += parent!.y - parent!.prevY;
1855	      this.vx += Math.sign(parent!.cx - this.cx) * 0.15;
1856	      this.vy += Math.sign(parent!.cy - this.cy) * 0.075;
1857	      const v = Math.hypot(this.vx, this.vy);
1858	      if (v > 6) { this.vx = (this.vx / v) * 6; this.vy = (this.vy / v) * 6; }
1859	      if (this.kind === 539 && ++this.frameT >= 4) { this.frameT = 0; this.frame++; }
1860	    } else if (this.ai0 === orbitT) {
1861	      const p = game.player;
1862	      if (this.kind === 539) {
1863	        // 直冲最近玩家(:32185-32212):方向 ±50px 抖动 ×0.8-1.2,16 速
1864	        const tx = p.cx + (Math.random() * 100 - 50), ty = p.cy + (Math.random() * 100 - 50);
1865	        const kx = 0.8 + Math.random() * 0.4, ky = 0.8 + Math.random() * 0.4;
1866	        const dx = (tx - this.cx) * kx, dy = (ty - this.cy) * ky;
1867	        const d = Math.hypot(dx, dy) || 1;
1868	        this.vx = (dx / d) * 16; this.vy = (dy / d) * 16;
1869	      } else {
1870	        // 线发 576 弹(:32204-32211):CanHitLine 门,8 速 65 伤;发射后重置计时。
1871	        // v6 傀儡不本地线发——房主的 576 弹经 msg27 同步,双端各发会翻倍
1872	        if (!this.netPuppet && !p.dead && canHitLine(game.world.store, this.cx, this.cy, 0, 0, p.cx, p.cy, 0, 0)) {
1873	          const dx = p.cx - this.cx, dy = p.cy - this.cy;
1874	          const d = Math.hypot(dx, dy) || 1;
1875	          (game as unknown as { entities: { add: (x: unknown, b: string) => void } }).entities.add(
1876	            new Arrow(this.cx, this.cy, (dx / d) * 8, (dy / d) * 8, 65, 0, 576, null,
1877	              { grav: 0, life: 600, pierce: 1, hostile: true }), 'projectiles');
1878	        }
1879	        this.ai0 = 0;
1880	      }
1881	    }
1882	    if (this.kind === 539 && this.ai0 > orbitT && ++this.frameT >= 2) {
1883	      this.frameT = 0; this.frame++;                  // 冲刺段帧率加倍(:32227-32235)
1884	    }
1885	    this.x += this.vx; this.y += this.vy;             // 539 tileCollide / 574 穿墙
1886	    if (this.kind === 539) {
1887	      const st = game.world.store;
1888	      const tx = Math.floor(this.cx / TILE), ty = Math.floor(this.cy / TILE);
1889	      if (st.inBounds(tx, ty) && st.isSolid(tx, ty)) { this.explode(game); return; }
1890	    }
1891	  }
1892	
1893	  /** 539 亡时 80×80 范围伤害 + 尘爆(:69366-69405) */
1894	  private explode(game: GameHooks): void {
1895	    this.dead = true;
1896	    game.spawnParticles(this.cx, this.cy, '#8FE8FF', 20, 3.4, { life: 40, damp: 0.94 });
1897	    game.spawnParticles(this.cx, this.cy, '#4FB8E8', 10, 2.2, { life: 36, damp: 0.94 });
1898	    const p = game.player;
1899	    if (p && !p.dead && this.dmg > 0) {
1900	      const half = 40;                                // 80×80 居中
1901	      if (p.x < this.cx + half && p.x + p.w > this.cx - half
1902	        && p.y < this.cy + half && p.y + p.h > this.cy - half) {
1903	        game.damagePlayer(this.dmg, this.cx, this.cy, null);
1904	      }
1905	    }
1906	  }
1907	
1908	  draw(r: Renderer, _cam: Camera): void {
1909	    const ctx = r.canvas.getContext('2d');
1910	    if (!ctx) return;
1911	    const img = projFrameImg(this.kind, this.kind === 574 ? 1 : this.frame);
1912	    ctx.save();
1913	    ctx.translate(this.cx, this.cy);
1914	    // 539 旋转分两段（AI_102）：盘旋期 vx*0.1（:32135）/冲刺期向 ToRotation+π/2 收敛
1915	    // （:32230 AngleLerp 0.4）;574 向瞄准向 ToRotation+π/2 收敛（:32167）。此处 539 恒用
1916	    // 盘旋档（冲刺段姿态差登记偏差）
1917	    ctx.rotate(this.kind === 539 ? this.vx * 0.1 : Math.atan2(this.vy, this.vx) + Math.PI / 2);
1918	    ctx.imageSmoothingEnabled = false;
1919	    if (img) {
1920	      // 原生帧 × scale=1（SetDefaults 539/574 无 scale;origin = 帧格 Size/2,Main.cs:32812
1921	      // 列表族 :32889）。曾归一到判定盒 18×30/18×18 → 539 纵横比失真（G11）
1922	      ctx.drawImage(img, -img.width / 2, -img.height / 2, img.width, img.height);
1923	    } else {
1924	      ctx.fillStyle = this.kind === 539 ? '#8FE8FF' : '#C060FF';
1925	      ctx.fillRect(-this.w / 2, -this.h / 2, this.w, this.h);
1926	    }
1927	    ctx.restore();
1928	  }

```


---

## 🤖 Assistant · 2026-08-19T03:10:20.970Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I've read the entire file. Now let me read the vanilla sections. Priority order:

1. moonLordFreeEyeAI: NPC.cs 38224-38667
2. moonLeechAI: 38668-38792
3. cultistTabletAI: 38793-38962 (aiStyle 83)
4. phantomAI: 39261-39519
5. bigMimicAI: 39520-39875
6. mothronAI: 39876-40406, mothronEggAI: 40407-40449, babyMothronAI: 40450-40685
7. graniteElementalAI: 40686-40870; starCellAI: 38967-39220; smallStarCellAI: 41445-41492; flowInvaderAI: 41493-41535; nebulaFloaterAI: 41536-41750; solarSlimeAI: 41997-42056; crawltipedeAI: 51357-52671 (412 segment).

Let me read the vanilla sections with sed. Start with 38224-38667 (444 lines).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:21.532Z · glm-x-preview-260804

```
文件已读取 (1929 行)。现在我来拉取各个 AI 家族的原版权威代码段，从月总游离眼 (38224-38667) 开始。
```


---

## 🤖 Assistant · 2026-08-19T03:10:22.057Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38224,38350p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla MoonLord free eye AI part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:22.098Z

**📎 ToolResult**

```
		else if (aiStyle == 81)
		{
			if (Main.rand.Next(420) == 0)
			{
				SoundEngine.PlaySound(29, (int)base.Center.X, (int)base.Center.Y, Main.rand.Next(100, 101));
			}
			Vector2 vector218 = new Vector2(30f);
			if (!Main.npc[(int)this.ai[3]].active || Main.npc[(int)this.ai[3]].type != 398)
			{
				life = 0;
				HitEffect();
				active = false;
			}
			float num1294 = 0f;
			float num1295 = 0f;
			float num1296 = this.ai[0];
			this.ai[1]++;
			int num1297 = 0;
			int num1298 = 0;
			for (; num1297 < 10; num1297++)
			{
				num1295 = MoonLordAttacksArray2[1, num1297];
				if (!(num1295 + (float)num1298 <= this.ai[1]))
				{
					break;
				}
				num1298 += (int)num1295;
			}
			if (num1297 == 10)
			{
				num1297 = 0;
				this.ai[1] = 0f;
				num1295 = MoonLordAttacksArray2[1, num1297];
				num1298 = 0;
			}
			this.ai[0] = MoonLordAttacksArray2[0, num1297];
			num1294 = (int)this.ai[1] - num1298;
			if (this.ai[0] != num1296)
			{
				netUpdate = true;
			}
			if (this.ai[0] == -1f)
			{
				this.ai[1]++;
				if (this.ai[1] > 180f)
				{
					this.ai[1] = 0f;
				}
				float num1299 = 1f;
				if (this.ai[1] < 60f)
				{
					num1299 = 0.75f;
					localAI[0] = 0f;
					localAI[1] = (float)Math.Sin(this.ai[1] * (MathF.PI * 2f) / 15f) * 0.35f;
					if (localAI[1] < 0f)
					{
						localAI[0] = MathF.PI;
					}
				}
				else if (this.ai[1] < 120f)
				{
					num1299 = 1f;
					if (localAI[1] < 0.5f)
					{
						localAI[1] += 0.025f;
					}
					localAI[0] += MathF.PI / 15f;
				}
				else
				{
					num1299 = 1.15f;
					localAI[1] -= 0.05f;
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
				}
				localAI[2] = MathHelper.Lerp(localAI[2], num1299, 0.3f);
			}
			if (this.ai[0] == 0f)
			{
				TargetClosest(faceTarget: false);
				Vector2 v11 = Main.player[target].Center + Main.player[target].velocity * 20f - base.Center;
				localAI[0] = localAI[0].AngleLerp(v11.ToRotation(), 0.5f);
				localAI[1] += 0.05f;
				if (localAI[1] > 0.7f)
				{
					localAI[1] = 0.7f;
				}
				localAI[2] = MathHelper.Lerp(localAI[2], 1f, 0.2f);
				float num1300 = 24f;
				Vector2 center36 = base.Center;
				Vector2 center37 = Main.player[target].Center;
				Vector2 vector219 = center37 - center36;
				Vector2 vector220 = vector219 - Vector2.UnitY * 200f;
				vector220 = Vector2.Normalize(vector220) * num1300;
				int num1301 = 30;
				velocity.X = (velocity.X * (float)(num1301 - 1) + vector220.X) / (float)num1301;
				velocity.Y = (velocity.Y * (float)(num1301 - 1) + vector220.Y) / (float)num1301;
				float num1302 = 0.25f;
				for (int num1303 = 0; num1303 < Main.maxNPCs; num1303++)
				{
					if (num1303 != whoAmI && Main.npc[num1303].active && Main.npc[num1303].type == 400 && Vector2.Distance(base.Center, Main.npc[num1303].Center) < 150f)
					{
						if (position.X < Main.npc[num1303].position.X)
						{
							velocity.X -= num1302;
						}
						else
						{
							velocity.X += num1302;
						}
						if (position.Y < Main.npc[num1303].position.Y)
						{
							velocity.Y -= num1302;
						}
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

```


---

## 🤖 Assistant · 2026-08-19T03:10:25.937Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Continuing reading the vanilla. Next: 38350-38520.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:26.353Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38350,38520p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla MoonLord free eye AI part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:26.404Z

**📎 ToolResult**

```
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
				else if (num1294 < 75f)
				{
					float num1304 = (num1294 - 15f) / 10f;
					int num1305 = 0;
					int num1306 = 0;
					switch ((int)num1304)
					{
					case 0:
						num1305 = 0;
						num1306 = 2;
						break;
					case 1:
						num1305 = 2;
						num1306 = 5;
						break;
					case 2:
						num1305 = 5;
						num1306 = 3;
						break;
					case 3:
						num1305 = 3;
						num1306 = 1;
						break;
					case 4:
						num1305 = 1;
						num1306 = 4;
						break;
					case 5:
						num1305 = 4;
						num1306 = 0;
						break;
					}
					Vector2 spinningpoint10 = Vector2.UnitY * -30f;
					Vector2 value6 = spinningpoint10.RotatedBy((float)num1305 * (MathF.PI * 2f) / 6f);
					Vector2 value7 = spinningpoint10.RotatedBy((float)num1306 * (MathF.PI * 2f) / 6f);
					Vector2 vector223 = Vector2.Lerp(value6, value7, num1304 - (float)(int)num1304);
					float value8 = vector223.Length() / 30f;
					localAI[0] = vector223.ToRotation();
					localAI[1] = MathHelper.Lerp(localAI[1], value8, 0.5f);
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
					for (int num1311 = 0; num1311 < 1000; num1311++)
					{
						Projectile projectile9 = Main.projectile[num1311];
						if (projectile9.active && projectile9.type == 454 && projectile9.ai[1] == (float)whoAmI && projectile9.ai[0] != -1f)
						{
							projectile9.ai[0] = -1f;
							projectile9.velocity = vector224;
							projectile9.netUpdate = true;
						}
					}
				}
				else
				{
					velocity *= 0.92f;
					rotation = rotation.AngleLerp(0f, 0.2f);
				}
			}
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

```


---

## 🤖 Assistant · 2026-08-19T03:10:38.057Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note: at num1294 < 120f (the 105-120 segment), vanilla:
- PlaySound(29, ..., 102) every tick in that window
- vector224 = (ai[2] - π/2).ToRotationVector2() * 12; velocity = vector224 * 2 → speed 24. Our impl: `e.vx = Math.cos(e.ai2 - Math.PI / 2) * 24;` — same (12*2=24). OK.

Note: our impl plays 'Zombie_102' every tick in t<120 && t>=105 window — vanilla also plays every tick in that window. OK.

Also in num1294 < 105 segment: `if (num1294 == 75f)` — sets vy = -7. Our impl: `if (t === 75) { e.vx = 0; e.vy = -7; }` — vanilla sets `velocity = Vector2.UnitY * -7f` which zeroes vx too. OK.

Continue reading 38520-38667.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:38.470Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38520,38667p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla MoonLord free eye AI part 3"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:38.502Z

**📎 ToolResult**

```
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
					if (localAI[1] < 0f)
					{
						localAI[1] = 0f;
					}
				}
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:10:59.903Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Free eye AI looks mostly 1:1. Let me check some details:

1. Attack table: our ML_EYE_ATTACKS = [[0,90],[1,90],[0,90],[2,135],[0,90],[3,200],[0,90],[4,375],[0,90],[2,135]]. Let me verify against MoonLordAttacksArray2 in NPC.cs :6966-6985.

2. State 3 spiral: vanilla at `num1294 == 45f` sets ai[2] = random direction * π*2/40. Our impl matches. `(num1294 - 15 - 30) % 40 == 0` → t-45 % 40. Our impl `(t - 45) % 40 === 0`. OK.

Note: num1312 = Lerp(8, 20, (num1294-15-30)/140) → our lerp(8,20,(t-45)/140). OK.

Projectile 452 spawn position: Center + Normalize(vector225) * vector218.Length() * 0.4 = 30*0.4=12. Our: 12. OK.

3. Deathray damage: vanilla NewProjectile 455, 50 damage. Our MLDeathray passes 50*2 = 100?? Hmm — "50 伤×2". In expert mode damage scales. Actually the comment says 50 伤×2 — meaning the MLDeathray class multiplies by 2 somewhere? Let me check MLDeathray's constructor in bossAI_duke_moonlord.ts. Actually the vanilla projectile damage 50; the ML deathray proj damage would be further scaled by difficulty in vanilla via NPC damage scaling. But we pass 100. Hmm, that could be a legit deliberate choice (the projectile 'core' variant used by the Moon Lord core uses 100?). Actually in vanilla, Moon Lord core also shoots 455 with damage 50. Expert mode ×2 damage for projectiles? Actually vanilla: projectile damage passed is used directly in normal mode. Let me check the MLDeathray constructor to see if it applies its own scaling.

4. Sound 29 style: Main.rand.Next(100,101) = always 100. Our: 'Zombie_100'. OK.

5. State 4 charge particles: vanilla uses dust 229 with custom velocity toward center; ours approximates. Fine (visual).

6. In state 0 hover: ours `e.vx = (e.vx * 29 + tx) / 30;` OK.

7. `TargetClosest(faceTarget: false)` — sets target to closest player. Ours uses `player` (the game's player). OK-ish.

8. The ai[0]==-1 branch: unreachable because table only contains 0..4. Confirmed table values 0,1,0,2,0,3,0,4,0,2. So -1 unreachable. Good.

Let me now verify MoonLordAttacksArray2 at 6966-6985.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:00.358Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '6960,6990p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read MoonLordAttacksArray2 table"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:00.390Z

**📎 ToolResult**

```
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

## 🤖 Assistant · 2026-08-19T03:11:06.165Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Table matches exactly. Now check the MLDeathray constructor briefly to see damage semantics — but the audit target is this file. The 50*2 might be a deliberate doubling to account for projectile damage vs. NPC-scaled damage in expert? Vanilla 455 damage is 50. But wait — is there a possibility that in 1.4.5.6, NPC.damage for the projectile from free eye is different? The NewProjectile call: type 455, damage 50. Our passes 100. Let me quickly check MLDeathray class constructor to see how dmg param is used.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:06.694Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"class MLDeathray\" -A 40 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts | head -60",
 "description": "Check MLDeathray constructor damage semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:06.732Z

**📎 ToolResult**

```
998:export class MLDeathray extends Entity {
999-  w = 36; h = 36; // SetDefaults 455
1000-  private srcId: number;
1001-  /** v6 联机：锚定 NPC 的 netId（访客端锚=msg23 傀儡；0=本端真身走 srcId 查找） */
1002-  srcNetId = 0;
1003-  /** 'head' = 396 头眼 / 'core' = 400 真眼(本仓折叠到核心 398) */
1004-  private kind: 'head' | 'core';
1005-  /** 扫射角速度(原版 ai[0] = ±2π/540) */
1006-  private sweep: number;
1007-  /** 当前束角(原版 velocity.ToRotation,每 tick +sweep) */
1008-  private angle: number;
1009-  private age = 0;
1010-  /** 束长 Lerp 值(原版 localAI[1]) */
1011-  private len = 0;
1012-  private dmg: number;
1013-  dead = false;
1014-
1015-  constructor(src: Enemy | null, kind: 'head' | 'core', angle: number, sweep: number, dmg: number, x?: number, y?: number) {
1016-    super();
1017-    this.srcId = src?.id ?? 0;
1018-    this.kind = kind;
1019-    this.angle = angle;
1020-    this.sweep = sweep;
1021-    this.dmg = dmg;
1022-    // v6 傀儡重建：src=null 时由调用方传显式坐标（真身路径 src 必非空）
1023-    this.x = (x ?? src!.cx) - this.w / 2;
1024-    this.y = (y ?? src!.cy) - this.h / 2;
1025-  }
1026-
1027-  /** v6 联机打包：kind=7，tag=`${srcId},${0|1 数值位（0=head 1=core）}`，aux=扫速×10000，
1028-   *  束角经 vx/vy 通道携带（重建端 atan2 还原后本地扫射——确定性自包含） */
1029-  netProjMeta(): NetProjMeta {
1030-    return {
1031-      kind: 7,
1032-      tag: `${this.srcId},${this.kind === 'head' ? 0 : 1}`,
1033-      aux: Math.max(-32768, Math.min(32767, Math.round(this.sweep * 10000))),
1034-      dmg: this.dmg,
1035-      exVx: Math.cos(this.angle) * 1000,
1036-      exVy: Math.sin(this.angle) * 1000,
1037-    };
1038-  }

```


---

## 🤖 Assistant · 2026-08-19T03:11:10.527Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The MLDeathray uses dmg directly. So our free eye passes 50*2=100. What does the 'core' kind (from Moon Lord core 398 in bossAI_duke_moonlord.ts) pass? Let me check how the core spawns it there — to see whether 100 is consistent with the core variant (which is presumably already audited). Actually the vanilla 455 damage is 50 for both. In our port, NPC damage values may have been doubled to account for something (like "damage doubled since our damage application halves"?). Let me check what the core passes.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:11.494Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"MLDeathray(\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts | head; grep -rn \"MLDeathray(\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | grep -v duke_moonlord | head",
 "description": "Find all MLDeathray spawn sites and damage values"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:11.550Z

**📎 ToolResult**

```
1154:  addProj(game, new MLDeathray(src, kind, ang, n * (TAU / 540), dmg));
(eval):1: no matches found: --include=*.ts

```


---

## 🤖 Assistant · 2026-08-19T03:11:16.653Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 1100,1165p ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "description": "Read moonlord deathray spawn helper context"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:16.676Z

**📎 ToolResult**

```
      let d = 2400;
      for (let i = 1; i <= steps; i++) {
        const t = i * 8;
        const tx = Math.floor((ox + dirX * t) / TILE), ty = Math.floor((oy + dirY * t) / TILE);
        const st = game.world.store;
        if (!st.inBounds(tx, ty)) { d = t - 8; break; }
        if (st.isSolid(tx, ty)) { d = t - 8; break; }
      }
      sum += d;
    }
    return sum / 3;
  }

  draw(r: Renderer, _cam: Camera): void {
    const ctx = r.canvas.getContext('2d');
    if (!ctx) return;
    const scale = Math.min(this.maxScale, Math.sin((this.age * Math.PI) / 180) * 10 * this.maxScale);
    if (scale <= 0.01 || this.len <= 1) return;
    const thick = Math.max(2, 36 * scale);
    ctx.save();
    ctx.globalAlpha = clamp(scale * 1.6, 0.25, 1);
    ctx.translate(this.cx, this.cy);
    ctx.rotate(this.angle);
    ctx.fillStyle = '#B040D0';
    ctx.fillRect(0, -thick / 2, this.len, thick);
    ctx.globalAlpha = clamp(scale * 0.9, 0.15, 0.6);
    ctx.fillStyle = '#F0C8FF';
    ctx.fillRect(0, -thick / 4, this.len, thick / 2);
    ctx.restore();
  }
}

/** 线段 vs AABB(原版 Collision.CheckAABBvLineCollision 语义:线宽胶囊与矩形相交) */
function segHitsRect(x0: number, y0: number, dx: number, dy: number, width: number,
  t: { x: number; y: number; w: number; h: number }): boolean {
  // 最近点参数 t∈[0,1](钳到段内)
  const cx = t.x + t.w / 2, cy = t.y + t.h / 2;
  const len2 = dx * dx + dy * dy || 1;
  let k = ((cx - x0) * dx + (cy - y0) * dy) / len2;
  k = clamp(k, 0, 1);
  const px = x0 + dx * k, py = y0 + dy * k;
  // 最近点到矩形距离(逐轴钳位)
  const nx = clamp(px, t.x, t.x + t.w), ny = clamp(py, t.y, t.y + t.h);
  return Math.hypot(px - nx, py - ny) < width / 2;
}

/** 死亡之光发射出口(原版 :37902-37916 头 / :38625-38637 真眼):
 *  起角 = 朝玩家角 ∓ 60°(num1278 = 玩家在左 +1),角速度 = num1278·2π/540。
 *  返回源 NPC 的扫射编码角初值((起角+3π)·num1278,头部 ai2 逐 t 解码步进用)。 */
function mlDeathray(game: GameHooks, src: Enemy, kind: 'head' | 'core', player: Player, dmg: number): number {
  const dx = player.cx - src.cx, dy = player.cy - src.cy;
  const d = Math.hypot(dx, dy) || 1;
  const n = dx / d < 0 ? 1 : -1;                       // num1278
  const ang = Math.atan2(dy, dx) - n * (TAU / 6);
  addProj(game, new MLDeathray(src, kind, ang, n * (TAU / 540), dmg));
  return (ang + Math.PI * 3) * n;
}

/** 核心悬停移动(:36854-36865 / :36912-36923 同构):目标 = 玩家 + (0,130),8 速/0.5 步进+半程混合 */
function mlCoreHover(e: Enemy, player: Player) {
  const dx = player.cx - e.cx;
  const dy = player.cy + 130 - e.cy;
  if (Math.hypot(dx, dy) > 20) {
    const d = Math.hypot(dx - e.vx, dy - e.vy) || 1;
    flyLerp(e, ((dx - e.vx) / d) * 8, ((dy - e.vy) / d) * 8, 0.5);
  }

```


---

## 🤖 Assistant · 2026-08-19T03:11:19.408Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Where is mlDeathray called with what dmg? Let me grep mlDeathray( calls.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:19.683Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"mlDeathray(\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "description": "Find mlDeathray call sites with damage args"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:19.709Z

**📎 ToolResult**

```
1149:function mlDeathray(game: GameHooks, src: Enemy, kind: 'head' | 'core', player: Player, dmg: number): number {
1303:      if (inSlot === 180) { e.ai2 = mlDeathray(game, e, 'core', player, 50 * 2); }
1570:        e.ai2 = mlDeathray(game, e, 'head', player, 75 * 2); // :37913 扫射编码角初值

```


---

## 🤖 Assistant · 2026-08-19T03:11:25.535Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The core deathray (from Moon Lord core 398) uses 50*2 as well, and head uses 75*2. Vanilla head 455 damage: let me check :37902-37916 to see — head spawns with 75? Probably. And the doubling might be a project-wide convention to counteract a damage application halving (or deliberate expert scaling). Both use ×2 consistently, and core was already audited in an earlier batch (boss-audit). So the free eye passing 50*2 matches the project convention. Not a deviation to report (consistent internal convention; likely registered).

Now moonLeechAI: read vanilla 38668-38792.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:26.039Z · glm-x-preview-260804

```
已确认月总游离眼的攻击表准确无误。现在来读取水蛭块 (38668-38792) 的代码。
```


---

## 🤖 Assistant · 2026-08-19T03:11:26.500Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38668,38800p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla MoonLord leech AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:26.530Z

**📎 ToolResult**

```
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
							}
							if (num1325 != -1 && num1326 != -1 && num1327 != -1)
							{
								break;
							}
						}
					}
					int num1329 = 1000;
					int num1330 = Main.npc[num1324].lifeMax - Main.npc[num1324].life;
					int num1331 = Main.npc[num1325].lifeMax - Main.npc[num1325].life;
					int num1332 = Main.npc[num1326].lifeMax - Main.npc[num1326].life;
					int num1333 = Main.npc[num1327].lifeMax - Main.npc[num1327].life;
					if (num1333 > 0 && num1329 > 0)
					{
						int num1334 = num1333 - num1329;
						if (num1334 > 0)
						{
							num1334 = 0;
						}
						int num1335 = num1329 + num1334;
						num1329 -= num1335;
						NPC nPC3 = Main.npc[num1327];
						nPC3.life += num1335;
						HealEffect(Utils.CenteredRectangle(Main.npc[num1327].Center, new Vector2(50f)), num1335);
					}
					if (num1330 > 0 && num1329 > 0)
					{
						int num1336 = num1330 - num1329;
						if (num1336 > 0)
						{
							num1336 = 0;
						}
						int num1337 = num1329 + num1336;
						num1329 -= num1337;
						NPC nPC3 = Main.npc[num1324];
						nPC3.life += num1337;
						HealEffect(Utils.CenteredRectangle(Main.npc[num1324].Center, new Vector2(50f)), num1337);
					}
					if (num1331 > 0 && num1329 > 0)
					{
						int num1338 = num1331 - num1329;
						if (num1338 > 0)
						{
							num1338 = 0;
						}
						int num1339 = num1329 + num1338;
						num1329 -= num1339;
						NPC nPC3 = Main.npc[num1325];
						nPC3.life += num1339;
						HealEffect(Utils.CenteredRectangle(Main.npc[num1325].Center, new Vector2(50f)), num1339);
					}
					if (num1332 > 0 && num1329 > 0)
					{
						int num1340 = num1332 - num1329;
						if (num1340 > 0)
						{
							num1340 = 0;
						}
						int num1341 = num1329 + num1340;
						num1329 -= num1341;
						NPC nPC3 = Main.npc[num1326];
						nPC3.life += num1341;
						HealEffect(Utils.CenteredRectangle(Main.npc[num1326].Center, new Vector2(50f)), num1341);
					}
				}
				life = 0;
				HitEffect();
				active = false;
			}
			else
			{
				velocity = Vector2.Zero;
				base.Center = Vector2.Lerp(Main.projectile[num1323].Center, Main.npc[(int)Math.Abs(this.ai[0]) - 1].Center + vector229, this.ai[2] / num1321);
				Vector2 spinningpoint12 = Vector2.UnitY * -height / 2f;
				for (int num1342 = 0; num1342 < 6; num1342++)
				{
					int num1343 = Dust.NewDust(base.Center - Vector2.One * 4f + spinningpoint12.RotatedBy((float)num1342 * (MathF.PI * 2f) / 6f), 0, 0, 229);
					Main.dust[num1343].velocity = -Vector2.UnitY;
					Main.dust[num1343].noGravity = true;
					Main.dust[num1343].scale = 0.7f;
					Main.dust[num1343].customData = this;
				}
				spinningpoint12 = Vector2.UnitY * -height / 6f;
				for (int num1344 = 0; num1344 < 3; num1344++)
				{
					int num1345 = Dust.NewDust(base.Center - Vector2.One * 4f + spinningpoint12.RotatedBy((float)num1344 * (MathF.PI * 2f) / 6f), 0, 0, 229, 0f, -2f);
					Main.dust[num1345].noGravity = true;
					Main.dust[num1345].scale = 1.5f;
					Main.dust[num1345].customData = this;
				}
			}
		}
		else if (aiStyle == 83)
		{
			if (type == 437)
			{
				if (localAI[3] == 0f && Main.netMode != 1)
				{
					localAI[3] = 1f;
					netUpdate = true;

```


---

## 🤖 Assistant · 2026-08-19T03:11:39.280Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Leech AI check details:

Vanilla healing order: 
1. First: num1327 = head (num1322 = |ai[0]|-1, type 396 head) — healed FIRST.
2. Then num1324 = core = head.ai[3] (type 398? Actually Main.npc[num1324] — ai[3] of head points to core; the core id).
3. Then num1325 = hand with ai[2]==0, num1326 = hand with ai[2]==1.

Our impl: `for (const tgt of [head, core, hand0, hand1])` — head, core, hand0, hand1. Matches vanilla order: head → core → hand0(ai2=0) → hand1(ai2=1). 

One difference: vanilla iterates NPCs to find hands by `ai[3] == num1324` (ai[3] of the hand equals core id? No wait — head's ai[3] = num1324; the loop looks for NPC whose ai[3] == num1324; the hands' ai[3] presumably also points to the core id). Our impl filters hands by `n.ai3 === head.ai3`. Matches.

Vanilla interp: Center = Lerp(projectile[ai[1]].Center, head.Center + (0,216), ai[2]/90). Our impl: e.x = lerp(x[0], head.cx, k) - e.w/2; x[0] was set at spawn = e.cx (approximation for the projectile 456 impact point; noted in comment). OK, documented approximation.

Vanilla also has head-gone → despawn. Ours does that. 

ai[0] can be negative? num1322 = |ai[0]|-1. Ours uses Math.floor(e.ai0) - 1 without abs. Where does the leech NPC get spawned? In this repo, moonlord spawns leech with ai0 = head.id + 1 (positive). In vanilla, Projectile AI for 456 spawns NPC 401 with ai[0] = -(npc id+1)? Let me check quickly: grep in Projectile.cs for "401". Actually the vanilla NPC leech spawn: `Main.npc[num].ai[0] = ...`. The abs suggests it can be negative. Since our repo spawns it positive, it's fine.

Now note one detail: in our impl, the interp start point x[0] = e.cx at spawn. Vanilla uses projectile[ai[1]].Center — the leech proj 456's center. Our approximation noted. Fine.

Also the vanilla head check: `!Main.npc[num1322].active || type != 396 → despawn`. Ours: `if (!head || head.dead) { e.dead = true; return; }` — matches (dead ≈ !active).

Now the tablet (aiStyle 83). Read vanilla 38793-38962.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:39.732Z · glm-x-preview-260804

```
水蛭治疗顺序匹配 (head→core→hand0→hand1)。接下来是教徒仪式 (38793-38962)。
```


---

## 🤖 Assistant · 2026-08-19T03:11:40.281Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38800,38962p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla cultist tablet and devotee AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:40.318Z

**📎 ToolResult**

```
					netUpdate = true;
					Point[] spawnPoints = null;
					if (!CultistRitual.CheckFloor(base.Center, out spawnPoints))
					{
						life = 0;
						HitEffect();
						active = false;
						return;
					}
					int num1346 = 0;
					int num1347 = 1;
					for (int num1348 = 0; num1348 < 4; num1348++)
					{
						int num1349 = 0;
						bool flag92 = num1348 == 1 || num1348 == 2;
						num1349 = ((!flag92) ? 379 : 438);
						int num1350 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), spawnPoints[num1348].X * 16 + 8, spawnPoints[num1348].Y * 16 - 48, num1349);
						if (flag92)
						{
							localAI[num1347++] = num1350 + 1;
							Main.npc[num1350].ai[3] = -(whoAmI + 1);
						}
						else
						{
							this.ai[num1346++] = num1350 + 1;
							Main.npc[num1350].ai[3] = -(whoAmI + 1);
						}
						Main.npc[num1350].netUpdate = true;
					}
				}
				if (localAI[0] == 1f && Main.netMode != 1)
				{
					localAI[0] = 2f;
					for (int num1351 = 0; num1351 < 2; num1351++)
					{
						Main.npc[(int)localAI[num1351 + 1] - 1].ai[1] = 1f;
						Main.npc[(int)localAI[num1351 + 1] - 1].netUpdate = true;
						Main.npc[(int)this.ai[num1351] - 1].ai[3] = 0f;
						Main.npc[(int)this.ai[num1351] - 1].TargetClosest();
						Main.npc[(int)this.ai[num1351] - 1].netUpdate = true;
					}
				}
				if (this.ai[0] != -1f && Main.netMode != 1)
				{
					bool flag93 = true;
					for (int num1352 = 0; num1352 < 2; num1352++)
					{
						if (Main.npc[(int)localAI[num1352 + 1] - 1].active && Main.npc[(int)localAI[num1352 + 1] - 1].type == 438)
						{
							flag93 = false;
						}
						if (Main.npc[(int)this.ai[num1352] - 1].active && Main.npc[(int)this.ai[num1352] - 1].type == 379)
						{
							flag93 = false;
						}
					}
					if (flag93)
					{
						this.ai[0] = -1f;
						this.ai[1] = 0f;
						this.ai[3] = 0f;
						int num1353 = (int)base.Center.X / 16 + 11 * (Main.rand.Next(2) == 0).ToDirectionInt();
						int num1354 = 0;
						for (int num1355 = -5; num1355 < 12; num1355++)
						{
							int num1356 = num1353;
							int num1357 = (int)base.Center.Y / 16 + num1355;
							if (WorldGen.SolidTile(num1356, num1357) && !Collision.SolidTiles(num1356 - 1, num1356 + 1, num1357 - 3, num1357 - 1))
							{
								num1354 = num1357;
								break;
							}
							if (num1355 == 11)
							{
								num1354 = num1357;
							}
						}
						int num1358 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), num1353 * 16 + 10, num1354 * 16 - 2, 439);
						Main.npc[num1358].direction = (Main.npc[num1358].spriteDirection = Math.Sign(base.Center.X - (float)(num1353 * 16) - 10f));
						this.ai[2] = num1358;
						netUpdate = true;
						CultistRitual.TabletDestroyed();
					}
				}
				if (this.ai[0] == -1f)
				{
					this.ai[3]++;
					if (this.ai[3] > 300f)
					{
						life = 0;
						HitEffect(0, 9999.0);
						active = false;
						if (Main.netMode != 1)
						{
							for (int num1359 = 0; num1359 < 6; num1359++)
							{
								float num1360 = 3f + Main.rand.NextFloat() * 6f;
								Vector2 vector230 = Vector2.UnitY.RotatedByRandom(6.2831854820251465);
								Vector2 center39 = base.Center;
								center39 += vector230 * 30f;
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center39.X, center39.Y, vector230.X * num1360, vector230.Y * num1360, 526, 0, 0f, Main.myPlayer, Main.npc[(int)this.ai[2]].Center.X, Main.npc[(int)this.ai[2]].Center.Y);
							}
							for (int num1361 = 0; num1361 < 20; num1361++)
							{
								if (Main.rand.Next(2) != 0)
								{
									float num1362 = 3f + Main.rand.NextFloat() * 6f;
									Vector2 vector231 = Vector2.UnitY.RotatedByRandom(6.2831854820251465);
									Vector2 center40 = base.Center;
									center40 += vector231 * 30f;
									Vector2 vector232 = base.Center + vector231 * (Main.rand.NextFloat() * 45f + 45f) + Vector2.UnitY * 20f;
									Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center40.X, center40.Y, vector231.X * num1362, -20f, 526, 0, 0f, Main.myPlayer, vector232.X, vector232.Y);
								}
							}
						}
					}
					else if (this.ai[3] % 10f == 1f && this.ai[3] > 120f && Main.netMode != 1)
					{
						float num1363 = 3f + Main.rand.NextFloat() * 6f;
						Vector2 vector233 = Vector2.UnitY.RotatedByRandom(6.2831854820251465);
						Vector2 center41 = base.Center;
						center41 += vector233 * 25f;
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center41.X, center41.Y, vector233.X * num1363, vector233.Y * num1363, 526, 0, 0f, Main.myPlayer, Main.npc[(int)this.ai[2]].Center.X, Main.npc[(int)this.ai[2]].Center.Y);
					}
				}
			}
			if (type == 438)
			{
				velocity.X *= 0.93f;
				if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
				{
					velocity.X = 0f;
				}
				int num1364 = (int)(0f - this.ai[3] - 1f);
				if (num1364 == -1)
				{
					life = 0;
					HitEffect();
					active = false;
					return;
				}
				int num1365 = Math.Sign(Main.npc[num1364].Center.X - base.Center.X);
				if (num1365 != direction)
				{
					velocity.X = 0f;
					direction = (spriteDirection = num1365);
					netUpdate = true;
				}
				if (justHit && Main.netMode != 1 && Main.npc[num1364].localAI[0] == 0f)
				{
					Main.npc[num1364].localAI[0] = 1f;
				}
				if ((this.ai[0] += 1f) >= 300f)
				{
					this.ai[0] = 0f;
					netUpdate = true;
				}
			}
			if (type == 437)
			{
				Lighting.AddLight(base.Center, 0.8f, 0.75f, 0.55f);
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:12:10.746Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Cultist tablet comparison:

Vanilla:
- `localAI[3] == 0` gate for init. Ours uses bInit — first-tick only. Equivalent-ish. Vanilla would re-init if localAI[3] got reset, but it never does. OK.
- Spawn positions: `spawnPoints[k].X * 16 + 8, spawnPoints[k].Y * 16 - 48`. NewNPC takes position (top-left). So child.y = point.y*16 - 48, i.e., 48 px above the floor tile top (NPC height for 438 is 48? Let me think: devotee 438 height = 48? Probably). Our impl: `child.y = pts[k].y * TILE - child.h;` — that puts the child's bottom at the floor tile top. Vanilla puts top at y*16-48, meaning bottom at y*16 if height==48. So identical for height 48. OK.
- Our impl devotes localAI[1..2] = devotee ids, ai[0..1] = archer ids. Vanilla: same (localAI[num1347++] with num1347=1,2 for devotees; ai[num1346++] with 0,1 for archers). Match.
- `localAI[0] == 1` → set to 2, loop: devotee ai[1] = 1; archer ai[3] = 0 + TargetClosest. Ours: sets dev.ai1 = 1, arc.ai3 = 0. TargetClosest not needed (no target field in our port — facing is computed). OK.
- Gone check: vanilla `flag93 = true; for both slots: if npc[localAI[k+1]-1].active && type==438 → flag93=false; if npc[ai[k]-1].active && type==379 → flag93=false`. Ours: same with `(!dev || dev.dead || dev.vanillaId !== 438) && (!arc || ...)`. Wait — vanilla uses OR: if EITHER is active → flag93 = false (i.e., not gone). Ours: `gone = [0,1].every(k => (!dev || dev.dead || dev.vanillaId !== 438) && (!arc || arc.dead || arc.vanillaId !== 379))`. every slot must have both dead → gone. Vanilla: gone = for all slots, NOT(dev active) AND NOT(arc active) = for all slots (dev inactive AND arc inactive). Same. OK.
- Cultist spawn: side column scan from -5..11; num1353 = center.X/16 + 11*dir. Ours: tx = floor(cx/16) + 11*side; ty scan j from -5..11 with `if (solidTileAt(tx,y) && !solidRect(tx-1,tx+1,y-3,y-1)) { ty = y; break; } if (j === 11) ty = y;`. Vanilla: same structure. But note vanilla `if (num1355 == 11) num1354 = num1357;` — this is INSIDE the loop after the break-check, executes even when not solid at j=11. Ours: `if (j === 11) ty = y;` same. OK.
- Cultist y: num1354 * 16 - 2. Ours: `cultist.y = ty * TILE - cultist.h;` — comment says "原版顶锚 y=tileY*16-2,本仓落底对齐". Vanilla top anchor = ty*16-2 → bottom at ty*16-2+h. Ours bottom at ty*16 → 2px+h higher... wait ours: bottom = ty*TILE, i.e., the cultist stands ON the tile top. Vanilla: top = ty*16-2 → bottom = ty*16-2+height. If height=48, bottom = ty*16+46 → 46px BELOW the tile top?? No wait: bottom = top + height = (ty*16 - 2) + 48 = ty*16 + 46. That's inside/below the floor tile. Hmm, but NewNPC typically snaps to ground via "npc position is top-left, then gravity settles". The vanilla spawn slightly overlaps the ground by 2px; then gravity/collision settles it. Ours places bottom exactly at the tile top. Minor difference (~2px + settle), acceptable. Not structural.
- Countdown: vanilla ai[3] > 300 → despawn + 6 projectiles 526 + 20×(1/2) projectiles 526. Ours spawns particles instead of 526 projectiles (documented: "526 仪式粒子有贴图但带 ai[0..1] 归巢弹道,降级为粒子"). Registered deviation in header comment. It's a projectile→particle downgrade. The header comment discloses it. Priority-wise this is a known/disclosed deviation. The task says "抓结构性偏差" — this is disclosed. I might mention in passing but it's not a CONFIRMED new finding. Actually wait — 526 projectiles are homing toward the cultist (ai[0], ai[1] = Main.npc[ai[2]].Center). These are visual ritual particles that fly to the cultist. Downgrade to particles is visual-only, no damage (dmg 0). Fine.

One notable thing: vanilla spawn loop uses `GetSpawnSourceForNPCFromNPCAI`, NewNPC(x,y,type) — no ai setting for the cultist. Ours sets bInit = true (skip own init?) Hmm — `cultist.bInit = true` — wait, for NPC 439 (Lunatic Cultist, aiStyle 84 handled elsewhere), setting bInit true might skip its first-tick init. Not part of this audit.

Vanilla tablet 437: `if (localAI[3] == 0f && netMode != 1)` gate, and importantly vanilla does NOT set dontTakeDamage here... wait our impl sets e.iframes = 2 each tick (invulnerable). In vanilla, SetDefaults for 437 has dontTakeDamage = true? The comment says (:14115 段). Plausible.

Also vanilla devotee (438): `num1364 = (int)(0 - ai[3] - 1)`; `if (num1364 == -1) → despawn`. Ours: `if (!owner || owner.dead) → despawn`. Vanilla doesn't check active of owner explicitly beyond indexing — if ai[3] = -1 → owner index -1 → despawn. If the tablet (owner) dies (inactive), Main.npc[owner].Center.X would read stale data — the devotee doesn't despawn in vanilla when the tablet dies?? Actually vanilla: devotee with dead tablet keeps flying with stale center. Hmm, but tablet death → ai[3] anchor stays; the devotee would keep targeting the dead slot position. Actually in vanilla when tablet is killed... the tablet is invulnerable (dontTakeDamage), and when the ritual completes (ai[0]=-1) it despawns after 300t; then devotees... but by then devotees are dead (all four dead → cultist spawned). If a devotee survives while tablet despawns at 300t — but devotees must ALL be dead for ai[0] to become -1. So the owner-dead case can't normally occur. Our despawn is a safe-side deviation. Fine.

Now phantom AI (39261-39519).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:11.208Z · glm-x-preview-260804

```
石碑的移植与原版逻辑高度一致。现在我来分析幻影 (39261-39519)。
```


---

## 🤖 Assistant · 2026-08-19T03:12:11.674Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '39261,39400p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla phantom AI part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:11.733Z

**📎 ToolResult**

```
		else if (aiStyle == 86)
		{
			if (alpha > 0)
			{
				alpha -= 30;
				if (alpha < 0)
				{
					alpha = 0;
				}
			}
			noGravity = true;
			noTileCollide = true;
			knockBackResist = 0f;
			for (int num1381 = 0; num1381 < Main.maxNPCs; num1381++)
			{
				if (num1381 == whoAmI || !Main.npc[num1381].active || Main.npc[num1381].type != type)
				{
					continue;
				}
				Vector2 vector241 = Main.npc[num1381].Center - base.Center;
				if (!(vector241.Length() < 50f))
				{
					continue;
				}
				vector241.Normalize();
				if (vector241.X == 0f && vector241.Y == 0f)
				{
					if (num1381 > whoAmI)
					{
						vector241.X = 1f;
					}
					else
					{
						vector241.X = -1f;
					}
				}
				vector241 *= 0.4f;
				velocity -= vector241;
				NPC nPC3 = Main.npc[num1381];
				nPC3.velocity += vector241;
			}
			if (type == 472)
			{
				float num1382 = 120f;
				if (localAI[0] < num1382)
				{
					if (localAI[0] == 0f)
					{
						SoundEngine.PlaySound(SoundID.Item8, base.Center);
						TargetClosest();
						if (direction > 0)
						{
							velocity.X += 2f;
						}
						else
						{
							velocity.X -= 2f;
						}
						position += netOffset;
						for (int num1383 = 0; num1383 < 20; num1383++)
						{
							Vector2 center45 = base.Center;
							center45.Y -= 18f;
							Vector2 vector242 = new Vector2(Main.rand.Next(-100, 101), Main.rand.Next(-100, 101));
							vector242.Normalize();
							vector242 *= (float)Main.rand.Next(0, 100) * 0.1f;
							center45 += vector242;
							vector242.Normalize();
							vector242 *= (float)Main.rand.Next(50, 90) * 0.2f;
							int num1384 = Dust.NewDust(center45, 1, 1, 27);
							Main.dust[num1384].velocity = -vector242 * 0.3f;
							Main.dust[num1384].alpha = 100;
							if (Main.rand.Next(2) == 0)
							{
								Main.dust[num1384].noGravity = true;
								Dust dust = Main.dust[num1384];
								dust.scale += 0.3f;
							}
						}
						position -= netOffset;
					}
					localAI[0] += 1f;
					float num1385 = 1f - localAI[0] / num1382;
					float num1386 = num1385 * 20f;
					for (int num1387 = 0; (float)num1387 < num1386; num1387++)
					{
						if (Main.rand.Next(5) == 0)
						{
							position += netOffset;
							int num1388 = Dust.NewDust(position, width, height, 27);
							Main.dust[num1388].alpha = 100;
							Dust dust = Main.dust[num1388];
							dust.velocity *= 0.3f;
							dust = Main.dust[num1388];
							dust.velocity += velocity * 0.75f;
							Main.dust[num1388].noGravity = true;
							position -= netOffset;
						}
					}
				}
			}
			if (type == 521)
			{
				float num1389 = 120f;
				if (localAI[0] < num1389)
				{
					if (localAI[0] == 0f)
					{
						SoundEngine.PlaySound(SoundID.Item8, base.Center);
						TargetClosest();
						if (direction > 0)
						{
							velocity.X += 2f;
						}
						else
						{
							velocity.X -= 2f;
						}
					}
					localAI[0] += 1f;
					int num1390 = 10;
					for (int num1391 = 0; num1391 < 2; num1391++)
					{
						position += netOffset;
						int num1392 = Dust.NewDust(position - new Vector2(num1390), width + num1390 * 2, height + num1390 * 2, 228, 0f, 0f, 100, default(Color), 2f);
						Main.dust[num1392].noGravity = true;
						Main.dust[num1392].noLight = true;
						position -= netOffset;
					}
				}
			}
			if (this.ai[0] == 0f)
			{
				TargetClosest();
				this.ai[0] = 1f;
				this.ai[1] = direction;
			}
			else if (this.ai[0] == 1f)
			{
				TargetClosest();

```


---

## 🤖 Assistant · 2026-08-19T03:12:16.271Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note: our impl uses x[3] (localAI[3]) for the 120t reveal counter, vanilla uses localAI[0]. That's fine since localAI[0] is unused elsewhere in our port for phantom.

Continue reading 39400-39519.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:16.906Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '39400,39519p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla phantom AI part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:16.968Z

**📎 ToolResult**

```
				TargetClosest();
				float num1393 = 0.3f;
				float num1394 = 7f;
				float num1395 = 4f;
				float num1396 = 660f;
				float num1397 = 4f;
				if (type == 521)
				{
					num1393 = 0.7f;
					num1394 = 14f;
					num1396 = 500f;
					num1395 = 6f;
					num1397 = 3f;
				}
				velocity.X += this.ai[1] * num1393;
				if (velocity.X > num1394)
				{
					velocity.X = num1394;
				}
				if (velocity.X < 0f - num1394)
				{
					velocity.X = 0f - num1394;
				}
				float num1398 = Main.player[target].Center.Y - base.Center.Y;
				if (Math.Abs(num1398) > num1395)
				{
					num1397 = 15f;
				}
				if (num1398 > num1395)
				{
					num1398 = num1395;
				}
				else if (num1398 < 0f - num1395)
				{
					num1398 = 0f - num1395;
				}
				velocity.Y = (velocity.Y * (num1397 - 1f) + num1398) / num1397;
				if ((this.ai[1] > 0f && Main.player[target].Center.X - base.Center.X < 0f - num1396) || (this.ai[1] < 0f && Main.player[target].Center.X - base.Center.X > num1396))
				{
					this.ai[0] = 2f;
					this.ai[1] = 0f;
					if (base.Center.Y + 20f > Main.player[target].Center.Y)
					{
						this.ai[1] = -1f;
					}
					else
					{
						this.ai[1] = 1f;
					}
				}
			}
			else if (this.ai[0] == 2f)
			{
				float num1399 = 0.4f;
				float num1400 = 0.95f;
				float num1401 = 5f;
				if (type == 521)
				{
					num1399 = 0.3f;
					num1401 = 7f;
					num1400 = 0.9f;
				}
				velocity.Y += this.ai[1] * num1399;
				if (velocity.Length() > num1401)
				{
					velocity *= num1400;
				}
				if (velocity.X > -1f && velocity.X < 1f)
				{
					TargetClosest();
					this.ai[0] = 3f;
					this.ai[1] = direction;
				}
			}
			else if (this.ai[0] == 3f)
			{
				float num1402 = 0.4f;
				float num1403 = 0.2f;
				float num1404 = 5f;
				float num1405 = 0.95f;
				if (type == 521)
				{
					num1402 = 0.6f;
					num1403 = 0.3f;
					num1404 = 7f;
					num1405 = 0.9f;
				}
				velocity.X += this.ai[1] * num1402;
				if (base.Center.Y > Main.player[target].Center.Y)
				{
					velocity.Y -= num1403;
				}
				else
				{
					velocity.Y += num1403;
				}
				if (velocity.Length() > num1404)
				{
					velocity *= num1405;
				}
				if (velocity.Y > -1f && velocity.Y < 1f)
				{
					TargetClosest();
					this.ai[0] = 0f;
					this.ai[1] = direction;
				}
			}
			if (type == 521)
			{
				int num1406 = 10;
				position += netOffset;
				for (int num1407 = 0; num1407 < 1; num1407++)
				{
					int num1408 = Dust.NewDust(position - new Vector2(num1406), width + num1406 * 2, height + num1406 * 2, 228, 0f, 0f, 100, default(Color), 2f);
					Main.dust[num1408].noGravity = true;
					Main.dust[num1408].noLight = true;
				}
				position -= netOffset;
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:12:28.338Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Phantom AI check:

State 1 (horizontal sweep):
- Vanilla: velocity.X += ai[1]*acc; clamp ±max. Ours: `e.vx = clamp(e.vx + e.ai1 * acc, -max, max)`. OK.
- Y servo: num1398 = player.cy - e.cy; if |dy| > clamp → num1397 = 15; clamp dy to ±num1395; velocity.Y = (vy*(num1397-1) + dy)/num1397.
- Ours: `let dy = player ? player.cy - e.cy : 0; let step = yStep; if (Math.abs(dy) > yClamp) { step = 15; dy = clamp(dy, -yClamp, yClamp); } e.vy = (e.vy * (step - 1) + dy) / step;`. 
  - yStep for 472 = 4, yClamp = 4; 521: yStep = 3, yClamp = 6. Vanilla: 472 num1395 (clamp) = 4, num1397 (step) = 4; 521: num1395 = 6, num1397 = 3. Matches.
- Turn condition: (ai1>0 && px-e.x < -660) || (ai1<0 && px-e.x > 660) → state 2, ai[1] = (cy+20 > player.cy) ? -1 : 1. Ours matches. Range 660/500. OK.

State 2: acc 0.4/0.3 (472/521) — ours: `const acc = big ? 0.3 : 0.4`. cap 5/7 — ours `cap = big ? 7 : 5`. damp 0.95/0.9 — ours `damp = big ? 0.9 : 0.95`. vy += ai1*acc; if len > cap → *= damp. If vx in (-1,1) → state 3 with ai1 = direction. Ours matches.

State 3: acc 0.4/0.6 (472/521) — ours `acc = big ? 0.6 : 0.4`. vyAcc 0.2/0.3 — ours `vyAcc = big ? 0.3 : 0.2`. cap 5/7, damp 0.95/0.9. vx += ai1*acc; vy ±vyAcc; len>cap → damp; vy in (-1,1) → state 0, ai1 = direction. Ours matches.

State 0 → 1 immediate with ai1 = direction. Ours matches.

Reveal: 472 initial burst + follow dusts; 521 two dusts/tick. Ours approximates. OK.

One subtle thing: state 0 in ours calls `e.seekDirX(player)` then `e.ai0 = 1; e.ai1 = e.facing`. Vanilla: TargetClosest(); ai[0]=1; ai[1]=direction. OK.

But NOTE: vanilla calls TargetClosest() in states 0,1,2,3 — fine.

The phantom looks clean. Now bigMimicAI (39520-39875).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:28.747Z · glm-x-preview-260804

```
Phantom 已符合。现在处理 big mimic (39520-39875)。
```


---

## 🤖 Assistant · 2026-08-19T03:12:29.151Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '39520,39700p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla big mimic AI part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:29.207Z

**📎 ToolResult**

```
		else if (aiStyle == 87)
		{
			knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.2f);
			dontTakeDamage = false;
			noTileCollide = false;
			noGravity = false;
			reflectsProjectiles = false;
			if (this.ai[0] != 7f && Main.player[target].dead)
			{
				TargetClosest();
				if (Main.player[target].dead)
				{
					this.ai[0] = 7f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
					netUpdate = true;
				}
			}
			if (this.ai[0] == 0f)
			{
				TargetClosest();
				Vector2 vector243 = Main.player[target].Center - base.Center;
				if (Main.netMode != 1 && (velocity.X != 0f || velocity.Y > 100f || justHit || vector243.Length() < 80f))
				{
					this.ai[0] = 1f;
					this.ai[1] = 0f;
					netUpdate = true;
				}
			}
			else if (this.ai[0] == 1f)
			{
				this.ai[1] += 1f;
				if (Main.netMode != 1 && this.ai[1] > 36f)
				{
					this.ai[0] = 2f;
					this.ai[1] = 0f;
					netUpdate = true;
				}
			}
			else if (this.ai[0] == 2f)
			{
				Vector2 vector244 = Main.player[target].Center - base.Center;
				if (Main.netMode != 1 && vector244.Length() > 600f)
				{
					this.ai[0] = 5f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
					netUpdate = true;
				}
				if (velocity.Y == 0f)
				{
					TargetClosest();
					velocity.X *= 0.85f;
					this.ai[1] += 1f;
					float num1409 = 15f + 30f * ((float)life / (float)lifeMax);
					float num1410 = 3f + 4f * (1f - (float)life / (float)lifeMax);
					float num1411 = 4f;
					if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
					{
						num1411 += 2f;
					}
					if (Main.netMode != 1 && this.ai[1] > num1409)
					{
						this.ai[3] += 1f;
						if (this.ai[3] >= 3f)
						{
							this.ai[3] = 0f;
							num1411 *= 2f;
							num1410 /= 2f;
						}
						this.ai[1] = 0f;
						velocity.Y -= num1411;
						velocity.X = num1410 * (float)direction;
						netUpdate = true;
					}
				}
				else
				{
					knockBackResist = 0f;
					velocity.X *= 0.99f;
					if (direction < 0 && velocity.X > -1f)
					{
						velocity.X = -1f;
					}
					if (direction > 0 && velocity.X < 1f)
					{
						velocity.X = 1f;
					}
				}
				this.ai[2] += 1f;
				if ((double)this.ai[2] > 210.0 && velocity.Y == 0f && Main.netMode != 1)
				{
					switch (Main.rand.Next(3))
					{
					case 0:
						this.ai[0] = 3f;
						break;
					case 1:
						this.ai[0] = 4f;
						noTileCollide = true;
						velocity.Y = -8f;
						break;
					case 2:
						this.ai[0] = 6f;
						break;
					default:
						this.ai[0] = 2f;
						break;
					}
					if (Main.tenthAnniversaryWorld && type == 476 && this.ai[0] == 3f && Main.rand.Next(2) == 0)
					{
						this.ai[0] = 8f;
					}
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
					netUpdate = true;
				}
			}
			else if (this.ai[0] == 3f)
			{
				velocity.X *= 0.85f;
				dontTakeDamage = true;
				this.ai[1] += 1f;
				if (Main.netMode != 1 && this.ai[1] >= 180f)
				{
					this.ai[0] = 2f;
					this.ai[1] = 0f;
					netUpdate = true;
				}
				if (Main.expertMode)
				{
					ReflectProjectiles(base.Hitbox);
					reflectsProjectiles = true;
				}
			}
			else if (this.ai[0] == 4f)
			{
				noTileCollide = true;
				noGravity = true;
				knockBackResist = 0f;
				if (velocity.X < 0f)
				{
					direction = -1;
				}
				else
				{
					direction = 1;
				}
				spriteDirection = direction;
				TargetClosest();
				Vector2 center46 = Main.player[target].Center;
				center46.Y -= 350f;
				Vector2 vector245 = center46 - base.Center;
				if (this.ai[2] == 1f)
				{
					this.ai[1] += 1f;
					vector245 = Main.player[target].Center - base.Center;
					vector245.Normalize();
					vector245 *= 8f;
					velocity = (velocity * 4f + vector245) / 5f;
					if (Main.netMode != 1 && this.ai[1] > 6f)
					{
						this.ai[1] = 0f;
						this.ai[0] = 4.1f;
						this.ai[2] = 0f;
						velocity = vector245;
						netUpdate = true;
					}
				}
				else if (Math.Abs(base.Center.X - Main.player[target].Center.X) < 40f && base.Center.Y < Main.player[target].Center.Y - 300f)
				{
					if (Main.netMode != 1)
					{
						this.ai[1] = 0f;
						this.ai[2] = 1f;
						netUpdate = true;
					}
				}

```


---

## 🤖 Assistant · 2026-08-19T03:12:33.934Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '39700,39875p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla big mimic AI part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:33.992Z

**📎 ToolResult**

```
				}
				else
				{
					vector245.Normalize();
					vector245 *= 12f;
					velocity = (velocity * 5f + vector245) / 6f;
				}
			}
			else if (this.ai[0] == 4.1f)
			{
				knockBackResist = 0f;
				if (this.ai[2] == 0f && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1) && !Collision.SolidCollision(position, width, height))
				{
					this.ai[2] = 1f;
				}
				if (position.Y + (float)height >= Main.player[target].position.Y || velocity.Y <= 0f)
				{
					this.ai[1] += 1f;
					if (Main.netMode != 1 && this.ai[1] > 10f)
					{
						this.ai[0] = 2f;
						this.ai[1] = 0f;
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
						if (Collision.SolidCollision(position, width, height))
						{
							this.ai[0] = 5f;
						}
					}
				}
				else if (this.ai[2] == 0f)
				{
					noTileCollide = true;
					noGravity = true;
					knockBackResist = 0f;
				}
				velocity.Y += 0.2f;
				if (velocity.Y > 16f)
				{
					velocity.Y = 16f;
				}
			}
			else if (this.ai[0] == 5f)
			{
				if (velocity.X > 0f)
				{
					direction = 1;
				}
				else
				{
					direction = -1;
				}
				spriteDirection = direction;
				noTileCollide = true;
				noGravity = true;
				knockBackResist = 0f;
				Vector2 vector246 = Main.player[target].Center - base.Center;
				vector246.Y -= 4f;
				if (Main.netMode != 1 && vector246.Length() < 200f && !Collision.SolidCollision(position, width, height))
				{
					this.ai[0] = 2f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
					netUpdate = true;
				}
				if (vector246.Length() > 10f)
				{
					vector246.Normalize();
					vector246 *= 10f;
				}
				velocity = (velocity * 4f + vector246) / 5f;
			}
			else if (this.ai[0] == 6f)
			{
				knockBackResist = 0f;
				if (velocity.Y == 0f)
				{
					TargetClosest();
					velocity.X *= 0.8f;
					this.ai[1] += 1f;
					if (this.ai[1] > 5f)
					{
						this.ai[1] = 0f;
						velocity.Y -= 4f;
						if (Main.player[target].position.Y + (float)Main.player[target].height < base.Center.Y)
						{
							velocity.Y -= 1.25f;
						}
						if (Main.player[target].position.Y + (float)Main.player[target].height < base.Center.Y - 40f)
						{
							velocity.Y -= 1.5f;
						}
						if (Main.player[target].position.Y + (float)Main.player[target].height < base.Center.Y - 80f)
						{
							velocity.Y -= 1.75f;
						}
						if (Main.player[target].position.Y + (float)Main.player[target].height < base.Center.Y - 120f)
						{
							velocity.Y -= 2f;
						}
						if (Main.player[target].position.Y + (float)Main.player[target].height < base.Center.Y - 160f)
						{
							velocity.Y -= 2.25f;
						}
						if (Main.player[target].position.Y + (float)Main.player[target].height < base.Center.Y - 200f)
						{
							velocity.Y -= 2.5f;
						}
						if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
						{
							velocity.Y -= 2f;
						}
						velocity.X = 12 * direction;
						this.ai[2] += 1f;
						netUpdate = true;
					}
				}
				else
				{
					velocity.X *= 0.98f;
					if (direction < 0 && velocity.X > -8f)
					{
						velocity.X = -8f;
					}
					if (direction > 0 && velocity.X < 8f)
					{
						velocity.X = 8f;
					}
				}
				if (Main.netMode != 1 && this.ai[2] >= 3f && velocity.Y == 0f)
				{
					this.ai[0] = 2f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
					netUpdate = true;
				}
			}
			else if (this.ai[0] == 7f)
			{
				damage = 0;
				life = lifeMax;
				defense = 9999;
				noTileCollide = true;
				alpha += 7;
				if (alpha > 255)
				{
					alpha = 255;
				}
				velocity.X *= 0.98f;
			}
			else
			{
				if (this.ai[0] != 8f)
				{
					return;
				}
				velocity.X *= 0.85f;
				this.ai[1] += 1f;
				if (Main.netMode != 1)
				{
					if (!Main.tenthAnniversaryWorld || this.ai[1] >= 180f)
					{
						this.ai[0] = 2f;
						this.ai[1] = 0f;
						netUpdate = true;
					}
					else if (this.ai[1] % 20f == 0f)
					{
						AI_87_BigMimic_FireStuffCannonBurst();
					}
				}
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:13:31.496Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Big Mimic comparison:

State 0: vanilla wake condition: velocity.X != 0 || velocity.Y > 100 || justHit || dist < 80. Ours: `e.vx !== 0 || e.vy > 100 || e.justHit || near`. Matches.

State 2:
- >600 → state 5: ours matches.
- grounded branch: vanilla `velocity.Y == 0f` gate. Ours uses `e.onGround && e.vy === 0`. Hmm — vanilla just checks velocity.Y == 0 (not onGround). A mimic falling could have vy==0 momentarily? vy==0 mid-air is rare. onGround&&vy==0 is a reasonable equivalent since gravity is applied... but in our impl `grounded()` applies gravity AFTER the branch (end of the state). So vy==0 in our engine implies resting. OK.
- wait num1409 = 15 + 30 * life/lifeMax — NOTE: vanilla uses `life/lifeMax` (higher = more HP). Ours: `hpFrac = e.hp / e.maxHp; wait = 15 + 30 * hpFrac`. Matches.
- num1410 = 3 + 4*(1 - life/lifeMax). Ours: `jumpV = 3 + 4 * (1 - hpFrac)`. Matches.
- num1411 = 4 (+2 if no LOS). Ours: `jumpPow = los ? 4 : 6`. Matches.
- ai[3]>=3 → num1411 *= 2, num1410 /= 2. Ours: `jumpPow *= 2; jumpV /= 2`. Matches.
- velocity.Y -= num1411; velocity.X = num1410 * direction. Ours: `e.vy -= jumpPow; e.vx = jumpV * e.facing`. Matches.
- air branch: vx *= 0.99, min ±1 by direction. Ours matches.
- 210 gate: ai[2] > 210 && vy == 0: vanilla switch rand(3): 0→3, 1→4 (noTileCollide=true, vy=-8), 2→6. Ours: `pick === 0 ? 3 : pick === 1 ? 4 : 6; if (pick === 1) e.vy = -8`. Matches (noTileCollide in ours handled by state 4 setting noGravity/fly; state 4 uses fly() so tile collision is skipped — matches noTileCollide=true).
- 10th anniversary: 8 unreachable, ours comments it. OK.

State 3: vx *= 0.85, dontTakeDamage, ai1 >= 180 → 2. Ours matches (iframes=2 ≈ dontTakeDamage; expert reflect unreachable).

State 4: 
- vanilla: noTileCollide=true, noGravity=true. TargetClosest. Target = player center Y-350. 
- ai2==1 branch: ai1++, vector245 = player.Center - center normalized *8; velocity = (v*4 + vec)/5; ai1 > 6 → state 4.1, ai1=0, ai2=0, velocity = vector245.
- Ours: matches (tx = dx/d*8 etc.).
- else if |cx - px| < 40 && cy < pcy - 300 → ai1=0, ai2=1. Ours matches.
- else: normalized *12, velocity = (v*5+vec)/6. Ours matches.

State 4.1:
- vanilla: ai2==0 && CanHit && !SolidCollision → ai2=1.
- if (y + height >= player.y || vy <= 0): ai1++; ai1 > 10 → state 2 (or 5 if solid collision).
- else if ai2 == 0: noTileCollide = true; noGravity = true.
- gravity: vy += 0.2, cap 16.

Ours:
```
if (e.ai2 === 0 && p && losClear && !inSolidBody) e.ai2 = 1;
e.vy = Math.min(e.vy + 0.2, 16);
if (!p || e.y + e.h >= p.y || e.vy <= 0) {
  ai1++; if > 10 → ai0 = inSolidBody ? 5 : 2 ...
  moveAndCollide
} else if (e.ai2 === 0) {
  e.noGravity = true; fly(e);
}
```
Vanilla order: the state-4.1 code sets gravity AFTER the branch (velocity.Y += 0.2 at the end), and importantly in the first branch (past player / vy<=0) it does NOT set noGravity — but noGravity persists from state 4? No wait — at the top of aiStyle 87, `noGravity = false` is reset every tick (line: noGravity = false at the start). So in state 4.1, when passing player or vy<=0, noGravity remains false → gravity applies; when in the dive segment (ai2==0, above player), noGravity=true and noTileCollide=true → flies through walls downward. Ours matches this via noGravity flag + fly/moveAndCollide.

BUT: there's a subtlety — in our impl, the branch `if (!p || e.y + e.h >= p.y || e.vy <= 0)` uses moveAndCollide(e.vx, e.vy) — and vy was already incremented by 0.2 BEFORE (ours applies gravity first). Vanilla applies gravity at end; net effect equivalent.

Note vanilla when vy<=0 → gravity continues... whatever, equivalent.

Also ours: in the "not yet aligned" branch (else if ai2===0) → fly. But what if ai2 === 1 and not past player and vy > 0? Then neither branch runs the movement! Ours: `if (...) { ... } else if (e.ai2 === 0) { fly(e) }` — if ai2==1 and above player and vy>0, no movement happens this tick. Vanilla: velocity integrates regardless (NPC movement is handled by the shared movement code outside the AI switch — in vanilla, position += velocity always happens for non-noTileCollide... wait no. In vanilla, the AI sets velocity, and the actual position integration happens in the main NPC update after AI (either via collision or direct). Actually in vanilla NPC.UpdateNPC, after AI() the movement integration always occurs (Collision or direct when noTileCollide). So vanilla: in that case, the NPC moves with tile collision (since noGravity=false, noTileCollide=false in that configuration — ai2==1 means aligned; noTileCollide not set in this branch). So vanilla WOULD move with collision. Ours: NO movement at all (neither moveAndCollide nor fly). Missing movement for one tick. Hmm — wait let me re-read our code:

```js
} else if (e.ai0 === 4.1) {
    if (e.ai2 === 0 && p && losClear(...) && !inSolidBody(game, e)) e.ai2 = 1;
    e.vy = Math.min(e.vy + 0.2, 16);
    if (!p || e.y + e.h >= p.y || e.vy <= 0) {
      e.ai1 += 1;
      if (e.ai1 > 10) { ... }
      moveAndCollide(e, game.world, e.vx, e.vy);
    } else if (e.ai2 === 0) {
      e.noGravity = true;
      fly(e);
    }
  }
```

Case: ai2 == 1 (aligned, LOS), still above player, vy > 0 → no movement call. In vanilla this state has noGravity=false (reset at top), noTileCollide=false... wait actually — noTileCollide was set true when entering state 4 and also at 4.1's third branch. At the top of the AI: `noTileCollide = false` reset each tick! Look at vanilla start of aiStyle 87: `noTileCollide = false; noGravity = false;` — every tick resets. So in state 4.1, ai2==1, above player, vy>0: noGravity=false, noTileCollide=false → gravity applies... and vy>0 means falling with collision. Vanilla moves with collision. Ours: frozen for that tick (velocity accumulates vy += 0.2 but position doesn't change). Hmm, but wait — can this case even occur? ai2 becomes 1 when CanHit && !SolidCollision while above player with vy>0 falling. The transition from state 4: velocity = toward player *8 — vy positive if player below. So typically enters 4.1 with vy > 0 (player below → dy > 0 → vy = +8). So immediately: y+h >= p.y? No (still above). vy <= 0? No (vy=+8 > 0). So first tick in 4.1: ai2 goes 0→1 if CanHit&&!solid. Then: first branch false (not past player, vy>0), else-if ai2===0 false (ai2 just became 1!). → NO MOVEMENT. And subsequent ticks: vy keeps +0.2, never past player, never vy<=0 → mimic hovers frozen in air above player forever?? 

Hold on — that would be a visible bug (mimic freezes mid-air during dive when it has LOS). Let me double check vanilla semantics for the ai2==1 case: vanilla 4.1 with ai2==1, above player, vy>0: first branch (position.Y + height >= player.position.Y || velocity.Y <= 0f)? Not yet. else if (ai[2] == 0f)? ai2==1 → no. So vanilla AI sets nothing → but movement still happens via the standard update: velocity integrates (noGravity false → but gravity is applied by the shared code? Actually for aiStyle 87, gravity is applied inside AI? No — gravity for NPCs is applied in UpdateNPC shared section when !noGravity. And 4.1 applies vy += 0.2 itself at the end. So vanilla: vy += 0.2, position += velocity with collision. The mimic FALLS with tile collision toward the player, since ai2==1 means "aligned, use normal collision".

So the ai2==1 case means "fall through normal collision" — our impl never moves in that case. This is a real deviation: during the aligned dive (ai2=1, LOS, above player, vy>0), our mimic is frozen in place until vy... vy only increases (0.2/tick), never <= 0, and position never changes so y+h >= p.y never becomes true → stuck forever until... nothing. Hmm wait — actually would this freeze happen? Let me re-check: `if (e.ai2 === 0 && p && losClear && !inSolidBody) e.ai2 = 1;` — this is at the top, before the branches. So entering 4.1 from state 4 (vy>0 toward player): ai2=0. If LOS && !inSolid → ai2=1 immediately → then the else-if (ai2===0) fails → frozen. If no LOS or embedded → ai2 stays 0 → else-if runs → fly (through walls). So with LOS (typical case), mimic freezes mid-dive!

Hmm wait, but actually — is that right? Let me re-read the vanilla one more time to make sure ai2==1 case really just falls with collision (i.e., there's movement). Yes: in vanilla, NPC velocity always integrates after AI (shared movement code at ~:91400). noTileCollide=false in this branch → collision movement. So vanilla mimic falls at up to 16 px/t with collision. Ours: velocity accumulates but never integrates position. CONFIRMED structural bug (state freeze).

Actually wait — maybe I should double check whether Enemy.ts applies gravity+collision outside the AI dispatch for mimics (like the "shared displacement block" mentioned in comments: "NPC.cs UpdateNPC :91400 段共享位移的穿墙分支"). The header comments mention shared gravity blocks for other AIs (devotee calls moveAndCollide itself). For bigMimicAI, the function handles all movement itself (calls grounded()/fly()/moveAndCollide per state). In state 4.1 ai2==1-above-player case, no movement call → frozen. Unless Enemy.update does something extra when noGravity is false. Let me check Enemy.ts's update loop for the AI dispatch to see if movement is applied generically after AI. Let me grep Enemy.ts for bigMimicAI.

Also state 5: vanilla `vector246 = player.Center - center; vector246.Y -= 4` — wait: `Vector2 vector246 = Main.player[target].Center - base.Center; vector246.Y -= 4f;` — dy = (pcy - cy) - 4. Ours: `dy = (p ? p.cy : e.cy) - 4 - e.cy` = pcy - 4 - cy. Matches.
- near 200 && !solid → state 2. Ours matches. speed 10, (v*4+vec)/5. Ours matches.

State 6: grounded: vx *= 0.8, ai1 > 5 → vy -= 4, minus extra based on player height, vx = 12*direction, ai2++. Ours matches all thresholds (1.25/1.5/1.75/2/2.25/2.5 at 0/40/80/120/160/200, -2 no LOS). Matches.
- air: vx *= 0.98, min ±8. Ours matches.
- ai2 >= 3 && vy==0 → state 2. Ours: `e.ai2 >= 3 && e.onGround && e.vy === 0`. Matches.

State 7: damage=0, life=lifeMax, defense=9999, alpha += 7, vx *= 0.98. Ours: def.damage = 0, hp = maxHp, spawnAlpha += 7 (hmm — alpha in vanilla goes UP to 255 = invisible; spawnAlpha in our repo probably starts at 255 and decreases for spawn fade-in... need to check semantics. `e.spawnAlpha = Math.min(255, e.spawnAlpha + 7)` — if spawnAlpha is "alpha" then increasing = fading out, matching vanilla. OK.)
- defense = 9999: ours doesn't set defense, but sets def.damage=0. Mimic is damage-0 but still takes damage in state 7 in ours (hp restored each tick anyway = full heal). Vanilla def 9999 + life=max → effectively invulnerable. Ours: hp = maxHp each tick → also effectively invulnerable. OK.

State 4 in ours: `if (p) e.facing = e.vx < 0 ? -1 : 1;` — vanilla: direction = velocity.X < 0 ? -1 : 1 unconditionally. Minor.

Now — the wake condition in state 0: vanilla TargetClosest each tick. OK.

Let me now verify the claim about Enemy.ts not moving NPCs generically. Check how Enemy dispatches these AI functions.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:31.930Z · glm-x-preview-260804

```
Big mimic state 4.1 有个可疑的停滞路径。让我先确认 Enemy.ts 的移动分发方式，再核对 mothron 段。
```


---

## 🤖 Assistant · 2026-08-19T03:13:33.198Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"bigMimicAI\\|moonLordFreeEyeAI\\|mothronAI\\|graniteElementalAI\\|starCellAI\\|flowInvaderAI\\|nebulaFloaterAI\\|solarSlimeAI\\|crawltipedeAI\\|phantomAI\\|smallStarCellAI\\|babyMothronAI\\|mothronEggAI\\|moonLeechAI\\|cultistTabletAI\\|lunaticDevoteeAI\\|cultistArcherStandbyAI\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -40",
 "description": "Find AI dispatch sites in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:33.255Z

**📎 ToolResult**

```
59:  moonLordFreeEyeAI, moonLeechAI, cultistTabletAI, lunaticDevoteeAI,
60:  cultistArcherStandbyAI, cultistArcherWake, phantomAI, bigMimicAI,
61:  mothronAI, mothronEggAI, babyMothronAI, graniteElementalAI,
62:  starCellAI, smallStarCellAI, flowInvaderAI, nebulaFloaterAI, solarSlimeAI,
63:  crawltipedeAI, lunarLocalAI,
150: * "EoW 打两下自动战败"根因。★413/414（爬尾虫身/尾）同款补入：crawltipedeAI 的
1185:            cultistArcherStandbyAI(this, game);
1205:          if (this.vanillaId === 412) crawltipedeAI(this, game, p);
1237:        case 81: moonLordFreeEyeAI(this, game, p); break;                // AI_081 月总游离眼 400（cs:38224 十槽攻击表+死光）
1238:        case 82: moonLeechAI(this, game, p); break;                       // AI_082 月总水蛭块 401（cs:38668 90t 插值吸血回灌）
1240:          if (this.vanillaId === 437) cultistTabletAI(this, game, p);
1241:          else lunaticDevoteeAI(this, game, p);
1243:        case 86: phantomAI(this, game, p); break;                          // AI_086 暗焰幻影 472/远古幻影 521（cs:39261 穿墙横掠循环）
1244:        case 87: bigMimicAI(this, game, p); break;                         // AI_087 珍稀四宝箱怪 473-476（cs:39520 跳扑+蓄能/俯冲/三连扑）
1245:        case 88: mothronAI(this, game, p); break;                          // AI_088 飞蛾魔 477（cs:39876 日食限定轮换+产卵）
1246:        case 89: mothronEggAI(this, game, p); break;                       // AI_089 蛾卵 478（cs:40407 900t→Transform 479）
1247:        case 90: babyMothronAI(this, game, p); break;                      // AI_090 幼蛾 479（cs:40450 日食贴脸冲撞）
1248:        case 91: graniteElementalAI(this, game, p); break;                 // AI_091 花岗岩元素 483（cs:40686 五态寻路）
1290:        case 85: starCellAI(this, game, p); break;                    // AI_085 星细胞 405/星云头蟹 421（六态寻路+吸附）
1291:        case 95: smallStarCellAI(this, game, p); break;               // AI_095 小星细胞 406（300t 长大 Transform 405）
1292:        case 96: flowInvaderAI(this, game, p); break;                 // AI_096 水流入侵者 407(/408)（悬顶伺服+甩 539）
1293:        case 97: nebulaFloaterAI(this, game, p); break;               // AI_097 星云悬浮脑 420（瞬移+环绕球 574→弹 576）
1294:        case 99: solarSlimeAI(this, game, p); break;                  // AI_099 日耀黏液 519（坠落→落地 5t 自爆）

```


---

## 🤖 Assistant · 2026-08-19T03:13:38.635Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1150,1300p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read Enemy.ts AI dispatch context for shared movement"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:38.683Z

**📎 ToolResult**

```
    this.animT++;
    this.walkCycleT += Math.abs(this.vx); // 原版 zombie/fighter 行走帧按 |vx| 累加（L77072/L70216）
    // 原版 case46 族 vx==0 清 frameCounter（NPC.cs:77571-77577）——站定即清相位，
    // 起步必从帧 0 起稳走（2026-08-18 审查：曾保留相位起步首帧非 0）
    if (Math.abs(this.vx) <= 0.05) this.walkCycleT = 0;

    // 出生渐显（alphaFade 族，AI 分发【前】的近似段）——静态半透明不受影响。
    // EoW 族（13-15）除外：走下方 AI 分发后的 1:1 段（移动门 -42/t，NPC.cs:52650-52670）
    if (this.alphaFade && !(this.vanillaId !== null && this.vanillaId >= 13 && this.vanillaId <= 15)) {
      this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
      if (this.spawnAlpha === 0) this.alphaFade = false;
    }

    const player = (game as unknown as { player: Player }).player;
    const hasPlayer = !!player && !player.dead;

    // ---- 原版数据驱动路径：按 aiStyle 分发到已移植的 AI 家族（分发后落入共享尾段） ----
    // 蠕虫身体段（wormFollow 非空）无 AI：位置由头部 wormAI 沿链驱动，但仍走共享尾段（接触伤害等）
    // 例外：EoW 三段各段独立跑 eowAI（断链自查 + 身/尾自跟随，:51874/:52266），
    // 不再由头统一驱动链——断链拆分后每条子虫的头各自驱动
    const eowSeg = this.vanillaId !== null && this.vanillaId >= 13 && this.vanillaId <= 15;
    const wormBody = this.wormFollow && !eowSeg;
    // 小动物（critter）优先走被动游荡，绝不落入 default 的追击 fallback
    if (this.vanilla && !wormBody && this.vanilla.critter) {
      this.critterWanderAI(game, hasPlayer ? player : null);
    } else if (this.vanilla && !wormBody) {
      const p = hasPlayer ? player : null;
      switch (this.vanilla.aiStyle) {
        case 92: this.dummyAI(game); break;                            // AI_092 训练假人（NPC 488）
        case 1: this.slimeAI(game, p); break;                          // AI_001 史莱姆
        case 2: this.floatEyeAI(game, p); break;                        // AI_002 飘浮眼（原版核）
        case 3:
          // AI_003 拜月教弓手 379/380 仪式待机（NPC.cs:56575-56601,ai[3]<0 静立面碑零伤；
          // 碑置 ai[3]=0 后激活复位 :56602-56609,回战士核）——bossAI_lunar_misc
          if ((this.vanillaId === 379 || this.vanillaId === 380) && this.ai3 < 0) {
            cultistArcherStandbyAI(this, game);
            break;
          }
          if (this.vanillaId === 379 || this.vanillaId === 380) cultistArcherWake(this);
          this.fighterAI(game, p);
          // 火把僵尸 590/591 手持火把发光（NPC.cs:57309-57366 AI_003 内 type 段）：
          //  590 按朝向取 (Center±22 / y+6) 格，火把格与相邻格均无液体才点亮；
          //  591 持械变体 !wet 即亮，偏移 ±36/±28（专家变体，尘需 ai[2]==0 门）。
          //  色 (1, 0.95, 0.8) = 与手持火把同色；尘 6 号 1/30 概率
          if (this.vanillaId === 590 || this.vanillaId === 591) this.torchZombieLight(game);
          // AI_003 火星尾段（bossAI_martian.ts）：军官 383 带盾无敌/补盾、工程师 386 放炮塔
          if (this.vanillaId === 383 || this.vanillaId === 386) martianFighterExtras(this, game, p);
          break;                                                        // AI_003 战士族（原版通用核）
        // EoC 传参例外:玩家死亡也要传原对象(cs:19931 dead 判定走逃离分支,
        // 冲刺计时合法冻结;传 null 会让 aiT 照走、状态机停摆 → 首冲时长翻倍)
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
        case 0: this.boundNPCAI(game, p); break;                          // AI_000 被缚NPC（cs:19774 站立/水上漂流；Enemy 侧防御，常规走 TownNPC.bound）
        case 17: this.vultureAI(game, p); break;                          // AI_017 秃鹫（cs:24079 栖息→200px盒/受击起飞，单向不回落）
        case 19: this.antlionAI(game, p); break;                          // AI_019 蚁狮（cs:24465 扎沙不动+沙球；传送带特例略）
        case 23: this.flyingWeaponAI(game, p); break;                     // AI_023 飞行武器（cs:25316 冲/漂100/转120 循环，受击回蓄转）
        case 25: this.mimicAI(game, p); break;                            // AI_025 宝箱怪（cs:25621 伪装200px盒→小小大跳循环）
        case 39: this.tortoiseAI(game, p); break;                         // AI_039 陆龟族（cs:29257 待机蓄力→蓄势→旋冲→恢复）
        case 41: this.herplingAI(game, p); break;                         // AI_041 赫柏林/德普林/378 咬齿炸弹（cs:30017 低跳连扑+自爆链）
        case 44: this.flyingSwarmerAI(game, p); break;                    // AI_044 飞鱼/蚁狮蜂（cs:30999 分轴限速追+失视逃逸）
        case 56: this.dungeonSpiritAI(game, p); break;                    // AI_056 地牢之魂（cs:32915 穿墙0.99惯性追踪）
        case 26: this.chargerAI(game, p); break;                        // AI_026 独角兽/冲锋族（原版核）
        case 107:                                                          // AI_107 ImprovedWalkers（NPC.cs:63372-64919）
          if (this.vanillaId !== 620) ai107ImprovedWalkers(this, game, p); // DD2 walker 族 1:1（bossAI_dd2.ts：近战前摇/投弹/掷矛/喷吐/自爆/灵气）
          else this.chargerAI(game, p, 1);                                 // 620 地精鲨（wet 游泳档,cs:64118-64230 专属分支）
          break;
        case 94: this.towerAI(game, p); break;                          // AI_094 星璇四塔（NPC.cs:41029-41443，核心 1:1）
        // ---- 星璇塔四组专属怪 1:1（bossAI_lunar_misc.ts；docs/event-lunar-pillars.md §4）----
        // 74 穿心者 418 / 75 日耀骑手 416 已由火星批 bossAI_martian.ts 落位（见下方
        // 火星族分发）；85/95/96/97/99 五族 1:1 内核在 lunar_misc（一期近似档已退役）。
        // 勘误：NPC 408 无 NewNPC 调用源（docs §4"408 由投射物 539 生成"不成立）。
        case 85: starCellAI(this, game, p); break;                    // AI_085 星细胞 405/星云头蟹 421（六态寻路+吸附）
        case 95: smallStarCellAI(this, game, p); break;               // AI_095 小星细胞 406（300t 长大 Transform 405）
        case 96: flowInvaderAI(this, game, p); break;                 // AI_096 水流入侵者 407(/408)（悬顶伺服+甩 539）
        case 97: nebulaFloaterAI(this, game, p); break;               // AI_097 星云悬浮脑 420（瞬移+环绕球 574→弹 576）
        case 99: solarSlimeAI(this, game, p); break;                  // AI_099 日耀黏液 519（坠落→落地 5t 自爆）
        // ---- 月事件（南瓜月/霜月）Boss 族 1:1（bossAI_moon_events.ts）----
        case 57: mourningWoodAI(this, game, p); break;                  // AI_057 悲木 325/常世吼 344（cs:32937 悬浮树怪+分阶段弹幕）
        case 58: pumpkingAI(this, game, p); break;                       // AI_058 南瓜王 327（cs:33246 悬浮/俯冲+生双刃）
        case 59: pumpkingBladeAI(this, game, p); break;                   // AI_059 南瓜王之刃 328（cs:33405 锚主环绕/俯冲/横扫）
        case 60: iceQueenAI(this, game, p); break;                        // AI_060 冰雪女王 345（cs:33588 滑翔/落冰/旋射三态）
        case 61: santaNK1AI(this, game, p); break;                        // AI_061 圣诞坦克 346（cs:33902 悬浮+链炮/火箭/礼盒）

```


---

## 🤖 Assistant · 2026-08-19T03:14:05.614Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Confirmed: these AI functions handle movement themselves (no shared movement after dispatch, except the "共享尾段" for contact damage etc.). So bigMimicAI state 4.1's missing movement in the (ai2==1, above player, vy>0) case is a real freeze — velocity accumulates vy up to 16 but position never updates.

Wait, actually, let me re-check. In the first branch `if (!p || e.y + e.h >= p.y || e.vy <= 0)` — hmm, once vy accumulates... vy starts at +8 (toward player below). vy only grows: min(vy+0.2, 16). So `e.vy <= 0` false. `e.y + e.h >= p.y`: e.y never changes (no movement) → if mimic was above player (y+h < p.y), stays above → false forever. `!p` false. So the first branch never fires; the second branch requires ai2===0, but ai2 was just set to 1 at the top (when LOS && !inSolidBody). Result: mimic freezes mid-air permanently in the common LOS case.

Hmm wait — but hold on. Let me re-check the transition from state 4 to 4.1: state 4 sets `e.vx = tx; e.vy = ty` where ty = (dy/d)*8 with dy = player.cy - e.cy (positive if player below). So yes vy>0 diving down. First tick of 4.1: LOS clear (mimic flew above player at 350px, likely LOS clear through air), not in solid → ai2 = 1 → frozen forever.

Hmm, that seems like a very visible bug that would have been noticed... unless inSolidBody is usually true right after transition? No. Or unless losClear from 350px above through air — usually clear. Hmm.

Wait, wait. Let me re-read the transition condition in vanilla once more:

```
else if (this.ai[0] == 4.1f)
{
    knockBackResist = 0f;
    if (this.ai[2] == 0f && Collision.CanHit(...) && !Collision.SolidCollision(position, width, height))
    {
        this.ai[2] = 1f;
    }
    if (position.Y + (float)height >= Main.player[target].position.Y || velocity.Y <= 0f)
    {
        ... ai[1] += 1; if > 10 → 2 (or 5 if solid) ...
    }
    else if (this.ai[2] == 0f)
    {
        noTileCollide = true;
        noGravity = true;
        knockBackResist = 0f;
    }
    velocity.Y += 0.2f;
    if (velocity.Y > 16f) velocity.Y = 16f;
}
```

So in vanilla, with ai2==1 and above player and vy>0: neither branch → noGravity stays false, noTileCollide stays false (reset at top of aiStyle 87) → gravity... wait, but gravity for NPCs: does the shared update apply gravity? Yes, for !noGravity NPCs gravity is applied in the shared section. Plus 4.1 adds vy += 0.2 itself. So it falls with tile collision. The mimic "aligned dive" = fall onto the player with collision.

Our version: in that case → NO movement at all. Also note: our `e.vy = Math.min(e.vy + 0.2, 16)` runs BEFORE the branch (equivalent to vanilla's after).

Also another subtle difference: in ours, the first branch `if (!p || e.y + e.h >= p.y || e.vy <= 0)` — vanilla doesn't have `!p` (it indexes Main.player[target] which could be dead...). Fine.

So CONFIRMED bug #1: bigMimic 4.1 ai2==1 aligned-dive case lacks the collision fall movement → mimic freezes mid-air above player indefinitely (until player moves under it? No — position frozen means y+h >= p.y can only become true if the PLAYER moves up into the mimic; otherwise stuck). Actually the player could jump into it. But structurally: freeze.

Severity: high (state machine dead-lock in a common path).

Let me now double-check the claim "4.1 仅未过玩家Y且ai[2]==0的真俯冲段(:39724-39730),过顶回落段 false" in the comment — they interpreted the else-if(ai2==0) branch as the noGravity segment and deliberately didn't set noGravity otherwise, but forgot the movement entirely.

Actually hmm, wait. Let me re-read our code once more:

```js
} else if (e.ai0 === 4.1) {
    if (e.ai2 === 0 && p && losClear(game, e.cx, e.cy, p.cx, p.cy) && !inSolidBody(game, e)) e.ai2 = 1;
    e.vy = Math.min(e.vy + 0.2, 16);
    if (!p || e.y + e.h >= p.y || e.vy <= 0) {
      e.ai1 += 1;
      if (e.ai1 > 10) {
        e.ai0 = inSolidBody(game, e) ? 5 : 2;
        e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
      }
      moveAndCollide(e, game.world, e.vx, e.vy);
    } else if (e.ai2 === 0) {
      e.noGravity = true;
      fly(e);
    }
  }
```

Yes — if ai2==1 and above player and vy>0: nothing. Frozen. CONFIRMED.

Hmm, but wait — could ai1 be nonzero from earlier ticks so that "if (e.ai1 > 10)" fires quickly? ai1 was reset when entering 4.1 (ai1=0). ai1 only increments in the first branch. So no.

Also note: in vanilla, when vy<=0 OR past player → ai1++ and after >10 → state 2. In that window (first branch), vanilla does NOT set noGravity → gravity + collision... wait no: the first branch in vanilla also doesn't set noGravity/noTileCollide — but they're false by default anyway. So vanilla movement = collision-based fall. Ours calls moveAndCollide with e.vx, e.vy — but our e.noGravity was set true in the previous tick's dive (state 4 set noGravity = true... wait, does our engine use noGravity anywhere for movement? We call moveAndCollide explicitly with vy, so noGravity flag doesn't matter — WE control gravity via `e.vy = Math.min(e.vy + 0.2, 16)`. OK so first branch is fine.

So the only missing piece is the third case movement. In vanilla, ai2==1 case → falls via shared movement with collision. So the fix: add an `else { moveAndCollide(e, game.world, e.vx, e.vy); }` for the ai2==1 case.

Now, Mothron (39876-40406). Read vanilla.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:06.345Z · glm-x-preview-260804

```
Enemy.ts 已确认这些 AI 自行处理移动 —— 模仿者 4.1 停滞问题是真实存在的。现在检查 Mothron 家族 (39876-40406)。
```


---

## 🤖 Assistant · 2026-08-19T03:14:06.789Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '39876,40060p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla Mothron AI part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:06.857Z

**📎 ToolResult**

```
		else if (aiStyle == 88)
		{
			int num1412 = 7;
			noTileCollide = false;
			noGravity = true;
			knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.2f);
			damage = defDamage;
			if (!Main.eclipse && Main.netMode != 1)
			{
				if (this.ai[0] != -1f)
				{
					netUpdate = true;
				}
				this.ai[0] = -1f;
			}
			else if (target < 0 || Main.player[target].dead || !Main.player[target].active)
			{
				TargetClosest();
				Vector2 vector247 = Main.player[target].Center - base.Center;
				if (Main.netMode != 1 && (Main.player[target].dead || vector247.Length() > 3000f))
				{
					if (this.ai[0] != -1f)
					{
						netUpdate = true;
					}
					this.ai[0] = -1f;
				}
			}
			else
			{
				Vector2 vector248 = Main.player[target].Center - base.Center;
				if (Main.netMode != 1 && this.ai[0] > 1f && vector248.Length() > 1000f)
				{
					if (this.ai[0] != 1f)
					{
						netUpdate = true;
					}
					this.ai[0] = 1f;
				}
			}
			if (this.ai[0] == -1f)
			{
				Vector2 vector249 = new Vector2(0f, -8f);
				velocity = (velocity * 9f + vector249) / 10f;
				noTileCollide = true;
				dontTakeDamage = true;
			}
			else if (this.ai[0] == 0f)
			{
				TargetClosest();
				if (base.Center.X < Main.player[target].Center.X - 2f)
				{
					direction = 1;
				}
				if (base.Center.X > Main.player[target].Center.X + 2f)
				{
					direction = -1;
				}
				spriteDirection = direction;
				rotation = (rotation * 9f + velocity.X * 0.1f) / 10f;
				if (collideX)
				{
					velocity.X *= (0f - oldVelocity.X) * 0.5f;
					if (velocity.X > 4f)
					{
						velocity.X = 4f;
					}
					if (velocity.X < -4f)
					{
						velocity.X = -4f;
					}
				}
				if (collideY)
				{
					velocity.Y *= (0f - oldVelocity.Y) * 0.5f;
					if (velocity.Y > 4f)
					{
						velocity.Y = 4f;
					}
					if (velocity.Y < -4f)
					{
						velocity.Y = -4f;
					}
				}
				Vector2 vector250 = Main.player[target].Center - base.Center;
				vector250.Y -= 200f;
				if (vector250.Length() > 800f)
				{
					this.ai[0] = 1f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
					netUpdate = true;
				}
				else if (vector250.Length() > 80f)
				{
					float num1413 = 6f;
					float num1414 = 30f;
					vector250.Normalize();
					vector250 *= num1413;
					velocity = (velocity * (num1414 - 1f) + vector250) / num1414;
				}
				else if (velocity.Length() > 2f)
				{
					velocity *= 0.95f;
				}
				else if (velocity.Length() < 1f)
				{
					velocity *= 1.05f;
				}
				if (Main.netMode == 1)
				{
					return;
				}
				this.ai[1] += 1f;
				if (justHit)
				{
					this.ai[1] += Main.rand.Next(10, 30);
				}
				if (!(this.ai[1] >= 180f))
				{
					return;
				}
				this.ai[1] = 0f;
				this.ai[2] = 0f;
				this.ai[3] = 0f;
				netUpdate = true;
				while (this.ai[0] == 0f)
				{
					int num1415 = Main.rand.Next(3);
					if (num1415 == 0 && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
					{
						this.ai[0] = 2f;
						continue;
					}
					switch (num1415)
					{
					case 1:
						this.ai[0] = 3f;
						break;
					case 2:
						if (CountNPCS(478) + CountNPCS(479) < num1412)
						{
							this.ai[0] = 4f;
						}
						break;
					}
				}
			}
			else if (this.ai[0] == 1f)
			{
				collideX = false;
				collideY = false;
				noTileCollide = true;
				knockBackResist = 0f;
				if (target < 0 || !Main.player[target].active || Main.player[target].dead)
				{
					TargetClosest();
				}
				if (velocity.X < 0f)
				{
					direction = -1;
				}
				else if (velocity.X > 0f)
				{
					direction = 1;
				}
				spriteDirection = direction;
				rotation = (rotation * 9f + velocity.X * 0.08f) / 10f;
				Vector2 vector251 = Main.player[target].Center - base.Center;
				if (Main.netMode != 1 && vector251.Length() < 300f && !Collision.SolidCollision(position, width, height))
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
					netUpdate = true;
				}
				float num1416 = 7f + vector251.Length() / 100f;
				float num1417 = 25f;
				vector251.Normalize();
				vector251 *= num1416;
				velocity = (velocity * (num1417 - 1f) + vector251) / num1417;
			}
			else if (this.ai[0] == 2f)

```


---

## 🤖 Assistant · 2026-08-19T03:14:18.219Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Mothron state 0 hover:
- ours: facing, spin, then `moveAndCollide` + bounceAxis (collideX/collideY handling). Vanilla reads collideX/collideY from the PREVIOUS tick's collision (they're set by the collision step and persist). Our approach: move first then bounce using pre-move velocity — approximately equivalent to vanilla reading last tick's collide flags before this tick's movement. Actually vanilla applies bounce BEFORE modifying velocity toward the target, using collide flags from last tick's movement. Ours: moveAndCollide then bounce. Both orderings produce similar behavior; minor.

- One notable difference: vanilla's target-dead branch: `if target<0 || dead || !active → TargetClosest(); if (dead || dist>3000) → ai[0]=-1`. Ours: `else if (!p) e.ai0 = -1` — no 3000px despawn check. Vanilla also goes -1 when the player is >3000px away even if alive. Ours drops this. Minor deviation (flee semantics without source) — actually ours is missing a vanilla behavior (3000px → flee). It's a deviation but low impact. Hmm — "flee 或事件结束语义无出处" is an audit dimension: ours only has !p. Vanilla: eclipse off → -1; target dead/inactive/(>3000px) → -1. Ours covers eclipse off and !p (dead). Missing >3000px case. Minor, reportable as low.

- The 180t pick loop: vanilla `while (ai[0]==0)` re-rolls indefinitely: rand(3); if 0 && CanHit → 2; if 1 → 3; if 2 && count < 7 → 4; otherwise stays 0 and re-rolls. Ours: `const pick = rnd(3)` once — if pick==0 but no LOS → stays ai0 = 0 (comment says "原版 while 重摇,单帧一次近似"). With ai1 reset to 0 → effectively delays 180t before next attempt instead of instant re-roll. Documented approximation. Acceptable-ish but could report as minor. It's disclosed in code comment. Not structural — skip.

Now continue vanilla 40060-40220.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:18.594Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '40060,40230p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla Mothron AI part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:18.713Z

**📎 ToolResult**

```
			else if (this.ai[0] == 2f)
			{
				damage = (int)((double)defDamage * 0.5);
				knockBackResist = 0f;
				if (target < 0 || !Main.player[target].active || Main.player[target].dead)
				{
					TargetClosest();
					this.ai[0] = 0f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
					netUpdate = true;
				}
				if (Main.player[target].Center.X - 10f < base.Center.X)
				{
					direction = -1;
				}
				else if (Main.player[target].Center.X + 10f > base.Center.X)
				{
					direction = 1;
				}
				spriteDirection = direction;
				rotation = (rotation * 4f + velocity.X * 0.1f) / 5f;
				if (collideX)
				{
					velocity.X *= (0f - oldVelocity.X) * 0.5f;
					if (velocity.X > 4f)
					{
						velocity.X = 4f;
					}
					if (velocity.X < -4f)
					{
						velocity.X = -4f;
					}
				}
				if (collideY)
				{
					velocity.Y *= (0f - oldVelocity.Y) * 0.5f;
					if (velocity.Y > 4f)
					{
						velocity.Y = 4f;
					}
					if (velocity.Y < -4f)
					{
						velocity.Y = -4f;
					}
				}
				Vector2 vector252 = Main.player[target].Center - base.Center;
				vector252.Y -= 20f;
				this.ai[2] += 1f / 45f;
				if (Main.expertMode)
				{
					this.ai[2] += 1f / 60f;
				}
				float num1418 = 4f + this.ai[2] + vector252.Length() / 120f;
				float num1419 = 20f;
				vector252.Normalize();
				vector252 *= num1418;
				velocity = (velocity * (num1419 - 1f) + vector252) / num1419;
				if (Main.netMode != 1)
				{
					this.ai[1] += 1f;
					if (this.ai[1] > 240f || !Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
					{
						this.ai[0] = 0f;
						this.ai[1] = 0f;
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
					}
				}
			}
			else if (this.ai[0] == 3f)
			{
				knockBackResist = 0f;
				noTileCollide = true;
				if (velocity.X < 0f)
				{
					direction = -1;
				}
				else
				{
					direction = 1;
				}
				spriteDirection = direction;
				rotation = (rotation * 4f + velocity.X * 0.07f) / 5f;
				Vector2 vector253 = Main.player[target].Center - base.Center;
				vector253.Y -= 12f;
				if (base.Center.X > Main.player[target].Center.X)
				{
					vector253.X += 400f;
				}
				else
				{
					vector253.X -= 400f;
				}
				if (Main.netMode != 1 && Math.Abs(base.Center.X - Main.player[target].Center.X) > 350f && Math.Abs(base.Center.Y - Main.player[target].Center.Y) < 20f)
				{
					this.ai[0] = 3.1f;
					this.ai[1] = 0f;
					netUpdate = true;
				}
				this.ai[1] += 1f / 30f;
				float num1420 = 8f + this.ai[1];
				float num1421 = 4f;
				vector253.Normalize();
				vector253 *= num1420;
				velocity = (velocity * (num1421 - 1f) + vector253) / num1421;
			}
			else if (this.ai[0] == 3.1f)
			{
				knockBackResist = 0f;
				noTileCollide = true;
				rotation = (rotation * 4f + velocity.X * 0.07f) / 5f;
				Vector2 vector254 = Main.player[target].Center - base.Center;
				vector254.Y -= 12f;
				float num1422 = 16f;
				float num1423 = 8f;
				vector254.Normalize();
				vector254 *= num1422;
				velocity = (velocity * (num1423 - 1f) + vector254) / num1423;
				if (velocity.X < 0f)
				{
					direction = -1;
				}
				else
				{
					direction = 1;
				}
				spriteDirection = direction;
				this.ai[1] += 1f;
				if (Main.netMode != 1 && this.ai[1] > 10f)
				{
					velocity = vector254;
					if (velocity.X < 0f)
					{
						direction = -1;
					}
					else
					{
						direction = 1;
					}
					this.ai[0] = 3.2f;
					this.ai[1] = 0f;
					this.ai[1] = direction;
					netUpdate = true;
				}
			}
			else if (this.ai[0] == 3.2f)
			{
				damage = (int)((double)defDamage * 1.3);
				collideX = false;
				collideY = false;
				knockBackResist = 0f;
				noTileCollide = true;
				this.ai[2] += 1f / 30f;
				velocity.X = (16f + this.ai[2]) * this.ai[1];
				if ((this.ai[1] > 0f && base.Center.X > Main.player[target].Center.X + 260f) || (this.ai[1] < 0f && base.Center.X < Main.player[target].Center.X - 260f))
				{
					if (Main.netMode != 1 && !Collision.SolidCollision(position, width, height))
					{
						this.ai[0] = 0f;
						this.ai[1] = 0f;
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
					}
					else if (Main.netMode != 1 && Math.Abs(base.Center.X - Main.player[target].Center.X) > 800f)
					{
						this.ai[0] = 1f;
						this.ai[1] = 0f;

```


---

## 🤖 Assistant · 2026-08-19T03:14:22.580Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '40230,40450p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla Mothron AI part 3 plus egg AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:22.692Z

**📎 ToolResult**

```
						this.ai[1] = 0f;
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
					}
				}
				rotation = (rotation * 4f + velocity.X * 0.07f) / 5f;
			}
			else if (this.ai[0] == 4f)
			{
				bool flag95 = (double)(base.Center.Y / 16f) < Main.worldSurface;
				TargetClosest();
				if (Main.netMode != 1)
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					for (int num1424 = 0; num1424 < 1000; num1424++)
					{
						int num1425 = (int)Main.player[target].Center.X / 16;
						int num1426 = (int)Main.player[target].Center.Y / 16;
						int num1427 = 30 + num1424 / 50;
						int num1428 = 20 + num1424 / 75;
						num1425 += Main.rand.Next(-num1427, num1427 + 1);
						num1426 += Main.rand.Next(-num1428, num1428 + 1);
						if (WorldGen.SolidTile(num1425, num1426))
						{
							continue;
						}
						bool flag96 = false;
						int num1429 = 50;
						while (num1429 > 0)
						{
							num1429--;
							if (!WorldGen.InWorld(num1425, num1426, 5))
							{
								flag96 = true;
								break;
							}
							Tile tile2 = Main.tile[num1425, num1426];
							if (tile2 == null)
							{
								flag96 = true;
								break;
							}
							if (tile2.liquid > 0 && tile2.lava())
							{
								flag96 = true;
								break;
							}
							Tile tile3 = Main.tile[num1425, num1426 - 1];
							if (tile3 == null)
							{
								flag96 = true;
								break;
							}
							if (tile3.liquid > 0 && tile3.lava())
							{
								flag96 = true;
								break;
							}
							if (WorldGen.SolidTile(num1425, num1426) || (flag95 && (double)num1426 > Main.worldSurface))
							{
								break;
							}
							num1426++;
						}
						if (!(num1429 <= 0 || flag96) && (new Vector2(num1425 * 16 + 8, num1426 * 16 + 8) - Main.player[target].Center).Length() < 600f)
						{
							this.ai[0] = 4.1f;
							this.ai[1] = num1425;
							this.ai[2] = num1426;
							break;
						}
					}
				}
				netUpdate = true;
			}
			else if (this.ai[0] == 4.1f)
			{
				if (velocity.X < -2f)
				{
					direction = -1;
				}
				else if (velocity.X > 2f)
				{
					direction = 1;
				}
				spriteDirection = direction;
				rotation = (rotation * 9f + velocity.X * 0.1f) / 10f;
				noTileCollide = true;
				int num1430 = (int)this.ai[1];
				int num1431 = (int)this.ai[2];
				float x4 = num1430 * 16 + 8;
				float y4 = num1431 * 16 - 20;
				Vector2 v13 = new Vector2(x4, y4);
				v13 -= base.Center;
				float num1432 = 6f + v13.Length() / 150f;
				if (num1432 > 10f)
				{
					num1432 = 10f;
				}
				float num1433 = 10f;
				if (v13.Length() < 10f)
				{
					this.ai[0] = 4.2f;
					netUpdate = true;
				}
				v13 = v13.SafeNormalize(Vector2.Zero);
				v13 *= num1432;
				velocity = (velocity * (num1433 - 1f) + v13) / num1433;
				if (velocity.Length() > num1432)
				{
					velocity.Normalize();
					velocity *= num1432;
				}
			}
			else
			{
				if (this.ai[0] != 4.2f)
				{
					return;
				}
				rotation = (rotation * 9f + velocity.X * 0.1f) / 10f;
				knockBackResist = 0f;
				noTileCollide = true;
				int num1434 = (int)this.ai[1];
				int num1435 = (int)this.ai[2];
				float x5 = num1434 * 16 + 8;
				float y5 = num1435 * 16 - 20;
				Vector2 vector255 = new Vector2(x5, y5);
				vector255 -= base.Center;
				float num1436 = 4f;
				float num1437 = 2f;
				if (Main.netMode != 1 && vector255.Length() < 4f)
				{
					int num1438 = 70;
					if (Main.expertMode)
					{
						num1438 = (int)((double)num1438 * 0.75);
					}
					this.ai[3] += 1f;
					if (this.ai[3] == (float)num1438)
					{
						int num1439 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), num1434 * 16 + 8, num1435 * 16, 478, whoAmI);
						Main.npc[num1439].netUpdate = true;
					}
					else if (this.ai[3] == (float)(num1438 * 2))
					{
						this.ai[0] = 0f;
						this.ai[1] = 0f;
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
						if (CountNPCS(478) + CountNPCS(479) < num1412 && Main.rand.Next(3) != 0)
						{
							this.ai[0] = 4f;
						}
						else if (Collision.SolidCollision(position, width, height))
						{
							this.ai[0] = 1f;
						}
					}
				}
				if (vector255.Length() > num1436)
				{
					vector255.Normalize();
					vector255 *= num1436;
				}
				velocity = (velocity * (num1437 - 1f) + vector255) / num1437;
				if (velocity.Length() > num1436)
				{
					velocity.Normalize();
					velocity *= num1436;
				}
			}
		}
		else if (aiStyle == 89)
		{
			if (velocity.Y == 0f)
			{
				velocity.X *= 0.9f;
				rotation += velocity.X * 0.02f;
			}
			else
			{
				velocity.X *= 0.99f;
				rotation += velocity.X * 0.04f;
			}
			int num1440 = 900;
			if (Main.expertMode)
			{
				num1440 = 600;
			}
			if (justHit)
			{
				this.ai[0] -= Main.rand.Next(10, 21);
				if (!Main.expertMode)
				{
					this.ai[0] -= Main.rand.Next(10, 21);
				}
			}
			this.ai[0] += 1f;
			if (this.ai[0] >= (float)num1440)
			{
				Transform(479);
			}
			if (Main.netMode != 1 && velocity.Y == 0f && (double)Math.Abs(velocity.X) < 0.2 && (double)this.ai[0] >= (double)num1440 * 0.75)
			{
				float num1441 = this.ai[0] - (float)num1440 * 0.75f;
				num1441 /= (float)num1440 * 0.25f;
				if ((float)Main.rand.Next(-10, 120) < num1441 * 100f)
				{
					velocity.Y -= (float)Main.rand.Next(20, 40) * 0.025f;
					velocity.X += (float)Main.rand.Next(-20, 20) * 0.025f;
					velocity *= 1f + num1441 * 2f;
					netUpdate = true;
				}
			}
		}
		else if (aiStyle == 90)

```


---

## 🤖 Assistant · 2026-08-19T03:15:20.543Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Mothron comparison:

State 4 (egg-laying search):
- Vanilla resets ai[0..2] = 0 FIRST, then searches; if found → 4.1 with ai1/ai2 = tile. Ours does the same.
- Vanilla: `num1425 = player.cx/16` (int truncation) then add random ±num1427. Ours: ptx + rndRange(-rx, rx+1) = ptx + [-rx, rx]. Matches Next(-n, n+1).
- Search loop: identical structure. `aboveGround = e.cy / TILE < game.world.groundLevel`. Vanilla flag95 = Center.Y/16 < worldSurface. Ours: `e.cy / TILE < game.world.groundLevel` — is groundLevel ≈ worldSurface in tiles? Need to check game.world.groundLevel units. In this repo, groundLevel is probably in tiles. Let me check quickly. Actually in other code I saw `game.world.groundLevel` compared with `ty >` — vanilla compares num1426 (tile) > Main.worldSurface (double, in tiles). If repo groundLevel is in tiles, matches.
- The 4.2 hatch: `NewNPC(..., num1434*16+8, num1435*16, 478)` — egg position y = num1435*16 (top-left at tile top). Ours: `egg.y = e.ai2 * TILE - egg.h` — bottom at tile top. Egg height for 478? If 478 height is 22... vanilla y = num1435*16 top → bottom = num1435*16+h → embedded into the ground by h. Hmm wait NewNPC position is the NPC top-left; egg spawns with its top at the tile top, so the egg overlaps the ground tile below (it'll be pushed up? or settle). Actually vanilla eggs appear sitting on the ground with their bottom at (num1435*16 + height). Hmm, that would embed the egg INTO the floor. But wait — num1435 is the tile where the search found a solid tile BELOW (the search increments num1426 until solid → so num1435 = the air tile just above the solid floor? No: `if (WorldGen.SolidTile(num1425, num1426)) break;` — breaks when the CURRENT tile is solid → num1435 IS the solid floor tile. Then y = num1435*16 = top of the floor tile. So the egg top = floor top → egg fully embedded in the ground?! Hmm. That doesn't sound right visually... but eggs are small (478 egg is like 16x22?). Actually looking at Mothron egg laying in-game: the egg is embedded in the ground, only the top part sticks out? Let me think... In Terraria, Mothron lays eggs that appear to sit ON the ground. With y = floor top, the egg's top at floor top means the egg is fully buried. Hmm, wait — maybe the search lands on the tile ABOVE the solid one: the loop checks `if solid → break` with the check happening at the top; num1426 starts at the random point and increments. When it breaks, num1426 = first solid tile. So yes num1435 = solid tile.

Hmm, but hold on: NewNPC y is the NPC's position.Y = top. Egg height 478 = 34? Let me not go down this hole — vanilla: egg top anchored at floor tile top (egg visually sunk into floor, only matching if egg height ≤ 16?). Actually the egg sprite for 478 is 34px tall per vanilla NPC SetDefaults? Hmm. In-game Mothron eggs are partially sunken? Let me check vanilla NPC.SetDefaults for 478 height... Actually, it doesn't matter much: ours places egg bottom at floor top (fully above). This is a visual placement difference of one egg-height; vanilla has it sunk (position y = tile*16). Wait — maybe there's special handling in NewNPC or NPC spawning that shifts y. NewNPC → npc.position = (x, y). Then the AI 89 gravity settles it... it's already on/in ground.

Actually hmm, I realize the same pattern appeared for the devotees: vanilla spawns at Y*16-48 (bottom at Y*16 exactly if h=48). For the egg: y=num1435*16 with the egg height probably 16? Egg 478 frame: The Mothron egg sprite... it's 16 wide 16 high? If height is 16, bottom = num1435*16+16 = 1 tile below the surface tile top → embedded 1 tile. Hmm.

OK whatever — this is sub-visual. Ours: bottom at tile top. Vanilla: top at tile top. If egg height is ~34, ours sits visibly on ground, vanilla sinks. It's a minor placement deviation, low priority. Not worth one of the 10 slots.

Wait, actually, let me reconsider: is it y = num1435*16 or num1435*16 - something? Reading again: `NewNPC(GetSpawnSourceForNPCFromNPCAI(), num1434 * 16 + 8, num1435 * 16, 478, whoAmI)` — yes y = num1435*16. Hmm interesting. But note in our 4.2 hover target: `gy = e.ai2 * TILE - 20` — vanilla y4 = num1431*16 - 20. Matches.

State 2 details:
- vanilla damage = defDamage*0.5 — ours Math.round(baseDmg*0.5). OK.
- target dead → reset to 0 (ours: the !p case was already handled by the global gate at top which sets ai0=-1 for mothron. Wait — for mothron ours: `if (!game.world.clock.eclipse) ai0=-1 else if (!p) ai0 = -1`. Vanilla for state 2 with dead target: TargetClosest; if still dead → ai[0] = 0. But the global gate at top already set ai[0] = -1 for dead target, so state 2's dead-check is unreachable in vanilla too (the top gate runs first). OK.
- ai2 += 1/45 (+1/60 expert). ours: `e.ai2 += 1 / 45; if (EXPERT) e.ai2 += 1 / 60;` OK.
- speed 4 + ai2 + d/120, 20 step. Ours matches.
- exit: ai1 > 240 || !CanHit → 0. Ours matches.

State 3: 
- dx ±400: vanilla `if (e.cx > p.cx) vector253.X += 400 else -= 400`. Ours: `if (e.cx > p.cx) dx += 400; else dx -= 400`. Matches.
- Transition to 3.1: |dx|>350 && |dy|<20 → 3.1, ai1 = 0. Ours matches.
- ai1 += 1/30; speed 8+ai1, step 4. Ours matches.
- Vanilla dy = p.cy - 12 - e.cy. Ours: dy = p.cy - 12 - e.cy. Matches.

State 3.1: target = player - 12; speed 16 step 8. ai1 > 10 → 3.2, ai1 = direction, velocity = vector254 (normalized*16). Ours: matches (e.vx = (dx/d)*16).

State 3.2: damage ×1.3; ai2 += 1/30; vx = (16+ai2)*ai1; pass-player checks. Ours matches; note ours doesn't set vy=0... vanilla leaves vy unchanged in 3.2. Ours leaves vy unchanged. OK.

State 4.1: speed 6 + d/150 cap 10, step 10; d < 10 → 4.2. Ours matches.
- direction: velocity.X < -2 → -1; > 2 → 1. Ours matches.

State 4.2: hover speed 4 step 2; if d < 4: hatch at 70 (expert 52.5 → (int)(70*0.75) = 52). Ours: `hatchT = EXPERT ? Math.round(70*0.75) : 70` = 52 expert. OK.
- At num1438: spawn egg at (ai1*16+8, ai2*16). Ours: egg.x = ai1*TILE + 8 - w/2; egg.y = ai2*TILE - h. As discussed, minor placement deviation.
- At num1438*2 → state 0; if count < 7 && rand(3)!=0 → 4; else if solid → 1. Ours matches.

Egg AI (89): vanilla exactly as ours: vy==0 → vx *= 0.9, rotation += vx*0.02; else vx *= 0.99, rotation += vx*0.04. justHit → ai0 -= Next(10,21); if !expert -= Next(10,21). ai0 += 1; >= 900 (600 expert) → Transform(479). Twitch: vy==0 && |vx|<0.2 && ai0 >= 900*0.75: num1441 = (ai0 - 675)/225; rand(-10,120) < num1441*100 → vy -= Next(20,40)*0.025; vx += Next(-20,20)*0.025; velocity *= 1+num1441*2. Ours matches (rndRange(-10,120): rand.Next(-10,120) = [-10,119]. rndRange(-10,120) = -10 + floor(rand*130) = [-10,119]. OK. rndRange(20,40) = [20,39]. Next(20,40) = [20,39]. OK. rndRange(-20,20) = [-20,19]. Next(-20,20) = [-20,19]. OK.)

But note: ours applies gravity at end via moveAndCollide — vanilla relies on shared gravity. Fine.

Now the mothron egg -1 gate: `if (e.ai0 < 0) e.ai0 = 0` at the start — WAIT. The justHit handler DECREMENTS ai0 (to accelerate hatching). If ai0 goes negative, ours... The order in ours: `if (e.ai0 < 0) e.ai0 = 0;` comes FIRST (line 980), before justHit handling? Let me re-read:

```js
export function mothronEggAI(e: Enemy, game: GameHooks, _player: Player | null) {
  const hatchT = EXPERT ? 600 : 900;
  if (e.ai0 < 0) e.ai0 = 0;
  ...
  if (e.justHit) {
    e.ai0 -= rndRange(10, 21);
    if (!EXPERT) e.ai0 -= rndRange(10, 21);
  }
  e.ai0 += 1;
```

Hmm: the `if (e.ai0 < 0) e.ai0 = 0` clamp happens before the decrement — this is the Enemy sentinel -1120 normalization (ai0 defaults to -1120 in this repo). After justHit decrements, ai0 could go negative — then NEXT tick the clamp `if (e.ai0 < 0) e.ai0 = 0` ZEROES it, erasing the accumulated hatch progress below zero! E.g., egg at ai0=5 gets hit twice: ai0 = 5 - 15 - 15 = -25. Next tick: ai0 < 0 → ai0 = 0 (progress reset to 0, but hatching is at >= 900 so being negative just means "not yet"). Wait, in vanilla negative ai0 is fine — it just needs to count up to 900. The clamp to 0 in ours means: hit an egg early (ai0 small) → ai0 negative → next tick reset to 0. Effect: hatch delay extended by up to 40 ticks per hit beyond vanilla? No wait — vanilla: ai0 = -25, then counts up: reaches 900 at tick 925 from now. Ours: ai0 = 0 → reaches 900 at tick 900 from now. So ours actually hatches EARLIER (up to 40t sooner) after early hits than vanilla. Marginal. Hmm, but wait: also the twitch gate `ai0 >= hatchT*0.75` — negative ai0 vs 0 barely matters.

Hmm, but actually, why is the clamp there? Because Enemy ai0 default is -1120 (sentinel). On first tick, ai0 = -1120 → clamp to 0. OK. But the clamp re-fires every tick when ai0 < 0, clobbering legitimate negative progress from justHit. Minor deviation: hatch timing after early hits slightly off (earlier by ≤40t). Low priority; not top-10 material probably. Actually hold on, it also affects repeated hits: each hit while ai0 < 20 has no cumulative effect in ours (clamped to 0 each tick), whereas vanilla accumulates negative (egg can't hatch FASTER — negative just delays... wait no: hatch is when ai0 >= 900. Vanilla being at -25 vs ours at 0: vanilla needs 925 more ticks, ours 900 → ours faster. Hitting repeatedly in vanilla keeps pushing the hatch LATER (subtracting), ours has a floor at 0 → hitting stops delaying after ai0 hits 0. So vanilla: repeated hits DELAY hatching cumulatively without bound; ours: delay capped at (current ai0) → i.e., an egg hit many times early hatches ~900t after the last reset, while vanilla would take 900 + total-subtracted. Deviation exists but bounded by player hitting eggs... unusual. Low.

Also note the ai0 sentinel: our repo says Enemy ai0 initial = -1120. But wait, what about mothron spawning eggs with `egg.bInit = true` — does bInit affect ai0? No. OK.

Now baby mothron (aiStyle 90): read vanilla 40450-40685.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:20.968Z · glm-x-preview-260804

```
Mothron 的主要逻辑符合。现在查看幼年 Mothron (40450-40685) 和花岗岩元素 (40686-40870)。
```


---

## 🤖 Assistant · 2026-08-19T03:15:21.363Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '40450,40685p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla baby Mothron AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:21.419Z

**📎 ToolResult**

```
		else if (aiStyle == 90)
		{
			noTileCollide = false;
			knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.4f);
			noGravity = true;
			rotation = (rotation * 9f + velocity.X * 0.1f) / 10f;
			if (!Main.eclipse)
			{
				EncourageDespawn(5);
				velocity.Y -= 0.2f;
				if (velocity.Y < -8f)
				{
					velocity.Y = -8f;
				}
				noTileCollide = true;
				return;
			}
			if (this.ai[0] == 0f || this.ai[0] == 1f)
			{
				for (int num1442 = 0; num1442 < Main.maxNPCs; num1442++)
				{
					if (num1442 != whoAmI && Main.npc[num1442].active && Main.npc[num1442].type == type)
					{
						Vector2 vector256 = Main.npc[num1442].Center - base.Center;
						if (vector256.Length() < (float)(width + height))
						{
							vector256.Normalize();
							vector256 *= -0.1f;
							velocity += vector256;
							NPC nPC3 = Main.npc[num1442];
							nPC3.velocity -= vector256;
						}
					}
				}
			}
			if (target < 0 || Main.player[target].dead || !Main.player[target].active)
			{
				TargetClosest();
				Vector2 vector257 = Main.player[target].Center - base.Center;
				if (Main.player[target].dead || vector257.Length() > 3000f)
				{
					this.ai[0] = -1f;
				}
			}
			else
			{
				Vector2 vector258 = Main.player[target].Center - base.Center;
				if (this.ai[0] > 1f && vector258.Length() > 1000f)
				{
					this.ai[0] = 1f;
				}
			}
			if (this.ai[0] == -1f)
			{
				Vector2 vector259 = new Vector2(0f, -8f);
				velocity = (velocity * 9f + vector259) / 10f;
				noTileCollide = true;
				dontTakeDamage = true;
			}
			else if (this.ai[0] == 0f)
			{
				TargetClosest();
				spriteDirection = direction;
				if (collideX)
				{
					velocity.X *= (0f - oldVelocity.X) * 0.5f;
					if (velocity.X > 4f)
					{
						velocity.X = 4f;
					}
					if (velocity.X < -4f)
					{
						velocity.X = -4f;
					}
				}
				if (collideY)
				{
					velocity.Y *= (0f - oldVelocity.Y) * 0.5f;
					if (velocity.Y > 4f)
					{
						velocity.Y = 4f;
					}
					if (velocity.Y < -4f)
					{
						velocity.Y = -4f;
					}
				}
				Vector2 vector260 = Main.player[target].Center - base.Center;
				if (vector260.Length() > 800f)
				{
					this.ai[0] = 1f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
				}
				else if (vector260.Length() > 200f)
				{
					float num1443 = 5.5f + vector260.Length() / 100f + this.ai[1] / 15f;
					float num1444 = 40f;
					vector260.Normalize();
					vector260 *= num1443;
					velocity = (velocity * (num1444 - 1f) + vector260) / num1444;
				}
				else if (velocity.Length() > 2f)
				{
					velocity *= 0.95f;
				}
				else if (velocity.Length() < 1f)
				{
					velocity *= 1.05f;
				}
				this.ai[1] += 1f;
				if (this.ai[1] >= 90f)
				{
					this.ai[1] = 0f;
					this.ai[0] = 2f;
				}
			}
			else if (this.ai[0] == 1f)
			{
				collideX = false;
				collideY = false;
				noTileCollide = true;
				knockBackResist = 0f;
				if (target < 0 || !Main.player[target].active || Main.player[target].dead)
				{
					TargetClosest();
				}
				if (velocity.X < 0f)
				{
					direction = -1;
				}
				else if (velocity.X > 0f)
				{
					direction = 1;
				}
				spriteDirection = direction;
				rotation = (rotation * 9f + velocity.X * 0.08f) / 10f;
				Vector2 vector261 = Main.player[target].Center - base.Center;
				if (vector261.Length() < 300f && !Collision.SolidCollision(position, width, height))
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
					this.ai[2] = 0f;
					this.ai[3] = 0f;
				}
				this.ai[2] += 1f / 60f;
				float num1445 = 5.5f + this.ai[2] + vector261.Length() / 150f;
				float num1446 = 35f;
				vector261.Normalize();
				vector261 *= num1445;
				velocity = (velocity * (num1446 - 1f) + vector261) / num1446;
			}
			else if (this.ai[0] == 2f)
			{
				if (velocity.X < 0f)
				{
					direction = -1;
				}
				else if (velocity.X > 0f)
				{
					direction = 1;
				}
				spriteDirection = direction;
				rotation = (rotation * 7f + velocity.X * 0.1f) / 8f;
				knockBackResist = 0f;
				noTileCollide = true;
				Vector2 vector262 = Main.player[target].Center - base.Center;
				vector262.Y -= 8f;
				float num1447 = 9f;
				float num1448 = 8f;
				vector262.Normalize();
				vector262 *= num1447;
				velocity = (velocity * (num1448 - 1f) + vector262) / num1448;
				if (velocity.X < 0f)
				{
					direction = -1;
				}
				else
				{
					direction = 1;
				}
				spriteDirection = direction;
				this.ai[1] += 1f;
				if (this.ai[1] > 10f)
				{
					velocity = vector262;
					if (velocity.X < 0f)
					{
						direction = -1;
					}
					else
					{
						direction = 1;
					}
					this.ai[0] = 2.1f;
					this.ai[1] = 0f;
				}
			}
			else
			{
				if (this.ai[0] != 2.1f)
				{
					return;
				}
				if (velocity.X < 0f)
				{
					direction = -1;
				}
				else if (velocity.X > 0f)
				{
					direction = 1;
				}
				spriteDirection = direction;
				velocity *= 1.01f;
				knockBackResist = 0f;
				noTileCollide = true;
				this.ai[1] += 1f;
				int num1449 = 45;
				if (this.ai[1] > (float)num1449)
				{
					if (!Collision.SolidCollision(position, width, height))
					{
						this.ai[0] = 0f;
						this.ai[1] = 0f;
						this.ai[2] = 0f;
					}
					else if (this.ai[1] > (float)(num1449 * 2))
					{
						this.ai[0] = 1f;
						this.ai[1] = 0f;
						this.ai[2] = 0f;
					}
				}
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:15:37.966Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Baby mothron comparison:

- Eclipse off: vanilla EncourageDespawn(5) + vy -= 0.2 clamp -8 + noTileCollide=true. Ours: `e.encourageDespawn(5); e.vy = Math.max(e.vy - 0.2, -8); fly(e);`. Matches.
- Separation: d < w+h → push -0.1. Ours matches (with d===0 guard).
- Target gate: dead → -1 (ours: !p → -1; missing >3000px again like mothron). Note ours also misses the >3000px → -1 case. Same minor.
- State 0: collideX/collideY bounce: ours does moveAndCollide + bounceAxis. Vanilla reads collide flags set during THIS tick's movement? No — collideX/collideY are set during the movement step AFTER AI in vanilla. So vanilla reads last tick's. Ours reads this tick's (moves first). Minor ordering, fine.
  - Wait: in ours, state 0 does `moveAndCollide` then bounceAxis with preVx... then later velocity lerp toward target. Vanilla: bounce (from last tick's collision) then velocity lerp. The net: ours bounces based on current tick collision. OK.
  - d > 800 → 1; d > 200 → speed 5.5 + d/100 + ai1/15, step 40. Ours matches.
  - else >2 → 0.95; <1 → 1.05. Ours matches.
  - ai1 >= 90 → 0 → 2. Ours matches.
- State 1: d<300 && !solid → 0. speed 5.5+ai2+d/150, ai2 += 1/60, step 35. Ours matches (34/35 step: (vx*34+x)/35 = 35-step. Yes).
- State 2: target dy -8, speed 9 step 8; ai1 > 10 → 2.1, velocity = vector262 (normalized*9). Ours matches.
- State 2.1: ×1.01; ai1 > 45: !solid → 0; else if ai1 > 90 → 1. Ours matches.

Note: ours baby mothron state 0 movement: vanilla noTileCollide=false (collision). Ours: moveAndCollide. Good.

Granite elemental: read 40686-40870.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:38.375Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '40686,40872p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla granite elemental AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:38.428Z

**📎 ToolResult**

```
		else if (aiStyle == 91)
		{
			noGravity = true;
			noTileCollide = false;
			dontTakeDamage = false;
			if (justHit && Main.netMode != 1 && Main.expertMode && Main.rand.Next(6) == 0)
			{
				netUpdate = true;
				this.ai[0] = -1f;
				this.ai[1] = 0f;
			}
			if (this.ai[0] == -1f)
			{
				dontTakeDamage = true;
				noGravity = false;
				velocity.X *= 0.98f;
				this.ai[1] += 1f;
				if (this.ai[1] >= 120f)
				{
					this.ai[0] = (this.ai[1] = (this.ai[2] = (this.ai[3] = 0f)));
				}
			}
			else if (this.ai[0] == 0f)
			{
				TargetClosest();
				if (Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[0] = 1f;
					return;
				}
				Vector2 vector263 = Main.player[target].Center - base.Center;
				vector263.Y -= Main.player[target].height / 4;
				float num1450 = vector263.Length();
				Vector2 center47 = base.Center;
				center47.X = Main.player[target].Center.X;
				Vector2 vector264 = center47 - base.Center;
				if (vector264.Length() > 8f && Collision.CanHit(base.Center, 1, 1, center47, 1, 1))
				{
					this.ai[0] = 3f;
					this.ai[1] = center47.X;
					this.ai[2] = center47.Y;
					Vector2 center48 = base.Center;
					center48.Y = Main.player[target].Center.Y;
					if (vector264.Length() > 8f && Collision.CanHit(base.Center, 1, 1, center48, 1, 1) && Collision.CanHit(center48, 1, 1, Main.player[target].position, 1, 1))
					{
						this.ai[0] = 3f;
						this.ai[1] = center48.X;
						this.ai[2] = center48.Y;
					}
				}
				else
				{
					center47 = base.Center;
					center47.Y = Main.player[target].Center.Y;
					if ((center47 - base.Center).Length() > 8f && Collision.CanHit(base.Center, 1, 1, center47, 1, 1))
					{
						this.ai[0] = 3f;
						this.ai[1] = center47.X;
						this.ai[2] = center47.Y;
					}
				}
				if (this.ai[0] == 0f)
				{
					localAI[0] = 0f;
					vector263.Normalize();
					vector263 *= 0.5f;
					velocity += vector263;
					this.ai[0] = 4f;
					this.ai[1] = 0f;
				}
			}
			else if (this.ai[0] == 1f)
			{
				Vector2 vector265 = Main.player[target].Center - base.Center;
				float num1451 = vector265.Length();
				float num1452 = 2f;
				num1452 += num1451 / 200f;
				int num1453 = 50;
				vector265.Normalize();
				vector265 *= num1452;
				velocity = (velocity * (num1453 - 1) + vector265) / num1453;
				if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
				}
			}
			else if (this.ai[0] == 2f)
			{
				noTileCollide = true;
				Vector2 vector266 = Main.player[target].Center - base.Center;
				float num1454 = vector266.Length();
				float num1455 = 2f;
				int num1456 = 4;
				vector266.Normalize();
				vector266 *= num1455;
				velocity = (velocity * (num1456 - 1) + vector266) / num1456;
				if (num1454 < 600f && !Collision.SolidCollision(position, width, height))
				{
					this.ai[0] = 0f;
				}
			}
			else if (this.ai[0] == 3f)
			{
				Vector2 vector267 = new Vector2(this.ai[1], this.ai[2]);
				Vector2 vector268 = vector267 - base.Center;
				float num1457 = vector268.Length();
				float num1458 = 1f;
				float num1459 = 3f;
				vector268.Normalize();
				vector268 *= num1458;
				velocity = (velocity * (num1459 - 1f) + vector268) / num1459;
				if (collideX || collideY)
				{
					this.ai[0] = 4f;
					this.ai[1] = 0f;
				}
				if (num1457 < num1458 || num1457 > 800f || Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[0] = 0f;
				}
			}
			else
			{
				if (this.ai[0] != 4f)
				{
					return;
				}
				if (collideX)
				{
					velocity.X *= -0.8f;
				}
				if (collideY)
				{
					velocity.Y *= -0.8f;
				}
				Vector2 vector269;
				if (velocity.X == 0f && velocity.Y == 0f)
				{
					vector269 = Main.player[target].Center - base.Center;
					vector269.Y -= Main.player[target].height / 4;
					vector269.Normalize();
					velocity = vector269 * 0.1f;
				}
				float num1460 = 1.5f;
				float num1461 = 20f;
				vector269 = velocity;
				vector269.Normalize();
				vector269 *= num1460;
				velocity = (velocity * (num1461 - 1f) + vector269) / num1461;
				this.ai[1] += 1f;
				if (this.ai[1] > 180f)
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
				}
				if (Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[0] = 0f;
				}
				localAI[0] += 1f;
				if (!(localAI[0] >= 5f) || Collision.SolidCollision(position - new Vector2(10f, 10f), width + 20, height + 20))
				{
					return;
				}
				localAI[0] = 0f;
				Vector2 center49 = base.Center;
				center49.X = Main.player[target].Center.X;
				if (Collision.CanHit(base.Center, 1, 1, center49, 1, 1) && Collision.CanHit(base.Center, 1, 1, center49, 1, 1) && Collision.CanHit(Main.player[target].Center, 1, 1, center49, 1, 1))
				{
					this.ai[0] = 3f;
					this.ai[1] = center49.X;
					this.ai[2] = center49.Y;
					return;
				}
				center49 = base.Center;
				center49.Y = Main.player[target].Center.Y;
				if (Collision.CanHit(base.Center, 1, 1, center49, 1, 1) && Collision.CanHit(Main.player[target].Center, 1, 1, center49, 1, 1))
				{
					this.ai[0] = 3f;
					this.ai[1] = center49.X;
					this.ai[2] = center49.Y;
				}
			}
		}
		else if (aiStyle == 92)
		{

```


---

## 🤖 Assistant · 2026-08-19T03:16:03.998Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Granite elemental comparison details:

State 0:
- Vanilla: `vector263 = player.Center - Center; vector263.Y -= player.height/4` (player center Y minus h/4). Ours: `dy = p.cy - p.h / 4 - e.cy`. Matches.
- Column anchor: center47 = Center with X = player.Center.X → vector264 = center47 - Center. Condition: `vector264.Length() > 8 && CanHit(Center, center47)`. Ours: `Math.abs(p.cx - e.cx) > 8 && losClear(e.cx, e.cy, p.cx, e.cy)`. Matches.
- Upgrade: center48 = Center with Y = player.Center.Y; condition `vector264.Length() > 8 && CanHit(Center, center48) && CanHit(center48, player.position)`. Ours: `Math.abs(p.cy - e.cy) > 8 && losClear(e.cx, e.cy, e.cx, p.cy) && losClear(e.cx, p.cy, p.x, p.y)`. Vanilla uses vector264.Length() > 8 (which is the X-distance!) for the row anchor condition — ours uses |p.cy - e.cy| > 8 for the second check but the comment says "原文复用列距 >8 判据". In graniteElementalAI ours: `if (Math.abs(p.cy - e.cy) > 8 && losClear(...))` — this differs from vanilla which reuses `vector264.Length() > 8` (X distance). Hmm wait, in vanilla the row-anchor branch is in the ELSE of the column-anchor: else → center47 = Center; center47.Y = player.Center.Y; if ((center47 - Center).Length() > 8 && CanHit(Center, center47)). Note here it's `(center47 - Center).Length()` = |dy| — that's the Y distance. OK so else-branch uses Y distance. And the upgrade inside the if-branch uses vector264.Length() (X distance, likely a vanilla bug/quirk). In graniteElemental ours, the upgrade check is `Math.abs(p.cy - e.cy) > 8` — vanilla uses vector264.Length() (X). So ours deviates from vanilla's quirky reuse of the X-distance in the upgrade check. This is a 1:1 fidelity nuance — vanilla's quirk means the double-anchor upgrade only happens when the player is >8px away horizontally (already guaranteed by the outer if) — i.e., the inner condition is ALWAYS true when reached! So effectively the upgrade happens whenever CanHit conditions pass, regardless of Y distance. Ours adds a |dy|>8 requirement that vanilla (buggily) doesn't have. Impact: occasionally ours stays with column anchor where vanilla would upgrade to row anchor. Very minor.

BUT NOTE: starCellAI (aiStyle 85, :38987-39008) has the same structure — there ours DOES copy the quirk (`if (Math.abs(p.cx - e.cx) > 8 && ...)` reused twice) per its comment "原文复用列距 >8 判据——按原文照抄". So starCell copies the quirk but granite doesn't. Inconsistent but each individually tiny.

State 1: speed 2 + d/200, step 50; exit on !CanHit. Ours matches.

State 2: noTileCollide=true (ours uses fly()), speed 2 step 4; d < 600 && !SolidCollision → 0. Ours matches.

State 3: speed 1 step 3; collideX||collideY → 4; d < 1 || d > 800 || CanHit → 0. Ours: `if (e.hitWall || e.hitHead || (e.onGround && preVy > 0)) → 4`. Vanilla: collideX || collideY. collideY includes landing AND hitting head. Ours approximates collideY as hitHead || (onGround && falling). onGround requires vy==0 post-move typically. OK approximation. `d < 1` — ours `d < 1`. Vanilla `num1457 < num1458` (1). Matches.

Hmm wait — one important thing in state 3: ours applies moveAndCollide... but before that: ours computes velocity THEN moveAndCollide. Vanilla: velocity set, movement by shared code. OK.

State 4: 
- bounce: collideX → vx *= -0.8; collideY → vy *= -0.8. Ours: `if (e.hitWall) e.vx *= -0.8; if (e.hitHead || e.onGround) e.vy *= -0.8;`. OK.
- zero velocity → direction toward player (Y - h/4) *0.1. Ours matches.
- speed 1.5 step 20. Ours matches.
- ai1 > 180 → 0; CanHit → 0. Ours matches (ours checks `e.ai1 > 180 || los`).
- Retry anchor every 5t (inflated 10 solid check): column anchor needs CanHit(Center→center49) ×2 && CanHit(player.Center→center49). Ours: `losClear(e.cx,e.cy,p.cx,e.cy) && losClear(e.cx,e.cy,p.cx,e.cy) && losClear(p.cx,p.cy,p.cx,e.cy)`. Wait — center49 = Center with X = player.Center.X → center49 = (p.cx, e.cy). CanHit(Center, center49) = losClear(e.cx,e.cy, p.cx, e.cy). Duplicated in vanilla. Ours: losClear(e.cx, e.cy, p.cx, e.cy) twice + losClear(p.cx, p.cy, p.cx, e.cy). Matches (3 checks; center49.Y = e.cy). Good.
- Row anchor: center49 = Center with Y = player.Center.Y = (e.cx, p.cy). CanHit(Center, center49) && CanHit(player.Center, center49) → losClear(e.cx,e.cy,e.cx,p.cy) && losClear(p.cx,p.cy,e.cx,p.cy). Ours matches.

State -1 (expert petrify): unreachable. Ours sets noGravity = ai0 !== -1 — vanilla -1 sets noGravity=false; others noGravity=true at top. Match.

Now — IMPORTANT: in state -1, vanilla applies... velocity.X *= 0.98 only; gravity comes from shared code since noGravity=false. Ours: `moveAndCollide(e, game.world, e.vx, e.vy)` without adding gravity! In vanilla noGravity=false → shared gravity applies → falls. Ours: no gravity added in -1 state → floats. But -1 is expert-only (EXPERT=false) → unreachable. Skip.

Also: in state -1 ours calls moveAndCollide without gravity — fine given unreachable.

Now starCell (aiStyle 85) 38967-39220. Read vanilla.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:04.451Z · glm-x-preview-260804

```
已检查花岗岩元素，无问题。现在处理星细胞家族 (38967-39220)。
```


---

## 🤖 Assistant · 2026-08-19T03:16:04.890Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '38967,39130p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla star cell AI part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:04.944Z

**📎 ToolResult**

```
		else if (aiStyle == 85)
		{
			noTileCollide = false;
			if (this.ai[0] == 0f)
			{
				TargetClosest();
				if (Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[0] = 1f;
				}
				else
				{
					Vector2 vector234 = Main.player[target].Center - base.Center;
					vector234.Y -= Main.player[target].height / 4;
					float num1366 = vector234.Length();
					if (num1366 > 800f)
					{
						this.ai[0] = 2f;
					}
					else
					{
						Vector2 center42 = base.Center;
						center42.X = Main.player[target].Center.X;
						Vector2 vector235 = center42 - base.Center;
						if (vector235.Length() > 8f && Collision.CanHit(base.Center, 1, 1, center42, 1, 1))
						{
							this.ai[0] = 3f;
							this.ai[1] = center42.X;
							this.ai[2] = center42.Y;
							Vector2 center43 = base.Center;
							center43.Y = Main.player[target].Center.Y;
							if (vector235.Length() > 8f && Collision.CanHit(base.Center, 1, 1, center43, 1, 1) && Collision.CanHit(center43, 1, 1, Main.player[target].position, 1, 1))
							{
								this.ai[0] = 3f;
								this.ai[1] = center43.X;
								this.ai[2] = center43.Y;
							}
						}
						else
						{
							center42 = base.Center;
							center42.Y = Main.player[target].Center.Y;
							if ((center42 - base.Center).Length() > 8f && Collision.CanHit(base.Center, 1, 1, center42, 1, 1))
							{
								this.ai[0] = 3f;
								this.ai[1] = center42.X;
								this.ai[2] = center42.Y;
							}
						}
						if (this.ai[0] == 0f)
						{
							localAI[0] = 0f;
							vector234.Normalize();
							vector234 *= 0.5f;
							velocity += vector234;
							this.ai[0] = 4f;
							this.ai[1] = 0f;
						}
					}
				}
			}
			else if (this.ai[0] == 1f)
			{
				rotation += (float)direction * 0.3f;
				Vector2 vector236 = Main.player[target].Center - base.Center;
				if (type == 421)
				{
					vector236 = Main.player[target].Top - base.Center;
				}
				float num1367 = vector236.Length();
				float num1368 = 5.5f;
				if (type == 405)
				{
					num1368 = 8f;
				}
				num1368 += num1367 / 100f;
				int num1369 = 50;
				vector236.Normalize();
				vector236 *= num1368;
				velocity = (velocity * (num1369 - 1) + vector236) / num1369;
				if (!Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
				}
				if (type == 421 && num1367 < 40f && Main.player[target].active && !Main.player[target].dead)
				{
					bool flag94 = true;
					for (int num1370 = 0; num1370 < Main.maxNPCs; num1370++)
					{
						NPC nPC11 = Main.npc[num1370];
						if (nPC11.active && nPC11.type == type && nPC11.ai[0] == 5f && nPC11.target == target)
						{
							flag94 = false;
							break;
						}
					}
					if (flag94)
					{
						base.Center = Main.player[target].Top;
						velocity = Vector2.Zero;
						this.ai[0] = 5f;
						this.ai[1] = 0f;
						netUpdate = true;
					}
				}
			}
			else if (this.ai[0] == 2f)
			{
				rotation = velocity.X * 0.1f;
				noTileCollide = true;
				Vector2 vector237 = Main.player[target].Center - base.Center;
				float num1371 = vector237.Length();
				float num1372 = 3f;
				if (type == 405)
				{
					num1372 = 6f;
				}
				int num1373 = 3;
				vector237.Normalize();
				vector237 *= num1372;
				velocity = (velocity * (num1373 - 1) + vector237) / num1373;
				if (num1371 < 600f && !Collision.SolidCollision(position, width, height))
				{
					this.ai[0] = 0f;
				}
			}
			else if (this.ai[0] == 3f)
			{
				rotation = velocity.X * 0.1f;
				Vector2 vector238 = new Vector2(this.ai[1], this.ai[2]);
				Vector2 vector239 = vector238 - base.Center;
				float num1374 = vector239.Length();
				float num1375 = 2f;
				if (type == 405)
				{
					num1375 = 3f;
				}
				float num1376 = 3f;
				vector239.Normalize();
				vector239 *= num1375;
				velocity = (velocity * (num1376 - 1f) + vector239) / num1376;
				if (collideX || collideY)
				{
					this.ai[0] = 4f;
					this.ai[1] = 0f;
				}
				if (num1374 < num1375 || num1374 > 800f || Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[0] = 0f;
				}
			}
			else if (this.ai[0] == 4f)
			{
				rotation = velocity.X * 0.1f;
				if (collideX)
				{
					velocity.X *= -0.8f;
				}
				if (collideY)
				{
					velocity.Y *= -0.8f;
				}
				Vector2 vector240;

```


---

## 🤖 Assistant · 2026-08-19T03:16:08.239Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '39130,39260p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla star cell AI part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:08.296Z

**📎 ToolResult**

```
				Vector2 vector240;
				if (velocity.X == 0f && velocity.Y == 0f)
				{
					vector240 = Main.player[target].Center - base.Center;
					vector240.Y -= Main.player[target].height / 4;
					vector240.Normalize();
					velocity = vector240 * 0.1f;
				}
				float num1377 = 2f;
				if (type == 405)
				{
					num1377 = 3f;
				}
				float num1378 = 20f;
				vector240 = velocity;
				vector240.Normalize();
				vector240 *= num1377;
				velocity = (velocity * (num1378 - 1f) + vector240) / num1378;
				this.ai[1] += 1f;
				if (this.ai[1] > 180f)
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
				}
				if (Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
				{
					this.ai[0] = 0f;
				}
				localAI[0] += 1f;
				if (localAI[0] >= 5f && !Collision.SolidCollision(position - new Vector2(10f, 10f), width + 20, height + 20))
				{
					localAI[0] = 0f;
					Vector2 center44 = base.Center;
					center44.X = Main.player[target].Center.X;
					if (Collision.CanHit(base.Center, 1, 1, center44, 1, 1) && Collision.CanHit(base.Center, 1, 1, center44, 1, 1) && Collision.CanHit(Main.player[target].Center, 1, 1, center44, 1, 1))
					{
						this.ai[0] = 3f;
						this.ai[1] = center44.X;
						this.ai[2] = center44.Y;
					}
					else
					{
						center44 = base.Center;
						center44.Y = Main.player[target].Center.Y;
						if (Collision.CanHit(base.Center, 1, 1, center44, 1, 1) && Collision.CanHit(Main.player[target].Center, 1, 1, center44, 1, 1))
						{
							this.ai[0] = 3f;
							this.ai[1] = center44.X;
							this.ai[2] = center44.Y;
						}
					}
				}
			}
			else if (this.ai[0] == 5f)
			{
				Player player16 = Main.player[target];
				if (!player16.active || player16.dead)
				{
					this.ai[0] = 0f;
					this.ai[1] = 0f;
					netUpdate = true;
				}
				else
				{
					base.Center = ((player16.gravDir == 1f) ? player16.Top : player16.Bottom) + new Vector2(player16.direction * 4, 0f);
					gfxOffY = player16.gfxOffY;
					velocity = Vector2.Zero;
					if (!player16.creativeGodMode)
					{
						player16.AddBuff(163, 59);
					}
				}
			}
			if (type == 405)
			{
				rotation = 0f;
				for (int num1379 = 0; num1379 < Main.maxNPCs; num1379++)
				{
					if (num1379 != whoAmI && Main.npc[num1379].active && Main.npc[num1379].type == type && Math.Abs(position.X - Main.npc[num1379].position.X) + Math.Abs(position.Y - Main.npc[num1379].position.Y) < (float)width)
					{
						if (position.X < Main.npc[num1379].position.X)
						{
							velocity.X -= 0.05f;
						}
						else
						{
							velocity.X += 0.05f;
						}
						if (position.Y < Main.npc[num1379].position.Y)
						{
							velocity.Y -= 0.05f;
						}
						else
						{
							velocity.Y += 0.05f;
						}
					}
				}
			}
			else
			{
				if (type != 421)
				{
					return;
				}
				hide = this.ai[0] == 5f;
				rotation = velocity.X * 0.1f;
				for (int num1380 = 0; num1380 < Main.maxNPCs; num1380++)
				{
					if (num1380 != whoAmI && Main.npc[num1380].active && Main.npc[num1380].type == type && Math.Abs(position.X - Main.npc[num1380].position.X) + Math.Abs(position.Y - Main.npc[num1380].position.Y) < (float)width)
					{
						if (position.X < Main.npc[num1380].position.X)
						{
							velocity.X -= 0.05f;
						}
						else
						{
							velocity.X += 0.05f;
						}
						if (position.Y < Main.npc[num1380].position.Y)
						{
							velocity.Y -= 0.05f;
						}
						else
						{
							velocity.Y += 0.05f;
						}
					}
				}
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:16:27.779Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Star cell comparison:

State 5 (421 latch): vanilla Center = (gravDir==1 ? player.Top : player.Bottom) + (direction*4, 0); gfxOffY; velocity zero; AddBuff(163, 59) unless creativeGodMode. Ours: `e.x = p.cx + dir*4 - e.w/2; e.y = p.y - e.h/2;` — hmm: Center = player.Top + (dir*4, 0) → x = p.cx + dir*4 - w/2; y = p.y - h/2. Player.Top = (x, y). So Center.Y = p.y → e.y = p.y - e.h/2. Ours matches (gravDir inverted case not handled — gravity inversion not in scope). Ours applies buff with 59/60 seconds. Vanilla 59 frames. OK.

Wait — ours in state 1: `if (is421 && d < 40 && !enemies...some(o => ... ai0 === 5))` — vanilla checks `nPC11.target == target` too (same target). Ours only checks ai0===5 without target match — single-player, fine.

Vanilla state-1 421 also: `base.Center = Main.player[target].Top` — Top = position.Y (top), so Center = (p.cx, p.y). Ours: `e.x = p.cx - e.w / 2; e.y = p.y - e.h;` — WAIT. Center.Y = Top.Y means e.y (top of NPC) = p.y - e.h/2. Ours sets `e.y = p.y - e.h` — that puts the NPC's BOTTOM at player top... hmm actually `e.y = p.y - e.h` → e.cy = p.y - e.h/2. Vanilla Center = player.Top = (p.cx, p.y) → e.cy = p.y → e.y = p.y - e.h/2. So ours is h/2 too high. Hmm — for a 421 with h=18ish: 9px offset. Minor visual. Actually wait, let me reconsider: vanilla `base.Center = Main.player[target].Top`. Player.Top property = (position.X + width/2, position.Y) → Y = p.y (top of player hitbox). So the head-crab's center sits at the player's top edge — i.e., half the crab is above the player's head. Ours: e.y = p.y - e.h → center at p.y - e.h/2 → crab fully above the player's head. 9px difference for h=18. Minor.

Also state 5 has `hide = ai[0]==5` — ours keeps visible, registered deviation in comment ("保持可见为已登记偏差"). OK disclosed.

Star cell state 0: distance gate num1366 > 800 → state 2. Ours matches. Anchors match (with quirk copied). State 1: rotation += direction*0.3 for non-421? Actually `rotation += (float)direction * 0.3f;` in state 1 applies to all (before type check). Then for 405 at end: rotation = 0. For 421: rotation = velocity.X*0.1. So the state-1 rotation += dir*0.3 gets overwritten at the end for both 405 and 421. Whatever — ours handles via starCellTail (visAngle). Fine.

State 2: noTileCollide=true, speed 3|6, step 3, <600 && !solid → 0. Ours matches. Ours rotation: for state 2 vanilla rotation = velocity.X*0.1 — but overwritten by tail (405→0, 421→vx*0.1). Our starCellTail handles. OK.

State 3: speed 2|3, step 3, collide → 4, d<spd || d>800 || CanHit → 0. Ours: `if (d < spd || d > 800 || los) e.ai0 = 0;`. Vanilla: `num1374 < num1375` where num1375 = 2|3 (the speed). Ours uses spd var = 2|3. Matches.

State 4: bounce, drift speed 2|3 step 20, ai1 > 180 → 0, CanHit → 0, retry anchor every 5t with inflate 10. Ours matches.

Now smallStarCell (41445-41492), flowInvader (41493-41535), nebulaFloater (41536-41750), solarSlime (41997-42056). Read them.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:28.386Z · glm-x-preview-260804

```
星形细胞匹配。现在处理小星形细胞、流动入侵者、星云漂浮者和太阳能史莱姆 (41445-42056)。
```


---

## 🤖 Assistant · 2026-08-19T03:16:28.866Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '41445,41560p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla small star cell and flow invader AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:28.926Z

**📎 ToolResult**

```
		else if (aiStyle == 95)
		{
			float num1505 = 300f;
			if (velocity.Length() > 4f)
			{
				velocity *= 0.95f;
			}
			velocity *= 0.99f;
			this.ai[0]++;
			float num1506 = MathHelper.Clamp(this.ai[0] / num1505, 0f, 1f);
			scale = 1f + 0.3f * num1506;
			if (this.ai[0] >= num1505)
			{
				if (Main.netMode != 1)
				{
					Transform(405);
				}
				return;
			}
			rotation += velocity.X * 0.1f;
			if (!(this.ai[0] > 20f))
			{
				return;
			}
			Vector2 center50 = base.Center;
			int num1507 = (int)(this.ai[0] / (num1505 / 2f));
			for (int num1508 = 0; num1508 < num1507 + 1; num1508++)
			{
				if (Main.rand.Next(2) != 0)
				{
					int num1509 = 226;
					float num1510 = 0.4f;
					if (num1508 % 2 == 1)
					{
						num1509 = 226;
						num1510 = 0.65f;
					}
					Vector2 vector276 = center50 + ((float)Main.rand.NextDouble() * (MathF.PI * 2f)).ToRotationVector2() * (12f - (float)(num1507 * 2));
					int num1511 = Dust.NewDust(vector276 - Vector2.One * 12f, 24, 24, num1509, velocity.X / 2f, velocity.Y / 2f);
					Dust dust = Main.dust[num1511];
					dust.position -= new Vector2(2f);
					Main.dust[num1511].velocity = Vector2.Normalize(center50 - vector276) * 1.5f * (10f - (float)num1507 * 2f) / 10f;
					Main.dust[num1511].noGravity = true;
					Main.dust[num1511].scale = num1510;
					Main.dust[num1511].customData = this;
				}
			}
		}
		else if (aiStyle == 96)
		{
			float num1512 = 5f;
			float moveSpeed = 0.15f;
			TargetClosest();
			Vector2 desiredVelocity3 = Main.player[target].Center - base.Center + new Vector2(0f, -250f);
			float num1513 = desiredVelocity3.Length();
			if (num1513 < 20f)
			{
				desiredVelocity3 = velocity;
			}
			else if (num1513 < 40f)
			{
				desiredVelocity3.Normalize();
				desiredVelocity3 *= num1512 * 0.35f;
			}
			else if (num1513 < 80f)
			{
				desiredVelocity3.Normalize();
				desiredVelocity3 *= num1512 * 0.65f;
			}
			else
			{
				desiredVelocity3.Normalize();
				desiredVelocity3 *= num1512;
			}
			SimpleFlyMovement(desiredVelocity3, moveSpeed);
			rotation = velocity.X * 0.1f;
			if (!((this.ai[0] += 1f) >= 70f))
			{
				return;
			}
			this.ai[0] = 0f;
			if (Main.netMode != 1)
			{
				Vector2 vector277 = Vector2.Zero;
				while (Math.Abs(vector277.X) < 1.5f)
				{
					vector277 = Vector2.UnitY.RotatedByRandom(1.5707963705062866) * new Vector2(5f, 3f);
				}
				Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector277.X, vector277.Y, 539, 60, 0f, Main.myPlayer, 0f, whoAmI);
			}
		}
		else if (aiStyle == 97)
		{
			float num1514 = 7f;
			int num1515 = 480;
			int num1516 = 30;
			int maxValue6 = 6;
			if (localAI[2] < 180f)
			{
				localAI[2]++;
				if (Main.netMode != 1 && localAI[2] % 60f == 0f)
				{
					Vector2 vector278 = Vector2.Zero;
					while (Math.Abs(vector278.X) < 1.5f)
					{
						vector278 = Vector2.UnitY.RotatedByRandom(1.5707963705062866) * new Vector2(4f, 2.5f);
					}
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector278.X, vector278.Y, 574, 0, 0f, Main.myPlayer, 0f, whoAmI);
				}
			}
			if (localAI[1] == 1f)
			{
				localAI[1] = 0f;
				if (Main.rand.Next(maxValue6) == 0)
				{
					this.ai[0] = num1515;

```


---

## 🤖 Assistant · 2026-08-19T03:16:35.810Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Small star cell: ours matches (dust approximated). One thing: ours `e.vanillaScale = 1 + 0.3 * clamp(...)` and transform at MAX. Vanilla: transform when ai0 >= 300 (returns). Ours: transformTo + return. Also vanilla applies gravity? NPC 406 has noGravity? SetDefaults for 406... The ours calls moveAndCollide without adding gravity. Vanilla NPC 406: noGravity = true presumably (it drifts). Let me trust.

Flow invader: matches — SimpleFlyMovement(desired, moveSpeed 0.15) = velocity += Clamp(desired - velocity, -0.15, 0.15)?? Actually SimpleFlyMovement in vanilla: velocity.X += Clamp(desiredVelocity.X - velocity.X, -moveSpeed, moveSpeed)? Let me recall: `private void SimpleFlyMovement(Vector2 desiredVelocity, float moveSpeed)` { velocity.X += MathHelper.Clamp(desiredVelocity.X - velocity.X, -moveSpeed, moveSpeed); velocity.Y += ... }. Ours matches.

539 throw: `Vector2.UnitY.RotatedByRandom(π/2) * (5,3)` re-roll |vx|>=1.5. Ours matches. damage 60. Ours passes 60 to LunarOrb (dmg for explosion). OK.

Nebula floater: continue reading 41560-41750.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:36.210Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '41560,41750p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla nebula floater AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:36.280Z

**📎 ToolResult**

```
					this.ai[0] = num1515;
				}
			}
			TargetClosest();
			if (Main.netMode != 1 && (!Main.player[target].active || Main.player[target].dead))
			{
				this.ai[0] = 0f;
				this.ai[1] = 1f;
				this.ai[2] = 0f;
				this.ai[3] = 0f;
				netUpdate = true;
			}
			rotation = Math.Abs(velocity.X) * (float)direction * 0.1f;
			spriteDirection = -direction;
			Vector2 vector279 = base.Center + new Vector2(direction * 20, 6f);
			Vector2 vector280 = Main.player[target].Center - vector279;
			bool flag103 = Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1);
			bool flag104 = false;
			if (this.ai[1] == 1f)
			{
				if (localAI[3] == 0f)
				{
					localAI[3] = 1f;
					this.ai[3] = 3f;
					SoundEngine.PlaySound(SoundID.Item8, base.Center);
					for (int num1517 = 0; num1517 < 20; num1517++)
					{
						int num1518 = Dust.NewDust(position, width, height, 242);
						Dust dust = Main.dust[num1518];
						dust.velocity *= 3f;
						Main.dust[num1518].noGravity = true;
						Main.dust[num1518].scale = 2.5f;
					}
				}
				this.ai[3]--;
				if (this.ai[3] <= 0f)
				{
					active = false;
					netUpdate = true;
				}
				return;
			}
			if (vector280.Length() > 400f || !flag103)
			{
				Vector2 vector281 = vector280;
				if (vector281.Length() > num1514)
				{
					vector281.Normalize();
					vector281 *= num1514;
				}
				int num1519 = 30;
				velocity = (velocity * (num1519 - 1) + vector281) / num1519;
			}
			else
			{
				velocity *= 0.98f;
				flag104 = true;
			}
			if (this.ai[2] != 0f && this.ai[3] != 0f)
			{
				SoundEngine.PlaySound(SoundID.Item8, base.Center);
				for (int num1520 = 0; num1520 < 20; num1520++)
				{
					int num1521 = Dust.NewDust(position, width, height, 242);
					Dust dust = Main.dust[num1521];
					dust.velocity *= 3f;
					Main.dust[num1521].noGravity = true;
					Main.dust[num1521].scale = 2.5f;
				}
				base.Center = new Vector2(this.ai[2] * 16f, this.ai[3] * 16f);
				velocity = Vector2.Zero;
				this.ai[2] = 0f;
				this.ai[3] = 0f;
				SoundEngine.PlaySound(SoundID.Item8, base.Center);
				for (int num1522 = 0; num1522 < 20; num1522++)
				{
					int num1523 = Dust.NewDust(position, width, height, 242);
					Dust dust = Main.dust[num1523];
					dust.velocity *= 3f;
					Main.dust[num1523].noGravity = true;
					Main.dust[num1523].scale = 2.5f;
				}
			}
			this.ai[0]++;
			if (this.ai[0] >= (float)num1515 && Main.netMode != 1)
			{
				this.ai[0] = 0f;
				Point point12 = base.Center.ToTileCoordinates();
				Point point13 = Main.player[target].Center.ToTileCoordinates();
				Vector2 chosenTile = Vector2.Zero;
				if (AI_AttemptToFindTeleportSpot(ref chosenTile, point13.X, point13.Y, 20, 12, 1, solidTileCheckCentered: true, teleportInAir: true))
				{
					this.ai[1] = 20f;
					this.ai[2] = chosenTile.X;
					this.ai[3] = chosenTile.Y;
					bool flag105 = true;
					for (int num1524 = 0; num1524 < 1000; num1524++)
					{
						Projectile projectile10 = Main.projectile[num1524];
						if (projectile10.active && projectile10.type == 574 && projectile10.ai[1] == (float)whoAmI && !(projectile10.ai[0] >= 0f))
						{
							flag105 = false;
							break;
						}
					}
					if (flag105)
					{
						for (int num1525 = 0; num1525 < 1000; num1525++)
						{
							Projectile projectile11 = Main.projectile[num1525];
							if (projectile11.active && projectile11.type == 574 && projectile11.ai[1] == (float)whoAmI)
							{
								projectile11.ai[0] -= num1516;
							}
						}
					}
				}
				netUpdate = true;
			}
			if (flag104 && velocity.Length() < 2f && Main.netMode != 1)
			{
				localAI[0] += 1f;
				_ = localAI[0];
				_ = 13f;
			}
		}
		else if (aiStyle == 98)
		{
			noTileCollide = false;
			if (this.ai[0] == 0f)
			{
				TargetClosest();
				this.ai[0] = 1f;
				this.ai[1] = 0f;
				this.ai[2] = 0f;
				this.ai[3] = 0f;
			}
			bool flag106 = Collision.CanHit(base.Center, 1, 1, Main.player[target].position, 1, 1);
			bool flag107 = true;
			if (!flag106 || Main.player[target].dead)
			{
				flag107 = false;
			}
			else
			{
				int num1526 = (int)(Main.player[target].Center.X / 16f);
				int num1527 = (int)(Main.player[target].Center.Y / 16f);
				for (int num1528 = num1526 - 2; num1528 <= num1526 + 2; num1528++)
				{
					for (int num1529 = num1527; num1529 <= num1527 + 25; num1529++)
					{
						if (WorldGen.SolidTile2(num1528, num1529))
						{
							flag107 = false;
						}
					}
				}
			}
			if (this.ai[0] < 0f)
			{
				Vector2 vector282 = Main.player[target].Center - base.Center;
				float num1530 = vector282.Length();
				if (this.ai[0] == -1f)
				{
					vector282.Normalize();
					if (vector282.HasNaNs())
					{
						vector282 = new Vector2(direction, 0f);
					}
					float num1531 = 8f + num1530 / 100f;
					float num1532 = 12f;
					if (Main.player[target].velocity.Length() > num1532)
					{
						num1532 = Main.player[target].velocity.Length();
					}
					if (num1531 > num1532)
					{
						num1531 = num1532;
					}
					vector282 *= num1531;
					float num1533 = 10f;
					velocity = (velocity * (num1533 - 1f) + vector282) / num1533;
					for (int num1534 = 0; num1534 < Main.maxNPCs; num1534++)
					{
						if (Main.npc[num1534].active && Main.npc[num1534].type == type && num1534 != whoAmI)
						{
							Vector2 vector283 = Main.npc[num1534].Center - base.Center;
							if (vector283.Length() < 40f)
							{
								vector283.Normalize();
								vector283 *= 1f;

```


---

## 🤖 Assistant · 2026-08-19T03:17:02.422Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Nebula floater comparison:

Vanilla order:
1. Opening orbs: localAI[2] < 180, every 60 → orb 574. Ours matches.
2. justHit → localAI[1] (set in StrikeNPC) — vanilla checks `localAI[1] == 1f` → reset to 0, 1/6 → ai[0] = 480. Ours matches.
3. TargetClosest; if player dead/inactive → ai = [0, 1, 0, 0]. Ours: `if (!p) { e.ai0 = 0; e.ai1 = 1; ... }`. Matches.
4. rotation = |vx| * direction * 0.1; spriteDirection = -direction. Ours matches.
5. vector279 = Center + (direction*20, 6); vector280 = player.Center - vector279. flag103 = CanHit(Center, player). Ours: ax = e.cx + dir*20, ay = e.cy + 6; tdx = p.cx - ax... los = losClear(e.cx, e.cy, p.cx, p.cy). Matches.
6. If ai[1] == 1 → dissolve: localAI[3]==0 → =1, ai[3] = 3, Item8 + 20 dust; ai[3]--; ai[3] <= 0 → active=false. Ours matches (dead = true).
   NOTE: vanilla's dissolve segment is BEFORE flag103 computed? Order in vanilla: rotation/spriteDirection, vector279/280, flag103, flag104, then `if (ai[1] == 1f) {...return}`. Ours places the dissolve check after computing dir/visAngle/facing, before los. Same semantics.
7. Chase: `if (vector280.Length() > 400 || !flag103)` — distance measured from the OFFSET aim point (Center + (dir*20, 6)). Ours uses td = hypot(tdx, tdy) — same offset. speed 7 clamp, step 30. Matches.
8. Else velocity *= 0.98 (hover). Ours matches.
9. Teleport execution: ai[2] != 0 && ai[3] != 0 → Item8 + dust, Center = (ai2*16, ai3*16), zero velocity, clear, Item8 + dust again. Ours matches.
   Order note: vanilla does teleport execution AFTER movement assignment (chase), and BEFORE ai[0]++. Ours: after hover/chase, then teleport block, then ai0 += 1. Matches.
10. Teleport period: ai[0]++ (after execution), if ai[0] >= 480 → 0; find spot; if found: ai[1] = 20, ai[2]/ai[3] = tile. Then flag105: scan projectiles for 574 with ai[1] == whoAmI && !(ai[0] >= 0) — i.e., aborts if ANY orb has ai[0] < 0 (charging state). If flag105 (no negative-orb), subtract 30 from all orbs' ai[0].
    Ours: comment says "原文 flag105 门 ai[0]<0 恒假 → 恒全量" — hmm. Vanilla's 574 projectile ai[0]: what values does it take? In Projectile AI_102 for 574: ai[0] is the orbit timer... Let me think. Vanilla 574 orbit timer counts up; ours LunarOrb uses ai0 counting 0→180 then fires 576 and resets to 0. When does vanilla's 574 ai[0] go negative? In Projectile.NewProjectile for 574: ai[0] = 0 initial. Hmm — the check `!(projectile10.ai[0] >= 0f)` = ai[0] < 0 → abort. If vanilla 574's ai[0] never goes negative, flag105 stays true and all orbs get -30. Ours always applies -30 (delay). Matches vanilla IF ai0 never < 0 for 574. Let me check Projectile.cs AI_102 for 574 to see if ai[0] can go negative. In vanilla AI_102 (:32040+), for type 574: ai[0] increments...; the accelerate call subtracts 30 (ai[0] -= 30). If teleported twice in quick succession or orb young... e.g., orb spawned at localAI[2]=120 (second orb), floater teleports at 480: orb's ai[0] might be 360-30=330 etc. Always positive. When firing 576: ai[0] = 0 reset. So ai[0] >= 0 always... unless delay(30) subtracted when ai0 < 30 → negative! E.g., orb just fired (ai0=0), teleport happens next tick → ai0 = -30 → negative → flag105 false on the NEXT teleport. So vanilla's gate isn't dead. But ours' `delay(30)` can also produce negative ai0 in our LunarOrb. Then next teleport: ours still applies delay unconditionally (can double-delay). Effect: orbs fire 576 sooner/more often than vanilla after multiple teleports with young orbs. Marginal. But note ours claims "恒假" — the claim is wrong in the edge case. Low priority.

    Actually wait — ours also replicates "ai[0] -= 30" via delay() which is what vanilla does when flag105. Vanilla skips the subtraction if any orb has ai[0] < 0. Ours never skips. So deviation only when an orb's ai0 < 30 at teleport time. Rare-ish. Low.

11. flag104 && velocity.Length() < 2 → localAI[0]++ (unused). Ours matches.

One more vanilla bit: TargetClosest() sets direction via `direction = ...`? TargetClosest(updates: direction). And "TargetClosest(confused 反向)" comment in ours. Ours: `const dir = p ? e.seekDirX(p) : e.facing`. OK.

Now solarSlime (41997-42056).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:03.071Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '41997,42060p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla solar slime AI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:03.123Z

**📎 ToolResult**

```
		else if (aiStyle == 99)
		{
			if (velocity.Y == 0f && this.ai[0] == 0f)
			{
				this.ai[0] = 1f;
				this.ai[1] = 0f;
				netUpdate = true;
				return;
			}
			if (this.ai[0] == 1f)
			{
				velocity = Vector2.Zero;
				position = oldPosition;
				this.ai[1]++;
				if (this.ai[1] >= 5f)
				{
					HitEffect(0, 9999.0);
					active = false;
				}
				return;
			}
			velocity.Y += 0.2f;
			if (velocity.Y > 12f)
			{
				velocity.Y = 12f;
			}
			rotation = velocity.ToRotation() - MathF.PI / 2f;
			if (type != 519)
			{
				return;
			}
			if (localAI[0] == 0f)
			{
				localAI[0] = 1f;
				for (int num1554 = 0; num1554 < 13; num1554++)
				{
					int num1555 = Dust.NewDust(position, width, height, 6, velocity.X * 0.5f, velocity.Y * 0.5f, 90, default(Color), 2.5f);
					Main.dust[num1555].noGravity = true;
					Main.dust[num1555].fadeIn = 1f;
					Dust dust = Main.dust[num1555];
					dust.velocity *= 4f;
					Main.dust[num1555].noLight = true;
				}
			}
			for (int num1556 = 0; num1556 < 3; num1556++)
			{
				if (Main.rand.Next(3) < 2)
				{
					int num1557 = Dust.NewDust(position, width, height, 6, velocity.X * 0.5f, velocity.Y * 0.5f, 90, default(Color), 2.5f);
					Main.dust[num1557].noGravity = true;
					Dust dust = Main.dust[num1557];
					dust.velocity *= 0.2f;
					Main.dust[num1557].fadeIn = 1f;
					if (Main.rand.Next(6) == 0)
					{
						dust = Main.dust[num1557];
						dust.velocity *= 30f;
						Main.dust[num1557].noGravity = false;
						Main.dust[num1557].noLight = true;
					}
					else
					{
						Main.dust[num1557].velocity = DirectionFrom(Main.dust[num1557].position) * Main.dust[num1557].velocity.Length();
					}

```


---

## 🤖 Assistant · 2026-08-19T03:17:09.724Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Solar slime: ours matches structurally (vy += 0.2 cap 12, rotation, ai0 gate vy==0&&ai0==0 → 1, state 1 freeze 5 ticks → dead). Dust approximated. 

Hmm, one thing: ours uses `e.vy === 0 && e.ai0 === 0` gate. In our engine, is vy reset to 0 on landing by moveAndCollide? Typically yes. OK.

Now the big one: crawltipede (412) at aiStyle 6, 51357-52671. That's a huge section (1300 lines) — the 412-specific segment is said to be at :51764-52671 region. Let me read strategically: 51740-51900 (chain build + segment integrity), then 52020-52070 (414 flash + head dust), then 52170-52330 (target override), then 52390-52410 (want velocity), 52500-52610 (steering), 52600 (rotation), 52260-52325 (segment follow).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:10.401Z · glm-x-preview-260804

```
已检查太阳能史莱姆，情况良好。现在是 crawltipede ——正在读取 AI_006 的 412 特定分段。
```


---

## 🤖 Assistant · 2026-08-19T03:17:11.022Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '51740,51870p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla crawltipede chain build segment"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:11.072Z

**📎 ToolResult**

```
						ai[2] *= 2f;
					}
					ai[0] = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)(position.X + (float)(width / 2)), (int)(position.Y + (float)height), type + 1, whoAmI);
					Main.npc[(int)ai[0]].CopyInteractions(this);
				}
				else if ((type == 8 || type == 11 || type == 14 || type == 40 || type == 96 || type == 99 || type == 118) && ai[2] > 0f)
				{
					ai[0] = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)(position.X + (float)(width / 2)), (int)(position.Y + (float)height), type, whoAmI);
					Main.npc[(int)ai[0]].CopyInteractions(this);
				}
				else
				{
					ai[0] = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)(position.X + (float)(width / 2)), (int)(position.Y + (float)height), type + 1, whoAmI);
					Main.npc[(int)ai[0]].CopyInteractions(this);
				}
				if (type < 13 || type > 15)
				{
					Main.npc[(int)ai[0]].ai[3] = ai[3];
					Main.npc[(int)ai[0]].realLife = realLife;
				}
				Main.npc[(int)ai[0]].ai[1] = whoAmI;
				Main.npc[(int)ai[0]].ai[2] = ai[2] - 1f;
				netUpdate = true;
			}
			if (type == 412 && ai[0] == 0f)
			{
				ai[3] = whoAmI;
				realLife = whoAmI;
				int num33 = 0;
				int num34 = whoAmI;
				int num35 = 30;
				for (int num36 = 0; num36 < num35; num36++)
				{
					int num37 = 413;
					if (num36 == num35 - 1)
					{
						num37 = 414;
					}
					num33 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)(position.X + (float)(width / 2)), (int)(position.Y + (float)height), num37, whoAmI);
					Main.npc[num33].ai[3] = whoAmI;
					Main.npc[num33].realLife = whoAmI;
					Main.npc[num33].ai[1] = num34;
					Main.npc[num33].CopyInteractions(this);
					Main.npc[num34].ai[0] = num33;
					NetMessage.SendData(23, -1, -1, null, num33);
					num34 = num33;
				}
			}
			switch (type)
			{
			case 8:
			case 9:
			case 11:
			case 12:
			case 40:
			case 41:
			case 88:
			case 89:
			case 90:
			case 91:
			case 92:
			case 96:
			case 97:
			case 99:
			case 100:
			case 118:
			case 119:
			case 413:
			case 414:
			case 455:
			case 456:
			case 457:
			case 458:
			case 459:
			case 511:
			case 512:
			case 514:
			case 515:
			case 622:
			case 623:
				if (!Main.npc[(int)ai[1]].active || Main.npc[(int)ai[1]].aiStyle != aiStyle)
				{
					life = 0;
					HitEffect();
					checkDead();
					active = false;
					NetMessage.SendData(28, -1, -1, null, whoAmI, -1f);
					return;
				}
				break;
			}
			switch (type)
			{
			case 7:
			case 8:
			case 10:
			case 11:
			case 39:
			case 40:
			case 87:
			case 88:
			case 89:
			case 90:
			case 91:
			case 95:
			case 96:
			case 98:
			case 99:
			case 117:
			case 118:
			case 412:
			case 413:
			case 454:
			case 455:
			case 456:
			case 457:
			case 458:
			case 510:
			case 511:
			case 513:
			case 514:
			case 621:
			case 622:
				if (!Main.npc[(int)ai[0]].active || Main.npc[(int)ai[0]].aiStyle != aiStyle)
				{
					life = 0;
					HitEffect();
					checkDead();
					active = false;
					NetMessage.SendData(28, -1, -1, null, whoAmI, -1f);
					return;

```


---

## 🤖 Assistant · 2026-08-19T03:17:17.385Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Chain build matches (30 segments, last = 414, realLife = whoAmI). Segment integrity: 413/414 check ai[1] (previous segment) — wait, the FIRST switch (413/414 case) checks `Main.npc[(int)ai[1]].active` (previous segment id stored in ai[1]). The SECOND switch (412/413 case) checks `Main.npc[(int)ai[0]].active` (next segment in ai[0]).

So: 413 checks BOTH prev (ai[1]) and next (ai[0]); 414 checks only prev (ai[1]); 412 checks only next (ai[0]). Ours: prevDead for all segs (s.wormFollow), nextDead only for 413. Head: wormNext dead → die. Matches.

Now read 52020-52070 (414 flash + head dust), and then the movement part.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:17.887Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '52020,52070p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla crawltipede 414 flash and head dust"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:17.928Z

**📎 ToolResult**

```
			}
			else if (velocity.X > 0f)
			{
				spriteDirection = -1;
			}
		}
		if (type == 414)
		{
			if (justHit)
			{
				localAI[3] = 3f;
			}
			if (localAI[2] > 0f)
			{
				localAI[2] -= 16f;
				if (localAI[2] == 0f)
				{
					localAI[2] = -128f;
				}
			}
			else if (localAI[2] < 0f)
			{
				localAI[2] += 16f;
			}
			else if (localAI[3] > 0f)
			{
				localAI[2] = 128f;
				localAI[3] -= 1f;
			}
		}
		if (type == 412)
		{
			position += netOffset;
			Vector2 vector3 = base.Center + (rotation - MathF.PI / 2f).ToRotationVector2() * 8f;
			Vector2 vector4 = rotation.ToRotationVector2() * 16f;
			Dust obj = Main.dust[Dust.NewDust(vector3 + vector4, 0, 0, 6, velocity.X, velocity.Y, 100, Color.Transparent, 1f + Main.rand.NextFloat() * 3f)];
			obj.noGravity = true;
			obj.noLight = true;
			obj.position -= new Vector2(4f);
			obj.fadeIn = 1f;
			obj.velocity = Vector2.Zero;
			Dust obj2 = Main.dust[Dust.NewDust(vector3 - vector4, 0, 0, 6, velocity.X, velocity.Y, 100, Color.Transparent, 1f + Main.rand.NextFloat() * 3f)];
			obj2.noGravity = true;
			obj2.noLight = true;
			obj2.position -= new Vector2(4f);
			obj2.fadeIn = 1f;
			obj2.velocity = Vector2.Zero;
			position -= netOffset;
		}
		float num46 = 8f;
		float num47 = 0.07f;

```


---

## 🤖 Assistant · 2026-08-19T03:17:23.839Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The 414 flash step matches crawltipedeFlashStep exactly. Head dust matches ours.

Interesting: after the 412 dust block, `float num46 = 8f; float num47 = 0.07f;` — this is the generic AI_006 steering (for other worms). The 412-specific override happens later at :52176-52254 per our comments (num46=10, num47=0.3). Let me read 52160-52340 to verify the target override + separation + speed clamp.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:24.388Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '52160,52330p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla crawltipede target override and steering"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:24.429Z

**📎 ToolResult**

```
				num47 += 0.1f;
			}
		}
		if (type == 39)
		{
			num46 = 9f;
			num47 = 0.1f;
			if (Main.getGoodWorld)
			{
				num46 = 10f;
				num47 = 0.12f;
			}
		}
		Vector2 center = base.Center;
		float num49 = Main.player[target].Center.X;
		float num50 = Main.player[target].Center.Y;
		if (type == 412)
		{
			num46 = 10f;
			num47 = 0.3f;
			int num51 = -1;
			int num52 = (int)(Main.player[target].Center.X / 16f);
			int num53 = (int)(Main.player[target].Center.Y / 16f);
			for (int num54 = num52 - 2; num54 <= num52 + 2; num54++)
			{
				for (int num55 = num53; num55 <= num53 + 15; num55++)
				{
					if (WorldGen.SolidTile2(num54, num55))
					{
						num51 = num55;
						break;
					}
				}
				if (num51 > 0)
				{
					break;
				}
			}
			if (num51 > 0)
			{
				num51 *= 16;
				int num56 = num51 - 800;
				if (Main.player[target].position.Y > (float)num56)
				{
					num50 = num56;
					if (Math.Abs(base.Center.X - Main.player[target].Center.X) < 500f)
					{
						num49 = ((!(velocity.X > 0f)) ? (Main.player[target].Center.X - 600f) : (Main.player[target].Center.X + 600f));
					}
				}
			}
			else
			{
				num46 = 14f;
				num47 = 0.5f;
			}
			float num57 = num46 * 1.3f;
			float num58 = num46 * 0.7f;
			float num59 = velocity.Length();
			if (num59 > 0f)
			{
				if (num59 > num57)
				{
					velocity.Normalize();
					velocity *= num57;
				}
				else if (num59 < num58)
				{
					velocity.Normalize();
					velocity *= num58;
				}
			}
			int num60 = 60;
			float num61 = 200f;
			if (num51 > 0)
			{
				num60 = 400;
				num61 = 1000f;
			}
			for (int num62 = 0; num62 < Main.maxNPCs; num62++)
			{
				if (Main.npc[num62].active && Main.npc[num62].type == type && num62 != whoAmI)
				{
					Vector2 vector5 = Main.npc[num62].Center - base.Center;
					if (vector5.Length() < (float)num60)
					{
						vector5.Normalize();
						vector5 *= num61;
						num49 -= vector5.X;
						num50 -= vector5.Y;
					}
				}
			}
		}
		num49 = (int)(num49 / 16f) * 16;
		num50 = (int)(num50 / 16f) * 16;
		center.X = (int)(center.X / 16f) * 16;
		center.Y = (int)(center.Y / 16f) * 16;
		num49 -= center.X;
		num50 -= center.Y;
		if (type == 375)
		{
			num49 *= -1f;
			num50 *= -1f;
		}
		float num63 = (float)Math.Sqrt(num49 * num49 + num50 * num50);
		if (ai[1] > 0f && ai[1] < (float)Main.npc.Length)
		{
			try
			{
				center = base.Center;
				num49 = Main.npc[(int)ai[1]].Center.X - center.X;
				num50 = Main.npc[(int)ai[1]].Center.Y - center.Y;
			}
			catch
			{
			}
			rotation = (float)Math.Atan2(num50, num49) + 1.57f;
			num63 = (float)Math.Sqrt(num49 * num49 + num50 * num50);
			float num64 = width;
			if (type >= 87 && type <= 92)
			{
				num64 = 42f;
			}
			if (type >= 454 && type <= 459)
			{
				num64 = 36f;
			}
			if (type >= 513 && type <= 515)
			{
				num64 -= 6f;
			}
			if (type >= 412 && type <= 414)
			{
				num64 += 6f;
			}
			if (type >= 621 && type <= 623)
			{
				num64 = 24f;
			}
			if (Main.getGoodWorld && type >= 13 && type <= 15)
			{
				num64 = 62f;
			}
			num63 = (num63 - num64) / num63;
			num49 *= num63;
			num50 *= num63;
			velocity = Vector2.Zero;
			position.X += num49;
			position.Y += num50;
			if ((type >= 87 && type <= 92) || (type >= 454 && type <= 459) || (type >= 621 && type <= 623))
			{
				if (num49 < 0f)
				{
					spriteDirection = 1;
				}
				else if (num49 > 0f)
				{
					spriteDirection = -1;
				}
			}
		}
		else
		{
			if (!flag3)
			{
				TargetClosest();
				if (type == 39 && velocity.Y < 0f)
				{
					velocity.Y += 0.08f;
				}

```


---

## 🤖 Assistant · 2026-08-19T03:17:40.456Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
IMPORTANT structural detail found: in vanilla AI_006, the head (412) has `ai[1] == 0` (heads have no previous segment; ai[1] is set to whoAmI of the previous... wait, for the head, ai[1] was never set — actually for the head: `ai[3] = whoAmI; realLife = whoAmI;` and the chain loop sets `Main.npc[num34].ai[0] = num33` where num34 starts as whoAmI (the head). So the head's ai[0] = first body segment. Head's ai[1] stays 0 (default).

So for the head, `if (ai[1] > 0f && ...)` is FALSE → goes to the else branch (the steering toward num49/num50 target). For the body segments (413/414), ai[1] > 0 → the follow-shrink block (rotation, num64 = width+6, shrink, velocity = 0).

So: the head does steering; segments do the follow. Ours: head does steering + loop drives segments with shrink = (d - (s.w + 6))/d, rotation = atan2(dyC, dxC) + π/2, vx/vy = 0, facing = dxC < 0 ? 1 : -1. Vanilla follow block: rotation = atan2 + 1.57; num64 = width + 6 (412-414); num63 = (num63 - num64)/num63; num49 *= num63; num50 *= num63; position += num49/num50; velocity = 0; spriteDirection flip only for 87-92/454-459/621-623 — NOT for 412-414 (so segments' spriteDirection is whatever set earlier in the shared code — there's a generic spriteDirection section earlier around 52000). Ours sets `s.facing = dxC < 0 ? 1 : -1` for all segments — vanilla for crawltipede segments: earlier block at :52010-52024: `if (velocity.X < 0f) spriteDirection = 1; else if (velocity.X > 0f) spriteDirection = -1;` — but velocity = 0 in the follow block... that earlier block runs BEFORE velocity zeroing? The order: the spriteDirection block at :52005-52024 uses velocity (before it's zeroed in the follow block at :52307). Segment velocity was zeroed last tick, so spriteDirection only updates when... hmm, whatever. Ours sets facing from the follow delta — reasonable approximation.

Ours' follow: `const shrink = (d - (s.w + 6)) / d; s.x += dxC * shrink;` — vanilla: num63 = (num63 - num64)/num63 then num49 *= num63 → position += delta * (d - num64)/d. Same. 

Head steering: the else branch. Need to read the steering (flag3, etc.) at 52330-52610. Also verify flag3 = true for 412 ("空泳追击环 flag3 恒 true :51955-51957"). Let me read 51940-51960 and 52330-52620.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:41.569Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '51930,51990p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ====; sed -n '52330,52420p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla flag3 gate and steering want-velocity"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:41.608Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
			num39 = Main.maxTilesX;
		}
		if (num40 < 0)
		{
			num40 = 0;
		}
		if (num41 > Main.maxTilesY)
		{
			num41 = Main.maxTilesY;
		}
		bool flag2 = false;
		bool flag3 = false;
		bool flag4 = false;
		if (type >= 87 && type <= 92)
		{
			flag3 = true;
		}
		if (type >= 454 && type <= 459)
		{
			flag3 = true;
		}
		if (type >= 621 && type <= 623)
		{
			flag3 = true;
		}
		if (type >= 412 && type <= 414)
		{
			flag3 = true;
		}
		if (type == 402)
		{
			flag3 = true;
		}
		if (type >= 13 && type <= 15 && WorldGen.Skyblock.lowTiles)
		{
			flag2 = true;
			flag3 = true;
		}
		if (!flag3 || flag2)
		{
			Vector2 vector2 = default(Vector2);
			for (int num42 = num38; num42 < num39; num42++)
			{
				for (int num43 = num40; num43 < num41; num43++)
				{
					if (Main.tile[num42, num43] == null || ((!Main.tile[num42, num43].nactive() || (!Main.tileSolid[Main.tile[num42, num43].type] && (!Main.tileSolidTop[Main.tile[num42, num43].type] || Main.tile[num42, num43].frameY != 0))) && Main.tile[num42, num43].liquid <= 64))
					{
						continue;
					}
					vector2.X = num42 * 16;
					vector2.Y = num43 * 16;
					if (position.X + (float)width > vector2.X && position.X < vector2.X + 16f && position.Y + (float)height > vector2.Y && position.Y < vector2.Y + 16f)
					{
						flag4 = true;
						flag3 = true;
						if (Main.rand.Next(100) == 0 && type != 117 && Main.tile[num42, num43].nactive() && Main.tileSolid[Main.tile[num42, num43].type])
						{
							WorldGen.KillTile(num42, num43, fail: true, effectOnly: true);
						}
					}
				}
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-19T03:17:44.615Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The `====` echo failed due to zsh glob. Let me run the second sed separately with quotes.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:45.166Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '52330,52430p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla worm steering section"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:45.200Z

**📎 ToolResult**

```
				}
				else
				{
					velocity.Y += 0.11f;
				}
				if (velocity.Y > num46)
				{
					velocity.Y = num46;
				}
				if ((double)(Math.Abs(velocity.X) + Math.Abs(velocity.Y)) < (double)num46 * 0.4)
				{
					if (velocity.X < 0f)
					{
						velocity.X -= num47 * 1.1f;
					}
					else
					{
						velocity.X += num47 * 1.1f;
					}
				}
				else if (velocity.Y == num46)
				{
					if (velocity.X < num49)
					{
						velocity.X += num47;
					}
					else if (velocity.X > num49)
					{
						velocity.X -= num47;
					}
				}
				else if (velocity.Y > 4f)
				{
					if (velocity.X < 0f)
					{
						velocity.X += num47 * 0.9f;
					}
					else
					{
						velocity.X -= num47 * 0.9f;
					}
				}
			}
			else
			{
				if (type != 621 && type != 87 && type != 117 && type != 454 && type != 412 && soundDelay == 0 && (type < 13 || type > 15 || !WorldGen.Skyblock.lowTiles || flag4))
				{
					float num65 = num63 / 40f;
					if (num65 < 10f)
					{
						num65 = 10f;
					}
					if (num65 > 20f)
					{
						num65 = 20f;
					}
					soundDelay = (int)num65;
					if (type >= 13 && type <= 15)
					{
						SoundEngine.PlaySound(SoundID.EOWDiggin, (int)position.X, (int)position.Y);
					}
					else
					{
						SoundEngine.PlaySound(15, (int)position.X, (int)position.Y);
					}
				}
				num63 = (float)Math.Sqrt(num49 * num49 + num50 * num50);
				float num66 = Math.Abs(num49);
				float num67 = Math.Abs(num50);
				float num68 = num46 / num63;
				num49 *= num68;
				num50 *= num68;
				bool flag6 = false;
				if ((type == 7 || type == 13) && ((!Main.player[target].ZoneCorrupt && !Main.player[target].ZoneCrimson) || Main.player[target].dead))
				{
					flag6 = true;
				}
				if ((type == 513 && (double)Main.player[target].position.Y < Main.worldSurface * 16.0 && !Main.player[target].ZoneSandstorm && !Main.player[target].ZoneUndergroundDesert) || Main.player[target].dead)
				{
					flag6 = true;
				}
				if ((type == 510 && (double)Main.player[target].position.Y < Main.worldSurface * 16.0 && !Main.player[target].ZoneSandstorm && !Main.player[target].ZoneUndergroundDesert) || Main.player[target].dead)
				{
					flag6 = true;
				}
				if (flag6)
				{
					bool flag7 = true;
					for (int num69 = 0; num69 < 255; num69++)
					{
						if (Main.player[num69].active && !Main.player[num69].dead && Main.player[num69].ZoneCorrupt)
						{
							flag7 = false;
						}
					}
					if (flag7)
					{
						if (Main.netMode != 1 && (double)(position.Y / 16f) > (Main.rockLayer + (double)Main.maxTilesY) / 2.0)
						{
							active = false;
							int num70 = (int)ai[0];

```


---

## 🤖 Assistant · 2026-08-19T03:17:49.593Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '52430,52620p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla worm steering continuation"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:49.627Z

**📎 ToolResult**

```
							int num70 = (int)ai[0];
							while (num70 > 0 && num70 < Main.maxNPCs && Main.npc[num70].active && Main.npc[num70].aiStyle == aiStyle)
							{
								int num71 = (int)Main.npc[num70].ai[0];
								Main.npc[num70].active = false;
								life = 0;
								if (Main.netMode == 2)
								{
									NetMessage.SendData(23, -1, -1, null, num70);
								}
								num70 = num71;
							}
							if (Main.netMode == 2)
							{
								NetMessage.SendData(23, -1, -1, null, whoAmI);
							}
						}
						num49 = 0f;
						num50 = num46;
					}
				}
				bool flag8 = false;
				if (type == 87)
				{
					if (((velocity.X > 0f && num49 < 0f) || (velocity.X < 0f && num49 > 0f) || (velocity.Y > 0f && num50 < 0f) || (velocity.Y < 0f && num50 > 0f)) && Math.Abs(velocity.X) + Math.Abs(velocity.Y) > num47 / 2f && num63 < 300f)
					{
						flag8 = true;
						if (Math.Abs(velocity.X) + Math.Abs(velocity.Y) < num46)
						{
							velocity *= 1.1f;
						}
					}
					if (base.Center.Y > Main.player[target].Center.Y || (double)(Main.player[target].Center.Y / 16f) > Main.worldSurface || Main.player[target].dead)
					{
						flag8 = true;
						if (Math.Abs(velocity.X) < num46 / 2f)
						{
							if (velocity.X == 0f)
							{
								velocity.X -= direction;
							}
							velocity.X *= 1.1f;
						}
						else if (velocity.Y > 0f - num46)
						{
							velocity.Y -= num47;
						}
					}
				}
				if (type == 454 || type == 621)
				{
					float num72 = 300f;
					if (type == 621)
					{
						num72 = 120f;
					}
					if (((velocity.X > 0f && num49 < 0f) || (velocity.X < 0f && num49 > 0f) || (velocity.Y > 0f && num50 < 0f) || (velocity.Y < 0f && num50 > 0f)) && Math.Abs(velocity.X) + Math.Abs(velocity.Y) > num47 / 2f && num63 < num72)
					{
						flag8 = true;
						if (Math.Abs(velocity.X) + Math.Abs(velocity.Y) < num46)
						{
							velocity *= 1.1f;
						}
					}
					if (position.Y > Main.player[target].position.Y || Main.player[target].dead)
					{
						flag8 = true;
						if (Math.Abs(velocity.X) < num46 / 2f)
						{
							if (velocity.X == 0f)
							{
								velocity.X -= direction;
							}
							velocity.X *= 1.1f;
						}
						else if (velocity.Y > 0f - num46)
						{
							velocity.Y -= num47;
						}
					}
				}
				if (!flag8)
				{
					if ((velocity.X > 0f && num49 > 0f) || (velocity.X < 0f && num49 < 0f) || (velocity.Y > 0f && num50 > 0f) || (velocity.Y < 0f && num50 < 0f))
					{
						if (velocity.X < num49)
						{
							velocity.X += num47;
						}
						else if (velocity.X > num49)
						{
							velocity.X -= num47;
						}
						if (velocity.Y < num50)
						{
							velocity.Y += num47;
						}
						else if (velocity.Y > num50)
						{
							velocity.Y -= num47;
						}
						if (Math.Abs(num50) < num46 * 0.2f && ((velocity.X > 0f && num49 < 0f) || (velocity.X < 0f && num49 > 0f)))
						{
							if (velocity.Y > 0f)
							{
								velocity.Y += num47 * 2f;
							}
							else
							{
								velocity.Y -= num47 * 2f;
							}
						}
						if (Math.Abs(num49) < num46 * 0.2f && ((velocity.Y > 0f && num50 < 0f) || (velocity.Y < 0f && num50 > 0f)))
						{
							if (velocity.X > 0f)
							{
								velocity.X += num47 * 2f;
							}
							else
							{
								velocity.X -= num47 * 2f;
							}
						}
					}
					else if (num66 > num67)
					{
						if (velocity.X < num49)
						{
							velocity.X += num47 * 1.1f;
						}
						else if (velocity.X > num49)
						{
							velocity.X -= num47 * 1.1f;
						}
						if (Math.Abs(velocity.X) + Math.Abs(velocity.Y) < num46 * 0.5f)
						{
							if (velocity.Y > 0f)
							{
								velocity.Y += num47;
							}
							else
							{
								velocity.Y -= num47;
							}
						}
					}
					else
					{
						if (velocity.Y < num50)
						{
							velocity.Y += num47 * 1.1f;
						}
						else if (velocity.Y > num50)
						{
							velocity.Y -= num47 * 1.1f;
						}
						if (Math.Abs(velocity.X) + Math.Abs(velocity.Y) < num46 * 0.5f)
						{
							if (velocity.X > 0f)
							{
								velocity.X += num47;
							}
							else
							{
								velocity.X -= num47;
							}
						}
					}
				}
			}
			rotation = (float)Math.Atan2(velocity.Y, velocity.X) + MathF.PI / 2f;
			if (type == 7 || type == 10 || type == 13 || type == 39 || type == 95 || type == 98 || type == 117 || type == 510 || type == 513 || type == 621)
			{
				if (flag3)
				{
					if (localAI[0] != 1f)
					{
						netUpdate = true;
					}
					localAI[0] = 1f;
				}
				else
				{
					if (localAI[0] != 0f)
					{
						netUpdate = true;
					}
					localAI[0] = 0f;
				}
				if (((velocity.X > 0f && oldVelocity.X < 0f) || (velocity.X < 0f && oldVelocity.X > 0f) || (velocity.Y > 0f && oldVelocity.Y < 0f) || (velocity.Y < 0f && oldVelocity.Y > 0f)) && !justHit)
				{

```


---

## 🤖 Assistant · 2026-08-19T03:18:34.376Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The !flag8 steering block matches ours exactly (first sub-branch: aligned axes → num47 steps; the num50/num49 < num46*0.2 perpendicular boosts; else num66>num67 branches with 1.1 steps and the |vx|+|vy| < num46*0.5 pushes). Ours implements precisely this.

Head rotation = atan2(vy,vx) + π/2 — ours matches.

Important detail: the flag6 flee logic (EoW/513/510 despawn) doesn't apply to 412 (flag6 false). Sound: type != 621/87/117/454/412 excludes 412 → wait: `if (type != 621 && type != 87 && type != 117 && type != 454 && type != 412 && soundDelay == 0 ...)` → for 412, NO digging sound. Ours doesn't play a sound. Good.

But one thing before steering: where's the "num47 += 0.1f" at :52160? That was in some earlier conditional for other types. Not 412.

Now — flag3 is true for 412, which affects the tile-collision bypass: since flag3=true from the start, the head never does the "collide with tiles" scanning. Where's flag3 used for movement? Looking at the snippet: `if (!flag3 || flag2) { tile scanning ... }` — that's for non-flag3 worms. And in the movement integration section later (~52650+?) flag3 likely disables tile collision. Ours: noTileCollide direct integration. OK.

Now the segment follow: vanilla head has ai[1] == 0 → steering. Segments: ai[1] = previous id > 0 → follow. Ours: the head loop drives segments (wormNext/wormFollow). Equivalent.

One important check — vanilla: when the head's target player dies or is far... TargetClosest(); flag6 false for 412. The num49/num50 target = player center. Ours has "无目标:缓漂" — in single player p is nearly always non-null. OK approximation.

Now — the 412 target override: vanilla checks `Main.player[target].position.Y > (float)num56` (player TOP y vs hover line). Ours: `if (player.y > hoverY)` — player.y is top. Matches.

num51 = first solid row from player row (pty) down 15 — vanilla `for num55 = num53; num55 <= num53 + 15` (INCLUSIVE of +15 → 16 rows). Ours: `for (let dy = 0; dy <= 15; dy++)` → also 16 rows. Matches.

num49/num50 quantization: `(int)(num49/16)*16` — truncation toward zero. Ours: Math.floor(tx/TILE)*TILE - Math.floor(e.cx/TILE)*TILE. Hmm — vanilla quantizes num49 and num50 separately from center: center.X = (int)(center.X/16)*16. Both use (int) cast = truncation toward zero. For negative values, Math.floor differs from truncation! Player centers are typically positive (world coords positive), so equivalent in practice. Fine.

num68 = num46 / num63; num49 *= num68 → target velocity = normalized delta * num46. Ours: wantX = (dxq/dist)*num46. Same.

So crawltipede is faithful. One more thing to check: vanilla crawltipede head uses `velocity` for dust AFTER... fine.

Also check the segment-follow code in ours runs every tick for segments via head loop, but the head also checks `if (!e.wormNext || e.wormNext.dead) { e.die(game); return; }`. Vanilla head: `if (!Main.npc[(int)ai[0]].active || aiStyle mismatch) → die`. Matches.

Now back to remaining unverified bits:

1. moonLordFreeEyeAI state 2 hex pair — verified against table (0-2,2-5,5-3,3-1,1-4,4-0). Matches.

2. The free eye: vanilla `num1294 = (int)this.ai[1] - num1298;` — (int) truncation. Ours: `const t = e.ai1 - consumed`. Equivalent.

3. Sound in state 1: `if (num1294 == num1295 - 35f) PlaySound(4, ..., 6)` — PlaySound(4) = NPCHit. Ours: t === dur - 35 → 'NPC_Hit_6'. OK.

4. State 4 (deathray): num1318: spinningpoint11 = normalized (player - center); num1318 = -1 if x < 0 else 1... wait: `float num1318 = -1f; if (spinningpoint11.X < 0f) num1318 = 1f;` → num1318 = (x < 0) ? 1 : -1. Ours: `const n = dx / dd < 0 ? 1 : -1;`. Matches. Angle: rotated by (0 - num1318) * 2π/6 → -n*π/3. Ours: `ang = atan2(dy,dx) - n * TAU/6`. Matches. ai[2] = (rotation + 3π) * num1318. Ours matches. Sweep num1318 * 2π/540. Ours passes n * TAU / 540. Matches. Projectile 455 damage 50 — ours 100 (project-wide ×2 convention, consistent with core). OK.

Now the remaining priority: verify the leech's `head.cx` vs `head.Center + (0,216)`: ours `e.y = lerp(x[1], head.cy + 216, k) - e.h / 2`. Matches.

Also check moonLeechAI heal: vanilla num1335 = num1329 + min(num1333 - num1329, 0) = min(pool, deficit). Ours: `amt = Math.min(pool, deficit)`. Matches. Heal effect particle counts approximate.

Now let me double check a few more suspicious spots I noted:

A. moonLordFreeEyeAI: state 0 hover target — vanilla: vector220 = (player.Center + vel*20 ... wait no. In state 0: v11 = player.Center + player.velocity*20 - Center (for eye angle); then vector219 = center37 - center36 = player.Center - Center; vector220 = vector219 - UnitY*200 → target = player - (0,200). Normalized * 24. Ours: tx = pcx + player.vx*20 - e.cx... for the ANGLE yes; but for hover: `let tx = pcx - e.cx, ty = pcy - 200 - e.cy`. Vanilla hover does NOT add velocity*20. Ours matches (velocity*20 only for the eye angle). Good.

B. State 1 shoot: vector221 = Vector2FromElipse(localAI[0].ToRotationVector2(), vector218 * localAI[1]) — ellipse (30,30)*openness. Ours: ox = cos(x[0])*30*x[1]. OK. Speed 8 normalized v12. Ours matches. num1295 is slot duration = 90; t === dur-35 → 55. Ours: `if (t === dur - 35)`. Matches.

C. bigMimic state 0 wake: vanilla includes `velocity.Y > 100f` (falling fast). Ours matches.

D. bigMimic: our state-2 `if (e.onGround && e.vy === 0)`: in our engine after grounded() the vy==0 when resting. OK.

E. mothron: noTileCollide handling: vanilla state 0/2 use collision; ours uses moveAndCollide + bounceAxis. Vanilla state 3/3.1/3.2/4.1/4.2 noTileCollide=true → fly. Ours matches.

F. babyMothron eclipse gate: vanilla returns BEFORE separation and states when eclipse false — ours: `if (!game.world.clock.eclipse) { encourageDespawn; vy clamp; fly; return; }`. Matches. Vanilla also sets noTileCollide=true there. Ours fly. OK.

G. mothron: `!game.world.clock.eclipse` — check `game.world.clock.eclipse` exists. It's used elsewhere (eclipse event system). Fine.

H. In mothronAI the egg-laying search uses `game.world.groundLevel` — let me verify the property name/units quickly.

I. cultistArcherStandbyAI + cultistArcherWake: vanilla :56575-56610. Let me read that to verify.

J. free eye: `if (rnd(420) === 0)` matches Main.rand.Next(420)==0.

K. One more check on mothron state 0: ours does `e.facing = e.cx < p.cx - 2 ? 1 : e.cx > p.cx + 2 ? -1 : e.facing` — vanilla sets direction=1 if <, direction=-1 if >, else keeps. Matches.

L. Mothron egg transform: `e.transformTo(479, ...)` — fine.

M. smallStarCell: `if (e.ai0 < 0) e.ai0 = 0` — same clamp-clobber concern as egg? For 406 there's no justHit decrement. Fine.

N. flowInvader: 407/408 — vanilla aiStyle 96 for both. Ours treats same. OK.

O. LunarOrb: vanilla 539 orbit 210t then charge; 574 orbit 180t then fire 576 and reset. Ours: `orbitT = 539 ? 210 : 180`. For 574: at ai0 === orbitT → fire 576 + reset ai0 = 0. For 539: at ai0 === orbitT → set velocity toward player; then continues ai0 > orbitT forever (charges until tile hit / life). Ours: life 600 decrements; `if (this.life-- <= 0) explode`. Hmm — for 539 vanilla: timeLeft? Projectile 539 SetDefaults timeLeft = 600? Let me check Projectile.cs 5864-5878 quickly. Also whether 539's explode-on-tile and 80x80 damage are right (:69366-69405 is the Kill/OnHitBits). I'll trust the referenced lines.

P. Nebula floater telefrag/teleport spot helper — vanilla AI_AttemptToFindTeleportSpot(18876-18946). Ours implements a condensed version. Let me verify key params: (20, 12, 1, solidTileCheckCentered: true, teleportInAir: true). Read vanilla 18876-18946 to compare the essential gates.

Q. starCellAI state 5: ours applies BuffType.Obstructed every tick — matches AddBuff(163, 59) unless creativeGodMode. Ours no god-mode check (journey mode). Fine.

Let me now read vanilla 56575-56610 for the archer standby, and 18876-18946 for the teleport spot.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:35.091Z · glm-x-preview-260804

```
爬行蜈蚣的转向逻辑已完成验证。接下来是弓箭手待机 (56575-56610) 和传送点查找器 (18876-18946)。
```


---

## 🤖 Assistant · 2026-08-19T03:18:35.648Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '56575,56615p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla cultist archer ritual standby"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:35.793Z

**📎 ToolResult**

```
		if (type == 379 || type == 380)
		{
			if (ai[3] < 0f)
			{
				directionY = -1;
				flag = false;
				damage = 0;
				velocity.X *= 0.93f;
				if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
				{
					velocity.X = 0f;
				}
				int num11 = (int)(0f - ai[3] - 1f);
				int num12 = Math.Sign(Main.npc[num11].Center.X - base.Center.X);
				if (num12 != direction)
				{
					velocity.X = 0f;
					direction = num12;
					netUpdate = true;
				}
				if (justHit && Main.netMode != 1 && Main.npc[num11].localAI[0] == 0f)
				{
					Main.npc[num11].localAI[0] = 1f;
				}
				if (ai[0] < 1000f)
				{
					ai[0] = 1000f;
				}
				if ((ai[0] += 1f) >= 1300f)
				{
					ai[0] = 1000f;
					netUpdate = true;
				}
				return;
			}
			if (ai[0] >= 1000f)
			{
				ai[0] = 0f;
			}
			damage = defDamage;
		}

```


---

## 🤖 Assistant · 2026-08-19T03:18:40.507Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The archer standby matches ours (ai[0] 1000..1300 loop, damage=0, friction, face tablet, justHit → tablet localAI[0]=1, then ai[0] >= 1000 → 0 + damage = defDamage on wake). Ours matches, including `damage = defDamage` restore via cultistArcherWake. Good.

Now the teleport spot helper vanilla 18876-18946.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:41.049Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '18876,18950p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_AttemptToFindTeleportSpot"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:41.125Z

**📎 ToolResult**

```
	public bool AI_AttemptToFindTeleportSpot(ref Vector2 chosenTile, int targetTileX, int targetTileY, int rangeFromTargetTile = 20, int telefragPreventionDistanceInTiles = 5, int solidTileCheckFluff = 1, bool solidTileCheckCentered = false, bool teleportInAir = false)
	{
		int num = (int)base.Center.X / 16;
		int num2 = (int)base.Center.Y / 16;
		int num3 = 0;
		bool flag = false;
		float num4 = 20f;
		if (Math.Abs(num * 16 - targetTileX * 16) + Math.Abs(num2 * 16 - targetTileY * 16) > 2000)
		{
			num3 = 100;
			flag = false;
		}
		while (!flag && num3 < 100)
		{
			num3++;
			int num5 = Main.rand.Next(targetTileX - rangeFromTargetTile, targetTileX + rangeFromTargetTile + 1);
			for (int i = Main.rand.Next(targetTileY - rangeFromTargetTile, targetTileY + rangeFromTargetTile + 1); i < targetTileY + rangeFromTargetTile; i++)
			{
				if ((i >= num2 - 1 && i <= num2 + 1 && num5 >= num - 1 && num5 <= num + 1) || (!teleportInAir && !Main.tile[num5, i].nactive()))
				{
					continue;
				}
				bool flag2 = true;
				if ((type == 32 || (type >= 281 && type <= 286)) && !Main.wallDungeon[Main.tile[num5, i - 1].wall])
				{
					if (!AnyNPCs(35))
					{
						flag2 = false;
					}
				}
				else if (Main.tile[num5, i - 1].lava())
				{
					flag2 = false;
				}
				if (!flag2 || (!teleportInAir && !Main.tileSolid[Main.tile[num5, i].type]))
				{
					continue;
				}
				bool flag3 = false;
				if (!((!solidTileCheckCentered) ? (!Collision.SolidTiles(num5 - solidTileCheckFluff, num5 + solidTileCheckFluff, i - 3 - solidTileCheckFluff, i - 1)) : (!Collision.SolidTiles(num5 - solidTileCheckFluff, num5 + solidTileCheckFluff, i - solidTileCheckFluff, i + solidTileCheckFluff))))
				{
					continue;
				}
				Rectangle rectangle = new Rectangle(num5 * 16, i * 16, 16, 16);
				rectangle.Inflate(telefragPreventionDistanceInTiles * 16, telefragPreventionDistanceInTiles * 16);
				for (int j = 0; j < Main.player.Length; j++)
				{
					Player player = Main.player[j];
					if (player != null && player.active && !player.dead)
					{
						Rectangle value = player.Hitbox;
						Rectangle value2 = value.Modified((int)(player.velocity.X * num4), (int)(player.velocity.Y * num4), 0, 0);
						Rectangle.Union(ref value2, ref value, out value2);
						if (value2.Intersects(rectangle))
						{
							flag2 = false;
							flag = false;
							break;
						}
					}
				}
				if (flag2)
				{
					chosenTile = new Vector2(num5, i);
					flag = true;
				}
				break;
			}
		}
		return flag;
	}

	private bool AI_AttemptToFindTeleportSpotNearBooks(Point targetPosition, int maxRangeInTiles, out Vector2 destination)
	{
		destination = Vector2.Zero;

```


---

## 🤖 Assistant · 2026-08-19T03:18:57.563Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla AI_AttemptToFindTeleportSpot with the nebula floater params (20, 12, 1, centered, inAir):

- rangeFromTargetTile = 20: num5 = rand(targetTileX-20, targetTileX+21).
- The Y loop: `for (int i = rand(ty-20, ty+21); i < ty+20; i++)` — interesting! The inner for starts at a RANDOM row and iterates UP TO ty+20 (exclusive). Since teleportInAir=true, the `(!teleportInAir && ...)` skip is off. So candidates are (num5, i) for i from a random start row up to ty+19. That's a partial column scan starting from a random row — quirky. Ours: single candidate per attempt (tx, ty both random). Vanilla's for-loop means: one X per while-iteration, scanning multiple Y values (from random start to ty+20). The loop body `break`s at the end of the first candidate evaluation regardless (the final `break` at the loop bottom). So per while iteration: ONE candidate is evaluated: (num5, i0) where i0 = random. Then break. So effectively ours = vanilla (one random candidate per attempt) EXCEPT vanilla's Y range is [random start, ty+20) — i0 is already uniform random in [ty-20, ty+20), so identical distribution. OK, ours matches.
- Self-exclusion: (i within ±1 of num2 && num5 within ±1 of num) → skip. Ours matches.
- Lava check on tile[num5, i-1].lava() → skip. Ours checks (tx, ty-1) liquid lava. Matches.
- Solid check (centered): !SolidTiles(num5-1, num5+1, i-1, i+1) must hold (i.e., the 3×3 centered on (num5,i) must be clear). Ours: solidRect(tx-1, ty-1, tx+1, ty+1) → skip if solid. Matches.
- Telefrag: rectangle = tile 16×16 inflated by telefragPreventionDistanceInTiles*16 = 12*16 (param 12). Player hitbox union (hitbox modified by velocity*20). Ours: inflate 12*16 both dirs, player union with vel*20. Matches.
- Distance gate: |selfTile*16 - targetTile*16| manhattan > 2000 → give up (num3 = 100 → loop doesn't run). Ours returns null. Matches.
- Note ours counts attempts from 0..99 (100 attempts). Vanilla: num3 starts 0; while (!flag && num3 < 100) { num3++; ... } → 100 iterations. Ours: `for (let attempt = 0; attempt < 100; attempt++)`. Matches.

Great — teleport spot helper matches.

Now let me verify some claims in ours that reference vanilla behaviors I haven't checked:

1. LunarOrb orbit / charge (Projectile.cs:32040-32280) and 539 death explosion (:69366-69405). Also timeLeft for 539/574 (Projectile.cs:5864-5878).

2. flowInvader: LunarOrb 539 with dmg 60 — vanilla 539 damage = 60. And our explode uses this.dmg for player damage. Vanilla: on 539 death, damage in 80×80 area. OK.

3. The free eye 'core' anchor: `n.vanillaId === 398` — vanilla checks Main.npc[(int)ai[3]].type != 398 → despawn. Ours: `!core || core.dead`. Matches.

Let me quickly check Projectile.cs 32040-32280 for the orb orbit/charge details (numbers 0.15/0.075, clamp 6, 16 speed charge, 574 fire 576 8 speed 65 dmg, reset).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:57.980Z · glm-x-preview-260804

```
Teleport matcher 已符合。现在我来验证 Projectile.cs 中的 LunarOrb 投射物行为 (32040-32280)。
```


---

## 🤖 Assistant · 2026-08-19T03:18:58.480Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '32040,32135p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs",
 "description": "Read vanilla projectile AI_102 orbit section"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:58.538Z

**📎 ToolResult**

```
		else if (aiStyle == 102)
		{
			int num850 = 0;
			float num851 = 0f;
			float x7 = 0f;
			float y9 = 0f;
			int num852 = -1;
			int num853 = 0;
			float num854 = 0f;
			bool flag47 = true;
			bool flag48 = false;
			bool flag49 = false;
			switch (type)
			{
			case 539:
				num850 = 407;
				num851 = 210f;
				x7 = 0.15f;
				y9 = 0.075f;
				num854 = 16f;
				break;
			case 573:
				num850 = 424;
				num851 = 90f;
				num854 = 20f;
				flag47 = false;
				flag48 = true;
				break;
			case 574:
				num850 = 420;
				num851 = 180f;
				x7 = 0.15f;
				y9 = 0.075f;
				num854 = 8f;
				flag47 = false;
				num852 = 576;
				num853 = 65;
				if (Main.expertMode)
				{
					num853 = 50;
				}
				flag49 = true;
				break;
			}
			if (flag49)
			{
				int num855 = (int)this.ai[1];
				if (!Main.npc[num855].active || Main.npc[num855].type != num850)
				{
					Kill();
					return;
				}
				timeLeft = 2;
			}
			this.ai[0]++;
			if (this.ai[0] < num851)
			{
				bool flag50 = true;
				int num856 = (int)this.ai[1];
				if (Main.npc[num856].active && Main.npc[num856].type == num850)
				{
					if (!flag48 && Main.npc[num856].oldPos[1] != Vector2.Zero)
					{
						base.position += Main.npc[num856].position - Main.npc[num856].oldPos[1];
					}
				}
				else
				{
					this.ai[0] = num851;
					flag50 = false;
				}
				if (flag50 && !flag48)
				{
					velocity += new Vector2(Math.Sign(Main.npc[num856].Center.X - base.Center.X), Math.Sign(Main.npc[num856].Center.Y - base.Center.Y)) * new Vector2(x7, y9);
					if (velocity.Length() > 6f)
					{
						velocity *= 6f / velocity.Length();
					}
				}
				if (type == 539)
				{
					if (Main.rand.Next(12) == 0)
					{
						int num857 = Dust.NewDust(base.Center, 8, 8, 180);
						Main.dust[num857].position = base.Center;
						Dust dust2 = Main.dust[num857];
						dust2.velocity *= 0.2f;
						Main.dust[num857].noGravity = true;
					}
					if (++frameCounter >= 4)
					{
						frameCounter = 0;
						if (++frame >= Main.projFrames[type])
						{
							frame = 0;
						}

```


---

## 🤖 Assistant · 2026-08-19T03:19:03.356Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Orbit matches (0.15/0.075 clamp 6, parent displacement). Note for 574: `timeLeft = 2` every tick while parent alive — our LunarOrb 574 dies when parent dead. Matches.

Let me check the 32135-32280 charge section quickly for the 539 charge and 574 fire numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:03.945Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '32150,32240p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs",
 "description": "Read vanilla projectile AI_102 fire section"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:04.012Z

**📎 ToolResult**

```
				}
				if (type == 574)
				{
					if (Main.rand.Next(10) == 0)
					{
						int num859 = Dust.NewDust(base.Center, 8, 8, 242);
						Main.dust[num859].position = base.Center;
						Main.dust[num859].velocity = velocity;
						Main.dust[num859].noGravity = true;
						Main.dust[num859].scale = 1.5f;
					}
					if (flag50)
					{
						int target2 = Main.npc[num856].target;
						float num860 = velocity.ToRotation();
						if (Collision.CanHitLine(base.Center, 0, 0, Main.player[target2].Center, 0, 0))
						{
							num860 = DirectionTo(Main.player[target2].Center).ToRotation();
						}
						rotation = rotation.AngleLerp(num860 + MathF.PI / 2f, 0.2f);
					}
					frame = 1;
				}
			}
			if (this.ai[0] == num851)
			{
				bool flag51 = true;
				int num861 = -1;
				if (!flag47)
				{
					int num862 = (int)this.ai[1];
					if (Main.npc[num862].active && Main.npc[num862].type == num850)
					{
						num861 = Main.npc[num862].target;
					}
					else
					{
						flag51 = false;
					}
				}
				else
				{
					flag51 = false;
				}
				if (!flag51)
				{
					num861 = Player.FindClosest(base.position, width, height);
				}
				Vector2 value12 = Main.player[num861].Center - base.Center;
				value12.X += Main.rand.Next(-50, 51);
				value12.Y += Main.rand.Next(-50, 51);
				value12.X *= (float)Main.rand.Next(80, 121) * 0.01f;
				value12.Y *= (float)Main.rand.Next(80, 121) * 0.01f;
				Vector2 vector103 = Vector2.Normalize(value12);
				if (vector103.HasNaNs())
				{
					vector103 = Vector2.UnitY;
				}
				if (num852 == -1)
				{
					velocity = vector103 * num854;
					netUpdate = true;
				}
				else
				{
					if (Main.netMode != 1 && Collision.CanHitLine(base.Center, 0, 0, Main.player[num861].Center, 0, 0))
					{
						NewProjectile(GetProjectileSource_FromThis(), base.Center.X, base.Center.Y, vector103.X * num854, vector103.Y * num854, num852, num853, 1f, Main.myPlayer);
					}
					this.ai[0] = 0f;
				}
			}
			if (!(this.ai[0] >= num851))
			{
				return;
			}
			rotation = rotation.AngleLerp(velocity.ToRotation() + MathF.PI / 2f, 0.4f);
			if (type == 539)
			{
				if (++frameCounter >= 2)
				{
					frameCounter = 0;
					if (++frame >= Main.projFrames[type])
					{
						frame = 0;
					}
				}
				if (Main.rand.Next(2) == 0)
				{
					int num863 = Dust.NewDust(base.position, width, height, 180, 0f, 0f, 100);
					Dust dust2 = Main.dust[num863];

```


---

## 🤖 Assistant · 2026-08-19T03:19:13.272Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key details:

1. 539 charge: velocity = vector103 * 16 where vector103 = normalized (player + jitter ±50, scaled 0.8-1.2). Ours matches.

2. 574 fire at ai0 == 180: fires 576 with damage num853 = 65 (normal) or 50 (EXPERT). Ours passes 65 always. Expert not reachable. OK. Speed num854 = 8. Ours: 8. Matches. Gate CanHitLine. Reset ai[0] = 0. Ours resets. 

Wait — important: for 574, `flag47 = false` → num861 = npc target's... For 574 the fire happens at ai0 == num851 = 180 targeting the PARENT's target player. Ours uses game.player. Fine (single player).

3. For 539 after charge (ai0 >= 210): rotation AngleLerp(velocity.ToRotation() + π/2, 0.4). Ours: registered deviation in draw() (always uses vx*0.1 orbit rotation). Disclosed in code comment. OK.

4. 574 orbit rotation: AngleLerp toward (CanHitLine ? direction-to-player : velocity rotation) + π/2, 0.2. Ours draw: Math.atan2(vy, vx) + π/2 directly. Approximation. Fine.

Now the 539 explosion (Projectile.cs:69366-69405). Let me check quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:13.723Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '69366,69410p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs",
 "description": "Read vanilla 539 death explosion"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:13.802Z

**📎 ToolResult**

```
		if (type == 539)
		{
			position = base.Center;
			width = (height = 80);
			base.Center = position;
			Damage();
			SoundEngine.PlaySound(4, (int)position.X, (int)position.Y, 7);
			for (int num242 = 0; num242 < 4; num242++)
			{
				int num243 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 31, 0f, 0f, 100, default(Color), 1.5f);
				Main.dust[num243].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 2f;
			}
			for (int num244 = 0; num244 < 20; num244++)
			{
				int num245 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 176, 0f, 0f, 200, default(Color), 3.7f);
				Main.dust[num245].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 2f;
				Main.dust[num245].noGravity = true;
				Dust dust2 = Main.dust[num245];
				dust2.velocity *= 3f;
			}
			for (int num246 = 0; num246 < 20; num246++)
			{
				int num247 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 180, 0f, 0f, 0, default(Color), 2.7f);
				Main.dust[num247].position = base.Center + Vector2.UnitX.RotatedByRandom(3.1415927410125732).RotatedBy(velocity.ToRotation()) * width / 2f;
				Main.dust[num247].noGravity = true;
				Dust dust2 = Main.dust[num247];
				dust2.velocity *= 3f;
			}
			for (int num248 = 0; num248 < 10; num248++)
			{
				int num249 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 31, 0f, 0f, 0, default(Color), 1.5f);
				Main.dust[num249].position = base.Center + Vector2.UnitX.RotatedByRandom(3.1415927410125732).RotatedBy(velocity.ToRotation()) * width / 2f;
				Main.dust[num249].noGravity = true;
				Dust dust2 = Main.dust[num249];
				dust2.velocity *= 3f;
			}
		}
		else if (type == 585)
		{
			SoundEngine.PlaySound(0, (int)position.X, (int)position.Y, 27);
			for (int num250 = 0; num250 < 20; num250++)
			{
				int num251 = Dust.NewDust(position, width, height, 26, 0f, 0f, 100);
				Main.dust[num251].noGravity = true;
				Dust dust2 = Main.dust[num251];

```


---

## 🤖 Assistant · 2026-08-19T03:19:33.657Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
539 explosion: 80×80 damage box centered — ours uses ±40 from center. Matches. Missing sound 4 style 7 (NPC_Hit_7) in explode — minor visual/audio. Our explode doesn't play a sound. Hmm — let me check: our `explode()` does particles + damage but no sound. Vanilla plays SoundID 4 style 7. Minor audio omission. Could mention as a minor note. Not top-10 worthy probably (the audit cares about structural). I'll list in minor notes.

Now remaining to verify:
1. moonLordFreeEyeAI — mostly done. One more check: state 2 "else if (t < 105)": ours has `if (t === 75) { e.vx = 0; e.vy = -7; }` — vanilla at num1294==75 sets velocity = UnitY*-7 (vx=0) AND adds velocity to existing 454 projectiles (skipped, documented). Then `velocity.Y *= 0.96`. And ai[2] = angle to player + π/2 (ours `if (player) e.ai2 = ...` — vanilla always sets, using Main.player[target]; if no player, ours keeps old ai2. Minor).

2. Also `e.spin` in state 2 t∈[75,105): rotation.AngleTowards(ai[2], π/30). Ours: `e.spin = angleTowards(e.spin, e.ai2, Math.PI / 30)`. Matches.

3. The free eye's movement: vanilla uses noTileCollide? Moon Lord free eye 400 — SetDefaults has noTileCollide... not critical: ours uses fly(). Vanilla NPC 400 noTileCollide = true (SetDefaults). Fine.

4. Verify `losClear` CanHit approximation — used broadly. Fine.

Now the flowInvader 407/408 check on `e.ai0 < 0` clamp — vanilla ai[0] starts 0. Fine.

Now double-check `cultistTabletAI` gone-check subtlety: ours checks `[0,1].every(...)`. Vanilla flag93 requires for BOTH k=0,1: devotee_k inactive AND archer_k inactive. Wait no — vanilla loop: for k in 0..1: if devotee_k active → flag93=false; if archer_k active → flag93=false. So gone = !(dev0 active) && !(arc0 active) && !(dev1 active) && !(arc1 active). Ours: every(k => dev_k dead && arc_k dead). Same. But subtle: vanilla checks `Main.npc[(int)localAI[k+1] - 1].active && type == 438` — if the slot got REUSED by another NPC (id reallocation), type != 438 → counts as gone. Ours: `dev.vanillaId !== 438` counts as gone. Matches.

Edge: ours uses `enemies(game).find(n => n.id === x[k+1]-1)` — if not found → `!dev` → counts dead. Matches !active.

5. bigMimic: our state 4 sets `e.noGravity = true` — but in our engine noGravity isn't used by these AI functions; state 4 uses fly(). The noGravity assignments are for StrikeNPC (per comment). OK.

6. Also mimic state 4: ours `if (p) e.facing = e.vx < 0 ? -1 : 1;` and target uses p.cx; vanilla always uses player[target]. Fine.

7. Check moonLeech: ours `const head = enemies(game).find(n => n.id === Math.floor(e.ai0) - 1 ...)` — vanilla `|ai[0]| - 1`. If ai0 negative → ours floor(-x)-1 wrong, but spawner passes positive. Where is the leech spawned in our code? bossAI_duke_moonlord (moonLordHeadAI spawns 456 projectiles; the 456 projectile spawns NPC 401 with ai0 = -(headId+1) or +(headId+1)?). Vanilla: NPC 401 spawned by Projectile 456 with ai[0] = npc head whoAmI + 1 (positive) — actually vanilla 456 AI: NewNPC type 401, then npc.ai[0] = projectile.ai[1] + 1? Something like that; the Abs in the leech AI is defensive. Let me check our 456 implementation quickly to see what ai0 it passes.

Actually let me grep for where NPC 401 is spawned in our codebase.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:34.547Z · glm-x-preview-260804

```
已验证爆炸盒。我来检查一下我们的代码中是如何生成水蛭 NPC 401 的（ai0 符号），以及模仿者的 state-4 细微差别。
```


---

## 🤖 Assistant · 2026-08-19T03:19:35.197Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"401\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts | head -10",
 "description": "Find leech NPC 401 spawn site"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:35.268Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts:973: *  于玩家处召 NPC 401,ai[0]=头 whoAmI+1 / ai[1]=源弹 456 索引。
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts:980:  const leech = spawnPart(game, head, 401);
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts:1546:      // :37828-37842 lt=120/180/240 于玩家处召 401 月噬怪(门禁说明见 spawnMoonLeech)
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts:1609:    // :37975-37989 inSlot=120/180/240 于玩家处召 401 月噬怪(门禁说明见 spawnMoonLeech)

```


---

## 🤖 Assistant · 2026-08-19T03:20:20.316Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
ai0 = head whoAmI + 1 (positive). Good, matches ours.

Now — let me scrutinize a couple more high-risk spots:

A. moonLordFreeEyeAI slot loop translation:
```js
let slot = 0, consumed = 0, dur = 0;
for (; slot < 10; slot++) {
  dur = ML_EYE_ATTACKS[slot][1];
  if (!(dur + consumed <= e.ai1)) break;
  consumed += dur;
}
```
Vanilla:
```
num1297=0; num1298=0;
for (; num1297 < 10; num1297++) {
  num1295 = arr[1, num1297];
  if (!(num1295 + num1298 <= ai[1])) break;
  num1298 += (int)num1295;
}
```
Identical. t = ai1 - consumed. Good.

B. Verify a numerically suspicious bit in free eye state 3: `(t - 45) % 40 === 0` for ai2 *= 0.95: vanilla `(num1294 - 15 - 30) % 40 == 0`. Same.

C. Free eye state 3: ours sets `x[0] += e.ai2` each tick in [45,185). Vanilla localAI[0] += ai[2]. OK.

D. In free eye state 4 charging (t<180): vanilla returns early if num1294 < 60 → `if (!(num1294 >= 60)) return;` — hmm, that's inside the t<180 branch AFTER velocity damping. Vanilla:
```
if (num1294 < 180) {
  localAI[2] lerp 1
  localAI[1] -= 0.05
  velocity *= 0.95; if len<1 → zero
  if (!(num1294 >= 60)) return;    // ← RETURNS - skips fly()? 
  ... dust ...
}
```
Wait — `return` exits AI_081 entirely! In vanilla, does returning skip movement? Yes — but wait, this is inside `else if (aiStyle == 81) { ... }` — a `return` from UpdateNPC? This is inside the big AI switch function (private void AI()?). A `return` there skips the REST of AI() but the movement integration happens in UpdateNPC after AI() returns... Hmm, actually no. Let me think about vanilla structure: NPC.UpdateNPC calls this.AI(); AI() contains the giant switch. Movement (velocity → position) happens inside AI() in the shared sections (e.g., the "flag3" tile collision or direct integration at the end of AI()). Actually in Terraria's NPC.cs, position integration happens inside AI() (the big method), in sections after the aiStyle switch — e.g. around :91400 per our comments ("UpdateNPC :91400 段共享位移"). If AI() returns early, does integration still happen? 

The `return` statements are inside `AI()` itself. If integration is in AI() after the switch... then early return would skip movement. But wait — for the Moon Lord free eye with noTileCollide=true, hmm. Actually I recall in decompiled Terraria, AI() is the giant method and the movement code IS inside it after the aiStyle switch. Early `return` skips it. E.g., aiStyle 87 state 7 has `return`-like flows... hmm no.

But for our audit, the relevant thing is what OUR code does: in state 4 t<180, ours does damping + particles, and at the end of the function calls fly(e) unconditionally (except the early despawn returns). Vanilla: for t < 60, return skips... what exactly? If vanilla skips movement integration on those ticks, the eye would freeze while velocity is being damped to zero anyway (velocity *= 0.95 → movement still occurs in vanilla if integration happens). Since velocity → ~0 quickly, the difference is negligible. Not worth reporting.

E. bigMimic: `if (e.ai0 < 0 || e.ai0 > 8) { e.ai0 = 0; ... }` — aiStyle 87 states include 4.1 (float). e.ai0 > 8 covers. OK.

F. Mothron state 4 search: ours caps the loop at 1000 iterations — vanilla 1000 too. OK.

G. Mothron: `if (e.ai0 < -1 || e.ai0 > 4.2) e.ai0 = 0;` — includes 4.1/4.2. OK.

H. babyMothron: `if (e.ai0 < -1 || e.ai0 > 2.1) e.ai0 = 0;` — includes 2.1. OK.

I. granite state 0: `if (e.ai0 === 0)` runs the vision check, but ours reads `if (los) { e.ai0 = 1; return; }` — WAIT. Ours:

```js
if (e.ai0 === 0) {
    if (los) { e.ai0 = 1; return; }
    ...
```
Vanilla: `if (CanHit) { ai[0] = 1; return; }` — wait, vanilla has `return`?? Let me re-check:

```
else if (this.ai[0] == 0f)
{
    TargetClosest();
    if (Collision.CanHit(...))
    {
        this.ai[0] = 1f;
        return;
    }
    ...
```
Hmm, vanilla RETURNS after setting ai[0]=1. That means the NPC doesn't move this tick (skips integration). Ours also returns. Match!

J. starCell state 0: vanilla sets ai[0]=1 WITHOUT return:
```
if (this.ai[0] == 0f)
{
    TargetClosest();
    if (Collision.CanHit(...))
    {
        this.ai[0] = 1f;
    }
    else { ... }
}
```
No return — falls through to... wait, this is an if/else-if chain: state 0 block ends, then `if (type == 405)` tail block. Since ai[0] was set to 1 this tick, the else-if for state 1 does NOT run this tick. Vanilla continues to the tail (rotation/separation) and movement. Ours: `if (e.ai0 === 0) { if (los) { e.ai0 = 1; } else {...} }` then falls to `if (flyPhase) fly(e); else moveAndCollide(...); starCellTail(...)`. Matches.

K. Now — the mimic issue: also check state 5's condition `if (p && Math.hypot(dx, dy) < 200 && !inSolidBody(game, e))` — dy here includes the -4. Vanilla: vector246 includes Y -= 4 then Length() < 200. Ours computes dx/dy including -4, then re-uses them for movement. Vanilla same vector. Match.

L. Nebula floater: ours `if (e.justHit) lai[1] = 1;` then immediately `if (lai[1] === 1) { lai[1] = 0; if (rnd(6)===0) e.ai0 = TP_T; }`. Vanilla: StrikeNPC sets localAI[1]=1 (outside AI); AI reads it. Equivalent.

M. Nebula floater dissolve: vanilla `if (this.ai[1] == 1f) { if (localAI[3] == 0) { localAI[3] = 1; ai[3] = 3; sound; dust } ai[3]--; if (ai[3] <= 0) active = false; return; }` — note: ai[3] = 3 then ai[3]-- → 2; then next ticks 1, 0 → dies on the 4th tick? T: set 3→2. T+1: 1. T+2: 0 → active=false. So dies 3 ticks after start. Ours: lai3==0 → set 1, ai3 = 3; ai3 -= 1 → 2; if (ai3 <= 0) dead. Same sequence → dies at ai3=0 on third decrement. Match.

N. Ours: `if (!p) { e.ai0 = 0; e.ai1 = 1; ... }` — then the dissolve check `if (e.ai1 === 1)` runs same tick. Vanilla: same order (sets ai[1]=1 then the dissolve branch later in same tick — wait, in vanilla the dead-player check happens BEFORE `if (this.ai[1] == 1f)`? Order in vanilla: TargetClosest; if dead → set ai [0,1,0,0]; rotation; spriteDirection; vector279/280; flag103; flag104; `if (ai[1] == 1) {dissolve; return}`. Yes same-tick dissolve entry. Ours matches.

O. starCell 421 state 1: ours `const is421 = e.vanillaId === 421; const tx = p.cx - e.cx, ty = (is421 ? p.y : p.cy) - e.cy;` — vanilla: vector236 = player.Center - Center; if 421 → player.Top - Center. Top = (cx, y). So ty = p.y - e.cy. Matches.

P. starCell state 1 attach: `e.x = p.cx - e.w / 2; e.y = p.y - e.h;` vs vanilla Center = player.Top → e.y = p.y - e.h/2. Deviation of h/2 — worth listing as minor. Actually let me double check: `base.Center = Main.player[target].Top;` — Center is the NPC's center = position + size/2. So position.Y = Top.Y - height/2. Ours: e.y = p.y - e.h → center at p.y - e.h/2 → off by h/2 above. For NPC 421 (h = 22?), 11px. Also state 5 ours: `e.y = p.y - e.h / 2` → center at p.y → matches vanilla state 5 (Center = Top + (dir*4,0) → e.y = p.y - h/2). Wait — state 5 in ours: `e.y = p.y - e.h / 2;` → e.cy = p.y. Vanilla state 5: Center = Top + (dir*4, 0) → Center.Y = p.y → e.cy = p.y → e.y = p.y - h/2. Match. But state 1→5 transition: vanilla Center = player.Top → e.cy = p.y too! Both are Center = Top. So state-1 attach in ours (e.y = p.y - e.h → e.cy = p.y - e.h/2) is WRONG vs state 5 (e.cy = p.y). One-tick visual offset only, since state 5 corrects next tick. Trivial. Skip.

Q. Mimic state 2: `const hpFrac = e.hp / e.maxHp;` — vanilla life/lifeMax. OK.

R. Mothron egg AI gravity: ours adds GRAVITY (0.3?) — vanilla gravity for 478 is the default (0.3? NPC default gravity 0.3 with maxFall 10). Our GRAVITY constant and MAX_FALL_SPEED used broadly. Fine.

S. mothronEgg: `if (e.vy === 0) { vx *= 0.9; spin += vx*0.02 } else { vx *= 0.99; spin += vx*0.04 }`. Vanilla identical.

Now, let me re-examine the free eye deathray damage 50*2 and whether our Arrow/MLDeathray damage application convention doubles. In this repo, hostile projectile damage: vanilla NewProjectile 462 dmg 35 → ours shootL passes 35 directly. So the ×2 only for 455 (deathray): 50 → 100. Is there an internal convention where MLDeathray damage gets halved somewhere? Let me check how MLDeathray applies damage in fixedUpdate.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:20.685Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1038,1100p' ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_duke_moonlord.ts",
 "description": "Read MLDeathray fixedUpdate damage application"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:20.727Z

**📎 ToolResult**

```
  }

  /** scale 上限:头 1.0 / 真眼 0.4(:30468-30478 num728) */
  private get maxScale(): number { return this.kind === 'head' ? 1 : 0.4; }

  fixedUpdate(_dt: number, game: GameHooks): void {
    // v6 近似收紧①：束角回写——快照把房主实时角度放在 vx/vy 通道（exVx/exVy），
    // 傀儡消费式同步（读后清零防下一 tick 重复回拉振荡）；快照间隙内本地按扫速
    // 自推插值。后台页暂停恢复后由下一快照纠偏（此前只按首帧角自推会永久漂移）
    if (this.netPuppet && (this.vx !== 0 || this.vy !== 0)) {
      this.angle = Math.atan2(this.vy, this.vx);
      this.vx = 0; this.vy = 0;
    }
    // v6 联机：傀儡端按 netId 找锚（msg23 傀儡）；本端真身按本地 id
    const src = this.srcNetId
      ? (game.enemies() as Enemy[]).find((n) => n.netId === this.srcNetId)
      : (game.enemies() as Enemy[]).find((n) => n.id === this.srcId);
    if (!src || src.dead) { this.dead = true; return; }        // 源消亡即 Kill(:30297)
    if (!this.netPuppet && this.kind === 'head' && src.ai0 === -2) { this.dead = true; return; } // :30296 头闭眼残肢（ai0 不同步,傀儡跳过——msg28 兜底）
    this.age++;
    if (this.age >= 180) { this.dead = true; return; }         // :30472 寿命 180t
    this.angle += this.sweep;                                  // :30521 rotation += ai[0]

    // 锚点:束原点 = 源心 + 眼球椭圆偏移(:30293-30308)
    const hx = headOf(src);
    const open = this.kind === 'head' ? hx.l1 : 1;
    const eyeA = this.kind === 'head' ? hx.l0 : this.angle;    // 真眼无独立瞳角,随束角
    const ex = this.kind === 'head' ? Math.cos(eyeA) * 27 * open : Math.cos(eyeA) * 30;
    const ey = this.kind === 'head' ? Math.sin(eyeA) * 59 * open : Math.sin(eyeA) * 30;
    this.x = src.cx + ex - this.w / 2;
    this.y = src.cy + ey - this.h / 2;

    // 束长:LaserScan 3 采样(线宽 36·scale,最大 2400)均值,:30483-30509
    const scale = Math.min(this.maxScale, Math.sin((this.age * Math.PI) / 180) * 10 * this.maxScale);
    const wSq = 36 * scale;
    const dirX = Math.cos(this.angle), dirY = Math.sin(this.angle);
    let amt = 0.5;
    let dist = this.laserScan(game, dirX, dirY, wSq);
    const p = game.player;
    if (this.kind === 'head' && p && !p.dead && !losClear(game, this.cx, this.cy, p.cx, p.cy)) {
      // :30511-30519 头与玩家无视线 → 束长取 距玩家+150(防隔墙盲射)
      dist = Math.min(2400, Math.hypot(p.cx - src.cx, p.cy - src.cy) + 150);
      amt = 0.75;
    }
    this.len = lerp(this.len, dist, amt);

    // 命中:玩家矩形 vs 束线段(线宽 36·scale),伤害走 damagePlayer(iframes 节流)。
    // 弹幕命中：attacker 仅做死亡归因，contactOnly 缺省 false → 荆棘不反伤
    // （反伤只在 NPC 接触分支 Player.cs:30910-30944）
    if (p && !p.dead && segHitsRect(this.cx, this.cy, dirX * this.len, dirY * this.len, wSq, p)) {
      game.damagePlayer(this.dmg, this.cx, this.cy, src);
    }
  }

  /** Collision.LaserScan 近似:垂直束向 ±半宽 3 条采样线,8px 步进至首实心块 */
  private laserScan(game: GameHooks, dirX: number, dirY: number, width: number): number {
    const px = -dirY, py = dirX; // 垂直束向
    let sum = 0;
    for (let k = -1; k <= 1; k++) {
      const off = (k * width) / 2;
      const ox = this.cx + px * off, oy = this.cy + py * off;
      const steps = Math.ceil(2400 / 8);
      let d = 2400;

```


---

## 🤖 Assistant · 2026-08-19T03:20:35.382Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
MLDeathray applies `game.damagePlayer(this.dmg, ...)` directly with this.dmg. So passing 50*2 = 100 means the player takes 100 per hit vs vanilla 50 per hit. That's 2x damage. UNLESS damagePlayer internally halves... Unlikely. Hmm — but is there a hit-rate difference: vanilla 455 damage 50, but in expert mode... our EXPERT is false. In normal mode vanilla does 50 per tick with player i-frames limiting rate. Ours: 100 with iframes. This is a 2x damage deviation on the free-eye deathray — BUT the core ('core' kind from moon lord core 398 in duke_moonlord) also passes 50*2, and head 75*2 (vanilla head 455 = 75? check :37902-37916: NewProjectile 455, 75? Let me verify quickly).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:36.110Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '37895,37920p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; grep -n \"damagePlayer\" ~/Project/GLM/SandboxWorld/game/src/Game.ts | head -3",
 "description": "Check vanilla head deathray damage and damagePlayer"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:36.176Z

**📎 ToolResult**

```
							Main.dust[num1277].scale = num1276;
							Main.dust[num1277].customData = this;
						}
					}
				}
				else if (num1260 < num1261 - 15f)
				{
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
ugrep: warning: ~/Project/GLM/SandboxWorld/game/src/Game.ts: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T03:21:16.259Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Vanilla head deathray = 75 damage; ours mlDeathray 'head' = 75*2 = 150; free eye / core = 50 → ours 100. So there's a consistent ×2 in the moonlord file. This suggests a deliberate project convention (perhaps compensating vanilla's expert scaling, or a design decision). Since the core variant was already audited in a previous batch (memory: "全Boss三维总审计批" and moonlord port), and our file merely mirrors the same 50*2, it's consistent with the audited baseline. I'll not report it as a CONFIRMED deviation but mention it as a note (consistent ×2 convention, if unintended it applies to all three).

Actually wait — let me quickly check where damagePlayer lives and whether it halves. Game.ts path may differ. Not critical — the ×2 is consistent across all 455 spawns in the codebase (75*2 head from audited file). I'll flag as a note.

Now let me do a final check on a couple of details I haven't verified:

1. `spawnPart` semantics — child spawn positions are set after; fine.

2. cultistTabletAI init gate: ours uses bInit (once). Vanilla uses localAI[3]==0 → set to 1 → once. But vanilla checks `localAI[3] == 0f && Main.netMode != 1` — after the first block localAI[3]=1 forever. Equivalent.

BUT — one difference: vanilla's init block is INSIDE `if (type == 437)` and the countdown/anitm happen every tick. Ours equivalent.

3. Ours tablet: `if (!pts) { e.dead = true; return; }` — vanilla: life=0; HitEffect; active=false. Match (silent despawn — vanilla HitEffect with life=0? HitEffect() with default args plays no sound? It spawns death dust/gore maybe. Ours: silent. Vanilla HitEffect() spawns gore for 437? Possibly none since type 437 has no gore... fine).

4. LunaticDevotee: vanilla `if (num1365 != direction)` — note num1365 could be 0 (same X) → vanilla sets direction = 0? `direction = (spriteDirection = num1365)` — if sign is 0, direction becomes 0. Ours: `if (dir !== 0 && dir !== e.facing)` — skips when dir==0. Vanilla would set direction=0 (sprite flips to 0 = facing... 0 means facing left?). Minor. Vanilla Math.Sign(0) = 0 → direction = 0. Actually in vanilla that means the devotee faces "0" which renders as facing right? direction 0 is unusual. Ours keeps last facing. Trivial.

5. Flow invader: ours missing TargetClosest / no dead-player handling: `const p = player && !player.dead ? player : null; if (p) {...}` — if no player: velocity unchanged, still moves with moveAndCollide. Vanilla targets stale player. Fine.

6. flowInvader throws 539 every 70t: vanilla `if (!((this.ai[0] += 1f) >= 70f)) return; this.ai[0] = 0f;` → at 70, resets and throws. Ours: `e.ai0 += 1; if (e.ai0 < 70) {...move; return;} e.ai0 = 0; ...throw; move`. Matches.

7. LunarOrb: `if (this.life-- <= 0) { explode; return; }` — 539: vanilla timeLeft for 539? SetDefaults probably timeLeft=600. When timeLeft hits 0 → Kill() → the Kill() override does the explosion. Ours: life 600 → explode. OK. For 574: timeLeft = 2 every tick while parent alive (never expires); if parent dead → Kill() (574 flag49 → Kill, no explosion — 574 has no type 539 explosion branch in Kill). Ours: 574 dead=true when parent dead (no explode). Match.

8. LunarOrb orbit: ours `if (this.ai0 < orbitT && alive)` — orbit while alive. Vanilla: if parent inactive → ai0 = num851 (jump straight to fire) for 539. Ours: for 539, if parent dead: `alive=false` → skips orbit AND skips the `ai0 === orbitT` fire branch (since ai0 keeps incrementing past orbitT... wait: `if (this.ai0 < orbitT && alive)` false; `else if (this.ai0 === orbitT)` — if parent died early, ai0 < 210 → the === check false → for 539 nothing happens (coasts with current velocity until tile hit). Vanilla: parent dead → ai0 = 210 (immediately charges at nearest player). Ours: coasts with old velocity until it hits a tile or expires (600t). Deviation: 539 whose parent 407 died doesn't retarget/charge; it drifts. Minor-moderate. Vanilla behavior: charge at player. Impact: orphaned orbs drift harmlessly instead of homing. Worth listing as a low/mid finding? It's an edge case (parent dies while orb orbiting — happens often in tower clears actually! Player kills 407s while orbs orbit). The orbs then never charge — noticeable. I'd list it as a minor/medium.

Hmm wait, let me re-read our code:

```js
this.ai0 += 1;
if (this.life-- <= 0) { this.explode(game); return; }
if (this.ai0 < orbitT && alive) {
  ...orbit...
} else if (this.ai0 === orbitT) {
  ...fire/charge...
}
```

If parent dies at ai0=50: alive=false → first branch false; `this.ai0 === orbitT`? 50 !== 210 → false. Next tick ai0=51... when ai0 reaches 210: `ai0 < orbitT && alive` false (alive still false); `ai0 === orbitT` TRUE → charge branch runs → for 539: charges toward player! So the orb DOES charge when ai0 reaches 210 — just 160 ticks later than vanilla. Vanilla charges immediately (ai0 set to num851). So deviation: delayed charge (up to ~2.6s) for orphaned orbs. Minor.

Also for 539 with alive parent — vanilla orbit uses oldPos[1] (2 frames back)? `base.position += Main.npc[num856].position - Main.npc[num856].oldPos[1]` — ours uses parent.x - parent.prevX (1 frame). Sub-pixel. Fine.

9. crawltipede: ours `if (groundRow > 0)` — vanilla `if (num51 > 0)`. Note vanilla breaks outer loop only `if (num51 > 0)`. Ours matches. Note: vanilla num51 = tile row of first solid; `num51 *= 16` → hover = row*16 - 800. Ours: hoverY = groundRow * TILE - 800. Match. And `player.y > hoverY` uses player TOP. Ours player.y = top. Match.

10. crawltipede: ours "同族头分离" modifies tx/ty by sepPush — vanilla modifies num49/num50. Match. Note vanilla vector5.Normalize() * num61 — with num61=1000: num49 -= vector5.X etc. Ours: `tx -= ((o.cx - e.cx)/d) * sepPush`. Match.

11. crawltipede speed clamp BEFORE separation — vanilla order: clamp velocity band, then separation modifies target. Ours: clamp, then separation. Match.

12. crawltipede: ours quantization `Math.floor(tx / TILE) * TILE - Math.floor(e.cx / TILE) * TILE` — vanilla `(int)(num49/16)*16` (trunc) then center quantized too, subtracted. Ours quantizes both target and self-center then diffs. Match modulo trunc-vs-floor (positive coords → identical).

13. crawltipede want velocity: `const ax = Math.abs(dxq), ay = Math.abs(dyq);` — vanilla num66/num67 computed AFTER num49/num50 scaled by num68 = num46/num63?? Let me re-check: vanilla computes num63 = sqrt(num49²+num50²); num66 = |num49|; num67 = |num50|; num68 = num46/num63; num49 *= num68; num50 *= num68. So num66/num67 are the UNSCALED absolute deltas, while want velocity = scaled to num46. In ours: `const ax = Math.abs(dxq), ay = Math.abs(dyq);` (unscaled) and `wantX = (dxq/dist)*num46` (scaled). Comment says "均匀缩放下比较不变" — comparing ax>ay with unscaled values is equivalent to comparing scaled |wantX|>|wantY|. Match.

14. The steering: vanilla condition `(velocity.X > 0 && num49 > 0) || ...` uses the SCALED num49/num50 (= want velocity). Ours uses wantX/wantY. Match. Then inner: `if (velocity.X < num49) velocity.X += num47;` — vanilla adds num47 toward want (not clamped at want!). Ours: `if (e.vx < wantX) e.vx += step; else if (e.vx > wantX) e.vx -= step;` Match.

15. Segments: `s.vx = 0; s.vy = 0;` vanilla velocity = Vector2.Zero. Match.

16. Head `e.facing = e.vx > 0 ? 1 : -1` — vanilla head spriteDirection: there's a block somewhere... fine.

OK. Now let me also verify the claimed ritualCheckFloor against CultistRitual.cs.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:16.530Z · glm-x-preview-260804

```
现在对比 `CultistRitual.cs` 验证 `CheckFloor`。
```


---

## 🤖 Assistant · 2026-08-19T03:21:17.338Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '80,130p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/CultistRitual.cs 2>/dev/null || find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"CultistRitual*\" 2>/dev/null",
 "description": "Read vanilla CultistRitual CheckFloor"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:17.391Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Events/CultistRitual.cs

```


---

## 🤖 Assistant · 2026-08-19T03:21:27.741Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '80,130p' ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent.Events/CultistRitual.cs",
 "description": "Read CheckFloor from CultistRitual.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:27.790Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent.Events/CultistRitual.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T03:21:33.928Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '60,130p' '~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent.Events/CultistRitual.cs'",
 "description": "Read CheckFloor from CultistRitual.cs correct path"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:34.021Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent.Events/CultistRitual.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T03:21:41.898Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/ | head; find ~/Project/GLM/SandboxWorld/Terarria1456 -name \"CultistRitual.cs\" | head -3",
 "description": "Locate CultistRitual.cs exact path"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:41.995Z

**📎 ToolResult**

```
app.ico
app.manifest
BCrypt.Net
Microsoft.Xna.Framework.RuntimeProfile
nativefiledialog.cs
Properties
Terraria
Terraria.Achievements
Terraria.Audio
Terraria.Chat
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Events/CultistRitual.cs

```


---

## 🤖 Assistant · 2026-08-19T03:21:55.623Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The find earlier said `~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.GameContent.Events/CultistRitual.cs` — but sed said no such file. Odd. Maybe there's a special character. Let me use the find output directly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:55.642Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && f=$(find . -name \"CultistRitual.cs\" | head -1) && echo \"$f\" && sed -n '60,130p' \"$f\"",
 "description": "Read CheckFloor via find-resolved path"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:55.708Z

**📎 ToolResult**

```
./Terraria.GameContent.Events/CultistRitual.cs

	public static bool TrySpawning(int x, int y, bool force = false)
	{
		if (x < 0 || y < 0 || x >= Main.maxTilesX || y >= Main.maxTilesY)
		{
			return false;
		}
		if (!force && (WorldGen.PlayerLOS(x - 6, y) || WorldGen.PlayerLOS(x + 6, y)))
		{
			return false;
		}
		if (!CheckRitual(x, y, force))
		{
			return false;
		}
		NPC.NewNPC(new EntitySource_WorldEvent(), x * 16 + 8, (y - 4) * 16 - 8, 437);
		return true;
	}

	private static bool CheckRitual(int x, int y, bool force = false)
	{
		if (!force && (delay != 0 || !Main.hardMode || !NPC.downedGolemBoss || !NPC.downedBoss3))
		{
			return false;
		}
		if (y < 7 || WorldGen.SolidTile(Main.tile[x, y - 7]))
		{
			return false;
		}
		if (!force && NPC.AnyNPCs(437))
		{
			return false;
		}
		Vector2 center = new Vector2(x * 16 + 8, y * 16 - 64 - 8 - 27);
		Point[] spawnPoints = null;
		if (!CheckFloor(center, out spawnPoints))
		{
			return false;
		}
		return true;
	}

	public static bool CheckFloor(Vector2 Center, out Point[] spawnPoints)
	{
		Point[] array = new Point[4];
		int num = 0;
		Point point = Center.ToTileCoordinates();
		for (int i = -5; i <= 5; i += 2)
		{
			if (i == -1 || i == 1)
			{
				continue;
			}
			for (int j = -5; j < 12; j++)
			{
				int num2 = point.X + i * 2;
				int num3 = point.Y + j;
				if ((WorldGen.SolidTile(num2, num3) || TileID.Sets.Platforms[Framing.GetTileSafely(num2, num3).type]) && (!Collision.SolidTiles(num2 - 1, num2 + 1, num3 - 3, num3 - 1) || (!Collision.SolidTiles(num2, num2, num3 - 3, num3 - 1) && !Collision.SolidTiles(num2 + 1, num2 + 1, num3 - 3, num3 - 2) && !Collision.SolidTiles(num2 - 1, num2 - 1, num3 - 3, num3 - 2))))
				{
					array[num++] = new Point(num2, num3);
					break;
				}
			}
		}
		if (num != 4)
		{
			spawnPoints = null;
			return false;
		}
		spawnPoints = array;
		return true;

```


---

## 🤖 Assistant · 2026-08-19T03:22:55.901Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
CheckFloor: `for (int i = -5; i <= 5; i += 2)` → i ∈ {-5, -3, -1, 1, 3, 5}, skip -1 and 1 → {-5, -3, 3, 5}. Ours `for (const i of [-5, -3, 3, 5])`. Match. i*2 offset. j from -5 to 11. Floor = SolidTile || Platforms. Clear condition: `(!SolidTiles(x-1..x+1, y-3..y-1) || (!SolidTiles(x..x, y-3..y-1) && !SolidTiles(x+1, y-3..y-2) && !SolidTiles(x-1, y-3..y-2)))`. Ours: clearMid = !solidRect(x-1, x+1, y-3, y-1); clearSide = !solidRect(x,x,y-3,y-1) && !solidRect(x+1,x+1,y-3,y-2) && !solidRect(x-1,x-1,y-3,y-2); if (clearMid || clearSide). Match exactly.

Great — ritualCheckFloor is 1:1.

Now remaining items to check before writing findings:

1. Confirm EXPERT constant claim: "本工程恒 false,Game.ts expertMode:false" — fine.

2. bigMimic state 4.1 bug — CONFIRMED. Let me also double-check the mimic state 4→4.1 vy: state 4 sets `e.vx = tx; e.vy = ty` (speed 8 toward player). Vanilla: velocity = vector245 (speed 8 toward player). Match.

3. Now the mimic bug #2 candidate: In state 4.1 first branch, after ai1 > 10 → state 2 or 5. Vanilla checks SolidCollision(position) → 5. Ours inSolidBody. Match.

4. Another check on mimic state 2: the air branch (`else`) runs when `!(e.onGround && e.vy === 0)`. Vanilla `velocity.Y == 0f`. Subtle: vanilla grounded branch is `if (velocity.Y == 0f)` — no onGround requirement. Ours requires onGround && vy===0. In our engine, could vy be 0 while airborne (apex of jump)? vy passes through 0 at jump apex → ours would apply the grounded branch (friction, ai1++, jump) mid-air at apex! Vanilla also would (velocity.Y == 0f at apex). Both share this quirk. Ours adds onGate requirement which PREVENTS the quirk (onGround false at apex). So ours is stricter — vanilla at vy==0 apex does the grounded logic. Ha — vanilla's quirk mostly doesn't matter since vy==0 exactly for a frame is rare with float integration. Ours safer. Fine.

5. Mothron 180t pick: ours `else if (pick === 1) e.ai0 = 3; else if (count < eggCap) e.ai0 = 4;` — vanilla: case 1 → 3; case 2 → if count < 7 → 4 (else stays 0, re-roll). Ours: pick===2 → else-if count<cap → 4 else stays 0. And pick===0 without LOS → stays 0. Vanilla would re-roll same tick; ours waits 180t. Documented in code ("单帧一次近似"). Minor.

6. Mothron: the >3000px → ai0=-1 missing (flee). Also babyMothron same. Both minor; combine into one finding: "Mothron 族缺 >3000px 脱战爬升门".

7. Egg hatch clamp clobber — combined into a minor note? It changes hatch timing. Eh. Let me evaluate: `if (e.ai0 < 0) e.ai0 = 0` at top. vanilla keeps negative. This resets accumulated delay. Effect: hitting eggs early doesn't extend hatch time; vanilla up to +40t/hit. Low severity. List as minor if room.

8. LunarOrb orphan charge delay — minor.

9. flowInvader: 407/408 vanilla has TWO types sharing aiStyle 96 — check vanilla SetDefaults... The claim: 408 has no spawn source; fine.

10. starCell state 0: ours checks `Math.hypot(dx, dy) > 800` where dy includes -h/4. Vanilla num1366 = length of vector234 (with -h/4). Match.

11. starCell state 2: `if (d < 600 && !touchesSolid(game, e))` — vanilla `num1371 < 600 && !SolidCollision(position, width, height)`. touchesSolid default inflate=0 with (x-0.01) — approximately the hitbox. Match.

12. starCell state 4 anchor retry: ours requires `!touchesSolid(game, e, 10)` (inflate 10) — vanilla `!SolidCollision(position - (10,10), width+20, height+20)`. Match.

13. nebulaFloater teleport: `if (hover && Math.hypot(e.vx, e.vy) < 2) lai[0] += 1;` — vanilla `if (flag104 && velocity.Length() < 2f && netMode != 1)`. Match.

14. nebulaFloater orbs delayed when negative — ours unconditional. Comment claims flag105 恒假 — actually flag105 = true unless an orb has ai[0] < 0. Orb ai[0] CAN go negative: vanilla orbs get `ai[0] -= 30` on teleport; a freshly-reset orb (just fired, ai0=0) receiving -30 → -30 < 0 → NEXT teleport skips. So vanilla gate is live in that edge. Ours: delay() can make ai0 negative, and we keep delaying every teleport. Difference: ours accelerates orbs more aggressively in repeated-teleport sequences. LOW.

Actually — hmm, wait. There's a subtlety: ours `delay(ORB_DELAY)` subtracts 30 from LunarOrb.ai0, and LunarOrb's `else if (this.ai0 === orbitT)` fires when EXACTLY equal. If ai0 goes negative (e.g., -30), it counts up: -30 → ... → 180 → fires. Vanilla projectile: ai[0] increments each tick; `if (ai[0] == num851)` — same exact equality. If negative, counts up to 180. Same behavior. OK.

15. The 574 fire: ours gate `canHitLine(...)`. Vanilla CanHitLine(Center 0,0 → player 0,0). Ours canHitLine(st, cx, cy, 0, 0, p.cx, p.cy, 0, 0). Match.

16. Free eye: `enemies(game).find(n => n.id === e.ai3 && n.vanillaId === 398)` — vanilla `Main.npc[(int)ai[3]].active && type == 398` — index by ai[3] directly. Ours by id — our Enemy.id ≈ whoAmI? In this repo, e.id is the entity slot id — used consistently (e.g., leech head lookup). Fine.

17. Leech: ours `if (e.ai2 >= LEECH_T)` heal — vanilla `>= num1321` (90). Ours LEECH_T=90, ai2 increments first. Vanilla ai[2]++ then check >= 90. Match.

18. Leech heal targets: vanilla heals num1327 = HEAD first (num1327 = num1322 = the head), then num1324 (core = head.ai[3]), then num1325 (hand ai2==0), num1326 (hand ai2==1). Ours order [head, core, hand0, hand1]. Match.

19. Leech heal amount: vanilla num1335 = num1329 + num1334 where num1334 = min(deficit - pool, 0) → amount = pool + min(deficit-pool, 0) = min(pool, deficit) when... if deficit < pool: pool + (deficit - pool) = deficit. If deficit >= pool: pool + 0 = pool. = min(pool, deficit). Ours same. Match. Also vanilla continues while pool > 0.

Also vanilla doesn't check target dead before healing (uses stale values); ours skips dead targets — fine (dead NPCs have no deficit anyway... actually dead NPC hp could be 0 → deficit = maxHp → ours would heal a DEAD npc if it were in the list. Ours: `if (!tgt || tgt.dead ...) continue`. Vanilla: heals regardless of active! Because Main.npc[num].life might be stale. Whatever — ours is the sane version; vanilla would heal a dead-slot NPC (which then... nothing). Not a real behavioral difference in practice since hands/core dead → their ai[3] anchor... skip.)

20. Leech: ours also handles `head.ai3` for core lookup: vanilla num1324 = (int)Main.npc[num1322].ai[3] — the head's ai[3] = core id. Ours: core = find(n.id === head.ai3 && vanillaId === 398). Match. Hands: vanilla scans for type 397 && ai[3] == num1324 (ai[3] = core id) with ai[2] 0/1. Ours: hands filter `n.ai3 === head.ai3` — hmm! Vanilla: hand.ai[3] == num1324 = head's ai[3] = CORE id. Ours compares n.ai3 === head.ai3 — if hands' ai3 = core id and head's ai3 = core id, equal. In our moonlord port, do hands have ai3 = core id? Presumably (that's how the port mirrors). OK.

21. Free-eye iframes=2 each tick — dontTakeDamage=true. OK.

22. Cultist tablet light — vanilla 437: AddLight(Center, 0.8, 0.75, 0.55). Ours matches.

23. Tablet: vanilla localAI[3] gate replaced by bInit — but ALSO vanilla tablet has `dontTakeDamage` from SetDefaults (invulnerable). Ours iframes=2. OK.

24. Tablet ai[3] countdown start: after cultist spawn sets ai[0] = -1, ai[1] = 0, ai[3] = 0. Next tick ai[3]++ → 1. Vanilla same. `> 300` → despawn. Match. Particle 526 at ai3%10==1 && ai3>120. Match.

25. BabyMothron: ours `if (e.ai0 === 0 || e.ai0 === 1)` separation — vanilla same states. Match.

26. BabyMothron state 0: ours missing `spriteDirection = direction` (facing). Fine.

27. babyMothron 2.1: `if (e.ai1 > 45) { if (!inSolidBody) → 0; else if (e.ai1 > 90) → 1 }` — vanilla: `if (ai[1] > 45) { if (!SolidCollision) {0} else if (ai[1] > 90) {1} }`. Match.

28. granite state 4 zero-velocity init: `const dx = p.cx - e.cx, dy = p.cy - p.h / 4 - e.cy;` — vanilla vector269 = player.Center - Center; vector269.Y -= player.height/4. Match.

29. granite state 3: ours `if (d < 1 || d > 800 || los)` — vanilla num1457 < num1458(1) || > 800 || CanHit. Match.

30. free eye state 0 target uses pcx/pcy which when no player falls back to e.cx/e.cy → dx,dy = 0 → atan2(0,0) = 0. Vanilla uses Main.player[target] (stale). Fine.

Now — one more important check: the mimic wake condition uses `e.vy > 100` — vanilla `velocity.Y > 100f`. OK.

Also mimic: `if (e.ai0 !== 7 && !p)` → 7. Vanilla `if (ai[0] != 7 && player.dead)` — with TargetClosest first. Ours !p covers dead. OK.

Now — the biggest remaining candidate: the free eye state 2's t<15 dust and t<75 particle counts are approximations. Fine.

Let me also double-check our moonLordFreeEyeAI state 2: `if ((t - 15) % 10 === 0)` fires 454 with speed 4 outward from vector223 — vanilla: vec4 = Normalize(vector223) (NaN → -UnitY) * 4. Ours: ux/uy from px/py with NaN-ish fallback -1 up. Wait ours: `const ux = d > 0.001 ? px / d : 0, uy = d > 0.001 ? py / d : -1;` — fallback (0,-1) = up. Vanilla fallback UnitY*-1 = up. Match (when |vector223| ~ 0 at hex center? fine).

Note k index: `const k = Math.floor((t - 15) / 10);` — t<75 → t-15 in [0,60) → k 0..5. Matches switch cases.

`const f = (t - 15) / 10 - k;` = fractional part. Vanilla: num1304 - (int)num1304. Match.

Dust 2/tick at Center+vector223 — ours 2 particles. Match-ish.

State 2 t in [105,120): ours plays Zombie_102 EVERY tick — vanilla plays every tick too (PlaySound inside the branch). Match. Hmm wait — actually vanilla plays sound EVERY tick in that 15-tick window? Yes: `SoundEngine.PlaySound(29, ..., 102);` is the first statement of the num1294 < 120 branch. OK ours matches.

Alright. Now let me quantify the mimic 4.1 bug impact more concretely and check whether some other code path moves mimics (e.g., a generic "noGravity false → gravity" tail in Enemy.update). Let me check the shared tail after AI dispatch in Enemy.ts (contact damage / despawn / etc.) to be sure there's no generic movement.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:22:56.584Z · glm-x-preview-260804

```
CheckFloor 已 1:1 复现。现在我来确认 Enemy.ts 中是否不存在会掩盖 mimic 4.1 问题的通用移动尾部逻辑。
```


---

## 🤖 Assistant · 2026-08-19T03:22:56.883Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '1300,1400p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read Enemy.ts shared tail after AI dispatch"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:56.904Z

**📎 ToolResult**

```
        case 61: santaNK1AI(this, game, p); break;                        // AI_061 圣诞坦克 346（cs:33902 悬浮+链炮/火箭/礼盒）
        case 62: elfCopterAI(this, game, p); break;                       // AI_062 玩具直升机 347（cs:34155 近距悬停点射）
        case 63: flockoAI(this, game, p); break;                          // AI_063 弗洛科 352（cs:34208 追踪+旋冲）
        case 38: snowmanAI(this, game, p); break;                         // AI_038 雪人三兄弟 143/144/145（cs:29115 跳扑/停顿/雪球）
        case 9: bouncingBallAI(this, game, p); break;                     // AI_009 弹跳球族 25/30/33/112/516/665/666（cs:21349 直飞球）
        // ---- 火星疯狂族 1:1（bossAI_martian.ts）----
        case 80: martianProbeAI(this, game, p); break;                    // AI_080 火星探测器 399（cs:38129 逃逸→StartInvasion(4)）
        case 76: martianSaucerAI(this, game, p); break;                   // AI_076 火星飞碟核心 395（cs:36322 600t 六窗口+部件生成）
        case 72: bubbleShieldAI(this, game, p); break;                    // AI_072 泡泡盾 384（cs:35318 锚军官 383）
        case 73: teslaTurretAI(this, game, p); break;                     // AI_073 特斯拉炮塔 387（cs:35340 部署渐显+180t 电击）
        case 74:                                                          // AI_074 火星无人机 388/日耀 Corite 418（cs:35452 悬浮→扑咬→自爆）
          if (this.vanillaId === 388 || this.vanillaId === 418) martianDroneAI(this, game, p);
          else this.floatEyeAI(game, p);                                  // 其余（一期近似档保留）
          break;
        case 75:                                                          // AI_075 飞碟部件 392/393/394 + 骑手 390（cs:35745 锚主体+攻击窗）
          if (this.vanillaId === 390 || this.vanillaId === 392
            || this.vanillaId === 393 || this.vanillaId === 394
            || this.vanillaId === 416 || this.vanillaId === 492) martianSaucerPartAI(this, game, p);
          else this.fighterAI(game, p);                                   // 其余（一期近似档保留）
          break;
        case 48: golemHeadAI(this, game, p); break;                       // AI_048 自由石巨人头 249（cs:31500,golemHeadAI 已含自由态分支）
        case 49: angryNimbusAI(this, game, p); break;                     // AI_049 愤怒云 250（cs:31742 悬顶淋雨 264）
        // ---- DD2/旧日军团 + 沙漠族（bossAI_dd2.ts）----
        case 93: flyingDutchmanAI(this, game, p); break;                  // AI_093 荷兰飞盗船 491（cs:40918 四炮部件+海盗跳舱+贴地巡航）
        case 102: sandElementalAI(this, game, p); break;                  // AI_102 沙尘精 541（cs:42224 walker 核+沙暴标记 658）
        case 103: sandSharkAI(this, game, p); break;                      // AI_103 沙鲨族 542-545（cs:42621 沙中巡游+跃沙扑咬,沙族豁免碰撞）
        case 104: dd2AttackerTestAI(this, game); break;                   // AI_104 DD2AttackerTest 547（cs:42807 出生即消）
        case 105: eterniaCrystalAI(this, game, p); break;                 // AI_105 永恒水晶 548（cs:42810 180t 双端放门+胜负演出）
        case 106: lanePortalAI(this, game, p); break;                     // AI_106 神秘传送门 549（cs:43063 出怪门节拍,事件依赖 DD2_EVENT_HOOKS）
        case 108: divingFlyerAI(this, game, p); break;                    // AI_108 飞龙 558-560/小妖魔滑翔怪 574-575（cs:65959 俯冲五态+自爆）
        case 109: darkMageAI(this, game, p); break;                       // AI_109 黑暗魔法师 564/565（cs:66392 walker+三连招 675/674/673）
        case 110: betsyAI(this, game, p); break;                          // AI_110 双足翼龙 551（cs:62266 八槽攻表+rotation 收敛）
        case 111: dd2LightningBugAI(this, game, p); break;                // AI_111 埃特尼亚荧光虫 578（cs:66799 悬停蓄电 682 电弧）
        case 113: this.windyBalloonAI(game, p); break;                    // AI_113 风气球 594（cs:48253 挂史莱姆 ai[0]=-999）
        case 125: this.balloonSlimeAI(game, p); break;                    // AI_125 笨笨气球史莱姆 686（cs:44009 漂浮悬停+爆裂解救）
        case 117: this.bloodNautilusAI(game, p); break;                  // AI_117 恐惧鹦鹉螺 618（cs:47488 血月钓鱼 Boss）
        case 119: this.dandelionAI(game, p); break;                      // AI_119 蒲公英 628（cs:43254 下风喷籽；非critter勿只登 critterWanderAI）
        case 126: this.statueMimicAI(game, p); break;                    // AI_126 雕像宝箱怪 690（cs:43760 伪装/唤醒/跳跃穿墙）
        default: this.zombieAI(game, p); break;                        // 其余家族待逐个移植
      }
    } else switch (this.key) {
      case 'slime_green':
      case 'slime_blue': this.slimeAI(game, hasPlayer ? player : null); break;
      case 'zombie': this.zombieAI(game, hasPlayer ? player : null); break;
      case 'demon_eye':
      case 'cave_bat': this.flyAI(game, hasPlayer ? player : null, 0.09); break;
      case 'servant_of_cthulhu': this.flyAI(game, hasPlayer ? player : null, 0.22); break;
      case 'eye_of_cthulhu': this.eocAI(game, player ?? null); break;
    }

    // ---- AI 家族外的三段恒走点光（与 AI 分发无关，原版各自独立方法）----
    this.updateNpcCastLights();
    this.updateNpcTrailLights();
    this.updateNpcDebuffLights();
    // 毁灭者族段光：原版 AI_037 每段独立发光，本仓身/尾 wormBody 跳过 AI 分发 →
    // 全族三 id（134/135/136）统一在此结算（含头，防与 destroyerAI 双写）
    if (this.vanillaId === 134 || this.vanillaId === 135 || this.vanillaId === 136) {
      destroyerSegmentLight(this, game);
    }

    // ---- EoW 出生渐显（AI_006 尾段 1:1，NPC.cs:52650-52670；须在 AI 分发后跑——
    //      原版位移门 `(position - oldPosition).Length() > 2` 量的是本 tick 位移，
    //      fixedUpdate 头部 prevX/prevY 在 AI 前采样）----
    // 门（:52650 原文为反写 return 表达式）：13 头恒过；14/15 身/尾须前段
    //   spawnAlpha < 85 才启动——渐显沿链向尾传播（头先现、段逐级跟上）。
    //   prev 链断（晋升中瞬时态）按头段放行，防残段卡全透明。
    // alpha>0 且存活（:52656-52664）：每 tick 2 颗 14 号腐化尘（noGravity/noLight、
    //   scale 2、尘 alpha 100——spawnParticles 紫尘近似，DustID.Corruption）。
    // 位移 >2px（:52666-52670）：spawnAlpha -42 钳 0——255→0 共 7 tick 现身。
    // ---- 幻影龙 454-459 出生渐显（AI_006 头段 :51379-51400 1:1）：头无条件 -42/t、
    //      身/尾须前段 spawnAlpha<85 沿链传播（无位移门——龙自传送圈直接成型）；
    //      渐隐期 dontTakeDamage + 每 tick 2 颗 228 紫尘（noGravity/noLight/scale 2）----
    if (this.vanillaId !== null && this.vanillaId >= 454 && this.vanillaId <= 459) {
      const prev = this.wormFollow;
      if (this.vanillaId === 454 || !prev || prev.spawnAlpha < 85) {
        this.dontTakeDamage = this.spawnAlpha > 0;    // :51381-51382
        if (this.spawnAlpha > 0 && this.hp > 0) {
          game.spawnParticles(this.x + Math.random() * this.w, this.y + Math.random() * this.h,
            '#A060E0', 2, 0, { life: 40, size: 2 });
        }
        this.spawnAlpha = Math.max(0, this.spawnAlpha - 42);
        if (this.spawnAlpha === 0) this.alphaFade = false;
      }
    }

    if (this.vanillaId !== null && this.vanillaId >= 13 && this.vanillaId <= 15 && this.alphaFade) {
      const prev = this.wormFollow;
      if (this.vanillaId === 13 || !prev || prev.spawnAlpha < 85) {
        if (this.spawnAlpha > 0 && this.hp > 0) {
          game.spawnParticles(
            this.x + Math.random() * this.w, this.y + Math.random() * this.h,
            '#8A62C0', 2, 0, { life: 40, size: 2 },
          );
        }
        if (Math.hypot(this.x - this.prevX, this.y - this.prevY) > 2) {
          this.spawnAlpha = Math.max(0, this.spawnAlpha - 42);
          if (this.spawnAlpha === 0) this.alphaFade = false;
        }
      }
    }

```


---

## 🤖 Assistant · 2026-08-19T03:24:29.534Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Confirmed: no generic movement after AI dispatch (only lights and alpha). So the mimic 4.1 freeze is real.

Now let me look at one more potential issue in mimic 4.1 — actually let me trace once more very carefully, because I want to present an accurate trigger:

Entry to 4.1 happens only from state 4 (ai1 > 6). At that moment vx/vy = speed-8 vector toward player (downward typically). Top-of-4.1:
1. `if (e.ai2 === 0 && p && losClear && !inSolidBody) e.ai2 = 1;` — ai2 is 0 (state 4 set ai2=0 when entering 4.1). So first tick: if LOS && not embedded → ai2 = 1.
2. vy += 0.2 (capped 16).
3. Branch A: `!p || y+h >= p.y || vy <= 0` — mimic is above player (state 4 hovered at cy < pcy-300) → y+h vs p.y: mimic 300+px above → false. vy = 8 > 0 → false. → Branch A false.
4. Branch B: `e.ai2 === 0` — false (set to 1 in step 1).
5. No movement. Frozen. vy grows +0.2/tick to 16. Position unchanged → conditions never change (unless player jumps up into the mimic or moves horizontally so that... note Branch A depends only on y+h >= p.y — player's Y. If the player GRAPPLES up or jumps 300px, could trigger. Otherwise stuck.)

So yes — mimic dive freezes mid-air whenever LOS was clear at dive start. This is a severe, common-path bug. But hold on — could `losClear` be false in the typical case? The mimic hovers 350px above the player through air — LOS almost always clear. So yes, common.

Hmm, actually wait. Let me reconsider: is state 4.1's Branch A perhaps meant to catch vy <= 0 quickly? vy starts +8 — no.

Double-check our claim about vanilla: in the ai2==1 aligned case with position above player and vy > 0, vanilla AI just does vy += 0.2 (nothing else) and noGravity stays false, noTileCollide stays false → shared movement integrates with collision. Yes.

So CONFIRMED finding #1 (severity: high).

Now, let me also double check one thing in state 4: the else-branch movement `e.vx = (e.vx * 5 + (dx / d) * 12) / 6;` — vanilla `vector245.Normalize(); vector245 *= 12; velocity = (velocity*5 + vector245)/6`. Match. And ai2==1 branch: vector245 = player.Center - Center (NOT the -350 target!), normalized *8. Ours: `if (e.ai2 === 1) { ... const dx = p ? p.cx - e.cx : ...; const dy = (p ? p.cy : e.cy) - 350 - e.cy;` — WAIT. Ours computes dy with -350 INSIDE the ai2===1 branch?

Let me re-read our state 4:

```js
} else if (e.ai0 === 4) {
    e.noGravity = true;
    if (p) e.facing = e.vx < 0 ? -1 : 1;
    const dx = p ? p.cx - e.cx : e.facing * 100;
    const dy = (p ? p.cy : e.cy) - 350 - e.cy;
    if (e.ai2 === 1) {
      e.ai1 += 1;
      const d = Math.hypot(dx, dy) || 1;
      const tx = (dx / d) * 8, ty = (dy / d) * 8;
      e.vx = (e.vx * 4 + tx) / 5; e.vy = (e.vy * 4 + ty) / 5;
      if (e.ai1 > 6) { e.ai0 = 4.1; ... }
    } else if (p && Math.abs(e.cx - p.cx) < 40 && e.cy < p.cy - 300) {
      e.ai1 = 0; e.ai2 = 1;
    } else {
      const d = Math.hypot(dx, dy) || 1;
      e.vx = (e.vx * 5 + (dx / d) * 12) / 6;
      e.vy = (e.vy * 5 + (dy / d) * 12) / 6;
    }
    fly(e);
  }
```

In the ai2===1 branch, ours uses dx/dy computed WITH the -350 offset. Vanilla ai2==1 branch REPLACES vector245 with `Main.player[target].Center - base.Center` (NO -350!) then normalize *8:

```
if (this.ai[2] == 1f)
{
    this.ai[1] += 1f;
    vector245 = Main.player[target].Center - base.Center;
    vector245.Normalize();
    vector245 *= 8f;
    velocity = (velocity * 4f + vector245) / 5f;
    ...
}
```

So ours aims at the player; vanilla's ai2==1 short-aim ALSO aims at the player (Center, no -350). Wait — ours dy includes -350! Ours: `const dy = (p ? p.cy : e.cy) - 350 - e.cy;` — this is the HOVER target (player - 350), used in the ai2===1 branch too. Vanilla ai2==1 aims at player CENTER directly. So ours' 6-tick "short aim" targets a point 350px ABOVE the player, while vanilla targets the player. Then at ai1 > 6, ours sets `e.vx = tx; e.vy = ty` = toward (player-350) — diving toward 350px above the player, NOT at the player!

Hmm wait — but then in 4.1, gravity +0.2 pulls it down... but as established, 4.1 freezes. Hmm, but if ai2 stayed 0 (no LOS), 4.1 flies through walls at velocity toward (player-350)? No wait — in state 4's ai2==1 branch exit: `e.vx = tx; e.vy = ty` where tx/ty = direction to (player-350) × 8.

Vanilla: direction to player × 8.

So CONFIRMED finding #2: mimic state 4 ai2==1 aim point wrong — should be player.Center (no -350). Effect: dive launches toward 350px above the player instead of the player. Combined with the 4.1 freeze this makes the whole dive sequence broken.

Let me re-verify ours once more from the file... From the earlier read (lines 679-698):

```
679	  } else if (e.ai0 === 4) {
680	    // ---- 飞天(:39639-39677):悬玩家上方 350px → ai[2]=1 短瞄 6t → 4.1 俯冲 ----
681	    e.noGravity = true;                                    // :39661 整态置位
682	    if (p) e.facing = e.vx < 0 ? -1 : 1;
683	    const dx = p ? p.cx - e.cx : e.facing * 100;
684	    const dy = (p ? p.cy : e.cy) - 350 - e.cy;
685	    if (e.ai2 === 1) {
686	      e.ai1 += 1;
687	      const d = Math.hypot(dx, dy) || 1;
688	      const tx = (dx / d) * 8, ty = (dy / d) * 8;
689	      e.vx = (e.vx * 4 + tx) / 5; e.vy = (e.vy * 4 + ty) / 5;
690	      if (e.ai1 > 6) { e.ai0 = 4.1; e.ai1 = 0; e.ai2 = 0; e.vx = tx; e.vy = ty; }
691	    } else if (p && Math.abs(e.cx - p.cx) < 40 && e.cy < p.cy - 300) {
692	      e.ai1 = 0; e.ai2 = 1;
693	    } else {
```

Yes: dx/dy include -350 and are used in the ai2===1 branch. Vanilla ai2==1 aims at player center. CONFIRMED.

Now finding #3 candidate — mothron missing 3000px flee (both 477 and 479). Vanilla: `if (target dead || dist > 3000) → ai[0] = -1` (climb & despawn-eligible). Ours: only !p. This is a missing despawn/flee gate. Report as low-medium.

Finding #4 candidate — egg hatch clamp clobber (`if (e.ai0 < 0) e.ai0 = 0` before justHit decrement). Wait, actually order:

```
979	  const hatchT = EXPERT ? 600 : 900;
980	  if (e.ai0 < 0) e.ai0 = 0;   // ← runs FIRST every tick
...
988	  if (e.justHit) {
989	    e.ai0 -= rndRange(10, 21);
990	    if (!EXPERT) e.ai0 -= rndRange(10, 21);
991	  }
992	  e.ai0 += 1;
```

Tick N: ai0 = 5, justHit → ai0 = 5-15-15 = -25. Tick N+1: clamp → ai0 = 0; then justHit may fire again → -30; +1. So ai0 oscillates around ≤0 until hits stop. Vanilla: ai0 accumulates negative freely. When does it matter? ai0 >= 675 for twitch; hatch at 900. Vanilla egg hit repeatedly early: hatch delayed by total subtraction; ours: delay bounded (ai0 floors at ~-40 → after last hit, 940 ticks). Actually the delay difference is tiny (bounded 40/hit... no: vanilla can accumulate unbounded negative, e.g., 10 hits → -300; ours resets to 0 each tick → effectively no accumulation → hatch ~900t after last hit sequence vs vanilla 1200t). Hmm — actually wait: ours clamp happens BEFORE the decrement each tick, so consecutive hits: tick1: 5→-25; tick2: clamp 0, hit → -30, +1 → -29; tick3: clamp 0 → 0, hit → -30... so during the hitting spree ai0 stays ~-30; after hits stop: 0 → 900 ticks. Vanilla: after same spree: 5 - 40*n → e.g. 10 hits over 10 ticks: 5-400 = -395 → needs 1295 ticks. So vanilla: hitting an egg 10 times delays hatch by ~6.5 seconds more than ours. Minor gameplay timing deviation. Report as low if room. Both are "hatch timing after hits" — meh. I have limited slots; I'll fold this into a minor note.

Finding #5 candidate — LunarOrb 539 orphan: delayed charge. Also minor.

Finding #6 candidate — nebula floater flag105 gate claim "恒假" wrong (orbs with negative ai0 exist after a delay subtraction, so vanilla sometimes SKIPS the -30). Effect: ours over-accelerates orbs. Minor.

Finding #7 candidate — 455 damage ×2. Consistent convention with the audited core/head spawns. I'll note it as "存疑/口径" rather than CONFIRMED bug — actually wait: since damagePlayer takes raw dmg, and vanilla 455 = 50... but hold on, maybe our NPC damage convention: our repo generally uses vanilla damage values directly (shootL passes 35/40/60/65 raw). Only 455 gets ×2. If the convention were "×2 for beams", it'd be inconsistent with 35/40 raw. Let me check one more beam-ish hostile: e.g., other lasers in the codebase — do they double? Golem head laser? Let me grep quickly for 455 damage elsewhere... The core file already passes 50*2 and 75*2 and was audited (per memory: "全Boss三维总审计批" audited summons/drops; moonlord was ported in bossAI_duke_moonlord and audited). The ×2 may be a deliberate balance for iframes throttling (vanilla 455 hits every frame? Vanilla deathray damage applies on contact each tick the player intersects, subject to player immunity frames ~10/tick? Player hurt cooldown... In vanilla, players take damage at most once per ~40 ticks? No — player i-frames are typically 10-ish ticks... hmm, vanilla player immunity after hit = 40 ticks? It's `immune` timer ~ 40 for most hits... If our damagePlayer iframes are twice as long as vanilla's, doubling damage compensates. The comment in MLDeathray says "伤害走 damagePlayer(iframes 节流)". The core variant passed audit with ×2. I'll list it as a note/question, not CONFIRMED.

Finding #8 candidate — tablet 439 cultist y-anchor: ours bottom-aligned vs vanilla y-2. Trivial.

Finding #9 candidate — mimic state 6 grounded gate: ours `e.onGround && e.vy === 0` vs vanilla `velocity.Y == 0f`. Also state 6's exit `e.ai2 >= 3 && e.onGround && e.vy === 0` vs vanilla `ai[2] >= 3 && velocity.Y == 0`. Consistent with our engine. Fine.

Finding #10 candidate — the free eye: state 0 hover lacks the extra `velocity` term? Verified fine.

Finding #11 — phantom reveal dust counts approximate. Fine.

Finding #12 — babyMothron/starCell latch y offsets (h/2 differences). Trivial.

Finding #13 — mothron egg spawn placement (top vs bottom anchor): vanilla top at tile → egg partially sunken into floor; ours bottom at tile top → sits on floor. Visual only. Note.

Finding #14 — cultistTablet particles instead of 526 projectiles: disclosed in header. Note.

Finding #15 — flowInvader: missing TargetClosest/`rotation` semantics fine.

Wait — one more thing to verify on the mimic: state 4 hover else-branch (ai2==0, not aligned): vanilla normalizes vector245 — which is the -350 target — *12. Ours matches. OK.

And state 4 entry `if (pick === 1) e.vy = -8` — vanilla case 1: ai[0]=4, noTileCollide=true, velocity.Y = -8. Ours matches (fly() in state 4 ignores tiles since we integrate directly). OK.

Now — one more potential structural check on mothron state 0: vanilla rotation formula uses velocity.X*0.1 with step 10 (spin). Ours: `e.spin = (e.spin * 9 + e.vx * 0.1) / 10;`. OK.

Also mothron -1 state: vanilla velocity = (velocity*9 + (0,-8))/10 — that's a full formula, not vx *= 0.9! Vanilla: velocity = (velocity * 9f + vector249) / 10f where vector249 = (0, -8). So vx = vx*9/10 (decay 0.9), vy = (vy*9 - 8)/10. Ours: `e.vx = (e.vx * 9) / 10; e.vy = (e.vy * 9 - 8) / 10;`. Match!

And babyMothron -1: same. Ours matches.

Also check moonLordFreeEyeAI state 0: `e.facing = e.seekDirX(player)` — TargetClosest(faceTarget: false) doesn't set direction! Vanilla TargetClosest(faceTarget: false) skips direction update. Ours updates facing. Trivial visual.

Let me also double-check the "moonLeechAI" spawn burst particles — cosmetic.

Now let me confirm the mimic findings by re-reading our exact lines for the report, and also verify vanilla line numbers for citations:
- Vanilla 4.1 branch: :39716-39731 (the `else if (this.ai[0] == 4.1f)` starts at :39716 per sed output: it was at line 39716 area. Let me get exact line numbers.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:29.546Z · glm-x-preview-260804

```
Mimic 的两个可疑问题均已确认。我来定位这些偏差的确切原版行号。
```


---

## 🤖 Assistant · 2026-08-19T03:24:29.547Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"this.ai\\[0\\] == 4.1f\\|this.ai\\[0\\] == 4f\\|vector245 = Main.player\\[target\\].Center - base.Center\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; sed -n '39643,39647p;39716,39740p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Pin vanilla mimic state 4 and 4.1 line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:29.590Z

**📎 ToolResult**

```
29621:			else if (this.ai[0] == 4f)
30974:			else if (this.ai[0] == 4f)
33140:			else if (this.ai[0] == 4f)
35672:			else if (this.ai[0] == 4f)
37538:				else if (this.ai[0] == 2f || this.ai[0] == 4f)
39119:			else if (this.ai[0] == 4f)
39658:			else if (this.ai[0] == 4f)
39679:					vector245 = Main.player[target].Center - base.Center;
39708:			else if (this.ai[0] == 4.1f)
40238:			else if (this.ai[0] == 4f)
				velocity.X *= 0.85f;
				dontTakeDamage = true;
				this.ai[1] += 1f;
				if (Main.netMode != 1 && this.ai[1] >= 180f)
				{
				{
					this.ai[1] += 1f;
					if (Main.netMode != 1 && this.ai[1] > 10f)
					{
						this.ai[0] = 2f;
						this.ai[1] = 0f;
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						netUpdate = true;
						if (Collision.SolidCollision(position, width, height))
						{
							this.ai[0] = 5f;
						}
					}
				}
				else if (this.ai[2] == 0f)
				{
					noTileCollide = true;
					noGravity = true;
					knockBackResist = 0f;
				}
				velocity.Y += 0.2f;
				if (velocity.Y > 16f)
				{
					velocity.Y = 16f;

```


---

## 🤖 Assistant · 2026-08-19T03:24:40.498Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed vanilla mimic:
- State 4: :39658-39706; ai2==1 aim replace at :39679 `vector245 = Main.player[target].Center - base.Center;` (player center, no -350).
- State 4.1: :39708-39731. The aligned-fall case (ai2==1, above player, vy>0) falls through with only vy += 0.2 (:39726-39731) and integrates via shared movement with collision (noGravity/noTileCollide both false — reset at :39524-39527).

Our file lines:
- bigMimicAI state 4: /game/src/entities/bossAI_lunar_misc.ts:679-698 (aim bug at 683-690).
- State 4.1: :699-713 (freeze at 701-713).

Now let me also double-check the mimic 4.1 first-branch ai1 > 10 vs vanilla: ours `if (e.ai1 > 10)`. Vanilla `> 10`. OK.

One more check — mimic state 4: vanilla ai2==1 exit sets `velocity = vector245` = toward PLAYER at speed 8. Ours sets `e.vx = tx; e.vy = ty` = toward player-350. Both confirmed.

Next, I want to verify two remaining things:

1. `game.world.groundLevel` unit for mothron egg search (flag95). Let me grep how groundLevel is defined.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:41.401Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"groundLevel\" ~/Project/GLM/SandboxWorld/game/src/world/*.ts | head -8; grep -rn \"clock.eclipse\\|eclipse\" ~/Project/GLM/SandboxWorld/game/src/world/GameWorld.ts 2>/dev/null | head -5",
 "description": "Check groundLevel units and eclipse clock field"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:41.450Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/LunarEvent.ts:143:  const surface = Math.floor(w.groundLevel);         // (int)Main.worldSurface
~/Project/GLM/SandboxWorld/game/src/world/Invasion.ts:145:  if (py > w.groundLevel * 16 + screenHPx && w.spawnY <= w.groundLevel) return false; // 地下
~/Project/GLM/SandboxWorld/game/src/world/TeleportPylons.ts:142:  if (y <= world.groundLevel) return false;
~/Project/GLM/SandboxWorld/game/src/world/TeleportPylons.ts:157:      const surface = y <= world.groundLevel;
~/Project/GLM/SandboxWorld/game/src/world/TeleportPylons.ts:167:      return y >= world.groundLevel;                  // :298（worldSurface 含）
~/Project/GLM/SandboxWorld/game/src/world/TeleportPylons.ts:170:      const depthOk = y <= world.groundLevel && y > world.groundLevel * 0.3499999940395355;
~/Project/GLM/SandboxWorld/game/src/world/MeteorFall.ts:17:  spawnX: number; groundLevel: number; rockLevel: number;
~/Project/GLM/SandboxWorld/game/src/world/MeteorFall.ts:55:  for (let y = 5; y < h.groundLevel; y++) {

```


---

## 🤖 Assistant · 2026-08-19T03:25:21.217Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
groundLevel is in tiles (used with y in tile coords). Ours: `const aboveGround = e.cy / TILE < game.world.groundLevel;` — vanilla `(double)(base.Center.Y / 16f) < Main.worldSurface`. Match.

Now, let me quickly double-check the moonLordFreeEyeAI hover separation loop break: vanilla continues (no break) — ours no break. Match.

Also verify the free eye's `if (e.ai0 === 4)` else-branch for t >= dur-15: ours reduces x[1]; vanilla same.

Now, let me also spot-check one claim about crawltipedeAI: `if (!e.wormNext || e.wormNext.dead) { e.die(game); return; }` — vanilla head checks `!Main.npc[(int)ai[0]].active || aiStyle != aiStyle → die`. Ours also aiStyle implicit (chain of same family). OK.

And crawltipede no-target branch: ours damps and drifts. Vanilla: TargetClosest() → stale target, still steers at last target position. Ours drifts. Minor single-player no-player case (only in multiplayer disconnect). Skip.

Now compile final counts. CONFIRMED findings:

1. (HIGH) bigMimic 4.1 aligned-dive case: no movement → mid-air freeze. Ours :699-713 vs vanilla :39708-39731 (aligned case falls through, only vy+=0.2, movement with collision). Trigger: LOS clear at dive start (typical).

2. (HIGH) bigMimic state 4 ai2==1 short-aim uses hover point (player-350) instead of player center; dive velocity launched toward 350px above player. Ours :683-690 vs vanilla :39672-39684 (vector245 replaced with player.Center - Center at :39679).

3. (MED) Mothron 477 + baby 479: missing ">3000px → ai[0] = -1 climb-despawn" gate (vanilla :39890-39903 / :40485-40496). Ours only !p. Effect: distant moths keep chasing instead of climbing off; also event-end semantics slightly narrower.

Let me verify those vanilla line numbers: mothron target gate at :39886-39915 per my earlier read (the block `else if (target < 0 || ...dead...) { TargetClosest(); ... if (dead || vector247.Length() > 3000f) ai[0] = -1 }`). From the sed of 39876-40060, the block started right after `else if (target < 0 ...` — line ~39890. And babyMothron: from sed 40450+, the block `if (target < 0 || dead || !active) { TargetClosest(); ... if (dead || Length() > 3000f) ai[0] = -1 }` around :40486-40497. Let me grep exact lines.

4. (LOW) mothronEgg clamp clobbers negative hatch progress: ours :980 `if (e.ai0 < 0) e.ai0 = 0` runs before justHit decrement each tick; vanilla accumulates negative ai0 freely (:40419-40425). Repeated early hits delay hatch unboundedly in vanilla, capped in ours.

Hmm — actually wait. Let me reconsider the severity/direction: vanilla negative = hatch LATER. Ours = hatch SOONER than vanilla. It's a real logic deviation but tiny. Keep as low.

5. (LOW) LunarOrb 539 orphan: when parent dies during orbit, vanilla sets ai[0] = 210 immediately (charge now) (:32093-32097); ours coasts with old velocity until its own ai0 reaches 210 (up to ~160t later). Also for 574... wait, for 574 the parent-death → Kill. Ours matches for 574. Just 539.

Let me verify the vanilla lines for the 539 parent-death: from my read of Projectile.cs 32083-32097:
```
if (flag49) { ... if (!Main.npc[num855].active || type != num850) { Kill(); return; } timeLeft = 2; }
this.ai[0]++;
if (this.ai[0] < num851)
{
    bool flag50 = true;
    int num856 = (int)this.ai[1];
    if (Main.npc[num856].active && type == num850)
    { ...position += ... }
    else
    {
        this.ai[0] = num851;   // ← parent gone → jump to charge threshold
        flag50 = false;
    }
```
Line numbers: the sed started at 32040; the `else { this.ai[0] = num851; flag50 = false; }` was around 32105-32108. Let me get exact.

6. (LOW) nebulaFloater teleport orb-accelerate gate: vanilla skips the -30 when any orb has ai[0] < 0 (:41673-41691); ours unconditional (claims 恒假). Actually wait — I need to double check vanilla's flag105 logic:
```
bool flag105 = true;
for ... { if (proj.active && type == 574 && ai[1] == whoAmI && !(ai[0] >= 0f)) { flag105 = false; break; } }
if (flag105) { for ... ai[0] -= 30 }
```
So if any orb's ai[0] < 0 → skip. When would ai[0] < 0? Only via the -30 subtraction when ai[0] < 30 — i.e., an orb that JUST fired its 576 (reset to 0) within 30 ticks of a teleport. Floater teleports every 480t; orbs reset at 180t cycles. Orb timelines: orb spawned at t=0/60/120. Fire at +180 etc. Teleport at 480: orb1 ai0 = (480-180k)-30... orb1 spawned t=0: ai0 counts 0..180 fires, resets; at t=480: 480 mod 180 = 120 → ai0 = 120-30 = 90 ≥ 0. orb2 spawned t=60: ai0 = (480-60) mod 180 = 60 → 30. orb3 spawned t=120: (360) mod 180 = 0 → -30 <0! So at t=480 teleport, orb3 (spawned at 120, fired at 300, reset, ai0 counts 0 from t=300; at 480 ai0 = 180 → fires at exactly 480!). Edge alignment. So the negative case occurs when teleport lands within 30 ticks after an orb fires. Rare but real. And in vanilla, once an orb goes negative it stays negative only until it counts back up to 180 (fires again). The gate matters ~rarely. LOW. Maybe skip from top-10 or keep as low. I'll mention in minor notes.

7. Note: 455 damage ×2 convention.

8. Note: cultist spawn y anchor -2, egg spawn anchor, 526→particles, 421 hide, 539 rotation — all disclosed/visual.

Also — did I miss checking "moonLordFreeEyeAI state 2 else (t>=120)" — `e.spin = angleLerp(e.spin, 0, 0.2)` — vanilla rotation.AngleLerp(0, 0.2). Match.

One more free-eye detail: state 1 `x[2] = lerp(x[2], t < 20 ? 1.1 : 0.4, 0.2)` — vanilla num1294 < 20 → 1.1 else 0.4. Match.

Now exact line numbers for the report on our side:
- moonLordFreeEyeAI: :142-314.
- bigMimicAI 4 aim: :683-690; 4.1: :699-713.
- mothronAI gate: :785-791.
- babyMothronAI gate: :1039-1040.
- mothronEggAI clamp: :980.
- LunarOrb: :1849-1860 (orbit/charge), orphan case at :1851-1860.

Vanilla lines to cite:
- mimic 4: :39658-39706 (aim replace :39679).
- mimic 4.1: :39708-39731.
- mothron gate: need exact — the `else if (target < 0 ...` block. From sed 39876-40060, it began at :39886 (`else if (target < 0 || Main.player[target].dead || !Main.player[target].active)` around :39886) with the >3000 check at :39891-39901. Let me grep for "3000f" nearby.

Also — one thing I should double check: free eye deathray dmg 50*2 and whether our Arrow for 462 (35 dmg) etc is raw. Yes shootL passes 35/40 raw — so ×2 only on MLDeathray. Let me look at what the "core" spawn passes — 50*2 at :1303 duke file (already checked). It's consistent within moonlord beams. I'll flag as note with "if unintended, applies to 3 sites".

Let me grep the exact vanilla line numbers for the 3000f gates.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:25:22.471Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"3000f\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1>39800 && $1<40700' ; grep -n \"this.ai\\[0\\] = num851;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Projectile.cs | head -3",
 "description": "Pin exact vanilla lines for 3000px gates and orb orphan jump"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:25:22.543Z

**📎 ToolResult**

```
39895:				if (Main.netMode != 1 && (Main.player[target].dead || vector247.Length() > 3000f))
40489:				if (Main.player[target].dead || vector257.Length() > 3000f)
32108:					this.ai[0] = num851;

```


---

## 🤖 Assistant · 2026-08-19T03:25:48.050Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Vanilla line numbers:
- Mothron 3000px gate: :39895 (477).
- Baby mothron: :40489 (479).
- LunarOrb orphan jump: Projectile.cs:32108.

Now let me do a final sanity pass on two more sections I haven't fully cross-checked: the free eye's state 2 (already done), and the moonLeech dust (cosmetic). Also — one loose end: bigMimicAI state 0 `grounded()` includes gravity — vanilla mimic state 0 also gravity. OK.

One more potential check — `cultistTabletAI`: ours sets `e.lightRGB` BEFORE bInit check; fine.

Also for `lunaticDevoteeAI`: ours `e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED); moveAndCollide(...)` — vanilla devotee gets gravity from shared code (noGravity false). Match.

And the devotee wake: `if (e.justHit)` sets owner's localAI[0]=1 — vanilla checks `Main.npc[num1364].localAI[0] == 0f` first. Ours: `if (ox[0] === 0) ox[0] = 1;`. Match.

One more: tablet's justHit chain — vanilla tablet localAI[0] set to 1 by devotee/archer being hit; the tablet reads localAI[0]==1 → 2 and activates archers. Ours matches. But ALSO: vanilla reads it even after it's 2? `if (localAI[0] == 1f)` only when exactly 1. Ours: `if (x[0] === 1) { x[0] = 2; ... }`. Match.

Now — final check of a suspicious piece in mothronAI state 0: ours early-returns `if (e.ai1 < 180) return;` AFTER movement — matches vanilla `if (!(ai[1] >= 180)) return;` (movement already applied via moveAndCollide + bounceAxis earlier in ours — vanilla movement happens in shared section after AI... wait, no: vanilla AI() returns → the shared movement integration at the end of AI() is SKIPPED on early return? Hmm. This is the same question as before. In Terraria's decompiled NPC.cs, the velocity→position integration happens INSIDE AI() in the post-switch shared section (~:91400). Early `return` skips it!

Wait, that can't be right — e.g. aiStyle 87 state 3 has `return` statements? Let me check: in the mimic code I read, states end without return... but the free-eye's `if (!(num1294 >= 60f)) return;` inside state 4 t<180 exists. If early return skipped movement entirely, the eye would freeze for the first 60 ticks of the deathray windup — with velocity damped ~0.95/tick... it would still move a bit in vanilla? If movement is skipped, no movement at all for t<60.

Hmm, I need to determine the actual structure. Let me look at the end of the aiStyle switch and the movement integration location. In the decompiled code, AI() is one giant method with the switch, and after the switch there's shared code (gravity etc.) then movement integration is inside "if (flag...) ... position += velocity". Let me check around :91400.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:25:48.831Z · glm-x-preview-260804

```
关于原版结构有一个遗留问题：早期的 `AI-return` 是否会跳过共享移动。我正在检查 `NPC.cs:91400` 附近的移动集成点。
```


---

## 🤖 Assistant · 2026-08-19T03:25:49.387Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '91380,91440p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla shared movement integration section"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:25:49.423Z

**📎 ToolResult**

```
			}
		}
		if (Main.netMode == 1 && NPCID.Sets.SkipUpdateInUnsyncedTiles[type])
		{
			bool flag = false;
			int num4 = (int)(position.X + (float)(width / 2)) / 16;
			int num5 = (int)(position.Y + (float)(height / 2)) / 16;
			try
			{
				if (num4 >= 4 && num4 <= Main.maxTilesX - 4 && num5 >= 4 && num5 <= Main.maxTilesY - 4)
				{
					if (Main.tile[num4, num5] == null)
					{
						flag = true;
					}
					else if (Main.tile[num4 - 3, num5] == null)
					{
						flag = true;
					}
					else if (Main.tile[num4 + 3, num5] == null)
					{
						flag = true;
					}
					else if (Main.tile[num4, num5 - 3] == null)
					{
						flag = true;
					}
					else if (Main.tile[num4, num5 + 3] == null)
					{
						flag = true;
					}
				}
			}
			catch
			{
				flag = true;
			}
			if (flag)
			{
				return;
			}
		}
		UpdateNPC_BuffFlagsReset();
		UpdateNPC_BuffSetFlags();
		UpdateNPC_SoulDrainDebuff();
		UpdateNPC_BuffClearExpiredBuffs();
		UpdateNPC_BuffApplyDOTs();
		UpdateNPC_BuffApplyVFX();
		UpdateNPC_BloodMoonTransformations();
		UpdateNPC_UpdateGravity(out var maxFallSpeed);
		if (soundDelay > 0)
		{
			soundDelay--;
		}
		if (life <= 0)
		{
			active = false;
			UpdateNetworkCode(i);
			netUpdate = false;
			justHit = false;
			return;

```


---

## 🤖 Assistant · 2026-08-19T03:25:53.595Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is in UpdateNPC (the caller of AI()), not AI() itself. So the shared movement/gravity is in UpdateNPC AFTER AI() returns — meaning early `return` from AI() does NOT skip movement. The movement integration must be further down in UpdateNPC. Let me confirm quickly by finding "position += velocity" or Collision.SweepCoinsAABBvBB... Actually the memory note said "NPC.cs UpdateNPC :91400 segment shared displacement wall-penetrating branch". Let me look at ~91440-91520.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:25:54.354Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '91440,91510p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"velocity\\|position\" | head -20",
 "description": "Find movement integration in UpdateNPC"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:25:54.389Z

**📎 ToolResult**

```
6:		float num6 = 1f + Math.Abs(velocity.X) / 3f;
56:				position += netOffset;
57:				int num9 = Dust.NewDust(position, width, height, num7, 0f, 0f, 254, default(Color), 0.25f);
58:				Main.dust[num9].velocity *= 0.1f;
59:				position -= netOffset;
71:			int num10 = (int)(position.X + (float)(width / 2)) / 16;

```


---

## 🤖 Assistant · 2026-08-19T03:25:57.900Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=91500 && NR<=92100 && (/position \\+= / || /Collision\\./ || /noTileCollide/ || /Sweep/)' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -20; grep -n \"private void AI()\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -2",
 "description": "Locate velocity integration and AI method boundary"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:25:57.971Z

**📎 ToolResult**

```
		if (!noGravity && !noTileCollide)
		if (!noTileCollide)
			position += velocity;
			if (Collision.WetCollision(position, width, height))
		if (Main.netMode != 1 && !noTileCollide && lifeMax > 1 && Collision.SwitchTiles(this, position, width, height, oldPosition, 2) && (type == 46 || type == 148 || type == 149 || type == 303 || type == 361 || type == 362 || type == 364 || type == 366 || type == 367 || (type >= 442 && type <= 448) || type == 602 || type == 608 || type == 614 || type == 687))

```


---

## 🤖 Assistant · 2026-08-19T03:26:40.073Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
So `position += velocity` (noTileCollide) or Collision-based movement happens in UpdateNPC after AI() — early return from AI() does NOT skip movement. Good — so vanilla mimic 4.1 aligned case falls with collision (movement in shared code), while ours has no movement call at all. Finding #1 stands firmly.

And this also means: in vanilla, velocity set by AI always integrates (except when AI returns before setting velocity... it still integrates with whatever velocity). Our port pattern (explicit moveAndCollide/fly per state) matches that — except the 4.1 hole.

Wait, but one more consideration for our finding #1: does OUR mimic get moved by anything else? bigMimicAI is the only mover, and state 4.1's hole = frozen. Confirmed.

Also note for finding #2: the dive direction toward (player - 350). Combined effect: mimic launches toward 350px above the player AND (with LOS) freezes right there in mid-air. Actually with finding #1, the mimic freezes immediately at the start of 4.1, so the launch direction bug (finding #2) manifests only in the no-LOS path... Both still real.

Hmm wait, actually — let me reconsider finding #1's trigger once more. The ai2 0→1 promotion requires `losClear && !inSolidBody`. With LOS blocked (player under a ceiling, common in caves!), ai2 stays 0 → else-if branch runs fly() → dives through walls correctly. With LOS clear (open field), ai2 → 1 → frozen. So behavior is inverted vs vanilla intent: vanilla uses ai2==1 to switch to COLLISION fall (aligned), ai2==0 to phase through. Ours freezes when aligned. In open terrain (mimics in caverns mostly — hallowed/corruption/jungle/desert mimics are usually in caves with ceilings...). Either way it's a hard stall.

Now, let me also double-check the free eye `if (!(num1294 >= 60f)) return;` — since AI-early-return doesn't skip movement, no issue at all. Good.

Now finalize minor notes and assemble the report. Let me also double check the nebula floater opening-orb count: localAI[2] < 180 with % 60 → at 60, 120, 180? At localAI[2]=180: increment to 180 → 180 % 60 == 0 → spawns a THIRD orb at 180? Ours: `if (lai[2] < 180) { lai[2] += 1; if (lai[2] % 60 === 0) spawn; }` — lai[2] reaches 180 on the 180th tick and 180 % 60 === 0 → spawns at t=180 while vanilla: localAI[2]++ then check % 60 — same: localAI[2] goes 1..180; at 180 → spawn. So 3 orbs (60/120/180). Vanilla identical structure. Match.

Also `e.ai1 = 20` on teleport (vanilla sets ai[1] = 20 — vanilla comment "(除 ==1 外无读者)" — hmm wait, ours says :41670 sets ai[1]=20. And the dissolve gate is ai[1]==1. 20 ≠ 1 fine.

One more possible check — nebulaFloater: vanilla `if (vector280.Length() > 400 || !flag103)` chase. Ours: `if (td > 400 || !los)`. Match.

And the teleport execution gating `if (e.ai2 !== 0 && e.ai3 !== 0)` — vanilla same.

Now — what about "e.ai0 >= TP_T" ordering: vanilla increments ai[0] AFTER the teleport-execution block, and the AI_097 teleport spot search uses `AI_AttemptToFindTeleportSpot(ref chosenTile, point13.X, point13.Y, 20, 12, 1, ...)`. Ours findTeleportSpot(game, e, p) — internally computes from p. Match.

OK — also the opening orb spawn position: vanilla `NewProjectile(Center.X, Center.Y, ...)` — projectile position is top-left = Center → orb CENTER at (Center.X + w/2...)? NewProjectile x,y is the projectile's position (top-left). Vanilla passes Center.X/Y as position — so orb top-left at NPC center (slightly offset). Ours: `this.x = (x ?? parent!.cx) - this.w / 2` → orb CENTER at parent center. Off by half-size. Trivial.

I think I have my findings. Let me also double check finding #3's exact vanilla behavior for mothron: `else if (target < 0 || dead || !active) { TargetClosest(); if (dead || dist > 3000) ai[0] = -1 }`. Ours:

```js
if (!game.world.clock.eclipse) {
    if (e.ai0 !== -1) e.ai0 = -1;
  } else if (!p) {
    e.ai0 = -1;
  } else if (e.ai0 > 1 && Math.hypot(...) > 1000) {
    e.ai0 = 1;
  }
```

Missing: alive player but > 3000px → -1 (climb away, invulnerable). Impact: in vanilla a Mothron that gets >3000px from the player flies up and despawns; ours keeps state 0/1 hover. Combined with `EncourageDespawn` absence for mothron (vanilla -1 state has no EncourageDespawn for 477? The -1 branch just climbs; despawn happens via normal off-screen despawn rules). Eh — it's a flee-gate deviation: report.

Also for babyMothron: vanilla same 3000 gate (line :40489). Ours `if (!p) e.ai0 = -1; else if (e.ai0 > 1 && d > 1000) e.ai0 = 1;`. Same missing gate.

Severity: medium-low. Both files ours: mothron :785-791, babyMothron :1039-1040.

Now assemble the final report. Structure: per-family sections with "核了什么+发现什么", then the CONFIRMED list (≤10, sorted by severity), then 存疑/minor notes.

Findings list:
1. bigMimic 4.1 freeze (HIGH) — ours 699-713 / vanilla 39708-39731.
2. bigMimic state 4 ai2==1 aim point (HIGH-MED) — ours 683-690 / vanilla 39672-39684 (esp. :39679).
3. Mothron+baby missing >3000px flee gate (MED) — ours 785-791, 1039-1040 / vanilla 39886-39901, 40485-40496.
4. LunarOrb 539 orphan delayed charge (LOW-MED) — ours 1851-1860 / Projectile.cs 32103-32109.
5. mothronEgg negative-progress clamp clobber (LOW) — ours 980 / vanilla 40419-40425.
6. nebulaFloater orb-accelerate gate skipped unconditionally (LOW) — ours 1574-1583 / vanilla 41673-41691.

存疑/notes:
- 455 damage ×2 convention (3 sites: free eye 100, core 100, head 150 vs vanilla 50/50/75) — consistent project-wide; if damagePlayer doesn't halve, deathray damage is double vanilla.
- 526 ritual projectile downgraded to particles (disclosed in header).
- Egg/cultist spawn anchor y (top vs bottom) — ~visual.
- 421 state-1 attach h/2 offset (one tick).
- granite double-anchor upgrade uses |dy|>8 where vanilla reuses |dx|>8 quirk (starCell copies the quirk; granite doesn't) — vanilla :40734-40742.
- LunarOrb explode missing SoundID 4 style 7.
- Mothron 180t pick: single roll per 180t vs vanilla while re-roll (disclosed).
- 539 draw rotation always orbit-mode during charge (disclosed).
- mimic state 7 no defense=9999 (hp full-heal each tick compensates).

Also should double check finding #2's vanilla line range. From sed output: state 4 block :39658-39706; the ai2==1 sub-block at :39672-39684 with :39679 being the re-aim. Good.

And our line numbers: state 4 block at :679-698; :683-684 dx/dy def; :685-690 ai2==1 branch. State 4.1 at :699-713.

Also confirm ours 713 is the closing brace... from the read: 
```
699	  } else if (e.ai0 === 4.1) {
700	    // ---- 俯冲下坠...
701	    if (e.ai2 === 0 && p && losClear(...) && !inSolidBody(game, e)) e.ai2 = 1;
702	    e.vy = Math.min(e.vy + 0.2, 16);
703	    if (!p || e.y + e.h >= p.y || e.vy <= 0) {
704	      e.ai1 += 1;
705	      if (e.ai1 > 10) {
706	        e.ai0 = inSolidBody(game, e) ? 5 : 2;
707	        e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
708	      }
709	      moveAndCollide(e, game.world, e.vx, e.vy);
710	    } else if (e.ai2 === 0) {
711	      e.noGravity = true;
712	      fly(e);
713	    }
714	  } else if (e.ai0 === 5) {
```
So the hole: ai2==1 && above player && vy>0 → nothing between 703/710. Yes.

Done. Write the final report in Chinese (the user's language), structured per-family, max 10 CONFIRMED, sorted by severity, with file:line / vanilla line / symptom / minimal fix / confidence.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:27:36.148Z · glm-x-preview-260804

```
所有系列已完成审计。正在整理最终报告。

# 月系 Boss AI 1:1 抡查审计报告

审计对象:`game/src/entities/bossAI_lunar_misc.ts`(1929 行) vs `Terarria1456/Terraria/NPC.cs`。逐族读了原版对应段(38224-38667 / 38668-38792 / 38793-38962 / 39261-39519 / 39520-39875 / 39876-40449 / 40450-40685 / 40686-40870 / 38967-39220 / 41445-41750 / 41997-42056 / 51740-52620)并抽验了 CultistRitual.cs、Projectile.cs(AI_102 :32040-32280、Kill :69366-69405)、MoonLordAttacksArray2(:6966-6985)、弓手待机(:56575-56610)、AI_AttemptToFindTeleportSpot(:18876-18946)。另核实了 Enemy.ts 的分发方式(这些 AI 自管位移，分发后无共享位移尾段)与 UpdateNPC 共享位移位于 AI() 之外(原版早 return 不跳过位移)。

## 逐族结论

- **月总游离眼 400(aiStyle 81)**:十槽攻击表与 :6966-6985 逐槽全等；ai[1] 累计/槽内 t 的解码循环、悬停排斥、462 三连(dur-35/-7/-dur)、454 六角螺旋(PAIRS 表+外发速 4/40 伤)、75t 起跳-105t 冲出(24 速)、452 螺旋洒射(8→20 速、每 10t)、455 起角/扫速/编码角逐 t 解码全部对上。核心亡消散、dontTakeDamage(iframes) 语义一致。**干净**。
- **水蛭块 401(aiStyle 82)**:90t 插值到头额 (0,+216)、1000 治疗池按 头→核心→手0→手1 亏血序、min(pool,deficit) 公式、头亡消散全对上。源弹插值起点用出生点近似已注明。**干净**。
- **拜月仪式链(437/438/379)**:CheckFloor 与 CultistRitual.cs:100-124 逐条件全等(i∈{-5,-3,3,5}×2、j -5..11、平台计入、双净空或语义);localAI[0]==1 激活链、四教徒全灭判定、侧面 11 格找列+439 朝向、300t 倒计时+120t 起每 10t 粒子全对上;弓手待机段与 :56575-56610(伤害 0、1000..1300 帧循环、受击回写碑 localAI[0]、唤醒复位)全等。**干净**(526 投射物降级为粒子系头部已登记偏差)。
- **幻影 472/521(aiStyle 86)**:四态参数(0.3/7/4/660/4、521 的 0.7/14/6/500/3;态 2 的 0.4/0.95/5 vs 0.3/0.9/7;态 3 的 0.4/0.2 与 0.6/0.3)全部与 :39400-39519 一致,越程掉头门与 ai[1] 垂直向选择也对。**干净**。
- **珍稀宝箱怪 473-476(aiStyle 87)**:跳扑参数(15+30·HP比、3+4(1-HP比)、LOS +2 跳力、每 3 跳双倍跳力/半横速)、210t 随机换招(3/4/6,4 起跳 -8 穿墙)、三连扑的 6 档跳力与 ±8 保底、5/6/7/8 态全对上;**但飞天俯冲链(态 4/4.1)有两处结构性偏差,见 CONFIRMED #1/#2**。
- **飞蛾魔家族(477/478/479)**:0/1/2/3/3.1/3.2/4/4.1/4.2 全状态速度档、步进、伤害档(×0.5/×1.3)、产卵扫描(±30/±20 扩圈、下潜 50 格、岩浆排除、600px 门)、478 的 900t 孵化与受击双扣、479 的 90t/10t/2.1 增速链全对上;**缺 >3000px 爬升脱战门(CONFIRMED #3)**,蛾卵 ai0 负值被钳(**CONFIRMED #5**)。
- **花岗岩元素 483(aiStyle 91)**:五态寻路(0 视线判别/1 直追 2+距/200/2 穿墙 2 速/3 锚点 1 速/4 漂移弹壁 1.5 速 180t+每 5t 重试锚)与 :40686-40870 一致。**干净**(一处原版怪癖未照抄,列入存疑)。
- **星璇塔四组怪**:星细胞 405/421 六态+421 头顶吸附(Obstructed 59t 续期、同族吸附互斥)与 :38967-39220 一致,且照抄了原版"列距>8 复用"怪癖;小星细胞 406(300t 长大+尘环档)、水流入侵者 407(SimpleFlyMovement 档位+每 70t 甩 539)、日耀黏液 519(0.2 重力钳 12、落地 5t 定格自爆)均与原版段一致;悬浮脑 420 的 3 枚环绕球、1/6 受击瞬移、480t 落点瞬移、消散 3t 链对上,AI_AttemptToFindTeleportSpot 收敛版与 :18876-18946 的门(±1 自排斥、岩浆、3×3 净空、12 tile telefrag∪速度 20 外推、2000px 放弃)逐条全等。**LunarOrb 539 孤儿延迟冲刺与 574 加速门见 CONFIRMED #4/#6**。
- **爬尾虫 412(aiStyle 6 专属段)**:30 段链构建(realLife=头)、段完整性自查(413 双向/414 前向/头后向)、414 红闪 localAI 状态机(与 :52026-52047 逐行全等)、头火尘双粒、目标覆写(玩家下方 15 格有地→悬停线 800px+|dx|<500 外推 600、悬空提速 14/0.5)、速度带钳 [0.7n,1.3n]、同族分离 60/200 或 400/1000、16px 量化、!flag8 舵机三分支(含 0.2n 垂直助推与 1.1 步进档)、段链收缩 (d-(w+6))/d 全部与 :51764-52620 对应段一致。**干净**。

## 已确认偏差(按严重度)

**#1 宝箱怪 4.1 态"对齐俯冲"分支无位移 → 空中永久僵死**(严重度:高,置信度:高)
- 我方:`bossAI_lunar_misc.ts:699-713`(漏洞在 :703 与 :710 之间)
- 原版:`NPC.cs:39708-39731`
- 症状:进入 4.1 后首 tick 若对玩家有视线且不埋块,`ai2` 即被置 1;此后"未过玩家 Y 且 vy>0"时,第一分支(过顶/回落)不进,第二分支又要求 `ai2===0` → **两条位移路径都不执行**。vy 只会 +0.2 累积到 16,位置永不变 → 宝箱怪在玩家上方 350px 处悬停僵死,直到玩家自己跳进它的判定盒。原版该情形 noGravity/noTileCollide 均为 false(每 tick 顶部复位),靠共享位移带碰撞下坠砸向玩家。开阔地带(LOS 常清)几乎必触发。
- 最小修复:给 `else if (e.ai2 === 0)` 补一个平级 `else { moveAndCollide(e, game.world, e.vx, e.vy); }`(对齐态带碰撞下坠)。

**#2 宝箱怪 4 态 ai2==1 短瞄目标错:瞄"玩家上方 350px"而非玩家**(严重度:高,置信度:高)
- 我方:`bossAI_lunar_misc.ts:683-690`(dx/dy 在 :684 已含 -350,又被 :687-690 的 ai2==1 分支复用)
- 原版:`NPC.cs:39672-39684`——ai2==1 时 `vector245` 被整体替换为 `player.Center - Center`(:39679,**无 -350**),归一化 ×8;离开该态时 `velocity = vector245` 即直指玩家。
- 症状:6t 短瞄与俯冲初速都朝玩家头顶 350px 发射,配合 #1 表现为"起飞→悬停在玩家头顶不砸下来";即使修了 #1,俯冲方向也偏 350px。
- 最小修复:ai2==1 分支内重算 `dx = p.cx - e.cx; dy = p.cy - e.cy;` 再归一化 ×8。

**#3 飞蛾魔 477/幼蛾 479 缺 ">3000px → ai[0]=-1 爬升脱战"门**(严重度:中,置信度:高)
- 我方:`bossAI_lunar_misc.ts:785-791`(477)与 `:1039-1040`(479),仅 `!p` 才 -1
- 原版:`NPC.cs:39886-39901`(477,`:39895` 为 `dead || Length() > 3000f` → -1)与 `:40485-40496`(479,`:40489` 同款)
- 症状:玩家活着但拉开 3000px 时,原版飞蛾会转入无敌爬升离场,我方继续悬顶/追击,脱战语义缺失。
- 最小修复:两处目标门补 `else if (Math.hypot(...) > 3000) e.ai0 = -1;`(与 !p 同级)。

**#4 LunarOrb 539 父体死亡后延迟最多 ~160t 才冲刺**(严重度:中低,置信度:高)
- 我方:`bossAI_lunar_misc.ts:1849-1860`——`ai0 < orbitT && alive` 为假时直接落空,只有 `ai0 === orbitT` 恰好相等才取最近玩家冲刺;父亡后要等自己的 ai0 慢慢数到 210。
- 原版:`Projectile.cs:32103-32109`——父体失活即 `this.ai[0] = num851`(立即置 210)→ 当 tick 就进入取玩家方向 16 速冲刺。
- 症状:清塔时常杀 407,残留 539 会沿旧速度漂 0-3 秒才转向,期间不构成威胁(原版立即变轨扑人)。
- 最小修复:orbit 分支加 `if (!alive) this.ai0 = orbitT;`(539 专用;574 维持父亡即亡)。

**#5 蛾卵 478 受击扣减的负值进度被哨兵钳清零**(严重度:低,置信度:高)
- 我方:`bossAI_lunar_misc.ts:980`(`if (e.ai0 < 0) e.ai0 = 0` 在 :988-991 的 justHit 扣减**之前**每 tick 执行)
- 原版:`NPC.cs:40419-40425`(ai[0] 可自由累积为负,孵化阈值 900 不变)
- 症状:早期( ai0<40 )反复击打蛾卵时,原版每击最多推迟 40t 孵化且可无限累积,我方次日晨即钳回 0 → 孵化比原版早(10 击约早 6.5s)。
- 最小修复:把钳位改成一次性哨兵归一,如 `if (e.ai0 <= -1000) e.ai0 = 0;`(只拦 Enemy -1120 初值),放行受击产生的小负值。

**#6 悬浮脑 420 瞬移时环绕球无条件 -30,原版有"负计时球在场则跳过"门**(严重度:低,置信度:中)
- 我方:`bossAI_lunar_misc.ts:1574-1583`(注释断言原版 flag105 门"恒假 → 恒全量")
- 原版:`NPC.cs:41673-41691`——`!(ai[0] >= 0f)` 即任意 574 计时为负时 flag105=false,跳过全量 -30
- 症状:断言不成立:球刚发完 576(计时归 0)后 30t 内瞬移,-30 会把计时打成负,下一次瞬移原版跳过加速、我方仍叠加,连环瞬移时 576 发射比原版更密。
- 最小修复:`orbs` 循环前先查是否存在 `o.ai0 < 0`(需给 LunarOrb 暴露只读计时),有则本轮不 delay。

## 存疑 / 备案(不列为 CONFIRMED)

- **455 死光伤害 ×2 口径**:游离眼传 `50*2`(:300)、核心 `50*2`、头 `75*2`(duke 文件),而 vanilla 三处为 50/50/75(:38639/:37904);MLDeathray 直接 `game.damagePlayer(this.dmg)`,同文件 462/454/452/576 均按原版裸值传。若非有意补偿 iframes 节流,死光伤害是原版两倍——建议向调用方确认该口径是否有登记。
- 花岗岩 483 双段锚升级条件我方用 `|dy|>8`(:1154),原版复用列距 `|dx|>8`(:40734-40742,疑似原版笔误);starCellAI 同构处(:1309)已照抄原版怪癖,两处口径不一致。
- 石碑 526 归巢投射物降级为粒子、421 吸附期保持可见(hide 未抄)、539 冲刺段姿态恒用盘旋档、蛾卵/邪教徒落点顶锚 vs 底锚、421 态 1 吸附瞬移高 h/2、539 自爆缺 SoundID 4 style 7、飞蛾魔 180t 选招单掷近似(原版同 tick while 重摇)——均为代码内已登记的近似,视觉/音效级,无行为链问题。

其余各族(游离眼、水蛭、仪式链、幻影、花岗岩、星细胞族、小星细胞、水流入侵者、日耀黏液、爬尾虫)未发现结构性偏差。
```
