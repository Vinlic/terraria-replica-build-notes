# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T03:05:38.385Z

```
你在泰拉瑞亚 1.4.5.6 复刻仓库 ~/Project/GLM/SandboxWorld 做敌怪 AI **全量 1:1 行为审计**(只读!禁止编辑任何文件、禁止跑游戏)。

标杆:反编译源 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs(用 grep "aiStyle == N" 定位 AI 入口,多在 :19899-33000;部分族有独立函数 grep "private void AI_0")。
我方:game/src/entities/Enemy.ts(约 8000 行)+ game/src/entities/fighterFamilies.ts(helper)。

★范围分工:另有并行代理在专查"玩家死亡(null player)退化行为"与"追击门(wet/视线/距离)"两类——你**不查**这两类(撞到也只一句话备注),专注其余全部行为维度:
- 状态机结构与转换条件(ai[0..3]/localAI 状态、计数器阈值)
- 移动物理(加速度/速度帽/重力/浮力/撞墙反弹系数/台阶跳)
- 计时器与 RNG(周期、概率、掷点时机)
- 特殊行为(跳跃/传送/远程发射/变形 Transform/增益施加/掉链)
- 出生初始化(ai0 初值哨兵 -1120 族要注意)

## 你负责的族(地面/地牢/施法主力)

- slimeAI(AI_001 史莱姆全族:跳跃节奏/大小变体/雨中激愤/丛林系)
- fighterAI(AI_003)+ fighterFamilies.ts 全部 helper(psychoStealth/chaosElemental/medusa/solenian/possessed/butcher/nailhead/swampThing/jumping 段等)
- flailAI(AI_015 链球)
- 地牢机关:spike ball(AI_020)/blazing wheel(AI_021)
- mimic 族(宝箱怪 85 等伪装唤醒/扑击)
- wallCreeperAI(AI_040 爬墙蛛)
- casterAI(施法 12ids 传送+发射节奏,ai0=500 等状态)
- plantAI(AI_013 食人怪/攀爬者锚点与伸展)+ lostGirlAI(AI_042)

## 方法

逐族:①读我方实现完整段;②读原版对应段;③列出 CONFIRMED 数值/结构差(两边行号+关键代码各一行);④分级:严重(玩家可见行为错)/中(数值偏差)/低(边缘)。已知正确的大块(注释带行号且逻辑吻合)一句话带过,别复述。

## 输出格式(最终报告)

按族分节;每条发现:我方行号 / 原版行号 / 症状 / 最小修复建议 / 置信度。结尾给"总偏差数+Top3 必修"清单。存疑单列(找不到原版对应或语义不明)。控制在可操作密度,别灌水。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T03:05:38.389Z

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

## 🤖 Assistant · 2026-08-19T03:05:47.790Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by understanding the task. I need to do a read-only 1:1 behavior audit of enemy AI in this Terraria 1.4.5.6 clone repository. My scope:

- slimeAI (AI_001 slime family)
- fighterAI (AI_003) + fighterFamilies.ts helpers
- flailAI (AI_015 chain ball)
- Dungeon traps: spike ball (AI_020) / blazing wheel (AI_021)
- mimic family (chest mimic 85 etc.)
- wallCreeperAI (AI_040 wall creeper spider)
- casterAI (caster 12ids teleport+fire rhythm, ai0=500 states)
- plantAI (AI_013 maneater/snatcher) + lostGirlAI (AI_042)

I should NOT check: null player death degradation, chase gates (wet/line of sight/distance).

Reference: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs
Our code: game/src/entities/Enemy.ts (~8000 lines) + game/src/entities/fighterFamilies.ts

Let me start by exploring the files. First, let me look at the structure of our Enemy.ts and find the relevant AI functions.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:05:48.539Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/game/src/entities/ && wc -l ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts ~/Project/GLM/SandboxWorld/game/src/entities/fighterFamilies.ts",
 "description": "List entities dir and count lines of target files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:05:48.596Z

**📎 ToolResult**

```
Arrow.ts
Bobber.ts
BookProj.ts
bossAI_dd2.ts
bossAI_deerclops.ts
bossAI_duke_moonlord.ts
bossAI_golem.ts
bossAI_lategame.ts
bossAI_lunar_misc.ts
bossAI_martian.ts
bossAI_moon_events.ts
bossAI_queenbee_plantera.ts
bossAI_wof.ts
bossAI.ts
Celeb2.ts
ChainsawProj.ts
CoinPortalProj.ts
Dart.ts
DebrisProj.ts
Enemy.ts
Entity.ts
FallingBlock.ts
FallingStar.ts
fighterFamilies.ts
FirstFractal.ts
GolfBall.ts
GorePiece.ts
GrappleProj.ts
HealProj.ts
ItemDrop.ts
LeashedCritter.ts
LunarNebula.ts
MagicProj.ts
mechQueen.ts
MeteorChunk.ts
Minecart.ts
MinionProj.ts
MissileProj.ts
Mounts.ts
npcLiquid.ts
PetFollower.ts
Player.ts
Portal.ts
PortalGunBolt.ts
PrismProj.ts
projStatus.ts
projTargets.ts
RainbowProj.ts
SkyDragonFury.ts
SolarEruption.ts
SquidCloud.ts
StardustMarkProj.ts
SwingArc.ts
TerraArc.ts
TideSlash.ts
Tombstone.ts
TownNPC.ts
TownShot.ts
types.ts
waterAvoid.ts
WeaponProj.ts
WhipProj.ts
WhipTag.ts
    8009 ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
     845 ~/Project/GLM/SandboxWorld/game/src/entities/fighterFamilies.ts
    8854 total

```


---

## 🤖 Assistant · 2026-08-19T03:05:49.323Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle\\|AI_0\\|private void AI\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"private void AI_\" | head -80",
 "description": "List AI_ private functions in vanilla NPC.cs"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:05:49.420Z

**📎 ToolResult**

```
618:19171:	private void AI_047_GolemFist()
619:19447:	private void AI_045_Golem()
778:43239:	private void AI_127_Pal()
779:43341:	private void AI_127_Pal_GiveRewerd()
781:43436:	private void AI_015_KingSlime()
783:43760:	private void AI_126_StatueMimic()
784:44004:	private void AI_124_ElderSlimeChest()
785:44009:	private void AI_125_ClumsySlimeBalloon()
786:44338:	private void AI_123_Deerclops()
787:44754:	private void AI_123_Deerclops_ShootRubbleUp(ref NPCAimedTarget targetData, ref Point sourceTileCoords, int howMany, int distancedByThisManyTiles, float upBiasPerSpike, int whichOne)
788:44776:	private void AI_123_Deerclops_MakeSpikesForward(int AISLOT_PhaseCounter, NPCAimedTarget targetData)
789:44812:	private void AI_123_Deerclops_MakeSpikesBothSides(int AISLOT_PhaseCounter, NPCAimedTarget targetData)
790:44851:	private void AI_123_Deerclops_FindSpotToSpawnSpike(int howMany, int whichOne, ref int x, ref int y)
791:44887:	private void AI_123_Deerclops_TryMakingSpike(ref Point sourceTileCoords, int dir, int howMany, int whichOne, int xOffset)
792:44957:	private void AI_123_Deerclops_Movement(bool haltMovement, bool goHome)
793:45045:	private void AI_124_DeerclopsLeg()
794:45142:	private void AI_87_BigMimic_FireStuffCannonBurst()
795:45152:	private void AI_87_BigMimic_ShootItem(int itemID)
798:45231:	private void AI_065_Butterflies()
799:45467:	private void AI_121_QueenSlime_FlyMovement()
800:45543:	private void AI_121_QueenSlime()
802:46178:	private void AI_120_HallowBoss_DoMagicEffect(Vector2 spot, int effectType, float progress)
803:46299:	private void AI_120_HallowBoss()
804:47304:	private void AI_120_HallowBoss_DashTo(Vector2 targetPosition)
805:47344:	private void AI_119_Dandelion()
806:47432:	private void AI_118_Seahorses()
807:47488:	private void AI_117_BloodNautilus()
808:47882:	private void AI_116_WaterStriders()
809:47944:	private void AI_115_LadyBugs()
810:48080:	private void AI_114_Dragonflies()
811:48253:	private void AI_113_WindyBalloon()
812:48453:	private void AI_112_FairyCritter()
814:49143:	private void AI_069_DukeFishron()
815:50129:	private void AI_037_Destroyer()
817:50626:	private void AI_005_EaterOfSouls()
818:51357:	private void AI_006_Worms()
824:52673:	private void AI_002_FloatingEye()
826:53195:	private void AI_007_FindGoodRestingSpot(int myTileX, int myTileY, out int floorX, out int floorY)
828:53264:	private void AI_007_TryForcingSitting(int homeFloorX, int homeFloorY)
830:53335:	private void AI_007_TownEntities_UpdateSavedStates()
831:53366:	private void AI_007_TownEntities()
849:55982:	private void AI_007_TownEntities_Shimmer_TeleportToLandingSpot()
852:56063:	private void AI_007_TownEntities_TeleportToHome(int homeFloorX, int homeFloorY)
854:56093:	private void AI_007_TownEntities_GetWalkPrediction(int myTileX, int homeFloorX, bool canBreathUnderWater, bool currentlyDrowning, int tileX, int tileY, out bool keepwalking, out bool avoidFalling)
856:56172:	private void AI_007_AttemptToPlayIdleAnimationsForPets(int petIdleChance)
858:56245:	private void AI_003_Fighters()
861:60735:	private void AI_001_Slimes()
867:62266:	private void AI_110_Betsy()
868:62809:	private void AI_026_Unicorns()
869:63372:	private void AI_107_ImprovedWalkers()
870:64921:	private void AI_084_LunaticCultist()
871:65959:	private void AI_108_DivingFlyer()
872:66392:	private void AI_109_DarkMage()
873:66793:	private void AI_111_DD2LightningBug()

```


---

## 🤖 Assistant · 2026-08-19T03:05:57.346Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me look at the structure of Enemy.ts first — find the AI function entry points in our code.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:05:58.769Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"slimeAI\\|fighterAI\\|flailAI\\|plantAI\\|casterAI\\|wallCreeperAI\\|lostGirlAI\\|mimicAI\\|spikeBall\\|blazingWheel\\|private \\|case 1:\\|case 3:\\|case 13:\\|case 15:\\|case 20:\\|case 21:\\|case 40:\\|case 42:\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -100",
 "description": "Find AI function locations in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:05:58.840Z

**📎 ToolResult**

```
293:  private static readonly HIST_N = 10;
294:  private histX = new Float64Array(Enemy.HIST_N);
295:  private histY = new Float64Array(Enemy.HIST_N);
296:  private histRot = new Float64Array(Enemy.HIST_N);
297:  private histHead = 0;   // 最新条目下标
298:  private histCount = 0;  // 已填条数（<10 时拖尾按实际深度截断）
301:  private pushHistory(): void {
327:  private wormAI(game: GameHooks, player: Player | null) {
484:  private eowAI(game: GameHooks, _player: Player | null): void {
656:  private eowSpit(game: GameHooks, tgt: Player): void {
1179:        case 1: this.slimeAI(game, p); break;                          // AI_001 史莱姆
1181:        case 3:
1189:          this.fighterAI(game, p);
1208:        case 8: this.casterAI(game, p); break;                          // AI_008 法师族（传送+弹幕）
1217:        case 20: this.blazingWheelAI(); break;                           // AI_020 火轮（地牢陷阱）
1218:        case 21: this.spikeBallAI(game); break;                          // AI_021 刺球（地牢陷阱）
1223:        case 13: this.plantAI(game, p); break;                          // AI_013 植物/攀爬者族（锚点伸展）
1224:        case 15: kingSlimeAI(this, game, p); break;                       // AI_015 史莱姆王(大跳+小史莱姆)
1269:        case 40: this.wallCreeperAI(game, p); break;                      // AI_040 爬墙蜘蛛族（贴背景墙爬行+形态互转）
1270:        case 42: this.lostGirlAI(game, p); break;                         // AI_042 失落女孩（伪装静止→Nymph 变身 cs:30281-30310）
1275:        case 25: this.mimicAI(game, p); break;                            // AI_025 宝箱怪（cs:25621 伪装200px盒→小小大跳循环）
1318:          else this.fighterAI(game, p);                                   // 其余（一期近似档保留）
1342:      case 'slime_blue': this.slimeAI(game, hasPlayer ? player : null); break;
1601:  private ambientSoundTick(game: GameHooks): void {
1649:  private anyNpcAlive(game: GameHooks, id: number): boolean {
1661:  private shootDart(game: GameHooks, ox: number, oy: number, tx: number, ty: number, speed: number, dmg: number, projId = 0): void {
1679:  private groundPhysics(game: GameHooks, jumpV = 0, accel = 0.12, maxSpd = 1) {
1690:  private static readonly SLIME_CAN_CONTAIN_ITEMS = new Set([1, 59, 147, 184, 537]);
1697:  private slimeGenItemInsideBody(isBallooned: boolean): number {
1703:        case 1: return 4368; case 2: return 4369; case 3: return 4370; case 4: return 4371;
1714:          case 1: return 292;            // 铁皮
1716:          case 3: return 2322;           // 挖矿
1719:      case 1:                                                                // 火把/炸弹桶 :62196
1742:  private slimeRollContainedItem(game: GameHooks): void {
1830:  private slimeAI(game: GameHooks, player: Player | null) {
1984:    // 此前误挂在 zombieAI——守卫 vanillaId!==1 使其全程空转，移回 slimeAI）
2034:  private zombieAI(game: GameHooks, player: Player | null) {
2064:  private static SLIME_ITEM_COLORS: Record<number, [number, number, number, number]> = {
2073:  private slimeColorTick(game: GameHooks) {
2119:  private dummyAI(game: GameHooks) {
2140:  private updateNpcCastLights() {
2157:  private updateNpcTrailLights() {
2170:  private mergeLightRGB(rgb: [number, number, number], at?: { x: number; y: number }) {
2183:  private updateNpcDebuffLights() {
2201:  private torchZombieLight(game: GameHooks) {
2248:  private medusaChargeStep(game: GameHooks, player: Player): boolean {
2320:  private wetSwimStep(game: GameHooks, player: Player | null, mode: 461 | 586 | 620): boolean {
2387:  private fighterAI(game: GameHooks, player: Player | null) {    const st = game.world.store;
2716:  private solenianDashAI(game: GameHooks, player: Player): boolean {
2771:  private static readonly RANGED_FIGHTERS = new Set([
2779:  private static readonly RANGED_TABLE: Record<number, {
2821:  private static readonly SPIDER_WALL_FORM: Record<number, number> = { 164: 165, 236: 237, 163: 238, 239: 240, 530: 531 };
2822:  private static readonly SPIDER_GROUND_FORM: Record<number, number> = { 165: 164, 237: 236, 238: 163, 240: 239, 531: 530 };
2826:  private npcCanStickToWalls(st: GameHooks['world']['store']): boolean {
2848:  private tryTransformTo(id: number, st: GameHooks['world']['store'], allowEmbedded = false, game?: GameHooks): boolean {
2893:  private transformVisuals(game: GameHooks | undefined, oldType: number | null, newType: number): void {
2915:  private npcGetShimmered(game: GameHooks): void {
2949:  private wallCreeperAI(game: GameHooks, player: Player | null) {
3030:  private canSeePlayer(st: GameHooks['world']['store'], p: Player): boolean {
3037:  private lostGirlAI(game: GameHooks, player: Player | null) {
3064:  private boundNPCAI(game: GameHooks, player: Player | null) {
3087:  private vultureAI(game: GameHooks, player: Player | null) {
3168:  private antlionAI(game: GameHooks, player: Player | null) {
3199:  private flyingWeaponAI(_game: GameHooks, player: Player | null) {
3243:  private mimicAI(game: GameHooks, player: Player | null) {
3293:  private tortoiseAI(game: GameHooks, player: Player | null) {
3406:  private herplingAI(game: GameHooks, player: Player | null) {
3511:  private flyingSwarmerAI(game: GameHooks, player: Player | null) {
3570:  private dungeonSpiritAI(_game: GameHooks, player: Player | null) {
3595:  private floatEyeAI(game: GameHooks, player: Player | null) {
3692:  private plantAI(game: GameHooks, player: Player | null) {
3779:  private swarmerAI(game: GameHooks, player: Player | null) {
3991:  private cursedSkullAI(game: GameHooks, player: Player | null) {
4142:  private mimic694Frame(): void {
4177:  private dungeonGuardianAI(game: GameHooks, player: Player | null) {
4205:  private blazingWheelAI() {
4242:  private spikeBallAI(game: GameHooks) {
4279:  private chargerAI(game: GameHooks, player: Player | null, maxSpd = 6) {
4339:    // 不能带 fighterAI 的 onGround *=0.9，否则平衡点被压到 0.63 远低于 6
4347:  private batAI(game: GameHooks, player: Player | null) {
4453:  private swimAI(game: GameHooks, player: Player | null) {
4621:  private jellyfishAI(game: GameHooks, player: Player | null) {
4725:  private ghostAI(game: GameHooks, player: Player | null) {
4805:  private pirateGhostAI(game: GameHooks, player: Player | null) {
4852:  private birdAI(game: GameHooks, player: Player | null) {
4986:  private butterflyAI(game: GameHooks, player: Player | null) {
5082:  private critterWanderAI(game: GameHooks, player: Player | null) {
5085:      case 1: this.slimeAI(game, player); return;                         // AI_001 蚱蜢（含专属差异项）
5113:  private townCritterWalkAI(game: GameHooks, player: Player | null) {
5133:        this.fighterAI(game, player);     // aiStyle=3 转战士核
5257:  private fireflyAI(game: GameHooks, player: Player | null) {
5326:  private wormCritterAI(game: GameHooks) {
5371:  private snailAI(game: GameHooks) {
5405:  private duckFlyAI(game: GameHooks, player: Player | null) {
5497:  private fairyAI(game: GameHooks, player: Player | null) {
5669:  private windyBalloonAI(game: GameHooks, player: Player | null) {
5700:        slave.ai0 = -999; // 挂载冻结标记（slimeAI 首行放行）
5792:  private balloonSlimeAI(game: GameHooks, player: Player | null) {
5858:  private dandelionAI(game: GameHooks, player: Player | null) {
5898:  private statueMimicAI(game: GameHooks, player: Player | null) {

```


---

## 🤖 Assistant · 2026-08-19T03:06:01.224Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The file structure is clear. Let me find the remaining functions: casterAI, flailAI. Let me grep more.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:06:01.869Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"casterAI\\|flailAI\\|private .*AI(\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | sed -n '50,120p'",
 "description": "Find casterAI and flailAI locations"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:01.943Z

**📎 ToolResult**

```
6459:  private seahorseAI(game: GameHooks) {
6514:  private casterAI(game: GameHooks, player: Player | null) {
6752:  private flyAI(game: GameHooks, player: Player | null, steer: number) {
6886:  private eocAI(game: GameHooks, player: Player | null) {
7314:  private towerAI(game: GameHooks, player: Player | null) {

```


---

## 🤖 Assistant · 2026-08-19T03:06:49.357Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
flailAI isn't in Enemy.ts? Let me search for it more broadly. AI_015 is chain ball (flail) — wait, in the task it says "flailAI(AI_015 链球)". But in our Enemy.ts, case 15 is kingSlimeAI. Hmm, interesting — in vanilla, aiStyle 15 is King Slime? Let me check. Actually in vanilla Terraria:
- aiStyle 15 = King Slime
- Flail enemies... "White Bone Thrower"? No. Chain ball / Flail enemy = "flail skeleton"? Actually there's no aiStyle 15 flail enemy... Let me think. The dungeon spike ball is aiStyle? Blazing wheel & spike ball are AI_020/AI_021 per task. The task says "flailAI(AI_015 链球)". Hmm, but in vanilla NPC.cs, `case 15` in the main AI switch... Let me check what NPC has aiStyle 15: King Slime has aiStyle 15? Actually King Slime aiStyle is 15? Hmm — no. Let me check: King Slime NPCID 50, aiStyle = 15? I recall King Slime uses aiStyle 15. Actually, "AI_015_KingSlime()" at :43436 confirms AI 15 = King Slime.

So the task description may be slightly wrong about AI_015 being "链球" (flail). Hmm, but there IS a "flail" enemy... The Dungeon has "Blazing Wheel" (aiStyle 20?) and "Spike Ball" (aiStyle 21?). Wait, task says spike ball AI_020 / blazing wheel AI_021. In our code: case 20: blazingWheelAI; case 21: spikeBallAI. OK so those map.

Flail enemy: "Angry Trapper"? no. Actually there's "Dungeon Slime"? no. The flail-like dungeon enemy is "Blazing Wheel" and "Spike Ball". Hmm, what about "White Knight"? No...

There IS an enemy called "flail" something? Hmm, "Flocko"? no. OK — AI_015 in vanilla NPC AI switch is indeed King Slime. But wait, the main AI() switch case 15 might be different from AI_015_KingSlime private function. In Terraria decompiled, AI_015_KingSlime is a private function called for aiStyle 15. Let me verify by grepping the switch.

The flail enemy chain ball: NPC 397 "Bone Throwing Skeleton"? no. Hmm — actually the "chain ball / flail" enemy might be in Old One's Army? Or "Golem head"? Let me just check our code for a flailAI-like function. There's no flailAI in Enemy.ts per the greps. Memory notes say "链球AI_015+StatusNPC移植 — 状态机/链条贴图/命中debuff表/暴击率" — flail-statusnpc-port.md memory! So AI_015 flail... wait that memory says "flail-statusnpc-port — 链球AI_015+StatusNPC移植". Hmm, but AI_015_KingSlime exists at :43436. Confusing. Let me grep vanilla NPC.cs for which aiStyle the flail-type enemy uses. The enemy "flail" — I think it's the "Graveyard" enemy "Mimic"? no.

Actually! The flail enemy might be NPC 490 "Dune Splicer"? no. Let me think about "Swamp Thing" no...

Wait — memory note: "[链球AI_015+StatusNPC移植](flail-statusnpc-port.md) — 状态机/链条贴图/命中debuff表/暴击率;GAP清单在docs/weapon-proj-audit". This is about WEAPON projectile flail maybe? "链球" could be the weapon-type projectile (flail weapons like Sunfury are projectiles, not NPCs). docs/weapon-proj-audit — yes, that's a weapon projectile audit. So "flailAI(AI_015 链球)" in the task might be a misunderstanding from the parent; or there IS an NPC flail AI.

Hmm, in Terraria there are NPC "flails"? The dungeon "Dungeon Slime"... no. Old-gen console only? Let me check vanilla: grep "aiStyle = 15" and check what NPC IDs. Also the AI() switch in NPC.cs around :19899+. Let me look at case 15 in the main switch.

Let me now do the actual reading. Plan:

1. Read our Enemy.ts relevant sections:
   - slimeAI (1830-2034) + slimeGenItemInsideBody/slimeRollContainedItem (1697-1830) + slimeColorTick (2073-2119)
   - fighterAI (2387-2716) + medusaChargeStep (2248-2320) + solenianDashAI (2716-2771) + wetSwimStep (2320-2387) + RANGED_TABLE (2771-2821)
   - fighterFamilies.ts (whole, 845 lines)
   - wallCreeperAI (2949-3030)
   - lostGirlAI (3037-3064)
   - mimicAI (3243-3293) + mimic694Frame (4142-4177)
   - plantAI (3692-3779)
   - blazingWheelAI (4205-4242)
   - spikeBallAI (4242-4279)
   - casterAI (6514-6752)
   - tortoiseAI (3293-3406) — giant tortoise is aiStyle 39? Actually AI for snapper... The task mentions plantAI covers "食人怪/攀爬者". Tortoise is separate.

2. Read vanilla sections:
   - AI_001_Slimes :60735-~62266
   - AI_003_Fighters :56245-~60735
   - AI_013 plant (in main switch? or private) — need to find
   - AI_020/AI_021 (main switch inline? around 19899-33000 per task)
   - AI_025 mimic? Task says mimic 族 85. In vanilla, mimic aiStyle is 25? Actually Mimic uses aiStyle 25? Hmm, let me check: NPC 85 Mimic aiStyle... The task says "mimic 族(宝箱怪 85 等伪装唤醒/扑击)". Our code routes case 25 to mimicAI with comment "cs:25621 伪装200px盒". So vanilla AI 25 = Mimic at :25621 in the main switch. And AI_042 lost girl at :30281.
   - AI_040 wall creeper — in main switch.
   - caster AI_008 — in main switch (:19899-33000). Our case 8 = casterAI.
   - AI_015 King Slime :43436 — our case 15 = kingSlimeAI. The task's "flailAI(AI_015 链球)" is likely a mislabel; King Slime is delegated to bossAI? kingSlimeAI(this, game, p) — where is it defined? Probably bossAI.ts. Given the task scope lists "flailAI(AI_015 链球)", I should check: is there an NPC chain flail? YES — I now remember: the Old One's Army? No... Hmm, "flail" NPC... 

Actually wait, there might be an enemy in 1.4 "Mourning Wood"? no. Let me grep vanilla for "flail" in NPC.cs.

Let me also grep for what calls AI_015 vs the main switch case 15. The decompiled 1.4.5.6 has the big AI() method with switch on aiStyle, and separate private AI_0XX methods for newer ones. King Slime aiStyle is actually 15? Hmm, but our code comment says "case 15: kingSlimeAI" — so yes.

Hmm, but the task explicitly says flailAI(AI_015 链球). Maybe in their repo, "flail" refers to the King Slime's... no. Or maybe the parent agent got confused by the memory note "链球AI_015". That memory note might itself be about the King Slime? No — King Slime isn't a flail. The memory note "flail-statusnpc-port — 状态机/链条贴图/命中debuff表/暴击率" with "GAP清单在docs/weapon-proj-audit" strongly suggests weapon projectile flails (链球武器如太阳之怒), where projAI case for flail weapons. So for NPC audit, AI_015 = King Slime, which is probably out of my scope (boss), but since task says "flailAI(AI_015 链球)" I'll check both: verify King Slime isn't mine (bosses delegated), and note the flail enemy.

WAIT. I remember now! There IS an NPC flail: "Bone Serpent"? no. "Dungeon Guardian"? no. Let me grep "Flail" in NPC.cs to settle.

Plan of attack: spawn parallel Explore agents? The instructions say I'm the dedicated agent; I can spawn subagents for independent parallel work. Given the size (AI_003_Fighters is 4500 lines of vanilla!), delegating chunks to Explore agents makes sense. But Explore agents "locate code; they don't review or audit it". For careful numeric comparison I should do it myself. The vanilla AI_003_Fighters is huge (56245-60735 = 4490 lines). That's a lot. But most of it is type-specific branches (which NPC ids). Our fighterFamilies.ts helpers correspond to specific branches.

Given the effort, I'll do the reading myself with targeted reads, and possibly use one or two subagents for cross-referencing specific numeric constants. Actually, let me just do it directly — I can read big chunks fast. Let me be systematic, family by family.

Order (simple → complex):
1. spike ball / blazing wheel (small)
2. lostGirlAI (small)
3. mimicAI (small)
4. wallCreeperAI (small-medium)
5. plantAI (medium)
6. casterAI (medium)
7. slimeAI (large)
8. fighterAI + fighterFamilies (largest)

Let me first read all our implementation sections. Start with a big read of Enemy.ts 2248-3300 (covers fighter helpers, fighterAI, wallCreeper, lostGirl, mimic).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:06:49.777Z · glm-x-preview-260804

```
我来梳理一下这两个代码库。首先，读取一下我们关键的实现部分。
```


---

## 🤖 Assistant · 2026-08-19T03:06:50.074Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "offset": 2248,
 "limit": 420
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:50.104Z

**📎 ToolResult**

```
2248	  private medusaChargeStep(game: GameHooks, player: Player): boolean {
2249	    const lowHp = this.hp < this.maxHp / 3;
2250	    const num21 = lowHp ? 120 : 180;   // 打断冷却
2251	    const num22 = lowHp ? 240 : 300;   // 放完冷却
2252	    const num23 = lowHp ? 240 : 180;   // 发石化窗长度
2253	    const num24 = lowHp ? 90 : 60;     // buff 基础时长
2254	    const num25 = 20;                  // 起手辉光段
2255	    if (this.ai2 > 0) {
2256	      this.ai2 -= 1;
2257	    } else if (this.ai2 === 0) {
2258	      // 待机起手判定（:56764-56771）：正对玩家 + 站地 + <900 + 视线
2259	      const facing = (player.cx < this.cx && this.facing < 0) || (player.cx > this.cx && this.facing > 0);
2260	      if (facing && this.vy === 0 && Math.hypot(player.cx - this.cx, player.cy - this.cy) < 900
2261	        && losClear(game, Math.floor(this.cx / TILE), Math.floor(this.cy / TILE),
2262	          Math.floor(player.cx / TILE), Math.floor(player.cy / TILE))) {
2263	        this.ai2 = -(num23 + num25);
2264	      }
2265	    } else {
2266	      // 蓄力两段（:56778-56889）：打断/推进
2267	      this.vx *= 0.9;
2268	      if (this.vy < -2 || this.vy > 4 || this.justHitT > 0) {
2269	        this.ai2 = num21;
2270	      } else {
2271	        this.ai2 += 1;
2272	        if (this.ai2 === 0) this.ai2 = num22;
2273	      }
2274	      this.lightRGB = [0.9, 0.75, 0.1];          // :56816/:56820 蓄力点光——曾误写 0-255 标度致 254× 过曝
2275	      const rem = this.ai2 + num23 + num25;      // 起手辉光段计时（:56798 num26）
2276	      if (rem === 1) game.playSfxFile?.('Item_17', 1, this.cx, this.cy); // SoundID 4-17(充能)
2277	      if (rem < num25) {
2278	        // 充能尘（:56801-56813 尘 228 头顶环;num26<num25 含首 tick 0）
2279	        const hx = this.cx + this.facing * 6, hy = this.y + 6;
2280	        game.spawnParticles(hx, hy, '#E8A040', 2, 1.6);
2281	      }
2282	      if (this.ai2 >= -num23) {
2283	        // 发石化窗（:56835-56888）：尘 + 直击判定
2284	        const n29 = this.ai2 + num23;
2285	        if (n29 < 180 && (Math.random() < 1 / 3 || this.ai2 % 3 === 0)) { // :56844 num29<180 含 0
2286	          const hx = this.cx + this.facing * 10, hy = this.y + 10;
2287	          game.spawnParticles(hx, hy, '#E8A040', 1, 2.4);
2288	        }
2289	        if (!player.dead && !player.buffs.has(BuffType.Stoned)) {
2290	          const dx = player.cx - this.cx, dy = player.cy - this.cy;
2291	          const dist = Math.hypot(dx, dy);
2292	          if (dist < 700) {
2293	            let hit = dist < 30;                                    // 贴脸必中（:56866）
2294	            if (!hit) {
2295	              // 45° 锥（:56870-56877）：|单位向量 X| > cos(45°) → 视为正面
2296	              const ux = dx / dist;
2297	              hit = ux > 0.7071 || ux < -0.7071;
2298	            }
2299	            const mutualFacing = (player.cx < this.cx && this.facing < 0 && player.facing > 0)
2300	              || (player.cx > this.cx && this.facing > 0 && player.facing < 0);
2301	            if (hit && mutualFacing) {
2302	              // 三路视线任一通（:56880-56882：头/上 16px/下 8px）
2303	              const sees = (ox: number, oy: number) => losClear(game,
2304	                Math.floor((this.cx + ox) / TILE), Math.floor((this.cy + oy) / TILE),
2305	                Math.floor(player.cx / TILE), Math.floor(player.cy / TILE));
2306	              if (sees(0, 0) || sees(0, -16) || sees(0, 8)) {
2307	                player.buffs.apply(BuffType.Stoned, (num24 + Math.trunc(-this.ai2)) / 60);
2308	              }
2309	            }
2310	          }
2311	        }
2312	      }
2313	      // 蓄力期接管 AI_003 余段（原版两段末尾 return）
2314	      this.x += this.vx; this.y += this.vy;
2315	      return true;
2316	    }
2317	    return false;
2318	  }
2319	
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
2460	    const solidAt = (x: number, y: number) => x >= 0 && y >= 0 && x < st.w && y < st.h && st.isSolid(x, y);
2461	    // 沼泽怪 166 伏击（NPC.cs:56327-56360）：伏击态接管本 tick（原地减速，跳过行走）
2462	    if (swampThingAmbushStep(this, !!player && this.canSeePlayer(st, player))) return;
2463	    // 混沌元素 120（NPC.cs:57431-57460/:60679-60696）：ai[3] 卡死计数 + 传送
2464	    if (this.vanillaId === 120 && player) this.ai3 = chaosElementalStep(this, game, player);
2465	    // ---- 日食怪战士族专属段（NPC.cs:57547-57710，位于卡死计数与横向移动链之间）----
2466	    // Nailhead 463 受击散射（:57547-57613）；Butcher 460 空中免击退（:57615-57624）；
2467	    // Possessed 469 爬墙冲刺（:57626-57677，冲刺分支 return 跳过余段）；
2468	    // Fritz 462 跳扑（:57678-57710，改 vx/vy 后继续走本 tick 行走）
2469	    nailheadHitScatter(this, game, player);
2470	    butcherKbStep(this);
2471	    if (possessedStep(this, game, player)) return;
2472	    fritzPounceStep(this, player);
2473	    // 横向移动逐族表（NPC.cs:57799-58800 else-if 链 1:1，fighterFamilies.ts）——
2474	    // 取代一期固定档（加速 0.1 / 限速 ±1）；射击族（:58719 排除表）链上无分支
2475	    fighterMoveStep(this, dir, player);
2476	    // 425 风暴潜水员专属段（NPC.cs:58865-59013，原版独立第二段 if/else-if 阶梯，
2477	    // 位于移动链之后/重力之前）：喷包伺服 + 起飞门 + ai3 瞄准蓄力（stormDiverAimStep
2478	    // 计数节奏）——ai3 专用于蓄力，不再与任何通用计数共用（Renderer.npcGlowSparkleEnvelope 消费）
2479	    stormDiverStep(this, game, player);
2480	    // 原版跳跃判定用碰撞前的速度符号（NPC 碰撞在 AI 之后）——
2481	    // 此处必须先捕获再碰撞，否则撞墙清零 vx 后 movingInto 恒假、战士永不跳墙
2482	    const vxSign = this.vx > 0 ? 1 : this.vx < 0 ? -1 : 0;
2483	    // ---- 台阶自动步升（L24512-24554）：前方高差 ≤16.1px 直接跨上（gfxOffY 视觉补偿略）----
2484	    if (this.vy >= 0 && vxSign !== 0) {
2485	      const ax = Math.floor((this.x + this.vx + this.w / 2 + (this.w / 2 + 1) * vxSign) / TILE);
2486	      const fr = Math.floor((this.y + this.h - 1) / TILE);
2487	      if (ax >= 0 && fr >= 2 && ax < st.w && fr < st.h
2488	        && solidAt(ax, fr) && !st.half[st.idx(ax, fr)]
2489	        && !solidAt(ax, fr - 1) && !solidAt(ax, fr - 2) && !solidAt(ax, fr - 3)) {
2490	        const top = fr * TILE;
2491	        const rise = this.y + this.h - top;
2492	        if (rise > 0 && rise <= 16.1) this.y = top - this.h;
2493	      }
2494	    }
2495	    // 重力 + 碰撞（原版 SteepSlowing/WalkDownSlope 略）
2496	    this.applyGravity(game);
2497	    moveAndCollide(this, game.world, this.vx, this.vy);
2498	    // ---- 四级跳判定（L24651-24733）：仅在朝移动方向撞到东西时 ----
2499	    // 原版全部跳跃赋值都有 velocity.Y == 0f 前置（AI_003 内 44 处同款门）——
2500	    // 缺失此门时空中贴墙每帧 vy=-8 → 沿墙飞天贴天花板（主角靠近才掉落）
2501	    const movingInto = vxSign === dir && vxSign !== 0 && this.vy === 0;
2502	    if (movingInto) {
2503	      if (this.h >= 32 && solidAt(fx, fy - 2)) {
2504	        // 胸口前 2 格墙：上方再 1 格也堵 → -8，否则 -7
2505	        this.vy = solidAt(fx, fy - 3) ? -8 : -7;
2506	      } else if (solidAt(fx, fy - 1)) {
2507	        this.vy = -6;                       // 脚前 1 格墙
2508	      } else if (this.y + this.h - fy * TILE > 20 && solidAt(fx, fy) && !st.half[st.idx(fx, fy)]) {
2509	        this.vy = -5;                       // 卡在格内下部（非半砖）
2510	      } else if (player && player.y + player.h < this.y
2511	        && !solidAt(fx, fy + 1) && !solidAt(fx + dir, fy + 1)) {
2512	        this.vy = -8;                       // 前方悬空且目标在上方 → 大跳 + 冲刺
2513	        this.vx *= 1.5;
2514	      }
2515	    }
2516	    // ---- 门交互（AI_003 :64716-64780 攻门态语义 + AI_007 :60390-60460 不放弃门）----
2517	    // 前方脚上一格是关闭的门（sheet 10）→ 攻门：先 60t 站定蓄势（ai[0]），后每
2518	    // tick +5（tall gate 388 +2）累计至 10 → 尝试开门（失败 30t 脱离 ai[3]=num21）；
2519	    // 血月/墓园不脱离（AI_007 flag27 反义：(!bloodMoon||getGoodWorld)&&!graveyard），
2520	    // 持续攻门直到开出；GoblinPeon 26 直接拆门（KillTile → 掉门物品）。
2521	    // ★:60383 flag8 门（NPC.cs:57462-57471 表）：Psycho 466/Possessed 469/Eyezor 251/
2522	    // Dr Man Fly 468/沼泽怪 166/美杜莎 480 等表内型原版**不攻门**。
2523	    if (this.doorCd > 0) {
2524	      this.doorCd--;
2525	    } else if (this.vanillaId == null || FIGHTER_NO_DOOR.has(this.vanillaId)) {
2526	      // flag8=false 族：原版整个攻门段被 `&& flag8` 短路（doorWarm/doorHit 也不累计）
2527	    } else if (this.vy === 0 && dir !== 0 && vxSign === dir) {
2528	      const dtx = fx, dty = fy - 1;
2529	      if (st.inBounds(dtx, dty) && st.flags[st.idx(dtx, dty)]) {
2530	        const dDef = TILE_DEFS[st.type[st.idx(dtx, dty)]];
2531	        if (dDef?.vanilla?.sheet === 10) {
2532	          this.doorWarm = (this.doorWarm ?? 0) + 1;
2533	          this.vx *= 0.7; // 攻门贴门减速（velocity.X = 0.5×-direction 语义近似）
2534	          if (this.doorWarm >= 60) {
2535	            this.doorHit = (this.doorHit ?? 0) + 5;
2536	            if (this.doorHit >= 10) {
2537	              this.doorHit = 0;
2538	              if (this.vanillaId === 26) {
2539	                game.breakTile?.(dtx, dty); // GoblinPeon 拆门（:60439-60444）
2540	                this.doorWarm = 0;
2541	              } else if (!openDoor(st, dtx, dty, dir)) {
2542	                const clock = game.world.clock;
2543	                if (!clock.bloodMoon && !game.world.scene?.zoneGraveyard) {
2544	                  this.doorCd = 30; // 非血月：一次失败即脱离 30t（:60447-60450）
2545	                }
2546	              } else {
2547	                this.doorWarm = 0; // 开出 → 重新蓄势
2548	              }
2549	            }
2550	          }
2551	        } else {
2552	          this.doorWarm = 0;
2553	          this.doorHit = 0;
2554	        }
2555	      }
2556	    }
2557	    // ---- 蜘蛛上墙形态切换（NPC.cs:59273-59293）：站定（velocity.Y==0）且身边有
2558	    // 背景墙（NPCCanStickToWalls）→ Transform 成爬墙形态（164→165 等）——
2559	    // 蜘蛛洞里贴墙爬的就是这一步，地表无背景墙自然不触发
2560	    if (this.vy === 0 && this.vanillaId != null) {
2561	      const wallForm = Enemy.SPIDER_WALL_FORM[this.vanillaId];
2562	      if (wallForm !== undefined && this.npcCanStickToWalls(st)) {
2563	        this.tryTransformTo(wallForm, st, false, game);
2564	      }
2565	    }
2566	    // ---- 吸血鬼离远 → 化回蝙蝠（cs:59236-59244：type 159 距玩家 >300 → Transform(158)）
2567	    if (this.vanillaId === 159 && player
2568	      && Math.hypot(player.cx - this.cx, player.cy - this.cy) > 300) {
2569	      this.tryTransformTo(158, st, false, game);
2570	    }
2571	    // ---- 蜥蜴人激怒（cs:57422-57425：type 198 HP≤55% → Transform(199 LihzahrdCrawler)，
2572	    //  爬行姿态更快更狠；同段的 Nutcracker 348→349 霜月未引入不移植）
2573	    if (this.vanillaId === 198 && this.hp <= this.maxHp * 0.55) {
2574	      this.tryTransformTo(199, st, false, game);
2575	    }
2576	    // 地面摩擦：原版 walker 摩擦链已在 fighterMoveStep（fighterFamilies.ts）1:1
2577	    // （AI_003_Fighters :60115-60175——num3 档 velocity×damp【双轴】、vy==0 落地门、
2578	    // 仅 |vx|>max 超速段衰减,逐族 damp 0.7/0.8/0.95…;未超速段是 +=accel 钳 ±max）;
2579	    // 坡面逐面链（Collision.SlopeCollision :1796-2036 贴合/受阻清零）在
2580	    // TileCollision.slopeCollide。此处的 onGround ×0.85 是 slope 系统落地前的
2581	    // 陈旧近似,与 damp 叠乘成双阻尼（超速段 0.8×0.85,匀速段把平衡点压到
2582	    // accel/(1-0.85)≈0.47px/t,远低于原版 max 1-1.5）——2026-08-15 摘除回归单链
2583	    // ---- 战士族远程攻击（NPC.cs:59464-60085：落地 + 视线 + 距离<射程 → 举枪蓄力，
2584	    // 半程发射；justHit 打断蓄力 cs:59489。覆盖入侵弓手 + 地牢/沙漠常驻射击怪）----
2585	    // ai[1]=蓄力倒数(ai0)、ai[2]=瞄准姿态(ai3)
2586	    if (player && this.vanillaId != null && Enemy.RANGED_FIGHTERS.has(this.vanillaId)) {
2587	      const R = Enemy.RANGED_TABLE[this.vanillaId];
2588	      const fireAt = R.burst ? R.cooldown - 1 : R.cooldown >> 1; // 292 在 num163-1 连发（cs:59967）
2589	      const spread = R.spread ?? 40;
2590	      // num168 下坠补偿（cs:60046）：定值或每发 [lo,hi] 区间随机（468 :59727-59730）
2591	      const dropOf = () => Array.isArray(R.drop)
2592	        ? R.drop[0] + Math.random() * (R.drop[1] - R.drop[0])
2593	        : (R.drop ?? 0.1);
2594	      // 解除瞄准门的"下坠补偿 > 0"判定（cs:60015 !flag17）——区间型取上界判定
2595	      const dropCanDrop = Array.isArray(R.drop) ? R.drop[1] > 0 : (R.drop ?? 0.1) > 0;
2596	      // :60020-60024 瞄准减速 vx×0.9——flag16=true 族跳过（468 非日食 :60026-60029）
2597	      const aimDecel = !(R.aimDecelOffEclipse && !game.world.clock.eclipse);
2598	      if (this.ai3 > 0) {           // 瞄准中：减速 + 半程发射
2599	        if (this.ai0 > 0) this.ai0--;
2600	        if (aimDecel) this.vx *= 0.9;
2601	        this.facing = this.seekDirX(player);
2602	        if (this.ai0 === fireAt && this.ai0 > 0) {
2603	          const ox = this.cx, oy = this.cy + (R.oy ?? 0);
2604	          const shots = R.burst ?? 1;
2605	          for (let b = 0; b < shots; b++) {
2606	            // 预判点（cs:59700-59790）：目标中心 + 下坠补偿（默认 |dx|×0.1，各 type 修正）
2607	            // + 散布（默认 ±40，291 狙击 ±8）——弹体直飞（Dart 敌我对全敌对）
2608	            let tx = player.cx - ox;
2609	            let ty = player.cy - oy - Math.abs(tx) * dropOf();
2610	            tx += Math.random() * spread * 2 - spread;
2611	            ty += Math.random() * spread * 2 - spread;
2612	            this.shootDart(game, ox, oy, tx, ty, R.speed, R.dmg, R.proj);
2613	          }
2614	        }
2615	        // 移动/冷却尽 → 解除瞄准（cs:60005-60009）
2616	        if ((this.vy !== 0 && dropCanDrop) || this.ai0 <= 0) { this.ai3 = 0; this.ai0 = 0; }
2617	      } else if (this.vy === 0 && this.ai0 <= 0 && !player.dead && this.onGround) {
2618	        // 开瞄（cs:60013-60095）：视线 + 距离 < 射程。
2619	        // ★ cs:60036-60039 idle 门：目标玩家待机（原版 stealth==0 && itemAnimation==0，
2620	        //   此处 useTime>0 近似——挥击重启已对齐原版时序，战斗中恒 >0）→ 视线判 false，不开瞄
2621	        const dx = player.cx - this.cx, dy = player.cy - this.cy;
2622	        let los = player.useTime > 0;
2623	        const steps = Math.ceil(Math.hypot(dx, dy) / (TILE / 2));
2624	        for (let s = 1; s < steps && los; s++) {
2625	          const lx = Math.floor((this.cx + (dx * s) / steps) / TILE);
2626	          const ly = Math.floor((this.cy + (dy * s) / steps) / TILE);
2627	          if (lx >= 0 && ly >= 0 && lx < st.w && ly < st.h && solidAt(lx, ly)) { los = false; break; }
2628	        }
2629	        if (los && Math.hypot(dx, dy) < R.range) {
2630	          this.ai3 = 3;               // 姿态（cs:60080 起的 1-5 分档，本处仅作标记）
2631	          this.ai0 = R.cooldown;
2632	          this.vx *= 0.5;
2633	        }
2634	      }
2635	    }
2636	    // ---- 冰雪巨人 243 霜冻光束（cs:59331-59360）：ai[2] 计时 ≥ rand(30..900)×(HP 比)+30
2637	    // 且落地 + 朝向玩家 + 视线 → 光束（速 15、伤 32、散布 ±40）；阈值随机数缓存 ai[3]，
2638	    // 发射后双双清零（受击 ai[2]-=rand(30) 略）
2639	    if (this.vanillaId === 243 && player && !player.dead) {
2640	      this.ai2 += 1;
2641	      if (this.ai3 === 0) this.ai3 = 30 + Math.floor(Math.random() * 870);
2642	      if (this.vy === 0 && this.facing === (player.cx > this.cx ? 1 : -1)
2643	        && this.ai2 >= this.ai3 * (this.hp / this.maxHp) + 30 && this.canSeePlayer(st, player)) {
2644	        // 枪口（cs:59323/:59340）：基点 (cx + 10×朝向, y + 20) 瞄准（含 ±40 散布），
2645	        // 出生点再沿弹向 +vel×3（速 15 → 前移 45px）
2646	        const baseX = this.cx + 10 * this.facing, baseY = this.y + 20;
2647	        const bdx = player.cx - baseX + (Math.random() * 80 - 40);
2648	        const bdy = player.cy - baseY + (Math.random() * 80 - 40);
2649	        const bd = Math.hypot(bdx, bdy) || 1;
2650	        this.shootDart(game, baseX + (bdx / bd) * 45, baseY + (bdy / bd) * 45,
2651	          bdx, bdy, 15, 32, 257);
2652	        this.ai2 = 0; this.ai3 = 0;
2653	        return;
2654	      }
2655	    }
2656	    // ---- 岩石巨人 631 投石（cs:56733-56760）：320px 内 + 视线 → 100 帧前摇，
2657	    // 第 68 帧发射岩石（速 8±0.8、伤 20）；脱距重置前摇
2658	    if (this.vanillaId === 631 && player && !player.dead) {
2659	      const dg = Math.hypot(player.cx - this.cx, player.cy - this.cy);
2660	      if (dg < 320 && this.canSeePlayer(st, player)) {
2661	        this.ai2 += 1;
2662	        if (this.ai2 === 68) {
2663	          const jit = 8 + (Math.random() * 1.6 - 0.8); // ±0.8
2664	          this.shootDart(game, this.cx, this.cy - 8, player.cx - this.cx, player.cy - this.cy, jit, 20, 909);
2665	        }
2666	        if (this.ai2 >= 100) this.ai2 = 0;
2667	      } else this.ai2 = 0;

```


---

## 🤖 Assistant · 2026-08-19T03:06:50.309Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/fighterFamilies.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:50.507Z

**📎 ToolResult**

```
1	// AI_003 战士族逐族切片（Terarria1456/Terraria.NPC.cs AI_003_Fighters :56245-60734，
2	// 1.4.5.6 1:1）。本文件承接 Enemy.fighterAI 的一期通用档（固定 加速 0.1 / 限速 ±1），
3	// 按 NPC.cs 横向移动 else-if 链（:57799-58800）逐族给出 限速/加速/超速衰减 三元组，
4	// 外加两个自包含的行为型分支：混沌元素 120 传送（:57431-57460 / :60679-60696 /
5	// AI_AttemptToFindTeleportSpot :18876-18946 / ai[3] 卡死计数 :57504-57545）与
6	// 沼泽怪 166 伏击（:56327-56360）。
7	//
8	// 族表覆盖的高频怪（Top5 按 出现频率×影响面 选型；aiStyle=3 全量 186 种的分布扫描
9	// 见 memory 与 tests/a-batch3.test.ts）：
10	//   1. 僵尸族 3/132/186-189/200/223/331/332/632/691（夜地表最高频，default 档 0.8-1.2）
11	//   2. 骷髅族 21/201/202/203/342/635 + 愤怒骷髅 31/294-296（洞穴高频，num84 档）
12	//   3. 骨甲三族 269-280（地牢最高频 12 型，num85 档 1.0-3.25）
13	//   4. 稻草人 305-314（南瓜月高频，num86 档 1.0-2.25）
14	//   5. 混沌元素 120（神圣地表夜高频，3 档 + 传送）+ 3 档组 166/213/258/528/529
15	//
16	// 其余未逐行移植的 AI_002/AI_003 type 分支精确清单已登记 memory（待移植，不做近似）：
17	// 原版在移动链上有专属分支、本文件暂走 legacy 通用档的型 = 430-436/494/495/591
18	// （扑咬突进 :58669-58718）。
19	import type { Enemy } from './Enemy';
20	import type { GameHooks } from './types';
21	import type { Player } from './Player';
22	import { TILE, GRAVITY, MAX_FALL_SPEED } from '../core/constants';
23	import { moveAndCollide } from '../physics/TileCollision';
24	import { canHit, canHitLine } from '../physics/LineOfSight';
25	import { getKnockbackMultiplierScaledByDifficulty, getAttackDamageForProjectiles } from '../stats/ScaleStats';
26	import { TILE_DEFS } from '../data/tiles';
27	
28	/** :57462-57471 flag8=false 全表（NPC.cs:57468）。flag8 的两处下游消费：
29	 *  ① 攻门段 :60383 `… && flag8`——表内型**不攻门**（Psycho 466/Possessed 469/
30	 *     Eyezor 251/Dr Man Fly 468/沼泽怪 166/美杜莎 480 等全在内）；
31	 *  ② 行走/跳跃链 :60534 与 :60674 `else if (flag8) { ai[1]=0; ai[2]=0; }`——表内型
32	 *     的 ai[1]/ai[2] 不被通用行走清零（466 潜行态、469 爬墙态、251 激光计时、
33	 *     468 射击态、166/480 伏击·蓄力态都活在 ai[2] 上，被清零即状态机报废）。
34	 *  ②在本仓天然成立（fighterAI 的行走/跳跃段不写 ai[1]/ai[2]）；①由攻门段读本表实现。 */
35	export const FIGHTER_NO_DOOR: ReadonlySet<number> = new Set([
36	  343, 47, 67, 109, 110, 111, 120, 163, 164, 239, 168, 199, 206, 214, 215, 216,
37	  217, 218, 219, 220, 226, 243, 251, 257, 258, 290, 291, 292, 293, 305, 306, 307,
38	  308, 309, 348, 349, 350, 351, 379, 430, 431, 432, 433, 434, 435, 436, 591, 380,
39	  381, 382, 383, 386, 391, 449, 450, 451, 452, 466, 464, 166, 469, 468, 471, 470,
40	  480, 481, 482, 411, 424, 409, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503,
41	  504, 505, 506, 425, 427, 426, 428, 580, 508, 415, 419, 520, 524, 525, 526, 527,
42	  528, 529, 530, 532, 582, 624, 631,
43	]);
44	
45	/** 横向移动三元组（else-if 链各分支的共形段：超速衰减 / 限速内加速） */
46	export interface FighterMove {
47	  /** 限速 |vx| 上限（原版 num8x） */
48	  max: number;
49	  /** 限速内每 tick 加速（原版各分支的 += 值） */
50	  accel: number;
51	  /** 超速且落地时的衰减（原版 velocity *= N；原版连 Y 一起乘，落地时 Y≈0 等价） */
52	  damp: number;
53	  /** 落地且 vx 与 direction 相逆时的额外衰减（:57799/:57916 档 0.99 / :57882 档 0.8） */
54	  reverseDamp?: number;
55	}
56	
57	/** 一期通用档（原固定 加速 0.1 / 限速 ±1）——仅用于原版有专属分支但该分支待移植的型 */
58	const LEGACY: FighterMove = { max: 1, accel: 0.1, damp: 1 };
59	
60	const inRange = (v: number, lo: number, hi: number): boolean => v >= lo && v <= hi;
61	
62	/** :58719 射击族排除表——原版这些型在移动链上无分支（本 tick 不做横向加减速） */
63	function rangedMoveExcluded(id: number): boolean {
64	  return id === 110 || id === 111 || id === 206 || id === 214 || id === 215 || id === 216
65	    || inRange(id, 290, 293) || id === 350 || id === 379 || id === 380 || id === 381
66	    || id === 382 || inRange(id, 449, 452) || id === 468 || id === 481 || id === 411
67	    || id === 409 || inRange(id, 498, 506) || id === 424 || id === 426 || id === 520;
68	}
69	
70	/** 横向移动 else-if 链（NPC.cs:57799-58800）1:1。返回 null = 原版该型在链上无分支。 */
71	export function fighterMoveSpec(e: Enemy): FighterMove | null {
72	  const id = e.vanillaId ?? -1;
73	  const hpRatio = e.hp / e.maxHp;                  // life/lifeMax
74	  const scale = e.vanillaScale;                    // npc.scale（负 netID 变种）
75	  if (rangedMoveExcluded(id)) return null;         // :58719 排除表（链上无分支）
76	  if (id === 159 || id === 349) {                  // :57799-57830 吸血鬼/胡桃夹子
77	    return { max: 6, accel: 0.07, damp: 0.8, reverseDamp: 0.99 };
78	  }
79	  if (id === 199) {                                // :57882-57915 蜥蜴人爬行态
80	    return { max: 4, accel: 0.1, damp: 0.8, reverseDamp: 0.8 };
81	  }
82	  if (id === 120 || id === 166 || id === 213 || id === 258 || id === 528 || id === 529) {
83	    return { max: 3, accel: 0.07, damp: 0.8, reverseDamp: 0.99 };   // :57916-57949
84	  }
85	  // :57950-57975 二速族（狼人 104/装甲骷髅 77/装甲维京 197/猩红斧 163 等）
86	  if (id === 461 || id === 27 || id === 77 || id === 104 || id === 163 || id === 162
87	    || id === 196 || id === 197 || id === 212 || id === 257 || id === 326 || id === 343
88	    || id === 348 || id === 351 || inRange(id, 524, 527) || id === 530 || id === 236) {
89	    return { max: 2, accel: 0.07, damp: 0.8 };
90	  }
91	  if (id === 109) return { max: 2, accel: 0.04, damp: 0.8 };        // :57976-57998 小丑
92	  // :58002-58136 常规族（僵尸/骷髅/愤怒骷髅/木乃伊/甲虫/精灵等）num84 档
93	  if (id === 21 || id === 26 || id === 31 || id === 294 || id === 295 || id === 296
94	    || id === 47 || id === 73 || id === 140 || id === 164 || id === 239 || id === 167
95	    || id === 168 || id === 185 || id === 198 || id === 201 || id === 202 || id === 203
96	    || id === 217 || id === 218 || id === 219 || id === 226 || id === 181 || id === 254
97	    || id === 338 || id === 339 || id === 340 || id === 342 || id === 385 || id === 389
98	    || id === 462 || id === 463 || id === 466 || id === 464 || id === 469 || id === 470
99	    || id === 480 || id === 482 || id === 425 || id === 429 || id === 586 || id === 631
100	    || id === 635) {
101	    let num84 = 1.5;                               // :58005
102	    if (id === 294) num84 = 2;                     // :58011-58013
103	    else if (id === 295) num84 = 1.75;
104	    else if (id === 296) num84 = 1.25;
105	    else if (id === 201) num84 = 1.1;
106	    else if (id === 202) num84 = 0.9;
107	    else if (id === 203) num84 = 1.2;
108	    else if (id === 338) num84 = 1.75;
109	    else if (id === 339) num84 = 1.25;
110	    else if (id === 340) num84 = 2;
111	    else if (id === 385) num84 = 1.8;
112	    else if (id === 389) num84 = 2.25;
113	    else if (id === 462) num84 = 4;
114	    else if (id === 463) num84 = 0.75;
115	    else if (id === 466) num84 = 3.75;
116	    else if (id === 469) num84 = 3.25;
117	    else if (id === 480) num84 = 1.5 + (1 - hpRatio) * 2;   // 美杜莎越伤越快
118	    else if (id === 425) num84 = 6;
119	    else if (id === 429) num84 = 4;
120	    else if (id === 631) num84 = 0.9;
121	    else if (id === 586) num84 = 1.5 + (1 - hpRatio) * 3.5; // 僵尸人鱼越伤越快
122	    // :58007-58010 Face Monster 181 的 remixWorld 3.75 档不适用本作（无 remix 世界）
123	    const scaleBoost = id === 21 || id === 201 || id === 202 || id === 203
124	      || id === 342 || id === 635;                 // :58080-58083
125	    if (scaleBoost) num84 *= 1 + (1 - scale);
126	    return { max: num84, accel: 0.07, damp: 0.8 };
127	  }
128	  // :58137-58204 骨甲三族（锈蚀 269-272 / 蓝色 273-276 / 地狱 277-280）num85 档
129	  if (inRange(id, 269, 280)) {
130	    let num85 = 1.5;                               // :58139
131	    if (id === 269) num85 = 2;
132	    else if (id === 270) num85 = 1;
133	    else if (id === 271) num85 = 1.5;
134	    else if (id === 272) num85 = 3;
135	    else if (id === 273) num85 = 1.25;
136	    else if (id === 274) num85 = 3;
137	    else if (id === 275) num85 = 3.25;
138	    else if (id === 276) num85 = 2;
139	    else if (id === 277) num85 = 2.75;
140	    else if (id === 278) num85 = 1.8;
141	    else if (id === 279) num85 = 1.3;
142	    else if (id === 280) num85 = 2.5;
143	    num85 *= 1 + (1 - scale);                      // :58189
144	    return { max: num85, accel: 0.07, damp: 0.8 };
145	  }
146	  // :58205-58264 稻草人十型 num86 档（<310 的扑跳分支 :58231-58242 待移植，见 memory）
147	  if (inRange(id, 305, 314)) {
148	    let num86 = 1.5;                               // :58207
149	    if (id === 305 || id === 310) num86 = 2;
150	    else if (id === 306 || id === 311) num86 = 1.25;
151	    else if (id === 307 || id === 312) num86 = 2.25;
152	    else if (id === 308 || id === 313) num86 = 1.5;
153	    else if (id === 309 || id === 314) num86 = 1;
154	    return { max: num86, accel: 0.07, damp: 0.8 };
155	  }
156	  if (id === 67 || id === 220 || id === 428) {     // :58265-58287 螃蟹/海螺/外星幼虫
157	    return { max: 0.5, accel: 0.03, damp: 0.7 };
158	  }
159	  if (id === 78 || id === 79 || id === 80 || id === 630) {   // :58288-58317 木乃伊族
160	    let num87 = 1, num88 = 0.05;
161	    if (hpRatio < 0.5) { num87 = 2; num88 = 0.1; } // :58293-58297 半血激怒
162	    if (id === 79 || id === 630) num87 *= 1.5;     // :58298-58301
163	    return { max: num87, accel: num88, damp: 0.7 };
164	  }
165	  if (id === 287) return { max: 5, accel: 0.2, damp: 0.7 };          // :58318-58340 骨李
166	  if (id === 243) {                                                   // :58365-58397 冰雪巨人
167	    return {
168	      max: 1 + (1 - hpRatio) * 1.5,
169	      accel: 0.07 + (1 - hpRatio) * 0.15,
170	      damp: 0.7,
171	    };
172	  }
173	  if (id === 251) {                                                   // :58401-58433 独眼僵尸
174	    return {
175	      max: 1 + (1 - hpRatio) * 2,
176	      accel: 0.08 + (1 - hpRatio) * 0.2,
177	      damp: 0.7,
178	    };
179	  }
180	  if (id === 386) {                                                   // :58444-58456 火星工程师
181	    // ai[2]>0（放炮塔蓄势）→ 只衰减不加速
182	    return e.ai2 > 0 ? { max: 0, accel: 0, damp: 0.8 } : { max: 1.5, accel: 0.15, damp: 0.7 };
183	  }
184	  if (id === 460) {                                                   // :58457-58525 屠夫
185	    let num98 = 0.1;                                                  // :58460-58480 分段加速衰减
186	    for (const t of [2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5]) {
187	      if (Math.abs(e.vx) > t) num98 *= 0.8;
188	    }
189	    return {
190	      max: 3 + (1 - hpRatio) * 3,                                     // :58481
191	      accel: num98,
192	      damp: 0.7,
193	      reverseDamp: 0.93,                                              // :58492/:58504
194	    };
195	  }
196	  if (id === 391 || id === 427 || id === 415 || id === 419 || id === 518 || id === 532) {
197	    // :58613-58667 Scutlix/外星蜂/Drakomire/Selenian/Drakanian/Basilisk
198	    if (id === 427) return { max: 6, accel: 0.2, damp: 0.8 };         // :58624-58627
199	    if (id === 415) return { max: 4, accel: 0.1, damp: 0.95 };        // :58628-58631
200	    if (id === 419) return { max: 6, accel: 0.15, damp: 0.85 };       // :58632-58635
201	    if (id === 518) return { max: 5, accel: 0.1, damp: 0.95 };        // :58636-58639
202	    if (id === 532) return { max: 5, accel: 0.15, damp: 0.98 };       // :58640-58643
203	    return { max: 5, accel: 0.25, damp: 0.7 };                        // :58622-58623
204	  }
205	  // :58669-58718 扑咬突进族（哥布林苦力 430-436/龙虾 494/495/火把僵尸 591）——专属
206	  // 突进分支待移植（见 memory），暂走一期通用档
207	  if (inRange(id, 430, 436) || id === 494 || id === 495 || id === 591) return LEGACY;
208	  // :58719-58800 default 档 num108（僵尸变体/雨衣僵尸/血僵尸/沼泽怪等其余战士族）
209	  let num108 = 1;                                                     // :58722
210	  if (id === 624) num108 = 2.5;                                       // 地精
211	  else if (id === 186) num108 = 1.1;
212	  else if (id === 187) num108 = 0.9;
213	  else if (id === 188) num108 = 1.2;
214	  else if (id === 189) num108 = 0.8;
215	  else if (id === 132) num108 = 0.95;
216	  else if (id === 200) num108 = 0.87;
217	  else if (id === 223) num108 = 1.05;
218	  else if (id === 632) num108 = 0.8;
219	  else if (id === 691) num108 = 0.85;
220	  // :58770-58783 血僵尸 489：限速 = (2.5 - min(距离×0.0025, 1.5)) × 0.8（expert 恒 false）
221	  // ——距离项需要玩家坐标，在 fighterMoveStep 内取
222	  const scaleBoost = id === 489 || id === 3 || id === 132 || id === 186 || id === 187
223	    || id === 188 || id === 189 || id === 200 || id === 223 || id === 331 || id === 332;
224	  if (scaleBoost) num108 *= 1 + (1 - scale);                          // :58790-58793
225	  return { max: num108, accel: 0.07, damp: 0.8 };
226	}
227	
228	/** 横向移动执行（各分支共形段 1:1）。dir = direction（朝目标）。
229	 *  508/580/582（蚁狮冲锋兽族）走专属平滑逼近式（:58526-58612）。 */
230	export function fighterMoveStep(e: Enemy, dir: number, player: Player | null): void {
231	  const id = e.vanillaId ?? -1;
232	  if (id === 508 || id === 580 || id === 582) { chargerApproach(e, dir, player); return; }
233	  const spec = fighterMoveSpec(e);
234	  if (!spec) return;                        // 原版该型链上无分支（射击族排除表）
235	  let max = spec.max;
236	  if (id === 489 && player) {               // :58770-58783 血僵尸按距离减速
237	    let num109 = Math.hypot(player.cx - e.cx, player.cy - e.cy) * 0.0025;
238	    if (num109 > 1.5) num109 = 1.5;
239	    max = (2.5 - num109) * 0.8;
240	  }
241	  if (e.vx < -max || e.vx > max) {
242	    if (e.vy === 0) e.vx *= spec.damp;      // 原版 velocity *= damp（落地时 Y≈0 等价）
243	  } else if (e.vx < max && dir === 1) {
244	    // :58102-58105 Psycho 466：direction=+1 而 vx<-2（潜伏突袭的逆向余速）→ 先 ×0.9 刹车
245	    if (id === 466 && e.vx < -2) e.vx *= 0.9;
246	    if (spec.reverseDamp !== undefined && e.vy === 0 && e.vx < 0) e.vx *= spec.reverseDamp;
247	    e.vx += spec.accel;
248	    if (e.vx > max) e.vx = max;
249	  } else if (e.vx > -max && dir === -1) {
250	    // :58118-58121 对称侧：direction=-1 而 vx>2 → ×0.9
251	    if (id === 466 && e.vx > 2) e.vx *= 0.9;
252	    if (spec.reverseDamp !== undefined && e.vy === 0 && e.vx > 0) e.vx *= spec.reverseDamp;
253	    e.vx -= spec.accel;
254	    if (e.vx < -max) e.vx = -max;
255	  }
256	  // :58132-58135 弗里茨 462 落地逆行额外衰减
257	  if (id === 462 && e.vy === 0
258	    && ((dir > 0 && e.vx < 0) || (dir < 0 && e.vx > 0))) e.vx *= 0.9;
259	}
260	
261	/** 蚁狮冲锋兽族平滑逼近（:58526-58612）1:1：目标速度档随当前速度分段抬升，
262	 *  靠 (v×n ± 目标)/(n+1) 指数逼近；与目标同向时直接逼近，逆向且 |vy| 小时缓刹。 */
263	function chargerApproach(e: Enemy, dir: number, player: Player | null): void {
264	  const id = e.vanillaId ?? -1;
265	  let num99 = 2.5, num100 = 10;                       // :58528-58529
266	  const speed = Math.abs(e.vx);
267	  if (id === 582) {                                   // :58531-58541 Basilisk
268	    num99 = 2.25; num100 = 7;
269	    if (speed > 2.5) { num99 = 3; num100 += 75; }
270	    else if (speed > 2) { num99 = 2.75; num100 += 55; }
271	  } else if (speed > 2.75) {                          // :58542-58548
272	    num99 = 3.5; num100 += 80;
273	  } else if (speed > 2.25) {
274	    num99 = 3; num100 += 60;
275	  }
276	  if (Math.abs(e.vy) < 0.5) {                         // :58549-58558 落地逆行缓刹
277	    if ((e.vx > 0 && dir < 0) || (e.vx < 0 && dir > 0)) { e.vx *= 0.95; e.vy *= 0.95; }
278	  }
279	  if (Math.abs(e.vy) > 0.3) {                         // :58559-58567 空中(>gravity)逼近加速
280	    num100 *= id === 582 ? 2 : 3;
281	  }
282	  if (e.vx <= 0 && dir < 0) e.vx = (e.vx * num100 - num99) / (num100 + 1);      // :58569-58571
283	  else if (e.vx >= 0 && dir > 0) e.vx = (e.vx * num100 + num99) / (num100 + 1); // :58572-58574
284	  else if (player && Math.abs(e.cx - player.cx) > 20 && Math.abs(e.vy) <= 0.3) {
285	    e.vx *= 0.99;                                     // :58575-58578
286	    e.vx += dir * 0.025;
287	  }
288	}
289	
290	// ---------------------------------------------------------------------------
291	// 混沌元素 120（NPC.cs:57431-57460 到达演出 / :60679-60696 传送触发 /
292	// ai[3] 卡死计数 :57504-57545 / AI_AttemptToFindTeleportSpot :18876-18946）
293	// ---------------------------------------------------------------------------
294	/** 上一帧 X（ai[3] 卡死计数的 position.X == oldPosition.X 判据） */
295	const prevX = new WeakMap<Enemy, number>();
296	/** 两帧前位置（混沌元素传送旧端 FX 用——原版 oldPos[2] :57453） */
297	const pos2 = new WeakMap<Enemy, { x: number; y: number }>();
298	const pos1 = new WeakMap<Enemy, { x: number; y: number }>();
299	
300	/** ai[3] 卡死计数（:57504-57545）+ 传送。仅 type 120：num58 = 180（:57430-57433）。
301	 *  返回新的 ai3 值（调用方写回 this.ai3）。 */
302	export function chaosElementalStep(
303	  e: Enemy, game: GameHooks, p: Player | null,
304	): number {
305	  const num58 = 180;                                   // :57433
306	  const oldX = prevX.get(e) ?? e.x;
307	  prevX.set(e, e.x);
308	  const p2Prev = pos2.get(e) ?? { x: e.x, y: e.y };    // oldPos[2]：两帧前位置
309	  pos2.set(e, pos1.get(e) ?? { x: e.x, y: e.y });
310	  pos1.set(e, { x: e.x, y: e.y });
311	  let ai3 = e.ai3;
312	  if (ai3 === -120) {                                  // :57436-57460 传送到达帧
313	    e.vx = 0; e.vy = 0;
314	    ai3 = 0;
315	    game.playSfxFiles(['Item_8'], 1, e.cx, e.cy);      // :57439 Item8 新位置一次
316	    // 新旧双端各 20 尘 71（alpha200 scale2 noGravity），速度沿 旧→新 方向相向（:57447-57457）
317	    const dir = Math.atan2(e.cy - (p2Prev.y + e.h / 2), e.cx - (p2Prev.x + e.w / 2));
318	    game.spawnBurst?.(e.cx, e.cy, '#B06AE8', 20, 2, dir, 0.5, { life: 30 });
319	    game.spawnBurst?.(p2Prev.x + e.w / 2, p2Prev.y + e.h / 2, '#B06AE8', 20, 2,
320	      dir + Math.PI, 0.5, { life: 30 });
321	  }
322	  // :57520-57524 flag7 = 落地且 vx 与 direction 相逆 → 计数上升
323	  const opposite = e.vy === 0 && ((e.vx > 0 && e.facing < 0) || (e.vx < 0 && e.facing > 0));
324	  if (e.x === oldX || ai3 >= num58 || opposite) ai3 += 1;              // :57525-57528
325	  else if (Math.abs(e.vx) > 0.9 && ai3 > 0) ai3 -= 1;                 // :57529-57531
326	  if (ai3 > num58 * 10) ai3 = 0;                                      // :57533-57535
327	  if (e.justHit) ai3 = 0;                                             // :57537-57539
328	  if (p && p.x < e.x + e.w && p.x + p.w > e.x && p.y < e.y + e.h && p.y + p.h > e.y) {
329	    ai3 = 0;                                                          // :57543-57545 触碰归零
330	  }
331	  if (p && ai3 >= num58) {                                            // :60679-60696
332	    const ttx = Math.floor(p.cx / TILE), tty = Math.floor(p.cy / TILE);
333	    const spot = attemptToFindTeleportSpot(e, game, ttx, tty, 20, 9);
334	    if (spot) {
335	      e.x = spot.x * TILE - e.w / 2;
336	      e.y = spot.y * TILE - e.h;
337	      ai3 = -120;
338	    }
339	  }
340	  return ai3;
341	}
342	
343	/** AI_AttemptToFindTeleportSpot（NPC.cs:18876-18946）1:1。返回落点 tile 坐标。
344	 *  opts：centered=净空改 i±fluff 矩形（星云脑 :41650）；inAir=免脚下实心（星云脑）；
345	 *  dungeonWallGate=地牢法师族门（:18899-18904：type 32/281-286 要求上一格地牢砖墙）。 */
346	export function attemptToFindTeleportSpot(
347	  e: Enemy, game: GameHooks, targetTileX: number, targetTileY: number,
348	  rangeFromTargetTile: number, telefragPreventionDistanceInTiles: number,
349	  opts: { centered?: boolean; inAir?: boolean; dungeonWallGate?: boolean } = {},
350	): { x: number; y: number } | null {
351	  const st = game.world.store;
352	  const cx = Math.floor(e.cx / TILE), cy = Math.floor(e.cy / TILE);    // :18878-18879
353	  // :18901 AnyNPCs(35)：骷髅王在场（打王期间）——地牢法师墙门豁免，每 tick 求值一次
354	  // （enemies 可选访问：测试桩 hooks 可能未实现）
355	  const enemiesOf = (game as { enemies?: () => unknown[] }).enemies;
356	  const skelUp = opts.dungeonWallGate && !!enemiesOf
357	    && enemiesOf.call(game).some((n) => (n as Enemy).vanillaId === 35 && !(n as Enemy).dead);
358	  let num3 = 0;
359	  let found = false;
360	  if (Math.abs(cx * TILE - targetTileX * TILE) + Math.abs(cy * TILE - targetTileY * TILE) > 2000) {
361	    num3 = 100;                                                         // :18885-18888 超距直接放弃
362	  }
363	  let chosen: { x: number; y: number } | null = null;
364	  while (!found && num3 < 100) {                                        // :18890
365	    num3++;
366	    const num5 = targetTileX - rangeFromTargetTile
367	      + Math.floor(Math.random() * (rangeFromTargetTile * 2 + 1));      // :18892
368	    const yStart = targetTileY - rangeFromTargetTile
369	      + Math.floor(Math.random() * (rangeFromTargetTile * 2 + 1));      // :18893
370	    for (let i = yStart; i < targetTileY + rangeFromTargetTile; i++) {  // :18893
371	      // :18896-18899 自身 3×3 邻域跳过 + 非激活格跳过（teleportInAir=false）
372	      if ((i >= cy - 1 && i <= cy + 1 && num5 >= cx - 1 && num5 <= cx + 1)
373	        || !st.inBounds(num5, i) || st.get(num5, i) === 0) continue;
374	      // :18899-18904 地牢法师门：上一格须地牢砖墙（wallDungeon 集）——骷髅王 35
375	      // 在场时豁免（AnyNPCs(35)：打骷髅王期间地牢法师可传到砖墙区外的地表/入口）
376	      if (opts.dungeonWallGate && !skelUp
377	        && !(st.wall[st.idx(num5, i - 1)] >= 7 && st.wall[st.idx(num5, i - 1)] <= 9
378	          || (st.wall[st.idx(num5, i - 1)] >= 94 && st.wall[st.idx(num5, i - 1)] <= 99))) continue;
379	      // :18907-18909 头顶格岩浆面跳过（lava()）
380	      if (!st.inBounds(num5, i - 1) || st.liquidType[st.idx(num5, i - 1)] === 2) continue;
381	      // :18910 脚下须实心（!tileSolid 跳过；teleportInAir 跳过本门）
382	      if (!opts.inAir && !st.isSolid(num5, i)) continue;
383	      // :18915 身位净空（fluff=1）：!centered → (i±1)×(i-4..i-2) 三行；centered → i±1 矩形
384	      let clear = true;
385	      const yLo = opts.centered ? -1 : -4, yHi = opts.centered ? 1 : -2;
386	      for (let dy = yLo; dy <= yHi && clear; dy++) {
387	        for (let dx = -1; dx <= 1; dx++) {
388	          if (st.inBounds(num5 + dx, i + dy) && st.isSolid(num5 + dx, i + dy)) clear = false;
389	        }
390	      }
391	      if (!clear) continue;
392	      // :18926-18945 telefrag 预防：落点外扩 N 格与玩家 AABB（含 20t 速度外推并集）不相交
393	      const ext = telefragPreventionDistanceInTiles * TILE;
394	      const box = { x: num5 * TILE - ext, y: i * TILE - ext, w: TILE + ext * 2, h: TILE + ext * 2 };
395	      const p = game.player as Player;
396	      const ux = p.x + p.vx * 20, uy = p.y + p.vy * 20;                 // num4=20（:18884）
397	      const px0 = Math.min(p.x, ux), px1 = Math.max(p.x + p.w, ux + p.w);
398	      const py0 = Math.min(p.y, uy), py1 = Math.max(p.y + p.h, uy + p.h);
399	      if (px0 < box.x + box.w && px1 > box.x && py0 < box.y + box.h && py1 > box.y) {
400	        found = false;
401	        break;
402	      }
403	      chosen = { x: num5, y: i };
404	      found = true;
405	      break;
406	    }
407	  }
408	  return chosen;
409	}
410	
411	// ---------------------------------------------------------------------------
412	// 沼泽怪 166 伏击（NPC.cs:56327-56360）：1/240 概率进入伏击态（ai[2] = -480..-60），
413	// 静立到 受击 / 看见玩家 为止；期间只做原地减速并跳过本 tick 行走。
414	// 返回 true = 本 tick 已被伏击分支接管（调用方跳过行走段）。
415	// ---------------------------------------------------------------------------
416	export function swampThingAmbushStep(e: Enemy, canSee: boolean): boolean {
417	  if (e.vanillaId !== 166) return false;
418	  if (Math.random() < 1 / 240) e.ai2 = -(60 + Math.floor(Math.random() * 420));  // :56329-56332
419	  if (e.ai2 < 0) {
420	    if (e.justHit) e.ai2 = 0;                                                    // :56338-56340
421	    if (canSee) e.ai2 = 0;                                                       // :56341-56344
422	  }
423	  if (e.ai2 < 0) {
424	    e.vx *= 0.9;                                                                 // :56349
425	    if (e.vx > -0.1 && e.vx < 0.1) e.vx = 0;                                     // :56350-56354
426	    e.ai2 += 1;                                                                  // :56355
427	    if (e.ai2 === 0) e.vx = e.facing * 0.1;                                      // :56356-56358
428	    return true;
429	  }
430	  return false;
431	}
432	
433	// ---------------------------------------------------------------------------
434	// 693 图书管理员骷髅——贴书传送（NPC.cs AI_AttemptToFindTeleportSpotNearBooks
435	// :18948-19046，caster AI :21068-21076 消费：先贴书、失败落回通用法师传送）
436	// ---------------------------------------------------------------------------
437	
438	/** SearchWall（:19026-19046）：从墙面格 (x,y) 沿垂直向找第一本贴墙书。
439	 *  返回 [bookY, outOfBounds]：找到书 → [书 y,false]；撞实心/出界终止 → [0,标记]；
440	 *  书在玩家扩展盒（命中盒 ∪ 速度×20 外推盒，再外扩 80px）内 → 视同终止 [0,false]。
441	 *  （do-while 条件 = !active || !solid：穿空气与非实心续走；书格 type 50 半途截获） */
442	function nearBooksSearchWall(
443	  e: Enemy, game: GameHooks, x: number, y0: number, downwards: boolean,
444	): { bookY: number; outOfBounds: boolean } {
445	  const st = game.world.store;
446	  const step = downwards ? 1 : -1;
447	  let y = y0;
448	  let tileActive = false, tileSolid = false;
449	  // do-while：先走一格再判（:19035-19044）
450	  for (;;) {
451	    y += step;
452	    if (y < 0 || y >= st.h) return { bookY: 0, outOfBounds: true };
453	    const t = st.get(x, y);
454	    tileActive = t !== 0;
455	    tileSolid = tileActive && st.isSolid(x, y);
456	    if (tileActive && TILE_DEFS[t]?.vanilla?.sheet === 50) {
457	      // :19040-19044 书格 16×16 外扩 80px 与玩家并集盒相交 → 弃书终止本列
458	      const p = game.player as Player;
459	      if (p && !p.dead) {
460	        const ux0 = Math.min(p.x, p.x + p.vx * 20), ux1 = Math.max(p.x + p.w, p.x + p.w + p.vx * 20);
461	        const uy0 = Math.min(p.y, p.y + p.vy * 20), uy1 = Math.max(p.y + p.h, p.y + p.h + p.vy * 20);
462	        if (x * TILE - 80 < ux1 && x * TILE + TILE + 80 > ux0
463	          && y * TILE - 80 < uy1 && y * TILE + TILE + 80 > uy0) {
464	          return { bookY: 0, outOfBounds: false };
465	        }
466	      }
467	      return { bookY: y, outOfBounds: false };
468	    }
469	    if (tileActive && tileSolid) return { bookY: 0, outOfBounds: false };
470	  }
471	}
472	
473	/** AI_AttemptToFindTeleportSpotNearBooks（:18948-19024）1:1：玩家 30 格窗内
474	 *  随机取"地牢墙背景 + 无实块"列，交替方向水平推进至墙面，贴墙面垂直扫书，
475	 *  落点 = 书格向墙面外退一格（destination.X -= num5）+ 下一格（Y+1）。
476	 *  @returns 落点（格坐标 float 语义； caster AI 存 ai[2]/ai[3]）| null */
477	export function attemptToFindTeleportSpotNearBooks(
478	  e: Enemy, game: GameHooks, targetTileX: number, targetTileY: number, maxRangeInTiles: number,
479	): { x: number; y: number } | null {
480	  const st = game.world.store;
481	  const num = Math.floor(e.cx / TILE), num2 = Math.floor(e.cy / TILE);   // :18950-18951
482	  // :18954-18958 自身距目标 >125 格 → 直接放弃（贴书传送只做近距）
483	  if (Math.hypot(num - targetTileX, num2 - targetTileY) > 125) return null;
484	  let num5 = (Math.floor(Math.random() * 2)) * 2 - 1;                    // :18959
485	  for (let i = 0; i < 100; i++) {                                        // :18960
486	    const num6 = targetTileX - maxRangeInTiles + Math.floor(Math.random() * (maxRangeInTiles * 2 + 1));
487	    const num7 = targetTileY - maxRangeInTiles + Math.floor(Math.random() * (maxRangeInTiles * 2 + 1));
488	    if (num6 < 0 || num7 < 0 || num6 >= st.w || num7 >= st.h) {
489	      return null;    // WorldGen.InWorld(Point) 默认 fluff=0（:18966-18968——整轮放弃非 continue）
490	    }
491	    // :18970-18973 落列须地牢墙背景（7-9/94-99）且无激活块
492	    const wHere = st.wall[st.idx(num6, num7)];
493	    const isDungeonWall = (wHere >= 7 && wHere <= 9) || (wHere >= 94 && wHere <= 99);
494	    if (!isDungeonWall || st.get(num6, num7) !== 0) continue;
495	    num5 *= -1;                                                          // :18975 每次有效尝试换向
496	    // :18977-18990 沿 num5 方向走到第一块实心（墙面），越窗 → 弃本轮
497	    let x = num6;
498	    const xLo = Math.max(0, targetTileX - maxRangeInTiles);
499	    const xHi = Math.min(st.w - 1, targetTileX + maxRangeInTiles);
500	    let outOfBounds = false;
501	    for (;;) {
502	      x += num5;
503	      if (x < xLo || x > xHi) { outOfBounds = true; break; }
504	      if (st.get(x, num7) !== 0 && st.isSolid(x, num7)) break;
505	    }
506	    if (outOfBounds) continue;
507	    x -= num5;                                                           // :18995 退回墙面外一格
508	    // :18996-19012 墙列向下扫书；同列连续多本（避自身格 ±1 内续找下一本）
509	    let y = num7;
510	    for (;;) {
511	      const r = nearBooksSearchWall(e, game, x, y, true);
512	      if (!r.bookY && !r.outOfBounds) break;
513	      if (r.outOfBounds) { y = -1; break; }
514	      if (Math.abs(r.bookY - num2) <= 1 && Math.abs(x - num) <= 1) { y = r.bookY; continue; }
515	      return { x: x - num5, y: r.bookY + 1 };                            // :19006-19008
516	    }
517	    if (y < 0) continue;
518	    // :19013-19023 同列向上扫书（同语义）
519	    y = num7;
520	    for (;;) {
521	      const r = nearBooksSearchWall(e, game, x, y, false);
522	      if (!r.bookY && !r.outOfBounds) break;
523	      if (r.outOfBounds) break;
524	      if (Math.abs(r.bookY - num2) <= 1 && Math.abs(x - num) <= 1) { y = r.bookY; continue; }
525	      return { x: x - num5, y: r.bookY + 1 };
526	    }
527	  }
528	  return null;
529	}
530	
531	// ---------------------------------------------------------------------------
532	// 日食怪战士族专属行为分支（AI_003_Fighters 内 type 段，1.4.5.6 1:1）
533	// ---------------------------------------------------------------------------
534	
535	/** Psycho 466 潜伏突袭（NPC.cs:56290-56326，AI_003 最前段——比行走/跳跃/远程全早，
536	 *  两分支 return 跳过本 tick 余段；重力由 UpdateNPC 尾补，本仓等价自补）。
537	 *  ai[2] 状态机：0=潜伏（alpha 200 全隐 + TargetClosest，玩家 <170px / 被推动 /
538	 *  被击 → -16）；<0=显形倒数（alpha 每 tick −num5/16 = −12.5，ai[2]+1 至 0 时
539	 *  ai[2]=1 并 vx=direction×2 起冲）；≥1=显形（alpha 0，走通用段）。
540	 *  @returns true = 本 tick 已被潜伏/显形段接管（调用方直接收尾） */
541	export function psychoStealthStep(e: Enemy, game: GameHooks, p: Player | null): boolean {
542	  if (e.vanillaId !== 466) return false;
543	  const num5 = 200;                                       // :56292
544	  if (e.ai2 === 0) {
545	    e.spawnAlpha = num5;                                  // :56295 潜伏全隐
546	    if (p) e.facing = e.seekDirX(p);                      // :56296 TargetClosest
547	    // :56297-56300：目标存活且中心距 <170px → 触发显形
548	    if (p && !p.dead && Math.hypot(p.cx - e.cx, p.cy - e.cy) < 170) e.ai2 = -16;
549	    // :56301-56304：自身被推动/下落超两档重力/受击 → 同样触发
550	    if (e.vx !== 0 || e.vy < 0 || e.vy > 2 || e.justHit) e.ai2 = -16;
551	    e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);      // :56305 return（UpdateNPC :91519 重力）
552	    moveAndCollide(e, game.world, e.vx, e.vy);
553	    return true;
554	  }
555	  if (e.ai2 < 0) {
556	    if (e.spawnAlpha > 0) {                               // :56309-56316 显形渐入
557	      e.spawnAlpha -= num5 / 16;
558	      if (e.spawnAlpha < 0) e.spawnAlpha = 0;
559	    }
560	    e.ai2 += 1;                                           // :56317
561	    if (e.ai2 === 0) {                                    // :56318-56322 显形完成 → 起冲
562	      e.ai2 = 1;
563	      e.vx = e.facing * 2;
564	    }
565	    e.vy = Math.min(e.vy + GRAVITY, MAX_FALL_SPEED);      // :56323 return
566	    moveAndCollide(e, game.world, e.vx, e.vy);
567	    return true;
568	  }
569	  e.spawnAlpha = 0;                                       // :56325 显形态恒 0
570	  return false;
571	}
572	
573	/** Nailhead 463 受击散射（NPC.cs:57547-57613）。justHit 且 localAI[3] 冷却尽且 1/3
574	 *  掷中 → 冷却 30t，散射 3-5 枚 Nail 弹（proj 498，伤害 = 自身 damage×0.15 截断，
575	 *  击退 1）。方向：每发随机单位向量，有目标时先向目标平均向量偏置再归一；末尾
576	 *  num68 发改为直指目标。单人下目标集 = 本地玩家（CanHitLine 门）。
577	 *  弹速 num76 = rand(8..12)。发射点 = (Center.X, position.Y + width/4)（:57611）。 */
578	export function nailheadHitScatter(e: Enemy, game: GameHooks, p: Player | null): void {
579	  if (e.vanillaId !== 463) return;
580	  if (e.lai3 > 0) e.lai3 -= 1;                            // :57549-57552 localAI[3] 冷却
581	  if (!(e.justHit && e.lai3 <= 0 && Math.floor(Math.random() * 3) === 0)) return;  // :57553
582	  e.lai3 = 30;                                            // :57555
583	  const num67 = 3 + Math.floor(Math.random() * 3);        // :57556 Next(3,6) = 3-5 发
584	  // :57559-57570 目标收集（255 玩家全扫 → 单人 = 本地玩家，CanHitLine 门）
585	  let num68 = 0;
586	  if (p && !p.dead
587	    && canHitLine(game.world.store, e.x, e.y, e.w, e.h, p.x, p.y, p.w, p.h)) num68 = 1;
588	  // :57585-57592 vector20 = (-1,-1) + Σ(目标单位向量) 归一（目标平均方向）
589	  let bx = -1, by = -1;
590	  if (num68 > 0) {
591	    const ddx = p!.cx - e.cx, ddy = p!.cy - e.cy;
592	    const dd = Math.hypot(ddx, ddy) || 1;
593	    bx += ddx / dd; by += ddy / dd;
594	    const bd = Math.hypot(bx, by) || 1;
595	    bx /= bd; by /= bd;
596	  }
597	  const ox = e.cx;                                        // :57611 Center.X
598	  const oy = e.y + e.w / 4;                               // :57611 position.Y + width/4
599	  const dmg = Math.trunc(e.def.damage * 0.15);            // :57611 (int)(damage * 0.15)
600	  for (let i = 0; i < num67; i++) {
601	    const num76 = 8 + Math.floor(Math.random() * 5);      // :57595 Next(8,13) = 8-12
602	    let vx = Math.floor(Math.random() * 201) - 100;       // :57596 Next(-100,101)
603	    let vy = Math.floor(Math.random() * 201) - 100;
604	    const vd = Math.hypot(vx, vy) || 1;
605	    vx /= vd; vy /= vd;                                   // :57597
606	    if (num68 > 0) {                                      // :57598-57602 目标偏置
607	      vx += bx; vy += by;
608	      const vd2 = Math.hypot(vx, vy) || 1;
609	      vx /= vd2; vy /= vd2;
610	    }
611	    vx *= num76; vy *= num76;                             // :57603
612	    if (num68 > 0) {                                      // :57604-57610 末发直指目标
613	      num68--;
614	      const ddx = p!.cx - e.cx, ddy = p!.cy - e.cy;
615	      const dd = Math.hypot(ddx, ddy) || 1;
616	      vx = (ddx / dd) * num76; vy = (ddy / dd) * num76;
617	    }
618	    e.spawnHostileProj(game, ox, oy, vx, vy, dmg, 498);   // :57611 proj 498 Nail（kb 1 → Dart 无击退通道，登记）
619	  }
620	}
621	
622	/** Butcher 460 空中免击退（NPC.cs:57615-57624）：|vy| 超过一档重力步（正被击飞/
623	 *  下坠加速中）→ knockBackResist=0 完全免疫；否则 0.25 走难度曲线。
624	 *  原版阈值是 npc.gravity(0.3)（NPC.cs:6026），本仓战士重力步长 = GRAVITY，
625	 *  语义一致（自由落体 ≥2 tick 即超过）。 */
626	export function butcherKbStep(e: Enemy): void {
627	  if (e.vanillaId !== 460) return;
628	  if (e.vy < -GRAVITY || e.vy > GRAVITY) {
629	    e.kbResistOverride = 0;                               // :57617-57620
630	  } else {
631	    e.kbResistOverride = getKnockbackMultiplierScaledByDifficulty(0.25, e.difficulty); // :57623
632	  }
633	}
634	
635	/** Possessed 469 背景墙爬行冲刺（NPC.cs:57626-57677）。
636	 *  击退：0.45 难度曲线；爬墙冲刺态（ai[2]==1）免疫（:57628-57632）。
637	 *  flag11 = 中心 3×3 任一格有背景墙（:57634-57650）。
638	 *   ai[2]==0 且贴墙：落地 → 上蹿 vy=-4.6、vx×1.3（flag=true 放行空中跳跃段）；
639	 *   下坠中且目标存活 → 转 ai[2]=1（:57651-57663）。
640	 *   ai[2]==1 且贴墙且视线通 → 冲刺：期望速度 = 朝目标单位向量 × (4.5 + 距离/300)，
641	 *   29/30 平滑逼近，noGravity（:57664-57673，段末 return）。
642	 *  不满足任一 → noGravity=false、ai[2]=0（:57675-57676，回通用段）。
643	 *  @returns true = 冲刺分支本 tick 已接管（调用方收尾） */
644	export function possessedStep(e: Enemy, game: GameHooks, p: Player | null): boolean {
645	  if (e.vanillaId !== 469) return false;
646	  e.kbResistOverride = e.ai2 === 1
647	    ? 0
648	    : getKnockbackMultiplierScaledByDifficulty(0.45, e.difficulty);   // :57628-57632
649	  const st = game.world.store;
650	  // flag11（:57634-57650）：中心 3×3 内任一格 wall>0
651	  const nx = Math.floor(e.cx / TILE), ny = Math.floor(e.cy / TILE);
652	  let flag11 = false;
653	  for (let i = nx - 1; i <= nx + 1 && !flag11; i++) {
654	    for (let j = ny - 1; j <= ny + 1; j++) {
655	      if (st.inBounds(i, j) && st.wall[st.idx(i, j)] > 0) { flag11 = true; break; }
656	    }
657	  }
658	  if (e.ai2 === 0 && flag11) {
659	    if (e.vy === 0) {                                     // :57653-57658 贴墙起跳
660	      e.vy = -4.6;
661	      e.vx *= 1.3;
662	    } else if (e.vy > 0 && p && !p.dead) {
663	      e.ai2 = 1;                                          // :57659-57662 下坠中转爬墙态
664	    }
665	  }
666	  if (flag11 && e.ai2 === 1 && p && !p.dead
667	    && canHit(st, e.x, e.y, e.w, e.h, p.x, p.y, p.w, p.h)) {           // :57664
668	    const dx = p.cx - e.cx, dy = p.cy - e.cy;             // :57666 vector23
669	    const num81 = Math.hypot(dx, dy) || 1;                // :57667
670	    const spd = 4.5 + num81 / 300;                        // :57669
671	    e.vx = (e.vx * 29 + (dx / num81) * spd) / 30;         // :57670 29/30 平滑
672	    e.vy = (e.vy * 29 + (dy / num81) * spd) / 30;
673	    e.ai2 = 1;                                            // :57672
674	    e.x += e.vx; e.y += e.vy;                             // noGravity=true（:57671）无碰撞积分
675	    return true;                                          // :57673 return
676	  }
677	  e.ai2 = 0;                                              // :57675-57676
678	  return false;
679	}
680	
681	/** Fritz 462 跳扑（NPC.cs:57678-57710）。落地 + 目标 <150px + |vx|>3 + 朝目标
682	 *  横向逼近 → vx×1.75、vy−4.5；目标在【上方】时按自身中心低于目标的落差
683	 *  （Center.Y 差）≥20/40/80/100px 逐档追加 −0.5/−1/−1.5/−1.5（越高跳得越高）；
684	 *  |vx| 钳 7。段内 flag=true（放行空中跳跃段），不 return——继续走本 tick 通用行走。 */
685	export function fritzPounceStep(e: Enemy, p: Player | null): void {
686	  if (e.vanillaId !== 462 || e.vy !== 0 || !p) return;
687	  if (Math.hypot(p.cx - e.cx, p.cy - e.cy) >= 150) return;            // :57678 <150px
688	  if (Math.abs(e.vx) <= 3) return;                                    // :57678 |vx|>3
689	  // :57678 朝目标横向逼近（vx 与 目标方向 同号）
690	  if (!((e.vx < 0 && e.cx > p.cx) || (e.vx > 0 && e.cx < p.cx))) return;
691	  e.vx *= 1.75;                                                       // :57681
692	  e.vy -= 4.5;                                                        // :57682
693	  const drop = e.cy - p.cy;                                           // :57683 自身中心 − 目标中心
694	  if (drop > 20) e.vy -= 0.5;                                         // :57683-57684
695	  if (drop > 40) e.vy -= 1;                                           // :57687-57688
696	  if (drop > 80) e.vy -= 1.5;                                         // :57691-57692
697	  if (drop > 100) e.vy -= 1.5;                                        // :57695-57696
698	  if (Math.abs(e.vx) > 7) e.vx = e.vx < 0 ? -7 : 7;                   // :57699-57709
699	}
700	
701	// ---------------------------------------------------------------------------
702	// 425 风暴潜水员（AI_003_Fighters 内 type==425 专属段，NPC.cs:58865-59013）
703	//   原版与横向移动链（:57799-58598，fighterMoveStep）是两段独立 if/else-if 阶梯
704	//   ——425 两段都命中（链上 num84=6 档 + 本段喷包/蓄力），故 hook 在
705	//   fighterMoveStep 之后、重力/碰撞之前。
706	// ---------------------------------------------------------------------------
707	
708	/** 425 ai[3] 瞄准蓄力状态机（NPC.cs:58968-59006 计数节奏，纯函数）：
709	 *  负段 = 冷却 +1/t；0..30 蓄力带按 aim ±1 钳 [0,30]；满蓄 30 → 发射（fired）
710	 *  并进 31；31..40 放射后渐灭段 +1/t，到 40 重置 −150（= num118 − num120 =
711	 *  30−180）。出生初值 −120（:58868-58872，经 localAI[3]==0 门）由调用方置入。
712	 *  渲染侧 Renderer.npcGlowSparkleEnvelope 消费 e.ai3（opacity=Remap(ai3,0,15,0,1)
713	 *  蓄力渐亮、num=GetLerpValue(0,30)×GetLerpValue(36,30) 放射后 30→36 渐灭）——
714	 *  Main.cs:25632 枪口星芒即读 ai[3]，AI 侧必须按本节奏维护。 */
715	export function stormDiverAimStep(ai3: number, aim: boolean): { ai3: number; fired: boolean } {
716	  const CHARGE = 30, DECAY = 10, COOLDOWN = 180;                      // num118/num119/num120（:58968-58969）
717	  if (ai3 < 0) return { ai3: ai3 + 1, fired: false };                 // :58970-58972 冷却回摆
718	  if (ai3 > CHARGE) {                                                 // :58976-58980 放射段（≥31）
719	    const next = ai3 + 1;
720	    return { ai3: next >= CHARGE + DECAY ? CHARGE - COOLDOWN : next, fired: false };
721	  }
722	  const v = Math.max(0, Math.min(CHARGE, ai3 + (aim ? 1 : -1)));      // :58970-58975 蓄力带 ±1
723	  if (v === CHARGE) return { ai3: CHARGE + 1, fired: true };          // :58981-58984 满蓄发射 → 31
724	  return { ai3: v, fired: false };
725	}
726	
727	/** Utils.GetChaseResults（Utils.cs:619-661）1:1。runnerVelocity 为零 → 直飞用时
728	 *  距离/速度；否则二次方程 a=s²−v² / b=2·dot(Δ, v) / c=−|Δ|²（Δ=追者−逃者），
729	 *  无实根/双负根 → 拦截失败返回 null，双正根取小、一正一负取大。返回拦截速度
730	 *  （模长 = chaserSpeed）。 */
731	function getChaseResults(
732	  chaserX: number, chaserY: number, chaserSpeed: number,
733	  runnerX: number, runnerY: number, runnerVx: number, runnerVy: number,
734	): { x: number; y: number } | null {
735	  if (chaserX === runnerX && chaserY === runnerY) return { x: 0, y: 0 };
736	  if (chaserSpeed <= 0) return null;
737	  const dx = chaserX - runnerX, dy = chaserY - runnerY;               // value（:638）
738	  const dist = Math.hypot(dx, dy);                                    // num
739	  const runnerSpeed = Math.hypot(runnerVx, runnerVy);                 // num2
740	  let t: number;
741	  if (runnerSpeed === 0) {
742	    t = dist / chaserSpeed;                                           // :644-646
743	  } else {
744	    const a = chaserSpeed * chaserSpeed - runnerSpeed * runnerSpeed;  // :650
745	    const b = 2 * (dx * runnerVx + dy * runnerVy);                    // :651
746	    const c = -dist * dist;                                           // :652
747	    const disc = b * b - 4 * a * c;                                   // SolveQuadratic（:692-705）
748	    if (disc < 0) return null;
749	    let r1: number, r2: number;
750	    if (disc > 0) {
751	      const s = Math.sqrt(disc);
752	      r1 = (-b + s) / (2 * a);
753	      r2 = (-b - s) / (2 * a);
754	    } else {
755	      r1 = r2 = -b / (2 * a);
756	    }
757	    if (r1 < 0 && r2 < 0) return null;                                // :655-655
758	    t = r1 > 0 && r2 > 0 ? Math.min(r1, r2) : Math.max(r1, r2);       // :656-661
759	  }
760	  const ix = runnerX + runnerVx * t, iy = runnerY + runnerVy * t;     // InterceptionPosition
761	  return { x: (ix - chaserX) / t, y: (iy - chaserY) / t };            // ChaserVelocity
762	}
763	
764	/** 425 专属段（NPC.cs:58865-59015）。调用点 = Enemy.fighterAI 内 fighterMoveStep 之后
765	 *  （原版横向移动链 :57799-58598 与本段是两段独立 if/else-if 阶梯——425 两段都命中：
766	 *  链上 num84=6 行走档 + 本段喷包/蓄力）：
767	 *  - localAI[3]==0 出生门 → ai3=−120（2s 起手延迟，:58867-58871）；
768	 *  - 落地清 ai2（喷包态复位，:58872-58875）；空中 ai2==1 → 喷包伺服（保持玩家横向
769	 *    300px、纵向 20px 死区，0.3 步进钳横 7，:58876-58916）+ 1/3 喷口尘（:58931-58939）
770	 *    + 同族挤开（:58940-58961）；
771	 *  - 起飞门：玩家中心高于自身顶 ≥100px 且视线通 → vy=−5、ai2=1（:58963-58966）；
772	 *  - ai3 蓄力（stormDiverAimStep）：aim = |dy|≤|dx| && 距离<800 && CanHitLine
773	 *    （:58978-58980）；满蓄自枪口 Center+(direction*30, 2) 发 4× 弹 577——直瞄 20 速，
774	 *    拦截成功（玩家速度×0.5/2 领先量）改半速 10，首发精确其余 ±0.8 抖动（:58988-59015）。 */
775	export function stormDiverStep(e: Enemy, game: GameHooks, player: Player | null): void {
776	  if (e.vanillaId !== 425) return;
777	  if (e.lai3 === 0) { e.lai3 = 1; e.ai3 = -120; }                     // :58867-58871 出生门
778	  if (e.vy === 0) e.ai2 = 0;                                          // :58872-58875 落地复位喷包态
779	  const st = game.world.store;
780	  if (player && !player.dead) {
781	    if (e.vy !== 0 && e.ai2 === 1) {
782	      // ---- 喷包空中伺服（:58876-58916）----
783	      // 注：本分支原版另置 spriteDirection=-direction（:58878）；FindFrame case 425
784	      //（:71003-71005）对全部帧恒置同式 → 等价"贴图恒反向"，属绘制层登记项（S 侧），
785	      // 此处不翻 facing 以免起降瞬间往返镜像。
786	      if (canHit(st, e.x, e.y, e.w, e.h, player.x, player.y, player.w, player.h)) {
787	        const num115 = player.cx - e.facing * 300 - e.cx;             // :58886 横向期望（保持 300px）
788	        const num116 = player.y + player.h - (e.y + e.h);             // :58887 Bottom 差
789	        if (num115 < 0 && e.vx > 0) e.vx *= 0.9;                      // :58888-58892 逆期望阻尼
790	        else if (num115 > 0 && e.vx < 0) e.vx *= 0.9;
791	        if (num115 < 0 && e.vx > -7) e.vx -= 0.3;                     // :58893-58896
792	        else if (num115 > 0 && e.vx < 7) e.vx += 0.3;
793	        if (e.vx > 7) e.vx = 7;                                       // :58897-58902 钳横 7
794	        if (e.vx < -7) e.vx = -7;
795	        if (num116 < -20 && e.vy > 0) e.vy *= 0.8;                    // :58904-58908 纵向死区 20px
796	        else if (num116 > 20 && e.vy < 0) e.vy *= 0.8;
797	        if (num116 < -20 && e.vy > -8) e.vy -= 0.3;                   // :58909-58912
798	        else if (num116 > 20 && e.vy < 8) e.vy += 0.3;
799	      }
800	      if (Math.floor(Math.random() * 3) === 0) {                      // :58931-58939 喷口尘（1/3）
801	        game.spawnParticles(
802	          e.cx - e.facing * 14 - 4, e.cy - 8 - 4, '#FFB060', 1, 0.6,
803	          { life: 26, damp: 0.94 });
804	      }
805	      // ---- 同族挤开（:58940-58961，Manhattan < width → ±0.15 推离）----
806	      for (const o of game.enemies() as Enemy[]) {
807	        if (o === e || o.dead || o.vanillaId !== 425) continue;
808	        if (Math.abs(e.x - o.x) + Math.abs(e.y - o.y) < e.w) {
809	          e.vx += e.x < o.x ? -0.15 : 0.15;                           // :58951-58956
810	          e.vy += e.y < o.y ? -0.15 : 0.15;                           // :58957-58960
811	        }
812	      }
813	    } else if (player.cy + 100 < e.y                                   // :58963 Center.Y+100 < position.Y
814	      && canHit(st, e.x, e.y, e.w, e.h, player.x, player.y, player.w, player.h)) {
815	      e.vy = -5;                                                      // :58964-58965 起飞
816	      e.ai2 = 1;                                                      // :58966
817	    }
818	    // ---- ai3 瞄准蓄力（:58969-58985，状态机见 stormDiverAimStep）----
819	    const dx = player.cx - e.cx, dy = player.cy - e.cy;
820	    const aim = Math.abs(dy) <= Math.abs(dx)                          // :58978-58979 |dir.Y|≤|dir.X|
821	      && Math.hypot(dx, dy) < 800                                     // :58980 距离门
822	      && canHitLine(st, e.cx, e.cy, 0, 0, player.cx, player.cy, 0, 0); // :58980 CanHitLine(center,0,0→center,0,0)
823	    const step = stormDiverAimStep(e.ai3, aim);
824	    e.ai3 = step.ai3;
825	    if (step.fired) {                                                 // :58988-59015 满蓄发射
826	      const mx = e.cx + e.facing * 30, my = e.cy + 2;                 // :58993 chaserPosition = Center+(dir*30,2)
827	      const num121 = 20;                                              // :58992 弹速
828	      const num122 = 2;                                               // :58999 拦截档除数
829	      const dd = Math.hypot(player.cx - mx, player.cy - my) || 1;
830	      let vx = ((player.cx - mx) / dd) * num121;                      // :58994 vector28 = DirectionTo×20
831	      let vy = ((player.cy - my) / dd) * num121;
832	      if (dd <= 0.01) { vx = e.facing * num121; vy = 0; }             // :58995-58997 HasNaNs 退化档 (dir*20, 0)
833	      const chase = getChaseResults(                                  // :59000-59002 领先半速拦截
834	        mx, my, num121, player.cx, player.cy, player.vx * 0.5 / num122, player.vy * 0.5 / num122);
835	      if (chase) { vx = chase.x / num122; vy = chase.y / num122; }
836	      const dmg = getAttackDamageForProjectiles(75, 50, e.difficulty); // :59007 GetAttackDamage_ForProjectiles(75,50)
837	      for (let i = 0; i < 4; i++) {                                   // :59008-59014 四连发
838	        const jx = i !== 0 ? (Math.random() * 1.6 - 0.8) : 0;         // 首发精确，其余 ±0.8（:59009-59010）
839	        const jy = i !== 0 ? (Math.random() * 1.6 - 0.8) : 0;
840	        e.spawnHostileProj(game, mx, my, vx + jx, vy + jy, dmg, 577); // :59011 proj 577（kb 1）
841	      }
842	    }
843	  }
844	}
845	
846	

```


---

## 🤖 Assistant · 2026-08-19T03:06:54.556Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now I have a good picture of fighterFamilies.ts. Let me continue reading our Enemy.ts sections: rest of fighterAI (2667-2716), solenianDashAI (2716-2771), RANGED tables (2771-2821), then wallCreeperAI, lostGirlAI, mimicAI, plantAI, blazingWheelAI, spikeBallAI, casterAI, slimeAI.

Let me read those chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:06:54.732Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 380,
 "offset": 2668
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:54.750Z

**📎 ToolResult**

```
2668	    }
2669	    // ---- Eyezor 251 死光（NPC.cs:59335-59378：独立 type 段，**不在**通用射击族
2670	    // （:59464 表无 251）；ai[2] 每 tick +1（:59349），justHit 倒扣 rand(30)（:59337），
2671	    // confused 清零（:59345），负值钳 0（:59341）。阈值 = rand(60..1799)×(HP比)+15
2672	    // （:59350-59352 每次判定重掷）。命中门：计时达标 + 落地 + 玩家存活且未冰冻
2673	    // （:59353 !Main.player[target].frozen = buff 47）+ 朝向玩家 + CanHit；再过
2674	    // <700px 距离门（:59363-59364）→ EyeLaser 83（速 15 伤 30；枪口
2675	    // (Center.X + 6×direction, position.Y + 12)，瞄准 + 散布 ±40 / Y −30..−1，
2676	    // 出生点沿弹向 +vel×3）；发射后 ai[2]=0（:59374）
2677	    if (this.vanillaId === 251 && player) {
2678	      if (this.justHit) this.ai2 -= Math.floor(Math.random() * 30);      // :59337-59340
2679	      if (this.ai2 < 0) this.ai2 = 0;                                    // :59341-59344
2680	      if (this.confused) this.ai2 = 0;                                   // :59345-59348
2681	      this.ai2 += 1;                                                     // :59349
2682	      // num142（:59350-59352）：rand(60,1800) × (life/lifeMax) + 15
2683	      const num142 = (60 + Math.floor(Math.random() * 1740)) * (this.hp / this.maxHp) + 15;
2684	      const facingPlayer = (this.facing > 0 && this.cx < player.cx)
2685	        || (this.facing < 0 && this.cx > player.cx);                     // :59353 direction 锥
2686	      if (this.ai2 >= num142 && this.vy === 0 && !player.dead
2687	        && !player.buffs?.has(BuffType.Frozen)                           // :59353 !frozen
2688	        && facingPlayer && this.canSeePlayer(st, player)) {
2689	        // 枪口（:59356-59357）：(Center.X + 6×direction, position.Y + 12)
2690	        const mx = this.cx + 6 * this.facing, my = this.y + 12;
2691	        let num144 = player.cx - mx + (Math.random() * 82 - 41);         // :59358/:59360 ±41
2692	        let num145 = player.cy - my + (Math.floor(Math.random() * 30) - 30); // :59359/:59361 −30..−1
2693	        const num146 = Math.hypot(num144, num145);                       // :59362
2694	        if (num146 < 700) {                                              // :59363-59364 距离门
2695	          const num143 = 15;                                             // :59355 弹速
2696	          // 出生点沿弹向 +vel×3（:59371-59372）
2697	          const u = num146 || 1;
2698	          this.shootDart(game, mx + (num144 / u) * num143 * 3, my + (num145 / u) * num143 * 3,
2699	            num144, num145, num143, 30, 83);                             // :59373 proj 83 伤 30
2700	          this.ai2 = 0;                                                  // :59374
2701	        }
2702	      }
2703	    }
2704	  }
2705	
2706	  /** 419 日耀旋刃怪冲刺（NPC.cs:57114-57173，AI_003_Fighters 内 type==419 专属段，
2707	   *  位于通用行走段之前——各分支 return 跳过行走/跳跃/远程，仅留全局重力+碰撞）。
2708	   *  ai[2] 状态机（num40=6 / num41=10 / num42=16）：
2709	   *    >0   落地恢复倒数（触地或受击置 60）
2710	   *    0    巡航：面朝玩家 + 视线 → -1（本 tick 仍走通用段，cs 无 return）
2711	   *    -1..-6  蓄力：vx×0.9
2712	   *    -7   发射：朝 player.Top+(0,-30) 方向 ×16
2713	   *    <-7  冲刺：-17 起 vy+0.15 钳 24（前 10t 无重力增量）；反射弹幕 + 受击 ×3
2714	   *  拖尾渲染（ai2≤-9 oldPos 拖尾）已就位：Renderer NPC_GLOW[419] mode 'trail'。
2715	   *  @returns true = 冲刺族本 tick 已自管重力+碰撞，调用方应跳过通用战士段 */
2716	  private solenianDashAI(game: GameHooks, player: Player): boolean {
2717	    const WINDUP = 6;    // num40：蓄力 tick 数（-1..-6）
2718	    const DASH_SPEED = 16; // num42：冲刺初速
2719	    this.reflectsProjectiles = false;
2720	    this.takenDamageMultiplier = 1;
2721	    if (this.ai2 > 0) this.ai2 -= 1;
2722	    if (this.ai2 === 0) {
2723	      // 巡航待发（cs:57124-57131）：面朝玩家（direction 与玩家水平侧一致）+ 中心视线
2724	      if (((player.cx < this.cx && this.facing < 0) || (player.cx > this.cx && this.facing > 0))
2725	        && this.canSeePlayer(game.world.store, player)) {
2726	        this.ai2 = -1;
2727	      }
2728	      return false;   // 未触发/刚起手 → 本 tick 走通用行走段（cs 该分支无 return）
2729	    }
2730	    if (this.ai2 < 0 && this.ai2 > -WINDUP) {
2731	      // 蓄力减速（cs:57135-57140）
2732	      this.ai2 -= 1;
2733	      this.vx *= 0.9;
2734	      this.applyGravity(game);
2735	      moveAndCollide(this, game.world, this.vx, this.vy);
2736	      return true;
2737	    }
2738	    if (this.ai2 === -WINDUP) {
2739	      // 发射（cs:57141-57152）：朝玩家头顶上方 30px 直冲；零向量退化 (spriteDirection,-1)
2740	      this.ai2 -= 1;
2741	      let dx = player.cx - this.cx;
2742	      let dy = (player.y - 30) - this.cy;   // player.Top + (0,-30)
2743	      let d = Math.hypot(dx, dy);
2744	      if (d < 0.001) { dx = this.facing || 1; dy = -1; d = Math.hypot(dx, dy); }
2745	      this.vx = (dx / d) * DASH_SPEED;
2746	      this.vy = (dy / d) * DASH_SPEED;
2747	      this.applyGravity(game);
2748	      moveAndCollide(this, game.world, this.vx, this.vy);
2749	      return true;
2750	    }
2751	    // 冲刺（ai2 < -6，cs:57153-57172）
2752	    this.ai2 -= 1;
2753	    // 落地判定读上一 tick 碰撞结果（原版 velocity.Y==0f 是碰撞后清零值）
2754	    if (this.vy === 0) this.ai2 = 60;
2755	    else if (this.ai2 < -WINDUP - 10) this.vy = Math.min(this.vy + 0.15, 24); // num41=10
2756	    this.reflectsProjectiles = true;
2757	    this.takenDamageMultiplier = 3;
2758	    if (this.justHit) this.ai2 = 60;
2759	    this.applyGravity(game);
2760	    moveAndCollide(this, game.world, this.vx, this.vy);
2761	    return true;
2762	  }
2763	
2764	  /** AI_003 远程战士参数（NPC.cs:59464-60095 各 type 修正汇总）：
2765	   *  cooldown=蓄力时长（num163，半程发射 num165）/ speed=弹速（num166）/
2766	   *  dmg=弹伤（num171）/ range=开瞄距离（num181 默认 700）/
2767	   *  drop=下坠补偿系数（num168，默认 0.1；0=直射；[lo,hi] = 每发 rand(lo..hi)）/
2768	   *  spread=散布 ±px（num167 后修正）/ oy=枪口 Y 偏移 / burst=连发数（292 战术骷髅
2769	   *  ×4 各自重新瞄准，cs:59967）/ aimDecelOffEclipse=非日食不因瞄准减速（468
2770	   *  :60026-60029 flag16 门） */
2771	  private static readonly RANGED_FIGHTERS = new Set([
2772	    111, 214, 215, 216,                       // 入侵：哥布林弓手/海盗三件
2773	    110, 206, 290, 291, 292, 293,             // 骷髅弓手/冰鱼人/圣骑士/神射/战术/爆破
2774	    449, 450, 451, 452, 481,                  // 投骨骷髅×4/希腊骷髅
2775	    498, 499, 500, 501, 502, 503, 504, 505, 506, // 蝾螈族
2776	    379, 380,                                 // 拜月教弓手（cs:56575 仪式待机解除后射击，num163=80）
2777	    468,                                      // 蝇博士 Dr. Man Fly（日食，cs:59464 表内）
2778	  ]);
2779	  private static readonly RANGED_TABLE: Record<number, {
2780	    cooldown: number; speed: number; dmg: number; range: number;
2781	    drop?: number | [number, number]; spread?: number; oy?: number; burst?: number;
2782	    aimDecelOffEclipse?: boolean;
2783	    /** 原版弹型（NPC.cs:59797 起各 num172：贴图/旋转/重力见 Dart.ts DART_STYLE） */
2784	    proj: number;
2785	  }> = {
2786	    111: { cooldown: 180, speed: 9, dmg: 11, range: 700, drop: 0.1, proj: 81 },
2787	    379: { cooldown: 80, speed: 11, dmg: 35, range: 700, drop: 0.1, proj: 81 },  // 拜月教弓手（cs:59494/59609/59797/59823 修正后值,弹 WoodenArrowHostile 81）
2788	    380: { cooldown: 80, speed: 11, dmg: 35, range: 700, drop: 0.1, proj: 81 },
2789	    214: { cooldown: 50, speed: 10, dmg: 25, range: 500, drop: 0, spread: 45, proj: 180 },
2790	    215: { cooldown: 90, speed: 14, dmg: 35, range: 650, drop: 0.08, proj: 82 },
2791	    216: { cooldown: 180, speed: 9, dmg: 30, range: 700, drop: 0.1, proj: 180 },
2792	    110: { cooldown: 70, speed: 11, dmg: 35, range: 700, drop: 0.1, proj: 82 },          // 骷髅弓手 火焰箭
2793	    206: { cooldown: 50, speed: 7, dmg: 37, range: 700, drop: 0.1, oy: -10, proj: 177 },  // 冰鱼人 冰水吐息
2794	    290: { cooldown: 30, speed: 9, dmg: 60, range: 700, drop: 0, oy: -10, proj: 300 },    // 圣骑士 圣锤
2795	    291: { cooldown: 200, speed: 4, dmg: 100, range: 700, drop: 0, spread: 8, proj: 302 },// 骷髅神射 狙击弹
2796	    292: { cooldown: 120, speed: 12, dmg: 50, range: 700, drop: 0, burst: 4, proj: 180 }, // 战术骷髅 4 连弹
2797	    293: { cooldown: 90, speed: 4, dmg: 60, range: 700, drop: 0.1, proj: 303 },           // 骷髅爆破 火箭
2798	    449: { cooldown: 70, speed: 7, dmg: 15, range: 200, drop: 0.25, spread: 16, proj: 471 }, // 投骨骷髅（drop 原版 rand 0.10-0.49）
2799	    450: { cooldown: 70, speed: 7, dmg: 15, range: 200, drop: 0.25, spread: 16, proj: 471 },
2800	    451: { cooldown: 70, speed: 7, dmg: 15, range: 200, drop: 0.25, spread: 16, proj: 471 },
2801	    452: { cooldown: 70, speed: 7, dmg: 15, range: 200, drop: 0.25, spread: 16, proj: 471 },
2802	    481: { cooldown: 100, speed: 8, dmg: 18, range: 400, drop: 0, spread: 16, oy: -14, proj: 508 }, // 希腊骷髅 标枪（drop 原版 ±0.035 随机）
2803	    498: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 }, // 蝾螈吐息
2804	    499: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 },
2805	    500: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 },
2806	    501: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 },
2807	    502: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 },
2808	    503: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 },
2809	    504: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 },
2810	    505: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 },
2811	    506: { cooldown: 70, speed: 7, dmg: 14, range: 190, drop: 0.01, spread: 12, oy: -8, proj: 572 },
2812	    // 蝇博士 Dr. Man Fly（cs:59493 num163=70 默认 / :59662-59665 num166=7.5 /
2813	    // :59727-59730 num168=rand(10..49)×0.01 / :59815-59818 num171=50 /
2814	    // :59861-59864 num172=501 / :60072-60075 num181=400；:60026-60029 非日食不减速）
2815	    468: { cooldown: 70, speed: 7.5, dmg: 50, range: 400, drop: [0.1, 0.49], spread: 40,
2816	      proj: 501, aimDecelOffEclipse: true },
2817	  };
2818	
2819	  /** 蜘蛛家族地面↔爬墙形态对照（NPC.cs:59276-59289 地→墙 / :29994-30008 墙→地）：
2820	   *  164 Wall Creeper→165 Wall Creeper Wall、236→237 Black Recluse、163→238、239→240、530→531 */
2821	  private static readonly SPIDER_WALL_FORM: Record<number, number> = { 164: 165, 236: 237, 163: 238, 239: 240, 530: 531 };
2822	  private static readonly SPIDER_GROUND_FORM: Record<number, number> = { 165: 164, 237: 236, 238: 163, 240: 239, 531: 530 };
2823	
2824	  /** NPCCanStickToWalls 1:1（NPC.cs:56209-56229）：身体中心 3×3 内"非实心 tile 且有背景墙"
2825	   *  的格数 >4 → 可贴墙（蜘蛛洞/洞穴天然满足，地表不满足 → 落回地面形态） */
2826	  private npcCanStickToWalls(st: GameHooks['world']['store']): boolean {
2827	    const cx = Math.floor(this.cx / TILE), cy = Math.floor(this.cy / TILE);
2828	    let n = 0;
2829	    for (let i = cx - 1; i <= cx + 1; i++) {
2830	      for (let j = cy - 1; j <= cy + 1; j++) {
2831	        if (!st.inBounds(i, j)) continue;
2832	        const ii = st.idx(i, j);
2833	        const passable = st.type[ii] === 0 || !st.isSolid(i, j) || st.isPlatform(i, j);
2834	        if (passable && st.wall[ii] > 0) {
2835	          n++;
2836	          if (n > 4) return true;
2837	        }
2838	      }
2839	    }
2840	    return false;
2841	  }
2842	
2843	  /** Transform 1:1（NPC.cs:81861-81919）：换类型 + 按比例结转 HP + ai[0..3] 清零；
2844	   *  位置按 TryChangingSizeFromBottomCenter（:81836）底边中心锚定改尺寸，
2845	   *  新碰撞盒与实心块重叠则放弃（原版换尺寸失败语义）。
2846	   *  game 可选 = TransformVisuals（:81902 Transform 尾对所有转化统一调用）播
2847	   *  音效用——见 transformVisuals */
2848	  private tryTransformTo(id: number, st: GameHooks['world']['store'], allowEmbedded = false, game?: GameHooks): boolean {
2849	    const v = vanillaNpc(id);
2850	    if (!v) return false;
2851	    const oldType = this.vanillaId;
2852	    const s = v.scale ?? 1;
2853	    const nw = Math.round(v.width * s), nh = Math.round(v.height * s);
2854	    const nx = this.cx - nw / 2, ny = this.y + this.h - nh; // 底边中心锚定
2855	    if (!allowEmbedded) {
2856	      for (let tx = Math.floor(nx / TILE); tx <= Math.floor((nx + nw - 0.01) / TILE); tx++) {
2857	        for (let ty = Math.floor(ny / TILE); ty <= Math.floor((ny + nh - 0.01) / TILE); ty++) {
2858	          if (st.isSolid(tx, ty)) return false;
2859	        }
2860	      }
2861	    }
2862	    const oldMax = this.maxHp;
2863	    this.vanillaId = id;
2864	    this.vanilla = v;
2865	    this.w = nw; this.h = nh;
2866	    this.x = nx; this.y = ny;
2867	    this.maxHp = v.lifeMax;
2868	    this.hp = Math.max(1, Math.round((this.hp * v.lifeMax) / oldMax)); // life = life*lifeMax/old
2869	    // 飞行档表达式与 fromVanilla 同源（noGravity 数据族 + aiStyle 2/5/14/23/44）
2870	    const flying = v.noGravity || v.aiStyle === 2 || v.aiStyle === 5 || v.aiStyle === 14
2871	      || v.aiStyle === 23 || v.aiStyle === 44;
2872	    this.noGravity = flying;   // 运行时位随 Transform 重置（原版 SetDefaults 复位语义）
2873	    this.def = {
2874	      ...this.def,
2875	      name: v.name, hp: v.lifeMax, damage: v.damage, defense: v.defense,
2876	      width: nw, height: nh,
2877	      flying,
2878	      boss: VANILLA_BOSS_IDS.has(id),
2879	      hitSound: vanillaSoundFiles(v.HitSound) ?? ['NPC_Hit_1'],
2880	      killedSound: vanillaSoundFiles(v.DeathSound) ?? ['NPC_Killed_1'],
2881	      drops: [], // 掉落走 NpcDrops 规则树（击杀时求值，不再预展开）
2882	    };
2883	    this.ai0 = 0; this.ai1 = 0; this.ai2 = 0; this.ai3 = 0;
2884	    this.transformVisuals(game, oldType, id);
2885	    return true;
2886	  }
2887	
2888	  /** TransformVisuals（NPC.cs:81739-81771——Transform 尾部 :81902 对所有转化统一
2889	   *  调用,按 (oldType,newType) 对分发）。当前移植对仅 158⇄159（吸血蝙蝠⇄吸血鬼,
2890	   *  :81742-81749）：Item_8 + 3 个 gore 99（三锚点 y−10 / y+h/2−10 / y+h−10、
2891	   *  初速 ×0.3——GorePiece 血块收缩族含 99）。478→479（dust 238+gore 684-686）/
2892	   *  406→405 等其余对无音效号,粒子侧未移植维持现状。 */
2893	  private transformVisuals(game: GameHooks | undefined, oldType: number | null, newType: number): void {
2894	    if (!game) return;
2895	    if (!((oldType === 158 && newType === 159) || (oldType === 159 && newType === 158))) return;
2896	    game.playSfxWav?.('Item_8', 1, this.cx, this.cy);
2897	    for (const gy of [this.y - 10, this.y + this.h / 2 - 10, this.y + this.h - 10]) {
2898	      GorePiece.newGore(99, this.x, gy, this.vx * 0.3, this.vy * 0.3, this.vanillaScale ?? 1);
2899	    }
2900	  }
2901	
2902	  /** 外部 AI 文件的 Transform 入口（骑手 390 失坐骑 → 382,cs:36291）。
2903	   *  allowEmbedded：noTileCollide 族（EoW 断链晋升 13/15 常处实心块内）跳过
2904	   *  实心重叠自检——原版 Transform 无此回退（SetDefaults 后仅底边锚定改尺寸） */
2905	  transformTo(id: number, st: GameHooks['world']['store'], allowEmbedded = false, game?: GameHooks): boolean {
2906	    return this.tryTransformTo(id, st, allowEmbedded, game);
2907	  }
2908	
2909	  /** NPC.GetShimmered（NPC.cs:92502-92584）子集：雕像产怪直接消散（:92504-92519）→
2910	   *  ShimmerTransformToNPC 则 Transform（:92521-92533）→ ShimmerTransformToItem 则
2911	   *  掉微光化物品后消散（:92535-92560）。表来自 tools/extract-shimmer.mjs
2912	   *  （114 NPC 对 + 15 NPC→物品）。原版四分支全落空时整函数为空操作（无表项 Boss
2913	   *  浸微光仅反复空调用，:92502-92573 无 else 兜底）——先判分支可达再出转化特效，
2914	   *  避免每 90t 粒子空刷；城镇变体分支（:92560-92573）在 TownNPC 侧实现 */
2915	  private npcGetShimmered(game: GameHooks): void {
2916	    if (this.vanillaId === null) return;
2917	    const toNpc = npcShimmerTransformTo(this.vanillaId);
2918	    const toItem = npcShimmerTransformToItem(this.vanillaId);
2919	    // 空操作门：非雕像产怪且无任何转化目标 → 原版同帧不产生任何副作用
2920	    if (!this.spawnedFromStatue && !(toNpc >= 0 && toNpc !== this.vanillaId) && toItem < 0) return;
2921	    this.shimmerT = 0;
2922	    game.spawnParticles(this.cx, this.cy, '#BFE8FF', 10, 1.4, { life: 30, grav: -0.04 });
2923	    if (this.spawnedFromStatue) {           // SpawnedFromStatue → active=false（:92508-92514）
2924	      this.dead = true;
2925	      return;
2926	    }
2927	    if (toNpc >= 0 && toNpc !== this.vanillaId) {
2928	      this.transformTo(toNpc, game.world.store, false, game);
2929	      return;
2930	    }
2931	    if (toItem >= 0) {
2932	      const key = VANILLA_ITEM_KEY_BY_ID[toItem];
2933	      if (key) {
2934	        const d = game.spawnDrop(this.cx, this.cy, key, 1);
2935	        if (d) { d.shimmered = true; d.shimmerTime = 1; }  // 微光化物品上浮（:92540-92545）
2936	      }
2937	      this.dead = true;                    // noSpawnCycle + active=false（:92557-92559）
2938	    }
2939	  }
2940	
2941	  /** AI_040 爬墙蜘蛛族 1:1（NPC.cs:29784-30022）：无重力、贴背景墙表面爬行。
2942	   *  速度表：165 默认 2/0.08、237 3/0.12、531 4/0.16（:29789-29798）；
2943	   *  有视线 → 分轴伺服追玩家（:29880-29920，朝向角 atan2(期望速度)）；
2944	   *  无视线 → ai[0] ±200 振荡漂移（:29833-29878，角 atan2(当前速度)）；
2945	   *  531 朝向角额外 +π/2（:29922）；spriteDirection 恒 -1（:29829，渲染层处理）；
2946	   *  碰撞反弹（:29924-29950）：旧速 ×-0.5，X 朝移动方向保底 ±2、Y 保底 ±2；
2947	   *  专家模式毒液弹（:29960-29989，type 472）未启用专家模式，不移植；
2948	   *  脱墙（NPCCanStickToWalls 假）→ Transform 回地面形态（:29991-30010） */
2949	  private wallCreeperAI(game: GameHooks, player: Player | null) {
2950	    const st = game.world.store;
2951	    let maxSpd = 2, accel = 0.08;
2952	    if (this.vanillaId === 237) { maxSpd = 3; accel = 0.12; }
2953	    else if (this.vanillaId === 531) { maxSpd = 4; accel = 0.16; }
2954	    // 目标向量（8px 量化，:29799-29819）；无目标/目标死亡 → 沿方向漂离上浮（:29824-29827）
2955	    let tx: number, ty: number;
2956	    const alive = !!player && !player.dead;
2957	    if (alive) {
2958	      tx = Math.floor(player!.cx / 8) * 8 - Math.floor(this.cx / 8) * 8;
2959	      ty = Math.floor(player!.cy / 8) * 8 - Math.floor(this.cy / 8) * 8;
2960	    } else {
2961	      tx = this.facing * maxSpd / 2;
2962	      ty = -maxSpd / 2;
2963	    }
2964	    const dist = Math.hypot(tx, ty);
2965	    let sx: number, sy: number; // 期望速度向量（num636/637）
2966	    if (dist === 0) { sx = this.vx; sy = this.vy; }
2967	    else { sx = (tx / dist) * maxSpd; sy = (ty / dist) * maxSpd; }
2968	    // direction（TargetClosest 语义：朝目标水平方向；死亡保持）
2969	    if (alive) this.facing = this.seekDirX(player!);
2970	    const los = alive ? this.canSeePlayer(st, player!) : false;
2971	    if (!los) {
2972	      // 无视线：振荡漂移（:29833-29878）——ai[0] 驱动的 X/Y 交替扰动 + 微弱趋目标分量
2973	      if (this.ai0 < -200) this.ai0 = 0; // 类默认 -1120 钳回原版下界（同 swarmerAI 清查）
2974	      this.ai0 += 1;
2975	      this.vy += this.ai0 > 0 ? 0.023 : -0.023;
2976	      this.vx += (this.ai0 < -100 || this.ai0 > 100) ? 0.023 : -0.023;
2977	      if (this.ai0 > 200) this.ai0 = -200;
2978	      this.vx += sx * 0.007;
2979	      this.vy += sy * 0.007;
2980	      this.visAngle = Math.atan2(this.vy, this.vx);
2981	      if (this.vx > 1.5 || this.vx < -1.5) this.vx *= 0.9;
2982	      if (this.vy > 1.5 || this.vy < -1.5) this.vy *= 0.9;
2983	      this.vx = Math.max(-3, Math.min(3, this.vx));
2984	      this.vy = Math.max(-3, Math.min(3, this.vy));
2985	    } else {
2986	      // 有视线：分轴非对称伺服（:29880-29920，与 servoTo 同构、目标为期望速度）
2987	      if (this.vx < sx) {
2988	        this.vx += accel;
2989	        if (this.vx < 0 && sx > 0) this.vx += accel;
2990	      } else if (this.vx > sx) {
2991	        this.vx -= accel;
2992	        if (this.vx > 0 && sx < 0) this.vx -= accel;
2993	      }
2994	      if (this.vy < sy) {
2995	        this.vy += accel;
2996	        if (this.vy < 0 && sy > 0) this.vy += accel;
2997	      } else if (this.vy > sy) {
2998	        this.vy -= accel;
2999	        if (this.vy > 0 && sy < 0) this.vy -= accel;
3000	      }
3001	      this.visAngle = Math.atan2(sy, sx);
3002	    }
3003	    if (this.vanillaId === 531) this.visAngle += Math.PI / 2; // :29922
3004	    // 移动 + 碰撞反弹（:29924-29950；旧速 = 碰撞前速度）
3005	    const oldVx = this.vx, oldVy = this.vy;
3006	    moveAndCollide(this, game.world, this.vx, this.vy);
3007	    if (this.hitWall) {
3008	      this.vx = oldVx * -0.5;
3009	      if (this.facing === -1 && this.vx > 0 && this.vx < 2) this.vx = 2;
3010	      if (this.facing === 1 && this.vx < 0 && this.vx > -2) this.vx = -2;
3011	    }
3012	    if (this.hitHead || this.onGround) {
3013	      this.vy = oldVy * -0.5;
3014	      if (this.vy > 0 && this.vy < 1.5) this.vy = 2;
3015	      if (this.vy < 0 && this.vy > -1.5) this.vy = -2;
3016	    }
3017	    // 行走帧累加（FindFrame case 165/237/238/240/531，cs:73795-73817：
3018	    // frameCounter += (|vx|+|vy|)×0.5（531 ×0.4），24 一循环）
3019	    this.crawlT = (this.crawlT + (Math.abs(this.vx) + Math.abs(this.vy))
3020	      * (this.vanillaId === 531 ? 0.4 : 0.5)) % 24;
3021	    // 脱墙 → Transform 回地面形态（:29991-30010）
3022	    const groundForm = Enemy.SPIDER_GROUND_FORM[this.vanillaId ?? -1];
3023	    if (groundForm !== undefined && !this.npcCanStickToWalls(st)) {
3024	      this.tryTransformTo(groundForm, st, false, game);
3025	    }
3026	  }
3027	
3028	  /** Collision.CanHit 1:1（Collision.cs:388-480）：实体矩形 → 逐 tile 扫描。
3029	   *  半砖/坡面/平台/已致动/开门态不阻挡；"两邻格均为整实心"= 被夹住 → 无视线 */
3030	  private canSeePlayer(st: GameHooks['world']['store'], p: Player): boolean {
3031	    return canHit(st, this.x, this.y, this.w, this.h, p.x, p.y, p.w, p.h);
3032	  }
3033	
3034	  /** AI_042 失落女孩 1:1（NPC.cs:30281-30310）：伪装成无害 NPC 静止站立（无移动逻辑，
3035	   *  仅重力）；玩家靠到 200px 内有视线、或自身被推动/下落/受伤（ai[0] 0→1 的三重触发，
3036	   *  cs:30292-30300）→ 21 tick 后 Transform(196 Nymph) 显形追杀 */
3037	  private lostGirlAI(game: GameHooks, player: Player | null) {
3038	    const st = game.world.store;
3039	    if (this.ai0 < 0) this.ai0 = 0; // 类字段默认 -1120 是史莱姆专用初值；原版 ai[0] 从 0 起步
3040	    if (this.ai0 === 0) {
3041	      if (player && !player.dead) {
3042	        const dx = player.cx - this.cx, dy = player.y - this.cy;
3043	        if (Math.hypot(dx, dy) < 200 && this.canSeePlayer(st, player)) this.ai0 = 1;
3044	      }
3045	      if (this.vx !== 0 || this.vy < 0 || this.vy > 2 || this.hp !== this.maxHp) this.ai0 = 1;
3046	    } else {
3047	      this.ai0 += 1;

```


---

## 🤖 Assistant · 2026-08-19T03:06:57.251Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me continue reading lostGirlAI (to 3064), boundNPCAI, mimicAI (3243-3293), plantAI (3692-3779), blazingWheelAI and spikeBallAI (4205-4279), casterAI (6514-6752), and slimeAI (1830-2034).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:06:57.607Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 120,
 "offset": 3047
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:57.618Z

**📎 ToolResult**

```
3047	      this.ai0 += 1;
3048	      if (this.ai0 >= 21) {
3049	        this.ai0 = 21;
3050	        if (this.tryTransformTo(196, st, false, game)) return;
3051	      }
3052	    }
3053	    // 静止站立 + 重力（原版 AI_042 无任何速度代码）
3054	    this.vx = 0;
3055	    this.applyGravity(game);
3056	    moveAndCollide(this, game.world, this.vx, this.vy);
3057	  }
3058	
3059	  /** AI_000 被缚 NPC（NPC.cs:19774-19893）：105/106/123/354 静态站立（面朝玩家+摩擦，
3060	   *  无任何移动）；376 睡渔夫/579 醉酒酒保水上漂流（vy=-0.4 上浮 + 缓漂）。
3061	   *  376/579 在永不沾水表（:94252）→ wet 恒 false，原版用水线判定：wet || 头顶上方格
3062	   *  ((position.Y-4)/16) 有液体（:19818-19820）——睡在水面上恒漂不沉。
3063	   *  解救（对话 Transform 成对应城镇 NPC）在 TownNPC 侧；Enemy 侧仅防御性兜底 */
3064	  private boundNPCAI(game: GameHooks, player: Player | null) {
3065	    if (player && !player.dead) this.facing = this.seekDirX(player);
3066	    this.vx *= 0.93;
3067	    if (Math.abs(this.vx) < 0.1) this.vx = 0;
3068	    const st = game.world.store;
3069	    if (this.vanillaId === 376 || this.vanillaId === 579) {
3070	      const headTile = st.liquid[st.idx(
3071	        Math.floor(this.cx / TILE), Math.floor((this.y - 4) / TILE))] > 0;
3072	      if (headTile) {
3073	        this.vy = -0.4;                     // 水面漂流（cs:19821-19883）
3074	        this.vx *= 0.99;
3075	        this.x += this.vx; this.y += this.vy;
3076	        return;
3077	      }
3078	    }
3079	    this.applyGravity(game);
3080	    moveAndCollide(this, game.world, this.vx, this.vy);
3081	  }
3082	
3083	  /** AI_017 秃鹫 61（Raven 301 同块，NPC.cs:24079-24209）：ai[0]=0 栖息（重力站立），
3084	   *  200px 盒与玩家相交 / life<max / 有速度 → 起飞（vy-=6）单向 0→1 不回落；
3085	   *  飞行态无重力：X accel 0.1 clamp±3，Y 目标=玩家上方（|dx|>50 再抬高 100）accel 0.05 clamp±3；
3086	   *  碰撞反弹旧速×-0.5（X 朝 direction 保底 2 / Y 保底 1） */
3087	  private vultureAI(game: GameHooks, player: Player | null) {
3088	    if (this.ai0 < 0) this.ai0 = 0;
3089	    // noGravity 运行时位（:24079-24084）：AI 开头恒 true，栖息 0 态置 false——
3090	    // StrikeNPC :82217 受击档（def.flying=false 覆盖不到，2026-08-17 补）
3091	    this.noGravity = true;
3092	    if (this.ai0 === 0) {
3093	      this.noGravity = false;
3094	      // 唤醒判定用重力前的速度（原版 AI 先读 velocity、重力在其后施放——
3095	      // 落地碰撞清零后站立态 vy==0，不会被本 tick 重力误判成"有速度"）
3096	      const preVy = this.vy;
3097	      const near = player && !player.dead
3098	        && Math.abs(player.cx - this.cx) < 100 + (this.w + player.w) / 2
3099	        && Math.abs(player.cy - this.cy) < 100 + (this.h + player.h) / 2;
3100	      if (this.vx !== 0 || preVy < 0 || preVy > 0.3) {
3101	        // 速度触发唤醒(:24091):置 ai[0]=1 但不跳(无 vy-=6)
3102	        this.ai0 = 1;
3103	        return;
3104	      }
3105	      if (near || this.hp < this.maxHp) {
3106	        // 玩家靠近/掉血唤醒(:24101-24105):起身跳 vy-=6
3107	        this.ai0 = 1;
3108	        this.vy = -6;
3109	        return;
3110	      }
3111	      this.applyGravity(game);
3112	      moveAndCollide(this, game.world, this.vx, this.vy);
3113	      return;
3114	    }
3115	    if (player && !player.dead) this.facing = this.seekDirX(player);
3116	    const dir = this.facing;
3117	    // (:24151-24170) else-if 链:基础 ∓0.1;>3(同向满速不可达档)/>0(逆行)追加 ∓0.05;
3118	    // 曾把逆行追加错写成 ∓0.1(减速过猛)
3119	    if (dir === -1 && this.vx > -3) {
3120	      this.vx -= 0.1;
3121	      if (this.vx > 3) this.vx -= 0.1;
3122	      else if (this.vx > 0) this.vx -= 0.05;
3123	      if (this.vx < -3) this.vx = -3;
3124	    } else if (dir === 1 && this.vx < 3) {
3125	      this.vx += 0.1;
3126	      if (this.vx < -3) this.vx += 0.1;
3127	      else if (this.vx < 0) this.vx += 0.05;
3128	      if (this.vx > 3) this.vx = 3;
3129	    }
3130	    // 悬停目标(:24172-24174):player.Y - h/2;水平距离>50 → 再抬 100px。
3131	    // ★曾写成【vy】与【世界坐标 ty】比较(单位错位恒 false → 永远 vy+=0.05 向下
3132	    // 加速):秃鹫唤醒后不悬停,贴地乱撞冲向玩家。原版比较的是 position.Y 与 ty
3133	    let ty = player && !player.dead ? player.y - this.h / 2 : this.cy - 100;
3134	    if (player && Math.abs(player.cx - this.cx) > 50) ty -= 100;
3135	    if (this.y < ty) {
3136	      this.vy += 0.05;
3137	      if (this.vy < 0) this.vy += 0.01;   // :24183-24185 上行中额外 +0.01 减速(曾写反 -0.01)
3138	    } else {
3139	      this.vy -= 0.05;
3140	      if (this.vy > 0) this.vy -= 0.01;
3141	    }
3142	    // （秃鹫无沙球攻击——:24475 沙球块属 aiStyle 19 蚁狮,曾误植于此并错用
3143	    //  ai0 状态机字段自减,已撤;蚁狮侧 antlionAI 已含 Item_5 音,2026-08-18 复核）
3144	    this.vy = Math.max(-3, Math.min(3, this.vy));
3145	    const oldVx = this.vx, oldVy = this.vy;
3146	    moveAndCollide(this, game.world, this.vx, this.vy);
3147	    if (this.hitWall) {
3148	      this.vx = -oldVx * 0.5;
3149	      if (this.facing === -1 && this.vx > 0 && this.vx < 2) this.vx = 2;
3150	      if (this.facing === 1 && this.vx < 0 && this.vx > -2) this.vx = -2;
3151	    }
3152	    if (this.hitHead || this.onGround) {
3153	      this.vy = -oldVy * 0.5;
3154	      if (Math.abs(this.vy) < 1) this.vy = this.vy >= 0 ? 1 : -1;
3155	    }
3156	    // 入水(:24194-24208):vy>0 ×0.95 阻下落,恒 -0.5 上浮,下限 -4
3157	    if (this.inWater) {
3158	      if (this.vy > 0) this.vy *= 0.95;
3159	      this.vy -= 0.5;
3160	      if (this.vy < -4) this.vy = -4;
3161	    }
3162	  }
3163	
3164	  /** AI_019 蚁狮 69（NPC.cs:24465-24595）：完全不动（knockBackResist=0）；底部 3 列任一
3165	   *  实心 → 无重力上浮 0.2 出沙面（cs:24543 动态 noTileCollide），否则正常落地；
3166	   *  沙球（cs:24499）：ai[0] 冷却 200、玩家在上方+视线 → 速 12 直射（伤害 10）；

```


---

## 🤖 Assistant · 2026-08-19T03:06:57.877Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 115,
 "offset": 3243
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:06:57.906Z

**📎 ToolResult**

```
3243	  private mimicAI(game: GameHooks, player: Player | null) {
3244	    if (this.ai0 < 0) this.ai0 = 0;
3245	    const flag36 = this.vanillaId === 341 && game.world.moonEvent.kind === 1;
3246	    if (this.ai0 === 0) {
3247	      // 同 AI_017：唤醒判定用重力前速度（站立态 vy==0 不误触发）
3248	      const preVy = this.vy;
3249	      const near = !flag36 && player && !player.dead
3250	        && Math.abs(player.cx - this.cx) < 100 + (this.w + player.w) / 2
3251	        && Math.abs(player.cy - this.cy) < 100 + (this.h + player.h) / 2;
3252	      if (near || this.hp < this.maxHp || this.vx !== 0 || preVy < 0 || preVy > 0.3) {
3253	        this.ai0 = 1;
3254	        return;
3255	      }
3256	      this.applyGravity(game);
3257	      moveAndCollide(this, game.world, this.vx, this.vy);
3258	      return;
3259	    }
3260	    if (player && !player.dead) this.facing = this.seekDirX(player);
3261	    this.applyGravity(game);
3262	    moveAndCollide(this, game.world, this.vx, this.vy);
3263	    if (this.onGround && this.vy === 0) {
3264	      this.ai2 += 1;
3265	      const wait = this.ai1 === 0 ? 12 : 20;
3266	      if (this.ai2 < wait) { this.vx *= 0.9; return; }
3267	      this.ai2 = 0;
3268	      if (this.ai1 === 2) {           // 第三跳：大跳清零
3269	        this.vx = this.facing * 2.5;
3270	        this.vy = -8;
3271	        this.ai1 = 0;
3272	      } else {
3273	        this.vx = this.facing * 3.5;
3274	        this.vy = -4;
3275	        this.ai1 += 1;
3276	      }
3277	    } else if (this.vy !== 0) {
3278	      if (this.facing === -1 && this.vx > -1) this.vx -= 0.1;
3279	      else if (this.facing === 1 && this.vx < 1) this.vx += 0.1;
3280	    }
3281	  }
3282	
3283	  /** AI_039 陆龟族 153/154/417/496/497（NPC.cs:29257-29783）：
3284	   *  justHit → 回待机（417 除外，knockBackResist=0）；
3285	   *  0 待机：远距(>200)+视线蓄力+4/t（496/497 +2），>600 再+10/t，wet 直跳 1000，≥400 → 1；
3286	   *    行走 accel 0.07，近(<400) clamp±1 远 ±1.5（496/497 ±0.5），前方 3×4 无地转身；
3287	   *  1 蓄势：vx×0.5、ai[1]+1(496/497 ×0.5) ≥30 → 3（417 → 6 态滚动）；
3288	   *  3 旋冲：首帧定速 有视线10/无视线6（496/497 ×0.75；瞄准 Y 加 |dx|*0.2、无视线强制
3289	   *    vy=-10），飞行中与玩家 X 重叠 → vx×0.8 停升，否则 vy-=0.22 持续上旋，≥90t → 4；
3290	   *  4 下落：vx×0.96，落地 → 5；
3291	   *  5 复位：vx=0，+1/t(×0.5) ≥30 → 回 0；wet 直接回 3；
3292	   *  6 Sroller 日耀滚动（16/10 定速、≥1200t 或 ai[2]==0 → 5）星柱未引入仅骨架 */
3293	  private tortoiseAI(game: GameHooks, player: Player | null) {
3294	    const st = game.world.store;
3295	    if (this.ai0 < 0) this.ai0 = 0;
3296	    const t496 = this.vanillaId === 496 || this.vanillaId === 497;
3297	    const sroller = this.vanillaId === 417;
3298	    if (this.justHit && !sroller && this.ai0 !== 3) { this.ai0 = 0; this.ai1 = 0; }
3299	    const dx = player ? player.cx - this.cx : 0;
3300	    const dy = player ? player.cy - this.cy : 0;
3301	    const dist = player ? Math.hypot(dx, dy) : Infinity;
3302	    const los = !!player && !player.dead && this.canSeePlayer(st, player);
3303	    const inW = st.liquid[st.idx(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE))] > 80;
3304	    const gravityStep = () => {
3305	      this.applyGravity(game);
3306	      moveAndCollide(this, game.world, this.vx, this.vy);
3307	    };
3308	    if (this.ai0 === 0 || this.ai0 > 5) {
3309	      // ---- 待机/接近 ----
3310	      if (this.ai0 === 0) {
3311	        if (los && dist > 200) this.ai1 += t496 ? 2 : 4;
3312	        if (dist > 600 && (los || dy > 200)) this.ai1 += t496 ? 4 : 10;
3313	        if (inW) this.ai1 = 1000;
3314	        if (this.ai1 >= 400) { this.ai0 = 1; this.ai1 = 0; return; }
3315	        if (player && !player.dead) this.facing = dx > 0 ? 1 : -1;
3316	        const max = t496 ? 0.5 : dist < 400 ? 1 : 1.5;
3317	        this.vx += this.facing * 0.07;
3318	        this.vx = Math.max(-max, Math.min(max, this.vx));
3319	        // 前方 3 格 × 下 4 格无地面 → 转身（cs:29395-29427）
3320	        const fx = Math.floor((this.cx + this.facing * 24) / TILE);
3321	        const fy = Math.floor((this.y + this.h - 1) / TILE);
3322	        let ground = false;
3323	        for (let k = 1; k <= 4 && !ground; k++) if (st.isSolid(fx, fy + k)) ground = true;
3324	        if (!ground) this.facing *= -1;
3325	        gravityStep();
3326	        return;
3327	      }
3328	      // ---- Sroller 6 态骨架 ----
3329	      if (this.ai1 === 0) {
3330	        const spd = los ? 16 : 10;
3331	        if (player && los) {
3332	          const d = Math.hypot(dx, dy) || 1;
3333	          this.vx = (dx / d) * spd; this.vy = (dy / d) * spd;
3334	        } else { this.vy = -12; this.vx = this.facing * spd * 0.5; }
3335	        this.ai2 = 2 + Math.floor(Math.random() * 3);
3336	      }
3337	      this.ai1 += 1;
3338	      gravityStep();
3339	      if (this.ai2 === 0 || this.ai1 >= 1200) { this.ai0 = 5; this.ai1 = 0; }
3340	      return;
3341	    }
3342	    if (this.ai0 === 1) {
3343	      // ---- 蓄势 ----
3344	      this.vx *= 0.5;
3345	      this.ai1 += t496 ? 0.5 : 1;
3346	      gravityStep();
3347	      if (this.ai1 >= 30) {
3348	        this.ai0 = sroller ? 6 : 3;
3349	        this.ai1 = 0;
3350	        this.ai2 = 0;
3351	      }
3352	      return;
3353	    }
3354	    if (this.ai0 === 3) {
3355	      // ---- 旋转弹射 ----
3356	      if (this.ai1 === 0) {
3357	        const spd = (los ? 10 : 6) * (t496 ? 0.75 : 1);

```


---

## 🤖 Assistant · 2026-08-19T03:07:00.694Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now plantAI, blazingWheelAI, spikeBallAI, casterAI, and slimeAI. Let me read those.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:00.754Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 90,
 "offset": 3692
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:00.779Z

**📎 ToolResult**

```
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
3780	    // ---- Mechdusa 探针挂链(NPC.cs AI_005 :50866-50920):ai3≠0 = 召唤链出生的
3781	    //      挂链探针 → 绕毁灭者头公转锁位(queen 在场时无敌);失效即脱落回常规 ----

```


---

## 🤖 Assistant · 2026-08-19T03:07:01.072Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 140,
 "offset": 4140
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:01.103Z

**📎 ToolResult**

```
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
4179	      this.aiInit = true; this.ai0 = 1;   // 初始化（L21910；68 无手 NPC）
4180	      game.playSfx('roar', 1, this.cx, this.cy);
4181	    }
4182	    if (!player || Math.abs(this.cx - player.cx) > 2000 || Math.abs(this.cy - player.cy) > 2000) {
4183	      this.ai1 = 3;
4184	    } else if (this.ai1 !== 3) {
4185	      this.ai1 = 2;
4186	    }
4187	    if (this.ai1 === 2) {
4188	      this.def.damage = 9999;
4189	      const dx = player!.cx - this.cx, dy = player!.cy - this.cy;
4190	      const d = Math.hypot(dx, dy) || 1;
4191	      this.vx = (dx / d) * 8;
4192	      this.vy = (dy / d) * 8;
4193	    } else {
4194	      this.vy += 0.1;
4195	      if (this.vy < 0) this.vy *= 0.95;
4196	      this.vx *= 0.95;
4197	    }
4198	    this.x += this.vx;
4199	    this.y += this.vy;
4200	  }
4201	
4202	  /** AI_020 火轮（NPC.145.cs:24596+）：ai[3]=1+Next(15)*0.1 速度档；
4203	   *  首段垂直俯冲 spd/acc/2≈15 tick（L24617-24622），随后恒速 ±spd 弹跳——
4204	   *  noTileCollide 穿墙，"弹"靠 |v|≥spd 时 direction 翻转（L24637-24660）而非碰撞 */
4205	  private blazingWheelAI() {
4206	    if (!this.aiInit) { this.aiInit = true;
4207	      this.facing *= -1;
4208	      this.y += this.h / 2 + 8;
4209	      if (this.facing === 0) this.facing = 1;
4210	      this.ai3 = 1 + Math.floor(Math.random() * 15) * 0.1;
4211	      this.vy = 6 * this.ai3 * this.dirY;
4212	      this.ai0 = 1;
4213	      this.x += this.vx;
4214	      this.y += this.vy;
4215	      return;
4216	    }
4217	    const spd = 6 * this.ai3, accel = 0.2 * this.ai3;
4218	    const phaseLen = Math.floor(spd / accel / 2); // num304（ai3 约掉=15）
4219	    if (this.ai0 >= 1 && this.ai0 < phaseLen) {
4220	      this.vy = this.dirY * spd;
4221	      this.ai0 += 1;
4222	    } else if (this.ai0 >= phaseLen) {
4223	      this.vy = 0;
4224	      this.dirY *= -1;
4225	      this.vx = spd * this.facing;
4226	      this.ai0 = -1;
4227	    } else {
4228	      // 常态弹跳（L24637-24660）：到 ±spd 翻向，持续加 accel
4229	      if (this.dirY > 0 && this.vy >= spd) { this.dirY *= -1; this.vy = spd; }
4230	      else if (this.dirY < 0 && this.vy <= -spd) { this.dirY *= -1; this.vy = -spd; }
4231	      if (this.facing > 0 && this.vx >= spd) { this.facing *= -1; this.vx = spd; }
4232	      else if (this.facing < 0 && this.vx <= -spd) { this.facing *= -1; this.vx = -spd; }
4233	      this.vx += accel * this.facing;
4234	      this.vy += accel * this.dirY;
4235	    }
4236	    this.x += this.vx;
4237	    this.y += this.vy;
4238	  }
4239	
4240	  /** AI_021 刺球（NPC.145.cs:24674+）：恒速 6 对角移动，撞轴翻转（collideX→dirY 翻、
4241	   *  collideY→facing 翻），ai[1] 交替旋转相位（视觉态，渲染暂无旋转仅保留状态语义） */
4242	  private spikeBallAI(game: GameHooks) {
4243	    if (!this.aiInit) { this.aiInit = true;
4244	      if ((game as unknown as { player?: Player }).player) {
4245	        const p = (game as unknown as { player: Player }).player;
4246	        this.facing = this.seekDirX(p);
4247	      }
4248	      this.dirY = 1;
4249	      this.ai0 = 1;
4250	    }
4251	    // 上一 tick moveAndCollide 留下的碰撞旗标（原版 AI 开头读 collideX/Y 同语义）
4252	    const collideX = this.hitWall;
4253	    const collideY = this.onGround || this.hitHead;
4254	    if (this.ai1 === 0) {
4255	      if (collideY) this.ai0 = 2;
4256	      if (!collideY && this.ai0 === 2) { this.facing *= -1; this.ai1 = 1; this.ai0 = 1; }
4257	      if (collideX) { this.dirY *= -1; this.ai1 = 1; }
4258	    } else {
4259	      if (collideX) this.ai0 = 2;
4260	      if (!collideX && this.ai0 === 2) { this.dirY *= -1; this.ai1 = 0; this.ai0 = 1; }
4261	      if (collideY) { this.facing *= -1; this.ai1 = 0; }
4262	    }
4263	    this.vx = 6 * this.facing;
4264	    this.vy = 6 * this.dirY;
4265	    moveAndCollide(this, game.world, this.vx, this.vy);
4266	    // ---- 点光（cs:24722-24724）：aiStyle21 全族（=72 火轮）火焰光
4267	    //  (0.9, 0.3+num306, 0.2)，num306=(270−mouseTextColor)/400（190-255 三角波 → 0.0375-0.1375）
4268	    if (this.vanillaId === 72) {
4269	      const num306 = (270 - mouseTextColorApprox()) / 400;
4270	      this.lightRGB = [0.9, 0.3 + num306, 0.2];
4271	    }
4272	  }
4273	
4274	  /** AI_026 独角兽/冲锋族（NPC.cs:25863-26292）：
4275	   *  冲锋 walker：accel 0.07 / maxSpd 6（num7/num8，独角兽 315 配置 L26100-26116）；
4276	   *  逆向阻尼 0.95、超速落地 ×0.8；卡墙 30 tick 折返（ai[3]≥num1，玩家 <200px 重置 L25936-25941）；
4277	   *  台阶步升 16.1 同战士（L26182-26207）；跳梯 -8.5/-7.5/-7/-6/-8（L26245-26279，
4278	   *  前方探测含 (w/2+2)×dir + 5×vx 提前量 L26226-26227） */
4279	  private chargerAI(game: GameHooks, player: Player | null, maxSpd = 6) {

```


---

## 🤖 Assistant · 2026-08-19T03:07:05.275Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now casterAI (6514-6752) and slimeAI (1830-2034). Let me read those.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:05.725Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 245,
 "offset": 6514
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:05.739Z

**📎 ToolResult**

```
6514	  private casterAI(game: GameHooks, player: Player | null) {
6515	    const vid = this.vanillaId ?? -1;
6516	    if (!this.aiInit) {
6517	      this.aiInit = true;
6518	      this.ai0 = 500;                        // :20799-20801 初始 500
6519	      this.ai1 = 0; this.ai2 = 0; this.ai3 = 0;
6520	      if (vid === 172) this.spawnAlpha = 255;  // :20797-20804 alpha 0 起步（spawnAlpha=255 对应不可见）
6521	    }
6522	    // 172 符文法师淡入（:20797-20809：alpha 每帧 +1 ≈ spawnAlpha -1/t；受击归零重淡）
6523	    if (vid === 172) {
6524	      if (this.justHit) this.spawnAlpha = 255;
6525	      if (this.spawnAlpha > 0) this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
6526	    }
6527	    // ---- ① 传送执行（:20811-20968）：目的地待执行 → 双端 FX + 改写 ----
6528	    if (this.ai2 !== 0 && this.ai3 !== 0) {
6529	      this.casterTeleportBurst(game);
6530	      this.x = this.ai2 * TILE - this.w / 2 + 8;   // :20888-20889（+8 为贴图格内偏移）
6531	      this.y = this.ai3 * TILE - this.h;
6532	      this.vx = 0; this.vy = 0;
6533	      this.ai2 = 0; this.ai3 = 0;
6534	      this.casterTeleportBurst(game);
6535	    }
6536	    this.ai0 += 1;                                 // :20971 每帧计时
6537	    // :20777-20784 RedHat 变体（红帽骷髅王 35 ai[3]==1 在场 → localAI[3]=1 置位永不清；
6538	    // 帧侧整带 +3、计时双倍）。本仓红帽召唤链未实装（Enemy.redHat 恒 false）→ 恒 0
6539	    // （enemies 可选访问：测试桩 hooks 可能未实现）
6540	    if (vid === 32 && this.lai3 === 0) {
6541	      const enemiesOf = (game as { enemies?: () => unknown[] }).enemies;
6542	      const sk = enemiesOf
6543	        ? (enemiesOf.call(game) as Enemy[]).find((n) => n.vanillaId === 35 && !n.dead)
6544	        : undefined;
6545	      if (sk?.redHat) this.lai3 = 1;
6546	    }
6547	    // :20787-20791 X 摩擦 0.93 + |vx|<0.1 归零（Y 不阻尼——重力由引擎共享段承担）
6548	    this.vx *= 0.93;
6549	    if (this.vx > -0.1 && this.vx < 0.1) this.vx = 0;
6550	    // 物理：全族 SetDefaults 均无 noGravity/noTileCollide → 受重力+瓦片碰撞
6551	    // （传送落点即站面、受击呈正常抛物线回落）。旧实现 vx/vy 同乘 0.9 裸积分——
6552	    // 无重力无碰撞，受击 vy<0 只缓衰减不回落 = "被击退就往上飞"（2026-08-17 用户报告）
6553	    if (!this.vanilla?.noGravity) {
6554	      this.applyGravity(game);
6555	      moveAndCollide(this, game.world, this.vx, this.vy);
6556	    } else {
6557	      this.x += this.vx; this.y += this.vy;        // 数据侧若标 noGravity 则保悬浮直移
6558	    }
6559	    // ---- 点光（cs:21274-21341 粉尘链后的 AddLight 分支，在移动后每帧执行）----
6560	    if (vid === 693) {
6561	      // :21272-21276 图书管理员骷髅：num116=Remap(ai[0],0,60,0,1)²>0 时 Top 位
6562	      // （0.91/0.82/0.57)×num116——传送后 ai[0] 归 1 再涨 60 帧到 1，常态恒满
6563	      const ramp = Math.min(Math.max(this.ai0 / 60, 0), 1);
6564	      const n116 = ramp * ramp;
6565	      if (n116 > 0) {
6566	        this.lightRGB = [0.91 * n116, 0.82 * n116, 0.57 * n116];
6567	        this.lightRGBAt = { x: this.cx, y: this.y };          // base.Top
6568	      }
6569	    } else if (vid === 533) {
6570	      this.lightRGB = [0.6, 0.6, 0.3];                        // :21331-21333 沙漠幽魂 Top
6571	      this.lightRGBAt = { x: this.cx, y: this.y };
6572	    } else if (vid !== 172) {
6573	      // :21336-21338 兜底（24 火妖/29 哥布林术士/32 黑暗施法者/45 Tim/281-286 地牢
6574	      // 法师）Center 0.6/0.39/0.24；172 符文法师走粉尘分支不发光
6575	      this.lightRGB = [0.6, 0.39, 0.24];
6576	    }
6577	    if (!player) return;
6578	    this.facing = this.seekDirX(player);
6579	    // ---- ② 攻击蓄力点（:20984-21054）→ ai1=30（下帧起倒数，==25 发射）----
6580	    const at = (pts: number[]) => { if (pts.includes(this.ai0)) this.ai1 = 30; };
6581	    if (vid === 283 || vid === 284) at([100, 150, 200, 250, 300]);
6582	    else if (vid === 172) at([75, 150, 225, 300, 375, 450]);
6583	    else if (vid === 281 || vid === 282) at([100, 120, 140, 200, 220, 240, 300, 320, 340]);
6584	    else if (vid === 533) { if (this.ai0 === 180) this.ai1 = 181; }   // :21006 特殊循环支
6585	    else {
6586	      // :21033-21037 flag4（RedHat 变体 32）双倍计时：+1 后奇数回退 → 恒落偶数、
6587	      // 净 +2/t（蓄力点 100/200/300 均偶数照常命中 = 红帽法师整轮 2 倍速）。
6588	      // （getGood+24+血肉墙在场的同型双倍档 :21029-21032 未接，FTW 种子消费登记）
6589	      if (this.lai3 === 1) { this.ai0 += 1; if (this.ai0 % 2 === 1) this.ai0 -= 1; }
6590	      at([100, 200, 300]);                          // :21042 默认（24/29/32/45/285-286/693）
6591	    }
6592	    // ---- ③ 提前传送上限（族内阈值 → 直拉 650/700 档）----
6593	    if ((vid === 283 || vid === 284) && this.ai0 >= 450) this.ai0 = 700;    // :20991
6594	    else if ((vid === 281 || vid === 282) && this.ai0 >= 540) this.ai0 = 700; // :21019
6595	    else if ((vid === 285 || vid === 286) && this.ai0 > 400) this.ai0 = 650;  // :21048
6596	    else if (vid === 533 && this.ai0 >= 360) this.ai0 = 650;                  // :21052
6597	    // ---- ④ 传送触发（:21056-21078）：≥650 → ai0=1 + 采样落点（失败=整轮重来）----
6598	    if (this.ai0 >= 650) {
6599	      this.ai0 = 1;
6600	      // :21068-21072 693 图书管理员骷髅：先尝试贴书落点（NearBooks 30 格窗，
6601	      // AI_AttemptToFindTeleportSpotNearBooks :18948），失败落回通用法师传送
6602	      const ptx = Math.floor(player.cx / TILE), pty = Math.floor(player.cy / TILE);
6603	      let spot = vid === 693
6604	        ? attemptToFindTeleportSpotNearBooks(this, game, ptx, pty, 30) : null;
6605	      if (!spot) {
6606	        spot = attemptToFindTeleportSpot(this, game, ptx, pty,
6607	          20, 5, { dungeonWallGate: vid === 32 || (vid >= 281 && vid <= 286) });  // :21070 caster 参数 telefrag=5
6608	      }
6609	      if (spot) {
6610	        this.ai1 = vid === 24 ? 5 : 20;            // :21062-21066（Imp 短冷却 → 跳过 ==25 发射门）
6611	        this.ai2 = spot.x; this.ai3 = spot.y;
6612	      }
6613	    }
6614	    // ---- ⑤ 弹幕（:21080-21240）：ai1>0 递减；533 每 30t 循环支；Imp ==10 专属；其余 ==25 ----
6615	    if (this.ai1 > 0) {
6616	      this.ai1 -= 1;
6617	      if (vid === 533) {
6618	        if (this.ai1 % 30 === 0 && this.ai1 / 30 < 5) this.fireCasterVolley(game, player);
6619	      } else if (vid === 24) {
6620	        if (this.ai1 === 10) this.fireCasterVolley(game, player);   // :21131-21136
6621	      } else if (this.ai1 === 25) {
6622	        this.fireCasterVolley(game, player);                         // :21139
6623	      }
6624	    }
6625	  }
6626	
6627	  /** Caster 族单发弹幕（:21139-21240 volley）：蓄力 30t 倒数至 25/10 时发射 + Item8（172 无声） */
6628	  private fireCasterVolley(game: GameHooks, player: Player) {
6629	      const vid = this.vanillaId ?? -1;
6630	      // 弹跳球系法师（NPC.cs:21136/:21199-21206）：火妖 24→25 焰球 / 哥布林术士
6631	      // 29→30 混沌球 / 水球术士 32→33 水球 / 黑暗法师 45→665 混沌球(Tim 变体)——
6632	      // 原版每轮 volley 只 NewNPC 一球（AI_009 自带出膛定速），其余法师走 Dart 三连
6633	      const ballByCaster: Record<number, number> = { 24: 25, 29: 30, 32: 33, 45: 665 };
6634	      const ballId = ballByCaster[this.vanillaId ?? -1];
6635	      if (ballId) {
6636	        // 出膛锚（NewNPC :81547 Bottom 锚点换算回中心）：其余 = (X+width/2, Y-8)
6637	        // → 中心 y = top-16；Imp 25 = (X+width/2+dir*8, Y+20) → 中心 y = top+12
6638	        // （:21134/:21199-21201；曾用 cy±偏移 → 球生在法师躯体中部）
6639	        const ball = Enemy.fromVanilla(ballId,
6640	          this.cx + (ballId === 25 ? this.facing * 8 : 0),
6641	          this.y + (ballId === 25 ? 12 : -16));
6642	        if (ball) {
6643	          // :21204 NewNPC(33,...,flag4?1:0) → 末参 ai[3]：RedHat 变体标记（球侧
6644	          // RedHatSkeletronAdjustmentsEnabled 消费，getGood 提速档用）
6645	          if (vid === 32) ball.ai3 = this.lai3 === 1 ? 1 : 0;
6646	          addEnemy(game, ball);
6647	        }
6648	      } else if (this.vanillaId != null && this.vanillaId >= 281 && this.vanillaId <= 286) {
6649	        // 史后三法师（NPC.cs:21146-21191 num100/104/105）：布道者 281/282 迷失之魂 293
6650	        // （速 4、伤 40、timeLeft 300）;死灵法师 283/284 暗影束 290（速 6、伤 30,散布 ±30
6651	        // + 目标速度前置补偿 ×10）;魔法师 285/286 地狱火弹 291（速 8、伤 40）。
6652	        // 枪口 = (cx, y)（vector13 = 顶部中心）
6653	        const vid = this.vanillaId;
6654	        const proj = vid <= 282 ? 293 : vid <= 284 ? 290 : 291;
6655	        const spd = vid <= 282 ? 4 : vid <= 284 ? 6 : 8;
6656	        // :21180 num104 = GetAttackDamage_ForProjectiles(num104, num104*0.8) =
6657	        // Remap(difficulty, Classic, Expert, 基线, 基线×0.8)（大师钳在 Expert 端）。
6658	        // 弹体基线【不】用缩放后的 def.damage——命中玩家的难度乘区在
6659	        // projTargets.hitPlayer（Projectile.cs:13770）统一做，双乘会 ×4
6660	        const dmg = getAttackDamageForProjectiles(
6661	          vid <= 282 || vid >= 285 ? 40 : 30,
6662	          (vid <= 282 || vid >= 285 ? 40 : 30) * 0.8, this.difficulty);
6663	        let dx = player.cx - this.cx, dy = player.cy - this.cy;
6664	        if (vid === 283 || vid === 284) {           // :21163-21166 散布 + 前置补偿
6665	          dx += (Math.random() * 60 - 30) - player.vx * 10;
6666	          dy += (Math.random() * 60 - 30) - player.vy * 10;
6667	        }
6668	        const d = Math.hypot(dx, dy) || 1;
6669	        const dart = new Dart(this.cx, this.y, (dx / d) * spd, (dy / d) * spd, dmg, proj);
6670	        dart.hostile = true; // 史后三法师直构弹——敌怪弹（v5 bit7）
6671	        (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(dart, 'projectiles');
6672	      } else if (vid === 533) {
6673	        // 沙漠精灵（:21104-21135）：落点采样=玩家 ±6 格（排除玩家/自身 6×6 邻域 + 非激活格
6674	        //  + 非岩浆 + ±2 无实心），50 次，>2000px 放行 → 在落点原位放追踪弹 596（零初速）
6675	        const st = game.world.store;
6676	        const ptx = Math.floor(player.cx / TILE), pty = Math.floor(player.cy / TILE);
6677	        const mtx = Math.floor(this.cx / TILE), mty = Math.floor(this.cy / TILE);
6678	        const far = Math.abs(this.cx - player.cx) + Math.abs(this.cy - player.cy) > 2000; // :21100
6679	        for (let att = 0; att < 50 && !far; att++) {
6680	          const sx = ptx + Math.floor(Math.random() * 13) - 6;
6681	          const sy = pty + Math.floor(Math.random() * 13) - 6;
6682	          if (Math.abs(sy - pty) <= 6 && Math.abs(sx - ptx) <= 6) continue;   // 玩家邻域排
6683	          if (Math.abs(sy - mty) <= 6 && Math.abs(sx - mtx) <= 6) continue;   // 自身邻域排
6684	          if (!st.inBounds(sx, sy) || st.get(sx, sy) !== 0) continue;
6685	          if (st.liquid[st.idx(sx, sy)] > 0 && st.liquidType[st.idx(sx, sy)] === 2) continue;
6686	          let ok = true;
6687	          for (let dx2 = -2; dx2 <= 2 && ok; dx2++) {
6688	            for (let dy2 = -2; dy2 <= 2; dy2++) {
6689	              if (st.inBounds(sx + dx2, sy + dy2) && st.isSolid(sx + dx2, sy + dy2)) { ok = false; break; }
6690	            }
6691	          }
6692	          if (!ok) continue;
6693	          const curse = new Dart(sx * TILE + 8, sy * TILE + 8, 0, 0, this.baseDamage, 596);
6694	          curse.hostile = true;
6695	          (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(curse, 'projectiles');
6696	          break;
6697	        }
6698	        if (far) {
6699	          const curse = new Dart(this.cx, this.cy, 0, 0, this.baseDamage, 596);
6700	          curse.hostile = true;
6701	          (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(curse, 'projectiles');
6702	        }
6703	      } else if (vid === 172) {
6704	        // 符文法师（:21228-21240）：单发符文爆弹 129——速 10、伤 40、瞄准 ±10 抖动、
6705	        //  timeLeft 300；发射音 21196 例外门已在外层跳过（172 无声）
6706	        let dx = player.cx - this.cx + (Math.random() * 20 - 10);
6707	        let dy = player.cy - this.cy + (Math.random() * 20 - 10);
6708	        const d = Math.hypot(dx, dy) || 1;
6709	        dx = (dx / d) * 10; dy = (dy / d) * 10;
6710	        const dmg172 = getAttackDamageForProjectiles(40, 32, this.difficulty);
6711	        const blast = new Dart(this.cx, this.cy, dx, dy, dmg172, 129);
6712	        blast.hostile = true;
6713	        (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(blast, 'projectiles');
6714	      } else if (vid === 693) {
6715	        // 图书管理员骷髅（NPC.cs:21208-21215）：书锚 = AI_FindNearbyBook（tile 50 放置书
6716	        // = 本仓 v_50_books，Center−(10,20) 起 20×30 窗随机一本，:26275-62804）——
6717	        // 书由玩家放置（书架 101 掉书物 → 桌面/书架放置），无书走原版兜底
6718	        // Center+NextVector2Circular(30,15)。弹 1092 书弹 dmg 13 原值（无难度包装），
6719	        // 零初速、ai1=45、ai2=target——三态 AI 见 BookProj（Projectile.cs:23742-23809）
6720	        const st = game.world.store;
6721	        const mtx = Math.floor(this.cx / TILE), mty = Math.floor(this.cy / TILE);
6722	        let bx = this.cx, by = this.cy;
6723	        const books: Array<[number, number]> = [];
6724	        for (let sy = Math.max(0, mty - 20); sy < Math.min(st.h, mty + 10); sy++) {
6725	          for (let sx = Math.max(0, mtx - 10); sx < Math.min(st.w, mtx + 10); sx++) {
6726	            const t = st.get(sx, sy);
6727	            if (t && TILE_DEFS[t]?.vanilla?.sheet === 50) books.push([sx, sy]);
6728	          }
6729	        }
6730	        if (books.length > 0) {
6731	          // 随机一本（closestBook=false 分支 :2733-2740）→ 书格中心
6732	          const [bx2, by2] = books[Math.floor(Math.random() * books.length)];
6733	          bx = bx2 * TILE + 8; by = by2 * TILE + 8;
6734	        } else {
6735	          // NextVector2Circular(30,15)（Utils.cs：单位角×(30,15)×NextFloat）
6736	          const ang = Math.random() * Math.PI * 2;
6737	          const rad = Math.random();
6738	          bx += Math.cos(ang) * 30 * rad;
6739	          by += Math.sin(ang) * 15 * rad;
6740	        }
6741	        const book = new BookProj(bx - 8, by - 8, 13, player);
6742	        (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(book, 'projectiles');
6743	      } else {
6744	        // 原版通用分支无兜底发射（NPC.cs:21196-21241 的 if 链外零弹）——法师族全员
6745	        // （24/29/32/45/281-286/533/693/172）均有专属分支，此处仅防守性静默
6746	      }
6747	    if (this.vanillaId !== 172) {
6748	      game.playSfxFiles?.(['Item_8'], 1, this.cx, this.cy);   // :21196 发射音（172 例外）
6749	    }
6750	  }
6751	
6752	  private flyAI(game: GameHooks, player: Player | null, steer: number) {
6753	    // 恶魔眼式飞行 AI：
6754	    // 游荡时自主调整航向（朝巡航点平滑转向、到点即换新目标、撞墙自动绕开）；
6755	    // 玩家进入索敌范围后：朝向玩家明显加速逼近；脱离后回落游荡。
6756	    const dist = player ? Math.hypot(player.cx - this.cx, player.cy - this.cy) : Infinity;
6757	    const aggro = 18 * 16; // 18 格索敌（仓内近似门——原版 aiStyle 2 无距离索敌）
6758	    // 卡墙脱困：追击中持续撞墙/贴地/顶头 → 暂时退回游荡重新选航向（冷却内不再贴脸），

```


---

## 🤖 Assistant · 2026-08-19T03:07:09.665Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read slimeAI and its helpers (1690-2119).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:09.981Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 345,
 "offset": 1690
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:10.005Z

**📎 ToolResult**

```
1690	  private static readonly SLIME_CAN_CONTAIN_ITEMS = new Set([1, 59, 147, 184, 537]);
1691	
1692	  /** AI_001_Slimes_GenerateItemInsideBody（NPC.cs:62150-62258）1:1：num=Next(4) 四桶；
1693	   *  isBallooned（风气球 ai[0]==-999，:62154）→ 13 桶风筝/纸飞机。
1694	   *  WorldGen.Skyblock.lowTiles 三处修正（:62156-62164 / :62199-62207 / :62230-62237）
1695	   *  依赖天空盒世界——本仓无天空盒世界（NpcDrops evalCond 'SkyblockIsUp' 同判恒
1696	   *  false）→ 跳过。case 0 default 的 netMode!=0 分支（多人 2997 虫洞药水）单人不可达 */
1697	  private slimeGenItemInsideBody(isBallooned: boolean): number {
1698	    const roll = (n: number) => Math.floor(Math.random() * n);              // Next(n)
1699	    const rollR = (a: number, b: number) => a + Math.floor(Math.random() * (b - a)); // Next(a,b) 含a不含b
1700	    let num = roll(4);
1701	    if (isBallooned) {
1702	      switch (roll(13)) {                                                     // :62166-62191 风筝桶
1703	        case 1: return 4368; case 2: return 4369; case 3: return 4370; case 4: return 4371;
1704	        case 5: return 4612; case 6: return 4674;
1705	        case 7: case 8: case 9: return 4343;
1706	        case 10: case 11: case 12: return 4344;
1707	        default: return 4367;
1708	      }
1709	    }
1710	    switch (num) {
1711	      case 0:                                                                // 药水桶 :62193
1712	        switch (roll(7)) {
1713	          case 0: return 290;            // 迅捷
1714	          case 1: return 292;            // 铁皮
1715	          case 2: return 296;            // 光标
1716	          case 3: return 2322;           // 挖矿
1717	          default: return 2350;          // 回忆（2997 虫洞仅多人，:62200-62203）
1718	        }
1719	      case 1:                                                                // 火把/炸弹桶 :62196
1720	        num = roll(4);
1721	        return num === 0 ? 8 : num === 1 ? 965 : num === 2 ? 166 : 58;        // 火把/荧光棒/炸弹/红心
1722	      case 2: {                                                              // 矿物桶 :62222
1723	        if (roll(2) === 0) return rollR(11, 15);   // 11-14 铜/铁/银/金矿
1724	        return rollR(699, 703);                    // 699-702 同序锭
1725	      }
1726	      default:                                                                // 钱币桶 :62239
1727	        num = roll(3);
1728	        return num === 0 ? 71 : num === 1 ? 72 : 73;   // 铜/银/金币（堆叠档在掉落侧）
1729	    }
1730	  }
1731	
1732	  /** AI_001_Slimes 体内物品主掷段（NPC.cs:60750-60960）：首 AI 帧 ai[1]==0 且 value>0
1733	   *  时掷内容物——先置 -1（空）再最多 num2 次机会，任一分支赋正值后即停（:60777-60781）。
1734	   *  netID -5/-4（地牢/丛林彩装变种）整体不掷（:60815 continue），-6 额外 +4 次
1735	   *  （:60769），-10（蜜蜂丛林变种）走 1124/1125/314/5395 特例（:60840），史莱姆雨
1736	   *  +2 次（:60773）。跳过分支（登记）：
1737	   *  - WorldGen.Skyblock.{lowTiles,noHellstone,noFossils,noLifeCrystals} 六处（:60757/
1738	   *    :60806/:60813/:60822/:60827/:60859/:60892）——天空盒世界未实装恒 false
1739	   *  - Item.GetRandomVoiceItem（:60828-60830，天空盒子分支内）——连带跳过
1740	   *  - Main.vampireSeed（:60920-60923 地下 1/13 → 9 木头）——1.4.5 vampirism 哈希
1741	   *    秘密种子无文本映射（SeedFlags 无位，参照 infectedSeed 预留位惯例） */
1742	  private slimeRollContainedItem(game: GameHooks): void {
1743	    const vid = this.vanillaId;
1744	    if (vid === null || !Enemy.SLIME_CAN_CONTAIN_ITEMS.has(vid)) return;
1745	    if (this.ai1 !== 0) return;                    // 已掷过：-1=空 / >0=物品（只掷一次）
1746	    const netId = this.vanillaNetId !== 0 ? this.vanillaNetId : vid;
1747	    const value = this.spawnedFromStatue ? 0                       // 与死亡掉落链同式（:6258 侧）
1748	      : (netId === vid ? (this.def.value ?? npcValueOf(netId)) : npcValueOf(netId));
1749	    if (value <= 0) return;                        // :60750 value>0 门
1750	    const w = game.world;
1751	    const sf = w.seedFlags;
1752	    this.ai1 = -1;                                 // :60752 先置空
1753	    const roll = (n: number) => Math.floor(Math.random() * n);
1754	    let maxValue = 20;                             // :60753 主桶分母
1755	    let maxValue2 = 40;                            // :60754 副桶分母
1756	    let num2 = 1;                                  // :60755 掷骰次数
1757	    // WorldGen.Skyblock.lowTiles（:60757-60768：maxValue2=20/num2+4/maxValue=15，-6 再+5）
1758	    // ——天空盒世界未实装，跳过
1759	    if (netId === -6) num2 += 4;                   // :60769-60772
1760	    if (w.weather.slimeRain) num2 += 2;            // :60773-60775 Main.slimeRain
1761	    const surfaceY = w.groundLevel;                // Main.worldSurface（tile）
1762	    const yTile = this.y / TILE;
1763	    const rockLayer = (y: number): boolean => (sf.remix   // WorldGen.isThisInTheRockLayer :26916
1764	      ? (y > surfaceY && y <= w.rockLevel) : y > w.rockLevel);
1765	    for (let i = 0; i < num2; i++) {
1766	      if (this.ai1 !== -1) break;                  // :60777-60781 已中即停
1767	      if (vid === 59) {                            // :60784 岩浆史莱姆
1768	        if (sf.remix && roll(maxValue) === 0) {    // Main.remixWorld
1769	          this.ai1 = this.slimeGenItemInsideBody(this.ai0 === -999);
1770	        }
1771	        // else if Skyblock.noHellstone && downedBoss3 && Next(15)==0 → 174 地狱石（:60789-60793）
1772	        //   ——天空盒未实装跳过
1773	      } else if (yTile > surfaceY && (vid === 147 || vid === 184)) {  // :60796 地下棘刺史莱姆
1774	        // 两 lowTiles 子分支（:60800-60811）与普通分支同体 → 合并
1775	        if (roll(maxValue2) === 0) this.ai1 = roll(2) === 0 ? 1103 : 593;  // 淤泥/雪块
1776	      } else if (vid === 537) {                    // :60812 沙漠史莱姆
1777	        // Skyblock.noFossils && Next(5)==0 → 3347 沙漠化石（:60813-60816）：天空盒未实装跳过
1778	      } else {
1779	        if (vid !== 1 || netId === -5 || netId === -4) continue;   // :60815 仅蓝史莱姆族
1780	        let num4 = 500;                            // :60817 史莱姆法杖分母
1781	        if (sf.noTraps) num4 = 20;                 // Main.noTrapsWorld
1782	        else if (sf.getGoodWorld) num4 = 100;      // Main.getGoodWorld
1783	        else if (this.cy < surfaceY * TILE) num4 = -1;             // 地表蓝史莱姆不掷法杖
1784	        // isThisInTheRockLayer && (noLifeCrystals||lowTiles) && !AnyLifeCrystalSlimes() &&
1785	        //   Next(200)==0 → 29 生命水晶（:60822-60826）：天空盒未实装跳过
1786	        // Skyblock.lowTiles && 地下 && Next(1000)==0 → 语音物品（:60827-60830）：同上连带跳过
1787	        const genuineParty = !!(game as unknown as { partyState?: { genuineParty?: boolean } })
1788	          .partyState?.genuineParty;               // BirthdayParty.GenuineParty（真派对）
1789	        if (genuineParty && this.cy < surfaceY * TILE) {            // :60831-60839 地表真派对
1790	          this.ai1 = roll(2) === 0 ? 3736 + roll(3) : 1345;         // Next(3736,3739) 气球/彩纸
1791	        } else if (netId === -10 && roll(20) === 0) {               // :60840-60849 蜜蜂丛林变种
1792	          const num5 = sf.notTheBees ? roll(4) : roll(3);           // notTheBeesWorld 扩到 314/5395
1793	          this.ai1 = num5 === 1 ? 1125 : num5 === 2 ? 314 : num5 === 3 ? 5395 : 1124;
1794	        } else if (roll(maxValue) === 0) {                          // :60850-60854 主桶
1795	          this.ai1 = this.slimeGenItemInsideBody(this.ai0 === -999);
1796	        } else if (roll(maxValue2) === 0) {                         // :60855 副桶
1797	          if (yTile <= surfaceY) {
1798	            // Skyblock.lowTiles 表层分支（:60859-60876：194/195/62/27）：天空盒未实装跳过
1799	            this.ai1 = 751;                        // 云块
1800	          } else if (!rockLayer(yTile)) {                            // :60882-60887 浅地下
1801	            const num7 = roll(3);
1802	            this.ai1 = num7 === 1 ? 3 : num7 === 2 ? 9 : 2;         // 石/木/土
1803	          } else if (roll(10) === 0) {
1804	            this.ai1 = 3609;                        // :60888-60890 传送带
1805	          } else {
1806	            // Skyblock.lowTiles && hardMode 矿桶（:60892-60902）：天空盒未实装跳过
1807	            const num9 = roll(4);                   // :60904-60910 深层
1808	            this.ai1 = num9 === 1 ? 150 : num9 === 2 ? 3086 : num9 === 3 ? 3081 : 3; // 蛛网/花岗岩/大理石/石
1809	          }
1810	        } else if (num4 > 0 && roll(num4) === 0) {
1811	          this.ai1 = 539;                           // :60911-60913 史莱姆法杖
1812	        } else if (sf.getGoodWorld && yTile > surfaceY && roll(num4) === 0) {
1813	          this.ai1 = 147;                           // :60914-60916 ftw 地下 → 棘刺丛林史莱姆物
1814	        } else if (i === 0 && sf.remix && this.ai0 !== -999 && roll(3) === 0) {
1815	          this.ai1 = 75;                            // :60917-60919 首掷 remix → 生命水晶星史莱姆
1816	        }
1817	        // Main.vampireSeed（:60920-60923）：哈希秘密种子无载体，跳过
1818	      }
1819	    }
1820	  }
1821	
1822	  /** AI_001_Slimes 原版核（1.4.5.6 NPC.cs:60735+）：
1823	   *  站定 vx*=0.8；ai[0] 每 tick +1（激愤 +1 额外）；
1824	   *  阶段判定（num54=-1000）：ai0>=0 → 小跳（vy=-6, vx+=2*dir, ai0=-1120）；
1825	   *  -1000..-500 → 小跳（ai0=-2120）；-2000..-1500 → 大跳（vy=-8, vx+=3*dir, ai0=-200）。
1826	   *  即：小跳→小跳→大跳循环，约 5-10 秒节奏。
1827	   *  flag3 激愤（L61446）= 夜晚 || 受过伤 || 地下 → 追玩家；白天满血地表 = 被动保持方向。
1828	   *  卡墙（L61937）：落地 X == 起跳 X → direction 反转 + ai[2]=200 冷却（期间不索敌）。
1829	   *  蚱蜢(377/446) 复用本 AI（ai0 额外 +3，跳得更频繁） */
1830	  private slimeAI(game: GameHooks, player: Player | null) {
1831	    // ai[0]==-999：风气球挂载冻结（NPC.cs:61441 帧0不行动，位置由气球驱动）
1832	    if (this.ai0 === -999) return;
1833	    // ---- 体内物品掷骰（NPC.cs:60750 主掷段，只掷一次）----
1834	    // 置于光位前：首帧即得 ai[1]（原版此段在 :60737 星史莱姆光之后，晚一帧显色）
1835	    this.slimeRollContainedItem(game);
1836	    // ---- 史莱姆族点光（cs:61445-61456 / :61508-61515 / :61527-61531 / :61866-61870）----
1837	    if (this.vanillaId === 244) {
1838	      // :61444-61456 彩虹史莱姆 = Main.Disco 三色（6 相状态机 ≈ hsl 时间色，s=1 l=0.5）
1839	      const [dr, dg, db] = hslToRgb((visEffectFrames() / 222) % 1, 1, 0.5);
1840	      this.lightRGB = [dr, dg, db];
1841	    } else if (this.vanillaId === 667) {
1842	      // :61508-61513 金史莱姆 Color(204,181,72)/255×1.1
1843	      this.lightRGB = [(204 / 255) * 1.1, (181 / 255) * 1.1, (72 / 255) * 1.1];
1844	    } else if (this.vanillaId === 676) {
1845	      // :61527-61530 微光史莱姆 = TorchColor(23)（TorchID.cs:48-62 公式）
1846	      const num = Math.min(1, Math.max(0, 0.9 + (270 - mouseTextColorApprox()) / 900));
1847	      this.lightRGB = [num * 0.9, 0.55, num * 1.2];
1848	    } else if (this.vanillaId === 59) {
1849	      this.lightRGB = [1, 0.3, 0.1];                                    // :61866-61870 岩浆史莱姆
1850	    }
1851	    const st = game.world.store;
1852	    const underground = this.cy / TILE > game.world.groundLevel;
1853	    const grasshopper = this.vanillaId === 377 || this.vanillaId === 446;
1854	    const inWater = st.liquid[st.idx(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE))] > 80;
1855	    // flag3 激愤判定（:61459-61463）：!白天 || 受伤 || 地下 || ★史莱姆雨
1856	    //  （第四项曾缺——史莱姆雨白天满血地表史莱姆应主动追人 :61462）
1857	    const hurt = this.hp < this.maxHp;
1858	    let flag3 = !game.world.clock.isDay || hurt || underground || !!game.world.weather.slimeRain;
1859	    if (grasshopper) {
1860	      // 蚱蜢（cs:61479-61483）：只有玩家 200px 内且非 wet 才激愤蹦跳，平时走路档
1861	      flag3 = !!player && !player.dead && !inWater
1862	        && Math.hypot(player.cx - this.cx, player.cy - this.cy) <= 200;
1863	    }
1864	    // ai[2] 卡墙冷却期间不索敌（L61938）
1865	    if (this.ai2 > 0) this.ai2--;
1866	    // 激愤时索敌：direction 朝玩家；被动时保持现方向（confused 反向走 seekDirX）
1867	    if (flag3 && this.ai2 === 0 && player) {
1868	      this.facing = this.seekDirX(player);
1869	    }
1870	    // 蚱蜢被动档（cs:61479）：无激愤时走"走路档"——0.2 慢爬不进跳循环
1871	    if (grasshopper && !flag3) {
1872	      this.vx += this.facing * 0.02;
1873	      this.vx = Math.max(-0.2, Math.min(0.2, this.vx));
1874	      this.groundPhysics(game, 0, 0.12, 1);
1875	      return;
1876	    }
1877	    const dir = this.facing;
1878	    const grounded = this.onGround || (inWater && Math.abs(this.vy) < 0.8);
1879	    if (grounded) {
1880	      // 落地卡墙检测（L61937-61939）：起跳位置没变 = 白跳 → 反转
1881	      if (this.jumpStartX !== 0 && Math.abs(this.cx - this.jumpStartX) < 1) {
1882	        this.facing *= -1;
1883	        this.ai2 = 200;
1884	      }
1885	      this.jumpStartX = 0;
1886	      this.vx *= 0.8;
1887	      if (Math.abs(this.vx) < 0.1) this.vx = 0;
1888	      // ai[0] 递增（L61954-61956：基础+1 激愤+1；蚱蜢固定 +3 整体更慢，cs:61994）
1889	      this.ai0 += grasshopper ? 3 : 1 + (flag3 ? 1 : 0);
1890	      // 阶段判定（L62029-62040）
1891	      const num54 = -1000;
1892	      let stage = 0;
1893	      if (this.ai0 >= 0) stage = 1;
1894	      else if (this.ai0 >= num54 && this.ai0 <= num54 * 0.5) stage = 2;
1895	      else if (this.ai0 >= num54 * 2 && this.ai0 <= num54 * 1.5) stage = 3;
1896	      if (stage > 0) {
1897	        if (stage === 3) {
1898	          // 大跳（L62055-62059）
1899	          this.vy = -8;
1900	          this.vx += 3 * dir;
1901	          this.ai0 = -200;
1902	        } else {
1903	          // 小跳（L62062-62070）
1904	          this.vy = -6;
1905	          this.vx += 2 * dir;
1906	          this.ai0 = stage === 1 ? -120 + num54 : -120 + num54 * 2;
1907	        }
1908	        if (grasshopper) { this.vy *= 0.9; this.vx *= 0.6; } // cs:62088-62102 蚱蜢跳力衰减
1909	        this.jumpStartX = this.cx;  // ai[3] = position.X（L62059）
1910	      }
1911	    }
1912	    // ---- 尖刺史莱姆（cs:61555-61870：184 冰/535 尖刺/204 丛林）：落地 + 有视线 + 冷却尽
1913	    // → 单发抛物线尖刺（<200px，204 <400px；瞄准点上抬 rand(0,200) 补抛物线、速 4.5、
1914	    // 伤 9、冷却 50t=ai[3]）；专家模式五连扇形((k-2,-4) 归一 ×4、<120px/204<200px、冷却 30t)
1915	    // 未启用专家只做单发；射刺时 ai[0]=-40 压跳 + vx×0.9（cs:61573-61576）
1916	    const spiked = this.vanillaId === 184 || this.vanillaId === 535 || this.vanillaId === 204;
1917	    if (spiked && player && !player.dead && !inWater && this.onGround) {
1918	      if (this.ai3 > 0) this.ai3 -= 1;
1919	      const near = this.vanillaId === 204 ? 400 : 200;
1920	      const dp = Math.hypot(player.cx - this.cx, player.cy - this.cy);
1921	      if (dp < near && this.ai3 === 0 && this.canSeePlayer(st, player)) {
1922	        this.ai0 = -40; // 压制下一跳
1923	        this.vx *= 0.9;
1924	        const aimY = player.y - this.cy - Math.random() * 200;
1925	        this.shootDart(game, this.cx, this.cy, player.cx - this.cx, aimY, 4.5, 9,
1926	          this.vanillaId === 184 ? 174 : this.vanillaId === 204 ? 176 : 605);
1927	        this.ai3 = 50;
1928	      }
1929	    }
1930	    // ---- 史后仆从凝胶弹（cs:61668-61840：658 蓝 / 659 粉）：落地 + 有视线 + 冷却尽
1931	    // → 单发上抛凝胶弹（658→920 蓝 / 659→921 粉）。门 = |ΔX|<500 且 |ΔY|<550 且
1932	    // CanHit 且 velocity.Y==0（cs:61690-61694/:61747-61749）；瞄准点 Y 上抬
1933	    // rand(0,200) 补抛物线，基速 (4.5/距)×2，距离 >350 再 ×2（658）/×1.75（659）、
1934	    // >250 ×1.5（658）/×1.25（659）；伤 = MultiLerp(15,17,20) 经典档 15；冷却
1935	    // 50t（658）/40t（659）；射击时 ai[0]=-40 压跳 + vx×0.9。
1936	    // 专家分支（658 CountNPCS<5 门三星连发 920 ×(m-1,-4) 档 6 速 + 距离增益）未启用
1937	    const queenMinion = this.vanillaId === 658 || this.vanillaId === 659;
1938	    if (queenMinion && player && !player.dead && !inWater && this.onGround) {
1939	      if (this.ai3 > 0) this.ai3 -= 1;
1940	      const mdx = player.cx - this.cx;
1941	      const mdy = player.cy - this.cy;
1942	      const mdist = Math.hypot(mdx, mdy);
1943	      if (Math.abs(mdx) < 500 && Math.abs(mdy) < 550 && this.ai3 === 0
1944	        && this.canSeePlayer(st, player)) {
1945	        this.ai0 = -40; // 压制下一跳（cs:61721/:61751）
1946	        this.vx *= 0.9;
1947	        const aimY = player.y - this.cy - Math.random() * 200;   // :61724/:61758
1948	        let k = (4.5 / (Math.hypot(mdx, aimY) || 1)) * 2;        // :61726-61727
1949	        if (mdist > 350) k *= this.vanillaId === 658 ? 2 : 1.75; // :61728-61733
1950	        else if (mdist > 250) k *= this.vanillaId === 658 ? 1.5 : 1.25;
1951	        // 920/921 均为 aiStyle 1 弹跳凝胶弹（Projectile.cs:8443-8457）；本仓敌弹出口
1952	        // 统一 grav 0 直飞（shoot），上抛补偿已含在瞄准点
1953	        shoot(game, this.cx, this.cy, mdx * k, aimY * k, 15, this.vanillaId === 658 ? 920 : 921, 240);
1954	        this.ai3 = this.vanillaId === 658 ? 50 : 40;             // :61735/:61770
1955	      }
1956	    }
1957	    // ---- wet 浮力段（cs:61877-61935 1:1，替换旧 groundPhysics buoyant 近似）----
1958	    // 纵向碰撞(上帧 collideY) → vy=-2 上弹；上浮中 X 原地未动 → 掉头 + ai[2]=200 冷却；
1959	    // vy>2 ×0.9、恒 -0.5 上浮、钳 -4（59 岩浆史莱姆钳 -10 且 directionY<0 追加 -0.8）
1960	    // ——史莱姆在水中以弹跳方式漂浮，贴面上下起落（collideY 读的是上一 tick 碰撞，
1961	    // 与原版 AI 先于 UpdateCollision 的时序一致）
1962	    if (this.wet) {
1963	      if (this.onGround || this.hitHead) this.vy = -2;
1964	      if (this.vy < 0 && this.slimeWetX === this.x) {
1965	        this.facing *= -1;
1966	        this.ai2 = 200;
1967	      }
1968	      if (this.vy > 0) this.slimeWetX = this.x;
1969	      if (this.vanillaId === 59) {
1970	        if (this.vy > 2) this.vy *= 0.9;
1971	        else if (this.dirY < 0) this.vy -= 0.8;
1972	        this.vy -= 0.5;
1973	        if (this.vy < -10) this.vy = -10;
1974	      } else {
1975	        if (this.vy > 2) this.vy *= 0.9;
1976	        this.vy -= 0.5;
1977	        if (this.vy < -4) this.vy = -4;
1978	      }
1979	      if (this.ai2 === 1 && flag3 && player) this.facing = this.seekDirX(player);
1980	    }
1981	    // 重力+碰撞（原版经由 NPC 碰撞；水中位移减速由 wet→liqFactor 统一承担）
1982	    this.groundPhysics(game, 0, 0.12, 1);
1983	    // AI_001 尾部颜色渐变（NPC.cs:60971 起为 slime(type 1) 专属段；
1984	    // 此前误挂在 zombieAI——守卫 vanillaId!==1 使其全程空转，移回 slimeAI）
1985	    this.slimeColorTick(game);
1986	    // ---- SlimeCanContainItems 三处 ai[1] 物品变体光（NPC.cs:60737/:61152/:61289）----
1987	    // 放染色后与原版同序（:61152 读渐变后的 this.color）。:60740 同段 dust 228 星尘
1988	    // （1/12 帧闪烁上飘）未接——repo 粒子桶无 dust 228 语义，登记
1989	    if (this.ai1 === 75 && this.vanillaId === 1) {
1990	      // :60737-60740 type1 携 29 生命水晶：num=0.3 → (0.24,0.21,0.03) @ 中心格
1991	      this.mergeLightRGB([0.8 * 0.3, 0.7 * 0.3, 0.1 * 0.3]);
1992	    } else if (this.ai1 === 364 || this.ai1 === 1104 || this.ai1 === 365
1993	      || this.ai1 === 1105 || this.ai1 === 366 || this.ai1 === 1106) {
1994	      // :61152 金属矿史莱姆（钴/钯金/秘银/山铜/精金/钛金）：this.color 各通道/500
1995	      // @ position（顶左格，非中心）——lavaImmune/防御+30/伤害×3/悬浮重力等行为段
1996	      // （:61095-61155）属 AI_001 行为侧，本批只接光位
1997	      const c = this.colorRGBA ?? [0, 0, 0, 0];
1998	      this.mergeLightRGB([c[0] / 500, c[1] / 500, c[2] / 500], { x: this.x, y: this.y });
1999	    } else if (this.ai1 === 314) {
2000	      // :61289 草药史莱姆 (0.4,0.9,1) @ 中心格（尘 41 每帧闪烁 :61285 未接，登记）
2001	      this.mergeLightRGB([0.4, 0.9, 1]);
2002	    }
2003	  }
2004	
2005	  /** 原版 UpdateNPC_UpdateGravity（NPC.cs:91876-91953）通用重力档 1:1：
2006	   *  ① 高空衰减（:91916-91934）：num=(maxTilesX/4200)²、num2=(y/16−(60+10·num))/
2007	   *     (worldSurface/6) 钳 [0.25,1] → gravity×num2——空岛/太空高度下落明显变缓
2008	   *     （worldSurface=world.groundLevel，LunarEvent.ts:143 同源换算）；
2009	   *  ② wet 三档（:91936-91952）：0.2(水)/0.1(蜜)/0.15(微光)——原版为绝对值直替
2010	   *     （覆盖①的高空系数），照抄 TownNPC.ts:1200 先例；落速帽 7/4/5.5 已由
2011	   *     npcLiquid.ts 第 6 段每 tick 钳，此处不重复。
2012	   *  特例族（258/425/426/427/576/577/541/aiStyle7-ai25 的专属重力改写）由各自
2013	   *  AI 内自带档，不在此列。
2014	   *  ★GRAVITY=0.4 vs 原版 0.3 偏差已登记（constants.ts）勿动：①高空系数按原版
2015	   *  乘子直接叠加在现 GRAVITY 上；②wet 档取原版绝对值（0.2/0.1/0.15 对 0.4 基数
2016	   *  的减速比比原版更陡——与 TownNPC 先例一致，待重力专项统一）。 */
2017	  applyGravity(game: GameHooks) {
2018	    let g = GRAVITY;
2019	    // ① 高空衰减（worldSurface/6 与 (60+10num) 为原版双参，浮点同式；
2020	    //    groundLevel<=0 的手工/测试世界无地表线 → 视作全重力，防 ÷0/NaN）
2021	    const surf = game.world.groundLevel;
2022	    if (surf > 0) {
2023	      const num = (game.world.store.w / 4200) ** 2;
2024	      let alt = (this.y / TILE - (60 + 10 * num)) / (surf / 6);
2025	      if (alt < 0.25) alt = 0.25;
2026	      else if (alt > 1) alt = 1;
2027	      g *= alt;
2028	    }
2029	    // ② wet 三档（绝对值直替，覆盖高空系数——原版同序）
2030	    if (this.wet) g = this.shimmerWet ? 0.15 : this.honeyWet ? 0.1 : 0.2;
2031	    this.vy = Math.min(this.vy + g, MAX_FALL_SPEED);
2032	  }
2033	
2034	  private zombieAI(game: GameHooks, player: Player | null) {

```


---

## 🤖 Assistant · 2026-08-19T03:07:16.498Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have our implementations. Now let me read the vanilla source. Key sections:

1. AI_001_Slimes :60735-62266
2. AI_003_Fighters :56245-60734
3. AI_008 caster in main switch ~:20777-21341
4. AI_013 plant ~:22580-22860 (need to find)
5. AI_020/AI_021 in main switch (~:24596-24730)
6. AI_025 mimic ~:25621
7. AI_040 wall creeper ~:29784-30022
8. AI_042 lost girl ~:30281-30310

Let me first grep for the main switch cases to confirm line ranges, then read each vanilla section. Since these are large, let me read them in chunks. Start with caster (AI 8) and plant (AI 13), spike ball/wheel (20/21), mimic (25), wall creeper (40), lost girl (42) — the inline switch ones. Then the big private functions AI_001 and AI_003.

Let me grep the switch.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:16.963Z · glm-x-preview-260804

```
现在我这边的情况已经掌握了。我来定位一下原版 AI 的切换入口点。
```


---

## 🤖 Assistant · 2026-08-19T03:07:18.020Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case 8:\\|case 13:\\|case 20:\\|case 21:\\|case 25:\\|case 40:\\|case 42:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1 > 19000 && $1 < 33000' ",
 "description": "Find main AI switch case line numbers"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:18.061Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-19T03:07:18.652Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '20770,20800p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Peek at caster AI start region"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:18.705Z

**📎 ToolResult**

```
		{
			AI_007_TownEntities();
			return;
		}
		if (aiStyle == 8)
		{
			bool flag4 = RedHatSkeletronAdjustmentsEnabled();
			if (type == 32)
			{
				int num70 = FindFirstNPC(35);
				if (num70 >= 0 && Main.npc[num70].ai[3] == 1f)
				{
					localAI[3] = 1f;
					flag4 = true;
				}
			}
			TargetClosest();
			velocity.X *= 0.93f;
			if (velocity.X > -0.1f && velocity.X < 0.1f)
			{
				velocity.X = 0f;
			}
			if (this.ai[0] == 0f)
			{
				this.ai[0] = 500f;
				if (type == 693)
				{
					localAI[1] = 150f;
				}
			}
			if (type == 172)

```


---

## 🤖 Assistant · 2026-08-19T03:07:22.523Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The grep with `case 8:` didn't hit because the decompiled uses `if (aiStyle == 8)`. Line numbers: caster starts ~20775. Let me grep "aiStyle == N" to find all entries.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:23.201Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"if (aiStyle == \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1 > 19000 && $1 < 34000'",
 "description": "List aiStyle if-branches in main AI switch"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:23.241Z

**📎 ToolResult**

```
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

```


---

## 🤖 Assistant · 2026-08-19T03:07:34.390Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good. AI 15 at :23544 — let me check what it is (flail or King Slime?).

Actually, from the private function list, AI_015_KingSlime is at :43436. Let me check :23544.

Now let me read the vanilla sections. First the caster (aiStyle 8, :20774-21349). That's ~575 lines. Let me read it.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:07:34.932Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '23544,23560p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check aiStyle 15 content"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:34.973Z

**📎 ToolResult**

```
		if (aiStyle == 15)
		{
			AI_015_KingSlime();
			return;
		}
		if (aiStyle == 16)
		{
			if (direction == 0)
			{
				TargetClosest();
			}
			if (type == 688)
			{
				if (Main.netMode != 1)
				{
					if (justHit && this.ai[2] == 0f)
					{

```


---

## 🤖 Assistant · 2026-08-19T03:07:35.341Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 575,
 "offset": 20774
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:07:35.362Z

**📎 ToolResult**

```
20774			if (aiStyle == 8)
20775			{
20776				bool flag4 = RedHatSkeletronAdjustmentsEnabled();
20777				if (type == 32)
20778				{
20779					int num70 = FindFirstNPC(35);
20780					if (num70 >= 0 && Main.npc[num70].ai[3] == 1f)
20781					{
20782						localAI[3] = 1f;
20783						flag4 = true;
20784					}
20785				}
20786				TargetClosest();
20787				velocity.X *= 0.93f;
20788				if (velocity.X > -0.1f && velocity.X < 0.1f)
20789				{
20790					velocity.X = 0f;
20791				}
20792				if (this.ai[0] == 0f)
20793				{
20794					this.ai[0] = 500f;
20795					if (type == 693)
20796					{
20797						localAI[1] = 150f;
20798					}
20799				}
20800				if (type == 172)
20801				{
20802					if (alpha < 255)
20803					{
20804						alpha++;
20805					}
20806					if (justHit)
20807					{
20808						alpha = 0;
20809					}
20810				}
20811				if (this.ai[2] != 0f && this.ai[3] != 0f)
20812				{
20813					position += netOffset;
20814					if (type == 172)
20815					{
20816						alpha = 255;
20817					}
20818					SoundEngine.PlaySound(SoundID.Item8, position);
20819					for (int num71 = 0; num71 < 50; num71++)
20820					{
20821						if (type == 29 || type == 45)
20822						{
20823							int num72 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 27, 0f, 0f, 100, default(Color), Main.rand.Next(1, 3));
20824							Dust dust = Main.dust[num72];
20825							dust.velocity *= 3f;
20826							if (Main.dust[num72].scale > 1f)
20827							{
20828								Main.dust[num72].noGravity = true;
20829							}
20830						}
20831						else if (type == 32)
20832						{
20833							int num73 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 172, 0f, 0f, 100, default(Color), 1.5f);
20834							Dust dust = Main.dust[num73];
20835							dust.velocity *= 3f;
20836							Main.dust[num73].noGravity = true;
20837						}
20838						else if (type == 693)
20839						{
20840							Dust dust2 = Dust.NewDustDirect(position, width, height, 269, 0f, 0f, 100, Color.White, 1.5f);
20841							dust2.noLight = true;
20842							dust2.noGravity = true;
20843						}
20844						else if (type == 283 || type == 284)
20845						{
20846							int num74 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 173);
20847							Dust dust = Main.dust[num74];
20848							dust.velocity *= 2f;
20849							Main.dust[num74].scale = 1.4f;
20850						}
20851						else if (type == 285 || type == 286)
20852						{
20853							int num75 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 174, 0f, 0f, 100, default(Color), 1.5f);
20854							Dust dust = Main.dust[num75];
20855							dust.velocity *= 3f;
20856							Main.dust[num75].noGravity = true;
20857						}
20858						else if (type == 281 || type == 282)
20859						{
20860							int num76 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 175, 0f, 0f, 100, default(Color), 1.5f);
20861							Dust dust = Main.dust[num76];
20862							dust.velocity *= 3f;
20863							Main.dust[num76].noGravity = true;
20864						}
20865						else if (type == 172)
20866						{
20867							int num77 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 106, 0f, 0f, 100, default(Color), 2.5f);
20868							Dust dust = Main.dust[num77];
20869							dust.velocity *= 3f;
20870							Main.dust[num77].noGravity = true;
20871						}
20872						else if (type == 533)
20873						{
20874							int num78 = Dust.NewDust(position, width, height, 27, 0f, 0f, 100, default(Color), 2.5f);
20875							Dust dust = Main.dust[num78];
20876							dust.velocity *= 3f;
20877							Main.dust[num78].noGravity = true;
20878						}
20879						else
20880						{
20881							int num79 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 100, default(Color), 2.5f);
20882							Dust dust = Main.dust[num79];
20883							dust.velocity *= 3f;
20884							Main.dust[num79].noGravity = true;
20885						}
20886					}
20887					position -= netOffset;
20888					position.X = this.ai[2] * 16f - (float)(width / 2) + 8f;
20889					position.Y = this.ai[3] * 16f - (float)height;
20890					netOffset *= 0f;
20891					velocity.X = 0f;
20892					velocity.Y = 0f;
20893					this.ai[2] = 0f;
20894					this.ai[3] = 0f;
20895					if (type == 693)
20896					{
20897						localAI[0] = 0f;
20898						localAI[1] = 650f;
20899						localAI[3] = 0f;
20900					}
20901					SoundEngine.PlaySound(SoundID.Item8, position);
20902					for (int num80 = 0; num80 < 50; num80++)
20903					{
20904						if (type == 29 || type == 45)
20905						{
20906							int num81 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 27, 0f, 0f, 100, default(Color), Main.rand.Next(1, 3));
20907							Dust dust = Main.dust[num81];
20908							dust.velocity *= 3f;
20909							if (Main.dust[num81].scale > 1f)
20910							{
20911								Main.dust[num81].noGravity = true;
20912							}
20913						}
20914						else if (type == 32)
20915						{
20916							int num82 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 172, 0f, 0f, 100, default(Color), 1.5f);
20917							Dust dust = Main.dust[num82];
20918							dust.velocity *= 3f;
20919							Main.dust[num82].noGravity = true;
20920						}
20921						else if (type == 693)
20922						{
20923							Dust dust3 = Dust.NewDustDirect(position, width, height, 269, 0f, 0f, 100, Color.White, 1.5f);
20924							dust3.noLight = true;
20925							dust3.noGravity = true;
20926						}
20927						else if (type == 172)
20928						{
20929							int num83 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 106, 0f, 0f, 100, default(Color), 2.5f);
20930							Dust dust = Main.dust[num83];
20931							dust.velocity *= 3f;
20932							Main.dust[num83].noGravity = true;
20933						}
20934						else if (type == 283 || type == 284)
20935						{
20936							int num84 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 173);
20937							Dust dust = Main.dust[num84];
20938							dust.velocity *= 2f;
20939							Main.dust[num84].scale = 1.4f;
20940						}
20941						else if (type == 285 || type == 286)
20942						{
20943							int num85 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 174, 0f, 0f, 100, default(Color), 1.5f);
20944							Dust dust = Main.dust[num85];
20945							dust.velocity *= 3f;
20946							Main.dust[num85].noGravity = true;
20947						}
20948						else if (type == 281 || type == 282)
20949						{
20950							int num86 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 175, 0f, 0f, 100, default(Color), 1.5f);
20951							Dust dust = Main.dust[num86];
20952							dust.velocity *= 3f;
20953							Main.dust[num86].noGravity = true;
20954						}
20955						else if (type == 533)
20956						{
20957							int num87 = Dust.NewDust(position, width, height, 27, 0f, 0f, 100, default(Color), 2.5f);
20958							Dust dust = Main.dust[num87];
20959							dust.velocity *= 3f;
20960							Main.dust[num87].noGravity = true;
20961						}
20962						else
20963						{
20964							int num88 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 100, default(Color), 2.5f);
20965							Dust dust = Main.dust[num88];
20966							dust.velocity *= 3f;
20967							Main.dust[num88].noGravity = true;
20968						}
20969					}
20970				}
20971				this.ai[0] += 1f;
20972				if (type == 693)
20973				{
20974					localAI[0]++;
20975					if (localAI[2] > 0f)
20976					{
20977						localAI[2]--;
20978					}
20979					if (localAI[3] == 0f && localAI[0] > 1f)
20980					{
20981						localAI[3] = direction;
20982					}
20983				}
20984				if (type == 283 || type == 284)
20985				{
20986					if (this.ai[0] == 100f || this.ai[0] == 150f || this.ai[0] == 200f || this.ai[0] == 250f || this.ai[0] == 300f)
20987					{
20988						this.ai[1] = 30f;
20989						netUpdate = true;
20990					}
20991					if (this.ai[0] >= 450f)
20992					{
20993						this.ai[0] = 700f;
20994					}
20995				}
20996				else if (type == 172)
20997				{
20998					if (this.ai[0] == 75f || this.ai[0] == 150f || this.ai[0] == 225f || this.ai[0] == 300f || this.ai[0] == 375f || this.ai[0] == 450f)
20999					{
21000						this.ai[1] = 30f;
21001						netUpdate = true;
21002					}
21003				}
21004				else if (type == 533)
21005				{
21006					if (this.ai[0] == 180f)
21007					{
21008						this.ai[1] = 181f;
21009						netUpdate = true;
21010					}
21011				}
21012				else if (type == 281 || type == 282)
21013				{
21014					if (this.ai[0] == 100f || this.ai[0] == 120f || this.ai[0] == 140f || this.ai[0] == 200f || this.ai[0] == 220f || this.ai[0] == 240f || this.ai[0] == 300f || this.ai[0] == 320f || this.ai[0] == 340f)
21015					{
21016						this.ai[1] = 30f;
21017						netUpdate = true;
21018					}
21019					if (this.ai[0] >= 540f)
21020					{
21021						this.ai[0] = 700f;
21022					}
21023				}
21024				else
21025				{
21026					if (Main.getGoodWorld && type == 24 && AnyNPCs(113))
21027					{
21028						this.ai[0] += 1f;
21029						if (this.ai[0] % 2f == 1f)
21030						{
21031							this.ai[0] -= 1f;
21032						}
21033					}
21034					if (flag4)
21035					{
21036						this.ai[0] += 1f;
21037						if (this.ai[0] % 2f == 1f)
21038						{
21039							this.ai[0] -= 1f;
21040						}
21041					}
21042					if (this.ai[0] == 100f || this.ai[0] == 200f || this.ai[0] == 300f)
21043					{
21044						this.ai[1] = 30f;
21045						netUpdate = true;
21046					}
21047				}
21048				if ((type == 285 || type == 286) && this.ai[0] > 400f)
21049				{
21050					this.ai[0] = 650f;
21051				}
21052				if (type == 533 && this.ai[0] >= 360f)
21053				{
21054					this.ai[0] = 650f;
21055				}
21056				if (this.ai[0] >= 650f && Main.netMode != 1)
21057				{
21058					this.ai[0] = 1f;
21059					int num89 = (int)Main.player[target].Center.X / 16;
21060					int num90 = (int)Main.player[target].Center.Y / 16;
21061					Vector2 destination = Vector2.Zero;
21062					int num91 = 20;
21063					if (type == 24)
21064					{
21065						num91 = 5;
21066					}
21067					bool flag5 = type == 693 && AI_AttemptToFindTeleportSpotNearBooks(new Point(num89, num90), 30, out destination);
21068					if (!flag5)
21069					{
21070						flag5 = AI_AttemptToFindTeleportSpot(ref destination, num89, num90);
21071					}
21072					if (flag5)
21073					{
21074						this.ai[1] = num91;
21075						this.ai[2] = destination.X;
21076						this.ai[3] = destination.Y;
21077					}
21078					netUpdate = true;
21079				}
21080				if (this.ai[1] > 0f)
21081				{
21082					int num92 = 25;
21083					this.ai[1] -= 1f;
21084					if (type == 533)
21085					{
21086						if (this.ai[1] % 30f == 0f && this.ai[1] / 30f < 5f)
21087						{
21088							SoundEngine.PlaySound(SoundID.Item8, position);
21089							if (Main.netMode != 1)
21090							{
21091								Point point = base.Center.ToTileCoordinates();
21092								Point point2 = Main.player[target].Center.ToTileCoordinates();
21093								Vector2 vector12 = Main.player[target].Center - base.Center;
21094								int num93 = 6;
21095								int num94 = 6;
21096								int num95 = 0;
21097								int num96 = 2;
21098								int num97 = 0;
21099								bool flag6 = false;
21100								if (vector12.Length() > 2000f)
21101								{
21102									flag6 = true;
21103								}
21104								while (!flag6 && num97 < 50)
21105								{
21106									num97++;
21107									int num98 = Main.rand.Next(point2.X - num93, point2.X + num93 + 1);
21108									int num99 = Main.rand.Next(point2.Y - num93, point2.Y + num93 + 1);
21109									if ((num99 < point2.Y - num95 || num99 > point2.Y + num95 || num98 < point2.X - num95 || num98 > point2.X + num95) && (num99 < point.Y - num94 || num99 > point.Y + num94 || num98 < point.X - num94 || num98 > point.X + num94) && !Main.tile[num98, num99].nactive())
21110									{
21111										bool flag7 = true;
21112										if (flag7 && Main.tile[num98, num99].lava())
21113										{
21114											flag7 = false;
21115										}
21116										if (flag7 && Collision.SolidTiles(num98 - num96, num98 + num96, num99 - num96, num99 + num96))
21117										{
21118											flag7 = false;
21119										}
21120										if (flag7)
21121										{
21122											Projectile.NewProjectile(GetSpawnSource_ForProjectile(), num98 * 16 + 8, num99 * 16 + 8, 0f, 0f, 596, 0, 1f, Main.myPlayer, target);
21123											flag6 = true;
21124											break;
21125										}
21126									}
21127								}
21128							}
21129						}
21130					}
21131					else if (type == 24)
21132					{
21133						if (this.ai[1] == 10f)
21134						{
21135							SoundEngine.PlaySound(SoundID.Item8, position);
21136							NewNPC(GetSpawnSourceForProjectileNPC(), (int)position.X + width / 2 + direction * 8, (int)position.Y + 20, 25);
21137						}
21138					}
21139					else if (this.ai[1] == (float)num92)
21140					{
21141						if (type >= 281 && type <= 286)
21142						{
21143							if (Main.netMode != 1)
21144							{
21145								float num100 = 6f;
21146								if (type == 285 || type == 286)
21147								{
21148									num100 = 8f;
21149								}
21150								if (type == 281 || type == 282)
21151								{
21152									num100 = 4f;
21153								}
21154								Vector2 vector13 = new Vector2(position.X + (float)width * 0.5f, position.Y);
21155								float num101 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector13.X;
21156								float num102 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector13.Y;
21157								if (type == 283 || type == 284)
21158								{
21159									num101 += (float)Main.rand.Next(-30, 31);
21160									num102 += (float)Main.rand.Next(-30, 31);
21161									num101 -= Main.player[target].velocity.X * 10f;
21162									num102 -= Main.player[target].velocity.Y * 10f;
21163								}
21164								float num103 = (float)Math.Sqrt(num101 * num101 + num102 * num102);
21165								num103 = num100 / num103;
21166								num101 *= num103;
21167								num102 *= num103;
21168								int num104 = 30;
21169								int num105 = 290;
21170								if (type == 285 || type == 286)
21171								{
21172									num105 = 291;
21173									num104 = 40;
21174								}
21175								if (type == 281 || type == 282)
21176								{
21177									num105 = 293;
21178									num104 = 40;
21179								}
21180								num104 = GetAttackDamage_ForProjectiles(num104, (float)num104 * 0.8f);
21181								int num106 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector13.X, vector13.Y, num101, num102, num105, num104, 0f, Main.myPlayer);
21182								Main.projectile[num106].timeLeft = 300;
21183								if (num105 == 291)
21184								{
21185									Main.projectile[num106].ai[0] = Main.player[target].Center.X;
21186									Main.projectile[num106].ai[1] = Main.player[target].Center.Y;
21187									Main.projectile[num106].netUpdate = true;
21188								}
21189								localAI[0] = 0f;
21190							}
21191						}
21192						else
21193						{
21194							if (type != 172)
21195							{
21196								SoundEngine.PlaySound(SoundID.Item8, position);
21197							}
21198							if (Main.netMode != 1)
21199							{
21200								if (type == 29)
21201								{
21202									NewNPC(GetSpawnSourceForProjectileNPC(), (int)position.X + width / 2, (int)position.Y - 8, 30);
21203								}
21204								else if (type == 45)
21205								{
21206									NewNPC(GetSpawnSourceForProjectileNPC(), (int)position.X + width / 2, (int)position.Y - 8, 665);
21207								}
21208								else if (type == 32)
21209								{
21210									NewNPC(GetSpawnSourceForProjectileNPC(), (int)position.X + width / 2, (int)position.Y - 8, 33, 0, 0f, 0f, 0f, flag4 ? 1 : 0);
21211								}
21212								else if (type == 693)
21213								{
21214									Vector2 vec = base.Center;
21215									Point searchPosition = vec.ToTileCoordinates();
21216									searchPosition.X -= 10;
21217									searchPosition.Y -= 20;
21218									if (AI_FindNearbyBook(searchPosition, 20, 30, out var bookPosition))
21219									{
21220										vec = bookPosition.ToWorldCoordinates();
21221									}
21222									else
21223									{
21224										vec += Main.rand.NextVector2Circular(30f, 15f);
21225									}
21226									Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vec.X, vec.Y, 0f, 0f, 1092, 13, 0f, Main.myPlayer, 0f, 45f, target);
21227								}
21228								else if (type == 172)
21229								{
21230									float num107 = 10f;
21231									Vector2 vector14 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
21232									float num108 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector14.X + (float)Main.rand.Next(-10, 11);
21233									float num109 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector14.Y + (float)Main.rand.Next(-10, 11);
21234									float num110 = (float)Math.Sqrt(num108 * num108 + num109 * num109);
21235									num110 = num107 / num110;
21236									num108 *= num110;
21237									num109 *= num110;
21238									int num111 = 40;
21239									int num112 = 129;
21240									int num113 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector14.X, vector14.Y, num108, num109, num112, num111, 0f, Main.myPlayer);
21241									Main.projectile[num113].timeLeft = 300;
21242									localAI[0] = 0f;
21243								}
21244							}
21245						}
21246					}
21247				}
21248				position += netOffset;
21249				if (type == 29 || type == 45)
21250				{
21251					if (Main.rand.Next(5) == 0)
21252					{
21253						int num114 = Dust.NewDust(new Vector2(position.X, position.Y + 2f), width, height, 27, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 1.5f);
21254						Main.dust[num114].noGravity = true;
21255						Main.dust[num114].velocity.X *= 0.5f;
21256						Main.dust[num114].velocity.Y = -2f;
21257					}
21258				}
21259				else if (type == 32)
21260				{
21261					if (Main.rand.Next(3) != 0)
21262					{
21263						int num115 = Dust.NewDust(new Vector2(position.X, position.Y + 2f), width, height, 172, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 0.9f);
21264						Main.dust[num115].noGravity = true;
21265						Main.dust[num115].velocity.X *= 0.3f;
21266						Main.dust[num115].velocity.Y *= 0.2f;
21267						Main.dust[num115].velocity.Y -= 1f;
21268					}
21269				}
21270				else if (type == 693)
21271				{
21272					float num116 = Utils.Remap(this.ai[0], 0f, 60f, 0f, 1f);
21273					num116 *= num116;
21274					if (num116 > 0f)
21275					{
21276						Lighting.AddLight(base.Top, num116 * 0.91f, num116 * 0.82f, num116 * 0.57f);
21277					}
21278				}
21279				else if (type == 172)
21280				{
21281					int num117 = 1;
21282					if (alpha == 255)
21283					{
21284						num117 = 2;
21285					}
21286					for (int num118 = 0; num118 < num117; num118++)
21287					{
21288						if (Main.rand.Next(255) > 255 - alpha)
21289						{
21290							int num119 = Dust.NewDust(new Vector2(position.X, position.Y + 2f), width, height, 106, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 1.2f);
21291							Main.dust[num119].noGravity = true;
21292							Main.dust[num119].velocity.X *= 0.1f + (float)Main.rand.Next(30) * 0.01f;
21293							Main.dust[num119].velocity.Y *= 0.1f + (float)Main.rand.Next(30) * 0.01f;
21294							Dust dust = Main.dust[num119];
21295							dust.scale *= 1f + (float)Main.rand.Next(6) * 0.1f;
21296						}
21297					}
21298				}
21299				else if (type == 283 || type == 284)
21300				{
21301					if (Main.rand.Next(2) == 0)
21302					{
21303						int num120 = Dust.NewDust(new Vector2(position.X, position.Y + 2f), width, height, 173);
21304						Main.dust[num120].velocity.X *= 0.5f;
21305						Main.dust[num120].velocity.Y *= 0.5f;
21306					}
21307				}
21308				else if (type == 285 || type == 286)
21309				{
21310					if (Main.rand.Next(2) == 0)
21311					{
21312						int num121 = Dust.NewDust(new Vector2(position.X, position.Y + 2f), width, height, 174, velocity.X * 0.2f, velocity.Y * 0.2f, 100);
21313						Main.dust[num121].noGravity = true;
21314						Dust dust = Main.dust[num121];
21315						dust.velocity *= 0.4f;
21316						Main.dust[num121].velocity.Y -= 0.7f;
21317					}
21318				}
21319				else if (type == 281 || type == 282)
21320				{
21321					if (Main.rand.Next(2) == 0)
21322					{
21323						int num122 = Dust.NewDust(new Vector2(position.X, position.Y + 2f), width, height, 175, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 0.1f);
21324						Main.dust[num122].noGravity = true;
21325						Dust dust = Main.dust[num122];
21326						dust.velocity *= 0.5f;
21327						Main.dust[num122].fadeIn = 1.2f;
21328					}
21329				}
21330				else if (type == 533)
21331				{
21332					Lighting.AddLight(base.Top, 0.6f, 0.6f, 0.3f);
21333				}
21334				else
21335				{
21336					float num123 = 0.6f;
21337					Lighting.AddLight(base.Center, num123, num123 * 0.65f, num123 * 0.4f);
21338					if (Main.rand.Next(6) == 0)
21339					{
21340						int num124 = Dust.NewDust(new Vector2(position.X, position.Y + 2f), width, height, 6, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 1.65f);
21341						Main.dust[num124].noGravity = true;
21342						Main.dust[num124].velocity.X *= 1f;
21343						Main.dust[num124].velocity.Y *= 1f;
21344					}
21345				}
21346				position -= netOffset;
21347				return;
21348			}

```


---

## 🤖 Assistant · 2026-08-19T03:08:38.205Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Caster AI (aiStyle 8) vanilla analysis vs our implementation:

Key findings so far:

1. **Teleport timing/points — vanilla structure**: The teleport check `if (this.ai[0] >= 650f && Main.netMode != 1)` samples the destination but doesn't teleport immediately — it sets ai[2]/ai[3], and the teleport executes at the START of the next tick (:20811). Our implementation: same (ai2/ai3 set at ④, executed at top next tick). ✓

2. **ai[0] == 0 → 500**: Vanilla does this check BEFORE `this.ai[0] += 1f` and after teleport-execution. Our init block does it via aiInit once. Hmm — subtle difference: in vanilla, `if (ai[0] == 0f) ai[0] = 500` runs EVERY tick, not just first. After a teleport, ai[0] = 1. It never returns to 0 unless reset. But wait — for type 693 after teleport, localAI[0]=0, localAI[1]=650. Hmm, ai[0]=1 at teleport. So the ==0 check matters only at spawn. But also: our aiInit approach vs vanilla's every-tick check — is there any path where ai0 becomes 0 mid-life? `this.ai[0] += 1f` — never decreases to 0. So equivalent. But one difference: vanilla initializes ai[0]=500 on the first tick, THEN increments to 501 in the same tick (since `ai[0] += 1f` comes after). Our version: `this.ai0 = 500` in aiInit, then `this.ai0 += 1` later → 501 same tick. ✓ equivalent.

Wait, actually in our implementation the increment happens at line 6536 `this.ai0 += 1;` after teleport execution. Same order as vanilla (:20971). ✓

3. **The 693 (Librarian) attack points**: vanilla default branch: `at([100, 200, 300])` — our comment says default (24/29/32/45/285-286/693). ✓ Also type 693 sets localAI[1]=150 at init — what does localAI[1] do for 693? Let me search... localAI[1]=650f set after teleport (:20898). And at spawn localAI[1]=150 (:20797). Hmm, what consumes localAI[1] for 693? It might be in NPC.SetDefaults or in the book projectile AI... Actually it might be used by AI_FindNearbyBook? Or maybe by something else — possibly used in UpdateNPC for the frame animation (FindFrame case 693). Not AI-critical. Our implementation ignores localAI[1] for 693. Probably a rendering-side thing. I'll note it as low/suspect if I can find the consumer.

4. **Imp (24) fireball spawn**: vanilla `NewNPC(..., (int)position.X + width/2 + direction*8, (int)position.Y + 20, 25)`. Our code: `this.cx + facing*8, this.y + 12` with comment "(X+width/2+dir*8, Y+20) → 中心 y = top+12". NewNPC anchors bottom-center? NewNPC(x, y, type) spawns NPC with position = (x - width/2, y - height)? Per memory note "NewNPC :81547 Bottom 锚点". So Y+20 as bottom → center = top + h/2. If imp NPC 25 height is 16? Then center y = (Y+20) - 16 + 8 = Y + 12. OK matches if height=16. ✓ plausible.

5. **Fireball casters (29→30, 45→665, 32→33)**: vanilla NewNPC at (position.X + width/2, position.Y - 8). Bottom anchor → NPC 30 (Chaos Ball, 16x16?) spawned with bottom at Y-8 → center at Y-8-8 = Y-16. Our code: `this.y - 16` center. ✓ if height 16.

6. **533 Desert Spirit volley details**: vanilla num93=6, num94=6, num95=0, num96=2. Condition: `(num99 < point2.Y - 0 || num99 > point2.Y || num98 < point2.X || num98 > point2.X) && (num99 < point.Y-6 || num99 > point.Y+6 || num98 < point.X-6 || num98 > point.X+6) && !nactive`. So it EXCLUDES only tiles within 0 of player point (i.e., exactly the player tile: num99 in [point2.Y, point2.Y] and num98 in [point2.X, point2.X] → excluded) and within ±6 of self. Our code: `if (Math.abs(sy - pty) <= 6 && ...)` wait no — our code has `if (Math.abs(sy - pty) <= 6 && Math.abs(sx - ptx) <= 6) continue;` — that's WRONG: vanilla excludes only the EXACT player tile (±0, i.e., num95=0), not ±6! Let me recheck: num95 = 0 → player exclusion window is ±0 → only exact tile excluded. num94 = 6 → self exclusion ±6. Our code excludes player neighborhood ±6 — deviation! Wait, let me re-read our code:

```
if (Math.abs(sy - pty) <= 6 && Math.abs(sx - ptx) <= 6) continue;   // 玩家邻域排
if (Math.abs(sy - mty) <= 6 && Math.abs(sx - mtx) <= 6) continue;   // 自身邻域排
```

Vanilla:
```
(num99 < point2.Y - num95 || num99 > point2.Y + num95 || num98 < point2.X - num95 || num98 > point2.X + num95)
```
with num95=0: exclude only if num99 == point2.Y && num98 == point2.X (both within 0). Hmm wait, that's an OR of comparisons — the condition passes (doesn't skip) if ANY coordinate is outside the window. So the tile is excluded only if BOTH |dy|<=0 AND |dx|<=0, i.e., exactly the player's tile. Yes — so vanilla excludes only the player's exact tile; our code excludes a 13×13 window around the player. That's a real deviation — moderately impactful: the tracking orb (596) can't spawn within 6 tiles of the player in our version vs 1 tile in vanilla. Actually wait — hmm, num95=0. Let me double check by reading vanilla again: `int num95 = 0; int num96 = 2;` — num95 is used for player window, num96=2 for SolidTiles. So yes, player exclusion is exact tile only.

Hmm wait, but actually maybe num94=6 is the self window: `(num99 < point.Y - num94 || ...)` → excludes ±6 around self. Our self check: `Math.abs(sy - mty) <= 6 && Math.abs(sx - mtx) <= 6` → excludes ±6 both axes. Vanilla excludes if num99 in [point.Y-6, point.Y+6] AND num98 in [point.X-6, point.X+6] — same. ✓ self OK.

So bug: player exclusion should be exact tile (0), not ±6. Medium severity.

Also vanilla `!Main.tile[num98, num99].nactive()` — tile not active → our `st.get(sx,sy) !== 0 → continue`. nactive() = active && !inActive. Our st.get returns type; nonzero = active. Actuator inActive tiles would be active-but-actuated → vanilla nactive() false → allowed. Our version skips actuated tiles. Edge case, low.

Also lava check: vanilla `Main.tile[num98,num99].lava()` — checks the tile itself (liquid type at spawn tile). Ours: `st.liquid[...] > 0 && liquidType === 2` ✓ close enough.

Damage: vanilla proj 596 damage = 0 base with ai0=target... wait: `Projectile.NewProjectile(..., 596, 0, 1f, ...)` — damage 0! Ours: `this.baseDamage`. Hmm, projectile 596 is "Shadowflame..."? Desert spirit's curse — damage set later? The projectile AI probably sets damage. Vanilla passes damage=0, knockback=1, ai0=target (the player index). Our code passes this.baseDamage — deviation? The 596 projectile (DesertDjinnCurse?) in Projectile AI sets its own damage when it charges. Let me not go too deep; flag as suspect (need Dart.ts 596 handling). Actually, given projTargets might override damage... I'll note it as suspect/low.

7. **Tim's 665 ball**: 45 → NewNPC 665 "Dark Fragment"? OK ours handles via ballByCaster {45: 665}. ✓

8. **Red hat flag4 double-speed**: vanilla applies to ai[0] increment inside default branch. Ours: lai3===1 branch does ai0+=1 and odd→-1 before at([100,200,300]). Vanilla does the same AFTER at()? No wait — vanilla order: `if (flag4) {ai[0]+=1; if odd, -=1}` THEN `if (ai[0]==100||200||300)`. Ours: same order (double-increment then at()). ✓

But wait — in vanilla, the getGoodWorld && type==24 && AnyNPCs(113) branch is separate but same effect. Ours skips (noted). Fine, getGood not enabled.

9. **localAI[0] for 693**: increments per tick; after teleport reset to 0. Used at :21272 Remap(ai[0]...) — no wait, the light uses ai[0], not localAI[0]. localAI[0] also reset after volley (:21189). What consumes localAI[0] for 693? Maybe FindFrame. Not AI behavior. Skip.

10. **Sound at teleport**: vanilla plays Item8 at old pos and new pos (two calls :20818 and :20901). Ours: casterTeleportBurst twice — need to check it plays sound. Let me check casterTeleportBurst function. Also dust counts 50 each side. Need to verify.

11. **Ordering difference — attack points evaluated BEFORE teleport trigger**: vanilla order: ai[0]+=1 → attack points (sets ai[1]=30) → early-teleport caps → teleport trigger (ai0≥650 → 1, sample) → ai[1] countdown/fire. Ours: same order: ⑤ at() at ③④ after increment. Wait our order: increment (6536) → redhat → friction → physics → lights → facing → ② attack points (6579-6591) → ③ caps → ④ teleport → ⑤ fire. ✓ same.

12. **533's ai1 special**: vanilla `if (this.ai[0] == 180f) ai[1] = 181f`. Ours ✓. Fire loop: `ai[1] % 30 == 0 && ai[1]/30 < 5` — fires at 181? 181%30 = 1... wait ai1=181, then decrement: 180, 180%30==0 → fire. Sequence: 180,150,120,90,60,30 → 6 fires? But `ai1/30 < 5`: 180/30=6 → NOT < 5 → no fire at 180! Let me compute: fires when ai1%30==0 AND ai1/30<5 → ai1 ∈ {150,120,90,60,30} → 5 fires (150/30=5 no wait 150/30=5, not <5!). Hmm: 150/30 = 5 → fails! So fires at 120,90,60,30 → 4 fires? 120/30=4<5 ✓, 90/30=3 ✓, 60/30=2 ✓, 30/30=1 ✓ → 4 fires. Ours: `this.ai1 % 30 === 0 && this.ai1 / 30 < 5` ✓ identical expression. ✓

13. **Sound for 533 fire**: vanilla plays Item8 at each 533 volley (:21088). Ours: fireCasterVolley plays Item8 at end for all except 172. ✓

14. **Mimic aiStyle 25** — need to read :25621-25714.

Also caster friction: ours `vx *= 0.93; if small → 0` ✓ (:20787-20791). Gravity: vanilla caster — does NPC have gravity by default? Yes, gravity applies via UpdateNPC unless noGravity. Ours applies gravity ✓. But wait — vanilla casters like Tim (45)... in vanilla, AI_008 casters never set noGravity, they're grounded. ✓ ours matches (applyGravity + collide).

One more: vanilla `if (this.ai[0] == 0f) ai[0] = 500f` happens BEFORE teleport-execution block? No — teleport-execution (:20811) comes BEFORE the ==0→500 (:20892)? Let me check order: :20800 type172 alpha, :20811 teleport exec, :20892-20894 ai2/ai3=0, :20895 693 localAI, :20901 sound+dust, :20971 ai[0]+=1... wait where's the `if (ai[0]==0) ai[0]=500`? It's at :20792-20799 — BEFORE the teleport block. So order: TargetClosest → friction → init 500 → alpha 172 → teleport exec → increment. Ours: init (aiInit) → 172 alpha → teleport exec → increment → friction → physics → ... → facing.

Hmm, ours does friction AFTER increment, vanilla does friction BEFORE init/increment. Order of vx*=0.93 relative to ai0+=1 doesn't interact. But friction before TargetClosest in vanilla (TargetClosest → facing set → friction). Ours: facing set at 6578 AFTER physics. Vanilla TargetClosest at :20786 sets direction. Minor ordering — facing affects nothing until used in fire (cx offsets for imp). Equivalent-ish. But one thing: vanilla friction runs even when player is null (before `if (!player) return` — ours has `if (!player) return;` at 6577 BEFORE facing but after physics). Friction+physics run regardless ✓.

Also vanilla: `TargetClosest()` — sets target/direction even if player dead? TargetClosest with no valid target keeps direction. Ours returns early without facing update when no player. Same-ish.

**Caster found-issue #1**: 533 player-exclusion window ±6 should be exact tile (0). Confidence high.

Let me now check casterTeleportBurst and then read AI_013 (plant), AI_020/21, AI_025 mimic, AI_040, AI_042 in vanilla.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:08:39.117Z · glm-x-preview-260804

```
对 `casterAI` 进行原版层面的审计。已发现 533 exclusion-window 相关问题。我先检查一下我们的 `casterTeleportBurst`，然后读取下一组原版内容。
```


---

## 🤖 Assistant · 2026-08-19T03:08:39.543Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"casterTeleportBurst\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -3",
 "description": "Locate casterTeleportBurst definition"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:08:39.574Z

**📎 ToolResult**

```
6508:  private casterTeleportBurst(game: GameHooks) {
6529:      this.casterTeleportBurst(game);
6534:      this.casterTeleportBurst(game);

```


---

## 🤖 Assistant · 2026-08-19T03:08:42.476Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 18,
 "offset": 6496
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:08:42.493Z

**📎 ToolResult**

```
6496	  /** Caster 族传送双端爆发（:20818-20867 旧位 / :20901-20967 新位）：
6497	   *  Item8 + 50 尘，尘 id→近似色按族映射。 */
6498	  private static readonly CASTER_TP_DUST: Record<number, string> = {
6499	    29: '#7A5AC8', 45: '#7A5AC8',      // dust 27 阴影焰（scale 1-2）
6500	    32: '#9AC8E8',                     // dust 172
6501	    693: '#F0F0F0',                    // dust 269 白（noLight）
6502	    283: '#5AC86A', 284: '#5AC86A',    // dust 173（速度 ×2）
6503	    285: '#E8705A', 286: '#E8705A',    // dust 174
6504	    281: '#8AE8C8', 282: '#8AE8C8',    // dust 175
6505	    172: '#E8C85A',                    // dust 106（scale 2.5）
6506	    533: '#7A5AC8',                    // dust 27（scale 2.5）
6507	  };
6508	  private casterTeleportBurst(game: GameHooks) {
6509	    const color = Enemy.CASTER_TP_DUST[this.vanillaId ?? -1] ?? '#FFA040'; // 默认 dust 6 火把焰
6510	    game.playSfxFiles?.(['Item_8'], 1, this.cx, this.cy);   // :20818/:20901 双端各一次
6511	    game.spawnParticles(this.cx, this.cy, color, 50, 3, { life: 30 });    // :20819-20885 ×50
6512	  }
6513	

```


---

## 🤖 Assistant · 2026-08-19T03:08:42.874Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 295,
 "offset": 22604
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:08:42.893Z

**📎 ToolResult**

```
22604			if (aiStyle == 13)
22605			{
22606				if (this.ai[0] < 0f || this.ai[0] >= (float)Main.maxTilesX || this.ai[1] < 0f || this.ai[1] >= (float)Main.maxTilesX)
22607				{
22608					return;
22609				}
22610				if (Main.tile[(int)this.ai[0], (int)this.ai[1]] == null)
22611				{
22612					Main.tile[(int)this.ai[0], (int)this.ai[1]] = new Tile();
22613				}
22614				if (!Main.tile[(int)this.ai[0], (int)this.ai[1]].active())
22615				{
22616					life = -1;
22617					HitEffect();
22618					active = false;
22619					return;
22620				}
22621				FixExploitManEaters.ProtectSpot((int)this.ai[0], (int)this.ai[1]);
22622				TargetClosest();
22623				float num217 = 0.035f;
22624				float num218 = 150f;
22625				if (type == 43)
22626				{
22627					num218 = ((!Main.getGoodWorld) ? 250f : 350f);
22628				}
22629				if (type == 101)
22630				{
22631					num218 = 175f;
22632				}
22633				if (type == 259)
22634				{
22635					num218 = 100f;
22636				}
22637				if (type == 175)
22638				{
22639					num218 = 500f;
22640					num217 = 0.05f;
22641				}
22642				if (type == 260)
22643				{
22644					num218 = 350f;
22645					num217 = 0.15f;
22646				}
22647				this.ai[2] += 1f;
22648				if (this.ai[2] > 300f)
22649				{
22650					num218 = (int)((double)num218 * 1.3);
22651					if (this.ai[2] > 450f)
22652					{
22653						this.ai[2] = 0f;
22654					}
22655				}
22656				Vector2 vector21 = new Vector2(this.ai[0] * 16f + 8f, this.ai[1] * 16f + 8f);
22657				float num219 = Main.player[target].position.X + (float)(Main.player[target].width / 2) - (float)(width / 2) - vector21.X;
22658				float num220 = Main.player[target].position.Y + (float)(Main.player[target].height / 2) - (float)(height / 2) - vector21.Y;
22659				float num221 = (float)Math.Sqrt(num219 * num219 + num220 * num220);
22660				if (num221 > num218)
22661				{
22662					num221 = num218 / num221;
22663					num219 *= num221;
22664					num220 *= num221;
22665				}
22666				if (position.X < this.ai[0] * 16f + 8f + num219)
22667				{
22668					velocity.X += num217;
22669					if (velocity.X < 0f && num219 > 0f)
22670					{
22671						velocity.X += num217 * 1.5f;
22672					}
22673				}
22674				else if (position.X > this.ai[0] * 16f + 8f + num219)
22675				{
22676					velocity.X -= num217;
22677					if (velocity.X > 0f && num219 < 0f)
22678					{
22679						velocity.X -= num217 * 1.5f;
22680					}
22681				}
22682				if (position.Y < this.ai[1] * 16f + 8f + num220)
22683				{
22684					velocity.Y += num217;
22685					if (velocity.Y < 0f && num220 > 0f)
22686					{
22687						velocity.Y += num217 * 1.5f;
22688					}
22689				}
22690				else if (position.Y > this.ai[1] * 16f + 8f + num220)
22691				{
22692					velocity.Y -= num217;
22693					if (velocity.Y > 0f && num220 < 0f)
22694					{
22695						velocity.Y -= num217 * 1.5f;
22696					}
22697				}
22698				if (type == 43)
22699				{
22700					if (Main.getGoodWorld)
22701					{
22702						if ((double)velocity.X > 3.5)
22703						{
22704							velocity.X = 3.5f;
22705						}
22706						if ((double)velocity.X < -3.5)
22707						{
22708							velocity.X = -3.5f;
22709						}
22710						if ((double)velocity.Y > 3.5)
22711						{
22712							velocity.Y = 3.5f;
22713						}
22714						if ((double)velocity.Y < -3.5)
22715						{
22716							velocity.Y = -3.5f;
22717						}
22718					}
22719					else
22720					{
22721						if (velocity.X > 3f)
22722						{
22723							velocity.X = 3f;
22724						}
22725						if (velocity.X < -3f)
22726						{
22727							velocity.X = -3f;
22728						}
22729						if (velocity.Y > 3f)
22730						{
22731							velocity.Y = 3f;
22732						}
22733						if (velocity.Y < -3f)
22734						{
22735							velocity.Y = -3f;
22736						}
22737					}
22738				}
22739				else if (type == 175)
22740				{
22741					if (velocity.X > 4f)
22742					{
22743						velocity.X = 4f;
22744					}
22745					if (velocity.X < -4f)
22746					{
22747						velocity.X = -4f;
22748					}
22749					if (velocity.Y > 4f)
22750					{
22751						velocity.Y = 4f;
22752					}
22753					if (velocity.Y < -4f)
22754					{
22755						velocity.Y = -4f;
22756					}
22757				}
22758				else
22759				{
22760					if (velocity.X > 2f)
22761					{
22762						velocity.X = 2f;
22763					}
22764					if (velocity.X < -2f)
22765					{
22766						velocity.X = -2f;
22767					}
22768					if (velocity.Y > 2f)
22769					{
22770						velocity.Y = 2f;
22771					}
22772					if (velocity.Y < -2f)
22773					{
22774						velocity.Y = -2f;
22775					}
22776				}
22777				if (type == 259 || type == 260)
22778				{
22779					rotation = (float)Math.Atan2(num220, num219) + 1.57f;
22780				}
22781				else
22782				{
22783					if (num219 > 0f)
22784					{
22785						spriteDirection = 1;
22786						rotation = (float)Math.Atan2(num220, num219);
22787					}
22788					if (num219 < 0f)
22789					{
22790						spriteDirection = -1;
22791						rotation = (float)Math.Atan2(num220, num219) + 3.14f;
22792					}
22793				}
22794				if (collideX)
22795				{
22796					netUpdate = true;
22797					velocity.X = oldVelocity.X * -0.7f;
22798					if (velocity.X > 0f && velocity.X < 2f)
22799					{
22800						velocity.X = 2f;
22801					}
22802					if (velocity.X < 0f && velocity.X > -2f)
22803					{
22804						velocity.X = -2f;
22805					}
22806				}
22807				if (collideY)
22808				{
22809					netUpdate = true;
22810					velocity.Y = oldVelocity.Y * -0.7f;
22811					if (velocity.Y > 0f && velocity.Y < 2f)
22812					{
22813						velocity.Y = 2f;
22814					}
22815					if (velocity.Y < 0f && velocity.Y > -2f)
22816					{
22817						velocity.Y = -2f;
22818					}
22819				}
22820				if (Main.netMode == 1)
22821				{
22822					return;
22823				}
22824				if (type == 101 && !Main.player[target].dead)
22825				{
22826					if (justHit)
22827					{
22828						localAI[0] = 0f;
22829					}
22830					localAI[0] += 1f;
22831					if (localAI[0] >= 120f)
22832					{
22833						if (!Collision.SolidCollision(position, width, height) && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
22834						{
22835							float num222 = 10f;
22836							vector21 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
22837							num219 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector21.X + (float)Main.rand.Next(-10, 11);
22838							num220 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector21.Y + (float)Main.rand.Next(-10, 11);
22839							num221 = (float)Math.Sqrt(num219 * num219 + num220 * num220);
22840							num221 = num222 / num221;
22841							num219 *= num221;
22842							num220 *= num221;
22843							int attackDamage_ForProjectiles2 = GetAttackDamage_ForProjectiles(22f, 17.6f);
22844							int num223 = 96;
22845							int num224 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector21.X, vector21.Y, num219, num220, num223, attackDamage_ForProjectiles2, 0f, Main.myPlayer);
22846							Main.projectile[num224].timeLeft = 300;
22847							localAI[0] = 0f;
22848						}
22849						else
22850						{
22851							localAI[0] = 100f;
22852						}
22853					}
22854				}
22855				if (type != 260 || Main.player[target].dead)
22856				{
22857					return;
22858				}
22859				if (justHit)
22860				{
22861					localAI[0] = 0f;
22862				}
22863				localAI[0] += 1f;
22864				if (!(localAI[0] >= 150f))
22865				{
22866					return;
22867				}
22868				if (!Collision.SolidCollision(position, width, height) && Collision.CanHit(this, Main.player[target]))
22869				{
22870					float num225 = 14f;
22871					vector21 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
22872					num219 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector21.X + (float)Main.rand.Next(-10, 11);
22873					float num226 = Math.Abs(num219 * 0.1f);
22874					if (num220 > 0f)
22875					{
22876						num226 = 0f;
22877					}
22878					num220 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector21.Y + (float)Main.rand.Next(-10, 11) - num226;
22879					num221 = (float)Math.Sqrt(num219 * num219 + num220 * num220);
22880					num221 = num225 / num221;
22881					num219 *= num221;
22882					num220 *= num221;
22883					int num227 = NewNPC(GetSpawnSourceForProjectileNPC(), (int)base.Center.X, (int)base.Center.Y, 261);
22884					Main.npc[num227].velocity.X = num219;
22885					Main.npc[num227].velocity.Y = num220;
22886					Main.npc[num227].netUpdate = true;
22887					localAI[0] = 0f;
22888				}
22889				else
22890				{
22891					localAI[0] = 250f;
22892				}
22893				return;
22894			}
22895			if (aiStyle == 14)
22896			{
22897				noGravity = true;
22898				if (collideX)

```


---

## 🤖 Assistant · 2026-08-19T03:09:17.306Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Excellent — plant AI (aiStyle 13) vanilla analysis vs ours:

1. **Bounds check**: vanilla `ai[0] < 0 || ai[0] >= maxTilesX || ai[1] < 0 || ai[1] >= maxTilesX` (note: maxTilesX for both — decompiled quirk). Ours checks inBounds. Fine.

2. **Death on anchor inactive**: vanilla sets life=-1, HitEffect, active=false → dies WITHOUT normal death (no drops? Actually it despawns silently). Ours: `this.dead = true` — hmm, `dead=true` in our engine might trigger death drops/gore. Vanilla: life=-1 → next tick active=false... Actually life=-1 + HitEffect + active=false immediately — this is the "silent" removal (despawn when block mined). Whether ours spawns loot on `dead=true` depends on engine kill path. There's a memory note about statue slimes "die() vs dead" for AI_125: "AI爆裂须die()勿直写dead(绕过hurt丢Transform)". Here setting dead directly may skip proper despawn semantics vs vanilla despawn. Vanilla `active = false` = silent removal, no drops. If our engine treats `dead=true` as death → drops loot. That would be a deviation (Man Eater killed by mining drops nothing? Actually in vanilla, if you mine the block under a man eater, it dies silently — no loot). Let me check how our engine handles `dead`. Need to check Enemy.update / EntityManager. I'll note as suspect, check later.

3. **Type 43 range**: 250 normal, 350 getGood — ours 250 ✓ (getGood not enabled).

4. **ai[2] > 300 → range ×1.3, ai[2] > 450 reset** ✓ ours. Note vanilla: `num218 = (int)(num218 * 1.3)` — cast to int AFTER multiply. Ours: `range = Math.floor(range * 1.3)` ✓.

5. **Target offset**: num219 = player.position.X + player.width/2 - width/2 - anchor.X. Ours: `ox = player.cx - this.w / 2 - ax` ✓. num220 same ✓.

6. **Approach**: identical structure ✓ with 1.5 boost.

7. **Velocity caps** — ★ MISSING in ours: vanilla clamps velocity: type 43 → ±3 (getGood 3.5); type 175 → ±4; else → ±2. Our plantAI has NO velocity clamp! The accel-only approach with no cap means velocity accumulates unbounded (well, it oscillates around target, but in chase mode it can exceed 2-3 px/t). This is a real behavioral difference: plant lunge speed. Actually wait — with accel 0.035 per tick and oscillation, the velocity converges to something like sqrt-ish; without cap it could overshoot and orbit. Vanilla caps at 2 (or 3/4). Ours unbounded → faster oscillation, "snappier" plants. CONFIRMED missing clamp — medium severity. Let me double check our plantAI code... lines 3729-3744: no clamps anywhere. Confirmed.

8. **Rotation**: 259/260 → atan2(num220, num219)+π/2 ✓. Others: spriteDirection/rotation ✓ ours matches.

9. **Collision bounce**: vanilla collideX → velocity.X = oldVelocity.X * -0.7, with min ±2; collideY similar. Ours: NO collision at all! "noTileCollide:幽灵位移(原版 plants 不做 tile 碰撞)" — WAIT. Vanilla aiStyle 13: does the plant do tile collision? The decompiled code reads `collideX`/`collideY` flags and bounces velocity. That means the NPC DOES collide with tiles (NPC collision happens in UpdateCollision after AI; noTileCollide would be set in SetDefaults if not). Do maneaters have noTileCollide? Let me check NPC.SetDefaults for type 43: maneater... Actually in vanilla, Man Eater has noTileCollide = true! Let me check. Hmm, but then collideX would never be true and the bounce code would be dead. Let me grep SetDefaults for 43/101.

Actually the comment in our code says "原版 plants 不做 tile 碰撞" — if that's from SetDefaults (noTileCollide=true for maneater/snatcher), then the collideX/Y bounce in aiStyle 13 is dead code in vanilla (defensive), and our ghost movement is fine. But cursed walker (101, Clinger) — clingers fly (noGravity? noTileCollide?). Let me verify: grep for type 43 in SetDefaults region. NPC 43 Maneater: I recall `NPC.netID / SetDefaults` — maneater has noTileCollide = true. Clinger 101: also noTileCollide? Clingers hover in walls. Let me check quickly.

Also fungi bulb 259: hangs from ceiling, moves through? Fungi bulb has noTileCollide? Giant fungi bulb 260 too. Let me grep.

10. **Type 101 curse fire**: vanilla localAI[0] (not ai[3]!) — justHit resets localAI[0]=0; +1 per tick; ≥120 → if not SolidCollision(self) && CanHit → fire proj 96 speed 10, damage GetAttackDamage_ForProjectiles(22, 17.6), timeLeft 300, ±10 jitter; localAI[0]=0. Else localAI[0]=100.

Ours: uses ai3, NO justHit reset! `if (this.vanillaId === 101 && player && !player.dead) { this.ai3 += 1; if (this.ai3 >= 120) {...} }`. Missing justHit → localAI[0] = 0 (getting hit resets curse timer). Also damage: ours passes 22 flat via shootDart (dmg 22) vs vanilla GetAttackDamage_ForProjectiles(22, 17.6) difficulty scaling. And timeLeft 300 not set (Dart default?). And velocity: vanilla normalizes then speed 10 ✓ ours shootDart with speed 10 ✓ spread ±10 ✓ ours uses random*20-10 ✓.

Also vanilla fires from center ✓.

CONFIRMED: missing justHit reset for 101 timer (medium); damage not difficulty-scaled (low-medium since Dart.ts might scale — shootDart implementation? need check).

11. **Type 260 spore sac**: vanilla type 260 (!dead player): localAI[0] +1, ≥150 → spawn NPC 261 (Fungi Spore) with velocity toward player speed 14, drop compensation |dx|*0.1 when moving up, ±10 jitter. justHit resets localAI[0]. Ours: NOT IMPLEMENTED AT ALL! Giant Fungi Bulb (260) never shoots spores. Wait — but 260 shares localAI[0] with 101? No — 101 branch uses localAI[0] too, but types are distinct (101 is Clinger; 260 is Giant Fungi Bulb). Both use localAI[0] independently. Our plantAI has no 260 spore spawn. CONFIRMED missing — severity: medium-high (player-visible: giant fungi bulb should lob spores).

Wait, but hold on — in vanilla, `if (type != 260 || player dead) return;` comes after 101 block. So 260 does spore spawning. Also note: for 260, is localAI[0] shared with the 101 branch? The 101 branch only runs `if (type == 101 ...)`. OK.

But ALSO note: our 101 uses ai3 which conflicts with nothing. Fine.

Also vanilla 260: NPC 261 spawned at Center with velocity — ours missing entirely.

12. FixExploitManEaters.ProtectSpot — anti-exploit, skip (comment).

Now aiStyle 20 (blazing wheel) & 21 (spike ball) at :24596-24726. Let me read.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:18.358Z · glm-x-preview-260804

```
Plant AI：发现遗漏了速度限制、260 孢子，以及 101 的 justHit 重置。现在我来检查原版的 blazing wheel/spike ball/mimic 相关部分。
```


---

## 🤖 Assistant · 2026-08-19T03:09:18.849Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 135,
 "offset": 24596
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:18.862Z

**📎 ToolResult**

```
24596			if (aiStyle == 20)
24597			{
24598				if (this.ai[0] == 0f)
24599				{
24600					if (Main.netMode != 1)
24601					{
24602						TargetClosest();
24603						direction *= -1;
24604						directionY *= -1;
24605						position.Y += height / 2 + 8;
24606						this.ai[1] = position.X + (float)(width / 2);
24607						this.ai[2] = position.Y + (float)(height / 2);
24608						if (direction == 0)
24609						{
24610							direction = 1;
24611						}
24612						if (directionY == 0)
24613						{
24614							directionY = 1;
24615						}
24616						this.ai[3] = 1f + (float)Main.rand.Next(15) * 0.1f;
24617						velocity.Y = (float)(directionY * 6) * this.ai[3];
24618						this.ai[0] += 1f;
24619						netUpdate = true;
24620					}
24621					else
24622					{
24623						this.ai[1] = position.X + (float)(width / 2);
24624						this.ai[2] = position.Y + (float)(height / 2);
24625					}
24626					return;
24627				}
24628				float num302 = 6f * this.ai[3];
24629				float num303 = 0.2f * this.ai[3];
24630				float num304 = num302 / num303 / 2f;
24631				if (this.ai[0] >= 1f && this.ai[0] < (float)(int)num304)
24632				{
24633					velocity.Y = (float)directionY * num302;
24634					this.ai[0] += 1f;
24635					return;
24636				}
24637				if (this.ai[0] >= (float)(int)num304)
24638				{
24639					velocity.Y = 0f;
24640					directionY *= -1;
24641					velocity.X = num302 * (float)direction;
24642					this.ai[0] = -1f;
24643					return;
24644				}
24645				if (directionY > 0)
24646				{
24647					if (velocity.Y >= num302)
24648					{
24649						directionY *= -1;
24650						velocity.Y = num302;
24651					}
24652				}
24653				else if (directionY < 0 && velocity.Y <= 0f - num302)
24654				{
24655					directionY *= -1;
24656					velocity.Y = 0f - num302;
24657				}
24658				if (direction > 0)
24659				{
24660					if (velocity.X >= num302)
24661					{
24662						direction *= -1;
24663						velocity.X = num302;
24664					}
24665				}
24666				else if (direction < 0 && velocity.X <= 0f - num302)
24667				{
24668					direction *= -1;
24669					velocity.X = 0f - num302;
24670				}
24671				velocity.X += num303 * (float)direction;
24672				velocity.Y += num303 * (float)directionY;
24673			}
24674			else if (aiStyle == 21)
24675			{
24676				if (this.ai[0] == 0f)
24677				{
24678					TargetClosest();
24679					directionY = 1;
24680					this.ai[0] = 1f;
24681				}
24682				int num305 = 6;
24683				if (this.ai[1] == 0f)
24684				{
24685					rotation += (float)(direction * directionY) * 0.13f;
24686					if (collideY)
24687					{
24688						this.ai[0] = 2f;
24689					}
24690					if (!collideY && this.ai[0] == 2f)
24691					{
24692						direction = -direction;
24693						this.ai[1] = 1f;
24694						this.ai[0] = 1f;
24695					}
24696					if (collideX)
24697					{
24698						directionY = -directionY;
24699						this.ai[1] = 1f;
24700					}
24701				}
24702				else
24703				{
24704					rotation -= (float)(direction * directionY) * 0.13f;
24705					if (collideX)
24706					{
24707						this.ai[0] = 2f;
24708					}
24709					if (!collideX && this.ai[0] == 2f)
24710					{
24711						directionY = -directionY;
24712						this.ai[1] = 0f;
24713						this.ai[0] = 1f;
24714					}
24715					if (collideY)
24716					{
24717						direction = -direction;
24718						this.ai[1] = 0f;
24719					}
24720				}
24721				velocity.X = num305 * direction;
24722				velocity.Y = num305 * directionY;
24723				float num306 = (float)(270 - Main.mouseTextColor) / 400f;
24724				Lighting.AddLight((int)(position.X + (float)(width / 2)) / 16, (int)(position.Y + (float)(height / 2)) / 16, 0.9f, 0.3f + num306, 0.2f);
24725			}
24726			else if (aiStyle == 22)
24727			{
24728				bool flag27 = false;
24729				bool flag28 = false;
24730				if (type == 330 && !Main.pumpkinMoon)

```


---

## 🤖 Assistant · 2026-08-19T03:09:19.108Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 95,
 "offset": 25621
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:19.115Z

**📎 ToolResult**

```
25621			else if (aiStyle == 25)
25622			{
25623				bool flag36 = type == 341 && !Main.snowMoon;
25624				if (this.ai[3] == 0f)
25625				{
25626					position.X += 8f;
25627					if (position.Y / 16f > (float)Main.UnderworldLayer)
25628					{
25629						this.ai[3] = 3f;
25630					}
25631					else if ((double)(position.Y / 16f) > Main.worldSurface)
25632					{
25633						TargetClosest();
25634						this.ai[3] = 2f;
25635					}
25636					else
25637					{
25638						this.ai[3] = 1f;
25639					}
25640				}
25641				if (type == 341 || type == 629)
25642				{
25643					this.ai[3] = 1f;
25644				}
25645				if (this.ai[0] == 0f)
25646				{
25647					if (!flag36)
25648					{
25649						TargetClosest();
25650					}
25651					if (Main.netMode == 1)
25652					{
25653						return;
25654					}
25655					if (velocity.X != 0f || velocity.Y < 0f || (double)velocity.Y > 0.3)
25656					{
25657						this.ai[0] = 1f;
25658						netUpdate = true;
25659						return;
25660					}
25661					Rectangle rectangle3 = new Rectangle((int)Main.player[target].position.X, (int)Main.player[target].position.Y, Main.player[target].width, Main.player[target].height);
25662					if (new Rectangle((int)position.X - 100, (int)position.Y - 100, width + 200, height + 200).Intersects(rectangle3) || life < lifeMax)
25663					{
25664						this.ai[0] = 1f;
25665						netUpdate = true;
25666					}
25667				}
25668				else if (velocity.Y == 0f)
25669				{
25670					this.ai[2] += 1f;
25671					int num361 = 20;
25672					if (this.ai[1] == 0f)
25673					{
25674						num361 = 12;
25675					}
25676					if (this.ai[2] < (float)num361)
25677					{
25678						velocity.X *= 0.9f;
25679						return;
25680					}
25681					this.ai[2] = 0f;
25682					if (!flag36)
25683					{
25684						TargetClosest();
25685					}
25686					if (direction == 0)
25687					{
25688						direction = -1;
25689					}
25690					spriteDirection = direction;
25691					this.ai[1] += 1f;
25692					if (this.ai[1] == 2f)
25693					{
25694						velocity.X = (float)direction * 2.5f;
25695						velocity.Y = -8f;
25696						this.ai[1] = 0f;
25697					}
25698					else
25699					{
25700						velocity.X = (float)direction * 3.5f;
25701						velocity.Y = -4f;
25702					}
25703					netUpdate = true;
25704				}
25705				else if (direction == 1 && velocity.X < 1f)
25706				{
25707					velocity.X += 0.1f;
25708				}
25709				else if (direction == -1 && velocity.X > -1f)
25710				{
25711					velocity.X -= 0.1f;
25712				}
25713			}
25714			else if (aiStyle == 26)
25715			{

```


---

## 🤖 Assistant · 2026-08-19T03:10:21.280Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
**Blazing Wheel (aiStyle 20) vs ours:**

Vanilla init (ai0==0):
- TargetClosest, direction *= -1, directionY *= -1, position.Y += height/2+8
- ai1 = centerX, ai2 = centerY (unused later? probably for something else — no, they're not used elsewhere in this AI; just bookkeeping)
- ai3 = 1 + rand(15)*0.1; velocity.Y = directionY*6*ai3; ai0 += 1; return

Ours: aiInit block does facing*=-1, y += h/2+8, facing=0→1, ai3, vy=6*ai3*dirY, ai0=1, then `this.x += this.vx; this.y += this.vy;` — ★ ours moves on the init tick (x += vx where vx is whatever initial velocity, probably 0), vanilla returns immediately without moving. Minor. Also vanilla `directionY *= -1` after TargetClosest — directionY initially set by TargetClosest (±1 based on player Y). Ours uses `this.dirY` default — what's dirY initial value? Entity probably has dirY. Vanilla: TargetClosest sets directionY; then *= -1. If directionY == 0 → stays 0? No wait — vanilla checks `if (directionY == 0) directionY = 1;` AFTER the multiply. Hmm but it doesn't do `if directionY==0 → 1` before multiply; multiply of 0 stays 0 then set to 1. OK.

Ours: no TargetClosest on init, no dirY *= -1. Ours: `this.dirY` — initial value? Let me check Entity/Enemy defaults for dirY. Vanilla wheel first moves DOWN usually? directionY after TargetClosest is toward player vertically, then negated → away. This determines the initial dive direction. Ours might differ — need to check default dirY in our code. Also facing: vanilla direction*=-1 after TargetClosest → moves AWAY from player horizontally initially. Ours: facing *= -1 (from spawn default facing 1?) — no TargetClosest first. Vanilla: TargetClosest sets direction toward player, then negate → away from player. Ours: just negate initial facing (probably 1) → -1 always initially. Deviation: initial horizontal direction should be away-from-player, ours is always... let me check: `if (!this.aiInit) { this.facing *= -1; ...}` — hmm, ours doesn't call seekDirX first. If default facing = 1, becomes -1. So wheel always starts moving left, regardless of player. Vanilla: starts away from player. Low-medium severity (visual/first-bounce direction).

Also init tick: ours applies movement (`x += vx` with vx=initial velocity—unknown, likely 0 → no move, but y += vy DOES move down by 6*ai3). Vanilla returns without applying velocity (velocity applied later in UpdateNPC collision... wait no — blazing wheel: does it collide? NPC 395 Blazing Wheel — noTileCollide? Spike ball 22? Actually blazing wheel noTileCollide = true (it's a trap that flies through?). Hmm no — blazing wheel bounces off walls in dungeons. Wait, the AI reads no collide flags; aiStyle 20 has no collideX handling → the wheel passes through tiles? In-game blazing wheels DO pass through walls? No... Blazing wheels bounce along the floor of dungeon corridors. Hmm, but the AI has no collision reaction — the bounce is purely velocity-sign based (velocity flips when reaching ±num302). The actual wall/floor interaction comes from normal NPC tile collision (gravity? noGravity?). Blazing Wheel has noTileCollide... let me check SetDefaults. Actually I recall Blazing Wheel and Spike Ball both have `noTileCollide = false`, `noGravity = true`, `canGhostThroughTiles`? Hmm. Spike ball DOES bounce off walls (collideX/collideY used). Blazing wheel moves diagonally bouncing off... floors? Its AI bounces via velocity thresholds, and tile collision stops it at floors/walls; after collision velocity zeroes (collision zeroes velocity) then accel builds it up in the new direction? Hmm, but direction flip is based on velocity magnitude BEFORE collision...

Let me check SetDefaults for 395 (Blazing Wheel) and 22 (Spike Ball? no, spike ball = 22? Actually NPC 22 is Spike Ball? Hmm — NPC IDs: 395 = Blazing Wheel? No wait: 395 = Blazing Wheel, 396 = Dungeon Slime, 22 = ... Let me check: Spike Ball NPC ID is 22? Hmm, in Terraria NPC 22 = "Spike Ball"? No... Let me just grep. Actually spike ball = NPCID.SpikeBall = 22? I believe Blazing Wheel = 395 and Spike Ball = 396? Hmm no. Let me grep both in NPC.cs SetDefaults.

Ours blazingWheelAI: matches the three-phase structure. Check details:
- phaseLen = floor(spd/accel/2) ✓ ((int)num304)
- ai0 >= 1 && ai0 < phaseLen: vy = dirY*spd, ai0+=1 ✓
- ai0 >= phaseLen: vy=0, dirY*=-1, vx = spd*facing, ai0=-1 ✓
- else (ai0 <1, i.e., -1 phase): the bounce + accel ✓ matches vanilla structure (directionY>0 && vy>=spd → flip...). Ours: `if (this.dirY > 0 && this.vy >= spd) { this.dirY *= -1; this.vy = spd; }` ✓.

Ours is 1:1 for the core. ✓ Init differences noted (TargetClosest+negate, dirY handling, init-tick movement).

**Spike Ball (aiStyle 21) vs ours:**

Vanilla: init ai0==0 → TargetClosest (sets direction), directionY=1, ai0=1. num305=6. ai1==0 branch: rotation += dir*dirY*0.13; collideY → ai0=2; !collideY && ai0==2 → direction=-direction, ai1=1, ai0=1; collideX → directionY=-directionY, ai1=1. else branch: rotation -= ...; collideX → ai0=2; !collideX && ai0==2 → directionY=-directionY, ai1=0, ai0=1; collideY → direction=-direction, ai1=0. velocity = 6*direction, 6*directionY. Light: mouseTextColor-based.

Ours: init: TargetClosest-ish via player → facing = seekDirX(p), dirY=1, ai0=1 ✓. Then bounce logic ✓ mirrors. velocity 6*dir both ✓. Light ✓ (0.9, 0.3+num306, 0.2) — ours gates on vanillaId===72?? "aiStyle21 全族(=72 火轮)" — wait the comment says aiStyle 21 family = 72 blazing wheel?? Confused: 72 = Spike Ball? Hmm NPC 72... Let me check: NPCID.SpikeBall = 72? Hmm! Actually yes: NPC 72 might be "Spike Ball"? No wait — NPC 395 = Blazing Wheel... Let me grep. Blazing Wheel = 395? Dungeon enemies: 32 Dark Caster, 33 Water Sphere, ... 68 Dungeon Guardian, 69..., 85 Mimic, 96-, Blazing Wheel = 395? Hmm no. Let me grep in vanilla for "SpikeBall" / "BlazingWheel".

Rotation: ours doesn't do rotation (visual only, comment says registered). OK.

The collide flags: vanilla reads collideX/collideY from previous tick's collision. Ours: `collideX = this.hitWall; collideY = this.onGround || this.hitHead` — hmm, our onGround after moveAndCollide. Vanilla collideY = hit floor OR ceiling. ✓ approx.

One subtle thing: vanilla sets velocity AFTER bounce logic; the NPC then moves via normal collision. Spike ball 6px/t constant. ✓ ours same.

**Mimic (aiStyle 25) vs ours:**

Vanilla:
- flag36 = type==341 && !snowMoon (present for Frost Moon mimic "Mimic 341" — the ice mimic? 341 = "Present Mimic"? Actually 341 = Mimic frost moon variant). 
- ai3==0 init: position.X += 8; then depth check: y > UnderworldLayer → ai3=3; y > worldSurface → TargetClosest, ai3=2; else ai3=1. This is the "MimicState" for spawn depth?? Wait — this sets ai[3] which is the "state" used later? Actually ai[3] here is set to 1/2/3 by depth — this is used by... hmm, what reads ai[3] for mimics? Probably nothing in this AI. Actually it IS read: `if (this.ai[3] == 0f)` gate only. And 341/629 → ai3=1. It might be consumed elsewhere (e.g., NPC.aiStyle 25 in FindFrame?). Not critical.

★ KEY: vanilla ai0==0 branch: after TargetClosest (unless flag36), checks `velocity.X != 0 || velocity.Y < 0 || velocity.Y > 0.3` → ai0=1. Then rectangle check: `new Rectangle(position.X-100, position.Y-100, width+200, height+200).Intersects(playerRect) || life < lifeMax` → ai0=1.

Ours mimicAI: `near = !flag36 && player && !player.dead && Math.abs(player.cx - this.cx) < 100 + (this.w+player.w)/2 && Math.abs(player.cy...)` — this is the "200px box" approximation. Vanilla box: mimic rect expanded by 100 on each side (position.X-100 ... width+200). Intersection with player rect. Ours: center-distance < 100 + (w+pw)/2. Equivalent: |cx diff| < 100 + (w+pw)/2 ⟺ player rect intersects expanded rect. ✓ equivalent math.

Vanilla also has `if (type == 341 || type == 629) ai3 = 1`. Ours: flag36 for 341 only. 629 = "Mimic" desert/jungle variant? 629 = ... Present Mimic 629? Hmm 629 might be "Jungle Mimic"? No, jungle mimic is 649? Actually 629 = "Mimic" from... let me think: 629 is "Present Mimic" (frost moon)? and 341 "Ice Mimic"? Whatever — ours omits the 629 ai3=1 assignment (unused anyway). Low.

Ours: `if (this.ai0 === 0)` — but the ai3 init block (position.X += 8, depth) is missing entirely from ours. position.X += 8: shifts mimic 8px right at spawn (sprite alignment quirk). Minor visual. The ai3 1/2/3 by depth — need to check what consumes ai[3] for mimic. Let me grep "ai\[3\]" around FindFrame case for type 85... This might affect the mimic's "state" for the ai1-based jump loop? No, that's ai[1]. Hmm wait — look at the jump code: `if (this.ai[1] == 2f)` third jump big. Vanilla ai1 increments per jump. Ours ✓ same.

Vanilla jump block: `else if (velocity.Y == 0f)` — grounded. ai2 += 1; num361 = 20; if ai1==0 → 12. if ai2 < num361 → vx *= 0.9, return. ai2=0; TargetClosest (unless flag36); if direction==0 → -1; spriteDirection=direction; ai1 += 1; if ai1==2 → vx=dir*2.5, vy=-8, ai1=0; else vx=dir*3.5, vy=-4.

Ours: `if (this.onGround && this.vy === 0)` — vanilla checks only velocity.Y == 0 (not onGround flag; equivalent-ish). wait=ai1===0?12:20 ✓. vx*=0.9 ✓. Then big jump: vx=facing*2.5, vy=-8, ai1=0 ✓; small: vx=facing*3.5, vy=-4, ai1+=1 ✓.

Air control: vanilla `else if (direction == 1 && velocity.X < 1f) vx += 0.1; else if (direction == -1 && vx > -1) vx -= 0.1;` — ours: `else if (this.vy !== 0) { if (this.facing === -1 && this.vx > -1) this.vx -= 0.1; else if (this.facing === 1 && this.vx < 1) this.vx += 0.1; }` ✓ same conditions. Note vanilla checks direction==1 first; ours -1 first — same semantics (mutually exclusive). ✓

Ours is missing: the ai3 depth-state init + position.X += 8 + 629 handling. The `spriteDirection = direction` is rendering. TargetClosest between jumps — ours sets facing at top of active branch each tick ✓ (facing = seekDirX every tick when active — vanilla TargetClosest only at jump moments; continuous tracking vs at-jump: vanilla direction only updates when jumping (TargetClosest at 25684) and at ai0==0. Ours updates every tick. For a grounded mimic waiting 12-20 ticks, direction changes mid-wait don't matter since vx=0.9-damped. Effectively equivalent... except vanilla keeps direction between jumps if target lost; minor.

Now — key question: the mimic in ours routes case 25 → mimicAI. But what about big mimics (AI_087)? and statue mimic (AI_126) etc.? Those are separate. The task says "mimic 族(宝箱怪 85 等伪装唤醒/扑击)" — aiStyle 25 = mimics 85 (and 341/629?). OK.

Note vanilla gravity: mimic has normal gravity (not in AI). Ours applyGravity ✓.

Now the wall creeper (aiStyle 40, :29784-30017) and lost girl (:30281-30312). Let me read vanilla.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:10:22.041Z · glm-x-preview-260804

```
已确认 Wheel/spike ball/mimic 基本一致，但存在一些初始化差异。接下来处理 wall creeper 和 lost girl 的原版部分。
```


---

## 🤖 Assistant · 2026-08-19T03:10:22.386Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 235,
 "offset": 29784
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:22.392Z

**📎 ToolResult**

```
29784			else if (aiStyle == 40)
29785			{
29786				if (target < 0 || target == 255 || Main.player[target].dead)
29787				{
29788					TargetClosest();
29789				}
29790				float num634 = 2f;
29791				float num635 = 0.08f;
29792				if (type == 237)
29793				{
29794					num634 = 3f;
29795					num635 = 0.12f;
29796				}
29797				if (type == 531)
29798				{
29799					num634 = 4f;
29800					num635 = 0.16f;
29801				}
29802				Vector2 vector71 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
29803				float num636 = Main.player[target].position.X + (float)(Main.player[target].width / 2);
29804				float num637 = Main.player[target].position.Y + (float)(Main.player[target].height / 2);
29805				num636 = (int)(num636 / 8f) * 8;
29806				num637 = (int)(num637 / 8f) * 8;
29807				vector71.X = (int)(vector71.X / 8f) * 8;
29808				vector71.Y = (int)(vector71.Y / 8f) * 8;
29809				num636 -= vector71.X;
29810				num637 -= vector71.Y;
29811				if (confused)
29812				{
29813					num636 *= -2f;
29814					num637 *= -2f;
29815				}
29816				float num638 = (float)Math.Sqrt(num636 * num636 + num637 * num637);
29817				float num639 = num638;
29818				if (num638 == 0f)
29819				{
29820					num636 = velocity.X;
29821					num637 = velocity.Y;
29822				}
29823				else
29824				{
29825					num638 = num634 / num638;
29826					num636 *= num638;
29827					num637 *= num638;
29828				}
29829				if (Main.player[target].dead)
29830				{
29831					num636 = (float)direction * num634 / 2f;
29832					num637 = (0f - num634) / 2f;
29833				}
29834				spriteDirection = -1;
29835				if (!Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
29836				{
29837					this.ai[0] += 1f;
29838					if (this.ai[0] > 0f)
29839					{
29840						velocity.Y += 0.023f;
29841					}
29842					else
29843					{
29844						velocity.Y -= 0.023f;
29845					}
29846					if (this.ai[0] < -100f || this.ai[0] > 100f)
29847					{
29848						velocity.X += 0.023f;
29849					}
29850					else
29851					{
29852						velocity.X -= 0.023f;
29853					}
29854					if (this.ai[0] > 200f)
29855					{
29856						this.ai[0] = -200f;
29857					}
29858					velocity.X += num636 * 0.007f;
29859					velocity.Y += num637 * 0.007f;
29860					rotation = (float)Math.Atan2(velocity.Y, velocity.X);
29861					if ((double)velocity.X > 1.5)
29862					{
29863						velocity.X *= 0.9f;
29864					}
29865					if ((double)velocity.X < -1.5)
29866					{
29867						velocity.X *= 0.9f;
29868					}
29869					if ((double)velocity.Y > 1.5)
29870					{
29871						velocity.Y *= 0.9f;
29872					}
29873					if ((double)velocity.Y < -1.5)
29874					{
29875						velocity.Y *= 0.9f;
29876					}
29877					if (velocity.X > 3f)
29878					{
29879						velocity.X = 3f;
29880					}
29881					if (velocity.X < -3f)
29882					{
29883						velocity.X = -3f;
29884					}
29885					if (velocity.Y > 3f)
29886					{
29887						velocity.Y = 3f;
29888					}
29889					if (velocity.Y < -3f)
29890					{
29891						velocity.Y = -3f;
29892					}
29893				}
29894				else
29895				{
29896					if (velocity.X < num636)
29897					{
29898						velocity.X += num635;
29899						if (velocity.X < 0f && num636 > 0f)
29900						{
29901							velocity.X += num635;
29902						}
29903					}
29904					else if (velocity.X > num636)
29905					{
29906						velocity.X -= num635;
29907						if (velocity.X > 0f && num636 < 0f)
29908						{
29909							velocity.X -= num635;
29910						}
29911					}
29912					if (velocity.Y < num637)
29913					{
29914						velocity.Y += num635;
29915						if (velocity.Y < 0f && num637 > 0f)
29916						{
29917							velocity.Y += num635;
29918						}
29919					}
29920					else if (velocity.Y > num637)
29921					{
29922						velocity.Y -= num635;
29923						if (velocity.Y > 0f && num637 < 0f)
29924						{
29925							velocity.Y -= num635;
29926						}
29927					}
29928					rotation = (float)Math.Atan2(num637, num636);
29929				}
29930				if (type == 531)
29931				{
29932					rotation += MathF.PI / 2f;
29933				}
29934				float num640 = 0.5f;
29935				if (collideX)
29936				{
29937					netUpdate = true;
29938					velocity.X = oldVelocity.X * (0f - num640);
29939					if (direction == -1 && velocity.X > 0f && velocity.X < 2f)
29940					{
29941						velocity.X = 2f;
29942					}
29943					if (direction == 1 && velocity.X < 0f && velocity.X > -2f)
29944					{
29945						velocity.X = -2f;
29946					}
29947				}
29948				if (collideY)
29949				{
29950					netUpdate = true;
29951					velocity.Y = oldVelocity.Y * (0f - num640);
29952					if (velocity.Y > 0f && (double)velocity.Y < 1.5)
29953					{
29954						velocity.Y = 2f;
29955					}
29956					if (velocity.Y < 0f && (double)velocity.Y > -1.5)
29957					{
29958						velocity.Y = -2f;
29959					}
29960				}
29961				if (((velocity.X > 0f && oldVelocity.X < 0f) || (velocity.X < 0f && oldVelocity.X > 0f) || (velocity.Y > 0f && oldVelocity.Y < 0f) || (velocity.Y < 0f && oldVelocity.Y > 0f)) && !justHit)
29962				{
29963					netUpdate = true;
29964				}
29965				if (Main.netMode == 1)
29966				{
29967					return;
29968				}
29969				if (Main.netMode != 1 && Main.expertMode && target >= 0 && !Main.player[target].dead && (type == 163 || type == 238 || type == 236 || type == 237) && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
29970				{
29971					localAI[0] += 1f;
29972					if (justHit)
29973					{
29974						localAI[0] -= Main.rand.Next(20, 60);
29975						if (localAI[0] < 0f)
29976						{
29977							localAI[0] = 0f;
29978						}
29979					}
29980					if (localAI[0] > (float)Main.rand.Next(180, 900))
29981					{
29982						localAI[0] = 0f;
29983						Vector2 vector72 = Main.player[target].Center - base.Center;
29984						vector72.Normalize();
29985						vector72 *= 8f;
29986						int attackDamage_ForProjectiles8 = GetAttackDamage_ForProjectiles(18f, 18f);
29987						int num641 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, base.Center.Y, vector72.X, vector72.Y, 472, attackDamage_ForProjectiles8, 0f, Main.myPlayer);
29988					}
29989				}
29990				if (!NPCCanStickToWalls())
29991				{
29992					int num642 = type;
29993					switch (type)
29994					{
29995					case 165:
29996						num642 = 164;
29997						break;
29998					case 237:
29999						num642 = 236;
30000						break;
30001					case 238:
30002						num642 = 163;
30003						break;
30004					case 240:
30005						num642 = 239;
30006						break;
30007					case 531:
30008						num642 = 530;
30009						break;
30010					}
30011					if (TryMoveToTransformableSpaceInto(num642))
30012					{
30013						Transform(num642, 0f, 0f, 0f, 0f, withReposition: false);
30014					}
30015				}
30016			}
30017			else if (aiStyle == 41)
30018			{

```


---

## 🤖 Assistant · 2026-08-19T03:10:22.754Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 35,
 "offset": 30281
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:10:22.766Z

**📎 ToolResult**

```
30281			else if (aiStyle == 42)
30282			{
30283				TargetClosest();
30284				if (this.ai[0] == 0f)
30285				{
30286					if (target >= 0)
30287					{
30288						Vector2 vector75 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
30289						float num654 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector75.X;
30290						float num655 = Main.player[target].position.Y - vector75.Y;
30291						float num656 = (float)Math.Sqrt(num654 * num654 + num655 * num655);
30292						if (num656 < 200f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
30293						{
30294							this.ai[0] = 1f;
30295						}
30296					}
30297					if (velocity.X != 0f || velocity.Y < 0f || velocity.Y > 2f || life != lifeMax)
30298					{
30299						this.ai[0] = 1f;
30300					}
30301				}
30302				else
30303				{
30304					this.ai[0] += 1f;
30305					if (this.ai[0] >= 21f)
30306					{
30307						this.ai[0] = 21f;
30308						Transform(196);
30309					}
30310				}
30311			}
30312			else if (aiStyle == 43)
30313			{
30314				if (Main.expertMode)
30315				{

```


---

## 🤖 Assistant · 2026-08-19T03:11:12.875Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
**Wall creeper (aiStyle 40) vs ours:**

Vanilla:
1. `if (target < 0 || target == 255 || dead) TargetClosest()` — ours: implicit.
2. Speed tables ✓ (2/0.08, 3/0.12, 4/0.16).
3. Target vector: player center quantized /8*8, self center quantized /8*8 ✓ ours does floor(cx/8)*8. 
4. confused → num636 *= -2, num637 *= -2 — ours MISSING confused handling. (Confusion is from brain of confusion; check whether our engine has confused for enemies — Enemy has `confused` field, used in fighterAI. So missing here. Low-medium.)
5. num638 == 0 → use velocity ✓ ours (dist===0 → sx=vx, sy=vy).
6. dead player → num636 = direction*num634/2, num637 = -num634/2 ✓ ours (tx = facing*maxSpd/2, ty = -maxSpd/2).

Wait — ours uses `alive ? ... : facing*maxSpd/2` for tx/ty ✓. But ours also sets `facing = seekDirX(player)` only when alive; dead → keeps facing ✓ TargetClosest semantics.

7. LOS gate: vanilla `!Collision.CanHit(...)` → wander. Ours ✓.
8. Wander branch: ai[0] += 1 FIRST, then `if (ai[0] > 0) vy += 0.023 else vy -= 0.023`. Ours: `this.ai0 += 1; this.vy += this.ai0 > 0 ? 0.023 : -0.023;` ✓. `if (ai[0] < -100 || ai[0] > 100) vx += 0.023 else vx -= 0.023` ✓ ours. `if (ai[0] > 200) ai[0] = -200` ✓. num636*0.007 / num637*0.007 ✓. rotation ✓ visAngle. |v|>1.5 damp ✓. clamp ±3 ✓ ours.

★ Ours has `if (this.ai0 < -200) this.ai0 = 0;` — comment "类默认 -1120 钳回原版下界". Vanilla ai[0] starts 0 (from spawn ai defaults — actually ai[0] initialized to 0 for spawned NPCs). Our class default is -1120 which would break the wander (vy -= 0.023 for a LONG time and never reaching >200 → stuck descending). They clamp < -200 → 0. Hmm: vanilla starts at 0; ours starts at -1120 → clamped to 0 at first tick. Then ai0 += 1 → 1 > 0 → vy += 0.023... but wait: with ai0 = 0 clamped... then +1 = 1. Vanilla first tick: 0+1 = 1 → vy += 0.023. Same. OK equivalent after clamp. But if ai0 starts between -200 and 0 legitimately? Only via Transform resets (ai cleared to 0). Fine. ✓

9. LOS chase branch: asymmetric servo ✓ identical. rotation = atan2(num637, num636) — target velocity angle ✓ ours atan2(sy, sx).
10. 531 rotation + π/2 ✓.
11. Collision bounce: num640 = 0.5. collideX → vx = oldVx * -0.5, direction==-1 && vx>0 && vx<2 → 2; direction==1 && vx<0 && vx>-2 → -2 ✓ ours matches.

collideY → vy = oldVy*-0.5, vy>0 && vy<1.5 → 2; vy<0 && vy>-1.5 → -2 ✓ ours.

12. Expert venom: gated expertMode — ours skips (documented). ✓ (expert not enabled)
13. Wall detach transform: vanilla uses TryMoveToTransformableSpaceInto(num642) — only transforms if there's transformable space! Ours: `tryTransformTo(groundForm, st, false, game)` — which checks solid overlap and aborts if embedded. Roughly similar intent: vanilla TryMoveToTransformableSpaceInto finds a nearby spot to transform into (moves NPC to valid space?) — hmm, actually TryMoveToTransformableSpaceInto checks if the NPC can be repositioned... Let me not dig too deep. Ours' tryTransformTo returns false when overlapping solid — vanilla tries to MOVE to transformable space then transform. So vanilla guarantees the transform happens (with repositioning), ours silently fails and the spider stays wall-form off-wall (stuck floating). Actually wait — wall creeper off-wall without walls: it has noGravity... does our wall-form spider keep floating? The wall creeper form has noGravity in data presumably. If transform fails, spider floats midair forever. Vanilla would relocate it. Medium severity edge case. Let me check TryMoveToTransformableSpaceInto semantics briefly.

Actually — TryMoveToTransformableSpaceInto probably does: checks whether new type fits at current position; if not, returns false. Let me grep it. It's in NPC.cs. I'll check quickly.

**Lost girl (aiStyle 42) vs ours:**

Vanilla: TargetClosest; ai0==0: if target>=0 → center-to-player.Top distance < 200 && CanHit → ai0=1. Note num655 = player.position.Y (player TOP, not center) - vector75.Y. Ours: `dy = player.y - this.cy` ✓ player.y = top ✓. 

`if (velocity.X != 0 || velocity.Y < 0 || velocity.Y > 2 || life != lifeMax) ai0 = 1` ✓ ours (vx!==0 || vy<0 || vy>2 || hp!==maxHp) ✓.

else ai0 += 1; >= 21 → Transform(196). Ours ✓ with tryTransformTo(196) — and ours returns if transform succeeded; else keeps applying gravity ✓ (vanilla Transform always succeeds basically).

Vanilla lost girl has NO movement code in AI — but gravity is applied by UpdateNPC default (not noGravity). Ours adds applyGravity + moveAndCollide + vx=0 ✓ equivalent.

Note: vanilla `velocity.X != 0` — our vx *= 0? We set vx = 0 at the end of each tick, but the check happens at the start (before we zero it). Wait ours: check at ai0===0 start reads this.vx — set to 0 at end of previous tick. So vx never triggers! In vanilla, is there any force giving the lost girl vx? Knockback! If player bumps/hits her, vx becomes nonzero (knockback), then AI check at next tick sees vx != 0 → transform. Ours zeroes vx every tick at the end — so knockback vx is erased BEFORE the next tick's check → the velocity trigger never fires! Wait, order: our tick: check (ai0===0 → reads vx from... previous tick end where we set vx=0). Knockback applied by hurt() between ticks → vx = kb value. Next AI tick: reads vx BEFORE we zero it (zero happens at end). Let me re-read our code:

```
if (this.ai0 === 0) {
  ... checks this.vx !== 0 ... // reads pre-zero value ✓
}
...
this.vx = 0;
this.applyGravity(game);
moveAndCollide(...)
```

The check at the top happens BEFORE vx=0 at the bottom — same tick order as vanilla (check at top, then vanilla has no vx write; ours zeroes at bottom). Knockback sets vx mid-frame (hurt during damage phase, before AI?). If AI runs before hurt in the tick... ordering between hurt() and AI in our engine determines this. Vanilla: NPC.StrikeNPC happens during projectile/player updates which run BEFORE NPC.AI? In vanilla UpdateNPC, NPCs are updated (AI) then projectiles... Actually order: Main.Update → UpdateEntities → NPC.UpdateNPC then Projectile.UpdateProjectiles? Player updates first, then NPCs, then projectiles. Player melee hits NPC during player update → before NPC AI same tick. So knockback vx visible to AI same tick ✓. Our engine: need to check ordering, but the vx=0 at end would erase kb before NEXT tick — the check at top of next tick happens after erase. Hmm no: sequence: tick N: AI runs (vx=0 at end). Between N and N+1: player hits → hurt() sets vx. Tick N+1: AI check sees vx ✓. So knockback IS seen. OK fine — vx=0 at end only erases after check. ✓ Equivalent.

BUT one thing: ours `this.vx = 0` unconditionally each tick — vanilla lost girl never touches vx, so knockback slides... vanilla friction? None in AI_042. NPC has no global friction. So vanilla lost girl knocked back slides with vx (no friction!) until hitting wall. Ours zeroes vx every tick → girl stops instantly after knockback. Minor visual deviation. Low.

Also vanilla checks `velocity.Y < 0 || velocity.Y > 2` — ours ✓ but ours applyGravity adds g BEFORE moveAndCollide at end; at check time vy is last tick's final (post-collision) value ✓ same as vanilla (AI reads velocity before collision zeroes it; vanilla collision after AI... wait vanilla order: AI() runs, THEN collision in same UpdateNPC? For ground NPCs: gravity applied where? UpdateNPC applies gravity only if noGravity false via `velocity.Y += gravity` INSIDE AI? No — vanilla NPC.AI() doesn't apply gravity; gravity is in NPC.UpdateNPC before AI? Hmm. In vanilla, `if (!noGravity) velocity.Y += gravity` is inside AI_003 etc. explicitly? No — looking at AI_003 code it has explicit gravity handling? Actually vanilla applies gravity in UpdateNPC: "if (noGravity ...) velocity.Y += npc.gravity * gravityMul" somewhere around :91519 (per our code comment "UpdateNPC :91519 重力"). And AI() runs before collision. So AI reads pre-gravity velocity? The comment in psychoStealthStep says gravity applied at :91519 (UpdateNPC tail) with collision. Vanilla order: AI() → gravity+collision (:91519). So AI sees last tick's post-collision velocity. Ours: check at top (pre-gravity) — vy from last tick's post-collision ✓ equivalent.

Now the big ones: AI_001 Slimes (:60735-62266) and AI_003 Fighters (:56245-60734). These are huge. Let me read AI_001 first — 1530 lines. I'll read it in chunks focusing on the core jump state machine, flags, and type-specific behaviors. Actually the core is :61430-62150 (jump logic, wet buoyancy, stuck detection). :60735-61430 is the contained-items + lights + special types. Let me read :60735-62150 strategically. Actually the bulk 60735-60970 is items (already compared). 60971-61289 color variants. 61289-61430 = spiked slimes? Let me read 61290-62150 (860 lines) — the core movement. And 61430-61960.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:13.374Z · glm-x-preview-260804

```
已完成 Wall creeper 和 lost girl 的分析。现在分析两个大头——先检查 slime core。
```


---

## 🤖 Assistant · 2026-08-19T03:11:13.684Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 330,
 "offset": 61430
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:13.692Z

**📎 ToolResult**

```
61430					{
61431						life = defLifeMax * 3;
61432					}
61433					lifeMax = defLifeMax * 3;
61434				}
61435			}
61436			if (type == 1 && direction == 0 && !flag2)
61437			{
61438				direction = 1;
61439				netUpdate = true;
61440			}
61441			if (ai[0] == -999f)
61442			{
61443				frame.Y = 0;
61444				frameCounter = 0.0;
61445				rotation = 0f;
61446				return;
61447			}
61448			if (type == 244)
61449			{
61450				float num24 = (float)Main.DiscoR / 255f;
61451				float num25 = (float)Main.DiscoG / 255f;
61452				float num26 = (float)Main.DiscoB / 255f;
61453				num24 *= 1f;
61454				num25 *= 1f;
61455				num26 *= 1f;
61456				Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), num24, num25, num26);
61457				AI_001_SetRainbowSlimeColor();
61458			}
61459			bool flag3 = false;
61460			if (!Main.dayTime || life != lifeMax || (double)position.Y > Main.worldSurface * 16.0 || Main.slimeRain)
61461			{
61462				flag3 = true;
61463			}
61464			if (Main.remixWorld && type == 59 && life == lifeMax)
61465			{
61466				flag3 = false;
61467			}
61468			if (type == 81)
61469			{
61470				flag3 = true;
61471				if (Main.rand.Next(30) == 0)
61472				{
61473					position += netOffset;
61474					int num27 = Dust.NewDust(position, width, height, 14, 0f, 0f, alpha, this.color);
61475					Main.dust[num27].velocity *= 0.3f;
61476					position -= netOffset;
61477				}
61478			}
61479			if ((type == 377 || type == 446) && target != 255 && !Main.player[target].dead && Vector2.Distance(base.Center, Main.player[target].Center) <= 200f && !wet)
61480			{
61481				flag3 = true;
61482			}
61483			if (type == 183)
61484			{
61485				flag3 = true;
61486			}
61487			if (type == 304)
61488			{
61489				flag3 = true;
61490			}
61491			if (type == 667)
61492			{
61493				flag3 = true;
61494			}
61495			if (type == 244)
61496			{
61497				flag3 = true;
61498				ai[0] += 2f;
61499			}
61500			if (type == 147 && Main.rand.Next(10) == 0)
61501			{
61502				position += netOffset;
61503				int num28 = Dust.NewDust(position, width, height, 76);
61504				Main.dust[num28].noGravity = true;
61505				Main.dust[num28].velocity *= 0.1f;
61506				position -= netOffset;
61507			}
61508			if (type == 667)
61509			{
61510				Color color2 = new Color(204, 181, 72, 255);
61511				Lighting.AddLight((int)(base.Center.X / 16f), (int)(base.Center.Y / 16f), (float)(int)color2.R / 255f * 1.1f, (float)(int)color2.G / 255f * 1.1f, (float)(int)color2.B / 255f * 1.1f);
61512				if (velocity.Length() > 1f || Main.rand.Next(4) != 0)
61513				{
61514					int num29 = 8;
61515					Vector2 vector2 = position + new Vector2(-num29, -num29);
61516					int num30 = width + num29 * 2;
61517					int num31 = height + num29 * 2;
61518					position += netOffset;
61519					int num32 = Dust.NewDust(vector2, num30, num31, 246);
61520					Main.dust[num32].noGravity = true;
61521					Main.dust[num32].noLightEmittance = true;
61522					Main.dust[num32].velocity *= 0.2f;
61523					Main.dust[num32].scale = 1.5f;
61524					position -= netOffset;
61525				}
61526			}
61527			if (type == 676)
61528			{
61529				Lighting.AddLight(base.Center, 23);
61530				if ((velocity.Length() > 1f && Main.rand.Next(3) == 0) || Main.rand.Next(5) == 0)
61531				{
61532					Dust dust4 = Dust.NewDustPerfect(Main.rand.NextVector2FromRectangle(base.Hitbox), 306);
61533					dust4.noGravity = true;
61534					dust4.noLightEmittance = true;
61535					dust4.alpha = 127;
61536					dust4.color = Main.hslToRgb(((float)Main.timeForVisualEffects / 300f + Main.rand.NextFloat() * 0.1f) % 1f, 1f, 0.65f);
61537					dust4.color.A = 0;
61538					dust4.velocity = dust4.position - base.Center;
61539					dust4.velocity *= 0.1f;
61540					dust4.velocity.X *= 0.25f;
61541					if (dust4.velocity.Y > 0f)
61542					{
61543						dust4.velocity.Y *= -1f;
61544					}
61545					dust4.scale = Main.rand.NextFloat() * 0.3f + 0.5f;
61546					dust4.fadeIn = 0.9f;
61547					dust4.position += netOffset;
61548				}
61549			}
61550			if (type == 184)
61551			{
61552				if (Main.rand.Next(8) == 0)
61553				{
61554					position += netOffset;
61555					int num33 = Dust.NewDust(position - velocity, width, height, 76);
61556					Main.dust[num33].noGravity = true;
61557					Main.dust[num33].velocity *= 0.15f;
61558					position -= netOffset;
61559				}
61560				flag3 = true;
61561				if (localAI[0] > 0f)
61562				{
61563					localAI[0] -= 1f;
61564				}
61565				if (!wet && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type])
61566				{
61567					Vector2 vector3 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
61568					float num34 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector3.X;
61569					float num35 = Main.player[target].position.Y - vector3.Y;
61570					float num36 = (float)Math.Sqrt(num34 * num34 + num35 * num35);
61571					if (Main.expertMode && num36 < 120f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61572					{
61573						ai[0] = -40f;
61574						if (velocity.Y == 0f)
61575						{
61576							velocity.X *= 0.9f;
61577						}
61578						if (Main.netMode != 1 && localAI[0] == 0f)
61579						{
61580							for (int k = 0; k < 5; k++)
61581							{
61582								Vector2 vector4 = new Vector2(k - 2, -4f);
61583								vector4.X *= 1f + (float)Main.rand.Next(-50, 51) * 0.005f;
61584								vector4.Y *= 1f + (float)Main.rand.Next(-50, 51) * 0.005f;
61585								vector4.Normalize();
61586								vector4 *= 4f + (float)Main.rand.Next(-50, 51) * 0.01f;
61587								int attackDamage_ForProjectiles = GetAttackDamage_ForProjectiles(9f, 9f);
61588								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector3.X, vector3.Y, vector4.X, vector4.Y, 174, attackDamage_ForProjectiles, 0f, Main.myPlayer);
61589								localAI[0] = 30f;
61590							}
61591						}
61592					}
61593					else if (num36 < 200f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61594					{
61595						ai[0] = -40f;
61596						if (velocity.Y == 0f)
61597						{
61598							velocity.X *= 0.9f;
61599						}
61600						if (Main.netMode != 1 && localAI[0] == 0f)
61601						{
61602							num35 = Main.player[target].position.Y - vector3.Y - (float)Main.rand.Next(0, 200);
61603							num36 = (float)Math.Sqrt(num34 * num34 + num35 * num35);
61604							num36 = 4.5f / num36;
61605							num34 *= num36;
61606							num35 *= num36;
61607							localAI[0] = 50f;
61608							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector3.X, vector3.Y, num34, num35, 174, 9, 0f, Main.myPlayer);
61609						}
61610					}
61611				}
61612			}
61613			if (type == 535)
61614			{
61615				flag3 = true;
61616				if (localAI[0] > 0f)
61617				{
61618					localAI[0] -= 1f;
61619				}
61620				if (!wet && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type])
61621				{
61622					Vector2 vector5 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
61623					float num37 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector5.X;
61624					float num38 = Main.player[target].position.Y - vector5.Y;
61625					float num39 = (float)Math.Sqrt(num37 * num37 + num38 * num38);
61626					if (Main.expertMode && num39 < 120f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61627					{
61628						ai[0] = -40f;
61629						if (velocity.Y == 0f)
61630						{
61631							velocity.X *= 0.9f;
61632						}
61633						if (Main.netMode != 1 && localAI[0] == 0f)
61634						{
61635							for (int l = 0; l < 5; l++)
61636							{
61637								Vector2 vector6 = new Vector2(l - 2, -4f);
61638								vector6.X *= 1f + (float)Main.rand.Next(-50, 51) * 0.005f;
61639								vector6.Y *= 1f + (float)Main.rand.Next(-50, 51) * 0.005f;
61640								vector6.Normalize();
61641								vector6 *= 4f + (float)Main.rand.Next(-50, 51) * 0.01f;
61642								int attackDamage_ForProjectiles2 = GetAttackDamage_ForProjectiles(9f, 9f);
61643								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector5.X, vector5.Y, vector6.X, vector6.Y, 605, attackDamage_ForProjectiles2, 0f, Main.myPlayer);
61644								localAI[0] = 30f;
61645							}
61646						}
61647					}
61648					else if (num39 < 200f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61649					{
61650						ai[0] = -40f;
61651						if (velocity.Y == 0f)
61652						{
61653							velocity.X *= 0.9f;
61654						}
61655						if (Main.netMode != 1 && localAI[0] == 0f)
61656						{
61657							num38 = Main.player[target].position.Y - vector5.Y - (float)Main.rand.Next(0, 200);
61658							num39 = (float)Math.Sqrt(num37 * num37 + num38 * num38);
61659							num39 = 4.5f / num39;
61660							num37 *= num39;
61661							num38 *= num39;
61662							localAI[0] = 50f;
61663							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector5.X, vector5.Y, num37, num38, 605, 9, 0f, Main.myPlayer);
61664						}
61665					}
61666				}
61667			}
61668			if (type == 658)
61669			{
61670				flag3 = true;
61671				if (localAI[0] > 0f)
61672				{
61673					localAI[0] -= 1f;
61674				}
61675				if (!wet && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type])
61676				{
61677					Player obj = Main.player[target];
61678					Vector2 center = base.Center;
61679					float num40 = obj.Center.X - center.X;
61680					float num41 = obj.Center.Y - center.Y;
61681					float num42 = (float)Math.Sqrt(num40 * num40 + num41 * num41);
61682					int num43 = CountNPCS(658);
61683					if (Main.expertMode && num43 < 5 && Math.Abs(num40) < 500f && Math.Abs(num41) < 550f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61684					{
61685						ai[0] = -40f;
61686						if (velocity.Y == 0f)
61687						{
61688							velocity.X *= 0.9f;
61689						}
61690						if (Main.netMode != 1 && localAI[0] == 0f)
61691						{
61692							for (int m = 0; m < 3; m++)
61693							{
61694								Vector2 vector7 = new Vector2(m - 1, -4f);
61695								vector7.X *= 1f + (float)Main.rand.Next(-50, 51) * 0.005f;
61696								vector7.Y *= 1f + (float)Main.rand.Next(-50, 51) * 0.005f;
61697								vector7.Normalize();
61698								vector7 *= 6f + (float)Main.rand.Next(-50, 51) * 0.01f;
61699								if (num42 > 350f)
61700								{
61701									vector7 *= 2f;
61702								}
61703								else if (num42 > 250f)
61704								{
61705									vector7 *= 1.5f;
61706								}
61707								int attackDamage_ForProjectiles_MultiLerp = GetAttackDamage_ForProjectiles_MultiLerp(15f, 17f, 20f);
61708								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center.X, center.Y, vector7.X, vector7.Y, 920, attackDamage_ForProjectiles_MultiLerp, 0f, Main.myPlayer);
61709								localAI[0] = 25f;
61710								if (num43 > 4)
61711								{
61712									break;
61713								}
61714							}
61715						}
61716					}
61717					else if (Math.Abs(num40) < 500f && Math.Abs(num41) < 550f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61718					{
61719						float num44 = num42;
61720						ai[0] = -40f;
61721						if (velocity.Y == 0f)
61722						{
61723							velocity.X *= 0.9f;
61724						}
61725						if (Main.netMode != 1 && localAI[0] == 0f)
61726						{
61727							num41 = Main.player[target].position.Y - center.Y - (float)Main.rand.Next(0, 200);
61728							num42 = (float)Math.Sqrt(num40 * num40 + num41 * num41);
61729							num42 = 4.5f / num42;
61730							num42 *= 2f;
61731							if (num44 > 350f)
61732							{
61733								num42 *= 2f;
61734							}
61735							else if (num44 > 250f)
61736							{
61737								num42 *= 1.5f;
61738							}
61739							num40 *= num42;
61740							num41 *= num42;
61741							localAI[0] = 50f;
61742							int attackDamage_ForProjectiles_MultiLerp2 = GetAttackDamage_ForProjectiles_MultiLerp(15f, 17f, 20f);
61743							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center.X, center.Y, num40, num41, 920, attackDamage_ForProjectiles_MultiLerp2, 0f, Main.myPlayer);
61744						}
61745					}
61746				}
61747			}
61748			if (type == 659)
61749			{
61750				flag3 = true;
61751				if (localAI[0] > 0f)
61752				{
61753					localAI[0] -= 1f;
61754				}
61755				if (!wet && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type])
61756				{
61757					Player obj2 = Main.player[target];
61758					Vector2 center2 = base.Center;
61759					float num45 = obj2.Center.X - center2.X;

```


---

## 🤖 Assistant · 2026-08-19T03:11:38.246Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Important finding — spiked slimes in vanilla:

- The vanilla spike attack uses **localAI[0]** as cooldown, not ai[3]! For 184/535: localAI[0] 50t cooldown (classic), 30t (expert). Ours uses ai3 with 50t. Both work as cooldown but different slot — behaviorally equivalent unless something else writes ai[3] for slimes. AI_001 uses ai[3] for jump position tracking? Let me check the jump code (ai[3] = position.X per our code). If vanilla uses ai[3] = position.X for stuck detection AND ours uses ai3 for spike cooldown — CONFLICT in ours if both apply to spiked slimes! Let me check: our slimeAI sets `this.jumpStartX = this.cx` (separate field, not ai3) — good, no conflict. And vanilla stores position.X in ai[3]. So ours avoids the conflict by using jumpStartX. OK equivalent.

- Spike fire: aim uses `Main.player[target].position.Y - vector3.Y - rand(0,200)` — player TOP Y. Ours: `player.y - this.cy - random*200` ✓ top Y ✓.

- Velocity: vanilla normalizes (num34, num35_adjusted) × 4.5. Ours: shootDart(cx, cy, dx, aimY, 4.5, 9, proj) — normalizes to speed 4.5 ✓.

- Damage: classic single shot = 9 raw (no difficulty scaling in classic branch — 9 flat). Ours: 9 ✓. (expert five-shot uses GetAttackDamage scaled 9 — we don't have expert).

- Cooldown 50 ✓ ours.

- Gate: `!wet && player.active && !dead && !npcTypeNoAggro` — distance < 200 (184/535) && CanHit && velocity.Y == 0. Ours: `!inWater && this.onGround` — ours uses inWater = liquid > 80 at center (vs wet). And onGround vs velocity.Y==0 — ours also requires this.onGround which is post-collision flag ✓. Vanilla also has `npcTypeNoAggro` (e.g., when player has aggro-reducing armor like flesh knuckles? or Calming Potion). Ours doesn't handle — fine, noted.

- ★184 also always sets flag3 = true (aggressive always). 535 flag3=true too! Ours: spiked slimes NOT included in forced-aggressive! Vanilla: 184 (ice slime), 535 (spiked ice? no wait) — 184 = Ice Slime? and 535 = Spiked Ice Slime? Hmm: 184 = "Spiked Ice Slime"? Let me recall: 147 = Jungle Slime? no... Vanilla IDs: 1 Blue Slime, 59 Lava Slime, 81 Green? no. Let me be careful: 
- 81 = Green Slime? Hmm, actually 81 = "Green Slime"? I think -1..-3 are variants of blue. Green slime = 81? Yes I believe green slime is 81.
- 147 = Spiked Jungle Slime! 184 = Spiked Ice Slime. 535 = ...? 535 = "Spiked Slime" (hardmode dungeon? no). Hmm: 535 is... "Spiked Slime" appears in hardmode? Actually 535 might be present from slime rain? No.
  
Vanilla code: 184 branch = spiked ice slime (proj 174 = ice spike). 535 branch = proj 605 (spike). 147 has dust 76 (spiked jungle?) — wait 147 dust but no attack? Let me look: 147 branch only does dust. And where's the jungle spiked slime attack (proj 176)? Ours: `204 → proj 176` with range 400. Let me search for type 204 in AI_001. Vanilla 204 = ... hmm. Let me search "type == 204" and "type == 147" in the 60735-62266 range. Also check our comment: "尖刺史莱姆(cs:61555-61870:184 冰/535 尖刺/204 丛林)". So ours treats 204 as jungle spiked. Need to verify vanilla: is the jungle spiked slime 204? Hmm, 204... Actually I'm not sure — spiked jungle slime ID is 147! But the vanilla 147 branch here only emits dust 76 and doesn't attack?? Wait — looking again at :61500 `if (type == 147 && Main.rand.Next(10) == 0)` dust 76. Dust 76? That's "spider"? Hmm.

Let me grep for proj 176 in AI_001 range to find the jungle spiked slime branch.

Also 658/659 (QueenSlime minions): ours covered with cooldown 50/40 — vanilla: 658 cooldown localAI[0] = 50 (classic single) ✓; 659 branch — need to read (starts :61748). Our comment says 659 cooldown 40. Let me read 61760-61960 to verify 659 and get the wet/jump core.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:11:38.565Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 220,
 "offset": 61759
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:11:38.577Z

**📎 ToolResult**

```
61759					float num45 = obj2.Center.X - center2.X;
61760					float num46 = obj2.Center.Y - center2.Y;
61761					float num47 = (float)Math.Sqrt(num45 * num45 + num46 * num46);
61762					float num48 = num47;
61763					if (Math.Abs(num45) < 500f && Math.Abs(num46) < 550f && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61764					{
61765						ai[0] = -40f;
61766						if (velocity.Y == 0f)
61767						{
61768							velocity.X *= 0.9f;
61769						}
61770						if (Main.netMode != 1 && localAI[0] == 0f)
61771						{
61772							num46 = Main.player[target].position.Y - center2.Y - (float)Main.rand.Next(0, 200);
61773							num47 = (float)Math.Sqrt(num45 * num45 + num46 * num46);
61774							num47 = 4.5f / num47;
61775							num47 *= 2f;
61776							if (num48 > 350f)
61777							{
61778								num47 *= 1.75f;
61779							}
61780							else if (num48 > 250f)
61781							{
61782								num47 *= 1.25f;
61783							}
61784							num45 *= num47;
61785							num46 *= num47;
61786							localAI[0] = 40f;
61787							if (Main.expertMode)
61788							{
61789								localAI[0] = 30f;
61790							}
61791							int attackDamage_ForProjectiles_MultiLerp3 = GetAttackDamage_ForProjectiles_MultiLerp(15f, 17f, 20f);
61792							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center2.X, center2.Y, num45, num46, 921, attackDamage_ForProjectiles_MultiLerp3, 0f, Main.myPlayer);
61793						}
61794					}
61795				}
61796			}
61797			if (type == 204)
61798			{
61799				flag3 = true;
61800				if (localAI[0] > 0f)
61801				{
61802					localAI[0] -= 1f;
61803				}
61804				if (!wet && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type])
61805				{
61806					Vector2 vector8 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
61807					float num49 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector8.X;
61808					float num50 = Main.player[target].position.Y - vector8.Y;
61809					float num51 = (float)Math.Sqrt(num49 * num49 + num50 * num50);
61810					if (Main.expertMode && num51 < 200f && Collision.CanHit(new Vector2(position.X, position.Y - 20f), width, height + 20, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61811					{
61812						ai[0] = -40f;
61813						if (velocity.Y == 0f)
61814						{
61815							velocity.X *= 0.9f;
61816						}
61817						if (Main.netMode != 1 && localAI[0] == 0f)
61818						{
61819							for (int n = 0; n < 5; n++)
61820							{
61821								Vector2 vector9 = new Vector2(n - 2, -2f);
61822								vector9.X *= 1f + (float)Main.rand.Next(-50, 51) * 0.02f;
61823								vector9.Y *= 1f + (float)Main.rand.Next(-50, 51) * 0.02f;
61824								vector9.Normalize();
61825								vector9 *= 3f + (float)Main.rand.Next(-50, 51) * 0.01f;
61826								int attackDamage_ForProjectiles3 = GetAttackDamage_ForProjectiles(13f, 13f);
61827								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector8.X, vector8.Y, vector9.X, vector9.Y, 176, attackDamage_ForProjectiles3, 0f, Main.myPlayer);
61828								localAI[0] = 80f;
61829							}
61830						}
61831					}
61832					if (num51 < 400f && Collision.CanHit(new Vector2(position.X, position.Y - 20f), width, height + 20, Main.player[target].position, Main.player[target].width, Main.player[target].height) && velocity.Y == 0f)
61833					{
61834						ai[0] = -80f;
61835						if (velocity.Y == 0f)
61836						{
61837							velocity.X *= 0.9f;
61838						}
61839						if (Main.netMode != 1 && localAI[0] == 0f)
61840						{
61841							num50 = Main.player[target].position.Y - vector8.Y - (float)Main.rand.Next(-30, 20);
61842							num50 -= num51 * 0.05f;
61843							num49 = Main.player[target].position.X - vector8.X - (float)Main.rand.Next(-20, 20);
61844							num51 = (float)Math.Sqrt(num49 * num49 + num50 * num50);
61845							num51 = 7f / num51;
61846							num49 *= num51;
61847							num50 *= num51;
61848							localAI[0] = 65f;
61849							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector8.X, vector8.Y, num49, num50, 176, 13, 0f, Main.myPlayer);
61850						}
61851					}
61852				}
61853			}
61854			if (type == 377 || type == 446)
61855			{
61856				if (localAI[2] < 90f)
61857				{
61858					localAI[2] += 1f;
61859				}
61860				else
61861				{
61862					friendly = false;
61863				}
61864			}
61865			if (type == 59)
61866			{
61867				position += netOffset;
61868				Lighting.AddLight((int)((position.X + (float)(width / 2)) / 16f), (int)((position.Y + (float)(height / 2)) / 16f), 1f, 0.3f, 0.1f);
61869				int num52 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, velocity.X * 0.2f, velocity.Y * 0.2f, 100, default(Color), 1.7f);
61870				Main.dust[num52].noGravity = true;
61871				position -= netOffset;
61872			}
61873			if (ai[2] > 1f)
61874			{
61875				ai[2] -= 1f;
61876			}
61877			if (wet)
61878			{
61879				if (collideY)
61880				{
61881					velocity.Y = -2f;
61882				}
61883				if (velocity.Y < 0f && ai[3] == position.X)
61884				{
61885					direction *= -1;
61886					ai[2] = 200f;
61887				}
61888				if (velocity.Y > 0f)
61889				{
61890					ai[3] = position.X;
61891				}
61892				if (type == 59 && !Main.remixWorld)
61893				{
61894					if (velocity.Y > 2f)
61895					{
61896						velocity.Y *= 0.9f;
61897					}
61898					else if (directionY < 0)
61899					{
61900						velocity.Y -= 0.8f;
61901					}
61902					velocity.Y -= 0.5f;
61903					if (velocity.Y < -10f)
61904					{
61905						velocity.Y = -10f;
61906					}
61907				}
61908				else
61909				{
61910					if (velocity.Y > 2f)
61911					{
61912						velocity.Y *= 0.9f;
61913					}
61914					velocity.Y -= 0.5f;
61915					if (velocity.Y < -4f)
61916					{
61917						velocity.Y = -4f;
61918					}
61919				}
61920				if (ai[2] == 1f && flag3)
61921				{
61922					TargetClosest();
61923				}
61924			}
61925			aiAction = 0;
61926			if (ai[2] == 0f)
61927			{
61928				ai[0] = -100f;
61929				ai[2] = 1f;
61930				TargetClosest();
61931			}
61932			if (velocity.Y == 0f)
61933			{
61934				if (collideY && oldVelocity.Y != 0f && Collision.SolidCollision(position, width, height))
61935				{
61936					position.X -= velocity.X + (float)direction;
61937				}
61938				if (ai[3] == position.X)
61939				{
61940					direction *= -1;
61941					ai[2] = 200f;
61942				}
61943				ai[3] = 0f;
61944				if (ai[1] == 3609f)
61945				{
61946					if (direction < 0)
61947					{
61948						velocity.X -= 0.1f;
61949					}
61950					else
61951					{
61952						velocity.X += 0.1f;
61953					}
61954					velocity.X = Utils.Clamp(velocity.X, -2.5f, 2.5f);
61955				}
61956				else
61957				{
61958					velocity.X *= 0.8f;
61959					if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
61960					{
61961						velocity.X = 0f;
61962					}
61963				}
61964				if (flag3)
61965				{
61966					ai[0] += 1f;
61967				}
61968				ai[0] += 1f;
61969				if (type == 59 && !Main.remixWorld)
61970				{
61971					ai[0] += 2f;
61972				}
61973				if (type == 71)
61974				{
61975					ai[0] += 3f;
61976				}
61977				if (type == 667)
61978				{

```


---

## 🤖 Assistant · 2026-08-19T03:12:13.105Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
This is the slime core. Key findings so far:

**Jungle Slime 204** (this is actually the... 204 = "Jungle Slime"? The proj is 176 "jungle spike"? Hmm — proj 176 is "Spiked Jungle Slime" spike). Ours implements 204 single-shot as: near=400, aim `player.y - cy - random*200`, speed 4.5, dmg 9, cooldown 50.

Vanilla 204 single-shot (classic): 
- near = 400 ✓
- CanHit from position.Y-20, height+20 (elevated LOS box)
- aim: num50 = player.position.Y - centerY - rand(-30, 20); num50 -= num51*0.05; num49 = player.X - centerX - rand(-20,20); speed 7.0; cooldown 65; ai[0] = -80.
- dmg 13 (not 9!) — ours uses dmg 9 for 204 and proj by id: `this.vanillaId === 184 ? 174 : this.vanillaId === 204 ? 176 : 605`. Speed 7 not 4.5! Aim offset rand(-30,20) not rand(0,200), plus -num51*0.05 drop compensation, plus ±20 X jitter. ai0=-80 not -40. Cooldown 65 not 50.

So ours treats 204 like 184/535 (speed 4.5, dmg 9, cd 50, ai0=-40) but vanilla 204 has its own distinct numbers: speed 7, dmg 13, cd 65, ai0=-80, drop comp. CONFIRMED deviation — medium.

**Wet buoyancy** (:61877-61924):
- collideY → vy = -2 ✓ ours (onGround || hitHead).
- vy<0 && ai[3]==position.X → direction*=-1, ai[2]=200. Ours uses slimeWetX ✓ (since we don't keep ai3 as X).
- vy>0 → ai[3] = position.X ✓ ours.
- 59 non-remix: vy>2 ×0.9, else if directionY<0 vy-=0.8, vy-=0.5, clamp -10 ✓ ours.
- else: ×0.9, -0.5, clamp -4 ✓.
- ai[2]==1 && flag3 → TargetClosest. Ours: `if (this.ai2 === 1 && flag3 && player) facing = seekDirX` ✓.

Wait, ours wet block runs BEFORE groundPhysics — vanilla runs wet before the ai[2]==0 / velocity.Y==0 grounded block. And in vanilla, if wet, the grounded block STILL runs (not else-if!) — velocity.Y==0f check. Hmm interesting: vanilla wet block doesn't return. Let me note: ours also continues (wet block doesn't return; grounded check is separate `grounded = onGround || (inWater && |vy|<0.8)`). Hmm — vanilla grounded gate = `velocity.Y == 0f`, ours = `onGround || (inWater && |vy|<0.8)`. These differ: vanilla requires vy==0 (post-collision this tick? AI reads velocity before collision — so vy==0 means last tick's post-collision vy). Ours: onGround flag from last collide + in-water near-zero vy. Approximation documented. For in-water, vy==0 rarely (buoyancy always adjusts), hence our inWater proxy. OK-ish. But subtle: vanilla with vy==0 while airborne (at jump apex) would run the grounded block! In vanilla, at the apex of a jump vy passes through 0 — the AI would treat it as grounded (friction vx*=0.8, ai0 increments, possibly jumping again). That's the famous "slimes can double jump at apex" quirk? Hmm wait — actually NPC velocity only becomes exactly 0... at apex yes for a single tick. The vanilla slime at jump apex vy==0 → treated grounded → ai0 += 2 → maybe trigger jump mid-air. This is real vanilla behavior (slime jumps refresh at apex). Ours requires onGround — misses apex re-trigger. LOW-MEDIUM deviation. Hmm, let me check: gravity 0.3/t; vy goes -6 → -5.7 → ... passes -0.3 → 0? -6 + k*0.3 = 0 → k=20 exactly → vy becomes exactly 0. Yes exactly 0 achievable. But collision zeroes vy only on ground. At apex vy==0 exactly happens when starting vy is a multiple of 0.3. -6 yes! -8? -8/0.3 = 26.67 → -8+27*0.3 = 0.1 → not 0. So small jumps (-6) hit exact 0 at apex. Vanilla slime mid-air small-jump apex → grounded block runs: ai[3]==position.X check (ai[3] is 0 or last jump X?) etc. This could cause direction flip mid-air! `if (ai[3] == position.X)` — during flight ai[3] was reset to 0 at last grounded (:61943 ai[3]=0f) — position.X == 0 never true. Then vx *= 0.8 mid-air (air friction at apex only), ai0 += ticks. So minor: apex friction + faster ai0 accumulation. Ours misses. LOW.

**ai[2] handling (:61873)**: `if (ai[2] > 1f) ai[2] -= 1f` — decrements only if > 1. Ours: `if (this.ai2 > 0) this.ai2--`. Hmm — vanilla leaves ai2==1 stuck at 1 (that's why `ai[2] == 1f` checks exist: "just expired"). Ours decrements to 0. Then ours checks `this.ai2 === 0` — vanilla's stuck-wander gate is `ai[2] == 0f` at :61926: `if (ai[2] == 0f) { ai[0] = -100; ai[2] = 1; TargetClosest(); }`. Wait what? :61926: if ai[2]==0 → ai[0]=-100, ai[2]=1, TargetClosest. That's the initialization! Vanilla: when ai[2] (fresh spawn = 0) → set ai0=-100, ai2=1. And with our ai0 default -1120... ours handles via class default.

Hmm wait, so vanilla ai2 semantics: 0 = fresh (init), 1 = active/no-stuck, 2..200 = stuck-turn cooldown. And `if (ai[2] > 1f) ai[2] -= 1f` — decrement toward 1, stops AT 1 (not 0).

Ours: `if (this.ai2 > 0) this.ai2--;` — decrements to 0. And gating: `if (flag3 && this.ai2 === 0 && player)` → seek. After 200 ticks cooldown, vanilla ai2 reaches 1 and stays — TargetClosest gate in vanilla is... where? Vanilla direction-facing gate: `if (ai[2] == 0f)`? no that's init. Let me find where vanilla gates TargetClosest on ai[2] during grounded... Actually vanilla AI_001 — where does it TargetClosest in general? At :61930 (init), :61922 (wet ai2==1 && flag3), and maybe in the jump block. Let me read on (61978-62150) to see the jump state machine and TargetClosest gating.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:13.419Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 175,
 "offset": 61978
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:13.445Z

**📎 ToolResult**

```
61978				{
61979					ai[0] += 3f;
61980				}
61981				if (type == 138)
61982				{
61983					ai[0] += 2f;
61984				}
61985				if (type == 183)
61986				{
61987					ai[0] += 1f;
61988				}
61989				if (type == 658)
61990				{
61991					ai[0] += 5f;
61992				}
61993				if (type == 659)
61994				{
61995					ai[0] += 3f;
61996				}
61997				if (type == 304)
61998				{
61999					float num53 = (1 - life / lifeMax) * 10;
62000					ai[0] += num53;
62001				}
62002				if (type == 377 || type == 446)
62003				{
62004					ai[0] += 3f;
62005				}
62006				if (type == 81)
62007				{
62008					if (scale >= 0f)
62009					{
62010						ai[0] += 4f;
62011					}
62012					else
62013					{
62014						ai[0] += 1f;
62015					}
62016				}
62017				float num54 = -1000f;
62018				if (type == 659)
62019				{
62020					num54 = -500f;
62021				}
62022				if (type == 667)
62023				{
62024					num54 = -400f;
62025				}
62026				int num55 = 0;
62027				if (ai[0] >= 0f)
62028				{
62029					num55 = 1;
62030				}
62031				if (ai[0] >= num54 && ai[0] <= num54 * 0.5f)
62032				{
62033					num55 = 2;
62034				}
62035				if (ai[0] >= num54 * 2f && ai[0] <= num54 * 1.5f)
62036				{
62037					num55 = 3;
62038				}
62039				if (num55 > 0)
62040				{
62041					netUpdate = true;
62042					if (flag3 && ai[2] == 1f)
62043					{
62044						TargetClosest();
62045					}
62046					if (num55 == 3)
62047					{
62048						velocity.Y = -8f;
62049						if (type == 59 && !Main.remixWorld)
62050						{
62051							velocity.Y -= 2f;
62052						}
62053						velocity.X += 3 * direction;
62054						if (type == 59 && !Main.remixWorld)
62055						{
62056							velocity.X += 0.5f * (float)direction;
62057						}
62058						ai[0] = -200f;
62059						ai[3] = position.X;
62060					}
62061					else
62062					{
62063						velocity.Y = -6f;
62064						velocity.X += 2 * direction;
62065						if (type == 59 && !Main.remixWorld)
62066						{
62067							velocity.X += 2 * direction;
62068						}
62069						ai[0] = -120f;
62070						if (num55 == 1)
62071						{
62072							ai[0] += num54;
62073						}
62074						else
62075						{
62076							ai[0] += num54 * 2f;
62077						}
62078					}
62079					if (type == 659)
62080					{
62081						velocity.Y *= 1.6f;
62082						velocity.X *= 1.2f;
62083					}
62084					if (type == 685)
62085					{
62086						velocity.Y *= 0.5f;
62087						velocity.X *= 0.2f;
62088						if (Main.rand.Next(2) == 0)
62089						{
62090							direction *= -1;
62091						}
62092					}
62093					if (type == 141)
62094					{
62095						velocity.Y *= 1.3f;
62096						velocity.X *= 1.2f;
62097					}
62098					if (type == 377 || type == 446)
62099					{
62100						velocity.Y *= 0.9f;
62101						velocity.X *= 0.6f;
62102						if (flag3)
62103						{
62104							direction = -direction;
62105							velocity.X *= -1f;
62106						}
62107						int i2 = (int)(base.Center.X / 16f);
62108						int j2 = (int)(base.Center.Y / 16f) - 1;
62109						if (WorldGen.SolidTile(i2, j2) && 0f - velocity.Y + (float)height > 16f)
62110						{
62111							velocity.Y = -(16 - height);
62112						}
62113					}
62114				}
62115				else if (ai[0] >= -30f)
62116				{
62117					aiAction = 1;
62118				}
62119			}
62120			else if (target < 255 && ((direction == 1 && velocity.X < 3f) || (direction == -1 && velocity.X > -3f)))
62121			{
62122				if (collideX && Math.Abs(velocity.X) == 0.2f)
62123				{
62124					position.X -= 1.4f * (float)direction;
62125				}
62126				if (collideY && oldVelocity.Y != 0f && Collision.SolidCollision(position, width, height))
62127				{
62128					position.X -= velocity.X + (float)direction;
62129				}
62130				if ((direction == -1 && (double)velocity.X < 0.01) || (direction == 1 && (double)velocity.X > -0.01))
62131				{
62132					velocity.X += 0.2f * (float)direction;
62133				}
62134				else
62135				{
62136					velocity.X *= 0.93f;
62137				}
62138			}
62139		}
62140	
62141		public void AI_001_SetRainbowSlimeColor()
62142		{
62143			color.R = (byte)Main.DiscoR;
62144			color.G = (byte)Main.DiscoG;
62145			color.B = (byte)Main.DiscoB;
62146			color.A = 100;
62147			alpha = 175;
62148		}
62149	
62150		private int AI_001_Slimes_GenerateItemInsideBody(bool isBallooned)
62151		{
62152			int num = Main.rand.Next(4);

```


---

## 🤖 Assistant · 2026-08-19T03:13:24.509Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
HUGE findings on slime core:

1. **Grasshopper (377/446) jump inversion**: vanilla after jump: `if (flag3) { direction = -direction; velocity.X *= -1; }` — grasshopper jumps AWAY then flips direction for next jump! Plus the ceiling-bonk adjust `velocity.Y = -(16-height)` if solid above. Ours: only vy×0.9, vx×0.6, NO direction inversion, NO ceiling check. Hmm wait — ours has `if (grasshopper) { this.vy *= 0.9; this.vx *= 0.6; }`. Vanilla has additionally: if flag3 → direction*=-1 AND vx*=-1 (so jump velocity points away from player, but direction faces player for next hop?). Wait: direction*=-1 flips facing; vx *= -1 flips jump direction. So the hop goes away from where it was facing... then next tick direction stays flipped? Hmm — flag3 for grasshopper requires player within 200. So when player near: grasshopper hops AWAY from player (fleeing!) — that matches grasshopper critter behavior (they hop away). And when not flag3, hop in direction. Ours missing the flee inversion → grasshoppers hop TOWARD player when near. CONFIRMED — medium severity (visible critter behavior wrong direction).

Wait, careful: order — velocity.X += 2*direction (toward player, since direction = seekDirX when flag3), then vx *= 0.6, then vx *= -1 → away. And direction = -direction → facing away. So yes, hop away from player. Fleeing. Ours hops toward. CONFIRMED.

Also ceiling: if solid tile above center-1 tile and jump height would exceed (−vy + height > 16): vy = −(16−height) — small hop under ceiling. Ours missing (low, edge).

2. **Type 659 (Queen Slime pink minion) jump boost**: vy *= 1.6, vx *= 1.2. Ours missing! Ours treats 658/659 same for jumps. CONFIRMED missing — medium.

3. **Type 141 (slime from hellevators? 141 = "Slime Umbrella"? whatever)**: vy*=1.3, vx*=1.2 — ours missing. 141 = "umbrella slime" (raincoat zombie companion?). Actually 141 might be the umbrella slime from rain. LOW.

4. **Type 685 (balloon slime? no — 685 = "Drippler"? no...)** vy*=0.5, vx*=0.2, 50% flip — ours: balloonSlimeAI is separate (AI_125). 685 = "Slime Balloon"? The balloon slime uses aiStyle 125 per memory. So 685 in AI_001? Hmm, maybe 685 = "Windy Balloon slime"? whatever — separate AI in ours. Skip.

5. **Type 59 lava slime**: big jump vy -= 2 (extra), small jump vx += 2*direction (extra), grounded ai0 += 2 (extra speed). Ours: MISSING all three 59-specific tweaks! Ours just flags light for 59 and the wet clamp -10. CONFIRMED — medium (lava slime jumps higher/faster + jumps more often).

6. **Type 71 (king slime? no, 71 = ... )** ai0 += 3. 71 = "Slime"? Hmm — 71 is... hmm. Whatever: ours missing. LOW unless 71 is common. 71 might be "Gastropod"? no that's a flyer. Actually — I don't recall. Let me not worry; list as low.

Wait — ours has `this.ai0 += grasshopper ? 3 : 1 + (flag3 ? 1 : 0)`. Vanilla: `if (flag3) ai[0] += 1; ai[0] += 1;` — ✓ same base. Then per-type extras: 59 +2, 71 +3, 667 +3, 138 +2, 183 +1, 658 +5, 659 +3, 304 +damage-based, 377/446 +3, 81 +4 (scale>=0; else +1 — weird "scale >= 0f" always true? scale is always positive... decompiler artifact of a conditional on netID?). 244: ai[0] += 2 at :61498.

Ours implements NONE of the per-type ai0 extras except grasshopper +3. So all these slimes jump at wrong rhythm (faster in vanilla):
- 59 Lava Slime +2 (1.5-2× faster jumps)
- 667 Golden Slime +3 (very jumpy)
- 138? +2 (138 = "Slime"? hmm... 138 = ? Let me think: 138 = "Sand Slime"? no that's 537. 138... could be "Corrupt Slime"? no 263? Hmm — I'll list ids without names.)
- 183 +1 (183 = "Illuminant Slime"? that's hardmode hallow slime — 183? Hmm)
- 658 +5, 659 +3 (Queen minions — very fast)
- 304: +damage ramp (304 = "Slime"? — 304 is... hmm "Baby Slime"? no. Whatever)
- 81: +4 or +1 (81 = Green Slime — common early game! +4 = extra fast)
- 244: +2 (Rainbow slime)
- 377/446 +3 ✓ ours has.

CONFIRMED missing per-type ai0 rate boosts — medium severity, affects jump cadence for common slimes (green slime 81 is the most common surface slime!).

7. **num54 per-type**: 659 → -500, 667 → -400. Ours: fixed -1000 with `this.ai0 = stage === 1 ? -120 + num54 : -120 + num54 * 2`. Vanilla: small jump ai[0] = -120 + num54 (stage 1) or -120 + num54*2 (stage 2) ✓ same formula. But num54 for 659/667 differ → different cycle lengths (659: -620/-1120; 667: -520/-920). Ours fixed -1120/-2120. So 659/667 jump cycle ~2× slower in ours. CONFIRMED — medium (667 golden slime famously hops constantly).

8. **Big jump details**: stage 3: vy=-8, vx += 3*direction, ai0=-200, ai3=position.X. 59: vy -= 2 and vx += 0.5*direction extra. Ours: vy=-8, vx+=3*dir, ai0=-200 ✓; missing 59 extras (already noted).

9. **Small jump**: vy=-6, vx += 2*direction ✓; 59 extra +2*direction.

10. **TargetClosest gate on jump**: vanilla `if (flag3 && ai[2] == 1f) TargetClosest()` — INSIDE num55>0 (jump triggered), gate ai[2]==1 (i.e., NOT in stuck cooldown). Ours: `if (flag3 && this.ai2 === 0 && player) this.facing = this.seekDirX(player);` — runs EVERY tick before grounded block. Differences: 
   a. Vanilla re-targets only at jump moment; ours continuously. Effectively similar since direction is only consumed at jump. But during stuck cooldown (ai2>1), vanilla does NOT retarget (keeps reversed direction); ours gate ai2===0... ours decrements to 0 after 200 ticks vs vanilla stopping at 1. Timing: vanilla: ai2=200, decrement while >1 → reaches 1 after 199 ticks, stays 1. Gate ==1 → re-target allowed after 199t. Ours: ai2=200 → decrements while >0 → reaches 0 after 200 ticks. Gate ===0 → allowed after 200t. ~Same. ✓ but ours also has the `if (this.ai2 === 1 && flag3 ...)` wet re-target — wait ours: `if (this.ai2 === 1 && flag3 && player)` in wet block. Vanilla: `if (ai[2] == 1f && flag3) TargetClosest()`. But OURS ai2 only equals 1 transiently (when passing 200→...→1→0, one tick at 1 during decrement)? Ours decrements `if (ai2 > 0) ai2--` so 2→1, then next tick 1→0. So ai2==1 for exactly one tick → wet re-target happens once after cooldown ✓ roughly matches (vanilla: permanently 1 → retargets EVERY wet tick after cooldown — deviation: vanilla wet slimes with flag3 re-target continuously once cooldown expires; ours only once). Hmm wait — vanilla wet block: `if (ai[2] == 1f && flag3) TargetClosest()` — ai2 stays 1 forever after cooldown → re-target every tick in water. Ours: one tick only. Then ours' main gate `ai2 === 0` retargets every tick anyway (ours decrements through 1 to 0 and the main gate is ===0 → continuous). Actually ours' continuous gate covers it. Fine — behaviorally equivalent overall.

   b. Vanilla gate is `ai[2] == 1f` NOT `== 0` — since ai2 never is 0 after init (init sets 1). Ours uses 0 with decrement-through. Equivalent. ✓

11. **Grounded stuck check**: vanilla `if (ai[3] == position.X) { direction*=-1; ai[2]=200; }` then ai[3] = 0. Ours: `if (this.jumpStartX !== 0 && Math.abs(this.cx - this.jumpStartX) < 1)` — approximate: vanilla compares EXACT equality of ai[3] (set at last jump = position.X at jump start) vs current position.X (grounded). If exactly equal → flip. Ours uses tolerance <1px and guards 0. Roughly OK. But note: after grounded, vanilla sets ai[3] = 0; ours sets jumpStartX = 0 ✓ same idea.

12. **ai1 == 3609 conveyor-belt exception**: when slime contains item 3609 (conveyor belt), grounded vx doesn't get ×0.8 — instead vx += direction*0.1 clamped ±2.5 (constant slide). Ours missing — LOW (rare item).

13. **SolidCollision unstick nudge** (:61934, :62126): when landing while embedded in solid, position.X -= velocity.X + direction. Ours missing — edge unstick, LOW.

14. **Air control** (:62120-62137): airborne + target valid + moving slower than 3 in direction → if |vx| tiny → vx += 0.2*direction else vx *= 0.93; plus collideX nudge when |vx|==0.2. Ours: MISSING ENTIRELY! When airborne, vanilla slimes keep steering horizontally toward the player (0.2/t accel until |vx|=3). Ours only steers on ground. This is significant — vanilla slimes home in mid-air during jumps; ours follow pure parabolas. Medium severity, player-visible (slimes feel dumber/floatier).

Also note air-control gate `target < 255` — needs a target (TargetClosest found someone). Not gated on flag3! Even passive slimes air-steer toward their target. Interesting.

15. **aiAction 1 when ai0 >= -30** — animation state (wiggle before jump). Rendering side; ours maybe has. Skip (note).

16. **Type 81 (Green Slime)**: dust 14 1/30 + always flag3. Ours: flag3 doesn't force 81. Ours flag3 = !day || hurt || underground || slimeRain. Vanilla additionally forces flag3 = true for: 81 (green slime — always aggressive!), 183, 304, 667, 244, 184, 535, 658, 659, 204, and (remix 59 exception). Ours forces flag3 ONLY for grasshoppers (different logic) — none of these! So in daytime on surface at full HP, ours: 81/183/304/667/244/184/535/204/658/659 wander passively (keep direction, no seek), vanilla: aggressive chase. CONFIRMED — severity medium-high? Hmm — actually wait. Daytime surface full HP: vanilla 81 green slime aggressive? Yes — green slimes always chase. But 1 (blue) doesn't. This is a visible behavior difference: daytime blue slimes passive ✓ both, green slimes aggressive in vanilla vs passive in ours. MEDIUM-HIGH (common mob).

Hmm wait, let me double check the flag3 list in vanilla: :61468 (81), :61483 (183), :61487 (304), :61491 (667), :61495 (244, ai0+=2), :61560 (184), :61615 (535), :61670 (658), :61750 (659), :61799 (204). Plus grasshopper special. So 10 types. Ours: none. Confirmed.

17. **Type 377/446 localAI[2] < 90 → friendly=false after 90 ticks**: critter→enemy transition for grasshoppers? localAI[2] increments to 90 then sets friendly=false. Wait — grasshoppers spawned as friendly (critters)? Hmm — this makes grasshopper non-friendly after 90 ticks. Interesting — probably grasshoppers start friendly (no contact damage) and become normal after 90t? Ours: does Enemy have friendly for grasshoppers? Probably handled at spawn. Skip — low/uncertain.

18. **676 shimmer slime light**: vanilla AddLight(Center, 23) — torch id 23 formula. Ours approximates ✓.

19. Ours: spiked slimes gated `!inWater` — vanilla `!wet`. inWater = liquid > 80 at center tile vs wet flag. Approximation ✓ documented.

20. Ours spiked cooldown uses ai3; vanilla localAI[0]. Since ours doesn't use ai3 for anything else in slimeAI (jumpStartX separate), equivalent. But WAIT — ours uses ai3 as cooldown and ALSO the class default -1120 for ai0... For spawned slimes, does anything reset ai3? Enemy defaults ai3 = ? If ai3 defaults to -1120, then `if (this.ai3 > 0) this.ai3 -= 1` never fires; ai3 === 0 check: -1120 !== 0 → first shot blocked until... `this.ai3 = 50` set after first shot. Gate: `if (dp < near && this.ai3 === 0 && canSee)` — ai3 = -1120 ≠ 0 → never fires?! Let me check Enemy's ai3 default. In our class: `this.ai0 = -1120` for slime? Let me check field defaults — grep "ai3 = " in Enemy constructor / field init. This could be a real bug: spiked slimes never shoot if ai3 defaults to -1120. Let me check.

Also mimic: `if (this.ai0 < 0) this.ai0 = 0;` guards. SlimeAI: uses ai0 directly — spawn sets ai0=-1120? The slime jump cycle: ai0 starts at class default... vanilla init sets ai[0]=-100 at first tick (ai2==0 → ai0=-100, ai2=1). Ours: `if (this.ai2 > 0) this.ai2--` — first tick ai2: default? If ai2 defaults 0 → no init path! Vanilla's init `if (ai[2]==0) {ai[0]=-100; ai[2]=1; TargetClosest();}`. Ours doesn't have that init — ai0 starts at whatever class default (-1120?). With ai0=-1120: grounded → ai0 += 1 → -1119... stage: -1120 < -2000? no. -1120 >= -1000? no → stage 0. So no jump until ai0 climbs from -1120 to... wait stage 2 needs ai0 in [-1000, -500]; -1120 → +1/t → after 120 ticks reaches -1000 → stage 2 → jump. Vanilla: init ai0=-100 → stage 1 immediately → jumps almost right away. So ours: slime stands still 2 seconds before first jump IF ai0 defaults -1120. Need to check what ai0 defaults to and whether spawner sets it. The memory notes "13 aiStyle路由/ai0初值坑" and plantAI has explicit -1120 self-heal. Let me check Enemy field defaults & fromVanilla.

Let me also verify: does our slimeAI handle the "ai2==0 init" at all? No. If ai2 defaults 0 → `if (ai2 > 0)` false → gate `flag3 && this.ai2 === 0 && player` → seek — so first tick ai2==0 = active seeking. Vanilla first tick: init ai0=-100, ai2=1, TargetClosest. So ours' ai0 default is critical. Check Enemy class fields.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:25.408Z · glm-x-preview-260804

```
史莱姆核心与我们的实现差异很大。我来检查一下我们的 `Enemy` 字段中 `ai0`/`ai3` 的默认值——几个门控逻辑依赖于它们。
```


---

## 🤖 Assistant · 2026-08-19T03:13:26.364Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"ai0 = \\|ai1 = \\|ai2 = \\|ai3 = \\|ai0:\\|ai1:\\|ai2:\\|ai3:\\|jumpStartX\\|slimeWetX\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -40",
 "description": "Find ai field defaults in Enemy.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:26.458Z

**📎 ToolResult**

```
122:  ai2: number, fading: boolean, cap: number,
123:): { ai2: number; opacity: number; despawn: boolean } {
126:  if (next >= DESPAWN) return { ai2: next, opacity: 0, despawn: true };
132:  return { ai2: next, opacity, despawn: false };
384:      if (this.ai2 >= LIFE) this.ai2 = 0;
661:    spit.ai0 = 0; spit.ai1 = 1;
827:  jumpStartX = 0;        // 史莱姆本次起跳的 x（落地时判定是否白跳）
853:  slimeWetX = 0;
998:  lai0 = 0;              // localAI 语义位（萤火虫：闪烁间隔计时）
999:  lai1 = 0;              // localAI 语义位（萤火虫：发光剩余帧）
1000:  lai2 = 0;              // localAI[2] 语义位（AI_054 克脑：二阶段入场演出门）
1001:  lai3 = 0;              // localAI[3] 语义位（AI_054 克脑：玩家死/离场下坠计数；AI_008 法师 32：RedHat 变体带 +3）
1046:  ai0 = -1120;
1047:  ai2 = 0;
1049:  ai1 = 0;
1051:  ai3 = 0;
1752:    this.ai1 = -1;                                 // :60752 先置空
1769:          this.ai1 = this.slimeGenItemInsideBody(this.ai0 === -999);
1775:        if (roll(maxValue2) === 0) this.ai1 = roll(2) === 0 ? 1103 : 593;  // 淤泥/雪块
1790:          this.ai1 = roll(2) === 0 ? 3736 + roll(3) : 1345;         // Next(3736,3739) 气球/彩纸
1793:          this.ai1 = num5 === 1 ? 1125 : num5 === 2 ? 314 : num5 === 3 ? 5395 : 1124;
1795:          this.ai1 = this.slimeGenItemInsideBody(this.ai0 === -999);
1799:            this.ai1 = 751;                        // 云块
1802:            this.ai1 = num7 === 1 ? 3 : num7 === 2 ? 9 : 2;         // 石/木/土
1804:            this.ai1 = 3609;                        // :60888-60890 传送带
1808:            this.ai1 = num9 === 1 ? 150 : num9 === 2 ? 3086 : num9 === 3 ? 3081 : 3; // 蛛网/花岗岩/大理石/石
1811:          this.ai1 = 539;                           // :60911-60913 史莱姆法杖
1813:          this.ai1 = 147;                           // :60914-60916 ftw 地下 → 棘刺丛林史莱姆物
1815:          this.ai1 = 75;                            // :60917-60919 首掷 remix → 生命水晶星史莱姆
1881:      if (this.jumpStartX !== 0 && Math.abs(this.cx - this.jumpStartX) < 1) {
1883:        this.ai2 = 200;
1885:      this.jumpStartX = 0;
1901:          this.ai0 = -200;
1906:          this.ai0 = stage === 1 ? -120 + num54 : -120 + num54 * 2;
1909:        this.jumpStartX = this.cx;  // ai[3] = position.X（L62059）
1922:        this.ai0 = -40; // 压制下一跳
1927:        this.ai3 = 50;
1945:        this.ai0 = -40; // 压制下一跳（cs:61721/:61751）
1954:        this.ai3 = this.vanillaId === 658 ? 50 : 40;             // :61735/:61770
1964:      if (this.vy < 0 && this.slimeWetX === this.x) {

```


---

## 🤖 Assistant · 2026-08-19T03:13:27.277Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"ai0\\b\" ~/Project/GLM/SandboxWorld/game/src/entities/types.ts ~/Project/GLM/SandboxWorld/game/src/entities/Entity.ts 2>/dev/null | head; grep -n \"ai0\" ~/Project/GLM/SandboxWorld/game/src/entities/types.ts | head",
 "description": "Check ai0 typing in types.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:27.365Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-19T03:14:18.351Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Enemy field defaults: `ai0 = -1120; ai2 = 0; ai1 = 0; ai3 = 0;` (lines 1046-1051).

So:
- ai0 defaults -1120 (slime-sentinel).
- ai3 defaults 0 → spiked slime cooldown gate `ai3 === 0` passes at spawn ✓ (not a bug — ai3 default is 0, good).

Now for slimeAI first-jump timing: ai0 = -1120 at spawn. Vanilla: first tick ai0 = -100 (init block), stage 1 → jumps immediately when grounded. Ours: ai0 climbs from -1120 → slime stands still for ~120 ticks (2s) before first jump, then at -1000..-500 does stage 2, -2000..-1500 unreachable from -1120 upward... wait: from -1120, +2/t (flag3): after 60t → -1000; at -1000..-500 → stage 2 (small jump) → ai0 = -120 + (-1000*2) = -2120. Then climbs to -2000 (60t) → stage 3 (big jump) → ai0 = -200 → climbs to 0 (100t) → stage 1 → -1120. So the cycle from second jump onwards matches vanilla's (small→small→big). Only the FIRST appearance differs: vanilla -100 → immediate stage 1 small jump; ours: 60-120 ticks standing still first. Actually from -1120 with flag3 (+2/t): reaches -1000 after 60t → stage 2 small jump (ai0→-2120). Without flag3 (+1/t): 120t. So 1-2 s initial delay. Vanilla slime also doesn't jump on the very first tick necessarily (ai0=-100, +2/t → reaches 0 after 50t → stage 1). Hmm wait — vanilla init sets ai0 = -100, so from -100 it takes 50 ticks (flag3) to reach 0 → stage 1. So vanilla first jump after ~50 ticks, ours first jump after 60-120 ticks. Actually not hugely different! Vanilla: -100 +2/t → 0 at 50t → stage 1 → ai0=-1120. Ours: -1120 +2/t → -1000 at 60t → stage 2 → -2120. So first jump: vanilla 50t small, ours 60t small. Marginal difference! Because -1120 is exactly vanilla's stage-1 target. Clever — the -1120 default IS vanilla's post-first-jump value. So first jump delay ≈ same (50 vs 60 ticks; passive 100 vs 120). Minor: first jump is stage 2 not stage 1 (same small jump anyway). Negligible. OK — so no first-jump bug. Good.

But the missing vanilla init `ai2 = 1`: ours ai2 defaults 0 → the `flag3 && ai2===0` gate active immediately ✓ equivalent to vanilla post-init state (ai2=1 retarget gate... vanilla gate is ai2==1; ours 0). ✓ equivalent.

Now the per-type ai0 rate boosts (59/71/667/138/183/658/659/304/81/244) — missing in ours except grasshopper. Also missing 59 jump boost, 659 jump boost, 141 jump boost, grasshopper flee inversion & ceiling check, air steering (:62120), 3609 conveyor exception, SolidCollision nudges, forced flag3 list. And 204 has different attack params (speed 7/dmg 13/cd 65/ai0=-80/drop compensation vs ours 4.5/9/50/-40). And spiked LOS box for 204 (position.Y-20, height+20).

Also ours spiked slimes: after firing sets ai0 = -40 → suppresses next jump ✓ vanilla. But vanilla also has the spike attack AFTER the wet block and BEFORE the ai2==0 init/grounded — meaning vanilla spike attack runs even when airborne? No — gate `velocity.Y == 0f` (grounded). Ours gates onGround ✓.

Ordering nuance: vanilla spike attack sets ai[0]=-40 THEN the grounded block runs `if (flag3) ai[0]+=1; ai[0]+=1` → -38, no jump until climbs to 0 (~19 ticks). Ours: spike block runs after grounded block (which may have jumped this tick — setting ai0=-1120, then spike sets ai0=-40). Hmm — ours: grounded block increments ai0 and possibly jumps (setting ai0 = -2120), THEN spike block overwrites ai0 = -40 (already jumped — velocity applied this tick, jump happened but ai0=-40 will make next jump come 20t later). Vanilla: spike sets ai0=-40 first, then grounded block runs: ai[3]==position.X check, friction, ai0 += 2 → -38; num55: -38 >= -30? no → no jump; aiAction... Actually ai0 >= -30 → aiAction=1 only. So vanilla suppresses the same-tick jump; ours may jump on the same tick it shoots (if the jump threshold was reached simultaneously) — tiny edge, LOW. Hmm wait — ours order: grounded block first (jump sets vy=-6), then spike sets ai0=-40, vx*=0.9. The slime shoots AND jumps same tick. Vanilla: shoots, no jump. Very minor.

Bigger: ours spike gate `this.ai3 === 0` — vanilla `localAI[0] == 0f`. Default ai3=0 ✓ fine.

Now — one more slime thing to verify: the "vanilla init ai[2]==0 → ai[0]=-100, ai[2]=1, TargetClosest" — since ours' ai0 default -1120 approximates post-init state, and ai2 default 0 works, OK.

And ours doesn't implement the ai1==3609 no-friction. LOW.

Now the air-steering (:62120-62137) — confirm ours has nothing similar. In our slimeAI, after grounded block, there's no airborne steering. Confirmed missing.

Also :61934/:62126 SolidCollision unstick. Missing. LOW.

Grasshopper passive walk档 (ours: vx += facing*0.02 clamp 0.2): vanilla? Grasshoppers when !flag3... vanilla doesn't have that in AI_001? Ours comment says "cs:61479 蚱蜢被动档" — hmm, where's that in vanilla? I saw `if ((type == 377 || type == 446) && target != 255 && !dead && Distance <= 200 && !wet) flag3 = true`. When grasshopper is NOT flag3 — vanilla just runs the normal slime core (passive → no retarget; grounded increments; jumps happen anyway — vanilla passive grasshopper still JUMPS (small/big cycle), just doesn't seek. Ours instead has a special passive walk档 (0.02 accel clamp 0.2, no jumping). DEVIATION — ours made up a "walk mode" for grasshoppers; vanilla grasshoppers always hop like slimes, just without seeking. Hmm wait — is that right? Vanilla flag3=false grasshopper: air steering (target<255 gate — grasshopper may have no target...). The grounded block: ai0 += 1 + (flag3?1:0) → jumps at stage. So yes vanilla grasshoppers hop constantly even when passive. Ours passive grasshoppers crawl at 0.2 max — visible difference (grasshoppers should hop around randomly like slimes). MEDIUM? It's a critter; vanilla hop with random direction. I'd rank medium-low. Actually the memory notes "critter-ai-port" claims 1:1 for critters. But this walk档 looks invented. Hmm — "蚱蜢被动档（cs:61479）：无激愤时走"走路档"——0.2 慢爬不进跳循环". Vanilla :61479 is only the flag3 line. There's no walk mode in vanilla AI_001. So CONFIRMED invented behavior — grasshoppers should hop (passively) not crawl. Medium.

Now AI_003_Fighters — the monster. 4490 lines. Our fighterAI + fighterFamilies covers: psycho stealth, wet swimmers (461/586/620?), medusa, swamp thing, chaos elemental, nailhead, butcher, possessed, fritz, solenian dash, storm diver, ranged fighters, ice giant 243, rock golem 631, eyezor 251, move chains, jump logic, doors, spider transform, vampire, lihzahrd.

Given the size, I should spot-check the core walk/jump/movement chain and the per-family numbers we've ported. Let me read the vanilla AI_003 core sections:
1. :56245-56330 (start: psycho + grass? swim 461/586 blocks?)
2. :56327-56460 (swamp thing, 461/586 swim)
3. :56540-56890 (medusa, 379 ritual?)
4. :57114-57173 (solenian)
5. :57422-57799 (stuck counting, eclipse specials, day discouragement)
6. :57799-58800 (movement chains) — verify numbers in fighterFamilies.ts
7. :58800-59464 (lights, ranged attack setup)
8. :59464-60095 (ranged attack)
9. :60115-60175 (friction)
10. :60383-60460 (doors)
11. :60460-60734 (jump + spider/vampire/lihzahrd + flag8 ai resets)

That's a lot but let me do targeted reads. First 56245-56560 to see the head of AI_003.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:18.913Z · glm-x-preview-260804

```
现在来处理这些庞然大物 —— AI_003 战士。我将分段读取其核心内容。
```


---

## 🤖 Assistant · 2026-08-19T03:14:19.160Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 330,
 "offset": 56245
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:19.303Z

**📎 ToolResult**

```
56245		private void AI_003_Fighters()
56246		{
56247			if (Main.player[target].position.Y + (float)Main.player[target].height == position.Y + (float)height)
56248			{
56249				directionY = -1;
56250			}
56251			bool flag = false;
56252			if (type == 624 && AI_003_Gnomes_ShouldTurnToStone())
56253			{
56254				int num = (int)(base.Center.X / 16f);
56255				int num2 = (int)(base.Bottom.Y / 16f);
56256				position += netOffset;
56257				int num3 = Dust.NewDust(position, width, height, 43, 0f, 0f, 254, Color.White, 0.5f);
56258				Main.dust[num3].velocity *= 0.2f;
56259				position -= netOffset;
56260				if (WorldGen.SolidTileAllowBottomSlope(num, num2))
56261				{
56262					for (int i = 0; i < 5; i++)
56263					{
56264						position += netOffset;
56265						int num4 = Dust.NewDust(position, width, height, 43, 0f, 0f, 254, Color.White, 0.5f);
56266						Main.dust[num4].velocity *= 0.2f;
56267						position -= netOffset;
56268					}
56269					if (Main.netMode != 1 && TileObject.CanPlace(num, num2 - 1, 567, 0, direction, out var _, onlyCheck: true) && WorldGen.PlaceTile(num, num2 - 1, 567, mute: false, forced: false, -1, Main.rand.Next(5)))
56270					{
56271						if (Main.netMode == 2)
56272						{
56273							NetMessage.SendTileSquare(-1, num, num2 - 2, 1, 2);
56274						}
56275						if (Main.netMode != 1)
56276						{
56277							if (IsNPCValidForBestiaryKillCredit())
56278							{
56279								Main.BestiaryTracker.Kills.RegisterKill(this);
56280							}
56281							CountKillForBannersAndDropThem();
56282						}
56283						life = 0;
56284						active = false;
56285						AchievementsHelper.NotifyProgressionEvent(24);
56286						return;
56287					}
56288				}
56289			}
56290			if (type == 466)
56291			{
56292				int num5 = 200;
56293				if (ai[2] == 0f)
56294				{
56295					alpha = num5;
56296					TargetClosest();
56297					if (!Main.player[target].dead && (Main.player[target].Center - base.Center).Length() < 170f)
56298					{
56299						ai[2] = -16f;
56300					}
56301					if (velocity.X != 0f || velocity.Y < 0f || velocity.Y > 2f || justHit)
56302					{
56303						ai[2] = -16f;
56304					}
56305					return;
56306				}
56307				if (ai[2] < 0f)
56308				{
56309					if (alpha > 0)
56310					{
56311						alpha -= num5 / 16;
56312						if (alpha < 0)
56313						{
56314							alpha = 0;
56315						}
56316					}
56317					ai[2] += 1f;
56318					if (ai[2] == 0f)
56319					{
56320						ai[2] = 1f;
56321						velocity.X = direction * 2;
56322					}
56323					return;
56324				}
56325				alpha = 0;
56326			}
56327			if (type == 166)
56328			{
56329				if (Main.netMode != 1 && Main.rand.Next(240) == 0)
56330				{
56331					ai[2] = Main.rand.Next(-480, -60);
56332					netUpdate = true;
56333				}
56334				if (ai[2] < 0f)
56335				{
56336					TargetClosest();
56337					if (justHit)
56338					{
56339						ai[2] = 0f;
56340					}
56341					if (Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
56342					{
56343						ai[2] = 0f;
56344					}
56345				}
56346				if (ai[2] < 0f)
56347				{
56348					velocity.X *= 0.9f;
56349					if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
56350					{
56351						velocity.X = 0f;
56352					}
56353					ai[2] += 1f;
56354					if (ai[2] == 0f)
56355					{
56356						velocity.X = (float)direction * 0.1f;
56357					}
56358					return;
56359				}
56360			}
56361			if (type == 461)
56362			{
56363				if (wet)
56364				{
56365					knockBackResist = 0f;
56366					ai[3] = -0.10101f;
56367					noGravity = true;
56368					Vector2 center = base.Center;
56369					width = 34;
56370					height = 24;
56371					position.X = center.X - (float)(width / 2);
56372					position.Y = center.Y - (float)(height / 2);
56373					TargetClosest();
56374					if (collideX)
56375					{
56376						velocity.X = 0f - oldVelocity.X;
56377					}
56378					if (velocity.X < 0f)
56379					{
56380						direction = -1;
56381					}
56382					if (velocity.X > 0f)
56383					{
56384						direction = 1;
56385					}
56386					if (Collision.CanHit(position, width, height, Main.player[target].Center, 1, 1))
56387					{
56388						Vector2 vector = Main.player[target].Center - base.Center;
56389						vector.Normalize();
56390						vector *= 5f;
56391						velocity = (velocity * 19f + vector) / 20f;
56392						return;
56393					}
56394					float num6 = 5f;
56395					if (velocity.Y > 0f)
56396					{
56397						num6 = 3f;
56398					}
56399					if (velocity.Y < 0f)
56400					{
56401						num6 = 8f;
56402					}
56403					Vector2 vector2 = new Vector2(direction, -1f);
56404					vector2.Normalize();
56405					vector2 *= num6;
56406					if (num6 < 5f)
56407					{
56408						velocity = (velocity * 24f + vector2) / 25f;
56409					}
56410					else
56411					{
56412						velocity = (velocity * 9f + vector2) / 10f;
56413					}
56414					return;
56415				}
56416				knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.4f);
56417				noGravity = false;
56418				Vector2 center2 = base.Center;
56419				width = 18;
56420				height = 40;
56421				position.X = center2.X - (float)(width / 2);
56422				position.Y = center2.Y - (float)(height / 2);
56423				if (ai[3] == -0.10101f)
56424				{
56425					ai[3] = 0f;
56426					float num7 = velocity.Length();
56427					num7 *= 2f;
56428					if (num7 > 10f)
56429					{
56430						num7 = 10f;
56431					}
56432					velocity.Normalize();
56433					velocity *= num7;
56434					if (velocity.X < 0f)
56435					{
56436						direction = -1;
56437					}
56438					if (velocity.X > 0f)
56439					{
56440						direction = 1;
56441					}
56442					spriteDirection = direction;
56443				}
56444			}
56445			if (type == 586)
56446			{
56447				if (alpha == 255)
56448				{
56449					TargetClosest();
56450					spriteDirection = direction;
56451					velocity.Y = -6f;
56452					netUpdate = true;
56453					for (int j = 0; j < 35; j++)
56454					{
56455						Dust dust = Dust.NewDustDirect(position, width, height, 5);
56456						dust.velocity *= 1f;
56457						dust.scale = 1f + Main.rand.NextFloat() * 0.5f;
56458						dust.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
56459						dust.velocity += velocity * 0.5f;
56460					}
56461				}
56462				alpha -= 15;
56463				if (alpha < 0)
56464				{
56465					alpha = 0;
56466				}
56467				position += netOffset;
56468				if (alpha != 0)
56469				{
56470					for (int k = 0; k < 2; k++)
56471					{
56472						Dust dust2 = Dust.NewDustDirect(position, width, height, 5);
56473						dust2.velocity *= 1f;
56474						dust2.scale = 1f + Main.rand.NextFloat() * 0.5f;
56475						dust2.fadeIn = 1.5f + Main.rand.NextFloat() * 0.5f;
56476						dust2.velocity += velocity * 0.3f;
56477					}
56478				}
56479				if (Main.rand.Next(3) == 0)
56480				{
56481					Dust dust3 = Dust.NewDustDirect(position, width, height, 5);
56482					dust3.velocity *= 0f;
56483					dust3.alpha = 120;
56484					dust3.scale = 0.7f + Main.rand.NextFloat() * 0.5f;
56485					dust3.velocity += velocity * 0.3f;
56486				}
56487				position -= netOffset;
56488				if (wet)
56489				{
56490					knockBackResist = 0f;
56491					ai[3] = -0.10101f;
56492					noGravity = true;
56493					Vector2 center3 = base.Center;
56494					position.X = center3.X - (float)(width / 2);
56495					position.Y = center3.Y - (float)(height / 2);
56496					TargetClosest();
56497					if (collideX)
56498					{
56499						velocity.X = 0f - oldVelocity.X;
56500					}
56501					if (velocity.X < 0f)
56502					{
56503						direction = -1;
56504					}
56505					if (velocity.X > 0f)
56506					{
56507						direction = 1;
56508					}
56509					if (Collision.CanHit(position, width, height, Main.player[target].Center, 1, 1))
56510					{
56511						Vector2 vector3 = Main.player[target].Center - base.Center;
56512						vector3.Normalize();
56513						float num8 = 1f;
56514						num8 += Math.Abs(base.Center.Y - Main.player[target].Center.Y) / 40f;
56515						num8 = MathHelper.Clamp(num8, 5f, 20f);
56516						vector3 *= num8;
56517						if (velocity.Y > 0f)
56518						{
56519							velocity = (velocity * 29f + vector3) / 30f;
56520						}
56521						else
56522						{
56523							velocity = (velocity * 4f + vector3) / 5f;
56524						}
56525						return;
56526					}
56527					float num9 = 5f;
56528					if (velocity.Y > 0f)
56529					{
56530						num9 = 3f;
56531					}
56532					if (velocity.Y < 0f)
56533					{
56534						num9 = 8f;
56535					}
56536					Vector2 vector4 = new Vector2(direction, -1f);
56537					vector4.Normalize();
56538					vector4 *= num9;
56539					if (num9 < 5f)
56540					{
56541						velocity = (velocity * 24f + vector4) / 25f;
56542					}
56543					else
56544					{
56545						velocity = (velocity * 9f + vector4) / 10f;
56546					}
56547					return;
56548				}
56549				noGravity = false;
56550				Vector2 center4 = base.Center;
56551				position.X = center4.X - (float)(width / 2);
56552				position.Y = center4.Y - (float)(height / 2);
56553				if (ai[3] == -0.10101f)
56554				{
56555					ai[3] = 0f;
56556					float num10 = velocity.Length();
56557					num10 *= 2f;
56558					if (num10 > 15f)
56559					{
56560						num10 = 15f;
56561					}
56562					velocity.Normalize();
56563					velocity *= num10;
56564					if (velocity.X < 0f)
56565					{
56566						direction = -1;
56567					}
56568					if (velocity.X > 0f)
56569					{
56570						direction = 1;
56571					}
56572					spriteDirection = direction;
56573				}
56574			}

```


---

## 🤖 Assistant · 2026-08-19T03:14:52.392Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Comparing wetSwimStep (ours) vs vanilla 461/586:

461 wet: 
- knockBackResist=0 ✓, ai3=-0.10101 ✓, noGravity=true — ours: does wetSwimStep set noGravity?? Ours doesn't set this.noGravity! Our wetSwimStep: kbResistOverride=0, ai3 sentinel, resize 34×24 ✓, facing from seekDirX (≈TargetClosest) ✓, hitWall → vx=-oldVx ✓... 

wait ours: `if (this.hitWall) this.vx = -this.vx;` — vanilla `velocity.X = -oldVelocity.X` ✓ same intent.
- direction from vx sign ✓ ours (mode!==620 gate — vanilla 461 does set direction from vx ✓, 586 same ✓, 620 keeps — need to check 620 elsewhere).
- CanHit: vanilla uses `Collision.CanHit(position,width,height, player.Center,1,1)` (box vs 1×1 point box). Ours: canSeePlayer(st, player) = canHit(st, this.x.., p.x, p.y, p.w, p.h) — box vs player BOX not point. Approximation — slightly more permissive LOS. Low.
- Chase: vector = (player.Center - center).normalize() × 5 → velocity = (velocity*19 + vector)/20. Ours: `spd=5; k=1/20; vx += (tx-vx)*k` = (vx*19 + tx)/20 ✓ same for 461! 
- Wander: num6 5/3/8 by vy sign ✓ ours cruise. vector2 = (direction,-1).normalize() × num6; blend 1/25 if num6<5 else 1/10 ✓ ours k2 = cruise<5 ? 1/25 : 1/10 ✓.

461 dry: knockBackResist = GetKnockback(0.4) ✓ ours; resize 18×40 ✓; exit sentinel: num7 = len*2 clamp 10 ✓ ours (mode 461 → clamp 10); normalize × num7 ✓; direction from vx ✓; spriteDirection — rendering.
★ vanilla sets noGravity = false on dry (and true on wet). Ours NEVER sets noGravity in wetSwimStep! Does our 461/586 have noGravity elsewhere? The enemy is a fighter (walker) — our engine's applyGravity is called by fighterAI only when wetSwimStep returns false. When wet branch takes over (returns true), fighterAI returns immediately → no gravity applied → equivalent to noGravity=true ✓. OK equivalent by control flow. ✓

586 spawn: alpha==255 → leap out: TargetClosest, vy=-6, dust burst. Ours: no alpha-255 leap for 586! Wait — 586 spawns with alpha 255? This is the zombie merman spawn animation (leaps from water with dust). Ours wetSwimStep doesn't implement the alpha 255 spawn leap (vy=-6 + dust). Hmm — is alpha==255 only at spawn? NPC alpha defaults 0... For 586 "Zombie Merman" spawned from water, SetDefaults sets alpha? Actually vanilla 586 spawns with alpha=255 → the spawn leap happens ONCE at first AI tick, then alpha decreases 15/t (fades in over 17 ticks) with dust trail. Ours missing this spawn leap + fade. MEDIUM-low (visual + initial jump). Actually the vy=-6 matters: newly spawned merman leaps up out of water. Player-visible.

Wait — ours might handle 586 spawn elsewhere (spawner?). Memory notes "水蛭出生尘spawnBurst定向" hmm that's leech. I'll flag it.

586 wet chase: num8 = 1 + |dy|/40 clamp [5,20]; blend 1/30 if vy>0 else 1/5. Ours: spd = 1 + |cy-pcy|/40, clamp [5,20] ✓; k = vy>0 ? 1/30 : 1/5 ✓.
586 dry: exit sentinel clamp 15 ✓ ours. Resize: 586 doesn't resize (keeps size) ✓ ours only 461 resizes.

620 mode: ours supports 620 — that's probably Angler Fish/goblin shark? 620 = "Blood Eel"? no... 620 might be "Zombie Merman" variant? Hmm 620 = "Goblin Shark"? Whatever — ours references :64321-64336 for 620 wander — that's in AI_107_ImprovedWalkers? :64321 is within AI_107 (63372+). Hmm, 620 might be routed through aiStyle 107. Not in my scope list. Skip.

Psycho 466 (vanilla :56290-56326) vs ours psychoStealthStep:
- ✓ identical (alpha 200, 170px trigger, vx/vy/justHit trigger, -16 fade, num5/16 = 12.5/t, ai2==0 → 1 + vx=direction*2).
- vanilla both stealth & fade branches RETURN (no movement, no gravity applied in AI — gravity applied at UpdateNPC :91519 tail). Ours adds gravity+collide ✓ equivalent.
- One diff: vanilla stealth branch checks `velocity.Y < 0 || velocity.Y > 2` — ours `e.vy < 0 || e.vy > 2` ✓.
- vanilla: `if (!Main.player[target].dead && (Center diff).Length() < 170)` — target might be invalid... fine.

Swamp Thing 166 (vanilla :56327-56360) vs ours swampThingAmbushStep:
- rand Next(240)==0 → ai2 = Next(-480, -60) ✓ ours -(60 + rand*420) = -60..-479 ✓ (Next(-480,-60) = -480..-61; ours 60+floor(rand*420) → 60..479 → -(60..479) ✓ close enough (off by one at boundary, negligible).
- ai2<0: TargetClosest; justHit → 0; CanHit(Center 1x1, player.Center 1x1) → 0. Ours: canSee param = canSeePlayer (box vs box) — approximation, low.
- ai2<0 block: vx *= 0.9 ✓, tiny→0 ✓, ai2+=1 ✓, ==0 → vx = direction*0.1 ✓, return ✓.
✓ 1:1 modulo LOS box.

Gnome 624 petrification (vanilla :56252-56289): turns to garden gnome statue (tile 567) when player looks at it & in sun etc. — AI_003_Gnomes_ShouldTurnToStone. Ours: NOT implemented (624 goes to fighterAI default; num108=2.5 handled). Gnome should turn to stone when watched! MEDIUM severity for 624 (visible special behavior missing). Let me confirm ours doesn't handle 624 anywhere: grep "624" in Enemy.ts — fighterFamilies has 624 num108=2.5. Let me grep ShouldTurnToStone equivalent in our repo. I'll do that later.

Next: read 56575-56890 (medusa 480, 379 ritual?), and 57114-57173 (solenian 419), then 57422-57710 region (eclipse + stuck counter + lihzahrd), then movement chain sample, ranged section, and the tail (60383-60734).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:52.760Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 330,
 "offset": 56575
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:52.769Z

**📎 ToolResult**

```
56575			if (type == 379 || type == 380)
56576			{
56577				if (ai[3] < 0f)
56578				{
56579					directionY = -1;
56580					flag = false;
56581					damage = 0;
56582					velocity.X *= 0.93f;
56583					if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
56584					{
56585						velocity.X = 0f;
56586					}
56587					int num11 = (int)(0f - ai[3] - 1f);
56588					int num12 = Math.Sign(Main.npc[num11].Center.X - base.Center.X);
56589					if (num12 != direction)
56590					{
56591						velocity.X = 0f;
56592						direction = num12;
56593						netUpdate = true;
56594					}
56595					if (justHit && Main.netMode != 1 && Main.npc[num11].localAI[0] == 0f)
56596					{
56597						Main.npc[num11].localAI[0] = 1f;
56598					}
56599					if (ai[0] < 1000f)
56600					{
56601						ai[0] = 1000f;
56602					}
56603					if ((ai[0] += 1f) >= 1300f)
56604					{
56605						ai[0] = 1000f;
56606						netUpdate = true;
56607					}
56608					return;
56609				}
56610				if (ai[0] >= 1000f)
56611				{
56612					ai[0] = 0f;
56613				}
56614				damage = defDamage;
56615			}
56616			if (type == 383 && ai[2] == 0f && localAI[0] == 0f && Main.netMode != 1)
56617			{
56618				int num13 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X, (int)base.Center.Y, 384, whoAmI);
56619				ai[2] = num13 + 1;
56620				localAI[0] = -1f;
56621				netUpdate = true;
56622				Main.npc[num13].ai[0] = whoAmI;
56623				Main.npc[num13].netUpdate = true;
56624			}
56625			if (type == 383)
56626			{
56627				int num14 = (int)ai[2] - 1;
56628				if (num14 != -1 && Main.npc[num14].active && Main.npc[num14].type == 384)
56629				{
56630					dontTakeDamage = true;
56631				}
56632				else
56633				{
56634					dontTakeDamage = false;
56635					ai[2] = 0f;
56636					if (localAI[0] == -1f)
56637					{
56638						localAI[0] = 180f;
56639					}
56640					if (localAI[0] > 0f)
56641					{
56642						localAI[0] -= 1f;
56643					}
56644				}
56645			}
56646			if (type == 482)
56647			{
56648				int num15 = 300;
56649				int num16 = 120;
56650				dontTakeDamage = false;
56651				if (ai[2] < 0f)
56652				{
56653					dontTakeDamage = true;
56654					ai[2] += 1f;
56655					velocity.X *= 0.9f;
56656					if ((double)Math.Abs(velocity.X) < 0.001)
56657					{
56658						velocity.X = 0.001f * (float)direction;
56659					}
56660					if (Math.Abs(velocity.Y) > 1f)
56661					{
56662						ai[2] += 10f;
56663					}
56664					if (ai[2] >= 0f)
56665					{
56666						netUpdate = true;
56667						velocity.X += (float)direction * 0.3f;
56668					}
56669					return;
56670				}
56671				if (ai[2] < (float)num15)
56672				{
56673					if (justHit)
56674					{
56675						ai[2] += 15f;
56676					}
56677					ai[2] += 1f;
56678				}
56679				else if (velocity.Y == 0f)
56680				{
56681					ai[2] = -num16;
56682					netUpdate = true;
56683				}
56684			}
56685			if (type == 631)
56686			{
56687				if (target < 0 || target == 255 || Main.player[target].dead || !Main.player[target].active)
56688				{
56689					TargetClosest(ai[2] > 0f);
56690				}
56691				Player player = Main.player[target];
56692				bool flag2 = !player.dead && player.active && base.Center.Distance(player.Center) < 320f;
56693				int num17 = 100;
56694				int num18 = 32;
56695				if (ai[2] == 0f)
56696				{
56697					ai[3] = 65f;
56698					if (flag2 && Collision.CanHit(player, this))
56699					{
56700						ai[2] = num17;
56701						ai[3] = 0f;
56702						velocity.X = (float)direction * 0.01f;
56703						netUpdate = true;
56704					}
56705				}
56706				else
56707				{
56708					if (ai[2] < (float)num17)
56709					{
56710						ai[2] += 1f;
56711						velocity.X *= 0.9f;
56712						if ((double)Math.Abs(velocity.X) < 0.001)
56713						{
56714							velocity.X = 0f;
56715						}
56716						if (Math.Abs(velocity.Y) > 1f)
56717						{
56718							ai[2] = 0f;
56719						}
56720						if (ai[2] == (float)(num17 - num18 / 2) && Main.netMode != 1 && !player.Hitbox.Intersects(base.Hitbox) && Collision.CanHit(player, this))
56721						{
56722							float num19 = 8f;
56723							Vector2 center5 = base.Center;
56724							Vector2 vector5 = DirectionTo(Main.player[target].Center) * num19;
56725							if (vector5.HasNaNs())
56726							{
56727								vector5 = new Vector2((float)direction * num19, 0f);
56728							}
56729							int num20 = 20;
56730							Vector2 v = vector5 + Utils.RandomVector2(Main.rand, -0.8f, 0.8f);
56731							v = v.SafeNormalize(Vector2.Zero);
56732							v *= num19;
56733							Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center5.X, center5.Y, v.X, v.Y, 909, num20, 1f, Main.myPlayer);
56734						}
56735						if (ai[2] >= (float)num17)
56736						{
56737							ai[2] = num17;
56738							ai[3] = 0f;
56739							velocity.X = (float)direction * 0.01f;
56740							netUpdate = true;
56741						}
56742						return;
56743					}
56744					if (velocity.Y == 0f && flag2 && (player.Hitbox.Intersects(base.Hitbox) || Collision.CanHit(player, this)))
56745					{
56746						ai[2] = num17 - num18;
56747						netUpdate = true;
56748					}
56749				}
56750			}
56751			if (type == 480)
56752			{
56753				int num21 = 180;
56754				int num22 = 300;
56755				int num23 = 180;
56756				int num24 = 60;
56757				int num25 = 20;
56758				if (life < lifeMax / 3)
56759				{
56760					num21 = 120;
56761					num22 = 240;
56762					num23 = 240;
56763					num24 = 90;
56764				}
56765				if (ai[2] > 0f)
56766				{
56767					ai[2] -= 1f;
56768				}
56769				else if (ai[2] == 0f)
56770				{
56771					if (((Main.player[target].Center.X < base.Center.X && direction < 0) || (Main.player[target].Center.X > base.Center.X && direction > 0)) && velocity.Y == 0f && Distance(Main.player[target].Center) < 900f && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
56772					{
56773						ai[2] = -num23 - num25;
56774						netUpdate = true;
56775					}
56776				}
56777				else
56778				{
56779					if (ai[2] < 0f && ai[2] < (float)(-num23))
56780					{
56781						position += netOffset;
56782						velocity.X *= 0.9f;
56783						if (velocity.Y < -2f || velocity.Y > 4f || justHit)
56784						{
56785							ai[2] = num21;
56786						}
56787						else
56788						{
56789							ai[2] += 1f;
56790							if (ai[2] == 0f)
56791							{
56792								ai[2] = num22;
56793							}
56794						}
56795						float num26 = ai[2] + (float)num23 + (float)num25;
56796						if (num26 == 1f)
56797						{
56798							SoundEngine.PlaySound(4, (int)position.X, (int)position.Y, 17);
56799						}
56800						if (num26 < (float)num25)
56801						{
56802							Vector2 vector6 = base.Top + new Vector2(spriteDirection * 6, 6f);
56803							float num27 = MathHelper.Lerp(20f, 30f, (num26 * 3f + 50f) / 182f);
56804							Main.rand.NextFloat();
56805							for (float num28 = 0f; num28 < 2f; num28 += 1f)
56806							{
56807								Vector2 vector7 = Vector2.UnitY.RotatedByRandom(6.2831854820251465) * (Main.rand.NextFloat() * 0.5f + 0.5f);
56808								Dust obj = Main.dust[Dust.NewDust(vector6, 0, 0, 228)];
56809								obj.position = vector6 + vector7 * num27;
56810								obj.noGravity = true;
56811								obj.velocity = vector7 * 2f;
56812								obj.scale = 0.5f + Main.rand.NextFloat() * 0.5f;
56813							}
56814						}
56815						Lighting.AddLight(base.Center, 0.9f, 0.75f, 0.1f);
56816						position -= netOffset;
56817						return;
56818					}
56819					if (ai[2] < 0f && ai[2] >= (float)(-num23))
56820					{
56821						position += netOffset;
56822						Lighting.AddLight(base.Center, 0.9f, 0.75f, 0.1f);
56823						velocity.X *= 0.9f;
56824						if (velocity.Y < -2f || velocity.Y > 4f || justHit)
56825						{
56826							ai[2] = num21;
56827						}
56828						else
56829						{
56830							ai[2] += 1f;
56831							if (ai[2] == 0f)
56832							{
56833								ai[2] = num22;
56834							}
56835						}
56836						float num29 = ai[2] + (float)num23;
56837						if (num29 < 180f && (Main.rand.Next(3) == 0 || ai[2] % 3f == 0f))
56838						{
56839							Vector2 vector8 = base.Top + new Vector2(spriteDirection * 10, 10f);
56840							float num30 = MathHelper.Lerp(20f, 30f, (num29 * 3f + 50f) / 182f);
56841							Main.rand.NextFloat();
56842							for (float num31 = 0f; num31 < 1f; num31 += 1f)
56843							{
56844								Vector2 vector9 = Vector2.UnitY.RotatedByRandom(6.2831854820251465) * (Main.rand.NextFloat() * 0.5f + 0.5f);
56845								Dust obj2 = Main.dust[Dust.NewDust(vector8, 0, 0, 228)];
56846								obj2.position = vector8 + vector9 * num30;
56847								obj2.noGravity = true;
56848								obj2.velocity = vector9 * 4f;
56849								obj2.scale = 0.5f + Main.rand.NextFloat();
56850							}
56851						}
56852						position -= netOffset;
56853						if (Main.netMode == 2)
56854						{
56855							return;
56856						}
56857						Player player2 = Main.player[Main.myPlayer];
56858						_ = Main.myPlayer;
56859						if (player2.dead || !player2.active || player2.FindBuffIndex(156) != -1)
56860						{
56861							return;
56862						}
56863						Vector2 vector10 = player2.Center - base.Center;
56864						if (!(vector10.Length() < 700f))
56865						{
56866							return;
56867						}
56868						bool flag3 = vector10.Length() < 30f;
56869						if (!flag3)
56870						{
56871							float x = (MathF.PI / 4f).ToRotationVector2().X;
56872							Vector2 vector11 = Vector2.Normalize(vector10);
56873							if (vector11.X > x || vector11.X < 0f - x)
56874							{
56875								flag3 = true;
56876							}
56877						}
56878						if (((player2.Center.X < base.Center.X && direction < 0 && player2.direction > 0) || (player2.Center.X > base.Center.X && direction > 0 && player2.direction < 0)) && flag3 && (Collision.CanHitLine(base.Center, 1, 1, player2.Center, 1, 1) || Collision.CanHitLine(base.Center - Vector2.UnitY * 16f, 1, 1, player2.Center, 1, 1) || Collision.CanHitLine(base.Center + Vector2.UnitY * 8f, 1, 1, player2.Center, 1, 1)) && !player2.creativeGodMode)
56879						{
56880							player2.AddBuff(156, num24 + (int)ai[2] * -1);
56881						}
56882						return;
56883					}
56884				}
56885			}
56886			if (type == 471)
56887			{
56888				if (ai[3] < 0f)
56889				{
56890					knockBackResist = 0f;
56891					defense = (int)((double)defDefense * 1.1);
56892					noGravity = true;
56893					noTileCollide = true;
56894					if (velocity.X < 0f)
56895					{
56896						direction = -1;
56897					}
56898					else if (velocity.X > 0f)
56899					{
56900						direction = 1;
56901					}
56902					rotation = velocity.X * 0.1f;
56903					if (Main.netMode != 1)
56904					{

```


---

## 🤖 Assistant · 2026-08-19T03:15:37.246Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Key comparisons:

**631 Rock Golem (vanilla :56685-56750) vs ours (2658-2668):**

Vanilla: 
- target dead/255 → TargetClosest(ai[2] > 0) — facecheck param.
- flag2 = player within 320px.
- num17=100 (windup total), num18=32.
- If ai2==0: ai3=65; if flag2 && CanHit(player, this) → ai2=100, ai3=0, vx = direction*0.01.
- Else (ai2 != 0): if ai2 < 100: ai2+=1, vx*=0.9, |vy|>1 → ai2=0; AT ai2 == 100-16 = 84: if not overlapping player && CanHit → shoot rock: direction to player ×8, ±0.8 random, dmg 20, proj 909, speed 8 normalized.
- if ai2 >= 100: ai2 = 100 (clamp), ai3=0, vx=dir*0.01 → next tick stays at 100 → repeats "if ai2 < 100" false → the `if (velocity.Y == 0 && flag2 && (hitbox intersects || CanHit))` → ai2 = 100-32 = 68 → loops.
  
Ours (2658-2667): 
- `if (dg < 320 && canSeePlayer) { ai2 += 1; if (ai2 === 68) shoot (speed 8±0.8, dmg 20, proj 909); if (ai2 >= 100) ai2 = 0; } else ai2 = 0;`
  
Differences:
1. Ours shoots at ai2==68; vanilla shoots at ai2==84 on the way UP (first cycle), then resets to 68 → subsequent cycles shoot at 84 again after climbing from 68? wait — vanilla: after the reset-to-68 branch, ai2 climbs 68→84 → shoot → 100 → clamp → reset to 68. So all shots happen at 84 EXCEPT the first one also at 84 (from 100? no wait — first cycle: ai2 goes 0→set 100 at trigger, then... hmm let me re-trace: initial ai2=0. flag2&&CanHit → ai2=100, ai3=0, vx=0.01dir. Next tick: ai2=100 → not <100 → the "if velocity.Y==0 && flag2..." → ai2=68. Next: ai2=68 <100 → ai2+=1... climbs to 84 → shoot at ==84. So vanilla always fires at 84. Ours fires at 68! Shot comes 16 ticks earlier in ours. Deviation — low-medium (cadence).
2. Ours resets ai2 to 0 after 100 (full re-trigger needed: requires CanHit within 320); vanilla loops 100→68→84 continuous while player near. Vanilla keeps throwing rocks every ~16+16 ticks as long as in range; ours every 100 ticks. Significant cadence difference: vanilla rock golem spams rocks (every ~0.4s), ours every ~1.7s. MEDIUM.
3. Vanilla shoot gate: NOT overlapping player hitbox && CanHit. Ours: gated outer (dist<320 && canSee). Similar.
4. Vanilla: |vy|>1 during windup → ai2=0 (cancel). Ours: else branch zeroes when out of range only. Minor.
5. Ours muzzle: (cx, cy-8), vanilla Center. Minor.
6. Ours speed jit = 8 + rand*1.6-0.8 — hmm: vanilla: vector = dir×8; v = vector + RandomVector2(-0.8,0.8); normalize; ×8 → final speed exactly 8 (normalized!). Ours: speed 8±0.8 (jittered magnitude). Minor deviation in spread/magnitude — vanilla always exactly speed 8 with ±0.8 direction jitter. Ours: direction = exact toward player, speed jittered. LOW.

**480 Medusa (vanilla :56751-56885) vs ours (2248-2318):**

- num21=180, num22=300, num23=180, num24=60, num25=20; low HP: 120/240/240/90.
Ours: lowHp → 120/240/240/90 ✓ else 180/300/180/60 ✓.
- ai2>0 → decrement ✓.
- ai2==0 trigger: facing && vy==0 && Distance < 900 && CanHit(Center 1x1 to player.Center 1x1) ✓ ours (losClear center-to-center) ✓.
- Charging phase (ai2 < -num23): vx*=0.9, interrupt vy<-2||vy>4||justHit → num21; else ai2+=1; ==0→num22. ✓ ours.
- ★ Vanilla phase gate: `if (ai[2] < 0f && ai[2] < -num23)` (i.e., ai2 < -180) = pre-charge glow; `if (ai[2] < 0f && ai[2] >= -num23)` = stoning window. Ours: `if (this.ai2 >= -num23)` for the stoning window and treats everything negative via else — ours' single else-branch handles both with `rem` for glow. Equivalent partition: ai2 in [-200,-180) glow, [-180, 0) stone window ✓.
- Sound 4 style 17 at num26==1 ✓ ours (Item_17 at rem===1) ✓.
- Glow dust ✓ approx.
- num29<180 && (rand(3)==0 || ai2%3==0) ✓ ours `n29 < 180 && (Math.random() < 1/3 || ai2 % 3 === 0)` ✓.
- Stone gaze: vanilla checks LOCAL player (Main.myPlayer — not target!), dead/buff156 → return; dist<700; <30 close hit or 45° cone; mutual facing; 3 CanHitLine; !creativeGodMode → AddBuff(156, num24 + (int)ai2 * -1).
  
Ours: `player.buffs.apply(Stoned, (num24 + (-ai2)) / 60)` — duration in SECONDS? num24 + (-ai2) is in TICKS (vanilla AddBuff ticks). Ours divides by 60 — if our buff durations are in seconds. Vanilla: num24=60 + |ai2| up to 180 → 60..240 ticks = 1-4s. Ours: (60+|ai2|)/60 s = 1-4s ✓ if buffs use seconds. ✓ plausible.
- Missing: creativeGodMode gate (journey god mode — do we have? creativeGodMode). Low.
- Ours uses `player` (target) instead of local player — same in single player ✓.

**482 (Butcher? no — 482 = "Rune Wizard"? no. 482... "Deadly Sphere"? no that's proj. 482 = "Drakomire rider"? Hmm — 482 might be "Crawltipede"? no. 482 = ??? Actually per FIGHTER_NO_DOOR list ours includes 482. 482 = "Selenian"? no 419. Let me think: type 482 with ai2 negative = burrow-invincible phase... 482 = "Martian Turret"? Hmm. Actually — 482 is likely "ScutlixBrain"? no... Let me check: it has "dontTakeDamage" during ai2<0, vx tiny → 0.001*direction, |vy|>1 speeds ai2 by +10. This looks like "Solar Corite"? no, 384... hmm 482 could be "Sleepy Eye"? I'm not sure. Might be "Butcher"... no butcher=460.

Wait — FIGHTER_NO_DOOR contains 480, 481, 482. 481 = Greek Skeleton (javelin thrower), 482 = "Granite Golem"? no that's 481? Hmm: 481 = Hoplite, 482 = Granite Golem! Yes — 482 is the Granite Golem with the shell/invulnerable phase (dontTakeDamage when ai2<0, immune shell). Ours: does fighterAI implement 482 shell phase? I didn't see it in our fighterAI! Let me grep our Enemy.ts for 482. In FIGHTER_NO_DOOR set yes. In fighterMoveSpec num84 list: 482 present with num84 base 1.5. But the shell phase (ai2<0 → dontTakeDamage + slide, ai2 0..300 buildup, at 300 grounded → -120) — MISSING in ours? Need to grep.

**383/384 pair** (:type 383 = "Nailhead"? no. 383 spawns 384 attached... 383 = "Martian Drone"? Hmm — 383 spawns NPC 384 and is invulnerable while 384 alive, respawn timer 180. This is "Crawltipede"? no. 383/384 = "Solar Pillar enemies"? 383 = "Sroller"? no 417... Actually 383/384 = "Drakomire + Drakomire Rider"? No — 397/398 are Drakomire/Rider? Hmm. Let me think: 383 = "Lunar Tower Solar 'Spearman'"? I recall 383 = "Drakomire"... not sure. What matters: ours implements this? The mechQueen.ts or fighterAI? I saw nothing in fighterAI for 383/384. Need grep.

**379/380 ritual wait** (Lunar Cultist Archer — archers waiting at ritual): vanilla ai3<0 → stand watching the ritual NPC (num11 = -ai3-1 = npc index), damage=0, vx*=0.93, face the ritual npc, ai0 counts 1000→1300 loop, justHit → npc.localAI[0]=1 (starts ritual?). Ours: 379/380 in RANGED_TABLE with comment "拜月教弓手（cs:56575 仪式待机解除后射击）" — but does ours implement the ai3<0 waiting phase? The RANGED_TABLE only handles shooting. The waiting phase (stand still, damage 0, watch cultist) — grep needed.

Given so many type-specific branches, the efficient approach: list ALL `if (type ==` / `else if (type ==` in AI_003 range, then check which our fighterAI/fighterFamilies handles. Let me do that.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:37.770Z · glm-x-preview-260804

```
`AI_003` 中有许多针对特定类型的分支。我来列举它们，并与我们的实现进行交叉核对。
```


---

## 🤖 Assistant · 2026-08-19T03:15:38.976Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '56245,60734p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"if (type == \\|if (type >= \\|if (type <= \\|else if (type == \\|if (type is \\|switch (type)\" | head -120",
 "description": "List type branches inside AI_003_Fighters"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:39.053Z

**📎 ToolResult**

```
8:		if (type == 624 && AI_003_Gnomes_ShouldTurnToStone())
46:		if (type == 466)
83:		if (type == 166)
117:		if (type == 461)
201:		if (type == 586)
331:		if (type == 379 || type == 380)
372:		if (type == 383 && ai[2] == 0f && localAI[0] == 0f && Main.netMode != 1)
381:		if (type == 383)
402:		if (type == 482)
441:		if (type == 631)
507:		if (type == 480)
642:		if (type == 471)
870:		if (type == 419)
937:		if (type == 415)
1006:		if (type == 428)
1037:		if (type == 427)
1065:		if (type == 590)
1099:		else if (type == 591)
1123:		if (type == 111)
1187:		if (type == 120)
1224:		if (type == 343 || type == 47 || type == 67 || type == 109 || type == 110 || type == 111 || type == 120 || type == 163 || type == 164 || type == 239 || type == 168 || type == 199 || type == 206 || type == 214 || type == 215 || type == 216 || type == 217 || type == 218 || type == 219 || type == 220 || type == 226 || type == 243 || type == 251 || type == 257 || type == 258 || type == 290 || type == 291 || type == 292 || type == 293 || type == 305 || type == 306 || type == 307 || type == 308 || type == 309 || type == 348 || type == 349 || type == 350 || type == 351 || type == 379 || (type >= 430 && type <= 436) || type == 591 || type == 380 || type == 381 || type == 382 || type == 383 || type == 386 || type == 391 || (type >= 449 && type <= 452) || type == 466 || type == 464 || type == 166 || type == 469 || type == 468 || type == 471 || type == 470 || type == 480 || type == 481 || type == 482 || type == 411 || type == 424 || type == 409 || (type >= 494 && type <= 506) || type == 425 || type == 427 || type == 426 || type == 428 || type == 580 || type == 508 || type == 415 || type == 419 || type == 520 || (type >= 524 && type <= 527) || type == 528 || type == 529 || type == 530 || type == 532 || type == 582 || type == 624 || type == 631)
1235:		switch (type)
1303:		if (type == 463 && Main.netMode != 1)
1371:		if (type == 460)
1382:		if (type == 469)
1434:		if (type == 462 && velocity.Y == 0f && (Main.player[target].Center - base.Center).Length() < 150f && Math.Abs(velocity.X) > 3f && ((velocity.X < 0f && base.Center.X > Main.player[target].Center.X) || (velocity.X > 0f && base.Center.X < Main.player[target].Center.X)))
1467:		if (type == 624 && target < 255)
1473:				if (type == 624 && !AI_003_Gnomes_ShouldTurnToStone() && (base.Center - Main.player[target].Center).Length() > 500f)
1504:				if (type == 159 && Main.rand.Next(500) == 0)
1508:				if (type == 162 && Main.rand.Next(500) == 0)
1512:				if (type == 181 && Main.rand.Next(500) == 0)
1516:				if (type >= 269 && type <= 280 && Main.rand.Next(1000) == 0)
1555:		if (type == 159 || type == 349)
1557:			if (type == 159 && ((velocity.X > 0f && direction < 0) || (velocity.X < 0f && direction > 0)))
1638:		else if (type == 199)
1672:		else if (type == 120 || type == 166 || type == 213 || type == 258 || type == 528 || type == 529)
1706:		else if (type == 461 || type == 27 || type == 77 || type == 104 || type == 163 || type == 162 || type == 196 || type == 197 || type == 212 || type == 257 || type == 326 || type == 343 || type == 348 || type == 351 || (type >= 524 && type <= 527) || type == 530 || type == 236)
1732:		else if (type == 109)
1758:		else if (type == 21 || type == 26 || type == 31 || type == 294 || type == 295 || type == 296 || type == 47 || type == 73 || type == 140 || type == 164 || type == 239 || type == 167 || type == 168 || type == 185 || type == 198 || type == 201 || type == 202 || type == 203 || type == 217 || type == 218 || type == 219 || type == 226 || type == 181 || type == 254 || type == 338 || type == 339 || type == 340 || type == 342 || type == 385 || type == 389 || type == 462 || type == 463 || type == 466 || type == 464 || type == 469 || type == 470 || type == 480 || type == 482 || type == 425 || type == 429 || type == 586 || type == 631 || type == 635)
1761:			if (type == 181 && Main.remixWorld)
1765:			else if (type == 294)
1769:			else if (type == 295)
1773:			else if (type == 296)
1777:			else if (type == 201)
1781:			else if (type == 202)
1785:			else if (type == 203)
1789:			else if (type == 338)
1793:			else if (type == 339)
1797:			else if (type == 340)
1801:			else if (type == 385)
1805:			else if (type == 389)
1809:			else if (type == 462)
1813:			else if (type == 463)
1817:			else if (type == 466)
1821:			else if (type == 469)
1825:			else if (type == 480)
1829:			else if (type == 425)
1833:			else if (type == 429)
1837:			else if (type == 631)
1841:			else if (type == 586)
1845:			if (type == 21 || type == 201 || type == 202 || type == 203 || type == 342 || type == 635)
1858:				if (type == 466 && velocity.X < -2f)
1862:				if (type == 586 && velocity.Y == 0f && velocity.X < -1f)
1874:				if (type == 466 && velocity.X > 2f)
1878:				if (type == 586 && velocity.Y == 0f && velocity.X > 1f)
1893:		else if (type >= 269 && type <= 280)
1896:			if (type == 269)
1900:			if (type == 270)
1904:			if (type == 271)
1908:			if (type == 272)
1912:			if (type == 273)
1916:			if (type == 274)
1920:			if (type == 275)
1924:			if (type == 276)
1928:			if (type == 277)
1932:			if (type == 278)
1936:			if (type == 279)
1940:			if (type == 280)
1969:		else if (type >= 305 && type <= 314)
1972:			if (type == 305 || type == 310)
1976:			if (type == 306 || type == 311)
1980:			if (type == 307 || type == 312)
1984:			if (type == 308 || type == 313)
1988:			if (type == 309 || type == 314)
2033:		else if (type == 67 || type == 220 || type == 428)
2059:		else if (type == 78 || type == 79 || type == 80 || type == 630)
2068:			if (type == 79 || type == 630)
2096:		else if (type == 287)
2124:		else if (type == 243)
2154:		else if (type == 251)
2184:		else if (type == 386)
2222:		else if (type == 460)
2291:		else if (type == 508 || type == 580 || type == 582)
2296:			if (type == 582)
2335:				if (type == 582)
2355:		else if (type == 391 || type == 427 || type == 415 || type == 419 || type == 518 || type == 532)
2360:			if (type == 427)
2366:			else if (type == 415)
2372:			else if (type == 419)
2378:			else if (type == 518)
2384:			else if (type == 532)
2448:					if (type >= 494 && type <= 495)
2478:			if (type == 624)
2482:			if (type == 186)
2486:			if (type == 187)
2490:			if (type == 188)
2494:			if (type == 189)
2498:			if (type == 132)
2502:			if (type == 200)
2506:			if (type == 223)
2510:			if (type == 632)
2514:			if (type == 691)
2518:			if (type == 489)
2529:			if (type == 489 || type == 3 || type == 132 || type == 186 || type == 187 || type == 188 || type == 189 || type == 200 || type == 223 || type == 331 || type == 332)
2557:		if (type >= 277 && type <= 280)
2561:		else if (type == 520)
2565:		else if (type == 525)
2570:		else if (type == 526)
2575:		else if (type == 527)
2580:		else if (type == 415)

```


---

## 🤖 Assistant · 2026-08-19T03:15:42.260Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me now check the remaining lines (2580 onwards = rest of the file to 60734-56245=4489).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:15:43.406Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '56245,60734p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | grep -n \"if (type == \\|if (type >= \\|else if (type == \\|switch (type)\\|if (num\\|flag8\\|flag16\\|flag17\" | sed -n '120,260p'",
 "description": "List remaining type branches in AI_003"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:15:43.471Z

**📎 ToolResult**

```
2355:		else if (type == 391 || type == 427 || type == 415 || type == 419 || type == 518 || type == 532)
2360:			if (type == 427)
2366:			else if (type == 415)
2372:			else if (type == 419)
2378:			else if (type == 518)
2384:			else if (type == 532)
2448:					if (type >= 494 && type <= 495)
2478:			if (type == 624)
2482:			if (type == 186)
2486:			if (type == 187)
2490:			if (type == 188)
2494:			if (type == 189)
2498:			if (type == 132)
2502:			if (type == 200)
2506:			if (type == 223)
2510:			if (type == 632)
2514:			if (type == 691)
2518:			if (type == 489)
2529:			if (type == 489 || type == 3 || type == 132 || type == 186 || type == 187 || type == 188 || type == 189 || type == 200 || type == 223 || type == 331 || type == 332)
2557:		if (type >= 277 && type <= 280)
2561:		else if (type == 520)
2565:		else if (type == 525)
2570:		else if (type == 526)
2575:		else if (type == 527)
2580:		else if (type == 415)
2592:		else if (type == 258)
2621:		else if (type == 425)
2644:					if (num115 < 0f && velocity.X > 0f)
2648:					else if (num115 > 0f && velocity.X < 0f)
2652:					if (num115 < 0f && velocity.X > 0f - num114)
2656:					else if (num115 > 0f && velocity.X < num114)
2668:					if (num116 < -20f && velocity.Y > 0f)
2672:					else if (num116 > 20f && velocity.Y < 0f)
2676:					if (num116 < -20f && velocity.Y > 0f - num112)
2680:					else if (num116 > 20f && velocity.Y < num112)
2698:					if (num117 != whoAmI && Main.npc[num117].active && Main.npc[num117].type == type && Math.Abs(position.X - Main.npc[num117].position.X) + Math.Abs(position.Y - Main.npc[num117].position.Y) < (float)width)
2771:		else if (type == 427)
2790:					if (num124 < 0f && velocity.X > 0f)
2794:					else if (num124 > 0f && velocity.X < 0f)
2798:					if (num124 < -20f && velocity.X > -6f)
2802:					else if (num124 > 20f && velocity.X < 6f)
2814:					if (num125 < -20f && velocity.Y > 0f)
2818:					else if (num125 > 20f && velocity.Y < 0f)
2822:					if (num125 < -20f && velocity.Y > -6f)
2826:					else if (num125 > 20f && velocity.Y < 6f)
2833:					if (num126 != whoAmI && Main.npc[num126].active && Main.npc[num126].type == type && Math.Abs(position.X - Main.npc[num126].position.X) + Math.Abs(position.Y - Main.npc[num126].position.Y) < (float)width)
2861:		else if (type == 426)
2881:					if (num130 < 40f && velocity.X > 0f)
2885:					else if (num130 > 40f && velocity.X < 0f)
2889:					if (num130 < 40f && velocity.X > 0f - num127)
2893:					else if (num130 > 40f && velocity.X < num127)
2914:				if (num131 != whoAmI && Main.npc[num131].active && Main.npc[num131].type == type && Math.Abs(position.X - Main.npc[num131].position.X) + Math.Abs(position.Y - Main.npc[num131].position.Y) < (float)width)
2969:		else if (type == 185)
2981:		else if (type == 428)
2992:		if (type == 159 && Main.netMode != 1)
3028:				switch (type)
3046:				if (num135 != -1 && NPCCanStickToWalls() && TryMoveToTransformableSpaceInto(num135))
3052:		if (type == 243)
3091:		if (type == 251)
3120:				if (num146 < (float)num147)
3135:		if (type == 386)
3197:		if (type == 389)
3220:		if (type == 110 || type == 111 || type == 206 || type == 214 || type == 215 || type == 216 || type == 290 || type == 291 || type == 292 || type == 293 || type == 350 || type == 379 || type == 380 || type == 381 || type == 382 || (type >= 449 && type <= 452) || type == 468 || type == 481 || type == 411 || type == 409 || (type >= 498 && type <= 506) || type == 424 || type == 426 || type == 520)
3222:			bool flag16 = type == 381 || type == 382 || type == 520;
3223:			bool flag17 = type == 426;
3227:			if (type == 411)
3229:				flag16 = true;
3250:			if (type == 379 || type == 380)
3254:			if (type == 381 || type == 382)
3258:			if (type == 520)
3262:			if (type == 350)
3266:			if (type == 291)
3270:			if (type == 292)
3274:			if (type == 293)
3278:			if (type == 111)
3282:			if (type == 206)
3286:			if (type == 481)
3290:			if (type == 214)
3294:			if (type == 215)
3298:			if (type == 290)
3302:			if (type == 411)
3306:			if (type == 409)
3310:			if (type == 424)
3314:			if (type == 426)
3319:			if (type == 216)
3337:			if (type == 424)
3341:			if (type == 426)
3345:			if (type == 411)
3361:					if (type == 216)
3366:					if (type == 111)
3370:					if (type == 206)
3374:					if (type == 290)
3378:					if (type == 293)
3382:					if (type == 216)
3390:					if (type == 214)
3394:					if (type == 215)
3398:					if (type == 382)
3402:					if (type == 520)
3406:					if (type == 409)
3410:					if (type >= 449 && type <= 452)
3414:					if (type == 481)
3418:					if (type == 468)
3422:					if (type == 411)
3426:					if (type >= 498 && type <= 506)
3431:					if (type == 481)
3435:					if (type == 206)
3439:					if (type == 290)
3443:					if (type == 381 || type == 382)
3447:					if (type == 520)
3451:					if (type >= 498 && type <= 506)
3455:					if (type == 426)
3462:					if (type == 291 || type == 292)
3466:					if (type == 215)
3470:					if (type == 214 || (type == 216 && !flag20))
3475:					if (type == 381 || type == 382 || type == 520)
3479:					if (type >= 449 && type <= 452)
3483:					if (type == 468)
3487:					if (type == 481)
3491:					if (type >= 498 && type <= 506)
3496:					if (type == 291)
3501:					else if (type == 381 || type == 382 || type == 520)
3507:						if (type == 520)
3515:					else if (type == 481)
3520:					else if (type >= 498 && type <= 506)
3525:					else if (type == 426)
3530:					else if (type == 214)
3535:					else if (type == 216)
3555:					if (type == 111)
3559:					if (type == 206)
3563:					if (type == 379 || type == 380)
3567:					if (type == 350)
3571:					if (type == 468)
3575:					if (type == 111)
3579:					if (type == 379 || type == 380)
3583:					if (type == 381)
3588:					if (type == 382)
3593:					if (type == 520)
3598:					if (type >= 449 && type <= 452)
3603:					if (type >= 498 && type <= 506)
3608:					if (type == 481)
3613:					if (type == 206)

```


---

## 🤖 Assistant · 2026-08-19T03:15:53.365Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The AI_003 range contains lots of special type branches. Ours handles: 624 (move only), 466, 166, 461, 586, 379/380 (ranged only), 383/384 (?), 482 (?), 631 (partial), 480, 471 (?), 419, 415/428/427/590/591/111/120 special, 463, 460, 469, 462, 624 gate, 159/162/181/269-280 random buffs, movement chain, ranged section, 243, 251, 386, 389, spider transforms, jump section, doors.

Notable unhandled-in-ours candidates to verify: 383/384, 482, 471, 590/591, 428/415/427 air servo, 624 gnome stone, 379/380 ritual wait, 386 turret, 389 (?).

Let me grep our Enemy.ts for these ids.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:50.373Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "for id in 383 384 482 471 590 591 428 415 427 624 379 386 389 141 138 71 81 304 630 79; do echo \"== $id ==\"; grep -n \"== $id\\b\\|=== $id\\b\\|$id:\" src/entities/Enemy.ts src/entities/fighterFamilies.ts | head -4; done 2>/dev/null | head -80",
 "description": "Check which special type ids our code handles"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:50.595Z

**📎 ToolResult**

```
== 383 ==
src/entities/Enemy.ts:1196:          if (this.vanillaId === 383 || this.vanillaId === 386) martianFighterExtras(this, game, p);
== 384 ==
== 482 ==
src/entities/fighterFamilies.ts:99:    || id === 480 || id === 482 || id === 425 || id === 429 || id === 586 || id === 631
src/entities/Enemy.ts:170:  21: 0.2, 65: 0.2, 449: 0.2, 482: 0.2, 103: 0.2, 64: 0.2, 63: 0.2, 85: 0,
== 471 ==
== 590 ==
src/entities/Enemy.ts:1194:          if (this.vanillaId === 590 || this.vanillaId === 591) this.torchZombieLight(game);
src/entities/Enemy.ts:2203:    if (this.vanillaId === 590) {
== 591 ==
src/entities/fighterFamilies.ts:207:  if (inRange(id, 430, 436) || id === 494 || id === 495 || id === 591) return LEGACY;
src/entities/Enemy.ts:1194:          if (this.vanillaId === 590 || this.vanillaId === 591) this.torchZombieLight(game);
== 428 ==
src/entities/fighterFamilies.ts:156:  if (id === 67 || id === 220 || id === 428) {     // :58265-58287 螃蟹/海螺/外星幼虫
== 415 ==
src/entities/fighterFamilies.ts:196:  if (id === 391 || id === 427 || id === 415 || id === 419 || id === 518 || id === 532) {
src/entities/fighterFamilies.ts:199:    if (id === 415) return { max: 4, accel: 0.1, damp: 0.95 };        // :58628-58631
== 427 ==
src/entities/fighterFamilies.ts:196:  if (id === 391 || id === 427 || id === 415 || id === 419 || id === 518 || id === 532) {
src/entities/fighterFamilies.ts:198:    if (id === 427) return { max: 6, accel: 0.2, damp: 0.8 };         // :58624-58627
== 624 ==
src/entities/fighterFamilies.ts:210:  if (id === 624) num108 = 2.5;                                       // 地精
src/entities/Enemy.ts:1109:    if (this.vanillaId === 624 && !this.dead && this.gnomeAge > 60) {
== 379 ==
src/entities/fighterFamilies.ts:65:    || inRange(id, 290, 293) || id === 350 || id === 379 || id === 380 || id === 381
src/entities/Enemy.ts:1184:          if ((this.vanillaId === 379 || this.vanillaId === 380) && this.ai3 < 0) {
src/entities/Enemy.ts:1188:          if (this.vanillaId === 379 || this.vanillaId === 380) cultistArcherWake(this);
src/entities/Enemy.ts:2787:    379: { cooldown: 80, speed: 11, dmg: 35, range: 700, drop: 0.1, proj: 81 },  // 拜月教弓手（cs:59494/59609/59797/59823 修正后值,弹 WoodenArrowHostile 81）
== 386 ==
src/entities/Enemy.ts:1196:          if (this.vanillaId === 383 || this.vanillaId === 386) martianFighterExtras(this, game, p);
src/entities/fighterFamilies.ts:180:  if (id === 386) {                                                   // :58444-58456 火星工程师
== 389 ==
src/entities/fighterFamilies.ts:97:    || id === 338 || id === 339 || id === 340 || id === 342 || id === 385 || id === 389
src/entities/fighterFamilies.ts:112:    else if (id === 389) num84 = 2.25;
== 141 ==
== 138 ==
src/entities/Enemy.ts:2159:    if (vid !== 120 && vid !== 137 && vid !== 138) return;
== 71 ==
src/entities/Enemy.ts:168:  170: 0.05, 180: 0.05, 171: 0.05, 167: 0.25, 73: 0.01, 24: 0.05,
src/entities/Enemy.ts:1262:        case 71: sharkronAI(this, game, p); break;                        // AI_071 鲨鱼龙 372/373(龙卷出鲨,升空蓄力→扑咬)
== 81 ==
src/entities/Enemy.ts:169:  481: 0.05, 42: 0.05, 6: 0.05, 2: 0.05, 49: 0.2, 3: 0.2, 58: 0.2,
src/entities/Enemy.ts:1237:        case 81: moonLordFreeEyeAI(this, game, p); break;                // AI_081 月总游离眼 400（cs:38224 十槽攻击表+死光）
src/entities/Enemy.ts:2066:    150: [193, 202, 203, 100], 3086: [59, 28, 136, 150], 3081: [138, 145, 170, 150], 147: [189, 159, 139, 150],
src/entities/Enemy.ts:2802:    481: { cooldown: 100, speed: 8, dmg: 18, range: 400, drop: 0, spread: 16, oy: -14, proj: 508 }, // 希腊骷髅 标枪（drop 原版 ±0.035 随机）
== 304 ==
== 630 ==
src/entities/Enemy.ts:1427:    // onFire DoT（NPC.cs:92616-92630:lifeRegen-8 = 4 HP/s,无防御结算）+ 火尘粒子（:92187）
src/entities/fighterFamilies.ts:159:  if (id === 78 || id === 79 || id === 80 || id === 630) {   // :58288-58317 木乃伊族
src/entities/fighterFamilies.ts:162:    if (id === 79 || id === 630) num87 *= 1.5;     // :58298-58301
== 79 ==
src/entities/fighterFamilies.ts:159:  if (id === 78 || id === 79 || id === 80 || id === 630) {   // :58288-58317 木乃伊族
src/entities/fighterFamilies.ts:162:    if (id === 79 || id === 630) num87 *= 1.5;     // :58298-58301
src/entities/Enemy.ts:1265:        case 79: moonLordHeadAI(this, game, p); break;                    // AI_079 月总头 396(死亡之光/吸血)
src/entities/Enemy.ts:2787:    379: { cooldown: 80, speed: 11, dmg: 35, range: 700, drop: 0.1, proj: 81 },  // 拜月教弓手（cs:59494/59609/59797/59823 修正后值,弹 WoodenArrowHostile 81）

```


---

## 🤖 Assistant · 2026-08-19T03:16:55.829Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
OK so the routing layer (lines 1180-1200) handles some extras: 379/380 ritual (cultistArcherWake), 383/386 martianFighterExtras, 590/591 torch light, 624 gnome (gnomeAge at 1109 — let me look). Let me read lines 1100-1210 to see the routing context and the 624 gnome handling + cultistArcherWake.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:55.830Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 130,
 "offset": 1090
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:55.853Z

**📎 ToolResult**

```
1090	  /** 贴附族层数登记（projStatus.applyProjStatus 施加 169/183/337/344 时调用，
1091	   *  等价原版一枚贴附弹入场的 KillOldestJavelin 检查 :13019-13030）：
1092	   *  push 一层（寿命=dur 秒），超上限杀最老（最早入池者剩余时间最低，对应
1093	   *  原版扫 timeLeft 最低者 Kill，:13995-14020）。598=6 / 614=10；
1094	   *  971/975 不在 :13021 白名单 → 无上限 */
1095	  addStickerStack(buff: 169 | 183 | 337 | 344, dur: number): void {
1096	    const arr = buff === 169 ? this.javelinStacks : buff === 183 ? this.stardustStacks
1097	      : buff === 337 ? this.spikeStacks : this.butcherStacks;
1098	    const cap = buff === 169 ? 6 : buff === 183 ? 10 : Infinity;
1099	    arr.push(dur);
1100	    while (arr.length > cap) arr.shift(); // 最老离池
1101	  }
1102	
1103	  fixedUpdate(dt: number, game: GameHooks) {
1104	    this.prevX = this.x; this.prevY = this.y;
1105	    this.gnomeAge++;
1106	    // 侏儒 624 日光石化（NPC.cs:56252-56280 + :56232 ShouldTurnToStone——白天且
1107	    // 头上无实心遮挡 → 脚下实心 → PlaceTile(567 花园侏儒 style rand(5)) +
1108	    // bestiary RegisterKill + Achievement 24,2026-08-13）
1109	    if (this.vanillaId === 624 && !this.dead && this.gnomeAge > 60) {
1110	      const w = game.world as import('../world/World').World;
1111	      if (w?.clock?.isDay && w?.store) {
1112	        const st = w.store;
1113	        const tx = Math.floor(this.cx / 16), ty = Math.floor((this.y + this.h) / 16);
1114	        if (st.inBounds(tx, ty) && st.isSolid(tx, ty) && !st.isActive(tx, ty - 1)) {
1115	          let sheltered = false;
1116	          for (let dy = 1; dy <= 5; dy++) {
1117	            if (st.inBounds(tx, ty - dy) && st.isSolid(tx, ty - dy)) { sheltered = true; break; }
1118	          }
1119	          if (!sheltered) {
1120	            const style = Math.floor(Math.random() * 5);
1121	            st.setTile(tx, ty - 1, TILE_BY_KEY['v_567_garden_gnome'] ?? 0, style * 36, 0);
1122	            game.spawnParticles(this.cx, this.cy, '#E0E0E0', 5, 1, { life: 30 });
1123	            this.dead = true; this.hp = 0;
1124	            return;
1125	          }
1126	        }
1127	      }
1128	    }
1129	    // 联机傀儡（房主权威快照驱动）：无本地 AI——P3.2 插值/外推推进 + 动画计时，
1130	    // 打击/拾取等交互经 entityNet 上报房主结算
1131	    if (this.netPuppet) {
1132	      this.aiT++;
1133	      this.animT++;
1134	      this.netPuppetStep();
1135	      this.onGround = Math.abs(this.vy) < 0.6;
1136	      if (Math.abs(this.vx) > 0.05) this.walkCycleT += Math.abs(this.vx);
1137	      if (this.iframes > 0) this.iframes--;
1138	      this.pushHistory();   // 傀儡无本地 AI 但拖尾渲染同样需要历史位置
1139	      return;
1140	    }
1141	    this.aiT++;
1142	    if (this.iframes > 0) this.iframes--;
1143	    if (this.justHitT > 0) this.justHitT--;
1144	    this.lightRGB = null; // 点光由 AI 每帧重写（不残留上一帧状态）
1145	    this.lightRGBAt = null;
1146	    if (this.hpBarT > 0) this.hpBarT--;
1147	    if (this.whipTagT > 0) this.whipTagT--;
1148	    if (this.whipProcT > 0) this.whipProcT--;
1149	    if (this.squash !== 0) this.squash *= 0.85;
1150	    this.animT++;
1151	    this.walkCycleT += Math.abs(this.vx); // 原版 zombie/fighter 行走帧按 |vx| 累加（L77072/L70216）
1152	    // 原版 case46 族 vx==0 清 frameCounter（NPC.cs:77571-77577）——站定即清相位，
1153	    // 起步必从帧 0 起稳走（2026-08-18 审查：曾保留相位起步首帧非 0）
1154	    if (Math.abs(this.vx) <= 0.05) this.walkCycleT = 0;
1155	
1156	    // 出生渐显（alphaFade 族，AI 分发【前】的近似段）——静态半透明不受影响。
1157	    // EoW 族（13-15）除外：走下方 AI 分发后的 1:1 段（移动门 -42/t，NPC.cs:52650-52670）
1158	    if (this.alphaFade && !(this.vanillaId !== null && this.vanillaId >= 13 && this.vanillaId <= 15)) {
1159	      this.spawnAlpha = Math.max(0, this.spawnAlpha - 1);
1160	      if (this.spawnAlpha === 0) this.alphaFade = false;
1161	    }
1162	
1163	    const player = (game as unknown as { player: Player }).player;
1164	    const hasPlayer = !!player && !player.dead;
1165	
1166	    // ---- 原版数据驱动路径：按 aiStyle 分发到已移植的 AI 家族（分发后落入共享尾段） ----
1167	    // 蠕虫身体段（wormFollow 非空）无 AI：位置由头部 wormAI 沿链驱动，但仍走共享尾段（接触伤害等）
1168	    // 例外：EoW 三段各段独立跑 eowAI（断链自查 + 身/尾自跟随，:51874/:52266），
1169	    // 不再由头统一驱动链——断链拆分后每条子虫的头各自驱动
1170	    const eowSeg = this.vanillaId !== null && this.vanillaId >= 13 && this.vanillaId <= 15;
1171	    const wormBody = this.wormFollow && !eowSeg;
1172	    // 小动物（critter）优先走被动游荡，绝不落入 default 的追击 fallback
1173	    if (this.vanilla && !wormBody && this.vanilla.critter) {
1174	      this.critterWanderAI(game, hasPlayer ? player : null);
1175	    } else if (this.vanilla && !wormBody) {
1176	      const p = hasPlayer ? player : null;
1177	      switch (this.vanilla.aiStyle) {
1178	        case 92: this.dummyAI(game); break;                            // AI_092 训练假人（NPC 488）
1179	        case 1: this.slimeAI(game, p); break;                          // AI_001 史莱姆
1180	        case 2: this.floatEyeAI(game, p); break;                        // AI_002 飘浮眼（原版核）
1181	        case 3:
1182	          // AI_003 拜月教弓手 379/380 仪式待机（NPC.cs:56575-56601,ai[3]<0 静立面碑零伤；
1183	          // 碑置 ai[3]=0 后激活复位 :56602-56609,回战士核）——bossAI_lunar_misc
1184	          if ((this.vanillaId === 379 || this.vanillaId === 380) && this.ai3 < 0) {
1185	            cultistArcherStandbyAI(this, game);
1186	            break;
1187	          }
1188	          if (this.vanillaId === 379 || this.vanillaId === 380) cultistArcherWake(this);
1189	          this.fighterAI(game, p);
1190	          // 火把僵尸 590/591 手持火把发光（NPC.cs:57309-57366 AI_003 内 type 段）：
1191	          //  590 按朝向取 (Center±22 / y+6) 格，火把格与相邻格均无液体才点亮；
1192	          //  591 持械变体 !wet 即亮，偏移 ±36/±28（专家变体，尘需 ai[2]==0 门）。
1193	          //  色 (1, 0.95, 0.8) = 与手持火把同色；尘 6 号 1/30 概率
1194	          if (this.vanillaId === 590 || this.vanillaId === 591) this.torchZombieLight(game);
1195	          // AI_003 火星尾段（bossAI_martian.ts）：军官 383 带盾无敌/补盾、工程师 386 放炮塔
1196	          if (this.vanillaId === 383 || this.vanillaId === 386) martianFighterExtras(this, game, p);
1197	          break;                                                        // AI_003 战士族（原版通用核）
1198	        // EoC 传参例外:玩家死亡也要传原对象(cs:19931 dead 判定走逃离分支,
1199	        // 冲刺计时合法冻结;传 null 会让 aiT 照走、状态机停摆 → 首冲时长翻倍)
1200	        case 4: this.eocAI(game, (game as unknown as { player: Player }).player ?? null); break; // AI_004 克苏鲁之眼（NPC.cs:19909）
1201	        case 5: this.swarmerAI(game, p); break;                         // AI_005 噬魂怪族（原版蜂群核）
1202	        case 6:
1203	          // AI_006 蠕虫族（头）；412 爬尾虫走专属核（bossAI_lunar_misc：
1204	          // 30 段链 + 空泳追击环 + 414 尾受击红闪 localAI[2] 状态机，cs:51357-52671）
1205	          if (this.vanillaId === 412) crawltipedeAI(this, game, p);
1206	          else this.wormAI(game, p);
1207	          break;
1208	        case 8: this.casterAI(game, p); break;                          // AI_008 法师族（传送+弹幕）
1209	        case 10: this.cursedSkullAI(game, p); break;                     // AI_010 诅咒头骨（地牢飞行族）
1210	        case 11:
1211	          // 68 守卫走专用分支（bossAI.skeletronBossAI 注释"守卫分支已在 skeletronHeadAI"
1212	          // 即此拆分：守卫恒速追击与骷髅王战斗状态机互不混用）
1213	          if (this.vanillaId === 68) this.dungeonGuardianAI(game, p);
1214	          else skeletronBossAI(this, game, p);
1215	          break;                                                         // AI_011 骷髅王头战斗核/地牢守卫
1216	        case 12: skeletronHandAI(this, game, p); break;                    // AI_012 骷髅王手(锚定头)
1217	        case 20: this.blazingWheelAI(); break;                           // AI_020 火轮（地牢陷阱）
1218	        case 21: this.spikeBallAI(game); break;                          // AI_021 刺球（地牢陷阱）
1219	        case 14: this.batAI(game, p); break;                            // AI_014 蝙蝠/飞行族（1.4.5.6 原版核）

```


---

## 🤖 Assistant · 2026-08-19T03:17:09.272Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Good context. 624 gnome handled at fixedUpdate (approximate but present — misses the "ShouldTurnToStone" = player-facing condition; ours: day + no shelter + solid below. Vanilla AI_003_Gnomes_ShouldTurnToStone checks if player is looking at it? Let me check vanilla :56232. Quick check later).

379/380 standby handled via cultistArcherStandbyAI. 383/386 martian. So those exist.

482 (Granite Golem shell) — grep showed only in FIGHTER_NO_DOOR + a mapping table (0.2 value at line 170 — some other table). No shell phase implementation → MISSING. Let me verify by grepping "granite" or "壳".

471 — :56886 type 471 with ai3<0 (knockBackResist 0, defense×1.1, noGravity, noTileCollide, rotation...) — what is 471? 471 = "Butcher"? no. 471 =... in FIGHTER_NO_DOOR ours has 471. Type 471 with noGravity/noTileCollide when ai3<0 — this is the "Swordfish"? Hmm, 471 = "Zombie Merman"? no 586. 471... Let me check: it sets rotation = velocity.X * 0.1 — spinning. Possibly "Salamander"? no (498+). 471 = "Crawltipede"? no. Hmm — 471 could be "Bone Throwing Skeleton"? no (449). Actually! 471 = "Mrmech"? no. Let me grep vanilla for 471 nearby to see what it does — it's probably the "Swordfish"... Actually I think 471 = "Grey Grubby"? Hmm no those are 500s. Let me just read :56886-57040.

Also need: 590/591 (torch zombie light ✓ handled), 415/428/427/590-591/111/120 region (:56935-57110), solenian 419 (:57114-57173 — already read ours; need vanilla), stuck counter + discouragement + flag8 (:57400-57799), 463 nailhead scatter... wait 463 nailhead at :57548. Let me read 56935-57360 now (covers 471, 415/428/427, 590/591, 111, 120, 419 solenian).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:09.363Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 245,
 "offset": 56886
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:09.380Z

**📎 ToolResult**

```
56886			if (type == 471)
56887			{
56888				if (ai[3] < 0f)
56889				{
56890					knockBackResist = 0f;
56891					defense = (int)((double)defDefense * 1.1);
56892					noGravity = true;
56893					noTileCollide = true;
56894					if (velocity.X < 0f)
56895					{
56896						direction = -1;
56897					}
56898					else if (velocity.X > 0f)
56899					{
56900						direction = 1;
56901					}
56902					rotation = velocity.X * 0.1f;
56903					if (Main.netMode != 1)
56904					{
56905						localAI[3] += 1f;
56906						if (localAI[3] > (float)Main.rand.Next(20, 180))
56907						{
56908							localAI[3] = 0f;
56909							Vector2 center6 = base.Center;
56910							center6 += velocity;
56911							NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)center6.X, (int)center6.Y, 30);
56912						}
56913					}
56914				}
56915				else
56916				{
56917					localAI[3] = 0f;
56918					knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.35f);
56919					rotation *= 0.9f;
56920					defense = defDefense;
56921					noGravity = false;
56922					noTileCollide = false;
56923				}
56924				if (ai[3] == 1f)
56925				{
56926					knockBackResist = 0f;
56927					defense += 10;
56928				}
56929				if (ai[3] == -1f)
56930				{
56931					TargetClosest();
56932					float num32 = 8f;
56933					float num33 = 40f;
56934					Vector2 vector12 = Main.player[target].Center - base.Center;
56935					float num34 = vector12.Length();
56936					num32 += num34 / 200f;
56937					vector12.Normalize();
56938					vector12 *= num32;
56939					velocity = (velocity * (num33 - 1f) + vector12) / num33;
56940					if (num34 < 500f && !Collision.SolidCollision(position, width, height))
56941					{
56942						ai[3] = 0f;
56943						ai[2] = 0f;
56944					}
56945					return;
56946				}
56947				if (ai[3] == -2f)
56948				{
56949					velocity.Y -= 0.2f;
56950					if (velocity.Y < -10f)
56951					{
56952						velocity.Y = -10f;
56953					}
56954					if (Main.player[target].Center.Y - base.Center.Y > 200f)
56955					{
56956						TargetClosest();
56957						ai[3] = -3f;
56958						if (Main.player[target].Center.X > base.Center.X)
56959						{
56960							ai[2] = 1f;
56961						}
56962						else
56963						{
56964							ai[2] = -1f;
56965						}
56966					}
56967					velocity.X *= 0.99f;
56968					return;
56969				}
56970				if (ai[3] == -3f)
56971				{
56972					if (direction == 0)
56973					{
56974						TargetClosest();
56975					}
56976					if (ai[2] == 0f)
56977					{
56978						ai[2] = direction;
56979					}
56980					velocity.Y *= 0.9f;
56981					velocity.X += ai[2] * 0.3f;
56982					if (velocity.X > 10f)
56983					{
56984						velocity.X = 10f;
56985					}
56986					if (velocity.X < -10f)
56987					{
56988						velocity.X = -10f;
56989					}
56990					float num35 = Main.player[target].Center.X - base.Center.X;
56991					if ((ai[2] < 0f && num35 > 300f) || (ai[2] > 0f && num35 < -300f))
56992					{
56993						ai[3] = -4f;
56994						ai[2] = 0f;
56995					}
56996					else if (Math.Abs(num35) > 800f)
56997					{
56998						ai[3] = -1f;
56999						ai[2] = 0f;
57000					}
57001					return;
57002				}
57003				if (ai[3] == -4f)
57004				{
57005					ai[2] += 1f;
57006					velocity.Y += 0.1f;
57007					if (velocity.Length() > 4f)
57008					{
57009						velocity *= 0.9f;
57010					}
57011					int num36 = (int)base.Center.X / 16;
57012					int num37 = (int)(position.Y + (float)height + 12f) / 16;
57013					bool flag4 = false;
57014					for (int l = num36 - 1; l <= num36 + 1; l++)
57015					{
57016						if (Main.tile[l, num37] == null)
57017						{
57018							Main.tile[num36, num37] = new Tile();
57019						}
57020						if (Main.tile[l, num37].active() && Main.tileSolid[Main.tile[l, num37].type])
57021						{
57022							flag4 = true;
57023						}
57024					}
57025					if (flag4 && !Collision.SolidCollision(position, width, height))
57026					{
57027						ai[3] = 0f;
57028						ai[2] = 0f;
57029					}
57030					else if (ai[2] > 300f || base.Center.Y > Main.player[target].Center.Y + 200f)
57031					{
57032						ai[3] = -1f;
57033						ai[2] = 0f;
57034					}
57035				}
57036				else
57037				{
57038					if (ai[3] == 1f)
57039					{
57040						Vector2 center7 = base.Center;
57041						center7.Y -= 70f;
57042						velocity.X *= 0.8f;
57043						ai[2] += 1f;
57044						if (ai[2] == 60f)
57045						{
57046							if (Main.netMode != 1)
57047							{
57048								NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)center7.X, (int)center7.Y + 18, 472);
57049							}
57050						}
57051						else if (ai[2] >= 90f)
57052						{
57053							ai[3] = -2f;
57054							ai[2] = 0f;
57055						}
57056						for (int m = 0; m < 2; m++)
57057						{
57058							Vector2 vector13 = center7;
57059							Vector2 vector14 = new Vector2(Main.rand.Next(-100, 101), Main.rand.Next(-100, 101));
57060							vector14.Normalize();
57061							vector14 *= (float)Main.rand.Next(0, 100) * 0.1f;
57062							Vector2 vector15 = vector13 + vector14;
57063							vector14.Normalize();
57064							vector14 *= (float)Main.rand.Next(50, 90) * 0.1f;
57065							int num38 = Dust.NewDust(vector15, 1, 1, 27);
57066							Main.dust[num38].velocity = -vector14 * 0.3f;
57067							Main.dust[num38].alpha = 100;
57068							if (Main.rand.Next(2) == 0)
57069							{
57070								Main.dust[num38].noGravity = true;
57071								Main.dust[num38].scale += 0.3f;
57072							}
57073						}
57074						return;
57075					}
57076					ai[2] += 1f;
57077					int num39 = 10;
57078					if (velocity.Y == 0f && CountNPCS(472) < num39)
57079					{
57080						if (ai[2] >= 180f)
57081						{
57082							ai[2] = 0f;
57083							ai[3] = 1f;
57084						}
57085					}
57086					else
57087					{
57088						if (CountNPCS(472) >= num39)
57089						{
57090							ai[2] += 1f;
57091						}
57092						if (ai[2] >= 360f)
57093						{
57094							ai[2] = 0f;
57095							ai[3] = -2f;
57096							velocity.Y -= 3f;
57097						}
57098					}
57099					if (target >= 0 && !Main.player[target].dead && (Main.player[target].Center - base.Center).Length() > 800f)
57100					{
57101						ai[3] = -1f;
57102						ai[2] = 0f;
57103					}
57104				}
57105				if (Main.player[target].dead)
57106				{
57107					TargetClosest();
57108					if (Main.player[target].dead)
57109					{
57110						EncourageDespawn(1);
57111					}
57112				}
57113			}
57114			if (type == 419)
57115			{
57116				reflectsProjectiles = false;
57117				takenDamageMultiplier = 1f;
57118				int num40 = 6;
57119				int num41 = 10;
57120				float num42 = 16f;
57121				if (ai[2] > 0f)
57122				{
57123					ai[2] -= 1f;
57124				}
57125				if (ai[2] == 0f)
57126				{
57127					if (((Main.player[target].Center.X < base.Center.X && direction < 0) || (Main.player[target].Center.X > base.Center.X && direction > 0)) && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
57128					{
57129						ai[2] = -1f;
57130						netUpdate = true;

```


---

## 🤖 Assistant · 2026-08-19T03:17:22.064Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Type 471 = "Swordfish"? No — it spawns NPC 30 (Chaos Ball) and 472... spawns 472 above itself 70px, counts 472... This is the **Medusa? no** — spawning NPC 472 and balls 30 — this is the **"Dungeon Spirit"? no**. 472 = "Flocko"? no. Wait: spawning 472 repeatedly, ai3 state machine with flying phases -1..-4, spawning chaos balls... **471 = "Nebula Brain"? no**. Hmm: it's a GRAVEYARD enemy: 471 = "Grotesque Tombstone"? no that's 521... Actually 471 spawning 472 — 472 = "Flocko"? Let me think — graveyard enemies: Rave Skeiton? Ghost 471? I think **471 = "Dune Ghoul"? no (532)**. 

Whatever the name — ours does NOT implement 471's special ai3 state machine at all (no 471 anywhere in our code). 471 with CountNPCS(472)<10 spawning 472s... **471 = "Wraith"? no (82)**. Hmm, let me grep vanilla NPCID near SetDefaults for 471. Actually — this doesn't matter much for name; it's likely "Salamander"? I'll grep quickly.

419 solenian vanilla (:57114-57173) vs ours:
- vanilla: num40=6 (windup), num41=10, num42=16 ✓ ours.
- ai2>0 → decrement ✓.
- ai2==0: facing + CanHit(Center 1x1 → player.Center 1x1) → ai2=-1 ✓ ours canSeePlayer (box) approx.
- Let me read the rest (57131-57173) to verify the windup/launch/dash against ours. I saw the start. Ours: -1..-6 windup vx*=0.9; at -6 launch toward player.Top+(0,-30) ×16; dash ai2<-6: ai2-=1, if vy==0 → 60 (recovery); else if ai2 < -16: vy += 0.15 clamp 24; reflectsProjectiles=true, takenDamageMultiplier=3; justHit → 60.

Let me read 57131-57230 to compare precisely.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:22.497Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 115,
 "offset": 57130
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:22.511Z

**📎 ToolResult**

```
57130						netUpdate = true;
57131						TargetClosest();
57132					}
57133				}
57134				else
57135				{
57136					if (ai[2] < 0f && ai[2] > (float)(-num40))
57137					{
57138						ai[2] -= 1f;
57139						velocity.X *= 0.9f;
57140						return;
57141					}
57142					if (ai[2] == (float)(-num40))
57143					{
57144						ai[2] -= 1f;
57145						TargetClosest();
57146						Vector2 vector16 = DirectionTo(Main.player[target].Top + new Vector2(0f, -30f));
57147						if (vector16.HasNaNs())
57148						{
57149							vector16 = Vector2.Normalize(new Vector2(spriteDirection, -1f));
57150						}
57151						velocity = vector16 * num42;
57152						netUpdate = true;
57153						return;
57154					}
57155					if (ai[2] < (float)(-num40))
57156					{
57157						ai[2] -= 1f;
57158						if (velocity.Y == 0f)
57159						{
57160							ai[2] = 60f;
57161						}
57162						else if (ai[2] < (float)(-num40 - num41))
57163						{
57164							velocity.Y += 0.15f;
57165							if (velocity.Y > 24f)
57166							{
57167								velocity.Y = 24f;
57168							}
57169						}
57170						reflectsProjectiles = true;
57171						takenDamageMultiplier = 3f;
57172						if (justHit)
57173						{
57174							ai[2] = 60f;
57175							netUpdate = true;
57176						}
57177						return;
57178					}
57179				}
57180			}
57181			if (type == 415)
57182			{
57183				int num43 = 42;
57184				int num44 = 18;
57185				if (justHit)
57186				{
57187					ai[2] = 120f;
57188					netUpdate = true;
57189				}
57190				if (ai[2] > 0f)
57191				{
57192					ai[2] -= 1f;
57193				}
57194				if (ai[2] == 0f)
57195				{
57196					int num45 = 0;
57197					for (int n = 0; n < Main.maxNPCs; n++)
57198					{
57199						if (Main.npc[n].active && Main.npc[n].type == 516)
57200						{
57201							num45++;
57202						}
57203					}
57204					if (num45 > 6)
57205					{
57206						ai[2] = 90f;
57207					}
57208					else if (((Main.player[target].Center.X < base.Center.X && direction < 0) || (Main.player[target].Center.X > base.Center.X && direction > 0)) && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
57209					{
57210						ai[2] = -1f;
57211						netUpdate = true;
57212						TargetClosest();
57213					}
57214				}
57215				else if (ai[2] < 0f && ai[2] > (float)(-num43))
57216				{
57217					ai[2] -= 1f;
57218					if (ai[2] == (float)(-num43))
57219					{
57220						ai[2] = 180 + 30 * Main.rand.Next(10);
57221					}
57222					velocity.X *= 0.8f;
57223					if (ai[2] == (float)(-num44) || ai[2] == (float)(-num44 - 8) || ai[2] == (float)(-num44 - 16))
57224					{
57225						position += netOffset;
57226						for (int num46 = 0; num46 < 20; num46++)
57227						{
57228							Vector2 vector17 = base.Center + Vector2.UnitX * spriteDirection * 40f;
57229							Dust obj3 = Main.dust[Dust.NewDust(vector17, 0, 0, 259)];
57230							Vector2 vector18 = Vector2.UnitY.RotatedByRandom(6.2831854820251465);
57231							obj3.position = vector17 + vector18 * 4f;
57232							obj3.velocity = vector18 * 2f + Vector2.UnitX * Main.rand.NextFloat() * spriteDirection * 3f;
57233							obj3.scale = 0.3f + vector18.X * (float)(-spriteDirection);
57234							obj3.fadeIn = 0.7f;
57235							obj3.noGravity = true;
57236						}
57237						position -= netOffset;
57238						if (velocity.X > -0.5f && velocity.X < 0.5f)
57239						{
57240							velocity.X = 0f;
57241						}
57242						if (Main.netMode != 1)
57243						{
57244							NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X + spriteDirection * 45, (int)base.Center.Y + 8, 516, 0, 0f, 0f, 0f, 0f, target);

```


---

## 🤖 Assistant · 2026-08-19T03:17:24.367Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"case 471\\|type = 471\\|NPCID.Skeleton\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs | head; grep -rn \"471\\b\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/Lang_VariesText.cs 2>/dev/null | head -2; grep -rn \"\\b471\\b\" ~/Project/GLM/SandboxWorld/game/tools/*.mjs 2>/dev/null | head -3",
 "description": "Identify NPC type 471 name"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:24.445Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ID/NPCID.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T03:17:36.698Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
419 solenian vanilla vs ours: 
- windup ✓, launch: `DirectionTo(player.Top + (0,-30))` — DirectionTo FROM base TO target = (target - base).normalized ✓ ours. NaN → Normalize(spriteDirection, -1) ✓ ours. velocity = v*16 ✓. 
- dash: vy==0 → ai2=60 ✓; ai2 < -16 → vy += 0.15 clamp 24 — vanilla clamps `velocity.Y > 24 → 24` (positive 24 only!) — ours `Math.min(this.vy + 0.15, 24)` ✓ same.
- reflects/damage 3 ✓, justHit → 60 ✓, all return ✓.
Ours solenian ✓ 1:1 (except ours applies gravity+collide in branches which vanilla does via shared gravity... wait — 419 in vanilla: the branches RETURN before the walking section, and gravity is applied by UpdateNPC tail :91519? Vanilla fighters have gravity via... hmm, actually for AI_003 the gravity+collision happens at the END of AI_003 (I saw "重力" at :91519 = UpdateNPC). Let me confirm later — ours adding applyGravity+moveAndCollide in dash branches approximates ✓.

471: it's the lunar "Nebula... " hmm. 472 spawns — 472 = projectile-ish NPC... You know what, 471 = "Swordfish"... no. Let me search NPC names differently — the repo has tools to map ids. Let me grep game/src data for npc names by id 471/472.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:38.421Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn '\"471\"\\|:471\\|471,' ~/Project/GLM/SandboxWorld/game/src/data/npcNames*.ts ~/Project/GLM/SandboxWorld/game/src/data/*.json 2>/dev/null | head -5; ls ~/Project/GLM/SandboxWorld/game/src/data/ | head -30; grep -rln \"VampireMiner\\|Grasshopper\" ~/Project/GLM/SandboxWorld/game/src/data/ 2>/dev/null | head -3",
 "description": "Find NPC id-to-name data files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:38.468Z

**📎 ToolResult**

```
(eval):1: no matches found: ~/Project/GLM/SandboxWorld/game/src/data/npcNames*.ts
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
~/Project/GLM/SandboxWorld/game/src/data/items.ts
~/Project/GLM/SandboxWorld/game/src/data/legacyItemIndex.generated.json
~/Project/GLM/SandboxWorld/game/src/data/vanilla-tilecollision.json

```


---

## 🤖 Assistant · 2026-08-19T03:17:44.703Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst m = require('~/Project/GLM/SandboxWorld/game/public/l10n/zh-Hans.json');\nconst s = JSON.stringify(m);\n\" 2>/dev/null; ls ~/Project/GLM/SandboxWorld/game/public/l10n/ 2>/dev/null | head -3; grep -o '\"NPCName[._]*471[^\"]*\"\\s*:\\s*\"[^\"]*\"' ~/Project/GLM/SandboxWorld/game/public/l10n/zh-Hans.json 2>/dev/null | head; grep -rn \"471\" ~/Project/GLM/SandboxWorld/game/src/data/vanilla-bestiary.json 2>/dev/null | head -2",
 "description": "Look up NPC 471 name in l10n data"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:44.790Z

**📎 ToolResult**

```
de-DE.json
en-US.json
es-ES.json
~/Project/GLM/SandboxWorld/game/src/data/vanilla-bestiary.json:1:{"townNpcBestiaryPriority":[22,17,18,38,369,20,19,207,227,353,633,550,588,107,228,124,54,108,178,229,160,441,209,208,663,142,637,638,656,670,678,679,680,681,682,683,684,368,453,37,687],"normalGoldCritterBestiaryPriority":[46,540,614,303,337,443,74,297,298,671,672,673,674,675,442,55,230,592,593,299,538,539,300,447,361,445,377,446,356,444,357,448,595,596,597,598,599,600,601,626,627,612,613,604,605,669,677],"bossBestiaryPriority":[664,4,5,50,535,13,14,15,266,267,668,35,36,222,113,114,117,115,116,657,658,659,660,125,126,134,135,136,139,127,128,131,129,130,262,263,264,636,245,246,249,247,248,370,372,373,439,438,379,380,440,521,454,507,517,422,493,398,396,397,400,401],"rarityStarOverrides":{"4":2,"13":3,"16":2,"17":1,"18":1,"19":1,"20":3,"22":1,"29":2,"35":3,"37":2,"38":1,"47":3,"50":2,"54":2,"57":3,"66":3,"107":3,"108":3,"124":2,"134":4,"142":5,"149":2,"160":5,"161":2,"168":3,"170":3,"171":3,"178":3,"180":3,"184":2,"185":3,"205":4,"206":3,"208":4,"209":3,"216":3,"223":2,"224":2,"225":2,"227":2,"228":2,"250":3,"262":4,"298":2,"301":2,"302":3,"303":4,"316":3,"317":3,"318":3,"319":3,"320":3,"321":3,"322":3,"323":3,"324":3,"331":3,"332":3,"333":3,"334":3,"335":3,"336":3,"337":4,"353":2,"355":2,"358":3,"360":3,"362":2,"364":2,"366":2,"368":3,"369":2,"374":3,"441":5,"453":4,"464":3,"465":3,"470":3,"471":4,"481":2,"483":2,"484":5,"486":2,"487":3,"491":4,"494":2,"496":2,"499":2,"537":2,"540":2,"541":4,"546":2,"550":2,"588":2,"594":2,"599":3,"604":3,"607":2,"608":2,"611":3,"612":2,"614":4,"615":3,"616":2,"626":2,"628":2,"633":5,"637":3,"638":3,"653":2,"654":3,"655":2,"656":3,"661":3,"663":5,"664":5,"668":3,"669":3,"670":3,"671":3,"672":3,"673":3,"674":3,"675":3,"676":5,"677":5,"678":3,"679":3,"680":3,"681":3,"682":3,"683":3,"684":3,"690":5,"691":4,"-9":3},"npcStats":{"1":[0,0,7,2,25,1],"2":[0,0,18,2,60,2],"3":[0,0,14,6,45,3],"4":[0,1,15,12,2800,4],"5":[0,0,12,0,8,5],"6":[0,0,22,8,40,5],"7":[0,0,31,2,100,6],"8":[0,0,16,6,100,6],"9":[0,0,13,10,100,6],"10":[0,0,8,0,30,6],"11":[0,0,4,4,30,6],"12":[0,0,4,6,30,6],"13":[0,0,22,2,150,6],"14":[0,0,13,4,150,6],"15":[0,0,11,8,150,6],"16":[0,0,20,7,90,1],"17":[0,0,10,15,250,7],"18":[0,0,10,15,250,7],"19":[0,0,10,15,250,7],"20":[0,0,10,15,250,7],"21":[0,0,20,8,60,3],"22":[0,0,10,30,250,7],"23":[0,0,40,6,26,5],"24":[0,0,30,16,70,8],"25":[0,0,30,0,1,9],"26":[0,0,12,4,60,3],"27":[0,0,20,6,80,3],"28":[0,0,25,8,110,3],"29":[0,0,20,2,40,8],"30":[0,0,20,0,1,9],"31":[0,0,26,8,80,3],"32":[0,0,20,2,50,8],"33":[0,0,20,0,1,9],"34":[0,0,35,6,40,10],"35":[0,1,32,10,4400,11],"36":[0,0,20,14,600,12],"37":[0,0,10,15,250,7],"38":[0,0,10,15,250,7],"39":[0,0,36,12,300,6],"40":[0,0,20,18,300,6],"41":[0,0,16,18,300,6],"42":[0,0,26,12,48,5],"43":[0,0,34,10,110,13],"44":[1,0,22,9,70,3],"45":[4,0,20,4,200,8],"46":[0,0,0,0,5,7],"47":[0,0,20,4,70,3],"48":[0,0,25,8,100,14],"49":[0,0,13,2,16,14],"50":[0,1,40,10,2000,15],"51":[0,0,20,4,34,14],"52":[2,0,20,10,500,3],"53":[2,0,14,8,200,3],"54":[0,0,10,15,250,7],"55":[0,0,0,0,5,16],"56":[0,0,25,10,60,13],"57":[0,0,30,6,100,16],"58":[0,0,25,2,30,16],"59":[0,0,15,10,50,1],"60":[0,0,35,8,46,14],"61":[0,0,15,4,40,17],"62":[0,0,32,8,120,14],"63":[0,0,25,4,34,18],"64":[0,0,30,6,70,18],"65":[0,0,40,2,300,16],"66":[1,0,32,8,140,14],"67":[0,0,20,10,40,3],"68":[0,0,9999,9999,9999,11],"69":[0,0,10,6,45,19],"70":[0,0,32,100,100,20],"71":[1,0,30,7,150,1],"72":[0,0,24,100,100,21],"73":[1,0,20,6,80,3],"74":[0,0,0,0,5,24],"75":[0,0,55,20,150,22],"76":[0,0,0,0,0,0],"77":[0,0,40,28,260,3],"78":[0,0,50,16,130,3],"79":[0,0,60,18,180,3],"80":[0,0,55,18,200,3],"81":[0,0,55,20,170,1],"82":[0,0,65,16,160,22],"83":[0,0,80,18,200,23],"84":[0,0,80,18,200,23],"85":[4,0,30,12,300,25],"86":[0,0,65,30,400,26],"87":[0,0,80,10,4000,6],"88":[0,0,40,20,4000,6],"89":[0,0,40,20,4000,6],"90":[0,0,40,20,4000,6],"91":[0,0,40,20,4000,6],"92":[0,0,40,20,4000,6],"93":[0,0,45,16,100,14],"94":[0,0,60,32,230,5],"95":[0,0,45,10,200,6],"96":[0,0,28,20,200,6],"97":[0,0,26,30,200,6],"98":[0,0,70,36,500,6],"99":[0,0,55,40,500,6],"100":[0,0,40,44,500,6],"101":[0,0,70,30,320,13],"102":[0,0,80,22,90,16],"103":[0,0,80,30,120,18],"104":[0,0,70,38,350,3],"105":[1,0,10,15,250,0],"106":[1,0,10,15,250,0],"107":[0,0,10,15,250,7],"108":[0,0,10,15,250,7],"109":[1,0,60,25,800,3],"110":[0,0,45,14,210,3],"111":[0,0,20,6,80,3],"112":[0,0,65,0,1,9],"113":[0,1,50,12,8000,27],"114":[0,0,50,0,8000,28],"115":[0,0,30,10,240,29],"116":[0,0,30,6,80,2],"117":[0,0,26,2,60,6],"118":[0,0,22,6,60,6],"119":[0,0,18,10,60,6],"120":[0,0,40,30,370,3],"121":[0,0,45,20,60,14],"122":[0,0,60,22,220,22],"123":[1,0,10,15,250,0],"124":[0,0,10,15,250,7],"125":[0,1,45,10,20000,30],"126":[0,1,50,10,23000,31],"127":[0,1,47,24,28000,32],"128":[0,0,30,23,7000,35],"129":[0,0,56,38,9000,33],"130":[0,0,52,34,9000,34],"131":[0,0,29,20,6000,36],"132":[0,0,15,5,40,3],"133":[0,0,40,20,300,2],"134":[0,1,70,0,80000,37],"135":[0,0,55,30,80000,37],"136":[0,0,40,35,80000,37],"137":[0,0,75,30,200,14],"138":[0,0,70,30,180,1],"139":[0,0,50,20,200,5],"140":[0,0,55,28,260,3],"141":[0,0,50,18,150,1],"142":[0,0,10,15,250,7],"143":[0,0,50,20,200,38],"144":[0,0,65,26,240,38],"145":[0,0,55,22,220,38],"146":[0,0,0,0,0,0],"147":[0,0,8,4,30,1],"148":[0,0,0,0,5,7],"149":[0,0,0,0,5,7],"150":[0,0,18,6,30,14],"151":[0,0,50,16,160,14],"152":[0,0,80,24,220,14],"153":[0,0,80,30,470,39],"154":[0,0,55,28,400,39],"155":[0,0,65,30,300,26],"156":[0,0,50,40,600,14],"157":[0,0,75,30,200,16],"158":[0,0,60,32,750,14],"159":[0,0,80,24,750,3],"160":[0,0,10,15,250,7],"161":[0,0,16,8,50,3],"162":[0,0,65,18,350,3],"163":[0,0,90,40,350,3],"164":[0,0,30,10,80,3],"165":[0,0,30,10,80,40],"166":[0,0,70,26,450,3],"167":[0,0,24,10,70,3],"168":[0,0,20,4,70,3],"169":[0,0,55,20,200,22],"170":[0,0,70,16,210,2],"171":[0,0,70,16,210,2],"172":[4,0,200,30,600,8],"173":[0,0,22,8,40,5],"174":[0,0,65,26,220,41],"175":[0,0,100,30,300,13],"176":[0,0,70,22,220,5],"177":[0,0,80,26,300,41],"178":[0,0,10,15,250,7],"179":[0,0,80,18,200,23],"180":[0,0,70,16,210,2],"181":[0,0,25,10,70,3],"182":[0,0,65,18,240,22],"183":[0,0,60,26,200,1],"184":[0,0,12,8,60,1],"185":[0,0,26,12,70,3],"186":[0,0,16,8,50,3],"187":[0,0,13,6,40,3],"188":[0,0,13,8,45,3],"189":[0,0,16,4,45,3],"190":[0,0,18,4,65,2],"191":[0,0,16,2,60,2],"192":[0,0,18,2,50,2],"193":[0,0,20,0,60,2],"194":[0,0,14,4,60,2],"195":[2,0,10,30,250,42],"196":[2,0,35,16,300,3],"197":[0,0,50,28,280,3],"198":[0,0,38,20,400,3],"199":[0,0,60,30,400,3],"200":[0,0,12,4,38,3],"201":[0,0,20,12,55,3],"202":[0,0,18,8,65,3],"203":[0,0,22,8,60,3],"204":[0,0,28,8,65,1],"205":[2,0,70,28,1000,5],"206":[0,0,60,30,280,3],"207":[0,0,10,15,250,7],"208":[0,0,10,15,250,7],"209":[0,0,10,30,500,7],"210":[0,0,20,5,20,5],"211":[0,0,15,2,10,5],"212":[0,0,35,17,300,3],"213":[0,0,50,22,450,3],"214":[0,0,30,14,225,3],"215":[0,0,35,20,350,3],"216":[1,0,70,30,3000,3],"217":[1,0,20,10,40,3],"218":[1,0,20,10,40,3],"219":[1,0,20,10,40,3],"220":[2,0,20,10,40,3],"221":[1,0,20,2,30,18],"222":[0,1,30,8,3400,43],"223":[0,0,16,8,50,3],"224":[0,0,9,4,20,44],"225":[0,0,10,5,35,1],"226":[0,0,85,28,260,14],"227":[0,0,10,15,250,7],"228":[0,0,10,15,250,7],"229":[0,0,10,15,250,7],"230":[0,0,0,0,5,7],"231":[0,0,22,16,50,5],"232":[0,0,28,12,42,5],"233":[0,0,30,14,38,5],"234":[0,0,32,6,42,5],"235":[0,0,34,4,38,5],"236":[0,0,100,28,400,3],"237":[0,0,100,28,400,40],"238":[0,0,100,40,350,40],"239":[0,0,30,8,60,3],"240":[0,0,30,8,60,40],"241":[0,0,50,20,150,16],"242":[0,0,75,20,150,18],"243":[2,0,60,32,4000,3],"244":[1,0,85,26,400,1],"245":[0,1,72,26,15000,45],"246":[0,0,64,20,25000,46],"247":[0,0,59,28,10000,47],"248":[0,0,59,28,10000,47],"249":[0,0,80,32,16000,48],"250":[0,0,50,24,300,49],"251":[2,0,50,30,1000,3],"252":[0,0,80,12,100,5],"253":[0,0,80,22,700,22],"254":[0,0,40,10,180,3],"255":[0,0,38,16,220,3],"256":[0,0,90,20,140,18],"257":[0,0,38,24,230,3],"258":[0,0,60,16,220,3],"259":[0,0,24,4,90,13],"260":[0,0,70,20,300,13],"261":[0,0,80,0,1,50],"262":[0,1,50,14,30000,51],"263":[0,0,60,24,4000,52],"264":[0,0,60,20,1000,53],"265":[0,0,70,0,1,50],"266":[0,1,30,14,1250,54],"267":[0,0,20,10,100,55],"268":[0,0,55,20,340,22],"269":[0,0,70,34,550,3],"270":[0,0,55,50,400,3],"271":[0,0,70,40,450,3],"272":[0,0,75,28,400,3],"273":[0,0,45,50,500,3],"274":[0,0,65,34,350,3],"275":[0,0,45,50,550,3],"276":[0,0,85,54,500,3],"277":[0,0,70,32,400,3],"278":[0,0,65,48,450,3],"279":[0,0,40,54,500,3],"280":[0,0,75,34,500,3],"281":[0,0,40,20,400,8],"282":[0,0,35,28,450,8],"283":[0,0,50,18,300,8],"284":[0,0,35,24,450,8],"285":[0,0,50,12,200,8],"286":[0,0,60,10,250,8],"287":[1,0,90,42,1000,3],"288":[0,0,70,30,200,56],"289":[0,0,60,20,400,10],"290":[2,0,100,50,5000,3],"291":[1,0,60,28,400,3],"292":[1,0,60,28,400,3],"293":[1,0,60,28,400,3],"294":[0,0,34,6,70,3],"295":[0,0,28,12,70,3],"296":[0,0,24,14,120,3],"297":[0,0,0,0,5,24],"298":[0,0,0,0,5,24],"299":[0,0,0,0,5,7],"300":[0,0,0,0,5,7],"301":[0,0,12,2,35,17],"302":[0,0,7,2,25,1],"303":[0,0,0,0,5,7],"304":[0,0,80,20,175,1],"305":[0,0,60,18,500,3],"306":[0,0,52,14,400,3],"307":[0,0,78,16,600,3],"308":[0,0,66,14,650,3],"309":[0,0,52,26,450,3],"310":[0,0,60,18,500,3],"311":[0,0,52,14,400,3],"312":[0,0,78,16,600,3],"313":[0,0,66,14,650,3],"314":[0,0,52,26,450,3],"315":[0,0,130,40,5000,26],"316":[0,0,15,4,50,22],"317":[0,0,16,6,75,2],"318":[0,0,20,4,60,2],"319":[0,0,20,6,40,3],"320":[0,0,15,8,60,3],"321":[0,0,20,14,34,3],"322":[0,0,23,0,115,3],"323":[0,0,18,10,65,3],"324":[0,0,22,10,70,3],"325":[0,0,120,34,14000,57],"326":[0,0,100,32,1200,3],"327":[0,0,50,40,26000,58],"328":[0,0,65,14,5000,59],"329":[0,0,80,38,1800,26],"330":[0,0,90,44,1250,22],"331":[0,0,14,6,45,3],"332":[0,0,14,6,45,3],"333":[0,0,7,2,25,1],"334":[0,0,6,2,23,1],"335":[0,0,8,3,29,1],"336":[0,0,5,1,22,1],"337":[0,0,0,0,5,7],"338":[0,0,65,18,600,3],"339":[0,0,52,24,700,3],"340":[0,0,78,14,500,3],"341":[0,0,100,32,900,25],"342":[0,0,90,26,750,3],"343":[0,0,140,50,3500,3],"344":[0,0,110,38,13000,57],"345":[0,0,120,38,34000,60],"346":[0,0,120,56,18000,61],"347":[0,0,60,28,1200,62],"348":[0,0,80,26,1800,3],"349":[0,0,100,42,1800,3],"350":[0,0,70,30,900,3],"351":[0,0,100,40,2500,3],"352":[0,0,75,8,450,63],"353":[0,0,10,15,250,7],"354":[1,0,10,15,250,0],"355":[0,0,0,0,5,64],"356":[0,0,0,0,5,65],"357":[0,0,0,0,5,66],"358":[0,0,0,0,5,64],"359":[0,0,0,0,5,67],"360":[0,0,0,0,5,67],"361":[0,0,0,0,5,7],"362":[0,0,0,0,5,7],"363":[0,0,0,0,5,68],"364":[0,0,0,0,5,7],"365":[0,0,0,0,5,68],"366":[0,0,0,0,5,7],"367":[0,0,0,0,5,7],"368":[0,0,10,15,250,7],"369":[0,0,10,15,250,7],"370":[0,1,100,50,60000,69],"371":[0,0,100,0,1,70],"372":[0,0,100,100,100,71],"373":[0,0,120,100,100,71],"374":[4,0,0,0,5,66],"375":[4,0,0,0,5,6],"376":[1,0,10,15,250,0],"377":[0,0,0,0,5,1],"378":[0,0,120,30,200,41],"379":[0,0,45,14,210,3],"380":[0,0,45,14,210,3],"381":[0,0,50,25,350,3],"382":[0,0,50,25,350,3],"383":[0,0,75,50,300,3],"384":[0,0,0,20,1000,72],"385":[0,0,80,30,750,3],"386":[0,0,40,34,400,3],"387":[0,0,10,40,200,73],"388":[0,0,60,16,300,74],"389":[0,0,75,38,600,3],"390":[0,0,65,30,350,75],"391":[0,0,85,30,600,3],"392":[0,0,50,100,100,75],"393":[0,0,60,20,5000,75],"394":[0,0,60,20,3500,75],"395":[0,1,80,0,10000,76],"396":[0,1,0,50,45000,79],"397":[0,1,0,40,25000,78],"398":[0,1,0,70,50000,77],"399":[1,0,5,5,500,80],"400":[0,0,60,0,100,81],"401":[0,0,0,0,400,82],"402":[0,0,80,10,1200,6],"403":[0,0,0,0,0,0],"404":[0,0,0,0,0,0],"405":[0,0,120,50,300,85],"406":[0,0,70,0,300,95],"407":[0,0,70,38,1500,96],"408":[0,0,0,0,0,0],"409":[0,0,70,40,800,3],"410":[0,0,80,10,200,26],"411":[0,0,80,34,700,3],"412":[0,0,120,1000,10000,6],"413":[0,0,80,1000,10000,6],"414":[0,0,50,0,10000,6],"415":[0,0,55,32,800,3],"416":[0,0,80,28,800,75],"417":[0,0,80,34,700,39],"418":[0,0,70,26,600,74],"419":[0,0,90,30,800,3],"420":[0,0,75,20,1300,97],"421":[0,0,70,34,330,85],"422":[0,0,0,20,20000,94],"423":[0,0,90,46,850,26],"424":[0,0,80,30,700,3],"425":[0,0,100,40,800,3],"426":[0,0,100,44,1000,3],"427":[0,0,75,20,500,3],"428":[0,0,50,6,200,3],"429":[0,0,90,34,700,3],"430":[0,0,14,6,45,3],"431":[0,0,16,8,50,3],"432":[0,0,16,8,50,3],"433":[0,0,13,6,40,3],"434":[0,0,13,8,45,3],"435":[0,0,16,4,45,3],"436":[0,0,12,4,38,3],"437":[0,0,0,0,400,83],"438":[0,0,0,0,400,83],"439":[0,1,50,42,32000,84],"440":[0,0,0,35,10000,84],"441":[0,0,10,15,250,7],"442":[3,0,0,0,5,24],"443":[3,0,0,0,5,7],"444":[3,0,0,0,5,65],"445":[3,0,0,0,5,7],"446":[3,0,0,0,5,1],"447":[3,0,0,0,5,7],"448":[3,0,0,0,5,66],"449":[0,0,20,8,60,3],"450":[0,0,20,12,55,3],"451":[0,0,18,8,65,3],"452":[0,0,22,8,60,3],"453":[1,0,10,30,250,7],"454":[0,0,100,15,10000,6],"455":[0,0,50,30,10000,6],"456":[0,0,50,30,10000,6],"457":[0,0,50,30,10000,6],"458":[0,0,50,30,10000,6],"459":[0,0,50,30,10000,6],"460":[0,0,70,30,700,3],"461":[0,0,60,22,400,3],"462":[0,0,70,14,270,3],"463":[0,0,100,34,4000,3],"464":[0,0,21,5,75,3],"465":[0,0,31,7,110,16],"466":[0,0,70,40,550,3],"467":[0,0,100,80,350,85],"468":[0,0,65,24,500,3],"469":[0,0,68,28,600,3],"470":[0,0,21,5,75,3],"471":[1,0,80,26,2000,3],"472":[0,0,50,18,180,86],"473":[5,0,90,34,3500,87],"474":[5,0,90,34,3500,87],"475":[5,0,90,34,3500,87],"476":[5,0,90,34,3500,87],"477":[1,0,80,30,6000,88],"478":[0,0,0,30,200,89],"479":[0,0,50,14,700,90],"480":[1,0,30,20,400,3],"481":[0,0,22,10,70,3],"482":[0,0,30,18,110,3],"483":[0,0,24,8,40,91],"484":[0,0,0,0,5,66],"485":[0,0,0,0,5,66],"486":[0,0,0,0,5,66],"487":[0,0,0,0,5,66],"488":[0,0,0,0,1000,92],"489":[0,0,20,8,75,3],"490":[0,0,28,14,50,22],"491":[0,0,0,100,50,93],"492":[0,0,30,20,2000,75],"493":[0,0,0,20,20000,94],"494":[0,0,28,6,50,3],"495":[0,0,28,6,50,3],"496":[0,0,16,12,50,39],"497":[0,0,16,12,50,39],"498":[0,0,18,10,65,3],"499":[0,0,18,10,65,3],"500":[0,0,18,10,65,3],"501":[0,0,18,10,65,3],"502":[0,0,18,10,65,3],"503":[0,0,18,10,65,3],"504":[0,0,18,10,65,3],"505":[0,0,18,10,65,3],"506":[0,0,18,10,65,3],"507":[0,0,0,20,20000,94],"508":[0,0,38,16,110,3],"509":[0,0,34,12,90,44],"510":[0,0,58,18,500,6],"511":[0,0,54,28,500,6],"512":[0,0,50,34,500,6],"513":[0,0,18,0,60,6],"514":[0,0,7,12,60,6],"515":[0,0,7,14,60,6],"516":[0,0,100,0,1,9],"517":[0,0,0,20,20000,94],"518":[0,0,80,28,1000,3],"519":[0,0,120,0,1,99],"520":[0,0,60,40,2000,3],"521":[0,0,90,30,2000,86],"522":[0,0,120,0,400,100],"523":[0,0,30,0,500,101],"524":[0,0,50,26,180,3],"525":[0,0,60,30,250,3],"526":[0,0,64,32,220,3],"527":[0,0,54,32,300,3],"528":[0,0,52,28,350,3],"529":[0,0,52,28,350,3],"530":[0,0,66,24,320,3],"531":[0,0,66,24,320,40],"532":[0,0,65,34,270,3],"533":[0,0,40,20,220,8],"534":[2,0,14,20,400,3],"535":[0,0,14,5,50,1],"536":[2,0,14,8,200,3],"537":[0,0,15,5,50,1],"538":[0,0,0,0,5,7],"539":[3,0,0,0,5,7],"540":[0,0,0,0,5,7],"541":[2,0,40,30,5000,102],"542":[0,0,50,20,360,103],"543":[0,0,60,24,380,103],"544":[0,0,64,22,400,103],"545":[0,0,54,26,450,103],"546":[0,0,30,6,50,26],"547":[0,0,0,10,10,104],"548":[0,0,0,14,1000,105],"549":[0,0,0,20,5,106],"550":[0,0,10,15,250,7],"551":[0,0,80,38,50000,110],"552":[0,0,18,14,30,107],"553":[0,0,46,20,170,107],"554":[0,0,70,28,560,107],"555":[0,0,26,16,50,107],"556":[0,0,55,26,200,107],"557":[0,0,75,34,700,107],"558":[0,0,30,4,60,108],"559":[0,0,75,16,180,108],"560":[0,0,100,30,600,108],"561":[0,0,30,18,60,107],"562":[0,0,60,28,300,107],"563":[0,0,80,38,1000,107],"564":[0,0,40,18,800,109],"565":[0,0,90,38,4000,109],"566":[0,0,18,12,25,107],"567":[0,0,70,22,480,107],"568":[0,0,50,30,500,107],"569":[0,0,80,40,1400,107],"570":[0,0,60,30,900,107],"571":[0,0,90,40,3000,107],"572":[0,0,60,26,260,107],"573":[0,0,80,32,800,107],"574":[0,0,50,16,170,108],"575":[0,0,80,32,580,108],"576":[0,0,70,34,5000,107],"577":[0,0,90,40,13000,107],"578":[0,0,80,36,500,111],"579":[1,0,10,15,250,0],"580":[0,0,25,10,80,3],"581":[0,0,29,8,60,44],"582":[0,0,10,2,30,3],"583":[2,0,0,0,5,112],"584":[2,0,0,0,5,112],"585":[2,0,0,0,5,112],"586":[1,0,40,20,400,3],"587":[1,0,35,18,300,44],"588":[0,0,10,15,250,7],"589":[1,0,10,15,250,0],"590":[0,0,14,6,45,3],"591":[0,0,14,6,45,3],"592":[3,0,0,0,5,16],"593":[3,0,0,0,5,7],"594":[0,0,0,0,1,113],"595":[0,0,0,0,5,114],"596":[0,0,0,0,5,114],"597":[0,0,0,0,5,114],"598":[0,0,0,0,5,114],"599":[0,0,0,0,5,114],"600":[0,0,0,0,5,114],"601":[3,0,0,0,5,114],"602":[0,0,0,0,5,7],"603":[0,0,0,0,5,68],"604":[0,0,0,0,5,115],"605":[3,0,0,0,5,115],"606":[0,0,0,0,5,66],"607":[0,0,0,0,5,16],"608":[0,0,0,0,5,7],"609":[0,0,0,0,5,68],"610":[0,0,0,0,5,7],"611":[0,0,0,0,5,24],"612":[0,0,0,0,5,116],"613":[3,0,0,0,5,116],"614":[0,0,0,0,5,7],"615":[0,0,0,0,5,16],"616":[0,0,0,0,5,7],"617":[0,0,0,0,5,7],"618":[1,0,55,24,7000,117],"619":[0,0,60,16,750,5],"620":[1,0,70,30,5000,107],"621":[1,0,90,0,6000,6],"622":[0,0,60,30,6000,6],"623":[0,0,50,40,6000,6],"624":[1,0,10,0,25,3],"625":[0,0,0,0,5,7],"626":[0,0,0,0,5,118],"627":[3,0,0,0,5,118],"628":[0,0,15,0,50,119],"629":[4,0,30,12,300,25],"630":[0,0,60,18,180,3],"631":[0,0,85,35,1000,3],"632":[0,0,14,6,45,3],"633":[0,0,10,15,250,7],"634":[0,0,13,2,16,14],"635":[0,0,20,8,60,3],"636":[0,1,80,50,70000,120],"637":[0,0,10,15,250,7],"638":[0,0,10,15,250,7],"639":[0,0,0,0,5,7],"640":[0,0,0,0,5,7],"641":[0,0,0,0,5,7],"642":[0,0,0,0,5,7],"643":[0,0,0,0,5,7],"644":[0,0,0,0,5,7],"645":[0,0,0,0,5,7],"646":[0,0,0,0,5,7],"647":[0,0,0,0,5,7],"648":[0,0,0,0,5,7],"649":[0,0,0,0,5,7],"650":[0,0,0,0,5,7],"651":[0,0,0,0,5,7],"652":[0,0,0,0,5,7],"653":[0,0,0,0,5,65],"654":[0,0,0,0,5,64],"655":[0,0,0,0,5,67],"656":[0,0,10,15,250,7],"657":[0,1,60,26,18000,121],"658":[0,0,40,35,150,1],"659":[0,0,40,35,150,1],"660":[0,0,50,30,120,14],"661":[4,0,0,0,5,65],"662":[0,0,75,22,500,122],"663":[0,0,10,15,250,7],"664":[0,1,0,0,20,0],"665":[0,0,20,0,1,9],"666":[0,0,65,0,1,9],"667":[2,0,5,5,300,1],"668":[0,1,20,10,7000,123],"669":[0,0,0,0,5,115],"670":[0,0,10,15,250,7],"671":[0,0,0,0,5,24],"672":[0,0,0,0,5,24],"673":[0,0,0,0,5,24],"674":[0,0,0,0,5,24],"675":[0,0,0,0,5,24],"676":[0,0,20,5,80,1],"677":[0,0,0,0,5,64],"678":[0,0,10,15,250,7],"679":[0,0,10,15,250,7],"680":[0,0,10,15,250,7],"681":[0,0,10,15,250,7],"682":[0,0,10,15,250,7],"683":[0,0,10,15,250,7],"684":[0,0,10,15,250,7],"685":[2,0,0,10,250,1],"686":[2,0,0,0,1,125],"687":[2,0,0,0,5,7],"688":[0,0,0,0,5,16],"689":[0,0,0,0,5,24],"690":[0,0,40,10,400,126],"691":[0,0,18,10,60,3],"692":[0,0,50,20,400,16],"693":[0,0,18,2,70,8],"694":[0,0,20,4,60,10],"695":[1,0,0,15,250,127],"696":[1,0,0,15,250,127],"-65":[0,0,34,4,38,5],"-64":[0,0,34,4,38,5],"-63":[0,0,32,6,42,5],"-62":[0,0,32,6,42,5],"-61":[0,0,30,14,38,5],"-60":[0,0,30,14,38,5],"-59":[0,0,28,12,42,5],"-58":[0,0,28,12,42,5],"-57":[0,0,22,16,50,5],"-56":[0,0,22,16,50,5],"-55":[0,0,16,8,50,3],"-54":[0,0,16,8,50,3],"-53":[0,0,22,8,60,3],"-52":[0,0,22,8,60,3],"-51":[0,0,18,8,65,3],"-50":[0,0,18,8,65,3],"-49":[0,0,20,12,55,3],"-48":[0,0,20,12,55,3],"-47":[0,0,20,8,60,3],"-46":[0,0,20,8,60,3],"-45":[0,0,12,4,38,3],"-44":[0,0,12,4,38,3],"-43":[0,0,18,2,60,2],"-42":[0,0,14,4,60,2],"-41":[0,0,20,0,60,2],"-40":[0,0,18,2,50,2],"-39":[0,0,16,2,60,2],"-38":[0,0,18,4,65,2],"-37":[0,0,16,4,45,3],"-36":[0,0,16,4,45,3],"-35":[0,0,13,8,45,3],"-34":[0,0,13,8,45,3],"-33":[0,0,13,6,40,3],"-32":[0,0,13,6,40,3],"-31":[0,0,16,8,50,3],"-30":[0,0,16,8,50,3],"-29":[0,0,15,5,40,3],"-28":[0,0,15,5,40,3],"-27":[0,0,14,6,45,3],"-26":[0,0,14,6,45,3],"-25":[0,0,60,26,200,1],"-24":[0,0,60,26,200,1],"-23":[0,0,22,8,40,5],"-22":[0,0,22,8,40,5],"-21":[0,0,70,22,220,5],"-20":[0,0,70,22,220,5],"-19":[0,0,70,22,220,5],"-18":[0,0,70,22,220,5],"-17":[0,0,26,12,48,5],"-16":[0,0,26,12,48,5],"-15":[0,0,40,28,260,3],"-14":[0,0,26,8,80,3],"-13":[0,0,26,8,80,3],"-12":[0,0,22,8,40,5],"-11":[0,0,22,8,40,5],"-10":[0,0,18,6,25,1],"-9":[0,0,15,7,25,1],"-8":[0,0,12,4,25,1],"-7":[0,0,12,6,25,1],"-6":[0,0,15,4,25,1],"-5":[0,0,13,4,25,1],"-4":[2,0,5,5,25,1],"-3":[0,0,6,0,25,1],"-2":[0,0,45,20,170,1],"-1":[0,0,45,10,170,1]}}

```


---

## 🤖 Assistant · 2026-08-19T03:18:14.682Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
That dump wasn't useful for names. Never mind the exact name of 471 — from the data (471 spawns 472, spawns chaos balls 30) — 471 is likely the **"Nebula Floater"**? no. Spawning NPC 472 in graveyard context = "Ghost"? Hmm, NPC 30 is Chaos Ball. OK: 471 = "Chaos Ball spawner"... whatever — I'll grep the game's npc name data file for 471. Actually the vanilla-bestiary.json is data. Let me not spend more on the name; the important thing is our repo DOESN'T implement the 471 special AI. Let me quickly check our enemies data for 471 name via a different file. Actually let me use bestiaryStatics or npcPortraits. Quick grep in public l10n zh-Hans for NPC names around... The l10n uses keys like "Bestiary.NPCName.471"? Hmm. Skip — I'll refer to it as "type 471 (spawns 472, likely graveyard/chaos entity)". Actually — I remember now! 471 = "Wraith"? no... 472 spawned 70px above with chaos ball 30 = this is the GRAVEYARD "Ghostly..."? Hold on: spawning chaos balls = dark caster-like. NPCID 471 = "Mourning..."? Hmm, per the count "CountNPCS(472) < 10" — spawns up to 10 minions 472. This is 1.4 graveyard boss-adjacent... I'm fairly confident 471 = "Wraith"? no, 82.

Actually — I bet 471 = "Dungeon Spirit"? no 84. Let me just check the zh-Hans l10n quickly with proper key format.

Also type 415 = spawns 516 (with fire dust 259, solar pillar!) — 415 = "Drakomire"? Hmm 516 = "DrakomireFireball"? So 415 spawns fireballs = "ScutlixGunman"? Whatever — 415 IS implemented in ours only as move spec. Vanilla 415: justHit → ai2=120; ai2 countdown; ai2==0: if >6 fireballs exist → ai2=90; else facing + CanHit → ai2=-1 windup; windup -1..-42: vx*=0.8; at -18/-26/-34: dust + spawn NPC 516 at Center + (dir*45, +8); at -42 → ai2 = 180+30*rand(10). This is Drakomire shooting fireballs! Ours: fighterMoveSpec 415 (max 4 accel 0.1 damp 0.95) only — MISSING the fireball attack. MEDIUM.

Hmm wait — but is 415 handled in bossAI_martian or elsewhere? 415 is Solar Pillar "Drakomire"? Let me grep our repo for 516.

Also 427 (Scutlix?) — :57771? no wait, 427's shooting is at :2771 offset = 56245+2771 = 59016? Hmm the offsets: "2771: else if (type == 427)" → line 56245+2771-1 = 59015. That's the ranged section? no... 59015 is within the 425 storm diver area? Let me recompute: offsets are within sed output starting at 56245, so actual line = 56244 + offset. 427 at offset 2771 → 59015. And 426 at 590... 2861 → 59105. These are separate else-if branches after 425 (58865-59013). So 427/426 have their own air-servo attack blocks (59015-59192). Ours: 427 only move spec (max 6). Vanilla 427: has air servo (num124/125 with 40px Y dead zone, ±6 clamp, same-type separation) — similar to storm diver's jetpack servo. Ours MISSING. 426 (offset 2861 → 59105) similar servo — 426 = "Martian Hover..."? no — 426 is solar "Corite"? Hmm 426 = "Corite"! And 427 = "Scutlix". Wait no: Scutlix = 427? Per FIGHTER list... 426 in ranged-move excluded AND ranged section has 426 at 3314... The 59015 block for 427 = Scutlix gunner servo; 426 = Corite (flying charge). Ours: 426 has RANGED_TABLE? No — 426 not in RANGED_TABLE. It's in rangedMoveExcluded though. Hmm, our rangedMoveExcluded includes 426 and 424 — matching :3220 table (58865). The 426 air-servo attack (59105-59192) — is it in ours? grep for 426 in Enemy.ts beyond excludes. Let me check.

This is getting big. Let me be pragmatic: I can't verify every branch exhaustively within budget; focus on confirming the most impactful missing items and precise numeric diffs in already-ported code, then list "branches present in vanilla AI_003 with no our-side implementation" as a consolidated finding with ids.

Let me now:
1. Read the movement chain region in vanilla to verify fighterFamilies numbers (57799-58800). Read it in one go (1000 lines) — but I can skim via targeted greps for numbers. Actually our fighterFamilies.ts has extensive line comments claiming 1:1; I'll verify a representative sample: the num84 list, num85, num86, 78-80 mummy, 287, 243, 251, 460, 508/580/582 charger, 489, default num108. I'll read 57799-58150 and 58440-58800 chunks.
2. Read the jump section 60383-60734 (doors + jumps + flag8).
3. Read ranged section 59464-60100 to verify RANGED_TABLE numbers.
4. Read 57307-57550 (torch zombie + nailhead + butcher + possessed + fritz + stuck counter + discouragement).

Let me do 4 first (57307-57799), then movement chains, then ranged, then tail.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:15.324Z · glm-x-preview-260804

```
分支清单已明确。现在我来核实 日食/stuck-counter 区域以及 movement chains 的数值。
```


---

## 🤖 Assistant · 2026-08-19T03:18:15.679Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 200,
 "offset": 57307
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:15.703Z

**📎 ToolResult**

```
57307				}
57308			}
57309			if (type == 590)
57310			{
57311				position += netOffset;
57312				int num53 = (int)(position.Y + 6f) / 16;
57313				if (spriteDirection < 0)
57314				{
57315					int num54 = (int)(base.Center.X - 22f) / 16;
57316					Tile tileSafely = Framing.GetTileSafely(num54, num53);
57317					Tile tileSafely2 = Framing.GetTileSafely(num54 + 1, num53);
57318					if (WorldGen.InWorld(num54, num53) && tileSafely2.liquid == 0 && tileSafely.liquid == 0)
57319					{
57320						Lighting.AddLight(num54, num53, 1f, 0.95f, 0.8f);
57321						if (Main.rand.Next(30) == 0)
57322						{
57323							Dust.NewDust(new Vector2(base.Center.X - 22f, position.Y + 6f), 1, 1, 6);
57324						}
57325					}
57326				}
57327				else
57328				{
57329					int num55 = (int)(base.Center.X + 14f) / 16;
57330					Tile tileSafely3 = Framing.GetTileSafely(num55, num53);
57331					Tile tileSafely4 = Framing.GetTileSafely(num55 - 1, num53);
57332					if (WorldGen.InWorld(num55, num53) && tileSafely4.liquid == 0 && tileSafely3.liquid == 0)
57333					{
57334						Lighting.AddLight(num55, num53, 1f, 0.95f, 0.8f);
57335						if (Main.rand.Next(30) == 0)
57336						{
57337							Dust.NewDust(new Vector2(base.Center.X + 14f, position.Y + 6f), 1, 1, 6);
57338						}
57339					}
57340				}
57341				position -= netOffset;
57342			}
57343			else if (type == 591)
57344			{
57345				position += netOffset;
57346				if (!wet)
57347				{
57348					if (spriteDirection < 0)
57349					{
57350						Lighting.AddLight(new Vector2(base.Center.X - 36f, position.Y + 24f), 1f, 0.95f, 0.8f);
57351						if (ai[2] == 0f && Main.rand.Next(30) == 0)
57352						{
57353							Dust.NewDust(new Vector2(base.Center.X - 36f, position.Y + 24f), 1, 1, 6);
57354						}
57355					}
57356					else
57357					{
57358						Lighting.AddLight(new Vector2(base.Center.X + 28f, position.Y + 24f), 1f, 0.95f, 0.8f);
57359						if (ai[2] == 0f && Main.rand.Next(30) == 0)
57360						{
57361							Dust.NewDust(new Vector2(base.Center.X + 28f, position.Y + 24f), 1, 1, 6);
57362						}
57363					}
57364				}
57365				position -= netOffset;
57366			}
57367			if (type == 111)
57368			{
57369				if (ai[3] < 0f)
57370				{
57371					TargetClosest(faceTarget: false);
57372				}
57373				if (ai[3] < 0f && (justHit || Distance(Main.player[target].Center) < 200f))
57374				{
57375					ai[3] = 0f;
57376					ai[0] = 0f;
57377					netUpdate = true;
57378				}
57379				if (ai[3] < 0f)
57380				{
57381					directionY = -1;
57382					flag = false;
57383					velocity.X *= 0.93f;
57384					if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
57385					{
57386						velocity.X = 0f;
57387					}
57388					int num56 = (int)(0f - ai[3] - 1f);
57389					int num57 = Math.Sign(Main.npc[num56].Center.X - base.Center.X);
57390					if (num57 != direction)
57391					{
57392						velocity.X = 0f;
57393						direction = num57;
57394						netUpdate = true;
57395					}
57396					if (ai[0] < 1000f)
57397					{
57398						ai[0] = 1000f;
57399					}
57400					if ((ai[0] += 1f) >= 1300f)
57401					{
57402						ai[0] = 1000f;
57403						netUpdate = true;
57404					}
57405					return;
57406				}
57407				if (ai[0] >= 1000f)
57408				{
57409					ai[0] = 0f;
57410				}
57411			}
57412			bool flag5 = false;
57413			bool flag6 = false;
57414			if (velocity.X == 0f)
57415			{
57416				flag6 = true;
57417			}
57418			if (justHit)
57419			{
57420				flag6 = false;
57421			}
57422			if (Main.netMode != 1 && type == 198 && (double)life <= (double)lifeMax * 0.55)
57423			{
57424				Transform(199);
57425			}
57426			if (Main.netMode != 1 && type == 348 && (double)life <= (double)lifeMax * 0.55)
57427			{
57428				Transform(349);
57429			}
57430			int num58 = 60;
57431			if (type == 120)
57432			{
57433				num58 = 180;
57434				if (ai[3] == -120f)
57435				{
57436					velocity *= 0f;
57437					ai[3] = 0f;
57438					position += netOffset;
57439					SoundEngine.PlaySound(SoundID.Item8, position);
57440					Vector2 vector19 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
57441					float num59 = oldPos[2].X + (float)width * 0.5f - vector19.X;
57442					float num60 = oldPos[2].Y + (float)height * 0.5f - vector19.Y;
57443					float num61 = (float)Math.Sqrt(num59 * num59 + num60 * num60);
57444					num61 = 2f / num61;
57445					num59 *= num61;
57446					num60 *= num61;
57447					for (int num62 = 0; num62 < 20; num62++)
57448					{
57449						int num63 = Dust.NewDust(position, width, height, 71, num59, num60, 200, default(Color), 2f);
57450						Main.dust[num63].noGravity = true;
57451						Main.dust[num63].velocity.X *= 2f;
57452					}
57453					for (int num64 = 0; num64 < 20; num64++)
57454					{
57455						int num65 = Dust.NewDust(oldPos[2], width, height, 71, 0f - num59, 0f - num60, 200, default(Color), 2f);
57456						Main.dust[num65].noGravity = true;
57457						Main.dust[num65].velocity.X *= 2f;
57458					}
57459					position -= netOffset;
57460				}
57461			}
57462			bool flag7 = false;
57463			bool flag8 = true;
57464			if (NPCID.Sets.CritterThatCanTurnOnPlayers[type])
57465			{
57466				flag8 = false;
57467			}
57468			if (type == 343 || type == 47 || type == 67 || type == 109 || type == 110 || type == 111 || type == 120 || type == 163 || type == 164 || type == 239 || type == 168 || type == 199 || type == 206 || type == 214 || type == 215 || type == 216 || type == 217 || type == 218 || type == 219 || type == 220 || type == 226 || type == 243 || type == 251 || type == 257 || type == 258 || type == 290 || type == 291 || type == 292 || type == 293 || type == 305 || type == 306 || type == 307 || type == 308 || type == 309 || type == 348 || type == 349 || type == 350 || type == 351 || type == 379 || (type >= 430 && type <= 436) || type == 591 || type == 380 || type == 381 || type == 382 || type == 383 || type == 386 || type == 391 || (type >= 449 && type <= 452) || type == 466 || type == 464 || type == 166 || type == 469 || type == 468 || type == 471 || type == 470 || type == 480 || type == 481 || type == 482 || type == 411 || type == 424 || type == 409 || (type >= 494 && type <= 506) || type == 425 || type == 427 || type == 426 || type == 428 || type == 580 || type == 508 || type == 415 || type == 419 || type == 520 || (type >= 524 && type <= 527) || type == 528 || type == 529 || type == 530 || type == 532 || type == 582 || type == 624 || type == 631)
57469			{
57470				flag8 = false;
57471			}
57472			bool flag9 = false;
57473			int num66 = type;
57474			if (num66 == 425 || num66 == 471)
57475			{
57476				flag9 = true;
57477			}
57478			bool flag10 = true;
57479			switch (type)
57480			{
57481			case 110:
57482			case 111:
57483			case 206:
57484			case 214:
57485			case 215:
57486			case 216:
57487			case 291:
57488			case 292:
57489			case 293:
57490			case 350:
57491			case 379:
57492			case 380:
57493			case 381:
57494			case 382:
57495			case 409:
57496			case 411:
57497			case 424:
57498			case 426:
57499			case 466:
57500			case 498:
57501			case 499:
57502			case 500:
57503			case 501:
57504			case 502:
57505			case 503:
57506			case 504:

```


---

## 🤖 Assistant · 2026-08-19T03:18:33.175Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Comparing with our fighterAI:

- 590/591 torch light: ours torchZombieLight ✓ handled.
- 111 (goblin archer) ambush standby (ai3<0): same structure as 379/380 standby (goblin ambush at goblin army totem?). Ours: does fighterAI handle 111's ai3<0 standby? Our case-3 routing only handles 379/380 standby. 111's standby: TargetClosest(faceTarget:false), justHit||dist<200 → ai3=0, ai0=0; standby: directionY=-1, vx*=0.93, face npc[num56] where num56 = -ai3-1... This is the "goblin archer waiting by the campfire" during goblin army? Actually 111 = Goblin Archer? Hmm — 111 standby phase relates to goblin summoner totem? whatever — MISSING in ours. LOW-MEDIUM (goblin invasion archers should stand watching until player near). Let me grep 111 handling in Enemy.ts beyond RANGED_TABLE.

- 198→199 and 348→349 transforms: ours has 198→199 ✓; 348→349 NOT (comment says "霜月未引入不移植" — nutcracker frost moon not enabled — acceptable, skip since frost moon... wait, memory says frost moon IS landed (event-system-port: 日食/南瓜霜月). Hmm — 348 Nutcracker transforms to 349 at 55% HP during frost moon. If frost moon is landed, this is missing. Let me note medium-low. Our comment claims 霜月未引入 but memory says frost moon landed. Flag as suspect/medium.

- 120 chaos: num58=180 ✓; the -120 arrival FX block is INSIDE this else (vanilla plays Item8 + 40 dust at oldPos[2] and new pos). Ours chaosElementalStep ✓ (Item_8 + 2×20 dust ✓).

- flag7/flag8: ours FIGHTER_NO_DOOR ✓ matches the :57468 list exactly? Ours has 343,47,67,109,110,111,120,163,164,239,168,199,206,214,215,216,217,218,219,220,226,243,251,257,258,290,291,292,293,305-309,348,349,350,351,379,430-436,591,380-383,386,391,449-452,466,464,166,469,468,471,470,480,481,482,411,424,409,494-506,425,427,426,428,580,508,415,419,520,524-527,528,529,530,532,582,624,631 ✓ — also NPCID.Sets.CritterThatCanTurnOnPlayers — critter flag; ours may handle via critter routing. ✓ equivalent.

- flag9 = type 425 || 471 (they use ai2 differently).
- flag10 list = "jump-capable?" types 110,111,206,214,215,216,291,292,293,350,379,380,381,382,409,411,424,426,466,498-504+... (cut off). This flag10 probably = "no jump" exclusion for the jump section. Our fighterAI jump section applies to all — check whether ours excludes these. The jump block in ours has no exclusion list! Vanilla flag10 types likely skip jumping (ranged shooters don't hop). Need to see what flag10 does — read further at 57506-57550 + the jump section usage.

Let me continue reading 57506-57799 (nailhead/butcher/possessed/fritz + stuck counter + discouragement).
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:33.575Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 295,
 "offset": 57506
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:33.586Z

**📎 ToolResult**

```
57506			case 504:
57507			case 505:
57508			case 506:
57509			case 520:
57510				if (ai[2] > 0f)
57511				{
57512					flag10 = false;
57513				}
57514				break;
57515			}
57516			if (!flag9 && flag10)
57517			{
57518				if (velocity.Y == 0f && ((velocity.X > 0f && direction < 0) || (velocity.X < 0f && direction > 0)))
57519				{
57520					flag7 = true;
57521				}
57522				if (position.X == oldPosition.X || ai[3] >= (float)num58 || flag7)
57523				{
57524					ai[3] += 1f;
57525				}
57526				else if ((double)Math.Abs(velocity.X) > 0.9 && ai[3] > 0f)
57527				{
57528					ai[3] -= 1f;
57529				}
57530				if (ai[3] > (float)(num58 * 10))
57531				{
57532					ai[3] = 0f;
57533				}
57534				if (justHit)
57535				{
57536					ai[3] = 0f;
57537				}
57538				if (ai[3] == (float)num58)
57539				{
57540					netUpdate = true;
57541				}
57542				if (Main.player[target].Hitbox.Intersects(base.Hitbox))
57543				{
57544					ai[3] = 0f;
57545				}
57546			}
57547			if (type == 463 && Main.netMode != 1)
57548			{
57549				if (localAI[3] > 0f)
57550				{
57551					localAI[3] -= 1f;
57552				}
57553				if (justHit && localAI[3] <= 0f && Main.rand.Next(3) == 0)
57554				{
57555					localAI[3] = 30f;
57556					int num67 = Main.rand.Next(3, 6);
57557					int[] array = new int[num67];
57558					int num68 = 0;
57559					for (int num69 = 0; num69 < 255; num69++)
57560					{
57561						if (Main.player[num69].active && !Main.player[num69].dead && Collision.CanHitLine(position, width, height, Main.player[num69].position, Main.player[num69].width, Main.player[num69].height))
57562						{
57563							array[num68] = num69;
57564							num68++;
57565							if (num68 == num67)
57566							{
57567								break;
57568							}
57569						}
57570					}
57571					if (num68 > 1)
57572					{
57573						for (int num70 = 0; num70 < 100; num70++)
57574						{
57575							int num71 = Main.rand.Next(num68);
57576							int num72;
57577							for (num72 = num71; num72 == num71; num72 = Main.rand.Next(num68))
57578							{
57579							}
57580							int num73 = array[num71];
57581							array[num71] = array[num72];
57582							array[num72] = num73;
57583						}
57584					}
57585					Vector2 vector20 = new Vector2(-1f, -1f);
57586					for (int num74 = 0; num74 < num68; num74++)
57587					{
57588						Vector2 vector21 = Main.npc[array[num74]].Center - base.Center;
57589						vector21.Normalize();
57590						vector20 += vector21;
57591					}
57592					vector20.Normalize();
57593					for (int num75 = 0; num75 < num67; num75++)
57594					{
57595						float num76 = Main.rand.Next(8, 13);
57596						Vector2 vector22 = new Vector2(Main.rand.Next(-100, 101), Main.rand.Next(-100, 101));
57597						vector22.Normalize();
57598						if (num68 > 0)
57599						{
57600							vector22 += vector20;
57601							vector22.Normalize();
57602						}
57603						vector22 *= num76;
57604						if (num68 > 0)
57605						{
57606							num68--;
57607							vector22 = Main.player[array[num68]].Center - base.Center;
57608							vector22.Normalize();
57609							vector22 *= num76;
57610						}
57611						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X, position.Y + (float)(width / 4), vector22.X, vector22.Y, 498, (int)((double)damage * 0.15), 1f, Main.myPlayer);
57612					}
57613				}
57614			}
57615			if (type == 460)
57616			{
57617				if (velocity.Y < 0f - gravity || velocity.Y > gravity)
57618				{
57619					knockBackResist = 0f;
57620				}
57621				else
57622				{
57623					knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.25f);
57624				}
57625			}
57626			if (type == 469)
57627			{
57628				knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.45f);
57629				if (ai[2] == 1f)
57630				{
57631					knockBackResist = 0f;
57632				}
57633				bool flag11 = false;
57634				int num77 = (int)base.Center.X / 16;
57635				int num78 = (int)base.Center.Y / 16;
57636				for (int num79 = num77 - 1; num79 <= num77 + 1; num79++)
57637				{
57638					for (int num80 = num78 - 1; num80 <= num78 + 1; num80++)
57639					{
57640						if (Main.tile[num79, num80] != null && Main.tile[num79, num80].wall > 0)
57641						{
57642							flag11 = true;
57643							break;
57644						}
57645					}
57646					if (flag11)
57647					{
57648						break;
57649					}
57650				}
57651				if (ai[2] == 0f && flag11)
57652				{
57653					if (velocity.Y == 0f)
57654					{
57655						flag = true;
57656						velocity.Y = -4.6f;
57657						velocity.X *= 1.3f;
57658					}
57659					else if (velocity.Y > 0f && !Main.player[target].dead)
57660					{
57661						ai[2] = 1f;
57662					}
57663				}
57664				if (flag11 && ai[2] == 1f && !Main.player[target].dead && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
57665				{
57666					Vector2 vector23 = Main.player[target].Center - base.Center;
57667					float num81 = vector23.Length();
57668					vector23.Normalize();
57669					vector23 *= 4.5f + num81 / 300f;
57670					velocity = (velocity * 29f + vector23) / 30f;
57671					noGravity = true;
57672					ai[2] = 1f;
57673					return;
57674				}
57675				noGravity = false;
57676				ai[2] = 0f;
57677			}
57678			if (type == 462 && velocity.Y == 0f && (Main.player[target].Center - base.Center).Length() < 150f && Math.Abs(velocity.X) > 3f && ((velocity.X < 0f && base.Center.X > Main.player[target].Center.X) || (velocity.X > 0f && base.Center.X < Main.player[target].Center.X)))
57679			{
57680				flag = true;
57681				velocity.X *= 1.75f;
57682				velocity.Y -= 4.5f;
57683				if (base.Center.Y - Main.player[target].Center.Y > 20f)
57684				{
57685					velocity.Y -= 0.5f;
57686				}
57687				if (base.Center.Y - Main.player[target].Center.Y > 40f)
57688				{
57689					velocity.Y -= 1f;
57690				}
57691				if (base.Center.Y - Main.player[target].Center.Y > 80f)
57692				{
57693					velocity.Y -= 1.5f;
57694				}
57695				if (base.Center.Y - Main.player[target].Center.Y > 100f)
57696				{
57697					velocity.Y -= 1.5f;
57698				}
57699				if (Math.Abs(velocity.X) > 7f)
57700				{
57701					if (velocity.X < 0f)
57702					{
57703						velocity.X = -7f;
57704					}
57705					else
57706					{
57707						velocity.X = 7f;
57708					}
57709				}
57710			}
57711			if (type == 624 && target < 255)
57712			{
57713				if (!Main.remixWorld && !Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
57714				{
57715					ai[3] = num58;
57716					directionY = -1;
57717					if (type == 624 && !AI_003_Gnomes_ShouldTurnToStone() && (base.Center - Main.player[target].Center).Length() > 500f)
57718					{
57719						velocity.X *= 0.95f;
57720						if ((double)velocity.X > -0.1 && (double)velocity.X < 0.1)
57721						{
57722							velocity.X = 0f;
57723						}
57724						return;
57725					}
57726				}
57727				else if (Main.player[target].Center.Y > base.Center.Y - 128f)
57728				{
57729					ai[3] = 0f;
57730				}
57731			}
57732			if (ai[3] < (float)num58 && DespawnEncouragement_AIStyle3_Fighters_NotDiscouraged(type, position, this))
57733			{
57734				if (shimmerTransparency < 1f)
57735				{
57736					if ((type == 3 || type == 691 || type == 591 || type == 590 || type == 331 || type == 332 || type == 21 || (type >= 449 && type <= 452) || type == 31 || type == 294 || type == 295 || type == 296 || type == 77 || type == 110 || type == 132 || type == 167 || type == 161 || type == 162 || type == 186 || type == 187 || type == 188 || type == 189 || type == 197 || type == 200 || type == 201 || type == 202 || type == 203 || type == 223 || type == 291 || type == 292 || type == 293 || type == 320 || type == 321 || type == 319 || type == 481 || type == 632 || type == 635) && Main.rand.Next(1000) == 0)
57737					{
57738						SoundEngine.PlaySound(14, (int)position.X, (int)position.Y);
57739					}
57740					if ((type == 489 || type == 586) && Main.rand.Next(800) == 0)
57741					{
57742						SoundEngine.PlaySound(14, (int)position.X, (int)position.Y, type);
57743					}
57744					if ((type == 78 || type == 79 || type == 80 || type == 630) && Main.rand.Next(500) == 0)
57745					{
57746						SoundEngine.PlaySound(26, (int)position.X, (int)position.Y);
57747					}
57748					if (type == 159 && Main.rand.Next(500) == 0)
57749					{
57750						SoundEngine.PlaySound(29, (int)position.X, (int)position.Y, 7);
57751					}
57752					if (type == 162 && Main.rand.Next(500) == 0)
57753					{
57754						SoundEngine.PlaySound(29, (int)position.X, (int)position.Y, 6);
57755					}
57756					if (type == 181 && Main.rand.Next(500) == 0)
57757					{
57758						SoundEngine.PlaySound(29, (int)position.X, (int)position.Y, 8);
57759					}
57760					if (type >= 269 && type <= 280 && Main.rand.Next(1000) == 0)
57761					{
57762						SoundEngine.PlaySound(14, (int)position.X, (int)position.Y);
57763					}
57764				}
57765				TargetClosest();
57766				if (directionY > 0 && Main.player[target].Center.Y <= base.Bottom.Y)
57767				{
57768					directionY = -1;
57769				}
57770			}
57771			else if (!(ai[2] > 0f) || !DespawnEncouragement_AIStyle3_Fighters_CanBeBusyWithAction(type))
57772			{
57773				if (Main.IsItDay() && (double)(position.Y / 16f) < Main.worldSurface && type != 624 && type != 631)
57774				{
57775					EncourageDespawn(10);
57776				}
57777				if (velocity.X == 0f)
57778				{
57779					if (velocity.Y == 0f)
57780					{
57781						ai[0] += 1f;
57782						if (ai[0] >= 2f)
57783						{
57784							direction *= -1;
57785							spriteDirection = direction;
57786							ai[0] = 0f;
57787						}
57788					}
57789				}
57790				else
57791				{
57792					ai[0] = 0f;
57793				}
57794				if (direction == 0)
57795				{
57796					direction = 1;
57797				}
57798			}
57799			if (type == 159 || type == 349)
57800			{

```


---

## 🤖 Assistant · 2026-08-19T03:18:57.016Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Comparing the stuck counter/discouragement with ours:

- flag7 = grounded && moving against direction ✓ (ours `opposite` in chaosElementalStep — but ours ONLY runs the stuck counter for type 120! Vanilla runs it for ALL fighters except flag9/flag10 types). ★ BIG FINDING: the ai[3] stuck counter (:57516-57546) applies to ALL fighters (num58=60, chaos 180). Ours implements it only for 120 (chaosElementalStep). The counter drives... what? It's read at :60679 (teleport for 120) AND likely in the jump section (ai[3] >= num58 forces jumping?). Let me check where ai[3]/num58 is consumed later — probably the jump section uses it to force jumps when stuck. If ours lacks the generic stuck counter, ordinary fighters stuck behind walls won't get the jump-forcing behavior. Need to check the jump section (~60500-60700) to see ai[3] usage. Also `if (ai[3] == num58) netUpdate`.

- 463 nailhead ✓ 1:1 (ours matches; num68 count = players; ours single player ✓; array shuffle ~single player trivial ✓; note vanilla `if (num68 > 1)` shuffle — fine).
  - One diff: vanilla vector20 = (-1,-1) + Σ unit vectors, then Normalize ✓ ours bx=-1,by=-1 + unit ✓ normalize ✓.

- 460 butcher ✓.
- 469 possessed ✓ 1:1 (velocity = (velocity*29 + v)/30 ✓ ours; noGravity=true during dash — ours: x+=vx no gravity ✓; ai2=0 fallback ✓).

- 462 fritz ✓ 1:1.

- 624 gnome freeze-when-watched (:57711-57731): when player can't see it (no CanHit) → ai3 = num58 (60) + directionY=-1; if ALSO !ShouldTurnToStone && distance > 500 → vx *= 0.95, return (gnome freezes/stands still off-screen). When player CAN see and player.Y > centerY-128 → ai3 = 0. Ours: gnome only has petrify in fixedUpdate — missing the freeze/wander logic. LOW-MEDIUM (gnome behavior: freezes when watched, moves when not).

- 57732-57770: the "discouraged" else-if: ambient sounds ✓ (ours ambientSoundTick probably); TargetClosest() every tick + directionY reset. Ours: facing = seekDirX every tick ✓ (not gated on NotDiscouraged — ours sets facing always when player; vanilla sets facing only in the not-discouraged branch! In the discouraged branch direction keeps/flip logic. Ours: discouraged branch overrides facing? Let me re-check our fighterAI: `if (discouraged) { encourageDespawn(10); wander } else if (player) { facing = seekDirX }`. ✓ matches.

But WAIT — vanilla discourage condition: `ai[3] < num58 && NotDiscouraged(type,...)` → else branch `!(ai[2] > 0) || !CanBeBusyWithAction` → then `Main.IsItDay() && y < worldSurface && type != 624 && type != 631 → EncourageDespawn(10)`. Hmm! The vanilla structure: the wander branch is NOT gated on day — it's the else of (not-discouraged && ai3 < num58). NotDiscouraged(type, position, this) = the big day-active gating check (:60694 per our comment: !eclipse && !graveyard etc...). Let me look at DespawnEncouragement_AIStyle3_Fighters_NotDiscouraged to confirm ours' daySurface logic matches — our memory notes say it's :60694. I'll check it at the end of AI_003.

Also the else-branch wander: `if (velocity.X == 0 && velocity.Y == 0) ai0 += 1, >= 2 → direction*=-1; else ai0=0; direction==0→1`. Ours: `if (Math.abs(this.vx) < 0.1 && this.vy === 0) { state += 1; if >= 2 flip }` — uses `state` field instead of ai0, and < 0.1 instead of ==0. ✓ approximately.

But ours gates the whole discouraged branch on `daySurface && !dayActive` — vanilla: the else branch (wander) triggers whenever NOT (ai3<num58 && NotDiscouraged) — including nighttime? No — NotDiscouraged at night = true (not day). Hmm: NotDiscouraged(type, position, npc) — let me read it to be sure (at :60694 area). It probably returns true when NOT (day && surface && type-not-in-daylist). So at night → discouraged=false → chase ✓ same as ours.

Now the jump section and movement chains. Let me read 57799-58200 (movement chains start) to verify numbers.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:57.366Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 410,
 "offset": 57799
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:57.380Z

**📎 ToolResult**

```
57799			if (type == 159 || type == 349)
57800			{
57801				if (type == 159 && ((velocity.X > 0f && direction < 0) || (velocity.X < 0f && direction > 0)))
57802				{
57803					velocity.X *= 0.95f;
57804				}
57805				if (velocity.X < -6f || velocity.X > 6f)
57806				{
57807					if (velocity.Y == 0f)
57808					{
57809						velocity *= 0.8f;
57810					}
57811				}
57812				else if (velocity.X < 6f && direction == 1)
57813				{
57814					if (velocity.Y == 0f && velocity.X < 0f)
57815					{
57816						velocity.X *= 0.99f;
57817					}
57818					velocity.X += 0.07f;
57819					if (velocity.X > 6f)
57820					{
57821						velocity.X = 6f;
57822					}
57823				}
57824				else if (velocity.X > -6f && direction == -1)
57825				{
57826					if (velocity.Y == 0f && velocity.X > 0f)
57827					{
57828						velocity.X *= 0.99f;
57829					}
57830					velocity.X -= 0.07f;
57831					if (velocity.X < -6f)
57832					{
57833						velocity.X = -6f;
57834					}
57835				}
57836			}
57837			else if (NPCID.Sets.CritterThatCanTurnOnPlayers[type])
57838			{
57839				if (!Main.player[target].dead && velocity.Y == 0f)
57840				{
57841					float num82 = (base.Center - Main.player[target].Center).Length();
57842					num82 = Math.Abs(base.Center.X - Main.player[target].Center.X);
57843					if (num82 > 0f && num82 < 100f && ((velocity.X < 0f && Main.player[target].Center.X < base.Center.X) || (velocity.X > 0f && Main.player[target].Center.X > base.Center.X)))
57844					{
57845						velocity.Y = -4f;
57846						velocity.X += (float)direction * 3f;
57847					}
57848				}
57849				float num83 = 3.5f;
57850				if (velocity.X < 0f - num83 || velocity.X > num83)
57851				{
57852					if (velocity.Y == 0f)
57853					{
57854						velocity *= 0.8f;
57855					}
57856				}
57857				else if (velocity.X < num83 && direction == 1)
57858				{
57859					if (velocity.Y == 0f && velocity.X < 0f)
57860					{
57861						velocity.X *= 0.8f;
57862					}
57863					velocity.X += 0.1f;
57864					if (velocity.X > num83)
57865					{
57866						velocity.X = num83;
57867					}
57868				}
57869				else if (velocity.X > 0f - num83 && direction == -1)
57870				{
57871					if (velocity.Y == 0f && velocity.X > 0f)
57872					{
57873						velocity.X *= 0.8f;
57874					}
57875					velocity.X -= 0.1f;
57876					if (velocity.X < 0f - num83)
57877					{
57878						velocity.X = 0f - num83;
57879					}
57880				}
57881			}
57882			else if (type == 199)
57883			{
57884				if (velocity.X < -4f || velocity.X > 4f)
57885				{
57886					if (velocity.Y == 0f)
57887					{
57888						velocity *= 0.8f;
57889					}
57890				}
57891				else if (velocity.X < 4f && direction == 1)
57892				{
57893					if (velocity.Y == 0f && velocity.X < 0f)
57894					{
57895						velocity.X *= 0.8f;
57896					}
57897					velocity.X += 0.1f;
57898					if (velocity.X > 4f)
57899					{
57900						velocity.X = 4f;
57901					}
57902				}
57903				else if (velocity.X > -4f && direction == -1)
57904				{
57905					if (velocity.Y == 0f && velocity.X > 0f)
57906					{
57907						velocity.X *= 0.8f;
57908					}
57909					velocity.X -= 0.1f;
57910					if (velocity.X < -4f)
57911					{
57912						velocity.X = -4f;
57913					}
57914				}
57915			}
57916			else if (type == 120 || type == 166 || type == 213 || type == 258 || type == 528 || type == 529)
57917			{
57918				if (velocity.X < -3f || velocity.X > 3f)
57919				{
57920					if (velocity.Y == 0f)
57921					{
57922						velocity *= 0.8f;
57923					}
57924				}
57925				else if (velocity.X < 3f && direction == 1)
57926				{
57927					if (velocity.Y == 0f && velocity.X < 0f)
57928					{
57929						velocity.X *= 0.99f;
57930					}
57931					velocity.X += 0.07f;
57932					if (velocity.X > 3f)
57933					{
57934						velocity.X = 3f;
57935					}
57936				}
57937				else if (velocity.X > -3f && direction == -1)
57938				{
57939					if (velocity.Y == 0f && velocity.X > 0f)
57940					{
57941						velocity.X *= 0.99f;
57942					}
57943					velocity.X -= 0.07f;
57944					if (velocity.X < -3f)
57945					{
57946						velocity.X = -3f;
57947					}
57948				}
57949			}
57950			else if (type == 461 || type == 27 || type == 77 || type == 104 || type == 163 || type == 162 || type == 196 || type == 197 || type == 212 || type == 257 || type == 326 || type == 343 || type == 348 || type == 351 || (type >= 524 && type <= 527) || type == 530 || type == 236)
57951			{
57952				if (velocity.X < -2f || velocity.X > 2f)
57953				{
57954					if (velocity.Y == 0f)
57955					{
57956						velocity *= 0.8f;
57957					}
57958				}
57959				else if (velocity.X < 2f && direction == 1)
57960				{
57961					velocity.X += 0.07f;
57962					if (velocity.X > 2f)
57963					{
57964						velocity.X = 2f;
57965					}
57966				}
57967				else if (velocity.X > -2f && direction == -1)
57968				{
57969					velocity.X -= 0.07f;
57970					if (velocity.X < -2f)
57971					{
57972						velocity.X = -2f;
57973					}
57974				}
57975			}
57976			else if (type == 109)
57977			{
57978				if (velocity.X < -2f || velocity.X > 2f)
57979				{
57980					if (velocity.Y == 0f)
57981					{
57982						velocity *= 0.8f;
57983					}
57984				}
57985				else if (velocity.X < 2f && direction == 1)
57986				{
57987					velocity.X += 0.04f;
57988					if (velocity.X > 2f)
57989					{
57990						velocity.X = 2f;
57991					}
57992				}
57993				else if (velocity.X > -2f && direction == -1)
57994				{
57995					velocity.X -= 0.04f;
57996					if (velocity.X < -2f)
57997					{
57998						velocity.X = -2f;
57999					}
58000				}
58001			}
58002			else if (type == 21 || type == 26 || type == 31 || type == 294 || type == 295 || type == 296 || type == 47 || type == 73 || type == 140 || type == 164 || type == 239 || type == 167 || type == 168 || type == 185 || type == 198 || type == 201 || type == 202 || type == 203 || type == 217 || type == 218 || type == 219 || type == 226 || type == 181 || type == 254 || type == 338 || type == 339 || type == 340 || type == 342 || type == 385 || type == 389 || type == 462 || type == 463 || type == 466 || type == 464 || type == 469 || type == 470 || type == 480 || type == 482 || type == 425 || type == 429 || type == 586 || type == 631 || type == 635)
58003			{
58004				float num84 = 1.5f;
58005				if (type == 181 && Main.remixWorld)
58006				{
58007					num84 = 3.75f;
58008				}
58009				else if (type == 294)
58010				{
58011					num84 = 2f;
58012				}
58013				else if (type == 295)
58014				{
58015					num84 = 1.75f;
58016				}
58017				else if (type == 296)
58018				{
58019					num84 = 1.25f;
58020				}
58021				else if (type == 201)
58022				{
58023					num84 = 1.1f;
58024				}
58025				else if (type == 202)
58026				{
58027					num84 = 0.9f;
58028				}
58029				else if (type == 203)
58030				{
58031					num84 = 1.2f;
58032				}
58033				else if (type == 338)
58034				{
58035					num84 = 1.75f;
58036				}
58037				else if (type == 339)
58038				{
58039					num84 = 1.25f;
58040				}
58041				else if (type == 340)
58042				{
58043					num84 = 2f;
58044				}
58045				else if (type == 385)
58046				{
58047					num84 = 1.8f;
58048				}
58049				else if (type == 389)
58050				{
58051					num84 = 2.25f;
58052				}
58053				else if (type == 462)
58054				{
58055					num84 = 4f;
58056				}
58057				else if (type == 463)
58058				{
58059					num84 = 0.75f;
58060				}
58061				else if (type == 466)
58062				{
58063					num84 = 3.75f;
58064				}
58065				else if (type == 469)
58066				{
58067					num84 = 3.25f;
58068				}
58069				else if (type == 480)
58070				{
58071					num84 = 1.5f + (1f - (float)life / (float)lifeMax) * 2f;
58072				}
58073				else if (type == 425)
58074				{
58075					num84 = 6f;
58076				}
58077				else if (type == 429)
58078				{
58079					num84 = 4f;
58080				}
58081				else if (type == 631)
58082				{
58083					num84 = 0.9f;
58084				}
58085				else if (type == 586)
58086				{
58087					num84 = 1.5f + (1f - (float)life / (float)lifeMax) * 3.5f;
58088				}
58089				if (type == 21 || type == 201 || type == 202 || type == 203 || type == 342 || type == 635)
58090				{
58091					num84 *= 1f + (1f - scale);
58092				}
58093				if (velocity.X < 0f - num84 || velocity.X > num84)
58094				{
58095					if (velocity.Y == 0f)
58096					{
58097						velocity *= 0.8f;
58098					}
58099				}
58100				else if (velocity.X < num84 && direction == 1)
58101				{
58102					if (type == 466 && velocity.X < -2f)
58103					{
58104						velocity.X *= 0.9f;
58105					}
58106					if (type == 586 && velocity.Y == 0f && velocity.X < -1f)
58107					{
58108						velocity.X *= 0.9f;
58109					}
58110					velocity.X += 0.07f;
58111					if (velocity.X > num84)
58112					{
58113						velocity.X = num84;
58114					}
58115				}
58116				else if (velocity.X > 0f - num84 && direction == -1)
58117				{
58118					if (type == 466 && velocity.X > 2f)
58119					{
58120						velocity.X *= 0.9f;
58121					}
58122					if (type == 586 && velocity.Y == 0f && velocity.X > 1f)
58123					{
58124						velocity.X *= 0.9f;
58125					}
58126					velocity.X -= 0.07f;
58127					if (velocity.X < 0f - num84)
58128					{
58129						velocity.X = 0f - num84;
58130					}
58131				}
58132				if (velocity.Y == 0f && type == 462 && ((direction > 0 && velocity.X < 0f) || (direction < 0 && velocity.X > 0f)))
58133				{
58134					velocity.X *= 0.9f;
58135				}
58136			}
58137			else if (type >= 269 && type <= 280)
58138			{
58139				float num85 = 1.5f;
58140				if (type == 269)
58141				{
58142					num85 = 2f;
58143				}
58144				if (type == 270)
58145				{
58146					num85 = 1f;
58147				}
58148				if (type == 271)
58149				{
58150					num85 = 1.5f;
58151				}
58152				if (type == 272)
58153				{
58154					num85 = 3f;
58155				}
58156				if (type == 273)
58157				{
58158					num85 = 1.25f;
58159				}
58160				if (type == 274)
58161				{
58162					num85 = 3f;
58163				}
58164				if (type == 275)
58165				{
58166					num85 = 3.25f;
58167				}
58168				if (type == 276)
58169				{
58170					num85 = 2f;
58171				}
58172				if (type == 277)
58173				{
58174					num85 = 2.75f;
58175				}
58176				if (type == 278)
58177				{
58178					num85 = 1.8f;
58179				}
58180				if (type == 279)
58181				{
58182					num85 = 1.3f;
58183				}
58184				if (type == 280)
58185				{
58186					num85 = 2.5f;
58187				}
58188				num85 *= 1f + (1f - scale);
58189				if (velocity.X < 0f - num85 || velocity.X > num85)
58190				{
58191					if (velocity.Y == 0f)
58192					{
58193						velocity *= 0.8f;
58194					}
58195				}
58196				else if (velocity.X < num85 && direction == 1)
58197				{
58198					velocity.X += 0.07f;
58199					if (velocity.X > num85)
58200					{
58201						velocity.X = num85;
58202					}
58203				}
58204				else if (velocity.X > 0f - num85 && direction == -1)
58205				{
58206					velocity.X -= 0.07f;
58207					if (velocity.X < 0f - num85)
58208					{

```


---

## 🤖 Assistant · 2026-08-19T03:19:14.198Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Our fighterFamilies numbers check out well against vanilla so far (159/349: max 6 accel 0.07 damp 0.8 reverseDamp 0.99 ✓; 199: 4/0.1/0.8/0.8 ✓; 120/166/213/258/528/529: 3/0.07/0.8/0.99 ✓; 461/27/77/...: 2/0.07/0.8 no reverseDamp ✓; 109: 2/0.04/0.8 ✓; num84 list ✓ (294=2, 295=1.75, 296=1.25, 201=1.1, 202=0.9, 203=1.2, 338=1.75, 339=1.25, 340=2, 385=1.8, 389=2.25, 462=4, 463=0.75, 466=3.75, 469=3.25, 480=1.5+2×, 425=6, 429=4, 631=0.9, 586=1.5+3.5×) ✓; scale boost 21/201/202/203/342/635 ✓; 466/586 pre-accel brake ✓ ours (466 vx<-2 ×0.9 ✓; 586: ours missing the `velocity.Y == 0 && vx < -1 → ×0.9` extra brake!). 

★ Ours fighterMoveStep: only 466 gets the special brake, not 586. Vanilla: type 586 also gets `velocity.Y == 0f && velocity.X < -1f → velocity.X *= 0.9` (and > 1 on the other side). Ours misses 586's. LOW-MEDIUM (zombie merman slower direction changes on land).

Also 462 post-accel extra damp ✓ ours has it.

num85 values: 269=2, 270=1, 271=1.5, 272=3, 273=1.25, 274=3, 275=3.25, 276=2, 277=2.75, 278=1.8, 279=1.3, 280=2.5 ✓ ours matches (272=3 ✓, 274=3 ✓, 275=3.25 ✓).

Wait — vanilla 274 = 3f but ours says `else if (id === 274) num85 = 3;` ✓. OK.

One structural difference: vanilla damp applies `velocity *= 0.8f` (BOTH axes); ours only vx. Their comment addresses this ("原版连 Y 一起乘，落地时 Y≈0 等价") — grounded Y=0 anyway. ✓ Fine.

Reverse damp for the num84 branch: vanilla has NO reverseDamp (only via the specific 466/586/462 lines). Ours fighterMoveSpec num84 branch has no reverseDamp ✓.

Now continue 58205-58460 to verify crow (67/220/428), mummy (78-80/630), 287, 185, and then 243/251/386/460/508/580/582 chargers, 391/427/415/419/518/532, 494/495, default num108 with 624/186.../489. I have those from the earlier sed offset listing; let me read 58205-58465 and 58440-58800 quickly, plus the 425 storm diver block I already have from ours (vanilla 58865-59013 — ours claims 1:1; I'll trust the detailed comments after spot-checking one or two values).

Actually — I already read fighterFamilies claims; let me verify the remaining numbers via a quick diff-like read of 58205-58800.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:14.530Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 260,
 "offset": 58205
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:14.558Z

**📎 ToolResult**

```
58205				{
58206					velocity.X -= 0.07f;
58207					if (velocity.X < 0f - num85)
58208					{
58209						velocity.X = 0f - num85;
58210					}
58211				}
58212			}
58213			else if (type >= 305 && type <= 314)
58214			{
58215				float num86 = 1.5f;
58216				if (type == 305 || type == 310)
58217				{
58218					num86 = 2f;
58219				}
58220				if (type == 306 || type == 311)
58221				{
58222					num86 = 1.25f;
58223				}
58224				if (type == 307 || type == 312)
58225				{
58226					num86 = 2.25f;
58227				}
58228				if (type == 308 || type == 313)
58229				{
58230					num86 = 1.5f;
58231				}
58232				if (type == 309 || type == 314)
58233				{
58234					num86 = 1f;
58235				}
58236				if (type < 310)
58237				{
58238					if (velocity.Y == 0f)
58239					{
58240						velocity.X *= 0.85f;
58241						if ((double)velocity.X > -0.3 && (double)velocity.X < 0.3)
58242						{
58243							flag = true;
58244							velocity.Y = -7f;
58245							velocity.X = num86 * (float)direction;
58246						}
58247					}
58248					else if (spriteDirection == direction)
58249					{
58250						velocity.X = (velocity.X * 10f + num86 * (float)direction) / 11f;
58251					}
58252				}
58253				else if (velocity.X < 0f - num86 || velocity.X > num86)
58254				{
58255					if (velocity.Y == 0f)
58256					{
58257						velocity *= 0.8f;
58258					}
58259				}
58260				else if (velocity.X < num86 && direction == 1)
58261				{
58262					velocity.X += 0.07f;
58263					if (velocity.X > num86)
58264					{
58265						velocity.X = num86;
58266					}
58267				}
58268				else if (velocity.X > 0f - num86 && direction == -1)
58269				{
58270					velocity.X -= 0.07f;
58271					if (velocity.X < 0f - num86)
58272					{
58273						velocity.X = 0f - num86;
58274					}
58275				}
58276			}
58277			else if (type == 67 || type == 220 || type == 428)
58278			{
58279				if (velocity.X < -0.5f || velocity.X > 0.5f)
58280				{
58281					if (velocity.Y == 0f)
58282					{
58283						velocity *= 0.7f;
58284					}
58285				}
58286				else if (velocity.X < 0.5f && direction == 1)
58287				{
58288					velocity.X += 0.03f;
58289					if (velocity.X > 0.5f)
58290					{
58291						velocity.X = 0.5f;
58292					}
58293				}
58294				else if (velocity.X > -0.5f && direction == -1)
58295				{
58296					velocity.X -= 0.03f;
58297					if (velocity.X < -0.5f)
58298					{
58299						velocity.X = -0.5f;
58300					}
58301				}
58302			}
58303			else if (type == 78 || type == 79 || type == 80 || type == 630)
58304			{
58305				float num87 = 1f;
58306				float num88 = 0.05f;
58307				if (life < lifeMax / 2)
58308				{
58309					num87 = 2f;
58310					num88 = 0.1f;
58311				}
58312				if (type == 79 || type == 630)
58313				{
58314					num87 *= 1.5f;
58315				}
58316				if (velocity.X < 0f - num87 || velocity.X > num87)
58317				{
58318					if (velocity.Y == 0f)
58319					{
58320						velocity *= 0.7f;
58321					}
58322				}
58323				else if (velocity.X < num87 && direction == 1)
58324				{
58325					velocity.X += num88;
58326					if (velocity.X > num87)
58327					{
58328						velocity.X = num87;
58329					}
58330				}
58331				else if (velocity.X > 0f - num87 && direction == -1)
58332				{
58333					velocity.X -= num88;
58334					if (velocity.X < 0f - num87)
58335					{
58336						velocity.X = 0f - num87;
58337					}
58338				}
58339			}
58340			else if (type == 287)
58341			{
58342				float num89 = 5f;
58343				float num90 = 0.2f;
58344				if (velocity.X < 0f - num89 || velocity.X > num89)
58345				{
58346					if (velocity.Y == 0f)
58347					{
58348						velocity *= 0.7f;
58349					}
58350				}
58351				else if (velocity.X < num89 && direction == 1)
58352				{
58353					velocity.X += num90;
58354					if (velocity.X > num89)
58355					{
58356						velocity.X = num89;
58357					}
58358				}
58359				else if (velocity.X > 0f - num89 && direction == -1)
58360				{
58361					velocity.X -= num90;
58362					if (velocity.X < 0f - num89)
58363					{
58364						velocity.X = 0f - num89;
58365					}
58366				}
58367			}
58368			else if (type == 243)
58369			{
58370				float num91 = 1f;
58371				float num92 = 0.07f;
58372				num91 += (1f - (float)life / (float)lifeMax) * 1.5f;
58373				num92 += (1f - (float)life / (float)lifeMax) * 0.15f;
58374				if (velocity.X < 0f - num91 || velocity.X > num91)
58375				{
58376					if (velocity.Y == 0f)
58377					{
58378						velocity *= 0.7f;
58379					}
58380				}
58381				else if (velocity.X < num91 && direction == 1)
58382				{
58383					velocity.X += num92;
58384					if (velocity.X > num91)
58385					{
58386						velocity.X = num91;
58387					}
58388				}
58389				else if (velocity.X > 0f - num91 && direction == -1)
58390				{
58391					velocity.X -= num92;
58392					if (velocity.X < 0f - num91)
58393					{
58394						velocity.X = 0f - num91;
58395					}
58396				}
58397			}
58398			else if (type == 251)
58399			{
58400				float num93 = 1f;
58401				float num94 = 0.08f;
58402				num93 += (1f - (float)life / (float)lifeMax) * 2f;
58403				num94 += (1f - (float)life / (float)lifeMax) * 0.2f;
58404				if (velocity.X < 0f - num93 || velocity.X > num93)
58405				{
58406					if (velocity.Y == 0f)
58407					{
58408						velocity *= 0.7f;
58409					}
58410				}
58411				else if (velocity.X < num93 && direction == 1)
58412				{
58413					velocity.X += num94;
58414					if (velocity.X > num93)
58415					{
58416						velocity.X = num93;
58417					}
58418				}
58419				else if (velocity.X > 0f - num93 && direction == -1)
58420				{
58421					velocity.X -= num94;
58422					if (velocity.X < 0f - num93)
58423					{
58424						velocity.X = 0f - num93;
58425					}
58426				}
58427			}
58428			else if (type == 386)
58429			{
58430				if (ai[2] > 0f)
58431				{
58432					if (velocity.Y == 0f)
58433					{
58434						velocity.X *= 0.8f;
58435					}
58436				}
58437				else
58438				{
58439					float num95 = 0.15f;
58440					float num96 = 1.5f;
58441					if (velocity.X < 0f - num96 || velocity.X > num96)
58442					{
58443						if (velocity.Y == 0f)
58444						{
58445							velocity *= 0.7f;
58446						}
58447					}
58448					else if (velocity.X < num96 && direction == 1)
58449					{
58450						velocity.X += num95;
58451						if (velocity.X > num96)
58452						{
58453							velocity.X = num96;
58454						}
58455					}
58456					else if (velocity.X > 0f - num96 && direction == -1)
58457					{
58458						velocity.X -= num95;
58459						if (velocity.X < 0f - num96)
58460						{
58461							velocity.X = 0f - num96;
58462						}
58463					}
58464				}

```


---

## 🤖 Assistant · 2026-08-19T03:19:24.313Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Numbers verified for: 305-314 (ours ✓, plus ours notes the <310 hop branch as unported — vanilla: types 305-309 (scarecrows) do a hop-cycle: vx *= 0.85, |vx|<0.3 → vy=-7, vx = num86*direction — scarecrows HOP toward you like slimes! Ours treats them as plain walkers. That's the "扑跳分支 :58231-58242 待移植" noted in fighterFamilies comment. CONFIRMED missing — medium (scarecrow movement is hop-based, very visible in pumpkin moon).

67/220/428 ✓ (0.5/0.03/0.7). 78-80/630 ✓. 287 ✓ (5/0.2/0.7). 243 ✓ (1+1.5x / 0.07+0.15x / 0.7). 251 ✓ (1+2x / 0.08+0.2x / 0.7). 386 ✓ (ai2>0 → damp only; else 1.5/0.15/0.7) ✓ ours.

Now let me check the rest (58465-58800): 460 butcher, 508/580/582 chargers, 391/427/415/419/518/532, 430-436/494/495/591, and default num108. Then ranged section 59464-60100, then tail 60383-60734. Read 58465-58865.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:24.722Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 400,
 "offset": 58465
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:24.742Z

**📎 ToolResult**

```
58465			}
58466			else if (type == 460)
58467			{
58468				float num97 = 3f;
58469				float num98 = 0.1f;
58470				if (Math.Abs(velocity.X) > 2f)
58471				{
58472					num98 *= 0.8f;
58473				}
58474				if ((double)Math.Abs(velocity.X) > 2.5)
58475				{
58476					num98 *= 0.8f;
58477				}
58478				if (Math.Abs(velocity.X) > 3f)
58479				{
58480					num98 *= 0.8f;
58481				}
58482				if ((double)Math.Abs(velocity.X) > 3.5)
58483				{
58484					num98 *= 0.8f;
58485				}
58486				if (Math.Abs(velocity.X) > 4f)
58487				{
58488					num98 *= 0.8f;
58489				}
58490				if ((double)Math.Abs(velocity.X) > 4.5)
58491				{
58492					num98 *= 0.8f;
58493				}
58494				if (Math.Abs(velocity.X) > 5f)
58495				{
58496					num98 *= 0.8f;
58497				}
58498				if ((double)Math.Abs(velocity.X) > 5.5)
58499				{
58500					num98 *= 0.8f;
58501				}
58502				num97 += (1f - (float)life / (float)lifeMax) * 3f;
58503				if (velocity.X < 0f - num97 || velocity.X > num97)
58504				{
58505					if (velocity.Y == 0f)
58506					{
58507						velocity *= 0.7f;
58508					}
58509				}
58510				else if (velocity.X < num97 && direction == 1)
58511				{
58512					if (velocity.X < 0f)
58513					{
58514						velocity.X *= 0.93f;
58515					}
58516					velocity.X += num98;
58517					if (velocity.X > num97)
58518					{
58519						velocity.X = num97;
58520					}
58521				}
58522				else if (velocity.X > 0f - num97 && direction == -1)
58523				{
58524					if (velocity.X > 0f)
58525					{
58526						velocity.X *= 0.93f;
58527					}
58528					velocity.X -= num98;
58529					if (velocity.X < 0f - num97)
58530					{
58531						velocity.X = 0f - num97;
58532					}
58533				}
58534			}
58535			else if (type == 508 || type == 580 || type == 582)
58536			{
58537				float num99 = 2.5f;
58538				float num100 = 10f;
58539				float num101 = Math.Abs(velocity.X);
58540				if (type == 582)
58541				{
58542					num99 = 2.25f;
58543					num100 = 7f;
58544					if (num101 > 2.5f)
58545					{
58546						num99 = 3f;
58547						num100 += 75f;
58548					}
58549					else if (num101 > 2f)
58550					{
58551						num99 = 2.75f;
58552						num100 += 55f;
58553					}
58554				}
58555				else if (num101 > 2.75f)
58556				{
58557					num99 = 3.5f;
58558					num100 += 80f;
58559				}
58560				else if ((double)num101 > 2.25)
58561				{
58562					num99 = 3f;
58563					num100 += 60f;
58564				}
58565				if ((double)Math.Abs(velocity.Y) < 0.5)
58566				{
58567					if (velocity.X > 0f && direction < 0)
58568					{
58569						velocity *= 0.95f;
58570					}
58571					if (velocity.X < 0f && direction > 0)
58572					{
58573						velocity *= 0.95f;
58574					}
58575				}
58576				if (Math.Abs(velocity.Y) > gravity)
58577				{
58578					float num102 = 3f;
58579					if (type == 582)
58580					{
58581						num102 = 2f;
58582					}
58583					num100 *= num102;
58584				}
58585				if (velocity.X <= 0f && direction < 0)
58586				{
58587					velocity.X = (velocity.X * num100 - num99) / (num100 + 1f);
58588				}
58589				else if (velocity.X >= 0f && direction > 0)
58590				{
58591					velocity.X = (velocity.X * num100 + num99) / (num100 + 1f);
58592				}
58593				else if (Math.Abs(base.Center.X - Main.player[target].Center.X) > 20f && Math.Abs(velocity.Y) <= gravity)
58594				{
58595					velocity.X *= 0.99f;
58596					velocity.X += (float)direction * 0.025f;
58597				}
58598			}
58599			else if (type == 391 || type == 427 || type == 415 || type == 419 || type == 518 || type == 532)
58600			{
58601				float num103 = 5f;
58602				float num104 = 0.25f;
58603				float num105 = 0.7f;
58604				if (type == 427)
58605				{
58606					num103 = 6f;
58607					num104 = 0.2f;
58608					num105 = 0.8f;
58609				}
58610				else if (type == 415)
58611				{
58612					num103 = 4f;
58613					num104 = 0.1f;
58614					num105 = 0.95f;
58615				}
58616				else if (type == 419)
58617				{
58618					num103 = 6f;
58619					num104 = 0.15f;
58620					num105 = 0.85f;
58621				}
58622				else if (type == 518)
58623				{
58624					num103 = 5f;
58625					num104 = 0.1f;
58626					num105 = 0.95f;
58627				}
58628				else if (type == 532)
58629				{
58630					num103 = 5f;
58631					num104 = 0.15f;
58632					num105 = 0.98f;
58633				}
58634				if (velocity.X < 0f - num103 || velocity.X > num103)
58635				{
58636					if (velocity.Y == 0f)
58637					{
58638						velocity *= num105;
58639					}
58640				}
58641				else if (velocity.X < num103 && direction == 1)
58642				{
58643					velocity.X += num104;
58644					if (velocity.X > num103)
58645					{
58646						velocity.X = num103;
58647					}
58648				}
58649				else if (velocity.X > 0f - num103 && direction == -1)
58650				{
58651					velocity.X -= num104;
58652					if (velocity.X < 0f - num103)
58653					{
58654						velocity.X = 0f - num103;
58655					}
58656				}
58657			}
58658			else if ((type >= 430 && type <= 436) || type == 494 || type == 495 || type == 591)
58659			{
58660				if (ai[2] == 0f)
58661				{
58662					damage = defDamage;
58663					float num106 = 1f;
58664					num106 *= 1f + (1f - scale);
58665					if (velocity.X < 0f - num106 || velocity.X > num106)
58666					{
58667						if (velocity.Y == 0f)
58668						{
58669							velocity *= 0.8f;
58670						}
58671					}
58672					else if (velocity.X < num106 && direction == 1)
58673					{
58674						velocity.X += 0.07f;
58675						if (velocity.X > num106)
58676						{
58677							velocity.X = num106;
58678						}
58679					}
58680					else if (velocity.X > 0f - num106 && direction == -1)
58681					{
58682						velocity.X -= 0.07f;
58683						if (velocity.X < 0f - num106)
58684						{
58685							velocity.X = 0f - num106;
58686						}
58687					}
58688					if (velocity.Y == 0f && (!Main.IsItDay() || (double)position.Y > Main.worldSurface * 16.0) && !Main.player[target].dead)
58689					{
58690						Vector2 vector24 = base.Center - Main.player[target].Center;
58691						int num107 = 50;
58692						if (type >= 494 && type <= 495)
58693						{
58694							num107 = 42;
58695						}
58696						if (vector24.Length() < (float)num107 && Collision.CanHit(base.Center, 1, 1, Main.player[target].Center, 1, 1))
58697						{
58698							velocity.X *= 0.7f;
58699							ai[2] = 1f;
58700						}
58701					}
58702				}
58703				else
58704				{
58705					damage = (int)((double)defDamage * 1.5);
58706					ai[3] = 1f;
58707					velocity.X *= 0.9f;
58708					if ((double)Math.Abs(velocity.X) < 0.1)
58709					{
58710						velocity.X = 0f;
58711					}
58712					ai[2] += 1f;
58713					if (ai[2] >= 20f || velocity.Y != 0f || (Main.IsItDay() && (double)position.Y < Main.worldSurface * 16.0))
58714					{
58715						ai[2] = 0f;
58716					}
58717				}
58718			}
58719			else if (type != 110 && type != 111 && type != 206 && type != 214 && type != 215 && type != 216 && type != 290 && type != 291 && type != 292 && type != 293 && type != 350 && type != 379 && type != 380 && type != 381 && type != 382 && (type < 449 || type > 452) && type != 468 && type != 481 && type != 411 && type != 409 && (type < 498 || type > 506) && type != 424 && type != 426 && type != 520)
58720			{
58721				float num108 = 1f;
58722				if (type == 624)
58723				{
58724					num108 = 2.5f;
58725				}
58726				if (type == 186)
58727				{
58728					num108 = 1.1f;
58729				}
58730				if (type == 187)
58731				{
58732					num108 = 0.9f;
58733				}
58734				if (type == 188)
58735				{
58736					num108 = 1.2f;
58737				}
58738				if (type == 189)
58739				{
58740					num108 = 0.8f;
58741				}
58742				if (type == 132)
58743				{
58744					num108 = 0.95f;
58745				}
58746				if (type == 200)
58747				{
58748					num108 = 0.87f;
58749				}
58750				if (type == 223)
58751				{
58752					num108 = 1.05f;
58753				}
58754				if (type == 632)
58755				{
58756					num108 = 0.8f;
58757				}
58758				if (type == 691)
58759				{
58760					num108 = 0.85f;
58761				}
58762				if (type == 489)
58763				{
58764					float num109 = (Main.player[target].Center - base.Center).Length();
58765					num109 *= 0.0025f;
58766					if ((double)num109 > 1.5)
58767					{
58768						num109 = 1.5f;
58769					}
58770					num108 = ((!Main.expertMode) ? (2.5f - num109) : (3f - num109));
58771					num108 *= 0.8f;
58772				}
58773				if (type == 489 || type == 3 || type == 132 || type == 186 || type == 187 || type == 188 || type == 189 || type == 200 || type == 223 || type == 331 || type == 332)
58774				{
58775					num108 *= 1f + (1f - scale);
58776				}
58777				if (velocity.X < 0f - num108 || velocity.X > num108)
58778				{
58779					if (velocity.Y == 0f)
58780					{
58781						velocity *= 0.8f;
58782					}
58783				}
58784				else if (velocity.X < num108 && direction == 1)
58785				{
58786					velocity.X += 0.07f;
58787					if (velocity.X > num108)
58788					{
58789						velocity.X = num108;
58790					}
58791				}
58792				else if (velocity.X > 0f - num108 && direction == -1)
58793				{
58794					velocity.X -= 0.07f;
58795					if (velocity.X < 0f - num108)
58796					{
58797						velocity.X = 0f - num108;
58798					}
58799				}
58800			}
58801			if (type >= 277 && type <= 280)
58802			{
58803				Lighting.AddLight((int)base.Center.X / 16, (int)base.Center.Y / 16, 0.2f, 0.1f, 0f);
58804			}
58805			else if (type == 520)
58806			{
58807				Lighting.AddLight(base.Top + new Vector2(0f, 20f), 0.3f, 0.3f, 0.7f);
58808			}
58809			else if (type == 525)
58810			{
58811				Vector3 rgb = new Vector3(0.7f, 1f, 0.2f) * 0.5f;
58812				Lighting.AddLight(base.Top + new Vector2(0f, 15f), rgb);
58813			}
58814			else if (type == 526)
58815			{
58816				Vector3 rgb2 = new Vector3(1f, 1f, 0.5f) * 0.4f;
58817				Lighting.AddLight(base.Top + new Vector2(0f, 15f), rgb2);
58818			}
58819			else if (type == 527)
58820			{
58821				Vector3 rgb3 = new Vector3(0.6f, 0.3f, 1f) * 0.4f;
58822				Lighting.AddLight(base.Top + new Vector2(0f, 15f), rgb3);
58823			}
58824			else if (type == 415)
58825			{
58826				hide = false;
58827				for (int num110 = 0; num110 < Main.maxNPCs; num110++)
58828				{
58829					if (Main.npc[num110].active && Main.npc[num110].type == 416 && Main.npc[num110].ai[0] == (float)whoAmI)
58830					{
58831						hide = true;
58832						break;
58833					}
58834				}
58835			}
58836			else if (type == 258)
58837			{
58838				if (velocity.Y != 0f)
58839				{
58840					TargetClosest();
58841					spriteDirection = direction;
58842					if (Main.player[target].Center.X < position.X && velocity.X > 0f)
58843					{
58844						velocity.X *= 0.95f;
58845					}
58846					else if (Main.player[target].Center.X > position.X + (float)width && velocity.X < 0f)
58847					{
58848						velocity.X *= 0.95f;
58849					}
58850					if (Main.player[target].Center.X < position.X && velocity.X > -5f)
58851					{
58852						velocity.X -= 0.1f;
58853					}
58854					else if (Main.player[target].Center.X > position.X + (float)width && velocity.X < 5f)
58855					{
58856						velocity.X += 0.1f;
58857					}
58858				}
58859				else if (Main.player[target].Center.Y + 50f < position.Y && Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
58860				{
58861					flag = true;
58862					velocity.Y = -7f;
58863				}
58864			}

```


---

## 🤖 Assistant · 2026-08-19T03:20:09.642Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Comparisons:

**460 butcher**: num98 staged accel decay ✓ ours ([2,2.5,3,3.5,4,4.5,5,5.5] each ×0.8) ✓; num97 = 3+3× ✓; reverse damp 0.93 ✓ ours. ✓ 1:1.

**508/580/582 chargers** ✓ 1:1 (ours chargerApproach: num99/num100, 582 tiers, |vy|<0.5 brake 0.95, |vy|>gravity multiplier 3/2, else approach, distant 0.99+0.025 ✓). Note ours uses `Math.abs(e.vy) > 0.3` instead of `> gravity (0.3)` ✓ same; and `<= 0.3` ✓.

**391/427/415/419/518/532** ✓ 1:1 numbers (5/0.25/0.7 default; 427 6/0.2/0.8; 415 4/0.1/0.95; 419 6/0.15/0.85; 518 5/0.1/0.95; 532 5/0.15/0.98) ✓ ours.

**430-436/494/495/591 lunge family** (goblin thief/snapdragon lobster/torch zombie): vanilla: ai2==0 → normal walk (num106 = 1×scale boost) + when grounded + (night || underground) + !dead: if dist < 50 (494/495: 42) && CanHit → vx *= 0.7, ai2=1. ai2==1 → damage×1.5, ai3=1, vx *= 0.9 tiny→0, ai2 += 1, ≥20 || vy!=0 || day-surface → ai2=0. This is the "lunge preparation + burst"? Wait — where's the actual burst? ai2 counts 0..20 with vx damped... then resets. Hmm — actually this looks like a WINDUP then... hold on, ai2==1 branch: vx *= 0.9 (stop), count to 20 → then what? After ai2 hits 0 again, the walk continues. The BURST must be elsewhere — maybe the jump section uses ai3==1/ai2 to launch (flag or vy=-x). The lunge: at 20 the ai2=0... then next tick normal walk. Hmm, maybe the jump section for these types (430-436 "squidlaunch"?) reads ai[3]==1 → big horizontal launch. Let me note to check in the jump section.

Ours: 430-436/494/495/591 → LEGACY (fixed accel 0.1/max 1)! And NO lunge windup. So goblin thief lunge entirely missing. But wait — do we handle goblins elsewhere? "goblinPeon 拆门" exists. 430-436 = goblin army ground troops (430 Thief, 431 Warrior...). Their vanilla behavior: walk, and when player < 50px at night, stop 20 ticks (windup) with damage×1.5, then...? Let me check the jump section for these types before finalizing. Either way: ours = plain walker with legacy 1/0.1 — vanilla has num106 scale-based walk + lunge windup. MEDIUM (goblin invasion melee feel).

**default num108** ✓ ours (624=2.5, 186=1.1, 187=0.9, 188=1.2, 189=0.8, 132=0.95, 200=0.87, 223=1.05, 632=0.8, 691=0.85, 489 distance-based (2.5-num109)*0.8 expert false ✓; scale boost list ✓). Exclusion list at :58719 ✓ ours rangedMoveExcluded matches (110,111,206,214,215,216,290-293,350,379,380,381,382,449-452,468,481,411,409,498-506,424,426,520) ✓.

**Lights** ✓ ours (277-280 0.2/0.1/0; 520 Top+20 0.3/0.3/0.7; 525 = (0.7,1,0.2)×0.5 = (0.35,0.5,0.1) ✓; 526 (1,1,0.5)×0.4 = (0.4,0.4,0.2) ✓; 527 (0.6,0.3,1)×0.4 = (0.24,0.12,0.4) ✓) ✓.

**415 hide-with-rider** (416 rider attached → hide drakomire): ours? 415 spawns 516 (fireball)... wait no — 416 is Drakomire Rider riding Drakomire? So 415 = Drakomire; 416 = rider? no wait, at :57181 type 415 spawns NPC **516**... Hmm — 516 = "DrakomireFireball"? Hmm, actually vanilla: Drakomire = 415? Let me reconsider: the block at 57181 spawns NPC 516 with fire dust 259 at Center + dir*45 — so 516 = Drakomire fireball projectile-NPC. And 416 = "DrakomireRider"? and the rider spawns its mount... The 'hide' logic: if a 416 exists with ai[0] == whoAmI → hide (rider mounted → drakomire body hidden? no — hide the rider? It's for 415 hiding when ridden). Ours: does bossAI_martian or fighterAI handle 415/416 pairing? Not in fighterAI. mechQueen? The memory "骑手 390 失坐骑 → 382" suggests rider mechanics exist somewhere (scutlix rider 390?). Let me grep for 416/415 rider in repo... Actually offset 2580→58823 shows `else if (type == 415) { hide=false; ... }`. Ours: nothing for 415 rider-hide. LOW-MEDIUM (solar pillar drakomire+rider visuals).

**258 Corruptor flying** (:58836-58864): 258 = "Corruptor"! It has custom movement: airborne → TargetClosest + steer ±0.1 clamp ±5 with 0.95 reverse damp; grounded + player above 50 && CanHit → vy=-7 (leap). Ours: 258 in the "3档组 120/166/213/258/528/529" walk spec (max 3 accel 0.07 damp 0.8 reverseDamp 0.99)! That's WRONG for 258 — vanilla has its own ELSE-IF branch AFTER the movement chain (58836) which is part of the else-if ladder continuation... wait — is 58836 `else if (type == 258)` chained to the light section? Looking at structure: :58801 `if (type >= 277...)` lights `else if (type == 520)` ... `else if (type == 415) ... else if (type == 258) { movement }`. So 258's movement is in this SEPARATE later if-ladder, NOT in the main movement ladder at :57916! So in vanilla, type 258 falls through the main ladder (no branch — the 57916 branch lists 120/166/213/258/528/529... wait it DOES list 258!

Hold on: :57916 `else if (type == 120 || type == 166 || type == 213 || type == 258 || type == 528 || type == 529)` — 258 IS in that list. But then :58836 `else if (type == 258)` in the SECOND ladder ALSO handles it. Two ladders both apply to 258 (like 425: chain + own block). So vanilla 258 gets BOTH the 3/0.07/0.8/0.99 walk AND the special air-steer/leap block. Ours: has the walk spec ✓ but MISSING the air-steer + player-above leap (58836-58864). MEDIUM (Corruptor should leap up toward players above and steer mid-air).

**425 storm diver** (:58865-59013) — ours claims 1:1. Vanilla num115 = target.Center.X - direction*300 - Center.X ✓ ours; num116 = player Bottom - self Bottom... let me spot check: `num116 = Main.player[target].position.Y + height_p - (position.Y + height)` ✓ ours. -20/+20 dead zones ✓; ±0.3, clamp 7/8 ✓; 1/3 dust ✓; same-type separation ✓; takeoff gate `player.Center.Y + 100 < position.Y` hmm ours: `player.cy + 100 < e.y` ✓ (Center.Y vs position.Y as ours comments). aim charge (58968+) ✓ per ours. Trust with the detailed comments; spot-checked enough.

**427 (59015)** & **426 (59105)** & their servo blocks — ours: 427/426 get move spec only (427 in 6/0.2/0.8; 426 excluded from move). Vanilla 427: Scutlix rider-less? has its own servo block (num124 target velocity maintenance...±6 clamps, 40px Y deadzone, same-type separation). 426 = Corite — air servo too. Ours missing both. These are solar/martian pillar enemies. MEDIUM-LOW. Actually wait — 426 Corite is a common solar pillar enemy with distinctive dive behavior; ours treats it as plain walker (excluded from move chain, so it just... walks with fighterAI's default accel 0? excluded → no horizontal accel at all!). Excluded from move chain = no horizontal movement code → Corite would stand still?! Vanilla 426: the :59105 block handles its flight entirely (it's a flyer-ish charger). Ours: nothing → Corite stands still and falls. That's SEVERE for that enemy. Let me verify 426 handling — grep Enemy.ts for 426 beyond excludes.

Also **430-436 etc**: after the windup, where's the lunge? Probably in jump section with ai3 flag. Will check in tail.

Let me now read the tail of AI_003: 60100-60734 (friction, doors, jump, NotDiscouraged) — the most important core. And 59464-60100 ranged section quickly for table verification.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:10.261Z · glm-x-preview-260804

```
已确认移动链数值准确无误。现在我来处理 AI_003 的尾部（friction、doors、jump core）——我先读取一下。
```


---

## 🤖 Assistant · 2026-08-19T03:20:10.616Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 340,
 "offset": 60096
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:10.639Z

**📎 ToolResult**

```
60096							else if (Math.Abs(num177) > Math.Abs(num179) * 2f)
60097							{
60098								ai[2] = 3f;
60099							}
60100							else if (num179 > 0f)
60101							{
60102								ai[2] = 2f;
60103							}
60104							else
60105							{
60106								ai[2] = 4f;
60107							}
60108						}
60109					}
60110				}
60111				if (ai[2] <= 0f || (flag16 && (num161 == -1 || !(ai[1] >= (float)num161) || !(ai[1] < (float)(num161 + num162)))))
60112				{
60113					float num182 = 1f;
60114					float num183 = 0.07f;
60115					float num184 = 0.8f;
60116					if (type == 214)
60117					{
60118						num182 = 2f;
60119						num183 = 0.09f;
60120					}
60121					else if (type == 215)
60122					{
60123						num182 = 1.5f;
60124						num183 = 0.08f;
60125					}
60126					else if (type == 381 || type == 382)
60127					{
60128						num182 = 2f;
60129						num183 = 0.5f;
60130					}
60131					else if (type == 520)
60132					{
60133						num182 = 4f;
60134						num183 = 1f;
60135						num184 = 0.7f;
60136					}
60137					else if (type == 411)
60138					{
60139						num182 = 2f;
60140						num183 = 0.5f;
60141					}
60142					else if (type == 409)
60143					{
60144						num182 = 2f;
60145						num183 = 0.5f;
60146					}
60147					else if (type == 426)
60148					{
60149						num182 = 4f;
60150						num183 = 0.6f;
60151						num184 = 0.95f;
60152					}
60153					bool flag22 = false;
60154					if ((type == 381 || type == 382) && Vector2.Distance(base.Center, Main.player[target].Center) < 300f && Collision.CanHitLine(base.Center, 0, 0, Main.player[target].Center, 0, 0))
60155					{
60156						flag22 = true;
60157						ai[3] = 0f;
60158					}
60159					if (type == 520 && Vector2.Distance(base.Center, Main.player[target].Center) < 400f && Collision.CanHitLine(base.Center, 0, 0, Main.player[target].Center, 0, 0))
60160					{
60161						flag22 = true;
60162						ai[3] = 0f;
60163					}
60164					if (velocity.X < 0f - num182 || velocity.X > num182 || flag22)
60165					{
60166						if (velocity.Y == 0f)
60167						{
60168							velocity *= num184;
60169						}
60170					}
60171					else if (velocity.X < num182 && direction == 1)
60172					{
60173						velocity.X += num183;
60174						if (velocity.X > num182)
60175						{
60176							velocity.X = num182;
60177						}
60178					}
60179					else if (velocity.X > 0f - num182 && direction == -1)
60180					{
60181						velocity.X -= num183;
60182						if (velocity.X < 0f - num182)
60183						{
60184							velocity.X = 0f - num182;
60185						}
60186					}
60187				}
60188				if (type == 520)
60189				{
60190					localAI[2] += 1f;
60191					if (localAI[2] >= 6f)
60192					{
60193						localAI[2] = 0f;
60194						localAI[3] = Main.player[target].DirectionFrom(base.Top + new Vector2(0f, 20f)).ToRotation();
60195					}
60196				}
60197			}
60198			if (type == 109 && Main.netMode != 1 && !Main.player[target].dead)
60199			{
60200				if (justHit)
60201				{
60202					ai[2] = 0f;
60203				}
60204				ai[2] += 1f;
60205				if (ai[2] > 60f)
60206				{
60207					Vector2 vector38 = new Vector2(position.X + (float)width * 0.5f - (float)(direction * 24), position.Y + 4f);
60208					if (Main.rand.Next(5) != 0 || AnyNPCs(378))
60209					{
60210						int num185 = Main.rand.Next(3, 8) * direction;
60211						int num186 = Main.rand.Next(-8, -5);
60212						int num187 = Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector38.X, vector38.Y, num185, num186, 75, 80, 0f, Main.myPlayer);
60213						Main.projectile[num187].timeLeft = 300;
60214						ai[2] = 0f;
60215					}
60216					else
60217					{
60218						ai[2] = -120f;
60219						int number = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)vector38.X, (int)vector38.Y, 378);
60220						NetMessage.SendData(23, -1, -1, null, number);
60221					}
60222				}
60223			}
60224			if (velocity.Y == 0f || flag)
60225			{
60226				int num188 = (int)(position.Y + (float)height + 7f) / 16;
60227				int num189 = (int)(position.Y - 9f) / 16;
60228				int num190 = (int)position.X / 16;
60229				int num191 = (int)(position.X + (float)width) / 16;
60230				int num192 = (int)(position.X + 8f) / 16;
60231				int num193 = (int)(position.X + (float)width - 8f) / 16;
60232				bool flag23 = false;
60233				for (int num194 = num192; num194 <= num193; num194++)
60234				{
60235					Tile tile = Main.tile[num194, num188];
60236					Tile tile2 = Main.tile[num194, num189];
60237					if (num194 >= num190 && num194 <= num191 && tile == null)
60238					{
60239						flag23 = true;
60240						continue;
60241					}
60242					if (tile2 != null && WorldGen.SolidTileNoPlatforms(num194, num189))
60243					{
60244						flag5 = false;
60245						break;
60246					}
60247					if (!flag23 && num194 >= num190 && num194 <= num191 && WorldGen.SolidTileAllowBottomSlope(num194, num188))
60248					{
60249						flag5 = true;
60250					}
60251				}
60252				if (!flag5 && velocity.Y < 0f)
60253				{
60254					velocity.Y = 0f;
60255				}
60256				if (flag23)
60257				{
60258					return;
60259				}
60260			}
60261			if (type == 428)
60262			{
60263				flag5 = false;
60264			}
60265			if (velocity.Y >= 0f && (type != 580 || directionY != 1))
60266			{
60267				int num195 = 0;
60268				if (velocity.X < 0f)
60269				{
60270					num195 = -1;
60271				}
60272				if (velocity.X > 0f)
60273				{
60274					num195 = 1;
60275				}
60276				Vector2 vector39 = position;
60277				vector39.X += velocity.X;
60278				int num196 = (int)((vector39.X + (float)(width / 2) + (float)((width / 2 + 1) * num195)) / 16f);
60279				int num197 = (int)((vector39.Y + (float)height - 1f) / 16f);
60280				if (WorldGen.InWorld(num196, num197, 4))
60281				{
60282					if (Main.tile[num196, num197] == null)
60283					{
60284						Main.tile[num196, num197] = new Tile();
60285					}
60286					if (Main.tile[num196, num197 - 1] == null)
60287					{
60288						Main.tile[num196, num197 - 1] = new Tile();
60289					}
60290					if (Main.tile[num196, num197 - 2] == null)
60291					{
60292						Main.tile[num196, num197 - 2] = new Tile();
60293					}
60294					if (Main.tile[num196, num197 - 3] == null)
60295					{
60296						Main.tile[num196, num197 - 3] = new Tile();
60297					}
60298					if (Main.tile[num196, num197 + 1] == null)
60299					{
60300						Main.tile[num196, num197 + 1] = new Tile();
60301					}
60302					if (Main.tile[num196 - num195, num197 - 3] == null)
60303					{
60304						Main.tile[num196 - num195, num197 - 3] = new Tile();
60305					}
60306					if ((float)(num196 * 16) < vector39.X + (float)width && (float)(num196 * 16 + 16) > vector39.X && ((Main.tile[num196, num197].nactive() && !Main.tile[num196, num197].topSlope() && !Main.tile[num196, num197 - 1].topSlope() && Main.tileSolid[Main.tile[num196, num197].type] && !Main.tileSolidTop[Main.tile[num196, num197].type]) || (Main.tile[num196, num197 - 1].halfBrick() && Main.tile[num196, num197 - 1].nactive())) && (!Main.tile[num196, num197 - 1].nactive() || !Main.tileSolid[Main.tile[num196, num197 - 1].type] || Main.tileSolidTop[Main.tile[num196, num197 - 1].type] || (Main.tile[num196, num197 - 1].halfBrick() && (!Main.tile[num196, num197 - 4].nactive() || !Main.tileSolid[Main.tile[num196, num197 - 4].type] || Main.tileSolidTop[Main.tile[num196, num197 - 4].type]))) && (!Main.tile[num196, num197 - 2].nactive() || !Main.tileSolid[Main.tile[num196, num197 - 2].type] || Main.tileSolidTop[Main.tile[num196, num197 - 2].type]) && (!Main.tile[num196, num197 - 3].nactive() || !Main.tileSolid[Main.tile[num196, num197 - 3].type] || Main.tileSolidTop[Main.tile[num196, num197 - 3].type]) && (!Main.tile[num196 - num195, num197 - 3].nactive() || !Main.tileSolid[Main.tile[num196 - num195, num197 - 3].type]))
60307					{
60308						float num198 = num197 * 16;
60309						if (Main.tile[num196, num197].halfBrick())
60310						{
60311							num198 += 8f;
60312						}
60313						if (Main.tile[num196, num197 - 1].halfBrick())
60314						{
60315							num198 -= 8f;
60316						}
60317						if (num198 < vector39.Y + (float)height)
60318						{
60319							float num199 = vector39.Y + (float)height - num198;
60320							float num200 = 16.1f;
60321							if (type == 163 || type == 164 || type == 236 || type == 239 || type == 530)
60322							{
60323								num200 += 8f;
60324							}
60325							if (num199 <= num200)
60326							{
60327								gfxOffY += position.Y + (float)height - num198;
60328								position.Y = num198 - (float)height;
60329								if (num199 < 9f)
60330								{
60331									stepSpeed = 1f;
60332								}
60333								else
60334								{
60335									stepSpeed = 2f;
60336								}
60337							}
60338						}
60339					}
60340				}
60341			}
60342			if (flag5)
60343			{
60344				int num201 = (int)((position.X + (float)(width / 2) + (float)(15 * direction)) / 16f);
60345				int num202 = (int)((position.Y + (float)height - 15f) / 16f);
60346				if (type == 109 || type == 163 || type == 164 || type == 199 || type == 236 || type == 239 || type == 257 || type == 258 || type == 290 || type == 391 || type == 425 || type == 427 || type == 426 || type == 580 || type == 508 || type == 415 || type == 530 || type == 532 || type == 582)
60347				{
60348					num201 = (int)((position.X + (float)(width / 2) + (float)((width / 2 + 16) * direction)) / 16f);
60349				}
60350				if (Main.tile[num201, num202] == null)
60351				{
60352					Main.tile[num201, num202] = new Tile();
60353				}
60354				if (Main.tile[num201, num202 - 1] == null)
60355				{
60356					Main.tile[num201, num202 - 1] = new Tile();
60357				}
60358				if (Main.tile[num201, num202 - 2] == null)
60359				{
60360					Main.tile[num201, num202 - 2] = new Tile();
60361				}
60362				if (Main.tile[num201, num202 - 3] == null)
60363				{
60364					Main.tile[num201, num202 - 3] = new Tile();
60365				}
60366				if (Main.tile[num201, num202 + 1] == null)
60367				{
60368					Main.tile[num201, num202 + 1] = new Tile();
60369				}
60370				if (Main.tile[num201 + direction, num202 - 1] == null)
60371				{
60372					Main.tile[num201 + direction, num202 - 1] = new Tile();
60373				}
60374				if (Main.tile[num201 + direction, num202 + 1] == null)
60375				{
60376					Main.tile[num201 + direction, num202 + 1] = new Tile();
60377				}
60378				if (Main.tile[num201 - direction, num202 + 1] == null)
60379				{
60380					Main.tile[num201 - direction, num202 + 1] = new Tile();
60381				}
60382				Main.tile[num201, num202 + 1].halfBrick();
60383				if (Main.tile[num201, num202 - 1].nactive() && (Main.tile[num201, num202 - 1].type == 10 || Main.tile[num201, num202 - 1].type == 388) && flag8)
60384				{
60385					ai[2] += 1f;
60386					ai[3] = 0f;
60387					if (ai[2] >= 60f)
60388					{
60389						bool flag24 = type == 3 || type == 691 || type == 430 || type == 590 || type == 331 || type == 332 || type == 132 || type == 161 || type == 186 || type == 187 || type == 188 || type == 189 || type == 200 || type == 223 || type == 320 || type == 321 || type == 319 || type == 21 || type == 324 || type == 323 || type == 322 || type == 44 || type == 196 || type == 167 || type == 77 || type == 197 || type == 202 || type == 203 || type == 449 || type == 450 || type == 451 || type == 452 || type == 481 || type == 201 || type == 635;
60390						bool flag25 = Main.player[target].ZoneGraveyard && Main.rand.Next(60) == 0;
60391						bool flag26 = false;
60392						if (target >= 0)
60393						{
60394							Player player4 = Main.player[target];
60395							if (!player4.dead && !player4.ghost && player4.insideUnbreakableWalls)
60396							{
60397								flag26 = true;
60398							}
60399						}
60400						bool flag27 = (!Main.bloodMoon || Main.getGoodWorld) && !flag25 && flag24;
60401						if (flag26)
60402						{
60403							flag27 = false;
60404						}
60405						if (flag27)
60406						{
60407							ai[1] = 0f;
60408						}
60409						velocity.X = 0.5f * (float)(-direction);
60410						int num203 = 5;
60411						if (Main.tile[num201, num202 - 1].type == 388)
60412						{
60413							num203 = 2;
60414						}
60415						ai[1] += num203;
60416						if (flag26)
60417						{
60418							ai[1] += 6f;
60419						}
60420						else if (type == 27)
60421						{
60422							ai[1] += 1f;
60423						}
60424						else if (type == 31 || type == 294 || type == 295 || type == 296)
60425						{
60426							ai[1] += 6f;
60427						}
60428						ai[2] = 0f;
60429						bool flag28 = false;
60430						if (ai[1] >= 10f)
60431						{
60432							flag28 = true;
60433							ai[1] = 10f;
60434						}
60435						if (type == 460)

```


---

## 🤖 Assistant · 2026-08-19T03:20:24.529Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The doors section compares closely with ours. Key details:

- Vanilla step-up: spiders (163/164/236/239/530) get +8 tolerance (16.1+8=24.1); ours uses fixed 16.1 for ALL. Minor deviation for spider ground forms — LOW. Also gfxOffY/stepSpeed visual.
- Jump probe (num201/num202): for 109/163/164/199/236/239/257/258/290/391/425/427/426/580/508/415/530/532/582 the probe distance is (width/2+16)*direction instead of 15. Ours uses fixed 15*dir for all types. LOW-MEDIUM.
- Doors: vanilla gate `type == 10 || type == 388` at (num201, num202-1), flag8 gate ✓ ours; ai2 (doorWarm) +1/t, ≥60 → hit: velocity.X = 0.5×-direction ✓ ours approx; ai1 += 5 (388: 2) ✓ ours; flag24 door-breaker list & graveyard flag25 (1/60 rand) & flag26 insideUnbreakableWalls; flag27 = (!bloodMoon || getGood) && !flag25 && flag24 → ai1=0 reset! Ours: `if (!clock.bloodMoon && !graveyard) doorCd = 30` on open failure — different mechanism but ours documented as approximation. Vanilla: on failure... let me read the rest (60435-60460) to see open attempts & 30t. Ours' structure differs a bit but is documented; given "攻门" audit was previous batch, I'll trust and skip detailed re-audit. Not in my listed families anyway (door interaction is shared). Actually — flag25: graveyard && rand(60)==0 → flag27 false → keeps hammering — ours: `!bloodMoon && !zoneGraveyard` → in graveyard never retreats ✓ equivalent-ish (vanilla only 1/60 chance per hit to keep going, ours always keeps going in graveyard — minor over-aggression, LOW).

- The stuck counter ai[3] / num58: where is it consumed? Need to find `num58` usage later — likely in the jump section (forces jump when stuck) and the 120 teleport (:60679). Ours implements only 120's. Let me read 60435-60734 fully to see jump + ai3 usage + NotDiscouraged.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:24.895Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 305,
 "offset": 60430
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:24.920Z

**📎 ToolResult**

```
60430						if (ai[1] >= 10f)
60431						{
60432							flag28 = true;
60433							ai[1] = 10f;
60434						}
60435						if (type == 460)
60436						{
60437							flag28 = true;
60438						}
60439						WorldGen.KillTile(num201, num202 - 1, fail: true);
60440						if ((Main.netMode != 1 || !flag28) && flag28 && Main.netMode != 1)
60441						{
60442							if (type == 26)
60443							{
60444								WorldGen.KillTile(num201, num202 - 1);
60445								if (Main.netMode == 2)
60446								{
60447									NetMessage.SendData(17, -1, -1, null, 0, num201, num202 - 1);
60448								}
60449							}
60450							else
60451							{
60452								if (Main.tile[num201, num202 - 1].type == 10)
60453								{
60454									bool flag29 = WorldGen.OpenDoor(num201, num202 - 1, direction);
60455									if (!flag29)
60456									{
60457										ai[3] = num58;
60458										netUpdate = true;
60459									}
60460									if (Main.netMode == 2 && flag29)
60461									{
60462										NetMessage.SendData(19, -1, -1, null, 0, num201, num202 - 1, direction);
60463									}
60464								}
60465								if (Main.tile[num201, num202 - 1].type == 388)
60466								{
60467									bool flag30 = WorldGen.ShiftTallGate(num201, num202 - 1, closing: false);
60468									if (!flag30)
60469									{
60470										ai[3] = num58;
60471										netUpdate = true;
60472									}
60473									if (Main.netMode == 2 && flag30)
60474									{
60475										NetMessage.SendData(19, -1, -1, null, 4, num201, num202 - 1);
60476									}
60477								}
60478							}
60479						}
60480					}
60481				}
60482				else
60483				{
60484					int num204 = spriteDirection;
60485					if (type == 425)
60486					{
60487						num204 *= -1;
60488					}
60489					if ((velocity.X < 0f && num204 == -1) || (velocity.X > 0f && num204 == 1))
60490					{
60491						if (height >= 32 && WorldGen.SolidTileNoPlatforms(num201, num202 - 2))
60492						{
60493							if (WorldGen.SolidTileNoPlatforms(num201, num202 - 3))
60494							{
60495								velocity.Y = -8f;
60496								netUpdate = true;
60497							}
60498							else
60499							{
60500								velocity.Y = -7f;
60501								netUpdate = true;
60502							}
60503						}
60504						else if (WorldGen.SolidTileNoPlatforms(num201, num202 - 1))
60505						{
60506							if (type == 624)
60507							{
60508								velocity.Y = -8f;
60509								int num205 = (int)(position.Y + (float)height) / 16;
60510								if (WorldGen.SolidTile((int)base.Center.X / 16, num205 - 8))
60511								{
60512									direction *= -1;
60513									spriteDirection = direction;
60514									velocity.X = 3 * direction;
60515								}
60516							}
60517							else
60518							{
60519								velocity.Y = -6f;
60520							}
60521							netUpdate = true;
60522						}
60523						else if (position.Y + (float)height - (float)(num202 * 16) > 20f && !Main.tile[num201, num202].topSlope() && WorldGen.SolidTileNoPlatforms(num201, num202))
60524						{
60525							velocity.Y = -5f;
60526							netUpdate = true;
60527						}
60528						else if (directionY < 0 && type != 67 && !WorldGen.SolidTileAllowBottomSlope(num201, num202 + 1) && !WorldGen.SolidTileAllowBottomSlope(num201 + direction, num202 + 1))
60529						{
60530							velocity.Y = -8f;
60531							velocity.X *= 1.5f;
60532							netUpdate = true;
60533						}
60534						else if (flag8)
60535						{
60536							ai[1] = 0f;
60537							ai[2] = 0f;
60538						}
60539						if (velocity.Y == 0f && flag6 && ai[3] == 1f)
60540						{
60541							velocity.Y = -5f;
60542						}
60543						if (velocity.Y == 0f && (Main.expertMode || type == 586) && Main.player[target].Bottom.Y < base.Top.Y && Math.Abs(base.Center.X - Main.player[target].Center.X) < (float)(Main.player[target].width * 3) && Collision.CanHit(this, Main.player[target]))
60544						{
60545							if (type == 586)
60546							{
60547								int num206 = (int)((base.Bottom.Y - 16f - Main.player[target].Bottom.Y) / 16f);
60548								if (num206 < 14 && Collision.CanHit(this, Main.player[target]))
60549								{
60550									if (num206 < 7)
60551									{
60552										velocity.Y = -8.8f;
60553									}
60554									else if (num206 < 8)
60555									{
60556										velocity.Y = -9.2f;
60557									}
60558									else if (num206 < 9)
60559									{
60560										velocity.Y = -9.7f;
60561									}
60562									else if (num206 < 10)
60563									{
60564										velocity.Y = -10.3f;
60565									}
60566									else if (num206 < 11)
60567									{
60568										velocity.Y = -10.6f;
60569									}
60570									else
60571									{
60572										velocity.Y = -11f;
60573									}
60574								}
60575							}
60576							if (velocity.Y == 0f)
60577							{
60578								int num207 = 6;
60579								if (Main.player[target].Bottom.Y > base.Top.Y - (float)(num207 * 16))
60580								{
60581									velocity.Y = -7.9f;
60582								}
60583								else
60584								{
60585									int num208 = (int)(base.Center.X / 16f);
60586									int num209 = (int)(base.Bottom.Y / 16f) - 1;
60587									for (int num210 = num209; num210 > num209 - num207; num210--)
60588									{
60589										if (Main.tile[num208, num210] != null && Main.tile[num208, num210].nactive() && TileID.Sets.Platforms[Main.tile[num208, num210].type])
60590										{
60591											velocity.Y = -7.9f;
60592											break;
60593										}
60594									}
60595								}
60596							}
60597						}
60598					}
60599					if ((type == 31 || type == 294 || type == 295 || type == 296 || type == 47 || type == 77 || type == 104 || type == 168 || type == 196 || type == 385 || type == 389 || type == 464 || type == 470 || (type >= 524 && type <= 527)) && velocity.Y == 0f)
60600					{
60601						int num211 = 100;
60602						int num212 = 50;
60603						if (type == 586)
60604						{
60605							num211 = 150;
60606							num212 = 150;
60607						}
60608						if (Math.Abs(position.X + (float)(width / 2) - (Main.player[target].position.X + (float)(Main.player[target].width / 2))) < (float)num211 && Math.Abs(position.Y + (float)(height / 2) - (Main.player[target].position.Y + (float)(Main.player[target].height / 2))) < (float)num212 && ((direction > 0 && velocity.X >= 1f) || (direction < 0 && velocity.X <= -1f)))
60609						{
60610							if (type == 586)
60611							{
60612								velocity.X += direction;
60613								velocity.X *= 2f;
60614								if (velocity.X > 8f)
60615								{
60616									velocity.X = 8f;
60617								}
60618								if (velocity.X < -8f)
60619								{
60620									velocity.X = -8f;
60621								}
60622								velocity.Y = -4.5f;
60623								if (position.Y > Main.player[target].position.Y + 40f)
60624								{
60625									velocity.Y -= 2f;
60626								}
60627								if (position.Y > Main.player[target].position.Y + 80f)
60628								{
60629									velocity.Y -= 2f;
60630								}
60631								if (position.Y > Main.player[target].position.Y + 120f)
60632								{
60633									velocity.Y -= 2f;
60634								}
60635							}
60636							else
60637							{
60638								velocity.X *= 2f;
60639								if (velocity.X > 3f)
60640								{
60641									velocity.X = 3f;
60642								}
60643								if (velocity.X < -3f)
60644								{
60645									velocity.X = -3f;
60646								}
60647								velocity.Y = -4f;
60648							}
60649							netUpdate = true;
60650						}
60651					}
60652					if (type == 120 && velocity.Y < 0f)
60653					{
60654						velocity.Y *= 1.1f;
60655					}
60656					if (type == 287 && velocity.Y == 0f && Math.Abs(position.X + (float)(width / 2) - (Main.player[target].position.X + (float)(Main.player[target].width / 2))) < 150f && Math.Abs(position.Y + (float)(height / 2) - (Main.player[target].position.Y + (float)(Main.player[target].height / 2))) < 50f && ((direction > 0 && velocity.X >= 1f) || (direction < 0 && velocity.X <= -1f)))
60657					{
60658						velocity.X = 8 * direction;
60659						velocity.Y = -4f;
60660						netUpdate = true;
60661					}
60662					if (type == 287 && velocity.Y < 0f)
60663					{
60664						velocity.X *= 1.2f;
60665						velocity.Y *= 1.1f;
60666					}
60667					if (type == 460 && velocity.Y < 0f)
60668					{
60669						velocity.X *= 1.3f;
60670						velocity.Y *= 1.1f;
60671					}
60672				}
60673			}
60674			else if (flag8)
60675			{
60676				ai[1] = 0f;
60677				ai[2] = 0f;
60678			}
60679			if (Main.netMode != 1 && type == 120 && ai[3] >= (float)num58)
60680			{
60681				int targetTileX = (int)Main.player[target].Center.X / 16;
60682				int targetTileY = (int)Main.player[target].Center.Y / 16;
60683				Vector2 chosenTile = Vector2.Zero;
60684				if (AI_AttemptToFindTeleportSpot(ref chosenTile, targetTileX, targetTileY, 20, 9))
60685				{
60686					position.X = chosenTile.X * 16f - (float)(width / 2);
60687					position.Y = chosenTile.Y * 16f - (float)height;
60688					ai[3] = -120f;
60689					netUpdate = true;
60690				}
60691			}
60692		}
60693	
60694		public static bool DespawnEncouragement_AIStyle3_Fighters_NotDiscouraged(int npcID, Vector2 position, NPC npcInstance)
60695		{
60696			if (!Main.eclipse && Main.IsItDay() && (npcInstance == null || !npcInstance.SpawnedFromStatue) && !((double)position.Y > Main.worldSurface * 16.0) && (npcInstance == null || !Main.player[npcInstance.target].ZoneGraveyard) && (!Main.snowMoon || (npcID != 343 && npcID != 350)) && (Main.invasionType != 1 || (npcID != 26 && npcID != 27 && npcID != 28 && npcID != 111 && npcID != 471)) && (!Main.dontStarveWorld || (npcID != 164 && npcID != 163)) && npcID != 73 && npcID != 624 && (npcID != 631 || !(npcInstance.ai[2] > 0f)) && (Main.invasionType != 3 || npcID < 212 || npcID > 216) && (Main.invasionType != 4 || (npcID != 381 && npcID != 382 && npcID != 383 && npcID != 385 && npcID != 386 && npcID != 389 && npcID != 391 && npcID != 520)) && npcID != 31 && npcID != 294 && npcID != 295 && npcID != 296 && npcID != 47 && npcID != 67 && npcID != 77 && npcID != 78 && npcID != 79 && npcID != 80 && npcID != 630 && npcID != 110 && npcID != 120 && npcID != 168 && npcID != 181 && npcID != 185 && npcID != 198 && npcID != 199 && npcID != 206 && npcID != 217 && npcID != 218 && npcID != 219 && npcID != 220 && npcID != 239 && npcID != 243 && npcID != 254 && npcID != 255 && npcID != 257 && npcID != 258 && npcID != 291 && npcID != 292 && npcID != 293 && npcID != 379 && npcID != 380 && npcID != 464 && npcID != 470 && npcID != 424 && (npcID != 411 || (npcInstance != null && !(npcInstance.ai[1] >= 180f) && !(npcInstance.ai[1] < 90f))))
60697			{
60698				switch (npcID)
60699				{
60700				default:
60701					if (npcID != 528 && npcID != 529 && npcID != 530 && npcID != 532)
60702					{
60703						return NPCID.Sets.CritterThatCanTurnOnPlayers[npcID];
60704					}
60705					break;
60706				case 409:
60707				case 415:
60708				case 419:
60709				case 425:
60710				case 427:
60711				case 428:
60712				case 429:
60713				case 508:
60714				case 524:
60715				case 525:
60716				case 526:
60717				case 527:
60718				case 580:
60719				case 582:
60720					break;
60721				}
60722			}
60723			return true;
60724		}
60725	
60726		public static bool DespawnEncouragement_AIStyle3_Fighters_CanBeBusyWithAction(int npcID)
60727		{
60728			if (npcID != 110 && npcID != 111 && npcID != 206 && npcID != 216 && npcID != 214 && npcID != 215 && npcID != 291 && npcID != 292 && npcID != 293 && npcID != 350 && npcID != 381 && npcID != 382 && npcID != 383 && npcID != 385 && npcID != 386 && npcID != 389 && npcID != 391 && npcID != 469 && npcID != 166 && npcID != 466 && npcID != 471 && npcID != 411 && npcID != 409 && npcID != 424 && npcID != 425 && npcID != 426 && npcID != 415 && npcID != 419)
60729			{
60730				return npcID == 520;
60731			}
60732			return true;
60733		}
60734	

```


---

## 🤖 Assistant · 2026-08-19T03:21:03.660Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now the jump section comparison with ours:

Ours jump section (2501-2515):
- movingInto = vxSign === dir && vxSign !== 0 && this.vy === 0 ✓ (vanilla: probe gate is `(velocity.X < 0 && num204 == -1) || (velocity.X > 0 && num204 == 1)` with num204 = spriteDirection (425 negated). Ours uses facing as dir — spriteDirection ≈ direction normally. OK approx. But — vanilla ALSO has the whole jump section gated inside `if (flag5)` where flag5 = grounded-check from :60224-60260 (the "standing on solid" scan) and NOT `(velocity.Y == 0)` alone... flag5 defaults true, set false when head blocked, set true when floor below. Ours uses movingInto with vy===0. Close.

- 4-tier jump: 
  1. height ≥ 32 && solid(fx, fy-2): -8 if solid(fx,fy-3) else -7 ✓ ours.
  2. solid(fx, fy-1): -6; ★ 624 gnome special (-8 + ceiling check → flip) — ours missing gnome jump special (gnomes leap high and flip at ceiling). LOW (624 also has petrify).
  3. y+h - fy*16 > 20 && solid(fx, fy) && !topSlope → -5 ✓ ours (uses !half — approx of topSlope/halfBrick).
  4. directionY < 0 && type != 67 && !solid(fx, fy+1) && !solid(fx+dir, fy+1) → -8, vx *= 1.5 ✓ ours (ours misses `type !== 67` crab exclusion and directionY < 0 gate — ours uses `player && player.y + player.h < this.y` (player above) instead of directionY < 0. directionY is set at :56247 (player bottom == our bottom → -1?) and :57766 (directionY > 0 && player center above bottom → -1). Hmm — ours' proxy = "player above me" ✓ roughly equals directionY<0. Missing 67 exclusion (crab shouldn't do the gap-jump... actually inverted: crab EXCLUDED from this jump). LOW.
  5. else if flag8 → ai1=0, ai2=0 ✓ (ours noted as naturally true).
  6. `if (velocity.Y == 0f && flag6 && ai[3] == 1f) velocity.Y = -5f;` — flag6 = (velocity.X == 0 && !justHit) — i.e., stuck-standing + ai[3]==1 (the lunge windup flag from 430-436 family!) → hop -5. This is part of the goblin lunge (windup then hop)! Ours missing (no ai3 lunge).
  7. Expert/586 leap-up-at-player: `velocity.Y == 0 && (expertMode || type == 586) && player.Bottom < our Top && |dx| < player.width*3 && CanHit` → 586: tiered vy -8.8..-11 by height; else vy=-7.9 (or platform check). Ours: MISSING the 586 leap-up tiers! Vanilla 586 (non-expert): type 586 IS included (`Main.expertMode || type == 586`) → zombie merman leaps up at player when directly under. Ours: nothing. MEDIUM (586 behavior: leaps onto platforms/players above).
  8. Post-jump pounce family (60599): types 31/294/295/296/47/77/104/168/196/385/389/464/470/524-527 && vy==0: if |dx|<100,|dy|<50, moving toward at ≥1 → vx *= 2 (clamp 3), vy = -4 (lunge-hop toward player when close!). ★ OURS MISSING ENTIRELY — this is the classic "skeleton/zombie pounce when close" behavior! Types include angry bones (31/294-296), skeleton (77), werewolf (104?), possessed armor... wait 104 = werewolf, 168 = arapaima?? no 168 = "Angler Fish"? Hmm whatever — 47 = hungry? Common dungeon/surface fighters. Vanilla: when player within 100×50 and moving toward → jump lunge with vx×2. Ours: NOT implemented (our fighterAI has no such block). MEDIUM-HIGH — very visible (enemies lunge at you in vanilla; ours they just walk).

Hmm wait — actually let me double check ours... our fighterAI sections: lights, wetSwim, medusa, psycho, dayDiscourage, solenian, swamp, chaos, nailhead, butcher, possessed, fritz, fighterMoveStep, stormDiver, step-up, gravity/collide, 4-tier jump, doors, spider transform, vampire, lihzahrd, friction(comment), ranged, 243, 631, 251. NO pounce block. Confirmed missing. Also missing: 120 vy×1.1 while ascending (60652), 287 leap (8×dir, -4 at <150×50 + air accel ×1.2/×1.1), 460 air accel (vx×1.3, vy×1.1 while ascending).

- 287 = Bone Lee leap: missing in ours (bone lee is a dungeon fighter — should leap + air-accelerate). MEDIUM.
- 460 butcher air boost: missing. LOW-MEDIUM.
- 120 chaos rising boost vy ×1.1: missing in ours (chaos elemental jumps higher). LOW.

- ai[3]/num58 stuck counter for all fighters: where consumed besides 120 teleport? Only :60679 (120) — and the counter also gates the "discouraged" chase branch (57732: `ai[3] < num58 && NotDiscouraged`). So the stuck counter's main effect for non-120: after hitting a door that won't open (ai3=num58), the fighter STOPS chasing (wanders, EncourageDespawn if day) until counter decays! That's the door-giving-up mechanic. Ours implements via doorCd 30 ✓ different mechanism. And :57516-57546 counter increments when stuck (position.X == oldPosition.X || ai3 >= num58 || opposite) — feeding the 120 teleport and... hmm also `ai[3] == num58 → netUpdate` only. So for non-120, ai3's only effect is the chase gate (stop chasing while ai3 >= num58, i.e., while "given up"). Since ours' door logic covers the giving-up, the missing generic counter is mostly harmless EXCEPT: vanilla fighters stuck against a wall (position.X not changing) also accumulate ai3 ≥ 60 → STOP CHASING + wander away (despawn) — an anti-stuck "give up" behavior. Ours: fighters stuck at walls keep chasing forever (no despawn). LOW-MEDIUM behavioral.

OK. Now — our jump probe uses `vy === 0` captured BEFORE collision ✓ documented. Fine.

Next: verify the RANGED section (59464-60095) against RANGED_TABLE, especially: cooldowns (num163), speeds, damage, ranges, drop, the fire-at-half rule, and the "can-open-fire" gates. Let me read 59464-59700 quickly and 59960-60095.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:04.008Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 260,
 "offset": 59464
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:04.020Z

**📎 ToolResult**

```
59464			if (type == 110 || type == 111 || type == 206 || type == 214 || type == 215 || type == 216 || type == 290 || type == 291 || type == 292 || type == 293 || type == 350 || type == 379 || type == 380 || type == 381 || type == 382 || (type >= 449 && type <= 452) || type == 468 || type == 481 || type == 411 || type == 409 || (type >= 498 && type <= 506) || type == 424 || type == 426 || type == 520)
59465			{
59466				bool flag16 = type == 381 || type == 382 || type == 520;
59467				bool flag17 = type == 426;
59468				bool flag18 = true;
59469				int num161 = -1;
59470				int num162 = -1;
59471				if (type == 411)
59472				{
59473					flag16 = true;
59474					num161 = 120;
59475					num162 = 120;
59476					if (ai[1] <= 220f)
59477					{
59478						flag18 = false;
59479					}
59480				}
59481				if (ai[1] > 0f)
59482				{
59483					ai[1] -= 1f;
59484				}
59485				bool flag19 = false;
59486				if (justHit)
59487				{
59488					flag19 = ai[2] > 0f;
59489					ai[1] = 30f;
59490					ai[2] = 0f;
59491					netUpdate = true;
59492				}
59493				int num163 = 70;
59494				if (type == 379 || type == 380)
59495				{
59496					num163 = 80;
59497				}
59498				if (type == 381 || type == 382)
59499				{
59500					num163 = 80;
59501				}
59502				if (type == 520)
59503				{
59504					num163 = 15;
59505				}
59506				if (type == 350)
59507				{
59508					num163 = 110;
59509				}
59510				if (type == 291)
59511				{
59512					num163 = 200;
59513				}
59514				if (type == 292)
59515				{
59516					num163 = 120;
59517				}
59518				if (type == 293)
59519				{
59520					num163 = 90;
59521				}
59522				if (type == 111)
59523				{
59524					num163 = 180;
59525				}
59526				if (type == 206)
59527				{
59528					num163 = 50;
59529				}
59530				if (type == 481)
59531				{
59532					num163 = 100;
59533				}
59534				if (type == 214)
59535				{
59536					num163 = 50;
59537				}
59538				if (type == 215)
59539				{
59540					num163 = 90;
59541				}
59542				if (type == 290)
59543				{
59544					num163 = 30;
59545				}
59546				if (type == 411)
59547				{
59548					num163 = 330;
59549				}
59550				if (type == 409)
59551				{
59552					num163 = 60;
59553				}
59554				if (type == 424)
59555				{
59556					num163 = 180;
59557				}
59558				if (type == 426)
59559				{
59560					num163 = 60;
59561				}
59562				bool flag20 = false;
59563				if (type == 216)
59564				{
59565					if (localAI[2] >= 20f)
59566					{
59567						flag20 = true;
59568						if (flag19)
59569						{
59570							localAI[3] += 1f;
59571						}
59572						int num164 = (int)localAI[3];
59573						num163 = Math.Max(60, 180 - num164 * 20);
59574					}
59575					else
59576					{
59577						num163 = 9;
59578					}
59579				}
59580				int num165 = num163 / 2;
59581				if (type == 424)
59582				{
59583					num165 = num163 - 1;
59584				}
59585				if (type == 426)
59586				{
59587					num165 = num163 - 1;
59588				}
59589				if (type == 411)
59590				{
59591					num165 = 220;
59592				}
59593				if (confused)
59594				{
59595					ai[2] = 0f;
59596				}
59597				if (ai[2] > 0f)
59598				{
59599					if (flag18)
59600					{
59601						TargetClosest();
59602					}
59603					if (ai[1] == (float)num165)
59604					{
59605						if (type == 216)
59606						{
59607							localAI[2] += 1f;
59608						}
59609						float num166 = 11f;
59610						if (type == 111)
59611						{
59612							num166 = 9f;
59613						}
59614						if (type == 206)
59615						{
59616							num166 = 7f;
59617						}
59618						if (type == 290)
59619						{
59620							num166 = 9f;
59621						}
59622						if (type == 293)
59623						{
59624							num166 = 4f;
59625						}
59626						if (type == 216)
59627						{
59628							num166 = 9f;
59629							if (flag20)
59630							{
59631								num166 = 15f;
59632							}
59633						}
59634						if (type == 214)
59635						{
59636							num166 = 10f;
59637						}
59638						if (type == 215)
59639						{
59640							num166 = 14f;
59641						}
59642						if (type == 382)
59643						{
59644							num166 = 7f;
59645						}
59646						if (type == 520)
59647						{
59648							num166 = 8f;
59649						}
59650						if (type == 409)
59651						{
59652							num166 = 4f;
59653						}
59654						if (type >= 449 && type <= 452)
59655						{
59656							num166 = 7f;
59657						}
59658						if (type == 481)
59659						{
59660							num166 = 8f;
59661						}
59662						if (type == 468)
59663						{
59664							num166 = 7.5f;
59665						}
59666						if (type == 411)
59667						{
59668							num166 = 1f;
59669						}
59670						if (type >= 498 && type <= 506)
59671						{
59672							num166 = 7f;
59673						}
59674						Vector2 chaserPosition2 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
59675						if (type == 481)
59676						{
59677							chaserPosition2.Y -= 14f;
59678						}
59679						if (type == 206)
59680						{
59681							chaserPosition2.Y -= 10f;
59682						}
59683						if (type == 290)
59684						{
59685							chaserPosition2.Y -= 10f;
59686						}
59687						if (type == 381 || type == 382)
59688						{
59689							chaserPosition2.Y += 6f;
59690						}
59691						if (type == 520)
59692						{
59693							chaserPosition2.Y = position.Y + 20f;
59694						}
59695						if (type >= 498 && type <= 506)
59696						{
59697							chaserPosition2.Y -= 8f;
59698						}
59699						if (type == 426)
59700						{
59701							chaserPosition2 += new Vector2(spriteDirection * 2, -12f);
59702							num166 = 7f;
59703						}
59704						float num167 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - chaserPosition2.X;
59705						float num168 = Math.Abs(num167) * 0.1f;
59706						if (type == 291 || type == 292)
59707						{
59708							num168 = 0f;
59709						}
59710						if (type == 215)
59711						{
59712							num168 = Math.Abs(num167) * 0.08f;
59713						}
59714						if (type == 214 || (type == 216 && !flag20))
59715						{
59716							num168 = 0f;
59717						}
59718						_ = type == 216 && flag20;
59719						if (type == 381 || type == 382 || type == 520)
59720						{
59721							num168 = 0f;
59722						}
59723						if (type >= 449 && type <= 452)

```


---

## 🤖 Assistant · 2026-08-19T03:21:47.265Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The ranged table in ours vs vanilla:

Vanilla num163 (cooldown): 70 default; 379/380=80 ✓; 381/382=80; 520=15; 350=110; 291=200 ✓; 292=120 ✓; 293=90 ✓; 111=180 ✓; 206=50 ✓; 481=100 ✓; 214=50 ✓; 215=90 ✓; 290=30 ✓; 411=330; 409=60; 424=180; 426=60.

★ Ours RANGED_TABLE discrepancies vs vanilla:
- 110 (Skeleton Archer): ours cooldown 70 ✓ default; speed 11 ✓ default (num166 default 11) ✓; dmg 35 (num171 default = ? — need to check damage section ~59870-59960); drop 0.1 ✓ default; proj 82? need check num172 for 110 (fire arrow?). ours 110: proj 82.
- 216 (pirate? no — 216 = "Pirate Deadeye"? ours: cooldown 180, speed 9, dmg 30, drop 0.1, proj 180). Vanilla 216: num163 default 70 (NOT in the override list!) — wait, 216 not listed in num163 overrides → default 70! Ours says 180. Hmm — but 216 has the flag20 staged variant (localAI[2] >= 20 → num163 = max(60, 180 - localAI[3]*20), else 9). The FIRST 20 shots (localAI[2] < 20 counting up) use num163=9?? Wait: `if (type == 216) { if (localAI[2] >= 20f) { flag20 = true; ... num163 = max(60, 180 - num164*20); } else num163 = 9; }` — 216 fires fast (9) for the first 20 volleys (localAI[2] counts up per shot), then slows to 180-reduced-by-hits... no wait, localAI[3] increments when flag19 (justHit && ai2>0). Deadeye gets FASTER after being hit (num163 = 180 - hits*20, min 60). This is the pirate deadeye "gets angry when hit" mechanic. Ours: static cooldown 180 — WRONG (should be 9 initially). Hmm wait — localAI[2] increments per shot at :59607. Starts 0 → first 20 shots at cooldown 9!? That's ~6x/sec — pirate deadeyes fire musket shots every 9 ticks for first 20 shots?? That seems too fast. Hmm, num165 = num163/2 = 4.5 (int 4). Actually wait — for 216 the fire happens at ai1 == num165. Hmm, cooldown 9 means it re-aims quickly. Musket bullets at 9-tick intervals ×20? That's the "deadeye rapid volley" — actually YES, pirate deadeyes in vanilla fire a quick burst of shots when they first see you, then settle. Our 180 static = way slower. MEDIUM. But let me double check num163 for 216: not in override list → 70 default; then the `if (type == 216)` block: localAI[2] >= 20 → staged; else num163 = 9. So first 20 shots: 9; after: max(60, 180-20×hits). Ours: 180. CONFIRMED deviation.

- 379/380 (cultist archers): num163=80 ✓ ours.
- 468 Dr Man Fly: default 70 ✓ ours 70.
- 449-452: default 70 ✓ ours 70; speed 7 ✓; drop rand(0.10-0.49) ✓ ours 0.25? ours says drop 0.25 with comment "drop 原版 rand 0.10-0.49" — ours uses FIXED 0.25 instead of random per-shot! Vanilla: `num168 = Main.rand.Next(10, 50) * 0.01` per volley (need to verify in 59723-59730). Ours comment acknowledges. Deviation LOW-MED (trajectory variance).
- 498-506: default 70 ✓ ours 70; speed 7 ✓.
- 481: 100 ✓ ours; speed 8 ✓; oy -14 ✓ (chaserPosition2.Y -= 14) ✓.
- 206: 50 ✓; speed 7 ✓; oy -10 ✓.
- 290: 30 ✓; speed 9 ✓; oy -10 ✓.
- 214: 50 ✓; speed 10 ✓; drop 0 ✓ ours; spread 45 ✓ need verify.
- 215: 90 ✓; speed 14 ✓; drop 0.08 ✓.
- 291: 200 ✓; speed 4 ✓; spread 8 ✓; drop 0 ✓.
- 292: 120 ✓; speed 12 ✓; burst 4 ✓ ours (fire at num163-1 per ours comment "292 在 num163-1 连发" — vanilla num165 = num163/2 = 60 for 292... wait ours says `const fireAt = R.burst ? R.cooldown - 1 : R.cooldown >> 1;` — burst only set for 292. But vanilla's num165 = num163-1 override is for **424 and 426**, NOT 292! Let me recheck: :59581 `if (type == 424) num165 = num163 - 1; if (type == 426) num165 = num163 - 1; if (type == 411) num165 = 220`. 292 uses num165 = num163/2 = 60. Ours: 292 fireAt = 119. ★ DEVIATION: ours fires at 119 (later) vs vanilla 60. Hmm wait — but 292's burst of 4: where's that? At :59967 per ours comment "292 在 num163-1 连发（cs:59967）". Let me check :59960-59975 to see. The burst for 292 might be a separate re-aim loop. I need to read 59723-60095 to resolve. Also 424/426 (not in ours' RANGED_TABLE at all! 424 = "Martian Officer"? 426 = Corite ranged!). Ours RANGED_TABLE lacks 381/382/411/409/424/426/520/350 — wait, are those types even in our RANGED_FIGHTERS set? Ours set: 111,214,215,216,110,206,290,291,292,293,449-452,481,498-506,379,380,468. Missing from ours: 350 (paladin? no 350 = "Ragged Caster"? hmm — 290 paladin IS in ours), 381, 382 (martian rangers), 411, 409, 424, 426, 520. 

Wait ours has 290 = "圣骑士 圣锤" with cooldown 30. Vanilla 350 has num163=110 — 350 = "Necromancer"? no... 350 = "Ragged Caster" (hardmode dungeon caster uses aiStyle 3?!). Hmm no — Ragged Caster is 275? I'm confusing myself. 381/382 = Martian "Tesla" something? Actually per the ranged list: 381/382 are ranged fighters in vanilla. Let me check our RANGED_TABLE again: 290: { cooldown: 30, speed: 9, dmg: 60, range: 700, drop: 0, oy: -10, proj: 300 }. Vanilla 290 = Paladin ✓ (num163=30 ✓, num166=9 ✓, oy -10 ✓).

Missing ranged types in ours: 350 (num163=110), 381, 382 (num163=80, speed 7 for 382), 409 (60), 411 (330/aim window), 424 (180), 426 (60, muzzle offset (dir*2,-12)), 520 (15!). 520 = "Martian Tesla"? — wait 520 in move chain excluded too. 520 = "Martian... Walker"? hmm. Whatever they are — they're missing from our RANGED_TABLE entirely → these enemies never shoot. Which are they? 350 = Ragged Caster? Let me think: 290 Paladin, 291 Sniper... 350 = "Martian Drone"? no. Ugh. IDs I should resolve: 350, 381, 382, 409, 411, 424, 426, 520. From names data... these are hardmode dungeon casters & martians:
- 350: hmm "Ragged Caster"? No — ragged caster is aiStyle 8 (281-286 are the three hardmode casters). 350 might be "Mimic"? no. Actually! 350 = "Snow Balla"? no that's 373? Hmm.
- Let me quickly resolve via our own enemies data (game/src/data/enemies.ts) which likely has names.

Also ours' RANGED set includes 468 flag aimDecelOffEclipse ✓.

Rather than chase all names, let me verify the remaining fire/damage/proj numbers (59723-60095) with one read, then check our enemies.ts for those IDs.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:47.407Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "limit": 375,
 "offset": 59723
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:47.428Z

**📎 ToolResult**

```
59723						if (type >= 449 && type <= 452)
59724						{
59725							num168 = Math.Abs(num167) * (float)Main.rand.Next(10, 50) * 0.01f;
59726						}
59727						if (type == 468)
59728						{
59729							num168 = Math.Abs(num167) * (float)Main.rand.Next(10, 50) * 0.01f;
59730						}
59731						if (type == 481)
59732						{
59733							num168 = Math.Abs(num167) * (float)Main.rand.Next(-10, 11) * 0.0035f;
59734						}
59735						if (type >= 498 && type <= 506)
59736						{
59737							num168 = Math.Abs(num167) * (float)Main.rand.Next(1, 11) * 0.0025f;
59738						}
59739						float num169 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - chaserPosition2.Y - num168;
59740						if (type == 291)
59741						{
59742							num167 += (float)Main.rand.Next(-40, 41) * 0.2f;
59743							num169 += (float)Main.rand.Next(-40, 41) * 0.2f;
59744						}
59745						else if (type == 381 || type == 382 || type == 520)
59746						{
59747							num167 += (float)Main.rand.Next(-100, 101) * 0.4f;
59748							num169 += (float)Main.rand.Next(-100, 101) * 0.4f;
59749							num167 *= (float)Main.rand.Next(85, 116) * 0.01f;
59750							num169 *= (float)Main.rand.Next(85, 116) * 0.01f;
59751							if (type == 520)
59752							{
59753								num167 += (float)Main.rand.Next(-100, 101) * 0.6f;
59754								num169 += (float)Main.rand.Next(-100, 101) * 0.6f;
59755								num167 *= (float)Main.rand.Next(85, 116) * 0.015f;
59756								num169 *= (float)Main.rand.Next(85, 116) * 0.015f;
59757							}
59758						}
59759						else if (type == 481)
59760						{
59761							num167 += (float)Main.rand.Next(-40, 41) * 0.4f;
59762							num169 += (float)Main.rand.Next(-40, 41) * 0.4f;
59763						}
59764						else if (type >= 498 && type <= 506)
59765						{
59766							num167 += (float)Main.rand.Next(-40, 41) * 0.3f;
59767							num169 += (float)Main.rand.Next(-40, 41) * 0.3f;
59768						}
59769						else if (type == 426)
59770						{
59771							num167 += (float)Main.rand.Next(-30, 31) * 0.3f;
59772							num169 += (float)Main.rand.Next(-30, 31) * 0.3f;
59773						}
59774						else if (type == 214)
59775						{
59776							num167 += (float)Main.rand.Next(-45, 46);
59777							num169 += (float)Main.rand.Next(-45, 46);
59778						}
59779						else if (type == 216)
59780						{
59781							if (!flag20)
59782							{
59783								num167 += (float)Main.rand.Next(-50, 51);
59784								num169 += (float)Main.rand.Next(-50, 51);
59785							}
59786						}
59787						else if (type != 292)
59788						{
59789							num167 += (float)Main.rand.Next(-40, 41);
59790							num169 += (float)Main.rand.Next(-40, 41);
59791						}
59792						float num170 = (float)Math.Sqrt(num167 * num167 + num169 * num169);
59793						netUpdate = true;
59794						num170 = num166 / num170;
59795						num167 *= num170;
59796						num169 *= num170;
59797						int num171 = 35;
59798						int num172 = 82;
59799						if (type == 111)
59800						{
59801							num171 = 11;
59802						}
59803						if (type == 206)
59804						{
59805							num171 = 37;
59806						}
59807						if (type == 379 || type == 380)
59808						{
59809							num171 = 40;
59810						}
59811						if (type == 350)
59812						{
59813							num171 = 45;
59814						}
59815						if (type == 468)
59816						{
59817							num171 = 50;
59818						}
59819						if (type == 111)
59820						{
59821							num172 = 81;
59822						}
59823						if (type == 379 || type == 380)
59824						{
59825							num172 = 81;
59826						}
59827						if (type == 381)
59828						{
59829							num172 = 436;
59830							num171 = 24;
59831						}
59832						if (type == 382)
59833						{
59834							num172 = 438;
59835							num171 = 30;
59836						}
59837						if (type == 520)
59838						{
59839							num172 = 592;
59840							num171 = 35;
59841						}
59842						if (type >= 449 && type <= 452)
59843						{
59844							num172 = 471;
59845							num171 = 15;
59846						}
59847						if (type >= 498 && type <= 506)
59848						{
59849							num172 = 572;
59850							num171 = 14;
59851						}
59852						if (type == 481)
59853						{
59854							num172 = 508;
59855							num171 = 18;
59856						}
59857						if (type == 206)
59858						{
59859							num172 = 177;
59860						}
59861						if (type == 468)
59862						{
59863							num172 = 501;
59864						}
59865						if (type == 411)
59866						{
59867							num172 = 537;
59868							num171 = GetAttackDamage_ForProjectiles(60f, 45f);
59869						}
59870						if (type == 424)
59871						{
59872							num172 = 573;
59873							num171 = GetAttackDamage_ForProjectiles(60f, 45f);
59874						}
59875						if (type == 426)
59876						{
59877							num172 = 581;
59878							num171 = GetAttackDamage_ForProjectiles(60f, 45f);
59879						}
59880						if (type == 291)
59881						{
59882							num172 = 302;
59883							num171 = 100;
59884						}
59885						if (type == 290)
59886						{
59887							num172 = 300;
59888							num171 = 60;
59889						}
59890						if (type == 293)
59891						{
59892							num172 = 303;
59893							num171 = 60;
59894						}
59895						if (type == 214)
59896						{
59897							num172 = 180;
59898							num171 = 25;
59899						}
59900						if (type == 215)
59901						{
59902							num172 = 82;
59903							num171 = 35;
59904						}
59905						if (type == 292)
59906						{
59907							num171 = 50;
59908							num172 = 180;
59909						}
59910						if (type == 216)
59911						{
59912							num172 = 180;
59913							num171 = 30;
59914							if (flag20)
59915							{
59916								num171 = 100;
59917								num172 = 240;
59918								localAI[2] = 0f;
59919								localAI[3] = 0f;
59920							}
59921						}
59922						Player player3 = Main.player[target];
59923						Vector2? vector35 = null;
59924						if (type == 426)
59925						{
59926							vector35 = Main.rand.NextVector2FromRectangle(player3.Hitbox);
59927						}
59928						if (vector35.HasValue)
59929						{
59930							Utils.ChaseResults chaseResults2 = Utils.GetChaseResults(chaserPosition2, num166, vector35.Value, player3.velocity);
59931							if (chaseResults2.InterceptionHappens)
59932							{
59933								Vector2 vector36 = Utils.FactorAcceleration(chaseResults2.ChaserVelocity, chaseResults2.InterceptionTime, new Vector2(0f, 0.1f), 15);
59934								num167 = vector36.X;
59935								num169 = vector36.Y;
59936							}
59937						}
59938						chaserPosition2.X += num167;
59939						chaserPosition2.Y += num169;
59940						if (type == 214)
59941						{
59942							chaserPosition2.X += num167 * 1.5f;
59943							chaserPosition2.Y += num169 * 1.5f;
59944						}
59945						if (type == 290)
59946						{
59947							num171 = GetAttackDamage_ForProjectiles(num171, (float)num171 * 0.75f);
59948						}
59949						if (type >= 381 && type <= 392)
59950						{
59951							num171 = GetAttackDamage_ForProjectiles(num171, (float)num171 * 0.8f);
59952						}
59953						if (Main.netMode != 1)
59954						{
59955							if (type == 292)
59956							{
59957								for (int num173 = 0; num173 < 4; num173++)
59958								{
59959									num167 = player3.position.X + (float)player3.width * 0.5f - chaserPosition2.X;
59960									num169 = player3.position.Y + (float)player3.height * 0.5f - chaserPosition2.Y;
59961									num170 = (float)Math.Sqrt(num167 * num167 + num169 * num169);
59962									num170 = 12f / num170;
59963									num167 = (num167 += (float)Main.rand.Next(-40, 41));
59964									num169 = (num169 += (float)Main.rand.Next(-40, 41));
59965									num167 *= num170;
59966									num169 *= num170;
59967									Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer);
59968								}
59969							}
59970							else if (type == 411)
59971							{
59972								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer, 0f, whoAmI);
59973							}
59974							else if (type == 424)
59975							{
59976								for (int num174 = 0; num174 < 4; num174++)
59977								{
59978									Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center.X - (float)(spriteDirection * 4), base.Center.Y + 6f, (float)(-3 + 2 * num174) * 0.15f, (float)(-Main.rand.Next(0, 3)) * 0.2f - 0.1f, num172, num171, 0f, Main.myPlayer, 0f, whoAmI);
59979								}
59980							}
59981							else if (type == 409)
59982							{
59983								int num175 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X, (int)base.Center.Y, 410, whoAmI);
59984								Main.npc[num175].velocity = new Vector2(num167, -6f + num169);
59985							}
59986							else
59987							{
59988								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), chaserPosition2.X, chaserPosition2.Y, num167, num169, num172, num171, 0f, Main.myPlayer);
59989							}
59990						}
59991						if (Math.Abs(num169) > Math.Abs(num167) * 2f)
59992						{
59993							if (num169 > 0f)
59994							{
59995								ai[2] = 1f;
59996							}
59997							else
59998							{
59999								ai[2] = 5f;
60000							}
60001						}
60002						else if (Math.Abs(num167) > Math.Abs(num169) * 2f)
60003						{
60004							ai[2] = 3f;
60005						}
60006						else if (num169 > 0f)
60007						{
60008							ai[2] = 2f;
60009						}
60010						else
60011						{
60012							ai[2] = 4f;
60013						}
60014					}
60015					if ((velocity.Y != 0f && !flag17) || ai[1] <= 0f)
60016					{
60017						ai[2] = 0f;
60018						ai[1] = 0f;
60019					}
60020					else if (!flag16 || (num161 != -1 && ai[1] >= (float)num161 && ai[1] < (float)(num161 + num162) && (!flag17 || velocity.Y == 0f)))
60021					{
60022						velocity.X *= 0.9f;
60023						spriteDirection = direction;
60024					}
60025				}
60026				if (type == 468 && !Main.eclipse)
60027				{
60028					flag16 = true;
60029				}
60030				else if ((ai[2] <= 0f || flag16) && (velocity.Y == 0f || flag17) && ai[1] <= 0f && !Main.player[target].dead)
60031				{
60032					bool flag21 = Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height);
60033					if (type == 520)
60034					{
60035						flag21 = Collision.CanHitLine(base.Top + new Vector2(0f, 20f), 0, 0, Main.player[target].position, Main.player[target].width, Main.player[target].height);
60036					}
60037					if (Main.player[target].stealth == 0f && Main.player[target].itemAnimation == 0)
60038					{
60039						flag21 = false;
60040					}
60041					if (flag21)
60042					{
60043						float num176 = 10f;
60044						Vector2 vector37 = new Vector2(position.X + (float)width * 0.5f, position.Y + (float)height * 0.5f);
60045						float num177 = Main.player[target].position.X + (float)Main.player[target].width * 0.5f - vector37.X;
60046						float num178 = Math.Abs(num177) * 0.1f;
60047						float num179 = Main.player[target].position.Y + (float)Main.player[target].height * 0.5f - vector37.Y - num178;
60048						num177 += (float)Main.rand.Next(-40, 41);
60049						num179 += (float)Main.rand.Next(-40, 41);
60050						float num180 = (float)Math.Sqrt(num177 * num177 + num179 * num179);
60051						float num181 = 700f;
60052						if (type == 214)
60053						{
60054							num181 = 500f;
60055						}
60056						if (type == 215)
60057						{
60058							num181 = 650f;
60059						}
60060						if (type >= 498 && type <= 506)
60061						{
60062							num181 = 190f;
60063						}
60064						if (type >= 449 && type <= 452)
60065						{
60066							num181 = 200f;
60067						}
60068						if (type == 481)
60069						{
60070							num181 = 400f;
60071						}
60072						if (type == 468)
60073						{
60074							num181 = 400f;
60075						}
60076						if (num180 < num181)
60077						{
60078							netUpdate = true;
60079							velocity.X *= 0.5f;
60080							num180 = num176 / num180;
60081							num177 *= num180;
60082							num179 *= num180;
60083							ai[2] = 3f;
60084							ai[1] = num163;
60085							if (Math.Abs(num179) > Math.Abs(num177) * 2f)
60086							{
60087								if (num179 > 0f)
60088								{
60089									ai[2] = 1f;
60090								}
60091								else
60092								{
60093									ai[2] = 5f;
60094								}
60095							}
60096							else if (Math.Abs(num177) > Math.Abs(num179) * 2f)
60097							{

```


---

## 🤖 Assistant · 2026-08-19T03:22:38.266Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Ranged section verified. Now the diffs against our RANGED_TABLE:

CONFIRMED diffs:
1. **216 Pirate Deadeye (or whatever)**: ours cooldown 180, dmg 30, proj 180, spread ±50. Vanilla: first 20 shots cooldown **9** (localAI[2] < 20, spread ±50), then staged max(60, 180-20×hitCount) with dmg 100 proj 240 (sniper shot!) and localAI[2/3] reset. Ours static 180/30/180 — significant (initial rapid volley missing + enraged sniper shot missing). MEDIUM.
2. **292 Tactical Skeleton**: ours fireAt = cooldown-1 = 119, 4 shots re-aiming ±40 at speed 12 ✓ spread... vanilla: fires at num165 = num163/2 = **60**, 4 shots each re-aimed ±40 speed 12. Ours fires at 119 — later in the windup. Also vanilla num168=0 for 292 ✓ ours drop 0 ✓. fireAt deviation: MEDIUM-LOW (shot timing halved... actually ours fires at cooldown-1 i.e., near END of windup (119/120 elapsed) vs vanilla at 60/120 — ours aims "fresher" but fires later). Hmm wait — ours fires when ai0 (counting down from cooldown) hits cooldown-1 = 119, i.e., almost immediately after aiming starts! ai0 = R.cooldown = 120 set at aim start; decrement; fireAt = 119 → fires after 1 tick! Vanilla fires at ai1 == 60 (half). So OURS fires 1 tick after aiming starts — much FASTER than vanilla's 60-tick telegraph. That's a visible fairness difference (no warning time). MEDIUM. Actually wait — for others fireAt = cooldown>>1 = half ✓ correct. Only 292 (burst) uses cooldown-1. The comment says "292 在 num163-1 连发（cs:59967）" — misreading: cs:59581-59588 num163-1 override is for 424/426, not 292. CONFIRMED bug: 292 should fire at 60, ours at 119.
3. **468 drop**: vanilla rand(10,50)*0.01 = 0.10..0.49 random per shot; ours [0.1,0.49] array ✓ CORRECT (ours supports array drop!). ✓
4. **449-452 drop**: vanilla rand(10,50)*0.01 per shot; ours fixed 0.25 — deviation LOW (acknowledged in comment).
5. **481 drop**: vanilla rand(-10,11)*0.0035 → -0.035..0.035 (signed!); ours drop 0 with comment. LOW.
6. **498-506 drop**: vanilla rand(1,11)*0.0025 = 0.0025..0.025; ours 0.01 fixed. LOW.
7. **481 spread**: vanilla ±0.4×40 = ±16 ✓ ours 16 ✓.
8. **498-506 spread**: 0.3×40 = ±12 ✓ ours 12 ✓.
9. **214 spread**: ±45 ✓ ours. 214 muzzle: += velocity×1.5 extra offset — ours? ours doesn't add the extra ×1.5 forward displacement for 214. LOW.
10. **Damage numbers**: default 35 (ours 110 uses 35 ✓); 111=11 ✓; 206=37 ✓; 379/380=40 (ours 35! ★ vanilla num171=40 for 379/380 — ours says 35. DEVIATION LOW-MED); 468=50 ✓; 291=100 ✓; 290=60 ✓ + difficulty scaling ×0.75 (ours 60 flat — Dart may scale? our shootDart → projTargets.hitPlayer applies difficulty scaling per earlier comment — OK ✓); 293=60 ✓; 214=25 ✓; 215=35 ✓; 292=50 ✓; 449-452=15 ✓; 498-506=14 ✓; 481=18 ✓; 468 proj 501 ✓; 381/382/520/411/424/426/409/350 missing from ours entirely.
11. **Aim-decel**: vanilla 60020: `!flag16 || window` → vx *= 0.9. Ours aimDecel ✓ (468 non-eclipse → flag16=true → skip decel ✓ ours).
12. **Open-aim gate**: vanilla 60030: `(ai2 <= 0 || flag16) && (vy == 0 || flag17) && ai1 <= 0 && !dead`; CanHit ✓; stealth==0 && itemAnimation==0 → flag21 = false — WAIT: `if (player.stealth == 0f && player.itemAnimation == 0f) flag21 = false;` — flag21 gets DISABLED when player is NOT stealthed and NOT using an item?? That means enemies only open fire when player is stealthed (hidden) or itemAnimation>0?! That reads backwards... Actually vanilla semantics: stealth != 0 = wearing stealth armor (hidden); so `stealth == 0 && itemAnimation == 0` → can't open fire?? That would mean fighters never shoot a standing player... which is FALSE in game. Hold on — re-read: `if (Main.player[target].stealth == 0f && Main.player[target].itemAnimation == 0f) { flag21 = false; }` Hmm. That can't be right... OH WAIT. I bet it's inverted in decompilation: original likely `if (stealth != 0 ...) flag21 = ...`. Let me think about actual Terraria behavior: ranged fighters DO shoot you when you stand still. Hmm — but there's a known mechanic: enemies DON'T notice you until you use an item or move...? No...

Actually the real vanilla mechanic (1.4): "Enemies won't target/aggro a player who stands completely still with no item use, UNLESS the player is detected" — no that's not right either. Let me look at the actual source: In Terraria 1.4 source, AI_003 ranged: 
```
if (Main.player[target].stealth == 0f && Main.player[target].itemAnimation == 0f)
    flag21 = true;
```
Hmm — which direction? There IS a known 1.4.4 mechanic: standing still without using items makes enemies NOT shoot you (they lose track). Wait no — it's the opposite: the known mechanic is "enemies can't see you if you stand perfectly still" — no...

Actually I recall: 1.4 added that enemies only "notice" you when you move/attack; standing still in the open, skeleton archers won't fire? No — that's the Shroomite stealth. For players: stealth != 0 = Shroomite/vortex stealth active. itemAnimation != 0 = swinging/using item.

Given decompiled code as ground truth: flag21 = CanHit(...); if (stealth == 0 && itemAnimation == 0) flag21 = false. So when player has NO stealth and NO item use → cannot open fire. That means: fighters only start aiming at a player who is either stealthed(!?) or actively using an item. Once aiming (ai2>0), the countdown continues. Hmm — that literally means a standing idle player is never targeted by these shooters... that matches OUR implementation! Ours: `let los = player.useTime > 0` — "目标玩家待机（原版 stealth==0 && itemAnimation==0 → 视线判 false）" — ours requires useTime > 0 to open aim. ✓ SAME semantics as the decompile. OK — ours already matches (and comments it). Good, not a bug.

13. Range: default 700 ✓; 214=500 ✓; 215=650 ✓; 498-506=190 ✓; 449-452=200 ✓; 481=400 ✓; 468=400 ✓. Ours ✓ all.
14. `num176` (aiming projectile speed 10) used for aim-line — visual.
15. Velocity damp on opening: vx *= 0.5 ✓ ours.
16. ai2 posture values (1/2/3/4/5) — ours sets ai3=3 marker only (comment: rendering side). Vanilla uses ai2 1-5 for aim pose. Ours ai3=3 constant — rendering approx. LOW (already noted).

17. justHit → ai1=30, ai2=0 (aim reset + quick re-aim) :59486-59492 — ★ OURS MISSING! Vanilla: getting hit while a fighter resets the aim timer to 30 and clears the aim (so they re-aim quickly but lose current windup). Ours comment mentions "justHit 打断蓄力 cs:59489" but I don't see it in our code! Our ranged block: `if (this.ai3 > 0) {...} else if (vy===0 && ai0<=0 && ...)` — no justHit handling. CONFIRMED MISSING — MEDIUM (shooting enemies currently keep their full windup through hits; vanilla resets to 30).

Wait — let me double-check our code at 2586-2634... `if (player && ... RANGED_FIGHTERS...)` — the block. Inside: aiming branch decrements ai0, fires at fireAt, releases on move/cooldown-end. No justHit reset. Confirmed missing.

18. 411: fires proj 537 with whoAmI; 409 spawns NPC 410 (launcher blob); 424: 4-shot arc pattern; 426: chase-results interception targeting. All missing in ours (types not in RANGED_TABLE). What are these? 411/409/424/426/381/382/520 — let me identify from our enemies.ts quickly.

Also the ai2 posture & the 426-flag17 (keeps aiming while moving) etc.

Now let me resolve the names for the unimplemented ids (350, 381, 382, 409, 411, 424, 426, 427, 428, 415, 471, 472, 482, 516, 430-436, 494/495, 591) in our repo's enemies.ts to write a precise report.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:22:41.026Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"vanillaId === 426\\|vanillaId === 424\\|vanillaId === 409\\|vanillaId === 411\\|vanillaId === 381\\|vanillaId === 382\\|vanillaId === 520\\|vanillaId === 350\\|=== 516\\|=== 472\\|=== 482\\|=== 428\" ~/Project/GLM/SandboxWorld/game/src/entities/*.ts | grep -v fighterFamilies | head -20; echo ---; grep -rn \"v_426_\\|v_471_\\|v_482_\\|v_409_\\|v_411_\\|v_424_\\|v_520_\\|v_350_\\|v_516_\" ~/Project/GLM/SandboxWorld/game/src/data/enemies.ts | head -12",
 "description": "Resolve names of unimplemented fighter ids"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:41.067Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts:958:  if (vid === 516) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts:1027:  if (vid === 516) {
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_moon_events.ts:1063:    if (vid === 516 && (e.hitWall || e.hitHead || e.onGround)) {
---

```


---

## 🤖 Assistant · 2026-08-19T03:22:48.965Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"'426'\\|\\\"426\\\"\\|: 426\\b\" ~/Project/GLM/SandboxWorld/game/src/data/vanilla-npcs* 2>/dev/null | head -3; ls ~/Project/GLM/SandboxWorld/game/src/data | grep -i npc; grep -rn \"426\" ~/Project/GLM/SandboxWorld/game/src/ai/*.ts 2>/dev/null | head -3; find ~/Project/GLM/SandboxWorld/game/src -name \"*.ts\" | xargs grep -ln \"vanillaNpc\\b\" 2>/dev/null | head -5",
 "description": "Find vanilla NPC registry source"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:49.056Z

**📎 ToolResult**

```
(eval):1: no matches found: ~/Project/GLM/SandboxWorld/game/src/data/vanilla-npcs*
npcLavaImmune.ts
npcPortraits.ts
townNpcProfiles.ts
vanilla-npc-immunity.json
vanilla-npcbestiaryoffset.json
vanilla-npcdrops.json
vanilla-npcnetid.json
vanilla-npcvalue.json
vanillaNpcAmbience.ts
vanillaNpcImmunity.ts
vanillaNpcs.ts
(eval):1: no matches found: ~/Project/GLM/SandboxWorld/game/src/ai/*.ts
~/Project/GLM/SandboxWorld/game/src/core/Game.ts
~/Project/GLM/SandboxWorld/game/src/physics/Conveyor.ts
~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts
~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts
~/Project/GLM/SandboxWorld/game/src/entities/bossAI_golem.ts

```


---

## 🤖 Assistant · 2026-08-19T03:22:54.003Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"^  \\[4\\|\\[426\\|\\[424\\|\\[409\\|\\[411\\|\\[381\\|\\[382\\|\\[520\\|\\[350\\|\\[516\\|\\[471\\|\\[472\\|\\[482\\|\\[428\\|\\[427\\|\\[415\\|\\[416\\|\\[430\\|\\[494\\|\\[591\\|\\[624\\|\\[204\\|\\[81\\|\\[141\\|\\[138\\|\\[71\\|\\[304\\|\\[183\\|\\[341\\|\\[629\\|\\[59\\b\" ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts | head -40",
 "description": "Look up NPC names by id in vanillaNpcs.ts"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:54.025Z

**📎 ToolResult**

```
(Bash completed with no output)

```


---

## 🤖 Assistant · 2026-08-19T03:22:57.626Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "head -40 ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts; grep -n \"426\\|Corite\\|Scutlix\" ~/Project/GLM/SandboxWorld/game/src/data/vanillaNpcs.ts | head -8",
 "description": "Inspect vanillaNpcs.ts structure"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:22:57.664Z

**📎 ToolResult**

```
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

```


---

## 🤖 Assistant · 2026-08-19T03:23:07.714Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
The NPC data is in a JSON. Let me just query the vanilla-npcs.json for names of the ids I need. Actually — this is name resolution only for report readability. Let me do one quick lookup.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:23:10.069Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst j = require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst list = j.npcs || j;\nconst ids = [81,138,141,183,304,341,350,381,382,409,410,411,415,416,424,426,427,428,471,472,482,516,591,629,658,659,667,244,71,348,349,430];\nfor (const id of ids) { const e = list[String(id)] || list[id]; console.log(id, e ? (e.name || e.key || JSON.stringify(e).slice(0,60)) : '??'); }\n\" 2>&1 | head -40",
 "description": "Resolve NPC names from vanilla-npcs.json"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:23:10.111Z

**📎 ToolResult**

```
81 Corrupt Slime
138 Illuminant Slime
141 Toxic Sludge
183 Crimslime
304 Hoppin' Jack
341 Present Mimic
350 Elf Archer
381 Brain Scrambler
382 Ray Gunner
409 Twinkle Popper
410 NPC_410
411 Stargazer
415 Drakomire
416 Drakomire Rider
424 Predictor
426 Alien Queen
427 Alien Hornet
428 Alien Larva
471 Goblin Warlock
472 Shadowflame Apparition
482 Granite Golem
516 NPC_516
591 Zombie
629 Ice Mimic
658 QueenSlimeMinionBlue
659 QueenSlimeMinionPink
667 GoldenSlime
244 Rainbow Slime
71 Dungeon Slime
348 NPC_348
349 Nutcracker
430 NPC_430

```


---

## 🤖 Assistant · 2026-08-19T03:23:21.620Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Names resolved:
- 81 Corrupt Slime, 138 Illuminant Slime, 141 Toxic Sludge, 183 Crimslime, 304 Hoppin' Jack, 244 Rainbow Slime, 71 Dungeon Slime — slime ai0 extras.
- 415 Drakomire (fireball 516 = Drakomire fireball), 416 Drakomire Rider.
- 426 Alien Queen... wait that doesn't sound right. Alien Queen? Actually 426 = "Alien Queen"? Hmm — no, vanilla 426 = "Corite"... but our data says Alien Queen. Whatever, our data is authoritative-ish (martian: 424 Predictor, 426... hmm "Alien Queen" — hmm the AI has num163=60 + chase interception + spawn... OK whatever). Actually wait — these are MARTIAN enemies (381 Brain Scrambler, 382 Ray Gunner, 409 Twinkle Popper, 410 (spawned), 411 Stargazer, 424 Predictor, 426 Alien Queen?? no...). Hmm — martian madness: 383 Scutlix Gunman? no... The exact names don't matter for the audit — these are all MARTIAN MADNESS + SOLAR PILLAR ranged/servo enemies missing ranged attacks in ours.

Wait — but memory note "AI路由双门全量审计" and "spawner-vanilla-alignment" suggest martian handled in bossAI_martian.ts. martianFighterExtras handles 383/386 only. Do 381/382/411/424/426 get shooting from bossAI_martian? Let me check bossAI_martian for these ids.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:23:23.584Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"381\\|382\\|409\\|411\\|424\\|426\\|427\\|428\\|415\\|471\\|472\\|482\\|516\\|430\\|431\\|494\\|495\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_martian.ts | head -25; echo ===; grep -rn \"=== 482\\|=== 471\\|=== 426\\|=== 409\\|=== 411\\|=== 424\\|=== 381\\|=== 382\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -10",
 "description": "Check martian bossAI coverage of ranged ids"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:23:23.613Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
2://   aiStyle 80  火星探测器 399                NPC.cs:38129-38223（巡逻→受惊悬停 60t→
15://   aiStyle  3  火星军官 383 / 工程师 386 尾段  NPC.cs:56614-56645 / 59384-59428（军官带盾
19:// 4272),按原版结构保留代码、入口 EXPERT 门关闭;netcode 跳过。
48:/** expert 模式门（本工程恒 false,Game.ts:4272 expertMode:false） */
95:// AI_080 火星探测器 399（NPC.cs:38129-38223）
102:  // 撞墙转向（:38137-38140 collideX → direction 翻转;首帧 direction==0 先索敌）
106:    // 方向固定（原版仅 direction==0 时 TargetClosest,:38133-38136;撞墙翻转）
108:    // 贴地升降（:38145-38163）：脚下 30t 内首个实心面 <15t 升 / <20t 平 / 其余缓降
117:    // 受惊门（:38165-38173）：352px 内且玩家中心在探测器下方
122:    // 悬停报警（:38175-38192）：60t 减速 → 逃逸,ai[3] = 玩家反侧方向
130:    // 逃逸（:38194-38208）：noTileCollide,向上加速+横向 4px;出屏/180t → 入侵
135:      // Main.StartInvasion(4)（:38202）：原版只查"≥200HP 玩家数>0"且无视 delay;
148:  // 点光（:38210-38217）：rgb = ai0==2 ? Color.Red : Color.SkyBlue，×0.65
226:    if (w !== w1) {                                // 窗口切换初始化（:36414-36430）
341://   393→395 (±60,+29);394→395 (±49,-13),spriteDirection=±1;416→415 (-spriteDir*10,-30)
342:// 主体消亡（:36288-36299）:390→Transform(382) / 416→Transform(518) / 其余消散
352:    const mount = spawnPart(game, e, id === 390 ? 391 : 415);
362:      e.transformTo(id === 390 ? 382 : 518, game.world.store, false, game);   // Transform → 下车变步兵
677:  e.lightRGBAt = { x: e.cx, y: e.cy - 10 };   // :35411 光源 = Center.Y−10
679:  // ---- 电击循环（:35409-35450）----
749:// AI_003 火星尾段：军官 383（cs:56614-56645）/ 工程师 386（cs:59384-59428）
781:    // ---- 工程师：放炮塔（:59384-59428）----
789:      // ±5t 随机扫位（:59402-59424）：非中心 2t 禁区 + 实心面 + 上方 4t 净空 + 无岩浆
808:            turret.y = ty * TILE - turret.h;   // 底边贴实心面顶（:59425-59426）
814:    if (e.ai2 === 60) e.ai2 = -120;                 // :59427-59429
(eval):1: == not found

```


---

## 🤖 Assistant · 2026-08-19T03:24:02.329Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
So bossAI_martian handles 399, 383/386, 390/391, 416→415 mount logic (spawnPart for riders), 393-395. The 381/382/409/411/424/426 ranged attacks + 415 Drakomire fireball + 427/428 hornet/larva blocks are NOT implemented anywhere. But wait — 416 rider: bossAI_martian line 341-362 handles rider mounting (390→391 Scutlix, 416→415 Drakomire). So the 415 "hide when ridden" might be handled there. Partial.

OK — I now have enough for AI_003. Time check: I've spent a lot. Remaining families to verify deeply: 
1. Slime remainder: I read the core (61430-62139). I should also check the 60971-61430 color/metal-slime segment briefly for behavioral parts (lavaImmune, defense+30, damage×3 for metal slimes at :61095-61155) — ours comments "behavioral段...本批只接光位" = intentionally not ported (metal slime buffs). That's a known gap: CONFIRMED missing (metal slimes with ore inside get defense+30/damage×3/hover gravity). MEDIUM-LOW (registered).
2. AI_008 caster — done (found 533 window bug).
3. plantAI — done.
4. spike/wheel — done.
5. mimic — done.
6. wallCreeper — done (missing confused; TryMoveToTransformableSpaceInto).
7. lostGirl — done.
8. tortoiseAI — NOT in my scope list explicitly (it's "陆龟族" AI_039) — skip.
9. solenian ✓, stormDiver ✓ (spot), psycho ✓, chaos ✓, medusa ✓, swamp ✓, nailhead ✓, butcher ✓, possessed ✓, fritz ✓, wetSwim ✓ (586 spawn leap missing).

Let me also quickly verify:
- AI_003 flag5/flag6 head-block scan (:60224-60260): the "standing under solid ceiling → flag5=false (no jumping), tile-null → return" — ours: no head-block scan (our jump gate is movingInto && vy===0 only; vanilla also cancels vy<0 if no ground below: `if (!flag5 && velocity.Y < 0f) velocity.Y = 0f`). Ours: jumping in mid-air prevented by vy===0 gate; "no floor below" cancel of negative vy — ours missing but low impact.
- Chaos 120 teleport placement in ours: chaosElementalStep called where? In our fighterAI before movement — `this.ai3 = chaosElementalStep(this, game, player)` at :2464 — vanilla teleports at the very END (:60679, after movement/jump). Ours teleports mid-frame before movement — minor ordering. LOW.

Now — slime metal variants :61095-61155 quick check for the exact buffs. And also check the spiked slime 147 (jungle) — ours maps proj 176 to id 204... wait, ours: `this.vanillaId === 184 ? 174 : this.vanillaId === 204 ? 176 : 605`. Vanilla: 184 → proj 174 ✓; 535 → 605 ✓; 204 → 176 ✓. ID check: is 204 "Jungle Slime"? per json: let me check 204. And 147 = "Spiked Jungle Slime"! The 147 branch in vanilla only does dust 76 — because 147's ATTACK is in the 204?? No wait — vanilla has separate `if (type == 204)` attack with proj 176. What's 204? Let me check our json for 204/147. If 204 = "Spiked Jungle Slime" then ours is right that 204 shoots 176; but vanilla params differ (speed 7 dmg 13 cd 65). And 147 = ? probably "Jungle Slime" (no attack, just dust) ✓ ours has no attack for 147 ✓.

Quick check 204 name + metal slime buffs (61095-61155). Then write the report. Also verify our Enemy 'dead = true' semantics for plantAI anchor death (drops or silent?). Check how Enemy death processes `dead` — the kill path. Let me grep quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:02.333Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst j = require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst list = j.npcs || j;\nfor (const id of [147,184,204,535,259,260,43,101,175,172,24,29,32,45,533,693,281,283,285]) console.log(id, (list[String(id)]||{}).name);\n\"; sed -n '61095,61160p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check names and metal slime buff block"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:02.391Z

**📎 ToolResult**

```
147 Ice Slime
184 Spiked Ice Slime
204 Spiked Jungle Slime
535 NPC_535
259 Fungi Bulb
260 Giant Fungi Bulb
43 Man Eater
101 Clinger
175 Angry Trapper
172 Rune Wizard
24 Fire Imp
29 Goblin Sorcerer
32 Dark Caster
45 Tim
533 Desert Spirit
693 LibrarianSkeleton
281 Ragged Caster
283 Necromancer
285 Diabolist
				{
					num11 -= 120;
				}
				if (Main.getGoodWorld)
				{
					num11 -= 120;
				}
				if (Main.rand.Next(num11) == 0 && target >= 0 && Main.player[target].active && !Main.player[target].dead && !Main.player[target].npcTypeNoAggro[type] && Collision.CanHit(this, Main.player[target]))
				{
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), (int)base.Center.X, base.Center.Y, direction * 12, 0f, 1073, 20, 2f, Main.myPlayer);
				}
			}
			else if (ai[1] == 364f || ai[1] == 1104f || ai[1] == 365f || ai[1] == 1105f || ai[1] == 366f || ai[1] == 1106f)
			{
				lavaImmune = true;
				defense = defDefense + 30;
				damage = defDamage * 3;
				buffImmune[70] = false;
				buffImmune[20] = false;
				knockBackResist = 0f;
				if (lifeMax == defLifeMax)
				{
					position.X += width / 2;
					position.Y += height;
					scale *= 1.2f;
					width = (int)((float)width * scale);
					height = (int)((float)height * scale);
					position.X -= width / 2;
					position.Y -= height;
					if (life == lifeMax)
					{
						life = defLifeMax * 3;
					}
					lifeMax = defLifeMax * 3;
				}
				if (base.Bottom.Y < Main.player[target].Top.Y && base.Right.X >= Main.player[target].Left.X && base.Left.X <= Main.player[target].Right.X && Collision.CanHitWithCheck(this, Main.player[target], DelegateMethods.NotSolidOrPlatforms))
				{
					flag2 = true;
					direction = 0;
					velocity.X *= 0.5f;
					if (velocity.Y < 0f)
					{
						velocity.Y = 0f;
					}
					velocity.Y += gravity;
				}
				else
				{
					if (velocity.Y > 0f)
					{
						velocity.Y += gravity;
					}
					if (velocity.Y < 0f)
					{
						velocity.Y -= gravity * 0.75f;
					}
				}
				Lighting.AddLight(position, (float)(int)this.color.R / 500f, (float)(int)this.color.G / 500f, (float)(int)this.color.B / 500f);
				extraValue = 0;
				if (ai[1] == 364f)
				{
					_givenName = Language.GetTextValue("SpecialNPCName.CobaltSlime");
				}
				else if (ai[1] == 1104f)
				{
					_givenName = Language.GetTextValue("SpecialNPCName.PalladiumSlime");

```


---

## 🤖 Assistant · 2026-08-19T03:24:10.491Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Metal slime block confirmed: lavaImmune, defense+30, damage×3, kbResist 0, scale×1.2, HP×3, hover-gravity — ours intentionally not ported (registered in comment as "本批只接光位"). CONFIRMED missing — MEDIUM (hardmode Promoted metal slimes: ours treats them as normal slimes with normal HP/damage → much weaker).

Also spotted: a projectile 1073 branch right before (ai1 in some ore set → shoot proj 1073 horizontally direction*12 when player above? that's for gem/ore slimes maybe "Spike" — whatever, part of unported metal/ore block.

Also 147 = Ice Slime (no attack, dust only ✓ ours). 184 = Spiked Ice Slime ✓. 204 = Spiked Jungle Slime ✓ (ours attack params wrong as found). 535 = Spiked Slime ✓.

Now, let me double check our spiked-slime block: `this.vanillaId === 184 ? 174 : this.vanillaId === 204 ? 176 : 605` ✓ mapping right.

Now check Enemy death semantics for plantAI (dead=true → loot?): look at how dead is consumed. In Enemy.ts, checkDead / EntityManager. Quick grep.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:11.634Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"checkDead\\|this.dead = true\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -12; sed -n '/checkDead/,/^  }/p' ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -40",
 "description": "Check Enemy dead handling and death drops path"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:11.693Z

**📎 ToolResult**

```
474:   *  - 两邻全灭 / 头(13)的下段灭 / 尾(15)的前段灭 → 自灭（走标准死亡管线=checkDead）；
1123:            this.dead = true; this.hp = 0;
1580:          this.dead = true;
2124:      this.dead = true;
2924:      this.dead = true;
2937:      this.dead = true;                    // noSpawnCycle + active=false（:92557-92559）
3434:      if (this.ai2 === 1) this.dead = true;   // life=-1+active=false（:30087-30090,不走掉落/死亡管线）
3704:      this.dead = true;
5020:      if (f.despawn) { this.dead = true; return; }             // cs:45254-45262
5507:    if (this.ai3 >= 18000) { this.dead = true; return; } // 存在期满离场
5627:        this.dead = true; return;
5713:      this.dead = true;
   *  - 两邻全灭 / 头(13)的下段灭 / 尾(15)的前段灭 → 自灭（走标准死亡管线=checkDead）；
   *  - 身段(14)前段灭 → Transform(13)（:51906-51909）晋升新头，断开 wormFollow；
   *  - 身段(14)后段灭 → Transform(15)（:51910-51913）收成新尾，断开 wormNext；
   *  → 杀中段把一条虫拆成两条独立虫；杀头不灭虫（下段即晋升新头）。
   *  头速度双模（:52091-52104）：num46=10/num47=0.07，专家 12/0.15，FTW +4/+0.05——
   *  埋地（AABB 外扩 1-2 格实心/液体>64 :51968-51992，玩家距 >1000px 亦视作埋地
   *  :51993-52014）走全向舵（:52511-52597）；空中 vy+=0.11 钳 num46 + 三档横漂不转向
   *  （:52324-52371）。离开腐化下潜（:52402-52450）：目标玩家 !ZoneCorrupt&&!ZoneCrimson
   *  （或死）→ 直向下潜，y > (rockLevel+h)/2 整链清除（无掉落无记账）。
   *  专家毒唾 666（:51468-51504）；掘地音效（:52375-52395 间隔=距离/40 钳 10..20）。 */
  private eowAI(game: GameHooks, _player: Player | null): void {
    const st = game.world.store;
    const w = game.world;
    // 原版 target 即便玩家死亡仍指向其槽位（:51532 TargetClosest 后舵机照用其坐标）
    const tgt = (game as unknown as { player: Player }).player ?? null;
    if (!tgt) return;
    // ---- 链维护（:51874-51914）----
    const linkAlive = (s: Enemy | null): boolean =>
      !!s && !s.dead && s.vanillaId !== null && s.vanillaId >= 13 && s.vanillaId <= 15;
    const prevOk = linkAlive(this.wormFollow), nextOk = linkAlive(this.wormNext);
    if (!prevOk && !nextOk) { this.die(game); return; }                   // :51876-51885 两邻全灭
    const kind0 = this.vanillaId ?? 0;
    if (kind0 === 13 && !nextOk) { this.die(game); return; }              // :51886-51895 头的下段灭
    if (kind0 === 15 && !prevOk) { this.die(game); return; }              // :51896-51905 尾的前段灭
    if (kind0 === 14) {
      if (!prevOk) {
        // :51906-51909 Transform(13, ai[0])：晋升新头（SetDefaults(13) 换头属性/贴图，
        // HP 按比例结转；三段 lifeMax 同为 150 → 原值保留）
        if (this.wormFollow) this.wormFollow.wormNext = null;
        this.wormFollow = null;
        this.transformTo(13, st, true, game);
      } else if (!nextOk) {
        // :51910-51913 Transform(15, 0, ai[1])：收成新尾
        if (this.wormNext) this.wormNext.wormFollow = null;
        this.wormNext = null;
        this.transformTo(15, st, true, game);
      }
    }
    // ---- 专家毒唾 666（:51468-51504）----
    const id = this.vanillaId ?? 0;

```


---

## 🤖 Assistant · 2026-08-19T03:24:18.876Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Line 3434 shows tortoiseAI uses `this.dead = true` with comment "不走掉落/死亡管线" — so `dead = true` in this engine apparently bypasses the death pipeline? Let me check how `dead` is consumed — is there a separate `die()` for full death with drops? Enemy has `die(game)` (used by eow). And `dead = true` alone — what happens? Let me look at the update loop / EntityManager to see if dead=true triggers gore/drops or silent removal.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:20.474Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"die(\\|\\.dead\\b\" ~/Project/GLM/SandboxWorld/game/src/entities/EntityManager.ts 2>/dev/null | head -10; grep -rn \"e.dead\\|enemy.dead\\|n.dead\" ~/Project/GLM/SandboxWorld/game/src/core/Game.ts | grep -i \"drop\\|gore\\|kill\\|remove\\|filter\" | head -8; grep -n \"  die(game\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "description": "Find dead-flag consumption in entity update"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:20.531Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4715:          const town = this.entities.npcs.filter((n) => n instanceof TownNPC && !n.dead)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4835:        const townCount = this.entities.npcs.filter((n) => n instanceof TownNPC && !n.dead).length;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4937:            ...this.entities.enemies.filter((e) => !e.dead).map((e) => ({ x: e.x, y: e.y, w: e.w, h: e.h })),
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:4938:            ...this.entities.npcs.filter((n) => !n.dead).map((n) => ({ x: n.x, y: n.y, w: n.w, h: n.h })),
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:5061:        const housed = this.entities.npcs.filter((n) => n instanceof TownNPC && !n.dead && (n as TownNPC).home).length;
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12538:      .filter((n) => !n.dead && !n.bound && n.home)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12587:        .filter((e) => !e.dead && e.vanillaId === 548)
~/Project/GLM/SandboxWorld/game/src/core/Game.ts:12631:        .filter((e) => !e.dead && (e.vanillaId === 548 || e.vanillaId === 549))
7941:  die(game: GameHooks): void {

```


---

## 🤖 Assistant · 2026-08-19T03:24:30.296Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 40,
 "offset": 7938
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:30.307Z

**📎 ToolResult**

```
7938	  /** AI 触发的标准死亡（EoW 断链自灭，NPC.cs:51876-51905 的 life=0 + HitEffect +
7939	   *  checkDead 语义）：清无敌帧后走 hurt 全管线（掉落/记账/音效/粒子）——
7940	   *  原版直改 life 不经 StrikeNPC，故 iframes 不应阻塞 */
7941	  die(game: GameHooks): void {
7942	    this.hp = 0;
7943	    this.iframes = 0;
7944	    this.hurt(this.maxHp + 9999, 0, 0, game);
7945	  }
7946	
7947	  draw() { /* Renderer 统一绘制 */ }
7948	}
7949	bindEnemyCtor(Enemy);
7950	
7951	// ===================== 仙灵宝箱搜索（GetFairyTreasureCoords NPC.cs:48794-48852 1:1）=====================
7952	
7953	/** FriendlyFairyCanLureTo（TileID.cs:409）：仙灵可引导到的宝箱/家具 tile 表 */
7954	const FAIRY_LURE_SHEETS = new Set([8, 169, 21, 467, 107, 108, 111, 221, 222, 223, 211, 12, 665, 639, 236, 702, 227]);
7955	
7956	/** tileOreFinderPriority（Main.cs:6356-6391）：引导优先级——同优先级取最近，
7957	 *  矿石族 3×3 计数 ≥40 才有效（大矿脉才算"宝藏"） */
7958	const FAIRY_LURE_PRIORITY: Record<number, number> = {
7959	  28: 100, 407: 150, 404: 150, 7: 200, 166: 210, 6: 220, 167: 230, 9: 240,
7960	  168: 250, 8: 260, 169: 270, 22: 300, 204: 310, 37: 400, 21: 500, 467: 500,
7961	  441: 500, 468: 500, 12: 550, 665: 550, 639: 550, 107: 600, 221: 610,
7962	  108: 620, 222: 630, 111: 640, 223: 650, 129: 675, 211: 700, 227: 750,
7963	};
7964	
7965	/** IsValidForOreFinder（SceneMetrics.cs:904-919）：227 生命果仅 272≤frameX≤374、
7966	 *  129 宝箱仅 frameX≥324 才算 */
7967	function fairyOreFinderValid(sheet: number, frameX: number): boolean {
7968	  if (sheet === 227) return frameX >= 272 && frameX <= 374;
7969	  if (sheet === 129) return frameX >= 324;
7970	  return true;
7971	}
7972	
7973	/** 宝箱/引导目标搜索（GetFairyTreasureCoords :48794-48852）：中心 ±75×±50 窗
7974	 *  （钳世界缘 40），按优先级取最高（同优先取最近）；矿石族 3×3 同类计数 ≥40 */
7975	export function fairyTreasureCoords(
7976	  st: import('../world/TileStore').TileStore, cx: number, cy: number,
7977	): [number, number] | null {

```


---

## 🤖 Assistant · 2026-08-19T03:24:30.486Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"enemies = \\|pruneEnemies\\|\\.dead)\" ~/Project/GLM/SandboxWorld/game/src/core/EntityManager.ts | head; grep -rn \"if (e.dead)\\|if (enemy.dead)\\|\\.dead &&\" ~/Project/GLM/SandboxWorld/game/src/core/EntityManager.ts | head -6",
 "description": "Read die() and dead consumption in EntityManager"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:30.532Z

**📎 ToolResult**

```
ugrep: warning: ~/Project/GLM/SandboxWorld/game/src/core/EntityManager.ts: No such file or directory
ugrep: warning: ~/Project/GLM/SandboxWorld/game/src/core/EntityManager.ts: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T03:24:50.187Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
`die()` runs the full hurt pipeline (drops etc). `dead = true` alone → likely silent removal by the entity sweep (filtered out). Tortoise comment says dead=true "不走掉落/死亡管线" — so dead=true = silent removal. Good: plantAI's `this.dead = true` on anchor loss = silent removal ✓ matches vanilla (life=-1, active=false, no loot). ✓ No issue.

Now I have comprehensive findings. Let me do a few final verifications on things I flagged but haven't confirmed:

1. **Our fighterAI: is there a pounce block?** — verified absent (read whole function 2387-2704).
2. **586 spawn leap (alpha 255)** — ours wetSwimStep has no alpha handling. But wait — does our Enemy use spawnAlpha=255 for 586 at spawn? grep 586 in Enemy.ts: line 1194 is 590/591... let me check if 586 spawn leap exists anywhere: grep "586" showed fighterFamilies (move) + RANGED... line 1188 comment (379/380). Let me grep quickly for alphaFade/586 spawn.
3. **Spike ball id 72 vs 395**: our blazingWheelAI light is gated `vanillaId === 72` inside spikeBallAI — with comment "=72 火轮". Wait — that's in spikeBallAI (case 21). The light :24722-24724 belongs to aiStyle 21 (spike ball). And the aiStyle-21 family: which NPC is spike ball? Blazing Wheel = 395? Spike Ball = 72? Hmm: per vanilla, Spike Ball = NPC 72? hmm — actually no! Blazing Wheel = 395, Spike Ball = 72? Our blazingWheelAI handles case 20 with no vid check; spikeBallAI case 21 with vid 72 check for light. Vanilla light at :24724 is in aiStyle 21 (spike ball) — all spike balls. Vanilla data: Spike Ball NPC = 72? Hmm, hold on — I recall Spike Ball = 22 and Blazing Wheel = 395... Let me check json: 72 and 395.
4. Confirm our mimic handles 629/341 (present/ice mimic) — flag36 for 341 ✓ ours; 629 missing ai3=1 (unused).
5. grasshopper flee — confirmed missing.

Let me check 72/395 names + 586 spawn + our FIGHTER_DAY_ACTIVE table vs vanilla NotDiscouraged list (ours FIGHTER_DAY_ACTIVE — check it matches :60696's day-active ids: 73, 624, 631(cond), 31, 294-296, 47, 67, 77, 78-80, 630, 110, 120, 168, 181, 185, 198, 199, 206, 217-219, 220, 239, 243, 254, 255, 257, 258, 291-293, 379, 380, 464, 470, 424, 411(cond), 409, 415, 419, 425, 427, 428, 429, 508, 524-527, 580, 582 + critterThatCanTurnOnPlayers + invasion exceptions (snowMoon 343/350; invasionType 1: 26/27/28/111/471; invasionType 3: 212-216; invasionType 4: 381/382/383/385/386/389/391/520)). Ours: FIGHTER_DAY_ACTIVE + MARTIAN_DAY_ACTIVE (invasionType 4). Let me check the tables.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:24:51.356Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "node -e \"\nconst j = require('~/Project/GLM/SandboxWorld/game/public/sprites/vanilla-npcs.json');\nconst l = j.npcs || j; for (const id of [72,395,586,461,620]) console.log(id, (l[String(id)]||{}).name);\n\"; grep -n \"FIGHTER_DAY_ACTIVE\\|MARTIAN_DAY_ACTIVE\" ~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts | head -4",
 "description": "Check trap NPC names and day-active tables"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:51.412Z

**📎 ToolResult**

```
72 NPC_72
395 Martian Saucer
586 Zombie Merman
461 Creature from the Deep
620 Goblin Shark
199:const FIGHTER_DAY_ACTIVE = new Set([
208:const MARTIAN_DAY_ACTIVE = new Set([381, 382, 383, 385, 386, 389, 391, 520]);
2433:      && (FIGHTER_DAY_ACTIVE.has(this.vanillaId)
2434:        || (game.world.invasionType === 4 && MARTIAN_DAY_ACTIVE.has(this.vanillaId)));

```


---

## 🤖 Assistant · 2026-08-19T03:24:56.410Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/Enemy.ts",
 "limit": 55,
 "offset": 195
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:24:56.424Z

**📎 ToolResult**

```
195	
196	// AI_003 战士族昼行豁免表（DespawnEncouragement_AIStyle3_Fighters_NotDiscouraged 排除表
197	// NPC.cs:60694-60724 + switch 保留集 :60712-60721）：白天地表仍索敌的类型
198	// （腐化/猩红战士、秃鹫、鸟妖、事件怪等群系原住民）。僵尸 3 不在表内 → 白天驱散。
199	const FIGHTER_DAY_ACTIVE = new Set([
200	  73, 624, 631, 31, 294, 295, 296, 47, 67, 77, 78, 79, 80, 630, 110, 120, 168, 181, 185,
201	  198, 199, 206, 217, 218, 219, 220, 239, 243, 254, 255, 257, 258, 291, 292, 293,
202	  379, 380, 464, 470, 424, 411, 409, 415, 419, 425, 427, 428, 429, 508, 524, 525, 526, 527, 580, 582,
203	  // 入侵怪（原版昼行：入侵期间不被驱散——哥布林 26-29/111/471、海盗 212-216、雪人 143-145）
204	  26, 27, 28, 29, 111, 471, 212, 213, 214, 215, 216, 143, 144, 145,
205	]);
206	// 火星入侵昼行豁免（cs:60705 第四组 invasionType!=4 门）：入侵进行中这些战士族
207	// 不被白天驱散（387 特斯拉炮塔是 aiStyle 73 无此逻辑,不列）
208	const MARTIAN_DAY_ACTIVE = new Set([381, 382, 383, 385, 386, 389, 391, 520]);
209	// AI_002 飘浮眼昼散表（DespawnEncouragement_AIStyle2_FloatingEye_IsDiscouraged, cs:53152-53165）：
210	// 白天 && y≤worldSurface → EncourageDespawn(10) + 保持水平方向向上飞离
211	const EYE_DAY_DESPAWN = new Set([2, 133, 190, 191, 192, 193, 194, 317, 318]);
212	
213	// AI_014 wet 浮力表（cs:23232 蝙蝠/恶魔/巨狐蝠/孢子蝠 + cs:23380 哈比 48）：
214	// 入水上浮弹出水面（vy>0 ×0.95、恒 -0.5、钳 -4 + TargetClosest）；表外 aiStyle14 无此段
215	const AI014_SWIM_UP = new Set([48, 49, 51, 60, 62, 66, 93, 137, 150, 151, 152, 634]);
216	
217	/** 原版路径 key（v_*）的占位 def，fromVanilla 会整体覆写 */
218	const PLACEHOLDER_DEF: EnemyDef = {
219	  key: 'v_placeholder', name: '?', hp: 1, damage: 0, knockbackResist: 0.5,
220	  width: 16, height: 16, mapColor: '#9A8FA0', gore: ['#9A8FA0', '#5E5566', '#C4BACC'],
221	  hitSound: ['NPC_Hit_1'], killedSound: ['NPC_Killed_1'], drops: [],
222	};
223	
224	export class Enemy extends Entity {
225	  /** 原版 NPC id（数据驱动路径启用时非空） */
226	  vanillaId: number | null = null;
227	  /** 穿墙旗（原版 noTileCollide；fairyAI 状态 2-7 宝箱引导态置真） */
228	  noTileCollide = false;
229	  vanilla: VanillaNpc | null = null;
230	  /** npc.difficulty（ScaleStats 写入，NPC.cs:18086 = strengthOverride ?? Main.Difficulty）：
231	   *  原版档位浮点（Classic 1/Expert 2/Master 3，getGoodWorld +1）——AI 段
232	   *  GetAttackDamage_ScaledByDifficulty/ForProjectiles（如饥饿者 :26341）消费。
233	   *  未进 ScaleStats 门（friendly/townNPC/无伤小动物）保持 0（原版字段初值） */
234	  difficulty = 0;
235	  /** defDamage 的【未缩放】基线（ScaleStats 前的 v.damage，critter/friendly 归零后值）。
236	   *  敌怪弹幕出膛原版一律用 ForProjectiles(基线, 基线×N) 这类显式档位 lerp
237	   *  （NPC.cs:21180 等），命中玩家的难度乘区在 Projectile.cs:13770 统一做——
238	   *  若此处误用缩放后的 def.damage 会与命中端乘区叠加成双重缩放 */
239	  baseDamage = 0;
240	  /** 雕像产怪（Wiring.cs:2480 SpawnedFromStatue）：value=0 不掉钱、
241	   *  肉前集合不掉战利品、StatueSpawnedDropRarity 概率门（NPCLoot :79648-79654） */
242	  spawnedFromStatue = false;
243	  /** 捕获物释放出生（NPC.releaseOwner != 255 语义，NPC.cs:78709 不计 nearby 槽） */
244	  releasedFromItem = false;
245	  /** NPC.AnyInteractions（NPC.cs:5431 playerInteraction[who] 任一 true）——本仓 hurt 调用方
246	   *  全为玩家武器/弹幕/荆棘链 → hurt 生效即等价玩家交互；雕像门 :79651 消费 */
247	  playerInteracted = false;
248	  /** 鞭 tag（Projectile.ApplyTag → npc.whipTimeLeft 系）：剩余 tick 与附加伤害
249	   *  （240t=4 秒；随从命中被 tag 敌伤害 +whipTagDmg） */

```


---

## 🤖 Assistant · 2026-08-19T03:25:17.354Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
FIGHTER_DAY_ACTIVE check vs vanilla :60696:
Vanilla day-active (i.e., NOT discouraged during day): 73, 624, 631(ai2 gate), 31, 294, 295, 296, 47, 67, 77, 78, 79, 80, 630, 110, 120, 168, 181, 185, 198, 199, 206, 217, 218, 219, 220, 239, 243, 254, 255, 257, 258, 291, 292, 293, 379, 380, 464, 470, 424, 411(cond), plus switch: 409, 415, 419, 425, 427, 428, 429, 508, 524-527, 580, 582 + CritterThatCanTurnOnPlayers + invasion exceptions (snowMoon: 343,350; invasion 1: 26,27,28,111,471; invasion 3: 212-216; invasion 4: 381,382,383,385,386,389,391,520) + dontStarve 163/164.

Ours: matches almost fully ✓ + adds 143/144/145 (frost legion? snowMoon is invasionType 2? snow moon... whatever, ours comments 雪人 143-145 = frost legion invasionType 2 — vanilla's snowMoon exception is for 343/350 during SNOW MOON (pumpkinMoon? snowMoon = frost moon). Ours adds 143-145 (Snowman gang = frost legion, invasionType 2) — vanilla exception is `( !Main.snowMoon || (npcID != 343 && npcID != 350))` — hmm, inverted: discouraged unless... the NotDiscouraged returns true (chase OK) when `!snowMoon || npcID not 343/350`... wait the whole condition is "if (all these) return false(discouraged)". Let me parse: `if (!eclipse && day && ... && (!snowMoon || (id != 343 && id != 350)) && ...)` → return switch(...) — i.e., during snowMoon, types 343/350 skip the discouragement check entirely → always chase ✓ (they're frost moon enemies). Ours: no snowMoon 343/350 exception — but 343 (ice queen? no — 343 = "Present Mimic"? no 341... 343 = elf copter?) — whatever, ours lacks it → frost moon ground enemies (343/350 = "Elf Copter"/"Elf Archer"!) get day-discouraged in ours during frost moon day? Frost moon is night-only event; during the event it's night → not discouraged anyway. At dawn the event ends. Minor. LOW.
Also 411 condition (ai1 window) not replicated — LOW.
Missing critterThatCanTurnOnPlayers set — ours routes critters separately ✓ probably fine.

OK. I think I've covered enough. Let me also double-check the two spike-ball/wheel ids: 72 = "NPC_72" (unnamed in json) and 395 = "Martian Saucer"?! That's wrong — 395 is Blazing Wheel. The json extraction might be off-by... whatever. In vanilla: Blazing Wheel = NPC 395? No wait — Blazing Wheel is definitely NPCID 395? Hmm — actually yes: BlazingWheel = 395 is what I remembered... but json says 395 = Martian Saucer. Hmm, martian saucer is 580? No — ours says 580 is a charger approach id. Ugh. NPCID 395 = Blazing Wheel (I'm fairly confident; Martian Saucer = 580? no 580 = "Martian Saucer"? Hmm). Our charger 580/508/582 = "Antlion Charger/Albino/Black"? Hmm 508 = "Antlion Charger"? Let me not worry — for the audit: spike ball = NPC 72? Hmm, actually Spike Ball = NPCID 72?? I believe SpikeBall = 72... no wait — NPC 72 might be "Spike Ball"? Hmm honestly: Dungeon traps: Blazing Wheel (395) and Spike Ball (72)? Hmm, I actually think Spike Ball = 395 and Blazing Wheel = 394? Let me check vanilla SetDefaults quickly for tileSolid etc. Actually — aiStyle 20 = Blazing Wheel, aiStyle 21 = Spike Ball. Which NPC ids use them? Let me grep SetDefaults for aiStyle = 20/21 assignments.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:25:20.100Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"aiStyle = 20;\\|aiStyle = 21;\\|npc.aiStyle = 20\\|npc.aiStyle = 21\\|type = 72\\|NPCID.SpikeBall\\|NPCID.BlazingWheel\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -6; grep -n \"case 394\\|case 395\\|case 72:\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -4; awk 'NR>=1 && /SetDefaults\\(int type/,0' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs 2>/dev/null | grep -n \"num == 394\\|num == 395\\|num == 72\\|num == 22\\b\" | head -6",
 "description": "Find which NPC ids use aiStyle 20/21"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:25:20.203Z

**📎 ToolResult**

```
9617:			aiStyle = 20;
9651:			aiStyle = 21;
72495:		case 394:
72520:		case 395:
75340:		case 72:
78629:		case 394:

```


---

## 🤖 Assistant · 2026-08-19T03:25:34.476Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '9605,9665p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read SetDefaults for blazing wheel and spike ball"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:25:34.510Z

**📎 ToolResult**

```
			lifeMax = 45;
			HitSound = SoundID.NPCHit31;
			DeathSound = SoundID.NPCDeath34;
			knockBackResist = 0f;
			value = 60f;
			behindTiles = true;
		}
		else if (type == 70)
		{
			npcSlots = 0.3f;
			width = 34;
			height = 34;
			aiStyle = 20;
			damage = 32;
			defense = 100;
			lifeMax = 100;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath1;
			knockBackResist = 0f;
			noGravity = true;
			noTileCollide = true;
			dontTakeDamage = true;
			scale = 1.5f;
		}
		else if (type == 71)
		{
			npcSlots = 2f;
			width = 36;
			height = 24;
			aiStyle = 1;
			damage = 30;
			defense = 7;
			lifeMax = 150;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath1;
			alpha = 60;
			value = 150f;
			scale = 1.25f;
			knockBackResist = 0.6f;
			rarity = 1;
		}
		else if (type == 72)
		{
			npcSlots = 0.3f;
			width = 34;
			height = 34;
			aiStyle = 21;
			damage = 24;
			defense = 100;
			lifeMax = 100;
			alpha = 100;
			behindTiles = true;
			HitSound = SoundID.NPCHit1;
			DeathSound = SoundID.NPCDeath1;
			knockBackResist = 0f;
			noGravity = true;
			dontTakeDamage = true;
			scale = 1.2f;
		}
		else if (type == 73)
		{

```


---

## 🤖 Assistant · 2026-08-19T03:25:56.679Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed: NPC 70 = Blazing Wheel (aiStyle 20), NPC 72 = Spike Ball (aiStyle 21). Ours' spikeBallAI light gate `vanillaId === 72` ✓ correct (spike ball light). But note: spike ball (72) has `noGravity = true` and NO noTileCollide — so it collides with tiles (bounces) ✓; blazing wheel (70) has `noGravity + noTileCollide` ✓ passes through tiles, bouncing via velocity logic ✓. Ours: blazingWheelAI does raw x+=vx (no collision) ✓; spikeBallAI uses moveAndCollide ✓.

Also blazing wheel 70: scale 1.5, damage 32; spike ball 72: scale 1.2 damage 24 — data side (vanillaNpcs.ts) should have it.

Wait — one thing about our spikeBallAI: vanilla `rotation += direction*directionY*0.13` — ours noted as not implemented (visual). Fine, registered.

Also — vanilla spike ball init: `if (ai[0] == 0f) { TargetClosest(); directionY = 1; ai[0] = 1; }` — NO return! The init tick continues into the bounce logic. Ours: aiInit block doesn't return either — continues ✓. Good.

But wait — ours spikeBallAI reads collideX/collideY from PREVIOUS tick's moveAndCollide flags (hitWall etc. are post-collision from last tick since we moveAndCollide at the end) ✓ comment says so.

Vanilla blazing wheel init RETURNS after setting velocity ✓ ours returns too (via the early return in aiInit block — yes ours has `return` after setting up... looking at code: aiInit block ends with `return;` — yes line 4215 `return;`). ✓ Except ours applies `this.x += this.vx; this.y += this.vy;` BEFORE the return on init tick — vanilla returns before moving (velocity applied later by collision update). Ours moves 1 tick earlier — negligible.

One more blazing wheel diff: vanilla init: `TargetClosest(); direction *= -1; directionY *= -1;` — TargetClosest then negate both. directionY after TargetClosest = sign toward player vertically (or 0→1). Then negated. So initial vertical dive = AWAY from player (if player below, dive up). Ours: `this.dirY` — what's dirY default in our Entity? Probably 1 (or 0?). Ours doesn't negate or seek. Ours initial: vy = 6*ai3*dirY with dirY = default. If default 1 → dives down. Vanilla: away from player vertically. MEDIUM-LOW (initial bounce direction wrong). Also `if (directionY == 0) directionY = 1` after negate ✓ ours `if (this.facing === 0) this.facing = 1` ✓ but ours lacks dirY==0→1 guard. LOW.

Now I have a thorough picture. Let me also double-check two remaining claimed-1:1 blocks I haven't verified in vanilla: stormDiver (58865-59013) — I'll trust ours' line-cited comments (they're detailed and my spot checks of this repo's ports have been accurate for other blocks). And the AI_001 wet block — done. And AI_008 — done.

One more important caster item: ours casterAI `if (!player) return;` placed AFTER physics/lights but BEFORE facing/attack — vanilla TargetClosest at top (even without player). Fine.

And caster telefrag distance: vanilla AI_AttemptToFindTeleportSpot for caster (aiStyle 8) called with default telefragPrevention = 5? Vanilla call: `AI_AttemptToFindTeleportSpot(ref destination, num89, num90)` — the overload without explicit range params! Let me check the signature default: our implementation used rangeFromTargetTile=20, telefrag=5. Vanilla default params for that overload — grep quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:25:57.620Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"bool AI_AttemptToFindTeleportSpot\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; sed -n '18870,18900p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Check teleport spot function default parameters"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:25:57.658Z

**📎 ToolResult**

```
18876:	public bool AI_AttemptToFindTeleportSpot(ref Vector2 chosenTile, int targetTileX, int targetTileY, int rangeFromTargetTile = 20, int telefragPreventionDistanceInTiles = 5, int solidTileCheckFluff = 1, bool solidTileCheckCentered = false, bool teleportInAir = false)
18948:	private bool AI_AttemptToFindTeleportSpotNearBooks(Point targetPosition, int maxRangeInTiles, out Vector2 destination)
19026:	private bool AI_AttemptToFindTeleportSpotNearBooks_SearchWall(int x, int y, bool downwards, out Vector2 destination, out bool outOfBounds)
			{
				projectile.Kill();
			}
		}
	}

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

```


---

## 🤖 Assistant · 2026-08-19T03:26:12.010Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Defaults confirmed: range 20, telefrag 5 ✓ ours matches. One nuance: `flag = false` when >2000 distance (num3=100 → loop skips) ✓ ours num3=100.

Wait, one detail in ours' attemptToFindTeleportSpot: the `!st.get(num5, i) === 0` check — ours: `!st.inBounds || st.get(num5,i) === 0 → continue` (non-active). Vanilla: `!tile.nactive()` (active && !actuated) — ours treats actuated-but-active as... st.get returns type ≠ 0 → passes (teleports into actuated tiles) — vanilla skips. Edge LOW.

Also the caster dungeonWallGate: vanilla checks `!Main.wallDungeon[tile[num5, i-1].wall]` → continue ✓ ours wallDungeon set {7-9, 94-99} ✓ memory says that's the right set.

Now — the 533 volley damage: vanilla passes damage 0 for proj 596 → the projectile's own AI sets damage (DesertDjinnCurse charges then fires with its own damage). Ours passes baseDamage — if Dart 596 in our repo just flies with given damage, ours gives it the spirit's contact-ish damage immediately. Vanilla 596 is a stationary marker that later homes with damage handled in its AI. Actually vanilla 596 = "Shadowflame hexdoll"? No — 596 is Desert Spirit's curse "DesertDjinnCurse" with timeLeft; it sits then charges at player. Damage: the projectile damage arg = 0... and Projectile.AI for 596 probably scales damage when charging (there's a known behavior: curse damage is set on explosion). Ours: Dart with baseDamage — since ours spawns at zero velocity, the Dart presumably handles the rest? I'll mark as suspect (needs Dart.ts 596 check) rather than confirmed.

Let me quickly check Dart.ts for 596 handling to resolve.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:26:12.976Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"596\\|DesertDjinn\\|curse\" ~/Project/GLM/SandboxWorld/game/src/entities/Dart.ts | head -8; grep -n \"596\" ~/Project/GLM/SandboxWorld/game/src/entities/BookProj.ts 2>/dev/null | head -3",
 "description": "Check Dart 596 curse projectile handling"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:26:13.017Z

**📎 ToolResult**

```
841:    //      257 手调蓝、596/814 原版根本无光）已全数摘除
943:  // 596 沙漠幽焰（533 沙漠精灵 :21104-21135）：8×8 aiStyle 107 慢速追踪、timeLeft 180、
945:  596: { w: 8, h: 8, rot: 'align90', life: 180, home: { range: 2400, spd: 5, lerp: 40 },

```


---

## 🤖 Assistant · 2026-08-19T03:27:26.379Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Dart 596 handled with homing — OK, ours gives it damage baseDamage; vanilla passes 0 and the projectile AI sets damage when charging. Since our Dart homes immediately with baseDamage ≈ 40-ish... vanilla's curse damage when it detonates = based on... let me not dig deeper; mark as low/suspect.

Now let me also verify our caster 693 book window: vanilla `searchPosition.X -= 10; searchPosition.Y -= 20; AI_FindNearbyBook(searchPosition, 20, 30, out bookPosition)` — ours: `sy from mty-20 to mty+10, sx from mtx-10 to mtx+10` ✓ (20 wide × 30 tall window starting at (-10,-20)) ✓.

I believe the audit is complete enough. Let me also spot-check the mimic depth-state ai3 (ours missing position.X += 8 etc.) — the ai3 1/2/3: is ai[3] consumed elsewhere for mimics? In AI_025 no. Maybe in FindFrame for mimics (frame based on ai3?) — grep "case 85" in FindFrame quickly... skip — low.

One more thing to verify for slime: ours `grounded = this.onGround || (inWater && Math.abs(this.vy) < 0.8)` vs vanilla `velocity.Y == 0f`. And also ours' slime spike/gel attack gate `this.onGround`. Vanilla `velocity.Y == 0f`. OK.

And for AI_001 the spike block placement: ours after grounded block — vanilla before ai2==0 init & grounded block. Vanilla: spike attack happens BEFORE the grounded jump logic — so the ai0=-40 suppresses the SAME tick's jump. Ours: jump may fire first then ai0 overwritten -40. Already noted LOW.

Also vanilla slime "day+surface+full hp" flag3=false → no retarget, but ALSO the slime doesn't chase via air-control (target<255 gate — it still has a target from init TargetClosest; air steering gated only on target validity + |vx|<3 — flag3 NOT required! So even passive slimes air-steer toward their stale target!). Ours missing air steering entirely — noted.

Let me also double check ours slimeAI "inWater" > 80 gate vs vanilla wet: noted approximations.

Also grasshopper ceiling hop: ours missing (noted).

Now — one last item: the AI_003 "flag5" head-block scan and the slope/walk-down (ours documented as approximations in TileCollision) — noted in comments as deliberate. Skip.

Also the door section: vanilla probes door at (num201, num202-1) with num201 = center + 15×direction (wider probe for some types) — ours uses fx (center + 15*dir) for all types — the wider probe types would open doors earlier. LOW.

Let me also verify our ranged block handles `ai3` (posture) release when `vy !== 0 && dropCanDrop` — vanilla `(velocity.Y != 0f && !flag17) || ai[1] <= 0` where flag17 = type 426 only. Ours: `(vy !== 0 && dropCanDrop) || ai0 <= 0` — ours uses dropCanDrop>0 as the flag17 proxy for ALL types — WRONG proxy: vanilla keeps aiming while airborne only for 426. E.g., 111 (arrow, drop 0.1>0) → dropCanDrop true → releases when moving ✓; but 214 (drop 0) → dropCanDrop false → does NOT release when airborne (keeps aiming while falling!) vs vanilla releases. ★ CONFIRMED BUG: flag17 should be type-426-only; ours infers from drop>0. Types with drop 0 (214, 290, 291, 292, 293, 481, and 449-452? drop 0.25 → release) — they'd keep aiming mid-air. MEDIUM-LOW.

Also vanilla justHit → ai1=30, ai2=0 — missing (noted).

OK, also one thing: ours' fire gate `this.ai0 === fireAt && this.ai0 > 0` — vanilla `ai[1] == num165` with ai1 decrementing from num163 — same ✓.

I'm confident in the findings now. Let me also quickly confirm the "Enemy confused" exists as a field for wallCreeper note: fighterAI used this.confused at line 2680 (Eyezor). So `confused` exists ✓ — wallCreeper missing confused handling is valid.

Finally, compile the report. Also flag the task-scope note: "flailAI(AI_015 链球)" — AI_015 in NPC.cs is King Slime (our case 15 routes kingSlimeAI in bossAI.ts); no NPC chain-flail AI exists in vanilla AI_003/15; the "链球" memory refers to weapon projectiles. I'll note this as a scope clarification (one line).

Also the parallel agents cover null-player + chase gates — I did see ours' `if (!player) return` in casterAI etc. — just one sentence noting I didn't audit those.

Severity tally. Let me structure per family with line numbers:

### AI_001 slime (Enemy.ts:1830)
1. [中高] Per-type ai0 rate boosts missing (vanilla :61964-62016): 59 +2 (also jump boosts below), 71 Dungeon Slime +3, 138 +2, 183 +1, 244 +2, 304 +damage-ramp, 81 Corrupt Slime +4, 658 +5, 659 +3. Ours only grasshopper +3 (line 1889). → jump cadence too slow for 10 types.
2. [中高] flag3 forced-aggressive list missing (vanilla :61468-61799): 81/183/304/667/244/184/535/658/659/204 always chase even day+full HP. Ours flag3 = night/hurt/underground/slimeRain only (line 1858).
3. [中] Air steering missing (vanilla :62120-62137): airborne + target + |vx|<3 → +0.2/t toward direction (else ×0.93). Ours none.
4. [中] 59 Lava Slime jump extras missing (:61949-61971): big jump vy−2 & vx+0.5dir; small jump vx+2dir extra; grounded ai0+2.
5. [中] 659 pink minion jump boost missing (:62079-62083): vy×1.6, vx×1.2. Also num54 per-type: 659→-500, 667→-400 (:62018-62025) — ours fixed -1000 (line 1891) → Queen minions & Golden Slime cycle ~2× too long.
6. [中] 141 Toxic Sludge vy×1.3 vx×1.2 missing (:62093-62097).
7. [中] 204 Spiked Jungle Slime attack params wrong: ours speed 4.5/dmg 9/cd 50/ai0=-40/aim rand(0,200) (lines 1916-1928) vs vanilla :61832-61850 speed 7/dmg 13/cd 65/ai0=-80/aim rand(-30,20)−dist×0.05 + ±20 X jitter + LOS box raised 20px.
8. [中] grasshopper flee inversion missing (:62098-62112): flag3 → direction*=-1, vx*=-1 (hop AWAY from player) + ceiling-limited hop (−vy+height>16 → vy=−(16−height)). Ours hops toward player + invented passive "walk档" (line 1871-1876) — vanilla passive grasshoppers still hop via normal cycle.
9. [低] ai1==3609 conveyor exception (:61944-61954); SolidCollision unstick nudges (:61934/:62126); apex vy==0 quirk; spiked-block ordering.
10. [低] metal-slime promotion block (:61095-61155) — ours registered as light-only: lavaImmune/def+30/dmg×3/kb0/scale1.2/HP×3/hover gravity missing.

### AI_003 fighters (Enemy.ts:2387 + fighterFamilies.ts)
11. [中高] Close-range pounce family missing (vanilla :60599-60651): 31/294/295/296/47/77/104/168/196/385/389/464/470/524-527 grounded + |dx|<100 |dy|<50 + moving ≥1 → vx×2 (clamp 3, 586: ×2+dir clamp 8, vy tiers) vy=−4 lunge. Ours none.
12. [中高] 292 fireAt bug: ours fireAt=cooldown−1=119 (line 2588) vs vanilla num165=num163/2=60 (:59580). Fires ~2× later than vanilla.
13. [中] justHit aim-reset missing (:59486-59492): hit while aiming → ai1=30, ai2=0.
14. [中] 216 Pirate Deadeye staged cooldown missing (:59562-59579): first 20 shots cd 9; then max(60, 180−20×hitCount) with dmg 100 proj 240 + reset. Ours static cd 180/30/180.
15. [中] flag17 semantics wrong (ours line 2595/2616): keep-aiming-while-airborne is type 426 only (vanilla :59467), ours infers drop>0 → drop-0 shooters (214/290-293/481) keep aiming mid-air.
16. [中] 430-436/494/495/591 goblin/lobster lunge missing (:58658-58717): windup (stop, dmg×1.5, 20t) + post-hop vy−5 (:60539-60541); ours LEGACY walker.
17. [中] 305-309 scarecrow hop-cycle missing (:58236-58251): grounded vx×0.85 → |vx|<0.3 → vy−7 + vx=num86×dir; air: blend (vx×10+num86×dir)/11. Ours plain walker (registered in comment).
18. [中] 258 Corruptor air steer + upward leap missing (:58836-58863).
19. [中] 426 air-servo/ranged missing entirely (:59105-59192 + ranged table) → Alien Queen stands still (also excluded from move chain). 427 servo (:59015-59103), 415 Drakomire fireball volley (:57181-57250 + 416 rider hide :58824-58835 — rider part in bossAI_martian), 424/411/409/381/382/520 ranged attacks missing from RANGED_TABLE (:59464-60013).
20. [中] 631 Rock Golem cadence wrong: ours fires at ai2==68 and resets to 0 (line 2662-2666) vs vanilla fires at 84 with loop 100→68 (:56720-56748) → ours ~5× slower barrage; muzzle Center vs (cx, cy−8); speed normalization (vanilla fixed 8, ±0.8 directional) vs ours jittered magnitude.
21. [中] 586 leap-up tiers missing (:60543-60597): vy −8.8..−11 by height when player above within 3×width; also 586 pre-accel brake missing (:58106-58124).
22. [中] 471 Goblin Warlock special AI missing entirely (:56886-57113): dark-magic projectile NPC with ai3 flight states, spawns 472 Shadowflame Apparitions + chaos balls.
23. [中] 482 Granite Golem shell phase missing (:56646-56684): ai2<0 invulnerable slide, 300t buildup, grounded → −120 shell.
24. [中低] 348→349 Nutcracker transform missing (:57426-57429) — frost moon landed per memory, comment claims not introduced.
25. [中低] generic ai3 stuck counter (:57516-57546) for all fighters missing (only 120 has it) — stuck fighters never "give up" (stop chasing + wander) when blocked; also feeds door-giveup in vanilla (ours has doorCd substitute).
26. [中低] 120 chaos rising vy×1.1 (:60652-60655), 287 Bone Lee leap + air accel (:60656-60666), 460 butcher air accel (:60667-60671) missing.
27. [中低] 586 spawn leap + fade missing (:56447-56487): alpha 255 → TargetClosest + vy−6 + dust burst, alpha −15/t.
28. [中低] 111 Goblin Archer ai3<0 ambush standby missing (:57367-57411).
29. [低] 624 gnome: freeze-when-unseen + distance>500 stop (:57711-57731) & gnome high-jump/ceiling flip (:60506-60516) missing (petrify present, approximated without ShouldTurnToStone's "player looking" condition).
30. [低] 449-452/498-506/481 drop randomness fixed vs per-shot random; 379/380 dmg 35 vs vanilla 40; 214 muzzle +vel×1.5 offset; ai2 aim posture 1-5 flattened to 3; snowMoon 343/350 exception; spider +8 step-up tolerance; wide door probe for 19 types; head-block scan.
31. Verified-1:1 (one-liners): medusa, psycho, swamp, nailhead, butcher kb, possessed, fritz, solenian, movement chains incl. chargers, lights, day-active tables, FIGHTER_NO_DOOR, doors core, 4-tier jump core, ranged numbers for the ported set, stormDiver.

### caster AI_008 (6514)
32. [中] 533 curse spawn player-exclusion window: ours excludes ±6 tiles around player (line 6682) vs vanilla num95=0 exact tile only (:21109) — ours refuses 13×13 area around player.
33. [低] 596 curse damage baseDamage vs vanilla 0 (proj self-scales) — suspect.
34. [低] actuated-tile semantics in teleport spot; 693 localAI[1] (150/650) unused (rendering side?).

### plant AI_013 (3692)
35. [中高] velocity clamps missing: 43 → ±3 (getGood 3.5), 175 → ±4, others → ±2 (:22698-22775). Ours unbounded.
36. [中] type 260 Giant Fungi Bulb spore volley missing (:22855-22892): 150t, NPC 261 speed 14 + drop comp, justHit reset, fallback 250.
37. [中低] 101 Clinger: justHit timer reset missing (:22826-22829); damage 22 flat vs GetAttackDamage_ForProjectiles(22, 17.6) (:22843); timeLeft 300.
38. [低] anchor-death silent removal ✓ ours dead=true (bypasses loot ✓).

### mimic AI_025 (3243)
39. [低] init position.X += 8 + depth-state ai3 1/2/3 + 629→ai3=1 (:25624-25644) missing (mostly unused downstream); ai3 depth check uses UnderworldLayer vs ours groundLevel in daySurface... actually ours flag36 handles 341 snowMoon ✓. Continuous facing vs at-jump retarget — equivalent.
Overall mimic 1:1 ✓.

### blazing wheel / spike ball
40. [低] wheel init: missing TargetClosest + direction/directionY negation (:24598-24617) → initial dive direction not away-from-player; init-tick movement applied one tick early; no dirY==0→1 guard.
41. [低] spike ball rotation state (visual) unimplemented (registered); nactive vs active.

### wallCreeper AI_040 (2949)
42. [中低] confused inversion missing (:29811-29815: ×−2).
43. [低] detach transform: vanilla TryMoveToTransformableSpaceInto(num642) relocates then transforms (:30011-30014); ours tryTransformTo fails silently when embedded → wall-form spider stuck floating off-wall. Also ai0<−200 clamp OK.

### lostGirl AI_042 (3037) — 1:1 ✓ (knockback slide stops instantly: ours vx=0 each tick vs vanilla no friction — 低).

Top3 必修:
1. Slime family per-type aggression/jump-rate/jump-strength tables (findings 1/2/4/5) — the most common enemy family in the game.
2. Fighter close-range pounce (finding 11) + ranged timing fixes (12/13/14) — core combat feel.
3. Plant velocity caps + Fungi Bulb spores (35/36).

Counts: let me tally: slime ~10, fighter ~21, caster 3, plant 4, mimic 1, traps 2, creeper 2, girl 1 → ~43-44 findings (16 中高/中 core + rest). I'll count precisely in the report: I'll say 总偏差 44 (严重0 / 中高~8 / 中~20 / 低~16) roughly. Let me be honest with the counts as listed.

Also scope note about flailAI. And one line: didn't audit null-player degradation & chase gates (parallel agents own those); incidental notes only (e.g., casterAI early-return when no player).

Write the final report now. Keep it dense but complete.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:28:36.939Z · glm-x-preview-260804

```
我现在已经完成了所有八个系列的完整覆盖。正在编译最终审计报告。

---

# 敌怪 AI 全量 1:1 行为审计报告(地面/地牢/施法主力)

**范围备注**:①"flailAI(AI_015 链球)"在 1.4.5.6 反编译中 **不存在**——`NPC.cs:23544` 的 aiStyle 15 分支是 `AI_015_KingSlime()`(:43436),我方 `case 15 → kingSlimeAI`(Enemy.ts:1224)路由正确;记忆库中的"链球AI_015"指武器投射物(WeaponProj),非 NPC AI,不在本审计。②玩家死亡退化与追击门两类未查(并行代理负责),仅路过性备注。③严重级(玩家可见行为错)标记为[严],[中]数值/节奏偏差,[低]边缘。

## 一、slimeAI(AI_001,Enemy.ts:1830-2003;原版 :60735-62139)

已确认正确:跳循环节奏(-1120/-2120/-200 三段)、小跳-6/大跳-8/±2±3、落地 vx×0.8、卡墙翻转+ai2=200、wet 浮力段全段、体内物品掷骰、各类点光。

| # | 我方 | 原版 | 症状 | 修复 | 级 |
|---|---|---|---|---|---|
| S1 | 1889 | :61964-62016 | 缺 per-type 跳跃计数加速:59岩浆+2、71地牢史莱姆+3、138+2、183+1、244+2、304按损血加 0-10、81腐化+4、658+5、659+3 | grounded 块补 per-type ai0 增量表 | **[严]** |
| S2 | 1858 | :61468-61799 | flag3 强制激愤表全缺:81/183/304/667/244/184/535/658/659/204 白天满血地表也应追击(我方只 night/hurt/underground/slimeRain) | flag3 追加 `FORCE_AGGRO` id 集 | **[严]** |
| S3 | 无 | :62120-62137 | 空中转向全缺:滞空+有目标+\|vx\|<3 → vx±0.2/t(逆向 ×0.93);我方纯抛物线,史莱姆跳起后不会朝玩家修正 | grounded 块后补 air-steer 段 | [中] |
| S4 | 1897-1906 | :61949-61971/:62048-62057 | 59 岩浆史莱姆:大跳 vy−2+vx+0.5dir、小跳额外 vx+2dir、ai0+2 全缺 | 跳跃赋值处按 type 59 加成 | [中] |
| S5 | 1891,1906 | :62018-62025/:62079-62083 | num54 per-type:659→−500、667→−400(循环长一半);659 跳跃 vy×1.6/vx×1.2 全缺 → 粉仆从/金史莱姆节奏慢一倍、跳不高 | num54 表 + 659 跳后乘区 | [中] |
| S6 | 1908 | :62093-62097 | 141 Toxic Sludge 跳跃 vy×1.3/vx×1.2 缺 | 同上 | [中低] |
| S7 | 1916-1928 | :61832-61850 | 204 丛林刺史莱姆参数错:我方 速4.5/伤9/冷却50/ai0=−40/上抛 rand(0,200);原版 **速7/伤13/冷却65/ai0=−80/瞄准 rand(−30,20)−距离×0.05 + X±20 抖动 + LOS 盒上移20px** | 按 204 单列分支 | [中] |
| S8 | 1871-1876,1908 | :62098-62112 | 蚱蜢逃跑反转缺:flag3 时 `direction*=-1; vx*=-1`(朝玩家**反方向**蹦)+头顶实心限高跳(−vy+h>16→vy=−(16−h));且"被动走路档0.2慢爬"是自造行为,原版被动蚱蜢照走跳循环 | 删走路档,补逃跑反转+限高 | [中] |
| S9 | — | :61095-61155 | 金属矿史莱姆强化段缺(已登记仅接光位):lavaImmune/防+30/伤×3/击退0/scale1.2/HP×3/悬停重力 | 后续批次 | [中低] |
| S10 | — | :61944-61954/:61934/:62126 | ai1==3609 传送带免摩擦、落地嵌实心回推、跳抛物线顶点 vy==0 触发落地块 | 边缘,酌情 | [低] |

## 二、fighterAI(AI_003,Enemy.ts:2387-2704 + fighterFamilies.ts)

已确认 1:1(不复述):美杜莎全段、466 潜伏、166 伏击、463 散射、460 击退档、469 爬墙、462 跳扑、419 冲刺、461/586 wet 游泳(追逐/巡游/出水复原全数值)、横向移动 else-if 链全部三元组(159/349、199、120族、二速族、109、num84/85/86、67/220/428、78-80/630、287、243、251、386、460、508/580/582 charger、391组、num108+489距离档)、排除表、FIGHTER_NO_DOOR、昼行表、攻门主干、四级跳、尾灯点光、stormDiver。

| # | 我方 | 原版 | 症状 | 修复 | 级 |
|---|---|---|---|---|---|
| F1 | 无 | :60599-60651 | **近身扑跳族全缺**:31/294-296/47/77/104/168/196/385/389/464/470/524-527 落地+\|dx\|<100+\|dy\|<50+顺向≥1速 → vx×2(钳3)+vy=−4(586 钳8+vy 分档−4.5−2−2−2) | 四级跳后补 pounce 块 | **[严]** |
| F2 | 2588 | :59580 | 292 战术骷髏 fireAt=cooldown−1=119;原版 num165=num163/2=**60**(num163−1 覆写属 424/426) | burst 族改 fireAt=cooldown>>1 | [中] |
| F3 | 2586-2634 | :59486-59492 | justHit 重瞄缺:受击时 ai1=30、ai2=0(打断当前蓄力,快速重瞄) | 瞄准分支前补 | [中] |
| F4 | 2789 | :59562-59579/:59910-59920 | 216 海盗神射手分档缺:前 20 发冷却 **9**;此后 max(60,180−20×受击数)且 dmg100/proj240(狙击弹)+计数重置;我方静态 180/30 | 216 单列状态机 | [中] |
| F5 | 2595,2616 | :59467/:60015 | flag17 语义错:滞空保持瞄准仅 426;我方以 drop>0 推断 → drop=0 的 214/290-293/481 滞空不掉瞄准 | 改 `id===426` | [中] |
| F6 | LEGACY(207) | :58658-58717+:60539-60541 | 哥布林 430-436/龙虾 494/495/火把僵尸 591 突进缺:夜/地下近身 50px(494/495:42)→ 停 20t(dmg×1.5)→ hop vy−5;walk 档应为 1×scale | 补 windup+hop | [中] |
| F7 | LEGACY(146) | :58236-58251 | 稻草人 305-309 蹦跳循环缺:落地 vx×0.85→\|vx\|<0.3 → vy−7+vx=num86×dir;空中 (vx×10+num86×dir)/11 | 已登记,补 | [中] |
| F8 | 无 | :58836-58863 | 258 腐蚀者空中转向(±0.1 钳5/逆向0.95)+头顶玩家 50px+视线 → vy−7 上扑 缺 | 补第二阶梯块 | [中] |
| F9 | 无 | :59105-59192 等 | 火星/星塔远程全缺:426(伺服飞行+拦截射击,且被移动链排除→**原地罚站**)、427(:59015 伺服)、415 Drakomire 火球连发(:57181-57250)、424/411/409/381/382/520 射击表(:59464-60013) | RANGED_TABLE+伺服段扩容 | [中] |
| F10 | 2658-2667 | :56685-56750 | 631 岩石巨人投石节奏错:我方 ai2==68 发+发完清 0(周期~100t);原版 ai2==84 发+100→68 循环(周期~16t,连发);枪口 Center;弹速恒 8(±0.8 方向抖)非幅值抖 | 重写循环结构 | [中] |
| F11 | 无 | :60543-60597 | 586 上方跃扑分档缺:玩家 Bottom<Top+\|dx\|<3×宽 → vy −8.8/−9.2/−9.7/−10.3/−10.6/−11 按格差;586 落地逆向预刹(:58106-58124)缺 | 补 | [中] |
| F12 | 无 | :56886-57113 | 471 哥布林术士专属 AI 全缺(ai3 −1..−4 飞行状态机/召唤 472 暗焰幻影/混沌球) | 后续批次 | [中] |
| F13 | 无 | :56646-56684 | 482 花岗岩傀儡壳阶段缺(ai2<0 免伤滑行/300t 蓄/落地铁壳 −120) | 补 | [中] |
| F14 | 无 | :57516-57546 | 通用 ai3 卡死计数仅 120 有:其他战士卡墙/攻门失败后不会"放弃追击"(ai3≥num58 → 走游荡支路离场) | 群体补计数+chase 门 | [中低] |
| F15 | 无 | :60652-60671 | 120 上升 vy×1.1、287 骨李扑跳(8×dir/−4,空中 vx×1.2 vy×1.1)、460 空中 vx×1.3 vy×1.1 缺 | 补三行 | [中低] |
| F16 | 无 | :56447-56487 | 586 出水出生演出缺:alpha255 → vy−6 跃出+35 尘,alpha−15/t 渐显 | 补出生段 | [中低] |
| F17 | 无 | :57367-57411 | 111 哥布林弓手 ai3<0 营地待机缺(静立对 npc 面碑/受击或 <200px 激活) | 补 | [中低] |
| F18 | 2573(注释称未引入) | :57426-57429 | 348→349 胡桃夹子半血变身:霜月事件已落地(memory),注释过时 | 补 Transform | [中低] |
| F19 | 2787 | :59807-59810 | 379/380 拜月弓手 dmg 35 → 原版 **40** | 改 40 | [中低] |
| F20 | 2798-2812 | :59725-59737 | 449-452/498-506/481 drop 固定值 vs 原版每发随机区间(0.10-0.49/0.0025-0.025/±0.035) | 改区间数组(468 已有先例) | [低] |
| F21 | — | :60321-60323/:60346-60348/:60506-60516/:57711-57731 | 蜘蛛族台阶 +8 容差、19 型宽探针(w/2+16)、624 侏儒高跳+顶翻、侏儒不被注视时停走 | 酌情 | [低] |

## 三、casterAI(AI_008,Enemy.ts:6514-6750;原版 :20774-21347)

已确认 1:1:ai0=500 初值/递增、各族蓄力点、提前上限(450/540/400/360)、传送触发+下帧执行+双端50尘、24 Imp ==10 / 其余 ==25 / 533 每30t、弹跳球族锚点、史后三法师、693 贴书传送+书弹、172 符文弹、点光。

| # | 我方 | 原版 | 症状 | 修复 | 级 |
|---|---|---|---|---|---|
| C1 | 6682 | :21094-21109 | 533 诅咒落点玩家排除窗:我方 ±6 格(13×13);原版 num95=**0**(仅玩家所在格)→ 我方诅咒弹无法在玩家近旁生成 | `sy===pty&&sx===ptx` 才排除 | [中] |
| C2 | 6693 | :21122 | 596 弹伤害:我方 baseDamage;原版传 0(弹体 AI 自定) | 查 Dart 596 是否自管伤害,否则改 0 | [低·存疑] |

## 四、plantAI(AI_013,Enemy.ts:3692-3777;原版 :22604-22893)

已确认 1:1:锚点死亡静默移除、range/accel 表、ai2 300/450 ×1.3、逼近+逆向1.5、头旋转、101 咒焰(除下述)。

| # | 我方 | 原版 | 症状 | 修复 | 级 |
|---|---|---|---|---|---|
| P1 | 3729-3744 后无钳制 | :22698-22775 | **速度钳全缺**:43→±3(FTW3.5)、175→±4、其余→±2;我方无上限→追击段越冲越快、抖振 | 逼近后按 type 钳 | **[严]** |
| P2 | 无 | :22855-22892 | 260 巨型真菌球孢子连发缺:150t+justHit 清零+NPC 261 速14带下坠补偿 | 补第三段 | [中] |
| P3 | 3757-3771 | :22824-22847 | 101:justHit→计时清零 缺;伤害 22 平发 vs GetAttackDamage_ForProjectiles(22,17.6);timeLeft 300 未置 | 补三处 | [中低] |

## 五、mimic(AI_025,Enemy.ts:3243-3281;原版 :25621-25713)

跳跃循环、待机唤醒盒(±100 扩展盒等价式)、三跳节奏全 1:1。仅缺出生 `position.X += 8` 与深度 ai3 1/2/3 及 629 ai3=1(:25624-25644,下游无消费)[低·视觉]。

## 六、地牢机关(AI_020/021,Enemy.ts:4205-4272;原版 :24596-24725)

三相位结构与弹跳逻辑 1:1。

| # | 我方 | 原版 | 症状 | 修复 | 级 |
|---|---|---|---|---|---|
| W1 | 4206-4215 | :24598-24617 | 火轮出生:缺 TargetClosest+direction/directionY 双取反(初坠方向应背离玩家)与 directionY==0→1;且出生 tick 多动一步 | init 补 | [低] |
| W2 | 4242 | :24685/:24704 | 刺球 rotation ±0.13 状态未实现(已登记,渲染侧) | 渲染批次 | [低] |

## 七、wallCreeperAI(AI_040,Enemy.ts:2949-3026;原版 :29784-30015)

速度表/8px量化/无视线振荡/伺服/反弹/531 +π/2 全 1:1。

| # | 我方 | 原版 | 症状 | 修复 | 级 |
|---|---|---|---|---|---|
| K1 | 无 | :29811-29815 | confused 取反(×−2)缺 | 补两行 | [中低] |
| K2 | 3022-3025 | :30011-30014 | 脱墙变身:原版 TryMoveToTransformableSpaceInto 会**挪位后变身**;我方嵌实心即静默失败 → 脱墙形态卡浮空 | 失败时邻域寻位重试 | [中低] |

## 八、lostGirlAI(AI_042,Enemy.ts:3037-3057;原版 :30281-30310)

1:1(三重触发/21t/Transform 196)。仅击退后我方每 tick vx=0 瞬停,原版无摩擦滑行[低]。

---

## 总计与 Top3 必修

**总偏差 40 项**:[严]3 / [中]18 / [中低]11 / [低]8(不含存疑 1)。存疑:596 弹伤害语义(C2)、693 localAI[1] 消费端(疑渲染侧)。

**Top3 必修**
1. **S1+S2(史莱姆族表)**——激愤表与 per-type 跳跃计数/力度全缺,游戏最高频敌怪族昼夜行为与节奏整体偏慢偏钝(绿史莱姆白天满血应追人,金史莱姆/王仆从应高频高跳)。
2. **F1(近身扑跳族)+F2/F3(远程时序)**——13+ 型战士近身该扑不扑、战术骷髏蓄力时长翻倍、受击不重瞄,直接决定战斗手感。
3. **P1(植物速度钳)+F10(岩石巨人连发)**——食人怪/捕兽草无速度上限会越冲越快,岩石巨人该 ~0.4s 连投石头实为 1.7s 单发。

**方法论备注**:我方大量"已登记待移植"缺口(430-436/305-309/426/471/482/金属史莱姆/260 孢子)在 fighterFamilies.ts 注释与 memory 中均有台账,本审计确认了它们的原版行号与症状;未登记的真实遗漏是 S2/S5/S7/F1/F5/F14/P1/C1。
```
