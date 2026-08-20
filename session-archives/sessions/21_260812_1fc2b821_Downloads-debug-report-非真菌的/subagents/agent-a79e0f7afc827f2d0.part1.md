# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-12T16:52:33.613Z

```
Codebase: ~/Project/GLM/SandboxWorld (Terraria 1.4.5.6 remake, TS, main code in game/). Thoroughness: very thorough.

Question: in world generation (game/src/world/gen/), the DUNGEON ENTRANCE CORRIDOR at the surface (the open-air hallway where the Old Man walks, carved by DungeonPass) sometimes ends up BLOCKED/COVERED by sand. I need to find every mechanism in OUR worldgen that can place sand (tile id sand / hardened sand / sandstone / desert fossil) on or next to the dungeon entrance corridor.

Investigate and report with file:line citations:

1. Pass order: game/src/world/gen/WorldGen.ts — list the exact order passes run (Reset, Terrain, ..., Dungeon, ..., GravitatingSand, Piles, Beach, Dunes, Desert, FinalCleanup etc.). Especially: does anything that adds/moves sand run AFTER the Dungeon pass?
2. game/src/world/gen/vanilla/DungeonPass.ts — how the entrance is carved (entrance tower/hall), the precalc drift (gs.dungeonLocation can move ±325 per lines ~113-148), and what bounds protect it (beachDistance check line ~123). Also what gs.beachLeftEnd typically is (WorldGen.ts:434) vs minimum possible dungeonLocation after drift.
3. game/src/world/gen/vanilla/BeachPass.ts — full read: how far inland can beach sand be placed? Any bounds vs beachLeftEnd/beachRightStart? Does it skip dungeon bricks (tileDungeon / wallDungeon checks)?
4. game/src/world/gen/vanilla/GravitatingSandPass.ts — what it does, order relative to DungeonPass, whether sand can fall onto/into the carved entrance hall.
5. game/src/world/gen/vanilla/PilesPass.ts, DunesPass.ts, DesertPass.ts — do they place sand at the surface, and do they check for dungeon tiles (tileDungeon/wallDungeon) before placing? Search the whole gen dir for any tileDungeon/wallDungeon gating in sand-placement code.
6. Search for any post-dungeon cleanup that vanilla has like "Clean Up" passes that remove sand from dungeon entrance — do we have equivalents (CleanupPass.ts, FinalCleanupPass.ts)?
7. Also check game/src/world/gen/vanilla/TerrainPass.ts beach flattening — can the entrance corridor be carved into terrain that TerrainPass already flattened near the beach?

Report: concrete list of candidate root causes with file:line, plus the pass order list. Don't fix anything.
```

---

## 📎 Attachment · skill_listing · 2026-08-12T16:52:33.619Z

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

## 🤖 Assistant · 2026-08-12T16:52:35.081Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me investigate this thoroughly. I'll start by listing the gen directory and reading WorldGen.ts pass order, then read the relevant passes in parallel.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:52:35.424Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls -la ~/Project/GLM/SandboxWorld/game/src/world/gen/ ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/ 2>/dev/null",
 "description": "List world gen directory contents"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:35.477Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/:
total 144
drwxr-xr-x@  5 user  staff    160  8月 13 00:16 .
drwxr-xr-x@ 29 user  staff    928  8月 13 00:39 ..
-rw-r--r--@  1 user  staff   2365  8月 10 13:30 SeedEasterEggs.ts
drwxr-xr-x@ 56 user  staff   1792  8月 13 00:34 vanilla
-rw-r--r--@  1 user  staff  69226  8月 13 00:16 WorldGen.ts

~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/:
total 2000
drwxr-xr-x@ 56 user  staff   1792  8月 13 00:34 .
drwxr-xr-x@  5 user  staff    160  8月 13 00:16 ..
-rw-r--r--@  1 user  staff  16491  8月 12 17:27 BeachPass.ts
-rw-r--r--@  1 user  staff   7860  8月 12 23:12 BrokenTrapCleanupPass.ts
-rw-r--r--@  1 user  staff  27149  8月 12 23:38 BuriedChestsPass.ts
-rw-r--r--@  1 user  staff  32160  8月 12 18:23 CaveHousePass.ts
-rw-r--r--@  1 user  staff   9377  8月 11 16:31 CavesPass.ts
-rw-r--r--@  1 user  staff  12242  8月 12 17:14 CaveWallsPass.ts
-rw-r--r--@  1 user  staff   3452  8月 12 17:49 CleanupPass.ts
-rw-r--r--@  1 user  staff  41458  8月 13 00:48 CorruptionPass.ts
-rw-r--r--@  1 user  staff  35925  8月 12 23:38 DesertPass.ts
-rw-r--r--@  1 user  staff   2297  8月 12 11:17 DirtToMudPass.ts
-rw-r--r--@  1 user  staff   9735  8月 12 23:23 DunesPass.ts
-rw-r--r--@  1 user  staff  78768  8月 12 17:45 DungeonPass.ts
-rw-r--r--@  1 user  staff  11655  8月 12 23:11 FinalCleanupPass.ts
-rw-r--r--@  1 user  staff  17141  8月 12 23:30 GemPasses.ts
-rw-r--r--@  1 user  staff   8629  8月 12 23:38 GenState.ts
-rw-r--r--@  1 user  staff   1253  8月 11 16:49 GrassPass.ts
-rw-r--r--@  1 user  staff   6850  8月 12 17:48 GrassWallPass.ts
-rw-r--r--@  1 user  staff   2695  8月 12 17:30 GravitatingSandPass.ts
-rw-r--r--@  1 user  staff  17818  8月 12 17:57 HalfBrickPass.ts
-rw-r--r--@  1 user  staff   1684  8月 11 12:35 HellforgesPass.ts
-rw-r--r--@  1 user  staff  13293  8月 10 13:48 HellFortPass.ts
-rw-r--r--@  1 user  staff  28113  8月 12 18:19 HiveSpiderPass.ts
-rw-r--r--@  1 user  staff   4884  8月 12 15:44 IceBiomePass.ts
-rw-r--r--@  1 user  staff   5562  8月 11 17:53 IslandHousePass.ts
-rw-r--r--@  1 user  staff  11275  8月 12 17:45 JunglePass.ts
-rw-r--r--@  1 user  staff   6555  8月 12 17:54 JungleShrinePass.ts
-rw-r--r--@  1 user  staff   9867  8月 12 17:48 LakesPass.ts
-rw-r--r--@  1 user  staff  38945  8月 12 11:30 LivingTreePass.ts
-rw-r--r--@  1 user  staff  18496  8月 12 13:15 MarbleGranitePass.ts
-rw-r--r--@  1 user  staff  46637  8月 12 23:47 MicroBiomesPass.ts
-rw-r--r--@  1 user  staff   6512  8月 12 17:42 MissingCavesPass.ts
-rw-r--r--@  1 user  staff  13224  8月 12 18:19 MossPass.ts
-rw-r--r--@  1 user  staff   8370  8月 11 23:27 MountCavesPass.ts
-rw-r--r--@  1 user  staff  11890  8月 12 23:48 MushroomPass.ts
-rw-r--r--@  1 user  staff  10388  8月 12 23:06 OasisPass.ts
-rw-r--r--@  1 user  staff  10184  8月 12 22:50 OceanCavesPass.ts
-rw-r--r--@  1 user  staff  20222  8月 12 18:14 PilesPass.ts
-rw-r--r--@  1 user  staff  14731  8月 12 18:17 ShimmerPass.ts
-rw-r--r--@  1 user  staff   6205  8月 12 17:49 ShiniesPass.ts
-rw-r--r--@  1 user  staff   6911  8月 11 17:11 Spread.ts
-rw-r--r--@  1 user  staff   5247  8月 12 18:21 StatuesPass.ts
-rw-r--r--@  1 user  staff  54611  8月 12 23:23 StructuresPass.ts
-rw-r--r--@  1 user  staff  80016  8月 12 18:22 SurfaceDecorPasses.ts
-rw-r--r--@  1 user  staff   5302  8月 11 17:20 SwordShrinePass.ts
-rw-r--r--@  1 user  staff  30521  8月 12 17:32 TemplePass.ts
-rw-r--r--@  1 user  staff   7273  8月 11 21:12 TerrainPass.ts
-rw-r--r--@  1 user  staff   9668  8月 12 23:14 TileCleanupPass.ts
-rw-r--r--@  1 user  staff  12764  8月 12 13:08 TileRunner.ts
-rw-r--r--@  1 user  staff  16883  8月 12 23:51 TrackPass.ts
-rw-r--r--@  1 user  staff  13931  8月 12 18:21 TrapsPass.ts
-rw-r--r--@  1 user  staff  23248  8月 12 23:04 TreePass.ts
-rw-r--r--@  1 user  staff   7207  8月 12 23:24 UnderworldPass.ts
-rw-r--r--@  1 user  staff   4548  8月 12 18:30 WaterIcePasses.ts
-rw-r--r--@  1 user  staff   1863  8月 12 14:23 WebsPass.ts

