# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T09:23:47.926Z

```
你在 ~/Project/GLM/SandboxWorld/ 项目（工作目录 game/）。Terraria 复刻，1:1 对齐 Terarria1456/。**诊断并修复玩家微光湖失灵**。

用户实测（硬刷新后）：进微光湖后①仍能自由行走（原版 buff 353 应封输入）②左上角无 debuff 图标 ③怪物也能进湖（无法攻击角色——伤害免疫生效了，说明 shimmering 部分路径在跑）。

关键背景：`src/entities/Player.ts` 刚被并行会话大规模重写（矿车 ridingCart/装备聚合 equipStats/星云甲虫等，文件 1700+ 行，行号整体漂移）。此前微光实现（约旧 :699-730 区域）：
- `inShimmer = liquidType[centerIdx]===4 && liq>30`；`shimmering = inShimmer && y/TILE < lavaLine`
- `if (this.shimmering) this.buffs.apply(BuffType.Shimmered, 1)`（buff 图标，我刚加的）
- 物理 else-if 链：`if (this.inShimmer && !this.shimmering) {轻浮}` `else if (this.shimmering) { inputX/inputJump/inputUp/inputDown 清零 + 慢沉 }`
- timeShimmering 累积 + shimmerUnstuck 传送（findShimmerFreeSpot 三层兜底）

"伤害免疫生效但能行走"= shimmering=true 但**输入清零没生效**——最可疑：并行重写后①物理分支顺序变了（微光分支排在移动积分之后或被 return 提前跳过）②或清零后 Game 在 fixedUpdate 之后又重写 inputX 并做第二次移动 ③或 `centerIdx` 采样点变了。逐项核对：

1. **读当前 Player.ts 全文**（重点 fixedUpdate 主干顺序）：liquid 采样/inShimmer/shimmering/物理 else-if 链/输入清零的实际位置与执行顺序；确认我的 buffs.apply(Shimmered) 是否幸存；确认 BuffType.Shimmered=77 枚举与 UI.ts 图标映射 `[BuffType.Shimmered, 'vi_5340_galaxy_pearl']` 是否还在（UI.ts :2498 附近当时因两处重复没插上——检查是否真的没插！我上次 Edit 失败后被打断，**图标映射可能根本没加上**——若缺则补两处 map 都加）。
2. **执行顺序修**：确保 清零发生在移动消费之前；若并行版把输入清零放到了移动之后或被矿车分支提前 return 绕过（ridingCart 分支 return 前要检查微光？原版矿车上微光仍生效）——按原版 Player.Update 顺序（微光物理在主移动链内）修。
3. **怪物进湖**：对照原版——Enemy 浸微光 90t 会转化/消散（NPC.cs:92502 GetShimmered，我们已实现 Enemy shimmerWet/shimmerTransparency）——若敌怪进湖既不转化也不受影响，查 Enemy 侧微光浸入判定是否被并行改动弄丢；原版敌怪物理上可以走进湖（无 avoidShimmer），但 90t 后应触发转化——核实链路是否活着。
4. **写一个探针测试**锁定回归：构造微光池+Player 跑 fixedUpdate 断言 inputX 清零+buffs 含 Shimmered+不可位移；Enemy 浸入 90t 转化。加进 tests/shimmer.test.ts 或新文件。
5. 验证：tsc 零新增（忽略并行在制品）；vitest tests/shimmer.test.ts 全绿。

报告 ≤25 行：根因（并行重写破坏点）/修复内容/图标映射状态/探针数字。
```

---

## 📎 Attachment · skill_listing · 2026-08-12T09:23:47.934Z

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

## 🤖 Assistant · 2026-08-12T09:23:52.856Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by reading the current Player.ts to understand the structure after the parallel rewrite. The file is 1700+ lines, so I'll read it fully, and in parallel check UI.ts icon mapping and the Enemy shimmer logic.

Let me plan:
1. Read src/entities/Player.ts (full).
2. Grep UI.ts for BuffType.Shimmered / vi_5340_galaxy_pearl.
3. Grep Enemy shimmer.
4. Grep BuffType enum for Shimmered.
5. Check tests/shimmer.test.ts existence.

Let me do these in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:23:52.857Z · glm-x-preview-260804

```
我先并行读取 Player.ts 全文，并检查 UI.ts 图标映射、BuffType 枚举、Enemy 微光逻辑和现有测试。
```


---

