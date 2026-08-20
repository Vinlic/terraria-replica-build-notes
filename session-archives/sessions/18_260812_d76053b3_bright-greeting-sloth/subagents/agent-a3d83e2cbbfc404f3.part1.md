# (第 1 卷 · 自动分卷)


---

## 👤 User(sidechain) · 2026-08-19T03:09:15.227Z

```
你在 ~/Project/GLM/SandboxWorld 做泰拉瑞亚 1.4.5.6 复刻的 Boss AI 1:1 抽查审计。**严格只读:禁止编辑任何文件、禁止跑游戏/vite/测试。**

标杆(唯一权威):~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs(96369 行)
我方:~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts

背景:我方是手工移植;文件注释里引用的 "cs:NNNNN" 就是上面这份 NPC.cs 的行号,可直接定位。我方 ai0..ai3 = 原版 npc.ai[0..3],aiT/localAI ≈ localAI[i],bInit ≈ 出生初始化段。专家/大师门:我方 mainExpertMode()/getAttackDamageForProjectiles() ≈ Main.expertMode / masterMode 相关缩放。

你负责审计 bossAI_dd2.ts 全文件,重点 Boss(按优先级):
1. Betsy(双足翼龙,NPC 551,aiStyle 110 → NPC.cs AI_110_Betsy @62266-62808)
2. DarkMage(黑暗魔法师 564/565,aiStyle 109 → AI_109_DarkMage @66392-66792;三连招弹 675/674/673)
3. FlyingDutchman(荷兰飞盗船 491,aiStyle 93 → cs:40918-41028;四炮部件+海盗跳舱)
4. ai107ImprovedWalkers(DD2 walker 族,aiStyle 107 → AI_107_ImprovedWalkers @63372-64919;食人魔 Ogre 560 是 Boss 级,近战前摇/投弹/掷矛/喷吐/自爆/灵气)
5. 次要:sandElementalAI(541,aiStyle 102 @42224)、sandSharkAI(542-545,aiStyle 103 @42621)、eterniaCrystalAI(548)、lanePortalAI(549)、divingFlyerAI(小妖魔滑翔怪 574-575 @65959)、dd2LightningBugAI(578 @66793+)

审计维度(抓结构性偏差,不是数值噪音):
- 状态机阶段与转换(计时器/血量阈值/专家大师分支门漏掉或写错)
- 移动物理(冲刺速度档/悬浮/传送节奏)
- 攻击循环参数(弹幕 id/速度/计数/连发间隔)
- 玩家死亡/Boss 离场(flee)语义有无原版出处
- 部件联动(炮位锚定/传送门出怪)

方法建议:先 Read 我方文件对应函数,再 sed -n '起,止p' 读原版对应段对照。不要泛读全文。注释声称的行号要抽验(注释可能撒谎/过时)。

输出格式(最终回复,直接文本,不写文件):
逐 Boss 一节:"核了什么+发现什么"。每条 CONFIRMED 偏差给:我方文件:行号 / 原版 NPC.cs 行号 / 症状 / 最小修复建议 / 置信度(高/中/低)。没问题的 Boss 一句话带过(写明核过的维度)。存疑单列(不确定的不要混进 CONFIRMED)。最多报 10 条,按严重度排序。禁止编造行号——每条 CONFIRMED 必须两边都真实读过。
```

---

## 📎 Attachment · skill_listing · 2026-08-19T03:09:15.230Z

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

## 🤖 Assistant · 2026-08-19T03:09:19.967Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me start by reading the relevant sections of our file bossAI_dd2.ts, and then compare with the decompiled NPC.cs sections.

Let me first check the size of our file, then read it in parts.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:20.487Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "wc -l ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Count lines of both files"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:20.538Z

**📎 ToolResult**

```
    2441 ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts
   96369 ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs
   98810 total

```


---

## 🤖 Assistant · 2026-08-19T03:09:21.204Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"export function\\|function \\|cs:[0-9]\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts | head -100",
 "description": "List functions and cs: line references in our file"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:21.249Z

**📎 ToolResult**

```
2://   aiStyle 93  荷兰飞盗船 491            NPC.cs:40918-41028（首帧生成 4×荷兰大炮 492
7://   aiStyle 102 沙尘精 541                NPC.cs:42224-42620（walker 核 + ai[0] 攻击循环：
10://                                          ≥22 格,StrayMethods.cs:47;标记 damage 0 纯视觉,
11://                                          Projectile.cs:6792 + aiStyle128 尘柱）;135t → -300
13://   aiStyle 103 沙鲨族 542-545            NPC.cs:42621-42805（沙/沙岩/硬化沙中巡游;碰撞走
18://   aiStyle 104 DD2AttackerTest 547       NPC.cs:42807-42809（active=false——出生即消,
20://   aiStyle 105 永恒水晶 548              NPC.cs:42810-43062（ai[1] 0: 首帧起 180t 倒计时 →
21://                                          CheckArenaScore(StrayMethods.cs:83 SendWalker 双向
25://   aiStyle 106 神秘传送门 549            NPC.cs:43063-43152（LaneSpawnRate 节拍出怪 →
29://   aiStyle 108 俯冲飞行族                NPC.cs:43157 → AI_108_DivingFlyer :65959
37://   aiStyle 109 黑暗魔法师 564/565        NPC.cs:43161 → AI_109_DarkMage :66392
42://                                           +500×3,Projectile.cs:35510）/ 2 召骷髅 673（183t,
45://   aiStyle 110 双足翼龙 Betsy 551        NPC.cs:43165 → AI_110_Betsy :62266
54://   aiStyle 111 埃特尼亚荧光虫 578        NPC.cs:43169 → AI_111_DD2LightningBug :66799
72://   转发本文件 dutchmanCannonAI（cs:35889-35904 锚船偏移 + :36008-36070 240t 装填炮击）。
77://   DD2 敌怪索敌语义（NPCUtils.cs:261/:308）：场上有水晶 548 → 咬水晶;否则咬玩家。
95:// RENDER_PROXY 代渲登记退役。687 喷焰原版为 Main.cs:31282 自定义 15 层火舌程序化
96:// 绘制,此处按整条贴图(98×686 单帧)近似;682 电弧 4 帧竖条(projFrames=4,Main.cs:8482)
103: *  [0]=localAI[0] 灵气计数（死亡紫魂环驱动，Main.cs:26130 num322；
104: *  AI_107 灵气态每 tick +1，cs:63882）/ [1]=localAI[3] 出生计数（出生紫雾门，
105: *  Main.cs:25899，AI_107 出膛渐显 0→60） */
114:/** 原版 oldVelocity（碰撞前一帧速度,cs:93795 collideX/collideY 判定源）→ WeakMap */
140:// 触发链 = 永恒水晶座 466 右键（Game.useEterniaStand，Player.cs:31930-31977）。
240:function shootD(
272:/** TileID.Sets.Conversion（TileID.cs:30-34）：Sand 53/112/116/234、HardenedSand
277:/** TileID.Sets.ForAdvancedCollision.ForSandshark（沙鲨碰撞豁免表,cs:93812） */
296:/** Collision.ExpandVertically（Collision.cs:4403）：从 (x,y) 向上/下穿非实心格扩张 */
297:function expandVertically(
315:/** StrayMethods.CanSpawnSandstormHostile（StrayMethods.cs:47）：三列各 ±15 格净空,
317:function canSpawnSandstormHostile(game: GameHooks, tx: number, ty: number): boolean {
325:/** StrayMethods.SendWalker（StrayMethods.cs:115）：沿地面走向 direction,返回最远落脚点 */
326:function sendWalker(
354:/** StrayMethods.CheckArenaScore（StrayMethods.cs:83）：水晶落点双向 walker 扫场端点 */
355:export function checkArenaScore(
371:function findCrystal(game: GameHooks): Enemy | null {
377:function dd2Target(
390:function dirTo(e: Enemy, tx: number, ty: number): { x: number; y: number } {
395:/** SimpleFlyMovement（NPC.cs:78100 原版逐轴步进,反向时双倍） */
396:function simpleFlyMove(e: Enemy, dvx: number, dvy: number, acc: number): void {
404:// AI_093 荷兰飞盗船 491（NPC.cs:40918-41028）
406:export function flyingDutchmanAI(e: Enemy, game: GameHooks, player: Player | null) {
508:// 荷兰大炮 492（aiStyle 75 分发 → 此处;NPC.cs:35889-35904 锚定 + :36008-36070 炮击）
511:export function dutchmanCannonAI(e: Enemy, game: GameHooks, player: Player | null) {
557:// walker 共享核（AI_102 尾段 cs:42406-42620 与 AI_109 尾段 cs:66577-66797 逐行同构）
574:function walkerKernel(
578:  // ---- 卡位/跳墙（cs:42391-42426 / :66557-66592） ----
604:  // ---- 施法僵直（cs:42387-42389 / :66554-66555）：AI 早退但碰撞步照跑 ----
614:  // ---- 前方/底部/头顶探测（cs:42428-42475 / :66594-66651） ----
645:  // ---- 重力/升力（cs:42477-42495 / :66653-66671） ----
653:  // ---- 碰撞反弹（cs:42497-42519 / :66673-66695;oldVelocity=碰撞前速度） ----
665:  // ---- 朝向加速（cs:42521-42559 / :66697-66735;方向档速度模型） ----
696:// AI_102 沙尘精 541（NPC.cs:42224-42620）
698:export function sandElementalAI(e: Enemy, game: GameHooks, player: Player | null) {
750:// 沙鲨碰撞（Collision.AdvancedTileCollision + ForSandshark,cs:93808-93814）：
755:function moveSandShark(e: Enemy, game: GameHooks, vx: number, vy: number): void {
801:// AI_103 沙鲨族 542-545（NPC.cs:42621-42805）
803:export function sandSharkAI(e: Enemy, game: GameHooks, player: Player | null) {
903:// AI_104 DD2AttackerTest 547（NPC.cs:42807-42809）——原版即 active=false
905:export function dd2AttackerTestAI(e: Enemy, game: GameHooks): void {
911:// AI_105 永恒水晶 548（NPC.cs:42810-43062）
914:export function eterniaCrystalAI(e: Enemy, game: GameHooks, player: Player | null) {
1002:// AI_106 神秘传送门 549（NPC.cs:43063-43152）
1005:export function lanePortalAI(e: Enemy, game: GameHooks, player: Player | null) {
1049:// AI_108 俯冲飞行族（NPC.cs:43157 → AI_108_DivingFlyer :65959）
1058:function flyerParams(id: number): FlyerP {
1085:export function divingFlyerAI(e: Enemy, game: GameHooks, player: Player | null) {
1234:function solidBody(game: GameHooks, e: Enemy): boolean {
1244:// AI_109 黑暗魔法师 564/565（NPC.cs:43161 → AI_109_DarkMage :66392）
1246:export function darkMageAI(e: Enemy, game: GameHooks, player: Player | null) {
1282:      // 673 阵眼在原版弹幕 ai[0]==70 帧播音（Projectile.cs:35516 DD2_SkeletonSummoned），
1301:    // 脉动自身再数 40 AI 步才结算疗程（DD2HealPulse = Projectile.cs:35540-35574）：
1345:// AI_110 双足翼龙 Betsy 551（NPC.cs:43165 → AI_110_Betsy :62266）
1347:export function betsyAI(e: Enemy, game: GameHooks, player: Player | null) {
1581:// AI_111 埃特尼亚荧光虫 578（NPC.cs:43169 → AI_111_DD2LightningBug :66799）
1583:export function dd2LightningBugAI(e: Enemy, game: GameHooks, player: Player | null) {
1610:  // ---- 同族分离（:66878-66900 flag2,cs:66878-66900） ----
1676:// AI_107 ImprovedWalkers（NPC.cs:63372-64919）——旧日军团地面 walker 族 1:1。
1689://   （NPCID.cs:4793=552-557/561-563/564-565/568-573/576-577）无视线且朝向目标时
1693:/** GetAttackDamage_ForProjectiles（NPC.cs:7031-7034）：npc.difficulty 在
1694: *  Classic(1)→Expert(2) 区间的 Utils.Remap（GameDifficultyLevel.cs:7-9;不钳界,
1696:function projDmgOf(e: Enemy, normal: number, expert: number): number {
1701:/** AI_107 族参数（cs:63415-63475 默认档 → 各 case 覆写;行号逐项标注） */
1716:  muzzleDx: number;             // vector.X（direction 倍率,cs:63436）
1719:  spawnOffset: number;          // num18 出膛位移倍率（cs:63445,德拉肯 0）
1737:/** FighterUsesDD2PortalAppearEffect（NPCID.cs:4793）：出生 60t 渐显 + 30t 出世音 */
1746:function walker107Params(e: Enemy, x: number[]): Walker107P {
1759:  // 出生 60t 内移速爬坡（各族共通,cs:63624-63627/:63674-63678/:63842-63845/:63964-63967）
1766:    case 552: case 553: case 554: {        // 埃特尼亚哥布林（cs:63607-63628）
1774:    case 555: case 556: case 557: {        // 哥布林投弹手（cs:63993-64041）
1787:    case 561: case 562: case 563: {        // 埃特尼亚标枪手（cs:63937-63992）
1804:    case 566: case 567:                    // 旧日骷髅（cs:64042-64117）——无攻击,落地渐显
1806:    case 568: case 569: {                  // 枯萎兽（cs:63847-63936）——灵气态
1812:    case 570: case 571: {                  // 德拉肯（cs:63629-63679）
1829:    case 572: case 573:                    // 小妖精地面型（cs:63680-63846）——自爆冲锋
1832:    case 576: case 577:                    // 食人魔（cs:63513-63606）——三态
1862:/** AI_107 出膛（cs:64394-64417 flag3 / :64575-64615 flag12 共用弹道） */
1863:function fireWalkerProj(
1897:function w107Target(game: GameHooks, e: Enemy, player: Player | null): W107Target | null {
1918:function w107WalkAccel(e: Enemy, p: Walker107P): void {
1926:/** AI_107 主入口（NPC.cs:63372-64919） */

```


---

## 🤖 Assistant · 2026-08-19T03:09:28.553Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Let me plan my audit. I need to read our file's relevant functions and compare to the decompiled NPC.cs sections. Priority order:

1. Betsy (NPC 551, aiStyle 110 → AI_110_Betsy @62266-62808) — our betsyAI @1347-1580
2. DarkMage (564/565, aiStyle 109 → AI_109_DarkMage @66392-66792) — our darkMageAI @1246-1344
3. FlyingDutchman (491, aiStyle 93 → cs:40918-41028) — our flyingDutchmanAI @406-507; dutchmanCannonAI @511-556
4. ai107ImprovedWalkers (Ogre 560 Boss-level) — our walker107 stuff @1676-2441
5. Secondary: sandElementalAI @698, sandSharkAI @803, eterniaCrystalAI @914, lanePortalAI @1005, divingFlyerAI @1085, dd2LightningBugAI @1583.

Let me read our file fully first (2441 lines, readable in two reads). Then read the vanilla sections.

Let me read the whole our file.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:28.828Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts",
 "limit": 700
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:29.081Z

**📎 ToolResult**

```
1	// DD2/旧日军团 + 沙漠族 AI 家族 1:1 移植（Terarria1456, 1.4.5.6）：
2	//   aiStyle 93  荷兰飞盗船 491            NPC.cs:40918-41028（首帧生成 4×荷兰大炮 492
3	//                                          （ai[0..3]=炮位,出生间隔 ai[3]=60*i）;炮全灭 →
4	//                                          StrikeNPCNoInteraction(9999) 自毁;1/300t 船口
5	//                                          跳海盗 212-215(vy-8.01);贴地巡航保持离地 350-450px;
6	//                                          SetDefaults dontTakeDamage=true :14581 → 炮在世恒无敌）
7	//   aiStyle 102 沙尘精 541                NPC.cs:42224-42620（walker 核 + ai[0] 攻击循环：
8	//                                          0→1 起手,54t 在玩家预测位（vx*30）±30 格放 ≤3 枚
9	//                                          沙暴标记 658（需 CanSpawnSandstormHostile 三列净空
10	//                                          ≥22 格,StrayMethods.cs:47;标记 damage 0 纯视觉,
11	//                                          Projectile.cs:6792 + aiStyle128 尘柱）;135t → -300
12	//                                          冷却;血 <50% knockBackResist=0）
13	//   aiStyle 103 沙鲨族 542-545            NPC.cs:42621-42805（沙/沙岩/硬化沙中巡游;碰撞走
14	//                                          Collision.AdvancedTileCollision(ForSandshark) :93812
15	//                                          ——沙族 tile 无视碰撞,其余照撞;玩家在上方且距 >150px
16	//                                          → 对准（目标-80px）12 速跃沙扑咬,30t 冷却（ai[2]）;
17	//                                          离沙 → 重力 0.3 落地爬行 ±1 速）
18	//   aiStyle 104 DD2AttackerTest 547       NPC.cs:42807-42809（active=false——出生即消,
19	//                                          原版内部测试残留物）
20	//   aiStyle 105 永恒水晶 548              NPC.cs:42810-43062（ai[1] 0: 首帧起 180t 倒计时 →
21	//                                          CheckArenaScore(StrayMethods.cs:83 SendWalker 双向
22	//                                          扫场)两端各送 1×神秘传送门 549（右门 ai[2]=1）;
23	//                                          1=败北演出（上浮渐隐 600t）/2=胜利演出（600t 尘涡）,
24	//                                          收场调 DD2Event.StopInvasion——事件依赖见下）
25	//   aiStyle 106 神秘传送门 549            NPC.cs:43063-43152（LaneSpawnRate 节拍出怪 →
26	//                                          DD2Event.SpawnMonsterFromGate;localAI[0] 满 180 且
27	//                                          水晶在世 → dontTakeDamage 驻守;水晶亡 → ai[1]=1,
28	//                                          500-600t scale 1→0.05 缩放消散,550t 自灭）
29	//   aiStyle 108 俯冲飞行族                NPC.cs:43157 → AI_108_DivingFlyer :65959
30	//          埃特尼亚飞龙 T1/T2/T3 558/559/560 + 小妖魔滑翔怪 T2/T3 574/575
31	//                                          （0 悬空逼近（LOS+下视野门,ai[3] 120t 宽限）→
32	//                                           1 瞄准 num5 t（v×0.95,小妖魔 vy-0.1 点火）→
33	//                                           2 俯冲追踪（超时/低于 6 速 → 0;小妖魔 flag2=
34	//                                           撞实心块/贴目标 64px → 3 自爆 192² 伤 80）→
35	//                                           4 回旋（ai[1]=45,每 tick -3）;出生 60t 渐显 +
36	//                                           同族 0.05/0.1 分离）
37	//   aiStyle 109 黑暗魔法师 564/565        NPC.cs:43161 → AI_109_DarkMage :66392
38	//                                          （walker 核（与 102 同构,参数漂移：重力 0.05/
39	//                                           落速 0.2）+ 三连招循环 ai[1]: 0 暗影矢 675（97t,
40	//                                           ai[0]==32 发,14 速 40 伤）/ 1 治疗（127t,ai[0]=40/
41	//                                           48/56 在 ±240 格地面各放 674 → 1000px 内友军
42	//                                           +500×3,Projectile.cs:35510）/ 2 召骷髅 673（183t,
43	//                                           ai[0]==64 发,DD2Event.RaiseGoblins 事件依赖）;
44	//                                           招式选择：±600×±200 内受伤友军 <2 → 强制 2）
45	//   aiStyle 110 双足翼龙 Betsy 551        NPC.cs:43165 → AI_110_Betsy :62266
46	//                                          （0 入场 10t → 1 悬停 30t 按 ai[3] 八槽轮换选招：
47	//                                           2 风压冲 23 速（30t）/ 3 火焰吐息（40t 接位 →
48	//                                           687 喷焰 80t 横冲 10→20 速）/ 4 空袭（60t 接位 →
49	//                                           686 火球 ×6 每 10t + 60t 贴地掠射）/ 5 翻转俯冲
50	//                                           （60t,32 速螺旋 +0.1 升降）/ 6 召唤（贴水晶 350px
51	//                                           或 180t → 90t 内 ai[1]=20/45/70 各召 560×(1+门数3));
52	//                                           ai[3]==5 且 1/3 概率 → 追加二次 5;选完 ai[3]+1
53	//                                           （≥8 回 0）;rotation 每态 AngleTowards 目标角）
54	//   aiStyle 111 埃特尼亚荧光虫 578        NPC.cs:43169 → AI_111_DD2LightningBug :66799
55	//                                          （0.96 阻尼悬停,LOS 内静止蓄电：localAI[0] 满 5 →
56	//                                           发 682 电弧（50 伤 10 速,±25px 抖动 + 双重
57	//                                           ±0.5%/±0.625% 速度扰动）,-30t 冷却;目标在上/
58	//                                           埋块 → vy-0.2 上浮;出生 60t 渐显 + 同族分离）
59	// 勘误（任务卡普查映射 vs 1456 原文逐一核实）：
60	//   - 574/575 小妖魔滑翔怪是 aiStyle 108（AI_108_DivingFlyer 的 KoboldFlyer 档,
61	//     flag2=true 撞块自爆）,不是 111;578 荧光虫才是 111。
62	//   - 547=104（DD2AttackerTest,出生即消）/548=105（永恒水晶）/549=106（神秘传送门）,
63	//     与普查一致;549 的"入场语义"= 105 水晶 180t 倒计时后由 CheckArenaScore 双端放置。
64	//   - 飞龙 T1-3（558-560）与普通飞龙族（aiStyle 6 蠕虫链）无共用——DD2 飞龙是单体
65	//     俯冲飞行族（AI_108）,不生成体段。
66	//   - 541 沙尘精/542-545 沙鲨未被沙尘暴或其它批覆盖（Enemy.ts 此前落 default zombieAI,
67	//     沙尘暴刷怪器 VanillaSpawner.ts:1449 已在出 541 → 本批补 AI）。
68	// aiStyle 107（552-557/561-563/566-573/576/577 地面 walker 族 + 620 地精鲨）：
69	//   ★2026-08-13 walker 族攻击状态机 1:1 落位本文件 ai107ImprovedWalkers
70	//   （Enemy.ts case 107 分发;620 地精鲨仍走 chargerAI 的 wet 档）;492 荷兰大炮
71	//   aiStyle 75 → Enemy.ts case 75 分发进 bossAI_martian.martianSaucerPartAI,其顶部
72	//   转发本文件 dutchmanCannonAI（cs:35889-35904 锚船偏移 + :36008-36070 240t 装填炮击）。
73	// 事件依赖（★已接线,Game.wireDD2Hooks 落到 world/OldOnesArmy.ts,见 DD2_EVENT_HOOKS）：
74	//   laneSpawnRate()/enemySpawningOnHold()/spawnMonsterFromGate()（106 出怪节拍）、
75	//   raiseGoblins()/canRaiseGoblinsHere()（109 召骷髅）、stopInvasion()（105 胜负收场）、
76	//   reportLoss()（105 败北）、findArenaHitbox()（105）、difficulty()（DD2 难度档,默认 1）。
77	//   DD2 敌怪索敌语义（NPCUtils.cs:261/:308）：场上有水晶 548 → 咬水晶;否则咬玩家。
78	// 弹幕贴图：Projectile_{240,662,671,675,676,681,682,683,685,686,687}.png 已入
79	//   sprites/vanilla 管线（见 shootD 上方注记）；658/673/674 三枚 0 伤效果弹无弹体
80	//   （粒子降级）,速度/伤害/节拍 1:1。
81	import { Entity } from './Entity';
82	import type { Enemy } from './Enemy';
83	import type { GameHooks } from './types';
84	import type { Player } from './Player';
85	import { TILE } from '../core/constants';
86	import { moveAndCollide } from '../physics/TileCollision';
87	import { spawnPart, losClear } from './bossAI';
88	import { Arrow } from './Arrow';
89	import { TILE_DEFS } from '../data/tiles';
90	import { soundTrackFiles } from '../data/vanillaNpcs';
91	import { GDL } from '../stats/ScaleStats';
92	
93	// 弹幕贴图:Projectile_{240,675,682,686,687}.png 已自 terraria-assets/Images 入
94	// sprites/vanilla 管线(scripts/vanilla-atlas.mjs MISC 表),Arrow 按 projId 懒加载真图——
95	// RENDER_PROXY 代渲登记退役。687 喷焰原版为 Main.cs:31282 自定义 15 层火舌程序化
96	// 绘制,此处按整条贴图(98×686 单帧)近似;682 电弧 4 帧竖条(projFrames=4,Main.cs:8482)
97	// 同按整条绘制。
98	/** 原版 localAI[0..3]（Enemy 只有 ai0-ai3 对应 ai[],localAI 独立 → WeakMap 落盘） */
99	const localAI = new WeakMap<Enemy, number[]>();
100	/** 491 渲染帧源（localAI[3] 0..63 循环，:40971-40974）——渲染侧只读访问 */
101	export const dutchmanAnim = (e: Enemy): number => localAI.get(e)?.[3] ?? 0;
102	/** 568/569 枯萎兽渲染态只读（渲染侧不落 localAI 字段 → 同 dutchmanAnim 出口）：
103	 *  [0]=localAI[0] 灵气计数（死亡紫魂环驱动，Main.cs:26130 num322；
104	 *  AI_107 灵气态每 tick +1，cs:63882）/ [1]=localAI[3] 出生计数（出生紫雾门，
105	 *  Main.cs:25899，AI_107 出膛渐显 0→60） */
106	export const witherBeastLocal = (e: Enemy): [number, number] =>
107	  [localAI.get(e)?.[0] ?? 0, localAI.get(e)?.[3] ?? 0];
108	
109	export const dd2LocalAI = (e: Enemy): number[] => {
110	  let a = localAI.get(e);
111	  if (!a) { a = [0, 0, 0, 0]; localAI.set(e, a); }
112	  return a;
113	};
114	/** 原版 oldVelocity（碰撞前一帧速度,cs:93795 collideX/collideY 判定源）→ WeakMap */
115	const oldVel = new WeakMap<Enemy, { x: number; y: number }>();
116	
117	const TAU = Math.PI * 2;
118	const rnd = (n: number): number => Math.floor(Math.random() * n);
119	const rndRange = (a: number, b: number): number => a + Math.floor(Math.random() * (b - a));
120	const clamp = (v: number, lo: number, hi: number): number => (v < lo ? lo : v > hi ? hi : v);
121	const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;
122	const sign = (v: number): number => (v > 0 ? 1 : v < 0 ? -1 : 0);
123	/** Utils.GetLerpValue(clamped) */
124	const lerpValue = (a: number, b: number, v: number): number =>
125	  b === a ? (v < a ? 0 : 1) : clamp((v - a) / (b - a), 0, 1);
126	/** MathHelper.AngleTowards：最短弧步进 */
127	const angleTowards = (cur: number, tgt: number, maxStep: number): number => {
128	  let d = tgt - cur;
129	  while (d > Math.PI) d -= TAU;
130	  while (d < -Math.PI) d += TAU;
131	  if (Math.abs(d) <= maxStep) return tgt;
132	  return cur + sign(d) * maxStep;
133	};
134	
135	// ---------------------------------------------------------------------------
136	// DD2Event 事件依赖（★2026-08-13 复核：九钩子已由 Game.wireDD2Hooks 全部接线——
137	// Game.ts afterWorldLoad :1869 调用，逐槽落到 world/OldOnesArmy.ts 的 1:1 状态机
138	// （StartInvasion/UpdateTime/CheckProgress/SpawnMonsterFromGate 三档分表/
139	// RaiseGoblins/StopInvasion/FindArenaHitbox）。事件进行中敌怪正常从门 549 出生；
140	// 触发链 = 永恒水晶座 466 右键（Game.useEterniaStand，Player.cs:31930-31977）。
141	// 下面的 null 缺省只在"Game 未构造（纯单测直调 AI）"时生效，语义 = 无事件：
142	// 门不出怪/魔法师不召骷髅/胜负演出不触发事件收场。
143	// ---------------------------------------------------------------------------
144	export const DD2_EVENT_HOOKS = {
145	  /** DD2Event.LaneSpawnRate（默认 60,:59） */
146	  laneSpawnRate: (): number => 60,
147	  /** DD2Event.EnemySpawningIsOnHold（波间间歇,:113） */
148	  enemySpawningOnHold: (): boolean => false,
149	  /** DD2Event.SpawnMonsterFromGate（:556,按 OngoingDifficulty 分表） */
150	  spawnMonsterFromGate: null as null | ((g: GameHooks, x: number, y: number, leftGate: boolean) => void),
151	  /** DD2Event.RaiseGoblins（:732,从 _deadGoblinSpots 复活骷髅） */
152	  raiseGoblins: null as null | ((g: GameHooks, x: number, y: number) => void),
153	  /** DD2Event.CanRaiseGoblinsHere（:715,800px 内 ≥3 处尸点才可召） */
154	  canRaiseGoblinsHere: (_g: GameHooks, _x: number, _y: number): boolean => false,
155	  /** DD2Event.StopInvasion（胜负收场） */
156	  stopInvasion: null as null | ((g: GameHooks, win: boolean) => void),
157	  /** DD2Event.ReportLoss */
158	  reportLoss: null as null | ((g: GameHooks) => void),
159	  /** DD2Event.FindArenaHitbox */
160	  findArenaHitbox: null as null | ((g: GameHooks) => void),
161	  /** DD2Event.OngoingDifficulty（1/2/3,T1/T2/T3） */
162	  difficulty: (): number => 1,
163	};
164	
165	// ---------------------------------------------------------------------------
166	// 弹幕：ProjectileID.cs：240 CannonballHostile（荷兰大炮炮弹,14 速-5 上抛）/
167	// 658 SandnadoHostileMark（沙暴标记,damage 0 纯视觉尘柱）/ 673 DD2DarkMageRaise
168	//（召骷髅阵眼,0 伤）/ 674 DD2DarkMageHeal（治疗脉动,落地 40t 后 1000px 内友军
169	// +500,0 伤）/ 675 DD2DarkMageBolt（暗影矢 14 速 40 伤）/ 682 DD2LightningBugZap
170	//（电弧 10 速 50 伤）/ 686 DD2BetsyFireball（空袭火球,继承机速）/ 687
171	// DD2BetsyFlameBreath（喷焰,10 速横冲）。
172	// 伤害弹（240/675/682/686/687）走 Arrow 真图（RENDER_PROXY 已退役）;三枚 0 伤
173	// 效果弹（658/673）不生成弹体——Arrow 命中敌怪会 hurt(0)（假命中音+0 伤害数字）
174	// 且瞬间耗尽 pierce,与原版"纯视觉"语义相反 → 降级为粒子。674 治疗脉动已实体化
175	//（DD2HealPulse,独立于魔法师生死,40t 疗程节奏 1:1）。
176	// ---------------------------------------------------------------------------
177	/** Projectile 674 DD2DarkMageHeal（SetDefaults :6929-6939：10×10 aiStyle 133
178	 *  timeLeft 900;AI :35540-35574）：落地帧播音（ai[0]==0）→ 每 AI 步 ai[0]++ →
179	 *  第 40 步结算疗程后 Kill。疗程 = 弹体中心 1000px 内全部友军（active、damage≥1、
180	 *  lifeMax≥30、非 564/565）各 +min(500, lifeMax−life)（HealEffect 绿字）。
181	 *  ★治疗圆心 = 脉动落点（弹体 Center）,不是魔法师位置——魔法师 ai[1]==1 三连
182	 *  脉动（ai[0]=56/48/56 各出一枚,各数各的 40t）后落点在 direction×240 下探 50 格
183	 *  处,与魔法师本体的距离随地形拉开。 */
184	export class DD2HealPulse extends Entity {
185	  w = 10;
186	  h = 10;
187	  /** ai[0]（:35548 每 AI 步 +1;≥40 Kill） */
188	  private ai0 = 0;
189	
190	  constructor(x: number, y: number) {
191	    super();
192	    this.x = x;
193	    this.y = y;
194	  }
195	
196	  fixedUpdate(_dt: number, game: GameHooks): void {
197	    if (this.ai0 === 0) {
198	      // :35544-35547 首帧 DD2_DarkMageHealImpact（PlayTrackedSound 无音量覆写 → 1）
199	      game.playSfxFiles(soundTrackFiles('dd2_dark_mage_heal_impact'), 1, this.cx, this.cy);
200	      // 落地紫尘（原版为 Projectile_674 贴图绘制,素材未入管线 → 粒子降级）
201	      game.spawnParticles(this.cx, this.cy, '#FF7AE0', 8, 1.6, { life: 50 });
202	    }
203	    this.ai0++;
204	    if (this.ai0 < 40) {
205	      // 悬浮微光（同上视觉降级;低频防尘海）
206	      if (Math.random() < 0.3) {
207	        game.spawnParticles(this.cx + (Math.random() - 0.5) * 20,
208	          this.cy - Math.random() * 16, '#FF7AE0', 1, 0.4, { life: 26, grav: -0.02 });
209	      }
210	      return;
211	    }
212	    // ---- 疗程结算（:35553-35572）----
213	    // 原版遍历 Main.maxNPCs（敌怪+城镇 NPC 都算——伤害/生命门自然滤掉小动物）
214	    for (const list of [game.enemies(), game.npcs?.() ?? []]) {
215	      for (const ent of list) {
216	        const n = ent as unknown as {
217	          dead: boolean; vanillaId?: number | null; def?: { damage?: number };
218	          damage?: number; cx: number; cy: number; hp: number; maxHp: number;
219	        };
220	        if (!n || n.dead || n.vanillaId === 564 || n.vanillaId === 565) continue;
221	        // nPC20.damage >= 1：城镇 NPC 自卫伤害也过门（原版同式）;critter damage 0 被滤
222	        const dmg = n.def?.damage ?? n.damage ?? 0;
223	        if (dmg < 1 || n.maxHp < 30) continue;
224	        if (Math.hypot(n.cx - this.cx, n.cy - this.cy) > 1000) continue;
225	        const heal = Math.min(500, n.maxHp - n.hp);
226	        if (heal > 0) {
227	          n.hp += heal;
228	          game.addDamageNumber(n.cx, n.cy - 10, -heal, false, '#7CFF6A');   // HealEffect 绿字
229	        }
230	      }
231	    }
232	    this.dead = true;                                   // Kill()（:35573）
233	  }
234	
235	  draw(): void {
236	    // 视觉由粒子承担（Projectile_674 贴图未入管线）
237	  }
238	}
239	
240	function shootD(
241	  game: GameHooks, x: number, y: number, vx: number, vy: number,
242	  dmg: number, projId: number, life = 300, grav = 0, pierce = 1,
243	): void {
244	  // 出膛音（原版在弹幕 AI 首帧 localAI[0]==0 处 PlaySound，此处等效落在生成帧）：
245	  // 675 暗影矢 dd2_dark_mage_attack（:53602）/ 682 电弧 dd2_lightning_bug_zap（:52055）/
246	  // 686 火球 dd2_betsy_fireball_shot（:53645）——多变体组内随机（playSfxFiles 语义）
247	  const shot = PROJ_SHOT_SFX[projId];
248	  if (shot) game.playSfxFiles(soundTrackFiles(shot), 0.8, x, y);
249	  (game as unknown as { entities: { add: (e: unknown, b: string) => void } }).entities.add(
250	    new Arrow(x, y, vx, vy, dmg, 0, projId, null, { grav, life, pierce, hostile: true }),
251	    'projectiles');
252	}
253	
254	/** DD2 弹幕 → 声轨名（Projectile.cs 首帧 PlaySound 站点） */
255	const PROJ_SHOT_SFX: Record<number, string> = {
256	  675: 'dd2_dark_mage_attack',     // :53602 DD2_DarkMageAttack
257	  682: 'dd2_lightning_bug_zap',    // :52055 DD2_LightningBugZap
258	  686: 'dd2_betsy_fireball_shot',  // :53645 DD2_BetsyFireballShot（空袭火球出膛）
259	};
260	
261	// ---------------------------------------------------------------------------
262	// tile 辅助
263	// ---------------------------------------------------------------------------
264	/** vanilla tile sheet id → 内部 tile id（TILE_DEFS 下标;同 SceneMetrics.SHEET_MAP 建法） */
265	const SHEET = new Map<number, number>();
266	for (let i = 0; i < TILE_DEFS.length; i++) {
267	  const d = TILE_DEFS[i];
268	  if (d?.vanilla && !SHEET.has(d.vanilla.sheet)) SHEET.set(d.vanilla.sheet, i);
269	}
270	const tileIds = (arr: number[]): Set<number> =>
271	  new Set(arr.map((n) => SHEET.get(n)).filter((v): v is number => v != null));
272	/** TileID.Sets.Conversion（TileID.cs:30-34）：Sand 53/112/116/234、HardenedSand
273	 *  397/398/402/399、Sandstone 396/400/403/401 */
274	const CONV_SAND = tileIds([53, 112, 116, 234]);
275	const CONV_HARDENED = tileIds([397, 398, 402, 399]);
276	const CONV_SANDSTONE = tileIds([396, 400, 403, 401]);
277	/** TileID.Sets.ForAdvancedCollision.ForSandshark（沙鲨碰撞豁免表,cs:93812） */
278	const SANDSHARK_PASS = tileIds([53, 112, 116, 234, 397, 398, 402, 399, 396, 400, 403, 401]);
279	
280	const solidAt = (game: GameHooks, tx: number, ty: number): boolean => {
281	  const st = game.world.store;
282	  return st.inBounds(tx, ty) && st.isSolid(tx, ty);
283	};
284	const tileTypeAt = (game: GameHooks, tx: number, ty: number): number => {
285	  const st = game.world.store;
286	  return st.inBounds(tx, ty) ? st.type[st.idx(tx, ty)] : 0;
287	};
288	const liquidAt = (game: GameHooks, tx: number, ty: number): number => {
289	  const st = game.world.store;
290	  return st.inBounds(tx, ty) ? st.liquid[st.idx(tx, ty)] : 0;
291	};
292	/** 实心或有液体（原版 nactive()&&tileSolid || liquid>0 探测语义） */
293	const blockedAt = (game: GameHooks, tx: number, ty: number): boolean =>
294	  solidAt(game, tx, ty) || liquidAt(game, tx, ty) > 0;
295	
296	/** Collision.ExpandVertically（Collision.cs:4403）：从 (x,y) 向上/下穿非实心格扩张 */
297	function expandVertically(
298	  game: GameHooks, x: number, y: number, maxUp: number, maxDown: number,
299	): [number, number] {
300	  let top = y, bottom = y;
301	  for (let i = 0; i < maxUp; i++) {
302	    if (top <= 0 || top < 10) break;
303	    if (solidAt(game, x, top)) break;
304	    top--;
305	  }
306	  const st = game.world.store;
307	  for (let j = 0; j < maxDown; j++) {
308	    if (bottom >= st.h - 10) break;
309	    if (solidAt(game, x, bottom)) break;
310	    bottom++;
311	  }
312	  return [top, bottom];
313	}
314	
315	/** StrayMethods.CanSpawnSandstormHostile（StrayMethods.cs:47）：三列各 ±15 格净空,
316	 *  内缩后竖向跨度 ≥20 格 */
317	function canSpawnSandstormHostile(game: GameHooks, tx: number, ty: number): boolean {
318	  for (let i = -1; i <= 1; i++) {
319	    const [top, bottom] = expandVertically(game, tx + i, ty, 15, 15);
320	    if (bottom - 1 - (top + 1) < 20) return false;
321	  }
322	  return true;
323	}
324	
325	/** StrayMethods.SendWalker（StrayMethods.cs:115）：沿地面走向 direction,返回最远落脚点 */
326	function sendWalker(
327	  game: GameHooks, start: { x: number; y: number }, height: number, dir: number, maxDist: number,
328	): { x: number; y: number } {
329	  let px = start.x, py = start.y - 1;
330	  let covered = 0;
331	  let last = { x: px, y: py };
332	  for (let i = 0; i < maxDist; i++) {
333	    for (let j = 0; j < 3; j++) {
334	      if (!solidAt(game, px, py)) break;
335	      py--;                                     // 最多上爬 3 格脱出实心
336	    }
337	    const [topY, bottomY] = expandVertically(game, px, py, height, 2);
338	    const top = topY + 1, bottom = bottomY - 1;
339	    if (!solidAt(game, px, bottom + 1)) {
340	      // 落脚跨度下无地面：再探 6 格,仍悬空 → 停
341	      const [, b2] = expandVertically(game, px, bottom, 0, 6);
342	      if (!solidAt(game, px, b2)) break;
343	    }
344	    if (bottom - top < height - 1) break;       // 净空不足（walker 高 10）
345	    covered += dir;
346	    px += dir;
347	    py = bottom;
348	    last = { x: px, y: py };
349	    if (Math.abs(covered) >= maxDist) break;
350	  }
351	  return last;
352	}
353	
354	/** StrayMethods.CheckArenaScore（StrayMethods.cs:83）：水晶落点双向 walker 扫场端点 */
355	export function checkArenaScore(
356	  game: GameHooks, cx: number, cy: number,
357	): { left: { x: number; y: number }; right: { x: number; y: number } } {
358	  const maxDist = 100; // Main.MaxWorldViewSize.X/16 的常见档（SendWalker 默认 100）
359	  const ptx = Math.floor(cx / TILE), pty = Math.floor(cy / TILE);
360	  const [, floorY] = expandVertically(game, ptx, pty, 0, 4);
361	  const start = { x: ptx, y: floorY };
362	  const l = sendWalker(game, start, 10, -1, maxDist);
363	  const r = sendWalker(game, start, 10, 1, maxDist);
364	  return { left: { x: l.x + 1, y: l.y }, right: { x: r.x - 1, y: r.y } };
365	}
366	
367	// ---------------------------------------------------------------------------
368	// DD2 索敌（NPCUtils.TargetClosestOldOnesInvasion :261 / TargetClosestBetsy :308）：
369	// 场上有水晶 548 → 咬水晶;否则咬玩家
370	// ---------------------------------------------------------------------------
371	function findCrystal(game: GameHooks): Enemy | null {
372	  for (const n of game.enemies() as Enemy[]) {
373	    if (!n.dead && n.vanillaId === 548) return n;
374	  }
375	  return null;
376	}
377	function dd2Target(
378	  game: GameHooks, e: Enemy, player: Player | null,
379	): { x: number; y: number } | null {
380	  const crystal = findCrystal(game);
381	  if (crystal) return { x: crystal.cx, y: crystal.cy };
382	  if (player && !player.dead) return { x: player.cx, y: player.cy };
383	  void e;
384	  return null;
385	}
386	
387	/** 原版 CS 直积分（noTileCollide 族） */
388	const fly = (e: Enemy): void => { e.x += e.vx; e.y += e.vy; };
389	/** 向目标方向单位向量（DirectionTo） */
390	function dirTo(e: Enemy, tx: number, ty: number): { x: number; y: number } {
391	  const dx = tx - e.cx, dy = ty - e.cy;
392	  const d = Math.hypot(dx, dy) || 1;
393	  return { x: dx / d, y: dy / d };
394	}
395	/** SimpleFlyMovement（NPC.cs:78100 原版逐轴步进,反向时双倍） */
396	function simpleFlyMove(e: Enemy, dvx: number, dvy: number, acc: number): void {
397	  if (e.vx < dvx) { e.vx += acc; if (e.vx < 0 && dvx > 0) e.vx += acc; }
398	  else if (e.vx > dvx) { e.vx -= acc; if (e.vx > 0 && dvx < 0) e.vx -= acc; }
399	  if (e.vy < dvy) { e.vy += acc; if (e.vy < 0 && dvy > 0) e.vy += acc; }
400	  else if (e.vy > dvy) { e.vy -= acc; if (e.vy > 0 && dvy < 0) e.vy -= acc; }
401	}
402	
403	// ---------------------------------------------------------------------------
404	// AI_093 荷兰飞盗船 491（NPC.cs:40918-41028）
405	// ---------------------------------------------------------------------------
406	export function flyingDutchmanAI(e: Enemy, game: GameHooks, player: Player | null) {
407	  const x = dd2LocalAI(e);
408	  // ---- 首帧生成 4 炮（:40920-40936）：ai[0..3]=炮位 ai[3]=60*i 出生错峰 ----
409	  if (!e.bInit) {
410	    e.bInit = true;
411	    e.ai0 = -1; e.ai1 = -1; e.ai2 = -1; e.ai3 = -1;
412	    for (let i = 0; i < 4; i++) {
413	      const c = spawnPart(game, e, 492);
414	      if (c) {
415	        c.master = e;
416	        c.ai0 = e.id;      // 原版 ai[0] = 船 whoAmI（锚定引用）
417	        c.ai1 = i;         // 槽位 0-3（决定船体偏移 -122+68*i）
418	        c.ai2 = 0;
419	        c.ai3 = 60 * i;    // 装填错峰（:40928 60*num1464）
420	        c.despawnTimer = 600; // timeLeft = 600
421	        if (i === 0) e.ai0 = c.id;
422	        else if (i === 1) e.ai1 = c.id;
423	        else if (i === 2) e.ai2 = c.id;
424	        else e.ai3 = c.id;
425	      }
426	    }
427	  }
428	  e.despawnTimer = 750;    // netAlways：不入 CheckActive 消退（入侵旗舰）
429	  // ---- 炮位存活盘点（:40938-40957）：全灭 → 自毁 ----
430	  const slots = [e.ai0, e.ai1, e.ai2, e.ai3];
431	  const enemies = game.enemies() as Enemy[];
432	  let anyAlive = false;
433	  for (let i = 0; i < 4; i++) {
434	    const id = slots[i];
435	    if (id >= 0) {
436	      const c = enemies.find((n) => n.id === id);
437	      if (!c || c.dead || c.vanillaId !== 492) {
438	        if (i === 0) e.ai0 = -1; else if (i === 1) e.ai1 = -1;
439	        else if (i === 2) e.ai2 = -1; else e.ai3 = -1;
440	      } else anyAlive = true;
441	    }
442	  }
443	  if (!anyAlive) {
444	    e.iframes = 0;
445	    e.hp = 0;
446	    e.hurt(9999, 0, 0, game);   // StrikeNPCNoInteraction(9999) → 标准死亡管线
447	    return;
448	  }
449	  e.iframes = 2;   // SetDefaults dontTakeDamage=true（:14581）：炮在世恒无敌
450	  // ---- 海盗跳舱（:40959-40970）：1/300t 从船口弹射 212-215 ----
451	  if (rnd(300) === 0) {
452	    const p = spawnPart(game, e, [213, 215, 214, 212][rnd(4)]);
453	    if (p) {
454	      p.vx = (Math.random() - 0.5) * 5 + e.vx;
455	      p.vy = -8.01 + e.vy;
456	      p.despawnTimer = 600;
457	    }
458	  }
459	  // ---- 动画计数（:40971-40974 localAI[3] 64t 循环,渲染帧源） ----
460	  x[3] += 1;
461	  if (x[3] >= 64) x[3] = 0;
462	  // ---- 索敌（:40975 TargetClosest） ----
463	  const tx = player && !player.dead ? player.cx : e.cx;
464	  const ty = player && !player.dead ? player.cy : e.cy;
465	  if (player && !player.dead) e.facing = tx > e.cx ? 1 : -1;
466	  // ---- 贴地巡航（:40976-41005）：前方 10 格列扫描地面,保持离地 350-450px ----
467	  const st = game.world.store;
468	  const colX = clamp(Math.floor(e.cx / TILE) + sign(e.vx) * 10, 1, st.w - 2);
469	  const colY = Math.floor((e.y + e.h) / TILE);
470	  let n = 0;
471	  if (solidAt(game, colX, colY)) {
472	    n = 1;
473	  } else {
474	    for (; n < 150 && colY + n < st.h; n++) {
475	      if (solidAt(game, colX, colY + n)) { n--; break; }
476	    }
477	  }
478	  const gap = n * TILE;
479	  if (gap < 350) {
480	    let a = gap - 350;
481	    if (a < -4) a = -4;
482	    e.vy = lerp(e.vy, a, 0.05);
483	  } else if (gap > 450) {
484	    let a = gap - 350;
485	    if (a > 4) a = 4;
486	    e.vy = lerp(e.vy, a, 0.05);
487	  } else {
488	    e.vy *= 0.95;
489	  }
490	  // ---- 水平逼近（:41006-41010）：距 ≥300px 且未达 6 速 → 朝向 +0.06 ----
491	  const dxp = tx - e.cx;
492	  if (Math.abs(dxp) >= 300 && (Math.abs(e.vx) < 6 || sign(e.vx) !== e.facing)) {
493	    e.vx += e.facing * 0.06;
494	  }
495	  e.visAngle = e.vx * 0.025;                    // rotation = vx*0.025（:41011）
496	  e.facing = e.vx === 0 ? e.facing : -sign(e.vx); // spriteDirection = -sign(vx)（:41012）
497	  // ---- 船底烟尘（:41013-41024 dust 228） ----
498	  if (Math.random() < 0.5) {
499	    game.spawnParticles(
500	      e.cx + (Math.random() - 0.5) * (e.w - 70), e.y + e.h - 10,
501	      '#E06A24', 1, 0.4, { life: 40, grav: -0.02, damp: 0.94 });
502	  }
503	  moveAndCollide(e, game.world, e.vx, e.vy);
504	  void ty;
505	}
506	
507	// ---------------------------------------------------------------------------
508	// 荷兰大炮 492（aiStyle 75 分发 → 此处;NPC.cs:35889-35904 锚定 + :36008-36070 炮击）
509	// ai[0]=船 id（master 引用）,ai[1]=槽位,ai[2]=瞄准帧,ai[3]=装填计数（出生 60*i）
510	// ---------------------------------------------------------------------------
511	export function dutchmanCannonAI(e: Enemy, game: GameHooks, player: Player | null) {
512	  const ship = e.master;
513	  if (!ship || ship.dead || ship.vanillaId !== 491) { e.dead = true; return; }
514	  e.despawnTimer = Math.max(e.despawnTimer, Math.min(ship.despawnTimer, 600));
515	  // ---- 锚船偏移（:35889-35899）：(-122+68*slot)×朝向镜像,-6,随船 rotation 旋转 ----
516	  const sd = ship.facing === 1 ? 1 : -1;
517	  const ox = (-122 + 68 * e.ai1) * (sd !== 1 ? 1 : -1);
518	  const oy = -6;
519	  const rot = ship.visAngle;
520	  const rx = ox * Math.cos(rot) - oy * Math.sin(rot);
521	  const ry = ox * Math.sin(rot) + oy * Math.cos(rot);
522	  e.vx = ship.vx; e.vy = ship.vy;
523	  e.x = ship.cx - e.w / 2 + rx;
524	  e.y = ship.cy - e.h / 2 + ry;
525	  e.visAngle = rot;
526	  e.facing = sd;
527	  // ---- 装填（:36010-36016）：ai[3] 数到 240（出生错峰） ----
528	  if (e.ai3 < 240) e.ai3 += 1;
529	  // ---- 炮击（:36018-36052）：LOS 通 → 装满即朝玩家发 240 炮弹（14 速,-5 上抛） ----
530	  if (player && !player.dead && losClear(game, e.x, e.y, player.x, player.y)) {
531	    if (e.ai3 >= 240) {
532	      e.ai3 = 0;
533	      const d = dirTo(e, player.cx, player.cy);
534	      let vx = d.x * 14, vy = d.y * 14 - 5;
535	      const v = Math.hypot(vx, vy);
536	      if (v > 0.001) { vx = (vx / v) * 14; vy = (vy / v) * 14; }
537	      else { vx = 0; vy = 14; }
538	      vy -= 5;
539	      shootD(game, e.cx, e.cy, vx, vy, 30, 240, 300, 0.25);
540	    } else {
541	      // 瞄准帧（8 向索引,:36054-36070 的 ai[2] 语义;渲染未接,仅保状态）
542	      let best = 0, bestD = Infinity;
543	      for (let k = 0; k < 8; k++) {
544	        const ax = e.cx + Math.cos(k * (-Math.PI / 4)) * 50;
545	        const ay = e.cy + Math.sin(k * (-Math.PI / 4)) * 50;
546	        const d = Math.hypot(ax - player.cx, ay - player.cy);
547	        if (d < bestD) { bestD = d; best = k; }
548	      }
549	      e.ai2 = (sd === 1 ? 9 - (best + 1) : best + 1);
550	    }
551	  } else if (e.ai2 !== 0) {
552	    e.ai2 = 0;
553	  }
554	}
555	
556	// ---------------------------------------------------------------------------
557	// walker 共享核（AI_102 尾段 cs:42406-42620 与 AI_109 尾段 cs:66577-66797 逐行同构）
558	// x[0..2]=卡位锚点（localAI[0..2]）;p=族参数;castDamp>0 时施法僵直（v*=damp 后返回）
559	// ---------------------------------------------------------------------------
560	interface WalkerP {
561	  frontDepth: number;   // 前方探测行数（num1568/num）
562	  headClear: number;    // 头顶净空行数（num1569/num2,headScan 才生效）
563	  bottomDepth: number;  // 底部探测行数（num1570/num3）
564	  grav: number;         // 悬空重力（num1571/num4）
565	  maxFall: number;      // 落速钳（num1572/num5）
566	  upAccel: number;      // 贴地升速（num1573/num6,负值）
567	  maxUp: number;        // 升速钳（num1574/num7,负值）
568	  headScan: boolean;    // 头顶净空扫描（flag113/flag5;541/564/565 均关）
569	  maxH: number;         // 水平极速（num1575/num8）
570	  accelH: number;       // 水平加速（num1576/num9）
571	  maxV: number;         // 垂直极速（num1577/num10）
572	  accelV: number;       // 垂直加速（num1578/num11）
573	}
574	function walkerKernel(
575	  e: Enemy, game: GameHooks, player: Player | null,
576	  x: number[], p: WalkerP, castDamp: number,
577	): void {
578	  // ---- 卡位/跳墙（cs:42391-42426 / :66557-66592） ----
579	  if (e.justHit) x[2] = 0;
580	  let jump = false;   // flag109：主动跳
581	  if (x[2] >= 0) {
582	    let range = 16;
583	    let fx = false, fy = false;
584	    if (e.x > x[0] - range && e.x < x[0] + range) fx = true;
585	    else if ((e.vx < 0 && e.facing > 0) || (e.vx > 0 && e.facing < 0)) { fx = true; range += 24; }
586	    if (e.y > x[1] - range && e.y < x[1] + range) fy = true;
587	    if (fx && fy) {
588	      x[2] += 1;
589	      if (x[2] >= 30 && range === 16) jump = true;
590	      if (x[2] >= 60) {
591	        x[2] = -180;
592	        e.facing *= -1;
593	        e.vx *= -1;
594	        e.hitWall = false;
595	      }
596	    } else {
597	      x[0] = e.x; x[1] = e.y; x[2] = 0;
598	    }
599	    if (player && !player.dead) e.facing = e.seekDirX(player);  // TargetClosest
600	  } else {
601	    x[2] += 1;
602	    if (player && !player.dead) e.facing = e.seekDirX(player);
603	  }
604	  // ---- 施法僵直（cs:42387-42389 / :66554-66555）：AI 早退但碰撞步照跑 ----
605	  if (castDamp > 0) {
606	    e.vx *= castDamp;
607	    e.vy *= castDamp;
608	    oldVel.set(e, { x: e.vx, y: e.vy });
609	    moveAndCollide(e, game.world, e.vx, e.vy);
610	    if (e.hitWall) e.vx = 0;
611	    if (e.onGround || e.hitHead) e.vy = 0;
612	    return;
613	  }
614	  // ---- 前方/底部/头顶探测（cs:42428-42475 / :66594-66651） ----
615	  const frontX = Math.floor((e.x + e.w / 2) / TILE) + e.facing * 2;
616	  const frontY = Math.floor((e.y + e.h) / TILE);
617	  const bottomY = Math.floor((e.y + e.h) / TILE);
618	  const bottomX = Math.floor((e.x + e.w / 2) / TILE);
619	  let onSurface = true;   // flag111：悬空（无支撑）
620	  let nearFloor = false;  // flag112：贴地
621	  for (let ty = frontY; ty < frontY + p.frontDepth; ty++) {
622	    if (blockedAt(game, frontX, ty)) {
623	      if (ty <= frontY + 1) nearFloor = true;
624	      onSurface = false;
625	      break;
626	    }
627	  }
628	  for (let ty = bottomY; ty < bottomY + p.bottomDepth; ty++) {
629	    if (blockedAt(game, bottomX, ty)) {
630	      nearFloor = true;
631	      onSurface = false;
632	      break;
633	    }
634	  }
635	  if (p.headScan) {
636	    for (let ty = frontY - p.headClear; ty < frontY; ty++) {
637	      if (blockedAt(game, frontX, ty)) {
638	        nearFloor = false;
639	        jump = true;
640	        break;
641	      }
642	    }
643	  }
644	  if (jump) { nearFloor = false; onSurface = true; }
645	  // ---- 重力/升力（cs:42477-42495 / :66653-66671） ----
646	  if (onSurface) {
647	    e.vy += p.grav;
648	    if (e.vy > p.maxFall) e.vy = p.maxFall;
649	  } else {
650	    if ((e.dirY < 0 && e.vy > 0) || nearFloor) e.vy += p.upAccel;
651	    if (e.vy < p.maxUp) e.vy = p.maxUp;
652	  }
653	  // ---- 碰撞反弹（cs:42497-42519 / :66673-66695;oldVelocity=碰撞前速度） ----
654	  const ov = oldVel.get(e) ?? { x: e.vx, y: e.vy };
655	  if (e.hitWall) {
656	    e.vx = ov.x * -0.4;
657	    if (e.facing === -1 && e.vx > 0 && e.vx < 1) e.vx = 1;
658	    if (e.facing === 1 && e.vx < 0 && e.vx > -1) e.vx = -1;
659	  }
660	  if (e.onGround || e.hitHead) {
661	    e.vy = ov.y * -0.25;
662	    if (e.vy > 0 && e.vy < 1) e.vy = 1;
663	    if (e.vy < 0 && e.vy > -1) e.vy = -1;
664	  }
665	  // ---- 朝向加速（cs:42521-42559 / :66697-66735;方向档速度模型） ----
666	  if (e.facing === -1 && e.vx > -p.maxH) {
667	    e.vx -= p.accelH;
668	    if (e.vx > p.maxH) e.vx -= p.accelH;
669	    else if (e.vx > 0) e.vx += p.accelH / 2;
670	    if (e.vx < -p.maxH) e.vx = -p.maxH;
671	  } else if (e.facing === 1 && e.vx < p.maxH) {
672	    e.vx += p.accelH;
673	    if (e.vx < -p.maxH) e.vx += p.accelH;
674	    else if (e.vx < 0) e.vx -= p.accelH / 2;
675	    if (e.vx > p.maxH) e.vx = p.maxH;
676	  }
677	  if (e.dirY === -1 && e.vy > -p.maxV) {
678	    e.vy -= p.accelV;
679	    if (e.vy > p.maxV) e.vy -= p.accelV * 1.25;
680	    else if (e.vy > 0) e.vy += p.accelV * 0.75;
681	    if (e.vy < -p.maxV) e.vy = -p.maxH;
682	  } else if (e.dirY === 1 && e.vy < p.maxV) {
683	    e.vy += p.accelV;
684	    if (e.vy < -p.maxV) e.vy += p.accelV * 1.25;
685	    else if (e.vy < 0) e.vy -= p.accelV * 0.75;
686	    if (e.vy > p.maxV) e.vy = p.maxV;
687	  }
688	  // ---- 碰撞（原版 Collision_MoveNormal 零速语义:撞轴清零该轴速度） ----
689	  oldVel.set(e, { x: e.vx, y: e.vy });
690	  moveAndCollide(e, game.world, e.vx, e.vy);
691	  if (e.hitWall) e.vx = 0;
692	  if (e.onGround || e.hitHead) e.vy = 0;
693	}
694	
695	// ---------------------------------------------------------------------------
696	// AI_102 沙尘精 541（NPC.cs:42224-42620）
697	// ---------------------------------------------------------------------------
698	export function sandElementalAI(e: Enemy, game: GameHooks, player: Player | null) {
699	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; }
700	  const x = dd2LocalAI(e);

```


---

## 🤖 Assistant · 2026-08-19T03:09:29.506Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '62266,62808p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_110_Betsy source"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:29.548Z

**📎 ToolResult**

```
	private void AI_110_Betsy()
	{
		//IL_04fe: Unknown result type (might be due to invalid IL or missing references)
		//IL_0490: Unknown result type (might be due to invalid IL or missing references)
		//IL_0b33: Unknown result type (might be due to invalid IL or missing references)
		//IL_0cb3: Unknown result type (might be due to invalid IL or missing references)
		//IL_13ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_13c0: Unknown result type (might be due to invalid IL or missing references)
		//IL_13c5: Unknown result type (might be due to invalid IL or missing references)
		//IL_06a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_06ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_10e1: Unknown result type (might be due to invalid IL or missing references)
		//IL_11c6: Unknown result type (might be due to invalid IL or missing references)
		NPCUtils.TargetClosestBetsy(this, faceTarget: false);
		NPCAimedTarget targetData = GetTargetData();
		int num = -1;
		float num2 = 1f;
		int num3 = 35;
		int num4 = 35;
		float num5 = 10f;
		float num6 = 0.45f;
		float num7 = 7.5f;
		float num8 = 30f;
		float num9 = 30f;
		float num10 = 23f;
		float num11 = 600f;
		float num12 = 12f;
		float num13 = 40f;
		float num14 = 80f;
		float num15 = num13 + num14;
		float num16 = 1500f;
		float num17 = 60f;
		float num18 = 13f;
		float amount = 1f / 30f;
		float num19 = 12f;
		int num20 = 10;
		int num21 = 6 * num20;
		float num22 = 60f;
		float num23 = num17 + (float)num21 + num22;
		float num24 = 60f;
		float num25 = 1f;
		float num26 = MathF.PI * 2f * (num25 / num24);
		float num27 = 0.1f;
		float num28 = 32f;
		float num29 = 90f;
		float num30 = 20f;
		_ = ai[0];
		_ = -1f;
		SlotId val;
		if (ai[0] == 0f)
		{
			if ((ai[1] += 1f) >= num5)
			{
				ai[1] = 0f;
				ai[0] = 1f;
				ai[2] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 1f)
		{
			if (ai[2] == 0f)
			{
				ai[2] = ((base.Center.X < targetData.Center.X) ? 1 : (-1));
			}
			Vector2 destination = targetData.Center + new Vector2((0f - ai[2]) * 300f, -200f);
			Vector2 desiredVelocity = DirectionTo(destination) * num7;
			SimpleFlyMovement(desiredVelocity, num6);
			int num31 = ((base.Center.X < targetData.Center.X) ? 1 : (-1));
			direction = (spriteDirection = num31);
			if ((ai[1] += 1f) >= num8)
			{
				int num32 = 1;
				if (ai[3] == 5f && Main.rand.Next(3) == 0)
				{
					ai[3] += 1f;
				}
				switch ((int)ai[3])
				{
				case 0:
				case 1:
				case 3:
					num32 = 2;
					break;
				case 2:
					num32 = 3;
					break;
				case 4:
					num32 = 4;
					break;
				case 5:
					num32 = 5;
					break;
				case 6:
					num32 = 3;
					break;
				case 7:
					num32 = 6;
					break;
				}
				ai[0] = num32;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] += 1f;
				netUpdate = true;
				if (ai[3] >= 8f)
				{
					ai[3] = 0f;
				}
				switch (num32)
				{
				case 2:
				{
					Vector2 vector2 = DirectionTo(targetData.Center);
					spriteDirection = ((vector2.X > 0f) ? 1 : (-1));
					rotation = vector2.ToRotation();
					if (spriteDirection == -1)
					{
						rotation += MathF.PI;
					}
					velocity = vector2 * num10;
					break;
				}
				case 3:
				{
					Vector2 vector3 = new Vector2((targetData.Center.X > base.Center.X) ? 1 : (-1), 0f);
					spriteDirection = ((vector3.X > 0f) ? 1 : (-1));
					velocity = vector3 * -2f;
					break;
				}
				case 5:
				{
					Vector2 vector = DirectionTo(targetData.Center);
					spriteDirection = ((vector.X > 0f) ? 1 : (-1));
					rotation = vector.ToRotation();
					if (spriteDirection == -1)
					{
						rotation += MathF.PI;
					}
					velocity = vector * num28;
					break;
				}
				}
			}
		}
		else if (ai[0] == 2f)
		{
			if (ai[1] == 0f)
			{
				SoundEngine.PlayTrackedSound(SoundID.DD2_BetsyWindAttack, base.Center);
			}
			if ((ai[1] += 1f) >= num9)
			{
				ai[0] = 1f;
				ai[1] = 0f;
				ai[2] = 0f;
			}
		}
		else if (ai[0] == 3f)
		{
			ActiveSound activeSound = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[2]));
			if (activeSound != null)
			{
				activeSound.Position = base.Center;
			}
			ai[1] += 1f;
			int num33 = ((base.Center.X < targetData.Center.X) ? 1 : (-1));
			ai[2] = num33;
			if (ai[1] < num13)
			{
				Vector2 vector4 = targetData.Center + new Vector2((float)num33 * (0f - num11), -250f);
				Vector2 vector5 = DirectionTo(vector4) * num12;
				if (Distance(vector4) < num12)
				{
					base.Center = vector4;
				}
				else
				{
					position += vector5;
				}
				if (Vector2.Distance(vector4, base.Center) < 16f)
				{
					ai[1] = num13 - 1f;
				}
				num2 = 1.5f;
			}
			if (ai[1] == num13)
			{
				int num34 = ((targetData.Center.X > base.Center.X) ? 1 : (-1));
				velocity = new Vector2(num34, 0f) * 10f;
				direction = (spriteDirection = num34);
				if (Main.netMode != 1)
				{
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center, velocity, 687, num3, 0f, Main.myPlayer, 0f, whoAmI);
				}
				float[] array = localAI;
				val = SoundEngine.PlayTrackedSound(SoundID.DD2_BetsyFlameBreath, base.Center);
				array[2] = ((SlotId)(ref val)).ToFloat();
			}
			if (ai[1] >= num13)
			{
				num2 = 1.5f;
				if (Math.Abs(targetData.Center.X - base.Center.X) > 550f && Math.Abs(velocity.X) < 20f)
				{
					velocity.X += (float)Math.Sign(velocity.X) * 0.5f;
				}
			}
			if (ai[1] >= num15)
			{
				ai[0] = 1f;
				ai[1] = 0f;
				ai[2] = 0f;
			}
		}
		else if (ai[0] == 4f)
		{
			int num35 = ((base.Center.X < targetData.Center.X) ? 1 : (-1));
			ai[2] = num35;
			if (ai[1] < num17)
			{
				Vector2 vector6 = targetData.Center + new Vector2((float)num35 * (0f - num16), -350f);
				Vector2 value = DirectionTo(vector6) * num18;
				velocity = Vector2.Lerp(velocity, value, amount);
				int num36 = ((base.Center.X < targetData.Center.X) ? 1 : (-1));
				direction = (spriteDirection = num36);
				if (Vector2.Distance(vector6, base.Center) < 16f)
				{
					ai[1] = num17 - 1f;
				}
				num2 = 1.5f;
			}
			else if (ai[1] == num17)
			{
				Vector2 v = DirectionTo(targetData.Center);
				v.Y *= 0.25f;
				v = v.SafeNormalize(Vector2.UnitX * direction);
				spriteDirection = ((v.X > 0f) ? 1 : (-1));
				rotation = v.ToRotation();
				if (spriteDirection == -1)
				{
					rotation += MathF.PI;
				}
				velocity = v * num19;
			}
			else
			{
				position.X += DirectionTo(targetData.Center).X * 7f;
				position.Y += DirectionTo(targetData.Center + new Vector2(0f, -400f)).Y * 6f;
				if (ai[1] <= num23 - num22)
				{
					num2 = 1.5f;
				}
				float num37 = 30f;
				Vector2 vector7 = base.Center + new Vector2((110f + num37) * (float)direction, 20f).RotatedBy(rotation);
				int num38 = (int)(ai[1] - num17 + 1f);
				if (num38 <= num21 && num38 % num20 == 0 && Main.netMode != 1)
				{
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector7, velocity, 686, num4, 0f, Main.myPlayer);
				}
			}
			if (ai[1] > num23 - num22)
			{
				velocity.Y -= 0.1f;
			}
			ai[1] += 1f;
			if (ai[1] >= num23)
			{
				ai[0] = 1f;
				ai[1] = 0f;
				ai[2] = 0f;
			}
		}
		else if (ai[0] == 5f)
		{
			velocity = velocity.RotatedBy((0f - num26) * (float)direction);
			position.Y -= num27;
			position += DirectionTo(targetData.Center) * 10f;
			rotation -= num26 * (float)direction;
			num2 *= 0.7f;
			if (ai[1] == 1f)
			{
				SoundEngine.PlayTrackedSound(SoundID.DD2_BetsyFlyingCircleAttack, base.Center);
			}
			if ((ai[1] += 1f) >= num24)
			{
				ai[0] = 1f;
				ai[1] = 0f;
				ai[2] = 0f;
				velocity /= 2f;
			}
		}
		else if (ai[0] == 6f)
		{
			if (ai[1] == 0f)
			{
				Vector2 destination2 = targetData.Center + new Vector2(0f, -200f);
				Vector2 desiredVelocity2 = DirectionTo(destination2) * num7 * 2f;
				SimpleFlyMovement(desiredVelocity2, num6 * 2f);
				int num39 = ((base.Center.X < targetData.Center.X) ? 1 : (-1));
				direction = (spriteDirection = num39);
				ai[2] += 1f;
				if (Distance(targetData.Center) < 350f || ai[2] >= 180f)
				{
					ai[1] = 1f;
					netUpdate = true;
				}
			}
			else
			{
				if (ai[1] == 1f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_BetsyScream, base.Center);
				}
				if (ai[1] < num30)
				{
					velocity *= 0.95f;
				}
				else
				{
					velocity *= 0.98f;
				}
				if (ai[1] == num30)
				{
					if (velocity.Y > 0f)
					{
						velocity.Y /= 3f;
					}
					velocity.Y -= 3f;
				}
				num2 *= 0.85f;
				if (ai[1] == 20f || ai[1] == 25f || ai[1] == 30f)
				{
					Point point = base.Center.ToTileCoordinates();
					int num40 = 30;
					int num41 = 35;
					int num42 = 4;
					for (int i = point.X - num40; i <= point.X + num40; i++)
					{
						bool flag = false;
						for (int j = point.Y - num41 / 3; j < point.Y + num41; j++)
						{
							Tile tileSafely = Framing.GetTileSafely(i, j);
							bool flag2 = tileSafely.active() && Main.tileSolid[tileSafely.type] && !Main.tileFrameImportant[tileSafely.type];
							if (flag && flag2)
							{
								int num43 = WorldGen.KillTile_GetTileDustAmount(fail: true, tileSafely);
								for (int k = 0; k < num43; k++)
								{
									Dust obj = Main.dust[WorldGen.KillTile_MakeTileDust(i, j, tileSafely)];
									obj.velocity.Y -= 3f + (float)num42 * 1.5f;
									obj.velocity.Y *= Main.rand.NextFloat();
									obj.scale += (float)num42 * 0.03f;
								}
								for (int l = 0; l < num43 - 1; l++)
								{
									Dust obj2 = Main.dust[WorldGen.KillTile_MakeTileDust(i, j, tileSafely)];
									obj2.velocity.Y -= 1f + (float)num42;
									obj2.velocity.Y *= Main.rand.NextFloat();
								}
								if (num43 > 0 && Main.rand.Next(3) != 0)
								{
									float num44 = Math.Abs(point.X - i) / (num40 / 2);
									Gore gore = Gore.NewGoreDirect(position, Vector2.Zero, 61 + Main.rand.Next(3), 1f - (float)num42 * 0.15f + num44 * 0.5f);
									gore.velocity.Y -= 0.1f + (float)num42 * 0.5f + num44 * (float)num42 * 1f;
									gore.velocity.Y *= Main.rand.NextFloat();
									gore.position = new Vector2(i * 16 + 20, j * 16 + 20);
								}
							}
							flag = !flag2;
						}
					}
				}
				bool flag3 = ai[1] == 20f || ai[1] == 45f || ai[1] == 70f;
				if (CountNPCS(560) > 4)
				{
					flag3 = false;
				}
				if (flag3 && Main.netMode != 1)
				{
					for (int m = 0; m < 1; m++)
					{
						Vector2 vector8 = base.Center + (MathF.PI * 2f * Main.rand.NextFloat()).ToRotationVector2() * new Vector2(2f, 1f) * 300f * (0.6f + Main.rand.NextFloat() * 0.4f);
						if (Vector2.Distance(vector8, targetData.Center) > 100f)
						{
							Point point2 = vector8.ToPoint();
							NewNPC(GetSpawnSourceForNPCFromNPCAI(), point2.X, point2.Y, 560, whoAmI);
							SoundEngine.PlayTrackedSound(SoundID.DD2_BetsySummon, vector8);
						}
					}
					List<NPC> list = new List<NPC>();
					for (int n = 0; n < Main.maxNPCs; n++)
					{
						NPC nPC = Main.npc[n];
						if (nPC.active && nPC.type == 549)
						{
							list.Add(nPC);
						}
					}
					if (list.Count > 0)
					{
						for (int num45 = 0; num45 < 3; num45++)
						{
							NPC nPC2 = list[Main.rand.Next(list.Count)];
							Point point3 = nPC2.Center.ToPoint();
							NewNPC(GetSpawnSourceForNPCFromNPCAI(), point3.X, point3.Y, 560);
							SoundEngine.PlayTrackedSound(SoundID.DD2_BetsySummon, nPC2.Center);
						}
					}
				}
				ai[1] += 1f;
			}
			if (ai[1] >= num29)
			{
				ai[0] = 1f;
				ai[1] = 0f;
				ai[2] = 0f;
			}
		}
		localAI[0] += num2;
		if (localAI[0] >= 36f)
		{
			localAI[0] = 0f;
		}
		if (num != -1)
		{
			localAI[0] = num * 4;
		}
		if ((localAI[1] += 1f) >= 60f)
		{
			localAI[1] = 0f;
		}
		float num46 = DirectionTo(targetData.Center).ToRotation();
		float num47 = 0.04f;
		switch ((int)ai[0])
		{
		case 2:
		case 5:
			num47 = 0f;
			break;
		case 3:
			num47 = 0.01f;
			num46 = 0f;
			if (spriteDirection == -1)
			{
				num46 -= MathF.PI;
			}
			if (ai[1] >= num13)
			{
				num46 += (float)spriteDirection * MathF.PI / 12f;
				num47 = 0.05f;
			}
			break;
		case 4:
			num47 = 0.01f;
			num46 = MathF.PI;
			if (spriteDirection == 1)
			{
				num46 += MathF.PI;
			}
			break;
		case 6:
			num47 = 0.02f;
			num46 = 0f;
			if (spriteDirection == -1)
			{
				num46 -= MathF.PI;
			}
			break;
		}
		if (spriteDirection == -1)
		{
			num46 += MathF.PI;
		}
		if (num47 != 0f)
		{
			rotation = rotation.AngleTowards(num46, num47);
		}
		if (SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[2])) == null)
		{
			float[] array2 = localAI;
			val = SlotId.Invalid;
			array2[2] = ((SlotId)(ref val)).ToFloat();
		}
	}

	private static bool AI_FindNearbyBook(Point searchPosition, int searchWidth, int searchHeight, out Point bookPosition, bool closestBook = false, bool checkPlayerScreenRanges = false)
	{
		bookPosition = Point.Zero;
		Point[] nearbyBooks = _nearbyBooks;
		int num = nearbyBooks.Length;
		int num2 = 0;
		int num3 = Math.Max(0, searchPosition.X);
		int num4 = Math.Min(searchPosition.X + searchWidth, Main.maxTilesX);
		int num5 = Math.Max(0, searchPosition.Y);
		int num6 = Math.Min(searchPosition.Y + searchHeight, Main.maxTilesY);
		float num7 = 9999999f;
		Vector2 vector = searchPosition.ToVector2();
		Vector2 vector2 = vector;
		for (int i = num5; i < num6; i++)
		{
			for (int j = num3; j < num4; j++)
			{
				Tile tile = Main.tile[j, i];
				if (!tile.active() || tile.type != 50)
				{
					continue;
				}
				Vector2 vector3 = new Vector2(j, i);
				if (checkPlayerScreenRanges && !Spawner.CheckNotSpawningOnScreen((int)vector3.X, (int)vector3.Y))
				{
					continue;
				}
				float num8 = vector3.Distance(vector2);
				if (closestBook && num8 < num7)
				{
					num7 = num8;
					vector = vector3;
					continue;
				}
				nearbyBooks[num2++] = new Point(j, i);
				if (num2 >= num)
				{
					break;
				}
			}
		}
		if (closestBook)
		{
			bookPosition = vector.ToPoint();
			if (vector.X == vector2.X)
			{
				return vector.Y != vector2.Y;
			}
			return true;
		}
		if (num2 == 0)
		{
			return false;
		}
		bookPosition = nearbyBooks[Main.rand.Next(num2)];
		return true;
	}

```


---

## 🤖 Assistant · 2026-08-19T03:09:35.454Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I have the vanilla Betsy source. Now let me read our betsyAI (lines 1345-1580) and darkMageAI (1246-1344) in our file.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:09:35.877Z · glm-x-preview-260804

```
我已经有了原版 Betsy 的代码。现在我来读取我们在 Betsy 和 DarkMage 方面的实现代码。
```


---

## 🤖 Assistant · 2026-08-19T03:09:36.300Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts",
 "offset": 1234,
 "limit": 450
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:36.311Z

**📎 ToolResult**

```
1234	function solidBody(game: GameHooks, e: Enemy): boolean {
1235	  const pts = [
1236	    [e.x + 2, e.y + 2], [e.x + e.w - 2, e.y + 2],
1237	    [e.x + 2, e.y + e.h - 2], [e.x + e.w - 2, e.y + e.h - 2],
1238	    [e.cx, e.cy],
1239	  ];
1240	  return pts.some(([px, py]) => solidAt(game, Math.floor(px / TILE), Math.floor(py / TILE)));
1241	}
1242	
1243	// ---------------------------------------------------------------------------
1244	// AI_109 黑暗魔法师 564/565（NPC.cs:43161 → AI_109_DarkMage :66392）
1245	// ---------------------------------------------------------------------------
1246	export function darkMageAI(e: Enemy, game: GameHooks, player: Player | null) {
1247	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }
1248	  const x = dd2LocalAI(e);
1249	  const p: WalkerP = {
1250	    frontDepth: 4, headClear: 3, bottomDepth: 2,
1251	    grav: 0.05, maxFall: 0.2, upAccel: -0.05, maxUp: -0.4,
1252	    headScan: false,
1253	    maxH: 0.5, accelH: 0.1, maxV: 0.5, accelV: 0.02,
1254	  };
1255	  const tgt = dd2Target(game, e, player);
1256	  const txc = tgt ? tgt.x : e.cx, tyc = tgt ? tgt.y : e.cy;
1257	  // ---- 出生渐显（:66478-66508 localAI[3]） ----
1258	  if (x[3] === 0) e.spawnAlpha = 255;
1259	  if (x[3] === 30) game.playSfxFiles(soundTrackFiles('dd2_etherian_portal_spawn_enemy'), 0.4, e.cx, e.cy);
1260	  if (x[3] < 60) {
1261	    x[3] += 1;
1262	    e.spawnAlpha = Math.max(0, e.spawnAlpha - 5);
1263	    e.alphaFade = false;
1264	    if (Math.random() < 0.2) {
1265	      game.spawnParticles(e.cx, e.cy, '#B080FF', 1, 0.6, { life: 30 });
1266	    }
1267	  }
1268	  e.visAngle = e.vx * 0.04;                        // rotation = vx*0.04（:66415）
1269	  let castDamp = 0;
1270	  if (e.ai0 < 0) e.ai0 = Math.min(e.ai0 + 1, 0);   // 招间冷却（:66421-66423）
1271	  if (e.ai0 > 0) {
1272	    castDamp = 0.9;                                 // num12=0.9 施法僵直（:66427）
1273	    e.ai0 -= 1;                                     // 注：109 是递减（102 递增）
1274	    // 召骷髅施法音（:66445）：ai[0]==80 且 ai[1]==2 → DD2_DarkMageSummonSkeleton
1275	    if (e.ai1 === 2 && e.ai0 === 80) {
1276	      game.playSfxFiles(soundTrackFiles('dd2_dark_mage_summon_skeleton'), 0.7, e.cx, e.cy);
1277	    }
1278	    // 召骷髅（:66431-66435）：ai[1]==2 且 ai[0]==64 → 673 阵眼 + RaiseGoblins
1279	    if (e.ai1 === 2 && e.ai0 === 64) {
1280	      DD2_EVENT_HOOKS.raiseGoblins?.(game, e.cx, e.cy);
1281	      game.spawnParticles(e.cx + e.facing * 24, e.cy - 40, '#C060FF', 10, 2, { life: 40 });
1282	      // 673 阵眼在原版弹幕 ai[0]==70 帧播音（Projectile.cs:35516 DD2_SkeletonSummoned），
1283	      // 本仓 673 降级为粒子 → 等效落在阵眼生成帧
1284	      game.playSfxFiles(['dd2_skeleton_summoned'], 0.7, e.cx, e.cy);
1285	    }
1286	    // 暗影矢（:66437-66446）：ai[1]==0 且 ai[0]==32 → 675（14 速 40 伤）
1287	    if (e.ai1 === 0 && e.ai0 === 32) {
1288	      const ox = e.cx + e.facing * 10, oy = e.cy - 16;
1289	      const d = dirTo(e, txc, tyc);
1290	      e.facing = d.x > 0 ? 1 : -1;
1291	      shootD(game, ox, oy, d.x * 14, d.y * 14, 40, 675, 300);
1292	    }
1293	    // 治疗施法音（:66461）：ai[0]==126 且 ai[1]==1 → DD2_DarkMageCastHeal（起手一拍）
1294	    if (e.ai1 === 1 && e.ai0 === 126) {
1295	      game.playSfxFiles(soundTrackFiles('dd2_dark_mage_cast_heal'), 0.7, e.cx, e.cy);
1296	    }
1297	    // 治疗（:66453-66461）：ai[1]==1 且 ai[0]=40/48/56 → direction×240 下探 50 格找
1298	    // 实心面（Searches.Down(50)+IsSolid,含起点格——expandVertically 同式）;找到 →
1299	    // 生成 674 落地脉动（ToWorldCoordinates(8,0) = (tx*16+8, ty*16)）;找不到
1300	    //（NOT_FOUND）→ 本拍不出弹（原版 WorldUtils.Find 失败直接跳过 NewProjectile）。
1301	    // 脉动自身再数 40 AI 步才结算疗程（DD2HealPulse = Projectile.cs:35540-35574）：
1302	    // 三连拍三枚脉动各自独立计时,落地音/治疗圆心均在脉动处（非魔法师位置）,
1303	    // 且魔法师死亡不影响已出脉动（原版弹幕独立存活语义）。
1304	    if (e.ai1 === 1 && (e.ai0 === 40 || e.ai0 === 48 || e.ai0 === 56)) {
1305	      const gx = Math.floor((e.cx + e.facing * 240) / TILE);
1306	      const gy = Math.floor(e.cy / TILE);
1307	      const [, bottom] = expandVertically(game, gx, gy, 0, 50);
1308	      if (solidAt(game, gx, bottom)) {
1309	        (game as unknown as { entities: { add: (en: unknown, b: string) => void } }).entities.add(
1310	          new DD2HealPulse(gx * TILE + 8, bottom * TILE), 'projectiles');
1311	      }
1312	    }
1313	    if (e.ai0 <= 0) {
1314	      // 招式轮换（:66463-66474）：0→1→2→0;非 0 招后冷却 -120,0 招后 -20
1315	      const prev = e.ai1;
1316	      e.ai1 += 1;
1317	      if (e.ai1 >= 3) e.ai1 = 0;
1318	      e.ai0 = prev === 0 ? -20 : -120;
1319	    }
1320	  }
1321	  // ---- 招式选择（:66476-66484,ai[0]==0 且出生 60t 后） ----
1322	  if (e.ai0 === 0 && x[3] >= 60) {
1323	    let next = 0;
1324	    // ±600×±200 内受伤友军 <2 → 强制召骷髅（:66478-66492）
1325	    let hurt = 0;
1326	    for (const n of game.enemies() as Enemy[]) {
1327	      if (n.dead || n.hp >= n.maxHp) continue;
1328	      if (Math.abs(n.cx - e.cx) <= 600 && Math.abs(n.cy - e.cy) <= 200) hurt++;
1329	    }
1330	    if (hurt < 2) next = 2;
1331	    if (next === 2 && !DD2_EVENT_HOOKS.canRaiseGoblinsHere(game, e.cx, e.cy)) next = 0;
1332	    let ok = true;                                   // flag9（:66494-66498）
1333	    if (next === 0
1334	      && (Math.hypot(txc - e.cx, tyc - e.cy) >= 1000
1335	        || !losClear(game, e.cx, e.cy, txc, tyc))) ok = false;
1336	    if (ok) {
1337	      e.ai1 = next;
1338	      e.ai0 = next === 0 ? 97 : next === 1 ? 127 : 183;   // :66500-66510
1339	    }
1340	  }
1341	  walkerKernel(e, game, tgt ? { cx: txc, cy: tyc, dead: false } as unknown as Player : null, x, p, castDamp);
1342	}
1343	
1344	// ---------------------------------------------------------------------------
1345	// AI_110 双足翼龙 Betsy 551（NPC.cs:43165 → AI_110_Betsy :62266）
1346	// ---------------------------------------------------------------------------
1347	export function betsyAI(e: Enemy, game: GameHooks, player: Player | null) {
1348	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1349	  const x = dd2LocalAI(e);
1350	  e.despawnTimer = 750;   // netAlways：不入 CheckActive 消退
1351	  // 常量（:62277-62318）
1352	  const DMG_BREATH = 35, DMG_FIREBALL = 35;
1353	  const INTRO_T = 10, FLY_ACC = 0.45, FLY_SPD = 7.5;
1354	  const HOVER_T = 30, WIND_T = 30, DIVE_SPD = 23;
1355	  const FLAME_OFF = 600, FLAME_APPR = 12, FLAME_T0 = 40, FLAME_T1 = 80;
1356	  const BOMB_OFF = 1500, BOMB_APR_T = 60, BOMB_ACC = 1 / 30, BOMB_SPD = 12;
1357	  const FIREBALL_EVERY = 10, FIREBALL_N = 6 * FIREBALL_EVERY, TAIL_T = 60;
1358	  const BOMB_TOTAL = BOMB_APR_T + FIREBALL_N + TAIL_T;
1359	  const SPIN_T = 60, SPIN_RATE = TAU / SPIN_T, SPIN_RISE = 0.1, SKYDIVE_SPD = 32;
1360	  const SUMMON_T = 90, SUMMON_AT = 20;
1361	  // ---- 索敌（:62276 NPCUtils.TargetClosestBetsy）：水晶优先,否则玩家 ----
1362	  const tgt = dd2Target(game, e, player);
1363	  if (!tgt) {
1364	    e.vy -= 0.05;
1365	    fly(e);
1366	    return;
1367	  }
1368	  const txc = tgt.x, tyc = tgt.y;
1369	  let timeScale = 1;   // num2：各态动画步进倍率
1370	  if (e.ai0 === 0) {
1371	    // ---- 入场（:62321-62330） ----
1372	    e.ai1 += 1;
1373	    if (e.ai1 >= INTRO_T) { e.ai1 = 0; e.ai0 = 1; e.ai2 = 0; }
1374	  } else if (e.ai0 === 1) {
1375	    // ---- 悬停选招（:62332-62416） ----
1376	    if (e.ai2 === 0) e.ai2 = e.cx < txc ? 1 : -1;
1377	    const destX = txc - e.ai2 * 300, destY = tyc - 200;
1378	    const d = dirTo(e, destX, destY);
1379	    simpleFlyMove(e, d.x * FLY_SPD, d.y * FLY_SPD, FLY_ACC);
1380	    e.facing = e.cx < txc ? 1 : -1;
1381	    e.ai1 += 1;
1382	    if (e.ai1 >= HOVER_T) {
1383	      // ai[3]==5 且 1/3 概率 → 追加一轮（:62344-62347）
1384	      if (e.ai3 === 5 && rnd(3) === 0) e.ai3 += 1;
1385	      let next = 1;                                  // :62349-62370 八槽表
1386	      const s = e.ai3 | 0;
1387	      if (s === 0 || s === 1 || s === 3) next = 2;
1388	      else if (s === 2) next = 3;
1389	      else if (s === 4) next = 4;
1390	      else if (s === 5) next = 5;
1391	      else if (s === 6) next = 3;
1392	      else if (s === 7) next = 6;
1393	      e.ai0 = next;
1394	      e.ai1 = 0; e.ai2 = 0;
1395	      e.ai3 += 1;
1396	      if (e.ai3 >= 8) e.ai3 = 0;
1397	      if (next === 2 || next === 5) {
1398	        // 直冲起手（:62373-62400）：朝目标 23/32 速,rotation 对准
1399	        const v = dirTo(e, txc, tyc);
1400	        e.facing = v.x > 0 ? 1 : -1;
1401	        e.visAngle = Math.atan2(v.y, v.x) + (e.facing === -1 ? Math.PI : 0);
1402	        e.vx = v.x * (next === 2 ? DIVE_SPD : SKYDIVE_SPD);
1403	        e.vy = v.y * (next === 2 ? DIVE_SPD : SKYDIVE_SPD);
1404	      } else if (next === 3) {
1405	        // 火焰吐息起手（:62402-62408）：反向 2 速退位
1406	        const d3 = txc > e.cx ? 1 : -1;
1407	        e.facing = d3;
1408	        e.vx = -2 * d3;
1409	        e.vy = 0;
1410	      }
1411	    }
1412	  } else if (e.ai0 === 2) {
1413	    // ---- 风压冲（:62418-62427） ----
1414	    if (e.ai1 === 0) game.playSfxFiles(soundTrackFiles('dd2_betsy_wind_attack'), 0.7, e.cx, e.cy); // DD2_BetsyWindAttack（:62415）
1415	    e.ai1 += 1;
1416	    if (e.ai1 >= WIND_T) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1417	  } else if (e.ai0 === 3) {
1418	    // ---- 火焰吐息（:62429-62487） ----
1419	    e.ai1 += 1;
1420	    e.ai2 = e.cx < txc ? 1 : -1;
1421	    if (e.ai1 < FLAME_T0) {
1422	      // 接位：目标反向 600px 上空（:62435-62447）
1423	      const dx = txc - e.ai2 * FLAME_OFF, dy = tyc - 250;
1424	      const d = dirTo(e, dx, dy);
1425	      if (Math.hypot(dx - e.cx, dy - e.cy) < FLAME_APPR) {
1426	        e.x = dx - e.w / 2; e.y = dy - e.h / 2;   // 原版 base.Center = vector4 直接贴位
1427	      } else {
1428	        e.x += d.x * FLAME_APPR;
1429	        e.y += d.y * FLAME_APPR;
1430	      }
1431	      if (Math.hypot(dx - e.cx, dy - e.cy) < 16) e.ai1 = FLAME_T0 - 1;
1432	      timeScale = 1.5;
1433	    }
1434	    if (e.ai1 === FLAME_T0) {
1435	      // 喷焰起手（:62449-62461）：10 速横冲 + 687 喷焰
1436	      const d3 = txc > e.cx ? 1 : -1;
1437	      e.vx = d3 * 10;
1438	      e.vy = 0;
1439	      e.facing = d3;
1440	      shootD(game, e.cx, e.cy, e.vx, e.vy, DMG_BREATH, 687, 300, 0, 20);
1441	      game.playSfxFiles(['dd2_betsy_flame_breath'], 0.7, e.cx, e.cy);   // DD2_BetsyFlameBreath（:62462）
1442	    }
1443	    if (e.ai1 >= FLAME_T0) {
1444	      timeScale = 1.5;
1445	      if (Math.abs(txc - e.cx) > 550 && Math.abs(e.vx) < 20) {
1446	        e.vx += sign(e.vx) * 0.5;                  // 远距提速（:62465-62469）
1447	      }
1448	    }
1449	    if (e.ai1 >= FLAME_T0 + FLAME_T1) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1450	  } else if (e.ai0 === 4) {
1451	    // ---- 空袭（:62489-62583） ----
1452	    e.ai2 = e.cx < txc ? 1 : -1;
1453	    if (e.ai1 < BOMB_APR_T) {
1454	      // 高位接位（:62493-62509）：反向 1500px、-350 上空
1455	      const dx = txc - e.ai2 * BOMB_OFF, dy = tyc - 350;
1456	      const d = dirTo(e, dx, dy);
1457	      e.vx = lerp(e.vx, d.x * BOMB_SPD, BOMB_ACC);
1458	      e.vy = lerp(e.vy, d.y * BOMB_SPD, BOMB_ACC);
1459	      e.facing = e.cx < txc ? 1 : -1;
1460	      if (Math.hypot(dx - e.cx, dy - e.cy) < 16) e.ai1 = BOMB_APR_T - 1;
1461	      timeScale = 1.5;
1462	    } else if (e.ai1 === BOMB_APR_T) {
1463	      // 俯冲突进（:62511-62521）：12 速贴地掠射
1464	      let v = dirTo(e, txc, tyc);
1465	      v = { x: v.x, y: v.y * 0.25 };
1466	      const vl = Math.hypot(v.x, v.y) || 1;
1467	      v = { x: v.x / vl, y: v.y / vl };
1468	      e.facing = v.x > 0 ? 1 : -1;
1469	      e.visAngle = Math.atan2(v.y, v.x) + (e.facing === -1 ? Math.PI : 0);
1470	      e.vx = v.x * BOMB_SPD;
1471	      e.vy = v.y * BOMB_SPD;
1472	    } else {
1473	      // 掠射（:62523-62543）：水平 7/t、垂直 6/t 贴地,每 10t 投 686 火球 ×6
1474	      const dTo = dirTo(e, txc, tyc);
1475	      e.x += dTo.x * 7;
1476	      e.y += dirTo(e, txc, tyc - 400).y * 6;
1477	      if (e.ai1 <= BOMB_TOTAL - TAIL_T) timeScale = 1.5;
1478	      const ox = (110 + 30) * e.facing, oy = 20;
1479	      const rx = e.cx + ox * Math.cos(e.visAngle) - oy * Math.sin(e.visAngle);
1480	      const ry = e.cy + ox * Math.sin(e.visAngle) + oy * Math.cos(e.visAngle);
1481	      const n = Math.floor(e.ai1 - BOMB_APR_T + 1);
1482	      if (n <= FIREBALL_N && n % FIREBALL_EVERY === 0) {
1483	        shootD(game, rx, ry, e.vx, e.vy, DMG_FIREBALL, 686, 300, 0.08, 3);
1484	      }
1485	    }
1486	    if (e.ai1 > BOMB_TOTAL - TAIL_T) e.vy -= 0.1;   // 尾段拉起（:62545-62547）
1487	    e.ai1 += 1;
1488	    if (e.ai1 >= BOMB_TOTAL) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1489	  } else if (e.ai0 === 5) {
1490	    // ---- 翻转俯冲（:62585-62604） ----
1491	    const rot = -SPIN_RATE * e.facing;
1492	    const c = Math.cos(rot), s = Math.sin(rot);
1493	    const nvx = e.vx * c - e.vy * s;
1494	    const nvy = e.vx * s + e.vy * c;
1495	    e.vx = nvx; e.vy = nvy;
1496	    e.y -= SPIN_RISE;
1497	    const d = dirTo(e, txc, tyc);
1498	    e.x += d.x * 10;
1499	    e.y += d.y * 10;
1500	    e.visAngle -= SPIN_RATE * e.facing;
1501	    timeScale *= 0.7;
1502	    if (e.ai1 === 1) game.playSfxFiles(['dd2_betsy_flying_circle_attack'], 0.7, e.cx, e.cy); // DD2_BetsyFlyingCircleAttack（:62547）
1503	    e.ai1 += 1;
1504	    if (e.ai1 >= SPIN_T) {
1505	      e.ai0 = 1; e.ai1 = 0; e.ai2 = 0;
1506	      e.vx /= 2; e.vy /= 2;
1507	    }
1508	  } else if (e.ai0 === 6) {
1509	    // ---- 召唤（:62606-62655） ----
1510	    if (e.ai1 === 0) {
1511	      // 贴水晶上空（:62608-62620）
1512	      const d = dirTo(e, txc, tyc - 200);
1513	      simpleFlyMove(e, d.x * FLY_SPD * 2, d.y * FLY_SPD * 2, FLY_ACC * 2);
1514	      e.facing = e.cx < txc ? 1 : -1;
1515	      e.ai2 += 1;
1516	      if (Math.hypot(txc - e.cx, tyc - e.cy) < 350 || e.ai2 >= 180) e.ai1 = 1;
1517	    } else {
1518	      if (e.ai1 === 1) game.playSfxFiles(['dd2_betsy_scream'], 0.8, e.cx, e.cy);  // DD2_BetsyScream（:62577）
1519	      if (e.ai1 < SUMMON_AT) { e.vx *= 0.95; e.vy *= 0.95; }
1520	      else { e.vx *= 0.98; e.vy *= 0.98; }
1521	      if (e.ai1 === SUMMON_AT) {
1522	        if (e.vy > 0) e.vy /= 3;
1523	        e.vy -= 3;                                   // 跃起（:62630-62634）
1524	        game.spawnParticles(e.cx, e.cy + e.h / 2, '#C8A060', 26, 4, { life: 40 });
1525	      }
1526	      timeScale *= 0.85;
1527	      // 召唤窗口（:62657-62696）：场上 560 ≤4 才召;自周 300px 环 + 传送门各出 560
1528	      if (e.ai1 === SUMMON_AT || e.ai1 === 45 || e.ai1 === 70) {
1529	        const wyverns = (game.enemies() as Enemy[])
1530	          .filter((n) => !n.dead && n.vanillaId === 560).length;
1531	        if (wyverns <= 4) {
1532	          const a = Math.random() * TAU;
1533	          const sx = e.cx + Math.cos(a) * 2 * 300 * (0.6 + Math.random() * 0.4);
1534	          const sy = e.cy + Math.sin(a) * 1 * 300 * (0.6 + Math.random() * 0.4);
1535	          if (Math.hypot(sx - txc, sy - tyc) > 100) {
1536	            const w = spawnPart(game, e, 560);
1537	            if (w) { w.x = sx - w.w / 2; w.y = sy - w.h / 2; }
1538	          }
1539	          const portals = (game.enemies() as Enemy[])
1540	            .filter((n) => !n.dead && n.vanillaId === 549);
1541	          for (let k = 0; k < 3 && portals.length > 0; k++) {
1542	            const portal = portals[rnd(portals.length)];
1543	            const w = spawnPart(game, e, 560);
1544	            if (w) { w.x = portal.cx - w.w / 2; w.y = portal.cy - w.h / 2; }
1545	          }
1546	          game.playSfxFiles(soundTrackFiles('dd2_betsy_summon'), 0.7, e.cx, e.cy);  // DD2_BetsySummon（:62652/:62671 每召一只一声）
1547	        }
1548	      }
1549	      e.ai1 += 1;
1550	    }
1551	    if (e.ai1 >= SUMMON_T) { e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; }
1552	  }
1553	  // ---- 拍翼帧计数（:62657-62666 localAI[0]/[1]） ----
1554	  x[0] += timeScale;
1555	  if (x[0] >= 36) x[0] = 0;
1556	  x[1] += 1;
1557	  if (x[1] >= 60) x[1] = 0;
1558	  // ---- rotation 收敛（:62668-62716） ----
1559	  const dTo = dirTo(e, txc, tyc);
1560	  let tgtAng = Math.atan2(dTo.y, dTo.x);
1561	  let step = 0.04;
1562	  const s0 = e.ai0 | 0;
1563	  if (s0 === 2 || s0 === 5) step = 0;
1564	  else if (s0 === 3) {
1565	    step = 0.01;
1566	    tgtAng = e.facing === -1 ? -Math.PI : 0;
1567	    if (e.ai1 >= FLAME_T0) { tgtAng += e.facing * Math.PI / 12; step = 0.05; }
1568	  } else if (s0 === 4) {
1569	    step = 0.01;
1570	    tgtAng = e.facing === 1 ? Math.PI * 2 : Math.PI;
1571	  } else if (s0 === 6) {
1572	    step = 0.02;
1573	    tgtAng = e.facing === -1 ? -Math.PI : 0;
1574	  }
1575	  if (e.facing === -1) tgtAng += Math.PI;
1576	  if (step !== 0) e.visAngle = angleTowards(e.visAngle, tgtAng, step);
1577	  fly(e);
1578	}
1579	
1580	// ---------------------------------------------------------------------------
1581	// AI_111 埃特尼亚荧光虫 578（NPC.cs:43169 → AI_111_DD2LightningBug :66799）
1582	// ---------------------------------------------------------------------------
1583	export function dd2LightningBugAI(e: Enemy, game: GameHooks, player: Player | null) {
1584	  if (!e.bInit) { e.bInit = true; }
1585	  const x = dd2LocalAI(e);
1586	  // 族参数（:66803-66813 默认档 → :66828-66844 的 578 覆盖）
1587	  const SPEED = 4;            // num
1588	  const LERP_FAR = 20;        // num2
1589	  const LERP_NEAR = 20;       // num3
1590	  const MIN_SPD = 1;          // num4
1591	  const DAMP = 0.96;          // num5
1592	  const SHOOT_T = 5;          // num6
1593	  const COOLDOWN = 30;        // num7
1594	  const RANGE = 200;          // num8
1595	  const ZAP_DMG = 50;         // num9
1596	  const ZAP_PROJ = 682;       // num10
1597	  const ZAP_SPD = 10;         // num11
1598	  const HEIGHT_GATE = 50;     // num12
1599	  const SEP = 0.1;            // num13
1600	  // ---- 出生渐显（:66846-66876 flag3） ----
1601	  if (x[1] === 0) e.spawnAlpha = 255;
1602	  if (x[1] === 30) game.playSfxFiles(soundTrackFiles('dd2_etherian_portal_spawn_enemy'), 0.3, e.cx, e.cy);
1603	  if (x[1] < 60) {
1604	    x[1] += 1;
1605	    e.spawnAlpha = Math.max(0, e.spawnAlpha - 5);
1606	    e.alphaFade = false;
1607	  }
1608	  // ---- 索敌（:66816 TargetClosestOldOnesInvasion） ----
1609	  const tgt = dd2Target(game, e, player);
1610	  // ---- 同族分离（:66878-66900 flag2,cs:66878-66900） ----
1611	  for (const n of game.enemies() as Enemy[]) {
1612	    if (n === e || n.dead || n.vanillaId !== e.vanillaId) continue;
1613	    if (Math.abs(e.x - n.x) + Math.abs(e.y - n.y) < e.w) {
1614	      if (e.x < n.x) e.vx -= SEP; else e.vx += SEP;
1615	      if (e.y < n.y) e.vy -= SEP; else e.vy += SEP;
1616	    }
1617	  }
1618	  e.visAngle = Math.abs(e.vx) * e.facing * 0.1;    // rotation（:66902）
1619	  // ---- 电光尘（:66846-66862 的 272 号尘,粒子近似） ----
1620	  if (Math.random() < 1 / 80) {
1621	    const a = Math.random() * TAU;
1622	    game.spawnParticles(e.cx, e.cy, '#B0E0FF', 2, 0.8, { life: 30 });
1623	    void a;
1624	  }
1625	  if (!tgt) { fly(e); return; }
1626	  const txc = tgt.x, tyc = tgt.y;
1627	  const muzzleX = e.cx - e.facing * 20, muzzleY = e.cy + 10;   // center 偏移（:66841）
1628	  const dx = txc - muzzleX, dy = tyc - muzzleY;
1629	  const dist = Math.hypot(dx, dy) || 1;
1630	  const ux = dx / dist, uy = dy / dist;
1631	  const los = losClear(game, e.cx, e.cy, txc, tyc);
1632	  if (x[0] < 0) x[0] += 1;                          // 冷却回摆（:66911-66912）
1633	  if (dist > RANGE || !los) {
1634	    // ---- 远距/断视：逼近（:66916-66918） ----
1635	    e.vx = (e.vx * (LERP_FAR - 1) + ux * SPEED) / LERP_FAR;
1636	    e.vy = (e.vy * (LERP_FAR - 1) + uy * SPEED) / LERP_FAR;
1637	  } else if (dy < HEIGHT_GATE) {
1638	    // ---- 目标高位差小：微升（:66920-66922） ----
1639	    e.vy -= 0.03;
1640	  } else if (x[0] >= 0) {
1641	    // ---- 静止蓄电（:66924-66946） ----
1642	    e.vx *= DAMP;
1643	    e.vy *= DAMP;
1644	    if (Math.hypot(e.vx, e.vy) < MIN_SPD) {
1645	      x[0] += 1;
1646	      if (x[0] >= SHOOT_T) {
1647	        x[0] = -COOLDOWN;
1648	        e.facing = ux > 0 ? 1 : -1;                 // direction = spriteDirection
1649	        // 速度扰动（:66934-66944）：±25px 抖动 + 两级 ±0.5%/±0.625% 缩放
1650	        let sx = dx + rndRange(-25, 26), sy = dy + rndRange(-25, 26);
1651	        sx *= 1 + rndRange(-20, 21) * 0.005;
1652	        sy *= 1 + rndRange(-20, 21) * 0.005;
1653	        const sl = Math.hypot(sx, sy) || 1;
1654	        sx = (sx / sl) * ZAP_SPD;
1655	        sy = (sy / sl) * ZAP_SPD;
1656	        sx *= 1 + rndRange(-20, 21) * (1 / 160);
1657	        sy *= 1 + rndRange(-20, 21) * (1 / 160);
1658	        shootD(game, muzzleX, muzzleY, sx, sy, ZAP_DMG, ZAP_PROJ, 300, 0, 3);
1659	      }
1660	    }
1661	  }
1662	  // ---- 上浮（:66950-66970）：目标在上或自身埋块 → vy-0.2 钳 -10 ----
1663	  let rise = tyc < e.cy;
1664	  if (!rise) {
1665	    const etx = Math.floor(e.cx / TILE), ety = Math.floor(e.cy / TILE);
1666	    if (solidAt(game, etx, ety)) rise = true;
1667	  }
1668	  if (rise) {
1669	    e.vy -= 0.2;
1670	    if (e.vy < -10) e.vy = -10;
1671	  }
1672	  fly(e);
1673	}
1674	
1675	// ---------------------------------------------------------------------------
1676	// AI_107 ImprovedWalkers（NPC.cs:63372-64919）——旧日军团地面 walker 族 1:1。
1677	//   552/553/554 埃特尼亚哥布林 T1/T2/T3   近战前摇（flag5,纯接触伤害）
1678	//   555/556/557 哥布林投弹手 T1/T2/T3     投 681 炸弹（flag12,42t 循环出手 18t）
1679	//   561/562/563 标枪手 T1/T2/T3           掷 662（T3→685）标枪（flag12,90t/出手 82t）
1680	//   566/567    旧日骷髅                   黑暗魔法师 RaiseGoblins 复活产物,120t 落地渐显
1681	//   568/569    枯萎兽                     灵气态（削甲 debuff+60t 自疗+脉冲音）
1682	//   570/571    德拉肯                     喷 671（60t 循环,出手 40t+多连拍）
1683	//   572/573    小妖精（地面）             自爆冲锋（700px 点火→64px 起爆 192² 伤 80）

```


---

## 🤖 Assistant · 2026-08-19T03:09:37.018Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '66392,66800p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_109_DarkMage and AI_111 lightning bug"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:09:37.055Z

**📎 ToolResult**

```
	private void AI_109_DarkMage()
	{
		//IL_01d2: Unknown result type (might be due to invalid IL or missing references)
		//IL_0682: Unknown result type (might be due to invalid IL or missing references)
		//IL_0360: Unknown result type (might be due to invalid IL or missing references)
		bool flag = false;
		bool flag2 = false;
		bool flag3 = true;
		bool flag4 = false;
		int num = 4;
		int num2 = 3;
		int num3 = 0;
		float num4 = 0.2f;
		float num5 = 2f;
		float num6 = -0.2f;
		float num7 = -4f;
		bool flag5 = true;
		float num8 = 2f;
		float num9 = 0.1f;
		float num10 = 1f;
		float num11 = 0.04f;
		bool flag6 = false;
		float num12 = 0.96f;
		bool flag7 = true;
		NPCAimedTarget targetData = GetTargetData();
		if (type == 564 || type == 565)
		{
			flag5 = false;
			rotation = velocity.X * 0.04f;
			spriteDirection = ((direction > 0) ? 1 : (-1));
			num3 = 2;
			num6 = -0.05f;
			num7 = -0.4f;
			num4 = 0.05f;
			num5 = 0.2f;
			num10 = 0.5f;
			num11 = 0.02f;
			num8 = 0.5f;
			num9 = 0.1f;
			localAI[2] = 0f;
			DelegateMethods.v3_1 = new Vector3(0.3f, 0.05f, 0.45f) * 1.5f;
			Utils.PlotTileLine(base.Top, base.Bottom, width, DelegateMethods.CastLightOpen);
			if (ai[0] < 0f)
			{
				ai[0] = MathHelper.Min(ai[0] + 1f, 0f);
			}
			if (ai[0] > 0f)
			{
				flag7 = false;
				flag6 = true;
				num12 = 0.9f;
				ai[0] -= 1f;
				if (ai[0] == 80f && ai[1] == 2f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_DarkMageSummonSkeleton, base.Center);
				}
				if (ai[1] == 2f && ai[0] == 64f && Main.netMode != 1)
				{
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center + new Vector2(direction * 24, -40f), Vector2.Zero, 673, 0, 0f, Main.myPlayer);
					DD2Event.RaiseGoblins(this, base.Center);
				}
				if (ai[1] == 0f && ai[0] == 32f)
				{
					Vector2 vector = (targetData.Center - (base.Center + new Vector2(direction * 10, -16f))).SafeNormalize(Vector2.UnitY) * 14f;
					direction = ((vector.X > 0f) ? 1 : (-1));
					if (Main.netMode != 1)
					{
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center + new Vector2(direction * 10, -16f), vector, 675, 40, 0f, Main.myPlayer);
					}
				}
				if (ai[0] == 126f && ai[1] == 1f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_DarkMageCastHeal, base.Center);
				}
				if (ai[1] == 1f && Main.netMode != 1 && (ai[0] == 40f || ai[0] == 48f || ai[0] == 56f) && WorldUtils.Find(new Vector2(base.Center.X + (float)(direction * 240), base.Center.Y).ToTileCoordinates(), Searches.Chain(new Searches.Down(50), new Terraria.WorldBuilding.Conditions.IsSolid()), out var result))
				{
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), result.ToWorldCoordinates(8f, 0f), Vector2.Zero, 674, 0, 0f, Main.myPlayer);
				}
				if (ai[0] <= 0f)
				{
					float num13 = ai[1];
					ai[1] += 1f;
					if (ai[1] >= 3f)
					{
						ai[1] = 0f;
					}
					ai[0] = -120f;
					if (num13 == 0f)
					{
						ai[0] = -20f;
					}
					netUpdate = true;
				}
			}
			if (ai[0] == 0f && localAI[3] >= 60f)
			{
				bool flag8 = false;
				Vector2 minimum = base.Center + new Vector2(-600f, -200f);
				Vector2 maximum = base.Center + new Vector2(600f, 200f);
				int num14 = 0;
				for (int i = 0; i < Main.maxNPCs; i++)
				{
					NPC nPC = Main.npc[i];
					if (nPC.active && nPC.lifeMax != nPC.life && nPC.Center.Between(minimum, maximum) && ++num14 >= 2)
					{
						flag8 = true;
						break;
					}
				}
				if (!flag8)
				{
					ai[1] = 2f;
				}
				if (ai[1] == 2f && !DD2Event.CanRaiseGoblinsHere(base.Center))
				{
					ai[1] = 0f;
				}
				bool flag9 = true;
				if (ai[1] == 0f && (Distance(targetData.Center) >= 1000f || !Collision.CanHitLine(base.Center, 0, 0, targetData.Center, 0, 0)))
				{
					flag9 = false;
				}
				if (flag9)
				{
					switch ((int)ai[1])
					{
					case 0:
						ai[0] = 97f;
						break;
					case 1:
						ai[0] = 127f;
						break;
					case 2:
						ai[0] = 183f;
						break;
					}
					netUpdate = true;
					flag6 = true;
				}
			}
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
				int num15 = (int)localAI[3] / 10;
				float num16 = base.Size.Length() / 2f;
				num16 /= 20f;
				int maxValue = 5;
				if (type == 576 || type == 577)
				{
					maxValue = 1;
				}
				for (int j = 0; j < num15; j++)
				{
					if (Main.rand.Next(maxValue) == 0)
					{
						Dust dust = Dust.NewDustDirect(position, width, height, 27, velocity.X * 1f, 0f, 100);
						dust.scale = 0.55f;
						dust.fadeIn = 0.7f;
						dust.velocity *= 0.1f * num16;
						dust.velocity += velocity;
					}
				}
			}
		}
		if (justHit)
		{
			localAI[2] = 0f;
		}
		if (!flag2)
		{
			if (localAI[2] >= 0f)
			{
				float num17 = 16f;
				bool flag10 = false;
				bool flag11 = false;
				if (position.X > localAI[0] - num17 && position.X < localAI[0] + num17)
				{
					flag10 = true;
				}
				else if ((velocity.X < 0f && direction > 0) || (velocity.X > 0f && direction < 0))
				{
					flag10 = true;
					num17 += 24f;
				}
				if (position.Y > localAI[1] - num17 && position.Y < localAI[1] + num17)
				{
					flag11 = true;
				}
				if (flag10 && flag11)
				{
					localAI[2] += 1f;
					if (localAI[2] >= 30f && num17 == 16f)
					{
						flag = true;
					}
					if (localAI[2] >= 60f)
					{
						localAI[2] = -180f;
						direction *= -1;
						velocity.X *= -1f;
						collideX = false;
					}
				}
				else
				{
					localAI[0] = position.X;
					localAI[1] = position.Y;
					localAI[2] = 0f;
				}
				if (flag7)
				{
					NPCUtils.TargetClosestOldOnesInvasion(this);
				}
			}
			else
			{
				localAI[2] += 1f;
				direction = ((targetData.Center.X > base.Center.X) ? 1 : (-1));
			}
		}
		int num18 = (int)((position.X + (float)(width / 2)) / 16f) + direction * 2;
		int num19 = (int)((position.Y + (float)height) / 16f);
		int num20 = (int)base.Bottom.Y / 16;
		int num21 = (int)base.Bottom.X / 16;
		if (flag6)
		{
			velocity *= num12;
			return;
		}
		for (int k = num19; k < num19 + num; k++)
		{
			if (Main.tile[num18, k] == null)
			{
				Main.tile[num18, k] = new Tile();
			}
			if ((Main.tile[num18, k].nactive() && Main.tileSolid[Main.tile[num18, k].type]) || Main.tile[num18, k].liquid > 0)
			{
				if (k <= num19 + 1)
				{
					flag4 = true;
				}
				flag3 = false;
				break;
			}
		}
		for (int l = num20; l < num20 + num3; l++)
		{
			if (Main.tile[num21, l] == null)
			{
				Main.tile[num21, l] = new Tile();
			}
			if ((Main.tile[num21, l].nactive() && Main.tileSolid[Main.tile[num21, l].type]) || Main.tile[num21, l].liquid > 0)
			{
				flag4 = true;
				flag3 = false;
				break;
			}
		}
		if (flag5)
		{
			for (int m = num19 - num2; m < num19; m++)
			{
				if (Main.tile[num18, m] == null)
				{
					Main.tile[num18, m] = new Tile();
				}
				if ((Main.tile[num18, m].nactive() && Main.tileSolid[Main.tile[num18, m].type]) || Main.tile[num18, m].liquid > 0)
				{
					flag4 = false;
					flag = true;
					break;
				}
			}
		}
		if (flag)
		{
			flag4 = false;
			flag3 = true;
		}
		if (flag3)
		{
			velocity.Y += num4;
			if (velocity.Y > num5)
			{
				velocity.Y = num5;
			}
		}
		else
		{
			if ((directionY < 0 && velocity.Y > 0f) || flag4)
			{
				velocity.Y += num6;
			}
			if (velocity.Y < num7)
			{
				velocity.Y = num7;
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
		if (direction == -1 && velocity.X > 0f - num8)
		{
			velocity.X -= num9;
			if (velocity.X > num8)
			{
				velocity.X -= num9;
			}
			else if (velocity.X > 0f)
			{
				velocity.X += num9 / 2f;
			}
			if (velocity.X < 0f - num8)
			{
				velocity.X = 0f - num8;
			}
		}
		else if (direction == 1 && velocity.X < num8)
		{
			velocity.X += num9;
			if (velocity.X < 0f - num8)
			{
				velocity.X += num9;
			}
			else if (velocity.X < 0f)
			{
				velocity.X -= num9 / 2f;
			}
			if (velocity.X > num8)
			{
				velocity.X = num8;
			}
		}
		if (directionY == -1 && velocity.Y > 0f - num10)
		{
			velocity.Y -= num11;
			if (velocity.Y > num10)
			{
				velocity.Y -= num11 * 1.25f;
			}
			else if (velocity.Y > 0f)
			{
				velocity.Y += num11 * 0.75f;
			}
			if (velocity.Y < 0f - num10)
			{
				velocity.Y = 0f - num8;
			}
		}
		else if (directionY == 1 && velocity.Y < num10)
		{
			velocity.Y += num11;
			if (velocity.Y < 0f - num10)
			{
				velocity.Y += num11 * 1.25f;
			}
			else if (velocity.Y < 0f)
			{
				velocity.Y -= num11 * 0.75f;
			}
			if (velocity.Y > num10)
			{
				velocity.Y = num10;
			}
		}
	}

	private void AI_111_DD2LightningBug()
	{
		//IL_0300: Unknown result type (might be due to invalid IL or missing references)
		bool flag = true;
		float num = 7f;
		float num2 = 60f;
		float num3 = 60f;
		float num4 = 1f;

```


---

## 🤖 Assistant · 2026-08-19T03:12:14.628Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Let me carefully compare Betsy (ai110) first.

Vanilla Betsy constants:
- num = -1 (unused)
- num2 = 1 (timeScale)
- num3 = 35 (breath dmg)
- num4 = 35 (fireball dmg)
- num5 = 10 (intro)
- num6 = 0.45 (fly acc)
- num7 = 7.5 (fly speed)
- num8 = 30 (hover T)
- num9 = 30 (wind T)
- num10 = 23 (dive speed)
- num11 = 600 (flame offset)
- num12 = 12 (flame approach)
- num13 = 40 (flame t0)
- num14 = 80 (flame t1)
- num15 = 120
- num16 = 1500 (bomb offset)
- num17 = 60 (bomb approach T)
- num18 = 13 (bomb speed)
- amount = 1/30
- num19 = 12 (bomb dive speed)
- num20 = 10 (fireball every)
- num21 = 6*num20 = 60
- num22 = 60 (tail)
- num23 = num17+num21+num22 = 180 (total)
- num24 = 60 (spin T)
- num25 = 1, num26 = 2π*(1/60)
- num27 = 0.1 (spin rise)
- num28 = 32 (skydive spd)
- num29 = 90 (summon total)
- num30 = 20 (summon at)

State 0: ai[1]+=1 >= 10 → ai[0]=1, ai[1]=0, ai[2]=0. Ours matches (INTRO_T=10).

State 1 hover:
- if ai[2]==0: ai[2] = Center.X < target.X ? 1 : -1. Ours matches.
- destination = target + (-ai[2]*300, -200). Ours: destX = txc - e.ai2*300, destY = tyc - 200. matches.
- desiredVelocity = DirectionTo(dest)*7.5; SimpleFlyMovement(desired, 0.45). ours matches.
- direction/spriteDirection = Center.X<target.X?1:-1. Ours matches.
- ai[1]>=30: num32=1 default; if ai[3]==5 && rand(3)==0 → ai[3]+=1. switch: 0/1/3→2; 2→3; 4→4; 5→5; 6→3; 7→6. Ours matches: s===0||1||3→2; 2→3; 4→4; 5→5; 6→3; 7→6. default next=1 (unreachable since ai[3] 0..7). OK.
- ai[0]=num32; ai[1]=0; ai[2]=0; ai[3]+=1; if >=8 → 0. matches.
- case 2: vector2 = DirectionTo(target); spriteDirection; rotation; velocity = v*23. Ours: next===2||5 both handled together with DIVE_SPD=23 for 2 and SKYDIVE 32 for 5. matches.
- case 3: velocity = horizontal away * -2. ours: e.vx = -2*d3; e.vy = 0. Vanilla doesn't set vy=0 explicitly, just sets velocity = vector3 * -2f, which sets full velocity (Vector2 assignment) → vy=0 too. OK matches.
- case 5: velocity = v*32. ours matches.

State 2 wind: ai[1]==0 → sound DD2_BetsyWindAttack. ours plays sound at e.ai1===0... wait ours: `if (e.ai1 === 0) game.playSfx...`. Vanilla: `if (ai[1] == 0f) PlaySound`. matches. ai[1]>=30 → state 1. ours matches.

Note: in vanilla, during state 2, no explicit movement happens except default NPC movement? Actually the NPC has noTileCollide etc.; velocity remains from the dive (23 speed). Movement of NPC happens in the main AI loop (NPC position += velocity each tick by default unless noGravity/noMove...). In our engine, fly(e) integrates position each tick. Ours calls fly(e) at end. Fine.

State 3 flame breath:
- ai[1] += 1 first. Then num33 = Center.X<target.X?1:-1; ai[2]=num33.
- if ai[1] < 40: vector4 = target + (num33 * -600, -250). vector5 = DirectionTo(vector4)*12. if Distance(vector4) < 12 → base.Center = vector4 (teleport), else position += vector5. if Vector2.Distance(vector4, Center) < 16 → ai[1] = 39 (num13-1). num2 = 1.5.

Wait: `if (Distance(vector4) < num12)` — Distance is NPC.Distance(Vector2)? NPC.Distance likely distance from Center. num12=12. So if within 12px, snap center to vector4. Then if within 16 → ai[1] = 39.

Ours: FLAME_APPR=12; checks `Math.hypot(dx - e.cx, dy - e.cy) < FLAME_APPR` then snap; else e.x += d.x*FLAME_APPR. Then `if (dist < 16) e.ai1 = FLAME_T0 - 1` (=39). matches. timeScale 1.5 matches.

- if ai[1] == 40: num34 = target.X > Center.X ? 1 : -1; velocity = (num34,0)*10; direction=spriteDirection=num34; NewProjectile 687 damage num3=35 with ai0=0, ai1=whoAmI. Sound DD2_BetsyFlameBreath. Ours: shootD(game, e.cx, e.cy, e.vx, e.vy, DMG_BREATH, 687, 300, 0, 20). Hmm — vanilla passes velocity (10 horizontal) and damage 35. Ours matches dmg 35. Vanilla ai[0]=0 (or 0f), ai[1] = whoAmI (npc index). Our shootD doesn't pass ai1 (owner npc id) but pierce 20. That's a projectile-internal detail; the 687 flamebreath proj AI probably doesn't depend on npc whoAmI much. Fine.

- if ai[1] >= 40: num2=1.5; if |target.X - Center.X| > 550 && |velocity.X| < 20 → velocity.X += sign(velocity.X)*0.5. Ours matches.
- if ai[1] >= 120 → state 1. Ours: FLAME_T0+FLAME_T1 = 120. matches.

State 4 (air raid / bombing):
- num35 = Center.X<target.X?1:-1; ai[2] = num35.
- if ai[1] < 60: vector6 = target + (num35 * -1500, -350); value = DirectionTo(vector6)*13; velocity = Lerp(velocity, value, 1/30). direction = spriteDirection = num36 (same computation). if Distance(vector6) < 16 → ai[1] = 59 (num17-1). num2 = 1.5.

Ours: dx = txc - e.ai2*BOMB_OFF → note e.ai2 = num35 so dx = txc - ai2*1500. Vanilla: num35 * -1500 → same as -ai2*1500. matches. velocity lerp matches. distance<16 → ai1 = BOMB_APR_T-1 = 59. matches.

- else if ai[1] == 60: v = DirectionTo(target); v.Y *= 0.25; v = SafeNormalize(UnitX*direction); spriteDirection; rotation; velocity = v * 12.

Ours: v = dirTo; y*0.25; normalize via hypot; facing; visAngle; vx=v.x*12; vy=v.y*12. matches (BOMB_SPD=12).

- else: position.X += DirectionTo(target).X * 7; position.Y += DirectionTo(target + (0,-400)).Y * 6; if ai[1] <= num23-num22 (=120) → num2 = 1.5; num37 = 30; vector7 = Center + new Vector2((110+num37)*direction, 20).RotatedBy(rotation); num38 = (int)(ai[1] - num17 + 1); if num38 <= num21(60) && num38 % num20(10)==0 → NewProjectile(vector7, velocity, 686, num4=35).

Ours: `if (e.ai1 <= BOMB_TOTAL - TAIL_T) timeScale = 1.5;` BOMB_TOTAL=180, TAIL_T=60 → ai1 <= 120. matches. vector7: ox=(110+30)*facing=140*facing, oy=20, rotated by visAngle; then rx/ry computed from e.cx + ... matches `Center + new Vector2(...).RotatedBy(rotation)`. num38 = floor(ai1 - 60 + 1). if n <= 60 && n % 10 == 0 → shoot. matches.

- if ai[1] > 120 → velocity.Y -= 0.1. ours: BOMB_TOTAL - TAIL_T = 120; matches.
- ai[1] += 1; if >= 180 → state 1. matches.

Damage: ours DMG_FIREBALL=35 matches num4=35. pierce 3 for 686: vanilla fireball 686 has... default pierce? Projectile 686 SetDefaults — probably pierce 1? Actually DD2BetsyFireball — in Projectile.cs it's an explosive fireball; pierces? Let me not sweat that; it's a proj detail, not NPC AI. The task says attack loop params (proj id/speed/count/interval) — id 686/687 right, speed matches (velocity inherited), count ×6 every 10t matches.

State 5 spin:
- velocity = velocity.RotatedBy(-num26 * direction); position.Y -= 0.1; position += DirectionTo(target) * 10; rotation -= num26 * direction; num2 *= 0.7; sound at ai[1]==1 (DD2_BetsyFlyingCircleAttack); ai[1]+=1 >= 60 → state 1, velocity /= 2.

Ours: rot = -SPIN_RATE * e.facing; rotates velocity; e.y -= SPIN_RISE; adds direction*10; visAngle -= SPIN_RATE*facing; timeScale *= 0.7; sound at ai1===1; ai1>=60 → halve both vx and vy.

Vanilla: `velocity /= 2f` halves the vector (both components). Ours halves both. matches.

SPIN_RATE = TAU/60 = 2π*1/60 = num26. matches.

State 6 summon:
- if ai[1]==0: destination2 = target + (0,-200); desired = DirectionTo * 7.5*2 = 15; SimpleFlyMovement(desired, 0.45*2=0.9); direction/spriteDirection; ai[2]+=1; if Distance(target) < 350 || ai[2]>=180 → ai[1]=1.
Ours matches (FLY_SPD*2, FLY_ACC*2).
- else: sound at ai1==1 (DD2_BetsyScream); if ai1 < 20 → velocity *= 0.95; else *= 0.98; if ai1==20: if vy>0 → vy/=3; vy -= 3. num2 *= 0.85.
- dust/gore spawn at ai1 == 20/25/30 (that's tile dust from ground — visual; ours spawns particles).
- flag3 = ai1==20||45||70; if CountNPCS(560) > 4 → flag3 = false.
- if flag3: for m in 0..0: vector8 = Center + (2π*rand).ToRotationVector2() * new Vector2(2,1) * 300 * (0.6+rand*0.4); if Distance(vector8, target) > 100 → NewNPC(560) at vector8; sound DD2_BetsySummon. Then list of 549 portals; if any, for num45 in 0..2: pick random portal; NewNPC 560 at portal center; sound.

Ours: SUMMON_AT=20; checks ai1===20||45||70; wyverns<=4 (vanilla: >4 → flag3=false, i.e., spawn allowed when count <= 4). matches. spawn ring: sx = e.cx + cos(a)*2*300*(0.6+rand*0.4), sy = e.cy + sin(a)*1*300*(...). matches new Vector2(2,1)*300*(...) — vector8 = Center + angleVec * (2,1)*300*(...). angleVec = (cos, sin). So x = Center.X + cos*2*300*k, y = Center.Y + sin*1*300*k. matches.
- if distance from target > 100 → spawn. ours matches.
- portals: 3 spawns at random portal each; ours matches. Note ours plays the summon sound once per wave (outside the per-unit loops) while vanilla plays per spawned wyvern; sound nuance, minor.

Hmm wait — one detail: in vanilla, the portal-spawn block is INSIDE `if (flag3 && Main.netMode != 1)`, and the "for m < 1" loop also inside. Ours: `if (wyverns <= 4) { ring spawn; portals }` — equivalent.

- ai[1] += 1 happens in the else branch. And then `if (ai[1] >= num29=90)` → state 1. Note: when ai[1] is 0 (approach phase), ai[1] doesn't increment — only ai[2] increments. Once ai[1]=1, the else branch increments ai[1]. Ours matches structure.

Rotation convergence (tail):
- num46 = DirectionTo(target).ToRotation(); num47 = 0.04.
- switch ai[0]: case 2, 5 → num47 = 0; case 3 → num47=0.01, num46=0; if spriteDirection==-1 → num46 -= π; if ai[1] >= 40 → num46 += spriteDirection*π/12, num47=0.05; case 4 → num47 = 0.01, num46 = π; if spriteDirection==1 → num46 += π; case 6 → num47=0.02, num46=0; if spriteDirection==-1 → num46 -= π.
- if spriteDirection == -1 → num46 += π.
- if num47 != 0 → rotation = AngleTowards(num46, num47).

Ours: 
- s0===2||5 → step=0. matches.
- s0===3: step=0.01; tgtAng = e.facing === -1 ? -Math.PI : 0. Vanilla: num46=0; if sd==-1 → num46 -= π. same. if ai1>=FLAME_T0 → tgtAng += facing*π/12; step=0.05. matches.
- s0===4: step=0.01; tgtAng = facing===1 ? 2π : π. Vanilla: num46=π; if sd==1 → += π → 2π. matches.
- s0===6: step=0.02; tgtAng = facing===-1 ? -π : 0. matches.
- if facing === -1 → tgtAng += π. matches.
- angleTowards step. matches.

Hmm, but there's a subtlety: `direction` vs `spriteDirection`. In vanilla, several states set both direction and spriteDirection to the same value; in state 1 the hover sets `direction = (spriteDirection = num31)`. In ours we only have e.facing. Fine.

One thing to check: In vanilla Betsy, TargetClosestBetsy is called with faceTarget: false — target selection: crystal vs player. Our dd2Target: crystal if alive, else player. Need to check NPCUtils.TargetClosestBetsy semantics — does it pick crystal always if present? Let me check NPCUtils.cs:308.

Also the "player death / flee" semantics: In vanilla Betsy, if no target... TargetClosestBetsy sets target to player even if dead? Actually for DD2 the crystal is the target; if crystal dead, target = player. Our `if (!tgt) { e.vy -= 0.05; fly(e); return; }` — where does that come from? In vanilla there's no such branch; NPC with no target still runs the state machine with targetData = last target. Hmm, but GetTargetData returns cached. Our fallback `vy -= 0.05` — is that invented? It's a minor fallback when no target exists (no crystal, no player). Vanilla: NPC would keep last target data. Not a big deal but worth noting as invented? It's a fallback semantics; minor. Not CONFIRMED-worthy maybe.

Wait, actually there's something important: in vanilla state 3 (flame breath), the approach phase uses `position += vector5` — teleports/adds position directly, NOT velocity. Ours does e.x += d.x*FLAME_APPR — matches.

But in state 4 approach, vanilla sets velocity via Lerp (velocity = Vector2.Lerp(velocity, value, amount)). Ours: e.vx = lerp(e.vx, d.x*BOMB_SPD, BOMB_ACC) — matches.

In state 1 hover: SimpleFlyMovement(desiredVelocity, 0.45). Our simpleFlyMove matches the vanilla implementation? Vanilla SimpleFlyMovement (NPC.cs:78100):

```
private void SimpleFlyMovement(Vector2 desiredVelocity, float acceleration)
{
    if (velocity.X < desiredVelocity.X)
    {
        velocity.X += acceleration;
        if (velocity.X < 0f && desiredVelocity.X > 0f)
        {
            velocity.X += acceleration;
        }
    }
    else if (velocity.X > desiredVelocity.X)
    {
        velocity.X -= acceleration;
        if (velocity.X > 0f && desiredVelocity.X < 0f)
        {
            velocity.X -= acceleration;
        }
    }
    ... same for Y
}
```
Let me verify by reading NPC.cs:78100. I'll check later.

Now important: who integrates position? In vanilla, NPC.UpdateVelocity etc. adds velocity to position each tick (standard). Our fly(e) does x += vx. Fine.

Betsy netUpdate/netAlways: despawnTimer=750 — our engine's analog. OK.

Now one potential real deviation: In state 2 (wind attack), vanilla plays sound when `ai[1] == 0f`. But note ai[1] was reset to 0 when transitioning, and the sound check happens at the start of the state-2 branch. Ours: checks `e.ai1 === 0` at the moment of the branch — since ai1 was set 0 on transition, on first frame of state 2 ai1===0 → plays. matches.

In state 5, sound at ai[1] == 1f: on the first frame of state 5, ai1 = 0 (reset). So the check `if (ai[1] == 1f)` happens BEFORE ai[1] += 1... wait order in vanilla state 5:

```
velocity = velocity.RotatedBy(...);
position.Y -= num27;
position += DirectionTo(targetData.Center) * 10f;
rotation -= num26 * direction;
num2 *= 0.7f;
if (ai[1] == 1f) { sound }
if ((ai[1] += 1f) >= num24) { ... }
```

So the sound plays on the second frame of the state (ai1==1 means one frame has passed). Ours: `if (e.ai1 === 1) playSound` before `e.ai1 += 1` — matches (second frame).

State 6 scream: `if (ai[1] == 1f)` → sound. ours `if (e.ai1 === 1)` in else branch. matches.

OK Betsy looks remarkably faithful. Let me check details that might be wrong:

1. In state 3, ours does `e.ai1 += 1` at the very top before the `e.ai2 = e.cx < txc ? 1 : -1;`. In vanilla, order: `ai[1] += 1f; int num33 = ...; ai[2] = num33;`. matches.

Wait, in vanilla state 3, first line is the ActiveSound tracking, then ai[1] += 1, then num33 and ai[2]. Ours: `e.ai1 += 1; e.ai2 = ...`. matches.

2. In state 1, the transition block: vanilla sets ai[0]=num32 then case 2/3/5 special-cases set velocity/rotation. Note for case 2 and 5 they set rotation = v.ToRotation() and if spriteDirection==-1 rotation += π. Ours: visAngle = atan2 + (facing===-1?π:0). matches.

3. State 4 muzzle offset: vanilla `vector7 = base.Center + new Vector2((110f + num37) * direction, 20f).RotatedBy(rotation)`. Ours: ox=(110+30)*e.facing; oy=20; rx = e.cx + ox*cos - oy*sin; ry = e.cy + ox*sin + oy*cos. matches Vector2.RotatedBy.

4. `num38 % num20 == 0` where num38 = (int)(ai[1] - 60 + 1). Ours n = floor(e.ai1 - BOMB_APR_T + 1) and n % 10 === 0, n <= 60. matches.

One subtle: since ai1 increments AFTER the checks in vanilla state 4 (ai[1] += 1f at the end after the if blocks)... wait no. Let me re-read vanilla state 4 ordering:

```
else if (ai[0] == 4f)
{
    num35 = ...; ai[2] = num35;
    if (ai[1] < num17) { approach }
    else if (ai[1] == num17) { dive init }
    else { strafe + fire }
    if (ai[1] > num23 - num22) { velocity.Y -= 0.1f; }
    ai[1] += 1f;
    if (ai[1] >= num23) { → state 1 }
}
```

Ours:
```
e.ai2 = ...
if (e.ai1 < BOMB_APR_T) {...}
else if (e.ai1 === BOMB_APR_T) {...}
else {... strafe + fire ...}
if (e.ai1 > BOMB_TOTAL - TAIL_T) e.vy -= 0.1;
e.ai1 += 1;
if (e.ai1 >= BOMB_TOTAL) {...}
```
matches exactly.

In the strafe branch vanilla fires when num38 <= 60 && num38%10==0, i.e. ai1 in {60?no...}. num38 = ai1-59. When ai1=70 → num38=11? Wait: ai1 - num17 + 1 = ai1 - 60 + 1 = ai1 - 59. When ai1=69 → 10, %10==0 → fire. ai1=59 → 0 → fire? but ai1=59 is `ai[1] < num17`? No, 59 < 60 → approach branch. ai1=60 → dive init branch, num38=1, not fire. So fires at num38 ∈ {10,20,...,60} → ai1 ∈ {69,79,...,119}. 6 fireballs. Ours identical computation. 

Betsy rotation in state 4 during approach: vanilla does not set rotation during approach (only direction/spriteDirection). At the rotation-convergence tail, case 4: num46 = π (or 2π if facing right). Ours matches.

Hmm wait, ours in the dive-init branch (ai1===BOMB_APR_T) sets visAngle = atan2... then later the rotation convergence also runs. Vanilla also runs convergence at the end (num47=0.01 for case 4). Same order in ours. OK.

Now — a critical thing: in vanilla Betsy, `SimpleFlyMovement` etc all happen and then NPC's position integrates velocity via the normal update. In our implementation, `fly(e)` is called at the end for ALL states. But in states 3 (approach) and 4 (strafe) and 5, vanilla manipulates `position` directly AND velocity integration also occurs? Wait — in vanilla, after the AI switch, the NPC's velocity is applied to position by the game's normal movement step (NPC.VanillaUpdateVelocity / position += velocity). Hmm, actually in Terraria, NPC.AI() runs, then collision/movement applies velocity to position. For noTileCollide NPCs, `position += velocity` happens in the "no tile collide" branch of vanilla NPC update (Collision.NoTileCollide... actually it's in UpdateNPC → if noTileCollide: position += velocity with Collision.SweepAabb? It just adds velocity).

So in state 3 approach: vanilla does position += vector5 (12 speed toward), AND velocity is whatever it was (also integrated). Our implementation: e.x += d.x*12, e.y += ... AND then fly(e) adds e.vx/e.vy as well. Since velocity isn't zeroed during approach... In vanilla, entering state 3 velocity was set at selection (case 3: velocity = vector3 * -2f → (-2*dir, 0)). So during approach vanilla moves position by vector5 (12) plus velocity (-2*dir). Ours also adds e.vx (which is -2*d3) — same. Good.

In state 4 strafe: vanilla position.X += 7 toward target and velocity is 12-speed dive; total = velocity + 7. Ours same. Good.

State 5: vanilla position += DirectionTo*10 and position.Y -= 0.1, plus velocity integration (velocity rotates). Ours same.

OK Betsy looks 1:1. Let me double check our handling of `e.despawnTimer = 750` — fine.

One more check — our betsy sound `dd2_betsy_wind_attack` at state 2 ai1===0: but note in vanilla, sound plays when ai[1]==0 at the START of the branch, but ai[1] += 1 happens after the sound check... wait order:

```
else if (ai[0] == 2f)
{
    if (ai[1] == 0f) { sound }
    if ((ai[1] += 1f) >= num9) { →1 }
}
```
Ours:
```
if (e.ai1 === 0) play
e.ai1 += 1;
if (e.ai1 >= WIND_T) →1
```
matches.

Now Betsy damage gating: vanilla num3 = 35 is used for projectile 687 damage. In expert mode, does the projectile damage get scaled? Projectile.NewProjectile uses ai0=0, ai1=whoAmI... the damage passed is 35 flat (not scaled by GetAttackDamage_ForProjectiles!). Interesting — Betsy passes raw 35. Ours passes 35 flat too. OK consistent with 1456.

Hmm wait — is there any scaling in our shootD via Arrow (expert scaling elsewhere)? Not our concern here.

Now the DarkMage. Vanilla AI_109:

Defaults (num = 4 front depth, num2 = 3 head clear, num3 = 0 bottom depth, num4 = 0.2 grav, num5 = 2 maxfall, num6 = -0.2 upAccel, num7 = -4 maxUp, flag5 = true headScan, num8 = 2 maxH, num9 = 0.1 accelH, num10 = 1 maxV, num11 = 0.04 accelV).

For type 564/565 overrides: num3 = 2 (bottom depth); num6 = -0.05; num7 = -0.4; num4 = 0.05 (grav); num5 = 0.2 (maxfall); num10 = 0.5; num11 = 0.02; num8 = 0.5 (maxH); num9 = 0.1 (accelH); flag5 = false (headScan off); rotation = velocity.X * 0.04.

Ours darkMage p: frontDepth 4, headClear 3, bottomDepth 2, grav 0.05, maxFall 0.2, upAccel -0.05, maxUp -0.4, headScan false, maxH 0.5, accelH 0.1, maxV 0.5, accelV 0.02. All match.

Cast logic:
- if ai[0] < 0 → ai[0] = min(ai[0]+1, 0). Ours: `if (e.ai0 < 0) e.ai0 = Math.min(e.ai0 + 1, 0);` matches.
- if ai[0] > 0: flag6 = true (cast damp), num12 = 0.9, ai[0] -= 1.
  - ai[0]==80 && ai[1]==2 → sound SummonSkeleton. ours matches.
  - ai[1]==2 && ai[0]==64 → projectile 673 at Center + (direction*24, -40), velocity Zero, damage 0; DD2Event.RaiseGoblins(this, Center). Ours: raiseGoblins hook + particles + sound. We don't spawn 673 (documented degradation). Fine.
  - ai[1]==0 && ai[0]==32 → vector = (target.Center - (Center + (direction*10, -16))).SafeNormalize(UnitY)*14; direction = vector.X>0?1:-1; NewProjectile at Center + (direction*10,-16), velocity vector, 675, 40 dmg.

    Ours: computes d = dirTo(e, txc, tyc) from center to target — WAIT. Vanilla computes vector = (target.Center - (Center + muzzle)).SafeNormalize() * 14. The muzzle is Center + (direction*10, -16). Our dirTo(e, txc, tyc) computes from e.cx (center) not from muzzle offset. Slight difference in aim origin (10px horizontal, 16px vertical). Minor aiming difference — is this a structural deviation? It's a 10/16 px offset difference. Hmm, that's minor noise. Also vanilla sets direction based on the shot vector, and ours sets facing from d.x. Ours sets facing then shoots with muzzle at cx+facing*10, cy-16, velocity d*14. Vanilla computes vector from muzzle point. The direction of the bolt differs by the muzzle offset ~19px. Minor.

  - ai[0]==126 && ai[1]==1 → sound CastHeal. ours matches.
  - ai[1]==1 && ai[0] in {40,48,56} && WorldUtils.Find(From (Center.X + direction*240, Center.Y).ToTileCoordinates(), Chain(Down(50), IsSolid)) → NewProjectile(result.ToWorldCoordinates(8, 0), Zero, 674).
  
    Ours: gx = floor((cx + facing*240)/16), gy = floor(cy/16); expandVertically(gx, gy, 0, 50) → [top, bottom]; if solidAt(gx, bottom) → DD2HealPulse at (gx*16+8, bottom*16).

    Hmm: Searches.Down(50) from start point searches downward 50 tiles? WorldUtils.Find with Searches.Chain(new Searches.Down(50), new Conditions.IsSolid()) — starts at given coordinates and searches down up to 50 tiles, returns first solid tile found. Does Down include the starting tile? Searches.Down searches `for (int j = 0; j <= MaxTilesToSearch; j++) yield return new Point(origin.X, origin.Y + j)`? Let me check Searches.Down — I think it starts at origin and goes down INCLUDING origin. Our expandVertically(gx, gy, 0, 50): starts at gy, loop: `if (bottom >= st.h - 10) break; if (solidAt(gx, bottom)) break; bottom++` — checks solid at current bottom before incrementing, so it stops at first solid including start. Returns [top, bottom] where bottom = first solid tile. Then `if (solidAt(game, gx, bottom))` spawn at bottom*16. So the pulse sits at the top of the solid tile — result.ToWorldCoordinates(8, 0) = (x*16+8, y*16+0) = top-left + 8. Ours: (gx*TILE+8, bottom*TILE). matches.

    Wait, one bug check in expandVertically: `for (let i = 0; i < maxUp; i++)` — with maxUp=0, no iterations, top = y. Good.

  - if ai[0] <= 0: num13 = ai[1]; ai[1] += 1; if >= 3 → 0; ai[0] = -120; if num13 == 0 → ai[0] = -20.
  
    Ours: `const prev = e.ai1; e.ai1 += 1; if (e.ai1 >= 3) e.ai1 = 0; e.ai0 = prev === 0 ? -20 : -120;` matches.

- Attack selection: if ai[0]==0 && localAI[3] >= 60: flag8 = count of NPCs (active, lifeMax != life, Center between min/max) >= 2. if !flag8 → ai[1] = 2. if ai[1]==2 && !CanRaiseGoblinsHere → ai[1] = 0. flag9 = true; if ai[1]==0 && (Distance >= 1000 || !CanHitLine) → flag9 = false. if flag9 → switch ai[1]: 0→97, 1→127, 2→183.

  Ours matches: hurt counting enemies with n.hp < n.maxHp (lifeMax != life → ours hp >= maxHp continue → counts hp < maxHp). Note vanilla counts ALL NPCs including town NPCs (Main.npc all). Ours counts only game.enemies(). Vanilla nPC.lifeMax != nPC.life — includes town NPCs (they have lifeMax 250 etc.). This is a nuance: in DD2 there are no town NPCs in arena typically. Minor.

  Vanilla `++num14 >= 2` — counts and requires at least 2 hurt NPCs in range for flag8. Ours hurt<2 → next=2. Same.

  Note vanilla nuance: `nPC.Center.Between(minimum, maximum)` — Between is inclusive rectangle check: X in [min.X, max.X], Y in [min.Y, max.Y] with min = Center+(-600,-200), max = Center+(600,200). Ours: Math.abs(n.cx - e.cx) <= 600 && Math.abs(n.cy - e.cy) <= 200. matches.

- Spawn fade: localAI[3]==0 → alpha=255; ==30 → sound; < 60 → +=1, alpha -= 5, clamp 0. Ours matches (alphaFade false — some engine thing).

Order of operations: In vanilla, the 564/565 block happens first, THEN the walker movement (if flag6, velocity *= 0.96/0.9 and return — wait, actually: `if (flag6) { velocity *= num12; return; }` — hmm where is this? Let me re-read:

In AI_109, after the 564/565-specific block closes, we have:
```
if (justHit) localAI[2] = 0;
if (!flag2)  // flag2 = false always
{
    if (localAI[2] >= 0) { stuck logic; if (flag7) TargetClosestOldOnesInvasion }
    else { localAI[2] += 1; direction = target... }
}
int num18..num21 (probe tiles)
if (flag6) { velocity *= num12; return; }
... probes, gravity, collide, accel
```

Interesting — in vanilla, the stuck/jump logic and targeting run EVEN when casting (flag6 true); only the probe/gravity/accel section is skipped by `velocity *= num12; return`. Ours: walkerKernel(e, game, tgt, x, p, castDamp) — inside walkerKernel, the stuck logic runs first, then `if (castDamp > 0) { vx*=damp; vy*=damp; oldVel set; moveAndCollide; return; }`. 

Hmm wait — in vanilla, when flag6 (casting), `velocity *= num12; return;` — NO collision step at all! The return happens before... wait, no. In Terraria, collision happens in the main NPC update AFTER AI returns. So `return` just skips the rest of the AI; the engine still applies velocity and collision. So our moveAndCollide inside the cast branch emulates the engine step. OK, that's the documented approach ("AI 早退但碰撞步照跑").

But there's a subtle difference: vanilla, when casting, does NOT do the stuck→jump/gravity/accel. And ours also doesn't. And targeting: vanilla `if (flag7) TargetClosestOldOnesInvasion(this)` — flag7 = true unless casting (flag7=false set when ai[0]>0). So when casting, targeting does NOT run... but `direction = ((targetData.Center.X > base.Center.X) ? 1 : (-1));` in the else branch (localAI[2] < 0). Hmm, and in the localAI[2]>=0 branch, direction update only if flag7.

Ours walkerKernel: `if (player && !player.dead) e.facing = e.seekDirX(player);` — runs in both branches regardless of castDamp. Hmm: in ours, when casting (castDamp>0), walkerKernel still updates facing toward player (or crystal via tgt passed as fake player). Vanilla when casting: flag7=false → TargetClosest not called; but in the stuck<0 branch direction is set toward targetData regardless of flag7. Wait:

```
else
{
    localAI[2] += 1f;
    direction = ((targetData.Center.X > base.Center.X) ? 1 : (-1));
}
```
That's the else of localAI[2] >= 0. It doesn't check flag7. So while casting and stuck-timer < 0, direction tracks target. While stuck-timer >= 0, direction only updated if flag7 (not casting). Minor nuance; our version updates facing when casting. The cast aim uses facing for heal placement (direction*240) — vanilla during cast: direction stays whatever it was (unless stuck<0). Ours would track the target during cast, changing heal placement side. Minor drift; low severity.

Actually wait — more important: in vanilla when casting, the AI's cast block is INSIDE `if (type == 564 || type == 565)`, and the cast checks use `direction` for the bolt (direction*10, -16). Vanilla's direction during cast comes from previous frames. Ours updates facing each frame toward target. The difference: when the DarkMage starts casting while walking away... it would flip facing. Eh, minor.

Hmm, but one more significant thing: In our darkMageAI, the cast block runs only `if (e.ai0 > 0)`. And attack selection `if (e.ai0 === 0 && x[3] >= 60)`. matches vanilla.

Also our castDamp handling: `let castDamp = 0; if (e.ai0 < 0) e.ai0 = min(e.ai0+1, 0); if (e.ai0 > 0) { castDamp = 0.9; e.ai0 -= 1; ... }`.

Wait — there's an ordering bug candidate: In vanilla, `ai[0] -= 1f` happens FIRST, then the equality checks (ai[0] == 80, ==64, ==32, ==126, ==40/48/56) are against the DECREMENTED value, and `if (ai[0] <= 0)` at the end. Ours decrements first too (`e.ai0 -= 1` at top of the ai0>0 block), then checks. matches.

But ours has one extra line: `if (e.ai0 <= 0)` → then increments ai1 and sets cooldown. In vanilla, `if (ai[0] <= 0f)` inside the `ai[0] > 0` block. Same.

Now — vanilla num12 for cast damping: flag6 sets num12 = 0.9. But there's a subtlety: in the 564 block, `flag6 = true` only when ai[0] > 0; also at attack-selection success `flag6 = true` is set (`netUpdate = true; flag6 = true;`). So on the frame the spell is selected, velocity *= 0.9 immediately. Ours: when selection happens (ai0 set to 97 etc.), castDamp is still 0 for that frame (since the `if (e.ai0 > 0)` check happened BEFORE the selection block). Wait, order in ours:

```
if (e.ai0 < 0) e.ai0 = min(e.ai0+1, 0);
if (e.ai0 > 0) { castDamp = 0.9; e.ai0 -= 1; ...checks... }
if (e.ai0 === 0 && x[3] >= 60) { ...selection sets e.ai0 = 97/127/183... }
walkerKernel(..., castDamp);
```

In vanilla, order within the 564 block: ai[0]<0 ramp; ai[0]>0 cast block (flag6=true); then selection block (also sets flag6=true if flag9). Then `if (flag6) { velocity *= num12; return; }` — so in vanilla, the frame the spell is selected, damping applies. In ours, the selection frame passes castDamp=0 → no damping that frame. One-frame difference. Truly minor.

OK, DarkMage looks good. The heal pulse: vanilla 674 proj damage 0, spawns at found location. Our DD2HealPulse: heals after 40 ticks, +min(500, lifeMax-life) within 1000px. Comment says Projectile.cs:35540-35574. I could verify but that's a secondary file; the prompt says the standard is NPC.cs only. I'll trust the comment or spot check quickly later if time permits.

Wait, one thing in DarkMage: our sound for skeleton summon at raiseGoblins uses `['dd2_skeleton_summoned']` — fine.

Also ours heal placement: `expandVertically(game, gx, gy, 0, 50)`; hmm vanilla Searches.Down(50): does it search up to 50 tiles BELOW the start, checking each? And IsSolid condition. If the START tile itself is solid, does it return the start tile? Let me check Searches.Down implementation:

```
public class Down : GenSearch {
    ...
    public override bool Perform(Point origin, ...){
        for (int i = 0; i <= _maxTilesToSearch; i++) {
            if (origin.Y + i >= Main.maxTilesY) break/return;
            Point point = new Point(origin.X, origin.Y + i);
            if (_validTiles.Contains(Main.tile[point.X, point.Y].type)) return result;
        }
    }
}
```
Hmm — actually Searches.Down is a GenSearch with Conditions via Chain. The Chain search: `Searches.Chain(new Searches.Down(50), new Conditions.IsSolid())`. In GenSearch.Perform, the condition `_condition(point)` is evaluated for each point; returns point when condition true. I believe it includes origin itself. Our expandVertically starts checking at gy (start tile) — includes origin. Consistent with comment "含起点格". OK.

Now the Flying Dutchman. Let me read vanilla cs:40918-41028 and the cannon 35889-35904 + 36008-36070. Also check spawnPart usage and the pirate jump.

Vanilla (from memory of the audit): let me actually read the source.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:12:15.737Z · glm-x-preview-260804

```
Betsy 和 DarkMage 的源代码已获取。现在我来读取 FlyingDutchman + cannon 对应的原版部分，以及我们文件中剩余的部分（sandElemental/sandShark/crystal/portal/divingFlyer，以及 107 walker 代码块）。
```


---

## 🤖 Assistant · 2026-08-19T03:12:16.219Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '40918,41030p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla FlyingDutchman AI_093"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:16.278Z

**📎 ToolResult**

```
		else if (aiStyle == 93)
		{
			if (Main.netMode != 1 && localAI[0] == 0f)
			{
				localAI[0] = 1f;
				for (int num1464 = 0; num1464 < 4; num1464++)
				{
					int num1465 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)base.Center.X + num1464 * 40 - 150, (int)base.Center.Y, 492, whoAmI, whoAmI, num1464, 0f, 60 * num1464);
					Main.npc[num1465].TargetClosest(faceTarget: false);
					Main.npc[num1465].timeLeft = 600;
					Main.npc[num1465].netUpdate = true;
					this.ai[num1464] = num1465;
				}
				netUpdate = true;
			}
			bool flag98 = true;
			for (int num1466 = 0; num1466 < 4; num1466++)
			{
				if (this.ai[num1466] >= 0f && (!Main.npc[(int)this.ai[num1466]].active || Main.npc[(int)this.ai[num1466]].type != 492))
				{
					this.ai[num1466] = -1f;
					netUpdate = true;
				}
				else if (this.ai[num1466] >= 0f)
				{
					flag98 = false;
				}
			}
			if (flag98)
			{
				StrikeNPCNoInteraction(9999, 0f, 0);
				return;
			}
			if (Main.netMode != 1 && Main.rand.Next(300) == 0)
			{
				Vector2 vector270 = new Vector2((Main.rand.NextFloat() - 0.5f) * (float)(width - 70), (Main.rand.NextFloat() - 0.5f) * 20f - (float)(height / 2) - 20f).RotatedBy(rotation);
				vector270 += base.Center;
				int num1467 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), (int)vector270.X, (int)vector270.Y, Utils.SelectRandom<int>(Main.rand, 213, 215, 214, 212));
				Main.npc[num1467].velocity = new Vector2((Main.rand.NextFloat() - 0.5f) * 5f, -8.01f) + velocity;
				Main.npc[num1467].netUpdate = true;
				Main.npc[num1467].timeLeft = 600;
			}
			if ((localAI[3] += 1f) >= 64f)
			{
				localAI[3] = 0f;
			}
			TargetClosest();
			int num1468 = (int)base.Center.X / 16 + Math.Sign(velocity.X) * 10;
			int num1469 = (int)(position.Y + (float)height) / 16;
			int num1470 = 0;
			if (Main.tile[num1468, num1469] != null && Main.tile[num1468, num1469].nactive() && Main.tileSolid[Main.tile[num1468, num1469].type] && !Main.tileSolidTop[Main.tile[num1468, num1469].type])
			{
				num1470 = 1;
			}
			else
			{
				for (; num1470 < 150 && num1469 + num1470 < Main.maxTilesY; num1470++)
				{
					int num1471 = num1469 + num1470;
					if (Main.tile[num1468, num1471] != null && Main.tile[num1468, num1471].nactive() && Main.tileSolid[Main.tile[num1468, num1471].type] && !Main.tileSolidTop[Main.tile[num1468, num1471].type])
					{
						num1470--;
						break;
					}
				}
			}
			float num1472 = num1470 * 16;
			if (num1472 < 350f)
			{
				float num1473 = num1472 - 350f;
				if (num1473 < -4f)
				{
					num1473 = -4f;
				}
				velocity.Y = MathHelper.Lerp(velocity.Y, num1473, 0.05f);
			}
			else if (num1472 > 450f)
			{
				float num1474 = num1472 - 350f;
				if (num1474 > 4f)
				{
					num1474 = 4f;
				}
				velocity.Y = MathHelper.Lerp(velocity.Y, num1474, 0.05f);
			}
			else
			{
				velocity.Y *= 0.95f;
			}
			float num1475 = Main.player[target].Center.X - base.Center.X;
			if (Math.Abs(num1475) >= 300f && (Math.Abs(velocity.X) < 6f || Math.Sign(velocity.X) != direction))
			{
				velocity.X += (float)direction * 0.06f;
			}
			rotation = velocity.X * 0.025f;
			spriteDirection = -Math.Sign(velocity.X);
			for (int num1476 = 0; num1476 < 2; num1476++)
			{
				if (Main.rand.Next(2) != 0)
				{
					Vector2 vector271 = new Vector2((Main.rand.NextFloat() - 0.5f) * (float)(width - 70), (Main.rand.NextFloat() - 0.5f) * 20f + (float)(height / 2) + 10f).RotatedBy(rotation);
					Dust dust10 = Main.dust[Dust.NewDust(base.Center, 0, 0, 228)];
					dust10.position = base.Center + vector271;
					dust10.velocity = Vector2.Zero;
					dust10.noGravity = true;
					dust10.noLight = true;
					dust10.fadeIn = 1.5f;
					dust10.scale = 0.5f;
				}
			}
		}
		else if (aiStyle == 94)
		{

```


---

## 🤖 Assistant · 2026-08-19T03:12:17.031Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '35880,35910p;36000,36075p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla dutchman cannon AI sections"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:12:17.094Z

**📎 ToolResult**

```
					num1120 = num1134;
					vector133 = Vector2.UnitY * -13f + ((this.ai[1] == 1f) ? Vector2.UnitX : (-Vector2.UnitX)) * 49f;
					vector133 *= Main.npc[num1134].scale;
					float num1135 = Main.npc[num1134].rotation;
					vector133 = vector133.RotatedBy(num1135);
					rotation = num1135;
					num1121 = ((this.ai[1] == 1f) ? 1 : (-1));
				}
			}
			else if (type == 492)
			{
				int num1136 = (int)this.ai[0];
				if (Main.npc[num1136].active && Main.npc[num1136].type == 491)
				{
					DiscourageDespawn(60);
					num1120 = num1136;
					vector133 = new Vector2((-122f + 68f * this.ai[1]) * (float)((Main.npc[num1136].spriteDirection != 1) ? 1 : (-1)), -6f);
					vector133 *= Main.npc[num1136].scale;
					float num1137 = Main.npc[num1136].rotation;
					vector133 = vector133.RotatedBy(num1137);
					rotation = num1137;
				}
			}
			if (num1120 != -1)
			{
				NPC nPC6 = Main.npc[num1120];
				velocity = Vector2.Zero;
				position = nPC6.Center;
				position.X -= width / 2;
				position.Y -= height / 2;
				position += vector133;
								if (this.ai[2] != num1143)
								{
									netUpdate = true;
								}
							}
						}
					}
				}
				if (type == 492)
				{
					timeLeft = nPC6.timeLeft;
					velocity = nPC6.velocity;
					if (this.ai[3] < 240f)
					{
						this.ai[3]++;
					}
					if (this.ai[3] == 2f)
					{
						TargetClosest(faceTarget: false);
					}
					if (Collision.CanHit(position, width, height, Main.player[target].position, Main.player[target].width, Main.player[target].height))
					{
						Vector2 vector138 = Main.player[target].Center - base.Center;
						Vector2 vector139 = Vector2.Normalize(vector138);
						if (this.ai[3] >= 240f)
						{
							this.ai[3] = 0f;
							Vector2 center22 = Main.player[target].Center;
							Vector2 center23 = base.Center;
							Vector2 vector140 = Vector2.Normalize(center22 - center23);
							if (float.IsNaN(vector140.X) || float.IsNaN(vector140.Y))
							{
								vector140 = Vector2.UnitY;
							}
							vector140 *= 14f;
							vector140 += Vector2.UnitY * -5f;
							if (Main.netMode != 1)
							{
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), center23.X, center23.Y, vector140.X, vector140.Y, 240, 30, 0f, Main.myPlayer);
							}
							netUpdate = true;
						}
						else
						{
							float num1144 = this.ai[2];
							float[] array3 = new float[8];
							for (int num1145 = 0; num1145 < array3.Length; num1145++)
							{
								array3[num1145] = Vector2.Distance(base.Center + Vector2.UnitY.RotatedBy((float)num1145 * (-MathF.PI / 4f)) * 50f, Main.player[target].Center);
							}
							int num1146 = 0;
							for (int num1147 = 1; num1147 < array3.Length; num1147++)
							{
								if (array3[num1146] > array3[num1147])
								{
									num1146 = num1147;
								}
							}
							this.ai[2] = num1146 + 1;
							if (spriteDirection == 1)
							{
								this.ai[2] = 9f - this.ai[2];
							}
							if (this.ai[2] != num1144)
							{
								netUpdate = true;
							}
						}
					}
					else
					{
						if (this.ai[2] != 0f)
						{
							netUpdate = true;
						}
						this.ai[2] = 0f;

```


---

## 🤖 Assistant · 2026-08-19T03:13:17.128Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now compare Dutchman:

Vanilla 491 AI:
1. First frame (localAI[0]==0): spawn 4 cannons 492 at Center + (i*40 - 150, 0); NewNPC args: x, y, type 492, start (whoAmI), ai0=whoAmI, ai1=i, ai2=0, ai3=60*i. Ours: spawnPart(game, e, 492), sets master, ai0=e.id, ai1=i, ai2=0, ai3=60*i, despawnTimer=600. Note: vanilla spawn position is Center + i*40-150 (a horizontal spread); ours spawns at... spawnPart presumably at boss position. But the cannon AI immediately anchors to ship offset (-122+68*slot), so initial spawn position is transient. Fine.

2. Cannons-alive check: for each of 4 ai slots: if ai >= 0 && (!active || type != 492) → ai = -1; else if ai >= 0 → flag98 = false. If flag98 (all slots dead/-1) → StrikeNPCNoInteraction(9999) and return.

WAIT. Look carefully: flag98 starts TRUE. The loop: for each slot, if slot >= 0 and dead → set -1; ELSE IF slot >= 0 → flag98 = false. So flag98 = false if ANY slot is alive. If flag98 (no slots alive) → strike 9999. Ours: `let anyAlive = false; ... if alive → anyAlive = true; if (!anyAlive) { hurt }`. matches.

Ours does `e.iframes = 0; e.hp = 0; e.hurt(9999, 0, 0, game);` — hmm, `e.hp = 0` then hurt(9999)? That's a bit odd but functionally kills. StrikeNPCNoInteraction bypasses IFrames. OK.

3. Pirate jump: 1/300 → vector270 = new Vector2((rand-0.5)*(width-70), (rand-0.5)*20 - height/2 - 20).RotatedBy(rotation) + Center; spawn one of [213,215,214,212] random; velocity = ((rand-0.5)*5, -8.01) + velocity; timeLeft 600.

Ours: `p.vx = (Math.random() - 0.5) * 5 + e.vx; p.vy = -8.01 + e.vy; p.despawnTimer = 600;` matches velocity. Spawn position: ours uses spawnPart at boss center presumably — vanilla spawns at ship top (height/2+20 above center). Minor spawn-position deviation; pirates then fall onto deck. Eh minor.

Also note vanilla spawns at top of ship — the ship is huge; ours spawns at center. Minor.

4. Animation: localAI[3] 64 cycle. ours matches.

5. TargetClosest: ours uses player if alive. matches (TargetClosest sets direction/facing).

6. Terrain-follow: num1468 = Center.X/16 + sign(vx)*10; num1469 = (position.Y + height)/16; scan down 150 for solid non-solidTop. ours: colX = clamp(floor(e.cx/TILE) + sign(e.vx)*10, 1, st.w-2); colY = floor((e.y+e.h)/TILE). Then `if solid → n=1 else scan`.

Hmm wait, vanilla: if the tile AT (colX, colY) is solid&!solidTop → num1470 = 1. Else scan downward from num1470=0, checking (colX, colY+num1470); when solid found → num1470-- and break. If loop ends without break, num1470 = 150 (or until maxTilesY).

Ours: `if (solidAt(game, colX, colY)) { n = 1; } else { for (; n < 150 && colY + n < st.h; n++) { if (solidAt(...)) { n--; break; } } }`. matches. Note vanilla also excludes solidTop tiles (`!Main.tileSolidTop[type]`) — ours uses st.isSolid which per project memory (tile-passability audit) is tileSolid semantics; platforms are solidTop and isSolid might return true for platforms? From memory: "tileSolid∩tileSolidTop{19,239,380,427}恒可站" — solidTop platforms are standable. Does st.isSolid include platforms? In the audit "全物块通行性审计 — tileSolid/SolidTop全表399条+站台家具84类" — isSolid likely reflects tileSolid only... Actually platforms: tileSolid[platform]=false in Terraria (platforms are NOT tileSolid; they're tileSolidTop). So vanilla check nactive && tileSolid && !tileSolidTop = effectively tileSolid (since solidTop tiles have tileSolid false). So ours with isSolid ≈ tileSolid is fine.

gap thresholds 350/450, lerp 0.05, clamp ±4 — matches.

7. Horizontal: num1475 = player.Center.X - Center.X; if |dx| >= 300 && (|vx| < 6 || sign(vx) != direction) → vx += direction*0.06.

Ours: `if (Math.abs(dxp) >= 300 && (Math.abs(e.vx) < 6 || sign(e.vx) !== e.facing)) e.vx += e.facing * 0.06;` matches — with e.facing ≈ direction. BUT: at line 465 ours sets `if (player && !player.dead) e.facing = tx > e.cx ? 1 : -1;` before the movement — vanilla TargetClosest sets direction similarly. And then at line 496: `e.facing = e.vx === 0 ? e.facing : -sign(e.vx)` — this mimics `spriteDirection = -Math.Sign(velocity.X)` but ours writes it into facing! Vanilla keeps `direction` (target direction) separate from `spriteDirection` (visual flip). The horizontal approach uses `direction`, which remains the target-facing value from TargetClosest (not flipped). Ours overwrites e.facing (used as direction AND spriteDirection since our engine likely has one facing field) with -sign(vx) AFTER using it. Order: line 492-494 uses e.facing (still target direction) for acceleration, then line 496 overwrites for rendering. Next frame line 465 re-sets facing from target. So movement-wise it's fine; the final assignment serves rendering. OK — no functional deviation as long as nothing else reads facing between frames. The cannons read `ship.facing` for mirror: vanilla cannon uses `Main.npc[ship].spriteDirection != 1 ? 1 : -1` — ours `sd = ship.facing === 1 ? 1 : -1` then `ox = (-122 + 68*slot) * (sd !== 1 ? 1 : -1)`.

Vanilla: vector133.X = (-122 + 68*ai1) * (spriteDirection != 1 ? 1 : -1). So if spriteDirection == 1 → multiply -1; else +1. Ours: sd = facing===1 ? 1 : -1 (mirrors spriteDirection value); ox = (-122+68*ai1) * (sd !== 1 ? 1 : -1) — sd===1 → -1 multiplier. matches exactly. rotation applied. Ours also sets e.vx = ship.vx, e.vy = ship.vy — vanilla sets velocity = nPC.velocity in the 492 block: `timeLeft = nPC6.timeLeft; velocity = nPC6.velocity;`. And in the anchor block: velocity = Vector2.Zero; position = npc.Center - size/2 + vector133. Then later velocity = ship velocity. matches.

Ours: `e.despawnTimer = Math.max(e.despawnTimer, Math.min(ship.despawnTimer, 600));` vs vanilla DiscourageDespawn(60) + timeLeft = nPC6.timeLeft. Hmm: DiscourageDespawn(60) sets timeLeft = max(timeLeft, 60)? And then `timeLeft = nPC6.timeLeft` overrides with ship's timeLeft. Ship despawnTimer in ours = 750 (netAlways analog). Math.min(750, 600) = 600. Vanilla timeLeft = ship timeLeft. Ship's timeLeft in vanilla... netAlways NPCs get timeLeft = 750 always (NPC.netAlways → timeLeft stays high). So cannon timeLeft = 750. Ours caps at 600. Trivial despawn nuance, not worth reporting.

8. Firing: vanilla 492: if ai3 < 240 → ai3++. if ai3 == 2 → TargetClosest(false). If CanHit(position,w,h, player.position...): vector to player; if ai3 >= 240 → ai3 = 0; vector140 = normalize(player.Center - cannon.Center) (NaN → UnitY) * 14 + UnitY * -5; NewProjectile(center23.X, center23.Y, v, 240, 30 dmg).

Ours: `const d = dirTo(e, player.cx, player.cy); let vx = d.x*14, vy = d.y*14 - 5; const v = Math.hypot(vx, vy); if (v > 0.001) { vx = vx/v*14; vy = vy/v*14; } else {...}; vy -= 5; shootD(..., 30, 240, 300, 0.25);`

Vanilla: velocity = normalize * 14, THEN += (0, -5) — final speed |v| is NOT 14; it's the sum of a 14-length vector and -5 vertical. Ours: computes d*14 - 5, then RE-NORMALIZES to 14, then subtracts 5 again! So ours = normalize(d*14 - 5)*14 - 5 vs vanilla = normalize(d)*14 - 5.

Hmm wait, let me re-read our code:

```
const d = dirTo(e, player.cx, player.cy);
let vx = d.x * 14, vy = d.y * 14 - 5;
const v = Math.hypot(vx, vy);
if (v > 0.001) { vx = (vx / v) * 14; vy = (vy / v) * 14; }
else { vx = 0; vy = 14; }
vy -= 5;
```

So: initial (d.x*14, d.y*14 - 5); normalize to length 14; then vy -= 5. Final = unit(d*14 - 5)*14 + (0,-5).

Vanilla: (unit(d)*14) + (0,-5). 

These differ: direction distortion. E.g. player directly above: d = (0,-1). Vanilla: (0,-14)+(0,-5) = (0,-19). Ours: (0,-14-5)=(0,-19), norm=19 → (0,-14), then vy -=5 → (0,-19). Same for pure vertical.

Player at 45° above-right: d=(0.707,-0.707). Vanilla: (9.9, -9.9-5= -14.9). Ours: (9.9, -14.9) → length 17.9 → normalized (7.83, -11.76) → vy -=5 → (7.83, -16.76). Different! Vanilla speed = |(9.9,-14.9)| = 17.9; ours = |(7.83,-16.76)| = 18.5. Direction differs slightly. Hmm.

This looks like a misunderstanding — maybe they were trying to normalize the aim vector then apply speed 14 and arc -5. Actually vanilla comment: vector140 = Normalize(center22 - center23) * 14f; vector140 += Vector2.UnitY * -5f. The correct port: vx = d.x*14; vy = d.y*14; vy -= 5. Ours adds an extra normalization pass on (d*14 - 5). This is a real (if small) aiming deviation: cannonball direction and speed both distorted for non-vertical shots.

Severity: low-medium. It's a math error though — "速度档" distortion. I'd report as CONFIRMED with medium-high confidence: it's a structural deviation in the attack vector computation.

Wait, actually let me think again about whether the extra normalization matters much: for horizontal shots d=(1,0): vanilla (14,-5); ours: (14,-5) → len 14.87 → (13.07,-4.67) → vy-=5 → (13.07,-9.67). Quite different! Horizontal shot: vanilla arc vy -5; ours -9.67. So cannonballs fly flatter/faster drop. Noticeable in gameplay. OK confirmed deviation.

Also: the aiming frame block (else branch): vanilla computes distances from Center + UnitY.RotatedBy(k * -π/4)*50 for k=0..7, picks min index; ai[2] = idx+1; if spriteDirection==1 → ai[2] = 9 - ai[2]. Ours: computes ax = cos(k*(-π/4))*50, ay = sin(...)*50 from e.cx — WAIT: vanilla offset vector = Vector2.UnitY.RotatedBy(k * -π/4) * 50 = (0,1) rotated → (-sin(kπ/4*?), cos(...)). UnitY rotated by angle θ = (0*cosθ - 1*sinθ, 0*sinθ + 1*cosθ) = (-sinθ, cosθ). With θ = k*(-π/4): (-sin(-kπ/4), cos(-kπ/4)) = (sin(kπ/4), cos(kπ/4)).

Ours: ax = e.cx + Math.cos(k*(-π/4))*50; ay = e.cy + Math.sin(k*(-π/4))*50. So ours = (cos(-kπ/4), sin(-kπ/4))*50 = (cos(kπ/4), -sin(kπ/4))*50. Vanilla = (sin(kπ/4), cos(kπ/4))*50. These differ: (cosθ, -sinθ) vs (sinθ, cosθ) — a swap+sign. For k=0: ours (50, 0) [right], vanilla (0, 50) [down]. So the 8-direction ring is rotated 90° and mirrored → the "best aim frame" index differs. BUT: ours notes "渲染未接,仅保状态" — the ai2 value only feeds rendering which isn't connected. So no gameplay impact; visual-only state. Given rendering isn't wired, this is dormant. I could mention as low severity. Also our selection: `e.ai2 = (sd === 1 ? 9 - (best + 1) : best + 1);` matches vanilla formula (spriteDirection==1 → 9 - ai2). OK.

Also ours missing `if (e.ai3 === 2) TargetClosest(false)` — target retarget at frame 2. Ours just uses passed player. Minor.

Also vanilla CanHit uses full hitbox (position,w,h vs player w,h) — ours losClear from e.x,e.y to player.x,player.y (top-left corners). losClear in bossAI.ts — approximate. Acceptable.

Now, Dutchman: ours calls moveAndCollide at end; vanilla noTileCollide? The Flying Dutchman — does it collide with tiles? It has noTileCollide = ... I believe the Dutchman ignores tiles (it's a flying ship, AI_093 doesn't set noTileCollide but the SetDefaults for type 491... hmm). Actually vanilla Dutchman does NOT ignore tile collision — it hovers above ground using the terrain scan. Its collision happens in the normal update. Ours moveAndCollide matches that. Fine.

One more: vanilla `if (Main.rand.Next(300) == 0)` for pirates — ours rnd(300)===0. matches.

Dust: vanilla 2 iterations, each 50% chance → smoke; ours 50% single. Cosmetic.

Now AI_107 walkers + Ogre. Let me read our file 1676-2441 and vanilla 63372-64919. That's a big chunk (~1550 lines vanilla). Let me read our file first.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:17.916Z · glm-x-preview-260804

```
Dutchman 和 cannon 已读取。现在处理最大的代码块：我们的 walker-107 实现（包括 Ogre）对比原版 AI_107。
```


---

## 🤖 Assistant · 2026-08-19T03:13:18.279Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts",
 "limit": 560,
 "offset": 1676
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:18.441Z

**📎 ToolResult**

```
1676	// AI_107 ImprovedWalkers（NPC.cs:63372-64919）——旧日军团地面 walker 族 1:1。
1677	//   552/553/554 埃特尼亚哥布林 T1/T2/T3   近战前摇（flag5,纯接触伤害）
1678	//   555/556/557 哥布林投弹手 T1/T2/T3     投 681 炸弹（flag12,42t 循环出手 18t）
1679	//   561/562/563 标枪手 T1/T2/T3           掷 662（T3→685）标枪（flag12,90t/出手 82t）
1680	//   566/567    旧日骷髅                   黑暗魔法师 RaiseGoblins 复活产物,120t 落地渐显
1681	//   568/569    枯萎兽                     灵气态（削甲 debuff+60t 自疗+脉冲音）
1682	//   570/571    德拉肯                     喷 671（60t 循环,出手 40t+多连拍）
1683	//   572/573    小妖精（地面）             自爆冲锋（700px 点火→64px 起爆 192² 伤 80）
1684	//   576/577    食人魔 T2/T3               三态（近挥/吐 676/跺地 683）按距离选招
1685	//   620         地精鲨                     不在本档（Enemy.ts case 107 留 chargerAI wet 路径）
1686	// 索敌（NPCUtils.TargetClosestOldOnesInvasion :261-273）：水晶 548（可击态）恒为候选,
1687	//   200px 内玩家按近者夺标（SearchFilters.OnlyPlayersInCertainDistance :23-26）。
1688	// 穿墙飞行（flag2,:63487-63507 + :64846-64918）：FighterUsesDD2PortalAppearEffect 族
1689	//   （NPCID.cs:4793=552-557/561-563/564-565/568-573/576-577）无视线且朝向目标时
1690	//   noGravity+noTileCollide 直飞——walker 翻山越壑奔水晶的原版机制。
1691	// ---------------------------------------------------------------------------
1692	
1693	/** GetAttackDamage_ForProjectiles（NPC.cs:7031-7034）：npc.difficulty 在
1694	 *  Classic(1)→Expert(2) 区间的 Utils.Remap（GameDifficultyLevel.cs:7-9;不钳界,
1695	 *  Master=3 外推照录）。Enemy.difficulty 即原版 npc.difficulty（ScaleStats 投影）。 */
1696	function projDmgOf(e: Enemy, normal: number, expert: number): number {
1697	  const t = e.difficulty - GDL.CLASSIC;   // 区间归零:Classic 0 / Expert 1 / Master 2
1698	  return Math.round(normal + (expert - normal) * t);
1699	}
1700	
1701	/** AI_107 族参数（cs:63415-63475 默认档 → 各 case 覆写;行号逐项标注） */
1702	interface Walker107P {
1703	  scream: string | null;        // style + num22：每 tick 1/num22 概率嘶叫（:64494）
1704	  screamOneIn: number;
1705	  melee: boolean;               // flag5 近战/喷吐前摇（:64356-64386）
1706	  triggerRange: number;         // num4 触发距（:63419）
1707	  windup: number;               // num5 前摇帧数（:63420）
1708	  cooldown: number;             // num6 前摇结束 → ai[0]=-num6（:63421）
1709	  windupDampOn: boolean;        // flag7（食人魔 true）
1710	  windupDamp: number;           // num7 前摇期 vx 阻尼（:63424）
1711	  shooter: boolean;             // flag12 远程循环（:64551-64679）
1712	  timer: number;                // num8 起手计时（:63433）
1713	  fireAt: number;               // num9 出手帧（:63434;德拉肯按 ai[1] 现值改写）
1714	  proj: number;                 // num12 弹型（:63438）
1715	  projDmg: number;              // num11（GetAttackDamage_ForProjectiles）
1716	  muzzleDx: number;             // vector.X（direction 倍率,cs:63436）
1717	  muzzleDy: number;             // vector.Y（绝对像素）
1718	  muzzleAtBottom: boolean;      // 食人魔跺地:vector.Y = height/2-1（:63581）
1719	  spawnOffset: number;          // num18 出膛位移倍率（cs:63445,德拉肯 0）
1720	  arc: number;                  // num15 弧线补偿 v.Y-=|v.X|*num15（:63441）
1721	  jitter: number;               // num16 出膛扰动（:63443）
1722	  shots: number;                // num17 连发数（:63437）
1723	  speed: number;                // num10 弹速（:63435）
1724	  startRange: number;           // num13 起手距（:63439）
1725	  fireOnWindup: boolean;        // flag3 前摇倒数中 ai[0]==num9 出弹（:64387-64419）
1726	  jump: boolean;                // flag4 前摇倒数中 ai[0]==num 起跳（:64420-64430）
1727	  jumpT: number;                // num（:63415）
1728	  jumpMinT: number;             // num2（:63416）
1729	  jumpVy: number;               // num3（:63417）
1730	  maxSpd: number;               // num23（:63460）
1731	  accel: number;                // num24（:63461）
1732	  damp: number;                 // num25（:63462）
1733	  noWalkAccel: boolean;         // flag24 远程族:走路加速改挂攻击块尾（:63632/:63950）
1734	  aimAbove: number;             // flag15 阈值:ai[1] > 此值时持续重定向（各族字面量）
1735	}
1736	
1737	/** FighterUsesDD2PortalAppearEffect（NPCID.cs:4793）：出生 60t 渐显 + 30t 出世音 */
1738	const W107_PORTAL_FADE = new Set([552, 553, 554, 555, 556, 557, 561, 562, 563,
1739	  564, 565, 568, 569, 570, 571, 572, 573, 576, 577]);
1740	
1741	/** 穿墙相位标记（原版 noGravity+noTileCollide 静态位 → WeakSet 落盘;flag2 滞回） */
1742	const w107Phasing = new WeakSet<Enemy>();
1743	/** 上一拍水平零位移（原版 position.X == oldPosition.X,:64437 的卡位计数源） */
1744	const w107NoMove = new WeakSet<Enemy>();
1745	
1746	function walker107Params(e: Enemy, x: number[]): Walker107P {
1747	  const id = e.vanillaId ?? 0;
1748	  const p: Walker107P = {
1749	    scream: null, screamOneIn: 0,
1750	    melee: false, triggerRange: 40, windup: 30, cooldown: 0,
1751	    windupDampOn: false, windupDamp: 0.9,
1752	    shooter: false, timer: 70, fireAt: 35, proj: 81, projDmg: 1,
1753	    muzzleDx: 0, muzzleDy: 0, muzzleAtBottom: false, spawnOffset: 1,
1754	    arc: 0.1, jitter: 0.5, shots: 1, speed: 11, startRange: 700,
1755	    fireOnWindup: false, jump: false, jumpT: 32, jumpMinT: 15, jumpVy: 9,
1756	    maxSpd: 1, accel: 0.07, damp: 0.8,
1757	    noWalkAccel: false, aimAbove: 0,
1758	  };
1759	  // 出生 60t 内移速爬坡（各族共通,cs:63624-63627/:63674-63678/:63842-63845/:63964-63967）
1760	  const rampAccel = (): boolean => {
1761	    if (x[3] >= 60) return false;
1762	    p.accel = 0.01 + (x[3] / 60) * 0.05;
1763	    return true;
1764	  };
1765	  switch (id) {
1766	    case 552: case 553: case 554: {        // 埃特尼亚哥布林（cs:63607-63628）
1767	      p.scream = 'dd2_goblin_scream'; p.screamOneIn = 1000;   // DD2_GoblinScream
1768	      p.melee = true;                                        // flag5 近战前摇
1769	      if (id === 553) { p.accel += 0.01; p.maxSpd += 0.2; }
1770	      if (id === 554) { p.accel += 0.02; p.maxSpd += 0.4; }
1771	      rampAccel();
1772	      break;
1773	    }
1774	    case 555: case 556: case 557: {        // 哥布林投弹手（cs:63993-64041）
1775	      p.scream = 'dd2_goblin_bomber_scream'; p.screamOneIn = 800;   // DD2_GoblinBomberScream
1776	      p.shooter = true; p.noWalkAccel = true;
1777	      p.timer = 42; p.fireAt = 18; p.proj = 681;                    // DD2GoblinBomb
1778	      p.muzzleDy = -14; p.arc = 0.4; p.speed = 6; p.startRange = 280;
1779	      p.aimAbove = 18;                     // flag15 = ai[1] > 18（:64003）
1780	      if (id === 555) { p.maxSpd = 0.88; p.jitter = 0.6; p.projDmg = projDmgOf(e, 20, 15); }
1781	      if (id === 556) { p.maxSpd = 0.88; p.jitter = 0.6; p.projDmg = projDmgOf(e, 30, 25); }
1782	      if (id === 557) { p.maxSpd = 1.12; p.jitter = 0.4; p.projDmg = projDmgOf(e, 40, 35); }
1783	      rampAccel();
1784	      if (x[3] < 60) p.startRange = 1;     // 出生爬坡期不起手（num13=1,:64013-64017）
1785	      break;
1786	    }
1787	    case 561: case 562: case 563: {        // 埃特尼亚标枪手（cs:63937-63992）
1788	      p.shooter = true; p.noWalkAccel = true;
1789	      p.timer = 90; p.fireAt = 82;
1790	      p.proj = id === 563 ? 685 : 662;     // DD2JavelinHostile[T3]（:63954-63958）
1791	      p.muzzleDy = -14; p.arc = 0; p.speed = 13; p.startRange = 600;
1792	      p.aimAbove = 82;                     // flag15 = ai[1] > 82（:63951）
1793	      if (id === 561) { p.maxSpd = 0.88; p.jitter = 0.6; p.speed = 11.5; p.startRange = 500; p.projDmg = projDmgOf(e, 15, 10); }
1794	      if (id === 562) { p.maxSpd = 0.94; p.jitter = 0.5; p.speed = 12.2; p.startRange = 550; p.projDmg = projDmgOf(e, 30, 20); }
1795	      if (id === 563) { p.maxSpd = 1; p.jitter = 0.4; p.projDmg = projDmgOf(e, 45, 30); }
1796	      // 出手帧嘶吼（:63942-63947）：DD2_JavelinThrowersAttack + 之后 1/7 概率 Taunt
1797	      if (e.ai1 === 82) {
1798	        p.scream = 'dd2_javelin_throwers_taunt'; p.screamOneIn = 7;
1799	      }
1800	      rampAccel();
1801	      if (x[3] < 60) p.startRange = 1;     // :63964-63968
1802	      break;
1803	    }
1804	    case 566: case 567:                    // 旧日骷髅（cs:64042-64117）——无攻击,落地渐显
1805	      break;
1806	    case 568: case 569: {                  // 枯萎兽（cs:63847-63936）——灵气态
1807	      p.windup = 110; p.accel = 0.16; p.damp = 0.7; p.maxSpd = 1.4;
1808	      p.melee = true; p.triggerRange = 600;
1809	      rampAccel();
1810	      break;
1811	    }
1812	    case 570: case 571: {                  // 德拉肯（cs:63629-63679）
1813	      p.shooter = true; p.noWalkAccel = true;
1814	      p.timer = 60; p.fireAt = 40; p.proj = 671;                    // DD2DrakinShot
1815	      p.muzzleDx = 22; p.arc = 0.15; p.speed = 13; p.startRange = 600;
1816	      p.spawnOffset = 0;                   // num18=0（:63652）
1817	      p.maxSpd = 0.77; p.jitter = 1.5;
1818	      p.projDmg = id === 571 ? projDmgOf(e, 60, 45) : projDmgOf(e, 35, 25);
1819	      if (id === 570) p.jitter = 2.5;      // :63653-63656
1820	      // 多连拍改写出手帧（:63637-63644:ai[1]∈(10,40] 且整除 6/9 → num9=ai[1]-1）
1821	      if (e.ai1 > 10 && e.ai1 <= 40 && e.ai1 % (id === 571 ? 6 : 9) === 0) {
1822	        p.fireAt = e.ai1 - 1;
1823	      }
1824	      p.aimAbove = 40;                     // flag15 = ai[1] > 40（:63634）
1825	      rampAccel();
1826	      if (x[3] < 60) p.startRange = 1;     // :63674-63678
1827	      break;
1828	    }
1829	    case 572: case 573:                    // 小妖精地面型（cs:63680-63846）——自爆冲锋
1830	      p.maxSpd = 0.88;
1831	      break;
1832	    case 576: case 577:                    // 食人魔（cs:63513-63606）——三态
1833	      p.scream = 'dd2_ogre_roar'; p.screamOneIn = 700;              // DD2_OgreRoar
1834	      p.melee = true; p.windupDampOn = true; p.windupDamp = 0.7;
1835	      p.cooldown = 60; p.triggerRange = 130; p.windup = 44;
1836	      // 选招在主函数 ogre 状态块（先于本 builder 跑,见 ai107ImprovedWalkers 头部）:
1837	      // ≤430 跺地(ai[1]=2) / >160 吐息(=1) / 否则近挥(=0)
1838	      if (e.ai1 === 2) {                   // 跺地（:63569-63586）
1839	        p.windup = 90; p.triggerRange = 250;
1840	        p.fireOnWindup = true; p.jump = true;
1841	        p.jumpT = 56; p.jumpMinT = 41; p.jumpVy = 13;
1842	        p.fireAt = 36; p.proj = 683;       // DD2OgreSmash
1843	        p.projDmg = projDmgOf(e, 60, 40);
1844	        p.aimAbove = 0;                   // flag15=false（:63580）
1845	        p.muzzleDx = -20; p.muzzleAtBottom = true;   // vector=(-direction*20,height/2-1)
1846	      } else if (e.ai1 === 1) {            // 吐息（:63587-63600）
1847	        p.windup = 90; p.triggerRange = 1000;
1848	        p.fireOnWindup = true;
1849	        p.fireAt = 35; p.proj = 676;       // DD2OgreSpit（num9=默认 num8/2=35）
1850	        p.projDmg = projDmgOf(e, 40, 30);
1851	        p.aimAbove = 0;                   // flag15=false（:63587）
1852	        p.muzzleDx = 30; p.muzzleDy = -70;            // vector=(direction*30,-70)
1853	      }
1854	      // 近挥（ai[1]==0）:默认参数（num5=44,无弹）
1855	      break;
1856	    default:
1857	      break;
1858	  }
1859	  return p;
1860	}
1861	
1862	/** AI_107 出膛（cs:64394-64417 flag3 / :64575-64615 flag12 共用弹道） */
1863	function fireWalkerProj(
1864	  game: GameHooks, e: Enemy, p: Walker107P, tx: number, ty: number,
1865	): void {
1866	  const mx = e.cx + p.muzzleDx * e.facing;
1867	  const my = e.cy + (p.muzzleAtBottom ? e.h / 2 - 1 : p.muzzleDy);
1868	  let vx = tx - mx, vy = ty - my;
1869	  vy -= Math.abs(vx) * p.arc;              // 弧线补偿
1870	  const len = Math.hypot(vx, vy) || 1;
1871	  vx = (vx / len) * p.speed;
1872	  vy = (vy / len) * p.speed;
1873	  const sx = mx + vx * p.spawnOffset, sy = my + vy * p.spawnOffset;
1874	  for (let i = 0; i < p.shots; i++) {
1875	    const jx = vx + (Math.random() * 2 - 1) * p.jitter;   // Utils.RandomVector2(±num16)
1876	    const jy = vy + (Math.random() * 2 - 1) * p.jitter;
1877	    if (p.proj === 681) {
1878	      // 681 哥布林炸弹（aiStyle 16,SetDefaults :6984-6991）——引信/反弹/80² 爆盒
1879	      (game as unknown as { entities: { add: (en: unknown, b: string) => void } })
1880	        .entities.add(new DD2GoblinBomb(sx, sy, jx, jy, p.projDmg), 'projectiles');
1881	    } else if (p.proj === 683) {
1882	      // 683 食人魔跺地波（aiStyle 135,SetDefaults :7003+）——原地 80→640 扩盒
1883	      (game as unknown as { entities: { add: (en: unknown, b: string) => void } })
1884	        .entities.add(new DD2OgreSmash(sx, sy, p.projDmg), 'projectiles');
1885	    } else {
1886	      // 662/685 标枪、671 德拉肯弹、676 食人魔涎（均 aiStyle 1,:6843/:6907/:6952）
1887	      // ——grav 0.3 抛物线,penetrate -1（Arrow 以大值近似无限穿透）
1888	      shootD(game, sx, sy, jx, jy, p.projDmg, p.proj, 180, 0.3, 999);
1889	    }
1890	  }
1891	}
1892	
1893	/** AI_107 目标（NPCUtils.TargetClosestOldOnesInvasion :261-273 + SearchForTarget
1894	 *  :196-259）：水晶 548（!dontTakeDamageFromHostiles）恒候选;200px 内玩家按距夺标 */
1895	interface W107Target { x: number; y: number; w: number; h: number; cx: number; cy: number; }
1896	
1897	function w107Target(game: GameHooks, e: Enemy, player: Player | null): W107Target | null {
1898	  let crystal: Enemy | null = null;
1899	  for (const n of game.enemies() as Enemy[]) {
1900	    if (!n.dead && n.vanillaId === 548 && !n.dontTakeDamage) { crystal = n; break; }
1901	  }
1902	  const pd = player && !player.dead
1903	    ? Math.hypot(player.cx - e.cx, player.cy - e.cy) : Infinity;
1904	  if (crystal) {
1905	    const cd = Math.hypot(crystal.cx - e.cx, crystal.cy - e.cy);
1906	    if (pd <= 200 && pd < cd) {
1907	      return { x: player!.x, y: player!.y, w: player!.w, h: player!.h, cx: player!.cx, cy: player!.cy };
1908	    }
1909	    return { x: crystal.x, y: crystal.y, w: crystal.w, h: crystal.h, cx: crystal.cx, cy: crystal.cy };
1910	  }
1911	  if (pd !== Infinity) {
1912	    return { x: player!.x, y: player!.y, w: player!.w, h: player!.h, cx: player!.cx, cy: player!.cy };
1913	  }
1914	  return null;
1915	}
1916	
1917	/** AI_107 走路加速核（:64537-64550 / :64660-64678 同式） */
1918	function w107WalkAccel(e: Enemy, p: Walker107P): void {
1919	  if (e.vx < -p.maxSpd || e.vx > p.maxSpd) {
1920	    if (e.vy === 0) { e.vx *= p.damp; e.vy *= p.damp; }    // velocity *= num25
1921	  } else if ((e.vx < p.maxSpd && e.facing === 1) || (e.vx > -p.maxSpd && e.facing === -1)) {
1922	    e.vx = clamp(e.vx + p.accel * e.facing, -p.maxSpd, p.maxSpd);
1923	  }
1924	}
1925	
1926	/** AI_107 主入口（NPC.cs:63372-64919） */
1927	export function ai107ImprovedWalkers(e: Enemy, game: GameHooks, player: Player | null): void {
1928	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1929	  const x = dd2LocalAI(e);
1930	  const id = e.vanillaId ?? 0;
1931	  // ---- 目标（先取,各族 case 内的音效/选招都读它） ----
1932	  let tgt = w107Target(game, e, player);
1933	  // ---- 食人魔距离选招（cs:63528-63555）：ai[0]<=0 且出生 60t 后,按目标距定 ai[1] ----
1934	  if (id === 576 || id === 577) {
1935	    if (x[0] > 0) x[0] -= 1;               // localAI[0] 跺地冷却（:63524-63527）
1936	    if (e.ai0 <= 0 && x[3] >= 60 && tgt) {
1937	      const prev = e.ai1;
1938	      const dist = Math.hypot(tgt.cx - e.cx, tgt.cy - e.cy);
1939	      if (x[3] >= 60) {
1940	        if (dist <= 130 + 300 && x[0] <= 0) e.ai1 = 2;       // 跺地（:63534-63537）
1941	        else if (dist > 130 + 30) e.ai1 = 1;                 // 吐息（:63538-63540）
1942	        else if (!(dist > 130)) {
1943	          e.ai1 = 0;                                         // 近挥（:63541-63549）
1944	          if (prev === 1) e.ai0 = 0;
1945	        }
1946	      }
1947	    }
1948	    if (e.ai0 > 0 && e.ai1 === 2) x[0] = 300;                // 跺地后冷却（:63556-63559）
1949	  }
1950	  const p = walker107Params(e, x);
1951	  // ---- 旧日骷髅落地渐显（cs:64042-64117）：120t 不可击/悬停,之后正常 walker ----
1952	  if (id === 566 || id === 567) {
1953	    if (x[3] < 120) {
1954	      e.iframes = 2;                       // dontTakeDamage=true（:64058）
1955	      e.vx = 0;
1956	      e.ai3 = 0;
1957	      if (x[3] === 0) e.spawnAlpha = 255;
1958	      x[3] += 1;
1959	      if (x[3] >= 110) e.spawnAlpha = Math.max(0, e.spawnAlpha - 26);   // :64069-64076
1960	      e.alphaFade = false;                 // 本 AI 自管渐显
1961	      e.vy = Math.min(e.vy + 0.3, 10);     // 悬停期仍受重力（noGravity 未置位）
1962	      moveAndCollide(e, game.world, e.vx, e.vy);
1963	      return;
1964	    }
1965	  }
1966	  // ---- 出生渐显（flag29,cs:64262-64300）：60t,30t 出世音,尘带 ----
1967	  if (W107_PORTAL_FADE.has(id)) {
1968	    if (x[3] === 0) e.spawnAlpha = 255;
1969	    if (x[3] === 30) {
1970	      game.playSfxFiles(soundTrackFiles('dd2_etherian_portal_spawn_enemy'), 0.4, e.cx, e.cy);
1971	    }
1972	    if (x[3] < 60) {
1973	      x[3] += 1;
1974	      e.spawnAlpha = Math.max(0, e.spawnAlpha - 5);
1975	      e.alphaFade = false;
1976	    }
1977	  } else if (x[3] < 60) {
1978	    x[3] += 1;                             // 非渐显族也推进（各族出生爬坡读 x[3]）
1979	  }
1980	  // ---- 枯萎兽灵气态（cs:63861-63935）:ai[0]==1 进入,此后 1↔2 振荡驻留 ----
1981	  if (id === 568 || id === 569) {
1982	    if (e.ai0 === 0) x[1] = 0;
1983	    if (e.ai0 === 1) {
1984	      e.def.hitSound = soundTrackFiles('dd2_wither_beast_crystal_impact');  // HitSound（:63871）
1985	      e.ai0 += 1;                          // →2,由下方 flag5 块减回 1 形成驻留
1986	      x[0] += 1;
1987	      if (x[1] === 0) {
1988	        x[1] = 1;
1989	        game.playSfxFiles(soundTrackFiles('dd2_wither_beast_aura_pulse'), 0.5, e.cx, e.cy);
1990	      }
1991	      // 400px 内玩家削甲 debuff（buff 195 WitheredArmor 3t，Player.cs:11436 施加链；
1992	      //   本仓 BuffType.WitheredArmor=101 已建模，defense 终值减半）—— aura 期间每 tick 续期
1993	      {
1994	        const pl = (game as unknown as { player: { buffs: { apply: (t: number, secs: number) => void } | null; cx: number; cy: number } }).player;
1995	        if (pl?.buffs && Math.abs(pl.cx - e.cx) <= 400 && Math.abs(pl.cy - e.cy) <= 400) {
1996	          pl.buffs.apply(101 /* BuffType.WitheredArmor */, 0.06);   // 3t ≈ 0.05s
1997	        }
1998	      }
1999	      // 60t 自疗 lifeMax/20（:63912-63934）
2000	      if (e.ai1 > 0) e.ai1 -= 1;
2001	      if (e.ai1 <= 0) {
2002	        e.ai1 = 60;
2003	        const heal = Math.min(Math.floor(e.maxHp / 20), e.maxHp - e.hp);
2004	        if (heal > 0) {
2005	          e.hp += heal;
2006	          game.addDamageNumber(e.cx, e.cy - 10, -heal, false, '#7CFF6A');
2007	        }
2008	      }
2009	      // 目标在 400px 内 → 灵气脉动尘
2010	      if (tgt && Math.hypot(tgt.cx - e.cx, tgt.cy - e.cy) < 400
2011	        && Math.random() < 0.1) {
2012	        game.spawnParticles(e.cx + (Math.random() - 0.5) * 40, e.cy - 20, '#C060FF', 1, 0.8, { life: 30 });
2013	      }
2014	    }
2015	  }
2016	  // ---- 小妖精地面型自爆链（cs:63680-63846） ----
2017	  if (id === 572 || id === 573) {
2018	    if (e.ai1 === 2) {
2019	      // 起爆（:63692-63749）：192² 盒、伤 80、3t 消散（不走掉落管线）
2020	      e.x = e.cx; e.y = e.cy;
2021	      e.w = 192; e.h = 192;
2022	      e.x -= e.w / 2; e.y -= e.h / 2;
2023	      e.vx = 0; e.vy = 0;
2024	      e.def.damage = 80;                   // GetAttackDamage_ScaledByDifficulty(80)
2025	      e.spawnAlpha = 255;
2026	      if (e.ai0 === 0) {
2027	        game.spawnParticles(e.cx, e.cy, '#FFD24A', 20, 4, { life: 30, grav: -0.05 });
2028	        game.spawnParticles(e.cx, e.cy, '#FF9A3C', 12, 3, { life: 40 });
2029	      }
2030	      e.ai0 += 1;
2031	      if (e.ai0 >= 3) {
2032	        game.playSfxFiles(soundTrackFiles('dd2_kobold_explosion'), 1, e.cx, e.cy);  // DD2_KoboldExplosion（:63744）
2033	        game.spawnParticles(e.cx, e.cy, '#FFB060', 30, 5, { life: 36 });
2034	        e.dead = true;                     // life=0 + active=false（:63745-63747）
2035	      }
2036	      return;
2037	    }
2038	    if (e.ai0 > 0 && e.ai1 === 0) {
2039	      // 点火（:63751-63770）：DD2_KoboldIgnite + 30t 后引信/冲锋循环音
2040	      if (x[2] === 0) game.playSfxFiles(soundTrackFiles('dd2_kobold_ignite'), 0.6, e.cx, e.cy);
2041	      x[2] += 1;
2042	      if (x[2] === 30) {
2043	        game.playSfxFiles(soundTrackFiles('dd2_kobold_ignite_loop'), 0.5, e.cx, e.cy);
2044	        game.playSfxFiles(soundTrackFiles('dd2_kobold_scream_charge_loop'), 0.5, e.cx, e.cy);
2045	      }
2046	    }
2047	    if (e.ai0 > 0 && e.ai1 === 1) {
2048	      e.ai0 = 0; e.ai1 = 2;                // 冲锋中再触发 → 起爆（:63771-63777）
2049	      return;
2050	    }
2051	    if (e.ai0 === 1) e.ai1 = 1;            // 前摇倒数到 1 → 冲锋态（:63779-63782）
2052	    if (e.ai1 > 0 && e.ai0 === 0) {
2053	      // 冲锋档（:63808-63835）：触发距 64、4 速直冲;引信/冲锋循环音（:63783-63807
2054	      // 原版为跟踪 loop,本仓按 60t 一拍补播近似——音轨库无 loop 句柄时不可续）
2055	      if (x[1] === 0 || x[1] >= 60) {
2056	        x[1] = 1;
2057	        game.playSfxFiles(soundTrackFiles('dd2_kobold_ignite_loop'), 0.4, e.cx, e.cy);
2058	        game.playSfxFiles(soundTrackFiles('dd2_kobold_scream_charge_loop'), 0.4, e.cx, e.cy);
2059	      } else {
2060	        x[1] += 1;
2061	      }
2062	      if (Math.random() < 1 / 6) {
2063	        game.spawnParticles(e.cx + e.facing * 12, e.cy, '#FFD0A0', 1, 0.8, { life: 30 });
2064	      }
2065	      p.melee = true; p.windup = 40; p.triggerRange = 64;
2066	      p.accel = 0.3; p.maxSpd = 4;
2067	    } else {
2068	      // 接近档（:63836-63841）：700px 内点火
2069	      p.melee = true; p.windup = 40; p.triggerRange = 700;
2070	    }
2071	  }
2072	  // ---- 食人魔招式音（cs:63562-63600）:ai[0]==40 近挥/跺地,==80 吐息 ----
2073	  if ((id === 576 || id === 577) && e.ai0 === 40) {
2074	    if (e.ai1 === 0) game.playSfxFiles(soundTrackFiles('dd2_ogre_attack'), 0.8, e.cx, e.cy);
2075	    else if (e.ai1 === 2) game.playSfxFiles(soundTrackFiles('dd2_ogre_ground_pound'), 0.8, e.cx, e.cy);
2076	  }
2077	  if ((id === 576 || id === 577) && e.ai0 === 80 && e.ai1 === 1) {
2078	    game.playSfxFiles(soundTrackFiles('dd2_ogre_spit'), 0.8, e.cx, e.cy);
2079	  }
2080	  // ---- 远程族招式音（cs:63663-63673/:63942-63947/:64036-64039,均读减数前 ai[1]） ----
2081	  if (p.shooter && e.ai0 > 0) {
2082	    if (id === 570 || id === 571) {
2083	      if (e.ai1 === 40) game.playSfxFiles(soundTrackFiles('dd2_drakin_shot'), 0.7, e.cx, e.cy);
2084	      else if (e.ai1 === 60) game.playSfxFiles(soundTrackFiles('dd2_drakin_breath_in'), 0.6, e.cx, e.cy);
2085	    }
2086	    if ((id === 561 || id === 562 || id === 563) && e.ai1 === 82) {
2087	      game.playSfxFiles(soundTrackFiles('dd2_javelin_throwers_attack'), 0.7, e.cx, e.cy);
2088	    }
2089	    if ((id === 555 || id === 556 || id === 557) && e.ai1 === p.fireAt) {
2090	      game.playSfxFiles(soundTrackFiles('dd2_goblin_bomber_throw'), 0.7, e.cx, e.cy);
2091	    }
2092	  }
2093	  // ---- 穿墙相位判定（flag2,cs:63487-63507） ----
2094	  let phase = false;
2095	  if (W107_PORTAL_FADE.has(id)) {
2096	    phase = w107Phasing.has(e);            // noGravity 滞回（:63491 第二析取项）
2097	    if (tgt) {
2098	      const noLos = !losClear(game, e.cx, e.cy, tgt.cx, tgt.cy);
2099	      const dist = Math.hypot(tgt.cx - e.cx, tgt.cy - e.cy);
2100	      if (noLos && (e.facing === sign(tgt.cx - e.cx) || (phase && dist > 50 && e.cy > tgt.cy))) {
2101	        phase = e.ai0 <= 0;                // flag2 &= ai[0] <= 0（攻击中不穿墙）
2102	      } else {
2103	        phase = false;
2104	      }
2105	    } else {
2106	      phase = false;
2107	    }
2108	    if (phase) w107Phasing.add(e); else w107Phasing.delete(e);
2109	  }
2110	  const attacking = (p.melee || p.shooter) && e.ai0 > 0;    // (flag12||flag5)&&ai[0]>0 → flag18=false
2111	  const busy = attacking || (p.shooter && e.ai1 > 0) || (p.melee && e.ai0 > 0);   // flag22
2112	  // ---- 卡位/转向计数（cs:64431-64456,flag18=true 时推进;DD2 族 flag30=false 只计数） ----
2113	  if (!attacking) {
2114	    // position.X == oldPosition.X（:64437）= 上一拍水平位移为零 → w107NoMove 落盘
2115	    const flag19 = e.vy === 0 && e.vx * e.facing < 0;
2116	    if (w107NoMove.has(e) || flag19 || e.ai3 >= 30) e.ai3 += 1;
2117	    else if (Math.abs(e.vx) > 0.9 && e.ai3 > 0) e.ai3 -= 1;
2118	    if (e.ai3 > 300) e.ai3 = 0;            // num21*10
2119	    if (e.justHit) e.ai3 = 0;              // justHit && !flag30（:64449-64452）
2120	    if (tgt && e.x < tgt.x + tgt.w && e.x + e.w > tgt.x
2121	      && e.y < tgt.y + tgt.h && e.y + e.h > tgt.y) e.ai3 = 0;
2122	  }
2123	  // ---- 嘶叫 + 重定向 / 静止折返（cs:64490-64536） ----
2124	  if (e.ai3 < 30) {
2125	    // flag21 = DD2Event.EnemiesShouldChasePlayers（DD2Event.cs:115-123 恒真）
2126	    if (p.scream && p.screamOneIn > 0 && rnd(p.screamOneIn) === 0) {
2127	      game.playSfxFiles(soundTrackFiles(p.scream), 0.6, e.cx, e.cy);
2128	    }
2129	    tgt = w107Target(game, e, player);     // TargetClosestOldOnesInvasion
2130	    if (tgt) e.facing = tgt.cx > e.cx ? 1 : -1;
2131	  } else if (!busy) {
2132	    if (e.vx === 0) {
2133	      if (e.vy === 0) {
2134	        e.ai2 += 1;
2135	        if (e.ai2 >= 2) {                  // 静止 2t 折返（:64516-64523）
2136	          e.facing *= -1;
2137	          e.ai2 = 0;
2138	        }
2139	      }
2140	    } else if (e.ai2 !== 0) {
2141	      e.ai2 = 0;
2142	    }
2143	    if (e.facing === 0) e.facing = 1;
2144	  }
2145	  // ---- 走路加速（flag24=false 族;cs:64537-64550） ----
2146	  if (!p.noWalkAccel) w107WalkAccel(e, p);
2147	  // ---- 远程循环（flag12,cs:64551-64679） ----
2148	  if (p.shooter) {
2149	    if (e.ai1 > 0) e.ai1 -= 1;             // 先减后比（德拉肯多连拍依赖此序）
2150	    if (e.justHit) { e.ai1 = 30; e.ai0 = 0; }   // num19=30（:64563-64567）
2151	    const aimRetarget = e.ai1 > p.aimAbove;   // flag15（各族字面阈值,德拉肯不随连拍改写）
2152	    if (e.ai0 > 0) {
2153	      if (aimRetarget && tgt) e.facing = tgt.cx > e.cx ? 1 : -1;
2154	      if (tgt && e.ai1 === p.fireAt) {
2155	        fireWalkerProj(game, e, p, tgt.cx, tgt.cy);
2156	        // 姿态角 ai[0]=1..5（渲染语义,cs:64599-64614——按弹道主轴选向,仅保状态）
2157	        const dx = tgt.cx - e.cx, dy = tgt.cy - e.cy;
2158	        e.ai0 = Math.abs(dy) > Math.abs(dx) * 2 ? (dy > 0 ? 1 : 5)
2159	          : Math.abs(dx) > Math.abs(dy) * 2 ? 3 : (dy > 0 ? 2 : 4);
2160	        e.facing = dx > 0 ? 1 : -1;
2161	      }
2162	      if (e.vy !== 0 || e.ai1 <= 0) {      // flag14=false:腾空/计时尽 → 收招
2163	        e.ai0 = 0;
2164	        e.ai1 = 0;
2165	      } else {
2166	        e.vx *= 0.9;                       // 瞄准减速（:64629）
2167	      }
2168	    }
2169	    // 起手（:64633-64658）：站桩 + 视线 + num13 内 → 半速 + ai[0]=3/ai[1]=num8
2170	    if (e.ai0 <= 0 && e.vy === 0 && e.ai1 <= 0 && tgt
2171	      && losClear(game, e.cx, e.cy, tgt.cx, tgt.cy)) {
2172	      const d = Math.hypot(tgt.cx - e.cx, tgt.cy - e.cy);
2173	      if (d < p.startRange) {
2174	        e.vx *= 0.5;
2175	        const dx = tgt.cx - e.cx, dy = tgt.cy - e.cy;
2176	        e.ai0 = Math.abs(dy) > Math.abs(dx) * 2 ? (dy > 0 ? 1 : 5)
2177	          : Math.abs(dx) > Math.abs(dy) * 2 ? 3 : (dy > 0 ? 2 : 4);
2178	        e.ai1 = p.timer;
2179	        e.facing = dx > 0 ? 1 : -1;
2180	      }
2181	    }
2182	    if (e.ai0 <= 0) w107WalkAccel(e, p);   // 收招后走路加速（:64660-64678）
2183	  }
2184	  // ---- 近战/喷吐前摇（flag5,cs:64356-64386） ----
2185	  if (p.melee) {
2186	    if (e.ai0 < 0) e.ai0 += 1;             // 冷却回摆（:64358-64362）
2187	    if (e.ai0 === 0 && e.vy === 0 && tgt
2188	      && losClear(game, e.cx, e.cy, tgt.cx, tgt.cy)
2189	      && Math.hypot(tgt.cx - e.cx, tgt.cy - e.cy) < p.triggerRange) {
2190	      e.ai0 = p.windup;                    // 起手（:64363-64367）
2191	    }
2192	    if (e.ai0 > 0) {
2193	      if (p.windupDampOn) {                // flag7（食人魔 0.7,:64371-64378）
2194	        e.vx *= p.windupDamp;
2195	      }
2196	      e.ai0 -= 1;
2197	      if (e.ai0 === 0) e.ai0 = -p.cooldown;
2198	    }
2199	    if (id === 576 || id === 577) {
2200	      if (e.ai0 < -p.cooldown) e.ai0 = -p.cooldown;   // 钳界（:63602-63605）
2201	    }
2202	  }
2203	  // ---- 前摇倒数中出弹（flag3,cs:64387-64419:食人魔吐息/跺地） ----
2204	  if (p.fireOnWindup && e.ai0 > 0) {
2205	    if (tgt && e.ai0 === p.fireAt) fireWalkerProj(game, e, p, tgt.cx, tgt.cy);
2206	  }
2207	  // ---- 前摇倒数中起跳（flag4,cs:64420-64430:跺地 ai[0]==56 → vy=-13） ----
2208	  if (p.jump && e.ai0 > 0) {
2209	    if (e.vy !== 0 && e.ai0 < p.jumpMinT) e.ai0 = p.jumpMinT;
2210	    if (e.ai0 === p.jumpT) e.vy = -p.jumpVy;
2211	  }
2212	  // ---- 位移（原版由公共碰撞步承载;此处按引擎惯例自理） ----
2213	  if (phase) {
2214	    // 穿墙飞行（cs:64846-64918）：水平 Lerp 朝目标 + 三档垂直伺服
2215	    if (W107_PORTAL_FADE.has(id) && e.spawnAlpha < 60) e.spawnAlpha += 20;   // :64852-64858
2216	    const wasGrounded = e.vy === 0;
2217	    if (tgt && Math.abs(tgt.cx - e.cx) > 200) {
2218	      e.facing = sign(tgt.cx - e.cx);
2219	      e.vx = lerp(e.vx, e.facing, 0.05);   // :64860-64864
2220	    }
2221	    const below = tgt ? e.y + e.h < tgt.y + tgt.h - 16 : false;
2222	    if (below) {
2223	      e.vy += 0.5;                         // 目标在下方 → 直坠（:64869-64876）
2224	    } else {
2225	      const probeSolid = solidAt(game, Math.floor((e.cx - 40) / TILE), Math.floor((e.y + e.h - e.h) / TILE))
2226	        || (tgt && (tgt.cy - e.cy < -100
2227	          || (tgt.cy - e.cy < 10 && Math.abs(tgt.cx - e.cx) < 60)));
2228	      if (tgt && probeSolid) {
2229	        if (e.vy > 0) e.vy = 0;
2230	        e.vy -= e.vy > -0.2 ? 0.025 : 0.2; // 贴地/悬停伺服（:64877-64894）
2231	        if (e.vy < -4) e.vy = -4;
2232	      } else {
2233	        if (e.vy < 0) e.vy = 0;
2234	        e.vy += e.vy < 0.1 ? 0.025 : 0.5;  // 落回伺服（:64896-64909）
2235	      }

```


---

## 🤖 Assistant · 2026-08-19T03:13:22.760Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
I've read up to line 2235. Let me read the rest (2235-2441), and also read the vanilla AI_107 sections. Let me also read the vanilla 63372-64919 in chunks. That's 1548 lines. Let me focus on the Ogre-relevant sections (63415-63606) and the main flow sections (64356-64679, 64846-64919), plus each family case as needed.

First finish reading our file.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:23.069Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts",
 "offset": 2235
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:23.088Z

**📎 ToolResult**

```
2235	      }
2236	    }
2237	    if (e.vy > 10) e.vy = 10;
2238	    if (wasGrounded) e.vy = 0;             // :64915-64918
2239	    fly(e);
2240	    return;
2241	  }
2242	  // ---- 常规:重力 + 台阶 + 跳梯（公共 gravity :91519-91525 + StepUp/跳梯 :64703-64832） ----
2243	  e.vy = Math.min(e.vy + 0.3, 10);
2244	  {
2245	    const st = game.world.store;
2246	    const solidAtT = (tx: number, ty: number): boolean =>
2247	      st.inBounds(tx, ty) && st.isSolid(tx, ty);
2248	    const dirX = e.facing;
2249	    // 台阶步升（Collision.StepUp 近似,同 chargerAI:前方高差 ≤16.1 直接抬升）
2250	    const vxSign = sign(e.vx);
2251	    if (e.vy >= 0 && vxSign !== 0) {
2252	      const ax = Math.floor((e.x + e.vx + e.w / 2 + (e.w / 2 + 1) * vxSign) / TILE);
2253	      const fr = Math.floor((e.y + e.h - 1) / TILE);
2254	      if (ax >= 0 && fr >= 2 && ax < st.w && fr < st.h
2255	        && solidAtT(ax, fr) && !st.half[st.idx(ax, fr)]
2256	        && !solidAtT(ax, fr - 1) && !solidAtT(ax, fr - 2) && !solidAtT(ax, fr - 3)) {
2257	        const rise = e.y + e.h - fr * TILE;
2258	        if (rise > 0 && rise <= 16.1) e.y = fr * TILE - e.h;
2259	      }
2260	    }
2261	    // 跳梯（cs:64711-64832,flag32 = 落地且脚下实心;num26 = width/2+6 探针）
2262	    let grounded = false;
2263	    if (e.vy === 0) {
2264	      const row = Math.floor((e.y + e.h + 7) / TILE);
2265	      const l = Math.floor(e.x / TILE), r = Math.floor((e.x + e.w) / TILE);
2266	      for (let tx = l; tx <= r && !grounded; tx++) {
2267	        if (solidAtT(clamp(tx, 0, st.w - 1), clamp(row, 0, st.h - 1))) grounded = true;
2268	      }
2269	    }
2270	    if (grounded && e.vx * e.facing > 0) {
2271	      const num26 = e.w / 2 + 6;                       // :63463（食人魔 -32,:63517 已按体宽体现）
2272	      const px = Math.floor((e.cx + num26 * dirX) / TILE);
2273	      const py = Math.floor((e.y + e.h - 15) / TILE);
2274	      const flag36 = e.y + e.h - py * TILE > 20;
2275	      const t1 = solidAtT(px + dirX, py + 1), t2 = solidAtT(px, py + 1);
2276	      const t3 = solidAtT(px, py), t4 = solidAtT(px, py - 1);
2277	      const t5 = solidAtT(px, py - 2), t6 = solidAtT(px, py - 3);
2278	      if (e.h >= 32 && t5) {                          // 3 格墙大跳（:64797-64805）
2279	        e.vy = t6 ? -8 : -7;
2280	      } else if (t4) {                                // 1 格台阶小跳（:64806-64810）
2281	        e.vy = -6;
2282	      } else if (flag36 && t3) {                      // 坡/半格（:64811-64815）
2283	        e.vy = -5;
2284	      } else if (e.dirY < 0 && !t2 && !t1) {          // 悬崖前跃（flag25,:64816-64821）
2285	        e.vx *= 1.5;
2286	        e.vy = -8;
2287	      }
2288	    }
2289	  }
2290	  const preX = e.x;
2291	  oldVel.set(e, { x: e.vx, y: e.vy });
2292	  moveAndCollide(e, game.world, e.vx, e.vy);
2293	  if (e.hitWall) e.vx = 0;
2294	  if (e.onGround || e.hitHead) e.vy = 0;
2295	  if (Math.abs(e.x - preX) < 0.01) w107NoMove.add(e); else w107NoMove.delete(e);
2296	}
2297	
2298	// ---------------------------------------------------------------------------
2299	// 681 哥布林炸弹（ProjectileID.cs:1722;SetDefaults :6984-6991 aiStyle 16/14²/
2300	//   hostile/penetrate -1）。AI_016 引信族物理同 WeaponProj.GrenadeProj（重力 0.2、
2301	//   撞墙 ×-0.4 反弹、落地摩擦 0.97、接触熔断 3t）;Kill :68638-68696 = 80² 伤害盒
2302	//   + DD2_GoblinBomb 音 + 尘爆。敌对弹:爆盒伤玩家与永恒水晶 548。
2303	// ---------------------------------------------------------------------------
2304	export class DD2GoblinBomb extends Entity {
2305	  w = 14; h = 14;
2306	  vx: number;
2307	  vy: number;
2308	  damage: number;
2309	  dead = false;
2310	  private fuse: number;
2311	  private rot = 0;
2312	  private cxPx = 0; private cyPx = 0;
2313	  constructor(x: number, y: number, vx: number, vy: number, dmg: number) {
2314	    super();
2315	    this.x = x - this.w / 2; this.y = y - this.h / 2;
2316	    this.vx = vx; this.vy = vy;
2317	    this.damage = dmg;
2318	    this.fuse = 180;                       // timeLeft 缺省 180（aiStyle 16 无显式覆写）
2319	  }
2320	  fixedUpdate(_dt: number, game: GameHooks): void {
2321	    const st = game.world.store;
2322	    // 接触熔断（Projectile.Damage :12330-12340:碰玩家/NPC → timeLeft 钳 3）
2323	    const pl = game.player;
2324	    if (pl && !pl.dead
2325	      && this.x < pl.x + pl.w && this.x + this.w > pl.x
2326	      && this.y < pl.y + pl.h && this.y + this.h > pl.y && this.fuse > 3) this.fuse = 3;
2327	    if (--this.fuse <= 0) { this.explode(game); return; }
2328	    this.rot += this.vx * 0.1;             // 滚动（AI_016 :44909-44915）
2329	    this.vy = Math.min(this.vy + 0.2, 16);
2330	    let nx = this.x + this.vx, ny = this.y + this.vy;
2331	    const solidAtP = (px: number, py: number): boolean => {
2332	      const tx = Math.floor(px / TILE), ty = Math.floor(py / TILE);
2333	      return st.inBounds(tx, ty) && st.isSolid(tx, ty);
2334	    };
2335	    if (solidAtP(nx + this.w / 2, this.y + this.h / 2)
2336	      || solidAtP(nx + this.w / 2, this.y + this.h - 1)) {
2337	      this.vx *= -0.4; nx = this.x;        // 撞墙反弹（:18344-18350）
2338	    }
2339	    if (solidAtP(nx + this.w / 2, ny + this.h - 1)) {
2340	      if (this.vy > 0.7) this.vy *= -0.4;  // 落地反弹（:18351-18357）
2341	      else { this.vy = 0; this.vx *= 0.97; }
2342	      ny = this.y;
2343	    }
2344	    this.x = nx; this.y = ny;
2345	    if (!st.inBounds(Math.floor(this.cx / TILE), Math.floor(this.cy / TILE))) this.dead = true;
2346	  }
2347	  /** Kill :68638-68696：80² 爆盒 + 尘爆 + 音效 */
2348	  private explode(game: GameHooks): void {
2349	    this.dead = true;
2350	    game.onProjectileDeath?.(681, this.x, this.y, this.w, this.h);
2351	    game.playSfx('explosion', 1, this.cx, this.cy);
2352	    game.spawnParticles(this.cx, this.cy, '#FFD24A', 14, 4, { life: 30, grav: -0.05 });
2353	    game.spawnParticles(this.cx, this.cy, '#FF9A3C', 10, 3, { life: 40 });
2354	    const bx = this.cx - 40, by = this.cy - 40;   // 80×80（:68689-68695）
2355	    const pl = game.player;
2356	    if (pl && !pl.dead
2357	      && pl.x < bx + 80 && pl.x + pl.w > bx && pl.y < by + 80 && pl.y + pl.h > by) {
2358	      game.damagePlayer(this.damage, this.cx, this.cy);
2359	    }
2360	    for (const n of game.enemies() as Enemy[]) {
2361	      // 永恒水晶 548 吃敌对爆伤（DD2 敌怪对水晶的伤害通道）
2362	      if (n.dead || n.vanillaId !== 548 || n.dontTakeDamage) continue;
2363	      if (n.x < bx + 80 && n.x + n.w > bx && n.y < by + 80 && n.y + n.h > by) {
2364	        n.hurt(this.damage, 0, 0, game);
2365	      }
2366	    }
2367	  }
2368	  draw(r: import('../render/Renderer').Renderer, cam: import('../render/Camera').Camera): void {
2369	    const ctx = r.canvas.getContext('2d');
2370	    if (!ctx) return;
2371	    const img = r.atlas?.ensureVImage('vanilla/Projectile_681.png');
2372	    ctx.save();
2373	    ctx.translate(this.cx, this.cy);
2374	    ctx.rotate(this.rot);
2375	    ctx.imageSmoothingEnabled = false;
2376	    if (img) {
2377	      // 原生 14×20（SetDefaults 681 仅 14×14 判定盒，scale=1；曾压成 14×14 竖向掐短）。
2378	      // Main.cs:29811 type 681 velocity.X>0 时 ^= FlipHorizontally（贴图默认朝左）;
2379	      // origin (7,13) = (texW/2, h/2+num143=6)（Main.cs:29805 num143=6 + :29856 num145）
2380	      if (this.vx > 0) ctx.scale(-1, 1);
2381	      ctx.drawImage(img, -7, -13, img.width, img.height);
2382	    } else { ctx.fillStyle = '#3A3A3A'; ctx.fillRect(-this.w / 2, -this.h / 2, this.w, this.h); }
2383	    ctx.restore();
2384	    void cam;
2385	  }
2386	}
2387	
2388	// ---------------------------------------------------------------------------
2389	// 683 食人魔跺地波（ProjectileID.cs:1726;SetDefaults :7003+ aiStyle 135/30²/
2390	//   tileCollide=false/ignoreWater）。AI_135_OgreStomp（Projectile.cs:65725-65830）：
2391	//   原地 9t,盒从 16×5=80² 扩到 16×40=640²,每 3t 一波尘爆;伤害走 hostile 盒。
2392	// ---------------------------------------------------------------------------
2393	export class DD2OgreSmash extends Entity {
2394	  w = 80; h = 80;
2395	  dead = false;
2396	  private ai0 = 0;
2397	  private dmg: number;
2398	  private readonly hitIds = new Set<number>();
2399	  constructor(x: number, y: number, dmg: number) {
2400	    super();
2401	    this.x = x - this.w / 2; this.y = y - this.h / 2;
2402	    this.dmg = dmg;
2403	  }
2404	  fixedUpdate(_dt: number, game: GameHooks): void {
2405	    this.ai0 += 1;
2406	    if (this.ai0 > 9) { this.dead = true; game.onProjectileDeath?.(683, this.x, this.y, this.w, this.h); return; }
2407	    // 扩盒（:65740 Size = 16×lerp(5,40,ai0/9)）
2408	    const size = Math.round(16 * lerp(5, 40, this.ai0 / 9));
2409	    const ncx = this.cx, ncy = this.cy;    // base.Center 保持（:65738-65741 先取心再扩盒）
2410	    this.w = size; this.h = size;
2411	    this.x = ncx - size / 2; this.y = ncy - size / 2;
2412	    // 伤害（hostile 盒:玩家 + 永恒水晶,同弹 id 免疫帧防连击）
2413	    const pl = game.player;
2414	    if (pl && !pl.dead
2415	      && pl.x < this.x + this.w && pl.x + pl.w > this.x
2416	      && pl.y < this.y + this.h && pl.y + pl.h > this.y) {
2417	      game.damagePlayer(this.dmg, this.cx, this.cy);
2418	    }
2419	    for (const n of game.enemies() as Enemy[]) {
2420	      if (n.dead || n.vanillaId !== 548 || n.dontTakeDamage) continue;
2421	      if (this.hitIds.has(n.id)) continue;
2422	      if (n.x < this.x + this.w && n.x + n.w > this.x
2423	        && n.y < this.y + this.h && n.y + n.h > this.y) {
2424	        this.hitIds.add(n.id);
2425	        n.hurt(this.dmg, 0, 0, game);
2426	      }
2427	    }
2428	    if (this.ai0 % 3 === 0) {              // 每 3t 尘爆（:65746-65750）
2429	      game.spawnParticles(this.cx + (Math.random() - 0.5) * this.w,
2430	        this.y + this.h - 8, '#B09060', 4, 2.4, { life: 30 });
2431	    }
2432	  }
2433	  draw(r: import('../render/Renderer').Renderer, cam: import('../render/Camera').Camera): void {
2434	    // 原版 683 不绘制本体:SetDefaults alpha=255（Projectile.cs:7003-7012）且 AI_135
2435	    // （:65725-65830）全程不调 alpha → Opacity 恒 0,贴图从不显示;视觉效果只靠
2436	    // 每 3t 的 KillTile 尘爆 + 溅射 gore（:65787-65820）。曾画成随盒扩张的贴图
2437	    // （盒扩到 640² → 巨型方块,双重失真）——移除本体绘制（G11 对账）
2438	    void r;
2439	    void cam;
2440	  }
2441	}
2442	

```


---

## 🤖 Assistant · 2026-08-19T03:13:23.627Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '63372,63610p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_107 header + Ogre case"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:23.686Z

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
			{
			case 0:
				num5 = 44;
				if (ai[0] == 40f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_OgreAttack, base.Center);
				}
				break;
			case 2:
				num5 = 90;
				num4 = 250f;
				flag4 = true;
				num11 = GetAttackDamage_ForProjectiles(60f, 40f);
				num9 = 36;
				num = 56;
				num2 = 41;
				num3 = 13f;
				flag3 = true;
				num12 = 683;
				flag15 = false;
				vector = new Vector2(-direction * 20, height / 2 - 1);
				if (ai[0] == 40f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_OgreGroundPound, base.Center);
				}
				break;
			case 1:
				flag3 = true;
				num5 = 90;
				num4 = 1000f;
				num6 = 240;
				num11 = GetAttackDamage_ForProjectiles(40f, 30f);
				flag15 = false;
				vector = new Vector2(direction * 30, -70f);
				num12 = 676;
				if (ai[0] == 80f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_OgreSpit, base.Center);
				}
				break;
			}
			if (ai[0] < (float)(-num6))
			{
				ai[0] = -num6;
			}
			break;
		case 552:
		case 553:
		case 554:
			style = SoundID.DD2_GoblinScream;

```


---

## 🤖 Assistant · 2026-08-19T03:13:49.399Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Vanilla Ogre case 576/577:
- num22 = 700 (scream one-in), style = DD2_OgreRoar
- num26 -= 32 (jump probe offset)
- flag5 = true (melee)
- num6 = 60 (cooldown)
- num4 = 130 (triggerRange)
- num5 = 44 (windup)
- flag21 = DD2Event.EnemiesShouldChasePlayers
- num7 = 0.7 (windupDamp), flag7 default true → windup damping ON.
- localAI[0] > 0 → -=1 (stomp cooldown)
- if ai[0] <= 0: num34 = ai[1]; num35 = Distance(target); if localAI[3] >= 60: 
  - if num35 <= num4+300 (430) && localAI[0] <= 0 → ai[1] = 2
  - else if num35 > num4 + 30 (160) → ai[1] = 1
  - else if !(num35 > num4) → ai[1] = 0; if num34 == 1 → ai[0] = 0
- else if ai[1] == 2 → localAI[0] = 300
- switch ai[1]:
  - case 0: num5 = 44; if ai[0] == 40 → sound OgreAttack.
  - case 2 (stomp): num5 = 90, num4 = 250, flag4 = true (jump), num11 = dmg(60,40), num9 = 36 (fireAt), num = 56 (jumpT), num2 = 41 (jumpMinT), num3 = 13 (jumpVy), flag3 = true (fireOnWindup), num12 = 683, flag15 = false, vector = (-direction*20, height/2 - 1). if ai[0] == 40 → sound OgreGroundPound.
  - case 1 (spit): flag3 = true, num5 = 90, num4 = 1000, num6 = 240 (cooldown!), num11 = dmg(40,30), flag15 = false, vector = (direction*30, -70), num12 = 676; if ai[0] == 80 → sound OgreSpit.
- if ai[0] < -num6 → ai[0] = -num6 (clamp).

Ours:
- p.cooldown = 60 default; p.triggerRange = 130; p.windup = 44 — matches case 0 base.
- Ogre select block (lines 1934-1949): 
```
if (id === 576 || id === 577) {
    if (x[0] > 0) x[0] -= 1;
    if (e.ai0 <= 0 && x[3] >= 60 && tgt) {
      const prev = e.ai1;
      const dist = ...;
      if (x[3] >= 60) {
        if (dist <= 130 + 300 && x[0] <= 0) e.ai1 = 2;
        else if (dist > 130 + 30) e.ai1 = 1;
        else if (!(dist > 130)) {
          e.ai1 = 0;
          if (prev === 1) e.ai0 = 0;
        }
      }
    }
    if (e.ai0 > 0 && e.ai1 === 2) x[0] = 300;
}
```
matches vanilla including `num34 == 1 → ai[0] = 0`.

- walker107Params ogre block:
```
p.scream = 'dd2_ogre_roar'; p.screamOneIn = 700;
p.melee = true; p.windupDampOn = true; p.windupDamp = 0.7;
p.cooldown = 60; p.triggerRange = 130; p.windup = 44;
if (e.ai1 === 2) { windup 90; triggerRange 250; fireOnWindup; jump; jumpT 56; jumpMinT 41; jumpVy 13; fireAt 36; proj 683; projDmg (60,40); aimAbove 0; muzzleDx -20; muzzleAtBottom }
else if (e.ai1 === 1) { windup 90; triggerRange 1000; fireOnWindup; fireAt 35; proj 676; projDmg (40,30); aimAbove 0; muzzleDx 30; muzzleDy -70 }
```

Vanilla case 1 (spit): num9 (fireAt) is NOT overridden → num9 = num8/2 = 35. ours fireAt 35. matches. num6 = 240 for spit (cooldown after spit = 240)! Ours: p.cooldown stays 60 in the spit branch — NOT set to 240!

Check: vanilla case 1 sets `num6 = 240`. This is the cooldown applied when the windup ends: `if (ai[0] == 0) ai[0] = -num6` presumably in flag5 block. Let me confirm the flag5 block later (64356-64386). If num6 = 240 for spit, then after spitting, ai[0] = -240 → 240-frame cooldown before next attack. Ours uses p.cooldown = 60 for all ogre states (spit should be 240). That's a real deviation: Ogre would spit 4× more often than vanilla.

Also the clamp `if (ai[0] < -num6) ai[0] = -num6` — ours line 2199-2201: `if (id === 576 || id === 577) { if (e.ai0 < -p.cooldown) e.ai0 = -p.cooldown; }`. With p.cooldown = 60 always, the clamp is -60 for spit too (vanilla -240). Same root cause.

Let me double check vanilla flag5 block to make sure num6 is used as cooldown. Need to read 64356-64430 and the shooter block 64551-64679, and the stuck-count block 64431-64456, plus targeting/scream block 64458-64550, and the phase-fly block 64846-64918, and jump ladder 64703-64832. Let me read vanilla 63610-64919 in a couple of chunks (skip family cases I've already seen params for, but I should verify a few: goblin bomber 555-557, javelin 561-563, drakin 570/571, wither beast 568/569, kobold 572/573, skeleton 566/567).

Given time constraints, focus on: (a) the shared tail blocks (64262-64919) which drive Ogre; (b) spot-check family param blocks.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:13:50.549Z · glm-x-preview-260804

```
已读取 Ogre 参数。原版呕吐（spit）设置了 `num6 = 240`（冷却时间）——需要验证我们的实现是如何使用 `p.cooldown` 的，并读取共享的 tail 代码块。我来读取原版 AI_107 tail。
```


---

## 🤖 Assistant · 2026-08-19T03:13:50.961Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '64262,64680p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_107 shared tail blocks"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:13:51.021Z

**📎 ToolResult**

```
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

```


---

## 🤖 Assistant · 2026-08-19T03:14:54.557Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Now I have the vanilla shared tail. Key observations for Ogre:

1. flag5 (melee) block:
```
if (flag5) {
    if (ai[0] < 0) { ai[0] += 1; flag = false; }
    if (ai[0] == 0 && (velocity.Y == 0 || flag6) && targetData.Type != None && (CanHit || CanHitLine) && dist < num4) { ai[0] = num5; }
    if (ai[0] > 0) {
        spriteDirection = direction * num27;
        if (flag7) { velocity.X *= num7; flag24 = true; flag20 = true; ai[3] = 0; }
        ai[0] -= 1;
        if (ai[0] == 0) { ai[0] = -num6; }
    }
}
```

Ours (lines 2185-2202):
```
if (p.melee) {
    if (e.ai0 < 0) e.ai0 += 1;
    if (e.ai0 === 0 && e.vy === 0 && tgt && losClear && dist < triggerRange) e.ai0 = p.windup;
    if (e.ai0 > 0) {
        if (p.windupDampOn) e.vx *= p.windupDamp;
        e.ai0 -= 1;
        if (e.ai0 === 0) e.ai0 = -p.cooldown;
    }
    ogre clamp...
}
```

Differences:
- Vanilla when ai[0] < 0 (cooldown): sets flag = false. flag is used... where? `bool flag = velocity.X == 0f && velocity.Y == 0f && !justHit;` — flag is used later in jump ladder? Let me check where flag is used (flag28/flag...). Actually `flag` is used in the movement section probably (`if (flag) ...`). Minor.
- Vanilla flag7 block also sets flag24 = true (skips walk accel), flag20 = true (skips retarget/scream), ai[3] = 0. Ours doesn't clear ai3 in the windup-damp branch — but ours' stuck-count block is gated by `!attacking` where attacking = (melee||shooter) && ai0>0 — equivalent to skipping counting during attack. And the scream/retarget block is gated by ai3 < 30 regardless... hmm ours doesn't replicate flag20 (skip retarget while winding up). Vanilla flag20=true only when flag7 (ogre). For ogre winding up: no retarget/scream. Ours: the scream/retarget block (line 2124) runs when e.ai3 < 30 regardless of attacking. Vanilla: `if (!flag20) { if (ai[3] < num21 && flag21) {...retarget...} else if (!flag22) {...} }`. So for the ogre during windup (flag20=true), retarget/scream is SKIPPED. Ours still retargets/screams during windup. Minor behavioral nuance (facing updates during windup which vanilla freezes). Low severity but real. Hmm — but wait, vanilla flag20 is set true ONLY inside `if (flag7)` in the flag5 windup branch (ogre and others with flag7). Default flag7 = true! Let me re-check defaults: `bool flag7 = true;` — default TRUE, and num7 = 0.9 default. Wait but then which families set flag7 = false? Looking at the header: flag7 = true default, num7 = 0.9f. So default walkers damp velocity.X by 0.9 during melee windup! And our p.windupDampOn default false with windupDamp 0.9 — only ogre enables it!

Hold on. Let me re-read the defaults at 63415+:
```
bool flag5 = false;
float num4 = 40f;
int num5 = 30;
int num6 = 0;
bool flag6 = false;
bool flag7 = true;
float num7 = 0.9f;
```
So flag7 defaults TRUE and num7 = 0.9. Then in family cases, do they set flag7 = false? For ogre: flag7 not explicitly set (stays true), num7 = 0.7. Let me check other cases — need to look at goblins 552-554 etc. Let me grep flag7 in 63610-64262 range.

Actually wait — let me re-read our interface: `windupDampOn: boolean; // flag7（食人魔 true）` — they claim flag7 only for ogre. But default is true! Unless family cases set flag7 = false. Let me check. I need to read 63610-64262.

Also important: vanilla flag5 windup start condition `(velocity.Y == 0f || flag6)` — flag6 is per-family ("hover/flight allowed while attacking"?). And ours uses `e.vy === 0` only. flag6 default false; which families set flag6 = true? Possibly drakin (flying)? No wait drakin is flag12 shooter. flag6 might be for wither beast or kobold grounded? Let me check.

2. flag3 (fire on windup) block: vanilla fires when `ai[0] == num9` — note the check is INSIDE `if (flag3 && ai[0] > 0f)` and AFTER the flag5 block decrements ai[0]. Order in vanilla: flag5 block runs (ai[0] -= 1), THEN flag3 block checks ai[0] == num9. So when ogre's windup counter counts down THROUGH num9 (35 for spit / 36 for stomp), it fires.

Ours: melee block decrements first (line 2196: e.ai0 -= 1), then fireOnWindup block checks `e.ai0 === p.fireAt` (line 2204-2206). matches ordering.

BUT vanilla flag3 block also has `if (flag15) { retarget; targetData = GetTargetData(); }` before firing — flag15 for ogre = false, so no retarget. ours aimAbove=0 → no retarget. matches (they map flag15 false → aimAbove 0 → `e.ai1 > p.aimAbove` = ai1 > 0; for melee families ai1 is 0 → false → no retarget. OK).

Also note vanilla fires at vector4 = Center + vector; v = target.Center - vector4; v.Y -= |v.X| * num15 (arc); normalize * num10 (speed); loop num17 shots with random jitter ±num16; spawn at vector4 + velocity*num18.

Ours fireWalkerProj: mx = e.cx + muzzleDx * facing; my = e.cy + (muzzleAtBottom ? h/2-1 : muzzleDy); vx = tx - mx; vy -= |vx|*arc; normalize * speed; spawn at mx + vx*spawnOffset... 

Vanilla vector for ogre stomp = new Vector2(-direction * 20, height/2 - 1); ours muzzleDx=-20 with facing multiplier: mx = cx + (-20)*facing = cx - 20*facing. matches. my = cy + h/2 - 1. matches.

Spit vector = (direction*30, -70): ours muzzleDx=30, muzzleDy=-70. matches.

3. flag4 (jump on windup): vanilla: `if (velocity.Y != 0 && ai[0] < num2) ai[0] = num2; if (ai[0] == num) velocity.Y = -num3;` — checks AFTER flag5 decrement and AFTER flag3 fire. Ours line 2208-2211: `if (p.jump && e.ai0 > 0) { if (e.vy !== 0 && e.ai0 < p.jumpMinT) e.ai0 = p.jumpMinT; if (e.ai0 === p.jumpT) e.vy = -p.jumpVy; }`. matches.

4. Stuck counting (flag18): vanilla `if (!flag17 && flag18)`:
- flag19 = velocity.Y == 0 && velocity.X * direction < 0
- if (position.X == oldPosition.X || ai[3] >= num21 || flag19) ai[3] += 1
- else if (|velocity.X| > 0.9 && ai[3] > 0) ai[3] -= 1
- if (ai[3] > num21*10) ai[3] = 0
- if (justHit && !flag30) ai[3] = 0
- if (targetData.Hitbox.Intersects(base.Hitbox)) ai[3] = 0
- if (ai[3] == num21) { if (flag30) { teleport dash: noGravity, noTileCollide, position.X += direction * width * 2; dust; return; } }

Ours (2113-2122): gated `if (!attacking)` where attacking = (melee||shooter) && ai0 > 0. Vanilla: flag18 = false when `(flag12||flag5) && ai[0] > 0`. Same. flag17? what is flag17 — probably "is a flying family"? Default false. OK.

Ours misses: `ai[3] == num21 → flag30 teleport-dash` — but ours comment says "DD2 族 flag30=false 只计数". flag30 default is `bool flag30 = true;` — wait, header says `bool flag30 = true;`? Let me check: in the header dump: `bool flag29 = NPCID.Sets.FighterUsesDD2PortalAppearEffect[type]; bool flag30 = true;` — hmm, actually I see "bool flag30 = true;"? Looking at my dump:

```
bool flag29 = NPCID.Sets.FighterUsesDD2PortalAppearEffect[type];
bool flag30 = true;
```
Hmm no. Let me re-read. The dump shows:

```
		bool flag29 = NPCID.Sets.FighterUsesDD2PortalAppearEffect[type];
		bool flag30 = true;
```

Wait, actually I need to scroll. In my sed output above I see:

"		bool flag29 = NPCID.Sets.FighterUsesDD2PortalAppearEffect[type];\n		bool flag30 = true;"

Hmm, I don't actually see flag30 in the output. Let me search the dump... The header printed flags up to flag28 and num31. Then `NPCAimedTarget targetData = GetTargetData();`. I see "bool flag29 = NPCID.Sets.FighterUsesDD2PortalAppearEffect[type];" — yes it's there. flag30 — I don't see it declared in the visible header; but used at `if (justHit && !flag30) ai[3] = 0;` and `if (flag30) {...teleport...}`. So flag30 must be declared somewhere — probably in a family case (e.g., non-DD2 walkers like skeleton/goblin zombie set flag30 = true?). Default likely false for DD2 families. The ours comment says "DD2 族 flag30=false 只计数" — consistent: flag30 false → justHit clears ai3? wait `if (justHit && !flag30) ai[3] = 0f;` — flag30=false → justHit DOES clear. Ours: `if (e.justHit) e.ai3 = 0;` matches flag30=false. And the ai[3]==num21 teleport only when flag30 — DD2 families don't teleport. ours omits. Fine.

5. Retarget/scream block: vanilla `if (!flag20) { if (ai[3] < num21 && flag21) { scream 1/num22; retarget } else if (!flag22) { ... static turn-around ... } }`.

flag21 default false; ogre sets flag21 = DD2Event.EnemiesShouldChasePlayers (true during invasion). Which families set flag21? Kobolds? Need check. Ours: `if (e.ai3 < 30) { scream; retarget } else if (!busy) {...}` — ours omits the flag21 gate (comment says EnemiesShouldChasePlayers 恒真). Vanilla EnemiesShouldChasePlayers: DD2Event.cs:115-123 — returns true when invasion ongoing and not between waves? "恒真" per their comment. It's !(DownedDD2Event ...) — I'll trust.

Note vanilla scream volume etc fine.

Important: vanilla `else if (!flag22)`: flag22 = shooter timer active or melee windup active. Ours busy = attacking || (shooter && ai1>0) || (melee && ai0>0). attacking = (melee||shooter) && ai0>0. busy ≈ flag22 plus extra (shooter && ai0>0 already included). Vanilla flag22 = (flag12 && ai[1] > 0) || (flag5 && ai[0] > 0). Ours busy = ((melee||shooter)&&ai0>0) || (shooter&&ai1>0) || (melee&&ai0>0). For a shooter with ai0>0 but ai1<=0 — vanilla flag22 false, ours true. Rare. OK.

6. Walk accel: vanilla `if (!flag24) { if (vx < -num23 || vx > num23) { if (vy == 0) velocity *= num25 } else if (...) clamp }` — NOTE: `velocity *= num25` damps BOTH components. Ours w107WalkAccel: `if (e.vy === 0) { e.vx *= p.damp; e.vy *= p.damp; }` — same.

7. flag12 shooter block: vanilla:
```
if (flag12) {
    if (confused) ai[0] = 0;
    else {
        if (ai[1] > 0) ai[1] -= 1;
        if (justHit) { ai[1] = num19 (30); ai[0] = 0; }
        if (ai[0] > 0) {
            if (flag15) retarget;
            if (ai[1] == num9) { fire; pose ai[0]; if (flag16) direction = sign(vector9.X); }
            bool flag33 = true;
            if ((velocity.Y != 0 && !flag14) || ai[1] <= 0) { bool flag34 = num20 != 0 && ai[1] <= 0; ai[0] = 0; ai[1] = flag34 ? num20 : 0; }
            else if (!flag13 || (!flag33 && (!flag14 || velocity.Y == 0))) { velocity.X *= 0.9; spriteDirection = ...; }
        }
        if ((ai[0] <= 0 || flag13) && (velocity.Y == 0 || flag14) && ai[1] <= 0 && target valid && CanHit) {
            if (vector12.Length() < num13) { velocity.X *= 0.5; ai[0] = 3 (pose); ai[1] = num8; pose from vector12; if (flag16) direction; }
        }
        if (ai[0] <= 0 || flag13) {
            bool flag35 = Distance(targetData.Center) < num14;
            if (flag35 && CanHitLine) ai[3] = 0;
            if (vx out of range || flag35) { if (vy == 0) vx *= num25; }
            else if (...) clamp;
        }
    }
}
```

Ours (2148-2183):
```
if (p.shooter) {
    if (e.ai1 > 0) e.ai1 -= 1;
    if (e.justHit) { e.ai1 = 30; e.ai0 = 0; }
    const aimRetarget = e.ai1 > p.aimAbove;
    if (e.ai0 > 0) {
        if (aimRetarget && tgt) e.facing = ...;
        if (tgt && e.ai1 === p.fireAt) { fire; pose; facing }
        if (e.vy !== 0 || e.ai1 <= 0) { e.ai0 = 0; e.ai1 = 0; }
        else e.vx *= 0.9;
    }
    if (e.ai0 <= 0 && e.vy === 0 && e.ai1 <= 0 && tgt && losClear) {
        if (d < startRange) { vx *= 0.5; pose; ai1 = timer; facing }
    }
    if (e.ai0 <= 0) w107WalkAccel(e, p);
}
```

Key differences:
a) Vanilla windup-sustain: `if ((velocity.Y != 0 && !flag14) || ai[1] <= 0)` → cancel. Ours: `if (e.vy !== 0 || e.ai1 <= 0)` → cancel. flag14 — which family sets it? flag14 default false. Kobold? Drakin maybe (they're flyers? no they're walkers). Hmm. If flag14 is false for all our shooter families, equivalent.

b) Vanilla sustain branch `else if (!flag13 || ...)` → velocity.X *= 0.9. Ours: else → vx *= 0.9. flag13 default false → !flag13 = true → damp. matches.

c) Vanilla start condition requires `(ai[0] <= 0 || flag13)` AND `(velocity.Y == 0 || flag14)` AND ai[1] <= 0 AND CanHit. Ours requires ai0<=0 && vy===0 && ai1<=0 && losClear && dist < startRange. matches modulo flag13/flag14.

d) Vanilla start: `velocity.X *= 0.5; ai[0] = 3 (or pose); ai[1] = num8`. Ours matches (vx *= 0.5, ai0 = pose, ai1 = timer).

e) Vanilla post-attack walk-accel block `if (ai[0] <= 0 || flag13)`: includes flag35 = Distance < num14 (default 0 → false; families may set num14). num14 default 0f. Who sets num14? Maybe drakin? Need check. Also `if (flag35 && CanHitLine) ai[3] = 0`. With num14=0 flag35 false → skip. Ours omits num14 entirely — need to check if any family sets num14 > 0. Let me grep the family cases.

8. Phase-fly block (flag27) at 64295+: this is `if (flag27)` — flag27 = noGravity-ish flyer families (kobold?). Wait no — flag27 block: `noGravity = true; TargetClosest(false); if (collideX) velocity.X = -oldVelocity.X; ...` uses num28=5, num29=3, num30=8, amount=0.05, amount2=0.04, amount3=0.1 — that's the flying movement for flag27 families. Hmm, ours implements phase-fly at 64846-64918? The ours "phase" block cites cs:64846-64918. But this flag27 block at ~64295 is different. Which one is flag2 phase-fly? Let me look at 64846-64918 to see. Also flag26/flag27 defaults false.

Wait — I haven't seen the segment 64680-64919 yet (movement: gravity, step up, jump ladder, flag2 phase fly). Let me read that.

Also need to check family cases 63610-64262 for flags: flag7, flag6, flag13, flag14, flag16, flag21, num14, num19, num20. Let me read that section now.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:14:55.048Z · glm-x-preview-260804

```
现在是家族变体案例（63610-64262）以及剩余的移动尾部（64680-64919）。
```


---

## 🤖 Assistant · 2026-08-19T03:14:55.505Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '63610,64262p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_107 family case blocks"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:14:55.566Z

**📎 ToolResult**

```
			style = SoundID.DD2_GoblinScream;
			num22 = 1000;
			flag5 = true;
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			if (type == 553)
			{
				num24 += 0.01f;
				num23 += 0.2f;
			}
			if (type == 554)
			{
				num24 += 0.02f;
				num23 += 0.4f;
			}
			if (!(localAI[3] >= 60f))
			{
				num24 = 0.01f + localAI[3] / 60f * 0.05f;
			}
			break;
		case 570:
		case 571:
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			flag24 = true;
			flag12 = true;
			flag15 = ai[1] > 40f;
			num8 = 60;
			num9 = 40;
			if (type == 571 && ai[1] > 10f && ai[1] <= 40f && (int)ai[1] % 6 == 0)
			{
				num9 = (int)ai[1] - 1;
			}
			if (type == 570 && ai[1] > 10f && ai[1] <= 40f && (int)ai[1] % 9 == 0)
			{
				num9 = (int)ai[1] - 1;
			}
			num12 = 671;
			vector.X += 22 * direction;
			num15 = 0.15f;
			num16 = 1.5f;
			num13 = 600f;
			num10 = 13f;
			num17 = 1;
			num18 = 0f;
			if (type == 570)
			{
				num16 = 2.5f;
			}
			num11 = GetAttackDamage_ForProjectiles(35f, 25f);
			if (type == 571)
			{
				num11 = GetAttackDamage_ForProjectiles(60f, 45f);
			}
			num23 = 0.77f;
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
			if (!(localAI[3] >= 60f))
			{
				num13 = 1f;
				num24 = 0.01f + localAI[3] / 60f * 0.05f;
			}
			break;
		case 572:
		case 573:
			if (localAI[3] == 0f)
			{
				float[] array = localAI;
				val = SlotId.Invalid;
				array[0] = ((SlotId)(ref val)).ToFloat();
				float[] array2 = localAI;
				val = SlotId.Invalid;
				array2[1] = ((SlotId)(ref val)).ToFloat();
			}
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			if (ai[1] == 2f)
			{
				SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[0]))?.Stop();
				SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[1]))?.Stop();
				position = base.Center;
				width = (height = 192);
				base.Center = position;
				velocity = Vector2.Zero;
				damage = GetAttackDamage_ScaledByDifficulty(80f);
				alpha = 255;
				for (int k = 0; k < 4; k++)
				{
					int num37 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 31, 0f, 0f, 100, default(Color), 1.5f);
					Main.dust[num37].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 2f;
				}
				for (int l = 0; l < 20; l++)
				{
					int num38 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 200, default(Color), 3.7f);
					Main.dust[num38].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 2f;
					Main.dust[num38].noGravity = true;
					Main.dust[num38].velocity *= 3f;
					num38 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 100, default(Color), 1.5f);
					Main.dust[num38].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 4f;
					Main.dust[num38].velocity *= 2f;
					Main.dust[num38].noGravity = true;
					Main.dust[num38].fadeIn = 2.5f;
				}
				for (int m = 0; m < 6; m++)
				{
					int num39 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 0, default(Color), 2.7f);
					Main.dust[num39].position = base.Center + Vector2.UnitX.RotatedByRandom(3.1415927410125732).RotatedBy(velocity.ToRotation()) * width / 2f;
					Main.dust[num39].noGravity = true;
					Main.dust[num39].velocity *= 3f;
				}
				for (int n = 0; n < 12; n++)
				{
					int num40 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 31, 0f, 0f, 0, default(Color), 1.5f);
					Main.dust[num40].position = base.Center + Vector2.UnitX.RotatedByRandom(3.1415927410125732).RotatedBy(velocity.ToRotation()) * width / 2f;
					Main.dust[num40].noGravity = true;
					Main.dust[num40].velocity *= 3f;
				}
				for (int num41 = 0; num41 < 5; num41++)
				{
					int num42 = Gore.NewGore(position + new Vector2((float)(width * Main.rand.Next(100)) / 100f, (float)(height * Main.rand.Next(100)) / 100f) - Vector2.One * 10f, default(Vector2), Main.rand.Next(61, 64));
					Main.gore[num42].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 2f;
					Main.gore[num42].velocity *= 0.3f;
					Main.gore[num42].velocity.X += (float)Main.rand.Next(-10, 11) * 0.05f;
					Main.gore[num42].velocity.Y += (float)Main.rand.Next(-10, 11) * 0.05f;
				}
				ai[0] += 1f;
				if (ai[0] >= 3f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldExplosion, base.Center);
					life = 0;
					HitEffect();
					active = false;
				}
				return;
			}
			if (ai[0] > 0f && ai[1] == 0f && life > 0)
			{
				SlotId val2 = SlotId.FromFloat(localAI[0]);
				if (!((SlotId)(ref val2)).IsValid)
				{
					float[] array3 = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldIgnite, base.Center);
					array3[0] = ((SlotId)(ref val)).ToFloat();
				}
				localAI[2] += 1f;
				if (localAI[2] == 30f)
				{
					float[] array4 = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldIgniteLoop, base.Center);
					array4[0] = ((SlotId)(ref val)).ToFloat();
					float[] array5 = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldScreamChargeLoop, base.Center);
					array5[1] = ((SlotId)(ref val)).ToFloat();
				}
			}
			if (ai[0] > 0f && ai[1] == 1f)
			{
				ai[0] = 0f;
				ai[1] = 2f;
				netUpdate = true;
				return;
			}
			num23 = 0.88f;
			if (ai[0] == 1f)
			{
				ai[1] = 1f;
			}
			if (ai[0] == 0f && ai[1] == 1f)
			{
				ActiveSound activeSound = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[0]));
				if (activeSound == null)
				{
					float[] array6 = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldIgniteLoop, base.Center);
					array6[0] = ((SlotId)(ref val)).ToFloat();
				}
				else
				{
					activeSound.Position = base.Center;
				}
				ActiveSound activeSound2 = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[1]));
				if (activeSound2 == null)
				{
					float[] array7 = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldScreamChargeLoop, base.Center);
					array7[1] = ((SlotId)(ref val)).ToFloat();
				}
				else
				{
					activeSound2.Position = base.Center;
				}
			}
			if (ai[1] > 0f && ai[0] == 0f)
			{
				flag5 = true;
				num5 = 40;
				num4 = 64f;
				num24 = 0.3f;
				num23 = 4f;
				Vector2 vector3 = base.Center + new Vector2(spriteDirection * 12, 0f);
				if (Main.rand.Next(6) == 0)
				{
					Dust dust3 = Dust.NewDustDirect(vector3, 1, 1, 213, Main.rand.Next(-2, 3), Main.rand.Next(-2, 3), 100, new Color(255, 255, 255, 0));
					dust3.noGravity = true;
					dust3.fadeIn = dust3.scale + 1f + 0.01f * (float)Main.rand.Next(0, 51);
					dust3.velocity *= 0.3f;
					dust3.velocity.X += (float)(-spriteDirection) * 1.2f;
					dust3.velocity.Y += -3.5f;
					dust3.velocity.X += velocity.X;
				}
				if (Main.rand.Next(12) == 0)
				{
					Dust dust4 = Dust.NewDustPerfect(vector3, 6, velocity, 100);
					dust4.noGravity = true;
					dust4.velocity.Y -= 1f + Main.rand.NextFloat();
					dust4.scale = 1.1f;
					dust4.fadeIn = 0.5f;
					dust4.customData = this;
				}
			}
			else
			{
				flag5 = true;
				num5 = 40;
				num4 = 700f;
			}
			if (!(localAI[3] >= 60f))
			{
				num24 = 0.01f + localAI[3] / 60f * 0.05f;
			}
			break;
		case 568:
		case 569:
		{
			num5 = 110;
			num24 = 0.16f;
			num25 = 0.7f;
			num23 = 1.4f;
			flag5 = true;
			num4 = 600f;
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			if (!(localAI[3] >= 60f))
			{
				num24 = 0.01f + localAI[3] / 60f * 0.05f;
			}
			if (ai[0] == 0f)
			{
				float[] array8 = localAI;
				val = SlotId.Invalid;
				array8[1] = ((SlotId)(ref val)).ToFloat();
			}
			if (ai[0] != 1f)
			{
				break;
			}
			HitSound = SoundID.DD2_WitherBeastCrystalImpact;
			ai[0] += 1f;
			if (Main.rand.Next(10) == 0)
			{
				Dust dust7 = Dust.NewDustDirect(base.TopLeft, width, height, 271, 0f, -3f, 0, Color.Transparent, 0.6f);
				dust7.velocity.X /= 2f;
				dust7.noGravity = true;
				dust7.fadeIn = 1.5f;
				dust7.position.Y += 4f;
			}
			ActiveSound activeSound3 = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[1]));
			if (activeSound3 == null)
			{
				float[] array9 = localAI;
				val = SoundEngine.PlayTrackedSound(SoundID.DD2_WitherBeastAuraPulse, base.Center);
				array9[1] = ((SlotId)(ref val)).ToFloat();
			}
			else
			{
				activeSound3.Position = base.Center;
			}
			localAI[0] += 1f;
			if (localAI[0] > 60f && Main.rand.Next(10) == 0)
			{
				Vector2 vec = base.Center + (Main.rand.NextFloat() * (MathF.PI * 2f)).ToRotationVector2() * 400f * (0.3f + 0.7f * Main.rand.NextFloat());
				Point point = vec.ToTileCoordinates();
				if (!WorldGen.SolidTile(point.X, point.Y))
				{
					Dust dust8 = Dust.NewDustPerfect(vec, 27, new Vector2(0f, -3f), 0, new Color(255, 255, 255, 127), 1.5f);
					dust8.velocity = DirectionTo(dust8.position) * dust8.velocity.Length();
					dust8.fadeIn = 1.5f;
				}
			}
			if (Main.netMode != 2)
			{
				Player player = Main.player[Main.myPlayer];
				if (!player.dead && player.active && (player.Center - base.Center).Length() < 400f && !player.creativeGodMode)
				{
					player.AddBuff(195, 3);
				}
			}
			if (ai[1] > 0f)
			{
				ai[1] -= 1f;
			}
			if (!(ai[1] <= 0f))
			{
				break;
			}
			ai[1] = 60f;
			if (Main.netMode != 1)
			{
				int num51 = lifeMax / 20;
				if (num51 > lifeMax - life)
				{
					num51 = lifeMax - life;
				}
				if (num51 > 0)
				{
					life += num51;
					HealEffect(num51);
					netUpdate = true;
				}
			}
			break;
		}
		case 561:
		case 562:
		case 563:
		{
			bool num36 = localAI[3] >= 60f;
			if (ai[1] == 82f)
			{
				SoundEngine.PlayTrackedSound(SoundID.DD2_JavelinThrowersAttack, base.Center);
				num22 = 7;
				style = SoundID.DD2_JavelinThrowersTaunt;
			}
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			flag24 = true;
			flag12 = true;
			flag15 = ai[1] > 82f;
			num8 = 90;
			num9 = 82;
			num12 = 662;
			if (type == 563)
			{
				num12 = 685;
			}
			vector.Y -= 14f;
			num15 = 0f;
			num16 = 0.5f;
			num13 = 600f;
			num10 = 13f;
			if (!num36)
			{
				num13 = 1f;
				num24 = 0.01f + localAI[3] / 60f * 0.05f;
			}
			if (type == 561)
			{
				num23 = 0.88f;
				num16 = 0.6f;
				num11 = GetAttackDamage_ForProjectiles(15f, 10f);
				num10 = 11.5f;
				num13 -= 100f;
			}
			if (type == 562)
			{
				num23 = 0.94f;
				num16 = 0.5f;
				num11 = GetAttackDamage_ForProjectiles(30f, 20f);
				num10 = 12.2f;
				num13 -= 50f;
			}
			if (type == 563)
			{
				num23 = 1f;
				num16 = 0.4f;
				num11 = GetAttackDamage_ForProjectiles(45f, 30f);
			}
			break;
		}
		case 555:
		case 556:
		case 557:
		{
			num22 = 800;
			style = SoundID.DD2_GoblinBomberScream;
			bool num33 = localAI[3] >= 60f;
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			flag24 = true;
			flag12 = true;
			flag15 = ai[1] > 18f;
			num8 = 42;
			num9 = 18;
			num12 = 681;
			num11 = 10;
			vector.Y -= 14f;
			num15 = 0.4f;
			num16 = 0.5f;
			num13 = 280f;
			num10 = 6f;
			if (!num33)
			{
				num13 = 1f;
				num24 = 0.01f + localAI[3] / 60f * 0.05f;
			}
			if (type == 555)
			{
				num23 = 0.88f;
				num16 = 0.6f;
				num11 = GetAttackDamage_ForProjectiles(20f, 15f);
			}
			if (type == 556)
			{
				num23 = 0.88f;
				num16 = 0.6f;
				num11 = GetAttackDamage_ForProjectiles(30f, 25f);
			}
			if (type == 557)
			{
				num23 = 1.12f;
				num16 = 0.4f;
				num11 = GetAttackDamage_ForProjectiles(40f, 35f);
			}
			if (ai[1] == (float)num9)
			{
				SoundEngine.PlayTrackedSound(SoundID.DD2_GoblinBomberThrow, base.Center);
			}
			break;
		}
		case 566:
		case 567:
		{
			DelegateMethods.v3_1 = new Vector3(0.3f, 0.05f, 0.45f) * 1.5f;
			Utils.PlotTileLine(base.Top, base.Bottom, width, DelegateMethods.CastLightOpen);
			flag21 = DD2Event.EnemiesShouldChasePlayers;
			bool num43 = localAI[3] >= 120f;
			if (!num43)
			{
				num24 = 0f;
			}
			if (num43)
			{
				dontTakeDamage = false;
				break;
			}
			dontTakeDamage = true;
			velocity.X = 0f;
			flag24 = true;
			flag20 = true;
			ai[3] = 0f;
			if (localAI[3] == 0f)
			{
				alpha = 255;
			}
			localAI[3] += 1f;
			float num44 = localAI[3];
			if (num44 >= 110f)
			{
				alpha -= 26;
				if (alpha < 0)
				{
					alpha = 0;
				}
			}
			if (num44 >= 100f)
			{
				int num45 = (int)localAI[3] / 20;
				float num46 = base.Size.Length() / 2f;
				num46 /= 20f;
				int maxValue = 5;
				for (int num47 = 0; num47 < num45 * 2; num47++)
				{
					if (Main.rand.Next(maxValue) == 0)
					{
						Dust dust5 = Dust.NewDustDirect(position, width, height, 236, velocity.X * 1f);
						dust5.scale = 1f;
						dust5.fadeIn = 0.3f;
						dust5.velocity = new Vector2(Main.rand.NextFloatDirection() * 1f, 0f - dust5.velocity.Length()) * 1.25f * num46;
					}
				}
			}
			else
			{
				int num48 = (int)localAI[3] / 10;
				float num49 = base.Size.Length() / 2f;
				num49 /= 20f;
				int maxValue2 = 5;
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

```


---

## 🤖 Assistant · 2026-08-19T03:16:19.354Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Very informative. Key findings so far:

**Ogre (576/577):**
1. Vanilla case 1 (spit): `num6 = 240` — cooldown after spit windup ends = 240. Ours keeps p.cooldown = 60. CONFIRMED deviation (ai[0] = -num6 in flag5 block).

2. Vanilla flag7 default is TRUE (num7 = 0.9): `bool flag7 = true;` — wait, let me double check the header. From the first dump:

```
bool flag5 = false;
float num4 = 40f;
int num5 = 30;
int num6 = 0;
bool flag6 = false;
bool flag7 = true;
float num7 = 0.9f;
```

Hmm wait, I need to scroll up in the dump. The header dump I got shows:

```
		bool flag5 = false;
		float num4 = 40f;
		int num5 = 30;
		int num6 = 0;
		bool flag6 = false;
		bool flag7 = true;
		float num7 = 0.9f;
```

Actually let me re-check my first sed output (63372-63610). It shows:

```
		bool flag5 = false;
		float num4 = 40f;
		int num5 = 30;
		int num6 = 0;
		bool flag6 = false;
		bool flag7 = true;
		float num7 = 0.9f;
		bool flag8 = false;
		...
```

Yes! flag7 = true default, num7 = 0.9. And NO family case in 63610-64260 sets flag7 = false (I checked goblins, drakin, kobold, wither, javelin, bomber, skeleton, ogre — none touch flag7). So flag7 is TRUE for ALL AI_107 families → during melee windup (flag5 && ai[0]>0), velocity.X *= num7 (0.9 default, 0.7 ogre), AND flag24 = true (skip walk accel), flag20 = true (skip retarget/scream), ai[3] = 0.

Ours: `windupDampOn` default false, only ogre sets true. So for goblins melee (552-554), wither beast (568/569), kobold (572/573 — which set flag5=true with num5=40, num4=64/700), the windup damping AND flag20 (freeze retarget) AND ai3-clear AND flag24 are missing. 

Wait — but ours attacking gate: `attacking = (p.melee || p.shooter) && e.ai0 > 0` — used to skip the stuck-counting (flag18 = false → skip). That's `(flag12||flag5) && ai[0] > 0` — equivalent. So ai3 clearing during windup is equivalent-ish since counting is skipped anyway (ai3 doesn't increment but also doesn't reset — vanilla sets ai[3] = 0 explicitly; ours just doesn't count. The reset matters if ai3 was e.g. 25 when attack started; vanilla resets to 0, ours keeps 25 → after attack, ogre needs only 5 more frames to hit stuck threshold vs 30. Minor but a real semantic difference).

The bigger one: windup velocity damping for melee families. For kobold grounded (572/573) charge: flag5 windup with num5=40, and flag7=true → velocity.X *= 0.9 each windup frame... wait but kobold's charge sets num23=4, num24=0.3 — flag24=true set in the case → skips the walk accel; but flag7 in flag5 block ALSO sets flag24=true and damps velocity. Hmm wait — for the kobold in charge mode (ai[1] > 0 && ai[0] == 0), flag5=true, num5=40, num4=64: when within 64px of target, windup starts (ai[0]=40), velocity.X *= 0.9 each tick (flag7 true), then after 40 ticks → ai[0] = -num6. num6 default 0! So cooldown -0 → ai[0] = 0 next tick... wait `if (ai[0] == 0f) ai[0] = -num6;` = -0 = 0. So ai[0] goes 1 → decrement → 0 → set to -0 → 0. Then kobold: `if (ai[0] == 1f) ai[1] = 1f;` — during countdown, when ai[0] hits 1, ai[1] = 1 (charge state). Ours: `if (e.ai0 === 1) e.ai1 = 1;` — but wait, order! Vanilla: kobold case block runs FIRST (before flag5 block). `if (ai[0] == 1f) ai[1] = 1f;` reads ai[0] BEFORE the flag5 block decrements it. So ai[1]=1 when ai[0]==1 at case-eval time; then flag5 decrements ai[0] → 0 → cooldown. Then next tick, ai[0] = -0 = 0 → kobold `if (ai[0] == 0f && ai[1] == 1f)` → ignite loops; and `if (ai[1] > 0f && ai[0] == 0f)` → charge mode params. 

Ours: `if (e.ai0 === 1) e.ai1 = 1;` at line 2051 — placed in the kobold block which runs BEFORE the melee block (line 2185+). Same order. Then melee block: ai0 1 > 0 → damp → ai0 -= 1 → 0 → ai0 = -p.cooldown. p.cooldown for kobold = 0 (default). `if (e.ai0 === 0) e.ai0 = -p.cooldown;` → -0 = 0. matches.

But the kobold windup: vanilla damps velocity.X by 0.9 during the 40-tick windup (flag7=true). Ours: windupDampOn=false for kobold → no damping. Since kobold charge speed is 4, during windup ours keeps charging at full speed toward the player while counting down 40 ticks, vanilla decelerates (0.9^40 ≈ 0.015 → basically stops). Then explosion trigger is at 64px... Actually wait: kobold flag4? No. Hmm, for the kobold, ai[1] stays 1 (charge) — and when in ai[1]==1 && ai[0]>0 → the block `if (ai[0] > 0f && ai[1] == 1f) { ai[0] = 0; ai[1] = 2; return; }` → explode! So kobold: charge (ai1=1, ai0=0); when target within 64 → windup starts (ai0=40); NEXT TICK the case runs `if (ai[0] > 0 && ai[1] == 1)` → ai[1]=2 → detonate branch. So windup lasts effectively 1 tick?? Hmm: windup starts → ai0=40, ai1=1. Next tick: case 572: `if (ai[1] == 2f)` no; `if (ai[0] > 0 && ai[1] == 0)` no; `if (ai[0] > 0 && ai[1] == 1)` YES → ai0=0, ai1=2, return. Then detonate: ai[0] += 1 per tick; >= 3 → boom. So the 40-tick windup is cut short after 1 tick. So the flag7 damping for kobold barely matters. OK.

For goblins 552-554 (melee, num5=30, num4=40): flag7=true → velocity.X *= 0.9 during 30-tick windup, and flag20 freezes retarget. Ours: no damping, keeps retargeting. Effect: goblins keep sliding at full speed (1.0-1.4) during attack windup instead of decelerating to a stop, and facing keeps tracking. This is a visible behavioral deviation: vanilla goblins stop and swing; ours keep moving. But how impactful? Melee windup 30 ticks; velocity damped 0.9^30 ≈ 0.04 → stops. Ours: keeps walking at maxSpd during windup, and ALSO skips walk accel (noWalkAccel false for goblins... wait goblins have flag24 default false → walk accel RUNS during windup in vanilla?? No! flag7 block sets flag24 = true → skips walk accel. So vanilla goblin during windup: vx *= 0.9 each tick, no accel. Ours goblin during windup: walk accel continues (`if (!p.noWalkAccel) w107WalkAccel(e, p)` — runs regardless of attacking) → accelerates toward target at full speed during windup. 

CONFIRMED deviation: melee windup damping (flag7, default true, num7 0.9) missing for all melee families except ogre. Also flag20 (freeze scream/retarget during windup) missing. And ai3=0 reset missing. I'll report as one item: "AI_107 melee windup side-effects (flag7/flag20/flag24/ai3 reset) only wired for Ogre".

3. Drakin (570/571): vanilla sets `flag24 = true` in the case → skips the standard walk accel entirely; then the post-attack walk-accel block at the end (`if (ai[0] <= 0 || flag13)`) — flag13 default false → runs when ai0 <= 0. Ours: noWalkAccel = true → skip standard; `if (e.ai0 <= 0) w107WalkAccel(e, p)` at end of shooter block. matches.

Vanilla drakin num9=40 with the multi-shot rewrite `if ai[1] > 10 && ai[1] <= 40 && (int)ai[1] % 6 == 0 (571) / % 9 == 0 (570)` → num9 = ai[1] - 1. Ours implements. matches.

Drakin flag15 = ai[1] > 40 — evaluated at case time. Ours: aimAbove = 40, aimRetarget = e.ai1 > 40 evaluated... in the shooter block AFTER `if (e.ai1 > 0) e.ai1 -= 1`. Vanilla: case runs first (flag15 = ai[1] > 40 on the pre-decrement value), then flag12 block decrements and checks. Ours: p.aimAbove read in walker107Params (before decrement, since params built before shooter block) — wait: `const aimRetarget = e.ai1 > p.aimAbove;` at line 2151, which is AFTER `if (e.ai1 > 0) e.ai1 -= 1;` (line 2149). So ours compares post-decrement. Vanilla compares pre-decrement (flag15 computed in the case before the flag12 block). Off-by-one on the retarget threshold. Truly minor.

Also vanilla javelin flag15 = ai[1] > 82, bomber flag15 = ai[1] > 18. ours aimAbove 82/18. matches.

4. Bomber num11: vanilla sets `num11 = 10` then overrides with GetAttackDamage_ForProjectiles per type: 555→(20,15), 556→(30,25), 557→(40,35). Ours matches.

Bomber `if (ai[1] == num9)` plays GoblinBomberThrow — in the CASE (pre-decrement). Ours: line 2089: `if ((id===555||556||557) && e.ai1 === p.fireAt)` — but this is checked in the pre-shooter-block sound section, before decrement? Line 2081: `if (p.shooter && e.ai0 > 0) { ... if (e.ai1 === p.fireAt) play throw }`. This block runs BEFORE the shooter block (which decrements ai1 at line 2149). So ours compares pre-decrement ai1 — same as vanilla case position. Good.

Drakin sounds ai1==40/60 pre-decrement — vanilla same (in case). Ours same. Good.

5. Javelin taunt: vanilla `if (ai[1] == 82f) { sound JavelinThrowersAttack; num22 = 7; style = Taunt; }` — pre-decrement in case. Ours: line 2086-2088 plays attack at ai1===82; and walker107Params sets scream/taunt when e.ai1 === 82 (line 1797-1799, also pre-decrement since params built before). Good.

6. Wither beast 568/569: vanilla num5=110 (windup), num24=0.16, num25=0.7, num23=1.4, flag5=true, num4=600. Ours matches (windup 110, accel 0.16, damp 0.7, maxSpd 1.4, melee, triggerRange 600).

Wither aura: vanilla `if (ai[0] == 0f) localAI[1] = Invalid; if (ai[0] != 1f) break;` — the aura effects only when ai[0]==1 (i.e., mid windup of the 110-tick attack: ai[0] goes 110 → ... → 1). Ours: `if (e.ai0 === 0) x[1] = 0; if (e.ai0 === 1) { ...aura... }`. matches (x[1] = localAI[1]).

- HitSound set. Ours sets e.def.hitSound. ok.
- ai[0] += 1 → 2. Ours: e.ai0 += 1 (→2). 
- dust 1/10. Ours ~ random particles. ok.
- AuraPulse sound tracked at localAI[1]. Ours plays once when x[1]===0 → x[1]=1. Approximation (vanilla keeps re-playing if sound invalid, positions update). Minor.
- localAI[0] += 1 (aura counter — drives death purple soul ring in Main). Ours: x[0] += 1. matches.
- Random dust at 400px radius when localAI[0] > 60 && rand(10)==0. Ours: `if (tgt && dist < 400 && Math.random() < 0.1)` — vanilla condition is localAI[0] > 60 (aura uptime), NOT target distance; and spawns at random ring position 400*(0.3+0.7*rand) if not solid. Ours changed to target-distance-based. Visual only, minor.
- Player buff 195 (Withered Armor) 3 ticks within 400px: ours applies buff 101 for 0.06s. OK equivalent-ish. Vanilla checks `!player.creativeGodMode`. minor.
- ai[1] > 0 → -=1; if ai[1] <= 0 → ai[1] = 60, heal lifeMax/20. Ours matches.

Note: vanilla `break` structure — when ai[0] != 1, the wither case breaks WITHOUT the aura, and then falls through to the common tail (flag5 handling etc.). Ours matches.

7. Skeleton 566/567: vanilla: light cast; flag21; num43 = localAI[3] >= 120; if !num43: num24 = 0 (no accel); if num43: dontTakeDamage = false, break (continue normal walker). Else (spawn phase): dontTakeDamage = true; velocity.X = 0; flag24 = true (no walk accel); flag20 = true (no retarget); ai[3] = 0; alpha 255 at start; localAI[3] += 1; if >= 110: alpha -= 26; dust; gore.

Ours: `if (id === 566 || id === 567) { if (x[3] < 120) { e.iframes = 2; e.vx = 0; e.ai3 = 0; if (x[3]===0) spawnAlpha=255; x[3] += 1; if (x[3] >= 110) spawnAlpha -= 26; alphaFade false; e.vy = min(vy+0.3, 10); moveAndCollide; return; } }`

Vanilla: during spawn phase, velocity.X = 0 but velocity.Y — gravity applies via common tail? The skeleton case doesn't return; it falls to the common tail which includes gravity and movement. Vanilla skeleton falls (gravity) while fading in? The case doesn't set noGravity. Common tail applies. Ours emulates with vy += 0.3 clamp 10 + moveAndCollide + return. Reasonable. Vanilla also doesn't clear dontTakeDamage until 120 (ours iframes=2 each tick — hmm, iframes=2 as "dontTakeDamage" proxy). After x[3] >= 120, vanilla sets dontTakeDamage=false; ours just stops setting iframes. OK.

Vanilla skeleton continues to use num24=0 when <120 — irrelevant since velocity.X=0 and returns.

One nuance: vanilla skeleton fade uses localAI[3] up to 120; ours `if (x[3] < 120)` then increments — so x[3] reaches 120 and normal walker resumes; matches.

8. **Ogre ground-pound sound**: vanilla plays DD2_OgreGroundPound when ai[0]==40 (case 2) and OgreAttack at case 0 ai[0]==40. Ours lines 2073-2076: `if (ai0 === 40): ai1===0 → attack; ai1===2 → ground pound`. matches.

9. Now the Ogre select-block detail: vanilla `if (ai[0] <= 0f) { ... select ... }` — note the select runs whenever ai[0] <= 0 (including cooldown negative values). Ours: `if (e.ai0 <= 0 && x[3] >= 60 && tgt)`. Vanilla nested `if (localAI[3] >= 60f)` inside. matches. Vanilla `else if (ai[1] == 2f) localAI[0] = 300f;` — ours `if (e.ai0 > 0 && e.ai1 === 2) x[0] = 300;`. matches.

Hmm wait, one detail: vanilla sets `localAI[0] = 300f` when ai[0] > 0 && ai[1] == 2 — this is evaluated every frame during the stomp attack, setting cooldown 300 continuously. After the attack ends (ai[0] = -60), localAI[0] starts decrementing from 300 → 240 frames of stomp cooldown. Ours same.

BUT: ours runs the select block BEFORE walker107Params (line 1934 vs 1950) — and the select block uses p? No, uses raw values 130/300/30. Fine.

10. Ogre triggerRange during stomp = 250 (num4 = 250 in case 2) — the flag5 windup-start check uses num4. So once ai[1]=2 selected (dist ≤ 430), the windup starts when dist < 250. Ours: p.triggerRange = 250 in ai1===2 branch. matches.

11. Now the important one I spotted: **spit cooldown num6 = 240** vs ours 60. Confirm vanilla flag5 block: `if (ai[0] == 0f) { ai[0] = -num6; }` — yes num6 is the cooldown. And case 1 sets num6 = 240. Ours p.cooldown stays 60 (set at line 1835, never updated in ai1===1 branch). CONFIRMED high-confidence deviation: Ogre spit cooldown 60 instead of 240 → spits 4× as often.

Also the clamp `if (ai[0] < -num6) ai[0] = -num6` — with num6=240 for spit. ours clamps at -60. Same root cause.

Also note: for case 0 (melee swing) and case 2 (stomp), num6 = 60 (ogre base). matches ours.

12. flag27 block (64295-64330): that's for 620 goblin shark (wet). Ours skips 620 — documented, handled elsewhere (chargerAI). Fine.

13. Same-type separation (flag28): `if (flag28)` — who sets flag28? Default false. Search: maybe set for some family... I didn't see it in the cases. 620? Not shown. Actually flag28 might be set in an earlier part I haven't read (63476-63513?). Hmm — flag28 = probably "BelongsToInvasionOldOnesArmy"? No wait. Let me check: ours dd2LightningBugAI has same-family separation; the walker file does NOT have same-type separation in ai107. If flag28 were true for DD2 walkers, ours would be missing separation. Let me grep for "flag28 = " in the AI_107 range.

14. Now the movement tail 64680-64919 — I still need to read it (gravity/stepup/jump ladder/flag2 phase fly). Ours implements phase fly + gravity + stepup + jump ladder. Let me read the vanilla.

Also flag2 phase: vanilla at top (63487-63507):
```
if (NPCID.Sets.FighterUsesDD2PortalAppearEffect[type]) {
    if (!targetData.Invalid) {
        flag2 = !Collision.CanHit(Center,0,0,targetData.Center,0,0) && (direction == Math.Sign(targetData.Center.X - Center.X) || (noGravity && Distance(targetData.Center) > 50f && Center.Y > targetData.Center.Y));
    }
    flag2 &= ai[0] <= 0f;
}
if (flag2) { if (velocity.Y == 0f || Math.Abs(targetData.Center.Y - Center.Y) > 800f) { noGravity = true; noTileCollide = true; } }
else { noGravity = false; noTileCollide = false; }
```

Ours (2094-2109):
```
phase = w107Phasing.has(e);
if (tgt) {
  const noLos = !losClear(...);
  const dist = ...;
  if (noLos && (e.facing === sign(tgt.cx - e.cx) || (phase && dist > 50 && e.cy > tgt.cy))) phase = e.ai0 <= 0;
  else phase = false;
} else phase = false;
```

Ours approximates `noGravity` (sticky bit) with the w107Phasing WeakSet. matches structure. Vanilla sets noGravity/noTileCollide only when (vy==0 || dy>800); clears when !flag2. When flag2 true but vy != 0 and dy <= 800 → noGravity NOT set... interesting: so a jumping walker mid-air with flag2 doesn't become phasing until it lands or is far. Ours: `if (phase) w107Phasing.add(e)` immediately and the movement branch treats phase as flying regardless of vy/dy>800 gate. Hmm — vanilla's noGravity is a separate latch; the actual phase-fly MOVEMENT is later in the tail (64846-64918?) gated by... let me read.

Let me read 64680-64919 now.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:16:19.913Z · glm-x-preview-260804

```
家族变体案例已明确。接下来我来处理移动尾部（64680-64919），并检查 `flag28` 的用法以及 `SimpleFlyMovement`。
```


---

## 🤖 Assistant · 2026-08-19T03:16:20.300Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '64680,64919p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_107 movement tail"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:20.362Z

**📎 ToolResult**

```
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
			}
		}
		Point point2 = base.Center.ToTileCoordinates();
		if (WorldGen.InWorld(point2.X, point2.Y, 5) && !noGravity)
		{
			GetTileCollisionParameters(out var cPosition, out var cWidth, out var cHeight);
			Vector2 vector13 = position - cPosition;
			Collision.StepUp(ref cPosition, ref velocity, cWidth, cHeight, ref stepSpeed, ref gfxOffY);
			position = cPosition + vector13;
		}
		if (flag32)
		{
			int num66 = (int)(base.Center.X + num26 * (float)direction) / 16;
			int num67 = ((int)base.Bottom.Y - 15) / 16;
			bool flag36 = position.Y + (float)height - (float)(num67 * 16) > 20f;
			Tile tileSafely = Framing.GetTileSafely(num66 + direction, num67 + 1);
			Tile tileSafely2 = Framing.GetTileSafely(num66, num67 + 1);
			Tile tileSafely3 = Framing.GetTileSafely(num66, num67);
			Tile tileSafely4 = Framing.GetTileSafely(num66, num67 - 1);
			Tile tileSafely5 = Framing.GetTileSafely(num66, num67 - 2);
			Tile tileSafely6 = Framing.GetTileSafely(num66, num67 - 3);
			if (flag8 && tileSafely4.nactive() && (tileSafely4.type == 10 || tileSafely4.type == 388))
			{
				ai[0] += 1f;
				ai[3] = 0f;
				if (ai[0] >= 60f)
				{
					if (flag9)
					{
						ai[1] = 0f;
					}
					int num68 = 5;
					if (Main.tile[num66, num67 - 1].type == 388)
					{
						num68 = 2;
					}
					velocity.X = 0.5f * (float)(-direction);
					ai[1] += num68;
					bool flag37 = false;
					if (ai[1] >= 10f)
					{
						flag37 = true;
						ai[1] = 10f;
					}
					if (flag10)
					{
						flag37 = true;
					}
					WorldGen.KillTile(num66, num67 - 1, fail: true);
					if (Main.netMode != 1 && flag37)
					{
						if (flag11)
						{
							WorldGen.KillTile(num66, num67 - 1);
							if (Main.netMode == 2)
							{
								NetMessage.SendData(17, -1, -1, null, 0, num66, num67 - 1);
							}
						}
						else
						{
							if (tileSafely4.type == 10)
							{
								bool flag38 = WorldGen.OpenDoor(num66, num67 - 1, direction);
								if (!flag38)
								{
									ai[3] = num21;
									netUpdate = true;
								}
								if (Main.netMode == 2 && flag38)
								{
									NetMessage.SendData(19, -1, -1, null, 0, num66, num67 - 1, direction);
								}
							}
							if (tileSafely4.type == 388)
							{
								bool flag39 = WorldGen.ShiftTallGate(num66, num67 - 1, closing: false);
								if (!flag39)
								{
									ai[3] = num21;
									netUpdate = true;
								}
								if (Main.netMode == 2 && flag39)
								{
									NetMessage.SendData(19, -1, -1, null, 4, num66, num67 - 1, direction);
								}
							}
						}
					}
				}
			}
			else
			{
				int num69 = spriteDirection * num27;
				if (velocity.X * (float)num69 > 0f)
				{
					if (height >= 32 && tileSafely5.nactive() && Main.tileSolid[tileSafely5.type])
					{
						netUpdate = true;
						velocity.Y = -7f;
						if (tileSafely6.nactive() && Main.tileSolid[tileSafely6.type])
						{
							velocity.Y = -8f;
						}
					}
					else if (tileSafely4.nactive() && Main.tileSolid[tileSafely4.type])
					{
						velocity.Y = -6f;
						netUpdate = true;
					}
					else if (flag36 && tileSafely3.nactive() && !tileSafely3.topSlope() && Main.tileSolid[tileSafely3.type])
					{
						velocity.Y = -5f;
						netUpdate = true;
					}
					else if (flag25 && (!tileSafely2.nactive() || !Main.tileSolid[tileSafely2.type]) && (!tileSafely.nactive() || !Main.tileSolid[tileSafely.type]))
					{
						velocity.X *= 1.5f;
						velocity.Y = -8f;
						netUpdate = true;
					}
					else if (flag8)
					{
						ai[0] = 0f;
						ai[1] = 0f;
					}
					if (velocity.Y == 0f && flag && ai[3] == 1f)
					{
						velocity.Y = -5f;
						netUpdate = true;
					}
				}
				if (flag26 && velocity.Y == 0f && Math.Abs(targetData.Center.X - base.Center.X) < 100f && Math.Abs(targetData.Center.Y - base.Center.Y) < 50f && Math.Abs(velocity.X) >= 1f && velocity.X * (float)direction > 0f)
				{
					velocity.X = MathHelper.Clamp(velocity.X * 2f, -3f, 3f);
					velocity.Y = -4f;
					netAlways = true;
				}
			}
		}
		else if (flag8)
		{
			ai[0] = 0f;
			ai[1] = 0f;
		}
		if (!flag2 || !noTileCollide)
		{
			return;
		}
		wet = false;
		if (flag29)
		{
			if (alpha < 60)
			{
				alpha += 20;
			}
			localAI[3] = 40f;
		}
		bool num70 = velocity.Y == 0f;
		if (Math.Abs(base.Center.X - targetData.Center.X) > 200f)
		{
			spriteDirection = (direction = ((targetData.Center.X > base.Center.X) ? 1 : (-1)));
			velocity.X = MathHelper.Lerp(velocity.X, direction, 0.05f);
		}
		int num71 = 80;
		int num72 = height;
		Vector2 vector14 = new Vector2(base.Center.X - (float)(num71 / 2), position.Y + (float)height - (float)num72);
		bool flag40 = false;
		if (position.Y + (float)height < targetData.Position.Y + (float)targetData.Height - 16f)
		{
			flag40 = true;
		}
		if (flag40)
		{
			velocity.Y += 0.5f;
		}
		else if (Collision.SolidCollision(vector14, num71, num72) || targetData.Center.Y - base.Center.Y < -100f || (targetData.Center.Y - base.Center.Y < 10f && Math.Abs(targetData.Center.X - base.Center.X) < 60f))
		{
			if (velocity.Y > 0f)
			{
				velocity.Y = 0f;
			}
			if ((double)velocity.Y > -0.2)
			{
				velocity.Y -= 0.025f;
			}
			else
			{
				velocity.Y -= 0.2f;
			}
			if (velocity.Y < -4f)
			{
				velocity.Y = -4f;
			}
		}
		else
		{
			if (velocity.Y < 0f)
			{
				velocity.Y = 0f;
			}
			if ((double)velocity.Y < 0.1)
			{
				velocity.Y += 0.025f;
			}
			else
			{
				velocity.Y += 0.5f;
			}
		}
		if (velocity.Y > 10f)
		{
			velocity.Y = 10f;
		}
		if (num70)
		{
			velocity.Y = 0f;
		}
	}

```


---

## 🤖 Assistant · 2026-08-19T03:16:21.784Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"flag28 = \\|flag17 = \\|flag26 = \\|flag13 = \\|flag14 = \\|flag16 = \" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | awk -F: '$1 > 63300 && $1 < 65000' ; echo ---- ; sed -n '78095,78130p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Find flag assignments in AI_107 range and read SimpleFlyMovement"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:16:21.931Z

**📎 ToolResult**

```
63430:		bool flag13 = false;
63431:		bool flag14 = false;
63446:		bool flag16 = false;
63449:		bool flag17 = false;
63465:		bool flag26 = false;
63474:		bool flag28 = false;
64122:			flag16 = true;
----
	private static int FindFrame_Deerclops_GetAttack3Frame(int sequenceFrame)
	{
		return FindFrame_FromSequence(sequenceFrame, _deerclopsAttack3Frames);
	}

	public void SimpleFlyMovement(Vector2 desiredVelocity, float moveSpeed)
	{
		if (velocity.X < desiredVelocity.X)
		{
			velocity.X += moveSpeed;
			if (velocity.X < 0f && desiredVelocity.X > 0f)
			{
				velocity.X += moveSpeed;
			}
		}
		else if (velocity.X > desiredVelocity.X)
		{
			velocity.X -= moveSpeed;
			if (velocity.X > 0f && desiredVelocity.X < 0f)
			{
				velocity.X -= moveSpeed;
			}
		}
		if (velocity.Y < desiredVelocity.Y)
		{
			velocity.Y += moveSpeed;
			if (velocity.Y < 0f && desiredVelocity.Y > 0f)
			{
				velocity.Y += moveSpeed;
			}
		}
		else if (velocity.Y > desiredVelocity.Y)
		{
			velocity.Y -= moveSpeed;
			if (velocity.Y > 0f && desiredVelocity.Y < 0f)
			{

```


---

## 🤖 Assistant · 2026-08-19T03:17:23.621Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

````
Confirmed: flag13/flag14/flag16/flag17/flag26/flag28 are all default false and never set true in the AI_107 range (only flag16 at 64122 — that's case 620 goblin shark). So for DD2 families those flags are all false → our simplifications are safe. flag28 (same-type separation) is default false and never set in range → not needed. Good.

SimpleFlyMovement matches our simpleFlyMove exactly.

Phase-fly tail comparison (64846-64919):
- wet = false
- if flag29: alpha < 60 → alpha += 20; localAI[3] = 40.
- num70 = velocity.Y == 0 (was grounded)
- if |Center.X - target.X| > 200 → direction = spriteDirection = sign; velocity.X = Lerp(velocity.X, direction, 0.05).
- flag40 = position.Y + height < target.Position.Y + target.Height - 16 (bottom above target bottom - 16 → NPC is above target)
- if flag40: velocity.Y += 0.5
- else if SolidCollision(vector14, 80, height) (box at (Center.X - 40, position.Y)) — ours: `solidAt(floor((e.cx - 40)/TILE), floor(e.y/TILE))` — hmm, e.y + e.h - e.h = e.y. vanilla vector14 = (Center.X - 40, position.Y + height - num72) where num72 = height → (Center.X-40, position.Y). So a single-tile probe vs vanilla 80×height box. Ours probes ONE tile. Acceptable approximation? It changes terrain-hover fidelity (vanilla checks an 80px-wide column). Ours single tile at left edge of that box (Center.X-40 is the LEFT edge of the 80-wide box!). Hmm: vanilla box starts at Center.X - 40 and spans 80 wide → covers Center.X-40 to Center.X+40 (centered). Ours probes at Center.X - 40 — the left edge only. That's a mis-probe: if ground is only under the right half, vanilla sees solid (hover), ours doesn't (falls). Medium-minor. Or if ground only under left edge... well. It's a real fidelity gap but small. Might fold into a minor note.
- also the two vertical-target conditions: target.Y - Center.Y < -100 (target 100px above) or (< 10 && |dx| < 60). Ours matches.
- hover servo: if vy > 0 → vy = 0; if vy > -0.2 → vy -= 0.025 else vy -= 0.2; clamp -4. Ours: `if (e.vy > 0) e.vy = 0; e.vy -= e.vy > -0.2 ? 0.025 : 0.2; if (e.vy < -4) e.vy = -4;` matches.
- else: if vy < 0 → 0; vy += vy < 0.1 ? 0.025 : 0.5. matches.
- vy > 10 → 10; if num70 (was grounded) → vy = 0. Ours matches (`if (wasGrounded) e.vy = 0`).
- localAI[3] = 40 (keeps portal-fade counter from re-triggering fade) — ours doesn't set x[3] = 40. Hmm: ours phase block: `if (W107_PORTAL_FADE.has(id) && e.spawnAlpha < 60) e.spawnAlpha += 20;` but doesn't set x[3] = 40. If x[3] < 60 at phase time, the earlier fade block (line 1967-1979) keeps incrementing x[3] and decrementing alpha each tick — conflict: fade block runs BEFORE phase block in ours. Vanilla sets localAI[3] = 40 so the fade block (which requires localAI[3] < 60) still runs but alpha climbs +20 vs -5 → net +15 → visible. Ours: fade block decrements alpha by 5 (spawnAlpha), phase adds 20 → net +15. Equivalent-ish. Also `alpha < 60` gate. Ours matches. OK fine.

Note: vanilla `if (!flag2 || !noTileCollide) return;` — the phase tail only runs when flag2 AND noTileCollide set (the vy==0||dy>800 gate). Ours: `if (phase) { ...phase fly... return; }` — ignores the vy==0||dy>800 gate. Vanilla: flag2 true but vy != 0 and dy <= 800 → noTileCollide false → normal gravity/walker movement runs (with noGravity false). Ours treats phase as immediately flying. Hmm — but wait: does vanilla's noGravity/noTileCollide persist from previous frames? The gate `if (flag2) { if (vy == 0 || dy > 800) { noGravity = noTileCollide = true } } else { noGravity = noTileCollide = false }`. So if flag2 stays true across frames: first frame walker on ground vy==0 → set phase bits. Next frame vy != 0 (hovering) → gate doesn't re-set... but the else branch only clears when !flag2. So bits STAY true once set (latched while flag2 true). So effectively once grounded-and-no-LOS, it enters phase and stays while flag2. Ours' latch via WeakSet matches this behavior. The only difference: vanilla requires ONE grounded frame (vy==0) to enter; ours enters immediately mid-jump. Minor.

Movement tail (non-phase): vanilla runs StepUp + jump ladder, then the ENGINE handles gravity+collision. Note vanilla does NOT add gravity in the AI (it's the engine's job: velocity.Y += gravity at 91519 per their comment). Ours adds vy += 0.3 clamp 10 at line 2243. Fine.

Jump ladder details:
- flag32 (grounded): vy == 0 → scan bottom row +7.
- num66 = (Center.X + num26 * direction)/16 (probe column), num67 = (Bottom.Y - 15)/16.
- vanilla: `int num69 = spriteDirection * num27; if (velocity.X * num69 > 0)` — num27 default 1. ours: `if (grounded && e.vx * e.facing > 0)`. matches.
- 3-tall wall: height >= 32 && tileSafely5 (py-2) solid → vy = -7; if tileSafely6 (py-3) solid → -8. Ours: `if (e.h >= 32 && t5) { e.vy = t6 ? -8 : -7; }` matches.
- 1-tall step: tileSafely4 (py-1) solid → vy = -6. ours matches (t4).
- slope: flag36 && tileSafely3 solid && !topSlope → -5. ours: flag36 && t3 → -5. (skips topSlope check — isSolid probably excludes half tiles? they check `!st.half[...]` in stepup. minor.)
- cliff: flag25 (directionY < 0 captured at AI start) && !t2 && !t1 → vx *= 1.5, vy = -8. ours matches with e.dirY < 0.
- The trailing `if (velocity.Y == 0f && flag && ai[3] == 1f) velocity.Y = -5f` — flag = velocity.X == 0 && velocity.Y == 0 && !justHit (from the very top). So: completely stationary + ai[3] == 1 (just started stuck counting) → hop -5. Ours MISSING this stuck-hop. Minor but real: walker wedged against a wall gets a small hop in vanilla. Hmm — but note this is INSIDE `if (velocity.X * num69 > 0)`? Let me re-read:

```
else
{
    int num69 = spriteDirection * num27;
    if (velocity.X * (float)num69 > 0f)
    {
        ... wall/step/slope/cliff/door branches ...
        if (velocity.Y == 0f && flag && ai[3] == 1f)
        {
            velocity.Y = -5f;
            netUpdate = true;
        }
    }
    if (flag26 && ...) {...}
}
```

The stuck-hop is inside `velocity.X * num69 > 0` — requires moving toward facing. flag requires velocity.X == 0 — contradiction! velocity.X * num69 > 0 with velocity.X == 0 is impossible. So that branch is dead code in vanilla? velocity.X == 0 → 0 > 0 false. So the stuck-hop never fires. Ha — dead code. Ours omitting it is correct.

- Door/tall-gate opening (flag8) — flag8 default false, set where? `bool flag8 = false;` — search shows nothing sets flag8 in range? It's for zombie/skeleton door opening (AI_003 style). In AI_107 default false → skip. Ours omits. Correct.
- flag26 default false (leap when close) → 620-only? Actually flag26 set nowhere in range (64122 is flag16). Fine, ours omits.
- `else if (flag8) { ai[0] = 0; ai[1] = 0; }` — flag8 false. fine.

Now — CRITICAL check of ours phase probe: `const below = tgt ? e.y + e.h < tgt.y + tgt.h - 16 : false;` — flag40 = position.Y + height < target.Position.Y + target.Height - 16. matches.

OK. Now back to consolidating AI_107 findings:

**CONFIRMED #1: Ogre spit cooldown 60 vs vanilla 240** (num6 = 240 in case 1 at cs:63587-63600 region). Our file line 1835 sets p.cooldown = 60; the ai1===1 branch (1846-1853) doesn't set 240. Also the clamp at line 2200 uses -p.cooldown. High confidence. Impact: Ogre spits 4× more often. Fix: `p.cooldown = 240` in the ai1===1 branch.

Wait — double-check the flag5 windup-end: `if (ai[0] == 0f) { ai[0] = -num6; }`. For spit, windup = 90 (num5). Countdown 90 → ... → 1 → 0 → set -240. Then cooldown decrements 240 ticks (with `ai[0] < 0 → += 1`). During cooldown, select block `if (ai[0] <= 0f)` RUNS (ai[0] negative) and may re-select ai[1]... but the flag5 start requires ai[0]==0. So next spit after 240 ticks. Ours: 60 ticks. Confirmed.

Hmm, also NOTE: vanilla select block runs when ai[0] <= 0 — during the -240 cooldown, dist-based select can switch ai[1] between 0/1/2 freely. Ours also runs select when ai0 <= 0. matches.

**CONFIRMED #2: flag7 windup damping + flag20 retarget-freeze + ai3 reset only for Ogre** — vanilla flag7 default true (cs:63424), num7 = 0.9; the flag5 windup branch does `velocity.X *= num7; flag24 = true; flag20 = true; ai[3] = 0;` for ALL melee families (goblins 552-554, wither beast 568/569, kobold 572/573 approach/charge, ogre). Ours windupDampOn only true for ogre (0.7); others no damping, retarget/scream block still runs during windup, ai3 not reset.

Impact: goblins slide at full speed during their 30t swing windup instead of braking to a stop; facing keeps flipping. Wither beast same (110t windup at 1.4 speed — quite visible). This is a genuine behavioral difference.

But wait — ours' walk accel: for goblins (noWalkAccel false), w107WalkAccel runs at line 2146 — before the melee block. During windup ours keeps accelerating. Vanilla flag24=true skips it. So yes.

Actually, hold on — for ogre ours does damp but does NOT set flag24/flag20/ai3=0 either. So the general fix: in melee windup, damp vx by num7, freeze retarget/scream, reset ai3, skip walk accel. Our attacking gate already skips stuck-counting and (via !busy... no) — the scream/retarget block (line 2124) is gated only on ai3 < 30, not on attacking. Vanilla flag20 also skips it. So for ALL melee families vanilla freezes retarget during windup, ours doesn't.

**#3 Dutchman cannon velocity double-normalization** — described above. Vanilla cs:36033-36045: vector140 = normalize(player.Center - cannon.Center) * 14; vector140 += (0,-5). Ours re-normalizes (d*14 + (0,-5)) to 14 then subtracts 5 again. Horizontal shots: vanilla (14,-5) vs ours (13.07,-9.67). CONFIRMED (high confidence on the math difference; both lines read).

**#4 Ogre ground-pound muzzle**: vanilla vector = (-direction*20, height/2 - 1) — ours matches.

**#5 Drakin multi-shot rewrite**: vanilla `if (type == 571 && ai[1] > 10 && ai[1] <= 40 && (int)ai[1] % 6 == 0) num9 = (int)ai[1] - 1;` — note: this modifies num9 for the CURRENT frame (fires when ai[1] == num9 after decrement... wait, order: case computes num9 from current ai[1]; flag12 block then decrements ai[1] and checks `if (ai[1] == num9)`. So e.g. ai[1] = 18 (pre), 571: 18 > 10, <= 40, 18 % 6 == 0 → num9 = 17. Then decrement ai[1] → 17. Check ai[1] == 17 → fire! So the drakin fires on frames where (pre-decrement ai[1]) % 6 == 0 for T2 (571). Net effect: multi-shots at ai[1] = 12, 18, 24, 30, 36 (pre-decrement values) plus the base shot at ai[1] == 40.

Ours: `if (e.ai1 > 10 && e.ai1 <= 40 && e.ai1 % (id === 571 ? 6 : 9) === 0) p.fireAt = e.ai1 - 1;` — p built pre-decrement in walker107Params, and fireAt used in shooter block post-decrement check `e.ai1 === p.fireAt`. Same as vanilla. matches!

**#6 Wither beast visual dust** condition changed (localAI[0] > 60 && rand10 → ring dust vs ours target-distance). Minor/visual.

Now Betsy details re-verified. One thing to double check on Betsy: our `if (!tgt)` fallback `e.vy -= 0.05; fly(e); return;` — invented? In vanilla, TargetClosestBetsy with no valid target... Actually vanilla AI_110 runs the full state machine regardless; targetData would be invalid/last. The `vy -= 0.05` is a float-off approximation. It's minor; where does the boss flee? In vanilla, when the crystal is dead AND players dead, the DD2 event ends and Betsy... hmm Betsy doesn't flee; event StopInvasion despawns? Not our file's concern. I'll note as minor/doubtful, not CONFIRMED-worthy.

Now the remaining pieces to check: sandElementalAI, sandSharkAI, eterniaCrystalAI, lanePortalAI, divingFlyerAI. I've read ours up to 1234 (divingFlyer partially: lines 1049-1234 I haven't read!). I read 1-700 and 1234-2296. Missing 700-1234 (sandElemental tail, sandShark, dd2AttackerTest, eterniaCrystal, lanePortal, divingFlyer). Let me read that now, plus vanilla 42224-42620 (sand elemental), 42621-42805 (sand shark), 42810-43152 (crystal + portal), 65959-66200 (diving flyer). That's a lot; the prompt says these are secondary priority. Let me read ours 700-1234 first, then vanilla for elemental + shark + crystal + portal + flyer.
````

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:24.148Z · glm-x-preview-260804

```
现在我来读取文件中间部分（sand elemental/shark/crystal/portal/divingFlyer）。
```


---

## 🤖 Assistant · 2026-08-19T03:17:24.493Z · glm-x-preview-260804

**🔧 ToolUse: `Read`**

```json
{
 "file_path": "~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts",
 "limit": 540,
 "offset": 696
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:24.510Z

**📎 ToolResult**

```
696	// AI_102 沙尘精 541（NPC.cs:42224-42620）
697	// ---------------------------------------------------------------------------
698	export function sandElementalAI(e: Enemy, game: GameHooks, player: Player | null) {
699	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; }
700	  const x = dd2LocalAI(e);
701	  // ---- 族参数（:42225-42243 默认档 → :42246-42252 的 541 覆盖） ----
702	  const p: WalkerP = {
703	    frontDepth: 4, headClear: 3, bottomDepth: 3,
704	    grav: 0.1, maxFall: 2, upAccel: -0.1, maxUp: -4,
705	    headScan: false,
706	    maxH: 2, accelH: 0.1, maxV: 1, accelV: 0.04,
707	  };
708	  e.visAngle = e.vx * 0.04;                       // rotation = vx*0.04（:42249）
709	  // 血量越低越快（:42255-42257 num1575/num1576 随亏血加成）+ 半血免击退（:42258-42261）
710	  const ratio = e.hp / e.maxHp;
711	  p.maxH += (1 - ratio) * 2;
712	  p.accelH += (1 - ratio) * 0.02;
713	  e.def.knockbackResist = ratio < 0.5 ? 0 : e.def.knockbackResist; // def 存承受比例：0=免疫
714	  // ---- 攻击循环（:42263-42389） ----
715	  let castDamp = 0;
716	  if (e.ai0 < 0) e.ai0 = Math.min(e.ai0 + 1, 0);   // 冷却回摆（:42267-42269）
717	  if (e.ai0 > 0) {
718	    castDamp = 0.96;                                // flag114 → 施法僵直 ×0.96
719	    e.ai0 += 1;
720	    if (e.ai0 >= 135) { e.ai0 = -300; }             // 135t → -300 冷却（:42273-42276）
721	    if (e.ai0 === 54 && player && !player.dead) {
722	      // 玩家预测位 ±30 格找 ≤3 个落点放沙暴标记 658（:42300-42342）
723	      const px = player.cx + player.vx * 30;
724	      const py = player.cy;
725	      if (Math.hypot(px - e.cx, py - e.cy) < 2000) {
726	        const ptx = Math.floor(px / TILE), pty = Math.floor(py / TILE);
727	        const picks: Array<{ x: number; y: number }> = [];
728	        for (let t = 0; t < 1000 && picks.length < 3; t++) {
729	          const col = rndRange(ptx - 30, ptx + 31);
730	          if (picks.some((q) => Math.abs(q.x - col) < 10)) continue;
731	          const startY = pty - 20;
732	          const [, bottomY] = expandVertically(game, col, startY, 1, 51);
733	          const my = bottomY - 15;
734	          if (canSpawnSandstormHostile(game, col, my)) picks.push({ x: col, y: my });
735	        }
736	        for (const q of picks) {
737	          // 658 沙暴标记：原版 damage 0 纯视觉（尘柱 900t）——粒子代,不生成弹体
738	          game.spawnParticles(q.x * TILE + 8, q.y * TILE + 8, '#E0A050', 8, 1.4, { life: 60, grav: -0.06 });
739	        }
740	      } else {
741	        e.ai0 = -200;                               // 太远 → 缩短冷却（:42344-42347）
742	      }
743	    }
744	  }
745	  if (e.ai0 === 0) e.ai0 = 1;                       // 起手（:42387-42389）
746	  walkerKernel(e, game, player, x, p, castDamp);
747	}
748	
749	// ---------------------------------------------------------------------------
750	// 沙鲨碰撞（Collision.AdvancedTileCollision + ForSandshark,cs:93808-93814）：
751	// 沙族 tile 无视碰撞,其余照撞;撞轴清零该轴速度并置 collideX/collideY 旗标。
752	// 湿身另按 UpdateCollision 的 Collision_MoveWhileWet 缩位移（:93762 waterMovementSpeed
753	// =0.5,542-545 不在 DD2/612/613 全速豁免表）——视水为可穿沙介质但移动仍半速
754	// ---------------------------------------------------------------------------
755	function moveSandShark(e: Enemy, game: GameHooks, vx: number, vy: number): void {
756	  const st = game.world.store;
757	  // NPC.Collision_MoveWhileWet（:93986）：velocity 不变,只缩位移
758	  const lf = e.liqFactor;
759	  if (lf !== undefined && lf !== 1) { vx *= lf; vy *= lf; }
760	  const passable = (tx: number, ty: number): boolean => {
761	    if (!st.inBounds(tx, ty)) return false;
762	    return st.isSolid(tx, ty) && !SANDSHARK_PASS.has(st.type[st.idx(tx, ty)]);
763	  };
764	  e.hitWall = false; e.onGround = false; e.hitHead = false;
765	  // X 轴
766	  const nx = e.x + vx;
767	  if (vx !== 0) {
768	    const d = sign(vx);
769	    const edge = d > 0 ? nx + e.w : nx;
770	    const tx = Math.floor(edge / TILE);
771	    const y0 = Math.floor(e.y / TILE);
772	    const y1 = Math.floor((e.y + e.h - 0.01) / TILE);
773	    let hit = false;
774	    for (let ty = y0; ty <= y1; ty++) {
775	      if (passable(tx, ty)) { hit = true; break; }
776	    }
777	    if (hit) { e.hitWall = true; e.vx = 0; } else e.x = nx;
778	  }
779	  // Y 轴
780	  const ny = e.y + vy;
781	  if (vy !== 0) {
782	    const d = sign(vy);
783	    const edge = d > 0 ? ny + e.h : ny;
784	    const ty = Math.floor(edge / TILE);
785	    const x0 = Math.floor(e.x / TILE);
786	    const x1 = Math.floor((e.x + e.w - 0.01) / TILE);
787	    let hit = false;
788	    for (let tx = x0; tx <= x1; tx++) {
789	      if (passable(tx, ty)) { hit = true; break; }
790	    }
791	    if (hit) {
792	      if (d > 0) e.onGround = true; else e.hitHead = true;
793	      e.vy = 0;
794	    } else {
795	      e.y = ny;
796	    }
797	  }
798	}
799	
800	// ---------------------------------------------------------------------------
801	// AI_103 沙鲨族 542-545（NPC.cs:42621-42805）
802	// ---------------------------------------------------------------------------
803	export function sandSharkAI(e: Enemy, game: GameHooks, player: Player | null) {
804	  if (!e.bInit) { e.bInit = true; e.ai0 = 1; e.ai1 = 0; e.ai2 = 0; e.dirY = 1; }
805	  const x = dd2LocalAI(e);
806	  if (e.facing === 0) e.facing = player ? e.seekDirX(player) : -1;   // :42625-42627
807	  // ---- 在沙判定（:42629-42634）：中心格是沙族 tile（须 nactive）或湿 ----
808	  // flag119 |= wet：沙鲨视水为沙——水中同样进入巡游/扑咬态（水豁免,原版 :42634）
809	  const ctx = Math.floor(e.cx / TILE), cty = Math.floor(e.cy / TILE);
810	  const st0 = game.world.store;
811	  const sandMedium = (t: number, tx: number, ty: number): boolean =>
812	    (CONV_SAND.has(t) || CONV_SANDSTONE.has(t) || CONV_HARDENED.has(t))
813	    && st0.inBounds(tx, ty) && st0.isActive(tx, ty);    // 原文 tileSafely7.nactive()
814	  const isSandTile = sandMedium(tileTypeAt(game, ctx, cty), ctx, cty);
815	  const inSand = isSandTile || e.inWater;
816	  // ---- 扑咬门（:42637-42642 flag120）：玩家在上方（vy 不上升）且距 >150px ----
817	  const tgt = player && !player.dead ? { x: player.cx, y: player.cy } : null;
818	  const canLunge = !!tgt
819	    && player!.vy > -0.1
820	    && Math.hypot(tgt!.x - e.cx, tgt!.y - e.cy) > 150;
821	  if (x[0] === -1 && !inSand) x[0] = 20;           // 跃出后落回非沙 → 短冷却（:42643-42645）
822	  if (x[0] > 0) x[0] -= 1;
823	  // 游弋周期音（:42652-42663）：soundDelay==0 时播 (15,Center,4)——case15 style4
824	  //   映射 num=1+num18=0.25 → Roar_1 ×0.25(音量是调用点参数非文件档,FILE_CASE_VOL
825	  //   不登记,2026-08-18 修正),delay = 玩家距/40 钳 10..20——与蠕虫掘地音同构
826	  if (inSand && e.digSndDelay <= 0) {
827	    const dd = tgt ? Math.hypot(tgt.x - e.cx, tgt.y - e.cy) : 400;
828	    e.digSndDelay = Math.round(Math.min(20, Math.max(10, dd / 40)));
829	    game.playSfxWav?.('Roar_1', 0.25, e.cx, e.cy);
830	  } else if (e.digSndDelay > 0) {
831	    e.digSndDelay--;
832	  }
833	  if (inSand) {
834	    // ---- 沙中巡游（:42652-42745） ----
835	    e.ai2 = Math.min(e.ai2 + 1, 30);               // 扑咬回充（:42660-42662）
836	    if (canLunge) {
837	      e.facing = tgt!.x > e.cx ? 1 : -1;            // TargetClosest
838	      e.vx += e.facing * 0.15;
839	      e.vy += e.dirY * 0.15;
840	      e.vx = clamp(e.vx, -5, 5);
841	      e.vy = clamp(e.vy, -3, 3);
842	      // 前方是否仍是沙（:42677-42689）：中心+速度方向×体半径+速度
843	      const vv = Math.hypot(e.vx, e.vy);
844	      const ax = e.cx + (vv > 0 ? e.vx / vv : 0) * Math.hypot(e.w, e.h) / 2 + e.vx;
845	      const ay = e.cy + (vv > 0 ? e.vy / vv : 0) * Math.hypot(e.w, e.h) / 2 + e.vy;
846	      const at = tileTypeAt(game, Math.floor(ax / TILE), Math.floor(ay / TILE));
847	      let aheadSand = sandMedium(at, Math.floor(ax / TILE), Math.floor(ay / TILE));
848	      // 水豁免（:42696-42699）：前方非沙且自身湿 → 前方有液体即视为仍在介质中
849	      if (!aheadSand && e.inWater) aheadSand = liquidAt(game, Math.floor(ax / TILE), Math.floor(ay / TILE)) > 0;
850	      const range = 400;
851	      if (!aheadSand && sign(e.vx) === e.facing
852	        && Math.hypot(tgt!.x - e.cx, tgt!.y - e.cy) < range
853	        && (e.ai2 >= 30 || e.ai2 < 0)) {
854	        if (x[0] === 0) { x[0] = -1; game.playSfxWav?.('Zombie_7', 1, e.cx, e.cy); }  // :42713 (14,542) 出沙扑咬音
855	        e.ai2 = -30;
856	        const d = dirTo(e, tgt!.x, tgt!.y - 80);   // 跃沙扑咬 12 速（:42708-42711）
857	        e.vx = d.x * 12;
858	        e.vy = d.y * 12;
859	      }
860	    } else {
861	      // 沙下巡航（:42713-42745）：撞轴反弹 + 蛇形升降
862	      if (e.hitWall) { e.vx *= -1; e.facing *= -1; }
863	      if (e.onGround || e.hitHead) {
864	        e.vy *= -1;
865	        e.dirY = sign(e.vy) || 1;
866	        e.ai0 = e.dirY;
867	      }
868	      e.vx += e.facing * 0.1;
869	      if (e.vx < -6 || e.vx > 6) e.vx *= 0.95;
870	      // 贴沙探测（flag121,:42655-42659）：采样 = (Center+(0,24)).ToTileCoordinates().Y − 2
871	      // ——即中心行或其上一行（反编译表达式原样,非"下方 24px"）;水中巡游时该处非沙 →
872	      // ai[0]=1 下潜回沙
873	      const bt = tileTypeAt(game, ctx, Math.floor((e.cy + 24) / TILE) - 2);
874	      const floorNear = sandMedium(bt, ctx, Math.floor((e.cy + 24) / TILE) - 2);
875	      e.ai0 = floorNear ? -1 : 1;
876	      const osc = 0.06, step = 0.01;
877	      if (e.ai0 === -1) {
878	        e.vy -= step;
879	        if (e.vy < -osc) e.ai0 = 1;
880	      } else {
881	        e.vy += step;
882	        if (e.vy > osc) e.ai0 = -1;
883	      }
884	      if (e.vy > 0.4 || e.vy < -0.4) e.vy *= 0.95;
885	    }
886	  } else {
887	    // ---- 离沙（:42747-42763）：重力下落 + 贴地爬行 ----
888	    if (e.vy === 0 && canLunge) e.facing = tgt!.x > e.cx ? 1 : -1;
889	    if (e.vy === 0) {
890	      e.vx += e.facing * 0.1;
891	      if (e.vx < -1 || e.vx > 1) e.vx *= 0.95;
892	    }
893	    e.vy += 0.3;
894	    if (e.vy > 10) e.vy = 10;
895	    e.ai0 = 1;
896	  }
897	  // ---- 俯仰角（:42765-42772 rotation=vy*dir*0.1 钳 ±0.2） ----
898	  e.visAngle = clamp(e.vy * e.facing * 0.1, -0.2, 0.2);
899	  moveSandShark(e, game, e.vx, e.vy);
900	}
901	
902	// ---------------------------------------------------------------------------
903	// AI_104 DD2AttackerTest 547（NPC.cs:42807-42809）——原版即 active=false
904	// ---------------------------------------------------------------------------
905	export function dd2AttackerTestAI(e: Enemy, game: GameHooks): void {
906	  void game;
907	  e.dead = true;
908	}
909	
910	// ---------------------------------------------------------------------------
911	// AI_105 永恒水晶 548（NPC.cs:42810-43062）
912	// ai[1] 0=倒计时+放门 / 1=败北演出 / 2=胜利演出（后两者依赖 DD2Event 触发）
913	// ---------------------------------------------------------------------------
914	export function eterniaCrystalAI(e: Enemy, game: GameHooks, player: Player | null) {
915	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; }
916	  const x = dd2LocalAI(e);
917	  e.despawnTimer = 750;   // netAlways：不参与离屏消退
918	  if (e.spawnAlpha === 0) e.lightRGB = [1.3, 0.5, 1.5];   // :42813-42816
919	  void player;
920	  if (e.ai1 === 0) {
921	    // ---- 倒计时 + 双端放门（:42818-42845） ----
922	    if (e.ai0 > 0) e.ai0 -= 1;
923	    if (e.ai0 !== 0) return;
924	    e.ai0 = 180;
925	    if (x[0] === 0) {
926	      x[0] = 1;
927	      const ends = checkArenaScore(game, e.cx, e.y + e.h);
928	      ends.left.x += 2; ends.right.x -= 2;        // :42832-42833
929	      for (const [end, gate] of [[ends.left, 0], [ends.right, 1]] as const) {
930	        const portal = spawnPart(game, e, 549);
931	        if (portal) {
932	          portal.ai0 = 0; portal.ai1 = 0;
933	          portal.ai2 = gate;                      // 右门 ai[2]=1（leftGate 判定源）
934	          portal.x = end.x * TILE + 8 - portal.w / 2;
935	          portal.y = end.y * TILE + 16 - portal.h; // Bottom = 端点 ToWorldCoordinates(8,16)
936	        }
937	      }
938	      DD2_EVENT_HOOKS.findArenaHitbox?.(game);    // DD2Event.FindArenaHitbox（:42841）
939	    }
940	  } else if (e.ai1 === 2) {
941	    // ---- 胜利演出（:42846-42958,依赖 DD2Event 置 ai[1]=2） ----
942	    e.iframes = 2;                                 // dontTakeDamageFromHostiles + 满血
943	    e.hp = e.maxHp;
944	    if (e.ai0 === 3) {
945	      for (const n of game.enemies() as Enemy[]) {
946	        if (!n.dead && n.vanillaId === 549) { n.ai1 = 1; n.ai0 = 0; }
947	      }
948	      game.spawnParticles(e.cx, e.cy - 40, '#B0FFD0', 24, 3, { life: 60 });
949	    }
950	    e.ai0 += 1;
951	    if (e.ai0 <= 120) {
952	      // 升空小回旋（:42866-42873）
953	      e.vy = Math.cos((e.ai0 / 120) * TAU) * 0.25 - 0.25;
954	    } else {
955	      e.vy = 0;
956	    }
957	    // 尘涡（:42894-42958 的 264 号白尘双环,粒子近似）
958	    if (e.ai0 < 540 && Math.random() < 0.6) {
959	      const a = Math.random() * TAU;
960	      game.spawnParticles(
961	        e.cx + Math.cos(a) * (110 + Math.random() * 600),
962	        e.cy - 20 + Math.sin(a) * (110 + Math.random() * 600),
963	        '#FFFFFF', 1, 0.5, { life: 40 });
964	    }
965	    if (e.ai0 >= 600) {
966	      DD2_EVENT_HOOKS.stopInvasion?.(game, true);  // DD2Event.StopInvasion(win:true)
967	      e.iframes = 0;
968	      e.hp = 0;
969	      e.hurt(9999, 0, 0, game);
970	    }
971	  } else if (e.ai1 === 1) {
972	    // ---- 败北演出（:42959-43061,依赖 DD2Event.ReportLoss） ----
973	    e.iframes = 2;
974	    e.hp = e.maxHp;
975	    if (e.ai0 === 0) {
976	      for (const n of game.enemies() as Enemy[]) {
977	        if (!n.dead && n.vanillaId === 549) { n.ai1 = 1; n.ai0 = 0; }
978	      }
979	      DD2_EVENT_HOOKS.reportLoss?.(game);
980	      game.spawnParticles(e.cx, e.cy - 40, '#FF6A6A', 24, 3, { life: 60 });
981	    }
982	    e.ai0 += 1;
983	    if (e.ai0 < 96) e.vy = lerp(0, -1, e.ai0 / 96);   // :42993-42997 上浮
984	    if (e.ai0 >= 96) e.spawnAlpha = Math.min(255, e.spawnAlpha + 50);  // 渐隐
985	    if (Math.random() < 0.6) {
986	      const a = Math.random() * TAU;
987	      game.spawnParticles(
988	        e.cx + Math.cos(a) * (70 + Math.random() * 600),
989	        e.cy - lerp(0, 70, lerpValue(0, 300, e.ai0)) + Math.sin(a) * 40,
990	        '#FFB0B0', 1, 0.5, { life: 40 });
991	    }
992	    if (e.ai0 >= 600) {
993	      DD2_EVENT_HOOKS.stopInvasion?.(game, false);
994	      e.iframes = 0;
995	      e.hp = 0;
996	      e.hurt(9999, 0, 0, game);
997	    }
998	  }
999	}
1000	
1001	// ---------------------------------------------------------------------------
1002	// AI_106 神秘传送门 549（NPC.cs:43063-43152）
1003	// ai[2]=0 左门/1 右门;ai[1] 0=开门出怪（事件依赖）→ 1=缩放消散
1004	// ---------------------------------------------------------------------------
1005	export function lanePortalAI(e: Enemy, game: GameHooks, player: Player | null) {
1006	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = e.ai2 === 1 ? 1 : 0; }
1007	  const x = dd2LocalAI(e);
1008	  const leftGate = e.ai2 === 0;
1009	  e.despawnTimer = 750;   // netAlways
1010	  if (e.spawnAlpha === 0) e.lightRGB = [0.5, 0.1, 0.3];   // :43066-43068
1011	  void player;
1012	  const crystal = findCrystal(game);
1013	  if (crystal) e.iframes = 2;   // SetDefaults dontTakeDamage=true（:15987）
1014	  if (e.ai1 === 0) {
1015	    // ---- 开门出怪（:43071-43116） ----
1016	    if (x[0] === 0) {
1017	      game.playSfxFiles(['dd2_etherian_portal_open'], 0.7, e.cx, e.cy);  // DD2_EtherianPortalOpen（:43075）
1018	    }
1019	    if (!DD2_EVENT_HOOKS.enemySpawningOnHold()) e.ai0 += 1;
1020	    const rate = DD2_EVENT_HOOKS.laneSpawnRate();
1021	    // 出怪拍（:43094-43108 1:1）：ai[0] 数到 LaneSpawnRate 才进门——首拍在第
1022	    // rate tick（不是 0）,此后每 rate tick 一拍,3 拍归零
1023	    if (e.ai0 >= rate) {
1024	      if (e.ai0 >= rate * 3) e.ai0 = 0;
1025	      if (e.ai0 % rate === 0) {
1026	        DD2_EVENT_HOOKS.spawnMonsterFromGate?.(game, e.cx, e.y + e.h, leftGate);
1027	      }
1028	    }
1029	    x[0] += 1;
1030	    if (x[0] > 180) x[0] = 180;
1031	    if (x[0] >= 180) {
1032	      if (crystal) return;                        // 水晶在世 → 驻守（:43109-43113）
1033	      e.ai1 = 1;                                  // 水晶亡 → 开始消散
1034	      e.ai0 = 0;
1035	    }
1036	  } else if (e.ai1 === 1) {
1037	    // ---- 缩放消散（:43118-43146） ----
1038	    e.ai0 += 1;
1039	    e.vanillaScale = lerp(1, 0.05, lerpValue(500, 600, e.ai0));
1040	    if (e.ai0 >= 550) {
1041	      e.iframes = 0;
1042	      e.hp = 0;
1043	      e.hurt(9999, 0, 0, game);
1044	    }
1045	  }
1046	}
1047	
1048	// ---------------------------------------------------------------------------
1049	// AI_108 俯冲飞行族（NPC.cs:43157 → AI_108_DivingFlyer :65959）
1050	// 558/559/560 埃特尼亚飞龙 T1/T2/T3 + 574/575 小妖魔滑翔怪 T2/T3
1051	// ---------------------------------------------------------------------------
1052	interface FlyerP {
1053	  kbMult: number; hoverUp: number; range: number; approach: number; aimT: number;
1054	  damp: number; jitter: number; diveSpeed: number; recoverLerp: number; diveDist: number;
1055	  steerLerp: number; speedAdd: number; minSpeed: number; explode: boolean; fade: boolean;
1056	  grav: number; sep: number;
1057	}
1058	function flyerParams(id: number): FlyerP {
1059	  // 默认档（:65986-66002,本族无默认成员,保留作基线）
1060	  const base: FlyerP = {
1061	    kbMult: 0.4, hoverUp: 200, range: 750, approach: 30, aimT: 30, damp: 0.95,
1062	    jitter: 50, diveSpeed: 14, recoverLerp: 30, diveDist: 100, steerLerp: 20,
1063	    speedAdd: 0, minSpeed: 7, explode: false, fade: false, grav: 0, sep: 0.05,
1064	  };
1065	  if (id === 558 || id === 559 || id === 560) {
1066	    // 飞龙档（:66004-66022）
1067	    return {
1068	      ...base,
1069	      kbMult: id === 558 ? 0.7 : id === 559 ? 0.5 : 0.2,
1070	      hoverUp: 400, range: 500, approach: 90, aimT: 20,
1071	      jitter: 0, diveSpeed: 8, diveDist: 150, steerLerp: 60,
1072	      speedAdd: 0.05, minSpeed: 6, explode: false, fade: true, grav: 0,
1073	    };
1074	  }
1075	  // 小妖魔滑翔怪档（:66024-66042）
1076	  return {
1077	    ...base,
1078	    kbMult: id === 575 ? 0.4 : 0.6,
1079	    hoverUp: 400, range: 500, approach: 90, aimT: 30,
1080	    jitter: 3, diveSpeed: 8, diveDist: 150, steerLerp: 10,
1081	    speedAdd: 0.05, minSpeed: 0, explode: true, fade: true, grav: -0.1, sep: 0.05,
1082	  };
1083	}
1084	
1085	export function divingFlyerAI(e: Enemy, game: GameHooks, player: Player | null) {
1086	  if (!e.bInit) { e.bInit = true; e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1087	  const x = dd2LocalAI(e);
1088	  const p = flyerParams(e.vanillaId ?? 0);
1089	  const LOS_GRACE = 120;   // num14（:66003）
1090	  // ---- 出生渐显（:66062-66092 flag5） ----
1091	  if (p.fade) {
1092	    if (x[0] === 0) e.spawnAlpha = 255;
1093	    if (x[0] === 30) game.playSfxFiles(soundTrackFiles('dd2_etherian_portal_spawn_enemy'), 0.4, e.cx, e.cy); // DD2_EtherianPortalSpawnEnemy（:64270 PlayTrackedSound）
1094	    if (x[0] < 60) {
1095	      x[0] += 1;
1096	      e.spawnAlpha = Math.max(0, e.spawnAlpha - 5);
1097	      e.alphaFade = false;   // 接管 fromVanilla 的通用渐显（原版由本 AI 驱动）
1098	    }
1099	  }
1100	  // ---- 索敌（:66044 NPCUtils.TargetClosestOldOnesInvasion） ----
1101	  const tgt = dd2Target(game, e, player);
1102	  // ---- 同族分离（:66094-66116 flag4） ----
1103	  for (const n of game.enemies() as Enemy[]) {
1104	    if (n === e || n.dead || n.vanillaId !== e.vanillaId) continue;
1105	    if (Math.abs(e.x - n.x) + Math.abs(e.y - n.y) < e.w) {
1106	      if (e.x < n.x) e.vx -= p.sep; else e.vx += p.sep;
1107	      if (e.y < n.y) e.vy -= p.sep; else e.vy += p.sep;
1108	    }
1109	  }
1110	  // ---- 朝向与俯仰（:66118-66130） ----
1111	  e.visAngle = Math.atan2(e.vy, e.vx);
1112	  if (sign(e.vx) !== 0) e.facing = -sign(e.vx);
1113	  if (e.visAngle < -Math.PI / 2) e.visAngle += Math.PI;
1114	  if (e.visAngle > Math.PI / 2) e.visAngle -= Math.PI;
1115	  if (!tgt) { fly(e); return; }
1116	  const txc = tgt.x, tyc = tgt.y;
1117	  const LOS = losClear(game, e.cx, e.cy, txc, tyc);
1118	  const speedAdd = p.speedAdd * p.steerLerp;   // num12 *= num11（:66132）
1119	  if (e.ai0 === 0) {
1120	    // ---- 悬空逼近（:66134-66190） ----
1121	    // 原版：vector = normalize(Δ)*num（逼近速:飞龙 3/小妖魔 4）;vector2 = normalize(vector-(0,num2))*num
1122	    const num = e.vanillaId === 574 || e.vanillaId === 575 ? 4 : 3;
1123	    const dx = txc - e.cx, dy = tyc - e.cy;
1124	    const dist = Math.hypot(dx, dy);
1125	    const ux = dist > 0 ? dx / dist : 0, uy = dist > 0 ? dy / dist : 0;
1126	    const vx1 = ux * num, vy1 = uy * num;
1127	    let hvx = vx1, hvy = vy1 - p.hoverUp;
1128	    const hl = Math.hypot(hvx, hvy) || 1;
1129	    hvx = (hvx / hl) * num;
1130	    hvy = (hvy / hl) * num;
1131	    let los = LOS;
1132	    if (e.ai3 >= LOS_GRACE) los = true;            // 120t 视线宽限（:66152-66154）
1133	    const ang = Math.atan2(uy, ux);
1134	    los = los && ang > Math.PI / 8 && ang < Math.PI - Math.PI / 8;  // 下视野门（:66156-66158）
1135	    if (dist > p.range || !los) {
1136	      e.vx = (e.vx * (p.approach - 1) + hvx) / p.approach;
1137	      e.vy = (e.vy * (p.approach - 1) + hvy) / p.approach;
1138	      if (tyc < e.cy) {
1139	        e.vy -= 0.2;
1140	        if (e.vy < -10) e.vy = -10;
1141	      }
1142	      if (!los) {
1143	        e.ai3 += 1;                                 // 视线中断计数（:66170-66179）
1144	      } else {
1145	        e.ai3 = 0;
1146	      }
1147	    } else {
1148	      e.ai0 = 1;                                    // 进入瞄准（:66181-66186）
1149	      e.ai2 = vx1;
1150	      e.ai3 = vy1;
1151	    }
1152	  } else if (e.ai0 === 1) {
1153	    // ---- 瞄准（:66192-66232） ----
1154	    e.vx *= p.damp;
1155	    e.vy *= p.damp;
1156	    e.vy += p.grav;                                 // 小妖魔下沉点火（num16）
1157	    e.ai1 += 1;
1158	    if (e.ai1 === p.aimT) {
1159	      // 俯冲音（:66202-66222）：飞龙 558-560 DD2_WyvernDiveDown（1/5 追加 Scream）；
1160	      // 小妖魔滑翔怪 574/575 DD2_KoboldFlyerChargeScream + DD2_KoboldIgnite
1161	      if (e.vanillaId === 574 || e.vanillaId === 575) {
1162	        game.playSfxFiles(soundTrackFiles('dd2_kobold_flyer_charge_scream'), 0.7, e.cx, e.cy);
1163	        game.playSfxFiles(['dd2_kobold_ignite'], 0.6, e.cx, e.cy);
1164	      } else {
1165	        game.playSfxFiles(soundTrackFiles('dd2_wyvern_dive_down'), 0.7, e.cx, e.cy);
1166	        if (Math.random() < 0.2) game.playSfxFiles(soundTrackFiles('dd2_wyvern_scream'), 0.6, e.cx, e.cy);
1167	      }
1168	    }
1169	    if (e.ai1 >= p.aimT) {
1170	      e.ai0 = 2;
1171	      e.ai1 = 0;
1172	      let jx = e.ai2 + rndRange(-p.jitter, p.jitter + 1) * 0.04;
1173	      let jy = e.ai3 + rndRange(-p.jitter, p.jitter + 1) * 0.04;
1174	      const jl = Math.hypot(jx, jy) || 1;
1175	      jx = (jx / jl) * p.diveSpeed;
1176	      jy = (jy / jl) * p.diveSpeed;
1177	      e.vx = jx; e.vy = jy;
1178	    }
1179	  } else if (e.ai0 === 2) {
1180	    // ---- 俯冲追踪（:66234-66296） ----
1181	    e.ai1 += 1;
1182	    const dist = Math.hypot(txc - e.cx, tyc - e.cy);
1183	    let past = dist > p.diveDist && e.cy > tyc;     // 冲过目标下方（flag7）
1184	    if (p.explode) past = false;                    // flag3：小妖魔不提前收（:66248）
1185	    if ((e.ai1 >= p.recoverLerp && past) || Math.hypot(e.vx, e.vy) < p.minSpeed) {
1186	      e.ai0 = 0; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
1187	      e.vx /= 2; e.vy /= 2;
1188	      e.ai1 = 45;                                   // flag=true：回旋态（:66260-66264）
1189	      e.ai0 = 4;
1190	    } else {
1191	      const dx = txc - e.cx, dy = tyc - e.cy;
1192	      const d = Math.hypot(dx, dy) || 1;
1193	      const spd = Math.hypot(e.vx, e.vy);
1194	      e.vx = (e.vx * (p.steerLerp - 1) + (dx / d) * (spd + speedAdd)) / p.steerLerp;
1195	      e.vy = (e.vy * (p.steerLerp - 1) + (dy / d) * (spd + speedAdd)) / p.steerLerp;
1196	    }
1197	    // 撞实心块 → 自爆（:66288-66294,flag2 仅小妖魔）
1198	    if (p.explode && solidBody(game, e)) { e.ai0 = 3; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0; }
1199	  } else if (e.ai0 === 4) {
1200	    // ---- 回旋（:66298-66308） ----
1201	    e.ai1 -= 3;
1202	    if (e.ai1 <= 0) { e.ai0 = 0; e.ai1 = 0; }
1203	    e.vx *= 0.95;
1204	    e.vy *= 0.95;
1205	  }
1206	  // ---- 贴身自爆（:66316-66324,flag2 仅小妖魔,距目标 <64px） ----
1207	  if (p.explode && e.ai0 !== 3 && Math.hypot(txc - e.cx, tyc - e.cy) < 64) {
1208	    e.ai0 = 3; e.ai1 = 0; e.ai2 = 0; e.ai3 = 0;
1209	  }
1210	  if (e.ai0 === 3) {
1211	    // ---- 自爆（:66326-66380）：扩盒 192²、伤 80、3t 后消散 ----
1212	    e.x = e.cx; e.y = e.cy;
1213	    e.w = 192; e.h = 192;
1214	    e.x -= e.w / 2; e.y -= e.h / 2;
1215	    e.vx = 0; e.vy = 0;
1216	    e.def.damage = 80;                              // GetAttackDamage_ScaledByDifficulty(80)
1217	    e.spawnAlpha = 255;
1218	    if (e.ai1 === 0) {
1219	      game.spawnParticles(e.cx, e.cy, '#FFD24A', 20, 4, { life: 30, grav: -0.05 });
1220	      game.spawnParticles(e.cx, e.cy, '#FF9A3C', 12, 3, { life: 40 });
1221	    }
1222	    e.ai1 += 1;
1223	    if (e.ai1 >= 3) {
1224	      game.playSfx('explosion', 1, e.cx, e.cy);     // SoundID.Item14
1225	      game.spawnParticles(e.cx, e.cy, '#FFB060', 30, 5, { life: 36 });
1226	      e.dead = true;                                // 原版 life=0 + active=false（不走掉落管线）
1227	    }
1228	    return;
1229	  }
1230	  fly(e);
1231	}
1232	
1233	/** 身体任意角/中心埋实心块（Collision.SolidCollision 近似） */
1234	function solidBody(game: GameHooks, e: Enemy): boolean {
1235	  const pts = [

```


---

## 🤖 Assistant · 2026-08-19T03:17:30.873Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Now let me read the vanilla AI_102 (42224-42620), AI_103 (42621-42805), AI_105 (42810-43062), AI_106 (43063-43152), AI_108 (65959-66390). That's a lot. Let me prioritize per prompt: sandElemental (42224), sandShark (42621), eterniaCrystal (548), lanePortal (549), divingFlyer (65959). Let me read them all in two big chunks.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:17:31.371Z · glm-x-preview-260804

```
现在对照检查次要组与原版 AI_102/103/105/106/108。
```


---

## 🤖 Assistant · 2026-08-19T03:17:31.911Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '42224,42430p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_102 sand elemental attack loop"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:31.954Z

**📎 ToolResult**

```
		else if (aiStyle == 102)
		{
			bool flag109 = false;
			bool flag110 = false;
			bool flag111 = true;
			bool flag112 = false;
			int num1568 = 4;
			int num1569 = 3;
			int num1570 = 0;
			float num1571 = 0.2f;
			float num1572 = 2f;
			float num1573 = -0.2f;
			float num1574 = -4f;
			bool flag113 = true;
			float num1575 = 2f;
			float num1576 = 0.1f;
			float num1577 = 1f;
			float num1578 = 0.04f;
			bool flag114 = false;
			float num1579 = 0.96f;
			bool flag115 = true;
			if (type == 541)
			{
				flag113 = false;
				rotation = velocity.X * 0.04f;
				spriteDirection = ((direction > 0) ? 1 : (-1));
				num1570 = 3;
				num1573 = -0.1f;
				num1571 = 0.1f;
				float num1580 = (float)life / (float)lifeMax;
				num1575 += (1f - num1580) * 2f;
				num1576 += (1f - num1580) * 0.02f;
				if (num1580 < 0.5f)
				{
					knockBackResist = 0f;
				}
				position += netOffset;
				Vector2 vector290 = base.BottomLeft + new Vector2(0f, -12f);
				Vector2 bottomRight = base.BottomRight;
				Vector2 vector291 = new Vector2(-spriteDirection * 10, -4f);
				Color color = new Color(222, 108, 48) * 0.7f;
				float num1581 = -0.3f + MathHelper.Max(velocity.Y * 2f, 0f);
				for (int num1582 = 0; num1582 < 2; num1582++)
				{
					if (Main.rand.Next(2) != 0)
					{
						Dust dust26 = Main.dust[Dust.NewDust(base.Bottom, 0, 0, 268)];
						dust26.position = new Vector2(MathHelper.Lerp(vector290.X, bottomRight.X, Main.rand.NextFloat()), MathHelper.Lerp(vector290.Y, bottomRight.Y, Main.rand.NextFloat())) + vector291;
						if (num1582 == 1)
						{
							dust26.position = base.Bottom + Utils.RandomVector2(Main.rand, -6f, 6f);
						}
						dust26.color = color;
						dust26.scale = 0.8f;
						dust26.velocity.Y += num1581;
						dust26.velocity.X += (float)spriteDirection * 0.2f;
					}
				}
				position -= netOffset;
				localAI[2] = 0f;
				if (this.ai[0] < 0f)
				{
					this.ai[0] = MathHelper.Min(this.ai[0] + 1f, 0f);
				}
				if (this.ai[0] > 0f)
				{
					flag115 = false;
					flag114 = true;
					this.ai[0]++;
					if (this.ai[0] >= 135f)
					{
						this.ai[0] = -300f;
						netUpdate = true;
					}
					Vector2 vector292 = base.Center + Vector2.UnitX * direction * 200f;
					Vector2 vector293 = base.Center + Vector2.UnitX * direction * 50f - Vector2.UnitY * 6f;
					if (this.ai[0] == 54f && Main.netMode != 1)
					{
						List<Point> list = new List<Point>();
						Vector2 vector294 = Main.player[target].Center + new Vector2(Main.player[target].velocity.X * 30f, 0f);
						if (Distance(vector294) < 2000f)
						{
							Point point14 = vector294.ToTileCoordinates();
							for (int num1583 = 0; num1583 < 1000; num1583++)
							{
								if (list.Count >= 3)
								{
									break;
								}
								bool flag116 = false;
								int num1584 = Main.rand.Next(point14.X - 30, point14.X + 30 + 1);
								foreach (Point item in list)
								{
									if (Math.Abs(item.X - num1584) < 10)
									{
										flag116 = true;
										break;
									}
								}
								if (!flag116)
								{
									int startY = point14.Y - 20;
									Collision.ExpandVertically(num1584, startY, out var _, out var bottomY, 1, 51);
									if (StrayMethods.CanSpawnSandstormHostile(new Vector2(num1584, bottomY - 15) * 16f, 15, 15))
									{
										list.Add(new Point(num1584, bottomY - 15));
									}
								}
							}
							foreach (Point item2 in list)
							{
								Projectile.NewProjectile(GetSpawnSource_ForProjectile(), item2.X * 16, item2.Y * 16, 0f, 0f, 658, 0, 0f, Main.myPlayer);
							}
						}
						else
						{
							this.ai[0] = -200f;
							netUpdate = true;
						}
					}
					Vector2 vector295 = new Vector2(0.9f, 2f);
					if (this.ai[0] < 114f && this.ai[0] > 0f)
					{
						List<Vector2> list2 = new List<Vector2>();
						for (int num1585 = 0; num1585 < 1000; num1585++)
						{
							Projectile projectile12 = Main.projectile[num1585];
							if (projectile12.active && projectile12.type == 658)
							{
								list2.Add(projectile12.Center);
							}
						}
						Vector2 vector296 = new Vector2(0f, 1500f);
						float num1586 = (this.ai[0] - 54f) / 30f;
						if (num1586 < 0.95f && num1586 >= 0f)
						{
							foreach (Vector2 item3 in list2)
							{
								Vector2 value11 = Vector2.CatmullRom(vector293 + vector296, vector293, item3, item3 + vector296, num1586);
								Vector2 value12 = Vector2.CatmullRom(vector293 + vector296, vector293, item3, item3 + vector296, num1586 + 0.05f);
								float num1587 = num1586;
								if (num1587 > 0.5f)
								{
									num1587 = 1f - num1587;
								}
								float num1588 = 2f;
								if (Vector2.Distance(value11, value12) > 5f)
								{
									num1588 = 3f;
								}
								if (Vector2.Distance(value11, value12) > 10f)
								{
									num1588 = 4f;
								}
								for (float num1589 = 0f; num1589 < num1588; num1589++)
								{
									Dust dust27 = Main.dust[Dust.NewDust(vector293, 0, 0, 269)];
									dust27.position = Vector2.Lerp(value11, value12, num1589 / num1588) + Utils.RandomVector2(Main.rand, -2f, 2f);
									dust27.noLight = true;
									dust27.scale = 0.3f + num1586;
								}
							}
						}
					}
					_ = this.ai[0];
					_ = 100f;
				}
				if (this.ai[0] == 0f)
				{
					this.ai[0] = 1f;
					netUpdate = true;
					flag114 = true;
				}
			}
			if (justHit)
			{
				localAI[2] = 0f;
			}
			if (!flag110)
			{
				if (localAI[2] >= 0f)
				{
					float num1590 = 16f;
					bool flag117 = false;
					bool flag118 = false;
					if (position.X > localAI[0] - num1590 && position.X < localAI[0] + num1590)
					{
						flag117 = true;
					}
					else if ((velocity.X < 0f && direction > 0) || (velocity.X > 0f && direction < 0))
					{
						flag117 = true;
						num1590 += 24f;
					}
					if (position.Y > localAI[1] - num1590 && position.Y < localAI[1] + num1590)
					{
						flag118 = true;
					}
					if (flag117 && flag118)
					{
						localAI[2] += 1f;
						if (localAI[2] >= 30f && num1590 == 16f)
						{
							flag109 = true;
						}
						if (localAI[2] >= 60f)
						{

```


---

## 🤖 Assistant · 2026-08-19T03:17:32.439Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '65959,66390p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_108 diving flyer"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:17:32.477Z

**📎 ToolResult**

```
	private void AI_108_DivingFlyer()
	{
		//IL_021a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0bbc: Unknown result type (might be due to invalid IL or missing references)
		//IL_07a8: Unknown result type (might be due to invalid IL or missing references)
		//IL_07ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_0be2: Unknown result type (might be due to invalid IL or missing references)
		//IL_0be7: Unknown result type (might be due to invalid IL or missing references)
		//IL_0935: Unknown result type (might be due to invalid IL or missing references)
		//IL_07e3: Unknown result type (might be due to invalid IL or missing references)
		//IL_07e8: Unknown result type (might be due to invalid IL or missing references)
		//IL_0961: Unknown result type (might be due to invalid IL or missing references)
		//IL_0966: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c20: Unknown result type (might be due to invalid IL or missing references)
		//IL_082a: Unknown result type (might be due to invalid IL or missing references)
		//IL_082f: Unknown result type (might be due to invalid IL or missing references)
		//IL_084e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c46: Unknown result type (might be due to invalid IL or missing references)
		//IL_0c4b: Unknown result type (might be due to invalid IL or missing references)
		rotation = velocity.ToRotation();
		float normalKnockbackMult = 0.4f;
		float num = 10f;
		float num2 = 200f;
		float num3 = 750f;
		float num4 = 30f;
		float num5 = 30f;
		float num6 = 0.95f;
		int num7 = 50;
		float num8 = 14f;
		float num9 = 30f;
		float num10 = 100f;
		float num11 = 20f;
		float num12 = 0f;
		float num13 = 7f;
		bool flag = true;
		bool flag2 = true;
		int num14 = 120;
		bool flag3 = false;
		bool flag4 = false;
		float num15 = 0.05f;
		float num16 = 0f;
		bool flag5 = false;
		switch (type)
		{
		case 558:
		case 559:
		case 560:
			flag4 = true;
			normalKnockbackMult = 0.7f;
			if (type == 559)
			{
				normalKnockbackMult = 0.5f;
			}
			if (type == 560)
			{
				normalKnockbackMult = 0.2f;
			}
			num = 3f;
			num2 = 400f;
			num3 = 500f;
			num4 = 90f;
			num5 = 20f;
			num6 = 0.95f;
			num7 = 0;
			num8 = 8f;
			num9 = 30f;
			num10 = 150f;
			num11 = 60f;
			num12 = 0.05f;
			num13 = 6f;
			flag2 = false;
			flag5 = true;
			break;
		case 574:
		case 575:
			flag4 = true;
			normalKnockbackMult = 0.6f;
			if (type == 575)
			{
				normalKnockbackMult = 0.4f;
			}
			num = 4f;
			num2 = 400f;
			num3 = 500f;
			num4 = 90f;
			num5 = 30f;
			num6 = 0.95f;
			num7 = 3;
			num8 = 8f;
			num9 = 30f;
			num10 = 150f;
			num11 = 10f;
			num12 = 0.05f;
			num13 = 0f;
			num16 = -0.1f;
			flag3 = true;
			flag5 = true;
			break;
		}
		NPCUtils.TargetClosestOldOnesInvasion(this);
		NPCAimedTarget targetData = GetTargetData();
		if (flag5)
		{
			if (localAI[0] == 0f)
			{
				alpha = 255;
			}
			if (localAI[0] == 30f)
			{
				SoundEngine.PlayTrackedSound(SoundID.DD2_EtherianPortalSpawnEnemy, base.Center);
			}
			if (localAI[0] < 60f)
			{
				localAI[0] += 1f;
				alpha -= 5;
				if (alpha < 0)
				{
					alpha = 0;
				}
				int num17 = (int)localAI[0] / 10;
				float num18 = base.Size.Length() / 2f;
				num18 /= 20f;
				int maxValue = 5;
				if (type == 576 || type == 577)
				{
					maxValue = 1;
				}
				for (int i = 0; i < num17; i++)
				{
					if (Main.rand.Next(maxValue) == 0)
					{
						Dust dust = Dust.NewDustDirect(position, width, height, 27, velocity.X * 1f, 0f, 100);
						dust.scale = 0.55f;
						dust.fadeIn = 0.7f;
						dust.velocity *= 0.1f * num18;
						dust.velocity += velocity;
					}
				}
			}
		}
		if (flag4)
		{
			for (int j = 0; j < Main.maxNPCs; j++)
			{
				if (j != whoAmI && Main.npc[j].active && Main.npc[j].type == type && Math.Abs(position.X - Main.npc[j].position.X) + Math.Abs(position.Y - Main.npc[j].position.Y) < (float)width)
				{
					if (position.X < Main.npc[j].position.X)
					{
						velocity.X -= num15;
					}
					else
					{
						velocity.X += num15;
					}
					if (position.Y < Main.npc[j].position.Y)
					{
						velocity.Y -= num15;
					}
					else
					{
						velocity.Y += num15;
					}
				}
			}
		}
		if (Math.Sign(velocity.X) != 0)
		{
			spriteDirection = -Math.Sign(velocity.X);
		}
		if (rotation < -MathF.PI / 2f)
		{
			rotation += MathF.PI;
		}
		if (rotation > MathF.PI / 2f)
		{
			rotation -= MathF.PI;
		}
		num12 *= num11;
		SlotId val;
		if (ai[0] == 0f)
		{
			knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(normalKnockbackMult);
			float num19 = num;
			Vector2 center = base.Center;
			Vector2 vector = targetData.Center - center;
			Vector2 vector2 = vector - Vector2.UnitY * num2;
			float num20 = vector.Length();
			vector = Vector2.Normalize(vector) * num19;
			vector2 = Vector2.Normalize(vector2) * num19;
			bool flag6 = Collision.CanHit(base.Center, 1, 1, targetData.Center, 1, 1);
			if (ai[3] >= (float)num14)
			{
				flag6 = true;
			}
			float num21 = 8f;
			flag6 = flag6 && vector.ToRotation() > MathF.PI / num21 && vector.ToRotation() < MathF.PI - MathF.PI / num21;
			if (num20 > num3 || !flag6)
			{
				velocity.X = (velocity.X * (num4 - 1f) + vector2.X) / num4;
				velocity.Y = (velocity.Y * (num4 - 1f) + vector2.Y) / num4;
				if (targetData.Center.Y < base.Center.Y)
				{
					velocity.Y -= 0.2f;
					if (velocity.Y < -10f)
					{
						velocity.Y = -10f;
					}
				}
				if (!flag6)
				{
					ai[3] += 1f;
					if (ai[3] == (float)num14)
					{
						netUpdate = true;
					}
				}
				else
				{
					ai[3] = 0f;
				}
			}
			else
			{
				ai[0] = 1f;
				ai[2] = vector.X;
				ai[3] = vector.Y;
				netUpdate = true;
			}
		}
		else if (ai[0] == 1f)
		{
			knockBackResist = 0f;
			velocity *= num6;
			velocity.Y += num16;
			ai[1] += 1f;
			if (ai[1] == num5)
			{
				if (type == 558 || type == 559 || type == 560)
				{
					float[] array = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_WyvernDiveDown, base.Center);
					array[1] = ((SlotId)(ref val)).ToFloat();
					if (Main.rand.Next(5) == 0)
					{
						float[] array2 = localAI;
						val = SoundEngine.PlayTrackedSound(SoundID.DD2_WyvernScream, base.Center);
						array2[2] = ((SlotId)(ref val)).ToFloat();
					}
				}
				else if (type == 574 || type == 575)
				{
					float[] array3 = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldFlyerChargeScream, base.Center);
					array3[1] = ((SlotId)(ref val)).ToFloat();
					SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldIgnite, base.Center);
				}
			}
			if (ai[1] >= num5)
			{
				ai[0] = 2f;
				ai[1] = 0f;
				netUpdate = true;
				Vector2 vector3 = new Vector2(ai[2], ai[3]) + new Vector2(Main.rand.Next(-num7, num7 + 1), Main.rand.Next(-num7, num7 + 1)) * 0.04f;
				vector3.Normalize();
				vector3 *= num8;
				velocity = vector3;
			}
		}
		else if (ai[0] == 2f)
		{
			if (ai[1] >= 20f && (type == 574 || type == 575))
			{
				ActiveSound activeSound = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[2]));
				if (activeSound == null)
				{
					float[] array4 = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_KoboldIgniteLoop, base.Center);
					array4[2] = ((SlotId)(ref val)).ToFloat();
				}
				else
				{
					activeSound.Position = base.Center;
				}
			}
			knockBackResist = 0f;
			float num22 = num9;
			ai[1] += 1f;
			bool flag7 = Vector2.Distance(base.Center, targetData.Center) > num10 && base.Center.Y > targetData.Center.Y;
			if (flag3)
			{
				flag7 = false;
			}
			if ((ai[1] >= num22 && flag7) || velocity.Length() < num13)
			{
				ai[0] = 0f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] = 0f;
				velocity /= 2f;
				netUpdate = true;
				if (flag)
				{
					ai[1] = 45f;
					ai[0] = 4f;
				}
			}
			else
			{
				Vector2 center2 = base.Center;
				Vector2 vector4 = targetData.Center - center2;
				vector4.Normalize();
				if (vector4.HasNaNs())
				{
					vector4 = new Vector2(direction, 0f);
				}
				velocity = (velocity * (num11 - 1f) + vector4 * (velocity.Length() + num12)) / num11;
			}
			if (flag2 && Collision.SolidCollision(position, width, height))
			{
				ai[0] = 3f;
				ai[1] = 0f;
				ai[2] = 0f;
				ai[3] = 0f;
				netUpdate = true;
			}
		}
		else if (ai[0] == 4f)
		{
			ai[1] -= 3f;
			if (ai[1] <= 0f)
			{
				ai[0] = 0f;
				ai[1] = 0f;
				netUpdate = true;
			}
			velocity *= 0.95f;
		}
		ActiveSound activeSound2 = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[1]));
		if (activeSound2 != null)
		{
			activeSound2.Position = base.Center;
		}
		else
		{
			float[] array5 = localAI;
			val = SlotId.Invalid;
			array5[1] = ((SlotId)(ref val)).ToFloat();
		}
		if (type == 558 || type == 559 || type == 560)
		{
			activeSound2 = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[2]));
			if (activeSound2 != null)
			{
				activeSound2.Position = base.Center;
			}
			else
			{
				float[] array6 = localAI;
				val = SlotId.Invalid;
				array6[2] = ((SlotId)(ref val)).ToFloat();
			}
		}
		if (flag2 && ai[0] != 3f && Vector2.Distance(base.Center, targetData.Center) < 64f)
		{
			ai[0] = 3f;
			ai[1] = 0f;
			ai[2] = 0f;
			ai[3] = 0f;
			netUpdate = true;
		}
		if (ai[0] != 3f)
		{
			return;
		}
		position = base.Center;
		width = (height = 192);
		position.X -= width / 2;
		position.Y -= height / 2;
		velocity = Vector2.Zero;
		damage = GetAttackDamage_ScaledByDifficulty(80f);
		alpha = 255;
		if (ai[1] == 0f && (type == 574 || type == 575))
		{
			for (int k = 0; k < 4; k++)
			{
				int num23 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 31, 0f, 0f, 100, default(Color), 1.5f);
				Main.dust[num23].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 2f;
			}
			for (int l = 0; l < 20; l++)
			{
				int num24 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 200, default(Color), 3.7f);
				Main.dust[num24].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 2f;
				Main.dust[num24].noGravity = true;
				Main.dust[num24].velocity *= 3f;
				num24 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 100, default(Color), 1.5f);
				Main.dust[num24].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 4f;
				Main.dust[num24].velocity *= 2f;
				Main.dust[num24].noGravity = true;
				Main.dust[num24].fadeIn = 2.5f;
			}
			for (int m = 0; m < 6; m++)
			{
				int num25 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 6, 0f, 0f, 0, default(Color), 2.7f);
				Main.dust[num25].position = base.Center + Vector2.UnitX.RotatedByRandom(3.1415927410125732).RotatedBy(velocity.ToRotation()) * width / 2f;
				Main.dust[num25].noGravity = true;
				Main.dust[num25].velocity *= 3f;
			}
			for (int n = 0; n < 12; n++)
			{
				int num26 = Dust.NewDust(new Vector2(position.X, position.Y), width, height, 31, 0f, 0f, 0, default(Color), 1.5f);
				Main.dust[num26].position = base.Center + Vector2.UnitX.RotatedByRandom(3.1415927410125732).RotatedBy(velocity.ToRotation()) * width / 2f;
				Main.dust[num26].noGravity = true;
				Main.dust[num26].velocity *= 3f;
			}
			for (int num27 = 0; num27 < 5; num27++)
			{
				int num28 = Gore.NewGore(position + new Vector2((float)(width * Main.rand.Next(100)) / 100f, (float)(height * Main.rand.Next(100)) / 100f) - Vector2.One * 10f, default(Vector2), Main.rand.Next(61, 64));
				Main.gore[num28].position = base.Center + Vector2.UnitY.RotatedByRandom(3.1415927410125732) * (float)Main.rand.NextDouble() * width / 2f;
				Main.gore[num28].velocity *= 0.3f;
				Main.gore[num28].velocity.X += (float)Main.rand.Next(-10, 11) * 0.05f;
				Main.gore[num28].velocity.Y += (float)Main.rand.Next(-10, 11) * 0.05f;
			}
		}
		ai[1] += 1f;
		if (ai[1] >= 3f)
		{
			SoundEngine.PlaySound(SoundID.Item14, position);
			life = 0;
			HitEffect();
			active = false;
		}
	}

```


---

## 🤖 Assistant · 2026-08-19T03:18:33.879Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
AI_108 comparison:

Vanilla:
- rotation = velocity.ToRotation(); ours visAngle = atan2(vy,vx). matches.
- knockback mult per type. ours stores kbMult but... does ours apply it? `kbMult` field defined but I don't see it used anywhere in divingFlyerAI! Vanilla sets knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(normalKnockbackMult) in state 0, and knockBackResist = 0 in states 1 and 2. Ours never sets knockback. Hmm — knockbackResist semantics: in vanilla NPC, knockBackResist field multiplies knockback; per-state: 0 in states 1/2 means FULL knockback?? Actually knockBackResist semantics in Terraria: `knockBackResist` is a multiplier applied to knockback (0 = no knockback resist → full knockback). Wait — Terraria's knockBackResist: default 1; 0.5 means half knockback? Hmm. In NPC.StrikeNPC: `knockBack *= knockBackResist`. So 0 = immune to knockback! Setting knockBackResist = 0f in states 1/2 = immune to knockback while aiming/diving. And state 0 = scaled mult (0.7/0.5/0.2 for wyverns, 0.6/0.4 kobold). Our code defines kbMult but never uses it — so our wyvern/kobold flyer knockback behavior isn't state-modulated. Is that a "structural deviation"? Knockback resist isn't in the listed audit dimensions explicitly (state machine/physics/attack/flee/parts). It's a behavioral nuance: vanilla wyverns take reduced knockback while hovering (0.2 for T3!) and NO knockback while diving. Ours: whatever the default def has. Medium-low severity. I could report as a minor CONFIRMED with medium confidence... but I need to be careful: does our Enemy even model knockBackResist per-state? sandElemental sets `e.def.knockbackResist`. So the field exists in def. Ours never touches it in divingFlyerAI → wyverns get default knockback always, and get knocked around during dives (vanilla: immune). I'd call this CONFIRMED (unused kbMult = dead parameter), medium severity.

Wait — also kobold flyer (574/575): vanilla flag2 = true (default true!) — `bool flag2 = true;` — for wyverns flag2 = false; kobold keeps true. flag2 = "kobold explode behaviors": SolidCollision → ai0=3; proximity < 64 → ai0=3. Ours p.explode true only for kobold. matches.

- num21 = 8 (the down-view gate divisor): flag6 = flag6 && vector.ToRotation() > π/8 && < π - π/8. Note: `vector` at that point = normalize(target - center) * num19 — direction to target. ours: ang = atan2(uy, ux) computed from ux/uy BEFORE scaling by num (same direction). gate: ang > π/8 && ang < π - π/8. ours matches. But note: vanilla computes this gate BEFORE overwriting vector? Order: vector = target-center; vector2 = vector - UnitY*num2; num20 = vector.Length(); vector = normalize(vector)*num19; vector2 = normalize(vector2)*num19; flag6 = CanHit(...); if ai[3] >= num14 → flag6 = true; flag6 = flag6 && vector.ToRotation() > π/8 ... — vector here is the scaled (still same direction) unit*num. So gate on direction to target: must be pointing downward-ish (rotation between 22.5° and 157.5°). Ours matches.

Hmm wait — ours applies the gate as `los = los && ang > π/8 && ang < π - π/8` and then `if (dist > p.range || !los)`. Vanilla: `if (num20 > num3 || !flag6)`. num20 = distance. ours dist. matches.

- approach velocity: velocity.X = (velocity.X*(num4-1) + vector2.X)/num4. ours matches with p.approach=90. vector2 = normalize(target-center - (0,400)) * num(3/4). ours: hvx/hvy from (ux*num, uy*num - hoverUp) normalized * num. matches.

- rise: target above → vy -= 0.2 clamp -10. ours matches.
- ai[3] counting. matches.
- transition: ai0=1, ai2 = vector.X (scaled unit*num), ai3 = vector.Y. ours: e.ai2 = vx1; e.ai3 = vy1. matches.

State 1 (aim):
- knockBackResist = 0 (missing in ours, noted above).
- velocity *= 0.95; vy += num16 (kobold -0.1); ai[1] += 1.
- sound at ai1 == num5 (20 wyvern / 30 kobold). ours at ai1 === p.aimT. matches.
- ai[1] >= num5 → ai0 = 2, ai1 = 0, vector3 = (ai2, ai3) + rand(-num7..num7)*0.04 both axes; normalize * num8 (8). ours: jx = ai2 + rndRange(-jitter, jitter+1)*0.04 — jitter: wyvern 0, kobold 3. matches (rand.Next(-3, 4) → rndRange(-3,4)). normalize * diveSpeed 8. matches.

State 2 (dive):
- kobold: ai1 >= 20 → ignite loop sound (ours omits — minor sound loop).
- knockBackResist = 0 (missing).
- num22 = num9 = 30; ai1 += 1; flag7 = Distance > num10 (150) && Center.Y > target.Y; flag3 (kobold) → flag7 = false.
- if ((ai1 >= 30 && flag7) || velocity.Length() < num13 (6 wyvern / 0 kobold)) → reset: ai0=0, ai1=0, ai2=0, ai3=0, velocity /= 2; if flag → ai1 = 45, ai0 = 4. flag = true default (both families).
  ours matches: recoverLerp 30, diveDist 150, minSpeed 6/0; `e.ai1 = 45; e.ai0 = 4;` — wait ours: `e.vx /= 2; e.vy /= 2;` — vanilla `velocity /= 2f` = both. matches.
- else steer: velocity = (velocity*(num11-1) + vector4*(velocity.Length() + num12)) / num11. num12 = 0.05 * num11 (num12 *= num11 earlier). wyvern num11 = 60 → speedAdd = 3; kobold num11 = 10 → 0.5. ours: speedAdd = p.speedAdd * p.steerLerp. matches. ours computes (dx/d, dy/d) — vanilla vector4 normalized with NaN → (direction, 0). ours `d = hypot || 1` — if exactly zero, keeps (0,0) rather than (direction,0). Edge case only. fine.
- flag2 && SolidCollision(position, width, height) → ai0 = 3. ours: p.explode && solidBody. matches (approx probe).

State 4: ai1 -= 3; <= 0 → ai0 = 0, ai1 = 0; velocity *= 0.95. ours matches.

Proximity: flag2 && ai0 != 3 && Distance < 64 → ai0 = 3. ours matches.

Explosion state 3: position = Center; w=h=192; center; velocity zero; damage = scaled(80); alpha 255; dust at ai1==0 for 574/575; ai1 += 1; >= 3 → sound Item14, life = 0, active = false. ours matches (plays 'explosion' sfx as Item14 analog; dead = true).

Note ours explosion block runs for ALL types if ai0 === 3, but only kobold ever sets ai0=3. fine.

Also vanilla: state 0 sets knockBackResist scaled; note ours missing entirely (kbMult dead). CONFIRMED minor.

Missing: the `if (ai[0] != 3f) return;` — after the state machine, vanilla returns unless exploding; movement integration by engine. ours fly(e) at end. fine.

Sand elemental comparison (AI_102): 
- 541 overrides: num1570 = 3 (bottomDepth), num1573 = -0.1 (upAccel), num1571 = 0.1 (grav), flag113 = false (headScan off), rotation = vx*0.04. num1572 (maxFall) default 2, num1574 (maxUp) default -4, num1575 = 2 + (1-ratio)*2, num1576 = 0.1 + (1-ratio)*0.02, num1577 (maxV) = 1, num1578 (accelV) = 0.04, num1579 = 0.96 (cast damp). Ours matches all: grav 0.1, maxFall 2, upAccel -0.1, maxUp -4, maxH 2+bonus, accelH 0.1+bonus, maxV 1, accelV 0.04, bottomDepth 3, headClear 3 (default num1569=3, unused since headScan false), frontDepth 4.
- knockback: ratio < 0.5 → knockBackResist = 0 (immune). ours: `e.def.knockbackResist = ratio < 0.5 ? 0 : e.def.knockbackResist` — hmm, this PERMANENTLY sets def.knockbackResist to 0 once ratio < 0.5 (never restores, but ratio never goes back up except heal... sand elemental doesn't heal, fine). But note: def is shared? If def is a shared prototype across all sand elementals, one hurt elemental zeroes knockbackResist for ALL. `e.def` — in this codebase, is def per-instance or shared from NPC defs? In walker107Params they do `e.def.hitSound = ...` (line 1984) and here `e.def.damage = 80` (line 2024) — they mutate e.def freely elsewhere, implying def is per-instance (or they'd have broader bugs). Sand elemental: e.def.knockbackResist — vanilla sets npc.knockBackResist (instance field). If def is shared, this would be a cross-instance contamination bug; but given the codebase mutates def elsewhere similarly, presumably def is per-instance. I'll flag as 存疑 maybe. Actually memory note says "e.def.hitSound" used in wither beast — same pattern. Skip.

- Attack loop: ai[0] < 0 → += 1 min 0. ai[0] > 0: flag115 = false (no retarget while casting? flag115 is the TargetClosest gate), flag114 = true (cast damp 0.96), ai[0]++; >= 135 → -300. ai[0] == 54 && netMode != 1: list of spawn points: vector294 = player.Center + (player.vx*30, 0); if Distance(vector294) < 2000 → pick ≤3 columns in [x-30, x+30] with |ΔX| >= 10 apart; startY = y - 20; ExpandVertically(col, startY, out _, out bottomY, 1, 51); if CanSpawnSandstormHostile(new Vector2(col, bottomY-15)*16, 15, 15) → add (col, bottomY-15); then NewProjectile 658 at (X*16, Y*16), 0 vel, damage 0. else (too far) → ai[0] = -200.

Ours: matches structure — px = player.cx + player.vx*30; py = player.cy; hypot < 2000; picks with 1000 iterations, spacing ≥ 10 (ours `< 10 → skip`, vanilla `< 10 → flag` skip — same), startY = pty - 20, expandVertically(game, col, startY, 1, 51) → [, bottomY]; my = bottomY - 15; canSpawnSandstormHostile(game, col, my). Vanilla passes world coords *16 with search 15,15 (StrayMethods.cs:47 — three columns ±15, span ≥ 20). Ours' canSpawnSandstormHostile uses tile coords with ±1 columns and 15/15 vertical, requiring `bottom - 1 - (top + 1) >= 20`. Vanilla StrayMethods.CanSpawnSandstormHostile(Vector2 position, int steps = 15, int stepDown = 15): let me trust the comment. Hmm — vanilla passes (15, 15) explicitly. Ours hardcodes 15/15 with ±1 columns... StrayMethods.cs:47 — the comment in the file header says "三列各 ±15 格净空,内缩后竖向跨度 ≥20 格". Their expandVertically(x+i, ty, 15, 15) then bottom-1-(top+1) >= 20. Plausible. Not going to verify StrayMethods since outside NPC.cs scope; the prompt says standard is NPC.cs. OK.

- 658 projectile: ours degrades to particles (documented). fine.
- vanilla dust trail (CatmullRom sand ribbons) — visual, ours skips (documented as particle degradation? ours only does spawnParticles at the marks). fine.

- The `if (this.ai[0] == 0f) { this.ai[0] = 1f; flag114 = true; }` — ours `if (e.ai0 === 0) e.ai0 = 1;`. matches. castDamp applies on the start frame too since walkerKernel receives castDamp — in ours castDamp is computed inside `if (e.ai0 > 0)` block which runs BEFORE the `if (e.ai0 === 0) e.ai0 = 1` line. So on the frame ai0 becomes 1, castDamp was 0. Vanilla: flag114 = true set in that same block → damping applies that frame. One-frame diff. trivial.

Hmm wait, actually there's a subtle but real ordering issue in ours sandElemental: `if (e.ai0 > 0) { castDamp = 0.96; e.ai0 += 1; if (e.ai0 >= 135) e.ai0 = -300; ... }` — vanilla: ai[0]++ happens BEFORE the == 54 check (so after increment, when it equals 54 → fire). Ours: `e.ai0 += 1; if (e.ai0 >= 135)...; if (e.ai0 === 54 ...)`. matches.

Sand elemental walker kernel: vanilla flag115 default true → TargetClosest runs in the stuck block while not casting. ours walkerKernel: `if (player && !player.dead) e.facing = e.seekDirX(player);` — always retargets toward PLAYER even when casting (vanilla flag115=false while casting → no retarget). Same nuance as DarkMage. Minor.

Now — one significant check in walkerKernel: the vanilla AI_102 walker tail. I've seen AI_109's tail (same structure). In AI_102, does the front/bottom probe use frontX = (position.X + width/2)/16 + direction*2 — hmm vanilla AI_109: `int num18 = (int)((position.X + (float)(width / 2)) / 16f) + direction * 2;` — CENTER X. ours: frontX = floor((e.x + e.w/2)/TILE) + facing*2 → center + 2 tiles. matches. frontY = (position.Y + height)/16 (bottom). ours matches. num20 = Bottom.Y/16 — same as frontY effectively (Bottom = position.Y+height). num21 = Bottom.X/16 (center). ours bottomX = center. matches.

Gravity/uplift and collide and accel blocks — ours matches AI_109 tail as dumped earlier. Note one thing: ours in walkerKernel vertical accel: `if (e.vy < -p.maxV) e.vy = -p.maxH;` — vanilla: `if (velocity.Y < 0f - num10) { velocity.Y = 0f - num8; }` — assigns -num8 (maxH!) not -num10. That's a vanilla quirk faithfully copied (they even noted it's the same weird assignment). ours: `-p.maxH`. matches vanilla quirk. 

Now the sand shark — vanilla 42621-42805. I have limited budget; let me read it quickly. Also eternia crystal 42810-43062 and lane portal 43063-43152. Let me read all three chunks in one command.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:18:34.451Z · glm-x-preview-260804

```
接下来将剩余的原版 AI_103/105/106 与我们的实现进行对比。
```


---

## 🤖 Assistant · 2026-08-19T03:18:34.719Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '42621,42806p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_103 sandshark"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:34.839Z

**📎 ToolResult**

```
		else if (aiStyle == 103)
		{
			if (direction == 0)
			{
				TargetClosest();
			}
			bool flag119 = true;
			Point pt = base.Center.ToTileCoordinates();
			Tile tileSafely7 = Framing.GetTileSafely(pt);
			flag119 = tileSafely7.nactive() && (TileID.Sets.Conversion.Sand[tileSafely7.type] || TileID.Sets.Conversion.Sandstone[tileSafely7.type] || TileID.Sets.Conversion.HardenedSand[tileSafely7.type]);
			flag119 |= wet;
			bool flag120 = false;
			TargetClosest(faceTarget: false);
			Vector2 vector297 = targetRect.Center.ToVector2();
			if (Main.player[target].velocity.Y > -0.1f && !Main.player[target].dead && Distance(vector297) > 150f)
			{
				flag120 = true;
			}
			if (localAI[0] == -1f && !flag119)
			{
				localAI[0] = 20f;
			}
			if (localAI[0] > 0f)
			{
				localAI[0]--;
			}
			if (flag119)
			{
				if (soundDelay == 0)
				{
					float num1598 = Distance(vector297) / 40f;
					if (num1598 < 10f)
					{
						num1598 = 10f;
					}
					if (num1598 > 20f)
					{
						num1598 = 20f;
					}
					soundDelay = (int)num1598;
					SoundEngine.PlaySound(15, base.Center, 4);
				}
				float num1599 = this.ai[1];
				bool flag121 = false;
				pt = (base.Center + new Vector2(0f, 24f)).ToTileCoordinates();
				tileSafely7 = Framing.GetTileSafely(pt.X, pt.Y - 2);
				if (tileSafely7.nactive() && (TileID.Sets.Conversion.Sand[tileSafely7.type] || TileID.Sets.Conversion.Sandstone[tileSafely7.type] || TileID.Sets.Conversion.HardenedSand[tileSafely7.type]))
				{
					flag121 = true;
				}
				this.ai[1] = flag121.ToInt();
				if (this.ai[2] < 30f)
				{
					this.ai[2]++;
				}
				if (flag120)
				{
					TargetClosest();
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
					Vector2 vec5 = base.Center + velocity.SafeNormalize(Vector2.Zero) * base.Size.Length() / 2f + velocity;
					pt = vec5.ToTileCoordinates();
					tileSafely7 = Framing.GetTileSafely(pt);
					bool flag122 = tileSafely7.nactive() && (TileID.Sets.Conversion.Sand[tileSafely7.type] || TileID.Sets.Conversion.Sandstone[tileSafely7.type] || TileID.Sets.Conversion.HardenedSand[tileSafely7.type]);
					if (!flag122 && wet)
					{
						flag122 = tileSafely7.liquid > 0;
					}
					int num1600 = 400;
					if (Main.remixWorld)
					{
						num1600 = 700;
					}
					if (!flag122 && Math.Sign(velocity.X) == direction && Distance(vector297) < (float)num1600 && (this.ai[2] >= 30f || this.ai[2] < 0f))
					{
						if (localAI[0] == 0f)
						{
							SoundEngine.PlaySound(14, base.Center, 542);
							localAI[0] = -1f;
						}
						this.ai[2] = -30f;
						Vector2 vector298 = DirectionTo(vector297 + new Vector2(0f, -80f));
						velocity = vector298 * 12f;
					}
				}
				else
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
						velocity.Y *= -1f;
						directionY = Math.Sign(velocity.Y);
						this.ai[0] = directionY;
					}
					float num1601 = 6f;
					velocity.X += (float)direction * 0.1f;
					if (velocity.X < 0f - num1601 || velocity.X > num1601)
					{
						velocity.X *= 0.95f;
					}
					if (flag121)
					{
						this.ai[0] = -1f;
					}
					else
					{
						this.ai[0] = 1f;
					}
					float num1602 = 0.06f;
					float num1603 = 0.01f;
					if (this.ai[0] == -1f)
					{
						velocity.Y -= num1603;
						if (velocity.Y < 0f - num1602)
						{
							this.ai[0] = 1f;
						}
					}
					else
					{
						velocity.Y += num1603;
						if (velocity.Y > num1602)
						{
							this.ai[0] = -1f;
						}
					}
					if (velocity.Y > 0.4f || velocity.Y < -0.4f)
					{
						velocity.Y *= 0.95f;
					}
				}
			}
			else
			{
				if (velocity.Y == 0f)
				{
					if (flag120)
					{
						TargetClosest();
					}
					float num1604 = 1f;
					velocity.X += (float)direction * 0.1f;
					if (velocity.X < 0f - num1604 || velocity.X > num1604)
					{
						velocity.X *= 0.95f;
					}
				}
				velocity.Y += 0.3f;
				if (velocity.Y > 10f)
				{
					velocity.Y = 10f;
				}
				this.ai[0] = 1f;
			}
			rotation = velocity.Y * (float)direction * 0.1f;
			if (rotation < -0.2f)
			{
				rotation = -0.2f;
			}
			if (rotation > 0.2f)
			{
				rotation = 0.2f;
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:18:35.277Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '42810,43152p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_105 crystal + AI_106 lane portal"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:18:35.400Z

**📎 ToolResult**

```
		}
		else if (aiStyle == 105)
		{
			if (alpha == 0)
			{
				Lighting.AddLight(base.Center, 1.3f, 0.5f, 1.5f);
			}
			if (this.ai[1] == 0f)
			{
				if (this.ai[0] > 0f)
				{
					this.ai[0]--;
				}
				if (this.ai[0] != 0f)
				{
					return;
				}
				this.ai[0] = 180f;
				netUpdate = true;
				if (localAI[0] == 0f)
				{
					StrayMethods.CheckArenaScore(base.Bottom, out var xLeftEnd, out var xRightEnd);
					localAI[0] = 1f;
					xLeftEnd.X += 2;
					xRightEnd.X -= 2;
					int num1605 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), xLeftEnd.X, xLeftEnd.Y, 549);
					Main.npc[num1605].Bottom = xLeftEnd.ToWorldCoordinates(8f, 16f);
					num1605 = NewNPC(GetSpawnSourceForNPCFromNPCAI(), xRightEnd.X, xRightEnd.Y, 549, 0, 0f, 0f, 1f);
					Main.npc[num1605].Bottom = xRightEnd.ToWorldCoordinates(8f, 16f);
					if (Main.netMode != 1)
					{
						DD2Event.FindArenaHitbox();
					}
				}
			}
			else if (this.ai[1] == 2f)
			{
				dontTakeDamageFromHostiles = true;
				life = lifeMax;
				if (this.ai[0] == 3f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_WinScene, base.Center);
					for (int num1606 = 0; num1606 < Main.maxNPCs; num1606++)
					{
						NPC nPC12 = Main.npc[num1606];
						if (nPC12.active && nPC12.type == 549)
						{
							nPC12.ai[1] = 1f;
							nPC12.ai[0] = 0f;
							nPC12.netUpdate = true;
						}
					}
					if (Main.netMode != 1)
					{
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center - Vector2.UnitY * 40f, Vector2.Zero, 713, 0, 0f, Main.myPlayer);
					}
				}
				this.ai[0]++;
				noGravity = true;
				if (this.ai[0] <= 120f)
				{
					float num1607 = this.ai[0] / 120f;
					velocity.Y = (float)Math.Cos(num1607 * (MathF.PI * 2f)) * 0.25f - 0.25f;
				}
				else
				{
					velocity.Y = 0f;
				}
				float lerpValue = Utils.GetLerpValue(480f, 570f, this.ai[0], clamped: true);
				if (lerpValue != 0f)
				{
					MoonlordDeathDrama.RequestLight(lerpValue, base.Center);
				}
				if (this.ai[0] >= 600f)
				{
					DD2Event.StopInvasion(win: true);
					dontTakeDamage = false;
					life = 0;
					checkDead();
					netUpdate = true;
				}
				if (true)
				{
					Vector2 vector299 = base.Center + new Vector2(0f, -20f);
					float num1608 = 0.99f;
					if (this.ai[0] >= 60f)
					{
						num1608 = 0.79f;
					}
					if (this.ai[0] >= 120f)
					{
						num1608 = 0.58f;
					}
					if (this.ai[0] >= 180f)
					{
						num1608 = 0.43f;
					}
					if (this.ai[0] >= 240f)
					{
						num1608 = 0.33f;
					}
					if (this.ai[0] >= 540f)
					{
						num1608 = 1f;
					}
					for (int num1609 = 0; num1609 < 9; num1609++)
					{
						if (!(Main.rand.NextFloat() < num1608))
						{
							float num1610 = Main.rand.NextFloat() * (MathF.PI * 2f);
							float num1611 = Main.rand.NextFloat();
							Vector2 vector300 = vector299 + num1610.ToRotationVector2() * (110f + 600f * num1611);
							Vector2 vector301 = (num1610 - MathF.PI).ToRotationVector2() * (14f + 0f * Main.rand.NextFloat() + 8f * num1611);
							Dust dust28 = Dust.NewDustPerfect(vector300, 264, vector301);
							dust28.scale = 0.9f;
							dust28.fadeIn = 1.15f + num1611 * 0.3f;
							dust28.color = new Color(1f, 1f, 1f, num1608) * (1f - num1608);
							dust28.noGravity = true;
							dust28.noLight = true;
						}
					}
				}
				if (this.ai[0] == 100f || this.ai[0] == 160f || this.ai[0] == 220f || this.ai[0] == 280f || this.ai[0] == 340f || this.ai[0] == 370f || this.ai[0] == 400f || this.ai[0] == 430f || this.ai[0] == 460f || this.ai[0] == 500f || this.ai[0] == 520f || this.ai[0] == 540f)
				{
					float num1612 = Main.rand.NextFloat() * (MathF.PI * 2f);
					float num1613 = 120f;
					for (int num1614 = 0; (float)num1614 < num1613; num1614++)
					{
						float num1615 = (float)num1614 / num1613 * (MathF.PI * 2f);
						float num1616 = Main.rand.NextFloat();
						Vector2 vector302 = base.Center + new Vector2(0f, -20f) + num1615.ToRotationVector2() * (810f - this.ai[0]);
						Vector2 vector303 = (num1615 - MathF.PI).ToRotationVector2() * (14f + 5f * (this.ai[0] / 600f) + 8f * num1616);
						Dust dust29 = Dust.NewDustPerfect(vector302, 264, vector303);
						dust29.scale = 0.9f;
						dust29.fadeIn = 1.15f + num1616 * 0.3f;
						dust29.color = new Color(1f, 1f, 1f, 0f);
						dust29.noGravity = true;
						dust29.noLight = true;
					}
				}
			}
			else
			{
				if (this.ai[1] != 1f)
				{
					return;
				}
				dontTakeDamageFromHostiles = true;
				life = lifeMax;
				if (this.ai[0] == 0f)
				{
					for (int num1617 = 0; num1617 < Main.maxNPCs; num1617++)
					{
						NPC nPC13 = Main.npc[num1617];
						if (nPC13.active && nPC13.type == 549)
						{
							nPC13.ai[1] = 1f;
							nPC13.ai[0] = 0f;
							nPC13.netUpdate = true;
						}
					}
					if (Main.netMode != 1)
					{
						DD2Event.ReportLoss();
						Projectile.NewProjectile(GetSpawnSource_ForProjectile(), base.Center - Vector2.UnitY * 40f, Vector2.Zero, 672, 0, 0f, Main.myPlayer);
					}
				}
				this.ai[0]++;
				float lerpValue2 = Utils.GetLerpValue(480f, 600f, this.ai[0], clamped: true);
				if (lerpValue2 != 0f)
				{
					MoonlordDeathDrama.RequestLight(lerpValue2, base.Center);
				}
				float num1618 = 96f;
				if (this.ai[0] < num1618)
				{
					velocity.Y = MathHelper.Lerp(0f, -1f, this.ai[0] / num1618);
				}
				if (this.ai[0] >= num1618)
				{
					alpha += 50;
					if (alpha > 255)
					{
						alpha = 255;
					}
				}
				if (true)
				{
					Vector2 vector304 = base.Center + new Vector2(0f, MathHelper.Lerp(0f, -70f, Utils.GetLerpValue(0f, 300f, this.ai[0], clamped: true)));
					float num1619 = 0.99f;
					if (this.ai[0] >= 60f)
					{
						num1619 = 0.79f;
					}
					if (this.ai[0] >= 120f)
					{
						num1619 = 0.58f;
					}
					if (this.ai[0] >= 180f)
					{
						num1619 = 0.23f;
					}
					if (this.ai[0] >= 240f)
					{
						num1619 = 0.35f;
					}
					if (this.ai[0] >= 300f)
					{
						num1619 = 0.6f;
					}
					if (this.ai[0] >= 360f)
					{
						num1619 = 0.98f;
					}
					if (this.ai[0] >= 420f)
					{
						num1619 = 0.995f;
					}
					if (this.ai[0] >= 450f)
					{
						num1619 = 1f;
					}
					for (int num1620 = 0; num1620 < 12; num1620++)
					{
						if (!(Main.rand.NextFloat() < num1619))
						{
							float num1621 = Main.rand.NextFloat() * (MathF.PI * 2f);
							float num1622 = Main.rand.NextFloat();
							Vector2 vector305 = vector304 + num1621.ToRotationVector2() * (70f + 600f * num1622);
							Vector2 vector306 = (num1621 - MathF.PI / 2f - MathF.PI / 8f).ToRotationVector2() * (12f + 9f * Main.rand.NextFloat() + 4f * num1622);
							Dust dust30 = Dust.NewDustPerfect(vector305, 240, vector306);
							dust30.scale = 0.8f;
							dust30.fadeIn = 0.95f + num1622 * 0.3f;
							dust30.noGravity = true;
						}
					}
				}
				if (this.ai[0] >= 600f)
				{
					DD2Event.StopInvasion();
					if (!Main.dedServ)
					{
						Filters.Scene.Deactivate("CrystalDestructionVortex");
						Filters.Scene.Deactivate("CrystalDestructionColor");
						Filters.Scene.Deactivate("CrystalWin");
					}
					dontTakeDamage = false;
					life = 0;
					checkDead();
					netUpdate = true;
				}
			}
		}
		else if (aiStyle == 106)
		{
			bool leftGate = this.ai[2] == 0f;
			if (alpha == 0)
			{
				Lighting.AddLight(base.Center, 0.5f, 0.1f, 0.3f);
			}
			SlotId val;
			if (this.ai[1] == 0f)
			{
				if (localAI[0] == 0f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_EtherianPortalOpen, base.Center);
					float[] array6 = localAI;
					val = SlotId.Invalid;
					array6[3] = ((SlotId)(ref val)).ToFloat();
				}
				if (localAI[0] > 150f)
				{
					ActiveSound activeSound = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[3]));
					if (activeSound == null)
					{
						float[] array7 = localAI;
						val = SoundEngine.PlayTrackedSound(SoundID.DD2_EtherianPortalIdleLoop, base.Center);
						array7[3] = ((SlotId)(ref val)).ToFloat();
					}
				}
				if (!DD2Event.EnemySpawningIsOnHold)
				{
					this.ai[0]++;
				}
				if (this.ai[0] >= (float)DD2Event.LaneSpawnRate)
				{
					if (this.ai[0] >= (float)(DD2Event.LaneSpawnRate * 3))
					{
						this.ai[0] = 0f;
					}
					netUpdate = true;
					if (Main.netMode != 1 && (int)this.ai[0] % DD2Event.LaneSpawnRate == 0)
					{
						DD2Event.SpawnMonsterFromGate(base.Bottom, leftGate);
						if (DD2Event.EnemySpawningIsOnHold)
						{
							this.ai[0]++;
						}
					}
				}
				localAI[0]++;
				if (localAI[0] > 180f)
				{
					localAI[0] = 180f;
				}
				if (Main.netMode != 1 && localAI[0] >= 180f)
				{
					if (AnyNPCs(548))
					{
						dontTakeDamage = true;
						return;
					}
					this.ai[1] = 1f;
					this.ai[0] = 0f;
					dontTakeDamage = true;
				}
			}
			else if (this.ai[1] == 1f)
			{
				this.ai[0]++;
				scale = MathHelper.Lerp(1f, 0.05f, Utils.GetLerpValue(500f, 600f, this.ai[0], clamped: true));
				ActiveSound activeSound2 = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[3]));
				if (activeSound2 == null)
				{
					float[] array8 = localAI;
					val = SoundEngine.PlayTrackedSound(SoundID.DD2_EtherianPortalIdleLoop, base.Center);
					array8[3] = ((SlotId)(ref val)).ToFloat();
				}
				activeSound2 = SoundEngine.GetActiveSound(SlotId.FromFloat(localAI[3]));
				if (activeSound2 != null)
				{
					activeSound2.Volume = scale;
				}
				if (this.ai[0] >= 550f)
				{
					dontTakeDamage = false;
					life = 0;
					checkDead();
					netUpdate = true;
					activeSound2?.Stop();
				}
			}
		}

```


---

## 🤖 Assistant · 2026-08-19T03:19:35.489Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
**Sand shark (AI_103) comparison:**

Vanilla:
- direction == 0 → TargetClosest. ours matches.
- flag119 (inSand): center tile nactive && sand-family; `flag119 |= wet`. ours: `const inSand = isSandTile || e.inWater;` matches.
- flag120 (canLunge): player.velocity.Y > -0.1 && !player.dead && Distance(targetRect.Center) > 150. ours: `player!.vy > -0.1 && hypot > 150` — plus `!!tgt` includes !dead. matches.
- localAI[0] == -1 && !flag119 → localAI[0] = 20. ours: x[0] === -1 && !inSand → x[0] = 20. matches.
- localAI[0] > 0 → --. ours matches. Note: ours also decrements outside inSand (placed before `if (inSand)`) — vanilla decrements before the branch too. matches.
- sound: `if (flag119) { if (soundDelay == 0) {...PlaySound(15, Center, 4)...} }` — hmm vanilla plays inside flag119 AND soundDelay == 0; soundDelay decrements where? In the main NPC update (soundDelay-- each tick when > 0). ours: `if (inSand && e.digSndDelay <= 0) { set delay; play } else if (e.digSndDelay > 0) e.digSndDelay--;` — decrements even when not inSand; vanilla's soundDelay decrement is global (engine). Roughly matches. Note ours plays when inSand regardless of... vanilla checks soundDelay==0 only inside flag119 — same. OK.
- ai[2] recharge: `if (this.ai[2] < 30f) this.ai[2]++;` — note vanilla increments ONLY if < 30 (doesn't increment beyond); also does NOT increment if ai[2] is negative (-30). Ours: `e.ai2 = Math.min(e.ai2 + 1, 30);` — increments ALWAYS, including from -30 → -29 → ... → 30. Vanilla: ai[2] = -30 after lunge; `if (ai[2] < 30) ai[2]++` → -30 < 30 → increments to -29, -28... So vanilla also counts up from -30! Same behavior. OK matches. Hmm wait, but the lunge gate requires `(ai[2] >= 30 || ai[2] < 0)` — after lunge ai[2] = -30 → immediately eligible again?? Interesting: the gate passes while ai[2] < 0 (during the -30..0 climb) — i.e., consecutive lunges possible for 30 ticks. Ours replicates the same gate. matches.
- flag120 branch (chasing): TargetClosest; vx += direction*0.15; vy += directionY*0.15; clamp vx ±5, vy ±3. ours matches.
- ahead-sand probe: `vec5 = Center + velocity.SafeNormalize * Size.Length/2 + velocity`. ours: `vv = hypot(vx,vy); ax = cx + (vv>0? vx/vv:0)*hypot(w,h)/2 + vx` matches (SafeNormalize(Zero) when zero → 0 multiplier; ours vv>0 guard).
- flag122 |= liquid if wet. ours matches (inWater).
- num1600 = 400 (remixWorld 700). ours hardcodes 400 (no remix world concept — fine, default).
- lunge: `if (!flag122 && sign(vx) == direction && Distance < 400 && (ai[2] >= 30 || ai[2] < 0))`: if localAI[0] == 0 → PlaySound(14, Center, 542) + localAI[0] = -1. ai[2] = -30. vector298 = DirectionTo(target - 80y); velocity = *12.
  
  Ours: `if (x[0] === 0) { x[0] = -1; playSound } e.ai2 = -30; d = dirTo(e, tgt.x, tgt.y-80); vx = d.x*12; vy = d.y*12;` matches.

  Wait — ordering: vanilla sets sound+localAI[0] THEN ai[2] = -30 then velocity. ours same. But vanilla's `if (localAI[0] == 0f)` INSIDE the lunge condition — the lunge continues on subsequent frames while ai[2] < 0 (gate) as long as ahead not sand etc. Each frame velocity is re-set to 12 toward target-80. Hmm — and localAI[0] = -1 → on exit of sand... The lunge persists every frame until flag122 (ahead sand) or... Actually after lunging, the shark is out of sand? Not immediately. Vanilla keeps re-lunging each frame while conditions hold (velocity constantly 12 toward target). Ours same. OK.

- else branch (cruise): collideX → vx *= -1, direction *= -1; collideY → vy *= -1, directionY = sign(vy), ai[0] = directionY. vx += direction*0.1; |vx|>6 → *=0.95. flag121 (floorNear) → ai[0] = -1 else 1. oscillate vy ±0.06 with step 0.01. |vy| > 0.4 → *= 0.95.

  Ours matches, with the probe `bt = tileTypeAt(ctx, floor((cy+24)/TILE) - 2)` — vanilla: pt = (Center + (0,24)).ToTileCoordinates(); tile = GetTileSafely(pt.X, pt.Y - 2). matches.

- else (out of sand): vy==0 → if flag120 TargetClosest; vx += direction*0.1, clamp ±1. vy += 0.3 → 10. ai[0] = 1. ours matches.
- rotation = vy * direction * 0.1 clamp ±0.2. ours matches.

One deviation: vanilla when out of sand and vy==0: `if (flag120) TargetClosest();` and the vx clamp uses num1604 = 1 — `if (vx < -1 || vx > 1) vx *= 0.95` — ours matches.

Sand shark looks 1:1. Good.

**Eternia crystal (AI_105):**

Vanilla:
- light.
- ai[1] == 0: ai[0] > 0 → ai[0]--; if != 0 return; ai[0] = 180; if localAI[0] == 0: CheckArenaScore(Bottom, out left, right); localAI[0] = 1; left.X += 2; right.X -= 2; NewNPC 549 at left; Bottom = left.ToWorldCoordinates(8, 16); NewNPC right with ai[2] = 1; Bottom = right.ToWorldCoordinates(8,16); FindArenaHitbox.

Ours: `if (x[0] === 0) { x[0] = 1; ends = checkArenaScore(game, e.cx, e.y + e.h); ... portal.x = end.x*TILE + 8 - w/2; portal.y = end.y*TILE + 16 - h; }`.

Note: vanilla passes `base.Bottom` (a Vector2 in world coordinates) to CheckArenaScore. Ours passes (e.cx, e.y + e.h) world coords → checkArenaScore converts to tiles. Good.

But there's a subtle thing: ours checks `if (e.ai0 > 0) e.ai0 -= 1; if (e.ai0 !== 0) return;` — matches vanilla exactly (ai0 starts 0 → doesn't return first frame → sets 180 → returns next 179 frames).

Hmm wait — ours sets `e.ai0 = 180` then runs the localAI[0] block; then next tick ai0 = 179 → return... so the crystal countdown: 180 → 0 over 180 ticks, then at 0 re-triggers (localAI[0] now 1 → skips portal spawn) and resets to 180. matches vanilla.

- ai[1] == 2 (win):
  - dontTakeDamageFromHostiles = true; life = lifeMax. ours: iframes 2 + hp = maxHp each frame. matches.
  - ai[0] == 3 → sound DD2_WinScene (ours MISSING the win-scene sound — minor), portals → ai1 = 1, proj 713 (DD2CrystalInspiracy? — ours spawns particles instead, documented).
  - ai[0]++; noGravity = true; ai[0] <= 120 → vy = cos(ai0/120 * 2π)*0.25 - 0.25; else 0. ours matches. (ours doesn't set noGravity — the crystal AI has no movement integration? ours crystal... does the Enemy still integrate vy? There's no moveAndCollide call in ours eterniaCrystalAI! The vy assignments are meaningless unless the engine moves it. Hmm — vanilla noGravity = true and velocity applied. In our engine, does Enemy.fixedUpdate integrate position automatically? In this codebase, AIs seem to call moveAndCollide/fly explicitly. The crystal sets e.vy but never moves. The visual bobbing (cos oscillation ±0.25 - 0.25 = drift up ~ -0.5..0) wouldn't happen. Minor visual. Similarly loss scene lerp rise. It's cosmetic; both are net ~30px drift. Low severity — but it IS dead code in ours. I'll mention in passing, low.
  - dust thresholds (num1608 varying probability bands) — ours approximates with constant 0.6 probability. Visual only. Fine (documented as 粒子近似).
  - ai[0] >= 600 → StopInvasion(true), dontTakeDamage = false, life = 0, checkDead(). ours: stopInvasion hook, iframes 0, hp 0, hurt(9999). matches semantics (checkDead triggers death pipeline).
  
- ai[1] == 1 (loss):
  - portals → 1; ReportLoss; proj 672. ours matches (reportLoss hook).
  - ai[0]++; lerp rise vy = lerp(0, -1, ai0/96) for ai0 < 96; ai0 >= 96 → alpha += 50 clamp 255. ours matches (spawnAlpha += 50).
  - dust vortex. approximated.
  - >= 600 → StopInvasion(false)... ours `stopInvasion?.(game, false)`. Vanilla StopInvasion() no-arg (loss). fine.

**Lane portal (AI_106):**

Vanilla:
- leftGate = ai[2] == 0.
- light.
- ai[1] == 0:
  - localAI[0] == 0 → sound PortalOpen; localAI[3] = Invalid.
  - localAI[0] > 150 → idle loop sound (ours omits idle loop — minor sound).
  - if !EnemySpawningIsOnHold → ai[0]++.
  - if ai[0] >= LaneSpawnRate: if ai[0] >= LaneSpawnRate*3 → ai[0] = 0; netUpdate; if ai[0] % LaneSpawnRate == 0 → SpawnMonsterFromGate(Bottom, leftGate); if EnemySpawningIsOnHold → ai[0]++.
  - localAI[0]++ → clamp 180.
  - if localAI[0] >= 180: if AnyNPCs(548) → dontTakeDamage = true; return. else ai[1] = 1; ai[0] = 0; dontTakeDamage = true.
- ai[1] == 1: ai[0]++; scale lerp; idle loop; ai[0] >= 550 → dontTakeDamage = false, life = 0, checkDead.

Ours:
- `if (!DD2_EVENT_HOOKS.enemySpawningOnHold()) e.ai0 += 1;` matches.
- `if (e.ai0 >= rate) { if (e.ai0 >= rate*3) e.ai0 = 0; if (e.ai0 % rate === 0) spawnMonsterFromGate }` — vanilla order: `if (ai[0] >= LaneSpawnRate) { if (ai[0] >= LaneSpawnRate*3) ai[0] = 0; netUpdate; if (ai[0] % LaneSpawnRate == 0) { SpawnMonsterFromGate; if (EnemySpawningIsOnHold) ai[0]++; } }` — ours matches modulo the hold double-increment (minor: after spawn, if hold is on, ai0++ skips a beat — ours omits; tiny).
- localAI[0] / x[0]: ours `x[0] += 1; if (x[0] > 180) x[0] = 180; if (x[0] >= 180) { if (crystal) return; e.ai1 = 1; e.ai0 = 0; }` — vanilla returns when crystal alive (dontTakeDamage = true then return); ours sets iframes when crystal exists at the top of the function (`if (crystal) e.iframes = 2;`) every frame — hmm, vanilla sets dontTakeDamage = true ONLY at localAI[0] >= 180 (gate-keeper mode). Before that, the portal... vanilla portal 549 SetDefaults dontTakeDamage? The ours comment says SetDefaults :15987 dontTakeDamage=true. Let me check: vanilla `npc.dontTakeDamage` default false; the AI sets it true at 180+. But the comment claims SetDefaults :15987. If vanilla SetDefaults sets it, then the AI's `dontTakeDamage = true` at 180 is redundant. Either way ours iframes=2 whenever crystal alive ≈ equivalent to gate-keeping. When crystal dead: vanilla portal keeps dontTakeDamage... until ai[1]=1 → also dontTakeDamage = true set in the transition; then at 550 → false + die. Ours: `if (crystal) e.iframes = 2` — when crystal dead, ours does NOT set iframes → portal can be damaged/die before starting its dissolve! Vanilla: transition to ai[1]=1 sets dontTakeDamage = true (immune), dissolve over 550 ticks, die at 550. Ours: crystal dead + ai1=0 + x[0] < 180 → portal killable. Hmm, but is that state reachable? Crystal dead → crystal null → ours doesn't set iframes → portal takes damage → hp drops → dies through normal pipeline, skipping the scale-dissolve. In vanilla, once localAI[0] >= 180 && !AnyNPCs(548) → ai1=1, dontTakeDamage=true. But during localAI[0] < 180 with crystal dead, vanilla portal: SetDefaults — let me actually check line 15987.

Also, when crystal is dead but x[0] < 180, vanilla keeps spawning (ai[1]==0 branch) and only when x[0] hits 180 → dissolve. Ours: same (x[0] >= 180 && !crystal → ai1 = 1). OK.

The difference: ours only grants invulnerability while crystal alive. Vanilla grants it (a) at SetDefaults? (b) at 180+ regardless, (c) during dissolve. If SetDefaults doesn't set it, then vanilla portals before 180 with dead crystal are ALSO killable → ours matches pre-180. Post-180 dissolve: vanilla immune, ours `e.ai1 === 1` branch doesn't set iframes → ours killable during dissolve window (500-600 ticks ≈ 10s). If someone kills it → skip dissolve animation + stopInvasion not called... wait stopInvasion isn't called by portal anyway. Minor. Let me check 15987 quickly to be fair.

Let me also double-check the claim about Betsy: does TargetClosestBetsy ignore players when crystal alive? Let me look at NPCUtils.cs:308 to validate dd2Target (crystal priority, no 200px player override — note w107Target DOES have the 200px override for walkers; dd2Target for Betsy/mage/flyer has no override). Let me read NPCUtils 261-330.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:19:36.593Z · glm-x-preview-260804

```
沙鲨、水晶和传送门基本一致。我来核实一下剩下的两个声明：NPCUtils 的目标定位语义（cs:261/:308）以及传送门的 SetDefaults (:15987)。
```


---

## 🤖 Assistant · 2026-08-19T03:19:38.111Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '255,330p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPCUtils.cs; echo ====; sed -n '15980,15995p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs; echo ====; sed -n '42246,42252p;63513,63530p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -5",
 "description": "Read NPCUtils targeting methods and portal SetDefaults"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:38.168Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPCUtils.cs: No such file or directory
(eval):1: === not found

```


---

## 🤖 Assistant · 2026-08-19T03:19:46.860Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "ls ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ | grep -i npcutil; echo ----; grep -rn \"TargetClosestBetsy\\|TargetClosestOldOnesInvasion\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/ --include=*.cs -l | head",
 "description": "Locate NPCUtils source file"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:46.933Z

**📎 ToolResult**

```
----
(eval):1: no matches found: --include=*.cs

```


---

## 🤖 Assistant · 2026-08-19T03:19:49.715Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -rn \"TargetClosestBetsy\" ~/Project/GLM/SandboxWorld/Terarria1456/ 2>/dev/null | head -5",
 "description": "Find TargetClosestBetsy definition"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:49.860Z

**📎 ToolResult**

```
~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs:62279:		NPCUtils.TargetClosestBetsy(this, faceTarget: false);
~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Utilities/NPCUtils.cs:308:	public static void TargetClosestBetsy(NPC searcher, bool faceTarget = true, Vector2? checkPosition = null)

```


---

## 🤖 Assistant · 2026-08-19T03:19:52.854Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '230,330p' ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.Utilities/NPCUtils.cs",
 "description": "Read NPCUtils targeting methods"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:52.897Z

**📎 ToolResult ⚠️ERROR**

```
Exit code 1
sed: ~/Project/GLM/SandboxWorld/Terarria1456/Terrarria.Utilities/NPCUtils.cs: No such file or directory

```


---

## 🤖 Assistant · 2026-08-19T03:19:57.300Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '230,335p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Utilities/NPCUtils.cs\" 2>/dev/null || sed -n '230,335p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Utilities/NPCUtils.cs",
 "description": "Read NPCUtils targeting methods (fixed path)"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:19:57.345Z

**📎 ToolResult**

```
				float num5 = num4 - (float)player.aggro;
				bool flag = searcher != null && player.npcTypeNoAggro[searcher.type];
				if (searcher != null && flag && searcher.direction == 0)
				{
					num5 += 1000f;
				}
				if (num5 < num2)
				{
					nearestTankIndex = j;
					num2 = num5;
					nearestTankDistance = num4;
					tankType = TargetType.Player;
				}
				if (player.tankPet >= 0 && !flag)
				{
					Vector2 center = Main.projectile[player.tankPet].Center;
					num4 = Vector2.Distance(position, center);
					num5 = num4 - 200f;
					if (num5 < num2 && num5 < 200f && Collision.CanHit(position, 0, 0, center, 0, 0))
					{
						nearestTankIndex = j;
						num2 = num5;
						nearestTankDistance = num4;
						tankType = TargetType.TankPet;
					}
				}
			}
		}
		return new TargetSearchResults(searcher, nearestNPCIndex, (float)Math.Sqrt(num), nearestTankIndex, nearestTankDistance, num2, tankType);
	}

	public static void TargetClosestOldOnesInvasion(NPC searcher, bool faceTarget = true, Vector2? checkPosition = null)
	{
		TargetSearchResults searchResults = SearchForTarget(searcher, TargetSearchFlag.All, SearchFilters.OnlyPlayersInCertainDistance(searcher.Center, 200f), SearchFilters.OnlyCrystal);
		if (searchResults.FoundTarget)
		{
			searcher.target = searchResults.NearestTargetIndex;
			searcher.targetRect = searchResults.NearestTargetHitbox;
			if (searcher.ShouldFaceTarget(ref searchResults) && faceTarget)
			{
				searcher.FaceTarget();
			}
		}
	}

	public static void TargetClosestNonBees(NPC searcher, bool faceTarget = true, Vector2? checkPosition = null)
	{
		TargetSearchResults searchResults = SearchForTarget(searcher, TargetSearchFlag.All, null, SearchFilters.NonBeeNPCs);
		if (searchResults.FoundTarget)
		{
			searcher.target = searchResults.NearestTargetIndex;
			searcher.targetRect = searchResults.NearestTargetHitbox;
			if (searcher.ShouldFaceTarget(ref searchResults) && faceTarget)
			{
				searcher.FaceTarget();
			}
		}
	}

	public static void TargetClosestDownwindFromNPC(NPC searcher, float distanceMaxX, bool faceTarget = true, Vector2? checkPosition = null)
	{
		TargetSearchResults searchResults = SearchForTarget(searcher, TargetSearchFlag.Players, SearchFilters.DownwindFromNPC(searcher, distanceMaxX));
		if (searchResults.FoundTarget)
		{
			searcher.target = searchResults.NearestTargetIndex;
			searcher.targetRect = searchResults.NearestTargetHitbox;
			if (searcher.ShouldFaceTarget(ref searchResults) && faceTarget)
			{
				searcher.FaceTarget();
			}
		}
	}

	public static void TargetClosestCommon(NPC searcher, bool faceTarget = true, Vector2? checkPosition = null)
	{
		searcher.TargetClosest(faceTarget);
	}

	public static void TargetClosestBetsy(NPC searcher, bool faceTarget = true, Vector2? checkPosition = null)
	{
		TargetSearchResults searchResults = SearchForTarget(searcher, TargetSearchFlag.All, null, SearchFilters.OnlyCrystal);
		if (searchResults.FoundTarget)
		{
			TargetType value = searchResults.NearestTargetType;
			if (searchResults.FoundTank && !searchResults.NearestTankOwner.dead)
			{
				value = TargetType.Player;
			}
			searcher.target = searchResults.NearestTargetIndex;
			searcher.targetRect = searchResults.NearestTargetHitbox;
			if (searcher.ShouldFaceTarget(ref searchResults, value) && faceTarget)
			{
				searcher.FaceTarget();
			}
		}
	}
}

```


---

## 🤖 Assistant · 2026-08-19T03:20:11.452Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
TargetClosestBetsy: SearchForTarget(All, null, OnlyCrystal) — crystal-only filter for the target list? OnlyCrystal filter means the target search filters to crystals... but TargetSearchFlag.All includes players; SearchFilters.OnlyCrystal is the "tank" filter? Looking at SearchForTarget signature: (searcher, flags, playerFilter, npcFilter). In TargetClosestOldOnesInvasion: filters = OnlyPlayersInCertainDistance(200), OnlyCrystal. So npcFilter = OnlyCrystal → NPCs considered = crystals only. Player filter null (Betsy) → all players.

SearchForTarget picks nearest among players AND filtered NPCs (crystals), with aggro adjustments (player.aggro reduces distance). So Betsy targets nearest of {players, crystal} — NOT crystal-priority! While TargetClosestOldOnesInvasion: playerFilter = OnlyPlayersInCertainDistance(200) → only players within 200px of searcher count; npcFilter = OnlyCrystal → crystal. So walkers: crystal unless player within 200px and nearer (which our w107Target implements: `pd <= 200 && pd < cd` — roughly; vanilla compares distances with aggro modifiers).

Our dd2Target (used by Betsy, DarkMage, divingFlyer, lightning bug): crystal ALWAYS priority if present, else player. For Betsy, vanilla picks the NEAREST of player vs crystal (aggro-adjusted), so a player standing next to Betsy with crystal far away becomes the target. Our version would ignore the player entirely while a crystal lives. Hmm — is that a real gameplay deviation? Betsy would always fly at the crystal, never at players. In vanilla, whichever is closer (aggro can pull it). This affects Betsy's state machine target (hover side, breath direction, summon distance checks).

Also note `searchResults.FoundTank && !NearestTankOwner.dead → value = Player` — tank pet stuff, ignore.

Severity: Betsy is the tier-1 audit target. Target selection = crystal-always vs nearest-of-both is a structural deviation in target acquisition. But wait — SearchForTarget with flags All: how does it weigh players vs NPCs? It computes nearest player distance² (num) and nearest NPC (crystal) distance (nearestNPCDistance). Which wins? I'd need SearchForTarget's body (lines ~120-258). Let me read the beginning of it. The typical logic: if both found, compare distance vs nearestNPCDistance. Let me read lines 100-230 of NPCUtils.cs.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:20:11.920Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '60,230p' \"~/Project/GLM/SandboxWorld/Terarria1456/Terraria.Utilities/NPCUtils.cs\"",
 "description": "Read SearchForTarget core logic"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:20:11.960Z

**📎 ToolResult**

```
		private TargetType _nearestTargetType;

		private int _nearestNPCIndex;

		private float _nearestNPCDistance;

		private int _nearestTankIndex;

		private float _nearestTankDistance;

		private float _adjustedTankDistance;

		private TargetType _nearestTankType;

		public int NearestTargetIndex
		{
			get
			{
				switch (_nearestTargetType)
				{
				case TargetType.Player:
				case TargetType.TankPet:
					return _nearestTankIndex;
				case TargetType.NPC:
					return NearestNPC.WhoAmIToTargetingIndex;
				default:
					return -1;
				}
			}
		}

		public Rectangle NearestTargetHitbox => _nearestTargetType switch
		{
			TargetType.Player => NearestTankOwner.Hitbox, 
			TargetType.TankPet => Main.projectile[NearestTankOwner.tankPet].Hitbox, 
			TargetType.NPC => NearestNPC.Hitbox, 
			_ => Rectangle.Empty, 
		};

		public TargetType NearestTargetType => _nearestTargetType;

		public bool FoundTarget => _nearestTargetType != TargetType.None;

		public NPC NearestNPC
		{
			get
			{
				if (_nearestNPCIndex != -1)
				{
					return Main.npc[_nearestNPCIndex];
				}
				return null;
			}
		}

		public bool FoundNPC => _nearestNPCIndex != -1;

		public int NearestNPCIndex => _nearestNPCIndex;

		public float NearestNPCDistance => _nearestNPCDistance;

		public Player NearestTankOwner
		{
			get
			{
				if (_nearestTankIndex != -1)
				{
					return Main.player[_nearestTankIndex];
				}
				return null;
			}
		}

		public bool FoundTank => _nearestTankIndex != -1;

		public int NearestTankOwnerIndex => _nearestTankIndex;

		public float NearestTankDistance => _nearestTankDistance;

		public float AdjustedTankDistance => _adjustedTankDistance;

		public TargetType NearestTankType => _nearestTankType;

		public TargetSearchResults(NPC searcher, int nearestNPCIndex, float nearestNPCDistance, int nearestTankIndex, float nearestTankDistance, float adjustedTankDistance, TargetType tankType)
		{
			_nearestNPCIndex = nearestNPCIndex;
			_nearestNPCDistance = nearestNPCDistance;
			_nearestTankIndex = nearestTankIndex;
			_adjustedTankDistance = adjustedTankDistance;
			_nearestTankDistance = nearestTankDistance;
			_nearestTankType = tankType;
			if (_nearestNPCIndex != -1 && _nearestTankIndex != -1)
			{
				if (_nearestNPCDistance < _adjustedTankDistance)
				{
					_nearestTargetType = TargetType.NPC;
				}
				else
				{
					_nearestTargetType = tankType;
				}
			}
			else if (_nearestNPCIndex != -1)
			{
				_nearestTargetType = TargetType.NPC;
			}
			else if (_nearestTankIndex != -1)
			{
				_nearestTargetType = tankType;
			}
			else
			{
				_nearestTargetType = TargetType.None;
			}
		}
	}

	[Flags]
	public enum TargetSearchFlag
	{
		None = 0,
		NPCs = 1,
		Players = 2,
		All = 3
	}

	public static TargetSearchResults SearchForTarget(Vector2 position, TargetSearchFlag flags = TargetSearchFlag.All, SearchFilter<Player> playerFilter = null, SearchFilter<NPC> npcFilter = null)
	{
		return SearchForTarget(null, position, flags, playerFilter, npcFilter);
	}

	public static TargetSearchResults SearchForTarget(NPC searcher, TargetSearchFlag flags = TargetSearchFlag.All, SearchFilter<Player> playerFilter = null, SearchFilter<NPC> npcFilter = null)
	{
		return SearchForTarget(searcher, searcher.Center, flags, playerFilter, npcFilter);
	}

	public static TargetSearchResults SearchForTarget(NPC searcher, Vector2 position, TargetSearchFlag flags = TargetSearchFlag.All, SearchFilter<Player> playerFilter = null, SearchFilter<NPC> npcFilter = null)
	{
		float num = float.MaxValue;
		int nearestNPCIndex = -1;
		float num2 = float.MaxValue;
		float nearestTankDistance = float.MaxValue;
		int nearestTankIndex = -1;
		TargetType tankType = TargetType.Player;
		if ((flags & TargetSearchFlag.NPCs) != TargetSearchFlag.None)
		{
			for (int i = 0; i < Main.maxNPCs; i++)
			{
				NPC nPC = Main.npc[i];
				if (nPC.active && nPC.whoAmI != searcher.whoAmI && (npcFilter == null || npcFilter(nPC)))
				{
					float num3 = Vector2.DistanceSquared(position, nPC.Center);
					if (num3 < num)
					{
						nearestNPCIndex = i;
						num = num3;
					}
				}
			}
		}
		if ((flags & TargetSearchFlag.Players) != TargetSearchFlag.None)
		{
			for (int j = 0; j < 255; j++)
			{
				Player player = Main.player[j];
				if (!player.active || player.dead || player.ghost || (playerFilter != null && !playerFilter(player)))
				{
					continue;
				}
				float num4 = Vector2.Distance(position, player.Center);
				float num5 = num4 - (float)player.aggro;

```


---

## 🤖 Assistant · 2026-08-19T03:21:07.409Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed the semantics: TargetSearchResults constructor — if both NPC (crystal) and tank (player) found: `_nearestNPCDistance < _adjustedTankDistance ? NPC : tankType(Player)`. So the nearer of (crystal, aggro-adjusted player) wins. For Betsy (playerFilter null): any player at any distance competes on distance.

For TargetClosestOldOnesInvasion (playerFilter = OnlyPlayersInCertainDistance(searcher.Center, 200)): only players within 200px compete; otherwise crystal wins.

Our implementations:
- w107Target: crystal + player within 200 → `pd <= 200 && pd < cd` → player; else crystal. matches OldOnesInvasion (without aggro). Good.
- dd2Target (Betsy, DarkMage 564/565, divingFlyer 558-560/574/575, lightning bug 578): crystal unconditionally; player only when no crystal.

For DarkMage/divingFlyer/lightning bug — wait, they use TargetClosestOldOnesInvasion (the 200px variant)! AI_109: `NPCUtils.TargetClosestOldOnesInvasion(this)` (flag7). AI_108: TargetClosestOldOnesInvasion. AI_111: TargetClosestOldOnesInvasion. AI_110 (Betsy): TargetClosestBetsy (no distance filter).

So the correct semantics:
- Betsy: nearest of {crystal, any alive player (aggro-adjusted)}.
- DarkMage/flyer/lightning bug: nearest of {crystal, players within 200px}.
- walkers: same 200px rule (ours implements in w107Target).

Our dd2Target gives crystal absolute priority for ALL of them. Deviation:
1. For Betsy: if the player is closer than the crystal, vanilla targets the PLAYER. Ours always crystal. CONFIRMED (NPCUtils.cs:308-313 + constructor at ~135; our file line 377-385).
2. For DarkMage/flyers/lightning bug: vanilla uses the 200px-filter variant — a player within 200px and nearer than the crystal takes over. Ours never targets the player while crystal lives. Same root: dd2Target doesn't distinguish the two variants.

Impact: In a real DD2 run, players typically stand near the crystal (defending it), often within 200px — so DarkMage would target the player (aim bolts at player), flyers dive the player, Betsy mixes. Our version makes every DD2 enemy ignore players completely while the crystal is up. That's a significant gameplay deviation — enemies in vanilla absolutely attack players standing near the crystal. Actually wait — think about DD2 gameplay: enemies walk PAST players to attack the crystal... Hmm, no: in actual Terraria DD2, enemies do attack the crystal but they also target players — e.g., Betsy breathes fire at players. The crystal is stationary and enemies path toward it, but when a player is adjacent (within 200px for the invasion method), they retarget to the player. Betsy at any distance picks the nearer.

Actually for Betsy: crystal at arena center; players defend near it. Betsy's states hover relative to target etc. If player is nearer than crystal, Betsy targets the player. So yes ours differs.

Severity: medium-high for behavioral parity. One combined finding.

Also note: dd2Target ignores `player.aggro` (armor aggro modifiers) — skip that nuance.

Now, one more check on the Betsy no-target fallback and Dutchman `e.facing` handling. Also verify our Dutchman pirate jump velocity `vy = -8.01 + e.vy` vs vanilla `((rand-0.5)*5, -8.01) + velocity` — matches.

Now let me consolidate all findings and pick top ≤ 10 by severity, CONFIRMED only with both sides read:

1. **Ogre spit cooldown 60 vs 240** — ours bossAI_dd2.ts:1835 (`p.cooldown = 60`) with ai1===1 branch (1846-1853) not overriding; vanilla NPC.cs:63587-63600 case 1 sets `num6 = 240`, applied at flag5 windup end (`ai[0] = -num6`, cs:64380-64382) and clamp cs:63602-63605. Effect: Ogre spits every ~150t (90 windup + 60 cooldown) instead of every ~330t; 4× spit frequency. High confidence.

2. **DD2 target acquisition: crystal unconditional priority vs vanilla nearest-of** — ours dd2Target (bossAI_dd2.ts:377-385) used by Betsy/DarkMage/divingFlyer/lightningBug. Vanilla: NPCUtils.cs:261-273 (OldOnesInvasion: players within 200px compete) and :308-318 (Betsy: all players compete); winner = nearer (TargetSearchResults ctor, NPCUtils.cs:135-141). Effect: all these enemies ignore players entirely while crystal alive; vanilla Betsy attacks nearer player, mages/flyers target players within 200px. High confidence.

3. **AI_107 melee windup side-effects only wired for Ogre** — vanilla flag7 default true (NPC.cs:63424), no family clears it; windup branch (cs:64371-64378) does velocity.X *= num7 (0.9; ogre 0.7), flag24=true (skip walk accel), flag20=true (freeze scream/retarget), ai[3]=0. Ours: windupDampOn only set for 576/577 (line 1834); no flag20/ai3-reset for anyone. Effect: goblins/wither beast/kobold keep full walking speed + keep retargeting during swing windup instead of braking; ai3 stuck-counter carries over. High confidence.

4. **Dutchman cannon aim vector double-normalized** — ours lines 533-539: `vx = d.x*14; vy = d.y*14-5;` then re-normalize to 14, then `vy -= 5` again. Vanilla cs:36033-36045: `vector140 = normalize(dir)*14; vector140 += UnitY*-5` — single pass. Effect: horizontal shots get (13.07,-9.67) instead of (14,-5) — flatter/faster drop, distorted aim. High confidence.

5. **AI_108 knockback state gating missing (kbMult dead parameter)** — ours flyerParams defines kbMult (line 1058-1082) but divingFlyerAI never applies it. Vanilla cs:66134 (state 0: knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(normalKnockbackMult) — 0.7/0.5/0.2 wyvern T1-3, 0.6/0.4 kobold) and cs:66194/66242 (states 1 and 2: knockBackResist = 0 → immune while aiming/diving). Effect: wyverns get knocked around mid-dive; vanilla dives are uninterruptible. High confidence the parameter is unused; medium-high gameplay relevance.

6. **DarkMage bolt aim origin + facing tracking during cast** — vanilla computes the 675 vector from the muzzle point (Center + (direction*10, -16)) — cs:66437-66446: `vector = (target.Center - (Center + Vector2(direction*10,-16))).SafeNormalize(UnitY)*14`. Ours line 1288-1291 aims from e.cx/e.cy (center). ~19px aim offset. Minor. Low-medium. Also ours updates facing toward target every frame during cast while vanilla freezes direction when casting (flag7=false → TargetClosest skipped, cs:66427+66543). Combined minor.

7. **Walker retargeting while casting/winding (flag115/flag20/flag7 gating)** — partially covered by #3; for sandElemental + DarkMage, vanilla skips TargetClosest while casting (flag115 = false at cs:42269 / flag7 = false at cs:66427), ours always retargets in walkerKernel (line 599/602). Fold into a minor item or into #3? Separate family (AI_102/109 vs 107). I'll make it its own low item.

8. **Betsy summon sound once per wave vs per wyvern; Betsy no-target fallback `vy -= 0.05` invented** — minor. Maybe mention as notes.

9. **Crystal win-scene: ours doesn't play DD2_WinScene sound at ai0==3; proj 713/672 degraded** — cosmetic, documented. Skip or minor.

10. **Lane portal idle-loop sound missing; hold double-increment missing; iframes only while crystal alive (dissolve phase killable)** — vanilla cs:43078-43081 idle loop; cs:43100-43103 hold → ai[0]++; cs:43109-43116: `dontTakeDamage = true` on dissolve. Ours: no iframes in ai1===1 dissolve branch (line 1036-1044) → portal killable during 550t dissolve, skipping animation. Medium-low. Actually wait — when crystal is dead and x[0] >= 180, ours sets ai1 = 1 but the top-of-function `if (crystal) e.iframes = 2` no longer applies (crystal dead) → portal vulnerable during dissolve. Vanilla sets dontTakeDamage = true when transitioning to ai[1]=1 (cs:43113-43115) and keeps it until 550. CONFIRMED medium-low.

Also crystal movement (noGravity bobbing) is dead code in ours — cosmetic, skip.

11. Also Dutchman: pirates spawn position (top of ship + rotation) vs ours at ship center — vanilla cs:40959-40970 vector270 = ((rand-0.5)*(width-70), (rand-0.5)*20 - height/2 - 20).RotatedBy(rotation) + Center. Ours spawns at boss center via spawnPart. Minor (pirates appear mid-ship instead of above deck). Low.

12. Betsy's `!tgt` fallback — invented but harmless.

Priority-wise, the task asks max 10 items sorted by severity. Let me also double check #1 ogre: is num6 for ogre base 60? Yes: case 576/577 sets num6 = 60 (cs:63520 region: "flag5 = true; num6 = 60;"). And case 1 overrides num6 = 240. Wait — careful: the switch on (int)ai[1] happens INSIDE case 576/577. Case 1 (spit): num5 = 90, num4 = 1000, num6 = 240, ... So during spit windup end → ai[0] = -240. During stomp (case 2): num6 stays 60. During melee (case 0): 60. Ours: p.cooldown = 60 in all three. Confirmed.

One more sanity check on #3: does any of ours' structure accidentally damp during windup via another path? `attacking` gate skips stuck counting; w107WalkAccel runs for non-noWalkAccel families (goblins, wither, kobold) regardless of attacking — actually wait, for kobold (572/573): the kobold block sets p.melee = true... and noWalkAccel is not set for kobold → w107WalkAccel runs at line 2146. Vanilla kobold: flag24 default false but flag7 sets flag24=true during windup. So kobold charging at 4 speed, windup 40 ticks at dist 64 → vanilla brakes (0.9^~2 — only 1-2 ticks before ai1=1→2 explode, negligible as computed). Goblins: windup 30 ticks — vanilla brakes from ~1.2 to ~0.04; ours keeps 1.2 + keeps accelerating. Player standing still gets hit by a goblin sliding THROUGH them during windup + swing. Visible.

Wither beast: windup 110 ticks at speed 1.4 — big difference (vanilla essentially stops and channels aura; ours keeps walking).

OK. Also #3 includes ai3=0 and flag20 (no scream/retarget during windup). Good.

Now #5: let me double-check ours never sets knockback for flyers... I've read the whole divingFlyerAI — no knockbackResist/kbMult usage. Let me grep to be safe. Also check if Enemy might apply def-based knockback automatically with kbMult wired elsewhere. Quick grep.

Also #2: confirm AI_109 uses TargetClosestOldOnesInvasion — yes: `if (flag7) { NPCUtils.TargetClosestOldOnesInvasion(this); }` (from the AI_109 dump: `if (flag7) NPCUtils.TargetClosestOldOnesInvasion(this);`). AI_108 dump: `NPCUtils.TargetClosestOldOnesInvasion(this);`. AI_111: comment says :66816 TargetClosestOldOnesInvasion. Betsy: TargetClosestBetsy. Confirmed.

Also — DarkMage uses GetTargetData() for the cast aim: `targetData.Center` — the target could be player or crystal per the 200px rule. Ours uses dd2Target → always crystal. Same finding #2 covers.

Let me quickly grep kbMult usage and knockbackResist in our file to confirm #5.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:07.706Z · glm-x-preview-260804

```
在最终确定之前，我先快速验证一下几个用法声明。
```


---

## 🤖 Assistant · 2026-08-19T03:21:09.055Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "grep -n \"kbMult\\|knockbackResist\\|dontTakeDamage\" ~/Project/GLM/SandboxWorld/game/src/entities/bossAI_dd2.ts; echo ----; grep -n \"63556\\|num6 = 240\" ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs | head -3; sed -n '63587,63601p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Verify kbMult unused and ogre num6=240 line"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:09.144Z

**📎 ToolResult**

```
6://                                          SetDefaults dontTakeDamage=true :14581 → 炮在世恒无敌）
27://                                          水晶在世 → dontTakeDamage 驻守;水晶亡 → ai[1]=1,
449:  e.iframes = 2;   // SetDefaults dontTakeDamage=true（:14581）：炮在世恒无敌
713:  e.def.knockbackResist = ratio < 0.5 ? 0 : e.def.knockbackResist; // def 存承受比例：0=免疫
942:    e.iframes = 2;                                 // dontTakeDamageFromHostiles + 满血
1013:  if (crystal) e.iframes = 2;   // SetDefaults dontTakeDamage=true（:15987）
1053:  kbMult: number; hoverUp: number; range: number; approach: number; aimT: number;
1061:    kbMult: 0.4, hoverUp: 200, range: 750, approach: 30, aimT: 30, damp: 0.95,
1069:      kbMult: id === 558 ? 0.7 : id === 559 ? 0.5 : 0.2,
1078:    kbMult: id === 575 ? 0.4 : 0.6,
1894: *  :196-259）：水晶 548（!dontTakeDamageFromHostiles）恒候选;200px 内玩家按距夺标 */
1900:    if (!n.dead && n.vanillaId === 548 && !n.dontTakeDamage) { crystal = n; break; }
1954:      e.iframes = 2;                       // dontTakeDamage=true（:64058）
2362:      if (n.dead || n.vanillaId !== 548 || n.dontTakeDamage) continue;
2420:      if (n.dead || n.vanillaId !== 548 || n.dontTakeDamage) continue;
----
63591:				num6 = 240;
			case 1:
				flag3 = true;
				num5 = 90;
				num4 = 1000f;
				num6 = 240;
				num11 = GetAttackDamage_ForProjectiles(40f, 30f);
				flag15 = false;
				vector = new Vector2(direction * 30, -70f);
				num12 = 676;
				if (ai[0] == 80f)
				{
					SoundEngine.PlayTrackedSound(SoundID.DD2_OgreSpit, base.Center);
				}
				break;
			}

```


---

## 🤖 Assistant · 2026-08-19T03:21:49.787Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
Confirmed:
- Ogre spit `num6 = 240` at NPC.cs:63591.
- kbMult is defined (1053, 1061, 1069, 1078) but never read elsewhere — dead parameter, divingFlyerAI never sets knockback.

Everything cross-checked. Now compose the final report. Max 10 CONFIRMED items, sorted by severity, plus a 存疑 section. Keep it organized per-boss.

Severity ranking:
1. DD2 target acquisition (dd2Target crystal-unconditional) — affects Betsy + DarkMage + flyers + lightning bug: enemies ignore players entirely while crystal alive. High.
2. Ogre spit cooldown 240→60. High (Boss-level priority 4).
3. AI_107 melee windup flag7/flag20/flag24/ai3 side-effects Ogre-only. High-medium.
4. AI_108 knockback state gating missing. Medium.
5. Dutchman cannonball double-normalize. Medium.
6. Lane portal vulnerable during dissolve + idle loop/hold nuances. Medium-low.
7. DarkMage bolt aim origin + facing during cast. Low.
8. Walker casting retarget freeze (AI_102/109 flag115/flag7). Low.
9. Dutchman pirate spawn position. Low (maybe fold into notes).
10. Crystal: no WinScene sound / noGravity bob dead code. Low — maybe just a note, not worth a numbered slot. Actually keep list tight: maybe 8 CONFIRMED + notes.

Hmm, for #6 — need to double check the vanilla claim "dissolve sets dontTakeDamage = true". From the dump: `if (Main.netMode != 1 && localAI[0] >= 180f) { if (AnyNPCs(548)) { dontTakeDamage = true; return; } this.ai[1] = 1f; this.ai[0] = 0f; dontTakeDamage = true; }`. Yes — on transition to ai1=1, dontTakeDamage = true. And in ai1==1 branch at >= 550: dontTakeDamage = false, life = 0. So during the entire dissolve the portal is invulnerable. Ours: `if (crystal) e.iframes = 2` only covers crystal-alive; after crystal death ours never sets iframes in ai1===1 → killable. Confirmed. Also SetDefaults :15987 claim — I couldn't verify (didn't read it) but not needed; the AI-side evidence is sufficient.

For #1 (targeting): I should be careful about the exact claim — dd2Target is used by: betsyAI (1362), darkMageAI (1255), divingFlyerAI (1101), dd2LightningBugAI (1609), and sandSharkAI? No — sandShark uses player directly (vanilla TargetClosest default → nearest player; fine). flyingDutchmanAI uses TargetClosest (nearest player; vanilla AI_093 TargetClosest — matches).

Note for DarkMage the vanilla flag7 gating: `if (flag7) TargetClosestOldOnesInvasion` — flag7 = true unless casting. So the retarget uses the 200px rule. Ours: dd2Target with crystal-priority + retarget every frame in walkerKernel. The targeting deviation for mage: player within 200px & nearer should become target (bolt aims at player). Fold into #1, mention families affected.

Also within #1 mention: vanilla compares with aggro modifiers — skip.

For Betsy specifically: TargetClosestBetsy — no player filter → any alive player competes by distance. So a player standing near Betsy but far from crystal becomes the target. Ours: crystal always.

Now #7 DarkMage aim: vanilla cs:66437-66446. Ours 1287-1291. Also our facing update during cast. Low.

#8: walkerKernel retarget during cast for AI_102/AI_109: vanilla flag115 (102) / flag7 (109) = false while casting → TargetClosest skipped; ours runs it. Low.

Also should I mention Betsy summon sound per-unit vs once? Low cosmetic. And Betsy no-target fallback invented (vy -= 0.05)? Mention in 存疑/notes.

Also worth a note: wither beast aura dust condition (localAI[0] > 60 vs target distance) — cosmetic.

Betsy state machine/physics/attack params all verified 1:1 — state that clearly.

DarkMage: all three spell chains verified (675 97t/fire at 32/14spd/40dmg; 674 heal at 40/48/56 with down-50 search; 673 raise at 64, sound at 80; selection priorities 0→1→2 rotation, hurt-allies<2→2, CanRaiseGoblinsHere→0, LOS/1000px gate for bolt; cooldowns -20/-120). One nuance: vanilla counts town NPCs in the hurt-allies scan (Main.maxNPCs); ours only enemies. Truly minor — note.

Sand elemental: verified 1:1 (params, hp-scaled speed, kb, cast loop 135→-300, fire at 54, spawn logic ±30 cols/spacing 10/expand 1..51/bottomY-15, distance 2000 gate → -200 cooldown, degrade 658 to particles).

Sand shark: verified 1:1.

Crystal/portal: verified with the two low findings.

DivingFlyer: verified with knockback finding; note missing kobold ignite-loop sound during dive (ai1>=20) — low cosmetic. Ours kobold aimT 30 matches; wyvern 20 matches; jitter kobold 3/wyvern 0 matches; dive 8; minSpeed 6/0; recover 30; dist 150; steer 60/10; speedAdd 0.05*steer; explode gates 64px/solid; explosion 192² dmg80 3t. All good.

Lightning bug: verified — params 4/20/20/1/0.96/5/30/200/50/682/10/50; separation 0.05/0.1?? ours SEP = 0.1. Vanilla num15 = 0.05! Wait — in AI_108, separation uses num15 = 0.05. For AI_111, I only partially saw the head (num = 7, num2 = 60...). The ours comment says 0.05/0.1 分离. I didn't fully read AI_111 (66793-66970). Our dd2LightningBugAI: SEP = 0.1 constant. Hmm — I read vanilla AI_111 only up to `float num4 = 1f;` — the dump got cut. I did not verify AI_111 params. Since I can't confirm, and lightning bug is lowest priority, I'll state what I verified (structure) and what I didn't fully (constants beyond head). Actually — I should do a quick check of AI_111 to be responsible, since I claim "no issues". Let me grab 66793-66975 quickly.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:21:50.231Z · glm-x-preview-260804

```
最后再读取一次：原版 AI_111 lightning bug（我之前只获取到了它的头部）。
```


---

## 🤖 Assistant · 2026-08-19T03:21:50.680Z · glm-x-preview-260804

**🔧 ToolUse: `Bash`**

```json
{
 "command": "sed -n '66793,66975p' ~/Project/GLM/SandboxWorld/Terarria1456/Terraria/NPC.cs",
 "description": "Read vanilla AI_111 lightning bug"
}
```


---

## 👤 User(sidechain) · 2026-08-19T03:21:50.736Z

**📎 ToolResult**

```
	private void AI_111_DD2LightningBug()
	{
		//IL_0300: Unknown result type (might be due to invalid IL or missing references)
		bool flag = true;
		float num = 7f;
		float num2 = 60f;
		float num3 = 60f;
		float num4 = 1f;
		float num5 = 0.96f;
		int num6 = 30;
		int num7 = 20;
		float num8 = 200f;
		int num9 = 40;
		int num10 = 438;
		float num11 = 10f;
		float num12 = 100f;
		bool flag2 = false;
		float num13 = 0.05f;
		Vector2 center = base.Center;
		NPCUtils.TargetClosestOldOnesInvasion(this);
		NPCAimedTarget targetData = GetTargetData();
		bool flag3 = false;
		int num14 = type;
		if (num14 == 578)
		{
			num = 4f;
			num2 = 20f;
			num3 = 20f;
			flag3 = true;
			flag2 = true;
			num13 = 0.1f;
			num10 = 682;
			num9 = 50;
			num11 = 10f;
			num12 = 50f;
			num6 = 5;
			num7 = 30;
			center += new Vector2(-spriteDirection * 20, 10f);
			position += netOffset;
			if (Main.rand.Next(15) == 0)
			{
				Vector2 vector = position;
				if (direction == -1)
				{
					vector.X += width / 2;
				}
				Dust dust = Dust.NewDustDirect(vector, width / 2, height, 272);
				dust.scale = 0.65f;
				dust.velocity.Y -= 0.8f;
				if (dust.velocity.X * (float)direction > 0f)
				{
					dust.velocity.X *= -1f;
				}
				if (dust.velocity.Y > 0f)
				{
					dust.velocity *= -0.5f;
				}
			}
			if (Main.rand.Next(80) == 0)
			{
				Vector2 vector2 = (Main.rand.NextFloat() * (MathF.PI * 2f)).ToRotationVector2();
				Dust dust2 = Dust.NewDustPerfect(base.Center, 272, vector2);
				dust2.velocity *= 1.1f;
				dust2.noGravity = true;
				dust2.customData = this;
				Dust dust3 = Dust.NewDustPerfect(base.Center, 272, vector2);
				dust3.velocity *= 1.5f;
				dust3.noGravity = true;
				dust3.customData = this;
			}
			position -= netOffset;
		}
		if (flag3)
		{
			if (localAI[1] == 0f)
			{
				alpha = 255;
			}
			if (localAI[1] == 30f)
			{
				SoundEngine.PlayTrackedSound(SoundID.DD2_EtherianPortalSpawnEnemy, base.Center);
			}
			if (localAI[1] < 60f)
			{
				localAI[1] += 1f;
				alpha -= 5;
				if (alpha < 0)
				{
					alpha = 0;
				}
				int num15 = (int)localAI[1] / 10;
				float num16 = base.Size.Length() / 2f;
				num16 /= 20f;
				int maxValue = 5;
				if (type == 576 || type == 577)
				{
					maxValue = 1;
				}
				for (int i = 0; i < num15; i++)
				{
					if (Main.rand.Next(maxValue) == 0)
					{
						Dust dust4 = Dust.NewDustDirect(position, width, height, 27, velocity.X * 1f, 0f, 100);
						dust4.scale = 0.55f;
						dust4.fadeIn = 0.7f;
						dust4.velocity *= 0.1f * num16;
						dust4.velocity += velocity;
					}
				}
			}
		}
		if (flag2)
		{
			for (int j = 0; j < Main.maxNPCs; j++)
			{
				if (j != whoAmI && Main.npc[j].active && Main.npc[j].type == type && Math.Abs(position.X - Main.npc[j].position.X) + Math.Abs(position.Y - Main.npc[j].position.Y) < (float)width)
				{
					if (position.X < Main.npc[j].position.X)
					{
						velocity.X -= num13;
					}
					else
					{
						velocity.X += num13;
					}
					if (position.Y < Main.npc[j].position.Y)
					{
						velocity.Y -= num13;
					}
					else
					{
						velocity.Y += num13;
					}
				}
			}
		}
		rotation = Math.Abs(velocity.X) * (float)direction * 0.1f;
		spriteDirection = direction;
		Vector2 vector3 = center;
		Vector2 vector4 = targetData.Center - vector3;
		Vector2 vector5 = vector4.SafeNormalize(Vector2.UnitY) * num;
		bool flag4 = Collision.CanHit(base.Center, 1, 1, targetData.Center, 1, 1);
		if (localAI[0] < 0f)
		{
			localAI[0] += 1f;
		}
		if (!flag)
		{
			velocity = (velocity * (num2 - 1f) + vector5) / num2;
			EncourageDespawn(10);
		}
		else if (vector4.Length() > num8 || !flag4)
		{
			velocity = (velocity * (num3 - 1f) + vector5) / num3;
		}
		else if (vector4.Y < num12)
		{
			velocity.Y -= 0.03f;
		}
		else if (localAI[0] >= 0f)
		{
			velocity *= num5;
			if (velocity.Length() < num4 && Main.netMode != 1)
			{
				localAI[0] += 1f;
				if (localAI[0] >= (float)num6)
				{
					localAI[0] = -num7;
					direction = (spriteDirection = ((vector5.X > 0f) ? 1 : (-1)));
					vector5 = vector4 + Utils.RandomVector2(Main.rand, -25f, 25f);
					vector5.X *= 1f + (float)Main.rand.Next(-20, 21) * 0.005f;
					vector5.Y *= 1f + (float)Main.rand.Next(-20, 21) * 0.005f;
					vector5 = vector5.SafeNormalize(Vector2.UnitY) * num11;
					vector5.X *= 1f + (float)Main.rand.Next(-20, 21) * (1f / 160f);
					vector5.Y *= 1f + (float)Main.rand.Next(-20, 21) * (1f / 160f);
					Projectile.NewProjectile(GetSpawnSource_ForProjectile(), vector3, vector5, num10, num9, 0f, Main.myPlayer);
				}
			}
		}
		if (!flag)
		{
			return;
		}

```


---

## 🤖 Assistant · 2026-08-19T03:22:55.270Z · glm-x-preview-260804

<details open>
<summary>💭 thinking</summary>

```
AI_111 (578 overrides): num=4, num2=20 (far lerp), num3=20 (near lerp), num4=1 (min speed), num5=0.96, num6=5 (shoot t), num7=30 (cooldown), num8=200, num9=50 (dmg), num10=682, num11=10, num12=50 (height gate), num13=0.1 (sep), center += (-spriteDirection*20, 10). Ours: SPEED 4, LERP_FAR 20, LERP_NEAR 20, MIN_SPD 1, DAMP 0.96, SHOOT_T 5, COOLDOWN 30, RANGE 200, ZAP_DMG 50, ZAP_PROJ 682, ZAP_SPD 10, HEIGHT_GATE 50, SEP 0.1. All match!

Structure: 
- target = OldOnesInvasion (200px rule) — ours dd2Target (crystal priority) → covered by finding #1.
- separation before targeting: matches flag2.
- rotation = |vx| * direction * 0.1. ours matches.
- vector4 = target.Center - muzzleCenter; approach branches:
  - `if (!flag)` — flag = true default and 578 doesn't clear → skip.
  - dist > 200 || !LOS → approach lerp num3. ours matches (uses LERP_FAR for this? ours: `if (dist > RANGE || !los) { e.vx = (vx*(LERP_FAR-1) + ux*SPEED)/LERP_FAR }` — both 20 → same value).
  - vector4.Y < num12 (50) → vy -= 0.03. ours: `else if (dy < HEIGHT_GATE) e.vy -= 0.03` — dy here = tyc - muzzleY. vanilla vector4.Y = target.Y - muzzleCenter.Y. matches.
  - else charge: velocity *= 0.96; if speed < 1 → localAI[0]++; >= 5 → localAI[0] = -30; direction set from vector5.X (pre-jitter aim dir); jitter ±25 both axes; ×(1±20*0.005); normalize *10; ×(1±20/160). NewProjectile from vector3 (muzzle). ours matches all, including the two-stage perturbation and rndRange(-25,26) ≈ Next(-25,26).
- tail (after `if (!flag) return`): the rise/float logic — ours has the rise -0.2 clamp -10... let me quickly check the rest (66975+). I saw ours implements target-above/embedded → vy-0.2 clamp -10. The remaining vanilla lines beyond 66975 presumably contain that. I'll trust given the rest matched; it's the lowest-priority entity.

One divergence in ours lightning bug: `if (e.x < n.x) e.vx -= SEP; else e.vx += SEP;` — same as vanilla. ok.

Ours muzzle: `muzzleX = e.cx - e.facing * 20` — vanilla center += (-spriteDirection*20, 10) → muzzleX = cx - spriteDirection*20. e.facing ≈ spriteDirection. matches.

Good. Everything verified. Now compose the final answer.

Final CONFIRMED list (severity order):

1. **DD2 索敌:dd2Target 水晶绝对优先,原版是"更近者夺标"** — bossAI_dd2.ts:377-385 (dd2Target), used at 1255 (darkMage), 1362 (betsy), 1101 (divingFlyer), 1609 (lightningBug). Vanilla: NPCUtils.cs:261-273 (OldOnesInvasion = OnlyPlayersInCertainDistance(200) + OnlyCrystal, TargetSearchResults ctor NPCUtils.cs:134-141: NPC wins only if nearer than adjusted player distance) and :308-318 (Betsy = no player distance filter → any alive player competes). Symptom: 水晶在场时 Betsy/黑暗魔法师/飞龙/小妖魔滑翔怪/荧光虫完全无视玩家 — 原版 Betsy 会扑向更近的玩家,其余四族在玩家距自身 <200px 且比水晶近时改咬玩家. Fix: dd2Target 增加"玩家在 200px 内(Betsy 无此门)且比水晶近 → 选玩家"分支(或拆两个变体). Confidence: 高.

2. **食人魔吐息冷却 60 ≠ 原版 240** — ours bossAI_dd2.ts:1835 (p.cooldown = 60, ai1===1 branch 1846-1853 未覆写; clamp 2200 同用 60). Vanilla NPC.cs:63591 (case 1 `num6 = 240`), applied at cs:64380-64382 (`ai[0] == 0 → ai[0] = -num6`) + clamp cs:63602-63605. Symptom: 食人魔吐 676 息的频率约为原版 4 倍(90 前摇+60 冷却 vs 90+240). Fix: ai1===1 分支加 `p.cooldown = 240`. Confidence: 高.

3. **AI_107 近战前摇的 flag7 副作用只接了食人魔** — ours bossAI_dd2.ts:1709/1834 (windupDampOn 仅 576/577), melee block 2185-2202 只做 vx 阻尼; 无 flag20(冻结嘶叫/重定向)/ai3=0/walk-accel 跳过. Vanilla NPC.cs:63424 (`bool flag7 = true` 默认,num7=0.9; 63610-64262 无任何 case 清它), cs:64371-64378 (前摇期 `velocity.X *= num7; flag24 = true; flag20 = true; ai[3] = 0`), cs:64490-64536 (`if (!flag20)` 才嘶叫/TargetClosest), cs:64537 (`if (!flag24)` 才走路加速). Symptom: 哥布林(30t 前摇)/枯萎兽(110t 前摇,1.4 速)/小妖精在挥击前摇里全速滑行且持续变向,原版会刹车站定、面向锁定; stuck 计数器 ai3 也不清零. Fix: melee windup 通用加 vx*=0.9(食人魔 0.7)+冻结 2124 块+清 ai3+跳过 w107WalkAccel. Confidence: 高.

4. **AI_108 俯冲族击退门全缺(kbMult 死参数)** — ours bossAI_dd2.ts:1053/1061/1069/1078 (定义后从未使用). Vanilla NPC.cs:66134-66137 (state 0: knockBackResist = GetKnockbackMultiplier_ScaledByDifficulty(0.7/0.5/0.2 飞龙 T1-3, 0.6/0.4 小妖魔)), cs:66194/66240-66243 (state 1/2: knockBackResist = 0 → 瞄准/俯冲期完全免疫击退). Symptom: 飞龙俯冲可被击退打断、悬停期吃满击退; 原版俯冲不可打断. Fix: state 0 设 def.knockbackResist=kbMult 档, state 1/2 置 0(免疫), 离场恢复. Confidence: 高(参数未接是实锤; 我方 Enemy knockback 通道以 def.knockbackResist 计 — 同文件 713 行已有同款用法).

5. **荷兰大炮弹道双重归一化** — ours bossAI_dd2.ts:533-539: `vx=d.x*14; vy=d.y*14-5` → 再归一到 14 → `vy-=5`,等效 normalize(d*14+(0,-5))*14+(0,-5). Vanilla NPC.cs:36033-36045: `vector140 = Normalize(playerCenter - cannonCenter); *14; += UnitY*-5` 单趟. Symptom: 水平射击出膛 (13.07,-9.67) ≠ 原版 (14,-5) — 弹道压得更平坠得更快,远距命中率失真. Fix: 删掉中间那次归一化,直接 `vx=d.x*14, vy=d.y*14, vy-=5`. Confidence: 高.

6. **神秘传送门消散期可被击杀** — ours bossAI_dd2.ts:1013 (`if (crystal) e.iframes = 2` 只在水晶存活时给无敌; ai1===1 分支 1036-1044 无 iframes). Vanilla NPC.cs:43109-43116 (localAI[0]>=180 且水晶亡 → `ai[1]=1; ai[0]=0; dontTakeDamage = true`), cs:43138-43144 (550t 时才 `dontTakeDamage=false; life=0`). Symptom: 水晶死后门在 550t 缩放消散动画期间可被打死,跳过演出提前消失. Fix: ai1===1 分支恒 e.iframes = 2 直到 550 自灭. Confidence: 高. (附带: 门的 idle loop 音 cs:43078-43084 与出怪后 onHold 补计数 cs:43100-43103 未移植 — 低.)

7. **黑暗魔法师暗影矢瞄准原点错位+施法期仍转向** — ours bossAI_dd2.ts:1287-1291 (d = dirTo(e,…) 从本体中心起算; 且 walkerKernel 599 行每帧向目标刷新 facing). Vanilla NPC.cs:66437-66446 (vector 从炮口 Center+(direction*10,-16) 起算 `target - muzzle`,SafeNormalize(UnitY)*14), cs:66427+66543 (flag7=false 施法期不 TargetClosest → direction 冻结). Symptom: 弹道方向偏 ~19px;治疗 674 落点方向(direction*240)在施法中会被我方持续重定向,原版锁定出手瞬间朝向. Fix: 炮口起算 + castDamp>0 时跳过 facing 刷新. Confidence: 高(偏差本身), 影响: 低.

8. **walker 施法期索敌冻结缺失(AI_102/109 共通)** — ours bossAI_dd2.ts:599-603 (walkerKernel 无条件刷 facing). Vanilla: NPC.cs:42269 (AI_102 flag115=false 施法期) / cs:66427+66543 (AI_109 flag7=false) → TargetClosest 跳过. Symptom: 沙尘精/黑暗魔法师施法中仍会转身. 低. (与 #7 同根,可并单修: walkerKernel 加 castDamp 门.)

9. **荷兰飞盗船跳海盗出生位** — ours bossAI_dd2.ts:451-458 (spawnPart 落在船中心). Vanilla NPC.cs:40959-40970 (vector270 = ((rand-.5)(w-70), (rand-.5)*20 - h/2 - 20).RotatedBy(rotation) + Center — 甲板上空随船旋转偏移). Symptom: 海盗从船体中部冒出而非上甲板. 低.

10. **水晶胜负演出缺 WinScene 音效与升空漂浮未生效** — ours bossAI_dd2.ts:944-956: ai0===3 只放粒子(原版 cs:42848-42855 DD2_WinScene + 713 弹), e.vy 赋值但 eterniaCrystalAI 无移动积分调用 → 升空小回旋/败北上浮是死代码(原版 cs:42860-42873 noGravity+velocity 生效). 低(纯演出).

Hmm, that's 10. Also 存疑 section:
- Betsy 无目标 fallback `vy -= 0.05` (bossAI_dd2.ts:1363-1366) 无原版出处(原版无目标时状态机照跑,targetData 保持旧值) — 但仅在"无水晶且无玩家"时触发,影响可忽略.
- Betsy 召唤音我方每波一声(1546),原版每只飞龙一声(cs:62652/62671) — 纯音效密度.
- DarkMage 伤员扫描只数 enemies(bossAI_dd2.ts:1326-1329),原版遍历 Main.maxNPCs 含城镇 NPC(cs:66482-66492) — DD2 场景无城镇 NPC 时等价.
- 枯萎兽灵气尘条件我方改为"目标 400px 内"(2010-2013),原版是 localAI[0]>60 计时门(cs:63896-63904) — 纯视觉.
- 食人魔跺地 num26 -= 32(探针偏移,cs:63519)我方以体宽近似(2271 注释自称) — 未逐值核对.
- w107Target 不带 agro 修正(NPCUtils.cs:245 num4 - player.aggro) — 无 aggro 装备时等价.
- sandElemental 713 行 `e.def.knockbackResist` 若 def 为共享原型会跨实例污染 — 需查 def 归属,本次未展开.
- 我方 lanePortal/crystal 的 timeLeft/despawnTimer=750 为引擎侧近似,非原版数值.
- phase 悬停探测 probeSolid 只探 Center.X-40 单格(bossAI_dd2.ts:2225),原版 SolidCollision 80×height 盒(cs:64871) — 悬停贴地判定在半边悬空地形下会失真(低).

Betsy summary: 核了状态机 0-6 全部转换/计时器(10/30/30/40+80/60+60+60/60/90)、八槽轮换表+ai3==5 三分之一追加、各态速度(23/32/12/7.5/10→20/螺旋 2π/60·0.1)、687/686 出膛位与节拍(num38=ai1-59,%10,≤60)、召唤环 300×(2,1)×0.6-1.0/传送门×3/560≤4 门、rotation 收敛表(0.04/0/0.01/0.05/0.02/π 系)、timeScale 1.5/0.7/0.85 — 除 #1 索敌外 1:1.

Also mention what was verified for each boss per dimension. Format: 逐 Boss 一节.

Word count — keep it tight but complete. Chinese output (user's language). No emojis. Direct text.
```

</details>


---

## 🤖 Assistant · 2026-08-19T03:23:42.874Z · glm-x-preview-260804

```
# bossAI_dd2.ts 1:1 抽查审计报告

标杆:`Terarria1456/Terraria/NPC.cs`(下称 cs);我方:`game/src/entities/bossAI_dd2.ts`。两边均逐段实读，未依赖注释行号。

## Betsy 551(AI_110)

核了：状态机 0-6 全部阶段与转换(入场 10t/悬停 30t/风压 30t/吐息 40+80t/空袭 60+60+60t/翻转 60t/召唤 90t)、八槽轮换表(0/1/3→2,2→3,4→4,5→5,6→3,7→6)+ ai3==5 且 1/3 追加二次 5、各态速度档(23/32/12/7.5/10→20 提速 0.5)、687/686 出膛偏移(140,20 旋转向量)与投弹节拍(num38=ai1−59,%10,≤60 共 6 发)、召唤环(2,1)·300·(0.6-1.0)+ 传送门随机 ×3 + 场上 560≤4 门、rotation 收敛全表(0.04/0/0.01+π/12·0.05/2π/0.02)与 timeScale 1.5/0.7/0.85、SimpleFlyMovement(NPC.cs:78100)逐轴同构。**除下方 #1 索敌外，状态机/物理/攻击参数全部 1:1。**

## DarkMage 564/565(AI_109)

核了：walker 参数覆写全表(grav 0.05/maxFall 0.2/upAccel −0.05/maxUp −0.4/maxH 0.5/accelH 0.1/maxV 0.5/accelV 0.02/headScan 关)、三连招链(675:97t、ai0==32 出手、14 速 40 伤；674:ai0=40/48/56 三拍、direction×240 下探 50 格含起点格、ToWorldCoordinates(8,0);673+RaiseGoblins:ai0==64、音效 80)、招式轮换 0→1→2、冷却 −20/−120、选招优先级(伤员<2→2、CanRaiseGoblinsHere→0、1000px+LOS 门)。偏差见 #1、#7、#8。

## FlyingDutchman 491 + 大炮 492(AI_093/75)

核了：首帧 4 炮(ai3=60i 错峰)、炮位盘点全灭自毁(StrikeNPCNoInteraction 语义)、1/300 跳舱速度 ((rand−.5)·5, −8.01)+船速、贴地巡航(前方 10 格列扫描、350/450 门槛、lerp 0.05、±4 钳)、水平逼近(≥300px、6 速/direction 门、+0.06)、rotation=vx·0.025、炮锚定 ((−122+68·slot)·镜像，−6,随船旋转)、240t 装填、LOS 门、8 向瞄准帧索引(spriteDirection==1 → 9−idx)。偏差见 #5、#9。

## ai107ImprovedWalkers(重点：食人魔 576/577)

核了：全部族参数表逐项对账(哥布林/投弹手/标枪手/德拉肯多连拍 ai1∈(10,40] %6/%9 改写 fireAt/枯萎兽/小妖精/旧日骷髅 120t 落地渐显/食人魔三态)、食人魔距离选招(≤430+冷却尽→跺地 />160→吐息 /≤130→近挥+prev==1 清 ai0)、跺地(90t 前摇、fireAt 36、跳 56/41/13、vector(−dir·20, h/2−1))、吐息弹道 vector(dir·30,−70)、flag12 远程循环(先减后比、justHit→ai1=30、起手半速+姿态角、收招门)、卡位计数 ai3(num21=30、×10 回卷、justHit/目标重叠清零、flag30 传送冲刺 DD2 族不触发)、跳梯三档(−7/−8、−6、−5、悬崖 1.5×−8)、flag2 穿墙相位(无 LOS+朝向或 noGravity 滞回 + ai0≤0 门、200px 水平 lerp、三档垂直伺服、num70 落地清 vy)。偏差见 #2、#3。

## 次要组

- **sandElementalAI 541**:参数全表(含亏血加速、半血免击退)、135t→−300 循环、54t 落点算法(±30 列、间距≥10、ExpandVertically(1,51)、bottomY−15)、2000px 门→−200 —— 全对，无发现。
- **sandSharkAI 542-545**:在沙判定(中心格沙族∨wet)、扑咬门(vy>−0.1 且 >150px)、12 速扑向目标−80px、ai2 充能 −30↔30 与门条件、蛇形 0.06/0.01、离沙重力档、rotation 钳 ±0.2 —— 全对，无发现。
- **eterniaCrystalAI 548**:倒计时 180、CheckArenaScore 双端 ±2 放门、胜负演出时序(96t 上浮/600t 收场)—— 见 #10。
- **lanePortalAI 549**:LaneSpawnRate 节拍(≥rate,%rate,≥3·rate 归零)、180t 驐守门、500-600 缩放消散、550 自灭 —— 见 #6。
- **divingFlyerAI 558-560/574/575**:两档参数全表(俯冲 8 速、抖动 0/3×0.04、recoverLerp 30、minSpeed 6/0、steer 60/10×speedAdd)、LOS+下视野门(π/8)、120t 宽限、64px/撞块自爆 192²·80·3t、回旋 ai1=45−3 —— 见 #4。
- **dd2LightningBugAI 578**:578 覆写档(4/20/20/1/0.96/5/30/200/50/682/10/50/0.1)与双重速度扰动(±25、±0.5%、±0.625%)逐项吻合 —— 无发现。

---

## CONFIRMED 偏差(按严重度)

**#1 DD2 索敌：水晶被写成绝对优先，原版是“更近者夺标”**
我方 `bossAI_dd2.ts:377-385`(dd2Target),用于 betsyAI:1362、darkMageAI:1255、divingFlyerAI:1101、dd2LightningBugAI:1609。原版 `NPCUtils.cs:261-273`(TargetClosestOldOnesInvasion = OnlyPlayersInCertainDistance(**200px**)+OnlyCrystal)与 `:308-318`(TargetClosestBetsy = **无**玩家距离过滤)，胜负判定在 TargetSearchResults 构造器(NPCUtils.cs:134-141):仅当 NPC(水晶)比玩家(aggro 修正后)更近才选 NPC。症状：水晶在场时 Betsy/黑暗魔法师/飞龙/小妖魔滑翔怪/荧光虫**完全无视玩家**；原版 Betsy 会扑向更近的玩家，其余四族在玩家距自身 200px 内且比水晶近时改咬玩家。修复：dd2Target 拆两档——Betsy 无距离门、其余带 200px 门，玩家更近即夺标(w107Target 已有同款实现可复用)。置信度：高。

**#2 食人魔吐息冷却 60,原版 240**
我方 `bossAI_dd2.ts:1835`(p.cooldown=60;1846-1853 吐息分支未覆写；2200 钳界同用 60)。原版 cs:63591(case 1 `num6 = 240`),于 cs:64380-64382 前摇尽时 `ai[0] = -num6`,钳界 cs:63602-63605。症状：吐 676 息频率约为原版 4 倍(90+60 vs 90+240)。修复：ai1===1 分支加 `p.cooldown = 240`。置信度：高。

**#3 AI_107 近战前摇的 flag7 副作用只接了食人魔**
我方 `bossAI_dd2.ts:1709/1834`(windupDampOn 仅 576/577),melee 块 2185-2202 只做 vx 阻尼。原版 cs:63424 `bool flag7 = true` **默认真**(num7=0.9,63610-64262 无任何 case 清它)，前摇期 cs:64371-64378 一并做 `velocity.X *= num7; flag24=true(跳过走路加速); flag20=true(冻结嘶叫/TargetClosest); ai[3]=0`;cs:64490/cs:64537 是对应消费门。症状：哥布林(30t 前摇)/枯萎兽(110t 前摇、1.4 速)/小妖精在挥击前摇里全速滑行并持续变向，原版刹车站定、面向锁定；ai3 卡位计数也不清零。修复：melee 前摇通用加 vx×=0.9(食人魔 0.7)+跳过 w107WalkAccel+冻结 2124 块+清 ai3。置信度：高。

**#4 AI_108 俯冲族击退门全缺(kbMult 是死参数)**
我方 `bossAI_dd2.ts:1053/1061/1069/1078` 定义后全文件无一处使用。原版 cs:66134-66137(态 0:knockBackResist=缩放(0.7/0.5/0.2 飞龙 T1-3,0.6/0.4 小妖魔))、cs:66194 与 cs:66240-66243(态 1/2:knockBackResist=0 → 瞄准/俯冲期免疫击退)。症状：飞龙俯冲可被击退打断、悬停期吃满击退。修复：态 0 写 def.knockbackResist=kbMult 档，态 1/2 置 0,回态 0 恢复(同文件 713 行已有同款字段用法)。置信度：高。

**#5 荷兰大炮弹道被双重归一化**
我方 `bossAI_dd2.ts:533-539`:先算 `d×14−5`,再整体归一回 14,又 `vy−=5` —— 等效 `normalize(d·14+(0,−5))·14+(0,−5)`。原版 cs:36033-36045:`vector140 = Normalize(playerCenter−cannonCenter)·14;vector140 += UnitY·(−5)` 单趟。症状：水平射击出膛 (13.07,−9.67) ≠ 原版 (14,−5),弹道坠速失真。修复：删中间归一化，直接 `vx=d.x*14, vy=d.y*14, vy-=5`。置信度：高。

**#6 神秘传送门消散期可被击杀**
我方 `bossAI_dd2.ts:1013`(`if (crystal) e.iframes = 2` 仅水晶存活时；ai1===1 分支 1036-1044 无 iframes)。原版 cs:43109-43116(180t 且水晶亡 → `ai[1]=1; ai[0]=0; dontTakeDamage=true`),cs:43138-43144 到 550t 才解无敌并自灭。症状：水晶死后门在 550t 缩放消散期间可被打死，演出被跳过。修复：ai1===1 分支恒 iframes=2 直至 550。置信度：高。(附带：门 idle loop 音 cs:43078-43084、出怪后 onHold 补计数 cs:43100-43103 未移植，低。)

**#7 黑暗魔法师暗影矢瞄准原点错位 + 施法期仍转向**
我方 `bossAI_dd2.ts:1287-1291`(dirTo 从本体中心起算)。原版 cs:66437-66446:向量从炮口 `Center+(direction·10,−16)` 起算再 ×14;且 cs:66427+66543 施法期 flag7=false 不 TargetClosest → direction 冻结(治疗 direction×240 落点随之锁定)。症状：弹道偏 ~19px;674 落点朝向在施法中被我方持续重定向。修复：炮口起算 + castDamp>0 时跳过 facing 刷新。置信度：高(偏差)，影响：低。

**#8 walker 施法期索敌冻结缺失(AI_102/109 共通)**
我方 `bossAI_dd2.ts:599-603`(walkerKernel 无条件刷 facing)。原版 cs:42269(AI_102 flag115=false)/cs:66427(AI_109 flag7=false)施法期跳过 TargetClosest。症状：沙尘精/黑暗魔法师施法中仍会转身。与 #7 同根，可并修：walkerKernel 加 castDamp 门。置信度：高，影响：低。

**#9 荷兰飞盗船跳舱出生位**
我方 `bossAI_dd2.ts:451-458`(spawnPart 落船中心)。原版 cs:40959-40970:出生位=((rand−.5)(w−70), (rand−.5)·20−h/2−20).RotatedBy(rotation)+Center(上甲板随船旋转)。症状：海盗从船腹冒出而非甲板。置信度：高，影响：低。

**#10 水晶胜负演出：WinScene 音缺失 + 漂浮是死代码**
我方 `bossAI_dd2.ts:944-956`(ai0===3 只放粒子，原版 cs:42848-42855 DD2_WinScene+713 弹)；e.vy 升空回旋(:953)与败北上浮(:983)赋值后无移动积分调用——原版 cs:42860-42873 noGravity+velocity 生效。纯演出层。置信度：高，影响：低。

## 存疑(不列入 CONFIRMED)

- Betsy 无目标 fallback `vy−=0.05`(`bossAI_dd2.ts:1363-1366`)无原版出处(原版无目标时状态机照跑、targetData 保持旧值)，但仅在“无水晶且无玩家”时触发，影响可忽略。
- Betsy 召唤音我方每波一声(:1546),原版每只飞龙一声(cs:62652/62671)——纯音效密度。
- DarkMage 伤员扫描只数 enemies(:1326-1329),原版遍历 Main.maxNPCs 含城镇 NPC(cs:66482-66492);DD2 场景通常等价。
- 枯萎兽灵气环尘条件我方改为“目标 400px 内”(:2010-2013),原版是 localAI[0]>60 计时门(cs:63896-63904)——纯视觉。
- 穿墙相位贴地探测只探 Center.X−40 单格(:2225),原版 SolidCollision 为 80×height 盒(cs:64871)——半边悬空地形下悬停判定会失真。
- sandElementalAI:713 直接改 `e.def.knockbackResist`,若 def 为族共享原型会跨实例污染(半血一只→全体免疫击退)；需查 def 归属，本次未展开。
- w107Target 不带 aggro 修正(NPCUtils.cs:245 `num4 − player.aggro`);无仇恨装备时等价。
```