```


---

## 🤖 Assistant · 2026-08-12T16:52:35.788Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"Pass\\b\\|Pass(\" ~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts | head -120",
 "description": "Find pass order in WorldGen.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:35.843Z

**📎 ToolResult**

```
19:export interface Pass {
50:  // 单一 vanilla 管线。原 lgcTerrain=false 的 fbm 回退（terrainPass/cavePass/
51:  // floatCleanupPass 分支）是无 UI 入口的死代码且 hellPass 处会空指针崩溃，已删除。
52:  // pass 顺序对齐原版 AddGenerationPass 注册序（WorldGen.cs:11525-22660，
58:  const passes: Pass[] = [
75:    { name: '引力沙', run: gravitatingSandPass },
85:    { name: '水体沉降', run: liquidSettlePass },
89:    { name: '沙上清水', run: surfaceWaterAboveSandPass },
93:    { name: '绿洲', run: oasisPass },
99:    // （半砖 = 原版水浸润/瀑布触发的核心，见 HalfBrickPass.ts）
100:    { name: '半砖平滑', run: halfBrickSmoothPass },
101:    { name: '瀑布唇缘', run: waterfallLipPass },
105:    { name: '薄冰', run: fragileIcePass },
109:    { name: '洞穴墙变体', run: caveWallVarietyPass },
114:    // 曾在生物群系 pass 里随洞穴箱一起放 → 被后续 hellPass 重写 100% 抹除
115:    { name: '地狱箱', run: underworldChestsPass },
122:    { name: '宝石洞', run: gemCavesPass },
128:    { name: '洞穴墙', run: caveWallsPass },
131:    { name: '瓦罐', run: potPass },
133:    { name: '地狱熔炉', run: hellforgesPass },
135:    { name: '矿骨堆', run: pilesPass },
136:    // 表面（legacy 外壳：铺草=原版 pass 77 SpreadingGrass；内嵌 vanilla TreePass
138:    { name: '表面', run: surfacePass },
153:    { name: '栽树', run: treesPass },
179:    { name: '蜂巢幼虫', run: beeLarvaPass },
184:    { name: '仙人掌珊瑚', run: cactusCoralPass },
188:    { name: '瓦片清理', run: tileCleanupPass },
198:    { name: '断线陷阱清理', run: brokenTrapCleanupPass },
202:    { name: '终清理', run: finalCleanupPass },
221:import { runTerrainPass } from './vanilla/TerrainPass';
222:import { runRocksAndClayPass, runCavesPass } from './vanilla/CavesPass';
223:import { runOceanSandPass, runBeachesPass, runBeachDecorPass } from './vanilla/BeachPass';
224:import { runIceBiomePass, runSlushPass } from './vanilla/IceBiomePass';
225:import { runWebsPass as runVanillaWebsPass } from './vanilla/WebsPass';
226:import { runUnderworldPass } from './vanilla/UnderworldPass';
227:import { runGrassPass } from './vanilla/GrassPass';
228:import { runJunglePass } from './vanilla/JunglePass';
229:import { runMudCavesPass, spreadGrass } from './vanilla/Spread';
230:import { runDesertPass } from './vanilla/DesertPass';
231:import { runMushroomPass } from './vanilla/MushroomPass';
232:import { runMarbleGranitePass } from './vanilla/MarbleGranitePass';
233:import { runDunesPass } from './vanilla/DunesPass';
234:import { runShimmerPass } from './vanilla/ShimmerPass';
235:import { runMicroBiomesPass } from './vanilla/MicroBiomesPass';
236:import { runDirtToMudAndSiltPass } from './vanilla/DirtToMudPass';
237:import { runCleanupPass } from './vanilla/CleanupPass';
238:import { runSmoothWorldPass, runWaterfallLipPass } from './vanilla/HalfBrickPass';
239:import { runShiniesPass, runGemsPass } from './vanilla/ShiniesPass';
240:import { runGemCavesPass, runExposedGemsPass, runGemTreesPass } from './vanilla/GemPasses';
241:import { runCaveWallsPass, runCaveWallVarietyPass } from './vanilla/CaveWallsPass';
242:import { runOasisPass } from './vanilla/OasisPass';
243:import { runCactusPalmTreesAndCoralPass } from './vanilla/StructuresPass';
244:import { runTileCleanupPass } from './vanilla/TileCleanupPass';
245:import { runBrokenTrapCleanupPass } from './vanilla/BrokenTrapCleanupPass';
246:import { runFinalCleanupPass } from './vanilla/FinalCleanupPass';
247:import { runMossAndMossCavesPass } from './vanilla/MossPass';
248:import { runGrassWallPass } from './vanilla/GrassWallPass';
249:import { runMountCavesPass, runMountainCavesPass } from './vanilla/MountCavesPass';
250:import { runTreePass, randomizeTreeStyle, growAshTree } from './vanilla/TreePass';
251:import { runLakesPass } from './vanilla/LakesPass';
252:import { runGravitatingSandPass } from './vanilla/GravitatingSandPass';
253:import { runTrapsPass } from './vanilla/TrapsPass';
254:import { runFloatingIslandsPass, runLifeCrystalsPass, runSurfaceDecorPass, runPyramidPass, runWetJunglePass, runAlchemyHerbsPass } from './vanilla/StructuresPass';
256:  runSurfaceOreAndStonePass, runFallenLogsPass, runDyePlantsPass, runVinesPass,
257:  runFlowersPass, runMushroomsPass, runLongMossPass, runLilypadsPass,
258:  runGrassPlantsPass, runGlowingMushroomPlantsPass,
260:import { runLivingTreesPass, runLivingTreeWallsPass } from './vanilla/LivingTreePass';
261:import { runBeehivePass, runSpiderNestPass, runWebsInSpiderCavesPass, runBeeLarvaPass } from './vanilla/HiveSpiderPass';
262:import { runPilesPass } from './vanilla/PilesPass';
263:import { runRemoveSurfaceWaterAboveSandPass, runFragileIcePass } from './vanilla/WaterIcePasses';
265:import { runDungeonPass } from './vanilla/DungeonPass';
266:import { runTemplePass } from './vanilla/TemplePass';
267:import { runIslandHousePass } from './vanilla/IslandHousePass';
268:import { runHellFortPass } from './vanilla/HellFortPass';
269:import { runSwordShrinePass } from './vanilla/SwordShrinePass';
270:import { runBuriedChestsPass, runUnderworldChestsPass, runSurfaceChestsPass, runWaterChestsPass } from './vanilla/BuriedChestsPass';
271:import { runStatuesPass } from './vanilla/StatuesPass';
272:import { runJungleShrinePass, runJungleChestsPass } from './vanilla/JungleShrinePass';
273:import { runCaveHousesPass } from './vanilla/CaveHousePass';
274:import { runOceanCavesPass, runUnderwaterChestsPass } from './vanilla/OceanCavesPass';
275:import { runHellforgesPass } from './vanilla/HellforgesPass';
276:import { runCorruptionPass } from './vanilla/CorruptionPass';
277:import { runSandPatchesPass, runTunnelsPass, runDirtWallBgPass, runSmallHolesPass } from './vanilla/MissingCavesPass';
282:async function liquidSettlePass({ world }: GenCtx) {
319:  //    JungleShrinePass 复用本值（曾照掷照弃致 pass 内重掷、流位+样式双偏）
444:  runTerrainPass(store, rng, gs);
445:  // surface 数组给后续旧 pass(surfacePass 树木等)用:每列首个实心行
462:  runDunesPass(store, rng, gs);
469:  runShimmerPass(store, rng, gs);
479:  runSurfaceOreAndStonePass(store, rng, gs);
484:  runFallenLogsPass(store, rng, gs);
491:  runDyePlantsPass(store, rng, gs);
496:  runVinesPass(store, rng, gs);
501:  runFlowersPass(store, rng, gs);
506:  runMushroomsPass(store, rng, gs);
511:  runLongMossPass(store, rng, gs);
516:  runLilypadsPass(store, rng, gs);
523:  runMicroBiomesPass(store, rng, gs);
541:  runOceanSandPass(store, rng, gs);
542:  runSandPatchesPass(store, rng, gs);   // 地下沙团（沙漠雏形）
543:  runTunnelsPass(store, rng, gs);       // 地表隧道（dirt runner 双向填充）
544:  runMountCavesPass(store, rng, gs);    // 山丘本体
545:  runDirtWallBgPass(store, rng, gs);    // 地表自然墙（wall 2/40）
546:  runRocksAndClayPass(store, rng, gs);
547:  runSmallHolesPass(store, rng, gs);    // 小空洞（每轮 2 发挖除 runner）
548:  runCavesPass(store, rng, gs);
561:  runIceBiomePass(store, rng, gs);       // 16 Generate Ice Biome
562:  runGrassPass(store, rng, gs);          // 17 Grass
563:  const jx = runJunglePass(store, rng, gs); // JunglePass
580:  runMudCavesPass(store, TILE_BY_KEY['mud']!, TILE_BY_KEY['v_60_jungle_grass_block']!);
581:  runDesertPass(store, rng, gs);         // 19 Full Desert
582:  runMushroomPass(store, rng, gs);       // 20 Mushroom Patches
583:  runMarbleGranitePass(store, rng, gs);  // 21/22 Marble/Granite
584:  runFloatingIslandsPass(store, rng, gs); // 23 Floating Islands（原在蘑菇前——注册序修正）
585:  runDirtToMudAndSiltPass(store, rng, gs); // 24 Dirt To Mud / 25 Silt
586:  runShiniesPass(store, rng, gs);        // 26 Ores And Shinies（原在很后"矿石"槽——移到 Silt 后=Webs 位）
587:  runVanillaWebsPass(store, rng, gs);     // 27 Webs（cs:13659——原后置防被清，注册序修正回 27 位）
588:  runUnderworldPass(store, rng, gs);     // 28 Underworld（cs:13697——原管线末"地狱"槽；
590:  runCorruptionPass(store, rng, gs);     // 29 Corruption/Crimson
591:  runLakesPass(store, rng, gs);          // 30 Lakes（cs:14613——原"液体"槽在结构段后，注册序修正）

```


---

## 🤖 Assistant · 2026-08-12T16:52:37.169Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me read WorldGen.ts passes list (lines 58-220) and the full gen sequence (lines 400-700). Also DungeonPass lines around 113-148, and BeachPass full.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:52:37.414Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts",
 "limit": 170,
 "offset": 55
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:37.435Z

**📎 ToolResult**

```
55	  //   清理(37) 生命水晶(55) 半砖平滑(57) 瀑布(58) 地狱(31) 地狱屋(76 前段)
56	  //   地狱箱(63 地狱段) 小屋+散箱(63) 瓦罐(75) 矿骨堆(81) 表面(77/86/90)
57	  //   地表装饰(76 traps/85) 海滩装饰(56) 结构
58	  const passes: Pass[] = [
59	    { name: '原版地形', run: vanillaTerrain },
60	    // 原版注册序 Dunes(cs:11540) < Ocean Sand(cs:11603):沙丘先于海洋沙/海滩塑造,
61	    // 并同时掷金字塔候选(cs:11591-11599 → gs.pyramidSpots)
62	    { name: '沙丘', run: vanillaDunes },
63	    { name: '洞穴', run: vanillaCaves },
64	    // 海滩(33 MountainCaveOpenings+34 Beaches)与矿石(26 OresAndShinies)原在此处
65	    // 各占一槽——已按 1456 注册序并入 vanillaBiomes（分别在 Dungeon(32) 后与 Silt(25) 后）。
66	    { name: '生物群系', run: vanillaBiomes },
67	    // 原版 1456 注册序:OresAndShinies(13233) → Lakes(14613) → DirtWallCleanup(15310)
68	    // → SettleLiquids(16215) → SmoothWorld(16507) → Waterfalls(16697) → LifeCrystals(16847)。
69	    // 生命水晶曾排在湖泊之前——湖泊 pass 挖湖盆会掏空已放水晶的脚下 → 凭空悬浮
70	    // （唯一硬约束:水晶在 Lakes 之后;平滑/瀑布在其前的原版序可完整对齐）
71	    { name: '液体', run: vanillaLakes },
72	    // 引力沙（原版 GravitatingSandCleanup cs:15198，注册位 Lakes(14613) < 本 pass <
73	    // Shimmer(15256)）：地表内悬空 Falling 系方块空腔落定。纯扫描零掷骰。
74	    // 2026-08-12 前整 pass 缺失——海岸/沙滩带生成残留的浮空沙无人回收。
75	    { name: '引力沙', run: gravitatingSandPass },
76	    // 原版注册序 Lakes(14613) < Shimmer(15256) < DirtWallCleanup(15310)：
77	    // 微光以太在此挖洞灌液，清理/沉降在其后（Slush 31 已随 Lakes 入"液体"槽）
78	    { name: '微光', run: vanillaShimmer },
79	    { name: '清理', run: vanillaCleanup },
80	    // 原版 SettleLiquids（cs:16215）：Lakes 之后、SmoothWorld/Waterfalls 之前的中途
81	    // 沉降——瀑布唇缘/半砖平滑直接读 st.liquid 判定，必须在静止水面数据上跑
82	    // （此前沉降只在管线末尾 → 唇缘基于未沉降水体漂移）。
83	    // 原版 SettleLiquidsPart2（cs:21051，管线尾二次沉降）由 generateWorld 之后
84	    // worker/Game 的 settleWorldLiquids('gen') 承担。
85	    { name: '水体沉降', run: liquidSettlePass },
86	    // 沙上清水（原版 RemoveSurfaceWaterAboveSand cs:16295-16326，注册序
87	    // SettleLiquids(16215) < 本 pass < Oasis(16327) < ShellPiles(16385)）：
88	    // 地表沙柱上方的悬空水清除——零掷骰纯扫描（2026-08-12 前整 pass 缺失）
89	    { name: '沙上清水', run: surfaceWaterAboveSandPass },
90	    // 绿洲（原版 Oasis cs:16327，注册序 RemoveSurfaceWaterAboveSand(16295) < 本 pass
91	    // < ShellPiles(16385)）：PlaceOasis 挖塘+岸线，登记 gs.oasisX/Y/W（pass 98 的
92	    // 绿洲棕榈/燕麦/植物 530 消费段未实现，备案）
93	    { name: '绿洲', run: oasisPass },
94	    // 海滩装饰（原版 ShellPiles cs:16393-16501）：贝壳堆。原版注册序
95	    // SettleLiquids(16215) < ShellPiles(16385) < SmoothWorld(16507)——必须在半砖平滑
96	    // 之前，否则堆出的散沙/孤立单格无人回收（2026-08-12 前排管线末尾=海里单体沙来源之一）
97	    { name: '海滩装饰', run: vanillaBeachDecor },
98	    // 原版 "Smooth World"(cs:16507)+"Waterfalls"(cs:16697)：地表凸起与水边唇缘砸半砖
99	    // （半砖 = 原版水浸润/瀑布触发的核心，见 HalfBrickPass.ts）
100	    { name: '半砖平滑', run: halfBrickSmoothPass },
101	    { name: '瀑布唇缘', run: waterfallLipPass },
102	    // 薄冰（原版 FragileIceOverIceBiomeWater cs:16756-16785 + MakeWateryIceThing
103	    // cs:80206，注册序 Waterfalls(16697) < 本 pass < CaveWallVariety(16786)）：
104	    // 冰原水面上铺 BreakableIce 162——零掷骰（2026-08-12 前整 pass 缺失）
105	    { name: '薄冰', run: fragileIcePass },
106	    // 洞穴墙变体斑（原版 CaveWallVariety cs:16786，注册序 Waterfalls(16697) <
107	    // 本 pass < LifeCrystals(16847)）：泥土墙 196-199/丛林 204-207/石墙 208-215
108	    // —— CaveWalls 主 pass（苔藓槽后）的前置墙基之一
109	    { name: '洞穴墙变体', run: caveWallVarietyPass },
110	    { name: '生命水晶', run: vanillaLifeCrystals },
111	    // 地狱(Underworld 28) 已按注册序并入 vanillaBiomes（Webs 27 后、Corruption 29 前）
112	    { name: '地狱屋', run: vanillaHellHouses },
113	    // 地狱箱:必须在地狱地形+地狱屋之后(原版 Underworld 29 < Buried Chests 59);
114	    // 曾在生物群系 pass 里随洞穴箱一起放 → 被后续 hellPass 重写 100% 抹除
115	    { name: '地狱箱', run: underworldChestsPass },
116	    // 苔藓（原版 MossAndMossCaves cs:17573，注册序 BuriedChests 17066 < 本 pass <
117	    // Pots 18186）：霓虹苔藓洞 + 苔藓斑/散点/地狱氦苔藓——洞穴系全部定型后只做
118	    // 石→苔藓点状替换；长苔藓 pass（20915）的上游，缺它则全图 0 长苔藓
119	    // 宝石洞（原版 GemCaves cs:17528，注册序 < Moss(17573) < CaveWalls(17819)）：
120	    // 必须先于 CaveWalls——Spread.Gem 遇墙不扩散，先刷墙会压制宝石洞；
121	    // 此前挤在"宝石系统"槽（Moss 后近 30 槽）= 顺序偏差，已归位
122	    { name: '宝石洞', run: gemCavesPass },
123	    { name: '苔藓', run: vanillaMoss },
124	    // 洞穴自然墙（原版 CaveWallsInEnclosedSpaces cs:17819，注册序 Moss(17573) <
125	    // 本 pass < UndergroundJungleTrees(17952)）：封闭腔刷洞穴背景墙 + 丛林泥墙段。
126	    // 地下自然墙唯二来源之一（另一=DirtWallBackgrounds 近地表）——缺它全洞穴无墙,
127	    // 暴露晶簇(178,贴墙装饰)悬空(2026-08-12 用户标注)
128	    { name: '洞穴墙', run: caveWallsPass },
129	    // 瓦罐（原版 PotsGraveyardsAndBoulderPiles cs:18108,注册序 CaveWalls(17819) <
130	    // 本 pass < Hellforges(18298)）——曾排在熔炉后=与原版对调,2026-08-13 归位
131	    { name: '瓦罐', run: potPass },
132	    // 地狱熔炉(原版 Hellforges,cs:18298:w/200 个,墙 13/14 门禁)
133	    { name: '地狱熔炉', run: hellforgesPass },
134	    // 矿骨堆（原版 pass 81 Piles 位置）
135	    { name: '矿骨堆', run: pilesPass },
136	    // 表面（legacy 外壳：铺草=原版 pass 77 SpreadingGrass；内嵌 vanilla TreePass
137	    // =原版 pass 82 Trees；AlchemyHerbs(20109)+GrassPlants(20209)）
138	    { name: '表面', run: surfacePass },
139	    // 地表矿石（原版 SurfaceOreAndStone cs:18559）：OrePatch/StonePatch 需先有草面
140	    //（SpreadingGrass 18349 < 本 pass）——放在"表面"之后、"地表装饰"(内含 Traps 18769)之前
141	    { name: '地表矿石', run: vanillaSurfaceOre },
142	    // 倒木（原版 FallenLogsAndWaterFeatures cs:18625，仅倒木段）：登记 gs.logX/logY
143	    // 给 Flowers(20592) 消费
144	    { name: '倒木水景', run: vanillaFallenLogs },
145	    { name: '地表装饰', run: vanillaSurfaceDecor },
146	    // 草墙（原版 SurfaceDirtWallsToGrassWalls cs:19734，注册序 Piles 18900 之后的
147	    // SpawnPoint 19605 < 本 pass < DyePlants 20126）：地表泥土墙洞 → 草墙 63/花墙 65——
148	    // Vines pass 花藤 382 的上游（藤头墙 ∈ {63,65,66,68} 才出花藤）
149	    { name: '草墙', run: vanillaGrassWall },
150	    // 栽树（原版 Planting Trees cs:20085，注册序 GrassWall(19734) < 本 pass <
151	    // AlchemyHerbs(20109)）——曾内嵌"表面"槽（地表矿石/倒木/陷阱/矿骨堆/草墙之前）,
152	    // 2026-08-13 归位（Batch D）
153	    { name: '栽树', run: treesPass },
154	    // 炼金草药（原版 AlchemyHerbs cs:20109，Trees 之后、DyePlants(20126) 之前）
155	    { name: '炼金草药', run: alchemyHerbsSlot },
156	    // 染料植物（原版 DyePlants cs:20126）：plantDye + MatureTheHerbPlants +
157	    // GrowGlowTulips(656) + PlaceChilletEggs(752)，位于 AlchemyHerbs(20109) 之后
158	    { name: '染料植物', run: vanillaDyePlants },
159	    // 蛛网蜂巢（原版 WebsInSpiderCavesAndHoney cs:20140，注册序 DyePlants(20126) <
160	    // 本 pass < GrassPlants(20232)）——曾内嵌 vanillaBiomes 尾（提前约 40 槽）,归位
161	    { name: '蛛网蜂巢', run: websInSpiderCavesSlot },
162	    // 地表植物（原版 GrassPlants cs:20232 + GlowingMushroomPlants cs:20278，注册序
163	    // Webs(20140) < 两者 < Vines(20338)）——曾内嵌"表面"槽,归位
164	    { name: '地表植物', run: grassPlantsSlot },
165	    // 藤蔓（原版 Vines cs:20338）：六类藤蔓逐列生长 + 丛林蜂巢凹龛
166	    { name: '藤蔓', run: vanillaVines },
167	    // 地表花（原版 Flowers cs:20592）：花圃重帧，消费 gs.logX/logY
168	    { name: '地表花', run: vanillaFlowers },
169	    // 地表蘑菇（原版 Mushrooms cs:20744）：蘑菇斑帧重刷
170	    { name: '地表蘑菇', run: vanillaMushrooms },
171	    // 宝石系统（原版 ExposedGems(20842/20874) < SpeleothemsAndGemTrees(22196)：
172	    // 装饰之后、海滩装饰之前；GemCaves 已前移"宝石洞"槽）
173	    { name: '宝石系统', run: vanillaGems },
174	    // 长苔藓（原版 LongMoss cs:20915）：苔藓块四向冒芽，位于 ExposedGems 之后
175	    { name: '长苔藓', run: vanillaLongMoss },
176	    // 蜂巢幼虫（原版 BeeLarvaInBeehives cs:21018-21050，注册序 LongMoss(20915) <
177	    // 本 pass < SettleLiquidsPart2(21051)）：蜂巢 pass 只登记坐标，托台清空+幼虫
178	    // 放置推迟到这里——过早放置会被中途宝箱/装饰 pass 破坏
179	    { name: '蜂巢幼虫', run: beeLarvaPass },
180	    // 仙人掌/棕榈/珊瑚（原版 CactusPalmTreesAndCoral cs:21115-21325，注册序
181	    // SettleLiquidsPart2(21051) < 本 pass < TileCleanup(21327)）：GrowCactus 全量
182	    //（PlantCactus 150 次邻域成簇）+两端海滩珊瑚 81/贝壳 324+中段水盒棕榈
183	    //（此前为 12% 直柱简化,2026-08-13 全量重写）
184	    { name: '仙人掌珊瑚', run: cactusCoralPass },
185	    // 瓦片清理（原版 TileCleanup cs:21327-21751 必补子项：全图清坡/坡接半砖修复/
186	    // 液体中草本 KillTile/滴水石笋 373-375/墙 13·14·87 液体清零/祭坛下 232→226；
187	    // 帧规范化族由放置端保证,备案）——注册序本 pass(21327) < MicroBiomes(21785)
188	    { name: '瓦片清理', run: tileCleanupPass },
189	    // 原版 Micro Biomes(cs:21785:Campsites 21915 + MiningExplosives 21951),
190	    // 位于 Traps/Piles/Trees 之后、Lilypads/海藻(22131,=海滩装饰)之前
191	    { name: '微群系', run: vanillaMicroBiomes },
192	    // 水生植物（原版 LilypadsCattailsBambooAndSeaweed cs:22131）：睡莲/香蒲/竹/海藻
193	    // （注册序 Lilypads(22131) 在 ShellPiles(16385) 之后——贝壳堆已前移"水体沉降"后）
194	    { name: '水生植物', run: vanillaLilypads },
195	    // 断线陷阱清理（原版 BrokenTrapCleanup cs:22283：电线 BFS 连通网无陷阱/触发器
196	    // 对→整网拆除,含巨石回滚/孤儿陷阱击杀/矿轨压板复位）——注册序 Lilypads(22131)
197	    // < 本 pass < FinalCleanup(22304)。零掷骰
198	    { name: '断线陷阱清理', run: brokenTrapCleanupPass },
199	    // 终清理（原版 FinalCleanup cs:22304-22670 必补子项：悬空落体柱生长+封底/
200	    // 沙岩硬沙墙灌满岩浆/巨石重帧补支撑/液体中棕榈杀/地牢墙液体转水/矿轨清液/
201	    // 金币堆补底/地表散水清除/画作继承邻墙；FillWallHoles 与彩蛋备案）。零掷骰
202	    { name: '终清理', run: finalCleanupPass },
203	  ];
204	
205	  for (let i = 0; i < passes.length; i++) {
206	    onProgress?.(passes[i].name, i / passes.length);
207	    await nextFrame();
208	    await passes[i].run(ctx, () => {});
209	    // 部分世界回调（生成期实时预览）：pass 完成即暴露，不等 finalize
210	    if (cfg.onWorldPartial) cfg.onWorldPartial(world, i, passes[i].name);
211	  }
212	
213	  finalize(ctx);
214	  onProgress?.('完成', 1);
215	  return world;
216	}
217	
218	// ---------- 原版管线 pass(阶段 1-2 移植) ----------
219	import { newGenState, type GenState } from './vanilla/GenState';
220	import { parseSeed } from './SeedEasterEggs';
221	import { runTerrainPass } from './vanilla/TerrainPass';
222	import { runRocksAndClayPass, runCavesPass } from './vanilla/CavesPass';
223	import { runOceanSandPass, runBeachesPass, runBeachDecorPass } from './vanilla/BeachPass';
224	import { runIceBiomePass, runSlushPass } from './vanilla/IceBiomePass';

```


---

## 🤖 Assistant · 2026-08-12T16:52:37.608Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts",
 "limit": 280,
 "offset": 420
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:37.615Z

**📎 ToolResult**

```
420	  let dX = rng.nextInt(W);
421	  const dLo = W * (gs.dungeonSide === 1 ? 0.60 : 0.25);
422	  const dHi = W * (gs.dungeonSide === 1 ? 0.75 : 0.40);
423	  while (dX < dLo || dX > dHi) dX = rng.nextInt(W);
424	  gs.dungeonX = dX;
425	  // ⑳ 雪原（cs:11425-11440）：锚点两侧独立扩展（num9 = w/4200，小世界恰 1.0）
426	  const num9 = W / 4200;
427	  const snowHalf = () => rng.nextIntRange(50, 90)
428	    + Math.trunc(rng.nextIntRange(20, 40) * num9)
429	    + Math.trunc(rng.nextIntRange(20, 40) * num9);
430	  const snowL = snowHalf(), snowR = snowHalf();
431	  gs.snowOriginLeft = Math.max(0, dX - snowL);
432	  gs.snowOriginRight = Math.min(W, dX + snowR);
433	  // ㉑㉒ 海滩（cs:11445-11459）：Next(300,340)（center 320±range 20）+ 侧别加宽
434	  gs.beachLeftEnd = rng.nextIntRange(300, 340) + (gs.dungeonSide === 1 ? 40 : 20);
435	  gs.beachRightStart = W - rng.nextIntRange(300, 340) - (gs.dungeonSide === -1 ? 40 : 20);
436	  // ㉓ 地牢入口（cs:11461-11470）：地牢侧海滩内 15% 区间（dungeonBeachPadding=50）
437	  if (gs.dungeonSide === -1) {
438	    gs.dungeonLocation = rng.nextIntRange(gs.beachLeftEnd + 50, Math.trunc(W * 0.2));
439	  } else {
440	    gs.dungeonLocation = rng.nextIntRange(Math.trunc(W * 0.8), gs.beachRightStart - 50);
441	  }
442	  world.dungeonX = gs.dungeonLocation;
443	  // ===== Terrain pass（原版第一个注册 pass，cs:11526）=====
444	  runTerrainPass(store, rng, gs);
445	  // surface 数组给后续旧 pass(surfacePass 树木等)用:每列首个实心行
446	  for (let x = 0; x < store.w; x++) {
447	    for (let y = 0; y < store.h; y++) {
448	      if (store.flags[store.idx(x, y)]) { surface[x] = y; break; }
449	    }
450	  }
451	  ctxGs[0] = gs;
452	  // 世界级常量同步
453	  world.groundLevel = gs.worldSurface;
454	  world.rockLevel = gs.rockLevel;
455	  world.lavaLine = gs.lavaLine;
456	}
457	
458	// 原版 pass "Dunes"(cs:11540):沙丘塑造 + 金字塔候选(gs.pyramidSpots)
459	function vanillaDunes({ store, rng }: GenCtx) {
460	  const gs = ctxGs[0];
461	  if (!gs) return;
462	  runDunesPass(store, rng, gs);
463	}
464	
465	// 原版 pass "Shimmer"(cs:15256):以太微光生物群系
466	function vanillaShimmer({ store, rng, world }: GenCtx) {
467	  const gs = ctxGs[0];
468	  if (!gs) return;
469	  runShimmerPass(store, rng, gs);
470	  // GenVars.shimmerPosition 落到 World（中途沉降 pass 在 finalize 之前就需要它）
471	  world.shimmerX = gs.shimmerX;
472	  world.shimmerY = gs.shimmerY;
473	}
474	
475	// 原版 pass "Surface Ore And Stone"(cs:18559) + "Fallen Logs And Water Features"(cs:18625)
476	function vanillaSurfaceOre({ store, rng }: GenCtx) {
477	  const gs = ctxGs[0];
478	  if (!gs) return;
479	  runSurfaceOreAndStonePass(store, rng, gs);
480	}
481	function vanillaFallenLogs({ store, rng }: GenCtx) {
482	  const gs = ctxGs[0];
483	  if (!gs) return;
484	  runFallenLogsPass(store, rng, gs);
485	}
486	
487	// 原版表面装饰子 pass 群（cs:20126/20338/20592/20744/20915/22131，见 SurfaceDecorPasses.ts）
488	function vanillaDyePlants({ store, rng }: GenCtx) {
489	  const gs = ctxGs[0];
490	  if (!gs) return;
491	  runDyePlantsPass(store, rng, gs);
492	}
493	function vanillaVines({ store, rng }: GenCtx) {
494	  const gs = ctxGs[0];
495	  if (!gs) return;
496	  runVinesPass(store, rng, gs);
497	}
498	function vanillaFlowers({ store, rng }: GenCtx) {
499	  const gs = ctxGs[0];
500	  if (!gs) return;
501	  runFlowersPass(store, rng, gs);
502	}
503	function vanillaMushrooms({ store, rng }: GenCtx) {
504	  const gs = ctxGs[0];
505	  if (!gs) return;
506	  runMushroomsPass(store, rng, gs);
507	}
508	function vanillaLongMoss({ store, rng }: GenCtx) {
509	  const gs = ctxGs[0];
510	  if (!gs) return;
511	  runLongMossPass(store, rng, gs);
512	}
513	function vanillaLilypads({ store, rng }: GenCtx) {
514	  const gs = ctxGs[0];
515	  if (!gs) return;
516	  runLilypadsPass(store, rng, gs);
517	}
518	
519	// 原版 pass "Micro Biomes"(cs:21785):露营地标 + 炸药陷阱屋
520	function vanillaMicroBiomes({ store, rng }: GenCtx) {
521	  const gs = ctxGs[0];
522	  if (!gs) return;
523	  runMicroBiomesPass(store, rng, gs);
524	}
525	
526	function vanillaLakes({ store, rng }: GenCtx) {
527	  // Lakes(30)/Slush(31) 已按注册序并入 vanillaBiomes（Corruption(29) 后、Dungeon(32) 前）
528	  // ——本槽保留空壳防外部引用。
529	  void store; void rng;
530	  const gs = ctxGs[0];
531	  if (!gs) return;
532	}
533	
534	function vanillaCaves({ store, rng }: GenCtx) {
535	  const gs = ctxGs[0];
536	  if (!gs) return;
537	  // 原版注册序（1456）：OceanSand(11603) → SandPatches(11712) → Tunnels(11743) →
538	  // MountainCaves(11809) → DirtWallBackgrounds(11883) → RocksInDirt/DirtInRocks/Clay
539	  // → SmallHoles(12034) → DirtLayer/RockLayer/Surface Caves（WavyCaves 12301 仅
540	  // 饥荒世界，普通世界零掷骰跳过）
541	  runOceanSandPass(store, rng, gs);
542	  runSandPatchesPass(store, rng, gs);   // 地下沙团（沙漠雏形）
543	  runTunnelsPass(store, rng, gs);       // 地表隧道（dirt runner 双向填充）
544	  runMountCavesPass(store, rng, gs);    // 山丘本体
545	  runDirtWallBgPass(store, rng, gs);    // 地表自然墙（wall 2/40）
546	  runRocksAndClayPass(store, rng, gs);
547	  runSmallHolesPass(store, rng, gs);    // 小空洞（每轮 2 发挖除 runner）
548	  runCavesPass(store, rng, gs);
549	}
550	
551	// 原版 1456 真实注册序（执行序=注册序，WorldGenerator.cs:447 _passes[PassResults.Count]）：
552	//   14 SurfaceCaves → 15 WavyCaves(仅饥荒世界,普通零消耗) → 16 IceBiome → 17 Grass
553	//   → 18 MudCaves → 19 Desert → 20 Mushroom → 21 Marble → 22 Granite → 23 FloatingIslands
554	//   → 24 DirtToMud → 25 Silt → 26 OresAndShinies → 27 Webs(未移植) → 28 Underworld
555	//   → 29 Corruption → 30 Lakes → 31 Slush → 32 Dungeon → 33 MountainCaveOpenings
556	//   → 34 Beaches → 35 Gems → 36 GravitatingSand → 37 OceanCaves → 38 Shimmer → 39 DirtWallCleanup
557	// 本函数内对齐到 16-35 段（Underworld 28 在管线末"地狱"槽、Webs 27 后置——既有偏差另案）。
558	function vanillaBiomes({ store, rng, world, surface }: GenCtx) {
559	  const gs = ctxGs[0];
560	  if (!gs) return;
561	  runIceBiomePass(store, rng, gs);       // 16 Generate Ice Biome
562	  runGrassPass(store, rng, gs);          // 17 Grass
563	  const jx = runJunglePass(store, rng, gs); // JunglePass
564	  world.jungleX = jx;
565	  // 丛林表面泥化:泥柱核心区 ±0.12w 内,表层 10 格 dirt→mud(原版巨型 runner
566	  // 覆盖表面所致;我们补这一步让丛林表面成草皮而非裸土)
567	  {
568	    const core = (gs as any).jungleCoreX ?? jx;
569	    const reach = Math.floor(store.w * 0.12);
570	    for (let x = Math.max(0, core - reach); x < Math.min(store.w, core + reach); x++) {
571	      let sy = 0;
572	      while (sy < store.h - 12 && !store.flags[store.idx(x, sy)]) sy++;
573	      for (let y = sy; y < sy + 10; y++) {
574	        if (store.get(x, y) === T.DIRT) store.setTileSilent(x, y, TILE_BY_KEY['mud']!);
575	      }
576	    }
577	  }
578	  // 18 Mud Caves To Grass（cs:12499-12530 原版精确版：全图递归洪水+散块清除；
579	  // 曾用近似 spreadGrassAll 中心限距+2 轮快照——caves-oracle 位级对账后替换）
580	  runMudCavesPass(store, TILE_BY_KEY['mud']!, TILE_BY_KEY['v_60_jungle_grass_block']!);
581	  runDesertPass(store, rng, gs);         // 19 Full Desert
582	  runMushroomPass(store, rng, gs);       // 20 Mushroom Patches
583	  runMarbleGranitePass(store, rng, gs);  // 21/22 Marble/Granite
584	  runFloatingIslandsPass(store, rng, gs); // 23 Floating Islands（原在蘑菇前——注册序修正）
585	  runDirtToMudAndSiltPass(store, rng, gs); // 24 Dirt To Mud / 25 Silt
586	  runShiniesPass(store, rng, gs);        // 26 Ores And Shinies（原在很后"矿石"槽——移到 Silt 后=Webs 位）
587	  runVanillaWebsPass(store, rng, gs);     // 27 Webs（cs:13659——原后置防被清，注册序修正回 27 位）
588	  runUnderworldPass(store, rng, gs);     // 28 Underworld（cs:13697——原管线末"地狱"槽；
589	                                        //  地狱屋/地狱箱/熔炉等依赖槽在数组其后 = 地狱 pass 之后 ✓）
590	  runCorruptionPass(store, rng, gs);     // 29 Corruption/Crimson
591	  runLakesPass(store, rng, gs);          // 30 Lakes（cs:14613——原"液体"槽在结构段后，注册序修正）
592	  runSlushPass(store, gs);               // 31 StoneToIceAndSiltPlusMudIntoSlush（cs:14756，紧随 Lakes）
593	  runDungeonPass(store, rng, gs, world.chests); // 32 Dungeon(蓝/粉砖主题+走廊房间+宝箱)
594	  // 地牢 pass 预计算会重掷 dungeonLocation(锚点 ±300 拒绝采样后迁移)——必须在此后
595	  // 回写最终位置,否则 world.dungeonX 停留在 Reset 期的旧值(与实际地牢偏差可达数百格)。
596	  // 优先取入口门厅可站立点(原版 dungeonX/Y 语义 cs L72510-72527:入口结构上可站处,
597	  // 守卫老人出生/游走锚)——塔心锚点会把老人漏进塔内
598	  world.dungeonX = gs.dungeonEntX || gs.dungeonLocation;
599	  world.dungeonY = gs.dungeonEntY || gs.dungeonY || 0;
600	  // 33 MountainCaveOpenings + 34 Beaches（原紧跟 SurfaceCaves——注册序修正移到 Dungeon 后）
601	  runMountainCavesPass(store, rng, gs);
602	  runBeachesPass(store, rng, gs);
603	  // 海盆挖完后刷新 surface[](后续旧 pass 依赖;本函数之后才到那些 pass)
604	  for (let x = 0; x < store.w; x++) {
605	    for (let y = 0; y < store.h; y++) {
606	      if (store.flags[store.idx(x, y)]) { surface[x] = y; break; }
607	    }
608	  }
609	  runGemsPass(store, rng, gs);           // 35 Gems（原捆绑在 Lakes 槽——注册序修正移到 Beaches 后）
610	  // 原版 1456 注册序（WorldGen.cs 行号 = 唯一权威，2026-08-11 review 依此重排）：
611	  //   OceanCaves(15228) < Pyramids(15426) < SurfaceWaterInJungle(15887) <
612	  //   Temple(15911) < Beehives(16005) < JungleShrines(16059) < Statues(16947) <
613	  //   UndergroundHouses+BuriedChests(17066) < SurfaceChests(17226) <
614	  //   ChestsInJungleShrines(17308) < UnderwaterChests(17343) < SpiderCaves(17455) <
615	  //   FloatingIslandHouses(17971) < MicroBiomes(21785)
616	  // 神庙/灌水提前到宝箱系之前（原版语义:大结构先占位,箱/雕像后放才不会塞进
617	  // 神庙体内或被灌水淹没;此前神庙在蜘蛛洞后 → 占地区内已塞雕像/箱,放置互相破坏）。
618	  const oceanTreasures = runOceanCavesPass(store, rng, gs); // 海洋洞窟蠕虫+宝藏点记录
619	  runPyramidPass(store, rng, gs, world.chests); // Pyramids(沙岩砖金字塔+宝箱)
620	  // 原版注册序 Pyramids(15426) < LivingTrees(15551) < LivingTreeWalls(15792) <
621	  // SurfaceWaterInJungle(15887)——世界树插在金字塔后、丛林灌水前（方案 A 原版位置）。
622	  // LivingTrees：GrowLivingTree 树干壳+枝叶+根系+贯通竖井+密室宝箱；LivingTreeWalls：
623	  // 全图 type==191 连通核补墙 244（零掷骰）。
624	  runLivingTreesPass(store, rng, gs, world.chests);  // Living Trees(世界树)
625	  runLivingTreeWallsPass(store, gs);                 // Living Tree Walls(活木墙)
626	  runWetJunglePass(store, rng, gs);             // SurfaceWaterInJungle(1456 cs:15887 逐列灌水,零 RNG)
627	  runTemplePass(store, rng, gs, world.chests);  // Jungle Temple(之字形房间链+走廊+门+宝箱)
628	  runBeehivePass(store, rng, gs);               // Hives(丛林蜂巢:蜂巢壳+蜂蜜+腔)
629	  const shrineSpots = runJungleShrinePass(store, rng, gs);  // 丛林神龛(壳+腔+火把+金字塔顶)
630	  runStatuesPass(store, rng, gs);                           // 雕像 73 序+陷阱雕像接线
631	  runBuriedChestsPass(store, rng, gs, world.chests); // Buried Chests(洞穴金/冰箱/沙箱;地狱箱已拆到地狱箱 pass)
632	  runCaveHousesPass(store, rng, gs, world.chests);   // 地下小屋七主题(木/冰/丛林/沙/花岗岩/大理石/蘑菇)
633	  runSurfaceChestsPass(store, rng, gs, world.chests); // Surface Chests(地表木箱;只放一次——曾双调致密度翻倍)
634	  runJungleChestsPass(store, rng, gs, world.chests, shrineSpots); // 常春藤箱(神龛中心)
635	  runUnderwaterChestsPass(store, rng, gs, world.chests, oceanTreasures); // 海洋洞窟水箱
636	  runWaterChestsPass(store, rng, gs, world.chests); // Water Chests(水中 style17;1.4.4 概念保留)
637	  // Webs(51) 已按注册序回到 #27 位（vanillaBiomes 前段）——此处旧迟置调用删除
638	  runSpiderNestPass(store, rng, gs, world.chests); // Spider Caves(countTiles 门+波前BFS刷墙62+蛛网罐/箱/垂网/覆饰)
639	  // WebsInSpiderCavesAndHoney(cs:20140)曾内嵌于此（提前约 40 槽）——2026-08-13
640	  // 按注册序(DyePlants 20126 < 本 pass < GrassPlants 20232)拆出独立槽归位（Batch D）
641	  runIslandHousePass(store, rng, gs, world.chests); // 浮空岛日光板房屋(Skyware 门+箱+桌椅)
642	  runSwordShrinePass(store, rng, gs);          // 附魔剑圣地(竖井+水潭洞+土丘剑)
643	}
644	
645	// 原版 pass 37 Clean Up Dirt:表层墙清理 + 连通小块(<20)清除
646	function vanillaCleanup({ store, rng }: GenCtx) {
647	  const gs = ctxGs[0];
648	  if (!gs) return;
649	  runCleanupPass(store, rng, gs);
650	}
651	
652	// 生命水晶(pass 55)——清完散块后放
653	function vanillaLifeCrystals({ store, rng }: GenCtx) {
654	  const gs = ctxGs[0];
655	  if (!gs) return;
656	  runLifeCrystalsPass(store, rng, gs);
657	}
658	
659	// 原版 "Smooth World"(L7568)：地表凸起 → 半砖/削除（HalfBrickPass）
660	function halfBrickSmoothPass({ store, rng }: GenCtx) {
661	  const gs = ctxGs[0];
662	  if (!gs) return;
663	  runSmoothWorldPass(store, rng, gs);
664	}
665	
666	// 原版 "Waterfalls"(L7697)：水边唇缘砸半砖（瀑布触发来源）
667	function waterfallLipPass({ store, rng }: GenCtx) {
668	  const gs = ctxGs[0];
669	  if (!gs) return;
670	  runWaterfallLipPass(store, rng, gs);
671	}
672	
673	// 沙上清水（RemoveSurfaceWaterAboveSand cs:16295）：零掷骰
674	function surfaceWaterAboveSandPass({ store }: GenCtx) {
675	  const gs = ctxGs[0];
676	  if (!gs) return;
677	  runRemoveSurfaceWaterAboveSandPass(store, gs);
678	}
679	
680	// 薄冰（FragileIceOverIceBiomeWater cs:16756）：零掷骰
681	function fragileIcePass({ store }: GenCtx) {
682	  const gs = ctxGs[0];
683	  if (!gs) return;
684	  runFragileIcePass(store, gs);
685	}
686	
687	// 蜂巢幼虫（BeeLarvaInBeehives cs:21018）：蜂巢 pass 已登记坐标，此处放置
688	function beeLarvaPass({ store }: GenCtx) {
689	  const gs = ctxGs[0];
690	  if (!gs) return;
691	  runBeeLarvaPass(store, gs);
692	}
693	
694	// 地狱要塞 HellFort(5列×10行网格塔)——地狱层就绪后
695	function vanillaHellHouses({ store, rng }: GenCtx) {
696	  const gs = ctxGs[0];
697	  if (!gs) return;
698	  runHellFortPass(store, rng, gs);
699	}

```


---

## 🤖 Assistant · 2026-08-12T16:52:46.160Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key finding already: In vanillaBiomes, runDungeonPass (line 593) runs BEFORE runMountainCavesPass (601) and runBeachesPass (602). In vanilla, pass 32 Dungeon < 33 MountainCaveOpenings < 34 Beaches — so beaches run AFTER dungeon. This means beach sand placement can overwrite dungeon entrance. Also GravitatingSand pass 36 in vanilla runs after Beaches — in our pipeline, GravitatingSandPass runs in "引力沙" slot which is way earlier (before Shimmer and after liquid settle)... wait, actually gravitatingSandPass is in the pass list at index ~4 (line 75), which runs BEFORE vanillaBiomes. Wait no — order in passes array: 原版地形 (vanillaTerrain), 沙丘 (dunes), 洞穴 (caves), 生物群系 (biomes), 液体, 引力沙, 微光, 清理...

Wait — 引力沙 is after 生物群系. Since dungeon is inside vanillaBiomes (slot 3), gravitating sand runs AFTER dungeon. Yes: passes array order: 0 terrain, 1 dunes, 2 caves, 3 biomes (includes dungeon at 593, then mountain caves, beaches, gems, ocean caves, pyramids, ... structures), 4 vanillaLakes (empty shell), 5 gravitatingSandPass, 6 shimmer, 7 cleanup, ...

So after dungeon: Beaches (602), Gems, OceanCaves, Pyramids, Living trees, temple, etc (all within biomes), then gravitatingSand, cleanup, etc.

Also ocean sand (runOceanSandPass) runs in vanillaCaves slot, which is BEFORE biomes/dungeon. Fine.

But wait — dunes pass runs at slot 1 (vanillaDunes → runDunesPass) which is before dungeon. And desert runs inside biomes before dungeon. So post-dungeon sand mechanisms: runBeachesPass (602), GravitatingSandPass (slot 5), FinalCleanup (sandstone/hardened sand walls with lava?), PilesPass (slot "矿骨堆" — piles can place sand? Let me check), BeachDecor (ShellPiles cs:16385, slot "海滩装饰" line 97), Oasis (slot 92) — oasis digs ponds + shoreline; could place sand near desert only. Also CactusCoral (structures: palm trees in sand, coral) — doesn't place sand presumably.

Also SurfaceDecorPasses might place sand. Let me grep for sand tile placements across gen dir.

Now let's read the key files: DungeonPass precalc (lines ~80-200), BeachPass full, GravitatingSandPass, DunesPass, PilesPass, DesertPass, CleanupPass, FinalCleanupPass, TerrainPass. And grep for tileDungeon/wallDungeon gating.

Let me find tile ids: sand, hardened sand, sandstone, desert fossil keys. Let me grep TILE_BY_KEY usage of 'sand' etc.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:52:46.340Z · glm-x-preview-260804

```
Now let me read the key passes in parallel.
```


---

## 🤖 Assistant · 2026-08-12T16:52:46.564Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts",
 "limit": 260,
 "offset": 1
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:46.582Z

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
108	  // ---- 1456 入口位置预计算(DungeonCrawler.cs L280-326):锚点 ±300 内拒绝采样地表点
109	  // (从 y=10 下扫到首个"有内容"格:实心/液体/墙),校验无云块(±15 方框 + 上方 50 带)
110	  // 与头顶余量(ny-40-RoughHeight40>0);成功则锚点迁移到入口旁(±25),爬升改为
111	  // 沿直线分段走向入口(Precalculated),否则回退 legacy 盲爬。根治:盲爬探测点落在
112	  // 高坡时楼梯被迫越坡堆积、后一次外壳埋掉前一次挖空 → 实心砖瘤封死下行通道 ----
113	  let entPos: [number, number] | null = null;
114	  {
115	    const CLOUD = new Set<number>(
116	      ['v_189_cloud_block', 'v_196_rain_cloud_block', 'v_460_snow_cloud_block']
117	        .map((k) => TILE_BY_KEY[k])
118	        .filter((v): v is number => v !== undefined),
119	    );
120	    let found = false, nx = 0, ny = 0;
121	    for (let t = 0; t < 3000 && !found; t++) {
122	      nx = gs.dungeonLocation - 300 + rng.int(0, 599);
123	      if (nx <= gs.beachDistance || nx >= w - gs.beachDistance) continue;
124	      ny = 10;
125	      while (ny < st.h - 2) {
126	        const i = st.idx(nx, ny);
127	        if (st.flags[i] || st.liquid[i] > 0 || st.wall[i] > 0) break;
128	        ny++;
129	      }
130	      let cloud = false;
131	      for (let dx = -15; dx <= 15 && !cloud; dx++) {
132	        for (let dy = -15; dy <= 15; dy++) {
133	          if (st.inBounds(nx + dx, ny + dy) && CLOUD.has(st.type[st.idx(nx + dx, ny + dy)])) { cloud = true; break; }
134	        }
135	      }
136	      for (let dx = -50; dx < 50 && !cloud; dx++) {
137	        for (let y = Math.max(50, ny - 50); y < ny; y++) {
138	          if (st.inBounds(nx + dx, y) && CLOUD.has(st.type[st.idx(nx + dx, y)])) { cloud = true; break; }
139	        }
140	      }
141	      if (cloud || ny - 80 <= 0) continue;
142	      found = true;
143	    }
144	    if (found) {
145	      gs.dungeonLocation = nx + 25 - rng.int(0, 49);
146	      entPos = [nx, ny];
147	    }
148	  }
149	  const x0 = gs.dungeonLocation;
150	  if (x0 < 30 || x0 > w - 30) return;
151	  // 原版主题在 **Dunes pass 头**已掷（SetupDungeonGenVarVariables，cs:11542）；
152	  // 此处只消费 gs.dungeonTheme（-1=非原版管线直调时回退自掷）
153	  const theme = gs.dungeonTheme >= 0 ? gs.dungeonTheme : rng.int(0, 2);
154	  const brick = theme === 0 ? BLUE : theme === 1 ? GREEN : PINK;
155	  const wallId = brick === BLUE ? 7 : brick === GREEN ? 8 : 9;
156	  // 深度:找实心(L6565)
157	  let y0 = Math.floor((gs.worldSurface + gs.rockLevel) / 2) + rng.int(-200, 199);
158	  let solid = false;
159	  for (let d = 0; d < 10; d++) if (st.flags[st.idx(x0, y0 + d)]) { solid = true; break; }
160	  if (!solid) {
161	    const cap = Math.floor((gs.worldSurface + gs.rockLevel) / 2) + 200;
162	    while (y0 < cap && !st.flags[st.idx(x0, y0 + 10)]) y0++;
163	  }
164	  y0 = Math.max(gs.worldSurface + 10, Math.min(h - 220, y0));
165	  const dc = new DungeonCtx(brick, wallId, x0, y0);
166	  dc.shelfStyles = shelfStyles;
167	  dc.lanternStyles = lanternStyles;
168	  // 原版 L18045-18048:入口塔尺寸强度(DungeonEnt 与竖井出口探测共用)
169	  dc.dxS1 = rng.int(25, 29); dc.dyS1 = rng.int(20, 24);
170	  dc.dxS2 = rng.int(35, 49); dc.dyS2 = rng.int(10, 14);
171	  // ---- 主链随机游走(L18053)----
172	  let budget = w / 60 + rng.int(0, Math.max(1, Math.floor(w / 180)));
173	  let dx = x0, dy = y0;
174	  dungeonRoom(st, rng, gs, dc, dx, dy);
175	  let step5 = 5;
176	  while (budget > 0) {
177	    dc.updateBBox(dx, dy);
178	    budget--;
179	    step5--;
180	    if (step5 === 0 && rng.next() * 3 < 1) {
181	      step5 = 5;
182	      if (rng.next() < 0.5) {
183	        // 分支:保存位置→走廊(可能两条)+房→恢复
184	        const sx = dx, sy = dy;
185	        [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
186	        if (rng.next() < 0.5) [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
187	        dungeonRoom(st, rng, gs, dc, dx, dy);
188	        dx = sx; dy = sy;
189	      } else {
190	        dungeonRoom(st, rng, gs, dc, dx, dy);
191	      }
192	    } else {
193	      [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, false);
194	    }
195	  }
196	  dungeonRoom(st, rng, gs, dc, dx, dy);
197	  // ---- 爬升到地表(1456 语义,DungeonCrawler.cs L400-449):上限 100;num8 到 0 后
198	  // 每轮 1/5 概率 halls(forceX)+room 分支(原版 num8 保持在 0) ----
199	  let best = dc.rooms[0];
200	  for (const r of dc.rooms) if (r.t < best.t) best = r;
201	  dc.entranceX = best.cx;
202	  dx = best.cx; dy = best.cy;
203	  if (entPos) {
204	    // 预计算模式:沿直线分段走向入口,每段 10-29 步,剩余距离耗尽即达(确定性终止)
205	    let remaining = Math.hypot(entPos[0] - dx, entPos[1] - dy);
206	    let delay = 5, guard = 0;
207	    while (remaining > 0 && guard++ < 100) {
208	      if (delay > 0) delay--;
209	      if (delay === 0 && rng.next() < 0.2 && dy > gs.worldSurface + 100) {
210	        delay = 10;
211	        const sx = dx, sy = dy;
212	        [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, true);
213	        dungeonRoom(st, rng, gs, dc, dx, dy);
214	        dx = sx; dy = sy;
215	      }
216	      let steps = rng.int(10, 29);
217	      if (steps > remaining) steps = Math.max(1, Math.floor(remaining));
218	      const d = Math.hypot(entPos[0] - dx, entPos[1] - dy) || 1;
219	      const res = dungeonStairs(st, rng, gs, dc, dx, dy, {
220	        vx: (entPos[0] - dx) / d, vy: (entPos[1] - dy) / d, steps,
221	      });
222	      dx = res[0]; dy = res[1];
223	      remaining -= steps;
224	    }
225	    dx = entPos[0]; dy = entPos[1];
226	    dungeonEnt(st, rng, gs, dc, dx, dy);
227	    gs.dungeonY = entPos[1];   // 入口地表 Y（刷怪门槛 CheckToSpawnDungeonEnemies）
228	  } else {
229	    // legacy 盲爬(1405 结构 + 1456 的 100 上限):外壳探测到开放天空即停
230	    let reached = false;
231	    let delay = 5, guard = 0;
232	    while (!reached && guard++ < 100) {
233	      if (delay > 0) delay--;
234	      if (delay === 0 && rng.next() < 0.2 && dy > gs.worldSurface + 100) {
235	        delay = 10;
236	        const sx = dx, sy = dy;
237	        [dx, dy] = dungeonHalls(st, rng, gs, dc, dx, dy, true);
238	        dungeonRoom(st, rng, gs, dc, dx, dy);
239	        dx = sx; dy = sy;
240	      }
241	      const res = dungeonStairs(st, rng, gs, dc, dx, dy);
242	      dx = res[0]; dy = res[1];
243	      reached = res[2];
244	    }
245	    // 兜底:楼梯没到地表则从当前位置直挖竖井到地表(垂直,保证衔接)
246	    if (dy > gs.worldSurface - 5) {
247	      let sx2 = dx, sy2 = dy;
248	      let guard2 = 0;
249	      while (sy2 > gs.worldSurface - 5 && guard2++ < 800) {
250	        for (let ax = -3; ax <= 3; ax++) {
251	          for (let ay = -3; ay <= 3; ay++) {
252	            if (!st.inBounds(sx2 + ax, sy2 + ay)) continue;
253	            const i = st.idx(sx2 + ax, sy2 + ay);
254	            st.flags[i] = 0; st.wall[i] = dc.wall;
255	          }
256	        }
257	        for (let ax = -4; ax <= 4; ax++) {
258	          for (let ay = -4; ay <= 4; ay++) {
259	            if (!st.inBounds(sx2 + ax, sy2 + ay)) continue;
260	            const i = st.idx(sx2 + ax, sy2 + ay);

```


---

## 🤖 Assistant · 2026-08-12T16:52:46.718Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:46.731Z

**📎 ToolResult**

```
1	// 原版 pass 3 "Ocean Sand"(L4962) + pass 33 "Beaches"(L6639) 移植。
2	// Ocean Sand:海滩区地表按深度随机走铺沙(50-200),顺手记录金字塔候选;
3	// Beaches:从海滩边缘挖出斜坡海盆( TuneOceanDepth 深度曲线),灌水,清墙,盆底铺沙。
4	// 原版固定 tile 常量按 4200 宽设计,此处按 w/4200 线性缩放保持比例(大世界 = 精确原版)。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T } from '../../../data/tiles';
9	
10	/** Ocean Sand:海滩铺沙 + 金字塔候选(L4962-5042) */
11	export function runOceanSandPass(st: TileStore, rng: RNG, gs: GenState): void {
12	  const w = st.w;
13	  for (let i = 0; i < 3; i++) {
14	    // 拒绝采样:中部 40%-60% 区间的起点重掷(原版 while 循环)
15	    let x0 = rng.int(0, w - 1);
16	    while (x0 > w * 0.40 && x0 < w * 0.60) x0 = rng.int(0, w - 1);
17	    let left = rng.int(35, 89);
18	    if (i === 1) left += Math.floor(rng.int(20, 39) * (w / 4200));
19	    if (rng.next() * 3 < 1) left *= 2;
20	    if (i === 1) left *= 2;
21	    let right = rng.int(35, 89);
22	    if (rng.next() * 3 < 1) right *= 2;
23	    if (i === 1) right *= 2;
24	    let x1 = x0 - left, x2 = x0 + right;
25	    if (x1 < 0) x1 = 0;
26	    if (x2 > w) x2 = w;
27	    if (i === 1) continue; // 中段跳过(原版 case 1: continue)
28	    if (i === 0) { x1 = 0; x2 = gs.beachLeftEnd; }
29	    if (i === 2) { x1 = gs.beachRightStart; x2 = w; }
30	    // 沙层厚度随机走(50-200)
31	    let depth = rng.int(50, 99);
32	    for (let x = x1; x < x2; x++) {
33	      if (rng.next() < 0.5) {
34	        depth += rng.int(-1, 1);
35	        if (depth < 50) depth = 50;
36	        if (depth > 200) depth = 200;
37	      }
38	      // 列深度上界（cs:11682）：double 比较 (wS+rockLayer)/2.0，奇和时多扫一行
39	      const depthScan = (gs.worldSurface + gs.rockLevel) / 2;
40	      for (let y = 0; y < depthScan; y++) {
41	        const ii = st.idx(x, y);
42	        if (!st.flags[ii]) continue;
43	        // 中点列金字塔候选（cs:11685-11691）：Next(6)==0 时登记 PyrX/PyrY
44	        //（此前缺失→每侧少 1 颗骰 + 海洋金字塔候选丢失=流错位+内容缺）
45	        if (x === Math.trunc((x1 + x2) / 2) && rng.nextIntRange(0, 6) === 0) {
46	          gs.pyramidSpots.push({ x, y });
47	        }
48	        const edge = Math.min(depth, x - x1, x2 - x);
49	        const thick = edge + rng.int(0, 4);
50	        for (let y2 = y; y2 < y + thick && y2 < st.h; y2++) {
51	          const jj = st.idx(x, y2);
52	          if (x > x1 + rng.int(0, 4) && x < x2 - rng.int(0, 4)) {
53	            st.type[jj] = T.SAND;
54	          }
55	        }
56	        break;
57	      }
58	    }
59	  }
60	}
61	
62	/** TuneOceanDepth(L11682):逐列深度增量曲线,阈值按世界宽度比例缩放 */
63	function tuneOceanDepth(rng: RNG, count: number, depth: number, van: number, floridaStyle: boolean): number {
64	  const inc = (f: number) => depth + rng.int(10, 19) * f;
65	  const t = (n: number) => Math.max(1, Math.floor(n * van));
66	  if (!floridaStyle) {
67	    if (count < t(3)) return inc(0.2);
68	    if (count < t(6)) return inc(0.15);
69	    if (count < t(9)) return inc(0.1);
70	    if (count < t(15)) return inc(0.07);
71	    if (count < t(50)) return inc(0.05);
72	    if (count < t(75)) return inc(0.04);
73	    if (count < t(100)) return inc(0.03);
74	    if (count < t(125)) return inc(0.02);
75	    if (count < t(150)) return inc(0.01);
76	    if (count < t(175)) return inc(0.005);
77	    if (count < t(200)) return inc(0.001);
78	    if (count < t(230)) return inc(0.01);
79	    if (count < t(235)) return inc(0.05);
80	    if (count < t(240)) return inc(0.1);
81	    if (count < t(245)) return inc(0.05);
82	    if (count < t(255)) return inc(0.01);
83	    return depth;
84	  }
85	  // florida 变体:同阈值曲线,近岸增量极小、远岸陡增(L11719-11748)
86	  if (count < t(3)) return inc(0.001);
87	  if (count < t(6)) return inc(0.002);
88	  if (count < t(9)) return inc(0.004);
89	  if (count < t(15)) return inc(0.007);
90	  if (count < t(50)) return inc(0.01);
91	  if (count < t(75)) return inc(0.014);
92	  if (count < t(100)) return inc(0.019);
93	  if (count < t(125)) return inc(0.027);
94	  if (count < t(150)) return inc(0.038);
95	  if (count < t(175)) return inc(0.052);
96	  if (count < t(200)) return inc(0.08);
97	  if (count < t(230)) return inc(0.12);
98	  if (count < t(235)) return inc(0.16);
99	  if (count < t(240)) return inc(0.27);
100	  if (count < t(245)) return inc(0.43);
101	  if (count < t(255)) return inc(0.6);
102	  return depth;
103	}
104	
105	/** Beaches:挖海盆灌水(L6639-6728) */
106	export function runBeachesPass(st: TileStore, rng: RNG, gs: GenState): void {
107	  const w = st.w;
108	  const van = w / 4200;
109	  const sc = (n: number) => Math.max(1, Math.floor(n * van)); // C# (int) 截断
110	  const oceanWaterMin = sc(220), oceanWaterMax = sc(260), forcedJungleLen = sc(275), minSand = sc(50);
111	  const edgeWall = Math.max(4, Math.floor(30 * van));
112	
113	  let floridaL = false, floridaR = false;
114	  if (rng.next() < 0.25) {
115	    if (rng.next() < 0.5) floridaL = true; else floridaR = true;
116	  }
117	
118	  for (let side = 0; side < 2; side++) {
119	    if (side === 0) {
120	      // 左海盆:从 beachLeftEnd-50 之左往世界缘挖
121	      let waterX = rng.int(oceanWaterMin, oceanWaterMax - 1);  // 原版 Next(220,260) 上界开
122	      if (gs.dungeonSide === 1) waterX = forcedJungleLen; // 丛林侧强制 275(缩放)
123	      const cap = gs.beachLeftEnd - minSand;
124	      if (waterX > cap) waterX = Math.max(2, cap);
125	      // 该列地表
126	      let surfY = 0;
127	      while (!st.flags[st.idx(waterX - 1, surfY)]) surfY++;
128	      gs.shellStartYLeft = surfY; // cs:14996：ShellPiles 锚点 Y（waterY 调整前的地表值）
129	      const waterY = surfY + rng.int(1, 4);
130	      let count = 0, depth = 1;
131	      for (let x = waterX - 1; x >= 0; x--) {
132	        if (x > edgeWall) { count++; depth = tuneOceanDepth(rng, count, depth, van, floridaL); }
133	        else depth += 1;
134	        const pad = rng.int(15, 19);
135	        const yEnd = Math.trunc(waterY + depth + pad); // C# (int) 截断——浮点直比会多挖一行
136	        for (let y = 0; y < yEnd && y < st.h; y++) {
137	          const i = st.idx(x, y);
138	          if (y < waterY + depth * 0.75 - 3) {
139	            // 原版仅 active(false)（cs:15014）——保留 type 幽灵（曾清零，
140	            // 与 oracle 天空/海盆幽灵分叉 6383 格）
141	            st.flags[i] = 0;
142	            if (y > waterY) { st.liquid[i] = 255; st.liquidType[i] = 1; }
143	            else if (y === waterY) {
144	              st.liquid[i] = 127; st.liquidType[i] = 1;
145	              // cs:15025-15027：首个到达水线分支的列 = ShellPiles 锚点 X（仅首次）
146	              if (gs.shellStartXLeft === 0) gs.shellStartXLeft = x;
147	            }
148	          } else if (y > waterY) {
149	            st.type[i] = T.SAND; st.flags[i] = 1;
150	          }
151	          st.wall[i] = 0;
152	        }
153	      }
154	    } else {
155	      // 右海盆:镜像
156	      let waterX = w - rng.int(oceanWaterMin, oceanWaterMax - 1);  // 上界开,同原版 Next
157	      if (gs.dungeonSide === -1) waterX = w - forcedJungleLen;
158	      const cap = gs.beachRightStart + minSand;
159	      if (waterX < cap) waterX = Math.min(w - 2, cap);
160	      let surfY = 0;
161	      while (!st.flags[st.idx(waterX, surfY)]) surfY++;
162	      gs.shellStartXRight = 0;            // cs:15060：显式清零（左值不串扰，1:1）
163	      gs.shellStartYRight = surfY;        // cs:15061
164	      const waterY = surfY + rng.int(1, 4);
165	      let count = 0, depth = 1;
166	      for (let x = waterX; x < w; x++) {
167	        if (x < w - edgeWall) { count++; depth = tuneOceanDepth(rng, count, depth, van, floridaR); }
168	        else depth += 1;
169	        const pad = rng.int(15, 19);
170	        const yEnd = Math.trunc(waterY + depth + pad); // C# (int) 截断——浮点直比会多挖一行
171	        for (let y = 0; y < yEnd && y < st.h; y++) {
172	          const i = st.idx(x, y);
173	          if (y < waterY + depth * 0.75 - 3) {
174	            // 原版仅 active(false)（cs:15014）——保留 type 幽灵（曾清零，
175	            // 与 oracle 天空/海盆幽灵分叉 6383 格）
176	            st.flags[i] = 0;
177	            if (y > waterY) { st.liquid[i] = 255; st.liquidType[i] = 1; }
178	            else if (y === waterY) {
179	              st.liquid[i] = 127; st.liquidType[i] = 1;
180	              // cs:15090-15092：首个到达水线分支的列 = ShellPiles 锚点 X（仅首次）
181	              if (gs.shellStartXRight === 0) gs.shellStartXRight = x;
182	            }
183	          } else if (y > waterY) {
184	            st.type[i] = T.SAND; st.flags[i] = 1;
185	          }
186	          st.wall[i] = 0;
187	        }
188	      }
189	    }
190	  }
191	}
192	
193	// ---- 原版 ShellPiles pass（WorldGen.cs:16393-16501）+ ShellPile 方法（cs:10307-10420）----
194	// 每侧 50% 概率；先在 shellStart±20/±10 盒内找"水线接触点"（活性沙 + 上方空且无水 +
195	// 海侧邻格有水），Y-=50 后以原版偏移区间最多 6 堆；ShellPile：沙面上逐像素
196	// 椭圆（半径每像素掷 Next(70,91)*0.01）填 tile 495（贝壳堆块），下方悬空逐层补
197	// 495→沙 53→硬化沙 397（cs:10350-10403）。锚点与深度门均为 worldSurface（地表内）——
198	// 曾放宽 +120 并自创锚点 = 深水海盆冒出孤立沙堆（2026-08-12 修复）。
199	import { TILE_BY_KEY, TILE_DEFS } from '../../../data/tiles';
200	
201	/** WorldGen.SolidTile：active && tileSolid（cs:70037 区；生成期无 inActive） */
202	function solidTile(st: TileStore, x: number, y: number): boolean {
203	  if (!st.inBounds(x, y)) return false;
204	  const i = st.idx(x, y);
205	  if (!st.flags[i]) return false;
206	  const d = TILE_DEFS[st.type[i]];
207	  return !!d && d.solid;
208	}
209	
210	/** 原版只写 type/active/halfBrick/slope（cs:10350-10403），不动 frame（后续整帧 pass 刷） */
211	function putPile(st: TileStore, x: number, y: number, type: number): void {
212	  if (!st.inBounds(x, y)) return;
213	  const i = st.idx(x, y);
214	  st.type[i] = type; st.flags[i] = 1; st.half[i] = 0; st.slope[i] = 0;
215	}
216	
217	function inactive(st: TileStore, x: number, y: number): boolean {
218	  return !st.inBounds(x, y) || !st.flags[st.idx(x, y)];
219	}
220	
221	function shellPile(st: TileStore, rng: RNG, X: number, Y: number, worldSurface: number): boolean {
222	  if (!st.inBounds(X, Y)) return false;               // InWorld(X,Y)
223	  let num = Y;
224	  while (!solidTile(st, X, num)) {
225	    num++;
226	    if (num > worldSurface) return false;             // cs:10338：下探过 worldSurface 即弃
227	  }
228	  if (st.type[st.idx(X, num)] !== T.SAND) return false;   // 必须沙面
229	  if (st.wall[st.idx(X, num)] !== 0) return false;        // 无背景墙
230	  num--;
231	  const SHELL = TILE_BY_KEY['v_495_shell_pile_block'] ?? 0;
232	  const HARD_SAND = TILE_BY_KEY['hardened_sand'] ?? 0;
233	  if (!SHELL) return false;
234	  let cx = X, cy = num;
235	  let vx = rng.next() * 0.6 - 0.3, vy = rng.next() * 0.5 + 0.5;
236	  let radius = rng.int(2, 3);                         // Next(2,4)
237	  if (rng.int(0, 9) === 0) radius += 1;               // Next(10)==0
238	  let layers = rng.int(3, 5);                         // Next(3,6)
239	  while (layers-- > 0) {
240	    for (let i = X - radius * 4; i <= X + radius * 4; i++) {
241	      for (let num4 = num + radius * 4; num4 > num - radius * 4; num4--) {
242	        // cs:10358：每像素掷一次半径抖动（Next(70,91) 上界开）
243	        const r = radius * rng.int(70, 90) * 0.01;
244	        const dx = (cx - i) * 0.6, dy = cy - num4;    // Vector2D.X 分量 ×0.6
245	        if (Math.sqrt(dx * dx + dy * dy) >= r) continue;
246	        if (num4 <= num + 1 || rng.int(0, 5) === 0) { // Next(6)==0
247	          putPile(st, i, num4, SHELL);
248	          // 下方悬空补壳/沙/硬化沙（cs:10363-10399 三层下探，条件仅看 active）
249	          if (inactive(st, i, num4 + 1)) {
250	            putPile(st, i, num4 + 1, SHELL);
251	            if (inactive(st, i, num4 + 2)) {
252	              putPile(st, i, num4 + 2, T.SAND);
253	              if (inactive(st, i, num4 + 3)) putPile(st, i, num4 + 3, HARD_SAND);
254	            }
255	          }
256	        } else if (st.inBounds(i, num4) && st.type[st.idx(i, num4)] !== SHELL) {
257	          putPile(st, i, num4, T.SAND);
258	        }
259	      }
260	    }
261	    cx += vx; cy += vy;
262	    vx += rng.next() * 0.2 - 0.1; vy += rng.next() * 0.2 - 0.1;
263	    vx = Math.max(-0.3, Math.min(0.3, vx));           // Utils.Clamp
264	    vy = Math.max(0.5, Math.min(1.0, vy));
265	  }
266	  return true;
267	}
268	
269	/** 海滩装饰 = 原版 ShellPiles 段（cs:16393-16501；海藻不在此——由 Lilypads pass 的
270	 *  GrowCheckSeaweed 承担，cs:22177-22192 全列上扫）。
271	 *  注意：本 pass 在原版注册序中先于 SmoothWorld（cs:16385 < 16507），管线里须排在
272	 *  "半砖平滑"之前，否则堆出的散沙无人回收（两侧悬空孤立单格清理在平滑 pass）。 */
273	export function runBeachDecorPass(st: TileStore, rng: RNG, gs: GenState): void {
274	  if (gs.seedFlags.notTheBees) return;                // cs:16393：蜜蜂世界整段跳过（零掷骰）
275	  const spawn = (x: number, y: number) => shellPile(st, rng, x, y, gs.worldSurface);
276	  // ---- 左侧（cs:16399-16450）----
277	  if (rng.int(0, 1) === 0) {                          // genRand.Next(2)==0
278	    // 水线接触点盒扫描（cs:16404-16413）：活性沙 + 上方空且无液 + 海侧（左）邻格有水
279	    for (let j = gs.shellStartXLeft - 20; j <= gs.shellStartXLeft + 20; j++) {
280	      for (let k = gs.shellStartYLeft - 10; k <= gs.shellStartYLeft + 10; k++) {
281	        if (!st.inBounds(j, k) || !st.inBounds(j - 1, k) || !st.inBounds(j, k - 1)) continue;
282	        const i = st.idx(j, k);
283	        if (st.flags[i] && st.type[i] === T.SAND
284	          && !st.flags[st.idx(j, k - 1)] && st.liquid[st.idx(j, k - 1)] === 0
285	          && !st.flags[st.idx(j - 1, k)] && st.liquid[st.idx(j - 1, k)] > 0) {
286	          gs.shellStartXLeft = j; gs.shellStartYLeft = k;  // 后命中者胜
287	        }
288	      }
289	    }
290	    gs.shellStartYLeft -= 50;                         // cs:16415
291	    gs.shellStartXLeft -= rng.int(0, 4);              // Next(5)
292	    if (rng.int(0, 1) === 0) gs.shellStartXLeft -= rng.int(0, 9);    // Next(10)
293	    if (rng.int(0, 2) === 0) gs.shellStartXLeft -= rng.int(0, 14);   // Next(15)
294	    if (rng.int(0, 3) !== 0) spawn(gs.shellStartXLeft, gs.shellStartYLeft);  // Next(4)!=0
295	    const maxValue = rng.int(2, 3);                   // Next(2,4)
296	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXLeft - rng.int(10, 34), gs.shellStartYLeft);
297	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXLeft - rng.int(40, 64), gs.shellStartYLeft);
298	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXLeft - rng.int(70, 94), gs.shellStartYLeft);
299	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXLeft - rng.int(100, 124), gs.shellStartYLeft);
300	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXLeft + rng.int(10, 24), gs.shellStartYLeft);
301	  }
302	  // ---- 右侧（cs:16451-16501）：镜像；邻格判海侧（右 = j+1）----
303	  if (rng.int(0, 1) === 0) {
304	    for (let j = gs.shellStartXRight - 20; j <= gs.shellStartXRight + 20; j++) {
305	      for (let k = gs.shellStartYRight - 10; k <= gs.shellStartYRight + 10; k++) {
306	        if (!st.inBounds(j, k) || !st.inBounds(j + 1, k) || !st.inBounds(j, k - 1)) continue;
307	        const i = st.idx(j, k);
308	        if (st.flags[i] && st.type[i] === T.SAND
309	          && !st.flags[st.idx(j, k - 1)] && st.liquid[st.idx(j, k - 1)] === 0
310	          && !st.flags[st.idx(j + 1, k)] && st.liquid[st.idx(j + 1, k)] > 0) {
311	          gs.shellStartXRight = j; gs.shellStartYRight = k;
312	        }
313	      }
314	    }
315	    gs.shellStartYRight -= 50;                        // cs:16465
316	    gs.shellStartXRight += rng.int(0, 4);             // Next(5)
317	    // cs:16468/16472 原版复制粘贴怪癖：右侧 ±10/±15 调整误写 shellStartXLeft。
318	    // 该值此后无人再读（全仓仅本 pass 消费），保留掷骰与写法以维持 RNG 流一致。
319	    if (rng.int(0, 1) === 0) gs.shellStartXLeft += rng.int(0, 9);
320	    if (rng.int(0, 2) === 0) gs.shellStartXLeft += rng.int(0, 14);
321	    if (rng.int(0, 3) !== 0) spawn(gs.shellStartXRight, gs.shellStartYRight);
322	    const maxValue = rng.int(2, 3);
323	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXRight + rng.int(10, 34), gs.shellStartYRight);
324	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXRight + rng.int(40, 64), gs.shellStartYRight);
325	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXRight + rng.int(70, 94), gs.shellStartYRight);
326	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXRight + rng.int(100, 124), gs.shellStartYRight);
327	    if (rng.int(0, maxValue - 1) === 0) spawn(gs.shellStartXRight - rng.int(10, 24), gs.shellStartYRight);
328	  }
329	}
330	

```


---

## 🤖 Assistant · 2026-08-12T16:52:56.446Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Very important: runBeachesPass runs AFTER runDungeonPass (WorldGen.ts:593 → 602). And runBeachesPass converts everything below waterY+depth*0.75-3 in the ocean basin into SAND, with NO dungeon tile gating (lines 148-150, 183-185). Also it CLEARS walls (st.wall[i] = 0 at line 151/186), which would strip dungeon walls. The beach carving extends from waterX-1 down to 0 (left side). waterX is capped at gs.beachLeftEnd - minSand (minSand = 50 * van). So carving can reach x=0, i.e., inland all the way to world edge — but actually carving proceeds leftward from waterX to 0, so it affects columns < waterX. waterX <= beachLeftEnd - 50.

So the question: can the dungeon entrance be carved into the region x < beachLeftEnd? The precalc drift: nx = dungeonLocation - 300 + rng.int(0,599); check nx <= gs.beachDistance → continue. What's gs.beachDistance? Let me check GenState. And dungeonLocation initial: for side -1: rng.nextIntRange(beachLeftEnd+50, W*0.2); for side 1: rng.nextIntRange(0.8W, beachRightStart-50).

Drift: nx in [dungeonLocation-300, dungeonLocation+299]. gs.dungeonLocation = nx + 25 - rng.int(0,49) → final dungeonLocation in [nx-24, nx+25].

Guard is only nx <= gs.beachDistance. If gs.beachDistance is e.g. 250 (vanilla-ish?) then nx >= 251 minimum... wait guard says `if (nx <= gs.beachDistance ...) continue;` so nx must be > beachDistance. So nx >= beachDistance+1. Then dungeonLocation >= beachDistance - 23ish.

But beachLeftEnd is typically 320-380. If beachDistance < beachLeftEnd - 50, then dungeon entrance could be placed inside the beach basin region (x < waterX cap = beachLeftEnd-50), and runBeachesPass would later carve sand over it. Need to check gs.beachDistance value in GenState.ts.

Also TerrainPass beach flattening. Let me read GenState.ts, TerrainPass.ts, GravitatingSandPass.ts, DunesPass.ts, PilesPass.ts, DesertPass.ts, CleanupPass.ts, FinalCleanupPass.ts. And grep for tileDungeon/wallDungeon gating and T.SAND placements.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:52:56.608Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GenState.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:56.625Z

**📎 ToolResult**

```
1	// 原版生成管线共享状态（对应 WorldGen.GenerateWorld 闭包变量 L4694-4741 + Reset pass 掷的骰子）。
2	// 105 个 pass 按序读写,顺序不可调换。
3	import type { SeedFlags } from '../SeedEasterEggs';
4	
5	export interface GenState {
6	  // 世界常量（Reset / Terrain pass 输出）
7	  /** 世界种子 int（translateSeed 产物；DesertHive 的 FastRandom(seed).WithModifier(57005) 消费） */
8	  seed: number;
9	  /** 彩蛋种子旗标（SeedEasterEggs.parseSeed 灌入；vanillaTerrain 开头赋值）。
10	   *  原版经 Main.drunkWorld/anniversaryWorld 等 WorldGen.* 静态消费——pass 内
11	   *  特殊种子分支读它（如 GemPasses 宝石掷骰的 tenthAnniversary/drunkWorld 门）。 */
12	  seedFlags: SeedFlags;
13	  worldSurface: number;   // 平均地表 y（tile）
14	  worldSurfaceLow: number;
15	  worldSurfaceHigh: number;
16	  rockLevel: number;
17	  rockLevelLow: number;
18	  rockLevelHigh: number;
19	  waterLine: number;      // 雪原上方（原版 waterLine ≈ 0.35×h）
20	  lavaLine: number;       // 地狱顶（原版 ≈ h-200）
21	  beachDistance: number;
22	  /** GenVars.worldSurface/rockLayer：Terrain 游走**终值**（double，≠ Main.worldSurface
23	   *  的 worldSurfaceHigh+25；SandPatches/SmallHoles/Tunnels 等按 GenVars 值掷骰） */
24	  genWorldSurface: number;
25	  genRockLayer: number;
26	  /** GenVars.worldSurfaceHigh 原始 double（≠ floor 版 worldSurfaceHigh；
27	   *  SmallHoles/DirtLayerCaves/SurfaceCaves 的拒绝判定与首实心行上界用它比较） */
28	  genWorldSurfaceHigh: number;
29	  /** Tunnels pass 记录（cs:11743：numTunnels ≤ maxTunnels-1；tunnelX[5] 存档用） */
30	  tunnelX: number[];
31	  numTunnels: number;
32	
33	  // Reset pass 掷的世界级选择
34	  crimson: boolean;           // 50% 猩红 / 50% 腐化
35	  oreTiers: { copper: number; iron: number; silver: number; gold: number }; // 含替代 id
36	  dungeonSide: 1 | -1;        // 地牢在地图哪侧
37	  dungeonX: number;           // 地牢位置（Reset num4：仅作雪原中心）
38	  dungeonLocation: number;    // 地牢入口实际位置（Reset 末掷）
39	  /** 地牢主题（Dunes pass 头 DungeonCrawler.SetupDungeonGenVarVariables 掷 Next(3)，
40	   *  cs:11542+DungeonCrawler.cs:56——掷骰时点在 Dunes，不在 Dungeon pass；-1=未掷） */
41	  dungeonTheme: number;
42	  dungeonY: number;           // 地牢入口地表 Y（DungeonPass 回填；刷怪门槛 dungeonY+40 用）
43	  dungeonEntX: number;        // 入口门厅可站立点 X（DungeonPass 回填；原版 dungeonX 语义=老头锚）
44	  lAltarX: number;             // 神庙祭坛 3×2 左上角（GenVars.lAltarX/Y 语义；-1=未放置）
45	  lAltarY: number;
46	  dungeonEntY: number;        // 入口门厅可站立点 Y
47	  jungleX: number;            // 丛林（与地牢异侧）
48	  snowOriginLeft: number;
49	  snowOriginRight: number;
50	  beachLeftEnd: number;       // 左海滩右界（Reset L4880 掷，Ocean Sand/Beaches 消费）
51	  beachRightStart: number;    // 右海滩左界
52	  // ShellPiles 锚点（GenVars.shellStart{X,Y}{Left,Right}，cs:11183-11186 清零）：
53	  // Beaches pass 记录（cs:14996/15025/15060/15090），海滩装饰 pass 消费（cs:16402）
54	  shellStartXLeft: number;
55	  shellStartYLeft: number;
56	  shellStartXRight: number;
57	  shellStartYRight: number;
58	
59	  // 各 pass 记录给后续 pass 用的区域
60	  // RandomizeTreeStyle（Reset 掷）：树冠样式边界与样式（finalize 写回 world）
61	  treeX: number[];
62	  treeStyle: number[];
63	  /** 生成的树登记（{x, y=树顶, h}；finalize 写 world.trees 供砍伐整棵判定） */
64	  genTrees: Array<{ x: number; y: number; h: number }>;
65	  /** Lakes pass 记录的湖位 x（后续 pass 避让用） */
66	  lakeX: number[];
67	  // Mount Caves（pass 7）记录的山丘坐标（pass 34/Webs 消费）
68	  mCaveX: Int32Array;
69	  mCaveY: Int32Array;
70	  numMCaves: number;
71	  snowMinX: Int32Array | null; // 每行雪原左边界（C# int[]；Ice Biome pass 写）
72	  snowMaxX: Int32Array | null;
73	  snowTop: number; snowBottom: number;
74	  jungleBounds: [number, number] | null; // [minX, maxX]
75	  evilZones: Array<{ x0: number; x1: number }>;
76	  undergroundDesert: { x0: number; y0: number; x1: number; y1: number } | null;
77	
78	  // 结构候选（由早期 pass 排队、后期 pass 消费）
79	  pyramidSpots: Array<{ x: number; y: number }>;
80	  floatingIslands: Array<{ x: number; y: number; style: number; isLake: boolean }>;
81	  /** 微光以太中心（Shimmer pass cs:15301 GenVars.shimmerPosition；-1 = 未生成） */
82	  shimmerX: number;
83	  shimmerY: number;
84	  /** 沙漠蜂巢实际雕刻范围（GenVars.desertHiveHigh/Low/Left/Right，Reset 初始化
85	   *  cs:11162-11165：High=maxTilesY Low=0 Left=maxTilesX Right=0；PlaceClustersArea
86	   *  flag2 格逐点收缩 DesertHive.cs:395-397 → UpdateDesertHiveBounds cs:11004）。
87	   *  消费方：地下沙漠宝箱战利品分层（cs:36084 的 3:4 分位点） */
88	  desertHiveHigh: number;
89	  desertHiveLow: number;
90	  desertHiveLeft: number;
91	  desertHiveRight: number;
92	  /** 丛林小屋样式（Reset 掷 cs:11182 Next(5)，原值 0-4；cs:11333-11352 映射
93	   *  0→119/1→120/2→158/3→175/4→45——JungleShrinePass 复用，不再重掷） */
94	  jungleHut: number;
95	
96	  // 宝箱战利品序（AddBuriedChest 全局态,cs:11262/36165/10130）
97	  hellChestItems: number[] | null; // 每世界乱序 [274,220,112,218,3019]（首只地狱箱时掷）
98	  hellChestIdx: number;            // 地狱箱主件序游标（成功一只 +1,循环）
99	  jungleItemIdx: number;           // 常春藤箱主件序游标（JungleItemCount）
100	  gennedMahoganyWands: boolean;    // 活桃花心木法杖对已给过标记（GenVars.gennedLivingMahoganyWands）
101	
102	  // 表面装饰 pass 共享态（GenVars）
103	  /** GenVars.orePatchX/numOrePatch/maxOrePatch=50（GenVars.cs:238-242；ResetGenerator 清零 cs:8289）：
104	   *  SurfaceOreAndStone(18559) 登记，石块段与后续回避用 */
105	  orePatchX: Int32Array;
106	  numOrePatch: number;
107	  /** GenVars.logX/logY（GenVars.cs:250-252，进程级静态默认 0）：FallenLogs(18625) 50% 登记，
108	   *  Flowers(20592) 消费后置 -1 */
109	  logX: number;
110	  logY: number;
111	  /** GenVars.larvaX/larvaY（蜂巢 pass 登记，BeeLarvaInBeehives cs:21018 消费） */
112	  larvaX: number[];
113	  larvaY: number[];
114	  /** 绿洲登记（GenVars.oasisPosition/oasisWidth/numOasis，GenVars.cs:260-268；上限
115	   *  maxOasis=20）：Oasis pass（cs:16327）写，CactusPalmTreesAndCoral 头段（cs:21129-
116	   *  21153）消费——绿洲棕榈 323 / 海滨燕麦 / 绿洲植物 530（本仓库未实现，备案） */
117	  oasisX: number[];
118	  oasisY: number[];
119	  oasisW: number[];
120	  numOasis: number;
121	}
122	
123	export function newGenState(w: number, h: number): GenState {
124	  return {
125	    seed: 0,
126	    seedFlags: {},
127	    worldSurface: Math.floor(h * 0.3), worldSurfaceLow: 0, worldSurfaceHigh: 0,
128	    rockLevel: Math.floor(h * 0.42), rockLevelLow: 0, rockLevelHigh: 0,
129	    waterLine: Math.floor(h * 0.35), lavaLine: h - 200,
130	    beachDistance: 380,  // 原版 WorldGen.beachDistance = 380（cs:4102 readonly 常量，不随尺寸缩放；曾误用 w*0.06=252 → 大理石/花岗岩采样重掷范围分叉）
131	    genWorldSurface: 0, genRockLayer: 0, genWorldSurfaceHigh: 0,
132	    tunnelX: new Array(50).fill(0), numTunnels: 0,
133	    crimson: false,
134	    oreTiers: { copper: 0, iron: 0, silver: 0, gold: 0 },
135	    dungeonSide: 1, dungeonX: 0, dungeonLocation: 0, dungeonTheme: -1, dungeonY: 0, dungeonEntX: 0, dungeonEntY: 0, lAltarX: -1, lAltarY: -1, jungleX: 0,
136	    snowOriginLeft: 0, snowOriginRight: 0,
137	    beachLeftEnd: 0, beachRightStart: 0,
138	    shellStartXLeft: 0, shellStartYLeft: 0, shellStartXRight: 0, shellStartYRight: 0,
139	    treeX: [0, 0, 0], treeStyle: [0, 0, 0, 0], genTrees: [], lakeX: [],
140	    mCaveX: new Int32Array(1024), mCaveY: new Int32Array(1024), numMCaves: 0,
141	    snowMinX: null, snowMaxX: null, snowTop: 0, snowBottom: 0,
142	    jungleBounds: null,
143	    evilZones: [],
144	    undergroundDesert: null,
145	    pyramidSpots: [],
146	    floatingIslands: [],
147	    shimmerX: -1, shimmerY: -1,
148	    desertHiveHigh: h, desertHiveLow: 0, desertHiveLeft: w, desertHiveRight: 0,
149	    jungleHut: 0,
150	    hellChestItems: null, hellChestIdx: 0, jungleItemIdx: 0, gennedMahoganyWands: false,
151	    orePatchX: new Int32Array(50), numOrePatch: 0,            // ResetGenerator 清零（cs:8289）
152	    logX: 0, logY: 0,                                          // 进程级静态默认 0（GenVars.cs:250）
153	    larvaX: [], larvaY: [],                                    // BeeLarva pass（cs:21018）消费
154	    oasisX: [], oasisY: [], oasisW: [], numOasis: 0,           // Oasis pass（cs:16327）登记
155	  };
156	}
157	

```


---

## 🤖 Assistant · 2026-08-12T16:52:56.791Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TerrainPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:56.801Z

**📎 ToolResult**

```
1	// 原版 TerrainPass 移植（1456 Terraria.GameContent.Biomes/TerrainPass.cs 1:1，
2	// 2026-08-11 种子等价对账修正：num3/num4 是 double 非 float——此前误加 fround
3	// float32 每步舍入，整条随机游走被腐蚀；小世界 clamp 缺 +0.02（GetWorldSize()==0）；
4	// 填柱空气边界是 trunc(num3) 非 ceil（原版 dirt 循环从 (int)num3 起覆盖小数格））。
5	// 逐列随机走 5 种地形特征(Plateau/Hill/Dale/Mountain/Valley)驱动 worldSurface/rockLayer;
6	// 输出 worldSurfaceHigh/Low、rockLevelHigh/Low、waterLine、lavaLine 到 GenState;
7	// 海滩区按 Reset 掷的 beachLeftEnd/beachRightStart 平坦化,右海滩入口 Retarget 收平。
8	import type { TileStore } from '../../TileStore';
9	import type { RNG } from '../../../core/rng';
10	import type { GenState } from './GenState';
11	import { T } from '../../../data/tiles';
12	
13	const enum Feature { Plateau, Hill, Dale, Mountain, Valley }
14	
15	// GenerateWorldSurfaceOffset（1456 cs:293-401，普通模式 else 分支：
16	// 条件 drunk/getGood/remix 为 false 时不掷判定骰）
17	function genSurfaceOffset(rng: RNG, f: Feature): number {
18	  let n = 0;
19	  switch (f) {
20	    case Feature.Plateau:
21	      while (rng.next() * 7 < 1) n += rng.int(-1, 1);
22	      break;
23	    case Feature.Hill:
24	      while (rng.next() * 4 < 1) n--;
25	      while (rng.next() * 10 < 1) n++;
26	      break;
27	    case Feature.Dale:
28	      while (rng.next() * 4 < 1) n++;
29	      while (rng.next() * 10 < 1) n--;
30	      break;
31	    case Feature.Mountain:
32	      while (rng.next() * 2 < 1) n--;
33	      while (rng.next() * 6 < 1) n++;
34	      break;
35	    case Feature.Valley:
36	      while (rng.next() * 2 < 1) n++;
37	      while (rng.next() * 5 < 1) n--;
38	      break;
39	  }
40	  return n;
41	}
42	
43	export function runTerrainPass(st: TileStore, rng: RNG, gs: GenState, flatBeachPadding = 5): void {
44	  const { w, h } = st;
45	  const leftBeach = gs.beachLeftEnd, rightBeach = w - gs.beachRightStart;
46	  // num10（cs:117-131）：0.17 基线，小世界（GetWorldSize()==0，maxTilesX==4200）+0.02
47	  const surfLo = h * (0.17 + (w === 4200 ? 0.02 : 0));
48	  const surfHi = h * 0.26;
49	  let feature: Feature = Feature.Plateau;
50	  let num2 = h * 0.3 * (rng.int(90, 109) * 0.005);            // num3 worldSurface(逐列游走,double)
51	  let num3 = (num2 + h * 0.2) * (rng.int(90, 109) * 0.01);      // num4 rockLayer(逐列游走,double)
52	  let loSurf = num2, hiSurf = num2, loRock = num3, hiRock = num3;
53	  const maxSurf = h * 0.23;
54	  const history: number[] = []; // 近 500 列地表(右海滩 Retarget 用)
55	
56	  let runLen = leftBeach + flatBeachPadding;
57	  for (let x = 0; x < w; x++) {
58	    loSurf = Math.min(num2, loSurf);
59	    hiSurf = Math.max(num2, hiSurf);
60	    loRock = Math.min(num3, loRock);
61	    hiRock = Math.max(num3, hiRock);
62	    if (runLen <= 0) {
63	      feature = rng.int(0, 4);
64	      runLen = rng.int(5, 39);
65	      if (feature === Feature.Plateau) runLen *= Math.floor(rng.int(5, 29) * 0.2);
66	    }
67	    runLen--;
68	    // 出生点 ±2% 强制高原;±5% 内避免山/谷(原版换 0-2 低洼特征)
69	    if (x > w * 0.45 && x < w * 0.55 && (feature === Feature.Mountain || feature === Feature.Valley)) {
70	      feature = rng.int(0, 2);
71	    }
72	    if (x > w * 0.48 && x < w * 0.52) feature = Feature.Plateau;
73	    // 原版：double 累加（整数偏移），无任何 float 舍入——IEEE754 double 与 C# 位级一致
74	    num2 += genSurfaceOffset(rng, feature);
75	    if (x < leftBeach + flatBeachPadding || x > w - rightBeach - flatBeachPadding) {
76	      num2 = Math.max(surfLo, Math.min(num2, maxSurf)); // Utils.Clamp(海滩区)
77	    } else if (num2 < surfLo) { num2 = surfLo; runLen = 0; }
78	    else if (num2 > surfHi) { num2 = surfHi; runLen = 0; }
79	    while (rng.int(0, 2) === 0) num3 += rng.int(-2, 2);
80	    if (num3 < num2 + h * 0.06) num3++;
81	    if (num3 > num2 + h * 0.35) num3--;
82	    history.push(num2);
83	    if (history.length > 500) history.shift();
84	    // 填列（FillColumn cs:246-271）：air 循环 i<num3，dirt 循环从 (int)num3 起覆盖
85	    // → 最终态 y < trunc(num3) 空气、[trunc(num3), num4) 泥土、≥num4 石头。
86	    // （此前按 y<num3 空气 = ceil 边界，小数列整体低一格）
87	    const surfTrunc = Math.trunc(num2);
88	    for (let y = 0; y < h; y++) {
89	      const i = st.idx(x, y);
90	      if (y < surfTrunc) {
91	        st.type[i] = 0; st.flags[i] = 0;
92	      } else if (y < num3) {
93	        // ★原版 FillColumn 只写 active+type 不刷墙（地下自然墙全部来自后置 pass：
94	        // DirtWallBackgrounds 近地表 + CaveWallsInEnclosedSpaces(17819) 封闭腔 +
95	        // digTunnel 无墙 + mudWall 丛林）。自刷渲染墙曾致 mudWall 分支短路分叉
96	        st.type[i] = T.DIRT; st.flags[i] = 1;
97	      } else {
98	        st.type[i] = T.STONE; st.flags[i] = 1;
99	      }
100	    }
101	    // 右海滩入口:若地表高于 maxSurf,回溯改写近 500 列向下收平(cs:196-204)
102	    if (x === w - rightBeach - flatBeachPadding) {
103	      if (num2 > maxSurf) retargetSurfaceHistory(st, history, x, maxSurf);
104	      feature = Feature.Plateau;
105	      runLen = w - x;
106	    }
107	  }
108	
109	  // 输出常量(TerrainPass.cs:109-132)
110	  const worldSurface = Math.floor(hiSurf + 25);
111	  const rockLayer = Math.floor(worldSurface + Math.floor((hiRock - worldSurface) / 6) * 6);
112	  gs.waterLine = Math.floor((rockLayer + h) / 2) + rng.int(-100, 19);
113	  gs.lavaLine = gs.waterLine + rng.int(50, 79);
114	  // num11 校正:rockLayerLow 与 worldSurfaceHigh 间距 < 20 → 拉开
115	  const num11 = 20;
116	  if (loRock < hiSurf + num11) {
117	    const mid = (loRock + hiSurf) / 2;
118	    let spread = Math.abs(loRock - hiSurf);
119	    if (spread < num11) spread = num11;
120	    loRock = mid + spread / 2;
121	    hiSurf = mid - spread / 2;
122	  }
123	  gs.worldSurface = worldSurface;
124	  gs.rockLevel = rockLayer;
125	  gs.worldSurfaceLow = Math.floor(loSurf);
126	  gs.worldSurfaceHigh = Math.floor(hiSurf);
127	  gs.rockLevelLow = Math.floor(loRock);
128	  gs.rockLevelHigh = Math.floor(hiRock);
129	  // GenVars 终值（cs:232-237：游走最后一列的 num3/num4 double——注意 ≠ Main.worldSurface）
130	  gs.genWorldSurface = num2;
131	  gs.genRockLayer = num3;
132	  gs.genWorldSurfaceHigh = hiSurf; // num6 校正后 raw double（cs:236）
133	}
134	
135	// RetargetSurfaceHistory(TerrainPass.cs:256-276):将历史地表逐列下压到目标高度后重写地形
136	function retargetSurfaceHistory(st: TileStore, history: number[], targetX: number, targetHeight: number): void {
137	  for (let i1 = 0; i1 < history.length / 2 && history[history.length - 1] > targetHeight; i1++) {
138	    for (let i2 = 0; i2 < history.length - i1 * 2; i2++) {
139	      const v = history[history.length - i2 - 1] - 1;
140	      history[history.length - i2 - 1] = v;
141	      if (v <= targetHeight) break;
142	    }
143	  }
144	  for (let i = 0; i < history.length; i++) {
145	    const surf = history[history.length - i - 1];
146	    retargetColumn(st, targetX - i, surf);
147	  }
148	}
149	
150	function retargetColumn(st: TileStore, x: number, worldSurface: number): void {
151	  if (x < 0 || x >= st.w) return;
152	  const surfTrunc = Math.trunc(worldSurface); // 同 FillColumn：dirt 循环 (int) 起覆盖小数格
153	  for (let y = 0; y < st.h; y++) {
154	    const i = st.idx(x, y);
155	    if (y < surfTrunc) {
156	      st.type[i] = 0; st.flags[i] = 0;
157	    } else if (!(st.type[i] === T.STONE && st.flags[i])) {
158	      st.type[i] = T.DIRT; st.flags[i] = 1;
159	    }
160	  }
161	}
162	

```


---

## 🤖 Assistant · 2026-08-12T16:52:56.961Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GravitatingSandPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:52:56.973Z

**📎 ToolResult**

```
1	// 原版 GravitatingSandCleanup（1456 cs:15198-15226，注册位 Lakes(14613) 之后、
2	// Shimmer(15256) 之前）：逐列自底向上扫，地表内（y < worldSurface）的 Falling 系
3	// 方块（沙/邪沙/淤泥/雪泥/贝壳堆等，TileID.Sets.Falling cs:391）若与上方上一处实心
4	// 之间有空腔，把整段空腔 ResetToType 成同型方块——悬空沙柱"落定"，杜绝海岸/沙滩带
5	// 生成后残留的浮空沙。纯确定性扫描，零掷骰。
6	import type { TileStore } from '../../TileStore';
7	import type { GenState } from './GenState';
8	import { TILE_BY_KEY } from '../../../data/tiles';
9	import { solidOrSlopedTile } from './HalfBrickPass';
10	
11	/** TileID.Sets.Falling（1456 Terraria.ID/TileID.cs:391）：53,234,112,116,224,123,330,331,332,333,495 */
12	const FALLING = new Set<number>([
13	  TILE_BY_KEY['sand'] ?? 0,                    // 53
14	  TILE_BY_KEY['v_234_crimsand_block'] ?? 0,    // 234
15	  TILE_BY_KEY['v_112_ebonsand_block'] ?? 0,    // 112
16	  TILE_BY_KEY['v_116_pearlsand_block'] ?? 0,   // 116
17	  TILE_BY_KEY['v_224_slush_block'] ?? 0,       // 224
18	  TILE_BY_KEY['silt'] ?? 0,                    // 123
19	  TILE_BY_KEY['v_330_copper_coin_pile'] ?? 0,  // 330
20	  TILE_BY_KEY['v_331_silver_coin_pile'] ?? 0,  // 331
21	  TILE_BY_KEY['v_332_gold_coin_pile'] ?? 0,    // 332
22	  TILE_BY_KEY['v_333_platinum_coin_pile'] ?? 0,// 333
23	  TILE_BY_KEY['v_495_shell_pile_block'] ?? 0,  // 495
24	].filter((v) => v !== 0));
25	
26	/** Tile.ResetToType（1456 Tile.cs:279-289）：liquid 清零 + 仅 active 位的 header +
27	 *  frame 清零 + 换 type；wall 不动（wall 为独立 ushort 字段，不在 header 里） */
28	function resetToType(st: TileStore, x: number, y: number, type: number): void {
29	  const i = st.idx(x, y);
30	  st.type[i] = type;
31	  st.flags[i] = 1;          // sTileHeader = 32（active 位）
32	  st.liquid[i] = 0;
33	  st.liquidType[i] = 0;     // bTileHeader3 = 0
34	  st.half[i] = 0;
35	  st.slope[i] = 0;
36	  st.frameX[i] = 0;
37	  st.frameY[i] = 0;
38	  st.wire[i] = 0;           // bTileHeader/bTileHeader2 = 0（电线/致动位清零）
39	}
40	
41	export function runGravitatingSandPass(st: TileStore, gs: GenState): void {
42	  for (let x = 0; x < st.w; x++) {
43	    let flag = false;
44	    let num = 0;
45	    for (let y = st.h - 1; y > 0; y--) {
46	      if (!solidOrSlopedTile(st, x, y)) continue;
47	      const type = st.type[st.idx(x, y)];
48	      // cs:15210：上方曾有实心 && 在地表内 && 与上一实心不贴合 && Falling 系
49	      // → 把 (y, num) 空腔整段填成同型
50	      if (flag && y < gs.worldSurface && y !== num - 1 && FALLING.has(type)) {
51	        for (let j = y; j < num; j++) resetToType(st, x, j, type);
52	      }
53	      flag = true;
54	      num = y;
55	    }
56	  }
57	}
58	

```


---

## 🤖 Assistant · 2026-08-12T16:53:36.661Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key facts so far:

- gs.beachDistance = 380 (GenState.ts:130). BeachLeftEnd = 320..380 + (side?40:20). For dungeonSide === 1 (dungeon on right): beachLeftEnd = 320..380 + 20 = 340..400. For dungeonSide === -1 (dungeon on left): beachLeftEnd = 320..380 + 40 = 360..420.

Dungeon initial location (side -1): rng.nextIntRange(beachLeftEnd + 50, W*0.2) = [410..470, 0.2W].
Drift: nx = dungeonLocation - 300 + rng.int(0,599) → nx ∈ [dungeonLocation-300, dungeonLocation+299]. Guard: nx <= 380 → skip (continue). So nx >= 381 possible! For side -1 with initial dungeonLocation as low as 410: nx could be 381..410 region → i.e., dungeon entrance as low as nx+25-49 = nx-24 → ~357. And beachLeftEnd could be as high as 420, waterX cap = beachLeftEnd - 50 = 370... hmm. So dungeon entrance at x≈360 could be right at the beach basin edge. But wait — the beach basin carving region: waterX <= beachLeftEnd - minSand (minSand=50 for w=4200). Carving loop `for (x = waterX-1; x >= 0; x--)` — it carves from waterX-1 leftward. So inland columns > waterX are NOT carved. The sand placement `else if (y > waterY) st.type[i] = SAND` applies only for x <= waterX-1. So the entrance must be at x < waterX to be covered.

waterX: rng.int(220,259) (oceanWaterMin=220, max=260, upper bound open) or forcedJungleLen 275 if dungeonSide===1. cap = beachLeftEnd - 50.

For side -1 (dungeon left): waterX = rng.int(220,259); if waterX > cap → clamp. cap = beachLeftEnd-50 = 310..370. Typically waterX ~220-259 < cap, so no clamp. So beach basin carved region is x <= waterX-1 ≈ 219-258. And minimum possible dungeon location after drift is nx-24 where nx >= 381 → ~357. So the beach carving can't reach the dungeon entrance horizontally... unless the depth curve: the sand fill region is only within y range 0..yEnd for x <= waterX. So no horizontal reach beyond waterX.

Hmm. So beaches pass carving doesn't reach x≈360+. Unless waterX clamped to cap: for side -1 with beachLeftEnd = 360..420, cap=310..370 > 259 always. So no.

For side 1 (dungeon right): right basin: waterX = W - rng.int(220,259), cap = beachRightStart + 50; waterX < cap → clamp to min(w-2, cap). beachRightStart = W - 320..380 - 40 = W-360..W-420. cap = W-310..W-370. waterX = W-220..W-259. Is waterX < cap? W-259 vs W-310: waterX > cap typically (since -259 > -310). So clamp: waterX = min(w-2, cap) → cap = beachRightStart+50. So waterX = beachRightStart+50. Then carving from x = waterX rightward to w. So carving region x >= beachRightStart+50. Dungeon location side 1 initial ∈ [0.8W, beachRightStart-50]; after drift nx ∈ [dLoc-300, dLoc+299], guard nx >= w - 380 → nx <= w-380 → continue; so nx ∈ [dLoc-300, w-381]. dLoc max = beachRightStart-50. So nx can be up to beachRightStart - 51, i.e., still 101 columns left of the carving start (beachRightStart+50). So carving won't reach it... but wait — carving could also be within waterX..: hmm carving goes rightward x>=waterX.

Hmm, so direct beach-basin overwrite doesn't reach the entrance hall horizontally. BUT — critical: the dungeon entrance hall is carved at surface with entrance tower, and after drift the entrance may be very close to the beach edge. But the more direct issue: runBeachesPass also clears walls (st.wall[i]=0) — irrelevant here.

Wait, but important: the OceanSand pass (runOceanSandPass) runs in vanillaCaves slot, i.e. BEFORE biomes/dungeon. It places sand from surface down thickness for x in [0, beachLeftEnd). Not post-dungeon.

But hmm — question says entrance corridor "sometimes ends up blocked/covered by sand". Candidates:

1. GravitatingSandPass runs AFTER dungeon (slot order: biomes [includes dungeon] then 引力沙). It fills air cavities below falling tiles with the same falling tile — within y < worldSurface. If the entrance hall is carved open-air at the surface and there's sand above it (e.g., from Desert pass or Dunes or OceanSand... wait OceanSand is before dungeon; desert pass is before dungeon). Hmm, but GravitatingSand works per column: if a falling tile exists at y with an air cavity above (j from y to num), it fills the cavity with sand — i.e., the open entrance corridor air would be filled with sand if a sand tile exists below it in the same column... wait direction: scan from bottom y=h-1 up. `flag` = had solid above previously... let me parse: iterating y from bottom upward. num = y of last solid seen (below). Actually scanning upward, first encountered solid at bottom sets flag... hmm num is set after each solid. Condition: flag && y < worldSurface && y !== num-1 && FALLING.has(type). num is the y of the previous solid tile encountered (which is below current since we scan upward). So cavity between y (falling tile) and num (solid below). Wait scanning upward: first solid from bottom is at yBottom. flag was false → skip, flag=true, num=yBottom. Next solid at y2 > yBottom: cavity between yBottom+1..y2-1. If type at y2 is falling, fill j=y2..num-1... wait `for (j = y; j < num; j++)` — y (current, above) to num (below). j from y2 to yBottom-1?? That seems off; probably y2 < num? Hmm, since scanning upward y increases; num was the previously processed solid which is at a LOWER y... no wait, scanning upward means y decreases? `for (let y = st.h - 1; y > 0; y--)` — y DECREASES: from bottom to top. So the first solid found is the lowest, num = that. Next solid found at smaller y (higher up). Condition y !== num-1 means there's a gap between the current solid (above) and num (below). So the cavity is (y, num) = between higher tile y and lower tile num. Fill j=y..num-1 with the type of the UPPER tile (falling). So: if a sand tile is sitting at height y and there's an air gap below it down to num, the whole gap is filled with sand. So the open-air dungeon entrance hall: if the dungeon carved a hall into a hill of sand/dirt — if a SAND tile exists at the top of the column above the carved hall, the gravitating pass fills the entire hall with sand! That's a strong candidate: the corridor carved below a sand surface (dungeon near beach/desert where surface is sand from OceanSand/Desert pass) would be re-filled with sand by GravitatingSandPass — since it runs AFTER the dungeon pass (slot 引力沙 after 生物群系). In vanilla, GravitatingSand (36) is registered AFTER Dungeon (32) too — and vanilla also fills these cavities. Hmm, but vanilla's would do the same. But vanilla dungeon entrance is typically carved such that... well vanilla has same behavior. But in vanilla, does dungeon entrance get covered? Reportedly no. But our drift may put the entrance in sand terrain where vanilla wouldn't.

Actually wait — in vanilla the scan condition uses `Main.worldSurface` semantics similarly. The entrance hall has a roof of dungeon bricks (the tower). So the column: tower roof bricks (not falling), then air hall, then floor bricks. When scanning, the solid at floor brick is not falling; roof brick above is not falling → no fill. Hmm — unless the hall is open-air: the precalc entrance (entPos) is at the surface: nx scan finds first solid/liquid/wall from y=10 down. The entrance hall (dungeonEnt) is an open-air structure: DungeonEnt carves a corridor with a tower. The hall air may connect to the sky. Then for a column within the hall: solids above? The Old Man walks on the corridor floor. The corridor is open air to the sky at its top? DungeonEnt builds crenellated tower; the walkway is open-air. Then a column above the corridor floor: no solid above (sky) — flag only set when solid found; scan from bottom: floor brick solid → flag=true num=floor. Next going up: nothing (air to top of world) → no fill. So no.

But the hall carved through a SAND dune/hill: the corridor floor is dungeon brick; walls are dug through sand terrain. The sand hills adjacent could overhang: a column of sand above the corridor roof gap. If the corridor has openings (where the tower has gaps or where the corridor passes under a sand overhang), a sand tile at y with air gap below it (the hall interior) down to the hall floor... wait fill j=y..num-1 where num is the first solid BELOW the sand. If the sand overhang is above the hall interior, num = hall floor brick? No — between the sand overhang and the floor there's air = the hall. num = the lowest solid found first = hall floor. y = sand overhang. y !== num-1 → gap → fills j from y (overhang) down to num-1 (floor above). So it fills the hall with sand. Yes! This is candidate #1 — plausible: "sand covering corridor".

Note in vanilla the same code exists (cs:15198) and runs after dungeon... so vanilla would have same issue unless vanilla's dungeon placement avoids sand. But our drift may differ. Still report as candidate.

2. Post-dungeon passes that place sand. Let me enumerate remaining: PilesPass (矿骨堆 slot, after dungeon), FinalCleanupPass (sandstone/hardened sand walls lava — walls not tiles, but check), BeachDecor shell piles (place SAND + hardened sand at shellStart anchors — near beach waterline, not dungeon), Oasis (digs ponds, shoreline sand — desert only), DunesPass — wait dunes run in slot 1 BEFORE dungeon? Let me confirm: passes order: '原版地形' (slot 0), '沙丘' (slot 1), '洞穴' (slot 2), '生物群系' (slot 3). So Dunes before Dungeon. But wait — hmm, in vanilla Dunes(11540) < Dungeon. Yes fine.

But DunesPass also throws dungeonTheme. Dunes place sand hills — before dungeon, so it can create sand terrain where the dungeon entrance will be carved, but cannot cover it afterwards. Still relevant as the source of sand above the corridor (feeds candidate #1).

3. DesertPass runs inside vanillaBiomes BEFORE dungeon (line 581). Sand surface where dungeon carved. Also before.

4. StructuresPass: CactusPoralTreesAndCoral — palm trees need sand? Places palm trunks in sand. Probably not covering corridor.

5. SurfaceDecorPasses: SurfaceOreAndStone? FallenLogs? Flowers etc. Probably no sand.

6. MissingCavesPass runSandPatchesPass — runs in vanillaCaves slot (before dungeon) - underground sand blobs.

7. BuriedChestsPass "sand chests"? Buried chests in desert — places chest, maybe digs.

8. MicroBiomesPass — campsites? no sand.

9. CleanupPass / FinalCleanupPass / TileCleanupPass — check for sand handling.

Let me grep across the gen dir for sand placements: T.SAND, hardened_sand, sandstone, desert fossil, tileDungeon, wallDungeon gating.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:53:36.852Z · glm-x-preview-260804

```
Now let me grep for all sand placements and dungeon gating across the gen dir.
```


---

## 🤖 Assistant · 2026-08-12T16:53:37.403Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"hardened_sand\\|sandstone\\|desert_fossil\\|HARD_SAND\\|SANDSTONE\\|FOSSIL\" ~/Project/GLM/SandboxWorld/game/src/world/gen/ | grep -v \"\\.md\"",
 "description": "Find hardened sand/sandstone/fossil placements"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:53:37.429Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileCleanupPass.ts:53:const CONV_SANDSTONE = idsByVanillaSheet(396, 400, 403, 401);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileCleanupPass.ts:172:          if (CONV_SANDSTONE.has(st.type[above]) || CONV_HARDENED_SAND.has(st.type[above])) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:232:  const HARD_SAND = TILE_BY_KEY['hardened_sand'] ?? 0;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:253:              if (inactive(st, i, num4 + 3)) putPile(st, i, num4 + 3, HARD_SAND);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts:12:const SANDSTONE = TILE_BY_KEY['sandstone']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts:13:const HARDSAND = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts:163:            } else if (cur === SANDSTONE || cur === HARDSAND) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OceanCavesPass.ts:13:const HARDSAND = TILE_BY_KEY['hardened_sand']!; // 397
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:20:const SANDSTONE = TILE_BY_KEY['sandstone']!;   // 396
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:21:const HARDSAND = TILE_BY_KEY['hardened_sand']!; // 397
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:221:  if (!(t === SAND || t === SANDSTONE || t === HARDSAND)) return false;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:227:      if (st.type[st.idx(i, yy)] !== SANDSTONE) return false;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:272:        if (!flag) st.setTileSilent(xx, yy, SANDSTONE);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:274:        st.setTileSilent(xx, yy, !flag || !st.flags[st.idx(xx, yy - 1)] ? SANDSTONE : HARDSAND);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:276:        if (!flag) st.setTileSilent(xx, yy, SANDSTONE);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:36:const SANDSTONE = TILE_BY_KEY['sandstone']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:37:const HARDSAND = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:38:const FOSSIL = TILE_BY_KEY['desert_fossil']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:44:const HARDSAND_TILE = TILE_BY_KEY['hardened_sand']!; // 原版 SetTile(397)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:270:      if (t === SAND || t === SANDSTONE || t === HARDSAND || t === FOSSIL) wallType = 171;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:18:const CORRUPT_HARDSAND = TILE_BY_KEY['v_398_corrupt_hardened_sand_block']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:22:const CRIMSON_HARDSAND = TILE_BY_KEY['v_399_crimson_hardened_sand_block']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:23:const CORRUPT_SANDSTONE = TILE_BY_KEY['v_400_corrupt_sandstone_block']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:24:const CRIMSON_SANDSTONE = TILE_BY_KEY['v_401_crimson_sandstone_block']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:51:const SANDSTONE = TILE_BY_KEY['sandstone']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:52:const HARDSAND = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:234:      else if (st.type[i] === SANDSTONE) st.type[i] = crimson ? CRIMSON_SANDSTONE : CORRUPT_SANDSTONE;  // 396→401/400
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts:134:const SANDSTONE = TILE_BY_KEY['sandstone']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts:135:const HARDSAND = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts:136:const FOSSIL = TILE_BY_KEY['desert_fossil']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts:636:        if (f2 % 15 === 2) resetToType(px, py, FOSSIL);     // 获胜簇索引 %15==2
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts:641:        if (!isEdge || st.flags[i]) resetToType(px, py, SANDSTONE);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts:703:      if (!st.flags[i] || st.type[i] !== SANDSTONE) continue;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:38:  desert:   { tile: TILE_BY_KEY['sandstone']!, wall: 187, beam: TILE_BY_KEY['v_577_sandstone_column']!, door: 43, platformStyle: 42, chestStyle: 10, chestTile2: true, tables2: true, table: 7, workbench: 39, piano: 38, bookcase: 39 },
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:58:const HARDSAND397 = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:69:const SC396 = TILE_BY_KEY['sandstone']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:70:const SC397 = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/WaterIcePasses.ts:13:const SAND_HARD = TILE_BY_KEY['hardened_sand']!;   // 397
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/WaterIcePasses.ts:14:const SANDSTONE = TILE_BY_KEY['sandstone']!;       // 396？原版 404=Sandstone，见下
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/WaterIcePasses.ts:46:  void SAND; void SAND_HARD; void SANDSTONE;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:529:const SANDSTONE_BRICK = TILE_BY_KEY['v_151_sandstone_brick']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:578:  const num = SANDSTONE_BRICK;   // 151
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SwordShrinePass.ts:98:      const HARDENED = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts:18:const SANDSTONE = TILE_BY_KEY['sandstone']!, HARDSAND = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts:39:          || t === MUSH_GRASS || t === MUSH_TREE || t === SANDSTONE || t === HARDSAND) return true;

