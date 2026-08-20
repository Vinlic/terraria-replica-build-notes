# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-11T18:17:13.564Z

```
你在 ~/Project/GLM/SandboxWorld/ 项目（工作目录 game/）。这是"近似清零"工程的**终审复查**（只读，禁止修改文件）。（前代理两次流中断，你从头接手——高效执行：以 grep 为主、只读关键段落，避免长读。）

背景：初普查 B 清单（src/entities/ + src/render/ + src/drops/ + src/items/ + src/physics/ + src/stats/，45 条）之后已修复大批：AI 四批（bossAI_moon_events/martian/lunar_misc/dd2.ts + lategame 重写，59+ 种）、渲染批（GlowMask/月总躯干/女皇/塔护盾/微光/Boss条）、敌弹批（hitPlayer/StatusPlayer/Chilled 62/Frozen 63）、lategame 批（克隆体 440/522 轨道/贴图 26 张补齐）、波 3 useStyle 全族+弹药格+近战门、波 8 食物链（WellFed 64-66）、提取器波 7。

任务：复查 B 清单每条现状，判定（以磁盘最新代码为准）：
- ✅ 已清零（真 1:1）| 📋 依赖登记（注释精确到缺什么子系统/素材=合规终态）| ❌ 漏网（既非 1:1 也无精确登记——重点产出）

复查路径（高效）：
1. **AI 家族重统计**：读 Enemy.ts 分发表的 case 全集 vs public/sprites/vanilla-npcs.json 各 NPC aiStyle——统计还有哪些 NPC 落 default 兜底（用 node 脚本统计最快：json 遍历 aiStyle→NPC 列表，对照 case 集）。
2. Enemy.ts 散点（初查 677/805/1069 CanHit/1253/1468/2139/2699/2749/2782/2791/3316/3460）grep 现状。
3. bossAI_*.ts 各文件"近似/简化/二期"残留 grep。
4. render/ 残留（Glow_100/101/146/154/156、着色器载体类、BiomeBackground、WaterfallRenderer 坡面——渲染批处置过的除外）。
5. NpcDrops（RemixSeed 类外还有吗）、items/Inventory/physics/stats 残留。

产出 ≤60 行：三类计数 + ❌ 漏网清单（每条：文件:行 | 现状 | 为何不合规）。
```

---

## 📎 Attachment · skill_listing · 2026-08-11T18:17:13.567Z

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

## 🤖 Assistant · 2026-08-11T18:17:15.451Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by exploring the project structure to understand the codebase.

The task is a final review (终审复查) of "近似清零" (near-zero approximation) project. I need to:
1. AI family re-statistics: read Enemy.ts dispatch table case set vs public/sprites/vanilla-npcs.json NPC aiStyle — find NPCs falling to default fallback
2. Enemy.ts scattered points grep status
3. bossAI_*.ts files residual grep
4. render/ residuals
5. NpcDrops, items/Inventory/physics/stats residuals

Let me start with parallel exploration.
```

</details>


---

## 🤖 Assistant · 2026-08-11T18:17:16.148Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/entities/ ~/Project/GLM/SandboxWorld/game/src/render/ ~/Project/GLM/SandboxWorld/game/src/drops/ ~/Project/GLM/SandboxWorld/game/src/items/ ~/Project/GLM/SandboxWorld/game/src/physics/ ~/Project/GLM/SandboxWorld/game/src/stats/ 2>&1",
 "description": "List key source directories"
}
```


---

## 👤 User(sidechain) · 2026-08-11T18:17:16.174Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/drops/:
NpcDrops.ts

~/Project/GLM/SandboxWorld/game/src/entities/:
Arrow.ts
Bobber.ts
bossAI_dd2.ts
bossAI_duke_moonlord.ts
bossAI_golem.ts
bossAI_lategame.ts
bossAI_lunar_misc.ts
bossAI_martian.ts
bossAI_moon_events.ts
bossAI_queenbee_plantera.ts
bossAI_wof.ts
bossAI.ts
Critter.ts
Dart.ts
Enemy.ts
Entity.ts
FallingBlock.ts
ItemDrop.ts
MagicProj.ts
Minecart.ts
MinionProj.ts
Player.ts
Portal.ts
projTargets.ts
Tombstone.ts
TownNPC.ts
types.ts
waterAvoid.ts
WeaponProj.ts

~/Project/GLM/SandboxWorld/game/src/items/:
Inventory.ts

~/Project/GLM/SandboxWorld/game/src/physics/:
Conveyor.ts
TileCollision.ts

~/Project/GLM/SandboxWorld/game/src/render/:
AutoTiler.ts
BiomeBackground.ts
BlendFraming.ts
Camera.ts
ChunkCache.ts
EmoteBubble.ts
MapColors.ts
MenuBackground.ts
Renderer.ts
ResourceBars.ts
SkyRenderer.ts
TileAnim.ts
TileParticles.ts
VanillaLiquidRenderer.ts
VanillaTiler.ts
VanillaWallTiler.ts
WallTiler.ts
WaterfallRenderer.ts
WeatherRenderer.ts

~/Project/GLM/SandboxWorld/game/src/stats/:
Buffs.ts
TouchDamage.ts

```


---

## 🤖 Assistant · 2026-08-11T18:17:16.900Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts 2>/dev/null; ls ~/Project/GLM/SandboxWorld/game/src/entities/ 2>/dev/null | head -50",
 "description": "Check Enemy.ts size and entities dir"
}
```


---

## 👤 User(sidechain) · 2026-08-11T18:17:16.931Z

**📎 ToolResult**

```
    3906 ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
Arrow.ts
Bobber.ts
bossAI_dd2.ts
bossAI_duke_moonlord.ts
bossAI_golem.ts
bossAI_lategame.ts
bossAI_lunar_misc.ts
bossAI_martian.ts
bossAI_moon_events.ts
bossAI_queenbee_plantera.ts
bossAI_wof.ts
bossAI.ts
Critter.ts
Dart.ts
Enemy.ts
Entity.ts
FallingBlock.ts
ItemDrop.ts
MagicProj.ts
Minecart.ts
MinionProj.ts
Player.ts
Portal.ts
projTargets.ts
Tombstone.ts
TownNPC.ts
types.ts
waterAvoid.ts
WeaponProj.ts

```


---