## 🤖 Assistant · 2026-08-12T09:23:52.858Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Player.ts"
}
```


---

## 🤖 Assistant · 2026-08-12T09:23:52.943Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Shimmered\\|shimmer\" ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts | head -50",
 "description": "Search UI.ts for Shimmered buff icon mapping"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:23:52.985Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 👤 User(sidechain) · 2026-08-12T09:23:53.028Z

**📎 ToolResult**

```
1	// 玩家实体：移动、跳跃、游泳、Buff/配饰属性聚合、摔伤
2	import { Entity } from './Entity';
3	import type { GameHooks } from './types';
4	import {
5	  GRAVITY, MAX_FALL_SPEED, PLAYER_WALK_ACCEL, PLAYER_WALK_MAX,
6	  PLAYER_FRICTION, PLAYER_AIR_FRICTION, PLAYER_JUMP_SPEED, PLAYER_JUMP_TICKS,
7	  PLAYER_IFRAME_TICKS, TILE,
8	} from '../core/constants';
9	import { moveAndCollide } from '../physics/TileCollision';
10	import { Inventory, ACC_ARMOR_START } from '../items/Inventory';
11	import { BuffState, BuffType } from '../stats/Buffs';
12	import { LuckState } from '../stats/Luck';
13	import { ITEM_DEFS, VANILLA_ITEM_KEY_BY_ID } from '../data/items';
14	import { statOfInternal } from '../data/vanillaItemStats';
15	import { wingStatOf } from '../data/vanillaWingStats';
16	import { accFxOfInternal } from '../data/vanillaAccFx';
17	import { ARMOR_SET_BONUSES } from '../data/vanillaArmorSets';
18	import { SUMMON_GEAR, SUMMON_SET, type SummonSetFx } from '../data/vanillaSummonStats';
19	import { TILE_DEFS, TILE_BY_KEY } from '../data/tiles';
20	import { hurtTiles, liquidCollision, TOUCH_IMMEDIATE, TOUCH_HOT, TOUCH_BLEEDING, SUFFOCATE, TOUCH_DESTROY, type HurtTile } from '../stats/TouchDamage';
21	import { findShimmerFreeSpot, shimmerTeleportPos } from '../stats/Shimmer';
22	
23	// 摔伤参数（移植自 Maples Player.Fall，单位换算为 tile）
24	// 对齐原版体感：跳跃/小坡绝不受伤（原版约 25 格起伤）；落水另行豁免
25	const FALL_SAFE_TILES = 22;
26	const FALL_FATAL_TILES = 45;
27	
28	// 沙族地格集合（TileID.Sets.Conversion：Sand{53,112,116,234} / HardenedSand{397,398,399,402}
29	// / Sandstone{396,400,401,403}——TileID.cs:30-34）。53/396/397 是本地基础方块键。
30	const SAND_FLOOR_IDS = new Set<number>([
31	  'sand', 'sandstone', 'hardened_sand',
32	  'v_112_ebonsand_block', 'v_116_pearlsand_block', 'v_234_crimsand_block',
33	  'v_398_corrupt_hardened_sand_block', 'v_399_crimson_hardened_sand_block',
34	  'v_402_hallow_hardened_sand_block', 'v_400_corrupt_sandstone_block',
35	  'v_401_crimson_sandstone_block', 'v_403_hallow_sandstone_block',
36	].map((k) => TILE_BY_KEY[k] ?? 0).filter((id) => id > 0));
37	
38	export class Player extends Entity {
39	  w = 20; h = 42;        // 原版 Player 构造(Player.cs:55083-55084 width=20 height=42;
40	                         // ResizeHitbox :28744 同值)。曾 16×39(窄 4px 矮 3px)——
41	                         // 精灵帧 40×56 已对齐,盒偏小导致判定区比视觉小一圈
42	  facing = 1;            // 1 右 -1 左
43	  baseMaxHp = 100;
44	  baseMaxMana = 20;   // 原版 statManaMax2 起步 20,坠落之星 +20/颗(上限 200)
45	  mana = 20;
46	  /** 奥术水晶（item 5339 使用后永久旗标，Player.cs:44780-44783）——本仓 5339 尚无使用
47	   *  链路，恒 false；接使用系统后置 true 即自动进回复模型（:19242/:19259） */
48	  usedArcaneCrystal = false;
49	  /** 魔力蓄能（Player.manaRegenCount :1824，UpdateManaRegen :19274 累积 ≥120 +1 魔） */
50	  manaRegenCount = 0;
51	  /** 用魔惩罚期（Player.manaRegenDelay :1826，float）：>0 时每帧产额 0（:19270-19271） */
52	  manaRegenDelay = 0;
53	  /** 用魔物品动画窗剩余 tick（itemAnimation>0 期每帧重置 delay，:42131-42137） */
54	  manaAnimTicks = 0;
55	  hp = 100;
56	  /** 最近一次伤害死因（PlayerDeathReason 语义子集）——死亡瞬间由 Game 消费生成原版死亡文本 */
57	  lastDamageCause: import('../i18n/RandomText').DeathCause | null = null;
58	  inv: Inventory;
59	  /** 玩家储物（原版 Player.cs:1468-1474 Chest.CreateBank(-2..-5)，各 40 槽）：
60	   *  [0]=bank 存钱罐(29) / [1]=bank2 保险箱(97) / [2]=bank3 守护者熔炉(463) /
61	   *  [3]=bank4 虚空保险库(491)——右键绑定见 Player.cs:32598+。内容随玩家存档，
62	   *  方块破坏不丢内容（原版同语义，掉落回收 place_v_ 物品） */
63	  banks: Array<Array<{ id: number; stack: number } | null>> = [
64	    Array(40).fill(null), Array(40).fill(null), Array(40).fill(null), Array(40).fill(null),
65	  ];
66	  buffs = new BuffState();
67	  /** 角色外观（来自角色系统；渲染层 M7 切换 PaperDoll 时使用） */
68	  appearance?: import('../player/Appearance').Appearance;
69	  iframes = 0;
70	  jumpHold = 0;          // 长按跳跃剩余加速 tick
71	  inWater = false;
72	  headUnderwater = false;
73	  /** 税务员累积税款（Player.cs:792 taxMoney，铜币；对话「收集」领取） */
74	  taxMoney = 0;
75	  /** PVE 死亡计数（Player.numberOfDeathsPVE，PL:53840；存档 player 段持久化） */
76	  deathsPve = 0;
77	  /** 收税计时（Player.cs:793 taxTimer；taxRate=3600 即每游戏小时一结） */
78	  taxTimer = 0;
79	  /** 蜂蜜浸入（原版 honeyWet，Player.cs:27436-27438）：授予 Honey buff(48,1800t) 的来源 */
80	  inHoney = false;
81	  /** 微光浸入（原版 shimmerWet，Player.cs:27420-27424：Collision.shimmer 盒命中） */
82	  inShimmer = false;
83	  /** 微光化态（buff 353，Player.cs:11381-11388）：frozen 封输入 + fallStart 重置 +
84	   *  受击免疫（Hurt :37591-37595 直接 0）+ 慢沉（:24117-24119 ×0.9） */
85	  shimmering = false;
86	  /** 微光滞留 tick（TryToShimmerUnstuck :28378：钳 0-7200，shimmering +1/否则 -10） */
87	  timeShimmering = 0;
88	  // 气口：5 个气泡，共 23.33 秒（原版参数），每颗 ≈4.67 秒
89	  static readonly BREATH_BUBBLES = 5;
90	  static readonly BREATH_SECONDS = 23.33;
91	  breath = Player.BREATH_BUBBLES;
92	  private breathAccum = 0;
93	  private drownAccum = 0;
94	  inLava = false;
95	  private lavaAccum = 0;
96	  animTime = 0;          // 走路动画计时
97	  useTime = 0;           // 通用动作冷却
98	  dead = false;
99	  respawnTimer = 0;
100	  /** 死亡画面淡入（Player.cs:16873：dead 时 +2/tick 钳 255；GetDeathAlpha :53284 消费） */
101	  immuneAlpha = 0;
102	  // 摔伤追踪
103	  fallStartY: number | null = null;   // 矿车骑乘同步清空（车上不计摔伤），公开给 Minecart
104	  /** 蛛网挣扎计数（原版 stickyBreak，Player.cs:22653） */
105	  private stickyBreak = 0;
106	  private surfaceJumpCd = 0;  // 水面起跳冷却
107	  sinceHurt = 0;               // 距上次受击 tick（自然回血计时；渲染层读取做心心跳动效）
108	  /** 本 tick 落地冲击速度（碰撞前 vy≥3 落地才非 0；Game 消费：起爆器 411 坠落触发） */
109	  landImpactVy = 0;
110	  private regenAccum = 0;
111	  stepRenderY = 0;             // 跨台阶的渲染高度补偿（缓动到 0，消除瞬移顿挫）
112	  stepUp = true;               // Collision.StepUp 自动上台阶（moveAndCollide 内消费）
113	  /** 鞭命中授予的玩家 buff（WhipTagEffect.PlayerBuffId → 剩余 tick；
114	   *  效果实装（:9790-9802）：311 镰鞭=鞭攻速+35%、308 剑鞭=+25%、314 荆棘鞭=+12%
115	   *  ——Game 鞭 useTime 结算读取；312/365 登记持续期（效果端暂不接） */
116	  whipBuffs: Record<number, number> = {};
117	  /** 右键集火目标（MinionAttackTargetNPC，Player.cs:48952：召唤杖右键指定，
118	   *  随从索敌优先；-1=无。失效：死亡或离玩家 >3000px——随从侧判定） */
119	  minionTargetId = -1;
120	  /** 星云三族等级（0-3，各自独立 480t；NebulaLevelup :56091-56121 逐级升/降）：
121	   *  0=伤害 179-181（四系 +15%/级）1=生命 173-175（lifeRegen +6/级）2=魔力 176-178 */
122	  nebula = [0, 0, 0];
123	  private nebulaT = [0, 0, 0];
124	  private nebulaManaAccum = 0;
125	  private nebulaLifeAccum = 0;
126	  /** NebulaLevelup（:56091-56121）：本族 +1 级 cap3，满 480t 重置（拾取驱动） */
127	  nebulaLevelup(family: 0 | 1 | 2): void {
128	    this.nebula[family] = Math.min(3, this.nebula[family] + 1);
129	    this.nebulaT[family] = 480;
130	  }
131	  /** 甲虫攻击球（0-3）：近战命中蓄能，受击掉一颗 */
132	  beetleOrbs = 0;
133	  private beetleCharge = 0;
134	  /** 近战续航窗口（onMeleeHit 刷新；fixedUpdate 内蓄能消费） */
135	  private lastMeleeTick = 0;
136	  /** 潜行 0(可见)-1(满)：蘑菇矿=移动蓄/星璇=双击↓开关（:25500/:25542） */
137	  stealth = 0;
138	  private stealthTimer = 0;
139	  vortexStealthActive = false;
140	  private prevDown = false;
141	  private downTapT = 0;
142	  private sharpenedCd = 0;
143	  /** BOC 受击脉冲（fixedUpdate 消费：buff 321 + 困惑近敌） */
144	  bocPulse = 0;
145	  /** 联机远端位置平滑偏移（原版 Player.netOffset，MessageBuffer.cs case 13 注入、
146	   *  Player.UpdateNetOffset :28240 衰减）：模拟位置与权威快照的差，渲染时叠加。
147	   *  本地玩家恒 0 */
148	  netOffX = 0;
149	  netOffY = 0;
150	  /** 联机远端挥舞动画（msg13 useItem 位驱动；Game 派生，Renderer 以 swing 参数消费）。
151	   *  本地玩家不用（本地走 Game.swing） */
152	  swingNet: { t: number; dur: number; item: number } | null = null;
153	  /** 矿车骑乘中（原版 mount.Active && mount.Cart）：常规移动/跳跃/重力由 Minecart
154	   *  实体接管（Player.cs:27783-27850 TrackCollision 段），fixedUpdate 提前返回；
155	   *  渲染层消费本标志取坐姿帧（mount.BodyFrame=3）并叠画车身 */
156	  ridingCart = false;
157	  /** 当前所骑矿车（渲染层叠画车身/倾角用；Game 挂载） */
158	  cart: import('./Minecart').Minecart | null = null;
159	
160	  constructor(x: number, y: number, inv: Inventory) {
161	    super();
162	    this.x = x; this.y = y;
163	    this.inv = inv;
164	  }
165	
166	  // ---- 配饰效果（重算式聚合，幂等）----
167	  get hasHorseshoe(): boolean {
168	    for (let i = ACC_ARMOR_START; i < ACC_ARMOR_START + 7; i++) { // armor[3-9] 配饰槽（原版 Player.cs:36326）
169	      const s = this.inv.armor[i];
170	      if (s && ITEM_DEFS[s.id]?.accessory === 'lucky_horseshoe') return true;
171	    }
172	    return false;
173	  }
174	  get hasFeralClaws(): boolean {
175	    for (let i = ACC_ARMOR_START; i < ACC_ARMOR_START + 7; i++) {
176	      const s = this.inv.armor[i];
177	      if (s && ITEM_DEFS[s.id]?.accessory === 'feral_claws') return true;
178	    }
179	    return false;
180	  }
181	  /** 防御 = 基础(0) + 盔甲/配饰（含 vi_ 表防御+accfx def+词缀 62-65）+ 铁皮 Buff(+6)（时装不计） */
182	  get defense(): number {
183	    let d = this.buffs.defenseBonus + this.equipStats.def;
184	    for (const id of this.inv.equippedArmor()) {
185	      if (id != null) d += ITEM_DEFS[id]?.armor?.defense ?? statOfInternal(id)?.def ?? 0;
186	    }
187	    return d;
188	  }
189	
190	  /** 装备数值聚合（GrantArmorBenefits/ApplyEquipFunctional/GrantPrefixBenefits 可移植切片）。
191	   *  覆盖：配饰防御/魔力/回复/移速/近战速度/全系伤害/暴击 + 词缀 62-80 效益；
192	   *  行为型效果（火箭靴飞行/熔岩护身等）不在内。每帧重算式聚合，幂等 */
193	  get equipStats(): {
194	    def: number; mana: number; hpPerSec: number;
195	    dmgMelee: number; dmgRanged: number; dmgMagic: number;
196	    critMelee: number; critRanged: number; critMagic: number;
197	    moveMult: number; meleeSpeed: number;
198	    extraFall: number; lavaMax: number; armorPen: number;
199	    rocketBoots: number; autoJump: boolean; fireWalk: boolean;
200	    noKnockback: boolean; noFallDmg: boolean; desertBoots: boolean;
201	    waterWalk: boolean; jumpBoost: boolean; panic: boolean; starCloak: boolean;
202	    jumpOpts: string[];
203	    wing: { logic: number; time: number; accSpeed: number; accelMult: number; hover: boolean } | null;
204	    dash: number; blackBelt: boolean; bees: boolean; carpet: boolean;
205	    jumpSpd: number; flipper: boolean; longInvince: boolean; spikedBoots: boolean;
206	    treasureMagnet: boolean; goldRing: boolean; luckyCoin: boolean; discount: boolean;
207	    arrowDmg: number; ammoSave: boolean; kbGlove: boolean; yoyoString: boolean;
208	    quiver: boolean;
209	    moltenQuiver: boolean;
210	    arrowStack: number;      // 箭袋 additiveStack（仅箭，:14785）
211	    shroomiteType: 'arrow' | 'bullet' | 'rocket' | null;
212	    shroomiteSet: boolean; vortexSet: boolean; nebulaSet: boolean; beetleOff: boolean;
213	    beetleDef: boolean;
214	    wolfAcc: boolean; boc: boolean;
215	    tileSpeed: boolean; wallSpeed: boolean; tileRange: boolean; pStone: boolean;
216	    counterWeight: boolean; manaMagnet: boolean; magicCuffs: boolean; manaFlower: boolean;
217	    manaRegenBonus: number; manaRegenDelayBonus: number;
218	    setBonus: ReturnType<typeof activeArmorSetBonus> | null;
219	    manaCostMul: number;
220	    // ---- 召唤师链（vanillaSummonStats：ApplyEquipFunctional type if-chain 1:1）----
221	    minionSlots: number;   // maxMinions += N（散件+套装合计）
222	    minionDmg: number;     // minionDamage += X（加算乘区，散件+套装合计）
223	    minionKB: number;      // minionKB += N
224	    sentrySlots: number;   // maxTurrets += N
225	    whipRange: number;     // whipRangeMultiplier += X
226	    whipSpd: number;       // 鞭 useTime 倍率（黑曜套 1/1.15）
227	    summonSet: SummonSetFx | null;
228	  } {
229	    /** 当前套装匹配（armor[0-2] 的 hs/bs/ls 槽序号 → ARMOR_SET_BONUSES；通配 `${hs}|${bs}|*` 兜底） */
230	    function activeArmorSetBonus(self: Player) {
231	      const st0 = statOfInternal(self.inv.armor[0]?.id ?? -1);
232	      const st1 = statOfInternal(self.inv.armor[1]?.id ?? -1);
233	      const st2 = statOfInternal(self.inv.armor[2]?.id ?? -1);
234	      if (!st0?.hs || st1?.bs === undefined || st2?.ls === undefined) return null;
235	      return ARMOR_SET_BONUSES[`${st0.hs}|${st1.bs}|${st2.ls}`]
236	        ?? ARMOR_SET_BONUSES[`${st0.hs}|${st1.bs}|*`] ?? null;
237	    }
238	    let def = 0, mana = 0, life = 0;
239	    let dmgMelee = 0, dmgRanged = 0, dmgMagic = 0;
240	    let critMelee = 0, critRanged = 0, critMagic = 0;
241	    let move = 0, meleeSpeed = 0, runSpeed = 0;
242	    // 魔力回复直值（ApplyEquipFunctional if-chain :14379-14383——魔力斗篷 982 专属）
243	    let manaRegenBonus = 0, manaRegenDelayBonus = 0;
244	    let extraFall = 0, lavaMax = 0, armorPen = 0, rocketBoots = 0;
245	    let autoJump = false, fireWalk = false, noKnockback = false, noFallDmg = false;
246	    let desertBoots = false, waterWalk = false, jumpBoost = false, panic = false, starCloak = false;
247	    const jumpSet = new Set<string>();
248	    let wing: { logic: number; time: number; accSpeed: number; accelMult: number; hover: boolean } | null = null;
249	    let dash = 0, blackBelt = false, bees = false, carpet = false;
250	    let jumpSpd = 0, arrowDmg = 0;
251	    let equipHasQuiver = false;
252	    let wolfAcc = false, boc = false;
253	    let moltenQuiver = false;
254	    let shroomiteType: 'arrow' | 'bullet' | 'rocket' | null = null;
255	    let shroomiteSet = false, vortexSet = false, nebulaSet = false, beetleOff = false;
256	    let beetleDef = false;
257	    let flipper = false, longInvince = false, spikedBoots = false;
258	    let treasureMagnet = false, goldRing = false, luckyCoin = false, discount = false;
259	    let ammoSave = false, kbGlove = false, yoyoString = false;
260	    let tileSpeed = false, wallSpeed = false, tileRange = false, skyStone = false, pStone = false, counterWeight = false;
261	    let manaMagnet = false, magicCuffs = false, manaFlower = false;
262	    let manaCostMul = 1;
263	    for (let i = ACC_ARMOR_START; i < ACC_ARMOR_START + 7; i++) {
264	      const s = this.inv.armor[i];
265	      if (!s) continue;
266	      const fx = accFxOfInternal(s.id);
267	      // 翅膀（Item.wingSlot>0 → WingStatsInitializer 全字段；多翅膀取首个）
268	      const wingSlot = statOfInternal(s.id)?.wing;
269	      if (wingSlot && wingSlot > 0 && !wing) {
270	        const ws = wingStatOf(wingSlot);
271	        wing = { logic: wingSlot, time: ws.time, accSpeed: ws.accSpeed, accelMult: ws.accelMult, hover: ws.hover };
272	      }
273	      // 悠悠球线（Item.stringColor>0 → yoyoString，Player.cs:14170）
274	      if (statOfInternal(s.id)?.str) yoyoString = true;
275	      // 生命回复优先取 Item.lifeRegen 字段（再生手环族，GrantArmorBenefits :12700），
276	      // accfx.life 为 if-chain 段的 lifeRegen += N
277	      const itemLife = statOfInternal(s.id)?.life ?? 0;
278	      if (itemLife) life += itemLife;
279	      if (fx) {
280	        if (fx.def) def += fx.def;
281	        if (fx.mana) mana += fx.mana;
282	        if (fx.life) life += fx.life;
283	        if (fx.move) move += fx.move;
284	        if (fx.meleeSpd) meleeSpeed += fx.meleeSpd;
285	        if (fx.runSpeed) runSpeed = Math.max(runSpeed, fx.runSpeed);
286	        if (fx.dmgMelee) dmgMelee += fx.dmgMelee;
287	        if (fx.dmgRanged) dmgRanged += fx.dmgRanged;
288	        if (fx.dmgMagic) dmgMagic += fx.dmgMagic;
289	        if (fx.dmgAll) { dmgMelee += fx.dmgAll; dmgRanged += fx.dmgAll; dmgMagic += fx.dmgAll; }
290	        if (fx.critMelee) critMelee += fx.critMelee;
291	        if (fx.critRanged) critRanged += fx.critRanged;
292	        if (fx.critMagic) critMagic += fx.critMagic;
293	        // ---- 行为型（ApplyEquipFunctional 布尔/数值字段）----
294	        if (fx.extraFall) extraFall += fx.extraFall;
295	        if (fx.lavaMax) lavaMax += fx.lavaMax;       // 熔岩护身符族：叠加（lavaMax += 420）
296	        if (fx.armorPen) armorPen += fx.armorPen;
297	        if (fx.rocketBoots) rocketBoots = Math.max(rocketBoots, fx.rocketBoots);
298	        if (fx.autoJump) autoJump = true;
299	        if (fx.fireWalk) fireWalk = true;
300	        if (fx.noKnockback) noKnockback = true;
301	        if (fx.noFallDmg) noFallDmg = true;
302	        if (fx.desertBoots) desertBoots = true;
303	        if (fx.waterWalk || fx.waterWalk2) waterWalk = true;
304	        if (fx.jumpBoost) jumpBoost = true;
305	        if (fx.panic) panic = true;
306	        if (fx.starCloak) starCloak = true;
307	        if (fx.dashType) dash = Math.max(dash, fx.dashType);
308	        if (fx.blackBelt) blackBelt = true;
309	        if (fx.bees) bees = true;
310	        if (fx.carpet) carpet = true;
311	        if (fx.jumpSpd) jumpSpd = Math.max(jumpSpd, fx.jumpSpd);
312	        if (fx.arrowDmg) arrowDmg += fx.arrowDmg; // 箭袋 +0.1（仅箭吃，见 rangedDamageMult）
313	        if (fx.nightWolf) wolfAcc = true;
314	        if (fx.quiver) equipHasQuiver = true;
315	        if (fx.moltenQuiver) moltenQuiver = true;
316	        if (fx.brainOfConfusion) boc = true;
317	        if (fx.flipper) flipper = true;
318	        if (fx.longInvince) longInvince = true;
319	        if (fx.spikedBoots) spikedBoots = true;
320	        if (fx.treasureMagnet) treasureMagnet = true;
321	        if (fx.goldRing) goldRing = true;
322	        if (fx.luckyCoin) luckyCoin = true;
323	        if (fx.discount) discount = true;
324	        if (fx.ammoSave || fx.huntressSave) ammoSave = true;
325	        if (fx.kbGlove) kbGlove = true;
326	        if (fx.yoyoString) yoyoString = true;
327	        if (fx.tileSpeed) tileSpeed = true;
328	        if (fx.wallSpeed) wallSpeed = true;
329	        if (fx.tileRange) tileRange = true;
330	        if (fx.skyStone) skyStone = true;
331	        if (fx.pStone) pStone = true;
332	        if (fx.manaMagnet) manaMagnet = true;
333	        if (fx.magicCuffs) magicCuffs = true;
334	        if (fx.manaFlower) manaFlower = true;
335	        if (fx.manaRegenBonus) manaRegenBonus += fx.manaRegenBonus;           // 魔力斗篷 982（:14383）
336	        if (fx.manaRegenDelayBonus) manaRegenDelayBonus += fx.manaRegenDelayBonus; // 982（:14382）
337	        if (fx.counterWeight) counterWeight = true;
338	        for (const j of fx.jumpOpts ?? []) jumpSet.add(j);
339	      }
340	      // 词缀效益（GrantPrefixBenefits :13531：配饰前缀 62-80）
341	      const p = s.prefix;
342	      if (p && p >= 62 && p <= 80) {
343	        if (p <= 65) def += p - 61;              // 62-65：+1..4 防御
344	        else if (p === 66) mana += 20;           // Arcane：魔力 +20
345	        else if (p === 67) { critMelee += 2; critRanged += 2; critMagic += 2; }
346	        else if (p === 68) { critMelee += 4; critRanged += 4; critMagic += 4; }
347	        else if (p >= 69 && p <= 72) dmgMelee += dmgRanged += dmgMagic += (p - 68) / 100; // 69-72：+1..4% 全伤
348	        else if (p <= 76) move += (p - 72) / 100; // 73-76：+1..4% 移速
349	        else meleeSpeed += (p - 76) / 100;        // 77-80：+1..4% 近战速度
350	      }
351	    }
352	    // 恐慌项链受击加速窗口（PanicSpeedBoost :25034：panicTime 300 tick 内 moveSpeed +0.5）
353	    if (this.panicTime > 0) move += 0.5;
354	    // runSpeed：accRunSpeed=6 vs 基础 maxRunSpeed=3 → 移速倍率贡献（取最高不叠）
355	    const moveMult = 1 + move + (runSpeed > 0 ? runSpeed / 3 - 1 : 0);
356	    // 多段跳按原版优先序排列（JumpMovement 消费序）
357	    const JUMP_ORDER = ['Cloud', 'Sail', 'Sandstorm', 'Blizzard', 'Fart', 'Tsunami', 'Unicorn', 'Basilisk', 'WallOfFleshGoat', 'Santank'];
358	    const jumpOpts = JUMP_ORDER.filter((j) => jumpSet.has(j));
359	    // ---- 召唤师链（vanillaSummonStats：ApplyEquipFunctional armor[0-9] 单遍语义 =
360	    //      盔甲三件 + 配饰各扫一遍 SUMMON_GEAR；套装查 SUMMON_SET）----
361	    let minionSlots = 0, minionDmg = 0, minionKB = 0, sentrySlots = 0, whipRange = 0;
362	    // 原版 ApplyEquipFunctional armor[0-9] 单遍 = 盔甲三件 + 配饰各扫（SummonFx 同表直查）
363	    const sumFx = (s: { id: number } | null): void => {
364	      if (!s) return;
365	      const d = ITEM_DEFS[s.id];
366	      const vid = d?.vid ?? (d?.key.startsWith('vi_') ? parseInt(d.key.slice(3), 10) : -1);
367	      const fx = vid >= 0 ? SUMMON_GEAR[vid] : undefined;
368	      if (!fx) return;
369	      if (fx.slot) minionSlots += fx.slot;
370	      if (fx.sentry) sentrySlots += fx.sentry;
371	      if (fx.dmg) minionDmg += fx.dmg;
372	      if (fx.kb) minionKB += fx.kb;
373	      if (fx.whipRange) whipRange += fx.whipRange;
374	    };
375	    for (let i = 0; i < 3; i++) sumFx(this.inv.armor[i]);
376	    // 套装/头盔 type 检测（vid 直查）：蘑菇矿头 1546箭/1547弹/1548火箭（:13274-13288）
377	    const aVid = (i: number): number => {
378	      const d = ITEM_DEFS[this.inv.armor[i]?.id ?? -1];
379	      return d?.vid ?? (d?.key?.startsWith('vi_') ? parseInt(d.key.slice(3), 10) : -1);
380	    };
381	    const [hVid, bVid, lVid] = [aVid(0), aVid(1), aVid(2)];
382	    if (hVid === 1546) shroomiteType = 'arrow';
383	    else if (hVid === 1547) shroomiteType = 'bullet';
384	    else if (hVid === 1548) shroomiteType = 'rocket';
385	    shroomiteSet = (hVid >= 1546 && hVid <= 1548) && bVid === 1549 && lVid === 1550;
386	    vortexSet = hVid === 2757 && bVid === 2758 && lVid === 2759;
387	    nebulaSet = hVid === 2760 && bVid === 2761 && lVid === 2762;
388	    beetleOff = hVid === 2199 && bVid === 2200 && lVid === 2202; // 进攻甲
389	    beetleDef = hVid === 2199 && bVid === 2201 && lVid === 2202; // 防御甲（壳：beetleEndurance 15%/球）
390	    for (let i = ACC_ARMOR_START; i < ACC_ARMOR_START + 7; i++) sumFx(this.inv.armor[i]);
391	    // 盔甲套装加成（vanillaArmorSets.ts：槽序号三键匹配）
392	    const sb = activeArmorSetBonus(this);
393	    if (sb) {
394	      if (sb.def) def += sb.def;
395	      if (sb.mana) mana += sb.mana;
396	      if (sb.move) move += sb.move;
397	      if (sb.meleeSpd) meleeSpeed += sb.meleeSpd;
398	      if (sb.dmgMelee) dmgMelee += sb.dmgMelee;
399	      if (sb.dmgRanged) dmgRanged += sb.dmgRanged;
400	      if (sb.dmgMagic) dmgMagic += sb.dmgMagic;
401	      if (sb.critMelee) critMelee += sb.critMelee;
402	      if (sb.critRanged) critRanged += sb.critRanged;
403	      if (sb.critMagic) critMagic += sb.critMagic;
404	      if (sb.noKnockback) noKnockback = true;
405	      if (sb.fireWalk) fireWalk = true;
406	      if (sb.ammoCost80) ammoSave = true;
407	      if (sb.manaCostMul !== undefined) manaCostMul = sb.manaCostMul;
408	    }
409	    // 召唤系套装（SUMMON_SET 槽序键；散件效果已在上扫，此处只叠套装层）
410	    const summonSet = (() => {
411	      const st0 = statOfInternal(this.inv.armor[0]?.id ?? -1);
412	      const st1 = statOfInternal(this.inv.armor[1]?.id ?? -1);
413	      const st2 = statOfInternal(this.inv.armor[2]?.id ?? -1);
414	      if (!st0?.hs || st1?.bs === undefined || st2?.ls === undefined) return null;
415	      const s = SUMMON_SET[`${st0.hs}|${st1.bs}|${st2.ls}`] ?? SUMMON_SET[`${st0.hs}|${st1.bs}|*`];
416	      if (!s) return null;
417	      if (s.slot) minionSlots += s.slot;
418	      if (s.sentry) sentrySlots += s.sentry;
419	      if (s.dmg) minionDmg += s.dmg;
420	      if (s.whipRange) whipRange += s.whipRange;
421	      return s;
422	    })();
423	    // 天界石族复合（Player.cs:12558-12570：life+2/def+4/近战速+10%/全系伤+10%/全系暴+2%）
424	    if (skyStone) {
425	      life += 2; def += 4; meleeSpeed += 0.1;
426	      dmgMelee += 0.1; dmgRanged += 0.1; dmgMagic += 0.1;
427	      critMelee += 2; critRanged += 2; critMagic += 2;
428	    }
429	    return {
430	      def, mana, hpPerSec: life / 2, // lifeRegen 单位 = 每半秒（NaturalLifeRegen 语义）
431	      dmgMelee, dmgRanged, dmgMagic,   // 箭袋 arrowDmg 移入 arrowStack（仅箭吃，:3820）
432	      critMelee, critRanged, critMagic,
433	      moveMult, meleeSpeed,
434	      extraFall, lavaMax, armorPen, rocketBoots,
435	      autoJump, fireWalk, noKnockback, noFallDmg, desertBoots,
436	      waterWalk, jumpBoost, panic, starCloak,
437	      jumpOpts,
438	      wing, dash, blackBelt, bees, carpet,
439	      jumpSpd: jumpSpd + (this.buffs.has(BuffType.Werewolf) ? 0.2 : 0), flipper, longInvince, spikedBoots,
440	      treasureMagnet, goldRing, luckyCoin, discount,
441	      arrowDmg, ammoSave, kbGlove, yoyoString,
442	    quiver: equipHasQuiver,
443	    moltenQuiver, // 箭袋族：箭速/击退 ×1.1（Player.cs:52711-52715）
444	      arrowStack: arrowDmg, shroomiteType, shroomiteSet, vortexSet, nebulaSet, beetleOff,
445	      beetleDef,
446	      wolfAcc, boc,
447	      tileSpeed, wallSpeed, tileRange, pStone, counterWeight,
448	      manaMagnet, magicCuffs, manaFlower,
449	      manaRegenBonus, manaRegenDelayBonus,
450	      setBonus: sb, manaCostMul,
451	      minionSlots, minionDmg, minionKB, sentrySlots, whipRange,
452	      whipSpd: summonSet?.whipSpd ?? 1,
453	      summonSet,
454	    };
455	  }
456	  get maxHp(): number {
457	    // 生命力药水（Lifeforce :9883）：statLifeMax2 += statLifeMax/5/20*20 → +20%（按 20 取整）
458	    const lf = this.buffs.has(BuffType.Lifeforce) ? Math.floor(this.baseMaxHp / 5 / 20) * 20 : 0;
459	    return this.baseMaxHp + this.buffs.healthBonus + lf;
460	  }
461	  get maxMana(): number {
462	    return this.baseMaxMana + this.equipStats.mana + this.buffs.manaMaxBonus; // 星力手环族等 + 水晶球预见 +20（:11481)
463	  }
464	  /** 随从/鞭伤害乘区（GetWeaponDamageMultiplier summon → minionDamage 链：独立第四链，
465	   *  不再复用 magic——MagicPower 等 magic-only 来源不吃召唤；四系通用来源照常） */
466	  get summonDamageMult(): number {
467	    return this.damageMult('summon');
468	  }
469	  /** 随从上限（Player.cs:9855+ buff + ApplyEquipFunctional 散件/配饰 + 套装层） */
470	  get maxMinions(): number {
471	    return 1 + (this.buffs.has(BuffType.Bewitched) ? 1 : 0)
472	      + (this.buffs.has(BuffType.Summoning) ? 1 : 0)
473	      + this.equipStats.minionSlots;
474	  }
475	  /** 哨兵上限（maxTurrets 链 :9863 War Table buff 未实装暂缺 + 散件/套装） */
476	  get maxSentries(): number {
477	    // War Table buff 348（:9863-9866 maxTurrets++，:2714 默认 1）
478	    return 1 + this.equipStats.sentrySlots + (this.buffs.has(BuffType.WarTable) ? 1 : 0);
479	  }
480	  get thornsActive(): boolean {
481	    return this.buffs.hasThorns;
482	  }
483	  /** 近战攻速倍率（猛爪手套 ×2 + 装备 meleeSpeed 67-80 词缀/狂战士手套累加 + 醉酒近战速 ×1.1） */
484	  get attackSpeedMult(): number {
485	    return (1 + this.equipStats.meleeSpeed) * (this.hasFeralClaws ? 2 : 1)
486	      * (this.buffs.has(BuffType.Tipsy) ? 1.1 : 1)
487	      * (this.buffs.has(BuffType.Werewolf) ? 1.051 : 1)      // 狼人 meleeSpeed += 5.1%（:11489）
488	      * (this.buffs.has(BuffType.Weak) ? 0.949 : 1)          // 虚弱 meleeSpeed -= 5.1%（:11507）
489	      * (1 + 0.1 * this.beetleOrbs)                           // 甲虫攻击球攻速（:10071+）
490	
491	      * (1 + this.buffs.wellFedMeleeSpeed);   // 食物近战速 +5/7.5/10%（:11528+）
492	  }
493	  /** 近战伤害加成（猛爪手套 +5） */
494	  get meleeDamageBonus(): number {
495	    return this.hasFeralClaws ? 5 : 0;
496	  }
497	  /** 全系伤害加成装备聚合（ApplyEquipFunctional dmgX 段；四系分道——summon 是独立
498	   *  minionDamage 链：装备走 SUMMON_GEAR/SET，不含 magic-only 来源） */
499	  damageMult(kind: 'melee' | 'ranged' | 'magic' | 'summon'): number {
500	    const st = this.equipStats;
501	    if (kind === 'summon') {
502	      // minionDamage 链（Player.cs GetWeaponDamageMultiplier summon 分支）：仅四系通用
503	      // 来源（怒气/食物）+ 召唤装备链；MagicPower/Archery 等 class 来源不吃
504	      let m = 1 + st.minionDmg;
505	      if (this.buffs.has(BuffType.Rage)) m += 0.1;
506	      if (this.buffs.has(BuffType.BrainOfConfusionBuff)) m += 0.1; // BOC 321（:9639-9646）
507	      m += this.buffs.wellFedDamage;
508	      m += 0.15 * this.nebula[0];        // 星云伤害 179-181 每级四系 +15%（:10118-10124）
509	      return m;
510	    }
511	    let m = 1 + (kind === 'melee' ? st.dmgMelee : kind === 'ranged' ? st.dmgRanged : st.dmgMagic);
512	    if (kind === 'magic') {
513	      m += this.buffs.magicDmgBonus;            // MagicPower +20%（:9669）
514	      m *= this.buffs.manaSickMagicMult;        // 魔力眩晕最高 -25% 线性恢复（:10003/:25616）
515	    }
516	    if (kind === 'ranged') m *= this.buffs.arrowDmgMult;   // Archery ×1.1（:9712,ranged 近义）
517	    // R1 药水：怒气(117)全系 +10%（:9947）；醉酒(25)近战 +10%（:11513）
518	    if (this.buffs.has(BuffType.Rage)) m += 0.1;
519	    if (kind === 'melee') {
520	      if (this.buffs.has(BuffType.Tipsy)) m += 0.1;
521	      if (this.buffs.has(BuffType.Werewolf)) m += 0.051;      // 狼人（:11488）
522	      if (this.buffs.has(BuffType.Weak)) m -= 0.051;         // 虚弱（:11506）
523	      m += 0.1 * this.beetleOrbs;                              // 甲虫攻击球每颗 +10%（:10071+）
524	      if (this.heldPsychoKnife) m += (1 - this.stealth) * 3;   // 变态刀潜行（:25487）
525	    }
526	    m += this.buffs.wellFedDamage;   // 食物三档全系 +5/7.5/10%（:11527+）
527	    m += 0.15 * this.nebula[0];      // 星云四系 +15%/层
528	    return m;
529	  }
530	  /** 远程分道乘区（Player.cs:3820-3824 bowEffectiveDamage 拆分）：
531	   *  箭 = (rangedDamage + 箭袋stack) × Archery × 蘑菇矿箭头 1.12 × 潜行增伤；
532	   *  弹/火箭 = rangedDamage × 对应蘑菇矿头 1.12 × 潜行；其他（飞镖等）= rangedDamage */
533	  rangedDamageMult(kind: 'arrow' | 'bullet' | 'rocket' | 'other'): number {
534	    const st = this.equipStats;
535	    const base = this.damageMult('ranged'); // rangedDamage 全链（装备+四系 buff）
536	    const stealthBonus = 1 + (1 - this.stealth) * (st.vortexSet ? 0.8 : st.shroomiteSet ? 0.6 : 0);
537	    if (kind === 'arrow') {
538	      // bowEffectiveDamage :3820 = (rangedDamage/arrowMult + stack) × arrowMult²
539	      //   = (rangedDamage + stack×arrowMult) × arrowMult——stack 段平方差异在此
540	      const arrowMult = this.buffs.arrowDmgMult * (st.shroomiteType === 'arrow' ? 1.12 : 1);
541	      return (base + st.arrowStack * arrowMult) * arrowMult * stealthBonus;
542	    }
543	    if (kind === 'bullet') return base * (st.shroomiteType === 'bullet' ? 1.12 : 1) * stealthBonus;
544	    if (kind === 'rocket') return base * (st.shroomiteType === 'rocket' ? 1.12 : 1) * stealthBonus;
545	    return base;
546	  }
547	  /** 手持变态刀 3106（潜行判定用） */
548	  get heldPsychoKnife(): boolean {
549	    const d = ITEM_DEFS[this.inv.heldItem()?.id ?? -1];
550	    const vid = d?.vid ?? (d?.key?.startsWith('vi_') ? parseInt(d.key.slice(3), 10) : -1);
551	    return vid === 3106;
552	  }
553	  /** 潜行 aggro（:25518/:25557/:25491：蘑菇矿 -750×(1-s) / 星璇 -1200 / 变态刀 -750）
554	   *  ——敌人索敌距离缩短（NPC.cs:78375 dist -= aggro）；各 AI 家族索敌门消费见后续批 */
555	  get aggro(): number {
556	    const s1 = 1 - this.stealth;
557	    if (this.equipStats.vortexSet) return -Math.round(1200 * s1);
558	    if (this.equipStats.shroomiteSet) return -Math.round(750 * s1);
559	    if (this.heldPsychoKnife) return -Math.round(750 * s1);
560	    return 0;
561	  }
562	  /** 近战护甲穿透（磨刀 159：meleeArmorPenetration += 12，仅近战/投掷） */
563	  get meleeArmorPen(): number {
564	    return this.buffs.has(BuffType.Sharpened) ? 12 : 0;
565	  }
566	  /** 星云 booster CD（命中驱动，Game 侧判定；:12895 nebulaCD=30） */
567	  nebulaCD = 0;
568	  /** 用魔物品起手（Game 在设定 useTime 后调用）：登记动画窗，窗内每帧重置
569	   *  manaRegenDelay（Player.cs:42131-42137 itemAnimation>0 && item.mana>0 →
570	   *  ItemCheck_ApplyManaRegenDelay :49851；本仓单计时器模型以 useTime 代 useAnimation） */
571	  onManaItemUsed(): void {
572	    this.manaAnimTicks = Math.max(this.manaAnimTicks, this.useTime);
573	  }
574	  /** 甲虫进攻套：近战命中蓄能（45 次/球，满 3 球；受击掉球见 damage()） */
575	  onMeleeHit(): void {
576	    // ⑰ 时间蓄能（原版持续近战 ~90t/球）：命中只刷新续航窗口，蓄能走 fixedUpdate 每 tick
577	    if (this.equipStats.beetleOff || this.equipStats.beetleDef) this.lastMeleeTick = 30;
578	  }
579	  /** 装备暴击率（critX 段 + 词缀 67/68） */
580	  critChance(kind: 'melee' | 'ranged' | 'magic'): number {
581	    const st = this.equipStats;
582	    let c = kind === 'melee' ? st.critMelee : kind === 'ranged' ? st.critRanged : st.critMagic;
583	    // R1 药水：暴怒(115)全系暴击 +10（:9890）；醉酒(25)近战暴击 +2（:11515）
584	    if (this.buffs.has(BuffType.Wrath)) c += 10;
585	    if (this.buffs.has(BuffType.BrainOfConfusionBuff)) c += 10; // BOC（:9639）
586	    if (kind === 'melee' && this.buffs.has(BuffType.Tipsy)) c += 2;
587	    if (kind === 'melee' && this.buffs.has(BuffType.Werewolf)) c += 2; // 狼人（:11493）
588	    if (kind === 'melee' && this.heldPsychoKnife) c = Math.min(100, c + Math.round((1 - this.stealth) * 30)); // 变态刀（:25489）
589	    if (kind === 'ranged') {
590	      if (this.equipStats.shroomiteType) c += 5; // 蘑菇矿头 rangedCrit+5（:13274+）
591	      if (st.shroomiteSet || st.vortexSet) c += Math.round((1 - this.stealth) * (st.vortexSet ? 20 : 10)); // 潜行暴击
592	    }
593	    c += this.buffs.wellFedCrit;    // 食物三档全系暴击 +2/3/4（:11525+）
594	    return c;
595	  }
596	
597	  get frame(): number {
598	    if (!this.onGround) return 4;
599	    if (Math.abs(this.vx) > 0.3) {
600	      return 1 + Math.floor(this.animTime / 8) % 3;
601	    }
602	    return 0;
603	  }
604	
605	  fixedUpdate(dt: number, game: GameHooks) {
606	    const world = game.world;
607	    if (this.iframes > 0) this.iframes--;
608	    if (this.useTime > 0) this.useTime--;
609	
610	    // Buff tick：自然回复 / 环境 DoT（负值=持续伤害,原版 lifeRegen 路径:无视防御与无敌帧）
611	    const buffHeal = this.buffs.tick(dt);
612	    if (buffHeal > 0 && this.hp > 0) this.hp = Math.min(this.maxHp, this.hp + buffHeal);
613	    else if (buffHeal < 0 && this.hp > 0) {
614	      this.hp = Math.max(0, this.hp + buffHeal);
615	      if (this.hp <= 0) this.lastDamageCause = { kind: 'default' }; // DoT 致死=默认死亡包
616	    }
617	    // 恐慌项链加速窗口倒计时
618	    if (this.panicTime > 0) this.panicTime -= dt;
619	    // 装备生命回复（再生手环族 lifeRegen：每半秒 N/2 HP → 每秒 N/2；战斗中也生效）
620	    const equipRegen = this.equipStats.hpPerSec;
621	    if (equipRegen > 0 && this.hp > 0) {
622	      this.regenAccum += equipRegen * dt;
623	      if (this.regenAccum >= 1) {
624	        const n = Math.floor(this.regenAccum);
625	        this.regenAccum -= n;
626	        this.hp = Math.min(this.maxHp, this.hp + n);
627	      }
628	    }
629	    // 自然回血：脱离战斗 5 秒后每秒缓回 1 点（流血 Bleeding 清 lifeRegenTime → 阻断,:18998；
630	    // 遮挡 Obstructed 163 的 bleed 同门——:11424 bleed=true 同消费点）
631	    this.sinceHurt++;
632	    if (this.sinceHurt > 300 && this.hp > 0 && this.hp < this.maxHp
633	      && !this.buffs.has(BuffType.Bleeding) && !this.buffs.obstructed) {
634	      this.regenAccum += dt;
635	      if (this.regenAccum >= 1) {
636	        this.regenAccum -= 1;
637	        this.hp = Math.min(this.maxHp, this.hp + 1);
638	      }
639	    }
640	    // 上限收缩时钳制
641	    if (this.hp > this.maxHp) this.hp = this.maxHp;
642	    // ---- 魔力自然回复 1:1（Player.UpdateManaRegen :19214-19302）----
643	    // maxRegenDelay（:24378-24379）：(1−mana/max)×60×4+45 再 ×0.7——用魔越狠惩罚越长
644	    const smm = this.maxMana;                       // statManaMax2（buff+装备后上限）
645	    if (this.manaAnimTicks > 0) {
646	      // 用魔物品动画期：每帧重置 delay（ItemCheck :42131-42137 → ApplyManaRegenDelay
647	      // :49851-49856；spaceGun+太空枪族 127/4347/4348/514 豁免项本仓无该配饰，恒重置）
648	      this.manaAnimTicks--;
649	      this.manaRegenDelay = Math.floor((1 - this.mana / smm) * 240 + 45) * 0.7;
650	    }
651	    // manaRegenBonus/manaRegenDelayBonus（:18481-18482 每帧清零后由 buff 158 :9629-9632
652	    // 与魔力斗篷 982 :14379-14383 重算）
653	    const mRegenBonus = this.equipStats.manaRegenBonus
654	      + (this.buffs.has(BuffType.StarInBottle) ? 10 : 0);
655	    const mDelayBonus = this.equipStats.manaRegenDelayBonus
656	      + (this.buffs.has(BuffType.StarInBottle) ? 0.5 : 0);
657	    if (this.manaRegenDelay > 0) {
658	      // 惩罚期衰减（:19234-19246）：基础 1 + delayBonus；静止/攀绳/魔力再生再 −1
659	      this.manaRegenDelay -= 1 + mDelayBonus;
660	      const still = Math.abs(this.vx) < 0.05 && Math.abs(this.vy) < 0.05; // IsConsideredStandingStill :3175
661	      if (still || this.onRope || this.buffs.manaRegenBuff) this.manaRegenDelay -= 1;
662	      if (this.usedArcaneCrystal) this.manaRegenDelay -= 0.05;   // :19442-19446
663	    }
664	    if (this.buffs.manaRegenBuff && this.manaRegenDelay > 20) this.manaRegenDelay = 20; // :19247-19250
665	    let manaRegen = 0;
666	    if (this.manaRegenDelay <= 0) {
667	      this.manaRegenDelay = 0;
668	      // 每帧产额（:19251-19268）：max/3+1+bonus；静止/攀绳/魔力再生再 +max/3；
669	      // 奥术水晶 +max/50；存量系数 num2=mana/max×0.8+0.2（魔力再生恒 1）×1.15 取整
670	      const still = Math.abs(this.vx) < 0.05 && Math.abs(this.vy) < 0.05;
671	      manaRegen = Math.floor(smm / 3) + 1 + mRegenBonus;
672	      if (still || this.onRope || this.buffs.manaRegenBuff) manaRegen += Math.floor(smm / 3);
673	      if (this.usedArcaneCrystal) manaRegen += Math.floor(smm / 50);
674	      let num2 = smm > 0 ? (this.mana / smm) * 0.8 + 0.2 : 1;
675	      if (this.buffs.manaRegenBuff) num2 = 1;
676	      manaRegen = Math.floor(manaRegen * num2 * 1.15);
677	    }
678	    // 蓄能结算（:19274-19278）：≥120 扣 120 换 1 魔（满魔时也扣——原版同语义）
679	    this.manaRegenCount += manaRegen;
680	    while (this.manaRegenCount >= 120) {
681	      this.manaRegenCount -= 120;
682	      if (this.mana < smm) this.mana++;
683	    }
684	    if (this.manaRegenCount < 0) this.manaRegenCount = 0;  // :25686-25688
685	    if (this.mana > smm) this.mana = smm;                  // :25690-25693
686	
687	    // 液体检测：身体采样在脚底上方固定 4px（贴脚即入水，不随身高缩放）
688	    const liq = world.store.liquid[world.store.idx(
689	      Math.floor(this.cx / TILE), Math.floor((this.y + this.h - 4) / TILE),
690	    )];
691	    const wasInWater = this.inWater;
692	    // wet 判定排除微光（Collision.cs:1418 WetCollision 只认 !lava && !shimmer）
693	    this.inWater = liq > 100 && world.store.liquidType[
694	      world.store.idx(Math.floor(this.cx / TILE), Math.floor((this.y + this.h - 4) / TILE))] !== 4;
695	    // 入水瞬间：水花声（出水不响）
696	    if (this.inWater && !wasInWater) game.playSfx('splash');
697	    const centerIdx = world.store.idx(Math.floor(this.cx / TILE), Math.floor((this.y + this.h - 4) / TILE));
698	    // waterWalk 时缩高 6px 判定(原版 num80,Player.cs:27349/27352:水面行走不因脚尖触浆受伤)
699	    // 水上行走（装备 waterWalk 族 ∪ 水上行走药水 buff 15,:9706）
700	    const canWaterWalk = this.equipStats.waterWalk || this.buffs.canWaterWalk;
701	    const lavaProbeH = canWaterWalk ? this.h - 6 : this.h;
702	    this.inLava = liquidCollision(world.store, this.x, this.y, this.w, lavaProbeH, 2); // LavaCollision 盒判定
703	    // 蜂蜜浸入（Player.cs:27436）：湿判定命中蜂蜜 → AddBuff(48, 1800t=30s) + honeyWet。
704	    // BuffState.apply 是 max 合并（AddBuff 语义），浸着恒 30s，离开后自然倒计时
705	    this.inHoney = world.store.liquidType[centerIdx] === 3 && liq > 30;
706	    if (this.inHoney) this.buffs.apply(BuffType.Honey, 30);
707	    // 微光浸入（Player.cs:27420-27434）：盒命中微光 → shimmerWet；本地玩家非免疫且
708	    // 脚格是微光且在地狱层之上 → AddBuff(353, 60)（每 tick 刷新 = 浸着恒微光化）。
709	    // shimmerImmune（:14981 原版旗标来源未移植）恒 false；地狱层内微光不生效
710	    // （:11391-11397 position.Y/16 > UnderworldLayer → DelBuff）
711	    this.inShimmer = world.store.liquidType[centerIdx] === 4 && liq > 30;
712	    this.shimmering = this.inShimmer && this.y / TILE < world.lavaLine;
713	    // buff 353 登记（每 tick 刷新 1s = 浸着恒显示；离开后 ≤1s 消失）——左上角图标依赖
714	    if (this.shimmering) this.buffs.apply(BuffType.Shimmered, 1);
715	    // TryToShimmerUnstuck（:28377-28389）：timeShimmering 钳 0-7200（shimmering +1/
716	    // 否则 -10）；≥3600 或 ≥1200 且有任意输入 → ShimmerUnstuck 传送脱困
717	    this.timeShimmering = Math.max(0, Math.min(7200,
718	      this.timeShimmering + (this.shimmering ? 1 : -10)));
719	    if (this.shimmering || this.timeShimmering > 0) {
720	      const anyInput = this.inputX !== 0 || this.inputJump || this.inputUp || this.inputDown;
721	      if (this.timeShimmering >= 3600 || (this.timeShimmering >= 1200 && anyInput)) {
722	        this.shimmerUnstuck(game, world);
723	      }
724	    }
725	    const headIdx = world.store.idx(Math.floor(this.cx / TILE), Math.floor((this.y + 8) / TILE), // 鼻子位置（头顶下方半格）
726	    );
727	    const headLiq = world.store.liquid[headIdx];
728	    const prevHeadUnderwater = this.headUnderwater; // 旧值（判定"刚出水"必须用更新前状态）
729	    // 气口消耗只对水（原版 DrownCollision 不含水蜜/岩浆——蜂蜜和岩浆不会淹死）
730	    this.headUnderwater = headLiq > 40 && world.store.liquidType[headIdx] === 1;
731	    // 岩浆伤害 1:1（Player.cs:27350-27440）：盒判定接触 → lavaTime 宽限（护身符族）耗尽后
732	    // 单发 80（Hurt 全结算：防御+无敌帧）+ 着火 OnFire 7s（AddBuff(24,420)）；
733	    // 无敌帧承担原版 hurtCooldowns[Lava] 冷却
734	    if (this.inLava && !this.buffs.obsidianSkin) {
735	      // 黑曜石皮 buff:lavaImmune 完全豁免（Player.cs:9573）,不伤不火
736	      const lavaMax = this.equipStats.lavaMax;
737	      if (lavaMax > 0 && this.lavaImmuneTicks > 0) {
738	        this.lavaImmuneTicks--;
739	      } else if (this.iframes <= 0) {
740	        this.lastDamageCause = { kind: 'lava' };
741	        if (this.damage(80, this.cx, this.y - 10, false)) {
742	          this.buffs.apply(BuffType.OnFire, 7);
743	          game.playSfx('hurt');
744	          game.addDamageNumber(this.cx, this.y, Math.max(1, Math.round(80 - this.defense * 0.5)), false, '#FF6020');
745	          game.spawnParticles(this.cx, this.y + this.h / 2, '#FF9A3C', 12, 1.6, { life: 32, grav: -0.05 });
746	        }
747	      }
748	    } else if (!this.inLava) {
749	      this.lavaAccum = 0;
750	      // 离浆宽限逐步恢复(Player.cs:27405:lavaTime < lavaMax 时每 tick +1,
751	      // 非立即回满——护身符 7s 宽限需要等价时间回充)
752	      const lavaMax = this.equipStats.lavaMax;
753	      if (lavaMax > 0 && this.lavaImmuneTicks < lavaMax) this.lavaImmuneTicks++;
754	    }
755	    // 入水熄灭着火（Player.cs:27426：wet 且非岩浆 → DelBuff 24）
756	    if (this.inWater && !this.inLava) this.buffs.remove(BuffType.OnFire);
757	    // 着火/燃烧粒子（dust6 火尘族,每 tick 0.8 概率一枚上浮）
758	    if (this.buffs.has(BuffType.OnFire) || this.buffs.has(BuffType.Burning)) {
759	      if (Math.random() < 0.8) {
760	        game.spawnParticles(
761	          this.x + Math.random() * this.w, this.y + Math.random() * this.h,
762	          Math.random() < 0.7 ? '#FF9A3C' : '#FFD24A', 1, 0.7,
763	          { life: 26 + Math.random() * 14, grav: -0.06, damp: 0.96 });
764	      }
765	    }
766	    // HurtTiles 接触伤害（Collision.cs:3128 + Player.cs:27296/28507）:
767	    // 尖刺/木尖刺/荆棘族直接伤害 + 流血,陨石/狱石族 Burning,沙族窒息,荆棘族触碰毁块
768	    const ht = hurtTiles(world.store, this.x, this.y, this.w, this.h,
769	      this.equipStats.fireWalk || this.buffs.obsidianSkin); // 黑曜石皮含 fireWalk（:9576）
770	    if (ht) this.applyTouchDamage(game, ht);
771	
772	    // 气口：头部浸水时 23.33 秒耗尽，耗尽后每秒掉 10 血；出水立即恢复；
773	    // 鱼鳃 buff（gills,:9656）水下呼吸不耗
774	    const wasHead = prevHeadUnderwater;
775	    if (this.headUnderwater && !this.buffs.gills) {
776	      this.breathAccum += dt;
777	      const per = Player.BREATH_SECONDS / Player.BREATH_BUBBLES;
778	      while (this.breathAccum >= per && this.breath > 0) {
779	        this.breathAccum -= per;
780	        this.breath--;
781	      }
782	      if (this.breath <= 0) {
783	        this.drownAccum += dt;
784	        if (this.drownAccum >= 1) {
785	          this.drownAccum -= 1;
786	          this.lastDamageCause = { kind: 'drowned' };
787	          this.damage(10, this.cx, this.y - 10, false); // 窒息环境伤害：只掉血，无击退
788	          game.playSfx('drown');
789	          game.addDamageNumber(this.cx, this.y, 10, false, '#FF5050'); // 与受击同色
790	        }
791	      }
792	    } else if (wasHead || this.breath < Player.BREATH_BUBBLES) {
793	      // 出水补气。关键：刚出水时 breath 可能仍为满值但有一颗正在渐隐消耗中
794	      // （breathAccum > 0）——只判 breath==5 会跳过补气导致气泡瞬间消失。
795	      // 余量取「整口气 + 正在消耗那颗的剩余比例」的精确小数，从该状态回满
796	      const per = Player.BREATH_SECONDS / Player.BREATH_BUBBLES;
797	      const drainRemain = wasHead ? Math.max(0, Math.min(1, 1 - this.breathAccum / per)) : 1;
798	      this.refillFrom = Math.min(Player.BREATH_BUBBLES, this.breath - 1 + drainRemain);
799	      const missing = 1 - this.refillFrom / Player.BREATH_BUBBLES;
800	      this.breath = Player.BREATH_BUBBLES;
801	      this.breathAccum = 0;
802	      this.drownAccum = 0;
803	      // 补气时长：缺口比例（1.11s × 缺口），保底 0.55s 能看清；满后停留 0.35s 再隐藏
804	      this.refillDur = Math.max(0.55, 1.11 * missing);
805	      this.refillT = 0;
806	    }
807	    // 补气动画推进（补满后停留 REFILL_HOLD 再隐藏）
808	    if (this.refillT >= 0) {
809	      this.refillT += dt;
810	      if (this.refillT >= this.refillDur + 0.15) this.refillT = -1;
811	    }
812	
813	    // 死亡等待重生（任何死法统一在此发声——溺水/岩浆/摔落/受击都经过这里）
814	    if (this.hp <= 0) {
815	      if (!this.dead) game.playSfx('pkilled');
816	      this.dead = true;
817	      return;
818	    }
819	
820	    // 水平（敏捷 Buff 提速 + 装备移速（赫尔墨斯靴族 runSpeed/词缀 73-76）；蜂蜜比水更黏滞）
821	    const eqEarly = this.equipStats;
822	    // 沙丘行者靴地板旗标（FloorVisuals :23434-23471 + GetFloorTile :23481-23509）：
823	    // vy==0 时取脚下一行的 x/x−1/x+1 首个 active+solid 格，属沙族地格即 runningOnSand
824	    // （TileID.Sets.Conversion Sand{53,112,116,234}/HardenedSand{397-399,402}/
825	    // Sandstone{396,400,401,403}，TileID.cs:30-34）。原版只在 vy==0 时刷新、离地不清零
826	    // （ResetFloorFlags 仅重生/传送调用）——空中保留加成，同语义
827	    if (this.vy === 0 && !this.ridingCart) {
828	      const st0 = world.store;
829	      const fx0 = Math.floor(this.cx / TILE), fy0 = Math.floor((this.y + this.h) / TILE);
830	      let ft = -1;
831	      for (const d of [0, -1, 1]) {
832	        const xx = fx0 + d;
833	        if (!st0.inBounds(xx, fy0)) continue;
834	        const ii = st0.idx(xx, fy0);
835	        if (st0.flags[ii] && st0.isSolid(xx, fy0)) { ft = st0.type[ii]; break; }
836	      }
837	      this.runningOnSand = ft >= 0 && SAND_FLOOR_IDS.has(ft);
838	    }
839	    // 沙丘行者靴 1:1（Player.cs:26225-26231）：runningOnSand && desertBoots →
840	    // maxRunSpeed/accRunSpeed/runAcceleration/runSlowdown 全部 ×1.75（原版是乘区，
841	    // 非 ZoneDesert 门——曾按 zoneDesert+0.25 定值近似）。speedMult 同时乘加速与
842	    // 限速 = 前三者的复合；runSlowdown ×1.75 以摩擦指数 1.75 等价（乘法摩擦下
843	    // 每帧减量 ∝ 1−f^n）
844	    const duneBoost = eqEarly.desertBoots && this.runningOnSand;
845	    const speedMult = this.buffs.moveSpeedMult * this.equipStats.moveMult * (this.inHoney ? 0.5 : 1)
846	      * (this.vortexStealthActive && this.stealth > 0 ? 0.3 : 1)   // 星璇潜行移速（:25563）
847	      * (duneBoost ? 1.75 : 1);
848	    // 冰冻 Frozen(47,Player.cs:9749 frozen=true)：整帧封移动输入——跳跃/攀绳/矿车
849	    // 同读这些标志,一并归零(原版 Update 段 control* 清零语义)。帧末由 Game 重灌输入
850	    if (this.buffs.has(BuffType.Frozen)) { this.inputX = 0; this.inputJump = false; this.inputUp = false; this.inputDown = false; }
851	    // 矿车骑乘（mount.Cart 语义）：移动/跳跃/重力/碰撞全部由 Minecart 实体接管
852	    //（原版 Player.Update :27783-27850 的 TrackCollision 段替代常规移动链）。
853	    // 上面的 buff/液体/受伤逻辑照常 tick；位置每 tick 由矿车回写。
854	    if (this.ridingCart) {
855	      this.vx = 0; this.vy = 0;
856	      this.onGround = true;
857	      this.fallStartY = null;
858	      return;
859	    }
860	    const ix = this.inputX;
861	    // 冲刺滑行期（dashDelay<0）常规加速/摩擦/限速整体跳过——Run 各分支 dashDelay>=0 门
862	    // （Player.cs:19559/:19575/:19675/:19705），速度由 DashMovement 阻尼段独占
863	    if (this.dashDelay >= 0) {
864	      let accel = PLAYER_WALK_ACCEL;
865	      if (!this.onGround && this.equipStats.wing && this.vy !== 0) {
866	        const ws = wingStatOf(this.equipStats.wing.logic);
867	        const hoverDownMove = this.inputDown && this.inputJump && ws.hover && this.wingTime > 0;
868	        accel *= hoverDownMove && ws.hover ? ws.hoverAccelMult : ws.accelMult;
869	      }
870	      if (ix !== 0) {
871	        this.vx += ix * accel * (this.inWater ? 0.6 : 1) * speedMult;
872	        this.facing = ix;
873	      } else {
874	        this.vx *= this.onGround ? PLAYER_FRICTION ** (duneBoost ? 1.75 : 1) : PLAYER_AIR_FRICTION;
875	        if (Math.abs(this.vx) < 0.05) this.vx = 0;
876	      }
877	      let maxSpd = PLAYER_WALK_MAX * (this.inWater ? 0.55 : 1) * speedMult;
878	      // 翅膀空中横移上限覆盖（WingAirLogicTweaks cs:28843-48：AccRunSpeedOverride；
879	      // hover 下落态改用 DownHoverSpeedOverride 档）
880	      if (!this.onGround && this.equipStats.wing && this.vy !== 0) {
881	        const ws = wingStatOf(this.equipStats.wing.logic);
882	        const hoverDownMove = this.inputDown && this.inputJump && ws.hover && this.wingTime > 0;
883	        const spd = hoverDownMove && ws.hoverSpeed > 0 ? ws.hoverSpeed : ws.accSpeed;
884	        if (spd > maxSpd) maxSpd = spd;
885	      }
886	      this.vx = Math.max(-maxSpd, Math.min(maxSpd, this.vx));
887	    } else if (ix !== 0) {
888	      this.facing = ix; // 滑行中朝向仍随输入（ChangeDir 独立于 Run）
889	    }
890	
891	    // 绳索攀爬(原版:身体中心格为绳(213/353/950-9)时无重力,上/下键攀爬,左右离绳)
892	    const st = world.store;
893	    const ropeTx = Math.floor((this.x + this.w / 2) / TILE);
894	    const ropeTy = Math.floor((this.y + this.h / 2) / TILE);
895	    const ropeHere = !!(st.inBounds(ropeTx, ropeTy) && st.flags[st.idx(ropeTx, ropeTy)]
896	      && TILE_DEFS[st.type[st.idx(ropeTx, ropeTy)]]?.rope);
897	    this.onRope = ropeHere;
898	    if (ropeHere && !this.inWater) {
899	      // 原版攀爬(Player.cs:17169-17212):上爬 vy>0 先阻尼×0.7,-3 以上每 tick -0.2
900	      // (之下 -0.02,下限 -8);下滑镜像(+0.2/+0.1,上限 maxFallSpeed);静止 vy*=0.7
901	      if (this.inputJump) {
902	        if (this.vy > 0) this.vy *= 0.7;
903	        this.vy -= this.vy > -3 ? 0.2 : 0.02;
904	        if (this.vy < -8) this.vy = -8;
905	      } else if (this.inputDown) {
906	        if (this.vy < 0) this.vy *= 0.7;
907	        this.vy += this.vy < 3 ? 0.2 : 0.1;
908	        if (this.vy > MAX_FALL_SPEED) this.vy = MAX_FALL_SPEED;
909	      } else {
910	        this.vy *= 0.7;
911	      }
912	      this.fallStartY = null; // 绳上不计摔伤
913	    } else
914	    // 微光物理（Player.cs:24115-24127 else if (shimmerWet || shimmering) 分支）
915	    if (this.inShimmer && !this.shimmering) {
916	      // 非微光化态浸微光：gravity 0.15（水 0.3 的一半）+ jumpHeight 23/jumpSpeed 5.51
917	      // （:24219-24223）——更轻、可大跳离池；微光不计摔伤
918	      if (this.inputJump) this.vy = Math.max(this.vy - 0.62, -5.5);
919	      this.vy += GRAVITY * 0.15;
920	      this.vy = Math.max(-5.5, Math.min(3.0, this.vy));
921	      this.fallStartY = null;
922	    } else if (this.shimmering) {
923	      // buff 353（:11381-11388）：frozen 封输入 + fallStart 重置（免摔伤）；
924	      // 物理 :24117-24119 gravity/maxFall ×0.9（近似正常慢沉，原地等脱困传送）
925	      this.inputX = 0; this.inputJump = false; this.inputUp = false; this.inputDown = false;
926	      this.vy = Math.min(this.vy + GRAVITY * 0.7 * 0.9, MAX_FALL_SPEED * 0.9);
927	      this.fallStartY = null;
928	    } else
929	    // 跳跃 / 游泳
930	    if (this.inWater) {
931	      // ---- 水面行走（WaterWalkingBoots/LavaWaders 族，Player.WaterWalk 语义近似）----
932	      // 装备后落向液面时站在液面（vy 清零、可正常行走/起跳/重置空中能力）；
933	      // 按 ↓ 下潜。waterWalk2（水上漂靴）同效。
934	      if (canWaterWalk && !this.headUnderwater && this.vy >= 0 && !this.inputDown) {
935	        this.onWaterSurface = true;
936	        this.vy = 0;
937	        this.fallStartY = null;
938	        // 站在液面等价落地：重置多段跳/飞行/飞毯，允许起跳离水面
939	        this.extraJumps = [...this.equipStats.jumpOpts];
940	        const eqW = this.equipStats;
941	        this.wingTime = eqW.wing ? eqW.wing.time : 0;
942	        this.rocketTime = 7; this.rocketRelease = true; this.rocketDelay = 0;
943	        this.canCarpet = true;
944	        this.carpetTime = 300;
945	        if (this.inputJump && this.surfaceJumpCd <= 0) {
946	          this.vy = -PLAYER_JUMP_SPEED;
947	          this.jumpHold = PLAYER_JUMP_TICKS;
948	          this.surfaceJumpCd = 24;
949	        }
950	        if (this.surfaceJumpCd > 0) this.surfaceJumpCd--;
951	      } else {
952	        this.onWaterSurface = false;
953	        // 头部露出水面（踩水状态）→ 允许正常力度起跳跃上岸块（带冷却防连跳）
954	        if (this.inputJump && !this.headUnderwater) {
955	          if (this.surfaceJumpCd <= 0) {
956	            this.vy = -PLAYER_JUMP_SPEED;
957	            this.jumpHold = PLAYER_JUMP_TICKS;
958	            this.surfaceJumpCd = 24;
959	          }
960	      } else if (this.inputJump) {
961	        // 全浸没：游泳上浮（脚蹼族 accFlipper：提速 1.5×）
962	        const swimMult = (this.equipStats.flipper || this.buffs.has(BuffType.FlipperPotion)) ? 1.5 : 1;
963	        this.vy = Math.max(this.vy - 0.62 * swimMult, -4.4 * swimMult);
964	      }
965	      if (this.surfaceJumpCd > 0) this.surfaceJumpCd--;
966	      this.vy += GRAVITY * 0.3;
967	      this.vy = Math.max(-4.6, Math.min(3.0, this.vy));
968	      this.fallStartY = null;
969	      }
970	    } else {
971	      const gd = this.gravDir;
972	      if (this.inputJump && this.onGround) {
973	        // 跳跃速度 = 基础 + jumpSpeedBoost（蛙腿族 +1.6，Player.jumpSpeedBoost :22427）；
974	        // 重力倒置时方向取反（gravDir，Player.cs:3207 全部 vy 乘 gravDir 语义）
975	        this.vy = -(PLAYER_JUMP_SPEED + this.equipStats.jumpSpd) * gd;
976	        this.jumpHold = PLAYER_JUMP_TICKS;
977	      }
978	      if (this.inputJump && this.jumpHold > 0) {
979	        this.vy -= 0.22;
980	        this.jumpHold--;
981	      } else {
982	        this.jumpHold = 0;
983	      }
984	      // ---- 多段跳（RefreshDoubleJumps + JumpMovement 近似）：云朵/沙暴/暴雪/屁瓶族 ----
985	      // 空中再按跳（持续按住 + 段数剩余 + 未在急升中）→ 消费一段；各段速度原版梯度近似
986	      const eq = this.equipStats;
987	      if (this.onGround) this.extraJumps = [...eq.jumpOpts]; // 落地重置段数
988	      if (!this.onGround && this.inputJump && this.extraJumps.length > 0 && this.vy > -2 && this.extraJumpCd <= 0) {
989	        const opt = this.extraJumps.shift()!;
990	        const mult = opt === 'Fart' ? 1.28 : (opt === 'Sandstorm' || opt === 'Blizzard') ? 1.18 : 1.0;
991	        this.vy = -PLAYER_JUMP_SPEED * mult * (eq.jumpBoost ? 1.25 : 1);
992	        this.jumpHold = PLAYER_JUMP_TICKS;
993	        this.extraJumpCd = 8; // 防同帧连段
994	      }
995	      if (this.extraJumpCd > 0) this.extraJumpCd--;
996	      // ---- 翅膀/火箭靴/飞毯 1:1（Player.Update :26388-27092 + WingMovement :21746 +
997	      //      CarpetMovement :21568 + RocketBoots :26548-26628）----
998	      const wings = eq.wing ? eq.wing.logic : 0;   // wingsLogic = armor.wingSlot（:12584）
999	      const hoverDown = this.inputDown;            // TryingToHoverDown（保持态近似省略）
1000	      const JS = PLAYER_JUMP_SPEED;                // jumpSpeed 基准（原版 5.301 系按本地尺度）
1001	      // 落地重置（原版 :26169 地面块 + :26490 vy==0&&releaseJump 语义并入）
1002	      // 松跳重触发（原版 :20765 松跳段独立于地面状态——rocketRelease/wingRelease）
1003	      if (!this.inputJump) { this.rocketRelease = true; this.wingRelease = true; }
1004	      if (this.onGround) {
1005	        this.wingTime = eq.wing ? eq.wing.time : 0;   // :26169 = wingTimeMax（FlyTime）
1006	        this.rocketTime = eq.rocketBoots > 0 ? 7 : 0;  // :2612 + :26436（无靴恒 0）
1007	        this.rocketDelay = 0;
1008	        this.canRocket = false;
1009	        this.rocketRelease = false;
1010	        this.canCarpet = true;        // :26173
1011	        this.carpetTime = 300;
1012	      } else {
1013	        // canRocket 门（:26487）：vy > -jumpSpeed 且 vy≠0
1014	        if (this.vy > -JS && this.vy !== 0) this.canRocket = true;
1015	        // vy==0 恢复 rocketTime（:26540：velocity.Y==0 即回满，含撞顶悬停等非落地场景）
1016	        if (this.vy === 0) this.rocketTime = eq.rocketBoots > 0 ? 7 : 0;
1017	        // flag19 = 翅膀飞行中（:26500-26510：wings>0 && controlJump && wingTime>0 &&
1018	        //   jump==0 && vy≠0；hover 族 + ↓+跳 也算 :26505）
1019	        const flying =
1020	          (wings > 0 && this.inputJump && this.wingTime > 0 && this.jumpHold === 0 && this.vy !== 0)
1021	          || (eq.wing !== null && eq.wing.hover && this.inputJump && hoverDown && this.wingTime > 0);
1022	        if (flying) {
1023	          this.wingMovement(wings, hoverDown, JS);
1024	          // WingFrame 通用 flap（:29425+ 各族主干）：6t/帧循环 1→2→3→2
1025	          this.wingFrameCounter++;
1026	          const beat = 6;
1027	          const phase = Math.floor(this.wingFrameCounter / beat) % 4;
1028	          this.wingFrame = [1, 2, 3, 2][phase];
1029	        } else if (this.vy !== 0 && this.inputJump) {
1030	          this.wingFrame = 2;      // 滑翔固定帧（各族主干 else-if 段）
1031	          this.wingFrameCounter = 0;
1032	        } else if (this.vy !== 0) {
1033	          this.wingFrame = 2;      // 空中下落张翼
1034	        } else {
1035	          this.wingFrame = 0;      // 地面收起
1036	          this.wingFrameCounter = 0;
1037	        }
1038	        // 翅膀+火箭靴动态合并（:26523-26531）：空中且 rocketTime 有余 →
1039	        // 剩余脉冲×6 并入 wingTime（上限 = wingTimeMax + 本次转换量），rocketTime 清零
1040	        if (wings > 0 && eq.rocketBoots > 0 && this.vy !== 0 && this.rocketTime > 0) {
1041	          const add = this.rocketTime * 6;
1042	          this.wingTime += add;
1043	          const cap = (eq.wing ? eq.wing.time : 0) + add;
1044	          if (this.wingTime > cap) this.wingTime = cap;
1045	          this.rocketTime = 0;
1046	        }
1047	        // ---- 火箭靴（:26548-26628）：翅膀不可用（无翅或时间尽）才接管 ----
1048	        if (!flying && (this.wingTime <= 0 || wings === 0) && eq.rocketBoots > 0
1049	          && this.inputJump && this.rocketDelay === 0 && this.canRocket && this.rocketRelease) {
1050	          if (this.rocketTime > 0) {
1051	            this.rocketTime--;
1052	            this.rocketDelay = 10;    // 推力脉冲段（:26556）
1053	            if (this.rocketDelay2 <= 0) this.rocketDelay2 = eq.rocketBoots === 1 ? 30 : 15;
1054	          } else {
1055	            this.canRocket = false;
1056	          }
1057	        }
1058	        if (this.rocketDelay2 > 0) this.rocketDelay2--;
1059	        if (this.rocketDelay > 0) {
1060	          // 推力脉冲速度模型（:26602-26626，与翅膀同构 0.1/0.5/1.5 档）：
1061	          this.rocketDelay--;
1062	          this.vy -= 0.1;
1063	          if (this.vy > 0) this.vy -= 0.5;
1064	          else if (this.vy > -JS * 0.5) this.vy -= 0.1;
1065	          if (this.vy < -JS * 1.5) this.vy = -JS * 1.5;
1066	          this.fallStartY = null;
1067	        } else if (!flying) {
1068	          // ---- 飞毯（CarpetMovement :21568-21602）：条件=无多段跳余量/jumpHold 空/
1069	          //      vy≠0/火箭靴未在用/翅膀时间尽；效果=vy 钳到 -(gravity+ε) 抵消重力 ----
1070	          if (eq.carpet && this.extraJumps.length === 0 && this.jumpHold === 0
1071	            && this.vy !== 0 && this.rocketTime === 0 && this.wingTime <= 0) {
1072	            if (this.inputJump && this.canCarpet) { this.canCarpet = false; this.carpetTime = 300; }
1073	            if (this.carpetTime > 0 && this.inputJump) {
1074	              this.carpetTime--;
1075	              this.fallStartY = null;
1076	              this.vy = -(GRAVITY + 1e-6);   // :21588 微升抵消随后重力 → 净缓降
1077	            }
1078	          }
1079	        }
1080	        // 悬浮缓降（:27083-27102）：hover 族 + ↓+跳 + wingTime>0 → vy×0.9（45=0.8）
1081	        if (eq.wing?.hover && hoverDown && this.inputJump && this.wingTime > 0) {
1082	          this.vy *= wings === 45 ? 0.8 : 0.9;
1083	          if (this.vy > -2 && this.vy < 1) this.vy = 1e-5;
1084	        }
1085	      }
1086	      // ---- 冲刺 1:1（DashMovement :20769-21265 + DoCommonDashHandle :21267-21323）----
1087	      // 1=忍者足具/水晶刺客（纯位移） 2=克苏鲁护盾（冲撞 30+反弹）。
1088	      // dashDelay 三态（:20775-20782）：0=就绪 / -1=滑行中（阻尼衰减） / >0=冷却倒计时；
1089	      // 触发帧单次置速（:21131 dash1=16.9 / :21162 dash2=14.5，原版 px 值），此后靠
1090	      // 滑行阻尼自然衰减——无恒速段（旧 dashTicks=15×12.5 近似已废）；重力照常作用
1091	      if (this.dashDelay > 0) {
1092	        // 冷却段（:20958-20968）：eocDash 同步倒数，归零清冲撞命中标记
1093	        if (this.eocDash > 0) this.eocDash--;
1094	        if (this.eocDash === 0) this.eocHitId = -1;
1095	        this.dashDelay--;
1096	      }
1097	      // 克苏鲁护盾冲撞（:20784-20846）：eocDash>0 且未命中时逐帧扫敌。命中判定盒 =
1098	      // 位置 + 速度×0.5 外扩 4px（:20786）；伤害 30×meleeDamage 可暴击、击退 9
1099	      // （kbGlove ×2 / 泰坦 kbBuff ×1.5，:20800-20808）；命中 → eocDash=10、30t 冷却、
1100	      // 反弹 vx=-dir×9 vy=-4（:20825-20840）
1101	      if (eq.dash === 2 && this.eocDash > 0 && this.eocHitId < 0) {
1102	        const bhx = this.x + this.vx * 0.5 - 4, bhy = this.y + this.vy * 0.5 - 4;
1103	        const bhw = this.w + 8, bhh = this.h + 8;
1104	        for (const e of game.enemies()) {
1105	          const en = e as { id?: number; x?: number; y?: number; w?: number; h?: number; cx?: number; cy?: number;
1106	            dead?: boolean; hurt?: (d: number, kx: number, ky: number, g: unknown) => boolean };
1107	          if (en.dead || !en.hurt || en.cx === undefined || en.cy === undefined) continue;
1108	          const ex = en.x ?? en.cx - 8, ey = en.y ?? en.cy - 8, ew = en.w ?? 16, eh = en.h ?? 16;
1109	          if (!(bhx < ex + ew && bhx + bhw > ex && bhy < ey + eh && bhy + bhh > ey)) continue;
1110	          const dir = this.vx < 0 ? -1 : this.vx > 0 ? 1 : this.facing; // :20809-20815
1111	          const crit = Math.random() * 100 < this.critChance('melee');  // :20811-20813
1112	          const dmg = Math.max(1, Math.round(30 * this.damageMult('melee')) * (crit ? 2 : 1));
1113	          const kb = 9 * (eq.kbGlove ? 2 : 1) * (this.buffs.has(BuffType.Titan) ? 1.5 : 1);
1114	          en.hurt(dmg, dir * kb, -4, game);
1115	          game.addDamageNumber(en.cx, en.cy, dmg, crit, crit ? '#FF8040' : '#FFD080');
1116	          this.eocDash = 10;            // :20833
1117	          this.eocHitId = en.id ?? -2;  // :20840（后续帧不再对同一敌结算）
1118	          this.dashDelay = 30;          // :20834 反弹并结束滑行
1119	          this.vx = -dir * 9;
1120	          this.vy = -4;
1121	          break;
1122	        }
1123	      }
1124	      if (this.inputX !== 0 && this.prevInputX === 0) {
1125	        // 双击触发（DoCommonDashHandle :21296-21320 release 语义）：就绪 + 同向二连击
1126	        const dir = this.inputX;
1127	        if (eq.dash > 0 && this.dashDelay === 0 && (dir > 0 ? this.dashT > 0 : this.dashT < 0)) {
1128	          this.dashT = 0;               // :21305 触发即清双击窗
1129	          this.dashDir = dir;
1130	          this.dashDelay = -1;          // :21138 进入滑行态
1131	          this.vx = (eq.dash === 2 ? 14.5 : 16.9) * dir;   // :21162 / :21131 单帧置速
1132	          // 头部将撞墙减半（:21132-21137）：身前半宽+2px 的头部点/身体中点格
1133	          // SolidOrSlopedTile → velocity.X /= 2
1134	          const wtx = Math.floor((this.cx + dir * (this.w / 2) + 2 * dir) / TILE);
1135	          const hty = Math.floor((this.cy + this.gravDir * (-this.h / 2) + 2 * this.gravDir) / TILE);
1136	          const solidOrSloped = (tx: number, ty: number): boolean =>
1137	            st.inBounds(tx, ty) && !!st.flags[st.idx(tx, ty)] && st.isSolid(tx, ty);
1138	          if (solidOrSloped(wtx, hty) || solidOrSloped(wtx, Math.floor(this.cy / TILE))) this.vx /= 2;
1139	          if (eq.dash === 2) { this.eocDash = 15; this.eocHitId = -1; } // :21170
1140	        } else {
1141	          this.dashT = dir * 15;        // :21316-21321 首击登记双击窗（dashTime ±15）
1142	        }
1143	      }
1144	      if (this.dashT > 0) this.dashT--; // :21268-21271 每帧向 0 收敛
1145	      else if (this.dashT < 0) this.dashT++;
1146	      // ---- 攀壁钉鞋（spikedBoots：攀爬爪/鞋钉/忍者大师装备——贴墙缓降+蹬墙跳）----
1147	      this.wallCling = false;
1148	      if (!this.onGround && eq.spikedBoots && this.hitWall && this.inputX !== 0 && this.vy > 0) {
1149	        this.vy = Math.min(this.vy, 1.5); // 贴墙缓降
1150	        this.fallStartY = null;
1151	        this.wallCling = true;
1152	        if (this.inputJump) { // 蹬墙跳
1153	          this.vy = -PLAYER_JUMP_SPEED;
1154	          this.jumpHold = PLAYER_JUMP_TICKS;
1155	          this.vx = -Math.sign(this.vx || this.facing) * 3;
1156	        }
1157	      }
1158	      if (this.dashDelay < 0) {
1159	        // 滑行阻尼（:20970-21113）：|vx|>12 → ×0.985；否则 |vx|>max(accRunSpeed,
1160	        // maxRunSpeed) → ×0.94；跌破档位即结束滑行（dashDelay=20）并把 vx 钳回
1161	        // ±maxRunSpeed（:21108-21113）。num13 = max(accRunSpeed,maxRunSpeed)
1162	        // （accRunSpeed=靴 6/裸 3，maxRunSpeed=3×moveSpeed）
1163	        const num13 = Math.max(eq.accRunSpeed > 0 ? eq.accRunSpeed : 3, 3 * eq.moveMult);
1164	        this.vortexStealthActive = false;  // :21106 滑行中强制显形
1165	        if (Math.abs(this.vx) > 12) {
1166	          this.vx *= 0.985;
1167	        } else if (Math.abs(this.vx) > num13) {
1168	          this.vx *= 0.94;
1169	        } else {
1170	          this.dashDelay = 20;             // :21110（dash1/2 档 num15=20）
1171	          this.vx = this.vx < 0 ? -num13 : num13;
1172	        }
1173	      }
1174	      // 翅膀滑翔（:27015-27027）：wingTime 尽后按住跳 = 重力/3 + 终端 maxFallSpeed/3
1175	      // （!hoverDown）——原版此段在 else-if 链替换常规重力，此处以等价条件并入
1176	      const gliding = !!eq.wing && this.wingTime <= 0 && this.inputJump && this.vy > 0 && !hoverDown;
1177	      // 羽落 buff（slowFall,:21369）：重力 /3,fallStart 每帧重置 → 免坠伤
1178	      let grav = this.buffs.slowFall ? GRAVITY / 3 : GRAVITY;
1179	      if (gliding) {
1180	        grav = GRAVITY / 3;
1181	        if (this.vy > MAX_FALL_SPEED / 3) this.vy = MAX_FALL_SPEED / 3;
1182	      }
1183	      // 重力倒置（gravDir，R7）：方向取反（Player.cs:3207 vy×gravDir 全局语义近似）
1184	      this.vy = gd === 1
1185	        ? Math.min(this.vy + grav, MAX_FALL_SPEED)
1186	        : Math.max(this.vy - grav, -MAX_FALL_SPEED);
1187	      if (this.buffs.slowFall) this.fallStartY = null;
1188	      // 倒置时天花板即地板（TileCollision.hitHead → onGround 近似）
1189	      if (gd === -1) this.onGround = this.hitHead;
1190	    }
1191	    // 松键截断上升（手感；倒置时镜像）
1192	    if (!this.inputJump && (this.gravDir === 1 ? this.vy < -2 : this.vy > 2)) this.vy = 2 * this.gravDir;
1193	
1194	    // ---- 黏滞 tile（Collision.StickyTiles + Player.cs:22650-22740 1:1）----
1195	    // 蛛网(51)：泡在网里 X/Y 双重阻尼、禁跳、不计摔伤、挣扎随机会撕破网（掉蛛丝）；
1196	    // 蜂蜜块(229)：只阻尼、不破坏、不禁跳（原版 type!=229 才清 jump）
1197	    {
1198	      const stickId = TILE_BY_KEY['v_51_cobweb'] ?? 0;
1199	      const honeyId = TILE_BY_KEY['v_229_honey_block'] ?? 0;
1200	      const tx0 = Math.floor(this.x / TILE) - 1, tx1 = Math.floor((this.x + this.w) / TILE) + 1;
1201	      const ty0 = Math.floor(this.y / TILE) - 1, ty1 = Math.floor((this.y + this.h) / TILE) + 1;
1202	      let inWeb = false, inHoney = false;
1203	      let webTx = 0, webTy = 0;
1204	      // 扫描顺序 1:1（Collision.StickyTiles cs:3399-3402）：外层 X 自左向右、
1205	      // 内层 Y 自顶向下——撕网目标=最左重叠列的顶端那张（垂直蛛网串即从身体最上方
1206	      // 开始撕，原版语义；此前行优先会错撕横向蛛网层的最上行）
1207	      for (let tx = tx0; tx <= tx1 && !(inWeb || inHoney); tx++) {
1208	        for (let ty = ty0; ty <= ty1; ty++) {
1209	          if (!st.inBounds(tx, ty)) continue;
1210	          const t = st.type[st.idx(tx, ty)];
1211	          if (t === 0) continue;
1212	          const cell = { x: tx * TILE, y: ty * TILE };
1213	          const pad = t === honeyId ? 1 : 0;
1214	          if (this.x + this.w > cell.x - pad && this.x < cell.x + TILE + pad
1215	            && this.y + this.h > cell.y && this.y < cell.y + TILE + 0.01) {
1216	            if (t === stickId) { inWeb = true; webTx = tx; webTy = ty; break; }
1217	            if (t === honeyId) { inHoney = true; break; }
1218	          }
1219	        }
1220	      }
1221	      if (inWeb || inHoney) {
1222	        this.fallStartY = null; // fallStart 重置（黏滞中不积累摔伤）
1223	        // X 阻尼（L22688-22699）：钳 ±1；|vx|>0.75 → ×0.85，否则 ×0.6
1224	        this.vx = Math.max(-1, Math.min(1, this.vx));
1225	        this.vx *= Math.abs(this.vx) > 0.75 ? 0.85 : 0.6;
1226	        // Y 阻尼（gravDir=1，L22715-22726）：下落钳 1（缓沉）、上升钳 -5；
1227	        // 上升 ×0.96，下落 ×0.3
1228	        if (this.vy > 1) this.vy = 1;
1229	        if (this.vy < -5) this.vy = -5;
1230	        this.vy *= this.vy < 0 ? 0.96 : 0.3;
1231	        // 丝尘（Collision.cs:3416）：纠缠中速度>0.7 时每 tick 1/30 出白色网屑
1232	        if (inWeb && Math.abs(this.vx) + Math.abs(this.vy) > 0.7 && Math.random() < 1 / 30) {
1233	          game.spawnParticles(webTx * TILE + 8, webTy * TILE + 8, '#C8C8CC', 1, 0.4, { life: 26, damp: 0.96, grav: 0 });
1234	        }
1235	        // 蜂蜜滴落尘（Player.cs:22747-22760，dust 153）：1/5 且垂直有速
1236	        if (inHoney && (this.vy > 0.15 || this.vy < 0) && Math.random() < 1 / 5) {
1237	          const side = this.cx > webTx * TILE + TILE / 2 ? -1 : 1;
1238	          game.spawnParticles(this.cx + side * (this.w / 2 + 2), this.y + this.h * 0.6,
1239	            '#E8A020', 1, 0.3, { life: 22, damp: 0.97, grav: 0.02 });
1240	        }
1241	        if (inWeb) {
1242	          this.jumpHold = 0; // L22676：type != 229 → jump 清零（蛛网内禁跳）
1243	          // 挣扎撕网（L22653-22670）：移动中 stickyBreak++，超 rand(20,100) →
1244	          // WorldGen.KillTile(检测格)——原版直接破坏 StickyTiles 返回的那一格
1245	          if (this.vx !== 0 || this.vy !== 0) {
1246	            this.stickyBreak++;
1247	            if (this.stickyBreak > 20 + Math.floor(Math.random() * 80)) {
1248	              this.stickyBreak = 0;
1249	              st.setTile(webTx, webTy, 0);
1250	              // 破坏爆散（KillTile HitEffect 网屑四溅近似）
1251	              game.spawnParticles(webTx * TILE + 8, webTy * TILE + 8, '#C8C8CC', 8, 1.4, { life: 30, grav: 0.05 });
1252	              game.spawnDrop(webTx * TILE + 8, webTy * TILE, VANILLA_ITEM_KEY_BY_ID[150] ?? 'vi_150_cobweb', 1);
1253	            }
1254	          }
1255	        }
1256	      }
1257	    }
1258	
1259	    // 摔伤追踪：开始下落记录高度，落地结算
1260	    const fallVy = this.vy * this.gravDir;
1261	    if (!this.onGround && fallVy > 0 && this.fallStartY === null) {
1262	      this.fallStartY = this.y;
1263	    }
1264	    if (fallVy < -0.1) this.fallStartY = null; // 重新上升则重置
1265	
1266	    this.dropThrough = !!this.inputDown;
1267	    this.stepUp = true; // 原版玩家走 Collision.StepUp（Player.cs:23258/:27753）
1268	    // 落地冲击速度留存（原版 TryLandingOnDetonator Player.cs:34368 的 velocity.Y>=3 门；
1269	    // 碰撞前捕获——碰撞会清零 vy。Game 侧消费：落在起爆器 411 上触发电路）
1270	    const impactVy = this.vy;
1271	    const preY = this.y;
1272	    moveAndCollide(this, world, this.vx, this.vy);
1273	    this.landImpactVy = this.onGround && impactVy >= 3 ? impactVy : 0;
1274	    // StepUp 抬升检测（原版 gfxOffY）：水平移动中被抬升 ≤16px → 渲染缓动补偿
1275	    const lifted = preY - this.y;
1276	    if (this.inputX !== 0 && lifted > 0.5 && lifted <= 16.1) this.stepRenderY = lifted;
1277	
1278	    // 边缘滑落：已移除（改为收窄支撑判定宽度——本质相同但无侧推力）
1279	    if (false) {
1280	      const fy = Math.floor((this.y + this.h + 1) / TILE);
1281	      const fx0 = Math.floor(this.x / TILE), fx1 = Math.floor((this.x + this.w - 0.01) / TILE);
1282	      let support = 0;
1283	      let supportX = 0; // 支撑面积加权重心
1284	      for (let tx = fx0; tx <= fx1; tx++) {
1285	        if (!world.store.isSolid(tx, fy)) continue;
1286	        const left = Math.max(this.x, tx * TILE);
1287	        const right = Math.min(this.x + this.w, tx * TILE + TILE);
1288	        const ov = Math.max(0, right - left);
1289	        support += ov;
1290	        supportX += (left + right) / 2 * ov;
1291	      }
1292	      // 主动移动（上行爬坡/走动）时只在彻底失撑（≤2px）才坠落，不参与缓滑——
1293	      // 爬台阶时身体经常大半悬空，缓滑会把人往回推；静止站边缘才触发缓滑
1294	      const moving = this.inputX !== 0 && Math.abs(this.vx) > 0.3;
1295	      // 固定 3px 阈值：几乎完全悬空才滑落（比例阈值对放大后的宽碰撞盒过敏）
1296	      void moving;
1297	      if (support > 0 && support < 3) {
1298	        const cen = supportX / support;
1299	        const dir = cen < this.cx ? 1 : -1; // 支撑在身体哪侧，就往反侧滑
1300	        if (support <= 2) {
1301	          this.x += dir * 1.2;
1302	          this.onGround = false; // 彻底失撑，下坠
1303	        } else {
1304	          this.x += dir * 0.9; // 缓慢滑向悬空侧
1305	        }
1306	      }
1307	    }
1308	
1309	    // 自动上台阶：统一走原版 Collision.StepUp（moveAndCollide 内 stepUp 门，
1310	    // Physics/TileCollision.ts applyStepUp 1:1）——此前自研版只处理玩家，
1311	    // 敌人/小动物卡死半砖；原版玩家与 NPC 共用同一 StepUp。视觉缓动保留：
1312	    // 每帧检测被抬升时记录补偿高度
1313	    if (this.onGround && this.hitWall && this.inputX !== 0) {
1314	      // 碰撞被拦但 StepUp 已抬升过（y 比上一帧高出一格内）→ 渲染缓动
1315	      void 0;
1316	    }
1317	    // 台阶视觉缓动：每帧向 0 收敛
1318	    if (this.stepRenderY > 0.5) this.stepRenderY *= 0.55;
1319	    else this.stepRenderY = 0;
1320	    // ---- 职业状态机（对账批实装）----
1321	    // 狼人（月亮符 485 + 夜间：Player.cs:11488 链 wolfAcc&&night）
1322	    if (this.equipStats.wolfAcc && !(game.world.clock?.isDay ?? true)) this.buffs.apply(BuffType.Werewolf, 2);
1323	    // 磨刀站 3198 就近常驻（每 60t 扫 41×25 区）
1324	    if (--this.sharpenedCd <= 0) {
1325	      this.sharpenedCd = 60;
1326	      const stt = game.world.store;
1327	      const tid = TILE_BY_KEY['v_377_sharpening_station'] ?? -1;
1328	      if (tid > 0) {
1329	        const tx0 = Math.floor(this.cx / TILE) - 20, tx1 = tx0 + 40;
1330	        const ty0 = Math.floor(this.cy / TILE) - 12, ty1 = ty0 + 25;
1331	        outer: for (let ty = ty0; ty <= ty1; ty++) for (let tx = tx0; tx <= tx1; tx++) {
1332	          if (stt.inBounds(tx, ty) && stt.type[stt.idx(tx, ty)] === tid) { this.buffs.apply(BuffType.Sharpened, 2); break outer; }
1333	        }
1334	      }
1335	    }
1336	    // BOC 受击脉冲消费
1337	    if (this.bocPulse > 0) {
1338	      this.bocPulse = 0;
1339	      this.buffs.apply(BuffType.BrainOfConfusionBuff, 4);
1340	      for (const e of game.enemies()) {
1341	        const en = e as { cx?: number; cy?: number; confusedT?: number; dead?: boolean };
1342	        if (en.dead || en.cx === undefined || en.cy === undefined) continue;
1343	        if (Math.abs(en.cx - this.cx) < 300 && Math.abs(en.cy - this.cy) < 200) en.confusedT = 4;
1344	      }
1345	    }
1346	    // 潜行（1:1 改写 :25500-25567）：蘑菇矿套=移动蓄(|vx|+|vy|)×0.0075/t、静止散 0.015/t
1347	    // （攻击中 itemAnimation 门→近似 useTime>0 暂停 5t）；星璇套=双击↓开关 vortexStealthActive
1348	    // （开时 stealth 从满每 t -0.04、移速 ×0.3；再双击关）——星璇的增伤/暴在乘区读同一 stealth
1349	    // ⑭ 变态刀 3106 单件潜行（:25448-25493：挥击中 stealth +0.1/t 且 timer=15；
1350	    // 静止衰减同蘑菇矿；效果在 damageMult/critChance 消费）
1351	    const heldVid = (() => {
1352	      const d = ITEM_DEFS[this.inv.heldItem()?.id ?? -1];
1353	      return d?.vid ?? (d?.key?.startsWith('vi_') ? parseInt(d.key.slice(3), 10) : -1);
1354	    })();
1355	    if (heldVid === 3106) {
1356	      if (this.useTime > 0) { this.stealthTimer = 15; if (this.stealth > 0) this.stealth = Math.min(1, this.stealth + 0.1); }
1357	      else if (Math.abs(this.vx) < 0.1 && Math.abs(this.vy) < 0.1 && this.stealthTimer === 0 && this.stealth > 0) {
1358	        this.stealth = Math.max(0, this.stealth - 0.015);
1359	      }
1360	      if (this.stealthTimer > 0) this.stealthTimer--;
1361	    } else if (this.equipStats.shroomiteSet) {
1362	      if (this.useTime > 0) this.stealthTimer = 5;
1363	      const still = Math.abs(this.vx) < 0.1 && Math.abs(this.vy) < 0.1;
1364	      if (still) {
1365	        if (this.stealthTimer === 0 && this.stealth > 0) this.stealth = Math.max(0, this.stealth - 0.015);
1366	      } else {
1367	        this.stealth = Math.min(1, this.stealth + (Math.abs(this.vx) + Math.abs(this.vy)) * 0.0075);
1368	      }
1369	      if (this.stealthTimer > 0) this.stealthTimer--;
1370	    } else if (this.equipStats.vortexSet) {
1371	      // 双击↓检测（KeyDoubleTap :24740-24749 窗口 15t）
1372	      const downNow = this.inputDown;
1373	      if (downNow && !this.prevDown && this.downTapT > 0) {
1374	        this.vortexStealthActive = !this.vortexStealthActive;
1375	        if (this.vortexStealthActive) this.stealth = 1;
1376	      }
1377	      if (downNow && !this.prevDown) this.downTapT = 15;
1378	      else if (this.downTapT > 0) this.downTapT--;
1379	      this.prevDown = downNow;
1380	      if (this.vortexStealthActive) this.stealth = Math.max(0, this.stealth - 0.04);
1381	    } else {
1382	      this.stealth = 0;
1383	      this.vortexStealthActive = false;
1384	    }
1385	    // 星云三族逐级衰减（:11660-11670：到时降 1 级并重挂 480t，非直接清零）
1386	    for (let f = 0; f < 3; f++) {
1387	      if (this.nebula[f] > 0 && --this.nebulaT[f] <= 0) {
1388	        this.nebula[f]--;
1389	        if (this.nebula[f] > 0) this.nebulaT[f] = 480;
1390	      }
1391	    }
1392	    // 星云生命 173-175（:10111-10115 lifeRegen+6/级 = 3HP/s/级）
1393	    if (this.nebula[1] > 0 && this.hp > 0) {
1394	      this.nebulaLifeAccum += 3 * this.nebula[1] * dt;
1395	      if (this.nebulaLifeAccum >= 1) { const n = Math.floor(this.nebulaLifeAccum); this.nebulaLifeAccum -= n; this.hp = Math.min(this.maxHp, this.hp + n); }
1396	    }
1397	    // 星云魔力 176-178（:19214-19226 counter+level/t，>=6 → mana++）
1398	    if (this.nebula[2] > 0) {
1399	      this.nebulaManaAccum += this.nebula[2] * dt;
1400	      if (this.nebulaManaAccum >= 6) { this.nebulaManaAccum -= 6; this.mana = Math.min(this.maxMana, this.mana + 1); }
1401	    }
1402	    // 甲虫球时间蓄能（进攻+防御共用；窗口内每 tick +1，90t/球；受击掉球见 damage()）
1403	    if (this.lastMeleeTick > 0) {
1404	      this.lastMeleeTick--;
1405	      if ((this.equipStats.beetleOff || this.equipStats.beetleDef) && ++this.beetleCharge >= 90) {
1406	        this.beetleCharge = 0;
1407	        this.beetleOrbs = Math.min(3, this.beetleOrbs + 1);
1408	      }
1409	    } else this.beetleCharge = Math.max(0, this.beetleCharge - 2); // 断战缓退
1410	    // 鞭 buff 倒计时（WhipTagEffect.PlayerBuffTime=180 系）
1411	    for (const k of Object.keys(this.whipBuffs)) {
1412	      if (--this.whipBuffs[Number(k)] <= 0) delete this.whipBuffs[Number(k)];
1413	    }
1414	
1415	    // 落地摔伤结算（幸运马掌免疫；落在水里豁免——水有缓冲）
1416	    if (this.onGround && this.fallStartY !== null) {
1417	      const fallTiles = (this.y - this.fallStartY) / TILE;
1418	      this.fallStartY = null;
1419	      const feetLiq = world.store.liquid[world.store.idx(Math.floor(this.cx / TILE), Math.floor((this.y + this.h - 1) / TILE))];
1420	      const landedInWater = feetLiq > 60 || this.inWater;
1421	      if (landedInWater) { /* 落水缓冲：不计摔伤 */ }
1422	      else if (fallTiles > FALL_SAFE_TILES + this.equipStats.extraFall
1423	        && !(this.hasHorseshoe || this.equipStats.noFallDmg)) {
1424	        const safeT = FALL_SAFE_TILES + this.equipStats.extraFall;
1425	        const t = Math.min(1, (fallTiles - safeT) / (FALL_FATAL_TILES - FALL_SAFE_TILES));
1426	        const dmgPercent = 10 + 90 * t * t * t; // 10%~100% 三次方曲线（Maples 公式）
1427	        const dmg = Math.max(1, Math.round((dmgPercent / 100) * this.hp));
1428	        this.lastDamageCause = { kind: 'fell' };
1429	        this.damage(dmg, this.cx, this.y - 10);
1430	        game.playSfx('hurt');
1431	        game.addDamageNumber(this.cx, this.y, dmg, false, '#FF5050');
1432	      }
1433	    }
1434	
1435	    // 走跑动画计时（仅地面；空中贴图静态不参与动画）
1436	    if (Math.abs(this.vx) > 0.3 && this.onGround) this.animTime += Math.abs(this.vx);
1437	    else this.animTime = 0;
1438	
1439	    // 越界保护
1440	    const maxY = world.h * TILE;
1441	    if (this.y > maxY + 100) this.damage(9999, this.cx, this.y);
1442	    this.prevInputX = this.inputX; // 冲刺双击检测（DoCommonDashHandle release 语义）
1443	  }
1444	
1445	  /** 出水补气动画进度 0..1（-1 = 未在补气） */
1446	  refillT = -1;
1447	  refillDur = 1.11; // 本次补气总时长（按出水时的缺口比例：1.11s × 缺口）
1448	  refillFrom = 0;   // 出水时的余量（补气动画从此处起填）
1449	  static readonly REFILL_HOLD = 0.35; // 补满后满格停留时长
1450	  get refill01(): number {
1451	    return this.refillT < 0 ? 1 : Math.min(1, this.refillT / this.refillDur);
1452	  }
1453	
1454	  /** 当前正在消耗的那口气泡进度 0..1（1=满，趋 0 渐隐）；头部浸水外为 0 */
1455	  get breathDrain01(): number {
1456	    if (!this.headUnderwater || this.breath <= 0) return 0;
1457	    const per = Player.BREATH_SECONDS / Player.BREATH_BUBBLES;
1458	    return Math.max(0, Math.min(1, 1 - this.breathAccum / per));
1459	  }
1460	
1461	  // 输入状态由 Game 每帧写入
1462	  inputX = 0;
1463	  inputJump = false;
1464	  /** 多段跳剩余段（原版 RefreshDoubleJumps：落地时重置为 equipStats.jumpOpts 拷贝） */
1465	  extraJumps: string[] = [];
1466	  extraJumpCd = 0;
1467	  /** 火箭靴 1:1（Player.cs:2612/26548-26628）：rocketTime 剩余脉冲次数（max=7）/
1468	   *  rocketDelay 推力脉冲倒计时（每次触发=10t 加速段）/ rocketDelay2 焰间隔
1469	   *  （1 档 30 / 2+ 档 15）/ canRocket 门（vy>-jumpSpeed 才可启动）/ rocketRelease
1470	   *  需松跳重触发 */
1471	  rocketTime = 0;
1472	  rocketDelay = 0;
1473	  rocketDelay2 = 0;
1474	  canRocket = false;
1475	  rocketRelease = false;
1476	  /** WingMovement（Player.cs:21746-21966）1:1：飞行中每 tick 垂直运动。
1477	   *  wings==4（UFO 之翼）+TryingToHoverUp 独占分支（消耗 ×2）；
1478	   *  其余按翼型参数表（num 恒减/num2 下落减速/num5 上升微推/num4 jumpSpeed 区间
1479	   *  系数/num3 上升帽系数），上升帽 = -jumpSpeed×num3（1.5~4.5 按翼型）；
1480	   *  hover 下落无左右移时 wingTime 消耗减半（×0.5） */
1481	  private wingMovement(wings: number, hoverDown: boolean, JS: number): void {
1482	    if (wings === 4 && this.inputUp) {
1483	      // wingsLogic 4 + TryingToHoverUp（:21748-21782）
1484	      this.vy -= 0.2;
1485	      if (this.vy > 0) this.vy -= 1;
1486	      else if (this.vy > -JS) this.vy -= 0.2;
1487	      if (this.vy < -JS * 3) this.vy = -JS * 3;
1488	      this.wingTime -= 2;
1489	    } else {
1490	      // 参数表（:21785-21789 基准 + 翼型覆盖 :21790-21921）
1491	      let num = 0.1, num2 = 0.5, num3 = 1.5, num4 = 0.5, num5 = 0.1;
1492	      if (wings === 26) { num2 = 0.75; num5 = 0.15; num4 = 1; num3 = 2.5; num = 0.125; }
1493	      if (wings === 8 || wings === 11 || wings === 24 || wings === 27 || wings === 22) num3 = 1.66;
1494	      if (wings === 21 || wings === 12 || wings === 20 || wings === 23) num3 = 1.805;
1495	      if (wings === 37) { num2 = 0.75; num5 = 0.15; num4 = 1; num3 = 2.5; num = 0.125; }
1496	      if (wings === 44 || wings === 45) {
1497	        // 星尘/星旋悬浮强化：±0.4 hover 推力（:21814-21904）
1498	        if (wings === 44) { num2 = 0.85; num3 = 2.75; }
1499	        else { num2 = 0.95; num3 = 4.5; }
1500	        num5 = 0.15; num4 = 1; num = 0.125;
1501	        if (this.inputUp) {
1502	          // TryingToHoverUp 附加推力（:21821-21838 / :21866-21883 同构）
1503	          this.vy -= 0.4;
1504	          if (this.vy > 0) this.vy -= 1;
1505	          else if (this.vy > -JS) this.vy -= 0.2;
1506	          if (this.vy < -JS * 3) this.vy = -JS * 3;
1507	        }
1508	        // （:21855/:21900 TryingToHoverDown && !controlJump 下沉分支在原版调用门
1509	        //  flag19（要求 controlJump）下不可达——反编译证实为死分支，不移植）
1510	      }
1511	      if (wings === 29 || wings === 32) { num2 = 0.85; num5 = 0.15; num4 = 1; num3 = 3; num = 0.135; }
1512	      if (wings === 30 || wings === 31) { num4 = 1; num3 = 2.45; if (!hoverDown) num = 0.15; }
1513	      // 主体（:21922-21952，gravDir=1 半边）
1514	      this.vy -= num;
1515	      if (this.vy > 0) this.vy -= num2;
1516	      else if (this.vy > -JS * num4) this.vy -= num5;
1517	      if (this.vy < -JS * num3) this.vy = -JS * num3;
1518	      // wingTime 消耗（:21953-21960）：hover 下落且无左右移 ×0.5
1519	      const halfCost = (wings === 22 || wings === 28 || wings === 30 || wings === 31
1520	        || wings === 37 || wings === 45) && hoverDown && this.inputX === 0;
1521	      this.wingTime -= halfCost ? 0.5 : 1;
1522	    }
1523	    this.fallStartY = null;
1524	  }
1525	
1526	  /** 恐慌项链受击加速计时（tick，原版 panicTime=300） */
1527	  panicTime = 0;
1528	  /** 岩浆免疫剩余 tick（熔岩护身符族 lavaMax；离开岩浆回满） */
1529	  lavaImmuneTicks = 0;
1530	  /** 翅膀：剩余飞行 tick（float，hover 下落档 0.5/tick）+ 需松跳键重触发 */
1531	  wingTime = 0;
1532	  wingRelease = true;
1533	  /** 飞毯触发门（CarpetMovement :21575：起跳后置 true，触发一次即 false） */
1534	  canCarpet = true;
1535	  /** 翅膀动画帧（WingFrame :29002：0 收起 / flap 循环 1→2→3→2 / 滑翔 2）+ 拍速计数 */
1536	  wingFrame = 0;
1537	  private wingFrameCounter = 0;
1538	
1539	  /** 飞毯滑翔剩余 tick（CarpetMovement carpetTime=300） */
1540	  carpetTime = 0;
1541	  /** 冲刺：双击窗口（dashTime ±15）/ 方向 / dashDelay 三态（0 就绪 / -1 滑行 / >0 冷却） */
1542	  dashT = 0;
1543	  dashDir = 1;
1544	  dashDelay = 0;
1545	  /** 克苏鲁护盾冲撞判定窗（eocDash :20784，触发=15/命中=10）+ 已命中敌 id（eocHit） */
1546	  eocDash = 0;
1547	  eocHitId = -1;
1548	  prevInputX = 0;
1549	  /** 水面行走状态（水上漂靴族：站在液面，按 ↓ 下潜） */
1550	  onWaterSurface = false;
1551	  /** 所在沙漠区（Game 每帧同步 scene.zoneDesert） */
1552	  zoneDesert = false;
1553	  /** 脚下是沙族地格（runningOnSand，FloorVisuals :23457——沙丘行者靴消费）。
1554	   *  原版只在 vy==0 时刷新、离地不清零（ResetFloorFlags 仅重生/传送） */
1555	  runningOnSand = false;
1556	  /** 重力方向（R7：1 普通 / -1 倒置——重力药水 buff 18 激活时按 Up 切换，Player.gravDir）
1557	   *  倒置 = 重力/跳跃/落点起点全部取反；onGround 由 hitHead 近似（天花板当地板） */
1558	  gravDir: 1 | -1 = 1;
1559	  /** 贴墙缓降中（spikedBoots 攀壁） */
1560	  wallCling = false;
1561	  /** 拾取范围扩展（宝藏磁石/金戒指族，px；defaultItemGrabRange=42） */
1562	  get grabRangeBonus(): number {
1563	    return this.equipStats.treasureMagnet ? 94 : this.equipStats.goldRing ? 12 : 0;
1564	  }
1565	  /** 红心拾取范围扩展（拾心药水 lifeMagnet，ItemDrop 心分支消费） */
1566	  get heartGrabBonus(): number {
1567	    return this.buffs.has(BuffType.Heartreach) ? 60 : 0;
1568	  }
1569	  /** 魔力星拾取范围扩展（魔力磁石族 manaMagnet，ItemDrop 星分支消费） */
1570	  get manaMagnetBonus(): number {
1571	    return this.equipStats.manaMagnet ? 80 : 0;
1572	  }
1573	  /** 幸运度聚合态（src/stats/Luck.ts LuckState；环境因子由 Game 扫描写入，
1574	   *  RecalculateLuck :28672-28697 各项见 LuckState 注释） */
1575	  readonly luckState = new LuckState();
1576	  /** 吸血预算（Player.cs:962 初始 99999 → 首帧 Update 钳到上限；本体语义 =
1577	   *  每秒可吸血总量池）。Game 每 tick 回充：普通 +0.6 钳 80 / 专家 +0.5 钳 70
1578	   *  （:24196-24216）。吸血命中扣全额浮点（Projectile.cs:11417/:11444） */
1579	  lifeSteal = 80;
1580	  /** 幸运值（RecalculateLuck :28672-28697 1:1）：
1581	   *  luck = 瓢虫×0.2 + 火炬×0.2 + 药水档×0.1 + 风筝档×0.1/3 + 银河珍珠 0.03
1582	   *        + 灯笼夜 0.3 + 地精 0.2 − 臭屁 0.25 + 装备 + 钱币 − 碎镜 0.25。
1583	   *  不 clamp——luckMinimumCap=-0.7/luckMaximumCap=1（Player.cs:2952/2954）只喂 UI 计量
1584	   *  （:3950-3957），聚合本体可超界（原版如此）。
1585	   *  来源接线：药水 buff 257 三档 / 灯笼夜 / 地精+火炬（Game 15t 扫描）/ 装备（幸运币 855
1586	   *  +0.05、马掌族 +0.05，Player.cs:12629-12647）已接；瓢虫 359/360、buff 383 风筝、
1587	   *  buff 120 臭屁、银河珍珠 5340、碎镜 810、微光化币——登记（物品/子系统未移植） */
1588	  get luck(): number {
1589	    const l = this.luckState;
1590	    let v = l.ladyBugLuck * 0.2 + l.torchLuck * 0.2;        // :28673
1591	    v += this.luckPotionTier * 0.1;                          // :28674（buff 257 三档）
1592	    v += this.kiteLuckTier * (0.1 / 3);                      // :28675（buff 383 三档）
1593	    if (l.usedGalaxyPearl) v += 0.03;                        // :28676-28678
1594	    if (l.lanternsUp) v += 0.3;                              // :28679-28682
1595	    if (l.hasGardenGnomeNearby) v += 0.2;                    // :28683-28686
1596	    if (l.stinky || this.buffs.has(BuffType.Stinky)) v -= 0.25; // :28687-28690（buff 120 → stinky；l.stinky 为环境外注入位）
1597	    v += this.luckEquipmentBonus;                            // :28692
1598	    v += l.coinLuckValue;                                    // :28693
1599	    if (l.brokenMirrorBadLuck) v -= 0.25;                    // :28694-28696
1600	    return v;
1601	  }
1602	  /** luckPotion（Player.cs:9971-9982 buff 257 分档）：0 无 / >600s=3 / >300s=2 / 其余 1 */
1603	  get luckPotionTier(): number {
1604	    const left = this.buffs.active.get(BuffType.Luck);
1605	    if (left === undefined) return 0;
1606	    return left > 600 ? 3 : left > 300 ? 2 : 1;
1607	  }
1608	  /** kiteLuckLevel（Player.cs:9618-9623 buff 383）：clamp(buffTime/10800, 0, 3)——
1609	   *  active 存秒，10800t=180s 一档；无 buff = 0（luck += 档×0.1/3 :28675） */
1610	  get kiteLuckTier(): number {
1611	    return this.buffs.kiteLuckLevel;
1612	  }
1613	  /** equipmentBasedLuckBonus（Player.cs:12629-12647）：
1614	   *  幸运币 855 +0.05（hasLuck_LuckyCoin）/ 马掌族 +0.05（hasLuck_LuckyHorseshoe）。
1615	   *  四叶草 5574 +0.03 / 枯萎 5575 −0.1 / 乌鸦羽 5576 −0.1（RefreshInfoAccsFromItemType
1616	   *  :12321-12332）——三件物品未入物品表，登记 */
1617	  get luckEquipmentBonus(): number {
1618	    let b = this.equipStats.luckyCoin ? 0.05 : 0;
1619	    if (this.hasHorseshoe) b += 0.05;
1620	    return b;
1621	  }
1622	  inputDown = false;
1623	  inputUp = false;
1624	  onRope = false;
1625	
1626	  /** 受击：防御减伤公式 max(1, dmg - defense*0.5)（移植自 Maples Player.OnAttacked）。
1627	   *  knockback=false 用于窒息等环境伤害（只掉血不击退） */
1628	  damage(dmg: number, srcX: number, srcY: number, knockback = true): boolean {
1629	    // 微光化免伤（Player.cs:37591-37595 Hurt 前置：shimmering 且可闪避 → 直接返回 0；
1630	    // 本仓 damage 以 false 表示完全免伤——Boss 专属弹幕 371 等不可闪避源未移植）
1631	    if (this.shimmering) return false;
1632	    if (this.iframes > 0 || this.dead) return false;
1633	    const eq = this.equipStats;
1634	    // 黑带/忍者大师装备 10% 闪避（Player.Hurt :9772 blackBelt 分支）
1635	    if (eq.blackBelt && Math.random() < 0.1) return false;
1636	    // 耐久药水(114)：endurance+0.1 → 受伤 ×0.9（Player.endurance 在 Hurt 结算）
1637	    const endurance = (this.buffs.has(BuffType.Endurance) ? 0.1 : 0)
1638	      + (this.equipStats.beetleDef ? 0.15 * this.beetleOrbs : 0); // 甲虫壳每球 15%（buffs 95-97）
1639	    const reduction = Math.max(1, Math.round((dmg - this.defense * 0.5) * (1 - endurance)));
1640	    this.hp -= reduction;
1641	    // 十字项链/星星面纱：无敌帧翻倍（longInvince）
1642	    this.iframes = PLAYER_IFRAME_TICKS * (eq.longInvince ? 2 : 1);
1643	    this.sinceHurt = 0; // 受击打断自然回血
1644	    // 甲虫攻击球受击掉一颗
1645	    if (this.beetleOrbs > 0) this.beetleOrbs--;
1646	    // 混乱之脑（:37488-37496：受击 1/6 → buff 321 + 困惑近敌；damage 无 game 参→脉冲标志）
1647	    if (this.equipStats.boc && Math.random() < 1 / 6) this.bocPulse = 1;
1648	    // 恐慌项链：受击触发 5 秒移速爆发（panicTime=300，PanicSpeedBoost :25034）
1649	    if (eq.panic) this.panicTime = 300;
1650	    // 魔力手铐（magicCuffs :37678）：受伤回蓝 = 原始伤害 1:1（防前数值）
1651	    if (eq.magicCuffs) this.mana = Math.min(this.maxMana, this.mana + dmg);
1652	    // 击退（钴护盾族 noKnockback 免疫）
1653	    if (knockback && !eq.noKnockback) {
1654	      const dir = this.cx < srcX ? -1 : 1;
1655	      this.vx = dir * 3.4;
1656	      this.vy = -3;
1657	    }
1658	    return true;
1659	  }
1660	
1661	  /** ShimmerUnstuck（Player.cs:28394-28428）：timeShimmering 清零，找最近无微光
1662	   *  落点传送（TryFindingShimmerFreeSpot :28414-28440，落点 = spot+(0,-2)px、
1663	   *  velocity=(0,0.0001)），清微光化态；找不到则保持原位等下一轮（原版同样仅
1664	   *  StartUnstuck 辅助）。传送附带短暂无敌帧（原版 Teleport style 12 的 immune
1665	   *  语义近似——落点邻敌免秒杀） */
1666	  private shimmerUnstuck(game: GameHooks, world: import('../world/World').World): void {
1667	    this.timeShimmering = 0;
1668	    const st = world.store;
1669	    // 三层兜底（原版 :28442-28469）：玩家周围 → 出生点——保证封闭洞穴内也必脱困
1670	    const spot = findShimmerFreeSpot(
1671	      st, Math.floor(this.cx / TILE), Math.floor(this.y / TILE),
1672	      world.spawnX, world.spawnY,
1673	    );
1674	    if (!spot) return;
1675	    const p = shimmerTeleportPos(spot);
1676	    this.x = p.x;
1677	    this.y = p.y;
1678	    this.vx = 0;
1679	    this.vy = 0.0001;
1680	    this.shimmering = false;
1681	    this.inShimmer = false;
1682	    this.iframes = Math.max(this.iframes, PLAYER_IFRAME_TICKS);
1683	    game.spawnParticles(this.cx, this.cy, '#BFE8FF', 14, 1.4, { life: 30, grav: -0.04 });
1684	    game.playSfx('shimmerSplash', 0.75, this.cx, this.cy);
1685	  }
1686	
1687	  /** ApplyTouchDamage（Player.cs:28507）1:1:直接伤害(护甲结算)→灼烧/流血 buff→
1688	   *  窒息延迟→荆棘族触碰毁块。伤害被完全抵消(含无敌帧)时跳过 buff 授予(原版 num83==0 分支) */
1689	  private suffocateDelay = 0;
1690	  private applyTouchDamage(game: GameHooks, ht: HurtTile): void {
1691	    let blocked = false;
1692	    const dmg = TOUCH_IMMEDIATE.get(ht.type);
1693	    if (dmg !== undefined) {
1694	      this.lastDamageCause = { kind: 'default' }; // PlayerDeathReason.ByOther(3) → 默认包
1695	      if (!this.damage(dmg, this.cx, this.y - 10, false)) {
1696	        blocked = true;
1697	      } else {
1698	        game.playSfx('hurt');
1699	        game.addDamageNumber(this.cx, this.y, Math.max(1, Math.round(dmg - this.defense * 0.5)), false, '#FF5050');
1700	      }
1701	    }
1702	    if (!blocked) {
1703	      if (TOUCH_HOT.has(ht.type)) this.buffs.apply(BuffType.Burning, 20 / 60);   // AddBuff(67,20)
1704	      if (TOUCH_BLEEDING.has(ht.type)) this.buffs.apply(BuffType.Bleeding, (600 + Math.random() * 600) / 60); // AddBuff(30,600-1200)
1705	    }
1706	    if (SUFFOCATE.has(ht.type)) {
1707	      if (this.suffocateDelay < 5) this.suffocateDelay++;       // suffocateDelay<5 递增
1708	      else this.buffs.apply(BuffType.Suffocation, 1 / 60);      // 满后每 tick AddBuff(68,1)
1709	    } else {
1710	      this.suffocateDelay = 0;
1711	    }
1712	    if (TOUCH_DESTROY.has(ht.type)) {
1713	      game.world.breakTileAt(ht.x, ht.y); // TouchDamageDestroyTile → KillTile
1714	    }
1715	  }
1716	
1717	  /** 清坠落起点(F10 调试瞬移用):瞬移不结算高空摔伤 */
1718	  clearFall(): void {
1719	    this.fallStartY = null;
1720	  }
1721	
1722	  draw() { /* 由 Renderer 统一绘制 */ }
1723	}
1724	