```


---

## 🤖 Assistant · 2026-08-12T16:53:38.322Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"T\\.SAND\\|'sand'\\|isDungeon\\|dungeonWall\\|wall.*=== *\\(7\\|8\\|9\\)\\b\" ~/Project/GLM/SandboxWorld/game/src/world/gen/ --include=\"*.ts\" | grep -v \"//\" | head -80",
 "description": "Find sand tile writes in gen"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:53:38.349Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DirtToMudPass.ts:12:const SAND = T.SAND;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts:112:          if (st.type[ti] === T.SAND) st.flags[ti] = 0;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts:122:          st.type[ti] = T.SAND;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts:170:            st.type[st.idx(num29, num19)] = T.SAND;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts:174:              st.type[st.idx(num29, num19 - 1)] = T.SAND;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts:46:function isDungeonWall(wl: number): boolean {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts:428:    if (isDungeonWall(wl) || wl === 87 || !placeBuriedChest(st, rng, gs, chests, x, y)) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:210:      if (st.type[i] === T.SAND && x >= zLo + rng.int(0, 4) && x <= zHi - rng.int(0, 4)) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:53:            st.type[jj] = T.SAND;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:149:            st.type[i] = T.SAND; st.flags[i] = 1;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:184:            st.type[i] = T.SAND; st.flags[i] = 1;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:252:              putPile(st, i, num4 + 2, T.SAND);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:257:          putPile(st, i, num4, T.SAND);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:283:        if (st.flags[i] && st.type[i] === T.SAND
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:308:        if (st.flags[i] && st.type[i] === T.SAND
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts:129:          if (st.flags[ti] && st.type[ti] === T.SAND) continue;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileRunner.ts:157:            } else if (cur === T.SAND) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:35:const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LakesPass.ts:22:const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:19:const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts:133:const SAND = T.SAND;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts:144:  const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IceBiomePass.ts:48:        if (t === 0 || t === T.DIRT || t === T.GRASS || t === CORRUPT_GRASS || t === CLAY || t === T.SAND) st.type[i] = T.SNOW;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/IceBiomePass.ts:63:          if (t === 0 || t === T.DIRT || t === T.GRASS || t === CORRUPT_GRASS || t === CLAY || t === T.SAND) st.type[i] = T.SNOW;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:68:const SC53 = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/ShiniesPass.ts:95:    ['sand', 'v_112_ebonsand_block', 'v_234_crimsand_block']
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CleanupPass.ts:30:            ? (st.type[ii] === T.SAND || st.type[ii] === EBONSAND || st.type[ii] === CRIMSAND)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CleanupPass.ts:31:            : st.type[ii] === T.SAND;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SwordShrinePass.ts:34:    for (let y = 0; y < oy && !sandAbove; y++) if (st.type[st.idx(x, y)] === T.SAND && st.flags[st.idx(x, y)]) sandAbove = true;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SwordShrinePass.ts:103:          if (st.type[j] === T.SAND) st.type[j] = HARDENED;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:61:function isDungeonWall(w: number): boolean { return DUNGEON_WALLS.has(w); }
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:151:  if (wl === WALL_LIVING_WOOD || wl === 78 || isDungeonWall(wl)) return false;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:327:        if (!isDungeonWall(wl)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:329:            || (!isDungeonWall(wallAt(st, n11, n10 - 1)) && !isDungeonWall(wallAt(st, n11, n10 + 1))))
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:342:        if (!isDungeonWall(wallAt(st, n11, n10))) st.wall[st.idx(n11, n10)] = WALL_LIVING_WOOD;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:349:      if (isDungeonWall(wallAt(st, n11, n10)) || isDungeonWall(wallAt(st, n11, n10 - 1)) || isDungeonWall(wallAt(st, n11, n10 - 2))) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:418:          if (!isDungeonWall(wl) && wl !== 3 && wl !== 83) st.wall[st.idx(i, num4)] = WALL_LIVING_WOOD;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:420:          if (!isDungeonWall(wlL) && (wlL > 0 || num4 >= worldSurface)) st.wall[st.idx(i - 1, num4)] = WALL_LIVING_WOOD;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:422:          if (!isDungeonWall(wlR) && (wlR > 0 || num4 >= worldSurface)) st.wall[st.idx(i + 1, num4)] = WALL_LIVING_WOOD;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:434:          if (!isDungeonWall(wl) && wl !== 3 && wl !== 83 && (activeAt(st, i, num4) || wl !== 34)) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:456:        if (isDungeonWall(wallAt(st, minl, num4 + 1))
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:457:          || isDungeonWall(wallAt(st, minl + 1, num4 + 1))
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:458:          || isDungeonWall(wallAt(st, minl + 2, num4 + 1))) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:513:      if (flag7 && !isDungeonWall(wallAt(st, n14, n15))) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:609:    if (!isDungeonWall(wallAt(st, n16, n17 + 1))) setLivingWood(st, n16, n17 + 1);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:613:      if (!isDungeonWall(wallAt(st, n16, n17))) setLivingWood(st, n16, n17);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:623:        if (!isDungeonWall(wallAt(st, n16, n17))) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:646:    if (!isDungeonWall(wallAt(st, n20, n21))) setLivingWood(st, n20, n21);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:659:        if (!isDungeonWall(wallAt(st, n26, n27))) setLivingWood(st, n26, n27);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:663:          if (!isDungeonWall(wallAt(st, n26, n27))) setLivingWood(st, n26, n27);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:672:          if (!isDungeonWall(wallAt(st, n30, n31))) setLivingWood(st, n30, n31);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:681:      if (!isDungeonWall(wallAt(st, n20, n21))) setLivingWood(st, n20, n21);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/HalfBrickPass.ts:267:      if (st.flags[ti] && T.SAND.has(t)) smoothSlope(st, i, j);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:533:const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DunesPass.ts:14:const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:81:  isDungeonWall(st: TileStore, x: number, y: number): boolean {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:261:            if (!dc.isDungeonWall(st, sx2 + ax, sy2 + ay)) { st.type[i] = dc.brick; st.flags[i] = 1; }
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:349:        if (!dc.isDungeonWall(st, x, y)) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:374:          if (st.flags[i] || !dc.isDungeonWall(st, x, y)) { st.type[i] = dc.cracked; st.flags[i] = 1; }
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:405:        if (!dc.isDungeonWall(st, x, y)) { st.type[i] = dc.brick; st.flags[i] = 1; }
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:494:        if (!dc.isDungeonWall(st, x, y)) { st.type[i] = dc.brick; st.flags[i] = 1; }
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:539:  const isDW = (x: number, y: number) => st.inBounds(x, y) && dc.isDungeonWall(st, x, y);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:852:    const style = rng.next() < 1 / 3 ? (dc.wall === 7 ? 16 : dc.wall === 8 ? 17 : 18) : 13;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:886:  const roomWall = wallType === 7 ? [7, 94, 95] : wallType === 9 ? [9, 96, 97] : [8, 98, 99];
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:893:  const isDWall = (x: number, y: number): boolean => st.inBounds(x, y) && dc.isDungeonWall(st, x, y);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:894:  const airDW = (x: number, y: number) => st.inBounds(x, y) && !st.flags[st.idx(x, y)] && dc.isDungeonWall(st, x, y);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:914:  const platFrameY = wallType === 7 ? 108 : wallType === 8 ? 144 : 126;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:1226:    const S = wallType === 7
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:1228:      : wallType === 8
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MissingCavesPass.ts:26:    tileRunner(st, rng, gs, num2, num3, { strength: num4, steps, type: T.SAND });

```