## 🤖 Assistant · 2026-08-11T18:17:17.966Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me do the AI family statistics first. I need to read Enemy.ts dispatch table case set, and vanilla-npcs.json aiStyle.
```

</details>


---

## 🤖 Assistant · 2026-08-11T18:17:18.209Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case \" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -120",
 "description": "List switch cases in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-11T18:17:18.236Z

**📎 ToolResult**

```
261:  crawlT = 0;            // AI_040 爬墙帧累加器（FindFrame case 165 族：(|vx|+|vy|)×0.5，24 循环）
379:        case 92: this.dummyAI(game); break;                            // AI_092 训练假人（NPC 488）
380:        case 1: this.slimeAI(game, p); break;                          // AI_001 史莱姆
381:        case 2: this.floatEyeAI(game, p); break;                        // AI_002 飘浮眼（原版核）
382:        case 3:
396:        case 4: this.eocAI(game, (game as unknown as { player: Player }).player ?? null); break; // AI_004 克苏鲁之眼（NPC.cs:19909）
397:        case 5: this.swarmerAI(game, p); break;                         // AI_005 噬魂怪族（原版蜂群核）
398:        case 6: this.wormAI(game, p); break;                           // AI_006 蠕虫族（头）
399:        case 8: this.casterAI(game, p); break;                          // AI_008 法师族（传送+弹幕）
400:        case 10: this.cursedSkullAI(game, p); break;                     // AI_010 诅咒头骨（地牢飞行族）
401:        case 11:
407:        case 12: skeletronHandAI(this, game, p); break;                    // AI_012 骷髅王手(锚定头)
408:        case 20: this.blazingWheelAI(); break;                           // AI_020 火轮（地牢陷阱）
409:        case 21: this.spikeBallAI(game); break;                          // AI_021 刺球（地牢陷阱）
410:        case 14: this.batAI(game, p); break;                            // AI_014 蝙蝠/飞行族（1.4.5.6 原版核）
411:        case 16: this.swimAI(game, p); break;                           // AI_016 游泳族（鲨鱼/食人鱼）
412:        case 18: this.jellyfishAI(game, p); break;                      // AI_018 水母族（脉冲游动）
413:        case 22: this.ghostAI(game, p); break;                          // AI_022 幽灵族（穿墙缓速）
414:        case 13: this.plantAI(game, p); break;                          // AI_013 植物/攀爬者族（锚点伸展）
415:        case 15: kingSlimeAI(this, game, p); break;                       // AI_015 史莱姆王(大跳+小史莱姆)
416:        case 54: brainOfCthulhuAI(this, game, p); break;                  // AI_054 克脑(爬行者环→瞬移冲刺)
417:        case 55: creeperAI(this, game, p); break;                         // AI_055 爬行者(环绕漂移)
418:        case 30: twinsAI(this, game, p, false); break;                    // AI_030 雷神之眼 125(悬浮/连冲/变身/激光)
419:        case 31: twinsAI(this, game, p, true); break;                     // AI_031 魔神之眼 126(诅咒焰/火焰喷射)
420:        case 32: skeletronPrimeAI(this, game, p); break;                  // AI_032 机械骷髅王头 127(4 部件/旋冲/白天狂暴)
421:        case 33: case 34: case 35: case 36: primePartAI(this, game, p); break; // AI_033-036 Prime 部件(锯/激光/钳/炮)
422:        case 37: destroyerAI(this, game, p); break;                       // AI_037 毁灭者 134(80 段链穿地/探针激光)
423:        case 27: wallOfFleshAI(this, game, (game as unknown as { player: Player }).player ?? null); break; // AI_027 血肉墙(空腔扫描/速度血量档/Leech 轮)
424:        case 28: wofEyeAI(this, game, p); break;                          // AI_028 血肉墙之眼(钉墙吸附/激光连射 83)
425:        case 29: hungryAI(this, game, p); break;                          // AI_029 饥饿者(挂墙环绕→受击脱落扑咬)
426:        case 84: lunaticCultistAI(this, game, p); break;                  // AI_084 拜月教邪教徒(瞬移+四系弹幕轮换)
428:        case 81: moonLordFreeEyeAI(this, game, p); break;                // AI_081 月总游离眼 400（cs:38224 十槽攻击表+死光）
429:        case 82: moonLeechAI(this, game, p); break;                       // AI_082 月总水蛭块 401（cs:38668 90t 插值吸血回灌）
430:        case 83:                                                            // AI_083 神秘石碑 437/忠实信徒 438（cs:38793）
434:        case 86: phantomAI(this, game, p); break;                          // AI_086 暗焰幻影 472/远古幻影 521（cs:39261 穿墙横掠循环）
435:        case 87: bigMimicAI(this, game, p); break;                         // AI_087 珍稀四宝箱怪 473-476（cs:39520 跳扑+蓄能/俯冲/三连扑）
436:        case 88: mothronAI(this, game, p); break;                          // AI_088 飞蛾魔 477（cs:39876 日食限定轮换+产卵）
437:        case 89: mothronEggAI(this, game, p); break;                       // AI_089 蛾卵 478（cs:40407 900t→Transform 479）
438:        case 90: babyMothronAI(this, game, p); break;                      // AI_090 幼蛾 479（cs:40450 日食贴脸冲撞）
439:        case 91: graniteElementalAI(this, game, p); break;                 // AI_091 花岗岩元素 483（cs:40686 五态寻路）
440:        case 120: empressOfLightAI(this, game, p); break;                 // AI_120 光之女皇(连段选招/半血变身)
441:        case 121: queenSlimeAI(this, game, p); break;                     // AI_121 史莱姆皇后(走路四连跳→飞行二阶段)
442:        case 100: ancientLightAI(this, game, p); break;                  // AI_100 远古之光 522(直飞投射物型)
443:        case 101: ancientDoomAI(this, game, p); break;                  // AI_101 远古末日 523(锚邪教徒蓄能自爆)
444:        case 43: queenBeeAI(this, game, p); break;                        // AI_043 蜂后(悬浮俯冲/蜜蜂机枪/毒刺)
445:        case 50: planteraHookAI(this, game, p); break;                    // AI_050 真菌孢子 261/孢子 265
446:        case 51: planteraAI(this, game, p); break;                        // AI_051 世纪之花(钩蔓牵引→二阶段)
447:        case 52: planteraTentacleAI(this, game, p); break;                // AI_052 钩蔓 263(抓墙换锚收线)
448:        case 53: planteraTentacle2AI(this, game, p); break;               // AI_053 触须 264(二阶段环绕)
449:        case 69: dukeFishronAI(this, game, p); break;                     // AI_069 猪鲨(冲撞/泡泡/龙卷,半血变身)
450:        case 70: dukeBubbleAI(this, game, p); break;                      // AI_070 爆裂泡泡 371
451:        case 71: sharkronAI(this, game, p); break;                        // AI_071 鲨鱼龙 372/373(龙卷出鲨,升空蓄力→扑咬)
452:        case 77: moonLordCoreAI(this, game, p); break;                    // AI_077 月总核心 398(双手死前无敌)
453:        case 78: moonLordHandAI(this, game, p); break;                    // AI_078 月总手 397(攻表/睁眼可击)
454:        case 79: moonLordHeadAI(this, game, p); break;                    // AI_079 月总头 396(死亡之光/吸血)
455:        case 45: golemAI(this, game, p); break;                        // AI_045 石巨人本体 245(蓄力跳/挂头无敌)
456:        case 46: golemHeadAI(this, game, p); break;                      // AI_046 挂载头 246(锚本体/火焰弹眼激光;249 自由态)
457:        case 47: golemFistAI(this, game, p); break;                      // AI_047 石巨人拳 247/248(肩锚冲拳)
458:        case 40: this.wallCreeperAI(game, p); break;                      // AI_040 爬墙蜘蛛族（贴背景墙爬行+形态互转）
459:        case 42: this.lostGirlAI(game, p); break;                         // AI_042 失落女孩（伪装静止→Nymph 变身 cs:30281-30310）
460:        case 0: this.boundNPCAI(game, p); break;                          // AI_000 被缚NPC（cs:19774 站立/水上漂流；Enemy 侧防御，常规走 TownNPC.bound）
461:        case 17: this.vultureAI(game, p); break;                          // AI_017 秃鹫（cs:24079 栖息→200px盒/受击起飞，单向不回落）
462:        case 19: this.antlionAI(game, p); break;                          // AI_019 蚁狮（cs:24465 扎沙不动+沙球；传送带特例略）
463:        case 23: this.flyingWeaponAI(game, p); break;                     // AI_023 飞行武器（cs:25316 冲/漂100/转120 循环，受击回蓄转）
464:        case 25: this.mimicAI(game, p); break;                            // AI_025 宝箱怪（cs:25621 伪装200px盒→小小大跳循环）
465:        case 39: this.tortoiseAI(game, p); break;                         // AI_039 陆龟族（cs:29257 待机蓄力→蓄势→旋冲→恢复）
466:        case 41: this.herplingAI(game, p); break;                         // AI_041 赫柏林/德普林（cs:30017 低跳连扑；378 炸弹自爆略）
467:        case 44: this.flyingSwarmerAI(game, p); break;                    // AI_044 飞鱼/蚁狮蜂（cs:30999 分轴限速追+失视逃逸）
468:        case 56: this.dungeonSpiritAI(game, p); break;                    // AI_056 地牢之魂（cs:32915 穿墙0.99惯性追踪）
469:        case 26: this.chargerAI(game, p); break;                        // AI_026 独角兽/冲锋族（原版核）
470:        case 107: this.chargerAI(game, p, 1); break;                    // AI_107 ImprovedWalkers（0.07/±1.0 walker 档，NPC.145.cs:43153 引擎核同构）
471:        case 94: this.towerAI(game, p); break;                          // AI_094 星璇四塔（NPC.cs:41029-41443，核心 1:1）
478:        case 85: case 95: case 96: case 99: this.swarmerAI(game, p); break;
479:        case 97: this.casterAI(game, p); break;
481:        case 57: mourningWoodAI(this, game, p); break;                  // AI_057 悲木 325/常世吼 344（cs:32937 悬浮树怪+分阶段弹幕）
482:        case 58: pumpkingAI(this, game, p); break;                       // AI_058 南瓜王 327（cs:33246 悬浮/俯冲+生双刃）
483:        case 59: pumpkingBladeAI(this, game, p); break;                   // AI_059 南瓜王之刃 328（cs:33405 锚主环绕/俯冲/横扫）
484:        case 60: iceQueenAI(this, game, p); break;                        // AI_060 冰雪女王 345（cs:33588 滑翔/落冰/旋射三态）
485:        case 61: santaNK1AI(this, game, p); break;                        // AI_061 圣诞坦克 346（cs:33902 悬浮+链炮/火箭/礼盒）
486:        case 62: elfCopterAI(this, game, p); break;                       // AI_062 玩具直升机 347（cs:34155 近距悬停点射）
487:        case 63: flockoAI(this, game, p); break;                          // AI_063 弗洛科 352（cs:34208 追踪+旋冲）
488:        case 38: snowmanAI(this, game, p); break;                         // AI_038 雪人三兄弟 143/144/145（cs:29115 跳扑/停顿/雪球）
489:        case 9: bouncingBallAI(this, game, p); break;                     // AI_009 弹跳球族 25/30/33/112/516/665/666（cs:21349 直飞球）
491:        case 80: martianProbeAI(this, game, p); break;                    // AI_080 火星探测器 399（cs:38129 逃逸→StartInvasion(4)）
492:        case 76: martianSaucerAI(this, game, p); break;                   // AI_076 火星飞碟核心 395（cs:36322 600t 六窗口+部件生成）
493:        case 72: bubbleShieldAI(this, game, p); break;                    // AI_072 泡泡盾 384（cs:35318 锚军官 383）
494:        case 73: teslaTurretAI(this, game, p); break;                     // AI_073 特斯拉炮塔 387（cs:35340 部署渐显+180t 电击）
495:        case 74:                                                          // AI_074 火星无人机 388/日耀 Corite 418（cs:35452 悬浮→扑咬→自爆）
499:        case 75:                                                          // AI_075 飞碟部件 392/393/394 + 骑手 390（cs:35745 锚主体+攻击窗）
505:        case 48: golemHeadAI(this, game, p); break;                       // AI_048 自由石巨人头 249（cs:31500,golemHeadAI 已含自由态分支）
506:        case 49: angryNimbusAI(this, game, p); break;                     // AI_049 愤怒云 250（cs:31742 悬顶淋雨 264）
508:        case 93: flyingDutchmanAI(this, game, p); break;                  // AI_093 荷兰飞盗船 491（cs:40918 四炮部件+海盗跳舱+贴地巡航）
509:        case 102: sandElementalAI(this, game, p); break;                  // AI_102 沙尘精 541（cs:42224 walker 核+沙暴标记 658）
510:        case 103: sandSharkAI(this, game, p); break;                      // AI_103 沙鲨族 542-545（cs:42621 沙中巡游+跃沙扑咬,沙族豁免碰撞）
511:        case 104: dd2AttackerTestAI(this, game); break;                   // AI_104 DD2AttackerTest 547（cs:42807 出生即消）
512:        case 105: eterniaCrystalAI(this, game, p); break;                 // AI_105 永恒水晶 548（cs:42810 180t 双端放门+胜负演出）
513:        case 106: lanePortalAI(this, game, p); break;                     // AI_106 神秘传送门 549（cs:43063 出怪门节拍,事件依赖 DD2_EVENT_HOOKS）
514:        case 108: divingFlyerAI(this, game, p); break;                    // AI_108 飞龙 558-560/小妖魔滑翔怪 574-575（cs:65959 俯冲五态+自爆）
515:        case 109: darkMageAI(this, game, p); break;                       // AI_109 黑暗魔法师 564/565（cs:66392 walker+三连招 675/674/673）
516:        case 110: betsyAI(this, game, p); break;                          // AI_110 双足翼龙 551（cs:62266 八槽攻表+rotation 收敛）
517:        case 111: dd2LightningBugAI(this, game, p); break;                // AI_111 埃特尼亚荧光虫 578（cs:66799 悬停蓄电 682 电弧）
521:      case 'slime_green':
522:      case 'slime_blue': this.slimeAI(game, hasPlayer ? player : null); break;
523:      case 'zombie': this.zombieAI(game, hasPlayer ? player : null); break;
524:      case 'demon_eye':
525:      case 'cave_bat': this.flyAI(game, hasPlayer ? player : null, 0.09); break;
526:      case 'servant_of_cthulhu': this.flyAI(game, hasPlayer ? player : null, 0.22); break;
527:      case 'eye_of_cthulhu': this.eocAI(game, player ?? null); break;
1199:    // 行走帧累加（FindFrame case 165/237/238/240/531，cs:73795-73817：
2555:      case 24: this.birdAI(game, player); return;                        // AI_024 鸟
2556:      case 1: this.slimeAI(game, player); return;                         // AI_001 蚱蜢（含专属差异项）
2557:      case 16: this.swimAI(game, player); return;                         // AI_016 鱼类小动物（含河鲀/海豚特化）
2558:      case 64: this.fireflyAI(game, player); return;                      // AI_064 萤火虫
2559:      case 65: this.butterflyAI(game, player); return;                    // AI_065 蝴蝶
2560:      case 66: this.wormCritterAI(game); return;                          // AI_066 蠕虫
2561:      case 67: this.snailAI(game); return;                                // AI_067 蜗牛
2562:      case 68: this.duckFlyAI(game, player); return;                      // AI_068 鸭飞形
2563:      case 112: this.fairyAI(game, player); return;                       // AI_112 仙灵
2564:      case 113: this.windyBalloonAI(game, player); return;                // AI_113 风气球（cs:43036 挂史莱姆）
2565:      case 114: this.dragonflyAI(game, player); return;                   // AI_114 蜻蜓

