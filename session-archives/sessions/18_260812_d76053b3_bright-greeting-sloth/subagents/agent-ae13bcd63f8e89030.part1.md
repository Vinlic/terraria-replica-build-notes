# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T03:05:55.902Z

```
你在泰拉瑞亚 1.4.5.6 复刻仓库 ~/Project/GLM/SandboxWorld 做敌怪 AI **全量 1:1 行为审计**(只读!禁止编辑任何文件、禁止跑游戏)。

标杆:反编译源 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs(grep "aiStyle == N" 定位入口;独立函数 grep "private void AI_0")。
我方:game/src/entities/Enemy.ts。

★范围分工:另有并行代理在专查"玩家死亡(null player)退化行为"与"追击门(wet/视线)"两类——你**不查**这两类(撞到一句话备注),专注其余维度:状态机/移动物理(加速度、速度帽、环绕摆动、悬浮钉定)/计时器/RNG/特殊技能(冲刺链、发射、传送、变形)/wet 浮力族表。

## 你负责的族

- 蜂群 AI_005(Eater of Souls 6/Crimera 173:8px 网格量化制导、ai[0] 环绕摆动 ±200)
- chargerAI(黄蜂族 42/231-235 冲刺链;620 地精鲨 wet 游泳档 cs:64118-64230)
- jellyfishAI(AI_018 水母:潜伏态/追击脉冲/漂移振荡/离水坠落)
- 恶魔/小鬼族(AI_004 恶魔 66/火小鬼 24?核 aiStyle 归属;水母外的 aiStyle 4/14 专属分支)
- 哈比 48/其他 aiStyle 14 蝙蝠族专属分支(158 吸血蝙蝠/660 巨狐蝠——batAI 主体已修勿重报,查这两专属分支的参数)
- 骷髅王手/克眼之外的眼睛族专属(若 Enemy.ts 有 eocAI/eyeAI 家族)
- 其他 Enemy.ts aiStyle switch 里未列但属飞行/水生的 case(自己 grep `case \d+: this\.\w+AI` 枚举补全,归你管的报出来)

## 方法

逐族:①读我方实现;②读原版段;③列 CONFIRMED 差(两边行号+关键代码一行);④分级 严重/中/低。已修勿重报:floatEyeAI/batAI 主体/swimAI flag22。已知正确带行号的大块一句话带过。

## 输出格式(最终报告)

按族分节;每条:我方行号/原版行号/症状/最小修复建议/置信度;结尾"总偏差数+Top3 必修"。存疑单列。控制密度。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T03:05:55.905Z

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

## 🤖 Assistant · 2026-08-19T03:06:03.846Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me understand the task. I'm auditing enemy AI implementations in a Terraria 1.4.5.6 clone. I need to compare our implementation (game/src/entities/Enemy.ts) against the decompiled vanilla source (Terarria1456/Terraria/NPC.cs).

My assigned families:
1. AI_005 (蜂群): Eater of Souls 6 / Crimera 173 — 8px grid quantization guidance, ai[0] hover swing ±200
2. chargerAI: hornet family 42/231-235 dash chain; 620 goblin shark wet swim tier cs:64118-64230
3. jellyfishAI (AI_018 jellyfish): lurk/chase pulse/drift oscillation/out-of-water fall
4. Demon/imp family (AI_004 demon 66 / fire imp; aiStyle 4/14 exclusive branches)
5. Harpy 48 / other aiStyle 14 bat family exclusive branches (158 vampire bat / 660 giant fox bat — batAI main body already fixed, don't re-report; check these two exclusive branch parameters)
6. Skeleton hand / eye family exclusive (if Enemy.ts has eocAI/eyeAI family)
7. Other unlisted flying/aquatic cases in Enemy.ts aiStyle switch

Excluded (another agent handles): player death (null player) degenerate behavior, chase gates (wet/line of sight).

Read-only audit. No file edits, no running the game.

Method: for each family: ① read our implementation; ② read vanilla section; ③ list CONFIRMED diffs (both line numbers + one key code line); ④ grade severity.

Let me start by exploring the files.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:06:04.314Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check line counts of both files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:04.416Z

**📎 ToolResult**

```
    8009 ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
   96369 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs
  104378 total

```


---

## 🤖 Assistant · 2026-08-19T03:06:04.966Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle == \\|aiStyle==\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -80",
 "description": "List aiStyle dispatch entries in vanilla NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:05.032Z

**📎 ToolResult**

```
6567:			if (isLikeATownNPC && aiStyle == 7 && velocity.Y == 0f)
6579:			if (isLikeATownNPC && aiStyle == 7)
19756:			return aiStyle == 3;
19774:		if (aiStyle == 0)
19894:		if (aiStyle == 1)
19899:		if (aiStyle == 2)
19904:		if (aiStyle == 3)
19909:		if (aiStyle == 4)
20759:		if (aiStyle == 5)
20764:		if (aiStyle == 6)
20769:		if (aiStyle == 7)
20774:		if (aiStyle == 8)
21349:		if (aiStyle == 9)
21553:		if (aiStyle == 10)
21904:		if (aiStyle == 11)
22289:		if (aiStyle == 12)
22604:		if (aiStyle == 13)
22895:		if (aiStyle == 14)
23544:		if (aiStyle == 15)
23549:		if (aiStyle == 16)
24079:		if (aiStyle == 17)
24210:		if (aiStyle == 18)
24465:		if (aiStyle == 19)
24596:		if (aiStyle == 20)
24674:		else if (aiStyle == 21)
24726:		else if (aiStyle == 22)
25316:		else if (aiStyle == 23)
25396:		else if (aiStyle == 24)
25621:		else if (aiStyle == 25)
25714:		else if (aiStyle == 26)
25718:		else if (aiStyle == 27)
26141:		else if (aiStyle == 28)
26299:		else if (aiStyle == 29)
26497:		else if (aiStyle == 30)
27116:		else if (aiStyle == 31)
27736:		else if (aiStyle == 32)
28055:		else if (aiStyle == 33)
28360:		else if (aiStyle == 34)
28640:		else if (aiStyle == 35)
28876:		else if (aiStyle == 36)
29111:		else if (aiStyle == 37)
29115:		else if (aiStyle == 38)
29257:		else if (aiStyle == 39)
29784:		else if (aiStyle == 40)
30017:		else if (aiStyle == 41)
30281:		else if (aiStyle == 42)
30312:		else if (aiStyle == 43)
30999:		else if (aiStyle == 44)
31269:		else if (aiStyle == 45)
31273:		else if (aiStyle == 46)
31496:		else if (aiStyle == 47)
31500:		else if (aiStyle == 48)
31742:		else if (aiStyle == 49)
31807:		else if (aiStyle == 50)
31873:		else if (aiStyle == 51)
31905:				if (Main.npc[num792].active && Main.npc[num792].aiStyle == 52)
32160:							if (Main.npc[num813].active && Main.npc[num813].aiStyle == 52)
32238:		else if (aiStyle == 52)
32406:		else if (aiStyle == 53)
32537:		else if (aiStyle == 54)
32828:		else if (aiStyle == 55)
32915:		else if (aiStyle == 56)
32937:		else if (aiStyle == 57)
33246:		else if (aiStyle == 58)
33405:		else if (aiStyle == 59)
33588:		else if (aiStyle == 60)
33902:		else if (aiStyle == 61)
34155:		else if (aiStyle == 62)
34208:		else if (aiStyle == 63)
34256:		else if (aiStyle == 64)
34486:		else if (aiStyle == 65)
34490:		else if (aiStyle == 66)
34586:		else if (aiStyle == 67)
34861:		else if (aiStyle == 68)
35118:		else if (aiStyle == 69)
35122:		else if (aiStyle == 70)
35196:		else if (aiStyle == 71)
35318:		else if (aiStyle == 72)
35340:		else if (aiStyle == 73)
35452:		else if (aiStyle == 74)

```


---

## 🤖 Assistant · 2026-08-19T03:06:13.965Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by understanding the structure of our Enemy.ts and the vanilla NPC.cs dispatch. First, let me look at our Enemy.ts aiStyle switch and the AI function list.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:06:14.848Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case [0-9]*: this\\.\\w*AI\\|private \\w*AI(\\|\\w*AI(\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -120",
 "description": "List AI function dispatch in our Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:14.935Z

**📎 ToolResult**

```
327:  private wormAI(game: GameHooks, player: Player | null) {
330:      this.eowAI(game, player);
484:  private eowAI(game: GameHooks, _player: Player | null): void {
1174:      this.critterWanderAI(game, hasPlayer ? player : null);
1178:        case 92: this.dummyAI(game); break;                            // AI_092 训练假人（NPC 488）
1179:        case 1: this.slimeAI(game, p); break;                          // AI_001 史莱姆
1180:        case 2: this.floatEyeAI(game, p); break;                        // AI_002 飘浮眼（原版核）
1185:            cultistArcherStandbyAI(this, game);
1189:          this.fighterAI(game, p);
1200:        case 4: this.eocAI(game, (game as unknown as { player: Player }).player ?? null); break; // AI_004 克苏鲁之眼（NPC.cs:19909）
1201:        case 5: this.swarmerAI(game, p); break;                         // AI_005 噬魂怪族（原版蜂群核）
1205:          if (this.vanillaId === 412) crawltipedeAI(this, game, p);
1206:          else this.wormAI(game, p);
1208:        case 8: this.casterAI(game, p); break;                          // AI_008 法师族（传送+弹幕）
1209:        case 10: this.cursedSkullAI(game, p); break;                     // AI_010 诅咒头骨（地牢飞行族）
1213:          if (this.vanillaId === 68) this.dungeonGuardianAI(game, p);
1214:          else skeletronBossAI(this, game, p);
1216:        case 12: skeletronHandAI(this, game, p); break;                    // AI_012 骷髅王手(锚定头)
1217:        case 20: this.blazingWheelAI(); break;                           // AI_020 火轮（地牢陷阱）
1218:        case 21: this.spikeBallAI(game); break;                          // AI_021 刺球（地牢陷阱）
1219:        case 14: this.batAI(game, p); break;                            // AI_014 蝙蝠/飞行族（1.4.5.6 原版核）
1220:        case 16: this.swimAI(game, p); break;                           // AI_016 游泳族（鲨鱼/食人鱼）
1221:        case 18: this.jellyfishAI(game, p); break;                      // AI_018 水母族（脉冲游动）
1222:        case 22: this.ghostAI(game, p); break;                          // AI_022 幽灵族（穿墙缓速）
1223:        case 13: this.plantAI(game, p); break;                          // AI_013 植物/攀爬者族（锚点伸展）
1224:        case 15: kingSlimeAI(this, game, p); break;                       // AI_015 史莱姆王(大跳+小史莱姆)
1225:        case 54: brainOfCthulhuAI(this, game, p); break;                  // AI_054 克脑(爬行者环→瞬移冲刺)
1226:        case 55: creeperAI(this, game, p); break;                         // AI_055 爬行者(环绕漂移)
1227:        case 30: twinsAI(this, game, p, false); break;                    // AI_030 雷神之眼 125(悬浮/连冲/变身/激光)
1228:        case 31: twinsAI(this, game, p, true); break;                     // AI_031 魔神之眼 126(诅咒焰/火焰喷射)
1229:        case 32: skeletronPrimeAI(this, game, p); break;                  // AI_032 机械骷髅王头 127(4 部件/旋冲/白天狂暴)
1230:        case 33: case 34: case 35: case 36: primePartAI(this, game, p); break; // AI_033-036 Prime 部件(锯/激光/钳/炮)
1231:        case 37: destroyerAI(this, game, p); break;                       // AI_037 毁灭者 134(80 段链穿地/探针激光)
1232:        case 27: wallOfFleshAI(this, game, (game as unknown as { player: Player }).player ?? null); break; // AI_027 血肉墙(空腔扫描/速度血量档/Leech 轮)
1233:        case 28: wofEyeAI(this, game, p); break;                          // AI_028 血肉墙之眼(钉墙吸附/激光连射 83)
1234:        case 29: hungryAI(this, game, p); break;                          // AI_029 饥饿者(挂墙环绕→受击脱落扑咬)
1235:        case 84: lunaticCultistAI(this, game, p); break;                  // AI_084 拜月教邪教徒(瞬移+四系弹幕轮换)
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
1249:        case 120: empressOfLightAI(this, game, p); break;                 // AI_120 光之女皇(连段选招/半血变身)
1250:        case 121: queenSlimeAI(this, game, p); break;                     // AI_121 史莱姆皇后(走路四连跳→飞行二阶段)
1251:        case 122: this.pirateGhostAI(game, p); break;                     // AI_122 海盗幽灵 662（穿墙追击+失标渐隐自灭）
1252:        case 123: deerclopsAI(this, game, p); break;                      // AI_123 鹿角怪(尖刺/碎石/影手/回家)
1253:        case 100: ancientLightAI(this, game, p); break;                  // AI_100 远古之光 522(直飞投射物型)
1254:        case 101: ancientDoomAI(this, game, p); break;                  // AI_101 远古末日 523(锚邪教徒蓄能自爆)
1255:        case 43: queenBeeAI(this, game, p); break;                        // AI_043 蜂后(悬浮俯冲/蜜蜂机枪/毒刺)
1256:        case 50: planteraHookAI(this, game, p); break;                    // AI_050 真菌孢子 261/孢子 265
1257:        case 51: planteraAI(this, game, p); break;                        // AI_051 世纪之花(钩蔓牵引→二阶段)
1258:        case 52: planteraTentacleAI(this, game, p); break;                // AI_052 钩蔓 263(抓墙换锚收线)
1259:        case 53: planteraTentacle2AI(this, game, p); break;               // AI_053 触须 264(二阶段环绕)
1260:        case 69: dukeFishronAI(this, game, p); break;                     // AI_069 猪鲨(冲撞/泡泡/龙卷,半血变身)
1261:        case 70: dukeBubbleAI(this, game, p); break;                      // AI_070 爆裂泡泡 371
1262:        case 71: sharkronAI(this, game, p); break;                        // AI_071 鲨鱼龙 372/373(龙卷出鲨,升空蓄力→扑咬)
1263:        case 77: moonLordCoreAI(this, game, p); break;                    // AI_077 月总核心 398(双手死前无敌)
1264:        case 78: moonLordHandAI(this, game, p); break;                    // AI_078 月总手 397(攻表/睁眼可击)
1265:        case 79: moonLordHeadAI(this, game, p); break;                    // AI_079 月总头 396(死亡之光/吸血)
1266:        case 45: golemAI(this, game, p); break;                        // AI_045 石巨人本体 245(蓄力跳/挂头无敌)
1267:        case 46: golemHeadAI(this, game, p); break;                      // AI_046 挂载头 246(锚本体/火焰弹眼激光;249 自由态)
1268:        case 47: golemFistAI(this, game, p); break;                      // AI_047 石巨人拳 247/248(肩锚冲拳)
1269:        case 40: this.wallCreeperAI(game, p); break;                      // AI_040 爬墙蜘蛛族（贴背景墙爬行+形态互转）
1270:        case 42: this.lostGirlAI(game, p); break;                         // AI_042 失落女孩（伪装静止→Nymph 变身 cs:30281-30310）
1271:        case 0: this.boundNPCAI(game, p); break;                          // AI_000 被缚NPC（cs:19774 站立/水上漂流；Enemy 侧防御，常规走 TownNPC.bound）
1272:        case 17: this.vultureAI(game, p); break;                          // AI_017 秃鹫（cs:24079 栖息→200px盒/受击起飞，单向不回落）
1273:        case 19: this.antlionAI(game, p); break;                          // AI_019 蚁狮（cs:24465 扎沙不动+沙球；传送带特例略）
1274:        case 23: this.flyingWeaponAI(game, p); break;                     // AI_023 飞行武器（cs:25316 冲/漂100/转120 循环，受击回蓄转）
1275:        case 25: this.mimicAI(game, p); break;                            // AI_025 宝箱怪（cs:25621 伪装200px盒→小小大跳循环）
1276:        case 39: this.tortoiseAI(game, p); break;                         // AI_039 陆龟族（cs:29257 待机蓄力→蓄势→旋冲→恢复）
1277:        case 41: this.herplingAI(game, p); break;                         // AI_041 赫柏林/德普林/378 咬齿炸弹（cs:30017 低跳连扑+自爆链）
1278:        case 44: this.flyingSwarmerAI(game, p); break;                    // AI_044 飞鱼/蚁狮蜂（cs:30999 分轴限速追+失视逃逸）
1279:        case 56: this.dungeonSpiritAI(game, p); break;                    // AI_056 地牢之魂（cs:32915 穿墙0.99惯性追踪）
1280:        case 26: this.chargerAI(game, p); break;                        // AI_026 独角兽/冲锋族（原版核）
1283:          else this.chargerAI(game, p, 1);                                 // 620 地精鲨（wet 游泳档,cs:64118-64230 专属分支）
1285:        case 94: this.towerAI(game, p); break;                          // AI_094 星璇四塔（NPC.cs:41029-41443，核心 1:1）
1290:        case 85: starCellAI(this, game, p); break;                    // AI_085 星细胞 405/星云头蟹 421（六态寻路+吸附）
1291:        case 95: smallStarCellAI(this, game, p); break;               // AI_095 小星细胞 406（300t 长大 Transform 405）
1292:        case 96: flowInvaderAI(this, game, p); break;                 // AI_096 水流入侵者 407(/408)（悬顶伺服+甩 539）
1293:        case 97: nebulaFloaterAI(this, game, p); break;               // AI_097 星云悬浮脑 420（瞬移+环绕球 574→弹 576）
1294:        case 99: solarSlimeAI(this, game, p); break;                  // AI_099 日耀黏液 519（坠落→落地 5t 自爆）
1296:        case 57: mourningWoodAI(this, game, p); break;                  // AI_057 悲木 325/常世吼 344（cs:32937 悬浮树怪+分阶段弹幕）
1297:        case 58: pumpkingAI(this, game, p); break;                       // AI_058 南瓜王 327（cs:33246 悬浮/俯冲+生双刃）
1298:        case 59: pumpkingBladeAI(this, game, p); break;                   // AI_059 南瓜王之刃 328（cs:33405 锚主环绕/俯冲/横扫）
1299:        case 60: iceQueenAI(this, game, p); break;                        // AI_060 冰雪女王 345（cs:33588 滑翔/落冰/旋射三态）
1300:        case 61: santaNK1AI(this, game, p); break;                        // AI_061 圣诞坦克 346（cs:33902 悬浮+链炮/火箭/礼盒）
1301:        case 62: elfCopterAI(this, game, p); break;                       // AI_062 玩具直升机 347（cs:34155 近距悬停点射）
1302:        case 63: flockoAI(this, game, p); break;                          // AI_063 弗洛科 352（cs:34208 追踪+旋冲）
1303:        case 38: snowmanAI(this, game, p); break;                         // AI_038 雪人三兄弟 143/144/145（cs:29115 跳扑/停顿/雪球）
1304:        case 9: bouncingBallAI(this, game, p); break;                     // AI_009 弹跳球族 25/30/33/112/516/665/666（cs:21349 直飞球）
1306:        case 80: martianProbeAI(this, game, p); break;                    // AI_080 火星探测器 399（cs:38129 逃逸→StartInvasion(4)）
1307:        case 76: martianSaucerAI(this, game, p); break;                   // AI_076 火星飞碟核心 395（cs:36322 600t 六窗口+部件生成）
1308:        case 72: bubbleShieldAI(this, game, p); break;                    // AI_072 泡泡盾 384（cs:35318 锚军官 383）
1309:        case 73: teslaTurretAI(this, game, p); break;                     // AI_073 特斯拉炮塔 387（cs:35340 部署渐显+180t 电击）
1311:          if (this.vanillaId === 388 || this.vanillaId === 418) martianDroneAI(this, game, p);
1312:          else this.floatEyeAI(game, p);                                  // 其余（一期近似档保留）
1317:            || this.vanillaId === 416 || this.vanillaId === 492) martianSaucerPartAI(this, game, p);
1318:          else this.fighterAI(game, p);                                   // 其余（一期近似档保留）
1320:        case 48: golemHeadAI(this, game, p); break;                       // AI_048 自由石巨人头 249（cs:31500,golemHeadAI 已含自由态分支）
1321:        case 49: angryNimbusAI(this, game, p); break;                     // AI_049 愤怒云 250（cs:31742 悬顶淋雨 264）
1323:        case 93: flyingDutchmanAI(this, game, p); break;                  // AI_093 荷兰飞盗船 491（cs:40918 四炮部件+海盗跳舱+贴地巡航）
1324:        case 102: sandElementalAI(this, game, p); break;                  // AI_102 沙尘精 541（cs:42224 walker 核+沙暴标记 658）
1325:        case 103: sandSharkAI(this, game, p); break;                      // AI_103 沙鲨族 542-545（cs:42621 沙中巡游+跃沙扑咬,沙族豁免碰撞）
1326:        case 104: dd2AttackerTestAI(this, game); break;                   // AI_104 DD2AttackerTest 547（cs:42807 出生即消）
1327:        case 105: eterniaCrystalAI(this, game, p); break;                 // AI_105 永恒水晶 548（cs:42810 180t 双端放门+胜负演出）
1328:        case 106: lanePortalAI(this, game, p); break;                     // AI_106 神秘传送门 549（cs:43063 出怪门节拍,事件依赖 DD2_EVENT_HOOKS）
1329:        case 108: divingFlyerAI(this, game, p); break;                    // AI_108 飞龙 558-560/小妖魔滑翔怪 574-575（cs:65959 俯冲五态+自爆）
1330:        case 109: darkMageAI(this, game, p); break;                       // AI_109 黑暗魔法师 564/565（cs:66392 walker+三连招 675/674/673）
1331:        case 110: betsyAI(this, game, p); break;                          // AI_110 双足翼龙 551（cs:62266 八槽攻表+rotation 收敛）
1332:        case 111: dd2LightningBugAI(this, game, p); break;                // AI_111 埃特尼亚荧光虫 578（cs:66799 悬停蓄电 682 电弧）
1333:        case 113: this.windyBalloonAI(game, p); break;                    // AI_113 风气球 594（cs:48253 挂史莱姆 ai[0]=-999）
1334:        case 125: this.balloonSlimeAI(game, p); break;                    // AI_125 笨笨气球史莱姆 686（cs:44009 漂浮悬停+爆裂解救）
1335:        case 117: this.bloodNautilusAI(game, p); break;                  // AI_117 恐惧鹦鹉螺 618（cs:47488 血月钓鱼 Boss）
1336:        case 119: this.dandelionAI(game, p); break;                      // AI_119 蒲公英 628（cs:43254 下风喷籽；非critter勿只登 critterWanderAI）
1337:        case 126: this.statueMimicAI(game, p); break;                    // AI_126 雕像宝箱怪 690（cs:43760 伪装/唤醒/跳跃穿墙）

```


---

## 🤖 Assistant · 2026-08-19T03:06:15.285Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private void AI_\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "List independent AI_ functions in vanilla NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:15.360Z

**📎 ToolResult**

```
19171:	private void AI_047_GolemFist()
19447:	private void AI_045_Golem()
43239:	private void AI_127_Pal()
43341:	private void AI_127_Pal_GiveRewerd()
43436:	private void AI_015_KingSlime()
43760:	private void AI_126_StatueMimic()
44004:	private void AI_124_ElderSlimeChest()
44009:	private void AI_125_ClumsySlimeBalloon()
44338:	private void AI_123_Deerclops()
44754:	private void AI_123_Deerclops_ShootRubbleUp(ref NPCAimedTarget targetData, ref Point sourceTileCoords, int howMany, int distancedByThisManyTiles, float upBiasPerSpike, int whichOne)
44776:	private void AI_123_Deerclops_MakeSpikesForward(int AISLOT_PhaseCounter, NPCAimedTarget targetData)
44812:	private void AI_123_Deerclops_MakeSpikesBothSides(int AISLOT_PhaseCounter, NPCAimedTarget targetData)
44851:	private void AI_123_Deerclops_FindSpotToSpawnSpike(int howMany, int whichOne, ref int x, ref int y)
44887:	private void AI_123_Deerclops_TryMakingSpike(ref Point sourceTileCoords, int dir, int howMany, int whichOne, int xOffset)
44957:	private void AI_123_Deerclops_Movement(bool haltMovement, bool goHome)
45045:	private void AI_124_DeerclopsLeg()
45142:	private void AI_87_BigMimic_FireStuffCannonBurst()
45152:	private void AI_87_BigMimic_ShootItem(int itemID)
45231:	private void AI_065_Butterflies()
45467:	private void AI_121_QueenSlime_FlyMovement()
45543:	private void AI_121_QueenSlime()
46178:	private void AI_120_HallowBoss_DoMagicEffect(Vector2 spot, int effectType, float progress)
46299:	private void AI_120_HallowBoss()
47304:	private void AI_120_HallowBoss_DashTo(Vector2 targetPosition)
47344:	private void AI_119_Dandelion()
47432:	private void AI_118_Seahorses()
47488:	private void AI_117_BloodNautilus()
47882:	private void AI_116_WaterStriders()
47944:	private void AI_115_LadyBugs()
48080:	private void AI_114_Dragonflies()
48253:	private void AI_113_WindyBalloon()
48453:	private void AI_112_FairyCritter()
49143:	private void AI_069_DukeFishron()
50129:	private void AI_037_Destroyer()
50626:	private void AI_005_EaterOfSouls()
51357:	private void AI_006_Worms()
52673:	private void AI_002_FloatingEye()
53195:	private void AI_007_FindGoodRestingSpot(int myTileX, int myTileY, out int floorX, out int floorY)
53264:	private void AI_007_TryForcingSitting(int homeFloorX, int homeFloorY)
53335:	private void AI_007_TownEntities_UpdateSavedStates()
53366:	private void AI_007_TownEntities()
55982:	private void AI_007_TownEntities_Shimmer_TeleportToLandingSpot()
56063:	private void AI_007_TownEntities_TeleportToHome(int homeFloorX, int homeFloorY)
56093:	private void AI_007_TownEntities_GetWalkPrediction(int myTileX, int homeFloorX, bool canBreathUnderWater, bool currentlyDrowning, int tileX, int tileY, out bool keepwalking, out bool avoidFalling)
56172:	private void AI_007_AttemptToPlayIdleAnimationsForPets(int petIdleChance)
56245:	private void AI_003_Fighters()
60735:	private void AI_001_Slimes()
62266:	private void AI_110_Betsy()
62809:	private void AI_026_Unicorns()
63372:	private void AI_107_ImprovedWalkers()
64921:	private void AI_084_LunaticCultist()
65959:	private void AI_108_DivingFlyer()
66392:	private void AI_109_DarkMage()
66793:	private void AI_111_DD2LightningBug()

```


---

## 🤖 Assistant · 2026-08-19T03:06:18.412Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The dispatch shows many cases are in separate functions (imported from other files). Let me see the full switch in Enemy.ts, including which are in this file vs imported. Let me look at the imports and the rest of the switch.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:06:18.895Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 1160,1360p ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read full aiStyle switch in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:18.954Z

**📎 ToolResult**

```
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

```


---

## 🤖 Assistant · 2026-08-19T03:07:03.808Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me map my assigned families to implementations:

1. **AI_005 swarmerAI** (蜂群 Eater of Souls 6/Crimera 173) — vanilla NPC.cs:50626 `AI_005_EaterOfSouls`, our Enemy.ts `swarmerAI`.
2. **chargerAI** (AI_026 独角兽/冲锋族) — vanilla NPC.cs:62809 `AI_026_Unicorns`. But wait, the task says "chargerAI(黄蜂族 42/231-235 冲刺链...)". Hmm, "黄蜂族 42/231-235" — the NPC types 42 (Unicorn?), 231-235... wait. Let me check: NPC 42 is Unicorn. 231-235? Actually the hornet is NPC 42? No — NPC 42 is "Unicorn"? Let me recall Terraria NPC IDs: 42 = Unicorn? Actually: 42 is Unicorn... Hmm no. Terraria NPC id 42 = "Unicorn"? Let me think. ID list: 41 Snow Flinx? Hmm.

Actually in Terraria: NPC 42 = "Unicorn". No wait — Unicorn is 62? Let me check by grepping. The charger AI in vanilla is AI_026_Unicorns which handles types 42 (Man Eater? no)... Let me just grep.

Actually the task states: "chargerAI(黄蜂族 42/231-235 冲刺链;620 地精鲨 wet 游泳档 cs:64118-64230)". "黄蜂族" = hornet family. Hmm, but charger... Actually NPC 42 = "Hornet"? No... In Terraria, Hornet is NPC 42? Let me verify: Terraria NPC IDs: 40 = Wall Creeper, 41 = ... hmm. Actually I recall: 42 = Hornet? No, 42 = "Unicorn"?? Let me just grep the source.

Actually I remember: NPC 42 is "Man Eater"? No, Man Eater is 41? Hmm. Terraria IDs: 39 Cave Bat? 40 = ... Let me just check.

The chargerAI in our code is case 26 which is AI_026_Unicorns (cs:62809). The types handled by AI_026 in vanilla include Unicorn (62?)... whatever. The task says hornet family 42/231-235. Hornet is NPC 42? No! NPC 42 in Terraria... Let me look: "Hornet" NPC ID = 42? Actually yes I believe Hornet = 42? Hmm, wait: 42 = "Hornet"? The list: 36 Chaos Element? no...

Let me stop guessing and grep.

3. **jellyfishAI** (AI_018 水母) — vanilla NPC.cs:24210 (aiStyle == 18), our jellyfishAI.
4. **恶魔/小鬼族 AI_004** — 恶魔 66 / 火小鬼. But in our code, case 4 goes to eocAI (Eye of Cthulhu). In vanilla, aiStyle 4 is the "Eye of Cthulhu" style but also used by Demon (66)? Hmm — actually in vanilla, NPC 66 Demon has aiStyle 4? Let me check: Demon aiStyle = 4? Hmm. In vanilla Terraria, Demon (66) has aiStyle 4? I recall Demon uses aiStyle 4 with flag special handling (scythe shooting). Voodoo Demon too. Fire Imp (24) has aiStyle 4? Hmm — Fire Imp actually has aiStyle 4? No, Fire Imp has aiStyle... 4? Let me check the vanilla source. Actually Fire Imp is aiStyle 4? I recall Fire Imp uses aiStyle 4 with teleportation... no wait, Fire Imp uses aiStyle 4? Hmm, the Fire Imp (NPC 24) — in vanilla, aiStyle 4 branch at :19909 has "if (npc.type == 24)" segments? Let me grep.

So task item 4: "恶魔/小鬼族(AI_004 恶魔 66/火小鬼 24?核 aiStyle 归属;水母外的 aiStyle 4/14 专属分支)" — I need to determine which aiStyle demon 66 and fire imp 24 use, and check the type-specific branches inside aiStyle 4 (and 14 outside jellyfish) in vanilla vs ours. Our case 4 is eocAI — does eocAI handle Demon 66 / Voodoo Demon 67 / Fire Imp 24? Let me check.

5. **哈比 48 / aiStyle 14 蝙蝠族专属分支** — vanilla aiStyle 14 at :22895 (batAI). Harpy is NPC 48, aiStyle 14? Yes Harpy has aiStyle 14? Hmm... Actually Harpy in 1.4 uses aiStyle 14? I believe yes (Flying). The batAI main body is already fixed — I only check the two exclusive branches: 158 vampire bat (Giant Bat? no — 158 = "Vampire Bat"? Actually 158 is "Slimer"? no... 158 = Vampire Bat? hmm; 660 = Giant Fox Bat (苯... "巨狐蝠" = Giant Fox Bat, NPC 660)). I need to find type==158 and type==660 branches inside aiStyle 14 in vanilla and compare with our batAI.

6. **骷髅王手/克眼之外的眼睛族专属** — skeletronHandAI is imported from bossAI. eocAI is in Enemy.ts? Let me check where eocAI is defined. The task says "若 Enemy.ts 有 eocAI/eyeAI 家族". eocAI is `this.eocAI` so it's a method of Enemy (maybe defined in a separate partial file? In TS you can't have partial classes, so Enemy.ts must define it or it's mixed in). Let me grep for "eocAI(" definitions.

7. **Other unlisted flying/aquatic cases** — from the switch: case 2 floatEyeAI (already fixed, don't re-report main body), case 14 batAI (main fixed), case 16 swimAI (flag22 fixed; but other parts? The task says "已知正确带行号的大块一句话带过" and swimAI flag22 已修勿重报). I should check other flying/aquatic cases not listed: e.g., case 17 vultureAI (AI_017, flying — per memory "秃鹫/萤火虫 AI 修复" already done), case 44 flyingSwarmerAI (AI_044 flying fish), case 56 dungeonSpiritAI, case 49 angryNimbusAI... The task says "其他 Enemy.ts aiStyle switch 里未列但属飞行/水生的 case(自己 grep 枚举补全,归你管的报出来)" — so I should enumerate flying/aquatic cases and audit them too, but "控制密度" — control density. The focus is the listed families; others get a lighter check.

Let me be careful about scope: The listed families are primary. I'll do deep audits of:
- AI_005 swarmerAI vs cs:50626-51356
- chargerAI vs cs:62809-63372 (AI_026) + 620 goblin shark branch cs:64118-64230 (which is inside AI_107 ImprovedWalkers? Actually 64118-64230 is within AI_107_ImprovedWalkers cs:63372-64919). Hmm wait — the task says "620 地精鲨 wet 游泳档 cs:64118-64230". So goblin shark 620 is aiStyle 107 but has a wet branch within AI_107. Our dispatch: case 107 → if vanillaId !== 620 ai107ImprovedWalkers else chargerAI(game,p,1). Hmm, that means our code routes 620 entirely to chargerAI with flag 1. Need to compare against cs:64118-64230 which is presumably `if (npc.type == 620)` inside AI_107.

Wait, but actually, let me reconsider: is the hornet family using aiStyle 26? "chargerAI(黄蜂族 42/231-235 冲刺链)" — hmm, maybe our chargerAI implements AI_026 and also handles hornets? Hornets in vanilla have aiStyle 26? No! Hornets have aiStyle... Hornets (NPC 42? no). Let me get IDs straight by grepping NPCID or the spawn code. Actually Terraria NPC 42 = "Hornet"? Hmm, I really think Hornet is 42? Let me check: The jungle hornet... NPC IDs around 42: 37 = ...? 

Terraria 1.4 NPC IDs (approx):
- 16 Zombie? no. Let me recall precisely: 
  - 1 Blue Slime? No, 1 = Blue Slime? Actually NPC 1 = Blue Slime? Hmm, -1? Let me just grep the decompiled source for type assignments.

Anyway — the vanilla AI_026_Unicorns function handles npc.type 62 (Unicorn)? and also "if (npc.type == 42)"? Hmm. Let me look at AI_026 source.

Actually wait: I recall AI_026 (Unicorn) covers: Unicorn, Wolf? No, wolf is fighter... Let me just read the code. AI_026_Unicorns at cs:62809. And NPC 42 — in Terraria, NPC 42 is "Man Eater"? Hmm no. Let me grep quickly.

Also 231-235: those are... 231 = Queen Bee Larva? no (that's NPC 211? hmm). 231-235: Moss hornet variants! Yes! 231-235 are the Moss Hornet variants (big/little etc.). And 42 = Hornet. So chargerAI handles hornets 42 and moss hornets 231-235? But wait — do hornets have aiStyle 26? Hmm, actually no — Hornets have aiStyle... let me think. Hornets fly. In vanilla, Hornet aiStyle = 26? I don't think so... 

Hmm wait. Actually I remember now: Hornets use "aiStyle 26"? No. Let me check: In vanilla, Hornet NPC.aiStyle = 26? The AI_026 function is named "Unicorns" but might contain a `if (npc.type == 42 || (npc.type >= 231 && npc.type <= 235))` branch for hornets (flying charger). Hmm, but unicorns don't fly. Actually I do recall AI_026 handles both unicorns and wolves? No...

Let me just read the source. Also our chargerAI(game, p, 1) for goblin shark.

Let me also confirm which file our AI functions live in. eocAI, swarmerAI, chargerAI, jellyfishAI, batAI — grep for their definitions.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:04.677Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private \\(swarmerAI\\|chargerAI\\|jellyfishAI\\|batAI\\|eocAI\\|floatEyeAI\\|swimAI\\|ghostAI\\|flyAI\\|dungeonGuardianAI\\)\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Locate AI method definitions in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:04.723Z

**📎 ToolResult**

```
3595:  private floatEyeAI(game: GameHooks, player: Player | null) {
3779:  private swarmerAI(game: GameHooks, player: Player | null) {
4177:  private dungeonGuardianAI(game: GameHooks, player: Player | null) {
4279:  private chargerAI(game: GameHooks, player: Player | null, maxSpd = 6) {
4347:  private batAI(game: GameHooks, player: Player | null) {
4453:  private swimAI(game: GameHooks, player: Player | null) {
4621:  private jellyfishAI(game: GameHooks, player: Player | null) {
4725:  private ghostAI(game: GameHooks, player: Player | null) {
6752:  private flyAI(game: GameHooks, player: Player | null, steer: number) {
6886:  private eocAI(game: GameHooks, player: Player | null) {

```


---

## 🤖 Assistant · 2026-08-19T03:07:05.135Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 62809,63000p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_026_Unicorns start"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:05.249Z

**📎 ToolResult**

```
	private void AI_026_Unicorns()
	{
		int num = 30;
		int num2 = 10;
		bool flag = false;
		bool flag2 = false;
		bool flag3 = false;
		if (velocity.Y == 0f && ((velocity.X > 0f && direction < 0) || (velocity.X < 0f && direction > 0)))
		{
			flag2 = true;
			ai[3] += 1f;
		}
		if (type == 546)
		{
			num2 = 4;
			bool flag4 = velocity.Y == 0f;
			for (int i = 0; i < Main.maxNPCs; i++)
			{
				if (i != whoAmI && Main.npc[i].active && Main.npc[i].type == type && Math.Abs(position.X - Main.npc[i].position.X) + Math.Abs(position.Y - Main.npc[i].position.Y) < (float)width)
				{
					if (position.X < Main.npc[i].position.X)
					{
						velocity.X -= 0.05f;
					}
					else
					{
						velocity.X += 0.05f;
					}
					if (position.Y < Main.npc[i].position.Y)
					{
						velocity.Y -= 0.05f;
					}
					else
					{
						velocity.Y += 0.05f;
					}
				}
			}
			if (flag4)
			{
				velocity.Y = 0f;
			}
		}
		if (type == 315)
		{
			int num3 = 480;
			if (localAI[0]++ >= (float)num3)
			{
				localAI[0] = 0f;
				int num4 = target;
				if (Main.netMode != 1 && num4 != 255)
				{
					int attackDamage_ForProjectiles = GetAttackDamage_ForProjectiles(40f, 30f);
					Projectile.NewProjectile(GetSpawnSourceForNPCFromNPCAI(), base.Center + Main.rand.NextVector2Circular(40f, 40f), new Vector2(velocity.X, Main.rand.NextFloatDirection() * 3f), 1001, attackDamage_ForProjectiles, 0f, Main.myPlayer, num4);
				}
			}
			Lighting.AddLight(base.Center, 0.4f, 0.36f, 0.2f);
			int num5 = frame.Height;
			if (num5 < 1)
			{
				num5 = 1;
			}
			int num6 = frame.Y / num5;
			if (num6 >= 4 && num6 <= 7)
			{
				Vector2 vector = base.Bottom + new Vector2(-30f, -8f);
				Vector2 vector2 = new Vector2(60f, 8f);
				if (Main.rand.Next(3) != 0)
				{
					Dust dust = Dust.NewDustPerfect(vector + new Vector2(Main.rand.NextFloat() * vector2.X, Main.rand.NextFloat() * vector2.Y), 6, velocity);
					dust.scale = 0.6f;
					dust.fadeIn = 1.1f;
					dust.noGravity = true;
					dust.noLight = true;
				}
			}
		}
		if (position.X == oldPosition.X || ai[3] >= (float)num || flag2)
		{
			ai[3] += 1f;
			flag3 = true;
		}
		else if (ai[3] > 0f)
		{
			ai[3] -= 1f;
		}
		if (ai[3] > (float)(num * num2))
		{
			ai[3] = 0f;
		}
		if (justHit)
		{
			ai[3] = 0f;
		}
		if (ai[3] == (float)num)
		{
			netUpdate = true;
		}
		Vector2 vector3 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
		float num7 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector3.X;
		float num8 = Main.player[target].position.Y - vector3.Y;
		float num9 = (float)Math.Sqrt(num7 * num7 + num8 * num8);
		if (num9 < 200f && !flag3)
		{
			ai[3] = 0f;
		}
		if (type == 410)
		{
			ai[1] += 1f;
			bool flag5 = ai[1] >= 240f;
			if (!flag5 && velocity.Y == 0f)
			{
				for (int j = 0; j < 255; j++)
				{
					if (Main.player[j].active && !Main.player[j].dead && Main.player[j].Distance(base.Center) < 800f && Main.player[j].Center.Y < base.Center.Y && Math.Abs(Main.player[j].Center.X - base.Center.X) < 20f)
					{
						flag5 = true;
						break;
					}
				}
			}
			if (flag5 && Main.netMode != 1)
			{
				for (int k = 0; k < 3; k++)
				{
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, (Main.rand.NextFloat() - 0.5f) * 2f, -4f - 10f * Main.rand.NextFloat(), 538, 50, 0f, Main.myPlayer);
				}
				life = 0;
				HitEffect(0, 9999.0);
				active = false;
				return;
			}
		}
		else if (type == 423)
		{
			if (ai[2] == 1f)
			{
				ai[1] += 1f;
				velocity.X *= 0.7f;
				if (ai[1] < 30f)
				{
					Vector2 vector4 = base.Center + Vector2.UnitX * spriteDirection * -20f;
					Dust obj = Main.dust[Dust.NewDust(vector4, 0, 0, 242)];
					Vector2 vector5 = Vector2.UnitY.RotatedByRandom(6.2831854820251465);
					obj.position = vector4 + vector5 * 20f;
					obj.velocity = -vector5 * 2f;
					obj.scale = 0.5f + vector5.X * (float)(-spriteDirection);
					obj.fadeIn = 1f;
					obj.noGravity = true;
				}
				else if (ai[1] == 30f)
				{
					for (int l = 0; l < 20; l++)
					{
						Vector2 vector6 = base.Center + Vector2.UnitX * spriteDirection * -20f;
						Dust obj2 = Main.dust[Dust.NewDust(vector6, 0, 0, 242)];
						Vector2 vector7 = Vector2.UnitY.RotatedByRandom(6.2831854820251465);
						obj2.position = vector6 + vector7 * 4f;
						obj2.velocity = vector7 * 4f + Vector2.UnitX * Main.rand.NextFloat() * spriteDirection * -5f;
						obj2.scale = 0.5f + vector7.X * (float)(-spriteDirection);
						obj2.fadeIn = 1f;
						obj2.noGravity = true;
					}
				}
				if (velocity.X > -0.5f && velocity.X < 0.5f)
				{
					velocity.X = 0f;
				}
				if (ai[1] == 30f && Main.netMode != 1)
				{
					int attackDamage_ForProjectiles2 = GetAttackDamage_ForProjectiles(50f, 35f);
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X + (float)(spriteDirection * -20), base.Center.Y, spriteDirection * -7, 0f, 575, attackDamage_ForProjectiles2, 0f, Main.myPlayer, target);
				}
				if (ai[1] >= 60f)
				{
					ai[1] = -Main.rand.Next(320, 601);
					ai[2] = 0f;
				}
			}
			else
			{
				ai[1] += 1f;
				if (ai[1] >= 180f && num9 < 500f && velocity.Y == 0f)
				{
					flag = true;
					ai[1] = 0f;
					ai[2] = 1f;
					netUpdate = true;
				}
				else if (velocity.Y == 0f && num9 < 100f && Math.Abs(velocity.X) > 3f && ((base.Center.X < Main.player[target].Center.X && velocity.X > 0f) || (base.Center.X > Main.player[target].Center.X && velocity.X < 0f)))
				{
					velocity.Y -= 4f;

```


---

## 🤖 Assistant · 2026-08-19T03:07:21.233Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK so AI_026 handles types: 546 (Crawltipede junior? no — 546 is "Sroller"? hmm, 546 = "Solar Pillar"? no...). Actually 546 is... hmm. Let me not worry — types in AI_026: 546, 315 (Selenian? no — 315 = "Blood Feeder"? hmm), 410 (Drakomire Rider? no — 410 = "Sroller"?), 423 (Corite)... these are all walkers. Hmm wait, 410 = Sroller, 423 = Corite, 315 = Selenian, 546 = ? These are Tower-side enemies.

Hmm wait — but the task said chargerAI covers "黄蜂族 42/231-235 冲刺链". Hornets! Let me check whether hornets have aiStyle 26. Hmm, actually... Hornets in vanilla have aiStyle 26? No wait. Hornets are aiStyle... Let me grep the type-specific code inside AI_026 for hornet types 42, 231-235.

Wait, actually I misremember: In Terraria, Hornet NPC 42? No! NPC 42 = "Hornet"? The jungle hornet is NPC 42? Hmm... Actually I'm fairly confident: NPC 42 is "Man Eater"? no. Let me check the ID table: 

Terraria NPC IDs: 
- 41 = Jellyfish? no.
- Actually: 16 = Zombie? No — Zombie is 21? Hmm.

Let me just grep for "npc.type == 42" or check the NPC id table in the decompiled source. Let me search for type 42 usage in AI_026 continuation.

Actually, hmm: I recall in the AI_026 there's a section for `if (type == 42 || (type > 230 && type < 236))` — hmm wait that's for... Hornets ARE 42? No wait — 42 = "Hornet"? Let me verify via our own repo: game data has NPC defs with names. Let me grep vanilla.json or NPC defs for hornet.

Actually from memory: NPC 42 = "Hornet" is wrong; NPC 42 = "Hornet"... ugh. Terraria ID list (1.4): 
- 37 Skeleton? no.
Let me just check: Desert Antlion = 42? Hmm no, Antlion = 41? 

I'll grep the decompiled source. NPCID in decompiled might not exist as class with names, but there's usually a switch in SetDefaults with type names. Or grep "Hornet" in NPC.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:22.474Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"type == 42\\b\\|type >= 231\\|type > 230\\|npc.type == 42\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; grep -n \"\\\"Hornet\\\"\\|Hornet\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs | head",
 "description": "Find hornet type IDs in vanilla"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:22.533Z

**📎 ToolResult**

```
9211:		else if (type == 42)
50720:		else if (type == 42 || (type >= 231 && type <= 235))
50826:		bool flag3 = type == 42 || type == 94 || type == 619 || type == 176 || type == 210 || type == 211 || (type >= 231 && type <= 235);
51031:		else if (type == 42 || type == 176 || type == 205 || (type >= 231 && type <= 235))
51047:		if (type == 6 || type == 619 || type == 23 || type == 42 || type == 94 || type == 139 || type == 173 || type == 176 || type == 205 || type == 210 || type == 211 || (type >= 231 && type <= 235))
51130:		if (type == 42 || type == 176 || (type >= 231 && type <= 235))
78885:		if (Main.netMode != 1 && Main.getGoodWorld && (type == 42 || type == 176 || (type >= 231 && type <= 235)))
90738:			else if (type == 42 || type == 176 || type == 205 || (type >= 231 && type <= 235))
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T03:07:22.997Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 63000,63372p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read rest of vanilla AI_026_Unicorns"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:23.042Z

**📎 ToolResult**

```
					velocity.Y -= 4f;
				}
			}
		}
		else if (type == 155 || type == 329)
		{
			if (velocity.Y == 0f && num9 < 100f && Math.Abs(velocity.X) > 3f && ((position.X + (float)(width / 2) < Main.player[target].position.X + (float)(Main.player[target].width / 2) && velocity.X > 0f) || (position.X + (float)(width / 2) > Main.player[target].position.X + (float)(Main.player[target].width / 2) && velocity.X < 0f)))
			{
				velocity.Y -= 4f;
			}
		}
		else if (type == 546 && velocity.Y == 0f && Math.Abs(velocity.X) > 3f && ((base.Center.X < Main.player[target].Center.X && velocity.X > 0f) || (base.Center.X > Main.player[target].Center.X && velocity.X < 0f)))
		{
			velocity.Y -= 4f;
			SoundEngine.PlaySound(3, base.Center, 11);
		}
		if (type == 546 && !Main.player[target].ZoneDesert)
		{
			int num10 = direction;
			TargetClosest();
			if (!Main.player[target].ZoneDesert)
			{
				EncourageDespawn(10);
				ai[3] = num;
				direction = num10;
			}
		}
		if (ai[3] < (float)num)
		{
			if ((type == 329 || type == 315) && !Main.pumpkinMoon)
			{
				EncourageDespawn(10);
			}
			else
			{
				TargetClosest();
			}
		}
		else
		{
			if (velocity.X == 0f)
			{
				if (velocity.Y == 0f)
				{
					ai[0] += 1f;
					if (ai[0] >= 2f)
					{
						direction *= -1;
						spriteDirection = direction;
						ai[0] = 0f;
					}
				}
			}
			else
			{
				ai[0] = 0f;
			}
			directionY = -1;
			if (direction == 0)
			{
				direction = 1;
			}
		}
		float num11 = 6f;
		float num12 = 0.07f;
		if (!flag && (velocity.Y == 0f || wet || (velocity.X <= 0f && direction < 0) || (velocity.X >= 0f && direction > 0)))
		{
			if (type == 155)
			{
				if (velocity.X > 0f && direction < 0)
				{
					velocity.X *= 0.95f;
				}
				if (velocity.X < 0f && direction > 0)
				{
					velocity.X *= 0.95f;
				}
			}
			else if (type == 329)
			{
				if (velocity.X > 0f && direction < 0)
				{
					velocity.X *= 0.9f;
				}
				if (velocity.X < 0f && direction > 0)
				{
					velocity.X *= 0.9f;
				}
				if (direction > 0 && velocity.X < 3f)
				{
					velocity.X += 0.1f;
				}
				if (direction < 0 && velocity.X > -3f)
				{
					velocity.X -= 0.1f;
				}
			}
			else if (type == 315)
			{
				if (velocity.X > 0f && direction < 0)
				{
					velocity.X *= 0.95f;
				}
				if (velocity.X < 0f && direction > 0)
				{
					velocity.X *= 0.95f;
				}
				if (velocity.X < 0f - num11 || velocity.X > num11)
				{
					if (velocity.Y == 0f)
					{
						velocity *= 0.8f;
					}
				}
				else if (velocity.X < num11 && direction == 1)
				{
					velocity.X += 0.07f;
					if (velocity.X > num11)
					{
						velocity.X = num11;
					}
				}
				else if (velocity.X > 0f - num11 && direction == -1)
				{
					velocity.X -= 0.07f;
					if (velocity.X < 0f - num11)
					{
						velocity.X = 0f - num11;
					}
				}
			}
			else if (type == 410)
			{
				if (Math.Sign(velocity.X) != direction)
				{
					velocity.X *= 0.9f;
				}
				num11 = 6f;
				num12 = 0.2f;
			}
			else if (type == 423)
			{
				if (Math.Sign(velocity.X) != direction)
				{
					velocity.X *= 0.85f;
				}
				num11 = 10f;
				num12 = 0.2f;
			}
			else if (type == 546)
			{
				if (Math.Sign(velocity.X) != direction)
				{
					velocity.X *= 0.92f;
				}
				float num13 = MathHelper.Lerp(0.6f, 1f, Math.Abs(Main.windSpeedTarget)) * (float)Math.Sign(Main.windSpeedTarget);
				if (!Main.player[target].ZoneSandstorm)
				{
					num13 = 0f;
				}
				num11 = 4f + num13 * (float)direction * 3f;
				num12 = 0.05f;
			}
			if (velocity.X < 0f - num11 || velocity.X > num11)
			{
				if (velocity.Y == 0f)
				{
					velocity *= 0.8f;
				}
			}
			else if (velocity.X < num11 && direction == 1)
			{
				velocity.X += num12;
				if (velocity.X > num11)
				{
					velocity.X = num11;
				}
			}
			else if (velocity.X > 0f - num11 && direction == -1)
			{
				velocity.X -= num12;
				if (velocity.X < 0f - num11)
				{
					velocity.X = 0f - num11;
				}
			}
		}
		if (velocity.Y >= 0f)
		{
			int num14 = 0;
			if (velocity.X < 0f)
			{
				num14 = -1;
			}
			if (velocity.X > 0f)
			{
				num14 = 1;
			}
			Vector2 vector8 = position;
			vector8.X += velocity.X;
			int num15 = (int)((vector8.X + (float)(width / 2) + (float)((width / 2 + 1) * num14)) / 16f);
			int num16 = (int)((vector8.Y + (float)height - 1f) / 16f);
			if (Main.tile[num15, num16] == null)
			{
				Main.tile[num15, num16] = new Tile();
			}
			if (Main.tile[num15, num16 - 1] == null)
			{
				Main.tile[num15, num16 - 1] = new Tile();
			}
			if (Main.tile[num15, num16 - 2] == null)
			{
				Main.tile[num15, num16 - 2] = new Tile();
			}
			if (Main.tile[num15, num16 - 3] == null)
			{
				Main.tile[num15, num16 - 3] = new Tile();
			}
			if (Main.tile[num15, num16 + 1] == null)
			{
				Main.tile[num15, num16 + 1] = new Tile();
			}
			if ((float)(num15 * 16) < vector8.X + (float)width && (float)(num15 * 16 + 16) > vector8.X && ((Main.tile[num15, num16].nactive() && !Main.tile[num15, num16].topSlope() && !Main.tile[num15, num16 - 1].topSlope() && Main.tileSolid[Main.tile[num15, num16].type] && !Main.tileSolidTop[Main.tile[num15, num16].type]) || (Main.tile[num15, num16 - 1].halfBrick() && Main.tile[num15, num16 - 1].nactive())) && (!Main.tile[num15, num16 - 1].nactive() || !Main.tileSolid[Main.tile[num15, num16 - 1].type] || Main.tileSolidTop[Main.tile[num15, num16 - 1].type] || (Main.tile[num15, num16 - 1].halfBrick() && (!Main.tile[num15, num16 - 4].nactive() || !Main.tileSolid[Main.tile[num15, num16 - 4].type] || Main.tileSolidTop[Main.tile[num15, num16 - 4].type]))) && (!Main.tile[num15, num16 - 2].nactive() || !Main.tileSolid[Main.tile[num15, num16 - 2].type] || Main.tileSolidTop[Main.tile[num15, num16 - 2].type]) && (!Main.tile[num15, num16 - 3].nactive() || !Main.tileSolid[Main.tile[num15, num16 - 3].type] || Main.tileSolidTop[Main.tile[num15, num16 - 3].type]) && (!Main.tile[num15 - num14, num16 - 3].nactive() || !Main.tileSolid[Main.tile[num15 - num14, num16 - 3].type]))
			{
				float num17 = num16 * 16;
				if (Main.tile[num15, num16].halfBrick())
				{
					num17 += 8f;
				}
				if (Main.tile[num15, num16 - 1].halfBrick())
				{
					num17 -= 8f;
				}
				if (num17 < vector8.Y + (float)height)
				{
					float num18 = vector8.Y + (float)height - num17;
					if ((double)num18 <= 16.1)
					{
						gfxOffY += position.Y + (float)height - num17;
						position.Y = num17 - (float)height;
						if (num18 < 9f)
						{
							stepSpeed = 1f;
						}
						else
						{
							stepSpeed = 2f;
						}
					}
				}
			}
		}
		if (velocity.Y == 0f)
		{
			bool flag6 = true;
			int num19 = (int)(position.Y - 7f) / 16;
			int num20 = (int)(position.X - 7f) / 16;
			int num21 = (int)(position.X + (float)width + 7f) / 16;
			for (int m = num20; m <= num21; m++)
			{
				if (Main.tile[m, num19] != null && Main.tile[m, num19].nactive() && Main.tileSolid[Main.tile[m, num19].type])
				{
					flag6 = false;
					break;
				}
			}
			if (flag6)
			{
				int num22 = (int)((position.X + (float)(width / 2) + (float)((width / 2 + 2) * direction) + velocity.X * 5f) / 16f);
				int num23 = (int)((position.Y + (float)height - 15f) / 16f);
				if (Main.tile[num22, num23] == null)
				{
					Main.tile[num22, num23] = new Tile();
				}
				if (Main.tile[num22, num23 - 1] == null)
				{
					Main.tile[num22, num23 - 1] = new Tile();
				}
				if (Main.tile[num22, num23 - 2] == null)
				{
					Main.tile[num22, num23 - 2] = new Tile();
				}
				if (Main.tile[num22, num23 - 3] == null)
				{
					Main.tile[num22, num23 - 3] = new Tile();
				}
				if (Main.tile[num22, num23 + 1] == null)
				{
					Main.tile[num22, num23 + 1] = new Tile();
				}
				if (Main.tile[num22, num23 + 2] == null)
				{
					Main.tile[num22, num23 + 2] = new Tile();
				}
				if (Main.tile[num22 + direction, num23 - 1] == null)
				{
					Main.tile[num22 + direction, num23 - 1] = new Tile();
				}
				if (Main.tile[num22 + direction, num23 + 1] == null)
				{
					Main.tile[num22 + direction, num23 + 1] = new Tile();
				}
				if (Main.tile[num22 - direction, num23 + 1] == null)
				{
					Main.tile[num22 - direction, num23 + 1] = new Tile();
				}
				if (Main.tile[num22 + direction, num23 + 3] == null)
				{
					Main.tile[num22 + direction, num23 + 3] = new Tile();
				}
				int num24 = spriteDirection;
				if (type == 423 || type == 410 || type == 546)
				{
					num24 *= -1;
				}
				if ((velocity.X < 0f && num24 == -1) || (velocity.X > 0f && num24 == 1))
				{
					bool flag7 = type == 410 || type == 423;
					float num25 = 3f;
					if (Main.tile[num22, num23 - 2].nactive() && Main.tileSolid[Main.tile[num22, num23 - 2].type])
					{
						if (Main.tile[num22, num23 - 3].nactive() && Main.tileSolid[Main.tile[num22, num23 - 3].type])
						{
							velocity.Y = -8.5f;
							netUpdate = true;
						}
						else
						{
							velocity.Y = -7.5f;
							netUpdate = true;
						}
					}
					else if (Main.tile[num22, num23 - 1].nactive() && !Main.tile[num22, num23 - 1].topSlope() && Main.tileSolid[Main.tile[num22, num23 - 1].type])
					{
						velocity.Y = -7f;
						netUpdate = true;
					}
					else if (position.Y + (float)height - (float)(num23 * 16) > 20f && Main.tile[num22, num23].nactive() && !Main.tile[num22, num23].topSlope() && Main.tileSolid[Main.tile[num22, num23].type])
					{
						velocity.Y = -6f;
						netUpdate = true;
					}
					else if ((directionY < 0 || Math.Abs(velocity.X) > num25) && (!flag7 || !Main.tile[num22, num23 + 1].nactive() || !Main.tileSolid[Main.tile[num22, num23 + 1].type]) && (!Main.tile[num22, num23 + 2].nactive() || !Main.tileSolid[Main.tile[num22, num23 + 2].type]) && (!Main.tile[num22 + direction, num23 + 3].nactive() || !Main.tileSolid[Main.tile[num22 + direction, num23 + 3].type]))
					{
						velocity.Y = -8f;
						netUpdate = true;
					}
				}
			}
		}
		if (type == 423 && Math.Abs(velocity.X) >= num11 * 0.95f)
		{
			Rectangle hitbox = base.Hitbox;
			for (int n = 0; n < 2; n++)
			{
				if (Main.rand.Next(3) == 0)
				{
					Dust obj3 = Main.dust[Dust.NewDust(hitbox.TopLeft(), hitbox.Width, hitbox.Height, 242)];
					obj3.velocity = Vector2.Zero;
					obj3.noGravity = true;
					obj3.fadeIn = 1f;
					obj3.scale = 0.5f + Main.rand.NextFloat();
				}
			}
		}
		if (type == 546)
		{
			rotation += velocity.X * 0.05f;
			spriteDirection = -direction;
		}
	}

	private void AI_107_ImprovedWalkers()

```


---

## 🤖 Assistant · 2026-08-19T03:07:38.206Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So AI_026 handles ground chargers: 155 (Unicorn? no wait 155 = ...), 329 (Hellhound? no...), 315 (Selenian?), 410 (Sroller), 423 (Corite), 546 (Tomb Crawler? Actually 546 = "Golfer"? no). Let me check: 155 = "Rune Wizard"? no. Hmm, 155 = "Wraith"? no. Actually:
- 155: Werewolf? Hmm no. Let me check: Werewolf = 155? Actually yes! Werewolf is NPC 155. And 329 = "Butterfly"? no. 329 = "Poltergeist"! Yes, Poltergeist = 329 (pumpkin moon ghost)... hmm but that's aiStyle 22? Hmm.

Wait — actually I should check SetDefaults for these types. 155 Werewolf? Let me verify quickly via our repo's data since we have vanilla.json with names. But it doesn't matter much — my main task for chargerAI is: the task description says "chargerAI(黄蜂族 42/231-235 冲刺链...)". Hmm, but hornets are NOT in AI_026. Hornets (42, 231-235) are in AI_005? No wait — grep above showed "50720: else if (type == 42 || (type >= 231 && type <= 235))" which is inside AI_005_EaterOfSouls (50626-51356). So hornets use aiStyle 5?? Hmm no wait. Let me check: NPC 42 Hornet aiStyle — hmm. Actually I recall Hornet aiStyle = 5? No...

Hold on. Hornets in vanilla: NPC.aiStyle = 5? The AI_005_EaterOfSouls function name suggests it's the swarmer style used by EoS. Line 50720 is within 50626-51356 → AI_005. And it has a hornet branch. So yes, hornets (42, 231-235) use aiStyle 5! Hmm wait, really? Let me double check: In Terraria, Hornet's aiStyle... In 1.4 the hornet uses aiStyle 5? I actually think that's right — the "Swarmer" aiStyle covers Eater of Souls, Crimera, Hornets, and many others (e.g., 94? 176? 205? 210? 211? 619? 23?).

Hmm wait — line 51047: `if (type == 6 || type == 619 || type == 23 || type == 42 || type == 94 || type == 139 || type == 173 || type == 176 || type == 205 || type == 210 || type == 211 || (type >= 231 && type <= 235))`. Type 6 = Eater of Souls, 173 = Crimera. So AI_005 is indeed "swarmerAI" and the hornet charge chain is INSIDE AI_005, not chargerAI!

So the task description maps: "chargerAI(黄蜂族 42/231-235 冲刺链;620 地精鲨 wet 游泳档 cs:64118-64230)" — meaning OUR chargerAI is being used for these two things? Our chargerAI(game,p,maxSpd=6) — maybe our chargerAI implements the hornet charge chain from AI_005? Let me read our swarmerAI and chargerAI to see.

Let me read our implementations now: swarmerAI (3779-...), chargerAI (4279-4347), batAI (4347-4453), swimAI (4453-4621), jellyfishAI (4621-4725), ghostAI (4725-...), eocAI (6886-...), flyAI (6752-6886).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:38.514Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "offset": 3779,
 "limit": 400
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:38.526Z

**📎 ToolResult**

```
3779	  private swarmerAI(game: GameHooks, player: Player | null) {
3780	    // ---- Mechdusa 探针挂链(NPC.cs AI_005 :50866-50920):ai3≠0 = 召唤链出生的
3781	    //      挂链探针 → 绕毁灭者头公转锁位(queen 在场时无敌);失效即脱落回常规 ----
3782	    if (this.vanillaId === 139 && this.ai3 !== 0 && mechProbeLock(this, game, player)) return;
3783	    const isEater = this.vanillaId === 6 || this.vanillaId === 173 || this.vanillaId === 139;
3784	    // 蜜蜂（210/211，L50768-50784）：ai[1] 计数爬坡 num3=(ai1-60)/60≤1；
3785	    // 暖机期（num3<1）逐轴速度钳 ±6；速度档 5 / 加速 0.1×num3
3786	    const isBee = this.vanillaId === 210 || this.vanillaId === 211;
3787	    let maxSpd = isEater ? 4 : this.vanillaId === 94 ? 4.2 : this.vanillaId === 5 ? 5 : 6;
3788	    // 619 血鱿鱼（:50702-50705）：num=6 / num2=0.1（默认档 6/0.05 → 加速翻倍）
3789	    let accel = isEater ? 0.02 : this.vanillaId === 94 ? 0.022 : this.vanillaId === 5 ? 0.03
3790	      : this.vanillaId === 619 ? 0.1 : 0.05;
3791	    if (isBee) {
3792	      this.ai1 += 1;
3793	      let ramp = (this.ai1 - 60) / 60;
3794	      if (ramp > 1) ramp = 1;
3795	      else if (this.vx > 6) this.vx = 6;
3796	      else if (this.vx < -6) this.vx = -6;
3797	      if (ramp < 1) {
3798	        if (this.vy > 6) this.vy = 6;
3799	        else if (this.vy < -6) this.vy = -6;
3800	      }
3801	      maxSpd = 5;
3802	      accel = 0.1 * ramp;
3803	    }
3804	    // flag4（L50829）：非 173/6/42/231-235/94/139/619 = 双步加速（蜂族真；eater 族假）
3805	    const vid = this.vanillaId ?? 0;   // swarmerAI 仅数据驱动路径可达，vanillaId 恒非空
3806	    const flag4 = !isEater && vid !== 94 && vid !== 619
3807	      && vid !== 42 && !(vid >= 231 && vid <= 235) && vid !== 139;
3808	    const tx = player ? player.cx : this.cx + this.facing * 100;
3809	    const ty = player ? player.cy : this.cy - 100;
3810	    // 8px 网格量化（L17705-17710）
3811	    const dx = Math.floor(tx / 8) * 8 - Math.floor(this.cx / 8) * 8;
3812	    const dy = Math.floor(ty / 8) * 8 - Math.floor(this.cy / 8) * 8;
3813	    const dist = Math.hypot(dx, dy) || 1;
3814	    const sx = (dx / dist) * maxSpd;
3815	    const sy = (dy / dist) * maxSpd;
3816	    // 摆动项（L50837-50848）：num8 族（6/139/173/205）需 dist>100；flag3 族
3817	    // （42/94/619/176/210/211/231-235，含蜜蜂）无条件摆动
3818	    const swarmGated = isEater || this.vanillaId === 205;
3819	    const swarmAlways = vid === 42 || vid === 94 || vid === 619
3820	      || vid === 176 || isBee || (vid >= 231 && vid <= 235);
3821	    if ((swarmGated && dist > 100) || swarmAlways) {
3822	      if (this.ai0 < -200) this.ai0 = 0; // 类默认 -1120 钳回原版下界（振荡相位漂移 ~22s,2026-08-13 清查）
3823	      this.ai0 += 1;
3824	      if (this.ai0 > 200) this.ai0 = -200;
3825	      this.vy += this.ai0 > 0 ? 0.023 : -0.023;
3826	      this.vx += Math.abs(this.ai0) > 100 ? 0.023 : -0.023;
3827	    } else if (swarmGated) {
3828	      this.ai0 = 0; // 近距无摆动
3829	    }
3830	    // 近距制导（6/94/173/619）
3831	    if (dist < 150 && (isEater || this.vanillaId === 94 || this.vanillaId === 619)) {
3832	      this.vx += sx * 0.007;
3833	      this.vy += sy * 0.007;
3834	    }
3835	    // 各轴步进逼近期望速度（L50924-50961）：flag4 族逆向时追加一步（num2 再乘一次）
3836	    if (this.vx < sx) {
3837	      this.vx += accel;
3838	      if (flag4 && this.vx < 0 && sx > 0) this.vx += accel;
3839	    } else if (this.vx > sx) {
3840	      this.vx -= accel;
3841	      if (flag4 && this.vx > 0 && sx < 0) this.vx -= accel;
3842	    }
3843	    if (this.vy < sy) {
3844	      this.vy += accel;
3845	      if (flag4 && this.vy < 0 && sy > 0) this.vy += accel;
3846	    } else if (this.vy > sy) {
3847	      this.vy -= accel;
3848	      if (flag4 && this.vy > 0 && sy < 0) this.vy -= accel;
3849	    }
3850	    this.facing = this.vx > 0 ? 1 : -1;
3851	    // 旋转角来源分族（cs:51022/51045-51052）：6/94/173/619 用**指向目标的期望速度**
3852	    // (sx,sy)——噬魂怪永远盯着目标转头，惯性环绕/漂移时头不乱摆（此前误用当前速度，
3853	    // 观感"AI 不对"的最大来源）；其余全转头成员（仆从 5 等）原版用当前速度角。
3854	    // 符号取原版 −π/2（:51029/:51045）：本族贴图（NPC_4/NPC_5 实测瞳孔偏帧下半）
3855	    // 正面朝帧底（+Y），canvas rotate 正角顺时针下 −π/2 恰把帧底转向运动方向；
3856	    // 此前 +π/2 把正面调转 180° = "球屁股朝前"（rotationDriven 禁镜像，无翻转可抵）
3857	    const faceTarget = vid === 6 || vid === 94 || vid === 173 || vid === 619;
3858	    const fax = faceTarget ? sx : this.vx;
3859	    const fay = faceTarget ? sy : this.vy;
3860	    this.visAngle = Math.atan2(fay, fax) - Math.PI * 0.5;
3861	    // ---- 黄蜂毒刺（cs:51125-51213：42/176/231-235）：ai[1] 每 tick +rand(5,20)×0.1
3862	    // （苔藓黄蜂 176 ×2）；玩家待机未挥动（原版 itemAnimation==0 && stealth==0 门）清零；
3863	    // ≥130 且有视线且朝向与移动方向一致 → 毒刺（速 8、伤 10×scale/176 30×scale、
3864	    // 散布 ±20），ai[1]=101 次帧清零（原版此处播音效 Item17）
3865	    // ---- 腐化者 94 唾液（cs:51257-51276）：ai[2] 每 tick +1，==180 且有视线 → VileSpit
3866	    // （原版 NewNPC 112 aiStyle 9 追踪球速 7，此处 Dart 直飞近似、伤害取 NPC 112 数据）
3867	    const st = game.world.store;
3868	    const isHornet = vid === 42 || vid === 176 || (vid >= 231 && vid <= 235);
3869	    if (player && !player.dead && (isHornet || vid === 94)) {
3870	      if (this.ai1 === 101) { this.ai1 = 0; game.playSfxFiles?.(['Item_17'], 1, this.cx, this.cy); } // :51147 发射音
3871	      if (isHornet) {
3872	        this.ai1 += (Math.random() * 15 + 5) * 0.1;
3873	        if (vid === 176) this.ai1 += (Math.random() * 15 + 5) * 0.1;
3874	        if (player.useTime === 0) this.ai1 = 0; // 待机清零（原版潜行/挥动门）
3875	        if (this.ai1 >= 130 && this.canSeePlayer(st, player)) {
3876	          const sxp = player.cx - this.cx + (Math.random() * 40 - 20);
3877	          const syp = player.cy - this.cy + (Math.random() * 40 - 20);
3878	          if ((sxp < 0 && this.vx < 0) || (sxp > 0 && this.vx > 0)) {
3879	            const vScale = this.vanilla?.scale ?? 1;
3880	            this.shootDart(game, this.cx, this.cy, sxp, syp, 8, Math.round((vid === 176 ? 30 : 10) * vScale), 55);
3881	            this.ai1 = 101;
3882	          } else this.ai1 = 0;
3883	        }
3884	      } else {
3885	        this.ai2 += 1;
3886	        if (this.ai2 === 180 && this.canSeePlayer(st, player)) {
3887	          // VileSpit（原版 NewNPC 112，cs:51257-51276——aiStyle 9 直飞球速 7）：
3888	          // AI_009 已 1:1，改出真 NPC 112（此前 Dart 直飞近似、伤害取 NPC 112 数据）
3889	          const spit = Enemy.fromVanilla(112, this.cx, this.cy);
3890	          if (spit) addEnemy(game, spit);
3891	          this.ai2 = 0;
3892	        }
3893	      }
3894	    }
3895	    // ---- 探针 139 专属射击段（NPC.cs AI_005 :50975-51007,在位移/反弹之前）：
3896	    //  localAI[0] +1/t（挂链 +3 已在 mechProbeLock）、受击清零；cadence 120(常规)
3897	    //  /360(mech 世界)；84 号弹 25 伤——mech 弹道 = 目标中心-自身中心-玩家速度×20
3898	    //  归一 ×8（预判直飞），常规 = 期望速度直飞（noTileCollide 早退在前,须置于此） */
3899	    if (vid === 139) {
3900	      this.lai0 += 1;
3901	      if (this.justHitT > 0) this.lai0 = 0;
3902	      if (this.lai0 >= (mechQueenUp() ? 360 : 120)) {
3903	        this.lai0 = 0;
3904	        if (player && losClear(game, this.cx, this.cy, player.cx, player.cy)) {
3905	          let pvx = sx, pvy = sy;
3906	          if (mechQueenUp()) {
3907	            const ddx = player.cx - this.cx - player.vx * 20;
3908	            const ddy = player.cy - this.cy - player.vy * 20;
3909	            const dl = Math.hypot(ddx, ddy) || 1;
3910	            pvx = ddx / dl * 8; pvy = ddy / dl * 8;
3911	          }
3912	          shoot(game, this.cx, this.cy, pvx, pvy,
3913	            getAttackDamageForProjectiles(25, 22, this.difficulty), 84);
3914	        }
3915	      }
3916	      if (mechQueenUp()) {
3917	        // :51206-51224 远距(>600)朝目标增速 mech 钳 5（常规 12）,逆向 ×0.9
3918	        if (dist > 600) {
3919	          if ((this.vx > 0 && sx > 0) || (this.vx < 0 && sx < 0)) {
3920	            if (Math.abs(this.vx) < 5) this.vx *= 1.05;
3921	          } else {
3922	            this.vx *= 0.9;
3923	          }
3924	        }
3925	        // :51225-51234 mech && ai2==0（身体段掉落的散探针）：距玩家 <120 →
3926	        // 沿连线推到 120px 外（贴脸风筝位）
3927	        if (this.ai2 === 0 && player) {
3928	          const kx = player.cx - this.cx, ky = player.cy - this.cy;
3929	          const kl = Math.hypot(kx, ky);
3930	          if (kl < 120) {
3931	            this.x = player.cx - kx / (kl || 1) * 120 - this.w / 2;
3932	            this.y = player.cy - ky / (kl || 1) * 120 - this.h / 2;
3933	          }
3934	        }
3935	      }
3936	    }
3937	    // noTileCollide 成员(仆从 type 5 等)原版幽灵位移:直积分、无碰撞无反弹——
3938	    // 曾对所有成员 moveAndCollide+反弹,仆从撞墙弹跳完全不像原版(穿墙追击)
3939	    if (this.vanilla?.noTileCollide) {
3940	      this.x += this.vx;
3941	      this.y += this.vy;
3942	      return;
3943	    }
3944	    moveAndCollide(this, game.world, this.vx, this.vy);
3945	    // 撞墙/撞地反弹 1:1（cs:51041-51066）：6/173 ×0.4、其余 ×0.7；
3946	    // collideX 朝 direction 保底 ±2、collideY |vy|<1.5 保底 ±2（此前最小弹速略）
3947	    const bounce = isEater ? 0.4 : 0.7;
3948	    if (this.hitWall) {
3949	      this.vx = -this.vx * bounce;
3950	      if (this.facing === -1 && this.vx > 0 && this.vx < 2) this.vx = 2;
3951	      if (this.facing === 1 && this.vx < 0 && this.vx > -2) this.vx = -2;
3952	    }
3953	    if (this.onGround || this.hitHead) {
3954	      this.vy = -this.vy * bounce;
3955	      if (this.vy > 0 && this.vy < 1.5) this.vy = 2;
3956	      if (this.vy < 0 && this.vy > -1.5) this.vy = -2;
3957	    }
3958	    // ---- wet 浮力（cs:51106-51136）：噬魂怪族(6/94/173/619) vy>0 ×0.95、-0.3、钳 -2
3959	    // （入水即上浮不沉底）；黄蜂族(42/176/231-235) -0.5 钳 -4
3960	    const inW = st.liquid[st.idx(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE))] > 0;
3961	    if (inW && (vid === 6 || vid === 94 || vid === 173)) {
3962	      if (this.vy > 0) this.vy *= 0.95;
3963	      this.vy -= 0.3;
3964	      if (this.vy < -2) this.vy = -2;
3965	    } else if (inW && (vid === 42 || vid === 176 || (vid >= 231 && vid <= 235))) {
3966	      if (this.vy > 0) this.vy *= 0.95;
3967	      this.vy -= 0.5;
3968	      if (this.vy < -4) this.vy = -4;
3969	    }
3970	    // ---- 环境拖尾尘（cs:51083-51091）：非蜂族 1/20 出下半身尘（dust 18 紫；
3971	    // 173 Crimera dust 5 红），vel.X×0.5/Y×0.1 近似
3972	    if (!isHornet && vid !== 205 && Math.random() < 1 / 20) {
3973	      game.spawnParticles(this.cx, this.y + this.h * 0.5,
3974	        vid === 173 ? '#8A3030' : '#7A4FA8', 1, 0.3, { life: 30, damp: 0.9, grav: 0 });
3975	    }
3976	    // ---- 点光（cs:51006-51017）：**139 探针专属**（AI_005 内 type==139 段——
3977	    //  非全族！）：中心格在世界内且非实心 → Center (0.3,0.1,0.05)
3978	    if (vid === 139) {
3979	      const ltx = Math.floor(this.cx / TILE), lty = Math.floor(this.cy / TILE);
3980	      if (st.inBounds(ltx, lty) && !st.isSolid(ltx, lty)) {
3981	        this.lightRGB = [0.3, 0.1, 0.05];
3982	      }
3983	    }
3984	  }
3985	
3986	  /** AI_010 诅咒头骨（NPC.145.cs:21553+；type 34 路径，书怪 694/魔法骷髅 289 分支未达）：
3987	   *  距离分档速度（>350:5/0.3 >300:3/0.2 >250:1.5/0.1 其余 1/0.011，L21655-21672）；
3988	   *  <250 环绕摆动（ai[0] +=0.9、vy ±0.019、|ai0|>100 时 vx 反向，L21636-21651）；
3989	   *  ai[1] 追击计数 >600 加速档（×8/速度4）>650 清零；贴脸 <100 时 ai[1]=-60（L21620-21634）；
3990	   *  noTileCollide 穿墙直移 */
3991	  private cursedSkullAI(game: GameHooks, player: Player | null) {
3992	    // AI_010 全块 1:1（NPC.cs:21552-21888）。flag9 族员 = 694 水书宝箱怪（多状态机）；
3993	    // 34 诅咒头骨/289 巨型诅咒颅走通用悬浮档
3994	    const isMimic = this.vanillaId === 694;
3995	    let maxSpd = 1, accel = 0.011;                 // num145/num146（:21562-21563）
3996	    const num147 = 600, num148 = 650;              // 脱离加速门（:21564-21565）
3997	    let dx = player ? player.cx - this.cx : this.facing * 100;
3998	    let dy = player ? player.cy - this.cy : -100;
3999	    const dist = Math.hypot(dx, dy) || 1;          // num153
4000	    if (this.ai3 !== 3) this.ai1 += 1;             // :21577-21579
4001	    const flag13 = this.ai2 >= 0 && this.ai3 === 2;   // 冲刺态（694 专属）
4002	    const flag14 = this.ai2 >= 0 && this.ai3 === 1;   // 咒球态（694 专属）
4003	    const flag15 = this.ai1 > num147;
4004	    const flag16 = this.ai1 < -30;
4005	    const flag17 = isMimic && !flag13 && !flag14 && !flag15 && flag16;  // 逃逸档
4006	    // 帧机（FindFrame case 694 :77905-77980——AI 侧维护，customFrameIdx 供渲染端直读；
4007	    // 34/289 单帧恒 0 由渲染端缺省，不进此链）
4008	    if (isMimic) this.mimic694Frame();
4009	    // ---- 伪装态 ai[3]==3（:21581-21590）：钉死成"放着的书"——静止、无旋转、
4010	    //      击退免疫；受击 → ai[3]=4 觉醒。AI 早退（不移动不索敌）----
4011	    if (this.ai3 === 3) {
4012	      this.facing = 1; this.visAngle = 0;
4013	      this.vx = 0; this.vy = 0;
4014	      this.kbResistOverride = 0;                   // knockBackResist=0f（:21586）
4015	      if (this.justHit) this.ai3 = 4;              // :21587-21589（frameCounter 清零在帧机）
4016	      return;
4017	    }
4018	    // ---- 觉醒态 ai[3]==4（:21592-21601）：翻书动画 80t，静止，结束转 0----
4019	    if (this.ai3 === 4) {
4020	      this.facing = 1; this.visAngle = 0;
4021	      this.vx = 0; this.vy = 0;
4022	      this.kbResistOverride = 1;                   // knockBackResist=1f（:21597）
4023	      if (this.ai1 > 80) { this.ai1 = 0; this.ai3 = 0; }   // :21598-21600 num149=80
4024	      return;
4025	    }
4026	    if (isMimic) this.kbResistOverride = null;     // :21603-21605 knockBackResist=0.2（def 数据）
4027	    // ---- 逼近/悬停段（:21607-21636；冲刺态跳过）----
4028	    if (!flag13) {
4029	      if (flag15) {
4030	        accel *= 8; maxSpd = 4;                    // 超时脱离加速（:21609-21611）
4031	        if (this.ai1 > num148) this.ai1 = 0;
4032	      } else if (isMimic && player && dist < 100 && this.ai1 >= 0) {
4033	        this.ai1 = -60;                            // 贴脸重置冷却（:21615-21621 flag10 专属）
4034	      } else if (dist < 250) {
4035	        this.ai0 += 0.9;                           // 近距 8 字漂移（:21622-21635）
4036	        if (this.ai0 < -200) this.ai0 = 0;         // 类默认 -1120 钳回（同 swarmerAI 清查）
4037	        this.vy += this.ai0 > 0 ? 0.019 : -0.019;
4038	        this.vx += (this.ai0 < -100 || this.ai0 > 100) ? 0.019 : -0.019;
4039	        if (this.ai0 > 200) this.ai0 = -200;
4040	      }
4041	    }
4042	    // 速度档（:21638-21658）：逃逸 8/0.25 → >350 5/0.3 → >300 3/0.2 → >250 1.5/0.1 → 默认 1/0.011
4043	    if (flag17) { maxSpd = 8; accel = 0.25; }
4044	    else if (dist > 350) { maxSpd = 5; accel = 0.3; }
4045	    else if (dist > 300) { maxSpd = 3; accel = 0.2; }
4046	    else if (dist > 250) { maxSpd = 1.5; accel = 0.1; }
4047	    let sx = (dx / dist) * maxSpd, sy = (dy / dist) * maxSpd;   // num150/num151
4048	    const num154 = sx, num155 = sy;                // 未反向的目标方向（朝向判据）
4049	    if (flag17) { sx = -sx; sy = -sy; }            // :21662-21665 逃逸反向
4050	    if (!player) { sx = this.facing * maxSpd / 2; sy = -maxSpd / 2; }  // 玩家死亡漂移（:21666-21669）
4051	    if (flag13) {
4052	      // 冲刺态速度（:21700-21711）：前 10t 速度 ×0.5（≥18t 归零）；之后以 14px/t
4053	      // 直线冲（方向 = 当前速度，慢于 0.1 时改取朝玩家）
4054	      const n156 = this.ai2;
4055	      if (n156 < 10) {
4056	        this.vx *= 0.5; this.vy *= 0.5;
4057	        if (n156 >= 18) { this.vx = 0; this.vy = 0; }
4058	      } else {
4059	        let vx2 = this.vx, vy2 = this.vy;
4060	        if (Math.hypot(this.vx, this.vy) < 0.1) { vx2 = player!.cx - this.cx; vy2 = player!.cy - this.cy; }
4061	        const vl = Math.hypot(vx2, vy2) || 1;
4062	        this.vx = (vx2 / vl) * 14;
4063	        this.vy = (vy2 / vl) * 14;
4064	      }
4065	    } else {
4066	      if (this.vx < sx) this.vx += accel;
4067	      else if (this.vx > sx) this.vx -= accel;
4068	      if (this.vy < sy) this.vy += accel;
4069	      else if (this.vy > sy) this.vy -= accel;
4070	    }
4071	    // 朝向/旋转（:21713-21727；冲刺态冻结）：num154>0 → 右向不翻 + atan2；
4072	    // <0 → 翻转 + atan2+π；694 的 spriteDirection 再取反（贴图口朝向与 34 相反）
4073	    if (!flag13) {
4074	      if (num154 > 0) { this.facing = -1; this.visAngle = Math.atan2(num155, num154); }
4075	      else if (num154 < 0) { this.facing = 1; this.visAngle = Math.atan2(num155, num154) + Math.PI; }
4076	      if (isMimic) this.facing *= -1;
4077	    }
4078	    // ---- 巨型诅咒颅 289 暗影焰（:21730-21761）：justHit 清态 + ≤500px 状态机
4079	    //      （0 累计 120t → 1 冲刺段 40t），冲刺段 ai[2]==20 发射暗影焰（速 6、伤 25）----
4080	    if (this.vanillaId === 289) {
4081	      if (this.justHit) { this.ai2 = 0; this.ai3 = 0; }    // :21733-21735（受击打断蓄力）
4082	      dx = player ? player.cx - this.cx : this.facing * 100;
4083	      dy = player ? player.cy - this.cy : -100;
4084	      const d289 = Math.hypot(dx, dy) || 1;
4085	      if (player && d289 <= 500) {
4086	        this.ai2 += 1;
4087	        if (this.ai3 === 0) {
4088	          if (this.ai2 > 120) { this.ai2 = 0; this.ai3 = 1; }
4089	        } else {
4090	          if (this.ai2 === 20) this.shootDart(game, this.cx, this.cy, dx, dy, 6, 25, 299);
4091	          if (this.ai2 > 40) { this.ai3 = 0; this.ai2 = 0; }
4092	        }
4093	      } else { this.ai2 = 0; this.ai3 = 0; }
4094	    }
4095	    this.x += this.vx;
4096	    this.y += this.vy;
4097	    // ---- 694 水书宝箱怪攻击状态机（:21763-21888）----
4098	    if (!isMimic) return;
4099	    if (this.justHit) { this.ai2 = 0; this.ai3 = 0; }      // :21765-21767
4100	    const mcx = this.cx, mcy = this.cy + 10;               // center4 = Center+(0,10)（:21768）
4101	    const mdx = player ? player.cx - mcx : this.facing * 100;
4102	    const mdy = player ? player.cy - mcy : -100;
4103	    const md = Math.hypot(mdx, mdy);                       // num152
4104	    // :21776-21783 flag18 = 中距带[100,300]+态 0/2（冲刺蓄力）;flag19 = ≤500+态 0/1（咒球蓄力）
4105	    const flag18 = md >= 100 && md <= 300 && this.ai2 >= 0 && (this.ai3 === 0 || this.ai3 === 2);
4106	    const flag19 = md <= 500 && this.ai2 >= 0 && (this.ai3 === 0 || this.ai3 === 1);
4107	    if (flag18 && (!flag19 || Math.floor(Math.random() * 3) === 0)) {
4108	      // 冲刺链（:21786-21797）：态 0 蓄 120t → 态 2 冲刺 60t → ai[2]=-300 冷却
4109	      this.ai2 += 1;
4110	      if (this.ai3 === 0) {
4111	        if (this.ai2 > 120) { this.ai2 = 0; this.ai3 = 2; }
4112	      } else if (this.ai3 === 2 && this.ai2 > 60) {
4113	        this.ai2 = -300; this.ai3 = 0;
4114	      }
4115	    } else if (flag19) {
4116	      // 咒球链（:21798-21827）：态 0 蓄 120t → 态 1 发射段；态 1 内 30t 结束，
4117	      // ai[2]==17 时 Center+(0,10) 出一颗水球 33（NewNPC :21820-21824）
4118	      this.ai2 += 1;
4119	      if (this.ai3 === 0) {
4120	        if (this.ai2 > 120) { this.ai2 = 0; this.ai3 = 1; }
4121	      } else if (this.ai3 === 1) {
4122	        if (this.ai2 > 30) { this.ai2 = 0; this.ai3 = 0; }
4123	        if (this.ai2 === 17) {
4124	          game.playSfxFiles?.(['Item_8'], 1, this.cx, this.cy);
4125	          // NewNPC 锚 = 底边对齐 center4（16px 球 → 中心再 -8）
4126	          const ball = Enemy.fromVanilla(33, mcx, mcy - 8);
4127	          if (ball) addEnemy(game, ball);
4128	        }
4129	      }
4130	    } else {
4131	      // 脱档衰减（:21879-21886）：ai[2] 归零、态回 0
4132	      this.ai2 += 1;
4133	      if (this.ai2 > 0) this.ai2 = 0;
4134	      this.ai3 = 0;
4135	    }
4136	  }
4137	
4138	  /** 694 帧机（FindFrame case 694，NPC.cs:77905-77980）：
4139	   *  态 3 伪装 → 帧 0；态 4 觉醒 → 帧 0..16（5t/帧）；态 2 冲刺 → 17..19(<40t)/..23；
4140	   *  态 1 咒球 → 24..29；态 0 巡航 → 17/22/23 三帧循环（6t/帧）。
4141	   *  npcFrameT = frameCounter（态切换清零），customFrameIdx 供渲染端直读 */
4142	  private mimic694Frame(): void {
4143	    this.npcFrameT += 1;
4144	    let n = this.customFrameIdx ?? 0;
4145	    if (this.ai3 === 3) {
4146	      n = 0; this.npcFrameT = 0;
4147	    } else if (this.ai3 === 4) {
4148	      if (this.npcFrameT >= 5) { this.npcFrameT = 0; n = Math.min(16, n + 1); }
4149	    } else if (this.ai3 === 2) {
4150	      if (this.ai2 === 0) n = 17;
4151	      if (n < 17 || n > 23) n = 17;
4152	      if (this.npcFrameT >= 5) {
4153	        this.npcFrameT = 0; n += 1;
4154	        if (this.ai2 < 40 && n > 19) n = 19;
4155	        if (n > 23) n = 23;
4156	      }
4157	    } else if (this.ai3 === 1) {
4158	      if (n < 24 || n > 29) n = 24;
4159	      if (this.npcFrameT >= 5) { this.npcFrameT = 0; n = Math.min(29, n + 1); }
4160	    } else {
4161	      if (n < 17 || n > 23) n = 17;
4162	      if (this.npcFrameT >= 6) {
4163	        this.npcFrameT = 0;
4164	        n = n === 17 ? 22 : n === 22 ? 23 : 17;
4165	      }
4166	      if (n >= 30) n = 0;
4167	    }
4168	    this.customFrameIdx = n;
4169	  }
4170	
4171	  // AI_011 骷髅王(35)战斗状态机在 bossAI.ts skeletronBossAI；68 守卫走下方专用分支
4172	
4173	  /** AI_011 地牢守卫(68)（NPC.145.cs:21937-21941, 22277-22288）：
4174	   *  恒 ai[1]=2：伤害 9999、恒速 8 直线追击；玩家死/超 2000px → ai[1]=3 下坠脱场。
4175	   *  noTileCollide 直移。生成瞬间一声 Roar（:21929-21933 localAI[0]==0 单次——
4176	   *  地牢守卫是全游戏唯一"非物品召唤也咆哮"的生成点） */
4177	  private dungeonGuardianAI(game: GameHooks, player: Player | null) {
4178	    if (!this.aiInit) {

```


---

## 🤖 Assistant · 2026-08-19T03:07:41.558Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have the swarmerAI implementation. Now let me read the vanilla AI_005_EaterOfSouls (cs:50626-51356) carefully to compare.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:41.601Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 50626,51130p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_005_EaterOfSouls part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:41.644Z

**📎 ToolResult**

```
	private void AI_005_EaterOfSouls()
	{
		if (type == 210 || type == 211)
		{
			NPCUtils.TargetClosestNonBees(this);
		}
		else if (target < 0 || target <= 255 || Main.player[target].dead)
		{
			TargetClosest();
		}
		if (type == 619)
		{
			if (Main.dayTime)
			{
				velocity.Y -= 0.3f;
				EncourageDespawn(60);
			}
			position += netOffset;
			if (alpha == 255)
			{
				spriteDirection = direction;
				velocity.Y = -6f;
				for (int i = 0; i < 35; i++)
				{
					Dust dust = Dust.NewDustDirect(position, width, height, 5);
					dust.velocity *= 1f;
					dust.scale = 1f + Main.rand.NextFloat() * 0.5f;
					dust.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
					dust.velocity += velocity * 0.5f;
				}
			}
			alpha -= 15;
			if (alpha < 0)
			{
				alpha = 0;
			}
			if (alpha != 0)
			{
				for (int j = 0; j < 2; j++)
				{
					Dust dust2 = Dust.NewDustDirect(position, width, height, 5);
					dust2.velocity *= 1f;
					dust2.scale = 1f + Main.rand.NextFloat() * 0.5f;
					dust2.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
					dust2.velocity += velocity * 0.3f;
				}
			}
			position -= netOffset;
		}
		NPCAimedTarget targetData = GetTargetData();
		bool flag = false;
		if (targetData.Type == NPCTargetType.Player)
		{
			flag = Main.player[target].dead;
		}
		float num = 6f;
		float num2 = 0.05f;
		if (type == 6 || type == 173)
		{
			num = 4f;
			num2 = 0.02f;
			if (type == 6 && Main.expertMode)
			{
				num2 = 0.035f;
			}
			if (Main.remixWorld)
			{
				num2 = 0.06f;
				num = 5f;
			}
		}
		else if (type == 94)
		{
			num = 4.2f;
			num2 = 0.022f;
		}
		else if (type == 619)
		{
			num = 6f;
			num2 = 0.1f;
		}
		else if (type == 252)
		{
			if (targetData.Type != NPCTargetType.None && Collision.CanHit(this, targetData))
			{
				num = 6f;
				num2 = 0.1f;
			}
			else
			{
				num2 = 0.01f;
				num = 2f;
			}
		}
		else if (type == 42 || (type >= 231 && type <= 235))
		{
			num = 3.5f;
			num2 = 0.021f;
			if (type == 231)
			{
				num = 3f;
				num2 = 0.017f;
			}
			num *= 1f - scale;
			num2 *= 1f - scale;
			if ((double)(position.Y / 16f) < Main.worldSurface)
			{
				if (Main.player[target].position.Y - position.Y > 300f && velocity.Y < 0f)
				{
					velocity.Y *= 0.97f;
				}
				if (Main.player[target].position.Y - position.Y < 80f && velocity.Y > 0f)
				{
					velocity.Y *= 0.97f;
				}
			}
		}
		else if (type == 205)
		{
			num = 3.25f;
			num2 = 0.018f;
		}
		else if (type == 176)
		{
			num = 4f;
			num2 = 0.017f;
		}
		else if (type == 23)
		{
			num = 1f;
			num2 = 0.03f;
		}
		else if (type == 5)
		{
			num = 5f;
			num2 = 0.03f;
		}
		else if (type == 210 || type == 211)
		{
			ai[1] += 1f;
			float num3 = (ai[1] - 60f) / 60f;
			if (num3 > 1f)
			{
				num3 = 1f;
			}
			else
			{
				if (velocity.X > 6f)
				{
					velocity.X = 6f;
				}
				if (velocity.X < -6f)
				{
					velocity.X = -6f;
				}
				if (velocity.Y > 6f)
				{
					velocity.Y = 6f;
				}
				if (velocity.Y < -6f)
				{
					velocity.Y = -6f;
				}
			}
			num = 5f;
			num2 = 0.1f;
			num2 *= num3;
		}
		else if (type == 139 && Main.zenithWorld)
		{
			num = 3f;
		}
		Vector2 vector = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
		float num4 = targetData.Position.X + (float)(targetData.Width / 2);
		float num5 = targetData.Position.Y + (float)(targetData.Height / 2);
		num4 = (int)(num4 / 8f) * 8;
		num5 = (int)(num5 / 8f) * 8;
		vector.X = (int)(vector.X / 8f) * 8;
		vector.Y = (int)(vector.Y / 8f) * 8;
		num4 -= vector.X;
		num5 -= vector.Y;
		float num6 = (float)Math.Sqrt(num4 * num4 + num5 * num5);
		float num7 = num6;
		bool flag2 = false;
		if (num6 > 600f)
		{
			flag2 = true;
		}
		if (num6 == 0f)
		{
			num4 = velocity.X;
			num5 = velocity.Y;
		}
		else
		{
			num6 = num / num6;
			num4 *= num6;
			num5 *= num6;
		}
		bool num8 = type == 6 || type == 139 || type == 173 || type == 205;
		bool flag3 = type == 42 || type == 94 || type == 619 || type == 176 || type == 210 || type == 211 || (type >= 231 && type <= 235);
		bool flag4 = type != 173 && type != 6 && type != 42 && (type < 231 || type > 235) && type != 94 && type != 139 && type != 619;
		if (num8 || flag3)
		{
			if (num7 > 100f || flag3)
			{
				ai[0] += 1f;
				if (ai[0] > 0f)
				{
					velocity.Y += 0.023f;
				}
				else
				{
					velocity.Y -= 0.023f;
				}
				if (ai[0] < -100f || ai[0] > 100f)
				{
					velocity.X += 0.023f;
				}
				else
				{
					velocity.X -= 0.023f;
				}
				if (ai[0] > 200f)
				{
					ai[0] = -200f;
				}
			}
			if (num7 < 150f && (type == 6 || type == 94 || type == 173 || type == 619))
			{
				velocity.X += num4 * 0.007f;
				velocity.Y += num5 * 0.007f;
			}
		}
		if (flag)
		{
			num4 = (float)direction * num / 2f;
			num5 = (0f - num) / 2f;
		}
		else if (type == 619 && base.Center.Y > targetData.Center.Y - 200f)
		{
			velocity.Y -= 0.3f;
		}
		if (type == 139 && ai[3] != 0f)
		{
			if (IsMechQueenUp)
			{
				NPC nPC = Main.npc[mechQueen];
				Vector2 vector2 = new Vector2(26f * ai[3], 0f);
				int num9 = (int)ai[2];
				if (num9 < 0 || num9 >= Main.maxNPCs)
				{
					num9 = FindFirstNPC(134);
					ai[2] = num9;
					netUpdate = true;
				}
				if (num9 > -1)
				{
					NPC nPC2 = Main.npc[num9];
					if (!nPC2.active || nPC2.type != 134)
					{
						dontTakeDamage = false;
						if (ai[3] > 0f)
						{
							netUpdate = true;
						}
						ai[3] = 0f;
					}
					else
					{
						Vector2 spinningpoint = nPC2.Center + vector2;
						spinningpoint = spinningpoint.RotatedBy(nPC2.rotation, nPC2.Center);
						base.Center = spinningpoint;
						velocity = nPC.velocity;
						dontTakeDamage = true;
					}
				}
				else
				{
					dontTakeDamage = false;
					if (ai[3] > 0f)
					{
						netUpdate = true;
					}
					ai[3] = 0f;
				}
			}
			else
			{
				dontTakeDamage = false;
				if (ai[3] > 0f)
				{
					netUpdate = true;
				}
				ai[3] = 0f;
			}
		}
		else
		{
			if (type == 139)
			{
				dontTakeDamage = false;
			}
			if (velocity.X < num4)
			{
				velocity.X += num2;
				if (flag4 && velocity.X < 0f && num4 > 0f)
				{
					velocity.X += num2;
				}
			}
			else if (velocity.X > num4)
			{
				velocity.X -= num2;
				if (flag4 && velocity.X > 0f && num4 < 0f)
				{
					velocity.X -= num2;
				}
			}
			if (velocity.Y < num5)
			{
				velocity.Y += num2;
				if (flag4 && velocity.Y < 0f && num5 > 0f)
				{
					velocity.Y += num2;
				}
			}
			else if (velocity.Y > num5)
			{
				velocity.Y -= num2;
				if (flag4 && velocity.Y > 0f && num5 < 0f)
				{
					velocity.Y -= num2;
				}
			}
		}
		if (type == 23)
		{
			if (num4 > 0f)
			{
				spriteDirection = 1;
				rotation = (float)Math.Atan2(num5, num4);
			}
			else if (num4 < 0f)
			{
				spriteDirection = -1;
				rotation = (float)Math.Atan2(num5, num4) + 3.14f;
			}
		}
		else if (type == 139)
		{
			localAI[0] += 1f;
			if (ai[3] != 0f)
			{
				localAI[0] += 2f;
			}
			if (justHit)
			{
				localAI[0] = 0f;
			}
			float num10 = 120f;
			if (IsMechQueenUp)
			{
				num10 = 360f;
			}
			if (Main.netMode != 1 && localAI[0] >= num10)
			{
				localAI[0] = 0f;
				if (targetData.Type != NPCTargetType.None && Collision.CanHit(this, targetData))
				{
					int attackDamage_ForProjectiles = GetAttackDamage_ForProjectiles(25f, 22f);
					int num11 = 84;
					Vector2 vector3 = new Vector2(num4, num5);
					if (IsMechQueenUp)
					{
						Vector2 v = targetData.Center - base.Center - targetData.Velocity * 20f;
						float num12 = 8f;
						vector3 = v.SafeNormalize(Vector2.UnitY) * num12;
					}
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector.X, vector.Y, vector3.X, vector3.Y, num11, attackDamage_ForProjectiles, 0f, Main.myPlayer);
				}
			}
			int num13 = (int)position.X + width / 2;
			int num14 = (int)position.Y + height / 2;
			num13 /= 16;
			num14 /= 16;
			if (WorldGen.InWorld(num13, num14) && !WorldGen.SolidTile(num13, num14))
			{
				Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), 0.3f, 0.1f, 0.05f);
			}
			if (num4 > 0f)
			{
				spriteDirection = 1;
				rotation = (float)Math.Atan2(num5, num4);
			}
			if (num4 < 0f)
			{
				spriteDirection = -1;
				rotation = (float)Math.Atan2(num5, num4) + 3.14f;
			}
		}
		else if (type == 6 || type == 94 || type == 173 || type == 619)
		{
			rotation = (float)Math.Atan2(num5, num4) - 1.57f;
		}
		else if (type == 42 || type == 176 || type == 205 || (type >= 231 && type <= 235))
		{
			if (velocity.X > 0f)
			{
				spriteDirection = 1;
			}
			if (velocity.X < 0f)
			{
				spriteDirection = -1;
			}
			rotation = velocity.X * 0.1f;
		}
		else
		{
			rotation = (float)Math.Atan2(velocity.Y, velocity.X) - 1.57f;
		}
		if (type == 6 || type == 619 || type == 23 || type == 42 || type == 94 || type == 139 || type == 173 || type == 176 || type == 205 || type == 210 || type == 211 || (type >= 231 && type <= 235))
		{
			float num15 = 0.7f;
			if (type == 6 || type == 173)
			{
				num15 = 0.4f;
			}
			if (collideX)
			{
				netUpdate = true;
				velocity.X = oldVelocity.X * (0f - num15);
				if (direction == -1 && velocity.X > 0f && velocity.X < 2f)
				{
					velocity.X = 2f;
				}
				if (direction == 1 && velocity.X < 0f && velocity.X > -2f)
				{
					velocity.X = -2f;
				}
			}
			if (collideY)
			{
				netUpdate = true;
				velocity.Y = oldVelocity.Y * (0f - num15);
				if (velocity.Y > 0f && (double)velocity.Y < 1.5)
				{
					velocity.Y = 2f;
				}
				if (velocity.Y < 0f && (double)velocity.Y > -1.5)
				{
					velocity.Y = -2f;
				}
			}
			position += netOffset;
			if (type == 619)
			{
				int num16 = Dust.NewDust(position, width, height, 5, velocity.X * 0.2f, velocity.Y * 0.2f, 100);
				Main.dust[num16].velocity *= 0.5f;
			}
			else if (type != 42 && type != 139 && type != 176 && type != 205 && type != 210 && type != 211 && type != 252 && (type < 231 || type > 235) && Main.rand.Next(20) == 0)
			{
				int num17 = 18;
				if (type == 173)
				{
					num17 = 5;
				}
				int num18 = Dust.NewDust(new Vector2(position.X, position.Y + (float)height * 0.25f), width, (int)((float)height * 0.5f), num17, velocity.X, 2f, 75, color, scale);
				Main.dust[num18].velocity.X *= 0.5f;
				Main.dust[num18].velocity.Y *= 0.1f;
			}
			position -= netOffset;
		}
		else if (type != 252 && Main.rand.Next(40) == 0)
		{
			int num19 = Dust.NewDust(new Vector2(position.X, position.Y + (float)height * 0.25f), width, (int)((float)height * 0.5f), 5, velocity.X, 2f);
			Main.dust[num19].velocity.X *= 0.5f;
			Main.dust[num19].velocity.Y *= 0.1f;
		}
		if ((type == 6 || type == 94 || type == 173 || type == 619) && wet)
		{
			if (velocity.Y > 0f)
			{
				velocity.Y *= 0.95f;
			}
			velocity.Y -= 0.3f;
			if (velocity.Y < -2f)
			{
				velocity.Y = -2f;
			}
		}
		if (type == 205 && wet)
		{
			if (velocity.Y > 0f)
			{
				velocity.Y *= 0.95f;
			}
			velocity.Y -= 0.5f;
			if (velocity.Y < -4f)
			{
				velocity.Y = -4f;
			}
			TargetClosest();
		}
		if (type == 42 || type == 176 || (type >= 231 && type <= 235))

```


---

## 🤖 Assistant · 2026-08-19T03:07:49.035Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me see the rest (51130-51356).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:49.405Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 51130,51356p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_005_EaterOfSouls part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:49.449Z

**📎 ToolResult**

```
		if (type == 42 || type == 176 || (type >= 231 && type <= 235))
		{
			if (wet)
			{
				if (velocity.Y > 0f)
				{
					velocity.Y *= 0.95f;
				}
				velocity.Y -= 0.5f;
				if (velocity.Y < -4f)
				{
					velocity.Y = -4f;
				}
				TargetClosest();
			}
			if (ai[1] == 101f)
			{
				SoundEngine.PlaySound(SoundID.Item17, position);
				ai[1] = 0f;
			}
			if (Main.netMode != 1)
			{
				ai[1] += (float)Main.rand.Next(5, 20) * 0.1f * scale;
				if (type == 176)
				{
					ai[1] += (float)Main.rand.Next(5, 20) * 0.1f * scale;
				}
				if (Main.getGoodWorld)
				{
					ai[1] += (float)Main.rand.Next(5, 20) * 0.1f * scale;
				}
				if (targetData.Type == NPCTargetType.Player)
				{
					Player player = Main.player[target];
					if (player != null && player.stealth == 0f && player.itemAnimation == 0)
					{
						ai[1] = 0f;
					}
				}
				if (ai[1] >= 130f)
				{
					if (targetData.Type != NPCTargetType.None && Collision.CanHit(this, targetData))
					{
						float num20 = 8f;
						Vector2 vector4 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)(height / 2));
						float num21 = targetData.Center.X - vector4.X + (float)Main.rand.Next(-20, 21);
						float num22 = targetData.Center.Y - vector4.Y + (float)Main.rand.Next(-20, 21);
						if ((num21 < 0f && velocity.X < 0f) || (num21 > 0f && velocity.X > 0f))
						{
							float num23 = (float)Math.Sqrt(num21 * num21 + num22 * num22);
							num23 = num20 / num23;
							num21 *= num23;
							num22 *= num23;
							int num24 = (int)(10f * scale);
							if (type == 176)
							{
								num24 = (int)(30f * scale);
							}
							int num25 = 55;
							int num26 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector4.X, vector4.Y, num21, num22, num25, num24, 0f, Main.myPlayer);
							Main.projectile[num26].timeLeft = 300;
							ai[1] = 101f;
							netUpdate = true;
						}
						else
						{
							ai[1] = 0f;
						}
					}
					else
					{
						ai[1] = 0f;
					}
				}
			}
		}
		if (type == 139 && flag2)
		{
			if ((velocity.X > 0f && num4 > 0f) || (velocity.X < 0f && num4 < 0f))
			{
				int num27 = 12;
				if (IsMechQueenUp)
				{
					num27 = 5;
				}
				if (Math.Abs(velocity.X) < (float)num27)
				{
					velocity.X *= 1.05f;
				}
			}
			else
			{
				velocity.X *= 0.9f;
			}
		}
		if (type == 139 && IsMechQueenUp && ai[2] == 0f)
		{
			Vector2 center = GetTargetData().Center;
			Vector2 v2 = center - base.Center;
			int num28 = 120;
			if (v2.Length() < (float)num28)
			{
				base.Center = center - v2.SafeNormalize(Vector2.UnitY) * num28;
			}
		}
		if (Main.netMode != 1)
		{
			if (Main.getGoodWorld && type == 6 && AnyNPCs(13))
			{
				if (justHit)
				{
					localAI[0] = 0f;
				}
				localAI[0] += 1f;
				if (localAI[0] == 60f)
				{
					if (targetData.Type != NPCTargetType.None && Collision.CanHit(this, targetData))
					{
						NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)(position.X + (float)(width / 2) + velocity.X), (int)(position.Y + (float)(height / 2) + velocity.Y), 666);
					}
					localAI[0] = 0f;
				}
			}
			if (type == 94 && !flag)
			{
				if (justHit)
				{
					localAI[0] = 0f;
				}
				localAI[0] += 1f;
				if (localAI[0] == 180f)
				{
					if (targetData.Type != NPCTargetType.None && Collision.CanHit(this, targetData))
					{
						NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)(position.X + (float)(width / 2) + velocity.X), (int)(position.Y + (float)(height / 2) + velocity.Y), 112);
					}
					localAI[0] = 0f;
				}
			}
			if (type == 619 && !flag)
			{
				if (justHit)
				{
					localAI[0] += 10f;
				}
				localAI[0] += 1f;
				if (localAI[0] >= 120f)
				{
					if (targetData.Type != NPCTargetType.None && Collision.CanHit(this, targetData))
					{
						if ((base.Center - targetData.Center).Length() < 400f)
						{
							Vector2 vector5 = DirectionTo(new Vector2(targetData.Center.X, targetData.Position.Y));
							velocity = -vector5 * 5f;
							netUpdate = true;
							localAI[0] = 0f;
							vector5 = DirectionTo(new Vector2(targetData.Center.X + (float)Main.rand.Next(-100, 101), targetData.Position.Y + (float)Main.rand.Next(-100, 101)));
							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center, vector5 * 15f, 811, 35, 1f, Main.myPlayer);
						}
						else
						{
							localAI[0] = 50f;
						}
					}
					else
					{
						localAI[0] = 50f;
					}
				}
			}
		}
		if ((Main.IsItDay() && type != 173 && type != 619 && type != 6 && type != 23 && type != 42 && type != 94 && type != 176 && type != 205 && type != 210 && type != 211 && type != 252 && (type < 231 || type > 235)) || flag)
		{
			velocity.Y -= num2 * 2f;
			EncourageDespawn(10);
		}
		if (((velocity.X > 0f && oldVelocity.X < 0f) || (velocity.X < 0f && oldVelocity.X > 0f) || (velocity.Y > 0f && oldVelocity.Y < 0f) || (velocity.Y < 0f && oldVelocity.Y > 0f)) && !justHit)
		{
			netUpdate = true;
		}
	}

	public void CopyInteractions(NPC npc)
	{
		for (int i = 0; i < playerInteraction.Length; i++)
		{
			playerInteraction[i] = npc.playerInteraction[i];
		}
		lastInteraction = npc.lastInteraction;
	}

	public static int GetEaterOfWorldsSegmentsCount()
	{
		if (!Main.expertMode)
		{
			return 65;
		}
		return 70;
	}

	public static int GetBrainOfCthuluCreepersCount()
	{
		if (Main.getGoodWorld)
		{
			return 40;
		}
		return 20;
	}

	public static int GetDestroyerSegmentsCount()
	{
		if (Main.getGoodWorld)
		{
			return 100;
		}
		return 80;
	}

	public Vector2 GetMechQueenCenter()
	{
		if (IsMechQueenUp && type == 127)
		{
			return base.Center + new Vector2(0f, -14f);
		}
		return base.Center;
	}

```


---

## 🤖 Assistant · 2026-08-19T03:09:35.268Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I can compare swarmerAI vs vanilla AI_005. Let me note the differences:

**Our swarmerAI issues:**

1. **Hornet speed table missing** (cs:50720-50751): Vanilla hornet (42/231-235): `num = 3.5f, num2 = 0.021f; if type==231: 3/0.017; num *= 1f - scale; num2 *= 1f - scale;` plus the "above world surface" Y-velocity damping branch. Ours: default 6/0.05 for hornets! Line 3787: `let maxSpd = isEater ? 4 : this.vanillaId === 94 ? 4.2 : this.vanillaId === 5 ? 5 : 6;` — hornets (42/176/231-235) fall to default 6/0.05. Also 176 (Moss Hornet): num=4, num2=0.017. Also 205 (Seeker? no — 205 = "Pigron"? hmm; 205 = "Slimer"? Actually 205 = "Slimer2"? whatever) num=3.25/0.018. Also 23: num=1/0.03 (23 = "Eater of Worlds head"? no — type 23 in AI_005... 23 = "Nymph"? no. Hmm, 23 = "?" — type 23 might be "Seeker"? Let me think: NPC 23... Actually AI_005 covers type 23 too. NPC 23 = "?" I think 23 might be the "Hungry"? No. Hmm — 23 = "Bee"? no bees are 210/211. NPC 23... The rotation branch for type 23 uses spriteDirection + atan2 without -1.57. Actually NPC 23 might be... "Seeker" is 562? Hmm, whatever. Let me check which NPC has aiStyle 5 in our data. I'll grep vanilla.json.

   Ours misses: 42/231-235 (3.5/0.021, 231: 3/0.017, ×(1-scale)), 176 (4/0.017), 205 (3.25/0.018), 23 (1/0.03), 252 (2/0.01 or 6/0.1 by LOS — 252 is... "Ghost"? no, 252 = "Cochineal Beetle"? whatever), expert EoS num2=0.035 (type 6 expert), remix world. The task said "蜂群 AI_005(Eater of Souls 6/Crimera 173:8px 网格量化制导、ai[0] 环绕摆动 ±200)" — but also hornet family is in chargerAI per the task? Wait no — the task lists "chargerAI(黄蜂族 42/231-235 冲刺链...)". Hmm — the task author believed hornets are handled by chargerAI in our code? But actually our dispatch: case 5 → swarmerAI, and swarmerAI handles hornets (sting chain at 3861+). And chargerAI is case 26 (AI_026 unicorns) + goblin shark 620. The task's "chargerAI(黄蜂族 42/231-235 冲刺链)" — maybe the task author means the hornet "冲刺链" (charge chain) which in vanilla is part of AI_005... but the task's parenthetical for chargerAI mentions "620 地精鲨 wet 游泳档 cs:64118-64230" which IS chargerAI(game,p,1). So the hornet 42/231-235 part — let me check whether our chargerAI handles hornets too. Let me read chargerAI (4279-4347).

2. **Bee ramp clamp differences** (cs:50768-50790): vanilla: `num3 = (ai[1]-60)/60; if num3 > 1 → 1; else { clamp vx,vy to ±6 }` — note the clamp applies to BOTH axes in the else branch (when num3 <= 1). Ours lines 3795-3800: `else if (this.vx > 6) this.vx = 6; else if (this.vx < -6) this.vx = -6; if (ramp < 1) { if (this.vy > 6)... }` — the vx clamp uses else-if chain but that's fine since mutually exclusive. Wait: ours clamps vx when ramp<=1 and vy when ramp<1 — both same condition actually (`ramp < 1` vs the else of `ramp > 1` — for ramp exactly 1? Vanilla: `if (num3 > 1f) { num3 = 1f } else { clamp }`. So when num3 == 1 exactly, clamp applies. Ours: `if (ramp > 1) ramp = 1; else if (vx>6)...; else if (vx<-6)...` — when ramp == 1 exactly, vx clamp applies. Then `if (ramp < 1)` for vy — when ramp == 1 exactly, vy clamp does NOT apply. Minor off-by-boundary difference; negligible (1 tick). Not worth reporting maybe as low.

   Also missing: bees' TargetClosestNonBees (210/211 target non-bee: i.e., don't target... actually TargetClosestNonBees targets players who aren't... hmm it's about targeting the player unless they have bee-related? Actually it skips targeting players standing near beehives? Whatever - minor). Our code doesn't call target selection at all (uses current target). Targeting differences probably out of scope-ish but could note.

3. **Hornet Y-damp above surface** (cs:50749-50757): `if ((position.Y/16) < Main.worldSurface) { if (target.Y - position.Y > 300 && velocity.Y < 0) velocity.Y *= 0.97; if (target.Y - position.Y < 80 && velocity.Y > 0) velocity.Y *= 0.97; }` — missing in ours. Medium/low.

4. **flag (player dead) handling** (cs:50675-50679, 50795-50800): `flag = Main.player[target].dead;` then `if (flag) { num4 = direction * num/2; num5 = -num/2; }` — dead player → fly up-left drift. Ours: `tx = player ? ... : this.cx + facing*100; ty = player ? ... : this.cy - 100` — hmm. Our dispatch passes `p = hasPlayer ? player : null`. So when player dead, ours uses fake target at cx+facing*100, cy-100 — approximates direction*num/2? Direction is facing... The excluded scope says null player behavior is handled by another agent ("玩家死亡(null player)退化行为"). So skip.

5. **619 Blood Squid dash-shot** (cs:51271-51307): when localAI[0] >= 120 and LOS and dist < 400: velocity = -dirTo * 5 (back away), then shoot projectile 811 at 15 speed from center, 35 damage. Ours: vid 619 gets accel 0.1 but no dash/backoff/shot. Missing entirely! Also the 619 spawn fade dust, daylight despawn (velocity.Y -= 0.3 + EncourageDespawn(60)), ai[?] hover: `type == 619 && base.Center.Y > targetData.Center.Y - 200f → velocity.Y -= 0.3f` (cs:50803-50805) — missing in ours. Medium.

6. **type 6 expert accel 0.035** (cs:50690-50693): `if (type == 6 && Main.expertMode) num2 = 0.035f`. Ours: `accel = isEater ? 0.02 : ...` — no expert branch. Medium-low.

7. **Hornet sting gate uses `player.useTime === 0`** (our line 3874) as approximation of `stealth == 0 && itemAnimation == 0` — noted in comment as approximation. Vanilla: reset when idle (stealth==0 && itemAnimation==0). Ours: useTime===0. itemAnimation vs useTime differ when swinging (itemAnimation>0 during use). This is a known approximation. Also vanilla multiplies rand by scale (`* scale`): `ai[1] += Main.rand.Next(5,20)*0.1f*scale` — ours omits ×scale. Low.

8. **Hornet sting projectile spawn position**: vanilla vector4 = (position.X + width*0.5, position.Y + height/2) — ours uses this.cx, this.cy. Fine.

9. **vanilla sting spread ±20** — ours matches (`Math.random()*40-20`).

10. **Sound at ai[1]==101**: vanilla `SoundID.Item17` then ai[1]=0 — ours plays 'Item_17'. OK.

11. **Corruptor 94 spit** (cs:51258-51276): vanilla uses localAI[0] (not ai[2])! `if (type == 94 && !flag) { if (justHit) localAI[0]=0; localAI[0] += 1; if (localAI[0] == 180) { spawn NPC 112 at position + width/2 + velocity... ; localAI[0] = 0; } }` — Ours uses this.ai2 += 1 and `if (this.ai2 === 180 && canSee)`. Two diffs: (a) uses ai[2] instead of localAI[0] — wrong slot but functionally similar (unless ai2 used elsewhere — for 139 mech it is; for 94 probably unused elsewhere, but hit reset missing: vanilla justHit → localAI[0]=0; ours doesn't reset on justHit). (b) missing justHit reset. Also vanilla checks CanHit (LOS) — ours canSeePlayer. OK. Also spawn position: vanilla `position + width/2 + velocity` (in px + velocity as int) — ours spawns at cx,cy. Minor. Also vanilla NewNPC 112 — ours matches now (spawn 112). Good. But justHit reset missing — low/medium.

12. **619 daylight despawn + fade-in dust** (cs:50636-50665): missing in ours. Low (visual/spawn).

13. **wet for 205** (cs:51106-51116): type 205 wet → vy *= 0.95, vy -= 0.5, clamp -4, TargetClosest. Ours: hornet branch covers 42/176/231-235 but NOT 205. Wait our line 3965: `else if (inW && (vid === 42 || vid === 176 || (vid >= 231 && vid <= 235)))`. 205 has its own wet branch in vanilla (same numbers). Ours misses 205. Low.

14. **wet for 619**: vanilla `type == 6 || 94 || 173 || 619` (cs:51106) — ours line 3961: `vid === 6 || vid === 94 || vid === 173` — missing 619! Low-medium (blood squid buoyancy).

15. **139 far-boost** (cs:51237-51250): vanilla `if (type == 139 && flag2)` where flag2 = num7 > 600 (the ORIGINAL distance BEFORE normalization... wait num7 = num6 initial distance). boost applies when dist > 600, num27 = 12 (regular) / 5 (mech queen), vx *= 1.05 if |vx| < num27, else vx *= 0.9. Ours (3918-3924): `if (mechQueenUp()) { if (dist > 600) ... }` — WRONG GATE: vanilla applies this to ALL 139 probes when dist>600 with cap 12 regular / 5 mech; ours only applies when mechQueenUp, and cap 5 mech only. Missing the regular (cap 12) branch. Medium.

16. **139 mech && ai[2]==0 reposition** (cs:51252-51261): ours has it (3927-3934) — matches, gated mechQueenUp && ai2===0. Vanilla `if (type == 139 && IsMechQueenUp && ai[2] == 0f)`. OK.

17. **Daytime despawn clause** (cs:51324-51329): `if ((IsItDay() && type != 173 && type != 619 && ... && (type < 231 || type > 235)) || flag) { velocity.Y -= num2*2; EncourageDespawn(10); }` — e.g., type 5 (Servant of Cthulhu)? Wait type 5 excluded? No: excluded list: 173,619,6,23,42,94,176,205,210,211,252,231-235. So type 5, 139, and others → daytime: fly up + despawn. Ours: no daytime handling in swarmerAI. But maybe despawn handled globally (EncourageDespawn may be in shared code). Let me check if Enemy.ts has day-despawn logic elsewhere. Grep "encourageDespawn" or dayTime in Enemy.ts. Also null-player behavior excluded from my scope, but daytime behavior is in scope (it's not null player). Let me check.

18. **The bounce uses `direction`** (vanilla) vs `this.facing` (ours line 3950-3951): vanilla `if (direction == -1 && velocity.X > 0 ...)`; ours facing. facing is set from vx>0 at line 3850 — direction in vanilla = target direction (set by TargetClosest), not velocity direction. Minor.

19. **collide bounce set**: vanilla applies to types in the list at cs:51047 (6/619/23/42/94/139/173/176/205/210/211/231-235): bounce 0.7 (0.4 for 6/173). Others (e.g., 252? and default members like type 5?) get the else: dust 1/40 — no bounce. Ours applies bounce to all non-noTileCollide members including type 5 (servant). Hmm: type 5 = Servant of Cthulhu — vanilla: noTileCollide = false for servant; collideX → bounce? Type 5 IS in the list? No! The list: 6,619,23,42,94,139,173,176,205,210,211,231-235. Type 5 NOT in list → else branch: 1/40 dust, no bounce. Ours: bounce 0.7 applied to type 5 too. Hmm wait, actually Servant of Cthulhu — does it collide with tiles? Yes. So in vanilla, servant hits wall and just keeps pushing (velocity persists, collision zeroes it anyway). Ours bounces. Minor behavioral diff (low).

Wait — actually, hmm, careful: our line 3947: `const bounce = isEater ? 0.4 : 0.7;` and applies to all. For type 5, vanilla has no bounce. Low.

20. **dust conditions** (cs:51083-51091): vanilla skips dust for 42/139/176/205/210/211/252/231-235 — ours: `if (!isHornet && vid !== 205 ...)` — ours skips hornets/205 but NOT 139 (should skip) and not 252. 139 gets dust — minor visual. Low.

21. **139 shooting position** — vanilla `Projectile.NewProjectile(spawn, vector.X, vector.Y, ...)` where vector = the 8px-quantized center computed at :50793. Ours uses cx,cy. Minor.

22. **bee clamp** — vx AND vy clamped when num3<=1: ours clamps vx via else-if (works), vy under `ramp<1` (works except ramp==1 boundary). Also vanilla clamps happen BEFORE setting num=5/num2 — same as ours. OK.

23. **Bees TargetClosestNonBees**: vanilla line 50630: `if (type == 210 || type == 211) NPCUtils.TargetClosestNonBees(this); else if (target < 0 || target <= 255 || player[target].dead) TargetClosest();` — hmm wait `target < 0 || target <= 255`? That's odd — target <= 255 is always true for valid player indices... whatever, decompiler artifact; effectively always TargetClosest when target invalid. Ours doesn't retarget per-tick (uses game's current player). Targeting model in our engine is single-player anyway. Skip (targeting infra).

24. **type 252** (cs:50708-50719): num/num2 by CanHit: LOS → 6/0.1 else 2/0.01. Ours: 252 falls to default 6/0.05 always. 252 = "?" — what NPC is 252? "Ichor Sticker"? no that's 173? Hmm. 252 = "Cochineal Beetle"? no... Actually 252 = "Ghost"? no ghost is 81? Hmm, NPC 252 = "Crimson Axe"? no that's 167? Let me not worry; it's a swarmer-family member (maybe "Slimer"? no). Actually! 252 might be "Floaty Gross"? Hmm — Floaty Gross is 252? No, Floaty Gross = 252? I recall Floaty Gross NPC ID = 252? Hmm... Actually I think Floaty Gross is 252. Whatever the name — it's handled by our swarmerAI with default params, missing the LOS-based speed switch. Low-medium.

25. **type 23**: NPC 23 = "Nymph"? no, Nymph is 195... Type 23... hmm. Actually type 23 in Terraria = "Eater of Worlds body"? No, EoW is 13/14/15. Type 23... could be "Corruptor"? no 94. Hmm, type 23... Let me grep our data for aiStyle 5 members. I'll check vanilla.json in game/public or src/data. Let me grep for '"aiStyle": 5' in our data files to enumerate which NPCs route to swarmerAI.

Also the last vanilla block: velocity sign flip → netUpdate. Irrelevant for us.

26. **Hornet netUpdate / timeLeft 300**: our shootDart sets timeLeft? Projectile 55 (Poison Stinger? no — 55 = "Hornet stinger"? proj 55 = PoisonStinger? hmm). Our shootDart(..., 55) — hopefully sets timeLeft. Vanilla explicitly timeLeft = 300 for the projectile. Let me check shootDart signature quickly. Low priority.

Now the **8px grid quantization**: ours (3811-3812): `dx = floor(tx/8)*8 - floor(cx/8)*8; dy likewise` — matches vanilla (num4 = (int)(num4/8)*8; vector quantized then subtracted). dist = hypot(dx,dy) || 1 — vanilla: num6 == 0 → use velocity. Ours uses `|| 1` fallback (dist 0 → sx=0-ish...). Actually if dist==0, vanilla num4=velocity.X, num5=velocity.Y (target speed = current velocity direction). Ours: dist=1, sx=0/1*maxSpd = 0 → target velocity zero. Minor edge case; low.

BUT: vanilla num7 (=num6 original) is used for the swarm gate (`num7 > 100f`) and 139 boost (`num7 > 600`). Ours uses `dist` (same value). OK.

**Swing gate**: vanilla `if (num8 || flag3)` — num8 = {6,139,173,205} needs num7>100; flag3 unconditional. Ours: swarmGated = isEater(6,173,139) || 205 — wait: `const swarmGated = isEater || this.vanillaId === 205;` where isEater = 6||173||139. num8 vanilla = {6,139,173,205} ✓ matches. swarmAlways = 42,94,619,176,210,211,231-235 ✓ = flag3. Good. And near-swarm reset: vanilla — for num8 family when num7 <= 100, ai[0] stays (no reset!). Hmm wait: vanilla `if (num8 || flag3) { if (num7 > 100f || flag3) { ai[0] += 1 ... } if (num7 < 150 && (6/94/173/619)) { ... } }` — no reset of ai[0] when close. Ours line 3827-2828: `else if (swarmGated) { this.ai0 = 0; }` — ours RESETS ai[0] when close! Vanilla doesn't reset. Divergence: minor phase difference — when eater comes within 100px, vanilla freezes ai[0] (stops oscillating but keeps phase); ours zeroes phase. Low severity but confirmed diff.

Wait, ours: `if ((swarmGated && dist > 100) || swarmAlways) {...} else if (swarmGated) { this.ai0 = 0; }` — hmm and for non-gated non-always members (e.g., type 5, 252), nothing. Vanilla same (no branch). OK. The reset is the only diff. Low.

Also note the oscillation sign logic: vanilla: `ai[0] += 1; if (ai[0] > 0) vy += 0.023 else vy -= 0.023; if (ai[0] < -100 || ai[0] > 100) vx += 0.023 else vx -= 0.023; if (ai[0] > 200) ai[0] = -200;` Ours: `this.ai0 += 1; if (this.ai0 > 200) this.ai0 = -200; this.vy += this.ai0 > 0 ? 0.023 : -0.023; this.vx += Math.abs(this.ai0) > 100 ? 0.023 : -0.023;` ✓ matches.

ai0 < -200 clamp at spawn (ours line 3822: `if (this.ai0 < -200) this.ai0 = 0`) — vanilla: ai[0] starts at 0 for AI_005 family? In vanilla, ai array initialized to 0 on spawn (NPC.ai default 0 unless set). The -1120 default is for other families. Our Enemy class default ai0 = -1120? The comment says "类默认 -1120 钳回原版下界". OK fine.

**Rotation**: vanilla type 6/94/173/619: rotation = atan2(num5, num4) - 1.57. Ours: faceTarget for 6/94/173/619 ✓ using sx,sy. BUT WAIT: vanilla uses num4/num5 AFTER the flag (dead player) rewrite and BEFORE... hmm num4/num5 at rotation time: they were possibly modified by `if (flag)` (dead) but otherwise unchanged since normalization. For hornet family (42/176/205/231-235): spriteDirection by velocity.X; rotation = velocity.X * 0.1 (tilt, not full atan2!). Ours line 3850-3860: `this.facing = vx > 0 ? 1 : -1` for ALL members, and visAngle = atan2(fay, fax) - π/2 for ALL members (using vx,vy for non-faceTarget). Vanilla for hornets: rotation = velocity.X * 0.1 (small banking tilt) NOT atan2-π/2! Ours gives hornets a full facing rotation (head pointing along movement). Hmm — but wait, is visAngle used for all? The hornets in Terraria fly upright with slight tilt. This is a visual diff — confirmed: our swarmerAI sets visAngle = atan2(vy,vx) - π/2 for hornets (42/176/205/231-235) and bees (210/211) and 5/23/252 — vanilla: for 42/176/205/231-235 → rotation = vx*0.1 (bank); for else (5, 210, 211, 252, 23...) → atan2(vy,vx) - 1.57 ✓. So hornet family rotation wrong. Medium (visual).

Wait but rendering may handle facing separately. visAngle presumably rotates sprite. Vanilla hornets stay upright-ish. Also vanilla 23 (and 139) use spriteDirection flip + atan2(num5,num4) possibly +π — for 139: rotation = atan2(num5,num4) (no -1.57!) when num4>0... wait: for type 139: `if (num4 > 0f) { spriteDirection = 1; rotation = Atan2(num5, num4); } if (num4 < 0f) { spriteDirection = -1; rotation = Atan2(num5,num4) + 3.14; }` — probe spins with sprite flip, rotation relative. Ours treats 139 in faceTarget group with -π/2. Hmm — type 23 similar. These are minor visual details. I'll report the hornet banking as the main one (medium-low), and note 139/23 flip+atan2 as low.

OK that's AI_005. Now — the task says hornet charge chain is in chargerAI per the parent's description. Let me now read our chargerAI (4279-4347) to see what it does.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:35.765Z · glm-x-preview-260804

```
现在我来读取我们关于 charger、bat、swim、jellyfish 的 AI 实现。
```


---

## 🤖 Assistant · 2026-08-19T03:09:36.062Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 480,
 "offset": 4279
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:36.070Z

**📎 ToolResult**

```
4279	  private chargerAI(game: GameHooks, player: Player | null, maxSpd = 6) {
4280	    const st = game.world.store;
4281	    // 游泳化 620 地精鲨（AI_107_ImprovedWalkers flag27=wet，cs:64122/:64300-64336）：
4282	    // 游泳块在 walker 逻辑之前且 return 接管本 tick——wet 时跳过冲锋/跳跃
4283	    if (this.vanillaId === 620 && this.wetSwimStep(game, player, 620)) return;
4284	    // ---- 点光（cs:62852-62865）：type==315 无头骑士骑手段——Center (0.4,0.36,0.2)
4285	    //  恒亮（南瓜灯头；在 type==315 块内、于 1001 骑手弹幕计时之后）
4286	    if (this.vanillaId === 315) this.lightRGB = [0.4, 0.36, 0.2];
4287	    const solidAt = (x: number, y: number) => x >= 0 && y >= 0 && x < st.w && y < st.h && st.isSolid(x, y);
4288	    // 方向：卡墙 ≥30 tick 折返；玩家 200px 内重置计数并朝玩家冲
4289	    if (this.stuckT >= 30) { this.facing *= -1; this.stuckT = 0; }
4290	    if (player && Math.hypot(player.cx - this.cx, player.cy - this.cy) < 200) {
4291	      this.stuckT = 0;
4292	      this.facing = this.seekDirX(player);
4293	    }
4294	    const dir = this.facing;
4295	    const accel = 0.07;
4296	    // 逆向阻尼（L26105-26108）
4297	    if ((this.vx > 0 && dir < 0) || (this.vx < 0 && dir > 0)) this.vx *= 0.95;
4298	    if (dir === 1 && this.vx < maxSpd) { this.vx += accel; if (this.vx > maxSpd) this.vx = maxSpd; }
4299	    else if (dir === -1 && this.vx > -maxSpd) { this.vx -= accel; if (this.vx < -maxSpd) this.vx = -maxSpd; }
4300	    const vxSign = this.vx > 0 ? 1 : this.vx < 0 ? -1 : 0;
4301	    // 台阶步升（同战士：前方高差 ≤16.1 直接抬升）
4302	    if (this.vy >= 0 && vxSign !== 0) {
4303	      const ax = Math.floor((this.x + this.vx + this.w / 2 + (this.w / 2 + 1) * vxSign) / TILE);
4304	      const fr = Math.floor((this.y + this.h - 1) / TILE);
4305	      if (ax >= 0 && fr >= 2 && ax < st.w && fr < st.h
4306	        && solidAt(ax, fr) && !st.half[st.idx(ax, fr)]
4307	        && !solidAt(ax, fr - 1) && !solidAt(ax, fr - 2) && !solidAt(ax, fr - 3)) {
4308	        const rise = this.y + this.h - fr * TILE;
4309	        if (rise > 0 && rise <= 16.1) this.y = fr * TILE - this.h;
4310	      }
4311	    }
4312	    this.applyGravity(game);
4313	    const xBefore = this.x;
4314	    moveAndCollide(this, game.world, this.vx, this.vy);
4315	    // 怒滚虫 546 追击跳（AI_026 :63012-63017）：落地(vy==0) + |vx|>3 + 朝玩家侧 →
4316	    // vy-=4 + PlaySound(3,11)=NPC_Hit_11（跳沙坑声）
4317	    if (this.vanillaId === 546 && this.vy === 0 && Math.abs(this.vx) > 3 && player
4318	      && ((this.cx < player.cx && this.vx > 0) || (this.cx > player.cx && this.vx < 0))) {
4319	      this.vy -= 4;
4320	      game.playSfxWav?.('NPC_Hit_11', 1, this.cx, this.cy);
4321	    }
4322	    // 卡墙计数（X 未动，原版 position.X == oldPosition.X 判定）
4323	    if (Math.abs(this.x - xBefore) < 0.01) this.stuckT++;
4324	    // 跳梯（前方探测带 5×vx 提前量）
4325	    if (vxSign === dir && vxSign !== 0) {
4326	      const fx = Math.floor((this.x + this.w / 2 + (this.w / 2 + 2) * dir + this.vx * 5) / TILE);
4327	      const fy = Math.floor((this.y + this.h - 15) / TILE);
4328	      if (this.h >= 32 && solidAt(fx, fy - 2)) {
4329	        this.vy = solidAt(fx, fy - 3) ? -8.5 : -7.5;
4330	      } else if (solidAt(fx, fy - 1)) {
4331	        this.vy = -7;
4332	      } else if (this.y + this.h - fy * TILE > 20 && solidAt(fx, fy)) {
4333	        this.vy = -6;
4334	      } else if (!solidAt(fx, fy + 1) && !solidAt(fx + dir, fy + 1) && !solidAt(fx + dir, fy + 2)) {
4335	        this.vy = -8; // 前方悬空（悬崖/沟）大跳
4336	      }
4337	    }
4338	    // 注意：原版 AI_026 无逐帧地面摩擦（速度持续加到 maxSpd，只有逆向阻尼/超速落地衰减）——
4339	    // 不能带 fighterAI 的 onGround *=0.9，否则平衡点被压到 0.63 远低于 6
4340	  }
4341	
4342	  /** AI_014 蝙蝠/飞行族（1.4.5.6 完整反编译 NPC.145.cs:22895+）：
4343	   *  noGravity；撞墙旧速×-0.5 反弹（X 最小弹速朝向 ±2 / Y ±1）；
4344	   *  通用分轴加速 X 0.1/±4、Y 0.04/±1.5（逆转修正 0.05/0.03）；
4345	   *  Giant Bat(158) 0.2/±7；血乌贼(660) X 0.35/±6、Y 0.3/±5。
4346	   *  （1.4.0.5 反编译包 AI() 空壳，此处以 1.4.5.6 源为准——旧编号行为两版未变） */
4347	  private batAI(game: GameHooks, player: Player | null) {
4348	    const oldVx = this.vx, oldVy = this.vy;
4349	    let ax = 0.1, ay = 0.04, cx = 4, cy = 1.5;
4350	    if (this.vanillaId === 158) { ax = 0.2; ay = 0.2; cx = 7; cy = 7; }
4351	    else if (this.vanillaId === 660) { ax = 0.35; ay = 0.3; cx = 6; cy = 5; }
4352	    const vampireBat = this.vanillaId === 158;
4353	    let dirX: number, dirY: number;
4354	    if (player) {
4355	      dirX = player.cx > this.cx ? 1 : -1;
4356	      dirY = player.cy > this.cy ? 1 : -1;
4357	      this.dirY = dirY;   // 持久化:玩家死亡后 TargetClosest 无操作(AI_014 :22943
4358	      // 同款语义)→ 沿用最后垂直方向滑行,而非恒上飞(2026-08-19 修正)
4359	    } else { dirX = this.facing; dirY = this.dirY; }
4360	    // 吸血蝙蝠白天离场（cs:22944-22949）：158 且在地表之上 && 白天 && 非日食 →
4361	    // directionY=-1 上飞、direction 翻转水平远离（曾缺——白天吸血蝙蝠赖场不退）
4362	    if (vampireBat && this.y < game.world.groundLevel * TILE
4363	      && game.world.clock.isDay && !game.world.clock.eclipse) {
4364	      dirY = -1;
4365	      this.dirY = -1;
4366	      dirX = -dirX;
4367	    }
4368	    this.facing = dirX;
4369	    // X 轴（L23314-23345）
4370	    if (dirX === -1 && this.vx > -cx) {
4371	      this.vx -= ax;
4372	      if (this.vx > cx) this.vx -= ax; else if (this.vx > 0) this.vx += ax * 0.5;
4373	      if (this.vx < -cx) this.vx = -cx;
4374	    } else if (dirX === 1 && this.vx < cx) {
4375	      this.vx += ax;
4376	      if (this.vx < -cx) this.vx += ax; else if (this.vx < 0) this.vx -= ax * 0.5;
4377	      if (this.vx > cx) this.vx = cx;
4378	    }
4379	    // Y 轴（L23346-23377）
4380	    if (dirY === -1 && this.vy > -cy) {
4381	      this.vy -= ay;
4382	      if (this.vy > cy) this.vy -= 0.05; else if (this.vy > 0) this.vy += 0.03;
4383	      if (this.vy < -cy) this.vy = -cy;
4384	    } else if (dirY === 1 && this.vy < cy) {
4385	      this.vy += ay;
4386	      if (this.vy < -cy) this.vy += 0.05; else if (this.vy < 0) this.vy -= 0.03;
4387	      if (this.vy > cy) this.vy = cy;
4388	    }
4389	    // ---- wet 浮力（cs:23232-23243 蝙蝠/恶魔/巨狐蝠/孢子蝠族 + cs:23380-23392 哈比 48）：
4390	    // 入水 vy>0 ×0.95、恒 -0.5 上浮、钳 -4 并重新索敌——飞行族扎水后弹出水面而非
4391	    // 照常追击。表外 aiStyle14（158 吸血蝙蝠等）原版无此段
4392	    if (this.wet && this.vanillaId !== null && AI014_SWIM_UP.has(this.vanillaId)) {
4393	      if (this.vy > 0) this.vy *= 0.95;
4394	      this.vy -= 0.5;
4395	      if (this.vy < -4) this.vy = -4;
4396	      if (player) this.facing = this.seekDirX(player);   // TargetClosest
4397	    }
4398	    moveAndCollide(this, game.world, this.vx, this.vy);
4399	    // 撞墙/撞地反弹（L22899-22923：collideX/Y → oldVelocity*-0.5 + 最小弹速）
4400	    if (this.hitWall) {
4401	      this.vx = -oldVx * 0.5;
4402	      if (this.facing === -1 && this.vx > 0 && this.vx < 2) this.vx = 2;
4403	      if (this.facing === 1 && this.vx < 0 && this.vx > -2) this.vx = -2;
4404	    }
4405	    if (this.hitHead || this.onGround) {
4406	      this.vy = -oldVy * 0.5;
4407	      if (this.vy > 0 && this.vy < 1) this.vy = 1;
4408	      if (this.vy < 0 && this.vy > -1) this.vy = -1;
4409	    }
4410	    // ---- 吸血蝙蝠俯袭击变形（cs:23393-23402）：玩家在下方 200px 内且有视线 →
4411	    // 落地化作人形吸血鬼（159，AI_003 战士 + 离远化回）
4412	    if (vampireBat && player && !player.dead) {
4413	      const d = Math.hypot(player.cx - this.cx, player.cy - this.cy);
4414	      if (d < 200 && this.y + this.h < player.y + player.h && this.canSeePlayer(game.world.store, player)) {
4415	        this.tryTransformTo(159, game.world.store, false, game);
4416	      }
4417	    }
4418	    // ---- 飞行射击族（cs:23463-23543，逐发要求视线；轮空后 ai[0] 达随机阈值归零——
4419	    // 阈值缓存 ai[2]）：哈比 48 羽毛 38（30/60/90 连三、速 6、伤 15、±100、归零 400+rand400）/
4420	    // 恶魔 62/66 飞镰 44（20/40/60/80 连四、伤 21、±100、300+rand300；弹速 0.2 起步,
4421	    // AI_018 加速 ×1.06@ai0[30,100) 见 Dart.ts DART_STYLE[44]）/ 红恶魔 156 三叉戟 115
4422	    // （20/40/60/80/100 连五、伤 80、±50、250+rand250；弹速 0.2 起步 AI_027 ×1.125@ai0<30；
4423	    // 出生点沿弹向前移 100px cs:23538-23540）
4424	    const shooter = this.vanillaId === 48
4425	      ? { ticks: [30, 60, 90], spd: 6, dmg: 15, spread: 100, reset: 400, proj: 38, lead: 0 }
4426	      : this.vanillaId === 62 || this.vanillaId === 66
4427	        ? { ticks: [20, 40, 60, 80], spd: 0.2, dmg: 21, spread: 100, reset: 300, proj: 44, lead: 0 }
4428	        : this.vanillaId === 156
4429	          ? { ticks: [20, 40, 60, 80, 100], spd: 0.2, dmg: 80, spread: 50, reset: 250, proj: 115, lead: 100 }
4430	          : null;
4431	    if (shooter && player && !player.dead) {
4432	      if (this.ai0 < 0) this.ai0 = 0; // 类字段默认 -1120 是史莱姆初值；原版 ai[0] 从 0 起步
4433	      this.ai0 += 1;
4434	      if (shooter.ticks.includes(this.ai0)) {
4435	        if (this.canSeePlayer(game.world.store, player)) {
4436	          const ox = player.cx - this.cx + (Math.random() * 2 - 1) * shooter.spread;
4437	          const oy = player.cy - this.cy + (Math.random() * 2 - 1) * shooter.spread;
4438	          const d = Math.hypot(ox, oy) || 1;
4439	          // 出生点沿弹向偏移 lead px（原版 vector25 += dir*100,cs:23538）
4440	          this.shootDart(game, this.cx + (ox / d) * shooter.lead, this.cy + (oy / d) * shooter.lead,
4441	            ox, oy, shooter.spd, shooter.dmg, shooter.proj);
4442	        }
4443	      } else if (this.ai0 > shooter.ticks[shooter.ticks.length - 1]) {
4444	        if (this.ai2 === 0) this.ai2 = shooter.reset + Math.floor(Math.random() * shooter.reset);
4445	        if (this.ai0 >= this.ai2) { this.ai0 = 0; this.ai2 = 0; }
4446	      }
4447	    }
4448	  }
4449	
4450	  /** AI_016 游泳族（1.4.5.6 NPC.145.cs:23549+）：鲨鱼/食人鱼/琵琶鱼等
4451	   *  通用档水中 accel 0.1/0.1、上限 X±3/Y±2（L23883-23897）；Arapaima(157) 0.25/0.2、±7/±4（L23831+）；
4452	   *  撞墙掉头；离水缓慢上浮。螺旋转向/专家模式特化略 */
4453	  private swimAI(game: GameHooks, player: Player | null) {
4454	    const st = game.world.store;
4455	    // wet = 原版 Collision.WetCollision（npcLiquid 每 tick 写；中心小盒判水线，
4456	    // 浅水/贴面与中心格 liquid>80 近似有别——水面行为以此为准）
4457	    const inWater = this.wet;
4458	    const ara = this.vanillaId === 157;
4459	    // ---- 河鲀 688 膨胀（cs:23555-23620）：受击进入膨胀 180t——缓速悬浮贴水面，
4460	    // 期间不吃通用鱼逻辑（简化为阻尼漂浮，贴水线钉法省略）
4461	    if (this.vanillaId === 688) {
4462	      if (this.justHit && this.ai2 === 0) { this.ai2 = 1; this.ai3 = 180; }
4463	      if (this.ai2 === 1) {
4464	        this.vx *= 0.98;
4465	        this.vy = inWater ? Math.max(this.vy - 0.3, -10) : Math.min(this.vy + 0.3, 10);
4466	        this.vy *= 0.98;
4467	        this.ai3 -= 1;
4468	        if (this.ai3 <= 0) this.ai2 = 0;
4469	        moveAndCollide(this, game.world, this.vx, this.vy);
4470	        return;
4471	      }
4472	    }
4473	    // ---- 海豚 615 周期跃出（cs:23629-23747）：每 300-1199t 触发，水中持续上冲
4474	    //  （vy-=0.4 限 -6）出水后抛物线落回
4475	    if (this.vanillaId === 615) {
4476	      if (this.ai2 !== 1) {
4477	        this.ai1 += 1;
4478	        if (this.ai1 >= 300 + Math.random() * 900 && inWater) { this.ai2 = 1; this.ai1 = 0; }
4479	      } else {
4480	        if (inWater) {
4481	          this.vy -= 0.4;
4482	          if (this.vy < -6) this.vy = -6;
4483	          // 跃出叫声（cs:23735-23740）：ai[3] 每 tick +1（≥300 清零回落），
4484	          // ==60 且 1/2 掷 → (45)=Zombie_109 海豚音
4485	          this.ai3 += 1;
4486	          if (this.ai3 >= 300) { this.ai2 = 0; this.ai3 = 0; this.vy = 4; }
4487	          else if (this.ai3 === 60 && Math.floor(Math.random() * 2) === 0) {
4488	            game.playSfxWav?.('Zombie_109', 1, this.cx, this.cy);
4489	          }
4490	        } else {
4491	          this.vy = Math.min(this.vy + 0.3, 10); // 出水抛物线
4492	        }
4493	        if (this.onGround || this.hitWall) this.ai2 = 0;
4494	        moveAndCollide(this, game.world, this.vx, this.vy);
4495	        return;
4496	      }
4497	    }
4498	    if (inWater) {
4499	      // ---- flag22 攻击门（cs:23731-23740）：55 金鱼/592/607 鳉/615 海豚/688 河鲀
4500	      //    五族不索敌（连 TargetClosest 都不调）恒游荡；其余玩家【湿身】+视线
4501	      //    可及才追击。★此前无条件朝玩家全速追（±3/±2）——岸上玩家会把鱼
4502	      //    vy=-2 直拖出水面,出水落岸后无限拍打 = "鱼经常蹦出水面上岸"根因
4503	      //    （2026-08-19 用户报,食人鱼例）
4504	      const noChase = this.vanillaId === 55 || this.vanillaId === 592
4505	        || this.vanillaId === 607 || this.vanillaId === 615 || this.vanillaId === 688;
4506	      const chase = !noChase && !!player && !player.dead
4507	        && player.inWater && this.canSeePlayer(st, player);
4508	      if (chase && player) {
4509	        // 攻击形（cs:23822-23862）：TargetClosest + 分族推进档
4510	        this.facing = this.seekDirX(player);
4511	        const dy = player.cy > this.cy ? 1 : -1;
4512	        if (ara) {
4513	          // 157 巨骨舌鱼（cs:23829-23845）：逆向阻尼 + 0.25/0.2 推进,钳 ±7/±4
4514	          if ((this.vx > 0 && this.facing < 0) || (this.vx < 0 && this.facing > 0)) this.vx *= 0.95;
4515	          this.vx += this.facing * 0.25;
4516	          this.vy += dy * 0.2;
4517	          if (this.vx > 8) this.vx = 7;
4518	          if (this.vx < -8) this.vx = -7;
4519	          if (this.vy > 5) this.vy = 4;
4520	          if (this.vy < -5) this.vy = -4;
4521	        } else if (this.vanillaId === 65 || this.vanillaId === 102 || this.vanillaId === 692) {
4522	          // 鲨鱼/琵琶鱼/虎鲸（cs:23846-23862）：0.15/0.15,钳 ±5/±3
4523	          this.vx += this.facing * 0.15;
4524	          this.vy += dy * 0.15;
4525	          this.vx = Math.max(-5, Math.min(5, this.vx));
4526	          this.vy = Math.max(-3, Math.min(3, this.vy));
4527	        } else {
4528	          // 其余（食人鱼 58 等,cs:23856-23862）：0.1/0.1,钳 ±3/±2
4529	          this.vx += this.facing * 0.1;
4530	          this.vy += dy * 0.1;
4531	          this.vx = Math.max(-3, Math.min(3, this.vx));
4532	          this.vy = Math.max(-2, Math.min(2, this.vy));
4533	        }
4534	      } else {
4535	        // 游荡形（cs:23864-24004）：direction 恒存（撞墙翻,不追玩家）——
4536	        // 水平 vx += dir*0.1 钳 ±1（615 海豚 ±3,cs:23952 num269）；
4537	        // 垂直 ai[0] 慢振荡 ±0.3（cs:23968-23981,0.01 步进）贴水深游
4538	        this.vx += this.facing * 0.1;
4539	        const capX = this.vanillaId === 615 ? 3 : 1;
4540	        if (this.vx < -capX || this.vx > capX) this.vx *= 0.95;
4541	        if (ara) {
4542	          // 157 游荡档（cs:23898-23945）：directionY 取自玩家纵深;ai[0] 振荡阈值
4543	          // ±0.6 随 dirY 偏移（<0→-1/0.2,>0→-0.2/1）,0.02 步进
4544	          this.dirY = player ? (player.cy > this.cy ? 1 : -1) : this.dirY;
4545	          if (this.ai0 === -1) {
4546	            this.vy -= 0.02;
4547	            if (this.vy < (this.dirY < 0 ? -1 : this.dirY > 0 ? -0.2 : -0.6)) this.ai0 = 1;
4548	          } else {
4549	            this.vy += 0.02;
4550	            if (this.vy > (this.dirY < 0 ? 0.2 : this.dirY > 0 ? 1 : 0.6)) this.ai0 = -1;
4551	          }
4552	          this.vx += this.facing * 0.1;   // 157 共 0.2 推进（cs:23919）
4553	          this.vx = Math.max(-2, Math.min(2, this.vx));
4554	        } else {
4555	          if (this.ai0 === -1) {
4556	            this.vy -= 0.01;
4557	            if (this.vy < -0.3) this.ai0 = 1;
4558	          } else {
4559	            this.vy += 0.01;
4560	            if (this.vy > 0.3) this.ai0 = -1;
4561	          }
4562	          // 浅水上升检查（cs:23984-24000）：头顶格 liquid>128 且脚下 1-2 格
4563	          // 有实心 → ai[0]=-1 上浮（浅水贴面巡游,不触底）
4564	          const tx = Math.floor(this.cx / 16), ty = Math.floor((this.y + this.h / 2) / 16);
4565	          if (st.inBounds(tx, ty - 1) && st.liquid[st.idx(tx, ty - 1)] > 128
4566	            && ((st.inBounds(tx, ty + 1) && st.flags[st.idx(tx, ty + 1)])
4567	              || (st.inBounds(tx, ty + 2) && st.flags[st.idx(tx, ty + 2)]))) {
4568	            this.ai0 = -1;
4569	          }
4570	          // 垂直阻尼（cs:24001-24004,157 豁免）：|vy|>0.4 ×0.95
4571	          if (this.vy > 0.4 || this.vy < -0.4) this.vy *= 0.95;
4572	        }
4573	      }
4574	      moveAndCollide(this, game.world, this.vx, this.vy);
4575	      // 撞轴反弹（仅 !chase,cs:23790-23807）：撞墙 vx/朝向双翻;撞顶/底
4576	      // vy 反弹并同步 ai[0] 方向（追击态不吃反弹）
4577	      if (!chase) {
4578	        if (this.hitWall) { this.vx *= -1; this.facing *= -1; }
4579	        if (this.hitHead || this.onGround) {
4580	          if (this.vy > 0) { this.vy = -Math.abs(this.vy); this.ai0 = -1; }
4581	          else if (this.vy < 0) { this.vy = Math.abs(this.vy); this.ai0 = 1; }
4582	        }
4583	      }
4584	    } else {
4585	      // 离水（cs:24019-24034）：vy==0 → 拍打挣扎 vy=rand(-5,-2)/vx=rand(-2,2)
4586	      // （65 食人鱼/692 貌鱼例外：只 ×0.94 阻尼不蹦）；重力 0.3 钳 10
4587	      if (this.vy === 0) {
4588	        if (this.vanillaId === 65 || this.vanillaId === 692) {
4589	          this.vx *= 0.94;
4590	          if (Math.abs(this.vx) < 0.2) this.vx = 0;
4591	        } else {
4592	          this.vy = -5 + Math.random() * 3;   // rand(-50,-20) × 0.1
4593	          this.vx = -2 + Math.random() * 4;   // rand(-20,20) × 0.1
4594	          this.facing = Math.random() < 0.5 ? 1 : -1;   // direction 随机（rotation 基向）
4595	        }
4596	      }
4597	      this.vy = Math.min(this.vy + 0.3, 10);
4598	      moveAndCollide(this, game.world, this.vx, this.vy);
4599	    }
4600	    // ---- 102 灯笼鱼额前小灯（cs:23820-23822）：面朝方向前 (width+8)px、y+2 处
4601	    //  0.07/0.04/0.025 微光（钓竿诱饵）——位置偏移走 lightRGBAt ----
4602	    if (this.vanillaId === 102) {
4603	      this.lightRGB = [0.07, 0.04, 0.025];
4604	      this.lightRGBAt = { x: this.x + this.w / 2 + this.facing * (this.w + 8), y: this.y + 2 };
4605	    }
4606	  }
4607	
4608	  /** AI_018 水母族 1:1（cs:24212-24474）：潜伏（专家）+ 水中追击脉冲 + 上下漂移。
4609	   *  潜伏 lurk（cs:24215-24269，仅专家且 63/64/103/242）：
4610	   *   - ai[1]=1 潜伏中 → dontTakeDamage（不可击）且 AI 提前 return（原地悬浮）；
4611	   *   - 玩家湿身+视线+150px 内：非潜伏 ai[2]+2（提前触发）/潜伏中 ai[2]−0.25（延长）；
4612	   *   - 非潜伏 ai[2]≥420 → 入潜伏（ai[1]=1, ai[2]=0）；潜伏 ai[2]≥120 → 出潜伏；
4613	   *   - 离水 → ai[1]=ai[2]=0（潜伏态清零）。发光 ×1.5（num274）。
4614	   *  水中（cs:24330-24457）：撞轴反弹（collideX/collideY 原文 ± 反转）；玩家湿身+视线
4615	   *   → 攻击形：阻尼（0.98 + 逐族再乘）+ 静止阈值 num277（63/64=0.2、103=0.6、221=1、
4616	   *   242=3）内重定向脉冲 num278（7/103 9）；否则漂移形：vx+=dir×0.02 钳 ±1、
4617	   *   rotation=vx×0.4、ai[0] 上下振荡（0.01 步进 ±1 阈值）+ 液深探测（上格液>128 且
4618	   *   下 1-2 格有实心 → 转向上）。
4619	   *  离水（cs:24459-24474）：rotation+=vx×0.1、vy==0 时 vx 阻尼归零、重力 0.2 钳 10
4620	   *  ——水母离水只坠不蹦（与 aiStyle16 鱼的拍打挣扎不同） */
4621	  private jellyfishAI(game: GameHooks, player: Player | null) {
4622	    const st = game.world.store;
4623	    const vid = this.vanillaId ?? 63;
4624	    const inWater = this.wet;
4625	    // ---- 潜伏态（专家 + 63/64/103/242，cs:24215）----
4626	    const lurkCapable = mainExpertMode(game.world) && (vid === 63 || vid === 64 || vid === 103 || vid === 242);
4627	    let lurking = false;
4628	    if (inWater && this.ai1 === 1) lurking = true;
4629	    else this.dontTakeDamage = false;                     // :24224 else 分支
4630	    const playerWet = !!player && !player.dead && player.inWater;
4631	    const near = !!player && !player.dead && playerWet
4632	      && this.canSeePlayer(st, player)
4633	      && Math.hypot(player.cx - this.cx, player.cy - this.cy) < 150;  // :24229-24236
4634	    if (lurkCapable) {
4635	      if (inWater) {
4636	        if (near) {
4637	          if (this.ai1 === 0) this.ai2 += 2;              // 非潜伏：提前触发
4638	          else this.ai2 -= 0.25;                          // 潜伏中：延长
4639	        }
4640	        if (lurking) {
4641	          this.dontTakeDamage = true;                     // :24247
4642	          this.ai2 += 1;
4643	          if (this.ai2 >= 120) this.ai1 = 0;              // :24252 出潜伏
4644	        } else {
4645	          this.ai2 += 1;
4646	          if (this.ai2 >= 420) { this.ai1 = 1; this.ai2 = 0; }  // :24257 入潜伏
4647	        }
4648	      } else {
4649	        this.ai1 = 0; this.ai2 = 0;                       // :24262 离水清零
4650	      }
4651	      lurking = inWater && this.ai1 === 1;
4652	    }
4653	    // ---- 发光（cs:24272-24290，num274 = 1 + 潜伏 0.5）----
4654	    const lum = lurking ? 1.5 : 1;
4655	    if (vid === 63) this.lightRGB = [0.05 * lum, 0.15 * lum, 0.4 * lum];
4656	    else if (vid === 103) this.lightRGB = [0.05 * lum, 0.45 * lum, 0.1 * lum];
4657	    else if (vid !== 221 && vid !== 242) this.lightRGB = [0.35 * lum, 0.05 * lum, 0.2 * lum];
4658	    // ---- 潜伏中：原地悬浮（AI 提前 return，velocity 保持 → 缓漂）----
4659	    if (lurking) return;
4660	    if (inWater) {
4661	      // 撞轴反弹（cs:24333-24363：collideX/collideY 原速反转；坡面翻转由
4662	      // moveAndCollide 的 slopeCollide 承担，方向翻转近似）
4663	      if (this.hitWall) { this.vx *= -1; this.facing *= -1; }
4664	      if (this.onGround) { if (this.vy > 0) { this.vy = -Math.abs(this.vy); this.ai0 = -1; } }
4665	      else if (this.hitHead) { if (this.vy < 0) { this.vy = Math.abs(this.vy); this.ai0 = 1; } }
4666	      // 玩家湿身 + 视线 → 攻击形（cs:24366-24420 flag24）
4667	      if (playerWet && player && this.canSeePlayer(st, player)) {
4668	        let damp = 0.98;
4669	        let still = 0.2;                                   // num277：静止阈值
4670	        if (vid === 103) { damp *= 0.98; still = 0.6; }
4671	        if (vid === 221) { damp *= 0.99; still = 1; }
4672	        if (vid === 242) { damp *= 0.995; still = 3; }
4673	        this.visAngle = Math.atan2(this.vy, this.vx) + Math.PI / 2;
4674	        this.vx *= damp; this.vy *= damp;
4675	        if (Math.abs(this.vx) < still && Math.abs(this.vy) < still) {
4676	          if (player) {
4677	            this.facing = this.seekDirX(player);          // TargetClosest
4678	            const spd = vid === 103 ? 9 : 7;              // num278
4679	            const dx = player.cx - this.cx, dy = player.cy - this.cy;
4680	            const d = Math.hypot(dx, dy) || 1;
4681	            this.vx = (dx / d) * spd;
4682	            this.vy = (dy / d) * spd;
4683	          }
4684	        }
4685	        moveAndCollide(this, game.world, this.vx, this.vy);
4686	        return;
4687	      }
4688	      // 漂移形（cs:24421-24457）
4689	      this.vx += this.facing * 0.02;
4690	      this.visAngle = this.vx * 0.4;
4691	      if (this.vx < -1 || this.vx > 1) this.vx *= 0.95;
4692	      if (this.ai0 === -1) {
4693	        this.vy -= 0.01;
4694	        if (this.vy < -1) this.ai0 = 1;
4695	      } else {
4696	        this.vy += 0.01;
4697	        if (this.vy > 1) this.ai0 = -1;
4698	      }
4699	      // 液深探测（cs:24440-24455）：中心上格液>128 且下 1-2 格实心 → 转向上
4700	      const cx = Math.floor(this.cx / TILE), cy = Math.floor(this.cy / TILE);
4701	      if (st.inBounds(cx, cy) && st.liquid[st.idx(cx, cy - 1)] > 128) {
4702	        if ((st.inBounds(cx, cy + 1) && st.isActive(cx, cy + 1))
4703	          || (st.inBounds(cx, cy + 2) && st.isActive(cx, cy + 2))) this.ai0 = -1;
4704	      } else {
4705	        this.ai0 = 1;
4706	      }
4707	      if (this.vy > 1.2 || this.vy < -1.2) this.vy *= 0.99;
4708	      if (this.facing === 0) this.facing = player && player.cx > this.cx ? 1 : -1;
4709	      moveAndCollide(this, game.world, this.vx, this.vy);
4710	      return;
4711	    }
4712	    // ---- 离水（cs:24459-24474）----
4713	    this.visAngle += this.vx * 0.1;
4714	    if (this.vy === 0) {
4715	      this.vx *= 0.98;
4716	      if (Math.abs(this.vx) < 0.01) this.vx = 0;
4717	    }
4718	    this.vy = Math.min(this.vy + 0.2, 10);
4719	    this.ai0 = 1;
4720	    moveAndCollide(this, game.world, this.vx, this.vy);
4721	  }
4722	
4723	  /** AI_022 幽灵族（NPC.145.cs:24726+）：穿墙缓速追击
4724	   *  目标速度 = 归一化方向×7（num312），Lerp 系数 0.0125（num317）——飘忽逼近的手感 */
4725	  private ghostAI(game: GameHooks, player: Player | null) {
4726	    // ---- 点光（cs:24858-24860 蜗牛怪 / cs:24934-24936 冰雪元素，Center，恒亮）----
4727	    if (this.vanillaId === 122) this.lightRGB = [0.4, 0, 0.25];
4728	    else if (this.vanillaId === 169) this.lightRGB = [0, 0.6, 0.75];
4729	    // 小精灵 75 环境声（cs:24928）：1/40 掷 → PlaySound(27)=Pixie.wav（闪烁伴随 55 尘
4730	    //   1/6 已在通用尘段;音频在 type==75 专属块）
4731	    if (this.vanillaId === 75 && Math.floor(Math.random() * 40) === 0) {
4732	      game.playSfxWav?.('Pixie', 1, this.cx, this.cy);
4733	    }
4734	    // 幽灵 316 消散（cs:24750-24758）：ai[3]==1 首帧 → NPCDeath55
4735	    if (this.vanillaId === 316 && this.ai3 === 1 && !(this as unknown as { _g316snd?: boolean })._g316snd) {
4736	      (this as unknown as { _g316snd?: boolean })._g316snd = true;
4737	      game.playSfxFiles?.(['NPC_Killed_55'], 1, this.cx, this.cy);
4738	    }
4739	    if (!player) { this.vx *= 0.95; this.vy *= 0.95; return; }
4740	    const dx = player.cx - this.cx, dy = player.cy - this.cy;
4741	    const d = Math.hypot(dx, dy) || 1;
4742	    this.vx += ((dx / d) * 7 - this.vx) * 0.0125;
4743	    this.vy += ((dy / d) * 7 - this.vy) * 0.0125;
4744	    this.facing = this.vx > 0 ? 1 : -1;
4745	    // ---- 漂浮射击三族（cs:24854-25048）----
4746	    // 蜗牛怪 122 粉激光 / 冰雪元素 169 霜爆：同一充能机——待机计数(localAI[1]→ai[2])
4747	    // >120 且有视线 → 充能(ai[3]=1)；充能中出射程即取消、满 64 归零；受击清空；
4748	    // 122 在 ai[3]==32 发射（速 7、伤 25、射程 700、RotatedByRandom(0.0785) 微散布），
4749	    // 169 在 ai[3]==16 发射（速 5、伤 45）
4750	    // 脓水粘怪 268 金雨：ai[3] 每 tick +1（受击置 -45），≥60+rand(60) 且有视线 →
4751	    // 喷（速 10、伤 40、|dx|×0.1 下坠补偿、枪口 (cx-4, y+h×0.7)、散布 x±10/y-30..20）
4752	    const st = game.world.store;
4753	    if (this.vanillaId === 122 || this.vanillaId === 169) {
4754	      const fireAt = this.vanillaId === 122 ? 32 : 16;
4755	      if (this.iframes > 0 && this.iframes % 4 === 0) { this.ai3 = 0; this.ai2 = 0; } // justHit 清充能
4756	      if (this.ai3 === fireAt && d < 700) {
4757	        const spd = this.vanillaId === 122 ? 7 : 5;
4758	        const dmg = this.vanillaId === 122 ? 25 : 45;

```


---

## 🤖 Assistant · 2026-08-19T03:10:12.714Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I've now read batAI, swimAI, jellyfishAI, ghostAI. Let me now check the vanilla AI_018 jellyfish section (cs:24210-24465) to compare against ours. Also AI_014 bat family (cs:22895-23543) for the harpy 48 / 158 / 660 exclusive branches. Also the demon family — wait, the demon 62/66 shooting is in our batAI (shooter table line 4424-4430)! Vanilla: harpy 48 feathers, demon 62/66 scythes, red devil 156 tridents — these are all in aiStyle 14 (bat AI). Interesting. So demons (62? no wait — 62 is "Demon"? Hmm: 62 = "Demon"? Let me check: NPC 62 = Demon, 66 = Voodoo Demon, 156 = Red Devil. And "火小鬼 24?" — Fire Imp NPC 24? Hmm no, Fire Imp = 24? Actually Fire Imp is NPC 24? Hmm — Fire Imp is 24? Let me check: Terraria: 23 = "Imp"? no... Let me grep our data for names.

Actually the vanilla AI_004 (aiStyle 4) at cs:19909 — let me read it. aiStyle 4 is Eye of Cthulhu only? The task says "恶魔/小鬼族(AI_004 恶魔 66/火小鬼 24?核 aiStyle 归属)". Hmm — but from our code, demons 62/66 are handled in batAI (aiStyle 14). In vanilla, Demon aiStyle = 14? Hmm wait, really? Let me check: In Terraria, Demon's aiStyle... I actually believe Demon is aiStyle 14 (Flying). Hmm, no wait — I recall Demon is aiStyle 4? Let me check SetDefaults in vanilla. Actually the Demon shoots scythes while flying — the code at cs:23463-23543 (in aiStyle 14) covers shooting types. Let me verify demon 62/66 are aiStyle 14 in vanilla.

Also Fire Imp (24?) — Fire Imp NPC id is 24? Terraria: 24 = "Burning Spirit"? Hmm no. Fire Imp = 24? Actually I'm quite sure Fire Imp is NPC 24? Hmm: 23 = "Demon Eye"? no, demon eye is 191... ugh.

Terraria NPC IDs: 1 Demon Eye? No... Let me recall properly: 1 = Green Slime? no, -28? Bah. Actual IDs: 
- 1: Blue Slime? Hmm no, I think 1 = "Slime"? 
Let me just grep our own game data (vanilla.json has names).

Fire Imp: In Terraria, Fire Imp has aiStyle 4? No — Fire Imp uses aiStyle 4? Hmm, Fire Imp teleports and shoots fireballs — that's the caster AI (aiStyle 8)! Actually no — Fire Imp (NPC 24?) teleports like a caster and shoots three fireballs. Yes, Fire Imp uses "aiStyle 8"? Hmm, but caster 8 covers Tim, Dark Caster, Goblin Sorcerer, Fire Imp? Hmm — actually I'm fairly sure Fire Imp is in the caster AI family (aiStyle 8) — "FireImp" NPC id 24? Hmm.

Wait the task says "火小鬼 24?" with a question mark — uncertain. Fire Imp's actual NPC id is 24? Let me check our data: grep '"Fire Imp"' or aiStyle in vanilla.json.

Actually, Demon NPC id: 62? Hmm no! 62 = "Man Eater"? Ugh. Let me settle this by grepping our data files.

Also need to check: AI_004 at cs:19909 — what types use aiStyle 4? EoC (4) and Servant? no. In vanilla: aiStyle 4 = "Eye of Cthulhu" only for npc 4? Also "Demon" might be aiStyle 4! Because AI_004 in vanilla is named... hmm the vanilla source at 19909: `if (aiStyle == 4)` — let me read that block. It handles Demon 62? Wait our comment at case 4 says "AI_004 克苏鲁之眼（NPC.cs:19909）". Let me read vanilla cs:19909-20758 to see what's in there — maybe it includes type 62 demon (flying demon with scythe shots IS aiStyle 4? no...).

Hold on — I recall now: vanilla AI_004 block at 19909 is huge (19909-20758) and includes Demon! Yes! The aiStyle 4 block includes: general floating eye movement + type-specific: Demon (62), Voodoo Demon (66), Red Devil (156), and also "Fire Imp" (24)? Hmm... Actually wait — I remember the "aiStyle 4" handles npc.type 4 (EoC), 62 (Demon), 66 (Voodoo Demon), 156 (Red Devil)? And the scythe shooting is at the end of that block. Hmm, but our batAI has the demon shooting table at cs:23463-23543 which is within aiStyle 14 (22895-23543). 23463 < 23543 so it's inside aiStyle 14. So demons are aiStyle 14 in 1.4.5.6? 

Hmm wait, maybe demons are aiStyle 14. Let me verify with SetDefaults. Let me grep "npc.aiStyle = 4" or rather find type 62's aiStyle assignment. In the decompiled source, SetDefaults has a big switch on type. Let me grep for "case 62:" near aiStyle.

Let me also read AI_004 block fully (19909-20759) — it's 850 lines; the EoC core. The task item says "恶魔/小鬼族(AI_004 恶魔 66/火小鬼 24?核 aiStyle 归属;水母外的 aiStyle 4/14 专属分支)" — so my job: determine aiStyle ownership of Demon 66 / Fire Imp 24, and audit the aiStyle 4 and 14 type-specific branches (excluding jellyfish-related and the already-audited batAI main body + 158/660 which I audit).

So let me:
1. Read vanilla aiStyle 4 block (cs:19909-20758) to enumerate type-specific branches.
2. Check SetDefaults aiStyle for types 24, 62, 66, 156, 48, 158, 660, 205, 252, 23.

Then compare with our eocAI (6886+) and batAI.

Let me first read the vanilla aiStyle 4 block.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:12.852Z · glm-x-preview-260804

```
现在我来读取原版 `aiStyle 4` 代码块以及 `aiStyle 14` (蝙蝠) 代码块。
```


---

## 🤖 Assistant · 2026-08-19T03:10:13.132Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 19909,20100p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 4 block start"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:13.166Z

**📎 ToolResult**

```
		if (aiStyle == 4)
		{
			bool flag2 = false;
			if (Main.expertMode && (double)life < (double)lifeMax * 0.12)
			{
				flag2 = true;
			}
			bool flag3 = false;
			if (Main.expertMode && (double)life < (double)lifeMax * 0.04)
			{
				flag3 = true;
			}
			float num4 = 20f;
			if (flag3)
			{
				num4 = 10f;
			}
			if (target < 0 || target == 255 || Main.player[target].dead || !Main.player[target].active)
			{
				TargetClosest();
			}
			bool dead = Main.player[target].dead;
			float num5 = position.X + (float)(width / 2) - Main.player[target].position.X - (float)(Main.player[target].width / 2);
			float num6 = position.Y + (float)height - 59f - Main.player[target].position.Y - (float)(Main.player[target].height / 2);
			float num7 = (float)Math.Atan2(num6, num5) + 1.57f;
			if (num7 < 0f)
			{
				num7 += 6.283f;
			}
			else if ((double)num7 > 6.283)
			{
				num7 -= 6.283f;
			}
			float num8 = 0f;
			if (this.ai[0] == 0f && this.ai[1] == 0f)
			{
				num8 = 0.02f;
			}
			if (this.ai[0] == 0f && this.ai[1] == 2f && this.ai[2] > 40f)
			{
				num8 = 0.05f;
			}
			if (this.ai[0] == 3f && this.ai[1] == 0f)
			{
				num8 = 0.05f;
			}
			if (this.ai[0] == 3f && this.ai[1] == 2f && this.ai[2] > 40f)
			{
				num8 = 0.08f;
			}
			if (this.ai[0] == 3f && this.ai[1] == 4f && this.ai[2] > num4)
			{
				num8 = 0.15f;
			}
			if (this.ai[0] == 3f && this.ai[1] == 5f)
			{
				num8 = 0.05f;
			}
			if (Main.expertMode)
			{
				num8 *= 1.5f;
			}
			if (flag3 && Main.expertMode)
			{
				num8 = 0f;
			}
			if (rotation < num7)
			{
				if ((double)(num7 - rotation) > 3.1415)
				{
					rotation -= num8;
				}
				else
				{
					rotation += num8;
				}
			}
			else if (rotation > num7)
			{
				if ((double)(rotation - num7) > 3.1415)
				{
					rotation += num8;
				}
				else
				{
					rotation -= num8;
				}
			}
			if (rotation > num7 - num8 && rotation < num7 + num8)
			{
				rotation = num7;
			}
			if (rotation < 0f)
			{
				rotation += 6.283f;
			}
			else if ((double)rotation > 6.283)
			{
				rotation -= 6.283f;
			}
			if (rotation > num7 - num8 && rotation < num7 + num8)
			{
				rotation = num7;
			}
			if (Main.rand.Next(5) == 0)
			{
				int num9 = Dust.NewDust(new Vector2(position.X, position.Y + (float)height * 0.25f), width, (int)((float)height * 0.5f), 5, velocity.X, 2f);
				Main.dust[num9].velocity.X *= 0.5f;
				Main.dust[num9].velocity.Y *= 0.1f;
			}
			reflectsProjectiles = false;
			if (Main.IsItDay() || dead)
			{
				velocity.Y -= 0.04f;
				EncourageDespawn(10);
				return;
			}
			if (this.ai[0] == 0f)
			{
				if (this.ai[1] == 0f)
				{
					float num10 = 5f;
					float num11 = 0.04f;
					if (Main.expertMode)
					{
						num11 = 0.15f;
						num10 = 7f;
					}
					if (Main.getGoodWorld)
					{
						num11 += 0.05f;
						num10 += 1f;
					}
					Vector2 vector = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
					float num12 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector.X;
					float num13 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - 200f - vector.Y;
					float num14 = (float)Math.Sqrt(num12 * num12 + num13 * num13);
					float num15 = num14;
					num14 = num10 / num14;
					num12 *= num14;
					num13 *= num14;
					if (velocity.X < num12)
					{
						velocity.X += num11;
						if (velocity.X < 0f && num12 > 0f)
						{
							velocity.X += num11;
						}
					}
					else if (velocity.X > num12)
					{
						velocity.X -= num11;
						if (velocity.X > 0f && num12 < 0f)
						{
							velocity.X -= num11;
						}
					}
					if (velocity.Y < num13)
					{
						velocity.Y += num11;
						if (velocity.Y < 0f && num13 > 0f)
						{
							velocity.Y += num11;
						}
					}
					else if (velocity.Y > num13)
					{
						velocity.Y -= num11;
						if (velocity.Y > 0f && num13 < 0f)
						{
							velocity.Y -= num11;
						}
					}
					this.ai[2] += 1f;
					float num16 = 600f;
					if (Main.expertMode)
					{
						num16 *= 0.35f;
					}
					if (this.ai[2] >= num16)
					{
						this.ai[1] = 1f;
						this.ai[2] = 0f;
						this.ai[3] = 0f;
						target = 255;
						netUpdate = true;
					}
					else if ((position.Y + (float)height < Main.player[target].position.Y && num15 < 500f) || (Main.expertMode && num15 < 500f))
					{
						if (!Main.player[target].dead)
						{
							this.ai[3] += 1f;

```


---

## 🤖 Assistant · 2026-08-19T03:10:18.664Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is the EoC core (aiStyle 4). Our eocAI is at Enemy.ts:6886. The EoC core was covered in memory (boss audit prehardmode "克眼专家状态机"). The task says EoC itself is out (already audited in boss-audit-prehardmode-2026-08-13). The aiStyle 4 exclusive branches I need: demon family. Let me check what type-specific branches exist inside aiStyle 4 block — grep for "type ==" within 19909-20758.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:19.419Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 19909,20758p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"type ==\\|npc\\.type\\|aiStyle\" | head -40",
 "description": "Find type-specific branches inside aiStyle 4 block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:19.460Z

**📎 ToolResult**

```
1:		if (aiStyle == 4)

```


---

## 🤖 Assistant · 2026-08-19T03:10:20.646Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"NPCID.Demon\\|NPCID.FireImp\\|case 62:\\|case 66:\\|case 24:\\|case 48:\\|case 158:\\|case 660:\\|case 205:\\|case 252:\\|case 23:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -30",
 "description": "Find SetDefaults cases for demon family types"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:20.685Z

**📎 ToolResult**

```
74256:		case 252:
74585:		case 62:
74586:		case 66:
74693:		case 23:
74703:		case 660:
75487:		case 158:
75522:		case 48:
75635:		case 205:
77681:		case 24:
79119:		case 252:
79613:			case 24:
79622:			case 23:

```


---

## 🤖 Assistant · 2026-08-19T03:10:23.539Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The aiStyle 4 block has NO type-specific branches — it's purely the Eye of Cthulhu. So demons are NOT aiStyle 4. Let me check SetDefaults for these cases to see aiStyle values.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:25.130Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for ln in 74256 74585 74693 74703 75487 75522 75635 77681; do echo \"=== line $ln ===\"; sed -n \"${ln},$((ln+42))p\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -m4 \"aiStyle\\|displayName\\|SetDefaults\\|netID\"; done",
 "description": "Check aiStyle assignments for types 252/62/66/23/660/158/48/205/24"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:25.259Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
=== line 74256 ===
=== line 74585 ===
=== line 74693 ===
=== line 74703 ===
=== line 75487 ===
=== line 75522 ===
=== line 75635 ===
=== line 77681 ===

```


---

## 🤖 Assistant · 2026-08-19T03:10:35.640Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 74580,74600p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; sed -n 74700,74712p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; sed -n 75485,75500p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; sed -n 75520,75540p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; sed -n 77678,77700p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ---; sed -n 75633,75645p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read SetDefaults context for demon family NPC types"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:35.739Z

**📎 ToolResult**

```
				{
					frame.Y = num * 11;
				}
			}
			break;
		case 62:
		case 66:
		{
			spriteDirection = direction;
			rotation = velocity.X * 0.1f;
			int num5 = 5;
			int num6 = 5;
			frameCounter += 1.0;
			if (frameCounter >= (double)(num5 * num6))
			{
				frameCounter = 0.0;
			}
			int num7 = (int)(frameCounter / (double)num5);
			frame.Y = num7 * num;
			break;
		}
---
		case 194:
		case 317:
		case 318:
		case 660:
		{
			if (type == 23)
			{
				int num137 = Dust.NewDust(new Vector2(position.X - velocity.X, position.Y - velocity.Y), width, height, 6, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 2f);
				Main.dust[num137].noGravity = true;
				Main.dust[num137].velocity.X *= 0.3f;
				Main.dust[num137].velocity.Y *= 0.3f;
			}
			if ((type == 121 || type == 660) && localAI[0] == 0f)
---
		case 151:
		case 152:
		case 158:
		case 226:
			if (type == 151)
			{
				int num12 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 2f);
				Main.dust[num12].noGravity = true;
			}
			if (type == 150 && Main.rand.Next(10) == 0)
			{
				int num13 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 67, velocity.X * 0.5f, velocity.Y * 0.5f, 90, default(Color), 1.5f);
				Main.dust[num13].noGravity = true;
				Dust dust = Main.dust[num13];
				dust.velocity *= 0.2f;
				Main.dust[num13].noLight = true;
---
			}
			break;
		case 48:
		case 49:
		case 51:
		case 60:
		case 82:
		case 93:
		case 137:
		case 182:
		case 210:
		case 211:
		case 253:
		case 316:
		case 634:
		case 662:
		case 664:
		{
			if (type == 60)
			{
				int num302 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 2f);
---
				frame.Y = 0;
			}
			break;
		case 24:
		{
			if (velocity.Y == 0f)
			{
				spriteDirection = direction;
			}
			int num117 = 5;
			if (ai[1] > 0f)
			{
				if (frame.Y < num * 4 || frame.Y > num * 9)
				{
					frameCounter = 0.0;
					frame.Y = num * 4;
				}
				frameCounter++;
				if (frameCounter > (double)num117)
				{
					frameCounter = 0.0;
					frame.Y += num;
				}
---
			}
			break;
		case 205:
			frameCounter += 0.5;
			if (frameCounter < 2.0)
			{
				frame.Y = 0;
			}
			else if (frameCounter < 4.0)
			{
				frame.Y = num;
			}
			else if (frameCounter < 6.0)

```


---

## 🤖 Assistant · 2026-08-19T03:10:48.341Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
These are FindFrame cases, not SetDefaults. The SetDefaults is elsewhere. Let me grep for "SetDefaults" switch with `npcType` param, e.g. "public void SetDefaults(int Type". Let me find aiStyle assignments per type — in decompiled code it might be in a different file (NPCSetDefaults or similar). Let me check what's in the Terraria folder.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:49.183Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | head -50; grep -rn \"aiStyle = 4;\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "List Terraria decompiled files and find aiStyle=4 assignments"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:49.222Z

**📎 ToolResult**

```
AdvancedPopupRequest.cs
Animation.cs
BitsByte.cs
Chest.cs
Cloud.cs
Collision.cs
CombatText.cs
Control.cs
DelegateMethods.cs
Dust.cs
Entity.cs
EquipmentLoadout.cs
FocusHelper.cs
FrameSkipTest.cs
Framing.cs
GetItemSettings.cs
Gore.cs
HitTile.cs
IEntitySourceTarget.cs
IngameOptions.cs
InitData.cs
Item.cs
ItemSerializationContext.cs
Lang.cs
Lighting.cs
Liquid.cs
LiquidBuffer.cs
MacLaunch.cs
Main.cs
MapRenderer.cs
MessageBuffer.cs
Minecart.cs
Mount.cs
NetMessage.cs
Netplay.cs
NewProjectileModifier.cs
NewProjectileModifiers.cs
NPC.cs
NPCSpawningFlagsForDualDungeons.cs
NPCSpawnParams.cs
PartyHatColor.cs
Player.cs
PlayerSpawnContext.cs
PopupText.cs
PopupTextContext.cs
Program.cs
Projectile.cs
Rain.cs
Recipe.cs
RecipeGroup.cs
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:8639:			aiStyle = 4;

```


---

## 🤖 Assistant · 2026-08-19T03:10:58.990Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"void SetDefaults\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; sed -n 8600,8660p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Locate SetDefaults and inspect context around aiStyle=4"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:59.030Z

**📎 ToolResult**

```
7633:	private void SetDefaultsFromNetId(int id, NPCSpawnParams spawnparams = default(NPCSpawnParams))
8327:	public void SetDefaults_ForNetId(int Type, NPCSpawnParams spawnparams, float scaleOverride)
8361:	public void SetDefaults(int Type, NPCSpawnParams spawnparams = default(NPCSpawnParams))
			aiStyle = 3;
			damage = 13;
			defense = 8;
			lifeMax = 45;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath2;
			knockBackResist = 0.45f;
			value = 80f;
		}
		else if (type == 435)
		{
			width = 18;
			height = 40;
			aiStyle = 3;
			damage = 16;
			defense = 4;
			lifeMax = 45;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath2;
			knockBackResist = 0.55f;
			value = 70f;
		}
		else if (type == 436)
		{
			width = 18;
			height = 40;
			aiStyle = 3;
			damage = 12;
			defense = 4;
			lifeMax = 38;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath2;
			knockBackResist = 0.6f;
			value = 65f;
		}
		else if (type == 4)
		{
			width = 100;
			height = 110;
			aiStyle = 4;
			damage = 15;
			defense = 12;
			lifeMax = 2800;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath1;
			knockBackResist = 0f;
			noGravity = true;
			noTileCollide = true;
			boss = true;
			value = 30000f;
			npcSlots = 5f;
		}
		else if (type == 5)
		{
			width = 20;
			height = 20;
			aiStyle = 5;
			damage = 12;
			defense = 0;
			lifeMax = 8;
			HitSound = SoundID.NPCHit1;

```


---

## 🤖 Assistant · 2026-08-19T03:11:03.771Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Only type 4 uses aiStyle 4. Let me confirm demon 62/66, fire imp 24, harpy 48, 158, 660 aiStyles. Let me grep in SetDefaults for `type == 62`, `type == 24`, `type == 48`, `type == 158`, `type == 660`, `type == 205`, `type == 252`, `type == 23`.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:06.231Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=7633 && NR<=56000' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"else if (type == \\(62\\|66\\|24\\|48\\|158\\|660\\|205\\|252\\|23\\|42\\|620\\))\" | while IFS=: read off rest; do ln=$((off+7632)); echo \"=== $ln: $rest\"; sed -n \"${ln},$((ln+8))p\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -m1 \"aiStyle\"; done",
 "description": "Find aiStyle for types 62/66/24/48/158/660/205/252/23/42/620"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:06.459Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
=== 8995: 		else if (type == 23)
			aiStyle = 5;
=== 9010: 		else if (type == 24)
			aiStyle = 8;
=== 9211: 		else if (type == 42)
			aiStyle = 5;
=== 9292: 		else if (type == 48)
			aiStyle = 14;
=== 9499: 		else if (type == 62)
			aiStyle = 14;
=== 9556: 		else if (type == 66)
			aiStyle = 14;
=== 11557: 		else if (type == 205)
			aiStyle = 5;
=== 12180: 		else if (type == 252)
			aiStyle = 5;
=== 15397: 		else if (type == 158)
			aiStyle = 14;
=== 16884: 		else if (type == 620)
			aiStyle = 107;
=== 17273: 		else if (type == 660)
			aiStyle = 14;
=== 21131: 				else if (type == 24)
=== 23084: 			else if (type == 660)
=== 50707: 		else if (type == 252)
=== 50743: 		else if (type == 205)
=== 50753: 		else if (type == 23)

```


---

## 🤖 Assistant · 2026-08-19T03:11:17.473Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed:
- type 23: aiStyle 5 (swarmer) — what is type 23? Let me find its name. Probably "Cave Bat"? no. Let me grep nearby lines. Actually type 23... let me check around line 8995.
- type 24 (Fire Imp): aiStyle 8 (caster) — so Fire Imp is casterAI in our code (case 8 → casterAI). Task said "火小鬼 24?" — so it's caster family; likely already covered by the casterAI implementation. But the fire imp has special branches inside AI_008? Memory notes "caster12ids重做(ai0=500/==25发射)". I can do a quick check of AI_008's type-24 branches vs our casterAI... but caster AI is not in my assigned families explicitly — "水母外的 aiStyle 4/14 专属分支" was the parenthetical, i.e. aiStyle 4/14 exclusive branches beyond jellyfish. Fire imp being aiStyle 8 means it's out of my listed scope but it was explicitly questioned ("火小鬼 24?核 aiStyle 归属") — I should resolve the ownership question: Fire Imp = aiStyle 8 caster, handled by our casterAI (case 8). I can spot-check the type-24 branch of AI_008 vs our casterAI briefly.
- 62/66 (Demon/Voodoo Demon): aiStyle 14 (bat family). Handled by our batAI — demon shooting table present. Good.
- 48 (Harpy): aiStyle 14 → our batAI shooter table. 
- 158: aiStyle 14, 660: aiStyle 14 → our batAI has special params (158: 0.2/0.2 ±7/7; 660: 0.35/0.3 ±6/5).
- 205: aiStyle 5 → our swarmerAI (Slimer? type 205 = "Slimer"? hmm; actually 205 might be "Iceling"? whatever — the wet branch exists).
- 252: aiStyle 5 → our swarmerAI. Type 252 = "Floaty Gross"? Let me check name around 12180. Actually not critical.
- 620: aiStyle 107 with special branch → our chargerAI(620).

Now let me read the vanilla aiStyle 14 block (cs:22895-23543) completely to compare batAI including 158/660/harpy 48/demons.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:18.005Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 22895,23320p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 14 bat block part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:18.029Z

**📎 ToolResult**

```
		if (aiStyle == 14)
		{
			noGravity = true;
			if (collideX)
			{
				velocity.X = oldVelocity.X * -0.5f;
				if (direction == -1 && velocity.X > 0f && velocity.X < 2f)
				{
					velocity.X = 2f;
				}
				if (direction == 1 && velocity.X < 0f && velocity.X > -2f)
				{
					velocity.X = -2f;
				}
			}
			if (collideY)
			{
				velocity.Y = oldVelocity.Y * -0.5f;
				if (velocity.Y > 0f && velocity.Y < 1f)
				{
					velocity.Y = 1f;
				}
				if (velocity.Y < 0f && velocity.Y > -1f)
				{
					velocity.Y = -1f;
				}
			}
			if (type == 226)
			{
				int num228 = 1;
				int num229 = 1;
				if (velocity.X < 0f)
				{
					num228 = -1;
				}
				if (velocity.Y < 0f)
				{
					num229 = -1;
				}
				TargetClosest();
				if (!Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
				{
					direction = num228;
					directionY = num229;
				}
			}
			else
			{
				TargetClosest();
			}
			if (type == 158)
			{
				if ((double)position.Y < Main.worldSurface * 16.0 && Main.IsItDay() && !Main.eclipse)
				{
					directionY = -1;
					direction *= -1;
				}
				if (direction == -1 && velocity.X > -7f)
				{
					velocity.X -= 0.2f;
					if (velocity.X > 4f)
					{
						velocity.X -= 0.1f;
					}
					else if (velocity.X > 0f)
					{
						velocity.X += 0.05f;
					}
					if (velocity.X < -7f)
					{
						velocity.X = -7f;
					}
				}
				else if (direction == 1 && velocity.X < 7f)
				{
					velocity.X += 0.2f;
					if (velocity.X < -4f)
					{
						velocity.X += 0.1f;
					}
					else if (velocity.X < 0f)
					{
						velocity.X -= 0.05f;
					}
					if (velocity.X > 7f)
					{
						velocity.X = 7f;
					}
				}
				if (directionY == -1 && velocity.Y > -7f)
				{
					velocity.Y -= 0.2f;
					if (velocity.Y > 4f)
					{
						velocity.Y -= 0.1f;
					}
					else if (velocity.Y > 0f)
					{
						velocity.Y += 0.05f;
					}
					if (velocity.Y < -7f)
					{
						velocity.Y = -7f;
					}
				}
				else if (directionY == 1 && velocity.Y < 7f)
				{
					velocity.Y += 0.2f;
					if (velocity.Y < -4f)
					{
						velocity.Y += 0.1f;
					}
					else if (velocity.Y < 0f)
					{
						velocity.Y -= 0.05f;
					}
					if (velocity.Y > 7f)
					{
						velocity.Y = 7f;
					}
				}
			}
			else if (type == 226)
			{
				if (direction == -1 && velocity.X > -4f)
				{
					velocity.X -= 0.2f;
					if (velocity.X > 4f)
					{
						velocity.X -= 0.1f;
					}
					else if (velocity.X > 0f)
					{
						velocity.X += 0.05f;
					}
					if (velocity.X < -4f)
					{
						velocity.X = -4f;
					}
				}
				else if (direction == 1 && velocity.X < 4f)
				{
					velocity.X += 0.2f;
					if (velocity.X < -4f)
					{
						velocity.X += 0.1f;
					}
					else if (velocity.X < 0f)
					{
						velocity.X -= 0.05f;
					}
					if (velocity.X > 4f)
					{
						velocity.X = 4f;
					}
				}
				if (directionY == -1 && (double)velocity.Y > -2.5)
				{
					velocity.Y -= 0.1f;
					if ((double)velocity.Y > 2.5)
					{
						velocity.Y -= 0.05f;
					}
					else if (velocity.Y > 0f)
					{
						velocity.Y += 0.03f;
					}
					if ((double)velocity.Y < -2.5)
					{
						velocity.Y = -2.5f;
					}
				}
				else if (directionY == 1 && (double)velocity.Y < 2.5)
				{
					velocity.Y += 0.1f;
					if ((double)velocity.Y < -2.5)
					{
						velocity.Y += 0.05f;
					}
					else if (velocity.Y < 0f)
					{
						velocity.Y -= 0.03f;
					}
					if ((double)velocity.Y > 2.5)
					{
						velocity.Y = 2.5f;
					}
				}
			}
			else if (type == 660)
			{
				float num230 = 0.1f;
				float num231 = 0.04f;
				float num232 = 4f;
				float num233 = 1.5f;
				int num234 = type;
				if (num234 == 660)
				{
					num230 = 0.35f;
					num231 = 0.3f;
					num232 = 6f;
					num233 = 5f;
				}
				if (direction == -1 && velocity.X > 0f - num232)
				{
					velocity.X -= num230;
					if (velocity.X > num232)
					{
						velocity.X -= num230;
					}
					else if (velocity.X > 0f)
					{
						velocity.X += num230 * 0.5f;
					}
					if (velocity.X < 0f - num232)
					{
						velocity.X = 0f - num232;
					}
				}
				else if (direction == 1 && velocity.X < num232)
				{
					velocity.X += num230;
					if (velocity.X < 0f - num232)
					{
						velocity.X += num230;
					}
					else if (velocity.X < 0f)
					{
						velocity.X -= num230 * 0.5f;
					}
					if (velocity.X > num232)
					{
						velocity.X = num232;
					}
				}
				if (directionY == -1 && velocity.Y > 0f - num233)
				{
					velocity.Y -= num231;
					if (velocity.Y > num233)
					{
						velocity.Y -= num231;
					}
					else if (velocity.Y > 0f)
					{
						velocity.Y += num231 * 0.75f;
					}
					if (velocity.Y < 0f - num233)
					{
						velocity.Y = 0f - num233;
					}
				}
				else if (directionY == 1 && velocity.Y < num233)
				{
					velocity.Y += num231;
					if (velocity.Y < 0f - num233)
					{
						velocity.Y += num231;
					}
					else if (velocity.Y < 0f)
					{
						velocity.Y -= num231 * 0.75f;
					}
					if (velocity.Y > num233)
					{
						velocity.Y = num233;
					}
				}
			}
			else
			{
				if (direction == -1 && velocity.X > -4f)
				{
					velocity.X -= 0.1f;
					if (velocity.X > 4f)
					{
						velocity.X -= 0.1f;
					}
					else if (velocity.X > 0f)
					{
						velocity.X += 0.05f;
					}
					if (velocity.X < -4f)
					{
						velocity.X = -4f;
					}
				}
				else if (direction == 1 && velocity.X < 4f)
				{
					velocity.X += 0.1f;
					if (velocity.X < -4f)
					{
						velocity.X += 0.1f;
					}
					else if (velocity.X < 0f)
					{
						velocity.X -= 0.05f;
					}
					if (velocity.X > 4f)
					{
						velocity.X = 4f;
					}
				}
				if (directionY == -1 && (double)velocity.Y > -1.5)
				{
					velocity.Y -= 0.04f;
					if ((double)velocity.Y > 1.5)
					{
						velocity.Y -= 0.05f;
					}
					else if (velocity.Y > 0f)
					{
						velocity.Y += 0.03f;
					}
					if ((double)velocity.Y < -1.5)
					{
						velocity.Y = -1.5f;
					}
				}
				else if (directionY == 1 && (double)velocity.Y < 1.5)
				{
					velocity.Y += 0.04f;
					if ((double)velocity.Y < -1.5)
					{
						velocity.Y += 0.05f;
					}
					else if (velocity.Y < 0f)
					{
						velocity.Y -= 0.03f;
					}
					if ((double)velocity.Y > 1.5)
					{
						velocity.Y = 1.5f;
					}
				}
			}
			if (type == 49 || type == 51 || type == 60 || type == 62 || type == 66 || type == 93 || type == 137 || type == 150 || type == 151 || type == 152 || type == 634)
			{
				if (wet)
				{
					if (velocity.Y > 0f)
					{
						velocity.Y *= 0.95f;
					}
					velocity.Y -= 0.5f;
					if (velocity.Y < -4f)
					{
						velocity.Y = -4f;
					}
					TargetClosest();
				}
				if (type == 60)
				{
					if (direction == -1 && velocity.X > -4f)
					{
						velocity.X -= 0.1f;
						if (velocity.X > 4f)
						{
							velocity.X -= 0.07f;
						}
						else if (velocity.X > 0f)
						{
							velocity.X += 0.03f;
						}
						if (velocity.X < -4f)
						{
							velocity.X = -4f;
						}
					}
					else if (direction == 1 && velocity.X < 4f)
					{
						velocity.X += 0.1f;
						if (velocity.X < -4f)
						{
							velocity.X += 0.07f;
						}
						else if (velocity.X < 0f)
						{
							velocity.X -= 0.03f;
						}
						if (velocity.X > 4f)
						{
							velocity.X = 4f;
						}
					}
					if (directionY == -1 && (double)velocity.Y > -1.5)
					{
						velocity.Y -= 0.04f;
						if ((double)velocity.Y > 1.5)
						{
							velocity.Y -= 0.03f;
						}
						else if (velocity.Y > 0f)
						{
							velocity.Y += 0.02f;
						}
						if ((double)velocity.Y < -1.5)
						{
							velocity.Y = -1.5f;
						}
					}
					else if (directionY == 1 && (double)velocity.Y < 1.5)
					{
						velocity.Y += 0.04f;
						if ((double)velocity.Y < -1.5)
						{
							velocity.Y += 0.03f;
						}
						else if (velocity.Y < 0f)
						{
							velocity.Y -= 0.02f;
						}
						if ((double)velocity.Y > 1.5)
						{
							velocity.Y = 1.5f;
						}
					}
				}
				else
				{
					if (direction == -1 && velocity.X > -4f)
					{
						velocity.X -= 0.1f;
						if (velocity.X > 4f)
						{
							velocity.X -= 0.1f;
						}

```


---

## 🤖 Assistant · 2026-08-19T03:11:50.742Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
I see the aiStyle 14 block. Key findings so far:

**158 Vampire Bat** (cs:22948-23000):
- Day-flee branch: `if (position.Y < Main.worldSurface*16 && IsItDay && !eclipse) { directionY = -1; direction *= -1; }` — ours has this ✓ (4362-4367).
- X-axis: `if (direction == -1 && velocity.X > -7f) { velocity.X -= 0.2f; if (velocity.X > 4f) velocity.X -= 0.1f; else if (velocity.X > 0f) velocity.X += 0.05f; ... }` — NOTE: the threshold in the second condition is **4f**, not 7f! Ours (4370-4378): `if (dirX === -1 && this.vx > -cx) { this.vx -= ax; if (this.vx > cx) this.vx -= ax; else if (this.vx > 0) this.vx += ax * 0.5; ... }` with cx=7, ax=0.2. So ours uses `vx > 7` where vanilla uses `vx > 4` (and `vx > 0 → +0.05` where ours does `+ax*0.5 = +0.1`). DIFF!

Wait, let me recheck: vanilla 158: `if (direction == -1 && velocity.X > -7f) { velocity.X -= 0.2f; if (velocity.X > 4f) velocity.X -= 0.1f; else if (velocity.X > 0f) velocity.X += 0.05f; if (velocity.X < -7f) velocity.X = -7f; }`.

Hmm interesting — so for 158 the "counter-thrust" thresholds are 4 (not cap 7) and the small counter is 0.05 (not half of 0.2). Compare the default branch: `velocity.X -= 0.1f; if (velocity.X > 4f) velocity.X -= 0.1f; else if (velocity.X > 0f) velocity.X += 0.05f;` — for default, cap = 4, so threshold 4 == cap, counter 0.05 = 0.5×0.1 ✓ consistent with ours (ax*0.5). For 158: cap 7, threshold 4, counter 0.05 (not 0.5×0.2=0.1). Ours uses threshold=cx(7) and counter=0.1. So two param diffs for 158.

- Y-axis 158: `velocity.Y -= 0.2f; if (velocity.Y > 4f) velocity.Y -= 0.1f; else if (velocity.Y > 0f) velocity.Y += 0.05f;` — same thresholds (4, 0.05). Ours uses same generic shape with cy=7, ay=0.2, threshold 7, counter 0.1. Same diff.

**660 Giant Fox Bat** (cs:23083-23147):
- X: num230=0.35, num232=6: `velocity.X -= 0.35; if (velocity.X > 6) velocity.X -= 0.35; else if (velocity.X > 0) velocity.X += 0.35*0.5;` — threshold = num232 (6) = cap ✓, counter = 0.5× ✓. Ours matches (ax=0.35, cx=6, generic). ✓
- Y: num231=0.3, num233=5: threshold 5 = cap ✓; counter: `velocity.Y += num231 * 0.75f` — 0.75×, NOT 0.5×! Ours Y-axis uses `ay * 0.5` wait — ours line 4382: `if (this.vy > cy) this.vy -= 0.05; else if (this.vy > 0) this.vy += 0.03;` — WAIT. Ours Y-axis branch is HARDCODED to the default bat values (0.05/0.03), not scaled by ay/cy! Look at ours 4380-4388:

```
if (dirY === -1 && this.vy > -cy) {
  this.vy -= ay;
  if (this.vy > cy) this.vy -= 0.05; else if (this.vy > 0) this.vy += 0.03;
  if (this.vy < -cy) this.vy = -cy;
}
```

So Y-axis counter-corrections are hardcoded 0.05/0.03 (default bat's values) regardless of ay. For 660 (ay=0.3, cy=5): vanilla does `vy -= 0.3; if (vy > 5) vy -= 0.3; else if (vy > 0) vy += 0.3*0.75 = 0.225`. Ours: `vy -= 0.3; if (vy > 5) vy -= 0.05; else if (vy > 0) vy += 0.03;` — wrong secondary values (0.05 vs 0.3; 0.03 vs 0.225). Also for 158 (ay=0.2, cy=7): vanilla `vy -= 0.2; if (vy > 4) vy -= 0.1; else if (vy > 0) vy += 0.05;` — ours: `vy -= 0.2; if (vy > 7) vy -= 0.05; else if (vy > 0) vy += 0.03`. Multiple diffs.

Also 660 X counter uses 0.5× (matches), Y uses 0.75× (ours 0.03 fixed).

**Default branch** (else, cs:23148-23200): X: 0.1/±4, second 0.1, counter 0.05 ✓ matches ours ax=0.1. Y: 0.04/±1.5, second 0.05, counter 0.03 ✓ matches ours (0.05/0.03 hardcoded = default). Good for default members.

**wet swim-up family** (cs:23232-23243): types 49/51/60/62/66/93/137/150/151/152/634. Ours has AI014_SWIM_UP set — need to check its contents match {49,51,60,62,66,93,137,150,151,152,634}. Let me grep.

Then type 60 (Giant Shelly? no — 60 = "Man Eater"? hmm; 60 is... "Cave Bat"? no. 60 = "?"). Type 60 has custom X/Y params (0.1/0.07/0.03; Y 0.04/0.03/0.02 ±1.5) — these are SECOND-tier corrections differing from default. Ours: after the wet block, vanilla has `if (type == 60) {...} else { default X/Y }` — wait no. Let me re-read: the wet block at 23232 contains `if (type == 60) { X params 0.1/0.07/0.03 } else { X params 0.1/0.1/0.05 } ...` — this is a SECOND movement block applied to the wet-family members (49/51/60/62/66/93/137/150/151/152/634) AFTER the general direction-based block! So these types get double-stepped? Wait no — let me look more carefully at the structure.

Actually looking at the code: line 23227: `if (type == 49 || type == 51 || type == 60 || ...)` — this block includes the wet handling AND THEN a second movement section (`if (type == 60) {movement} else {movement}`). So for these types, movement is handled INSIDE this block (separate from the earlier direction blocks)? No wait — the earlier blocks (158/226/660/else) already applied movement. Hmm, so the 49/51/60/62/66/93/137/150/151/152/634 family gets BOTH the general `else` branch movement AND this second block?? That would double-accelerate.

Hmm, let me look at the actual layout again. The first movement chain is: `if (type == 158) {...} else if (type == 226) {...} else if (type == 660) {...} else {...}` — so ALL types get one of these. Then `if (type == 49 || ... || type == 634)` block contains wet + ANOTHER movement block. So yes — these 11 types get a second movement application per tick! That means for e.g. Demon (62): first the default `else` movement (0.1/±4, 0.04/±1.5), then inside the wet block: the `else` sub-branch (0.1/0.1/0.05 X; and Y...) — demons effectively move at double acceleration? Interesting — this looks like the actual vanilla behavior (probably intentional for hell flyers to be faster). Let me read the rest of that block to confirm it's a second full movement application and not something else. Let me continue reading 23320-23543.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:51.165Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 23320,23544p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 14 block part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:51.224Z

**📎 ToolResult**

```
						}
						else if (velocity.X > 0f)
						{
							velocity.X += 0.05f;
						}
						if (velocity.X < -4f)
						{
							velocity.X = -4f;
						}
					}
					else if (direction == 1 && velocity.X < 4f)
					{
						velocity.X += 0.1f;
						if (velocity.X < -4f)
						{
							velocity.X += 0.1f;
						}
						else if (velocity.X < 0f)
						{
							velocity.X -= 0.05f;
						}
						if (velocity.X > 4f)
						{
							velocity.X = 4f;
						}
					}
					if (directionY == -1 && (double)velocity.Y > -1.5)
					{
						velocity.Y -= 0.04f;
						if ((double)velocity.Y > 1.5)
						{
							velocity.Y -= 0.05f;
						}
						else if (velocity.Y > 0f)
						{
							velocity.Y += 0.03f;
						}
						if ((double)velocity.Y < -1.5)
						{
							velocity.Y = -1.5f;
						}
					}
					else if (directionY == 1 && (double)velocity.Y < 1.5)
					{
						velocity.Y += 0.04f;
						if ((double)velocity.Y < -1.5)
						{
							velocity.Y += 0.05f;
						}
						else if (velocity.Y < 0f)
						{
							velocity.Y -= 0.03f;
						}
						if ((double)velocity.Y > 1.5)
						{
							velocity.Y = 1.5f;
						}
					}
				}
			}
			if (type == 48 && wet)
			{
				if (velocity.Y > 0f)
				{
					velocity.Y *= 0.95f;
				}
				velocity.Y -= 0.5f;
				if (velocity.Y < -4f)
				{
					velocity.Y = -4f;
				}
				TargetClosest();
			}
			if (type == 158 && Main.netMode != 1)
			{
				Vector2 vector22 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
				float num235 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector22.X;
				float num236 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector22.Y;
				float num237 = (float)Math.Sqrt(num235 * num235 + num236 * num236);
				if (num237 < 200f && position.Y + (float)height < Main.player[target].position.Y + (float)Main.player[target].height && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
				{
					Transform(159);
				}
			}
			this.ai[1] += 1f;
			if (type == 158)
			{
				this.ai[1] += 1f;
			}
			if (this.ai[1] > 200f)
			{
				if (!Main.player[target].wet && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
				{
					this.ai[1] = 0f;
				}
				float num238 = 0.2f;
				float num239 = 0.1f;
				float num240 = 4f;
				float num241 = 1.5f;
				if (type == 48 || type == 62 || type == 66)
				{
					num238 = 0.12f;
					num239 = 0.07f;
					num240 = 3f;
					num241 = 1.25f;
				}
				if (this.ai[1] > 1000f)
				{
					this.ai[1] = 0f;
				}
				this.ai[2] += 1f;
				if (this.ai[2] > 0f)
				{
					if (velocity.Y < num241)
					{
						velocity.Y += num239;
					}
				}
				else if (velocity.Y > 0f - num241)
				{
					velocity.Y -= num239;
				}
				if (this.ai[2] < -150f || this.ai[2] > 150f)
				{
					if (velocity.X < num240)
					{
						velocity.X += num238;
					}
				}
				else if (velocity.X > 0f - num240)
				{
					velocity.X -= num238;
				}
				if (this.ai[2] > 300f)
				{
					this.ai[2] = -300f;
				}
			}
			if (Main.netMode == 1)
			{
				return;
			}
			if (type == 48)
			{
				this.ai[0] += 1f;
				if (this.ai[0] == 30f || this.ai[0] == 60f || this.ai[0] == 90f)
				{
					if (Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
					{
						float num242 = 6f;
						Vector2 vector23 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
						float num243 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector23.X + (float)Main.rand.Next(-100, 101);
						float num244 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector23.Y + (float)Main.rand.Next(-100, 101);
						float num245 = (float)Math.Sqrt(num243 * num243 + num244 * num244);
						num245 = num242 / num245;
						num243 *= num245;
						num244 *= num245;
						int num246 = 15;
						int num247 = 38;
						int num248 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector23.X, vector23.Y, num243, num244, num247, num246, 0f, Main.myPlayer);
						Main.projectile[num248].timeLeft = 300;
					}
				}
				else if (this.ai[0] >= (float)(400 + Main.rand.Next(400)))
				{
					this.ai[0] = 0f;
				}
			}
			if (type == 62 || type == 66)
			{
				this.ai[0] += 1f;
				if (this.ai[0] == 20f || this.ai[0] == 40f || this.ai[0] == 60f || this.ai[0] == 80f)
				{
					if (Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
					{
						float num249 = 0.2f;
						Vector2 vector24 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
						float num250 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector24.X + (float)Main.rand.Next(-100, 101);
						float num251 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector24.Y + (float)Main.rand.Next(-100, 101);
						float num252 = (float)Math.Sqrt(num250 * num250 + num251 * num251);
						num252 = num249 / num252;
						num250 *= num252;
						num251 *= num252;
						int num253 = 21;
						int num254 = 44;
						int num255 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector24.X, vector24.Y, num250, num251, num254, num253, 0f, Main.myPlayer);
						Main.projectile[num255].timeLeft = 300;
					}
				}
				else if (this.ai[0] >= (float)(300 + Main.rand.Next(300)))
				{
					this.ai[0] = 0f;
				}
			}
			if (type != 156)
			{
				return;
			}
			this.ai[0] += 1f;
			if (this.ai[0] == 20f || this.ai[0] == 40f || this.ai[0] == 60f || this.ai[0] == 80f || this.ai[0] == 100f)
			{
				if (Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
				{
					float num256 = 0.2f;
					Vector2 vector25 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
					float num257 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector25.X + (float)Main.rand.Next(-50, 51);
					float num258 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector25.Y + (float)Main.rand.Next(-50, 51);
					float num259 = (float)Math.Sqrt(num257 * num257 + num258 * num258);
					num259 = num256 / num259;
					num257 *= num259;
					num258 *= num259;
					int num260 = 80;
					int num261 = 115;
					vector25 += velocity * 5f;
					int num262 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector25.X + num257 * 100f, vector25.Y + num258 * 100f, num257, num258, num261, num260, 0f, Main.myPlayer);
					Main.projectile[num262].timeLeft = 300;
				}
			}
			else if (this.ai[0] >= (float)(250 + Main.rand.Next(250)))
			{
				this.ai[0] = 0f;
			}
			return;
		}
		if (aiStyle == 15)

```


---

## 🤖 Assistant · 2026-08-19T03:13:03.092Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have the complete aiStyle 14 block. Let me carefully diff our batAI against it:

**Vanilla aiStyle 14 structure:**
1. noGravity = true.
2. collideX → bounce -0.5 + min ±2 (toward direction); collideY → bounce -0.5 + min ±1. — ours ✓ (4398-4409), applied AFTER moveAndCollide. Vanilla applies bounce FIRST (at AI start, using previous frame's collide flags — the collide flags from last tick's collision step). Ours applies after this tick's moveAndCollide. Equivalent-ish ordering. Note vanilla uses `direction` for the min-bounce direction; ours uses facing. Minor.
3. type 226: keep-direction-if-no-LOS (Loki? 226 = "Corruptor"? no — 226 = "Blood Feeder"? hmm — 226 is "Flocko"? no. 226... it's aiStyle 14 with special LOS-keep-direction. 226 = "Lavabat"? hmm. Actually 226 = "Salt Water... "? Whatever). Wait — 226 gets special movement block: X 0.2/±4, threshold 4, counter 0.05; Y 0.1/±2.5, counter 0.05/0.03. Ours: NO type-226 branch! Our batAI default treats 226 with 0.1/0.04 ±4/±1.5. What is type 226? Let me check the name — 226 might be "Giant Bat"? no 158. Hmm, 226 = "Arapaima"? no. Let me look up: NPC 226... In the FindFrame section earlier: "case 151: case 152: case 158: case 226:" grouped. 226 = "Icy Merman"? no. Hmm — 151/152 are "Slimer"/"Hoppin' Jack"? no... 151 = "Toxic Sludge"? 152 = "Ichor Sticker"? Hmm no, Ichor Sticker is 173. Let me just grep the Lang file or spawn names. Actually NPC 226 = "Lava Bat"? Hmm, Lava Bat is 95? No — Lava Bat is 95? Hmm. Let me check: 226 = "Giant Flying Fox"? no that's 660. Let me grep Lang or check around SetDefaults line for 226.

Let me do that later; it matters because our batAI lacks the 226 branch entirely (both the LOS-keep-direction pre-block and its custom movement params 0.2/±4 X, 0.1/±2.5 Y).

4. 158 branch: movement 0.2 accel ±7 cap; counter-thrust threshold 4 and counter 0.1/0.05. Also `direction *= -1` day-flee. Ours has day-flee ✓; but threshold/counter params wrong (uses 7 & 0.1 instead of 4 & 0.1/0.05). Wait — careful for X: vanilla `velocity.X -= 0.2; if (velocity.X > 4) velocity.X -= 0.1; else if (velocity.X > 0) velocity.X += 0.05;` — the counter uses 0.1 (half of 0.2? no wait 0.2's half is 0.1 ✓) hmm: -0.2 main; secondary -0.1 (= 0.5×0.2 ✓ same as generic); tertiary +0.05 (= generic 0.05 ✓). And threshold: generic uses `velocity.X > 4f` where cap is 4 — so threshold == cap generically; for 158 cap is 7 but threshold stays 4. So the ONLY diff for 158 X: threshold should be 4, not 7. Ours: `if (this.vx > cx) this.vx -= ax;` with cx=7 → threshold 7. Vanilla 4. Diff confirmed.
   For 158 Y: vanilla `velocity.Y -= 0.2; if (velocity.Y > 4) velocity.Y -= 0.1; else if (velocity.Y > 0) velocity.Y += 0.05;` — threshold 4, secondary 0.1, tertiary 0.05. Ours Y: hardcoded `if (vy > cy) vy -= 0.05; else if (vy > 0) vy += 0.03;` → threshold 7, secondary 0.05, tertiary 0.03. THREE diffs on Y axis.
   Y cap: vanilla -7/7 ✓ ours cy=7 ✓.

5. 660 branch: X: 0.35/±6, threshold 6 (=num232 ✓ cap), secondary num230 (0.35, full!), tertiary 0.5×num230 (0.175). Wait re-read: `velocity.X -= num230; if (velocity.X > num232) velocity.X -= num230; else if (velocity.X > 0f) velocity.X += num230 * 0.5f;` — secondary = num230 (0.35), NOT half. Ours: `if (this.vx > cx) this.vx -= ax;` → ax=0.35 secondary ✓ full! Hmm wait ours: `this.vx -= ax; if (this.vx > cx) this.vx -= ax; else if (this.vx > 0) this.vx += ax * 0.5;` — secondary = ax (0.35) ✓, tertiary 0.175 ✓. X matches for 660!
   Y: vanilla `velocity.Y -= num231; if (velocity.Y > num233) velocity.Y -= num231; else if (velocity.Y > 0f) velocity.Y += num231 * 0.75f;` — secondary 0.3, tertiary 0.225. Ours Y: hardcoded `vy -= ay; if (vy > cy) vy -= 0.05; else if (vy > 0) vy += 0.03;` → secondary 0.05 (should be 0.3), tertiary 0.03 (should be 0.225). DIFF (matches the generic Y hardcode problem).

   → Our batAI's Y-axis branch is hardwired to default-bat secondary/tertiary values (0.05/0.03) for ALL types including 158/660. This is a real confirmed bug affecting 660's Y responsiveness (0.05 vs 0.3 secondary accel → much weaker vertical correction).

6. Wet block (cs:23232): family {49,51,60,62,66,93,137,150,151,152,634} + harpy 48 (separate at 23372). Ours has AI014_SWIM_UP set — need to verify contents. Then type 60 custom params + else default params — a SECOND movement pass for the 11-member family. Ours: does NOT have this second pass at all! Wait — let me re-read ours... Our batAI only has one movement block. Vanilla applies movement TWICE per tick for types 49/51/60/62/66/93/137/150/151/152/634 (once from the 158/226/660/else chain — they hit the `else` default — and once inside the wet-family block). So demons (62/66), hellbats (49?), etc. get DOUBLE acceleration in vanilla (effective 0.2/±4 X, 0.08/±1.5 Y). Ours only applies once. CONFIRMED DIFF — significant: demon/hellbat family moves at half vanilla acceleration.

Wait wait. Let me re-read the vanilla structure carefully to be sure the second block is inside the wet-family if and not the continuation:

```
if (type == 49 || type == 51 || type == 60 || type == 62 || type == 66 || type == 93 || type == 137 || type == 150 || type == 151 || type == 152 || type == 634)
{
    if (wet) { ... TargetClosest(); }
    if (type == 60) { movement X 0.1/0.07/0.03 ±4; Y 0.04/0.03/0.02 ±1.5 }
    else { movement X 0.1/0.1/0.05 ±4; Y 0.04/0.05/0.03 ±1.5 }
}
```

Yes — the second movement block is inside the family `if`, applied unconditionally (not just when wet). So the 11 hell/dungeon flyer types get two movement passes. Hmm wait, but actually — is that right? The first `else` chain: `if (type == 158) ... else if (type == 226) ... else if (type == 660) ... else {default}`. Types 49/51/60/62/66/93/137/150/151/152/634 fall into the final `else` → first pass. Then the family block gives them a second pass. So yes double.

Hmm, that seems odd but it's what the decompiled code says. This matches "Demon flies noticeably fast" gameplay memory. OK.

So our batAI is missing the ENTIRE second pass for the 11-type family {49,51,60,62,66,93,137,150,151,152,634}. Severity: 严重 (movement feel halves) for demon/hellbat family. But note: batAI 主体已修勿重报 — the parent said the batAI main body was already fixed and not to re-report; but this second-pass omission is part of the main body... Hmm. The instruction: "158 吸血蝙蝠/660 巨狐蝠——batAI 主体已修勿重报,查这两专属分支的参数" — so they explicitly scoped me to the 158/660 branch params. But I discovered the missing second-pass for the wet-family — that's arguably "主体". I'll report it but flag that it may overlap the "主体已修" scope — it's a real diff either way; the parent can triage. Actually since they say "已修勿重报" (already fixed, don't re-report) — if the second pass is still missing after their fix, then it wasn't fixed; report it. The instruction's intent is to avoid duplicate noise on things already known-fixed, not to suppress real bugs.

7. **ai[1] > 200 forced vertical bob** (cs:23393-23462): For ALL aiStyle 14 NPCs: `ai[1] += 1 (158: +2); if (ai[1] > 200) { if (!player.wet && CanHit) ai[1] = 0; ... bob oscillation via ai[2]: vy += 0.1/0.07, ±1.5/±1.25 (48/62/66: 0.12/0.07 ±3/±1.25); ai[2] thresholds ±150/300 }`. Ours: MISSING entirely. This is the "approach-avoidance" wander: when in sight but... hmm wait — when does ai[1] exceed 200? It counts up always, resets to 0 when player NOT wet AND CanHit (has LOS). So when the bat LOST line of sight for 200 ticks, it starts oscillating vy/vx (search behavior), until ai[1] > 1000 → reset. Ours has nothing like this. Medium severity — behavior after losing sight.

Hmm wait, re-read: `this.ai[1] += 1; if (type == 158) ai[1] += 1; if (this.ai[1] > 200f) { if (!player.wet && CanHit) ai[1] = 0; ... }` — the check `!player[target].wet` — interesting: resets when player NOT wet and LOS clear. Note this is LOS chase-gate territory? It's "line of sight" related — the excluded scope is "追击门(wet/视线)" handled by another agent! Hmm. "另有并行代理在专查'玩家死亡(null player)退化行为'与'追击门(wet/视线)'两类——你不查这两类". The ai[1]>200 bob is a special skill (oscillation drift after losing target) — it's not exactly a chase gate; it's a behavior when LOS lost. Borderline. I'll mention briefly as "撞到一句话备注" territory? Actually the LOS gates themselves (whether to chase) are excluded; this ai[1] timer is a distinct mechanic (search bobbing). I'll report it briefly with a note that it may overlap the LOS-gate agent's scope.

8. Harpy 48 wet block (cs:23372-23382): ours has it in AI014_SWIM_UP (need to check 48 included). 

9. 158→159 transform (cs:23385-23400): vanilla checks `num237 < 200 && position.Y + height < player.position.Y + player.height && CanHit` → Transform(159). Ours (4412-4417) ✓ matches (d<200, y+h<player.y+h, canSee). ✓ Good.

10. Harpy 48 feather shots (cs:23464-23503): ai[0] += 1; at 30/60/90 shoot if CanHit: speed 6, spread ±100, dmg 15, proj 38, timeLeft 300; else if ai[0] >= 400+rand(400) reset. Ours (4424-4447): ticks [30,60,90], spd 6, dmg 15, spread 100, reset 400+rand400 ✓. BUT — reset logic diff: vanilla: `else if (ai[0] >= 400 + rand(400)) ai[0] = 0;` — the ELSE branch (i.e., when ai[0] not one of the shot ticks) checks reset with a FRESH random each tick; ours: caches the threshold in ai2 once (`if (this.ai2 === 0) this.ai2 = reset + rand(reset)`) then `if (ai0 >= ai2) {ai0=0; ai2=0}`. Ours caches — comment says "轮空后 ai[0] 达随机阈值归零——阈值缓存 ai[2]". Vanilla rerolls `400+rand(400)` every tick — expected first-hit after ~400+200... hmm no: `ai[0] >= 400 + Next(400)` evaluated each tick with new random → resets around ai[0]≈400-799, roughly when the fresh roll is low enough; effectively first tick where ai0 ≥ 400+U where U uniform 0-399 fresh each tick — since ai0 increments by 1 per tick, reset happens the first tick t ≥ 400 where U_t ≤ t-400; that's t ≈ 400 + geometric-ish ≈ 400+~1.4? no wait: at t=400, P(U≤0)=1/400; t=401, P(U≤1)=2/400... expected t ≈ 400 + 399/e? no — it's the minimum... P(reset by t) = 1-∏(1-(t-399-i+1)/400)... anyway ≈ 400+~27? Hmm actually expected overshoot is small (~26). Ours: single cached roll U0 → reset at exactly 400+U0 ∈ [400,799], mean 600. So ours waits ~2x longer on average between volleys. LOW-MED diff (fire cadence). Also vanilla timeLeft 300 on projectiles — ours shootDart probably handles; check shootDart for timeLeft. Eh.

Hmm wait, also vanilla's shots check `Collision.CanHit` per shot; ours canSeePlayer ✓.

11. Demon 62/66 (cs:23506-23543): shots at 20/40/60/80, speed 0.2, spread ±100, dmg 21, proj 44, reset 300+rand300 ✓ ours matches incl lead 0. ✓ Red Devil 156: ticks 20/40/60/80/100, spd 0.2, dmg 80, spread ±50, reset 250+rand250, spawn offset: vanilla `vector25 += velocity * 5f; NewProjectile(vector25 + num257*100...)`. Ours: lead=100 applied as `cx + (ox/d)*100` — vanilla offset = velocity*5 + direction*100. Ours omits `velocity*5` (small) and uses direction from spread-adjusted vector ✓ roughly. Minor.

12. Also vanilla `if (Main.netMode == 1) return;` then harpy/demon/156 blocks. Then `if (type != 156) return;` — fine.

13. Note vanilla 226 pre-block: `TargetClosest(); if (!CanHit) { direction = num228 (sign of velocity.X); directionY = num229 }` — keeps moving in current direction when LOS lost. Ours missing entirely for 226. What NPC is 226? Let me identify. It's grouped with 151/152/158 in FindFrame... 226 = "Lava Bat"? Hmm no — Lava Bat is 95? Let me check: our repo has names. grep vanilla.json for "226".

Also — what are types 49/51/60/93/137/150/151/152/634? 49 = "Cave Bat"? no... Let me enumerate: aiStyle 14 members in our data with names — I'll grep our data file to identify which of our NPCs route to batAI. This also covers "其他未列但属飞行 case 枚举补全".

Now — the Y-axis hardcoded 0.05/0.03 also affects 158/660 (already noted). And the X-axis `if (this.vx > cx)` threshold for 158 should be 4.

Also check AI014_SWIM_UP set contents — grep Enemy.ts.

Let me also read our eocAI to make sure nothing demon-related is misrouted, though aiStyle 4 is EoC-only (no type-specific branches) — so the answer for the "AI_004 恶魔 66/火小鬼 24 归属" question: Demon 62/66 = aiStyle 14 (batAI), Fire Imp 24 = aiStyle 8 (casterAI). aiStyle 4 = EoC only. I'll verify our data agrees (vanilla.json aiStyle for 24/62/66). If our data routes 24 → casterAI ✓.

Now the jellyfish: vanilla aiStyle 18 at cs:24210-24464. Our jellyfishAI has detailed comments. Let me read the vanilla block to verify numbers.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:03.495Z · glm-x-preview-260804

```
我先检查一下 `AI014_SWIM_UP` 集合，并识别我们数据中的蜂群类型。
```


---

## 🤖 Assistant · 2026-08-19T03:13:04.195Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"AI014_SWIM_UP\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head; grep -n \"AI014_SWIM_UP = \" -A4 ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Find AI014_SWIM_UP set definition"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:04.269Z

**📎 ToolResult**

```
215:const AI014_SWIM_UP = new Set([48, 49, 51, 60, 62, 66, 93, 137, 150, 151, 152, 634]);
4392:    if (this.wet && this.vanillaId !== null && AI014_SWIM_UP.has(this.vanillaId)) {
215:const AI014_SWIM_UP = new Set([48, 49, 51, 60, 62, 66, 93, 137, 150, 151, 152, 634]);
216-
217-/** 原版路径 key（v_*）的占位 def，fromVanilla 会整体覆写 */
218-const PLACEHOLDER_DEF: EnemyDef = {
219-  key: 'v_placeholder', name: '?', hp: 1, damage: 0, knockbackResist: 0.5,

```


---

## 🤖 Assistant · 2026-08-19T03:13:05.076Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/data/ 2>/dev/null; grep -rln '\"aiStyle\"' ~/Project/GLM/SandboxWorld/game/src/ ~/Project/GLM/SandboxWorld/game/public/ 2>/dev/null | head -5",
 "description": "Locate NPC data files with aiStyle"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:05.762Z

**📎 ToolResult**

```
Bestiary.ts
bestiaryStatics.generated.ts
combat-font.json
critters.ts
enemies.ts
flexible-wands.json
fxPixelShader.json
grappleHooks.ts
itemKeys.ts
itemMigration.ts
items.ts
itemUseSound.ts
legacyItemIndex.generated.json
Music.ts
npcLavaImmune.ts
npcPortraits.ts
tiles.ts
townNpcProfiles.ts
vanilla-accfx.json
vanilla-banners.json
vanilla-bestiary-spawn.json
vanilla-bestiary.json
vanilla-bossbags.json
vanilla-dyes.json
vanilla-equip.json
vanilla-fishing.json
vanilla-gore.json
vanilla-hairdyes.json
vanilla-hovericons.json
vanilla-itemcombat.json
vanilla-itemfunc.json
vanilla-itemrare.json
vanilla-itemstats.json
vanilla-itemusesound.json
vanilla-itemvalue.json
vanilla-mapcolors.json
vanilla-mounts.json
vanilla-npc-immunity.json
vanilla-npcbestiaryoffset.json
vanilla-npcdrops.json
vanilla-npcnetid.json
vanilla-npcvalue.json
vanilla-petai.json
vanilla-pets.json
vanilla-prefix.json
vanilla-projectiles.json
vanilla-projframes.json
vanilla-projstatus.json
vanilla-projstatusplayer.json
vanilla-recipes.json
vanilla-research.json
vanilla-shimmer.json
vanilla-shopstock.json
vanilla-soundtracks.json
vanilla-statusplayer.json
vanilla-tilecollision.json
vanilla-travelshop.json
vanilla-wallitems.json
vanilla-whips.json
vanilla-wingstats.json
vanillaAccFx.ts
vanillaAchievements.ts
vanillaArmorSets.ts
vanillaBossBags.ts
vanillaDyes.ts
vanillaEquip.ts
vanillaFishing.ts
vanillaFoodColors.ts
vanillaHairDyes.ts
vanillaHappiness.ts
vanillaItemCombat.ts
vanillaItemFunc.ts
vanillaItemStats.ts
vanillaMapColors.ts
vanillaNpcAmbience.ts
vanillaNpcImmunity.ts
vanillaNpcs.ts
vanillaOpenBags.ts
vanillaPets.ts
vanillaPrefixes.ts
vanillaProjectiles.ts
vanillaProjStatusPlayer.ts
vanillaRecipes.ts
vanillaSummonStats.ts
vanillaTownAttack.ts
vanillaWingStats.ts
vanillaWingVisuals.ts
~/Project/GLM/SandboxWorld/game/src/data/vanilla-petai.json
~/Project/GLM/SandboxWorld/game/src/data/vanilla-projectiles.json
~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json

```


---

## 🤖 Assistant · 2026-08-19T03:13:11.164Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The AI014_SWIM_UP set includes 48 (harpy) — vanilla has 48 in a separate block with the same numbers, fine. Set = {48,49,51,60,62,66,93,137,150,151,152,634} — vanilla wet family {49,51,60,62,66,93,137,150,151,152,634} + 48 separate ✓ combined correctly.

Now let me check vanillaNpcs.ts for the aiStyle data — which NPCs map to which aiStyle in OUR data (to catch misrouting). And get names for 226, 23, 252, 205, 155, 329, 315, 410, 423, 546.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:12.151Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"226\\|'226'\\|\\\"226\\\"\" ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts | head -5; grep -c \"\" ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts; head -60 ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts",
 "description": "Inspect vanillaNpcs.ts structure"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:12.233Z

**📎 ToolResult**

```
318
// 原版 1.4.0.5 全量 NPC 数据（tools/extract-npcs.mjs 从 Terarria1405/NPC.cs SetDefaults 提取）。
// 增量补齐（2026-08-11）：473-476/590/591/594/628/629/631/634/635/692 十三条取自
// Terarria1456/NPC.cs SetDefaults + Main.cs npcFrameCount（数值一律取 1456 最终态）。
// 弹跳球族增量（2026-08-11）：665 ChaosBallTim / 666 VileSpitEaterOfWorlds 两条取自
// Terarria1456/NPC.cs SetDefaults :17338-17367（aiStyle 9，字段对齐 30/112 同族；贴图
// NPC_665/666.png 已在 sprites，此前纯数据缺口）。
// 星璇塔增量（2026-08-11）：403/404（星尘蠕虫身/尾，字段复制 402 改宽高——1456 无独立
// SetDefaults，原版由 DrawNPC case 402 自绘 trail；本仓蠕虫链 spawnWormChain 需要
// 头+1/头+2 条目）、408（小水流入侵者，复制 407 缩小——1456 无独立 SetDefaults）。
// 城镇宠物声音增量（2026-08-18）：637/638/656 补 HitSound/DeathSound（1456
// SetDefaults :17142-17180/:17230-17244，提取器漏——637 猫 Hit1/Death6、
// 638 狗 Hit1/Death1、656 兔 Hit1/Death6；消费端 TownNPC.hurt/checkDead 数据驱动）。
// aiStyle 与 AI_XXX 方法的对应见 NPC.cs AI() 分发；此处先覆盖高频家族，
// 未移植 AI 家族的 aiStyle 回退到最接近的已移植行为（注释标注）。
import vanillaNpcsJson from '../../public/sprites/vanilla-npcs.json';
import vanillaDataJson from '../../public/sprites/vanilla.json';
import soundTracksJson from './vanilla-soundtracks.json';
import { ITEM_BY_KEY } from './items';
import { TILE_DEFS } from './tiles';

/** tile id → key 反查（biomeAt 群系判定用） */
const TILE_KEY_NAME: string[] = TILE_DEFS.map((d) => d.key);

// （旧掉落表已退役：掉落走 src/drops/NpcDrops.ts 规则树——
//  tools/extract-npcdrops.mjs 结构化提取 ItemDropDatabase.cs，含专家/大师/条件/链语义）

/** 原版物品 id → 本仓库 item key（vanilla.json 的 key 是 PascalCase，ITEM_BY_KEY 多为 snake_case；
 *  未注册的返回 null 跳过） */
export const vanillaItemKey = (() => {
  const map = new Map<number, string | null>();
  const items = (vanillaDataJson as unknown as { items: Record<string, { key?: string }> }).items ?? {};
  return (itemId: number): string | null => {
    if (map.has(itemId)) return map.get(itemId)!;
    const meta = items[String(itemId)];
    let key: string | null = null;
    if (meta?.key) {
      const snake = meta.key.replace(/([a-z0-9])([A-Z])/g, '$1_$2').toLowerCase();
      if (ITEM_BY_KEY[snake] != null) key = snake;
      else if (ITEM_BY_KEY[meta.key] != null) key = meta.key;
      // vi_NNN 导入物品（items.ts 的全量原版物品命名）：vi_<id> 或 vi_<id>_<snake>
      else if (ITEM_BY_KEY[`vi_${itemId}`] != null) key = `vi_${itemId}`;
      else if (ITEM_BY_KEY[`vi_${itemId}_${snake}`] != null) key = `vi_${itemId}_${snake}`;
    }
    map.set(itemId, key);
    return key;
  };
})();

export interface VanillaNpc {
  id: number;
  name: string;
  frames: number;
  lifeMax: number;
  damage: number;
  defense: number;
  knockBackResist: number;
  aiStyle: number;
  width: number;
  height: number;
  npcSlots: number;

```


---

## 🤖 Assistant · 2026-08-19T03:13:22.126Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst data = require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst list = Array.isArray(data) ? data : (data.npcs || data.entries || Object.values(data));\n// find entries for ids of interest\nconst ids = [6,23,42,48,49,51,60,62,66,93,112,137,150,151,152,158,176,205,210,211,226,231,232,233,234,235,242,252,315,329,410,423,546,619,620,634,660,24,63,64,103,221];\nfor (const e of list) {\n  if (ids.includes(e.id)) console.log(e.id, e.name || e.displayName || '', 'aiStyle=' + e.aiStyle);\n}\n\" 2>&1 | sort -n | head -60",
 "description": "List names and aiStyle for NPC ids of interest"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:22.227Z

**📎 ToolResult**

```
6 Eater of Souls aiStyle=5
23 Meteor Head aiStyle=5
24 Fire Imp aiStyle=8
42 Hornet aiStyle=5
48 Harpy aiStyle=14
49 Cave Bat aiStyle=14
51 Jungle Bat aiStyle=14
60 Hellbat aiStyle=14
62 Demon aiStyle=14
63 Blue Jellyfish aiStyle=18
64 Pink Jellyfish aiStyle=18
66 Voodoo Demon aiStyle=14
93 Giant Bat aiStyle=14
103 Green Jellyfish aiStyle=18
112 NPC_112 aiStyle=9
137 Illuminant Bat aiStyle=14
150 Ice Bat aiStyle=14
151 Lava Bat aiStyle=14
152 Giant Flying Fox aiStyle=14
158 NPC_158 aiStyle=14
176 Moss Hornet aiStyle=5
205 Moth aiStyle=5
210 Bee aiStyle=5
211 Bee aiStyle=5
221 Squid aiStyle=18
226 Flying Snake aiStyle=14
231 Hornet aiStyle=5
232 Hornet aiStyle=5
233 Hornet aiStyle=5
234 Hornet aiStyle=5
235 Hornet aiStyle=5
242 Blood Jelly aiStyle=18
252 Parrot aiStyle=5
315 Headless Horseman aiStyle=26
329 Hellhound aiStyle=26
410 NPC_410 aiStyle=26
423 Evolution Beast aiStyle=26
546 Angry Tumbler aiStyle=26
619 Blood Squid aiStyle=5
620 Goblin Shark aiStyle=107
634 Spore Bat aiStyle=14
660 QueenSlimeMinionPurple aiStyle=14

```


---

## 🤖 Assistant · 2026-08-19T03:14:19.625Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have names:
- 23 = Meteor Head (aiStyle 5) — swarmerAI member. Vanilla: num=1/num2=0.03, special rotation (spriteDirection + atan2 without -1.57), in the bounce-family list. Ours: default 6/0.05, faceTarget excludes 23 → uses current velocity for rotation with -π/2. Meteor Head in vanilla flies very slowly (speed 1!) and bounces. Ours: maxSpd 6! That's a big behavioral diff — meteor head would be 6x faster. Also 23 is in the bounce list (bounce 0.7) — ours ✓ applies bounce. But speed table missing. Hmm wait — is Meteor Head routed through swarmerAI? aiStyle 5 ✓ → case 5 → swarmerAI. maxSpd = isEater(6,173,139)? no → 94? no → 5? no → 6. So Meteor Head gets 6/0.05 vs vanilla 1/0.03. Confirmed diff, severity 中 (only appears in meteor biome; actually meteor heads — noticeable).

- 252 = Parrot (critter!). aiStyle 5 — critters go critterWanderAI first (critter gate before switch). So 252 never reaches swarmerAI — fine, actually. Vanilla AI_005 for parrot: the LOS-based speed 6/0.1 vs 2/0.01. Critter parrot — routing: critter check happens first (this.vanilla.critter). Is Parrot marked critter in our data? Probably (parrot is a critter in vanilla? No wait — Parrot 252 is a town-pet? No, Parrot is a critter? Actually the Parrot is a pet... no, the "Parrot" NPC 252 is a critter (jungle bird)? Hmm — 252 is "Parrot" — it's a critter you can catch? I believe yes, parrot is a critter (from 1.4? no...). Hmm, actually the Parrot (252) might be the pirate's pet? No — there's a "Parrot" critter? I don't recall a catchable parrot... Actually YES, there is no parrot critter; the parrot might be from the Pirate's... hmm. Whatever — since our critter gate sends it to critterWanderAI and vanilla routes 252 in AI_005 with LOS-based speed... If it IS a vanilla critter, vanilla would still run AI_005? Critters run their aiStyle AI normally (e.g., birds aiStyle 24?). Parrot with aiStyle 5 in AI_005 — with the "flag4" double-step (252 not excluded → flag4 true). This is a critter, low priority. I'll note briefly.

- 205 = Moth (aiStyle 5): num=3.25/num2=0.018. Ours: default 6/0.05. Diff. Moth is a... hardmode Hallowed critter? Moth is an enemy (hallow moth that drops butterfly dust? no that's... hmm, "Moth" drops Tattered Bee Wing? No — Moth is an enemy in the underground Hallow? Moth 205 is an enemy (spawns in Hallow) — actually wait, Moth might be a critter... "Moth" NPC 205 — I believe it's an enemy that spawns in the Hallow at night? Hmm no. Moth is a passive critter? There's "Moth" that drops Butterfly Dust... no that's Empress. Let me not worry: it's aiStyle 5 in our swarmerAI with wrong params (6/0.05 vs 3.25/0.018) + missing wet branch (already noted) + wrong dust (vanilla: 205 excluded from dust? The dust exclusion list: 42/139/176/205/210/211/252/231-235 — ours excludes 205 ✓).

- 226 = Flying Snake (aiStyle 14): missing special LOS-keep-direction + custom movement (X 0.2/±4, threshold 4; Y 0.1/±2.5). Ours: default 0.1/0.04 ±4/±1.5. Confirmed diff (中).

- 155 = ? not listed. 155/329 in AI_026 = Werewolf? Poltergeist? Let me check names: 155, 329, 315 (Headless Horseman), 410 (?), 423 (Evolution Beast), 546 (Angry Tumbler), 620 (Goblin Shark).
  - 315 Headless Horseman: AI_026 — our chargerAI: has light ✓ (4286). But missing: the 1001 rider projectile every 480 ticks (localAI[0] >= 480 → NewProjectile 1001...); missing pumpkin-head dust (frame 4-7 dust 6). Missing.
  - 329 Hellhound: AI_026 custom reverse-damp 0.9 + forward push 0.1 within ±3. Ours: generic 0.95 damp, no push, maxSpd=6 (default num11=6 ✓ but hellhound vanilla also has jump-when-close vy-=4 branch ✓ shared). Also 329: `if ((type == 329 || 315) && !Main.pumpkinMoon) EncourageDespawn(10)` gating TargetClosest — despawn logic.
  - 410 (Sroller?) & 423 (Evolution Beast): AI_026 with special: 410 — ai[1] += 1; if >= 240 or player above → explode into 3 projectiles 538 and die! Ours chargerAI: NO type-410 branch (missing suicide-burst). 423 — Corite-like: ai[2]==1 charging beam state (30t dust windup → fire projectile 575 backwards, 60t cycle, else ai[1]>=180 && dist<500 && onGround → start). Ours: missing entire 423 state machine. These are Tower enemies (Lunar events). Severity 中.
  - 546 Angry Tumbler: has separate movement (num11 = 4 + windLerp*3*direction, num12=0.05, reverse damp 0.92, rotation += vx*0.05, spriteDirection = -direction, desert-zone gate: if player not in ZoneDesert → EncourageDespawn + ai[3]=num) + flocking separation (the type==546 num2=4 mutual-repel loop at top). Ours: only the jump sound + generic movement 6/0.07. Missing: wind-modulated speed, rotation, spriteDirection flip, desert gate, flock separation. Severity 中 (tower event enemy).

Hmm wait — but is chargerAI even routed for 315/329/410/423/546? Our case 26 → chargerAI(game,p) for ALL aiStyle 26. And these types' exclusive branches are missing. But the parent's scope said "chargerAI(黄蜂族 42/231-235 冲刺链;620...)" — the parent thinks chargerAI handles hornets?? Hornets are aiStyle 5 → swarmerAI (with the sting chain implemented there at 3861+). So parent's description was slightly off; the "冲刺链" (charge chain) of hornets = the sting volley at 20/40/60...? No wait — hornets don't dash. Hmm, "黄蜂族 42/231-235 冲刺链" — maybe they mean the shooting cadence. Anyway, I've audited both swarmerAI (hornet chain) and chargerAI (AI_026). I'll report AI_026 type-specific gaps as part of chargerAI family.

Wait — actually let me double-check our case 26 routing: `case 26: this.chargerAI(game, p); break;` — yes all aiStyle-26. But wait — which NPCs in our data have aiStyle 26? Unicorn? Unicorn is 62? no 62=Demon. Unicorn = 62?? no. Unicorn NPC id... hmm: Unicorn = 62 is Demon so no. Let me query our data for aiStyle 26 members.

Also let me query aiStyle 5, 14, 18, 107, 4 members to enumerate the full family routing. That covers "枚举补全".

Now the jellyfish vanilla block — let me read cs:24210-24464 carefully to diff ours. Also check goblin shark 620 (cs:64118-64230) and wetSwimStep. And read our eocAI quickly for completeness (the EoC core was previously audited; but the aiStyle-4 audit — since aiStyle 4 has no type branches and EoC was audited in boss-audit-prehardmode, I'll do a light check to see if anything jumps out, especially since the task says eyes family "若 Enemy.ts 有 eocAI/eyeAI 家族" — eocAI exists at 6886; the known-correct parts per memory: "克眼专家状态机" done. I'll spot check a few core numbers quickly but keep it dense.)

Also "骷髅王手" = skeletronHandAI — imported from bossAI.ts. The task: "骷髅王手/克眼之外的眼睛族专属(若 Enemy.ts 有 eocAI/eyeAI 家族)" — skeletron hand is AI_012, in bossAI.ts. Hmm — "骷髅王手/克眼之外的眼睛族专属" is ambiguous but I read it as: skeleton-hand and the non-EoC eye family branches (floatEyeAI covers Demon Eye etc. — floatEyeAI 已修勿重报). Actually "floatEyeAI/batAI 主体/swimAI flag22" are the three already-fixed. So eyes: floatEyeAI is AI_002 (Demon Eye 191? no — aiStyle 2 = floating eye). The "eyeAI 家族" = AI_002 floatEyeAI — main body fixed. But AI_002 has type-specific branches too! Let me check the vanilla aiStyle 2 block (cs:19894-19899?) — wait, aiStyle 2 at 19894 is only 5 lines before aiStyle 4 at 19909? That can't be. Let me look: `19894: if (aiStyle == 2)` and `19899: if (aiStyle == 4)`. So aiStyle 2 is dispatched to AI_002_FloatingEye() (the independent function at 52673). Right — the big ones moved to functions. So floatEyeAI corresponds to AI_002_FloatingEye (52673-53195). Main body fixed — but there are type-specific branches inside (e.g., wraith? 316 ghost? demon eye variants, servant?). The task says check "eyes 族专属" if eocAI/eyeAI family exists. floatEyeAI exists (3595-3779). Since 主体已修, I should check only type-specific branches inside AI_002 that might be missing. Let me grep AI_002 for type-specific branches.

Also skeletronHandAI — AI_012 in bossAI.ts. Quick check against vanilla aiStyle 12 (22289-22604).

OK given scope, plan:
1. Read vanilla AI_018 (24210-24464) — diff jellyfishAI. 
2. Read vanilla cs:64118-64230 (goblin shark in AI_107) + our wetSwimStep.
3. Grep AI_002_FloatingEye type branches vs our floatEyeAI (light).
4. Read vanilla AI_012 skeletron hand (22289-22604) vs bossAI.ts skeletronHandAI (light).
5. Check eocAI core numbers quickly vs cs:19909-20758 (light, known audited).
6. Enumerate aiStyle routing for flying/aquatic cases in our data vs dispatch.

Let me do jellyfish first.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:19.931Z · glm-x-preview-260804

```
现在我来读取原版的 AI_018 jellyfish 代码块。
```


---

## 🤖 Assistant · 2026-08-19T03:14:20.339Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 24210,24464p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 18 jellyfish block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:20.667Z

**📎 ToolResult**

```
		if (aiStyle == 18)
		{
			bool flag23 = false;
			if (wet && this.ai[1] == 1f)
			{
				flag23 = true;
			}
			else
			{
				dontTakeDamage = false;
			}
			if (Main.expertMode && (type == 63 || type == 64 || type == 103 || type == 242))
			{
				if (wet)
				{
					if (target >= 0 && Main.player[target].wet && !Main.player[target].dead && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && (Main.player[target].Center - base.Center).Length() < 150f)
					{
						if (this.ai[1] == 0f)
						{
							this.ai[2] += 2f;
						}
						else
						{
							this.ai[2] -= 0.25f;
						}
					}
					if (flag23)
					{
						dontTakeDamage = true;
						this.ai[2] += 1f;
						if (this.ai[2] >= 120f)
						{
							this.ai[1] = 0f;
						}
					}
					else
					{
						this.ai[2] += 1f;
						if (this.ai[2] >= 420f)
						{
							this.ai[1] = 1f;
							this.ai[2] = 0f;
						}
					}
				}
				else
				{
					this.ai[1] = 0f;
					this.ai[2] = 0f;
				}
			}
			float num274 = 1f;
			if (flag23)
			{
				num274 += 0.5f;
			}
			if (type == 63)
			{
				Lighting.AddLight((int)(position.X + (float)(height / 2)) / 16, (int)(position.Y + (float)(height / 2)) / 16, 0.05f * num274, 0.15f * num274, 0.4f * num274);
			}
			else if (type == 103)
			{
				Lighting.AddLight((int)(position.X + (float)(height / 2)) / 16, (int)(position.Y + (float)(height / 2)) / 16, 0.05f * num274, 0.45f * num274, 0.1f * num274);
			}
			else if (type != 221 && type != 242)
			{
				Lighting.AddLight((int)(position.X + (float)(height / 2)) / 16, (int)(position.Y + (float)(height / 2)) / 16, 0.35f * num274, 0.05f * num274, 0.2f * num274);
			}
			if (direction == 0)
			{
				TargetClosest();
			}
			if (flag23)
			{
				return;
			}
			if (wet)
			{
				int num275 = (int)base.Center.X / 16;
				int num276 = (int)(position.Y + (float)height) / 16;
				if (Main.tile[num275, num276].topSlope())
				{
					if (Main.tile[num275, num276].leftSlope())
					{
						direction = -1;
						velocity.X = Math.Abs(velocity.X) * -1f;
					}
					else
					{
						direction = 1;
						velocity.X = Math.Abs(velocity.X);
					}
				}
				else if (Main.tile[num275, num276 + 1].topSlope())
				{
					if (Main.tile[num275, num276 + 1].leftSlope())
					{
						direction = -1;
						velocity.X = Math.Abs(velocity.X) * -1f;
					}
					else
					{
						direction = 1;
						velocity.X = Math.Abs(velocity.X);
					}
				}
				if (collideX)
				{
					velocity.X *= -1f;
					direction *= -1;
				}
				if (collideY)
				{
					if (velocity.Y > 0f)
					{
						velocity.Y = Math.Abs(velocity.Y) * -1f;
						directionY = -1;
						this.ai[0] = -1f;
					}
					else if (velocity.Y < 0f)
					{
						velocity.Y = Math.Abs(velocity.Y);
						directionY = 1;
						this.ai[0] = 1f;
					}
				}
				bool flag24 = false;
				if (!friendly)
				{
					TargetClosest(faceTarget: false);
					if (Main.player[target].wet && !Main.player[target].dead && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
					{
						flag24 = true;
					}
				}
				if (flag24)
				{
					localAI[2] = 1f;
					rotation = (float)Math.Atan2(velocity.Y, velocity.X) + 1.57f;
					velocity *= 0.98f;
					float num277 = 0.2f;
					if (type == 103)
					{
						velocity *= 0.98f;
						num277 = 0.6f;
					}
					if (type == 221)
					{
						velocity *= 0.99f;
						num277 = 1f;
					}
					if (type == 242)
					{
						velocity *= 0.995f;
						num277 = 3f;
					}
					if (velocity.X > 0f - num277 && velocity.X < num277 && velocity.Y > 0f - num277 && velocity.Y < num277)
					{
						if (type == 221)
						{
							localAI[0] = 1f;
						}
						TargetClosest();
						float num278 = 7f;
						if (type == 103)
						{
							num278 = 9f;
						}
						Vector2 vector26 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
						float num279 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector26.X;
						float num280 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - vector26.Y;
						float num281 = (float)Math.Sqrt(num279 * num279 + num280 * num280);
						num281 = num278 / num281;
						num279 *= num281;
						num280 *= num281;
						velocity.X = num279;
						velocity.Y = num280;
					}
					return;
				}
				localAI[2] = 0f;
				velocity.X += (float)direction * 0.02f;
				rotation = velocity.X * 0.4f;
				if (velocity.X < -1f || velocity.X > 1f)
				{
					velocity.X *= 0.95f;
				}
				if (this.ai[0] == -1f)
				{
					velocity.Y -= 0.01f;
					if (velocity.Y < -1f)
					{
						this.ai[0] = 1f;
					}
				}
				else
				{
					velocity.Y += 0.01f;
					if (velocity.Y > 1f)
					{
						this.ai[0] = -1f;
					}
				}
				int num282 = (int)(position.X + (float)(width / 2)) / 16;
				int num283 = (int)(position.Y + (float)(height / 2)) / 16;
				if (Main.tile[num282, num283 - 1] == null)
				{
					Main.tile[num282, num283 - 1] = new Tile();
				}
				if (Main.tile[num282, num283 + 1] == null)
				{
					Main.tile[num282, num283 + 1] = new Tile();
				}
				if (Main.tile[num282, num283 + 2] == null)
				{
					Main.tile[num282, num283 + 2] = new Tile();
				}
				if (Main.tile[num282, num283 - 1].liquid > 128)
				{
					if (Main.tile[num282, num283 + 1].active())
					{
						this.ai[0] = -1f;
					}
					else if (Main.tile[num282, num283 + 2].active())
					{
						this.ai[0] = -1f;
					}
				}
				else
				{
					this.ai[0] = 1f;
				}
				if ((double)velocity.Y > 1.2 || (double)velocity.Y < -1.2)
				{
					velocity.Y *= 0.99f;
				}
				return;
			}
			rotation += velocity.X * 0.1f;
			if (velocity.Y == 0f)
			{
				velocity.X *= 0.98f;
				if ((double)velocity.X > -0.01 && (double)velocity.X < 0.01)
				{
					velocity.X = 0f;
				}
			}
			velocity.Y += 0.2f;
			if (velocity.Y > 10f)
			{
				velocity.Y = 10f;
			}
			this.ai[0] = 1f;
			return;
		}

```


---

## 🤖 Assistant · 2026-08-19T03:15:15.487Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now diff jellyfishAI (ours 4621-4721) vs vanilla (24210-24464):

1. **Lurk gate** (24215): `if (wet && ai[1] == 1) flag23 = true; else dontTakeDamage = false;` — ours ✓ (4628-4629).

2. Expert + type gate (24229): expert && (63/64/103/242) ✓ ours lurkCapable uses mainExpertMode + same ids ✓.

3. Near check (24234-24240): `target >= 0 && player[target].wet && !dead && CanHit && dist < 150` — ours near ✓ (4631-4633). ✓

4. `if (ai[1] == 0) ai[2] += 2; else ai[2] -= 0.25` ✓ ours (4636-4639).

5. Lurk: dontTakeDamage = true, ai[2] += 1, >= 120 → ai[1] = 0 ✓ ours (4640-4643). Non-lurk: ai[2] += 1, >= 420 → ai[1]=1, ai[2]=0 ✓ (4644-4647). Out of water: both = 0 ✓ (4648-4650).

6. num274 light ✓ ours (4653-4657). Vanilla light position uses `(position.X + height/2)/16, (position.Y + height/2)/16` — ours uses lightRGB (center-based presumably). Fine.

7. `if (direction == 0) TargetClosest();` — ours: facing===0 → set from player (4708). Roughly ✓.

8. flag23 → return ✓ ours (4659).

9. Wet + slope handling (24295-24330): topSlope at bottom tile → direction flip. Ours: comment says slopeCollide in moveAndCollide approximates ✓ noted. collideX → vx *= -1, direction *= -1 ✓ ours (4663). collideY → vy invert + ai[0] sync ✓ ours (4664-4665) — BUT vanilla: `if (velocity.Y > 0) { vy = -|vy|; directionY=-1; ai[0]=-1 } else if (vy < 0) { vy = |vy|; ... }`. Ours: `if (this.onGround) { if (this.vy > 0) {...} } else if (this.hitHead) { if (this.vy < 0) {...} }` — equivalent-ish ✓ (assuming collideY → onGround/hitHead mapping). Vanilla applies this bounce BEFORE movement (collide flags from previous tick), ours after this tick's move — ordering nuance, same as bat. Fine.

   IMPORTANT ordering note: vanilla's collide handling happens BEFORE the movement/velocity updates and the actual position integration happens in the shared AI tail (collision at end). Ours does velocity updates then moveAndCollide then bounce check. Net effect roughly equivalent.

10. **flag24 attack form** (24365-24420): 
   - `if (!friendly) { TargetClosest(faceTarget: false); if (player.wet && !dead && CanHit) flag24 = true; }` — ours: playerWet && canSeePlayer (4667) — but ours doesn't check `!friendly` (all jellyfish enemies anyway; friendly jellies? There are no friendly aiStyle 18? Maybe from potions? Fine).
   - localAI[2] = 1 — ours doesn't persist (used where? maybe in damage code for something — grep vanilla localAI[2] elsewhere... it's likely used in Player/NPC hit code? Probably for "jellyfish zap"? Skip.)
   - rotation = atan2(vy,vx) + 1.57 ✓ ours visAngle (4673).
   - `velocity *= 0.98;` then type-specific: 103: `velocity *= 0.98` (TOTAL 0.98² per tick) and num277=0.6; 221: ×0.99, still=1; 242: ×0.995, still=3. Ours (4668-4672): `let damp = 0.98; if 103 damp *= 0.98; if 221 damp *= 0.99; if 242 damp *= 0.995;` ✓ matches (0.9604, 0.9702, 0.9751).
   - stillness gate ✓ (4675) `|vx|<still && |vy|<still` ✓.
   - `if (type == 221) localAI[0] = 1f;` — ours missing (221 Squid ink spray? localAI[0] used by... probably in hit code for squid ink). Let me check what localAI[2]/localAI[0] do — grep "localAI[2]" near damage or in Player? This could be the squid ink burst on contact. Minor; note as low/uncertain.
   - pulse: TargetClosest, num278=7 (103: 9), velocity = dir*num278 ✓ ours (4678-4682).
   - **RETURN** — note vanilla returns WITHOUT moving? No wait — vanilla AI functions don't move; movement happens in the shared tail via Collision. The `return` here returns from the aiStyle-18 block only... hmm, no — it's a `return` from... it's inside `if (aiStyle == 18) { ... }` in the big AI() method? `return` would exit AI() entirely! Wait — but then movement/collision wouldn't happen? Hmm, actually in vanilla, the AI() method continues to the movement section after the aiStyle switch. A `return` inside the aiStyle-18 block exits AI() → NO collision/movement this tick?! That can't be right — jellyfish DO move. Unless... position += velocity happens elsewhere. In vanilla NPC.cs AI(), after the big aiStyle switch there's the movement section (`if (noGravity ...) ... Collision` etc.) — a return would skip it.

Hmm wait — let me check: these `return`s at 24418 and 24457 (`return;` after the drift block). If AI() returned early, jellyfish would never move. Unless velocity integration happens in UpdateNPC elsewhere. Actually — vanilla NPC.AI() ends with the movement+collision code; early `return` skips it. But jellyfish DO move... so maybe the movement code is BEFORE the aiStyle switch? No... Hmm. Actually wait — in 1.4 vanilla, NPC.AI() structure: [lots of pre-code] → aiStyle switch (the giant if-chain) → [post-code: falling, collision, TargetClosest trailing, etc.]. An early return skips movement. But Terraria jellyfish visibly move and bounce off walls...

Hold on — maybe not. Let me verify: do jellyfish in Terraria actually move via the AI-set velocity with collision applied? The collideX/collideY handling at the TOP of the wet block references collide flags — those are set by the collision step which runs at the END of the previous tick's AI. So movement DOES happen. So the `return` must NOT skip it... unless the decompiled `return` is actually inside a lambda/local function? No.

Wait — let me re-look. Is this `return` actually inside the aiStyle==18 `if` block, and does the enclosing method have movement after? The decompiler emits `return;` for what in the original might be... hmm, actually in the original C#, this is exactly `return`. Let me check vanilla 1.4 source memory: AI_018? Hmm.

Actually wait — I bet the movement code comes BEFORE... no. Let me just check what follows the aiStyle==18 block: aiStyle == 19 at 24465. So the giant switch continues — `return` exits the whole AI() method. Then how do jellyfish move?

OH WAIT. I remember now — in vanilla, NPC movement integration happens in `NPC.UpdateNPC` → `AI()` — and velocity application/collision is INSIDE AI() at the end. Hmm, but then... let me actually check whether there's a "goto IL" pattern — decompilers sometimes produce `return` where the original had `goto` + shared tail... no, decompiled C# from IL2SPY/dnSpy on real code shows actual returns.

Hmm, hold on — maybe the aiStyle-18 block is not inside AI() but inside a separate method? Line 24210 `if (aiStyle == 18)` — the giant if-chain from 19774 to ~52600 is inside AI_??? Hmm, actually no. Let me check which method contains line 24210. The dispatch at 19774 `if (aiStyle == 0)`. Is that inside `private void AI()`? Let me check the method start before 19774 and see whether movement code follows the switch — and whether jellyfish moving is handled... 

Actually, you know what — jellyfish might genuinely not use the shared movement tail: the AI sets velocity, and position integration... Hmm no, SOMETHING integrates velocity.

Let me just grep the method containing this and look at the end of the method for the movement section. Actually simpler: check if `Collision` movement code appears after line 52600 (end of switch) — e.g., "noTileCollide" or "Collision.BoundingBoxCollision". But whatever — vanilla jellyfish obviously move; our implementation moves them via moveAndCollide. The important part is velocity logic, which I've verified. The early `return` just skips shared tail stuff (light? animations?) — not my concern. Actually it might matter for what's skipped (e.g., the despawn/timeLeft logic), but that's global. Skip.

11. **Drift form** (24421-24457): localAI[2]=0; vx += direction*0.02 ✓; rotation = vx*0.4 ✓; |vx|>1 ×0.95 ✓; ai[0] oscillation ±0.01 thresholds ±1 ✓; liquid probe (center tile col, tile above liquid>128 and +1/+2 active → ai[0]=-1; else ai[0]=1) ✓ ours (4700-4706); |vy|>1.2 ×0.99 ✓ (4707). 

    Ours drift block (4689-4709) ✓ matches. Note ours checks `st.isActive(cx, cy+1)` — vanilla `Main.tile[num282, num283 + 1].active()` — ours uses isActive (tile active) ✓.

    One nit: vanilla liquid probe uses `liquid > 128` ✓ ours ✓.

12. **Out of water** (24459-24473): rotation += vx*0.1 ✓ (4713); vy==0 → vx *= 0.98, |vx|<0.01 → 0 ✓ (4714-4717); gravity 0.2 cap 10 ✓ (4718); ai[0] = 1 ✓ (4719).

So jellyfishAI is nearly 1:1. Diffs:
- Missing `localAI[2]` persistence (24366/24421) and `localAI[0]=1` for squid 221 (24395) — need to check what consumes localAI[2] for jellyfish. Let me grep vanilla for localAI[2] usage in jellyfish-related code (e.g., NPC.hitEffect or Player contact). Search "localAI[2] == 1" elsewhere... it's generic across NPC types though (localAI is per-NPC). For jellyfish maybe used in Player.NPCInteraction for electrified debuff? Hmm. Let me grep quickly for context. Actually — 221 Squid's ink: when it hits the player? localAI[0]? I'll do one grep.
- The direction==0 → TargetClosest (24290): ours sets facing from player when facing===0 at line 4708 — but that's INSIDE the drift branch (after the drift block, before moveAndCollide) — vanilla does it before flag23 return (applies to attack form too). Ours: attack form sets facing only within stillness pulse (4677 seekDirX). Vanilla's TargetClosest(faceTarget:false) in flag24 gate updates `direction` continuously (facing used for drift horizontal push when returning to drift). Minor.

Actually also: ours drift `this.vx += this.facing * 0.02` — vanilla `velocity.X += direction * 0.02` ✓.

And in ours, drift-form facing init (4708): `if (this.facing === 0)` — facing probably never 0 in our engine (seekDirX returns ±1). fine.

Jellyfish: essentially clean. Report: localAI flags + minor ordering = 低/存疑.

Now goblin shark 620: read vanilla cs:64118-64230 and our wetSwimStep.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:16.112Z · glm-x-preview-260804

```
水母族的逻辑基本吻合。接下来我来查看地精鲨鱼分支 (cs:64118-64230) 以及我们编写的 `wetSwimStep`。
```


---

## 🤖 Assistant · 2026-08-19T03:15:16.623Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 64100,64240p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla goblin shark branch in AI_107"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:16.694Z

**📎 ToolResult**

```
				for (int num50 = 0; (float)num50 < (float)num48 * 1.3f; num50++)
				{
					if (Main.rand.Next(maxValue2) == 0)
					{
						Dust dust6 = Dust.NewDustDirect(position + new Vector2(-width / 2, 8f), width + width, height, 27, velocity.X * 1f, 0f, 100);
						dust6.scale = 1.1f;
						dust6.fadeIn = 0.1f;
						dust6.velocity = new Vector2(Main.rand.NextFloatDirection() * 0.1f, 0f - dust6.velocity.Length()) * 1.05f * num49 * Main.rand.NextFloat();
						dust6.velocity.Y *= Utils.GetLerpValue((float)width * 0.75f, 0f, Math.Abs(dust6.position.X - base.Center.X), clamped: true);
					}
				}
			}
			if (num44 > 100f && (int)num44 % 4 == 0)
			{
				Gore.NewGoreDirect(base.Left, new Vector2(0f, -3f), Utils.SelectRandom<int>(Main.rand, 971, 972), 0.85f).velocity.X *= 0.8f;
			}
			break;
		}
		case 620:
		{
			flag27 = wet;
			flag30 = false;
			flag16 = true;
			num20 = 150f;
			num19 = 20f;
			bool dayTime = Main.dayTime;
			flag21 = !dayTime;
			flag24 = true;
			flag12 = true;
			flag15 = ai[1] > 40f;
			num8 = 60;
			num9 = 40;
			if (ai[1] > 10f && ai[1] <= 40f && (int)ai[1] % 5 == 0)
			{
				num9 = (int)ai[1] - 1;
			}
			num12 = 811;
			vector.X -= 4 * direction;
			vector.Y -= 20f;
			num15 = 0.15f;
			num16 = 2.5f;
			num13 = 600f;
			num10 = 13f;
			num17 = 1;
			num18 = 0f;
			num11 = GetAttackDamage_ForProjectiles(40f, 30f);
			num23 = 8f;
			num24 *= 3f;
			num25 = 0.9f;
			if (ai[0] > 0f)
			{
				if (ai[1] == 40f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_DrakinShot, base.Center);
				}
				else if (ai[1] == 60f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_DrakinBreathIn, base.Center);
				}
			}
			position += netOffset;
			if (alpha == 255)
			{
				spriteDirection = direction;
				velocity.Y = -6f;
				netUpdate = true;
				for (int i = 0; i < 35; i++)
				{
					Dust dust = Dust.NewDustDirect(position, width, height, 5);
					dust.velocity *= 1f;
					dust.scale = 1f + Main.rand.NextFloat() * 0.5f;
					dust.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
					dust.velocity += velocity * 0.5f;
				}
			}
			alpha -= 15;
			if (alpha < 0)
			{
				alpha = 0;
			}
			if (alpha != 0)
			{
				for (int j = 0; j < 2; j++)
				{
					Dust dust2 = Dust.NewDustDirect(position, width, height, 5);
					dust2.velocity *= 1f;
					dust2.scale = 1f + Main.rand.NextFloat() * 0.5f;
					dust2.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
					dust2.velocity += velocity * 0.3f;
				}
			}
			if (Main.rand.Next(3) == 0)
			{
				Dust.NewDustDirect(position, width, height, 5, 0f, 0f, 50, default(Color), 1.3f).velocity = Vector2.Zero;
			}
			position -= netOffset;
			if (dayTime)
			{
				flag12 = false;
				flag24 = false;
				flag23 = true;
			}
			else
			{
				if (velocity.Y != 0f || !((float)targetData.Hitbox.Bottom < base.Top.Y) || !(Math.Abs(base.Center.X - (float)targetData.Hitbox.Center.X) < (float)(width * 3)) || !Collision.CanHit(base.Hitbox.TopLeft(), base.Hitbox.Width, base.Hitbox.Height, targetData.Hitbox.TopLeft(), targetData.Hitbox.Width, targetData.Hitbox.Height))
				{
					break;
				}
				int num32 = (int)((base.Bottom.Y - 16f - (float)targetData.Hitbox.Bottom) / 16f);
				if (num32 < 27)
				{
					if (num32 < 11)
					{
						velocity.Y = -11f;
					}
					else if (num32 < 15)
					{
						velocity.Y = -13f;
					}
					else if (num32 < 19)
					{
						velocity.Y = -14f;
					}
					else
					{
						velocity.Y = -15.9f;
					}
				}
			}
			break;
		}
		}
		if (flag28)
		{
			bool flag31 = velocity.Y == 0f;
			for (int num52 = 0; num52 < Main.maxNPCs; num52++)
			{
				if (num52 != whoAmI && Main.npc[num52].active && Main.npc[num52].type == type && Math.Abs(position.X - Main.npc[num52].position.X) + Math.Abs(position.Y - Main.npc[num52].position.Y) < (float)width)
				{
					if (position.X < Main.npc[num52].position.X)
					{

```


---

## 🤖 Assistant · 2026-08-19T03:15:17.028Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"wetSwimStep\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Find wetSwimStep definition"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:17.079Z

**📎 ToolResult**

```
2320:  private wetSwimStep(game: GameHooks, player: Player | null, mode: 461 | 586 | 620): boolean {
2408:      if (this.wetSwimStep(game, player, this.vanillaId as 461 | 586)) return;
4283:    if (this.vanillaId === 620 && this.wetSwimStep(game, player, 620)) return;

```


---

## 🤖 Assistant · 2026-08-19T03:15:28.427Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 140,
 "offset": 2320
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:28.446Z

**📎 ToolResult**

```
2320	  private wetSwimStep(game: GameHooks, player: Player | null, mode: 461 | 586 | 620): boolean {
2321	    if (!this.wet) {
2322	      // ---- 出水复原（461 :56409-56440 / 586 :56536-56558）----
2323	      if (mode === 461) {
2324	        this.kbResistOverride = getKnockbackMultiplierScaledByDifficulty(0.4, this.difficulty);
2325	        const cx = this.cx, cy = this.cy;
2326	        this.w = 18; this.h = 40;
2327	        this.x = cx - this.w / 2; this.y = cy - this.h / 2;
2328	      } else {
2329	        this.kbResistOverride = null;
2330	      }
2331	      if (this.ai3 === -0.10101) {
2332	        this.ai3 = 0;
2333	        let spd = Math.hypot(this.vx, this.vy) * 2;
2334	        if (spd > (mode === 586 ? 15 : 10)) spd = mode === 586 ? 15 : 10;
2335	        const l = Math.hypot(this.vx, this.vy);
2336	        if (l > 0) { this.vx = (this.vx / l) * spd; this.vy = (this.vy / l) * spd; }
2337	        if (this.vx < 0) this.facing = -1;
2338	        if (this.vx > 0) this.facing = 1;
2339	      }
2340	      return false;
2341	    }
2342	    // ---- 入水游泳 ----
2343	    this.kbResistOverride = 0;                                 // knockBackResist = 0f
2344	    this.ai3 = -0.10101;                                       // 出水冲量哨兵
2345	    if (mode === 461) {
2346	      // 缩盒 34×24（Center 保持，:56369-56373）
2347	      const cx = this.cx, cy = this.cy;
2348	      this.w = 34; this.h = 24;
2349	      this.x = cx - this.w / 2; this.y = cy - this.h / 2;
2350	    }
2351	    if (player && !player.dead) this.facing = this.seekDirX(player);  // TargetClosest
2352	    if (this.hitWall) this.vx = -this.vx;                      // collideX → -oldVelocity.X
2353	    if (mode !== 620) {                                        // 620 保持 direction（原文怪癖）
2354	      if (this.vx < 0) this.facing = -1;
2355	      if (this.vx > 0) this.facing = 1;
2356	    }
2357	    const sees = !!player && !player.dead && this.canSeePlayer(game.world.store, player);
2358	    if (sees) {
2359	      const dx = player!.cx - this.cx, dy = player!.cy - this.cy;
2360	      const d = Math.hypot(dx, dy) || 1;
2361	      let spd = 5;
2362	      let k = 1 / 20;                                          // 461/620 amount=0.05
2363	      if (mode === 586) {
2364	        spd = 1 + Math.abs(this.cy - player!.cy) / 40;         // num8（:56503-56506）
2365	        spd = Math.max(5, Math.min(20, spd));
2366	        k = this.vy > 0 ? 1 / 30 : 1 / 5;                      // :56511-56516
2367	      }
2368	      const tx = (dx / d) * spd, ty = (dy / d) * spd;
2369	      this.vx += (tx - this.vx) * k;
2370	      this.vy += (ty - this.vy) * k;
2371	      moveAndCollide(this, game.world, this.vx, this.vy);
2372	      return true;
2373	    }
2374	    // 无视线：斜上巡航（:56388-56405 / :56519-56536 / :64321-64336）
2375	    let cruise = 5;
2376	    if (this.vy > 0) cruise = 3;
2377	    if (this.vy < 0) cruise = 8;
2378	    const k2 = cruise < 5 ? 1 / 25 : 1 / 10;
2379	    const l = Math.hypot(this.facing, -1) || 1;
2380	    const tx2 = (this.facing / l) * cruise, ty2 = (-1 / l) * cruise;
2381	    this.vx += (tx2 - this.vx) * k2;
2382	    this.vy += (ty2 - this.vy) * k2;
2383	    moveAndCollide(this, game.world, this.vx, this.vy);
2384	    return true;
2385	  }
2386	
2387	  private fighterAI(game: GameHooks, player: Player | null) {    const st = game.world.store;
2388	    // ---- AI_003 尾段点光（cs:58802-58823，恒亮；放函数头防各 type 分支提前 return 漏写）----
2389	    const vidF = this.vanillaId ?? -1;
2390	    if (vidF >= 277 && vidF <= 280) {
2391	      this.lightRGB = [0.2, 0.1, 0];                                   // :58802-58804 地牢骷髅四族
2392	    } else if (vidF === 520) {
2393	      this.lightRGB = [0.3, 0.3, 0.7];                                 // :58806-58808 火星行者 Top+20
2394	      this.lightRGBAt = { x: this.cx, y: this.y + 20 };
2395	    } else if (vidF === 525) {
2396	      this.lightRGB = [0.35, 0.5, 0.1];                                // :58810-58813 腐化沙鬼 Top+15
2397	      this.lightRGBAt = { x: this.cx, y: this.y + 15 };
2398	    } else if (vidF === 526) {
2399	      this.lightRGB = [0.4, 0.4, 0.2];                                 // :58815-58818 猩红沙鬼 Top+15
2400	      this.lightRGBAt = { x: this.cx, y: this.y + 15 };
2401	    } else if (vidF === 527) {
2402	      this.lightRGB = [0.24, 0.12, 0.4];                               // :58820-58823 圣域沙鬼 Top+15
2403	      this.lightRGBAt = { x: this.cx, y: this.y + 15 };
2404	    }
2405	    // 游泳化双族 461/586（AI_003_Fighters cs:56361/:56486）：块在通用行走与白天驱散
2406	    // （cs:57732，位于其后）之前，wet 时整段接管本 tick——故 hook 在函数最前
2407	    if (this.vanillaId === 461 || this.vanillaId === 586) {
2408	      if (this.wetSwimStep(game, player, this.vanillaId as 461 | 586)) return;
2409	    }
2410	    // 美杜莎 480 蓄力石化（NPC.cs:56751-56889,位于 AI_003 通用行走之后——行走段先跑,
2411	    //  蓄力期行走被本块 velocity.X*=0.9 阻尼近似）。ai2: >0 冷却递减 / 0 蓄机判定 /
2412	    //  <-(num23+num25) 起手辉光 / >=-num23 发石化窗;贴脸|45°锥内|双向对视|视线通→
2413	    //  AddBuff(156, num24+剩余蓄力)——变身瞬间伤害/死因在 Player 石化过渡段
2414	    if (this.vanillaId === 480 && player) {
2415	      if (this.medusaChargeStep(game, player)) return;
2416	    }
2417	    // ---- Psycho 466 潜伏突袭（NPC.cs:56290-56326，AI_003 最前段——先于白天驱散）：
2418	    // 潜伏/显形两分支 return 跳过本 tick 余段（helper 自补重力+碰撞）
2419	    if (psychoStealthStep(this, game, player)) return;
2420	    // ---- 白天地表驱散（cs:57732-57775 + NotDiscouraged :60694）：
2421	    // 白天 && y<worldSurface && 类型不在昼行豁免表 → 停止索敌 + EncourageDespawn(10)，
2422	    // 沿原方向游荡（站定 2t 转向），离屏后由 CheckActive ~10t 清除。
2423	    // ★日食豁免（:60694 首条件 !Main.eclipse）：日食期间全体战士族不被驱散——
2424	    // 日食怪（Eyezor/Psycho/Nailhead/Butcher/Possessed/Fritz/Dr Man Fly）都是白天
2425	    // 刷的，缺此门会一出生就停止索敌游荡离场。
2426	    // 墓地豁免（:60698 `!Main.player[npcInstance.target].ZoneGraveyard`）：目标玩家在
2427	    // 墓地时白天不驱散——墓地白天刷出的僵尸/蛆僵尸白天照常索敌（scene 为本地玩家
2428	    // 快照，单人下与"目标玩家所在区"等价）
2429	    const daySurface = game.world.clock.isDay && !game.world.clock.eclipse
2430	      && this.cy < game.world.groundLevel * TILE
2431	      && !game.world.scene?.zoneGraveyard;
2432	    const dayActive = this.vanillaId != null
2433	      && (FIGHTER_DAY_ACTIVE.has(this.vanillaId)
2434	        || (game.world.invasionType === 4 && MARTIAN_DAY_ACTIVE.has(this.vanillaId)));
2435	    const discouraged = daySurface && !dayActive;
2436	    if (discouraged) {
2437	      this.encourageDespawn(10);
2438	      // 游荡转向（原版 else 分支 ：57783-57797：站定累计 2t 反转 direction）
2439	      if (Math.abs(this.vx) < 0.1 && this.vy === 0) {
2440	        this.state += 1;
2441	        if (this.state >= 2) { this.facing *= -1; this.state = 0; }
2442	      } else {
2443	        this.state = 0;
2444	      }
2445	      if (this.facing === 0) this.facing = 1;
2446	    } else if (player) {
2447	      // 方向：朝玩家（无玩家则保持）；confused 反向（TargetClosest :78569）
2448	      this.facing = this.seekDirX(player);
2449	    }
2450	    // ---- 419 日耀旋刃怪（AI_003_Fighters cs:57114-57173 type==419 段）：旋刃冲刺
2451	    //  状态机。该段位于原版通用行走段之前，各分支 return 跳过本 tick 行走/跳跃/远程——
2452	    //  helper 返回 true = 已自管重力+碰撞，调用方直接收尾
2453	    if (this.vanillaId === 419 && player && !player.dead && this.solenianDashAI(game, player)) {
2454	      return;
2455	    }
2456	    const dir = this.facing;
2457	    // 前方探测点（L24561-24562）：体中心前 15px、脚底上 15px
2458	    const fx = Math.floor((this.x + this.w / 2 + 15 * dir) / TILE);
2459	    const fy = Math.floor((this.y + this.h - 15) / TILE);

```


---

## 🤖 Assistant · 2026-08-19T03:15:48.893Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK — wetSwimStep for 620 (goblin shark): let me compare against vanilla cs:64118-64336. I have the 64118-64230 part above. I need 64240-64340 to see the wet block (flag27 handling — "游泳块在 walker 逻辑之前" per our comment; vanilla `if (flag27)` at 64235+). Let me read that part.

Key 620 params from vanilla (case 620):
- flag27 = wet; flag30 = false; flag16 = true; num20 = 150 (target range?); num19 = 20; dayTime handling: flag21 = !dayTime; flag24 = true; flag12 = true; flag15 = ai[1] > 40; num8 = 60; num9 = 40 (with ai[1] in (10,40] %5==0 → num9 = ai[1]-1); num12 = 811 (projectile: Blood Shark? proj 811); vector.X -= 4*direction; vector.Y -= 20; num15 = 0.15; num16 = 2.5; num13 = 600; num10 = 13; num17 = 1; num18 = 0; num11 = damage 40/30; num23 = 8; num24 *= 3; num25 = 0.9.
- Sounds at ai[1]==40/60 when ai[0]>0.
- Alpha fade-in + dust.
- dayTime → flag12 = false, flag24 = false, flag23 = true (despawn-ish).
- Night jump-out-of-water: if velocity.Y == 0 && target bottom < top && |dx| < width*3 && CanHit → compute tiles above → velocity.Y = -11/-13/-14/-15.9 (leap out of water to bite!).

Wait — this looks like the goblin shark in vanilla is NOT the chargerAI at all — it's an ImprovedWalker (aiStyle 107) with a wet swim override (flag27 = wet → the swim block at 64235+ takes over) and a shark-leap behavior. And there's projectile 811 shooting (num12 = 811 — this is the blood shark projectile from blood squid? no — 620 Goblin Shark shoots proj 811). And num23=8 speed... this is the AI_107 template (like DD2 walker with ranged attack).

Our implementation: chargerAI(game,p,1) with wetSwimStep(620) — our wetSwimStep handles wet; non-wet falls through to chargerAI generic (maxSpd 6... wait chargerAI(game,p,1)? The call is `this.chargerAI(game, p, 1)` — maxSpd = 1! Hmm: `case 107: if (vanillaId !== 620) ai107ImprovedWalkers else this.chargerAI(game, p, 1)`. So on land, goblin shark moves at max speed 1?? Let me look at vanilla non-wet 620 behavior: flag27 = wet = false → falls into AI_107 walker logic with the parameters set in case 620: flag16=true, flag21 = night (fight during night), num20=150 (aggro range), num19=20, flag12/flag24, num15=0.15 (accel?), num16=2.5, num13=600 (projectile range), num10=13 (teleport?), num17/num18, num23=8 (jump velocity?), num24*=3, num25=0.9.

I need to read the AI_107 template to understand what those flags mean and what our chargerAI(620, maxSpd=1) should be doing on land. Let me read AI_107 from 63372 to 64118 (the template part) and 64240-64400 (flag27 swim + shared tail). That's a lot; let me focus on:
1. The template's movement params (how flag27/flag16/num* drive walking) to compare with our chargerAI(maxSpd=1!).
2. The flag27 wet block 64235-64340 vs our wetSwimStep(620).

Actually — hold on. Scope check: the parent scoped me to "620 地精鲨 wet 游泳档 cs:64118-64230". So the wet tier is the focus. But the land routing to chargerAI with maxSpd=1 seems odd too. Let me read the AI_107 shared tail quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:49.526Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 63372,63560p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_107 template header to learn flag semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:49.582Z

**📎 ToolResult**

```
	private void AI_107_ImprovedWalkers()
	{
		//IL_175b: Unknown result type (might be due to invalid IL or missing references)
		//IL_08c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_08ca: Unknown result type (might be due to invalid IL or missing references)
		//IL_08db: Unknown result type (might be due to invalid IL or missing references)
		//IL_08e0: Unknown result type (might be due to invalid IL or missing references)
		//IL_140b: Unknown result type (might be due to invalid IL or missing references)
		//IL_1410: Unknown result type (might be due to invalid IL or missing references)
		//IL_090b: Unknown result type (might be due to invalid IL or missing references)
		//IL_092a: Unknown result type (might be due to invalid IL or missing references)
		//IL_2470: Unknown result type (might be due to invalid IL or missing references)
		//IL_14cc: Unknown result type (might be due to invalid IL or missing references)
		//IL_1f14: Unknown result type (might be due to invalid IL or missing references)
		//IL_19fc: Unknown result type (might be due to invalid IL or missing references)
		//IL_14f8: Unknown result type (might be due to invalid IL or missing references)
		//IL_14fd: Unknown result type (might be due to invalid IL or missing references)
		//IL_0fba: Unknown result type (might be due to invalid IL or missing references)
		//IL_0fbf: Unknown result type (might be due to invalid IL or missing references)
		//IL_0513: Unknown result type (might be due to invalid IL or missing references)
		//IL_0612: Unknown result type (might be due to invalid IL or missing references)
		//IL_05a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_1f40: Unknown result type (might be due to invalid IL or missing references)
		//IL_083e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0fe6: Unknown result type (might be due to invalid IL or missing references)
		//IL_0feb: Unknown result type (might be due to invalid IL or missing references)
		//IL_086a: Unknown result type (might be due to invalid IL or missing references)
		//IL_10fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_1035: Unknown result type (might be due to invalid IL or missing references)
		//IL_103a: Unknown result type (might be due to invalid IL or missing references)
		//IL_1060: Unknown result type (might be due to invalid IL or missing references)
		//IL_1065: Unknown result type (might be due to invalid IL or missing references)
		//IL_112a: Unknown result type (might be due to invalid IL or missing references)
		//IL_112f: Unknown result type (might be due to invalid IL or missing references)
		//IL_1150: Unknown result type (might be due to invalid IL or missing references)
		//IL_117c: Unknown result type (might be due to invalid IL or missing references)
		//IL_1181: Unknown result type (might be due to invalid IL or missing references)
		//IL_2cee: Unknown result type (might be due to invalid IL or missing references)
		//IL_0f5d: Unknown result type (might be due to invalid IL or missing references)
		bool flag = velocity.X == 0f && velocity.Y == 0f && !justHit;
		bool flag2 = false;
		bool flag3 = false;
		bool flag4 = false;
		int num = 32;
		int num2 = 15;
		float num3 = 9f;
		bool flag5 = false;
		float num4 = 40f;
		int num5 = 30;
		int num6 = 0;
		bool flag6 = false;
		bool flag7 = true;
		float num7 = 0.9f;
		bool flag8 = false;
		bool flag9 = false;
		bool flag10 = false;
		bool flag11 = false;
		bool flag12 = false;
		bool flag13 = false;
		bool flag14 = false;
		bool flag15 = true;
		int num8 = 70;
		int num9 = num8 / 2;
		float num10 = 11f;
		Vector2 vector = Vector2.Zero;
		int num11 = 1;
		int num12 = 81;
		float num13 = 700f;
		float num14 = 0f;
		float num15 = 0.1f;
		Vector2? vector2 = null;
		float num16 = 0.5f;
		int num17 = 1;
		float num18 = 1f;
		bool flag16 = false;
		float num19 = 30f;
		float num20 = 0f;
		bool flag17 = false;
		bool flag18 = true;
		bool flag19 = false;
		int num21 = 30;
		bool flag20 = false;
		bool flag21 = false;
		bool flag22 = false;
		bool flag23 = false;
		LegacySoundStyle style = null;
		int num22 = 0;
		bool flag24 = false;
		float num23 = 1f;
		float num24 = 0.07f;
		float num25 = 0.8f;
		float num26 = width / 2 + 6;
		bool flag25 = directionY < 0;
		bool flag26 = false;
		int num27 = 1;
		bool flag27 = false;
		float num28 = 5f;
		float num29 = 3f;
		float num30 = 8f;
		float amount = 0.05f;
		float amount2 = 0.04f;
		float amount3 = 0.1f;
		bool flag28 = false;
		float num31 = 0.025f;
		NPCAimedTarget targetData = GetTargetData();
		NPCUtils.NPCTargetingMethod nPCTargetingMethod = NPCUtils.TargetClosestCommon;
		if (NPCID.Sets.BelongsToInvasionOldOnesArmy[type])
		{
			nPCTargetingMethod = NPCUtils.TargetClosestOldOnesInvasion;
		}
		if (targetData.Type == NPCTargetType.NPC && Main.npc[TranslatedTargetIndex].type == 548 && Main.npc[TranslatedTargetIndex].dontTakeDamageFromHostiles)
		{
			nPCTargetingMethod(this, faceTarget: true, null);
			targetData = GetTargetData();
		}
		if (NPCID.Sets.FighterUsesDD2PortalAppearEffect[type])
		{
			if (!targetData.Invalid)
			{
				flag2 = !Collision.CanHit(base.Center, 0, 0, targetData.Center, 0, 0) && (direction == Math.Sign(targetData.Center.X - base.Center.X) || (noGravity && Distance(targetData.Center) > 50f && base.Center.Y > targetData.Center.Y));
			}
			flag2 &= ai[0] <= 0f;
		}
		if (flag2)
		{
			if (velocity.Y == 0f || Math.Abs(targetData.Center.Y - base.Center.Y) > 800f)
			{
				noGravity = true;
				noTileCollide = true;
			}
		}
		else
		{
			noGravity = false;
			noTileCollide = false;
		}
		bool flag29 = NPCID.Sets.FighterUsesDD2PortalAppearEffect[type];
		bool flag30 = true;
		SlotId val;
		switch (type)
		{
		case 576:
		case 577:
			num22 = 700;
			style = SoundID.DD2_OgreRoar;
			num26 -= 32f;
			flag5 = true;
			num6 = 60;
			num4 = 130f;
			num5 = 44;
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			num7 = 0.7f;
			if (localAI[0] > 0f)
			{
				localAI[0] -= 1f;
			}
			if (ai[0] <= 0f)
			{
				float num34 = ai[1];
				float num35 = Distance(targetData.Center);
				if (localAI[3] >= 60f)
				{
					if (num35 <= num4 + 300f && localAI[0] <= 0f)
					{
						ai[1] = 2f;
					}
					else if (num35 > num4 + 30f)
					{
						ai[1] = 1f;
					}
					else if (!(num35 > num4))
					{
						ai[1] = 0f;
						if (num34 == 1f)
						{
							ai[0] = 0f;
						}
					}
				}
				if (num34 != ai[1])
				{
					netUpdate = true;
				}
			}
			else if (ai[1] == 2f)
			{
				localAI[0] = 300f;
			}
			switch ((int)ai[1])

```


---

## 🤖 Assistant · 2026-08-19T03:16:56.752Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The AI_107 template is a large parameterized walker with defaults: num23 = 1f (walk speed?), num24 = 0.07f (accel), num25 = 0.8f... Let me look at where num23/num24/num25/num15/num16 are used in the movement part (after the type switch), to understand goblin shark's land movement: num23 = 8f (speed!), num24 *= 3 (0.21 accel), num25 = 0.9 (reverse damp?), num15 = 0.15, num16 = 2.5 (jump params?), num13 = 600 (ranged range), num12 = 811 (projectile), num10 = 13 (teleport distance?), num17=1, num18=0, num20 = 150 (aggro distance), num19 = 20 (jump height?).

Let me read the shared movement section of AI_107 (after the type switch, around 64240+ where flag27 is used, and beyond ~64340-64919). Focus on goblin shark: flag27 (wet) handling, then the walker movement with num23=8 etc., and the ranged attack (proj 811), plus teleport (num10).

Our implementation for 620 land: chargerAI(game, p, 1) → maxSpd = 1! That looks wrong — vanilla walk speed num23 = 8f. Hmm wait — need to see how num23 is used. Let me read the tail.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:56.753Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 64240,64550p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_107 shared tail with flag27 wet block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:56.802Z

**📎 ToolResult**

```
					{
						velocity.X -= num31;
					}
					else
					{
						velocity.X += num31;
					}
					if (position.Y < Main.npc[num52].position.Y)
					{
						velocity.Y -= num31;
					}
					else
					{
						velocity.Y += num31;
					}
				}
			}
			if (flag31)
			{
				velocity.Y = 0f;
			}
		}
		if (flag29)
		{
			if (localAI[3] == 0f)
			{
				alpha = 255;
			}
			if (localAI[3] == 30f)
			{
				SoundEngine.PlayTrackedSound(SoundID.DD2_EtherianPortalSpawnEnemy, base.Center);
			}
			if (localAI[3] < 60f)
			{
				localAI[3] += 1f;
				alpha -= 5;
				if (alpha < 0)
				{
					alpha = 0;
				}
				int num53 = (int)localAI[3] / 10;
				float num54 = base.Size.Length() / 2f;
				num54 /= 20f;
				int maxValue3 = 5;
				if (type == 576 || type == 577)
				{
					maxValue3 = 1;
				}
				for (int num55 = 0; num55 < num53; num55++)
				{
					if (Main.rand.Next(maxValue3) == 0)
					{
						Dust dust9 = Dust.NewDustDirect(position, width, height, 27, velocity.X * 1f, 0f, 100);
						dust9.scale = 0.55f;
						dust9.fadeIn = 0.7f;
						dust9.velocity *= 0.1f * num54;
						dust9.velocity += velocity;
					}
				}
			}
		}
		if (flag27)
		{
			noGravity = true;
			TargetClosest(faceTarget: false);
			if (collideX)
			{
				velocity.X = 0f - oldVelocity.X;
			}
			if (velocity.X != 0f)
			{
				direction = Math.Sign(direction);
			}
			if (Collision.CanHit(position, width, height, targetData.Position, targetData.Width, targetData.Height))
			{
				Vector2 value = targetData.Center - base.Center;
				value.Normalize();
				value *= num28;
				velocity = Vector2.Lerp(velocity, value, amount);
				return;
			}
			float num56 = num28;
			if (velocity.Y > 0f)
			{
				num56 = num29;
			}
			if (velocity.Y < 0f)
			{
				num56 = num30;
			}
			Vector2 value2 = new Vector2(direction, -1f);
			value2.Normalize();
			value2 *= num56;
			if (num56 < num28)
			{
				velocity = Vector2.Lerp(velocity, value2, amount2);
			}
			else
			{
				velocity = Vector2.Lerp(velocity, value2, amount3);
			}
			return;
		}
		bool flag32 = false;
		if ((flag12 || flag5) && ai[0] > 0f)
		{
			flag18 = false;
		}
		if (flag12 && ai[1] > 0f)
		{
			flag22 = true;
		}
		if (flag5 && ai[0] > 0f)
		{
			flag22 = true;
		}
		if (flag5)
		{
			if (ai[0] < 0f)
			{
				ai[0] += 1f;
				flag = false;
			}
			if (ai[0] == 0f && (velocity.Y == 0f || flag6) && targetData.Type != NPCTargetType.None && (Collision.CanHit(position, width, height, targetData.Position, targetData.Width, targetData.Height) || Collision.CanHitLine(position, width, height, targetData.Position, targetData.Width, targetData.Height)) && (targetData.Center - base.Center).Length() < num4)
			{
				ai[0] = num5;
				netUpdate = true;
			}
			if (ai[0] > 0f)
			{
				spriteDirection = direction * num27;
				if (flag7)
				{
					velocity.X *= num7;
					flag24 = true;
					flag20 = true;
					ai[3] = 0f;
					netUpdate = true;
				}
				ai[0] -= 1f;
				if (ai[0] == 0f)
				{
					ai[0] = -num6;
					netUpdate = true;
				}
			}
		}
		if (flag3 && ai[0] > 0f)
		{
			if (flag15)
			{
				nPCTargetingMethod(this, faceTarget: true, null);
				targetData = GetTargetData();
			}
			if (ai[0] == (float)num9)
			{
				Vector2 vector4 = base.Center + vector;
				Vector2 v = targetData.Center - vector4;
				v.Y -= Math.Abs(v.X) * num15;
				Vector2 vector5 = v.SafeNormalize(-Vector2.UnitY) * num10;
				for (int num57 = 0; num57 < num17; num57++)
				{
					Vector2 vector6 = vector5;
					Vector2 vector7 = vector4;
					if (vector2.HasValue)
					{
						vector6 += vector2.Value;
					}
					else
					{
						vector6 += Utils.RandomVector2(Main.rand, 0f - num16, num16);
					}
					vector7 += vector5 * num18;
					if (Main.netMode != 1)
					{
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector7, vector6, num12, num11, 0f, Main.myPlayer);
					}
				}
			}
		}
		if (flag4 && ai[0] > 0f)
		{
			if (velocity.Y != 0f && ai[0] < (float)num2)
			{
				ai[0] = num2;
			}
			if (ai[0] == (float)num)
			{
				velocity.Y = 0f - num3;
			}
		}
		if (!flag17 && flag18)
		{
			if (velocity.Y == 0f && velocity.X * (float)direction < 0f)
			{
				flag19 = true;
			}
			if (position.X == oldPosition.X || ai[3] >= (float)num21 || flag19)
			{
				ai[3] += 1f;
			}
			else if (Math.Abs(velocity.X) > 0.9f && ai[3] > 0f)
			{
				ai[3] -= 1f;
			}
			if (ai[3] > (float)(num21 * 10))
			{
				ai[3] = 0f;
			}
			if (justHit && !flag30)
			{
				ai[3] = 0f;
			}
			if (targetData.Hitbox.Intersects(base.Hitbox))
			{
				ai[3] = 0f;
			}
			if (ai[3] == (float)num21)
			{
				netUpdate = true;
				if (flag30)
				{
					noGravity = true;
					noTileCollide = true;
					position.X += direction * width * 2;
					int num58 = 20;
					float num59 = base.Size.Length() / 2f;
					num59 /= 20f;
					int maxValue4 = 5;
					if (type == 576 || type == 577)
					{
						maxValue4 = 1;
					}
					for (int num60 = 0; num60 < num58; num60++)
					{
						if (Main.rand.Next(maxValue4) == 0)
						{
							Dust dust10 = Dust.NewDustDirect(position, width, height, 27, velocity.X * 1f, 0f, 100);
							dust10.scale = 0.55f;
							dust10.fadeIn = 0.7f;
							dust10.velocity *= 3f * num59;
							dust10.noGravity = true;
							dust10.fadeIn = 1.5f;
							dust10.velocity *= 3f;
						}
					}
					return;
				}
			}
		}
		if (!flag20)
		{
			if (ai[3] < (float)num21 && flag21)
			{
				if (num22 > 0 && Main.rand.Next(num22) == 0)
				{
					SoundEngine.PlayTrackedSound(style, base.Center);
				}
				bool hasValidTarget = HasValidTarget;
				nPCTargetingMethod(this, faceTarget: true, null);
				targetData = GetTargetData();
				if (hasValidTarget != HasValidTarget)
				{
					netUpdate = true;
				}
			}
			else if (!flag22)
			{
				if (flag23)
				{
					EncourageDespawn(10);
				}
				if (velocity.X == 0f)
				{
					if (velocity.Y == 0f)
					{
						ai[2] += 1f;
						if (ai[2] >= 2f)
						{
							direction *= -1;
							spriteDirection = direction * num27;
							ai[2] = 0f;
							netUpdate = true;
						}
					}
				}
				else if (ai[2] != 0f)
				{
					ai[2] = 0f;
					netUpdate = true;
				}
				if (direction == 0)
				{
					direction = 1;
				}
			}
		}
		if (!flag24)
		{
			if (velocity.X < 0f - num23 || velocity.X > num23)
			{
				if (velocity.Y == 0f)
				{
					velocity *= num25;
				}
			}
			else if ((velocity.X < num23 && direction == 1) || (velocity.X > 0f - num23 && direction == -1))
			{
				velocity.X = MathHelper.Clamp(velocity.X + num24 * (float)direction, 0f - num23, num23);
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:17:26.429Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand the AI_107 movement core. For goblin shark 620:

**Wet (flag27)** block (64291-64334):
- noGravity = true; TargetClosest(faceTarget: false);
- collideX → velocity.X = -oldVelocity.X
- `if (velocity.X != 0f) direction = Math.Sign(direction)` — quirk (direction = sign of direction; keeps facing from TargetClosest? weird but as ours noted "620 保持 direction 原文怪癖" — ours: `if (mode !== 620) { if vx<0 facing=-1; if vx>0 facing=1 }` — hmm wait. Vanilla: `if (velocity.X != 0f) { direction = Math.Sign(direction); }` — that does nothing to direction unless direction==0. So vanilla KEEPS direction from TargetClosest(faceTarget:false) — i.e., facing player X. Ours: facing = seekDirX(player) then for mode!==620 override by vx sign; for 620 keep facing = seekDirX ✓. OK matches.
- If CanHit → velocity = Lerp(velocity, dirTo*5, 0.05) — num28 = 5 default (620 doesn't change num28/29/30: defaults num28=5, num29=3, num30=8; amount=0.05). Ours: sees → spd 5, k=1/20 = 0.05 ✓.
- Else cruise: num56 = 5 (or 3 if vy>0, 8 if vy<0); dir2 = (direction, -1) normalized * num56; Lerp amount2=0.04 if num56<num28 (i.e., 3), else amount3=0.1. Ours (2375-2382): cruise=5; vy>0→3; vy<0→8; k2 = cruise<5 ? 1/25 (0.04) : 1/10 (0.1) ✓; target (facing,-1)/norm*cruise ✓.
✓ wetSwimStep(620) matches vanilla wet block. 

Also vanilla `return`s after the flag27 block — the shared movement tail (which does the Collision movement) still runs? Again the `return` exits AI()... hmm, same question as jellyfish. Whatever — ours moveAndCollide ✓.

Note: vanilla wet block checks `Collision.CanHit(position, ..., targetData...)` — targetData is the CURRENT target (could be stale after TargetClosest(faceTarget:false)? faceTarget false means direction not updated but target updated). Ours canSeePlayer ✓.

**Land movement for 620** (case 620 params): flag24 = true initially... wait: `flag24 = true;` — but then `if (!flag24) {movement}` — flag24=true SKIPS the generic horizontal movement! Hmm — but then what moves it on land? flag24 set true means... wait re-read case 620: `flag27 = wet; flag30 = false; flag16 = true; num20 = 150f; num19 = 20f; bool dayTime = Main.dayTime; flag21 = !dayTime; flag24 = true; flag12 = true; flag15 = ai[1] > 40f; num8 = 60; num9 = 40; ...`

flag24 = true → skips `if (!flag24)` movement block? That would mean goblin shark on land doesn't accelerate horizontally at all?! Hmm wait — but later: `if (dayTime) { flag12 = false; flag24 = false; flag23 = true; }` — during DAY, flag24 = false → movement enabled (num23 = 8, num24 = 0.21, num25 = 0.9). At NIGHT, flag24 = true → movement disabled?? That seems backwards... 

Hmm wait, also `if ((flag12 || flag5) && ai[0] > 0f) flag18 = false; if (flag12 && ai[1] > 0f) flag22 = true;` — for 620: flag12=true (attack mode). flag16 = true.

I need to see more of the tail: what does flag16 do? There's more code after the movement block (jumping, animation). flag16 might be the "leap at player" thing. Let me read 64550-64919 to see flag16 handling and ranged attack (flag3? flag3 is for projectile users — 620 has num12=811 → flag3 probably set... no wait, flag3 was set where? case 620 doesn't set flag3. Hmm — flag3 default false. So the ranged attack block `if (flag3 && ai[0] > 0f)` doesn't run for 620?? But num12=811 set... Let me check case 620 again: it doesn't set flag3. Hmm — so the 811 projectile... 

Hold on, maybe I misread. Let me re-check the case 620 block: `flag27 = wet; flag30 = false; flag16 = true; num20 = 150f; num19 = 20f; bool dayTime = Main.dayTime; flag21 = !dayTime; flag24 = true; flag12 = true; flag15 = ai[1] > 40f; num8 = 60; num9 = 40; if (ai[1] > 10f && ai[1] <= 40f && (int)ai[1] % 5 == 0) num9 = (int)ai[1] - 1; num12 = 811; vector.X -= 4 * direction; vector.Y -= 20f; num15 = 0.15f; num16 = 2.5f; num13 = 600f; num10 = 13f; num17 = 1; num18 = 0f; num11 = GetAttackDamage(40,30); num23 = 8f; num24 *= 3f; num25 = 0.9f;`

Hmm wait — where's flag3 = true? Not there. So the flag3 ranged block is off? But num8/num9 (60/40) are used in... `if (flag3 && ai[0] > 0f) { if (flag15) retarget; if (ai[0] == num9) { fire num12 projectiles } }`. flag3 = false for 620?? Then num12=811 unused? That can't be. Let me search where flag3 is set — maybe in the shared section based on something. Actually flag3/flag4 are set per-type in the switch; e.g., "case 553: flag3 = true..." Hmm. Let me grep between 63560-64118 for "flag3 = true".

Wait — actually, hold on: flag15 = ai[1] > 40f for 620 — flag15 is used in the flag3 block ("if (flag15) retarget during attack"). And num8=60/num9=40 with the ai[1] in (10,40] mod 5 → num9 = ai[1]-1. This strongly suggests 620 IS a flag3 ranged attacker (the blood-shark spitter: fires proj 811 = "BloodShot"? no — 811 is the projectile used by 619 Blood Squid too). Let me grep "flag3 = true" in the 620 case... it's not in the block I read. Hmm, but wait — maybe I missed lines. The case 620 block I read fully (64117-64230). Let me search for "flag3" assignments near... Actually maybe flag3 gets set by `num12` usage — no.

Let me grep: awk lines 63372-64919 for "flag3 = true".
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:28.714Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "awk 'NR>=63372 && NR<=64919 && /flag3 = true|flag4 = true|flag16|num19|num20\\b/' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; echo ---; sed -n 64550,64921p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"flag16\\|flag12\\|num19\\|num20\\|num13\\|velocity.Y = \\|Jump\\|num23\\|num24\\|num25\" | head -40",
 "description": "Find flag3/flag16 usage in AI_107 tail"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:28.807Z

**📎 ToolResult**

```
		bool flag16 = false;
		float num19 = 30f;
				flag4 = true;
				flag3 = true;
				flag3 = true;
			flag16 = true;
			num19 = 20f;
					ai[1] = num19;
						if (flag16)
						if (flag16)
---
2:		if (flag12)
16:					ai[1] = num19;
62:						if (flag16)
71:						if (num20 != 0f && ai[1] <= 0f)
76:						ai[1] = (flag34 ? num20 : 0f);
87:					if (vector12.Length() < num13)
105:						if (flag16)
118:					if (velocity.X < 0f - num23 || velocity.X > num23 || flag35)
122:							velocity.X *= num25;
125:					else if ((velocity.X < num23 && direction == 1) || (velocity.X > 0f - num23 && direction == -1))
127:						velocity.X = MathHelper.Clamp(velocity.X + num24 * (float)direction, 0f - num23, num23);
251:						velocity.Y = -7f;
254:							velocity.Y = -8f;
259:						velocity.Y = -6f;
264:						velocity.Y = -5f;
270:						velocity.Y = -8f;
280:						velocity.Y = -5f;
287:					velocity.Y = -4f;
332:				velocity.Y = 0f;
344:				velocity.Y = -4f;
351:				velocity.Y = 0f;
364:			velocity.Y = 10f;
368:			velocity.Y = 0f;

```


---

## 🤖 Assistant · 2026-08-19T03:17:31.874Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 64551,64700p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_107 flag12 attack block for goblin shark"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:31.929Z

**📎 ToolResult**

```
		if (flag12)
		{
			if (confused)
			{
				ai[0] = 0f;
			}
			else
			{
				if (ai[1] > 0f)
				{
					ai[1] -= 1f;
				}
				if (justHit)
				{
					ai[1] = num19;
					ai[0] = 0f;
				}
				if (ai[0] > 0f)
				{
					if (flag15)
					{
						nPCTargetingMethod(this, faceTarget: true, null);
						targetData = GetTargetData();
					}
					if (ai[1] == (float)num9)
					{
						Vector2 vector8 = base.Center + vector;
						Vector2 v2 = targetData.Center - vector8;
						v2.Y -= Math.Abs(v2.X) * num15;
						Vector2 vector9 = v2.SafeNormalize(-Vector2.UnitY) * num10;
						for (int num61 = 0; num61 < num17; num61++)
						{
							Vector2 vector10 = vector8;
							Vector2 vector11 = vector9;
							if (vector2.HasValue)
							{
								vector11 += vector2.Value;
							}
							else
							{
								vector11 += Utils.RandomVector2(Main.rand, 0f - num16, num16);
							}
							vector10 += vector11 * num18;
							if (Main.netMode != 1)
							{
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector10, vector11, num12, num11, 0f, Main.myPlayer);
							}
						}
						if (Math.Abs(vector9.Y) > Math.Abs(vector9.X) * 2f)
						{
							ai[0] = ((vector9.Y > 0f) ? 1 : 5);
						}
						else if (Math.Abs(vector9.X) > Math.Abs(vector9.Y) * 2f)
						{
							ai[0] = 3f;
						}
						else
						{
							ai[0] = ((vector9.Y > 0f) ? 2 : 4);
						}
						if (flag16)
						{
							direction = ((vector9.X > 0f) ? 1 : (-1));
						}
					}
					bool flag33 = true;
					if ((velocity.Y != 0f && !flag14) || ai[1] <= 0f)
					{
						bool flag34 = false;
						if (num20 != 0f && ai[1] <= 0f)
						{
							flag34 = true;
						}
						ai[0] = 0f;
						ai[1] = (flag34 ? num20 : 0f);
					}
					else if (!flag13 || (!flag33 && (!flag14 || velocity.Y == 0f)))
					{
						velocity.X *= 0.9f;
						spriteDirection = direction * num27;
					}
				}
				if ((ai[0] <= 0f || flag13) && (velocity.Y == 0f || flag14) && ai[1] <= 0f && targetData.Type != NPCTargetType.None && Collision.CanHit(position, width, height, targetData.Position, targetData.Width, targetData.Height))
				{
					Vector2 vector12 = targetData.Center - base.Center;
					if (vector12.Length() < num13)
					{
						netUpdate = true;
						velocity.X *= 0.5f;
						ai[0] = 3f;
						ai[1] = num8;
						if (Math.Abs(vector12.Y) > Math.Abs(vector12.X) * 2f)
						{
							ai[0] = ((vector12.Y > 0f) ? 1 : 5);
						}
						else if (Math.Abs(vector12.X) > Math.Abs(vector12.Y) * 2f)
						{
							ai[0] = 3f;
						}
						else
						{
							ai[0] = ((vector12.Y > 0f) ? 2 : 4);
						}
						if (flag16)
						{
							direction = ((vector12.X > 0f) ? 1 : (-1));
						}
					}
				}
				if (ai[0] <= 0f || flag13)
				{
					bool flag35 = Distance(targetData.Center) < num14;
					if (flag35 && Collision.CanHitLine(position, width, height, targetData.Position, targetData.Width, targetData.Height))
					{
						ai[3] = 0f;
					}
					if (velocity.X < 0f - num23 || velocity.X > num23 || flag35)
					{
						if (velocity.Y == 0f)
						{
							velocity.X *= num25;
						}
					}
					else if ((velocity.X < num23 && direction == 1) || (velocity.X > 0f - num23 && direction == -1))
					{
						velocity.X = MathHelper.Clamp(velocity.X + num24 * (float)direction, 0f - num23, num23);
					}
				}
			}
		}
		if (velocity.Y == 0f)
		{
			int num62 = (int)(base.Bottom.Y + 7f) / 16;
			int num63 = (int)base.Left.X / 16;
			int num64 = (int)base.Right.X / 16;
			int num65;
			for (num65 = num63; num65 <= num64; num65++)
			{
				num65 = Utils.Clamp(num65, 0, Main.maxTilesX);
				num62 = Utils.Clamp(num62, 0, Main.maxTilesY);
				Tile tile = Main.tile[num65, num62];
				if (tile == null)
				{
					return;
				}
				if (tile.nactive() && Main.tileSolid[tile.type])
				{
					flag32 = true;
					break;
				}

```


---

## 🤖 Assistant · 2026-08-19T03:17:51.257Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I understand goblin shark land behavior. Vanilla 620 on land:
- flag12 = true (night only — during day flag12 = false → falls to wander/despawn with flag23 = true EncourageDespawn).
- Attack cycle: ai[1] counts down from num8 = 60 (windup counter, reset to num19 = 20 on justHit); when ai[0] > 0 (attacking) and ai[1] == num9 (40, or ai[1]-1 if in (10,40] %5): FIRE projectile 811 (blood shot) with arc-compensation `v2.Y -= |v2.X| * 0.15`, speed 13, spread rand ±2.5 (num16), count 1, damage 40/30, from Center + (-4*direction, -20).
- Then movement: while attacking, vx *= 0.9 damp; after attack (ai[0]<=0), movement: vx clamp accel num24 = 0.07*3 = 0.21, cap num23 = 8, reverse/speed damp num25 = 0.9.
- Leap: night jump-out (from case 620 block: when player above within 3*width and LOS, vy = -11/-13/-14/-15.9 based on tiles).
- Also num20 = 150: after volley, ai[1] = 150 (cooldown before next attack cycle).

Our 620 on land: chargerAI(game, p, 1) — maxSpd=1(!), accel 0.07, reverse damp 0.95 (vanilla 0.9), NO projectile 811 attack cycle, NO justHit reset, NO leap-out-of-water (the night leap), NO day despawn difference. So the land tier is very approximate. But wait — the goblin shark in vanilla only walks on land briefly (it flops). Hmm — actually goblin sharks spawn in water (fishing in... they spawn in the ocean? in 1.4.4, Goblin Shark spawns in water at night via fishing? They spawn submerged). The land behavior matters when knocked out.

Actually hold on — is the parent's scope "620 地精鲨 wet 游泳档 cs:64118-64230"? Yes — the wet tier. The wet tier via wetSwimStep matches vanilla (verified above ✓). The land tier is chargerAI(maxSpd=1) — vs vanilla num23=8/0.21/0.9 + attack cycle + leap. I'll report the land tier diffs as 中/低 (rare state) — the maxSpd=1 is definitely wrong vs vanilla 8. Also missing proj-811 ranged volley (which even fires while wet? No — the flag27 wet block returns early, so attacks only on land).

Hmm wait, actually — one more check: our dispatch calls chargerAI(game, p, 1) for 620 — with maxSpd=1 the shark on land barely moves (crawl at 1 px/t). Vanilla: 8 px/t run + shoots. Confirmed diff.

Also our chargerAI for 620: `if (this.vanillaId === 620 && this.wetSwimStep(game, player, 620)) return;` ✓ wet handling first ✓ (vanilla flag27 block also before the walker logic ✓ — well, actually vanilla case 620 runs in the type switch, then flag27 block runs at 64291 which is before flag12 attack etc. — ordering equivalent).

Now — the wetSwimStep 461/586 (SAND SHARK family? 461 = Sandshark? no — 461 is "Sand Shark"? Actually 461/586 — 461 = "Town slime"? no. Let me check names quickly — not needed, out of scope (fighter family).

OK. Now AI_026 chargerAI remaining members: 155, 329, 315, 410, 423, 546, and the default (Unicorn? which types have aiStyle 26?). Let me query our data for aiStyle 26 members.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:53.327Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst data = require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst list = Array.isArray(data) ? data : (data.npcs || data.entries || Object.values(data));\nconst byStyle = {};\nfor (const e of list) { (byStyle[e.aiStyle] ||= []).push(e.id + ':' + (e.name||'')); }\nfor (const s of [2,5,14,18,26,107]) console.log('aiStyle', s, '->', byStyle[s].join(', '));\nconsole.log('all styles:', Object.keys(byStyle).map(Number).sort((a,b)=>a-b).join(' '));\n\"",
 "description": "Enumerate NPC ids per aiStyle in our data"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:53.370Z

**📎 ToolResult**

```
aiStyle 2 -> 2:Demon Eye, 116:The Hungry, 133:Wandering Eye, 170:Pigron, 171:Pigron, 180:Pigron, 190:Demon Eye, 191:Demon Eye, 192:Demon Eye, 193:Demon Eye, 194:Demon Eye, 317:Demon Eye, 318:Demon Eye
aiStyle 5 -> 5:Servant of Cthulhu, 6:Eater of Souls, 23:Meteor Head, 42:Hornet, 94:Corruptor, 139:Probe, 173:Crimera, 176:Moss Hornet, 205:Moth, 210:Bee, 211:Bee, 231:Hornet, 232:Hornet, 233:Hornet, 234:Hornet, 235:Hornet, 252:Parrot, 619:Blood Squid
aiStyle 14 -> 48:Harpy, 49:Cave Bat, 51:Jungle Bat, 60:Hellbat, 62:Demon, 66:Voodoo Demon, 93:Giant Bat, 121:Slimer, 137:Illuminant Bat, 150:Ice Bat, 151:Lava Bat, 152:Giant Flying Fox, 156:Red Devil, 158:NPC_158, 226:Flying Snake, 634:Spore Bat, 660:QueenSlimeMinionPurple
aiStyle 18 -> 63:Blue Jellyfish, 64:Pink Jellyfish, 103:Green Jellyfish, 221:Squid, 242:Blood Jelly, 256:Fungo Fish
aiStyle 26 -> 86:Unicorn, 155:Wolf, 315:Headless Horseman, 329:Hellhound, 410:NPC_410, 423:Evolution Beast, 546:Angry Tumbler
aiStyle 107 -> 552:NPC_552, 553:NPC_553, 554:Etherian Goblin, 555:NPC_555, 556:NPC_556, 557:Etherian Goblin Bomber, 561:NPC_561, 562:NPC_562, 563:Etherian Javelin Thrower, 566:NPC_566, 567:Old One's Skeleton, 568:NPC_568, 569:Wither Beast, 570:NPC_570, 571:Drakin, 572:NPC_572, 573:Kobold, 576:NPC_576, 577:Ogre, 620:Goblin Shark
all styles: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 125 126 127

```


---

## 🤖 Assistant · 2026-08-19T03:18:03.603Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Family enumeration (per our data):
- aiStyle 5 (swarmerAI): 5, 6, 23, 42, 94, 139, 173, 176, 205, 210, 211, 231-235, 252, 619.
- aiStyle 14 (batAI): 48, 49, 51, 60, 62, 66, 93, 121(Slimer — wait, 121 Slimer has aiStyle 14? Vanilla FindFrame case had 121/660 group. Slimer — vanilla Slimer aiStyle 14? Actually in vanilla Slimer is aiStyle 26? Hmm — our data says 14. Let me trust our data extraction... wait, extraction was from 1405 SetDefaults. Slimer aiStyle: hmm. The FindFrame group "case 121: case 660" — hmm. Let me double check vanilla SetDefaults for 121: `else if (type == 121)` — search. Actually our list shows 121:Slimer in aiStyle 14. In 1456, Slimer aiStyle = 26? Let me verify. If our data (from 1405) says 14 and 1456 says something else, that's a data issue. Let me grep 1456 SetDefaults for type 121.
  Also 93 Giant Bat — vanilla FindFrame groups 158 with 151/152/226... The 158 special params. Giant Bat 93 gets default. ✓.
- aiStyle 18: 63, 64, 103, 221, 242, 256 (Fungo Fish — vanilla: 256 Fungo Fish, gets default light branch 0.35/0.05/0.2 ✓ ours `else if (vid !== 221 && vid !== 242)` ✓).
- aiStyle 26 (chargerAI): 86 Unicorn, 155 Wolf, 315, 329, 410, 423, 546.
- aiStyle 107: DD2 walkers + 620.

Let me verify Slimer (121) aiStyle in 1456 SetDefaults:
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:05.772Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"else if (type == 121)$\\|else if (type == 86)$\\|else if (type == 155)$\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; for t in 121 86 155 410; do ln=$(grep -n \"else if (type == $t)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -1 | cut -d: -f1); echo \"=== type $t @ $ln ===\"; sed -n \"${ln},$((ln+10))p\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -m2 \"aiStyle\\|width\\|height\"; done",
 "description": "Verify aiStyle for 121/86/155/410 in 1456 SetDefaults"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:05.980Z

**📎 ToolResult**

```
9858:		else if (type == 86)
10398:		else if (type == 121)
10893:		else if (type == 155)
88614:			else if (type == 86)
88636:			else if (type == 155)
=== type 121 @ 10398 ===
			width = 40;
			height = 30;
=== type 86 @ 9858 ===
			width = 46;
			height = 42;
=== type 155 @ 10893 ===
			width = 46;
			height = 30;
=== type 410 @ 15006 ===
			width = 22;
			height = 22;

```


---

## 🤖 Assistant · 2026-08-19T03:18:10.775Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for t in 121 86 155 410 329 315 546; do ln=$(grep -n \"else if (type == $t)\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -1 | cut -d: -f1); echo \"=== type $t @ $ln ===\"; sed -n \"${ln},$((ln+6))p\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep \"aiStyle\"; done",
 "description": "Get aiStyle lines for charger family types"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:11.168Z

**📎 ToolResult**

```
=== type 121 @ 10398 ===
			aiStyle = 14;
=== type 86 @ 9858 ===
			aiStyle = 26;
=== type 155 @ 10893 ===
			aiStyle = 26;
=== type 410 @ 15006 ===
			aiStyle = 26;
=== type 329 @ 13107 ===
			aiStyle = 26;
=== type 315 @ 12910 ===
			aiStyle = 26;
=== type 546 @ 15903 ===
			aiStyle = 26;

```


---

## 🤖 Assistant · 2026-08-19T03:19:00.574Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: Slimer 121 is aiStyle 14 (bat), matches our data. chargerAI family = {86 Unicorn, 155 Wolf, 315 Headless Horseman, 329 Hellhound, 410 Sroller, 423 Evolution Beast, 546 Angry Tumbler} + 620 special.

Now let me systematically diff chargerAI against AI_026 defaults:

Vanilla AI_026 core (cs:62809+):
- num = 30 (stuck threshold), num2 = 10.
- flag2 (turnaround while grounded moving against direction) → ai[3] += 1.
- Per-type overrides. Default: num11 = 6, num12 = 0.07.
- Stuck logic: `if (position.X == oldPosition.X || ai[3] >= num || flag2) ai[3] += 1; else if (ai[3] > 0) ai[3] -= 1;` — decrement when moving. `if (ai[3] > num*num2) ai[3] = 0`. justHit → ai[3] = 0.
- `if (num9 < 200 && !flag3) ai[3] = 0` (player within 200 → reset count) ✓ ours (4290).
- ai[3] >= num → wander (turn around every 2 ticks of standing); else TargetClosest ✓ ours approximates via facing flip (4289: stuckT >= 30 → flip).
- Movement: `if (!flag && (velocity.Y == 0f || wet || (velocity.X <= 0 && direction < 0) || (velocity.X >= 0 && direction > 0)))` — NOTE the gate: movement accel only applies when grounded OR wet OR moving toward direction. Ours applies accel unconditionally (4298-4299). Hmm — for a charging unicorn in the air, vanilla skips the horizontal accel (momentum preserved) — but the gate `velocity.X >= 0 && direction > 0` includes moving toward direction anyway, so effectively always except when airborne AND moving away from direction. Minor.
  - 155 Wolf: reverse damp 0.95 ✓ (ours generic).
  - 329 Hellhound: reverse damp 0.9 + `if (direction > 0 && velocity.X < 3) velocity.X += 0.1; if (direction < 0 && velocity.X > -3) velocity.X -= 0.1;` — extra push. Ours missing (generic 0.95 damp only).
  - 315: damp 0.95 + if |vx| > num11 && grounded → velocity *= 0.8; else standard accel 0.07 toward 6.
  - 410: damp 0.9, num11=6, num12=0.2.
  - 423: damp 0.85, num11=10, num12=0.2.
  - 546: damp 0.92, num11 = 4 + lerp(0.6,1,|wind|)*sign(wind)*3*direction (!), num12=0.05.
  - Default (86 Unicorn): num11=6, num12=0.07, no damp (else-branch falls to shared accel).
- Overspeed: `if (velocity.X < -num11 || velocity.X > num11) { if (velocity.Y == 0) velocity *= 0.8; }` (0.8 on BOTH axes? `velocity *= 0.8f` — Vector2 *= scalar → both axes! yes). Ours: no overspeed handling?? Ours chargerAI has no "if |vx|>maxSpd && grounded → velocity *= 0.8". Hmm wait — when would |vx| exceed maxSpd? After hit knockback or when num11 changes (423→10, or 546 wind). Ours: reverse damp only. Missing overspeed damp — minor (knockback recovery differs: vanilla grounded overshoot decays 0.8/t).
- Step-up ✓ ours (4302-4311) — vanilla cs:63075-63155 has the gfxOffY step logic with 16.1 check ✓ approximate but present. Vanilla also sets stepSpeed 1/2 — cosmetic.
- Jump ladder ✓ ours (4325-4337): vanilla 63157-63290: checks fy-2 solid → -8.5 (if fy-3 also solid) else -7.5; fy-1 → -7; y+h - fy*16 > 20 && fy solid → -6; else directionY<0 or |vx|>3 (and for 410/423 extra clearance checks) → -8. Ours ✓ mostly matches incl. the flag7 (410/423) clearance checks via the else branch (4334: !solidAt(fx,fy+1) && !solidAt(fx+dir,fy+1) && !solidAt(fx+dir,fy+2)) — hmm vanilla flag7 (410/423) requires NOT(tile[num22+direction, num23+3]) too: `(!flag7 || !Main.tile[num22 + direction, num23 + 3].nactive() || ...)` — ours checks fx+dir,fy+2 but not fx+dir,fy+3. Minor.
  - Also vanilla last else requires `(directionY < 0 || Math.Abs(velocity.X) > 3f)` — ours else branch requires only the !solid checks (no |vx|>3 gate) → may leap -8 off small ledges too eagerly. Vanilla gates the cliff-jump on |vx| > 3 or moving up. Ours missing the |vx|>3 condition. Low-medium: unicorn jumps -8 off every ledge even at crawl speed.
  - Also `num24 = spriteDirection; if (type == 423 || 410 || 546) num24 *= -1;` then `if ((velocity.X < 0 && num24 == -1) || (velocity.X > 0 && num24 == 1))` — the jump ladder only when moving in facing direction. Ours: `if (vxSign === dir && vxSign !== 0)` — uses facing not spriteDirection; for 423/410/546 spriteDirection is inverted relative to direction so vanilla gate is inverted for them... wait: num24 = spriteDirection (=direction normally? spriteDirection is set elsewhere from direction). For 423/410/546 num24 = -spriteDirection. And the check `(velocity.X < 0 && num24 == -1) || (velocity.X > 0 && num24 == 1)` — for those types the jump ladder triggers when moving OPPOSITE to facing?? Hmm — that's because those types' spriteDirection = -direction by default (546 explicitly sets spriteDirection = -direction at the end). For 410/423, spriteDirection is set where? Default spriteDirection = direction in most AI. Hmm — this is the "spriteDirection vs direction" subtlety; low priority, skip.
- 315: light ✓ ours; MISSING: rider projectile 1001 every 480t + horse-head dust (frames 4-7). Also missing `(type == 329 || 315) && !pumpkinMoon → EncourageDespawn(10)` gate.
- 410: MISSING entire suicide-burst (ai[1] >= 240 or player-above-within-800 → 3× proj 538 + life=0 + HitEffect death).
- 423: MISSING entire charge-shot state machine (ai[2]==1: 60t windup, at 30 fire proj 575 backwards at 7, then cooldown -320..-601; entry: ai[1]>=180 && dist<500 && grounded).
- 546: MISSING wind-speed modulation (num11 = 4 + wind*3*direction), rotation += vx*0.05, spriteDirection = -direction, desert-zone despawn gate, flock separation (num2=4 branch at top).
- 155/329 shared jump-on-player: `if (velocity.Y == 0 && num9 < 100 && |vx| > 3 && moving toward player) velocity.Y -= 4` ✓ ours has it ONLY for 546 (4317)! Vanilla has it for 155 and 329 (cs:63003-63009 `else if (type == 155 || type == 329)`), and separately for 546 with sound (63012). Ours: only 546. So Wolf 155 and Hellhound 329 miss the pounce jump. 中.

Wait — check ours 4317: `if (this.vanillaId === 546 && this.vy === 0 && ...)` — yes only 546. Vanilla: 155/329 pounce (no sound), 546 pounce + sound. Ours missing 155/329 pounce. Confirmed.

Also default Unicorn 86: vanilla cs:63056: `if (ai[3] < num) { TargetClosest } else { wander }` ✓ ours approx. 

Ours stuckT increments when `Math.abs(this.x - xBefore) < 0.01` ✓ vanilla `position.X == oldPosition.X`. Vanilla ALSO increments ai[3] for flag2 (grounded moving against direction) — ours doesn't (but reverse-damp handles). Vanilla decrements when moving (else if ai[3] > 0 → -=1) — ours never decrements stuckT except player-near reset. Low.

OK, chargerAI done. Now:

1. floatEyeAI type-specific branches — vanilla AI_002_FloatingEye (52673-53195). 主体 fixed. Let me grep for type-specific branches inside AI_002.
2. skeletronHandAI (AI_012, bossAI.ts) vs vanilla 22289-22604.
3. eocAI quick spot-check.
4. Also our flyAI (6752) — legacy non-vanilla path (only used for legacy keys demon_eye/cave_bat/servant_of_cthulhu — the `else switch (this.key)` fallback — those keys are legacy; vanilla-driven enemies never hit it. Skip? It's for legacy saves. Mention in enumeration as legacy fallback, low priority.)

Also — "其他 Enemy.ts aiStyle switch 里未列但属飞行/水生的 case": flying/aquatic cases in the switch: case 2 floatEyeAI (fixed), case 4 eocAI, case 5 swarmerAI ✓ audited, case 14 batAI ✓, case 16 swimAI (flag22 fixed; other checks?), case 18 jellyfishAI ✓, case 22 ghostAI (flying, through-walls), case 17 vultureAI (fixed per memory), case 44 flyingSwarmerAI (flying fish — AI_044), case 56 dungeonSpiritAI, case 49 angryNimbusAI, case 9 bouncingBallAI (flying-ish balls), case 10 cursedSkullAI (audited above — wait, cursedSkull is in my scope? "水母外的 aiStyle 4/14 专属分支" — no, AI_010 not assigned. I read it anyway; it looks well-done per memory book-mimic batch), case 20 blazingWheel, case 21 spikeBall (traps). The instruction says to enumerate unlisted flying/aquatic cases and report those in my scope — i.e., report which cases exist that are flying/aquatic beyond the listed families. I'll enumerate them and give quick spot-checks on the most relevant ones within reason. Since "控制密度" — I'll spot check ghostAI (22) and dungeonSpiritAI (56) + swimAI details vs vanilla quickly, but not deep-dive DD2/lunar stuff (those were other batches).

Actually, given time constraints, priorities: the assigned families deep; the enumeration listing; maybe quick spot check of swimAI numbers (since "swimAI flag22 已修勿重报" — only flag22 is protected; other swim diffs count). Let me verify swimAI against vanilla AI_016 (23549-24078) quickly — key numbers: Arapaima 0.25/0.2 ±7/4 (ours 4513-4520 ✓ but ours `if (this.vx > 8) this.vx = 7;` — that's `> 8 → 7`, vanilla is `if (velocity.X > 7) velocity.X = 7`? Let me check vanilla 23829-23845).

Let me read vanilla swim AI_016 attack block.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:01.113Z · glm-x-preview-260804

```
我先抽查一下原版 AI_016 游泳攻击代码块以及 AI_002 飞行眼睛的类型分支。
```


---

## 🤖 Assistant · 2026-08-19T03:19:01.706Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 23810,23900p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_016 attack-form movement"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:01.767Z

**📎 ToolResult**

```
						}
						else if (velocity.Y < 0f)
						{
							velocity.Y = Math.Abs(velocity.Y);
							directionY = 1;
							this.ai[0] = 1f;
						}
					}
				}
				if (type == 102)
				{
					Lighting.AddLight((int)(position.X + (float)(width / 2) + (float)(direction * (width + 8))) / 16, (int)(position.Y + 2f) / 16, 0.07f, 0.04f, 0.025f);
				}
				if (flag22)
				{
					if (this.ai[0] != 0f)
					{
						this.ai[0] = 0f;
						netUpdate = true;
					}
					TargetClosest();
					if (type == 157)
					{
						if (velocity.X > 0f && direction < 0)
						{
							velocity.X *= 0.95f;
						}
						if (velocity.X < 0f && direction > 0)
						{
							velocity.X *= 0.95f;
						}
						velocity.X += (float)direction * 0.25f;
						velocity.Y += (float)directionY * 0.2f;
						if (velocity.X > 8f)
						{
							velocity.X = 7f;
						}
						if (velocity.X < -8f)
						{
							velocity.X = -7f;
						}
						if (velocity.Y > 5f)
						{
							velocity.Y = 4f;
						}
						if (velocity.Y < -5f)
						{
							velocity.Y = -4f;
						}
					}
					else if (type == 65 || type == 102 || type == 692)
					{
						velocity.X += (float)direction * 0.15f;
						velocity.Y += (float)directionY * 0.15f;
						if (velocity.X > 5f)
						{
							velocity.X = 5f;
						}
						if (velocity.X < -5f)
						{
							velocity.X = -5f;
						}
						if (velocity.Y > 3f)
						{
							velocity.Y = 3f;
						}
						if (velocity.Y < -3f)
						{
							velocity.Y = -3f;
						}
					}
					else
					{
						velocity.X += (float)direction * 0.1f;
						velocity.Y += (float)directionY * 0.1f;
						if (velocity.X > 3f)
						{
							velocity.X = 3f;
						}
						if (velocity.X < -3f)
						{
							velocity.X = -3f;
						}
						if (velocity.Y > 2f)
						{
							velocity.Y = 2f;
						}
						if (velocity.Y < -2f)
						{
							velocity.Y = -2f;
						}

```


---

## 🤖 Assistant · 2026-08-19T03:19:02.417Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 52673,53195p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"type ==\\|type >\" | head -20",
 "description": "Find type branches in AI_002_FloatingEye"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:02.510Z

**📎 ToolResult**

```
3:		if ((type == 170 || type == 171 || type == 180) && Main.rand.Next(1000) == 0)
53:		if (type == 170 || type == 171 || type == 180)
152:		else if (type == 116)
229:		else if (type == 133)
437:		if ((type == 2 || type == 133 || type == 190 || type == 191 || type == 192 || type == 193 || type == 194) && Main.rand.Next(40) == 0)
470:			if (type == 176)
503:		if ((type == 361 || type == 445 || type == 687) && wet)

```


---

## 🤖 Assistant · 2026-08-19T03:19:14.571Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Swim attack form matches ours (Arapaima >8→7 quirk is literally vanilla ✓ — ours faithfully copied it; the 65/102/692 ±5/±3 ✓; default ±3/±2 ✓). Good.

Now vanilla AI_002_FloatingEye type branches (offsets relative to 52673):
- +3 (52676): Pigron 170/171/180 — rand(1000)==0 something (1/1000 — spawn dust? actually this is at function head; likely shimmer or pigron-special: `Main.rand.Next(1000) == 0` — maybe transform pigron variants?).
- +53 (52726): 170/171/180 pigron block.
- +152 (52825): 116 The Hungry.
- +229 (52902): 133 Wandering Eye.
- +437 (53110): demon eye family dust (1/40).
- +470 (53143): type 176?? inside wet block? "if (type == 176)" at 53143 — moss hornet?? in AI_002? weird — probably a different context (maybe `num` shadowing). Actually 176 in floatEye? Hmm — maybe it's "Ichor Sticker"? no. Whatever.
- +503 (53176): (361/445/687) && wet — floatEye family wet! 361 = Ice Tortoise? no... 361 = "Flying Antlion"? 361 = "??", 445 = "??", 687 = "??". These are floatEye members with wet handling: e.g., 361 = "Cochineal"? hmm. Actually 361 might be "Gnome"? no. Let me check our floatEyeAI for the wet branch. Since floatEyeAI 主体 fixed — but the wet branch for 361/445/687 might be missing! That's a "wet 浮力族表" item which IS my scope! Let me read vanilla 53110-53195 and our floatEyeAI.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:15.145Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 53100,53195p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_002 wet branch for types 361/445/687"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:15.309Z

**📎 ToolResult**

```
				{
					velocity.Y -= 0.03f;
				}
				if (velocity.Y > num3)
				{
					velocity.Y = num3;
				}
			}
		}
		if ((type == 2 || type == 133 || type == 190 || type == 191 || type == 192 || type == 193 || type == 194) && Main.rand.Next(40) == 0)
		{
			position += netOffset;
			int num4 = Dust.NewDust(new Vector2(position.X, position.Y + (float)height * 0.25f), width, (int)((float)height * 0.5f), 5, velocity.X, 2f);
			Main.dust[num4].velocity.X *= 0.5f;
			Main.dust[num4].velocity.Y *= 0.1f;
			position -= netOffset;
		}
		if (wet && type != 170 && type != 171 && type != 180)
		{
			if (velocity.Y > 0f)
			{
				velocity.Y *= 0.95f;
			}
			velocity.Y -= 0.5f;
			if (velocity.Y < -4f)
			{
				velocity.Y = -4f;
			}
			TargetClosest();
		}
	}

	private void StingerExplosion()
	{
		int num = Main.rand.Next(4, 9);
		for (int i = 0; i < num; i++)
		{
			float num2 = 8f;
			Vector2 vector = new Vector2(Main.rand.NextFloat() - 0.5f, Main.rand.NextFloat() - 0.5f);
			vector.Normalize();
			vector *= num2;
			int num3 = (int)(10f * scale);
			if (type == 176)
			{
				num3 = (int)(30f * scale);
			}
			int num4 = 55;
			int num5 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector.X, vector.Y, num4, num3, 0f, Main.myPlayer);
			Main.projectile[num5].timeLeft = 300;
		}
	}

	public static bool DespawnEncouragement_AIStyle2_FloatingEye_IsDiscouraged(int npcID, Vector2 npcPosition, int target = 255)
	{
		if (!Main.player[target].ZoneGraveyard && Main.IsItDay() && (double)npcPosition.Y <= Main.worldSurface * 16.0)
		{
			if (npcID != 2 && npcID != 133 && npcID != 190 && npcID != 191 && npcID != 192 && npcID != 193 && npcID != 194 && npcID != 317)
			{
				return npcID == 318;
			}
			return true;
		}
		return false;
	}

	private bool AI_007_TownEntities_IsInAGoodRestingSpot(int tileX, int tileY, int idealRestX, int idealRestY)
	{
		if (!Main.dayTime && ai[0] == 5f)
		{
			if (Math.Abs(tileX - idealRestX) <= 7)
			{
				return Math.Abs(tileY - idealRestY) <= 7;
			}
			return false;
		}
		if ((type == 361 || type == 445 || type == 687) && wet)
		{
			return false;
		}
		if (tileX == idealRestX)
		{
			return tileY == idealRestY;
		}
		return false;
	}

	private bool SolidOrSlopedTileOrPlatform(Tile tile)
	{
		if (tile != null && tile.active() && ((Main.tileSolid[tile.type] && !Main.tileSolidTop[tile.type]) || TileID.Sets.Platforms[tile.type]))
		{
			return !tile.inActive();
		}
		return false;
	}

	private void AI_007_FindGoodRestingSpot(int myTileX, int myTileY, out int floorX, out int floorY)

```


---

## 🤖 Assistant · 2026-08-19T03:19:15.398Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 185,
 "offset": 3595
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:15.420Z

**📎 ToolResult**

```
3595	  private floatEyeAI(game: GameHooks, player: Player | null) {
3596	    // 猪龙 grunt（AI_002 :52677-52680）：170/171/180 → PlaySound(29,9)=Zombie_9 1/1000
3597	    if ((this.vanillaId === 170 || this.vanillaId === 171 || this.vanillaId === 180)
3598	      && Math.floor(Math.random() * 1000) === 0) {
3599	      game.playSfxWav?.('Zombie_9', 1, this.cx, this.cy);
3600	    }
3601	    // 撞墙反弹（collideX/Y → hitWall/hitHead/onGround + 上一帧速度近似 oldVelocity）
3602	    const oldVx = this.vx, oldVy = this.vy;
3603	    // ---- 白天地表驱散（cs:52707-52715 + IsDiscouraged :53152）：
3604	    // 白天 && y≤worldSurface && 类型 ∈ 眼族昼散表 → EncourageDespawn(10) +
3605	    // 保持水平运动方向、directionY=-1 向上飞离（离屏后 CheckActive ~10t 清除）。
3606	    // 墓地豁免（:53154 `!Main.player[target].ZoneGraveyard` 首条件）：目标玩家在墓地时
3607	    // 恶魔眼白天不驱散（scene 为本地玩家快照，单人下等价）
3608	    const day = game.world.clock.isDay && !game.world.scene?.zoneGraveyard;
3609	    const eyeDiscouraged = day && this.cy <= game.world.groundLevel * TILE
3610	      && this.vanillaId != null && EYE_DAY_DESPAWN.has(this.vanillaId);
3611	    let dirX: number, dirY: number, cx: number, cy: number;
3612	    if (eyeDiscouraged) {
3613	      this.encourageDespawn(10);
3614	      dirX = oldVx > 0 ? 1 : -1;   // 原版保持水平方向（direction=-1，vx>0 时翻 1）
3615	      dirY = -1;
3616	      this.dirY = -1;              // 原版 directionY=-1 随 discouragement 持续
3617	      cx = 4; cy = 2.5;
3618	    } else if (!player) {
3619	      // 玩家死亡/无目标（原版语义：TargetClosest 落空是【无操作】——
3620	      // TargetClosestUpgraded :78421 无有效玩家时 num4 哨兵未动直接 return，
3621	      // direction/directionY 全部保持原值）→ 保持当前朝向 + 沿用上次垂直方向
3622	      // 滑行，由 despawn 系统（CheckActive 死亡玩家不重置屏内）750t 倒数消散。
3623	      // 曾写 dirX=-sign(vx)（朝自己速度的反方向看 → X 反复减速过零 = 左右朝向
3624	      // 抽搐）+ 恒 dirY=-1（无条件上飞——上飞是白天驱散分支专属），2026-08-19 修正
3625	      dirX = this.facing;
3626	      dirY = this.dirY;
3627	      cx = 4; cy = 2.5;
3628	    } else {
3629	      // TargetClosest（confused 反转 X；directionY 原版不反转）
3630	      dirX = this.seekDirX(player);
3631	      dirY = player.cy > this.cy ? 1 : -1;
3632	      this.dirY = dirY;   // 持久化（玩家死亡后沿用最后垂直方向,≈原版 directionY 保留）
3633	      const rage = this.vanillaId === 133 && this.hp < this.maxHp * 0.5;
3634	      cx = rage ? 6 : 4;
3635	      cy = rage ? 4 : 2.5;
3636	    }
3637	    this.facing = dirX;
3638	    // X 轴（L19211-19237 结构）：未越过目标且未达上限 → 朝目标加速，带两档修正
3639	    if (dirX === -1 && this.vx > -cx) {
3640	      this.vx -= 0.1;
3641	      if (this.vx > 0) this.vx -= 0.1;
3642	      if (this.vx < -cx) this.vx = -cx;
3643	    } else if (dirX === 1 && this.vx < cx) {
3644	      this.vx += 0.1;
3645	      if (this.vx < 0) this.vx += 0.1;
3646	      if (this.vx > cx) this.vx = cx;
3647	    }
3648	    // Y 轴（步长 0.1/0.04，档位简化为 0.1+逆风修正）
3649	    if (dirY === -1 && this.vy > -cy) {
3650	      this.vy -= 0.1;
3651	      if (this.vy > 0) this.vy -= 0.05;
3652	      if (this.vy < -cy) this.vy = -cy;
3653	    } else if (dirY === 1 && this.vy < cy) {
3654	      this.vy += 0.1;
3655	      if (this.vy < 0) this.vy += 0.05;
3656	      if (this.vy > cy) this.vy = cy;
3657	    }
3658	    moveAndCollide(this, game.world, this.vx, this.vy);
3659	    // 碰撞反弹（在碰撞后按旧速度算）
3660	    if (this.hitWall) {
3661	      this.vx = -oldVx * 0.5;
3662	      if (this.facing === -1 && this.vx > 0 && this.vx < 2) this.vx = 2;
3663	      if (this.facing === 1 && this.vx < 0 && this.vx > -2) this.vx = -2;
3664	    }
3665	    if (this.hitHead || this.onGround) {
3666	      this.vy = -oldVy * 0.5;
3667	      if (this.vy > 0 && this.vy < 1) this.vy = 1;
3668	      if (this.vy < 0 && this.vy > -1) this.vy = -1;
3669	    }
3670	    // wet 浮力尾段（cs:53117-53127）：wet 且非 170/171/180（猪龙三色变种，照常潜行）→
3671	    // vy>0 ×0.95 阻下落、恒 -0.5 上浮、下限 -4 并重新索敌——飘浮眼入水弹出水面
3672	    // 而非照常追击；此前缺失（"怪物下水照常攻击"主诉的飞行侧成因）
3673	    if (this.wet && this.vanillaId !== 170 && this.vanillaId !== 171 && this.vanillaId !== 180) {
3674	      if (this.vy > 0) this.vy *= 0.95;
3675	      this.vy -= 0.5;
3676	      if (this.vy < -4) this.vy = -4;
3677	      if (player) this.facing = this.seekDirX(player);   // TargetClosest
3678	    }
3679	    // ---- 点光（cs:52826-52828）：116 饿魂 II（脱落追击态）Center (0.3,0.2,0.1) 恒亮
3680	    if (this.vanillaId === 116) this.lightRGB = [0.3, 0.2, 0.1];
3681	  }
3682	
3683	  /** AI_005 噬魂怪族（NPC.cs:17567-17790）"蜂群"AI：
3684	   *  目标方向 8px 网格量化 → 期望速度 = 归一化方向 × maxSpd；
3685	   *  ai[0] 环绕摆动（>0 加 vy、|>100| 加 vx，±200 循环）产生盘旋蜂群感（L17742-17752）；
3686	   *  近距(<150) 附加 0.007×期望速度制导（L17754-17757）；
3687	   *  各轴以 accel 步进逼近期望速度（L17774-17789）。
3688	   *  速度表（L17610-17617）：Eater of Souls(6)/Crimera(173) 4/0.02，默认 6/0.05 */
3689	  /** AI_013 植物/攀爬者族(NPC.cs:22604-22700 一比一):锚点格(ai0/ai1)固定,
3690	   *  朝玩家伸展(range 内钳制),逆向加速 ×1.5;锚点格被挖掉即死;300-450 tick 周期 range ×1.3。
3691	   *  攀爬者 101: range 175、accel 0.035、noTileCollide 幽灵位移(穿墙摆动)。 */
3692	  private plantAI(game: GameHooks, player: Player | null) {
3693	    const st = game.world.store;
3694	    // 未初始化(-1120)自愈：绕过 VanillaSpawner 锚点传参的生成路径(fromVanilla/
3695	    // spawnNpcByVanilla/微光 Transform 等)从这里进——用当前格补锚点,否则下方
3696	    // ai0<0 判定会即刻误杀(2026-08-13 ai0 陷阱清查)
3697	    if (this.ai0 === -1120) {
3698	      this.ai0 = Math.floor(this.cx / TILE);
3699	      this.ai1 = Math.floor(this.cy / TILE);
3700	    }
3701	    // 锚点格失活 → 死亡(原版 :22608-22620)
3702	    if (this.ai0 < 0 || this.ai1 < 0 || !st.inBounds(this.ai0, this.ai1)
3703	      || st.type[st.idx(this.ai0, this.ai1)] === 0) {
3704	      this.dead = true;
3705	      return;
3706	    }
3707	    let range = 150;  // 默认 num218(:22632)；族内覆盖(:22636-22658)
3708	    let accel = 0.035; // num217(:22630)
3709	    if (this.vanillaId === 43) range = 250;          // 食人怪（getGoodWorld 350 未接入）
3710	    else if (this.vanillaId === 101) range = 175;    // 邪恶触手
3711	    else if (this.vanillaId === 259) range = 100;    // 真菌球
3712	    else if (this.vanillaId === 175) { range = 500; accel = 0.05; }   // 怒牙捕兽草
3713	    else if (this.vanillaId === 260) { range = 350; accel = 0.15; }   // 巨型真菌球
3714	    // ai2:300-450 tick 周期 → range ×1.3(:22644-22653)
3715	    this.ai2 += 1;
3716	    if (this.ai2 > 300) {
3717	      range = Math.floor(range * 1.3);
3718	      if (this.ai2 > 450) this.ai2 = 0;
3719	    }
3720	    const ax = this.ai0 * 16 + 8, ay = this.ai1 * 16 + 8;
3721	    // 目标点 = 锚点 + 朝玩家偏移(钳制在 range 内,:22655-22665)
3722	    let ox = 0, oy = 0;
3723	    if (player) {
3724	      ox = player.cx - this.w / 2 - ax;
3725	      oy = player.cy - this.h / 2 - ay;
3726	      const d = Math.hypot(ox, oy);
3727	      if (d > range) { ox = ox / d * range; oy = oy / d * range; }
3728	    }
3729	    // 各轴逼近,逆向 ×1.5(:22666-22699)
3730	    const tx = ax + ox, ty = ay + oy;
3731	    if (this.x < tx) {
3732	      this.vx += accel;
3733	      if (this.vx < 0 && ox > 0) this.vx += accel * 1.5;
3734	    } else if (this.x > tx) {
3735	      this.vx -= accel;
3736	      if (this.vx > 0 && ox < 0) this.vx -= accel * 1.5;
3737	    }
3738	    if (this.y < ty) {
3739	      this.vy += accel;
3740	      if (this.vy < 0 && oy > 0) this.vy += accel * 1.5;
3741	    } else if (this.y > ty) {
3742	      this.vy -= accel;
3743	      if (this.vy > 0 && oy < 0) this.vy -= accel * 1.5;
3744	    }
3745	    this.facing = this.vx > 0 ? 1 : -1;
3746	    // ---- 头部旋转（cs:22778-22794）：259/260 真菌球恒 +π/2；其余（43 食人怪/101 触手/175）
3747	    // 朝玩家伸展方向 atan2(num220,num219)，目标在左（num219<0）+π 且 spriteDirection=-1——
3748	    // 旋转+镜像组合保证头从不倒挂（此前只镜像不旋转 → 横向硬转）
3749	    if (this.vanillaId === 259 || this.vanillaId === 260) {
3750	      this.visAngle = Math.atan2(oy, ox) + Math.PI / 2;
3751	    } else {
3752	      if (ox > 0) { this.facing = 1; this.visAngle = Math.atan2(oy, ox); }
3753	      else if (ox < 0) { this.facing = -1; this.visAngle = Math.atan2(oy, ox) + Math.PI; }
3754	    }
3755	    // ---- 爬行者 101 诅咒焰（cs:22823-22856）：ai[3] 每 tick +1，≥120 且自身未嵌实心
3756	    // 且有视线 → 喷诅咒焰（速 10、伤 22、散布 ±10）；条件不满足回退 ai[3]=100（20t 重试）
3757	    if (this.vanillaId === 101 && player && !player.dead) {
3758	      this.ai3 += 1;
3759	      if (this.ai3 >= 120) {
3760	        let embedded = false;
3761	        for (let tx = Math.floor(this.x / TILE); tx <= Math.floor((this.x + this.w - 0.01) / TILE) && !embedded; tx++) {
3762	          for (let ty = Math.floor(this.y / TILE); ty <= Math.floor((this.y + this.h - 0.01) / TILE); ty++) {
3763	            if (st.isSolid(tx, ty)) { embedded = true; break; }
3764	          }
3765	        }
3766	        if (!embedded && this.canSeePlayer(st, player)) {
3767	          this.shootDart(game, this.cx, this.cy,
3768	            player.cx - this.cx + (Math.random() * 20 - 10),
3769	            player.cy - this.cy + (Math.random() * 20 - 10), 10, 22, 96);
3770	          this.ai3 = 0;
3771	        } else this.ai3 = 100;
3772	      }
3773	    }
3774	    // noTileCollide:幽灵位移(原版 plants 不做 tile 碰撞)
3775	    this.x += this.vx;
3776	    this.y += this.vy;
3777	  }
3778	
3779	  private swarmerAI(game: GameHooks, player: Player | null) {

```


---

## 🤖 Assistant · 2026-08-19T03:19:24.938Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
floatEyeAI: wet branch ✓ present (3670-3678), matching vanilla (all but pigrons). The 361/445/687 wet mention was in AI_007 (unrelated — it was IsInAGoodRestingSpot). floatEyeAI main structure matches (rage for 133 Wandering Eye at <50% hp: 6/4 — vanilla 133 block at +229... let me trust it since 主体 fixed).

Wait — one thing in floatEyeAI: vanilla movement for X axis: `velocity.X -= 0.1; if (velocity.X > 4) velocity.X -= 0.1; else if (velocity.X > 0) velocity.X += 0.05;` — ours (3639-3647): `this.vx -= 0.1; if (this.vx > 0) this.vx -= 0.1;` — uses threshold 0 instead of 4! Hmm — but comment says "L19211-19237 结构...带两档修正". The 主体已修 note says don't re-report floatEyeAI main body. Hmm — but is this actually a diff? Vanilla AI_002 X-axis: let me verify quickly at 52775+.

Let me quickly view vanilla AI_002 main movement to be fair.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:25.578Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 52726,52905p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read AI_002_FloatingEye main movement"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:25.637Z

**📎 ToolResult**

```
		{
			if (Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
			{
				if (ai[1] > 0f && !Collision.SolidCollision(position, width, height))
				{
					ai[1] = 0f;
					ai[0] = 0f;
					netUpdate = true;
				}
			}
			else if (ai[1] == 0f)
			{
				ai[0] += 1f;
			}
			if (ai[0] >= 300f)
			{
				ai[1] = 1f;
				ai[0] = 0f;
				netUpdate = true;
			}
			if (ai[1] == 0f)
			{
				alpha = 0;
				noTileCollide = false;
			}
			else
			{
				wet = false;
				alpha = 200;
				noTileCollide = true;
			}
			rotation = velocity.Y * 0.1f * (float)direction;
			TargetClosest();
			if (direction == -1 && velocity.X > -4f && position.X > Main.player[target].position.X + (float)Main.player[target].width)
			{
				velocity.X -= 0.08f;
				if (velocity.X > 4f)
				{
					velocity.X -= 0.04f;
				}
				else if (velocity.X > 0f)
				{
					velocity.X -= 0.2f;
				}
				if (velocity.X < -4f)
				{
					velocity.X = -4f;
				}
			}
			else if (direction == 1 && velocity.X < 4f && position.X + (float)width < Main.player[target].position.X)
			{
				velocity.X += 0.08f;
				if (velocity.X < -4f)
				{
					velocity.X += 0.04f;
				}
				else if (velocity.X < 0f)
				{
					velocity.X += 0.2f;
				}
				if (velocity.X > 4f)
				{
					velocity.X = 4f;
				}
			}
			if (directionY == -1 && (double)velocity.Y > -2.5 && position.Y > Main.player[target].position.Y + (float)Main.player[target].height)
			{
				velocity.Y -= 0.1f;
				if ((double)velocity.Y > 2.5)
				{
					velocity.Y -= 0.05f;
				}
				else if (velocity.Y > 0f)
				{
					velocity.Y -= 0.15f;
				}
				if ((double)velocity.Y < -2.5)
				{
					velocity.Y = -2.5f;
				}
			}
			else if (directionY == 1 && (double)velocity.Y < 2.5 && position.Y + (float)height < Main.player[target].position.Y)
			{
				velocity.Y += 0.1f;
				if ((double)velocity.Y < -2.5)
				{
					velocity.Y += 0.05f;
				}
				else if (velocity.Y < 0f)
				{
					velocity.Y += 0.15f;
				}
				if ((double)velocity.Y > 2.5)
				{
					velocity.Y = 2.5f;
				}
			}
		}
		else if (type == 116)
		{
			TargetClosest();
			Lighting.AddLight((int)(position.X + (float)(width / 2)) / 16, (int)(position.Y + (float)(height / 2)) / 16, 0.3f, 0.2f, 0.1f);
			if (direction == -1 && velocity.X > -6f)
			{
				velocity.X -= 0.1f;
				if (velocity.X > 6f)
				{
					velocity.X -= 0.1f;
				}
				else if (velocity.X > 0f)
				{
					velocity.X -= 0.2f;
				}
				if (velocity.X < -6f)
				{
					velocity.X = -6f;
				}
			}
			else if (direction == 1 && velocity.X < 6f)
			{
				velocity.X += 0.1f;
				if (velocity.X < -6f)
				{
					velocity.X += 0.1f;
				}
				else if (velocity.X < 0f)
				{
					velocity.X += 0.2f;
				}
				if (velocity.X > 6f)
				{
					velocity.X = 6f;
				}
			}
			if (directionY == -1 && (double)velocity.Y > -2.5)
			{
				velocity.Y -= 0.04f;
				if ((double)velocity.Y > 2.5)
				{
					velocity.Y -= 0.05f;
				}
				else if (velocity.Y > 0f)
				{
					velocity.Y -= 0.15f;
				}
				if ((double)velocity.Y < -2.5)
				{
					velocity.Y = -2.5f;
				}
			}
			else if (directionY == 1 && (double)velocity.Y < 1.5)
			{
				velocity.Y += 0.04f;
				if ((double)velocity.Y < -2.5)
				{
					velocity.Y += 0.05f;
				}
				else if (velocity.Y < 0f)
				{
					velocity.Y += 0.15f;
				}
				if ((double)velocity.Y > 2.5)
				{
					velocity.Y = 2.5f;
				}
			}
			if (Main.rand.Next(40) == 0)
			{
				position += netOffset;
				int num = Dust.NewDust(new Vector2(position.X, position.Y + (float)height * 0.25f), width, (int)((float)height * 0.5f), 5, velocity.X, 2f);
				Main.dust[num].velocity.X *= 0.5f;
				Main.dust[num].velocity.Y *= 0.1f;
				position -= netOffset;
			}
		}
		else if (type == 133)
		{
			if ((double)life < (double)lifeMax * 0.5)
			{
				if (direction == -1 && velocity.X > -6f)

```


---

## 🤖 Assistant · 2026-08-19T03:19:44.480Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait — this is AI_002_FloatingEye and the first block (52673-52800) is the PIGRON branch (170/171/180 — with the pass-through-walls ai[1] mechanic: alpha 200, noTileCollide when no LOS for 300 ticks). Note the pigron block has its own movement (0.08 accel, different counters). 

Interesting: the vanilla floatEye X-axis in these blocks: `velocity.X -= 0.08f; if (velocity.X > 4f) velocity.X -= 0.04f; else if (velocity.X > 0f) velocity.X -= 0.2f;` — thresholds at 4 (cap) and 0, correction -0.04 / -0.2. Ours floatEyeAI (3639-3647): `this.vx -= 0.1; if (this.vx > 0) this.vx -= 0.1;` — missing the `> cap` second-tier (-0.04 at >4) and using -0.1 instead of -0.2 for the reverse case. BUT — 主体已修勿重报 floatEyeAI. Hmm — "已修勿重报:floatEyeAI/batAI 主体/swimAI flag22" — the parent says the main body was already fixed/audited. So someone previously audited floatEyeAI and the current state is the accepted fixed state. I shouldn't re-audit/report the main body per instructions. OK — skip floatEyeAI main-body details. Only type-specific: pigron pass-through (ai[0]>=300 no-LOS → noTileCollide+alpha 200)? Ours floatEyeAI has no pigron wall-phase mechanic! That's a pigron-exclusive branch (type-specific) — in my scope ("水母外的 aiStyle 4/14 专属分支" — well that says 4/14; floatEye is aiStyle 2, not explicitly in scope... The scope said eyes family "骷髅王手/克眼之外的眼睛族专属(若 Enemy.ts 有 eocAI/eyeAI 家族)". So eyes-family exclusive branches ARE in scope: pigron phasing is an eye-family (aiStyle 2) exclusive branch. But also "floatEyeAI 主体已修勿重报" — the phasing mechanic is arguably part of the main body. Borderline — I'll mention it briefly as a one-liner (pigron LOS-phase branch missing) flagged as possible overlap with the fixed main body.

Also the pigron grunt sound ✓ present (3596-3600). 

Wandering Eye 133 rage ✓ (rage at <0.5 life: 6 cap). The Hungry 116: light ✓ (3680); ours caps: default 4/2.5 but vanilla 116: X ±6 (0.1/0.1/0.2), Y: up cap 2.5 down 1.5 — ours uses shared 4/2.5 for 116 → diff, but again main-body-ish. One-liner.

Given the "勿重报" instructions, I'll keep floatEyeAI findings to a single short line noting the pigron phase mechanic + 116 caps, marked as possibly-known.

Now let me look at our eocAI (6886+) — quickly scan for the core phases vs vanilla 19909-20758. EoC was audited before (memory: "EoC冲刺体感差结案=canvas无DPR(非AI bug)" and "克眼专家状态机" in boss audit). So known-good. I'll spot-check dash counts/speeds only lightly... Actually the parent explicitly said "克眼之外的眼睛族专属" — i.e., eyes other than EoC. So EoC core = out. Good.

Next: skeletronHandAI (AI_012). It's in bossAI.ts. Let me read vanilla aiStyle 12 (22289-22604) and our implementation.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:45.061Z · glm-x-preview-260804

```
现在我来查看 Skeletron的手 (AI_012) —— 原版实现对比我们的 bossAI 实现。
```


---

## 🤖 Assistant · 2026-08-19T03:19:45.515Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 22289,22420p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 12 skeletron hand part 1"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:45.571Z

**📎 ToolResult**

```
		if (aiStyle == 12)
		{
			spriteDirection = -(int)this.ai[0];
			if (!Main.npc[(int)this.ai[1]].active || Main.npc[(int)this.ai[1]].aiStyle != 11)
			{
				this.ai[2] += 10f;
				if (this.ai[2] > 50f || Main.netMode != 2)
				{
					life = -1;
					HitEffect();
					active = false;
				}
			}
			else
			{
				localAI[3] = Main.npc[(int)this.ai[1]].ai[3];
			}
			bool flag21 = RedHatSkeletronAdjustmentsEnabled();
			if (flag21)
			{
				damage = (int)((float)defDamage * 1.3f);
			}
			if (this.ai[2] == 0f || this.ai[2] == 3f)
			{
				if (Main.npc[(int)this.ai[1]].ai[1] == 3f)
				{
					EncourageDespawn(10);
				}
				if (Main.npc[(int)this.ai[1]].ai[1] != 0f && !flag21)
				{
					if (position.Y > Main.npc[(int)this.ai[1]].position.Y - 100f)
					{
						if (velocity.Y > 0f)
						{
							velocity.Y *= 0.96f;
						}
						velocity.Y -= 0.07f;
						if (velocity.Y > 6f)
						{
							velocity.Y = 6f;
						}
					}
					else if (position.Y < Main.npc[(int)this.ai[1]].position.Y - 100f)
					{
						if (velocity.Y < 0f)
						{
							velocity.Y *= 0.96f;
						}
						velocity.Y += 0.07f;
						if (velocity.Y < -6f)
						{
							velocity.Y = -6f;
						}
					}
					if (position.X + (float)(width / 2) > Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 120f * this.ai[0])
					{
						if (velocity.X > 0f)
						{
							velocity.X *= 0.96f;
						}
						velocity.X -= 0.1f;
						if (velocity.X > 8f)
						{
							velocity.X = 8f;
						}
					}
					if (position.X + (float)(width / 2) < Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 120f * this.ai[0])
					{
						if (velocity.X < 0f)
						{
							velocity.X *= 0.96f;
						}
						velocity.X += 0.1f;
						if (velocity.X < -8f)
						{
							velocity.X = -8f;
						}
					}
				}
				else
				{
					this.ai[3] += 1f;
					if (flag21)
					{
						this.ai[3] += 1f;
					}
					if (Main.expertMode)
					{
						this.ai[3] += 0.5f;
					}
					if (this.ai[3] >= 300f)
					{
						this.ai[2] += 1f;
						this.ai[3] = 0f;
						netUpdate = true;
					}
					if (Main.expertMode)
					{
						if (position.Y > Main.npc[(int)this.ai[1]].position.Y + 230f)
						{
							if (velocity.Y > 0f)
							{
								velocity.Y *= 0.96f;
							}
							velocity.Y -= 0.04f;
							if (velocity.Y > 3f)
							{
								velocity.Y = 3f;
							}
						}
						else if (position.Y < Main.npc[(int)this.ai[1]].position.Y + 230f)
						{
							if (velocity.Y < 0f)
							{
								velocity.Y *= 0.96f;
							}
							velocity.Y += 0.04f;
							if (velocity.Y < -3f)
							{
								velocity.Y = -3f;
							}
						}
						if (position.X + (float)(width / 2) > Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 200f * this.ai[0])
						{
							if (velocity.X > 0f)
							{
								velocity.X *= 0.96f;
							}
							velocity.X -= 0.07f;
							if (velocity.X > 8f)
							{
								velocity.X = 8f;

```


---

## 🤖 Assistant · 2026-08-19T03:19:46.093Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"export function skeletronHandAI\" ~/Project/GLM/SandboxWorld/game/src/ | head -2",
 "description": "Locate skeletronHandAI implementation"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:46.157Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts:177:export function skeletronHandAI(e: Enemy, game: GameHooks, player: Player | null) {

```


---

## 🤖 Assistant · 2026-08-19T03:19:49.176Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 22420,22604p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 12 skeletron hand part 2"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:49.231Z

**📎 ToolResult**

```
								velocity.X = 8f;
							}
						}
						if (position.X + (float)(width / 2) < Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 200f * this.ai[0])
						{
							if (velocity.X < 0f)
							{
								velocity.X *= 0.96f;
							}
							velocity.X += 0.07f;
							if (velocity.X < -8f)
							{
								velocity.X = -8f;
							}
						}
					}
					if (position.Y > Main.npc[(int)this.ai[1]].position.Y + 230f)
					{
						if (velocity.Y > 0f)
						{
							velocity.Y *= 0.96f;
						}
						velocity.Y -= 0.04f;
						if (velocity.Y > 3f)
						{
							velocity.Y = 3f;
						}
					}
					else if (position.Y < Main.npc[(int)this.ai[1]].position.Y + 230f)
					{
						if (velocity.Y < 0f)
						{
							velocity.Y *= 0.96f;
						}
						velocity.Y += 0.04f;
						if (velocity.Y < -3f)
						{
							velocity.Y = -3f;
						}
					}
					if (position.X + (float)(width / 2) > Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 200f * this.ai[0])
					{
						if (velocity.X > 0f)
						{
							velocity.X *= 0.96f;
						}
						velocity.X -= 0.07f;
						if (velocity.X > 8f)
						{
							velocity.X = 8f;
						}
					}
					if (position.X + (float)(width / 2) < Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 200f * this.ai[0])
					{
						if (velocity.X < 0f)
						{
							velocity.X *= 0.96f;
						}
						velocity.X += 0.07f;
						if (velocity.X < -8f)
						{
							velocity.X = -8f;
						}
					}
				}
				Vector2 vector18 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
				float num206 = Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 200f * this.ai[0] - vector18.X;
				float num207 = Main.npc[(int)this.ai[1]].position.Y + 230f - vector18.Y;
				float num208 = Math.Max(0.01f, (float)Math.Sqrt(num206 * num206 + num207 * num207));
				rotation = (float)Math.Atan2(num207, num206) + 1.57f;
			}
			else if (this.ai[2] == 1f)
			{
				Vector2 vector19 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
				float num209 = Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 200f * this.ai[0] - vector19.X;
				float num210 = Main.npc[(int)this.ai[1]].position.Y + 230f - vector19.Y;
				float num211 = Math.Max(0.01f, (float)Math.Sqrt(num209 * num209 + num210 * num210));
				rotation = (float)Math.Atan2(num210, num209) + 1.57f;
				velocity.X *= 0.95f;
				velocity.Y -= 0.1f;
				if (flag21)
				{
					float num212 = 15f;
					velocity.Y -= 0.09f;
					if (velocity.Y < 0f - num212)
					{
						velocity.Y = 0f - num212;
					}
				}
				else if (Main.expertMode)
				{
					velocity.Y -= 0.06f;
					if (velocity.Y < -13f)
					{
						velocity.Y = -13f;
					}
				}
				else if (velocity.Y < -8f)
				{
					velocity.Y = -8f;
				}
				if (position.Y < Main.npc[(int)this.ai[1]].position.Y - 200f)
				{
					TargetClosest();
					this.ai[2] = 2f;
					vector19 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
					num209 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector19.X;
					num210 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - vector19.Y;
					num211 = Math.Max(0.01f, (float)Math.Sqrt(num209 * num209 + num210 * num210));
					num211 = (flag21 ? (24f / num211) : ((!Main.expertMode) ? (18f / num211) : (21f / num211)));
					velocity.X = num209 * num211;
					velocity.Y = num210 * num211;
					netUpdate = true;
				}
			}
			else if (this.ai[2] == 2f)
			{
				if (position.Y > Main.player[target].position.Y || Vector2.Dot(velocity, Main.player[target].Center - base.Center) <= 0f || Distance(Main.player[target].position) > 2000f || velocity.Y < 0f)
				{
					this.ai[2] = 3f;
				}
			}
			else if (this.ai[2] == 4f)
			{
				Vector2 vector20 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
				float num213 = Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 200f * this.ai[0] - vector20.X;
				float num214 = Main.npc[(int)this.ai[1]].position.Y + 230f - vector20.Y;
				float num215 = Math.Max(0.01f, (float)Math.Sqrt(num213 * num213 + num214 * num214));
				rotation = (float)Math.Atan2(num214, num213) + 1.57f;
				velocity.Y *= 0.95f;
				velocity.X += 0.1f * (0f - this.ai[0]);
				if (flag21)
				{
					float num216 = 15f;
					velocity.X += 0.1f * (0f - this.ai[0]);
					if (velocity.X < 0f - num216)
					{
						velocity.X = 0f - num216;
					}
					else if (velocity.X > num216)
					{
						velocity.X = num216;
					}
				}
				else if (Main.expertMode)
				{
					velocity.X += 0.07f * (0f - this.ai[0]);
					if (velocity.X < -12f)
					{
						velocity.X = -12f;
					}
					else if (velocity.X > 12f)
					{
						velocity.X = 12f;
					}
				}
				else if (velocity.X < -8f)
				{
					velocity.X = -8f;
				}
				else if (velocity.X > 8f)
				{
					velocity.X = 8f;
				}
				if (position.X + (float)(width / 2) < Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) - 500f || position.X + (float)(width / 2) > Main.npc[(int)this.ai[1]].position.X + (float)(Main.npc[(int)this.ai[1]].width / 2) + 500f)
				{
					TargetClosest();
					this.ai[2] = 5f;
					vector20 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
					num213 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector20.X;
					num214 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - vector20.Y;
					num215 = Math.Max(0.01f, (float)Math.Sqrt(num213 * num213 + num214 * num214));
					num215 = (flag21 ? (25f / num215) : ((!Main.expertMode) ? (17f / num215) : (22f / num215)));
					velocity.X = num213 * num215;
					velocity.Y = num214 * num215;
					netUpdate = true;
				}
			}
			else if (this.ai[2] == 5f && ((velocity.X > 0f && position.X + (float)(width / 2) > Main.player[target].position.X + (float)(Main.player[target].width / 2)) || (velocity.X < 0f && position.X + (float)(width / 2) < Main.player[target].position.X + (float)(Main.player[target].width / 2)) || Vector2.Dot(velocity, Main.player[target].Center - base.Center) <= 0f || Distance(Main.player[target].position) > 2000f))
			{
				this.ai[2] = 0f;
			}
			return;
		}
		if (aiStyle == 13)

```


---

## 🤖 Assistant · 2026-08-19T03:19:49.528Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI.ts",
 "limit": 120,
 "offset": 177
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:49.548Z

**📎 ToolResult**

```
177	export function skeletronHandAI(e: Enemy, game: GameHooks, player: Player | null) {
178	  const headId = e.ai1;
179	  const enemies = game.enemies() as unknown[];
180	  const head = enemies.find((n) => (n as Enemy).id === headId) as Enemy | undefined;
181	  if (!head || head.vanilla?.aiStyle !== 11 || head.dead) { e.dead = true; return; }
182	  e.master = head; // 臂骨 IK 渲染用（Renderer.drawSkeletronArm）
183	  if (head.ai1 === 3) { e.dead = true; return; }
184	  e.facing = -(e.ai0 || 1);
185	  if (!player) { e.x += e.vx; e.y += e.vy; return; }
186	  // 缓慢环绕(头悬浮态);头冲撞态则回到侧位
187	  const ty = head.y - 100;
188	  const tx = head.x + head.w / 2 - e.w / 2 - 120 * (e.ai0 || 1);
189	  if (head.ai1 === 0) {
190	    e.ai3 += 1;
191	    if (e.ai3 >= 300) { e.ai3 = -120; } // 负值=挥击中
192	    if (e.ai3 < 0) {
193	      // 挥击:朝玩家冲刺 8 速
194	      const dx = player.cx - e.cx, dy = player.cy - e.cy;
195	      const d = Math.hypot(dx, dy) || 1;
196	      e.vx += ((dx / d) * 8 - e.vx) * 0.15;
197	      e.vy += ((dy / d) * 8 - e.vy) * 0.15;
198	    } else {
199	      // 环绕位:头右/左 200px、下方 230(原版 num200 系)
200	      const ox = head.x + head.w / 2 - e.w / 2 - 200 * (e.ai0 || 1);
201	      const oy = head.y + 230;
202	      e.vx += ((ox - e.x) * 0.02 - e.vx) * 0.1;
203	      e.vy += ((oy - e.y) * 0.02 - e.vy) * 0.1;
204	    }
205	  } else {
206	    // 头冲撞中:快速回侧位
207	    e.vx += ((tx - e.x) * 0.05 - e.vx) * 0.2;
208	    e.vy += ((ty - e.y) * 0.05 - e.vy) * 0.2;
209	  }
210	  e.x += e.vx; e.y += e.vy;
211	}
212	
213	/** AI_015 史莱姆王(NPC.cs SetDefaults case 50 / AI_015):大跳朝玩家 + 受击攒怒 +
214	 *  落地砸出小史莱姆(30% 概率)。经典模式无传送(专家专属),暂不移植传送。 */
215	/** 史莱姆王传送目的地（Bottom 锚像素，= vanilla localAI[1]/[2]；despawn 支=世界角 :43485） */
216	const kingTpDest = new WeakMap<Enemy, { x: number; y: number }>();
217	/** localAI[0] anti-cheese 计数（:43504-43510 ≥360 或距玩家 >2000px → 落玩家脚底） */
218	const kingAntiCheese = new WeakMap<Enemy, number>();
219	
220	/** AI_015_KingSlime_FindTeleportSpot（:43402-43434 收敛）：外环 ±10/内环 ±7 收
221	 *  "上格净空的实心格、非岩浆、对玩家有视线"的落点随机取一；失败退 (±6,±2)；
222	 *  再失败落玩家脚底。返回 Bottom 锚像素。 */
223	function kingFindTeleportSpot(e: Enemy, game: GameHooks, player: Player): { x: number; y: number } {
224	  const st = game.world.store;
225	  const px = Math.floor(player.cx / TILE), py = Math.floor((player.y + player.h) / TILE);
226	  const cand: Array<{ x: number; y: number }> = [];
227	  for (const [rx, ry] of [[10, 10], [6, 2]] as const) {
228	    cand.length = 0;
229	    for (let x = px - rx; x <= px + rx; x++) {
230	      for (let y = py - ry; y <= py + ry; y++) {
231	        if (!st.inBounds(x, y) || !st.isSolid(x, y)) continue;
232	        if (st.isSolid(x, y - 1)) continue;                       // 顶上净空
233	        if (st.liquid[st.idx(x, y - 1)] > 0 && st.liquidType[st.idx(x, y - 1)] === 2) continue; // 岩浆
234	        if (!canHit(st, x * TILE + 8, (y - 1) * TILE + 8, 1, 1, player.x, player.y, player.w, player.h)) continue;
235	        // 外环 ±10/内环 ±7：|dx|>7 || |dy|>7 的环带才收（内 7×7 排除近身）
236	        if (rx === 10 && Math.abs(x - px) <= 7 && Math.abs(y - py) <= 7) continue;
237	        cand.push({ x, y });
238	      }
239	    }
240	    if (cand.length) break;
241	  }
242	  const pick = cand.length ? cand[Math.floor(Math.random() * cand.length)] : { x: px, y: py };
243	  return { x: pick.x * TILE + TILE / 2, y: (pick.y + 1) * TILE };   // Bottom 锚
244	}
245	
246	export function kingSlimeAI(e: Enemy, game: GameHooks, player: Player | null) {
247	  // Enemy.ai0 默认 -1120(史莱姆族约定);原版 AI_015 的 ai[0] 从 0 起步 → 首帧复位
248	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }
249	  // 玩家死/远距 3000px(:43466-43485)：TargetClosest 二次判定后仍失败 →
250	  // EncourageDespawn(10) + 背对 + ai[1]=5 缩身离场（anti-cheese 传送回归）
251	  const ksd = player ? Math.hypot(player.cx - e.cx, player.cy - e.cy) : Infinity;
252	  if (!player || ksd > 3000) {
253	    e.encourageDespawn(10);
254	    if (player) e.facing = player.cx < e.cx ? 1 : -1; // 转身背对(:43479-43485)
255	    if (e.ai1 !== 5 && e.ai1 !== 6) {
256	      e.ai1 = 5; e.ai3 = 0;
257	      kingTpDest.set(e, { x: game.world.w * TILE, y: game.world.h * TILE }); // :43485-43488 世界角
258	    }
259	  }
260	  if (e.ai1 === 5) {
261	    // 离场/传送缩身态（:43537-43575）：60 tick 缩身 → Gore734 → Bottom 锚落位 → 6 号淡入
262	    e.ai3++;
263	    e.squash = Math.max(0, 1 - e.ai3 / 60) * 0.6; // 缩身近似（scale 收缩）
264	    game.spawnParticles(e.cx, e.cy, '#4E88FF', 10, 1.2, { life: 30 }); // 每帧 10 尘 4 蓝 ×0.5（:43564-43570）
265	    e.vy += 0.3;
266	    e.x += e.vx; e.y += e.vy;
267	    if (e.ai3 === 60) {
268	      game.spawnParticles(e.cx, e.cy - e.h / 2, '#FFD060', 6, 2, { life: 40 }); // Gore 734 王冠（:43552）
269	    }
270	    if (e.ai3 >= 60) {
271	      const dest = kingTpDest.get(e) ?? { x: game.world.w * TILE, y: game.world.h * TILE };
272	      e.x = dest.x - e.w / 2;
273	      e.y = dest.y - e.h;                          // base.Bottom = (localAI[1], localAI[2])（:43554）
274	      e.ai1 = 6; e.ai3 = 0;
275	      e.squash = 0;
276	      e.spawnAlpha = 255; e.alphaFade = true; // 淡入（6 号态）
277	    }
278	    return;
279	  }
280	  if (e.ai1 === 6) {
281	    // 淡入回归（约 30 tick spawnAlpha 归零后回战斗）
282	    e.ai3++;
283	    game.spawnParticles(e.cx, e.cy, '#4E88FF', 10, 2.4, { life: 30 }); // 到达尘 ×2（:43584-43590）
284	    e.ai0 = 0;
285	    if (e.ai3 >= 30) { e.ai1 = 0; e.ai3 = 0; }
286	    return;
287	  }
288	  if (!player) return;
289	  // ---- 常规周期传送（:43507-43530）：ai2 在 无视线||高差>160 时累计，≥300 且落地 →
290	  //  传送循环；antiCheese（localAI[0]≥360 或距玩家>2000px）直接落玩家脚底（:43504-43510）----
291	  if (e.ai1 < 5 && e.onGround) {
292	    const los = canHit(game.world.store, e.x, e.y, e.w, e.h, player.x, player.y, player.w, player.h);
293	    const heightGap = Math.abs(e.y - (player.y + player.h));
294	    if (!los || heightGap > 160) e.ai2 += 1;
295	    else if (e.ai2 > 0) e.ai2 -= 1;
296	    const ac = (kingAntiCheese.get(e) ?? 0) + 1;

```


---

## 🤖 Assistant · 2026-08-19T03:20:17.921Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
skeletronHandAI in bossAI.ts (177-211) vs vanilla AI_012 (22289-22604). This is a coarse approximation:

Vanilla hand state machine (ai[2] states 0/3 hover-orbit, 1 spin-up, 2 dash, 4 side-float, 5 dash-return):
- ai[2]==0||3 (orbit/hover): if head ai[1]!=0 (head spinning) → hand follows at (±120, -100) with damp 0.96/accel 0.07-0.1 caps ±6/±8; ELSE hover at (±200, +230): ai[3] counts (1/t, +0.5 expert, +1 getGood) — at 300 → ai[2]++ (0→1, 3→4). Hover: damp 0.96, accel 0.04 Y-cap 3, X accel 0.07 cap 8 toward (±200, +230). Expert has a DUPLICATE hover block (identical) — net double accel in expert. rotation = atan2 to anchor + 1.57.
- ai[2]==1 (spin-up): vx *= 0.95, vy -= 0.1 (expert: -0.06 extra cap -13; normal cap -8; getGood -0.09 cap -15); rotation tracks anchor; when position.Y < head.y - 200 → TargetClosest, ai[2]=2, velocity = dir * 18 (expert 21, getGood 24).
- ai[2]==2 (dash): exit when position.Y > player.Y || dot(velocity, toPlayer) <= 0 || dist > 2000 || velocity.Y < 0 → ai[2]=3.
- ai[2]==4: side float: vy *= 0.95, vx += 0.1*-ai[0] (expert extra 0.07, cap ±12; normal ±8; getGood ±15); when |x - headX| > 500 → TargetClosest, ai[2]=5, velocity = dir*17 (expert 22, getGood 25).
- ai[2]==5: exit when passing player X or dot <= 0 or dist > 2000 → ai[2]=0.
- Head dead (ai[1] invalid aiStyle) → ai[2] += 10 → die.
- Head ai[1]==3 (despawn) → EncourageDespawn.

Ours (bossAI.ts:177-211): completely different simplified model:
- head.ai1===3 → dead (vanilla: EncourageDespawn then die — fine).
- head.ai1===0 (hover): ai3 += 1; at 300 → ai3 = -120 "挥击中"; swing = lerp toward player at speed 8 (0.15 lerp) — NOT the vanilla spin-up (vy -= 0.1 rise to head-200 then 18-speed dash at player).
- orbit: lerp to (±200, +230) with (ox-x)*0.02 spring and 0.1 lerp — vanilla: piecewise damp/accel 0.04/0.07 caps 3/8.
- head.ai1!==0 (head spin): ours returns to (±120, -100) via spring 0.05/0.2 lerp — vanilla: damp 0.96 + accel 0.1/0.07 with caps (±8 X, ±6 Y). 
- No ai[2] state machine at all (no 1/2/4/5 dash phases with 18/21 speed dash and dot-product exit), no expert speed-ups, no rotation tracking, no despawn when head dead→ ai[2]+=10 (ours: e.dead immediately — vanilla waits ai[2]>50... minor).

So the hand AI is a spring-lerp approximation, not 1:1. Diffs:
1. Missing spin-up (ai2==1) + dash (ai2==2): hand never does the vertical rise + 18/21-speed lunge. Ours: 8-speed homing lerp "swing" for 120t. Severity 严重 for boss feel? It's Skeletron's primary hand attack. The head spin phase: vanilla hands follow at ±120/-100 then dash at player from side (4→5 at 17/22). Ours: neither. I'd grade 严重 (combat behavior substantially different).
2. Orbit params: spring vs damp/accel — medium.
3. No expert adjustments — medium.
4. rotation not maintained (vanilla atan2 to anchor +1.57) — our Renderer presumably rotates via visAngle? Ours doesn't set visAngle at all. Visual — medium-low.

Hmm wait — is skeletronHandAI in my scope? "骷髅王手/克眼之外的眼睛族专属(若 Enemy.ts 有 eocAI/eyeAI 家族)". I read this as: skeleton-king hand AND eyes-other-than-EoC family specifics. So yes, skeletron hand IS in scope. OK.

But wait — the memory notes say "boss-audit-prehardmode-2026-08-13 — 肉前三王+肉山1:1审计" — maybe the hand was audited then and this approximation was accepted? The memory summary says "GERunner转化链/世噬分体重构/克眼专家状态机;EoC冲刺体感差结案" — doesn't mention the hand specifically. I'll report it with a note.

Now — the parent said the parent said "已知正确带行号的大块一句话带过" — for pieces that are known-correct with line numbers, one sentence. And "已修勿重报:floatEyeAI/batAI 主体/swimAI flag22".

Next: eocAI — out of scope (克眼 excluded). Let me now do a quick check of the remaining "flying/aquatic" cases not in my families, per the enumeration duty: case 17 vultureAI (memory: fixed), case 44 flyingSwarmerAI (AI_044), case 56 dungeonSpiritAI, case 9 bouncingBallAI, case 22 ghostAI (read partially above), case 49 angryNimbusAI, case 2 floatEyeAI (main fixed). To control density, I'll spot-check ghostAI numbers vs vanilla aiStyle 22 (24726-25316) since I already have ours, and dungeonSpiritAI (32915) + flyingSwarmerAI (30999) quickly. Actually — these were covered in previous audit batches per memory ("近似清零" A批 AI_003移动族+混沌传送; "AI家族100%"). The task says "自己 grep case 枚举补全,归你管的报出来" — i.e., enumerate the flying/aquatic cases not explicitly assigned and report which ones fall to me. I'll list them and do a light parameter check on ghostAI only (since I already have the code in view), and note the others as covered by prior batches (memory).

Let me verify ghostAI numbers vs vanilla 24726-25316.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:18.557Z · glm-x-preview-260804

```
我先对比 `ghostAI` 和原版 `aiStyle 22`，并检查我们的 `eocAI` 入口是否存在像素级问题。
```


---

## 🤖 Assistant · 2026-08-19T03:20:19.564Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 24726,24760p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo '...'; sed -n 25048,25130p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 22 ghost core"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:19.643Z

**📎 ToolResult**

```
		else if (aiStyle == 22)
		{
			bool flag27 = false;
			bool flag28 = false;
			if (type == 330 && !Main.pumpkinMoon)
			{
				flag28 = true;
			}
			if (type == 253 && !Main.eclipse)
			{
				flag28 = true;
			}
			if (type == 490 && Main.dayTime)
			{
				flag28 = true;
			}
			if (justHit)
			{
				this.ai[2] = 0f;
			}
			if (type == 316 && (Main.player[target].dead || Vector2.Distance(base.Center, Main.player[target].Center) > 3000f))
			{
				if (this.ai[3] == 1f)
				{
					if (localAI[3] == 0f)
					{
						localAI[3] = 1f;
						SoundEngine.PlaySound(SoundID.NPCDeath55, (int)base.Center.X, (int)base.Center.Y);
					}
					flag28 = true;
					Opacity -= 0.025f;
					if (Opacity <= 0f)
					{
						active = false;
						netUpdate = true;
...
					}
					num310 += (int)num341;
				}
			}
			if (base.Bottom.Y > Main.player[target].Top.Y)
			{
				if (type == 330)
				{
					flag31 = false;
				}
				else
				{
					for (int num342 = num309; num342 < num309 + num310; num342++)
					{
						if (Main.tile[num308, num342] == null)
						{
							Main.tile[num308, num342] = new Tile();
						}
						if ((Main.tile[num308, num342].nactive() && Main.tileSolid[Main.tile[num308, num342].type]) || Main.tile[num308, num342].liquid > 0)
						{
							if (num342 <= num309 + 1)
							{
								flag32 = true;
							}
							flag31 = false;
							break;
						}
					}
				}
			}
			if (Main.player[target].npcTypeNoAggro[type])
			{
				bool flag33 = false;
				for (int num343 = num309; num343 < num309 + num310 - 2; num343++)
				{
					if (Main.tile[num308, num343] == null)
					{
						Main.tile[num308, num343] = new Tile();
					}
					if ((Main.tile[num308, num343].nactive() && Main.tileSolid[Main.tile[num308, num343].type]) || Main.tile[num308, num343].liquid > 0)
					{
						flag33 = true;
						break;
					}
				}
				directionY = (!flag33).ToDirectionInt();
			}
			if (type == 169 || type == 268)
			{
				for (int num344 = num309 - 3; num344 < num309; num344++)
				{
					if (Main.tile[num308, num344] == null)
					{
						Main.tile[num308, num344] = new Tile();
					}
					if ((Main.tile[num308, num344].nactive() && Main.tileSolid[Main.tile[num308, num344].type] && !TileID.Sets.Platforms[Main.tile[num308, num344].type]) || Main.tile[num308, num344].liquid > 0)
					{
						flag32 = false;
						flag27 = true;
						break;
					}
				}
			}
			if (flag27)
			{
				flag32 = false;
				flag31 = true;
				if (type == 268)
				{
					velocity.Y += 2f;
				}
			}
			if (flag31)
			{
				if (type == 75 || type == 169)
				{
					velocity.Y += 0.2f;
					if (velocity.Y > 2f)
					{
						velocity.Y = 2f;
					}
				}
				else if (type == 490)

```


---

## 🤖 Assistant · 2026-08-19T03:20:32.739Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The aiStyle 22 block is complex (line-of-sight following with flag31/flag32 — pass-through behavior: ghosts only chase when player in sight else float). Let me see the chase core numbers — grep for the Lerp in aiStyle 22.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:33.178Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 25130,25316p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 22 chase core"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:33.232Z

**📎 ToolResult**

```
				else if (type == 490)
				{
					velocity.Y += 0.03f;
					if (velocity.Y > 0.75f)
					{
						velocity.Y = 0.75f;
					}
				}
				else
				{
					velocity.Y += 0.1f;
					if (type == 316 && flag28)
					{
						velocity.Y -= 0.05f;
						if (velocity.Y > 6f)
						{
							velocity.Y = 6f;
						}
					}
					else if (velocity.Y > 3f)
					{
						velocity.Y = 3f;
					}
				}
			}
			else
			{
				if (type == 75 || type == 169)
				{
					if ((directionY < 0 && velocity.Y > 0f) || flag32)
					{
						velocity.Y -= 0.2f;
					}
				}
				else if (type == 490)
				{
					if ((directionY < 0 && velocity.Y > 0f) || flag32)
					{
						velocity.Y -= 0.075f;
					}
					if (velocity.Y < -0.75f)
					{
						velocity.Y = -0.75f;
					}
				}
				else if (directionY < 0 && velocity.Y > 0f)
				{
					velocity.Y -= 0.1f;
				}
				if (velocity.Y < -4f)
				{
					velocity.Y = -4f;
				}
			}
			if (type == 75 && wet)
			{
				velocity.Y -= 0.2f;
				if (velocity.Y < -2f)
				{
					velocity.Y = -2f;
				}
			}
			if (collideX)
			{
				velocity.X = oldVelocity.X * -0.4f;
				if (direction == -1 && velocity.X > 0f && velocity.X < 1f)
				{
					velocity.X = 1f;
				}
				if (direction == 1 && velocity.X < 0f && velocity.X > -1f)
				{
					velocity.X = -1f;
				}
			}
			if (collideY)
			{
				velocity.Y = oldVelocity.Y * -0.25f;
				if (velocity.Y > 0f && velocity.Y < 1f)
				{
					velocity.Y = 1f;
				}
				if (velocity.Y < 0f && velocity.Y > -1f)
				{
					velocity.Y = -1f;
				}
			}
			float num345 = 2f;
			if (type == 75)
			{
				num345 = 3f;
			}
			if (type == 253)
			{
				num345 = 4f;
			}
			if (type == 490)
			{
				num345 = 1.5f;
			}
			if (type == 330)
			{
				alpha = 0;
				num345 = 4f;
				if (!flag28)
				{
					TargetClosest();
				}
				else
				{
					EncourageDespawn(10);
				}
				if (direction < 0 && velocity.X > 0f)
				{
					velocity.X *= 0.9f;
				}
				if (direction > 0 && velocity.X < 0f)
				{
					velocity.X *= 0.9f;
				}
			}
			if (direction == -1 && velocity.X > 0f - num345)
			{
				velocity.X -= 0.1f;
				if (velocity.X > num345)
				{
					velocity.X -= 0.1f;
				}
				else if (velocity.X > 0f)
				{
					velocity.X += 0.05f;
				}
				if (velocity.X < 0f - num345)
				{
					velocity.X = 0f - num345;
				}
			}
			else if (direction == 1 && velocity.X < num345)
			{
				velocity.X += 0.1f;
				if (velocity.X < 0f - num345)
				{
					velocity.X += 0.1f;
				}
				else if (velocity.X < 0f)
				{
					velocity.X -= 0.05f;
				}
				if (velocity.X > num345)
				{
					velocity.X = num345;
				}
			}
			num345 = ((type != 490) ? 1.5f : 1f);
			if (directionY == -1 && velocity.Y > 0f - num345)
			{
				velocity.Y -= 0.04f;
				if (velocity.Y > num345)
				{
					velocity.Y -= 0.05f;
				}
				else if (velocity.Y > 0f)
				{
					velocity.Y += 0.03f;
				}
				if (velocity.Y < 0f - num345)
				{
					velocity.Y = 0f - num345;
				}
			}
			else if (directionY == 1 && velocity.Y < num345)
			{
				velocity.Y += 0.04f;
				if (velocity.Y < 0f - num345)
				{
					velocity.Y += 0.05f;
				}
				else if (velocity.Y < 0f)
				{
					velocity.Y -= 0.03f;
				}
				if (velocity.Y > num345)
				{
					velocity.Y = num345;
				}
			}
		}
		else if (aiStyle == 23)

```


---

## 🤖 Assistant · 2026-08-19T03:20:41.568Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Hmm — this is NOT the simple ghost lerp. Wait — aiStyle 22's X/Y movement here is the standard direction-based 0.1/±2 (with type overrides 75→3, 253→4, 490→1.5, 330→4). The our-ghostAI claims "Lerp 0.0125 toward normalized dir ×7" — that does NOT match aiStyle 22 at all! Which aiStyle is the "ghost" (Wraith 81? no — Wraith is... hmm). Let me check: Ghost NPC = 316 (Poltergeist? no — 316 = "Dungeon Spirit"? no, Dungeon Spirit is 484?). Which NPCs have aiStyle 22? Let me query our data. Our ghostAI handles aiStyle 22. Vanilla aiStyle 22 = "Wraith/Ghost family": Wraith (81?), Poltergeist (330?)... The comment in our code says "AI_022 幽灵族（NPC.145.cs:24726+）：穿墙缓速追击 目标速度 = 归一化方向×7（num312），Lerp 系数 0.0125（num317）". num312/num317 — those weren't in the section I read (24726-25316)... wait they must be between 24760-25048 (the middle chunk I skipped). Let me read that chunk — the lerp chase is probably the flag31/flag32 "pass-through" segment.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:42.193Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 24840,25048p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla aiStyle 22 middle (lerp chase)"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:42.247Z

**📎 ToolResult**

```
				if (Main.player[target].Center.X > base.Center.X)
				{
					direction = -1;
				}
				else
				{
					direction = 1;
				}
			}
			int num308 = (int)(base.Center.X / 16f) + direction * 2;
			int num309 = (int)(base.Bottom.Y / 16f);
			bool flag31 = true;
			bool flag32 = false;
			int num310 = 3;
			if (type == 122)
			{
				position += netOffset;
				if (type == 122)
				{
					Lighting.AddLight((int)base.Center.X / 16, (int)base.Center.Y / 16, 0.4f, 0f, 0.25f);
				}
				position -= netOffset;
				if (justHit)
				{
					this.ai[3] = 0f;
					localAI[1] = 0f;
				}
				int num311 = 700;
				if (Main.netMode != 1 && this.ai[3] == 32f && !Main.player[target].npcTypeNoAggro[type])
				{
					float num312 = 7f;
					Vector2 vector29 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
					float num313 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector29.X;
					float num314 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - vector29.Y;
					float num315 = (float)Math.Sqrt(num313 * num313 + num314 * num314);
					if (num315 < (float)num311)
					{
						float num316 = num315;
						num315 = num312 / num315;
						num313 *= num315;
						num314 *= num315;
						float num317 = 0.0125f;
						Vector2 vector30 = new Vector2(num313, num314).RotatedByRandom(num317 * (MathF.PI * 2f));
						num313 = vector30.X;
						num314 = vector30.Y;
						int num318 = 25;
						int num319 = 84;
						int num320 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector29.X, vector29.Y, num313, num314, num319, num318, 0f, Main.myPlayer);
					}
				}
				num310 = 8;
				if (this.ai[3] > 0f)
				{
					this.ai[3]++;
					Player player3 = Main.player[target];
					float num321 = player3.Center.Distance(base.Center);
					if (player3 != null && player3.active && num321 >= (float)num311)
					{
						this.ai[3] = 0f;
					}
					if (this.ai[3] >= 64f)
					{
						this.ai[3] = 0f;
					}
				}
				if (Main.netMode != 1 && this.ai[3] == 0f)
				{
					localAI[1]++;
					if (localAI[1] > 120f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && !Main.player[target].npcTypeNoAggro[type])
					{
						localAI[1] = 0f;
						this.ai[3] = 1f;
						netUpdate = true;
					}
				}
			}
			else if (type == 75)
			{
				num310 = 4;
				position += netOffset;
				if (Main.rand.Next(6) == 0)
				{
					int num322 = Dust.NewDust(position, width, height, 55, 0f, 0f, 200, this.color);
					Dust dust = Main.dust[num322];
					dust.velocity *= 0.3f;
				}
				if (Main.rand.Next(40) == 0)
				{
					SoundEngine.PlaySound(27, (int)position.X, (int)position.Y);
				}
				position -= netOffset;
			}
			else if (type == 169)
			{
				position += netOffset;
				Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), 0f, 0.6f, 0.75f);
				alpha = 30;
				if (Main.rand.Next(3) == 0)
				{
					int num323 = Dust.NewDust(position, width, height, 92, 0f, 0f, 200);
					Dust dust = Main.dust[num323];
					dust.velocity *= 0.3f;
					Main.dust[num323].noGravity = true;
				}
				position -= netOffset;
				if (justHit)
				{
					this.ai[3] = 0f;
					localAI[1] = 0f;
				}
				float num324 = 5f;
				Vector2 vector31 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
				float num325 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector31.X;
				float num326 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - vector31.Y;
				float num327 = (float)Math.Sqrt(num325 * num325 + num326 * num326);
				float num328 = num327;
				num327 = num324 / num327;
				num325 *= num327;
				num326 *= num327;
				if (num325 > 0f)
				{
					direction = 1;
				}
				else
				{
					direction = -1;
				}
				spriteDirection = direction;
				if (direction < 0)
				{
					rotation = (float)Math.Atan2(0f - num326, 0f - num325);
				}
				else
				{
					rotation = (float)Math.Atan2(num326, num325);
				}
				if (Main.netMode != 1 && this.ai[3] == 16f)
				{
					int num329 = 45;
					int num330 = 128;
					int num331 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector31.X, vector31.Y, num325, num326, num330, num329, 0f, Main.myPlayer);
				}
				num310 = 10;
				if (this.ai[3] > 0f)
				{
					this.ai[3]++;
					if (this.ai[3] >= 64f)
					{
						this.ai[3] = 0f;
					}
				}
				if (Main.netMode != 1 && this.ai[3] == 0f)
				{
					localAI[1] += 1f;
					if (localAI[1] > 120f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
					{
						localAI[1] = 0f;
						this.ai[3] = 1f;
						netUpdate = true;
					}
				}
			}
			else if (type == 268)
			{
				rotation = velocity.X * 0.1f;
				num310 = ((!(Main.player[target].Center.Y < base.Center.Y)) ? 6 : 12);
				if (Main.netMode != 1 && !confused)
				{
					this.ai[3]++;
					if (justHit)
					{
						this.ai[3] = -45f;
						localAI[1] = 0f;
					}
					if (Main.netMode != 1 && this.ai[3] >= (float)(60 + Main.rand.Next(60)))
					{
						this.ai[3] = 0f;
						if (Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
						{
							float num332 = 10f;
							Vector2 vector32 = new Vector2(position.X + (float)width * 0.5f - 4f, position.Y + (float)height * 0.7f);
							float num333 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - vector32.X;
							float num334 = Math.Abs(num333) * 0.1f;
							float num335 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - vector32.Y - num334;
							num333 += (float)Main.rand.Next(-10, 11);
							num335 += (float)Main.rand.Next(-30, 21);
							float num336 = (float)Math.Sqrt(num333 * num333 + num335 * num335);
							float num337 = num336;
							num336 = num332 / num336;
							num333 *= num336;
							num335 *= num336;
							int num338 = 40;
							int num339 = 288;
							int num340 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector32.X, vector32.Y, num333, num335, num339, num338, 0f, Main.myPlayer);
						}
					}
				}
			}
			if (type == 490)
			{
				num310 = 4;
				if (target >= 0)
				{
					float num341 = (Main.player[target].Center - base.Center).Length();
					num341 /= 70f;
					if (num341 > 8f)
					{
						num341 = 8f;
					}

```


---

## 🤖 Assistant · 2026-08-19T03:20:53.437Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Wait — I need to find where the ghost's actual "float toward player" movement is. The lerp 0.0125/×7 in our ghostAI comment refers to... hmm, num312 = 7f / num317 = 0.0125 are in the type==122 shoot branch (RotatedByRandom(0.0125*2π) — tiny spread for the laser!), NOT movement! So our ghostAI's "target velocity = dir×7, lerp 0.0125" model appears to be misread from the 122 laser parameters!

Hold on. Let me look at what the ACTUAL ghost (type 316? or which) movement is in aiStyle 22. The core movement in aiStyle 22 (from the tail I read at 25130-25316): standard direction-based X (0.1, ±2; 75→3, 253→4, 490→1.5, 330→4) and Y (0.04, ±1.5) plus the flag31/flag32 ceiling/floor logic (the "pass-through only when clear" hovering). No lerp.

Which types are aiStyle 22 in our data? Let me check. Also which type is "Ghost"? Ghost = NPC 316? Hmm — actually I recall Ghost (Wraith-like dungeon ghost) is NPC 316? No wait — 316 is... let me check our data names for aiStyle 22.

Hmm wait — hold on. Maybe our ghostAI's numbers come from a different part. Our comment: "目标速度 = 归一化方向×7（num312），Lerp 系数 0.0125（num317）——飘忽逼近的手感". In vanilla type==122 branch: num312 = 7f (laser speed), num317 = 0.0125 (laser spread). So indeed our ghost movement core (vx += (dir*7 - vx)*0.0125) is built from laser parameters — the movement model itself is fabricated relative to aiStyle 22! The real aiStyle 22 movement: direction-based 0.1/±2 X + 0.04/±1.5 Y with flag31/32 hover logic and pass-through tiles (noTileCollide presumably), type speed overrides (75 Pixie ±3, 253 Reaper ±4, 330 Poltergeist ±4, 490 creeper? 1.5).

Wait, but before declaring this — maybe our ghostAI models the Wraith (81)? Wraith aiStyle = 22? Let me check what aiStyle 22 members we have and their vanilla names. Let me query.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:54.629Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst data = require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst list = Array.isArray(data) ? data : (data.npcs || data.entries || Object.values(data));\nfor (const e of list) if (e.aiStyle === 22) console.log(e.id, e.name);\n\"; grep -n \"else if (type == 81)\" -A8 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -m1 aiStyle",
 "description": "List aiStyle 22 members and check type 81"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:54.736Z

**📎 ToolResult**

```
75 Pixie
82 Wraith
122 Gastropod
169 Ice Elemental
182 Floaty Gross
253 Reaper
268 Ichor Sticker
316 Ghost
330 Poltergeist
490 Drippler
9774-			aiStyle = 1;

```


---

## 🤖 Assistant · 2026-08-19T03:21:20.694Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
aiStyle 22 family: 75 Pixie, 82 Wraith, 122 Gastropod, 169 Ice Elemental, 182 Floaty Gross, 253 Reaper, 268 Ichor Sticker, 316 Ghost, 330 Poltergeist, 490 Drippler.

Our ghostAI (4725-4780+): 
- Simple lerp model vx += (dir*7 - vx)*0.0125 for ALL members — vs vanilla direction-based X 0.1/±2 (Pixie ±3, Reaper/Poltergeist ±4, Drippler 1.5), Y 0.04/±1.5.
- 122 laser at ai3==32 ✓ (present: fireAt 32, spd 7, dmg 25 — vanilla proj 84 dmg 25 ✓ but range gate: vanilla `num315 < 700` then normalize×7 with RotatedByRandom(0.0125*2π) — ours has d<700 ✓).
- 169 ice burst at ai3==16: vanilla projectile 128 dmg 45 ✓ spd 5 (vanilla num324=5 ✓). 
- 268 ichor: ✓ appears present.
- Missing: the whole flag31/flag32 vertical hover logic (ceiling checks: ghosts float up through solid only if 3 tiles above clear etc.), type speed overrides, 490 drippler spawn-count logic, 316 Ghost despawn-fade (NPCDeath55 + Opacity fade) — ours has the sound only when ai3==1 (4735-4738) — partial.
- Missing: 330 Poltergeist pumpkinMoon gate / 253 eclipse gate (despawn flags) — flag28 handling (EncourageDespawn when event off) — ours missing.
- Missing 75 Pixie wet (vy -= 0.2 cap -2) — wet family table item!
- Missing collideX/Y bounce (-0.4/-0.25 with min ±1).

Hmm — but wait: is ghostAI in my scope? My families: swarmer, charger, jellyfish, demon/imp, harpy/bats, eyes, skeleton hand, plus "其他飞行/水生 case 枚举". Ghost family is flying — "自己 grep case 枚举补全,归你管的报出来" — yes, report it. The lerp-based movement core being a fabricated approximation is a significant finding (all 10 members move wrong: ±2 direction-chase vs 7-speed slow lerp; actually lerp to 7 with 0.0125 is SLOW — e.g., terminal ~7 but takes ~80 ticks to get there; vanilla caps ±2 X / ±1.5 Y with 0.1/0.04 accel — much snappier. The ghost would feel floatier/slower to turn but faster max speed).

Hmm, actually wait — let me reconsider. Maybe our ghostAI movement was derived from Wraith (82)? Let me check the Wraith-specific handling in aiStyle 22... I didn't see type==82 in the branches (only 122/75/169/268/490/330/253/316/75wet/169||268). Wraith is default-member: direction-based. So no — the lerp model isn't from any aiStyle-22 code. It's a "悬停缓速追击" invention. But hold on — maybe it comes from 1405's different structure? The memory note "AI家族100%" suggests they ported all AI families... but ghostAI might be an early approximation. Let me check quickly whether vanilla 1405 has different aiStyle 22 — not needed; 1456 is authoritative.

Severity: 中-严重 for family movement (10 NPC types). I'll mark 中 (these are mostly rare enemies) with the wrong-model caveat.

Also note: ghost family — LOS/pass-through logic (flag31/32) is the "追击门(视线)" territory? The flag31/32 is not a chase gate — it's a vertical hover mechanism. The gates (npcTypeNoAggro) are excluded. I'll report movement model + wet + bounce + event gates, skip npcTypeNoAggro.

Now — the enumeration of remaining flying/aquatic cases (not in assigned families): case 2 floatEyeAI (main fixed; pigron branch note), case 9 bouncingBallAI, case 17 vultureAI (fixed per memory), case 22 ghostAI (report), case 44 flyingSwarmerAI, case 49 angryNimbusAI, case 56 dungeonSpiritAI, case 10 cursedSkullAI (looks complete), case 4 eocAI (out of scope), case 16 swimAI (flag22 fixed; attack/wander blocks verified ✓), case 18 jellyfishAI ✓ done, case 12 hand ✓ done, plus lunar/dd2 flying ones (covered by prior batches per memory).

Quick verification for dungeonSpiritAI (32915) and flyingSwarmerAI (30999) — one glance each to catch glaring diffs. Let me read vanilla 32915-32937 (it's only 22 lines! short) and 30999-31269 (flying fish — longer). And our implementations. Actually dungeonSpirit vanilla block is tiny (32915-32936) — check ours quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:21.535Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 32915,32937p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ===; grep -n \"private dungeonSpiritAI\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read vanilla dungeon spirit + find ours"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:21.592Z

**📎 ToolResult**

```
		else if (aiStyle == 56)
		{
			TargetClosest();
			Vector2 vector103 = new Vector2(base.Center.X, base.Center.Y);
			float num886 = Main.player[target].Center.X - vector103.X;
			float num887 = Main.player[target].Center.Y - vector103.Y;
			float num888 = (float)Math.Sqrt(num886 * num886 + num887 * num887);
			float num889 = 12f;
			num888 = num889 / num888;
			num886 *= num888;
			num887 *= num888;
			velocity.X = (velocity.X * 100f + num886) / 101f;
			velocity.Y = (velocity.Y * 100f + num887) / 101f;
			rotation = (float)Math.Atan2(num887, num886) - 1.57f;
			position += netOffset;
			int num890 = Dust.NewDust(position, width, height, 180);
			Dust dust = Main.dust[num890];
			dust.velocity *= 0.1f;
			Main.dust[num890].scale = 1.3f;
			Main.dust[num890].noGravity = true;
			position -= netOffset;
		}
		else if (aiStyle == 57)
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-19T03:21:22.124Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 30999,31100p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_044 flying fish block start"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:22.187Z

**📎 ToolResult**

```
		else if (aiStyle == 44)
		{
			noGravity = true;
			if (collideX)
			{
				if (oldVelocity.X > 0f)
				{
					direction = -1;
				}
				else
				{
					direction = 1;
				}
				velocity.X = direction;
			}
			if (collideY)
			{
				if (oldVelocity.Y > 0f)
				{
					directionY = -1;
				}
				else
				{
					directionY = 1;
				}
				velocity.Y = directionY;
			}
			if (type == 587)
			{
				position += netOffset;
				if (alpha == 255)
				{
					velocity.Y = -6f;
					netUpdate = true;
					for (int num706 = 0; num706 < 15; num706++)
					{
						Dust dust4 = Dust.NewDustDirect(position, width, height, 5);
						Dust dust = dust4;
						dust.velocity *= 0.5f;
						dust4.scale = 1f + Main.rand.NextFloat() * 0.5f;
						dust4.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
						dust = dust4;
						dust.velocity += velocity * 0.5f;
					}
				}
				alpha -= 15;
				if (alpha < 0)
				{
					alpha = 0;
				}
				if (alpha != 0)
				{
					for (int num707 = 0; num707 < 2; num707++)
					{
						Dust dust5 = Dust.NewDustDirect(position, width, height, 5);
						Dust dust = dust5;
						dust.velocity *= 1f;
						dust5.scale = 1f + Main.rand.NextFloat() * 0.5f;
						dust5.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
						dust = dust5;
						dust.velocity += velocity * 0.3f;
					}
				}
				if (Main.rand.Next(3) == 0)
				{
					Dust dust6 = Dust.NewDustDirect(position, width, height, 5);
					Dust dust = dust6;
					dust.velocity *= 0f;
					dust6.alpha = 120;
					dust6.scale = 0.7f + Main.rand.NextFloat() * 0.5f;
					dust = dust6;
					dust.velocity += velocity * 0.3f;
				}
				position -= netOffset;
			}
			int num708 = target;
			int num709 = direction;
			if (target == 255 || (type != 587 && Main.player[target].wet) || Main.player[target].dead || Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
			{
				this.ai[0] = 90f;
				TargetClosest();
			}
			else if (this.ai[0] > 0f)
			{
				this.ai[0] -= 1f;
				TargetClosest();
			}
			if (netUpdate && num708 == target && num709 == direction)
			{
				netUpdate = false;
			}
			float num710 = 0.05f;
			float num711 = 0.01f;
			float num712 = 3f;
			float num713 = 1f;
			float num714 = 30f;
			float num715 = 100f;
			float num716 = Math.Abs(position.X + (float)(width / 2) - (Main.player[target].position.X + (float)(Main.player[target].width / 2)));
			float num717 = Main.player[target].position.Y - (float)(height / 2);
			if (type == 509)
			{
				num710 = 0.08f;

```


---

## 🤖 Assistant · 2026-08-19T03:21:32.794Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Dungeon Spirit (aiStyle 56): velocity = (v*100 + dir*12)/101 (0.99 inertia blend to speed 12), rotation atan2-1.57, dust 180. Our dungeonSpiritAI — let me find it (it's a method `this.dungeonSpiritAI`). Let me grep its implementation. It was noted "穿墙0.99惯性追踪" in the dispatch comment — sounds right. Quick check.

Flying fish AI_044 — mostly type-specific param tables (509 etc. Hell? 509 = "Ghast... "? whatever). Given time, and memory "近似清零批 — AI_003移动族表" and "AI家族100%" — these were done in other batches. I'll trust and not deep-dive; they're not in my assigned families anyway. I'll just enumerate.

Let me quickly view dungeonSpiritAI ours.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:33.963Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"dungeonSpiritAI(game\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -2; sed -n \"$(grep -n 'private dungeonSpiritAI' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | cut -d: -f1),+30p\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read our dungeonSpiritAI"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:34.061Z

**📎 ToolResult**

```
1279:        case 56: this.dungeonSpiritAI(game, p); break;                    // AI_056 地牢之魂（cs:32915 穿墙0.99惯性追踪）
  private dungeonSpiritAI(_game: GameHooks, player: Player | null) {
    let ex: number, ey: number;
    if (player && !player.dead) {
      this.facing = this.seekDirX(player);
      const d = Math.hypot(player.cx - this.cx, player.cy - this.cy) || 1;
      ex = ((player.cx - this.cx) / d) * 12;
      ey = ((player.cy - this.cy) / d) * 12;
    } else {
      ex = this.facing * 6;
      ey = -6;
    }
    this.vx = (this.vx * 100 + ex) / 101;
    this.vy = (this.vy * 100 + ey) / 101;
    this.visAngle = Math.atan2(this.vy, this.vx) - Math.PI / 2;
    this.x += this.vx;
    this.y += this.vy;
  }

  /** AI_008 法师族（Fire Imp 24 / Goblin Sorcerer 29 / Dark Caster 32）：
   *  悬浮 + 周期传送（原版 ai[0] 计时到阈值或目标不可见时 TeleportSearch）+ 三连弹幕（原版 ai[1] volley）。
   *  弹幕复用 Dart（命中玩家）；传送条件：4-16 格内有地面 + 上下净空（原版 100 次随机试探） */
  /** AI_002_FloatingEye 通用核（NPC.cs:19118-19440）：
   *  分轴非对称加速 X±4 / Y±2.5（Wandering Eye 133 半血以下激怒 ±6/±4）；
   *  撞墙/撞地按 旧速度*-0.5 反弹并保证最小弹速（L19124-19140）；
   *  白天地表驱散（cs:52707/53152 昼散表）：EncourageDespawn(10)+保持水平方向上飞 */
  private floatEyeAI(game: GameHooks, player: Player | null) {
    // 猪龙 grunt（AI_002 :52677-52680）：170/171/180 → PlaySound(29,9)=Zombie_9 1/1000
    if ((this.vanillaId === 170 || this.vanillaId === 171 || this.vanillaId === 180)
      && Math.floor(Math.random() * 1000) === 0) {
      game.playSfxWav?.('Zombie_9', 1, this.cx, this.cy);
    }

```


---

## 🤖 Assistant · 2026-08-19T03:21:58.415Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
dungeonSpiritAI ✓ matches (rotation uses vy not target — vanilla uses num887 (target dir) for rotation; ours uses current velocity — minor visual). Missing dust 180 trail (visual, low). Dead-player branch (facing*6/-6) — null-player territory, skip.

Now, I have enough for the main report. Let me also double-check a few remaining specifics I flagged:

1. swarmerAI hornet: check `player.useTime === 0` — vanilla `player.itemAnimation == 0 && stealth == 0`. Does our Player expose itemAnimation? Not critical; it's a documented approximation. Also the hornet sting gate `ai[1] >= 130` requires LOS else reset — ours: `if (this.ai1 >= 130 && this.canSeePlayer(st, player))` — hmm: vanilla: `if (ai[1] >= 130) { if (CanHit) { ...fire or reset... } else { ai[1] = 0 } }` — ours: if ai1 >= 130 AND canSee → try fire (with direction match else ai1=0). But if ai1 >= 130 and NOT canSee → ours does NOTHING (ai1 keeps growing until LOS). Vanilla resets ai1 = 0 when no LOS at >=130. Ours differs: hornet keeps charging while player behind wall, then fires immediately when LOS regained, rather than resetting. Hmm wait — actually check ours again (3875): `if (this.ai1 >= 130 && this.canSeePlayer(st, player)) { ... }` — no else reset. Vanilla has else → ai1 = 0 (both for the direction-mismatch case ✓ ours has that, and the no-LOS case ✗ missing). Confirmed minor diff (低-中).

Hmm, wait — actually ours: within the fire branch, `else this.ai1 = 0` covers direction mismatch ✓. The outer no-LOS reset is missing. Also ours gates the whole hornet block behind `player && !player.dead` — vanilla runs the ai[1] == 101 sound + accumulation regardless of dead (uses targetData.Type checks). Minor.

2. Check `shootDart` signature to confirm proj id 55/38/44/115 mapping + timeLeft. Let me grep shootDart definition.

3. For batAI missing second-pass — double-check our batAI doesn't have a second movement elsewhere (I read the whole function 4347-4448 — no second pass). Confirmed.

4. Also vanilla bat block: aiStyle 14 sets noGravity=true at top ✓ ours? Our Enemy presumably sets noGravity from def data. Check: bats' defs have noGravity? vanilla SetDefaults for 49: noGravity = true? Let me verify one — cavebat 49 SetDefaults. Actually the AI itself sets `noGravity = true;` in vanilla. Our batAI doesn't set it; if def lacks it, bats would fall. Since bats visibly fly in-game per prior testing, presumably handled. Skip.

5. EoS expert num2 = 0.035: our swarmerAI accel for isEater = 0.02 flat — missing expert ×1.75. Also remixWorld — no remix support, skip (世界类型未支持).

6. Harpy ai[1] bob block missing (23393) — includes harpy/demon special params (0.12/0.07 ±3/±1.25). This is the "wander bob after losing sight" — related to LOS but a distinct timer mechanic. Report as 中/低 with overlap note.

7. Jellyfish 221 localAI[0]=1 + localAI[2] — let me check what consumes these in vanilla. grep "localAI[2]" in NPC.cs around damage/player interactions... Actually for squid: localAI[0]=1 probably triggers ink on death/hit (NPC.hitEffect?). Let me do a quick grep for squid ink.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:59.353Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"localAI\\[2\\] == 1f\\|localAI\\[2\\] == 1\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head; grep -n \"type == 221\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head",
 "description": "Find consumers of jellyfish localAI flags"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:59.396Z

**📎 ToolResult**

```
74660:			if (localAI[2] == 1f)
11772:		else if (type == 221)
24356:					if (type == 221)
24368:						if (type == 221)
89427:			else if (type == 220 || type == 221)
89441:				if (type == 221)

```


---

## 🤖 Assistant · 2026-08-19T03:22:00.337Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"private shootDart\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts; sed -n \"$(grep -n 'private shootDart' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -1 | cut -d: -f1),+25p\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read shootDart helper"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:00.377Z

**📎 ToolResult**

```
1661:  private shootDart(game: GameHooks, ox: number, oy: number, tx: number, ty: number, speed: number, dmg: number, projId = 0): void {
  private shootDart(game: GameHooks, ox: number, oy: number, tx: number, ty: number, speed: number, dmg: number, projId = 0): void {
    const d = Math.hypot(tx, ty) || 1;
    const dart = new Dart(ox, oy, (tx / d) * speed, (ty / d) * speed, dmg, projId);
    dart.hostile = true; // 敌怪发射弹（原版 Projectile.hostile）——联机 v5 随 msg27 bit7 下发
    (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities
      .add(dart, 'projectiles');
  }

  /** 敌怪弹幕发射辅助（原始速度向量版）：Nailhead 463 散射（NPC.cs:57611）等
   *  "速度向量已定"的发射点——shootDart 会把 (tx,ty) 归一到 speed，不适用此处。
   *  projId = 原版弹型（Dart.ts DART_STYLE 表） */
  spawnHostileProj(game: GameHooks, x: number, y: number, vx: number, vy: number, dmg: number, projId = 0): void {
    const dart = new Dart(x, y, vx, vy, dmg, projId);
    dart.hostile = true;
    (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities
      .add(dart, 'projectiles');
  }

  private groundPhysics(game: GameHooks, jumpV = 0, accel = 0.12, maxSpd = 1) {
    // 注：水中行为不在本方法——wet 减速由 npcLiquid→liqFactor 统一承担（原版
    // Collision_MoveWhileWet），浮力族（史莱姆）的弹跳漂浮在各自 AI 的 wet 段（cs:61877）
    this.applyGravity(game);
    this.vx = Math.max(-maxSpd, Math.min(maxSpd, this.vx + accel * Math.sign(this.vx || 1) * 0));
    if (jumpV && this.onGround) this.vy = -jumpV;
    moveAndCollide(this, game.world, this.vx, this.vy);
    this.vx *= this.onGround ? 0.8 : 0.98;

```


---

## 🤖 Assistant · 2026-08-19T03:22:30.177Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
The squid 221 stuff at 89427-89441 is in death/hit code (ink burst on death probably). localAI[2]==1 at 74660 is in FindFrame or scaling? Let me not chase — it's low priority (visual/ink). 

shootDart doesn't set timeLeft — Dart defaults presumably fine (vanilla projectiles default timeLeft... for proj 38/44/55 vanilla sets 300 explicitly since default is 3600? Actually Projectile.timeLeft default = 3600 in vanilla; AI blocks set 300 to cap feather/scythe lifetime. Ours: Dart class default lifespan — unknown; likely shorter. Skip — note as low/uncertain).

Now let me double check the hornet "scale" multiplication and sting proj speed: vanilla num20 = 8 → normalized ×8 ✓ ours speed 8 ✓ dmg 10×scale ✓ ours `Math.round((vid === 176 ? 30 : 10) * vScale)` ✓.

Also hornet/moss-hornet maxSpd: vanilla 42: num=3.5/0.021 (× (1-scale)); 231: 3/0.017; 176: 4/0.017. Ours: 6/0.05 default for all hornets. That's the biggest AI_005 diff — hornets move ~1.7x too fast with 2.4x accel. Confirm severity: 严重? It's a common early-game jungle enemy — very visible. I'd say 严重 (movement speed table wrong for 7 hornet types incl. Moss Hornet, plus Meteor Head 6x, Moth ~2x).

Wait — actually, let me double-check ours: maxSpd selection (3787): `let maxSpd = isEater ? 4 : this.vanillaId === 94 ? 4.2 : this.vanillaId === 5 ? 5 : 6;` — 42/176/231-235 → 6, 23 → 6, 205 → 6, 619 → 6 (but 619 vanilla = 6 ✓), 252 → 6 (parrot critter — gated out), 139 → 6 (vanilla: default 6 ✓; zenith 3 unsupported).

accel (3789): `isEater ? 0.02 : 94 ? 0.022 : 5 ? 0.03 : 619 ? 0.1 : 0.05` — 42/176/231-235 → 0.05 (vanilla 0.021/0.017), 23 → 0.05 (vanilla 0.03), 205 → 0.05 (vanilla 0.018).

So hornets: 6/0.05 vs vanilla 3.5/0.021 (42), 4/0.017 (176), 3/0.017 (231), 3.5×(1-scale)/0.021×(1-scale) others. Confirmed.

Also flag4 for hornets: flag4 vanilla excludes 42/231-235 ✓ ours excludes them ✓.

Also the flag3 "always swarm" includes 42/94/619/176/210/211/231-235 ✓ ours swarmAlways ✓.

Also the near-guidance `dist < 150 && (6/94/173/619)` ✓ ours (3831).

EoS expert accel — ours 0.02 flat. Vanilla: 6/173 0.02, expert 0.035 for type 6 only. Ours: missing expert branch — confirm with difficulty? The class has this.difficulty. Report as 中低.

Now let me also double-check our chargerAI jump gate `this.h >= 32` (4328) — vanilla has no height gate; it has the "flag6" head-clearance check (tiles above the NPC's head: num19..num21 row above). Vanilla: `bool flag6 = true; ... for tiles at row (position.Y - 7)/16 across width: if solid → flag6 = false` — the jump ladder only runs if no solid tile directly overhead. Ours replaced with `this.h >= 32` heuristic — means small NPCs (< 32px tall, e.g., 546 Angry Tumbler 22px? 410 22px) never jump! Vanilla 410/423/546 DO use the ladder. Hmm wait — `this.h >= 32` gates the -8.5/-7.5 branch only? Read ours again:

```
if (vxSign === dir && vxSign !== 0) {
  const fx..., fy...;
  if (this.h >= 32 && solidAt(fx, fy - 2)) { vy = solidAt(fx, fy-3) ? -8.5 : -7.5; }
  else if (solidAt(fx, fy - 1)) vy = -7;
  else if (y + h - fy*TILE > 20 && solidAt(fx, fy)) vy = -6;
  else if (!solidAt(fx, fy+1) && !solidAt(fx+dir, fy+1) && !solidAt(fx+dir, fy+2)) vy = -8;
}
```

The h>=32 gate only blocks the high-jump branch for short NPCs. Vanilla's gate is "no solid tile overhead" (flag6) for the WHOLE ladder. So for short enemies (tumbler 546 h=? def width/height from data — 546 is 22x22? hmm data says width 22 height 22 for 410; 546?), the 2-tile-high jump is suppressed → they'll do -7/-6/-8 instead. Minor behavioral. Also missing the directionY/|vx|>3 gate on the cliff-jump (noted). And vanilla checks `Main.tile[num22 + direction, num23 + 3]` for flag7 types in the last branch (noted).

OK — I think I also should verify the demon AI_008 (Fire Imp 24) since the parent asked about "火小鬼 24?核 aiStyle 归属". Our casterAI — let me quickly check the type-24 branch of vanilla AI_008 (22289? no that's aiStyle 12; aiStyle 8 = 21904-22288). Memory says caster family was redone ("caster12ids重做(ai0=500/==25发射)"). Fire Imp = aiStyle 8. Let me spot check the 24-specific bits: vanilla AI_008 has `if (type == 24)` branch? Let me grep quickly within 21904-22288.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:22:31.808Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 21904,22288p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"type == \\|ai\\[0\\] == \\|Teleport\\|NewProjectile\" | head -25; echo ===OURS===; sed -n \"$(grep -n 'private casterAI' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | cut -d: -f1),+60p\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Compare caster AI type branches with ours"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:31.847Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
6:			if (this.ai[0] == 0f && Main.netMode != 1)
25:			if ((type == 68 || Main.netMode == 1) && localAI[0] == 0f)
40:			if ((type == 68 || Main.IsItDay()) && this.ai[1] != 3f && this.ai[1] != 2f)
50:					if (Main.npc[num174].active && Main.npc[num174].type == type + 1)
96:							int num181 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center5.X, center5.Y, num177, num178, num180, attackDamage_ForProjectiles, 0f, Main.myPlayer, -1f);
(eval):1: ==OURS=== not found

```


---

## 🤖 Assistant · 2026-08-19T03:22:45.721Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Hmm, the range 21904-22288 gave few matches — the interesting branches (Fire Imp triple fireball) must use different text. Whatever — caster family is NOT in my assigned families (the parenthetical only asked me to resolve Fire Imp's aiStyle ownership, which I did: aiStyle 8 → casterAI). The caster family was already redone per memory ("敌怪传送全族审计 — caster12ids重做"). I'll spot-check just enough to answer ownership: our casterAI exists and dispatches case 8 ✓.

Now let me quickly view our casterAI header to confirm it handles 24 (one glance).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:22:46.164Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n \"$(grep -n 'private casterAI' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | cut -d: -f1),+42p\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Read our casterAI header"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:46.192Z

**📎 ToolResult**

```
  private casterAI(game: GameHooks, player: Player | null) {
    const vid = this.vanillaId ?? -1;
    if (!this.aiInit) {
      this.aiInit = true;
      this.ai0 = 500;                        // :20799-20801 初始 500
      this.ai1 = 0; this.ai2 = 0; this.ai3 = 0;
      if (vid === 172) this.spawnAlpha = 255;  // :20797-20804 alpha 0 起步（spawnAlpha=255 对应不可见）
    }
    // 172 符文法师淡入（:20797-20809：alpha 每帧 +1 ≈ spawnAlpha -1/t；受击归零重淡）
    if (vid === 172) {
      if (this.justHit) this.spawnAlpha = 255;
      if (this.spawnAlpha > 0) this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
    }
    // ---- ① 传送执行（:20811-20968）：目的地待执行 → 双端 FX + 改写 ----
    if (this.ai2 !== 0 && this.ai3 !== 0) {
      this.casterTeleportBurst(game);
      this.x = this.ai2 * TILE - this.w / 2 + 8;   // :20888-20889（+8 为贴图格内偏移）
      this.y = this.ai3 * TILE - this.h;
      this.vx = 0; this.vy = 0;
      this.ai2 = 0; this.ai3 = 0;
      this.casterTeleportBurst(game);
    }
    this.ai0 += 1;                                 // :20971 每帧计时
    // :20777-20784 RedHat 变体（红帽骷髅王 35 ai[3]==1 在场 → localAI[3]=1 置位永不清；
    // 帧侧整带 +3、计时双倍）。本仓红帽召唤链未实装（Enemy.redHat 恒 false）→ 恒 0
    // （enemies 可选访问：测试桩 hooks 可能未实现）
    if (vid === 32 && this.lai3 === 0) {
      const enemiesOf = (game as { enemies?: () => unknown[] }).enemies;
      const sk = enemiesOf
        ? (enemiesOf.call(game) as Enemy[]).find((n) => n.vanillaId === 35 && !n.dead)
        : undefined;
      if (sk?.redHat) this.lai3 = 1;
    }
    // :20787-20791 X 摩擦 0.93 + |vx|<0.1 归零（Y 不阻尼——重力由引擎共享段承担）
    this.vx *= 0.93;
    if (this.vx > -0.1 && this.vx < 0.1) this.vx = 0;
    // 物理：全族 SetDefaults 均无 noGravity/noTileCollide → 受重力+瓦片碰撞
    // （传送落点即站面、受击呈正常抛物线回落）。旧实现 vx/vy 同乘 0.9 裸积分——
    // 无重力无碰撞，受击 vy<0 只缓衰减不回落 = "被击退就往上飞"（2026-08-17 用户报告）
    if (!this.vanilla?.noGravity) {
      this.applyGravity(game);
      moveAndCollide(this, game.world, this.vx, this.vy);
    } else {

```


---

## 🤖 Assistant · 2026-08-19T03:23:38.431Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Caster family looks well-developed (per memory). Fine — ownership answer only.

Now let me verify a couple of remaining specifics for the report:

1. Our swarmerAI hornet sting: check canSeePlayer/losClear helpers exist — yes.
2. Our batAI: does vanilla `direction` in batAI = target direction (X sign toward player) ✓ ours seekDirX equivalent via player.cx compare ✓.

3. For the missing "second movement pass" in batAI — wait, I should double-check my reading of the vanilla block structure once more. Re-reading cs:23227: 

```
if (type == 49 || type == 51 || type == 60 || type == 62 || type == 66 || type == 93 || type == 137 || type == 150 || type == 151 || type == 152 || type == 634)
{
    if (wet) { ...buoyancy... TargetClosest(); }
    if (type == 60)
    {
        movement (X 0.1/0.07/0.03 ±4; Y 0.04/0.03/0.02 ±1.5)
    }
    else
    {
        movement (X 0.1/0.1/0.05 ±4; Y 0.04/0.05/0.03 ±1.5)
    }
}
```

Yes — the movement is inside the family-if. And earlier, the same types went through the final `else` of the 158/226/660 chain (they're not 158/226/660). So double application. ✓ Also NOTE: for these 11 types the second pass runs EVERY tick (wet or not). So effectively: demons/hellbats/ice bats/lava bats/illuminant bats/giant bats/spore bats/cave bats/jungle bats/flying foxes/gastropods?? no 122 isn't 14... wait 93 Giant Bat IS in the list. And 634 Spore Bat. OK.

Effective per-tick X: up to 2×0.1 accel toward ±4; Y: 2×0.04 toward ±1.5.

Ours: single pass. → hell/dungeon bat family moves at half accel and half responsiveness. Also the SECOND pass happens AFTER the wet buoyancy — order matters little.

BUT — hmm, one more check: is this second-pass really in the 1.4.5.6 source as I read? Yes — sed showed the structure directly. OK. Though — hmm, let me reconsider whether the first chain `else` includes these types... The first chain: `if (type == 158) {...} else if (type == 226) {...} else if (type == 660) {...} else {...}` — the else catches everything else including 49/51/60/62/66/93/137/150/151/152/634 AND all other bats (121 Slimer, 156 Red Devil, 48 Harpy). So yes.

Hmm OK wait, now I want to reconsider: is this double-pass actually making demons "fast" in vanilla — Demon gameplay: demons fly at you pretty quick ✓ feels right.

4. Also for batAI: vanilla 226 Flying Snake pre-block (LOS-keep-direction) — ours missing ✓ noted. 226 movement: X 0.2/±4 (threshold 4, secondary 0.1, tertiary 0.05), Y 0.1/±2.5 (secondary 0.05, tertiary 0.03). Ours: default 0.1/0.04 ±4/±1.5. Diff.

5. Harpy: ours — the shooter ticks/params ✓; missing the ai[1]>200 bob (shared) — noted.

6. Vampire bat 158 day-flee ✓ ours (day && !eclipse && above worldSurface ✓ ours uses groundLevel ✓).

7. 158→159 transform ✓ ours.

Also check: ours batAI applies `seekDirX` only when player; when player null → dirX = facing — that's null-player scope, skip.

Now compile the final report. Also the "wet 浮力族表" summary:
- AI_005: 6/94/173/619 wet buoyancy (0.3/-2) — ours missing 619 ✓ report; 205 & 42/176/231-235 (0.5/-4 + TargetClosest) — ours has hornets ✓ but missing 205 ✓ report.
- AI_014: family {49,51,60,62,66,93,137,150,151,152,634} + 48 ✓ ours AI014_SWIM_UP ✓ correct.
- AI_002: all but pigrons ✓ ours ✓.
- AI_022: 75 Pixie wet (vy -= 0.2 cap -2) — ours missing ✓ report.
- AI_018: no wet buoyancy section (jellyfish ARE the water family) ✓ n/a.

Double-check our swarmerAI wet for 619: line 3961: `if (inW && (vid === 6 || vid === 94 || vid === 173))` — yes 619 missing. And 205: line 3965 covers 42/176/231-235 — 205 missing (separate vanilla branch, same numbers + TargetClosest). ✓.

Also — one more AI_005 check: ours bounce applies when `this.hitWall` — vanilla collideX. ours bounce uses `bounce = isEater ? 0.4 : 0.7` — vanilla: 0.4 for 6/173; 0.7 for the whole list (619/23/42/94/139/173/176/205/210/211/231-235). Ours: type 5 & 252 also get 0.7 bounce (vanilla: not in list → no bounce) — minor, noted earlier.

And ours dust: `if (!isHornet && vid !== 205 && Math.random() < 1/20)` — vanilla skips dust for 42/139/176/205/210/211/252/231-235; ours doesn't skip 139 (and 252 unreachable via critter gate — fine). Report as one-liner low.

One more: our swarmerAI facing: `this.facing = this.vx > 0 ? 1 : -1` — vanilla hornets: spriteDirection by velocity.X ✓ same; for 23/139: spriteDirection + rotation formula (flip on num4 sign) — ours treats them in the atan2-π/2 bucket (faceTarget excludes them → uses vx,vy with -π/2). Vanilla type 23/139: `spriteDirection=±1; rotation = atan2(num5,num4)` or +π — no -1.57 offset. Ours wrong rotation base for 23/139 → visual. Report low (visual) — actually for 139 Probe, our faceTarget list includes... wait line 3857: `const faceTarget = vid === 6 || vid === 94 || vid === 173 || vid === 619;` — 139 NOT included → 139 uses vx,vy with -π/2. Vanilla 139: rotation = atan2(num5, num4) (target dir, NO -1.57) with spriteDirection flip. So probe rotation differs by 90°+flip model. Visual — 中低. Combined with hornet banking into one "rotation model per-type" finding.

Wait — also for 6/94/173/619 ours rotation = atan2(sy,sx) - π/2 ✓ vanilla ✓.

Bee 210/211 & servant 5 & 252: vanilla else-bucket: rotation = atan2(vy,vx) - 1.57 ✓ ours ✓.

Now the last piece: verify our eocAI exists and is the known-audited version — skip deep check (out of scope). And "克眼之外的眼睛族专属" — I covered floatEye pigron/116/133 notes.

Also confirm the AI014_SWIM_UP: includes 48 ✓ but vanilla 48's wet block is separate from the family (identical numbers) ✓ merged fine.

Also batAI min-bounce uses facing vs vanilla direction — minor, fold into a one-liner.

One more scope item: "恶魔/小鬼族(...水母外的 aiStyle 4/14 专属分支)" — aiStyle 14 type-specific branches: 226 (missing), 158 (params), 660 (Y params), 48/62/66/156 shooters ✓ present, wet family ✓, ai[1] bob (missing). aiStyle 4: EoC only, no type branches — nothing demon there. Done.

Also — hmm, the demon scythe: vanilla proj 44 speed 0.2 with proj's own AI (scythe accelerates). Ours comment says DART_STYLE[44] handles AI_018 accel ×1.06 — that's the projectile side (previously ported). ✓ trust.

The harpy feather proj 38 speed 6 ✓; dmg 15 ✓.

Red Devil 156: ours ticks [20,40,60,80,100] ✓ spd 0.2 ✓ dmg 80 ✓ spread 50 ✓ reset 250 ✓ lead 100 ✓ but missing `vector25 += velocity * 5f` pre-offset (minor) and the shots require CanHit ✓ ours canSeePlayer.

Volley reset cached vs re-rolled — report once (applies to 48/62/66/156): low.

Now — jellyfish: also check ours `lurking` recompute after ai1 changed (4651) ✓ fine; `else this.dontTakeDamage = false` (4629) matches vanilla else-branch ✓. One subtle thing: vanilla sets dontTakeDamage=false EVERY tick when not lurking (else branch), ours same ✓. And when lurkCapable is false (non-expert), vanilla skips the whole lurk section → flag23 false → dontTakeDamage = false ✓ ours: lurking stays false ✓.

Wait — one bug check in ours: `if (inWater && this.ai1 === 1) lurking = true; else this.dontTakeDamage = false;` ✓ vanilla.

But ours: `if (lurkCapable) { ... }` — inside `if (lurking) { this.ai2 += 1; if >= 120 ai1 = 0 }` — vanilla ALSO has dontTakeDamage = true inside flag23 ✓ ours 4641 ✓.

Vanilla light num274 — ✓.

OK also — the attack pulse: ours checks `playerWet && player && canSeePlayer` — vanilla flag24 = `!friendly && TargetClosest(faceTarget:false) && player.wet && !dead && CanHit` — the `!friendly` gate + TargetClosest retarget. Fine.

And squid 221 `localAI[0] = 1` in the stillness pulse — let me quickly check 89427 to see what it does (death ink?). Actually 89427 is in scale-armor or FindFrame? It says `else if (type == 220 || type == 221)` — near 89441 `if (type == 221)`. Probably FindFrame (squid ink animation when attacking). Skip — one-line note.

Let me also double check one thing in batAI — ours doesn't set noGravity; check Enemy def for bats: vanilla SetDefaults 49 sets noGravity = true? Actually the AI sets it each tick. Let me check our enemies handling of noGravity for bats — grep fromVanilla / def noGravity. Quick check: does Enemy.applyGravity get called for aiStyle 14? Our batAI never calls applyGravity and directly moveAndCollide — if def has noGravity... does moveAndCollide apply gravity? Probably gravity applied only via applyGravity in AI. So fine.

Also — IMPORTANT: does our batAI handle the vanilla `if (type == 226)` TargetClosest pre-block? No — covered.

I also want to confirm the claim "hornet sting reset when idle": vanilla `player.stealth == 0f && player.itemAnimation == 0f` → reset ai[1] = 0. Ours: `if (player.useTime === 0) this.ai1 = 0`. In our engine, is there an itemAnimation equivalent? grep quickly player.itemAnimation usage. Eh — ours approximates with useTime===0 (never swinging). useTime is the item's stat (nonzero for held item) — hmm, if player holds an item with useTime > 0 (always), then `player.useTime === 0` is FALSE → reset never happens?? That would make hornets sting much more often! Let me check what player.useTime is in our engine — grep.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:23:39.214Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"useTime\" ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts | head -8; grep -n \"get useTime\\|useTime =\\|itemAnimation\" ~/Project/GLM/SandboxWorld/game/src/entities/Player.ts | head -10",
 "description": "Check Player useTime/itemAnimation semantics"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:23:39.251Z

**📎 ToolResult**

```
236:  useTime = 0;           // 通用动作冷却
300:   *  ——Game 鞭 useTime 结算读取；312/365 登记持续期（效果端暂不接） */
584:    whipSpd: number;       // 鞭 useTime 倍率（黑曜套 1/1.15）
1026:   *  封顶 3 后取倒数，作为 useAnimation/useTime 的时长乘数。原"猛爪手套 ×2"档已废——
1117:  /** 用魔物品起手（Game 在设定 useTime 后调用）：登记动画窗，窗内每帧重置
1119:   *  ItemCheck_ApplyManaRegenDelay :49851；本仓单计时器模型以 useTime 代 useAnimation） */
1121:    this.manaAnimTicks = Math.max(this.manaAnimTicks, this.useTime);
1288:    if (this.useTime > 0) this.useTime--;
139:  /** 用魔物品动画窗剩余 tick（itemAnimation>0 期每帧重置 delay，:42131-42137） */
218:  /** 原版 itemAnimation 等效（>0 = 挥舞动画中）：芦苇管换气门禁（:22920/:3698）
236:  useTime = 0;           // 通用动作冷却
237:  /** 手持物品 useTurn（Item.cs SetDefaults；Game 每帧注入）——itemAnimation 窗内
1118:   *  manaRegenDelay（Player.cs:42131-42137 itemAnimation>0 && item.mana>0 →
1858:    // :19546-19556 门：itemAnimation 窗内仅 useTurn 物品允许移动改朝向
1955:        // :19546-19556：itemAnimation 窗内仅锁【朝向】不锁移动（挥砍中可跑）——
2757:    // （攻击中 itemAnimation 门→近似 useTime>0 暂停 5t）；星璇套=双击↓开关 vortexStealthActive
3062:    // :22436-22445 ChangeDir（itemAnimation==0 时按牵引方向转身）
3063:    if (this.itemAnimTicks <= 0 && this.useTime <= 0) {    // itemAnimation == 0（窗代理含 useTime）

```


---

## 🤖 Assistant · 2026-08-19T03:24:04.072Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So in our engine, `player.useTime` = generic action cooldown (0 when idle), and there's also `itemAnimTicks` (itemAnimation equivalent). So `useTime === 0` ≈ idle — a reasonable proxy for itemAnimation==0. OK, the hornet idle reset works approximately. Drop that from findings (or mention as OK).

Now let me finalize. Before writing, let me quickly double check two more claimed diffs to be safe:

1. batAI Y-axis hardcode — verify ours line numbers 4379-4388 and that 660/158 set ay but the secondary values are hardcoded. Yes (read earlier): lines 4380-4388: `if (this.vy > cy) this.vy -= 0.05; else if (this.vy > 0) this.vy += 0.03;` — hardcoded. Confirmed.

2. The 158 X threshold: ours `if (this.vx > cx) this.vx -= ax` with cx=7; vanilla threshold 4. Confirmed.

3. Charger pounce for 155/329 missing — ours only 546 (4317). Confirmed.

4. Vanilla charger: `if (ai[3] < num) { if ((type == 329 || type == 315) && !Main.pumpkinMoon) EncourageDespawn(10); else TargetClosest(); }` — hellhound/headless horseman despawn off-event. Ours: no pumpkinMoon gate. Minor (低) — fold into 315/329 finding.

5. Unicorn: `num11=6, num12=0.07` default ✓ ours maxSpd=6 accel=0.07 ✓; reverse damp: default branch has NO damp for unicorn (only 155/329/315/410/423/546 have damp) — ours applies 0.95 damp to ALL incl. unicorn (4297). Vanilla unicorn: no reverse damp — when direction flips, velocity keeps and the accel pulls it around... wait but then the gate `if (!flag && (velocity.Y == 0f || wet || ...))` — unicorn on ground moving away from direction: `velocity.X <= 0 && direction < 0` — moving left with direction left → in gate. Moving RIGHT with direction LEFT (reverse): gate fails → NO accel at all (waits for turn). Hmm interesting — so vanilla unicorn turning = stop accel until... anyway ours: applies damp 0.95 + accel always. Diff: low.

6. Goblin shark wet ✓ matches; land missing everything — confirm our chargerAI call for 620 — `this.chargerAI(game, p, 1)` — yes maxSpd=1.

Wait — actually maybe maxSpd=1 was chosen deliberately ("on land it flops slowly")? Vanilla: 8/0.21 with 0.9 damp + ranged 811 volleys + leaps. Definitely different. Report 中.

7. For AI_005 — one more check on ours: `const flag4 = !isEater && vid !== 94 && vid !== 619 && vid !== 42 && !(vid >= 231 && vid <= 235) && vid !== 139;` — vanilla flag4 = type != 173 && != 6 && != 42 && !(231-235) && != 94 && != 139 && != 619 ✓ equal. ✓

8. Ours: bees vx clamp `else if (this.vx > 6)... else if (this.vx < -6)...` — the else-if chain: `if (ramp > 1) {ramp=1} else if (vx > 6) {vx=6} else if (vx < -6) {vx=-6}` — hmm! If vx is e.g. 5 (not > 6, not < -6), no clamp ✓ fine. But if vx > 6 → clamp to 6 ✓. OK functionally fine except ramp==1 boundary for vy (noted, negligible — skip).

9. swarmerAI: vanilla bee 210/211 — `NPCUtils.TargetClosestNonBees` — skip (targeting infra).

10. Meteor head (23): speed 6/0.05 vs vanilla 1/0.03 + rotation base diff. Also vanilla 23 is in bounce list (0.7) ✓ ours ✓. And 23 dust: ours `!isHornet && vid !== 205` → 23 gets dust ✓ vanilla: 23 IS in the "no-dust skip list"? The skip list: 42/139/176/205/210/211/252/231-235 — 23 NOT in it → 23 DOES get dust (else branch 1/40? no wait). Re-read: `if (type == 6 || 619 || 23 || 42 || ... ) { bounce...dust 1/20 (skip list within) } else if (type != 252 && rand(40)) { dust }` — for the big list family: dust 1/20 EXCEPT skip-list types (which get none). 23 not in skip list → dust 1/20 ✓ ours gives dust 1/20 (color 18 purple — vanilla dust 18? for 23: num17 = 18, 173→5 ✓; hmm vanilla 23 in the 1/20 dust group with dust 18 ✓ fine).

OK. One more: our swarmerAI near-guidance condition `dist < 150 && (isEater || 94 || 619)` ✓ vanilla (6/94/173/619) ✓.

Now — where's the daytime despawn for AI_005 in ours? Let me check whether Enemy.ts has a global daytime-despawn for flyers (EYE_DAY_DESPAWN for floatEye). For swarmers: vanilla cs:51324: daytime && type not in nocturnal list → vy -= num2*2, EncourageDespawn(10). Members affected: 5 (servant), 139 (probe), 252... Let me grep our Enemy.ts for a swarm day-despawn. Search "EYE_DAY_DESPAWN" and any similar for aiStyle 5.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:04.886Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"EYE_DAY_DESPAWN\\|encourageDespawn\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -20; grep -n \"isDay\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -20",
 "description": "Check day-despawn handling in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:04.924Z

**📎 ToolResult**

```
211:const EYE_DAY_DESPAWN = new Set([2, 133, 190, 191, 192, 193, 194, 317, 318]);
389:      this.encourageDespawn(300);
406:      this.encourageDespawn(300);
411:      this.encourageDespawn(60);
547:    if (tgt.dead) this.encourageDespawn(300);
1654:  encourageDespawn(despawnTime: number): void {
2437:      this.encourageDespawn(10);
3610:      && this.vanillaId != null && EYE_DAY_DESPAWN.has(this.vanillaId);
3613:      this.encourageDespawn(10);
5862:    if (!wt.shouldUseWindyDayMusic) this.encourageDespawn(10); // :43257
6932:      this.encourageDespawn(10);
410:    if (this.vanillaId === 621 && game.world.clock.isDay) {
1111:      if (w?.clock?.isDay && w?.store) {
1612:      if (cs.gate === 'day') ok = clock.isDay;
1613:      else if (cs.gate === 'night') ok = !clock.isDay;
1614:      else if (cs.gate === 'dawn') ok = clock.isDay && clock.timeOfDay < Clock.DAWN + (Clock.DUSK - Clock.DAWN) / 3;  // Main.time<18000(清晨 1/3)
1616:        && (!clock.isDay || this.y > world.groundLevel * 16);
1858:    let flag3 = !game.world.clock.isDay || hurt || underground || !!game.world.weather.slimeRain;
2429:    const daySurface = game.world.clock.isDay && !game.world.clock.eclipse
3608:    const day = game.world.clock.isDay && !game.world.scene?.zoneGraveyard;
4363:      && game.world.clock.isDay && !game.world.clock.eclipse) {
4859:    const day = game.world.clock.isDay;
5280:      if (!game.world.clock.isDay || this.cy / TILE > game.world.groundLevel + 10) {
6074:    const bloodNight = !w.clock.isDay && w.clock.bloodMoon;
6930:    if (game.world.clock.isDay || player.dead) {

```


---

## 🤖 Assistant · 2026-08-19T03:24:21.628Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
No global AI_005 daytime despawn — line 547 `if (tgt.dead) this.encourageDespawn(300)` — that's probably the shared targeting part (null-player scope). The daytime clause at 51324 (fly up + EncourageDespawn) is missing for swarmers (affects 5/139/252 + any unlisted member; main nocturnal list covers most). Also 619 day: `velocity.Y -= 0.3 + EncourageDespawn(60)` at 50636 (blood squid daytime). Missing. Also — is there a generic "underground check"? Vanilla clause has no y-position gate for AI_005! It's purely daytime (surface check absent) — underground hornets etc. are excluded from despawn by type list (all the common ones are in the exclusion list). Affected: 5, 139, 252. Servant of Cthulhu despawning at day ✓ vanilla; probe 139 despawn at day ✓. Ours: neither. 低 (servant dies fast anyway; probes spawn during mech fights at night? probes can persist to day rarely).

OK — now also confirm ours handles AI_005 "flag" (dead player) — excluded from my scope (null player). Right.

Now — let me also double check the AI_026 stuck/gate structure once more for the "movement gate" claim: `if (!flag && (velocity.Y == 0f || wet || (velocity.X <= 0f && direction < 0) || (velocity.X >= 0f && direction > 0)))` — hmm wait, this gate wraps the type-specific damp/accel including the SHARED accel at the end. Actually re-reading the vanilla block: the gate `if (!flag && (...))` contains the per-type branches AND then the shared num11/num12 accel. So the whole accel is gated by grounded|wet|moving-toward-direction. Ours applies damp+accel unconditionally. For a unicorn mid-jump moving toward player: gate true (velocity.X toward direction) ✓ same. Mid-jump moving away (after knockback): vanilla skips accel, ours damps 0.95 + accels. Minor → fold into one line.

I think I've got everything. Let me also spot-check our eocAI existence/line count for the report reference (6886). It's known-audited. Fine.

Also — "其他未列 case 枚举" — I'll list: case 9 bouncingBallAI (弹跳球,cs:21349 — prior batch), case 10 cursedSkullAI (verified detailed ✓ — includes 694 book mimic + 289 per memory), case 17 vultureAI (fixed), case 22 ghostAI (findings), case 44 flyingSwarmerAI (prior batch "近似清零"), case 49 angryNimbusAI (prior batch), case 56 dungeonSpiritAI (✓ 1:1 modulo dust/dead branch), plus trap cases 20/21. And swimAI beyond flag22: verified attack/wander/out-of-water blocks match (with pufferfish/dolphin specials present). One check I didn't do: swimAI "螺旋转向/专家模式特化略" comment — vanilla AI_016 expert spiral? cs:24019 area. Eh — the comment admits omissions ("螺旋转向/专家模式特化略"). Let me quickly verify what that refers to: vanilla aiStyle 16 at ~23750-23820 might have an expert spiral chase. Let me grep quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:22.169Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n 23748,23810p ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check vanilla AI_016 expert spiral section"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:22.203Z

**📎 ToolResult**

```
						{
							velocity.Y = 10f;
						}
					}
					return;
				}
			}
			if (wet)
			{
				bool flag22 = false;
				if (type != 55 && type != 592 && type != 607 && type != 615 && type != 688)
				{
					TargetClosest(faceTarget: false);
					if (Main.player[target].wet && !Main.player[target].dead && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
					{
						flag22 = true;
					}
				}
				int num265 = (int)base.Center.X / 16;
				int num266 = (int)(position.Y + (float)height) / 16;
				if (Main.tile[num265, num266].topSlope())
				{
					if (Main.tile[num265, num266].leftSlope())
					{
						direction = -1;
						velocity.X = Math.Abs(velocity.X) * -1f;
					}
					else
					{
						direction = 1;
						velocity.X = Math.Abs(velocity.X);
					}
				}
				else if (Main.tile[num265, num266 + 1].topSlope())
				{
					if (Main.tile[num265, num266 + 1].leftSlope())
					{
						direction = -1;
						velocity.X = Math.Abs(velocity.X) * -1f;
					}
					else
					{
						direction = 1;
						velocity.X = Math.Abs(velocity.X);
					}
				}
				if (!flag22)
				{
					if (collideX)
					{
						velocity.X *= -1f;
						direction *= -1;
						netUpdate = true;
					}
					if (collideY)
					{
						netUpdate = true;
						if (velocity.Y > 0f)
						{
							velocity.Y = Math.Abs(velocity.Y) * -1f;
							directionY = -1;
							this.ai[0] = -1f;
						}

```


---

## 🤖 Assistant · 2026-08-19T03:24:35.503Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
No expert spiral here. Where's "spiral steering"? Maybe for 157? The 157 wander block I partially saw. Our swimAI has the arapaima wander block ✓. Fine — swimAI appears well covered apart from the flag22 already fixed. Good enough — one more check on ours: the flag22 noChase set {55, 592, 607, 615, 688} — ours has exactly {55,592,607,615,688} ✓ (4504-4505).

Now — before finalizing, one more re-verification of the biggest claims by re-reading the exact ours lines:

1. swarmerAI hornet speeds — ours 3787-3790. ✓
2. batAI second-pass missing — ours function spans 4347-4448, single movement block 4369-4388. ✓
3. chargerAI 620 maxSpd 1 — dispatch line 1282-1284 (`else this.chargerAI(game, p, 1);`). Let me get exact line number. From the earlier read: lines 1281-1284:
```
case 107:
  if (this.vanillaId !== 620) ai107ImprovedWalkers(this, game, p);
  else this.chargerAI(game, p, 1);
  break;
```
Line ~1282/1283. Let me grep exact.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:36.569Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"chargerAI(game, p, 1)\\|case 107\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts; grep -n \"case 26: this.chargerAI\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts; grep -n \"private eocAI\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Get exact line numbers for dispatch entries"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:36.607Z

**📎 ToolResult**

```
1281:        case 107:                                                          // AI_107 ImprovedWalkers（NPC.cs:63372-64919）
1283:          else this.chargerAI(game, p, 1);                                 // 620 地精鲨（wet 游泳档,cs:64118-64230 专属分支）
1280:        case 26: this.chargerAI(game, p); break;                        // AI_026 独角兽/冲锋族（原版核）
6886:  private eocAI(game: GameHooks, player: Player | null) {

```


---

## 🤖 Assistant · 2026-08-19T03:26:04.596Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have everything. Let me also quickly note the eocAI one thing — actually let me do a 30-second sanity scan of eocAI to see if it's the full state machine (since "克眼之外的眼睛族" excludes it, I'll just reference it as covered by prior audit). Skip.

Also — one last item to verify for batAI: vanilla aiStyle-14 `ai[1] > 200` bob block — ours missing entirely. Let me confirm no ai1 usage in our batAI... From my read of 4347-4448: ai0 used for shooters, ai2 for threshold cache, ai1 only in bee?? no that's swarmer. batAI has no ai1 counter ✓ missing.

Also confirm vanilla harpy ai[1] params: num238=0.2/num239=0.1/num240=4/num241=1.5; for 48/62/66: 0.12/0.07/3/1.25. Right.

Also for completeness on the demon family (aiStyle 14): ours' demon/voodoo shooter ticks [20,40,60,80] ✓ matches vanilla. Red devil ✓.

Also note the vanilla bat block ends `if (type != 156) return; ... return;` — fine.

Now — what about the second pass ALSO being applied for type 60 Hellbat with DIFFERENT params (0.1/0.07/0.03 X; 0.04/0.03/0.02 Y)? Ours missing ✓ (part of second-pass finding).

Let me now also double-check the claim about vanilla collideX bounce in batAI using oldVelocity: `velocity.X = oldVelocity.X * -0.5f` — ours `this.vx = -oldVx * 0.5` ✓.

OK — also the 619 blood squid dash+shot (cs:51271-51307): ours missing. And 619 hover-below-target (cs:50803-50805: `type == 619 && base.Center.Y > targetData.Center.Y - 200f → velocity.Y -= 0.3f`) — ours missing. And 619 daylight despawn + fade dust — missing. Also 619 spawn dust (cs:50636-50665) — missing. Also 619 wet buoyancy missing (noted). So blood squid is the most incomplete AI_005 member — grouped as one finding 中.

Also hornet Y-damp above surface (cs:50749-50757) missing — merge into hornet speed finding.

I'm confident in the report now. Structure:

### 分发/归属澄清
- Fire Imp 24 = aiStyle 8 → casterAI ✓ (1456 SetDefaults :9010); Demon 62/Voodoo 66 = aiStyle 14 → batAI ✓ (:9499/:9556); aiStyle 4 = EoC 专属无 type 分支 (:8639 一处) — "AI_004 恶魔"不成立.
- chargerAI 实际覆盖 AI_026 {86 独角兽,155 狼,315 无头骑士,329 地狱犬,410 Sroller,423 Evolution Beast,546 怒滚虫} + 620;黄蜂 42/231-235 实际在 AI_005(swarmerAI) — 毒刺链已在那边.

### 各族发现 (with line numbers)

Let me now assign severities and write it up concisely. Count total confirmed diffs:

**AI_005 swarmerAI (Enemy.ts:3779-3984 vs NPC.cs:50626-51356):**
1. [严重] 速度/加速表缺 hornet 族+Meteor Head+Moth: 42=3.5/0.021×(1-scale), 231=3/0.017, 176=4/0.017, 23=1/0.03, 205=3.25/0.018 (cs:50720-50766); ours 全落默认 6/0.05 (3787-3790). 症状: 黄蜂 1.7×速/2.4×加速、陨石弹头球 6×速、蛾 1.8×速.
2. [中] hornet 附加 Y 阻尼 (cs:50749-50757) 缺: 地表上方 target dy>300 且 vy<0 → ×0.97; dy<80 且 vy>0 → ×0.97.
3. [中] 619 血鱿鱼整链缺 (cs:50636-50665 白天上升+EncourageDespawn(60)+淡入尘; 50803-50805 悬于目标上方-200; 51271-51307 localAI[0]≥120+LOS+<400px → 后撤 velocity=-dirTo×5 + 射弹 811×15 速35伤, 否则 localAI[0]=50; justHit 时 localAI[0]+=10). ours 仅 6/0.1 加速档.
4. [中] 94 腐化者唾液计时用错槽: vanilla localAI[0] (+1/t, justHit 清零, ==180 发射) (cs:51258-51276); ours 用 ai2 且无 justHit 清零 (3885-3892).
5. [中低] 139 探针远距增速门错: vanilla `flag2(>600px)` 全时生效 num27=12 (mech 才 5) (cs:51237-51250); ours 仅 mechQueenUp 时 cap5 (3918-3924) → 常规探针远距无增速/无 0.9 逆向衰减.
6. [中低] EoS 专家加速缺: type6 expert num2=0.035 (cs:50690-93); ours 恒 0.02.
7. [低] wet 表缺 619 (cs:51106 含 619; ours 3961 无) 与 205 (cs:51107-51116; ours 3965 无).
8. [低] 摆动相位近距清零: vanilla num7≤100 时 ai[0] 保持(冻结), ours 归零 (3827-3828).
9. [低] 撞墙反弹门: vanilla 仅 bounce 列表族(6/619/23/42/94/139/173/176/205/210/211/231-235) 反弹 (cs:51047-51066); ours 全员反弹 → 仆从5 出弹跳.
10. [低] 旋转模型: hornet 族(42/176/205/231-235)应为 spriteDirection(vx)+rotation=vx×0.1 倾斜 (cs:51031-51037); 23/139 应 spriteDirection 翻转+atan2(±π 无 -1.57) (cs:51003-51028); ours 全员 atan2-π/2 (3850-3860).
11. [低] 尘: 139 应免尘 (cs:51083-51091); 白天驱散段(5/139/252, cs:51324-51329) 缺.
12. [低] ai[1]≥130 无 LOS 时 vanilla 清零 (cs:51167-51171 else), ours 挂起等 LOS (3875) — 越墙后立即sting.
13. [低] hornet ai[1] 累加缺 ×scale (cs:51153); sting 弹 timeLeft=300 未显式 (cs:51199).

**batAI (Enemy.ts:4347-4448 vs cs:22895-23543):** (主体已修部分不重报;以下为专属分支)
1. [严重] 恶魔/蝙蝠 11 类 {49,51,60,62,66,93,137,150,151,152,634} 的第二段移动整缺 (cs:23227-23372): 家族块内 wet 浮力后还有一次完整 X/Y 步进 (60 Hellbat: 0.1/0.07/0.03 ±4 + 0.04/0.03/0.02 ±1.5; 其余 0.1/0.1/0.05 ±4 + 0.04/0.05/0.03 ±1.5) → 原版双步进, ours 单步进 = 恶魔/地狱蝠族水平响应减半.
2. [中] 158 吸血蝙蝠 X 二档阈值: vanilla 4f/二次 0.1/三次 0.05 (cs:22962-22980); ours 用 cap7 阈值+0.1/0.1 (4370-4378).
3. [中] Y 轴二/三档修正硬编码默认值 0.05/0.03 (4380-4388): vanilla 158: 0.1/0.05 (cs:22982-23000 阈值4); 660: 0.3/0.225 (cs:23124-23147, 0.75×); 226: 0.05/0.03 — ours 660 巨狐蝠 Y 修正 0.05 vs 应 0.3.
4. [中] 226 飞蛇专属分支整缺: LOS 保持方向预块 (cs:22927-22941) + 移动档 X 0.2/±4、Y 0.1/±2.5 (cs:23002-23081); ours 走默认 0.1/0.04 ±4/±1.5.
5. [中低] ai[1]>200 失视振荡段缺 (cs:23393-23462): 失视200t后 ai[2] 摆动 (vy ±0.1/0.07, vx 0.2/0.12, 48/62/66 档 0.12/0.07 ±3/±1.25), 玩家非湿+有视线才复位; 158 双倍计数. (与"视线门"代理可能重叠, 报备)
6. [低] 俯冲变形 158→159 ✓ / 白天离场 ✓ / 湿浮族表 ✓ (48+11类, AI014_SWIM_UP :215 与 vanilla cs:23232+23372 全等) — 正确项.
7. [低] 射击族齐射后阈值: vanilla 每帧重掷 400+rand(400) (cs:23500-23503 等); ours 缓存 ai2 单掷 → 平均间歇翻倍 (4443-4445). 哈比/恶魔/红恶魔弹速/伤/散布 ✓.
8. [低] 红恶魔 156 出生预偏移缺 velocity×5 (cs:23538).

**jellyfishAI (4621-4721 vs cs:24210-24474):** 基本 1:1 ✓ (潜伏/发光/攻击脉冲/漂移/离水全对上). 
1. [低] localAI[2]=1/0 与 221 鱿鱼 localAI[0]=1 未持久化 (cs:24366/24395/24421) — 消费端在渲染/命中侧, 行为影响未证.
2. [低] direction==0 时 TargetClosest 应在攻击/漂移前 (cs:24289-24292); ours 仅漂移分支尾部 (4708).

**chargerAI/AI_026 (4279-4340 vs cs:62809-63371) + 620 (cs:64118-64230):**
1. [中] 620 地精鲨陆地段: dispatch 传 maxSpd=1 (1283) vs vanilla num23=8/num24=0.21/num25=0.9 (cs:64150-64152); 且缺: ai[0]>0 攻击循环 (60t windup, ai[1]==40 射 proj811 速13 带 |dx|×0.15 弧补+±2.5散布, justHit 重置, ai[1]=150 冷却) (cs:64551-64660), 夜间出水扑咬跳 (vy=-11/-13/-14/-15.9 按头顶格数) (cs:64212-64230), 白天 flag23 驱散. wet 档 wetSwimStep(620) ✓ 与 cs:64291-64334 全等.
2. [中] 155 狼/329 地狱犬扑跳缺: 贴近<100px、|vx|>3、朝玩家移动 → vy-=4 (cs:63003-63009); ours 仅 546 (4317). 329 另有逆向 0.9+3px 内 ±0.1 推进 (cs:63064-63076) ours 用通用 0.95.
3. [中] 410 Sroller 自爆链整缺 (cs:62937-62968): ai[1]≥240 或玩家头顶<20px·800 内 → 3×弹538 + 即死. 423 Evolution Beast 冲击波状态机整缺 (cs:62969-63001: 180t 蓄→60t 冲, ai[1]==30 后射弹575 反向7速).
4. [中] 546 怒滚虫专属缺: 沙漠区门 (玩家非 ZoneDesert → EncourageDespawn+ai[3]=30) (cs:63018-63027), 风速调制 num11=4+lerp(wind)×3×direction、num12=0.05 (cs:63125-63136), rotation+=vx×0.05+spriteDirection=-direction (cs:63346-63349), 同族斥离 (cs:62820-62846).
5. [中] 315 无头骑士骑手弹缺: localAI[0]≥480 → 弹1001 (伤40/30, 带 velocity.y+rand3f) + 灯头尘帧4-7 (cs:62850-62878); 点光 ✓ 有.
6. [低] 跳梯门差: vanilla 悬崖跳需 directionY<0 或 |vx|>3 (cs:63273); flag7 类(410/423) 加 fx+dir,fy+3 检查 (cs:63276); 整梯受"头顶无实心"门 flag6 (cs:63157-63168) — ours 用 h>=32 代理 (4328).
7. [低] 卡墙计数不衰减 (vanilla 移动时 ai[3]-=1, cs:62875-62877); 315/329 非南瓜月驱散门缺 (cs:63030-63034); 独角兽逆向阻尼 ours 多加了 0.95 (vanilla 默认档无) (4297); 超速落地 ×0.8 全向衰减缺 (cs:63154-63158).

**eye 族 (floatEyeAI 3595-3681 vs AI_002 cs:52673-53127):** 主体已修 ✓; 湿浮力尾段 ✓ (3673-3678 = cs:53117-53127 含猪龙豁免). 
1. [低] 猪龙 170/171/180 穿墙相位机制缺 (cs:52726-52791: 无视线 300t → ai[1]=1, alpha=200+noTileCollide 穿墙绕行; 恢复视线清回) — 或属主体已修范围, 报备.
2. [低] 116 The Hungry 专属速度档 (X ±6 0.1/0.1/0.2; Y 上2.5下1.5) (cs:52825-52899) 走通用 4/2.5.

**skeletronHandAI (bossAI.ts:177-211 vs cs:22289-22604):**
1. [严重] 五态机 (ai[2]=0/3 悬停→1 蓄升→2 直冲→4 侧浮→5 回冲) 未移植: vanilla 蓄升 vy-=0.1 到头-200 后 18/21(expert)/24(getGood) 速直冲, 点积≤0/越玩家/2000px 退出 (cs:22487-22551); 侧浮 ±500 后 17/22 速回冲 (cs:22552-22600). ours 是弹簧 lerp 近似 (200/230 锚 + 8 速 120t 追击) — 手永不升空俯冲.
2. [中] 专家档全缺 (蓄升 cap-13/额外-0.06; 侧浮 ±12; 冲速 21/22); rotation=atan2(锚)+1.57 未设; 头死→ ours 即死, vanilla ai[2]+=10 且 >50 才死.

**ghostAI (4725-4780 vs cs:24726-25316):**
1. [中] 移动核模型错: ours lerp (dir×7, 0.0125) — 该两数实为 122 激光参数 (cs:24866-24883 num312/num317); vanilla 为方向步进 X 0.1/±2 (75→3,253→4,330→4,490→1.5) + Y 0.04/±1.5 + flag31/32 悬浮/穿行逻辑 (cs:25191-25315) — 影响全 10 员 (幽灵/幽灵龙/食尸鬼…/滴血者).
2. [低] 75 Pixie wet 浮力缺 (vy-=0.2 cap-2, cs:25170-25177); collideX/Y 反弹 (-0.4/-0.25, min ±1) 缺 (cs:25179-25197); 330 非南瓜月/253 非日食/490 白天驱散门缺 (cs:24729-24740).

**枚举补全 (飞行/水生 case 清单):** case 2 floatEyeAI(主体✓), 4 eocAI(前期批已审), 5/14/18/26/107 本报告, 9 bouncingBallAI/44 flyingSwarmerAI/49 angryNimbusAI/17 vultureAI(历批已 1:1), 10 cursedSkullAI ✓(含694/289 专属, 抽查全等), 22 ghostAI(上述), 56 dungeonSpiritAI ✓ (0.99 惯性+12速全等, rotation 基向用速度而非目标向量 — 低), 12 手(bossAI, 上述). swimAI flag22 外的攻击/游荡/离水段抽查全等 (±3/±2, 65/102/692 ±5/±3, 157 ±7/±4 及 >8→7 怪癖 1:1).

**存疑:**
- jellyfish localAI[2]/221 localAI[0] 消费端未定位 (渲染侧?).
- 射弹 timeLeft (38/44/55/115/811) 是否 300 — Dart 默认寿命未查.
- AI_005 大量行为差异是否被并行"视线门"代理覆盖 (ai[1]>200 bob 与 hornet LOS reset 两处).
- 252 Parrot 走 critter gate, AI_005 的 LOS 变速 (2/0.01 ↔ 6/0.1) 不达 — 若 parrot 非 critter 则为缺口; 数据标 critter ✓ 按原版 (parrot 是 critter).

Count: swarmerAI 13 + batAI 8 + jellyfish 2 + charger 7 + eyes 2 + hand 2 + ghost 2 = 36. Top3: (1) batAI 恶魔/蝙蝠族第二段移动缺失 [严重]; (2) AI_005 hornet/meteor/moth 速度表 [严重]; (3) skeletronHandAI 五态机 [严重] (or 620 land / AI_026 type branches). Top3 必修: batAI second pass, AI_005 speed table, hand state machine.

Wait — I should double-check the "flag2 = num7 > 600" claim once more (139 boost): cs: `bool flag2 = false; if (num6 > 600f) flag2 = true;` where num6 = distance BEFORE normalization ✓. Then `if (type == 139 && flag2) { ... num27 = 12; if (IsMechQueenUp) num27 = 5; ... }` ✓. So regular probes: dist>600 → boost up to 12. Ours: only mech. ✓ my claim stands.

And the mech reposition `ai[2]==0` gate: vanilla `if (type == 139 && IsMechQueenUp && ai[2] == 0f)` ✓ ours ✓.

One more verify on the demon second pass — could the double-pass have been the fix mentioned in "batAI 主体已修"? I.e., maybe the parent's "主体已修" refers to the current state INCLUDING double pass somewhere else? I read the full function — single pass only. Unless moveAndCollide is called twice? No. OK.

Also should double check that ours' `AI014_SWIM_UP` block runs before movement ✓ (4392-4397 before moveAndCollide at 4398) — vanilla runs wet before the second pass ✓ fine ordering.

One more — jellyfish: vanilla wet block starts with the slope handling then collideX/Y — ours ✓.

Also — jellyfish attack-form: vanilla `return`s right after pulse (no drift logic) ✓ ours returns (4686) ✓.

Also ours jellyfish drift: `if (this.facing === 0)` at 4708 — fine.

Now severity for AI_005 #1: hornets are ubiquitous in jungle — 严重. Meteor Head 6× speed — that's severe too (meteor biome defense). OK.

Let me write the final report in Chinese (the user's working language), dense, per-family, with line numbers both sides, symptom, minimal fix suggestion, confidence. Keep it controlled in length.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:27:08.742Z · glm-x-preview-260804

```
所有族现已审计完毕。正在编译最终报告。

## 敌怪 AI 全量 1:1 行为审计报告(飞行/水生族;只读取证)

### 归属澄清(先回答悬案)

- **火小鬼 24 = aiStyle 8**(1456 SetDefaults :9010)→ 我方 `casterAI`,非 AI_004。恶魔 62/巫毒恶魔 66 = **aiStyle 14**(:9499/:9556)→ `batAI`(弹幕表已在那边)。**aiStyle 4 全源码仅 type 4(EoC)一处**(:8639),块内 19909-20758 无任何 type 专属分支 —— "AI_004 恶魔"不成立。
- **黄蜂 42/231-235 实际是 aiStyle 5**(:9211)→ 毒刺/冲刺链在 `swarmerAI` 内,不在 chargerAI。`chargerAI` 实际覆盖 AI_026 {86 独角兽, 155 狼, 315 无头骑士, 329 地狱犬, 410 Sroller, 423 Evolution Beast, 546 怒滚虫} + 620 地精鲨。
- 我方数据(vanilla-npcs.json)aiStyle 归属与 1456 逐条核对一致(含 121 Slimer=14)。

---

### 1. AI_005 蜂群 swarmerAI(Enemy.ts:3779-3984 vs NPC.cs:50626-51356)

8px 网格量化(:3811-3815 = cs:50792-50804)、摆动门 num8/flag3 分族(:3818-3829 = cs:50826-50848)、近距 0.007 制导、flag4 双步进、反弹系数 0.4/0.7、Mechdusa 挂链、探针射击段 —— 均已 1:1。差异:

| # | 级 | 我方 | 原版 | 症状/最小修复 |
|---|---|---|---|---|
| 1 | **严重** | :3787-3790 速度表仅 6/173/94/5/619,黄蜂族全落默认 **6/0.05** | cs:50720-50766:42=3.5/0.021×(1−scale);231=3/0.017;176=4/0.017;**23 陨石怪=1/0.03**;205 蛾=3.25/0.018 | 黄蜂 1.7×速/2.4×加速,陨石怪 6×速,蛾 1.8×速。补表即可 |
| 2 | 中 | 无 | cs:50749-50757 黄蜂地表上方 Y 阻尼(dy>300&&vy<0 或 dy<80&&vy>0 →×0.97) | 黄蜂追进/追出地表时垂直过冲 |
| 3 | 中 | :3885-3892 腐化者用 **ai2** 计时,无受击清零 | cs:51258-51276 用 **localAI[0]**,justHit 清零,==180 发射 | 受击后唾液节奏不重置;槽位错(ai2 与 mech 探针语义冲突风险) |
| 4 | 中 | 无 | cs:51271-51307 **619 血鱿鱼**:白天 vy−0.3+Despawn(60)、淡入尘(:50636-50665)、悬目标上方−200(:50803)、localAI[0]≥120+LOS+<400 → 后撤 −dirTo×5 + 射弹 811×15(伤 35) | 血月钓鱼副产物整段缺失 |
| 5 | 中低 | :3918-3924 远距增速仅 `mechQueenUp()` 时 cap 5 | cs:51237-51250 `flag2`(>600px)**恒生效**:常规 cap **12** 增速 ×1.05 / 逆向 ×0.9;mech 才 5 | 常规机械三王探针远距无追击增速 |
| 6 | 中低 | :3789 恒 0.02 | cs:50690-93 type 6 专家 0.035 | 专家噬魂怪加速差 1.75× |
| 7 | 低 | :3961/:3965 wet 表漏 **619、205** | cs:51106-51116 两族各自 vy−0.3/−0.5 钳 −2/−4+TargetClosest | 入水不上浮 |
| 8 | 低 | :3827 近距摆动 ai0=0 | cs:50831 num7≤100 时**冻结不归零** | 振荡相位每近距重置 |
| 9 | 低 | :3947 反弹全员(含 type 5 仆从) | cs:51047 反弹门=12 类型列表;列表外(type 5/252)只出尘不反弹 | 仆从克眼撞墙出现原版没有的弹跳 |
| 10 | 低 | :3850-3860 全族 `atan2−π/2` | cs:51003-51037:黄蜂族=tilt `vx×0.1`+spriteDirection;23/139=spriteDirection 翻转+atan2(±π,**无 −1.57**) | 黄蜂整身旋转、陨石怪/探针朝向基座错 |
| 11 | 低 | :3875 ai1≥130 无视线时挂起 | cs:51167-51171 无 CanHit → **ai1=0** | 越墙恢复视线瞬间即蜇(vs 重新蓄力);另 :3872 累加缺 ×scale |
| 12 | 低 | 无 | cs:51324-51329 白天驱散(5/139/252 等列表外)vy−2×num2+Despawn(10) | 白天仆从/探针滞场(死亡玩家分支归另一代理,此处仅白天维度) |

### 2. batAI(aiStyle 14,Enemy.ts:4347-4448 vs cs:22895-23543)

撞墙 −0.5 反弹、默认档 0.1/0.04 ±4/±1.5、158 白天离场、158→159 变形(:4412-4417 = cs:23385-23400)、湿浮族表(AI014_SWIM_UP :215 = cs:23232+23372 两处并集全等)、哈比/恶魔/红魔弹幕参数(:4424-4430 = cs:23463-23543)—— 已对上。差异:

| # | 级 | 我方 | 原版 | 症状/最小修复 |
|---|---|---|---|---|
| 1 | **严重** | 单段移动 | cs:23227-23372:**{49,51,60,62,66,93,137,150,151,152,634} 11 类在通用 else 段之后还有第二段完整 X/Y 步进**(60:0.1/0.07/0.03+0.04/0.03/0.02;其余 0.1/0.1/0.05+0.04/0.05/0.03) | 恶魔/地狱蝠/冰蝠/熔岩蝠/发光蝠/巨型蝠/孢子蝠水平响应减半(原版双步进≈0.2/t)。补第二遍循环 |
| 2 | 中 | :4370-4378 158 X 二档阈值=cap(7) | cs:22962-22980 阈值 **4f**、二次 0.1、三次 0.05 | 吸血蝙蝠大速度区间缺第二段减速 |
| 3 | 中 | :4380-4388 **Y 轴二/三档硬编码 0.05/0.03** | cs:23124-23147 660 Y 二次=0.3、三次=0.225(0.75×);cs:22982-23000 158 Y=0.1/0.05 阈值 4 | 巨狐蝠垂直修正弱 6×;158 同病 |
| 4 | 中 | 无 | cs:22927-22941+23002-23081 **226 飞蛇**:失视线保持速度方向 + 专属档 X 0.2/±4、Y 0.1/±2.5 | 飞蛇走默认档(慢且垂直弱) |
| 5 | 中低 | 无 | cs:23393-23462 **ai[1]>200 失视振荡**:失视 200t 后 ai[2] 驱动 vy±(0.1/0.07;48/62/66=0.12/0.07 ±3/±1.25)+vx 摆动,玩家非湿+有视线才归零;158 计数×2 | 失视后直线发呆而非盘旋搜寻(★与"视线门"代理可能重叠,报备) |
| 6 | 低 | :4443-4445 齐射阈值缓存单掷 | cs:23500 等 每帧重掷 `400+rand(400)` | 哈比/恶魔/红魔平均齐射间歇≈2× |
| 7 | 低 | :4440 lead=100 | cs:23538 红魔出生点还 `+= velocity×5` | 三叉戟出生位置小偏差 |

### 3. jellyfishAI(Enemy.ts:4621-4721 vs cs:24210-24474)

潜伏态/专家门/发光×1.5/攻击脉冲(阻尼逐族 0.98²⁻⁵/静止阈值/7|9 脉冲)/漂移振荡/液深探测/离水坠落 —— **逐行全等,基本 1:1**。仅:

- [低] :4667 攻击态未持久化 vanilla `localAI[2]=1`、:4684 未置 221 鱿鱼 `localAI[0]=1`(cs:24366/24395/24421)——消费端在渲染/受击侧,行为影响未证(存疑)。
- [低] :4708 `direction==0→TargetClosest` 应在攻击/漂移分派前(cs:24289-24292),ours 在漂移尾部。

### 4. chargerAI / AI_026 + 620(Enemy.ts:4279-4340、dispatch :1280-1284 vs cs:62809-63371、64118-64230、64551-64660)

通用核(卡墙 30t 翻向、200px 重置、0.07 加速、跳梯 -8.5/-7.5/-7/-6、台阶 16.1 步升)已同构。**620 wet 档 `wetSwimStep(620)`(:2320-2384)与 cs:64291-64334 全等**(Lerp 0.05/巡航 3-5-8、amount2/3、direction 怪癖)。差异:

| # | 级 | 我方 | 原版 | 症状/最小修复 |
|---|---|---|---|---|
| 1 | 中 | :1283 陆地走 `chargerAI(…, maxSpd=**1**)` | cs:64150-64152 num23=**8**/num24=0.21/num25=0.9;cs:64551-64660 攻击循环(60t windup、ai[1]==40 射 **proj811** 速 13 带 \|dx\|×0.15 弧补±2.5 散布、justHit 重置、150 冷却);cs:64212-64230 夜间出水扑咬跳 −11/−13/−14/−15.9 | 被打上岸后 1px/t 爬行、无远程、无跃咬 |
| 2 | 中 | :4317 扑跳仅 546 | cs:63003-63009 **155 狼/329 地狱犬**:贴近<100、\|vx\|>3、朝玩家 → vy−=4;cs:63064-63076 329 逆向 0.9+3 内 ±0.1 推进 | 狼/地狱犬不扑;329 用通用 0.95 |
| 3 | 中 | 无 | cs:62937-62968 **410 自爆**(240t 或玩家顶上 800px 内 → 3×弹538+即死);cs:62969-63001 **423 蓄力冲**(180t 蓄→60t,ai[1]==30 反向射弹 575 速 7,冷却 −320..−601) | 日塔两怪技能整缺 |
| 4 | 中 | 无 | cs:63018-63027+63125-63136+63346-63349+62820-62846 **546**:沙漠区驱散门、风速调制 `num11=4+lerp(0.6,1,\|wind\|)×3×dir`、rotation+=vx×0.05、spriteDirection=−dir、同族斥离 | 怒滚虫无滚转/风偏/成群推挤 |
| 5 | 中 | 仅点光(:4286) | cs:62850-62878 **315 骑手弹**:localAI[0]≥480 → 弹 1001(40/30 伤)+灯头尘(帧 4-7) | 无头骑士不掷南瓜头 |
| 6 | 低 | :4328 跳梯以 `h>=32` 代理头顶门;悬崖跳无 \|vx\|>3 门;flag7 缺 fy+3 检查 | cs:63157-63168(头顶净空 flag6)、cs:63273(directionY<0\|\|\|vx\|>3)、cs:63276 | 矮个怪跳梯档错、低速也大跳 |
| 7 | 低 | :4323 卡墙计数不衰减;无 315/329 非南瓜月驱散;:4297 独角兽多吃 0.95 阻尼;无超速全向 ×0.8 | cs:62875-76 / 63030-63034 / 63057-63072 / 63154-63158 | 微观节奏差 |

### 5. 眼睛族(floatEyeAI :3595-3681 vs AI_002 cs:52673-53127)

主体已修不重报;湿浮力尾段(:3673-3678 = cs:53117-53127,猪龙豁免全等)✓;133 激怒档 ✓。仅:

- [低] **猪龙 170/171/180 穿墙相位**缺(cs:52726-52791:失视线累计 300t → ai[1]=1, alpha 200+noTileCollide 绕墙;恢复视线/出墙清回)——疑似属"主体"范围,报备待定。
- [低] 116 The Hungry 专属档(X ±6、Y 上 2.5/下 1.5,cs:52825-52899)走通用 4/2.5。

### 6. 骷髅王手 skeletronHandAI(bossAI.ts:177-211 vs cs:22289-22604)

- [**严重**] **五态机未移植**:vanilla ai[2] 0/3 悬停(±200,+230,ai[3] 300t 专家×1.5)→ 1 蓄升(vy−0.1 至头−200)→ 2 直冲(**18/专家21** 速,dot≤0/越线/2000px 退)→ 4 侧浮(±8/12)→ 5 回冲(17/22 速);rotation=atan2(锚)+1.57。ours 是弹簧 lerp(±200/+230 锚 + 8 速 120t 追击,bossAI.ts:189-209)—— **手永不升空俯冲/回冲**,头部旋转也不设。
- [中] 专家档全缺;头死 ours 立即 `dead`(:181)vs vanilla ai[2]+=10 且 >50 才死(cs:22295-22303)。

### 7. ghostAI(Enemy.ts:4725-4780 vs cs:24726-25316)—— 枚举补全归我管的飞行族

- [中] **移动核模型整体错**:ours `vx += (dir×7 − vx)×0.0125`(:4742-4743)——这两个数实为 122 激光的速度/散布参数(cs:24866-24883 num312=7/num317=0.0125),被误读成移动。vanilla 为方向步进 X 0.1/±2(**75→3、253/330→4、490→1.5**)+ Y 0.04/±1.5 + flag31/32 悬浮-穿行逻辑(cs:25191-25315)。影响全 10 员(幽灵/死神/食尸鬼/滴血者/漂浮怪等)。
- [低] 75 Pixie wet 浮力(vy−0.2 钳 −2,cs:25170-25177)缺;collideX/Y 反弹 −0.4/−25%(cs:25179-25197)缺;330 非南瓜月/253 非日食/490 白天驱散门(cs:24729-24740)缺。122/169/268 三套射击链已 1:1 ✓。

### 枚举补全(其余飞行/水生 case 处置)

`case 10` cursedSkullAI(抽查 34/289/694 分支全等)、`case 56` dungeonSpiritAI(0.99 惯性+12 速 = cs:32915-32936 全等;rotation 基向用速度而非目标向量,低)、`case 16` swimAI flag22 外的攻击/游荡/离水段逐数全等(±3/±2、65/102/692 ±5/±3、157 ±7/±4 含 >8→7 原版怪癖、河鲀/海豚专属)、`case 9/17/44/49` 历批已 1:1、`case 4` eocAI 前期 Boss 批已审 —— 均不再展开。legacy `flyAI`(:6752)仅旧存档 key 兜底,非数据驱动路径。

---

### 总计与优先级

**确认偏差 36 条**(严重 3 / 中 14 / 中低 3 / 低 16),存疑 4(水母 localAI 消费端、弹 timeLeft=300、ai[1]>200 振荡与并行"视线门"代理的重叠归属、猪龙相位是否算 floatEye 主体)。

**Top3 必修**:
1. **batAI 恶魔/蝙蝠 11 类第二段移动缺失**(Enemy.ts:4369-4388 后补 cs:23227-23372 循环)—— 恶魔全难度出镜,移动手感减半;
2. **AI_005 速度表**(Enemy.ts:3787-3790 补 42/231-235/176/23/205 档 + expert 6)—— 陨石怪 6× 速最失真;
3. **skeletronHandAI 五态机重写**(bossAI.ts:177-211)—— 骷髅王战斗核心副手行为(蓄升俯冲)整体缺失。

其次建议同批带走:620 陆地段(batAI 同文件的 wetSwimStep 已好,只差陆地核)、ghostAI 移动核纠偏、410/423/546/315 四个塔/月事件专属段。
```