---

## 🤖 Assistant · 2026-08-12T16:53:45.396Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let's read the remaining passes: DunesPass (where dunes are placed, and whether they check dungeon), DesertPass (surface sand placement + gating), PilesPass, CleanupPass, FinalCleanupPass, MicroBiomesPass (fossil biome — places fossils? MicroBiomes 21785 is post-dungeon! It has FOSSIL const and wallType 171. Let me check MicroBiomesPass for placing sand tiles... line 270 wall only. Also MicroBiomes has "MiningExplosives"/"Campsites". Hmm, FOSSIL used where? Let me check. Also OasisPass (post-dungeon: oasis slot is after 引力沙 — yes slot 92 '绿洲' which is after biomes). Oasis places sand — but only in desert areas.

Also note DunesPass: check whether dunes can be near the dungeon. Dunes place sand hills along surface — runs BEFORE dungeon. But wait — is there any chance dunes run after? No.

Important: also check TrapsPass — places sandstone traps in desert; Traps pass slot: where? In passes array, traps are in '地表装饰' (vanillaSurfaceDecor → includes Traps 18769). That's after dungeon. TrapsPass lines 221-276: digs dart traps in sandstone deserts, converts tiles to SANDSTONE/HARDSAND. If dungeon entrance carved into desert... but it gates on sand context. Let me read TrapsPass relevant portion.

Also CaveHousePass (desert houses with sandstone) — post-dungeon (runCaveHousesPass at line 632 inside biomes, after dungeon 593). Desert cave houses place sandstone bricks — deep underground though.

Let me now read: DunesPass.ts, DesertPass.ts (surface sand part), PilesPass.ts, CleanupPass.ts, FinalCleanupPass.ts, and check MicroBiomesPass + TrapsPass + OasisPass sand placements with dungeon gating. Let me batch reads.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:53:45.550Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DunesPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:53:45.558Z

**📎 ToolResult**

```
1	// 原版 pass "Dunes"(GenPassNameID.DunesAndPyramidLocations,WorldGen.cs:11540-11602)
2	// + DunesBiome.cs(DunesBiome.cs:53-161)1:1 移植。
3	// 两个单侧沙丘(各宽 SingleDunesWidth 150-250、高 60-99×HeightScale 1.0)叠在 origin 两侧:
4	//   PlaceSingle = 8-10 个小山丘(二次贝塞尔 PlaceCurvedLine,曲线以下到 Surface+√x*3 全转沙 53,
5	//   曲线上方 10 格清非沙物) + 1-2 个 0.8 scale 中央大山丘。
6	// 同 pass 还掷金字塔候选(cs:11591-11599:80% 概率,origin±200 列地表+20 → GenVars.PyrX/PyrY,
7	// 这里写 gs.pyramidSpots,由 StructuresPass.runPyramidPass 按 cs:15426 段消费)。
8	// 数量:Dunes.Count = WorldGenRange 1-2 × WorldWidth/4200(Configuration.json)。
9	import type { TileStore } from '../../TileStore';
10	import type { RNG } from '../../../core/rng';
11	import type { GenState } from './GenState';
12	import { TILE_BY_KEY } from '../../../data/tiles';
13	
14	const SAND = TILE_BY_KEY['sand']!;
15	const CLOUD = TILE_BY_KEY['v_189_cloud_block']!;
16	const RAIN_CLOUD = TILE_BY_KEY['v_196_rain_cloud_block']!;
17	
18	interface DunesArea { left: number; top: number; width: number; height: number }
19	interface DunesDesc {
20	  area: DunesArea;
21	  surface: Int16Array; // SurfaceMap 高度(相对 area.left-20)
22	  surfaceX: number;    // SurfaceMap 起始列(= area.left-20)
23	  windRight: boolean;  // WindDirection
24	}
25	
26	const HEIGHT_SCALE = 1.0; // Configuration.json DunesBiome.HeightScale
27	
28	/** SurfaceMap.FromArea(DunesBiome 描述用):每列自 y=50 向下扫 maxTilesY/2 格,
29	 *  跳过云族(Clouds)取首个实心;无则 maxTilesY/2+50(SurfaceMap.cs:41-64) */
30	function surfaceMap(st: TileStore, startX: number, width: number): Int16Array {
31	  const limit = Math.floor(st.h / 2);
32	  const out = new Int16Array(width);
33	  for (let i = 0; i < width; i++) {
34	    const x = startX + i;
35	    let found = false;
36	    let y = 0;
37	    for (let j = 50; j < 50 + limit; j++) {
38	      if (!st.inBounds(x, j) || !st.flags[st.idx(x, j)]) continue;
39	      const t = st.type[st.idx(x, j)];
40	      if (t === CLOUD || t === RAIN_CLOUD) { found = false; continue; }
41	      if (!found) { y = j; found = true; }
42	    }
43	    out[i] = found ? y : limit + 50;
44	  }
45	  return out;
46	}
47	
48	export function runDunesPass(st: TileStore, rng: RNG, gs: GenState, onIter?: (i: number) => void): void {
49	  const { w, h } = st;
50	  // pass 头：DungeonCrawler.SetupDungeonGenVarVariables（cs:11542 + DungeonCrawler.cs:56）
51	  // ——地牢主题 Next(3) 在**这里**消耗（曾错放到 DungeonPass=流错位 1 颗）
52	  gs.dungeonTheme = rng.nextIntRange(0, 3);
53	  // WorldGenRange(1,2,ScaleWith:WorldWidth).GetRandom:ScaleValue=(int)(w/4200×v)
54	  const ws = w / 4200;
55	  const lo = Math.max(1, Math.trunc(ws * 1));
56	  const hi = Math.max(lo, Math.trunc(ws * 2));
57	  const count = rng.int(lo, hi);
58	  const pyramidChance = 0.8; // Configuration.json Dunes.ChanceOfPyramid
59	  const scale = w / 4200;    // cs:11562 num2
60	  for (let i = 0; i < count; i++) {
61	    // RandomWorldPoint(0, 500, 0, 500)(cs:11570)+ 拒绝带(cs:11572-11588):
62	    // 丛林 ±600·num2 / 中央 ±300 / 雪原带 ±300;超 w 次放松丛林、超 2w 次放松雪原
63	    let ox = 0, oy = 0, tries = 0;
64	    for (;;) {
65	      ox = rng.int(500, w - 501); // Next(500, w-500)
66	      oy = rng.int(0, h - 1);     // Next(0, maxTilesY)
67	      let fJungle = Math.abs(ox - gs.jungleX) < Math.trunc(600 * scale);
68	      const fCenter = Math.abs(ox - w / 2) < 300;
69	      let fSnow = ox > gs.snowOriginLeft - 300 && ox < gs.snowOriginRight + 300;
70	      tries++;
71	      if (tries >= w) fJungle = false;
72	      if (tries >= 2 * w) fSnow = false;
73	      if (!(fJungle || fCenter || fSnow)) break;
74	    }
75	    placeDunes(st, rng, ox, oy);
76	    // 金字塔候选(cs:11591-11599)
77	    if (rng.next() <= pyramidChance) {
78	      const px = rng.int(ox - 200, ox + 199); // Next(origin.X-200, origin.X+200)
79	      for (let j = 0; j < h; j++) {
80	        if (st.inBounds(px, j) && st.flags[st.idx(px, j)]) {
81	          gs.pyramidSpots.push({ x: px, y: j + 20 });
82	          break;
83	        }
84	      }
85	    }
86	  }
87	}
88	
89	/** DunesBiome.Place(cs:DunesBiome.cs:53-64):左右两个单侧沙丘 */
90	function placeDunes(st: TileStore, rng: RNG, ox: number, oy: number): void {
91	  const h1 = Math.trunc(rng.int(60, 99) * HEIGHT_SCALE); // Next(60,100)
92	  const h2 = Math.trunc(rng.int(60, 99) * HEIGHT_SCALE);
93	  const w1 = rng.int(150, 250); // SingleDunesWidth.GetRandom(含两端)
94	  const w2 = rng.int(150, 250);
95	  // ★求值顺序（DunesBiome.cs:62-65）：两张 description（含 SurfaceMap 采样+风向掷）
96	  // 都在 PlaceSingle **之前**创建——dune2 的地表图取的是 dune1 放置前的地形。
97	  // 此前 makeDesc 内联在 placeSingle 实参里 → dune2 的图被 dune1 污染（+/- 若干行）
98	  const d1 = makeDesc(st, rng, ox - Math.trunc(w1 / 2) + 30, oy, w1, h1);
99	  const d2 = makeDesc(st, rng, ox + Math.trunc(w2 / 2) - 30, oy, w2, h2);
100	  placeSingle(st, rng, d1);
101	  placeSingle(st, rng, d2);
102	}
103	
104	function makeDesc(st: TileStore, rng: RNG, x: number, y: number, width: number, height: number): DunesDesc {
105	  // DunesDescription.CreateFromPlacement:area = origin-(w/2,h/2, w, h);
106	  // SurfaceMap.FromArea(area.Left-20, area.Width+40);风向后随机(DunesBiome.cs:26-36)
107	  const left = x - Math.trunc(width / 2);
108	  const area: DunesArea = { left, top: y - Math.trunc(height / 2), width, height };
109	  const sx = left - 20;
110	  return { area, surface: surfaceMap(st, sx, width + 40), surfaceX: sx, windRight: rng.int(0, 1) !== 0 };
111	}
112	
113	/** DunesBiome.PlaceSingle(DunesBiome.cs:66-87) */
114	function placeSingle(st: TileStore, rng: RNG, d: DunesDesc): void {
115	  const num = rng.int(0, 2) + 8; // Next(3)+8 → 8-10
116	  for (let i = 0; i < num - 1; i++) {
117	    const n2 = Math.trunc((2 / num) * d.area.width); // C# int
118	    let n3 = Math.trunc((i / num) * d.area.width + d.area.left) + Math.trunc((n2 * 2) / 5);
119	    n3 += rng.int(-5, 5);
120	    const n4 = i / (num - 2);
121	    const n5 = 1 - Math.abs(n4 - 0.5) * 2;
122	    placeHill(st, rng, d, n3 - Math.trunc(n2 / 2), n3 + Math.trunc(n2 / 2), (n5 * 0.3 + 0.2) * HEIGHT_SCALE);
123	  }
124	  const n6 = rng.int(0, 1) + 1; // Next(2)+1
125	  for (let j = 0; j < n6; j++) {
126	    const n7 = Math.trunc(d.area.width / 2);
127	    const cx = d.area.left + Math.trunc(d.area.width / 2) + rng.int(-10, 10);
128	    placeHill(st, rng, d, cx - Math.trunc(n7 / 2), cx + Math.trunc(n7 / 2), 0.8 * HEIGHT_SCALE);
129	  }
130	}
131	
132	/** DunesBiome.PlaceHill(DunesBiome.cs:89-108) */
133	function placeHill(st: TileStore, rng: RNG, d: DunesDesc, startX: number, endX: number, scale: number): void {
134	  // SurfaceMap 越界钳到边缘列(原版越界会 IndexOutOfRange,此处防御)
135	  const surfAt = (x: number) => {
136	    const i = Math.max(0, Math.min(d.surface.length - 1, x - d.surfaceX));
137	    return d.surface[i];
138	  };
139	  const startPoint = { x: startX, y: surfAt(startX) };
140	  const endPoint = { x: endX, y: surfAt(endX) };
141	  const center = { x: Math.trunc((startPoint.x + endPoint.x) / 2), y: Math.trunc((startPoint.y + endPoint.y) / 2) - Math.trunc(35 * scale) };
142	  const big = Math.trunc((endPoint.x - center.x) / 4);
143	  const small = Math.trunc((endPoint.x - center.x) / 16);
144	  if (!d.windRight) center.x -= rng.int(small, big);      // Next(min, num+1)
145	  else center.x += rng.int(small, big);
146	  const p2 = { x: 0, y: Math.trunc(scale * 12) };
147	  const p3 = { x: Math.trunc(p2.x / -2), y: Math.trunc(p2.y / -2) };
148	  placeCurvedLine(st, d, startPoint, center, d.windRight ? p3 : p2);
149	  placeCurvedLine(st, d, center, endPoint, !d.windRight ? p3 : p2);
150	}
151	
152	/** DunesBiome.PlaceCurvedLine(DunesBiome.cs:110-161):二次贝塞尔取样,
153	 *  曲线以上 10 格清非沙物、曲线到 Surface+√(num3)*3 全列转沙(ResetToType(53)) */
154	function placeCurvedLine(
155	  st: TileStore, d: DunesDesc,
156	  startPoint: { x: number; y: number }, endPoint: { x: number; y: number },
157	  anchorOffset: { x: number; y: number },
158	): void {
159	  const p = {
160	    x: Math.trunc((startPoint.x + endPoint.x) / 2) + anchorOffset.x,
161	    y: Math.trunc((startPoint.y + endPoint.y) / 2) + anchorOffset.y,
162	  };
163	  const step = 0.5 / (endPoint.x - startPoint.x);
164	  let prevX = -1, prevY = -1;
165	  let t = 0, guard = 0;
166	  while (t <= 1 && guard++ < 10000) {
167	    const ax = startPoint.x + (p.x - startPoint.x) * t;
168	    const ay = startPoint.y + (p.y - startPoint.y) * t;
169	    const bx = p.x + (endPoint.x - p.x) * t;
170	    const by = p.y + (endPoint.y - p.y) * t;
171	    const px = Math.trunc(ax + (bx - ax) * t); // Vector2D.Lerp(...).ToPoint() 截断
172	    const py = Math.trunc(ay + (by - ay) * t);
173	    t += step;
174	    if (px === prevX && py === prevY) continue;
175	    prevX = px; prevY = py;
176	    const centerX = d.area.left + Math.trunc(d.area.width / 2);
177	    const n3 = Math.trunc(d.area.width / 2) - Math.abs(px - centerX);
178	    const surf = d.surface[Math.max(0, Math.min(d.surface.length - 1, px - d.surfaceX))];
179	    // 原版 Math.Sqrt(负)=NaN → (int)NaN。★平台语义：x86 cvttsd2si=0x80000000
180	    //（int.MinValue→填充循环不执行）；ARM64 fcvtzs=0（会填一格）。金标 .wld 在本机
181	    // 生成但游戏经 Rosetta x86 运行——实证 (2315,310) 无沙 = x86 语义。按 x86 复刻：
182	    const castSq = n3 < 0 ? -2147483648 : Math.trunc(Math.sqrt(n3) * 3);
183	    const n4 = surf + castSq;
184	    if (!st.inBounds(px, py)) continue;
185	    for (let i = py - 10; i < py; i++) {
186	      if (!st.inBounds(px, i)) continue;
187	      const ti = st.idx(px, i);
188	      if (st.flags[ti] && st.type[ti] !== SAND) {
189	        st.type[ti] = 0; st.flags[ti] = 0; st.liquid[ti] = 0; st.liquidType[ti] = 0;
190	      }
191	    }
192	    for (let j = py; j < n4; j++) {
193	      if (!st.inBounds(px, j)) continue;
194	      const ti = st.idx(px, j);
195	      st.type[ti] = SAND; st.flags[ti] = 1;
196	      st.liquid[ti] = 0; st.liquidType[ti] = 0; // ResetToType 清液体,墙保留
197	    }
198	  }
199	}
200	

```


---

## 🤖 Assistant · 2026-08-12T16:53:45.736Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CleanupPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:53:45.744Z

**📎 ToolResult**

```
1	// 原版 pass 37 "Clean Up Dirt"(L6873)移植:
2	// 1) 表层天然墙清理:地表以上暴露区的土/雪/丛林/蜂巢墙(2/40/64/86)清除(含左右 ±3 邻列,±2/3 各 50%);
3	// 2) ScanTileColumnAndRemoveClumps(L4141):逐列找竖向连续 < tileCounterMax(20) 的可清实心段,
4	//    连通块总 size < 20 则整块移除(消灭浮空散块)。
5	import type { TileStore } from '../../TileStore';
6	import type { RNG } from '../../../core/rng';
7	import type { GenState } from './GenState';
8	import { T, TILE_DEFS, TILE_BY_KEY } from '../../../data/tiles';
9	
10	const TILE_COUNTER_MAX = 20;
11	const EBONSAND = TILE_BY_KEY['v_112_ebonsand_block']!;
12	const CRIMSAND = TILE_BY_KEY['v_234_crimsand_block']!;
13	
14	export function runCleanupPass(st: TileStore, rng: RNG, gs: GenState): void {
15	  const { w } = st;
16	  // 1) 表层墙清理两遍(cs L6877-6938):
17	  //    左→右(3..w-4):中央清 2/40/64/86;右→左(w-5..5):中央清 2/40/64(不重复清蜂巢墙)。
18	  //    邻列两遍都只清 2/40;邻列清理门禁 = !active || type∉沙系(53/112/234,第二遍仅 53),
19	  //    ±2/±3 的 Next(2) 仅当墙命中才消费(cs:15340 短路)
20	  for (let dir = 0; dir < 2; dir++) {
21	    const from = dir === 0 ? 3 : w - 5;
22	    const to = dir === 0 ? w - 4 : 5;
23	    for (let x = from; dir === 0 ? x <= to : x >= to; x += dir === 0 ? 1 : -1) {
24	      let open = true;
25	      for (let y = 0; y < gs.worldSurface; y++) {
26	        if (open) {
27	          clearWallSet(st, x, y, dir === 0 ? [2, 40, 64, 86] : [2, 40, 64]);
28	          const ii = st.idx(x, y);
29	          const isSand = dir === 0
30	            ? (st.type[ii] === T.SAND || st.type[ii] === EBONSAND || st.type[ii] === CRIMSAND)
31	            : st.type[ii] === T.SAND;
32	          // cs:15334 门禁 = !active || type∉{53,112,234}(幽灵沙列有 type 无 flags,也进门并掷 4 骰)
33	          if (!st.flags[ii] || !isSand) {
34	            clearWallSet(st, x - 1, y, [2, 40]);
35	            // cs:15340/15344/15352/15356:±2/±3 的 Next(2) 仅当墙∈{2,40} 才消费(&& 短路)
36	            const rollIf = (xx: number) => {
37	              const ji = st.idx(xx, y);
38	              if ((st.wall[ji] === 2 || st.wall[ji] === 40) && rng.next() < 0.5) st.wall[ji] = 0;
39	            };
40	            rollIf(x - 2);
41	            rollIf(x - 3);
42	            clearWallSet(st, x + 1, y, [2, 40]);
43	            rollIf(x + 2);
44	            rollIf(x + 3);
45	            // cs:15360-15364:flag=false 在非沙分支内,仅 active 才关(原在分支外)
46	            if (st.flags[ii]) open = false;
47	          }
48	        } else {
49	          // 重新开放判定:本格与下方 4 格、左右 2 格全无墙且上方 4 格无活性块
50	          let reopen = true;
51	          for (let dy = 0; dy <= 4 && reopen; dy++) if (st.wall[st.idx(x, y + dy)] !== 0) reopen = false;
52	          for (const dx of [-2, -1, 1, 2]) if (st.wall[st.idx(x + dx, y)] !== 0) reopen = false;
53	          for (let dy = 0; dy <= 3 && reopen; dy++) if (st.flags[st.idx(x, y + dy)]) reopen = false;
54	          if (reopen) open = true;
55	        }
56	      }
57	    }
58	  }
59	  // 2) 散块清除已移至 MudCaves pass（1456 调用点 cs:12526—— DirtWallCleanup 只清墙；
60	  //    此前重复跑=双倍清除偏离原版，已删）
61	}
62	
63	function clearWallSet(st: TileStore, x: number, y: number, set: number[]): boolean {
64	  if (!st.inBounds(x, y)) return false;
65	  const wl = st.wall[st.idx(x, y)];
66	  if (set.includes(wl)) { st.wall[st.idx(x, y)] = 0; return true; }
67	  return false;
68	}
69	

```