```


---

## 🤖 Assistant · 2026-08-11T18:17:24.457Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle\" ~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json | head -5; node -e \"\nconst j=require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst arr=Array.isArray(j)?j:(j.npcs||j.data||Object.values(j).find(v=>Array.isArray(v)));\nif(!arr){console.log('keys',Object.keys(j).slice(0,10));process.exit(0);}\nconsole.log('count',arr.length,'sample',JSON.stringify(arr[0]));\n\"",
 "description": "Inspect vanilla-npcs.json structure"
}
```


---

## 👤 User(sidechain) · 2026-08-11T18:17:28.460Z

**📎 ToolResult**

```
<persisted-output>
Output too large (133.2KB). Full output saved to: ~/.claude/projects/-Users-user-Project-GLM-SandboxWorld/372ae608-2da7-4502-87f6-cedcc2af7bb7/tool-results/bgcw6dabk.txt

Preview (first 2KB):
1:{"1":{"id":1,"name":"Blue Slime","frames":2,"lifeMax":25,"damage":7,"defense":2,"aiStyle":1,"width":24,"height":18,"HitSound":"NPCHit1","DeathSound":"NPCDeath1","alpha":175,"color":[0,80,255,100]},"2":{"id":2,"name":"Demon Eye","frames":2,"lifeMax":60,"damage":18,"defense":2,"knockBackResist":0.8,"aiStyle":2,"width":30,"height":32,"HitSound":"NPCHit1","DeathSound":"NPCDeath1"},"3":{"id":3,"name":"Zombie","frames":3,"lifeMax":45,"damage":14,"defense":6,"knockBackResist":0.5,"aiStyle":3,"width":18,"height":40,"HitSound":"NPCHit1","DeathSound":"NPCDeath2"},"4":{"id":4,"name":"Eye of Cthulhu","frames":6,"lifeMax":2800,"damage":15,"defense":12,"knockBackResist":0,"aiStyle":4,"width":100,"height":110,"npcSlots":5,"noGravity":true,"noTileCollide":true,"HitSound":"NPCHit1","DeathSound":"NPCDeath1"},"5":{"id":5,"name":"Servant of Cthulhu","frames":2,"lifeMax":8,"damage":12,"defense":0,"aiStyle":5,"width":20,"height":20,"noGravity":true,"noTileCollide":true,"HitSound":"NPCHit1","DeathSound":"NPCDeath1"},"6":{"id":6,"name":"Eater of Souls","frames":2,"lifeMax":40,"damage":22,"defense":8,"knockBackResist":0.5,"aiStyle":5,"width":30,"height":30,"npcSlots":1,"noGravity":true,"HitSound":"NPCHit1","DeathSound":"NPCDeath1"},"7":{"id":7,"name":"Devourer","frames":1,"lifeMax":100,"damage":31,"defense":2,"knockBackResist":0,"aiStyle":6,"width":22,"height":22,"npcSlots":3.5,"noGravity":true,"noTileCollide":true,"HitSound":"NPCHit1","DeathSound":"NPCDeath1","behindTiles":true},"8":{"id":8,"name":"NPC_8","frames":1,"lifeMax":100,"damage":16,"defense":6,"knockBackResist":0,"aiStyle":6,"width":22,"height":22,"noGravity":true,"noTileCollide":true,"HitSound":"NPCHit1","DeathSound":"NPCDeath1","behindTiles":true},"9":{"id":9,"name":"NPC_9","frames":1,"lifeMax":100,"damage":13,"defense":10,"knockBackResist":0,"aiStyle":6,"width":22,"height":22,"noGravity":true,"noTileCollide":true,"HitSound":"NPCHit1","DeathSound":"NPCDeath1","behindTiles":true},"10":{"id":10,"name":"Giant Worm","frames":1,"l
...
</persisted-output>

```