```


---

## 🤖 Assistant · 2026-08-12T09:23:53.029Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Shimmer\" ~/Project/GLM/SandboxWorld/game/src/systems/Buffs.ts 2>/dev/null | head -20; echo ---; grep -rln \"BuffType\" ~/Project/GLM/SandboxWorld/game/src --include=*.ts | head",
 "description": "Find BuffType enum definition location"
}
```


---

## 🤖 Assistant · 2026-08-12T09:23:53.073Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"shimmer\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -40; echo ---; ls ~/Project/GLM/SandboxWorld/game/tests/ | grep -i shimmer",
 "description": "Check Enemy shimmer logic and existing tests"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:23:53.102Z

**📎 ToolResult**

```
---
(eval):1: no matches found: --include=*.ts

```


---

## 👤 User(sidechain) · 2026-08-12T09:23:53.129Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:320:  /** 微光浸入进度（≈shimmerTransparency ×100，NPC.cs:92468-92483：+0.01/t，
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:322:  shimmerT = 0;
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:651:    // 微光接触（NPC.cs:94268-94274）：WetCollision 盒命中微光 → shimmerWet +
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:652:    // TryAddingRepeatedBuff(353,100)；buff 353 → shimmering（:93313-93321）→
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:653:    // shimmerTransparency +0.01/t（:92468-92483）>0.9 → GetShimmered。离池衰减
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:657:        this.shimmerT += 1;
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:658:        if (this.shimmerT > 90) this.npcGetShimmered(game);
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:659:      } else if (this.shimmerT > 0) {
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:660:        this.shimmerT -= 1;
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1399:   *  掉微光化物品后消散（:92535-92560）。表来自 tools/extract-shimmer.mjs
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1404:    this.shimmerT = 0;
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1420:        if (d) { d.shimmered = true; d.shimmerTime = 1; }  // 微光化物品上浮（:92540-92545）
---
shimmer.test.ts

```


---

## 🤖 Assistant · 2026-08-12T09:24:07.477Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I've read Player.ts fully. Key observations:

1. Line 711-714: inShimmer / shimmering detection survived, buffs.apply(BuffType.Shimmered, 1) survived. Good.
2. Line 922-927: shimmering branch zeroes inputs — survived.
3. BUT the critical issue: **the horizontal movement block (lines 860-889) runs BEFORE the shimmering physics else-if chain (lines 914-927)**. In the shimmering branch, inputX is zeroed at line 925, but the horizontal acceleration at line 870-876 already consumed `this.inputX` (via `const ix = this.inputX;` at line 860). So zeroing inputX at 925 doesn't prevent the movement at 871. Wait — zeroing inputX at line 925 happens after `ix` was captured at 860 and after acceleration at 870-886. So the player still accelerates horizontally. Also moveAndCollide at line 1272 uses this.vx which still has horizontal velocity from the acceleration.

Actually in original old code, presumably the shimmering input zeroing happened before the horizontal movement. So the fix: move input zeroing (for shimmering) to before horizontal movement — i.e., extend the Frozen zeroing at line 850 to include shimmering, OR reorder.

Best fix per vanilla: vanilla Player.Update: `if (shimmering) frozen = true` → frozen causes controlUp/controlDown/controlLeft/controlRight/controlJump = false early in Update. So the input zeroing should happen at the same place as the Frozen zeroing (line 850), i.e., before horizontal movement.

So modify line 850:

```ts
if (this.buffs.has(BuffType.Frozen) || this.shimmering) { this.inputX = 0; ... }
```

But wait — shimmering is computed at line 712 which is before 850. Yes, shimmering is computed at line 712, before line 850. 

But there's also the else-if chain at 915-927 which zeroes again — harmless.

But also the `this.inShimmer && !this.shimmering` buoyancy branch is in the else-if chain after rope. That's fine.

However, there's another consideration: with inputX zeroed at 850, at 860 `ix = this.inputX` = 0 → friction applied → vx decays. Good — player can't walk.

Also need to check: does Game write inputX after fixedUpdate and do a second movement? Need to check Game.ts. Let me grep for inputX writes and where player.fixedUpdate is called.

Also check ridingCart: line 854-859 — `if (this.ridingCart) { ...; return; }`. This return happens before the shimmering physics else-if chain, but input zeroing at 850 is before it, so shimmering + ridingCart → input zeroed (vanilla: on cart in shimmer still works? The prompt says "原版矿车上微光仍生效" — original cart in shimmer still works... hmm, actually it says check that ridingCart branch return doesn't bypass shimmer. Input zeroing at 850 is before the return, so frozen/shimmering input zeroing applies. Fine.)

Now item 2: buffs.apply(BuffType.Shimmered, 1) survived at 714. Need to check BuffType.Shimmered = 77? The prompt said "BuffType.Shimmered=77 枚举" — wait, buff 353 is Shimmered. Let me check Buffs.ts for Shimmered enum value. The prompt says confirm `BuffType.Shimmered=77`... hmm that seems odd. Maybe the local enum uses a compact numbering. Let me check src/stats/Buffs.ts.

3. UI.ts icon mapping: grep returned NOTHING for "Shimmered|shimmer" in UI.ts. Wait — the first grep on UI.ts returned no output at all. Hmm, but maybe UI.ts path is wrong. Let me check where the buff icon map is. Grep for 'vi_5340_galaxy_pearl' across src.

4. Enemy shimmer: lines 651-660 in Enemy.ts — check what condition gates it. Let me read that region.

5. tests/shimmer.test.ts exists.

Also need to check Game.ts: order of input write vs player.fixedUpdate, and whether a second movement happens.

Let me gather all these in parallel.
````

</details>


---

## 🤖 Assistant · 2026-08-12T09:24:09.080Z · glm-x-preview-260804

```
Player.ts 读完。关键发现：`buffs.apply(Shimmered)`（:714）和微光物理分支（:915-927）都幸存，但**输入清零在 :925 位于水平移动积分（:860-889，`const ix = this.inputX` 已在 :860 消费）之后**——清零形同虚设。另外 UI.ts 里 grep 不到任何 Shimmered/shimmer，疑似图标映射确实没加上。继续核对 Buffs 枚举、Game 输入顺序、Enemy 微光门、UI 图标表。
```


---

## 🤖 Assistant · 2026-08-12T09:24:09.926Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Shimmered\" ~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts; echo ===; grep -rn \"Shimmered\\|galaxy_pearl\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" -l 2>/dev/null || grep -rn \"Shimmered\" ~/Project/GLM/SandboxWorld/game/src -l",
 "description": "Find BuffType.Shimmered enum and all referencing files"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:09.998Z

**📎 ToolResult**

```
114:  Shimmered = 77,   // 微光化(353,浸微光每 tick 刷新)：frozen 封输入+免伤+慢沉——
176:  [BuffType.Shimmered]: { vanillaBuff: 353, descKey: 'Mods.SandboxWorld.Buff.Shimmered.Desc', fallbackName: '微光化' },
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-12T09:24:10.554Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"inputX\\|inputJump\" ~/Project/GLM/SandboxWorld/game/src/Game.ts | head -30; echo ===; grep -n \"fixedUpdate\" ~/Project/GLM/SandboxWorld/game/src/Game.ts | head",
 "description": "Check Game.ts input write order vs fixedUpdate"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:10.619Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
ugrep: warning: ~/Project/GLM/SandboxWorld/game/src/Game.ts: No such file or directory
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-12T09:24:11.309Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"galaxy_pearl\\|buffIcon\\|BUFF_ICON\\|buffIcons\" ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts | head; echo ===; ls ~/Project/GLM/SandboxWorld/game/src/ui/ | head -40",
 "description": "Locate buff icon map in UI files"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:11.396Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:1767:      const iconId = this.buffIconItem.get(t);
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:1779:  buffIconItem = new Map<BuffType, number>();
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2429:    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);  }
~/Project/GLM/SandboxWorld/game/src/ui/UI.ts:2503:    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-12T09:24:11.552Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "offset": 630,
 "limit": 60
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:11.583Z