---

## 🤖 Assistant · 2026-08-12T16:53:45.896Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:53:45.900Z

**📎 ToolResult**

```
1	// 原版 pass "FinalCleanup"(1456 WorldGen.cs:22304-22670)1:1 移植。
2	//
3	// ── 建议接入位(协调者接线用) ──
4	//   原版注册序 cs:22304(BrokenTrapCleanup cs:22283 之后,是 105 pass 的最后一个
5	//   全图清理);我方应在 runBrokenTrapCleanupPass 之后调用:
6	//     runFinalCleanupPass(store, gs);
7	//
8	// 子项处置(审计裁决「补」;编号沿用审计清单):
9	//   ② FillWallHolesInArea(cs:22306)+ SecretSeed surfaceIsDesert 分支(cs:22309)——
10	//      备案跳过(FillWallHoles 我方未实装;特殊种子分支不适用普通世界)
11	//   ③ 悬空落体柱生长(cs:22312-22385):{53 沙,112 邪沙,234 猩沙,224 淤泥,123 粉砂}
12	//      下方无实心 → 地表带向下长同类型 ≤10 格(10 格内有矿轨 314 则停),停点封底
13	//      (397/398/399/147/1 按类型);非地表带直接转硬化沙族
14	//   ④ 墙 187/216(沙岩/硬沙墙)液体 → 满岩浆(cs:22387-22392;remix/dualDungeons 种子门不适用)
15	//   ⑤ 137 石板?——实为 statue/陷阱类 slope/halfBrick 复位(cs:22394-22398,无 active 门)
16	//   ⑥ 巨石重帧+补支撑(cs:22400-22458):2×2 重帧;上方有 26 祭坛则整块替换
17	//      (138/664/665/711-716 → 石 0,浮空滚动仙人掌 484 → 397)
18	//   ⑦ 液体中棕榈 323 杀(cs:22460-22463)
19	//   ⑧ 地牢墙(wallDungeon 7/8/9/94-99)内液体转水、374→373、刺 56 杀+灌满水
20	//      (cs:22465-22477)
21	//   ⑨ 314 矿轨上下清液(上 15 下 1,cs:22479-22491;extraLiquid 种子门不适用)
22	//   ⑩ 金币堆 332 下方补 332(cs:22493-22498,先 ClearEverything)
23	//   ⑪ 地表散水清除(cs:22500-22510:非满液且左右下邻皆非满液、邻格非云族)
24	//   ⑫ 无墙画作继承邻墙(cs:22512-22543,继承序:左→右→上→下)
25	//   ⑭ DirtiestBlock 彩蛋(cs:22546+)——备案跳过(审计裁决)
26	//   循环末尾的 TileFrame(i,j)(cs:22544)——跳过:帧管线统一负责,此处不重复
27	//
28	// ① Main.tileSolid[484]=false(cs:22305)——本 pass 全程生效;原版不在此还原
29	//   (Main.tileSolid 随读档重置),故 ③ 的 SolidTile 与 ⑥ 后的类型判断都要用覆写表。
30	//
31	// 零掷骰(③-⑫ 全部确定性写格)→ 不收 rng。
32	import type { TileStore } from '../../TileStore';
33	import { LIQUID_TYPE } from '../../TileStore';
34	import type { GenState } from './GenState';
35	import { TILE_DEFS, TILE_BY_KEY } from '../../../data/tiles';
36	import { idsByVanillaSheet } from './TileRunner';
37	
38	/** sheet(=原版 tile id)→ 内部 id;未实装时 0(空格)安全退化 */
39	const SHEET_TO_INTERNAL = new Map<number, number>();
40	for (const d of TILE_DEFS) {
41	  const vs = d.vanilla?.sheet;
42	  if (vs !== undefined && !SHEET_TO_INTERNAL.has(vs)) SHEET_TO_INTERNAL.set(vs, TILE_BY_KEY[d.key]);
43	}
44	const sid = (sheet: number): number => SHEET_TO_INTERNAL.get(sheet) ?? 0;
45	
46	/** ③ 落体族 → 封底/转化类型(53→397,112→398,234→399,224→147,123→1) */
47	const SAND_FALL_BASE = new Map<number, number>([
48	  [sid(53), sid(397)],
49	  [sid(112), sid(398)],
50	  [sid(234), sid(399)],
51	  [sid(224), sid(147)],
52	  [sid(123), sid(1)],
53	]);
54	/** TileID.Sets.Boulders(1456 TileID.cs:195) */
55	const BOULDERS = idsByVanillaSheet(138, 484, 664, 665, 711, 712, 713, 714, 715, 716);
56	/** TileID.Sets.Clouds(1456 TileID.cs:197) */
57	const CLOUDS = idsByVanillaSheet(189, 196, 460, 717, 718, 719);
58	/** TileID.Sets.Paintings(1456 TileID.cs:187) */
59	const PAINTINGS = idsByVanillaSheet(245, 246, 240, 241, 242);
60	/** Main.wallDungeon(Main.cs:10507-10515) */
61	const WALL_DUNGEON = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
62	
63	const ROLLING_CACTUS = sid(484);
64	const TRACK = sid(314);
65	const PALM_TREE = sid(323);
66	const COIN_PILE = sid(332);
67	const SPIKE = sid(56);
68	const LAVA_DRIP = sid(374);
69	const WATER_DRIP = sid(373);
70	const DEMON_ALTAR = sid(26);
71	const TRAP_137 = sid(137);
72	
73	/** Main.tileSolid[t](含 ① 的 484=false 覆写) */
74	function tileSolidT(t: number): boolean {
75	  if (t === ROLLING_CACTUS) return false; // ① 覆写(cs:22305)
76	  return !!TILE_DEFS[t]?.solid;
77	}
78	
79	/** WorldGen.SolidTile(cs:42370):active && tileSolid && !tileSolidTop && !halfBrick && slope==0 */
80	function solidTile(st: TileStore, x: number, y: number): boolean {
81	  if (!st.inBounds(x, y)) return false;
82	  const i = st.idx(x, y);
83	  if (!st.flags[i]) return false;
84	  const d = TILE_DEFS[st.type[i]];
85	  return !!d && tileSolidT(st.type[i]) && !d.platform && !st.half[i] && st.slope[i] === 0;
86	}
87	
88	/** 生成期 KillTile(cs:63559,生成期 noItem=true):仅清活性/类型,保留液体 */
89	function killTile(st: TileStore, x: number, y: number): void {
90	  if (!st.inBounds(x, y)) return;
91	  if (!st.flags[st.idx(x, y)]) return;
92	  st.setTileSilent(x, y, 0);
93	}
94	
95	/** slope(0)+halfBrick(false)(原版两连写,如 cs:22320-22321) */
96	function flatten(st: TileStore, x: number, y: number): void {
97	  if (!st.inBounds(x, y)) return;
98	  const i = st.idx(x, y);
99	  st.slope[i] = 0;
100	  st.half[i] = 0;
101	}
102	
103	/** Tile.ClearEverything(Tile.cs:140-151):type/wall/liquid/headers/帧全清 */
104	function clearEverything(st: TileStore, x: number, y: number): void {
105	  if (!st.inBounds(x, y)) return;
106	  const i = st.idx(x, y);
107	  st.setTileSilent(x, y, 0);
108	  st.wall[i] = 0;
109	  st.liquid[i] = 0;
110	  st.liquidType[i] = LIQUID_TYPE.NONE;
111	  st.wire[i] = 0;
112	}
113	
114	/** oceanDepths(cs:10978-10989):y 超过海洋层直接 false;横向上进沙滩带返回 true */
115	function oceanDepths(st: TileStore, gs: GenState, x: number, y: number): boolean {
116	  if (y > (gs.worldSurface + gs.rockLevel) / 2 + 40) return false;
117	  return x < gs.beachDistance || x > st.w - gs.beachDistance;
118	}
119	
120	export function runFinalCleanupPass(st: TileStore, gs: GenState): void {
121	  const { w, h } = st;
122	
123	  for (let i = 0; i < w; i++) {
124	    for (let j = 0; j < h; j++) {
125	      const t = st.idx(i, j);
126	      const type = st.type[t];
127	
128	      // ③ 悬空落体柱(cs:22312-22385)
129	      if (st.flags[t] && !solidTile(st, i, j + 1) && SAND_FALL_BASE.has(type)) {
130	        if (j < gs.worldSurface + 10 && !st.flags[st.idx(i, j + 1)]
131	          && st.wall[st.idx(i, j + 1)] !== 191 && !oceanDepths(st, gs, i, j)) {
132	          // 地表带:向下生长同类型柱
133	          let num = 10;
134	          for (let k = j + 1; k <= j + 10; k++) { // 下方 10 格内有矿轨 314 则停(cs:22321-22328)
135	            const kk = st.idx(i, k);
136	            if (st.flags[kk] && st.type[kk] === TRACK) { num = 0; break; }
137	          }
138	          let num2 = j + 1;
139	          while (!st.flags[st.idx(i, num2)] && num > 0 && num2 < h - 50) {
140	            flatten(st, i, num2 - 1);
141	            st.setTileSilent(i, num2, type);
142	            flatten(st, i, num2);
143	            num2++;
144	            num--;
145	          }
146	          if (num === 0 && !st.flags[st.idx(i, num2)]) {
147	            // 封底(cs:22345-22368)
148	            st.setTileSilent(i, num2, SAND_FALL_BASE.get(type)!);
149	          } else {
150	            const below = st.idx(i, num2);
151	            if (st.flags[below] && tileSolidT(st.type[below])
152	              && !TILE_DEFS[st.type[below]]?.platform) {
153	              flatten(st, i, num2);
154	            }
155	          }
156	        } else if (tileSolidT(st.type[st.idx(i, j + 1)])
157	          && !TILE_DEFS[st.type[st.idx(i, j + 1)]]?.platform
158	          && ((st.slope[st.idx(i, j + 1)] === 1 || st.slope[st.idx(i, j + 1)] === 2)
159	            || st.half[st.idx(i, j + 1)] === 1)) {
160	          // 下方是坡面/半砖实心 → 复位(cs:22370-22376)
161	          flatten(st, i, j + 1);
162	        } else {
163	          // 深层悬空 → 直接转硬化沙族(cs:22377-22385)
164	          st.type[t] = SAND_FALL_BASE.get(type)!;
165	        }
166	        // 棕榈重帧(cs:22386)——TileFrame 跳过(帧管线负责)
167	      }
168	
169	      // ④ 墙 187/216 液体 → 满岩浆(cs:22387-22392;remix/dualDungeons 种子门不适用)
170	      if ((st.wall[t] === 187 || st.wall[t] === 216) && st.liquid[t] > 0) {
171	        st.liquid[t] = 255;
172	        st.liquidType[t] = LIQUID_TYPE.LAVA;
173	      }
174	
175	      // ⑤ 137 复位 slope/halfBrick(cs:22394-22398,注意无 active 门)
176	      if (type === TRAP_137) {
177	        flatten(st, i, j);
178	      }
179	
180	      // ⑥ 巨石重帧+补支撑(cs:22400-22458)
181	      if (st.flags[t] && BOULDERS.has(type)) {
182	        const x0 = i - Math.floor(st.frameX[t] / 18);
183	        const y0 = j - Math.floor(st.frameY[t] / 18);
184	        let hasAltar = false;
185	        for (let l = 0; l < 2; l++) {
186	          if (st.inBounds(x0 + l, y0 - 1)) {
187	            const ab = st.idx(x0 + l, y0 - 1);
188	            if (st.flags[ab] && st.type[ab] === DEMON_ALTAR) { hasAltar = true; break; }
189	          }
190	          for (let m = 0; m < 2; m++) {
191	            st.setTileSilent(x0 + l, y0 + m, type, l * 18, m * 18);
192	          }
193	        }
194	        if (hasAltar) {
195	          // 上方有恶魔祭坛 → 整块替换(cs:22429-22450:484→397,其余→0)
196	          const repl = type === ROLLING_CACTUS ? sid(397) : 0;
197	          for (let n = 0; n < 2; n++) {
198	            for (let o = 0; o < 2; o++) {
199	              st.setTileSilent(x0 + n, y0 + o, repl, 0, 0);
200	            }
201	          }
202	        }
203	      }
204	
205	      // ⑦ 液体中棕榈杀(cs:22460-22463;原版无 active 门,经 KillTile 内部门兜底)
206	      if (type === PALM_TREE && st.liquid[t] > 0) {
207	        killTile(st, i, j);
208	      }
209	
210	      // ⑧ 地牢墙内液体规范化(cs:22465-22477)
211	      if (WALL_DUNGEON.has(st.wall[t])) {
212	        st.liquidType[t] = LIQUID_TYPE.WATER; // liquidType(0):原版无条件写位(液量为 0 时无实际意义)
213	        if (type === LAVA_DRIP) st.type[t] = WATER_DRIP;
214	        if (st.flags[t] && type === SPIKE) {
215	          killTile(st, i, j);
216	          const tt = st.idx(i, j);
217	          st.liquidType[tt] = LIQUID_TYPE.WATER;
218	          st.liquid[tt] = 255;
219	        }
220	      }
221	
222	      // ⑨ 314 矿轨上下清液(cs:22479-22491:上 15 格 + 下 1 格;extraLiquid 种子门不适用)
223	      if (st.flags[t] && type === TRACK) {
224	        for (let y2 = j; j - y2 < 15; y2--) { // j, j-1 … j-14
225	          if (y2 >= 0) st.liquid[st.idx(i, y2)] = 0;
226	        }
227	        for (let y2 = j; y2 - j < 1; y2++) { // j(原版重复清一次)
228	          if (y2 < h) st.liquid[st.idx(i, y2)] = 0;
229	        }
230	      }
231	
232	      // ⑩ 金币堆下方补 332(cs:22493-22498)
233	      if (st.flags[t] && type === COIN_PILE && !st.flags[st.idx(i, j + 1)]) {
234	        clearEverything(st, i, j + 1);
235	        st.setTileSilent(i, j + 1, COIN_PILE);
236	      }
237	
238	      // ⑪ 地表散水清除(cs:22500-22510)
239	      if (i > gs.beachDistance && i < w - gs.beachDistance && j < gs.worldSurface
240	        && st.liquid[t] > 0 && st.liquid[t] < 255
241	        && st.liquid[st.idx(i - 1, j)] < 255 && st.liquid[st.idx(i + 1, j)] < 255
242	        && st.liquid[st.idx(i, j + 1)] < 255
243	        && (!st.flags[st.idx(i - 1, j)] || !CLOUDS.has(st.type[st.idx(i - 1, j)]))
244	        && (!st.flags[st.idx(i + 1, j)] || !CLOUDS.has(st.type[st.idx(i + 1, j)]))
245	        && (!st.flags[st.idx(i, j + 1)] || !CLOUDS.has(st.type[st.idx(i, j + 1)]))) {
246	        st.liquid[t] = 0;
247	      }
248	
249	      // ⑫ 无墙画作继承邻墙(cs:22512-22543,继承序:左→右→上→下)
250	      if (st.flags[t] && type >= 0 && PAINTINGS.has(type) && st.wall[t] <= 0
251	        && i >= 2 && j >= 2 && i < w - 2 && j < h - 2) { // InWorld(i,j,2)
252	        let inherit = 0;
253	        if (inherit === 0 && st.wall[st.idx(i - 1, j)] > 0) inherit = st.wall[st.idx(i - 1, j)];
254	        if (inherit === 0 && st.wall[st.idx(i + 1, j)] > 0) inherit = st.wall[st.idx(i + 1, j)];
255	        if (inherit === 0 && st.wall[st.idx(i, j - 1)] > 0) inherit = st.wall[st.idx(i, j - 1)];
256	        if (inherit === 0 && st.wall[st.idx(i, j + 1)] > 0) inherit = st.wall[st.idx(i, j + 1)];
257	        if (inherit !== 0) st.wall[t] = inherit;
258	      }
259	
260	      // TileFrame(i,j)(cs:22544)——跳过:帧管线统一负责
261	    }
262	  }
263	}
264	

```


---