---

## 🤖 Assistant · 2026-08-11T18:17:32.107Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
vanilla-npcs.json is a single-line JSON with id keys. Let me write a node script to compute aiStyle → NPC list, and compare to case set. But wait — the case set is in Enemy.ts. I need to extract the case numbers. Note case labels can be multi-value.

Also I should note the JSON may have NPC ids that aren't in the game at all (e.g., NPC_8, NPC_9 placeholders). But the task says count NPCs falling to default fallback. Let me be careful: NPCs that are type-only names (NPC_8, NPC_9) with no sprite might not spawn. But let's count anyway, and note.

Let me write the node script carefully. But node -e with require of a path outside cwd... path is absolute so fine.

Note: no file creation allowed. node -e is read-only, fine.

Let me extract case numbers from Enemy.ts dispatch region (lines ~379-516).
```

</details>


---

## 🤖 Assistant · 2026-08-11T18:17:33.684Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst j=require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst byStyle={};\nfor(const k in j){const n=j[k];const s=n.aiStyle??0;(byStyle[s]=byStyle[s]||[]).push({id:n.id,name:n.name});}\nconst styles=Object.keys(byStyle).map(Number).sort((a,b)=>a-b);\nconsole.log('total NPC',Object.keys(j).length,'styles',styles.length);\nfor(const s of styles)console.log(s+':',byStyle[s].length,'=>',byStyle[s].slice(0,30).map(n=>n.id+':'+n.name).join(' | ')+(byStyle[s].length>30?' ...':''));\n\" 2>&1 | head -60",
 "description": "Group NPCs by aiStyle"
}
```


---

## 👤 User(sidechain) · 2026-08-11T18:17:50.479Z

**📎 ToolResult**