**📎 ToolResult**

```
630	    // 岩浆接触（NPC.cs:94520-94545）：30t 独立冷却（immune[255],不受普通受击 iframes 影响）,
631	    // onFire 7s + 50 直伤;lavaImmune 族（NPC_LAVA_IMMUNE,SetDefaults 提取）完全豁免
632	    if (this.vanillaId === null || !NPC_LAVA_IMMUNE.has(this.vanillaId)) {
633	      if (this.lavaCd > 0) this.lavaCd--;
634	      const inLava = liquidCollision(game.world.store, this.x, this.y, this.w, this.h, 2);
635	      if (inLava) {
636	        this.lavaWet = true;
637	        if (this.lavaCd <= 0) {
638	          this.lavaCd = 30;
639	          this.onFireT = Math.max(this.onFireT, 7); // AddBuff(24,420)
640	          this.hurt(50, 0, 0, game);                // StrikeNPCNoInteraction(50)
641	          game.spawnParticles(this.cx, this.cy, '#FF9A3C', 10, 1.6, { life: 30, grav: -0.05 });
642	        }
643	      } else {
644	        this.lavaWet = false;
645	      }
646	    } else {
647	      this.lavaWet = false;
648	    }
649	    // 入水熄灭 onFire（NPC.cs:94284 TryRemovingWaterPerishableEffects:水湿(非岩浆)→DelBuff 24）
650	    if (this.inWater && !this.lavaWet) this.onFireT = 0;
651	    // 微光接触（NPC.cs:94268-94274）：WetCollision 盒命中微光 → shimmerWet +
652	    // TryAddingRepeatedBuff(353,100)；buff 353 → shimmering（:93313-93321）→
653	    // shimmerTransparency +0.01/t（:92468-92483）>0.9 → GetShimmered。离池衰减
654	    // （:92484-92500）视觉侧未接（GAP），此处只保留转化触发计时
655	    if (this.vanillaId !== null && !this.def.boss) {
656	      if (liquidCollision(game.world.store, this.x, this.y, this.w, this.h, 4)) {
657	        this.shimmerT += 1;
658	        if (this.shimmerT > 90) this.npcGetShimmered(game);
659	      } else if (this.shimmerT > 0) {
660	        this.shimmerT -= 1;
661	      }
662	    }
663	    // onFire DoT（NPC.cs:92619:lifeRegen-8 = 4 HP/s,无防御结算）+ 火尘粒子（:92187）
664	    if (this.onFireT > 0) {
665	      this.onFireT -= dt;
666	      this.onFireDoT += 4 * dt;
667	      if (this.onFireDoT >= 1) {
668	        const n = Math.floor(this.onFireDoT);
669	        this.onFireDoT -= n;
670	        this.hp -= n;
671	        this.hpBarT = 240;
672	        if (this.hp <= 0) this.hurt(9999, 0, 0, game); // 走标准死亡管线(掉落/分裂/联机)
673	      }
674	      if (Math.random() < 0.75) {
675	        game.spawnParticles(
676	          this.x + Math.random() * this.w, this.y + Math.random() * this.h,
677	          Math.random() < 0.7 ? '#FF9A3C' : '#FFD24A', 1, 0.8,
678	          { life: 26 + Math.random() * 14, grav: -0.06, damp: 0.96 });
679	      }
680	    }
681	
682	    // ---- 武器浸剂 debuff 滴血（R2，NPC.cs:92585/92697/92708 DoT 同 onFire 模式） ----
683	    if (this.poisonT > 0) { this.poisonT -= dt; this.poisonDoT += 6 * dt; }
684	    if (this.venomT > 0) { this.venomT -= dt; this.venomDoT += 30 * dt; }
685	    if (this.cursedT > 0) { this.cursedT -= dt; this.cursedDoT += 24 * dt; }
686	    for (const [tKey, dKey] of [['poisonT', 'poisonDoT'], ['venomT', 'venomDoT'], ['cursedT', 'cursedDoT']] as const) {
687	      const acc = this[dKey];
688	      if (acc >= 1) {
689	        const n = Math.floor(acc);

```


