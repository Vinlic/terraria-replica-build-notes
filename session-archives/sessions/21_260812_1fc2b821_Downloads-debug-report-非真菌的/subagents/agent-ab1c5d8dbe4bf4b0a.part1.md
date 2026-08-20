# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-13T05:37:52.344Z

```
Codebase: ~/Project/GLM/SandboxWorld (TS, game/). READ-ONLY inventory. Thoroughness: very thorough.

Goal: inventory OUR spawn system's progression gates + enemy stat scaling, to compare against vanilla:

1. **game/src/world/spawn/VanillaSpawner.ts** (and any files it imports in that dir): report its full branch structure with line numbers — the biome/zone/depth/time selection tree. For EVERY branch, list:
   - which NPC ids it can spawn,
   - the progression gates present: `flags.hardMode` / `downed_125/126/127/134` (mechs) / `downed_262` (plantera) / `downed_398` (moon lord) / eclipse / bloodMoon etc.
   - explicitly flag any branch that LACKS a hardMode gate where intuition says vanilla would have one (e.g., hardmode-only enemies like wraiths 77/78, werewolf 145, clowns, corruptors 98/99/100, hallowed enemies 104+, armoured skeleton 77?, wraith, 闪电虫? — list which hardmode-only enemies we spawn and what gate protects them).
2. **Enemy stat scaling on spawn**: find where Enemy stats get scaled by difficulty/progression: game/src/stats/ScaleStats.ts (scaleStats function), game/src/entities/Enemy.ts fromVanilla (difficulty field, scaleStats call). Report:
   - what inputs drive scaling (world difficulty classic/expert/master? hardMode? downed flags? player count?),
   - whether ANY hardmode-progression multiplier exists (post-WoF / post-mech / post-plantera boosts),
   - the ScaleStats_ForExpertHardmode equivalent and its gates (downedPlantBoss etc.).
3. **Spawn rate/count modifiers**: where spawnRate/maxSpawns are set and whether hardMode/mech/plantera adjust them.
4. **setPlayerFlags** call and what flags flow into the spawner (line numbers).

Deliverable: structured inventory with file:line: (A) our spawn branch tree + gates per branch + list of hardmode-only enemy ids and their gates, (B) scaling inputs we consume (and any progression multiplier present/absent), (C) rate modifiers. Don't edit.
```

---

## 📎 Attachment · skill_listing · 2026-08-13T05:37:52.345Z

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

## 🤖 Assistant · 2026-08-13T05:37:54.082Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The user wants a very thorough read-only inventory of the spawn system. Let me start by finding the relevant files.

Let me look at the directory structure first, then read VanillaSpawner.ts and related files.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:37:54.321Z · glm-x-preview-260804

```
I'll start by mapping the spawn system directory structure and the key files.
```


---

## 🤖 Assistant · 2026-08-13T05:37:54.560Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/game/src/world/spawn -type f | sort",
 "description": "List all files in spawn directory"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:37:54.589Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts

```


---

## 🤖 Assistant · 2026-08-13T05:37:54.920Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/game/src/stats/ ~/Project/GLM/SandboxWorld/game/src/entities/ 2>/dev/null | head -80",
 "description": "List stats and entities directories"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:37:54.953Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/:
total 3144
drwxr-xr-x@ 44 user  staff    1408  8月 13 13:35 .
drwxr-xr-x@ 26 user  staff     832  8月 13 13:24 ..
-rw-r--r--@  1 user  staff   28700  8月 13 12:59 Arrow.ts
-rw-r--r--@  1 user  staff   19846  8月 13 13:31 Bobber.ts
-rw-r--r--@  1 user  staff   73957  8月 13 12:59 bossAI_dd2.ts
-rw-r--r--@  1 user  staff   26643  8月 13 13:35 bossAI_deerclops.ts
-rw-r--r--@  1 user  staff   76008  8月 13 11:39 bossAI_duke_moonlord.ts
-rw-r--r--@  1 user  staff   30328  8月 13 11:32 bossAI_golem.ts
-rw-r--r--@  1 user  staff   58775  8月 13 12:32 bossAI_lategame.ts
-rw-r--r--@  1 user  staff   82857  8月 13 12:38 bossAI_lunar_misc.ts
-rw-r--r--@  1 user  staff   37160  8月 13 10:37 bossAI_martian.ts
-rw-r--r--@  1 user  staff   43340  8月 13 11:35 bossAI_moon_events.ts
-rw-r--r--@  1 user  staff   31484  8月 13 12:34 bossAI_queenbee_plantera.ts
-rw-r--r--@  1 user  staff   30216  8月 13 13:04 bossAI_wof.ts
-rw-r--r--@  1 user  staff   60893  8月 13 13:05 bossAI.ts
-rw-r--r--@  1 user  staff   16428  8月 13 10:16 Critter.ts
-rw-r--r--@  1 user  staff   59988  8月 13 12:49 Dart.ts
-rw-r--r--@  1 user  staff  336802  8月 13 13:30 Enemy.ts
-rw-r--r--@  1 user  staff    3945  8月 13 10:49 Entity.ts
-rw-r--r--@  1 user  staff    4527  8月 13 01:25 FallingBlock.ts
-rw-r--r--@  1 user  staff    5473  8月 13 10:21 FallingStar.ts
-rw-r--r--@  1 user  staff   22129  8月 13 11:36 fighterFamilies.ts
-rw-r--r--@  1 user  staff   11601  8月 13 10:03 GolfBall.ts
-rw-r--r--@  1 user  staff   13714  8月 13 12:54 GrappleProj.ts
-rw-r--r--@  1 user  staff    3940  8月 12 17:21 HealProj.ts
-rw-r--r--@  1 user  staff   23120  8月 13 10:57 ItemDrop.ts
-rw-r--r--@  1 user  staff    2877  8月 13 09:51 MagicProj.ts
-rw-r--r--@  1 user  staff    4247  8月 13 08:40 MeteorChunk.ts
-rw-r--r--@  1 user  staff   13614  8月 13 12:52 Minecart.ts
-rw-r--r--@  1 user  staff   66791  8月 13 11:28 MinionProj.ts
-rw-r--r--@  1 user  staff   12206  8月 13 11:52 npcLiquid.ts
-rw-r--r--@  1 user  staff  140906  8月 13 13:35 Player.ts
-rw-r--r--@  1 user  staff   15902  8月 11 21:48 Portal.ts
-rw-r--r--@  1 user  staff    5380  8月 13 10:09 projStatus.ts
-rw-r--r--@  1 user  staff   12400  8月 13 10:54 projTargets.ts
-rw-r--r--@  1 user  staff    2830  8月 13 11:19 SquidCloud.ts
-rw-r--r--@  1 user  staff    5695  8月 10 13:32 Tombstone.ts
-rw-r--r--@  1 user  staff   29130  8月 13 13:07 TownNPC.ts
-rw-r--r--@  1 user  staff    3652  8月 13 00:33 TownShot.ts
-rw-r--r--@  1 user  staff    6306  8月 13 11:40 types.ts
-rw-r--r--@  1 user  staff    2154  8月 13 11:44 waterAvoid.ts
-rw-r--r--@  1 user  staff   63836  8月 13 11:28 WeaponProj.ts
-rw-r--r--@  1 user  staff   19546  8月 13 10:40 WhipProj.ts
-rw-r--r--@  1 user  staff    9847  8月 12 18:14 WhipTag.ts

~/Project/GLM/SandboxWorld/game/src/stats/:
total 256
drwxr-xr-x@  7 user  staff    224  8月 13 11:32 .
drwxr-xr-x@ 26 user  staff    832  8月 13 13:24 ..
-rw-r--r--@  1 user  staff  38911  8月 13 12:47 Buffs.ts
-rw-r--r--@  1 user  staff  16582  8月 13 10:14 Luck.ts
-rw-r--r--@  1 user  staff  30688  8月 13 11:31 ScaleStats.ts
-rw-r--r--@  1 user  staff  21083  8月 13 10:14 Shimmer.ts
-rw-r--r--@  1 user  staff   8739  8月 13 11:01 TouchDamage.ts

```


---

## 🤖 Assistant · 2026-08-13T05:37:55.903Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The spawn directory only has one file: VanillaSpawner.ts. Let me read it.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:37:56.040Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:37:56.259Z

**📎 ToolResult**

```
1	// 原版 1.4.5.6 NPC.Spawner 内嵌类 1:1 移植（Terarria1456/Terraria/NPC.cs:39-5952）。
2	// ★简化纪律:任何"未移植/近似/恒X"必须在 docs/spawn-parity-gaps.md 登记(含原版行号+
3	// 可见影响+依赖),否则视为未完成。先例:spawnFriendly 曾标"恒放行"导致兔鼠刷浮空岛。
4	// 结构：SetSpawnFlags(L276) → GetSpawnRate(L383-640) → FindSpawnTile(L879) →
5	//       SetSpawnFlagsForChosenTile(L950) → SpawnAnNPC(L1186-5144 巨型 if-else 链)。
6	// 权重语义：Main.rand.Next(N)==0（1/N 命中）；越靠前优先级越高。
7	// 困难模式分支保留并挂在 world.flags.hardMode（当前默认 false → 只走肉前）。
8	// 净 ID（负数）= SetDefaultsFromNetId(L7633)：基底类型 × scale + 属性/颜色覆盖。
9	// 原版 spawnTileType = NPC 落脚处上方格（GetProperGroundSpawnTileTypeAndWallType L5789）；
10	// 我们的等价 = 落脚格下方第一个实心格的 tile type。
11	import { TILE } from '../../core/constants';
12	import { RNG } from '../../core/rng';
13	import type { World } from '../World';
14	import { TILE_DEFS, TILE_BY_KEY } from '../../data/tiles';
15	import { Enemy } from '../../entities/Enemy';
16	import { debugPoolOverride } from '../../data/vanillaNpcs';
17	import { MOON_KIND_FROST, MOON_KIND_PUMPKIN } from '../MoonEvent';
18	import { TileStore } from '../TileStore';
19	import { mainExpertMode } from '../../stats/ScaleStats';
20	import { rollBadLuckExtreme, rollOnlyBadLuckExtreme, rollLuck } from '../../stats/Luck';
21	
22	/** 星璇塔刷怪上下文（Game 每帧随 setPlayerFlags 传入；null=事件未开启/不在任何塔区） */
23	export interface LunarSpawnCtx {
24	  /** 玩家 4000px 内各塔是否在场（SceneMetrics.CloseEnoughTo*Tower = WithinRangeOfNPC(塔id, 4000)，
25	   *  SceneMetrics.cs:276-282 / NPCEventZoneRadius=4000） */
26	  zone: { solar: boolean; vortex: boolean; nebula: boolean; stardust: boolean };
27	  /** 场上存活 NPC 计数（选表 CountNPCS 用；与月事件共用 Game 统计的 counts 表） */
28	  counts: ReadonlyMap<number, number>;
29	}
30	
31	/** 月事件刷怪上下文（Game 每帧随 setPlayerFlags 传入） */
32	export interface MoonEventSpawnCtx {
33	  /** 1=霜月 2=南瓜月（MoonEventState.kind） */
34	  kind: number;
35	  /** 当前波（MoonEventState.waveNumber） */
36	  wave: number;
37	  /** 场上存活 NPC 计数（id → 数量；选表 CountNPCS 用） */
38	  counts: ReadonlyMap<number, number>;
39	  /** Boss 族 npcSlots 总和（reachedInvasionBossCap 判定用，NPC.cs:159-183） */
40	  bossSlotSum: number;
41	}
42	
43	/** Boss 族（npcSlots 计入 reachedInvasionBossCap 的集合，NPC.cs:166-180） */
44	const MOON_BOSS_IDS = new Set([315, 325, 327, 328, 344, 345, 346]);
45	export { MOON_BOSS_IDS };
46	/** 单人 maxSpawns 上限 = ⌊5×(2+0.3×1)⌋ = 11（NPC.cs:174 num2） */
47	const MOON_BOSS_CAP_SLOTS = Math.floor(5 * (2 + 0.3 * 1));
48	
49	// ---- 原版 tile type 常量（TileID），我们通过 TILE_BY_KEY 反查内部 id ----
50	const T = (() => {
51	  const get = (k: string) => TILE_BY_KEY[k] ?? 0;
52	  return {
53	    DIRT: get('dirt'), GRASS: get('grass'), STONE: get('stone'),
54	    SAND: get('sand'), SNOW: get('snow'), ICE: get('ice'), MUD: get('mud'),
55	    JUNGLE_GRASS: get('v_60_jungle_grass_block'), CORRUPT_GRASS: get('v_23_corrupt_grass_block'),
56	    CRIMSON_GRASS: get('v_199_crimson_grass_block'), MUSHROOM_GRASS: get('v_70_mushroom_grass_block'),
57	    EBONSAND: get('v_112_ebonsand_block'), CRIMSAND: get('v_234_crimsand_block'),
58	    PEARLSAND: get('v_116_pearlsand_block'), HARDENED_SAND: get('hardened_sand'),
59	    SANDSTONE: get('sandstone'), FOSSIL: get('desert_fossil'),
60	    MARBLE: get('v_367_marble_block'), GRANITE: get('v_368_granite_block'),
61	    // 23 陨石（tiles.ts key 为 ore_meteorite，非 v_23_*）
62	    METEORITE: get('ore_meteorite'),
63	    // 恶地落脚门两矿石（NPC.cs:3973/4032 tile 门：猩红 =(204&&ZoneCrimson)||199||200||203||234||662，
64	    // 腐化 =(22&&ZoneCorrupt)||23||25||112||163||661）——204=猩红矿/22=魔矿（TileID.cs:477/841），
65	    // 旧注释把 22 误标为"黄沙"并以 T.SAND&&ZoneCorrupt 顶替，已按原版改判矿石
66	    CRIMTANE: get('ore_crimtane'), DEMONITE: get('ore_demonite'),
67	    // 232 木刺（NPC.cs:3821 神庙砖门 tile 226||232）
68	    WOODEN_SPIKE: get('v_232_wooden_spike'),
69	    CACTUS: get('v_80_cactus'), SNOW_BRICK: get('snow_brick'), CATTAIL: get('v_519_cattails'),
70	    CORRUPT_ICE: get('v_163_purple_ice_block'), CRIMSON_ICE: get('v_200_red_ice_block'),
71	    // 164 粉冰(=神圣冰)：key 实为 v_164_pink_ice_block（旧注"未注册→0"有误，已注册）
72	    HOLLOW_ICE: get('v_164_pink_ice_block'), DUNGEON_BLUE: get('v_41_blue_brick'),
73	    DUNGEON_GREEN: get('v_43_green_brick'), DUNGEON_PINK: get('v_44_pink_brick'),
74	    // 恶土系计数(SceneMetrics.cs:614-615 非 remix 的 _tileCounts 公式)
75	    EBONSTONE: get('v_25_ebonstone_block'), CORRUPT_PLANT: get('v_24_corruption_short_plants'),
76	    CORRUPT_THORN: get('v_32_corruption_thorns'), CORRUPT_HARDSAND: get('v_398_corrupt_hardened_sand_block'),
77	    CRIMSTONE: get('v_203_crimstone_block'), CRIMSON_PLANT: get('v_201_crimson_short_plants'),
78	    CRIMSAND_THORN: get('v_352_crimtane_thorns'), CRIMSON_HARDSAND: get('v_399_crimson_hardened_sand_block'),
79	    SUNFLOWER: get('v_27_sunflower'),
80	    // 墓碑 85（SceneMetrics.cs:622 GraveyardTileCount）：Tombstones 单 tile 覆盖全部
81	    // 6 种墓碑（GraveMarker/Cross/Headstone/Gravestone/Obelisk/Golden 均为 style 变体）
82	    TOMBSTONE: get('tombstone_v'),
83	    // 神圣族计数(SceneMetrics.cs:603)：109 神圣草/492 神圣修剪草/110 神圣矮草/
84	    // 113 神圣高草/117 珍珠岩/402 神圣硬化沙/403 神圣沙岩（116 珍珠沙/164 粉冰见上）
85	    HALLOW_GRASS: get('v_109_hallowed_grass_block'), HALLOW_MOWED_GRASS: get('v_492_hallowed_mowed_grass_block'),
86	    MOWED_GRASS: get('v_477_mowed_grass_block'),
87	    HALLOW_PLANT: get('v_110_hallow_short_plants'), HALLOW_TALL_PLANT: get('v_113_hallow_tall_plants'),
88	    PEARLSTONE_BLOCK: get('v_117_pearlstone_block'), HALLOW_HARDSAND: get('v_402_hallow_hardened_sand_block'),
89	    HALLOW_SANDSTONE: get('v_403_hallow_sandstone_block'),
90	    // 雪族计数(SceneMetrics.cs:604)：162 薄冰（147/148/161/163/200/164 见上/常量区）
91	    THIN_ICE: get('thin_ice'),
92	    // 丛林族计数(SceneMetrics.cs:613)：61 矮草/62 藤/74 高草/225 蜂巢块/226 神庙砖
93	    JUNGLE_PLANT: get('v_61_jungle_short_plants'), JUNGLE_VINE: get('v_62_jungle_vines'),
94	    JUNGLE_TALL_PLANT: get('v_74_jungle_tall_plants'), HIVE: get('v_225_hive_block'),
95	    LIHZAHRD_BRICK: get('v_226_lihzahrd_brick'),
96	    // 蘑菇族计数(SceneMetrics.cs:617)：71 植株/72 蘑菇树/528 藤（70 蘑菇草见上）
97	    MUSHROOM_PLANT: get('v_71_mushroom_plant'), MUSHROOM_TREE: get('v_72_mushroom_tree'),
98	    MUSHROOM_VINE: get('v_528_mushroom_vines'),
99	    // 190 发光蘑菇块（NPC.cs:5010/5109 glowshroom 出怪门 tile 70||190 之一）
100	    MUSHROOM_BLOCK: get('v_190_glowing_mushroom_block'),
101	    // Moss 族（TileID.Sets.Conversion.Moss，TileID.cs:38）：CheckToSpawnRockGolem 落脚门
102	    // 179 绿/180 黄/181 红/182 蓝/183 紫/381 熔岩/534 氪/536 氙/539 氩/625 氖/627 氦
103	    MOSS_GREEN: get('v_179_green_moss_block'), MOSS_YELLOW: get('v_180_yellow_moss_block'),
104	    MOSS_RED: get('v_181_red_moss_block'), MOSS_BLUE: get('v_182_blue_moss_block'),
105	    MOSS_PURPLE: get('v_183_purple_moss_block'), MOSS_LAVA: get('v_381_lava_moss'),
106	    MOSS_KRYPTON: get('v_534_krypton_moss_block'), MOSS_XENON: get('v_536_xenon_moss_block'),
107	    MOSS_ARGON: get('v_539_argon_moss_block'), MOSS_NEON: get('v_625_neon_moss_block'),
108	    MOSS_HELIUM: get('v_627_helium_moss_block'),
109	    // 恶地族补齐（SceneMetrics.cs:614-615）：661 腐化丛林草/400 腐化沙岩/662/401 猩红对位
110	    // （旧注释称引擎无 def——实际均已注册，按 0 计是漏）
111	    CORRUPT_JUNGLE_GRASS: get('v_661_corrupt_jungle_grass_block'),
112	    CORRUPT_SANDSTONE: get('v_400_corrupt_sandstone_block'),
113	    CRIMSON_JUNGLE_GRASS: get('v_662_crimson_jungle_grass_block'),
114	    CRIMSON_SANDSTONE: get('v_401_crimson_sandstone_block'),
115	  };
116	})();
117	/** 房屋墙表（Main.cs wallHouse[N]=true 全提取，265 项）：可由玩家放置的墙。
118	 *  FindSpawnTile L886：落点格带房屋墙 → 弃选（房屋内不刷怪的主守卫）；
119	 *  SetSpawnFlags L321：玩家所站格带房屋墙 → noWorms（房屋内不出蠕虫） */
120	const WALL_HOUSE = new Set([1, 4, 5, 6, 10, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 60, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 82, 84, 85, 88, 89, 90, 91, 92, 93, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 167, 168, 169, 172, 173, 174, 175, 176, 177, 179, 181, 182, 183, 184, 186, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366]);
121	
122	/** EvilTileCount 计数表(SceneMetrics.cs:614):23/661/24/25/32/112/163/400/398 计 1,27 向日葵 −10 */
123	const EVIL_LOOKUP = (() => {
124	  const t = new Uint8Array(TILE_DEFS.length);
125	  for (const id of [T.CORRUPT_GRASS, T.CORRUPT_JUNGLE_GRASS, T.EBONSTONE, T.CORRUPT_PLANT,
126	    T.CORRUPT_THORN, T.EBONSAND, T.CORRUPT_ICE, T.CORRUPT_SANDSTONE, T.CORRUPT_HARDSAND]) if (id) t[id] = 1;
127	  return t;
128	})();
129	/** BloodTileCount 计数表(SceneMetrics.cs:615):199/662/201/203/200/401/399/234/352 计 1 */
130	const BLOOD_LOOKUP = (() => {
131	  const t = new Uint8Array(TILE_DEFS.length);
132	  for (const id of [T.CRIMSON_GRASS, T.CRIMSON_JUNGLE_GRASS, T.CRIMSTONE, T.CRIMSON_PLANT,
133	    T.CRIMSON_ICE, T.CRIMSON_SANDSTONE, T.CRIMSON_HARDSAND, T.CRIMSAND, T.CRIMSAND_THORN]) if (id) t[id] = 1;
134	  return t;
135	})();
136	/** HolyTileCount 计数表(SceneMetrics.cs:603):109/492/110/113/117/116/164/403/402 计 1 */
137	const HOLY_LOOKUP = (() => {
138	  const t = new Uint8Array(TILE_DEFS.length);
139	  for (const id of [T.HALLOW_GRASS, T.HALLOW_MOWED_GRASS, T.HALLOW_PLANT, T.HALLOW_TALL_PLANT,
140	    T.PEARLSTONE_BLOCK, T.PEARLSAND, T.HOLLOW_ICE, T.HALLOW_SANDSTONE, T.HALLOW_HARDSAND]) if (id) t[id] = 1;
141	  return t;
142	})();
143	/** SnowTileCount 计数表(SceneMetrics.cs:604):147/148/161/162/164/163/200 计 1
144	 *  （注意 164 粉冰/163 紫冰/200 红冰同时计入雪族——转化冰都算雪原） */
145	const SNOW_LOOKUP = (() => {
146	  const t = new Uint8Array(TILE_DEFS.length);
147	  for (const id of [T.SNOW, T.SNOW_BRICK, T.ICE, T.THIN_ICE, T.HOLLOW_ICE,
148	    T.CORRUPT_ICE, T.CRIMSON_ICE]) if (id) t[id] = 1;
149	  return t;
150	})();
151	/** JungleTileCount 计数表(SceneMetrics.cs:613 非 remix):60/61/62/74/226/225 计 1 */
152	const JUNGLE_LOOKUP = (() => {
153	  const t = new Uint8Array(TILE_DEFS.length);
154	  for (const id of [T.JUNGLE_GRASS, T.JUNGLE_PLANT, T.JUNGLE_VINE, T.JUNGLE_TALL_PLANT,
155	    T.LIHZAHRD_BRICK, T.HIVE]) if (id) t[id] = 1;
156	  return t;
157	})();
158	/** MushroomTileCount 计数表(SceneMetrics.cs:617):70/71/72/528 计 1 */
159	const MUSHROOM_LOOKUP = (() => {
160	  const t = new Uint8Array(TILE_DEFS.length);
161	  for (const id of [T.MUSHROOM_GRASS, T.MUSHROOM_PLANT, T.MUSHROOM_TREE, T.MUSHROOM_VINE]) if (id) t[id] = 1;
162	  return t;
163	})();
164	/** Main.tileSand 全表（Main.cs:7177-7180，1.4.5.6 仅 4 项）：
165	 *  isOcean 判定（NPC.cs L1104）用沙族集合而非只认 53 黄沙 */
166	const TILE_SAND = new Set([T.SAND, T.EBONSAND, T.PEARLSAND, T.CRIMSAND]);
167	/** TileID.Sets.Conversion.Moss（TileID.cs:38）全表：CheckToSpawnRockGolem 落脚 tile 门
168	 *  （NPC.cs:5715：spawnTileType==1 石 或 Moss 族） */
169	const TILE_MOSS = new Set([T.MOSS_GREEN, T.MOSS_YELLOW, T.MOSS_RED, T.MOSS_BLUE, T.MOSS_PURPLE,
170	  T.MOSS_LAVA, T.MOSS_KRYPTON, T.MOSS_XENON, T.MOSS_ARGON, T.MOSS_NEON, T.MOSS_HELIUM]);
171	/** Main.unlockedSlimePurpleSpawn（NPC.cs:1325 绑缚紫史莱姆门）：玩家解锁紫城镇史莱姆后
172	 *  置位。本仓无城镇史莱姆解锁链 → 恒 false（门恒开，与未解锁世界一致）。
173	 *  登记 docs/spawn-parity-gaps.md（解锁链依赖 TownNPC 686 管线） */
174	const UNLOCKED_SLIME_PURPLE_SPAWN = false;
175	
176	// ---- 洞穴主池 cavernMonsterType 表（NPC.cs:6498 + 世界生成时 18058-18064 填充） ----
177	export let cavernMonsterType: number[][] = [[49, 49, 49], [49, 49, 49]];
178	export function rollCavernMonsterType(rng: RNG): void {
179	  for (let i = 0; i < 2; i++) {
180	    // 原版 Next(494,496)/Next(496,498)/Next(498,507)（WorldGen L18058-18064）——
181	    // 本仓库 RNG.int 为闭区间，此前写 int(494,496) 会多出 496/498/507 三个越界 id
182	    cavernMonsterType[i][0] = rng.int(494, 495); // 洞穴蝾螈族 v_494/v_495
183	    cavernMonsterType[i][1] = rng.int(496, 497);
184	    cavernMonsterType[i][2] = rng.int(498, 506);
185	  }
186	}
187	
188	// ---- 原版 netID（负数）→ SetDefaultsFromNetId（L7633-7820）：基底 id + scale + 属性覆盖 ----
189	// scale/color/alpha 一律取源数据（public/sprites/vanilla-npcnetid.json，extract-npccolors.mjs 提取）
190	import vanillaNetIdJson from '../../data/vanilla-npcnetid.json';
191	const NET_ID_OVERRIDE: Record<string, { scale?: number; color?: number[]; alpha?: number }> = vanillaNetIdJson;
192	
193	const NET_ID_MAP: Record<number, { base: number; scale: number; hp?: number; dmg?: number; def?: number }> = {
194	  '-1': { base: 16, scale: 0.6, hp: 90, dmg: 45, def: 10 },   // 母史莱姆
195	  '-2': { base: 16, scale: 0.9, hp: 90, dmg: 45, def: 20 },
196	  '-3': { base: 1, scale: 0.9, hp: 14, dmg: 6, def: 0 },   // 绿史莱姆
197	  '-4': { base: 1, scale: 0.6, hp: 150, dmg: 5, def: 5 },
198	  '-5': { base: 1, scale: 0.9, hp: 30, dmg: 13, def: 4 },  // 黑史莱姆
199	  '-6': { base: 1, scale: 1.05, hp: 45, dmg: 15, def: 4 },
200	  '-7': { base: 1, scale: 1.2, hp: 40, dmg: 12, def: 6 },
201	  '-8': { base: 1, scale: 1.025, hp: 35, dmg: 12, def: 4 }, // 红（母史莱姆子代）
202	  '-9': { base: 1, scale: 1.2, hp: 45, dmg: 15, def: 7 },   // 黄
203	  '-10': { base: 1, scale: 1.1, hp: 60, dmg: 18, def: 6 },  // 丛林
204	  '-11': { base: 6, scale: 0.85 },   // 小噬魂怪
205	  '-12': { base: 6, scale: 1.15 },   // 大噬魂怪
206	  // 黄蜂族大小变体（FromNetId NetIdMap[55..64]：两两一族 231-235；scale 取 netid 表）
207	  '-16': { base: 42, scale: 0.85 }, '-17': { base: 42, scale: 1.2 },    // Little/Big Stinger
208	  '-56': { base: 231, scale: 0.85 }, '-57': { base: 231, scale: 1.25 },
209	  '-58': { base: 232, scale: 0.8 }, '-59': { base: 232, scale: 1.17 },
210	  '-60': { base: 233, scale: 0.83 }, '-61': { base: 233, scale: 1.21 },
211	  '-62': { base: 234, scale: 0.78 }, '-63': { base: 234, scale: 1.16 },
212	  '-64': { base: 235, scale: 0.87 }, '-65': { base: 235, scale: 1.21 },
213	  // 地牢骷髅变体（SetDefaultsFromNetId L7770-7788：scale 后再乘 stat）
214	  '-13': { base: 31, scale: 0.9, hp: 72, dmg: 23, def: 7 },    // Short Bones(80/26/8 ×0.9)
215	  '-14': { base: 31, scale: 1.15, hp: 101, dmg: 33, def: 10 }, // Big Boned(×1.15 再 ×1.1)
216	  '-15': { base: 1, scale: 1.15 },   // 史莱姆王子
217	  // -22..-25 猩红族大小变体（SetDefaultsFromNetId L7858-7911 + NPCID.NetIdMap idx21-24）：
218	  //  -22/-23 = 小/大 Crimera（基底 173，scale 0.85/1.15）；-24/-25 = 小/大 Crimslime
219	  //  （基底 183，scale 0.85/1.15）。旧表误写 base:223（雨僵尸）——猩红分支
220	  //  （L4000-4020）补齐后这些 netId 会真实刷出，基底错则贴图/属性全错
221	  '-22': { base: 173, scale: 0.85 }, '-23': { base: 173, scale: 1.15 },
222	  '-24': { base: 183, scale: 0.85 }, '-25': { base: 183, scale: 1.15 },
223	  // 僵尸/骷髅/眼变种 = 基底 + scale（贴图同基底，属性缩放）。
224	  // 基底一律以 NPCID.NetIdMap（NPCID.cs:12457-12465，index = -id-1）为准：
225	  // -26..-37 僵尸族基底 3/132/186/187/188/189；-38..-42 恶魔眼族基底 190-194
226	  // （旧表误写 base:3——贴图/属性全错）；-43 基底 2；-44/-45 基底 200
227	  '-26': { base: 3, scale: 0.9 }, '-27': { base: 3, scale: 1.1 },
228	  '-28': { base: 132, scale: 0.85 }, '-29': { base: 132, scale: 1.15 },
229	  '-30': { base: 186, scale: 0.93 }, '-31': { base: 186, scale: 1.13 },
230	  '-32': { base: 187, scale: 0.89 }, '-33': { base: 187, scale: 1.11 },
231	  '-34': { base: 188, scale: 0.87 }, '-35': { base: 188, scale: 1.13 },
232	  '-36': { base: 189, scale: 0.92 }, '-37': { base: 189, scale: 1.08 },
233	  '-38': { base: 190, scale: 1.15 }, '-39': { base: 191, scale: 1.1 },
234	  '-40': { base: 192, scale: 0.9 }, '-41': { base: 193, scale: 0.85 },
235	  '-42': { base: 194, scale: 1.1 },
236	  '-43': { base: 2, scale: 0.85 },  // 小恶魔眼
237	  '-44': { base: 200, scale: 0.87 }, '-45': { base: 200, scale: 1.05 },
238	  '-46': { base: 21, scale: 0.9 }, '-47': { base: 21, scale: 0.9 },
239	  '-48': { base: 201, scale: 0.9 }, '-49': { base: 201, scale: 0.9 },
240	  '-50': { base: 202, scale: 0.9 }, '-51': { base: 202, scale: 0.9 },
241	  '-52': { base: 203, scale: 0.9 }, '-53': { base: 203, scale: 0.9 },
242	  '-54': { base: 223, scale: 0.9 }, '-55': { base: 223, scale: 1.1 },
243	};
244	
245	export class VanillaSpawner {
246	  // ---- SpawnFlags（Spawner 字段 L39-137） ----
247	  private pX = 0; private pY = 0;
248	  private dayTime = true;
249	  private hardMode = false;
250	  private expert = false;
251	  private waterTile = false;
252	  private noWorms = false;         // 原版 wallHouse（房屋内不出蠕虫）
253	  /** GetSpawnRate 城镇段置位（NPC.cs:717/:734/:750/:767/:792/:814）：城镇 NPC ≥1 时
254	   *  蠕虫抑制。原版与 wallHouse 同字段（GetSpawnRate 在 SetSpawnFlags 之后调用,
255	   *  直接覆写 noWorms）;本仓 getSpawnRate/spawn 拆两次调用 → 先闩锁,spawn() 合成 */
256	  private townNoWorms = false;
257	  /** 原 ignoreSafeWalls（:73/:318）：仅星璇四塔 Zone 置位——FindSpawnTile :886 的
258	   *  房屋墙拒选豁免（塔战允许穿房屋墙刷怪;普通入侵不置位） */
259	  private ignoreSafeWalls = false;
260	  private skyMob = false;
261	  private surfaceSpawn = false;
262	  /** 本轮 spawnFriendly（NPC.cs:711-832 掷骰）：true = 本轮只走友好小动物链
263	   *  （SpawnAnNPC `else if (spawnFriendly)` :2006 段）;false = 小动物/宝石鼠兔/水黾段全跳过 */
264	  private spawnFriendlyCycle = false;
265	  /** Game 每轮尝试前置入(原版在 GetSpawnRate 同一例程内掷,本仓拆到 Game 侧以便
266	   *  同步 spawnRate/maxSpawns 修正;语义同序:掷骰失败时的 spawnRate 罚倍由 Game 应用) */
267	  setFriendlyCycle(v: boolean): void {
268	    this.spawnFriendlyCycle = v;
269	  }
270	  /** 原 underGround（L1043 非 remix）= spawnTileY <= rockLayer——**含地表**（见
271	   *  setFlagsForChosenTile 注释：旧实现误写成 groundLevel<y<rockLayer 带状） */
272	  private underGround = false;
273	  private deeperThanRockLayer = false;
274	  private isOcean = false;
275	  private isBeach = false;
276	  private nearMarble = false;
277	  private nearGranite = false;
278	  private spawnUndergroundDesert = false;
279	  /** 蜘蛛巢旗标（L1066/L1074）：落点邻域 ±5..15 格内有墙 62（1/3 概率扫描），
280	   *  或玩家所站格墙 62（2/3 概率查玩家位）——蜘蛛巢内/附近必出蜘蛛的真正触发器 */
281	  private spawnSpider = false;
282	  private ZoneSnow = false; private ZoneCorrupt = false; private ZoneCrimson = false;
283	  private ZoneHallow = false; private ZoneJungle = false; private ZoneGlowshroom = false;
284	  /** 陨石带（SceneMetrics.cs:56/685：窗口内陨石 tile ≥ MeteorTileThreshold=75） */
285	  private ZoneMeteor = false;
286	  private ZoneDungeon = false; private ZoneGraveyard = false; private ZoneBeach = false;
287	  /** 原版 downedBoss3（杀过骷髅王）：地牢分支切换 守卫→常规怪池 */
288	  private downedBoss3 = false;
289	  private spawnTileX = 0; private spawnTileY = 0;
290	  /** FindSpawnTile 的 xRange 输出（L911：落脚点横向在 safeArea 内，传给 SpawnAnNPC） */
291	  private xRange = false;
292	  private spawnTileType = 0;
293	  /** 落脚点（Game 放置用） */
294	  currentSpawnX = 0;
295	  currentSpawnY = 0;
296	  /** GetZombieSettings（L5495）的地表夜僵尸 style（SpawnAnNPC 入口 Next(7) roll，L1193） */
297	  private zombieStyle = 0;
298	  /** GetZombieSettings（L5499-5514）：火把僵尸 590/591 的概率门分母。
299	   *  基础 12；playerHasStartingHealth（statLifeMax≤100，L327）→ 5 − 活跃玩家数/2（下限 2） */
300	  private torchZombieChance = 12;
301	  /** 玩家 statLifeMax（playerHasStartingHealth 判定用；未传入视为非初始血量 → 概率门 12） */
302	  private playerLifeMax = 0;
303	  /** 玩家幸运度（Spawner 各 Roll*Luck 掷骰的 luck 参，NPC.cs:5260-5275 委托
304	   *  Luck.Roll*(luck, range)；未传入 0 = 中性掷骰 Next(range)）。来源 Player.luck
305	   *  （RecalculateLuck :28672-28697 聚合，Game 每帧 setPlayerFlags 下发） */
306	  private playerLuck = 0;
307	  /** 玩家 ZoneWaterCandle（SetSpawnFlags L308 = player.ZoneWaterCandle =
308	   *  SceneMetrics.WaterCandleCount>0）。本仓取 getSpawnRate 的 waterCandle 入参
309	   *  （Game 传 手持||邻近，略宽于原版 SceneMetrics 单源）——SpawnAnNPC 的
310	   *  399/87/86 水蜡烛加重支消费 */
311	  private zoneWaterCandle = false;
312	
313	  constructor(private world: World) {}
314	
315	  /** 玩家级 Zone 旗标（原版 Spawner.SetSpawnFlags L300：ZoneDungeon = player.ZoneDungeon——
316	   *  SceneMetrics 按玩家中心窗口判定，与落脚点无关）。Game 每帧刷怪前调用。
317	   *  invaders = ShouldSpawnInvasionEnemies(NPC.cs:352，入侵前线 3000px 内的地表玩家)；
318	   *  activeIds = 场上存活 NPC 的 vanillaId 集（选表 AnyNPCs 去重用）；
319	   *  moonEvent = 月事件上下文（事件开启时 Game 传入；null=无事件） */
320	  invaders = false;
321	  activeIds: Set<number> = new Set();
322	  /** 月事件上下文（null=无事件）+ 当帧 Boss 上限旗标（Spawner.ctor NPC.cs:159-183） */
323	  moonEvent: MoonEventSpawnCtx | null = null;
324	  moonBossCap = false;
325	  /** 星璇塔 Zone 上下文（null=不在塔区）；invaders 语义（SetSpawnFlags :315-318）由此驱动 */
326	  lunar: LunarSpawnCtx | null = null;
327	  setPlayerFlags(zoneDungeon: boolean, downedSkeletron: boolean,
328	    invaders = false, activeIds: Set<number> = new Set(),
329	    moonEvent: MoonEventSpawnCtx | null = null,
330	    lunar: LunarSpawnCtx | null = null,
331	    playerLifeMax = 0,
332	    playerLuck = 0): void {
333	    this.ZoneDungeon = zoneDungeon;
334	    this.downedBoss3 = downedSkeletron;
335	    this.invaders = invaders;
336	    this.activeIds = activeIds;
337	    this.moonEvent = moonEvent;
338	    this.lunar = lunar;
339	    this.playerLifeMax = playerLifeMax;
340	    this.playerLuck = playerLuck;
341	    // SetSpawnFlags :315-319：任一塔 Zone → invaders=true && ignoreSafeWalls=true
342	    // （Game 侧 lunar 仅在任一塔 Zone 时非 null → 直接等价）
343	    this.ignoreSafeWalls = lunar != null;
344	    // reachedInvasionBossCap（Spawner 构造器 NPC.cs:159-183）：Boss 族 npcSlots 总和
345	    // ≥ 玩家数 × maxSpawns 上限（单人 ⌊5×2.3⌋=11）时当帧不刷 Boss
346	    this.moonBossCap = moonEvent != null && moonEvent.bossSlotSum >= 1 * MOON_BOSS_CAP_SLOTS;
347	  }
348	
349	  /** 天气注入（Game 每 15 tick 下发）：cloudAlpha（雨强度，雪原刷怪修正）与沙尘暴态（怪池） */
350	  rainCloudAlpha = 0;
351	  sandstormHappening = false;
352	  zoneSandstorm = false;
353	  setWeather(cloudAlpha: number, sandstormHappening: boolean, zoneSandstorm: boolean): void {
354	    this.rainCloudAlpha = cloudAlpha;
355	    this.sandstormHappening = sandstormHappening;
356	    this.zoneSandstorm = zoneSandstorm;
357	  }
358	
359	  /** SlimeRainSpawns（NPC.cs:5829-5898 1:1）：史莱姆雨天空落怪。
360	   *  独立于常规 spawnRate 概率门（原版每玩家每帧先调本函数再 TrySpawnAnNPC）。
361	   *  nearbySlots>15 / 玩家过深直接拒绝；num3=45+450×(nearby/15)（专家 ×0.85）。
362	   *  落点：x=玩家±viewW、y=玩家上方 (1.5~0.75)×viewH 带 → 格门：
363	   *  x∈[10,w+10]、y∈[surface×0.3, surface]、周围 7×8 无实心、落点无房屋墙。
364	   *  选怪：1/200 蓝(-4)；专家 1/7 大(-7)、1/3 绿(-3)；普通 1/10 大、2/5 绿；默认蓝(1) */
365	  slimeRainSpawns(px: number, py: number, nearbySlots: number, viewW: number, viewH: number, rng: RNG, expert: boolean): Enemy | null {
366	    const w = this.world;
367	    const worldSurface = w.groundLevel;
368	    if (py > worldSurface * 16 + viewH / 2 || nearbySlots > 15) return null;
369	    const num2 = nearbySlots / 15;
370	    let num3 = 45 + Math.floor(450 * num2);
371	    if (expert) num3 = Math.floor(num3 * 0.85);
372	    if (num3 < 1) num3 = 1;
373	    if (rng.int(0, num3 - 1) !== 0) return null;
374	    const x0 = Math.floor(px - viewW), x1 = x0 + viewW * 2;
375	    const y0 = Math.floor(py - viewH * 1.5), y1 = Math.floor(py - viewH * 0.75);
376	    const tx = Math.floor(rng.int(x0, x1 - 1) / 16);
377	    const ty = Math.floor(rng.int(y0, y1 - 1) / 16);
378	    const st = w.store;
379	    if (tx < 10 || tx > st.w + 10 || ty < worldSurface * 0.3 || ty > worldSurface) return null;
380	    if (!st.inBounds(tx, ty)) return null;
381	    for (let dx = -3; dx <= 3; dx++) {
382	      for (let dy = -5; dy <= 2; dy++) {
383	        if (st.inBounds(tx + dx, ty + dy) && st.isSolid(tx + dx, ty + dy)) return null;
384	      }
385	    }
386	    if (WALL_HOUSE.has(st.wall[st.idx(tx, ty)])) return null;
387	    let netId = 1;
388	    if (rng.int(0, 199) === 0) netId = -4;
389	    else if (expert) {
390	      if (rng.int(0, 6) === 0) netId = -7;
391	      else if (rng.int(0, 2) === 0) netId = -3;
392	    } else {
393	      if (rng.int(0, 9) === 0) netId = -7;
394	      else if (rng.int(0, 4) < 2) netId = -3;
395	    }
396	    return this.spawnNPC(tx * 16 + 8, ty * 16, netId, rng);
397	  }
398	
399	  /** 造怪入口：netId 可为负（SetDefaultsFromNetId 映射）；
400	   *  ai0/ai1 = 原版 SpawnNPC 第 6/7 参（如攀爬者 101 的锚点格，NPC.cs:4040） */
401	  private spawnNPC(x: number, y: number, netId: number, rng: RNG, ai0?: number, ai1?: number): Enemy | null {
402	    const map = NET_ID_MAP[netId];
403	    const baseId = map?.base ?? netId;
404	    const e = Enemy.fromVanilla(baseId, x, y);
405	    if (!e) return null;
406	    // 原版 NewNPC 锚点(NPC.cs:46596-46597):X-width/2, Y-height(底部贴格顶)。
407	    // 此前 fromVanilla 中心锚(y-h/2)把怪埋进落脚实心格半格高——飞行怪沿地面内沿
408	    // 漂移穿过侧壁,看起来像穿墙(噬魂怪等 ai5 族)
409	    e.y = y - e.h;
410	    const ov = NET_ID_OVERRIDE[String(netId)];
411	    e.vanillaNetId = netId;
412	    if (map) {
413	      e.vanillaScale = ov?.scale ?? map.scale;   // scale 优先源数据（SetDefaults_ForNetId 第 3 参）
414	      if (map.hp != null) e.hp = e.maxHp = map.hp;
415	      if (map.dmg != null) e.def.damage = map.dmg;
416	      if (map.def != null) e.def.defense = map.def;
417	    } else if (ov?.scale != null) {
418	      e.vanillaScale = ov.scale;
419	    }
420	    // SetDefaultsFromNetId 覆盖 color/alpha（L7633+：color = new Color(...) / alpha = N）
421	    if (ov?.color) e.colorRGBA = [ov.color[0], ov.color[1], ov.color[2], ov.color[3] ?? 255];
422	    if (ov?.alpha != null) e.spawnAlpha = ov.alpha;
423	    // 植物族锚点（aiStyle 13：锚点格存 ai0/ai1）
424	    if (ai0 !== undefined && ai1 !== undefined) { e.ai0 = ai0; e.ai1 = ai1; }
425	    e.id = this.world.store.w; // 占位，Game 侧会重编
426	    return e;
427	  }
428	
429	  /** 绑缚三人组占位造怪（NPC.cs:1994-2005）：105/106/685 在本仓的产出是 bound
430	   *  TownNPC——Game.trySpawnEnemy 只读 vanillaId 做转换，占位体随即弃置。
431	   *  不走 spawnNPC/fromVanilla：vanilla-npcs.json 缺 685 条目（fromVanilla null 静默
432	   *  丢弃，同 686 先例），三 id 统一走 PLACEHOLDER_DEF 保证链路可达 */
433	  private spawnBound(id: number): Enemy {
434	    const e = new Enemy(`v_${id}`, this.spawnTileX * TILE + 8, this.spawnTileY * TILE);
435	    e.vanillaId = id;
436	    e.id = this.world.store.w; // 占位，Game 侧会重编
437	    return e;
438	  }
439	
440	  // ---- SetSpawnFlagsForChosenTile（L950-1185） ----
441	  private setFlagsForChosenTile(spawnTileX: number, spawnTileY: number, spawnTileType: number, rng: RNG): void {
442	    const st = this.world.store;
443	    this.spawnTileX = spawnTileX; this.spawnTileY = spawnTileY; this.spawnTileType = spawnTileType;
444	    // waterTile（L957）：落脚格上方两格都是液体且为水
445	    const above1 = st.idx(spawnTileX, spawnTileY - 1), above2 = st.idx(spawnTileX, spawnTileY - 2);
446	    this.waterTile = st.liquid[above1] > 0 && st.liquid[above2] > 0 && st.liquidType[above1] === 1;
447	    // nearMarble/nearGranite（L960-1046）：落点 tile → 玩家 tile → 两轮邻近扫描
448	    // (落点 ±Next(20,30) 步长 Next(1,4) + 玩家 ±Next(30,60) 步长 Next(3,7) 抽样)。
449	    // 只查落点/玩家两格会让小体量大理石/花岗岩洞几乎永远探测不到
450	    if (spawnTileType === T.MARBLE) this.nearMarble = true;
451	    else if (spawnTileType === T.GRANITE) this.nearGranite = true;
452	    else if (st.type[st.idx(this.pX, this.pY)] === T.MARBLE) this.nearMarble = true;
453	    else if (st.type[st.idx(this.pX, this.pY)] === T.GRANITE) this.nearGranite = true;
454	    else {
455	      const scanType = (cx0: number, cy0: number, r: number, stepI: number, stepJ: number) => {
456	        const x0 = Math.max(0, cx0 - r), x1 = Math.min(st.w - 1, cx0 + r);
457	        const y0 = Math.max(0, cy0 - r), y1 = Math.min(st.h - 1, cy0 + r);
458	        for (let i = x0; i <= x1; i += stepI) {
459	          for (let j = y0; j <= y1; j += stepJ) {
460	            const tt = st.type[st.idx(i, j)];
461	            if (tt === T.MARBLE) this.nearMarble = true;
462	            else if (tt === T.GRANITE) this.nearGranite = true;
463	          }
464	        }
465	      };
466	      scanType(spawnTileX, spawnTileY, rng.int(20, 30), rng.int(1, 3), 1 + (rng.next() * 3 | 0));
467	      scanType(this.pX, this.pY, rng.int(30, 60), rng.int(3, 6), 3 + (rng.next() * 4 | 0));
468	    }
469	    // 地下沙漠（L1078-1100）：同蜘蛛巢的双路触发——1/3 扫落点 ±Next(5,15) 墙集，2/3 查玩家所站格墙。
470	    // 墙表 = WallID.Sets.AllowsUndergroundDesertEnemiesToSpawn 全表（WallID.cs:42：
471	    // 187,216,217,218,219,220,221,222,223 九种——此前只取 {216,217,187} 三分之一，
472	    // 沙岩/硬化沙变体墙区域漏判）；门带 !invaders（原版 L1077/L1053 同款）
473	    const DESERT_WALL = (w: number) => w === 216 || w === 217 || w === 218 || w === 219
474	      || w === 220 || w === 221 || w === 222 || w === 223 || w === 187;
475	    if (spawnTileY < this.world.rockLevel && spawnTileY > 200 && !this.ZoneDungeon && !this.invaders) {
476	      if (rng.next() < 1 / 3) {
477	        const r = rng.int(5, 14);
478	        const x0 = Math.max(0, spawnTileX - r), x1 = Math.min(st.w - 1, spawnTileX + r - 1);
479	        const y0 = Math.max(0, spawnTileY - r), y1 = Math.min(st.h - 1, spawnTileY + r - 1);
480	        for (let sx = x0; sx <= x1 && !this.spawnUndergroundDesert; sx++) {
481	          for (let sy = y0; sy <= y1; sy++) {
482	            if (DESERT_WALL(st.wall[st.idx(sx, sy)])) { this.spawnUndergroundDesert = true; break; }
483	          }
484	        }
485	      } else if (DESERT_WALL(st.wall[st.idx(this.pX, this.pY)])) {
486	        this.spawnUndergroundDesert = true;
487	      }
488	    }
489	    this.surfaceSpawn = spawnTileY <= this.world.groundLevel;
490	    // L1146-1153 第二支：岩石层-20 以下的落点在血月（或日食昼）且处于世界中带
491	    // （x ∈ (0.38w+50, 0.62w)）→ 强制地表化（血月僵尸从地下刷怪口涌向地表的语义）
492	    if (spawnTileY > this.world.rockLevel - 20
493	      && ((this.world.clock?.bloodMoon) || (this.world.clock?.eclipse && this.world.clock?.isDay))
494	      && spawnTileX > st.w * 0.38 + 50 && spawnTileX < st.w * 0.62) {
495	      this.surfaceSpawn = true;
496	    }
497	    this.deeperThanRockLayer = spawnTileY >= this.world.rockLevel;
498	    // L1043（非 remix）：underGround = spawnTileY <= rockLayer——**含地表**！消费点有二：
499	    //  ① 神圣段 :3946 门 (hardMode && underGround)（内部 661 支自带 surfaceSpawn 条件
500	    //   即是"本段可从地表进入"的原文佐证）→ 地表神圣落脚夜间同样出 122/86/75 池;
501	    //  ② 地下层刷怪段 :4718——位于 surfaceSpawn 段之后,可达时恒 worldSurface < y <= rockLayer
502	    //   （与旧带状写法等价,行为不变）。
503	    //  旧实现误写成 groundLevel<y<rockLayer 带状 → 地表神圣被该段漏判
504	    this.underGround = spawnTileY <= this.world.rockLevel;
505	    // isOcean（L1104 1:1）：(边缘 && Main.tileSand[spawnTileType] && 岩石层上)
506	    //  || (spawnTileType==53 && oceanDepths)。沙族 = Main.cs:7177-7180 全表（53/112/116/234），
507	    //  只认 53 会漏黑檀沙/珍珠沙/猩红沙海床。
508	    // oceanDepths（WorldGen.cs:10978-10988 1:1）：y ≤ oceanLevel（=（worldSurface+rockLayer)/2+40，
509	    //  WorldGen.cs:4393）&& x < beachDistance。oceanDistance/beachDistance 是
510	    //  **不随图宽缩放**的常量（WorldGen.cs:4100/4102 = 250/380）——BeachPass 的
511	    //  oceanWater 220~260 / beachSandRandomCenter+20=340 是另一套生成期随机值，
512	    //  与本判定的 250/380 无对应关系，此前借它近似（260/340）属错位：
513	    //  第二项 beachX 340→380 会漏判 40 格沙滩海床。本仓世界恒 4200 宽（van=1），
514	    //  直接取原版常量。
515	    const oceanX = 250;    // WorldGen.oceanDistance
516	    const beachX = 380;    // WorldGen.beachDistance
517	    this.isOcean = ((spawnTileX < oceanX || spawnTileX > st.w - oceanX)
518	      && TILE_SAND.has(spawnTileType) && spawnTileY < this.world.rockLevel)
519	      || (spawnTileType === T.SAND
520	        && spawnTileY <= (this.world.groundLevel + this.world.rockLevel) / 2 + 40
521	        && (spawnTileX < beachX || spawnTileX > st.w - beachX));
522	    this.isBeach = spawnTileY <= this.world.groundLevel && (spawnTileX < beachX || spawnTileX > st.w - beachX);
523	    // Zone 判定（SceneMetrics.cs:24-64/648-697）：全部六族走玩家中心 169×123 窗口计数，
524	    // 阈值 Snow 1500 / Corrupt·Crimson 300 / Hallow 125 / Jungle 140 / Mushroom 100。
525	    // 旧实现只有恶地走窗口计数，其余只看落脚单格 → 雪原/神圣/丛林/蘑菇地常漏判
526	    this.refreshZoneCounts(this.pX, this.pY);
527	    this.ZoneSnow = this.zoneCounts.snow >= 1500;
528	    this.ZoneCorrupt = this.zoneCounts.evil >= 300;
529	    this.ZoneCrimson = this.zoneCounts.blood >= 300;
530	    this.ZoneHallow = this.zoneCounts.holy >= 125;
531	    this.ZoneJungle = this.zoneCounts.jungle >= 140;
532	    this.ZoneGlowshroom = this.zoneCounts.mushroom >= 100;
533	    this.ZoneMeteor = this.zoneCounts.meteor >= 75;
534	    // ZoneGraveyard（SceneMetrics.cs:622-623/686）：墓碑 85 计数 − 向日葵/2（下取整、钳 ≥0）
535	    //  ≥ GraveyardTileThreshold 28——向日葵每 2 株抵 1 块墓碑
536	    this.ZoneGraveyard = this.zoneCounts.graveyard >= 28;
537	    // ZoneDungeon 不在此设置：原版取玩家 SceneMetrics（SetSpawnFlags L300），见 setPlayerFlags
538	    // ---- 蜘蛛巢旗标（L1045-1079）:岩石层~地狱层 && 非地牢 && 非入侵时 ----
539	    // 1/3 概率扫落点 ±Next(5,15) 立方盒内任意墙 62;否则查玩家所站格墙 62。
540	    // 此前只查落点一格,玩家站巢里时屏幕外环带点几乎全在巢外 → 蜘蛛永不触发
541	    if (spawnTileY > this.world.rockLevel && spawnTileY < st.h - 200 && !this.ZoneDungeon && !this.invaders) {
542	      if (rng.next() < 1 / 3) {
543	        const r = rng.int(5, 14);
544	        const x0 = Math.max(0, spawnTileX - r), x1 = Math.min(st.w - 1, spawnTileX + r - 1);
545	        const y0 = Math.max(0, spawnTileY - r), y1 = Math.min(st.h - 1, spawnTileY + r - 1);
546	        for (let sx = x0; sx <= x1 && !this.spawnSpider; sx++) {
547	          for (let sy = y0; sy <= y1; sy++) {
548	            if (st.wall[st.idx(sx, sy)] === 62) { this.spawnSpider = true; break; }
549	          }
550	        }
551	      } else if (st.wall[st.idx(this.pX, this.pY)] === 62) {
552	        this.spawnSpider = true;
553	      }
554	    }
555	  }
556	
557	  /** tileDungeon 集（Main.cs:7941-7946）：41/43/44 主砖（677-679 安全变体未注册缺席=0）。
558	   *  PostCheckChosenSpawnTile L922-927：ZoneDungeon 时落脚点必须踩地牢砖且
559	   *  spawnWallType（=落脚格上方一格的墙，GetProperGroundSpawnTileTypeAndWallType L5792）非 0。
560	   *  查落脚格自身的墙会因地板砖 wall=0 恒拒 → 地牢几乎不刷怪 */
561	  /** IsThisAGoodPlaceForAStatueMimic（NPC.cs:43751-43761 1:1）：落脚 x/x+1 两格
562	   *  SolidTile2（活跃+实心+无坡+非半砖+非致动），上方 3 格两列全净空。
563	   *  与附近是否存在雕像无关（函数名历史遗留）——纯落点预检 */
564	  private isGoodPlaceForAStatueMimic(): boolean {
565	    const st = this.world.store;
566	    const x = this.spawnTileX, y = this.spawnTileY;
567	    const solid2 = (tx: number, ty: number): boolean => {
568	      if (!st.inBounds(tx, ty)) return false;
569	      const i = st.idx(tx, ty);
570	      if (!st.flags[i]) return false;                    // active()
571	      if (st.wire[i] & TileStore.WIRE_ACTUATED) return false;   // inActive()（致动位）
572	      if (st.half[i]) return false;                      // halfBrick()
573	      if (st.slope[i] !== 0) return false;               // slope()==0
574	      return !!TILE_DEFS[st.type[i]]?.solid;             // Main.tileSolid
575	    };
576	    if (!solid2(x, y) || !solid2(x + 1, y)) return false;
577	    for (let dy = 1; dy <= 3; dy++) {
578	      if (st.inBounds(x, y - dy) && st.flags[st.idx(x, y - dy)]) return false;
579	      if (st.inBounds(x + 1, y - dy) && st.flags[st.idx(x + 1, y - dy)]) return false;
580	    }
581	    return true;
582	  }
583	
584	  private isDungeonTile(t: number): boolean {
585	    return t === T.DUNGEON_BLUE || t === T.DUNGEON_GREEN || t === T.DUNGEON_PINK;
586	  }
587	
588	  /** SceneMetrics.ScanTiles 近似：玩家中心 169×123 窗口(zoneScanSize=1920/16+49 × 1200/16+49)
589	   *  一次扫描同时产出全部六族计数，setFlagsForChosenTile 与 getSpawnRate 共用。
590	   *  原版 SceneMetrics 每帧增量维护；本类无帧钩子 → 0.5s 或玩家移动 ≥32 格才重算（近似） */
591	  private zoneStamp = -1;
592	  private zoneCX = -99999; private zoneCY = -99999;
593	  private zoneCounts = { evil: 0, blood: 0, holy: 0, snow: 0, jungle: 0, mushroom: 0, meteor: 0, graveyard: 0 };
594	
595	  private refreshZoneCounts(cx: number, cy: number): void {
596	    const now = performance.now();
597	    if (this.zoneStamp >= 0 && now - this.zoneStamp < 500
598	      && Math.abs(cx - this.zoneCX) < 32 && Math.abs(cy - this.zoneCY) < 32) return;
599	    this.zoneStamp = now; this.zoneCX = cx; this.zoneCY = cy;
600	    const st = this.world.store;
601	    const x0 = Math.max(2, cx - 84), x1 = Math.min(st.w - 3, cx + 84);
602	    const y0 = Math.max(2, cy - 61), y1 = Math.min(st.h - 3, cy + 61);
603	    let evil = 0, blood = 0, holy = 0, snow = 0, jungle = 0, mushroom = 0, sunflower = 0, meteor = 0, tomb = 0;
604	    for (let y = y0; y <= y1; y++) {
605	      const row = y * st.w;
606	      for (let x = x0; x <= x1; x++) {
607	        const i = row + x;
608	        if (!st.flags[i]) continue;   // 仅活跃格（SceneMetrics.ScanTiles 同语义）
609	        const t = st.type[i];
610	        if (EVIL_LOOKUP[t]) evil++;
611	        else if (BLOOD_LOOKUP[t]) blood++;
612	        else if (HOLY_LOOKUP[t]) holy++;
613	        else if (SNOW_LOOKUP[t]) snow++;
614	        else if (JUNGLE_LOOKUP[t]) jungle++;
615	        else if (MUSHROOM_LOOKUP[t]) mushroom++;
616	        else if (t === T.METEORITE) meteor++;
617	        else if (t === T.TOMBSTONE) tomb++;
618	        else if (t === T.SUNFLOWER) sunflower++;
619	      }
620	    }
621	    // SceneMetrics.cs:588-592/608-615：向日葵每株 −10 计入恶/血两族。
622	    //  num = −10，infectedSeed 种子（10xx 醉酒世界）时 num ×3 → 每株 −30——
623	    //  本仓无种子系统（恒非 infectedSeed）→ 恒 ×1
624	    evil += sunflower * -10; blood += sunflower * -10;
625	    // SceneMetrics.cs:648-662：神圣/邪恶/猩红两两互减后钳 ≥0
626	    const holyRaw = holy;
627	    holy -= evil; holy -= blood;
628	    evil -= holyRaw; blood -= holyRaw;
629	    this.zoneCounts = {
630	      evil: Math.max(0, evil), blood: Math.max(0, blood), holy: Math.max(0, holy),
631	      snow, jungle, mushroom, meteor,
632	      // GraveyardTileCount（SceneMetrics.cs:622-623/632-634）：85 计数 − 向日葵/2，钳 ≥0
633	      graveyard: Math.max(0, tomb - (sunflower >> 1)),
634	    };
635	  }
636	
637	  // ---- FindSpawnTile（L879-920）----
638	  /** GetSpawnRate（L383-668，单机非 remix 分支）：
639	   *  defaultSpawnRate=600 / defaultMaxSpawns=5（L6108/6110）。
640	   *  深度带/昼夜/附近怪分层/水蜡烛修正 + clamp（L655-662）。
641	   *  血月/日食/南瓜月（月事件覆盖见函数首分支）/和平蜡烛/向日葵/calmed 均已实现（:581-642）；
642	   *  隐身/仙女倍率未实现（依赖 stealth/luck 子系统，登记 docs/spawn-parity-gaps.md）。
643	   *  UnderworldLayer = maxTilesY-200(Main.cs:2863 属性表达式,精确非近似) */
644	  getSpawnRate(playerYpx: number, nearbySlots: number, waterCandle: boolean, sHeightPx: number,
645	    playerXpx = this.pX * TILE, peaceCandle = false, sunflower = false, calmed = false, battle = false,
646	    townNPCs = 0, dayTime = true, zoneEvil = false, bloodMoon = false): { spawnRate: number; maxSpawns: number } {
647	    // ZoneWaterCandle 先落字段（SetSpawnFlags L308 语义）：同一值既改刷怪率（:637/:650）
648	    // 也供 SpawnAnNPC 的 399/87/86 水蜡烛加重支——Game 每帧先 getSpawnRate 后 spawn
649	    this.zoneWaterCandle = waterCandle;
650	    // 月事件覆盖（L681-685）：南瓜月/霜月且玩家在地表（remix 省略）→
651	    // rate=20、max=⌊5×(2+0.3n)⌋（单人 11）；先于 invaders 覆盖（原版即此顺序）
652	    if (this.moonEvent && playerYpx < this.world.groundLevel * 16) {
653	      return { spawnRate: 20, maxSpawns: Math.floor(5 * (2 + 0.3 * 1)) };
654	    }
655	    // 入侵覆盖（L691-695）：rate=20（每帧 1/20 尝试），上限 5*(2+0.3n)（单人 11）。
656	    // 星璇塔 Zone 同走 invaders 语义（SetSpawnFlags :315-318 任一塔 Zone → invaders=true）
657	    if (this.invaders || this.lunar) {
658	      return { spawnRate: 20, maxSpawns: Math.floor(5 * (2 + 0.3 * 1)) };
659	    }
660	    let spawnRate = 600;
661	    let maxSpawns = 5;
662	    const w = this.world;
663	    // L389-392：困难模式 spawnRate×0.9 / maxSpawns+1——最先施加，后续修正全部叠在其上。
664	    // 直接读 world.flags（this.hardMode 要等 spawn() 才刷新，首帧会漏乘）
665	    if (w.flags.hardMode) {
666	      spawnRate = Math.floor(spawnRate * 0.9);
667	      maxSpawns += 1;
668	    }
669	    const underworldY = (w.store.h - 200) * 16;
670	    if (playerYpx > underworldY) {
671	      // L393-396：地狱 maxSpawns×2
672	      maxSpawns = Math.floor(maxSpawns * 2);
673	    } else if (playerYpx > w.rockLevel * 16 + sHeightPx) {
674	      // L402-407：洞穴层 spawnRate×0.4 / max×1.9
675	      spawnRate = Math.floor(spawnRate * 0.4);
676	      maxSpawns = Math.floor(maxSpawns * 1.9);
677	    } else if (playerYpx > w.groundLevel * 16 + sHeightPx) {
678	      // L418-422：地下层 spawnRate×0.5 / max×1.7
679	      spawnRate = Math.floor(spawnRate * 0.5);
680	      maxSpawns = Math.floor(maxSpawns * 1.7);
681	    } else if (!w.clock.isDay) {
682	      // L455-459：夜晚 spawnRate×0.6 / max×1.3；血月再 ×0.3/×1.8（L447-450）
683	      // （昼/夜直接读 clock，同 hardMode——this.dayTime 要等 spawn() 才刷新，首帧会漏判）
684	      spawnRate = Math.floor(spawnRate * 0.6);
685	      maxSpawns = Math.floor(maxSpawns * 1.3);
686	      if (w.clock.bloodMoon) {
687	        spawnRate = Math.floor(spawnRate * 0.3);
688	        maxSpawns = Math.floor(maxSpawns * 1.8);
689	      }
690	    } else if (w.clock.isDay && w.clock.eclipse) {
691	      // L458-461：日食白天 spawnRate×0.2 / max×1.9（血月同层级的 else-if 支）
692	      spawnRate = Math.floor(spawnRate * 0.2);
693	      maxSpawns = Math.floor(maxSpawns * 1.9);
694	    }
695	    // Zone 判定现取（原版每次从玩家 SceneMetrics 取，非上次生成残留 flag）：
696	    // 玩家中心窗口计数（0.5s 缓存近似，见 refreshZoneCounts），本函数每帧被调
697	    this.refreshZoneCounts(Math.floor(playerXpx / TILE), Math.floor(playerYpx / TILE));
698	    const zoneCorrupt = this.zoneCounts.evil >= 300;
699	    const zoneCrimson = this.zoneCounts.blood >= 300;
700	    const zoneSnow = this.zoneCounts.snow >= 1500;
701	    // 雨天雪原（L493-496，深度修正之后、地牢倍率之前）：ZoneSnow 且玩家在地表 →
702	    // max×(1+cloudAlpha) / rate×(1-cloudAlpha+1)/2（cloudAlpha=0 时为恒等变换）
703	    if (zoneSnow && playerYpx / TILE < w.groundLevel) {
704	      maxSpawns = Math.floor(maxSpawns * (1 + this.rainCloudAlpha));
705	      spawnRate = Math.floor(spawnRate * (1 - this.rainCloudAlpha + 1) / 2);
706	    }
707	    // 地牢→沙尘暴→地下沙漠→丛林→恶地→陨石 else-if 链（NPC.cs:504-544 1:1——
708	    // 互斥链，命中前支后支不再叠加；此前只移植了地牢一支）：
709	    //  地牢 ×0.3/×1.8（L504-505）——必须发生在 clamp（L661-664）之前，否则可产出
710	    //  max>15（旧实现放 clamp 后漏判）。
711	    //  沙尘暴（L507-511）hard?×0.4:×0.9 / hard?×1.5:×1.2。
712	    //  地下沙漠（L512-515）×0.2/×3（player.ZoneUndergroundDesert = SceneMetrics.cs:694，
713	    //  取 Game 每帧写入的 world.scene；测试直调无 scene 时按 false 处理）。
714	    //  丛林城镇阶梯（L516-538）townNPCs 0/1/2/≥3 → ×0.4/0.55/0.7/0.85 与
715	    //  ×1.5/1.4/1.3/1.2（城镇越大丛林越温和——镇住丛林刷怪的原版机制）。
716	    //  腐化/猩红（L539-542）×0.65/×1.3。陨石（L543-544）×0.4/×1.1
717	    const zoneJungle = this.zoneCounts.jungle >= 140;   // 与 setFlagsForChosenTile 同源计数
718	    const zoneMeteor = this.zoneCounts.meteor >= 75;
719	    const zoneUndergroundDesert = !!this.world.scene?.zoneUndergroundDesert;
720	    if (this.ZoneDungeon) {
721	      spawnRate = Math.floor(spawnRate * 0.3);
722	      maxSpawns = Math.floor(maxSpawns * 1.8);
723	    } else if (this.zoneSandstorm) {
724	      spawnRate = Math.floor(spawnRate * (w.flags.hardMode ? 0.4 : 0.9));
725	      maxSpawns = Math.floor(maxSpawns * (w.flags.hardMode ? 1.5 : 1.2));
726	    } else if (zoneUndergroundDesert) {
727	      spawnRate = Math.floor(spawnRate * 0.2);
728	      maxSpawns = Math.floor(maxSpawns * 3);
729	    } else if (zoneJungle) {
730	      if (townNPCs === 0) {
731	        spawnRate = Math.floor(spawnRate * 0.4);
732	        maxSpawns = Math.floor(maxSpawns * 1.5);
733	      } else if (townNPCs === 1) {
734	        spawnRate = Math.floor(spawnRate * 0.55);
735	        maxSpawns = Math.floor(maxSpawns * 1.4);
736	      } else if (townNPCs === 2) {
737	        spawnRate = Math.floor(spawnRate * 0.7);
738	        maxSpawns = Math.floor(maxSpawns * 1.3);
739	      } else {
740	        spawnRate = Math.floor(spawnRate * 0.85);
741	        maxSpawns = Math.floor(maxSpawns * 1.2);
742	      }
743	    } else if (zoneCorrupt || zoneCrimson) {
744	      spawnRate = Math.floor(spawnRate * 0.65);
745	      maxSpawns = Math.floor(maxSpawns * 1.3);
746	    } else if (zoneMeteor) {
747	      spawnRate = Math.floor(spawnRate * 0.4);
748	      maxSpawns = Math.floor(maxSpawns * 1.1);
749	    }
750	    // 神庙（L545-551 独立 if，不参与 else-if 互斥）：×0.8/×1.2（remix 再 ×0.4/×1.5 省略）。
751	    //  ZoneLihzhardTemple = 玩家所站格墙 87（SceneMetrics.cs:688）
752	    if (this.zoneLihzardTemple(Math.floor(playerXpx / TILE), Math.floor(playerYpx / TILE))) {
753	      spawnRate = Math.floor(spawnRate * 0.8);
754	      maxSpawns = Math.floor(maxSpawns * 1.2);
755	    }
756	    // 神圣深层（L556-559 独立 if）：ZoneHallow && 玩家深于 rockLayer×16+sHeight → ×0.65/×1.3
757	    if (this.zoneCounts.holy >= 125 && playerYpx > w.rockLevel * 16 + sHeightPx) {
758	      spawnRate = Math.floor(spawnRate * 0.65);
759	      maxSpawns = Math.floor(maxSpawns * 1.3);
760	    }
761	    // L583-591（无条件）：附近怪 <20%/40%/60%/80% 上限时 ×0.6/×0.7/×0.8/×0.9
762	    if (nearbySlots < maxSpawns * 0.2) spawnRate = Math.floor(spawnRate * 0.6);
763	    else if (nearbySlots < maxSpawns * 0.4) spawnRate = Math.floor(spawnRate * 0.7);
764	    else if (nearbySlots < maxSpawns * 0.6) spawnRate = Math.floor(spawnRate * 0.8);
765	    else if (nearbySlots < maxSpawns * 0.8) spawnRate = Math.floor(spawnRate * 0.9);
766	    // L592-604：地下中点以下/腐化/猩红再叠加（Zone 用上面现取值）
767	    if (playerYpx / TILE > (w.groundLevel + w.rockLevel) / 2 || zoneCorrupt || zoneCrimson) {
768	      if (nearbySlots < maxSpawns * 0.2) spawnRate = Math.floor(spawnRate * 0.7);
769	      else if (nearbySlots < maxSpawns * 0.4) spawnRate = Math.floor(spawnRate * 0.9);
770	    }
771	    // L617-620：镇静药水（calmed）×1.65 / ×0.6
772	    if (calmed) {
773	      spawnRate = Math.floor(spawnRate * 1.65);
774	      maxSpawns = Math.floor(maxSpawns * 0.6);
775	    }
776	    // L624-628：向日葵（buff 146 标志）×1.2 / ×0.8
777	    if (sunflower) {
778	      spawnRate = Math.floor(spawnRate * 1.2);
779	      maxSpawns = Math.floor(maxSpawns * 0.8);
780	    }
781	    // L632-635：战斗药水（enemySpawns）×0.5 / ×2
782	    if (battle) {
783	      spawnRate = Math.floor(spawnRate * 0.5);
784	      maxSpawns = Math.floor(maxSpawns * 2);
785	    }
786	    // L640-646：水蜡烛 spawnRate×0.75 / max×1.5；天空层再 ×0.5
787	    if (waterCandle) {
788	      spawnRate = Math.floor(spawnRate * 0.75);
789	      maxSpawns = Math.floor(maxSpawns * 1.5);
790	      if (playerYpx / TILE < w.groundLevel * 0.35) spawnRate = Math.floor(spawnRate * 0.5);
791	    } else if (peaceCandle) {
792	      // L645-648：和平蜡烛 ×1.3 / ×0.7（与水蜡烛互斥——原版 else if）
793	      spawnRate = Math.floor(spawnRate * 1.3);
794	      maxSpawns = Math.floor(maxSpawns * 0.7);
795	    }
796	    // L655-662：下限 spawnRate≥60，上限 maxSpawns≤15
797	    if (spawnRate < 60) spawnRate = 60;
798	    if (maxSpawns > 15) maxSpawns = 15;
799	    // L696：未杀骷髅王 rate=10（clamp 之后赋值，不受 ≥60 下限影响——守卫快速轮换）
800	    if (this.ZoneDungeon && !this.downedBoss3) spawnRate = 10;
801	    // ---- spawnFriendly 掷骰（NPC.cs:711-832;原版在 SetSpawnFlags 与 rate 同例程内）----
802	    // 外层门 :709 1:1：!invaders && ((!血月 && !南瓜月 && !霜月) || 白天) && 非日食白天
803	    //  && !腐化 && !猩红 && !陨石 && !旧军（旧军系统缺席恒 false;infectedSeed 变体省略;
804	    //  ZoneMeteor 与上面速率链同源的 zoneCounts 现取）。★此前漏 南瓜/霜月/日食/陨石 四门
805	    //  （事件/日食期小动物轮照跑）。
806	    // ★此前未移植:小动物链（SpawnAnNPC :2006 `else if (spawnFriendly)`）恒放行 →
807	    //  无城镇 NPC 也会满地兔鼠(甚至刷到浮空岛——原版岛边 townNPCs=0 永不出小动物)
808	    this.spawnFriendlyCycle = false;
809	    this.townNoWorms = false;
810	    if (!this.invaders && ((!bloodMoon && !this.moonEvent) || dayTime)
811	      && !(w.clock.eclipse && dayTime) && !zoneEvil && !(this.zoneCounts.meteor >= 75)) {
812	      const deep = playerYpx / TILE > w.h - 200;   // :711 player.Center.Y/16 > UnderworldLayer
813	      if (deep) {
814	        // 地狱侧(:713-763)：友好概率低；命中时 maxSpawns×0.5（:724/:741/:757——
815	        // 削减只在 friendly 命中分支内，未命中只放宽 spawnRate）。
816	        // 城镇 noWorms 掷骰（:717/:734/:750）在友好掷骰**之前**（原版同序）
817	        if (townNPCs === 1) {
818	          if (this.rateRng() < 1 / 2) this.townNoWorms = true;              // :717-720
819	          if (this.rateRng() < 1 / 10) { this.friendlyHit(); maxSpawns = Math.floor(maxSpawns * 0.5); } // :722-727
820	          else spawnRate = Math.floor(spawnRate * 1.25);
821	        } else if (townNPCs === 2) {
822	          if (this.rateRng() >= 1 / 4) this.townNoWorms = true;             // :734-737 Next(4)!=0
823	          if (this.rateRng() < 1 / 5) { this.friendlyHit(); maxSpawns = Math.floor(maxSpawns * 0.5); } // :736-743
824	          else spawnRate = Math.floor(spawnRate * 1.5);
825	        } else if (townNPCs >= 3) {
826	          if (this.rateRng() >= 1 / 10) this.townNoWorms = true;            // :750-753 Next(10)!=0
827	          if (this.rateRng() < 1 / 3) { this.friendlyHit(); maxSpawns = Math.floor(maxSpawns * 0.5); } // :753-759
828	          else spawnRate = Math.floor(spawnRate * 2);
829	        }
830	      } else {
831	        // 地表/洞穴侧(:765-832)：高友好率；命中时 maxSpawns×0.6（:782/:805/:821）；
832	        // townNPCs==0 → 永不友好(不出小动物)。
833	        // 城镇 noWorms 无条件置位（:767/:792/:814——地表侧城镇 ≥1 恒不出蠕虫）
834	        // 墓地段（:770-778/:793-800/:815-822）：ZoneGraveyard && (!ZonePeaceCandle || 1/3)
835	        //  → spawnRate 放宽（×1.66/×2.33/×3）且友好掷骰概率骤降（1/9 / 1/6 / 1/3）——
836	        //  墓地有城镇 NPC 也会高密度刷怪（墓地小动物只有蛆/鼠，:2008-2014）。
837	        //  gy 旗掷骰 RNG 消费序（:772 原文 Next(3)==0）：和平蜡烛在场时 || 短路不掷
838	        //  （恒走非墓地支），不在场才消费一掷；else-if 链每次调用只进一段，gy 每
839	        //  次 getSpawnRate 至多一掷
840	        const gy = this.ZoneGraveyard && (!peaceCandle || this.rateRng() < 1 / 3);
841	        if (townNPCs === 1) {
842	          this.townNoWorms = true;                                          // :767
843	          if (gy) {
844	            spawnRate = Math.floor(spawnRate * 1.66);                       // :771
845	            if (this.rateRng() < 1 / 9) { this.friendlyHit(); maxSpawns = Math.floor(maxSpawns * 0.6); } // :773-775
846	          } else if (this.rateRng() < 1 / 3) { this.friendlyHit(); maxSpawns = Math.floor(maxSpawns * 0.6); } // :779-783
847	          else spawnRate = Math.floor(spawnRate * 2);
848	        } else if (townNPCs === 2) {
849	          this.townNoWorms = true;                                          // :792
850	          if (gy) {
851	            spawnRate = Math.floor(spawnRate * 2.33);                       // :794
852	            if (this.rateRng() < 1 / 6) { this.friendlyHit(); maxSpawns = Math.floor(maxSpawns * 0.6); } // :796-798
853	          } else if (this.rateRng() < 2 / 3) { this.friendlyHit(); maxSpawns = Math.floor(maxSpawns * 0.6); } // :802-806
854	          else spawnRate = Math.floor(spawnRate * 3);
855	        } else if (townNPCs >= 3) {
856	          this.townNoWorms = true;                                          // :814
857	          if (gy) {
858	            spawnRate = Math.floor(spawnRate * 3);                          // :816
859	            if (this.rateRng() < 1 / 3) { this.friendlyHit(); maxSpawns = Math.floor(maxSpawns * 0.6); } // :818-820
860	          } else {
861	            this.friendlyHit();   // :826-828 非 ftw 恒友好(专家 1/30 例外未实装)
862	            maxSpawns = Math.floor(maxSpawns * 0.6); // :830 无条件削减（专家例外轮也削）
863	          }
864	        }
865	      }
866	    }
867	    // L834-838（友好块之后、return 之前）：非友好轮 && RollOnlyBadLuckExtreme(50)==0
868	    //  → spawnRate×0.85 / maxSpawns×1.15（"厄运轮"怪更密）。走 Luck.RollOnlyBadLuckExtreme
869	    //  （Luck.ts,luck 0 中性时即 Next(50)==0;正运无加成、负运收窄——与原版同式）
870	    if (!this.spawnFriendlyCycle && rollOnlyBadLuckExtreme(this.playerLuck, 50, () => this.rateRng()) === 0) {
871	      spawnRate = Math.floor(spawnRate * 0.85);
872	      maxSpawns = Math.floor(maxSpawns * 1.15);
873	    }
874	    return { spawnRate, maxSpawns };
875	  }
876	  /** friendly 命中（:723/:740/:756/:804/:828）：只置 spawnFriendlyCycle；
877	   *  maxSpawns 削减（地狱 ×0.5 / 地表 ×0.6，且 town≥3 地表无条件）在分支就地执行 */
878	  private friendlyHit(): void {
879	    this.spawnFriendlyCycle = true;
880	  }
881	  private rateRng(): number {
882	    return Math.random();
883	  }
884	
885	  /** 狙击镜扩圈系数（0=关；1.25/1.5/2.0——Game 每帧求值写入） */
886	  scopeNum3 = 0;
887	
888	  /** FindSpawnTile（L879-927）+ GetSpawnArea（L841-877）1:1：
889	   *  spawnArea = 玩家 ±(0.7×全屏格)（均匀取点，不是环带外扩！），
890	   *  safeArea = 玩家 ±(0.52×全屏格)——生成点必须落在画面外（!safeArea.Contains）。
891	   *  viewHalfW/H = 半屏格数 → 0.7×全屏 = ×1.4 半屏；0.52×全屏 = ×1.04 半屏 */
892	  private findSpawnTile(rng: RNG, viewHalfW: number, viewHalfH: number): boolean {
893	    const st = this.world.store;
894	    const px = this.pX, py = this.pY;
895	    // 狙击镜扩圈（GetSpawnArea :846-862）：手持 1254 狙击枪/1299 步枪镜 或装备 scope
896	    //  → 生成区与 safe 区各加 viewHalf/num3（num3=1.25 双持/1.5 单件/2.0 纯装备）
897	    const sc = this.scopeNum3 > 0 ? Math.floor(viewHalfW / this.scopeNum3) : 0;
898	    const scY = this.scopeNum3 > 0 ? Math.floor(viewHalfH / this.scopeNum3) : 0;
899	    const rangeX = Math.max(1, Math.floor(viewHalfW * 1.4)) + sc;
900	    const rangeY = Math.max(1, Math.floor(viewHalfH * 1.4)) + scY;
901	    const safeX = Math.max(1, Math.floor(viewHalfW * 1.04)) + sc;
902	    const safeY = Math.max(1, Math.floor(viewHalfH * 1.04)) + scY;
903	    // WorldUtils.ClampToWorld
904	    const areaL = Math.max(2, px - rangeX), areaR = Math.min(st.w - 3, px + rangeX);
905	    const areaT = Math.max(2, py - rangeY), areaB = Math.min(st.h - 3, py + rangeY);
906	    for (let attempt = 0; attempt < 50; attempt++) {
907	      const tx = rng.int(areaL, areaR);
908	      let ty = rng.int(areaT, areaB);
909	      // L886-888：点在实心格 或 (非 ignoreSafeWalls 且带房屋墙) → 重试
910	      //  （房屋内不刷怪的主守卫;ignoreSafeWalls :315-319 仅星璇四塔 Zone 置位——
911	      //   塔战期间允许穿房屋墙刷怪,普通入侵不置位）
912	      if (st.isSolid(tx, ty)) continue;
913	      if (!this.ignoreSafeWalls && WALL_HOUSE.has(st.wall[st.idx(tx, ty)])) continue;
914	      this.skyMob = false;
915	      // L890-897：天空怪选点门——!invaders && y<worldSurface×0.35 && !spawnFriendly &&
916	      //  (x<0.45w || x>0.55w || hardMode)；L898-903 第二支：!invaders && y<worldSurface×0.45
917	      //  && !spawnFriendly && hardMode && 1/10（困难模式加宽的第二天空层，此前缺失）。
918	      //  原版"两侧 45% 带外"隐含不变量 = 浮空岛只在两侧、中央带无高空地面；此处沿用
919	      //  本仓既定的"落脚面上方两格无墙"露天判据（兼容含中央浮空岛的存量世界，否则
920	      //  中央岛会被当地表刷僵尸/水母），并补齐 !invaders/!spawnFriendly/困难第二带三门
921	      const openAir = st.wall[st.idx(tx, ty - 1)] === 0 && st.wall[st.idx(tx, ty - 2)] === 0;
922	      if (!this.invaders && !this.spawnFriendlyCycle && ty < this.world.groundLevel * 0.35 && openAir
923	        && (tx < st.w * 0.45 || tx > st.w * 0.55 || this.world.flags.hardMode)) {
924	        this.skyMob = true;
925	      } else if (!this.invaders && !this.spawnFriendlyCycle && openAir
926	        && ty < this.world.groundLevel * 0.45 && this.world.flags.hardMode && rng.next() < 0.1) {
927	        this.skyMob = true;
928	      } else {
929	        // L900-906：向下找第一个实心格 = 落脚面（扫描上限 = spawnArea.Bottom，非世界底）
930	        let j = ty;
931	        while (j < areaB && !st.isSolid(tx, j)) j++;
932	        if (j >= areaB) continue;
933	        ty = j;
934	      }
935	      // L910：safeArea 内（画面内）一律拒绝 + HasTileSpawnSpace 落点空间校验
936	      if (Math.abs(tx - px) < safeX && Math.abs(ty - py) < safeY) continue;
937	      if (!this.hasTileSpawnSpace(tx, ty)) continue;
938	      // L911：xRange = 落脚点在 safeArea 横向范围内（原版传给 SpawnAnNPC 的水生成判定）
939	      this.xRange = tx >= px - safeX && tx < px + safeX;
940	      this.spawnTileX = tx; this.spawnTileY = ty;
941	      return true;
942	    }
943	    return false;
944	  }
945	
946	  /** HasTileSpawnSpace（L5306+5330）：落脚格上方 spawnSpaceX=2 × spawnSpaceY=3 区域
947	   *  逐格 CanSpawnInTile——非实心且非岩浆（防刷进实心/岩浆里） */
948	  private hasTileSpawnSpace(tx: number, ty: number): boolean {
949	    const st = this.world.store;
950	    for (let dx = -1; dx <= 0; dx++) {
951	      for (let dy = -3; dy <= -1; dy++) {
952	        const x = tx + dx, y = ty + dy;
953	        if (x < 0 || y < 0 || x >= st.w || y >= st.h) return false;
954	        const i = st.idx(x, y);
955	        if (st.isSolid(x, y)) return false;
956	        if (st.liquid[i] > 0 && st.liquidType[i] === 2) return false;
957	      }
958	    }
959	    return true;
960	  }
961	
962	  /** 联机远端玩家位置注入（px，玩家碰撞盒中心）：Game.trySpawnEnemy 每帧赋值一行。
963	   *  原版 CheckNotSpawningOnScreen（L5344-5366）遍历全部 255 名玩家——与任一活跃玩家
964	   *  的扩展屏相交即拒，不是只查本地玩家；否则分屏/异地队友眼前会凭空刷怪 */
965	  static remotePlayers: Array<{ x: number; y: number }> = [];
966	
967	  /** CheckNotSpawningOnScreen（L5344-5366）像素级双保险：
968	   *  落脚格 16×16 与"玩家屏幕 ±safeRange"矩形相交 → 拒绝。
969	   *  注意原版单位混用（L5354）：safeRangeX/Y 是格数但直接当像素偏移加——实际外扩仅 ~2 格 */
970	  private checkNotSpawningOnScreen(px: number, py: number, viewHalfW: number, viewHalfH: number): boolean {
971	    const sW = viewHalfW * 2 * TILE, sH = viewHalfH * 2 * TILE;
972	    const safePxX = viewHalfW * 1.04, safePxY = viewHalfH * 1.04; // 格数直接当像素（原版 L5354 原样）
973	    const tX = this.spawnTileX * TILE, tY = this.spawnTileY * TILE;
974	    const clear = (cx: number, cy: number): boolean => {
975	      const rectX = cx - sW / 2 - safePxX, rectY = cy - sH / 2 - safePxY;
976	      const rectW = sW + safePxX * 2, rectH = sH + safePxY * 2;
977	      return !(tX < rectX + rectW && tX + TILE > rectX && tY < rectY + rectH && tY + TILE > rectY);
978	    };
979	    if (!clear(px, py)) return false;
980	    for (const rp of VanillaSpawner.remotePlayers) {
981	      if (!clear(rp.x, rp.y)) return false;
982	    }
983	    return true;
984	  }
985	
986	  /** 向上 50 格找“干格 + 下两格非实心”的洞隙线（海洋段 L1711-1718 / L1737-1752、
987	   *  水池段 L1844-1852 四处共用的扫描体）：命中返回干格 y+2 并按 L1719-1722 /
988	   *  L1853-1856 钳到 spawnTileY，找不到返回 -1 */
989	  private findDryGapY(spawnTileY: number): number {
990	    const st = this.world.store;
991	    for (let y = spawnTileY - 1; y > spawnTileY - 50 && y >= 0; y--) {
992	      if (st.liquid[st.idx(this.spawnTileX, y)] === 0
993	        && !st.isSolid(this.spawnTileX, y) && !st.isSolid(this.spawnTileX, y + 1)
994	        && !st.isSolid(this.spawnTileX, y + 2)) {
995	        return Math.min(y + 2, spawnTileY);
996	      }
997	    }
998	    return -1;
999	  }
1000	
1001	  /** SpawnHornet（NPC.cs:5189-5255 1:1）：Next(8) 选族——
1002	   *  case0-4 黄蜂族 231-235（各 1/4 小 -2k/大 -2k+1 变体）；default(case5-7) 蜂刺族 42 */
1003	  private spawnHornet(x: number, y: number, rng: RNG): Enemy | null {
1004	    const v = rng.int(0, 8);
1005	    const table: Array<[number, number, number]> = [
1006	      [-56, -57, 231], [-58, -59, 232], [-60, -61, 233],
1007	      [-62, -63, 234], [-64, -65, 235],
1008	      [-16, -17, 42],
1009	    ];
1010	    const row = table[Math.min(v, 5)];
1011	    if (rng.next() < 0.25) return this.spawnNPC(x, y, row[0], rng);
1012	    if (rng.next() < 0.25) return this.spawnNPC(x, y, row[1], rng);
1013	    return this.spawnNPC(x, y, row[2], rng);
1014	  }
1015	
1016	  // ---- 月事件选怪（霜月 NPC.cs:2714-3132 / 南瓜月 :3134-3455，1:1） ----
1017	  /** CountNPCS（场内存活数）：activeIds 只去重，计数走 Game 传入的 counts 表 */
1018	  private moonCount(id: number): number {
1019	    return this.moonEvent?.counts.get(id) ?? 0;
1020	  }
1021	
1022	  /** 霜月选怪：返回 netId；0 = 本帧不刷（原版空过，勿加兜底——14 波三 Boss 唯一门
1023	   *  全被占时不刷是原版行为）。任意波先掷 1/30 && CountNPCS(341)<4 → 礼物窃贼 341。 */
1024	  private pickFrostMoonSpawn(wave: number, rng: RNG): number {
1025	    const N = (n: number) => rng.next() < 1 / n;
1026	    const C = (id: number) => this.moonCount(id);
1027	    if (N(30) && C(341) < 4) return 341;
1028	    if (wave >= 20) {
1029	      const num45 = rng.int(0, 2);   // 原版在 bossCap 检查前先掷（RNG 流对齐）
1030	      if (!this.moonBossCap) {
1031	        if (num45 === 0) return 345;   // 冰雪女王
1032	        if (num45 === 1) return 346;   // 圣诞坦克
1033	        return 344;                    // 常世吼
1034	      }
1035	      return 0;
1036	    }
1037	    if (wave >= 19) {
1038	      if (N(10) && C(345) < 4) return 345;
1039	      if (N(10) && C(346) < 5) return 346;
1040	      if (N(10) && C(344) < 7) return 344;
1041	      return 343;                      // 雪怪兜底
1042	    }
1043	    if (wave >= 18) {
1044	      if (N(10) && C(345) < 3) return 345;
1045	      if (N(10) && C(346) < 4) return 346;
1046	      if (N(10) && C(344) < 6) return 344;
1047	      if (N(3)) return 348;            // 胡桃夹子
1048	      if (N(3)) return 351;            // 坎卜斯
1049	      return 343;
1050	    }
1051	    if (wave >= 17) {
1052	      if (N(10) && C(345) < 2) return 345;
1053	      if (N(10) && C(346) < 3) return 346;
1054	      if (N(10) && C(344) < 5) return 344;
1055	      if (N(4)) return 347;            // 玩具直升机
1056	      if (N(2)) return 351;
1057	      return 343;
1058	    }
1059	    if (wave >= 16) {
1060	      if (N(10) && C(345) < 2) return 345;
1061	      if (N(10) && C(346) < 2) return 346;
1062	      if (N(10) && C(344) < 4) return 344;
1063	      if (N(2)) return 352;            // 弗洛科
1064	      return 343;
1065	    }
1066	    if (wave >= 15) {
1067	      if (N(10) && C(345) < 1) return 345;
1068	      if (N(10) && C(346) < 2) return 346;
1069	      if (N(10) && C(344) < 3) return 344;
1070	      if (N(3)) return 347;
1071	      return 343;
1072	    }
1073	    switch (wave) {
1074	      case 14:
1075	        if (N(10) && C(345) < 1) return 345;
1076	        if (N(10) && C(346) < 1) return 346;
1077	        if (N(10) && C(344) < 1) return 344;
1078	        if (N(3)) return 343;
1079	        return 0;   // 原版 case 14 无 else 兜底：全落空即空刷（勿修）
1080	      case 13:
1081	        if (N(10) && C(345) < 1) return 345;
1082	        if (N(10) && C(346) < 1) return 346;
1083	        if (N(3)) return 352;
1084	        if (N(6)) return 343;
1085	        if (N(3)) return 342;
1086	        return 347;
1087	      case 12:
1088	        if (N(10) && C(345) < 1) return 345;
1089	        if (N(10) && C(344) < 1) return 344;
1090	        if (N(8)) return 343;
1091	        if (N(3)) return 342;
1092	        return rng.int(338, 340);       // Main.rand.Next(338,341)
1093	      case 11:
1094	        if (N(10) && C(345) < 1) return 345;
1095	        if (N(6)) return 352;
1096	        if (N(2)) return 342;
1097	        return rng.int(338, 340);
1098	      case 10:
1099	        if (N(10) && C(346) < 1) return 346;
1100	        if (N(10) && C(344) < 2) return 344;
1101	        if (N(6)) return 351;
1102	        if (N(3)) return 348;
1103	        if (N(3)) return 347;
1104	        return rng.int(338, 340);
1105	      case 9:
1106	        if (N(10) && C(346) < 1) return 346;
1107	        if (N(10) && C(344) < 1) return 344;
1108	        if (N(2)) return 348;
1109	        if (N(3)) return 347;
1110	        return 342;
1111	      case 8:
1112	        if (N(10) && C(346) < 1) return 346;
1113	        if (N(8)) return 351;
1114	        if (N(3)) return 348;
1115	        if (N(3)) return 347;
1116	        return 350;                     // 精灵弓手
1117	      case 7:
1118	        if (N(10) && C(346) < 1) return 346;
1119	        if (N(3)) return 342;
1120	        if (N(4)) return 350;
1121	        return rng.int(338, 340);
1122	      case 6:
1123	        if (N(10) && C(344) < 2) return 344;
1124	        if (N(4)) return 347;
1125	        if (N(2)) return 348;
1126	        return 350;
1127	      case 5:
1128	        if (N(10) && C(344) < 1) return 344;
1129	        if (N(4)) return 350;
1130	        if (N(8)) return 348;
1131	        return rng.int(338, 340);
1132	      case 4:
1133	        if (N(10) && C(344) < 1) return 344;
1134	        if (N(4)) return 350;
1135	        if (N(3)) return 342;
1136	        return rng.int(338, 340);
1137	      case 3:
1138	        if (N(8)) return 348;
1139	        if (N(4)) return 350;
1140	        if (N(3)) return 342;
1141	        return rng.int(338, 340);
1142	      case 2:
1143	        if (N(3)) return 350;
1144	        return rng.int(338, 340);
1145	      default:                           // wave 1
1146	        if (N(3)) return 342;            // 姜饼人
1147	        return rng.int(338, 340);        // 精灵僵尸
1148	    }
1149	  }
1150	
1151	  /** 南瓜月选怪：返回 netId；0 = 本帧不刷（19 波 bossCap 占满后可能空刷，原版行为勿修）。
1152	   *  注意 wave 15-18 首支是独立 if（原版命中后仍会落入后续 else-if 链再判一次；
1153	   *  单返回值实现取首个命中即返回，语义等价） */
1154	  private pickPumpkinMoonSpawn(wave: number, rng: RNG): number {
1155	    const N = (n: number) => rng.next() < 1 / n;
1156	    const C = (id: number) => this.moonCount(id);
1157	    if (wave >= 20) {
1158	      if (!this.moonBossCap) {
1159	        if (N(2) && C(327) < 2) return 327;                 // 南瓜王
1160	        if (rng.next() >= 1 / 3 && C(325) < 2) return 325;  // Next(3)!=0 → 悲木
1161	        if (C(315) < 3) return 315;                          // 无头骑士
1162	      }
1163	      return 0;
1164	    }
1165	    switch (wave) {
1166	      case 19:
1167	        if (N(5) && C(327) < 2) return 327;
1168	        if (N(5) && C(325) < 2) return 325;
1169	        if (!this.moonBossCap && C(315) < 5) return 315;
1170	        return 0;   // 原版 case 19 无 else：三支全落空即空刷（勿修）
1171	      case 18:
1172	        if (N(7) && C(327) < 2) return 327;
1173	        if (N(7) && C(325) < 2) return 325;
1174	        if (N(7) && C(315) < 3) return 315;
1175	        return 330;                      // 胡闹鬼
1176	      case 17:
1177	        if (N(7) && C(327) < 2) return 327;
1178	        if (N(7) && C(325) < 2) return 325;
1179	        if (N(7) && C(315) < 2) return 315;
1180	        if (N(3)) return 330;
1181	        return 329;                      // 地狱犬
1182	      case 16:
1183	        if (N(10) && C(327) < 2) return 327;
1184	        if (N(10) && C(315) < 2) return 315;
1185	        if (N(6)) return 330;
1186	        if (N(3)) return 329;
1187	        return 326;                      // 树怪
1188	      case 15:
1189	        if (N(10) && C(327) < 1) return 327;
1190	        if (N(7) && C(325) < 2) return 325;
1191	        if (N(5)) return 330;
1192	        if (N(3)) return 326;
1193	        return rng.int(305, 314);        // 稻草人 Next(305,315)
1194	      case 14:
1195	        if (N(10) && C(327) < 1) return 327;
1196	        if (N(7) && C(325) < 2) return 325;
1197	        if (N(10) && C(315) < 1) return 315;
1198	        if (N(10)) return 330;
1199	        if (N(7)) return 329;
1200	        if (N(3)) return 326;
1201	        return rng.int(305, 314);
1202	      case 13:
1203	        if (N(7) && C(325) < 2) return 325;
1204	        if (N(10) && C(315) < 2) return 315;
1205	        if (N(6)) return 330;
1206	        if (N(3)) return 329;
1207	        return 326;
1208	      case 12:
1209	        if (N(5) && C(327) < 1) return 327;
1210	        return 330;
1211	      case 11:
1212	        if (N(7) && C(325) < 2) return 325;
1213	        if (N(3)) return 330;
1214	        return 326;
1215	      case 10:
1216	        if (N(10) && C(327) < 1) return 327;
1217	        if (N(3)) return 329;
1218	        return rng.int(305, 314);
1219	      case 9:
1220	        if (N(10) && C(325) < 2) return 325;
1221	        if (N(8)) return 330;
1222	        if (N(5)) return 329;
1223	        if (N(2)) return 326;
1224	        return rng.int(305, 314);
1225	      case 8:
1226	        if (N(8) && C(315) < 2) return 315;
1227	        if (N(4)) return 330;
1228	        return 329;
1229	      case 7:
1230	        if (N(7) && C(325) < 2) return 325;
1231	        if (N(4)) return 330;
1232	        return 329;
1233	      case 6:
1234	        if (N(7) && C(325) < 2) return 325;
1235	        if (N(2)) return 326;
1236	        return rng.int(305, 314);
1237	      case 5:
1238	        if (N(10) && C(315) < 1) return 315;
1239	        return 329;
1240	      case 4:
1241	        // 原版怪癖（NPC.cs:3421）：判定是 !AnyNPCs(325)（悲木唯一）却刷 330（胡闹鬼）
1242	        // ——疑似复制粘贴笔误，照抄源码不"修"
1243	        if (N(8) && C(325) < 1) return 330;
1244	        if (N(2)) return 326;
1245	        return rng.int(305, 314);
1246	      case 3:
1247	        if (N(3)) return 329;
1248	        return 326;
1249	      case 2:
1250	        if (N(3)) return 326;
1251	        return rng.int(305, 314);
1252	      default:                           // wave 1
1253	        return rng.int(305, 314);        // 稻草人
1254	    }
1255	  }
1256	
1257	  // ---- SpawnAnNPC（L1186-5144）——肉前分支 1:1，hardMode 分支保留 ----
1258	  private spawnAnNPC(rng: RNG): Enemy | null {
1259	    const st = this.world.store;
1260	    const x = this.spawnTileX * TILE + 8;
1261	    const y = this.spawnTileY * TILE;
1262	    const N = (n: number) => rng.next() < 1 / n;  // Main.rand.Next(n)==0
1263	    const hardMode = this.hardMode;
1264	    // Main.expertMode（Main.cs:2762：Difficulty>=Expert；getGoodWorld 抬档同样成立）——
1265	    // 专家持械僵尸变体（:4565/:4624/:4644）与各 AI 专家分支的门
1266	    const expert = mainExpertMode(this.world);
1267	    const t = this.spawnTileType;
1268	    // SetSpawnFlags L709：日食白天关闭小动物段（(!eclipse || !dayTime) 门）——
1269	    // 小动物块（下方 gem 支 + 地表森林块）须跳过
1270	    const friendlyBlocked = this.world.clock.eclipse && this.dayTime;
1271	    const D = (id: number) => this.spawnNPC(x, y, id, rng);
1272	    const any = (id: number) => this.activeIds.has(id);
1273	    // GetZombieSettings（L1193 调用，L5501：Next(7)）——地表夜最终僵尸 style，
1274	    // 原版在函数入口 roll（此处同位置，保持后续 RNG 流顺序一致）
1275	    this.zombieStyle = rng.int(0, 6);
1276	    // GetZombieSettings L5499-5514：torchZombieChance 基础 12；
1277	    //  playerHasStartingHealth（L327：statLifeMax ≤ 100）→ 5 − numberOfActivePlayers/2
1278	    //  （下限 2；活跃玩家数未跟踪 → 单人取 1）。skyblock 的 spawnArmedZombies=false
1279	    //  只影响 591 持械变体，不影响本概率门
1280	    this.torchZombieChance = this.playerLifeMax > 0 && this.playerLifeMax <= 100
1281	      ? Math.max(2, 5 - Math.floor(1 / 2)) : 12;
1282	
1283	    // ---- 星璇塔 Zone（NPC.cs:1204-1289：SpawnAnNPC 链**第一**分支——原版先于
1284	    //  天空怪/入侵/月事件段；逐塔 SelectRandom 权重表 + CountNPCS 上限重掷，1:1）----
1285	    if (this.lunar) {
1286	      const z = this.lunar.zone;
1287	      const C = (id: number) => this.lunar!.counts.get(id) ?? 0;
1288	      const pick = (arr: number[]) => arr[rng.int(0, arr.length - 1)];   // Utils.SelectRandom
1289	      if (z.nebula) {
1290	        // 星云（L1204-1229）：424×3/423×3/421×3/420×2；上限 424<3、423<3、420<3（421 无上限）
1291	        let id = 0;
1292	        for (;;) {
1293	          id = pick([424, 424, 424, 423, 423, 423, 421, 421, 421, 420, 420]);
1294	          if (id === 424 && C(424) >= 3) continue;
1295	          if (id === 423 && C(423) >= 3) continue;
1296	          if (id === 420 && C(420) >= 3) continue;
1297	          break;
1298	        }
1299	        if (id !== 0) return D(id);
1300	      } else if (z.vortex) {
1301	        // 星旋（L1230-1255）：429×4/427×2/425×2/426×1；上限 425<3、426<3、429<4
1302	        let id = 0;
1303	        for (;;) {
1304	          id = pick([429, 429, 429, 429, 427, 427, 425, 425, 426]);
1305	          if (id === 425 && C(425) >= 3) continue;
1306	          if (id === 426 && C(426) >= 3) continue;
1307	          if (id === 429 && C(429) >= 4) continue;
1308	          break;
1309	        }
1310	        if (id !== 0) return D(id);
1311	      } else if (z.stardust) {
1312	        // 星尘（L1256-1263）：411×3/409×2/407/402/405 各 1，无上限
1313	        return D(pick([411, 411, 411, 409, 409, 407, 402, 405]));
1314	      } else if (z.solar) {
1315	        // 日耀（L1264-1289）：518/419/418/412/417/416/415 各 1；掷中 418 再 1/2 重选
1316	        //  {415,416,419,417}；上限 518<2、412<1（千足蜈蚣场内唯一）
1317	        let id = 0;
1318	        for (;;) {
1319	          id = pick([518, 419, 418, 412, 417, 416, 415]);
1320	          if (id === 418 && rng.int(0, 1) === 0) id = pick([415, 416, 419, 417]);
1321	          if (id === 518 && C(518) >= 2) continue;
1322	          if (id === 412 && C(412) >= 1) continue;
1323	          break;
1324	        }
1325	        if (id !== 0) return D(id);
1326	      }
1327	    }
1328	
1329	    // ---- 天空怪（原版 NPC.cs:1290-1331：else-if 链最前、invaders 之前——
1330	    //  skyMob 优先于入侵分支；肉前 = 兜底鸟妖 48，困难 = 1/10 飞龙 87（场内唯一））----
1331	    if (this.skyMob) {
1332	      // 火星入侵期间天空怪位出无人机（L1295-1297：invaders && invasionType==4 → 388）
1333	      if (this.invaders && this.world.invasionType === 4) return D(388);
1334	      // 火星探测器 399（L1302-1305）：困难+已败石巨人,首次未败火星 1/8 否则 1/30,
1335	      // 场上无 399;flag5 的 skyBehindPlayer/AnyDanger 上下文本仓未跟踪,以 skyMob+带外
1336	      // 距中央 >1/3 近似（探测器本就只在高空两侧刷出）
1337	      if (hardMode && this.world.flags['downed_245'] && !any(399)
1338	        && Math.abs(this.spawnTileX - this.world.store.w / 2) / (this.world.store.w / 2) > 0.33
1339	        && (N(this.world.flags['downedMartians'] ? 30 : 8) || N(30))) {
1340	        return D(399);
1341	      }
1342	      // L1316：飞龙 87——hard && 场上无 87 && !noWorms（房屋内不出蠕虫门，此前缺失）&& 1/10
1343	      if (hardMode && !any(87) && !this.noWorms && N(10)) return D(87);
1344	      // L1325：绑缚紫史莱姆 686——!unlockedSlimePurpleSpawn && RollLuck(25) && 场上无 686。
1345	      //  unlockedSlimePurpleSpawn（Main 静态，碰过 687/686 解锁链置位）本仓未跟踪 → 恒 false；
1346	      //  686 无 vanilla-npcs.json 条目 → fromVanilla null 静默丢弃（同 473-476 先例，登记台账）
1347	      if (!UNLOCKED_SLIME_PURPLE_SPAWN && N(25) && !any(686)) return D(686);
1348	      return D(48);
1349	    }
1350	    // ---- 入侵分支（L1333-1401：else if (invaders)，与普通链互斥）----
1351	    if (this.invaders) {
1352	      const it = this.world.invasionType;
1353	      if (it === 1) {
1354	        // 哥布林（L1335-1360）：召唤师(1/30,困难,唯一)→法师→小兵→弓手→盗贼→兜底战士
1355	        if (hardMode && !any(471) && N(30)) return D(471);
1356	        if (N(9)) return D(29);
1357	        if (N(5)) return D(26);
1358	        if (N(3)) return D(111);
1359	        if (N(3)) return D(27);
1360	        return D(28);
1361	      }
1362	      if (it === 2) {
1363	        // 雪人军团（L1362-1372）：雪球怪 1/7 → 黑帮雪人 1/3 → 兜底 刺客雪人
1364	        if (N(7)) return D(145);
1365	        if (N(3)) return D(143);
1366	        return D(144);
1367	      }
1368	      if (it === 3) {
1369	        // 海盗（L1377-1401）：
1370	        // 491 荷兰飞盗船（L1379-1382）：进度>50%（size<start/2）&& 1/20 && 场上无 491 &&
1371	        //   净空（spawnTileX±20 × spawnTileY-40..-10 无实心，越界即实心）→
1372	        //   落点 (spawnTileX*16+8, (spawnTileY-10)*16)（Bottom 锚，比地面怪高 10 格）
1373	        // 船长(1/30,唯一)→弩手→鹦鹉→神枪手→海盗→兜底 甲板水手
1374	        if (this.world.invasionSize < this.world.invasionSizeStart / 2 && N(20) && !any(491)) {
1375	          let clear = true;
1376	          for (let cx0 = this.spawnTileX - 20; cx0 <= this.spawnTileX + 20 && clear; cx0++) {
1377	            for (let cy0 = this.spawnTileY - 40; cy0 <= this.spawnTileY - 10; cy0++) {
1378	              if (cx0 < 0 || cx0 >= st.w || cy0 < 0 || cy0 >= st.h - 40 || st.isSolid(cx0, cy0)) {
1379	                clear = false; break;
1380	              }
1381	            }
1382	          }
1383	          if (clear) return this.spawnNPC(x, (this.spawnTileY - 10) * TILE, 491, rng);
1384	        }
1385	        if (N(30) && !any(216)) return D(216);
1386	        if (N(11)) return D(215);
1387	        if (N(9)) return D(252);
1388	        if (N(7)) return D(214);
1389	        if (N(3)) return D(213);
1390	        return D(212);
1391	      }
1392	      if (it === 4) {
1393	        // 火星疯狂（L1408-1463）。flag6 = 进度≥30% 且场上无飞碟（1/45 或高档位 1/20 出 395）;
1394	        // num7=Next(7): ≥6 → 骑手 390/工程师 386 二选;≥4 → 炮手 382×2/无人机 388/扰脑者 381;
1395	        // <4 → 灰兵 385/电侠 389/军官 383,3/4 概率出火星行者 520（场上唯一,否则重掷）
1396	        const prog = (this.world.invasionSizeStart - this.world.invasionSize)
1397	          / (this.world.invasionSizeStart || 1);
1398	        const saucerOk = prog >= 0.3 && !any(395);
1399	        const num7 = rng.int(0, 6);
1400	        if (N(45) && saucerOk) return D(395);
1401	        if (num7 >= 6) {
1402	          if (N(20) && saucerOk) return D(395);
1403	          return D(rng.int(0, 1) === 0 ? 390 : 386);
1404	        }
1405	        if (num7 >= 4) {
1406	          const r9 = rng.int(0, 4);
1407	          return D(r9 < 2 ? 382 : r9 >= 4 ? 388 : 381);
1408	        }
1409	        let r10 = rng.int(0, 3);
1410	        if (r10 === 3) {
1411	          if (!any(520)) return D(520);
1412	          r10 = rng.int(0, 2);
1413	        }
1414	        return D(r10 === 0 ? 385 : r10 === 1 ? 389 : 383);
1415	      }
1416	    }
1417	
1418	    // ---- 蜘蛛巢（L1569-1587）：落点墙 62 或 spawnSpider 旗标 ----
1419	    const wall = st.wall[st.idx(this.spawnTileX, this.spawnTileY)];
1420	    if (wall === 62 || this.spawnSpider) {
1421	      // 造型师 354（1/8,岩石层深处+场内无 354）：解绑城镇 NPC 救援链路,注释保留
1422	      if (this.hardMode && !N(10)) return D(163);  // hardMode 9/10 黑寡妇(L1577)
1423	      return D(164);                               // 爬墙者
1424	    }
1425	    // ---- 地下沙漠（L1589-1672 1:1）----
1426	    //  门：落点/上格带沙漠墙（AllowsUndergroundDesertEnemiesToSpawn≈spawnUndergroundDesert
1427	    //  邻域扫描已覆盖）&& WorldGen.checkUnderground（L1589 第二合取项，此前缺失——
1428	    //  浅层沙洞误判地下沙漠）
1429	    if (this.spawnUndergroundDesert && this.checkUnderground(this.spawnTileX, this.spawnTileY)) {
1430	      // num11 深度系数（L1591-1599）：岩石层下再深(>(rockLayer*2+h)/3)×0.5、
1431	      // 岩石层下 ×0.85，用于下方两支蠕虫的 1/(50*num11) 概率门
1432	      let num11 = 1.3;
1433	      if (this.spawnTileY > (this.world.rockLevel * 2 + st.h) / 3) num11 *= 0.5;
1434	      else if (this.spawnTileY > this.world.rockLevel) num11 *= 0.85;
1435	      // L1600：高尔夫球手 589（1/20，非水域；savedGolfer 未跟踪恒 false；json 缺
1436	      //  589 条目 → fromVanilla null 静默丢弃，登记 docs/spawn-parity-gaps.md）
1437	      if (N(20) && !this.waterTile && !any(589)) return D(589);
1438	      // L1605：沙虫 510（hard，1/(50·num11)，非蠕虫禁置，落脚深于 worldSurface+100）
1439	      if (hardMode && N(Math.floor(50 * num11)) && !this.noWorms
1440	        && this.spawnTileY > this.world.groundLevel + 100) return D(510);
1441	      // L1610：墓穴爬虫 513（同概率门，场内唯一）
1442	      if (N(Math.floor(50 * num11)) && !this.noWorms
1443	        && this.spawnTileY > this.world.groundLevel + 100 && this.countNpc(513) === 0) return D(513);
1444	      // L1615：hard 4/5 加权池（SelectRandom：恶地双份 525/526/527、中立双份 524、
1445	      //  恶地补 533/529 否则 530/528、恒补 532）
1446	      if (hardMode && !N(5)) {
1447	        const ghoulPool: number[] = [];
1448	        if (this.ZoneCorrupt) ghoulPool.push(525, 525);
1449	        if (this.ZoneCrimson) ghoulPool.push(526, 526);
1450	        if (this.ZoneHallow) ghoulPool.push(527, 527);
1451	        if (ghoulPool.length === 0) ghoulPool.push(524, 524);
1452	        if (this.ZoneCorrupt || this.ZoneCrimson) ghoulPool.push(533, 529);
1453	        else ghoulPool.push(530, 528);
1454	        ghoulPool.push(532);
1455	        return D(ghoulPool[rng.int(0, ghoulPool.length - 1)]);
1456	      }
1457	      // L1654：基础池 = SelectRandom(69,580,580,580,581)（蚁狮 20%/步行蚁狮×3 60%/飞行蚁狮 20%），
1458	      //  再 1/15 覆盖沙史莱姆 537、1/10 升级巨型变体 508/509（顺序不可反——原版先选后改）
1459	      let num12 = [69, 580, 580, 580, 581][rng.int(0, 4)];
1460	      if (N(15)) num12 = 537;
1461	      else if (N(10)) {
1462	        if (num12 === 580) num12 = 508;
1463	        else if (num12 === 581) num12 = 509;
1464	      }
1465	      return D(num12);
1466	    }
1467	    // ---- 硬模式群系水面（:1673-1683,地下沙漠块尾 else-if 链;pre-hardmode 恒跳过）----
1468	    //  丛林水 2/3 → 巨骨舌鱼 157(Arapaima);猩红水 2/3 → 242/241(毒骨鱼/血浆渗透者)
1469	    //  ★此前未移植:困难模式丛林湖泊只有食人鱼/垂钓者兜底,原版主体是巨骨舌鱼
1470	    if (hardMode && this.waterTile && this.ZoneJungle && !N(3)) return D(157);
1471	    if (hardMode && this.waterTile && this.ZoneCrimson) {
1472	      if (!N(3)) return D(242);
1473	      if (!N(3)) return D(241);
1474	    }
1475	    // ---- 海洋（L1705-1834）----
1476	    // 门（L1705）：(!spawnFriendly || (!savedAngler && !AnyNPCs(376))) && waterTile && isOcean。
1477	    //  spawnFriendly（Spawner 字段 L71）：SetSpawnFlags L714-828 内**概率 roll** 的
1478	    //  "友好刷怪位"——该帧只刷小动物。门语义：友好轮**只**被"渔夫未救且场上无 376"
1479	    //  拦截（此时渔夫优先占位），敌怪轮恒放行——此前写成 !any(376) 整体封门，
1480	    //  睡渔夫在场时海洋敌怪（鲨鱼/水母/鱿鱼）全部断供。
1481	    //  savedAngler（NPC.savedAngler 静态）：由 AI_007_TownEntities_UpdateSavedStates
1482	    //  （NPC.cs:53337-53361 case 369）在渔夫 369 城镇化运行 AI 时置位；本仓渔夫
1483	    //  救援链未实装（376 睡渔夫可由本段刷出，但无 376→369 转换、flags 亦无
1484	    //  savedAngler 位）→ 恒 false。AnyNPCs(376) 用 activeIds 现查
1485	    if ((!this.spawnFriendlyCycle || !any(376)) && this.waterTile && this.isOcean) {
1486	      // 渔夫 376（L1708-1728）：表层水（spawnTileY < worldSurface-10）→ 向上 50 格
1487	      //  找干隙线 num15 → 抬到该线落点；!xRange 才出（L1723）
1488	      let angler: Enemy | null = null;
1489	      if (!any(376) && this.spawnTileY < this.world.groundLevel - 10) {
1490	        const num15 = this.findDryGapY(this.spawnTileY);
1491	        if (num15 > 0 && !this.xRange) angler = this.spawnNPC(x, num15 * TILE, 376, rng);
1492	      }
1493	      // L1729-1732：出了渔夫或落点在玩家横向 safe 范围内 → 直接返回
1494	      if (angler || this.xRange) return angler;
1495	      // 水面线 num17 / 岸上净空位 num18（L1733-1761，仅 spawnTileY<worldSurface 且 >50）
1496	      let num17 = -1, num18 = -1;
1497	      if (this.spawnTileY < this.world.groundLevel && this.spawnTileY > 50) {
1498	        for (let y2 = this.spawnTileY - 1; y2 > this.spawnTileY - 50; y2--) {
1499	          if (st.liquid[st.idx(this.spawnTileX, y2)] === 0
1500	            && !st.isSolid(this.spawnTileX, y2) && !st.isSolid(this.spawnTileX, y2 + 1)
1501	            && !st.isSolid(this.spawnTileX, y2 + 2)) {
1502	            num17 = y2 + 2;
1503	            // L1742-1745：num17 下两格净空且 num17+2 墙非房屋墙 → 岸上落点 num18
1504	            if (!st.isSolid(this.spawnTileX, num17 + 1) && !st.isSolid(this.spawnTileX, num17 + 2)
1505	              && !WALL_HOUSE.has(st.wall[st.idx(this.spawnTileX, num17 + 2)])) num18 = num17 + 2;
1506	            // L1746-1749：num17 自身在房屋墙内 → 作废水面线
1507	            if (WALL_HOUSE.has(st.wall[st.idx(this.spawnTileX, num17)])) num17 = -1;
1508	            break;
1509	          }
1510	        }
1511	        if (num17 > this.spawnTileY) num17 = this.spawnTileY;   // L1753-1756
1512	        if (num18 > this.spawnTileY) num18 = this.spawnTileY;   // L1757-1760
1513	      }
1514	      // 海鸥 602（L1762-1765）：干隙线存在 + !xRange + 1/10 → 落在水面线 num17
1515	      if (num17 > 0 && !this.xRange && N(10)) return this.spawnNPC(x, num17 * TILE, 602, rng);
1516	      // 鲨鱼 65（L1766-1769）：1/SharkSpawnChance。原版 SharkSpawnChance（L5458-5475）
1517	      //  基础 10，落点水面上方可命中弹体 820（血腥诱饵 Chum，Chum Caster 鱼竿施放）时降为 2。
1518	      //  依赖链未实装：items.ts 无 Chum 物品注册、无弹体 820 → 恒 10（依赖：
1519	      //  Chum Bucket/Chum Caster 物品 + 鱼竿弹体系统）
1520	      const sharkChance = 10;
1521	      if (N(sharkChance)) return D(65);
1522	      // 鲨鱼龙 692（L1770-1773，困难）：json 已有条目（1:1 虎鲸属性，aiStyle 16 游泳族）
1523	      if (hardMode && N(sharkChance)) return D(692);
1524	      // 海洋小动物（L1774-1817）：1/10 门 → Next(4) 四选
1525	      if (N(10)) {
1526	        const num20 = rng.int(0, 3);   // Main.rand.Next(4)
1527	        if (num20 === 0 && num17 > 0) return this.spawnNPC(x, num17 * TILE, 625, rng);  // 海龟
1528	        if (num20 === 1 && num18 > 0) return this.spawnNPC(x, num18 * TILE, 615, rng);  // 海豚
1529	        if (num20 === 2) {   // 海马（L1789-1805）：金 1/goldCritterChance(400, NPC.cs:5976)
1530	          const num22 = num18 > 0 ? num18 : this.spawnTileY;
1531	          return this.spawnNPC(x, num22 * TILE, N(400) ? 627 : 626, rng);
1532	        }
1533	        if (num20 === 3) {   // 河豚（L1806-1815）
1534	          const num21 = num18 > 0 ? num18 : this.spawnTileY;
1535	          return this.spawnNPC(x, num21 * TILE, 688, rng);
1536	        }
1537	        return null;   // case0/1 落点条件不满足 → 原版 switch 空过不生成
1538	      }
1539	      if (N(40)) return D(220);   // 海蜗牛（L1818-1821）
1540	      if (N(18)) return D(221);   // 鱿鱼（L1822-1825）
1541	      if (N(3)) return D(67);     // 螃蟹（L1826-1829）
1542	      return D(64);               // 粉水母兜底（L1830-1833）
1543	    }
1544	    // ---- 墓地雕像宝箱怪（NPC.cs:1478，原版链位在入侵段之后、水池段之前）----
1545	    //  downedBoss3 && ZoneGraveyard && !noWorms && RollBadLuckExtreme(25)==0 && 场上无 690
1546	    //  && IsThisAGoodPlaceForAStatueMimic（:43751 = 落脚 2 格实心 + 上方 3 格净空，与
1547	    //  邻近是否有雕像无关——名字只是历史）。该支不受 spawnFriendly 门（同链更早的
1548	    //  兄弟分支），友好轮也可命中。690 immortal+aiStyle126（伪装雕像待敌靠近）。
1549	    //  RollBadLuckExtreme = Luck.RollBadLuckExtreme(player.luck, 25)（NPC.cs:5271-5273，
1550	    //  Luck.cs:40-51）：正运改掷 Next(250)（命中 1/250）、负运改掷 Next(25/10=2)（命中
1551	    //  1/2）、否则 Next(25)（1/25）——曾裸 N(25) 无幸运度调制
1552	    if (this.downedBoss3 && this.ZoneGraveyard && !this.noWorms
1553	      && rollBadLuckExtreme(this.playerLuck, 25, () => rng.next()) === 0 && !any(690)
1554	      && this.isGoodPlaceForAStatueMimic()) {
1555	      return D(690);
1556	    }
1557	    // ---- 水池段（L1839-1905）----
1558	    //  两支 else-if（原版 L1839 / L1895,均带 !spawnFriendly 门）;友好轮落 SpawnAnNPC
1559	    //  :2006 的 spawnFriendly 段(水中小动物 :2136+),本仓该段走水中小动物近似于 A 段内
1560	    if (this.waterTile && !this.isOcean && !this.spawnFriendlyCycle) {
1561	      // 门 A（L1839）：!spawnFriendly && waterTile && ((deeperThanRockLayer && 1/2) || 丛林草 60)
1562	      if ((this.deeperThanRockLayer && N(2)) || t === T.JUNGLE_GRASS) {
1563	        let flag9 = false;
1564	        // L1842：丛林草 + 表层 + y>50 + 1/3 + 白天 → 水面线小动物
1565	        if (t === T.JUNGLE_GRASS && this.surfaceSpawn && this.spawnTileY > 50 && N(3) && this.dayTime) {
1566	          const num23 = this.findDryGapY(this.spawnTileY);
1567	          if (num23 > 0 && !this.xRange) {   // L1857
1568	            flag9 = true;
1569	            // 丛林龟 617（L1860-1864）：1/4
1570	            if (N(4)) return this.spawnNPC(x, num23 * TILE, 617, rng);
1571	            // 水黾群（L1865-1880）：无风（flag = |windSpeedTarget|>0.45, L1201）且非雨天
1572	            //  → Next(1,4) 只、x 抖 ±16px、落 num23 上一格；金水黾 1/400
1573	            //  spawner 单返回值 API 只能交付 1 只，其余丢弃（原版成群 1-3 只）
1574	            const windy = Math.abs(this.world.weather.windSpeedTarget) > 0.45;
1575	            const raining = this.world.weather.raining;
1576	            if (!windy && !raining) {
1577	              flag9 = true;
1578	              const num25 = rng.int(1, 3);   // Main.rand.Next(1,4)
1579	              const jx = x + rng.int(-16, 16);
1580	              return this.spawnNPC(jx, num23 * TILE - TILE, N(400) ? 613 : 612, rng);
1581	            }
1582	          }
1583	        }
1584	        if (!flag9) {
1585	          // L1883-1893：琵琶鱼（困难 Next(3)>0 = 2/3）/ 食人鱼兜底
1586	          if (hardMode && rng.next() < 2 / 3) return D(102);
1587	          return D(58);
1588	        }
1589	        return null;   // flag9 已置但雨天/有风未生成（L1883 守卫）→ 原版本帧不出怪
1590	      }
1591	      // 门 B（L1895）：!spawnFriendly && waterTile && spawnTileY>worldSurface && 1/3
1592	      //  → 绿水母（困难 2/3）/ 蓝水母 63
1593	      if (this.spawnTileY > this.world.groundLevel && N(3)) {
1594	        if (hardMode && rng.next() < 2 / 3) return D(103);
1595	        return D(63);
1596	      }
1597	    }
1598	    // ---- 水池第三支（L1906-1993 1:1，**无** !spawnFriendly 门——友好轮也可命中；
1599	    //  A/B 两支带 !spawnFriendly,本仓外层 if 只包 A/B,故此支独立成块）----
1600	    //  门：waterTile && 1/4 && (x 在两片海洋带之间 || y > worldSurface+50)：
1601	    //  腐化→57 腐化金鱼 / 猩红→465 邪恶金鱼；否则白天地表水（y<ws && >50 && 2/3）
1602	    //  → 水面线小动物（草地 1/5 水黾 616 / 沙地 1/2 水黾群或鸊鷉 608 / 其余鸭 362/364）；
1603	    //  深水或夜间 → 内带沙 607 鳉 / 金金鱼 592(1/400) / 兜底金鱼 55
1604	    if (this.waterTile && N(4) && ((this.spawnTileX > 250 && this.spawnTileX < st.w - 250)
1605	      || this.spawnTileY > this.world.groundLevel + 50)) {
1606	      if (this.ZoneCorrupt) return D(57);
1607	      if (this.ZoneCrimson) return D(465);
1608	      if (this.spawnTileY < this.world.groundLevel && this.spawnTileY > 50 && !N(3) && this.dayTime) {
1609	        // 地表白日水面线（:1918-1930 复用 findDryGapY）
1610	        const num26 = this.findDryGapY(this.spawnTileY);
1611	        if (num26 > 0 && !this.xRange) {
1612	          // :1933 草族(2/477) && 1/5 → 水黾 616
1613	          if (N(5) && (t === T.GRASS || t === T.MOWED_GRASS)) return this.spawnNPC(x, num26 * TILE, 616, rng);
1614	          // :1937 沙地：1/2 无风无雨 → 水黾群 613 金/612（原版 1-3 只,单返回值交付 1 只）;
1615	          //  否则鸊鷉 608
1616	          if (t === T.SAND) {
1617	            const windyC = Math.abs(this.world.weather.windSpeedTarget) > 0.45;   // :1201 flag
1618	            if (N(2) && !windyC && !this.world.weather.raining) {
1619	              return this.spawnNPC(x + rng.int(-16, 16), num26 * TILE - TILE, N(400) ? 613 : 612, rng);
1620	            }
1621	            return this.spawnNPC(x, num26 * TILE, 608, rng);
1622	          }
1623	          // :1959 其余 1/2 → 鸭 362 / 364
1624	          return this.spawnNPC(x, num26 * TILE, N(2) ? 362 : 364, rng);
1625	        }
1626	        // 水面线不成立（num26<=0 或 xRange 内）→ :1968 沙地内带鳉鱼 607（原版落在
1627	        //  num26*16——num26 为 -1 时即负 y,照抄）/ 金金鱼 592(1/400) / 金鱼 55
1628	        if (t === T.SAND && this.spawnTileX > 380 && this.spawnTileX < st.w - 380) {
1629	          return this.spawnNPC(x, num26 * TILE, 607, rng);
1630	        }
1631	        if (N(400)) return D(592);
1632	        return D(55);
1633	      }
1634	      // :1981 深水/夜间：内带沙 607 / 金金鱼 592(1/400) / 兜底金鱼 55
1635	      if (t === T.SAND && this.spawnTileX > 380 && this.spawnTileX < st.w - 380) return D(607);
1636	      if (N(400)) return D(592);
1637	      return D(55);
1638	    }
1639	    // ---- 绑缚三人组（NPC.cs:1994-2005：水池第三支之后、spawnFriendly 段之前的三支
1640	    //      else-if；友好轮同样可命中——原版无 spawnFriendly 门）----
1641	    //  公共门：RollLuck(20)==0 && !waterTile && deeperThanRockLayer &&
1642	    //  spawnTileY < maxTilesY-210 && 前置旗 && !savedXxx && 场上唯一（AnyNPCs）。
1643	    //  ★&& 求值序与原版一致（前置旗在 RollLuck 之前短路）——RNG 消费流不变。
1644	    //  产出为占位 Enemy（spawnBound——vanilla-npcs.json 缺 685 条目，fromVanilla 会
1645	    //  null；Game.trySpawnEnemy 按 vanillaId 转 bound TownNPC，占位体随即弃置）：
1646	    //    105 BoundGoblin  ← downedGoblins && !savedGoblin
1647	    //    106 BoundWizard  ← hardMode && !savedWizard
1648	    //    685 BoundTownSlimeOld ← downedBoss3 && !unlockedSlimeOldSpawn
1649	    //    （解救记账见 Game.freeBoundNpc；685 解救置 flags.unlockedSlimeOldSpawn）
1650	    {
1651	      const f = this.world.flags;
1652	      if (f['downedGoblins'] && N(20) && !this.waterTile && this.deeperThanRockLayer
1653	        && this.spawnTileY < st.h - 210 && !f['savedGoblin'] && !any(105)) {
1654	        return this.spawnBound(105);
1655	      }
1656	      if (hardMode && N(20) && !this.waterTile && this.deeperThanRockLayer
1657	        && this.spawnTileY < st.h - 210 && !f['savedWizard'] && !any(106)) {
1658	        return this.spawnBound(106);
1659	      }
1660	      if (this.downedBoss3 && N(20) && !this.waterTile && this.deeperThanRockLayer
1661	        && this.spawnTileY < st.h - 210 && !f['unlockedSlimeOldSpawn'] && !any(685)) {
1662	        return this.spawnBound(685);
1663	      }
1664	    }
1665	    // ---- 墓地友好轮（SpawnAnNPC :2008-2014，spawnFriendly 段首支）----
1666	    //  ZoneGraveyard 时友好轮恒走本支：非水域 50/50 蛆 606 / 鼠 610，水域直接空过——
1667	    //  不受昼夜门限制（原版本支无 dayTime 条件），也不落后续小动物链
1668	    if (this.spawnFriendlyCycle && this.ZoneGraveyard) {
1669	      if (!this.waterTile) return D(N(2) ? 610 : 606);
1670	      return null;
1671	    }
1672	    // ---- 雨天深层宝石松鼠/兔（NPC.cs:2289-2296，case 2/109/477/492 雨分支首两支）----
1673	    //  门：raining && spawnTileY <= UnderworldLayer && deeperThanRockLayer，各 1/5；
1674	    //  未命中则原版继续雨块尾段（金蚯蚓/蚯蚓/上岸金鱼——本仓雨块仅地表简化版，深处放行
1675	    //  落后续洞穴段）。宝石档位按 GetGemSquirrel/BunnyToSpawn 权重表 roll，
1676	    //  与落点附近是否有宝石 tile 无关（原版即如此）。
1677	    //  tile 门 = case 2/109/477/492 或地下任意（default: y>worldSurface → goto case 2）；
1678	    //  147/161/60/53 走各自 switch case（雪原/丛林蛙/沙地小动物），须排除
1679	    const gemTileOK = !(t === T.JUNGLE_GRASS || t === T.SNOW || t === T.ICE || t === T.SAND);
1680	    if (this.spawnFriendlyCycle && this.dayTime && !this.waterTile && this.world.weather.raining && gemTileOK
1681	      && !friendlyBlocked
1682	      && this.deeperThanRockLayer && this.spawnTileY <= st.h - 200) {
1683	      if (N(5)) return D(this.getGemSquirrelToSpawn(rng));
1684	      if (N(5)) return D(this.getGemBunnyToSpawn(rng));
1685	    }
1686	    // ---- 小动物（spawnFriendly 段 L2006-2535，白天 + 草/土 tile + Next(15) 门）----
1687	    //  日食白天小动物段整体关闭（L709 门，friendlyBlocked）
1688	    if (this.spawnFriendlyCycle && this.dayTime && !this.waterTile && this.surfaceSpawn && !friendlyBlocked &&
1689	      (t === T.GRASS || t === T.DIRT || t === T.SNOW || t === T.SNOW_BRICK || t === T.MOWED_GRASS)) {
1690	      // ---- 椿象/蝴蝶（cs:2381-2410，在 N(15) 近似的鸟兽链**之前**的两支 else-if）----
1691	      //  门：白昼草族 tile（case 2/109/477/492）+ !TooWindyForButterflies（|windSpeedTarget|
1692	      //  ≥0.4，NPC.cs:6801）+ 无雨 + Next(每夜概率)==0。概率源 = setFireFlyChance
1693	      //  （NPC.cs:94557-94610，每夜 StartNight 掷：4/5 的夜该族为 999999 绝迹哨兵；
1694	      //  世界字段随存档，旧档缺省=代表值 10/绝迹）——原版另有 1/4 概率左右 ±16px
1695	      //  附加只，单返回值 API 只交付 1 只（蜻蜓段同先例）
1696	      if (t === T.GRASS || t === T.MOWED_GRASS || t === T.HALLOW_GRASS || t === T.HALLOW_MOWED_GRASS) {
1697	        const tooWindyFB = Math.abs(this.world.weather.windSpeedTarget) >= 0.4;
1698	        const dryDay = !this.world.weather.raining;
1699	        // 椿象 669（cs:2381-2392）
1700	        if (!tooWindyFB && dryDay && N(Math.max(1, this.world.stinkBugChance))) return D(669);
1701	        // 蝴蝶 356 / 金蝴蝶 444（cs:2394-2410，金 = RollLuck(goldCritterChance)=1/400）
1702	        if (!tooWindyFB && dryDay && N(Math.max(1, this.world.butterflyChance))) {
1703	          return D(N(400) ? 444 : 356);
1704	        }
1705	      }
1706	      if (N(15)) {
1707	        if (t === T.SNOW || t === T.SNOW_BRICK) {
1708	          // 雪原小动物（L148→148|149 Next(2)）
1709	          if (N(2)) return D(148);
1710	          return D(149);
1711	        }
1712	        // 瓢虫 604/605（cs:2413-2445）：起风日（TooWindyForButterflies=|windSpeedTarget|
1713	        // ≥0.4，NPC.cs:6801）替换蝴蝶段——仅草族 tile（case 2/109/477/492）。
1714	        // butterflyChance 动态值 1..20（4/5 启用、1/5 关闭，cs:94582-94599），原版
1715	        // 门 Next(butterflyChance/2) 取期望 ≈ 1/5；金瓢虫 RollLuck(goldCritterChance)
1716	        // =1/400（luck 修正走 N(400)）。原版成群 1-4 只，本仓单只（API 限制同蜻蜓段）
1717	        if ((t === T.GRASS || t === T.MOWED_GRASS || t === T.HALLOW_GRASS || t === T.HALLOW_MOWED_GRASS)
1718	          && Math.abs(this.world.weather.windSpeedTarget) >= 0.4
1719	          && !this.world.weather.raining && N(5)) {
1720	          return D(N(400) ? 605 : 604);
1721	        }
1722	        // 森林小动物概率表（原版 butterflyChance/stinkBugChance 动态值，取代表值）
1723	        const r = rng.next();
1724	        if (r < 0.2) return D(357);       // 蚯蚓
1725	        if (r < 0.45) return D(377);      // 蚱蜢
1726	        if (r < 0.65) return D(46);       // 兔子
1727	        if (r < 0.8) return D(299);       // 松鼠
1728	        if (r < 0.9) return D(300);       // 老鼠
1729	        return D(74);                     // 鸟
1730	      }
1731	    }
1732	    // ---- 洞穴层宝石松鼠/兔（NPC.cs:2456-2531 case 2 尾段：flag11 = rockLayer ≤ y ≤ UnderworldLayer）----
1733	    //  Next(3)==0 → 1/5 宝石松鼠；否则 1/5 宝石兔（合计 1/15 + 2/15 ≈ 1/5）；
1734	    //  未命中则原版 switch 空过、落后续 else-if 链（地牢/陨石…），此处同序放行。
1735	    //  tile 门同雨天支（case 2/default-underground；147/161/60/53 各有独立 case 须排除）。
1736	    //  （原版该块外层为 spawnFriendly 小动物段；本仓小动物沿用 dayTime 简化门）
1737	    if (this.spawnFriendlyCycle && this.dayTime && !this.waterTile && !this.surfaceSpawn && gemTileOK && !friendlyBlocked
1738	      && this.spawnTileY >= this.world.rockLevel && this.spawnTileY <= st.h - 200) {
1739	      if (N(3)) {
1740	        if (N(5)) return D(this.getGemSquirrelToSpawn(rng));
1741	      } else if (N(5)) {
1742	        return D(this.getGemBunnyToSpawn(rng));
1743	      }
1744	    }
1745	    // 友好轮守卫（SpawnAnNPC :2006 else-if 链语义）：friendly 轮只可能出小动物,
1746	    // 前面各友好分支未命中(落点 tile 不合) → 本轮空过,绝不落入后续敌怪链
1747	    if (this.spawnFriendlyCycle) return null;
1748	    // ---- 地牢（L2536-2706：CheckToSpawnDungeonEnemies :5690-5697 1:1）----
1749	    //  原版 result = inTheDungeon;仅 (drunkWorld || !isThereAWorldSurface) 世界才有
1750	    //  "playerY < dungeonY+40 → false" 的限深门（醉酒/无地表的 remix 类世界）。
1751	    //  本仓恒有 worldSurface 且无 drunkWorld → 门恒开。旧实现把限深门无条件挂上,
1752	    //  玩家在地牢浅层（入口/地表段,dungeonY+40 之上）时整个地牢池不刷怪——错位
1753	    if (this.ZoneDungeon) {
1754	        // 墙变体（L2540-2552）：94/96/98→1、95/97/99→2；RollLuck(7) 重掷（0.9 尺度下 1/7≈1/7）
1755	        const wallA = st.wall[st.idx(this.spawnTileX, this.spawnTileY)];
1756	        const wallB = st.wall[st.idx(this.spawnTileX, this.spawnTileY - 1)];
1757	        let variant = 0;
1758	        if (wallA === 94 || wallA === 96 || wallA === 98 || wallB === 94 || wallB === 96 || wallB === 98) variant = 1;
1759	        if (wallA === 95 || wallA === 97 || wallA === 99 || wallB === 95 || wallB === 97 || wallB === 99) variant = 2;
1760	        if (N(7)) variant = rng.int(0, 3);
1761	        // 未杀骷髅王（flag12）→ 地牢守卫 68（9999 伤，1:1 原版劝退机制）
1762	        if (!this.downedBoss3) return D(68);
1763	        // L2562 机械师(123)：1/5，未救出+场内唯一+深层门（(ws*4+rl)/5）
1764	        const hardDungeon = this.hardMode && !!this.world.flags['downed_262']; // downedPlantBoss（世花 262，Game 击杀通用置位链 downed_{id}）
1765	        if (this.downedBoss3 && N(5) && !this.waterTile && !any(123)
1766	          && this.spawnTileY > (this.world.groundLevel * 4 + this.world.rockLevel) / 5) {
1767	          return D(123);
1768	        }
1769	        // L2570-2585 hardDungeon（hardMode && downedPlantBoss）：1/30 技师 287 + 各墙变体 1/15
1770	        if (hardDungeon && N(30)) return D(287);
1771	        if (hardDungeon && variant === 0 && N(15)) return D(293);
1772	        if (hardDungeon && variant === 1 && N(15)) return D(291);
1773	        if (hardDungeon && variant === 2 && N(15)) return D(292);
1774	        // L2588：骷髅神枪手 290——墙变体 0（蓝）专属，场上唯一，1/35
1775	        if (hardDungeon && !any(290) && variant === 0 && N(35)) return D(290);
1776	        // L2593：骷髅突击队长 289——墙变体 1/2（绿/粉），1/30
1777	        if (hardDungeon && (variant === 1 || variant === 2) && N(30)) return D(289);
1778	        // L2598：死灵法师族 281-286——1/20 → 281+2(蓝变体)+4(粉变体)+Next(2)，
1779	        //  场上已有该 id 则空过（原版 return，不落后续支）
1780	        if (hardDungeon && N(20)) {
1781	          const necro = 281 + (variant === 0 ? 2 : 0) + (variant === 2 ? 4 : 0) + rng.int(0, 1);
1782	          if (!any(necro)) return D(necro);
1783	          return null;
1784	        }
1785	        // L2616：破布施法者族 269-280——2/3 → 269+4(蓝变体)+8(粉变体)+Next(4)
1786	        if (hardDungeon && !N(3)) {
1787	          return D(269 + (variant === 0 ? 4 : 0) + (variant === 2 ? 8 : 0) + rng.int(0, 3));
1788	        }
1789	        if (N(35)) return D(71);   // 地牢史莱姆
1790	        // :2635 刺球 70（Spike Ball，NPCID.cs:11205，aiStyle 20）——绿变体 1/3 且
1791	        //  !NearSpikeBall（:90933 落点 ±300px 盒内已有 aiStyle==20 锚点则不出,防堆积）
1792	        if (variant === 1 && N(3) && !this.nearSpikeBall()) return D(70);
1793	        // :2640 火轮 72（Blazing Wheel，NPCID.cs:11209，aiStyle 21）——粉变体 1/5
1794	        //  （旧注释把 70/72 名字写反,已按 NPCID.cs 勘误）
1795	        if (variant === 2 && N(5)) return D(72);
1796	        if (variant === 0 && N(7)) return D(34);   // 诅咒头骨
1797	        if (N(7)) return D(32);    // 黑魔法师
1798	        // 书架书怪 693/694（AI_FindNearbyBook）：书架实体系统未实现，暂缺
1799	        // L2674：num44 = Next(5) → 0..4（本仓 rng.int 闭区间——此前误写 int(0,5) 多出
1800	        //  第 6 档 undefined id，已改 int(0,4)；case 3/4 落空走下方大小变体支）
1801	        const av = rng.int(0, 4);
1802	        if (av === 0) return D(294);
1803	        if (av === 1) return D(295);
1804	        if (av === 2) return D(296);
1805	        if (N(4)) return D(-14);   // Big Boned
1806	        if (N(5)) return D(-13);   // Short Bones
1807	        return D(31);              // 愤怒骨怪
1808	    }
1809	    // ---- 陨石带（L2704：else if (ZoneMeteor)）----
1810	    //  ZoneMeteor = 玩家窗口内陨石 tile ≥75（SceneMetrics.cs:56 MeteorTileThreshold）→ 陨石头 23
1811	    if (this.ZoneMeteor) return D(23);
1812	    // ---- 月事件（NPC.cs:2714-3455：霜月在先、南瓜月在后，均位于陨石段之后、日食段之前）----
1813	    //  门 = (spawnTileY <= worldSurface || remix) && !dayTime && 事件开启（remixWorld 省略）
1814	    if (this.moonEvent && this.spawnTileY <= this.world.groundLevel && !this.dayTime) {
1815	      const pick = this.moonEvent.kind === MOON_KIND_FROST
1816	        ? this.pickFrostMoonSpawn(this.moonEvent.wave, rng)
1817	        : this.pickPumpkinMoonSpawn(this.moonEvent.wave, rng);
1818	      if (pick !== 0) return D(pick);
1819	      return null;   // 波内全部分支落空（霜月 14 波 / 南瓜 19 波 bossCap 后）= 原版空过
1820	    }
1821	    // ---- 日食（NPC.cs:3459-3525：地表 && dayTime && eclipse——1.4.5.6 重做后的全表）----
1822	    //  门 = spawnTileY <= worldSurface（remix 深层支省略）&& 白天 && eclipse；
1823	    //  flag14 = 三机械全杀（downedMechBoss1/2/3 = 134 / 125|126 / 127）
1824	    if (this.surfaceSpawn && this.dayTime && this.world.clock.eclipse) {
1825	      const f = this.world.flags;
1826	      const downedPlant = !!f['downed_262'];   // downedPlantBoss（世花 262）
1827	      const flag14 = !!(f['downed_134'] && (f['downed_125'] || f['downed_126']) && f['downed_127']);
1828	      let cnt467 = 0; for (const id of this.activeIds) if (id === 467) cnt467++;
1829	      if (downedPlant && N(80) && !any(477)) return D(477);    // 飞蛾魔 Mothron（唯一）
1830	      if (N(50) && !any(251)) return D(251);                   // 独眼怪 Eyezor（唯一）
1831	      if (downedPlant && N(5) && !any(466)) return D(466);     // 精神病人 Psycho（唯一）
1832	      if (downedPlant && N(20) && !any(463)) return D(463);    // 钉头 Nailhead（唯一）
1833	      if (downedPlant && N(20) && cnt467 < 2) return D(467);   // 致命球 Deadly Sphere（≤2）
1834	      if (N(15)) return D(159);                                // 吸血鬼 Vampire
1835	      if (flag14 && N(13)) return D(253);                      // 死神 Reaper（需三机械全杀）
1836	      if (N(8)) return D(469);                                 // 被附身者 The Possessed
1837	      if (downedPlant && N(7)) return D(468);                  // 蝇博士 Dr. Man Fly
1838	      if (downedPlant && N(5)) return D(460);                  // 屠夫 Butcher
1839	      if (N(4)) return D(162);                                 // 科学怪人 Frankenstein
1840	      if (N(3)) return D(461);                                 // 深海怪形 Creature from the Deep
1841	      if (N(2)) return D(462);                                 // 弗里茨 Fritz
1842	      return D(166);                                           // 沼泽怪 Swamp Thing（兜底）
1843	    }
1844	    // ---- 蘑菇地（L3540-3610，tile 70；三支 else-if 1:1）----
1845	    if (t === T.MUSHROOM_GRASS) {
1846	      // :3540 水支：hard && tile 70 && waterTile → 真菌鱼 256（在水池段之后才可达）
1847	      if (hardMode && this.waterTile) return D(256);
1848	      // :3544 地表支：tile 70 && y<=worldSurface && Next(3)!=0（2/3 通过——
1849	      //  旧实现外层门写成 N(3) 恰好取反,且内层五支只剩两支）
1850	      if (this.spawnTileY <= this.world.groundLevel && !N(3)) {
1851	        // 发光蜗牛 360（critter）：肉前 1/6 || 困难 1/12（同层双门,原版即如此）
1852	        if ((!hardMode && N(6)) || N(12)) return D(360);
1853	        if (N(3)) {
1854	          // :2552 真菌球茎族（锚点格随 spawn 传 ai0/ai1）：1/4 命中后 hard 2/3 出大 260
1855	          if (N(4)) {
1856	            return this.spawnNPC(x, y, hardMode && !N(3) ? 260 : 259, rng, this.spawnTileX, this.spawnTileY);
1857	          }
1858	          return D(N(2) ? 257 : 258);   // 异腹真菌蟹 257 / 蘑菇瓢虫 258
1859	        }
1860	        // :2572 僵尸蘑菇 254 / 僵尸蘑菇帽 255（255 无 json 条目 → null,登记台账）
1861	        return D(N(2) ? 254 : 255);
1862	      }
1863	      // :3581 洞穴支：tile 70 && hard && y>=worldSurface && Next(3)!=0（2/3;
1864	      //  第三合取项 (!remix || getGood || y<h-360) 非 remix 恒真）。
1865	      //  肉前穿透本段落入洞穴主池/兜底段,由 L5010/5109 的 ZoneGlowshroom 门出 635/634
1866	      if (hardMode && this.spawnTileY >= this.world.groundLevel && !N(3)) {
1867	        // :3583 松露虫 374（hard 门内即 RollLuck(5)≈1/5,渔夫任务诱饵 critter）
1868	        if (N(5)) return D(374);
1869	        // :3587 发光蜗牛 360：肉前 1/4 支在 hard 门内是死码 → 实际 1/8
1870	        if (N(8)) return D(360);
1871	        if (N(4)) {
1872	          return this.spawnNPC(x, y, hardMode && !N(3) ? 260 : 259, rng, this.spawnTileX, this.spawnTileY);
1873	        }
1874	        return D(N(2) ? 257 : 258);
1875	      }
1876	    }
1877	    // ---- Devourer（NPC.cs:3611-3621，蘑菇地段之后、稀有元素段之前）----
1878	    //  门：ZoneCorrupt && Next(maxValue)==0 && !noWorms && CanSpawnDevourer(spawnTileX)。
1879	    //  maxValue=65（L1195；remixWorld+地表恶地时 25——remix 未实装恒 65）。
1880	    //  CanSpawnDevourer（L5478-5492）：!infectedSeed → 恒 true；本仓无种子系统
1881	    //  （恒非 infectedSeed）→ 恒 true（teamBasedSpawnsSeed/距出生点 0.08w 两分支不可达）。
1882	    //  出怪：hardMode && Next(4)!=0（3/4）→ 98 探求者头；else 7 吞噬怪头
1883	    if (this.ZoneCorrupt && N(65) && !this.noWorms && this.canSpawnDevourer()) {
1884	      if (hardMode && !N(4)) return D(98);
1885	      return D(7);
1886	    }
1887	    // ---- 洞穴稀有怪/小动物（L3644-3719；原版位于蘑菇地之后、丛林草之前）----
1888	    //  RollLuck(n)≈Next(n)（玩家幸运度未接入）；goldCritterChance=400
1889	    // L3644：hard && y>worldSurface && RollLuck(75) → 群系稀有元素怪。
1890	    //  473/474/475/476 与 629 在 vanilla-npcs.json 无条目（fromVanilla→null 静默丢弃），
1891	    //  实际可达的只有兜底 85（hellstone turtle）；分支按原版顺序保留
1892	    if (hardMode && this.spawnTileY > this.world.groundLevel && N(75)) {
1893	      if (N(2) && this.ZoneCorrupt && !any(473)) return D(473);
1894	      if (N(2) && this.ZoneCrimson && !any(474)) return D(474);
1895	      if (N(2) && this.ZoneHallow && !any(475)) return D(475);
1896	      if (N(2) && this.ZoneJungle && !any(476)) return D(476);   // 原版还要求 tenthAnniversaryWorld
1897	      if (this.ZoneSnow) return D(629);
1898	      return D(85);
1899	    }
1900	    // L3671：hard && 落脚墙 2（天然泥土墙）&& 1/20 → 85
1901	    if (hardMode && wall === 2 && N(20)) return D(85);
1902	    // L3676：hard && 地表 && 夜 && (1/20 或 满月 1/5) → 狼人 82
1903	    if (hardMode && this.surfaceSpawn && !this.dayTime
1904	      && (N(20) || (N(5) && this.world.clock.moonPhase === 4))) return D(82);
1905	    // L3681：丛林草 && RollLuck(500) && 夜 → 骨头博士 52(稀有,jungle 金表前置)
1906	    if (t === T.JUNGLE_GRASS && N(500) && !this.dayTime) return D(52);
1907	    // L3688：丛林草 && y>worldSurface && 1/60 → 龟甲虫 219
1908	    if (t === T.JUNGLE_GRASS && this.spawnTileY > this.world.groundLevel && N(60)) return D(219);
1909	    // L3690-3719：洞穴白天小动物（earthworm/mouse/grasshopper 族），条件排除群系旗标。
1910	    //  原版只看 Zone 旗标；直接调用 spawnAnNPC 的场景（测试/探针）旗标未刷新恒 false，
1911	    //  丛林草等群系 tile 会误漏小动物 → 补 tile 级守卫（现实世界群系 tile 必在对应
1912	    //  Zone 窗口内，行为与原版等价）
1913	    const neutralCave = t !== T.JUNGLE_GRASS;
1914	    const critGates = this.spawnTileY > this.world.groundLevel
1915	      && !this.ZoneSnow && !this.ZoneCrimson && !this.ZoneCorrupt && !this.ZoneJungle && !this.ZoneHallow
1916	      && neutralCave;
1917	    if (critGates && this.spawnTileY < st.h - 210 && N(8)) return D(N(400) ? 448 : 357);
1918	    if (critGates && this.spawnTileY < st.h - 210 && N(13)) return D(N(400) ? 447 : 300);
1919	    if (neutralCave && this.spawnTileY > this.world.groundLevel
1920	      && this.spawnTileY < (this.world.rockLevel + st.h) / 2
1921	      && !this.ZoneSnow && !this.ZoneCrimson && !this.ZoneCorrupt && !this.ZoneHallow && N(13)) return D(359);
1922	    // ---- 丛林四支（NPC.cs:3713-3830，原版序：地表小动物→蜂巢块→困难草池→神庙砖→蜂巢墙）----
1923	    // L3713 地表丛林小动物：surfaceSpawn && ZoneJungle && !ZoneCrimson && !ZoneCorrupt && 1/7 →
1924	    //  白天前半（dayTime && Main.time<43200 = 4:30-16:30）且 2/3 → Next(5) 金刚鹦鹉族 671-675；
1925	    //  其余 SpawnFrog（蛙 361 / 金蛙 445 1/400 / 绑缚黄史莱姆 687 1/30 未解锁门）
1926	    if (this.surfaceSpawn && this.ZoneJungle && !this.ZoneCrimson && !this.ZoneCorrupt && N(7)) {
1927	      if (this.dayTime && this.world.clock.hourFloat < 16.5 && !N(3)) {
1928	        return D([671, 672, 673, 674, 675][rng.int(0, 4)]);
1929	      }
1930	      return this.spawnFrog(rng);
1931	    }
1932	    // L3741 蜂巢块 225 落脚（tile 门，区别于 L3832 蜂巢墙 86）：1/2 →
1933	    //  hard 3/4 苔藓黄蜂族（-21/-20/-19/-18 各 1/10，兜底 176），else SpawnHornet
1934	    if (t === T.HIVE && N(2)) {
1935	      if (hardMode && !N(4)) {
1936	        if (N(10)) return D(-21);
1937	        if (N(10)) return D(-20);
1938	        if (N(10)) return D(-19);
1939	        if (N(10)) return D(-18);
1940	        return D(176);
1941	      }
1942	      return this.spawnHornet(x, y, rng);
1943	    }
1944	    // L3771 困难丛林草 60 主池（tile 60 && hard && 2/3）：地表夜 1/3→152 巨型飞狐 /
1945	    //  地表昼 3/4→177 蹦蹦兽 / 深层 1/100→205 飞蛾 / 深层 1/5→236 丛林爬行者 /
1946	    //  深层 3/4→苔藓黄蜂族 / 1/3→175 愤怒捕兽草(锚点) / else 153 巨龟
1947	    if (t === T.JUNGLE_GRASS && hardMode && !N(3)) {
1948	      if (this.surfaceSpawn && !this.dayTime && N(3)) return D(152);
1949	      if (this.surfaceSpawn && this.dayTime && !N(4)) return D(177);
1950	      if (this.spawnTileY > this.world.groundLevel && N(100)) return D(205);
1951	      if (this.spawnTileY > this.world.groundLevel && N(5)) return D(236);
1952	      if (this.spawnTileY > this.world.groundLevel && !N(4)) {
1953	        if (N(10)) return D(-21);
1954	        if (N(10)) return D(-20);
1955	        if (N(10)) return D(-19);
1956	        if (N(10)) return D(-18);
1957	        return D(176);
1958	      }
1959	      if (N(3)) return this.spawnNPC(x, y, 175, rng, this.spawnTileX, this.spawnTileY);
1960	      return D(153);
1961	    }
1962	    // L3821 神庙砖 226/232 && ZoneLihzhardTemple（玩家所站格墙 87，SceneMetrics.cs:688）
1963	    //  → 1/3 飞蛇 226 / else 蜥蜴人 198
1964	    if ((t === T.LIHZAHRD_BRICK || t === T.WOODEN_SPIKE) && this.zoneLihzardTemple()) {
1965	      return D(N(3) ? 226 : 198);
1966	    }
1967	    // ---- 蜂巢墙 86（NPC.cs:3833-3835）：7/8 SpawnHornet ----
1968	    if (wall === 86 && !N(8)) return this.spawnHornet(x, y, rng);
1969	    // ---- 丛林草 tile 60（NPC.cs:3839-3856；旧实现误在肉前出 158 巨型蝙蝠，原版无此分支）----
1970	    if (t === T.JUNGLE_GRASS) {
1971	      const midY = (this.world.groundLevel + this.world.rockLevel) / 2;
1972	      if (this.spawnTileY > midY) {
1973	        // 深层丛林（原版 remix 分支省略）：1/4 棘刺丛林史莱姆 / 1/4 食人怪(锚点) / else 黄蜂族
1974	        if (N(4)) return D(204);
1975	        if (N(4)) return this.spawnNPC(x, y, 43, rng, this.spawnTileX, this.spawnTileY);
1976	        return this.spawnHornet(x, y, rng);
1977	      }
1978	      // 浅层：1/4 丛林蝙蝠 / 1/8 魔腾怪(锚点)
1979	      if (N(4)) return D(51);
1980	      if (N(8)) return this.spawnNPC(x, y, 56, rng, this.spawnTileX, this.spawnTileY);
1981	    }
1982	    // ---- 沙尘暴怪池（NPC.cs:3859-3928 1:1）----
1983	    //  门（:3859 四合取）：Happening && ZoneSandstorm && TileID.Sets.Conversion.Sand
1984	    //  （TileID.cs:30 = 53/112/116/234 四沙——旧 tile 集误混入 397 硬化沙/396 沙岩
1985	    //   且漏 112/116/234 三色沙）&& Spawning_SandstoneCheck（成片沙面计数 ≥40——
1986	    //   孤沙/零星沙不刷,此前缺失致误刷）
1987	    if (this.sandstormHappening && this.zoneSandstorm && TILE_SAND.has(t)
1988	      && this.spawningSandstoneCheck(this.spawnTileX, this.spawnTileY)) {
1989	      // :3861 肉前支带 !downedBoss1（克眼）——杀过克眼但未入困难时落到下方 hard 池的
1990	      //  肉前可达段（mummy/shark 门全 false → 走 546/580/581 兜底）
1991	      const downedBoss1 = !!this.world.flags['downed_4'] || !!this.world.flags.downedEyeOfCthulhu;
1992	      if (!downedBoss1 && !hardMode) {
1993	        if (N(2)) return D(546);      // 怒滚虫 546
1994	        if (N(2)) return D(61);       // 秃鹫
1995	        return D(69);                 // 蚁狮
1996	      }
1997	      // :3876 沙尘元素 541：hard && 1/20 && 场上唯一
1998	      if (hardMode && N(20) && !any(541)) return D(541);
1999	      // :3880 沙丘穿刺者 510：hard && !noWorms && 1/3 && CountNPCS(510)<4,
2000	      //  落点在落脚格**下方 10 格**（(spawnTileY+10)*16——钻地虫从沙下钻出）
2001	      if (hardMode && !this.noWorms && N(3) && this.countNpc(510) < 4) {
2002	        return this.spawnNPC(x, (this.spawnTileY + 10) * TILE, 510, rng);
2003	      }
2004	      // :3884 沙鲨族：hard && !noWorms && 1/2 → 按落脚沙换色（门内 tile 恒在四沙集,
2005	      //  直接判 id：542 沙/543 腐化/544 猩红/545 神圣）
2006	      if (hardMode && !this.noWorms && N(2)) {
2007	        if (t === T.EBONSAND) return D(543);
2008	        if (t === T.CRIMSAND) return D(544);
2009	        if (t === T.PEARLSAND) return D(545);
2010	        return D(542);
2011	      }
2012	      // :3901 沙尘内木乃伊四支（各 1/3——与主链 :3930 的 53→1/3 其余 1/2 不同）
2013	      if (hardMode && t === T.SAND && N(3)) return D(78);
2014	      if (hardMode && t === T.EBONSAND && N(3)) return D(79);
2015	      if (hardMode && t === T.CRIMSAND && N(3)) return D(630);
2016	      if (hardMode && t === T.PEARLSAND && N(3)) return D(80);
2017	      // :3917 兜底池：1/2 怒滚虫 546 → 1/2 步行蚁狮 580 → 飞行蚁狮 581
2018	      if (N(2)) return D(546);
2019	      if (N(2)) return D(580);
2020	      return D(581);
2021	    }
2022	    // ---- 沙漠地表木乃伊（NPC.cs:3930-3944，主链层——位于昼夜池之前，昼夜皆可出）----
2023	    //  蚁狮/秃鹫不在此段：原版在昼池（L4374-4381），夜间沙地走僵尸族（见下方 surfaceSpawn 段）
2024	    if (hardMode && t === T.SAND && N(3)) return D(78);       // 木乃伊（黄沙 1/3）
2025	    if (hardMode && t === T.EBONSAND && N(2)) return D(79);   // 黑暗木乃伊（黑檀沙 1/2）
2026	    if (hardMode && t === T.CRIMSAND && N(2)) return D(630);  // 血腥木乃伊（猩红沙 1/2；json 缺 630 → null，登记台账）
2027	    if (hardMode && t === T.PEARLSAND && N(2)) return D(80);  // 光明木乃伊（珍珠沙 1/2）
2028	    // ---- 神圣 tiles（L3946-3971，tile 116 珍珠沙/117 珍珠石/109 神圣草/164 粉冰）----
2029	    //  旧"hard && 珍珠沙 && 1/2 → 80"独立支系误标 L3940——原版唯一的 116→80 门就在
2030	    //  上方木乃伊块 L3942，此处保留即重复出怪，已删
2031	    const hallowFloor = t === T.PEARLSAND || t === T.PEARLSTONE_BLOCK
2032	      || t === T.HALLOW_GRASS || t === T.HOLLOW_ICE;
2033	    // L3946：hard && underGround && !waterTile && 神圣 tile → 段内顺序 1:1（原版 661 首支）
2034	    //  ①月神蝶 661：downedPlantBoss && 夜前半(!dayTime && Main.time<16200 = 19:30-24:00)
2035	    //    && surfaceSpawn && RollLuck(10) && 场上无 661——与外层 underGround 门交集即
2036	    //    血月/日食强制地表化（L1146-1153）时段（原版即此怪癖，照抄）
2037	    //  ②雨天彩虹史莱姆 244（唯一，RollLuck(10)；NPCID.cs:11553 RainbowSlime——旧注
2038	    //    误标"附魔夜爬虫"）③夜毒气鼻涕虫 122（1/2）
2039	    //  ④独角兽 86：1/10，ZoneWaterCandle 再给一次独立 1/10（:3960 双掷 || 短路）
2040	    //  ⑤兜底妖精 75
2041	    if (hardMode && this.underGround && !this.waterTile && hallowFloor) {
2042	      const downedPlant = !!this.world.flags['downed_262'];
2043	      if (downedPlant && !this.dayTime && this.world.clock.hourFloat >= 19.5
2044	        && this.surfaceSpawn && N(10) && !any(661)) return D(661);
2045	      if (this.world.weather.raining && !any(244) && N(10)) return D(244);
2046	      if (!this.dayTime && N(2)) return D(122);
2047	      // :3960 Next(10)==0 || (ZoneWaterCandle && Next(10)==0)：水蜡烛下独角兽双掷
2048	      if (N(10) || (this.zoneWaterCandle && N(10))) return D(86);
2049	      return D(75);
2050	    }
2051	    // L3962：hard && 1/50 && !waterTile && 岩石层下 && 神圣 tile → 神圣噬魂怪 84
2052	    if (!this.noWorms && hardMode && N(50) && !this.waterTile && this.deeperThanRockLayer && hallowFloor) {
2053	      return D(84);
2054	    }
2055	    // ---- 猩红（L3973-4031 1:1）----
2056	    //  落脚 tile 门：=(204 猩红矿 && ZoneCrimson) || 199 猩红草 || 200 红冰 || 203 猩红石
2057	    //  || 234 猩红沙 || 662 猩红丛林草（remix 195 省略）——原版是 tile 门不是 Zone 门，
2058	    //  旧实现 ZoneCrimson 整段拦截会把腐化边界/猩红矿脉外的怪全劫持进猩红池
2059	    const crimsonFloor = (t === T.CRIMTANE && this.ZoneCrimson) || t === T.CRIMSON_GRASS
2060	      || t === T.CRIMSON_ICE || t === T.CRIMSTONE || t === T.CRIMSAND || t === T.CRIMSON_JUNGLE_GRASS;
2061	    if (crimsonFloor) {
2062	      // flag15 = 落脚深于岩石层（remix 取反省略）
2063	      const flag15 = this.spawnTileY >= this.world.rockLevel;
2064	      // 分层（前四支是 hard+深层专属，肉前不可达）：
2065	      //  ①hard && flag15 && 1/40 && !noWorms → 179 猩红斧（墙挂怪）
2066	      //  ②hard && flag15 && 1/5 && !noWorms → 182 浮空恶臭
2067	      //  ③hard && flag15 && 1/2 → 268 弱金史莱姆（旧实现无 hard/深层门，肉前误出）
2068	      //  ④hard && 1/3 → 小/大 Crimslime(-24/-25 各 1/3) / 183 Crimslime
2069	      //  ⑤hard && (1/2 || 深于地表) → 174 跳跳兽
2070	      //  ⑥(落脚墙>0 && 3/4) || 1/8 → 239 血爬虫（旧实现缺失）
2071	      //  ⑦1/2 → 181 脸怪  ⑧/⑨各 1/3 → -22/-23 小/大 Crimera  ⑩兜底 173 Crimera
2072	      if (hardMode && flag15 && N(40) && !this.noWorms) return D(179);
2073	      if (hardMode && flag15 && N(5) && !this.noWorms) return D(182);
2074	      if (hardMode && flag15 && N(2)) return D(268);
2075	      if (hardMode && N(3)) {
2076	        if (N(3)) return D(-24);
2077	        if (N(3)) return D(-25);
2078	        return D(183);
2079	      }
2080	      if (hardMode && (N(2) || this.spawnTileY > this.world.groundLevel)) return D(174);
2081	      if ((wall > 0 && !N(4)) || N(8)) return D(239);
2082	      if (N(2)) return D(181);
2083	      if (N(3)) return D(-22);
2084	      if (N(3)) return D(-23);
2085	      return D(173);
2086	    }
2087	    // ---- 腐化(NPC.cs:4032-4074 一比一)----
2088	    // 门禁 = 落脚面 tile:(22 魔矿 && ZoneCorrupt) || 腐化草 23 || 黑檀石 25 || 黑沙 112
2089	    // || 腐化冰 163 || 腐化丛林草 661（旧实现的 T.SAND&&ZoneCorrupt 是 22 的误标，661 漏列）。
2090	    // 攀爬者 101 仅困难模式+岩石层下 1/3,锚点格随 spawn 传入
2091	    const corruptFloor = (t === T.DEMONITE && this.ZoneCorrupt) || t === T.CORRUPT_GRASS
2092	      || t === T.EBONSTONE || t === T.EBONSAND || t === T.CORRUPT_ICE || t === T.CORRUPT_JUNGLE_GRASS;
2093	    const ugRock = this.spawnTileY >= this.world.rockLevel; // flag16
2094	    if (corruptFloor) {
2095	      // 83 = Cursed Hammer 诅咒锤（NPCID.cs:11231；旧注"World Feeder"有误——1.4.4 起
2096	      //  World Feeder 头是 98，在上方 Devourer 段）。门带 !noWorms（L4039，此前漏）
2097	      if (hardMode && ugRock && N(40) && !this.noWorms) return D(83);
2098	      if (hardMode && ugRock && N(3)) {
2099	        return this.spawnNPC(x, y, 101, rng, this.spawnTileX, this.spawnTileY); // 攀爬者(锚点格)
2100	      }
2101	      if (hardMode && N(3)) return D(N(3) ? 121 : 81);     // 史莱姆法师/腐化史莱姆
2102	      if (hardMode && (N(2) || ugRock)) return D(94);      // 腐化史莱姆
2103	      if (N(3)) return D(-11);   // 小噬魂怪
2104	      if (N(3)) return D(-12);   // 大噬魂怪
2105	      return D(6);               // 默认 Eater of Souls
2106	    }
2107	    // ---- 地表（L4075-4717）----
2108	    //  群系判定：雪原不走 ZoneSnow 旗标兜底段——原版白昼走小动物/基础史莱姆，
2109	    //  夜晚走 IcesSnow 落脚 tile 段（L4555），此前的 ZoneSnow 拦截段为误植已移除
2110	    if (this.surfaceSpawn) {
2111	      const clock = this.world.clock;
2112	      const raining = this.world.weather.raining;
2113	      const moonPhase = clock.moonPhase;
2114	      // TileID.Sets.IcesSnow（TileID.cs:297：161/200/163/164/147）+ 162
2115	      const iceTile = t === T.ICE || t === T.CRIMSON_ICE || t === T.CORRUPT_ICE
2116	        || t === T.HOLLOW_ICE || t === T.SNOW || t === T.THIN_ICE;
2117	      // ---- 墓地蛆/鼠（L4082-4091，surfaceSpawn 段首、昼池之前）----
2118	      //  ZoneGraveyard && !waterTile && 草族落脚（2/477）&& 1/10 → 50/50 蛆 606 / 鼠 610
2119	      if (this.ZoneGraveyard && !this.waterTile && (t === T.GRASS || t === T.MOWED_GRASS) && N(10)) {
2120	        return D(N(2) ? 610 : 606);
2121	      }
2122	      // ---- L4094-4108：雨雪高仑/雨云怪/火星探测器（surfaceSpawn 段首、昼池之前，昼夜皆可出）----
2123	      //  L4094 冰雪高仑 243：ZoneSnow && hard && raining && 场上无 243 && RollLuck(20)
2124	      if (this.ZoneSnow && hardMode && raining && !any(243) && N(20)) return D(243);
2125	      //  L4099 雨云怪 250：!ZoneSnow && hard && raining && CountNPCS(250)<2 && 1/10
2126	      if (!this.ZoneSnow && hardMode && raining && this.countNpc(250) < 2 && N(10)) return D(250);
2127	      //  L4104 火星探测器 399 地表支（区别于天空支 L1308）：远离世界中央（flag17）&& hard
2128	      //  && downedGolemBoss && ((未败火星 && 1/100) || 1/400) && 场上无 399。
2129	      //  flag17 的 AnyDanger 压制（有敌对 NPC 面向玩家时关闭）未实装 → 恒放行（登记台账）
2130	      const flag17 = Math.abs(this.spawnTileX - st.w / 2) / (st.w / 2) > 0.33;
2131	      if (flag17 && hardMode && this.world.flags['downed_245']
2132	        && ((!this.world.flags['downedMartians'] && N(100)) || N(400)) && !any(399)) {
2133	        return D(399);
2134	      }
2135	      // ---- 白昼（L4109-4435：!ZoneGraveyard && dayTime 大昼池）----
2136	      //  ★墓地白天整体跳过昼池（原版门即 !ZoneGraveyard && Main.dayTime）→ 白天也落入
2137	      //  夜间怪池（僵尸/眼球等）——"墓地白天刷夜怪"的本体语义；昼池兜底基础史莱姆同理不刷
2138	      if (this.dayTime && !this.ZoneGraveyard) {
2139	        // num46 = |落脚 x - 世界出生点 x|（L4108）
2140	        const num46 = Math.abs(this.spawnTileX - this.world.spawnX);
2141	        // L4277-4280：自然刷史莱姆王——!waterTile && num46>maxTilesX/3 && 落脚=草(2)
2142	        //  && 1/300 && 场上无 50 → SpawnOnPlayer(target, 50)（刷在玩家身上而非落脚点）。
2143	        //  SpawnOnPlayer（NPC.cs:81273+，500 次玩家 spawnArea 内选点）未移植，以
2144	        //  "currentSpawnX/Y 钉到玩家格 + Game 侧常规落位"近似（登记台账）
2145	        if (!this.waterTile && num46 > st.w / 3 && t === T.GRASS && N(300) && !any(50)) {
2146	          this.currentSpawnX = this.pX;
2147	          this.currentSpawnY = this.pY;
2148	          return D(50);
2149	        }
2150	        // L4374-4381：蚁狮/秃鹫（昼池内——原版在海滩海鸥支之后、哥布林侦察兵之前；
2151	        //  夜间沙地不出蚁狮/秃鹫，走僵尸族）。蚁狮门 = !waterTile && 黄沙 53 && 1/5 &&
2152	        //  Spawning_SandstoneCheck（成片沙面计数 ≥40）；秃鹫门 = 黄沙 53 && !waterTile。
2153	        //  旧实现放在主链且 tile 集含硬化沙/沙岩/化石 → 昼夜皆出、tile 集过宽，均错位
2154	        if (!this.waterTile && t === T.SAND && N(5)
2155	          && this.spawningSandstoneCheck(this.spawnTileX, this.spawnTileY)) return D(69);
2156	        if (t === T.SAND && !this.waterTile) return D(61);
2157	        // L4412：哥布林侦察兵 73——距出生点 >1/3 图宽，1/15
2158	        //  （或未破哥布林入侵 && 砸过暗影珠 → 1/7）
2159	        if (!this.waterTile && num46 > st.w / 3
2160	          && (N(15) || (!this.world.flags['downedGoblins'] && this.world.flags['shadowOrbSmashed'] && N(7)))) {
2161	          return D(73);
2162	        }
2163	        // L4417：雨天飞行怪 224（1/4，无 waterTile 门）
2164	        if (raining && N(4)) return D(224);
2165	        // L4421：雨伞史莱姆 225（!waterTile 1/2）
2166	        if (!this.waterTile && raining && N(2)) return D(225);
2167	        // L4426/4431：大风天 594 风气球（2/3）→ 628 蒲公英（草地 9/10）。
2168	        //  门：!waterTile && num==0（落点上格无墙，L1188 num=wall）&& IsItAHappyWindyDay
2169	        //  （=_shouldUseWindyDayMusic）&& isSpawningInWindDirection（L1101
2170	        //  (pX-spawnTileX)*windSpeedTarget>0，生成点在玩家下风侧）
2171	        const windyDay = this.world.weather.shouldUseWindyDayMusic;
2172	        const spawnWallEmpty = st.wall[st.idx(this.spawnTileX, this.spawnTileY - 1)] === 0;
2173	        const downwind = (this.pX - this.spawnTileX) * this.world.weather.windSpeedTarget > 0;
2174	        if (!this.waterTile && spawnWallEmpty && windyDay && downwind) {
2175	          if (!N(3)) return D(594);
2176	          // NPC.cs:4112:草族门 = 2/477/109/492/147/161(修剪草/神圣修剪草/雪/冰全在内)
2177	          if ((t === T.GRASS || t === T.MOWED_GRASS || t === T.HALLOW_GRASS || t === T.HALLOW_MOWED_GRASS
2178	            || t === T.SNOW || t === T.ICE) && !N(10)) return D(628);
2179	        }
2180	        // L4435：池底基础史莱姆
2181	        if (!this.waterTile) return D(this.getBasicSlimeToSpawn(true, t, rng));
2182	        return null;
2183	      }
2184	      // ---- 夜晚（L4437-4716；墓地白天亦落入本池——见上方昼池的 !ZoneGraveyard 门）----
2185	      // L4409 `if (ZoneGraveyard) defaultTarget = target`（:4411→:5161 Target 兜底）——
2186	      //  显式把刷出怪的目标设为玩家；本仓敌怪走最近玩家索敌，单人语义等价，不另设
2187	      // L4410：萤火虫（原版带 !ZoneGraveyard 门 :4413）——草族 tile + 无风 + 无雨 +
2188	      //  1/fireFlyChance。概率源 = setFireFlyChance（NPC.cs:94557-94610，每夜 StartNight
2189	      //  掷：1/9 高发夜 5-9 / 1/3 绝迹夜 999999 / 其余 10-59；世界字段随存档，
2190	      //  旧档缺省=代表值 30）——旧实现恒 30，台账登记已核销
2191	      const tooWindy = Math.abs(this.world.weather.windSpeedTarget) >= 0.4;
2192	      if (!this.ZoneGraveyard && !tooWindy && !raining
2193	        && (t === T.GRASS || t === T.MOWED_GRASS || t === T.HALLOW_GRASS || t === T.HALLOW_MOWED_GRASS)
2194	        && N(Math.max(1, this.world.fireFlyChance)) && this.spawnTileY <= this.world.groundLevel) {
2195	        return D(t === T.HALLOW_GRASS ? 358 : 355);
2196	      }
2197	      // L4439：乌鸦 Raven 301——(万圣节 || 墓地) && 1/12（节日未接 → 墓地单门）
2198	      if (this.ZoneGraveyard && N(12)) return D(301);
2199	      // L4444：幽灵 Ghost 316——墓地专属 1/30
2200	      if (this.ZoneGraveyard && N(30)) return D(316);
2201	      // L4449：南瓜跳跳 Hoppin' Jack 304——(万圣节 || 墓地) && hardMode && 1/10
2202	      if (this.ZoneGraveyard && hardMode && N(10)) return D(304);
2203	      // L4454：Next(6) 或 满月（moonPhase==4）1/2 门
2204	      if (N(6) || (moonPhase === 4 && N(2))) {
2205	        // L4456：hard 1/3 → Wandering Eye 133
2206	        if (hardMode && N(3)) return D(133);
2207	        // L4464：1/2 → 恶魔眼族（1/4 小眼 -43）
2208	        if (N(2)) return D(N(4) ? -43 : 2);
2209	        // L4471-4516：switch(Next(5)) 僵尸族 190-194；各 1/3 小变体与本体【同帧同出】
2210	        //  （原版先 SpawnNPC 小变体再 SpawnNPC 本体；单返回值 API 只能交付本体，
2211	        //   小变体另调一次 spawnNPC 后丢弃）。Next(5)=0..4——本仓 rng.int 闭区间，
2212	        //  此前误写 int(0,5) 多出第 6 档 undefined id，已改 int(0,4)
2213	        const zv = rng.int(0, 4);
2214	        if (N(3)) this.spawnNPC(x, y, [-38, -39, -40, -41, -42][zv], rng);
2215	        return D([190, 191, 192, 193, 194][zv]);
2216	      }
2217	      // L4518：hard 1/50 血月 && 场上无小丑 109 → Clown
2218	      if (hardMode && N(50) && clock.bloodMoon && !any(109)) return D(109);
2219	      // L4523/4529：(血月 || 墓地) && RollOnlyBadLuck(300) → The Groom 53 / The Bride 536。
2220	      //  RollOnlyBadLuck 正运无加成（Luck.cs:31-38）→ luck≥0 时 N(300) 即精确；
2221	      //  仅负运态有偏差（登记：负 luck 时应收窄为 [150,300)，见 src/stats/Luck.ts）
2222	      if ((clock.bloodMoon || this.ZoneGraveyard) && N(300)) return D(53);
2223	      if ((clock.bloodMoon || this.ZoneGraveyard) && N(300)) return D(536);
2224	      // L4533：新月（moonPhase==0）hard 2/3 → Werewolf 104
2225	      if (!this.dayTime && moonPhase === 0 && hardMode && !N(3)) return D(104);
2226	      // L4538：hard 1/3 → Werewolf 140
2227	      if (!this.dayTime && hardMode && N(3)) return D(140);
2228	      // L4543：血月 2/5 → Blood Zombie 489 / Drippler 490
2229	      if (clock.bloodMoon && rng.int(0, 5) < 2) return D(N(2) ? 490 : 489);
2230	      // L4555：冰系落脚 tile → hard 1/4 Ice Elemental 169 / hard 1/3 Wolf 155 /
2231	      //  专家 1/2 Armed Zombie 431 / else Frozen Zombie 161
2232	      //  （两支 hard 概率均带 !ZoneGraveyard 门 :4557/:4561——墓地里冰面上冰元素/狼不出，
2233	      //   兜底 161 照刷；:4565 spawnArmedZombies（无 skyblock 恒真）&& expertMode && 1/2 → 431。
2234	      //   Main.expertMode 经 mainExpertMode 求值——getGoodWorld(FTW) 抬档同样成立）
2235	      if (iceTile) {
2236	        if (!this.ZoneGraveyard && hardMode && N(4)) return D(169);
2237	        if (!this.ZoneGraveyard && hardMode && N(3)) return D(155);
2238	        if (expert && N(2)) return D(431);
2239	        return D(161);
2240	      }
2241	      // L4577：雨夜 1/2 → Raincoat Zombie 223（1/3 小变体 -54/-55）
2242	      if (raining && N(2)) {
2243	        if (!N(3)) return D(223);
2244	        return D(N(2) ? -55 : -54);
2245	      }
2246	      // L4585：skyblock 火把僵尸段省略（skyblock 语义未接；原文本支亦带 !ZoneGraveyard 门）
2247	      // L4612：苔藓僵尸 Moss Zombie 691——墓地专属 RollOnlyBadLuckExtreme(200)
2248	      if (this.ZoneGraveyard && N(200)) return D(691);
2249	      // L4617：蛆僵尸 Maggot Zombie 632——墓地专属 1/maggotZombieChance（GetZombieSettings
2250	      //  L5500 恒 20；skyblock/初始血量只调 torch 门，不改本值）
2251	      if (this.ZoneGraveyard && N(20)) return D(632);
2252	      // L4622：火把僵尸 590/591——Next(torchZombieChance)。原版条件**仅此一个概率门**，
2253	      //  与"点燃的火把/营火邻近"无关（590 贴图手持火把故俗名火把僵尸；
2254	      //  GetZombieSettings L5495-5523 全文无火把/营火邻接扫描）。:4624 持械变体 591 需
2255	      //  spawnArmedZombies && expertMode && Next(2)==0（掷骰仅在专家档发生，短路同原版）
2256	      if (N(this.torchZombieChance)) return D(expert && N(2) ? 591 : 590);
2257	      // L4634：halloween/xMas 节日僵尸 319-321/331-332 段略（节日未接）
2258	      // L4644：专家持械僵尸 430-436——spawnArmedZombies && zombieStyle!=1 &&
2259	      //   expertMode && Next(3)==0，按 zombieStyle 选型（0→430/2→432/3→433/4→434/
2260	      //   5→435/6→436；style 1 无持械变体；switch 缺省 430）
2261	      if (expert && this.zombieStyle !== 1 && N(3)) {
2262	        const armed = [430, 430, 432, 433, 434, 435, 436][this.zombieStyle] ?? 430;
2263	        return D(armed);
2264	      }
2265	      // ---- 最终僵尸 style 表（L4671-4716 + GetZombieSettings L5495）----
2266	      //  zombieStyle = Next(7)（在 SpawnAnNPC 入口即 roll，L1193）；各 style 配大小变体
2267	      const zrow = [
2268	        [3, -26, -27], [132, -28, -29], [186, -30, -31], [187, -32, -33],
2269	        [188, -34, -35], [189, -36, -37], [200, -44, -45],
2270	      ][this.zombieStyle] ?? [3, -26, -27];
2271	      let zid = zrow[0];
2272	      if (N(3)) zid = rng.next() < 0.5 ? zrow[1] : zrow[2];
2273	      return D(zid);
2274	    }
2275	    // ---- 地下层（L4718-4770，worldSurface < y < rockLayer）----
2276	    if (this.underGround) {
2277	      if (!this.noWorms && N(50) && !this.ZoneSnow) {
2278	        // L4722：hard → 2/3 Digger 95 / 1/3 Giant Worm 10；肉前恒 10
2279	        if (hardMode) return D(N(3) ? 10 : 95);
2280	        return D(10);
2281	      }
2282	      // L4734/4738：hard 1/3→140（Possessed Armor）/ 1/2→141（Toxic Sludge）
2283	      if (hardMode && N(3)) return D(140);
2284	      if (hardMode && N(2)) return D(141);
2285	      // L4748：落脚 147/161 或 ZoneSnow → 冰史莱姆 147
2286	      if (t === T.SNOW || t === T.ICE || this.ZoneSnow) return D(147);
2287	      return D(this.getBasicSlimeToSpawn(false, t, rng));
2288	    }
2289	    // ---- 地狱（L4771-4820，y > maxTilesY-190）----
2290	    //  mechAny = downedMechBossAny（Main 旗标；我们取 flags.downed_125/126/127/134 任一，
2291	    //  与 Game.ts flag 求值同源）
2292	    if (this.spawnTileY > st.h - 190) {
2293	      const mechAny = !!(this.world.flags['downed_125'] || this.world.flags['downed_126']
2294	        || this.world.flags['downed_127'] || this.world.flags['downed_134']);
2295	      // L4777：hard && 未救出税务官 && 1/20 && 场上无 534 → Tortured Soul 534
2296	      if (hardMode && !this.world.flags['savedTaxCollector'] && N(20) && !any(534)) return D(534);
2297	      // L4781：熔岩小动物 1/8（先于骨蛇——原版段序）。
2298	      //  SpawnLavaBaitCritters（L5760）：2/3 → 白天 Hell Butterfly 653 / 夜 Lavafly 654
2299	      //  （原版夜间成群 1-5 只，单返回值只交付 1 只）；else Magma Snail 655
2300	      if (N(8)) {
2301	        if (!N(3)) return D(this.dayTime ? 653 : 654);
2302	        return D(655);
2303	      }
2304	      // L4787：Bone Serpent 1/40（场上唯一）
2305	      if (N(40) && !any(39)) return D(39);
2306	      // L4794：Fire Imp 1/14
2307	      if (N(14)) return D(24);
2308	      if (N(7)) {
2309	        // L4799：Voodoo Demon 1/10；hard+mechAny 4/5 → Red Devil 156；else Demon
2310	        if (N(10)) return D(66);
2311	        if (hardMode && mechAny && !N(5)) return D(156);
2312	        return D(62);
2313	      }
2314	      // L4810：Lava Slime 1/3
2315	      if (N(3)) return D(59);
2316	      // L4812：hard+mechAny 4/5 → Lava Bat 151；else Hellbat
2317	      if (hardMode && mechAny && !N(5)) return D(151);
2318	      return D(60);
2319	    }
2320	    // CheckToSpawnRockGolem（L4821/L5713 1:1）→ 岩石高仑 631：
2321	    //  hard && (落脚=石 或 Moss 族) && !ZoneSnow && 1/50
2322	    //  && 落点上方 4 格三连（x−1/x/x+1）净空（体型 36×48 的头部空间预检）
2323	    if (this.checkToSpawnRockGolem(rng)) return D(631);
2324	    // ---- 洞穴通用池（L4825-5142）----
2325	    // 冰系 tile 分档（原版各段用不同子集）：
2326	    //  iceAll=147/161/162/163/164/200（蠕虫段 L4842）、iceCave=147/161/162（L4981/5117/5128）
2327	    const iceAll = t === T.SNOW || t === T.ICE || t === T.THIN_ICE
2328	      || t === T.CORRUPT_ICE || t === T.HOLLOW_ICE || t === T.CRIMSON_ICE;
2329	    const iceCave = t === T.SNOW || t === T.ICE || t === T.THIN_ICE;
2330	    if (N(60)) {
2331	      if (this.ZoneSnow) return D(218);
2332	      return D(217);
2333	    }
2334	    // L4836：hard && 珍珠沙/珍珠石/粉冰 && 1/8 → Chaos Elemental 120
2335	    if ((t === T.PEARLSAND || t === T.PEARLSTONE_BLOCK || t === T.HOLLOW_ICE)
2336	      && hardMode && !this.noWorms && N(8)) return D(120);
2337	    // L4842-4850：hard && 冰系 tile && 群系旗标 → Pigron 变体 170(腐化)/171(神圣)/180(猩红)
2338	    if (iceAll && !this.noWorms && hardMode) {
2339	      if (this.ZoneCorrupt && N(30)) return D(170);
2340	      if (this.ZoneHallow && N(30)) return D(171);
2341	      if (this.ZoneCrimson && N(30)) return D(180);
2342	    }
2343	    // L4852：hard && ZoneSnow && 1/10 → Ice Tortoise 154
2344	    if (hardMode && this.ZoneSnow && N(10)) return D(154);
2345	    // L4855：1/100 蠕虫——hard→Digger 95；肉前 ZoneSnow→Snow Flinx 185 / else Giant Worm 10
2346	    if (!this.noWorms && N(100) && !this.ZoneHallow) {
2347	      if (hardMode) return D(95);
2348	      if (this.ZoneSnow) return D(185);
2349	      return D(10);
2350	    }
2351	    // L4867：ZoneSnow && 1/20 → Snow Flinx 185
2352	    if (this.ZoneSnow && N(20)) return D(185);
2353	    // L4871：1/10(肉前)/1/20(hard) 母史莱姆族——雪/冰落脚 184，否则 1/3 黑 -6 / 母 16
2354	    if ((!hardMode && N(10)) || (hardMode && N(20))) {
2355	      if (this.ZoneSnow || t === T.ICE || t === T.SNOW) return D(184);
2356	      if (N(3)) return D(-6);
2357	      return D(16);
2358	    }
2359	    // L4890：(!hard || skyblock) && 1/4 史莱姆段——丛林→-10；雪/冰落脚→184；else -6
2360	    if (!hardMode && N(4)) {
2361	      if (this.ZoneJungle) return D(-10);
2362	      if (this.ZoneSnow || t === T.ICE || t === T.SNOW) return D(184);
2363	      return D(-6);
2364	    }
2365	    if (N(2)) {
2366	      // 洞穴主池（L4896-5099）
2367	      // 骷髅商 453（L4905-4910）：1/35，非水域（影烛未实现），场内唯一（CountNPCS==0）
2368	      // —— Game.trySpawnEnemy 把 453 转成 TownNPC 放 npcs 桶
2369	      if (N(35) && !this.waterTile && !any(453)) return D(453);
2370	      // L4911：Lost Girl 195（Nymph）1/80
2371	      if (N(80)) return D(195);
2372	      // 深层半段 = y > (rockLayer + maxTilesY)/2（L4913/4917 共用门）
2373	      const deepCave = this.spawnTileY > (this.world.rockLevel + st.h) / 2;
2374	      // L4913：hard && 深层半段 && 1/200 → Rune Wizard 172
2375	      if (hardMode && deepCave && N(200)) return D(172);
2376	      // L4917：深层半段 && 1/200（offensiveToTim 1/50 buff 未接）→ Bound Goblin 45
2377	      if (deepCave && N(200)) return D(45);
2378	      // L4929/4941：Next(4)!=0（3/4）→ 大理石房：Next(6)!=0（5/6）且场内无 480
2379	      //  且 hard → Medusa 480，else Hoplite 481（花岗岩同构 483/482）
2380	      if (this.nearMarble && !N(4)) {
2381	        if (!N(6) && !any(480) && hardMode) return D(480);
2382	        return D(481);
2383	      }
2384	      if (this.nearGranite && !N(5)) {
2385	        if (!N(6) && !any(483)) return D(483);
2386	        return D(482);
2387	      }
2388	      // L4951：hard && Next(10)!=0（9/10）→ 洞穴主池：
2389	      //  1/2 → ZoneSnow?197 : (深层半段 1/5→-15 Heavy Skeleton / else 77 Armored Skeleton)
2390	      //  else → ZoneSnow?206 : 110 Skeleton Archer
2391	      if (hardMode && !N(10)) {
2392	        if (N(2)) {
2393	          if (this.ZoneSnow) return D(197);
2394	          if (deepCave && N(5)) return D(-15);
2395	          return D(77);
2396	        }
2397	        return D(this.ZoneSnow ? 206 : 110);
2398	      }
2399	      // L4961：幽灵 Ghost 316——!noWorms && (万圣节 || 墓地) && 1/30（洞穴主池内）
2400	      if (!this.noWorms && this.ZoneGraveyard && N(30)) return D(316);
2401	      // L4969：Undead Miner 44（1/20）
2402	      if (N(20)) return D(44);
2403	      // L4979：冰洞池——落脚 147/161/162：1/15 Snow Flinx 185 / else Undead Viking 167
2404	      if (iceCave) return D(N(15) ? 185 : 167);
2405	      // L4993：ZoneSnow → Snow Flinx 185
2406	      if (this.ZoneSnow) return D(185);
2407	      // L5000：1/3 → cavernMonsterType[Next(2)][Next(3)]（洞穴蝾螈族，世界生成时 roll）
2408	      if (N(3)) return D(cavernMonsterType[rng.int(0, 1)][rng.int(0, 2)]);
2409	      // L5010：ZoneGlowshroom && tile 70/190 → 孢子骷髅 635（蘑菇草/发光蘑菇块落脚）
2410	      if (this.ZoneGlowshroom && (t === T.MUSHROOM_GRASS || t === T.MUSHROOM_BLOCK)) return D(635);
2411	      // L5018：halloween 南瓜精略；L5029：专家模式骨堆小动物 449-452 略（无专家模式）
2412	      // switch(Next(4)) 骷髅系（L5050-5099）：2/3 本体，1/3 大小变体二选一
2413	      const sv = rng.int(0, 3);
2414	      const sm = [21, 201, 202, 203][sv] ?? 21;
2415	      if (!N(3)) return D(sm);
2416	      const small = [[-46, -47], [-48, -49], [-50, -51], [-52, -53]][sv] ?? [-46, -47];
2417	      return D(rng.next() < 0.5 ? small[0] : small[1]);
2418	    }
2419	    // 洞穴兜底（L5101-5142，按原版段序）
2420	    // L5101：hard && ZoneHallow && 1/2 → Illuminant Slime 138
2421	    if (hardMode && this.ZoneHallow && N(2)) return D(138);
2422	    // L5105：ZoneJungle → Jungle Bat 51
2423	    if (this.ZoneJungle) return D(51);
2424	    // L5109：ZoneGlowshroom && tile 70/190 → 孢子蝙蝠 634（洞穴兜底段的蘑菇地支，
2425	    //  与 L5010 的 635 分居两支——命中本支说明洞穴主池 Next(2) 已先行掷空）
2426	    if (this.ZoneGlowshroom && (t === T.MUSHROOM_GRASS || t === T.MUSHROOM_BLOCK)) return D(634);
2427	    // L5113：hard && ZoneHallow → Illuminant Bat 137
2428	    if (hardMode && this.ZoneHallow) return D(137);
2429	    // L5117：hard && Next(6)>0（5/6）→ 冰落脚 1/3 Ice Bat 150 / else Giant Bat 93
2430	    if (hardMode && !N(6)) {
2431	      if (N(3) && iceCave) return D(150);
2432	      return D(93);
2433	    }
2434	    // L5128：冰落脚 tile（147/161/162，非 ZoneSnow 旗标）→ hard?169 Ice Elemental : 150
2435	    if (iceCave) return D(hardMode ? 169 : 150);
2436	    return D(49);  // Cave Bat
2437	  }
2438	
2439	  /** NearSpikeBall（NPC.cs:90933-90948）：落点 ±300px（600×600 px 盒）与场上
2440	   *  aiStyle==20（刺球 70）的锚点 (ai1,ai2) 20×20 盒相交 → true。地牢 :2635 出刺球
2441	   *  前的防堆积门。本仓 spawner 无 NPC 坐标通道（仅 activeIds id 集）→ 以
2442	   *  "场上存在刺球 70"近似（同地牢场景下与 ±300px 盒高度重合;登记台账近似表） */
2443	  private nearSpikeBall(): boolean {
2444	    return this.activeIds.has(70);
2445	  }
2446	
2447	  /** CanSpawnDevourer（NPC.cs:5478-5492 1:1）：!infectedSeed → 恒 true；
2448	   *  infectedSeed && teamBasedSpawnsSeed → false；|X-spawnTileX|>maxTilesX×0.08 → true。
2449	   *  本仓无种子系统（恒非 infectedSeed）→ 恒 true（后两分支不可达，保留签名对齐原文） */
2450	  private canSpawnDevourer(_x = 0): boolean {
2451	    const INFECTED_SEED = false;   // Main.infectedSeed：本仓恒 false
2452	    if (!INFECTED_SEED) return true;
2453	    return Math.abs(_x - this.world.spawnX) > this.world.store.w * 0.08;
2454	  }
2455	
2456	  /** WorldGen.checkUnderground（WorldGen.cs:10083-10129 1:1）：
2457	   *  y>worldSurface+80 → true；y<worldSurface/2 → false；其余扫 (x±60)×(y-80 起 3 行)
2458	   *  的 120×3 带——SolidTile 或 (x,y) 带墙（原版即用常数坐标查墙）计数 ≥288（80%）→ true。
2459	   *  地下沙漠分支门（NPC.cs:1589）的第二合取项 */
2460	  private checkUnderground(x: number, y: number): boolean {
2461	    const st = this.world.store;
2462	    if (y > this.world.groundLevel + 80) return true;
2463	    if (y < this.world.groundLevel / 2) return false;
2464	    let x0 = x - 60;
2465	    if (x0 < 0) x0 = 0;
2466	    if (x0 >= st.w - 120) x0 = st.w - 121;
2467	    const y0 = y - 80;
2468	    const walled = st.inBounds(x, y) && st.wall[st.idx(x, y)] > 0;
2469	    let count = 0;
2470	    for (let i = x0; i < x0 + 120; i++) {
2471	      for (let j = y0; j < y0 + 3; j++) {
2472	        if (!st.inBounds(i, j)) continue;
2473	        if (st.isSolid(i, j) || walled) count++;
2474	      }
2475	    }
2476	    return count >= 120 * 3 * 0.8;
2477	  }
2478	
2479	  /** CountNPCS 近似：优先用 Game 传入的计数表（月事件/星璇塔 ctx 同源），
2480	   *  无事件时退化为 activeIds 的 0/1 检测（Set 去重，无法区分 1 只与 N 只——
2481	   *  登记 docs/spawn-parity-gaps.md）。消费点：地牢外 513 唯一门 / 地表雨云怪 250<2 */
2482	  private countNpc(id: number): number {
2483	    const c = this.moonEvent?.counts.get(id) ?? this.lunar?.counts.get(id);
2484	    if (c != null) return c;
2485	    return this.activeIds.has(id) ? 1 : 0;
2486	  }
2487	
2488	  /** SpawnFrog（NPC.cs:5521-5535 1:1）：!unlockedSlimeYellowSpawn && RollLuck(30) 且
2489	   *  场上无 687 → 神秘青蛙 687（交付 pendingCritterKey 由 Game 转 Critter——687 无
2490	   *  Enemy 数据条目）；RollLuck(400) → 金蛙 445；else 蛙 361。 */
2491	  pendingCritterKey: string | null = null;
2492	  private spawnFrog(rng: RNG): Enemy | null {
2493	    const x = this.spawnTileX * TILE + 8;
2494	    const y = this.spawnTileY * TILE;
2495	    if (!this.world.flags.unlockedSlimeYellowSpawn && rollLuck(this.playerLuck, 30, rng.next) === 0
2496	      && !this.activeIds.has(687)) {
2497	      this.pendingCritterKey = 'mystic_frog';
2498	      return null;
2499	    }
2500	    if (rng.next() < 1 / 400) return this.spawnNPC(x, y, 445, rng);
2501	    return this.spawnNPC(x, y, 361, rng);
2502	  }
2503	
2504	  /** ZoneLihzhardTemple（SceneMetrics.cs:688）：玩家所站格墙 == 87（蜥蜴人砖墙）。
2505	   *  神庙砖怪池门（NPC.cs:3821）与 GetSpawnRate 神庙倍率共用；缺省取本帧玩家格 */
2506	  private zoneLihzardTemple(tx = this.pX, ty = this.pY): boolean {
2507	    const st = this.world.store;
2508	    return st.inBounds(tx, ty) && st.wall[st.idx(tx, ty)] === 87;
2509	  }
2510	
2511	  /** GetGemBunnyToSpawn（NPC.cs:5587-5615 1:1）：Next(100) 分档——琥珀 5%/钻石 8%/
2512	   *  红玉 10%/翠玉 12%/蓝玉 16%/黄玉 21%/紫晶 28%（越稀有权重越低） */
2513	  private getGemBunnyToSpawn(rng: RNG): number {
2514	    const n = Math.floor(rng.next() * 100);
2515	    if (n < 5) return 651;      // Amber Bunny
2516	    if (n < 13) return 652;     // Diamond Bunny
2517	    if (n < 23) return 650;     // Ruby Bunny
2518	    if (n < 35) return 649;     // Emerald Bunny
2519	    if (n < 51) return 648;     // Sapphire Bunny
2520	    if (n < 72) return 647;     // Topaz Bunny
2521	    return 646;                 // Amethyst Bunny
2522	  }
2523	
2524	  /** GetGemSquirrelToSpawn（NPC.cs:5617-5645 1:1）：权重表同上（639-645 松鼠族） */
2525	  private getGemSquirrelToSpawn(rng: RNG): number {
2526	    const n = Math.floor(rng.next() * 100);
2527	    if (n < 5) return 644;      // Amber Squirrel
2528	    if (n < 13) return 645;     // Diamond Squirrel
2529	    if (n < 23) return 643;     // Ruby Squirrel
2530	    if (n < 35) return 642;     // Emerald Squirrel
2531	    if (n < 51) return 641;     // Sapphire Squirrel
2532	    if (n < 72) return 640;     // Topaz Squirrel
2533	    return 639;                 // Amethyst Squirrel
2534	  }
2535	
2536	  /** CheckToSpawnRockGolem（NPC.cs:5713-5728 1:1）：
2537	   *  !hardMode / (落脚≠石 且 非 Moss 族) / ZoneSnow 任一 → false；
2538	   *  Next(50)≠0 → false；落点上方 4 格三连任一实心（WorldGen.SolidTile）→ false */
2539	  private checkToSpawnRockGolem(rng: RNG): boolean {
2540	    if (!this.hardMode) return false;
2541	    if (this.spawnTileType !== T.STONE && !TILE_MOSS.has(this.spawnTileType)) return false;
2542	    if (this.ZoneSnow) return false;
2543	    if (rng.next() >= 1 / 50) return false;   // Main.rand.Next(50)==0
2544	    const st = this.world.store;
2545	    const y4 = this.spawnTileY - 4;
2546	    if (st.isSolid(this.spawnTileX - 1, y4) || st.isSolid(this.spawnTileX, y4)
2547	      || st.isSolid(this.spawnTileX + 1, y4)) return false;
2548	    return true;
2549	  }
2550	
2551	  /** Spawning_SandstoneCheck（NPC.cs:5364-5403 1:1）：沙漠地表蚁狮门。
2552	   *  WorldGen.InWorld(x,y,10) 外 → false；自落脚格向下 ≤8 行逐行计数——本行须为
2553	   *  沙族 tile（中断止），并向两侧各延伸 ≤4 格（遇非沙族中断）；
2554	   *  计数 ≥40 通过（remixWorld 阈值 10 未接——本仓无 remix 世界恒 40） */
2555	  private spawningSandstoneCheck(x: number, y: number): boolean {
2556	    const st = this.world.store;
2557	    if (x < 10 || y < 10 || x > st.w - 10 || y > st.h - 10) return false;
2558	    let num = 0;
2559	    outer: for (let i = 0; i < 8; i++) {
2560	      let t = st.type[st.idx(x, y + i)];
2561	      if (!st.flags[st.idx(x, y + i)] || !TILE_SAND.has(t)) break;
2562	      num++;
2563	      for (let j = 1; j <= 4; j++) {
2564	        t = st.type[st.idx(x + j, y + i)];
2565	        if (!st.flags[st.idx(x + j, y + i)] || !TILE_SAND.has(t)) break;
2566	        num++;
2567	      }
2568	      for (let k = 1; k <= 4; k++) {
2569	        t = st.type[st.idx(x - k, y + i)];
2570	        if (!st.flags[st.idx(x - k, y + i)] || !TILE_SAND.has(t)) break;
2571	        num++;
2572	      }
2573	      if (num >= 40) break outer;
2574	    }
2575	    return num >= 40;
2576	  }
2577	
2578	  /** GetBasicSlimeToSpawn（L5537-5580） */
2579	  /** GetBasicSlimeToSpawn（NPC.cs:5537-5580）1:1。spawnDist = |spawnTileX − 世界出生点X|
2580	   *  （:4111/:4602），地下恒 -1。万圣/圣诞史莱姆门（节日系统未移植,备案） */
2581	  private getBasicSlimeToSpawn(surface: boolean, tileType: number, rng: RNG): number {
2582	    if (!surface) {
2583	      // 地下：Next(5)==0→-9（黄），否则 Next(2)==0→1（蓝）/-8（红）
2584	      if (rng.nextInt(5) === 0) return -9;
2585	      return rng.nextInt(2) === 0 ? 1 : -8;
2586	    }
2587	    switch (tileType) {
2588	      // case 60 = 丛林【草】(原版 :5550)——曾误绑 T.MUD(59 泥,2026-08-13 对齐)
2589	      case T.JUNGLE_GRASS: return -10;
2590	      // case 147/161 = 雪块/【冰块】(:5552-5554)——曾误绑雪砖(148)
2591	      case T.SNOW: case T.ICE: return 147;
2592	      default: {
2593	        // spawnDist 语义:远离出生点(>400)才出紫史莱姆、近出生点(<200)经典档易出绿(:5564-5572)
2594	        const spawnDist = Math.abs(this.spawnTileX - this.world.spawnX);
2595	        if (rng.nextInt(3) === 0 || (spawnDist < 200 && !this.expert)) return -3;
2596	        if (rng.nextInt(10) === 0 && (spawnDist > 400 || this.expert)) return -7;
2597	        return 1;
2598	      }
2599	    }
2600	  }
2601	
2602	  /** 主入口：Game.trySpawnEnemy 调用 */
2603	  spawn(playerX: number, playerY: number, rng: RNG, viewHalfW: number, viewHalfH: number): Enemy | null {
2604	    this.pX = Math.floor(playerX / TILE);
2605	    this.pY = Math.floor(playerY / TILE);
2606	    this.dayTime = this.world.clock.isDay;
2607	    this.hardMode = !!this.world.flags.hardMode;
2608	    this.expert = mainExpertMode(this.world);          // Main.expertMode（GetBasicSlimeToSpawn 绿/紫门用）
2609	    // SetSpawnFlags L321：noWorms = 玩家所站格带房屋墙（房屋内不出蠕虫）
2610	    this.noWorms = this.world.store.inBounds(this.pX, this.pY)
2611	      && WALL_HOUSE.has(this.world.store.wall[this.world.store.idx(this.pX, this.pY)]);
2612	    this.skyMob = false;
2613	    this.spawnSpider = false;
2614	    // 邻近旗标每尝试复位(原版每次 TrySpawnAnNPC 全新置旗;
2615	    // 泄漏会导致碰过大理石后全图永远出蛇发女妖)
2616	    this.nearMarble = false;
2617	    this.nearGranite = false;
2618	    this.spawnUndergroundDesert = false;
2619	    if (!this.findSpawnTile(rng, viewHalfW, viewHalfH)) return null;
2620	    // TrySpawnAnNPC L220：CheckNotSpawningOnScreen 像素级二次校验（画面内/贴屏拒绝）
2621	    if (!this.checkNotSpawningOnScreen(playerX, playerY, viewHalfW, viewHalfH)) return null;
2622	    // GetProperGroundSpawnTileTypeAndWallType（L5789-5792）：tile = 落脚格自身 type，
2623	    // wall = 落脚格【上方一格】的墙（skyMob 天空怪落点无实心面 → tile=0）
2624	    const st = this.world.store;
2625	    const groundType = this.skyMob ? 0 : st.type[st.idx(this.spawnTileX, this.spawnTileY)];
2626	    const spawnWallType = this.spawnTileY > 0
2627	      ? st.wall[st.idx(this.spawnTileX, this.spawnTileY - 1)] : 0;
2628	    // PostCheckChosenSpawnTile（L922-927）：地牢内刷怪点必须踩地牢砖且上方格有墙。
2629	    // 原版失败 = TrySpawnAnNPC return false（L227-230）——整帧放弃，不回选点循环换点重试
2630	    if (this.ZoneDungeon && (!this.isDungeonTile(groundType) || spawnWallType === 0)) return null;
2631	    // :931-940 落脚上方两格均有液体且非岩浆 → 微光/蜂蜜面拒绝（水走 waterTile 水生成链）
2632	    if (this.spawnTileY > 1) {
2633	      const iUp1 = st.idx(this.spawnTileX, this.spawnTileY - 1), iUp2 = st.idx(this.spawnTileX, this.spawnTileY - 2);
2634	      if (st.liquid[iUp1] > 0 && st.liquid[iUp2] > 0 && st.liquidType[iUp1] !== 2
2635	        && (st.liquidType[iUp1] === 3 || st.liquidType[iUp1] === 4)) return null;
2636	    }
2637	    // :943-947 高尔夫草地（477 修剪/492 神圣修剪）：非事件态 1/10 整帧拒绝
2638	    // （invasionType<=0 用 invaders 近前线代理——高尔夫球场+入侵的交集极罕见）
2639	    if ((groundType === T.MOWED_GRASS || groundType === T.HALLOW_MOWED_GRASS)
2640	      && !this.world.clock.bloodMoon && !this.world.clock.eclipse && !this.invaders
2641	      && (!this.moonEvent || this.moonEvent.kind === 0) && !this.world.weather.slimeRain
2642	      && Math.random() * 100 < 10) return null;
2643	    this.setFlagsForChosenTile(this.spawnTileX, this.spawnTileY, groundType, rng);
2644	    this.currentSpawnX = this.spawnTileX;
2645	    this.currentSpawnY = this.spawnTileY;
2646	    // 探针调试覆盖：debugPoolOverride 非空时绕过原版链直接从池选（确定性验证）
2647	    if (debugPoolOverride && debugPoolOverride.length) {
2648	      return this.spawnNPC(this.spawnTileX * 16 + 8, this.spawnTileY * 16,
2649	        debugPoolOverride[rng.int(0, debugPoolOverride.length - 1)], rng);
2650	    }
2651	    return this.spawnAnNPC(rng);
2652	  }
2653	}
2654	

```


---

## 🤖 Assistant · 2026-08-13T05:38:03.962Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have the full VanillaSpawner.ts. Let me now read ScaleStats.ts and the Enemy.ts fromVanilla. Enemy.ts is 336802 bytes — huge. Let me grep for fromVanilla in Enemy.ts.

Let me also find setPlayerFlags call site in Game.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:38:04.120Z · glm-x-preview-260804

```
Now let me examine ScaleStats.ts and find the Enemy.fromVanilla scaling code.
```


---

## 🤖 Assistant · 2026-08-13T05:38:04.264Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:04.493Z

**📎 ToolResult**

```
1	// ============================================================================
2	// 专家/大师世界强度轴 1:1 移植（Terarria1456 ilspycmd 反编译为唯一标杆）
3	//   NPC.ScaleStats                    NPC.cs:18081-18105
4	//   NPC.ScaleStats_ByDifficulty       NPC.cs:18106-18116
5	//   NPC.ScaleStats_ByDifficulty_Tweaks NPC.cs:18118-18447
6	//   NPC.ScaleStats_ForExpertHardmode  NPC.cs:18448-18497
7	//   NPC.ScaleStats_ByPlayerCount      NPC.cs:18498-18659
8	//   GameDifficultyData.LinearCurve    GameDifficultyData.cs:16-70
9	//   GameDifficultyLevel               GameDifficultyLevel.cs:8-16
10	//   Utils.GetLerpValue/Remap          Utils.cs:283-320
11	//   Main.Difficulty/expertMode/masterMode  Main.cs:2760-2786
12	//   NPC.GetAttackDamage_ScaledByDifficulty / ForProjectiles  NPC.cs:7015-7035
13	//   NPC.GetNPCInvasionGroup           NPC.cs:79095-79212
14	//   NPCID.Sets 四张表                 NPCID.cs:4440/4771/4799/4801
15	//
16	// 消费面：Enemy.fromVanilla 造怪（对应原版 NewNPC→SetDefaults→ScaleStats，
17	// NPC.cs:8322/17791 两个调用点都无差别进 ScaleStats，**Boss 不豁免**——
18	// 仅 ScaleStats_ForExpertHardmode 对 boss 提前 return，:18471-18474）。
19	// 本模块纯函数化（状态全走入参/出参 bundle），世界上下文经 bindScaleStatsWorld
20	// 注入（Game.afterWorldLoad；对应原版 Main 静态单例）。
21	// ============================================================================
22	import type { World } from '../world/World';
23	
24	// ---------------------------------------------------------------------------
25	// GameDifficultyLevel（GameDifficultyLevel.cs:8-16）：档位是【浮点值】不是枚举序号
26	//   Journey 0.5 / Classic 1 / Expert 2 / Master 3 / Legendary 4
27	// ---------------------------------------------------------------------------
28	export const GDL = {
29	  JOURNEY: 0.5,
30	  CLASSIC: 1,
31	  EXPERT: 2,
32	  MASTER: 3,
33	  LEGENDARY: 4,
34	} as const;
35	
36	/** float32（C# float 字面量/强转位）。JS number 是 float64，在原版显式 (float) 处对齐 */
37	const f32 = (v: number): number => Math.fround(v);
38	
39	/** C# Math.Round(double)（默认 MidpointRounding.ToEven 银行家舍入：.5 → 就近偶数；
40	 *  JS Math.round 是 .5 远离零舍入，逐半值处会差 1） */
41	export const roundCS = (v: number): number => {
42	  const f = Math.floor(v);
43	  const d = v - f;
44	  if (d < 0.5) return f;
45	  if (d > 0.5) return f + 1;
46	  return f % 2 === 0 ? f : f + 1;
47	};
48	
49	// ---------------------------------------------------------------------------
50	// Utils.GetLerpValue / Remap（Utils.cs:283-320，Remap 重载默认 clamped=true）
51	// ---------------------------------------------------------------------------
52	export function getLerpValue(from: number, to: number, t: number, clamped = false): number {
53	  if (clamped) {
54	    if (from < to) {
55	      if (t < from) return 0;
56	      if (t > to) return 1;
57	    } else {
58	      if (t < to) return 1;
59	      if (t > from) return 0;
60	    }
61	  }
62	  return (t - from) / (to - from);
63	}
64	
65	/** MathHelper.Lerp（XNA：a + (b-a)*t） */
66	export const lerpF = (a: number, b: number, t: number): number => f32(a + f32(b - a) * t);
67	
68	/** Utils.Lerp(double)（:246：a + (b-a)*t，双精度）——ByPlayerCount 的 balance 混合用 */
69	export const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;
70	
71	/** Utils.Remap（:313，默认 clamped=true）——float 重载入参先 (float) 对齐 */
72	export function remap(fromValue: number, fromMin: number, fromMax: number, toMin: number, toMax: number): number {
73	  return lerpF(f32(toMin), f32(toMax), getLerpValue(f32(fromMin), f32(fromMax), f32(fromValue), true));
74	}
75	
76	// ---------------------------------------------------------------------------
77	// GameDifficultyData.LinearCurve（GameDifficultyData.cs:16-60）：
78	//   keys 升序；Sample 找到 value 落入的相邻键区间做线性插值，
79	//   ≤首键输入取首键输出、≥尾键输入取尾键输出
80	// ---------------------------------------------------------------------------
81	export interface CurveKey { input: number; output: number }
82	
83	export function sampleCurve(keys: readonly CurveKey[], value: number): number {
84	  let key = keys[0];
85	  let key2 = key;
86	  for (let i = 0; i < keys.length; i++) {
87	    key2 = keys[i];
88	    if (value <= key2.input) break;
89	    key = key2;
90	  }
91	  const num = f32(key2.input - key.input);
92	  const num2 = f32(key2.output - key.output);
93	  if (num === 0) return key.output;
94	  return f32(f32(f32(value - key.input) * num2) / num + key.output);
95	}
96	
97	// 六条难度曲线（GameDifficultyData.cs:62-70，键值逐项照抄）
98	export const ENEMY_MAX_LIFE_MULTIPLIER: readonly CurveKey[] = [
99	  { input: GDL.JOURNEY, output: 0.5 }, { input: GDL.LEGENDARY, output: 4 },
100	];
101	export const ENEMY_DAMAGE_MULTIPLIER: readonly CurveKey[] = [
102	  { input: GDL.JOURNEY, output: 0.5 }, { input: GDL.MASTER, output: 3 }, { input: GDL.LEGENDARY, output: 5.3333335 },
103	];
104	export const HOSTILE_PROJECTILE_DAMAGE_MULTIPLIER: readonly CurveKey[] = [
105	  { input: GDL.JOURNEY, output: 0.5 }, { input: GDL.MASTER, output: 3 },
106	];
107	export const KNOCKBACK_TO_ENEMIES_MULTIPLIER: readonly CurveKey[] = [
108	  { input: GDL.CLASSIC, output: 1 }, { input: GDL.MASTER, output: 0.8 },
109	];
110	export const ENEMY_MONEY_DROP_MULTIPLIER: readonly CurveKey[] = [
111	  { input: GDL.CLASSIC, output: 1 }, { input: GDL.EXPERT, output: 2.5 },
112	  { input: GDL.MASTER, output: 2.5 }, { input: GDL.LEGENDARY, output: 3.5 },
113	];
114	
115	// ---------------------------------------------------------------------------
116	// Main.Difficulty / expertMode / masterMode（Main.cs:2760-2786）
117	//   ★ GameMode 3（旅程）**不**抬档——旅程世界的 NPC 数值=经典档；真正的旅程
118	//     0.5× 由 _gameModeDifficultyOverride（Main.cs:17245，旅程"给 NPC 的强度"
119	//     滑杆 StrengthMultiplierToGiveNPCs）注入，本仓未建模旅程能力滑杆 → 恒 null。
120	//   ★ getGoodWorld（for the worthy 种子）整体 +1 档（:2783-2785）——经典 FTW 世界
121	//     的 expertMode 即为 true，克脑 40 爬行者/饥饿者专家分支/持械僵尸全数生效。
122	//   我方 world.difficulty：0 经典 / 1 专家 / 2 大师 / 3 旅程（World.ts:73）。
123	// ---------------------------------------------------------------------------
124	export function mainDifficulty(world: Pick<World, 'difficulty' | 'seedFlags'> | null | undefined): number {
125	  let num: number = GDL.CLASSIC;
126	  if (world) {
127	    if (world.difficulty === 1) num = GDL.EXPERT;
128	    else if (world.difficulty === 2) num = GDL.MASTER;
129	    if (world.seedFlags?.getGoodWorld) num += 1;
130	  }
131	  return num;
132	}
133	
134	/** Main.expertMode（Main.cs:2762）：Difficulty >= Expert（getGoodWorld 抬档后同样生效） */
135	export function mainExpertMode(world: Pick<World, 'difficulty' | 'seedFlags'> | null | undefined): boolean {
136	  return mainDifficulty(world) >= GDL.EXPERT;
137	}
138	
139	/** Main.masterMode（Main.cs:2760）：Difficulty >= Master */
140	export function mainMasterMode(world: Pick<World, 'difficulty' | 'seedFlags'> | null | undefined): boolean {
141	  return mainDifficulty(world) >= GDL.MASTER;
142	}
143	
144	// ---------------------------------------------------------------------------
145	// NPCID.Sets（NPCID.cs：Factory.CreateBoolSet(...) 等价"集合包含"）
146	// ---------------------------------------------------------------------------
147	/** NeedsExpertScaling（:4799）：命中即强制进 ScaleStats（无视 lifeMax/damage 门） */
148	export const NEEDS_EXPERT_SCALING = new Set([25, 30, 665, 33, 112, 666, 261, 265, 371, 516, 519, 397, 396, 398, 491]);
149	/** ProjectileNPC（:4801）：弹体 NPC——不缩 life/value，ExpertHardmode 段只乘 damage */
150	export const PROJECTILE_NPC = new Set([25, 30, 665, 33, 112, 666, 261, 265, 371, 516, 519]);
151	/** DontDoHardmodeScaling（:4440）：豁免 ExpertHardmode 兜底增强 */
152	export const DONT_DO_HARDSMODE_SCALING = new Set([5, 13, 14, 15, 267, 113, 114, 115, 116, 117, 118, 119, 658, 659, 660, 400, 522]);
153	/** BelongsToInvasionOldOnesArmy（:4771） */
154	export const OLD_ONES_ARMY = new Set([552, 553, 554, 561, 562, 563, 555, 556, 557, 558, 559, 560, 576, 577, 568, 569, 566, 567, 570, 571, 572, 573, 548, 549, 564, 565, 574, 575, 551, 578]);
155	
156	/** NPC.CommonMasterBossLifeReduction（NPC.cs:6500） */
157	export const COMMON_MASTER_BOSS_LIFE_REDUCTION = 0.85;
158	
159	// ---------------------------------------------------------------------------
160	// 专家档体型放大系数（Tweaks 内 4 处 `scale *=`，NPC.cs:18187/18198/18300/18309）：
161	//   13-15 世吞三段 ×1.2；266/267 克脑+爬行者、134-136 毁灭者三段、139 探针 ×1.05。
162	//   门 difficulty >= Expert（getGoodWorld 抬档后的"经典 FTW"同样命中）。
163	//   单一数据源：Tweaks 与渲染侧 expertRenderScale 共用本表。
164	//   ★只改 npc.scale 不回写宽高——原版 NewNPC 的 width/height×scale 在 ScaleStats
165	//     之前（NPC.cs:17744-17747），故专家档"贴图变大、碰撞盒不变"是原版语义。
166	// ---------------------------------------------------------------------------
167	export function expertScaleMul(type: number): number {
168	  if (type >= 13 && type <= 15) return 1.2;
169	  if (type === 266 || type === 267 || (type >= 134 && type <= 136) || type === 139) return 1.05;
170	  return 1;
171	}
172	
173	/** 渲染侧专家体型系数（Renderer drawEnemy scale 乘区；碰撞盒不动）。
174	 *  世界难度经绑定上下文取（bindScaleStatsWorld，未绑定=经典档恒 1）。 */
175	export function expertRenderScale(type: number, ctx: ScaleStatsWorld | null = null): number {
176	  if ((ctx ?? scaleStatsWorld()).difficulty < GDL.EXPERT) return 1;
177	  return expertScaleMul(type);
178	}
179	
180	// ---------------------------------------------------------------------------
181	// NPC.GetNPCInvasionGroup（NPC.cs:79095-79212）：
182	//   1 哥布林 / 2 雪人军团 / 3 海盗 / 4 火星 / -1 南瓜月 / -2 霜月 / -3 旧日军团 / 0 其他
183	// ---------------------------------------------------------------------------
184	export function getNPCInvasionGroup(npcID: number): number {
185	  if (npcID === 26 || npcID === 27 || npcID === 28 || npcID === 29 || npcID === 111 || npcID === 471 || npcID === 472) return 1;
186	  if (npcID === 143 || npcID === 144 || npcID === 145) return 2;
187	  if (npcID === 212 || npcID === 213 || npcID === 214 || npcID === 215 || npcID === 216
188	    || npcID === 252 || npcID === 491 || npcID === 492 || npcID === 662) return 3;
189	  if (npcID === 381 || npcID === 382 || npcID === 383 || npcID === 385 || npcID === 386 || npcID === 387
190	    || npcID === 388 || npcID === 389 || npcID === 390 || npcID === 391 || npcID === 394 || npcID === 395 || npcID === 520) return 4;
191	  if (npcID >= 338 && npcID <= 352) return -1;
192	  if ((npcID >= 305 && npcID <= 315) || npcID === 325 || npcID === 326 || npcID === 327 || npcID === 329 || npcID === 330) return -2;
193	  if ((npcID >= 547 && npcID <= 578)) return -3;
194	  return 0;
195	}
196	
197	// ---------------------------------------------------------------------------
198	// NPC.GetAttackDamage_* 家族（NPC.cs:7010-7035）——AI 段逐处消费的难度伤害 API
199	// ---------------------------------------------------------------------------
200	/** GetKnockbackMultiplier_ScaledByDifficulty（:7010） */
201	export function getKnockbackMultiplierScaledByDifficulty(normalKnockbackMult: number, difficulty: number): number {
202	  return f32(normalKnockbackMult * sampleCurve(KNOCKBACK_TO_ENEMIES_MULTIPLIER, difficulty));
203	}
204	
205	/** GetAttackDamage_ScaledByDifficulty（:7015）：(int)(normal * EnemyDamageMultiplier.Sample(difficulty)) */
206	export function getAttackDamageScaledByDifficulty(normalDamage: number, difficulty: number): number {
207	  return Math.trunc(f32(normalDamage * sampleCurve(ENEMY_DAMAGE_MULTIPLIER, difficulty)));
208	}
209	
210	/** GetAttackDamage_CappedAtMaster（:7020）：大师以上钳在 Master 档 */
211	export function getAttackDamageCappedAtMaster(normalDamage: number, difficulty: number): number {
212	  const num = Math.min(difficulty, GDL.MASTER);
213	  return Math.trunc(f32(normalDamage * sampleCurve(ENEMY_DAMAGE_MULTIPLIER, num)));
214	}
215	
216	/** GetAttackDamage_ForProjectiles（:7031）：Remap(difficulty, Classic, Expert, normal, expert) */
217	export function getAttackDamageForProjectiles(normalDamage: number, expertDamage: number, difficulty: number): number {
218	  return Math.trunc(remap(difficulty, GDL.CLASSIC, GDL.EXPERT, normalDamage, expertDamage));
219	}
220	
221	/** 敌对弹幕命中玩家的难度乘区（Projectile.cs:264/544 hostileDamageScaling =
222	 *  GameDifficultyData.HostileProjectileDamageMultiplier，Damage_EVP :13770 消费：
223	 *  `if (!reflected) num3 = (int)(num3 * hostileDamageScaling.Sample(Main.Difficulty))`） */
224	export function hostileProjectileDamage(damage: number, difficulty: number): number {
225	  return Math.trunc(f32(damage * sampleCurve(HOSTILE_PROJECTILE_DAMAGE_MULTIPLIER, difficulty)));
226	}
227	
228	// ---------------------------------------------------------------------------
229	// 待缩放属性 bundle（对应 NPC 字段；knockBackResist 用【原版语义】=承受击退比例）
230	// ---------------------------------------------------------------------------
231	export interface ScalingStats {
232	  type: number;
233	  lifeMax: number;
234	  damage: number;
235	  value: number;
236	  defense: number;
237	  knockBackResist: number;
238	  boss: boolean;
239	  friendly: boolean;
240	  townNPC: boolean;
241	  /** npc.scale——Tweaks 专家段 ×1.05/×1.2（:18205-18207 等） */
242	  scale: number;
243	  /** npc.difficulty（ScaleStats 内写入；缺省 0 = 未缩放，对应原版字段初值） */
244	  difficulty: number;
245	}
246	
247	/** 世界上下文（原版 Main 静态的只读投影） */
248	export interface ScaleStatsWorld {
249	  /** Main.Difficulty（Main.cs:2764-2786，mainDifficulty() 求值结果） */
250	  difficulty: number;
251	  /** Main.hardMode */
252	  hardMode: boolean;
253	  /** Main.getGoodWorld */
254	  getGoodWorld: boolean;
255	  /** NPC.downedPlantBoss（ExpertHardmode 段 :18462 +20 阈值） */
256	  downedPlantBoss: boolean;
257	  /** NPC.AnyNPCs(type)（Tweaks/ExpertHardmode 的 getGoodWorld 联动门） */
258	  anyNpc: (type: number) => boolean;
259	  /** NPC.GetActivePlayerCount()（单人恒 1，Main.cs:18518-18521 netMode==0） */
260	  activePlayerCount: number;
261	}
262	
263	/** 经典档缺省上下文（未绑定世界时用——数值与原版 Main 未加载世界时一致走 Classic） */
264	export const CLASSIC_SCALE_WORLD: ScaleStatsWorld = {
265	  difficulty: GDL.CLASSIC, hardMode: false, getGoodWorld: false, downedPlantBoss: false,
266	  anyNpc: () => false, activePlayerCount: 1,
267	};
268	
269	// ---------------------------------------------------------------------------
270	// 世界绑定（Enemy.fromVanilla 无 world 引用；Game.afterWorldLoad 注入，
271	// 对应原版 Main 静态单例语义——存档不持久化缩放值，每次生成现场重算）
272	// ---------------------------------------------------------------------------
273	let boundWorld: ScaleStatsWorld | null = null;
274	
275	export function bindScaleStatsWorld(ctx: ScaleStatsWorld | null): void { boundWorld = ctx; }
276	
277	export function scaleStatsWorld(): ScaleStatsWorld { return boundWorld ?? CLASSIC_SCALE_WORLD; }
278	
279	/** World → ScaleStatsWorld 投影（Game.afterWorldLoad 用；anyNpc 由实体桶实现） */
280	export function scaleStatsWorldOf(
281	  world: Pick<World, 'difficulty' | 'seedFlags' | 'flags'>,
282	  anyNpc: (type: number) => boolean,
283	): ScaleStatsWorld {
284	  return {
285	    difficulty: mainDifficulty(world),
286	    hardMode: !!world.flags?.hardMode,
287	    getGoodWorld: !!world.seedFlags?.getGoodWorld,
288	    downedPlantBoss: !!world.flags?.['downed_262'],
289	    anyNpc,
290	    activePlayerCount: 1,   // 单机（NPC.GetActivePlayerCount :18518 netMode==0 → 1）
291	  };
292	}
293	
294	// ---------------------------------------------------------------------------
295	// NPC.ScaleStats（NPC.cs:18081-18105）
296	// ---------------------------------------------------------------------------
297	export function scaleStats(
298	  s: ScalingStats,
299	  ctx: ScaleStatsWorld = scaleStatsWorld(),
300	  activePlayersCount?: number | null,
301	  strengthOverride?: number | null,
302	): void {
303	  // 入口门（:18083）：NeedsExpertScaling 白名单 或 通用门
304	  //   lifeMax>5 && damage!=0 && !friendly && !townNPC
305	  //   → **Boss 不豁免**（boss 不在排除条件里）；ProjectNPC（25/30/…）靠白名单进入
306	  if (NEEDS_EXPERT_SCALING.has(s.type) || (s.lifeMax > 5 && s.damage !== 0 && !s.friendly && !s.townNPC)) {
307	    s.difficulty = strengthOverride != null ? strengthOverride : ctx.difficulty;   // :18086
308	    if (s.difficulty >= GDL.EXPERT && ctx.hardMode) scaleStatsForExpertHardmode(s, ctx);  // :18087-18089
309	    scaleStatsByDifficulty(s, ctx);                                                 // :18090
310	    if (s.difficulty >= GDL.EXPERT) {
311	      scaleStatsByPlayerCount(s, activePlayersCount != null ? activePlayersCount : ctx.activePlayerCount);  // :18091-18094
312	    }
313	    // :18096-18100 弹体 NPC 以外 lifeMax 下限 6（经典档同样生效）
314	    if ((s.type < 0 || !PROJECTILE_NPC.has(s.type)) && s.lifeMax < 6) s.lifeMax = 6;
315	    // :18101-18103 defDamage/defDefense/defLifeMax 快照 → 调用侧另存 baseDamage/baseDefense
316	  }
317	}
318	
319	// ---------------------------------------------------------------------------
320	// NPC.ScaleStats_ByDifficulty（NPC.cs:18106-18116）
321	// ---------------------------------------------------------------------------
322	function scaleStatsByDifficulty(s: ScalingStats, ctx: ScaleStatsWorld): void {
323	  if (s.type < 0 || !PROJECTILE_NPC.has(s.type)) {                       // :18108-18112
324	    s.lifeMax = Math.trunc(f32(s.lifeMax * sampleCurve(ENEMY_MAX_LIFE_MULTIPLIER, s.difficulty)));
325	    s.value = Math.trunc(f32(s.value * sampleCurve(ENEMY_MONEY_DROP_MULTIPLIER, s.difficulty)));
326	  }
327	  s.damage = getAttackDamageScaledByDifficulty(s.damage, s.difficulty);  // :18113
328	  s.knockBackResist = getKnockbackMultiplierScaledByDifficulty(s.knockBackResist, s.difficulty);  // :18114
329	  scaleStatsByDifficultyTweaks(s, ctx);                                  // :18115
330	}
331	
332	// ---------------------------------------------------------------------------
333	// NPC.ScaleStats_ByDifficulty_Tweaks（NPC.cs:18118-18447）
334	//   num=伤害系数（Classic→Expert）/ num2=生命 Classic→Expert / num3=生命 Expert→Master
335	// ---------------------------------------------------------------------------
336	function scaleStatsByDifficultyTweaks(s: ScalingStats, ctx: ScaleStatsWorld): void {
337	  let num = 1.0;   // damage
338	  let num2 = 1.0;  // lifeMax (classic→expert)
339	  let num3 = 1.0;  // lifeMax (expert→master)
340	  const type = s.type;
341	
342	  // ---- getGoodWorld 世吞/骷髅王/血肉墙本体降容联动（:18125-18152）----
343	  //   6 世吞头 且 AnyNPCs(13)（世吞在场）→ 大师生命数 ×0.85、伤害 ×1.5、专家防 +2
344	  //   32 腐化头 且 AnyNPCs(35)（骷髅王在场）→ 同上、专家防 +6
345	  //   24 火妖 且 AnyNPCs(113)（血肉墙在场）→ 同上、专家防 +10
346	  if (ctx.getGoodWorld) {
347	    if (type === 6 && ctx.anyNpc(13)) {
348	      num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
349	      num2 *= 1.5;
350	      if (s.difficulty >= GDL.EXPERT) s.defense += 2;
351	    }
352	    if (type === 32 && ctx.anyNpc(35)) {
353	      num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
354	      num2 *= 1.5;
355	      if (s.difficulty >= GDL.EXPERT) s.defense += 6;
356	    }
357	    if (type === 24 && ctx.anyNpc(113)) {
358	      num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
359	      num2 *= 1.5;
360	      if (s.difficulty >= GDL.EXPERT) s.defense += 10;
361	    }
362	  }
363	
364	  // ---- 类型逐档系数（:18154-18386；else-if 链，先命中先得）----
365	  //   210/211 蜂/毒蜂：生命 ×0.6、伤害 ×0.6、专家防御 Remap(1,0.8)
366	  if (type === 210 || type === 211) {
367	    num2 = 0.6;                       // 原文 0.6000000000000001 (double) → (float) 后为 0.6
368	    num = 0.6;
369	    s.defense = Math.trunc(remap(s.difficulty, GDL.CLASSIC, GDL.EXPERT, 1, 0.8) * s.defense);
370	  } else if (type === 5) {            // 5 克眼仆从（ServantOfCthulhu，:18159-18163 num2=0.75）
371	    num2 = 0.75;
372	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
373	  } else if (type === 4) {            // 4 克苏鲁之眼
374	    num2 = 0.65;
375	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
376	  } else if (type >= 13 && type <= 15) {  // 世吞三段
377	    num2 = 0.7;
378	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
379	    if (type === 13) num *= 1.1;      // 头
380	    if (type === 14) num *= 0.8;      // 身
381	    if (type === 15) num *= 0.8;      // 尾
382	    if (s.difficulty >= GDL.EXPERT) { s.scale *= expertScaleMul(type); s.defense += 2; }
383	  } else if (type === 266 || type === 267) {  // 克脑 + 爬行者
384	    num2 = 0.85;
385	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
386	    num *= 0.9;
387	    if (s.difficulty >= GDL.EXPERT) s.scale *= expertScaleMul(type);
388	  } else if (type === 50) {           // 50 骷髅王
389	    num2 = 0.7;
390	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
391	    num *= 0.8;
392	  } else if (type === 471) {          // 471 哥布林召唤师
393	    num2 = 0.85;
394	  } else if (type === 472) {          // 472 哥布林召唤师(暗影焰)
395	    num2 = 0.85;
396	    num = 0.8;
397	  } else if (type === 492) {          // 492 海盗神射手
398	    num2 = 0.85;
399	  } else if (type === 393 || type === 394 || type === 395) {  // 火星飞碟三段
400	    num2 = 0.85;
401	  } else if (type === 222) {          // 222 蜂后
402	    num2 = 0.7;
403	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
404	    num = 0.9;
405	  } else if (type === 35) {           // 35 骷髅王头(地牢守卫同 id 族)
406	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
407	    num = 1.1;
408	  } else if (type === 36) {           // 36 骷髅王手
409	    num2 = 1.3;
410	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
411	    num = 1.1;
412	  } else if (type === 668) {          // 668 帝王凝胶(史莱姆皇后召唤物)
413	    num2 = 0.85;
414	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
415	  } else if (type === 113 || type === 114) {  // 血肉墙 / 之眼
416	    num2 = 0.7;
417	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
418	    num = 1.5;
419	    if (s.difficulty >= GDL.EXPERT) s.defense += 6;
420	  } else if (type === 115) {          // 115 饥饿者
421	    num2 = 0.7;
422	    if (s.difficulty >= GDL.EXPERT) s.defense += 6;
423	  } else if (type === 116) {          // 116 饥饿者 II
424	    num2 = 0.7;
425	  } else if (type === 117 || type === 118 || type === 119) {  // 憎恶蜂群
426	    num2 = 0.8;
427	  } else if (type === 657) {          // 657 史莱姆皇后
428	    num2 = 0.8;
429	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
430	  } else if (type >= 658 && type <= 660) {  // 皇后水晶/水晶仆从
431	    num2 = 0.75;
432	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
433	  } else if (type >= 134 && type <= 136) {  // 毁灭者三段
434	    num2 = 0.75;
435	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
436	    if (type === 134) num *= 2.0;     // 头
437	    if (type === 135) num *= 0.85;    // 身
438	    if (type === 136) num *= 0.85;    // 尾
439	    if (s.difficulty >= GDL.EXPERT) s.scale *= expertScaleMul(type);
440	  } else if (type === 139) {          // 139 毁灭者探针
441	    num2 = 0.75;
442	    num = 0.8;
443	    if (s.difficulty >= GDL.EXPERT) s.scale *= expertScaleMul(type);
444	  } else if (type >= 127 && type <= 131) {  // 机械骷髅王 + 部件
445	    num2 = 0.75;
446	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
447	    num = 0.85;
448	  } else if (type >= 125 && type <= 126) {  // 双子魔眼
449	    num2 = 0.75;
450	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
451	    num = 0.85;
452	  } else if (type === 262) {          // 262 世纪之花
453	    num2 = 0.7;
454	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
455	    num = 1.15;
456	  } else if (type === 264) {          // 264 世纪之花钩/触手
457	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
458	    num = 1.15;
459	  } else if (type === 636) {          // 636 光之女皇
460	    num2 = 0.7;
461	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
462	  } else if (type >= 245 && type <= 249) {  // 石巨人族
463	    num2 = 0.75;
464	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
465	    num = 0.8;
466	  } else if (type === 370) {          // 370 猪龙鱼公爵
467	    num2 = 0.65;
468	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
469	    num = 0.7;
470	  } else if (type === 371 || type === 372 || type === 373) {  // 猪鲨气泡/鲨龙卷
471	    if (type !== 371) num2 = 0.75;
472	    num = 0.75;
473	  } else if (type === 439 || type === 440 || (type >= 454 && type <= 459) || type === 522 || type === 523) {
474	    // 拜月教邪教徒 439/440、拜月教忠实信徒 454-459、邪教弓手 522/523
475	    if (type !== 522) {
476	      num2 = 0.75;
477	      num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
478	    }
479	    num = 0.75;
480	  } else if (type === 397 || type === 396 || type === 398) {  // 月总手/头/核心
481	    num2 = 0.75;
482	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
483	    num = 0.75;
484	  } else if (type === 551) {          // 551 火星走卒(地表 UFO)
485	    num2 = 0.75;
486	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
487	    num = 0.65;
488	  } else if (OLD_ONES_ARMY.has(type)) {  // 旧日军团全体
489	    num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
490	  }
491	
492	  // ---- 月事件入侵组（:18388-18420）----
493	  const invasionGroup = getNPCInvasionGroup(type);
494	  if (invasionGroup === -2 || invasionGroup === -1) {
495	    switch (type) {
496	      // 哀木 325 / 南瓜王 327 / 冰女王 345 / 圣诞坦克 346 / 精灵直升机 344：
497	      // 生命 ×0.65、大师生命 ×0.85、伤害 ×0.75
498	      case 315: case 325: case 327: case 344: case 345: case 346:
499	        num2 = 0.65;
500	        num3 *= COMMON_MASTER_BOSS_LIFE_REDUCTION;
501	        num = 0.75;
502	        break;
503	      default:                        // 其余南瓜/霜月杂兵：生命 ×0.75、伤害 ×0.75
504	        num2 = 0.75;
505	        num = 0.75;
506	        break;
507	    }
508	  }
509	
510	  // ---- 汇总（:18422-18433）----
511	  let num4 = 1;
512	  num4 *= remap(s.difficulty, GDL.CLASSIC, GDL.EXPERT, 1, f32(num2));
513	  num4 *= remap(s.difficulty, GDL.EXPERT, GDL.MASTER, 1, f32(num3));
514	  s.lifeMax = roundCS(f32(f32(s.lifeMax) * num4));
515	  let num5 = 1;
516	  num5 *= remap(s.difficulty, GDL.CLASSIC, GDL.EXPERT, 1, f32(num));
517	  s.damage = roundCS(f32(f32(s.damage) * num5));
518	}
519	
520	// ---------------------------------------------------------------------------
521	// NPC.ScaleStats_ForExpertHardmode（NPC.cs:18448-18497）
522	//   专家+困难模式 的"杂兵兜底增强"：把 damage+defense+lifeMax/4 拉到 80
523	//   （世花后 100）的强度水位。boss / lifeMax>=1000 / DontDoHardmodeScaling 全豁免。
524	// ---------------------------------------------------------------------------
525	function scaleStatsForExpertHardmode(s: ScalingStats, ctx: ScaleStatsWorld): void {
526	  const isProj = s.type >= 0 && PROJECTILE_NPC.has(s.type);   // :18449
527	  let flag2 = !DONT_DO_HARDSMODE_SCALING.has(s.type);         // :18450
528	  if (ctx.getGoodWorld) {                                     // :18452-18468
529	    if ((s.type === 24 || s.type === 25) && ctx.anyNpc(113)) flag2 = false;
530	    if ((s.type === 32 || s.type === 33) && ctx.anyNpc(35)) flag2 = false;
531	    if (s.type === 6 && ctx.anyNpc(13)) flag2 = false;
532	  }
533	  if (s.boss || s.lifeMax >= 1000) flag2 = false;             // :18469-18472 ★Boss 豁免点
534	  if (!flag2) return;
535	
536	  let num = s.damage + s.defense + Math.trunc(s.lifeMax / 4); // :18476-18478 (int 除法)
537	  if (num === 0) num = 1;
538	  let num2 = 80;                                              // :18480
539	  if (ctx.downedPlantBoss) num2 += 20;                        // :18481-18483
540	  if (num < num2) {                                           // :18484
541	    const num3 = f32(num2 / num);
542	    s.damage = Math.trunc(f32(f32(s.damage * num3) * 0.9));   // :18486
543	    if (!isProj) {                                            // :18487-18492
544	      s.defense = Math.trunc(f32(s.defense * num3));
545	      s.lifeMax = Math.trunc(f32(f32(s.lifeMax * num3) * 1.1));
546	      s.value = Math.trunc(f32(f32(s.value * num3) * 0.8));
547	    }
548	  }
549	}
550	
551	// ---------------------------------------------------------------------------
552	// NPC.ScaleStats_ByPlayerCount（NPC.cs:18498-18659）
553	//   多人玩家数缩放。单人 balance=1 → 全部 `num *= balance` 恒等，仅多人有意义；
554	//   击退段全部门在 numPlayers>1，单人同样恒等。1:1 抄录以备多人接入。
555	// ---------------------------------------------------------------------------
556	export function getStatScalingFactors(numPlayers: number): { balance: number; boost: number } {
557	  let balance = 1;
558	  let boost = 0.35;
559	  for (let i = 1; i < numPlayers; i++) {
560	    balance += boost;
561	    boost += (1 - boost) / 3;
562	  }
563	  if (balance > 8) balance = (balance * 2 + 8) / 3;
564	  if (balance > 1000) balance = 1000;
565	  return { balance, boost };
566	}
567	
568	function scaleStatsByPlayerCount(s: ScalingStats, numPlayers: number): void {
569	  const { balance, boost } = getStatScalingFactors(numPlayers);
570	  let num = 1.0;
571	  const type = s.type;
572	  if (type === 4) num *= balance;
573	  if (type >= 13 && type <= 15) {
574	    num *= balance;
575	    // 世吞：balance 每 +0.34 一档削击退（:18508-18524）
576	    for (let num2 = 1; num2 < balance; num2 += 0.34) {
577	      if (s.knockBackResist < 0.1) { s.knockBackResist = 0; break; }
578	      s.knockBackResist *= 0.8;
579	    }
580	  }
581	  if (type === 266 || type === 267) num *= balance;
582	  if (type === 50) num *= balance;
583	  if (type === 471) num *= lerp(1, balance, 2 / 3);
584	  if (type === 472) num *= lerp(1, balance, 0.5);
585	  if (type === 222) num *= balance;
586	  if (type === 35) num *= balance;
587	  else if (type === 36) num *= balance;
588	  if (type === 668) num *= balance;
589	  if (type === 113 || type === 114) num *= balance;
590	  else if (type === 115) {
591	    num *= balance;
592	    if (numPlayers > 4) s.knockBackResist = 0;
593	    else if (numPlayers > 1) s.knockBackResist *= 1 - boost;
594	  } else if (type === 116) {
595	    num *= balance;
596	    if (numPlayers > 4) s.knockBackResist = 0;
597	    else if (numPlayers > 1) s.knockBackResist *= 1 - boost;
598	  }
599	  if (type === 657) num *= balance;
600	  if (type >= 658 && type <= 660) num *= balance;
601	  if (type >= 134 && type <= 136) num *= balance;
602	  else if (type === 139) num *= lerp(1, balance, 2 / 3);
603	  if (type >= 127 && type <= 131) num *= balance;
604	  if (type >= 125 && type <= 126) num *= balance;
605	  if (type === 262) num *= balance;
606	  else if (type === 264) num *= balance;
607	  if (type === 636) num *= balance;
608	  if (type >= 245 && type <= 249) num *= balance;
609	  if (type === 370) num *= balance;
610	  if (type === 439 || type === 440 || (type >= 454 && type <= 459) || type === 523) num *= balance;
611	  if (type === 397 || type === 396 || type === 398) num *= balance;
612	  if (type === 551) num *= balance;
613	  else if (OLD_ONES_ARMY.has(type)) num *= lerp(1, balance, 6 / 7);   // 原文 0.8571428656578064
614	  const invasionGroup = getNPCInvasionGroup(type);
615	  if (invasionGroup === -2 || invasionGroup === -1) {
616	    switch (type) {
617	      case 315: case 325: case 327: case 344: case 345: case 346:
618	        break;   // 月事件 Boss 不吃玩家数生命加成（:18648-18653）
619	      default:
620	        num *= 1 + (numPlayers - 1) * 0.2;
621	        break;
622	    }
623	  }
624	  s.lifeMax = roundCS(s.lifeMax * num);
625	}
626	

```


---

## 🤖 Assistant · 2026-08-13T05:38:04.631Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"fromVanilla\\|scaleStats\\|difficulty\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -60",
 "description": "Find fromVanilla and scaleStats in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:04.676Z

**📎 ToolResult**

```
57:  scaleStats, getAttackDamageForProjectiles, type ScalingStats,
123:/** 原版路径 key（v_*）的占位 def，fromVanilla 会整体覆写 */
134:  /** npc.difficulty（ScaleStats 写入，NPC.cs:18086 = strengthOverride ?? Main.Difficulty）：
138:  difficulty = 0;
451:    const spit = Enemy.fromVanilla(666, this.cx + this.vx, this.cy + this.vy);
464:      const s = Enemy.fromVanilla(id, head.cx, head.cy);
476:  static fromVanilla(id: number, x: number, y: number): Enemy | null {
498:      scale: v.scale ?? 1, difficulty: 0,
500:    scaleStats(ss);
501:    e.difficulty = ss.difficulty;          // npc.difficulty（AI 段 GetAttackDamage_* 消费）
1506:        this.kbResistOverride = getKnockbackMultiplierScaledByDifficulty(0.4, this.difficulty);
2692:    // 未初始化(-1120)自愈：绕过 VanillaSpawner 锚点传参的生成路径(fromVanilla/
2884:          const spit = Enemy.fromVanilla(112, this.cx, this.cy);
4036:      const slave = Enemy.fromVanilla(1, this.cx, this.cy);
4182:   *  （:17615，fromVanilla 侧已置 dontTakeDamage）。伪装态 ai[0]=0：timeLeft=60 恒续命、
4513:            const dmg = getAttackDamageForProjectiles(30, 25, this.difficulty);
4875:        const ball = Enemy.fromVanilla(ballId,
4888:        // Remap(difficulty, Classic, Expert, 基线, 基线×0.8)（大师钳在 Expert 端）。
4893:          (vid <= 282 || vid >= 285 ? 40 : 30) * 0.8, this.difficulty);
4941:        const dmg172 = getAttackDamageForProjectiles(40, 32, this.difficulty);
5172:            const s = Enemy.fromVanilla(5, this.cx + (dx / dist) * 10, this.cy + (dy / dist) * 10);
5255:        const s = Enemy.fromVanilla(5, this.cx + (rx / rl) * 10, this.cy + (ry / rl) * 10);
5291:      // fromVanilla 已是拷贝，恒等判断最多拷一次）
5866:        const h2 = Enemy.fromVanilla(116, this.cx, this.y + this.h);
5880:          const b = Enemy.fromVanilla(1, this.cx + (Math.random() - 0.5) * 28, this.cy - 6);
5930:        // （曾错接 p.appearance.difficulty：专家掉落/宝袋被角色难度误触发）

```


---

## 🤖 Assistant · 2026-08-13T05:38:09.750Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the fromVanilla section in Enemy.ts (around lines 476-520 and the difficulty field around line 134).
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:38:09.751Z · glm-x-preview-260804

```
Let me read the fromVanilla implementation in Enemy.ts and find the Game.ts call sites.
```


---

## 🤖 Assistant · 2026-08-13T05:38:09.857Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 80,
 "offset": 470
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:09.876Z

**📎 ToolResult**

```
470	    }
471	    return segs;
472	  }
473	
474	
475	  /** 用原版数据造怪：属性/碰撞/音效全部来自 SetDefaults 提取值 */
476	  static fromVanilla(id: number, x: number, y: number): Enemy | null {
477	    const v = vanillaNpc(id);
478	    if (!v) return null;
479	    const e = new Enemy(`v_${id}`, x, y);
480	    e.vanillaId = id;
481	    e.vanilla = v;
482	    const hit = vanillaSoundName(v.HitSound) ?? 'NPC_Hit_1';
483	    const kill = vanillaSoundName(v.DeathSound) ?? 'NPC_Killed_1';
484	    const flying = v.noGravity || v.aiStyle === 2 || v.aiStyle === 5 || v.aiStyle === 14;
485	    // ---- NPC.ScaleStats（NPC.cs:18081-18105，NewNPC→SetDefaults 后调用 :8322/:17791）----
486	    // 世界难度轴（Main.Difficulty → 生命/伤害/钱/击退倍率 + 逐类型系数 +
487	    // 专家困难模式兜底增强）。Boss **不豁免**（仅 ExpertHardmode 段跳过 :18471）。
488	    // 上下文经 bindScaleStatsWorld 注入（Game.afterWorldLoad；原版 Main 静态单例语义），
489	    // 未绑定=经典档（倍率恒 1，仅 lifeMax<6 下限与类型系数在 Classic 档同样无变化）。
490	    const rawDamage = (v.critter || v.friendly) ? 0 : v.damage;   // def.damage 基线
491	    // 原版"承受比例"语义——缺省 1f（NPC.cs:8449 SetDefaults 默认 knockBackResist=1,
492	    // JSON 提取表只写显式赋值,无字段的 137 只（克眼仆从等）此前落 0.5 吃半击退,2026-08-13 修正）
493	    const rawKb = v.knockBackResist ?? 1;
494	    const ss: ScalingStats = {
495	      type: id, lifeMax: v.lifeMax, damage: v.damage, value: npcValueOf(id),
496	      defense: v.defense, knockBackResist: rawKb,
497	      boss: VANILLA_BOSS_IDS.has(id), friendly: !!v.friendly, townNPC: !!v.townNPC,
498	      scale: v.scale ?? 1, difficulty: 0,
499	    };
500	    scaleStats(ss);
501	    e.difficulty = ss.difficulty;          // npc.difficulty（AI 段 GetAttackDamage_* 消费）
502	    e.baseDamage = rawDamage;              // defDamage 快照的【未缩放】基线（弹幕出膛用）
503	    // def.knockBackResist 直存原版"承受比例"语义（ScaleStats :307 缩放后仍是比例；
504	    // hurt() 无条件 kbx*resist——0=免疫、1=全额）。旧"1-比例"换算+0.89 钳已废（2026-08-13）
505	    const kbr = ss.knockBackResist;
506	    e.def = {
507	      ...e.def,
508	      // friendly（被缚 NPC 等城镇系）与 critter 一样零接触伤害——原版 friendly 旗
509	      name: v.name, hp: ss.lifeMax, damage: rawDamage !== 0 ? ss.damage : 0, defense: ss.defense,
510	      // 原版 knockBackResist="承受击退的比例"（0=免疫 Boss、0.5=吃一半、1=全额）
511	      knockbackResist: kbr,
512	      width: Math.round(v.width * (v.scale ?? 1)), height: Math.round(v.height * (v.scale ?? 1)), flying,
513	      boss: VANILLA_BOSS_IDS.has(id),
514	      nightOnly: v.aiStyle === 2 || v.aiStyle === 5, underground: false,
515	      mapColor: '#9A8FA0', gore: ['#9A8FA0', '#5E5566', '#C4BACC'],
516	      hitSound: [hit], killedSound: [kill], drops: [], // 掉落走 NpcDrops 规则树（击杀时求值，不再预展开）
517	      // ScaleStats 后的 npc.value（EnemyMoneyDropMultiplier 已乘，经典档=原值；
518	      // 弹体 NPC 不缩）——击杀掉钱消费位（Enemy.ts 掉落 ctx.value）
519	      value: ss.value,
520	      // 小动物：无接触伤害、不夜行（ScaleStats 对 damage=0/lifeMax≤5 的它们本就不进门）
521	      ...(v.critter ? { damage: 0, nightOnly: false } : {}),
522	    };
523	    // 接触伤害：战斗怪 = ScaleStats 缩放后 npc.damage（damage!=0 的 friendly/critter
524	    // 恒 0，与旧归零语义一致）
525	    e.hp = ss.lifeMax;
526	    e.maxHp = ss.lifeMax;
527	    // 碰撞盒乘 npc.scale(NPC.cs:17747-17748 width/height=(int)(×scale))——
528	    // 史莱姆王/毁灭者 1.25、血肉墙 1.2:此前未乘,贴图放大了盒子没放大,
529	    // 判定区比视觉小一圈(与渲染 scale 不一致的"盒贴图不匹配"来源)
530	    const vScale = v.scale ?? 1;
531	    e.w = Math.round(v.width * vScale);
532	    e.h = Math.round(v.height * vScale);
533	    e.spawnAlpha = v.alpha ?? 0; // 原版 SetDefaults alpha（静态不透明度，NPC.Opacity=1-alpha/255）
534	    // alpha=255 = 出生全透明渐显标记（13-15 世吞 / 134-136 毁灭者；其余 alpha 为
535	    // 静态不透明度,勿动）：置 alphaFade 交渐显路径逐 tick 减回 0。EoW 族保持原版
536	    // 初值 255（AI_006 尾段 :52650-52670 移动门 -42/t，见 fixedUpdate 渐显段）；
537	    // 其余 alpha=255 族沿用 254 起步走 -1/t 近似
538	    if (e.spawnAlpha >= 255) {
539	      e.alphaFade = true;
540	      e.spawnAlpha = (id >= 13 && id <= 15) ? 255 : 254;
541	    }
542	    e.colorRGBA = v.color ? [v.color[0], v.color[1], v.color[2], v.color[3] ?? 255] : null; // 原版 color 字段
543	    // 266 克脑 SetDefaults :12372 dontTakeDamage=true——一阶段（爬行者存活）不可击，
544	    // AI_054 二阶段入场段 :32589 自行解除（存档载入即二阶段也由该段下一 tick 清除）
545	    if (id === 266) e.dontTakeDamage = true;
546	    // 263 世纪之花钩蔓 SetDefaults :12331-12332 dontTakeDamage=true——恒不可击
547	    // （AI_052 本体消失时自伤 9999 走直改 hp 通道,不受此门禁阻塞）
548	    if (id === 263) e.dontTakeDamage = true;
549	    // 690 雕像宝箱怪 SetDefaults :17615-17627 immortal+dontTakeDamage=true——伪装态

```


---

## 🤖 Assistant · 2026-08-13T05:38:10.406Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"setPlayerFlags\\|bindScaleStatsWorld\\|scaleStatsWorldOf\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v \"VanillaSpawner.ts\\|ScaleStats.ts\"",
 "description": "Find setPlayerFlags and bindScaleStatsWorld call sites"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:10.488Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:112:import { bindScaleStatsWorld, scaleStatsWorldOf, mainExpertMode, mainMasterMode } from '../stats/ScaleStats';
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1636:    bindScaleStatsWorld(scaleStatsWorldOf(w, (type) => this.entities.enemies.some(
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8914:    this.vanillaSpawner.setPlayerFlags(!!this.scene?.zoneDungeon,
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:488:    // 上下文经 bindScaleStatsWorld 注入（Game.afterWorldLoad；原版 Main 静态单例语义），

```


---

## 🤖 Assistant · 2026-08-13T05:38:11.897Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at the Game.ts call sites: line 1636 (bindScaleStatsWorld) and 8914 (setPlayerFlags). Also the trySpawnEnemy / getSpawnRate callers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:38:12.087Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 30,
 "offset": 1625
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:12.097Z

**📎 ToolResult**

```
1625	    await this.preloadSceneAssets((label, p) => onProgress?.(label, 0.8 + p * 0.2));
1626	    this.afterWorldLoad();
1627	    this.cb.onWorldReady();
1628	  }
1629	
1630	  private afterWorldLoad() {
1631	    const w = this.world;
1632	    // 专家/大师强度轴上下文注入（NPC.ScaleStats 的 Main 静态投影，
1633	    // src/stats/ScaleStats.ts；newWorld worker/主线程两路与 loadWorld 都汇到此处）。
1634	    // 存档不持久化缩放值（WorldFile.SaveNPCs :1703-1746 只存城镇 NPC 的
1635	    // active/netID/position），每次 fromVanilla 现场重算——绑对象引用即可读最新档
1636	    bindScaleStatsWorld(scaleStatsWorldOf(w, (type) => this.entities.enemies.some(
1637	      (en) => { const e2 = en as Enemy; return !e2.dead && e2.vanillaId === type; })));
1638	    // 旧日军团事件依赖接线（bossAI_dd2.ts DD2_EVENT_HOOKS 占位正式落地）
1639	    this.wireDD2Hooks();
1640	    // 晶塔表首扫（wld 导入的既有晶塔即刻可点；放置/破坏时 refreshPylons 增量刷）
1641	    this.refreshPylons();
1642	    // 常用声效小集合预热（按需加载体系下的目标预热，异步不阻塞：
1643	    // 战斗/挖掘/拾取等开局即用的 ~20 个小 wav；怪物专属声仍随首次受击懒加载）
1644	    this.sfx.preloadNames(['hit', 'hurt', 'killed', 'pkilled', 'pickup', 'dig', 'place',
1645	      'chop', 'tink', 'shatter', 'coin', 'door_open', 'door_close', 'splash', 'bowShoot', 'throw', 'roar', 'thunder',
1646	      'explosion', 'summon', 'whipCrack']); // Item_14 爆炸/Item_44 召唤/Item_152 鞭——不预热则首播静音
1647	    this.sfx.preloadFiles(['Drip_0', 'Drip_1', 'Drip_2']); // 滴水溅落（SoundID 39，Gore 碰撞/入水）
1648	    // 敌怪弹幕发射音（Dart DART_STYLE sfx 直放文件名）：箭 Item_5 已在 bowShoot 预热,
1649	    // 其余不预热则各射击怪本局首射静音
1650	    this.sfx.preloadFiles(['Item_8', 'Item_11', 'Item_12', 'Item_17', 'Item_20', 'Item_28', 'Item_154']);
1651	    // 滴水溅落音钩子（Gore.cs :971-984：落地 Drip_0/1 随机、入水 Drip_2、位置 +8；
1652	    // 带坐标走 2500px 距离衰减，flag4 水型已在 NatureParticles 内静音）
1653	    natureParticles.onDripSplash = (x, y, wet) => {
1654	      this.sfx.playFiles(wet ? ['Drip_2'] : ['Drip_0', 'Drip_1'], 1, x, y);

```


---

## 🤖 Assistant · 2026-08-13T05:38:12.343Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 130,
 "offset": 8870
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:12.364Z

**📎 ToolResult**

```
8870	      this.entities.npcs.filter((n) => n instanceof TownNPC && !n.dead).map((n) => (n as TownNPC).cx));
8871	    const activeIds = new Set<number>();
8872	    // 月事件选怪需要 CountNPCS（场上同 id 数量）与 Boss 族 npcSlots 总和
8873	    // （reachedInvasionBossCap，NPC.cs:159-183）——activeIds 只去重不够，同轮统计
8874	    const moonCounts = new Map<number, number>();
8875	    let moonBossSlotSum = 0;
8876	    for (const e of this.entities.enemies) {
8877	      const en = e as Enemy;
8878	      if (en.dead || en.vanillaId == null) continue;
8879	      activeIds.add(en.vanillaId);
8880	      moonCounts.set(en.vanillaId, (moonCounts.get(en.vanillaId) ?? 0) + 1);
8881	      if (MOON_BOSS_IDS.has(en.vanillaId)) moonBossSlotSum += en.vanilla?.npcSlots ?? 1;
8882	    }
8883	    // bound TownNPC → 绑缚原版 id 登记（原版被缚 NPC 本体就是 105/106/123/354/589/685
8884	    // 类型，AnyNPCs 直接可见；本仓 bound 态以 TownNPC 近似 → 反查登记，使三人组链的
8885	    // !AnyNPCs(105/106/685) 场上唯一门与机械师/造型师/高尔夫球手各支同语义）
8886	    for (const n of this.entities.npcs) {
8887	      const tn = n as TownNPC;
8888	      if (!(tn instanceof TownNPC) || tn.dead || !tn.bound) continue;
8889	      const boundId = Game.BOUND_TOWN_NPC_ID[tn.npcKey];
8890	      if (boundId !== undefined) activeIds.add(boundId);
8891	    }
8892	    const moonCtx = w.moonEvent.kind !== 0
8893	      ? { kind: w.moonEvent.kind, wave: w.moonEvent.waveNumber, counts: moonCounts, bossSlotSum: moonBossSlotSum }
8894	      : null;
8895	    // 星璇塔 Zone（SceneMetrics.cs:276-282：玩家与场上塔 NPC 距离 <4000px）+
8896	    // 选表 CountNPCS 复用上面统计的 counts 表。任一塔 Zone → spawner 走 invaders 语义
8897	    // （SetSpawnFlags :315-318）+ SpawnAnNPC 链头四塔选怪段
8898	    let lunar: LunarSpawnCtx | null = null;
8899	    if (w.lunarEvent.active) {
8900	      const zone = { solar: false, vortex: false, nebula: false, stardust: false };
8901	      for (const e of this.entities.enemies) {
8902	        const en = e as Enemy;
8903	        if (en.dead || en.vanillaId == null) continue;
8904	        const k = TOWER_KEY[en.vanillaId];
8905	        if (!k) continue;
8906	        if (Math.hypot(en.cx - p.cx, en.cy - p.cy) < TOWER_ZONE_RADIUS) zone[k] = true;
8907	      }
8908	      if (zone.solar || zone.vortex || zone.nebula || zone.stardust) {
8909	        lunar = { zone, counts: moonCounts };
8910	      }
8911	    }
8912	    // downedBoss3 双键（骷髅王击杀链写 downed_35，旧档/导入可能写 downedSkeletron——
8913	    // 此前只传 downedSkeletron 恒 false，地牢守卫池永不切换、绑缚三人组 685 门不开）
8914	    this.vanillaSpawner.setPlayerFlags(!!this.scene?.zoneDungeon,
8915	      !!(w.flags.downedSkeletron || w.flags['downed_35']),
8916	      invaders, activeIds, moonCtx, lunar, this.player.maxHp, this.player.luck);
8917	    // 天气注入（雪原雨刷怪率修正 + 沙尘暴怪池门）
8918	    this.vanillaSpawner.setWeather(
8919	      w.weather.cloudAlpha,
8920	      w.weather.sandstorm.happening,
8921	      !!this.scene?.zoneDesert && p.cy / 16 < w.groundLevel + 30,
8922	    );
8923	    // 狙击镜扩圈（GetSpawnArea :846-862）：手持 1254/1299 或装备 1299 → num3 档
8924	    {
8925	      const heldV = viIdFromKey(ITEM_DEFS[p.inv.heldItem()?.id ?? -1]?.key ?? '') ?? -1;
8926	      const scopeAcc = p.inv.equippedAccessories()
8927	        .some((id) => viIdFromKey(ITEM_DEFS[id]?.key ?? '') === 1299);
8928	      this.vanillaSpawner.scopeNum3 = (heldV === 1254 || heldV === 1299 || scopeAcc)
8929	        ? (heldV === 1254 && scopeAcc ? 1.25 : (heldV === 1254 || heldV === 1299) ? 1.5 : 2.0)
8930	        : 0;
8931	    }
8932	    // TrySpawnAnNPC L23：nearbyActiveNPCs >= maxSpawns 拒绝
8933	    // （原版 nearbyActiveNPCs = 附近 NPC 的 npcSlots 加权和；我们的怪全部由 spawner 生成
8934	    //  在玩家附近，直接全量求和。蠕虫段也是独立 NPC，原版同样计入）
8935	    const nearby = this.entities.enemies.reduce((s, e) => {
8936	      const en = e as Enemy;
8937	      if (en.def.boss) return s;
8938	      return s + (en.vanilla?.npcSlots ?? 1);
8939	    }, 0);
8940	    const sHeightPx = this.camera.viewH / (this.camera.zoom || 1);
8941	    // 联机远端玩家注入（原版 CheckNotSpawningOnScreen L5344-5366 遍历全部玩家扩展屏）
8942	    VanillaSpawner.remotePlayers = this.net?.active
8943	      ? [...this.net.players.values()].filter((q) => q.active).map((q) => ({ x: q.x + 10, y: q.y + 21 }))
8944	      : [];
8945	    // townNPCs（Player.townNPCs = SceneMetrics.TownNPCCount）：玩家 ±(85×60) 格内存活
8946	    // 城镇 NPC 数——spawnFriendly 掷骰的门(NPC.cs:711-832)。岛/荒野无 NPC → 0 → 永不出小动物
8947	    const townNPCs = this.entities.npcs.reduce((s, n) => {
8948	      const tn = n as TownNPC;
8949	      return s + (tn instanceof TownNPC && !tn.dead
8950	        && Math.abs(tn.cx - p.cx) < 85 * TILE && Math.abs(tn.cy - p.cy) < 60 * TILE ? 1 : 0);
8951	    }, 0);
8952	    const { spawnRate, maxSpawns } = this.vanillaSpawner.getSpawnRate(
8953	      p.cy, nearby, this.heldWaterCandle || this.waterCandleNear, sHeightPx, p.cx,
8954	      this.peaceCandleNear, p.buffs.has(BuffType.Sunflower),
8955	      p.buffs.has(BuffType.Calming), p.buffs.has(BuffType.Battle),
8956	      townNPCs, w.clock.isDay,
8957	      !!this.scene?.zoneCorrupt || !!this.scene?.zoneCrimson,
8958	      !!w.clock.bloodMoon);
8959	    if (nearby >= maxSpawns) return;
8960	    // TrySpawnAnNPC L30：Main.rand.Next(spawnRate) != 0 拒绝（每帧 1/spawnRate 概率）
8961	    if (Math.floor(Math.random() * spawnRate) !== 0) return;
8962	    const viewHalfW = Math.ceil(this.camera.viewW / (this.camera.zoom || 1) / 2 / TILE);
8963	    const viewHalfH = Math.ceil(this.camera.viewH / (this.camera.zoom || 1) / 2 / TILE);
8964	    const rng = new RNG((Math.random() * 1e9) | 0);
8965	    const picked = this.vanillaSpawner.spawn(p.cx, p.cy, rng, viewHalfW, viewHalfH);
8966	    if (!picked) {
8967	      // SpawnFrog 687 交付（:5521-5535）：无 Enemy 数据条目 → 转 Critter；
8968	      // AnyNPCs(687) 去重的 Critter 侧补判（activeIds 不含小动物桶）
8969	      const ck = this.vanillaSpawner.pendingCritterKey;
8970	      if (ck) {
8971	        this.vanillaSpawner.pendingCritterKey = null;
8972	        const dupe = this.entities.critters.some((n) => {
8973	          const c = n as Critter;
8974	          return !c.dead && CRITTER_BY_KEY[c.key]?.npc === 687;
8975	        });
8976	        if (!dupe) {
8977	          this.entities.add(new Critter(ck,
8978	            this.vanillaSpawner.currentSpawnX * TILE + 8,
8979	            this.vanillaSpawner.currentSpawnY * TILE), 'critters');
8980	        }
8981	      }
8982	      return;
8983	    }
8984	    // 骷髅商（NPC.cs:4906-4910）：转 TownNPC 进 npcs 桶；场上已有则跳过（CountNPCS(453)==0）
8985	    if (picked.vanillaId === 453) {
8986	      if (this.entities.npcs.some((n) => n instanceof TownNPC && !n.dead && n.npcKey === 'skeleton_merchant')) return;
8987	      const sm = new TownNPC('skeleton_merchant', this.vanillaSpawner.currentSpawnX * TILE + 8, (this.vanillaSpawner.currentSpawnY + 1) * TILE);
8988	      this.entities.add(sm, 'npcs');
8989	      return;
8990	    }
8991	    // 绑缚三人组（NPC.cs:1994-2005）：105 BoundGoblin / 106 BoundWizard /
8992	    // 685 BoundTownSlimeOld——原版为独立被缚 NPC 类型，本仓以 bound TownNPC 近似
8993	    // （同 453 模式转桶；VanillaSpawner.spawnBound 只交付占位体）。已在场（含生成期
8994	    // placeBoundRescueNpcs 放置的 bound 态）则跳过——activeIds 的反查登记通常已在上游
8995	    // 拦下，此处双保险
8996	    {
8997	      const trioKey = picked.vanillaId === 105 ? 'goblin_tinkerer'
8998	        : picked.vanillaId === 106 ? 'wizard'
8999	          : picked.vanillaId === 685 ? 'town_slime_old' : null;

```


---

## 🤖 Assistant · 2026-08-13T05:38:14.367Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me check the flags in World.ts — particularly hardMode, downed_* flags, and where they get set (e.g., on boss kills). Also check if there's a `flags.hardMode` setter (e.g., WoF kill). Let me grep for `hardMode` across the codebase.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:38:14.628Z · glm-x-preview-260804

```
Now let me trace how flags.hardMode and downed_* flags are set, and verify the World.flags structure.
```


---

## 🤖 Assistant · 2026-08-13T05:38:15.043Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"hardMode\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v \"//\" | head -40",
 "description": "Find hardMode references excluding comments"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:15.150Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:61:  hardMode: boolean;
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:125:    case 'Easymode': return !ctx.hardMode;
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:126:    case 'IsHardmode': return ctx.hardMode;
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:127:    case 'NotRemixSeedHardmode': return ctx.hardMode;
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:132:    case 'NotRemixSeedEasymode': return !ctx.hardMode;
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:217:      return ctx.lifeMax > 5 && ctx.value > 0 && !ctx.friendly && ctx.hardMode
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:224:      if (!ctx.hardMode || ctx.lifeMax <= 1 || ctx.friendly || ctx.boss || ctx.value < 1) return false;
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:232:      return ctx.value > 0 && ctx.hardMode && ctx.y / 16 < ctx.worldSurfaceTile + 10
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:238:      if (ctx.value <= 0 || !ctx.hardMode || ctx.type === 23) return false;
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:252:      return !ctx.hardMode && !!ctx.hasPlayerTarget && ctx.lifeMax > 5 && !ctx.friendly && ctx.value > 0
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:255:      return ctx.hardMode && !!ex?.zoneSnow && !!ctx.hasPlayerTarget
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:258:      return ctx.hardMode && !!ex?.zoneJungle && (downed(ctx, 134) || downed(ctx, 125) || downed(ctx, 127))
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:261:      return ctx.hardMode && !!ex?.zoneDungeon && downed(ctx, 262)
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:264:      return ctx.hardMode && !ex?.zoneDungeon
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:429:      const can = ctx.value > 0 && ctx.hardMode && !downed(ctx, 134, 125, 127);
~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts:45:  hardMode: boolean;
~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts:166:  const hardMode = r.boolean();
~/Project/GLM/SandboxWorld/game/src/wld/WldParser.ts:304:    isCrimson, hardMode, gameMode,
~/Project/GLM/SandboxWorld/game/src/world/World.ts:37:   *  hardMode && downedMechBossAny && 1/20）/ 日耀碑牌召唤（Player.cs:43308，白天），
~/Project/GLM/SandboxWorld/game/src/world/World.ts:153:  flags: Record<string, boolean> = { downedEyeOfCthulhu: false, downedSkeletron: false, shadowOrbSmashed: false, hardMode: false };
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HardmodePass.ts:228: *  调用方（Game 击杀流）按原版顺序执行：brickbox → 捕获旧 hardMode → 本函数 →
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HardmodePass.ts:231:  const wasHard = !!world.flags.hardMode;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HardmodePass.ts:232:  (world.flags as Record<string, boolean>).hardMode = true;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1922:    if (this.world.flags.hardMode) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2980:      if (w.flags.hardMode && w.flags['downed_245']
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3064:            if ((ev === 16 || ev === 17 || ev === 18) && w.flags.hardMode
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3225:        if (!stopEvents && w.flags.hardMode && mechAny && Math.random() < 1 / 20) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3240:                ? (w.flags.hardMode ? 1 / 60 : 1 / 30) : 1 / 3;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3246:            if (w.invasionType === INVASION_NONE && w.flags.hardMode && w.altarCount > 0) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3328:        } else if (!this.spawnEyePending && w.flags.hardMode && w.altarCount > 0
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4674:          if (!this.world.flags.hardMode || this.world.clock.isDay
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4927:      if (!this.world.flags.hardMode) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4967:      if (this.world.flags.hardMode && this.world.clock.isDay && !this.world.clock.eclipse) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5587:      if (toolType === 'hammer' && power >= 80 && this.world.flags.hardMode) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7154:    const drop = rollExtractinatorDrop(mode, sheet, mathRand(), this.world.flags.hardMode);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7184:      chest, blockType, mathRand(), this.world.flags.hardMode, slotVanillaId);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7319:  /** 蜥蜴祭坛右键（Player.cs:32303-32335 1:1）：条件门 !AnyNPCs(245) && hardMode
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7332:    if (!w.flags.hardMode) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7845:      hardMode: !!w.flags.hardMode,
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8154:    st: World['store'], x: number, y: number, hardMode: boolean, golemDown: boolean, lavaLine: number,

```


---

## 🤖 Assistant · 2026-08-13T05:38:15.590Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"downed_262\\|downed_398\\|downed_125\\|downed_126\\|downed_127\\|downed_134\\|downed_245\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -40",
 "description": "Find progression flag usages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:15.641Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/drops/NpcDrops.ts:63:  /** world.flags（downedEyeOfCthulhu/downed_134 等） */
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:1711:    this.wiring.planteraDowned = !!w.flags['downed_262'];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:2980:      if (w.flags.hardMode && w.flags['downed_245']
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3065:              && w.flags['downed_134'] && w.flags['downed_125'] && w.flags['downed_127']) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3223:        const mechAny = !!(w.flags['downed_125'] || w.flags['downed_126']
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3224:          || w.flags['downed_127'] || w.flags['downed_134']);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3330:          && !(w.flags['downed_125'] && w.flags['downed_126'] && w.flags['downed_127'])
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3336:            const flag = n === 1 ? 'downed_125' : n === 2 ? 'downed_126' : 'downed_127';
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:6434:      if (oldWall === 87 && !this.world.flags['downed_245']) return;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7251:      if (plantGate && !this.world.flags['downed_262']) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7337:    if (!w.flags['downed_262']) {
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:7527:      downedPlantBoss: !!this.world.flags['downed_262'],
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:8193:    const golemDown = !!this.world.flags['downed_245'];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9130:        return !!(this.world.flags['downed_125'] || this.world.flags['downed_126']
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9131:          || this.world.flags['downed_127'] || this.world.flags['downed_134']);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9137:        return !!this.world.flags.hardMode && !!this.world.flags['downed_262'];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9472:        return Lang.text(w.flags['downed_398'] ? 'GuideSpecialText.Lantern2' : 'GuideSpecialText.Lantern1');
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:9984:          if (this.world.flags['downed_262']) add([4701]);                // 泥巴伙伴（世花后）:3326
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10025:        return !!(f['downed_125'] || f['downed_126'] || f['downed_127'] || f['downed_134']);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10027:      case 'downedMechBoss1': return !!f['downed_125'];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10028:      case 'downedMechBoss2': return !!f['downed_126'];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10029:      case 'downedMechBoss3': return !!f['downed_127'];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10032:      case 'downedPlantBoss': return !!f['downed_262'];
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10068:      downedMoonlord: !!w.flags['downed_398'],
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10092:      downedGolem: !!w.flags['downed_245'],                 // NPC.downedGolemBoss
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10345:      if (!!(f['downed_125'] || f['downed_126'] || f['downed_127'] || f['downed_134'])) list.push(2883, 2869, 2873, 2870);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10346:      if (f['downed_262']) list.push(2878, 2879, 2884, 2885);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:10348:      if (f['downed_398']) list.push(3024);
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:11398:   *  入 Boss 槽（专属 BGM 38 / 血条 / 击败记账 downed_398 → shieldMax 减半为 50） */
~/Project/GLM/SandboxWorld/game/src/world/LunarEvent.ts:78: *  本仓 downedMoonlord = flags['downed_398']（Game 击杀链通用置位 downed_<vanillaId>） */
~/Project/GLM/SandboxWorld/game/src/world/LunarEvent.ts:80:  return w.flags['downed_398'] ? 50 : 100;
~/Project/GLM/SandboxWorld/game/src/world/OldOnesArmy.ts:93:  return !!f.hardMode && !!(f['downed_125'] || f['downed_126'] || f['downed_127'] || f['downed_134']);
~/Project/GLM/SandboxWorld/game/src/world/OldOnesArmy.ts:97:  return !!w.flags.hardMode && !!w.flags['downed_245'];
~/Project/GLM/SandboxWorld/game/src/world/evolution/WorldEvolution.ts:185:    return !!(f['downed_125'] || f['downed_126'] || f['downed_127'] || f['downed_134']);
~/Project/GLM/SandboxWorld/game/src/world/evolution/WorldEvolution.ts:190:    return !!(f['downed_134'] && f['downed_125'] && f['downed_127']);
~/Project/GLM/SandboxWorld/game/src/world/evolution/WorldEvolution.ts:995:    if ((this.host.flags['downed_262'] && Math.random() < 1 / 2) || !this.allowedToSpread) return;
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1337:      if (hardMode && this.world.flags['downed_245'] && !any(399)
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1764:        const hardDungeon = this.hardMode && !!this.world.flags['downed_262']; // downedPlantBoss（世花 262，Game 击杀通用置位链 downed_{id}）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1826:      const downedPlant = !!f['downed_262'];   // downedPlantBoss（世花 262）
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1827:      const flag14 = !!(f['downed_134'] && (f['downed_125'] || f['downed_126']) && f['downed_127']);

```


---

## 🤖 Assistant · 2026-08-13T05:38:18.027Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me check the World.ts flags and where hardMode gets set (HardmodePass.ts line ~228). Also I want to check if there's a "downed_113" flag for WoF. Let me look at HardmodePass and the boss kill flag chain.

Also I should verify: does anything set flags.hardMode when WoF dies? Let me grep for that.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:38:18.519Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"hardMode = true\\|hardMode=true\\|hardMode: true\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\"",
 "description": "Find where hardMode flag is set to true"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:18.582Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HardmodePass.ts:9:// - StartHardmode（cs:31866-31880）：hardMode=true → 变换 → misc[15] 公告 +
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HardmodePass.ts:232:  (world.flags as Record<string, boolean>).hardMode = true;

```


---

## 🤖 Assistant · 2026-08-13T05:38:18.799Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HardmodePass.ts",
 "limit": 40,
 "offset": 215
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:18.819Z

**📎 ToolResult**

```
215	    for (let j = cyTile - r; j <= cyTile + r; j++) {
216	      if (!st.inBounds(i, j)) continue;
217	      const ii = st.idx(i, j);
218	      const onShell = i === cxTile - r || i === cxTile + r || j === cyTile - r || j === cyTile + r;
219	      if (onShell && !st.flags[ii]) {
220	        st.setTile(i, j, brick);
221	      }
222	      st.liquid[ii] = 0; st.liquidType[ii] = 0;          // 盒内岩浆清零
223	    }
224	  }
225	}
226	
227	/** StartHardmode（cs:31866-31880）+ SetEventFlagCleared（NPC.cs:80281-80292）语义。
228	 *  调用方（Game 击杀流）按原版顺序执行：brickbox → 捕获旧 hardMode → 本函数 →
229	 *  (!wasHard 时) 灯笼夜 19 → misc[15] 公告 + 成就 9（由返回值委托，调用方消费）。 */
230	export function startHardmode(world: World): { wasHard: boolean } {
231	  const wasHard = !!world.flags.hardMode;
232	  (world.flags as Record<string, boolean>).hardMode = true;
233	  initializeHardMode(world, new RNG(world.seed));
234	  return { wasHard };
235	}
236	

```


---

## 🤖 Assistant · 2026-08-13T05:38:20.195Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. `startHardmode` is called from Game kill flow (WoF kill). Let me verify that.

Let me grep for startHardmode call.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:38:20.559Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"startHardmode\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | grep -v HardmodePass.ts",
 "description": "Find startHardmode call site"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:20.604Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:204:import { createBrickBoxForWallOfFlesh, startHardmode } from '../world/gen/vanilla/HardmodePass';
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:3049:            const { wasHard } = startHardmode(w);

```


---

## 🤖 Assistant · 2026-08-13T05:38:21.143Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"downed_\\${\\|downed_\\` + \\|downed_${\" ~/Project/GLM/SandboxWorld/game/src --include=\"*.ts\" | head -20",
 "description": "Find generic downed flag setter"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:25.793Z

**📎 ToolResult**

```
(eval):1: unmatched "

```


---

## 🤖 Assistant · 2026-08-13T05:38:28.955Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 45,
 "offset": 3030
}
```


---

## 🤖 Assistant · 2026-08-13T05:38:28.958Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n 'downed_.*=' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | grep -v \"==\" | grep -v \"!==\" | grep -v \">=\" | grep -v \"<=\" | head -20",
 "description": "Find downed flag assignment sites"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:38:28.975Z

**📎 ToolResult**

```
3030	          this.newText(`${bname}逃走了…`, 150, 150, 150);
3031	        } else {
3032	          // 通用记账:按 Boss 名写 downed 标志(原版 NPC.downedBoss 表)
3033	          // NPC.cs:79833 BroadcastChatMessage("Announcement.HasBeenDefeated_Single", ChatColors.BossOrEvent)
3034	          this.newText(Lang.text('Announcement.HasBeenDefeated_Single', bname), 175, 75, 255);
3035	          const downedKey = `downed_${this.boss.vanillaId ?? 0}`;
3036	          // SetEventFlagCleared(NPC.cs:79557) 首次语义:downed 旗标翻转(false→true)
3037	          // 才触发灯笼夜——此前每次击杀都预约(2026-08-13 对齐;肉山 19 在下方链内单独投递)
3038	          const wasDowned = !!w.flags[downedKey];
3039	          w.flags[downedKey] = true;
3040	          // NPC.downedPlantBoss → Wiring 死门接活（Wiring.cs:3216 蜥蜴砖致动 / :1554
3041	          // 神庙传送器捕获：世纪之花前两处 return 拒绝）
3042	          if (this.boss.vanillaId === 262 && this.wiring) this.wiring.planteraDowned = true;
3043	          // 肉山：困难模式世界变换全链（NPC.cs:80281-80292 原序：砖盒 → 捕获旧
3044	          // hardMode → StartHardmode(置位+V 带转化+洞穴墙回填) → 灯笼夜 19(仅首次)
3045	          // → misc[15] 公告 + 成就 9(随本链迁移,2026-08-13 之前击杀即发的旧点已删))
3046	          if (this.boss.vanillaId === 113) {
3047	            const wof = this.boss;
3048	            createBrickBoxForWallOfFlesh(w.store, Math.trunc(wof.cx / 16), Math.trunc(wof.cy / 16), wof.w, w.crimson);
3049	            const { wasHard } = startHardmode(w);
3050	            if (!wasHard) LanternNight.onGameEventCleared(19);
3051	            this.newText(Lang.misc(15), 50, 255, 130);
3052	            this.achievements.notifyProgressionEvent(9);
3053	          }
3054	          // 首胜灯笼夜预约（NPC.cs NPCLoot 各 case SetEventFlagCleared 实参 →
3055	          // OnGameEventClearedForTheFirstTime default/10/16-18 翻转；4/21/22 排除）。
3056	          // id 表：11 史王 8 蜂后 13 EoC 14 世吞|克脑 15 骷髅王 19 肉山 12 世纪之花
3057	          // 6 石头人 7 猪鲨 9 邪教徒 10 月总 24 史后 23 光女 25 鹿角怪 16/17/18 三王
3058	          if (this.boss.vanillaId != null) {
3059	            const ev = BOSS_GAME_EVENT_BY_NPC[this.boss.vanillaId];
3060	            if (ev !== undefined && !wasDowned) LanternNight.onGameEventCleared(ev);
3061	            // 三王全灭 → 保底世花球茎（NPC.cs:79578-79585 case 16/17/18 →
3062	            // WorldGen.GeneratePlanteraBulbOnAllMechsDefeated：netMode!=1 &&
3063	            // hardMode && 三旗齐 → 丛林侧搜索框生成恰好一个灯泡）
3064	            if ((ev === 16 || ev === 17 || ev === 18) && w.flags.hardMode
3065	              && w.flags['downed_134'] && w.flags['downed_125'] && w.flags['downed_127']) {
3066	              this.evolution.planteraBulbBurst();
3067	            }
3068	          }
3069	          // 星璇塔触发（NPC.cs:80194-80197：教徒 439 死 → TriggerLunarApocalypse——
3070	          // downed_439 通用置位处直接追加，四塔就位 + 满盾 + misc[43] 公告）
3071	          if (this.boss.vanillaId === 439) this.triggerLunarApocalypse();
3072	          // Badger's Hat 同日双杀（DoDeathEvents_DropBossPotionsAndHearts 尾段，
3073	          // NPC.cs:79800-79814）：type==4 置 EoCKilledToday / type==113 置 WoFKilledToday
3074	          // （:79805-79811）；双旗齐 → ResetBadgerHatTime + 掉 5004 Badger's Hat

```


---

## 👤 User(sidechain) · 2026-08-13T05:38:28.997Z

**📎 ToolResult**

```
7847:      downedSlimeKing: !!(w.flags.downedSlimeKing ?? w.flags.downed_50),  // 击败键=downed_50(50=史莱姆王)

```


---

## 🤖 Assistant · 2026-08-13T05:39:55.903Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Good. Now I have all info about flags. The generic chain: `downed_${vanillaId}` is set on boss kills (line 3035-3039). So:
- downed_113 = WoF (also triggers hardMode via startHardmode at 3046-3053)
- downed_125 = Retinazer, downed_126 = Spazmatism, downed_127 = Skeletron Prime, downed_134 = Destroyer
- downed_262 = Plantera
- downed_245 = Golem
- downed_398 = Moon Lord

Wait — downed_398? Moon Lord's npc id... In vanilla, Moon Lord core is 398. Yes.

Now, one important check: is there a `downed_262` gate in scaling (downedPlantBoss)? Yes in ScaleStats.ts line 288 and 539.

Now let me double-check the question about "hardmode-only enemies we spawn and what gate protects them". I need to inventory the branches and flag ones that LACK hardMode gate.

Let me go through VanillaSpawner.ts branches carefully:

Branch tree (SpawnAnNPC, starting line 1258):
1. Line 1285-1327: Lunar pillar zone (this.lunar) — 4 pillars, NPC ids 420-429, 402, 405, 407, 409, 411, 412, 415-419, 518. Gate: `this.lunar != null` — which is set by Game when lunarEvent.active and near a tower. No hardMode gate needed (lunar event inherently post-Golem/Cultist). Note it's checked first — even before skyMob.

2. Line 1331-1349: skyMob branch — 388 (martian drone during invasion 4), 399 (martian probe: hardMode && downed_245), 87 (wyvern: hardMode), 686 (bound purple slime), 48 (harpy fallback). Gates noted.

3. Line 1351-1416: invaders branch — invasion 1 (goblin), 2 (frost legion), 3 (pirate), 4 (martian madness). Note: 471 goblin summoner requires hardMode. Frost legion 145/143/144 have NO hardMode gate — but in vanilla frost legion only occurs in hardmode? Actually Frost Legion can be summoned in pre-hardmode via Snow Globe. Hmm — Snow Globe is dropped by presents. Actually in vanilla Frost Legion can be summoned at any time with a Snow Globe. OK. Pirate invasion requires hardmode to occur naturally but can be summoned pre-hardmode with Pirate Map. So no gates = vanilla parity.

4. Line 1419-1424: Spider nest — 163 black widow (hardMode, 9/10), 164 wall creeper. Gates OK.

5. Line 1429-1466: Underground desert — 589 golfer, 510 tombcrawler (hardMode), 513 (no hardmode gate but it's pre-hardmode enemy - Tomb Crawler exists in pre-hardmode), 524-533 ghouls (hardMode), 69/580/581/537/508/509 basic pool.

6. Line 1470-1474: hardMode water — 157 arapaima (jungle), 242/241 crimson water. Both hardMode gated. Good.

7. Line 1485-1543: Ocean — 376 angler, 602 seagull, 65 shark, 692 orca (hardMode), 625 turtle/615 dolphin/626/627 seahorse/688 pufferfish, 220 sea snail, 221 squid, 67 crab, 64 pink jellyfish. Gates: 692 has hardMode. Others pre-hardmode valid.

8. Line 1552-1556: Statue mimic 690 — gate: downedBoss3 (skeletron) && ZoneGraveyard && !noWorms && luck && !any(690). Note: no hardMode gate! In vanilla, Wraith/statue mimic... Actually the statue mimic (Mimic disguised as statue) requires post-Skeletron graveyard in vanilla — no hardmode requirement. Vanilla NPC.cs:1478 requires downedBoss3 && ZoneGraveyard. So parity OK. Actually wait — is 690 gated by hardmode in vanilla? Let me think. In vanilla 1.4.4, the Statue Mimic spawns in graveyards after Skeletron is defeated. I believe it does not require hardmode. OK.

9. Line 1560-1597: Water pool A/B — 617 jungle turtle, 613/612 water strider, 102 angler fish (hardMode), 58 piranha, 103 green jellyfish (hardMode), 63 blue jellyfish. Gates OK.

10. Line 1604-1638: Water third branch — 57 corrupt goldfish, 465, 616 water strider, 613/612, 608 grebe, 362/364 duck, 607, 592, 55. No hardmode enemies.

11. Line 1650-1664: Bound trio — 105 (downedGoblins), 106 (hardMode), 685 (downedBoss3). Gates OK.

12. Line 1668-1671: Graveyard friendly — 610 maggot / 606 rat.

13. Line 1680-1685: rain deep gem squirrel/bunny.

14. Line 1688-1731: surface critters — 669 stinkbug, 356/444 butterfly, 148/149, 604/605 ladybug, 357 worm, 377 grasshopper, 46 bunny, 299 squirrel, 300 mouse, 74 bird.

15. Line 1737-1744: cave gem squirrel/bunny.

16. Line 1747: friendly cycle guard.

17. Line 1753-1808: Dungeon — 68 dungeon guardian (!downedBoss3), 123 mechanic (downedBoss3), hardDungeon = hardMode && downed_262 → 287 tactical skeleton, 293/291/292, 290 skeleton sniper, 289 skeleton commando, 281-286 necromancer, 269-280 ragged caster; then pre-hardmode pool: 71 dungeon slime, 70 spike ball, 72 blazing wheel, 34 cursed skull, 32 dark caster, 294/295/296, -14/-13/31 bone skeletons. Gates: hardDungeon requires hardMode && downed_262 — vanilla parity (post-Plantera dungeon enemies).

18. Line 1811: Meteor — 23 meteor head. Note: In vanilla, meteor heads spawn in pre-hardmode AND hardmode; in hardmode with... Actually in 1.4, meteor heads stop spawning in hardmode? No wait. In vanilla 1.3+, meteor heads don't spawn in hardmode? Hmm. Actually the change: In 1.4.0.1, Meteor Heads no longer spawn in hardmode worlds? Let me think... The actual vanilla code at NPC.cs:2704: `else if (spawn.wofFlagsAndPillars...)`. Hmm, I recall that in vanilla the meteor head spawn branch is `else if (Main.player[spawn.playerIndex].ZoneMeteor)`. There's no hardmode check in that branch in 1.4.4 source. Actually, I do recall a change where Meteor Heads only spawn pre-hardmode... Let me verify: Terraria 1.4 changelog: "Meteor Heads no longer spawn in Hardmode"? Hmm, I'm not sure. Actually I believe there IS such a change. In 1.4, the code is:

```
else if (spawn.player.ZoneMeteor)  // hmm
```

Hmm, actually I remember from decompiled sources that in SpawnAnNPC there's:
```
if (spawn.player.ZoneMeteor && !Main.hardMode) // ? 
```
I'm not certain. This is a parity question I should flag as "needs verification" rather than assert. Actually let me check the docs/spawn-parity-gaps.md file which may document this.

19. Line 1814-1820: Moon event — frost/pumpkin moon.

20. Line 1824-1843: Eclipse — 477 Mothron (downedPlant), 251 Eyezor, 466 Psycho (downedPlant), 463 Nailhead (downedPlant), 467 Deadly Sphere (downedPlant), 159 Vampire, 253 Reaper (all 3 mechs), 469 The Possessed, 468 Dr Man Fly (downedPlant), 460 Butcher (downedPlant), 162 Frankenstein, 461 Creature from the Deep, 462 Fritz, 166 Swamp Thing. Gates present. Note eclipse itself implies hardmode in vanilla (eclipse can only happen in hardmode). But our clock.eclipse — does it check hardmode? Let me check. If eclipse can trigger pre-hardmode, then 159 vampire etc would spawn pre-hardmode. Let me check clock.eclipse logic.

21. Line 1845-1876: Mushroom biome — 256 fungus fish (hardMode), 360 glowing snail, 260/259 fungibulb, 257/258, 254/255, 374 truffle worm (hardMode). Gates OK.

22. Line 1883-1886: Devourer — 98 World Feeder head (hardMode, 3/4), 7 Eater of Worlds head. Gates OK.

23. Line 1892-1904: rare cave — 473/474/475/476 biome elementals (hardMode), 629 ice tortoise? (ZoneSnow) — hmm 629 is... Actually "629" — let me think. The comment says "兜底 85（hellstone turtle）". 629 might be Ice Tortoise... Actually Ice Tortoise is 154. Hmm 629... not sure. Anyway: 85 wolf/jungle? Hmm 85 = Wolf? No — 85 is "Wolf"? Let me check: NPCID 85 = Wolf. Hmm the comment says "hellstone turtle" which seems wrong. Actually in vanilla at L3644 the fallback is `spawnNPC...85`? Hmm. Let me not over-assert names. I'll report ids as-is with our comments.

Also line 1901: 85 via wall===2 && hardMode. Line 1903-1904: werewolf 82 (hardMode && surface && night).

24. Line 1906: bone doctor? 52 — jungle grass && night && 1/500.
Line 1908: 219 jungle turtle? no — "龟甲虫" 219. Pre-hardmode.

25. Line 1913-1921: cave critters 448/357, 447/300, 359.

26. Line 1926-1931: jungle surface critters — macaw 671-675, frog.

27. Line 1934-1943: hive block — moss hornet -21..-18, 176 dragon hornet (hardMode), spawnHornet.

28. Line 1947-1961: hard jungle grass pool (hardMode) — 152 giant flying fox, 177 giant tortoise, 205 moth, 236 jungle creeper, moss hornets, 175 angry trapper, 153 giant tortoise. Wait: comment says 177 蹦蹦兽 (Derpling? no). 177 = Derpling? Hmm. Actually 177 = "Derpling". Let me be careful with names. I'll use our file's Chinese comments as-is.

29. Line 1964-1966: temple — 226 flying snake / 198 lizard. Gates: zoneLihzardTemple. No hardMode gate. In vanilla, temple requires Plantera to open doors but enemies spawn regardless of progression once inside. Vanilla code: `if ((tile == 226 || tile == 232) && player.ZoneLihzhardTemple)` — no hardmode gate. Parity OK.

30. Line 1968: hive wall — hornets.

31. Line 1970-1981: jungle grass (non-hard) — 204 spiked jungle slime, 43 man eater, hornets, 51 jungle bat, 56 hornet.

32. Line 1987-2021: sandstorm pool — 546/61/69 pre-hardmode (with !downedBoss1 && !hardMode), 541 sand elemental (hardMode), 510 dune splicer (hardMode), 542-545 sand sharks (hardMode), 78/79/630/80 mummies (hardMode), 546/580/581 fallback.

33. Line 2024-2027: surface desert mummies — 78, 79, 630, 80 all hardMode gated.

34. Line 2031-2054: Hallow tiles — 661 mothron? no, "月神蝶" 661 = Mothron? Hmm 661... Actually 661 is not Mothron (477). 661 = "Empress Butterfly"? Hmm. The comment says 月神蝶 661 — likely "Hallowed" ... Actually I think 661 = "Mothron"? No. Let me think: 660 = Torch God? 659? Hmm. Actually 661 could be "Empress of Light's"? Let me not worry: it's gated by downedPlant && night && surfaceSpawn. 244 rainbow slime (raining, unique), 122 gastropod (night), 86 unicorn, 75 pixie. All within hardMode && underGround && hallowFloor. Then line 2052: 84 hallowed devourer (hardMode).

35. Line 2059-2086: Crimson — 179 crimson axe (hard+deep), 182 floater (hard+deep), 268 (hard+deep), -24/-25/183 crimslime (hard), 174 face monster? no — 174 = Crimslime? Hmm. The comment: ⑤hard && (1/2 || 深于地表) → 174 跳跳兽 (Face Monster is 173? no). Let me check: 173 = Crimera, 174 = Crimson Axe? no... In vanilla: 173 Crimera, 174 Face Monster, 179 Crimson Axe, 180 Pigron (crimson), 181 Blood Feeder, 182 Crimslime, 183 Floaty Gross, 268 Ichor Sticker? Hmm no.

Actually the correct mapping: 173 Crimera, 174 Face Monster, 175 Crimslime? Hmm I'm getting confused. Let me just use ids and note the gates. The important thing for the deliverable is gates, not names. I'll include names where our comments are confident, and use "id N" otherwise. Actually our comments give Chinese names: 179 猩红斧 (crimson axe ✓), 182 浮空恶臭 (Floaty Gross ✓), 268 弱金史莱姆? (hmm - 268 is Ichor Sticker? The comment says 弱金史莱姆 which sounds like Ichor Sticker, whatever), 183 Crimslime? comment says 183 Crimslime ✓, 174 跳跳兽 (Face Monster? no — Crimslime? Hmm). Actually 174 = "Crimson Axe"? No that's 179. 174 = Face Monster ✓ (Face Monster is NPCID 174? Hmm, I believe Face Monster = 174 and Crimslime = 183, Floaty Gross = 182, Crimera = 173, Ichor Sticker = 268, Blood Feeder = 181, Pigron = 180/170/171. Yes! 181 Blood Feeder = "脸怪"? hmm the comment at line 2082 says 181 脸怪 which matches "Face Monster"? Hmm.

Hmm, let me get this right:
- 173 Crimera
- 174 Face Monster
- 180 Pigron (Crimson)
- 181 Blood Feeder
- 182 Floaty Gross
- 183 Crimslime
- 268 Ichor Sticker
- 179 Crimson Axe

Wait but the comment says "⑤hard && (1/2 || 深于地表) → 174 跳跳兽" and "⑦1/2 → 181 脸怪". Hmm "跳跳兽" for 174 — Face Monster hops. "脸怪" = Face Monster literally (脸=face). So they may have them swapped. I'll just report IDs with gates and note names per file comments.

Actually the important deliverable: which hardmode-only enemies lack gates. Let me focus.

36. Line 2091-2106: Corruption — 83 cursed hammer (hard+rock), 101 clinger (hard+rock), 121/81 slime? (hard) — comment "史莱姆法师/腐化史莱姆" hmm 81 = Corrupt Slime, 121 =... hmm. Actually 121 = "Shadow Slime"? No... In vanilla 121 = Corrupt Slime? Hmm: 81 Corrupt Slime, 121 Corrupt Slime? Let me not worry. Then -11/-12 devourer variants, 6 Eater of Souls.

37. Line 2110-2274: surfaceSpawn branch:
- 2119: graveyard maggot/mouse
- 2124: ice golem 243 (ZoneSnow && hard && rain)
- 2126: nimbus 250 (hard && rain)
- 2131: martian probe 399 (flag17 && hard && downed_245)
- 2138-2183: day pool — slime king 50, antlion 69, vulture 61, goblin scout 73, 224 flying enemy (rain), 225 umbrella slime, 594 windy balloon, 628 dandelion, basic slime.
- 2191-2273: night pool — firefly 358/355, raven 301 (graveyard), ghost 316 (graveyard), hoppin jack 304 (graveyard && hard), wandering eye 133 (hard), demon eye, zombie family 190-194, clown 109 (hard && bloodmoon), groom 53/bride 536, werewolf 104 (hard && new moon), werewolf 140? comment says "hard 1/3 → Werewolf 140" — 140 = Possessed Armor? Hmm. Wait line 2225: "L4533：新月（moonPhase==0）hard 2/3 → Werewolf 104" and line 2227: "L4538：hard 1/3 → Werewolf 140". Hmm, 104 = Werewolf ✓. 140 = ? In vanilla L4538 is `if (Main.hardMode && rand.Next(3)==0) → 140` which is... "Possessed Armor"? Hmm. Actually 140 might be... let me think about 1.4.4 SpawnAnNPC L4538: 

```
if (!Main.dayTime && Main.rand.Next(3) == 0 && Main.hardMode) → 104 (Werewolf)
```
Hmm. Actually I recall:
```
if (!Main.dayTime && Main.moonPhase == 0 && Main.rand.Next(3) != 0 && Main.hardMode) → 104 Werewolf
if (!Main.dayTime && Main.rand.Next(3) == 0 && Main.hardMode) → 140 Wandering Eye Fish? 
```
Hmm 140... Actually I don't need to resolve names.

- blood zombie 489/drippler 490 (bloodmoon)
- ice tile: 169 ice elemental (hard, !graveyard), 155 wolf (hard, !graveyard), 431 armed zombie (expert), 161 frozen zombie
- raincoat zombie 223
- moss zombie 691 (graveyard), maggot zombie 632 (graveyard)
- torch zombie 590/591
- armed zombies 430-436 (expert)
- final zombie table.

Note: werewolf 104 at line 2225 requires moonPhase===0 && hardMode && !N(3) → so 2/3 chance on new moon nights. ✓ gate present. Note: the user prompt asked about "werewolf 145" — 145 is actually Mister Stabby (snowman gang) in frost legion, not werewolf. The prompt guesses ids; I should clarify actual ids.

38. Line 2276-2288: underground — 10 giant worm/95 digger (hard), 140 (hard 1/3), 141 toxic sludge (hard 1/2), 147 ice slime, basic slime.

39. Line 2292-2319: underworld — mechAny = downed_125||126||127||134; 534 tortured soul (hard), lava critters 653/654/655, bone serpent 39, fire imp 24, voodoo demon 66, red devil 156 (hard && mechAny), demon 62, lava slime 59, lava bat 151 (hard && mechAny), hellbat 60.

40. Line 2323: rock golem 631 — checkToSpawnRockGolem requires hardMode.

41. Line 2327-2436: cave general pool — 218/217, chaos elemental 120 (hard), pigron 170/171/180 (hard), ice tortoise 154 (hard), digger 95 (hard)/snow flinx/giant worm, mother slime, skeleton merchant 453, nymph 195, rune wizard 172 (hard && deep), bound goblin 45, medusa 480 (hard), hoplite 481, granite 483/482, armored skeleton 77 / heavy skeleton -15 (hard), skeleton sniper? etc. 206/110, ghost 316 (graveyard), undead miner 44, ice cave pool, cavern salamanders, spore skeleton 635, skeletons, illuminant slime 138 (hard && hallow), jungle bat 51, spore bat 634, illuminant bat 137 (hard && hallow), ice bat 150/giant bat 93 (hard), ice elemental 169/ice bat (hard), cave bat 49.

Now: things the user explicitly asked to check for missing hardMode gates:
- wraiths 77/78: Actually in our code, 77 = Armored Skeleton (line 2395, gated by hardMode at 2391). 78 = Mummy (lines 2013, 2024, gated hardMode). So no wraith by those ids. Wraith in vanilla is 77! Wait — vanilla NPCID: 77 = Wraith? Let me check. Hmm. Vanilla: 
  - 77 = Armored Skeleton? or Wraith?
  
  Actually I'm fairly confident: 77 = Wraith is wrong. Let me recall the list around there:
  - 76 = Skeleton? 
  - 77 = Armored Skeleton
  - 78 = Mummy
  - 79 = Dark Mummy
  - 80 = Light Mummy
  - 81 = Corrupt Slime
  - 82 = Werewolf
  - 83 = Cursed Hammer
  - 84 = Enchanted Nightcrawler? no...
  - 84 = Clinger? Hmm no, 84 = "Clinger"? Actually Clinger is 101? no, 101 = Clinger? Let me recall: 101 = Clinger ✓ (our code line 2099 spawns 101 with ai anchor - Clinger is a wall plant ✓).
  - 84 = Enchanted Nightcrawler? No that's 620-ish. 84 = ... "Bound Wizard"? no that's 106.
  
  Hmm 84 = "Clinger"? Actually I believe 84 = Clinger and 101 = ... hmm. Our line 2052 spawns 84 as "神圣噬魂怪" (Hallowed devourer = Hallow Eater?). Hmm — actually in vanilla, the hallow worm is "Devourer variant"? The spawn at L3962 in vanilla is:
  ```
  if (!spawn.noWorms && Main.rand.Next(50)==0 && !water && deeperThanRock && hallowTiles) → 84 (Clinger? or "Enchanted Nightcrawler"?)
  ```
  Hmm. Actually I'm now fairly sure 84 = Clinger. And 101 = ... hmm but our code passes ai0/ai1 anchor for 101 (plant aiStyle 13)? Let me check: line 2099 spawns 101 with anchor → aiStyle 13 = plant. Clinger is a plant (grows from walls). Hmm so 101 = Clinger?
  
  Hmm, hold on. Let me check the actual vanilla NPCID around:
  - 77 Armored Skeleton
  - 78 Mummy  
  - 79 Dark Mummy
  - 80 Light Mummy
  - 81 Corrupt Slime
  - 82 Werewolf
  - 83 Cursed Hammer
  - 84 Clinger? 
  
  Hmm, but I also recall 84 = "Clinger"... Let me just verify via the JSON data in the repo! public/sprites/vanilla-npcs.json should have names. That's authoritative for our repo. Let me grep names for the ids of interest: 77, 78, 84, 98, 99, 100, 104, 109, 122, 133, 140, 145, 151, 156, 169, 120, 137, 138, 244, 256, 510, 541, 692, 629, 534, 473-476, 524-533.

Let me check the data file location.

Also "闪电虫" (lightning bug / firefly?) — that's 358? Our code spawns 358 for hallow grass firefly, 355 otherwise. 358 = "Lightning Bug" (hallow firefly variant) — gated? Line 2192-2196: `N(Math.max(1, this.world.fireFlyChance)) && this.spawnTileY <= groundLevel` → returns 358 if t === T.HALLOW_GRASS else 355. NO hardMode gate! But wait — hallow grass only exists in hardmode worlds (created by WoF), so effectively gated by world state. Hmm, but the file's comment notes it. Let me check: line 2191-2196:

```
if (!this.ZoneGraveyard && !tooWindy && !raining
  && (t === T.GRASS || t === T.MOWED_GRASS || t === T.HALLOW_GRASS || t === T.HALLOW_MOWED_GRASS)
  && N(Math.max(1, this.world.fireFlyChance)) && this.spawnTileY <= this.world.groundLevel) {
  return D(t === T.HALLOW_GRASS ? 358 : 355);
}
```

So 358 Lightning Bug spawns on hallow grass at night — no explicit hardMode gate, but hallow grass tiles only exist post-WoF (unless imported world). In vanilla L4410: `if (tile==109 || tile==492) → 358 (lightning bug) else 355`. Vanilla has no hardMode gate either because hallow grass implies hardmode. So parity OK but "implicit gate" worth flagging.

Now the user asks about "clowns" — 109, gated hardMode && bloodMoon at line 2218. ✓

"corruptors 98/99/100" — 98 World Feeder (hardMode, line 1884). 99/100 = Corruptor body/head segments — in vanilla, World Feeder spawns as a multi-segment worm (98 head, 99/100 body/tail). Our code spawns only D(98) — a single head NPC. Do we handle 99/100? Let me grep. Probably the worm segmentation is handled elsewhere in Enemy.ts (aiStyle 5 worm families). fighterFamilies.ts? Let me check for 99/100.

Also "hallowed enemies 104+" — hmm 104 = Werewolf (not hallowed). The user's id guesses are off; I'll map actual ids.

"wraith" — vanilla Wraith is NPCID 77? Hmm no! Let me actually check. I'm quite sure Wraith = 77? Ugh.

Let me check the JSON.

Let me also confirm whether eclipse requires hardmode in our clock (Game.ts line 4967 area showed `w.flags.hardMode && isDay && !eclipse` — that's a different check). Let me grep for eclipse trigger.

Also bloodMoon — pre-hardmode possible (vanilla allows blood moon pre-hardmode) ✓.

Let me look at the vanilla-npcs.json to get names for the ids.
````

</details>


---

## 🤖 Assistant · 2026-08-13T05:39:55.914Z · glm-x-preview-260804

```
Let me verify NPC names from the data file and check worm segment handling for multi-part enemies.
```


---

## 🤖 Assistant · 2026-08-13T05:39:55.969Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/public/sprites/ | grep -i npc | head; find ~/Project/GLM/SandboxWorld/game -name \"vanilla-npcs.json\" -not -path \"*/node_modules/*\" | head",
 "description": "Locate vanilla npc data json"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:39:56.015Z

**📎 ToolResult**

```
vanilla-npcgore.json
vanilla-npcs.json
~/Project/GLM/SandboxWorld/game/dist/sprites/vanilla-npcs.json
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json

```


---

## 🤖 Assistant · 2026-08-13T05:39:56.337Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\\b99\\b\\|\\b100\\b\\|WorldFeeder\\|world_feeder\" ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts | head",
 "description": "Check for corruptor body segments in spawner"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:39:56.366Z

**📎 ToolResult**

```
120:const WALL_HOUSE = new Set([1, 4, 5, 6, 10, 11, 12, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 60, 66, 67, 68, 72, 73, 74, 75, 76, 77, 78, 82, 84, 85, 88, 89, 90, 91, 92, 93, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 167, 168, 169, 172, 173, 174, 175, 176, 177, 179, 181, 182, 183, 184, 186, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366]);
299:   *  基础 12；playerHasStartingHealth（statLifeMax≤100，L327）→ 5 − 活跃玩家数/2（下限 2） */
524:    // 阈值 Snow 1500 / Corrupt·Crimson 300 / Hallow 125 / Jungle 140 / Mushroom 100。
532:    this.ZoneGlowshroom = this.zoneCounts.mushroom >= 100;
1277:    //  playerHasStartingHealth（L327：statLifeMax ≤ 100）→ 5 − numberOfActivePlayers/2
1280:    this.torchZombieChance = this.playerLifeMax > 0 && this.playerLifeMax <= 100
1438:      // L1605：沙虫 510（hard，1/(50·num11)，非蠕虫禁置，落脚深于 worldSurface+100）
1440:        && this.spawnTileY > this.world.groundLevel + 100) return D(510);
1443:        && this.spawnTileY > this.world.groundLevel + 100 && this.countNpc(513) === 0) return D(513);
1754:        // 墙变体（L2540-2552）：94/96/98→1、95/97/99→2；RollLuck(7) 重掷（0.9 尺度下 1/7≈1/7）

```


---

## 🤖 Assistant · 2026-08-13T05:39:59.232Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me get NPC names for the key ids from the JSON. Let me use node to parse it (read-only, no file writes). Actually I can use `node -e` with a script — that doesn't write files. But the instruction says Bash only for read-only operations; running node to read JSON is read-only. Let me do it via grep/python. Actually `python3 -c` reading JSON is read-only. Let me do that.

Actually, simpler: grep the JSON for the ids. The JSON structure — let me check its format first.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:39:59.464Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -c 600 ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json",
 "description": "Inspect npc json structure"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:39:59.500Z

**📎 ToolResult**

```
{"1":{"id":1,"name":"Blue Slime","frames":2,"lifeMax":25,"damage":7,"defense":2,"aiStyle":1,"width":24,"height":18,"HitSound":"NPCHit1","DeathSound":"NPCDeath1","alpha":175,"color":[0,80,255,100]},"2":{"id":2,"name":"Demon Eye","frames":2,"lifeMax":60,"damage":18,"defense":2,"knockBackResist":0.8,"aiStyle":2,"width":30,"height":32,"HitSound":"NPCHit1","DeathSound":"NPCDeath1"},"3":{"id":3,"name":"Zombie","frames":3,"lifeMax":45,"damage":14,"defense":6,"knockBackResist":0.5,"aiStyle":3,"width":18,"height":40,"HitSound":"NPCHit1","DeathSound":"NPCDeath2"},"4":{"id":4,"name":"Eye of Cthulhu","fra

```


---

## 🤖 Assistant · 2026-08-13T05:40:04.185Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'))\nids=[77,78,79,80,81,82,83,84,85,98,99,100,101,104,109,110,120,121,122,133,137,138,140,141,145,147,151,153,154,155,156,157,159,163,164,169,170,171,180,176,177,243,244,250,251,253,268,287,316,358,510,513,524,525,526,527,528,529,530,531,532,533,534,541,542,543,544,545,629,630,631,632,635,634,690,691,692,473,474,475,476,477,460,463,466,467,468,469,489,490,546,580,581,661,669]\nfor i in ids:\n    e=d.get(str(i))\n    print(i, (e or {}).get('name'), '| lifeMax=',(e or {}).get('lifeMax'),'dmg=',(e or {}).get('damage'),'def=',(e or {}).get('defense'))\n\"",
 "description": "Extract names and stats for key npc ids"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:09.404Z

**📎 ToolResult**

```
77 Armored Skeleton | lifeMax= 260 dmg= 40 def= 28
78 Mummy | lifeMax= 130 dmg= 50 def= 16
79 Dark Mummy | lifeMax= 180 dmg= 60 def= 18
80 Light Mummy | lifeMax= 200 dmg= 55 def= 18
81 Corrupt Slime | lifeMax= 170 dmg= 55 def= 20
82 Wraith | lifeMax= 160 dmg= 65 def= 16
83 Cursed Hammer | lifeMax= 200 dmg= 80 def= 18
84 Enchanted Sword | lifeMax= 200 dmg= 80 def= 18
85 Mimic | lifeMax= 500 dmg= 80 def= 30
98 World Feeder | lifeMax= 500 dmg= 70 def= 36
99 NPC_99 | lifeMax= 500 dmg= 55 def= 40
100 NPC_100 | lifeMax= 500 dmg= 40 def= 44
101 Clinger | lifeMax= 320 dmg= 70 def= 30
104 Werewolf | lifeMax= 350 dmg= 70 def= 38
109 Clown | lifeMax= 800 dmg= 60 def= 25
110 Skeleton Archer | lifeMax= 210 dmg= 45 def= 14
120 Chaos Elemental | lifeMax= 370 dmg= 40 def= 30
121 Slimer | lifeMax= 60 dmg= 45 def= 20
122 Gastropod | lifeMax= 220 dmg= 60 def= 22
133 Wandering Eye | lifeMax= 300 dmg= 40 def= 20
137 Illuminant Bat | lifeMax= 200 dmg= 75 def= 30
138 Illuminant Slime | lifeMax= 180 dmg= 70 def= 30
140 Possessed Armor | lifeMax= 260 dmg= 55 def= 28
141 Toxic Sludge | lifeMax= 150 dmg= 50 def= 18
145 Snow Balla | lifeMax= 220 dmg= 55 def= 22
147 Ice Slime | lifeMax= 30 dmg= 8 def= 4
151 Lava Bat | lifeMax= 160 dmg= 50 def= 16
153 Giant Tortoise | lifeMax= 470 dmg= 80 def= 30
154 Ice Tortoise | lifeMax= 400 dmg= 55 def= 28
155 Wolf | lifeMax= 300 dmg= 65 def= 30
156 Red Devil | lifeMax= 600 dmg= 50 def= 40
157 Arapaima | lifeMax= 200 dmg= 75 def= 30
159 Vampire | lifeMax= 750 dmg= 80 def= 24
163 NPC_163 | lifeMax= 350 dmg= 90 def= 40
164 NPC_164 | lifeMax= 80 dmg= 30 def= 10
169 Ice Elemental | lifeMax= 200 dmg= 55 def= 20
170 Pigron | lifeMax= 210 dmg= 70 def= 16
171 Pigron | lifeMax= 210 dmg= 70 def= 16
180 Pigron | lifeMax= 210 dmg= 70 def= 16
176 Moss Hornet | lifeMax= 220 dmg= 70 def= 22
177 Derpling | lifeMax= 300 dmg= 80 def= 26
243 Ice Golem | lifeMax= 4000 dmg= 60 def= 32
244 Rainbow Slime | lifeMax= 400 dmg= 85 def= 26
250 Angry Nimbus | lifeMax= 300 dmg= 50 def= 24
251 Eyezor | lifeMax= 1000 dmg= 50 def= 30
253 Reaper | lifeMax= 700 dmg= 80 def= 22
268 Ichor Sticker | lifeMax= 340 dmg= 55 def= 20
287 Bone Lee | lifeMax= 1000 dmg= 90 def= 42
316 Ghost | lifeMax= 70 dmg= 18 def= 8
358 Lightning Bug | lifeMax= 5 dmg= 0 def= 0
510 Dune Splicer | lifeMax= 500 dmg= 58 def= 18
513 Tomb Crawler | lifeMax= 60 dmg= 18 def= 0
524 Ghoul | lifeMax= 180 dmg= 50 def= 26
525 Vile Ghoul | lifeMax= 180 dmg= 50 def= 26
526 Tainted Ghoul | lifeMax= 180 dmg= 50 def= 26
527 Dreamer Ghoul | lifeMax= 180 dmg= 50 def= 26
528 Lamia | lifeMax= 350 dmg= 52 def= 28
529 Lamia | lifeMax= 350 dmg= 52 def= 28
530 NPC_530 | lifeMax= 320 dmg= 66 def= 24
531 Sand Poacher | lifeMax= 320 dmg= 66 def= 24
532 Basilisk | lifeMax= 270 dmg= 65 def= 34
533 Desert Spirit | lifeMax= 220 dmg= 40 def= 20
534 Tortured Soul | lifeMax= 400 dmg= 14 def= 20
541 Sand Elemental | lifeMax= 5000 dmg= 40 def= 30
542 Sand Shark | lifeMax= 360 dmg= 50 def= 20
543 Bone Biter | lifeMax= 380 dmg= 60 def= 24
544 Flesh Reaver | lifeMax= 400 dmg= 64 def= 22
545 Crystal Thresher | lifeMax= 450 dmg= 54 def= 26
629 Ice Mimic | lifeMax= 500 dmg= 80 def= 30
630 None | lifeMax= None dmg= None def= None
631 Rock Golem | lifeMax= 1000 dmg= 85 def= 35
632 Maggot Zombie | lifeMax= 45 dmg= 14 def= 6
635 Spore Skeleton | lifeMax= 60 dmg= 20 def= 8
634 Spore Bat | lifeMax= 16 dmg= 13 def= 2
690 Statue | lifeMax= 400 dmg= 40 def= 10
691 Moss Zombie | lifeMax= 60 dmg= 18 def= 10
692 Orca | lifeMax= 400 dmg= 50 def= 20
473 Corrupt Mimic | lifeMax= 3500 dmg= 90 def= 34
474 Crimson Mimic | lifeMax= 3500 dmg= 90 def= 34
475 Hallowed Mimic | lifeMax= 3500 dmg= 90 def= 34
476 Jungle Mimic | lifeMax= 3500 dmg= 90 def= 34
477 Mothron | lifeMax= 6000 dmg= 80 def= 30
460 Butcher | lifeMax= 700 dmg= 70 def= 30
463 Nailhead | lifeMax= 4000 dmg= 100 def= 34
466 Psycho | lifeMax= 550 dmg= 70 def= 40
467 Deadly Sphere | lifeMax= 350 dmg= 100 def= 80
468 Dr. Man Fly | lifeMax= 500 dmg= 65 def= 24
469 The Possessed | lifeMax= 600 dmg= 68 def= 28
489 Blood Zombie | lifeMax= 75 dmg= 20 def= 8
490 Drippler | lifeMax= 50 dmg= 28 def= 14
546 Angry Tumbler | lifeMax= 50 dmg= 30 def= 6
580 Antlion Charger | lifeMax= 80 dmg= 25 def= 10
581 Antlion Swarmer | lifeMax= 60 dmg= 29 def= 8
661 Prismatic Lacewing | lifeMax= 5 dmg= 0 def= 0
669 Stinkbug | lifeMax= 5 dmg= 0 def= 0

```


---

## 🤖 Assistant · 2026-08-13T05:40:23.047Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have authoritative names. Key clarifications:
- 82 = Wraith (our code line 1903-1904 gates it: hardMode && surface && night && 1/20 or full moon 1/5). ✓ GATED.
- 104 = Werewolf ✓ (line 2225, hardMode + new moon).
- 145 = Snow Balla (frost legion), not werewolf.
- 77 = Armored Skeleton (line 2391-2396, hardMode gated). ✓
- 78 = Mummy (lines 2013, 2024, hardMode gated). ✓
- 98 = World Feeder (line 1884, hardMode gated, 3/4). Body/tail 99/100 NOT spawned — need to check whether Enemy.ts worm families handle it (aiStyle 5).
- 99/100 = "NPC_99"/"NPC_100" = World Feeder body/tail (lifeMax 500, dmg 55/40, def 40/44). Are they ever spawned? Let me check Enemy.ts for worm family handling: does spawning 98 auto-generate 99/100? Let me grep for 99/100 in Enemy.ts and fighterFamilies.ts.
- 109 = Clown ✓ gated hardMode && bloodMoon (line 2218).
- 358 = Lightning Bug (line 2195) — no hardMode gate; only hallow-grass tile implies hardmode. Implicit.
- 629 = Ice Mimic (line 1897, hardMode gated at 1892) ✓
- 85 = Mimic (line 1898 fallback under hardMode gate; line 1901 also hardMode) ✓
- 473/474/475/476 = corrupt/crimson/hallowed/jungle Mimic — hardMode gated at 1892; but note our comment says these ids are MISSING from vanilla-npcs.json → fromVanilla returns null → silently dropped! Let me verify: 473 Corrupt Mimic IS in the JSON (lifeMax 3500). So the comment at line 1890-1891 ("473/474/475/476 与 629 在 vanilla-npcs.json 无条目") is STALE — they DO have entries now. Interesting finding worth reporting: the comment claims they're missing but the JSON has them. So they actually spawn now.
- 630 = "None" in JSON — the comment at line 2026 says "json 缺 630 → null，登记台账" — CORRECT, 630 (Blood Mummy) is missing → silently dropped.
- 84 = Enchanted Sword (our comment says 神圣噬魂怪 which is wrong name, but whatever) — hardMode gated at line 2052. ✓
- 163 = "NPC_163" = Black Widow; 164 = "NPC_164" = Wall Creeper. 163 gated hardMode ✓.
- 661 = Prismatic Lacewing (critter) — gated downedPlant && night && surfaceSpawn && hardMode (inside hardMode block at 2041) ✓.
- 534 = Tortured Soul — hardMode ✓ (line 2296).
- 287 = Bone Lee (comment said 技师/tactical skeleton — wrong name; 287 is Bone Lee) — hardDungeon = hardMode && downed_262 ✓.
- 291/292/293: let me check names. In the dungeon block: 293 (variant 0), 291 (variant 1), 292 (variant 2). Vanilla: 290 Skeleton Sniper, 289 Tactical Skeleton, 291 Skeleton Commando? Actually 288-296 are post-plantera dungeon skeletons: 288 Blue Armored Bones, 289 Rusty Armored Bones? Hmm. Whatever — they're hardDungeon gated.

Now let me check:
1. World Feeder 99/100 worm segments — are they spawned anywhere?
2. Whether eclipse requires hardMode in our clock (so eclipse branch's lack of a hardMode gate matters or not).
3. Whether bloodMoon requires hardMode.
4. downed_398 (moon lord) — does the spawner use it anywhere? No. Only LunarEvent.
5. The ScaleStats gates: difficulty, hardMode, downedPlantBoss. Note: there's no post-mech / post-moonlord scaling. Only downedPlantBoss (80→100 threshold).

Also important for (B): scaleStats inputs — world difficulty (0/1/2 = classic/expert/master + getGoodWorld +1), hardMode, downedPlantBoss, anyNpc, activePlayerCount (hardcoded 1). And the caller passes NO activePlayersCount or strengthOverride → ctx defaults.

Let me check eclipse and bloodMoon triggers.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:40:23.247Z · glm-x-preview-260804

```
Let me check the eclipse/bloodMoon triggers and World Feeder worm segment handling.
```


---

## 🤖 Assistant · 2026-08-13T05:40:23.935Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"eclipse\" ~/Project/GLM/SandboxWorld/game/src/world/Clock.ts 2>/dev/null | head -20; echo \"---- CLOCK FILE ----\"; find ~/Project/GLM/SandboxWorld/game/src -name \"*.ts\" | xargs grep -ln \"eclipse = true\\|eclipse=true\" 2>/dev/null",
 "description": "Find eclipse trigger logic"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:24.046Z

**📎 ToolResult**

```
---- CLOCK FILE ----
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/lighting/SkyColor.ts

```


---

## 🤖 Assistant · 2026-08-13T05:40:24.687Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"\\b99\\b.*World Feeder\\|World Feeder\\|WORM_FAMILY\\|wormFamily\\|segmentsFor\\|98\" ~/Project/GLM/SandboxWorld/game/src/entities/fighterFamilies.ts | head -20",
 "description": "Check worm family handling for World Feeder"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:24.714Z

**📎 ToolResult**

```
46:    || id === 409 || inRange(id, 498, 506) || id === 424 || id === 426 || id === 520;
70:  if (id === 109) return { max: 2, accel: 0.04, damp: 0.8 };        // :57976-57998 小丑
74:    || id === 168 || id === 185 || id === 198 || id === 201 || id === 202 || id === 203
141:    if (id === 79 || id === 630) num87 *= 1.5;     // :58298-58301
164:    let num98 = 0.1;                                                  // :58460-58480 分段加速衰减
166:      if (Math.abs(e.vx) > t) num98 *= 0.8;
170:      accel: num98,
181:    if (id === 532) return { max: 5, accel: 0.15, damp: 0.98 };       // :58640-58643

```


---

## 🤖 Assistant · 2026-08-13T05:40:27.167Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"eclipse = true\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Find eclipse trigger line in Game.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:27.189Z

**📎 ToolResult**

```
3226:          w.clock.eclipse = true;
4968:        this.world.clock.eclipse = true;
11223:        w.clock.eclipse = true;

```


---

## 🤖 Assistant · 2026-08-13T05:40:27.699Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"spawnWormSegments\\|wormSegments\\|makeWorm\\|segment\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -20",
 "description": "Find worm segment spawn logic in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:27.727Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-13T05:40:28.926Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me look at those eclipse trigger lines to check for hardMode gates.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:40:29.180Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 18,
 "offset": 3218
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:29.192Z

**📎 ToolResult**

```
3218	        if (w.invasionDelay > 0) w.invasionDelay--;
3219	        // 日食自然 roll（Main.cs:64898-64920）：hardMode && downedMechBossAny &&
3220	        // 1/20 → eclipse=true + 公告 LegacyMisc.20（remix 的 misc.106 无对应世界）。
3221	        // 原版与当日哥布林/海盗 roll 互斥（同一段 if/else）——命中日食则跳过入侵 roll。
3222	        // stopEvents 压掉整段（StartDay 头部 stopEvents → return，:64893-64895）
3223	        const mechAny = !!(w.flags['downed_125'] || w.flags['downed_126']
3224	          || w.flags['downed_127'] || w.flags['downed_134']);
3225	        if (!stopEvents && w.flags.hardMode && mechAny && Math.random() < 1 / 20) {
3226	          w.clock.eclipse = true;
3227	          this.newText(Lang.misc(20), 50, 255, 130);   // ChatColors.World
3228	        } else if (!stopEvents) {
3229	          // 月事件进行中则整段 return（Main.cs:64922-64926 snowMoon||pumpkinMoon||DD2）
3230	          if (!moonEventActive(w) && !w.oldOnesArmy.ongoing) {
3231	            // 哥布林军队自然 roll（Main.cs:64927-64936）：需砸过暗影珠/猩红之心；
3232	            // 未击败过 1/3，已击败 hardMode 1/60 否则 1/30。
3233	            // ★掷骰在门之前（:64929 rand.Next(3) 只要 shadowOrbSmashed 就无条件消耗）：
3234	            // invasionType/生命上限门在 StartInvasion（:63890/:63902）内——曾把门前置
3235	            // 导致少掷一次，RNG 与原版分叉。命中后直接 startInvasion（自带 invasionType

```


---

## 🤖 Assistant · 2026-08-13T05:40:29.372Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 12,
 "offset": 4962
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:29.384Z

**📎 ToolResult**

```
4962	      this.input.mouseDown = false;
4963	    } else if (heldDef && heldDef.key === 'vi_2767_solar_tablet'
4964	      && inp.mouseDown && this.player.useTime === 0) {
4965	      // 日耀碑牌（Player.cs:43308/51431：dayTime && !eclipse && hardMode 才可用，
4966	      // 成功 → Main.eclipse=true + Lang.misc[20] 公告；非白天/已日食/肉前静默不可用）
4967	      if (this.world.flags.hardMode && this.world.clock.isDay && !this.world.clock.eclipse) {
4968	        this.world.clock.eclipse = true;
4969	        this.newText(Lang.misc(20), 50, 255, 130);   // ChatColors.World
4970	        this.player.inv.removeAt(this.player.inv.selected, 1);
4971	        this.player.useTime = 60;
4972	        this.cb.onInventoryChanged();
4973	      } else if (!this.world.clock.isDay) {

```


---

## 🤖 Assistant · 2026-08-13T05:40:29.663Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "limit": 14,
 "offset": 11214
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:29.675Z

**📎 ToolResult**

```
11214	    if (this.net && !this.net.policy.isHost) return '仅房主可触发事件';
11215	    switch (key) {
11216	      case 'bloodMoon':
11217	        w.clock.bloodMoon = true;
11218	        w.sundialCooldown = 0; w.moondialCooldown = 0;   // 血月清晷冷却（:64892-64893）
11219	        this.newText(Lang.misc(8), 50, 255, 130);
11220	        return null;
11221	      case 'eclipse':
11222	        if (!w.clock.isDay) return '现在是夜晚——日食黄昏即被自然清除,请白天触发';
11223	        w.clock.eclipse = true;
11224	        this.newText(Lang.misc(20), 50, 255, 130);
11225	        return null;
11226	      case 'meteor':
11227	        this.meteorPending = true;   // 消费门:夜午夜后/昼 9AM 后,落点走保护/上限

```


---

## 🤖 Assistant · 2026-08-13T05:40:35.426Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important finding: There's a debug/admin command at line 11221-11225 that can set eclipse WITHOUT hardmode. So the eclipse spawn branch (line 1824-1843) could be reached in a pre-hardmode world via this command. In vanilla, eclipse can only happen in hardmode. So the eclipse spawn branch has NO hardMode gate and relies on the eclipse triggers being hardmode-gated. That's worth flagging as an "implicit gate" (with a debug-command hole).

Let me check the context of that 11221 switch — is it a debug/dev event trigger? Let me check briefly.

Also let me now check whether World Feeder (98) spawns body/tail segments (99/100). Let me look at how multi-segment worms are spawned in our engine. Search for aiStyle 5 family / "spawnWorm" in Enemy.ts or Game.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:40:36.181Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"triggerWorldEvent\\|devTrigger\\|debugEvent\\|case 'bloodMoon'\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | head; echo ---; sed -n '11195,11215p' ~/Project/GLM/SandboxWorld/game/src/core/Game.ts",
 "description": "Identify context of event trigger switch"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:36.215Z

**📎 ToolResult**

```
10046:      case 'bloodMoon': return this.world.clock.bloodMoon;
11216:      case 'bloodMoon':
---
    }
    this.summonPanel.toggle();
    this.input.uiBlocking = this.summonPanel.open;
  }

  /** F6 事件触发(调试):全部走**自然事件入口**——与自然 roll 命中同路径/同公告/
   *  同清旗点,不绕过保护门与昼夜消费时序,自然流程零破坏:
   *  - 血月 = 黄昏 roll 命中体(bloodMoon+清晷冷却+misc[8],Main.cs:64813-64831);
   *    夜间生效、黎明自然清除——白天按下 = 当晚升起
   *  - 日食 = 黎明 roll 命中体(eclipse+misc[20],Main.cs:64898-64920);黄昏自然清除,
   *    夜间按下会被即刻清除故拦下
   *  - 陨石 = 仅置 meteorPending(同 EoW 击杀/入夜 1/50 的旗位),消费仍走
   *    HandleMeteorFall 原始 time>16200 门(夜=午夜后/昼=9AM 后)+落点保护
   *  - 流星雨 = StartMeteorShower(:6189-6194) 计数 [650,751)×4
   *  - 入侵 = announceNaturalInvasion(StartInvasion 门:生命上限/Boss 在场/进行中) */
  debugTriggerEvent(key: string): string | null {
    const w = this.world;
    if (!w) return '世界未就绪';
    // 联机访客拦下(事件权威在房主,同 summonBossAtTx 的 Boss 门)
    if (this.net && !this.net.policy.isHost) return '仅房主可触发事件';
    switch (key) {

```


---

## 🤖 Assistant · 2026-08-13T05:40:36.946Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"aiStyle === 5\\|aiStyle5\\|AI_005\\|wormSegments\\|spawnSegments\\|attachSegments\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -15",
 "description": "Find worm ai handling"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:36.974Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:484:    const flying = v.noGravity || v.aiStyle === 2 || v.aiStyle === 5 || v.aiStyle === 14;
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:514:      nightOnly: v.aiStyle === 2 || v.aiStyle === 5, underground: false,
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:639:   *  直接用玩家坐标差算位移向量的族（AI_005 蜂群/AI_013 植物/AI_056 地牢之魂）
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:803:        case 5: this.swarmerAI(game, p); break;                         // AI_005 噬魂怪族（原版蜂群核）
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:1956:      flying: v.noGravity || v.aiStyle === 2 || v.aiStyle === 5 || v.aiStyle === 14,
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts:2681:  /** AI_005 噬魂怪族（NPC.cs:17567-17790）"蜂群"AI：

```


---

## 🤖 Assistant · 2026-08-13T05:40:41.588Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So eclipse debug trigger = F6 debug event, intentionally bypassing protection gates ("不绕过保护门" claim in comment but eclipse case has no hardMode check — the bloodMoon case has none either, but bloodmoon is fine pre-hardmode in vanilla). So eclipse can be forced pre-hardmode via F6 debug. That's the hole. Worth flagging.

Now, World Feeder 98 spawns as a single NPC (no 99/100 segments) — our engine treats it as aiStyle 5 "swarmer" not a segmented worm. Actually wait, vanilla World Feeder is a worm (aiStyle 5 with segments 99/100)? Hmm, in vanilla, World Feeder (98) is a segmented worm with body 99 and tail 100. Our code spawns only the head 98 and Enemy.ts treats aiStyle 5 as a swarmer (噬魂怪族). Hmm, but for Devourer (7) we spawn D(7) which is also a segmented worm. So this is a general "worm segments not modeled" simplification — probably registered in docs/spawn-parity-gaps.md. Let me check that doc to see if it exists and mentions these.

Let me check docs/spawn-parity-gaps.md.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:40:41.976Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld -name \"spawn-parity-gaps.md\" -not -path \"*/node_modules/*\" | head -3",
 "description": "Locate spawn parity gaps doc"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:42.036Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/docs/spawn-parity-gaps.md

```


---

## 🤖 Assistant · 2026-08-13T05:40:43.647Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"98\\|99\\|100\\|World Feeder\\|蠕虫\\|worm\" ~/Project/GLM/SandboxWorld/game/docs/spawn-parity-gaps.md | head -25",
 "description": "Check parity gaps doc for worm entries"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:43.675Z

**📎 ToolResult**

```
18:| 猩红段 tile 门+分层(高2) | :3973-4031 | 旧用 ZoneCrimson 整段拦截(腐化边界/猩红矿外怪被劫持)且 182/268 无 hard 门(肉前误出);现照原文 tile 门 `(204&&ZoneCrimson)\|\|199/200/203/234/662` + 十支分层(179/182 带 !noWorms、268/174 hard 门、239 血爬虫、-22~-25 netId) | ✅ 2026-08-13 |
20:| Devourer 段(高3) | :3611-3621/:5478-5492 | 整段缺失——腐化区永不出吞噬怪;CanSpawnDevourer 查原文=!infectedSeed 恒 true(本仓无种子系统),门=ZoneCorrupt&&1/65&&!noWorms,hard 3/4 出 98(探求者)else 7 | ✅ 2026-08-13 |
24:| 天空 686+飞龙门(中7) | :1316-1331 | 飞龙 87 缺 !noWorms(房屋内出蠕虫);686 绑缚紫史莱姆支整体缺失(!unlockedSlimePurpleSpawn 恒 false+1/25+场上唯一) | ✅ 2026-08-13 |
28:| 丛林四支(中11) | :3713-3830 | 地表小动物(671-675/SpawnFrog)、蜂巢块 225 落脚(hard 苔藓黄蜂族)、困难丛林草 60 主池(152/177/205/236/176/175/153)、神庙砖 226/232(墙 87 门,1/3 飞蛇 226 else 198)四段缺失,全补 | ✅ 2026-08-13 |
29:| 雨雪高仑/探测器(中12) | :4094-4108 | 243 冰雪高仑(雪原雨 hard 1/20 唯一)、250 雨云怪(!雪原雨 hard CountNPCS<2 1/10)、399 地表支(flag17+downedGolemBoss+(1/100 或 1/400))三支缺失,全补 | ✅ 2026-08-13 |
37:| 城镇 noWorms 置位(中) | :717/:734/:750/:767/:792/:814 | GetSpawnRate 城镇段原版会置 noWorms(城镇 NPC≥1 地表恒置,地狱侧按 town 数掷骰)→ 城镇附近不出蠕虫;旧实现缺失。本仓 getSpawnRate/spawn 拆两次调用 → townNoWorms 闩锁 + spawn() 合成 | ✅ 2026-08-13 |
40:| 水池第三支(中) | :1906-1993 | 整支缺失:waterTile&&1/4&&(x 在海洋带间\|\|y>ws+50) → 腐化 57/猩红 465 金鱼 / 白天地表水面线小动物(616 水黾/608 鸊鷉/613/612 水黾群/362/364 鸭)/深水夜间 607 鳉/592 金金鱼/55 金鱼;**无** !spawnFriendly 门(友好轮也可命中) | ✅ 2026-08-13 |
47:| 绑缚三人组 105/106/685 | :1994-2005 | 主链 spawnFriendly 块之前三支 else-if 补齐(1:1,&& 求值序保持 RNG 流):门=RollLuck(20)&&!waterTile&&deeperThanRockLayer&&y<h-210&&!saved*/场上唯一;前置 105=downedGoblins/106=hardMode/685=downedBoss3&&!unlockedSlimeOldSpawn。产出为 bound TownNPC(VanillaSpawner.spawnBound 占位体→Game.trySpawnEnemy 转换,685 无 json 条目走 PLACEHOLDER_DEF);bound TownNPC 经 BOUND_TOWN_NPC_ID 反查登记进 activeIds 使 !AnyNPCs 门成立;685 解救置 flags.unlockedSlimeOldSpawn(WF:1410)。附带修复:setPlayerFlags 的 downedBoss3 改双键 downedSkeletron\|\|downed_35(旧只传 downedSkeletron 恒 false,地牢守卫池永不切换) | ✅ 2026-08-13 |
48:| 夜萤火虫概率源 setFireFlyChance | :94557-94610/:4413 | 旧恒代表值 30;现每夜 StartNight 掷三档(1/9 高发 5-9 / 1/3 绝迹 999999 / 其余 10-59)落 World 五字段(随存档,旧档缺省=代表值),萤火虫门读 world.fireFlyChance;同源补白昼椿象 669(:2381)/蝴蝶 356\|金 444(:2394)两支(读 stinkBugChance/butterflyChance,位于瓢虫支之前=原版链序) | ✅ 2026-08-13 |
56:| 天空 ZoneWaterCandle 加重支 | :1299-1312/:1320-1324 | 影烛下 399 概率 1/8→1/3、87 1/10 加重与重复支未接 | ZoneWaterCandle 上下文(skyMob 段) |
57:| 天空/地表 399 的 skyBehindPlayer/AnyDanger 上下文 | :1292-1295/:4079-4081 | flag5/flag17 的"玩家背后/无危险"压制未跟踪→探测器略偏多 | skyBehindPlayer(生成点在玩家上空侧)+AnyDanger(NPC 敌对检测) |
62:| 290 暗影束 aiStyle48 反射 | 束弹撞墙反射数段 | 死灵法师束撞墙即灭(束速 updates=100 已近似瞬达) | 反射计数 + 重新瞄准 |
64:| 216 海盗火枪手专家炮弹 | num171=100/240 | 专家模式未实装,恒 180 弹 | 专家模式旗 |
66:| CountNPCS 计数通道 | :2590/:4100 等 | 250 雨云怪 CountNPCS<2 / 513 唯一门在无月事件/塔 ctx 时退化为 activeIds 0/1 检测(1 只即视为"占满"→雨云怪上限 1 而非 2) | Game 侧常驻 counts 表(或 activeIds 改 Multiset) |
92:| 天空 399 概率近似 | :1292-1312 原版 maxValue2/maxValue3=8/30(影烛 3/10);本仓取 `downedMartians?30:8`,影烛加重支未接(见待补) |

```


---

## 🤖 Assistant · 2026-08-13T05:40:49.276Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The parity doc is detailed. Good. Now I have everything I need for the deliverable. Let me do a final check on a couple of things:

1. Verify the `this.hardMode` initialization and where `hardMode` gets refreshed (line 2607 in spawn()).
2. Check `debugPoolOverride` (line 16, 2647) — test hook.
3. Double-check the exact line numbers for the key branches. I have them from the read.
4. Check getSpawnRate's caller signature in Game.ts (line 8952-8958) — done.
5. Verify scaleStats callers pass no activePlayersCount/strengthOverride — fromVanilla at Enemy.ts:500 calls `scaleStats(ss)` with just one arg. ✓

Let me also verify line numbers for key things in Enemy.ts: difficulty field (line 134-138).

Let me read Enemy.ts lines 120-145 to confirm the difficulty field.

Also let me double check whether `mainExpertMode` is used in Enemy.ts for spawn — no.

One more thing to verify: the `noWorms` gating and `townNoWorms` latching — is townNoWorms actually consumed in spawn()? Line 256 mentions "先闩锁,spawn() 合成" but I didn't see townNoWorms used in spawn() in the code I read. Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:40:49.591Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"townNoWorms\" ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts",
 "description": "Check townNoWorms consumption"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:49.614Z

**📎 ToolResult**

```
256:  private townNoWorms = false;
809:    this.townNoWorms = false;
818:          if (this.rateRng() < 1 / 2) this.townNoWorms = true;              // :717-720
822:          if (this.rateRng() >= 1 / 4) this.townNoWorms = true;             // :734-737 Next(4)!=0
826:          if (this.rateRng() >= 1 / 10) this.townNoWorms = true;            // :750-753 Next(10)!=0
842:          this.townNoWorms = true;                                          // :767
849:          this.townNoWorms = true;                                          // :792
856:          this.townNoWorms = true;                                          // :814

```


---

## 🤖 Assistant · 2026-08-13T05:40:49.820Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 18,
 "offset": 126
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:40:49.826Z

**📎 ToolResult**

```
126	  width: 16, height: 16, mapColor: '#9A8FA0', gore: ['#9A8FA0', '#5E5566', '#C4BACC'],
127	  hitSound: ['NPC_Hit_1'], killedSound: ['NPC_Killed_1'], drops: [],
128	};
129	
130	export class Enemy extends Entity {
131	  /** 原版 NPC id（数据驱动路径启用时非空） */
132	  vanillaId: number | null = null;
133	  vanilla: VanillaNpc | null = null;
134	  /** npc.difficulty（ScaleStats 写入，NPC.cs:18086 = strengthOverride ?? Main.Difficulty）：
135	   *  原版档位浮点（Classic 1/Expert 2/Master 3，getGoodWorld +1）——AI 段
136	   *  GetAttackDamage_ScaledByDifficulty/ForProjectiles（如饥饿者 :26341）消费。
137	   *  未进 ScaleStats 门（friendly/townNPC/无伤小动物）保持 0（原版字段初值） */
138	  difficulty = 0;
139	  /** defDamage 的【未缩放】基线（ScaleStats 前的 v.damage，critter/friendly 归零后值）。
140	   *  敌怪弹幕出膛原版一律用 ForProjectiles(基线, 基线×N) 这类显式档位 lerp
141	   *  （NPC.cs:21180 等），命中玩家的难度乘区在 Projectile.cs:13770 统一做——
142	   *  若此处误用缩放后的 def.damage 会与命中端乘区叠加成双重缩放 */
143	  baseDamage = 0;

```


---

## 🤖 Assistant · 2026-08-13T05:41:05.226Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Notable finding: `townNoWorms` is latched in getSpawnRate but NEVER consumed in spawn()/spawnAnNPC — i.e. the "城镇附近不出蠕虫" (no worms near town) latching is written but never read. The field is private and only assigned, never read. That's a dead latch — a bug worth reporting under (C) since it's part of spawn-rate/noWorms flow. Wait, but the comment says "spawn() 合成" (composed in spawn()). Let me search for `this.noWorms` assignment in spawn() to see if townNoWorms is used. Line 2610: `this.noWorms = ... WALL_HOUSE...`. That's the only assignment in spawn(). So indeed townNoWorms is never composed into noWorms. Confirmed dead latch. Good finding.

Now I have everything. Let me compile the deliverable.

Let me be careful and precise about line numbers. Let me verify a few line numbers precisely by grepping for specific markers.

Key branch line numbers from my read of VanillaSpawner.ts:
- setPlayerFlags: 327-347
- setWeather: 353-357
- slimeRainSpawns: 365-397
- getSpawnRate: 644-875
  - moonEvent override: 652-654
  - invaders/lunar override: 657-659
  - base 600/5: 660-661
  - hardMode rate×0.9 max+1: 665-668
  - underworld max×2: 670-672
  - cavern ×0.4/×1.9: 673-676
  - underground ×0.5/×1.7: 677-680
  - night ×0.6/×1.3: 681-685; blood moon ×0.3/×1.8: 686-689
  - eclipse day ×0.2/×1.9: 690-694
  - rain snow: 703-706
  - dungeon/sandstorm/ugdesert/jungle/corrupt-crimson/meteor chain: 720-749
  - temple: 752-755
  - hallow deep: 757-760
  - nearbySlots tiers: 762-770
  - calmed: 772-775; sunflower: 777-780; battle: 782-785; water candle: 787-790; peace candle: 791-795
  - clamps: 797-798
  - dungeon pre-skeletron rate=10: 800
  - spawnFriendly rolls: 808-866
  - bad-luck roll: 870-873
- findSpawnTile: 892-944; skyMob selection: 922-928
- spawn(): 2603-2652; hardMode refresh: 2607
- spawnAnNPC: 1258-2437
  Branch order:
  1. lunar towers: 1285-1327
  2. skyMob: 1331-1349
  3. invaders: 1351-1416
  4. spider nest: 1419-1424
  5. underground desert: 1429-1466
  6. hardmode water jungle/crimson: 1470-1474
  7. ocean: 1485-1543
  8. statue mimic: 1552-1556
  9. water pool A/B: 1560-1597
  10. water pool third: 1604-1638
  11. bound trio: 1650-1664
  12. graveyard friendly: 1668-1671
  13. rain gem critters: 1680-1685
  14. surface critters: 1688-1731
  15. cave gem critters: 1737-1744
  16. friendly guard: 1747
  17. dungeon: 1753-1808
  18. meteor: 1811
  19. moon event: 1814-1820
  20. eclipse: 1824-1843
  21. mushroom: 1845-1876
  22. devourer: 1883-1886
  23. rare cave / 473-476/629/85: 1892-1899
  24. wall 2 → 85: 1901
  25. wraith 82: 1903-1904
  26. jungle grass night 52: 1906
  27. jungle 219: 1908
  28. cave critters: 1913-1921
  29. jungle surface critters: 1926-1931
  30. hive block: 1934-1943
  31. hard jungle grass pool: 1947-1961
  32. temple: 1964-1966
  33. hive wall 86: 1968
  34. jungle grass (pre-hard): 1970-1981
  35. sandstorm: 1987-2021
  36. desert surface mummies: 2024-2027
  37. hallow tiles: 2031-2050 (661 at 2043-2044, 244 at 2045, 122 at 2046, 86 at 2048, 75 at 2049)
  38. hallow devourer 84: 2052-2054
  39. crimson: 2059-2086
  40. corrupt: 2091-2106
  41. surfaceSpawn: 2110-2274
     - graveyard maggot: 2119-2121
     - ice golem 243: 2124; nimbus 250: 2126; martian probe 399: 2130-2134
     - day pool: 2138-2183
     - night pool: 2191-2273
       - firefly/lightning bug: 2192-2196
       - raven 301: 2198; ghost 316: 2200; hoppin jack 304: 2202
       - wandering eye 133: 2206; demon eyes: 2208; zombies: 2213-2215
       - clown 109: 2218
       - groom/bride: 2222-2223
       - werewolf 104: 2225; possessed armor 140: 2227
       - blood zombie/drippler: 2229
       - ice tile: 2335-2240 → wait, 2235-2240
       - raincoat zombie: 2242-2245
       - moss zombie 691: 2248; maggot zombie 632: 2251
       - torch zombie 590/591: 2256
       - armed zombies: 2261-2264
       - final zombie table: 2267-2273
  42. underground: 2276-2288
  43. underworld: 2292-2319
  44. rock golem: 2323
  45. cave pool: 2327-2436

Let me double-check some of these line numbers by grepping quickly. Actually my Read output gave exact line numbers, and I've been tracking them. I'm confident.

Let me verify a few specific ones with grep to be safe.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:41:05.472Z · glm-x-preview-260804

```
Let me verify a few key line numbers before compiling the report.
```


---

## 🤖 Assistant · 2026-08-13T05:41:06.819Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"if (this.lunar)\\|if (this.skyMob)\\|if (this.invaders)\\|const hardDungeon\\|if (this.ZoneDungeon) {\\|if (this.ZoneMeteor) return\\|this.surfaceSpawn && this.dayTime && this.world.clock.eclipse\\|if (t === T.MUSHROOM_GRASS)\\|if (this.ZoneCorrupt && N(65)\\|if (this.surfaceSpawn) {\\|if (this.underGround) {\\|if (this.spawnTileY > st.h - 190)\\|if (this.checkToSpawnRockGolem\\|return D(49);  // Cave Bat\" ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts",
 "description": "Verify branch entry line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:41:06.855Z

**📎 ToolResult**

```
720:    if (this.ZoneDungeon) {
1285:    if (this.lunar) {
1331:    if (this.skyMob) {
1351:    if (this.invaders) {
1762:    if (this.ZoneDungeon) {
1773:        const hardDungeon = this.hardMode && !!this.world.flags['downed_262']; // downedPlantBoss（世花 262，Game 击杀通用置位链 downed_{id}）
1821:    if (this.ZoneMeteor) return D(23);
1834:    if (this.surfaceSpawn && this.dayTime && this.world.clock.eclipse) {
1855:    if (t === T.MUSHROOM_GRASS) {
1893:    if (this.ZoneCorrupt && N(65) && !this.noWorms && this.canSpawnDevourer()) {
2120:    if (this.surfaceSpawn) {
2286:    if (this.underGround) {
2302:    if (this.spawnTileY > st.h - 190) {
2333:    if (this.checkToSpawnRockGolem(rng)) return D(631);
2446:    return D(49);  // Cave Bat

```


---

## 🤖 Assistant · 2026-08-13T05:41:07.417Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"downed_398\\|downed_245\" ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts ~/Project/GLM/SandboxWorld/game/src/stats/ScaleStats.ts",
 "description": "Check moon lord golem flag usage in spawner and scalestats"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:41:07.457Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:1337:      if (hardMode && this.world.flags['downed_245'] && !any(399)
~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts:2141:      if (flag17 && hardMode && this.world.flags['downed_245']

```


---

## 🤖 Assistant · 2026-08-13T05:41:23.543Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line numbers confirmed (my Read output was from the same file so they match; the grep shows slightly different line numbers for some — e.g. ZoneMeteor at 1821 vs my read at 1811, eclipse at 1834 vs 1824, MUSHROOM_GRASS at 1855 vs 1845, devourer at 1893 vs 1883, surfaceSpawn at 2120 vs 2110, underGround at 2286 vs 2276, underworld at 2302 vs 2292, rock golem at 2333 vs 2323, cave bat at 2446 vs 2436).

There's a consistent +10 offset for lines after ~1811! That means the file was MODIFIED between my Read and this grep? No — wait. The Read output I got shows `if (this.ZoneMeteor) return D(23);` at line 1811. But grep says 1821. A 10-line offset. That means the file changed between my read and now?? That seems unlikely in this read-only environment... but possible if something else is editing (the user's other agents?).

Hmm, actually more likely: my Read tool output line numbers are authoritative and the grep... no, grep is authoritative too. Both can't be right.

Wait — let me re-check. In my Read output:
- Line 1753: `if (this.ZoneDungeon) {` — grep says 1762. Offset +9.
- Line 1811: `if (this.ZoneMeteor) return D(23);` — grep says 1821. Offset +10.
- Line 2110: `if (this.surfaceSpawn) {` — grep says 2120. Offset +10.
- Line 2333 in my read: `if (this.checkToSpawnRockGolem(rng)) return D(631);` — grep also says 2333! Offset 0?!

Wait, in my read: line 2323 is `if (this.checkToSpawnRockGolem(rng)) return D(631);`. grep says 2333. Offset +10.

And `return D(49);  // Cave Bat` my read line 2436, grep 2446. +10.

But `if (this.lunar) {` my read 1285, grep 1285. Offset 0.
`if (this.skyMob) {` 1331 both. 0.
`if (this.invaders) {` 1351 both. 0.
`if (this.ZoneMeteor)` 1811 vs 1821 → +10.
`this.surfaceSpawn && this.dayTime && ... eclipse` 1824 vs 1834 → +10.
`if (t === T.MUSHROOM_GRASS)` 1845 vs 1855 → +10.
`if (this.ZoneCorrupt && N(65)...` 1883 vs 1893 → +10.
`if (this.surfaceSpawn) {` 2110 vs 2120 → +10.
`if (this.underGround) {` 2276 vs 2286 → +10.
`if (this.spawnTileY > st.h - 190)` 2292 vs 2302 → +10.
`if (this.checkToSpawnRockGolem` 2323 vs 2333 → +10.
`return D(49)` 2436 vs 2446 → +10.
`const hardDungeon` 1764 (my read) vs 1773 (grep) → +9.
`if (this.ZoneDungeon) {` 1753 vs 1762 → +9.

So the offset starts between 1351 and 1753, growing +9 then +10. That means ~10 lines were ADDED to the file somewhere between line 1351 and 1753 between my Read call and my grep call. The file is being actively modified (the user said mtime 13:35 on Enemy.ts; VanillaSpawner.ts may be being edited by another agent right now).

Hmm wait. But this is a read-only task for me. Other agents may be editing concurrently. I should re-read the affected region to get accurate line numbers for my report. Let me diff: read lines 1400-1800 again to find the inserted block.

Actually, more robust: let me re-derive line numbers with grep for all the branch anchors I need, rather than relying on my earlier Read. Let me first find what changed — grep around 1400-1460.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:41:23.927Z · glm-x-preview-260804

```
The file shifted by ~10 lines mid-analysis (concurrent edit). Let me re-verify current line numbers.
```


---

## 🤖 Assistant · 2026-08-13T05:41:24.176Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts",
 "limit": 45,
 "offset": 1415
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:41:24.187Z

**📎 ToolResult**

```
1415	      }
1416	    }
1417	
1418	    // ---- 蜘蛛巢（L1568-1587）：(墙 62 || spawnSpider) && CheckToSpawnSpider ----
1419	    const wall = st.wall[st.idx(this.spawnTileX, this.spawnTileY)];
1420	    if (wall === 62 || this.spawnSpider) {
1421	      // flag7（L1574-1578）= deeperThanRockLayer && y<h-210（dontStarve 变体不适用）
1422	      const flag7 = this.deeperThanRockLayer && this.spawnTileY < st.h - 210;
1423	      // 造型师 354（L1579-1581）：墙 62 专属门 + 1/8 + !water + flag7 +
1424	      // !savedStylist + 场内唯一——曾因生成期 placeBoundRescueNpcs 近似而"注释保留"
1425	      // 跳过；2026-08-13 移除生成期放置后按原版补齐（D 真条目，Game 侧转 bound TownNPC）
1426	      if (wall === 62 && N(8) === 0 && !this.waterTile && flag7
1427	        && !this.world.flags['savedStylist'] && !any(354)) return D(354);
1428	      if (this.hardMode && !N(10)) return D(163);  // hardMode 9/10 黑寡妇(L1583)
1429	      return D(164);                               // 爬墙者
1430	    }
1431	    // ---- 地下沙漠（L1589-1672 1:1）----
1432	    //  门：落点/上格带沙漠墙（AllowsUndergroundDesertEnemiesToSpawn≈spawnUndergroundDesert
1433	    //  邻域扫描已覆盖）&& WorldGen.checkUnderground（L1589 第二合取项，此前缺失——
1434	    //  浅层沙洞误判地下沙漠）
1435	    if (this.spawnUndergroundDesert && this.checkUnderground(this.spawnTileX, this.spawnTileY)) {
1436	      // num11 深度系数（L1591-1599）：岩石层下再深(>(rockLayer*2+h)/3)×0.5、
1437	      // 岩石层下 ×0.85，用于下方两支蠕虫的 1/(50*num11) 概率门
1438	      let num11 = 1.3;
1439	      if (this.spawnTileY > (this.world.rockLevel * 2 + st.h) / 3) num11 *= 0.5;
1440	      else if (this.spawnTileY > this.world.rockLevel) num11 *= 0.85;
1441	      // L1600：高尔夫球手 589（1/20，非水域，!savedGolfer，场内唯一）——
1442	      //  json 缺 589 条目 → spawnBound 占位体（同三人组），Game 侧转 bound TownNPC。
1443	      //  savedGolfer 由 freeBoundNpc 解救时写（"未跟踪恒 false"注释已过时）
1444	      if (N(20) && !this.waterTile && !this.world.flags['savedGolfer'] && !any(589)) {
1445	        return this.spawnBound(589);
1446	      }
1447	      // L1605：沙虫 510（hard，1/(50·num11)，非蠕虫禁置，落脚深于 worldSurface+100）
1448	      if (hardMode && N(Math.floor(50 * num11)) && !this.noWorms
1449	        && this.spawnTileY > this.world.groundLevel + 100) return D(510);
1450	      // L1610：墓穴爬虫 513（同概率门，场内唯一）
1451	      if (N(Math.floor(50 * num11)) && !this.noWorms
1452	        && this.spawnTileY > this.world.groundLevel + 100 && this.countNpc(513) === 0) return D(513);
1453	      // L1615：hard 4/5 加权池（SelectRandom：恶地双份 525/526/527、中立双份 524、
1454	      //  恶地补 533/529 否则 530/528、恒补 532）
1455	      if (hardMode && !N(5)) {
1456	        const ghoulPool: number[] = [];
1457	        if (this.ZoneCorrupt) ghoulPool.push(525, 525);
1458	        if (this.ZoneCrimson) ghoulPool.push(526, 526);
1459	        if (this.ZoneHallow) ghoulPool.push(527, 527);

```


---

## 🤖 Assistant · 2026-08-13T05:41:26.510Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: the spider nest branch was rewritten (stylist 354 added, golfer 589 now via spawnBound). The file is being actively edited. My original Read snapshot is stale for the spider/desert region.

Since the file is a moving target, the safest approach for line numbers: re-grep for all branch anchors NOW and report current line numbers, noting the file is being edited concurrently.

Let me do one comprehensive grep to get current line numbers for all the key anchors.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:41:28.637Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"return D(\\|return this.spawnNPC(\\|return this.spawnBound(\\|return D(pick)\\|if (this\\.\\|if (hardMode\\|if (t === T\\.\\|if (wall\\|if (iceTile\\|if (iceCave\\|if (iceAll\\|if (crimsonFloor\\|if (corruptFloor\\|if (hallowFloor\\|if (critGates\\|if (neutralCave\\|if (flag17\\|if (downedPlant\\|if (hardDungeon\\|if (this.spawnFriendlyCycle\\|if (this.ZoneGraveyard\\|if (N(\\|if ((t === T.LIHZAHRD\" ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts | awk -F: '$1>1250 && $1<2470' ",
 "description": "Extract all branch anchors with current line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:41:32.131Z

**📎 ToolResult**

```
1285:    if (this.lunar) {
1299:        if (id !== 0) return D(id);
1310:        if (id !== 0) return D(id);
1313:        return D(pick([411, 411, 411, 409, 409, 407, 402, 405]));
1325:        if (id !== 0) return D(id);
1331:    if (this.skyMob) {
1333:      if (this.invaders && this.world.invasionType === 4) return D(388);
1337:      if (hardMode && this.world.flags['downed_245'] && !any(399)
1340:        return D(399);
1343:      if (hardMode && !any(87) && !this.noWorms && N(10)) return D(87);
1347:      if (!UNLOCKED_SLIME_PURPLE_SPAWN && N(25) && !any(686)) return D(686);
1348:      return D(48);
1351:    if (this.invaders) {
1355:        if (hardMode && !any(471) && N(30)) return D(471);
1356:        if (N(9)) return D(29);
1357:        if (N(5)) return D(26);
1358:        if (N(3)) return D(111);
1359:        if (N(3)) return D(27);
1360:        return D(28);
1364:        if (N(7)) return D(145);
1365:        if (N(3)) return D(143);
1366:        return D(144);
1374:        if (this.world.invasionSize < this.world.invasionSizeStart / 2 && N(20) && !any(491)) {
1383:          if (clear) return this.spawnNPC(x, (this.spawnTileY - 10) * TILE, 491, rng);
1385:        if (N(30) && !any(216)) return D(216);
1386:        if (N(11)) return D(215);
1387:        if (N(9)) return D(252);
1388:        if (N(7)) return D(214);
1389:        if (N(3)) return D(213);
1390:        return D(212);
1400:        if (N(45) && saucerOk) return D(395);
1402:          if (N(20) && saucerOk) return D(395);
1403:          return D(rng.int(0, 1) === 0 ? 390 : 386);
1407:          return D(r9 < 2 ? 382 : r9 >= 4 ? 388 : 381);
1411:          if (!any(520)) return D(520);
1414:        return D(r10 === 0 ? 385 : r10 === 1 ? 389 : 383);
1420:    if (wall === 62 || this.spawnSpider) {
1426:      if (wall === 62 && N(8) === 0 && !this.waterTile && flag7
1427:        && !this.world.flags['savedStylist'] && !any(354)) return D(354);
1428:      if (this.hardMode && !N(10)) return D(163);  // hardMode 9/10 黑寡妇(L1583)
1429:      return D(164);                               // 爬墙者
1435:    if (this.spawnUndergroundDesert && this.checkUnderground(this.spawnTileX, this.spawnTileY)) {
1439:      if (this.spawnTileY > (this.world.rockLevel * 2 + st.h) / 3) num11 *= 0.5;
1440:      else if (this.spawnTileY > this.world.rockLevel) num11 *= 0.85;
1444:      if (N(20) && !this.waterTile && !this.world.flags['savedGolfer'] && !any(589)) {
1445:        return this.spawnBound(589);
1448:      if (hardMode && N(Math.floor(50 * num11)) && !this.noWorms
1449:        && this.spawnTileY > this.world.groundLevel + 100) return D(510);
1451:      if (N(Math.floor(50 * num11)) && !this.noWorms
1452:        && this.spawnTileY > this.world.groundLevel + 100 && this.countNpc(513) === 0) return D(513);
1455:      if (hardMode && !N(5)) {
1457:        if (this.ZoneCorrupt) ghoulPool.push(525, 525);
1458:        if (this.ZoneCrimson) ghoulPool.push(526, 526);
1459:        if (this.ZoneHallow) ghoulPool.push(527, 527);
1461:        if (this.ZoneCorrupt || this.ZoneCrimson) ghoulPool.push(533, 529);
1464:        return D(ghoulPool[rng.int(0, ghoulPool.length - 1)]);
1469:      if (N(15)) num12 = 537;
1470:      else if (N(10)) {
1474:      return D(num12);
1479:    if (hardMode && this.waterTile && this.ZoneJungle && !N(3)) return D(157);
1480:    if (hardMode && this.waterTile && this.ZoneCrimson) {
1481:      if (!N(3)) return D(242);
1482:      if (!N(3)) return D(241);
1506:      if (this.spawnTileY < this.world.groundLevel && this.spawnTileY > 50) {
1524:      if (num17 > 0 && !this.xRange && N(10)) return this.spawnNPC(x, num17 * TILE, 602, rng);
1530:      if (N(sharkChance)) return D(65);
1532:      if (hardMode && N(sharkChance)) return D(692);
1534:      if (N(10)) {
1536:        if (num20 === 0 && num17 > 0) return this.spawnNPC(x, num17 * TILE, 625, rng);  // 海龟
1537:        if (num20 === 1 && num18 > 0) return this.spawnNPC(x, num18 * TILE, 615, rng);  // 海豚
1540:          return this.spawnNPC(x, num22 * TILE, N(400) ? 627 : 626, rng);
1544:          return this.spawnNPC(x, num21 * TILE, 688, rng);
1548:      if (N(40)) return D(220);   // 海蜗牛（L1818-1821）
1549:      if (N(18)) return D(221);   // 鱿鱼（L1822-1825）
1550:      if (N(3)) return D(67);     // 螃蟹（L1826-1829）
1551:      return D(64);               // 粉水母兜底（L1830-1833）
1561:    if (this.downedBoss3 && this.ZoneGraveyard && !this.noWorms
1564:      return D(690);
1569:    if (this.waterTile && !this.isOcean && !this.spawnFriendlyCycle) {
1574:        if (t === T.JUNGLE_GRASS && this.surfaceSpawn && this.spawnTileY > 50 && N(3) && this.dayTime) {
1579:            if (N(4)) return this.spawnNPC(x, num23 * TILE, 617, rng);
1589:              return this.spawnNPC(jx, num23 * TILE - TILE, N(400) ? 613 : 612, rng);
1595:          if (hardMode && rng.next() < 2 / 3) return D(102);
1596:          return D(58);
1602:      if (this.spawnTileY > this.world.groundLevel && N(3)) {
1603:        if (hardMode && rng.next() < 2 / 3) return D(103);
1604:        return D(63);
1613:    if (this.waterTile && N(4) && ((this.spawnTileX > 250 && this.spawnTileX < st.w - 250)
1615:      if (this.ZoneCorrupt) return D(57);
1616:      if (this.ZoneCrimson) return D(465);
1617:      if (this.spawnTileY < this.world.groundLevel && this.spawnTileY > 50 && !N(3) && this.dayTime) {
1622:          if (N(5) && (t === T.GRASS || t === T.MOWED_GRASS)) return this.spawnNPC(x, num26 * TILE, 616, rng);
1625:          if (t === T.SAND) {
1627:            if (N(2) && !windyC && !this.world.weather.raining) {
1628:              return this.spawnNPC(x + rng.int(-16, 16), num26 * TILE - TILE, N(400) ? 613 : 612, rng);
1630:            return this.spawnNPC(x, num26 * TILE, 608, rng);
1633:          return this.spawnNPC(x, num26 * TILE, N(2) ? 362 : 364, rng);
1637:        if (t === T.SAND && this.spawnTileX > 380 && this.spawnTileX < st.w - 380) {
1638:          return this.spawnNPC(x, num26 * TILE, 607, rng);
1640:        if (N(400)) return D(592);
1641:        return D(55);
1644:      if (t === T.SAND && this.spawnTileX > 380 && this.spawnTileX < st.w - 380) return D(607);
1645:      if (N(400)) return D(592);
1646:      return D(55);
1663:        return this.spawnBound(105);
1665:      if (hardMode && N(20) && !this.waterTile && this.deeperThanRockLayer
1667:        return this.spawnBound(106);
1669:      if (this.downedBoss3 && N(20) && !this.waterTile && this.deeperThanRockLayer
1671:        return this.spawnBound(685);
1677:    if (this.spawnFriendlyCycle && this.ZoneGraveyard) {
1678:      if (!this.waterTile) return D(N(2) ? 610 : 606);
1689:    if (this.spawnFriendlyCycle && this.dayTime && !this.waterTile && this.world.weather.raining && gemTileOK
1692:      if (N(5)) return D(this.getGemSquirrelToSpawn(rng));
1693:      if (N(5)) return D(this.getGemBunnyToSpawn(rng));
1697:    if (this.spawnFriendlyCycle && this.dayTime && !this.waterTile && this.surfaceSpawn && !friendlyBlocked &&
1705:      if (t === T.GRASS || t === T.MOWED_GRASS || t === T.HALLOW_GRASS || t === T.HALLOW_MOWED_GRASS) {
1709:        if (!tooWindyFB && dryDay && N(Math.max(1, this.world.stinkBugChance))) return D(669);
1712:          return D(N(400) ? 444 : 356);
1715:      if (N(15)) {
1716:        if (t === T.SNOW || t === T.SNOW_BRICK) {
1718:          if (N(2)) return D(148);
1719:          return D(149);
1729:          return D(N(400) ? 605 : 604);
1733:        if (r < 0.2) return D(357);       // 蚯蚓
1734:        if (r < 0.45) return D(377);      // 蚱蜢
1735:        if (r < 0.65) return D(46);       // 兔子
1736:        if (r < 0.8) return D(299);       // 松鼠
1737:        if (r < 0.9) return D(300);       // 老鼠
1738:        return D(74);                     // 鸟
1746:    if (this.spawnFriendlyCycle && this.dayTime && !this.waterTile && !this.surfaceSpawn && gemTileOK && !friendlyBlocked
1748:      if (N(3)) {
1749:        if (N(5)) return D(this.getGemSquirrelToSpawn(rng));
1750:      } else if (N(5)) {
1751:        return D(this.getGemBunnyToSpawn(rng));
1756:    if (this.spawnFriendlyCycle) return null;
1762:    if (this.ZoneDungeon) {
1767:        if (wallA === 94 || wallA === 96 || wallA === 98 || wallB === 94 || wallB === 96 || wallB === 98) variant = 1;
1768:        if (wallA === 95 || wallA === 97 || wallA === 99 || wallB === 95 || wallB === 97 || wallB === 99) variant = 2;
1769:        if (N(7)) variant = rng.int(0, 3);
1771:        if (!this.downedBoss3) return D(68);
1774:        if (this.downedBoss3 && N(5) && !this.waterTile
1777:          return D(123);
1780:        if (hardDungeon && N(30)) return D(287);
1781:        if (hardDungeon && variant === 0 && N(15)) return D(293);
1782:        if (hardDungeon && variant === 1 && N(15)) return D(291);
1783:        if (hardDungeon && variant === 2 && N(15)) return D(292);
1785:        if (hardDungeon && !any(290) && variant === 0 && N(35)) return D(290);
1787:        if (hardDungeon && (variant === 1 || variant === 2) && N(30)) return D(289);
1790:        if (hardDungeon && N(20)) {
1792:          if (!any(necro)) return D(necro);
1796:        if (hardDungeon && !N(3)) {
1797:          return D(269 + (variant === 0 ? 4 : 0) + (variant === 2 ? 8 : 0) + rng.int(0, 3));
1799:        if (N(35)) return D(71);   // 地牢史莱姆
1802:        if (variant === 1 && N(3) && !this.nearSpikeBall()) return D(70);
1805:        if (variant === 2 && N(5)) return D(72);
1806:        if (variant === 0 && N(7)) return D(34);   // 诅咒头骨
1807:        if (N(7)) return D(32);    // 黑魔法师
1812:        if (av === 0) return D(294);
1813:        if (av === 1) return D(295);
1814:        if (av === 2) return D(296);
1815:        if (N(4)) return D(-14);   // Big Boned
1816:        if (N(5)) return D(-13);   // Short Bones
1817:        return D(31);              // 愤怒骨怪
1821:    if (this.ZoneMeteor) return D(23);
1824:    if (this.moonEvent && this.spawnTileY <= this.world.groundLevel && !this.dayTime) {
1828:      if (pick !== 0) return D(pick);
1834:    if (this.surfaceSpawn && this.dayTime && this.world.clock.eclipse) {
1839:      if (downedPlant && N(80) && !any(477)) return D(477);    // 飞蛾魔 Mothron（唯一）
1840:      if (N(50) && !any(251)) return D(251);                   // 独眼怪 Eyezor（唯一）
1841:      if (downedPlant && N(5) && !any(466)) return D(466);     // 精神病人 Psycho（唯一）
1842:      if (downedPlant && N(20) && !any(463)) return D(463);    // 钉头 Nailhead（唯一）
1843:      if (downedPlant && N(20) && cnt467 < 2) return D(467);   // 致命球 Deadly Sphere（≤2）
1844:      if (N(15)) return D(159);                                // 吸血鬼 Vampire
1845:      if (flag14 && N(13)) return D(253);                      // 死神 Reaper（需三机械全杀）
1846:      if (N(8)) return D(469);                                 // 被附身者 The Possessed
1847:      if (downedPlant && N(7)) return D(468);                  // 蝇博士 Dr. Man Fly
1848:      if (downedPlant && N(5)) return D(460);                  // 屠夫 Butcher
1849:      if (N(4)) return D(162);                                 // 科学怪人 Frankenstein
1850:      if (N(3)) return D(461);                                 // 深海怪形 Creature from the Deep
1851:      if (N(2)) return D(462);                                 // 弗里茨 Fritz
1852:      return D(166);                                           // 沼泽怪 Swamp Thing（兜底）
1855:    if (t === T.MUSHROOM_GRASS) {
1857:      if (hardMode && this.waterTile) return D(256);
1860:      if (this.spawnTileY <= this.world.groundLevel && !N(3)) {
1862:        if ((!hardMode && N(6)) || N(12)) return D(360);
1863:        if (N(3)) {
1865:          if (N(4)) {
1866:            return this.spawnNPC(x, y, hardMode && !N(3) ? 260 : 259, rng, this.spawnTileX, this.spawnTileY);
1868:          return D(N(2) ? 257 : 258);   // 异腹真菌蟹 257 / 蘑菇瓢虫 258
1871:        return D(N(2) ? 254 : 255);
1876:      if (hardMode && this.spawnTileY >= this.world.groundLevel && !N(3)) {
1878:        if (N(5)) return D(374);
1880:        if (N(8)) return D(360);
1881:        if (N(4)) {
1882:          return this.spawnNPC(x, y, hardMode && !N(3) ? 260 : 259, rng, this.spawnTileX, this.spawnTileY);
1884:        return D(N(2) ? 257 : 258);
1893:    if (this.ZoneCorrupt && N(65) && !this.noWorms && this.canSpawnDevourer()) {
1894:      if (hardMode && !N(4)) return D(98);
1895:      return D(7);
1902:    if (hardMode && this.spawnTileY > this.world.groundLevel && N(75)) {
1903:      if (N(2) && this.ZoneCorrupt && !any(473)) return D(473);
1904:      if (N(2) && this.ZoneCrimson && !any(474)) return D(474);
1905:      if (N(2) && this.ZoneHallow && !any(475)) return D(475);
1906:      if (N(2) && this.ZoneJungle && !any(476)) return D(476);   // 原版还要求 tenthAnniversaryWorld
1907:      if (this.ZoneSnow) return D(629);
1908:      return D(85);
1911:    if (hardMode && wall === 2 && N(20)) return D(85);
1913:    if (hardMode && this.surfaceSpawn && !this.dayTime
1914:      && (N(20) || (N(5) && this.world.clock.moonPhase === 4))) return D(82);
1916:    if (t === T.JUNGLE_GRASS && N(500) && !this.dayTime) return D(52);
1918:    if (t === T.JUNGLE_GRASS && this.spawnTileY > this.world.groundLevel && N(60)) return D(219);
1927:    if (critGates && this.spawnTileY < st.h - 210 && N(8)) return D(N(400) ? 448 : 357);
1928:    if (critGates && this.spawnTileY < st.h - 210 && N(13)) return D(N(400) ? 447 : 300);
1929:    if (neutralCave && this.spawnTileY > this.world.groundLevel
1931:      && !this.ZoneSnow && !this.ZoneCrimson && !this.ZoneCorrupt && !this.ZoneHallow && N(13)) return D(359);
1936:    if (this.surfaceSpawn && this.ZoneJungle && !this.ZoneCrimson && !this.ZoneCorrupt && N(7)) {
1937:      if (this.dayTime && this.world.clock.hourFloat < 16.5 && !N(3)) {
1938:        return D([671, 672, 673, 674, 675][rng.int(0, 4)]);
1944:    if (t === T.HIVE && N(2)) {
1945:      if (hardMode && !N(4)) {
1946:        if (N(10)) return D(-21);
1947:        if (N(10)) return D(-20);
1948:        if (N(10)) return D(-19);
1949:        if (N(10)) return D(-18);
1950:        return D(176);
1957:    if (t === T.JUNGLE_GRASS && hardMode && !N(3)) {
1958:      if (this.surfaceSpawn && !this.dayTime && N(3)) return D(152);
1959:      if (this.surfaceSpawn && this.dayTime && !N(4)) return D(177);
1960:      if (this.spawnTileY > this.world.groundLevel && N(100)) return D(205);
1961:      if (this.spawnTileY > this.world.groundLevel && N(5)) return D(236);
1962:      if (this.spawnTileY > this.world.groundLevel && !N(4)) {
1963:        if (N(10)) return D(-21);
1964:        if (N(10)) return D(-20);
1965:        if (N(10)) return D(-19);
1966:        if (N(10)) return D(-18);
1967:        return D(176);
1969:      if (N(3)) return this.spawnNPC(x, y, 175, rng, this.spawnTileX, this.spawnTileY);
1970:      return D(153);
1974:    if ((t === T.LIHZAHRD_BRICK || t === T.WOODEN_SPIKE) && this.zoneLihzardTemple()) {
1975:      return D(N(3) ? 226 : 198);
1978:    if (wall === 86 && !N(8)) return this.spawnHornet(x, y, rng);
1980:    if (t === T.JUNGLE_GRASS) {
1982:      if (this.spawnTileY > midY) {
1984:        if (N(4)) return D(204);
1985:        if (N(4)) return this.spawnNPC(x, y, 43, rng, this.spawnTileX, this.spawnTileY);
1989:      if (N(4)) return D(51);
1990:      if (N(8)) return this.spawnNPC(x, y, 56, rng, this.spawnTileX, this.spawnTileY);
1997:    if (this.sandstormHappening && this.zoneSandstorm && TILE_SAND.has(t)
2003:        if (N(2)) return D(546);      // 怒滚虫 546
2004:        if (N(2)) return D(61);       // 秃鹫
2005:        return D(69);                 // 蚁狮
2008:      if (hardMode && N(20) && !any(541)) return D(541);
2011:      if (hardMode && !this.noWorms && N(3) && this.countNpc(510) < 4) {
2012:        return this.spawnNPC(x, (this.spawnTileY + 10) * TILE, 510, rng);
2016:      if (hardMode && !this.noWorms && N(2)) {
2017:        if (t === T.EBONSAND) return D(543);
2018:        if (t === T.CRIMSAND) return D(544);
2019:        if (t === T.PEARLSAND) return D(545);
2020:        return D(542);
2023:      if (hardMode && t === T.SAND && N(3)) return D(78);
2024:      if (hardMode && t === T.EBONSAND && N(3)) return D(79);
2025:      if (hardMode && t === T.CRIMSAND && N(3)) return D(630);
2026:      if (hardMode && t === T.PEARLSAND && N(3)) return D(80);
2028:      if (N(2)) return D(546);
2029:      if (N(2)) return D(580);
2030:      return D(581);
2034:    if (hardMode && t === T.SAND && N(3)) return D(78);       // 木乃伊（黄沙 1/3）
2035:    if (hardMode && t === T.EBONSAND && N(2)) return D(79);   // 黑暗木乃伊（黑檀沙 1/2）
2036:    if (hardMode && t === T.CRIMSAND && N(2)) return D(630);  // 血腥木乃伊（猩红沙 1/2；json 缺 630 → null，登记台账）
2037:    if (hardMode && t === T.PEARLSAND && N(2)) return D(80);  // 光明木乃伊（珍珠沙 1/2）
2051:    if (hardMode && this.underGround && !this.waterTile && hallowFloor) {
2053:      if (downedPlant && !this.dayTime && this.world.clock.hourFloat >= 19.5
2054:        && this.surfaceSpawn && N(10) && !any(661)) return D(661);
2055:      if (this.world.weather.raining && !any(244) && N(10)) return D(244);
2056:      if (!this.dayTime && N(2)) return D(122);
2058:      if (N(10) || (this.zoneWaterCandle && N(10))) return D(86);
2059:      return D(75);
2063:      return D(84);
2071:    if (crimsonFloor) {
2082:      if (hardMode && flag15 && N(40) && !this.noWorms) return D(179);
2083:      if (hardMode && flag15 && N(5) && !this.noWorms) return D(182);
2084:      if (hardMode && flag15 && N(2)) return D(268);
2085:      if (hardMode && N(3)) {
2086:        if (N(3)) return D(-24);
2087:        if (N(3)) return D(-25);
2088:        return D(183);
2090:      if (hardMode && (N(2) || this.spawnTileY > this.world.groundLevel)) return D(174);
2091:      if ((wall > 0 && !N(4)) || N(8)) return D(239);
2092:      if (N(2)) return D(181);
2093:      if (N(3)) return D(-22);
2094:      if (N(3)) return D(-23);
2095:      return D(173);
2104:    if (corruptFloor) {
2107:      if (hardMode && ugRock && N(40) && !this.noWorms) return D(83);
2108:      if (hardMode && ugRock && N(3)) {
2109:        return this.spawnNPC(x, y, 101, rng, this.spawnTileX, this.spawnTileY); // 攀爬者(锚点格)
2111:      if (hardMode && N(3)) return D(N(3) ? 121 : 81);     // 史莱姆法师/腐化史莱姆
2112:      if (hardMode && (N(2) || ugRock)) return D(94);      // 腐化史莱姆
2113:      if (N(3)) return D(-11);   // 小噬魂怪
2114:      if (N(3)) return D(-12);   // 大噬魂怪
2115:      return D(6);               // 默认 Eater of Souls
2120:    if (this.surfaceSpawn) {
2129:      if (this.ZoneGraveyard && !this.waterTile && (t === T.GRASS || t === T.MOWED_GRASS) && N(10)) {
2130:        return D(N(2) ? 610 : 606);
2134:      if (this.ZoneSnow && hardMode && raining && !any(243) && N(20)) return D(243);
2136:      if (!this.ZoneSnow && hardMode && raining && this.countNpc(250) < 2 && N(10)) return D(250);
2141:      if (flag17 && hardMode && this.world.flags['downed_245']
2143:        return D(399);
2148:      if (this.dayTime && !this.ZoneGraveyard) {
2158:          return D(50);
2165:          && this.spawningSandstoneCheck(this.spawnTileX, this.spawnTileY)) return D(69);
2166:        if (t === T.SAND && !this.waterTile) return D(61);
2171:          return D(73);
2174:        if (raining && N(4)) return D(224);
2176:        if (!this.waterTile && raining && N(2)) return D(225);
2185:          if (!N(3)) return D(594);
2188:            || t === T.SNOW || t === T.ICE) && !N(10)) return D(628);
2191:        if (!this.waterTile) return D(this.getBasicSlimeToSpawn(true, t, rng));
2205:        return D(t === T.HALLOW_GRASS ? 358 : 355);
2208:      if (this.ZoneGraveyard && N(12)) return D(301);
2210:      if (this.ZoneGraveyard && N(30)) return D(316);
2212:      if (this.ZoneGraveyard && hardMode && N(10)) return D(304);
2214:      if (N(6) || (moonPhase === 4 && N(2))) {
2216:        if (hardMode && N(3)) return D(133);
2218:        if (N(2)) return D(N(4) ? -43 : 2);
2224:        if (N(3)) this.spawnNPC(x, y, [-38, -39, -40, -41, -42][zv], rng);
2225:        return D([190, 191, 192, 193, 194][zv]);
2228:      if (hardMode && N(50) && clock.bloodMoon && !any(109)) return D(109);
2232:      if ((clock.bloodMoon || this.ZoneGraveyard) && N(300)) return D(53);
2233:      if ((clock.bloodMoon || this.ZoneGraveyard) && N(300)) return D(536);
2235:      if (!this.dayTime && moonPhase === 0 && hardMode && !N(3)) return D(104);
2237:      if (!this.dayTime && hardMode && N(3)) return D(140);
2239:      if (clock.bloodMoon && rng.int(0, 5) < 2) return D(N(2) ? 490 : 489);
2245:      if (iceTile) {
2246:        if (!this.ZoneGraveyard && hardMode && N(4)) return D(169);
2247:        if (!this.ZoneGraveyard && hardMode && N(3)) return D(155);
2248:        if (expert && N(2)) return D(431);
2249:        return D(161);
2253:        if (!N(3)) return D(223);
2254:        return D(N(2) ? -55 : -54);
2258:      if (this.ZoneGraveyard && N(200)) return D(691);
2261:      if (this.ZoneGraveyard && N(20)) return D(632);
2266:      if (N(this.torchZombieChance)) return D(expert && N(2) ? 591 : 590);
2273:        return D(armed);
2282:      if (N(3)) zid = rng.next() < 0.5 ? zrow[1] : zrow[2];
2283:      return D(zid);
2286:    if (this.underGround) {
2289:        if (hardMode) return D(N(3) ? 10 : 95);
2290:        return D(10);
2293:      if (hardMode && N(3)) return D(140);
2294:      if (hardMode && N(2)) return D(141);
2296:      if (t === T.SNOW || t === T.ICE || this.ZoneSnow) return D(147);
2297:      return D(this.getBasicSlimeToSpawn(false, t, rng));
2302:    if (this.spawnTileY > st.h - 190) {
2306:      if (hardMode && !this.world.flags['savedTaxCollector'] && N(20) && !any(534)) return D(534);
2310:      if (N(8)) {
2311:        if (!N(3)) return D(this.dayTime ? 653 : 654);
2312:        return D(655);
2315:      if (N(40) && !any(39)) return D(39);
2317:      if (N(14)) return D(24);
2318:      if (N(7)) {
2320:        if (N(10)) return D(66);
2321:        if (hardMode && mechAny && !N(5)) return D(156);
2322:        return D(62);
2325:      if (N(3)) return D(59);
2327:      if (hardMode && mechAny && !N(5)) return D(151);
2328:      return D(60);
2333:    if (this.checkToSpawnRockGolem(rng)) return D(631);
2340:    if (N(60)) {
2341:      if (this.ZoneSnow) return D(218);
2342:      return D(217);
2346:      && hardMode && !this.noWorms && N(8)) return D(120);
2348:    if (iceAll && !this.noWorms && hardMode) {
2349:      if (this.ZoneCorrupt && N(30)) return D(170);
2350:      if (this.ZoneHallow && N(30)) return D(171);
2351:      if (this.ZoneCrimson && N(30)) return D(180);
2354:    if (hardMode && this.ZoneSnow && N(10)) return D(154);
2357:      if (hardMode) return D(95);
2358:      if (this.ZoneSnow) return D(185);
2359:      return D(10);
2362:    if (this.ZoneSnow && N(20)) return D(185);
2365:      if (this.ZoneSnow || t === T.ICE || t === T.SNOW) return D(184);
2366:      if (N(3)) return D(-6);
2367:      return D(16);
2371:      if (this.ZoneJungle) return D(-10);
2372:      if (this.ZoneSnow || t === T.ICE || t === T.SNOW) return D(184);
2373:      return D(-6);
2375:    if (N(2)) {
2379:      if (N(35) && !this.waterTile && !any(453)) return D(453);
2381:      if (N(80)) return D(195);
2385:      if (hardMode && deepCave && N(200)) return D(172);
2387:      if (deepCave && N(200)) return D(45);
2390:      if (this.nearMarble && !N(4)) {
2391:        if (!N(6) && !any(480) && hardMode) return D(480);
2392:        return D(481);
2394:      if (this.nearGranite && !N(5)) {
2395:        if (!N(6) && !any(483)) return D(483);
2396:        return D(482);
2401:      if (hardMode && !N(10)) {
2402:        if (N(2)) {
2403:          if (this.ZoneSnow) return D(197);
2404:          if (deepCave && N(5)) return D(-15);
2405:          return D(77);
2407:        return D(this.ZoneSnow ? 206 : 110);
2410:      if (!this.noWorms && this.ZoneGraveyard && N(30)) return D(316);
2412:      if (N(20)) return D(44);
2414:      if (iceCave) return D(N(15) ? 185 : 167);
2416:      if (this.ZoneSnow) return D(185);
2418:      if (N(3)) return D(cavernMonsterType[rng.int(0, 1)][rng.int(0, 2)]);
2420:      if (this.ZoneGlowshroom && (t === T.MUSHROOM_GRASS || t === T.MUSHROOM_BLOCK)) return D(635);
2425:      if (!N(3)) return D(sm);
2427:      return D(rng.next() < 0.5 ? small[0] : small[1]);
2431:    if (hardMode && this.ZoneHallow && N(2)) return D(138);
2433:    if (this.ZoneJungle) return D(51);
2436:    if (this.ZoneGlowshroom && (t === T.MUSHROOM_GRASS || t === T.MUSHROOM_BLOCK)) return D(634);
2438:    if (hardMode && this.ZoneHallow) return D(137);
2440:    if (hardMode && !N(6)) {
2441:      if (N(3) && iceCave) return D(150);
2442:      return D(93);
2445:    if (iceCave) return D(hardMode ? 169 : 150);
2446:    return D(49);  // Cave Bat

```


---

## 🤖 Assistant · 2026-08-13T05:41:43.772Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have current line numbers (as of this grep). The file is being actively edited, so I'll note that. The structure is unchanged from my read except the spider nest branch (stylist 354 + golfer via spawnBound added).

Now let me compile the final deliverable. I'll be thorough but organized.

Let me note key mappings to correct the user's id guesses:
- "wraiths 77/78" → 77 = Armored Skeleton, 78 = Mummy, Wraith = 82
- "werewolf 145" → 145 = Snow Balla (Frost Legion), Werewolf = 104
- "corruptors 98/99/100" → 98 = World Feeder head (only head spawned), 99/100 = body/tail never spawned
- "hallowed enemies 104+" → hallow set is 75/84/86/120/122/137/138/244, and 661
- "闪电虫" = 358 Lightning Bug
- "armoured skeleton 77?" → yes, 77 = Armored Skeleton, hardMode gated

Hardmode-only enemies we spawn and their gates — let me build the full list with gates:

Wraith 82 → hardMode ✓ (line 1913-1914)
Werewolf 104 → hardMode ✓ (2235)
Wolf 155 → hardMode ✓ (2247)
Ice Elemental 169 → hardMode ✓ (2246, 2445)
Possessed Armor 140 → hardMode ✓ (2237, 2293)
Toxic Sludge 141 → hardMode ✓ (2294)
Wandering Eye 133 → hardMode ✓ (2216)
Clown 109 → hardMode && bloodMoon ✓ (2228)
Armored Skeleton 77 / Heavy Skeleton -15 → hardMode ✓ (2401-2405)
Skeleton mage variants 206/197, 110 → hardMode ✓ (2401-2407)
Mummy 78 / Dark Mummy 79 / Light Mummy 80 / Blood Mummy 630 → hardMode ✓ (2023-2026, 2034-2037). NOTE: 630 missing from JSON → silently dropped.
World Feeder 98 → hardMode ✓ (1894). Segments 99/100 never spawned.
Corruptor? — vanilla Corruptor is NPCID 93? No — 93 = Giant Bat. Hmm. Corruptor... In vanilla, "Corruptor" is NPCID 93? No. Let me think: the corruption hardmode flyer is "Corruptor" — hmm, actually the corruption's hardmode enemy is "Corruptor"? No wait. In Terraria, the Corruption hardmode enemies: World Feeder, Corruptor (spits vile spit), Slimer, Corrupt Slime, Cursed Hammer, Clinger, Dark Mummy. Corruptor = NPCID 93? No, Giant Bat is 93. Hmm.

Actually Corruptor is NPCID 94! Let me check: 94 = "Corruptor"? Hmm, our code line 2112 spawns 94 with comment "腐化史莱姆" (Corrupt Slime). Hmm. Actually I recall:
- 81 = Corrupt Slime? or Slimer?
- 94 = Corruptor? 

Let me check the JSON for 94, 121, 94, 81, 84.

Let me quickly query those.

Actually the user said "corruptors 98/99/100" — 98 = World Feeder, 99/100 = World Feeder body/tail. In vanilla, Corruptor is a different id. Let me just query the JSON for 81, 94, 121 to be accurate.

Also I should double check 661 name = Prismatic Lacewing (a critter that summons Empress of Light) — our code gates it with downedPlant && night && surfaceSpawn && hardMode. In vanilla L3946 661 is the Prismatic Lacewing which spawns at night 7:30pm-midnight on surface hallow after Plantera. ✓ Parity.

Let me query a few more names.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:41:45.717Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json'))\nfor i in [81,94,121,84,75,86,120,122,244,137,138,268,174,179,182,183,181,239,163,164,269,270,281,289,290,291,292,293,85,530,528,529,531,533,541,176,152,153,175,177,205,236,102,103,157,241,242,256,374,120,510]:\n    e=d.get(str(i)); print(i, (e or {}).get('name'))\n\"",
 "description": "Get names for corruption crimson hallow ids"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:41:59.014Z

**📎 ToolResult**

```
81 Corrupt Slime
94 Corruptor
121 Slimer
84 Enchanted Sword
75 Pixie
86 Unicorn
120 Chaos Elemental
122 Gastropod
244 Rainbow Slime
137 Illuminant Bat
138 Illuminant Slime
268 Ichor Sticker
174 Herpling
179 Crimson Axe
182 Floaty Gross
183 Crimslime
181 Face Monster
239 NPC_239
163 NPC_163
164 NPC_164
269 Rusty Armored Bones
270 Rusty Armored Bones
281 Ragged Caster
289 Giant Cursed Skull
290 Paladin
291 Skeleton Sniper
292 Tactical Skeleton
293 Skeleton Commando
85 Mimic
530 NPC_530
528 Lamia
529 Lamia
531 Sand Poacher
533 Desert Spirit
541 Sand Elemental
176 Moss Hornet
152 Giant Flying Fox
153 Giant Tortoise
175 Angry Trapper
177 Derpling
205 Moth
236 NPC_236
102 Angler Fish
103 Green Jellyfish
157 Arapaima
241 Blood Feeder
242 Blood Jelly
256 Fungo Fish
374 Truffle Worm
120 Chaos Elemental
510 Dune Splicer

```


---

## 🤖 Assistant · 2026-08-13T05:42:26.215Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have accurate names. Note:
- 94 = Corruptor ✓ (hardMode gated at 2112)
- 121 = Slimer (hardMode gated at 2111)
- 81 = Corrupt Slime (hardMode gated at 2111)
- 84 = Enchanted Sword (hardMode gated at 2063) — our comment "神圣噬魂怪" is wrong name but the gate is right
- 290 = Paladin (our comment says 骷髅神枪手/skeleton sniper — wrong name; 290 is Paladin). hardDungeon gated ✓
- 291 = Skeleton Sniper, 292 = Tactical Skeleton, 293 = Skeleton Commando — our comments mix these up. hardDungeon gated ✓
- 289 = Giant Cursed Skull (comment says 骷髅突击队长 — wrong). hardDungeon gated ✓
- 269/270 = Rusty Armored Bones; ragged caster family 281-286 = Ragged Caster ✓ (comment 破布施法者族 ✓)
- 287 = Bone Lee ✓ (comment said 技师 — wrong)
- 179 Crimson Axe ✓, 182 Floaty Gross ✓, 268 Ichor Sticker ✓ (comment 弱金史莱姆 wrong), 183 Crimslime ✓, 174 Herpling ✓ (comment 跳跳兽 close), 181 Face Monster ✓ (comment 脸怪 ✓), 173 Crimera ✓
- 239 = NPC_239 = Blood Crawler probably
- 163/164 unnamed in JSON but they're Black Widow / Wall Creeper

OK. I now have everything I need. The comment names in code are sometimes wrong, but that's not the ask. I'll report ids with authoritative names.

One last check: the user asked about "downed_398 (moon lord)" gates in the spawner — none used in VanillaSpawner. Only LunarEvent.ts uses it (shield). Confirmed by grep.

And in ScaleStats — no moon lord gate. Only downedPlantBoss.

Also the (B) question: "whether ANY hardmode-progression multiplier exists (post-WoF / post-mech / post-plantera boosts)":
- Post-WoF (hardMode): only used as a CONDITION for entering ScaleStats_ForExpertHardmode (line 308: `if (s.difficulty >= EXPERT && ctx.hardMode)`) — i.e., hardmode alone confers NO stat change in classic; it only enables the expert+hardmode floor. No classic-mode hardmode stat boost (vanilla parity: vanilla also has no classic hardmode multiplier except via ExpertHardmode... wait, in vanilla ScaleStats_ForExpertHardmode requires `Main.expertMode && Main.hardMode`? Let me recall vanilla NPC.cs:18087: `if (npc.difficulty >= 2 && Main.hardMode) ScaleStats_ForExpertHardmode`. Yes vanilla is expert-only too. OK parity.
- Post-mech: NO multiplier in scaling. Mech flags only affect: underworld Red Devil/Lava Bat swap (156/151), eclipse Reaper (253), eclipse trigger, spawn-rate? no. OldOnesArmy gating, plantera bulb.
- Post-plantera: downedPlantBoss → ScaleStats_ForExpertHardmode threshold 80→100 (line 539) — the ONLY progression multiplier in stat scaling. Plus spawn pools (dungeon hardDungeon, eclipse 477/466/463/467/468/460, hallow 661).
- Post-moonlord: nothing in scaling; spawner none.

Rate modifiers (C):
- getSpawnRate (644): hardMode rate×0.9/max+1 (665-668) — the ONLY hardmode rate effect.
- sandstorm uses hardMode ? ×0.4 : ×0.9 / ×1.5 : ×1.2 (line ~723-725 — need current line numbers; from my read it was 723-725, and since edits were after line 1418, the getSpawnRate line numbers are unchanged ✓)
- No mech/plantera/moonlord rate modifiers.
- moonEvent/invaders override to rate 20 / max 11.
- Also the slimeRainSpawns expert ×0.85 (line 371).

(D) setPlayerFlags call and flags flow: Game.ts:8914-8916. And setWeather 8918-8922, scopeNum3 8924-8931, getSpawnRate call 8952-8958, spawn call 8965. Also townNPCs 8947-8951, activeIds/moonCounts 8871-8891, lunar 8898-8911, nearby slots 8935-8939, remotePlayers 8942-8944.

Flags flow into spawner: hardMode (via spawn() reading world.flags.hardMode at 2607, and getSpawnRate reading w.flags.hardMode directly at 665), downedBoss3 (setPlayerFlags param 2 = downedSkeletron || downed_35), downed_245 (golem), downed_262 (plantera), downed_125/126/127/134 (mechs), downedGoblins, downedEyeOfCthulhu/downed_4, downedMartians, savedGoblin/savedWizard/savedStylist/savedGolfer/savedTaxCollector, unlockedSlimeOldSpawn, unlockedSlimeYellowSpawn, shadowOrbSmashed, downedGolemBoss. NOT passed: downed_398 (moon lord), downed_113 (WoF, implicit via hardMode), downed_222 (queen bee), etc.

Important note: `this.hardMode` is refreshed in spawn() (line 2607) but `spawnAnNPC` uses `this.hardMode`; `getSpawnRate` reads `w.flags.hardMode` directly — fine.

Now, the gaps I should flag (branches lacking hardMode gates where vanilla would have one):
1. Eclipse branch (1834-1852): no hardMode gate. Protected only because eclipse triggers are hardMode-gated (Game.ts:3225 natural, 4967 solar tablet). HOLE: F6 debug `debugTriggerEvent('eclipse')` (Game.ts:11221-11225) sets eclipse with no hardMode check → pre-hardmode world gets vampires/frankenstein/swamp things. Vanilla: eclipse only in hardmode. Flag this.
2. Lightning Bug 358 (2205): no hardMode gate — implicit via hallow grass tile (which only exists post-WoF unless imported/worldgen). Vanilla also gates only by tile, so parity, but worth noting as implicit.
3. Hallowed grass day critters 1697/1717-1729 include HALLOW_GRASS in the tile sets for surface critter spawning (line ~1705: stinkbug/butterfly/ladybug/firefly on hallow grass) — these are critters, fine.
4. Moon event branch (1824): no hardMode gate — moon events are summonable items that require hardmode to obtain in vanilla; our Game only triggers via moonEvent.kind != 0. Fine/implicit.
5. Lunar pillar branch (1285): no gate — implicitly post-Cultist via lunarEvent.active.
6. Statue mimic 690 (1561-1564): gate = downedBoss3 && ZoneGraveyard — matches vanilla (no hardmode requirement). Not a gap.
7. Meteor head 23 (1821): no hardMode gate. Vanilla 1.4: I believe there IS a hardmode restriction in vanilla... Let me think hard about this. In Terraria 1.4, changelog for 1.4.0.1: "Meteor Heads now only spawn pre-Hardmode"? Hmm. Actually I recall the opposite: the wiki says "Meteor Heads spawn at meteor sites. In Hardmode, they will no longer spawn" — no wait.

Let me check the vanilla source reference. Vanilla NPC.cs around :2704 (per our file's comment "L2704：else if (ZoneMeteor)"). I recall the actual vanilla code:

```
else if (spawn.player.ZoneMeteor && (!Main.hardMode || spawn.player.ZoneUnderworldLayer)) ?
```

Hmm, I'm not sure. Actually! I do remember: in 1.4, Meteor Heads spawn in the Underworld layer of meteor... no.

Let me search: Terraria wiki "Meteor Head": "Meteor Heads no longer spawn in Hardmode worlds"? I genuinely recall a 1.4 change: "Meteor Heads now stop spawning in Hardmode". Hmm, but there's also the famous "meteor head farm" that works in hardmode for farming... Actually the famous farm: "Meteor Head farming" was nerfed in 1.2? 

Given uncertainty, I should flag it as "unverified — worth checking against NPC.cs:2704" rather than asserting. Actually, I can be smarter: our file claims to be a 1:1 port with a documented-parity-gaps ledger. The ledger line 20 mentioned Devourer. Let me grep the ledger for meteor.

Let me do a quick grep for "陨石" in the gaps doc.

Also check "110" etc. Let me just grep the doc quickly for a few terms: 陨石 (meteor), 日食 (eclipse), 闪电 (lightning), 月总 (moonlord).
````

</details>


---

## 🤖 Assistant · 2026-08-13T05:42:26.924Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"陨石\\|日食\\|闪电虫\\|358\\|eclipse\\|月总\\|398\" ~/Project/GLM/SandboxWorld/game/docs/spawn-parity-gaps.md | head -20",
 "description": "Check gaps doc for meteor eclipse entries"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:42:26.955Z

**📎 ToolResult**

```
22:| 速率 else-if 链(高5) | :504-559 | 旧只移植地牢一支;补沙尘暴 hard?×0.4:0.9/×1.5:1.2、地下沙漠 ×0.2/×3、丛林城镇阶梯(0/1/2/≥3 → 0.4/0.55/0.7/0.85 与 1.5/1.4/1.3/1.2)、腐化猩红 ×0.65/×1.3、陨石 ×0.4/×1.1、神庙独立 if ×0.8/×1.2(墙 87)、神圣深层独立 if ×0.65/×1.3 | ✅ 2026-08-13 |
34:| 蘑菇地表/洞穴支(中) | :3540-3610 | 旧实现外层门写反(N(3) 应为 !N(3),2/3 通过写成 1/3)且内层只剩 254/257/259 三支;现 1:1 三支:hard 水支 256(:3540)、地表支 360(肉前 1/6\|\|困难 1/12)/260/259(锚点)/257/258/254/255(:3544)、洞穴支 374 松露虫(1/5)/360(1/8)/260/259/257/258(:3581) | ✅ 2026-08-13 |
36:| spawnFriendly 外层门四门(中) | :709 | 旧实现只挂 !血月/!invaders/!邪恶三门;补 南瓜霜月(!bloodMoon&&!pumpkinMoon&&!snowMoon)\|\|白天、日食白天关、ZoneMeteor 三门(:709 原文全列:flag(腐化\|\|猩红)+ZoneCrimson+ZoneMeteor+ZoneOldOneArmy) | ✅ 2026-08-13 |

```


---

## 🤖 Assistant · 2026-08-13T05:42:34.853Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The gaps doc doesn't mention meteor-head-hardmode. Our port spawns 23 unconditionally in ZoneMeteor. Vanilla NPC.cs:2704 — I'll flag as "worth verifying" but note that our port claims 1:1 for the branch chain, and the comment at line 1820 (current) says nothing about a hardmode restriction. Since the whole file is a meticulous 1:1 port with a parity ledger, and the ledger doesn't list a meteor-hardmode gap, I'll present it as: no hardMode gate on meteor heads (23); whether vanilla 1.4.5.6 has one at NPC.cs:2704 should be verified against the decompiled source — I'll note the evidence is that our port author didn't find one.

Actually, I can reason from another angle: in vanilla, the meteor spawn branch is at NPC.cs SpawnAnNPC around line 2704 per our comment. I'm fairly confident the vanilla condition is just `else if (ZoneMeteor)` — meteor heads DO spawn in hardmode worlds (that's why meteor-head soul farms... hmm, actually no, in 1.4 meteor head farms were fixed because in hardmode meteor heads... ). 

OK — I'll flag it neutrally as "verify".

One more thing: I noticed the "Moss Zombie 691" and "Statue 690" etc. Fine.

Also worth flagging: countNpc() degrades to 0/1 (documented gap) affecting 513 uniqueness and 250 nimbus cap.

And: `townNoWorms` dead latch (getSpawnRate latches it, never consumed) — this IS a gap: town no-worm suppression never applied. Let me double-check by grepping for `noWorms` assignment in spawn().

Let me verify once more that townNoWorms is truly never read (only lines 256, 809, 818, 822, 826, 842, 849, 856 = declaration, reset, and 6 assignments). No reads. Confirmed dead.

Wait — but maybe the intended composition is `this.noWorms ||= this.townNoWorms` somewhere in spawn(). Let me grep the spawn() body for noWorms.

Line 2610 (old numbering): `this.noWorms = ... WALL_HOUSE...`. Let me grep current.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:42:35.292Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"noWorms\" ~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts | head -40",
 "description": "List all noWorms usages"
}
```


---

## 👤 User(sidechain) · 2026-08-13T05:42:35.324Z

**📎 ToolResult**

```
119: *  SetSpawnFlags L321：玩家所站格带房屋墙 → noWorms（房屋内不出蠕虫） */
252:  private noWorms = false;         // 原版 wallHouse（房屋内不出蠕虫）
255:   *  直接覆写 noWorms）;本仓 getSpawnRate/spawn 拆两次调用 → 先闩锁,spawn() 合成 */
816:        // 城镇 noWorms 掷骰（:717/:734/:750）在友好掷骰**之前**（原版同序）
833:        // 城镇 noWorms 无条件置位（:767/:792/:814——地表侧城镇 ≥1 恒不出蠕虫）
1342:      // L1316：飞龙 87——hard && 场上无 87 && !noWorms（房屋内不出蠕虫门，此前缺失）&& 1/10
1343:      if (hardMode && !any(87) && !this.noWorms && N(10)) return D(87);
1448:      if (hardMode && N(Math.floor(50 * num11)) && !this.noWorms
1451:      if (N(Math.floor(50 * num11)) && !this.noWorms
1554:    //  downedBoss3 && ZoneGraveyard && !noWorms && RollBadLuckExtreme(25)==0 && 场上无 690
1561:    if (this.downedBoss3 && this.ZoneGraveyard && !this.noWorms
1888:    //  门：ZoneCorrupt && Next(maxValue)==0 && !noWorms && CanSpawnDevourer(spawnTileX)。
1893:    if (this.ZoneCorrupt && N(65) && !this.noWorms && this.canSpawnDevourer()) {
2009:      // :3880 沙丘穿刺者 510：hard && !noWorms && 1/3 && CountNPCS(510)<4,
2011:      if (hardMode && !this.noWorms && N(3) && this.countNpc(510) < 4) {
2014:      // :3884 沙鲨族：hard && !noWorms && 1/2 → 按落脚沙换色（门内 tile 恒在四沙集,
2016:      if (hardMode && !this.noWorms && N(2)) {
2062:    if (!this.noWorms && hardMode && N(50) && !this.waterTile && this.deeperThanRockLayer && hallowFloor) {
2075:      //  ①hard && flag15 && 1/40 && !noWorms → 179 猩红斧（墙挂怪）
2076:      //  ②hard && flag15 && 1/5 && !noWorms → 182 浮空恶臭
2082:      if (hardMode && flag15 && N(40) && !this.noWorms) return D(179);
2083:      if (hardMode && flag15 && N(5) && !this.noWorms) return D(182);
2106:      //  World Feeder 头是 98，在上方 Devourer 段）。门带 !noWorms（L4039，此前漏）
2107:      if (hardMode && ugRock && N(40) && !this.noWorms) return D(83);
2287:      if (!this.noWorms && N(50) && !this.ZoneSnow) {
2346:      && hardMode && !this.noWorms && N(8)) return D(120);
2348:    if (iceAll && !this.noWorms && hardMode) {
2356:    if (!this.noWorms && N(100) && !this.ZoneHallow) {
2409:      // L4961：幽灵 Ghost 316——!noWorms && (万圣节 || 墓地) && 1/30（洞穴主池内）
2410:      if (!this.noWorms && this.ZoneGraveyard && N(30)) return D(316);
2619:    // SetSpawnFlags L321：noWorms = 玩家所站格带房屋墙（房屋内不出蠕虫）
2620:    this.noWorms = this.world.store.inBounds(this.pX, this.pY)

```


---

## 🤖 Assistant · 2026-08-13T05:42:39.680Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: `townNoWorms` is latched in getSpawnRate (lines 816-862 region) but NEVER read — the "spawn() 合成" (compose in spawn()) promised in the line 255 comment is missing. `spawn()` at line 2620 sets `noWorms` only from the house-wall check. So town-based worm suppression is dead code. That's a genuine finding (relevant to C: rate/count modifiers).

Now I'm ready to write the deliverable. Let me organize:

A. Spawn branch tree + gates per branch + hardmode-only enemy list
B. Scaling inputs + progression multiplier presence/absence
C. Rate modifiers
D. setPlayerFlags + flag flow

I'll note the file is being concurrently edited (line numbers as of this pass; structure confirmed).

Let me write it up compactly but completely. Given "very thorough", I'll be detailed but use tight tables/lists.
```

</details>


---

## 🤖 Assistant · 2026-08-13T05:44:01.140Z · glm-x-preview-260804

````
Inventory complete. Note: `VanillaSpawner.ts` was being edited concurrently during this pass (a stylist/golfer block was inserted around line 1418 mid-analysis), so line numbers below reflect the file as of my final verification sweep. Structure confirmed stable otherwise.

---

# A. Spawn branch tree — `~/Project/GLM/SandboxWorld/game/src/world/spawn/VanillaSpawner.ts`

Single file in `game/src/world/spawn/` (no sibling files). It imports from `core/constants`, `core/rng`, `data/tiles`, `data/vanillaNpcs`, `data/vanilla-npcnetid.json`, `entities/Enemy`, `world/MoonEvent`, `world/TileStore`, `stats/ScaleStats` (`mainExpertMode`), `stats/Luck`.

**Entry chain**: `spawn()` L2603 → `findSpawnTile()` L892 → `setFlagsForChosenTile()` L441 → `spawnAnNPC()` L1264 (`this.hardMode` set from `world.flags.hardMode` at L2607; `expert` from `mainExpertMode(world)` at L1266).

## A.1 `spawnAnNPC` branch tree (order = priority; first hit returns)

| Lines | Branch / selector | NPC ids | Progression gates |
|---|---|---|---|
| 1285–1327 | Lunar pillar zone (`this.lunar`, first in chain) | Nebula 420/421/423/424; Vortex 425/426/427/429; Stardust 402/405/407/409/411; Solar 412/415/416/417/418/419/518 | none — implicit: `lunar != null` only when `lunarEvent.active` + within 4000px of a tower (post-Cultist) |
| 1331–1349 | `skyMob` | 388 (Martian drone), **399 Martian probe**, **87 Wyvern**, 686 (bound purple slime), 48 Harpy | 399: `hardMode && downed_245 (Golem) && !downedMartians ? 1/8 : 1/30`; 87: `hardMode && 1/10 && !noWorms` |
| 1351–1416 | `invaders` (invasion, exclusive) | Goblin 26/27/28/29/111/**471**; Frost Legion **145**/143/144; Pirate 212–216/252/**491**; Martian 381/382/383/385/386/388/389/390/395/520 | 471: `hardMode && 1/30`; 491 Dutchman: progress>50% && 1/20 && clear sky. **145 is Snow Balla (Frost Legion), NOT Werewolf** |
| 1420–1430 | Spider nest (wall 62 / `spawnSpider`) | **354 Stylist**, **163 Black Widow**, 164 Wall Creeper | 354: wall62 + 1/8 + `!savedStylist` + unique; 163: `hardMode` (9/10) |
| 1435–1474 | Underground desert | 589 Golfer, **510 Dune Splicer**, 513 Tomb Crawler, **524–527/528–533** (Ghoul/Lamia/Basilisk/etc.), 69/537/508/509/580/581 | 510: `hardMode`; 513: *no* hard gate (correct — pre-hard enemy); ghoul pool: `hardMode` |
| 1479–1482 | Hardmode biome water | **157 Arapaima**, **242 Blood Jelly / 241 Blood Feeder** | both `hardMode` |
| 1494–1551 | Ocean (`isOcean && waterTile`) | 376 Angler, 602 Seagull, 65 Shark, **692 Orca**, 615/625/626/627/688 critters, 220/221/67/64 | 692: `hardMode`; others ungated (pre-hard valid) |
| 1561–1564 | Statue Mimic | **690 Statue (Mimic)** | `downedBoss3 && ZoneGraveyard && !noWorms && badLuck(25) && unique` — **no hardMode gate** (matches vanilla NPC.cs:1478) |
| 1569–1604 | Water pool A/B (`!spawnFriendlyCycle`) | 617/613/612 critters, **102 Angler Fish**, 58 Piranha, **103 Green Jellyfish**, 63 Blue Jellyfish | 102, 103: `hardMode` (2/3) |
| 1613–1646 | Water pool 3rd (no friendly gate) | 57/465 goldfish, 608/616/613/612/362/364, 607/592/55 | none (all pre-hard) |
| 1663–1671 | Bound trio | 105 / **106** / 685 | 105: `downedGoblins`; 106: `hardMode`; 685: `downedBoss3 && !unlockedSlimeOldSpawn` |
| 1677–1751 | Friendly-cycle critters (graveyard / rain gem / surface / cave gem) | 606/610, gem squirrels 639–645, gem bunnies 646–652, 669/356/444/148/149/604/605/357/377/46/299/300/74 | `spawnFriendlyCycle` (rolled in `getSpawnRate`) + day + surface/cave tile |
| 1756 | Friendly guard | — | `spawnFriendlyCycle` → return null (never falls into enemy chain) |
| 1762–1817 | **Dungeon** (`ZoneDungeon`) | 68 Dungeon Guardian, 123 Mechanic, then `hardDungeon` pool **287 Bone Lee, 289/290/291/292/293, 281–286 Ragged Caster, 269–280**; pre-hard pool 71/70/72/34/32/294/295/296/-13/-14/31 | `!downedBoss3` → 68; 123: `downedBoss3`; **`hardDungeon = hardMode && downed_262 (Plantera)`** L1773 |
| 1821 | Meteor (`ZoneMeteor`) | **23 Meteor Head** | **none** — see gap note below |
| 1824–1829 | Moon event (Frost/Pumpkin) | full wave tables (`pickFrostMoonSpawn` L1030, `pickPumpkinMoonSpawn` L1160) | wave number only; no hardMode (implicit: items are hardmode-only) |
| 1834–1852 | **Eclipse** | **477 Mothron, 251 Eyezor, 466 Psycho, 463 Nailhead, 467 Deadly Sphere, 159 Vampire, 253 Reaper, 469 Possessed, 468 Dr. Man Fly, 460 Butcher, 162 Frankenstein, 461, 462, 166** | `downedPlant` (downed_262) for 477/466/463/467/468/460; `flag14 = downed_134 && (downed_125‖downed_126) && downed_127` for 253; **no hardMode gate** — see gap note below |
| 1855–1885 | Mushroom grass (tile 70) | **256 Fungo Fish**, 360 Glowing Snail, 260/259 Fungibulb, 257/258, 254/255, **374 Truffle Worm** | 256: `hardMode && waterTile`; cave branch 374/260: `hardMode` |
| 1893–1895 | Devourer (Corrupt) | **98 World Feeder**, 7 EoW head | 98: `hardMode && 3/4`. **Body/tail 99/100 never spawned** (single-NPC model, aiStyle 5 swarmer) |
| 1902–1908 | Rare cave | **473 Corrupt / 474 Crimson / 475 Hallowed / 476 Jungle Mimic**, **629 Ice Mimic**, **85 Mimic** | whole block: `hardMode && depth && 1/75` |
| 1911 | wall===2 | 85 Mimic | `hardMode && 1/20` |
| 1913–1914 | Surface night | **82 Wraith** | `hardMode && (1/20 ‖ full-moon 1/5)` |
| 1916 / 1918 | Jungle grass | 52, 219 | none (pre-hard) |
| 1936–1990 | Jungle (critters / hive / hard grass / temple / hive wall / grass) | 671–675, frog; **176 Moss Hornet + -18..-21**; **152/177/205/236/175/153**; **226/198** temple; hornets; 204/43/51/56 | hive moss hornets: `hardMode`; hard grass pool: `hardMode`; temple: `zoneLihzardTemple` (wall 87) only — **no hardMode gate, matches vanilla** |
| 1997–2030 | Sandstorm pool | 546/61/69 (pre-hard, `!downedBoss1 && !hardMode`), **541 Sand Elemental, 510, 542–545 Sand Sharks, 78/79/630/80 Mummies**, 546/580/581 | 541/510/sharks/mummies: `hardMode` |
| 2034–2037 | Desert surface mummies | **78/79/630/80** | `hardMode`. **630 (Blood Mummy) missing from `vanilla-npcs.json` → `fromVanilla` null → silently dropped** (stale comment at L1903 claiming 473–476/629 also missing — they DO exist) |
| 2051–2063 | **Hallow tiles** | **661 Prismatic Lacewing, 244 Rainbow Slime, 122 Gastropod, 86 Unicorn**, 75 Pixie; **84 Enchanted Sword** | block gate: `hardMode && underGround && !waterTile && hallowFloor`; 661 additionally `downed_262 && night≥19.5 && surfaceSpawn && unique`; 84: `!noWorms && hardMode && 1/50 && deeperThanRockLayer` |
| 2071–2095 | Crimson (tile gate) | **179 Crimson Axe, 182 Floaty Gross, 268 Ichor Sticker, -24/-25/183 Crimslime, 174 Herpling**, 239, 181 Face Monster, -22/-23, 173 Crimera | 179/182: `hardMode && flag15 && !noWorms`; 268: `hardMode && flag15`; -24/-25/183: `hardMode`; 174: `hardMode` |
| 2104–2115 | Corruption (tile gate) | **83 Cursed Hammer, 101 Clinger, 121 Slimer / 81 Corrupt Slime, 94 Corruptor**, -11/-12, 6 Eater of Souls | 83: `hardMode && ugRock && !noWorms`; 101: `hardMode && ugRock`; 121/81: `hardMode`; 94: `hardMode` |
| 2120–2283 | **Surface** (`surfaceSpawn`) | see below | see below |
| 2286–2297 | Underground (`underGround`) | 95 Digger/10 Giant Worm, **140 Possessed Armor, 141 Toxic Sludge**, 147, basic slime | 140/141: `hardMode` |
| 2302–2328 | **Underworld** (y > h−190) | **534 Tortured Soul**, 653/654/655, 39 Bone Serpent, 24, 66 Voodoo Demon, **156 Red Devil**, 62, 59, **151 Lava Bat**, 60 | 534: `hardMode && !savedTaxCollector`; **156/151: `hardMode && mechAny`** where `mechAny = downed_125‖126‖127‖134` (L2304) |
| 2333 | Rock Golem | 631 | `checkToSpawnRockGolem` requires `hardMode` (L2549) |
| 2340–2446 | Cave general pool | 218/217, **120 Chaos Elemental, 170/171/180 Pigron, 154 Ice Tortoise**, 95/185/10, 184/-6/16/-10, 453, 195, **172 Rune Wizard**, 45, **480 Medusa**, 481, 483/482, **77 Armored Skeleton / -15 / 206 / 197 / 110**, 316, 44, 185/167, cavern salamanders, 635, 21/201/202/203+variants, **138 Illuminant Slime, 137 Illuminant Bat, 93 Giant Bat / 150**, 169/150, 49 | 120/170/171/180/154/172/480/77-family/138/137/93/150: `hardMode` |

### Surface branch detail (2120–2283)
- Graveyard maggot/mouse 2129–2130 (`ZoneGraveyard`, no hard gate — correct)
- **243 Ice Golem** 2134: `ZoneSnow && hardMode && raining && unique && 1/20`
- **250 Angry Nimbus** 2136: `!ZoneSnow && hardMode && raining && countNpc(250)<2 && 1/10`
- **399 Martian probe** 2141: `flag17 && hardMode && downed_245 && (!downedMartians ? 1/100 : 1/400) && unique`
- Day pool 2148–2191: King Slime 50 (`!any(50) && >w/3 from spawn && grass && 1/300`), 69 antlion, 61 vulture, 73 Goblin Scout (`>w/3 && (1/15 ‖ (!downedGoblins && shadowOrbSmashed && 1/7))`), 224, 225, 594, 628, basic slime. **No hardMode gates (all pre-hard valid)**
- Night pool 2193–2283:
  - **358 Lightning Bug** 2200–2205: `!graveyard && !windy && !rain && grass-family tile && 1/fireFlyChance && surface` — **no hardMode gate** (implicit via hallow grass; see below)
  - 301 Raven / 316 Ghost 2208/2210: `ZoneGraveyard` only
  - **304 Hoppin' Jack** 2212: `ZoneGraveyard && hardMode`
  - **133 Wandering Eye** 2216: `hardMode && 1/3`
  - Demon eyes / zombie family 190–194 (+netIds) 2218–2225: none
  - **109 Clown** 2228: `hardMode && 1/50 && bloodMoon && unique`
  - Groom 53 / Bride 536 2232–2233: `bloodMoon ‖ graveyard`
  - **104 Werewolf** 2235: `!day && moonPhase===0 && hardMode && 2/3`
  - **140 Possessed Armor** 2237: `!day && hardMode && 1/3`
  - Blood Zombie 489 / Drippler 490 2239: `bloodMoon` only (pre-hard valid)
  - ice tile 2245–2249: **169 Ice Elemental / 155 Wolf** `!graveyard && hardMode`; 431 Armed Zombie `expert`; 161 Frozen Zombie fallback
  - 223 Raincoat Zombie 2252; **691 Moss Zombie** 2258 `graveyard && 1/200`; **632 Maggot Zombie** 2261 `graveyard && 1/20`; 590/591 Torch Zombie 2266 (`expert` for 591); 430–436 Armed Zombies 2268 (`expert`); final zombie table 2277–2283

### Hardmode-only enemies we spawn and their gates (corrections to your id guesses)
Your prompt's ids need remapping: **Wraith = 82** (not 77/78; 77 = Armored Skeleton, 78 = Mummy). **Werewolf = 104** (145 = Snow Balla). **"Corruptor 98/99/100"** = World Feeder head 98 + body/tail 99/100 (Corruptor itself = **94**).

| Enemy | id | Gate | Verdict |
|---|---|---|---|
| Armored Skeleton | 77 (Heavy −15) | `hardMode` L2401–2405 | ✅ |
| Mummy / Dark / Light / Blood | 78/79/630/80 | `hardMode` L2023–26, 2034–37 | ✅ (630 drops silently — no JSON entry) |
| Wraith | 82 | `hardMode` L1913 | ✅ |
| Werewolf | 104 | `hardMode` + new moon L2235 | ✅ |
| Wolf | 155 | `hardMode` L2247 | ✅ |
| Corruptor / Slimer / Corrupt Slime | 94/121/81 | `hardMode` L2111–2112 | ✅ |
| Cursed Hammer / Clinger | 83/101 | `hardMode && ugRock` L2107–2108 | ✅ |
| Enchanted Sword | 84 | `hardMode && deeperThanRock && !noWorms` L2062 | ✅ |
| Hallow set (Pixie/Unicorn/Gastropod/Rainbow Slime/Chaos Elemental/Illuminant Bat+Slime) | 75/86/122/244/120/137/138 | `hardMode` L2051, 2431, 2438, 2346 | ✅ |
| Prismatic Lacewing | 661 | `hardMode && downed_262 && night && surface` L2053 | ✅ |
| Possessed Armor / Toxic Sludge | 140/141 | `hardMode` L2237, 2294 | ✅ |
| Wandering Eye / Clown | 133/109 | `hardMode` (+bloodMoon for 109) L2216/2228 | ✅ |
| Black Widow | 163 | `hardMode` L1428 | ✅ |
| Ice Golem / Angry Nimbus / Ice Tortoise / Ice Elemental | 243/250/154/169 | `hardMode` L2134/2136/2354/2246 | ✅ |
| Rock Golem / Rune Wizard / Medusa / Mimics | 631/172/480/85/629/473–476 | `hardMode` L2549/2385/2391/1902–1908 | ✅ |
| Post-Plantera dungeon set | 287/289–293/281–286/269–280 | `hardMode && downed_262` L1773 | ✅ |
| Eclipse set | 159/162/166/251/469/461/462 + 460/463/466/467/468/477/253 | eclipse + (downed_262 or 3-mech) — **no hardMode** L1834 | ⚠️ see gaps |
| Red Devil / Lava Bat | 156/151 | `hardMode && mechAny` L2321/2327 | ✅ |
| Dune Splicer / Sand Elemental / Sand Sharks / Ghouls etc. | 510/541/542–545/524–533 | `hardMode` | ✅ |
| Lightning Bug | 358 | **none** (hallow-grass tile implies hardmode) L2205 | ⚠️ implicit |

### Branches lacking a hardMode gate — flagged
1. **Eclipse branch L1834** — the only real hole. `clock.eclipse` is set in exactly 3 places: natural dawn roll (Game.ts:3225, gated `hardMode && mechAny && 1/20`), Solar Tablet use (Game.ts:4967, gated `hardMode`), and **F6 debug `debugTriggerEvent('eclipse')` (Game.ts:11221–11225) which sets it with no hardMode check** — so a pre-hardmode world forced into eclipse will spawn Vampires/Frankensteins/Swamp Things/Eyezors. Vanilla: eclipse is hardmode-only. The 1/15 Vampire, 1/4 Frankenstein, 1/3 Creature-from-the-Deep, 1/2 Fritz, 1/8 Possessed and the unconditional Swamp-Thing fallback carry no internal gate.
2. **Lightning Bug 358 (L2205)** — no `hardMode`; protected only because hallow grass (tile 109/492) can't exist pre-WoF except in imported worlds. Matches vanilla's tile-only gate, but it's implicit.
3. **Meteor Head 23 (L1821)** — `ZoneMeteor` only, no hard gate. Whether vanilla 1.4.5.6 restricts meteor heads at `NPC.cs:2704` should be verified against the decompile; the parity ledger (`game/docs/spawn-parity-gaps.md`) registers no such gap, suggesting the porter found none.
4. **Temple 226/198 (L1974)** — `zoneLihzardTemple` (wall 87) only, no hardMode. Matches vanilla (progression enforced by locked door, not the spawner).
5. **Moon event / Lunar pillar / Frost Legion 143–145 / Pirate 212–216/252/491** — no hard gates; implicitly progression-locked by their triggers (all are summon-item or event-state driven). Parity-consistent.
6. **Blood Moon content** — 489/490/53/536 and Clown 109 are bloodMoon-gated (Clown additionally hardMode); blood moon itself is legitimately pre-hardmode in vanilla. ✅

---

# B. Enemy stat scaling on spawn

## `game/src/stats/ScaleStats.ts`

**`scaleStats(s, ctx = scaleStatsWorld(), activePlayersCount?, strengthOverride?)` L297–317**

Inputs actually consumed (`ScaleStatsWorld` L248–261, bound via `bindScaleStatsWorld` from Game.afterWorldLoad **Game.ts:1636**):

| Input | Source | Effect |
|---|---|---|
| `difficulty` | `mainDifficulty(world)` L124–132: `world.difficulty` 0/1/2 → Classic 1 / Expert 2 / Master 3; **`+1` if `seedFlags.getGoodWorld`**. Journey (3) deliberately NOT modeled as 0.5× | multiplies life/value/damage/knockback via 6 curves L98–113 |
| `hardMode` | `world.flags.hardMode` (L286) | only used as the **condition** for entering `scaleStatsForExpertHardmode` (L308) — confers **no** stat change on its own in Classic |
| `getGoodWorld` | `world.seedFlags.getGoodWorld` (L287) | boosts the difficulty axis +1, plus per-type boss-life/damage/defense interactions L346–362, L528–532 |
| `downedPlantBoss` | `world.flags['downed_262']` (L288) | **the only progression multiplier**: raises the ExpertHardmode floor 80 → 100 (L539) |
| `anyNpc(type)` | `this.entities.enemies.some(en => !en.dead && en.vanillaId === type)` (Game.ts:1636–1637) | getGoodWorld EoW/EoC/WoF co-presence tweaks |
| `activePlayerCount` | **hardcoded 1** (L290) | ByPlayerCount balance ≡ 1 → identity |

The `activePlayersCount` / `strengthOverride` params exist on the signature but **no caller passes them** — `Enemy.fromVanilla` calls `scaleStats(ss)` with one argument (Enemy.ts:500).

Entry gate (L306): `NEEDS_EXPERT_SCALING.has(type) ‖ (lifeMax > 5 && damage ≠ 0 && !friendly && !townNPC)` — **bosses not exempt**; then:
- L308 `if (difficulty >= EXPERT && hardMode) scaleStatsForExpertHardmode(...)` — **Expert + hardmode only**
- L309 `scaleStatsByDifficulty` — curves + per-type Tweaks (L336–518, ~60 type families, getGoodWorld hooks, moon-event invasion groups L494–508)
- L310–312 `if (difficulty >= EXPERT) scaleStatsByPlayerCount` — identity in single player
- L314 `lifeMax` floor 6 (except `PROJECTILE_NPC`)

**`scaleStatsForExpertHardmode` L525–549** (your `ScaleStats_ForExpertHardmode` equivalent):
- Exemptions: `DONT_DO_HARDSMODE_SCALING` set L152; getGoodWorld co-presence suppressions L528–532; **`boss ‖ lifeMax >= 1000` L533**.
- Computes `num = damage + defense + trunc(lifeMax/4)`; floor `num2 = 80`, **`+20` if `downedPlantBoss`**; if `num < num2`, multiplies `damage ×num3×0.9`, `defense ×num3`, `lifeMax ×num3×1.1`, `value ×num3×0.8`.

### Progression multipliers — present vs absent
| Progression point | Stat-scaling effect | Spawn-pool effect |
|---|---|---|
| Post-WoF (`hardMode`) | **None directly** — only *enables* the ExpertHardmode floor for Expert+ worlds. No Classic-mode hardmode stat boost (vanilla parity) | ~60 hardmode branches in A.1 + rate ×0.9/max +1 |
| Post-mech (`downed_125/126/127/134`) | **Absent** | Underworld 156/151 swap (L2321/2327), Eclipse Reaper 253 (L1845), event rolls |
| Post-Plantera (`downed_262`) | **Present**: ExpertHardmode floor 80→100 (ScaleStats L539) | Dungeon `hardDungeon` pool, Eclipse 477/466/463/467/468/460, Hallow 661 |
| Post-Golem (`downed_245`) | Absent | Martian probe 399 (L1337/2141) |
| Post-Moon Lord (`downed_398`) | **Absent entirely** — referenced only in `world/LunarEvent.ts:78–80` (tower shield 100→50), never in spawner or scaling | none |

## `game/src/entities/Enemy.ts` — `fromVanilla` L476–522

- Builds `ScalingStats` from the JSON row (L494–499: `lifeMax/damage/value/defense/knockBackResist/boss/friendly/townNPC/scale`, `difficulty: 0`), calls `scaleStats(ss)` (L500).
- `e.difficulty = ss.difficulty` (L501; field declared L134–138) — consumed by AI-side `getAttackDamageForProjectiles` / `getKnockbackMultiplierScaledByDifficulty` (e.g. L1506, 4513, 4888–4893, 4941).
- `e.baseDamage = rawDamage` (L502) — **un-scaled** baseline for projectile spawn, so the difficulty multiply isn't applied twice (comment L139–143).
- Scaled `ss.lifeMax/ss.damage/ss.defense/ss.value` flow into `e.def` and `e.hp/maxHp` (L506–526); friendly/critter damage forced 0 (L490, 509, 521).
- Other `fromVanilla` callers in Enemy.ts (451, 464, 2884, 4036, 4875, 5172, 5255, 5866, 5880) all go through the same scaling path — no boss exemption anywhere.

---

# C. Spawn rate / count modifiers

All in `getSpawnRate` L644–875 (defaults: rate 600, max 5 — L660–661). Caller: **Game.ts:8952–8958**.

| Lines | Modifier | Gate |
|---|---|---|
| 652–654 | rate = 20, max = ⌊5×2.3⌋ = 11 | moon event active + player above ground |
| 657–659 | rate = 20, max = 11 | `invaders ‖ lunar` |
| **665–668** | **rate ×0.9, max +1** | **`world.flags.hardMode` — the ONLY hardmode rate effect** (read directly from `w.flags`, not the latched `this.hardMode`, to avoid a first-frame miss) |
| 670–672 | max ×2 | Underworld depth |
| 673–676 | rate ×0.4, max ×1.9 | below rock layer |
| 677–680 | rate ×0.5, max ×1.7 | underground layer |
| 681–685 | rate ×0.6, max ×1.3 | night |
| 686–689 | rate ×0.3, max ×1.8 | blood moon (night branch) |
| 690–694 | rate ×0.2, max ×1.9 | day + eclipse |
| 703–706 | max ×(1+cloudAlpha), rate ×(1−cloudAlpha+1)/2 | ZoneSnow + surface + rain |
| 720–749 | else-if chain: Dungeon ×0.3/×1.8; **Sandstorm hard?×0.4:×0.9 / ×1.5:×1.2 (L723–725 — second hardmode rate touchpoint)**; Underground Desert ×0.2/×3; Jungle town ladder ×0.4–0.85/×1.5–1.2; Corrupt/Crimson ×0.65/×1.3; Meteor ×0.4/×1.1 | zone flags + townNPCs count |
| 752–755 | ×0.8/×1.2 | Lihzahrd Temple (player wall 87) |
| 757–760 | ×0.65/×1.3 | ZoneHallow && below rock layer |
| 762–770 | rate ×0.6/0.7/0.8/0.9 by nearbySlots < 20/40/60/80% of max; extra ×0.7/0.9 deep-or-evil | nearby NPC slots |
| 772–775 / 777–780 / 782–785 | Calming ×1.65/×0.6; Sunflower ×1.2/×0.8; Battle ×0.5/×2 | buffs |
| 787–795 | Water candle ×0.75/×1.5 (sky ×0.5 more) else Peace candle ×1.3/×0.7 | candle context |
| 797–800 | clamp rate ≥ 60, max ≤ 15; Dungeon pre-Skeletron rate = 10 | `!downedBoss3` |
| 808–866 | `spawnFriendly` roll block (max ×0.5 underworld / ×0.6 surface on hit; rate ×1.25–×3 on miss; graveyard rate ×1.66–×3) | `!invaders && ((!bloodMoon && !moonEvent) ‖ day) && !(eclipse&&day) && !zoneEvil && !ZoneMeteor` |
| 870–873 | rate ×0.85, max ×1.15 | `rollOnlyBadLuckExtreme(luck, 50)` |

Also: `slimeRainSpawns` L365–397 (independent sky drop; expert ×0.85 at L371); `MOON_BOSS_CAP_SLOTS` L47; maxSpawns enforcement `nearby >= maxSpawns` + `Next(spawnRate)` at **Game.ts:8959–8961**; nearby slot sum computed at Game.ts:8935–8939.

**No mech / Plantera / Golem / Moon Lord modifier exists anywhere in the rate path.** hardMode appears in exactly two places (L665–668, L723–725).

### Dead latch found (C-adjacent)
`townNoWorms` (L256) is latched in `getSpawnRate` (L816–862) per vanilla `:717/:734/:750/:767/:792/:814`, and the field comment at L255 says "先闩锁, spawn() 合成" — but **it is never read**. `spawn()` sets `this.noWorms` only from the house-wall check (L2620). Net effect: the "no worms near a town" suppression is latched and discarded; worms (7/10/87/95/98/510/etc.) still spawn adjacent to towns.

---

# D. `setPlayerFlags` and flag flow into the spawner

**Definition**: VanillaSpawner.ts:327–347.
```ts
setPlayerFlags(zoneDungeon, downedSkeletron, invaders?, activeIds?,
               moonEvent?, lunar?, playerLifeMax?, playerLuck?)
```
Derived in-body: `ignoreSafeWalls = lunar != null` (L343), `moonBossCap = moonEvent && bossSlotSum >= MOON_BOSS_CAP_SLOTS` (L346).

**Call site**: **Game.ts:8914–8916** (`trySpawnEnemy`, once per frame before `getSpawnRate`):
```ts
this.vanillaSpawner.setPlayerFlags(!!this.scene?.zoneDungeon,
  !!(w.flags.downedSkeletron || w.flags['downed_35']),   // downedBoss3 dual-key
  invaders, activeIds, moonCtx, lunar, this.player.maxHp, this.player.luck);
```

Supporting context built just above / below:
- Game.ts:8871–8891 — `activeIds`, `moonCounts`, `moonBossSlotSum`; bound TownNPC reverse-registered into `activeIds` (8886–8891) so `!AnyNPCs(105/106/685/123/354/589)` gates work.
- Game.ts:8892–8894 — `moonCtx`.
- Game.ts:8898–8911 — `lunar` (tower zone within 4000px).
- Game.ts:8918–8922 — `setWeather(cloudAlpha, sandstorm.happening, zoneDesert && near-surface)`.
- Game.ts:8924–8931 — `scopeNum3` (sniper scope ring widening).
- Game.ts:8942–8944 — `VanillaSpawner.remotePlayers`.
- Game.ts:8947–8951 — `townNPCs` (count within 85×60 tiles).
- Game.ts:8952–8958 — `getSpawnRate(...)` call; 8965 — `spawn(p.cx, p.cy, rng, viewHalfW, viewHalfH)`.

**Flags the spawner reads directly from `world.flags`** (not via `setPlayerFlags`): `hardMode` (L665, L923, L926, L2607), `downed_245` (Golem, L1337/2141), `downed_262` (Plantera, L1773/1836/2053), `downed_125/126/127/134` (mechs, L1837, L2304), `downed_4 ‖ downedEyeOfCthulhu` (L1992), `downedGoblins` (L1663, L2160), `downedMartians` (L1339), `savedGoblin/savedWizard/savedStylist/savedGolfer/savedTaxCollector`, `unlockedSlimeOldSpawn` (L1670), `unlockedSlimeYellowSpawn` (L2495), `shadowOrbSmashed` (L2160).

**Flags never consumed by the spawner**: `downed_398` (Moon Lord), `downed_113` (WoF — implicitly covered by `hardMode`), `downed_50/222/35/113/245/262/370/439` except as listed.

**Flag producers**: generic `downed_${vanillaId}` write on any boss kill at **Game.ts:3035–3039**; `startHardmode()` (**HardmodePass.ts:230–235**, sets `flags.hardMode = true` + V-biome conversion) invoked from the WoF kill chain at **Game.ts:3046–3053**. `downedPlantBoss` projection into scaling at **Game.ts:1636 → ScaleStats.ts:288**, and into wiring at Game.ts:1711.

**Scaling-context binding**: `bindScaleStatsWorld(scaleStatsWorldOf(...))` at **Game.ts:1636–1637** (`afterWorldLoad`) — the object is captured by reference, so `hardMode`/`downed_262` flips are picked up live without rebinding (comment 1630–1635).
````