```
total NPC 653 styles 120
0: 6 => 105:NPC_105 | 106:NPC_106 | 123:NPC_123 | 354:NPC_354 | 376:NPC_376 | 579:NPC_579
1: 25 => 1:Blue Slime | 16:Mother Slime | 59:Lava Slime | 71:Dungeon Slime | 81:Corrupt Slime | 138:Illuminant Slime | 141:Toxic Sludge | 147:Ice Slime | 183:Crimslime | 184:Spiked Ice Slime | 204:Spiked Jungle Slime | 225:Umbrella Slime | 244:Rainbow Slime | 302:Slime | 304:Hoppin' Jack | 333:Slime | 334:Slime | 335:Slime | 336:Slime | 377:Grasshopper | 446:Gold Grasshopper | 535:NPC_535 | 537:Sand Slime | 658:QueenSlimeMinionBlue | 659:QueenSlimeMinionPink
2: 13 => 2:Demon Eye | 116:The Hungry | 133:Wandering Eye | 170:Pigron | 171:Pigron | 180:Pigron | 190:Demon Eye | 191:Demon Eye | 192:Demon Eye | 193:Demon Eye | 194:Demon Eye | 317:Demon Eye | 318:Demon Eye
3: 186 => 3:Zombie | 21:Skeleton | 26:Goblin Peon | 27:Goblin Thief | 28:Goblin Warrior | 31:Angry Bones | 44:Undead Miner | 47:Corrupt Bunny | 52:Doctor Bones | 53:The Groom | 67:Crab | 73:Goblin Scout | 77:Armored Skeleton | 78:Mummy | 79:Dark Mummy | 80:Light Mummy | 104:Werewolf | 109:Clown | 110:Skeleton Archer | 111:Goblin Archer | 120:Chaos Elemental | 132:Zombie | 140:Possessed Armor | 159:Vampire | 161:Frozen Zombie | 162:Frankenstein | 163:NPC_163 | 164:NPC_164 | 166:Swamp Thing | 167:Undead Viking ...
4: 1 => 4:Eye of Cthulhu
5: 17 => 5:Servant of Cthulhu | 6:Eater of Souls | 23:Meteor Head | 42:Hornet | 94:Corruptor | 139:Probe | 173:Crimera | 176:Moss Hornet | 205:Moth | 210:Bee | 211:Bee | 231:Hornet | 232:Hornet | 233:Hornet | 234:Hornet | 235:Hornet | 252:Parrot
6: 42 => 7:Devourer | 8:NPC_8 | 9:NPC_9 | 10:Giant Worm | 11:NPC_11 | 12:NPC_12 | 13:Eater of Worlds | 14:NPC_14 | 15:NPC_15 | 39:Bone Serpent | 40:NPC_40 | 41:NPC_41 | 87:Wyvern | 88:NPC_88 | 89:NPC_89 | 90:NPC_90 | 91:NPC_91 | 92:NPC_92 | 95:Digger | 96:NPC_96 | 97:NPC_97 | 98:World Feeder | 99:NPC_99 | 100:NPC_100 | 117:Leech | 118:NPC_118 | 119:NPC_119 | 375:NPC_375 | 402:Milkyway Weaver | 403:Milkyway Weaver Body ...
7: 70 => 17:Merchant | 18:Nurse | 19:Arms Dealer | 20:Dryad | 22:Guide | 37:Old Man | 38:Demolitionist | 46:Bunny | 54:Clothier | 107:Goblin Tinkerer | 108:Wizard | 124:Mechanic | 142:Santa Claus | 148:Penguin | 149:Penguin | 160:Truffle | 178:Steampunker | 207:Dye Trader | 208:Party Girl | 209:Cyborg | 227:Painter | 228:Witch Doctor | 229:Pirate | 230:NPC_230 | 299:Squirrel | 300:Mouse | 303:Bunny | 337:Bunny | 353:Stylist | 361:Frog ...
8: 12 => 24:Fire Imp | 29:Goblin Sorcerer | 32:Dark Caster | 45:Tim | 172:Rune Wizard | 281:Ragged Caster | 282:Ragged Caster | 283:Necromancer | 284:Necromancer | 285:Diabolist | 286:Diabolist | 533:Desert Spirit
9: 7 => 25:NPC_25 | 30:NPC_30 | 33:NPC_33 | 112:NPC_112 | 516:NPC_516 | 665:NPC_665 | 666:NPC_666
10: 2 => 34:Cursed Skull | 289:Giant Cursed Skull
11: 2 => 35:Skeletron | 68:Dungeon Guardian
12: 1 => 36:NPC_36
13: 6 => 43:Man Eater | 56:Snatcher | 101:Clinger | 175:Angry Trapper | 259:Fungi Bulb | 260:Giant Fungi Bulb
14: 17 => 48:Harpy | 49:Cave Bat | 51:Jungle Bat | 60:Hellbat | 62:Demon | 66:Voodoo Demon | 93:Giant Bat | 121:Slimer | 137:Illuminant Bat | 150:Ice Bat | 151:Lava Bat | 152:Giant Flying Fox | 156:Red Devil | 158:NPC_158 | 226:Flying Snake | 634:Spore Bat | 660:QueenSlimeMinionPurple
15: 1 => 50:King Slime
16: 13 => 55:Goldfish | 57:Corrupt Goldfish | 58:Piranha | 65:Shark | 102:Angler Fish | 157:Arapaima | 241:Blood Feeder | 465:Vicious Goldfish | 592:Gold Goldfish | 607:Pupfish | 615:Dolphin | 688:Pufferfish | 692:Orca
17: 2 => 61:Vulture | 301:Raven
18: 6 => 63:Blue Jellyfish | 64:Pink Jellyfish | 103:Green Jellyfish | 221:Squid | 242:Blood Jelly | 256:Fungo Fish
19: 1 => 69:Antlion
20: 1 => 70:NPC_70
21: 1 => 72:NPC_72
22: 10 => 75:Pixie | 82:Wraith | 122:Gastropod | 169:Ice Elemental | 182:Floaty Gross | 253:Reaper | 268:Ichor Sticker | 316:Ghost | 330:Poltergeist | 490:Drippler
23: 3 => 83:Cursed Hammer | 84:Enchanted Sword | 179:Crimson Axe
24: 11 => 74:Bird | 297:Blue Jay | 298:Cardinal | 442:Gold Bird | 611:Owl | 671:Scarlet Macaw | 672:Blue Macaw | 673:Toucan | 674:Yellow Cockatiel | 675:Gray Cockatiel | 689:NPC_689
25: 3 => 85:Mimic | 341:Present Mimic | 629:Ice Mimic
26: 7 => 86:Unicorn | 155:Wolf | 315:Headless Horseman | 329:Hellhound | 410:NPC_410 | 423:Evolution Beast | 546:Angry Tumbler
27: 1 => 113:Wall of Flesh
28: 1 => 114:NPC_114
29: 1 => 115:The Hungry
30: 1 => 125:Retinazer
31: 1 => 126:Spazmatism
32: 1 => 127:Skeletron Prime
33: 1 => 129:Prime Saw
34: 1 => 130:Prime Laser
35: 1 => 128:Prime Vice
36: 1 => 131:Prime Cannon
37: 3 => 134:The Destroyer | 135:NPC_135 | 136:NPC_136
38: 3 => 143:Snowman Gangsta | 144:Mister Stabby | 145:Snow Balla
39: 5 => 153:Giant Tortoise | 154:Ice Tortoise | 417:Sroller | 496:Giant Shelly | 497:NPC_497
40: 5 => 165:Wall Creeper | 237:Jungle Creeper | 238:Black Recluse | 240:Blood Crawler | 531:Sand Poacher
41: 3 => 174:Herpling | 177:Derpling | 378:Chattering Teeth Bomb
42: 1 => 195:Lost Girl
43: 1 => 222:Queen Bee
44: 3 => 224:Flying Fish | 509:Giant Antlion Swarmer | 581:Antlion Swarmer
45: 1 => 245:Golem
46: 1 => 246:NPC_246
47: 2 => 247:NPC_247 | 248:NPC_248
48: 1 => 249:NPC_249
49: 1 => 250:Angry Nimbus
50: 2 => 261:NPC_261 | 265:NPC_265
51: 1 => 262:Plantera
52: 1 => 263:NPC_263
53: 1 => 264:NPC_264
54: 1 => 266:Brain of Cthulhu
55: 1 => 267:Creeper
56: 1 => 288:Dungeon Spirit
57: 2 => 325:Mourning Wood | 344:Everscream
58: 1 => 327:Pumpking

```


---