---

## 🤖 Assistant · 2026-08-12T09:24:23.746Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Findings so far:

- BuffType.Shimmered = 77 exists in Buffs.ts, with vanillaBuff 353 and descKey. Good.
- UI.ts has two map fill loops at :2429 and :2503 (`for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key])`). Grep found NO Shimmered in UI.ts → the icon mapping `[BuffType.Shimmered, 'vi_5340_galaxy_pearl']` is indeed missing. Need to add to both maps (the prompt says "若缺则补两处 map 都加").
- Enemy shimmer logic at :655-662 looks intact (gate: vanillaId !== null && !boss; box collision with liquid type 4; shimmerT>90 → npcGetShimmered). So enemy shimmer chain seems alive. But the user reports "monsters can also enter the lake" — which per prompt note 3: vanilla enemies CAN walk into shimmer physically; after 90t they transform. So enemy chain may be alive — but need to verify npcGetShimmered works and whether Enemy can path into shimmer. Actually the user complaint "怪物也能进湖（无法攻击角色——伤害免疫生效了）" — the prompt says verify the chain is alive. It looks alive. But let me check whether liquidCollision with type 4 works and whether npcGetShimmered is gated by something that fails. Also check Enemy's avoidShimmer — vanilla: enemies avoid shimmer? Actually in vanilla, NPCs avoid shimmer via `NPC.AI` checking... hmm. The prompt says "原版敌怪物理上可以走进湖（无 avoidShimmer），但 90t 后应触发转化". So our behavior matches vanilla: they walk in and after 90t transform. So the Enemy side is fine, provided npcGetShimmered triggers. But wait — is Enemy.shimmerT only incremented when `this.vanillaId !== null && !this.def.boss`? Yes. Fine.

But actually — hmm, one important check: does the player's shimmering detection work at all? The user says damage immunity works ("无法攻击角色——伤害免疫生效了"), meaning `this.shimmering` is true in damage(). damage() checks this.shimmering. And shimmering is set at :712. So detection works.

So the two real bugs:
1. Input zeroing happens after movement consumption → player can walk. FIX: add shimmering to the Frozen zeroing block at :850 (which runs before horizontal movement). Vanilla order: buff 353 → frozen → control* cleared early in Update before movement.

Wait, but there's a subtlety: the zeroing at :850 comment says "帧末由 Game 重灌输入" — Game re-writes input at frame end. So zeroing must happen before movement within fixedUpdate. :850 is before movement. Good.

But also, even if inputX is zeroed at :850, does moveAndCollide at :1272 still use vx? Friction would apply at :874 since ix===0 → vx *= friction → decays. Good, player slows to stop. Cannot walk. 

2. Buff icon mapping missing in UI.ts both maps → no debuff icon. FIX: add `[BuffType.Shimmered, 'vi_5340_galaxy_pearl']` to both maps. Need to check ITEM_BY_KEY includes that key, and whether the texture/asset is whitelisted. Let me check what these maps look like and confirm 'vi_5340_galaxy_pearl' exists in ITEM_BY_KEY. Also check BuffType import in UI.ts.

Also need to check where BuffType.Shimmered buff is displayed: UI iterates buffs. Let me look at UI.ts :1750-1790 and :2420-2510.

Also check Game.ts location: src/Game.ts doesn't exist. Find where player.fixedUpdate is called.

Also check tests/shimmer.test.ts current content.

Let me run these.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:24:24.581Z · glm-x-preview-260804

```
BuffType.Shimmered=77 存在；UI.ts 两处 map 填充（:2429/:2503）都没有 Shimmered 条目——图标映射确认缺失。Enemy 侧微光链（:655-662）结构完好。继续看 UI 两处 map 内容、Game 主循环输入顺序、现有测试。
```


---

## 🤖 Assistant · 2026-08-12T09:24:24.811Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/UI.ts",
 "offset": 2420,
 "limit": 90
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:24.826Z

**📎 ToolResult**

```
2420	      [BuffType.Lifeforce, 'vi_2345_LifeforcePotion'], [BuffType.Endurance, 'vi_2346_EndurancePotion'],
2421	      [BuffType.Wrath, 'vi_2349_WrathPotion'], [BuffType.Rage, 'vi_2347_RagePotion'],
2422	      [BuffType.Tipsy, 'vi_2266_Sake'],
2423	      // 后期批（近似图标：月噬→吸血鬼 knives / 遮挡→暗影钥匙）
2424	      [BuffType.MoonLeech, 'vi_1569_vampire_knives'], [BuffType.Obstructed, 'vi_329_shadow_key'],
2425	      // 食物三档（以已注册食物贴图为图标近似）
2426	      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],
2427	      [BuffType.WellFed3, 'vi_1919_sugar_cookie'],
2428	    ];
2429	    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);  }
2430	
2431	  /** 原版消息列(Main.NewText 入口) */
2432	  private chatMonitor: ChatMonitor | null = null;
2433	  /** 消息缓冲:ChatMonitor 未建(initInGame 之前,如新世界 afterWorldLoad
2434	   *  发出的 NPC 入驻公告)时暂存,initInGame 创建后回放——曾直接丢弃 */
2435	  private chatPending: Array<[string, number, number, number, number]> = [];
2436	  chatMessage(text: string, r = 255, g = 255, b = 255, width = -1): void {
2437	    if (this.chatMonitor) this.chatMonitor.message(text, r, g, b, width);
2438	    else this.chatPending.push([text, r, g, b, width]);
2439	  }
2440	
2441	  // ---- NPC 对话系统(SetTalkNPC + GetChat;内容在 Game 生成,此处纯渲染) ----
2442	  private npcDialog: NpcDialog | null = null;
2443	  private npcShop: NpcShop | null = null;
2444	
2445	  showNpcDialog(name: string, chat: string, buttons: Array<{ id: NpcButtonId; label: string }>, portrait?: string | null): void {
2446	    if (!this.npcDialog) {
2447	      this.npcDialog = new NpcDialog(this.root, (id) => {
2448	        this.npcShop?.close();
2449	        this.npcShop = null;
2450	        this.game?.npcDialogButton(id);
2451	      });
2452	    }
2453	    this.npcDialog.open(name, chat, buttons, portrait);
2454	  }
2455	
2456	  closeNpcDialog(): void {
2457	    this.npcDialog?.close();
2458	    this.npcShop?.close();
2459	    this.npcShop = null;
2460	  }
2461	
2462	  showNpcShop(title: string, items: Array<{ key: string; vanillaId: number; name: string; price: number }>, copper: number): void {
2463	    if (!this.npcShop) {
2464	      this.npcShop = new NpcShop(this.root,
2465	        (vid) => this.game?.npcShopBuy(vid),
2466	        () => { this.npcShop?.close(); this.npcShop = null; });
2467	    }
2468	    // 图标由 UI 侧按原版 id 补(atlas 管线)
2469	    const entries: ShopEntry[] = items.map((it) => ({
2470	      ...it,
2471	      iconUrl: this.game ? iconUrl(this.game, it.vanillaId) || '' : '',
2472	    }));
2473	    this.npcShop.open(title, entries, copper);
2474	  }
2475	
2476	  /** M5：背包/快捷栏已 Canvas 化，DOM 仅保留 Buff 栏 + Toast */
2477	  initInGameLite() {
2478	    this.buildBuffBar();
2479	    const map: Array<[BuffType, string]> = [
2480	      [BuffType.Agility, 'agility_potion'], [BuffType.Ironskin, 'ironskin_potion'],
2481	      [BuffType.Resistance, 'heal_potion'], [BuffType.Thorns, 'thorns_potion'],
2482	      [BuffType.Regen, 'regen_potion'], [BuffType.Honey, 'honey_bucket'],
2483	      [BuffType.OnFire, 'torch'], [BuffType.Burning, 'meteorite'],
2484	      [BuffType.Bleeding, 'lesser_healing_potion'], [BuffType.Suffocation, 'sand_block'],
2485	      [BuffType.ObsidianSkin, 'obsidian_skin_potion'], [BuffType.Gills, 'gills_potion'],
2486	      [BuffType.ManaRegen, 'mana_regen_potion'], [BuffType.MagicPower, 'magic_power_potion'],
2487	      [BuffType.Featherfall, 'featherfall_potion'], [BuffType.WaterWalking, 'water_walking_potion'],
2488	      [BuffType.Archery, 'archery_potion'], [BuffType.NightOwl, 'night_owl_potion'],
2489	      // R1 数值批（vi_ 药水物品图标）
2490	      [BuffType.Battle, 'vi_300_BattlePotion'], [BuffType.Calming, 'vi_2324_CalmingPotion'],
2491	      [BuffType.Mining, 'vi_2322_MiningPotion'], [BuffType.Builder, 'vi_2325_BuilderPotion'],
2492	      [BuffType.Heartreach, 'vi_2323_HeartreachPotion'], [BuffType.FlipperPotion, 'vi_2327_FlipperPotion'],
2493	      [BuffType.Titan, 'vi_2326_TitanPotion'], [BuffType.AmmoReservation, 'vi_2344_AmmoReservationPotion'],
2494	      [BuffType.Lifeforce, 'vi_2345_LifeforcePotion'], [BuffType.Endurance, 'vi_2346_EndurancePotion'],
2495	      [BuffType.Wrath, 'vi_2349_WrathPotion'], [BuffType.Rage, 'vi_2347_RagePotion'],
2496	      [BuffType.Tipsy, 'vi_2266_Sake'],
2497	      // 后期批（近似图标：月噬→吸血鬼 knives / 遮挡→暗影钥匙）
2498	      [BuffType.MoonLeech, 'vi_1569_vampire_knives'], [BuffType.Obstructed, 'vi_329_shadow_key'],
2499	      // 食物三档（以已注册食物贴图为图标近似）
2500	      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],
2501	      [BuffType.WellFed3, 'vi_1919_sugar_cookie'],
2502	    ];
2503	    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);
2504	  }
2505	}
2506	

```


---

## 🤖 Assistant · 2026-08-12T09:24:25.085Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/UI.ts",
 "offset": 1755,
 "limit": 35
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:25.099Z

**📎 ToolResult**

```
1755	    if (!this.game || !this.buffBar) return;
1756	    const buffs = this.game.player.buffs;
1757	    const invOpen = this.invPanel.style.display === 'block';
1758	    this.buffBar.style.display = invOpen ? 'none' : 'flex';
1759	    for (const [t, ui] of this.buffBlocks) {
1760	      const left = buffs.active.get(t);
1761	      if (left === undefined) {
1762	        ui.block.style.display = 'none';
1763	        continue;
1764	      }
1765	      ui.block.style.display = 'flex';
1766	      ui.block.title = `${buffName(t)}：${buffDesc(t)}`;
1767	      const iconId = this.buffIconItem.get(t);
1768	      if (iconId && !ui.icon.src) ui.icon.src = iconUrl(this.game, iconId);
1769	      const s = Math.ceil(left);
1770	      ui.time.textContent = s >= 60
1771	        ? (s % 60
1772	          ? Lang.text('Mods.SandboxWorld.Time.MinSec', Math.floor(s / 60), s % 60)
1773	          : Lang.text('Mods.SandboxWorld.Time.Minutes', Math.floor(s / 60)))
1774	        : Lang.text('Mods.SandboxWorld.Time.Seconds', s);
1775	    }
1776	  }
1777	
1778	  // Buff → 显示用物品图标（药水图标即 Buff 图标）
1779	  buffIconItem = new Map<BuffType, number>();
1780	
1781	  private buildChestPanel() {
1782	    this.chestPanel = el('div', 'sw-panel');
1783	    this.chestPanel.style.cssText = 'position:fixed; left:50%; top:16%; transform:translateX(-50%); display:none;';
1784	    this.chestTitle = el('div', 'sw-title', Lang.text('Mods.SandboxWorld.UI.Chest'));
1785	    this.chestPanel.appendChild(this.chestTitle);
1786	    const grid = el('div');
1787	    grid.style.cssText = 'display:grid; grid-template-columns:repeat(10,52px); gap:5px;';
1788	    // 按 40 槽上限构建（玩家储物 bank×4）；打开时按容器实际长度显隐（宝箱 10 / 储物 40）
1789	    for (let i = 0; i < 40; i++) {

```


---

## 🤖 Assistant · 2026-08-12T09:24:25.747Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"player.fixedUpdate\\|\\.fixedUpdate(\" ~/Project/GLM/SandboxWorld/game/src -l; echo ---; grep -rn \"inputX =\" ~/Project/GLM/SandboxWorld/game/src | grep -v Player.ts | head",
 "description": "Find fixedUpdate caller and inputX writers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:25.821Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts
---
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2234:    player.inputX = (inp.down('KeyA') || inp.down('ArrowLeft') ? -1 : 0) + (inp.down('KeyD') || inp.down('ArrowRight') ? 1 : 0);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10099:      proxy.inputX = stale ? 0 : (rp.left ? -1 : 0) + (rp.right ? 1 : 0);

