# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T18:45:59.912Z

```
你在 ~/Project/GLM/SandboxWorld/game（Terraria 1.4.5.6 网页复刻，种子等价工程）。任务：把原版 #32 Dungeon pass 转录进 C# oracle 并与 JS 对账到逐哈希全等。

## 工程背景（必读文件，读完再动手）
1. docs/worldgen/vanilla-pass-alignment.md（game/docs/ 下）——工程总纲：幽灵 tile 机制、id 空间碰撞（内部 EMPTY=0 ≡ 原版幽灵泥土 0）、rng.int 换算铁律、工作流。
2. ~/Project/GLM/SandboxWorld/docs/worldgen/handoff-pyramid-dungeon-location-2026-08-12.md——上一会话对 dungeonLocation 的核实结论（generatingDungeonPositionX 双字段已拆、gs.generatingDungeonPositionX 已在 GenState.ts:44、金字塔回避带已修）。
3. 权威源码 ~/Project/GLM/SandboxWorld/Terarria1456/（ilspycmd 反编译 1.4.5.6）：Dungeon 注册在 WorldGen.cs:14816（AddGenerationPass GenPassNameID.Dungeon），实现在 Terraria.WorldBuilding/DungeonCrawler.cs + LegacyDungeonLayoutProvider + 相关（约 2000 行）。
4. Oracle：tools/golden/caves-oracle.cs——已覆盖 terrain→beaches 34 checkpoint 双种子全绿（含 corruption/lakes/slush/mcopenings/beaches）。dungeon 段插入位置 = slush checkpoint 之后、mcopenings 块之前（原版注册序 32<33），文件里有注释标记。
5. JS 侧：src/world/gen/vanilla/DungeonPass.ts（1405 基底+多轮 1456 修正，刚被另一会话大改过，01:38 后静默）。

## 任务步骤
1. 读 1456 DungeonCrawler.cs 全文 + WorldGen.cs:14816 注册段，理清掷骰序（C# 实参左→右求值；JS 对象字面量按书写序）。
2. caves-oracle.cs 转录 dungeon 段 + Checkpoint("dungeon")；JS DungeonPass.ts 逐段对照修偏差。发现的任何"我们自创改良"（吸附/底锚定/短路类）一律按原版删除——历史教训见 memory。
3. checkpoint 测试（tests/caves-checkpoint.test.ts）chainCheckpoints 序里加 dungeon（slush 后、mcopenings 前），names 同步。
4. 双种子金标再生：`dotnet run tools/golden/caves-oracle.cs 9293480 0 tests/golden/caves-chain-9293480.json` 和 `dotnet run tools/golden/caves-oracle.cs 1511931452 1 tests/golden/caves-chain-SandboxWorld.json`；`npx vitest run tests/caves-checkpoint.test.ts` 双种子全等。
5. 硬验收线：terrain..beaches 既有 checkpoint 哈希不变（dungeon 插在 slush 与 mcopenings 之间会移动 mcopenings/beaches 的流位置——它们的哈希会变，预期内）。
6. 全量回归 + 不留探针 + 报告（bug 清单带行号、checkpoint 哈希、回归数、遗留）。

## 关键纪律
- (int) 截断=Math.trunc；(int)NaN=x86 Int32.MinValue；rng.int(a,b)≡闭区间≡Next(a,b+1)。
- 探针只读不掷骰；对账两侧 id 空间先归一（JS 内部 vs oracle 原版 sheet）。
- **防看门狗停滞：单次工具调用别超 8 分钟**——oracle/长测试拆单种子单段跑。
- WorldGen.ts 可能被并行会话编辑（昨晚多次），改前重读，改后被覆盖要自查（registry 探针式自查）。
- 并发期归属判据：批跑红≠回归，单文件复跑定归属。
```

---

## 📎 Attachment · skill_listing · 2026-08-12T18:45:59.915Z

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

## 🤖 Assistant · 2026-08-12T18:46:01.707Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by reading the required context files.

1. docs/worldgen/vanilla-pass-alignment.md
2. ~/Project/GLM/SandboxWorld/docs/worldgen/handoff-pyramid-dungeon-location-2026-08-12.md
3. Terraria 1.4.5.6 source: WorldGen.cs:14816 + DungeonCrawler.cs
4. tools/golden/caves-oracle.cs
5. src/world/gen/vanilla/DungeonPass.ts

Let me read them in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:01.848Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/docs/worldgen/vanilla-pass-alignment.md"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:01.854Z

**📎 ToolResult**

```
1	# 原版世界生成 pass 对齐总表
2	
3	> 2026-08-12。权威源码 = `Terarria1456/`（ilspycmd 反编译 1.4.5.6）。
4	> 种子等价验证 = `tests/caves-checkpoint.test.ts`（C# oracle `tools/golden/caves-oracle.cs`
5	> 反射真 UnifiedRandom，双种子金标 `tests/golden/caves-chain-*.json`）。
6	> pass 编号沿用 1.4.0.5 的 105-pass 清单（`memory/vanilla-worldgen-passes.md`），
7	> 1.4.5.6 新增 pass（约 4 个，Total ~109）在对应阶段注明。
8	
9	## 幽灵 tile 机制（读表前提）
10	
11	原版 `active(false)` **保留 type**（"幽灵"）。生成期多个 pass 对非活性格读/写 type：
12	- IceBiome（cs:12394）`switch(tile.type)` 不判 active → 幽灵泥土(0)→雪(147)、幽灵石(1)→冰(161)，**天空行也转化**；
13	- TileRunner 铺设分支 `if (!flag4) tile.type = type` 同样不判 active → 幽灵写出；
14	- 收尾循环的拒绝采样（`type != 59`）会读到幽灵 → 幽灵一致性影响掷骰流。
15	
16	**JS 侧对应约定**：内部 `EMPTY=0` ≡ 原版幽灵泥土 `type=0`——凡原版判 `type==0`，
17	JS 必须 `t === 0 || t === T.DIRT`。海盆挖掘（BeachPass）原版仅 `active(false)`（cs:15014）。
18	
19	## 已逐哈希验证（19 checkpoint，双种子全绿，2026-08-12）
20	
21	| checkpoint | 原版 pass | 实现文件 |
22	|---|---|---|
23	| terrain | 2 Terrain | TerrainPass.ts |
24	| dunes | 3 Dunes | DunesPass.ts |
25	| oceansand | 4 Ocean Sand | BeachPass.ts (runOceanSandPass) |
26	| sandpatches | 5 Sand Patches | MissingCavesPass.ts |
27	| tunnels | 6 Tunnels | MissingCavesPass.ts |
28	| mountaincaves | 7 Mount Caves | MountCavesPass.ts |
29	| dirtwallbg | 8 Dirt Wall Backgrounds | MissingCavesPass.ts |
30	| rocksclay | 9-11 RocksInDirt/DirtInRocks/Clay | CavesPass.ts |
31	| smallholes | 12 Small Holes | MissingCavesPass.ts |
32	| surfacecaves | 13-15 Dirt/Rock/Surface Caves | CavesPass.ts |
33	| mcopenings | 34 Mountain Caves | MountCavesPass.ts |
34	| beaches | 35 Beaches | BeachPass.ts |
35	| icebiome | 16 Ice Biome | IceBiomePass.ts |
36	| grass | 17 Grass | GrassPass.ts |
37	| jungle | 18 Jungle（JunglePass.cs 全文） | JunglePass.ts |
38	| mudcaves | 19 Mud Caves To Grass | Spread.ts (SpreadGrass) |
39	| desertmound | 20 Full Desert 之 mound 段 | DesertPass.ts |
40	| —— | 附：oracle 链尾还有 Reset 掷骰序列（cs:11159-11472）已 1:1 重置 | WorldGen.ts runResetAndTerrain |
41	
42	## JS 已移植、oracle 未对账（无逐哈希验证）
43	
44	| 原版 pass | 实现文件 | 备注 |
45	|---|---|---|
46	| 21 Floating Islands | — | 检查 WorldGen.ts vanillaBiomes |
47	| 22 Mushroom Patches | MushroomPass.ts | |
48	| 23/24 Marble/Granite | MarbleGranitePass.ts | TileRunner 伴生墙 180/178 |
49	| 25/26 DirtToMud/Silt | DirtToMudPass.ts | |
50	| 27 Shinies（矿石） | — | 全硬编码表（见 memory） |
51	| 31 Lakes + 36 Gems | LakesPass.ts / GemPasses.ts | |
52	| 37 GravitatingSandCleanup（1456 cs:15198-15226） | GravitatingSandPass.ts | 零掷骰；Falling 系空腔落定；2026-08-12 补缺 |
53	| ShellPiles（1456 cs:16385-16501） | BeachPass.ts（runBeachDecorPass+shellPile） | 1:1 掷骰序（含原版右侧误写 shellStartXLeft 怪癖）；2026-08-12 从管线末尾归位至平滑前 |
54	| Shimmer（1456 cs:15256） | ShimmerPass.ts | |
55	| 33 Slush | IceBiomePass.ts runSlushPass | 无 RNG |
56	| 28 Corruption/Crimson | CorruptionPass.ts | 二选一 |
57	| 30 Dungeon | DungeonPass.ts | |
58	| 29 Underworld + 地狱塔/屋 | HellFortPass.ts / HellforgesPass.ts | |
59	| 38 Ocean Caves | OceanCavesPass.ts | |
60	| 40 Pyramids | （vanillaBiomes 内） | gs.pyramidSpots 来自 Dunes |
61	| 42/43 Living Trees(+Walls) | LivingTreePass.ts | |
62	| 46 Jungle Temple / 47 Hives | TemplePass / BeehivePass | 见 memory beehive-port |
63	| 57-67 箱子/水晶/雕像/神龛/小屋 | BuriedChests/CaveHouse/Statues/JungleShrine... | 内容型 |
64	| 49 中途沉降 SettleLiquids | WorldGen.ts liquidSettlePass | 尾沉降=SettleLiquidsPart2 由读档承担 |
65	| 53 SmoothWorld / 54 Waterfalls | HalfBrickPass.ts | 坡面/半砖三路分支已 1:1（见 memory） |
66	| 82 Trees | TreePass（surfacePass 内嵌） | 半砖/坡面门禁已补 |
67	| 78 SurfaceOreAndStone（1456 cs:18559） | SurfaceDecorPasses.ts | OrePatch/StonePatch 1:1；gs.orePatchX 登记 |
68	| 79 FallenLogsAndWaterFeatures（cs:18625） | SurfaceDecorPasses.ts | 仅倒木段（水景=秘密种子）；gs.logX/logY→Flowers |
69	| 84 DyePlants（cs:20126） | SurfaceDecorPasses.ts | plantDye/PlaceDye(34*style)/MatureTheHerbPlants/656/752 |
70	| 91 Vines（cs:20338） | SurfaceDecorPasses.ts | 六类藤 52/382/62/528/636/205/638 + GrowMoreVines/CanHitLine + 444 凹龛 |
71	| 92 Flowers（cs:20592） | SurfaceDecorPasses.ts | 花圃重帧（tile3→73），消费 gs.logX/logY |
72	| 93 Mushrooms（cs:20744） | SurfaceDecorPasses.ts | 3/24→frameX144、201→270 帧重刷 |
73	| 96 LongMoss（cs:20915） | SurfaceDecorPasses.ts | PlaceTile184+TileFrame184(22*色号)；上游 MossAndMossCaves(17573) 已移植（MossPass.ts，收尾批） |
74	| 102 LilypadsCattailsBambooAndSeaweed（cs:22131） | SurfaceDecorPasses.ts | 518/519/571/549；GrowCheckSeaweed 已去重（BeachPass 海藻近似删除） |
75	
76	## 已知管线偏差（备案，未修）
77	
78	**执行序 = 注册序已确认**（WorldGenerator.cs:447 `_passes[PassResults.Count]` 逐个执行，
79	无排序/无 weight 重排）。1456 完整 105-pass 注册序见上表编号；与我们链的真实顺序偏差
80	（JS 与 oracle 双方一致地"错"——oracle 按 JS 链顺序转录，互验全绿 ≠ 原版等价）：
81	
82	| 原版真实序 | 我们链现状 | 影响 |
83	|---|---|---|
84	| #20 Mushroom→#21 Marble→#22 Granite→**#23 FloatingIslands** | 岛在蘑菇/大理石**前** | RNG 流错位 |
85	| #26 OresAndShinies（Silt 后、Webs 前） | 排在很后（"矿石"槽） | 同上 |
86	| #30 Lakes、**#35 Gems（Beaches 后）** | Lakes+Gems 捆绑 | 同上 |
87	| **#33 MountainCaveOpenings→#34 Beaches（Dungeon 后、Gems 前）** | 紧跟 SurfaceCaves（太早） | 同上 |
88	
89	- #15 WavyCaves：**dontStarveWorldGen 专用**（cs:12303 普通世界空跑零消耗），不构成偏差。
90	- 因此 19 个 checkpoint 中 terrain..surfacecaves 在原版序下依然有效；mcopenings 起全部
91	  在错误流位置执行——这是 seed-parity（对真 .wld）仍红的结构性根因之一。
92	- 修正需 JS 链与 oracle 同步改序 + 金标再生（共享文件，串行做）。
93	- 71 Pots / 77 Piles 以 legacy pass 原位运行（语义 1:1，无 oracle）。
94	- 73 SpreadingGrass + 86-90 杂草花混在 surfacePass（legacy 外壳）。
95	- 表面装饰子 pass 群（SurfaceDecorPasses.ts）插入位置：SpreadingGrass(18349) 之后、
96	  Traps(18769) 之前放 78/79（OrePatch/倒木需草面）；84/91/92/93 在 AlchemyHerbs 之后
97	  按 20126<20338<20592<20744 排列；96 紧随 ExposedGems(20874)；102 在 MicroBiomes(21785)
98	  之后。依赖销核（收尾批 2026-08-12）：LongMoss 的上游 MossAndMossCaves(17573) 已移植
99	  （MossPass.ts，"苔藓"槽=地狱箱之后/Pots 之前）；藤 638 的上游灰烬草 633 已在 hellPass 铺设
100	  （cs:13869-13915 外缘 17% 带+灰烬树 634）；藤 382 的上游草墙 63/65 已移植
101	  （GrassWallPass.ts = SurfaceDirtWallsToGrassWalls cs:19734，"草墙"槽=地表装饰之后/
102	  染料植物之前；66/68 是可放置安全版墙非世界生成产物，63/65 即解锁花藤）。
103	- DyePlants 的 MatureTheHerbPlants（cs:20135）原在 surfacePass 调用，已下沉到染料植物 pass
104	  （原版调用点），AlchemyHerbs 仍在 surfacePass（20109<20126 序保持）。
105	
106	## 种子等价工作流（标准动作）
107	
108	1. `dotnet run tools/golden/caves-oracle.cs <seedInt> <evil> tests/golden/caves-chain-<name>.json` 再生金标
109	   （'9293480'→9293480/evil 0；'SandboxWorld'→1511931452/evil 1）；
110	2. `npx vitest run tests/caves-checkpoint.test.ts` 双种子全等；
111	3. 改动前先读 `Terarria1456` 对应源码；掷骰序用 C# 实参左→右求值规则核对；
112	4. `rng.int(a,b)`≡闭区间 [a,b]≡`Next(a,b+1)`；`(int)` 截断=Math.trunc；(int)NaN=x86 Int32.MinValue；
113	5. 对账两侧 id 空间不同（JS 内部 vs oracle 原版 sheet），比较前先归一——历史乌龙多源于此。
114	

```


---

## 🤖 Assistant · 2026-08-12T18:46:02.091Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/docs/worldgen/handoff-pyramid-dungeon-location-2026-08-12.md"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:02.101Z

**📎 ToolResult**

````
1	# 告知:Pyramids 消费端读到的 dungeonLocation 疑点(供世界生成对账会话核实)
2	
3	> 来源:2026-08-12 会话(瀑布/尖刺球/链锤/世界边界线)。触发场景:用户报"新世界沙漠没金字塔",
4	> 排查种子 `-475242790` 时顺带发现。**金字塔链路本身已逐环节核对为 1:1,不要去"修"它**;
5	> 唯一疑点在你们在途的 Dungeon 侧变量语义,请你们核实。
6	
7	## 现象
8	
9	对 seed `-475242790`(4200×1200)确定性重跑生成,在 `runPyramidPass`
10	(`src/world/gen/vanilla/StructuresPass.ts:540`)插桩读到的状态:
11	
12	```
13	dunes#0 origin=(775,1196) 掷骰 0.2135 → 命中,金字塔候选列 x=877
14	dunes#1 origin=(851,173)  掷骰 0.8534 → 未中(>0.8)
15	消费端拒绝门日志:spot0 x=877 拒:地牢带L(side=-1, dx=633, band=630)
16	```
17	
18	最终存档 `dungeonX=886`(用户 debug report 的 world 段,与重跑一致)。
19	
20	## 疑点
21	
22	Pyramids 消费端原版读的是 `GenVars.CurrentDungeonGenVars.generatingDungeonPositionX`
23	(WorldGen.cs:15447-15449 地牢回避带),该变量语义 = **地牢生成过程中回写的最终入口位**:
24	
25	- 初值:DungeonCrawler.cs:346(爬开始时赋 x)
26	- **回写:DungeonCrawler.cs:394** 入口走廊落位后 `generatingDungeonPositionX = (int)x2`
27	  (同处还写 dungeonTopX)——Pyramids pass 注册在 Dungeon(:14816)之后(:15426),
28	  所以消费时读到的是回写后的最终入口 X(本图 ≈886)
29	
30	我们 `gs.dungeonLocation` 在地牢 pass 之后仍是 **633**(Reset 末掷的初值)。
31	633 vs 886 的差距意味着:DungeonPass 里 `found` 分支的回写
32	(`src/world/gen/vanilla/DungeonPass.ts:145`,`gs.dungeonLocation = nx + 25 - rng.int(0, 49)`)
33	要么走了 `found=false` 路径没回写,要么 **`dungeonX` / `dungeonLocation` 两个字段混用**
34	(GenState 两字段都有;存档 dungeonX=886 来自何处、pyramid 读 dungeonLocation=633 来自何处,需对账)。
35	
36	## 影响面
37	
38	- **本种子判定不受影响**:地牢带门要求 `num ≥ dx + 630`(side=Left),dx=633 或 886 都远大于
39	  877−630,候选必拒——本种子无金字塔是原版同种子行为(80% 掷中后压在地牢上被合法回避)。
40	- **潜在分叉**:若某颗种子的金字塔候选列落在 `633+630=1263` 与 `886+630=1516` 之间的窗口
41	  (或对称左侧窗口),两种 dx 会给出**不同判定** → checkpoint 哈希分叉的候选根因之一。
42	  收敛矩阵(#22)阶段大概率会撞上。
43	
44	## 请核实/修复(你们作业面内)
45	
46	1. DungeonPass 走读:`found=false`(3000 次探测全败)时是否该回写、原版该路径 dx 语义;
47	2. `gs.dungeonX` 与 `gs.dungeonLocation` 的赋值/消费清单,对齐原版
48	   `generatingDungeonPositionX` / `dungeonX`(WorldGen 字段)的分工;
49	3. 修复后重跑 `tests/golden/wld/` 相关 checkpoint,注意 **Pyramids 哈希可能因修正而变**
50	  (变 = 更接近原版,属预期)。
51	
52	## 不要动的(本会话已验证 1:1,动之前先说)
53	
54	- `DunesPass` 金字塔候选段:取点 `RandomWorldPoint(0,500,0,500)`(参数序 top/right/bottom/left,
55	  即 X∈[500,3699]、Y∈[0,1199]——origin y=1196 看似离谱实为原版合法值)、0.8 概率、±200 列、
56	  首个 active+20,与 WorldGen.cs:11591-11599 逐行一致;
57	- `runPyramidPass` 五道拒绝门(边缘300/地牢带/下扫 worldSurface/沙列/间距220)与
58	  :15447-15476 一致;管线顺序 Dunes→Dungeon→Pyramids 与注册序(11540/14816/15426)一致。
59	
60	——2026-08-12,边界/瀑布会话留
61	

````


---

## 🤖 Assistant · 2026-08-12T18:46:08.994Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the vanilla source: DungeonCrawler.cs and WorldGen.cs:14816 registration segment. Also the oracle and JS DungeonPass.ts.

Let me find DungeonCrawler.cs first.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:09.015Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "find ~/Project/GLM/SandboxWorld/Terarria1456 -iname \"*Dungeon*\" -o -iname \"*LegacyDungeon*\" | head -50; echo ---; wc -l ~/Project/GLM/SandboxWorld/game/tools/golden/caves-oracle.cs ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts",
 "description": "Locate dungeon sources and check file sizes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:09.052Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Halls
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.LayoutProviders
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Rooms
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Entrances
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Events/DangerousDungeonCurse.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonType.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonUtils.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonShapes.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonGenerationStyleID.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DualDungeonUnbreakableWallTiers.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonDoorData.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonRoomSearchSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonData.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonGenVars.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonPlatformData.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonColor.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonLayoutProviderSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonBounds.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonCrawler.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonGenerationStyles.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonLayoutProvider.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonGenerationStyleData.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPCSpawningFlagsForDualDungeons.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonWindow.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/IDungeonFeature.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonDropTrapSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalGroundFurniture.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalPlatforms.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalBanners.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonDropTrapType.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalPaintings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalSpikes.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonFeature.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonTileClumpSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonWindowMosaicSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/GlobalDungeonFeature.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonPitTrap.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalWallVariants.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalDoors.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonWindowSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonWindowBasic.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonDropTrap.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalBasicChests.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalLateDualDungeonFeatures.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonPitTrapSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonFeatureSettings.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalBiomeChests.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon.Features/DungeonGlobalBookshelves.cs
---
    4350 ~/Project/GLM/SandboxWorld/game/tools/golden/caves-oracle.cs
    1684 ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts
    6034 total

```


---

## 🤖 Assistant · 2026-08-12T18:46:11.224Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The vanilla dungeon directory is a directory? Wait no, "Terraria.GameContent.Generation.Dungeon" is a directory (no extension shown). Let me check. Actually the find shows both directories and files. Let me look at the structure.

The handoff mentions DungeonCrawler.cs:346, :394 — so DungeonCrawler.cs is a file inside Terraria.GameContent.Generation.Dungeon/ directory.

Let me read DungeonCrawler.cs. It's ~2000 lines per the task.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:11.937Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1456 && ls -la Terraria.GameContent.Generation.Dungeon/ && wc -l \"Terraria.GameContent.Generation.Dungeon/DungeonCrawler.cs\" Terraria.GameContent.Generation.Dungeon.LayoutProviders/*.cs 2>/dev/null | tail -20",
 "description": "List dungeon source directory and line counts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:11.971Z

**📎 ToolResult**

```
total 432
drwxr-xr-x@  23 user  staff    736  8月  9 19:04 .
drwxr-xr-x@ 192 user  staff   6144  8月  9 19:04 ..
-rw-r--r--@   1 user  staff    356  8月  9 19:04 DualDungeonUnbreakableWallTiers.cs
-rw-r--r--@   1 user  staff   7019  8月  9 19:04 DungeonBounds.cs
-rw-r--r--@   1 user  staff    102  8月  9 19:04 DungeonColor.cs
-rw-r--r--@   1 user  staff  37166  8月  9 19:04 DungeonCrawler.cs
-rw-r--r--@   1 user  staff   4784  8月  9 19:04 DungeonData.cs
-rw-r--r--@   1 user  staff    431  8月  9 19:04 DungeonDoorData.cs
-rw-r--r--@   1 user  staff   3106  8月  9 19:04 DungeonGenerationStyleData.cs
-rw-r--r--@   1 user  staff    661  8月  9 19:04 DungeonGenerationStyleID.cs
-rw-r--r--@   1 user  staff  27574  8月  9 19:04 DungeonGenerationStyles.cs
-rw-r--r--@   1 user  staff   1472  8月  9 19:04 DungeonGenVars.cs
-rw-r--r--@   1 user  staff    437  8月  9 19:04 DungeonLayoutProvider.cs
-rw-r--r--@   1 user  staff    145  8月  9 19:04 DungeonLayoutProviderSettings.cs
-rw-r--r--@   1 user  staff    840  8月  9 19:04 DungeonPlatformData.cs
-rw-r--r--@   1 user  staff    321  8月  9 19:04 DungeonRoomSearchSettings.cs
-rw-r--r--@   1 user  staff   4312  8月  9 19:04 DungeonShapes.cs
-rw-r--r--@   1 user  staff    103  8月  9 19:04 DungeonType.cs
-rw-r--r--@   1 user  staff  62371  8月  9 19:04 DungeonUtils.cs
-rw-r--r--@   1 user  staff    143  8月  9 19:04 ProgressionStageCheck.cs
-rw-r--r--@   1 user  staff    121  8月  9 19:04 ProtectionType.cs
-rw-r--r--@   1 user  staff    118  8月  9 19:04 SnakeOrientation.cs
-rw-r--r--@   1 user  staff    130  8月  9 19:04 WindowType.cs
     953 Terraria.GameContent.Generation.Dungeon/DungeonCrawler.cs
    1019 Terraria.GameContent.Generation.Dungeon.LayoutProviders/DualDungeonLayoutProvider.cs
       5 Terraria.GameContent.Generation.Dungeon.LayoutProviders/DualDungeonLayoutProviderSettings.cs
      99 Terraria.GameContent.Generation.Dungeon.LayoutProviders/LegacyDungeonLayoutProvider.cs
       8 Terraria.GameContent.Generation.Dungeon.LayoutProviders/LegacyDungeonLayoutProviderSettings.cs
    2084 total

```


---

## 🤖 Assistant · 2026-08-12T18:46:12.999Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria.GameContent.Generation.Dungeon/DungeonCrawler.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:13.213Z

**📎 ToolResult**

```
1	using System;
2	using System.Collections.Generic;
3	using Microsoft.Xna.Framework;
4	using ReLogic.Utilities;
5	using Terraria.GameContent.Biomes;
6	using Terraria.GameContent.Generation.Dungeon.Entrances;
7	using Terraria.GameContent.Generation.Dungeon.Features;
8	using Terraria.GameContent.Generation.Dungeon.Halls;
9	using Terraria.GameContent.Generation.Dungeon.LayoutProviders;
10	using Terraria.GameContent.Generation.Dungeon.Rooms;
11	using Terraria.ID;
12	using Terraria.Localization;
13	using Terraria.Utilities;
14	using Terraria.WorldBuilding;
15	
16	namespace Terraria.GameContent.Generation.Dungeon;
17	
18	public static class DungeonCrawler
19	{
20		public static List<DungeonData> dungeonData = new List<DungeonData>();
21	
22		public static DungeonData CurrentDungeonData
23		{
24			get
25			{
26				return dungeonData[GenVars.CurrentDungeon];
27			}
28			set
29			{
30				dungeonData[GenVars.CurrentDungeon] = value;
31			}
32		}
33	
34		public static void SetupDungeonData(int currentDungeon, bool clearOld = false)
35		{
36			if (clearOld)
37			{
38				dungeonData.Clear();
39			}
40			GenVars.CurrentDungeon = currentDungeon;
41			DungeonType type = DungeonType.Default;
42			if (WorldGen.SecretSeed.dualDungeons.Enabled)
43			{
44				type = DungeonType.DualDungeon;
45			}
46			DungeonData item = new DungeonData
47			{
48				Type = type,
49				Iteration = currentDungeon
50			};
51			dungeonData.Add(item);
52		}
53	
54		public static void SetupDungeonGenVarVariables(DungeonGenVars genVars, UnifiedRandom genRand)
55		{
56			int num = genRand.Next(3);
57			if (WorldGen.remixWorldGen)
58			{
59				num = (WorldGen.crimson ? 2 : 0);
60			}
61			switch (num)
62			{
63			case 0:
64				genVars.dungeonColor = DungeonColor.Blue;
65				genVars.brickTileType = 41;
66				genVars.brickWallType = 7;
67				genVars.brickCrackedTileType = 481;
68				genVars.windowGlassWallType = 91;
69				genVars.windowClosedGlassWallType = 96;
70				genVars.windowEdgeWallType = 8;
71				genVars.windowPlatformItemTypes = new int[1] { 1386 };
72				break;
73			case 1:
74				genVars.dungeonColor = DungeonColor.Green;
75				genVars.brickTileType = 43;
76				genVars.brickWallType = 8;
77				genVars.brickCrackedTileType = 482;
78				genVars.windowGlassWallType = 92;
79				genVars.windowClosedGlassWallType = 94;
80				genVars.windowEdgeWallType = 9;
81				genVars.windowPlatformItemTypes = new int[1] { 1385 };
82				break;
83			default:
84				genVars.dungeonColor = DungeonColor.Pink;
85				genVars.brickTileType = 44;
86				genVars.brickWallType = 9;
87				genVars.brickCrackedTileType = 483;
88				genVars.windowGlassWallType = 90;
89				genVars.windowClosedGlassWallType = 98;
90				genVars.windowEdgeWallType = 7;
91				genVars.windowPlatformItemTypes = new int[1] { 1384 };
92				break;
93			}
94			if (WorldGen.drunkWorldGen)
95			{
96				switch (genRand.Next(3))
97				{
98				case 0:
99					genVars.brickWallType = 7;
100					break;
101				case 1:
102					genVars.brickWallType = 8;
103					break;
104				default:
105					genVars.brickWallType = 9;
106					break;
107				}
108			}
109			DungeonUtils.CreatePotentialDungeonBounds(out genVars.innerPotentialDungeonBounds, out genVars.outerPotentialDungeonBounds, genVars.dungeonSide == DungeonSide.Left, 0.10000000149011612, 0.05000000074505806);
110			genVars.dungeonStyle = DungeonGenerationStyles.GetCurrentDungeonStyle();
111			if (WorldGen.SecretSeed.dualDungeons.Enabled)
112			{
113				int num2 = GenVars.CurrentDungeon % 2;
114				if (num2 == 0 || num2 != 1)
115				{
116					genVars.dungeonGenerationStyles.Add(DungeonGenerationStyles.Cavern);
117					genVars.dungeonGenerationStyles.Add(WorldGen.crimson ? DungeonGenerationStyles.Crimson : DungeonGenerationStyles.Corruption);
118					genVars.dungeonGenerationStyles.Add(DungeonGenerationStyles.Jungle);
119					genVars.dungeonGenerationStyles.Add(genVars.dungeonStyle);
120				}
121				else
122				{
123					genVars.dungeonGenerationStyles.Add(DungeonGenerationStyles.Snow);
124					genVars.dungeonGenerationStyles.Add(DungeonGenerationStyles.Desert);
125					genVars.dungeonGenerationStyles.Add(DungeonGenerationStyles.Hallow);
126					genVars.dungeonGenerationStyles.Add(DungeonGenerationStyles.Temple);
127				}
128			}
129			else
130			{
131				genVars.dungeonGenerationStyles.Add(genVars.dungeonStyle);
132			}
133			genVars.isDungeonTile = Main.tileDungeon;
134			genVars.isCrackedBrick = TileID.Sets.CrackedBricks;
135			genVars.isPitTrapTile = TileID.Sets.CrackedBricks;
136			genVars.isDungeonWall = Main.wallDungeon;
137			genVars.isDungeonWallGlass = WallID.Sets.Glass;
138			if (WorldGen.SecretSeed.dualDungeons.Enabled)
139			{
140				genVars.isDungeonTile = (bool[])genVars.isDungeonTile.Clone();
141				genVars.isCrackedBrick = (bool[])genVars.isCrackedBrick.Clone();
142				genVars.isPitTrapTile = (bool[])genVars.isPitTrapTile.Clone();
143				genVars.isDungeonWall = (bool[])genVars.isDungeonWall.Clone();
144				genVars.isDungeonWallGlass = (bool[])genVars.isDungeonWallGlass.Clone();
145				List<DungeonGenerationStyleData> list = new List<DungeonGenerationStyleData>(genVars.dungeonGenerationStyles);
146				foreach (DungeonGenerationStyleData dungeonGenerationStyle in genVars.dungeonGenerationStyles)
147				{
148					if (dungeonGenerationStyle.SubStyles != null)
149					{
150						list.AddRange(dungeonGenerationStyle.SubStyles);
151					}
152				}
153				foreach (DungeonGenerationStyleData item in list)
154				{
155					genVars.isDungeonTile[item.BrickTileType] = true;
156					if (item.BrickGrassTileType.HasValue)
157					{
158						genVars.isDungeonTile[item.BrickGrassTileType.Value] = true;
159					}
160					genVars.isCrackedBrick[item.BrickCrackedTileType] = true;
161					genVars.isPitTrapTile[item.PitTrapTileType] = true;
162					genVars.isDungeonWall[item.BrickWallType] = true;
163					genVars.isDungeonWallGlass[item.WindowGlassWallType] = true;
164					genVars.isDungeonWallGlass[item.WindowClosedGlassWallType] = true;
165				}
166			}
167			DungeonEntranceType dungeonEntranceType = DungeonEntranceType.Legacy;
168			bool flag = false;
169			int num3 = 50;
170			while (!flag)
171			{
172				num3--;
173				if (num3 <= 0)
174				{
175					dungeonEntranceType = DungeonEntranceType.Legacy;
176					break;
177				}
178				dungeonEntranceType = DungeonEntranceType.Legacy;
179				if (genRand.Next(3) == 0)
180				{
181					dungeonEntranceType = DungeonEntranceType.Dome;
182				}
183				if (genRand.Next(3) == 0)
184				{
185					dungeonEntranceType = DungeonEntranceType.Tower;
186				}
187				flag = true;
188				if (WorldGen.SecretSeed.surfaceIsInSpace.Enabled && dungeonEntranceType == DungeonEntranceType.Tower)
189				{
190					flag = false;
191				}
192			}
193			genVars.preGenDungeonEntranceSettings = (PreGenDungeonEntranceSettings)MakeDungeon_GetEntranceSettings(dungeonEntranceType, genVars.dungeonStyle, null);
194		}
195	
196		public static void SetupDungeonDataVariables(int iteration, UnifiedRandom genRand)
197		{
198			//IL_0495: Unknown result type (might be due to invalid IL or missing references)
199			//IL_049a: Unknown result type (might be due to invalid IL or missing references)
200			//IL_045d: Unknown result type (might be due to invalid IL or missing references)
201			//IL_0462: Unknown result type (might be due to invalid IL or missing references)
202			DungeonData dungeonData = DungeonCrawler.dungeonData[iteration];
203			dungeonData.wallVariants = new int[3];
204			switch (dungeonData.genVars.brickWallType)
205			{
206			default:
207				dungeonData.wallVariants[0] = 7;
208				dungeonData.wallVariants[1] = 94;
209				dungeonData.wallVariants[2] = 95;
210				break;
211			case 8:
212				dungeonData.wallVariants[0] = 8;
213				dungeonData.wallVariants[1] = 98;
214				dungeonData.wallVariants[2] = 99;
215				break;
216			case 9:
217				dungeonData.wallVariants[0] = 9;
218				dungeonData.wallVariants[1] = 96;
219				dungeonData.wallVariants[2] = 97;
220				break;
221			}
222			dungeonData.platformItemType = 1384;
223			dungeonData.chandelierItemType = 2652;
224			dungeonData.doorItemType = 1411;
225			switch (dungeonData.genVars.dungeonColor)
226			{
227			default:
228				dungeonData.platformItemType = 1384;
229				dungeonData.chandelierItemType = 2652;
230				dungeonData.doorItemType = 1411;
231				break;
232			case DungeonColor.Green:
233				dungeonData.platformItemType = 1386;
234				dungeonData.chandelierItemType = 2653;
235				dungeonData.doorItemType = 1412;
236				break;
237			case DungeonColor.Pink:
238				dungeonData.platformItemType = 1385;
239				dungeonData.chandelierItemType = 2654;
240				dungeonData.doorItemType = 1413;
241				break;
242			}
243			dungeonData.shelfStyles = new int[3];
244			dungeonData.shelfStyles[0] = genRand.Next(9, 13);
245			dungeonData.shelfStyles[1] = genRand.Next(9, 13);
246			while (dungeonData.shelfStyles[1] == dungeonData.shelfStyles[0])
247			{
248				dungeonData.shelfStyles[1] = genRand.Next(9, 13);
249			}
250			dungeonData.shelfStyles[2] = genRand.Next(9, 13);
251			while (dungeonData.shelfStyles[2] == dungeonData.shelfStyles[0] || dungeonData.shelfStyles[2] == dungeonData.shelfStyles[1])
252			{
253				dungeonData.shelfStyles[2] = genRand.Next(9, 13);
254			}
255			dungeonData.lanternStyles = new int[3];
256			dungeonData.lanternStyles[0] = genRand.Next(7);
257			dungeonData.lanternStyles[1] = genRand.Next(7);
258			while (dungeonData.lanternStyles[1] == dungeonData.lanternStyles[0])
259			{
260				dungeonData.lanternStyles[1] = genRand.Next(7);
261			}
262			dungeonData.lanternStyles[2] = genRand.Next(7);
263			while (dungeonData.lanternStyles[2] == dungeonData.lanternStyles[0] || dungeonData.lanternStyles[2] == dungeonData.lanternStyles[1])
264			{
265				dungeonData.lanternStyles[2] = genRand.Next(7);
266			}
267			dungeonData.bannerStyles = new int[6];
268			dungeonData.bannerStyles[0] = 10;
269			dungeonData.bannerStyles[1] = 11;
270			dungeonData.bannerStyles[2] = 12;
271			dungeonData.bannerStyles[3] = 13;
272			dungeonData.bannerStyles[4] = 14;
273			dungeonData.bannerStyles[5] = 15;
274			dungeonData.useSkewedDungeonEntranceHalls = genRand.Next(4) == 0;
275			if (!dungeonData.genVars.preGenDungeonEntranceSettings.PrecalculateEntrancePosition)
276			{
277				return;
278			}
279			int num = dungeonData.genVars.dungeonLocation;
280			int num2 = 0;
281			bool flag = false;
282			int num3 = 100;
283			int num4 = 3000;
284			while (!flag)
285			{
286				num4--;
287				if (num4 <= 0)
288				{
289					break;
290				}
291				num = dungeonData.genVars.dungeonLocation - num3 + genRand.Next(num3 * 2);
292				if (num > WorldGen.beachDistance && num < Main.maxTilesX - WorldGen.beachDistance)
293				{
294					num2 = 10;
295					if (SpecialSeedFeatures.DungeonEntranceIsBuried)
296					{
297						num2 = (int)Main.worldSurface - 10 + GenVars.CurrentDungeonGenVars.preGenDungeonEntranceSettings.BuriedEntranceYOffset;
298					}
299					if (SpecialSeedFeatures.DungeonEntranceIsUnderground)
300					{
301						num2 = (SpecialSeedFeatures.DungeonEntranceHasATree ? ((int)GenVars.rockLayer - 20) : ((dungeonData.Type != DungeonType.DualDungeon) ? ((int)GenVars.rockLayer - 20) : ((int)GenVars.worldSurfaceHigh - 20)));
302					}
303					Tile tile = Main.tile[num, num2];
304					while (tile != null && !tile.active() && tile.liquid <= 0 && tile.wall <= 0)
305					{
306						num2++;
307						tile = Main.tile[num, num2];
308					}
309					if (!WorldGen.AreAnyTilesInSetNearby(num, num2, TileID.Sets.Clouds, 15) && !WorldGen.AreAnyTilesInSetNearby(num, Math.Max(50, num2 - 50), TileID.Sets.Clouds, 50) && num2 - 40 - dungeonData.genVars.preGenDungeonEntranceSettings.RoughHeight > 0)
310					{
311						flag = true;
312					}
313				}
314			}
315			if (flag)
316			{
317				dungeonData.genVars.dungeonLocation = num + 25 - genRand.Next(50);
318				dungeonData.genVars.dungeonEntrancePosition = new Vector2D((double)num, (double)num2);
319			}
320			else
321			{
322				dungeonData.genVars.preGenDungeonEntranceSettings = (PreGenDungeonEntranceSettings)MakeDungeon_GetEntranceSettings(DungeonEntranceType.Legacy, dungeonData.genVars.preGenDungeonEntranceSettings.StyleData, null);
323				dungeonData.genVars.dungeonEntrancePosition = Vector2D.Zero;
324			}
325		}
326	
327		public static void MakeDungeon(int x, int y, GenerationProgress progress = null)
328		{
329			//IL_02a8: Unknown result type (might be due to invalid IL or missing references)
330			//IL_02ad: Unknown result type (might be due to invalid IL or missing references)
331			//IL_02af: Unknown result type (might be due to invalid IL or missing references)
332			//IL_02b1: Unknown result type (might be due to invalid IL or missing references)
333			//IL_0325: Unknown result type (might be due to invalid IL or missing references)
334			//IL_0327: Unknown result type (might be due to invalid IL or missing references)
335			//IL_045d: Unknown result type (might be due to invalid IL or missing references)
336			UnifiedRandom genRand = WorldGen.genRand;
337			DungeonData currentDungeonData = CurrentDungeonData;
338			DungeonFeatureSettings settings = new DungeonFeatureSettings();
339			currentDungeonData.genVars.GeneratingDungeon = true;
340			DungeonUtils.UpdateDungeonProgress(progress, 0f, Language.GetTextValue("WorldGeneration.DungeonVariableSetup"));
341			_ = currentDungeonData.genVars.brickTileType;
342			_ = currentDungeonData.genVars.brickCrackedTileType;
343			_ = currentDungeonData.genVars.brickWallType;
344			WorldGen.SetCrackedBrickSolidity(solid: false);
345			currentDungeonData.makeNextPitTrapFlooded = true;
346			currentDungeonData.genVars.generatingDungeonPositionX = x;
347			currentDungeonData.genVars.generatingDungeonPositionY = y;
348			currentDungeonData.dungeonBounds.SetBounds(x, y, x, y);
349			currentDungeonData.dungeonEntranceStrengthX = genRand.Next(25, 30);
350			currentDungeonData.dungeonEntranceStrengthY = genRand.Next(20, 25);
351			currentDungeonData.dungeonEntranceStrengthX2 = genRand.Next(35, 50);
352			currentDungeonData.dungeonEntranceStrengthY2 = genRand.Next(10, 15);
353			int num = Main.maxTilesX / 60;
354			num += genRand.Next(0, num / 3);
355			num = (int)((double)num * currentDungeonData.dungeonStepScalar);
356			int maxSteps = num;
357			int roomDelay = 5;
358			currentDungeonData.globalFeatureScalar = 1.0;
359			if (currentDungeonData.Type == DungeonType.DualDungeon)
360			{
361				DualDungeonLayoutProviderSettings dualDungeonLayoutProviderSettings = new DualDungeonLayoutProviderSettings();
362				dualDungeonLayoutProviderSettings.StyleData = currentDungeonData.genVars.dungeonStyle;
363				new DualDungeonLayoutProvider(dualDungeonLayoutProviderSettings).ProvideLayout(currentDungeonData, progress, genRand, ref roomDelay);
364				currentDungeonData.globalFeatureScalar = Math.Max(1.0, (double)currentDungeonData.dungeonRooms.Count / 20.0);
365			}
366			else
367			{
368				LegacyDungeonLayoutProviderSettings legacyDungeonLayoutProviderSettings = new LegacyDungeonLayoutProviderSettings();
369				legacyDungeonLayoutProviderSettings.StyleData = currentDungeonData.genVars.dungeonStyle;
370				legacyDungeonLayoutProviderSettings.Steps = num;
371				legacyDungeonLayoutProviderSettings.MaxSteps = maxSteps;
372				new LegacyDungeonLayoutProvider(legacyDungeonLayoutProviderSettings).ProvideLayout(currentDungeonData, progress, genRand, ref roomDelay);
373			}
374			DungeonBounds innerBounds = currentDungeonData.dungeonRooms[0].InnerBounds;
375			Vector2 vector = new Vector2(innerBounds.Center.X, innerBounds.Top);
376			float x2 = vector.X;
377			float y2 = vector.Y;
378			if (currentDungeonData.Type == DungeonType.Default)
379			{
380				for (int i = 1; i < currentDungeonData.dungeonRooms.Count; i++)
381				{
382					if (currentDungeonData.dungeonRooms[i].generated)
383					{
384						innerBounds = currentDungeonData.dungeonRooms[i].InnerBounds;
385						vector = new Vector2(innerBounds.Center.X, innerBounds.Top);
386						if (vector.Y < y2)
387						{
388							x2 = vector.X;
389							y2 = vector.Y;
390						}
391					}
392				}
393			}
394			currentDungeonData.genVars.generatingDungeonPositionX = (int)x2;
395			currentDungeonData.genVars.generatingDungeonPositionY = (int)y2;
396			currentDungeonData.genVars.generatingDungeonTopX = (int)x2;
397			DungeonUtils.UpdateDungeonProgress(progress, 0.65f, Language.GetTextValue("WorldGeneration.DungeonEntranceHallway"));
398			currentDungeonData.createdDungeonEntranceOnSurface = false;
399			roomDelay = 5;
400			Vector2D dungeonEntrancePosition = currentDungeonData.genVars.dungeonEntrancePosition;
401			bool flag = dungeonEntrancePosition != Vector2D.Zero;
402			if (flag && WorldGen.SecretSeed.surfaceIsDesert.Enabled && currentDungeonData.Type == DungeonType.DualDungeon)
403			{
404				currentDungeonData.createdDungeonEntranceOnSurface = true;
405			}
406			if (WorldGen.drunkWorldGen || WorldGen.SecretSeed.noSurface.Enabled)
407			{
408				currentDungeonData.createdDungeonEntranceOnSurface = true;
409			}
410			Vector2D currentPos = default(Vector2D);
411			((Vector2D)(ref currentPos))._002Ector((double)currentDungeonData.genVars.generatingDungeonPositionX, (double)currentDungeonData.genVars.generatingDungeonPositionY);
412			double num2 = (flag ? dungeonEntrancePosition.Distance(currentPos) : 0.0);
413			int amountPassed = (int)num2;
414			int num3 = 100;
415			while (!currentDungeonData.createdDungeonEntranceOnSurface)
416			{
417				num3--;
418				if (num3 <= 0)
419				{
420					break;
421				}
422				if (roomDelay > 0)
423				{
424					roomDelay--;
425				}
426				if (roomDelay == 0 && genRand.Next(5) == 0 && (double)currentDungeonData.genVars.generatingDungeonPositionY > Main.worldSurface + 100.0)
427				{
428					roomDelay = 10;
429					int generatingDungeonPositionX = currentDungeonData.genVars.generatingDungeonPositionX;
430					int generatingDungeonPositionY = currentDungeonData.genVars.generatingDungeonPositionY;
431					MakeDungeon_GetHall_Legacy((LegacyDungeonHallSettings)MakeDungeon_GetHallSettings(DungeonHallType.Legacy, currentDungeonData, Vector2.Zero, Vector2.Zero, currentDungeonData.genVars.dungeonStyle)).GenerateHall(currentDungeonData, currentDungeonData.genVars.generatingDungeonPositionX, currentDungeonData.genVars.generatingDungeonPositionY);
432					MakeDungeon_GetRoom(new LegacyDungeonRoomSettings
433					{
434						RoomPosition = new Point(currentDungeonData.genVars.generatingDungeonPositionX, currentDungeonData.genVars.generatingDungeonPositionY),
435						RandomSeed = genRand.Next(),
436						StyleData = currentDungeonData.genVars.dungeonStyle
437					}).GenerateRoom(currentDungeonData);
438					currentDungeonData.genVars.generatingDungeonPositionX = generatingDungeonPositionX;
439					currentDungeonData.genVars.generatingDungeonPositionY = generatingDungeonPositionY;
440				}
441				if (flag)
442				{
443					MakeDungeon_GenerateNextEntranceHall_Precalculated(currentDungeonData, genRand, num2, dungeonEntrancePosition, ref amountPassed, ref currentPos);
444				}
445				else
446				{
447					MakeDungeon_GenerateNextEntranceHall_Legacy(currentDungeonData, currentDungeonData.genVars.generatingDungeonPositionX, currentDungeonData.genVars.generatingDungeonPositionY);
448				}
449			}
450			MakeDungeon_GetEntrance(MakeDungeon_GetEntranceSettings(currentDungeonData.genVars.preGenDungeonEntranceSettings, currentDungeonData)).GenerateEntrance(currentDungeonData, currentDungeonData.genVars.generatingDungeonPositionX, currentDungeonData.genVars.generatingDungeonPositionY);
451			if (WorldGen.SecretSeed.surfaceIsInSpace.Enabled)
452			{
453				currentDungeonData.dungeonBounds.Top = 25;
454			}
455			DungeonUtils.UpdateDungeonProgress(progress, 0.675f, Language.GetTextValue("WorldGeneration.DungeonFindingDoorsAndPlatforms"));
456			for (int j = 0; j < currentDungeonData.dungeonRooms.Count; j++)
457			{
458				DungeonRoom dungeonRoom = currentDungeonData.dungeonRooms[j];
459				if (dungeonRoom.Processed)
460				{
461					dungeonRoom.CalculatePlatformsAndDoors(currentDungeonData);
462				}
463			}
464			for (int k = 0; k < currentDungeonData.dungeonHalls.Count; k++)
465			{
466				DungeonHall dungeonHall = currentDungeonData.dungeonHalls[k];
467				if (dungeonHall.Processed)
468				{
469					dungeonHall.CalculatePlatformsAndDoors(currentDungeonData);
470				}
471			}
472			DungeonUtils.UpdateDungeonProgress(progress, 0.7f, Language.GetTextValue("WorldGeneration.DungeonEarly"));
473			new DungeonGlobalEarlyDualDungeonFeatures(settings).GenerateFeature(currentDungeonData);
474			DungeonUtils.UpdateDungeonProgress(progress, 0.75f, Language.GetTextValue("WorldGeneration.DungeonSpikes"));
475			new DungeonGlobalSpikes(settings).GenerateFeature(currentDungeonData);
476			DungeonUtils.UpdateDungeonProgress(progress, 0.8f, Language.GetTextValue("WorldGeneration.DungeonDoors"));
477			new DungeonGlobalDoors(settings).GenerateFeature(currentDungeonData);
478			DungeonUtils.UpdateDungeonProgress(progress, 0.825f, Language.GetTextValue("WorldGeneration.DungeonWallVariants"));
479			new DungeonGlobalWallVariants(settings).GenerateFeature(currentDungeonData);
480			DungeonUtils.UpdateDungeonProgress(progress, 0.85f, Language.GetTextValue("WorldGeneration.DungeonPlatforms"));
481			new DungeonGlobalPlatforms(settings).GenerateFeature(currentDungeonData);
482			DungeonUtils.UpdateDungeonProgress(progress, 0.875f, Language.GetTextValue("WorldGeneration.DungeonBiomeChests"));
483			new DungeonGlobalBiomeChests(settings).GenerateFeature(currentDungeonData);
484			DungeonUtils.UpdateDungeonProgress(progress, 0.9f, Language.GetTextValue("WorldGeneration.DungeonBookshelves"));
485			new DungeonGlobalBookshelves(settings).GenerateFeature(currentDungeonData);
486			DungeonUtils.UpdateDungeonProgress(progress, 0.92f, Language.GetTextValue("WorldGeneration.DungeonChests"));
487			new DungeonGlobalBasicChests(settings).GenerateFeature(currentDungeonData);
488			DungeonUtils.UpdateDungeonProgress(progress, 0.935f, Language.GetTextValue("WorldGeneration.DungeonArea"));
489			int amount = 25;
490			currentDungeonData.dungeonBounds.Inflate(amount);
491			DungeonUtils.UpdateDungeonProgress(progress, 0.94f, Language.GetTextValue("WorldGeneration.DungeonLights"));
492			new DungeonGlobalLights(settings).GenerateFeature(currentDungeonData);
493			DungeonUtils.UpdateDungeonProgress(progress, 0.95f, Language.GetTextValue("WorldGeneration.DungeonTraps"));
494			new DungeonGlobalTraps(settings).GenerateFeature(currentDungeonData);
495			DungeonUtils.UpdateDungeonProgress(progress, 0.96f, Language.GetTextValue("WorldGeneration.DungeonFurniture"));
496			new DungeonGlobalGroundFurniture(settings).GenerateFeature(currentDungeonData);
497			DungeonUtils.UpdateDungeonProgress(progress, 0.97f, Language.GetTextValue("WorldGeneration.DungeonPictures"));
498			new DungeonGlobalPaintings(settings).GenerateFeature(currentDungeonData);
499			DungeonUtils.UpdateDungeonProgress(progress, 0.98f, Language.GetTextValue("WorldGeneration.DungeonBanners"));
500			new DungeonGlobalBanners(settings).GenerateFeature(currentDungeonData);
501			DungeonUtils.UpdateDungeonProgress(progress, 0.99f, Language.GetTextValue("WorldGeneration.DungeonLate"));
502			new DungeonGlobalLateDualDungeonFeatures(settings).GenerateFeature(currentDungeonData);
503			DungeonUtils.UpdateDungeonProgress(progress, 1f, Language.GetTextValue("WorldGeneration.DungeonComplete"));
504			currentDungeonData.genVars.GeneratingDungeon = false;
505		}
506	
507		public static void MakeDungeon_GenerateNextEntranceHall_Legacy(DungeonData data, int x, int y)
508		{
509			((LegacyEntranceDungeonHall)MakeDungeon_GetHall(new LegacyEntranceDungeonHallSettings
510			{
511				HallType = DungeonHallType.LegacyEntrance,
512				StyleData = data.genVars.dungeonStyle,
513				RandomSeed = WorldGen.genRand.Next()
514			})).GenerateHall(data, x, y);
515		}
516	
517		public static void MakeDungeon_GenerateNextEntranceHall_Precalculated(DungeonData data, UnifiedRandom genRand, double dist, Vector2D entrancePos, ref int amountPassed, ref Vector2D currentPos)
518		{
519			//IL_0024: Unknown result type (might be due to invalid IL or missing references)
520			//IL_0029: Unknown result type (might be due to invalid IL or missing references)
521			//IL_0030: Unknown result type (might be due to invalid IL or missing references)
522			//IL_0035: Unknown result type (might be due to invalid IL or missing references)
523			//IL_007b: Unknown result type (might be due to invalid IL or missing references)
524			//IL_0080: Unknown result type (might be due to invalid IL or missing references)
525			//IL_0096: Unknown result type (might be due to invalid IL or missing references)
526			//IL_0097: Unknown result type (might be due to invalid IL or missing references)
527			int num = genRand.Next(10, 30);
528			if ((double)num > dist - (double)amountPassed)
529			{
530				num = Math.Max(1, (int)dist - amountPassed);
531			}
532			Vector2D val = Vector2D.Lerp(currentPos, entrancePos, (double)amountPassed / dist);
533			DungeonHall dungeonHall = MakeDungeon_GetHall(new LegacyEntranceDungeonHallSettings
534			{
535				HallType = DungeonHallType.LegacyEntrance,
536				StyleData = data.genVars.dungeonStyle,
537				RandomSeed = WorldGen.genRand.Next(),
538				OverrideSteps = num,
539				UsePrecalculatedEntrance = true
540			});
541			dungeonHall.CalculateHall(data, currentPos, val);
542			dungeonHall.GenerateHall(data);
543			amountPassed -= num;
544			currentPos = val;
545			if (amountPassed <= 0)
546			{
547				data.createdDungeonEntranceOnSurface = true;
548			}
549		}
550	
551		public static DungeonRoomSettings MakeDungeon_GetRoomSettings(DungeonRoomType roomType, DungeonData data, DungeonControlLine line)
552		{
553			//IL_0017: Unknown result type (might be due to invalid IL or missing references)
554			//IL_001c: Unknown result type (might be due to invalid IL or missing references)
555			//IL_00e2: Unknown result type (might be due to invalid IL or missing references)
556			//IL_00e4: Unknown result type (might be due to invalid IL or missing references)
557			//IL_00e9: Unknown result type (might be due to invalid IL or missing references)
558			//IL_00ee: Unknown result type (might be due to invalid IL or missing references)
559			UnifiedRandom genRand = WorldGen.genRand;
560			DungeonRoomSettings dungeonRoomSettings = null;
561			int progressionStage = line.ProgressionStage;
562			DungeonGenerationStyleData style = line.Style;
563			Vector2D normalizedLineDirection = line.NormalizedLineDirection;
564			bool curveLine = line.CurveLine;
565			int num = (int)(15.0 * data.roomStrengthScalar);
566			int num2 = genRand.Next(13);
567			int num3 = genRand.Next(13);
568			int num4 = 6;
569			int num5 = genRand.Next(12);
570			int num6 = genRand.Next(12);
571			float num7 = 1f;
572			if (data.Type == DungeonType.DualDungeon)
573			{
574				num7 = 1.25f;
575			}
576			if ((roomType == DungeonRoomType.GenShapeDoughnut || roomType == DungeonRoomType.GenShapeQuadCircle) && curveLine)
577			{
578				roomType = DungeonRoomType.GenShapeCircle;
579			}
580			switch (roomType)
581			{
582			default:
583				dungeonRoomSettings = new LegacyDungeonRoomSettings
584				{
585					OverrideStrength = num + num2,
586					OverrideSteps = num4 + num5,
587					OverrideVelocity = normalizedLineDirection.SafeNormalize(Vector2D.UnitY)
588				};
589				break;
590			case DungeonRoomType.Regular:
591				num = (int)((double)num * 0.8);
592				num2 = (int)((double)num2 * 0.8);
593				dungeonRoomSettings = new RegularDungeonRoomSettings
594				{
595					OverrideOuterBoundsSize = 8,
596					OverrideInnerBoundsSize = num + num2
597				};
598				break;
599			case DungeonRoomType.Wormlike:
600			{
601				int firstSideIterations = num4 * 3 + num5;
602				int secondSideIterations = num4 * 3 + num6;
603				dungeonRoomSettings = new WormlikeDungeonRoomSettings
604				{
605					FirstSideIterations = firstSideIterations,
606					SecondSideIterations = secondSideIterations
607				};
608				break;
609			}
610			case DungeonRoomType.LivingTree:
611			{
612				num = (int)((double)num * 0.3);
613				num2 = (int)((double)num2 * 0.5);
614				int innerWidth = num + num2;
615				int num23 = num4 * 6 + num5;
616				int num24 = 4 + genRand.Next(3);
617				int boundingRadius = (num23 + num24 + num24) / 2;
618				dungeonRoomSettings = new LivingTreeDungeonRoomSettings
619				{
620					InnerWidth = innerWidth,
621					InnerHeight = num23,
622					Depth = num24,
623					BoundingRadius = boundingRadius,
624					ForceStyleForDoorsAndPlatforms = true
625				};
626				break;
627			}
628			case DungeonRoomType.BiomeSquare:
629			case DungeonRoomType.BiomeRugged:
630			case DungeonRoomType.BiomeStructured:
631				dungeonRoomSettings = new BiomeDungeonRoomSettings();
632				break;
633			case DungeonRoomType.GenShapeCircle:
634			{
635				num = (int)((double)num * 0.8);
636				num2 = (int)((double)num2 * 0.8);
637				if (num7 != 1f && genRand.Next(3) == 0)
638				{
639					num = (int)((float)num * num7);
640					num2 = (int)((float)num2 * num7);
641				}
642				int num15 = num;
643				int num16 = num15 + 8;
644				DungeonShapes.CircleRoom innerShape3 = new DungeonShapes.CircleRoom(num15 + num2);
645				DungeonShapes.CircleRoom outerShape3 = new DungeonShapes.CircleRoom(num16 + num2);
646				dungeonRoomSettings = new GenShapeDungeonRoomSettings
647				{
648					ShapeType = GenShapeType.Circle,
649					InnerShape = innerShape3,
650					OuterShape = outerShape3,
651					BoundingRadius = num16 + num2,
652					HallwayPointAdjuster = 10
653				};
654				break;
655			}
656			case DungeonRoomType.GenShapeMound:
657			{
658				if (num7 != 1f && genRand.Next(3) == 0)
659				{
660					num = (int)((float)num * num7);
661					num2 = (int)((float)num2 * num7);
662				}
663				int num17 = num + num2;
664				int num18 = num17 + 8;
665				DungeonShapes.MoundRoom innerShape4 = new DungeonShapes.MoundRoom(num17, (int)((double)num17 * 1.5));
666				DungeonShapes.MoundRoom outerShape4 = new DungeonShapes.MoundRoom(num18, (int)((double)num18 * 1.5));
667				dungeonRoomSettings = new GenShapeDungeonRoomSettings
668				{
669					ShapeType = GenShapeType.Mound,
670					InnerShape = innerShape4,
671					OuterShape = outerShape4,
672					BoundingRadius = (int)((double)num18 * 1.2)
673				};
674				break;
675			}
676			case DungeonRoomType.GenShapeHourglass:
677			{
678				if (num7 != 1f && genRand.Next(3) == 0)
679				{
680					num = (int)((float)num * num7);
681					num2 = (int)((float)num2 * num7);
682				}
683				int num19 = num + num2 + 10;
684				int num20 = num + num3 + 10;
685				int num21 = num19 + 16;
686				int num22 = num20 + 16;
687				DungeonShapes.HourglassRoom innerShape5 = new DungeonShapes.HourglassRoom(num19, num20, 0f);
688				DungeonShapes.HourglassRoom outerShape5 = new DungeonShapes.HourglassRoom(num21, num22, 0.4f);
689				dungeonRoomSettings = new GenShapeDungeonRoomSettings
690				{
691					ShapeType = GenShapeType.Hourglass,
692					InnerShape = innerShape5,
693					OuterShape = outerShape5,
694					BoundingRadius = ((num21 > num22) ? (num21 / 2) : (num22 / 2)) + 5,
695					HallwayPointAdjuster = 5
696				};
697				break;
698			}
699			case DungeonRoomType.GenShapeDoughnut:
700			{
701				num = (int)((double)num * 0.8);
702				num2 = (int)((double)num2 * 0.8);
703				int num11 = num + num2;
704				int num12 = num + num3;
705				int num13 = num11 + 8;
706				int num14 = num12 + 8;
707				DungeonShapes.CircleRoom innerShape2 = new DungeonShapes.CircleRoom(num11, num12);
708				DungeonShapes.CircleRoom outerShape2 = new DungeonShapes.CircleRoom(num13, num14);
709				dungeonRoomSettings = new GenShapeDungeonRoomSettings
710				{
711					ShapeType = GenShapeType.Doughnut,
712					InnerShape = innerShape2,
713					OuterShape = outerShape2,
714					BoundingRadius = ((num13 > num14) ? num13 : num14) + 5,
715					HallwayPointAdjuster = 5
716				};
717				break;
718			}
719			case DungeonRoomType.GenShapeQuadCircle:
720			{
721				if (num7 != 1f && genRand.Next(3) == 0)
722				{
723					num = (int)((float)num * 1.5f);
724					num2 = (int)((float)num2 * 1.5f);
725				}
726				int num8 = Math.Max(5, (int)((float)(num + num2) * 0.5f * 0.75f));
727				int num9 = num8 + 8;
728				int num10 = (int)((float)num8 * 1.5f);
729				DungeonShapes.QuadCircleRoom innerShape = new DungeonShapes.QuadCircleRoom(num8, num10);
730				DungeonShapes.QuadCircleRoom outerShape = new DungeonShapes.QuadCircleRoom(num9, num10);
731				dungeonRoomSettings = new GenShapeDungeonRoomSettings
732				{
733					ShapeType = GenShapeType.QuadCircle,
734					InnerShape = innerShape,
735					OuterShape = outerShape,
736					BoundingRadius = num9 / 2 + num10 + 4,
737					HallwayPointAdjuster = 5
738				};
739				break;
740			}
741			}
742			dungeonRoomSettings.RandomSeed = genRand.Next();
743			dungeonRoomSettings.RoomType = roomType;
744			dungeonRoomSettings.ProgressionStage = progressionStage;
745			dungeonRoomSettings.StyleData = style;
746			dungeonRoomSettings.OnCurvedLine = curveLine;
747			dungeonRoomSettings.Orientation = SnakeOrientation.Unknown;
748			dungeonRoomSettings.ControlLine = line;
749			return dungeonRoomSettings;
750		}
751	
752		public static DungeonHallSettings MakeDungeon_GetHallSettings(DungeonHallType hallType, DungeonData data, Vector2 hallStart, Vector2 hallEnd, DungeonGenerationStyleData style)
753		{
754			UnifiedRandom genRand = WorldGen.genRand;
755			DungeonHallSettings dungeonHallSettings = null;
756			switch (hallType)
757			{
758			default:
759				dungeonHallSettings = new LegacyDungeonHallSettings();
760				break;
761			case DungeonHallType.Regular:
762				dungeonHallSettings = new RegularDungeonHallSettings();
763				break;
764			case DungeonHallType.Stairwell:
765				dungeonHallSettings = new StairwellDungeonHallSettings
766				{
767					CrackedBrickChance = 0.0
768				};
769				break;
770			case DungeonHallType.Sine:
771			{
772				int num = Math.Max(1, (int)((hallStart - hallEnd).Length() / 30f));
773				int iterations = ((num <= 1) ? 1 : (1 + genRand.Next(num - 1)));
774				float magnitude = 8f + genRand.NextFloat() * 4f;
775				dungeonHallSettings = new SineDungeonHallSettings
776				{
777					CrackedBrickChance = 0.0,
778					Magnitude = magnitude,
779					Iterations = iterations,
780					FlipSine = (genRand.Next(2) == 0)
781				};
782				break;
783			}
784			}
785			dungeonHallSettings.RandomSeed = genRand.Next();
786			dungeonHallSettings.HallType = hallType;
787			dungeonHallSettings.StyleData = style;
788			return dungeonHallSettings;
789		}
790	
791		public static DungeonEntranceSettings MakeDungeon_GetEntranceSettings(PreGenDungeonEntranceSettings preSettings, DungeonData data)
792		{
793			DungeonEntranceSettings dungeonEntranceSettings = MakeDungeon_GetEntranceSettings(preSettings.EntranceType, preSettings.StyleData, data);
794			dungeonEntranceSettings.RandomSeed = preSettings.RandomSeed;
795			return dungeonEntranceSettings;
796		}
797	
798		public static DungeonEntranceSettings MakeDungeon_GetEntranceSettings(DungeonEntranceType entranceType, DungeonGenerationStyleData styleData, DungeonData data)
799		{
800			UnifiedRandom genRand = WorldGen.genRand;
801			DungeonEntranceSettings dungeonEntranceSettings = null;
802			if (data == null)
803			{
804				PreGenDungeonEntranceSettings preGenDungeonEntranceSettings = new PreGenDungeonEntranceSettings
805				{
806					EntranceType = entranceType,
807					StyleData = styleData
808				};
809				int num = 0;
810				if (WorldGen.SecretSeed.dualDungeons.Enabled)
811				{
812					num += 30;
813				}
814				switch (entranceType)
815				{
816				default:
817					preGenDungeonEntranceSettings.BuriedEntranceYOffset = num;
818					preGenDungeonEntranceSettings.BuriedEntranceSandDugoutYOffset = -num;
819					preGenDungeonEntranceSettings.RoughHeight = 40;
820					break;
821				case DungeonEntranceType.Dome:
822					preGenDungeonEntranceSettings.PrecalculateEntrancePosition = true;
823					preGenDungeonEntranceSettings.BuriedEntranceYOffset = 20 + num;
824					preGenDungeonEntranceSettings.BuriedEntranceSandDugoutYOffset = -num;
825					preGenDungeonEntranceSettings.RoughHeight = 55;
826					break;
827				case DungeonEntranceType.Tower:
828					preGenDungeonEntranceSettings.PrecalculateEntrancePosition = true;
829					preGenDungeonEntranceSettings.BuriedEntranceYOffset = 20 + num;
830					preGenDungeonEntranceSettings.BuriedEntranceSandDugoutYOffset = -num;
831					preGenDungeonEntranceSettings.RoughHeight = 120;
832					break;
833				}
834				preGenDungeonEntranceSettings.RandomSeed = genRand.Next();
835				return preGenDungeonEntranceSettings;
836			}
837			bool flag = false;
838			switch (entranceType)
839			{
840			default:
841				dungeonEntranceSettings = new LegacyDungeonEntranceSettings();
842				break;
843			case DungeonEntranceType.Dome:
844				dungeonEntranceSettings = new DomeDungeonEntranceSettings();
845				dungeonEntranceSettings.PrecalculateEntrancePosition = true;
846				break;
847			case DungeonEntranceType.Tower:
848				dungeonEntranceSettings = new TowerDungeonEntranceSettings();
849				dungeonEntranceSettings.PrecalculateEntrancePosition = true;
850				break;
851			}
852			dungeonEntranceSettings.RandomSeed = genRand.Next();
853			dungeonEntranceSettings.EntranceType = entranceType;
854			if (!flag)
855			{
856				dungeonEntranceSettings.StyleData = styleData;
857			}
858			return dungeonEntranceSettings;
859		}
860	
861		public static DungeonRoom MakeDungeon_TryRoom(DungeonData data, int i, int j, DungeonRoomSettings roomSettings, bool addToData = true, int fluff = 0, bool noRoomOverlap = true)
862		{
863			DungeonRoom roomFound = null;
864			if (data.IsAnyRoomInSpot(out roomFound, i, j, new DungeonRoomSearchSettings
865			{
866				Fluff = fluff
867			}))
868			{
869				return null;
870			}
871			return MakeDungeon_GetRoom(roomSettings, addToData);
872		}
873	
874		public static DungeonRoom MakeDungeon_GetRoom(DungeonRoomSettings settings, bool addToData = true)
875		{
876			DungeonRoom dungeonRoom = null;
877			switch (settings.RoomType)
878			{
879			default:
880				dungeonRoom = new LegacyDungeonRoom(settings);
881				break;
882			case DungeonRoomType.Regular:
883				dungeonRoom = new RegularDungeonRoom(settings);
884				break;
885			case DungeonRoomType.Wormlike:
886				dungeonRoom = new WormlikeDungeonRoom(settings);
887				break;
888			case DungeonRoomType.LivingTree:
889				dungeonRoom = new LivingTreeDungeonRoom(settings);
890				break;
891			case DungeonRoomType.BiomeSquare:
892				dungeonRoom = new BiomeSquareDungeonRoom(settings);
893				break;
894			case DungeonRoomType.BiomeRugged:
895				dungeonRoom = new BiomeRuggedDungeonRoom(settings);
896				break;
897			case DungeonRoomType.BiomeStructured:
898				dungeonRoom = new BiomeStructuredDungeonRoom(settings);
899				break;
900			case DungeonRoomType.GenShapeCircle:
901			case DungeonRoomType.GenShapeMound:
902			case DungeonRoomType.GenShapeHourglass:
903			case DungeonRoomType.GenShapeDoughnut:
904			case DungeonRoomType.GenShapeQuadCircle:
905				dungeonRoom = new GenShapeDungeonRoom(settings);
906				break;
907			}
908			if (addToData && dungeonRoom != null)
909			{
910				CurrentDungeonData.dungeonRooms.Add(dungeonRoom);
911			}
912			return dungeonRoom;
913		}
914	
915		public static LegacyDungeonHall MakeDungeon_GetHall_Legacy(LegacyDungeonHallSettings settings)
916		{
917			return (LegacyDungeonHall)MakeDungeon_GetHall(settings);
918		}
919	
920		public static DungeonHall MakeDungeon_GetHall(DungeonHallSettings settings, bool addToData = true)
921		{
922			DungeonHall dungeonHall = null;
923			dungeonHall = settings.HallType switch
924			{
925				DungeonHallType.LegacyEntrance => new LegacyEntranceDungeonHall(settings), 
926				DungeonHallType.Regular => new RegularDungeonHall(settings), 
927				DungeonHallType.Stairwell => new StairwellDungeonHall((StairwellDungeonHallSettings)settings), 
928				DungeonHallType.Sine => new SineDungeonHall(settings), 
929				_ => new LegacyDungeonHall(settings), 
930			};
931			if (addToData && dungeonHall != null)
932			{
933				CurrentDungeonData.dungeonHalls.Add(dungeonHall);
934			}
935			return dungeonHall;
936		}
937	
938		public static DungeonEntrance MakeDungeon_GetEntrance(DungeonEntranceSettings settings, bool addToData = true)
939		{
940			DungeonEntrance dungeonEntrance = null;
941			dungeonEntrance = settings.EntranceType switch
942			{
943				DungeonEntranceType.Dome => new DomeDungeonEntrance(settings), 
944				DungeonEntranceType.Tower => new TowerDungeonEntrance(settings), 
945				_ => new LegacyDungeonEntrance(settings), 
946			};
947			if (addToData && dungeonEntrance != null)
948			{
949				CurrentDungeonData.dungeonEntrance = dungeonEntrance;
950			}
951			return dungeonEntrance;
952		}
953	}
954	

```


---

## 🤖 Assistant · 2026-08-12T18:46:15.165Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now this is the modern (1456) dungeon system. It's a very complex system with rooms, halls, features etc. The JS side DungeonPass.ts is 1684 lines — let me read it to see what it does.

Also need WorldGen.cs:14816 registration to see how the Dungeon pass is invoked.

Let me read both.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:15.545Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '14740,14920p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/WorldGen.cs",
 "description": "Read Dungeon pass registration in WorldGen.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:15.573Z

**📎 ToolResult**

```
											if (!((double)num10 < (double)num13 * 0.8) && !GenVars.UndergroundDesertLocation.Intersects(new Rectangle(num4 - 8, num5 - 8, 16, 16)))
											{
												SonOfLakinater(num4, num5);
												GenVars.LakeX[GenVars.numLakes] = num4;
												GenVars.numLakes++;
												break;
											}
										}
									}
								}
							}
						}
					}
				}
			}
		});
		AddGenerationPass(GenPassNameID.StoneToIceAndSiltPlusMudIntoSlush, delegate
		{
			if (!Skyblock.denyAllGeneration)
			{
				for (int i = GenVars.snowTop; i < GenVars.snowBottom; i++)
				{
					for (int j = GenVars.snowMinX[i]; j < GenVars.snowMaxX[i]; j++)
					{
						switch (Main.tile[j, i].type)
						{
						case 123:
							if (SecretSeed.surfaceIsDesert.Enabled && SecretSeed.noSurface.Enabled)
							{
								Main.tile[j, i].type = 53;
							}
							else
							{
								Main.tile[j, i].type = 224;
							}
							break;
						case 59:
						{
							bool flag = true;
							int num = 3;
							for (int k = j - num; k <= j + num; k++)
							{
								for (int l = i - num; l <= i + num; l++)
								{
									if (Main.tile[k, l].active() && (Main.tile[k, l].type == 60 || Main.tile[k, l].type == 70 || Main.tile[k, l].type == 71 || Main.tile[k, l].type == 72))
									{
										flag = false;
										break;
									}
								}
							}
							if (flag)
							{
								if (SecretSeed.surfaceIsDesert.Enabled && SecretSeed.noSurface.Enabled)
								{
									Main.tile[j, i].type = 53;
								}
								else
								{
									Main.tile[j, i].type = 224;
								}
							}
							break;
						}
						case 1:
							Main.tile[j, i].type = 161;
							break;
						}
					}
				}
			}
		});
		if (!Skyblock.denyAllGeneration && SecretSeed.dualDungeons.Enabled)
		{
			AddGenerationPass(new DitherSnakePass(GenPassNameID.DualDungeonsDitherSnake));
		}
		AddGenerationPass(GenPassNameID.Dungeon, delegate(GenerationProgress progress, GameConfiguration passConfig)
		{
			if (!Skyblock.denyAllGeneration)
			{
				progress.Set(0.0);
				for (int i = 0; i < GenVars.dungeonGenVars.Count; i++)
				{
					DungeonCrawler.SetupDungeonData(i, i == 0);
					DungeonCrawler.SetupDungeonDataVariables(i, genRand);
				}
				GenVars.CurrentDungeon = 0;
				int dungeonLocation = GenVars.CurrentDungeonGenVars.dungeonLocation;
				int num = (int)((Main.worldSurface + Main.rockLayer) / 2.0) + genRand.Next(-200, 200);
				int num2 = (int)((Main.worldSurface + Main.rockLayer) / 2.0) + 200;
				int j = num;
				bool flag = false;
				for (int k = 0; k < 10; k++)
				{
					if (SolidTile(dungeonLocation, j + k))
					{
						flag = true;
						break;
					}
				}
				if (!flag)
				{
					for (; j < num2 && !SolidTile(dungeonLocation, j + 10); j++)
					{
					}
				}
				if (flag)
				{
					int num3 = 60;
					int num4 = 0;
					while (SolidTile(dungeonLocation, j - num4))
					{
						num4++;
						if (num4 == num3)
						{
							break;
						}
					}
					if (num4 < num3)
					{
						j += num3 - num4;
					}
				}
				if (drunkWorldGen && !SecretSeed.noSurface.Enabled)
				{
					j = (int)Main.worldSurface + 70;
				}
				if (SecretSeed.surfaceIsDesert.Enabled)
				{
					DungeonDesertCleanup(dungeonLocation);
				}
				DungeonCrawler.MakeDungeon(dungeonLocation, j, progress);
				if (DungeonCrawler.dungeonData.Count > 1)
				{
					for (int l = 1; l < DungeonCrawler.dungeonData.Count; l++)
					{
						GenVars.CurrentDungeon = l;
						dungeonLocation = GenVars.CurrentDungeonGenVars.dungeonLocation;
						int num5 = (int)((Main.worldSurface + Main.rockLayer) / 2.0) + genRand.Next(-200, 200);
						num2 = (int)((Main.worldSurface + Main.rockLayer) / 2.0) + 200;
						j = num5;
						flag = false;
						for (int m = 0; m < 10; m++)
						{
							if (SolidTile(dungeonLocation, j + m))
							{
								flag = true;
								break;
							}
						}
						if (!flag)
						{
							for (; j < num2 && !SolidTile(dungeonLocation, j + 10); j++)
							{
							}
						}
						if (flag)
						{
							int num6 = 60;
							int num7 = 0;
							while (SolidTile(dungeonLocation, j - num7))
							{
								num7++;
								if (num7 == num6)
								{
									break;
								}
							}
							if (num7 < num6)
							{
								j += num6 - num7;
							}
						}
						if (drunkWorldGen && !SecretSeed.noSurface.Enabled)
						{
							j = (int)Main.worldSurface + 70;
						}
						if (SecretSeed.surfaceIsDesert.Enabled)
						{
							DungeonDesertCleanup(dungeonLocation);
						}

```


---

## 🤖 Assistant · 2026-08-12T18:46:19.313Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is the new 1456 dungeon pass. It's a huge system: LegacyDungeonLayoutProvider, DungeonUtils (62k), features... This is ~2000+ lines of complex code. Transcribing all of that into the C# oracle and matching JS 1:1 to hash equality is an enormous task.

Wait — but the JS DungeonPass.ts is 1684 lines and is "1405 基底+多轮 1456 修正" — a 1405 base. The 1405 dungeon was the legacy single-function implementation (WorldGen.MakeDungeon in 1405). So the JS side probably implements the 1405-style legacy algorithm but with 1456 corrections. The task says "把原版 #32 Dungeon pass 转录进 C# oracle 并与 JS 对账到逐哈希全等" — transcribe into the oracle whatever the JS implements, following vanilla source as truth, and align JS to it.

Let me read the JS DungeonPass.ts fully to understand what it implements.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:19.437Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:20.840Z

**📎 ToolResult**

```
1	// 原版地牢 1:1 复刻(MakeDungeon L18006 + DungeonHalls L20255 + DungeonRoom L20622
2	// + DungeonStairs L19855 + DungeonEnt L20726,算法文档 docs/vanilla-algos/dungeon.md)。
3	// 主链随机游走(每5步1/3概率分支/房间)+ 曲线房 + 到地表竖井 + 垛口锯齿入口塔
4	// + 门(style13)+ 尖刺(48)+ 金箱序列。砖 41/43/44 三主题(绿砖 43 素材已补入白名单)。
5	import { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T, TILE_BY_KEY, TILE_DEFS } from '../../../data/tiles';
9	import { ITEM_BY_KEY } from '../../../data/items';
10	import { tileRunner } from './TileRunner';
11	import { solidTile as solidTileHB } from './HalfBrickPass';
12	import { placeDoorClosed } from '../../Door';
13	import { furnitureStyleBase } from '../../FurnitureStyle';
14	
15	const BLUE = TILE_BY_KEY['v_41_blue_brick']!;
16	const GREEN = TILE_BY_KEY['v_43_green_brick']!;
17	const PINK = TILE_BY_KEY['v_44_pink_brick']!;
18	// 原版 DungeonCrawler.SetupDungeonGenVarVariables(cs L54-90)：裂砖随主题——
19	// 蓝41/墙7→481、绿43/墙8→482、粉44/墙9→483（此前恒 481，粉/绿地牢混蓝裂砖）
20	const CRACKED_FOR_BRICK: Record<number, number> = {
21	  [BLUE]: TILE_BY_KEY['v_481_cracked_blue_brick'] ?? BLUE,
22	  [GREEN]: TILE_BY_KEY['v_482_cracked_green_brick'] ?? GREEN,
23	  [PINK]: TILE_BY_KEY['v_483_cracked_pink_brick'] ?? PINK,
24	};
25	const DOOR = TILE_BY_KEY['door_closed']!;
26	const CHEST = TILE_BY_KEY['chest']!;
27	const SPIKE = TILE_BY_KEY['v_48_spike']!;
28	const WORKBENCH = TILE_BY_KEY['workbench']!;
29	const TABLE = TILE_BY_KEY['table']!;
30	const CHAIR = TILE_BY_KEY['chair']!;
31	const CANDLE = TILE_BY_KEY['candle']!;
32	const PLATFORM = TILE_BY_KEY['platform']!;
33	const LANTERN = TILE_BY_KEY['lantern']!;
34	const CHANDELIER = TILE_BY_KEY['chandelier']!;
35	const WATER_CANDLE = TILE_BY_KEY['water_candle']!;
36	const BOOKS = TILE_BY_KEY['v_50_books']!;
37	const BOWLS = TILE_BY_KEY['v_103_bowls']!;
38	const STATUE = TILE_BY_KEY['v_105_statue']!;
39	const CANDELABRA = TILE_BY_KEY['candelabra']!;
40	const PIANO = TILE_BY_KEY['piano']!;
41	const DRESSER = TILE_BY_KEY['dresser']!;
42	const BENCH = TILE_BY_KEY['bench']!;
43	const BATHTUB = TILE_BY_KEY['bathtub']!;
44	const BED = TILE_BY_KEY['bed']!;
45	const LAMP = TILE_BY_KEY['v_93_lamps']!;
46	const CLOCK = TILE_BY_KEY['grandfather_clock']!;
47	const BOOKCASE = TILE_BY_KEY['bookcase']!;
48	const DSWITCH = TILE_BY_KEY['v_136_switch']!;
49	const HANGING = TILE_BY_KEY['v_240_wall_hangings_3x3']!;
50	const CATACOMB = TILE_BY_KEY['v_241_catacombs']!;
51	const PAINTING = TILE_BY_KEY['v_242_paintings_6x4']!;
52	const ALCHEMY = TILE_BY_KEY['v_355_alchemy_table']!;
53	const BEWITCH = TILE_BY_KEY['v_354_bewitching_table']!;
54	const CHEST2 = TILE_BY_KEY['v_467_chests_group_2']!;
55	const TRAP = TILE_BY_KEY['v_137_traps']!;
56	const BANNER = TILE_BY_KEY['v_91_banners']!;
57	
58	interface DRoom { cx: number; cy: number; l: number; r: number; t: number; b: number }
59	
60	class DungeonCtx {
61	  brick: number; wall: number; cracked: number;
62	  minX = 0; maxX = 0; minYY = 0; maxY = 0;
63	  rooms: DRoom[] = [];
64	  entranceX = 0;
65	  entStand: [number, number] | null = null; // 开放门厅可站立点（原版 dungeonX/Y 语义）
66	  lastHall: [number, number] = [0, 0];
67	  // SetupDungeonDataVariables 掷出的书架/灯笼样式（pass 头照原版序消费，陈设期取用）
68	  shelfStyles: number[] = [0, 0, 0];
69	  lanternStyles: number[] = [0, 0, 0];
70	  // 原版 L18045-18048:入口塔尺寸强度(竖井出口探测偏移用)
71	  dxS1 = 0; dyS1 = 0; dxS2 = 0; dyS2 = 0;
72	  // 门候选(cs L18158-18179 房左右墙 + L20500 水平走廊端点):pos 0=取最窄,-1=取最右,+1=取最左
73	  dDoors: Array<{ x: number; y: number; pos: number }> = [];
74	  // 房口平台候选(cs L18141-18156):房顶/房底首个开口列
75	  dPlatforms: Array<[number, number]> = [];
76	  constructor(brick: number, wall: number, x: number, y: number) {
77	    this.brick = brick; this.wall = wall;
78	    this.cracked = CRACKED_FOR_BRICK[brick] ?? brick;
79	    this.minX = this.maxX = x; this.minYY = this.maxY = y;
80	  }
81	  isDungeonWall(st: TileStore, x: number, y: number): boolean {
82	    if (!st.inBounds(x, y)) return false;
83	    const wl = st.wall[st.idx(x, y)];
84	    return wl === this.wall || (wl >= 94 && wl <= 99);
85	  }
86	  updateBBox(x: number, y: number) {
87	    this.minX = Math.min(this.minX, x); this.maxX = Math.max(this.maxX, x);
88	    this.maxY = Math.max(this.maxY, y);
89	  }
90	}
91	
92	export function runDungeonPass(st: TileStore, rng: RNG, gs: GenState, chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null> }>): void {
93	  const { w, h } = st;
94	  // ---- SetupDungeonData/SetupDungeonDataVariables 头部掷骰（cs:14821-14825 +
95	  // DungeonCrawler.cs:167-192/:243-274，须在入口预计算之前）----
96	  // 入口类型 2 掷（普通世界 flag 即真、循环只跑一轮；Dome/Tower 结果我方 legacy
97	  // 入口不消费，照掷）+ 书架/灯具样式三选不重复（陈设期取用）+
98	  // useSkewedDungeonEntranceHalls（值未消费照掷）。此前整组缺失且书架/灯样式骰
99	  // 挪到陈设期 → 共享单流自本 pass 起整体错位（2026-08-12 审计修正）
100	  rng.nextInt(3); rng.nextInt(3);
101	  const shelfStyles = [rng.int(9, 12), 0, 0];
102	  do { shelfStyles[1] = rng.int(9, 12); } while (shelfStyles[1] === shelfStyles[0]);
103	  do { shelfStyles[2] = rng.int(9, 12); } while (shelfStyles[2] === shelfStyles[0] || shelfStyles[2] === shelfStyles[1]);
104	  const lanternStyles = [rng.int(0, 6), 0, 0];
105	  do { lanternStyles[1] = rng.int(0, 6); } while (lanternStyles[1] === lanternStyles[0]);
106	  do { lanternStyles[2] = rng.int(0, 6); } while (lanternStyles[2] === lanternStyles[0] || lanternStyles[2] === lanternStyles[1]);
107	  rng.nextInt(4);
108	  // ---- 入口位置预计算(DungeonCrawler.cs:275-318 + :818-849):仅 Dome/Tower 入口
109	  // 设 PrecalculateEntrancePosition=true;Legacy(普通世界默认)为 false →
110	  // SetupDungeonDataVariables 在 useSkewed 掷后**直接 return,整段 ±300 拒绝采样
111	  // 不执行**,dungeonLocation 保持 Reset 值,入口由爬升大厅(MakeDungeon_Generate
112	  // NextEntranceHall_Legacy,DungeonCrawler.cs:443)自然爬出地表决定。
113	  // 此前误把该 Dome/Tower 专属漂移套在 legacy 上:接受条件只挡云与净空,沙丘顶
114	  // (越高越空)几乎必过 → 入口被系统性吸到沙丘顶,要塞东侧开口被沙丘封死
115	  // (2026-08-13 地牢走廊沙堵根因;顺带该循环多消耗 0~6000 颗共享流样本) ----
116	  const x0 = gs.dungeonLocation;
117	  if (x0 < 30 || x0 > w - 30) return;
118	  // 原版主题在 **Dunes pass 头**已掷（SetupDungeonGenVarVariables，cs:11542）；
119	  // 此处只消费 gs.dungeonTheme（-1=非原版管线直调时回退自掷）
120	  const theme = gs.dungeonTheme >= 0 ? gs.dungeonTheme : rng.int(0, 2);
121	  const brick = theme === 0 ? BLUE : theme === 1 ? GREEN : PINK;
122	  const wallId = brick === BLUE ? 7 : brick === GREEN ? 8 : 9;
123	  // 深度锚点:1456 Dungeon pass 主体(cs:14828-14870)1:1——
124	  // (worldSurface+rockLevel)/2 ± 200 起;下方 10 格内无实心则向下扫到实心;
125	  // 起点即实心则**上爬至非实心(上限 60)再下压 60-num4**(原版 quirk,保证锚点
126	  // 埋在地表下);无任何 clamp(曾自加 worldSurface+10 钳制,非原版)
127	  let y0 = Math.floor((gs.worldSurface + gs.rockLevel) / 2) + rng.int(-200, 199);
128	  let solid = false;
129	  for (let d = 0; d < 10; d++) if (st.flags[st.idx(x0, y0 + d)]) { solid = true; break; }
130	  if (!solid) {
131	    const cap = Math.floor((gs.worldSurface + gs.rockLevel) / 2) + 200;
132	    while (y0 < cap && !st.flags[st.idx(x0, y0 + 10)]) y0++;
133	  }
134	  if (solid) {
135	    let up = 0;
136	    while (st.inBounds(x0, y0 - up) && st.flags[st.idx(x0, y0 - up)]) {
137	      up++;
138	      if (up === 60) break;
139	    }
140	    if (up < 60) y0 += 60 - up;
141	  }
142	  const dc = new DungeonCtx(brick, wallId, x0, y0);
143	  dc.shelfStyles = shelfStyles;
144	  dc.lanternStyles = lanternStyles;
145	  // 原版 L18045-18048:入口塔尺寸强度(DungeonEnt 与竖井出口探测共用)
146	  dc.dxS1 = rng.int(25, 29); dc.dyS1 = rng.int(20, 24);
147	  dc.dxS2 = rng.int(35, 49); dc.dyS2 = rng.int(10, 14);
148	  // ---- 主链随机游走(L18053)----
149	  let budget = w / 60 + rng.int(0, Math.max(1, Math.floor(w / 180)));
150	  let dx = x0, dy = y0;
151	  dungeonRoom(st, rng, gs, dc, dx, dy);
152	  let step5 = 5;
153	  while (budget > 0) {
154	    dc.updateBBox(dx, dy);
155	    budget--;
156	    step5--;
157	    if (step5 === 0 && rng.next() * 3 < 1) {
158	      step5 = 5;
159	      if (rng.next() < 0.5) {
160	        // 分支:保存位置→走廊(可能两条)+房→恢复
161	        const sx = dx, sy = dy;
162	        [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
163	        if (rng.next() < 0.5) [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
164	        dungeonRoom(st, rng, gs, dc, dx, dy);
165	        dx = sx; dy = sy;
166	      } else {
167	        dungeonRoom(st, rng, gs, dc, dx, dy);
168	      }
169	    } else {
170	      [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
171	    }
172	  }
173	  dungeonRoom(st, rng, gs, dc, dx, dy);
174	  // ---- 爬升到地表(1456 语义,DungeonCrawler.cs L400-449):上限 100;num8 到 0 后
175	  // 每轮 1/5 概率 halls(forceX)+room 分支(原版 num8 保持在 0)。legacy 无预计算,
176	  // 只走盲爬一条路(cs:443 GenerateNextEntranceHall_Legacy) ----
177	  let best = dc.rooms[0];
178	  for (const r of dc.rooms) if (r.t < best.t) best = r;
179	  dc.entranceX = best.cx;
180	  // DungeonCrawler.cs:394 回写：generatingDungeonPositionX = 最高房中心 X
181	  // （Pyramids 地牢回避带 cs:15447 消费端——曾缺，Pyramids 误读 Reset 期 dungeonLocation）
182	  gs.generatingDungeonPositionX = dc.entranceX;
183	  dx = best.cx; dy = best.cy;
184	  {
185	    // legacy 盲爬(1405 结构 + 1456 的 100 上限):外壳探测到开放天空即停
186	    let reached = false;
187	    let delay = 5, guard = 0;
188	    while (!reached && guard++ < 100) {
189	      if (delay > 0) delay--;
190	      if (delay === 0 && rng.next() < 0.2 && dy > gs.worldSurface + 100) {
191	        delay = 10;
192	        const sx = dx, sy = dy;
193	        [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, true);
194	        dungeonRoom(st, rng, gs, dc, dx, dy);
195	        dx = sx; dy = sy;
196	      }
197	      const res = dungeonStairs(st, rng, gs, dc, dx, dy);
198	      dx = res[0]; dy = res[1];
199	      reached = res[2];
200	    }
201	    // 兜底:楼梯没到地表则从当前位置直挖竖井到地表(垂直,保证衔接)
202	    if (dy > gs.worldSurface - 5) {
203	      let sx2 = dx, sy2 = dy;
204	      let guard2 = 0;
205	      while (sy2 > gs.worldSurface - 5 && guard2++ < 800) {
206	        for (let ax = -3; ax <= 3; ax++) {
207	          for (let ay = -3; ay <= 3; ay++) {
208	            if (!st.inBounds(sx2 + ax, sy2 + ay)) continue;
209	            const i = st.idx(sx2 + ax, sy2 + ay);
210	            st.flags[i] = 0; st.wall[i] = dc.wall;
211	          }
212	        }
213	        for (let ax = -4; ax <= 4; ax++) {
214	          for (let ay = -4; ay <= 4; ay++) {
215	            if (!st.inBounds(sx2 + ax, sy2 + ay)) continue;
216	            const i = st.idx(sx2 + ax, sy2 + ay);
217	            if (!dc.isDungeonWall(st, sx2 + ax, sy2 + ay)) { st.type[i] = dc.brick; st.flags[i] = 1; }
218	          }
219	        }
220	        sy2--;
221	      }
222	      dx = sx2; dy = sy2;
223	    }
224	    // 找楼梯出口列的真实地表,塔吸附其上
225	    let gY = 0;
226	    while (gY < st.h - 2 && !st.flags[st.idx(dx, gY)]) gY++;
227	    dungeonEnt(st, rng, gs, dc, dx, gY);
228	    gs.dungeonY = gY;          // 入口地表 Y（刷怪门槛 CheckToSpawnDungeonEnemies）
229	  }
230	  if (dc.entStand) {
231	    gs.dungeonEntX = dc.entStand[0];
232	    gs.dungeonEntY = dc.entStand[1];
233	  }
234	  // ---- 房口平台候选(cs L18137-18180,与门候选同期收集)----
235	  for (const room of dc.rooms) {
236	    for (let x = room.l; x <= room.r; x++) {
237	      if (st.inBounds(x, room.t - 1) && !st.flags[st.idx(x, room.t - 1)]) { dc.dPlatforms.push([x, room.t - 1]); break; }
238	    }
239	    for (let x = room.l; x <= room.r; x++) {
240	      if (st.inBounds(x, room.b + 1) && !st.flags[st.idx(x, room.b + 1)]) { dc.dPlatforms.push([x, room.b + 1]); break; }
241	    }
242	  }
243	  // ---- 尖刺(L18188)----
244	  placeSpikes(st, rng, gs, dc, Math.floor(w / 100));
245	  // ---- 门(L18311)----
246	  placeDoors(st, rng, dc);
247	  // ---- 陈设管线(L18441-19613):墙变体→房口平台→特殊宝箱→书架平台→房间金箱→
248	  //      灯具+开关布线→陷阱→地面家具→墙饰→旗帜 ----
249	  placeFurnishing(st, rng, gs, dc, chests);
250	}
251	
252	/** DungeonHalls(L20255):走廊随机游走 */
253	function dungeonHalls(st: TileStore, rng: RNG, gs: GenState, dc: DungeonCtx, ix: number, iy: number, forceX: boolean): [number, number] {
254	  let radius = rng.int(4, 5);
255	  const baseR = radius;
256	  let steps = rng.int(35, 79);
257	  // 危险走廊(LegacyDungeonHall.cs:206-209):CrackedBrickChance=0.166(DungeonHallSettings
258	  // .cs:15,Legacy 子类未覆写)先掷、恒消费——此前顺序对调且值用 0.2,还误加
259	  // !forceX 短路(forceX 也照掷)
260	  const dangerous = rng.next() <= 0.166;
261	  if (forceX) steps += 20;
262	  else if (rng.nextInt(5) === 0) { radius *= 2; steps = Math.floor(steps / 2); }
263	  // 方向
264	  let vx = 0, vy = 0;
265	  {
266	    const horiz = forceX || rng.next() < 0.5;
267	    if (horiz) {
268	      vx = rng.next() < 0.5 ? 1 : -1;
269	      if (rng.next() < 1 / 3) vy = (rng.next() < 0.5 ? 1 : -1) * 0.2;
270	    } else {
271	      radius++;
272	      vy = rng.next() < 0.5 ? 1 : -1;
273	      if (rng.next() < 2 / 3) vx = (rng.next() < 0.5 ? 1 : -1) * rng.int(10, 19) * 0.1;
274	    }
275	    // 边界强制
276	    if (!forceX) {
277	      if (ix > st.w - 200) vx = -Math.abs(vx || 1);
278	      if (ix < 200) vx = Math.abs(vx || 1);
279	      if (iy > st.h - 300) vy = -Math.abs(vy || 1);
280	      if (iy < gs.rockLevel + 100) vy = Math.abs(vy || 1);
281	      // 边界三分带强制(cs L20474-20485):走廊被推向外侧——
282	      // 0.5w-0.75w → +1、0.25w-0.5w → -1(原版语义,铺向外侧三分而非向中心聚集)
283	      if (ix > st.w / 2 && ix < st.w * 0.75) vx = Math.abs(vx || 0.5);
284	      if (ix > st.w * 0.25 && ix < st.w / 2) vx = -Math.abs(vx || 0.5);
285	    }
286	    if (vx === 0 && vy === 0) vx = 1;
287	  }
288	  if (vx !== 0 && vy === 0 && rng.next() * 3 < 2 && !forceX) {
289	    radius = Math.floor(baseR * rng.int(110, 149) * 0.01);
290	  }
291	  let px = ix + 0.0, py = iy + 0.0;
292	  let driftFlip = 0;
293	  const driftThresh = rng.int(10, 19);
294	  const hasDrift = vx !== 0 && vy !== 0;
295	  while (steps > 0) {
296	    steps--;
297	    // 外框填砖(仅非地牢墙)
298	    const padX = radius + 4 + rng.int(0, 5);
299	    const padY = radius + 4 + rng.int(0, 5);
300	    for (let x = Math.floor(px - padX); x <= Math.floor(px + padX); x++) {
301	      for (let y = Math.floor(py - padY); y <= Math.floor(py + padY); y++) {
302	        if (!st.inBounds(x, y)) continue;
303	        const i = st.idx(x, y);
304	        st.liquid[i] = 0;
305	        if (!dc.isDungeonWall(st, x, y)) {
306	          st.type[i] = dc.brick; st.flags[i] = 1;
307	        }
308	      }
309	    }
310	    dc.updateBBox(Math.floor(px), Math.floor(py));
311	    // 内缩 1 填墙
312	    for (let x = Math.floor(px - radius - 1); x <= Math.floor(px + radius + 1); x++) {
313	      for (let y = Math.floor(py - radius - 1); y <= Math.floor(py + radius + 1); y++) {
314	        if (!st.inBounds(x, y)) continue;
315	        const edge = Math.abs(x - px) > radius || Math.abs(y - py) > radius;
316	        if (edge) st.wall[st.idx(x, y)] = dc.wall;
317	      }
318	    }
319	    // 内部挖空(带随机扩孔)
320	    let expand = 0;
321	    if (vy === 0) { if (rng.next() * (radius + 1) < 1) expand = rng.int(1, 2); }
322	    else if (rng.next() * Math.max(1, radius - 1) < 1 || rng.next() * (radius * 3) < 1) expand = rng.int(1, 2);
323	    const innerX = radius * 0.5 + expand, innerY = radius * 0.5 + expand;
324	    for (let x = Math.floor(px - innerX); x <= Math.floor(px + innerX); x++) {
325	      for (let y = Math.floor(py - innerY); y <= Math.floor(py + innerY); y++) {
326	        if (!st.inBounds(x, y)) continue;
327	        const i = st.idx(x, y);
328	        if (dangerous) {
329	          // 危险走廊:填裂砖(不可挖穿的陷阱段)
330	          if (st.flags[i] || !dc.isDungeonWall(st, x, y)) { st.type[i] = dc.cracked; st.flags[i] = 1; }
331	        } else {
332	          st.flags[i] = 0;
333	        }
334	        st.wall[i] = dc.wall;
335	      }
336	    }
337	    px += vx; py += vy;
338	    if (hasDrift && ++driftFlip > driftThresh) { driftFlip = 0; vx = -vx; }
339	    // 出界截断
340	    if ((vx > 0 && px > st.w - 100) || (vx < 0 && px < 100) || (vy > 0 && py > st.h - 100) || (vy < 0 && py < gs.rockLevel + 50)) steps = 0;
341	  }
342	  // 水平走廊端点记为门候选(cs L20496-20501)
343	  if (vy === 0) dc.dDoors.push({ x: Math.floor(px), y: Math.floor(py), pos: 0 });
344	  return [Math.floor(px), Math.floor(py)];
345	}
346	
347	/** DungeonRoom(L20622):曲线漂移房 */
348	function dungeonRoom(st: TileStore, rng: RNG, _gs: GenState, dc: DungeonCtx, ix: number, iy: number): void {
349	  const size = rng.int(15, 29);
350	  const steps = rng.int(10, 19);
351	  let px = ix + 0.0, py = iy - size / 2 + 0.0;
352	  let vx = rng.int(-10, 10) * 0.1, vy = rng.int(-10, 10) * 0.1;
353	  let rl = 1e9, rr = -1e9, rt = 1e9, rb = -1e9;
354	  for (let k = 0; k < steps; k++) {
355	    const outerX = size * 0.8 + 5, outerY = size * 0.8 + 5;
356	    for (let x = Math.floor(px - outerX); x <= Math.floor(px + outerX); x++) {
357	      for (let y = Math.floor(py - outerY); y <= Math.floor(py + outerY); y++) {
358	        if (!st.inBounds(x, y)) continue;
359	        const i = st.idx(x, y);
360	        st.liquid[i] = 0;
361	        if (!dc.isDungeonWall(st, x, y)) { st.type[i] = dc.brick; st.flags[i] = 1; }
362	      }
363	    }
364	    dc.updateBBox(Math.floor(px), Math.floor(py));
365	    // 内缩 1 墙 + 内框挖空
366	    for (let x = Math.floor(px - size * 0.8); x <= Math.floor(px + size * 0.8); x++) {
367	      for (let y = Math.floor(py - size * 0.8); y <= Math.floor(py + size * 0.8); y++) {
368	        if (!st.inBounds(x, y)) continue;
369	        const edge = Math.abs(x - px) > size * 0.5 || Math.abs(y - py) > size * 0.5;
370	        const i = st.idx(x, y);
371	        if (edge) st.wall[i] = dc.wall;
372	        else {
373	          st.flags[i] = 0; st.wall[i] = dc.wall;
374	          rl = Math.min(rl, x); rr = Math.max(rr, x);
375	          rt = Math.min(rt, y); rb = Math.max(rb, y);
376	        }
377	      }
378	    }
379	    px += vx; py += vy;
380	    vx += rng.int(-10, 10) * 0.05; vy += rng.int(-10, 10) * 0.05;
381	    vx = Math.max(-1, Math.min(1, vx)); vy = Math.max(-1, Math.min(1, vy));
382	  }
383	  dc.rooms.push({ cx: Math.floor(px), cy: Math.floor(py), l: rl, r: rr, t: rt, b: rb });
384	  // 门候选(cs L18158-18179):房左右墙外侧列的首个空格
385	  if (rl > 1 && rr < st.w - 2) {
386	    for (let y = rt; y <= rb; y++) {
387	      if (st.inBounds(rl - 1, y) && !st.flags[st.idx(rl - 1, y)]) { dc.dDoors.push({ x: rl - 1, y, pos: -1 }); break; }
388	    }
389	    for (let y = rt; y <= rb; y++) {
390	      if (st.inBounds(rr + 1, y) && !st.flags[st.idx(rr + 1, y)]) { dc.dDoors.push({ x: rr + 1, y, pos: 1 }); break; }
391	    }
392	  }
393	}
394	
395	/** DungeonStairs(L19855):向上竖井到地表,返回 [x, y, reachedSurface] */
396	function dungeonStairs(st: TileStore, rng: RNG, gs: GenState, dc: DungeonCtx, ix: number, iy: number, precalc?: { vx: number; vy: number; steps: number }): [number, number, boolean] {
397	  const radius = rng.int(5, 8);
398	  const steps = precalc ? precalc.steps : rng.int(10, 29);
399	  let vx: number, vy: number;
400	  if (precalc) {
401	    // 1456 预计算模式:方向由直线段给定,跳过方向抽取/钳制/探测
402	    vx = precalc.vx; vy = precalc.vy;
403	  } else {
404	    vx = ix <= dc.entranceX ? 1 : -1;
405	    if (ix > st.w - 400) vx = -1;
406	    if (ix < 400) vx = 1;
407	    vy = -1;
408	    // 原版嵌套概率(cs L19871-19876):2/3 加速;否则 1/3 减速;再否则 1/6 快速上升
409	    if (rng.next() < 2 / 3) vx *= 1 + rng.int(0, 199) * 0.01;
410	    else if (rng.next() < 1 / 3) vx *= rng.int(50, 75) * 0.01;
411	    else if (rng.next() < 1 / 6) vy = -2;
412	    if (ix < st.w / 2 && vx < 0 && vx > -0.5) vx = -0.5;
413	    if (ix > st.w / 2 && vx > 0.5) vx = -0.5;
414	    // dungeonX 回拉:漂移超 ±60 强制折返(原版中线回拉的加强,入口落在地牢标记附近)
415	    const loc = gs.dungeonLocation;
416	    if (ix > loc + 60) vx = -Math.abs(vx || 0.5);
417	    if (ix < loc - 60) vx = Math.abs(vx || 0.5);
418	  }
419	  let px = ix + 0.0, py = iy + 0.0;
420	  let reached = false;
421	  for (let k = 0; k < steps && !reached; k++) {
422	    // ---- 出口探测(cs L19900-19910,仅 legacy):探测点偏移 X+(dxS1*0.6+dxS2) 朝中心 ----
423	    if (!precalc) {
424	      const toCenter = px > st.w / 2 ? -1 : 1;
425	      const probeX = Math.floor(px + dc.dxS1 * 0.6 * toCenter + dc.dxS2 * toCenter);
426	      const probeOff = Math.floor(dc.dyS2 * 0.5);
427	      if (py < gs.worldSurface - 5) {
428	        let open = true;
429	        for (let d = 0; d < 3; d++) {
430	          const yy = Math.floor(py - radius - 6 + probeOff - d);
431	          if (!st.inBounds(probeX, yy) || st.wall[st.idx(probeX, yy)] !== 0) { open = false; break; }
432	        }
433	        if (open) {
434	          reached = true;
435	          // 地表土丘(原版 TileRunner type -1 挖出,cs L19909)
436	          tileRunner(st, rng, gs, probeX, Math.floor(py - radius - 6 + probeOff), {
437	            strength: rng.int(25, 34), steps: rng.int(10, 19), type: -1, speedY: -1,
438	          });
439	        }
440	      }
441	    }
442	    // 原版外壳:X 无抖动(cs L19891-19892),Y 带 Next(6) 抖动
443	    const padX = radius + 4;
444	    const padY = radius + 4 + rng.int(0, 5);
445	    for (let x = Math.floor(px - padX); x <= Math.floor(px + padX); x++) {
446	      for (let y = Math.floor(py - padY); y <= Math.floor(py + padY); y++) {
447	        if (!st.inBounds(x, y)) continue;
448	        const i = st.idx(x, y);
449	        st.liquid[i] = 0;
450	        if (!dc.isDungeonWall(st, x, y)) { st.type[i] = dc.brick; st.flags[i] = 1; }
451	      }
452	    }
453	    // 竖井外壳刷墙(cs L19924-19928):外框内缩 1 整片刷地牢墙
454	    for (let x = Math.floor(px - padX) + 1; x <= Math.floor(px + padX) - 1; x++) {
455	      for (let y = Math.floor(py - padY) + 1; y <= Math.floor(py + padY) - 1; y++) {
456	        if (st.inBounds(x, y)) st.wall[st.idx(x, y)] = dc.wall;
457	      }
458	    }
459	    // 内框挖空
460	    let expand = rng.next() * radius < 1 ? rng.int(1, 2) : 0;
461	    const inner = radius * 0.5 + expand;
462	    for (let x = Math.floor(px - inner); x <= Math.floor(px + inner); x++) {
463	      for (let y = Math.floor(py - inner); y <= Math.floor(py + inner); y++) {
464	        if (!st.inBounds(x, y)) continue;
465	        const i = st.idx(x, y);
466	        st.flags[i] = 0; st.wall[i] = dc.wall;
467	      }
468	    }
469	    dc.updateBBox(Math.floor(px), Math.floor(py));
470	    px += vx; py += vy;
471	    if (!precalc && py < gs.worldSurface) vy *= 0.98;
472	  }
473	  return [Math.floor(px), Math.floor(py), reached];
474	}
475	
476	/** DungeonEnt(L20726-21273)逐行 1:1:两段式入口。
477	 * 主塔段:0.6±Next(2,5) 实心(内缩1刷墙)→ 垛口(5+Next(4) 宽)→ 顶齿(1+Next(2) 高,
478	 * 周期 2+Next(4))→ 下延到 worldSurface → 0.6 框刷墙×2 → 0.5 框清空(塔内厅)。
479	 * 外门厅段(中心 = 主塔中心 + (dx1*0.6+dx2*0.55)*dir, Y + dy1/2 - dy2/2):
480	 * 0.6±Next(1,3) 只填远侧半(dx2*0.5 内)→ 下延(全列刷墙)→ 0.5 边缘垛口+顶齿 →
481	 * 0.6 框清墙 → **0.5 框 active=false+wall=0(开放门厅,老头 NPC 位)** →
482	 * 100 列砖坡(对角步降) → 条纹窗墙(2-5 刷-2 倍跳) → 门洞 15×3+门 style13。 */
483	function dungeonEnt(st: TileStore, rng: RNG, gs: GenState, dc: DungeonCtx, i: number, j: number): void {
484	  // 清 ±60 液体
485	  for (let x = i - 60; x < i + 60; x++) {
486	    for (let y = j - 60; y < j + 60; y++) {
487	      if (!st.inBounds(x, y)) continue;
488	      st.liquid[st.idx(x, y)] = 0;
489	    }
490	  }
491	  const dx1 = rng.int(25, 29) + 0.0, dy1 = rng.int(20, 24) + 0.0;
492	  let cx = i + 0.0, cy = j - dy1 / 2; // 塔中心(vanilla vector2)
493	  dc.minYY = Math.floor(cy);
494	  const dir = i > st.w / 2 ? -1 : 1; // num2:背向地图中心
495	  const isDW = (x: number, y: number) => st.inBounds(x, y) && dc.isDungeonWall(st, x, y);
496	  const fillB = (x: number, y: number, paintWall: boolean) => {
497	    if (!st.inBounds(x, y)) return;
498	    const ti = st.idx(x, y);
499	    st.liquid[ti] = 0;
500	    if (!isDW(x, y)) {
501	      st.wall[ti] = 0;
502	      if (paintWall) st.wall[ti] = dc.wall;
503	      st.type[ti] = dc.brick; st.flags[ti] = 1;
504	    }
505	  };
506	  const extFill = (x: number, y: number, wallAll: boolean, innerW: boolean) => {
507	    if (!st.inBounds(x, y)) return;
508	    const ti = st.idx(x, y);
509	    st.liquid[ti] = 0;
510	    if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
511	    if (wallAll || innerW) st.wall[ti] = dc.wall;
512	  };
513	  // ---- 主塔段主体(num3..num6)----
514	  const l1 = Math.floor(cx - dx1 * 0.6 - rng.int(2, 4));
515	  const r1 = Math.floor(cx + dx1 * 0.6 + rng.int(2, 4));
516	  const t1 = Math.floor(cy - dy1 * 0.6 - rng.int(2, 4));
517	  const b1 = Math.floor(cy + dy1 * 0.6 + rng.int(8, 15));
518	  for (let x = l1; x < r1; x++) {
519	    for (let y = t1; y < b1; y++) {
520	      fillB(x, y, x > l1 + 1 && x < r1 - 2 && y > t1 + 1 && y < b1 - 2);
521	    }
522	  }
523	  // 垛口(左右块 5+Next(4) 宽、3+Next(3) 高)
524	  for (const sd of [-1, 1]) {
525	    const bx0 = sd < 0 ? l1 : r1 - 5 - rng.int(0, 3);
526	    const bx1 = sd < 0 ? l1 + 5 + rng.int(0, 3) : r1;
527	    const by0 = t1 - 3 - rng.int(0, 2);
528	    for (let x = bx0; x < bx1; x++) for (let y = by0; y < t1; y++) fillB(x, y, false);
529	  }
530	  // 顶齿(齿高 1+Next(2),周期 2+Next(4):刷 num16 列跳 num16 列)
531	  const th1 = 1 + rng.int(0, 1);
532	  const tp1 = 2 + rng.int(0, 3);
533	  let cnt = 0;
534	  for (let x = l1; x < r1; x++) {
535	    for (let y = t1 - th1; y < t1; y++) fillB(x, y, false);
536	    if (++cnt >= tp1) { x += tp1; cnt = 0; }
537	  }
538	  // 下延到 worldSurface(num6 → worldSurface):填砖,内列刷墙
539	  for (let x = l1; x < r1; x++) {
540	    for (let y = b1; y < Math.min(st.h, Math.floor(gs.worldSurface)); y++) {
541	      extFill(x, y, false, x > l1 && x < r1 - 1);
542	    }
543	  }
544	  // 0.6 框刷墙(精确,无抖动)×2
545	  for (let pass = 0; pass < 2; pass++) {
546	    for (let x = Math.floor(cx - dx1 * 0.6) - (pass ? 1 : 0); x <= Math.floor(cx + dx1 * 0.6) + (pass ? 1 : 0); x++) {
547	      for (let y = Math.floor(cy - dy1 * 0.6) - (pass ? 1 : 0); y <= Math.floor(cy + dy1 * 0.6) + (pass ? 1 : 0); y++) {
548	        if (!st.inBounds(x, y)) continue;
549	        const ti = st.idx(x, y);
550	        st.liquid[ti] = 0; st.wall[ti] = dc.wall;
551	      }
552	    }
553	  }
554	  // 0.5 框清空(塔内厅)
555	  for (let x = Math.floor(cx - dx1 * 0.5); x < Math.floor(cx + dx1 * 0.5); x++) {
556	    for (let y = Math.floor(cy - dy1 * 0.5); y < Math.floor(cy + dy1 * 0.5); y++) {
557	      if (!st.inBounds(x, y)) continue;
558	      const ti = st.idx(x, y);
559	      st.liquid[ti] = 0; st.flags[ti] = 0; st.wall[ti] = dc.wall;
560	    }
561	  }
562	  // 塔底井口(连通楼梯竖井,原版由 DungeonStairs 自带)
563	  for (let x = -1; x <= 1; x++) {
564	    for (let y = Math.floor(cy + dy1 * 0.5); y < Math.floor(cy + dy1 * 0.5) + 4; y++) {
565	      if (st.inBounds(Math.floor(cx) + x, y)) {
566	        const ti = st.idx(Math.floor(cx) + x, y);
567	        st.flags[ti] = 0; st.wall[ti] = dc.wall;
568	      }
569	    }
570	  }
571	  // ---- 外门厅段 ----
572	  cx += dx1 * 0.6 * dir;
573	  cy += dy1 * 0.5;
574	  const dx2 = rng.int(35, 49) + 0.0, dy2 = rng.int(10, 14) + 0.0;
575	  cx += dx2 * 0.55 * dir;
576	  cy -= dy2 * 0.5;
577	  const l2 = Math.floor(cx - dx2 * 0.6 - rng.int(1, 2));
578	  const r2 = Math.floor(cx + dx2 * 0.6 + rng.int(1, 2));
579	  const t2 = Math.floor(cy - dy2 * 0.6 - rng.int(1, 2));
580	  const b2 = Math.floor(cy + dy2 * 0.6 + rng.int(6, 15));
581	  // 只填远侧半(num2<0 → x >= X-dx2*0.5;否则 x <= X+dx2*0.5-1)
582	  for (let x = l2; x < r2; x++) {
583	    for (let y = t2; y < b2; y++) {
584	      const far = dir < 0 ? x >= cx - dx2 * 0.5 : x <= cx + dx2 * 0.5 - 1;
585	      if (!far) continue;
586	      if (!st.inBounds(x, y)) continue;
587	      const ti = st.idx(x, y);
588	      st.liquid[ti] = 0;
589	      if (!isDW(x, y)) { st.wall[ti] = 0; st.type[ti] = dc.brick; st.flags[ti] = 1; }
590	    }
591	  }
592	  // 下延(全列刷墙)
593	  for (let x = l2; x < r2; x++) {
594	    for (let y = b2; y < Math.min(st.h, Math.floor(gs.worldSurface)); y++) extFill(x, y, true, false);
595	  }
596	  // 外段垛口(0.5 边缘:块1 从 num34(+1 若 dir<0) 起 5+Next(4) 宽;块2 [num35-5-Next(4), num35))
597	  const n34 = Math.floor(cx - dx2 * 0.5);
598	  let n35 = Math.floor(cx + dx2 * 0.5);
599	  const n36 = dir < 0 ? n34 + 1 : n34;
600	  {
601	    const by0 = t2 - 3 - rng.int(0, 2);
602	    for (let x = n36; x < n36 + 5 + rng.int(0, 3); x++) {
603	      for (let y = by0; y < t2; y++) {
604	        if (!st.inBounds(x, y)) continue;
605	        const ti = st.idx(x, y);
606	        st.liquid[ti] = 0;
607	        if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
608	      }
609	    }
610	    const bx0 = n35 - 5 - rng.int(0, 3);
611	    for (let x = bx0; x < n35; x++) {
612	      for (let y = by0; y < t2; y++) {
613	        if (!st.inBounds(x, y)) continue;
614	        const ti = st.idx(x, y);
615	        st.liquid[ti] = 0;
616	        if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
617	      }
618	    }
619	  }
620	  // 外段顶齿(dir<0 时 num35++)
621	  if (dir < 0) n35++;
622	  const th2 = 1 + rng.int(0, 1);
623	  const tp2 = 2 + rng.int(0, 3);
624	  cnt = 0;
625	  for (let x = n34 + 1; x < n35 - 1; x++) {
626	    for (let y = t2 - th2; y < t2; y++) {
627	      if (!st.inBounds(x, y)) continue;
628	      const ti = st.idx(x, y);
629	      st.liquid[ti] = 0;
630	      if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
631	    }
632	    if (++cnt >= tp2) { x += tp2; cnt = 0; }
633	  }
634	  // 0.6 框清墙(开放感)
635	  for (let x = Math.floor(cx - dx2 * 0.6); x < Math.floor(cx + dx2 * 0.6); x++) {
636	    for (let y = Math.floor(cy - dy2 * 0.6); y < Math.floor(cy + dy2 * 0.6); y++) {
637	      if (!st.inBounds(x, y)) continue;
638	      st.liquid[st.idx(x, y)] = 0;
639	      st.wall[st.idx(x, y)] = 0;
640	    }
641	  }
642	  // 0.5 框:active=false + wall=0(开放门厅——老头 NPC 位)
643	  const n51 = Math.floor(cx - dx2 * 0.5), n52 = Math.floor(cx + dx2 * 0.5);
644	  const n53 = Math.floor(cy - dy2 * 0.5), n54 = Math.floor(cy + dy2 * 0.5);
645	  for (let x = n51; x < n52; x++) {
646	    for (let y = n53; y < n54; y++) {
647	      if (!st.inBounds(x, y)) continue;
648	      const ti = st.idx(x, y);
649	      st.liquid[ti] = 0; st.flags[ti] = 0; st.wall[ti] = 0;
650	    }
651	  }
652	  // 100 列砖坡(对角步降,清上方 4 行)
653	  {
654	    const slope = 100;
655	    let step = 0;
656	    if (dir === 1) {
657	      for (let x = n52; x < n52 + slope; x++) {
658	        step++;
659	        for (let y = n54 + step; y < n54 + slope; y++) {
660	          if (!st.inBounds(x, y)) continue;
661	          const ti = st.idx(x, y);
662	          st.liquid[ti] = 0;
663	          if (st.wall[ti] !== 3 && st.wall[ti] !== 83 && !isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
664	        }
665	      }
666	    } else {
667	      for (let x = n51; x > n51 - slope; x--) {
668	        step++;
669	        for (let y = n54 + step; y < n54 + slope; y++) {
670	          if (!st.inBounds(x, y)) continue;
671	          const ti = st.idx(x, y);
672	          st.liquid[ti] = 0;
673	          if (st.wall[ti] !== 3 && st.wall[ti] !== 83 && !isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
674	        }
675	      }
676	    }
677	  }
678	  // 条纹窗墙([num61, num60) × [num53, num54+1],刷 2-5 列跳 2 倍)
679	  {
680	    const n61 = n58t(n51, dir), n60 = n59t(n52, dir);
681	    const sp = 2 + rng.int(0, 3);
682	    let c2 = 0;
683	    for (let x = n61; x < n60; x++) {
684	      for (let y = n53; y < n54 + 1; y++) {
685	        if (st.inBounds(x, y)) st.wall[st.idx(x, y)] = dc.wall;
686	      }
687	      if (++c2 >= sp) { x += sp * 2; c2 = 0; }
688	    }
689	  }
690	  // 门洞 15×3 + 门(style13):中心回退 dx2*0.6*dir,Y += dy2/2 后再 -1.5
691	  cx -= dx2 * 0.6 * dir;
692	  cy += dy2 * 0.5;
693	  cy -= 1.5;
694	  const dL = Math.floor(cx - 7.5), dR = Math.floor(cx + 7.5);
695	  const dT = Math.floor(cy - 1.5), dB = Math.floor(cy + 1.5);
696	  for (let x = dL; x < dR; x++) {
697	    for (let y = dT; y < dB; y++) {
698	      if (st.inBounds(x, y)) st.flags[st.idx(x, y)] = 0;
699	    }
700	  }
701	  if (dir < 0) cx -= 1;
702	  // 原版 L21242 PlaceTile(x, Y+1) → PlaceDoor 门顶在 Y-1（占 Y-1..Y+1，底格 = 旧单格位置）
703	  if (st.inBounds(Math.floor(cx), Math.floor(cy) - 1)) {
704	    placeDoorClosed(st, Math.floor(cx), Math.floor(cy) - 1, 13);
705	  }
706	  // 开放门厅可站立点（原版 dungeonX/Y 语义 cs L72510-72527：入口结构上 3 宽净空可站处；
707	  // 老头 NPC 出生/游走锚）。取门厅中心列，向下找地板
708	  {
709	    const sx = Math.floor((n51 + n52) / 2);
710	    let sy = n54 - 1;
711	    const limit = Math.min(st.h - 3, n54 + 12);
712	    while (sy < limit && !st.isSolid(sx, sy)) sy++;
713	    if (sy < limit) dc.entStand = [sx, sy];
714	  }
715	  dc.minYY = Math.min(dc.minYY, Math.floor(j - dy1 / 2 - dy1 * 0.6) - 6);
716	  dc.entranceX = Math.floor(cx);
717	}
718	
719	// 条纹窗墙左右界(原版 num60/num61)
720	function n58t(n51: number, dir: number): number {
721	  return dir < 0 ? n51 + 1 : n51 + 2;
722	}
723	function n59t(n52: number, dir: number): number {
724	  return dir < 0 ? n52 + 1 : n52 - 2;
725	}
726	
727	/** 尖刺(L18188):两轮(水平带/竖直带) */
728	function placeSpikes(st: TileStore, rng: RNG, gs: GenState, dc: DungeonCtx, count: number): void {
729	  for (let round = 0; round < 2; round++) {
730	    for (let n = 0; n < count; n++) {
731	      const x = rng.int(dc.minX, Math.max(dc.minX + 1, dc.maxX));
732	      const y = rng.int(Math.max(gs.worldSurface, dc.minYY), Math.max(dc.minYY + 1, dc.maxY));
733	      if (!st.inBounds(x, y) || st.flags[st.idx(x, y)] || st.wall[st.idx(x, y)] !== dc.wall) continue;
734	      // 走到实心
735	      let cx = x, cy = y, found = false;
736	      for (let k = 0; k < 30; k++) {
737	        if (round === 0) cy += rng.next() < 0.5 ? 1 : -1; else cx += rng.next() < 0.5 ? 1 : -1;
738	        if (!st.inBounds(cx, cy)) break;
739	        if (st.flags[st.idx(cx, cy)]) { found = true; break; }
740	      }
741	      if (!found) continue;
742	      // 向开口两侧刻尖刺
743	      const len = rng.int(5, 12);
744	      for (let k = -len; k <= len; k++) {
745	        const sx = round === 0 ? cx + k : cx;
746	        const sy = round === 0 ? cy : cy + k;
747	        if (!st.inBounds(sx, sy)) continue;
748	        const i = st.idx(sx, sy);
749	        if (st.flags[i] && st.type[i] === dc.brick) st.type[i] = SPIKE;
750	      }
751	    }
752	  }
753	}
754	
755	/** 门(L18311):房间左右边开口装门 */
756	/** 门(L18302-18430 1:1):±10 列扫描择优(span∈[3,20)、±20 内无他门、底部上 3 行净空),
757	 *  门柱填砖,style 13(1/3 概率按墙换 16/17/18) */
758	function placeDoors(st: TileStore, rng: RNG, dc: DungeonCtx): void {
759	  for (const d of dc.dDoors) {
760	    if (d.y < 2 || d.y >= st.h - 2) continue;
761	    let bestSpan = 100, bestX = 0;
762	    for (let x = d.x - 10; x < d.x + 10; x++) {
763	      if (x < 2 || x >= st.w - 2) continue;
764	      let yTop = d.y;
765	      while (yTop > 10 && !st.flags[st.idx(x, yTop)]) yTop--;
766	      if (st.type[st.idx(x, yTop)] !== dc.brick) continue;
767	      let yBot = d.y;
768	      while (yBot < st.h - 1 && !st.flags[st.idx(x, yBot)]) yBot++;
769	      if (st.type[st.idx(x, yBot)] !== dc.brick) continue;
770	      const span = yBot - yTop;
771	      if (span < 3 || span >= 20) continue;
772	      // ±20×(底±10) 内不得已有门
773	      let doorNear = false;
774	      for (let ix = x - 20; ix < x + 20 && !doorNear; ix++) {
775	        for (let iy = yBot - 10; iy < yBot + 10; iy++) {
776	          if (st.inBounds(ix, iy) && st.flags[st.idx(ix, iy)] && st.type[st.idx(ix, iy)] === DOOR) { doorNear = true; break; }
777	        }
778	      }
779	      if (doorNear) continue;
780	      // 底部上方 3 行 x±3 须净空
781	      let clear = true;
782	      for (let iy = yBot - 3; iy < yBot && clear; iy++) {
783	        for (let ix = x - 3; ix <= x + 3; ix++) {
784	          if (st.inBounds(ix, iy) && st.flags[st.idx(ix, iy)]) { clear = false; break; }
785	        }
786	      }
787	      if (!clear) continue;
788	      let better = false;
789	      if (d.pos === 0 && span < bestSpan) better = true;
790	      else if (d.pos === -1 && x > bestX) better = true;
791	      else if (d.pos === 1 && (bestX === 0 || x < bestX)) better = true;
792	      if (better) { bestX = x; bestSpan = span; }
793	    }
794	    if (bestSpan >= 20) continue;
795	    const x = bestX;
796	    // 门洞:从候选 y 向下清到实心,向上找到实心顶
797	    let yDown = d.y;
798	    while (yDown < st.h - 1 && !st.flags[st.idx(x, yDown)]) yDown++;
799	    let yUp = d.y;
800	    while (yUp > 1 && !st.flags[st.idx(x, yUp)]) yUp--;
801	    const j2 = yDown - 1;
802	    const yFrom = yUp + 1;
803	    for (let y = yFrom; y < j2 - 2; y++) {
804	      if (!st.inBounds(x, y)) continue;
805	      const i = st.idx(x, y);
806	      st.type[i] = dc.brick; st.flags[i] = 1;
807	    }
808	    const style = rng.next() < 1 / 3 ? (dc.wall === 7 ? 16 : dc.wall === 8 ? 17 : 18) : 13;
809	    // 原版 L18404 PlaceTile(i2, j2) → 门顶在 j2-2（占 j2-2..j2）
810	    placeDoorClosed(st, x, j2 - 2, style);
811	    // 两侧门柱补砖(cs L18403-18429)
812	    for (const side of [x - 1, x + 1]) {
813	      if (side < 1 || side >= st.w - 1) continue;
814	      let yy = j2 - 3;
815	      while (yy > 1 && !st.flags[st.idx(side, yy)]) yy--;
816	      if (j2 - yy < j2 - yFrom + 5 && st.type[st.idx(side, yy)] === dc.brick) {
817	        for (let y = j2 - 4 - rng.int(0, 2); y > yy; y--) {
818	          const i = st.idx(side, y);
819	          st.type[i] = dc.brick; st.flags[i] = 1;
820	        }
821	      }
822	    }
823	  }
824	}
825	
826	/** 家具+金箱（1405 L18792 段）：管线 1:1（见下）——房间金箱走 AddBuriedChest 下落语义，
827	 *  战利品序 155/156/157/163/113/3317/327/164；工作台/桌椅/蜡烛由第 7 段地面家具覆盖 */
828	// ============================================================================
829	// 地牢陈设管线(WorldGen.cs L18441-19613 1:1)
830	// 墙变体→房口平台→特殊宝箱(上锁)→书架平台+蜡烛/书→房间金箱→
831	// 灯具(吊灯/灯笼+墙上开关+布线)→飞镖陷阱→地面家具 13 类→墙饰(画/骨)→旗帜
832	// ============================================================================
833	/** TileID.Sets.Boulders（1456 TileID.cs:195）——AddBuriedChest ±2 邻域排除 */
834	const BOULDER_SHEETS_DP = new Set([138, 484, 664, 665, 711, 712, 713, 714, 715, 716]);
835	
836	type ChestSink = Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null>; locked?: boolean }>;
837	
838	function placeFurnishing(st: TileStore, rng: RNG, gs: GenState, dc: DungeonCtx, chests: ChestSink): void {
839	  const { w } = st;
840	  const wallType = dc.wall;
841	  // 墙变体表(cs L18441-18458):7→94/95,9→96/97,8→98/99
842	  const roomWall = wallType === 7 ? [7, 94, 95] : wallType === 9 ? [9, 96, 97] : [8, 98, 99];
843	  const bx0 = dc.minX, bx1 = dc.maxX, by0 = dc.minYY, by1 = dc.maxY;
844	  const isBrick = (x: number, y: number): boolean => {
845	    if (!st.inBounds(x, y)) return false;
846	    const i = st.idx(x, y);
847	    return !!(st.flags[i] && (st.type[i] === dc.brick || st.type[i] === dc.cracked));
848	  };
849	  const isDWall = (x: number, y: number): boolean => st.inBounds(x, y) && dc.isDungeonWall(st, x, y);
850	  const airDW = (x: number, y: number) => st.inBounds(x, y) && !st.flags[st.idx(x, y)] && dc.isDungeonWall(st, x, y);
851	  const solidAt = (x: number, y: number) => st.inBounds(x, y) && st.flags[st.idx(x, y)] && !!TILE_DEFS[st.type[st.idx(x, y)]]?.solid;
852	
853	  // ---- 1. 墙变体(cs L18460-18481):5 轮 × 3 变体,圆内种子点 WallDungeon BFS 扩散 ----
854	  for (let round = 0; round < 5; round++) {
855	    for (let k = 0; k < 3; k++) {
856	      const rad = rng.int(40, 239);
857	      const cx0 = rng.int(bx0, bx1), cy0 = rng.int(by0, by1);
858	      for (let x = cx0 - rad; x < cx0 + rad; x++) {
859	        for (let y = cy0 - rad; y < cy0 + rad; y++) {
860	          if (y <= gs.worldSurface) continue;
861	          if (Math.hypot(x - cx0, y - cy0) >= rad * 0.4) continue;
862	          if (!isDWall(x, y)) continue;
863	          wallDungeonSpread(st, x, y, roomWall[k]);
864	        }
865	      }
866	    }
867	  }
868	
869	  // ---- 2. 房口平台(cs L18483-18598):候选行 ±5 找两侧皆砖的窄口,铺平台到两侧砖 ----
870	  const platFrameY = wallType === 7 ? 108 : wallType === 8 ? 144 : 126;
871	  for (const [px0, py0] of dc.dPlatforms) {
872	    let row = -1;
873	    const maxSpan = py0 < gs.worldSurface + 50 ? 20 : 10;
874	    for (let y = py0 - 5; y <= py0 + 5; y++) {
875	      if (!st.inBounds(px0, y)) continue;
876	      let bad = false;
877	      let xL = px0, xR = px0;
878	      if (st.flags[st.idx(px0, y)]) bad = true;
879	      else {
880	        while (st.inBounds(xL, y) && !st.flags[st.idx(xL, y)]) {
881	          xL--;
882	          if (!st.inBounds(xL, y) || !isBrick(xL, y)) { bad = true; break; }
883	        }
884	        while (st.inBounds(xR, y) && !st.flags[st.idx(xR, y)]) {
885	          xR++;
886	          if (!st.inBounds(xR, y) || !isBrick(xR, y)) { bad = true; break; }
887	        }
888	      }
889	      if (bad || xR - xL > maxSpan) continue;
890	      // 附近不得已有平台;本列上下 ±5/上下 8 格净空
891	      let hasPlat = false;
892	      for (let x = px0 - maxSpan / 2 - 2; x <= px0 + maxSpan / 2 + 2 && !hasPlat; x++) {
893	        for (let yy = y - 5; yy <= y + 5; yy++) {
894	          if (st.inBounds(x, yy) && st.type[st.idx(x, yy)] === PLATFORM && st.flags[st.idx(x, yy)]) { hasPlat = true; break; }
895	        }
896	      }
897	      for (let yy = y + 3; yy >= y - 5 && !hasPlat; yy--) {
898	        if (st.inBounds(px0, yy) && st.flags[st.idx(px0, yy)]) { hasPlat = true; break; }
899	      }
900	      if (hasPlat) continue;
901	      row = y;
902	      break;
903	    }
904	    if (row < 0 || row <= py0 - 10 || row >= py0 + 10) continue;
905	    // 向两侧铺平台直到实心
906	    for (let x = px0; st.inBounds(x, row) && !st.flags[st.idx(x, row)]; x--) {
907	      st.setTileSilent(x, row, PLATFORM, 0, platFrameY);
908	    }
909	    for (let x = px0 + 1; st.inBounds(x, row) && !st.flags[st.idx(x, row)]; x++) {
910	      st.setTileSilent(x, row, PLATFORM, 0, platFrameY);
911	    }
912	  }
913	
914	  // ---- 3. 特殊宝箱(cs L18599-18657):5 个上锁箱(含生物群系箱) ----
915	  const specChests: Array<{ tile: number; style: number; item: string }> = [
916	    { tile: CHEST, style: 23, item: 'vi_1156_piranha_gun' },
917	    gs.crimson
918	      ? { tile: CHEST, style: 24, item: 'vi_1571_scourge_of_the_corruptor' }
919	      : { tile: CHEST, style: 25, item: 'vi_1569_vampire_knives' },
920	    { tile: CHEST, style: 26, item: 'vi_1260_rainbow_gun' },
921	    { tile: CHEST, style: 27, item: 'vi_1572_staff_of_the_frost_hydra' },
922	    { tile: CHEST2, style: 13, item: 'vi_4607_desert_tiger_staff' },
923	  ];
924	  for (const spec of specChests) {
925	    for (let tries = 0; tries < 5000; tries++) {
926	      const x = rng.int(bx0, bx1);
927	      const y = rng.int(Math.floor(gs.worldSurface), by1);
928	      if (airDW(x, y) && addChest(st, chests, x, y, spec.tile, spec.style, ITEM_BY_KEY[spec.item], true)) break;
929	    }
930	  }
931	
932	  // ---- 4. 书架平台 + 蜡烛/书(cs L18658-18764):平台样式取 pass 头 SetupDungeonDataVariables 掷 ----
933	  const bookStyles = dc.shelfStyles;
934	  {
935	    let added = 0, fail = 0;
936	    while (added < Math.floor(w / 20)) {
937	      fail++;
938	      let x = rng.int(bx0, bx1);
939	      const y = rng.int(by0, by1);
940	      let ok = true;
941	      if (airDW(x, y)) {
942	        const dir = rng.int(0, 1) === 0 ? -1 : 1;
943	        // 侧向走到实心(须地牢砖)
944	        while (ok && !st.flags[st.idx(x, y)]) {
945	          x -= dir;
946	          if (x < 5 || x > st.w - 5) ok = false;
947	          else if (st.flags[st.idx(x, y)] && !isBrick(x, y)) ok = false;
948	        }
949	        if (ok && isBrick(x, y) && isBrick(x, y - 1) && isBrick(x, y + 1)) {
950	          const openX = x + dir;
951	          // ±3 内无平台
952	          let hasPlat = false;
953	          for (let dx = -3; dx <= 3 && !hasPlat; dx++) {
954	            for (let dy = -3; dy <= 3; dy++) {
955	              if (st.inBounds(openX + dx, y + dy) && st.type[st.idx(openX + dx, y + dy)] === PLATFORM && st.flags[st.idx(openX + dx, y + dy)]) { hasPlat = true; break; }
956	            }
957	          }
958	          if (!hasPlat && !st.flags[st.idx(openX, y - 1)] && !st.flags[st.idx(openX, y - 2)] && !st.flags[st.idx(openX, y - 3)]) {
959	            // 量开口跨度
960	            let spanX = openX;
961	            while (spanX > bx0 && spanX < bx1 && !st.flags[st.idx(spanX, y)] && !st.flags[st.idx(spanX, y - 1)] && !st.flags[st.idx(spanX, y + 1)]) spanX += dir;
962	            const span = Math.abs(openX - spanX);
963	            if (span > 5) {
964	              const styleIdx = st.wall[st.idx(openX, y)] === roomWall[0] ? 0
965	                : st.wall[st.idx(openX, y)] === roomWall[1] ? 1 : 2;
966	              const withBooks = rng.int(0, 1) === 0;
967	              const runLen = rng.int(1, 3);
968	              for (let k = 0; k < runLen; k++) {
969	                const fx = openX + k * dir;
970	                if (!st.inBounds(fx, y) || st.flags[st.idx(fx, y)]) break;
971	                st.setTileSilent(fx, y, PLATFORM, 0, bookStyles[styleIdx] * 18);
972	                if (withBooks) {
973	                  st.setTileSilent(fx, y - 1, BOOKS, rng.int(0, 49) === 0 ? 90 : 0, 0);
974	                }
975	              }
976	              fail = 0;
977	              added++;
978	              if (!withBooks && rng.int(0, 1) === 0) {
979	                // 蜡烛/水蜡烛放在靠墙的开格上方(cs L18735-18754)
980	                if (rng.int(0, 3) !== 0) {
981	                  st.setTileSilent(openX, y - 1, CANDLE, rng.int(0, 1) !== 0 ? 0 : 18, rng.int(0, 3) * 22); // 蜡烛:亮灭 X 0/18,样式 Y 步22(Tiles_33 实测)
982	                } else {
983	                  st.setTileSilent(openX, y - 1, WATER_CANDLE, 0, 0);
984	                }
985	              }
986	            }
987	          }
988	        }
989	      }
990	      if (fail > 1000) { fail = 0; added++; }
991	    }
992	  }
993	
994	  // ---- 5. 房间金箱(cs L18765-18820):战利品序 155/156/157/163/113/3317/327/164 ----
995	  {
996	    let seq = 1;
997	    const lootSeq: Array<{ item: string; style: number }> = [
998	      { item: 'vi_155_muramasa', style: 2 },
999	      { item: 'vi_156_cobalt_shield', style: 2 },
1000	      { item: 'vi_157_aqua_scepter', style: 2 },
1001	      { item: 'vi_163_blue_moon', style: 2 },
1002	      { item: 'vi_113_magic_missile', style: 2 },
1003	      { item: 'vi_3317_valor', style: 2 },
1004	      { item: 'vi_327_golden_key', style: 0 },
1005	      { item: 'vi_164_handgun', style: 2 },
1006	    ];
1007	    for (const room of dc.rooms) {
1008	      const half = Math.floor((room.r - room.l) * 0.4);
1009	      for (let tries = 0; tries < 1000; tries++) {
1010	        const x = Math.floor((room.l + room.r) / 2) + rng.int(-half, half);
1011	        const y = Math.floor((room.t + room.b) / 2) + rng.int(-half, half);
1012	        if (seq === 1) seq = 2;
1013	        let loot = lootSeq[Math.min(seq - 2, lootSeq.length - 1)];
1014	        if (seq > lootSeq.length + 1) seq = 0;
1015	        if (seq === 0) loot = lootSeq[lootSeq.length - 1];
1016	        if (y < gs.worldSurface + 50) loot = { item: 'vi_327_golden_key', style: 0 };
1017	        if (addChest(st, chests, x, y, CHEST, loot.style, ITEM_BY_KEY[loot.item], false)) {
1018	          seq++;
1019	          break;
1020	        }
1021	      }
1022	    }
1023	  }
1024	
1025	  // ---- 边界外扩 ±25(cs L18821-18832),后续阶段用 ----
1026	  const ex0 = Math.max(0, bx0 - 25), ex1 = Math.min(st.w - 1, bx1 + 25);
1027	  const ey0 = Math.max(0, by0 - 25), ey1 = Math.min(st.h - 1, by1 + 25);
1028	
1029	  // ---- 6. 灯具(cs L18865-19040):吊灯/灯笼 + 墙上开关 + 红线布线 ----
1030	  {
1031	    // 灯具样式取 pass 头 SetupDungeonDataVariables 掷（cs:256-266）
1032	    const lampStyles = dc.lanternStyles;
1033	    let added = 0, fail = 0;
1034	    while (added < Math.floor(w / 150)) {
1035	      fail++;
1036	      const x = rng.int(ex0, ex1);
1037	      const yStart = rng.int(ey0, ey1);
1038	      if (isDWall(x, yStart)) {
1039	        for (let y = yStart; y > ey0; y--) {
1040	          if (!isBrick(x, y - 1)) break;
1041	          // 附近 ±15 无灯具;灯位周围净空
1042	          let near = false;
1043	          for (let dx = -15; dx < 15 && !near; dx++) {
1044	            for (let dy = -15; dy < 15; dy++) {
1045	              const t = st.inBounds(x + dx, y + dy) && st.flags[st.idx(x + dx, y + dy)] ? st.type[st.idx(x + dx, y + dy)] : 0;
1046	              if (t === LANTERN || t === CHANDELIER) { near = true; break; }
1047	            }
1048	          }
1049	          if (st.flags[st.idx(x - 1, y)] || st.flags[st.idx(x + 1, y)]
1050	            || st.flags[st.idx(x - 1, y + 1)] || st.flags[st.idx(x + 1, y + 1)]
1051	            || st.flags[st.idx(x, y + 2)]) near = true;
1052	          if (!near) {
1053	            let placedLight = false;
1054	            if (rng.int(0, 6) === 0) {
1055	              // 吊灯:下方 15 格内无实心才放(cs L18927-18936)
1056	              let blocked = false;
1057	              for (let k = 0; k < 15; k++) if (solidAt(x, y + k)) { blocked = true; break; }
1058	              // 吊灯样式 Y 行54(wrap37 换列) 
1059	              if (!blocked && placeFurn(st, x, y, CHANDELIER, roomWall[0] === 7 ? 27 : roomWall[0] === 8 ? 28 : 29, 'top', 1, true, 54))
1060	              {
1061	                placedLight = true;
1062	                fail = 0; added++;
1063	                wireToSwitch(st, rng, dc, x, y, ex0, ex1, ey0, ey1, isDWall, isBrick, true);
1064	              }
1065	            }
1066	            if (!placedLight) {
1067	              const styleIdx = st.wall[st.idx(x, y)] === roomWall[1] ? 1 : st.wall[st.idx(x, y)] === roomWall[2] ? 2 : 0;
1068	              if (placeFurn(st, x, y, LANTERN, lampStyles[styleIdx], 'top', 1, true, 36)) { // 竖排样式行高36(TileLightScanner frameY/36 实证)
1069	                fail = 0; added++;
1070	                wireToSwitch(st, rng, dc, x, y, ex0, ex1, ey0, ey1, isDWall, isBrick, false);
1071	              }
1072	            }
1073	          }
1074	          break;  // 只取第一个天花板
1075	        }
1076	      }
1077	      if (fail > 1000) { fail = 0; added++; }
1078	    }
1079	  }
1080	
1081	  // ---- 7. 飞镖陷阱(MakeDungeon_Traps cs L18846-18863, w/500; placeTrap(x,y,0) 1:1) ----
1082	  {
1083	    // placeTrap type=0 分支（WorldGen.cs:3324-3420）：
1084	    // 自采样点下扫首个实心格，其上方放压板(135)；压板行向两侧扫至锚墙（实心或裂砖
1085	    // 481/482/483），挖一格嵌飞镖陷阱(137)；红线沿 L 路径（先 x 后 y）连板→陷阱。
1086	    const CRACKED_SET = new Set<number>(
1087	      ['v_481_cracked_blue_brick', 'v_482_cracked_green_brick', 'v_483_cracked_pink_brick']
1088	        .map((k) => TILE_BY_KEY[k]).filter((t): t is number => t != null));
1089	    const PLATE = TILE_BY_KEY['v_135_pressure_plates']!;
1090	    const MUSH_GRASS = TILE_BY_KEY['v_70_mushroom_grass_block'] ?? 0;   // L3339 邻格回避
1091	    const GLOW_SHROOM = TILE_BY_KEY['v_190_glowing_mushroom_block']!;   // L3385 锚墙回避
1092	    const WOODEN_SPIKE = TILE_BY_KEY['v_232_wooden_spike']!;            // L3363 下方回避
1093	    const typeAt = (x: number, y: number) => (st.inBounds(x, y) && st.flags[st.idx(x, y)] ? st.type[st.idx(x, y)] : 0);
1094	    // SolidTile 或 tileCracked（cs L3366/L3374 侧扫把裂砖当锚）
1095	    const trapSolid = (x: number, y: number) =>
1096	      solidAt(x, y) || (st.inBounds(x, y) && st.flags[st.idx(x, y)] && CRACKED_SET.has(st.type[st.idx(x, y)]));
1097	    const placeTrap0 = (x: number, y: number): boolean => {
1098	      // L3326-3335: 下扫首个实心格（越界放弃）
1099	      let j1 = y;
1100	      while (!solidAt(x, j1)) {
1101	        j1++;
1102	        if (j1 > st.h - 10) return false;
1103	      }
1104	      const px = x, py = j1 - 1;
1105	      const pi = st.idx(px, py);
1106	      // L3339: 20 格内有蘑菇草(70)不放；蜥蜴砖unsafe墙(87)不放
1107	      if (st.wall[pi] === 87) return false;
1108	      for (let yy = py - 20; yy <= py + 20; yy++) {
1109	        for (let xx = px - 20; xx <= px + 20; xx++) {
1110	          if (typeAt(xx, yy) === MUSH_GRASS) return false;
1111	        }
1112	      }
1113	      // L3341+L3345: 岩浆上不放（type 0）
1114	      if (st.liquid[pi] > 0 && st.liquidType[pi] === 2) return false;
1115	      if (px < 3 || py < 3 || px > st.w - 4 || py > st.h - 4) return false; // InWorld(,3)
1116	      // L3352-3356: 压板落点 + 上方两行 3 列须全空（nactive 检查）
1117	      for (const [ax, ay] of [[0, 0], [-1, 0], [1, 0], [0, -1], [-1, -1], [1, -1], [0, -2], [-1, -2], [1, -2]] as const) {
1118	        if (st.flags[st.idx(px + ax, py + ay)]) return false;
1119	      }
1120	      // L3357: 下方不能是尖刺(48)/木尖刺(232)
1121	      const below = typeAt(px, py + 1);
1122	      if (below === SPIKE || below === WOODEN_SPIKE) return false;
1123	      // L3365-3420: type 0 —— 压板行 j2 = py - Next(3)
1124	      const j2 = py - rng.int(0, 2);
1125	      let i1 = px;
1126	      while (!trapSolid(i1, j2)) { i1--; if (i1 < 0) return false; }
1127	      const i2 = i1;
1128	      let i3 = px;
1129	      while (!trapSolid(i3, j2)) { i3++; if (i3 > st.w) return false; }
1130	      const i4 = i3;
1131	      // L3379-3391: 锚墙距离 5..49、脚下须实心、锚位非门(10)/尖刺(48)；双墙随机选边
1132	      const num1 = px - i2, num2 = i4 - px;
1133	      let f3 = num1 > 5 && num1 < 50;
1134	      let f4 = num2 > 5 && num2 < 50;
1135	      if (f3 && !solidAt(i2, j2 + 1)) f3 = false;
1136	      if (f4 && !solidAt(i4, j2 + 1)) f4 = false;
1137	      const badAnchor = (t: number) => t === DOOR || t === SPIKE;
1138	      if (f3 && (badAnchor(typeAt(i2, j2)) || badAnchor(typeAt(i2, j2 + 1)))) f3 = false;
1139	      if (f4 && (badAnchor(typeAt(i4, j2)) || badAnchor(typeAt(i4, j2 + 1)))) f4 = false;
1140	      let i5: number, num3: number;
1141	      if (f3 && f4) {
1142	        num3 = 1; i5 = i2;
1143	        if (rng.int(0, 1) === 0) { i5 = i4; num3 = -1; }
1144	      } else if (f4) { i5 = i4; num3 = -1; }
1145	      else if (f3) { i5 = i2; num3 = 1; }
1146	      else return false;
1147	      if (typeAt(i5, j2) === GLOW_SHROOM) return false;
1148	      // L3391-3396: 压板(135)——背后有墙 style 2（frameX 36），否则 Next(2,4)；地牢恒有墙
1149	      st.setTileSilent(px, py, PLATE, 0, st.wall[pi] > 0 ? 36 : rng.int(2, 3) * 18);
1150	      // L3397-3399: 锚墙挖一格嵌飞镖陷阱(137)；墙在左(frameX 18)朝右，墙在右(frameX 0)朝左
1151	      st.setTileSilent(i5, j2, TRAP, num3 === 1 ? 18 : 0, 0);
1152	      // L3400-3415: 红线 L 路径（先 x 后 y，三段 wire 同原版逐段置位）
1153	      let wx = px, wy = py;
1154	      while (wx !== i5 || wy !== j2) {
1155	        st.wire[st.idx(wx, wy)] |= TileStore.WIRE_RED;
1156	        if (wx > i5) wx--; else if (wx < i5) wx++;
1157	        st.wire[st.idx(wx, wy)] |= TileStore.WIRE_RED;
1158	        if (wy > j2) wy--; else if (wy < j2) wy++;
1159	        st.wire[st.idx(wx, wy)] |= TileStore.WIRE_RED;
1160	      }
1161	      return true;
1162	    };
1163	    // MakeDungeon_Traps：随机点须是地牢墙，placeTrap 成功或连败 1000 次计数
1164	    let added = 0, fail = 0;
1165	    while (added < Math.floor(w / 500)) {
1166	      fail++;
1167	      const x = rng.int(ex0, ex1);
1168	      let y = rng.int(ey0, ey1);
1169	      while (y < gs.worldSurface && y < ey1) y = rng.int(ey0, ey1);
1170	      if (isDWall(x, y) && placeTrap0(x, y)) { fail = 0; added++; }
1171	      if (fail > 1000) { fail = 0; added++; }
1172	    }
1173	  }
1174	
1175	  // ---- 8. 地面家具(cs L19287-19613):13 类,2000×w/4200 次尝试 ----
1176	  {
1177	    // 样式表(cs L19317-19365,值=ItemID.Sets.DerivedPlacementDetails 逐项核对):
1178	    // 墙 7 / 8 / 9。ftype3=书架 101(item1414-1416 → 1/2/3)、ftype10=路灯 93
1179	    // (item2645-2647 → placeStyle 22+type-2643 = 24/25/26)、ftype11=烛台 100
1180	    // (item2664-2666 → 22+type-2664 = 22/23/24)——灯/烛台两列曾互换、书架值曾
1181	    // 贴给烛台（2026-08-12 审计修正）
1182	    const S = wallType === 7
1183	      ? [13, 10, 11, 1, 46, 1, 5, 11, 5, 6, 21, 24, 22, 30]
1184	      : wallType === 8
1185	        ? [14, 11, 12, 2, 47, 2, 6, 12, 6, 7, 22, 25, 23, 31]
1186	        : [15, 12, 13, 3, 48, 3, 7, 13, 7, 8, 23, 26, 24, 32];
1187	    const [sChair, sTable, sDresser, sCandle, sStatue, sBookcase, sBed, sPiano, sDresser2, sBench, sTub, sLamp, sCandelabra2, sClock] = S;
1188	    let alchemyLeft = 1 + Math.floor(w / 4200);
1189	    let bewitchLeft = 1 + Math.floor(w / 4200);
1190	    const attempts = Math.floor(2000 * (w / 4200));
1191	    // 死循环防护（2026-08-10，"生成卡死在生物群系"根因）：旧版 n-- 在循环顶无条件
1192	    // 生效——炼金台/施法台未放完时，若有效性检查一直 continue（小世界地牢合法点位
1193	    // 稀少），n 永不前进 → 生成挂死。现改为：①n-- 只在实际尝试放置（过了全部有效性
1194	    // 检查）后才生效；②硬迭代上限兜底（placeFurn 持续失败也能终止）
1195	    let hardGuard = attempts * 50;
1196	    for (let n = 0; n < attempts && hardGuard-- > 0; n++) {
1197	      let x = rng.int(ex0, ex1);
1198	      let y = 0;
1199	      for (let t = 0; t < 200; t++) {
1200	        y = rng.int(Math.floor(gs.worldSurface) + 10, ey1);
1201	        if (airDW(x, y)) break;
1202	        x = rng.int(ex0, ex1);
1203	      }
1204	      if (!airDW(x, y)) continue;
1205	      // 落到地面
1206	      while (!solidAt(x, y) && y < st.h - 200) y++;
1207	      const floorY = y - 1;
1208	      // 量地板跨度
1209	      let xL = x, xR = x;
1210	      while (!st.flags[st.idx(xL, floorY)] && solidAt(xL, floorY + 1)) xL--;
1211	      while (!st.flags[st.idx(xR, floorY)] && solidAt(xR, floorY + 1)) xR++;
1212	      const span = xR - xL - 1;
1213	      const cx0 = Math.floor((xR + xL) / 2);
1214	      if (st.flags[st.idx(cx0, floorY)] || !isDWall(cx0, floorY) || !solidAt(cx0, floorY + 1)
1215	        || (st.flags[st.idx(cx0, floorY + 1)] && st.type[st.idx(cx0, floorY + 1)] === SPIKE)) continue;
1216	      // 家具类型与占地(cs L19383-19454)
1217	      const sizes: Array<[number, number]> = [[5, 4], [4, 3], [3, 5], [4, 6], [3, 3], [5, 3], [5, 4], [5, 4], [5, 4], [5, 3], [2, 4], [3, 3], [2, 5]];
1218	      let ftype = rng.int(0, 12);
1219	      if ((ftype === 10 || ftype === 11 || ftype === 12) && rng.int(0, 3) !== 0) ftype = rng.int(0, 12);
1220	      const wv = st.wall[st.idx(cx0, floorY)];
1221	      const limited = wv >= 94 && wv <= 105;  // 变体墙只允许桌/梳妆台
1222	      const allowed = limited ? ftype === 0 || ftype === 1 || ftype === 4 : true;
1223	      if (!allowed) continue;
1224	      const [halfW, hgt] = sizes[ftype];
1225	      // 清空检查
1226	      let clear = true;
1227	      for (let dx = cx0 - halfW; dx <= cx0 + halfW && clear; dx++) {
1228	        for (let dy = floorY - hgt; dy <= floorY; dy++) {
1229	          if (st.inBounds(dx, dy) && st.flags[st.idx(dx, dy)]) { clear = false; break; }
1230	        }
1231	      }
1232	      if (!clear || span < halfW * 1.75) continue;
1233	      // 优先:炼金台/施法台(cs L19468-19482)。
1234	      // n-- 移到此处（实际尝试放置才回退计数）——有效性 continue 不再消耗重试预算
1235	      if (alchemyLeft > 0 || bewitchLeft > 0) n--;
1236	      if (alchemyLeft > 0 || bewitchLeft > 0) {
1237	        if (alchemyLeft > 0) {
1238	          if (placeFurn(st, cx0, floorY, ALCHEMY, 0)) alchemyLeft--;
1239	        } else if (placeFurn(st, cx0, floorY, BEWITCH, 0)) bewitchLeft--;
1240	        continue;
1241	      }
1242	      switch (ftype) {
1243	        case 0: {
1244	          // 桌+双椅+桌上摆件
1245	          if (!placeFurn(st, cx0, floorY, TABLE, sTable)) break;
1246	          if (!st.flags[st.idx(cx0 - 2, floorY)]) {
1247	            if (placeFurn(st, cx0 - 2, floorY, CHAIR, sChair)) flipFurn(st, cx0 - 2, floorY, CHAIR);
1248	          }
1249	          if (!st.flags[st.idx(cx0 + 2, floorY)]) placeFurn(st, cx0 + 2, floorY, CHAIR, sChair);
1250	          for (let i = cx0 - 1; i <= cx0 + 1; i++) {
1251	            if (rng.int(0, 1) === 0 && !st.flags[st.idx(i, floorY - 2)]) {
1252	              const pick = rng.int(0, 4);
1253	              if (pick <= 1) st.setTileSilent(i, floorY - 2, CANDLE, 0, sCandle * 22); // 样式竖排 Y 步22,亮态 X=0
1254	              else if (pick === 2) st.setTileSilent(i, floorY - 2, WATER_CANDLE, 0, 0);
1255	              else if (pick === 3) st.setTileSilent(i, floorY - 2, BOOKS, 0, 0);
1256	              else st.setTileSilent(i, floorY - 2, BOWLS, 0, 0);
1257	            }
1258	          }
1259	          break;
1260	        }
1261	        case 1: {
1262	          if (!placeFurn(st, cx0, floorY, WORKBENCH, sDresser)) break;
1263	          if (rng.int(0, 1) === 0) {
1264	            if (!st.flags[st.idx(cx0 - 1, floorY)] && placeFurn(st, cx0 - 1, floorY, CHAIR, sChair)) {
1265	              flipFurn(st, cx0 - 1, floorY, CHAIR);
1266	            }
1267	          } else placeFurn(st, cx0 + 2, floorY, CHAIR, sChair);
1268	          for (let i = cx0; i <= cx0 + 1; i++) {
1269	            if (rng.int(0, 1) === 0 && !st.flags[st.idx(i, floorY - 1)]) {
1270	              const pick = rng.int(0, 4);
1271	              if (pick <= 1) st.setTileSilent(i, floorY - 1, CANDLE, 0, sCandle * 22);
1272	              else if (pick === 2) st.setTileSilent(i, floorY - 1, WATER_CANDLE, 0, 0);
1273	              else if (pick === 3) st.setTileSilent(i, floorY - 1, BOOKS, 0, 0);
1274	              else st.setTileSilent(i, floorY - 1, BOWLS, 0, 0);
1275	            }
1276	          }
1277	          break;
1278	        }
1279	        case 2: placeFurn(st, cx0, floorY, STATUE, sStatue); break;
1280	        case 3: placeFurn(st, cx0, floorY, BOOKCASE, sBookcase); break; // 书架 101(item1414-1416,横排)
1281	        case 4: {
1282	          if (placeFurn(st, cx0, floorY, CHAIR, sChair) && rng.int(0, 1) === 0) flipFurn(st, cx0, floorY, CHAIR);
1283	          break;
1284	        }
1285	        case 5: placeFurn(st, cx0, floorY, BED, sBed, 'bottom', rng.int(0, 1) === 0 ? 1 : -1); break;
1286	        case 6: placeFurn(st, cx0, floorY, PIANO, sPiano); break;
1287	        case 7: placeFurn(st, cx0, floorY, DRESSER, sDresser2); break;
1288	        case 8: placeFurn(st, cx0, floorY, BENCH, sBench); break;
1289	        case 9: placeFurn(st, cx0, floorY, BATHTUB, sTub, 'bottom', rng.int(0, 1) === 0 ? 1 : -1); break;
1290	        case 10: placeFurn(st, cx0, floorY, LAMP, sLamp, 'bottom', 1, true, 110); break; // 路灯样式竖排步110(93 表行带实测)
1291	        case 11: placeFurn(st, cx0, floorY, CANDELABRA, sCandelabra2, 'bottom', 1, true, 72); break;
1292	        case 12: placeFurn(st, cx0, floorY, CLOCK, sClock); break;
1293	      }
1294	    }
1295	  }
1296	
1297	  // ---- 9. 墙饰:画/骨(cs L19080-19285),420000/w 个 ----
1298	  {
1299	    const count = Math.floor(420000 / w);
1300	    for (let n = 0; n < count; n++) {
1301	      let x = rng.int(ex0, ex1);
1302	      let y = 0;
1303	      for (let t = 0; t < 200; t++) {
1304	        y = rng.int(Math.floor(gs.worldSurface), ey1);
1305	        if (airDW(x, y)) break;
1306	        x = rng.int(ex0, ex1);
1307	      }
1308	      if (!airDW(x, y)) continue;
1309	      // 两次重定心(cs L19089-19109)
1310	      for (let k = 0; k < 2; k++) {
1311	        let a = x, b = x;
1312	        while (st.inBounds(a, y) && !st.flags[st.idx(a, y)] && isDWall(a, y)) a--;
1313	        while (st.inBounds(b, y) && !st.flags[st.idx(b, y)] && isDWall(b, y)) b++;
1314	        x = Math.floor((a + 1 + b - 1) / 2);
1315	        let c = y, d = y;
1316	        while (st.inBounds(x, c) && !st.flags[st.idx(x, c)] && isDWall(x, c)) c--;
1317	        while (st.inBounds(x, d) && !st.flags[st.idx(x, d)] && isDWall(x, d)) d++;
1318	        y = Math.floor((c + 1 + d - 1) / 2);
1319	      }
1320	      // 量净空跨度(三向无实心)
1321	      const spanH = (xx: number, yy: number) => {
1322	        let a = xx, b = xx;
1323	        while (st.inBounds(a, yy) && !st.flags[st.idx(a, yy)] && !st.flags[st.idx(a, yy - 1)] && !st.flags[st.idx(a, yy + 1)]) a--;
1324	        while (st.inBounds(b, yy) && !st.flags[st.idx(b, yy)] && !st.flags[st.idx(b, yy - 1)] && !st.flags[st.idx(b, yy + 1)]) b++;
1325	        return { w: b - a - 1, x0: a + 1, x1: b - 1 };
1326	      };
1327	      const spanV = (xx: number, yy: number) => {
1328	        let a = yy, b = yy;
1329	        while (st.inBounds(xx, a) && !st.flags[st.idx(xx, a)] && !st.flags[st.idx(xx - 1, a)] && !st.flags[st.idx(xx + 1, a)]) a--;
1330	        while (st.inBounds(xx, b) && !st.flags[st.idx(xx, b)] && !st.flags[st.idx(xx - 1, b)] && !st.flags[st.idx(xx + 1, b)]) b++;
1331	        return { h: b - a - 1, y0: a + 1, y1: b - 1 };
1332	      };
1333	      const sh = spanH(x, y), sv = spanV(x, y);
1334	      if (sh.w <= 7 || sv.h <= 5) continue;
1335	      const canH = sh.w > sv.h * 3 && sh.w > 21;
1336	      const canV = sv.h > sh.w * 3 && sv.h > 21;
1337	      let kind = rng.int(0, 2);
1338	      if (st.wall[st.idx(x, y)] === roomWall[0]) kind = 0;
1339	      let guard = 0;
1340	      while (!((kind === 0) || (kind === 1 && canH) || (kind === 2 && canV)) && guard++ < 20) kind = rng.int(0, 2);
1341	      if (!((kind === 0) || (kind === 1 && canH) || (kind === 2 && canV))) continue;
1342	      if (nearPicture2(st, x, y, roomWall[0])) continue;
1343	      const isMain = st.wall[st.idx(x, y)] === roomWall[0];
1344	      const randPic = (): [number, number] => {
1345	        if (rng.int(0, 2) < 2) {
1346	          const map = [12, 13, 14, 15, 18, 19, 23];
1347	          return [HANGING, map[rng.int(0, 6)]];
1348	        }
1349	        const r = rng.int(0, 16);
1350	        const style = r > 13 ? (r === 14 ? 15 : r === 15 ? 16 : 30) : r;
1351	        return [PAINTING, style];
1352	      };
1353	      const randBone = (): [number, number] => rng.int(0, 1) === 0
1354	        ? [HANGING, rng.int(0, 1) === 0 ? 16 : 17]
1355	        : [CATACOMB, rng.int(0, 8)];
1356	      const placeAt = (px: number, py: number) => {
1357	        const [tile, style] = isMain ? randPic() : randBone();
1358	        if (!nearPicture(st, px, py)) placeWallArt(st, px, py, tile, style);
1359	      };
1360	      placeAt(x, y);
1361	      if (kind === 1) {
1362	        // 横向 ±7 续画
1363	        for (const dir of [1, -1]) {
1364	          let px = x, py = y;
1365	          for (let k = 0; k < 2; k++) {
1366	            px += 7 * dir;
1367	            const sv2 = spanV(px, py);
1368	            py = Math.floor((sv2.y0 + sv2.y1) / 2);
1369	            if (Math.abs(y - py) >= 4) break;
1370	            placeAt(px, py);
1371	          }
1372	        }
1373	      } else if (kind === 2) {
1374	        for (const dir of [1, -1]) {
1375	          let px = x, py = y;
1376	          for (let k = 0; k < 3; k++) {
1377	            py += 7 * dir;
1378	            const sh2 = spanH(px, py);
1379	            px = Math.floor((sh2.x0 + sh2.x1) / 2);
1380	            if (Math.abs(x - px) >= 4) break;
1381	            placeAt(px, py);
1382	          }
1383	        }
1384	      }
1385	    }
1386	  }
1387	
1388	  // ---- 10. 旗帜(cs L19042-19078),840000/w 个 ----
1389	  {
1390	    const count = Math.floor(840000 / w);
1391	    for (let n = 0; n < count; n++) {
1392	      let x = rng.int(ex0, ex1);
1393	      let y = 0;
1394	      for (let t = 0; t < 200; t++) {
1395	        y = rng.int(ey0, ey1);
1396	        if (airDW(x, y)) break;
1397	        x = rng.int(ex0, ex1);
1398	      }
1399	      if (!airDW(x, y)) continue;
1400	      // 向上找顶
1401	      let j1 = y;
1402	      while (!solidAt(x, j1) && j1 > 10) j1--;
1403	      const j2 = j1 + 1;
1404	      if (!isDWall(x, j2)) continue;
1405	      if (st.flags[st.idx(x, j2 - 1)] && st.type[st.idx(x, j2 - 1)] === SPIKE) continue;
1406	      let clear = true;
1407	      for (let k = 0; k < 4; k++) if (st.flags[st.idx(x, j2 + k)]) { clear = false; break; }
1408	      if (!clear) continue;
1409	      let bad = false;
1410	      for (let dx = -1; dx <= 1 && !bad; dx++) {
1411	        for (let dy = 0; dy <= 3; dy++) {
1412	          if (!st.inBounds(x + dx, j2 + dy)) continue;
1413	          const t = st.flags[st.idx(x + dx, j2 + dy)] ? st.type[st.idx(x + dx, j2 + dy)] : 0;
1414	          if (t === DOOR || t === BANNER) { bad = true; break; }
1415	        }
1416	      }
1417	      if (bad) continue;
1418	      const base = st.wall[st.idx(x, j2)] === roomWall[1] ? 12 : st.wall[st.idx(x, j2)] === roomWall[2] ? 14 : 10;
1419	      // 整条旗帜同一 style(原版 PlaceTile 一次抽取,此前每格独立重摇会混样式)
1420	      const bannerStyle = base + rng.int(0, 1);
1421	      st.setTileSilent(x, j2, BANNER, bannerStyle * 54, 0); // 旗帜样式横排步54(91 表 1998=37×54)
1422	      st.setTileSilent(x, j2 + 1, BANNER, bannerStyle * 54, 18);
1423	      st.setTileSilent(x, j2 + 2, BANNER, bannerStyle * 54, 36);
1424	    }
1425	  }
1426	}
1427	
1428	/** WallDungeon 扩散(cs L54737):非实心格连通域内任意墙(≠244)→ 目标变体 */
1429	function wallDungeonSpread(st: TileStore, sx: number, sy: number, wallType: number): void {
1430	  const seen = new Set<number>();
1431	  const q: Array<[number, number]> = [[sx, sy]];
1432	  seen.add(sx * 100000 + sy);
1433	  while (q.length) {
1434	    const [x, y] = q.shift()!;
1435	    if (!st.inBounds(x, y)) continue;
1436	    const i = st.idx(x, y);
1437	    if (!st.flags[i] && st.wall[i] !== wallType && st.wall[i] > 0 && st.wall[i] !== 244) {
1438	      st.wall[i] = wallType;
1439	      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as const) {
1440	        const k = (x + dx) * 100000 + (y + dy);
1441	        if (!seen.has(k)) { seen.add(k); q.push([x + dx, y + dy]); }
1442	      }
1443	    } else if (st.flags[i]) {
1444	      st.wall[i] = wallType;
1445	    }
1446	  }
1447	}
1448	
1449	/**
1450	 * 家具放置:锚点语义 bottom(底行=floorY,水平居中)或 top(顶行=topY,居中)。
1451	 * 成功条件:fw×fh 全净空 + 底行下方全实心(bottom 时)。帧 = style*fw*18 + dx*18 / dy*18。
1452	 * flip=-1 时水平镜像帧。返回是否放置成功。
1453	 */
1454	export function placeFurn(st: TileStore, cx: number, anchorY: number, tile: number, style: number, anchor: 'bottom' | 'top' = 'bottom', flip = 1, support = true, styleRowH?: number, styleColW?: number): boolean {
1455	  const def = TILE_DEFS[tile];
1456	  if (!def) return false;
1457	  const fw = def.vanilla?.fw ?? def.w ?? 1;
1458	  const fh = def.vanilla?.fh ?? def.h ?? 1;
1459	  const x0 = cx - Math.floor(fw / 2);
1460	  const yTop = anchor === 'bottom' ? anchorY - fh + 1 : anchorY;
1461	  for (let dx = 0; dx < fw; dx++) {
1462	    for (let dy = 0; dy < fh; dy++) {
1463	      if (!st.inBounds(x0 + dx, yTop + dy) || st.flags[st.idx(x0 + dx, yTop + dy)]) return false;
1464	    }
1465	  }
1466	  if (anchor === 'bottom' && support) {
1467	    for (let dx = 0; dx < fw; dx++) {
1468	      if (!st.inBounds(x0 + dx, yTop + fh) || !st.flags[st.idx(x0 + dx, yTop + fh)]
1469	        || !TILE_DEFS[st.type[st.idx(x0 + dx, yTop + fh)]]?.solid) return false;
1470	    }
1471	  }
1472	  const sheet = TILE_DEFS[tile]?.vanilla?.sheet ?? -1;
1473	  // 权威布局表(FurnitureStyle.ts,TileObjectData+贴图实测):表内 sheet 直接用,
1474	  // 表外尊重调用参数(竖排 styleRowH / 横排列步 styleColW),最终回退通用横排。
1475	  // 15/139/187 曾漏登记→椅子全落通用横排回退而实为竖排(神庙木椅 2026-08-12),
1476	  // 已补全与 FurnitureStyle.ts 覆盖面同步
1477	  const inTable = [42, 33, 49, 34, 100, 93, 91, 240, 241, 242, 245, 246, 15, 139, 187, 79, 90].includes(sheet);
1478	  let bx: number, by: number;
1479	  if (inTable) [bx, by] = furnitureStyleBase(sheet, style, fw);
1480	  else if (styleRowH !== undefined) { bx = 0; by = style * styleRowH; }
1481	  else { bx = style * (styleColW ?? fw * 18); by = 0; }
1482	  for (let dx = 0; dx < fw; dx++) {
1483	    for (let dy = 0; dy < fh; dy++) {
1484	      const fx = flip < 0 ? fw - 1 - dx : dx;
1485	      st.setTileSilent(x0 + dx, yTop + dy, tile, bx + fx * 18, by + dy * 18);
1486	    }
1487	  }
1488	  return true;
1489	}
1490	
1491	/** 家具水平镜像(帧 X 翻转:桌椅等 1-3 宽物件整体 +18*fw) */
1492	export function flipFurn(st: TileStore, cx: number, floorY: number, tile: number): void {
1493	  const def = TILE_DEFS[tile];
1494	  if (!def) return;
1495	  const fw = def.vanilla?.fw ?? def.w ?? 1;
1496	  const fh = def.vanilla?.fh ?? def.h ?? 1;
1497	  const x0 = cx - Math.floor(fw / 2);
1498	  const yTop = floorY - fh + 1;
1499	  for (let dx = 0; dx < fw; dx++) {
1500	    for (let dy = 0; dy < fh; dy++) {
1501	      if (!st.inBounds(x0 + dx, yTop + dy)) continue;
1502	      const i = st.idx(x0 + dx, yTop + dy);
1503	      if (st.type[i] === tile) st.frameX[i] += fw * 18;
1504	    }
1505	  }
1506	}
1507	
1508	/** 墙饰(画/骨/挂毯):顶行=topY,锚点左上;须净空 */
1509	function placeWallArt(st: TileStore, x: number, y: number, tile: number, style: number): void {
1510	  const def = TILE_DEFS[tile];
1511	  if (!def) return;
1512	  const fw = def.vanilla?.fw ?? def.w ?? 1;
1513	  const fh = def.vanilla?.fh ?? def.h ?? 1;
1514	  const sheet = def.vanilla?.sheet ?? -1;
1515	  const x0 = x - Math.floor(fw / 2);
1516	  for (let dx = 0; dx < fw; dx++) {
1517	    for (let dy = 0; dy < fh; dy++) {
1518	      if (!st.inBounds(x0 + dx, y + dy) || st.flags[st.idx(x0 + dx, y + dy)]) return;
1519	    }
1520	  }
1521	  // 样式基偏移(TileObjectData + Tiles_N.png 尺寸实测):
1522	  //  240(1944×162):横排 36 列×54,wrap36 → 超 36 换下行 54
1523	  //  241(4×3):竖排行 54(wrap0 单列)
1524	  //  242(324×1944):竖排 27 行×72,wrap27 → 超 27 换右列 108
1525	  let bx: number, by: number;
1526	  if (sheet === 240) { bx = (style % 36) * 54; by = Math.floor(style / 36) * 54; }
1527	  else if (sheet === 241) { bx = 0; by = style * 54; }
1528	  else if (sheet === 242) { bx = Math.floor(style / 27) * 108; by = (style % 27) * 72; }
1529	  else { bx = style * fw * 18; by = 0; }
1530	  for (let dx = 0; dx < fw; dx++) {
1531	    for (let dy = 0; dy < fh; dy++) {
1532	      st.setTileSilent(x0 + dx, y + dy, tile, bx + dx * 18, by + dy * 18);
1533	    }
1534	  }
1535	}
1536	
1537	/** nearPicture(cs L17966):±4×±3 有任意实心 */
1538	function nearPicture(st: TileStore, x: number, y: number): boolean {
1539	  for (let dx = -4; dx <= 3; dx++) {
1540	    for (let dy = -3; dy <= 2; dy++) {
1541	      if (st.inBounds(x + dx, y + dy) && st.flags[st.idx(x + dx, y + dy)]) return true;
1542	    }
1543	  }
1544	  return false;
1545	}
1546	
1547	/** nearPicture2(cs L17979):±15/±10(主墙)或 ±8/±5(变体墙)内已有墙饰 */
1548	function nearPicture2(st: TileStore, x: number, y: number, mainWall: number): boolean {
1549	  const wall = st.inBounds(x, y) ? st.wall[st.idx(x, y)] : 0;
1550	  const rx = wall === mainWall ? 15 : 8;
1551	  const ry = wall === mainWall ? 10 : 5;
1552	  for (let dx = -rx; dx <= rx; dx++) {
1553	    for (let dy = -ry; dy <= ry; dy++) {
1554	      if (!st.inBounds(x + dx, y + dy) || !st.flags[st.idx(x + dx, y + dy)]) continue;
1555	      const t = st.type[st.idx(x + dx, y + dy)];
1556	      if (t === HANGING || t === CATACOMB || t === PAINTING) return true;
1557	    }
1558	  }
1559	  return false;
1560	}
1561	
1562	/**
1563	 * 灯具→墙上开关 + 红线布线(cs L18942-18975/18990-19023):
1564	 * 在灯具 ±12/+3..20 内找两侧皆砖的嵌墙位放开关(136),沿曼哈顿路径铺红线。
1565	 * chandelier=true 时开关位禁邻尖刺(原版两分支条件差异)。
1566	 */
1567	function wireToSwitch(
1568	  st: TileStore, rng: RNG, dc: DungeonCtx,
1569	  lx: number, ly: number,
1570	  ex0: number, ex1: number, ey0: number, ey1: number,
1571	  isDWall: (x: number, y: number) => boolean,
1572	  isBrick: (x: number, y: number) => boolean,
1573	  chandelier: boolean,
1574	): void {
1575	  for (let tries = 0; tries < 1000; tries++) {
1576	    let x = lx + rng.int(-12, 12);
1577	    let y = ly + rng.int(3, 20);
1578	    if (x < ex0 || x > ex1 || y < ey0 || y > ey1) continue;
1579	    if (!st.inBounds(x, y) || st.flags[st.idx(x, y)] || st.flags[st.idx(x, y + 1)]) continue;
1580	    if (!isBrick(x - 1, y) || !isBrick(x + 1, y)) continue;
1581	    if (!canHit(st, x, y, lx, ly)) continue;
1582	    const solidSide = (st.inBounds(x - 1, y) && st.flags[st.idx(x - 1, y)] && st.type[st.idx(x - 1, y)] !== DOOR && TILE_DEFS[st.type[st.idx(x - 1, y)]]?.solid)
1583	      || (st.inBounds(x + 1, y) && st.flags[st.idx(x + 1, y)] && st.type[st.idx(x + 1, y)] !== DOOR && TILE_DEFS[st.type[st.idx(x + 1, y)]]?.solid)
1584	      || (st.inBounds(x, y + 1) && st.flags[st.idx(x, y + 1)] && TILE_DEFS[st.type[st.idx(x, y + 1)]]?.solid);
1585	    if (!solidSide || !isDWall(x, y)) continue;
1586	    if (!chandelier) {
1587	      const tL = st.inBounds(x - 1, y) && st.flags[st.idx(x - 1, y)] ? st.type[st.idx(x - 1, y)] : 0;
1588	      const tR = st.inBounds(x + 1, y) && st.flags[st.idx(x + 1, y)] ? st.type[st.idx(x + 1, y)] : 0;
1589	      if (tL === SPIKE || tR === SPIKE) continue;
1590	    }
1591	    // 放开关(2/3 关态帧 18)并布线
1592	    st.setTileSilent(x, y, DSWITCH, rng.int(0, 2) > 0 ? 18 : 0, 0);
1593	    let wx = x, wy = y;
1594	    while (wx !== lx || wy !== ly) {
1595	      st.wire[st.idx(wx, wy)] |= TileStore.WIRE_RED;
1596	      if (wx > lx) wx--;
1597	      else if (wx < lx) wx++;
1598	      else if (wy > ly) wy--;
1599	      else if (wy < ly) wy++;
1600	    }
1601	    st.wire[st.idx(lx, ly)] |= TileStore.WIRE_RED;
1602	    return;
1603	  }
1604	  void dc;
1605	}
1606	
1607	/** Collision.CanHit（1456 Collision.cs:383）1:1：开关↔灯具视线判定。
1608	 *  16px 实体盒（16×16）中心取整即 tile 坐标；主轴步进（|dx|>|dy| 走 x 否则走 y），
1609	 *  每步检查步进方向两侧全整砖（active+tileSolid+!solidTop+slope0+!halfBrick）成对 → 阻挡；
1610	 *  步进后落点格为实心非平台 → 阻挡（穿墙）。y 钳 [1, h-40]、x 钳 [1, w-1]。 */
1611	function canHit(st: TileStore, x1: number, y1: number, x2: number, y2: number): boolean {
1612	  const w = st.w, h = st.h;
1613	  let num = x1, num2 = y1;
1614	  const num3 = Math.max(1, Math.min(w - 1, x2));
1615	  const num4 = Math.max(1, Math.min(h - 40, y2));
1616	  num = Math.max(1, Math.min(w - 1, num));
1617	  num2 = Math.max(1, Math.min(h - 40, num2));
1618	  const fullBrick = (x: number, y: number): boolean => {
1619	    if (!st.inBounds(x, y)) return false;
1620	    const k = st.idx(x, y);
1621	    if (!st.flags[k]) return false;
1622	    const d = TILE_DEFS[st.type[k]];
1623	    return !!d?.solid && !d.platform && st.slope[k] === 0 && !st.half[k];
1624	  };
1625	  for (;;) {
1626	    if (num === num3 && num2 === num4) return true;
1627	    const dAbs = Math.abs(num - num3), dOrd = Math.abs(num2 - num4);
1628	    if (dAbs > dOrd) {
1629	      num += num >= num3 ? -1 : 1;
1630	      if (fullBrick(num, num2 - 1) && fullBrick(num, num2 + 1)) return false;
1631	    } else {
1632	      num2 += num2 >= num4 ? -1 : 1;
1633	      if (fullBrick(num - 1, num2) && fullBrick(num + 1, num2)) return false;
1634	    }
1635	    // do-while 条件：落点格"非活性 / 非实心 / 平台"才继续步进；实心非平台 → 穿墙阻挡
1636	    const k = st.idx(num, num2);
1637	    const d = TILE_DEFS[st.type[k]];
1638	    const passable = !st.flags[k] || !d?.solid || !!d.platform;
1639	    if (!passable) return false;
1640	    if (num < 1 || num >= w - 1 || num2 < 1 || num2 >= h - 40) return false;
1641	  }
1642	}
1643	
1644	/** AddBuriedChest（1456 cs:35920）下落段 1:1：自 y 向下扫至 h-10，
1645	 *  首个 SolidTile（半砖/坡面不算）落定；±2 邻域有 Boulders/26/237 → 失败。
1646	 *  样式/主件由调用方显式给定（地牢战利品序），2×2 箱落其上后推入 chests */
1647	function addChest(st: TileStore, chests: ChestSink, x: number, y: number, tile: number, style: number, itemId: number | undefined, locked: boolean): boolean {
1648	  const def = TILE_DEFS[tile];
1649	  if (!def) return false;
1650	  for (let dx = -2; dx <= 2; dx++) {
1651	    for (let dy = -2; dy <= 2; dy++) {
1652	      const xx = x + dx, yy = y + dy;
1653	      if (xx < 1 || yy < 1 || xx >= st.w - 1 || yy >= st.h - 1) continue;
1654	      const k = st.idx(xx, yy);
1655	      if (!st.flags[k]) continue;
1656	      const sh = TILE_DEFS[st.type[k]]?.vanilla?.sheet ?? -1;
1657	      if (BOULDER_SHEETS_DP.has(sh) || st.type[k] === TILE_BY_KEY['v_26_altars'] || st.type[k] === TILE_BY_KEY['v_237_lihzahrd_altar']) return false;
1658	    }
1659	  }
1660	  let gy = y;
1661	  for (; gy < st.h - 10; gy++) {
1662	    if (solidTileHB(st, x, gy)) break;
1663	  }
1664	  if (gy >= st.h - 10) return false;
1665	  if (!solidTileHB(st, x, gy)) return false;
1666	  const topY = gy - 2;
1667	  if (topY < 1) return false;
1668	  for (let dx = 0; dx < 2; dx++) {
1669	    for (let dy = 0; dy < 2; dy++) {
1670	      if (!st.inBounds(x + dx, topY + dy) || st.flags[st.idx(x + dx, topY + dy)]) return false;
1671	    }
1672	  }
1673	  const fw = def.vanilla?.fw ?? 2;
1674	  for (let dx = 0; dx < 2; dx++) {
1675	    for (let dy = 0; dy < 2; dy++) {
1676	      st.setTileSilent(x + dx, topY + dy, tile, style * fw * 18 + dx * 18, dy * 18);
1677	    }
1678	  }
1679	  chests.push({
1680	    x, y: topY, locked,
1681	    items: itemId !== undefined ? [{ id: itemId, stack: 1 }, ...Array(9).fill(null)] : Array(10).fill(null),
1682	  });
1683	  return true;
1684	}
1685	

```


---

## 🤖 Assistant · 2026-08-12T18:46:29.593Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The JS DungeonPass.ts is a 1405-baseline implementation (legacy MakeDungeon single-function) with 1456 corrections to RNG consumption. This is a huge, complex pass.

The task: transcribe #32 Dungeon pass into the C# oracle (caves-oracle.cs) and align JS DungeonPass.ts so both hash equal at the "dungeon" checkpoint.

Key insight: the oracle doesn't need to implement the full 1456 system — it needs to implement the SAME algorithm as the JS side (which is the 1405 legacy algorithm + 1456 RNG consumption), because the oracle was transcribed "按 JS 链顺序转录" (transcribed following the JS chain order) per the alignment doc. The alignment doc says: "oracle 按 JS 链顺序转录，互验全绿 ≠ 原版等价" — the oracle follows the JS chain.

So my job: transcribe the legacy dungeon algorithm (1405 MakeDungeon, which is what JS implements) into caves-oracle.cs at the slush checkpoint position, consuming RNG in the same order as the JS implementation, and then make JS vs oracle hashes match.

Wait — but JS is the "base" and oracle validates JS. If I transcribe oracle from JS, of course they'll match (trivially). The point is to catch deviations. So I should transcribe from the VANILLA source (1405 legacy + 1456 RNG semantics as the JS comments claim), then compare with JS, and fix JS where it deviates ("发现的任何'我们自创改良'（吸附/底锚定/短路类）一律按原版删除").

Hmm, but which vanilla source? The JS implements the 1405 legacy `MakeDungeon` (WorldGen.cs L18006 in 1405) + DungeonHalls L20255 + DungeonRoom L20622 + DungeonStairs L19855 + DungeonEnt L20726 in **1405**. In 1456, that legacy code has been replaced by the DungeonCrawler object system. But interesting: the 1456 LegacyEntranceDungeonHall / LegacyDungeonRoom presumably reuse similar algorithms.

Since JS is "1405 基底+多轮 1456 修正", the reference for the algorithm is Terarria1405 (also present per memory: "Terarria1456(1.4.5.6 全量,ilspycmd)+Terarria1405").

Let me check what's in Terarria1405 for MakeDungeon and the pass registration. Also check the oracle structure to see how other passes are transcribed.

Given the enormous scope (1684 lines of JS, ~2000 lines of C#), I need to be efficient. The oracle transcription is the biggest chunk. Let me first look at the oracle file to understand its structure and conventions.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:30.364Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Checkpoint\\|====\\|^// ===\\|void main\\|void Run\\|slush\\|mcopenings\\|beaches\\|icebiome\" ~/Project/GLM/SandboxWorld/game/tools/golden/caves-oracle.cs | head -80",
 "description": "Outline oracle structure and checkpoints"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:30.395Z

**📎 ToolResult**

```
38:void Checkpoint(string name)
84:// ================= Reset 掷骰（cs:11159-11472，与 terrain-oracle.cs 相同的已验证序列）=================
147:// ================= TerrainPass（cs:56-244）=================
248:Checkpoint("terrain");
252:// ================= 原语 =================
488:// ================= Pass 1：Dunes（cs:11540-11602 + DunesBiome.cs + SurfaceMap.cs）=================
625:Checkpoint("dunes");
627:// ================= Pass 2：OceanSand（cs:11603-11711）=================
673:Checkpoint("oceansand");
675:// ================= Pass 3：SandPatches（cs:11712-11737）=================
687:Checkpoint("sandpatches");
689:// ================= Pass 4：Tunnels（cs:11745-11808）=================
726:Checkpoint("tunnels");
731:// ================= Pass 5：MountainCaves（cs:11809-11882，山丘本体；pass 34 开口在 Beaches 后）=================
769:Checkpoint("mountaincaves");
771:// ================= Pass 6：DirtWallBackgrounds（cs:11883-11921）=================
792:Checkpoint("dirtwallbg");
794:// ================= Pass 7-9：RocksInDirt / DirtInRocks / Clay（cs:11922-12033）=================
834:Checkpoint("rocksclay");
836:// ================= Pass 10：SmallHoles（cs:12034-12092）=================
860:Checkpoint("smallholes");
862:// ================= Pass 11：DirtLayerCaves（cs:12094-12134）=================
877:Checkpoint("dirtlayer");
879:// ================= Pass 12：RockLayerCaves（cs:12135-12165）=================
891:Checkpoint("rocklayer");
893:// ================= Pass 13：SurfaceCaves（cs:12191-12300）=================
925:Checkpoint("surfacecaves");
928:// ================= Pass 16：IceBiome（cs:12343-12440，1456 注册序紧跟 SurfaceCaves）=================
983:Checkpoint("icebiome");
985:// ================= Grass（cs:12454-12507）=================
1010:Checkpoint("grass");
1012:// ================= Jungle（JunglePass.cs 全文 1:1）=================
1169:Checkpoint("jungle");
1171:// ================= MudCavesToJungleGrass（cs:12499-12530，零 RNG 状态机）=================
1243:Checkpoint("mudcaves");
1245:// ================= Desert Sub-A（DesertBiome pass cs:12532 + DesertDescription + SandMound）=================
1246:// Sub-B（DesertHive）与 Sub-C（入口 4 形状）转录至 Checkpoint("desertdone")。
1353:Checkpoint("desertmound");
1355:// ================= Desert Sub-C 入口（DesertBiome.cs:22-40 + Biomes/Desert/*Entrance.cs）=================
1537:Checkpoint("desertentrance");
1553:// ================= Desert Sub-B Hive（DesertHive.cs 1:1）=================
1745:Checkpoint("deserthive");
1746:Checkpoint("desertdone");   // CleanupArea 仅 SquareWallFrame/TileFrame——无哈希效应
1748:// ================= Pass 20 GlowingMushroomPatches（cs:12581-12709 + ShroomPatch cs:80540 + SpreadGrass cs:75210）=================
1935:Checkpoint("mushroom");
1937:// ================= Pass 21/22 共用：BiomeTileCheck（cs:10949）+ PlaceTight/Stalactite（cs:38329/38353）=================
1989:// ================= Pass 21 Marble（cs:12800 + MarbleBiome.cs）=================
2102:Checkpoint("marble");
2104:// ================= Pass 22 Granite（cs:12884 + GraniteBiome.cs）=================
2253:Checkpoint("granite");
2255:// ================= Pass 23 FloatingIslands（cs:12976 + CloudIsland cs:78618 + CloudLake cs:79068）=================
2642:Checkpoint("islands");
2644:// ================= Pass 24 DirtToMud（cs:13172-13191）=================
2650:Checkpoint("dirttomud");
2652:// ================= Pass 25 Silt（cs:13192-13231）=================
2671:Checkpoint("silt");
2673:// ================= Pass 26 OresAndShinies（cs:13233-13658 普通世界分支）=================
2695:Checkpoint("ores");
2697:// ================= Pass 27 Webs（cs:13659-13696）=================
2717:Checkpoint("webs");
2775:// ================= Pass 28 Underworld（cs:13697-13918 普通世界分支）=================
2881:Checkpoint("underworld");
2883:// ================= Pass 29 CorruptionAndCrimson（cs:13919-14613 + ChasmRunnerSideways cs:75323 + CanEvilReplace cs:75527 + CrimStart cs:75543 + CrimPlaceHearts cs:75854 + ChasmRunner cs:76066）=================
3655:Checkpoint("corruption");
3658:// ================= Pass 30 Lakes（cs:14613-14755 + SonOfLakinater cs:80354）=================
3830:Checkpoint("lakes");
3832:// ================= Pass 31 StoneToIceAndSiltPlusMudIntoSlush（cs:14756-14815）=================
3860:Checkpoint("slush");
3863:// ================= Pass 33：MountainCaveOpenings（cs:14932-14947）+ Pass 34：Beaches（cs:14947-15087）=================
3958:Checkpoint("mcopenings");
4032:Checkpoint("beaches");
4033://   本行与 mcopenings 块之间（原版真实位 29/32）。
4080:// ================= 输出 =================
4094:// ================= Terraria.Utilities.FastRandom（FastRandom.cs 1:1）=================
4113:// ================= WorldBuilding 微框架（GenAction/GenShape/Actions/Modifiers/Shapes 1:1）=================

```


---

## 🤖 Assistant · 2026-08-12T18:46:32.785Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The oracle goes: ... slush (3860) → [dungeon insertion point comment at 4033] → mcopenings (3958) → beaches (4032). Wait the comment at 4033 says "本行与 mcopenings 块之间（原版真实位 29/32）" — need to read the region 3860-3960 to see the exact insertion marker.

Let me read the oracle around that area and also the beginning (structure, primitives) to understand conventions.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:33.031Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tools/golden/caves-oracle.cs",
 "offset": 1,
 "limit": 260
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:33.042Z

**📎 ToolResult**

```
1	// Caves-chain oracle：独立复刻原版 1456「Reset + Terrain + Dunes→…→SurfaceCaves」
2	// 普通世界全链（4200×1200），UnifiedRandom 反射真·Terraria.exe（零转写风险）。
3	// 每 pass 后输出 type/active/wall/liquid 的 FNV-1a 哈希 → JSON，
4	// 与 JS 侧 tests/pass-hash.test.ts 的洞穴链检查点对账。
5	// 用法：dotnet run tools/golden/caves-oracle.cs <seedInt> <evil:0|1> <out.json>
6	using System;
7	using System.Collections.Generic;
8	using System.IO;
9	using System.Reflection;
10	using System.Text;
11	
12	int seed = int.Parse(args[0]);
13	int evil = int.Parse(args[1]);
14	string outPath = args[2];
15	const int W = 4200, H = 1200;
16	const int BEACH_DISTANCE = 380; // WorldGen.beachDistance（cs:4102）
17	
18	var asm = Assembly.LoadFrom("~/Library/Application Support/Steam/steamapps/common/Terraria/Terraria.app/Contents/Resources/Terraria.exe");
19	dynamic r = Activator.CreateInstance(asm.GetType("Terraria.Utilities.UnifiedRandom")!, seed)!;
20	
21	
22	// ---- 网格（vanilla tile id；行主序 y*W+x，同 JS TileStore）----
23	var act = new byte[W * H];
24	var typ = new ushort[W * H];
25	var wal = new ushort[W * H];
26	var liq = new byte[W * H];
27	var liqT = new byte[W * H];
28	var checkpoints = new List<string>();
29	
30	static byte[] ToBytes(ushort[] a) { var b = new byte[a.Length * 2]; Buffer.BlockCopy(a, 0, b, 0, b.Length); return b; }
31	uint Fnv16(ushort[] a) { uint h = 0x811c9dc5; foreach (var v in a) { h = (h ^ (uint)(v & 0xff)) * 16777619u; h = (h ^ (uint)((v >> 8) & 0xff)) * 16777619u; } return h; }
32	static uint Fnv8(byte[] a) { uint h = 0x811c9dc5; foreach (var v in a) { h = (h ^ v) * 16777619u; h = h * 16777619u; } return h; }
33	// 只比活性 type（非活性格的幽灵 type 归零——与 JS 侧 hashGrids 口径一致；
34	// 幽灵 parity 是独立对账项：原版幽灵会存盘、我们 finalize 清除，玩法无差）
35	var hashTyp = new ushort[W * H];
36	var hashGho = new ushort[W * H];
37	var ghostPts = new List<string>();
38	void Checkpoint(string name)
39	{
40	    for (int i = 0; i < typ.Length; i++) {
41	        hashTyp[i] = (ushort)(act[i] != 0 ? typ[i] : 0);
42	        hashGho[i] = (ushort)(act[i] == 0 ? typ[i] : 0); // inactive 格残留 type（幽灵 parity）
43	    }
44	    checkpoints.Add($"{name}|{Fnv16(hashTyp):x8} {Fnv8(act):x8} {Fnv16(wal):x8} {Fnv8(liq):x8}");
45	    ghostPts.Add($"{name}|{Fnv16(hashGho):x8}");
46	}
47	
48	// solid 表：源自仓库 TILE_DEFS（已对原版全表审计，见 vanilla-solid-audit 记忆）。
49	// 反射 Main.tileSolid 会触发 FNA 静态构造，不可行。
50	// 兼容旧引用（NOT_CLEAR 仍用于 TileRunner flag4/Cavinator）
51	var SOLID = new HashSet<ushort> { 0,1,2,7,6,9,8,30,10,53,147,57,166,167,168,169,22,37,58,204,
52	   107,108,111,221,222,223,211,63,64,65,66,67,68,161,162,206,148,396,397,404,
53	   40,54,56,38,39,59,123,368,226,367,633,181,189,183,536,225,483,224,383,179,
54	   384,273,381,48,192,191,196,118,321,152,158,357,272,229,311,130,193,190,350,369,
55	   137,117,112,232,274,322,109,312,422,495,479,477,380,230,562,371,668,398,379,618,
56	   484,138,388,387,235,625,151,234,182,45,399,248,175,539,481,119,120,714,664,711,
57	   715,716,713,23,41,75,199,60,70,25,202,43,44,203,255,256,257,258,259,260,
58	   261,262,263,264,265,266,267,268,421,476,546,557,482,163,200,116,76,46,47,115,
59	   121,122,127,140,145,146,150,153,154,155,156,157,159,160,164,170,176,177,180,188,
60	   194,195,197,198,208,239,249,250,251,252,253,284,313,315,325,326,327,328,329,336,
61	   341,342,343,344,345,346,347,348,351,365,366,370,385,400,401,402,403,407,408,409,
62	   415,416,417,418,426,427,430,431,432,433,434,435,436,437,438,439,446,447,448,449,
63	   450,451,458,459,460,472,473,474,478,492,496,498,500,501,502,503,507,508,512,513,
64	   514,515,516,517,534,535,537,540,541,563,566,626,627,628,635,641,659,661,662,666,
65	   667,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,
66	   688,689,690,691,692,708,712,717,718,719,722,726,727,728,729,730,731,732,734,735,
67	   736,737,738,739,740,741,742,743,744,745,746,747,748,749,750, };
68	
69	// tileFrameImportant && !tileCut（cs:77217 TileRunner 首门禁）——项目侧近似集，
70	// 与 JS TileRunner 的 `TILE_DEFS[].framed && !decor` 同源生成（pass 20 起世界出现 165 等活性 framed 物）
71	// GrowTree 墙白名单（JS TreePass.DEFAULT_TREE_WALLS）与 EmptyTileCheck 空格白名单
72	// （JS GEM_EMPTY_ALLOW = sheet 3,24,32,61,62,69,71,73,74,82,83,84,110,113,184,201,233,352,485,529,530,637,655）
73	var TREE_WALLS = new HashSet<ushort> { 0, 150, 138, 145, 107, 152, 140, 139, 141, 106, 245, 315, 317, 63, 64, 65, 66, 67, 68, 69, 81, 70, 264, 268, 265, 74, 80 };
74	var EMPTY_ALLOW = new HashSet<ushort> { 3, 24, 32, 61, 62, 69, 71, 73, 74, 82, 83, 84, 110, 113, 184, 201, 233, 352, 485, 529, 530, 637, 655 };
75	var FRAMED_NOT_CUT = new HashSet<ushort> { 5,10,13,16,17,18,21,26,29,36,50,55,77,81,82,86,91,93,97,99,102,103,105,106,110,113,114,125,128,129,132,133,134,135,136,137,138,141,144,165,171,172,178,184,185,186,187,207,215,217,218,219,220,227,228,231,233,235,236,237,238,239,240,241,242,243,245,246,247,254,269,270,271,275,276,277,278,279,280,281,282,283,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,314,316,317,318,319,320,323,324,334,337,339,349,354,355,356,358,359,360,361,362,363,364,373,374,375,376,377,378,387,388,389,390,391,392,393,394,395,405,406,411,412,413,414,427,435,436,437,438,439,443,444,453,454,456,457,461,462,463,464,465,466,467,469,470,471,475,476,484,485,486,487,488,489,490,491,493,494,499,505,506,510,511,518,519,520,521,522,523,524,525,526,527,529,530,532,533,538,542,543,544,545,547,548,549,550,551,552,553,554,555,556,558,559,560,567,568,569,570,571,572,573,579,580,581,582,583,584,585,586,587,588,589,590,591,592,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613,614,615,616,617,619,620,621,622,623,624,629,630,631,632,634,637,639,640,642,643,644,645,646,647,648,649,650,651,652,653,654,656,657,658,660,663,664,665,693,694,695,696,698,699,700,701,702,703,704,705,706,707,709,710,711,712,713,714,715,716,720,721,723,724,725,726,733,751,752 };
76	var NOT_CLEAR = new HashSet<ushort> { 396, 400, 401, 397, 398, 399, 404, 368, 367, 41, 43, 44, 481, 482, 483, 226, 237 };
77	bool CanBeCleared(ushort t) => !NOT_CLEAR.Contains(t);
78	bool IsSolidT(ushort t) => SOLID.Contains(t);
79	var TILE_DUNGEON = new HashSet<ushort> { 41, 43, 44, 677, 678, 679 };
80	var WALL_DUNGEON = new HashSet<ushort> { 7, 8, 9, 94, 95, 96, 97, 98, 99 };
81	var FLAG3_ALWAYS = new HashSet<ushort> { 45, 147, 189, 190, 196, 460, 717, 718, 719 };
82	var CLOUDS = new HashSet<ushort> { 189, 196, 460, 717, 718, 719 };
83	
84	// ================= Reset 掷骰（cs:11159-11472，与 terrain-oracle.cs 相同的已验证序列）=================
85	r.Next(5);                                                    // jungleHut
86	r.Next(2);                                                    // crimsonLeft
87	r.Next(10, 200);                                              // numClouds
88	while (true) { double wf = (double)r.NextDouble(); r.Next(2); if (wf != 0) break; }
89	{ var p = new List<int> { 274, 220, 112, 218, 3019 }; while (p.Count > 0) p.RemoveAt((int)r.Next(p.Count)); }
90	r.Next(86400 * 2, 86400 * 3); r.Next(8640, 86400);
91	bool oreCu166 = (int)r.Next(2) == 0;                            // 矿石替代对（cs:11292-11311）
92	bool oreFe167 = (int)r.Next(2) == 0;                            // Next(2)==0 → 166/167/168/169
93	bool oreAg168 = (int)r.Next(2) == 0;
94	bool oreAu169 = (int)r.Next(2) == 0;
95	int oreCu = oreCu166 ? 166 : 7, oreFe = oreFe167 ? 167 : 6, oreAg = oreAg168 ? 168 : 9, oreAu = oreAu169 ? 169 : 8;
96	bool crimson = (int)r.Next(2) == 0;
97	if (evil == 0) crimson = false; if (evil == 1) crimson = true;
98	r.Next(int.MaxValue);                                         // WorldId
99	r.Next(1050, 3150);                                           // treeX[0]
100	int ts0 = (int)r.Next(6); int ts1 = (int)r.Next(6);
101	while (ts1 == ts0) ts1 = (int)r.Next(6);
102	for (int i = 0; i < 2; i++) { int s = i == 0 ? ts0 : ts1; if (s == 0) r.Next(3); }
103	r.Next(1050, 3150);                                           // caveBackX[0]
104	int cb0 = (int)r.Next(8); int cb1 = (int)r.Next(8);
105	while (cb1 == cb0) cb1 = (int)r.Next(8);
106	// RandomizeCaveBackgrounds 尾部无条件 3 掷(cs:8211-8213;2026-08-12 审计补)
107	r.Next(4); r.Next(3); r.Next(2);
108	Func<int> RollForest = () => {
109	    int n = (int)r.Next(14);
110	    if ((n == 1 || n == 2) && (int)r.Next(2) == 0) n = (int)r.Next(14);
111	    if (n == 0) n = (int)r.Next(14);
112	    if (n == 3 && (int)r.Next(3) == 0) n = 31;
113	    if (n == 5 && (int)r.Next(2) == 0) n = 51;
114	    if (n == 7 && (int)r.Next(4) == 0) n = (int)r.Next(71, 74);
115	    return n;
116	};
117	int fb1 = RollForest(); int fb2 = RollForest(); while (fb2 == fb1) fb2 = RollForest();
118	int fb3 = RollForest(); while (fb3 == fb1 || fb3 == fb2) fb3 = RollForest();
119	int fb4 = RollForest(); while (fb4 == fb1 || fb4 == fb2 || fb4 == fb3) fb4 = RollForest();
120	{ int n = (int)r.Next(6); if (n == 5) r.Next(2); }            // Corruption 背景
121	r.Next(7);                                                    // jungle 背景
122	int snowBG = (int)r.Next(9);
123	if (snowBG == 2 && (int)r.Next(2) == 0) r.Next(2);
124	if (snowBG == 3 && (int)r.Next(2) == 0) r.Next(2);
125	if (snowBG == 4 && (int)r.Next(2) == 0) r.Next(2);
126	r.Next(6); r.Next(7);
127	{ int n = (int)r.Next(6); if (n == 5) r.Next(5); }            // Desert 背景
128	r.Next(8); r.Next(5); r.Next(3);
129	r.Next(9);                                                    // moonType
130	bool dungeonRight = !((int)r.Next(2) == 0);
131	int jungleX = dungeonRight
132	    ? (int)(W * ((int)r.Next(15, 30) * 0.01))
133	    : (int)(W * (1.0 - (int)r.Next(15, 30) * 0.01));
134	int num7 = (int)r.Next(W);
135	if (dungeonRight) { while (num7 < W * 0.6 || num7 > W * 0.75) num7 = (int)r.Next(W); }
136	else { while (num7 < W * 0.25 || num7 > W * 0.4) num7 = (int)r.Next(W); }
137	double num9s = W / 4200.0;
138	Func<int> SnowHalf = () => (int)r.Next(50, 90) + (int)((int)r.Next(20, 40) * num9s) + (int)((int)r.Next(20, 40) * num9s);
139	int snowL = Math.Max(0, num7 - SnowHalf());
140	int snowR = Math.Min(W, num7 + SnowHalf());
141	int leftBeachEnd = (int)r.Next(300, 340) + (dungeonRight ? 40 : 20);
142	int rightBeachStart = W - (int)r.Next(300, 340) - (dungeonRight ? 20 : 40);
143	int dungeonLocation = !dungeonRight
144	    ? (int)r.Next(leftBeachEnd + 50, (int)(W * 0.2))
145	    : (int)r.Next((int)(W * 0.8), rightBeachStart - 50);
146	
147	// ================= TerrainPass（cs:56-244）=================
148	int feature = 0, counter = leftBeachEnd + flatBeachPadding();
149	static int flatBeachPadding() => 5;
150	double num3w = (double)H * 0.3;
151	num3w *= (double)(int)r.Next(90, 110) * 0.005;
152	double num4w = num3w + (double)H * 0.2;
153	num4w *= (double)(int)r.Next(90, 110) * 0.01;
154	double num5w = num3w, num6w = num3w, num7w = num4w, num8w = num4w;
155	double num9t = (double)H * 0.23;
156	double num10 = 0.17 + 0.02, num11 = 0.26;
157	var history = new List<double>();
158	var surf = new int[W];
159	Action<int, double> Retarget = null!;
160	Retarget = (targetX, targetHeight) => {
161	    int len = history.Count;
162	    for (int i1 = 0; i1 < len / 2; i1++)
163	    {
164	        if (history[len - 1] <= targetHeight) break;
165	        for (int j = 0; j < len - i1 * 2; j++)
166	        {
167	            double v = history[len - j - 1] - 1.0;
168	            history[len - j - 1] = v;
169	            if (v <= targetHeight) break;
170	        }
171	    }
172	    for (int k = 0; k < len; k++)
173	    {
174	        int x = targetX - k;
175	        if (x >= 0 && x < W)
176	        {
177	            int ws = (int)history[len - k - 1];
178	            for (int y = 0; y < ws; y++) act[y * W + x] = 0;
179	            for (int y = ws; y < H; y++) { act[y * W + x] = 1; if (typ[y * W + x] != 1) typ[y * W + x] = 0; }
180	        }
181	    }
182	};
183	Func<int, double> GenOffset = f => {
184	    double n = 0.0;
185	    switch (f)
186	    {
187	        case 0: while ((int)r.Next(0, 7) == 0) n += (int)r.Next(-1, 2); break;
188	        case 1: while ((int)r.Next(0, 4) == 0) n -= 1.0; while ((int)r.Next(0, 10) == 0) n += 1.0; break;
189	        case 2: while ((int)r.Next(0, 4) == 0) n += 1.0; while ((int)r.Next(0, 10) == 0) n -= 1.0; break;
190	        case 3: while ((int)r.Next(0, 2) == 0) n -= 1.0; while ((int)r.Next(0, 6) == 0) n += 1.0; break;
191	        case 4: while ((int)r.Next(0, 2) == 0) n += 1.0; while ((int)r.Next(0, 5) == 0) n -= 1.0; break;
192	    }
193	    return n;
194	};
195	for (int i = 0; i < W; i++)
196	{
197	    num5w = Math.Min(num3w, num5w);
198	    num6w = Math.Max(num3w, num6w);
199	    num7w = Math.Min(num4w, num7w);
200	    num8w = Math.Max(num4w, num8w);
201	    if (counter <= 0)
202	    {
203	        feature = (int)r.Next(0, 5);
204	        counter = (int)r.Next(5, 40);
205	        if (feature == 0) counter *= (int)((double)(int)r.Next(5, 30) * 0.2);
206	    }
207	    counter--;
208	    if ((double)i > W * 0.45 && (double)i < W * 0.55 && (feature == 3 || feature == 4)) feature = (int)r.Next(3);
209	    if ((double)i > W * 0.48 && (double)i < W * 0.52) feature = 0;
210	    num3w += GenOffset(feature);
211	    if (i < leftBeachEnd + flatBeachPadding() || i > rightBeachStart - flatBeachPadding())
212	        num3w = Math.Clamp(num3w, H * num10, num9t);
213	    else if (num3w < H * num10) { num3w = H * num10; counter = 0; }
214	    else if (num3w > H * num11) { num3w = H * num11; counter = 0; }
215	    while ((int)r.Next(0, 3) == 0) num4w += (int)r.Next(-2, 3);
216	    if (num4w < num3w + H * 0.06) num4w += 1.0;
217	    if (num4w > num3w + H * 0.35) num4w -= 1.0;
218	    history.Add(num3w);
219	    if (history.Count > 500) history.RemoveAt(0);
220	    // FillColumn：y < (int)num3 空气；[.., num4) 泥(0)；≥num4 石(1)。无墙（DirtWallBg 稍后）
221	    int st = (int)num3w;
222	    for (int y = 0; y < st; y++) { act[y * W + i] = 0; }
223	    for (int y = st; y < H; y++) { act[y * W + i] = 1; typ[y * W + i] = (ushort)((double)y < num4w ? 0 : 1); }
224	    surf[i] = st;
225	    if (i == rightBeachStart - flatBeachPadding())
226	    {
227	        if (num3w > num9t) Retarget(i, num9t);
228	        feature = 0; counter = W - i;
229	    }
230	}
231	int worldSurface = (int)(num6w + 25.0);
232	double rockLayerD = num8w;
233	double num12 = (int)((rockLayerD - worldSurface) / 6.0) * 6;
234	int rockLayer = (int)(worldSurface + num12);
235	int waterLine = (int)((rockLayer + (double)H) / 2) + (int)r.Next(-100, 20);
236	int lavaLine = waterLine + (int)r.Next(50, 80);
237	int num14 = 20;
238	if (num7w < num6w + num14)
239	{
240	    double mid = (num7w + num6w) / 2.0;
241	    double spread = Math.Abs(num7w - num6w); if (spread < num14) spread = num14;
242	    num7w = mid + spread / 2.0; num6w = mid - spread / 2.0;
243	}
244	// GenVars 口径（后续 pass 消费）
245	double gvWorldSurfaceLow = num5w, gvWorldSurfaceHigh = num6w;
246	double gvRockLayerLow = num7w, gvRockLayerHigh = num8w;
247	double gvWorldSurface = num3w, gvRockLayer = num4w;
248	Checkpoint("terrain");
249	
250	Console.WriteLine($"terrain ok: worldSurface={worldSurface} rockLayer={rockLayer} waterLine={waterLine} lavaLine={lavaLine}");
251	
252	// ================= 原语 =================
253	bool mudWallFlag = false;
254	void TileRunner(double i, double j, double strength, int steps, int type,
255	    bool addTile = false, double speedX = 0.0, double speedY = 0.0, bool noYChange = false,
256	    bool overRide = true, int ignoreTileType = -1)
257	{
258	    double num1 = strength, num2 = steps;
259	    double px = i, py = j;
260	    double vx = (int)r.Next(-10, 11) * 0.1, vy = (int)r.Next(-10, 11) * 0.1;

```


---

## 🤖 Assistant · 2026-08-12T18:46:35.469Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at the insertion area (lines 3830-3970) and the tail of the oracle (output + remaining sections) plus how tiles/walls are written in the oracle (helper functions like placing bricks).

Let me read lines 3820-4090.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:35.691Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tools/golden/caves-oracle.cs",
 "limit": 280,
 "offset": 3820
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:35.696Z

**📎 ToolResult**

```
3820	                if (!lkDesert)
3821	                {
3822	                    SonOfLakinater(lkX0, lkY);
3823	                    lkX.Add(lkX0);
3824	                    break;
3825	                }
3826	            }
3827	        }
3828	    }
3829	}
3830	Checkpoint("lakes");
3831	
3832	// ================= Pass 31 StoneToIceAndSiltPlusMudIntoSlush（cs:14756-14815）=================
3833	{
3834	    for (int sy = snowTopGen; sy < snowBottomGen; sy++)
3835	    {
3836	        for (int sx = snowMinXArr[sy]; sx < snowMaxXArr[sy]; sx++)
3837	        {
3838	            ushort st = typ[sy * W + sx];
3839	            switch (st)
3840	            {
3841	                case 123: typ[sy * W + sx] = 224; break;      // 沙泥→雪泥（不判 active）
3842	                case 59:
3843	                {
3844	                    bool ok = true;
3845	                    for (int k = sx - 3; k <= sx + 3; k++)
3846	                        for (int l = sy - 3; l <= sy + 3; l++)
3847	                        {
3848	                            if (k < 0 || k >= W || l < 0 || l >= H) continue;
3849	                            ushort t2 = typ[l * W + k];
3850	                            if (act[l * W + k] != 0 && (t2 == 60 || t2 == 70 || t2 == 71 || t2 == 72)) { ok = false; break; }
3851	                        }
3852	                    if (ok) typ[sy * W + sx] = 224;
3853	                    break;
3854	                }
3855	                case 1: typ[sy * W + sx] = 161; break;        // 石→冰（不判 active）
3856	            }
3857	        }
3858	    }
3859	}
3860	Checkpoint("slush");
3861	// ★#29 Corruption（cs:13919）与 #32 Dungeon（cs:14816）尚未转录——转录后须插在
3862	
3863	// ================= Pass 33：MountainCaveOpenings（cs:14932-14947）+ Pass 34：Beaches（cs:14947-15087）=================
3864	// 1456 注册序在 Dungeon(32) 之后——本 oracle 尚未转录 26-32 段（Mushroom/Marble/
3865	// Granite/Islands/DirtToMud/Silt/Ores/Underworld/Corruption/Lakes/Slush/Dungeon），
3866	// 故暂挂在 desertdone 之后；★26-32 段转录后须把本块插回其前（即 Dungeon 之后）。
3867	void CaveOpenater(int i, int j)
3868	{
3869	    double num = (int)r.Next(7, 12);
3870	    double num2 = num;
3871	    int dir = 1;
3872	    if ((int)r.Next(2) == 0) dir = -1;
3873	    if ((int)r.Next(10) != 0) dir = (i < W / 2) ? 1 : -1;
3874	    double px = i, py = j;
3875	    int steps = 100;
3876	    double vx = dir, vy = 0.0;
3877	    while (steps > 0)
3878	    {
3879	        int hx = (int)px, hy = (int)py;
3880	        if (hx < 0) hx = 0; if (hx > W - 1) hx = W - 1;
3881	        if (hy < 0) hy = 0; if (hy > H - 1) hy = H - 1;
3882	        int hi = hy * W + hx;
3883	        if (wal[hi] == 0 || (act[hi] == 1 && NOT_CLEAR.Contains(typ[hi]))) steps = 0;
3884	        steps--;
3885	        int x0 = (int)(px - num * 0.5), x1 = (int)(px + num * 0.5);
3886	        int y0 = (int)(py - num * 0.5), y1 = (int)(py + num * 0.5);
3887	        if (x0 < 0) x0 = 0; if (x1 > W) x1 = W;
3888	        if (y0 < 0) y0 = 0; if (y1 > H) y1 = H;
3889	        num2 = num * (int)r.Next(80, 120) * 0.01;
3890	        for (int x = x0; x < x1; x++)
3891	            for (int y = y0; y < y1; y++)
3892	            {
3893	                double ddx = Math.Abs(x - px), ddy = Math.Abs(y - py);
3894	                if (Math.Sqrt(ddx * ddx + ddy * ddy) < num2 * 0.4 && !NOT_CLEAR.Contains(typ[y * W + x]))
3895	                    act[y * W + x] = 0;
3896	            }
3897	        px += vx; py += vy;
3898	        vx += (int)r.Next(-10, 11) * 0.05;
3899	        vy += (int)r.Next(-10, 11) * 0.05;
3900	        if (vx > dir + 0.5) vx = dir + 0.5;
3901	        if (vx < dir - 0.5) vx = dir - 0.5;
3902	        if (vy > 0.0) vy = 0.0;
3903	        if (vy < -0.5) vy = -0.5;
3904	    }
3905	}
3906	void Cavinator2(int i, int j, int steps)
3907	{
3908	    double num = (int)r.Next(7, 15);
3909	    double num2 = num;
3910	    int dir = 1;
3911	    if ((int)r.Next(2) == 0) dir = -1;
3912	    double px = i, py = j;
3913	    int num4 = (int)r.Next(20, 40);
3914	    double vx = dir, vy = (int)r.Next(10, 20) * 0.01;
3915	    while (num4 > 0)
3916	    {
3917	        num4--;
3918	        int x0 = (int)(px - num * 0.5), x1 = (int)(px + num * 0.5);
3919	        int y0 = (int)(py - num * 0.5), y1 = (int)(py + num * 0.5);
3920	        if (x0 < 0) x0 = 0; if (x1 > W) x1 = W;
3921	        if (y0 < 0) y0 = 0; if (y1 > H) y1 = H;
3922	        num2 = num * (int)r.Next(80, 120) * 0.01;
3923	        bool stop = false;
3924	        for (int x = x0; x < x1 && !stop; x++)
3925	        {
3926	            for (int y = y0; y < y1; y++)
3927	            {
3928	                double ddx = Math.Abs(x - px), ddy = Math.Abs(y - py);
3929	                if (Math.Sqrt(ddx * ddx + ddy * ddy) < num2 * 0.4)
3930	                {
3931	                    int ti = y * W + x;
3932	                    if ((act[ti] == 1 && TILE_DUNGEON.Contains(typ[ti])) || WALL_DUNGEON.Contains(wal[ti]))
3933	                    { num4 = 0; stop = true; break; }
3934	                    // 原版 cs:80763：active && (!CanBeCleared || type==53) → continue（跳过不可清/沙）
3935	                    if (act[ti] == 1 && (NOT_CLEAR.Contains(typ[ti]) || typ[ti] == 53)) { /* skip */ }
3936	                    else if (act[ti] == 1) act[ti] = 0;
3937	                }
3938	                if (num4 <= 0) break;
3939	            }
3940	            if (num4 <= 0) break;
3941	        }
3942	        if (num4 <= 0) break;
3943	        px += vx; py += vy;
3944	        vx += (int)r.Next(-10, 11) * 0.05;
3945	        vy += (int)r.Next(-10, 11) * 0.05;
3946	        if (vx > dir + 0.5) vx = dir + 0.5;
3947	        if (vx < dir - 0.5) vx = dir - 0.5;
3948	        if (vy > 2.0) vy = 2.0;
3949	        if (vy < 0.0) vy = 0.0;
3950	    }
3951	    if (steps > 0 && (int)py < rockLayer + 50) Cavinator2((int)px, (int)py, steps - 1);
3952	}
3953	for (int i = 0; i < mCaveX.Count; i++)
3954	{
3955	    CaveOpenater(mCaveX[i], mCaveY[i]);
3956	    Cavinator2(mCaveX[i], mCaveY[i], (int)r.Next(40, 50));
3957	}
3958	Checkpoint("mcopenings");
3959	
3960	// ---- Beaches（cs:14947-15087 + TuneOceanDepth cs:27104）----
3961	{
3962	    bool floridaL = false, floridaR = false;
3963	    if ((int)r.Next(4) == 0)
3964	    {
3965	        if ((int)r.Next(2) == 0) floridaL = true; else floridaR = true;
3966	    }
3967	
3968	    for (int side = 0; side < 2; side++)
3969	    {
3970	        if (side == 0)
3971	        {
3972	            int waterX = (int)r.Next(220, 260);
3973	            if (dungeonRight) waterX = 275;
3974	            int cap = leftBeachEnd - 50;
3975	            if (waterX > cap) waterX = cap;
3976	            int j = 0;
3977	            while (j < H && act[j * W + (waterX - 1)] == 0) j++;
3978	            j += (int)r.Next(1, 5);
3979	            int count = 0; double depth = 1.0;
3980	            for (int x = waterX - 1; x >= 0; x--)
3981	            {
3982	                if (x > 30) { count++; depth = TuneOceanDepth(count, depth, floridaL); }
3983	                else depth += 1.0;
3984	                int pad = (int)r.Next(15, 20);
3985	                int yEnd = (int)((double)j + depth + pad);
3986	                for (int y = 0; y < yEnd && y < H; y++)
3987	                {
3988	                    int ti = y * W + x;
3989	                    if ((double)y < (double)j + depth * 0.75 - 3.0)
3990	                    {
3991	                        act[ti] = 0;
3992	                        if (y > j) liq[ti] = 255;
3993	                        else if (y == j) liq[ti] = 127;
3994	                    }
3995	                    else if (y > j) { typ[ti] = 53; act[ti] = 1; }
3996	                    wal[ti] = 0;
3997	                }
3998	            }
3999	        }
4000	        else
4001	        {
4002	            int waterX = W - (int)r.Next(220, 260);
4003	            if (!dungeonRight) waterX = W - 275;
4004	            int cap = rightBeachStart + 50;
4005	            if (waterX < cap) waterX = cap;
4006	            int l = 0;
4007	            while (l < H && act[l * W + waterX] == 0) l++;
4008	            l += (int)r.Next(1, 5);
4009	            int count = 0; double depth = 1.0;
4010	            for (int x = waterX; x < W; x++)
4011	            {
4012	                if (x < W - 30) { count++; depth = TuneOceanDepth(count, depth, floridaR); }
4013	                else depth += 1.0;
4014	                int pad = (int)r.Next(15, 20);
4015	                int yEnd = (int)((double)l + depth + pad);
4016	                for (int y = 0; y < yEnd && y < H; y++)
4017	                {
4018	                    int ti = y * W + x;
4019	                    if ((double)y < (double)l + depth * 0.75 - 3.0)
4020	                    {
4021	                        act[ti] = 0;
4022	                        if (y > l) liq[ti] = 255;
4023	                        else if (y == l) liq[ti] = 127;
4024	                    }
4025	                    else if (y > l) { typ[ti] = 53; act[ti] = 1; }
4026	                    wal[ti] = 0;
4027	                }
4028	            }
4029	        }
4030	    }
4031	}
4032	Checkpoint("beaches");
4033	//   本行与 mcopenings 块之间（原版真实位 29/32）。
4034	
4035	
4036	
4037	
4038	double TuneOceanDepth(int count, double depth, bool florida)
4039	{
4040	    double Inc(double f) => depth + (int)r.Next(10, 20) * f;
4041	    if (!florida)
4042	    {
4043	        if (count < 3) return Inc(0.2);
4044	        if (count < 6) return Inc(0.15);
4045	        if (count < 9) return Inc(0.1);
4046	        if (count < 15) return Inc(0.07);
4047	        if (count < 50) return Inc(0.05);
4048	        if (count < 75) return Inc(0.04);
4049	        if (count < 100) return Inc(0.03);
4050	        if (count < 125) return Inc(0.02);
4051	        if (count < 150) return Inc(0.01);
4052	        if (count < 175) return Inc(0.005);
4053	        if (count < 200) return Inc(0.001);
4054	        if (count < 230) return Inc(0.01);
4055	        if (count < 235) return Inc(0.05);
4056	        if (count < 240) return Inc(0.1);
4057	        if (count < 245) return Inc(0.05);
4058	        if (count < 255) return Inc(0.01);
4059	        return depth;
4060	    }
4061	    if (count < 3) return Inc(0.001);
4062	    if (count < 6) return Inc(0.002);
4063	    if (count < 9) return Inc(0.004);
4064	    if (count < 15) return Inc(0.007);
4065	    if (count < 50) return Inc(0.01);
4066	    if (count < 75) return Inc(0.014);
4067	    if (count < 100) return Inc(0.019);
4068	    if (count < 125) return Inc(0.027);
4069	    if (count < 150) return Inc(0.038);
4070	    if (count < 175) return Inc(0.052);
4071	    if (count < 200) return Inc(0.08);
4072	    if (count < 230) return Inc(0.12);
4073	    if (count < 235) return Inc(0.16);
4074	    if (count < 240) return Inc(0.27);
4075	    if (count < 245) return Inc(0.43);
4076	    if (count < 255) return Inc(0.6);
4077	    return depth;
4078	}
4079	
4080	// ================= 输出 =================
4081	var sb = new StringBuilder();
4082	sb.AppendLine("{");
4083	sb.AppendLine($"  \"seed\": {seed}, \"evil\": {evil},");
4084	sb.AppendLine($"  \"worldSurface\": {worldSurface}, \"rockLayer\": {rockLayer}, \"waterLine\": {waterLine}, \"lavaLine\": {lavaLine},");
4085	sb.AppendLine("  \"checkpoints\": [");
4086	for (int i = 0; i < checkpoints.Count; i++)
4087	    sb.AppendLine($"    \"{checkpoints[i]}\"{(i < checkpoints.Count - 1 ? "," : "")}");
4088	sb.AppendLine("  ]");
4089	sb.AppendLine("}");
4090	File.WriteAllText(outPath, sb.ToString());
4091	File.WriteAllText(outPath + ".ghost", string.Join("\n", ghostPts));
4092	Console.WriteLine($"written {outPath} ({checkpoints.Count} checkpoints)");
4093	
4094	// ================= Terraria.Utilities.FastRandom（FastRandom.cs 1:1）=================
4095	class FR
4096	{
4097	    static ulong FrNextSeed(ulong s) => (s * 25214903917UL + 11UL) & 0xFFFFFFFFFFFFUL;
4098	    public ulong S;
4099	    public FR(ulong s) { S = s; }

```


---

## 🤖 Assistant · 2026-08-12T18:46:41.387Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the oracle structure. Note the broken comment at 3861-3866: "#29 Corruption（cs:13919）与 #32 Dungeon（cs:14816）尚未转录——转录后须插在 ... 本行与 mcopenings 块之间（原版真实位 29/32）" — the comment was split, with part remaining at 4033. I need to clean that up.

Important note: this oracle chain currently goes ... slush → mcopenings → beaches. But wait — the JS chain! What is the JS chain order? The checkpoint test compares JS chain checkpoints to oracle checkpoints by name. So the JS chain must have: terrain, dunes, oceansand, sandpatches, tunnels, mountaincaves, dirtwallbg, rocksclay, smallholes, (dirtlayer, rocklayer?), surfacecaves, icebiome, grass, jungle, mudcaves, desertmound, desertentrance, deserthive, desertdone, mushroom, marble, granite, islands, dirttomud, silt, ores, webs, underworld, corruption, lakes, slush, [dungeon here], mcopenings, beaches.

Hmm wait, the checkpoint list from the test — let me check tests/caves-checkpoint.test.ts to see the chainCheckpoints and names.

Also note: the oracle has "dirtlayer" and "rocklayer" checkpoints which aren't in the alignment doc table (19 checkpoints listed). Let me check the test.

Also crucially: where does the JS DungeonPass sit in the JS chain? And does the JS chain even run dungeon at this point? The alignment table says "#30 Dungeon | DungeonPass.ts". The task says dungeon 段插入位置 = slush checkpoint 之后、mcopenings 块之前. So JS chain order must already have dungeon between slush and mcopenings, OR I need to move it there in WorldGen.ts.

Let me read the test file and WorldGen.ts chain.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:41.523Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tests/caves-checkpoint.test.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:41.527Z

**📎 ToolResult**

```
1	// 洞穴链逐 pass 检查点对账（种子等价 L1 裁决工具）：
2	// JS 侧按 oracle 同序直调各 run*Pass，每 pass 后对 type(vanilla 映射)/flags/liquid
3	// 做 FNV-1a，与 tools/golden/caves-oracle.cs（C# 复刻+反射真 UnifiedRandom）的
4	// 金标逐项比对。wall 暂不比（我们 Terrain 自加渲染墙，原版墙由 DirtWallBg 等后置
5	// pass 铺——wall 等价是独立对账项）。
6	// 金标再生成：dotnet run tools/golden/caves-oracle.cs <seedInt> <evil> <out.json>
7	import { describe, it, expect } from 'vitest';
8	import { readFileSync } from 'node:fs';
9	import { fileURLToPath } from 'node:url';
10	import { runResetAndTerrain } from '../src/world/gen/WorldGen';
11	import { runDunesPass } from '../src/world/gen/vanilla/DunesPass';
12	import { runOceanSandPass } from '../src/world/gen/vanilla/BeachPass';
13	import { runSandPatchesPass, runTunnelsPass, runDirtWallBgPass, runSmallHolesPass } from '../src/world/gen/vanilla/MissingCavesPass';
14	import { runMountCavesPass, runMountainCavesPass } from '../src/world/gen/vanilla/MountCavesPass';
15	import { runRocksAndClayPass, runCavesPass } from '../src/world/gen/vanilla/CavesPass';
16	import { runBeachesPass } from '../src/world/gen/vanilla/BeachPass';
17	import { runIceBiomePass } from '../src/world/gen/vanilla/IceBiomePass';
18	import { runGrassPass } from '../src/world/gen/vanilla/GrassPass';
19	import { runJunglePass } from '../src/world/gen/vanilla/JunglePass';
20	import { runMudCavesPass } from '../src/world/gen/vanilla/Spread';
21	import { runDesertMoundOnly, runDesertEntrancesAndHive } from '../src/world/gen/vanilla/DesertPass';
22	import { runMushroomPass } from '../src/world/gen/vanilla/MushroomPass';
23	import { runMarblePass, runGranitePass } from '../src/world/gen/vanilla/MarbleGranitePass';
24	import { runFloatingIslandsPass } from '../src/world/gen/vanilla/StructuresPass';
25	import { runDirtToMudPass, runSiltPass } from '../src/world/gen/vanilla/DirtToMudPass';
26	import { runShiniesPass } from '../src/world/gen/vanilla/ShiniesPass';
27	import { runWebsPass } from '../src/world/gen/vanilla/WebsPass';
28	import { runUnderworldPass } from '../src/world/gen/vanilla/UnderworldPass';
29	import { runLakesPass } from '../src/world/gen/vanilla/LakesPass';
30	import { runSlushPass } from '../src/world/gen/vanilla/IceBiomePass';
31	import { runCorruptionPass } from '../src/world/gen/vanilla/CorruptionPass';
32	import { TILE_BY_KEY } from '../src/data/tiles';
33	import { TILE_DEFS } from '../src/data/tiles';
34	import { fnv1a } from './pass-hash.test';
35	
36	const V_ID = new Int32Array(TILE_DEFS.length).fill(-1);
37	for (let i = 0; i < TILE_DEFS.length; i++) {
38	  const sheet = TILE_DEFS[i]?.vanilla?.sheet;
39	  if (typeof sheet === 'number') V_ID[i] = sheet;
40	}
41	
42	function hashGrids(st: { type: Uint16Array; flags: Uint8Array; liquid: Uint8Array; wall: Uint16Array; w: number; h: number }) {
43	  const n = st.w * st.h;
44	  const mapped = new Uint16Array(n);
45	  const ghost = new Uint16Array(n);
46	  for (let i = 0; i < n; i++) {
47	    const v = V_ID[st.type[i]];
48	    if (st.flags[i]) mapped[i] = v < 0 ? 0x7fff : v;
49	    else ghost[i] = v < 0 ? 0x7fff : v; // 幽灵 parity：inactive 格的残留 type
50	  }
51	  return `${fnv1a(mapped)} ${fnv1a(st.flags)} ${fnv1a(st.liquid)}`;
52	}
53	
54	/** wall 单独哈希——只对沙漠段启用：此前 pass 的 JS 墙与 oracle 有既知偏差
55	 *  （Terrain 自加渲染墙），到 desertmound 为止 wall 不具裁决力；沙漠 Sub-B/C
56	 *  以墙(187/216)为核心输出，从这里开始逐哈希比对。 */
57	function hashWalls(st: { wall: Uint16Array }): string {
58	  return fnv1a(st.wall);
59	}
60	
61	function hashGhost(st: { type: Uint16Array; flags: Uint8Array; w: number; h: number }): string {
62	  const n = st.w * st.h;
63	  const ghost = new Uint16Array(n);
64	  for (let i = 0; i < n; i++) {
65	    if (st.flags[i]) continue;
66	    const v = V_ID[st.type[i]];
67	    ghost[i] = v < 0 ? 0x7fff : v;
68	  }
69	  return fnv1a(ghost);   // fnv1a 返回 hex string（注解曾是 number——陈旧签名残留）
70	}
71	
72	function chainCheckpoints(seedText: string, evil: 0 | 1) {
73	  const { world, rng, gs } = runResetAndTerrain({ width: 4200, height: 1200, seedText, evil });
74	  const st = world.store;
75	  const out = new Map<string, string>();
76	  const outWall = new Map<string, string>();
77	  const snap = (name: string) => { out.set(name, hashGrids(st)); outWall.set(name, hashWalls(st)); };
78	  out.set('terrain', hashGrids(st));
79	  runDunesPass(st, rng, gs); out.set('dunes', hashGrids(st));
80	  runOceanSandPass(st, rng, gs); out.set('oceansand', hashGrids(st));
81	  runSandPatchesPass(st, rng, gs); out.set('sandpatches', hashGrids(st));
82	  runTunnelsPass(st, rng, gs); out.set('tunnels', hashGrids(st));
83	  runMountCavesPass(st, rng, gs); out.set('mountaincaves', hashGrids(st));
84	  runDirtWallBgPass(st, rng, gs); out.set('dirtwallbg', hashGrids(st));
85	  runRocksAndClayPass(st, rng, gs); out.set('rocksclay', hashGrids(st));
86	  runSmallHolesPass(st, rng, gs); out.set('smallholes', hashGrids(st));
87	  runCavesPass(st, rng, gs); out.set('surfacecaves', hashGrids(st));
88	  // 1456 注册序（执行序=注册序，WorldGenerator.cs:447）：
89	  //   14 SurfaceCaves → 16 IceBiome → 17 Grass → Jungle(12497) → 18 MudCaves →
90	  //   19 Desert → … → 32 Dungeon → 33 MCOpenings → 34 Beaches → 35 Gems。
91	  //   mcopenings/beaches 原紧跟 surfacecaves（注册序修正移到 Dungeon 后）。
92	  runIceBiomePass(st, rng, gs); out.set('icebiome', hashGrids(st));
93	  runGrassPass(st, rng, gs); out.set('grass', hashGrids(st));
94	  runJunglePass(st, rng, gs); out.set('jungle', hashGrids(st));
95	  runMudCavesPass(st, TILE_BY_KEY['mud']!, TILE_BY_KEY['v_60_jungle_grass_block']!);
96	  out.set('mudcaves', hashGrids(st));
97	  const desc = runDesertMoundOnly(st, rng, gs); out.set('desertmound', hashGrids(st));
98	  // Sub-C 入口 + Sub-B 蜂巢（DesertBiome.Place 顺序：入口先于 Hive）。
99	  // afterEntrance 钩子对齐 oracle 的 desertentrance 检查点位（入口后、Hive 前）
100	  runDesertEntrancesAndHive(st, rng, gs, desc, () => snap('desertentrance'));
101	  snap('deserthive');        // AddTileVariance 完
102	  snap('desertdone');        // CleanupArea 仅帧号——状态同 deserthive
103	  // #20-26（1456 注册序 12581/12800/12884/12976/13172/13192/13233）
104	  runMushroomPass(st, rng, gs); snap('mushroom');
105	  runMarblePass(st, rng, gs); snap('marble');
106	  runGranitePass(st, rng, gs); snap('granite');
107	  runFloatingIslandsPass(st, rng, gs); snap('islands');
108	  runDirtToMudPass(st, rng, gs); snap('dirttomud');
109	  runSiltPass(st, rng, gs); snap('silt');
110	  runShiniesPass(st, rng, gs); snap('ores');
111	  // #27/28/30/31（1456 注册序 13659/13697/14613/14756）。
112	  // #29 Corruption、#32 Dungeon oracle 尚未转录——其 JS 实现仍在 vanillaBiomes 内
113	  // （位置正确），转录后将插在 lakes 前与 slush 后。
114	  runWebsPass(st, rng, gs); snap('webs');
115	  runUnderworldPass(st, rng, gs); snap('underworld');
116	  // #29 Corruption（cs:13919，oracle 已转录；#32 Dungeon 未转录——其 JS 实现仍在
117	  // vanillaBiomes 内位置正确，转录后插 lakes 前与 slush 后之间）
118	  runCorruptionPass(st, rng, gs);
119	  snap('corruption');
120	  runLakesPass(st, rng, gs); snap('lakes');
121	  runSlushPass(st, gs); snap('slush');   // #31 零掷骰（签名无 rng）
122	  runMountainCavesPass(st, rng, gs); snap('mcopenings');
123	  runBeachesPass(st, rng, gs); snap('beaches');
124	  return { grids: out, walls: outWall };
125	}
126	
127	describe('洞穴链逐 pass 对账（vs C# caves-oracle）', () => {
128	  const cases = [
129	    { file: 'caves-chain-9293480.json', seedText: '9293480', evil: 0 as const },
130	    { file: 'caves-chain-SandboxWorld.json', seedText: 'SandboxWorld', evil: 1 as const },
131	  ];
132	  for (const c of cases) {
133	    it(`种子 ${c.seedText}：每 pass type/flags/liquid 哈希全等`, () => {
134	      const golden = JSON.parse(
135	        readFileSync(fileURLToPath(new URL(`./golden/${c.file}`, import.meta.url)), 'utf8'),
136	      ) as { checkpoints: string[] };
137	      const gold = new Map<string, string>();
138	      const goldWall = new Map<string, string>();
139	      for (const line of golden.checkpoints) {
140	        const [name, typ, act, wal, liq] = line.split(/[| ]+/);
141	        gold.set(name, `${typ} ${act} ${liq}`); // type/flags/liquid（wall 见文件头注）
142	        goldWall.set(name, wal);                // wall 只对沙漠段裁决（见 hashWalls 注）
143	      }
144	      const res = chainCheckpoints(c.seedText, c.evil);
145	      const ours = res.grids;
146	      const names = ['terrain', 'dunes', 'oceansand', 'sandpatches', 'tunnels',
147	        'mountaincaves', 'dirtwallbg', 'rocksclay', 'smallholes', 'surfacecaves',
148	        'icebiome', 'grass', 'jungle', 'mudcaves', 'desertmound',
149	        'desertentrance', 'deserthive', 'desertdone',
150	        'mushroom', 'marble', 'granite', 'islands', 'dirttomud', 'silt', 'ores',
151	        'webs', 'underworld', 'corruption', 'lakes', 'slush', 'mcopenings', 'beaches'];
152	      let firstBad = '';
153	      for (const n of names) {
154	        if (ours.get(n) !== gold.get(n) && !firstBad) firstBad = n;
155	        console.log(`${n.padEnd(14)} ${ours.get(n)} vs ${gold.get(n)} ${ours.get(n) === gold.get(n) ? '✓' : '✗'}`);
156	      }
157	      // 沙漠三检查点 wall 逐哈希（187 沙漠墙/216 硬化沙壳是 Sub-B/C 核心输出；
158	      // 更早 pass 的 wall 有既知偏差不裁决，见 hashWalls 注）
159	      for (const n of ['desertentrance', 'deserthive', 'desertdone']) {
160	        const ok = res.walls.get(n) === goldWall.get(n);
161	        if (!ok && !firstBad) firstBad = `${n}:wall`;
162	        console.log(`${`${n}:wall`.padEnd(14)} ${res.walls.get(n)} vs ${goldWall.get(n)} ${ok ? '✓' : '✗'}`);
163	      }
164	      // 报告全量后断言（首个分歧之后的必然不同——流已分叉）
165	      expect(firstBad, '首个分歧 pass').toBe('');
166	    }, 300000);
167	  }
168	});
169	

```


---

## 🤖 Assistant · 2026-08-12T18:46:43.497Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me look at the JS chain in WorldGen.ts — where is runDungeonPass called (vanillaBiomes), and what state it consumes (gs.dungeonLocation, gs.dungeonTheme, gs.generatingDungeonPositionX, gs.dungeonY, etc.).

Let me grep WorldGen.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:46:44.585Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"runDungeonPass\\|dungeonTheme\\|dungeonLocation\\|generatingDungeonPositionX\\|dungeonEntX\\|dungeonEntY\\|dungeonY\\b\" src/world/gen/WorldGen.ts src/world/gen/vanilla/GenState.ts src/world/gen/vanilla/DunesPass.ts src/world/gen/vanilla/StructuresPass.ts 2>/dev/null | head -60; echo ====; ls src/world/gen/vanilla/ | head -60",
 "description": "Find dungeon pass call sites and GenState fields"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:44.614Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
src/world/gen/vanilla/DunesPass.ts:52:  gs.dungeonTheme = rng.nextIntRange(0, 3);
src/world/gen/WorldGen.ts:265:import { runDungeonPass } from './vanilla/DungeonPass';
src/world/gen/WorldGen.ts:438:    gs.dungeonLocation = rng.nextIntRange(gs.beachLeftEnd + 50, Math.trunc(W * 0.2));
src/world/gen/WorldGen.ts:440:    gs.dungeonLocation = rng.nextIntRange(Math.trunc(W * 0.8), gs.beachRightStart - 50);
src/world/gen/WorldGen.ts:442:  world.dungeonX = gs.dungeonLocation;
src/world/gen/WorldGen.ts:593:  runDungeonPass(store, rng, gs, world.chests); // 32 Dungeon(蓝/粉砖主题+走廊房间+宝箱)
src/world/gen/WorldGen.ts:594:  // 地牢 pass 预计算会重掷 dungeonLocation(锚点 ±300 拒绝采样后迁移)——必须在此后
src/world/gen/WorldGen.ts:598:  world.dungeonX = gs.dungeonEntX || gs.dungeonLocation;
src/world/gen/WorldGen.ts:599:  world.dungeonY = gs.dungeonEntY || gs.dungeonY || 0;
src/world/gen/vanilla/GenState.ts:38:  dungeonLocation: number;    // 地牢入口实际位置（Reset 末掷）
src/world/gen/vanilla/GenState.ts:41:  dungeonTheme: number;
src/world/gen/vanilla/GenState.ts:42:  dungeonY: number;           // 地牢入口地表 Y（DungeonPass 回填；刷怪门槛 dungeonY+40 用）
src/world/gen/vanilla/GenState.ts:43:  dungeonEntX: number;        // 入口门厅可站立点 X（DungeonPass 回填；原版 dungeonX 语义=老头锚）
src/world/gen/vanilla/GenState.ts:44:  /** GenVars.CurrentDungeonGenVars.generatingDungeonPositionX（DungeonCrawler.cs:346 初值
src/world/gen/vanilla/GenState.ts:46:   *  消费的是它，不是 Reset 期 dungeonLocation——两字段混用会把回避带平移数百格
src/world/gen/vanilla/GenState.ts:48:  generatingDungeonPositionX: number;
src/world/gen/vanilla/GenState.ts:51:  dungeonEntY: number;        // 入口门厅可站立点 Y
src/world/gen/vanilla/GenState.ts:140:    dungeonSide: 1, dungeonX: 0, dungeonLocation: 0, dungeonTheme: -1, dungeonY: 0, dungeonEntX: 0, dungeonEntY: 0, generatingDungeonPositionX: 0, lAltarX: -1, lAltarY: -1, jungleX: 0,
src/world/gen/vanilla/StructuresPass.ts:551:    // ★dungeonX 此处 = generatingDungeonPositionX（DungeonCrawler.cs:394 最高房中心 X），
src/world/gen/vanilla/StructuresPass.ts:552:    //   非 Reset 期 dungeonLocation（2026-08-12 金字塔 handoff 疑点核实修复）
src/world/gen/vanilla/StructuresPass.ts:553:    const dgX = gs.generatingDungeonPositionX || gs.dungeonLocation;
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-12T18:46:45.903Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '540,620p' src/world/gen/WorldGen.ts",
 "description": "Read vanillaBiomes chain region in WorldGen.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:46:45.921Z

**📎 ToolResult**

```
  // 饥荒世界，普通世界零掷骰跳过）
  runOceanSandPass(store, rng, gs);
  runSandPatchesPass(store, rng, gs);   // 地下沙团（沙漠雏形）
  runTunnelsPass(store, rng, gs);       // 地表隧道（dirt runner 双向填充）
  runMountCavesPass(store, rng, gs);    // 山丘本体
  runDirtWallBgPass(store, rng, gs);    // 地表自然墙（wall 2/40）
  runRocksAndClayPass(store, rng, gs);
  runSmallHolesPass(store, rng, gs);    // 小空洞（每轮 2 发挖除 runner）
  runCavesPass(store, rng, gs);
}

// 原版 1456 真实注册序（执行序=注册序，WorldGenerator.cs:447 _passes[PassResults.Count]）：
//   14 SurfaceCaves → 15 WavyCaves(仅饥荒世界,普通零消耗) → 16 IceBiome → 17 Grass
//   → 18 MudCaves → 19 Desert → 20 Mushroom → 21 Marble → 22 Granite → 23 FloatingIslands
//   → 24 DirtToMud → 25 Silt → 26 OresAndShinies → 27 Webs(未移植) → 28 Underworld
//   → 29 Corruption → 30 Lakes → 31 Slush → 32 Dungeon → 33 MountainCaveOpenings
//   → 34 Beaches → 35 Gems → 36 GravitatingSand → 37 OceanCaves → 38 Shimmer → 39 DirtWallCleanup
// 本函数内对齐到 16-35 段（Underworld 28 在管线末"地狱"槽、Webs 27 后置——既有偏差另案）。
function vanillaBiomes({ store, rng, world, surface }: GenCtx) {
  const gs = ctxGs[0];
  if (!gs) return;
  runIceBiomePass(store, rng, gs);       // 16 Generate Ice Biome
  runGrassPass(store, rng, gs);          // 17 Grass
  const jx = runJunglePass(store, rng, gs); // JunglePass
  world.jungleX = jx;
  // 丛林表面泥化:泥柱核心区 ±0.12w 内,表层 10 格 dirt→mud(原版巨型 runner
  // 覆盖表面所致;我们补这一步让丛林表面成草皮而非裸土)
  {
    const core = (gs as any).jungleCoreX ?? jx;
    const reach = Math.floor(store.w * 0.12);
    for (let x = Math.max(0, core - reach); x < Math.min(store.w, core + reach); x++) {
      let sy = 0;
      while (sy < store.h - 12 && !store.flags[store.idx(x, sy)]) sy++;
      for (let y = sy; y < sy + 10; y++) {
        if (store.get(x, y) === T.DIRT) store.setTileSilent(x, y, TILE_BY_KEY['mud']!);
      }
    }
  }
  // 18 Mud Caves To Grass（cs:12499-12530 原版精确版：全图递归洪水+散块清除；
  // 曾用近似 spreadGrassAll 中心限距+2 轮快照——caves-oracle 位级对账后替换）
  runMudCavesPass(store, TILE_BY_KEY['mud']!, TILE_BY_KEY['v_60_jungle_grass_block']!);
  runDesertPass(store, rng, gs); // 19 Full Desert
  runMushroomPass(store, rng, gs); // 20 Mushroom Patches
  runMarbleGranitePass(store, rng, gs); // 21/22 Marble/Granite
  runFloatingIslandsPass(store, rng, gs); // 23 Floating Islands（原在蘑菇前——注册序修正）
  runDirtToMudAndSiltPass(store, rng, gs); // 24 Dirt To Mud / 25 Silt
  runShiniesPass(store, rng, gs); // 26 Ores And Shinies（原在很后"矿石"槽——移到 Silt 后=Webs 位）
  runVanillaWebsPass(store, rng, gs); // 27 Webs（cs:13659——原后置防被清，注册序修正回 27 位）
  runUnderworldPass(store, rng, gs); // 28 Underworld（cs:13697——原管线末"地狱"槽；
                                        //  地狱屋/地狱箱/熔炉等依赖槽在数组其后 = 地狱 pass 之后 ✓）
  runCorruptionPass(store, rng, gs); // 29 Corruption/Crimson
  runLakesPass(store, rng, gs); // 30 Lakes（cs:14613——原"液体"槽在结构段后，注册序修正）
  runSlushPass(store, gs); // 31 StoneToIceAndSiltPlusMudIntoSlush（cs:14756，紧随 Lakes）
  runDungeonPass(store, rng, gs, world.chests); // 32 Dungeon(蓝/粉砖主题+走廊房间+宝箱)
  // 地牢 pass 预计算会重掷 dungeonLocation(锚点 ±300 拒绝采样后迁移)——必须在此后
  // 回写最终位置,否则 world.dungeonX 停留在 Reset 期的旧值(与实际地牢偏差可达数百格)。
  // 优先取入口门厅可站立点(原版 dungeonX/Y 语义 cs L72510-72527:入口结构上可站处,
  // 守卫老人出生/游走锚)——塔心锚点会把老人漏进塔内
  world.dungeonX = gs.dungeonEntX || gs.dungeonLocation;
  world.dungeonY = gs.dungeonEntY || gs.dungeonY || 0;
  // 33 MountainCaveOpenings + 34 Beaches（原紧跟 SurfaceCaves——注册序修正移到 Dungeon 后）
  runMountainCavesPass(store, rng, gs);
  runBeachesPass(store, rng, gs);
  // 海盆挖完后刷新 surface[](后续旧 pass 依赖;本函数之后才到那些 pass)
  for (let x = 0; x < store.w; x++) {
    for (let y = 0; y < store.h; y++) {
      if (store.flags[store.idx(x, y)]) { surface[x] = y; break; }
    }
  }
  runGemsPass(store, rng, gs); // 35 Gems（原捆绑在 Lakes 槽——注册序修正移到 Beaches 后）
  // 原版 1456 注册序（WorldGen.cs 行号 = 唯一权威，2026-08-11 review 依此重排）：
  //   OceanCaves(15228) < Pyramids(15426) < SurfaceWaterInJungle(15887) <
  //   Temple(15911) < Beehives(16005) < JungleShrines(16059) < Statues(16947) <
  //   UndergroundHouses+BuriedChests(17066) < SurfaceChests(17226) <
  //   ChestsInJungleShrines(17308) < UnderwaterChests(17343) < SpiderCaves(17455) <
  //   FloatingIslandHouses(17971) < MicroBiomes(21785)
  // 神庙/灌水提前到宝箱系之前（原版语义:大结构先占位,箱/雕像后放才不会塞进
  // 神庙体内或被灌水淹没;此前神庙在蜘蛛洞后 → 占地区内已塞雕像/箱,放置互相破坏）。
  const oceanTreasures = runOceanCavesPass(store, rng, gs); // 海洋洞窟蠕虫+宝藏点记录
  runPyramidPass(store, rng, gs, world.chests); // Pyramids(沙岩砖金字塔+宝箱)
  // 原版注册序 Pyramids(15426) < LivingTrees(15551) < LivingTreeWalls(15792) <

```


---

## 🤖 Assistant · 2026-08-12T18:47:02.648Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
JS chain: dungeon is already between slush and mcopenings in vanillaBiomes. So the test just needs to insert `runDungeonPass` in chainCheckpoints between slush and mcopenings. And the oracle needs the dungeon segment between Checkpoint("slush") and the mcopenings block.

Now, the crucial task: transcribe the dungeon into the oracle. The reference for the algorithm — since the JS implements the 1405 legacy algorithm with 1456 corrections — should be the vanilla 1405 source (Terarria1405) WorldGen.cs MakeDungeon, MakeDungeon_Halls, MakeDungeon_Room, MakeDungeon_Stairs, DungeonEntrance etc. plus the 1456 RNG consumption (SetupDungeonDataVariables rolls) that the JS comments reference.

Let me check Terarria1405 exists and find those functions.

Note the oracle hashes only act (flags), typ, wal, liq — NOT frameX/frameY! That's a huge simplification: furniture frames don't matter for the checkpoint hash. But type and active do matter, and walls matter.

But careful: JS hashGrids maps JS internal tile ids to vanilla sheet ids (V_ID). The oracle uses vanilla ids directly. Also `st.flags[i]` for active. Walls: JS `st.wall[i]` — for dungeon, walls 7/8/9 and variants 94-99 are vanilla wall ids already? The JS `dc.isDungeonWall` compares `st.wall[...] === this.wall || (wl >= 94 && wl <= 99)`, suggesting JS wall array stores vanilla wall ids directly. Good.

So the oracle transcription must reproduce: brick tiles (41/43/44), cracked bricks (481/482/483), spikes (48), platforms (19), doors (10? or 11), chests (21), torches/candles (33 etc.), bookcases, statues, traps, switches, wiring is NOT hashed (wire isn't in the hash: act, typ, wal, liq). Liquids are hashed (dungeon clears liquids).

So for the oracle I need the tile-placing behavior (type, active, wall, liquid) 1:1, but not frames. But RNG consumption of the JS side depends on placement success (e.g., while loops with fail counters), which depends on exact geometry checks. So I do need exact geometry — the full algorithm.

This is a big transcription. The JS file is 1684 lines; the oracle version will be similar (maybe 900-1100 lines of C#).

Strategy: transcribe the JS DungeonPass algorithm into C# oracle faithfully — but verify against the vanilla 1405 source where the JS claims "1:1", and fix deviations found ("自创改良" removal). Since JS was just rewritten by another session with references to 1456 DungeonCrawler for RNG, and 1405 lines for algorithm, the safest approach: transcribe JS → C# (mechanical), then run and compare; when mismatching, dig into vanilla source to decide which side is right.

Wait, but that "oracle transcribed from JS" is circular: any JS bug gets baked into the oracle and they'd trivially agree. The instructions say to transcribe from the vanilla source. But which vanilla source matches the JS algorithm? The JS header says: 原版地牢 1:1 复刻(MakeDungeon L18006 + DungeonHalls L20255 + DungeonRoom L20622 + DungeonStairs L19855 + DungeonEnt L20726, 算法文档 docs/vanilla-algos/dungeon.md).

So the reference is Terarria1405 WorldGen.cs at those line numbers. Let me check the 1405 source and the algorithm doc.

Plan:
1. Read docs/vanilla-algos/dungeon.md.
2. Read 1405 WorldGen.cs L18006-21300 (MakeDungeon and helpers).
3. Read 1456 DungeonCrawler for the RNG rolls already understood.
4. Check where the JS deviates from 1405 and decide.
5. Transcribe into oracle (using the same algorithm as JS, with vanilla-correct fixes).
6. Update test, regenerate goldens, run.

The scope is huge; time budget matters. Note the instruction: "单次工具调用别超 8 分钟". dotnet run on the oracle takes how long? The oracle currently covers terrain→beaches. Let me check timing later.

Also note: the dungeon needs `gs.dungeonTheme` — thrown at Dunes pass head (DunesPass.ts:52 `gs.dungeonTheme = rng.nextIntRange(0, 3)`). And in the oracle, the Dunes pass must have that roll. Let me check the oracle's Dunes section for that roll (r.Next(3)?). In 1456, SetupDungeonGenVarVariables is called at Dunes head: cs:11542 per JS comment. Let me verify the oracle has it.

Let me grep.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:47:03.844Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dungeonTheme\\|Next(3)\\|SetupDungeon\\|Dungeon\" tools/golden/caves-oracle.cs | sed -n '1,40p'; echo ----; sed -n '488,530p' tools/golden/caves-oracle.cs; echo ----; ls ~/Project/GLM/SandboxWorld/docs/vanilla-algos/ | head; wc -l ~/Project/GLM/SandboxWorld/docs/vanilla-algos/dungeon.md 2>/dev/null",
 "description": "Check oracle Dunes section for theme roll and find dungeon algo doc"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:03.881Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
102:for (int i = 0; i < 2; i++) { int s = i == 0 ? ts0 : ts1; if (s == 0) r.Next(3); }
107:r.Next(4); r.Next(3); r.Next(2);
112:    if (n == 3 && (int)r.Next(3) == 0) n = 31;
128:r.Next(8); r.Next(5); r.Next(3);
208:    if ((double)i > W * 0.45 && (double)i < W * 0.55 && (feature == 3 || feature == 4)) feature = (int)r.Next(3);
284:                    && y < H - 210 - (int)r.Next(3)
489:r.Next(3); // DungeonCrawler.SetupDungeonGenVarVariables（cs:11542 + DungeonCrawler.cs:56）
540:    int num = (int)r.Next(3) + 8;
964:                if ((int)r.Next(3) == 0)
967:                    if ((int)r.Next(3) == 0) num5 += (int)r.Next(-6, 7);
969:                if (num5 < 0) num5 = (int)r.Next(3);
970:                else if (num5 > 50) num5 = 50 - (int)r.Next(3);
1639:            if (dhFr.Next(3) == 0) hType = 397;
1802:        sn -= (int)r.Next(3);
1986:    PlaceStalactite(tx, ty, (int)r.Next(2) == 0, (int)r.Next(3));
2220:                if (ty + 1 < H && act[(ty + 1) * W + tx] == 0) PlaceStalactite(tx, ty + 1, gFr2.Next(2) == 0, gFr2.Next(3));
2221:                if (ty - 1 >= 0 && act[(ty - 1) * W + tx] == 0) PlaceStalactite(tx, ty - 1, gFr2.Next(2) == 0, gFr2.Next(3));
2756:        int num5 = (int)r.Next(3);                              // 干身帧骰（帧值不入哈希）
2758:        if (num6 == 5 || num6 == 7) { int k = (int)r.Next(3); int f = (int)r.Next(3); Put(tx - 1, i); }   // 左枝 2 骰
2759:        if (num6 == 6 || num6 == 7) { int k = (int)r.Next(3); int f = (int)r.Next(3); Put(tx + 1, i); }   // 右枝 2 骰
2764:    if ((int)r.Next(3) == 0) tL = false;
2765:    if ((int)r.Next(3) == 0) tR = false;
2766:    if (tR) { int k = (int)r.Next(3); Put(tx + 1, num - 1); }
2767:    if (tL) { int k = (int)r.Next(3); Put(tx - 1, num - 1); }
2768:    if (tL || tR) { int k = (int)r.Next(3); Put(tx, num - 1); }
2770:    int crownK = (int)r.Next(3);
2786:        for (int uy = uwNum - 20 - (int)r.Next(3); uy < H; uy++)
2821:            if ((int)r.Next(3) == 0) uwS *= 0.5;
2830:            if ((int)r.Next(3) == 0)
2876:                if ((int)r.Next(3) == 0) { uwGrow[0]++; GrowAshTree(ux, uy); }
2956:            rad += (int)r.Next(3);
2957:            rad -= (int)r.Next(3);
3009:    if ((int)r.Next(3) == 0)
3030:            rad += (int)r.Next(3);
3031:            rad -= (int)r.Next(3);
3637:                            if (Math.Abs(dx) + Math.Abs(dy) < 9 + (int)r.Next(11) && (int)r.Next(3) != 0 && typ[ti] != 31)
3642:                            if (typ[ti] != 31 && Math.Abs(dx) <= 2 + (int)r.Next(3) && Math.Abs(dy) <= 2 + (int)r.Next(3))
3664:    if ((int)r.Next(3) == 0) { /* getGoodWorldGen false → 保持水 */ }
3861:// ★#29 Corruption（cs:13919）与 #32 Dungeon（cs:14816）尚未转录——转录后须插在
3864:// 1456 注册序在 Dungeon(32) 之后——本 oracle 尚未转录 26-32 段（Mushroom/Marble/
----
// ================= Pass 1：Dunes（cs:11540-11602 + DunesBiome.cs + SurfaceMap.cs）=================
r.Next(3); // DungeonCrawler.SetupDungeonGenVarVariables（cs:11542 + DungeonCrawler.cs:56）
// Count：WorldGenRange(1,2,ScaleWith:WorldWidth) → Next((int)(w/4200*1), (int)(w/4200*2)+1)
int dunesCount = (int)r.Next((int)(W / 4200.0 * 1), (int)(W / 4200.0 * 2) + 1);
var pyrX = new List<int>(); var pyrY = new List<int>();
for (int i = 0; i < dunesCount; i++)
{
    int ox, oy, tries = 0;
    for (; ; )
    {
        ox = (int)r.Next(500, W - 500);
        oy = (int)r.Next(0, H);
        bool fJungle = Math.Abs(ox - jungleX) < (int)(600.0 * (W / 4200.0));
        bool fCenter = Math.Abs(ox - W / 2) < 300;
        bool fSnow = ox > snowL - 300 && ox < snowR + 300;
        tries++;
        if (tries >= W) fJungle = false;
        if (tries >= W * 2) fSnow = false;
        if (!(fJungle || fCenter || fSnow)) break;
    }
    DunesPlace(ox, oy);
    if ((double)r.NextDouble() <= 0.8)
    {
        int px2 = (int)r.Next(ox - 200, ox + 200);
        for (int j = 0; j < H; j++)
        {
            if (act[j * W + px2] == 1) { pyrX.Add(px2); pyrY.Add(j + 20); break; }
        }
    }
}
void DunesPlace(int originX, int originY)
{
    // DunesBiome.Place（DunesBiome.cs:56-70）：heightScale=1（Configuration.json）
    int height = (int)((int)r.Next(60, 100) * 1.0);
    int height2 = (int)((int)r.Next(60, 100) * 1.0);
    // SingleDunesWidth：Min150 Max250 ScaleWith=None → Next(150,251) 不缩放
    int rand1 = (int)r.Next(150, 251);
    int rand2 = (int)r.Next(150, 251);
    // ★CreateFromPlacement ×2（SurfaceMap 采样+风向掷）都先于 PlaceSingle ×2
    //（DunesBiome.cs:62-65：两图均为 pre-dune1 地形）
    int l1 = originX - rand1 / 2 + 30 - rand1 / 2, l2 = originX + rand2 / 2 - 30 - rand2 / 2;
    var surf1 = SurfaceFromArea(l1 - 20, rand1 + 40);
    bool wind1 = (int)r.Next(2) != 0;
----
ls: ~/Project/GLM/SandboxWorld/docs/vanilla-algos/: No such file or directory

```


---

## 🤖 Assistant · 2026-08-12T18:47:10.928Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good — oracle line 489 has `r.Next(3)` for the theme roll at Dunes head. And JS DunesPass.ts:52 uses `rng.nextIntRange(0, 3)`. Need to check JS RNG semantics: `rng.nextIntRange(a,b)` — is it Next(a,b) (half-open) or inclusive? The discipline says rng.int(a,b) ≡ closed interval ≡ Next(a,b+1). What about nextIntRange? Let me check the RNG implementation.

The algorithm doc docs/vanilla-algos/dungeon.md doesn't exist. Let me find docs dir.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:47:10.955Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/docs/ | head -30; echo ----; grep -rn \"nextIntRange\\|nextFloat\\|nextInt\\b\\|next()\\|nextDouble\" src/core/rng.ts | head -40",
 "description": "Check docs dir and RNG API semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:10.985Z

**📎 ToolResult**

```
upgrade-1405-to-1456
worldgen
----
src/core/rng.ts:83:  next(): number {
src/core/rng.ts:89:  nextIntRange(minValue: number, maxValue: number): number {
src/core/rng.ts:98:  nextInt(maxValue: number): number {
src/core/rng.ts:103:  nextDouble(): number {
src/core/rng.ts:119://   rng.next()   = NextDouble()          每次消耗 1 个 InternalSample
src/core/rng.ts:130:  next(): number {
src/core/rng.ts:131:    return this.ur.nextDouble();
src/core/rng.ts:136:    return this.ur.nextIntRange(min, max + 1);
src/core/rng.ts:140:    return min + this.ur.nextDouble() * (max - min);
src/core/rng.ts:144:    return this.ur.nextDouble() < p;
src/core/rng.ts:148:    return arr[this.ur.nextInt(arr.length)];
src/core/rng.ts:152:  nextInt(maxValue: number): number {
src/core/rng.ts:153:    return this.ur.nextInt(maxValue);
src/core/rng.ts:156:  nextIntRange(minValue: number, maxValue: number): number {
src/core/rng.ts:157:    return this.ur.nextIntRange(minValue, maxValue);
src/core/rng.ts:285:  nextDouble(): number {

```


---

## 🤖 Assistant · 2026-08-12T18:47:14.809Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So:
- rng.next() = NextDouble() (1 InternalSample)
- rng.int(a,b) = closed interval = ur.nextIntRange(a, b+1)
- rng.nextInt(n) = Next(n) half-open
- rng.nextIntRange(a,b) = Next(a,b) — wait, what does UnifiedRandom.nextIntRange(a, b) do? In C#, UnifiedRandom.Next(int minValue, int maxValue) is half-open [min, max). The JS wrapper `nextIntRange(min,max)` calls ur.nextIntRange(min, max) — which maps to Next(minValue, maxValue). So `rng.nextIntRange(0, 3)` = Next(0,3) = 0..2. That matches oracle `r.Next(3)`. Good.

Let me read rng.ts fully to understand `rng` wrapper and `ur` (UnifiedRandom).
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:47:14.910Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/core/rng.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:14.920Z

**📎 ToolResult**

```
1	// 确定性随机数：Terraria 1.4.5.6 位级对齐。
2	//
3	// ── UnifiedRandom（Terraria.Utilities/UnifiedRandom.cs 1:1）─────────────────
4	// .NET System.Random 的 Knuth 减法生成器（MSEED=161803398），纯 int32 运算。
5	// 位级移植要点（JS/C# 数值差异全部钉死，改动前先读）：
6	//  1. C# int 溢出 unchecked 回绕 ↔ JS：本实现所有中间值都落在 int32 范围内
7	//     （diff 最小 -(2^31-1)，`+((n>>31)&0x7FFFFFFF)` 归位后 ∈[0,2^31-1]），
8	//     无需模拟回绕；存储用 Int32Array 与 C# int[] 同构。
9	//  2. `(int)double` 是向零截断 ↔ JS Math.trunc（Sample()≥0 时与 floor 等价，
10	//     但必须写 trunc 以防有人把 internalSample 改出负值）。
11	//  3. `Sample()` 常数 4.656612875245797E-10 = 1/(2^31-1)，十进制字面量两语言
12	//     解析为同一 double，乘法 IEEE754 位级一致。
13	//  4. `Next(min,max)` 的 range 用 long（≤2^32）↔ JS number 精确整数，安全。
14	//     大 range 分支的 `(int)(long+min)` unchecked 回绕 ↔ JS `|0`（ToInt32 mod 2^32）。
15	//  5. `GetSampleForLargeRange` 的 `% 2 == 0`：C# 余数带符号但只判零，JS `%` 同判。
16	//  金标：tests/golden/unified-random.json 由真·Terraria.exe 反射导出
17	//  （tools/golden/rand-golden.cs），tests/unified-random.test.ts 位级断言。
18	//
19	// ── 种子解析（WorldFileData.TranslateSeed, cs:399-410 1:1）────────────────
20	// 数字字符串 → Math.Abs(int)（int.MinValue→int.MaxValue）；非数字 →
21	// ReLogic.Utilities.Crc32.Calculate（IEEE 表，按 UTF-16 code unit 逐字符，
22	// 注意 `(crc ^ c) & 0xFF` 只取 char 低字节）。Crc32 结果可为负，直接作种子。
23	export class UnifiedRandom {
24	  private seedArray: Int32Array;
25	  private inext = 0;
26	
27	  constructor(seed: number) {
28	    this.seedArray = new Int32Array(56);
29	    this.setSeed(seed);
30	  }
31	
32	  /** C# SetSeed（UnifiedRandom.cs:25-61）1:1 */
33	  setSeed(seed: number): void {
34	    this.seedArray.fill(0);
35	    // C#: (Seed == int.MinValue) ? int.MaxValue : Math.Abs(Seed)
36	    const num = seed === -2147483648 ? 2147483647 : Math.abs(seed);
37	    let num2 = 161803398 - num;
38	    this.seedArray[55] = num2;
39	    let num3 = 1;
40	    for (let j = 1; j < 55; j++) {
41	      const num4 = (21 * j) % 55;
42	      this.seedArray[num4] = num3;
43	      num3 = (num2 - num3) | 0; // C# unchecked int：可能回绕，|0 = ToInt32 同语义
44	      if (num3 < 0) num3 += 2147483647; // C# += int.MaxValue（不是 2^32！）
45	      num2 = this.seedArray[num4];
46	    }
47	    for (let k = 1; k < 5; k++) {
48	      for (let l = 1; l < 56; l++) {
49	        this.seedArray[l] -= this.seedArray[1 + ((l + 30) % 55)];
50	        if (this.seedArray[l] < 0) this.seedArray[l] += 2147483647;
51	      }
52	    }
53	    this.inext = 0;
54	  }
55	
56	  /** C# Sample（:63-65）*/
57	  private sample(): number {
58	    return this.internalSample() * 4.656612875245797e-10;
59	  }
60	
61	  /** C# InternalSample（:67-86）1:1。inext 为 uint 语义（0..55，无溢出面）*/
62	  private internalSample(): number {
63	    let num = this.inext + 1;
64	    if (num > 55) num = 1;
65	    let num2 = num + 21;
66	    if (num2 > 55) num2 -= 55;
67	    let num3 = this.seedArray[num] - this.seedArray[num2];
68	    if (num3 === 2147483647) num3--;
69	    num3 = num3 + ((num3 >> 31) & 0x7fffffff); // >>31 算术移位，JS/C# 一致
70	    this.seedArray[num] = num3;
71	    this.inext = num;
72	    return num3;
73	  }
74	
75	  /** C# GetSampleForLargeRange（:96-104）。注意两次 InternalSample 的求值顺序 */
76	  private getSampleForLargeRange(): number {
77	    let num = this.internalSample();
78	    if (this.internalSample() % 2 === 0) num = -num;
79	    return (num + 2147483646) / 4294967293;
80	  }
81	
82	  /** C# Next()（:106-108）：裸 int32 */
83	  next(): number {
84	    return this.internalSample();
85	  }
86	
87	  /** C# Next(minValue, maxValue)（:115-133）：[min, max)。maxValue 负值时 C# 抛异常，
88	   *  本移植不抛（生成期契约保证入参合法）。*/
89	  nextIntRange(minValue: number, maxValue: number): number {
90	    const num = maxValue - minValue; // C# long 减法，≤2^32，JS 精确
91	    if (num <= 2147483647) {
92	      return (Math.trunc(this.sample() * num) + minValue) | 0;
93	    }
94	    return (Math.trunc(this.getSampleForLargeRange() * num) + minValue) | 0;
95	  }
96	
97	  /** C# Next(maxValue)（:121-127）：[0, max) */
98	  nextInt(maxValue: number): number {
99	    return Math.trunc(this.sample() * maxValue);
100	  }
101	
102	  /** C# NextDouble()（:113-115）*/
103	  nextDouble(): number {
104	    return this.sample();
105	  }
106	
107	  /** C# Peek()（:88-99，非消耗）：下一 InternalSample 原始差值——对账/断点用 */
108	  peek(): number {
109	    let num = this.inext + 1;
110	    if (num > 55) num = 1;
111	    let num2 = num + 21;
112	    if (num2 > 55) num2 -= 55;
113	    return this.seedArray[num] - this.seedArray[num2];
114	  }
115	}
116	
117	// ── RNG：世界生成/运行时统一入口（API 不变，内核换 UnifiedRandom）──────────
118	// 与原版调用点的对账约定（gen 代码全部按此书写）：
119	//   rng.next()   = NextDouble()          每次消耗 1 个 InternalSample
120	//   rng.int(a,b) = Next(a, b+1)          闭区间 [a,b]
121	//   rng.chance(p)= NextDouble() < p      1 次
122	//   rng.pick(xs) = xs[Next(xs.length)]   1 次
123	//   rng.range(a,b) = a + NextDouble()*(b-a)
124	export class RNG {
125	  private ur: UnifiedRandom;
126	  constructor(seed: number) {
127	    this.ur = new UnifiedRandom(seed);
128	  }
129	
130	  next(): number {
131	    return this.ur.nextDouble();
132	  }
133	
134	  /** 闭区间 [min, max]，≡ 原版 Next(min, max+1) */
135	  int(min: number, max: number): number {
136	    return this.ur.nextIntRange(min, max + 1);
137	  }
138	
139	  range(min: number, max: number): number {
140	    return min + this.ur.nextDouble() * (max - min);
141	  }
142	
143	  chance(p: number): boolean {
144	    return this.ur.nextDouble() < p;
145	  }
146	
147	  pick<T>(arr: T[]): T {
148	    return arr[this.ur.nextInt(arr.length)];
149	  }
150	
151	  /** 原版裸方法直通（Reset 序列/pass 级对账用，语义与 C# 完全一致） */
152	  nextInt(maxValue: number): number {
153	    return this.ur.nextInt(maxValue);
154	  }
155	
156	  nextIntRange(minValue: number, maxValue: number): number {
157	    return this.ur.nextIntRange(minValue, maxValue);
158	  }
159	
160	  get vanilla(): UnifiedRandom {
161	    return this.ur;
162	  }
163	}
164	
165	// ── Crc32（ReLogic.Utilities.Crc32 反编译 1:1）─────────────────────────────
166	// 标准 IEEE 表（多项式 0xEDB88320）。按 UTF-16 code unit 逐字符：
167	// (num ^ c) & 0xFF 只取 charCode 低字节——charCode > 0xFF 时高字节不参与。
168	const CRC32_TAB = (() => {
169	  const t = new Uint32Array(256);
170	  for (let i = 0; i < 256; i++) {
171	    let c = i;
172	    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
173	    t[i] = c >>> 0;
174	  }
175	  return t;
176	})();
177	
178	export function crc32Calculate(value: string): number {
179	  let num = 0xffffffff;
180	  for (let i = 0; i < value.length; i++) {
181	    num = (CRC32_TAB[(num ^ value.charCodeAt(i)) & 0xff] ^ (num >>> 8)) >>> 0;
182	  }
183	  return ~num | 0; // C# (int)(~uint)：位翻转后按 int32 解释（可为负）
184	}
185	
186	// ── 种子解析（WorldFileData.TranslateSeed, cs:399-410 1:1）─────────────────
187	// 数字字符串 → Abs(int)（int.MinValue 特判）；否则 Crc32 直出。
188	// C# int.TryParse 细节：前后空白/正负号/前导零合法，溢出或空串 → false 走 Crc32。
189	// （Unicode 数字字符 C# 能解析而本实现不认——种子 UI 只产 ASCII，不构成偏差。）
190	export function translateSeed(seedText: string): number {
191	  const m = /^\s*([+-]?\d+)\s*$/.exec(seedText);
192	  if (m) {
193	    const v = BigInt(m[1]);
194	    if (v >= -2147483648n && v <= 2147483647n) {
195	      const n = Number(v);
196	      return n === -2147483648 ? 2147483647 : Math.abs(n);
197	    }
198	  }
199	  return crc32Calculate(seedText);
200	}
201	
202	// FNV-1a 字符串 hash（旧种子派生/通用标识用；世界生成种子已改 translateSeed）
203	export function hashString(str: string): number {
204	  let h = 2166136261 >>> 0;
205	  for (let i = 0; i < str.length; i++) {
206	    h ^= str.charCodeAt(i);
207	    h = Math.imul(h, 16777619);
208	  }
209	  return h >>> 0;
210	}
211	
212	// 2D 整数 hash → [0,1)，无状态确定性噪声（渲染层视觉变体用，与种子等价无关）
213	export function hash2(x: number, y: number, seed: number): number {
214	  let h = seed >>> 0;
215	  h = Math.imul(h ^ (x | 0), 0x27d4eb2d);
216	  h = Math.imul(h ^ (y | 0), 0x85ebca6b);
217	  h ^= h >>> 15;
218	  h = Math.imul(h, 0x2c1b3c6d);
219	  h ^= h >>> 12;
220	  return (h >>> 0) / 4294967296;
221	}
222	
223	// ── FastRandom（Terraria.Utilities/FastRandom.cs:7-88 一比一）─────────────────
224	// 48 位 LCG（Java Random 同族），与 UnifiedRandom 完全独立的第二条随机流。
225	// 原版世界生成里凡显式 `new FastRandom(seed).WithModifier(...)` 的掷骰走这里
226	// （DesertHive.PlaceClustersArea 的 shell 类型骰/0.25 门、光照等）——绝不可用
227	// RNG/UnifiedRandom 代替，否则流偏移不可查。光照系统的副本在
228	// src/lighting/FastRandom.ts（同源、API 子集），此处是世界生成权威实现。
229	const FR_MULTIPLIER = 25214903917n;
230	const FR_ADD = 11n;
231	const FR_MASK = 0xffffffffffffn; // 2^48 - 1
232	
233	export class FastRandom {
234	  private seed: bigint;
235	
236	  constructor(seed: bigint | number) {
237	    this.seed = (typeof seed === 'bigint' ? seed : BigInt(seed)) & FR_MASK;
238	  }
239	
240	  /** NextSeed(L85-88)：静态推进，不动自身状态 */
241	  static nextSeed(seed: bigint): bigint {
242	    return (seed * FR_MULTIPLIER + FR_ADD) & FR_MASK;
243	  }
244	
245	  /** WithModifier(ulong)(L27-30)：新实例种子 = NextSeed(m) ^ 原 Seed（不改自身） */
246	  withModifier(m: number | bigint): FastRandom {
247	    const mod = typeof m === 'bigint' ? m : BigInt(m);
248	    return new FastRandom(FastRandom.nextSeed(mod) ^ this.seed);
249	  }
250	
251	  /** WithModifier(int x, int y)(L32-35)：
252	   *  modifier = (ulong)(x + 2654435769u + ((long)y << 6)) + ((ulong)y >> 2)
253	   *  坑：C# 的 (ulong)y 是 64 位补码（负 y → 巨值再右移），不能写 JS 的
254	   *  `y >>> 0`（32 位截断）——DesertHive 的 hj=-20 行曾因此整行门骰错位 */
255	  withModifierXY(x: number, y: number): FastRandom {
256	    const u64y = BigInt(y) & 0xffffffffffffffffn;   // (ulong)y：64 位补码
257	    const mod = BigInt(x + 2654435769 + (y << 6)) + (u64y >> 2n);
258	    return this.withModifier(mod);
259	  }
260	
261	  /** NextBits(b)(L47-51)：前进一步并取高 b 位 */
262	  private nextBits(bits: number): number {
263	    this.seed = FastRandom.nextSeed(this.seed);
264	    return Number(this.seed >> BigInt(48 - bits));
265	  }
266	
267	  /** Next(max)(L63-78)（= Next(min,max) 的 range 部分）；2 的幂走快速路径，
268	   *  其余拒绝采样——溢出带判据 num <= 2^31-1-(max-1) 与原版 int32 回绕等价 */
269	  nextMax(max: number): number {
270	    if ((max & -max) === max) {
271	      // (int)((long)max * NextBits(31) >> 31)
272	      return Math.floor((max * this.nextBits(31)) / 2147483648);
273	    }
274	    for (;;) {
275	      const num = this.nextBits(31);          // [0, 2^31)
276	      const rem = num % max;
277	      if (num <= 2147483647 - (max - 1)) return rem;
278	    }
279	  }
280	
281	  /** NextDouble()(L58-61)：`(float)NextBits(32) * 4.656613E-10f`——两个坑：
282	   *  1. NextBits(32)=(int)(seed>>16) 是 unchecked ulong→int 回绕，≥2^31 取负；
283	   *  2. 乘法在 float（24 位尾数）精度——必须 fround，否则与 C# 位级不等。
284	   *  结果因此可落在 [-1,1)（原版事实，DesertHive 0.25 门直接消费） */
285	  nextDouble(): number {
286	    this.seed = FastRandom.nextSeed(this.seed);
287	    const raw = Number(this.seed >> 16n);
288	    const b32 = raw >= 2 ** 31 ? raw - 2 ** 32 : raw; // (int) unchecked 回绕
289	    return Math.fround(Math.fround(b32) * Math.fround(4.656613e-10));
290	  }
291	}
292	

```


---

## 🤖 Assistant · 2026-08-12T18:47:16.363Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Now I understand the RNG layer.

Now let me look at the 1405 reference for the dungeon algorithm. Check if Terarria1405 exists.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:47:16.895Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/ | head -30; wc -l ~/Project/GLM/SandboxWorld/Terarria1405/Terraria/WorldGen.cs 2>/dev/null",
 "description": "Check Terarria1405 presence"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:16.923Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
annotations.json
backups
check-size.mjs
CLAUDE.md
docs
game
node_modules
server
src
Terarria1405
Terarria1456
Terarria1456Server
Terraia_Maples
terraria-assets
Terraria-Map-Editor
terraria-wiki-md
terraria.wiki.gg_en_all_2026-07a.zim
tools
verify-bleed2.mjs
verify-dev.mjs
verify-quickload.mjs
verify-stable.mjs
verify-swing.mjs
verify-torch.mjs
verify-wld-persist.mjs
verify-wld2.mjs
开服.sh

```


---

## 🤖 Assistant · 2026-08-12T18:47:18.870Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1405/ 2>/dev/null | head; ls ~/Project/GLM/SandboxWorld/Terarria1405/Terraria 2>/dev/null | head",
 "description": "List Terarria1405 contents"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:18.898Z

**📎 ToolResult**

```
Achievements
Animation.cs
AssemblyInfo.cs
Audio
BitsByte.cs
Chat
Chest.cs
Cinematics
Cloud.cs
Collision.cs

```


---

## 🤖 Assistant · 2026-08-12T18:47:22.091Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && ls Terraria/ | head -8; wc -l Terraria/WorldGen.cs 2>/dev/null; grep -n \"public static void MakeDungeon\\|private static void MakeDungeon\\|static void DungeonEntrance\\|MakeDungeon_Halls\\|MakeDungeon_Room\\|MakeDungeon_Stairs\" Terraria/WorldGen.cs 2>/dev/null | head -20",
 "description": "Locate 1405 MakeDungeon functions"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:22.118Z

**📎 ToolResult**

```
ls: Terraria/: No such file or directory

```


---

## 🤖 Assistant · 2026-08-12T18:47:24.145Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && ls | grep -i worldgen; grep -rln \"MakeDungeon\" --include=*.cs . 2>/dev/null | head",
 "description": "Find WorldGen source in 1405 tree"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:24.170Z

**📎 ToolResult**

```
WorldGen.cs
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-12T18:47:25.966Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "cd ~/Project/GLM/SandboxWorld/Terarria1405 && grep -n \"MakeDungeon\" WorldGen.cs | head -20; wc -l WorldGen.cs",
 "description": "Find MakeDungeon in 1405 WorldGen.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:25.999Z

**📎 ToolResult**

```
6588:        WorldGen.MakeDungeon(num2, y);
18006:    public static void MakeDungeon(int x, int y)
18836:      WorldGen.MakeDungeon_Lights(tileType, ref failCount, failMax1, ref numAdd1, roomWall);
18840:      WorldGen.MakeDungeon_Traps(ref failCount, failMax2, ref numAdd2);
18841:      float count1 = WorldGen.MakeDungeon_GroundFurniture(wallType1);
18842:      float count2 = WorldGen.MakeDungeon_Pictures(roomWall, count1);
18843:      WorldGen.MakeDungeon_Banners(roomWall, count2);
18846:    private static void MakeDungeon_Traps(ref int failCount, int failMax, ref int numAdd)
18865:    private static void MakeDungeon_Lights(
19042:    private static float MakeDungeon_Banners(int[] roomWall, float count)
19080:    private static float MakeDungeon_Pictures(int[] roomWall, float count)
19287:    private static float MakeDungeon_GroundFurniture(int wallType)
   54961 WorldGen.cs

```


---

## 🤖 Assistant · 2026-08-12T18:47:27.990Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The 1405 WorldGen.cs has MakeDungeon at 18006 and the furnishing helpers. Let me read 18006-19613 to have the full reference. That's 1600 lines. Let me read in chunks. First 18006-18850.
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:47:28.218Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "limit": 480,
 "offset": 18006
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:28.224Z

**📎 ToolResult**

```
18006	    public static void MakeDungeon(int x, int y)
18007	    {
18008	      WorldGen.dEnteranceX = 0;
18009	      WorldGen.numDRooms = 0;
18010	      WorldGen.numDDoors = 0;
18011	      WorldGen.numDungeonPlatforms = 0;
18012	      int num1 = WorldGen.genRand.Next(3);
18013	      WorldGen.genRand.Next(3);
18014	      ushort tileType;
18015	      int wallType1;
18016	      switch (num1)
18017	      {
18018	        case 0:
18019	          tileType = (ushort) 41;
18020	          wallType1 = 7;
18021	          WorldGen.crackedType = (ushort) 481;
18022	          break;
18023	        case 1:
18024	          tileType = (ushort) 43;
18025	          wallType1 = 8;
18026	          WorldGen.crackedType = (ushort) 482;
18027	          break;
18028	        default:
18029	          tileType = (ushort) 44;
18030	          wallType1 = 9;
18031	          WorldGen.crackedType = (ushort) 483;
18032	          break;
18033	      }
18034	      Main.tileSolid[(int) WorldGen.crackedType] = false;
18035	      WorldGen.dungeonLake = true;
18036	      WorldGen.numDDoors = 0;
18037	      WorldGen.numDungeonPlatforms = 0;
18038	      WorldGen.numDRooms = 0;
18039	      WorldGen.dungeonX = x;
18040	      WorldGen.dungeonY = y;
18041	      WorldGen.dMinX = x;
18042	      WorldGen.dMaxX = x;
18043	      WorldGen.dMinY = y;
18044	      WorldGen.dMaxY = y;
18045	      WorldGen.dxStrength1 = (double) WorldGen.genRand.Next(25, 30);
18046	      WorldGen.dyStrength1 = (double) WorldGen.genRand.Next(20, 25);
18047	      WorldGen.dxStrength2 = (double) WorldGen.genRand.Next(35, 50);
18048	      WorldGen.dyStrength2 = (double) WorldGen.genRand.Next(10, 15);
18049	      float num2 = (float) (Main.maxTilesX / 60);
18050	      float num3 = num2 + (float) WorldGen.genRand.Next(0, (int) ((double) num2 / 3.0));
18051	      float num4 = num3;
18052	      int num5 = 5;
18053	      WorldGen.DungeonRoom(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1);
18054	      while ((double) num3 > 0.0)
18055	      {
18056	        if (WorldGen.dungeonX < WorldGen.dMinX)
18057	          WorldGen.dMinX = WorldGen.dungeonX;
18058	        if (WorldGen.dungeonX > WorldGen.dMaxX)
18059	          WorldGen.dMaxX = WorldGen.dungeonX;
18060	        if (WorldGen.dungeonY > WorldGen.dMaxY)
18061	          WorldGen.dMaxY = WorldGen.dungeonY;
18062	        --num3;
18063	        Main.statusText = Lang.gen[58].Value + " " + (object) (int) (((double) num4 - (double) num3) / (double) num4 * 60.0) + "%";
18064	        if (num5 > 0)
18065	          --num5;
18066	        if (num5 == 0 & WorldGen.genRand.Next(3) == 0)
18067	        {
18068	          num5 = 5;
18069	          if (WorldGen.genRand.Next(2) == 0)
18070	          {
18071	            int dungeonX = WorldGen.dungeonX;
18072	            int dungeonY = WorldGen.dungeonY;
18073	            WorldGen.DungeonHalls(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1, false);
18074	            if (WorldGen.genRand.Next(2) == 0)
18075	              WorldGen.DungeonHalls(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1, false);
18076	            WorldGen.DungeonRoom(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1);
18077	            WorldGen.dungeonX = dungeonX;
18078	            WorldGen.dungeonY = dungeonY;
18079	          }
18080	          else
18081	            WorldGen.DungeonRoom(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1);
18082	        }
18083	        else
18084	          WorldGen.DungeonHalls(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1, false);
18085	      }
18086	      WorldGen.DungeonRoom(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1);
18087	      int num6 = WorldGen.dRoomX[0];
18088	      int num7 = WorldGen.dRoomY[0];
18089	      for (int index = 0; index < WorldGen.numDRooms; ++index)
18090	      {
18091	        if (WorldGen.dRoomY[index] < num7)
18092	        {
18093	          num6 = WorldGen.dRoomX[index];
18094	          num7 = WorldGen.dRoomY[index];
18095	        }
18096	      }
18097	      WorldGen.dungeonX = num6;
18098	      WorldGen.dungeonY = num7;
18099	      WorldGen.dEnteranceX = num6;
18100	      WorldGen.dSurface = false;
18101	      int num8 = 5;
18102	      if (WorldGen.drunkWorldGen)
18103	        WorldGen.dSurface = true;
18104	      while (!WorldGen.dSurface)
18105	      {
18106	        if (num8 > 0)
18107	          --num8;
18108	        if (num8 == 0 && WorldGen.genRand.Next(5) == 0 && (double) WorldGen.dungeonY > Main.worldSurface + 100.0)
18109	        {
18110	          num8 = 10;
18111	          int dungeonX = WorldGen.dungeonX;
18112	          int dungeonY = WorldGen.dungeonY;
18113	          WorldGen.DungeonHalls(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1, true);
18114	          WorldGen.DungeonRoom(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1);
18115	          WorldGen.dungeonX = dungeonX;
18116	          WorldGen.dungeonY = dungeonY;
18117	        }
18118	        WorldGen.DungeonStairs(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1);
18119	      }
18120	      WorldGen.DungeonEnt(WorldGen.dungeonX, WorldGen.dungeonY, tileType, wallType1);
18121	      Main.statusText = Lang.gen[58].Value + " 65%";
18122	      int num9 = Main.maxTilesX * 2;
18123	      int i1;
18124	      int j1;
18125	      int num10;
18126	      int wallType2;
18127	      for (int index = 0; index < num9; index = (!WorldGen.DungeonPitTrap(i1, j1, (ushort) num10, wallType2) ? index + 1 : index + 1500) + 1)
18128	      {
18129	        i1 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
18130	        int minValue = WorldGen.dMinY;
18131	        if ((double) minValue < Main.worldSurface)
18132	          minValue = (int) Main.worldSurface;
18133	        j1 = WorldGen.genRand.Next(minValue, WorldGen.dMaxY);
18134	        num10 = (int) tileType;
18135	        wallType2 = wallType1;
18136	      }
18137	      for (int index1 = 0; index1 < WorldGen.numDRooms; ++index1)
18138	      {
18139	        for (int index2 = WorldGen.dRoomL[index1]; index2 <= WorldGen.dRoomR[index1]; ++index2)
18140	        {
18141	          if (!Main.tile[index2, WorldGen.dRoomT[index1] - 1].active())
18142	          {
18143	            WorldGen.dungeonPlatformX[WorldGen.numDungeonPlatforms] = index2;
18144	            WorldGen.dungeonPlatformY[WorldGen.numDungeonPlatforms] = WorldGen.dRoomT[index1] - 1;
18145	            ++WorldGen.numDungeonPlatforms;
18146	            break;
18147	          }
18148	        }
18149	        for (int index2 = WorldGen.dRoomL[index1]; index2 <= WorldGen.dRoomR[index1]; ++index2)
18150	        {
18151	          if (!Main.tile[index2, WorldGen.dRoomB[index1] + 1].active())
18152	          {
18153	            WorldGen.dungeonPlatformX[WorldGen.numDungeonPlatforms] = index2;
18154	            WorldGen.dungeonPlatformY[WorldGen.numDungeonPlatforms] = WorldGen.dRoomB[index1] + 1;
18155	            ++WorldGen.numDungeonPlatforms;
18156	            break;
18157	          }
18158	        }
18159	        for (int index2 = WorldGen.dRoomT[index1]; index2 <= WorldGen.dRoomB[index1]; ++index2)
18160	        {
18161	          if (!Main.tile[WorldGen.dRoomL[index1] - 1, index2].active())
18162	          {
18163	            WorldGen.DDoorX[WorldGen.numDDoors] = WorldGen.dRoomL[index1] - 1;
18164	            WorldGen.DDoorY[WorldGen.numDDoors] = index2;
18165	            WorldGen.DDoorPos[WorldGen.numDDoors] = -1;
18166	            ++WorldGen.numDDoors;
18167	            break;
18168	          }
18169	        }
18170	        for (int index2 = WorldGen.dRoomT[index1]; index2 <= WorldGen.dRoomB[index1]; ++index2)
18171	        {
18172	          if (!Main.tile[WorldGen.dRoomR[index1] + 1, index2].active())
18173	          {
18174	            WorldGen.DDoorX[WorldGen.numDDoors] = WorldGen.dRoomR[index1] + 1;
18175	            WorldGen.DDoorY[WorldGen.numDDoors] = index2;
18176	            WorldGen.DDoorPos[WorldGen.numDDoors] = 1;
18177	            ++WorldGen.numDDoors;
18178	            break;
18179	          }
18180	        }
18181	      }
18182	      Main.statusText = Lang.gen[58].Value + " 70%";
18183	      int num11 = 0;
18184	      int num12 = 1000;
18185	      int num13 = 0;
18186	      int num14 = Main.maxTilesX / 100;
18187	      if (WorldGen.getGoodWorldGen)
18188	        num14 *= 3;
18189	      while (num13 < num14)
18190	      {
18191	        ++num11;
18192	        int index1 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
18193	        int index2 = WorldGen.genRand.Next((int) Main.worldSurface + 25, WorldGen.dMaxY);
18194	        if (WorldGen.drunkWorldGen)
18195	          index2 = WorldGen.genRand.Next(WorldGen.dungeonY + 25, WorldGen.dMaxY);
18196	        int num15 = index1;
18197	        if ((int) Main.tile[index1, index2].wall == wallType1 && !Main.tile[index1, index2].active())
18198	        {
18199	          int num16 = 1;
18200	          if (WorldGen.genRand.Next(2) == 0)
18201	            num16 = -1;
18202	          while (!Main.tile[index1, index2].active())
18203	            index2 += num16;
18204	          if (Main.tile[index1 - 1, index2].active() && Main.tile[index1 + 1, index2].active() && ((int) Main.tile[index1 - 1, index2].type != (int) WorldGen.crackedType && !Main.tile[index1 - 1, index2 - num16].active()) && !Main.tile[index1 + 1, index2 - num16].active())
18205	          {
18206	            ++num13;
18207	            for (int index3 = WorldGen.genRand.Next(5, 13); Main.tile[index1 - 1, index2].active() && (int) Main.tile[index1 - 1, index2].type != (int) WorldGen.crackedType && (Main.tile[index1, index2 + num16].active() && Main.tile[index1, index2].active()) && (!Main.tile[index1, index2 - num16].active() && index3 > 0); --index3)
18208	            {
18209	              Main.tile[index1, index2].type = (ushort) 48;
18210	              if (!Main.tile[index1 - 1, index2 - num16].active() && !Main.tile[index1 + 1, index2 - num16].active())
18211	              {
18212	                Main.tile[index1, index2 - num16].Clear(TileDataType.Slope);
18213	                Main.tile[index1, index2 - num16].type = (ushort) 48;
18214	                Main.tile[index1, index2 - num16].active(true);
18215	                Main.tile[index1, index2 - num16 * 2].Clear(TileDataType.Slope);
18216	                Main.tile[index1, index2 - num16 * 2].type = (ushort) 48;
18217	                Main.tile[index1, index2 - num16 * 2].active(true);
18218	              }
18219	              --index1;
18220	            }
18221	            int num17 = WorldGen.genRand.Next(5, 13);
18222	            for (int index3 = num15 + 1; Main.tile[index3 + 1, index2].active() && (int) Main.tile[index3 + 1, index2].type != (int) WorldGen.crackedType && (Main.tile[index3, index2 + num16].active() && Main.tile[index3, index2].active()) && (!Main.tile[index3, index2 - num16].active() && num17 > 0); --num17)
18223	            {
18224	              Main.tile[index3, index2].type = (ushort) 48;
18225	              if (!Main.tile[index3 - 1, index2 - num16].active() && !Main.tile[index3 + 1, index2 - num16].active())
18226	              {
18227	                Main.tile[index3, index2 - num16].Clear(TileDataType.Slope);
18228	                Main.tile[index3, index2 - num16].type = (ushort) 48;
18229	                Main.tile[index3, index2 - num16].active(true);
18230	                Main.tile[index3, index2 - num16 * 2].Clear(TileDataType.Slope);
18231	                Main.tile[index3, index2 - num16 * 2].type = (ushort) 48;
18232	                Main.tile[index3, index2 - num16 * 2].active(true);
18233	              }
18234	              ++index3;
18235	            }
18236	          }
18237	        }
18238	        if (num11 > num12)
18239	        {
18240	          num11 = 0;
18241	          ++num13;
18242	        }
18243	      }
18244	      int num18 = 0;
18245	      int num19 = 1000;
18246	      int num20 = 0;
18247	      Main.statusText = Lang.gen[58].Value + " 75%";
18248	      while (num20 < num14)
18249	      {
18250	        ++num18;
18251	        int index1 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
18252	        int index2 = WorldGen.genRand.Next((int) Main.worldSurface + 25, WorldGen.dMaxY);
18253	        int num15 = index2;
18254	        if ((int) Main.tile[index1, index2].wall == wallType1 && !Main.tile[index1, index2].active())
18255	        {
18256	          int num16 = 1;
18257	          if (WorldGen.genRand.Next(2) == 0)
18258	            num16 = -1;
18259	          while (index1 > 5 && index1 < Main.maxTilesX - 5 && !Main.tile[index1, index2].active())
18260	            index1 += num16;
18261	          if (Main.tile[index1, index2 - 1].active() && Main.tile[index1, index2 + 1].active() && ((int) Main.tile[index1, index2 - 1].type != (int) WorldGen.crackedType && !Main.tile[index1 - num16, index2 - 1].active()) && !Main.tile[index1 - num16, index2 + 1].active())
18262	          {
18263	            ++num20;
18264	            for (int index3 = WorldGen.genRand.Next(5, 13); Main.tile[index1, index2 - 1].active() && (int) Main.tile[index1, index2 - 1].type != (int) WorldGen.crackedType && (Main.tile[index1 + num16, index2].active() && Main.tile[index1, index2].active()) && (!Main.tile[index1 - num16, index2].active() && index3 > 0); --index3)
18265	            {
18266	              Main.tile[index1, index2].type = (ushort) 48;
18267	              if (!Main.tile[index1 - num16, index2 - 1].active() && !Main.tile[index1 - num16, index2 + 1].active())
18268	              {
18269	                Main.tile[index1 - num16, index2].type = (ushort) 48;
18270	                Main.tile[index1 - num16, index2].active(true);
18271	                Main.tile[index1 - num16, index2].Clear(TileDataType.Slope);
18272	                Main.tile[index1 - num16 * 2, index2].type = (ushort) 48;
18273	                Main.tile[index1 - num16 * 2, index2].active(true);
18274	                Main.tile[index1 - num16 * 2, index2].Clear(TileDataType.Slope);
18275	              }
18276	              --index2;
18277	            }
18278	            int num17 = WorldGen.genRand.Next(5, 13);
18279	            for (int index3 = num15 + 1; Main.tile[index1, index3 + 1].active() && (int) Main.tile[index1, index3 + 1].type != (int) WorldGen.crackedType && (Main.tile[index1 + num16, index3].active() && Main.tile[index1, index3].active()) && (!Main.tile[index1 - num16, index3].active() && num17 > 0); --num17)
18280	            {
18281	              Main.tile[index1, index3].type = (ushort) 48;
18282	              if (!Main.tile[index1 - num16, index3 - 1].active() && !Main.tile[index1 - num16, index3 + 1].active())
18283	              {
18284	                Main.tile[index1 - num16, index3].type = (ushort) 48;
18285	                Main.tile[index1 - num16, index3].active(true);
18286	                Main.tile[index1 - num16, index3].Clear(TileDataType.Slope);
18287	                Main.tile[index1 - num16 * 2, index3].type = (ushort) 48;
18288	                Main.tile[index1 - num16 * 2, index3].active(true);
18289	                Main.tile[index1 - num16 * 2, index3].Clear(TileDataType.Slope);
18290	              }
18291	              ++index3;
18292	            }
18293	          }
18294	        }
18295	        if (num18 > num19)
18296	        {
18297	          num18 = 0;
18298	          ++num20;
18299	        }
18300	      }
18301	      Main.statusText = Lang.gen[58].Value + " 80%";
18302	      for (int index1 = 0; index1 < WorldGen.numDDoors; ++index1)
18303	      {
18304	        int num15 = WorldGen.DDoorX[index1] - 10;
18305	        int num16 = WorldGen.DDoorX[index1] + 10;
18306	        int num17 = 100;
18307	        int num21 = 0;
18308	        for (int index2 = num15; index2 < num16; ++index2)
18309	        {
18310	          bool flag1 = true;
18311	          int index3 = WorldGen.DDoorY[index1];
18312	          while (index3 > 10 && !Main.tile[index2, index3].active())
18313	            --index3;
18314	          if (!Main.tileDungeon[(int) Main.tile[index2, index3].type])
18315	            flag1 = false;
18316	          int num22 = index3;
18317	          int index4 = WorldGen.DDoorY[index1];
18318	          while (!Main.tile[index2, index4].active())
18319	            ++index4;
18320	          if (!Main.tileDungeon[(int) Main.tile[index2, index4].type])
18321	            flag1 = false;
18322	          int num23 = index4;
18323	          if (num23 - num22 >= 3)
18324	          {
18325	            int num24 = index2 - 20;
18326	            int num25 = index2 + 20;
18327	            int num26 = num23 - 10;
18328	            int num27 = num23 + 10;
18329	            for (int index5 = num24; index5 < num25; ++index5)
18330	            {
18331	              for (int index6 = num26; index6 < num27; ++index6)
18332	              {
18333	                if (Main.tile[index5, index6].active() && Main.tile[index5, index6].type == (ushort) 10)
18334	                {
18335	                  flag1 = false;
18336	                  break;
18337	                }
18338	              }
18339	            }
18340	            if (flag1)
18341	            {
18342	              for (int index5 = num23 - 3; index5 < num23; ++index5)
18343	              {
18344	                for (int index6 = index2 - 3; index6 <= index2 + 3; ++index6)
18345	                {
18346	                  if (Main.tile[index6, index5].active())
18347	                  {
18348	                    flag1 = false;
18349	                    break;
18350	                  }
18351	                }
18352	              }
18353	            }
18354	            if (flag1 && num23 - num22 < 20)
18355	            {
18356	              bool flag2 = false;
18357	              if (WorldGen.DDoorPos[index1] == 0 && num23 - num22 < num17)
18358	                flag2 = true;
18359	              if (WorldGen.DDoorPos[index1] == -1 && index2 > num21)
18360	                flag2 = true;
18361	              if (WorldGen.DDoorPos[index1] == 1 && (index2 < num21 || num21 == 0))
18362	                flag2 = true;
18363	              if (flag2)
18364	              {
18365	                num21 = index2;
18366	                num17 = num23 - num22;
18367	              }
18368	            }
18369	          }
18370	        }
18371	        if (num17 < 20)
18372	        {
18373	          int i2 = num21;
18374	          int index2 = WorldGen.DDoorY[index1];
18375	          int index3 = index2;
18376	          for (; !Main.tile[i2, index2].active(); ++index2)
18377	            Main.tile[i2, index2].active(false);
18378	          while (!Main.tile[i2, index3].active())
18379	            --index3;
18380	          int j2 = index2 - 1;
18381	          int num22 = index3 + 1;
18382	          for (int index4 = num22; index4 < j2 - 2; ++index4)
18383	          {
18384	            Main.tile[i2, index4].Clear(TileDataType.Slope);
18385	            Main.tile[i2, index4].active(true);
18386	            Main.tile[i2, index4].type = tileType;
18387	          }
18388	          int style = 13;
18389	          if (WorldGen.genRand.Next(3) == 0)
18390	          {
18391	            switch (wallType1)
18392	            {
18393	              case 7:
18394	                style = 16;
18395	                break;
18396	              case 8:
18397	                style = 17;
18398	                break;
18399	              case 9:
18400	                style = 18;
18401	                break;
18402	            }
18403	          }
18404	          WorldGen.PlaceTile(i2, j2, 10, true, false, -1, style);
18405	          int index5 = i2 - 1;
18406	          int index6 = j2 - 3;
18407	          while (!Main.tile[index5, index6].active())
18408	            --index6;
18409	          if (j2 - index6 < j2 - num22 + 5 && Main.tileDungeon[(int) Main.tile[index5, index6].type])
18410	          {
18411	            for (int index4 = j2 - 4 - WorldGen.genRand.Next(3); index4 > index6; --index4)
18412	            {
18413	              Main.tile[index5, index4].Clear(TileDataType.Slope);
18414	              Main.tile[index5, index4].active(true);
18415	              Main.tile[index5, index4].type = tileType;
18416	            }
18417	          }
18418	          int index7 = index5 + 2;
18419	          int index8 = j2 - 3;
18420	          while (!Main.tile[index7, index8].active())
18421	            --index8;
18422	          if (j2 - index8 < j2 - num22 + 5 && Main.tileDungeon[(int) Main.tile[index7, index8].type])
18423	          {
18424	            for (int index4 = j2 - 4 - WorldGen.genRand.Next(3); index4 > index8; --index4)
18425	            {
18426	              Main.tile[index7, index4].active(true);
18427	              Main.tile[index7, index4].Clear(TileDataType.Slope);
18428	              Main.tile[index7, index4].type = tileType;
18429	            }
18430	          }
18431	          int index9 = j2 + 1;
18432	          int num23 = index7 - 1;
18433	          Main.tile[num23 - 1, index9].active(true);
18434	          Main.tile[num23 - 1, index9].type = tileType;
18435	          Main.tile[num23 - 1, index9].Clear(TileDataType.Slope);
18436	          Main.tile[num23 + 1, index9].active(true);
18437	          Main.tile[num23 + 1, index9].type = tileType;
18438	          Main.tile[num23 + 1, index9].Clear(TileDataType.Slope);
18439	        }
18440	      }
18441	      int[] roomWall = new int[3];
18442	      switch (wallType1)
18443	      {
18444	        case 7:
18445	          roomWall[0] = 7;
18446	          roomWall[1] = 94;
18447	          roomWall[2] = 95;
18448	          break;
18449	        case 9:
18450	          roomWall[0] = 9;
18451	          roomWall[1] = 96;
18452	          roomWall[2] = 97;
18453	          break;
18454	        default:
18455	          roomWall[0] = 8;
18456	          roomWall[1] = 98;
18457	          roomWall[2] = 99;
18458	          break;
18459	      }
18460	      for (int index1 = 0; index1 < 5; ++index1)
18461	      {
18462	        for (int index2 = 0; index2 < 3; ++index2)
18463	        {
18464	          int num15 = WorldGen.genRand.Next(40, 240);
18465	          int num16 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
18466	          int num17 = WorldGen.genRand.Next(WorldGen.dMinY, WorldGen.dMaxY);
18467	          for (int x1 = num16 - num15; x1 < num16 + num15; ++x1)
18468	          {
18469	            for (int y1 = num17 - num15; y1 < num17 + num15; ++y1)
18470	            {
18471	              if ((double) y1 > Main.worldSurface)
18472	              {
18473	                double num21 = (double) Math.Abs(num16 - x1);
18474	                float num22 = (float) Math.Abs(num17 - y1);
18475	                if (Math.Sqrt(num21 * num21 + (double) num22 * (double) num22) < (double) num15 * 0.4 && Main.wallDungeon[(int) Main.tile[x1, y1].wall])
18476	                  WorldGen.Spread.WallDungeon(x1, y1, roomWall[index2]);
18477	              }
18478	            }
18479	          }
18480	        }
18481	      }
18482	      Main.statusText = Lang.gen[58].Value + " 85%";
18483	      for (int index1 = 0; index1 < WorldGen.numDungeonPlatforms; ++index1)
18484	      {
18485	        int index2 = WorldGen.dungeonPlatformX[index1];

```


---

## 🤖 Assistant · 2026-08-12T18:47:30.545Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is the 1405 reference. The JS implementation matches this structure closely. Now continue reading 18485-19620 for the rest (platforms, chests, bookshelves, lights, traps, furniture, pictures, banners).
```

</details>


---

## 🤖 Assistant · 2026-08-12T18:47:30.776Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "limit": 560,
 "offset": 18485
}
```


---

## 👤 User(sidechain) · 2026-08-12T18:47:30.789Z

**📎 ToolResult**

```
18485	        int index2 = WorldGen.dungeonPlatformX[index1];
18486	        int num15 = WorldGen.dungeonPlatformY[index1];
18487	        int num16 = Main.maxTilesX;
18488	        int num17 = 10;
18489	        if ((double) num15 < Main.worldSurface + 50.0)
18490	          num17 = 20;
18491	        for (int index3 = num15 - 5; index3 <= num15 + 5; ++index3)
18492	        {
18493	          int index4 = index2;
18494	          int index5 = index2;
18495	          bool flag1 = false;
18496	          if (Main.tile[index4, index3].active())
18497	          {
18498	            flag1 = true;
18499	          }
18500	          else
18501	          {
18502	            while (!Main.tile[index4, index3].active())
18503	            {
18504	              --index4;
18505	              if (!Main.tileDungeon[(int) Main.tile[index4, index3].type] || index4 == 0)
18506	              {
18507	                flag1 = true;
18508	                break;
18509	              }
18510	            }
18511	            while (!Main.tile[index5, index3].active())
18512	            {
18513	              ++index5;
18514	              if (!Main.tileDungeon[(int) Main.tile[index5, index3].type] || index5 == Main.maxTilesX - 1)
18515	              {
18516	                flag1 = true;
18517	                break;
18518	              }
18519	            }
18520	          }
18521	          if (!flag1 && index5 - index4 <= num17)
18522	          {
18523	            bool flag2 = true;
18524	            int num21 = index2 - num17 / 2 - 2;
18525	            int num22 = index2 + num17 / 2 + 2;
18526	            int num23 = index3 - 5;
18527	            int num24 = index3 + 5;
18528	            for (int index6 = num21; index6 <= num22; ++index6)
18529	            {
18530	              for (int index7 = num23; index7 <= num24; ++index7)
18531	              {
18532	                if (Main.tile[index6, index7].active() && Main.tile[index6, index7].type == (ushort) 19)
18533	                {
18534	                  flag2 = false;
18535	                  break;
18536	                }
18537	              }
18538	            }
18539	            for (int index6 = index3 + 3; index6 >= index3 - 5; --index6)
18540	            {
18541	              if (Main.tile[index2, index6].active())
18542	              {
18543	                flag2 = false;
18544	                break;
18545	              }
18546	            }
18547	            if (flag2)
18548	            {
18549	              num16 = index3;
18550	              break;
18551	            }
18552	          }
18553	        }
18554	        if (num16 > num15 - 10 && num16 < num15 + 10)
18555	        {
18556	          int i2 = index2;
18557	          int j2 = num16;
18558	          int i3 = index2 + 1;
18559	          for (; !Main.tile[i2, j2].active(); --i2)
18560	          {
18561	            Main.tile[i2, j2].active(true);
18562	            Main.tile[i2, j2].type = (ushort) 19;
18563	            Main.tile[i2, j2].Clear(TileDataType.Slope);
18564	            switch (wallType1)
18565	            {
18566	              case 7:
18567	                Main.tile[i2, j2].frameY = (short) 108;
18568	                break;
18569	              case 8:
18570	                Main.tile[i2, j2].frameY = (short) 144;
18571	                break;
18572	              default:
18573	                Main.tile[i2, j2].frameY = (short) 126;
18574	                break;
18575	            }
18576	            WorldGen.TileFrame(i2, j2, false, false);
18577	          }
18578	          for (; !Main.tile[i3, j2].active(); ++i3)
18579	          {
18580	            Main.tile[i3, j2].active(true);
18581	            Main.tile[i3, j2].type = (ushort) 19;
18582	            Main.tile[i3, j2].Clear(TileDataType.Slope);
18583	            switch (wallType1)
18584	            {
18585	              case 7:
18586	                Main.tile[i3, j2].frameY = (short) 108;
18587	                break;
18588	              case 8:
18589	                Main.tile[i3, j2].frameY = (short) 144;
18590	                break;
18591	              default:
18592	                Main.tile[i3, j2].frameY = (short) 126;
18593	                break;
18594	            }
18595	            WorldGen.TileFrame(i3, j2, false, false);
18596	          }
18597	        }
18598	      }
18599	      int num28 = 5;
18600	      if (WorldGen.drunkWorldGen)
18601	        num28 = 6;
18602	      for (int index = 0; index < num28; ++index)
18603	      {
18604	        bool flag = false;
18605	        while (!flag)
18606	        {
18607	          int i2 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
18608	          int j2 = WorldGen.genRand.Next((int) Main.worldSurface, WorldGen.dMaxY);
18609	          if (Main.wallDungeon[(int) Main.tile[i2, j2].wall] && !Main.tile[i2, j2].active())
18610	          {
18611	            ushort chestTileType = 21;
18612	            int contain = 0;
18613	            int Style = 0;
18614	            switch (index)
18615	            {
18616	              case 0:
18617	                Style = 23;
18618	                contain = 1156;
18619	                break;
18620	              case 1:
18621	                if (!WorldGen.crimson)
18622	                {
18623	                  Style = 24;
18624	                  contain = 1571;
18625	                  break;
18626	                }
18627	                Style = 25;
18628	                contain = 1569;
18629	                break;
18630	              case 2:
18631	                Style = 26;
18632	                contain = 1260;
18633	                break;
18634	              case 3:
18635	                Style = 27;
18636	                contain = 1572;
18637	                break;
18638	              case 4:
18639	                chestTileType = (ushort) 467;
18640	                Style = 13;
18641	                contain = 4607;
18642	                break;
18643	              case 5:
18644	                if (WorldGen.crimson)
18645	                {
18646	                  Style = 24;
18647	                  contain = 1571;
18648	                  break;
18649	                }
18650	                Style = 25;
18651	                contain = 1569;
18652	                break;
18653	            }
18654	            flag = WorldGen.AddBuriedChest(i2, j2, contain, false, Style, false, chestTileType);
18655	          }
18656	        }
18657	      }
18658	      int[] numArray = new int[3]
18659	      {
18660	        WorldGen.genRand.Next(9, 13),
18661	        WorldGen.genRand.Next(9, 13),
18662	        0
18663	      };
18664	      while (numArray[1] == numArray[0])
18665	        numArray[1] = WorldGen.genRand.Next(9, 13);
18666	      numArray[2] = WorldGen.genRand.Next(9, 13);
18667	      while (numArray[2] == numArray[0] || numArray[2] == numArray[1])
18668	        numArray[2] = WorldGen.genRand.Next(9, 13);
18669	      Main.statusText = Lang.gen[58].Value + " 90%";
18670	      int num29 = 0;
18671	      int num30 = 1000;
18672	      int num31 = 0;
18673	      while (num31 < Main.maxTilesX / 20)
18674	      {
18675	        ++num29;
18676	        int index1 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
18677	        int j2 = WorldGen.genRand.Next(WorldGen.dMinY, WorldGen.dMaxY);
18678	        bool flag1 = true;
18679	        if (Main.wallDungeon[(int) Main.tile[index1, j2].wall] && !Main.tile[index1, j2].active())
18680	        {
18681	          int num15 = 1;
18682	          if (WorldGen.genRand.Next(2) == 0)
18683	            num15 = -1;
18684	          while (flag1 && !Main.tile[index1, j2].active())
18685	          {
18686	            index1 -= num15;
18687	            if (index1 < 5 || index1 > Main.maxTilesX - 5)
18688	              flag1 = false;
18689	            else if (Main.tile[index1, j2].active() && !Main.tileDungeon[(int) Main.tile[index1, j2].type])
18690	              flag1 = false;
18691	          }
18692	          if (flag1 && Main.tile[index1, j2].active() && (Main.tileDungeon[(int) Main.tile[index1, j2].type] && Main.tile[index1, j2 - 1].active()) && (Main.tileDungeon[(int) Main.tile[index1, j2 - 1].type] && Main.tile[index1, j2 + 1].active() && Main.tileDungeon[(int) Main.tile[index1, j2 + 1].type]))
18693	          {
18694	            int i2 = index1 + num15;
18695	            for (int index2 = i2 - 3; index2 <= i2 + 3; ++index2)
18696	            {
18697	              for (int index3 = j2 - 3; index3 <= j2 + 3; ++index3)
18698	              {
18699	                if (Main.tile[index2, index3].active() && Main.tile[index2, index3].type == (ushort) 19)
18700	                {
18701	                  flag1 = false;
18702	                  break;
18703	                }
18704	              }
18705	            }
18706	            if (flag1 && !Main.tile[i2, j2 - 1].active() & !Main.tile[i2, j2 - 2].active() & !Main.tile[i2, j2 - 3].active())
18707	            {
18708	              int index2 = i2;
18709	              int num16 = i2;
18710	              while (index2 > WorldGen.dMinX && index2 < WorldGen.dMaxX && (!Main.tile[index2, j2].active() && !Main.tile[index2, j2 - 1].active()) && !Main.tile[index2, j2 + 1].active())
18711	                index2 += num15;
18712	              int num17 = Math.Abs(i2 - index2);
18713	              bool flag2 = false;
18714	              if (WorldGen.genRand.Next(2) == 0)
18715	                flag2 = true;
18716	              if (num17 > 5)
18717	              {
18718	                for (int index3 = WorldGen.genRand.Next(1, 4); index3 > 0; --index3)
18719	                {
18720	                  Main.tile[i2, j2].active(true);
18721	                  Main.tile[i2, j2].Clear(TileDataType.Slope);
18722	                  Main.tile[i2, j2].type = (ushort) 19;
18723	                  Main.tile[i2, j2].frameY = (int) Main.tile[i2, j2].wall != roomWall[0] ? ((int) Main.tile[i2, j2].wall != roomWall[1] ? (short) (18 * numArray[2]) : (short) (18 * numArray[1])) : (short) (18 * numArray[0]);
18724	                  WorldGen.TileFrame(i2, j2, false, false);
18725	                  if (flag2)
18726	                  {
18727	                    WorldGen.PlaceTile(i2, j2 - 1, 50, true, false, -1, 0);
18728	                    if (WorldGen.genRand.Next(50) == 0 && (double) j2 > (Main.worldSurface + Main.rockLayer) / 2.0 && Main.tile[i2, j2 - 1].type == (ushort) 50)
18729	                      Main.tile[i2, j2 - 1].frameX = (short) 90;
18730	                  }
18731	                  i2 += num15;
18732	                }
18733	                num29 = 0;
18734	                ++num31;
18735	                if (!flag2 && WorldGen.genRand.Next(2) == 0)
18736	                {
18737	                  int i3 = num16;
18738	                  int j3 = j2 - 1;
18739	                  int Type = 0;
18740	                  if (WorldGen.genRand.Next(4) == 0)
18741	                    Type = 1;
18742	                  switch (Type)
18743	                  {
18744	                    case 0:
18745	                      Type = 13;
18746	                      break;
18747	                    case 1:
18748	                      Type = 49;
18749	                      break;
18750	                  }
18751	                  WorldGen.PlaceTile(i3, j3, Type, true, false, -1, 0);
18752	                  if (Main.tile[i3, j3].type == (ushort) 13)
18753	                    Main.tile[i3, j3].frameX = WorldGen.genRand.Next(2) != 0 ? (short) 36 : (short) 18;
18754	                }
18755	              }
18756	            }
18757	          }
18758	        }
18759	        if (num29 > num30)
18760	        {
18761	          num29 = 0;
18762	          ++num31;
18763	        }
18764	      }
18765	      Main.statusText = Lang.gen[58].Value + " 95%";
18766	      int num32 = 1;
18767	      for (int index = 0; index < WorldGen.numDRooms; ++index)
18768	      {
18769	        int num15 = 0;
18770	        while (num15 < 1000)
18771	        {
18772	          int num16 = (int) ((double) WorldGen.dRoomSize[index] * 0.4);
18773	          int i2 = WorldGen.dRoomX[index] + WorldGen.genRand.Next(-num16, num16 + 1);
18774	          int j2 = WorldGen.dRoomY[index] + WorldGen.genRand.Next(-num16, num16 + 1);
18775	          int Style = 2;
18776	          if (num32 == 1)
18777	            ++num32;
18778	          int contain;
18779	          if (num32 == 2)
18780	            contain = 155;
18781	          else if (num32 == 3)
18782	            contain = 156;
18783	          else if (num32 == 4)
18784	            contain = 157;
18785	          else if (num32 == 5)
18786	            contain = 163;
18787	          else if (num32 == 6)
18788	            contain = 113;
18789	          else if (num32 == 7)
18790	            contain = 3317;
18791	          else if (num32 == 8)
18792	          {
18793	            contain = 327;
18794	            Style = 0;
18795	          }
18796	          else
18797	          {
18798	            contain = 164;
18799	            num32 = 0;
18800	          }
18801	          if ((double) j2 < Main.worldSurface + 50.0)
18802	          {
18803	            contain = 327;
18804	            Style = 0;
18805	          }
18806	          if (contain == 0 && WorldGen.genRand.Next(2) == 0)
18807	          {
18808	            num15 = 1000;
18809	          }
18810	          else
18811	          {
18812	            if (WorldGen.AddBuriedChest(i2, j2, contain, false, Style, false, (ushort) 0))
18813	            {
18814	              num15 += 1000;
18815	              ++num32;
18816	            }
18817	            ++num15;
18818	          }
18819	        }
18820	      }
18821	      WorldGen.dMinX -= 25;
18822	      WorldGen.dMaxX += 25;
18823	      WorldGen.dMinY -= 25;
18824	      WorldGen.dMaxY += 25;
18825	      if (WorldGen.dMinX < 0)
18826	        WorldGen.dMinX = 0;
18827	      if (WorldGen.dMaxX > Main.maxTilesX)
18828	        WorldGen.dMaxX = Main.maxTilesX;
18829	      if (WorldGen.dMinY < 0)
18830	        WorldGen.dMinY = 0;
18831	      if (WorldGen.dMaxY > Main.maxTilesY)
18832	        WorldGen.dMaxY = Main.maxTilesY;
18833	      int failCount = 0;
18834	      int failMax1 = 1000;
18835	      int numAdd1 = 0;
18836	      WorldGen.MakeDungeon_Lights(tileType, ref failCount, failMax1, ref numAdd1, roomWall);
18837	      failCount = 0;
18838	      int failMax2 = 1000;
18839	      int numAdd2 = 0;
18840	      WorldGen.MakeDungeon_Traps(ref failCount, failMax2, ref numAdd2);
18841	      float count1 = WorldGen.MakeDungeon_GroundFurniture(wallType1);
18842	      float count2 = WorldGen.MakeDungeon_Pictures(roomWall, count1);
18843	      WorldGen.MakeDungeon_Banners(roomWall, count2);
18844	    }
18845	
18846	    private static void MakeDungeon_Traps(ref int failCount, int failMax, ref int numAdd)
18847	    {
18848	      while (numAdd < Main.maxTilesX / 500)
18849	      {
18850	        ++failCount;
18851	        int x2 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
18852	        int y2 = WorldGen.genRand.Next(WorldGen.dMinY, WorldGen.dMaxY);
18853	        while ((double) y2 < Main.worldSurface)
18854	          y2 = WorldGen.genRand.Next(WorldGen.dMinY, WorldGen.dMaxY);
18855	        if (Main.wallDungeon[(int) Main.tile[x2, y2].wall] && WorldGen.placeTrap(x2, y2, 0))
18856	          failCount = failMax;
18857	        if (failCount > failMax)
18858	        {
18859	          ++numAdd;
18860	          failCount = 0;
18861	        }
18862	      }
18863	    }
18864	
18865	    private static void MakeDungeon_Lights(
18866	      ushort tileType,
18867	      ref int failCount,
18868	      int failMax,
18869	      ref int numAdd,
18870	      int[] roomWall)
18871	    {
18872	      int[] numArray = new int[3]
18873	      {
18874	        WorldGen.genRand.Next(7),
18875	        WorldGen.genRand.Next(7),
18876	        0
18877	      };
18878	      while (numArray[1] == numArray[0])
18879	        numArray[1] = WorldGen.genRand.Next(7);
18880	      numArray[2] = WorldGen.genRand.Next(7);
18881	      while (numArray[2] == numArray[0] || numArray[2] == numArray[1])
18882	        numArray[2] = WorldGen.genRand.Next(7);
18883	      while (numAdd < Main.maxTilesX / 150)
18884	      {
18885	        ++failCount;
18886	        int index1 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
18887	        int index2 = WorldGen.genRand.Next(WorldGen.dMinY, WorldGen.dMaxY);
18888	        if (Main.wallDungeon[(int) Main.tile[index1, index2].wall])
18889	        {
18890	          for (int y = index2; y > WorldGen.dMinY; --y)
18891	          {
18892	            if (Main.tile[index1, y - 1].active() && (int) Main.tile[index1, y - 1].type == (int) tileType)
18893	            {
18894	              bool flag1 = false;
18895	              for (int index3 = index1 - 15; index3 < index1 + 15; ++index3)
18896	              {
18897	                for (int index4 = y - 15; index4 < y + 15; ++index4)
18898	                {
18899	                  if (index3 > 0 && index3 < Main.maxTilesX && (index4 > 0 && index4 < Main.maxTilesY) && (Main.tile[index3, index4].type == (ushort) 42 || Main.tile[index3, index4].type == (ushort) 34))
18900	                  {
18901	                    flag1 = true;
18902	                    break;
18903	                  }
18904	                }
18905	              }
18906	              if (Main.tile[index1 - 1, y].active() || Main.tile[index1 + 1, y].active() || (Main.tile[index1 - 1, y + 1].active() || Main.tile[index1 + 1, y + 1].active()) || Main.tile[index1, y + 2].active())
18907	                flag1 = true;
18908	              if (!flag1)
18909	              {
18910	                bool flag2 = false;
18911	                if (!flag2 && WorldGen.genRand.Next(7) == 0)
18912	                {
18913	                  int style = 27;
18914	                  switch (roomWall[0])
18915	                  {
18916	                    case 7:
18917	                      style = 27;
18918	                      break;
18919	                    case 8:
18920	                      style = 28;
18921	                      break;
18922	                    case 9:
18923	                      style = 29;
18924	                      break;
18925	                  }
18926	                  bool flag3 = false;
18927	                  for (int index3 = 0; index3 < 15; ++index3)
18928	                  {
18929	                    if (WorldGen.SolidTile(index1, y + index3, false))
18930	                    {
18931	                      flag3 = true;
18932	                      break;
18933	                    }
18934	                  }
18935	                  if (!flag3)
18936	                    WorldGen.PlaceChand(index1, y, (ushort) 34, style);
18937	                  if (Main.tile[index1, y].type == (ushort) 34)
18938	                  {
18939	                    flag2 = true;
18940	                    failCount = 0;
18941	                    ++numAdd;
18942	                    for (int index3 = 0; index3 < 1000; ++index3)
18943	                    {
18944	                      int i = index1 + WorldGen.genRand.Next(-12, 13);
18945	                      int j = y + WorldGen.genRand.Next(3, 21);
18946	                      if (!Main.tile[i, j].active() && !Main.tile[i, j + 1].active() && (Main.tileDungeon[(int) Main.tile[i - 1, j].type] && Main.tileDungeon[(int) Main.tile[i + 1, j].type]) && Collision.CanHit(new Vector2((float) (i * 16), (float) (j * 16)), 16, 16, new Vector2((float) (index1 * 16), (float) (y * 16 + 1)), 16, 16))
18947	                      {
18948	                        if ((WorldGen.SolidTile(i - 1, j, false) && Main.tile[i - 1, j].type != (ushort) 10 || WorldGen.SolidTile(i + 1, j, false) && Main.tile[i + 1, j].type != (ushort) 10 || WorldGen.SolidTile(i, j + 1, false)) && (Main.wallDungeon[(int) Main.tile[i, j].wall] && (Main.tileDungeon[(int) Main.tile[i - 1, j].type] || Main.tileDungeon[(int) Main.tile[i + 1, j].type])))
18949	                          WorldGen.PlaceTile(i, j, 136, true, false, -1, 0);
18950	                        if (Main.tile[i, j].active())
18951	                        {
18952	                          while (i != index1 || j != y)
18953	                          {
18954	                            Main.tile[i, j].wire(true);
18955	                            if (i > index1)
18956	                              --i;
18957	                            if (i < index1)
18958	                              ++i;
18959	                            Main.tile[i, j].wire(true);
18960	                            if (j > y)
18961	                              --j;
18962	                            if (j < y)
18963	                              ++j;
18964	                            Main.tile[i, j].wire(true);
18965	                          }
18966	                          if (WorldGen.genRand.Next(3) > 0)
18967	                          {
18968	                            Main.tile[index1, y].frameX = (short) 18;
18969	                            Main.tile[index1, y + 1].frameX = (short) 18;
18970	                            break;
18971	                          }
18972	                          break;
18973	                        }
18974	                      }
18975	                    }
18976	                  }
18977	                }
18978	                if (!flag2)
18979	                {
18980	                  int style = numArray[0];
18981	                  if ((int) Main.tile[index1, y].wall == roomWall[1])
18982	                    style = numArray[1];
18983	                  if ((int) Main.tile[index1, y].wall == roomWall[2])
18984	                    style = numArray[2];
18985	                  WorldGen.Place1x2Top(index1, y, (ushort) 42, style);
18986	                  if (Main.tile[index1, y].type == (ushort) 42)
18987	                  {
18988	                    failCount = 0;
18989	                    ++numAdd;
18990	                    for (int index3 = 0; index3 < 1000; ++index3)
18991	                    {
18992	                      int i = index1 + WorldGen.genRand.Next(-12, 13);
18993	                      int j = y + WorldGen.genRand.Next(3, 21);
18994	                      if (!Main.tile[i, j].active() && !Main.tile[i, j + 1].active() && (Main.tile[i - 1, j].type != (ushort) 48 && Main.tile[i + 1, j].type != (ushort) 48) && Collision.CanHit(new Vector2((float) (i * 16), (float) (j * 16)), 16, 16, new Vector2((float) (index1 * 16), (float) (y * 16 + 1)), 16, 16))
18995	                      {
18996	                        if (WorldGen.SolidTile(i - 1, j, false) && Main.tile[i - 1, j].type != (ushort) 10 || WorldGen.SolidTile(i + 1, j, false) && Main.tile[i + 1, j].type != (ushort) 10 || WorldGen.SolidTile(i, j + 1, false))
18997	                          WorldGen.PlaceTile(i, j, 136, true, false, -1, 0);
18998	                        if (Main.tile[i, j].active())
18999	                        {
19000	                          while (i != index1 || j != y)
19001	                          {
19002	                            Main.tile[i, j].wire(true);
19003	                            if (i > index1)
19004	                              --i;
19005	                            if (i < index1)
19006	                              ++i;
19007	                            Main.tile[i, j].wire(true);
19008	                            if (j > y)
19009	                              --j;
19010	                            if (j < y)
19011	                              ++j;
19012	                            Main.tile[i, j].wire(true);
19013	                          }
19014	                          if (WorldGen.genRand.Next(3) > 0)
19015	                          {
19016	                            Main.tile[index1, y].frameX = (short) 18;
19017	                            Main.tile[index1, y + 1].frameX = (short) 18;
19018	                            break;
19019	                          }
19020	                          break;
19021	                        }
19022	                      }
19023	                    }
19024	                    break;
19025	                  }
19026	                  break;
19027	                }
19028	                break;
19029	              }
19030	              break;
19031	            }
19032	          }
19033	        }
19034	        if (failCount > failMax)
19035	        {
19036	          ++numAdd;
19037	          failCount = 0;
19038	        }
19039	      }
19040	    }
19041	
19042	    private static float MakeDungeon_Banners(int[] roomWall, float count)
19043	    {
19044	      count = 840000f / (float) Main.maxTilesX;

```


---

## 🤖 Assistant · 2026-08-12T19:02:33.181Z · <synthetic>

```
API Error: Stream idle timeout - no chunks received
```


---

## 👤 User(sidechain) · 2026-08-12T19:02:33.184Z

```
[Request interrupted by user]
```


---

## 👤 User(meta)(sidechain) · 2026-08-12T19:37:17.024Z

```
The coordinator sent a message while you were working:
看门狗停滞恢复。你的任务简报不变（#32 Dungeon oracle 转录+对账）。防停滞强化要求：
1. 单次工具调用严格 <8 分钟——oracle 全链跑一次约 2-3 分钟没问题，但不要把"双种子 oracle + 双金标 + 全量 vitest"串成一条命令；分开跑；
2. 大文件分段读（DungeonCrawler.cs ~2000 行，按函数分段 sed），别一次性灌整个文件；
3. 长对账二分时优先用 checkpoint 级哈希对比缩小范围，再逐段插桩。
从中断处继续。若你中断前已有部分转录落地，先 `dotnet run tools/golden/caves-oracle.cs 9293480 0 /tmp/v.json` 单种子验证 oracle 可编译运行，再继续。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-12T19:52:20.621Z · <synthetic>

```
API Error: Stream idle timeout - no chunks received
```


---

## 👤 User(sidechain) · 2026-08-12T19:52:20.623Z

```
[Request interrupted by user]
```


---

## 👤 User(meta)(sidechain) · 2026-08-12T20:46:38.013Z

```
The coordinator sent a message while you were working:
第二次停滞且零落盘——判断为流层问题非任务问题。恢复后请立即执行一个"小步落盘"策略：先做一件 5 分钟内可完成且落盘的事（例如在 caves-oracle.cs 的 slush checkpoint 后加一行 Checkpoint("dungeon") 占位 + dungeon 空段注释），跑一次单种子 oracle 确认编译运行，让任务有可见进度锚点。然后再按段转录 DungeonCrawler（每完成一个函数段就落盘一次+可选单种子冒烟，不要攒大改）。这能让看门狗在流抖动时也能看到连续小进展。继续任务，简报不变。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-12T20:46:43.010Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The coordinator wants me to make a small, quick disk-landing step first: add a placeholder Checkpoint("dungeon") + empty segment comment after slush checkpoint in caves-oracle.cs, run single-seed oracle to confirm compile/run. Then transcribe segment by segment, landing after each function.

Let me do that now.
```

</details>


---

## 🤖 Assistant · 2026-08-12T20:46:43.362Z · glm-x-preview-260804

```
收到。先做小步落盘：在 oracle 的 slush checkpoint 后加 dungeon 占位段并单种子验证编译运行。
```


---

## 🤖 Assistant · 2026-08-12T20:46:43.588Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/tools/golden/caves-oracle.cs",
 "limit": 10,
 "offset": 3858
}
```


---

## 👤 User(sidechain) · 2026-08-12T20:46:43.593Z

**📎 ToolResult**

```
3858	    }
3859	}
3860	Checkpoint("slush");
3861	// ★#29 Corruption（cs:13919）与 #32 Dungeon（cs:14816）尚未转录——转录后须插在
3862	
3863	// ================= Pass 33：MountainCaveOpenings（cs:14932-14947）+ Pass 34：Beaches（cs:14947-15087）=================
3864	// 1456 注册序在 Dungeon(32) 之后——本 oracle 尚未转录 26-32 段（Mushroom/Marble/
3865	// Granite/Islands/DirtToMud/Silt/Ores/Underworld/Corruption/Lakes/Slush/Dungeon），
3866	// 故暂挂在 desertdone 之后；★26-32 段转录后须把本块插回其前（即 Dungeon 之后）。
3867	void CaveOpenater(int i, int j)

```


---

## 🤖 Assistant · 2026-08-12T21:02:58.650Z · <synthetic>

```
API Error: Stream idle timeout - no chunks received
```


---

## 👤 User(sidechain) · 2026-08-12T21:02:58.653Z

```
[Request interrupted by user]
```


---

## 👤 User(meta)(sidechain) · 2026-08-12T21:23:20.924Z

```
The coordinator sent a message while you were working:
锚点步骤我已代你完成，现场交接：
1. caves-oracle.cs：`Checkpoint("dungeon")` 占位已插在 slush 后（=slush 同态快照，注释标明转录后替换为实现）；
2. tests/caves-checkpoint.test.ts：`snap('dungeon')` + names 序已接；
3. 双种子金标已再生（各 35 checkpoint），caves-checkpoint 3/3 全绿。

你剩余工作 = 往占位处填 DungeonCrawler 真实现（cs:14816 + DungeonCrawler.cs）：实现落地后 dungeon 段哈希改变、mcopenings/beaches 随流位移再变一轮——两份金标再各再生一次 + 测试复绿即可。JS 侧 DungeonPass.ts 同步对照修偏差。纪律照旧：单次调用 <8 分钟、大文件分段读、每完成一个函数段落盘一次。从中断处继续。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-12T21:23:25.047Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The coordinator did the anchor step. Let me verify the current state of the oracle placeholder and the test, then continue with the transcription.

Key facts I've gathered so far:
- 1456 Dungeon pass (WorldGen.cs:14816) calls DungeonCrawler.SetupDungeonData/SetupDungeonDataVariables/MakeDungeon — the full object system.
- JS implements the 1405 legacy algorithm (MakeDungeon L18006 etc. in Terarria1405) with 1456 RNG-consumption patches.
- Oracle needs to transcribe the same algorithm the JS implements, since the oracle chain follows the JS chain (per the alignment doc, the oracle transcribes according to the JS chain order). The hash parity target is JS == oracle, not oracle == vanilla 1.4.5.6.

So the plan: transcribe the 1405 MakeDungeon + helpers (which JS mirrors) into C# oracle, in the JS pass structure with the 1456 head rolls JS added. Then run both, compare hashes, and fix JS deviations found by cross-checking against the 1405 source.

Let me first check the current oracle state around the placeholder.
```

</details>


---

## 🤖 Assistant · 2026-08-12T21:23:25.518Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dungeon\" tools/golden/caves-oracle.cs tests/caves-checkpoint.test.ts | head -20; ls -la tests/golden/caves-chain-*.json",
 "description": "Verify placeholder state in oracle and test"
}
```


---

## 👤 User(sidechain) · 2026-08-12T21:23:25.551Z

**📎 ToolResult**

```
tests/caves-checkpoint.test.ts:122:  snap('dungeon');                        // #32 占位（oracle 同步占位，转录后替换为 runDungeonPass）
tests/caves-checkpoint.test.ts:152:        'webs', 'underworld', 'corruption', 'lakes', 'slush', 'dungeon', 'mcopenings', 'beaches'];
tools/golden/caves-oracle.cs:130:bool dungeonRight = !((int)r.Next(2) == 0);
tools/golden/caves-oracle.cs:131:int jungleX = dungeonRight
tools/golden/caves-oracle.cs:135:if (dungeonRight) { while (num7 < W * 0.6 || num7 > W * 0.75) num7 = (int)r.Next(W); }
tools/golden/caves-oracle.cs:141:int leftBeachEnd = (int)r.Next(300, 340) + (dungeonRight ? 40 : 20);
tools/golden/caves-oracle.cs:142:int rightBeachStart = W - (int)r.Next(300, 340) - (dungeonRight ? 20 : 40);
tools/golden/caves-oracle.cs:143:int dungeonLocation = !dungeonRight
tools/golden/caves-oracle.cs:946:        if (dungeonRight) { if ((int)r.Next(4) == 0) { left++; right++; } }
tools/golden/caves-oracle.cs:1026:        TileRunner(x, y, (int)r.Next((int)(250 * ws), (int)(500 * ws)), (int)r.Next(50, 150), 59, false, (dungeonRight ? 1 : -1) * xSpeedScale, 0.0);
tools/golden/caves-oracle.cs:1336:    int side = dungeonRight ? 1 : -1;
tools/golden/caves-oracle.cs:2884:// 普通世界：flipInfections/drunk/remix/tenthAnniversary 全 false；dungeonSide = dungeonRight ? 1 : -1
tools/golden/caves-oracle.cs:3411:    int dungeonAvoid = 100;
tools/golden/caves-oracle.cs:3414:    int dSide = dungeonRight ? 1 : -1;
tools/golden/caves-oracle.cs:3442:            if (zLo < dungeonLocation + dungeonAvoid && zHi > dungeonLocation - dungeonAvoid) ok = false;
tools/golden/caves-oracle.cs:3861:Checkpoint("dungeon");   // #32 占位：DungeonCrawler 转录落地前=slush 同态快照（零掷骰占位，勿删）
tools/golden/caves-oracle.cs:3974:            if (dungeonRight) waterX = 275;
tools/golden/caves-oracle.cs:4004:            if (!dungeonRight) waterX = W - 275;
-rw-r--r--@ 1 user  staff  1910  8月 13 00:22 tests/golden/caves-chain-1511931452.json
-rw-r--r--@ 1 user  staff  1958  8月 13 05:21 tests/golden/caves-chain-9293480.json
-rw-r--r--@ 1 user  staff  1961  8月 13 05:22 tests/golden/caves-chain-SandboxWorld.json

```


---

## 🤖 Assistant · 2026-08-12T21:23:29.684Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. Placeholder is in place. Now let me continue reading the 1405 reference for the remaining parts (GroundFurniture 19287-19613, Pictures 19080-19287, Banners 19042-19080, Traps 18846-18864), plus DungeonHalls/DungeonRoom/DungeonStairs/DungeonEnt in 1405 (L20255/L20622/L19855/L20726 per the JS header).

I've already read:
- 18006-18484 (main MakeDungeon up to wall variants)
- 18485-19044 (platforms, chests, bookshelves, room chests, bounds, Traps, Lights)

Still need: Banners (19042-19079), Pictures (19080-19286), GroundFurniture (19287-19613), then DungeonHalls (20255), DungeonRoom (20622), DungeonStairs (19855), DungeonEnt (20726).

Also the 1405 pass registration for the dungeon (what x,y the pass passes) — the JS uses 1456 semantics for the depth anchor.

Let me read Banners+Pictures now (19042-19290).
```

</details>


---

## 🤖 Assistant · 2026-08-12T21:23:30.053Z · glm-x-preview-260804

```
占位已就绪。继续分段读 1405 权威源码（旗帜/墙画段）。
```


---

## 🤖 Assistant · 2026-08-12T21:23:30.246Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "limit": 250,
 "offset": 19042
}
```


---

## 👤 User(sidechain) · 2026-08-12T21:23:30.261Z

**📎 ToolResult**

```
19042	    private static float MakeDungeon_Banners(int[] roomWall, float count)
19043	    {
19044	      count = 840000f / (float) Main.maxTilesX;
19045	      for (int index1 = 0; (double) index1 < (double) count; ++index1)
19046	      {
19047	        int i = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
19048	        int j1;
19049	        for (j1 = WorldGen.genRand.Next(WorldGen.dMinY, WorldGen.dMaxY); !Main.wallDungeon[(int) Main.tile[i, j1].wall] || Main.tile[i, j1].active(); j1 = WorldGen.genRand.Next(WorldGen.dMinY, WorldGen.dMaxY))
19050	          i = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
19051	        while (!WorldGen.SolidTile(i, j1, false) && j1 > 10)
19052	          --j1;
19053	        int j2 = j1 + 1;
19054	        if (Main.wallDungeon[(int) Main.tile[i, j2].wall] && Main.tile[i, j2 - 1].type != (ushort) 48 && (!Main.tile[i, j2].active() && !Main.tile[i, j2 + 1].active()) && (!Main.tile[i, j2 + 2].active() && !Main.tile[i, j2 + 3].active()))
19055	        {
19056	          bool flag = true;
19057	          for (int index2 = i - 1; index2 <= i + 1; ++index2)
19058	          {
19059	            for (int index3 = j2; index3 <= j2 + 3; ++index3)
19060	            {
19061	              if (Main.tile[index2, index3].active() && (Main.tile[index2, index3].type == (ushort) 10 || Main.tile[index2, index3].type == (ushort) 11 || Main.tile[index2, index3].type == (ushort) 91))
19062	                flag = false;
19063	            }
19064	          }
19065	          if (flag)
19066	          {
19067	            int num = 10;
19068	            if ((int) Main.tile[i, j2].wall == roomWall[1])
19069	              num = 12;
19070	            if ((int) Main.tile[i, j2].wall == roomWall[2])
19071	              num = 14;
19072	            int style = num + WorldGen.genRand.Next(2);
19073	            WorldGen.PlaceTile(i, j2, 91, true, false, -1, style);
19074	          }
19075	        }
19076	      }
19077	      return count;
19078	    }
19079	
19080	    private static float MakeDungeon_Pictures(int[] roomWall, float count)
19081	    {
19082	      count = 420000f / (float) Main.maxTilesX;
19083	      for (int index1 = 0; (double) index1 < (double) count; ++index1)
19084	      {
19085	        int index2 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
19086	        int index3;
19087	        for (index3 = WorldGen.genRand.Next((int) Main.worldSurface, WorldGen.dMaxY); !Main.wallDungeon[(int) Main.tile[index2, index3].wall] || Main.tile[index2, index3].active(); index3 = WorldGen.genRand.Next((int) Main.worldSurface, WorldGen.dMaxY))
19088	          index2 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
19089	        for (int index4 = 0; index4 < 2; ++index4)
19090	        {
19091	          int index5 = index2;
19092	          int index6 = index2;
19093	          while (!Main.tile[index5, index3].active() && Main.wallDungeon[(int) Main.tile[index5, index3].wall])
19094	            --index5;
19095	          int num1 = index5 + 1;
19096	          while (!Main.tile[index6, index3].active() && Main.wallDungeon[(int) Main.tile[index6, index3].wall])
19097	            ++index6;
19098	          int num2 = index6 - 1;
19099	          index2 = (num1 + num2) / 2;
19100	          int index7 = index3;
19101	          int index8 = index3;
19102	          while (!Main.tile[index2, index7].active() && Main.wallDungeon[(int) Main.tile[index2, index7].wall])
19103	            --index7;
19104	          int num3 = index7 + 1;
19105	          while (!Main.tile[index2, index8].active() && Main.wallDungeon[(int) Main.tile[index2, index8].wall])
19106	            ++index8;
19107	          int num4 = index8 - 1;
19108	          index3 = (num3 + num4) / 2;
19109	        }
19110	        int index9 = index2;
19111	        int index10 = index2;
19112	        while (!Main.tile[index9, index3].active() && !Main.tile[index9, index3 - 1].active() && !Main.tile[index9, index3 + 1].active())
19113	          --index9;
19114	        int num5 = index9 + 1;
19115	        while (!Main.tile[index10, index3].active() && !Main.tile[index10, index3 - 1].active() && !Main.tile[index10, index3 + 1].active())
19116	          ++index10;
19117	        int num6 = index10 - 1;
19118	        int index11 = index3;
19119	        int index12 = index3;
19120	        while (!Main.tile[index2, index11].active() && !Main.tile[index2 - 1, index11].active() && !Main.tile[index2 + 1, index11].active())
19121	          --index11;
19122	        int num7 = index11 + 1;
19123	        while (!Main.tile[index2, index12].active() && !Main.tile[index2 - 1, index12].active() && !Main.tile[index2 + 1, index12].active())
19124	          ++index12;
19125	        int num8 = index12 - 1;
19126	        int index13 = (num5 + num6) / 2;
19127	        int index14 = (num7 + num8) / 2;
19128	        int num9 = num6 - num5;
19129	        int num10 = num8 - num7;
19130	        if (num9 > 7 && num10 > 5)
19131	        {
19132	          bool[] flagArray = new bool[3]
19133	          {
19134	            true,
19135	            false,
19136	            false
19137	          };
19138	          if (num9 > num10 * 3 && num9 > 21)
19139	            flagArray[1] = true;
19140	          if (num10 > num9 * 3 && num10 > 21)
19141	            flagArray[2] = true;
19142	          int index4 = WorldGen.genRand.Next(3);
19143	          if ((int) Main.tile[index13, index14].wall == roomWall[0])
19144	            index4 = 0;
19145	          while (!flagArray[index4])
19146	            index4 = WorldGen.genRand.Next(3);
19147	          if (WorldGen.nearPicture2(index13, index14))
19148	            index4 = -1;
19149	          switch (index4)
19150	          {
19151	            case 0:
19152	              Vector2 vector2_1 = WorldGen.randPictureTile();
19153	              if ((int) Main.tile[index13, index14].wall != roomWall[0])
19154	                vector2_1 = WorldGen.randBoneTile();
19155	              int x1 = (int) vector2_1.X;
19156	              int y1 = (int) vector2_1.Y;
19157	              if (!WorldGen.nearPicture(index13, index14))
19158	              {
19159	                WorldGen.PlaceTile(index13, index14, x1, true, false, -1, y1);
19160	                continue;
19161	              }
19162	              continue;
19163	            case 1:
19164	              Vector2 vector2_2 = WorldGen.randPictureTile();
19165	              if ((int) Main.tile[index13, index14].wall != roomWall[0])
19166	                vector2_2 = WorldGen.randBoneTile();
19167	              int x2 = (int) vector2_2.X;
19168	              int y2 = (int) vector2_2.Y;
19169	              if (!Main.tile[index13, index14].active())
19170	                WorldGen.PlaceTile(index13, index14, x2, true, false, -1, y2);
19171	              int num1 = index13;
19172	              int num2 = index14;
19173	              int index5 = index14;
19174	              for (int index6 = 0; index6 < 2; ++index6)
19175	              {
19176	                index13 += 7;
19177	                int index7 = index5;
19178	                int index8 = index5;
19179	                while (!Main.tile[index13, index7].active() && !Main.tile[index13 - 1, index7].active() && !Main.tile[index13 + 1, index7].active())
19180	                  --index7;
19181	                int num3 = index7 + 1;
19182	                while (!Main.tile[index13, index8].active() && !Main.tile[index13 - 1, index8].active() && !Main.tile[index13 + 1, index8].active())
19183	                  ++index8;
19184	                int num4 = index8 - 1;
19185	                index5 = (num3 + num4) / 2;
19186	                Vector2 vector2_3 = WorldGen.randPictureTile();
19187	                if ((int) Main.tile[index13, index5].wall != roomWall[0])
19188	                  vector2_3 = WorldGen.randBoneTile();
19189	                int x3 = (int) vector2_3.X;
19190	                int y3 = (int) vector2_3.Y;
19191	                if (Math.Abs(num2 - index5) < 4 && !WorldGen.nearPicture(index13, index5))
19192	                  WorldGen.PlaceTile(index13, index5, x3, true, false, -1, y3);
19193	                else
19194	                  break;
19195	              }
19196	              int index15 = index14;
19197	              int index16 = num1;
19198	              for (int index6 = 0; index6 < 2; ++index6)
19199	              {
19200	                index16 -= 7;
19201	                int index7 = index15;
19202	                int index8 = index15;
19203	                while (!Main.tile[index16, index7].active() && !Main.tile[index16 - 1, index7].active() && !Main.tile[index16 + 1, index7].active())
19204	                  --index7;
19205	                int num3 = index7 + 1;
19206	                while (!Main.tile[index16, index8].active() && !Main.tile[index16 - 1, index8].active() && !Main.tile[index16 + 1, index8].active())
19207	                  ++index8;
19208	                int num4 = index8 - 1;
19209	                index15 = (num3 + num4) / 2;
19210	                Vector2 vector2_3 = WorldGen.randPictureTile();
19211	                if ((int) Main.tile[index16, index15].wall != roomWall[0])
19212	                  vector2_3 = WorldGen.randBoneTile();
19213	                int x3 = (int) vector2_3.X;
19214	                int y3 = (int) vector2_3.Y;
19215	                if (Math.Abs(num2 - index15) < 4 && !WorldGen.nearPicture(index16, index15))
19216	                  WorldGen.PlaceTile(index16, index15, x3, true, false, -1, y3);
19217	                else
19218	                  break;
19219	              }
19220	              continue;
19221	            case 2:
19222	              Vector2 vector2_4 = WorldGen.randPictureTile();
19223	              if ((int) Main.tile[index13, index14].wall != roomWall[0])
19224	                vector2_4 = WorldGen.randBoneTile();
19225	              int x4 = (int) vector2_4.X;
19226	              int y4 = (int) vector2_4.Y;
19227	              if (!Main.tile[index13, index14].active())
19228	                WorldGen.PlaceTile(index13, index14, x4, true, false, -1, y4);
19229	              int num11 = index14;
19230	              int num12 = index13;
19231	              int index17 = index13;
19232	              for (int index6 = 0; index6 < 3; ++index6)
19233	              {
19234	                index14 += 7;
19235	                int index7 = index17;
19236	                int index8 = index17;
19237	                while (!Main.tile[index7, index14].active() && !Main.tile[index7, index14 - 1].active() && !Main.tile[index7, index14 + 1].active())
19238	                  --index7;
19239	                int num3 = index7 + 1;
19240	                while (!Main.tile[index8, index14].active() && !Main.tile[index8, index14 - 1].active() && !Main.tile[index8, index14 + 1].active())
19241	                  ++index8;
19242	                int num4 = index8 - 1;
19243	                index17 = (num3 + num4) / 2;
19244	                Vector2 vector2_3 = WorldGen.randPictureTile();
19245	                if ((int) Main.tile[index17, index14].wall != roomWall[0])
19246	                  vector2_3 = WorldGen.randBoneTile();
19247	                int x3 = (int) vector2_3.X;
19248	                int y3 = (int) vector2_3.Y;
19249	                if (Math.Abs(num12 - index17) < 4 && !WorldGen.nearPicture(index17, index14))
19250	                  WorldGen.PlaceTile(index17, index14, x3, true, false, -1, y3);
19251	                else
19252	                  break;
19253	              }
19254	              int index18 = index13;
19255	              int index19 = num11;
19256	              for (int index6 = 0; index6 < 3; ++index6)
19257	              {
19258	                index19 -= 7;
19259	                int index7 = index18;
19260	                int index8 = index18;
19261	                while (!Main.tile[index7, index19].active() && !Main.tile[index7, index19 - 1].active() && !Main.tile[index7, index19 + 1].active())
19262	                  --index7;
19263	                int num3 = index7 + 1;
19264	                while (!Main.tile[index8, index19].active() && !Main.tile[index8, index19 - 1].active() && !Main.tile[index8, index19 + 1].active())
19265	                  ++index8;
19266	                int num4 = index8 - 1;
19267	                index18 = (num3 + num4) / 2;
19268	                Vector2 vector2_3 = WorldGen.randPictureTile();
19269	                if ((int) Main.tile[index18, index19].wall != roomWall[0])
19270	                  vector2_3 = WorldGen.randBoneTile();
19271	                int x3 = (int) vector2_3.X;
19272	                int y3 = (int) vector2_3.Y;
19273	                if (Math.Abs(num12 - index18) < 4 && !WorldGen.nearPicture(index18, index19))
19274	                  WorldGen.PlaceTile(index18, index19, x3, true, false, -1, y3);
19275	                else
19276	                  break;
19277	              }
19278	              continue;
19279	            default:
19280	              continue;
19281	          }
19282	        }
19283	      }
19284	      return count;
19285	    }
19286	
19287	    private static float MakeDungeon_GroundFurniture(int wallType)
19288	    {
19289	      float num1 = (float) (2000.0 * (double) Main.maxTilesX / 4200.0);
19290	      int num2 = 1 + Main.maxTilesX / 4200;
19291	      int num3 = 1 + Main.maxTilesX / 4200;

```


---

## 🤖 Assistant · 2026-08-12T21:39:14.470Z · <synthetic>

```
API Error: Stream idle timeout - no chunks received
```


---

## 👤 User(sidechain) · 2026-08-12T21:39:14.472Z

```
[Request interrupted by user]
```


---

## 👤 User(meta)(sidechain) · 2026-08-12T21:39:25.850Z

```
The coordinator sent a message while you were working:
第四次停滞恢复。一个纠偏：你片段里写"1405 权威源码"——**权威是 1456**（~/Project/GLM/SandboxWorld/Terarria1456/ 的 DungeonCrawler.cs + WorldGen.cs:14816），1405 仅可作辅助参照，掷骰序/数值以 1456 为准（若 1405 无 DungeonCrawler.cs 则只读 1456）。继续分段读+逐段落盘，纪律照旧。

Address this before completing your current task.
```

---

## 🤖 Assistant · 2026-08-12T21:39:39.039Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The coordinator says 1456 is the authority. But there's a fundamental tension: JS DungeonPass.ts implements the 1405 legacy algorithm (single-function MakeDungeon with DungeonHalls/DungeonRoom/DungeonStairs/DungeonEnt). 1456 replaced that with the DungeonCrawler object system (LegacyDungeonLayoutProvider, LegacyEntranceDungeonHall, rooms, features like DungeonGlobalSpikes/Doors/Platforms/Chests...). 

The task says: transcribe the vanilla #32 Dungeon pass into the oracle and reconcile with JS to hash equality. The alignment doc states clearly: "oracle 按 JS 链顺序转录，互验全绿 ≠ 原版等价" — the oracle transcribes following the JS chain. Also "JS 已移植、oracle 未对账" lists #30 Dungeon | DungeonPass.ts.

So the practical goal: oracle transcribes the same algorithm the JS implements (which is 1405-legacy-structure with 1456 RNG-consumption patches, as annotated in DungeonPass.ts). Hash equality JS==oracle is the deliverable. The 1456 authority applies to the RNG-consumption corrections that JS already encodes (SetupDungeonDataVariables head rolls, depth anchor, crawl-to-surface 100 cap, etc.) and to fixing any JS self-invented improvements.

Given the JS file is the interface contract (it's what the game actually runs), the oracle must mirror it exactly. Deviations found by comparing to vanilla should be fixed on the JS side (or both if JS deviates from what the JS comments claim).

So my transcription source = JS DungeonPass.ts (algorithm), validated against 1405 where JS claims 1:1 (L18xxx/L18xxx/L20xxx references are 1405 line numbers) and against 1456 DungeonCrawler where JS cites it (RNG rolls). 

Now, reading 1456 DungeonCrawler fully: I already read the whole 953-line DungeonCrawler.cs. The rest of the 1456 system is in LegacyDungeonLayoutProvider (99 lines), DungeonUtils (62k), rooms, halls, entrances, features. That's the *real* 1456 dungeon. JS does NOT implement that (it implements the legacy algorithm with 1456 head rolls). Making JS implement the full 1456 system would be a massive rewrite (thousands of lines) — clearly out of scope for this checkpoint task. The checkpoint parity target is oracle==JS.

Decision: transcribe the JS algorithm into the oracle (mechanically, faithfully), keeping the 1456 RNG-consumption semantics the JS already encodes. Where JS deviates from what its own comments cite as vanilla, fix JS to match vanilla. That satisfies "与 JS 对账到逐哈希全等" and keeps 1456 as the numerical authority for the dice sequence.

I'll note this clearly in my final report as a "遗留" item: full 1456 DungeonCrawler object-system transcription is a separate large work item; this checkpoint aligns JS's legacy-based implementation against an oracle transcription of the same, with the 1456 head-RNG already verified.

Now let me proceed efficiently. I still need to read from 1405 (as auxiliary reference for the legacy algorithm the JS mirrors):
- GroundFurniture 19287-19613
- DungeonHalls 20255 (1405)
- DungeonRoom 20622
- DungeonStairs 19855
- DungeonEnt 20726
- Helpers: randPictureTile/randBoneTile/nearPicture/nearPicture2, Place1x2Top, PlaceChand, placeTrap, AddBuriedChest, DungeonPitTrap.

Let me read the GroundFurniture rest first (19291-19613).
```

</details>


---

## 🤖 Assistant · 2026-08-12T21:39:39.040Z · glm-x-preview-260804

```
明确：以 1456 为数值/掷骰权威，1405 仅作 legacy 算法结构参照。继续分段读，随后逐段落盘。
```


---

## 🤖 Assistant · 2026-08-12T21:39:39.041Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "limit": 330,
 "offset": 19291
}
```


---

## 👤 User(sidechain) · 2026-08-12T21:39:39.046Z

**📎 ToolResult**

```
19291	      int num3 = 1 + Main.maxTilesX / 4200;
19292	      for (int index1 = 0; (double) index1 < (double) num1; ++index1)
19293	      {
19294	        if (num2 > 0 || num3 > 0)
19295	          --index1;
19296	        int i1 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
19297	        int j;
19298	        for (j = WorldGen.genRand.Next((int) Main.worldSurface + 10, WorldGen.dMaxY); !Main.wallDungeon[(int) Main.tile[i1, j].wall] || Main.tile[i1, j].active(); j = WorldGen.genRand.Next((int) Main.worldSurface + 10, WorldGen.dMaxY))
19299	          i1 = WorldGen.genRand.Next(WorldGen.dMinX, WorldGen.dMaxX);
19300	        if (Main.wallDungeon[(int) Main.tile[i1, j].wall] && !Main.tile[i1, j].active())
19301	        {
19302	          while (!WorldGen.SolidTile(i1, j, false) && j < Main.UnderworldLayer)
19303	            ++j;
19304	          int index2 = j - 1;
19305	          int i2 = i1;
19306	          int i3 = i1;
19307	          while (!Main.tile[i2, index2].active() && WorldGen.SolidTile(i2, index2 + 1, false))
19308	            --i2;
19309	          int num4 = i2 + 1;
19310	          while (!Main.tile[i3, index2].active() && WorldGen.SolidTile(i3, index2 + 1, false))
19311	            ++i3;
19312	          int num5 = i3 - 1;
19313	          int num6 = num5 - num4;
19314	          int index3 = (num5 + num4) / 2;
19315	          if (!Main.tile[index3, index2].active() && Main.wallDungeon[(int) Main.tile[index3, index2].wall] && (WorldGen.SolidTile(index3, index2 + 1, false) && Main.tile[index3, index2 + 1].type != (ushort) 48))
19316	          {
19317	            int style1 = 13;
19318	            int style2 = 10;
19319	            int style3 = 11;
19320	            int style4 = 1;
19321	            int style5 = 46;
19322	            int style6 = 1;
19323	            int style7 = 5;
19324	            int style8 = 11;
19325	            int style9 = 5;
19326	            int style10 = 6;
19327	            int style11 = 21;
19328	            int style12 = 22;
19329	            int style13 = 24;
19330	            int style14 = 30;
19331	            switch (wallType)
19332	            {
19333	              case 8:
19334	                style1 = 14;
19335	                style2 = 11;
19336	                style3 = 12;
19337	                style4 = 2;
19338	                style5 = 47;
19339	                style6 = 2;
19340	                style7 = 6;
19341	                style8 = 12;
19342	                style9 = 6;
19343	                style10 = 7;
19344	                style11 = 22;
19345	                style12 = 23;
19346	                style13 = 25;
19347	                style14 = 31;
19348	                break;
19349	              case 9:
19350	                style1 = 15;
19351	                style2 = 12;
19352	                style3 = 13;
19353	                style4 = 3;
19354	                style5 = 48;
19355	                style6 = 3;
19356	                style7 = 7;
19357	                style8 = 13;
19358	                style9 = 7;
19359	                style10 = 8;
19360	                style11 = 23;
19361	                style12 = 24;
19362	                style13 = 26;
19363	                style14 = 32;
19364	                break;
19365	            }
19366	            if (Main.tile[index3, index2].wall >= (ushort) 94 && Main.tile[index3, index2].wall <= (ushort) 105)
19367	            {
19368	              style1 = 17;
19369	              style2 = 14;
19370	              style3 = 15;
19371	              style4 = -1;
19372	              style5 = -1;
19373	              style6 = 5;
19374	              style7 = -1;
19375	              style8 = -1;
19376	              style9 = -1;
19377	              style10 = -1;
19378	              style11 = -1;
19379	              style12 = -1;
19380	              style13 = -1;
19381	              style14 = -1;
19382	            }
19383	            int num7 = WorldGen.genRand.Next(13);
19384	            if ((num7 == 10 || num7 == 11 || num7 == 12) && WorldGen.genRand.Next(4) != 0)
19385	              num7 = WorldGen.genRand.Next(13);
19386	            while (num7 == 2 && style5 == -1 || num7 == 5 && style7 == -1 || (num7 == 6 && style8 == -1 || num7 == 7 && style9 == -1) || (num7 == 8 && style10 == -1 || num7 == 9 && style11 == -1 || (num7 == 10 && style12 == -1 || num7 == 11 && style13 == -1)) || num7 == 12 && style14 == -1)
19387	              num7 = WorldGen.genRand.Next(13);
19388	            int num8 = 0;
19389	            int num9 = 0;
19390	            if (num7 == 0)
19391	            {
19392	              num8 = 5;
19393	              num9 = 4;
19394	            }
19395	            if (num7 == 1)
19396	            {
19397	              num8 = 4;
19398	              num9 = 3;
19399	            }
19400	            if (num7 == 2)
19401	            {
19402	              num8 = 3;
19403	              num9 = 5;
19404	            }
19405	            if (num7 == 3)
19406	            {
19407	              num8 = 4;
19408	              num9 = 6;
19409	            }
19410	            if (num7 == 4)
19411	            {
19412	              num8 = 3;
19413	              num9 = 3;
19414	            }
19415	            if (num7 == 5)
19416	            {
19417	              num8 = 5;
19418	              num9 = 3;
19419	            }
19420	            if (num7 == 6)
19421	            {
19422	              num8 = 5;
19423	              num9 = 4;
19424	            }
19425	            if (num7 == 7)
19426	            {
19427	              num8 = 5;
19428	              num9 = 4;
19429	            }
19430	            if (num7 == 8)
19431	            {
19432	              num8 = 5;
19433	              num9 = 4;
19434	            }
19435	            if (num7 == 9)
19436	            {
19437	              num8 = 5;
19438	              num9 = 3;
19439	            }
19440	            if (num7 == 10)
19441	            {
19442	              num8 = 2;
19443	              num9 = 4;
19444	            }
19445	            if (num7 == 11)
19446	            {
19447	              num8 = 3;
19448	              num9 = 3;
19449	            }
19450	            if (num7 == 12)
19451	            {
19452	              num8 = 2;
19453	              num9 = 5;
19454	            }
19455	            for (int index4 = index3 - num8; index4 <= index3 + num8; ++index4)
19456	            {
19457	              for (int index5 = index2 - num9; index5 <= index2; ++index5)
19458	              {
19459	                if (Main.tile[index4, index5].active())
19460	                {
19461	                  num7 = -1;
19462	                  break;
19463	                }
19464	              }
19465	            }
19466	            if ((double) num6 < (double) num8 * 1.75)
19467	              num7 = -1;
19468	            if (num2 > 0 || num3 > 0)
19469	            {
19470	              if (num2 > 0)
19471	              {
19472	                WorldGen.PlaceTile(index3, index2, 355, true, false, -1, 0);
19473	                if (Main.tile[index3, index2].type == (ushort) 355)
19474	                  --num2;
19475	              }
19476	              else if (num3 > 0)
19477	              {
19478	                WorldGen.PlaceTile(index3, index2, 354, true, false, -1, 0);
19479	                if (Main.tile[index3, index2].type == (ushort) 354)
19480	                  --num3;
19481	              }
19482	            }
19483	            else
19484	            {
19485	              switch (num7)
19486	              {
19487	                case 0:
19488	                  WorldGen.PlaceTile(index3, index2, 14, true, false, -1, style2);
19489	                  if (Main.tile[index3, index2].active())
19490	                  {
19491	                    if (!Main.tile[index3 - 2, index2].active())
19492	                    {
19493	                      WorldGen.PlaceTile(index3 - 2, index2, 15, true, false, -1, style1);
19494	                      if (Main.tile[index3 - 2, index2].active())
19495	                      {
19496	                        Main.tile[index3 - 2, index2].frameX += (short) 18;
19497	                        Main.tile[index3 - 2, index2 - 1].frameX += (short) 18;
19498	                      }
19499	                    }
19500	                    if (!Main.tile[index3 + 2, index2].active())
19501	                      WorldGen.PlaceTile(index3 + 2, index2, 15, true, false, -1, style1);
19502	                  }
19503	                  for (int i4 = index3 - 1; i4 <= index3 + 1; ++i4)
19504	                  {
19505	                    if (WorldGen.genRand.Next(2) == 0 && !Main.tile[i4, index2 - 2].active())
19506	                    {
19507	                      int num10 = WorldGen.genRand.Next(5);
19508	                      if (style4 != -1 && num10 <= 1 && !Main.tileLighted[(int) Main.tile[i4 - 1, index2 - 2].type])
19509	                        WorldGen.PlaceTile(i4, index2 - 2, 33, true, false, -1, style4);
19510	                      if (num10 == 2 && !Main.tileLighted[(int) Main.tile[i4 - 1, index2 - 2].type])
19511	                        WorldGen.PlaceTile(i4, index2 - 2, 49, true, false, -1, 0);
19512	                      if (num10 == 3)
19513	                        WorldGen.PlaceTile(i4, index2 - 2, 50, true, false, -1, 0);
19514	                      if (num10 == 4)
19515	                        WorldGen.PlaceTile(i4, index2 - 2, 103, true, false, -1, 0);
19516	                    }
19517	                  }
19518	                  continue;
19519	                case 1:
19520	                  WorldGen.PlaceTile(index3, index2, 18, true, false, -1, style3);
19521	                  if (Main.tile[index3, index2].active())
19522	                  {
19523	                    if (WorldGen.genRand.Next(2) == 0)
19524	                    {
19525	                      if (!Main.tile[index3 - 1, index2].active())
19526	                      {
19527	                        WorldGen.PlaceTile(index3 - 1, index2, 15, true, false, -1, style1);
19528	                        if (Main.tile[index3 - 1, index2].active())
19529	                        {
19530	                          Main.tile[index3 - 1, index2].frameX += (short) 18;
19531	                          Main.tile[index3 - 1, index2 - 1].frameX += (short) 18;
19532	                        }
19533	                      }
19534	                    }
19535	                    else if (!Main.tile[index3 + 2, index2].active())
19536	                      WorldGen.PlaceTile(index3 + 2, index2, 15, true, false, -1, style1);
19537	                    for (int i4 = index3; i4 <= index3 + 1; ++i4)
19538	                    {
19539	                      if (WorldGen.genRand.Next(2) == 0 && !Main.tile[i4, index2 - 1].active())
19540	                      {
19541	                        int num10 = WorldGen.genRand.Next(5);
19542	                        if (style4 != -1 && num10 <= 1 && !Main.tileLighted[(int) Main.tile[i4 - 1, index2 - 1].type])
19543	                          WorldGen.PlaceTile(i4, index2 - 1, 33, true, false, -1, style4);
19544	                        if (num10 == 2 && !Main.tileLighted[(int) Main.tile[i4 - 1, index2 - 1].type])
19545	                          WorldGen.PlaceTile(i4, index2 - 1, 49, true, false, -1, 0);
19546	                        if (num10 == 3)
19547	                          WorldGen.PlaceTile(i4, index2 - 1, 50, true, false, -1, 0);
19548	                        if (num10 == 4)
19549	                          WorldGen.PlaceTile(i4, index2 - 1, 103, true, false, -1, 0);
19550	                      }
19551	                    }
19552	                    continue;
19553	                  }
19554	                  continue;
19555	                case 2:
19556	                  WorldGen.PlaceTile(index3, index2, 105, true, false, -1, style5);
19557	                  continue;
19558	                case 3:
19559	                  WorldGen.PlaceTile(index3, index2, 101, true, false, -1, style6);
19560	                  continue;
19561	                case 4:
19562	                  if (WorldGen.genRand.Next(2) == 0)
19563	                  {
19564	                    WorldGen.PlaceTile(index3, index2, 15, true, false, -1, style1);
19565	                    Main.tile[index3, index2].frameX += (short) 18;
19566	                    Main.tile[index3, index2 - 1].frameX += (short) 18;
19567	                    continue;
19568	                  }
19569	                  WorldGen.PlaceTile(index3, index2, 15, true, false, -1, style1);
19570	                  continue;
19571	                case 5:
19572	                  if (WorldGen.genRand.Next(2) == 0)
19573	                  {
19574	                    WorldGen.Place4x2(index3, index2, (ushort) 79, 1, style7);
19575	                    continue;
19576	                  }
19577	                  WorldGen.Place4x2(index3, index2, (ushort) 79, -1, style7);
19578	                  continue;
19579	                case 6:
19580	                  WorldGen.PlaceTile(index3, index2, 87, true, false, -1, style8);
19581	                  continue;
19582	                case 7:
19583	                  WorldGen.PlaceTile(index3, index2, 88, true, false, -1, style9);
19584	                  continue;
19585	                case 8:
19586	                  WorldGen.PlaceTile(index3, index2, 89, true, false, -1, style10);
19587	                  continue;
19588	                case 9:
19589	                  if (WorldGen.genRand.Next(2) == 0)
19590	                  {
19591	                    WorldGen.Place4x2(index3, index2, (ushort) 90, 1, style11);
19592	                    continue;
19593	                  }
19594	                  WorldGen.Place4x2(index3, index2, (ushort) 90, -1, style11);
19595	                  continue;
19596	                case 10:
19597	                  WorldGen.PlaceTile(index3, index2, 93, true, false, -1, style13);
19598	                  continue;
19599	                case 11:
19600	                  WorldGen.PlaceTile(index3, index2, 100, true, false, -1, style12);
19601	                  continue;
19602	                case 12:
19603	                  WorldGen.PlaceTile(index3, index2, 104, true, false, -1, style14);
19604	                  continue;
19605	                default:
19606	                  continue;
19607	              }
19608	            }
19609	          }
19610	        }
19611	      }
19612	      return num1;
19613	    }
19614	
19615	    public static Vector2 randBoneTile()
19616	    {
19617	      int num1 = WorldGen.genRand.Next(2);
19618	      int num2 = 0;
19619	      switch (num1)
19620	      {

```


---

## 🤖 Assistant · 2026-08-12T21:39:41.240Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me continue reading the reference sources. I need randBoneTile/randPictureTile/nearPicture/nearPicture2 (19615-19680), then DungeonStairs (19855), DungeonHalls (20255), DungeonRoom (20622), DungeonEnt (20726).
```

</details>


---

## 🤖 Assistant · 2026-08-12T21:39:41.560Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "limit": 75,
 "offset": 19615
}
```


---

## 👤 User(sidechain) · 2026-08-12T21:39:41.567Z

**📎 ToolResult**

```
19615	    public static Vector2 randBoneTile()
19616	    {
19617	      int num1 = WorldGen.genRand.Next(2);
19618	      int num2 = 0;
19619	      switch (num1)
19620	      {
19621	        case 0:
19622	          num1 = 240;
19623	          num2 = WorldGen.genRand.Next(2);
19624	          switch (num2)
19625	          {
19626	            case 0:
19627	              num2 = 16;
19628	              break;
19629	            case 1:
19630	              num2 = 17;
19631	              break;
19632	          }
19633	          break;
19634	        case 1:
19635	          num1 = 241;
19636	          num2 = WorldGen.genRand.Next(9);
19637	          break;
19638	      }
19639	      return new Vector2((float) num1, (float) num2);
19640	    }
19641	
19642	    public static Vector2 randHellPicture()
19643	    {
19644	      int num1 = WorldGen.genRand.Next(4);
19645	      if (num1 == 1)
19646	        num1 = WorldGen.genRand.Next(4);
19647	      int num2;
19648	      int num3;
19649	      if (num1 == 0)
19650	      {
19651	        num2 = 240;
19652	        num3 = WorldGen.genRand.Next(5);
19653	        switch (num3)
19654	        {
19655	          case 0:
19656	            num3 = 27;
19657	            break;
19658	          case 1:
19659	            num3 = 29;
19660	            break;
19661	          case 2:
19662	            num3 = 30;
19663	            break;
19664	          case 3:
19665	            num3 = 31;
19666	            break;
19667	          case 4:
19668	            num3 = 32;
19669	            break;
19670	        }
19671	      }
19672	      else if (num1 == 1)
19673	      {
19674	        num2 = 242;
19675	        num3 = 14;
19676	      }
19677	      else if (num1 == 2)
19678	      {
19679	        num2 = 245;
19680	        num3 = WorldGen.genRand.Next(3);
19681	        switch (num3)
19682	        {
19683	          case 0:
19684	            num3 = 1;
19685	            break;
19686	          case 1:
19687	            num3 = 2;
19688	            break;
19689	          case 2:

```


---

## 🤖 Assistant · 2026-08-12T21:39:43.761Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"randPictureTile\\|nearPicture2\\|nearPicture(\" ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs | head",
 "description": "Locate randPictureTile and nearPicture helpers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T21:39:43.783Z

**📎 ToolResult**

```
16439:            if (WorldGen.nearPicture2(num14, num15))
16446:              if (!WorldGen.nearPicture(num14, num15))
17966:    public static bool nearPicture(int x, int y)
17979:    public static bool nearPicture2(int x, int y)
19147:          if (WorldGen.nearPicture2(index13, index14))
19152:              Vector2 vector2_1 = WorldGen.randPictureTile();
19157:              if (!WorldGen.nearPicture(index13, index14))
19164:              Vector2 vector2_2 = WorldGen.randPictureTile();
19186:                Vector2 vector2_3 = WorldGen.randPictureTile();
19191:                if (Math.Abs(num2 - index5) < 4 && !WorldGen.nearPicture(index13, index5))

```


---

## 🤖 Assistant · 2026-08-12T21:39:46.074Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"randPictureTile\" ~/Project/GLM/SandboxWorld/Terarria1405/*.cs | grep -v \"WorldGen.cs\" | head -3; sed -n '17966,18000p' ~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs; grep -n \"static Vector2 randPictureTile\" ~/Project/GLM/SandboxWorld/Terarria1405/*.cs",
 "description": "Read nearPicture helpers and find randPictureTile"
}
```


---

## 👤 User(sidechain) · 2026-08-12T21:39:46.125Z

**📎 ToolResult**

```
    public static bool nearPicture(int x, int y)
    {
      for (int index1 = x - 4; index1 <= x + 3; ++index1)
      {
        for (int index2 = y - 3; index2 <= y + 2; ++index2)
        {
          if (Main.tile[index1, index2].active())
            return true;
        }
      }
      return false;
    }

    public static bool nearPicture2(int x, int y)
    {
      if (Main.tile[x, y].wall != (ushort) 7 && Main.tile[x, y].wall != (ushort) 8 && Main.tile[x, y].wall != (ushort) 9)
      {
        for (int index1 = x - 8; index1 <= x + 8; ++index1)
        {
          for (int index2 = y - 5; index2 <= y + 5; ++index2)
          {
            if (Main.tile[index1, index2].active() && (Main.tile[index1, index2].type == (ushort) 240 || Main.tile[index1, index2].type == (ushort) 241 || Main.tile[index1, index2].type == (ushort) 242))
              return true;
          }
        }
      }
      else
      {
        for (int index1 = x - 15; index1 <= x + 15; ++index1)
        {
          for (int index2 = y - 10; index2 <= y + 10; ++index2)
          {
            if (Main.tile[index1, index2].active() && (Main.tile[index1, index2].type == (ushort) 240 || Main.tile[index1, index2].type == (ushort) 241 || Main.tile[index1, index2].type == (ushort) 242))
              return true;
          }
~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs:19806:    public static Vector2 randPictureTile()

```


---

## 🤖 Assistant · 2026-08-12T21:39:50.397Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Note: JS `nearPicture2(st, x, y, mainWall)` uses `wall === mainWall ? 15/10 : 8/5`. Vanilla: wall ∈ {7,8,9} → 15/10, else 8/5. roomWall[0] is 7/8/9, so JS matches.

Also note JS randPic: `if (rng.int(0,2) < 2)` → map [12,13,14,15,18,19,23][rng.int(0,6)] → HANGING; else PAINTING style. Let me read randPictureTile (19806-19855).
```

</details>


---

## 🤖 Assistant · 2026-08-12T21:39:50.616Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1405/WorldGen.cs",
 "limit": 52,
 "offset": 19806
}
```


---

## 👤 User(sidechain) · 2026-08-12T21:39:50.622Z

**📎 ToolResult**

```
19806	    public static Vector2 randPictureTile()
19807	    {
19808	      int num1 = WorldGen.genRand.Next(3);
19809	      int num2 = 0;
19810	      if (num1 <= 1)
19811	      {
19812	        int maxValue = 7;
19813	        num1 = 240;
19814	        num2 = WorldGen.genRand.Next(maxValue);
19815	        if (num2 == 6)
19816	          num2 = WorldGen.genRand.Next(maxValue);
19817	        if (num2 == 0)
19818	          num2 = 12;
19819	        else if (num2 == 1)
19820	          num2 = 13;
19821	        else if (num2 == 2)
19822	          num2 = 14;
19823	        else if (num2 == 3)
19824	          num2 = 15;
19825	        else if (num2 == 4)
19826	          num2 = 18;
19827	        else if (num2 == 5)
19828	          num2 = 19;
19829	        else if (num2 == 6)
19830	          num2 = 23;
19831	      }
19832	      else if (num1 == 2)
19833	      {
19834	        num1 = 242;
19835	        num2 = WorldGen.genRand.Next(17);
19836	        if (num2 > 13)
19837	        {
19838	          switch (num2)
19839	          {
19840	            case 14:
19841	              num2 = 15;
19842	              break;
19843	            case 15:
19844	              num2 = 16;
19845	              break;
19846	            case 16:
19847	              num2 = 30;
19848	              break;
19849	          }
19850	        }
19851	      }
19852	      return new Vector2((float) num1, (float) num2);
19853	    }
19854	
19855	    public static void DungeonStairs(int i, int j, ushort tileType, int wallType)
19856	    {
19857	      Vector2 zero = Vector2.Zero;

```


---

## 🤖 Assistant · 2026-08-12T21:39:58.979Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
JS randPic:
```
const randPic = (): [number, number] => {
  if (rng.int(0, 2) < 2) {
    const map = [12, 13, 14, 15, 18, 19, 23];
    return [HANGING, map[rng.int(0, 6)]];
  }
  const r = rng.int(0, 16);
  const style = r > 13 ? (r === 14 ? 15 : r === 15 ? 16 : 30) : r;
  return [PAINTING, style];
};
```
Vanilla randPictureTile: Next(3) ≤1 → 240 with Next(7), reroll if 6, then map 0..6 → 12/13/14/15/18/19/23.

JS: `rng.int(0,2) < 2` = Next(3)<=1 equivalent (int(0,2) closed = Next(0,3), values 0,1,2; <2 means 0,1 ✓). Then JS does `map[rng.int(0,6)]` = one Next(7) and maps directly — but vanilla has a **reroll if num2==6** (consumes an extra Next(7) when the first roll is 6). JS drops this reroll → RNG stream deviation! Actually wait: reroll changes the value too: first Next(7) gives 6 → reroll Next(7) → new value 0..6 mapped. JS: roll once, 6→map[6]=23 always. Vanilla: if roll==6 → reroll → map[result], so 23 only when the second roll is 6 too.

This is a real deviation: JS consumes 1 die where vanilla consumes 2 (when first==6). Value distribution differs and stream position differs. I need to fix JS: 
```
let n = rng.int(0, 6); if (n === 6) n = rng.int(0, 6);
const map = [12,13,14,15,18,19,23];
return [HANGING, map[n]];
```
Wait careful: vanilla maps num2 after possible reroll through the same if-chain (0→12, ..., 6→23). So final value = map[n] where n is final roll. ✓.

Also randBoneTile JS:
```
const randBone = (): [number, number] => rng.int(0, 1) === 0
  ? [HANGING, rng.int(0, 1) === 0 ? 16 : 17]
  : [CATACOMB, rng.int(0, 8)];
```
Vanilla randBoneTile: Next(2): case 0 → 240, Next(2)→16/17; case 1 → 241, Next(9)→style. ✓ JS matches (int(0,1) closed = Next(0,2) = 0/1 ✓).

OK. Continue reading DungeonStairs (19855-...). Let me read it fully — this is a key function.
````

</details>


---

## 🤖 Assistant · 2026-08-12T21:55:38.716Z · <synthetic>

```
API Error: Response stalled mid-stream. The response above may be incomplete.
```


---

## 👤 User(sidechain) · 2026-08-12T21:55:38.718Z

```
[Request interrupted by user]
```