## 🤖 Assistant · 2026-08-11T18:17:52.469Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst j=require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst byStyle={};\nfor(const k in j){const n=j[k];const s=n.aiStyle??0;(byStyle[s]=byStyle[s]||[]).push({id:n.id,name:n.name});}\nconst styles=Object.keys(byStyle).map(Number).sort((a,b)=>a-b);\nfor(const s of styles.filter(s=>s>=59))console.log(s+':',byStyle[s].length,'=>',byStyle[s].map(n=>n.id+':'+n.name).join(' | '));\n\"",
 "description": "List aiStyle 59+ NPC groups"
}
```


---

## 👤 User(sidechain) · 2026-08-11T18:18:04.930Z

**📎 ToolResult**

```
59: 1 => 328:NPC_328
60: 1 => 345:Ice Queen
61: 1 => 346:Santa-NK1
62: 1 => 347:Elf Copter
63: 1 => 352:Flocko
64: 4 => 355:Firefly | 358:Lightning Bug | 654:Lavafly | 677:Faeling
65: 4 => 356:Butterfly | 444:Gold Butterfly | 653:Hell Butterfly | 661:Prismatic Lacewing
66: 8 => 357:Worm | 374:Truffle Worm | 448:Gold Worm | 484:Enchanted Nightcrawler | 485:Grubby | 486:Sluggy | 487:Buggy | 606:Maggot
67: 3 => 359:Snail | 360:Glowing Snail | 655:Magma Snail
68: 4 => 363:NPC_363 | 365:NPC_365 | 603:NPC_603 | 609:NPC_609
69: 1 => 370:Duke Fishron
70: 1 => 371:NPC_371
71: 2 => 372:Sharkron | 373:NPC_373
72: 1 => 384:NPC_384
73: 1 => 387:Tesla Turret
74: 2 => 388:Martian Drone | 418:Corite
75: 6 => 390:Scutlix Gunner | 392:NPC_392 | 393:NPC_393 | 394:NPC_394 | 416:Drakomire Rider | 492:NPC_492
76: 1 => 395:Martian Saucer
77: 1 => 398:Moon Lord's Core
78: 1 => 397:NPC_397
79: 1 => 396:NPC_396
80: 1 => 399:Martian Probe
81: 1 => 400:NPC_400
82: 1 => 401:NPC_401
83: 2 => 437:NPC_437 | 438:Lunatic Devotee
84: 2 => 439:Lunatic Cultist | 440:NPC_440
85: 3 => 405:Star Cell | 421:Brain Suckler | 467:Deadly Sphere
86: 2 => 472:Shadowflame Apparition | 521:Ancient Vision
87: 4 => 473:Corrupt Mimic | 474:Crimson Mimic | 475:Hallowed Mimic | 476:Jungle Mimic
88: 1 => 477:Mothron
89: 1 => 478:NPC_478
90: 1 => 479:Baby Mothron
91: 1 => 483:Granite Elemental
92: 1 => 488:NPC_488
93: 1 => 491:Flying Dutchman
94: 4 => 422:Vortex Pillar | 493:Stardust Pillar | 507:Nebula Pillar | 517:Solar Pillar
95: 1 => 406:Mini Star Cell
96: 2 => 407:Flow Invader | 408:Small Flow Invader
97: 1 => 420:Nebula Floater
99: 1 => 519:NPC_519
100: 1 => 522:NPC_522
101: 1 => 523:NPC_523
102: 1 => 541:Sand Elemental
103: 4 => 542:Sand Shark | 543:Bone Biter | 544:Flesh Reaver | 545:Crystal Thresher
104: 1 => 547:NPC_547
105: 1 => 548:NPC_548
106: 1 => 549:NPC_549
107: 19 => 552:NPC_552 | 553:NPC_553 | 554:Etherian Goblin | 555:NPC_555 | 556:NPC_556 | 557:Etherian Goblin Bomber | 561:NPC_561 | 562:NPC_562 | 563:Etherian Javelin Thrower | 566:NPC_566 | 567:Old One's Skeleton | 568:NPC_568 | 569:Wither Beast | 570:NPC_570 | 571:Drakin | 572:NPC_572 | 573:Kobold | 576:NPC_576 | 577:Ogre
108: 5 => 558:NPC_558 | 559:NPC_559 | 560:Etherian Wyvern | 574:NPC_574 | 575:Kobold Glider
109: 2 => 564:NPC_564 | 565:Dark Mage
110: 1 => 551:Betsy
111: 1 => 578:Etherian Lightning Bug
112: 3 => 583:Pink Fairy | 584:Green Fairy | 585:Blue Fairy
113: 1 => 594:Windy Balloon
114: 7 => 595:NPC_595 | 596:NPC_596 | 597:NPC_597 | 598:NPC_598 | 599:Dragonfly | 600:NPC_600 | 601:Gold Dragonfly
115: 3 => 604:Ladybug | 605:Gold Ladybug | 669:Stinkbug
116: 2 => 612:Water Strider | 613:Gold Water Strider
118: 2 => 626:Seahorse | 627:Gold Seahorse
119: 1 => 628:Angry Dandelion
120: 1 => 636:Empress of Light
121: 1 => 657:Queen Slime

```


---

## 🤖 Assistant · 2026-08-11T18:18:07.232Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let's find the case set in Enemy.ts. I need the dispatch table region (lines 379-519) plus critter region (2555-2565). Let me extract case numbers from the dispatch switch. Let me read lines 370-560 of Enemy.ts.
```

</details>


---