```


---

## 🤖 Assistant · 2026-08-12T09:24:25.927Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:25.936Z

**📎 ToolResult**

```
1	// 微光实体转化系统回归（WorldItem.GetShimmered / Player shimmer / NPC.GetShimmered）。
2	// 表来源 = tools/extract-shimmer.mjs（ItemID.cs/NPCID.cs Sets → vanilla-shimmer.json）。
3	// 探针断言：
4	//  1. 转化表提取完整性（312 物品对 / 114 NPC 对）+ 已知对抽查
5	//  2. GetShimmerEquivalentType 等价计数（幻影族 5358-5361 → 5437）
6	//  3. 钱币 → coinLuck 接通（LuckState.addCoinLuck 距离门 + 面额放大 + 衰减）
7	//  4. 掉落物入微光端到端：进度累积 → 转化换物品（原堆叠保留）+ 钱币消失入 luck
8	//  5. 玩家脱困落点搜索（findShimmerFreeSpot：微光内不放、最近空气落点优先）
9	import { describe, it, expect } from 'vitest';
10	import {
11	  canShimmerItem, coinLuckAmount, findShimmerFreeSpot,
12	  getShimmerEquivalentType, getTransformToItem,
13	  internalIdOfVanilla, isNpcTownShimmerable, npcShimmerTransformTo,
14	  npcShimmerTransformToItem, vanillaIdOfItem,
15	} from '../src/stats/Shimmer';
16	import { LuckState } from '../src/stats/Luck';
17	import { ItemDrop } from '../src/entities/ItemDrop';
18	import { Player } from '../src/entities/Player';
19	import { Inventory } from '../src/items/Inventory';
20	import { World } from '../src/world/World';
21	import { TILE } from '../src/core/constants';
22	import { ITEM_BY_KEY, VANILLA_ITEM_KEY_BY_ID } from '../src/data/items';
23	import type { GameHooks } from '../src/entities/types';
24	
25	describe('转化表提取（ItemID.cs / NPCID.cs Sets）', () => {
26	  it('物品对 312 条 + 抽查已知转化（含火炬 8 → 5353 双向链）', () => {
27	    expect(getTransformToItem(3460)).toBe(947);      // 夜明锭链头
28	    expect(getTransformToItem(947)).toBe(1106);
29	    expect(getTransformToItem(8)).toBe(5353);        // 火炬 → 骨炬
30	    expect(getTransformToItem(206)).toBe(207);       // 凝胶 ↔ 精炼凝胶族
31	    expect(getTransformToItem(3461)).toBe(0);        // 无月相参 → 动态分支不启用（表外）
32	    // 月相砖动态分支全 8 相位（ShimmerTransforms.cs:108-125;MoonPhase 枚举序 0-7）
33	    const LUNAR = [5408, 5401, 5403, 5402, 5406, 5407, 5405, 5404]; // Full/TQL/HL/QL/Empty/QR/HR/TQR
34	    for (let ph = 0; ph < 8; ph++) {
35	      expect(getTransformToItem(3461, ph)).toBe(LUNAR[ph]);
36	      // 转化目标物品必须已注册(★曾缺 5402/5406/5408 → 对应月相转化静默丢物)
37	      expect(internalIdOfVanilla(LUNAR[ph])).toBeGreaterThanOrEqual(0);
38	    }
39	    expect(canShimmerItem(3461, false, 3)).toBe(true); // 有月相 → 可微光化(无参时 false)
40	    expect(getTransformToItem(4837)).toBe(999);      // 绿宝石 → 金皇冠（源在键侧）
41	  });
42	
43	  it('等价计数（Item.cs:49073-49086）：幻影系 5358-5360 → 5437，普通物品恒等', () => {
44	    expect(getShimmerEquivalentType(5358)).toBe(5437);
45	    expect(getShimmerEquivalentType(5360)).toBe(5437);
46	    expect(getShimmerEquivalentType(5437)).toBe(5437);
47	    expect(getShimmerEquivalentType(8)).toBe(8);
48	    expect(getShimmerEquivalentType(5669, true)).toBe(4956); // forDecraft 专用表
49	  });
50	
51	  it('CanShimmer 子集：钱币/可转化物为真，无表物品为假，月后锁生效', () => {
52	    expect(canShimmerItem(71)).toBe(true);            // 铜币
53	    expect(canShimmerItem(8)).toBe(true);             // 火炬
54	    expect(canShimmerItem(75)).toBe(false);           // 坠落之星：无表不可转
55	    expect(canShimmerItem(1326, false)).toBe(false);  // ShimmerPostMoonlord 锁
56	    expect(canShimmerItem(1326, true)).toBe(true);
57	  });
58	
59	  it('NPC 表：114 对转化 + NPC→物品 + 城镇变体名单', () => {
60	    expect(npcShimmerTransformTo(3)).toBeGreaterThan(0);
61	    expect(npcShimmerTransformTo(132)).toBe(202);
62	    expect(npcShimmerTransformToItem(651)).toBe(182);  // 附魔日晷族 → 哥布林数据
63	    expect(npcShimmerTransformToItem(448)).toBe(5341); // 448 → 银河珍珠 5341
64	    expect(isNpcTownShimmerable(22)).toBe(true);       // 向导
65	    expect(isNpcTownShimmerable(17)).toBe(true);       // 商人
66	    expect(isNpcTownShimmerable(1)).toBe(false);       // 蓝史莱姆非城镇
67	  });
68	});
69	
70	describe('钱币 → 微光化币 → coinLuck（WorldItem.cs:1791-1810 + Player.cs:17943-17963）', () => {
71	  it('面额放大：银 ×100 / 金 ×10000 / 铂 stack 钳 1 后 ×1e6', () => {
72	    expect(coinLuckAmount(71, 50)).toBe(50);
73	    expect(coinLuckAmount(72, 3)).toBe(300);
74	    expect(coinLuckAmount(73, 2)).toBe(20000);
75	    expect(coinLuckAmount(74, 7)).toBe(1000000);
76	  });
77	
78	  it('AddCoinLuck 距离门 <1000px + 1e6 cap + ×0.9999 衰减', () => {
79	    const s = new LuckState();
80	    s.addCoinLuck(999, 500);
81	    expect(s.coinLuck).toBe(500);
82	    s.addCoinLuck(1000, 500);           // 恰 1000px 不计
83	    expect(s.coinLuck).toBe(500);
84	    s.addCoinLuck(0, 2_000_000);        // cap 1e6
85	    expect(s.coinLuck).toBe(1_000_000);
86	    expect(s.coinLuckValue).toBe(0.2);  // >249000 满档
87	    s.update(1);
88	    expect(s.coinLuck).toBeLessThan(1_000_000);
89	  });
90	});
91	
92	// ============ 掉落物端到端（TileStore 造微光池） ============
93	
94	const W = 60, H = 60;
95	
96	function shimmerWorld(): World {
97	  const w = new World(W, H, 11, 'shimmer-test');
98	  const st = w.store;
99	  for (let x = 10; x < 30; x++) {
100	    st.setTile(x, 40, 1);               // 池底
101	    for (let y = 33; y < 40; y++) st.setLiquid(x, y, 255, 4); // 微光满格
102	  }
103	  for (let x = 30; x < 46; x++) st.setTile(x, 40, 1); // 池外实地（脱困传送落点候选）
104	  w.lavaLine = 50;
105	  return w;
106	}
107	
108	function hooks(w: World, p: Player): GameHooks {
109	  return {
110	    world: w, player: p,
111	    enemies: () => [], critters: () => [],
112	    spawnDrop: () => null,
113	    damagePlayer: () => {},
114	    addDamageNumber: () => {}, cutTile: () => {},
115	    onEnemyKilled: () => {}, spawnEnemy: () => {},
116	    spawnParticles: () => {}, notifyInventoryChanged: () => {},
117	    playSfx: () => {}, playSfxFiles: () => {}, showPickupLabel: () => {},
118	  } as unknown as GameHooks;
119	}
120	
121	describe('掉落物入微光（WorldItem.Shimmering + GetShimmered）', () => {
122	  it('金币 73 入池 90t → 消失并按 ×10000 计入 coinLuck', () => {
123	    const w = shimmerWorld();
124	    const p = new Player(45 * TILE, 30 * TILE, new Inventory());
125	    const key = 'coin_gold';
126	    const d = new ItemDrop(20 * TILE, 35 * TILE, ITEM_BY_KEY[key], 2);
127	    expect(vanillaIdOfItem(d.itemId)).toBe(73);
128	    for (let i = 0; i < 200 && !d.dead; i++) d.fixedUpdate(1, hooks(w, p));
129	    expect(d.dead).toBe(true);
130	    expect(p.luckState.coinLuck).toBe(2 * 10000); // 20000 铜币面额
131	  });
132	
133	  it('火炬 8 入池 → 换成 5353 原堆叠保留并微光化上浮（shimmered）', () => {
134	    const w = shimmerWorld();
135	    const p = new Player(45 * TILE, 30 * TILE, new Inventory());
136	    const d = new ItemDrop(20 * TILE, 35 * TILE, ITEM_BY_KEY['torch'], 5);
137	    for (let i = 0; i < 300; i++) {
138	      d.fixedUpdate(1, hooks(w, p));
139	      if (d.shimmered) break;
140	    }
141	    expect(d.shimmered).toBe(true);
142	    expect(d.stack).toBe(5);
143	    expect(vanillaIdOfItem(d.itemId)).toBe(5353);
144	    expect(internalIdOfVanilla(5353)).toBeGreaterThan(0);
145	  });
146	
147	  it('不可转化物（坠落之星 75）入池不转化不消失', () => {
148	    const w = shimmerWorld();
149	    const p = new Player(45 * TILE, 30 * TILE, new Inventory());
150	    const d = new ItemDrop(20 * TILE, 35 * TILE, ITEM_BY_KEY[VANILLA_ITEM_KEY_BY_ID[75]], 1);
151	    for (let i = 0; i < 400; i++) d.fixedUpdate(1, hooks(w, p));
152	    expect(d.dead).toBe(false);
153	    expect(d.shimmered).toBe(false);
154	    expect(d.shimmerTime).toBe(0);
155	  });
156	});
157	
158	describe('玩家脱困落点（ShimmerHelper.FindSpotWithoutShimmer 近似）', () => {
159	  it('微光柱内不放人；池外最近的空气+实地落点被选中', () => {
160	    const w = shimmerWorld();
161	    const st = w.store;
162	    // 池心上方全是微光 → 不该选池内任何格
163	    const inPool = findShimmerFreeSpot(st, 20, 36);
164	    if (inPool) {
165	      const i = st.idx(inPool.x, inPool.y);
166	      expect(st.liquid[i] === 0 || st.liquidType[i] !== 4).toBe(true);
167	    }
168	    // 池外（x=35 无液体，y=39 上方三格空 + 下方实地 40 行石）→ 选脚下实地上一格
169	    for (let x = 31; x < 40; x++) st.setTile(x, 40, 1);
170	    const spot = findShimmerFreeSpot(st, 35, 39);
171	    expect(spot).not.toBeNull();
172	    expect(spot!.x).toBeGreaterThanOrEqual(31);
173	    expect(spot!.y).toBeLessThan(40);
174	  });
175	
176	  it('封闭洞穴兜底（Player.cs:28442-28469 三层兜底）：玩家周围 60 圈无落点 → 出生点兜底必脱困', () => {
177	    // 140×140 全实心世界：玩家腔在 (10,10)，出生点区在 (130,120)——切比雪夫距离 120 > 59，
178	    // 第一层搜索（r<60）必空；出生点上方净空+实地 → 兜底层命中
179	    const EW = 140, EH = 140;
180	    const w = new World(EW, EH, 11, 'shimmer-enclosed');
181	    const st = w.store;
182	    for (let x = 0; x < EW; x++) for (let y = 0; y < EH; y++) st.setTile(x, y, 1);
183	    // 封闭微光腔（玩家位 10,10；腔 3×3 微光 + 上方 3 格空气）
184	    for (let x = 9; x <= 11; x++) {
185	      st.setTile(x, 9, 0); st.setTile(x, 10, 0); st.setTile(x, 11, 0);
186	      st.setLiquid(x, 10, 255, 4); st.setLiquid(x, 11, 255, 4);
187	    }
188	    // 出生点区：上方净空（3 格）+ 实地
189	    for (let x = 127; x <= 133; x++) {
190	      st.setTile(x, 121, 1);
191	      st.setTile(x, 120, 0); st.setTile(x, 119, 0); st.setTile(x, 118, 0);
192	    }
193	    w.spawnX = 130; w.spawnY = 120;
194	    w.lavaLine = 125;
195	    // 玩家层（无兜底参数）→ 旧实现在这里返回 null = 每 20s 重试永远失败 = 永久卡死
196	    expect(findShimmerFreeSpot(st, 10, 10)).toBeNull();
197	    // 三层兜底：出生点周围必命中
198	    const spot = findShimmerFreeSpot(st, 10, 10, w.spawnX, w.spawnY);
199	    expect(spot).not.toBeNull();
200	    expect(Math.abs(spot!.x - 130)).toBeLessThan(60);
201	    expect(st.liquid[st.idx(spot!.x, spot!.y)] === 0 || st.liquidType[st.idx(spot!.x, spot!.y)] !== 4).toBe(true);
202	  });
203	});
204	
205	describe('玩家浸微光（buff 353 + 脱困传送，Player.cs:27420/11381/28377）', () => {
206	  it('入微光：shimmering 置位 + 受击免疫 + timeShimmering 累积；脱困传送落点无微光', () => {
207	    const w = shimmerWorld();
208	    const p = new Player(20 * TILE, 36 * TILE, new Inventory());
209	    const h = hooks(w, p);
210	    p.fixedUpdate(1 / 60, h);
211	    expect(p.inShimmer).toBe(true);
212	    expect(p.shimmering).toBe(true);          // y=36 < lavaLine 50 → buff 353 生效
213	    expect(p.timeShimmering).toBe(1);
214	    expect(p.damage(9999, p.cx, p.cy)).toBe(false); // Hurt :37591-37595 直接 0
215	    // 强制走脱困（≥1200 且有输入）：传送到池外无微光落点
216	    p.timeShimmering = 1200;
217	    p.inputX = 1;
218	    p.fixedUpdate(1 / 60, h);
219	    const st = w.store;
220	    const i = st.idx(Math.floor(p.cx / TILE), Math.floor((p.y + p.h - 4) / TILE));
221	    expect(st.liquid[i] === 0 || st.liquidType[i] !== 4).toBe(true); // 落点不在微光里
222	    expect(p.shimmering).toBe(false);
223	    expect(p.timeShimmering).toBe(0);
224	  });
225	
226	  it('地狱层内微光不生效（:11391-11397 position.Y/16 > UnderworldLayer → DelBuff）', () => {
227	    const w = shimmerWorld();
228	    w.lavaLine = 30;                          // 玩家 y=36 已入地狱层
229	    const p = new Player(20 * TILE, 36 * TILE, new Inventory());
230	    p.fixedUpdate(1 / 60, hooks(w, p));
231	    expect(p.inShimmer).toBe(true);
232	    expect(p.shimmering).toBe(false);
233	  });
234	});
235	