## 🤖 Assistant · 2026-08-12T16:53:51.327Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
FinalCleanup ③: sand column growth downward — if a sand tile has air below and is in surface band (j < worldSurface+10), it grows downward up to 10 tiles, converting air to sand. So if a sand tile sits above the open-air entrance hall (e.g., the sand surface that the corridor was carved into, with the corridor's roof open... actually if the dungeon corridor carved through sand terrain and left a sand tile overhanging above the open corridor (e.g., dune surface above the hall opening), FinalCleanup would extend that sand column down up to 10 tiles into the corridor. This is another candidate — same family as GravitatingSand.

Note: FinalCleanup checks `!oceanDepths` (x >= beachDistance && x <= w-beachDistance). Dungeon entrance is > 380 from edges, so it applies.

Now DesertPass — where surface sand is placed and whether before/after dungeon. It runs before dungeon (line 581). But note DesertPass resets to SANDSTONE etc. Let me read key parts of DesertPass for surface placement. Also check PilesPass (post-dungeon slot "矿骨堆") and OasisPass (post-dungeon) and MicroBiomesPass (post-dungeon) and TrapsPass (post-dungeon, in surface decor).

Let me read PilesPass and the surface portion of DesertPass, plus OasisPass sand placement, MicroBiomesPass sand/fossil placement and TrapsPass sandstone sections.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:53:51.524Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/PilesPass.ts",
 "limit": 120
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:53:51.529Z

**📎 ToolResult**

```
1	// 原版 pass 81 "Piles"（1456 WorldGen.cs:18900-19599）1:1——七个子段全量移植。
2	// ① w*0.06 洞穴堆（cs:18924）② w*0.01 深层堆（cs:19049）③ w*0.03 地表堆（cs:19118）
3	// ④ w*0.0035 地表带墙堆（cs:19184）⑤ w*0.6 全洞穴 185 小堆（cs:19261）
4	// ⑥ w*0.02 地表 185 小堆（cs:19411）⑦ w*0.15 地表墙 2/40 小堆（cs:19472）
5	// （审计清单只列了 5 段——实读原版为 7 段，progress 权重 num=7 亦印证，全量移植。）
6	// 重试预算 GetPileGenerationAttempts()=w/2（cs:23873）；每段"成功即止"（flag）。
7	// 采样域 [25,w-25]；tile 187 装饰组链（多数群系走 187，186 仅默认/地牢/冰/蘑菇草）；
8	// 全部群系样式链逐 if 抄（非互斥、后命中覆盖、命中才掷）；小堆 scatter 掷骰
9	// Next(1,5)×Next(-10,11)×Next(5)×Next(12,36)。
10	import type { TileStore } from '../../TileStore';
11	import type { RNG } from '../../../core/rng';
12	import type { GenState } from './GenState';
13	import { TILE_BY_KEY, TILE_DEFS } from '../../../data/tiles';
14	
15	const PILE185 = TILE_BY_KEY['v_185_small_decos']!;
16	const PILE186 = TILE_BY_KEY['v_186_decos_3x2']!;
17	const PILE187 = TILE_BY_KEY['v_187_decos_3x2_group_2']!;
18	
19	// 内部 tile id → 原版 sheet id 查找表（模块级一次构建）
20	const SHEET = new Int16Array(TILE_DEFS.length).fill(-1);
21	for (let i = 0; i < TILE_DEFS.length; i++) {
22	  const s = TILE_DEFS[i]?.vanilla?.sheet;
23	  if (typeof s === 'number') SHEET[i] = s;
24	}
25	
26	/** Main.wallDungeon（墙 7/8/9/94-99） */
27	const WALL_DUNGEON = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
28	/** Main.tileDungeon（tile 41/43/44/677-679，按 sheet id 存放） */
29	const TILE_DUNGEON = new Set([41, 43, 44, 677, 678, 679]);
30	/** Main.tileMoss（Main.cs:6956-6996，按 sheet id 存放） */
31	const TILE_MOSS = new Set([182, 180, 179, 381, 183, 181, 534, 536, 539, 625, 627]);
32	/** TileID.Sets.Boulders（TileID.cs:195）——PlaceSmallPile 的 InvalidTile 门 */
33	const BOULDERS = new Set([138, 484, 664, 665, 711, 712, 713, 714, 715, 716]);
34	
35	const activeAt = (st: TileStore, x: number, y: number): boolean =>
36	  st.inBounds(x, y) && st.flags[st.idx(x, y)] !== 0;
37	/** 活性格的 sheet id（非 active 返回 -1）——原版 Main.tile[x,y].type 直比的 sheet 化 */
38	const sheetAt = (st: TileStore, x: number, y: number): number => {
39	  if (!st.inBounds(x, y)) return -1;
40	  const i = st.idx(x, y);
41	  return st.flags[i] ? SHEET[st.type[i]] : -1;
42	};
43	
44	/** SolidTile2（cs:46862）：active && tileSolid && slope==0 && !halfBrick && !inActive */
45	const solidTile2 = (st: TileStore, x: number, y: number): boolean => {
46	  if (!st.inBounds(x, y)) return false;
47	  const i = st.idx(x, y);
48	  if (!st.flags[i]) return false;
49	  const d = TILE_DEFS[st.type[i]];
50	  return !!d && !!d.solid && st.slope[i] === 0 && !st.half[i];
51	};
52	
53	/** PlaceSmallPile（cs:46831）1:1：size0=1×1（fx=style*18, fy=0）；size1=2×1（fx=style*36, fy=18）。
54	 *  anyLava 拒绝；type==185 时下方 Boulders 拒绝（InvalidTileForPilesOrSpeleothems）。 */
55	function placeSmallPile(st: TileStore, x: number, y: number, pileStyle: number, pileSize: number): boolean {
56	  const i = st.idx(x, y);
57	  if (st.liquid[i] > 0 && st.liquidType[i] === 2) return false;
58	  if (pileSize === 1) {
59	    if (!solidTile2(st, x, y + 1) || !solidTile2(st, x + 1, y + 1)) return false;
60	    if (activeAt(st, x, y) || activeAt(st, x + 1, y)) return false;
61	    if (BOULDERS.has(sheetAt(st, x, y + 1)) || BOULDERS.has(sheetAt(st, x + 1, y + 1))) return false;
62	    const fx = pileStyle * 36;
63	    st.setTileSilent(x, y, PILE185, fx, 18);
64	    st.setTileSilent(x + 1, y, PILE185, fx + 18, 18);
65	    return true;
66	  }
67	  if (!solidTile2(st, x, y + 1) || activeAt(st, x, y)) return false;
68	  st.setTileSilent(x, y, PILE185, pileStyle * 18, 0);
69	  return true;
70	}
71	
72	/** PlaceTile(186/187, style) 的 3×2 对象放置（Tiles_186/187 表 stride 54px）：
73	 *  占用 (x..x+2, y-1..y) 须净空；下方 3 列须实心（AnchorBottom 语义）。
74	 *  返回是否放置成功（原版 PlaceTile 后 type==186/187 才算命中）。 */
75	function placePile3x2(st: TileStore, x: number, y: number, type: number, style: number): boolean {
76	  for (let k = 0; k < 3; k++) {
77	    for (let l = -1; l <= 0; l++) {
78	      if (!st.inBounds(x + k, y + l) || st.flags[st.idx(x + k, y + l)]) return false;
79	    }
80	    const gi = st.idx(x + k, y + 1);
81	    if (!st.flags[gi] || !TILE_DEFS[st.type[gi]]?.solid) return false;
82	  }
83	  for (let k = 0; k < 3; k++) {
84	    for (let l = -1; l <= 0; l++) {
85	      st.setTileSilent(x + k, y + l, type, style * 54 + k * 18, (l + 1) * 18);
86	    }
87	  }
88	  return true;
89	}
90	
91	/** Piles pass 主体（cs:18900-19599） */
92	export function runPilesPass(st: TileStore, rng: RNG, gs: GenState): void {
93	  const w = st.w, h = st.h;
94	  const ws = Math.floor(gs.worldSurface);
95	  /** GetPileGenerationAttempts（cs:23873）：w/2（skyblock ÷10 分支不触发） */
96	  const attempts = (): number => Math.floor(w / 2);
97	  /** oceanDepths（cs:10979）：y > oceanLevel=(ws+rl)/2+40 直接 false */
98	  const ocean = (x: number, y: number): boolean => {
99	    if (y > (gs.worldSurface + gs.rockLevel) / 2 + 40) return false;
100	    return x < gs.beachDistance || x > w - gs.beachDistance;
101	  };
102	  const shimmerAt = (x: number, y: number): boolean => {
103	    const i = st.idx(x, y);
104	    return st.liquid[i] > 0 && st.liquidType[i] === 4;
105	  };
106	  /** 原版空 for 下落：到 (x,y+1) 变 active 为止（上界 h-5） */
107	  const dropTo = (x: number, y: number): number => {
108	    let j = y;
109	    while (!st.flags[st.idx(x, j + 1)] && j < h - 5) j++;
110	    return j;
111	  };
112	  /** 小堆 scatter（cs:18996-19010 同型四处）：Next(1,5)×Next(-10,11)×Next(5)×Next(12,36) */
113	  const scatter = (x: number, y: number): void => {
114	    const n = rng.int(1, 4);
115	    for (let k = 0; k < n; k++) {
116	      const sx = x + rng.int(-10, 10);
117	      const sy0 = y - rng.int(0, 4);
118	      if (!st.flags[st.idx(sx, sy0)]) {
119	        const sy = dropTo(sx, sy0);
120	        placeSmallPile(st, sx, sy, rng.int(12, 35), 0);

```


---

## 🤖 Assistant · 2026-08-12T16:53:51.938Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"SAND\\|sand\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts | head -60",
 "description": "Find sand usage in DesertPass"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:53:51.964Z

**📎 ToolResult**

```
87:  const sandBottom = topY + desertH;                        // Desert.Bottom（沙柱底）
110:    // PlaceSandColumn：从 surfY 填到 sandBottom（沙/清液体/激活；height 可为负→零次）
111:    for (let y = surfY + (sandBottom - surfY) - 1; y >= surfY; y--) {
114:      st.type[ti] = SAND; st.flags[ti] = 1;
133:const SAND = T.SAND;
134:const SANDSTONE = TILE_BY_KEY['sandstone']!;
135:const HARDSAND = TILE_BY_KEY['hardened_sand']!;
395:    genCircle(ox, oy, 24, 12, chain(new Blotches(), outA(new SetTile(SAND), shapeData)));
409:    genOutline(px, py, data, chain(new Expand(1), new OnlyTiles(SAND), new SetTile(HARDSAND), new PlaceWall(187)));
411:      new PlaceWall(187), new OnlyTiles(SAND), new SetTile(HARDSAND));
440:    genTail(ox, oy, holeRadius * 2, 0, -holeRadius * 1.5, outA(new SetTile(SAND), data));
443:    const pairC = chain(new IsSolid(), new SetTile(HARDSAND), new PlaceWall(187));
444:    const pairD = chain(new SkipWalls(187), new SetTile(SAND));
480:    const pairB = chain(new IsSolid(), new SetTile(HARDSAND), new PlaceWall(187));
514:        else if (Math.abs(i) < n3 + 3 && value > 0.35) resetToType(cx, j, HARDSAND);
611:      let shellType: number = SAND;
612:      if (fr.nextMax(3) === 0) shellType = HARDSAND;                  // fastRandom.Next(3)
641:        if (!isEdge || st.flags[i]) resetToType(px, py, SANDSTONE);
675:      if (st.type[i] === SAND && (!s1 || !s2)) st.type[i] = HARDSAND;
703:      if (!st.flags[i] || st.type[i] !== SANDSTONE) continue;

```


---

## 🤖 Assistant · 2026-08-12T16:53:52.356Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts",
 "limit": 200,
 "offset": 60
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:53:52.361Z

**📎 ToolResult**

```
60	    // cs:10749-10779：全盒异物扫描（OOB 读 = 空格：inactive/wall 0/liquid 0）
61	    for (let k = X - num3; k <= X + num3; k++) {
62	      for (let l = i - OASIS_HEIGHT; l <= i + OASIS_HEIGHT + num4; l++) {
63	        const inB = st.inBounds(k, l);
64	        const kk = inB ? st.idx(k, l) : -1;
65	        if (inB && st.flags[kk]) {
66	          const t = st.type[kk]!;
67	          if (TILE_DEFS[t]?.solid) {
68	            if (OASIS_REJECT.has(t) && Math.abs(k - X) < num2
69	              && Math.abs(l - i) < Math.trunc(OASIS_HEIGHT / 2)) return false;
70	            if (t !== T.SAND) return false;                  // 活性实心非沙 → 拒
71	          }
72	        } else if (inB && (st.liquid[kk!] > 0 || st.wall[kk!] > 0)
73	          && Math.abs(k - X) < num2 && Math.abs(l - i) < Math.trunc(OASIS_HEIGHT / 2)) {
74	          return false;                                      // 盒心有液/墙 → 拒
75	        }
76	      }
77	      // cs:10781-10790：k > X-num2/2 && k < X-num2/2 恒假（原版笔误死代码）——无掷骰
78	    }
79	    // cs:10792-10800：边缘下探 ≤20 格（±num2 列在 i+5 行须活性无墙）
80	    const num6 = i;
81	    while (!activeAt(st, X - num2, i + 5) || wallAt(st, X - num2, i + 5) !== 0
82	      || !activeAt(st, X + num2, i + 5) || wallAt(st, X + num2, i + 5) !== 0) {
83	      i++;
84	      if (i - num6 > 20) break;
85	    }
86	    const num7 = Math.trunc(num2 / 2);                       // cs:10802
87	    // ---- 第一遍：双椭圆挖水塘 + 沙缘硬化（cs:10804-10878）----
88	    let num8 = Math.max(0, X - num2 * 3);
89	    let num9 = Math.min(st.w, X + num2 * 3);
90	    const num10 = Math.max(0, i - OASIS_HEIGHT * 4);
91	    let num11 = Math.min(st.h, i + OASIS_HEIGHT * 3);
92	    for (let m = num8; m < num9; m++) {
93	      for (let n = num10; n < num11; n++) {
94	        const num12 = Math.abs(m - X) * 0.7;
95	        const num13 = Math.abs(n - i) * 1.35;
96	        const num14 = Math.sqrt(num12 * num12 + num13 * num13);
97	        const num15 = num7 * (0.53 + rng.next() * 0.04);     // cs:10819：每格一掷 NextDouble
98	        let num16 = Math.abs(m - X) / (num9 - X);            // cs:10821
99	        num16 = 1 - num16;
100	        num16 *= 2.3;
101	        num16 *= num16;
102	        num16 *= num16;
103	        const ti = st.idx(m, n);
104	        if (num14 < num15) {
105	          // 水塘：n==i+1 半格水 127，更深处满水 255（cs:10826-10833）
106	          if (n === i + 1) st.liquid[ti] = 127;
107	          else if (n > i + 1) st.liquid[ti] = 255;
108	          if (st.liquid[ti] > 0) st.liquidType[ti] = 1;      // lava(false) → 水
109	          st.flags[ti] = 0;                                  // active(false)（保留 type 幽灵）
110	        } else if (n < i && num12 < num15 + Math.abs(n - i) * 3 * num16) {
111	          // 塘上凹缘：沙格挖空（cs:10836-10840）
112	          if (st.type[ti] === T.SAND) st.flags[ti] = 0;
113	        } else if (n >= i && num12 < num15 + Math.abs(n - i) * num16 && st.wall[ti] === 0) {
114	          // 塘下/侧缘硬化成沙（cs:10842-10854）
115	          if (st.flags[ti] && !!TILE_DEFS[st.type[ti]]?.solid
116	            && !TILE_DEFS[st.type[ti]]?.platform) {
117	            st.slope[ti] = 0;
118	            st.half[ti] = 0;
119	            continue;
120	          }
121	          st.flags[ti] = 1;
122	          st.type[ti] = T.SAND;
123	          st.slope[ti] = 0;
124	          st.half[ti] = 0;
125	        }
126	      }
127	    }
128	    // ---- 第二遍：岸线细节（cs:10857-10926）----
129	    const num17 = 50;
130	    num8 = X - num2 * 2;
131	    num9 = X + num2 * 2;
132	    num11 = i + OASIS_HEIGHT * 2;
133	    const num23 = num7 * 0.5700000000000001;                 // cs:10866
134	    for (let num18 = num8; num18 < num9; num18++) {
135	      for (let num19 = num11; num19 >= i; num19--) {
136	        const num20 = Math.abs(num18 - X) * 0.7;
137	        const num21 = Math.abs(num19 - i) * 1.35;
138	        const num22 = Math.sqrt(num20 * num20 + num21 * num21);
139	        if (num22 <= num23) continue;                        // 水塘内部不动
140	        if (activeAt(st, num18, num19) || wallAt(st, num18, num19) !== 0) continue;
141	        // 东向找岸线实体（cs:10876-10886）
142	        let num25 = -1;
143	        for (let num26 = num18; num26 <= num18 + num17
144	          && solidAt(st, num26, num19 + 1) && wallAt(st, num26, num19) <= 0; num26++) {
145	          if (activeAt(st, num26, num19) && solidAt(st, num26, num19)) {
146	            num25 = num26;
147	            break;
148	          }
149	          if (activeAt(st, num26, num19)) break;
150	        }
151	        // 西向镜像（cs:10888-10899）
152	        let num24 = -1;
153	        let num27 = num18;
154	        while (num27 >= num18 - num17 && solidAt(st, num27, num19 + 1)
155	          && wallAt(st, num27, num19) <= 0) {
156	          if (activeAt(st, num27, num19) && solidAt(st, num27, num19)) {
157	            num24 = num27;
158	            break;
159	          }
160	          if (activeAt(st, num27, num19)) break;
161	          num27--;
162	        }
163	        // cs:10901：flag 被无条件覆写为 true（原版怪癖，保留）
164	        if (num24 > -1 && num25 > -1) {
165	          let num28 = 0;
166	          for (let num29 = num24 + 1; num29 < num25; num29++) {
167	            // cs:10907-10909：岸距 >5 时 1/5 概率掷凸起高度 Next(5,10)
168	            if (num25 - num24 > 5 && rng.int(0, 4) === 0) num28 = rng.int(5, 9);
169	            st.flags[st.idx(num29, num19)] = 1;
170	            st.type[st.idx(num29, num19)] = T.SAND;
171	            if (num28 > 0) {
172	              num28--;
173	              st.flags[st.idx(num29, num19 - 1)] = 1;
174	              st.type[st.idx(num29, num19 - 1)] = T.SAND;
175	            }
176	          }
177	        }
178	      }
179	    }
180	    // cs:10929-10936：登记（上限 maxOasis=20）
181	    if (gs.numOasis < MAX_OASIS) {
182	      gs.oasisX[gs.numOasis] = X;
183	      gs.oasisY[gs.numOasis] = i;
184	      gs.oasisW[gs.numOasis] = num2;
185	      gs.numOasis++;
186	    }
187	    return true;
188	  }
189	  return false;
190	}
191	
192	/** pass 94 本体（cs:16327-16352）。cs:16329 拒绝条件：Skyblock.denyAllGeneration /
193	 *  roundLandmasses / noSurface /（蜜蜂世界且非 dontStarve）——本仓库仅建模
194	 *  skyblock 与 notTheBees（roundLandmasses/noSurface 未建模）。 */
195	export function runOasisPass(st: TileStore, rng: RNG, gs: GenState): void {
196	  if (gs.seedFlags.skyblock) return;
197	  if (gs.seedFlags.notTheBees && !gs.seedFlags.theConstant) return;
198	  let num = Math.trunc(st.w / 2100);                         // C# int 除法
199	  num += rng.int(0, 1);                                      // cs:16336 Next(2)
200	  for (let i = 0; i < num; i++) {
201	    let budget = st.w * 2;                                   // cs:16341 num3
202	    const lo = gs.beachDistance + 300;                       // cs:16340 num2
203	    while (budget > 0) {
204	      budget--;
205	      const x = rng.int(lo, st.w - lo - 1);                  // cs:16344 Next(lo, w-lo)
206	      const y = rng.int(100, gs.worldSurface - 1);           // cs:16345 Next(100, (int)worldSurface)
207	      if (placeOasis(st, rng, gs, x, y)) budget = -1;
208	    }
209	  }
210	}
211	

```


---

## 🤖 Assistant · 2026-08-12T16:54:24.789Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Oasis: requires full box of only sand or air (line 70: any active solid non-sand → reject). Dungeon bricks are solid non-sand → reject. So oasis can't overlap dungeon. Good — not a candidate, but note.

Oasis is post-dungeon and places sand (T.SAND) but gated by the sand-only box check.

PilesPass: does it check WALL_DUNGEON/TILE_DUNGEON? It defines them (lines 27-29). Let me check where used — probably for style chain. Piles place decor tiles 185/186/187, not sand. Not a sand source. But do they place on the dungeon corridor floor? They place piles — not blocking tiles (decorations). Not a sand mechanism.

Now DesertPass — runs BEFORE dungeon (WorldGen.ts:581). Surface sand placement at line ~87-114 (PlaceSandColumn) etc. Not post-dungeon. But it can create sand surface where entrance will be carved → source sand above/around entrance. Also DesertPass may place sand walls (187). Fine.

Now what about MicroBiomesPass — post-dungeon (slot 微群系, after dungeon). Check what it does with sand/fossil — line 270 wallType 171. Let me check its placement — campsites? Let's grep quickly for setTile in MicroBiomesPass near FOSSIL.

Also TrapsPass (post-dungeon, within 地表装饰 slot): lines 221-276 convert sand to sandstone/hardsand for desert dart traps — check gating (needs sand context). It converts existing SAND→SANDSTONE, doesn't add new cover in non-desert. But if the dungeon entrance is in a desert (dungeon can be in desert? desert placement maybe anywhere), traps could convert. Minor.

Also SurfaceDecorPasses — check for sand placement. Let me grep SurfaceDecorPasses for sand.

Also StructuresPass runCactusPalmTreesAndCoral (post-dungeon): palm trees placed on sand — check if they place sand bases. grep "SAND" in StructuresPass — line 533 const. Let me look at usage.

Also HalfBrickPass T.SAND (line 267) — slopes sand, not placement.

TileCleanupPass lines 172: converts hardened sand → ? Let me look: CONV_SANDSTONE — likely the "convert sandstone above sand to ..." conversion? Let me read TileCleanupPass around 150-190.

Also check SurfaceDecorPasses for sand writes, and MicroBiomes, and Traps 221-280. And importantly: is there any place AFTER dungeon that writes T.SAND at surface broadly? Candidates: GravitatingSand (fills cavities), FinalCleanup ③ (grows sand columns down ≤10), Beaches sand fill (only x<=waterX region near ocean edge), BeachDecor shell piles (T.SAND + hardened sand, only at shellStart near waterline), Oasis (gated), Traps (sand→sandstone conversion in desert).

Now also the "dungeon entrance hall" specifics: read the dungeonEnt function to see the hall carving and entStand. Let me read DungeonPass around dungeonEnt (line ~800-880?) and also dungeonStairs hall. The user asks about entrance tower/hall carving. Let me read DungeonPass 600-900.

Also confirm question 1's exact pass order list, which I have from lines 58-203.

Also check WorldGen.ts:434 (beachLeftEnd) — got it. beachDistance=380.

Critical numeric analysis for question 2:
- gs.beachLeftEnd = rng.nextIntRange(300,340) + (dungeonSide===1?40:20) → dungeonSide -1: 340..380? Wait comment says +40 for side 1? Line 434: `gs.beachLeftEnd = rng.nextIntRange(300, 340) + (gs.dungeonSide === 1 ? 40 : 20);` Hmm — for dungeonSide===1 (dungeon on right), left beach gets +40; for side -1 (dungeon left) left beach +20. So side -1: beachLeftEnd = 320..360; side 1: beachLeftEnd = 340..380. (nextIntRange(300,340) presumably inclusive 300..340 → 320-380 range accordingly.)

Hmm wait, actually for side -1 (dungeon on left), the LEFT beach is the dungeon-side beach and vanilla widens the dungeon-side beach. Our code adds 40 when side===1 to the LEFT beach, which is the non-dungeon side — that looks inverted vs vanilla but whatever; note it.

- dungeonLocation initial: side -1: rng.nextIntRange(beachLeftEnd+50, trunc(W*0.2)) → [370..410, 0.2W].
- Drift: nx ∈ [dLoc-300, dLoc+299]; accepted only if nx > beachDistance = 380 and nx < w-380. So nx min = 381 (when dLoc as low as ~370-410 and drift lands at 381). Then final gs.dungeonLocation = nx + 25 - rng.int(0,49) ∈ [nx-24, nx+25] → min ≈ 357.

So minimum possible dungeonLocation ≈ 357, while beachLeftEnd can be up to 360 (side -1) — meaning the entrance can be placed INSIDE the beach strip (x < beachLeftEnd)! And OceanSand pass already put sand there (runs before dungeon, though). But beaches basin carving reaches x <= waterX-1 ≤ 258 — doesn't reach 357.

Hmm wait, but for side -1 the left waterX cap = beachLeftEnd - 50 = 270..310; waterX = rng.int(220,259) < cap typically. So basin carve only x ≤ 258ish. So the entrance at 357+ isn't covered by basin.

But hold on — what about the RIGHT side when dungeon side is 1? waterX = clamp to beachRightStart+50 → carving x ≥ beachRightStart+50; dungeon min x = 0.8W - 300ish. For W=4200: 0.8W=3360, drift nx ∈ [3060, 3659], guard nx < w-380=3820 ok. dLoc max initial = beachRightStart-50 = W-360..W-420-50. Hmm beachRightStart = W - 320..380 - (side -1? 40 : 20) → side 1: W-320..380-20 = W-340..W-400. dLoc initial ∈ [3360, beachRightStart-50 = W-390..W-450]. Drift nx up to min(dLoc+299, w-381). So nx could be as high as w-381, i.e., 39 columns left of the carve start (beachRightStart+50 = w-290..w-350). Gap: carve start - nx = (w-290) - (w-381) = 91 minimum gap. So again no direct overlap... but the drift sets gs.dungeonLocation = nx+25-rng.int(0,49) which could be up to nx+25 → still > carve start? nx+25 vs w-290: if nx = w-381, dLoc = w-356..w-356... up to w-356 which is < w-350? borderline: carve start could be w-350 (if beachRightStart = w-400... wait beachRightStart = W-340..W-400 for side 1? Let me recompute: beachRightStart = W - nextIntRange(300,340) - (dungeonSide === -1 ? 40 : 20). For side 1: subtract 20 → beachRightStart = W-320..W-380. Cap = beachRightStart+50 = W-270..W-330. waterX clamped to that. nx max = w-381 → dLoc max = w-356. Carve start min = w-330. So dLoc (w-356) < carve start (w-330): 26 columns of gap. Close but no overlap.

OK so Beaches pass can't directly overwrite the entrance hall horizontally. But WAIT — the entrance hall is not a single column; DungeonEnt builds a tower around entPos which spans dxS1 (25-29) etc. The tower is centered at nx. Still ≥ 26 columns away.

Hmm, but hold on: is the carve loop really limited to x≥waterX? Yes `for (x = waterX; x < w; x++)`. And waterX itself gets carved.

So the "sand covering the corridor" likely comes from:
(a) GravitatingSandPass — fills air cavity below a falling tile with that tile (whole hall!). Runs after dungeon. Strong.
(b) FinalCleanupPass ③ — grows sand columns down ≤10 tiles into open air below.
(c) The precalc drift moving entrance into the beach strip where OceanSand/Desert sand exists and the corridor is carved INTO sand → corridor walls/floor of sand above; then (a)/(b) fill.

Also (d): TerrainPass beach flattening: entrance near beach is fine because dungeon runs after terrain.

Another possibility: (e) the entrance hall is carved at surface but DunesPass ran before and placed dunes at the entrance location — dunes are sand hills up to 60-99 high. Dungeon corridor then is dug into the dune; the dune sand above the corridor → GravitatingSand fills. Dunes origin ox ∈ [500, w-501], with rejection zones only jungle/center/snow. The dungeon entrance x (≥ ~357 or near 0.8W-300) could coincide with a dune (dunes width 150-250 each side, i.e., up to ±280 from origin). Possible.

Also DesertPass: deserts placed where? Let me check DesertPass location selection — could be near dungeon. And surface sand column "PlaceSandColumn" (line 87-114) fills from surfY down to sandBottom.

Let me also check the MissingCavesPass runSandPatchesPass (before dungeon) — underground sand blobs. Not covering surface corridor.

Also — check the entrance carving code: dungeonEnt — let me read it, plus dungeonStairs, and how the hall is opened (clears tiles), and check for anything that re-covers.

Also verify where runTrapsPass is invoked (in surfacePass? Let me check WorldGen for runTrapsPass call). grep.

Let me also check MicroBiomesPass for fossil/sand placement and TrapsPass 200-290. And StructuresPass palm (SAND usage). And TileCleanupPass 150-190.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:54:25.288Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"runTrapsPass\\|runPilesPass\\|runCactusPalmTreesAndCoralPass\\|runSurfaceDecorPass\" ~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts",
 "description": "Locate traps/piles/cactus pass invocation"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:54:25.348Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:243:import { runCactusPalmTreesAndCoralPass } from './vanilla/StructuresPass';
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:253:import { runTrapsPass } from './vanilla/TrapsPass';
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:254:import { runFloatingIslandsPass, runLifeCrystalsPass, runSurfaceDecorPass, runPyramidPass, runWetJunglePass, runAlchemyHerbsPass } from './vanilla/StructuresPass';
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:262:import { runPilesPass } from './vanilla/PilesPass';
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:718:  runPilesPass(store, rng, gs);
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:725:  runSurfaceDecorPass(store, rng, gs);
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:726:  runTrapsPass(store, rng, gs); // 原版 pass 76 Traps（返回 slot15 排查计数回归）
~/Project/GLM/SandboxWorld/game/src/world/gen/WorldGen.ts:762:  runCactusPalmTreesAndCoralPass(store, rng, gs);

```


---

## 🤖 Assistant · 2026-08-12T16:54:26.077Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"SAND\\|FOSSIL\\|HARDSAND\\|SANDSTONE\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts | head -40",
 "description": "Check sand usage in post-dungeon decor passes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:54:26.137Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:35:const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:36:const SANDSTONE = TILE_BY_KEY['sandstone']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:37:const HARDSAND = TILE_BY_KEY['hardened_sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:38:const FOSSIL = TILE_BY_KEY['desert_fossil']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:44:const HARDSAND_TILE = TILE_BY_KEY['hardened_sand']!; // 原版 SetTile(397)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:270:      if (t === SAND || t === SANDSTONE || t === HARDSAND || t === FOSSIL) wallType = 171;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:303:            if (st.flags[ui] && st.type[ui] === SAND) st.type[ui] = HARDSAND_TILE;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:21:const EBONSAND = TILE_BY_KEY['v_112_ebonsand_block']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:22:const CRIMSAND = TILE_BY_KEY['v_234_crimsand_block']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:529:const SANDSTONE_BRICK = TILE_BY_KEY['v_151_sandstone_brick']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:533:const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:557:    if (st.type[st.idx(num, k)] !== SAND) continue;   // cs:15455 沙列门禁
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:578:  const num = SANDSTONE_BRICK;   // 151
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:623:      if (active(n14, n13 - 1) && st.type[st.idx(n14, n13 - 1)] === SAND) flag3 = true;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:632:        st.type[k] = SAND; st.flags[k] = 1; st.half[k] = 0; st.slope[k] = 0;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:945:const SAND_CONV = idsByVanillaSheet(53, 112, 116, 234);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:947:const SAND_GATE = idsByVanillaSheet(53, 112, 234);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:969:    || (anchorType !== CACTUS && !SAND_CONV.has(anchorType))
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:988:  if (SAND_CONV.has(anchorType)) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:1004:        if (SAND_CONV.has(t)) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:1143:        if (!st.flags[ti] || !SAND_GATE.has(st.type[ti])) continue;   // cs:21208-21211
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:42:const CONV_SAND = new Set([53, 112, 116, 234]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:186:      if (!st.flags[k] || TILE_DUNGEON.has(s) || CLOUDS.has(s) || CONV_SAND.has(s) || st.wall[k] === 0) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:313:      if (!st.flags[k] || TILE_DUNGEON.has(s) || CLOUDS.has(s) || CONV_SAND.has(s)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:1514:  const sandOk = CONV_SAND.has(gs) && solidAllowBottomSlope(st, x, y + 1);

```


---

## 🤖 Assistant · 2026-08-12T16:54:26.321Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts",
 "limit": 110,
 "offset": 200
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:54:26.337Z

**📎 ToolResult**

```
200	  // 压板 + 飞镖 + L 线
201	  st.setTileSilent(px, py, PLATE, 0, st.wall[st.idx(px, py)] > 0 ? 36 : rng.int(2, 3) * 18);
202	  st.setTileSilent(i5, j2, TRAP, dir === 1 ? 18 : 0, 0);
203	  lWire(st, px, py, i5, j2);
204	  return true;
205	}
206	
207	function isCracked(t: number): boolean {
208	  return t === (TILE_BY_KEY['v_481_cracked_blue_brick'] ?? -1)
209	    || t === (TILE_BY_KEY['v_482_cracked_green_brick'] ?? -1)
210	    || t === (TILE_BY_KEY['v_483_cracked_pink_brick'] ?? -1);
211	}
212	
213	/** PlaceSandTrap（cs:19962-20085）：地下沙漠蜂窝墙内的塌沙陷阱 */
214	function placeSandTrap(st: TileStore, rng: RNG, i: number, j: number): boolean {
215	  const num2 = 4, num3 = 25;
216	  let y = j;
217	  while (!st.flags[st.idx(i, y)] && y < st.h - 200) y++;
218	  const gi = st.idx(i, y);
219	  if (!st.flags[gi]) return false;
220	  const t = st.type[gi];
221	  if (!(t === SAND || t === SANDSTONE || t === HARDSAND)) return false;
222	  if (st.wall[gi] !== 216 && st.wall[gi] !== 187) return false;
223	  const j1 = y - 1;
224	  let sandTop = -1;
225	  for (let yy = j1; yy > j1 - 30; yy--) {
226	    if (st.flags[st.idx(i, yy)]) {
227	      if (st.type[st.idx(i, yy)] !== SANDSTONE) return false;
228	      sandTop = yy;
229	      break;
230	    }
231	  }
232	  const pocketW = rng.int(6, 11);   // Next(6,12)
233	  const pocketH = rng.int(6, 13);   // Next(6,14)
234	  if (sandTop <= -1 || j1 - sandTop < pocketH + num2) return false;
235	  // ±25 无线/箱/画/门/闸/牌（cs:19987-19995）
236	  for (let dx = -num3; dx <= num3; dx++) {
237	    for (let dy = -num3; dy < num3; dy++) {
238	      const xx = i + dx, yy = j1 + dy;
239	      if (!st.inBounds(xx, yy)) continue;
240	      const ii = st.idx(xx, yy);
241	      const tt = st.type[ii];
242	      if (st.wire[ii] || tt === CHEST || tt === CHEST2 || tt === DOOR || tt === GATE || tt === SIGN) return false;
243	    }
244	  }
245	  // ±2 下 3 格实心
246	  for (let dx = -2; dx <= 2; dx++) {
247	    for (let dy = 1; dy <= 3; dy++) {
248	      if (!st.flags[st.idx(i + dx, j1 + dy)]) return false;
249	    }
250	  }
251	  // 腰线全空 + 下方实心率 75%（cs:20006-20024）
252	  const mid = Math.floor((j1 + sandTop) / 2);
253	  let solidN = 0;
254	  for (let dx = -pocketW; dx <= pocketW; dx++) {
255	    if (st.flags[st.idx(i + dx, mid)]) return false;
256	    for (let dy = sandTop - pocketH; dy <= sandTop; dy++) {
257	      const ii = st.idx(i + dx, dy);
258	      if (st.flags[ii] && solidAt(st, i + dx, dy)) {
259	        if (isOre(st.type[ii]) || st.type[ii] === HARDSAND) return false;
260	        solidN++;
261	      }
262	    }
263	  }
264	  if (solidN < (pocketW * 2 + 1) * (pocketH + 1) * 0.75) return false;
265	  // 掏沙穴 + 壳（cs:20028-20064）：中空纯沙，底/边砂岩，顶硬化沙
266	  for (let dx = -pocketW - 1; dx <= pocketW + 1; dx++) {
267	    for (let dy = sandTop - pocketH; dy <= sandTop; dy++) {
268	      const xx = i + dx, yy = dy;
269	      if (!st.inBounds(xx, yy)) continue;
270	      const flag = st.flags[st.idx(xx, yy)] && solidAt(st, xx, yy);
271	      if (dy === sandTop) {
272	        if (!flag) st.setTileSilent(xx, yy, SANDSTONE);
273	      } else if (dy === sandTop - pocketH) {
274	        st.setTileSilent(xx, yy, !flag || !st.flags[st.idx(xx, yy - 1)] ? SANDSTONE : HARDSAND);
275	      } else if (dx === -pocketW - 1 || dx === pocketW + 1) {
276	        if (!flag) st.setTileSilent(xx, yy, SANDSTONE);
277	      } else {
278	        st.setTileSilent(xx, yy, SAND);
279	      }
280	    }
281	  }
282	  return true;
283	}
284	
285	let _oreSet: Set<number> | null = null;
286	function isOre(t: number): boolean {
287	  if (!_oreSet) {
288	    _oreSet = new Set<number>();
289	    TILE_DEFS.forEach((d, i) => { if (d?.key?.startsWith('ore_')) _oreSet!.add(i); });
290	  }
291	  return _oreSet.has(t);
292	}
293	
294	/** pass 76 Traps 主体（cs:18796-18896）：w*0.05 次 placeTrap + w*0.003 次 PlaceSandTrap。
295	 *  两段计数均为裸 double 比较（cs:18789/18866 `for i < num`，不取整） */
296	export function runTrapsPass(st: TileStore, rng: RNG, gs: GenState): void {
297	  bouldersPlaced.length = 0; // 模块级状态须按次生成重置，否则同种子双生成发散
298	  const trapTries = st.w * 0.05;
299	  for (let n = 0; n < trapTries; n++) {
300	    for (let k = 0; k < 1150; k++) {
301	      let x = rng.int(200, st.w - 201);                       // Next(200, w-200)
302	      let y = rng.int(gs.worldSurface, st.h - 211);           // Next(surface, h-210)
303	      // oceanDepths 回避（cs:18821）——海滩带是常量 beachDistance=380（cs:4102），
304	      // 非 beachLeftEnd/RightStart（那是 Reset 掷的海滩宽，不是回避带）
305	      const oceanTop = (gs.worldSurface + gs.rockLevel) / 2 + 40;
306	      while (y <= oceanTop && (x < gs.beachDistance || x > st.w - gs.beachDistance)) {
307	        x = rng.int(200, st.w - 201);
308	        y = rng.int(gs.worldSurface, st.h - 211);
309	      }

```


---

## 🤖 Assistant · 2026-08-12T16:54:31.134Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Traps: placeSandTrap is deep (y >= worldSurface) and requires wall 187/216 sand walls — underground desert only. Not the entrance.

MicroBiomesPass line 303: converts SAND→HARDSAND near campsites? MicroBiomes is post-dungeon; it only converts existing sand. Doesn't add sand cover.

StructuresPass line 632: `st.type[k] = SAND` — what is that? Around pyramid or palm? Let me check lines 540-640. It's likely the Pyramid pass placing sand around the pyramid base? Pyramid is placed from gs.pyramidSpots — near beaches/desert dunes. Post-dungeon (runPyramidPass at line 619 in WorldGen after dungeon 593!). Let me read StructuresPass 529-660 to see whether it can place sand onto the entrance. Pyramid spots come from OceanSand (mid column of beach strip) and Dunes pass (origin ±200). Dunes origin can be anywhere in [500, w-501] — could coincide with the dungeon entrance area! Pyramid then digs/builds with sandstone brick and sand. If a pyramid spot lands on the dungeon entrance... but pyramids are built before/after? runPyramidPass is after dungeon. Hmm, that's a candidate but requires overlap.

Let me read StructuresPass 540-660.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:54:31.378Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts",
 "limit": 140,
 "offset": 525
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:54:31.392Z

**📎 ToolResult**

```
525	    }
526	  }
527	}
528	
529	const SANDSTONE_BRICK = TILE_BY_KEY['v_151_sandstone_brick']!;
530	const TORCH = TILE_BY_KEY['torch']!;
531	const POT = TILE_BY_KEY['pot']!;
532	const SMALL185 = TILE_BY_KEY['v_185_small_decos']!;
533	const SAND = TILE_BY_KEY['sand']!;
534	const DUNGEON_WALLS = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
535	
536	/** Pyramids pass（1456 cs:15426-15534）1:1：候选全部来自 DunesPass（GenVars.PyrX/PyrY）。
537	 *  校验链：x∈(300,w-300) → 地牢侧带回避（cs:15450-15452）→ 自 PyrY 下扫首个活性格
538	 *  须 < worldSurface 且为沙 53 → 与**全部先序候选**（含已被拒者）距 ≥220 → k-- 后 Pyramid()。
539	 *  无候选时直接无金字塔（原版路径如此；旧自掷兜底已删——非原版且白耗 RNG）。 */
540	export function runPyramidPass(
541	  st: TileStore, rng: RNG, gs: GenState,
542	  chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null> }>,
543	): void {
544	  const accepted: Array<{ x: number; y: number }> = [];
545	  for (let idx = 0; idx < gs.pyramidSpots.length; idx++) {
546	    const cand = gs.pyramidSpots[idx];
547	    const num = cand.x;
548	    if (num <= 300 || num >= st.w - 300) continue;
549	    // 地牢侧回避（cs:15450-15452）：dungeonSide>Left 时须 num ≥ dungeonX+0.15w；
550	    // dungeonSide<Right 时须 num ≤ dungeonX-0.15w（任一不过即拒）
551	    const band = st.w * 0.15;
552	    if (!(gs.dungeonSide > -1 || !(num < gs.dungeonLocation + band))) continue;
553	    if (!(gs.dungeonSide < 1 || !(num > gs.dungeonLocation - band))) continue;
554	    let k = cand.y;
555	    while (k < st.h && st.inBounds(num, k) && !st.flags[st.idx(num, k)]) k++;
556	    if (k >= gs.worldSurface) continue;
557	    if (st.type[st.idx(num, k)] !== SAND) continue;   // cs:15455 沙列门禁
558	    // 与全部先序候选（PyrX[0..idx-1]）取最小距，须 ≥220（cs:15460-15472）
559	    let minDist = st.w;
560	    for (let l = 0; l < idx; l++) minDist = Math.min(minDist, Math.abs(num - gs.pyramidSpots[l].x));
561	    if (minDist >= 220) {
562	      k--;
563	      pyramid(st, rng, gs, chests, num, k, 75, 125, false);
564	      accepted.push({ x: num, y: k });
565	    }
566	  }
567	}
568	
569	/** WorldGen.Pyramid（1456 cs:27816-28160）1:1：沙岩砖 151 主体 + 墙 34 +
570	 *  入口阶梯掏空 → 之字形下行隧道（端点房间：金箱 1 号主件 848/857/934 三选一、
571	 *  小堆 185×N、四支火把 91、整排瓦罐 28 style25-27）→ 长出口隧道。
572	 *  RNG 消费顺序逐掷对齐（num2/num3/num5/num8/num11/num12/房间段/出口段）。 */
573	function pyramid(
574	  st: TileStore, rng: RNG, gs: GenState,
575	  chests: Array<{ x: number; y: number; items: Array<{ id: number; stack: number } | null> }>,
576	  i: number, j: number, pyramidMinDepth: number, pyramidMaxDepth: number, noTunnel: boolean,
577	): boolean {
578	  const num = SANDSTONE_BRICK;   // 151
579	  const wall = 34;               // SandstoneBrickUnsafe
580	  const gi = st.idx(i, j);
581	  if (st.flags[gi] && (st.type[gi] === num || st.wall[gi] === 151)) return false;
582	  const active = (x: number, y: number) => st.inBounds(x, y) && st.flags[st.idx(x, y)] !== 0;
583	  const deact = (x: number, y: number) => { if (st.inBounds(x, y)) st.flags[st.idx(x, y)] = 0; };
584	  const setBrick = (x: number, y: number) => {
585	    if (!st.inBounds(x, y)) return;
586	    const k = st.idx(x, y);
587	    st.type[k] = num; st.flags[k] = 1; st.half[k] = 0; st.slope[k] = 0;
588	  };
589	  const num2 = j - rng.int(0, 6);                       // j - Next(0,7)
590	  const num3 = rng.int(9, 12);                          // Next(9,13)
591	  let num4 = 1;
592	  const num5 = j + rng.int(pyramidMinDepth, pyramidMaxDepth - 1); // Next(75,125)
593	  // 主体：逐层加宽的实心沙岩砖塔（cs:27859-27868）
594	  for (let k = num2; k < num5; k++) {
595	    for (let l = i - num4; l < i + num4 - 1; l++) setBrick(l, k);
596	    num4++;
597	  }
598	  // 封闭区刷墙 34（cs:27870-27888：3×3 全砖）
599	  for (let m = i - num4 - 5; m <= i + num4 + 5; m++) {
600	    for (let n = j - 1; n <= num5 + 1; n++) {
601	      let all = true;
602	      for (let a = m - 1; a <= m + 1 && all; a++) {
603	        for (let b = n - 1; b <= n + 1; b++) {
604	          if (!st.inBounds(a, b) || !st.flags[st.idx(a, b)] || st.type[st.idx(a, b)] !== num) { all = false; break; }
605	        }
606	      }
607	      if (all && st.inBounds(m, n)) st.wall[st.idx(m, n)] = wall;
608	    }
609	  }
610	  let num8 = 1;
611	  if (rng.int(0, 1) === 0) num8 = -1;                   // Next(2)==0 → -1
612	  let num9 = i - num3 * num8;
613	  let num10 = j + num3;
614	  const num11 = rng.int(5, 7);                          // Next(5,8)
615	  let flag2 = true;
616	  let num12 = rng.int(20, 29);                          // Next(20,30)
617	  // 入口掏空（cs:27903-27924）：自沙面斜向下切阶梯
618	  while (flag2) {
619	    flag2 = false;
620	    let flag3 = false;
621	    for (let n13 = num10; n13 <= num10 + num11; n13++) {
622	      const n14 = num9;
623	      if (active(n14, n13 - 1) && st.type[st.idx(n14, n13 - 1)] === SAND) flag3 = true;
624	      if (active(n14, n13) && st.type[st.idx(n14, n13)] === num) {
625	        if (st.inBounds(n14, n13 + 1)) st.wall[st.idx(n14, n13 + 1)] = wall;
626	        if (st.inBounds(n14 + num8, n13)) st.wall[st.idx(n14 + num8, n13)] = wall;
627	        deact(n14, n13);
628	        flag2 = true;
629	      }
630	      if (flag3 && st.inBounds(n14, n13)) {
631	        const k = st.idx(n14, n13);
632	        st.type[k] = SAND; st.flags[k] = 1; st.half[k] = 0; st.slope[k] = 0;
633	      }
634	    }
635	    num9 -= num8;
636	  }
637	  num9 = i - num3 * num8;
638	  let flag4 = true;
639	  let flag5 = false;
640	  flag2 = true;
641	  // 之字形下行隧道 + 端点房间（cs:27928-28046）
642	  while (flag2) {
643	    for (let n15 = num10; n15 <= num10 + num11; n15++) deact(num9, n15);
644	    num9 += num8;
645	    num10++;
646	    num12--;
647	    if (num10 >= num5 - num11 * 2) num12 = 10;
648	    if (num12 <= 0) {
649	      let flag6 = false;
650	      if (!flag4 && !flag5) {
651	        if (noTunnel) flag2 = false;
652	        flag5 = true;
653	        flag6 = true;
654	        const num17 = rng.int(7, 12);                   // Next(7,13)
655	        const num18 = rng.int(23, 27);                  // Next(23,28)
656	        const num19 = num18;
657	        const num20 = num9;
658	        let cur = num18;
659	        while (cur > 0) {
660	          for (let n21 = num10 - num17 + num11; n21 <= num10 + num11; n21++) {
661	            if (cur === num19 || cur === 1) {
662	              if (n21 >= num10 - num17 + num11 + 2) deact(num9, n21);
663	            } else if (cur === num19 - 1 || cur === 2 || cur === num19 - 2 || cur === 3) {
664	              if (n21 >= num10 - num17 + num11 + 1) deact(num9, n21);

```


---

## 🤖 Assistant · 2026-08-12T16:54:32.265Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"TILE_DUNGEON\\|WALL_DUNGEON\\|tileDungeon\\|wallDungeon\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/*.ts | grep -v \"^.*PilesPass\\|LivingTreePass\\|BuriedChestsPass\\|DungeonPass\"",
 "description": "Find dungeon gating outside known passes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:54:32.342Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:38:/** CanEvilReplace(WorldGen.cs:76182-76197):地牢砖族(tileDungeon 41/43/44/677-679,Main.cs:7941-7946)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:39: *  /裂砖族(CrackedBricks 481-483)/地牢墙(wallDungeon 7-9/94-99,Main.cs:10507-10515)不可替换 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:40:const TILE_DUNGEON = new Set([41, 43, 44, 677, 678, 679]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:41:const WALL_DUNGEON = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:46:    if (TILE_DUNGEON.has(sheet) || (sheet >= 481 && sheet <= 483)) return false;  // tileDungeon ∪ CrackedBricks
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:48:  return !WALL_DUNGEON.has(st.wall[i]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:19://   ⑧ 地牢墙(wallDungeon 7/8/9/94-99)内液体转水、374→373、刺 56 杀+灌满水
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:60:/** Main.wallDungeon(Main.cs:10507-10515) */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:61:const WALL_DUNGEON = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:211:      if (WALL_DUNGEON.has(st.wall[t])) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GemPasses.ts:35:/** 地牢墙（Main.wallDungeon）：7/8/9 + 94-99 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GemPasses.ts:36:const WALL_DUNGEON = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GemPasses.ts:247:    if (wl === 27 || WALL_DUNGEON.has(wl)) continue;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MossPass.ts:28:/** Main.tileDungeon（Main.cs:7941-7946：41 青砖/43 蓝砖/44 绿砖/677-679 变体） */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MossPass.ts:140:        // 161 冰/147 雪砖/396/397 硬化沙族 + Main.tileDungeon）；墙不参与
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts:134:/** 原版 tileDungeon（Main.cs:7941-7946）与 wallDungeon（Main.cs:10507-10515） */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts:135:const TILE_DUNGEON = idsByVanillaSheet(41, 43, 44, 677, 678, 679);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts:136:const WALL_DUNGEON = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts:154:    // ★地牢命中即整轮终止（cs:80753-80762）：tileDungeon/墙 dungeon → num4=0
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts:163:          if ((active && TILE_DUNGEON.has(st.type[kk])) || WALL_DUNGEON.has(st.wall[kk])) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OceanCavesPass.ts:18:/** tileDungeon 族(Main.cs:7941-7946),sheet id 比较(内部 id ≠ sheet id) */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OceanCavesPass.ts:19:const TILE_DUNGEON = new Set([41, 43, 44, 677, 678, 679]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OceanCavesPass.ts:24:/** badOceanCaveTiles(cs:76679):墙 83/3/地牢墙 或 tile 203/25/tileDungeon 族/26/31 → 跳过
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OceanCavesPass.ts:32:  if (sheet === 203 || sheet === 25 || TILE_DUNGEON.has(sheet) || sheet === 26 || sheet === 31) return true;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:24://  - Main.tileDungeon 用 dungeon 砖 tile 近似(41/43/44),容器用 chest 族 key 近似
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:75:/** Main.tileDungeon(Main.cs:7941-7944) */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:255:        // Main.tileDungeon 近似:三种地牢砖(41/43/44)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts:440: *  锚行 num = k-1。anyLava/anyShimmer/EmptyTileCheck/wallDungeon 四门 →
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:45:/** Main.tileDungeon（Main.cs:7941-7946） */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:46:const TILE_DUNGEON = new Set([41, 43, 44, 677, 678, 679]);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:186:      if (!st.flags[k] || TILE_DUNGEON.has(s) || CLOUDS.has(s) || CONV_SAND.has(s) || st.wall[k] === 0) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:313:      if (!st.flags[k] || TILE_DUNGEON.has(s) || CLOUDS.has(s) || CONV_SAND.has(s)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:437:              if (s === 189 || s === 53 || TILE_DUNGEON.has(s)

```


---

## 🤖 Assistant · 2026-08-12T16:54:43.721Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Notable: BeachPass has NO dungeon gating. GravitatingSandPass has none. FinalCleanupPass none (except dungeon wall handling for liquids).

Also SurfaceDecorPasses has TILE_DUNGEON gating for grass/dirt decor (lines 186, 313, 437) — good to cite as "where gating exists."

Now, important remaining: read the dungeonEnt / dungeonStairs carving to describe the entrance hall and check for anything in DungeonPass that protects/doesn't protect. Also check DungeonPass for how the entrance hall is opened (e.g., "MakeDungeonEnt" clears surface). Let me read DungeonPass lines ~780-1000 (dungeonEnt + halls).

Also I should double check the order claim: is '引力沙' slot really after 生物群系? The passes array: [0] 原版地形, [1] 沙丘, [2] 洞穴, [3] 生物群系, [4] 液体 (empty), [5] 引力沙, [6] 微光, [7] 清理, [8] 水体沉降, [9] 沙上清水, [10] 绿洲, [11] 海滩装饰, [12] 半砖平滑, ... Yes. And the comment at line 72-74 says the gravitating sand pass runs after Lakes and before Shimmer per vanilla registration order (GravitatingSandCleanup cs:15198), matching vanilla's pass 36 which is after Dungeon 32 and Beaches 34. Good — so order matches vanilla; the vanilla behavior would also fill the dungeon corridor if a falling tile overhangs it.

Hmm — but wait. In vanilla, does the GravitatingSand fill happen only y < worldSurface and requires the cavity to be fully air? Our implementation mirrors vanilla. In vanilla, the dungeon entrance has a tower with roof, so sand above the tower roof wouldn't be overhanging the hall. But if the entrance is carved into a sand dune/beach slope where the corridor mouth opens sideways into a slope... the drift could place it oddly.

Actually, more importantly: is there a real known vanilla difference? Vanilla DungeonEnt builds the tower and then `MakeDungeonEntrance`/corridor. Also vanilla's dungeon placement: dungeonLocation from Reset is used directly in vanilla 1456? In vanilla 1456, the dungeon crawler precalc (DungeonCrawler.cs L280-326) does the ±300 rejection sampling and then ANCHOR MOVES to entrance. In vanilla the guard is likely also beachDistance... Our port matches.

But crucially: in VANILLA, is the entrance tower's corridor carved such that sand can't cover it? Vanilla has the same passes. So the "sometimes blocked" may be a real vanilla-compatible behavior amplified by differences, OR caused by a genuine deviation. Since the user just wants candidate mechanisms, I'll list them with citations and assess likelihood.

Let me now read the DungeonPass entrance functions to describe the carving, and check whether the hall is cleared of sand (e.g., does dungeonEnt clear tiles above?). Read lines 600-1000.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:54:43.864Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts",
 "limit": 220,
 "offset": 560
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:54:43.899Z

**📎 ToolResult**

```
560	  const t1 = Math.floor(cy - dy1 * 0.6 - rng.int(2, 4));
561	  const b1 = Math.floor(cy + dy1 * 0.6 + rng.int(8, 15));
562	  for (let x = l1; x < r1; x++) {
563	    for (let y = t1; y < b1; y++) {
564	      fillB(x, y, x > l1 + 1 && x < r1 - 2 && y > t1 + 1 && y < b1 - 2);
565	    }
566	  }
567	  // 垛口(左右块 5+Next(4) 宽、3+Next(3) 高)
568	  for (const sd of [-1, 1]) {
569	    const bx0 = sd < 0 ? l1 : r1 - 5 - rng.int(0, 3);
570	    const bx1 = sd < 0 ? l1 + 5 + rng.int(0, 3) : r1;
571	    const by0 = t1 - 3 - rng.int(0, 2);
572	    for (let x = bx0; x < bx1; x++) for (let y = by0; y < t1; y++) fillB(x, y, false);
573	  }
574	  // 顶齿(齿高 1+Next(2),周期 2+Next(4):刷 num16 列跳 num16 列)
575	  const th1 = 1 + rng.int(0, 1);
576	  const tp1 = 2 + rng.int(0, 3);
577	  let cnt = 0;
578	  for (let x = l1; x < r1; x++) {
579	    for (let y = t1 - th1; y < t1; y++) fillB(x, y, false);
580	    if (++cnt >= tp1) { x += tp1; cnt = 0; }
581	  }
582	  // 下延到 worldSurface(num6 → worldSurface):填砖,内列刷墙
583	  for (let x = l1; x < r1; x++) {
584	    for (let y = b1; y < Math.min(st.h, Math.floor(gs.worldSurface)); y++) {
585	      extFill(x, y, false, x > l1 && x < r1 - 1);
586	    }
587	  }
588	  // 0.6 框刷墙(精确,无抖动)×2
589	  for (let pass = 0; pass < 2; pass++) {
590	    for (let x = Math.floor(cx - dx1 * 0.6) - (pass ? 1 : 0); x <= Math.floor(cx + dx1 * 0.6) + (pass ? 1 : 0); x++) {
591	      for (let y = Math.floor(cy - dy1 * 0.6) - (pass ? 1 : 0); y <= Math.floor(cy + dy1 * 0.6) + (pass ? 1 : 0); y++) {
592	        if (!st.inBounds(x, y)) continue;
593	        const ti = st.idx(x, y);
594	        st.liquid[ti] = 0; st.wall[ti] = dc.wall;
595	      }
596	    }
597	  }
598	  // 0.5 框清空(塔内厅)
599	  for (let x = Math.floor(cx - dx1 * 0.5); x < Math.floor(cx + dx1 * 0.5); x++) {
600	    for (let y = Math.floor(cy - dy1 * 0.5); y < Math.floor(cy + dy1 * 0.5); y++) {
601	      if (!st.inBounds(x, y)) continue;
602	      const ti = st.idx(x, y);
603	      st.liquid[ti] = 0; st.flags[ti] = 0; st.wall[ti] = dc.wall;
604	    }
605	  }
606	  // 塔底井口(连通楼梯竖井,原版由 DungeonStairs 自带)
607	  for (let x = -1; x <= 1; x++) {
608	    for (let y = Math.floor(cy + dy1 * 0.5); y < Math.floor(cy + dy1 * 0.5) + 4; y++) {
609	      if (st.inBounds(Math.floor(cx) + x, y)) {
610	        const ti = st.idx(Math.floor(cx) + x, y);
611	        st.flags[ti] = 0; st.wall[ti] = dc.wall;
612	      }
613	    }
614	  }
615	  // ---- 外门厅段 ----
616	  cx += dx1 * 0.6 * dir;
617	  cy += dy1 * 0.5;
618	  const dx2 = rng.int(35, 49) + 0.0, dy2 = rng.int(10, 14) + 0.0;
619	  cx += dx2 * 0.55 * dir;
620	  cy -= dy2 * 0.5;
621	  const l2 = Math.floor(cx - dx2 * 0.6 - rng.int(1, 2));
622	  const r2 = Math.floor(cx + dx2 * 0.6 + rng.int(1, 2));
623	  const t2 = Math.floor(cy - dy2 * 0.6 - rng.int(1, 2));
624	  const b2 = Math.floor(cy + dy2 * 0.6 + rng.int(6, 15));
625	  // 只填远侧半(num2<0 → x >= X-dx2*0.5;否则 x <= X+dx2*0.5-1)
626	  for (let x = l2; x < r2; x++) {
627	    for (let y = t2; y < b2; y++) {
628	      const far = dir < 0 ? x >= cx - dx2 * 0.5 : x <= cx + dx2 * 0.5 - 1;
629	      if (!far) continue;
630	      if (!st.inBounds(x, y)) continue;
631	      const ti = st.idx(x, y);
632	      st.liquid[ti] = 0;
633	      if (!isDW(x, y)) { st.wall[ti] = 0; st.type[ti] = dc.brick; st.flags[ti] = 1; }
634	    }
635	  }
636	  // 下延(全列刷墙)
637	  for (let x = l2; x < r2; x++) {
638	    for (let y = b2; y < Math.min(st.h, Math.floor(gs.worldSurface)); y++) extFill(x, y, true, false);
639	  }
640	  // 外段垛口(0.5 边缘:块1 从 num34(+1 若 dir<0) 起 5+Next(4) 宽;块2 [num35-5-Next(4), num35))
641	  const n34 = Math.floor(cx - dx2 * 0.5);
642	  let n35 = Math.floor(cx + dx2 * 0.5);
643	  const n36 = dir < 0 ? n34 + 1 : n34;
644	  {
645	    const by0 = t2 - 3 - rng.int(0, 2);
646	    for (let x = n36; x < n36 + 5 + rng.int(0, 3); x++) {
647	      for (let y = by0; y < t2; y++) {
648	        if (!st.inBounds(x, y)) continue;
649	        const ti = st.idx(x, y);
650	        st.liquid[ti] = 0;
651	        if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
652	      }
653	    }
654	    const bx0 = n35 - 5 - rng.int(0, 3);
655	    for (let x = bx0; x < n35; x++) {
656	      for (let y = by0; y < t2; y++) {
657	        if (!st.inBounds(x, y)) continue;
658	        const ti = st.idx(x, y);
659	        st.liquid[ti] = 0;
660	        if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
661	      }
662	    }
663	  }
664	  // 外段顶齿(dir<0 时 num35++)
665	  if (dir < 0) n35++;
666	  const th2 = 1 + rng.int(0, 1);
667	  const tp2 = 2 + rng.int(0, 3);
668	  cnt = 0;
669	  for (let x = n34 + 1; x < n35 - 1; x++) {
670	    for (let y = t2 - th2; y < t2; y++) {
671	      if (!st.inBounds(x, y)) continue;
672	      const ti = st.idx(x, y);
673	      st.liquid[ti] = 0;
674	      if (!isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
675	    }
676	    if (++cnt >= tp2) { x += tp2; cnt = 0; }
677	  }
678	  // 0.6 框清墙(开放感)
679	  for (let x = Math.floor(cx - dx2 * 0.6); x < Math.floor(cx + dx2 * 0.6); x++) {
680	    for (let y = Math.floor(cy - dy2 * 0.6); y < Math.floor(cy + dy2 * 0.6); y++) {
681	      if (!st.inBounds(x, y)) continue;
682	      st.liquid[st.idx(x, y)] = 0;
683	      st.wall[st.idx(x, y)] = 0;
684	    }
685	  }
686	  // 0.5 框:active=false + wall=0(开放门厅——老头 NPC 位)
687	  const n51 = Math.floor(cx - dx2 * 0.5), n52 = Math.floor(cx + dx2 * 0.5);
688	  const n53 = Math.floor(cy - dy2 * 0.5), n54 = Math.floor(cy + dy2 * 0.5);
689	  for (let x = n51; x < n52; x++) {
690	    for (let y = n53; y < n54; y++) {
691	      if (!st.inBounds(x, y)) continue;
692	      const ti = st.idx(x, y);
693	      st.liquid[ti] = 0; st.flags[ti] = 0; st.wall[ti] = 0;
694	    }
695	  }
696	  // 100 列砖坡(对角步降,清上方 4 行)
697	  {
698	    const slope = 100;
699	    let step = 0;
700	    if (dir === 1) {
701	      for (let x = n52; x < n52 + slope; x++) {
702	        step++;
703	        for (let y = n54 + step; y < n54 + slope; y++) {
704	          if (!st.inBounds(x, y)) continue;
705	          const ti = st.idx(x, y);
706	          st.liquid[ti] = 0;
707	          if (st.wall[ti] !== 3 && st.wall[ti] !== 83 && !isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
708	        }
709	      }
710	    } else {
711	      for (let x = n51; x > n51 - slope; x--) {
712	        step++;
713	        for (let y = n54 + step; y < n54 + slope; y++) {
714	          if (!st.inBounds(x, y)) continue;
715	          const ti = st.idx(x, y);
716	          st.liquid[ti] = 0;
717	          if (st.wall[ti] !== 3 && st.wall[ti] !== 83 && !isDW(x, y)) { st.type[ti] = dc.brick; st.flags[ti] = 1; }
718	        }
719	      }
720	    }
721	  }
722	  // 条纹窗墙([num61, num60) × [num53, num54+1],刷 2-5 列跳 2 倍)
723	  {
724	    const n61 = n58t(n51, dir), n60 = n59t(n52, dir);
725	    const sp = 2 + rng.int(0, 3);
726	    let c2 = 0;
727	    for (let x = n61; x < n60; x++) {
728	      for (let y = n53; y < n54 + 1; y++) {
729	        if (st.inBounds(x, y)) st.wall[st.idx(x, y)] = dc.wall;
730	      }
731	      if (++c2 >= sp) { x += sp * 2; c2 = 0; }
732	    }
733	  }
734	  // 门洞 15×3 + 门(style13):中心回退 dx2*0.6*dir,Y += dy2/2 后再 -1.5
735	  cx -= dx2 * 0.6 * dir;
736	  cy += dy2 * 0.5;
737	  cy -= 1.5;
738	  const dL = Math.floor(cx - 7.5), dR = Math.floor(cx + 7.5);
739	  const dT = Math.floor(cy - 1.5), dB = Math.floor(cy + 1.5);
740	  for (let x = dL; x < dR; x++) {
741	    for (let y = dT; y < dB; y++) {
742	      if (st.inBounds(x, y)) st.flags[st.idx(x, y)] = 0;
743	    }
744	  }
745	  if (dir < 0) cx -= 1;
746	  // 原版 L21242 PlaceTile(x, Y+1) → PlaceDoor 门顶在 Y-1（占 Y-1..Y+1，底格 = 旧单格位置）
747	  if (st.inBounds(Math.floor(cx), Math.floor(cy) - 1)) {
748	    placeDoorClosed(st, Math.floor(cx), Math.floor(cy) - 1, 13);
749	  }
750	  // 开放门厅可站立点（原版 dungeonX/Y 语义 cs L72510-72527：入口结构上 3 宽净空可站处；
751	  // 老头 NPC 出生/游走锚）。取门厅中心列，向下找地板
752	  {
753	    const sx = Math.floor((n51 + n52) / 2);
754	    let sy = n54 - 1;
755	    const limit = Math.min(st.h - 3, n54 + 12);
756	    while (sy < limit && !st.isSolid(sx, sy)) sy++;
757	    if (sy < limit) dc.entStand = [sx, sy];
758	  }
759	  dc.minYY = Math.min(dc.minYY, Math.floor(j - dy1 / 2 - dy1 * 0.6) - 6);
760	  dc.entranceX = Math.floor(cx);
761	}
762	
763	// 条纹窗墙左右界(原版 num60/num61)
764	function n58t(n51: number, dir: number): number {
765	  return dir < 0 ? n51 + 1 : n51 + 2;
766	}
767	function n59t(n52: number, dir: number): number {
768	  return dir < 0 ? n52 + 1 : n52 - 2;
769	}
770	
771	/** 尖刺(L18188):两轮(水平带/竖直带) */
772	function placeSpikes(st: TileStore, rng: RNG, gs: GenState, dc: DungeonCtx, count: number): void {
773	  for (let round = 0; round < 2; round++) {
774	    for (let n = 0; n < count; n++) {
775	      const x = rng.int(dc.minX, Math.max(dc.minX + 1, dc.maxX));
776	      const y = rng.int(Math.max(gs.worldSurface, dc.minYY), Math.max(dc.minYY + 1, dc.maxY));
777	      if (!st.inBounds(x, y) || st.flags[st.idx(x, y)] || st.wall[st.idx(x, y)] !== dc.wall) continue;
778	      // 走到实心
779	      let cx = x, cy = y, found = false;

```


---

## 🤖 Assistant · 2026-08-12T16:55:41.477Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is dungeonEnt (entrance tower + open hall). Key facts:
- The tower interior hall is cleared at lines 599-605 (0.5 frame flags=0, wall=dc.wall).
- The open outer hall (Old Man area) is cleared lines 687-695 (flags=0, wall=0).
- 100-column brick slope (lines 697-721) built from the hall outward and downward: this REPLACES tiles with dungeon brick unless wall is 3/83 or dungeon wall. Note: this slope fills below/around, extending 100 columns from the hall edge — this is what vanilla does to prevent the entrance from being buried. Importantly, this slope does NOT clear the tiles ABOVE the hall; it builds a descending brick slope below n54+step.

Critically: the brick slope loop `for (let y = n54 + step; y < n54 + slope; y++)` — starts at n54+step (below the hall floor) and goes down 100 rows, converting terrain to brick. That protects the approach from the dungeon side. But the surface above/around the hall remains whatever it was (sand from dunes/desert/ocean).

Also note the hall top: the entrance hall interior is open-air? The tower has a roof (top teeth, crenellations). The outer hall (doorway area) is open.

Now: since the entrance hall's floor is at ~n54 and the surface terrain around might be a sand dune much higher, the hall is like an open box dug into terrain. Wait — is it? dungeonEnt at entPos (nx, ny) where ny is the first solid from y=10 downward at column nx, i.e., the actual terrain surface at nx. Then tower center is around that. So the hall is built AT the surface, not buried. The hall floor at n54 = cy + dy2*0.5, around surface level. The tower rises above the surface. So normally the open hall has open sky above it.

Hmm — so how would sand cover it? If the terrain at nx has a sand dune to one side higher than the hall, the 100-column brick slope handles below-hall terrain but not adjacent dune sand that could overhang... Actually the entrance structure spans: tower + outer hall + door; total width maybe dx1*1.2 + dx2*1.2 ≈ (25-29)*1.2 + (35-49)*1.2 ≈ 77-94 columns. Within that span, dungeonEnt fills bricks across. Outside that span, terrain unchanged.

So sand covering would have to come from: (1) later sand-moving passes, or (2) sand falling in from adjacent slopes (via GravitatingSand cavity fill, FinalCleanup column growth), or (3) the Beaches pass sand fill in the basin if the entrance ends up within the basin's x-range.

Wait, reconsider (3) more carefully. Left side (dungeonSide -1): waterX cap = beachLeftEnd - minSand. minSand = sc(50) = 50 for w=4200. beachLeftEnd (side -1) = 320..360 → cap 270..310. waterX = rng.int(220, 259) (inclusive?) — "rng.int(220, 259)" per code `rng.int(oceanWaterMin, oceanWaterMax - 1)` = rng.int(220,259). If waterX > cap, clamp to max(2, cap). So waterX ≤ 259 normally ≤ cap? cap=270..310 → no clamp. So carve columns 0..258.

Dungeon min x after drift ≈ 357 (nx=381, minus 24). So no overlap horizontally. Hmm, BUT what about w smaller than 4200? The world sizes: Terraria small 4200, medium 6400, large 8400. minSand scales with van = w/4200: for w=6400, minSand=76, oceanWaterMin=335... beachLeftEnd stays 320-380 (not scaled!). So for medium/large worlds, minSand = 76, oceanWaterMin=335 → waterX = rng.int(335, 395); cap = beachLeftEnd-76 = 244..304 → clamp → waterX = 244..304! So for medium worlds the basin extends INLAND to x≈300. And the dungeon min x = 381-24 = 357 > 304. Still no overlap. For large w=8400: minSand=100, oceanWaterMin=440, cap = 220..280; waterX = 220..280; carve to x≈279. Dungeon min 357. Still fine — beachDistance=380 constant protects the dungeon entrance from the basin carve as long as dungeon x > ~305.

Hmm OK so Beaches carving cannot reach. Unless... hmm, wait. Let me double check the drift guard direction: `if (nx <= gs.beachDistance || nx >= w - gs.beachDistance) continue;` with beachDistance=380. So nx ∈ [381, w-381]. And cap for carve ~ ≤310 (medium) — so carve max x ≈ 310 < 381-24=357. OK. And on the right side similarly.

So the Beaches pass is likely NOT the direct cause. But it's worth noting the entrance hall is ≥ ~50 columns from the basin edge.

Now what about the OCEAN SAND pass? It runs BEFORE dungeon (vanillaCaves slot, WorldGen.ts:541). It places sand from surface down `thick` (up to edge+4 where edge = min(depth, x-x1, x2-x)) for x in [0, beachLeftEnd). depth 50-200! So sand columns 50-200+ deep along the whole beach strip. The dungeon drift can put the entrance at x as low as ~357 which is < beachLeftEnd (up to 360-380) — meaning the entrance can be carved INTO the ocean-sand strip! Then the corridor's surroundings are all sand. That's the "sand next to the corridor" source. But ocean sand runs before dungeon, so it doesn't cover the carved corridor afterwards.

BUT WAIT: the key thing — the corridor is carved through sand, and then GravitatingSandPass (post-dungeon) fills any air cavity that has a falling tile above it. Consider a corridor column: dungeon bricks form the roof and floor inside the tower. But outside the tower, the open-air approach path (where the Old Man walks, the 100-column brick slope) — the slope is built downward from n54, but ABOVE the slope line (y < n54+step) terrain is untouched. If terrain there is sand at the surface and the slope carved below it... hmm, actually the slope sets brick from n54+step downward; the region above the slope (between hall floor level and original surface) retains sand? No wait — n54 is below the hall floor... Let me think again: the hall floor is at n54 (bottom of open hall). The slope starts at n54+step and goes DOWN (y increases). So above n54 (the hall interior and above) is air (cleared by the hall clearing + the original surface was at ny ≈ hall level). So there's nothing above. Hmm, unless the local terrain is HIGHER than the hall (e.g., a dune). Then the tower is dug into the dune: the tower's outer walls replace terrain with brick up to t1 (tower top). Outside the tower walls, dune sand remains, possibly overhanging the open hall approach at the door side.

The door side: outer hall at cx+dx2*0.55*dir... the 100-col brick slope goes in direction `dir` from n52/n51 outward. So the approach on the door side is protected below by the brick slope, and the hall is open above.

Where could sand overhang the open-air hall? At the boundary between the dungeon structure and adjacent terrain: e.g., a sand dune adjacent to the hall's open side, at height above the hall floor, with the hall carved into it — the hall clearing (lines 689-695) only clears the 0.5 frame box of the outer hall, NOT the terrain above/outside. So sand can remain directly above the hall roofline... but the hall is open to the sky at its location since entPos is at the local surface.

Honestly, precise geometric reasoning is limited without running. The main reportable candidates:

A. GravitatingSandPass (post-dungeon) cavity fill — fills the whole open-air entrance hall with sand if any falling-family tile exists above the cavity in the same column. Cite GravitatingSandPass.ts:41-57, especially line 50-51, and WorldGen.ts:75 (slot order after biomes/dungeon). Note NO dungeon-brick/wall gating.

B. FinalCleanupPass ③ sand column growth (FinalCleanupPass.ts:129-148) — grows a sand column downward up to 10 tiles into open air below, sets a hardened-sand cap. Post-dungeon, no dungeon gating. Also ⑧ only normalizes liquids in dungeon walls.

C. The drift can move the entrance into the ocean-sand strip / near-beach sand (DungeonPass.ts:122-147; guard only nx>380 while beachLeftEnd can be 320-380 and OceanSand sand runs 50-200 deep across [0, beachLeftEnd)). Minimum possible dungeonLocation ≈ 357 < beachLeftEnd max 380 → entrance carved inside beach sand zone. Combined with A/B this yields sand cover. Also note the guard uses beachDistance (380 constant) not beachLeftEnd — mismatch: beachLeftEnd is random 320-380, so for beachLeftEnd near 380 the entrance can be INSIDE the beach strip even though nx > 380? Hmm: dungeonLocation = nx+25-rng.int(0,49) ∈ [nx-24, nx+25]. nx ≥ 381. So dungeonLocation ≥ 357. beachLeftEnd up to 380 (side -1: 320-360; side 1: 340-380). So for side -1, beachLeftEnd max 360 > 357 → possible overlap of entrance within beach strip. Yes.

Also note inversion suspicion at WorldGen.ts:434: the +40 widening applies when dungeonSide===1 (dungeon right → left beach is the FAR side), while vanilla widens the DUNGEON-side beach. Need to check vanilla: Reset L4880-ish: beachSizeLeft = Next(300,340) + (dungeonSide == left ? 40 : 20)? Hmm, in vanilla: `num = (int)(WorldGen.dungeonX >= (double)(Main.maxTilesX / 2) ? 20 : 40)`? I can't verify vanilla source here. I'll flag it as worth double-checking but not assert. Actually wait — comment at line 436 says "地牢侧海滩内 15% 区间（dungeonBeachPadding=50）". Hmm the vanilla: `if (WorldGen.dungeonSide ...)`. I'll flag it neutrally: for dungeonSide===-1 (left), beachLeftEnd = 320..360 which is the dungeon-side beach; vanilla widens dungeon-side beach by 40. Our code adds 40 only when dungeonSide===1 (i.e., to the non-dungeon-side left beach) — possibly inverted. But hold on, if inverted, the dungeon-side beach would be NARROWER (320-360 instead of 340-380)... The consequence for this bug: narrower dungeon-side beach = entrance closer to basin. I'll mention as a deviation to verify.

D. Beaches pass (post-dungeon, WorldGen.ts:602) — writes T.SAND in basin (BeachPass.ts:148-150, 183-185) with NO tileDungeon/wallDungeon checks and clears walls (151/186). Horizontal reach: columns ≤ waterX-1 where waterX ≤ beachLeftEnd-minSand (124, 158-159). Cannot reach entrance (nx ≥ 381) — so not a direct cause but note it strips walls and could matter if constants change. Actually — wait, I should double check: could the basin's sand fill (y > waterY down to yEnd, which is waterY+depth+pad up to deep) reach horizontally adjacent columns beyond waterX? No.

Hmm, but actually there's another subtlety: the Beaches pass clears `st.flags[i] = 0` for y < waterY + depth*0.75-3 across the basin — if any dungeon structure extended into the basin it would be deleted. Entrance is ≥357; basin ≤ 310 max (medium worlds) — safe.

E. DunesPass runs BEFORE dungeon (WorldGen.ts:62 slot 1), but dunes are pure sand hills 60-99 high and up to ±280 wide; DunesPass has NO dungeon-avoidance (rejection only jungle/center/snow, DunesPass.ts:63-74). So a dune can sit on the future entrance site; the entrance then gets carved into a big sand hill — the corridor is surrounded by and possibly under sand overhangs, feeding candidates A and B. Also dune origin ox ∈ [500, w-501] — entrance can be at 357..410 (left) → no dune there since ox ≥ 500, but dunes extend ±(w1/2+30+...) ≈ ±155 from origin → min dune extent ≈ 500-155 = 345 < 410. So YES overlap possible on the left side.

F. DesertPass (WorldGen.ts:581, BEFORE dungeon): surface sand columns (DesertPass.ts:87-114 PlaceSandColumn fills SAND from surfY to sandBottom; lines 395-514 sandstone/hardsand shells). No dungeon check needed (runs before dungeon) but it determines whether the entrance area is sand. Desert location selection — where? Let me quickly check DesertPass location to see if desert can be near the dungeon/beach. Worth a quick grep.

G. Pyramid pass (post-dungeon, WorldGen.ts:619): pyramid spots from Dunes (origin±200) — pyramid avoidance uses gs.dungeonLocation ± 0.15w band (StructuresPass.ts:549-553) — but NOTE: this uses gs.dungeonLocation which IS updated by drift (line 598 comment says world.dungeonX updated after pass; gs.dungeonLocation was reassigned at line 145). So avoidance uses the drifted location. Good. But pyramid also requires sand column and digs staircase converting to SAND (line 632). Distance ≥ 0.15w from dungeon — safe.

H. Oasis (post-dungeon) — gated by sand-only box (OasisPass.ts:60-78) → cannot overlap dungeon bricks. Also x range ≥ beachDistance+300.

I. BeachDecor ShellPiles (post-dungeon, slot 海滩装饰): places SAND + hardened sand near waterline anchors (shellStartX ± ~124) — near ocean edge only; entrance ≥357 vs shell anchors near waterline (~250) ± 124 → up to ~374?! Hmm: shellStartXLeft is the first column reaching waterline in the basin (x ≤ waterX-1 ≤ ~300ish... actually the first column from waterX-1 going left that hits the water-line branch). Then offsets subtract up to 0..4+9+14 = 27 and spawns at -10..-124 further. So spawns around x ≈ waterX-1-27-... ≥ ~100. For the right side: shellStartXRight + offsets... up to +124. Right-side waterX ≈ beachRightStart+50, so spawns extend INLAND up to +124 from there: beachRightStart+174. Dungeon side 1 entrance min = 0.8W-300-... wait dLoc min = trunc(0.8W) - 300 + ... = 3360-300=3060+25-49 ≈ 3036 (for W=4200); beachRightStart+174 ≈ 3860-174... no: beachRightStart = W-320..380-20 = 3800..3860 for W=4200; +50+124 = 3974..4034. Entrance max = dLoc max = beachRightStart-50+299-24 ≈ 4074ish. Hmm! Let me compute worst case right side: dungeonLocation max = nx+25 where nx ≤ min(dLoc_init+299, w-381). dLoc_init max = beachRightStart-50 ≈ 3750..3810 (side 1, W=4200: beachRightStart = 4200-320..380-20 → 3800..3860; minus 50 → 3750..3810). nx max = min(4049..4109, 3819) = 3819. dungeonLocation max = 3844. Shell spawn max x = shellStartXRight + 124 where shellStartXRight ≈ waterX ≈ beachRightStart+50 = 3850..3910 → +124 = 3974..4034 > 3844. Overlap possible!! But shellPile requires the target column to have SAND surface with no wall, and water adjacent (line 222-229: must find SAND surface within worldSurface, wall==0). At x=3900+, that's inside the beach basin sand. Dungeon entrance at up to 3844 with tower half-width ~45 → up to ~3890. Marginal overlap possible (within ~90-150 columns). But shell piles place shell/sand/hardened-sand ON TOP of sand surface where water is adjacent — the dungeon entrance hall floor is brick, not sand → spawn rejected unless column has sand. Possible only at the rim. Weak candidate; mention briefly.

Also check: what about "runCactusPalmTreesAndCoralPass" (slot 仙人掌珊瑚, post-dungeon) — palm trees on sand; uses SAND_GATE. Doesn't add sand cover (maybe converts). Line 988/1004: `if (SAND_CONV.has(anchorType))` converts grass→sand for palm anchor? Let me peek at StructuresPass 940-1010 quickly to see whether palm planting writes SAND onto existing tiles (that could add sand onto... no, gated to sand anchors).

Let me check DesertPass placement location quickly and StructuresPass 940-1010, plus confirm SurfaceDecorPasses TILE_DUNGEON gating lines context (they gate grass decor — good). Also check HalfBrickPass sand smoothing (post-dungeon) — slopes sand, could turn corridor-adjacent sand into slopes, not cover.

One more: TileCleanupPass line 172 CONV_SANDSTONE/HARDENED — check what it does: probably converts sandstone→? Let me read TileCleanupPass 140-190 to rule it in/out.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:55:42.184Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 130,200p ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TileCleanupPass.ts; echo ===; sed -n 940,1015p ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StructuresPass.ts",
 "description": "Read TileCleanup sand conversion and palm sand writes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:55:42.255Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
          st.half[i] = 1;
        }
      }

      // ④ 液体中的 SlowlyDiesInWater 方块清除(cs:21354-21357)
      if (st.flags[i] && st.liquid[i] > 0 && SLOWLY_DIES_IN_WATER.has(st.type[i])) {
        killTile(st, k, l);
      }

      // ⑤ 滴水石笋(cs:21358-21435):空格+无液+上方实心才进
      if (!st.flags[i] && st.liquid[i] === 0 && rng.int(0, 2) !== 0 && solidTile(st, k, l - 1)) {
        // 上扫(cs:21360-21411):l-2 起向上 num(15-20) 格,液体>=128
        let num = rng.int(15, 20); // Next(15,21)
        for (let n2 = l - 2; n2 >= l - num; n2--) {
          const up = st.idx(k, n2);
          if (st.liquid[up] >= 128 && st.liquidType[up] !== LIQUID_TYPE.SHIMMER) {
            const maxValue = l - n2; // 距离,最小 2
            if (rng.int(0, maxValue - 1) <= 1) { // Next(maxValue)
              let drip = dripFor(st.liquidType[up]);
              if (st.wall[i] === BEE_WALL) drip = DRIP_HONEY; // cs:21404
              st.setTileSilent(k, l, drip, 0, 0);
              break;
            }
          }
        }
        // 下扫(cs:21413-21429):l+1 起向下 num(3-10) 格,液体>=200
        if (!st.flags[i]) {
          num = rng.int(3, 10); // Next(3,11)
          for (let m = l + 1; m <= l + num; m++) {
            const dn = st.idx(k, m);
            if (st.liquid[dn] >= 200 && st.liquidType[dn] !== LIQUID_TYPE.SHIMMER) {
              const dist = m - l;
              if (rng.int(0, dist * 3 - 1) <= 1) { // Next(dist*3)
                st.setTileSilent(k, l, dripFor(st.liquidType[dn]), 0, 0);
                break;
              }
            }
          }
        }
        // 小沙堆(cs:21431-21441):上方是沙岩/硬沙 → 1/4 概率放 461
        if (!st.flags[i] && rng.int(0, 3) === 0) { // Next(4)
          const above = st.idx(k, l - 1);
          if (CONV_SANDSTONE.has(st.type[above]) || CONV_HARDENED_SAND.has(st.type[above])) {
            st.setTileSilent(k, l, SAND_PILE, 0, 0);
          }
        }
      }

      // ⑥ 墙 13/14 液体清零(cs:21437-21439)
      if (st.wall[i] === 13 || st.wall[i] === 14) {
        st.liquid[i] = 0; // 原版只清液量,liquidType 位保留
      }
      // ⑥ 墙 87(cs:21441-21458):extraLiquid 特殊种子分支未实装(SeedFlags 无该旗标),
      //    恒走普通世界分支 = 液体清零
      if (st.wall[i] === 87) {
        st.liquid[i] = 0;
      }

      // ⑦⑧⑨⑩ 帧规范化族(cs:21461-21741)——跳过(我方放置端已保证帧,审计裁决)

      // ⑪ 祭坛 237 正下方 232 木刺 → 226 蜥蜴砖(cs:21743-21746)
      if (st.flags[i] && st.type[i] === LIHZARD_ALTAR && st.type[st.idx(k, l + 1)] === WOODEN_SPIKE) {
        st.type[st.idx(k, l + 1)] = LIHZARD_BRICK;
      }
    }
  }

  // ⑫ tileSolid[379] 还原 true(cs:21750)——TileStore 无全局 tileSolid 表,
  //    覆写经 solidTile/isSaveSlope 内的 BUBBLE 判定实现,pass 结束自动失效
}
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-12T16:55:43.004Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"desertPos\\|origin\\|rng.int\\|nextDouble\\|placeDesert\\|function runDesertPass\\|beach\\|dungeon\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts | head -40",
 "description": "Check desert placement bounds"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:55:43.065Z

**📎 ToolResult**

```
77:  const ox = x - Math.trunc(width / 2);      // origin.X -= num4/2（int 除）
82:  const hiveTop = topY + rng.int(40, 59);    // Next(40,60)
93:    if (i % 3 === 0) coarse = Math.max(-10, Math.min(10, coarse + rng.int(-1, 1)));
94:    fine = Math.max(-10, Math.min(10, fine + rng.int(-1, 1)));
144:  let side = gs.dungeonSide, tries = 0, flips = 0, skipCheck = false;
183:    out: Set<number> | null = null;            // GenAction.OutputData（origin 相对坐标）
215:        const a = rng.int(-1, 0), b = rng.int(0, 1), c = rng.int(-1, 0), d = rng.int(0, 1);
390:    const px = centerX + rng.int(-40, 40);                     // Next(-40,41)
397:    let num2 = rng.int(0, 1) !== 0 ? 1 : -1;                   // Next(2) != 0
399:    const num3 = rng.int(2, 3);                                // Next(2,4)
401:      const num4 = Math.trunc((i + 1) / num3 * hnum) + rng.int(-8, 8);
402:      const num5 = num2 * rng.int(20, 40);
403:      const num6 = rng.int(18, 28);
430:    const num = rng.int(2, 3);                                  // Next(2,4)
432:      const holeRadius = rng.int(15, 17);                       // Next(15,18)
451:        num += rng.int(-1, 1);                                  // Next(-1,2)
467:    const num = rng.int(2, 3);
469:      const holeRadius = rng.int(13, 15);                       // Next(13,16)
486:        num += rng.int(-1, 1);
496:    const holeRadius = rng.int(6, 8);                           // Next(6,9)
545:      for (let c = num1 - num5; c <= num1 + num5; c++) blockMap[c]![r] = rng.int(0, 1) === 0;
562:        if (blockMap[x]![y] && rng.int(0, 1) === 0) {
581:        const val = rng.int(0, 1) === 0 ? -1 : idx;
604:  //  完全独立的第二条流，曾误用 rng.int/rng.next 造成每格 1-2 次幽灵掷骰
648:        if (fr2.nextDouble() < (field - 0.25) / 0.45) {
714:      if (flag && rng.int(0, 19) === 0) {      // Next(20)==0 → 485/751
715:        const style = rng.int(0, 3);           // style = Next(4)
716:        if (rng.int(0, 29) === 0) placeDeco(px, py - 1, T751, 2, 2, 0);        // Next(30)==0 → 751
718:      } else if (flag && rng.int(0, 4) === 0) {          // 484
720:      } else if ((flag !== flag2) && rng.int(0, 4) === 0) {  // 165：flag 地面/!flag 倒挂
723:      } else if (flag && rng.int(0, 4) === 0) {          // 187：style 29+Next(6)（此前漏掷）
724:        placeDeco(px, py - 1, T187, 3, 2, (29 + rng.int(0, 5)) * 54);
740:export function runDesertPass(st: TileStore, rng: RNG, gs: GenState): void {

```


---

## 🤖 Assistant · 2026-08-12T16:55:46.755Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
TileCleanupPass ⑤ small sand pile 461 (SAND_PILE) — placed BELOW sandstone/hardened sand when the cell is air, no liquid, above is sand. This is post-dungeon (瓦片清理 slot). It's a small deco (461 = small sand pile, non-solid?). Probably non-solid decor. Not blocking. But worth a mention as sand-family placement without dungeon gating (it requires air cell + sandstone above — could place inside the entrance hall if hall has sandstone above? Hall has brick above → no).

Now DesertPass placement — let me read runDesertPass at line 740 onward to see x bounds (whether desert avoids the dungeon side).
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:55:46.783Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts",
 "limit": 80,
 "offset": 740
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:55:46.794Z

**📎 ToolResult**

```
740	export function runDesertPass(st: TileStore, rng: RNG, gs: GenState): void {
741	  const desc = runDesertMoundOnly(st, rng, gs);
742	  runDesertEntrancesAndHive(st, rng, gs, desc);
743	  // gs.undergroundDesert 已随 runDesertEntrancesAndHive 落盘（见其尾部）
744	}
745	
746	

```


---

## 🤖 Assistant · 2026-08-12T16:55:47.252Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"beachLeftEnd\\|beachRightStart\\|beachDistance\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/*.ts | grep -v GenState",
 "description": "Find all beach bound consumers"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:55:47.351Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CaveHousePass.ts:645:    if (oceanGate && (ox < gs.beachDistance || ox > w - gs.beachDistance)) return false; // oceanDepths 回避
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts:460:      // 原版 WorldGen.beachDistance 是常量 380(cs:4102)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts:464:      while (y <= oceanLevel && (x < gs.beachDistance || x > w - gs.beachDistance)) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BuriedChestsPass.ts:549:          trySlope: x < gs.beachDistance || x > w - gs.beachDistance,
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:28:    if (i === 0) { x1 = 0; x2 = gs.beachLeftEnd; }
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:29:    if (i === 2) { x1 = gs.beachRightStart; x2 = w; }
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:120:      // 左海盆:从 beachLeftEnd-50 之左往世界缘挖
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:123:      const cap = gs.beachLeftEnd - minSand;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/BeachPass.ts:158:      const cap = gs.beachRightStart + minSand;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:274: *  进沙滩带（beachDistance 内）返回 true。oceanLevel=(worldSurface+rockLayer)/2+40（cs:4393）。 */
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CorruptionPass.ts:277:  return x < gs.beachDistance || x > st.w - gs.beachDistance;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CavesPass.ts:92:  const beachL = gs.beachLeftEnd + 20, beachR = gs.beachRightStart - 20;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/GemPasses.ts:281:    return x < gs.beachDistance || x > st.w - gs.beachDistance;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:117:  return x < gs.beachDistance || x > st.w - gs.beachDistance;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/FinalCleanupPass.ts:239:      if (i > gs.beachDistance && i < w - gs.beachDistance && j < gs.worldSurface
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DungeonPass.ts:123:      if (nx <= gs.beachDistance || nx >= w - gs.beachDistance) continue;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/JunglePass.ts:67:  const i = Math.max(gs.beachLeftEnd + Math.floor(num2 / 2) + num3, Math.min(gs.beachRightStart - Math.floor(num2 / 2) - num3, cx));
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:13://      beachDistance, 200, beachDistance)。数量 CampsiteCount 6-11 × WorldArea。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:16://      起爆器 411 + 红线直连。位置 RandomWorldPoint(rockLayer, beachDistance, 200,
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:17://      beachDistance)。数量 ExplosiveTrapCount 14-29 × WorldArea。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:162:    const ox = rng.int(gs.beachDistance, w - gs.beachDistance - 1); // RandomWorldPoint(top,right,bottom,left)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:178:    const ox = rng.int(gs.beachDistance, w - gs.beachDistance - 1);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MicroBiomesPass.ts:838:    if (y <= oceanLevel && (x < this.gs.beachDistance || x > st.w - this.gs.beachDistance)) return false;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LivingTreePass.ts:808:      const num6 = rng.int(gs.beachDistance, w - gs.beachDistance - 1);  // cs:15610
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts:111: *  y∈[GenVars.rockLayer+20, +(h-rockLayer-40-200))；中部 45-55% 重掷 beachDistance..w-；
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts:127:      while (x > st.w * 0.45 && x < st.w * 0.55) x = rng.int(gs.beachDistance, st.w - gs.beachDistance - 1);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MarbleGranitePass.ts:244:      while (x > st.w * 0.45 && x < st.w * 0.55) x = rng.int(gs.beachDistance, st.w - gs.beachDistance - 1);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MushroomPass.ts:42:  // 与滩带（beachDistance=380）内禁长；其余草走 (j>=worldSurface && dirt==0) 门。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OceanCavesPass.ts:53:    // 离开海滩带(越过 beachDistance-50)后每步 ×0.96(cs:76746;flag2 地牢穿越本仓库恒 false)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OceanCavesPass.ts:54:    if (vx > gs.beachDistance - 50 && vx < w - gs.beachDistance + 50) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/PilesPass.ts:100:    return x < gs.beachDistance || x > w - gs.beachDistance;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:369:      let x = rng.int(gs.beachDistance, w - gs.beachDistance - 1);     // Next(bd, w-bd)
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:370:      while (x >= w * 0.48 && x <= w * 0.52) x = rng.int(gs.beachDistance, w - gs.beachDistance - 1);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:390:      let x = rng.int(gs.beachDistance, w - gs.beachDistance - 1);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:391:      while (x >= w * 0.47 && x <= w * 0.53) x = rng.int(gs.beachDistance, w - gs.beachDistance - 1);
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:412:    const x0 = gs.beachDistance + 20;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/SurfaceDecorPasses.ts:1433:    if (x < gs.beachDistance || x > w - gs.beachDistance) return [-1, -1];
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/StatuesPass.ts:83:      while (y <= oceanTop && (x < gs.beachDistance || x > w - gs.beachDistance) && guard-- > 0) {
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TerrainPass.ts:7:// 海滩区按 Reset 掷的 beachLeftEnd/beachRightStart 平坦化,右海滩入口 Retarget 收平。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TerrainPass.ts:45:  const leftBeach = gs.beachLeftEnd, rightBeach = w - gs.beachRightStart;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts:7://   （x∈[beachDistance+300, w-同]，y∈[100, worldSurface)），PlaceOasis 成功即止。
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/OasisPass.ts:202:    const lo = gs.beachDistance + 300;                       // cs:16340 num2
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrackPass.ts:376:    if (y <= oceanLevel && (x < gs.beachDistance || x > st.w - gs.beachDistance)) return true;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:303:      // oceanDepths 回避（cs:18821）——海滩带是常量 beachDistance=380（cs:4102），
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:304:      // 非 beachLeftEnd/RightStart（那是 Reset 掷的海滩宽，不是回避带）
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/TrapsPass.ts:306:      while (y <= oceanTop && (x < gs.beachDistance || x > st.w - gs.beachDistance)) {

```


---

## 🤖 Assistant · 2026-08-12T16:55:48.866Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me check desert mound placement bounds quickly — runDesertMoundOnly at ~line 140 (side = gs.dungeonSide). Let me read lines 100-180 of DesertPass.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:55:49.160Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/DesertPass.ts",
 "limit": 80,
 "offset": 120
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:55:49.168Z

**📎 ToolResult**

```
120	  return {
121	    combX: ox, combY: topY, combW: width, combH: hiveTop + height - topY,
122	    hiveTop, hiveH: height, desertH,
123	    blockCols, blockRows,
124	    surface: sm.heights, surfaceX: ox - 5,
125	    surface2: sm2.heights, surface2X: ox - 5,
126	  };
127	}
128	
129	const MUD = TILE_BY_KEY['mud']!;
130	const JUNGLE_GRASS = TILE_BY_KEY['v_60_jungle_grass_block']!;
131	const SNOW = TILE_BY_KEY['snow']!;
132	const ICE = TILE_BY_KEY['ice']!;
133	const SAND = T.SAND;
134	const SANDSTONE = TILE_BY_KEY['sandstone']!;
135	const HARDSAND = TILE_BY_KEY['hardened_sand']!;
136	const FOSSIL = TILE_BY_KEY['desert_fossil']!;
137	
138	/** 放置循环 + Description + SandMound（Sub-A；Hive/入口在 runDesertPass 续） */
139	export function runDesertMoundOnly(st: TileStore, rng: RNG, gs: GenState): DesertDesc {
140	  const { w } = st;
141	  const half = Math.floor(w / 2);
142	  // DesertBiome pass 放置循环（cs:12538-12562 1:1）：失败重掷**永不早退**，
143	  // 2 次换向后 skipDesertTileCheck 恒过（此前 tries>w/2 早退=可能整图无沙漠）
144	  let side = gs.dungeonSide, tries = 0, flips = 0, skipCheck = false;
145	  let num4 = Math.trunc(rng.nextIntRange(0, half) / 8) + Math.trunc(half / 8);
146	  let x = half + num4 * -side;
147	  let desc: DesertDesc | null = null;
148	  for (;;) {
149	    desc = desertPlaceMound(st, rng, x, gs.worldSurface);
150	    if (desc) break;
151	    num4 = Math.trunc(rng.nextIntRange(0, half) / 2) + Math.trunc(half / 8)
152	      + rng.nextIntRange(0, Math.trunc(tries / 12));
153	    x = half + num4 * -side;
154	    if (++tries > Math.floor(w / 4)) {
155	      side = (-side) as 1 | -1;
156	      tries = 0;
157	      if (++flips >= 2) skipCheck = true;
158	    }
159	    if (skipCheck) {
160	      // 恒过：RowHasInvalidTiles 直接 false（GenVars.skipDesertTileCheck 语义）
161	      desc = desertPlaceMound(st, rng, x, gs.worldSurface, true);
162	      break;
163	    }
164	  }
165	  return desc!; // skipCheck 后 RowHasInvalidTiles 恒 false → 必非 null
166	}
167	
168	// ---- 入口 + 蜂巢（Sub-C + Sub-B）。DesertBiome.Place 顺序（cs:21-42）：
169	//  mound → UpdateSurfaceMap → 入口（33% 门+Next(4)） → DesertHive.Place → CleanupArea。
170	//  入口必须在 Hive 之前（两侧共享同一条 genRand 流，次序即流位置）。
171	//  afterEntrance：入口完成、Hive 之前的对账钩子（oracle 的 desertentrance 检查点） ----
172	export function runDesertEntrancesAndHive(st: TileStore, rng: RNG, gs: GenState, desc: DesertDesc, afterEntrance?: () => void): void {
173	  const W = st.w, H = st.h;
174	  // UpdateSurfaceMap 后的表面图（DesertBiome.cs:22）；Surface[absoluteX]
175	  const surf2 = (ax: number) => desc.surface2[ax - desc.surface2X];
176	
177	  // ================= WorldBuilding 微框架（入口 4 形状共用）=================
178	  // 与 caves-oracle.cs 的 WC/GW 逐行对应；哈希无关副作用（SquareWallFrame/SmoothSlope）
179	  // 两侧一致省略。quitOnFail 恒 false → apply 返回 false 不中断遍历。
180	  const shapeKey = (dx: number, dy: number) => dx * 4194304 + dy + 2097152;
181	  abstract class Ga {
182	    next: Ga | null = null;
183	    out: Set<number> | null = null;            // GenAction.OutputData（origin 相对坐标）
184	    abstract apply(ox: number, oy: number, x: number, y: number): boolean;
185	    protected ua(ox: number, oy: number, x: number, y: number): boolean {
186	      if (this.out) this.out.add(shapeKey(x - ox, y - oy));
187	      return this.next ? this.next.apply(ox, oy, x, y) : true;
188	    }
189	  }
190	  function chain(...xs: Ga[]): Ga {           // Actions.Chain：串 NextAction 返回链首
191	    for (let i = 0; i < xs.length - 1; i++) xs[i]!.next = xs[i + 1]!;
192	    return xs[0]!;
193	  }
194	  function outA(a: Ga, o: Set<number>): Ga { a.out = o; return a; }   // GenAction.Output
195	
196	  const inW = (x: number, y: number) => x >= 0 && x < W && y >= 0 && y < H;
197	  const solidAt = (x: number, y: number) => inW(x, y) && st.flags[st.idx(x, y)] !== 0
198	    && !!TILE_DEFS[st.type[st.idx(x, y)]]?.solid;
199	  const clearEverything = (x: number, y: number) => {

```


---

## 🤖 Assistant · 2026-08-12T16:56:01.661Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Desert: side = dungeonSide, x = half + num4 * -side → desert placed on the OPPOSITE side of the dungeon (since x = half - num4*side... wait if dungeonSide=1 (dungeon right), x = half - num4 → desert left. Yes, desert is on the opposite side from the dungeon. So DesertPass surface sand shouldn't be at the dungeon entrance... except after flips (tries > w/4 → side flips, twice → skipCheck) — desert can end up anywhere including the dungeon side. Rare. So desert is mostly not the source; the main sources of sand near the dungeon entrance are OceanSand strip (beach), Dunes, and Beaches basin.

Now, one more thing to verify: the passes list order as required by question 1 — I have it (WorldGen.ts:58-203). And within vanillaBiomes, the inner order (WorldGen.ts:561-642), with Dungeon at 593 followed by Beaches at 602.

Also question 6: vanilla "Clean Up" equivalents — CleanupPass.ts (DirtWallCleanup, wall clearing + clump removal), TileCleanupPass.ts, FinalCleanupPass.ts, BrokenTrapCleanupPass.ts. Vanilla's FinalCleanup has no "remove sand from dungeon entrance" step — but vanilla has something relevant? In vanilla there IS no explicit "clean sand off dungeon entrance" pass; protection comes from ordering (Beaches before... no, Beaches is 34 AFTER Dungeon 32 in 1.4.4 vanilla registration). Hmm interesting — in vanilla, Beaches(34) runs after Dungeon(32), and beach basin is at the world edges, far from the dungeon entrance, so fine.

Wait — one more thing to check: in vanilla 1.4.4, is there a "DigDungeonEntrance" or post-pass that removes sand? There's `WorldGen.dungeonLocation`... Not needed. Our report: we have CleanupPass/TileCleanupPass/FinalCleanupPass/BrokenTrapCleanupPass; none remove sand from the dungeon entrance; FinalCleanup only normalizes dungeon-wall liquids (FinalCleanupPass.ts:210-220).

One more potential mechanism I should check: HalfBrickPass smooth world (post-dungeon) — "Smooth World" converts protruding surface tiles to half-bricks/slopes; does it also DELETE tiles? In vanilla, SmoothWorld knocks off single-tile protrusions. If the dungeon entrance's crenellations... not sand though. Skip.

And what about SurfaceDecorPasses line 186/313: those gates include TILE_DUNGEON for placing dirt/grass decor — meaning decor passes do check dungeon. Cite as contrast: sand-family placements (BeachPass, GravitatingSand, FinalCleanup ③) do NOT.

Also check SurfaceDecorPasses for any T.SAND writes — grep showed none except CONV_SAND gating. Fine.

Also: does anything else write sand post-dungeon? `WaterIcePasses` RemoveSurfaceWaterAboveSand (only clears water). `LakesPass` — sand? const SAND = TILE_BY_KEY['sand'] at line 22 — check usage; Lakes pass is pre-dungeon (inside vanillaBiomes at 591). Actually runLakesPass is called at line 591, before dungeon 593. Fine.

MountCavesPass: line 144 const SAND — runMountCavesPass is called at WorldGen.ts:544 (vanillaCaves slot, pre-dungeon) and runMountainCavesPass at 601 (post-dungeon!). Wait: line 601 runMountainCavesPass(store, rng, gs) — that's MountCavesPass's second export (MountainCaves = pass 33 MountainCaveOpenings). Does it place sand? MountCavesPass line 144 const SAND = TILE_BY_KEY['sand']!. Let me check its usage — MountainCaveOpenings digs openings in hills, maybe places sand at beach-adjacent hills? Let me check.

Let me grep MountCavesPass for SAND usage context.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:56:02.160Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"SAND\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts; echo ---; sed -n 120,175p ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MountCavesPass.ts",
 "description": "Check MountCavesPass sand usage"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:56:02.220Z

**📎 ToolResult**

```
15:const SAND_AVOID = idsByVanillaSheet(53, 151, 274);
80:          if (SAND_AVOID.has(st.type[st.idx(xx, yy)])) { nearSand = true; break; }
144:  const SAND = TILE_BY_KEY['sand']!;
168:          if (active && (NOT_CLEARABLE.has(st.type[kk]) || st.type[kk] === SAND)) continue;
---
        }
      }
    }
    px += vx; py += vy;
    vx += rng.int(-10, 10) * 0.05;
    vy += rng.int(-10, 10) * 0.05;
    if (vx > dir + 0.5) vx = dir + 0.5;
    if (vx < dir - 0.5) vx = dir - 0.5;
    if (vy > 0) vy = 0;
    if (vy < -0.5) vy = -0.5;
  }
}

/** Cavinator（L48733）：向下蜿蜒洞穴，递归 steps 次直至岩层（不挖沙 53） */
/** 原版 tileDungeon（Main.cs:7941-7946）与 wallDungeon（Main.cs:10507-10515） */
const TILE_DUNGEON = idsByVanillaSheet(41, 43, 44, 677, 678, 679);
const WALL_DUNGEON = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);

function cavinator(st: TileStore, rng: RNG, gs: GenState, i: number, j: number, steps: number): void {
  let num1 = rng.int(7, 14);              // Next(7,15)
  const dir = rng.int(0, 1) === 0 ? -1 : 1;
  let px = i, py = j;
  let num4 = rng.int(20, 39);            // Next(20,40)（num4：剩余步数，地牢命中清零）
  let vx = dir, vy = rng.int(10, 19) * 0.01; // Next(10,20)
  const SAND = TILE_BY_KEY['sand']!;
  while (num4 > 0) {
    num4--;
    let x0 = ctrunc(px - num1 * 0.5), x1 = ctrunc(px + num1 * 0.5);
    let y0 = ctrunc(py - num1 * 0.5), y1 = ctrunc(py + num1 * 0.5);
    if (x0 < 0) x0 = 0;
    if (x1 > st.w) x1 = st.w;
    if (y0 < 0) y0 = 0;
    if (y1 > st.h) y1 = st.h;
    const r = num1 * rng.int(80, 119) * 0.01;
    // ★地牢命中即整轮终止（cs:80753-80762）：tileDungeon/墙 dungeon → num4=0
    //  （此前缺失：跑满全程多耗每步 3 骰 → 条件性流漂移）
    outer:
    for (let x = x0; x < x1; x++) {
      for (let y = y0; y < y1; y++) {
        const dx = Math.abs(x - px), dy = Math.abs(y - py);
        if (Math.sqrt(dx * dx + dy * dy) < r * 0.4) {
          const kk = st.idx(x, y);
          const active = st.flags[kk] !== 0;
          if ((active && TILE_DUNGEON.has(st.type[kk])) || WALL_DUNGEON.has(st.wall[kk])) {
            num4 = 0;
            break outer;
          }
          // 不可清块/沙：跳过该格（原版 continue，不终止）
          if (active && (NOT_CLEARABLE.has(st.type[kk]) || st.type[kk] === SAND)) continue;
          if (active) st.flags[kk] = 0; // 原版 active(false) 保留幽灵 type（cavinator）
        }
        if (num4 <= 0) break;
      }
      if (num4 <= 0) break;
    }
    if (num4 <= 0) break; // 终止后不再消耗速度/半径骰（原版 while 条件）

```


---

## 🤖 Assistant · 2026-08-12T16:56:02.773Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"T.SAND\\|SAND\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LakesPass.ts ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MissingCavesPass.ts ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/CavesPass.ts",
 "description": "Check sand in lakes/caves passes"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:56:02.815Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LakesPass.ts:22:const SAND = TILE_BY_KEY['sand']!;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/LakesPass.ts:156:      if (!bad && st.type[st.idx(x, y)] === SAND) bad = true;
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MissingCavesPass.ts:25:    // ★type 是本仓库内部 id（原版 53 沙 = T.SAND；曾直传 53 = 内部表恰好沙漠化石!）
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MissingCavesPass.ts:26:    tileRunner(st, rng, gs, num2, num3, { strength: num4, steps, type: T.SAND });
~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/MissingCavesPass.ts:50:        if (st.type[st.idx(num2, j)] === T.SAND) flag = true; // 锚在沙上 → 整组重掷（原版 id 53=沙;内部 53 恰是沙漠化石,曾直传 53 致重掷永假）

```


---

## 🤖 Assistant · 2026-08-12T16:56:05.368Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. MountainCaves (post-dungeon, pass 33) only digs, doesn't add sand, and it skips sand + stops on dungeon (MountCavesPass.ts:134-170). Good to cite as "does check dungeon".

I now have everything needed. Let me also confirm the exact pass list order numbers/lines for the report, plus double-check `rng.nextIntRange(300, 340)` semantics (inclusive both ends?) — check RNG implementation briefly to state ranges correctly.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:56:05.781Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"nextIntRange\\|nextInt(\" ~/Project/GLM/SandboxWorld/game/src/core/rng.ts | head; echo ---; sed -n 1,60p ~/Project/GLM/SandboxWorld/game/src/core/rng.ts",
 "description": "Check RNG range semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:56:05.858Z

**📎 ToolResult**

```
89:  nextIntRange(minValue: number, maxValue: number): number {
98:  nextInt(maxValue: number): number {
136:    return this.ur.nextIntRange(min, max + 1);
148:    return arr[this.ur.nextInt(arr.length)];
152:  nextInt(maxValue: number): number {
153:    return this.ur.nextInt(maxValue);
156:  nextIntRange(minValue: number, maxValue: number): number {
157:    return this.ur.nextIntRange(minValue, maxValue);
---
// 确定性随机数：Terraria 1.4.5.6 位级对齐。
//
// ── UnifiedRandom（Terraria.Utilities/UnifiedRandom.cs 1:1）─────────────────
// .NET System.Random 的 Knuth 减法生成器（MSEED=161803398），纯 int32 运算。
// 位级移植要点（JS/C# 数值差异全部钉死，改动前先读）：
//  1. C# int 溢出 unchecked 回绕 ↔ JS：本实现所有中间值都落在 int32 范围内
//     （diff 最小 -(2^31-1)，`+((n>>31)&0x7FFFFFFF)` 归位后 ∈[0,2^31-1]），
//     无需模拟回绕；存储用 Int32Array 与 C# int[] 同构。
//  2. `(int)double` 是向零截断 ↔ JS Math.trunc（Sample()≥0 时与 floor 等价，
//     但必须写 trunc 以防有人把 internalSample 改出负值）。
//  3. `Sample()` 常数 4.656612875245797E-10 = 1/(2^31-1)，十进制字面量两语言
//     解析为同一 double，乘法 IEEE754 位级一致。
//  4. `Next(min,max)` 的 range 用 long（≤2^32）↔ JS number 精确整数，安全。
//     大 range 分支的 `(int)(long+min)` unchecked 回绕 ↔ JS `|0`（ToInt32 mod 2^32）。
//  5. `GetSampleForLargeRange` 的 `% 2 == 0`：C# 余数带符号但只判零，JS `%` 同判。
//  金标：tests/golden/unified-random.json 由真·Terraria.exe 反射导出
//  （tools/golden/rand-golden.cs），tests/unified-random.test.ts 位级断言。
//
// ── 种子解析（WorldFileData.TranslateSeed, cs:399-410 1:1）────────────────
// 数字字符串 → Math.Abs(int)（int.MinValue→int.MaxValue）；非数字 →
// ReLogic.Utilities.Crc32.Calculate（IEEE 表，按 UTF-16 code unit 逐字符，
// 注意 `(crc ^ c) & 0xFF` 只取 char 低字节）。Crc32 结果可为负，直接作种子。
export class UnifiedRandom {
  private seedArray: Int32Array;
  private inext = 0;

  constructor(seed: number) {
    this.seedArray = new Int32Array(56);
    this.setSeed(seed);
  }

  /** C# SetSeed（UnifiedRandom.cs:25-61）1:1 */
  setSeed(seed: number): void {
    this.seedArray.fill(0);
    // C#: (Seed == int.MinValue) ? int.MaxValue : Math.Abs(Seed)
    const num = seed === -2147483648 ? 2147483647 : Math.abs(seed);
    let num2 = 161803398 - num;
    this.seedArray[55] = num2;
    let num3 = 1;
    for (let j = 1; j < 55; j++) {
      const num4 = (21 * j) % 55;
      this.seedArray[num4] = num3;
      num3 = (num2 - num3) | 0; // C# unchecked int：可能回绕，|0 = ToInt32 同语义
      if (num3 < 0) num3 += 2147483647; // C# += int.MaxValue（不是 2^32！）
      num2 = this.seedArray[num4];
    }
    for (let k = 1; k < 5; k++) {
      for (let l = 1; l < 56; l++) {
        this.seedArray[l] -= this.seedArray[1 + ((l + 30) % 55)];
        if (this.seedArray[l] < 0) this.seedArray[l] += 2147483647;
      }
    }
    this.inext = 0;
  }

  /** C# Sample（:63-65）*/
  private sample(): number {
    return this.internalSample() * 4.656612875245797e-10;
  }

```


---

## 🤖 Assistant · 2026-08-12T16:56:07.435Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 85,110p ~/Project/GLM/SandboxWorld/game/src/core/rng.ts; sed -n 125,140p ~/Project/GLM/SandboxWorld/game/src/core/rng.ts",
 "description": "Read nextIntRange/nextInt bounds semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:56:07.498Z

**📎 ToolResult**

```
  }

  /** C# Next(minValue, maxValue)（:115-133）：[min, max)。maxValue 负值时 C# 抛异常，
   *  本移植不抛（生成期契约保证入参合法）。*/
  nextIntRange(minValue: number, maxValue: number): number {
    const num = maxValue - minValue; // C# long 减法，≤2^32，JS 精确
    if (num <= 2147483647) {
      return (Math.trunc(this.sample() * num) + minValue) | 0;
    }
    return (Math.trunc(this.getSampleForLargeRange() * num) + minValue) | 0;
  }

  /** C# Next(maxValue)（:121-127）：[0, max) */
  nextInt(maxValue: number): number {
    return Math.trunc(this.sample() * maxValue);
  }

  /** C# NextDouble()（:113-115）*/
  nextDouble(): number {
    return this.sample();
  }

  /** C# Peek()（:88-99，非消耗）：下一 InternalSample 原始差值——对账/断点用 */
  peek(): number {
    let num = this.inext + 1;
    if (num > 55) num = 1;
  private ur: UnifiedRandom;
  constructor(seed: number) {
    this.ur = new UnifiedRandom(seed);
  }

  next(): number {
    return this.ur.nextDouble();
  }

  /** 闭区间 [min, max]，≡ 原版 Next(min, max+1) */
  int(min: number, max: number): number {
    return this.ur.nextIntRange(min, max + 1);
  }

  range(min: number, max: number): number {
    return min + this.ur.nextDouble() * (max - min);

```


---

## 🤖 Assistant · 2026-08-12T16:56:25.438Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
nextIntRange(300, 340) = [300, 340) = 300..339. So beachLeftEnd:
- side 1: 300..339 + 40 = 340..379
- side -1: 300..339 + 20 = 320..359

dungeonLocation initial: side -1: rng.nextIntRange(beachLeftEnd+50, trunc(0.2W)) = [370..409, ...].
Drift: nx = dungeonLocation - 300 + rng.int(0,599) (int() is inclusive → 0..599) → nx ∈ [dLoc-300, dLoc+299]. Guard nx > 380 → nx ≥ 381, nx ≤ w-381.
Final dungeonLocation = nx + 25 - rng.int(0,49) → ∈ [nx-24, nx+25]. Min = 381-24 = 357.

beachLeftEnd (side -1) max = 359 → entrance can be at x=357..359, i.e., INSIDE the beach strip (x < beachLeftEnd=359), where OceanSand placed 50-200-deep sand columns and the beach basin waterX cap = beachLeftEnd-50 = 309 max (minSand=50 at w=4200). Basin carve x ≤ waterX-1. waterX = rng.int(220,259) typically ≤ 259 < 309 → carve x ≤ 258. So basin sand still can't reach 357.

Hmm wait — one more scenario for the left side. Actually let me reconsider: at medium/large worlds minSand scales (w/4200*50). For w=6400: minSand=76, oceanWaterMin=335, so waterX=rng.int(335,395)... cap=beachLeftEnd-76=244..283 → waterX clamped to 244..283; carve x ≤ 282. Still < 357.

Right side: cap = beachRightStart + minSand; carving x ≥ waterX where waterX = min(w-2, cap) when clamped... for w=4200: waterX = W - rng.int(220,259) = 3941..3980; cap = beachRightStart+50. beachRightStart (side 1) = W - (300..339) - 20 = 3841..3880; cap = 3891..3930. Is waterX (3941..3980) < cap (3891..3930)? Yes → clamp waterX = cap = 3891..3930. Carve x ≥ 3891. Dungeon nx ≤ w-381 = 3819 → dLoc ≤ 3844. Entrance structure extends ±~50 → up to ~3894 — borderline touching carve start 3891 in the extreme tail case! Interesting: with dungeonLocation=3844 and tower/hall half-width ~45-50, the outer edge could reach 3894 > 3891 = carve start. Then the Beaches pass would clear/deactivate dungeon tiles AND write sand (BeachPass.ts:141/149) over the outer end of the entrance hall. That's an extreme tail case (requires beachLeftEnd-ish values at both extremes). Worth listing as a lower-probability candidate.

Hmm wait, careful: for side 1, dungeonLocation initial ∈ [trunc(0.8W)=3360, beachRightStart-50 = 3791..3830]. Drift nx ∈ [dLoc-300, dLoc+299] ∩ (381, 3819) → nx up to min(3830+299=4129, 3819) = 3819. dLoc = nx+25-int(0,49) → up to 3844. Right. And hall extends toward the ocean side by dx2*0.55+... the outer hall is on the door side. dir sign? Unknown, but ±~50 plausible. So overlap of up to a few columns at the very extreme. Low probability but real.

Actually also more important: is the entrance really limited to ±50? The 100-column brick slope extends 100 columns outward from the hall edge (n52+100)! Lines 697-721. So the slope can reach x = n52 + 100. If the hall's right edge n52 ≈ dLoc + 45, slope reaches dLoc+145 = 3989 — deep into the beach basin (carve ≥3891). The slope converts to brick... but the basin carve happens AFTER the dungeon pass, so the basin would then delete the brick slope (st.flags=0) and write sand — carving a hole in the approach slope and filling with water/sand. That's visually "dungeon slope cut by ocean" and could dump sand/water at the entrance approach. This is more likely than the hall itself: with dLoc near max (up to 3844) the 100-col slope definitely extends into the basin (x ≥ 3891).

OK. I have enough for a thorough report. Let me also double-check question 7: TerrainPass flattens beach region columns x < beachLeftEnd+5 and x > w-rightBeach-5 to surfLo..maxSurf (TerrainPass.ts:75-77). The dungeon entrance (x ≥ 357) can be within beachLeftEnd+5 (up to 364 for side -1) → so yes, the entrance site may be in TerrainPass's flattened beach zone (flat, low surface) — the corridor is then carved into flat low terrain near the beach, where OceanSand later (pre-dungeon) puts deep sand. TerrainPass itself doesn't place sand; it only flattens height. So the answer: yes the entrance can be inside the flattened beach zone, which combined with OceanSand means the corridor is carved in flat sand terrain.

Also worth checking the dungeonEntrance: is the Old Man's walk corridor the "outer hall" — where entStand is. Yes DungeonPass.ts:750-758.

Also mention PilesPass defines TILE_DUNGEON/WALL_DUNGEON (lines 27-29) — where used? Let me check quickly whether it gates placement on dungeon (for completeness of item 5). grep usage in PilesPass.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:56:25.826Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"TILE_DUNGEON\\|WALL_DUNGEON\" ~/Project/GLM/SandboxWorld/game/src/world/gen/vanilla/PilesPass.ts",
 "description": "Check dungeon gating usage in PilesPass"
}
```


---

## 👤 User(sidechain) · 2026-08-12T16:56:25.895Z

**📎 ToolResult**

```
27:const WALL_DUNGEON = new Set([7, 8, 9, 94, 95, 96, 97, 98, 99]);
29:const TILE_DUNGEON = new Set([41, 43, 44, 677, 678, 679]);
149:            if (y > h - 300 || WALL_DUNGEON.has(wall) || below === 30 || below === 19 || below === 25 || below === 203) {
162:            if (WALL_DUNGEON.has(wall) && rng.int(0, 2) !== 0) {
194:            if (y > h - 300 || WALL_DUNGEON.has(wall) || below === 30 || below === 19) style = rng.int(0, 6);
224:            if (y > h - 300 || WALL_DUNGEON.has(wall) || below === 30 || below === 19
226:              || TILE_DUNGEON.has(below)) style = -1;
257:            if (y > h - 300 || WALL_DUNGEON.has(wall) || below === 30 || below === 19
258:              || TILE_DUNGEON.has(below)) style = -1;
304:            if (WALL_DUNGEON.has(wall) || wall === 87 || below === 30 || below === 19 || below === 25 || below === 203) {
330:            if (TILE_DUNGEON.has(below)) {
332:            } else if (WALL_DUNGEON.has(wall) && rng.int(0, 2) !== 0) {
377:            const bad = WALL_DUNGEON.has(wall) || below === 30 || below === 19 || below === 41
380:              || below === 177 || below === 25 || below === 203 || TILE_DUNGEON.has(below);
422:            const bad = (!special) && (WALL_DUNGEON.has(wall) || below === 30 || below === 19
425:              || below === 176 || below === 177 || below === 25 || below === 203 || TILE_DUNGEON.has(below));

```


---

## 🤖 Assistant · 2026-08-12T16:56:29.723Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
PilesPass does gate on dungeon (style -1 = skip placement presumably). Good.

Now compose the final report. Include:

1. Pass order (WorldGen.ts:58-203) full list with the key fact: Dungeon runs inside 生物群系 slot (WorldGen.ts:593) and Beaches after it (602); post-dungeon sand-capable passes: Beaches (602), GravitatingSand (75/slot 5), Oasis (93), BeachDecor/ShellPiles (97), Traps (via 地表装饰 145/WorldGen.ts:726), MicroBiomes (191), TileCleanup (188), CactusCoral (184), FinalCleanup (202).

2. DungeonPass entrance & drift analysis with numbers.

3. BeachPass analysis: no dungeon gating, but horizontal reach limited.

4. GravitatingSandPass: mechanism + no gating + runs after dungeon.

5. Piles/Dunes/Desert analysis; gating survey.

6. Cleanup passes: none remove sand from dungeon.

7. TerrainPass flattening.

Candidate root causes ranked with file:line.

Let me write it.
```

</details>


---

## 🤖 Assistant · 2026-08-12T16:57:06.760Z · glm-x-preview-260804

```
## 1. Pass order (`game/src/world/gen/WorldGen.ts:58-203`)

The `passes` array is executed strictly in order (`WorldGen.ts:205-211`). Exact order:

| # | Slot name | Runs | Line |
|---|---|---|---|
| 0 | 原版地形 (Terrain/Reset) | `runTerrainPass` (`WorldGen.ts:444`) + Reset dice incl. `beachLeftEnd` (`:434`) | 59 |
| 1 | 沙丘 (Dunes) | `runDunesPass` | 62 |
| 2 | 洞穴 (Caves) | **`runOceanSandPass`** (`WorldGen.ts:541`), sand patches, tunnels, rocks, small holes, caves | 63 |
| 3 | 生物群系 (Biomes) | huge batch, see below | 66 |
| 4 | 液体 (Lakes) | empty shell | 71 |
| 5 | **引力沙 (GravitatingSand)** | `runGravitatingSandPass` | **75** |
| 6 | 微光 (Shimmer) | | 78 |
| 7 | 清理 (DirtWallCleanup) | `runCleanupPass` | 79 |
| 8 | 水体沉降 | | 85 |
| 9 | 沙上清水 | | 89 |
| 10 | 绿洲 (Oasis) | `runOasisPass` — **places `T.SAND`** | 93 |
| 11 | 海滩装饰 (ShellPiles) | `runBeachDecorPass` — **places SAND + hardened sand** | 97 |
| 12-13 | 半砖平滑 / 瀑布唇缘 | | 100-101 |
| 14-… | 薄冰, 洞穴墙变体, 生命水晶, 地狱屋, 地狱箱, 宝石洞, 苔藓, 洞穴墙, 瓦罐, 地狱熔炉, **矿骨堆 (Piles)**, 表面, 地表矿石, 倒木, **地表装饰 (incl. Traps, `WorldGen.ts:726`)**, 草墙, 栽树, 草药, 染料, 蛛网, 地表植物, 藤蔓, 花, 蘑菇, 宝石, 长苔藓, 蜂巢幼虫, 仙人掌珊瑚, **瓦片清理 (TileCleanup)**, **微群系 (MicroBiomes)**, 水生植物, 断线陷阱清理, **终清理 (FinalCleanup)** | | 105-202 |

**Inside slot 3 (vanillaBiomes, `WorldGen.ts:558-643`)** the sub-order is: Ice(561), Grass(562), Jungle(563), MudCaves(580), **Desert(581)**, Mushroom, Marble/Granite, FloatingIslands, DirtToMud/Silt, Ores, Webs, Underworld, Corruption, Lakes(591), Slush, **DUNGEON(593)**, then **MountainCaves(601) and BEACHES(602)**, Gems(609), OceanCaves(618), **Pyramid(619)**, LivingTrees, Temple, Hives, Shrines, Statues, BuriedChests, CaveHouses, SurfaceChests, …, SwordShrine(642).

**Answer to "does anything sand-related run after Dungeon?": YES — Beaches (`:602`), Pyramid (`:619`), GravitatingSand (slot 5, `:75`), Oasis (`:93`), ShellPiles/BeachDecor (`:97`), Traps (`:726`), TileCleanup (`:188`), MicroBiomes (`:191`), FinalCleanup (`:202`).** This mirrors vanilla registration (Dungeon 32 < Beaches 34 < GravitatingSand 36, comment at `:556`).

## 2. DungeonPass entrance + precalc drift

- Drift: `DungeonPass.ts:113-148`. `nx = gs.dungeonLocation - 300 + rng.int(0,599)` (`:122`), guard **only** `nx <= gs.beachDistance || nx >= w - gs.beachDistance` (`:123`) where `gs.beachDistance = 380` constant (`GenState.ts:130`). On success `gs.dungeonLocation = nx + 25 - rng.int(0,49)` (`:145`) → final range `[nx-24, nx+25]`.
- Reset values (`WorldGen.ts:434-441`): `beachLeftEnd = nextIntRange(300,340)` (=`[300,340)`) `+ (dungeonSide===1 ? 40 : 20)` → **320..359 when dungeon is left (-1), 340..379 when right (+1)**. Initial `dungeonLocation`: left → `[beachLeftEnd+50, 0.2W)` = 370..409 min; right → `[0.8W, beachRightStart-50)`.
- **Minimum possible `dungeonLocation` after drift = 381-24 = 357** — which is **less than `beachLeftEnd` (up to 359)**, i.e. the entrance can land *inside* the beach strip, inside the zone where OceanSand already wrote 50-200-deep sand columns (`BeachPass.ts:31-57`, runs pre-dungeon at `WorldGen.ts:541`). The guard compares against the constant 380, not against `beachLeftEnd`, so nothing stops this.
- Side +1 tail case: `nx` can reach `w-381`, so `dungeonLocation` ≤ `w-356`, while the right beach-basin carve starts at `waterX ≥ beachRightStart+50` (`BeachPass.ts:158-159`) = `w-330..w-289` — the entrance's 100-column approach slope (`DungeonPass.ts:697-721`) reaches ~`dungeonLocation+145`, i.e. **into the basin** in the tail case.
- Entrance carving (`dungeonEnt`, `DungeonPass.ts:539-761`): tower shell + interior cleared (`:599-605`), open outer hall for the Old Man cleared `flags=0, wall=0` (`:686-695`), door hole (`:740-744`), 100-column brick slope outward/downward (`:697-721`), `entStand` stand point (`:750-758`). Note the slope only *adds* brick below `n54+step`; **nothing clears or holds back sand terrain above/around the open hall**.

## 3. BeachPass.ts

- `runOceanSandPass` (`:11-60`, pre-dungeon): sand columns `depth` 50-200 deep over `[0, beachLeftEnd)` / `[beachRightStart, w)` (`:28-29, 48-54`). No dungeon checks (irrelevant, runs before dungeon) — but this is what makes the drift-into-beach-strip entrance site pure sand.
- `runBeachesPass` (`:106-191`, **post-dungeon**, `WorldGen.ts:602`): for each basin column it either deactivates tiles + fills water (`:141-147`/`:176-182`) **or writes `T.SAND` + active** (`:148-150`/`:183-185`), and **unconditionally zeroes walls** (`:151`/`:186`). **There is no `tileDungeon`/`wallDungeon` gate anywhere in BeachPass** — any dungeon tile in range is overwritten and its wall stripped.
- Horizontal reach: left basin carves `x ∈ [0, waterX-1]` with `waterX ≤ beachLeftEnd - minSand` (`:121-124`); right basin `x ∈ [waterX, w)` with `waterX ≥ beachRightStart + minSand` (`:156-159`). For w=4200 `minSand=50` → left basin max x ≈ 309 < 357 (entrance safe), but on the right in the drift tail case the entrance/slope can overlap the basin (see §2).

## 4. GravitatingSandPass.ts — **prime suspect**

- Mechanism (`GravitatingSandPass.ts:41-57`): per column, bottom-up; if a tile of the Falling set (sand 53, ebonsand, crimsand, pearlsand, slush, silt, shell pile 495 — `:12-24`) has an air cavity beneath it down to the next solid, **the entire cavity is ResetToType'd to that tile** (`:50-51`), i.e. any air pocket under a sand tile becomes solid sand.
- Order: slot 5 (`WorldGen.ts:75`), i.e. **after** Dungeon (slot 3). So: if the drifted entrance puts the open-air hall / approach under any overhanging sand (beach strip per §2, dune per §5), this pass **fills the carved hall with sand**. No dungeon-brick/wall gating exists in this pass.

## 5. Piles / Dunes / Desert, and the gating survey

- **PilesPass** (post-dungeon, slot 135): places only decor 185/186/187, never sand, and **does** gate on `TILE_DUNGEON`/`WALL_DUNGEON` (defs `PilesPass.ts:27-29`, gates at `:149, :162, :194, :226, :258, :304, :330-332, :377-380, :422-425`).
- **DunesPass** (pre-dungeon, slot 1): builds sand hills (60-99 high, up to ±155 from origin) via `placeCurvedLine` (`DunesPass.ts:152-199`, sand write `:195`). Rejection zones are jungle/center/snow **only** (`:63-74`) — no dungeon or beach avoidance, and origin `ox ∈ [500, w-501]` with dune half-width up to ~155 can reach x≈345, overlapping the left-side entrance zone (357-410). Pre-dungeon, so it can't cover the hall itself, but it guarantees sand overhangs above the future corridor → feeds §4/§6.
- **DesertPass** (pre-dungeon, `WorldGen.ts:581`): surface sand column fill (`DesertPass.ts:87-114`), sandstone/hardened shells (`:395-514`), fossils (`:636`). Placement is biased to the **opposite** side of the dungeon (`side = gs.dungeonSide`, `x = half + num4*-side`, `:144-146`) but after 2 side flips + `skipCheck` (`:154-163`) it can land anywhere. Runs before dungeon → source sand only.
- **Gating survey**: `tileDungeon`/`wallDungeon` gating exists in PilesPass, MountCavesPass (`:134-170`, digging stops on dungeon), LivingTreePass, BuriedChestsPass (`:46`), SurfaceDecorPasses (grass/dirt decor, `:186`, `:313`, `:437`), MicroBiomesPass (`:75`, `:255`), OceanCavesPass, CorruptionPass (`:40-48`), GemPasses (`:36`, `:247`), StructuresPass (`:534`, `:440`). **The sand-writing passes — BeachPass, GravitatingSandPass, FinalCleanupPass, OasisPass (partially), TrapsPass(sand trap) — have no dungeon-tile gating.**

## 6. Cleanup passes (vanilla "Clean Up" equivalents)

We have `CleanupPass.ts` (DirtWallCleanup: surface wall clearing `:20-58` + clump removal moved out), `TileCleanupPass.ts`, `BrokenTrapCleanupPass.ts`, `FinalCleanupPass.ts`. **None of them removes sand from the dungeon entrance.** FinalCleanup's only dungeon handling is normalizing liquids/switches/spikes *inside dungeon walls* (`FinalCleanupPass.ts:210-220`). Worse, FinalCleanup **adds** sand: ③ "falling-column growth" (`:129-148`) extends a sand column downward up to 10 tiles into open air (with a hardened-sand cap `:148`) whenever `j < worldSurface+10` and below is air — no dungeon check, so an overhanging sand tile above the open hall grows a sand pillar into the corridor. TileCleanup ⑤ places small sand pile 461 under sandstone/hardened-sand (`TileCleanupPass.ts:172-175`) — decor only, but also ungated.

## 7. TerrainPass beach flattening

`TerrainPass.ts:43-77`: columns `x < beachLeftEnd + flatBeachPadding(5)` and `x > w - rightBeach - 5` are clamped to `[surfLo, maxSurf]` (`:75-76`), i.e. the entrance site (x as low as 357 vs `beachLeftEnd+5` up to 364) **can be inside the flattened beach zone** — flat, low, and (after OceanSand) pure sand. TerrainPass writes only dirt/stone (`:88-100`), no sand, and runs before the dungeon, so it cannot cover the corridor; it just guarantees the corridor is carved into flat low sand terrain near the ocean.

## Candidate root causes (ranked)

1. **`GravitatingSandPass` cavity fill over the carved hall** — `GravitatingSandPass.ts:50-51`, runs post-dungeon (`WorldGen.ts:75`). Any sand tile above the open-air hall/approach ⇒ whole air cavity becomes sand. No dungeon gating. Strongest single mechanism.
2. **FinalCleanup ③ sand column growth into the hall** — `FinalCleanupPass.ts:129-148`, post-dungeon (`WorldGen.ts:202`). ≤10-tile sand pillar + hardened-sand cap dropped into open air below any sand tile; `!oceanDepths` (`:115-118`, `:131`) does not exclude the dungeon (x > 380).
3. **Entrance drift into the beach/ocean-sand strip** — `DungeonPass.ts:122-147` guard uses constant `beachDistance=380` (`GenState.ts:130`) while `beachLeftEnd` is 320-379 (`WorldGen.ts:434`); min `dungeonLocation` ≈ 357 can be `< beachLeftEnd`, inside OceanSand's 50-200-deep sand (`BeachPass.ts:31-57`). This is the *enabler* that puts sand above/around the corridor for causes 1-2. Also worth verifying: the `+40/+20` beach widening at `WorldGen.ts:434` applies `+40` when `dungeonSide===1` (left beach = the **non-dungeon** side), which looks inverted vs the vanilla "widen the dungeon-side beach" intent and makes the dungeon-side beach narrower.
4. **Beaches basin overwrite in the right-side tail case** — `BeachPass.ts:148-150, 183-186, 151/186` (sand write + wall strip, no dungeon gate), post-dungeon at `WorldGen.ts:602`; reachable only when drift pushes the entrance to `nx ≈ w-381` and the 100-column brick slope (`DungeonPass.ts:697-721`) crosses `beachRightStart+50`.
5. **Dunes overlapping the entrance site** — `DunesPass.ts:63-74` (no dungeon/beach rejection), `:195` sand write; pre-dungeon but supplies the overhanging sand mass that causes 1 and 2.
6. Weaker/conditional: ShellPiles sand+hardened-sand at waterline anchors (`BeachPass.ts:221-267`, post-dungeon slot 97) can reach ~124 columns inland of `shellStartX` (`:296-300, 323-327`) — only lands on bare sand with adjacent water (`:228-229`), so only the basin rim; Traps sand-trap (`TrapsPass.ts:213-283`) requires wall 187/216 + `y ≥ worldSurface`, i.e. underground desert only; Oasis is blocked by the sand-only box check (`OasisPass.ts:60-78`, dungeon brick is solid non-sand ⇒ reject); Pyramid keeps ≥ `0.15w` from `gs.dungeonLocation` (`StructuresPass.ts:549-553`) and requires a sand column (`:557`).
```