## 🤖 Assistant · 2026-08-11T18:18:07.402Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "offset": 360,
 "limit": 175
}
```


---

## 👤 User(sidechain) · 2026-08-11T18:18:07.412Z

**📎 ToolResult**

```
360	    this.walkCycleT += Math.abs(this.vx); // 原版 zombie/fighter 行走帧按 |vx| 累加（L77072/L70216）
361	
362	    // EoW 族出生渐显（每 tick alpha-1;原版 AI_006）——静态半透明不受影响
363	    if (this.alphaFade) {
364	      this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
365	      if (this.spawnAlpha === 0) this.alphaFade = false;
366	    }
367	
368	    const player = (game as unknown as { player: Player }).player;
369	    const hasPlayer = !!player && !player.dead;
370	
371	    // ---- 原版数据驱动路径：按 aiStyle 分发到已移植的 AI 家族（分发后落入共享尾段） ----
372	    // 蠕虫身体段（wormFollow 非空）无 AI：位置由头部 wormAI 沿链驱动，但仍走共享尾段（接触伤害等）
373	    // 小动物（critter）优先走被动游荡，绝不落入 default 的追击 fallback
374	    if (this.vanilla && !this.wormFollow && this.vanilla.critter) {
375	      this.critterWanderAI(game, hasPlayer ? player : null);
376	    } else if (this.vanilla && !this.wormFollow) {
377	      const p = hasPlayer ? player : null;
378	      switch (this.vanilla.aiStyle) {
379	        case 92: this.dummyAI(game); break;                            // AI_092 训练假人（NPC 488）
380	        case 1: this.slimeAI(game, p); break;                          // AI_001 史莱姆
381	        case 2: this.floatEyeAI(game, p); break;                        // AI_002 飘浮眼（原版核）
382	        case 3:
383	          // AI_003 拜月教弓手 379/380 仪式待机（NPC.cs:56575-56601,ai[3]<0 静立面碑零伤；
384	          // 碑置 ai[3]=0 后激活复位 :56602-56609,回战士核）——bossAI_lunar_misc
385	          if ((this.vanillaId === 379 || this.vanillaId === 380) && this.ai3 < 0) {
386	            cultistArcherStandbyAI(this, game);
387	            break;
388	          }
389	          if (this.vanillaId === 379 || this.vanillaId === 380) cultistArcherWake(this);
390	          this.fighterAI(game, p);
391	          // AI_003 火星尾段（bossAI_martian.ts）：军官 383 带盾无敌/补盾、工程师 386 放炮塔
392	          if (this.vanillaId === 383 || this.vanillaId === 386) martianFighterExtras(this, game, p);
393	          break;                                                        // AI_003 战士族（原版通用核）
394	        // EoC 传参例外:玩家死亡也要传原对象(cs:19931 dead 判定走逃离分支,
395	        // 冲刺计时合法冻结;传 null 会让 aiT 照走、状态机停摆 → 首冲时长翻倍)
396	        case 4: this.eocAI(game, (game as unknown as { player: Player }).player ?? null); break; // AI_004 克苏鲁之眼（NPC.cs:19909）
397	        case 5: this.swarmerAI(game, p); break;                         // AI_005 噬魂怪族（原版蜂群核）
398	        case 6: this.wormAI(game, p); break;                           // AI_006 蠕虫族（头）
399	        case 8: this.casterAI(game, p); break;                          // AI_008 法师族（传送+弹幕）
400	        case 10: this.cursedSkullAI(game, p); break;                     // AI_010 诅咒头骨（地牢飞行族）
401	        case 11:
402	          // 68 守卫走专用分支（bossAI.skeletronBossAI 注释"守卫分支已在 skeletronHeadAI"
403	          // 即此拆分：守卫恒速追击与骷髅王战斗状态机互不混用）
404	          if (this.vanillaId === 68) this.dungeonGuardianAI(game, p);
405	          else skeletronBossAI(this, game, p);
406	          break;                                                         // AI_011 骷髅王头战斗核/地牢守卫
407	        case 12: skeletronHandAI(this, game, p); break;                    // AI_012 骷髅王手(锚定头)
408	        case 20: this.blazingWheelAI(); break;                           // AI_020 火轮（地牢陷阱）
409	        case 21: this.spikeBallAI(game); break;                          // AI_021 刺球（地牢陷阱）
410	        case 14: this.batAI(game, p); break;                            // AI_014 蝙蝠/飞行族（1.4.5.6 原版核）
411	        case 16: this.swimAI(game, p); break;                           // AI_016 游泳族（鲨鱼/食人鱼）
412	        case 18: this.jellyfishAI(game, p); break;                      // AI_018 水母族（脉冲游动）
413	        case 22: this.ghostAI(game, p); break;                          // AI_022 幽灵族（穿墙缓速）
414	        case 13: this.plantAI(game, p); break;                          // AI_013 植物/攀爬者族（锚点伸展）
415	        case 15: kingSlimeAI(this, game, p); break;                       // AI_015 史莱姆王(大跳+小史莱姆)
416	        case 54: brainOfCthulhuAI(this, game, p); break;                  // AI_054 克脑(爬行者环→瞬移冲刺)
417	        case 55: creeperAI(this, game, p); break;                         // AI_055 爬行者(环绕漂移)
418	        case 30: twinsAI(this, game, p, false); break;                    // AI_030 雷神之眼 125(悬浮/连冲/变身/激光)
419	        case 31: twinsAI(this, game, p, true); break;                     // AI_031 魔神之眼 126(诅咒焰/火焰喷射)
420	        case 32: skeletronPrimeAI(this, game, p); break;                  // AI_032 机械骷髅王头 127(4 部件/旋冲/白天狂暴)
421	        case 33: case 34: case 35: case 36: primePartAI(this, game, p); break; // AI_033-036 Prime 部件(锯/激光/钳/炮)
422	        case 37: destroyerAI(this, game, p); break;                       // AI_037 毁灭者 134(80 段链穿地/探针激光)
423	        case 27: wallOfFleshAI(this, game, (game as unknown as { player: Player }).player ?? null); break; // AI_027 血肉墙(空腔扫描/速度血量档/Leech 轮)
424	        case 28: wofEyeAI(this, game, p); break;                          // AI_028 血肉墙之眼(钉墙吸附/激光连射 83)
425	        case 29: hungryAI(this, game, p); break;                          // AI_029 饥饿者(挂墙环绕→受击脱落扑咬)
426	        case 84: lunaticCultistAI(this, game, p); break;                  // AI_084 拜月教邪教徒(瞬移+四系弹幕轮换)
427	        // ---- 月系批（bossAI_lunar_misc.ts）----
428	        case 81: moonLordFreeEyeAI(this, game, p); break;                // AI_081 月总游离眼 400（cs:38224 十槽攻击表+死光）
429	        case 82: moonLeechAI(this, game, p); break;                       // AI_082 月总水蛭块 401（cs:38668 90t 插值吸血回灌）
430	        case 83:                                                            // AI_083 神秘石碑 437/忠实信徒 438（cs:38793）
431	          if (this.vanillaId === 437) cultistTabletAI(this, game, p);
432	          else lunaticDevoteeAI(this, game, p);
433	          break;
434	        case 86: phantomAI(this, game, p); break;                          // AI_086 暗焰幻影 472/远古幻影 521（cs:39261 穿墙横掠循环）
435	        case 87: bigMimicAI(this, game, p); break;                         // AI_087 珍稀四宝箱怪 473-476（cs:39520 跳扑+蓄能/俯冲/三连扑）
436	        case 88: mothronAI(this, game, p); break;                          // AI_088 飞蛾魔 477（cs:39876 日食限定轮换+产卵）
437	        case 89: mothronEggAI(this, game, p); break;                       // AI_089 蛾卵 478（cs:40407 900t→Transform 479）
438	        case 90: babyMothronAI(this, game, p); break;                      // AI_090 幼蛾 479（cs:40450 日食贴脸冲撞）
439	        case 91: graniteElementalAI(this, game, p); break;                 // AI_091 花岗岩元素 483（cs:40686 五态寻路）
440	        case 120: empressOfLightAI(this, game, p); break;                 // AI_120 光之女皇(连段选招/半血变身)
441	        case 121: queenSlimeAI(this, game, p); break;                     // AI_121 史莱姆皇后(走路四连跳→飞行二阶段)
442	        case 100: ancientLightAI(this, game, p); break;                  // AI_100 远古之光 522(直飞投射物型)
443	        case 101: ancientDoomAI(this, game, p); break;                  // AI_101 远古末日 523(锚邪教徒蓄能自爆)
444	        case 43: queenBeeAI(this, game, p); break;                        // AI_043 蜂后(悬浮俯冲/蜜蜂机枪/毒刺)
445	        case 50: planteraHookAI(this, game, p); break;                    // AI_050 真菌孢子 261/孢子 265
446	        case 51: planteraAI(this, game, p); break;                        // AI_051 世纪之花(钩蔓牵引→二阶段)
447	        case 52: planteraTentacleAI(this, game, p); break;                // AI_052 钩蔓 263(抓墙换锚收线)
448	        case 53: planteraTentacle2AI(this, game, p); break;               // AI_053 触须 264(二阶段环绕)
449	        case 69: dukeFishronAI(this, game, p); break;                     // AI_069 猪鲨(冲撞/泡泡/龙卷,半血变身)
450	        case 70: dukeBubbleAI(this, game, p); break;                      // AI_070 爆裂泡泡 371
451	        case 71: sharkronAI(this, game, p); break;                        // AI_071 鲨鱼龙 372/373(龙卷出鲨,升空蓄力→扑咬)
452	        case 77: moonLordCoreAI(this, game, p); break;                    // AI_077 月总核心 398(双手死前无敌)
453	        case 78: moonLordHandAI(this, game, p); break;                    // AI_078 月总手 397(攻表/睁眼可击)
454	        case 79: moonLordHeadAI(this, game, p); break;                    // AI_079 月总头 396(死亡之光/吸血)
455	        case 45: golemAI(this, game, p); break;                        // AI_045 石巨人本体 245(蓄力跳/挂头无敌)
456	        case 46: golemHeadAI(this, game, p); break;                      // AI_046 挂载头 246(锚本体/火焰弹眼激光;249 自由态)
457	        case 47: golemFistAI(this, game, p); break;                      // AI_047 石巨人拳 247/248(肩锚冲拳)
458	        case 40: this.wallCreeperAI(game, p); break;                      // AI_040 爬墙蜘蛛族（贴背景墙爬行+形态互转）
459	        case 42: this.lostGirlAI(game, p); break;                         // AI_042 失落女孩（伪装静止→Nymph 变身 cs:30281-30310）
460	        case 0: this.boundNPCAI(game, p); break;                          // AI_000 被缚NPC（cs:19774 站立/水上漂流；Enemy 侧防御，常规走 TownNPC.bound）
461	        case 17: this.vultureAI(game, p); break;                          // AI_017 秃鹫（cs:24079 栖息→200px盒/受击起飞，单向不回落）
462	        case 19: this.antlionAI(game, p); break;                          // AI_019 蚁狮（cs:24465 扎沙不动+沙球；传送带特例略）
463	        case 23: this.flyingWeaponAI(game, p); break;                     // AI_023 飞行武器（cs:25316 冲/漂100/转120 循环，受击回蓄转）
464	        case 25: this.mimicAI(game, p); break;                            // AI_025 宝箱怪（cs:25621 伪装200px盒→小小大跳循环）
465	        case 39: this.tortoiseAI(game, p); break;                         // AI_039 陆龟族（cs:29257 待机蓄力→蓄势→旋冲→恢复）
466	        case 41: this.herplingAI(game, p); break;                         // AI_041 赫柏林/德普林（cs:30017 低跳连扑；378 炸弹自爆略）
467	        case 44: this.flyingSwarmerAI(game, p); break;                    // AI_044 飞鱼/蚁狮蜂（cs:30999 分轴限速追+失视逃逸）
468	        case 56: this.dungeonSpiritAI(game, p); break;                    // AI_056 地牢之魂（cs:32915 穿墙0.99惯性追踪）
469	        case 26: this.chargerAI(game, p); break;                        // AI_026 独角兽/冲锋族（原版核）
470	        case 107: this.chargerAI(game, p, 1); break;                    // AI_107 ImprovedWalkers（0.07/±1.0 walker 档，NPC.145.cs:43153 引擎核同构）
471	        case 94: this.towerAI(game, p); break;                          // AI_094 星璇四塔（NPC.cs:41029-41443，核心 1:1）
472	        // ---- 星璇塔四组专属怪 AI 一期近似（docs/event-lunar-pillars.md §4）----
473	        // 74 穿心者（悬浮俯冲）→ AI_002 飘浮眼核；75 日耀骑手 → AI_003 战士核；
474	        // 85 星细胞/星云头蟹、95 小星细胞、96 水流入侵者、99 日耀耀斑（漂浮追击族）→ AI_005 蜂群核；
475	        // 97 星云悬浮脑（瞬移+弹幕）→ AI_008 法师核。二期按各自 AI_0XX 1:1 补齐
476	        // （74/75 已由火星批 bossAI_martian.ts 1:1 落位：388 无人机/418 Corite、
477	        //   390 骑手/392-394 飞碟部件/416 日耀骑手——见下方火星族分发）
478	        case 85: case 95: case 96: case 99: this.swarmerAI(game, p); break;
479	        case 97: this.casterAI(game, p); break;
480	        // ---- 月事件（南瓜月/霜月）Boss 族 1:1（bossAI_moon_events.ts）----
481	        case 57: mourningWoodAI(this, game, p); break;                  // AI_057 悲木 325/常世吼 344（cs:32937 悬浮树怪+分阶段弹幕）
482	        case 58: pumpkingAI(this, game, p); break;                       // AI_058 南瓜王 327（cs:33246 悬浮/俯冲+生双刃）
483	        case 59: pumpkingBladeAI(this, game, p); break;                   // AI_059 南瓜王之刃 328（cs:33405 锚主环绕/俯冲/横扫）
484	        case 60: iceQueenAI(this, game, p); break;                        // AI_060 冰雪女王 345（cs:33588 滑翔/落冰/旋射三态）
485	        case 61: santaNK1AI(this, game, p); break;                        // AI_061 圣诞坦克 346（cs:33902 悬浮+链炮/火箭/礼盒）
486	        case 62: elfCopterAI(this, game, p); break;                       // AI_062 玩具直升机 347（cs:34155 近距悬停点射）
487	        case 63: flockoAI(this, game, p); break;                          // AI_063 弗洛科 352（cs:34208 追踪+旋冲）
488	        case 38: snowmanAI(this, game, p); break;                         // AI_038 雪人三兄弟 143/144/145（cs:29115 跳扑/停顿/雪球）
489	        case 9: bouncingBallAI(this, game, p); break;                     // AI_009 弹跳球族 25/30/33/112/516/665/666（cs:21349 直飞球）
490	        // ---- 火星疯狂族 1:1（bossAI_martian.ts）----
491	        case 80: martianProbeAI(this, game, p); break;                    // AI_080 火星探测器 399（cs:38129 逃逸→StartInvasion(4)）
492	        case 76: martianSaucerAI(this, game, p); break;                   // AI_076 火星飞碟核心 395（cs:36322 600t 六窗口+部件生成）
493	        case 72: bubbleShieldAI(this, game, p); break;                    // AI_072 泡泡盾 384（cs:35318 锚军官 383）
494	        case 73: teslaTurretAI(this, game, p); break;                     // AI_073 特斯拉炮塔 387（cs:35340 部署渐显+180t 电击）
495	        case 74:                                                          // AI_074 火星无人机 388/日耀 Corite 418（cs:35452 悬浮→扑咬→自爆）
496	          if (this.vanillaId === 388 || this.vanillaId === 418) martianDroneAI(this, game, p);
497	          else this.floatEyeAI(game, p);                                  // 其余（一期近似档保留）
498	          break;
499	        case 75:                                                          // AI_075 飞碟部件 392/393/394 + 骑手 390（cs:35745 锚主体+攻击窗）
500	          if (this.vanillaId === 390 || this.vanillaId === 392
501	            || this.vanillaId === 393 || this.vanillaId === 394
502	            || this.vanillaId === 416 || this.vanillaId === 492) martianSaucerPartAI(this, game, p);
503	          else this.fighterAI(game, p);                                   // 其余（一期近似档保留）
504	          break;
505	        case 48: golemHeadAI(this, game, p); break;                       // AI_048 自由石巨人头 249（cs:31500,golemHeadAI 已含自由态分支）
506	        case 49: angryNimbusAI(this, game, p); break;                     // AI_049 愤怒云 250（cs:31742 悬顶淋雨 264）
507	        // ---- DD2/旧日军团 + 沙漠族（bossAI_dd2.ts）----
508	        case 93: flyingDutchmanAI(this, game, p); break;                  // AI_093 荷兰飞盗船 491（cs:40918 四炮部件+海盗跳舱+贴地巡航）
509	        case 102: sandElementalAI(this, game, p); break;                  // AI_102 沙尘精 541（cs:42224 walker 核+沙暴标记 658）
510	        case 103: sandSharkAI(this, game, p); break;                      // AI_103 沙鲨族 542-545（cs:42621 沙中巡游+跃沙扑咬,沙族豁免碰撞）
511	        case 104: dd2AttackerTestAI(this, game); break;                   // AI_104 DD2AttackerTest 547（cs:42807 出生即消）
512	        case 105: eterniaCrystalAI(this, game, p); break;                 // AI_105 永恒水晶 548（cs:42810 180t 双端放门+胜负演出）
513	        case 106: lanePortalAI(this, game, p); break;                     // AI_106 神秘传送门 549（cs:43063 出怪门节拍,事件依赖 DD2_EVENT_HOOKS）
514	        case 108: divingFlyerAI(this, game, p); break;                    // AI_108 飞龙 558-560/小妖魔滑翔怪 574-575（cs:65959 俯冲五态+自爆）
515	        case 109: darkMageAI(this, game, p); break;                       // AI_109 黑暗魔法师 564/565（cs:66392 walker+三连招 675/674/673）
516	        case 110: betsyAI(this, game, p); break;                          // AI_110 双足翼龙 551（cs:62266 八槽攻表+rotation 收敛）
517	        case 111: dd2LightningBugAI(this, game, p); break;                // AI_111 埃特尼亚荧光虫 578（cs:66799 悬停蓄电 682 电弧）
518	        default: this.zombieAI(game, p); break;                        // 其余家族待逐个移植
519	      }
520	    } else switch (this.key) {
521	      case 'slime_green':
522	      case 'slime_blue': this.slimeAI(game, hasPlayer ? player : null); break;
523	      case 'zombie': this.zombieAI(game, hasPlayer ? player : null); break;
524	      case 'demon_eye':
525	      case 'cave_bat': this.flyAI(game, hasPlayer ? player : null, 0.09); break;
526	      case 'servant_of_cthulhu': this.flyAI(game, hasPlayer ? player : null, 0.22); break;
527	      case 'eye_of_cthulhu': this.eocAI(game, player ?? null); break;
528	    }
529	
530	    // 入水溅落声（与主角一致）：音量随与主角距离衰减，Boss 更响
531	    const eli = game.world.store.liquid[game.world.store.idx(
532	      Math.floor(this.cx / TILE), Math.floor(this.cy / TILE),
533	    )];
534	    const wasWater = this.inWater;

```


---

## 🤖 Assistant · 2026-08-11T18:33:09.217Z · <synthetic>

```
API Error: Stream idle timeout - no chunks received
```


---

## 👤 User(sidechain) · 2026-08-11T18:33:09.218Z

```
[Request interrupted by user]
```