```


---

## 🤖 Assistant · 2026-08-12T09:24:41.695Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the full picture:

1. **Player movement**: `const ix = this.inputX;` at :860 — shimmering input zeroing at :925 is too late. Fix: extend the Frozen zeroing block at :850 (before horizontal movement) to include `this.shimmering`. Note shimmering is computed at :712, before :850 — so safe.

Wait, but there's one more thing: after input zeroing at :850, `this.inputX = 0` — but the shimmering physics branch at :925 re-zeroes (harmless). Also :1192 松键截断 uses inputJump (false). And moveAndCollide :1272 still runs with vx — friction will have been applied at :874 since ix===0. Good.

Also `ridingCart` return at :854 is AFTER :850 zeroing, so shimmering input lock applies on cart too (vanilla-like). Good — the cart branch doesn't bypass.

2. **Buff icon**: UI.ts has TWO identical map arrays (one in a method ending at :2429, one in initInGameLite at :2479-2503). Neither has Shimmered. Add `[BuffType.Shimmered, 'vi_5340_galaxy_pearl']` to both. Check that 'vi_5340_galaxy_pearl' key exists in ITEM_BY_KEY. Galaxy pearl is item 5340. Also note test file uses 448 → 银河珍珠 5341 comment... The prompt says use 'vi_5340_galaxy_pearl'. Let me verify the key exists.

Also verify buff bar displays: it iterates this.buffBlocks — need to check that buffBlocks includes Shimmered (buildBuffBar probably iterates all BuffType). Let me check buildBuffBar.

3. **Enemy shimmer**: chain at :655-662 is intact and gated on `vanillaId !== null && !boss`, uses liquidCollision box with type 4, shimmerT>90 → npcGetShimmered. Need to verify npcGetShimmered exists (:1399-1420) — yes. And check Enemy avoids... hmm the user says "怪物也能进湖" — per vanilla that's expected physically; the issue is they should transform after 90t. Chain alive. But wait — one potential problem: does Enemy AI have pathing that avoids liquid? Enemy may not fall into the pool if... whatever. The user's complaint may just be a misunderstanding; per vanilla NPCs walk into shimmer and get transformed. But let me double-check the shimmer transformation actually triggers: `this.shimmerT += 1` per fixedUpdate tick with dt... fixedUpdate(1/60) called 60/s, so 90t = 1.5s. Fine.

But hold on — is there maybe a check in npcGetShimmered requiring `def.shimmerable` or a table entry that returns for most NPCs? Let me read Enemy :1395-1430. If NPC not in transform table, vanilla: GetShimmered still happens (NPCs not transformable just... actually in vanilla, NPCs in shimmer that can't transform just sink/fade? No — vanilla NPC.GetShimmered: if the NPC has a shimmer transform, it transforms; town NPCs transform to variant; others... Let me recall: NPC.shimmerTransparency > 0.9 → GetShimmered. In GetShimmered, NPCID.Sets.ShimmerTransformToNPC / TransformToItem; if neither, it does nothing? Actually for critters/enemies without entry, they just stay. Hmm. Let me read the local implementation to check behavior for table-less NPCs.

4. Tests: add probe tests to tests/shimmer.test.ts:
   - Player in shimmer pool with inputX=1: after fixedUpdate, inputX===0, buffs contain Shimmered, and x displacement == 0 (or vx decays and x unchanged after a few ticks... first tick: inputX zeroed before movement → friction applied → vx stays 0 if starting at 0 → x unchanged). Assert p.inputX === 0 and p.x unchanged and buffs.has Shimmered.
   - Enemy submerged 90t → transformed.

For the enemy test I need an Enemy instance. Let me check Enemy constructor signature. Let me read Enemy.ts around :1390-1430 and constructor, plus buildBuffBar in UI.ts.

Let me also verify BuffState.apply stores seconds (apply(BuffType.Shimmered, 1) → 1 second?) — Buffs apply semantics: active stores seconds; Honey applied 30 = 30s. Yes, seconds.

Also check `buffs.has(BuffType.Shimmered)` display — buffBlocks built from what? Check buildBuffBar.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:24:42.236Z · glm-x-preview-260804

```
三处根因基本锁定。现在核对 UI buildBuffBar 覆盖范围、`vi_5340_galaxy_pearl` 键存在性、Enemy npcGetShimmered 实现与构造签名。
```


---

## 🤖 Assistant · 2026-08-12T09:24:42.831Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"buildBuffBar\" ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts | head -3; echo ---; grep -n \"galaxy_pearl\" ~/Project/GLM/SandboxWorld/game/src/data/items.ts | head -5",
 "description": "Check buildBuffBar and galaxy pearl item key"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:42.889Z

**📎 ToolResult**

```
1712:  private buildBuffBar() {
2401:    this.buildBuffBar();
2478:    this.buildBuffBar();
---
498:item({ key: 'vi_5340_galaxy_pearl', name: '', maxStack: 999, value: 1 });

```


---

## 🤖 Assistant · 2026-08-12T09:24:43.088Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 45,
 "offset": 1390
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:43.097Z

**📎 ToolResult**

```
1390	  }
1391	
1392	  /** 外部 AI 文件的 Transform 入口（骑手 390 失坐骑 → 382,cs:36291） */
1393	  transformTo(id: number, st: GameHooks['world']['store']): boolean {
1394	    return this.tryTransformTo(id, st);
1395	  }
1396	
1397	  /** NPC.GetShimmered（NPC.cs:92502-92584）子集：雕像产怪直接消散（:92504-92519）→
1398	   *  ShimmerTransformToNPC 则 Transform（:92521-92533）→ ShimmerTransformToItem 则
1399	   *  掉微光化物品后消散（:92535-92560）。表来自 tools/extract-shimmer.mjs
1400	   *  （114 NPC 对 + 15 NPC→物品）。Boss 豁免（VANILLA_BOSS_IDS 外的 mini 部件走
1401	   *  上层表语义）；城镇变体分支（:92560-92573）在 TownNPC 侧实现 */
1402	  private npcGetShimmered(game: GameHooks): void {
1403	    if (this.vanillaId === null) return;
1404	    this.shimmerT = 0;
1405	    game.spawnParticles(this.cx, this.cy, '#BFE8FF', 10, 1.4, { life: 30, grav: -0.04 });
1406	    if (this.spawnedFromStatue) {           // SpawnedFromStatue → active=false（:92508-92514）
1407	      this.dead = true;
1408	      return;
1409	    }
1410	    const toNpc = npcShimmerTransformTo(this.vanillaId);
1411	    if (toNpc >= 0 && toNpc !== this.vanillaId) {
1412	      this.transformTo(toNpc, game.world.store);
1413	      return;
1414	    }
1415	    const toItem = npcShimmerTransformToItem(this.vanillaId);
1416	    if (toItem >= 0) {
1417	      const key = VANILLA_ITEM_KEY_BY_ID[toItem];
1418	      if (key) {
1419	        const d = game.spawnDrop(this.cx, this.cy, key, 1);
1420	        if (d) { d.shimmered = true; d.shimmerTime = 1; }  // 微光化物品上浮（:92540-92545）
1421	      }
1422	      this.dead = true;                    // noSpawnCycle + active=false（:92557-92559）
1423	    }
1424	  }
1425	
1426	  /** AI_040 爬墙蜘蛛族 1:1（NPC.cs:29784-30022）：无重力、贴背景墙表面爬行。
1427	   *  速度表：165 默认 2/0.08、237 3/0.12、531 4/0.16（:29789-29798）；
1428	   *  有视线 → 分轴伺服追玩家（:29880-29920，朝向角 atan2(期望速度)）；
1429	   *  无视线 → ai[0] ±200 振荡漂移（:29833-29878，角 atan2(当前速度)）；
1430	   *  531 朝向角额外 +π/2（:29922）；spriteDirection 恒 -1（:29829，渲染层处理）；
1431	   *  碰撞反弹（:29924-29950）：旧速 ×-0.5，X 朝移动方向保底 ±2、Y 保底 ±2；
1432	   *  专家模式毒液弹（:29960-29989，type 472）未启用专家模式，不移植；
1433	   *  脱墙（NPCCanStickToWalls 假）→ Transform 回地面形态（:29991-30010） */
1434	  private wallCreeperAI(game: GameHooks, player: Player | null) {

```


---

## 🤖 Assistant · 2026-08-12T09:24:43.688Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"constructor\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -3; echo ---; grep -rn \"new Enemy(\" ~/Project/GLM/SandboxWorld/game/tests/*.ts | head -5",
 "description": "Find Enemy constructor signature and test usage"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:43.749Z

**📎 ToolResult**

```
407:  constructor(public key: string, x: number, y: number) {
---
~/Project/GLM/SandboxWorld/game/tests/buff-r2-imbue.test.ts:39:    const e = new Enemy('zombie', 10 * 16, 10 * 16);
~/Project/GLM/SandboxWorld/game/tests/buff-r2-imbue.test.ts:57:    const e = new Enemy('zombie', 10 * 16, 10 * 16);
~/Project/GLM/SandboxWorld/game/tests/projectile-reflect.test.ts:42:  const e = new Enemy('zombie', 20 * 16, 10 * 16 - 8);

```


---

## 🤖 Assistant · 2026-08-12T09:24:46.839Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Enemy constructor: `new Enemy(key, x, y)`. And vanillaId presumably set from def. Enemy shimmer chain alive.

Note npcGetShimmered: for NPCs with neither transformTo NPC nor item (e.g. zombie? zombie is 3 → npcShimmerTransformTo(3) > 0 per test). Zombie 3 transforms (test says npcShimmerTransformTo(3)).toBeGreaterThan(0). So enemies in the pool transform after 90t. Chain alive — the user's observation "monsters can also enter the lake" matches vanilla (they physically enter), they should transform in 1.5s. I'll verify with probe test.

Now check buildBuffBar at :1712 to see which buff types get blocks.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:24:47.079Z · glm-x-preview-260804

```
看 buildBuffBar 如何枚举 buff 类型（决定 Shimmered 图标会不会显示）。
```


---

## 🤖 Assistant · 2026-08-12T09:24:47.277Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/UI.ts",
 "limit": 45,
 "offset": 1712
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:47.286Z

**📎 ToolResult**

```
1712	  private buildBuffBar() {
1713	    this.buffBar = el('div');
1714	    // 32 + 10×38 宽容纳 11 个/行（wrap = 原版 num2=11 行卷绕，行距 50-32=18）
1715	    this.buffBar.style.cssText = 'pointer-events:auto; position:fixed; top:76px; left:32px; display:flex; flex-wrap:wrap; width:412px; column-gap:6px; row-gap:18px;';
1716	    this.root.appendChild(this.buffBar);
1717	    this.buffBlocks.clear();
1718	    for (const t of [BuffType.Agility, BuffType.Ironskin, BuffType.Resistance, BuffType.Thorns, BuffType.Regen, BuffType.Honey,
1719	      BuffType.OnFire, BuffType.Burning, BuffType.Bleeding, BuffType.Suffocation,
1720	      BuffType.ObsidianSkin, BuffType.Gills, BuffType.ManaRegen, BuffType.MagicPower,
1721	      BuffType.Featherfall, BuffType.WaterWalking, BuffType.Archery, BuffType.NightOwl]) {
1722	      const block = el('div', 'sw-buff');
1723	      block.style.display = 'none';
1724	      block.style.cssText += 'width:32px; height:32px; background:none; border:none; border-radius:0; cursor:pointer;';
1725	      const icon = el('img') as HTMLImageElement;
1726	      icon.draggable = false;
1727	      icon.style.cssText = 'width:32px; height:32px; image-rendering:pixelated; display:block;';
1728	      block.appendChild(icon);
1729	      const time = el('span', '', '');
1730	      time.style.cssText = 'position:absolute; left:-4px; right:-4px; top:34px; text-align:center; font-size:11px; font-weight:bold; color:#fff; text-shadow:1px 1px 0 #000; white-space:nowrap;';
1731	      block.appendChild(time);
1732	      // 悬停高亮（原版 buffAlpha 悬停 +0.1/t 至 1、离开 -0.05/t 至 0.4——CSS 渐变近似）
1733	      block.addEventListener('mouseenter', () => { icon.style.filter = 'brightness(1.35)'; });
1734	      block.addEventListener('mouseleave', () => { icon.style.filter = ''; });
1735	      // 右键取消（TryRemovingBuff L42793+：非 debuff → DelBuff + SoundID 12）
1736	      block.addEventListener('contextmenu', (e) => {
1737	        e.preventDefault();
1738	        if (!this.game) return;
1739	        this.game.player.buffs.remove(t);
1740	        this.game.sfx.play('menuTick');
1741	        this.refreshBuffs();
1742	      });
1743	      this.buffBar.appendChild(block);
1744	      this.buffBlocks.set(t, { block, icon, time });
1745	    }
1746	  }
1747	
1748	  buffBar: HTMLElement | null = null;
1749	  buffBlocks = new Map<BuffType, { block: HTMLElement; icon: HTMLImageElement; time: HTMLElement }>();
1750	
1751	  /** 每秒左右调用一次（由 Game 经 callbacks 驱动）。
1752	   *  原版行为（Main.cs:42622）：背包/华美 UI 打开时整栏不画；时长文字用
1753	   *  LocalizedDuration 缩写格式（zh-Hans "30秒"/"2分30秒"），仅剩 >2 tick 时显示 */
1754	  refreshBuffs() {
1755	    if (!this.game || !this.buffBar) return;
1756	    const buffs = this.game.player.buffs;

```


---

## 🤖 Assistant · 2026-08-12T09:24:54.858Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Critical finding: buildBuffBar has a HARDCODED list of 18 BuffTypes and Shimmered is NOT in it. buffBlocks only contains those 18. So even if the icon map had Shimmered, no block would exist → no icon shown. This is the real reason for "左上角无 debuff 图标" (besides the missing icon map).

Wait — but there are two buildBuffBar call sites (:2401 and :2478, in two init paths). Both call this same private buildBuffBar(). So the fix is: add BuffType.Shimmered to the list in buildBuffBar (:1718-1721) AND add the icon mapping to BOTH map arrays (:2420-2428 and :2490-2501).

Hmm wait, but there are other buffs applied that aren't in the list either (WellFed, Titan, etc. are in the icon maps but not in buffBlocks?). The buffBlocks list is only 18 entries while icon maps have ~30. That's inconsistent in the existing code — maybe a known gap. But our task: make Shimmered show. So add Shimmered to buffBlocks list too.

Actually wait — let me double check: does buildBuffBar really only include those? Yes, hardcoded 18. And refreshBuffs iterates buffBlocks. So buffs not in buffBlocks never display (e.g. Battle, Calming, Tipsy, WellFed — those icons were added to the maps but would never render!). That seems like a pre-existing gap... Hmm, but the maps have entries for Battle/Tipsy etc. which are useless without buffBlocks entries. Unless there's a second UI (vui Canvas framework) that renders buffs separately. The memory notes mention vui/ Canvas framework for UI. But buffIconItem is DOM-side.

Let me check whether there's a vui buff display that uses buffIconItem or its own mapping. Search for Shimmered in vui directory. Earlier grep for "Shimmered" across src returned only... my grep `grep -rn "Shimmered\|galaxy_pearl" ... -l` failed due to zsh `==` issue. Let me redo: find all files with "Shimmered".

Let me search properly.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:24:55.783Z · glm-x-preview-260804

```
发现更深问题：buildBuffBar 的 buffBlocks 是**硬编码 18 项白名单**（:1718-1721），Shimmered 不在其中——即使图标 map 补了也不会显示。先确认 Shimmered 在全仓的所有引用面和 vui 侧是否有独立 buff 栏。
```


---

## 🤖 Assistant · 2026-08-12T09:24:56.148Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"Shimmered\" ~/Project/GLM/SandboxWorld/game/src | grep -v \"\\.js:\"",
 "description": "List all Shimmered references in src"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:56.186Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/stats/Shimmer.ts:2://   - 物品转化 WorldItem.GetShimmered（WorldItem.cs:1781-1931）：
~/Project/GLM/SandboxWorld/game/src/stats/Shimmer.ts:3://       入微光 → Shimmering()(:806-840) shimmerTime +0.01/t，>0.9 → GetShimmered
~/Project/GLM/SandboxWorld/game/src/stats/Shimmer.ts:19://       shimmerTransparency +0.01/t（:92468-92483）>0.9 → GetShimmered(:92502-92584)：
~/Project/GLM/SandboxWorld/game/src/stats/Shimmer.ts:31://     - 联机同步（NetMessage 145/146 ShimmeredItem/ShimmerEffect）
~/Project/GLM/SandboxWorld/game/src/stats/Shimmer.ts:134:// ============ NPC 侧（NPC.GetShimmered，NPC.cs:92502-92584） ============
~/Project/GLM/SandboxWorld/game/src/entities/Player.ts:716:    if (this.shimmering) this.buffs.apply(BuffType.Shimmered, 1);
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:114:  Shimmered = 77,   // 微光化(353,浸微光每 tick 刷新)：frozen 封输入+免伤+慢沉——
~/Project/GLM/SandboxWorld/game/src/stats/Buffs.ts:176:  [BuffType.Shimmered]: { vanillaBuff: 353, descKey: 'Mods.SandboxWorld.Buff.Shimmered.Desc', fallbackName: '微光化' },
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:321:   *  90t 到 0.9 阈值触发 NPC.GetShimmered；离池 -0.01/t） */
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:653:    // shimmerTransparency +0.01/t（:92468-92483）>0.9 → GetShimmered。离池衰减
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:658:        if (this.shimmerT > 90) this.npcGetShimmered(game);
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1397:  /** NPC.GetShimmered（NPC.cs:92502-92584）子集：雕像产怪直接消散（:92504-92519）→
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1402:  private npcGetShimmered(game: GameHooks): void {
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts:28:  /** 微光浸入进度 0-1（:27/:806-840 +0.01/t，>0.9 触发 GetShimmered；离池衰减） */
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts:150:   *  >0.9 触发 GetShimmered；不在微光中则进度衰减。转化触发在本地玩家侧语义
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts:164:        this.getShimmered(game);
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts:171:  /** WorldItem.GetShimmered（:1781-1931）本仓子集：钱币 → coinLuck（Luck.ts 数值位
~/Project/GLM/SandboxWorld/game/src/entities/ItemDrop.ts:174:  private getShimmered(game: GameHooks): void {
~/Project/GLM/SandboxWorld/game/src/entities/TownNPC.ts:95:    // 微光化城镇变体（NPC.GetShimmered :92560-92573：ShimmerTownTransform → ai[0]=25

```


---

## 🤖 Assistant · 2026-08-12T09:24:57.150Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"buffIconItem\\|buffBlocks\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v \"UI.ts\"; echo \"---vui buff---\"; grep -rln \"buff\" ~/Project/GLM/SandboxWorld/game/src/vui 2>/dev/null | head",
 "description": "Check other consumers of buff icon map and vui buff UI"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:24:57.212Z

**📎 ToolResult**

```
---vui buff---

```


---

## 🤖 Assistant · 2026-08-12T09:25:21.481Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Interesting — the grep for "Shimmered" in UI.ts shows nothing. And buffIconItem/buffBlocks have no other consumers. vui has no buff UI. So the DOM buff bar is the only buff display.

Note: Player.ts:716 line number shifted slightly (my earlier read said 714, now 716 — the file may have been modified by the parallel session? Or my read offset. Anyway.)

Also note: Buffs.ts:114 and :176 exist — buff name/desc registered. So `buffName(t)`/`buffDesc(t)` work for Shimmered. Good.

So fixes:

**Fix 1 (Player.ts)** — input zeroing order. Move shimmering input lock before horizontal movement. The Frozen block at :850 (line numbers from my read: 850) is the right place. Current:

```ts
    if (this.buffs.has(BuffType.Frozen)) { this.inputX = 0; this.inputJump = false; this.inputUp = false; this.inputDown = false; }
```

Change to include shimmering:

```ts
    if (this.buffs.has(BuffType.Frozen) || this.shimmering) { ... }
```

But wait — there's a subtlety with `shimmerUnstuck` teleport (lines ~719-724) which checks `anyInput` using inputX etc. That runs at :719-724, BEFORE :850 — that's fine, it uses the raw inputs (vanilla checks controlUp etc. too, pre-movement... in vanilla, TryToShimmerUnstuck is called in Update after input processing; fine).

Also — the teleport at :719-724 happens each tick when timeShimmering >= 1200 && anyInput. But inputX zeroing now happens at :850 — the anyInput check at :720 still sees raw input (set by Game at :2234 before fixedUpdate? Need to verify order: Game sets player.inputX at :2234, then calls fixedUpdate? Let me check the order in Game.ts around 2234.)

Actually important: if Game sets input AFTER fixedUpdate (i.e., reads input state for next frame), zeroing in fixedUpdate is durable within the frame. If Game sets input BEFORE fixedUpdate, then zeroing inside fixedUpdate at :850 works for that tick's movement. Either way, moving the zero earlier in fixedUpdate fixes the walk issue.

But one more: does Game do item use / other consumption of inputX after fixedUpdate? Not our concern.

**Fix 2 (Player.ts)** — keep the else-if chain branch but it now only does physics (vy). Keep input zeroing there too? It's harmless; but the comment should be updated. Actually simpler: remove the redundant zeroing in the shimmering branch and rely on the early one. But leaving it doesn't hurt (idempotent). I'll leave the zeroing but update the early block comment to note shimmering is included (frozen 封输入 semantics :11381-11388).

Wait — also check the `inShimmer && !shimmering` buoyancy branch (轻浮): it's in the else-if chain AFTER rope. Player in shimmer non-shimmering state (e.g. underworld or >lavaLine) — fine, unchanged.

**Fix 3 (UI.ts)** — add Shimmered to buffBlocks list in buildBuffBar + add icon mapping `[BuffType.Shimmered, 'vi_5340_galaxy_pearl']` to both map arrays. Note galaxy pearl item 5340 exists in items.ts :498.

Wait — should I also add the other missing buffs (Battle, Calming, etc.) to buffBlocks? The task scope is shimmer. Don't gold-plate. But hmm — the icon maps at :2420-2428 include Battle/Tipsy/WellFed etc. that never display... that's a pre-existing gap beyond scope. Only add Shimmered.

Now — is buff 353 a debuff that can't be right-click-removed? The contextmenu handler removes any buff. Vanilla Shimmered can't be cancelled. Minor; but right-clicking while shimmering does buffs.remove — it'd be re-applied next tick anyway (apply every tick while shimmering). Fine.

**Fix 4 (tests)** — add probe tests to tests/shimmer.test.ts:
- Player in pool with input: inputX zeroed, vx stays 0, x unchanged, buffs.has(Shimmered).
- Need several ticks: after 1 tick inputX===0? Careful: p.inputX = 1 set before fixedUpdate. In fixedUpdate: detection sets shimmering=true at :716 area, then at :850 (with fix) zeroing happens → inputX=0. Then ix=0 → friction, vx=0 → x unchanged. assert p.inputX === 0, p.x === initial, buffs.has(BuffType.Shimmered) true.
- Also test walking is blocked over multiple ticks: set inputX=1 each tick (as Game would), assert x stays constant.
- Enemy: new Enemy('zombie', ...) placed in pool; run fixedUpdate ~200 ticks; expect dead or transformed (vanillaId changed to 202? zombie 3 → npcShimmerTransformTo(3) = ? test says >0. Actually from test: npcShimmerTransformTo(132)).toBe(202). For zombie (3): transforms to something. I'll assert `e.dead || e.vanillaId changed from initial`.

Need Enemy hooks — Enemy.fixedUpdate(game, dt?) signature? Let me check Enemy.fixedUpdate signature. And vanillaId property. Let me check quickly.

Also need to check BuffState import for test: buffs.has(BuffType.Shimmered) — import BuffType from src/stats/Buffs.

Also check enemy spawnDrop hook: hooks() in test returns spawnDrop: () => null — for zombie → toItem? Zombie 3 → ShimmerTransformToNPC? Let me check vanilla: Zombie shimmer → ? In vanilla 1.4.4, NPCID.Sets.ShimmerTransformToNPC... zombie probably transforms into... hmm. Actually test file asserts npcShimmerTransformTo(3) > 0. If it's a NPC transform, transformTo() is called → tryTransformTo(id, st) — no spawnDrop needed. If toItem, spawnDrop returns null but d.shimmered line is guarded (`if (d)`), then dead=true. Either way dead or vanillaId changed. I'll assert `(e.dead || e.vanillaId !== original)`.

Let me check Enemy.fixedUpdate signature and vanillaId field, and how tests call it (buff-r2-imbue.test.ts).
````

</details>


---

## 🤖 Assistant · 2026-08-12T09:25:22.406Z · glm-x-preview-260804

```
UI 侧确认：`buffIconItem`/`buffBlocks` 无其他消费者，DOM buff 栏是唯一显示路径，而其白名单不含 Shimmered——图标缺失是双重原因（白名单 + 两处 icon map 都没条目）。再看 Enemy.fixedUpdate 签名和 Game 输入写入时序，然后动手修。
```


---

## 🤖 Assistant · 2026-08-12T09:25:23.311Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"fixedUpdate\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -3; echo ---; sed -n '35,60p' ~/Project/GLM/SandboxWorld/game/tests/buff-r2-imbue.test.ts; echo ---; grep -n \"vanillaId\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -5",
 "description": "Check Enemy fixedUpdate signature and test usage pattern"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:25:23.393Z

**📎 ToolResult**

```
143:  // （fixedUpdate 头部早退分支内单独调用）——傀儡只有快照推进但拖尾同样需要历史。
151:  /** fixedUpdate 尾部推入当前快照（位置=左上角，旋转=visAngle≈npc.rotation） */
281:    // 钳到 254 并置 alphaFade,由 fixedUpdate 逐 tick 减回 0（原版 AI_006 渐显）
---

describe('R2 敌 debuff DoT（NPC.cs:92585/92697/92708，lifeRegen/2=HP/s）', () => {
  it('毒 6HP/s / 毒液 30HP/s / 诅咒焰 24HP/s 滴血', () => {
    const { hooks } = makeHooks();
    const e = new Enemy('zombie', 10 * 16, 10 * 16);
    e.iframes = 0; e.hp = 1000; e.hpBarT = 0;
    // 毒 1 秒（world 挂在 hooks.world.store 形态与运行时一致）
    e.poisonT = 1;
    e.fixedUpdate(1, hooks as never);
    expect(e.hp).toBe(1000 - 6);
    // 毒液 1 秒
    e.hp = 1000; e.venomT = 1;
    e.fixedUpdate(1, hooks as never);
    expect(e.hp).toBe(1000 - 30);
    // 诅咒焰 1 秒
    e.hp = 1000; e.cursedT = 1;
    e.fixedUpdate(1, hooks as never);
    expect(e.hp).toBe(1000 - 24);
  });

  it('ichor：armorPenetration +15 折半 = +7 直伤（NPC.cs:81913-81938）', () => {
    const { hooks } = makeHooks();
    const e = new Enemy('zombie', 10 * 16, 10 * 16);
    e.hp = 1000; e.iframes = 0;
    const def = e.def.defense ?? 0;
    const noIchor = Math.max(1, Math.round(100 - def * 0.5));
---
2:// + 原版 NPC 数据驱动路径（vanillaId）：属性/AI/音效/贴图来自 vanilla-npcs.json（SetDefaults 提取）
114:  vanillaId: number | null = null;
193:      const s = this.vanillaId === 375 ? -1 : 1;
231:    const bodyId = head.vanillaId! + 1, tailId = head.vanillaId! + 2;
251:    e.vanillaId = id;

```


---

## 🤖 Assistant · 2026-08-12T09:25:23.543Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '2225,2245p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Check Game input write order around line 2234"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:25:23.598Z

**📎 ToolResult**

```
      } else if (this.world.store.inBounds(tx, ty)) {
        const existed = this.marks.some((m) => m.x === tx && m.y === ty);
        this.marks = this.marks.filter((m) => m.x !== tx || m.y !== ty); // 同格重复点 = 取消
        if (!existed) this.marks.push({ x: tx, y: ty });
        this.cb.onToast(existed ? `已取消标记 (${tx}, ${ty})` : `已标记 (${tx}, ${ty})，再次点击取消`);
        (window as unknown as { __swUI?: { updateAnnotateCount: (n: number) => void } }).__swUI?.updateAnnotateCount(this.marks.length);
      }
    }
    if (!inp.mouseDown) this._annoLatch = false;
    player.inputX = (inp.down('KeyA') || inp.down('ArrowLeft') ? -1 : 0) + (inp.down('KeyD') || inp.down('ArrowRight') ? 1 : 0);
    player.inputJump = inp.down('Space') || inp.down('KeyW') || inp.down('ArrowUp');
    player.inputDown = inp.down('KeyS') || inp.down('ArrowDown');
    player.inputUp = inp.down('KeyW') || inp.down('ArrowUp');
    // 重力药水（buff 18，:9720）：Up 边沿切换 gravDir（按住不连切）
    if (player.buffs.has(BuffType.Gravitation) && player.inputUp && !this.gravLatch) {
      player.gravDir = player.gravDir === 1 ? -1 : 1;
      this.gravLatch = true;
    }
    if (!player.inputUp) this.gravLatch = false;

    // 滚轮：全屏地图打开时缩放地图，否则缩放游戏画面

```


---

## 🤖 Assistant · 2026-08-12T09:26:04.888Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Game writes input at :2234 (input handling), and player.fixedUpdate is called separately in the fixed update loop. Order within a frame: presumably handleInput (writes inputX) then fixed step (fixedUpdate). Either way, zeroing early in fixedUpdate is correct.

Note: Game writes inputX every render/handle-input frame; fixedUpdate may run 0..n times per frame. Zeroing inside fixedUpdate means the zeroing lasts only within fixedUpdate — movement consumed there. With the fix, movement won't see input. 

Enemy.fixedUpdate(1, hooks) — dt=1 (seconds!). Note in buff test they call e.fixedUpdate(1, ...) for 1 second. And Enemy shimmer increments shimmerT by 1 per fixedUpdate call regardless of dt (`this.shimmerT += 1`). So 90 calls needed.

Wait — but does that mean in real gameplay, shimmerT increments per fixed tick (60/s), so 90t = 1.5s. Matches vanilla.

Now, does Enemy 'zombie' have vanillaId set? Enemy constructor: `constructor(public key: string, x, y)` — vanillaId presumably set in constructor from def. The shimmer gate requires `this.vanillaId !== null && !this.def.boss`. Zombie should be vanilla id 3.

But careful: does Enemy.fixedUpdate early-return somewhere before the shimmer section (:655)? The zombie AI runs; there might be gravity/movement that makes the zombie sink/fall. In test, pool at y 33-40, x 10-30. Place enemy at (20*TILE, 34*TILE). It'll bob around; liquidCollision box type 4 → true → shimmerT accumulates. After 91 ticks → npcGetShimmered → zombie 3 → npcShimmerTransformTo(3) = ? If >=0 → transformTo → tryTransformTo(3's target, st). tryTransformTo needs game.world.store — hooks has world. OK. Might set e.vanillaId to new id and possibly dead? Let's just assert dead || vanillaId !== 3. Need to know zombie's shimmer target... Actually test asserts `npcShimmerTransformTo(3)).toBeGreaterThan(0)` so a target exists.

Hmm, but wait: tryTransformTo may create a NEW Enemy and kill this one, or mutate in place? Either way dead===true likely. I'll assert `e.dead || e.vanillaId !== 3`.

Also for the Enemy test, hooks must provide what zombie AI needs — the shimmer.test.ts hooks() provides a minimal set. buff-r2 test has its own makeHooks. The shimmer hooks lacks things like spawnEnemy... it has spawnEnemy: () => {}. If zombie AI calls other hook methods missing from the object → runtime error (undefined is not a function). Risk: transformTo might call game.spawnEnemy or similar. tryTransformTo signature (id, st) — only store. Inside tryTransformTo, it might call this.game hooks? It takes st only. Probably fine. But zombie AI might call game.spawnParticles (provided), game.playSfx (provided), game.player (provided = p). Could call `game.enemies()` (provided). Might call something else like `game.world.clock`? world.clock?.isDay — optional. Might access `game.addDamageNumber` (provided). Let me just write the test and run it; adjust if it errors.

Now write the fixes.

**Fix 1 — Player.ts :850 block.** Current text (from my read):

```
    // 冰冻 Frozen(47,Player.cs:9749 frozen=true)：整帧封移动输入——跳跃/攀绳/矿车
    // 同读这些标志,一并归零(原版 Update 段 control* 清零语义)。帧末由 Game 重灌输入
    if (this.buffs.has(BuffType.Frozen)) { this.inputX = 0; this.inputJump = false; this.inputUp = false; this.inputDown = false; }
```

Replace with Frozen || shimmering and note it must precede the movement integration (regression: parallel rewrite moved horizontal integration above the shimmer branch's zeroing).

**Fix 2 — the shimmering branch at :922-927** — keep physics; the zeroing line there is now redundant but harmless. I'll trim it to avoid confusion? Actually leaving it is fine and acts as a belt. But cleanliness: the branch comment says frozen 封输入. I'll remove the redundant zeroing and point to the early block. Hmm — careful: if I remove it and something reads inputX between :850 and :925 expecting zero... no, it's zero from :850 onward. Keep removal minimal: I'll leave the zeroing line (harmless, idempotent) — no, better to keep code clear. Minimal diff principle: keep it. Actually keeping duplicate zeroing may confuse future readers. The instruction: fix execution order. Simplest robust fix: extend the early block. The later zeroing is redundant but not wrong. I'll keep it and add a comment that it's redundant-safe? Minimal: leave as is. Fine.

Also check: the shimmering physics branch is in the else-if chain keyed off `ropeHere && !this.inWater` first... The chain: `if (ropeHere && !this.inWater) {...} else if (this.inShimmer && !this.shimmering) {...} else if (this.shimmering) {...} else if (this.inWater) {...} else {...}`. Note: if player is in shimmer, inWater is false (wet excludes shimmer). ropeHere false in pool. So shimmering branch reached. OK.

But hmm — one more ordering check: the shimmering branch zeroes inputJump etc. at :925 — after that, code at :970+ `else` not taken. Then :1192 `if (!this.inputJump && ...)` — fine.

**Fix 3 — UI.ts:**
a) buildBuffBar list :1718-1721: add BuffType.Shimmered.
b) both icon maps: add `[BuffType.Shimmered, 'vi_5340_galaxy_pearl']`. Both maps are identical arrays; add at the end of each (after WellFed3 line, before `];`).

Wait — for map 1 (:2420-2428) the last entry is WellFed3 line then `];` then the for loop on same line `for (...) ...; }`. I'll insert before `];` in each.

Since the two arrays are textually identical in the tail, my Edit old_string must be unique. Map 1 tail:
```
      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],
      [BuffType.WellFed3, 'vi_1919_sugar_cookie'],
    ];
    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);  }
```
Map 2 tail:
```
      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],
      [BuffType.WellFed3, 'vi_1919_sugar_cookie'],
    ];
    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);
  }
}
```
Different following lines → unique. Good.

For buildBuffBar list, add Shimmered to the array.

**Fix 4 — tests.** Add describe block to tests/shimmer.test.ts. Need imports: BuffType from '../src/stats/Buffs'; Enemy from '../src/entities/Enemy'.

Tests:
1. `入微光：封输入（inputX 清零发生在移动积分之前）+ buff 353 登记 + 不可位移`:
```ts
const w = shimmerWorld();
const p = new Player(20 * TILE, 36 * TILE, new Inventory());
const h = hooks(w, p);
const x0 = p.x;
p.inputX = 1; p.inputJump = true;
for (let i = 0; i < 10; i++) {
  p.inputX = 1; p.inputJump = true;      // Game 每帧重灌（Game.ts:2234）
  p.fixedUpdate(1 / 60, h);
}
expect(p.inShimmer).toBe(true);
expect(p.shimmering).toBe(true);
expect(p.buffs.has(BuffType.Shimmered)).toBe(true);   // 左上角 debuff 图标来源
expect(p.inputX).toBe(0);                              // 清零须发生在移动积分之前
expect(Math.abs(p.vx)).toBeLessThan(0.05);
expect(p.x).toBe(x0);                                  // 不可位移
```
Careful: after the unstuck teleport (timeShimmering >= 1200 && anyInput → 1200 ticks) — 10 ticks only, timeShimmering=10, no teleport. Good. But wait — anyInput check happens at :719-724 BEFORE the zeroing, using raw input → with inputX=1, at 1200 it'd teleport; we're at 10 ticks, fine.

Hmm wait, another: `p.inputX).toBe(0)` — after 10th fixedUpdate, inputX was set to 1 before the call, then zeroed inside → 0. Good.

vx: with ix=0, friction applies: vx stays 0 (never accelerated). |vx| < 0.05. Good. x unchanged (moveAndCollide with vx=0; vy slow sink → y changes, x not). Good.

2. `Enemy 浸入 90t 转化`:
```ts
const w = shimmerWorld();
const p = new Player(45 * TILE, 30 * TILE, new Inventory());
const h = hooks(w, p);
const e = new Enemy('zombie', 20 * TILE, 34 * TILE);
const orig = e.vanillaId;
for (let i = 0; i < 200 && !e.dead; i++) e.fixedUpdate(1, h as never);
expect(e.dead || e.vanillaId !== orig).toBe(true);
```
Hmm — zombie AI may need more hooks. Let me be safe and check what zombie AI touches... simpler to write the test and run. If it fails due to missing hook, extend hooks(). But careful: hooks() is shared with other tests; I can create a local hooks2 with more fields. Let me first check what Enemy needs: does Enemy.fixedUpdate require `game.world.clock`? Possibly for day/night despawn (zombies flee/despawn at day). `game.world.clock?.isDay` — world has clock?: undefined → fallback. Might despawn? Let me just run it.

Also e.fixedUpdate(1, ...) with dt=1 second per call — zombie velocity integration with dt=1 might tunnel. But shimmer section just needs liquidCollision true. dt=1 movement: zombie falls 1s → could sink below pool bottom? Pool bottom at y=40 solid. Zombie at y=34, gravity 1s → vy ~ big → moveAndCollide clamps to solid. It will land at pool bottom, stay in shimmer. OK.

Actually there's a risk: zombie AI chases player... player at (45*TILE, 30*TILE) far away; zombie hops toward player, could exit pool? Only 20px/s × ... 200 calls × dt=1 = huge movement. Zombie would exit the pool quickly! Then shimmerT decays. Hmm.

Better: put the player far / or use an enemy with simple AI. Alternative: place player far away at (45*TILE, 30*TILE) = 400 tiles away? No: 45*TILE px = 45 tiles. Distance 25 tiles. Zombie walks at ~1-2 tiles/s; 200s of dt... it would leave.

Options: use dt small (1/60) and run 200 ticks = 3.3s — zombie moves a few tiles, pool is 20 tiles wide (x 10-30), starting at 20 → stays in pool. Good: run e.fixedUpdate(1/60, h) for 200 iterations. shimmerT increments per call → 200 > 90 → transform at ~91. 

But does zombie hop out of the pool? Zombie jump... pool is 7 tiles deep (33-40). Unlikely to escape in 1.5s. Also player is at y=30 above pool — zombie chases player direction (up-ish?). Eh. Should be fine; run and see.

Alternatively use 'green_slime' or something stationary. Zombie is proven constructible. Let's go with dt=1/60, 200 iterations.

3. Also maybe assert buff icon mapping? UI is DOM; can't easily test (needs document). Skip — the probe is about physics/buff/transform.

Now also verify the buff bar display path: refreshBuffs called by Game ~1/s. OK.

One more check on Fix 1: does `this.shimmering` exist at :850? Yes, computed at :712. But careful — the shimmerUnstuck teleport at :719-724 sets shimmering=false and teleports; then at :850 `this.shimmering` is false → no zeroing → player can move after teleport. Correct (vanilla: after unstuck you're free).

Also — `buffs.apply(BuffType.Shimmered, 1)` at :716: apply with 1 second. buffs.active stores seconds. And refreshBuffs shows ceil(left) seconds = "1秒". Vanilla shows the shimmer debuff icon. Fine.

Now implement edits.
````

</details>


---

## 🤖 Assistant · 2026-08-12T09:26:05.880Z · glm-x-preview-260804

```
根因齐了，开始修。**修 1**：Player.ts 把微光封输入提到移动积分之前（并入 Frozen 早封段，该段在水平积分 `const ix` 之前，且在 ridingCart 早退 return 之前——矿车上也生效，符合原版 Update 的 control* 清零语义）。
```


---

## 🤖 Assistant · 2026-08-12T09:26:08.657Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Player.ts",
 "old_string": "    // 冰冻 Frozen(47,Player.cs:9749 frozen=true)：整帧封移动输入——跳跃/攀绳/矿车\n    // 同读这些标志,一并归零(原版 Update 段 control* 清零语义)。帧末由 Game 重灌输入\n    if (this.buffs.has(BuffType.Frozen)) { this.inputX = 0; this.inputJump = false; this.inputUp = false; this.inputDown = false; }",
 "new_string": "    // 冰冻 Frozen(47,Player.cs:9749 frozen=true) ∪ 微光化 buff 353（:11381-11388\n    // frozen=true 同语义）：整帧封移动输入——跳跃/攀绳/矿车同读这些标志,一并归零\n    // （原版 Update 段 control* 清零语义,发生在移动积分之前）。帧末由 Game 重灌输入。\n    // ★必须在水平积分（下方 const ix = this.inputX 消费点）之前执行：矿车/装备聚合\n    // 重写曾把清零挪进 else-if 链的 shimmering 物理分支（位于积分之后）——清零形同\n    // 虚设,微光中仍可自由行走（2026-08 回归）\n    if (this.buffs.has(BuffType.Frozen) || this.shimmering) {\n      this.inputX = 0; this.inputJump = false; this.inputUp = false; this.inputDown = false;\n    }"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:08.730Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)

```


---

## 🤖 Assistant · 2026-08-12T09:26:10.930Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
File was modified on disk (parallel session still working). Careful. Next: the shimmering physics branch — remove the now-redundant zeroing? I need to re-read that area first since the file changed. Let me re-read the relevant regions (input zeroing area and shimmer branch) to confirm the edit landed correctly and see the current state.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:26:11.261Z · glm-x-preview-260804

```
并行会话仍在改盘。重读相关区域确认落地状态。
```


---

## 🤖 Assistant · 2026-08-12T09:26:12.057Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Frozen) || this.shimmering\\|else if (this.shimmering)\\|const ix = this.inputX\\|BuffType.Shimmered, 1\\|this.shimmering = this.inShimmer\" ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts",
 "description": "Verify edit anchors landed in Player.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:12.223Z

**📎 ToolResult**

```
714:    this.shimmering = this.inShimmer && this.y / TILE < world.lavaLine;
716:    if (this.shimmering) this.buffs.apply(BuffType.Shimmered, 1);
853:    // ★必须在水平积分（下方 const ix = this.inputX 消费点）之前执行：矿车/装备聚合
856:    if (this.buffs.has(BuffType.Frozen) || this.shimmering) {
868:    const ix = this.inputX;
930:    } else if (this.shimmering) {

```


---

## 🤖 Assistant · 2026-08-12T09:26:13.979Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Edit landed at :856, before :868 `const ix`. Good.

Now look at the shimmering physics branch :930 to remove the redundant zeroing (or leave). Let me read :925-940.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:26:14.252Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Player.ts",
 "limit": 14,
 "offset": 924
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:14.278Z

**📎 ToolResult**

```
924	      // 非微光化态浸微光：gravity 0.15（水 0.3 的一半）+ jumpHeight 23/jumpSpeed 5.51
925	      // （:24219-24223）——更轻、可大跳离池；微光不计摔伤
926	      if (this.inputJump) this.vy = Math.max(this.vy - 0.62, -5.5);
927	      this.vy += GRAVITY * 0.15;
928	      this.vy = Math.max(-5.5, Math.min(3.0, this.vy));
929	      this.fallStartY = null;
930	    } else if (this.shimmering) {
931	      // buff 353（:11381-11388）：frozen 封输入 + fallStart 重置（免摔伤）；
932	      // 物理 :24117-24119 gravity/maxFall ×0.9（近似正常慢沉，原地等脱困传送）
933	      this.inputX = 0; this.inputJump = false; this.inputUp = false; this.inputDown = false;
934	      this.vy = Math.min(this.vy + GRAVITY * 0.7 * 0.9, MAX_FALL_SPEED * 0.9);
935	      this.fallStartY = null;
936	    } else
937	    // 跳跃 / 游泳

```


---

## 🤖 Assistant · 2026-08-12T09:26:17.575Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Player.ts",
 "old_string": "    } else if (this.shimmering) {\n      // buff 353（:11381-11388）：frozen 封输入 + fallStart 重置（免摔伤）；\n      // 物理 :24117-24119 gravity/maxFall ×0.9（近似正常慢沉，原地等脱困传送）\n      this.inputX = 0; this.inputJump = false; this.inputUp = false; this.inputDown = false;\n      this.vy = Math.min(this.vy + GRAVITY * 0.7 * 0.9, MAX_FALL_SPEED * 0.9);\n      this.fallStartY = null;",
 "new_string": "    } else if (this.shimmering) {\n      // buff 353（:11381-11388）：frozen 封输入（输入清零在上方移动积分前的\n      // Frozen∪Shimmering 段执行——此处只做物理）+ fallStart 重置（免摔伤）；\n      // 物理 :24117-24119 gravity/maxFall ×0.9（近似正常慢沉，原地等脱困传送）\n      this.vy = Math.min(this.vy + GRAVITY * 0.7 * 0.9, MAX_FALL_SPEED * 0.9);\n      this.fallStartY = null;"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:17.648Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-12T09:26:20.004Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now UI.ts. Three edits:
1. buildBuffBar list: add BuffType.Shimmered.
2. Icon map 1 (ends :2428-2429 with `  }` on the for line).
3. Icon map 2 (initInGameLite).

For edit 1, old_string:
```
      BuffType.ObsidianSkin, BuffType.Gills, BuffType.ManaRegen, BuffType.MagicPower,
      BuffType.Featherfall, BuffType.WaterWalking, BuffType.Archery, BuffType.NightOwl]) {
```
Add `BuffType.Shimmered` — where? Put after NightOwl.
````

</details>


---

## 🤖 Assistant · 2026-08-12T09:26:20.600Z · glm-x-preview-260804

```
UI.ts 三处：buffBlocks 白名单 + 两处 icon map。
```


---

## 🤖 Assistant · 2026-08-12T09:26:21.122Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/UI.ts",
 "old_string": "      BuffType.ObsidianSkin, BuffType.Gills, BuffType.ManaRegen, BuffType.MagicPower,\n      BuffType.Featherfall, BuffType.WaterWalking, BuffType.Archery, BuffType.NightOwl]) {",
 "new_string": "      BuffType.ObsidianSkin, BuffType.Gills, BuffType.ManaRegen, BuffType.MagicPower,\n      BuffType.Featherfall, BuffType.WaterWalking, BuffType.Archery, BuffType.NightOwl,\n      BuffType.Shimmered]) {"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:21.250Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-12T09:26:24.723Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/UI.ts",
 "old_string": "      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],\n      [BuffType.WellFed3, 'vi_1919_sugar_cookie'],\n    ];\n    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);  }",
 "new_string": "      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],\n      [BuffType.WellFed3, 'vi_1919_sugar_cookie'],\n      // 微光化 353：银河珍珠 5340 近似（原版 Buff 353 无独立物品图标，debuff 显示\n      // 微光池主素材；两处 init 路径的 map 必须同步——曾只加一处导致另一路径无图标）\n      [BuffType.Shimmered, 'vi_5340_galaxy_pearl'],\n    ];\n    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);  }"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:24.790Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-12T09:26:27.438Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/src/ui/UI.ts",
 "old_string": "      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],\n      [BuffType.WellFed3, 'vi_1919_sugar_cookie'],\n    ];\n    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);",
 "new_string": "      [BuffType.WellFed, 'vi_5275_joja_cola'], [BuffType.WellFed2, 'vi_4023_grapes'],\n      [BuffType.WellFed3, 'vi_1919_sugar_cookie'],\n      // 微光化 353：银河珍珠 5340 近似（与上方 init 全量路径的 map 保持同步）\n      [BuffType.Shimmered, 'vi_5340_galaxy_pearl'],\n    ];\n    for (const [t, key] of map) this.buffIconItem.set(t, ITEM_BY_KEY[key]);"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:27.555Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/src/ui/UI.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-12T09:26:39.293Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now the probe tests. Append a describe block to tests/shimmer.test.ts. Need imports: BuffType, Enemy.

Current imports include Player, Inventory, World, TILE, ITEM_BY_KEY etc. Add:
```ts
import { BuffType } from '../src/stats/Buffs';
import { Enemy } from '../src/entities/Enemy';
```

Append describe block:

```ts
// ============ 回归探针（2026-08：并行矿车/装备重写把微光封输入挪到移动积分之后） ============
describe('微光封输入回归探针（buff 353 frozen + 图标来源 + NPC 转化链）', () => {
  it('浸微光：inputX 清零发生在移动积分之前 → 不可行走 + Shimmered buff 登记（左上角图标来源）', () => {
    const w = shimmerWorld();
    const p = new Player(20 * TILE, 36 * TILE, new Inventory());
    const h = hooks(w, p);
    const x0 = p.x;
    for (let i = 0; i < 10; i++) {
      // 模拟 Game.ts:2234 每帧重灌输入：灌进去之后 fixedUpdate 内必须清掉再积分
      p.inputX = 1; p.inputJump = true; p.inputDown = true;
      p.fixedUpdate(1 / 60, h);
    }
    expect(p.inShimmer).toBe(true);
    expect(p.shimmering).toBe(true);
    expect(p.buffs.has(BuffType.Shimmered)).toBe(true);  // 图标显示前提（UI buffBlocks 白名单）
    expect(p.inputX).toBe(0);                            // 清零须先于 const ix = this.inputX
    expect(Math.abs(p.vx)).toBeLessThan(0.05);           // 无水平加速 → 摩擦归零
    expect(p.x).toBe(x0);                                // 微光中不可位移（原版封输入）
  });

  it('敌怪浸入 90t 触发 NPC.GetShimmered 转化/消散（链路活性探针）', () => {
    const w = shimmerWorld();
    const p = new Player(45 * TILE, 30 * TILE, new Inventory());
    const h = hooks(w, p);
    const e = new Enemy('zombie', 20 * TILE, 34 * TILE);
    expect(e.vanillaId).not.toBeNull();
    const orig = e.vanillaId;
    for (let i = 0; i < 200 && !e.dead; i++) e.fixedUpdate(1 / 60, h as never);
    // 转化（ShimmerTransformToNPC 换型）或消散（TransformToItem 掉物后 dead）
    expect(e.dead || e.vanillaId !== orig).toBe(true);
  });
});
```

Concern: zombie AI may call hooks not in the hooks() stub → TypeError. Let me run and see. Also zombie may be a boss? no.

Also potential: `e.fixedUpdate(1/60, h)` — Enemy.fixedUpdate(game, dt)? In buff test: e.fixedUpdate(1, hooks) — so signature is (dt, game). Good, mine matches (1/60, h).

Also `hooks(w, p)` — spawnDrop returns null. If zombie → TransformToItem... zombie's transform: NPC 3 zombie. What is npcShimmerTransformTo(3)? Some NPC. transformTo called → tryTransformTo(id, store). OK.

Let me write the file edit. The file ends at line 234 with `});` for the last describe. I'll append after. Need to read the tail? I have the full file content already (read earlier). The tail is:

```
226	  it('地狱层内微光不生效（:11391-11397 position.Y/16 > UnderworldLayer → DelBuff）', () => {
...
233	  });
234	});
```

Wait the file may have been modified by parallel session? tests unlikely. Edit old_string: the last lines:
```
    p.fixedUpdate(1 / 60, hooks(w, p));
    expect(p.inShimmer).toBe(true);
    expect(p.shimmering).toBe(false);
  });
});
```

And append new describe after.

Also add imports. Old import block lines 10-23. I'll add after line 18 `import { Player } ...`:
Actually simplest: extend `import { Player } from '../src/entities/Player';` block — add new lines after `import { Inventory } from '../src/items/Inventory';`:

old:
```
import { Player } from '../src/entities/Player';
import { Inventory } from '../src/items/Inventory';
```
new:
```
import { Player } from '../src/entities/Player';
import { Enemy } from '../src/entities/Enemy';
import { Inventory } from '../src/items/Inventory';
import { BuffType } from '../src/stats/Buffs';
```
````

</details>


---

## 🤖 Assistant · 2026-08-12T09:26:39.616Z · glm-x-preview-260804

```
补探针测试到 tests/shimmer.test.ts：①封输入顺序+buff 登记 ②NPC 转化链活性。
```


---

## 🤖 Assistant · 2026-08-12T09:26:40.218Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts",
 "old_string": "import { Player } from '../src/entities/Player';\nimport { Inventory } from '../src/items/Inventory';",
 "new_string": "import { Player } from '../src/entities/Player';\nimport { Enemy } from '../src/entities/Enemy';\nimport { Inventory } from '../src/items/Inventory';\nimport { BuffType } from '../src/stats/Buffs';"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:40.326Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-12T09:26:46.504Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts",
 "old_string": "    p.fixedUpdate(1 / 60, hooks(w, p));\n    expect(p.inShimmer).toBe(true);\n    expect(p.shimmering).toBe(false);\n  });\n});",
 "new_string": "    p.fixedUpdate(1 / 60, hooks(w, p));\n    expect(p.inShimmer).toBe(true);\n    expect(p.shimmering).toBe(false);\n  });\n});\n\n// ============ 回归探针（2026-08：矿车/装备聚合重写把微光封输入挪到移动积分之后） ============\ndescribe('微光封输入回归探针（buff 353 frozen 语义 + 图标来源 + NPC 转化链）', () => {\n  it('浸微光：inputX 清零先于移动积分 → 不可行走 + Shimmered buff 每帧刷新（图标来源）', () => {\n    const w = shimmerWorld();\n    const p = new Player(20 * TILE, 36 * TILE, new Inventory());\n    const h = hooks(w, p);\n    const x0 = p.x;\n    for (let i = 0; i < 10; i++) {\n      // 模拟 Game.ts:2234 每帧重灌输入：灌入后 fixedUpdate 必须先清零再积分。\n      // 回归形态 = 清零在 else-if 链的 shimmering 物理分支（积分之后）→ 微光里自由行走\n      p.inputX = 1; p.inputJump = true; p.inputDown = true;\n      p.fixedUpdate(1 / 60, h);\n    }\n    expect(p.inShimmer).toBe(true);\n    expect(p.shimmering).toBe(true);\n    expect(p.buffs.has(BuffType.Shimmered)).toBe(true);  // 左上角 debuff 图标显示前提\n    expect(p.inputX).toBe(0);                            // 清零生效（先于 const ix 消费点）\n    expect(Math.abs(p.vx)).toBeLessThan(0.05);           // 无水平加速 → 摩擦钳零\n    expect(p.x).toBe(x0);                                // 微光中不可位移\n  });\n\n  it('敌怪浸微光 90t → NPC.GetShimmered 转化/消散链路活性（物理可入湖，入后必转化）', () => {\n    const w = shimmerWorld();\n    const p = new Player(45 * TILE, 30 * TILE, new Inventory());\n    const h = hooks(w, p);\n    const e = new Enemy('zombie', 20 * TILE, 34 * TILE);\n    expect(e.vanillaId).not.toBeNull();\n    const orig = e.vanillaId;\n    for (let i = 0; i < 200 && !e.dead; i++) e.fixedUpdate(1 / 60, h as never);\n    // ShimmerTransformToNPC 换型（vanillaId 变）或 TransformToItem 掉物后消散（dead）\n    expect(e.dead || e.vanillaId !== orig).toBe(true);\n  });\n});"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:26:46.635Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-12T09:26:47.926Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/shimmer.test.ts 2>&1 | tail -30",
 "description": "Run shimmer regression tests"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:27:02.630Z

**📎 ToolResult**

```
[l10n-audit] 312 键全部命中 ✓

 RUN  v2.1.9 ~/Project/GLM/SandboxWorld/game

 ❯ tests/shimmer.test.ts (15 tests | 1 failed) 59ms
   × 微光封输入回归探针（buff 353 frozen 语义 + 图标来源 + NPC 转化链） > 敌怪浸微光 90t → NPC.GetShimmered 转化/消散链路活性（物理可入湖，入后必转化） 9ms
     → expected null not to be null

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  tests/shimmer.test.ts > 微光封输入回归探针（buff 353 frozen 语义 + 图标来源 + NPC 转化链） > 敌怪浸微光 90t → NPC.GetShimmered 转化/消散链路活性（物理可入湖，入后必转化）
AssertionError: expected null not to be null
 ❯ tests/shimmer.test.ts:264:29
    262|     const h = hooks(w, p);
    263|     const e = new Enemy('zombie', 20 * TILE, 34 * TILE);
    264|     expect(e.vanillaId).not.toBeNull();
       |                             ^
    265|     const orig = e.vanillaId;
    266|     for (let i = 0; i < 200 && !e.dead; i++) e.fixedUpdate(1 / 60, h a…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯

 Test Files  1 failed (1)
      Tests  1 failed | 14 passed (15)
   Start at  17:26:57
   Duration  4.73s (transform 2.52s, setup 0ms, collect 3.48s, tests 59ms, environment 0ms, prepare 235ms)

```


---

## 🤖 Assistant · 2026-08-12T09:27:04.891Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The player probe passed. Enemy probe: `new Enemy('zombie', ...)` → vanillaId is null. So vanillaId is set later (perhaps by Game when spawning, or lazily in fixedUpdate). The shimmer gate requires `vanillaId !== null`. How is vanillaId assigned in production? Check Enemy.ts around :251 (`e.vanillaId = id;`) and constructor.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:27:05.282Z · glm-x-preview-260804

```
玩家探针全过。Enemy 的 vanillaId 构造时是 null——查它的赋值链路。
```


---

## 🤖 Assistant · 2026-08-12T09:27:05.739Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '400,430p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts; echo ---; sed -n '240,260p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Inspect Enemy constructor and vanillaId assignment"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:27:05.808Z

**📎 ToolResult**

```
   *  cs:57171 置位；Projectile.cs:12050 命中前反射——CanBeReflected 弹型白名单 +
   *  ReflectProjectile cs:67036 反向归属玩家管线未接，登记依赖） */
  reflectsProjectiles = false;
  /** 原版 NPC.takenDamageMultiplier（NPC.cs:6018，StrikeNPC :81997-82000 防
   *  御结算后 ×N）：419 旋刃冲刺中受击 ×3（cs:57172） */
  takenDamageMultiplier = 1;

  constructor(public key: string, x: number, y: number) {
    super();
    this.def = ENEMY_DEFS[key] ?? PLACEHOLDER_DEF;
    this.hp = this.def.hp;
    this.maxHp = this.def.hp;
    this.w = this.def.width;
    this.h = this.def.height;
    this.x = x - this.w / 2;
    this.y = y - this.h / 2;
  }

  fixedUpdate(dt: number, game: GameHooks) {
    this.prevX = this.x; this.prevY = this.y;
    // 联机傀儡（房主权威快照驱动）：无本地 AI——P3.2 插值/外推推进 + 动画计时，
    // 打击/拾取等交互经 entityNet 上报房主结算
    if (this.netPuppet) {
      this.aiT++;
      this.animT++;
      this.netPuppetStep();
      this.onGround = Math.abs(this.vy) < 0.6;
      if (Math.abs(this.vx) > 0.05) this.walkCycleT += Math.abs(this.vx);
      if (this.iframes > 0) this.iframes--;
      this.pushHistory();   // 傀儡无本地 AI 但拖尾渲染同样需要历史位置
      return;
---
      segs.push(s);
    }
    return segs;
  }


  /** 用原版数据造怪：属性/碰撞/音效全部来自 SetDefaults 提取值 */
  static fromVanilla(id: number, x: number, y: number): Enemy | null {
    const v = vanillaNpc(id);
    if (!v) return null;
    const e = new Enemy(`v_${id}`, x, y);
    e.vanillaId = id;
    e.vanilla = v;
    const hit = vanillaSoundName(v.HitSound) ?? 'NPC_Hit_1';
    const kill = vanillaSoundName(v.DeathSound) ?? 'NPC_Killed_1';
    const flying = v.noGravity || v.aiStyle === 2 || v.aiStyle === 5 || v.aiStyle === 14;
    e.def = {
      ...e.def,
      // friendly（被缚 NPC 等城镇系）与 critter 一样零接触伤害——原版 friendly 旗
      name: v.name, hp: v.lifeMax, damage: (v.critter || v.friendly) ? 0 : v.damage, defense: v.defense,
      // 原版 knockBackResist 是"承受击退的比例"（0.5=吃一半）；本仓库语义是

```


---

## 🤖 Assistant · 2026-08-12T09:27:07.456Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`Enemy.fromVanilla(id, x, y)` is the production constructor path that sets vanillaId. Zombie vanilla id = 3. Use `Enemy.fromVanilla(3, 20*TILE, 34*TILE)`. Check it returns non-null for id 3. Update the test.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:27:07.773Z · glm-x-preview-260804

```
vanillaId 由 `Enemy.fromVanilla` 赋值。改探针用该工厂（僵尸 = 原版 id 3）。
```


---

## 🤖 Assistant · 2026-08-12T09:27:09.209Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts",
 "old_string": "    const e = new Enemy('zombie', 20 * TILE, 34 * TILE);\n    expect(e.vanillaId).not.toBeNull();",
 "new_string": "    // 走原版数据工厂（fromVanilla 才置 vanillaId；直接 new Enemy('zombie') 是旧本地\n    // 数据路径，vanillaId=null → 微光转化门直接跳过——生产刷怪全部走 fromVanilla）\n    const e = Enemy.fromVanilla(3, 20 * TILE, 34 * TILE);   // 僵尸（NPCID 3）\n    expect(e).not.toBeNull();\n    expect(e!.vanillaId).toBe(3);"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:27:09.252Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-12T09:27:11.918Z · glm-x-preview-260804

**🔧 ToolUse: `Edit`**

```json
{
 "replace_all": false,
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts",
 "old_string": "    const orig = e.vanillaId;\n    for (let i = 0; i < 200 && !e.dead; i++) e.fixedUpdate(1 / 60, h as never);\n    // ShimmerTransformToNPC 换型（vanillaId 变）或 TransformToItem 掉物后消散（dead）\n    expect(e.dead || e.vanillaId !== orig).toBe(true);",
 "new_string": "    const orig = e!.vanillaId;\n    for (let i = 0; i < 200 && !e!.dead; i++) e!.fixedUpdate(1 / 60, h as never);\n    // ShimmerTransformToNPC 换型（vanillaId 变）或 TransformToItem 掉物后消散（dead）\n    expect(e!.dead || e!.vanillaId !== orig).toBe(true);"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:27:11.947Z

**📎 ToolResult**

```
The file ~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts has been updated successfully. (file state is current in your context — no need to Read it back)

```


---

## 🤖 Assistant · 2026-08-12T09:27:17.793Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/shimmer.test.ts 2>&1 | tail -20",
 "description": "Rerun shimmer tests"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:27:39.544Z

**📎 ToolResult**

```
[l10n-audit] 312 键全部命中 ✓

 RUN  v2.1.9 ~/Project/GLM/SandboxWorld/game

 ✓ tests/shimmer.test.ts (15 tests) 66ms

 Test Files  1 passed (1)
      Tests  15 passed (15)
   Start at  17:27:32
   Duration  6.64s (transform 4.34s, setup 0ms, collect 5.78s, tests 66ms, environment 0ms, prepare 177ms)

```


---

## 🤖 Assistant · 2026-08-12T09:27:41.398Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
All 15 pass. Now run tsc to check no new errors. The project has stale src/*.js artifacts per memory. Run `npx tsc --noEmit` and compare — the instruction says "tsc 零新增（忽略并行在制品）". Let me run tsc and look for errors in Player.ts, UI.ts, tests/shimmer.test.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:27:41.514Z · glm-x-preview-260804

```
15/15 全绿。跑 tsc 验证零新增。
```


---

## 🤖 Assistant · 2026-08-12T09:27:42.030Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | grep -E \"Player\\.ts|UI\\.ts|shimmer\" ; echo \"exit-filtered:$?\"",
 "description": "Typecheck filtered to touched files"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:28:10.959Z

**📎 ToolResult**

```
exit-filtered:1

```


---

## 🤖 Assistant · 2026-08-12T09:28:12.426Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx tsc --noEmit 2>&1 | tail -15; echo \"total:\"; npx tsc --noEmit 2>&1 | wc -l",
 "description": "Show overall tsc baseline"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:28:47.815Z

**📎 ToolResult**

```
src/core/Game.ts(8357,73): error TS2367: This comparison appears to be unintentional because the types '0 | 1 | 2' and '-1' have no overlap.
tests/_ghost.test.ts(28,3): error TS2322: Type 'string' is not assignable to type 'number'.
tests/hell-background.test.ts(51,8): error TS2341: Property 'ugAlpha' is private and only accessible within class 'BiomeBackground'.
tests/hell-background.test.ts(51,24): error TS2341: Property 'ugOld' is private and only accessible within class 'BiomeBackground'.
tests/hell-background.test.ts(72,8): error TS2341: Property 'ugAlpha' is private and only accessible within class 'BiomeBackground'.
tests/hell-background.test.ts(72,24): error TS2341: Property 'ugOld' is private and only accessible within class 'BiomeBackground'.
tests/hell-background.test.ts(88,8): error TS2341: Property 'ugAlpha' is private and only accessible within class 'BiomeBackground'.
tests/hell-background.test.ts(88,24): error TS2341: Property 'ugOld' is private and only accessible within class 'BiomeBackground'.
total:
       8

```


---

## 🤖 Assistant · 2026-08-12T09:29:00.473Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
tsc has 8 pre-existing errors, none in Player.ts / UI.ts / shimmer.test.ts — all zero new. (Game.ts error is parallel in-progress work; hell-background/_ghost are pre-existing test errors.)

Now one more sanity check: the buff bar display path. refreshBuffs iterates buffBlocks — Shimmered now included. buffIconItem has the entry in both init paths. Also check `iconUrl(this.game, iconId)` works for item 5340 (asset whitelist). Check iconUrl function handles it — galaxy pearl vi_5340 is a registered item; the atlas pipeline maps vi_ items. There was a memory note about "素材白名单管线" — items in items.ts get icons via atlas. Should be fine; can verify quickly whether iconUrl would produce a URL for 5340. Let me check the iconUrl implementation for whether vi_5340 is covered by the item atlas (items atlas is typically item_<id> sheet). Let me quickly grep iconUrl.

Actually the concern from memory (asset-lazy-loading): "素材白名单管线" for vui menu. In-game item icons use atlas item tiles by id — 5340 exists as an item in vanilla so its tile exists in the item sheet. Fine.

Also double-check: buffs.apply(BuffType.Shimmered, 1) — does BuffState.apply accept (type, seconds)? Yes, used elsewhere with 30, 7, 2.

One more consideration: refreshBuffs is called ~1/s; apply(…, 1) refreshes to 1s each tick — ceil(1)=1 → "1秒" label. Fine.

Also verify there isn't a second place in Game.ts that does a second movement after fixedUpdate (the user hypothesis ②). I checked inputX writers: :2234 (local input write) and :10099 (remote proxy). player.fixedUpdate called from Game fixed step. No second movement consumption found — and the probe test proves x displacement is 0 with the fix, which is the behavioral lock.

Also confirm ridingCart branch: zeroing at :856 happens before the ridingCart return at ~:860. Verified by grep earlier? The ridingCart block was at :854-859 before my edit (now shifted +6 → ~:860-866). The zeroing block at :856-858 is before it. Good — on-cart shimmer still locks input per vanilla.

Wait, actually let me double check one thing: on a minecart in shimmer, vanilla... the prompt says "ridingCart 分支 return 前要检查微光？原版矿车上微光仍生效". Our zeroing is before the return so input is locked; the cart (Minecart entity) drives position itself reading player input? The Minecart reads its own input presumably from inp directly, not player.inputX. Not our scope.

Everything done. Also quickly re-verify the file wasn't clobbered by the parallel session after my edits — run the vitest again? Already passed after edits (ran after both Player edits and UI edits and test edits). tsc ran last. Good.

Let me also run the wider related test suites quickly? The instruction says vitest tests/shimmer.test.ts green — done. Maybe also run buff-related tests to ensure no regression from the input zeroing change (e.g., tests that call player.fixedUpdate with inputs). Quick grep for tests using fixedUpdate with inputX expectations. Let me just run the full test suite? Could be long. Run a quick targeted set: tests matching player/buff/cart. Let me check how many test files exist and maybe run ones referencing inputX.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:29:01.089Z · glm-x-preview-260804

```
零新增（8 条全为并行在制品/历史遗留：Game.ts:8357、hell-background、_ghost）。跑一下涉及玩家输入的相邻测试防回归。
```


---

## 🤖 Assistant · 2026-08-12T09:29:01.634Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rln \"inputX\" ~/Project/GLM/SandboxWorld/game/tests | head; echo ---; npx vitest run tests/shimmer.test.ts tests/buff-r2-imbue.test.ts 2>&1 | tail -8",
 "description": "Run adjacent buff and input-related tests"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:29:30.148Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/tests/minecart-track.test.ts
~/Project/GLM/SandboxWorld/game/tests/a-batch1.test.ts
~/Project/GLM/SandboxWorld/game/tests/shimmer.test.ts
~/Project/GLM/SandboxWorld/game/tests/cobweb.test.ts
---
 ✓ tests/buff-r2-imbue.test.ts (5 tests) 12ms
 ✓ tests/shimmer.test.ts (15 tests) 37ms

 Test Files  2 passed (2)
      Tests  20 passed (20)
   Start at  17:29:27
   Duration  2.64s (transform 1.95s, setup 0ms, collect 3.91s, tests 49ms, environment 0ms, prepare 387ms)

```


---

## 🤖 Assistant · 2026-08-12T09:29:33.004Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/minecart-track.test.ts tests/cobweb.test.ts tests/a-batch1.test.ts 2>&1 | tail -8",
 "description": "Run minecart, cobweb, batch1 input tests"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:29:46.377Z

**📎 ToolResult**

```
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[11/11]⎯

 Test Files  1 failed | 2 passed (3)
      Tests  11 failed | 50 passed (61)
   Start at  17:29:41
   Duration  4.92s (transform 3.82s, setup 0ms, collect 7.58s, tests 89ms, environment 6ms, prepare 837ms)

```


---

## 🤖 Assistant · 2026-08-12T09:29:48.513Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "npx vitest run tests/minecart-track.test.ts tests/cobweb.test.ts tests/a-batch1.test.ts 2>&1 | grep -E \"FAIL|✗|×|AssertionError\" | head -20",
 "description": "Identify which test file failed"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:29:58.435Z

**📎 ToolResult**

```
   × 魔力回复（UpdateManaRegen :19214-19302） > 移动中基础产额：max100/mana50 → floor((33+1)×0.6×1.15)=23/tick 13ms
   × 魔力回复（UpdateManaRegen :19214-19302） > 静止加成：+max/3 → floor(67×0.6×1.15)=46/tick 2ms
   × 魔力回复（UpdateManaRegen :19214-19302） > 蓄能结算：累积 ≥120 才 +1 魔并扣 120（6×23=138 → mana51/count18） 1ms
   × 魔力回复（UpdateManaRegen :19214-19302） > 存量系数 num2：满魔 1.0 → 39/tick；空魔 0.2 → 7/tick（:19262-19268） 1ms
   × 魔力回复（UpdateManaRegen :19214-19302） > 用魔惩罚期：onManaItemUsed 后 delay=(1−0.5)×240+45 再 ×0.7=115.5，产额 0 2ms
   × 魔力回复（UpdateManaRegen :19214-19302） > 瓶中星 158：manaRegenBonus+10 / delayBonus+0.5（:9629-9632） 3ms
   × 冲刺（DashMovement 1:1） > 触发帧单次置速 16.9 并进入滑行态（:21131/:21138） 2ms
   × 冲刺（DashMovement 1:1） > 头部将撞墙减半（:21132-21137）：vx=8.45 1ms
   × 冲刺（DashMovement 1:1） > 滑行阻尼：|vx|>12 → ×0.985（:21100-21102） 2ms
   × 树苗全图切片采样（密度等价） > 单 tick 命中密度与原版逐点相等：gemP/(K×300) == 1.5e-05×(w×h)/区格数 0ms
   × 树苗全图切片采样（密度等价） > K 轮列切片无重叠覆盖全图（全图采样、不限域玩家附近） 1ms
 FAIL  tests/a-batch1.test.ts > 魔力回复（UpdateManaRegen :19214-19302） > 移动中基础产额：max100/mana50 → floor((33+1)×0.6×1.15)=23/tick
AssertionError: expected 106 to be 23 // Object.is equality
 FAIL  tests/a-batch1.test.ts > 魔力回复（UpdateManaRegen :19214-19302） > 静止加成：+max/3 → floor(67×0.6×1.15)=46/tick
AssertionError: expected 10 to be 46 // Object.is equality
 FAIL  tests/a-batch1.test.ts > 魔力回复（UpdateManaRegen :19214-19302） > 蓄能结算：累积 ≥120 才 +1 魔并扣 120（6×23=138 → mana51/count18）
AssertionError: expected 54 to be 51 // Object.is equality
 FAIL  tests/a-batch1.test.ts > 魔力回复（UpdateManaRegen :19214-19302） > 存量系数 num2：满魔 1.0 → 39/tick；空魔 0.2 → 7/tick（:19262-19268）
AssertionError: expected 63 to be 39 // Object.is equality
     97|     expect(p.manaRegenCount).toBe(39);  // floor(34×1.0×1.15)

```


---

## 🤖 Assistant · 2026-08-12T09:30:07.556Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The failures are in tests/a-batch1.test.ts (mana regen, dash, sapling). Are these pre-existing failures caused by the parallel rewrite (not by my change)? My change only adds `|| this.shimmering` to a zeroing block and removes a redundant zeroing. Mana regen failures ("expected 106 to be 23") look like the parallel session's mana/equip rewrite changed behavior. Dash failures similarly. To be sure my change isn't responsible, verify by stashing? Can't stash (not a git repo!). "Is directory a git repo: No". Hmm.

Check quickly: does a-batch1 failure relate to my change? My change only affects inputX/inputJump zeroing when shimmering. Mana regen: the "still" check uses |vx|<0.05 — input zeroing wouldn't change vx for those tests unless they set inputX... Dash tests use inputX. Hmm, dash: "触发帧单次置速" — my change zeroes inputX when shimmering; in dash tests player is not in shimmer (no shimmer in their world), so zeroing doesn't trigger. So failures unrelated.

Confirm by checking whether these tests fail due to pre-existing breakage — the mana numbers (106 vs 23) suggest manaRegen computation changed drastically by the parallel session (e.g., mana cap via equipStats.mana now includes something, or still detection). Let me verify quickly: run a-batch1 on the pristine copy? Not possible without git. But I can reason: run one mana test with a quick node check to see maxMana. If p.maxMana !== 100 expected... e.g., test expects 23 = floor((33+1)*0.6*1.15); got 106 → smm likely different (maybe maxMana now 200+?). That's from the parallel rewrite (they may have changed baseMaxMana or manaRegenDelayBonus). Definitely not my line.

Let me quickly confirm with a tiny script: create player, baseMaxHp... Actually faster: check git? Not a repo. Check if tests failed before my change — I can temporarily revert my Player.ts edit? Risky with parallel session writing. Instead reason via numbers: got 106 vs expected 23. My change can't alter manaRegen at all unless player.shimmering true (no shimmer in that test world presumably). Let me grep a-batch1 mana test setup to confirm no shimmer.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:30:08.147Z · glm-x-preview-260804

```
a-batch1 的失败集中在魔力回复/冲刺/树苗采样——与我的改动（仅微光封输入分支）无交集。快速验证这些是并行在制品导致的既有失败。
```


---

## 🤖 Assistant · 2026-08-12T09:30:09.432Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"shimmer\\|Shimmer\" ~/Project/GLM/SandboxWorld/game/tests/a-batch1.test.ts | head -3; echo \"---mana test setup---\"; grep -n \"manaRegenCount\\|baseMaxMana\\|new Player\" ~/Project/GLM/SandboxWorld/game/tests/a-batch1.test.ts | head -8; echo \"---跑一次单测看 maxMana---\"; sed -n '/移动中基础产额/,+12p' ~/Project/GLM/SandboxWorld/game/tests/a-batch1.test.ts | head -16",
 "description": "Check a-batch1 mana test setup for shimmer dependence"
}
```


---

## 👤 User(sidechain) · 2026-08-12T09:30:16.658Z

**📎 ToolResult**

```
---mana test setup---
49:const mkPlayer = (w: World): Player => new Player(20 * 16, 27 * 16, new Inventory());
60:    p.baseMaxMana = 100; p.mana = 50;
64:    expect(p.manaRegenCount).toBe(23);   // :19251-19268 产额公式
71:    p.baseMaxMana = 100; p.mana = 50;
74:    expect(p.manaRegenCount).toBe(46);
80:    p.baseMaxMana = 100; p.mana = 50;
87:    expect(p.manaRegenCount).toBe(18);  // 138-120
93:    p.baseMaxMana = 100;
---跑一次单测看 maxMana---
  it('移动中基础产额：max100/mana50 → floor((33+1)×0.6×1.15)=23/tick', () => {
    const w = mkWorld();
    const p = mkPlayer(w);
    p.baseMaxMana = 100; p.mana = 50;
    settle(p, w);
    p.vx = 10;                       // 非静止（IsConsideredStandingStill :3175 |v|<0.05）
    p.fixedUpdate(1 / 60, fakeHooks(w, p) as never);
    expect(p.manaRegenCount).toBe(23);   // :19251-19268 产额公式
    expect(p.mana).toBe(50);             // 23 < 120 不结算（:19275）
  });

  it('静止加成：+max/3 → floor(67×0.6×1.15)=46/tick', () => {
    const w = mkWorld();

```


---

## 🤖 Assistant · 2026-08-12T09:30:21.148Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No shimmer in a-batch1 world — my change cannot affect it. The failures are from the parallel rewrite (mana regen formula changed: got 106 for expected 23 — e.g., manaRegenDelay handling or still detection changed by the parallel session; also sapling sampling failures unrelated). These are pre-existing failures of the parallel in-progress work, out of scope. The task said "tsc 零新增（忽略并行在制品）" — same spirit for tests: shimmer.test.ts must be green, which it is (15/15).

To be extra certain my Player.ts edit didn't cause those, note the mana test got 106 vs 23 — that's ~4.6×, likely because `still` now computes differently or delay bonus. My edit touched only the shimmering input-zero block. Player at (20*16, 27*16) in mkWorld — no shimmer liquid. `this.shimmering` false → zeroing not triggered → identical behavior. Confirmed unrelated.

Done. Also confirm the buff icon key works: ITEM_BY_KEY['vi_5340_galaxy_pearl'] exists (items.ts:498). Good.

Final report ≤25 lines.
```

</details>


---

## 🤖 Assistant · 2026-08-12T09:30:28.713Z · glm-x-preview-260804

```
a-batch1 测试世界无任何微光（mkPlayer 在普通世界），我的改动（仅 shimmering 时清零）对它零影响——那 11 个失败是并行在制品（魔力回复公式/冲刺/树苗采样被重写改了行为）的既有失败，与本次修复无关。任务要求的 tests/shimmer.test.ts 15/15 全绿。

## 报告

**根因（并行重写破坏点）**
1. **能行走**：矿车/装备重写把水平移动积分提到前面（`const ix = this.inputX` @Player.ts:868），而微光封输入清零留在原 else-if 链的 shimmering 物理分支（:930，积分**之后**）——清零形同虚设。采样点 centerIdx 与 `buffs.apply(Shimmered)`（:716）均幸存，故伤害免疫在跑。
2. **无图标**：上次 Edit 确实没插上，且比预想更深——UI.ts 的 DOM buff 栏 `buffBlocks` 是硬编码 18 项白名单（buildBuffBar :1718），Shimmered 既不在白名单、也不在两处 icon map（:2429/:2503），双重缺失，buff 栏是唯一显示路径（vui 无 buff UI、buffIconItem 无其他消费者）。
3. **怪物进湖**：非 bug。Enemy 微光链（Enemy.ts:655-662 + npcGetShimmered :1402）完好，原版本就允许敌怪物理走进微光，90t（1.5s）后触发 GetShimmered 转化/消散；探针证实链路活着。

**修复**
- `src/entities/Player.ts`：封输入并入 :856 的 Frozen∪Shimmering 早封段（先于移动积分、先于 ridingCart 早退 return——矿车上也生效，对齐原版 Update 的 control* 清零序）；shimmering 物理分支删冗余清零只留慢沉。
- `src/ui/UI.ts`：buffBlocks 白名单 + **两处** icon map 均补 `[BuffType.Shimmered, 'vi_5340_galaxy_pearl']`（银河珍珠 5340 近似，键已注册 items.ts:498）。

**探针**（tests/shimmer.test.ts 新增 2 例，15/15 绿）
- 玩家浸微光每帧重灌 inputX=1×10t：`inputX===0`、`|vx|<0.05`、`x` 不变、`buffs.has(Shimmered)`——锁死清零顺序回归。
- `Enemy.fromVanilla(3)` 浸池 200t：转化/消散必发生（注：`new Enemy('zombie')` 的 vanillaId=null 不走转化门，生产必须用 fromVanilla）。

**验证**：tsc 零新增（现存 8 条均为并行在制品/历史遗留：Game.ts:8357、hell-background、_ghost）；相邻 minecart/cobweb/buff-r2 全过；a-batch1 的 11 个失败（魔力回复/冲刺/树苗）与本次无关，其世界无微光、改动点不触及。
```
